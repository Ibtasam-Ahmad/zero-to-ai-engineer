# Software Engineering for AI Developers

A model that works in a notebook is a prototype. A model that thousands of people rely on is a *software system*: it has an architecture, tests, logs, limits, security controls, a front end and a way to be rolled out and rolled back. This guide walks through the concepts behind the twelve notebooks of this module in order, from how to shape a single class to how a team ships a whole AI feature, and finally down to the hardware that decides how fast it all runs. Every idea is defined in plain words first, then made precise with a worked example, a formula or a comparison table. The glossary at the end collects every term.

The guide follows one thread: **each layer exists to make change safe**. Good classes make it safe to change one part. Tests make it safe to refactor. Profiling makes it safe to optimise. Limits, timeouts and security controls make it safe to face real traffic. Feature flags make it safe to launch.

---

## Part 1: Shaping code (notebooks 01 and 02)

### Classes, objects and encapsulation

A **class** is a blueprint; an **object** (or *instance*) is one thing built from it, with its own data. When Python looks up `obj.x`, it searches the instance first, then the class, then the base classes in a fixed order. A classic bug follows from this: a *mutable class attribute* (for example `history = []` written in the class body) is shared by every instance, so one object's training log appears in another's. Per-object state belongs in `__init__`.

**Encapsulation** means hiding the messy inside of an object behind a small, safe set of methods, like a car that exposes a steering wheel rather than the fuel injectors. Python does it by convention: `_name` means "internal, please don't touch", `__name` triggers **name mangling** (Python renames it to `_ClassName__name` so subclasses do not clash by accident), and `@property` turns a method into a validated attribute, for instance a `temperature` setter that rejects values outside $[0, 2]$.

**Dunder methods** (double-underscore methods such as `__len__`, `__iter__`, `__eq__`, `__enter__`, `__exit__`) let your objects work with Python syntax: `len(vocab)`, `for tok in vocab`, `with load_model() as m:`. A context manager's `__exit__` runs even when the body raises, which is how you guarantee that GPU memory or a file is released. **Dataclasses** generate `__init__`, `__repr__` and `__eq__` for you; `frozen=True` makes instances immutable (and hashable, so usable as dictionary keys), and `slots=True` removes the per-object `__dict__`, saving memory (24% per object in the notebook). **Enums** replace "magic strings" such as `"tset"` with a fixed set of named values that fail loudly when misspelt.

### Inheritance versus composition

**Inheritance** expresses "is-a" (`class B(A)` makes B a specialised A). **Composition** expresses "has-a" (a `ChatService` *has* an LLM client, a cache and a retry policy). The rule of thumb, "prefer composition over inheritance", comes from a counting argument. With $n$ independent optional features, covering every combination by subclassing needs

$$2^n - 1 \text{ classes},$$

while composition needs $n$ small components plugged into one class. For $n = 5$ that is 31 classes versus 5 parts.

**Polymorphism** means one piece of code works with many types. Python offers three flavours:

| Mechanism | How the "interface" is checked | Best for |
|---|---|---|
| Duck typing | not at all: if it has `.predict`, it works | quick scripts, scikit-learn style conventions |
| Abstract base class (`abc.ABC`) | at instantiation: a subclass missing an `@abstractmethod` cannot be created | a family of classes you own, with shared helper code |
| `typing.Protocol` | by a static type checker (and optionally `isinstance` with `@runtime_checkable`) without inheritance | accepting third-party objects (a scikit-learn pipeline, an SDK client) |

### Multiple inheritance and the MRO

When a class has several parents, Python computes a **method resolution order (MRO)** using **C3 linearisation**. The MRO of class $C$ with bases $B_1, \dots, B_k$ is

$$L[C] = C + \text{merge}(L[B_1], \dots, L[B_k], [B_1, \dots, B_k]),$$

where *merge* repeatedly takes the first head of a list that does not appear in the tail of any other list.

**Worked example.** `RobustClient(LoggingMixin, RetryMixin)`, where both mixins inherit from `BaseLLMClient`:

- $L[\text{LoggingMixin}] = [\text{Logging}, \text{Base}, \text{object}]$
- $L[\text{RetryMixin}] = [\text{Retry}, \text{Base}, \text{object}]$
- merge: take Logging (not in any tail); next head is Base, but Base is in the tail of Retry's list, so skip; take Retry; now take Base; then object.
- Result: `RobustClient → LoggingMixin → RetryMixin → BaseLLMClient → object`.

So `super()` inside `LoggingMixin` calls `RetryMixin`, a class it never mentions, and the expensive base call runs exactly once. When no consistent order exists, Python raises `TypeError: Cannot create a consistent method resolution order`.

### The SOLID principles

| Letter | Principle | One-line test | AI example of the fix |
|---|---|---|---|
| S | **Single responsibility** | does this class have exactly one reason to change? | split a "load CSV, clean, train, pickle" monolith into loader, cleaner, trainer and model store |
| O | **Open/closed** | can I add a new variant without editing existing code? | a model registry: `@register("ridge")` adds a model, `build_model` is untouched |
| L | **Liskov substitution** | can every subclass replace its parent without breaking callers? | a `ProbaPredictor` subclass must return values in $[0, 1]$ and accept a batch of any size |
| I | **Interface segregation** | is any client forced to depend on methods it does not use? | small roles (`Predicts`, `Trainable`, `Explainable`, `StreamsTokens`) instead of one fat backend interface |
| D | **Dependency inversion** | do high-level rules depend on abstractions, not on a vendor SDK? | a `TicketRouter` takes any `ChatModel`; tests pass a `FakeLLM`, production passes an adapter |

Liskov's principle is the subtle one. A subclass that *inherits* correctly can still *behave* incorrectly: a "probability" model that returns raw scores of −1.0 and 2.0 type-checks fine but breaks every threshold rule written against the parent. The textbook illustration is a `Square` inheriting from `Rectangle`: setting the width of a square also changes its height, which violates what callers of `Rectangle` expect.

Four further principles round this off: **DRY** (every piece of knowledge has one authoritative representation; duplicated preprocessing between training and serving causes *training/serving skew*), **KISS** (keep it simple), **YAGNI** (do not build for needs you do not have yet) and the **law of Demeter** (talk only to your immediate collaborators: `pipeline.token_id(word)`, not `pipeline.model.tokenizer.vocab[word]`). **Code smells** (long functions, deep nesting, magic numbers, long parameter lists) are warning signs that linters detect by walking the code's **abstract syntax tree**. A **UML class diagram** draws classes as boxes, inheritance as a solid line with a hollow triangle, and interface implementation as a dashed line.

### Design patterns

A **design pattern** is a named, reusable solution to a recurring design problem (the idea comes from the architect Christopher Alexander and was brought to software by the "Gang of Four" book in 1994). Patterns are vocabulary, not goals.

| Group | Pattern | Problem it solves in AI code | When *not* to use it |
|---|---|---|---|
| Creational | Factory / abstract factory | turn `"provider: rules"` in a config into the right object; build consistent families (an embedder and an index of the same dimension) | only one implementation exists |
| | Builder | assemble a prompt from optional parts, checking a context budget at the end | the object has two fields |
| | Singleton | "only one instance"; usually replaced by a module-level object or `functools.lru_cache` on a getter | almost always: it is hidden global state that leaks between tests |
| Structural | Adapter | give several vendor SDKs one interface | you control both sides |
| | Decorator | wrap retry, cache or timing around a call without changing it | the behaviour belongs inside the function |
| | Facade | one `ask()` method in front of a chunker, embedder, index and LLM | callers need fine control |
| | Proxy | stand-in that loads a heavy model only on first use | loading is cheap |
| Behavioural | Strategy | swap tokenisers or scoring functions at run time | a plain function argument does the job |
| | Observer | training callbacks: logging, early stopping, checkpointing | a single listener |
| | Template method | a fixed training skeleton; subclasses fill in `train_epoch` and `validate` | steps vary in order, not just content |
| | Chain of responsibility | a guardrails pipeline where any check may block, redact or pass | checks must all run in parallel |
| | Command | undoable, replayable data-cleaning steps | no undo or audit needed |
| | Iterator / generator | stream a corpus too big for memory | data fits in memory easily |
| Architectural | Dependency injection | pass collaborators in (FastAPI's `Depends`), so tests can override them | |
| | Repository | hide SQL behind `add()` / `recent()`, test with an in-memory version | trivial data access |
| | Plugin registry | other teams add metrics without editing core code | |
| | Pipeline / ETL | ordered small steps that report rows in and out | branching flows need a DAG orchestrator |
| | Event-driven | publish "document uploaded"; indexer, notifier and audit log react independently, failures go to a **dead-letter** list | you need an immediate, ordered answer |

Adapter, decorator and proxy all wrap another object, and the difference is a favourite interview question: an **adapter changes the interface**, a **decorator keeps the interface and adds behaviour**, a **proxy keeps the interface and controls access**.

---

## Part 2: Making code trustworthy (notebooks 03 and 04)

### Why and what to test

A **test** is code that checks other code automatically. The **testing pyramid** recommends many fast **unit tests** (one function or class, external services faked), fewer **integration tests** (several real components, such as code plus SQLite plus scikit-learn) and very few slow **end-to-end tests** (the whole deployed system). Tests run on every change in **continuous integration (CI)**.

pytest finds files named `test_*.py` and functions named `test_*`. Its progress line uses one character per test: `.` pass, `F` fail, `E` error in setup, `s` skipped, `x` expected failure, `X` unexpectedly passed. Its core features:

- **Fixtures** provide setup and teardown, injected by parameter name. Their **scope** (`function`, `module`, `session`) controls how often they are rebuilt; an expensive model can be built once per module while a mutable payload is rebuilt per test. Shared fixtures live in `conftest.py`.
- **`parametrize`** turns one test into a table of cases; **marks** label tests (`skip`, `skipif`, `xfail`, or custom ones like `slow`, selected with `-m "not slow"`).
- **`pytest.raises(Error, match=...)`** tests the unhappy paths; **`pytest.approx`** compares floats with a tolerance.

**Mocks and fakes.** A **mock** (`unittest.mock.MagicMock`) records how it was called and returns scripted values (`return_value`, or `side_effect` for a sequence of results or raised exceptions, perfect for testing retries). Two rules: create mocks with `spec=` so a typo such as `.compelte()` fails instead of silently "working", and **patch where a name is looked up, not where it is defined** (if `aikit/llm.py` does `import httpx`, patch `aikit.llm.httpx.post`). Often cleaner than patching is **dependency injection**: pass a `FakeLLM` into the constructor.

**Tolerances.** Floating-point results need tolerance-based assertions. NumPy's `assert_allclose` checks

$$|a - b| \le \text{atol} + \text{rtol} \cdot |b|.$$

`0.1 + 0.2 == 0.3` is false in binary floating point, while `pytest.approx` (default relative tolerance $10^{-6}$) accepts it. Summing 100,000 numbers in float32 differs from float64 in the fifth significant digit, so `rtol=1e-12` is too strict and `1e-5` is sensible for float32.

### Testing what is special about ML

| Question | Test type | Example |
|---|---|---|
| Is the data right? | **data validation** | required columns, dtypes, ranges, no duplicate IDs, allowed label values |
| Is training reproducible? | **deterministic training** | same seed gives identical weights; five seeds all exceed 90% accuracy with small spread; the model can overfit six examples |
| Does the model behave sensibly? | **behavioural (CheckList) tests** | MFT: "the movie was great" → positive; INV: changing a name does not change the label; DIR: adding "but the ending was awful" lowers P(positive) |
| Did a prompt change break answers? | **golden-set regression** | recorded responses on a frozen set; a snapshot test fails when the prompt template changes |
| Which code never ran? | **coverage** | read the missing lines, not just the percentage |

**Property-based testing** checks a rule over hundreds of generated inputs (for instance "cleaning is idempotent: `clean(clean(x)) == clean(x)`") instead of a few hand-picked ones. **Test-driven development (TDD)** writes a failing test first (red), the simplest code that passes (green), then tidies up (refactor). Seeing red first proves the test can fail; the notebook's chunking function shows how a second red test catches an infinite loop when `overlap >= max_words`.

### Debugging as a method

The **debugging loop** is the scientific method applied to code:

```
 reproduce (smallest input) -> isolate (first wrong value) -> hypothesise
        ^                                                          |
        |                                                          v
 add regression test  <-  fix the cause  <-  test the hypothesis (predict, check)
```

**Worked example.** Embedding 10 documents in batches of 4 with `n_batches = len(docs) // 4` gives 2 batches and loses 2 documents. Hypothesis: floor division drops the partial batch. Prediction: the number lost equals `len % batch_size`, and the bug vanishes when the length is a multiple of 4. Checking 210 cases confirms it. Fix: iterate `range(0, len(docs), batch_size)`; the correct count is $\lceil n / b \rceil$.

**Tracebacks** are read bottom-up. Python chains exceptions: "During handling of the above exception, another exception occurred" means a *second* bug in an error handler, while `raise NewError(...) from err` prints "The above exception was the direct cause", preserving the root cause.

**Logging** beats `print` because records carry a level (DEBUG < INFO < WARNING < ERROR < CRITICAL), a time-stamp and a logger name; handlers route them to different places with different thresholds; and loggers form a hierarchy (`rag.retriever` propagates to `rag`). Libraries should only call `logging.getLogger(__name__)`; applications configure handlers. Production logs are **structured** (one JSON object per line, with a request ID) and **redacted** (secrets masked before output).

**Assertions and invariants.** An **invariant** is a condition that must always hold at a point in a correct program: probability rows sum to 1, token IDs lie in $[0, V)$. Note that `python -O` removes `assert` statements, so checks that protect production must raise real exceptions.

### The silent numerical bugs of ML

| Bug | Symptom | How to catch it |
|---|---|---|
| NaN / overflow | loss becomes `nan`; naive softmax of large logits gives `inf/inf` | subtract the max before `exp`; `np.errstate(over="raise", invalid="raise")`; `np.isnan`, never `== nan` |
| Shape bug | `Q @ K` instead of `Q @ K.T` runs fine on square test matrices | use distinct sizes in tests (5 queries, 7 keys, $d = 4$) |
| Silent broadcasting | `(5, 1) - (5,)` becomes a 5×5 matrix; "MSE" 4.01 instead of 0.01 | assert shapes before element-wise operations |
| Data leakage | selecting features using all labels gives 0.795 CV accuracy on random labels | put every fitted step inside the cross-validated pipeline (honest result: 0.510) |
| Label misalignment | positional slicing after `dropna()` pairs rows with other rows' labels; accuracy falls from 0.906 to 0.524 | align by index, assert index equality |

### Profiling and performance

Donald Knuth's warning against premature optimisation continues: "yet we should not pass up our opportunities in that critical 3%". Profiling finds that 3%. Use `time.perf_counter()` for durations (monotonic, high resolution), `timeit` for micro-benchmarks, and `cProfile` + `pstats` for whole programs. In `pstats`, **`tottime`** is time inside a function itself and **`cumtime`** includes everything it calls: sort by `tottime` to find hotspots, by `cumtime` to find expensive call trees. Sampling profilers (py-spy, Scalene) have lower overhead; `line_profiler` shows per-line cost.

| Pattern | Typical gain | Why |
|---|---|---|
| Vectorise loops with NumPy | 10–1000× | the loop runs in compiled code |
| `functools.lru_cache` on a pure, slow function | proportional to repeat rate | 600 queries with 59 distinct: 541 hits |
| `set` instead of `list` for membership | grows with $n$ | hash lookup $O(1)$ average vs. scan $O(n)$ |
| Batch I/O (one commit, one write) | 100× or more | each `commit()` waits for the disk (`fsync`) |
| Avoid `iterrows` / `apply(axis=1)` | ~200× vs. vectorised | `iterrows` builds a `Series` per row |

Memory has its own tools: `tracemalloc` snapshots show which line allocated what; `sys.getsizeof` counts only the container (a list's pointer array, not its strings; a NumPy *view* reports about 128 bytes regardless of the data it sees). A Python `float` is a 24-byte object plus an 8-byte list pointer, so a list of floats takes about 32 bytes per number against 8 in a float64 array (4 in float32). Generators keep peak memory flat; pandas `category` dtype and downcasting cut memory by 90% or more. Basic NumPy slices, transposes and most reshapes are **views** sharing memory; fancy indexing and boolean masks make **copies**, so modifying a "batch" slice in place can silently change a cached array.

Big-O describes growth and ignores constants, so for small $n$ an $O(n^2)$ insertion sort can beat an $O(n \log n)$ merge sort (the notebook's crossover was around $n \approx 96$ for pure-Python versions), which is why production sorts switch to insertion sort for short runs.

---

## Part 3: The machine underneath (notebooks 05 and 06)

### Concurrency, parallelism and the GIL

**Concurrency** is structuring a program so several tasks make progress during overlapping time periods; **parallelism** is literally executing them at the same instant on several cores. A task is **I/O-bound** if its wall time is mostly waiting (CPU time ≈ 0) and **CPU-bound** if it is mostly computing (CPU time ≈ wall time). Measuring the ratio of `process_time()` to `perf_counter()` tells you which.

A **process** has its own memory; **threads** inside one process share memory. In CPython, the **Global Interpreter Lock (GIL)** lets only one thread execute Python bytecode at a time; it is released during blocking I/O, so threads speed up I/O-bound work (4 × 0.2 s sleeps: 0.80 s sequential, 0.21 s with 4 threads) but not CPU-bound pure Python (about 1×). Status as of late 2026: PEP 703 added an experimental free-threaded build in 3.13, PEP 779 made it officially supported but **optional** in 3.14, and the default `python` still has a GIL.

**Amdahl's law** bounds the speed-up from $p$ workers when a fraction $s$ of the work is serial:

$$S(p) = \frac{1}{s + \frac{1 - s}{p}}.$$

With $s = 0.1$ and $p = 8$: $S = 1 / (0.1 + 0.1125) \approx 4.7$, far below 8. Process pools add further overhead: every argument is **pickled**, piped and unpickled (sending a 40 MB array to 4 workers was slower than summing it locally), so use shared memory for big arrays and create pools once.

### Synchronisation and its hazards

A **race condition** occurs when the result depends on timing: `counter += 1` is a read, an add and a write, and two threads can interleave so one update is lost (126,445 of 400,000 counted in the notebook). A **critical section** is code that must not run in two threads at once, protected by a **mutex** (`Lock`). Variants: `RLock` (re-entrant: the same thread may acquire it again), `Semaphore(k)` (at most $k$ holders, for instance 3 GPU jobs), `Event` (a one-time "ready" signal), `Condition` (wait until a predicate holds) and thread-safe `queue.Queue`. A **bounded queue** gives **backpressure**: a fast producer blocks instead of filling memory.

A **deadlock** is a set of tasks each waiting for a resource another holds. It requires all four **Coffman conditions** at once: mutual exclusion, hold and wait, no preemption, circular wait. Breaking any one prevents it; the practical fix is a **global lock order** (always acquire lock A before lock B), plus timeouts. The dining-philosophers problem is the textbook case: everyone picking up the left fork first deadlocks; ordering forks by number fixes it. The **banker's algorithm** (Dijkstra) avoids deadlock by granting a request only if the resulting state is *safe* (some order lets every process finish); its safety check costs $O(m \cdot n^2)$ for $n$ processes and $m$ resource types.

### asyncio

`asyncio` runs many **coroutines** on one thread with an **event loop**: each `await` hands control back to the loop while waiting. `asyncio.gather` runs awaitables concurrently (three 0.2 s calls finish in 0.2 s, not 0.6 s); `create_task` starts one in the background; `asyncio.timeout` and `wait_for` cancel work that takes too long, by injecting `CancelledError` at the current `await` (which must be re-raised after cleanup). `gather(return_exceptions=True)` returns errors as values for partial results, while `TaskGroup` implements **structured concurrency**: one failure cancels the siblings and raises an `ExceptionGroup`. An `asyncio.Semaphore(k)` caps calls in flight.

Two resilience tools from this notebook reappear in system design:

- **Exponential backoff with full jitter**: wait a random time in $[0, \min(\text{cap}, \text{base} \cdot 2^k)]$ before retry $k$. Without jitter, 1,000 clients retry at exactly the same instants; with it, the spikes spread out (busiest 20 ms window: 200 retries without jitter vs. 59 with).
- **Token bucket**: a bucket holds at most $b$ tokens and refills at $r$ per second; each request spends one:

$$\text{tokens}(t) = \min\big(b,\ \text{tokens}(t_0) + r\,(t - t_0)\big).$$

With $b = 10$ and $r = 25/\text{s}$, 50 requests are granted by $(50 - 10) / 25 = 1.6$ s.

**Micro-batching** groups requests (up to 16 or 10 ms) to amortise a large fixed cost per call: 64 embedding requests became 4 API calls and finished more than twice as fast. The deadliest async pitfall is a **blocking call inside `async def`** (`time.sleep`, `requests.get`, heavy CPU): it freezes every coroutine on the loop (a 320 ms heartbeat gap in the notebook); move it to `asyncio.to_thread` or a process pool.

| Workload | Best tool |
|---|---|
| Many network calls (LLM APIs, databases) | `asyncio` with a semaphore, or a bounded thread pool |
| Blocking library with no async version | `ThreadPoolExecutor` / `asyncio.to_thread` |
| CPU-heavy pure Python | `ProcessPoolExecutor` / `multiprocessing` |
| NumPy / PyTorch heavy maths | the library's own threads (they release the GIL) or a GPU |

### What the operating system does

The **kernel** runs with full hardware privileges; programs run in **user space** and request services through **system calls** (`open`, `read`, `write`, `fork`), each costing a mode switch. That is why **buffering** matters: 100,000 raw `os.write` calls took 0.82 s against 0.19 s through Python's 8 KiB buffered file object.

A **program** is a file; a **process** is a running instance with a PID, memory, open files and a parent. Unix creates processes with **`fork`** (clone; returns 0 in the child and the child's PID in the parent) followed by **`exec`** (replace the program, keep the PID). Process states include running (R), sleeping (S), stopped (T) and **zombie** (Z: finished but not yet reaped by its parent's `wait()`); an **orphan** whose parent died is re-parented to PID 1 or a subreaper. A **context switch** saves one task's registers and loads another's; it is *voluntary* when the task blocks and *involuntary* when the scheduler preempts it.

### CPU scheduling, worked by hand

Four processes (arrival, burst): P1 (0, 7), P2 (2, 4), P3 (4, 1), P4 (5, 4). **Waiting time** = turnaround − burst, where turnaround = completion − arrival.

- **FCFS**: P1 0–7, P2 7–11, P3 11–12, P4 12–16. Waits 0, 5, 7, 7, average **4.75**.
- **SJF (non-preemptive)**: at $t = 7$ the shortest ready job is P3: P3 7–8, P2 8–12, P4 12–16. Waits 0, 6, 3, 7, average **4.00**.
- **SRTF (preemptive SJF)**: P1 0–2, P2 2–4, P3 4–5, P2 5–7, P4 7–11, P1 11–16. Waits 9, 1, 0, 2, average **3.00**.

| Algorithm | Preemptive | Optimal average wait? | Starvation? | Note |
|---|---|---|---|---|
| FCFS | no | no | no | **convoy effect**: short jobs stuck behind long ones |
| SJF | no | yes, among non-preemptive schedules with all jobs present | yes | needs burst estimates |
| SRTF | yes | yes, overall | yes | |
| Round robin (quantum $q$) | yes | no | no | good response time; $q$ too small means switching overhead |
| Priority | either | no | yes | fixed by **aging** |

### Memory management

Each process sees a private **virtual address space**, divided into fixed-size **pages** (commonly 4 KiB) mapped to physical **frames** by a **page table**. An address splits into page number and offset:

$$\text{page} = \lfloor \text{addr} / \text{size} \rfloor, \qquad \text{offset} = \text{addr} \bmod \text{size}.$$

With 4 KiB pages (`0x1000` bytes), address `0x03A7F` is page 3, offset `0xA7F`; if page 3 lives in frame 7, the physical address is `0x07A7F`. A missing page triggers a **page fault**. The **TLB** caches recent translations; with hit ratio $h$, TLB time $t_{\text{tlb}}$ and memory time $t_{\text{mem}}$, the effective access time is

$$\text{EAT} = h\,(t_{\text{tlb}} + t_{\text{mem}}) + (1 - h)\,(t_{\text{tlb}} + 2\,t_{\text{mem}}).$$

With 20 ns and 100 ns: $h = 0.80$ gives 140 ns; $h = 0.98$ gives 122 ns.

**Page replacement** on the classic reference string 7, 0, 1, 2, 0, 3, 0, 4, 2, 3, 0, 3, 2, 1, 2, 0, 1, 7, 0, 1 with 3 frames: FIFO 15 faults, LRU 12, Optimal (evict the page used furthest in the future) 9. FIFO suffers **Belady's anomaly**: on 1, 2, 3, 4, 1, 2, 5, 1, 2, 3, 4, 5 it makes 9 faults with 3 frames but 10 with 4. LRU and Optimal are *stack algorithms* and never show it.

The **stack** holds function frames (8 MiB per main thread on Linux by default, and Python's recursion limit is 1,000); the **heap** holds objects. A Python memory **leak** means something still references data you no longer need, such as an unbounded module-level list; a `deque(maxlen=50)` bounds it. **`mmap`** maps a file into virtual memory so pages load only when touched: `np.load(..., mmap_mode="r")` opened a 64 MiB file in milliseconds. **safetensors** stores an 8-byte header length, a JSON header (dtype, shape, byte offsets) and raw numbers, so it can be memory-mapped and contains nothing executable.

### Files, environment, signals and containers

A file's metadata lives in an **inode**; a **hard link** is a second name for the same inode (data survives deleting one name), a **symbolic link** is a file holding a path (it dangles if the target is removed). Permissions are `rwx` for owner, group and others; the **umask** removes bits from new files (umask 022 gives `-rw-r--r--`, umask 077 gives `-rw-------`). Every open file is a small integer **file descriptor**; 0, 1 and 2 are stdin, stdout and stderr. When stdout is a pipe (Docker, `kubectl logs`), Python **block-buffers** it, so log lines arrive late; use `python -u` or `PYTHONUNBUFFERED=1`.

**Environment variables** are copied to child processes and cannot leak back to the parent; they are the standard place for configuration and secrets. **Signals** are short OS messages: SIGINT (Ctrl+C), SIGTERM (polite stop, sent by `docker stop` and Kubernetes), SIGKILL (cannot be caught). A graceful server handles SIGTERM by finishing the current batch, saving a checkpoint and exiting with code 0. Exit codes follow conventions: 0 success, 1 general error, 2 usage error, 126 not executable, 127 command not found, and $128 + n$ for death by signal $n$ (143 = SIGTERM, 137 = SIGKILL, often the out-of-memory killer). Never build shell commands from user input with `shell=True`; pass a list of arguments.

A **container** is not a virtual machine: it is ordinary processes isolated by kernel **namespaces** (separate views of PIDs, mounts, network, users, hostnames) and limited by **cgroups** (CPU, memory, I/O quotas).

---

## Part 4: Talking to the world safely (notebooks 07 and 08)

### Layers, addresses and transport

Networks are layered so that each layer does one job:

```
 TCP/IP layer     Examples                  Unit       Address
 -------------    -----------------------   --------   ------------------
 Application      HTTP, DNS, TLS, SSE       message    URL, host name
 Transport        TCP, UDP                  segment    port (0-65535)
 Internet         IP (v4, v6)               packet     IP address
 Link             Ethernet, Wi-Fi           frame      MAC address
```

(The seven-layer OSI model splits application into application, presentation and session, and link into data link and physical.) **IPv4** addresses have 32 bits, **IPv6** 128. Private ranges are 10.0.0.0/8, 172.16.0.0/12 and 192.168.0.0/16. **CIDR** notation `address/prefix` keeps the first *prefix* bits for the network, so a /$p$ IPv4 network has $2^{32 - p}$ addresses and $2^{32-p} - 2$ usable hosts: /24 gives 256 and 254; a /16 (65,536 addresses) splits into 16 subnets of /20 (4,096 each). Membership is one bitwise AND of address and netmask. Binding a server to `127.0.0.1` accepts only local connections; `0.0.0.0` accepts connections on every interface (required inside a container).

**DNS** resolves names to addresses, checking `/etc/hosts` and caches before asking resolvers. **TCP** sets up a connection with a three-way handshake and delivers a reliable, ordered **byte stream** (two `send` calls may arrive as one `recv`, so applications need framing); **UDP** sends independent **datagrams** with no guarantee, fine for metrics.

### HTTP, TLS and REST

An HTTP message is a start line, `Name: value` headers, a blank line and an optional body. Status classes: 2xx success (200 OK, 201 Created), 3xx redirect, 4xx client error (400, 401 unauthenticated, 403 forbidden, 404, 413 too large, 415 unsupported media type, 422 validation failed, 429 too many requests), 5xx server error (500, 502, 503, 504). HTTP/1.1 reuses connections (keep-alive); HTTP/2 multiplexes streams over one TCP connection; HTTP/3 runs over QUIC on UDP.

**TLS** encrypts and authenticates the connection: the server presents a certificate chain signed by a trusted **certificate authority** for the requested host name. Disabling verification (`verify=False`) makes you blind to interception; the correct fix for a private certificate is to trust that specific certificate.

**REST** design models **resources** as nouns (`/v1/models/1`) acted on by methods. A method is **idempotent** if repeating it leaves the same state: GET, PUT and DELETE are; POST is not, unless the client sends an **idempotency key** that the server remembers. Good APIs also version their paths, paginate lists and return machine-readable errors.

### Streaming, CORS and latency

| | REST + JSON | Server-Sent Events | WebSocket | gRPC |
|---|---|---|---|---|
| Direction | request → response | server → client stream | both ways, any time | unary or streaming |
| Format | JSON text | `event:` / `data:` text lines | text or binary frames | binary protobuf over HTTP/2 |
| AI use | predictions | LLM token streaming | interactive chat, voice | service-to-service |

**Time to first token (TTFT)** is what streaming improves: a 200-word answer at 20 words per second takes 10 s in total, but the first word appears after about 0.05 s. **CORS** is a *browser* rule: before a cross-origin JSON `POST` the browser sends a **preflight** `OPTIONS` request and only lets the page read the response if `Access-Control-Allow-Origin` matches. It is not authentication; `curl` ignores it.

Transfer time is roughly

$$T \approx \text{RTT} + \frac{\text{size}}{\text{bandwidth}},$$

so a 2 KB call is dominated by the round trip (30 ms at home, 0.5 ms inside a data centre) and a 15 GB model by bandwidth ($15 \times 8{,}000 / 100 = 1{,}200$ s at 100 Mbit/s, 12 s at 10 Gbit/s). Reusing one HTTP client (connection keep-alive) cut median latency from about 91 ms to 9 ms even on localhost. Always set **timeouts**, retry only transient errors (429, 503) with jittered backoff, and verify **webhooks** with an HMAC signature plus a timestamp to block tampering and replay. Two classic failures differ by layer: **connection refused** returns almost instantly (nothing listens on that port, the kernel answers with a reset), while a **timeout** means nothing answered at all.

### The security mindset

Security protects **confidentiality, integrity and availability** (the **CIA triad**). **Threat modelling** with **STRIDE** asks, for each component, about Spoofing, Tampering, Repudiation, Information disclosure, Denial of service and Elevation of privilege, then ranks threats by likelihood × impact. Two design principles carry most of the weight: **defence in depth** (several independent layers) and **least privilege** (each user, key and agent gets only the permissions it needs).

**OWASP Top 10:2025** (web applications): A01 Broken Access Control (now including SSRF), A02 Security Misconfiguration, A03 Software Supply Chain Failures, A04 Cryptographic Failures, A05 Injection (including XSS), A06 Insecure Design, A07 Authentication Failures, A08 Software or Data Integrity Failures, A09 Security Logging and Alerting Failures, A10 Mishandling of Exceptional Conditions.

| Attack | Root cause | Fix |
|---|---|---|
| SQL injection (`root' --`) | input pasted into SQL text | parameterised queries |
| Command injection (`file.txt; rm -rf ~`) | input passed to a shell | list of arguments, no `shell=True` |
| Path traversal (`../../.env`, absolute paths) | joining user paths to a base folder | resolve the path and check it stays inside the base |
| XSS | untrusted text inserted as HTML | escape (`html.escape`, `textContent`), Content-Security-Policy |
| SSRF | server fetches attacker-chosen URLs (cloud metadata at 169.254.169.254) | parse the URL, allow-list scheme and exact host, block private ranges |
| Insecure deserialisation | `pickle.load` executes code while loading | safetensors / JSON for untrusted files |

### Identity and secrets

**Authentication** proves who you are; **authorisation** decides what you may do, on every request. Passwords must be stored as **salted, slow hashes** (argon2id, bcrypt, scrypt): a random **salt** per user makes identical passwords hash differently and defeats precomputed **rainbow tables**, and a deliberately slow, memory-hard function makes each guess cost a sizeable fraction of a second instead of a microsecond. A **JWT** is `base64url(header).base64url(payload).signature`; the payload is readable by anyone, so it holds claims, not secrets. Verification must pin the algorithm (reject `alg: none`), check `exp`, `aud` and `iss`, and use a long random key (a short key such as `"secret"` is cracked offline). **API keys** carry about 256 bits of entropy, so a fast SHA-256 of the key is a safe thing to store; show the key once. **RBAC** maps users to roles and roles to permissions, but you also need **object-level checks** ("is this chat *yours*?"), or a user with `chat:read` can read anyone's chat (a BOLA bug).

Secrets live in environment variables or a secrets manager, loaded from a `.env` file that is listed in `.gitignore`. A leaked key must be **rotated**, not just deleted, because Git history and forks keep it. Secret scanners match known prefixes plus high-**entropy** strings, where Shannon entropy per character is

$$H = -\sum_i p_i \log_2 p_i.$$

Supply-chain defences: pin versions, verify hashes (`pip install --require-hashes`), run `pip-audit`, watch for **typosquatting** (`reqeusts`) and treat downloaded model files as code unless they are in a non-executable format.

### LLM-specific risks

The **OWASP Top 10 for LLM Applications (2025)** lists LLM01 Prompt Injection, LLM02 Sensitive Information Disclosure, LLM03 Supply Chain, LLM04 Data and Model Poisoning, LLM05 Improper Output Handling, LLM06 Excessive Agency, LLM07 System Prompt Leakage, LLM08 Vector and Embedding Weaknesses, LLM09 Misinformation and LLM10 Unbounded Consumption. Practical lessons from the notebook:

- **Prompt injection cannot be fully filtered**: a paraphrased attack slipped past the input regexes and was caught only by a later output check. So defend in layers and limit what a tricked model can do.
- **Excessive agency** is fixed with scopes, caps and human approval: small refunds run, a 120 refund waits for a human, 5,000 hits a hard cap, `delete_account` does not exist as a tool.
- **Improper output handling**: never `eval` model output; parse it with `ast.literal_eval` or a strict schema, and run generated SQL under a read-only, column-restricted authoriser.
- **Data poisoning**: 60 poisoned samples out of 2,060 planted a backdoor trigger while both models scored 100% on clean test data; hashing approved data files catches tampering.
- **Unbounded consumption** ("denial of wallet"): a typical user cost $0.36 a day, an unthrottled attacker script $36,288 a day; token caps, per-user rates and daily budgets brought it to $1.00.

Security logs should be tamper-evident: in a **hash chain**, each entry stores the hash of the previous one, so editing entry 1 breaks verification from entry 1 onwards.

---

## Part 5: Systems, front ends and shipping (notebooks 09, 10 and 11)

### The design method and estimation

Every design problem follows the same method: clarify requirements (functional and non-functional, and what is out of scope), estimate scale, define the API and data model, draw the high-level design, deep-dive the hardest parts, and name the bottlenecks. Estimation needs one constant: a day has 86,400 seconds (about $10^5$).

**Worked example (LLM chat app).** One million users sending 20 messages a day: $2 \times 10^7 / 86{,}400 \approx 231$ requests per second on average, about 694 at a 3× peak. At 400 output tokens each, peak output is $694 \times 400 \approx 277{,}800$ tokens per second; at 2,500 tokens per second per GPU replica that is about 112 replicas. **Little's law** links the three quantities of any stable queue:

$$L = \lambda W,$$

(items in the system = arrival rate × time in system). 40 requests per second lasting 1 s each means 40 in flight, 10 per server across 4 servers.

### Scaling and load balancing

**Vertical scaling** buys a bigger machine; **horizontal scaling** adds machines, which requires **stateless** services (session data in a shared store). Load-balancing policies: round robin, random, least connections, and **power of two choices** (sample two servers, pick the less loaded), which gets most of least-connections' benefit at a fraction of the cost. Equal request *counts* are not equal *load*: a server that receives a few long requests piles up work under round robin.

**Consistent hashing** places servers and keys on a ring and assigns each key to the next server clockwise. Adding one server to $N$ moves only about $1 / (N + 1)$ of the keys, whereas `hash(key) mod N` moves about $N / (N + 1)$: going from 5 to 6 servers moved 17.1% of keys (ideal 16.7%) against 83.3%. **Virtual nodes** (many ring positions per server) even out the load: with 100 per server the busiest node was within about 12% of the mean.

### Caching

| Pattern | Read path | Write path | Risk |
|---|---|---|---|
| Cache-aside | app checks cache, on miss reads DB and fills cache | write DB, *delete* cache entry | brief staleness |
| Write-through | read cache | write cache and DB together | slower writes |
| Write-back | read cache | write cache, flush to DB later | data loss on crash |

With hit ratio $h$, average latency is $h \cdot t_{\text{cache}} + (1 - h) \cdot t_{\text{miss}}$: at $h = 0.9$, 1 ms hits and 50 ms misses average $0.9 + 5 = 5.9$ ms. **Eviction**: LRU removes the least recently used item, LFU the least frequently used; on a static Zipf (power-law popularity) workload LFU won at every size, while on a shifting workload LRU adapted better. A **TTL** bounds staleness. A **cache stampede** happens when a hot key expires and every concurrent request hits the database (50 queries); **single-flight** (one request recomputes, the rest wait) reduces it to 1. A **CDN** is a geographically distributed cache for static content.

### Databases at scale

**Replication** copies data for durability and read capacity. With asynchronous leader-follower replication, **replication lag** means a user can miss their own write (13.3% of reads-after-write in the notebook); **read-your-writes** routing fixes it. In leaderless systems with $N$ replicas, writes acknowledged by $W$ and reads from $R$ always overlap if

$$W + R > N,$$

by the pigeonhole principle (N = 3, W = 2, R = 2 is typical). **Sharding** splits data across machines by key; skewed popularity creates **hot keys** (one user produced 13.5% of requests), which **key salting** spreads out. A **B-tree index** turns a full scan into a logarithmic search (about 4,800× faster on 200,000 rows).

The **CAP theorem** (Brewer 2000, proved by Gilbert and Lynch 2002) says that during a network **partition** a distributed store must choose between **consistency** (linearisability) and **availability**. **PACELC** adds the normal case: *else*, when there is no partition, choose between **latency** and **consistency**.

### Asynchronous processing and resilience

Work that can wait (thumbnails, emails, embeddings) goes into a **message queue** consumed by background workers. Delivery guarantees are *at-most-once*, *at-least-once* and *effectively-once*; at-least-once is the norm, so handlers must be **idempotent**. In the notebook, 6 redelivered payment messages charged customers twice under a naive handler (340 collected instead of 280); an **idempotency key** table fixed it. Messages that keep failing go to a **dead-letter queue** for inspection.

| Rate limiter | Idea | State per client | Notes |
|---|---|---|---|
| Token bucket | refill $r$/s up to $b$ | 2 numbers | allows bursts up to $b$ |
| Leaky bucket | FIFO of size $b$ drained at $r$/s | a queue | smooth output, adds delay |
| Fixed window | count per calendar window | 1 counter | up to 2× the limit across a boundary |
| Sliding window log | timestamps of recent accepts | up to *limit* timestamps | exact, most memory |
| Sliding window counter | current count + previous count × overlap | 2 counters | close approximation |

A **circuit breaker** stops calling a failing dependency: CLOSED (normal) → OPEN after $k$ consecutive failures (fail fast) → HALF_OPEN after a cool-down (one trial call) → CLOSED on success or OPEN again on failure. **Bulkheads** give each dependency its own worker pool so a slow one cannot starve the others (4 fast calls took 0.61 s behind 8 slow ones in a shared pool and 0.02 s with bulkheads).

### Observability and reliability targets

**Observability** rests on three signals: **logs** (events), **metrics** (numbers over time) and **traces** (the path of one request through services, drawn as a waterfall). Latency is reported as **percentiles**, not averages: in the notebook the mean was 112 ms while p50 was 81 ms and p99 1,113 ms. An **SLI** is a measured indicator (fraction of successful requests), an **SLO** is the target (99.9%), and the **error budget** is what the target allows:

$$\text{budget} = (1 - \text{SLO}) \times \text{requests}.$$

At 500 requests per second, 30 days is $1.296 \times 10^9$ requests, so 99.9% allows 1,296,000 failures, equal to 43.2 minutes of full outage. The **burn rate** is the error rate divided by the budgeted rate; a 50× burn exhausts a month's budget in under a day, which is what alerts watch for. Availability composes: components in **series** multiply ($0.999^2 \approx 0.998$), while **redundant** components in parallel give $1 - \prod_i (1 - A_i)$ (two 99% replicas: 99.99%).

| Availability | Downtime per 30 days | Downtime per year |
|---|---|---|
| 99% | 7.2 h | 3.65 days |
| 99.9% | 43.2 min | 8.77 h |
| 99.99% | 4.32 min | 52.6 min |

### Connecting a model to a front end

A web AI app has four parts: the **browser**, the **frontend** (HTML, CSS and JavaScript running in the browser, readable by anyone, so it holds no secrets), the **API** (validation, authentication, logging, limits) and the **model** (behind the API, loaded once at start-up through a *lifespan* hook). A browser can talk to the server in four ways: JSON request/response (`fetch` + `POST /predict`), multipart **file upload** (with explicit 413, 415 and 400 errors), **SSE** for one-way streaming and **WebSockets** for two-way chat (with an `Origin` check, since WebSockets are not covered by CORS).

On the server, a plain `def` endpoint runs in FastAPI's thread pool, and a streaming generator should stop when the client disconnects (the Stop button then actually saves GPU time). A strict **Content-Security-Policy** limits which scripts may run, and model output is inserted with `textContent`, never `innerHTML`. Good AI **UX** sets a **latency budget** (the notebook's client p95 of 28 ms met a 100 ms budget), streams anything longer than about a second, always offers cancel, shows low confidence honestly (a 0.56 "positive" for "It is a lamp." is flagged as unsure), and logs 👍/👎 feedback together with the model version and input. Streamlit and Gradio build such pages in a few lines of Python for demos; React is the usual choice for products.

### Shipping a feature end to end

The capstone notebook applies everything to one ticket-triage feature. The order matters:

```
 design doc -> clean architecture -> tests -> profile -> security review
     -> thin API + page -> logs and metrics -> CI with quality gate
     -> feature flag + canary rollout -> monitoring -> retrospective
```

- **Design doc**: goals, non-goals, success metrics (macro-F1 ≥ 0.85), latency and cost budgets ($0.085 per 1,000 tickets against a $0.50 budget), risks.
- **Clean architecture**: a pure **domain** layer (categories, priority rules), interfaces (`TicketClassifier`, `LLMClient` as Protocols), adapters (a fake LLM and an OpenAI-compatible client), and typed settings read from environment variables. Dependencies point inwards, so the domain never imports FastAPI or scikit-learn.
- **Tests**: 25 tests at first, over 50 by the end, all offline; the HTTP client is tested against a **mock transport** that plays the provider.
- **Profiling**: one batching change made the backfill 32× faster with identical outputs.
- **Security review**: PII redaction before the LLM call, input and output guards, rate limits per tenant, secrets hidden from `repr`.
- **CI**: lint → tests on two Python versions → a **model-quality gate** on the frozen golden set → dependency audit. (YAML pitfalls: `on` parses as `True` in YAML 1.1 tools, and `3.10` written unquoted becomes `3.1`.)
- **Rollout**: a **feature flag** with a **kill switch**; tenants enabled when $\text{hash}(\text{tenant}) \bmod 100 < \text{rollout\%}$, so a tenant enabled at 5% stays enabled at 25%, 50% and 100%.
- **Monitoring**: review rate, accuracy, acceptance of drafts, and data drift measured by the **population stability index**

$$\text{PSI} = \sum_i (a_i - e_i) \ln \frac{a_i}{e_i},$$

where $e_i$ and $a_i$ are the expected and actual shares in bin $i$ (rule of thumb: below 0.1 stable, above 0.25 a major shift). On simulated day 15, new product vocabulary pushed PSI to 0.26 and the review rate to 40%; the alerts fired, and the **blameless retrospective** turned the incident into concrete actions.

**Why it matters.** Every step after the model was trained (profiling, security, flags, monitoring) decided whether the feature could ship, and none of them changed its accuracy.

---

## Part 6: The hardware underneath (notebook 12)

Profiling (Part 2) tells you *where* the time goes. Computer architecture tells you *why*: in most AI code the arithmetic units are idle, waiting for data. This part follows the classic university sequence (digital logic, computer organisation, computer architecture) and ends at GPUs and LLM inference.

### From bits to numbers

An $n$-bit **unsigned integer** $b_{n-1} \dots b_0$ has value $\sum_i b_i 2^i$ and range $0 \dots 2^n - 1$. **Hexadecimal** writes 4 bits per digit, so a byte is two hex digits (`200` = `11001000` = `0xC8`). In **two's complement**, the top bit has weight $-2^{n-1}$:

$$\text{value} = -b_{n-1} 2^{n-1} + \sum_{i < n-1} b_i 2^i, \qquad \text{range } -2^{n-1} \dots 2^{n-1} - 1.$$

To negate, flip every bit and add 1. Worked by hand: $5$ = `00000101`, flip → `11111010`, add 1 → `11111011` = $-5$; adding `00000101 + 11111011` gives `1 00000000`, and the carry falls off the 8 bits, leaving 0. The same adder therefore serves signed and unsigned numbers, and there is only one zero. **Overflow** wraps silently in NumPy and PyTorch integer arrays: int8 $127 + 1 = -128$ and $100 + 50 = -106$ ($150 - 256$). Python's own `int` never overflows, which hides this until you use tensors.

**IEEE-754 floating point** is scientific notation in base 2. A normal number is stored as sign $s$, biased exponent $e$ and fraction $f$:

$$x = (-1)^s \times 1.f_2 \times 2^{\,e - \text{bias}}, \qquad \text{bias} = 2^{k-1} - 1 \text{ for a } k\text{-bit exponent}.$$

An all-zero exponent field means zero or a **subnormal** (no hidden 1); all ones means infinity or NaN. Worked by hand: $0.15625 = 0.00101_2 = 1.01_2 \times 2^{-3}$, so $s = 0$, $e = -3 + 127 = 124$ = `01111100`, fraction `0100…0`, giving `0x3E200000`. The value $0.1$ has no finite binary expansion (like $1/3$ in decimal), so fp32 stores $0.10000000149…$ and `0.1 + 0.2 == 0.3` is `False`: compare floats with a tolerance.

| Format | Exponent / mantissa bits | Max | Machine epsilon | ≈ decimal digits | Typical AI use |
|---|---|---|---|---|---|
| fp32 | 8 / 23 | $3.4 \times 10^{38}$ | $1.19 \times 10^{-7}$ | 7.2 | master weights, accumulators |
| fp16 | 5 / 10 | 65,504 | $9.77 \times 10^{-4}$ | 3.3 | inference; training needs loss scaling |
| bf16 | 8 / 7 | $3.39 \times 10^{38}$ | $7.81 \times 10^{-3}$ | 2.4 | mixed-precision training |
| fp8 E4M3 | 4 / 3 | 448 | 0.125 | about 1 | H100-class forward passes |

The exponent bits set the **range**, the mantissa bits the **precision**. In fp16, $300 \times 300$ overflows to `inf` and a gradient of $10^{-8}$ underflows to 0; bf16 handles both coarsely. That is why fp16 training multiplies the loss by a large factor (**loss scaling**) and bf16 usually does not. Adding 1.0 five thousand times in fp16 gets stuck at 2048, because there the gap between neighbouring fp16 numbers is 2; mixed-precision training therefore keeps **fp32 master weights and accumulators**.

**Symmetric int8 quantisation** uses a scale $s = \max|x| / 127$, stores $q = \text{round}(x/s)$ clipped to $[-127, 127]$ and reconstructs $\hat{x} = s \cdot q$. Storage drops 4× versus fp32 and each rounding error is at most $s/2$. Products of int8 values are summed in **int32** so the accumulator cannot overflow; the notebook's int8 layer stayed within about 1.3% of the fp32 result. Outliers inflate $\max|x|$ and make every step coarse, which is why LLM quantisers use per-channel or per-group scales.

### Logic gates, adders and the ALU

A transistor is a switch; a few switches make a **logic gate**. **NAND** is *functionally complete*: NOT, AND, OR and XOR can all be built from it. A **half adder** gives sum $= A \oplus B$ and carry $= AB$; a **full adder** adds a carry-in: sum $= A \oplus B \oplus C_{in}$, $C_{out} = AB + C_{in}(A \oplus B)$. Chaining $n$ full adders gives a **ripple-carry adder** whose delay grows as $O(n)$, because each carry waits for the previous one. A **carry-lookahead** adder such as Kogge–Stone computes all carries as a *parallel prefix scan* over (generate, propagate) pairs in $O(\log n)$ levels: 4 levels instead of 16 carry steps for 16 bits.

The **ALU** (arithmetic logic unit) reuses the adder for subtraction, $A - B = A + \text{NOT}\,B + 1$, and outputs **flags**: Z (zero), N (negative), C (carry out: unsigned overflow) and V (signed overflow: same-sign inputs, different-sign result). A comparison such as `a < b` is a subtraction whose result is discarded and whose flags drive the branch.

A perceptron $\text{step}(w \cdot x + b)$ with suitable weights *is* a logic gate (AND, OR, NAND), and a sigmoid makes it a smooth, trainable "soft" gate. XOR is not linearly separable, so no single perceptron computes it, but two layers (OR and NAND feeding AND) do: the historical argument for hidden layers.

### The CPU: fetch, decode, execute, pipeline, predict

A CPU repeatedly **fetches** the instruction at the **program counter (PC)**, **decodes** it, **executes** it (ALU or memory access) and **writes back** the result to a **register**, then advances the PC or jumps. The notebook's toy CPU computes a 4-element dot product (300) in 31 instructions.

**Pipelining** overlaps the five classic stages (IF, ID, EX, MEM, WB), like a laundry where load 2 washes while load 1 dries. Ideally $n$ instructions take $n + k - 1$ cycles on a $k$-stage pipeline instead of $kn$, so the cycles per instruction (**CPI**) approach 1. **Hazards** break the ideal: a **data hazard** (with forwarding, only a load immediately followed by a use stalls 1 cycle), a **control hazard** (which instruction follows a branch?) and a **structural hazard** (two instructions need the same unit).

| Model for the 31-instruction trace | Cycles | CPI |
|---|---|---|
| no pipeline (5 cycles each) | 155 | 5.00 |
| ideal pipeline | 35 | 1.13 |
| stall on every branch | 47 | 1.52 |
| predict "taken" (wrong only on loop exit) | 41 | 1.32 |

A **branch predictor** guesses outcomes ahead of time; the classic **2-bit saturating counter** changes its prediction only after two misses in a row. On random bytes, the branch `x >= 128` is a coin flip (simulated miss rate 0.5); on sorted bytes it changes once (miss rate ≈ 0.00002). The compiled loop ran about 5× slower on unsorted data, because each miss flushes a 15–20-stage pipeline. The fix is not sorting ($O(n \log n)$) but **branchless code** (`np.where`, masks, `data[data >= 128]`).

### The memory hierarchy

Fast memory is small and expensive, so computers stack levels: registers → L1 (~32–64 KB per core, ~1 ns) → L2 (~0.25–2 MB, ~4 ns) → L3 (shared, ~4–100+ MB, ~10–20 ns) → DRAM (~80–100 ns) → SSD (~20–100 µs) → network. If an L1 hit took one second, a DRAM access would take about a minute and a half and a Europe–US round trip several years. Data moves in **cache lines** of 64 bytes, and caches pay off thanks to **temporal locality** (used again soon) and **spatial locality** (neighbours used soon).

The notebook measures its own caches by **pointer chasing** (each load gives the address of the next, so loads cannot overlap): about 3 ns per load while the working set fits in L1, rising past L1 and L2, and about 100 ns once it spills to RAM. The biggest jump can come before the reported L3 size because L3 is shared and the TLB starts missing.

NumPy, C and PyTorch store arrays in **row-major** order (`order="C"`); Fortran, MATLAB and R are **column-major**. **Strides** give the bytes to step along each axis: a $2048 \times 2048$ float64 array has strides $(16384, 8)$ and its transpose, a free **view**, has $(8, 16384)$. Summing columns of a row-major array uses 8 bytes of every 64-byte line and was 4.7× slower than summing rows. A stride sweep shows the cost per element climbing until the stride reaches 64 bytes (one line per element). `np.ascontiguousarray` (or `.contiguous()` in PyTorch) pays for one copy that pays off when the data is reused.

### SIMD and the roofline model

**SIMD** (single instruction, multiple data) processes a short vector per instruction: AVX2 handles 8 float32 values (256 bits), AVX-512 16, ARM has NEON/SVE. A million multiply-adds took about 0.1 s in a Python loop and under 1 ms in NumPy or numba (over 100× faster): no interpreter work per element, plus several elements per instruction. Strict IEEE rules forbid reordering a float sum, so numba needs `fastmath=True` to vectorise it.

The **roofline model** (Williams, Waterman and Patterson, 2009) asks whether a kernel is limited by arithmetic or by memory. With **arithmetic intensity** $I$ = FLOPs ÷ bytes moved, peak compute $P$ and memory bandwidth $\beta$:

$$\text{attainable FLOP/s} \le \min(P,\; I \beta), \qquad \text{ridge point } I^* = \frac{P}{\beta}.$$

Kernels with $I < I^*$ are **memory-bound** (move fewer bytes: fuse, use smaller dtypes); those with $I > I^*$ are **compute-bound**. Worked by hand in float32: `c = a + b` does $n$ FLOPs and moves $12n$ bytes, so $I = 1/12 \approx 0.083$; an $n \times n$ matmul does $2n^3$ FLOPs on at least $12n^2$ bytes, so $I = n/6 \approx 171$ for $n = 1024$. On the notebook's single core ($\beta \approx 17.7$ GB/s, $P \approx 65.6$ GFLOP/s, $I^* \approx 3.7$), element-wise kernels are memory-bound and large matmuls reach the compute roof.

### GPUs and transformer arithmetic intensity

A CPU has a few clever cores optimised for **latency**; a GPU has thousands of simple lanes optimised for **throughput**, hiding memory latency by keeping many threads in flight.

| GPU concept | Meaning |
|---|---|
| SM (streaming multiprocessor) | the GPU's "core"; an H100 SXM has 132 |
| Warp | 32 threads executing one instruction in lock-step (SIMT); divergent branches run one after the other |
| Shared memory | fast on-chip memory per SM, used for tiling (as in FlashAttention) |
| HBM | high-bandwidth memory: about 2–3.35 TB/s on A100/H100 |
| Coalescing | a warp's consecutive addresses merged into a few wide transactions |
| Tensor cores | units doing small matrix multiply-accumulates in fp16/bf16/fp8/int8 |
| Occupancy | resident warps per SM; more warps hide more latency |

With published dense bf16 peaks, the ridge point is about $312 / 2.04 \approx 153$ FLOP/byte on an A100 and $989 / 3.35 \approx 295$ on an H100. A linear layer $d_{in} \to d_{out}$ applied to $T$ tokens in bf16 does $2 T d_{in} d_{out}$ FLOPs and moves about $2(d_{in} d_{out} + T d_{in} + T d_{out})$ bytes, so for $T = 1$ its intensity is about 1 FLOP/byte. For the $4096 \to 11008$ MLP projection it crosses the A100 ridge at a few hundred tokens and the H100 ridge somewhat later. Hence **prefill** (many prompt tokens at once) is compute-bound and **decoding** (one token per step) is memory-bound; decode-time attention stays near 1 FLOP/byte whatever the batch size.

A quick bound: every decoding step reads all weights once, so tokens/s at batch 1 $\le \beta / \text{weight bytes}$. A 7B model in bf16 (13.5 GB) on an H100 gives at most about 248 tokens/s; int4 (3.4 GB) about 994. The KV cache of Llama-2-7B is $2 \times 32 \text{ layers} \times 4096 \times 2$ bytes = 0.5 MiB per token, 2 GiB for one 4,096-token conversation, which limits how many users fit on a GPU. Batching, weight quantisation, KV-cache tricks (grouped-query and paged attention) and speculative decoding all attack this one bottleneck.

### Measuring the machine and a performance checklist

`os.cpu_count()` reports **logical CPUs** (with SMT/hyper-threading, two per physical core), `psutil` gives physical cores, frequency and RAM, and `/sys` reports cache sizes on Linux. In containers use `len(os.sched_getaffinity(0))`, and beware **oversubscription**: 8 processes × 8 BLAS threads on 8 cores is 64 threads fighting for the same cores.

| Habit | Hardware reason | Measured gain in the notebook |
|---|---|---|
| Batch calls | amortises per-call overhead, raises intensity | about 1,400× |
| Vectorise | no interpreter overhead, SIMD | about 96× |
| Keep data contiguous | full use of each cache line | 2.6× |
| Avoid copies (in-place, `out=`) | less memory traffic and peak RAM | 3× less peak memory |
| Choose the dtype (float32 over float64) | half the bytes, twice the SIMD lanes | 2.3× |
| Fuse element-wise steps | memory-bound chains read the data once | (by design) |
| Measure first | optimise the real bottleneck | (Part 2) |

**Why it matters.** Mixed-precision training, LLM quantisation, FlashAttention (tiling so the $n \times n$ attention matrix never reaches HBM), continuous batching and llama.cpp on laptops are all applications of these few ideas: number formats, the memory hierarchy and arithmetic intensity.

---

## Complexity summary

| Operation | Cost | Notebook |
|---|---|---|
| `x in list` | $O(n)$ | 04 |
| `x in set`, dict lookup | $O(1)$ average | 04 |
| LRU cache get/put (hash map + doubly linked list) | $O(1)$ | 06, 09 |
| Banker's algorithm safety check | $O(m \cdot n^2)$ | 06 |
| FIFO / LRU page replacement with a hash map | $O(1)$ per reference | 06 |
| Consistent-hashing lookup (sorted ring, binary search) | $O(\log(N v))$ for $N$ servers with $v$ virtual nodes | 09 |
| B-tree index lookup | $O(\log n)$ | 09 |
| Full table scan | $O(n)$ | 09 |
| Sliding-window-log rate limiter memory | $O(\text{limit})$ per client | 09 |
| Insertion sort vs. merge sort | $O(n^2)$ vs. $O(n \log n)$, but insertion wins for small $n$ | 04 |
| Ripple-carry vs. carry-lookahead (Kogge–Stone) $n$-bit addition | $O(n)$ vs. $O(\log n)$ gate delays | 12 |
| $n$ instructions on a $k$-stage pipeline | $n + k - 1$ cycles (ideal) vs. $kn$ unpipelined | 12 |
| Matrix multiply $C = AB$, $n \times n$ | $2n^3$ FLOPs on $\ge 12n^2$ bytes (fp32): intensity $n/6$ | 12 |

---

## Glossary

- **Abstract base class (ABC)** — a class with abstract methods that subclasses must implement before they can be instantiated.
- **Adapter** — a wrapper that converts one interface into the one your code expects.
- **ALU** — the arithmetic logic unit: the circuit that adds, subtracts and compares, setting the Z, N, C and V flags.
- **Amdahl's law** — the speed-up limit $1/(s + (1-s)/p)$ imposed by a serial fraction $s$.
- **API key** — a long random secret that identifies a program rather than a person.
- **Arithmetic intensity** — FLOPs performed per byte moved to or from main memory.
- **asyncio** — Python's library for running many coroutines concurrently on one thread with an event loop.
- **Authentication / authorisation** — proving identity / checking permissions.
- **Backpressure** — slowing a producer (for example with a bounded queue) so it cannot overwhelm a consumer.
- **Banker's algorithm** — deadlock avoidance that grants a request only if the resulting state is safe.
- **Belady's anomaly** — FIFO page replacement causing more faults with more frames.
- **bf16 (bfloat16)** — 16-bit float with 8 exponent and 7 mantissa bits: fp32's range with less precision.
- **Branch prediction** — guessing a conditional branch's outcome so the pipeline keeps running; a miss flushes it.
- **Bulkhead** — separate resource pools per dependency so one failure cannot starve the rest.
- **Cache line** — the 64-byte block in which data moves between cache and RAM.
- **CAP theorem** — during a partition, a distributed store must choose consistency or availability.
- **Cache stampede** — many requests recomputing the same expired cache entry at once.
- **Chain of responsibility** — a line of handlers, any of which may stop or change a request.
- **CheckList** — behavioural testing of NLP models with minimum-functionality, invariance and directional tests.
- **CI (continuous integration)** — automatically running tests and checks on every change.
- **CIA triad** — confidentiality, integrity, availability.
- **CIDR** — `address/prefix` notation for IP networks.
- **Circuit breaker** — stops calls to a failing dependency (closed, open, half-open).
- **Coalescing** — merging a GPU warp's consecutive memory accesses into a few wide transactions.
- **Coffman conditions** — the four conditions required for deadlock.
- **Composition** — building objects from parts ("has-a") instead of inheritance ("is-a").
- **Consistent hashing** — a hash ring on which adding a server moves only about $1/(N+1)$ of keys.
- **Context switch** — saving one task's state and loading another's on a CPU.
- **CORS** — a browser rule controlling which origins may read cross-origin responses.
- **Coverage** — the share of code lines (or branches) that tests executed.
- **cProfile** — Python's deterministic per-function profiler.
- **Data leakage** — test or future information influencing training.
- **Deadlock** — tasks each waiting forever for a resource another holds.
- **Dead-letter queue** — where messages that keep failing are parked for inspection.
- **Decorator (pattern)** — a wrapper that adds behaviour while keeping the interface.
- **Defence in depth** — several independent security layers.
- **Dependency injection** — passing collaborators in from outside instead of creating them inside.
- **Design pattern** — a named, reusable solution to a recurring design problem.
- **Dunder method** — a `__double_underscore__` hook that connects objects to Python syntax.
- **Error budget** — the failures an SLO permits: $(1 - \text{SLO}) \times$ requests.
- **Event loop** — the scheduler that runs coroutines and resumes them when their I/O is ready.
- **Exit code** — a process's return status; $128 + n$ means killed by signal $n$.
- **Facade** — a simple front door to a complex subsystem.
- **Feature flag / kill switch** — configuration that turns a feature on for some users, or off for all, without a deploy.
- **File descriptor** — the small integer the OS uses for an open file or socket.
- **Fixture** — reusable test setup injected by pytest.
- **fork / exec** — Unix calls to clone a process / replace its program.
- **fp16 (half precision)** — 16-bit float with 5 exponent and 10 mantissa bits; maximum 65,504.
- **GIL** — CPython's lock letting one thread run Python bytecode at a time.
- **Golden set** — a frozen labelled set used to compare model or prompt versions over time.
- **Idempotent** — safe to repeat: the same request twice leaves the same state.
- **Idempotency key** — a client-chosen ID that lets the server ignore duplicate requests.
- **IEEE-754** — the floating-point standard: sign, biased exponent and fraction bits.
- **Inode** — the file-system record holding a file's metadata and data location.
- **Invariant** — a condition that must always hold at a point in a correct program.
- **JWT** — a signed token of the form header.payload.signature.
- **Least privilege** — granting only the permissions needed.
- **Liskov substitution** — subclasses must be usable wherever their parent is.
- **Little's law** — $L = \lambda W$ for any stable queue.
- **Locality (temporal / spatial)** — data used recently, or stored next to used data, is likely to be used soon.
- **Loss scaling** — multiplying the loss in fp16 training so small gradients do not underflow to zero.
- **LRU / LFU** — evict the least recently / least frequently used item.
- **Memory-bound / compute-bound** — limited by memory bandwidth / by arithmetic throughput.
- **mmap** — mapping a file into memory so pages load on demand.
- **Mock** — a test double that records calls and returns scripted results.
- **MRO / C3** — the order Python searches base classes, computed by C3 linearisation.
- **Mutex** — a lock allowing one holder at a time.
- **Namespaces and cgroups** — kernel features that isolate and limit container processes.
- **NAND** — the "not and" gate; functionally complete, so every logic circuit can be built from it.
- **Observer** — subscribers notified of events without the source knowing them.
- **Oversubscription** — more busy threads than cores, so they fight for the same hardware.
- **OWASP Top 10** — the consensus list of critical web (and, separately, LLM application) risks.
- **PACELC** — if partitioned, availability vs. consistency; else latency vs. consistency.
- **Page / frame / page fault** — fixed-size virtual memory unit / physical slot / access to a page not in RAM.
- **Percentile (p50, p95, p99)** — the latency below which that share of requests falls.
- **Pickle** — Python serialisation that can execute code on load; unsafe for untrusted data.
- **Pipelining / hazard** — overlapping instruction stages / a dependency that forces the pipeline to stall.
- **Port** — a 16-bit number identifying a program on a host.
- **Process / thread** — a running program with its own memory / a unit of execution sharing a process's memory.
- **Program counter (PC)** — the register holding the address of the next instruction.
- **Prompt injection** — text that makes an LLM ignore its instructions.
- **Property-based test** — checking a rule over many generated inputs.
- **Protocol (typing)** — a structural interface checked without inheritance.
- **Proxy** — a stand-in that controls access to a real object, for example lazy loading.
- **PSI** — population stability index, a drift measure between two distributions.
- **Quantisation** — storing values in fewer bits (int8, int4) with a scale factor.
- **Quorum** — read and write replica counts with $W + R > N$.
- **Race condition** — a result that depends on unpredictable timing.
- **RBAC / BOLA** — role-based access control / broken object-level authorisation.
- **Repository** — a collection-like interface that hides data storage.
- **REST** — API style built on resources, HTTP methods and status codes.
- **Roofline model** — attainable FLOP/s $\le \min(P, I\beta)$; the ridge point $P/\beta$ separates memory-bound from compute-bound.
- **Salt** — random per-password data that makes identical passwords hash differently.
- **Semaphore** — a counter allowing at most $k$ holders at once.
- **Sharding** — splitting data across machines by key.
- **Signal** — an OS notification to a process (SIGINT, SIGTERM, SIGKILL).
- **SIMD** — single instruction, multiple data: one instruction operating on a short vector (AVX2, AVX-512, NEON).
- **SLI / SLO** — a measured service indicator / its target.
- **SM (streaming multiprocessor)** — a GPU "core" with its own registers, shared memory and tensor cores.
- **SOLID** — single responsibility, open/closed, Liskov, interface segregation, dependency inversion.
- **SSE** — Server-Sent Events: a one-way text stream over HTTP, used for token streaming.
- **SSRF** — tricking a server into requesting attacker-chosen URLs.
- **STRIDE** — spoofing, tampering, repudiation, information disclosure, denial of service, elevation of privilege.
- **Strategy** — a swappable algorithm object.
- **Strides / contiguous** — bytes to step along each array axis / rows packed back to back in memory.
- **Subnormal** — a tiny float with an all-zero exponent field and no hidden leading 1.
- **System call** — a request from a program to the kernel.
- **TDD** — test-driven development: red, green, refactor.
- **Tensor core** — a GPU unit that does a small matrix multiply-accumulate per instruction in low precision.
- **TLB** — the CPU cache of virtual-to-physical page translations.
- **TLS** — the encryption and authentication layer under HTTPS.
- **Token bucket** — a rate limiter refilling $r$ tokens per second up to $b$.
- **TTFT** — time to first token in a streamed response.
- **TTL** — time to live: how long a cached entry stays valid.
- **Two's complement** — signed integer encoding in which negation is "flip all bits and add 1".
- **Typosquatting** — malicious packages named like popular ones.
- **View vs. copy** — a NumPy array sharing another's memory vs. owning its own.
- **Warp** — 32 GPU threads executing the same instruction in lock-step (SIMT).
- **WebSocket** — a persistent two-way connection upgraded from HTTP.
- **XSS** — cross-site scripting: untrusted text executed as HTML/JavaScript in a victim's browser.
