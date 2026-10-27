# Advanced Algorithms

This module is the follow-up to [`../dsa/`](../dsa/). It covers what an MS-level **Design and Analysis of Algorithms** course teaches (randomized and amortized analysis, NP-completeness, approximation, network flows, linear programming, streaming, geometry and the FFT, advanced data structures, parallel and external-memory algorithms), plus a tested **coding-interview workbook**. It is an **optional, university-level track**: nothing else in the repo depends on it, but it is recommended for BS/MS AI students, people revising for qualifying exams, and anyone heading into senior engineering or ML-engineering interviews.

**Why an AI engineer needs this.** The core DSA module teaches you to make ordinary code fast. This module is about the problems that are too big, too hard or too spread out for ordinary code, and those are exactly the problems AI systems run into:

1. **LP and MILP inside ML and MLOps.** L1 regression, the L1-SVM, optimal transport, MAP inference and ReLU-network verification are linear or mixed-integer programs. So are GPU job scheduling, ad-budget allocation and capacity planning. A solver gives you the provably best plan plus *shadow prices* that tell you what one more GPU-hour is worth.
2. **Sketches for big data.** You cannot keep every click, request or token in memory. HyperLogLog counts unique users in 3 KB, Count-Min finds heavy hitters, MinHash-LSH removes near-duplicates from LLM training corpora, and quantile sketches give p99 latency on dashboards.
3. **Approximation when the exact answer is NP-hard.** Optimal feature subsets, the smallest decision tree, optimal k-means, exact Bayesian-network inference and most scheduling problems are NP-hard. Knowing this tells you to stop searching for a perfect algorithm and to pick one with a proven guarantee, such as the greedy (1 − 1/e) rule used for diverse RAG context selection.
4. **Parallel algorithms for GPUs and clusters.** Work and span explain why 8 GPUs rarely give 8× speed-up (Amdahl's law), why GPUs love prefix sums (the scan behind Mamba), how FlashAttention's tiling is cache blocking, and why PyTorch DDP uses ring all-reduce.

> **Before you start:** finish (or at least skim) the core [DSA module](../dsa/) and the [discrete mathematics module](../../14_Mathematics/discrete_math/). Each notebook lists its own exact prerequisites at the top.

---

## The whole topic explained simply

The first DSA course asks "how do I solve this problem fast?". This course asks harder questions: what if the problem has **no known fast solution**, what if the data is **too big to store**, and what if the work is **split across many machines**? Think of a city planner. Some jobs are easy and exact (how much water can the pipes carry to the city? That is max flow). Some jobs are impossibly hard to do perfectly (the shortest route through every street), so the planner accepts a route that is **provably no more than 50 % longer** than the best. Some jobs involve too much data (counting every car that passes a bridge all year), so the planner keeps a tiny notebook of estimates instead of a photo of every car. And some jobs are split among many workers, where the slowest step that only one person can do limits everyone (painting a fence goes faster with friends, but fetching the paint does not). The tools in this module are the formal versions of these ideas: **reductions** to prove hardness, **approximation ratios** to promise quality, **linear programming** to find the best plan under limits, **sketches** with $(\varepsilon, \delta)$ error bounds, and the **work-span** model for parallel speed-up.

**Tiny worked example (real numbers).** A delivery van must visit **20 cities** and return home by the shortest route (the travelling salesperson problem, TSP).

| Approach | What it does | Work needed | Quality |
|---|---|---|---|
| Try every route | check all 19!/2 ≈ 6.1 × 10¹⁶ different tours | at 10⁹ tours per second, about 2 years | exact |
| Held–Karp dynamic programming | remember the best path for each (set of visited cities, last city) | n²·2ⁿ = 400 × 1,048,576 ≈ 4.2 × 10⁸ steps: about a second in C, minutes in Python | exact, but doubles with every extra city |
| Christofides approximation | spanning tree + matching + shortcuts | polynomial, milliseconds | at most **1.5 ×** the best (when distances obey the triangle inequality) |
| 2-opt local search | keep swapping two edges while the tour gets shorter | fast in practice | no guarantee, usually within a few % |

Same problem, four trade-offs between time and certainty. Choosing among them, and proving which guarantees hold, is what this module teaches.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | BS/MS AI and data-science students taking a second algorithms course ("Design and Analysis of Algorithms", "Advanced Algorithms", "Algorithms for Big Data", "Parallel and Distributed Computing"); people revising for MS admission or PhD qualifying exams; engineers preparing for senior SWE / ML-engineering interviews. |
| **Prerequisites** | The core [DSA module](../dsa/), especially [complexity and recursion](../dsa/01_complexity_analysis_and_recursion.ipynb), [hashing](../dsa/04_hashing.ipynb), [graphs](../dsa/07_graphs.ipynb), [greedy and divide and conquer](../dsa/08_greedy_and_divide_and_conquer.ipynb) and [dynamic programming](../dsa/09_dynamic_programming.ipynb). From [discrete mathematics](../../14_Mathematics/discrete_math/): [proofs](../../14_Mathematics/discrete_math/01_sets_relations_functions_and_proofs.ipynb), [combinatorics and recurrences](../../14_Mathematics/discrete_math/02_combinatorics_and_recurrences.ipynb), [graph theory](../../14_Mathematics/discrete_math/03_graph_theory.ipynb) and [computability](../../14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb). Basic [probability](../../14_Mathematics/03_probability.ipynb) for notebooks 01 and 06; [NumPy](../../02_Data_Analysis/02_numpy.ipynb) throughout. |
| **Time needed** | About 30 hours for notebooks 01–08 and 10 (about 3 hours each), plus the interview workbook (1 hour to read, then a 4-week practice plan). |
| **Runs on** | CPU only, no API key, no internet. Each notebook runs in about one to three minutes. Notebook 10 uses at most 4 worker processes. |
| **Optional?** | Yes. University-level fundamentals track; recommended, not required. |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Amortized and randomized algorithms](01_amortized_and_randomized_algorithms.ipynb) | Three ways to prove "cheap on average over a sequence", union-find, and algorithms that flip coins (quicksort, universal hashing, skip lists, treaps, Miller–Rabin, Karger). | 3 h |
| 02 | [NP-completeness and reductions](02_np_completeness_and_reductions.ipynb) | P, NP, NP-hard and NP-complete, certificate checkers, a DPLL SAT solver, reductions written as tested code, and why knapsack DP is only pseudo-polynomial. | 3 h |
| 03 | [Approximation and parameterized algorithms](03_approximation_and_parameterized_algorithms.ipynb) | Fast algorithms with a proven "at most X times worse than optimal" (vertex cover, set cover, TSP, knapsack FPTAS, k-center), FPT algorithms, and submodular greedy for RAG. | 3 h |
| 04 | [Network flows and matching](04_network_flows_and_matching.ipynb) | Max flow, min cut, bipartite matching and the Hungarian algorithm, applied to image segmentation, tracking and ticket routing. | 3 h |
| 05 | [Linear and integer programming](05_linear_and_integer_programming.ipynb) | Modelling with LPs, a simplex method from scratch, duality and shadow prices, branch-and-bound for integer programs, and modelling tricks. | 3 h |
| 06 | [Streaming and sketching algorithms](06_streaming_and_sketching_algorithms.ipynb) | One-pass, tiny-memory summaries: reservoir sampling, heavy hitters, Count-Min, HyperLogLog, MinHash-LSH, quantile sketches and sliding windows. | 3 h |
| 07 | [Computational geometry and the FFT](07_computational_geometry_and_fft.ipynb) | Orientation tests, convex hulls, sweep lines, polygons, Voronoi/Delaunay, and the FFT for fast polynomial multiplication and convolution. | 3 h |
| 08 | [Advanced data structures](08_advanced_data_structures.ipynb) | Sparse tables, suffix arrays, interval trees, KD-trees, red-black trees, persistent structures, LSM trees, gap buffers and ropes. | 3–4 h |
| 09 | [Coding interview workbook](09_coding_interview_workbook.ipynb) | A 7-step method and 45 tested problems in 15 patterns, a complexity-timing harness, Python idioms and six ML-flavoured coding questions. | 1 h + 4 weeks |
| 10 | [Parallel and external-memory algorithms](10_parallel_and_external_memory_algorithms.ipynb) | Work and span, Amdahl and Gustafson, parallel scan, parallel sorting, external merge sort, cache blocking, MapReduce and ring all-reduce. | 3 h |

```
 dsa/ (core module)   +   14_Mathematics/discrete_math/
            |
 01 amortized + randomized
            |
 02 NP-completeness ---> 03 approximation + FPT
            |
 04 flows + matching ---> 05 linear + integer programming
            |
 06 streaming + sketches     07 geometry + FFT     08 advanced data structures
            |                       |                        |
            +-----------------------+------------------------+
                                    |
                     09 coding interview workbook
                                    |
                     10 parallel + external memory
```

Notebooks 06, 07 and 08 are independent of each other; take them in any order after 01. Notebook 09 can be started at any time if your goal is interviews. The deeper study guide, with a **complexity-class cheat sheet** and a **"which algorithm for which problem" table**, is in [`notes/advanced_algorithms.md`](notes/advanced_algorithms.md).

---

## The notebooks one by one

### 01 · Amortized and Randomized Algorithms

*Explained simply.* Some operations are usually cheap and occasionally expensive; **amortized analysis** proves that, over any long sequence, the average cost per operation stays small. No probability is involved: it is a guarantee about the worst sequence. The second half is about **randomized algorithms**, which flip coins so that no particular input can trick them. A **Las Vegas** algorithm is always right and only its running time is random; a **Monte Carlo** algorithm always finishes on time but may be wrong with a small, controllable probability. Think of a monthly bus pass: one big payment, but spread over 30 days each ride is cheap.

*Tiny example.* A binary counter going 0 → 8 flips these many bits per step: 1, 2, 1, 3, 1, 2, 1, 4. One step costs 4, but the total is 15 for 8 steps, under 2 per step. Over 1,000 increments the notebook measured 1,994 flips, below the proven bound 2n = 2,000.

*You will learn:*
- The aggregate, accounting and potential methods, on a binary counter, a stack with `multipop` and a growable array (why ×2 growth beats +k growth).
- Union-find with union by rank and path compression, and the inverse Ackermann function α(n).
- Las Vegas vs Monte Carlo, expected vs worst-case time, and amplification by repetition.
- Randomized quicksort (about 1.39 n log₂ n expected comparisons) and quickselect (O(n) expected).
- Universal hashing, skip lists and treaps from scratch; Miller–Rabin primality; Karger's min-cut.
- How randomness powers AI: SGD, random restarts and randomized SVD.

*Key takeaway:* "fast on average over a sequence" (amortized) and "fast in expectation over coin flips" (randomized) are different promises; know which one you are making.

### 02 · NP-Completeness and Reductions

*Explained simply.* Some puzzles are quick to **check** but seem very slow to **solve**. **NP** is the class of yes/no problems whose "yes" answers come with a short proof (a **certificate**) that can be checked in polynomial time. **NP-complete** problems are the hardest problems in NP, and they are all linked by **reductions** (translations from one problem to another): a fast algorithm for one would give a fast algorithm for all. Nobody knows such an algorithm, and nobody has proved it impossible; that is the open **P vs NP** question. Think of a Sudoku: checking a filled grid takes a minute, filling a blank one can take an evening.

*Tiny example.* Can some of 3, 34, 4, 12, 5, 2 add up to exactly 9? Checking the answer "4 + 5" takes one addition. Finding it blindly means trying up to 2⁶ = 64 subsets; with 60 numbers it would be 2⁶⁰ ≈ 1.2 × 10¹⁸.

*You will learn:*
- Decision vs optimisation problems, and the classes P, NP, co-NP, NP-hard and NP-complete.
- Certificate checkers (verifiers) for SAT, Hamiltonian cycle and subset sum.
- Brute-force SAT and the DPLL algorithm; the random 3-SAT phase transition near clause/variable ratio 4.26.
- Reductions as tested code: 3-SAT → Independent Set → Vertex Cover → Clique.
- The Cook–Levin theorem and a catalogue of NP-complete problems next to look-alikes that are in P.
- Why the knapsack DP is pseudo-polynomial, and why core AI problems (Bayesian-network inference, optimal decision trees, best feature subsets) are NP-hard.

*Key takeaway:* proving a problem NP-hard is not giving up; it tells you which coping strategy to choose.

### 03 · Approximation and Parameterized Algorithms

*Explained simply.* When the perfect answer would take forever, an **approximation algorithm** runs fast and comes with a proof such as "never more than twice the best". The trick is to compare the answer with a number the optimum can never beat (a **lower bound on OPT**), so you can prove closeness without knowing the optimum. **Parameterized (FPT) algorithms** take a different route: the problem is hard in general, but exponential only in one small number k, so it is exact and fast when k is small. Think of packing a car boot: big suitcases first gets close to the best arrangement without trying them all.

*Tiny example.* A museum has corridors A–B, B–C and C–D; a guard in a room watches every corridor touching it. The best plan is 2 guards (B and C). The rule "take any unwatched corridor and guard both ends" may pick A–B, then C–D: 4 guards, exactly 2 × the best, and never worse than that.

*You will learn:*
- The approximation ratio and the "lower-bound OPT" proof technique.
- Vertex cover (2-approximation via a maximal matching) and greedy set cover (H(n) ≈ ln n).
- Metric TSP: double tree (2), Christofides (1.5) and 2-opt, compared with exact Held–Karp.
- The knapsack FPTAS (value scaling) and k-center farthest-first (2), linked to k-means++.
- FPT vertex cover in O(2ᵏ·n), kernelization, and why general TSP cannot be approximated at all unless P = NP.
- Submodular maximisation: the greedy (1 − 1/e) ≈ 63 % guarantee, used to choose diverse documents for RAG.

*Key takeaway:* a proven ratio turns "a heuristic that seems fine" into an engineering guarantee.

### 04 · Network Flows and Matching

*Explained simply.* A **flow network** is a graph whose edges have capacities, like water pipes from a reservoir (the source) to a city (the sink). **Maximum flow** asks how much can get through per second; the answer equals the capacity of the narrowest set of pipes you would need to cut to separate source from sink, the **minimum cut**. The same machinery solves **matching** (pair students with projects, taxis with passengers) and **assignment** (pair them at minimum total cost). Unlike the problems in 02 and 03, these have fast **exact** algorithms. Think of rush-hour traffic across a river: the bridges are the bottleneck.

*Tiny example.* Two routes from S to T: S → A → T with capacities 3 and 2, and S → B → T with 4 and 5. Max flow = 2 + 4 = **6**. Cutting A → T (2) and S → B (4) also totals **6**: max flow equals min cut.

*You will learn:*
- Residual graphs and augmenting paths; Ford–Fulkerson and Edmonds–Karp (O(VE²)) from scratch.
- The max-flow min-cut theorem, and how to read the cut off the final residual graph.
- Bipartite matching via flow, Hopcroft–Karp (O(E√V)) and Hall's theorem.
- The Hungarian algorithm for assignment (O(n³)) vs `scipy.optimize.linear_sum_assignment`; min-cost flow.
- Image segmentation as a min cut, object tracking as per-frame assignment, ticket routing with skills and capacities.
- Where it hides in AI: DETR's matching loss, multi-object tracking, optimal transport.

*Key takeaway:* before calling a scheduling or pairing problem "hard", check whether it is a flow or matching problem in disguise.

### 05 · Linear and Integer Programming

*Explained simply.* A **linear program (LP)** finds the best plan under limits: you choose numbers (the **decision variables**), you want to maximise or minimise a linear **objective**, and every limit is a linear **constraint**. The feasible plans form a many-sided shape (a **polytope**), and an optimum always sits at one of its corners, which the **simplex method** walks between. An **integer program (ILP/MILP)** adds "these must be whole numbers or yes/no", which makes it NP-hard, so solvers use **branch-and-bound**: split on a fractional variable and skip any branch whose LP bound cannot beat the best answer found so far. Think of a café deciding how many sandwiches and salads to make with limited bread and lettuce.

*Tiny example.* Desks earn $300 and chairs $500. Machine A allows at most 4 desks, machine B at most 6 chairs (12 h, 2 h each), and machine C has 18 h (3 h per desk, 2 h per chair). Best plan: 2 desks and 6 chairs, profit **$3,600**. One more hour on machine B would add $150 (its **shadow price**); one more hour on machine A adds nothing, because A is not a bottleneck.

*You will learn:*
- Modelling word problems (production, diet, transport) as LPs, and the vertex geometry.
- A two-phase tableau simplex with Bland's rule, cycling, and the Klee–Minty worst case (2ⁿ − 1 pivots).
- LP duality, weak and strong duality, and shadow prices.
- Why rounding fails, branch-and-bound from scratch, `scipy.optimize.milp`, and strong vs weak formulations.
- Modelling tricks (big-M, indicators, absolute values, min-max), sensitivity analysis and infeasibility diagnosis (IIS).
- AI uses: L1 regression and the L1-SVM as LPs, GPU job scheduling, ad-budget allocation.

*Key takeaway:* formulate first, solve second; the dual tells you what each limit is worth.

### 06 · Streaming and Sketching Algorithms

*Explained simply.* When data arrives faster than you can store it (clicks, searches, API calls to a model), a **streaming algorithm** looks at each item once and keeps only a small summary, a **sketch**. From the sketch it answers questions like "how many different users?" or "which items are most frequent?" with a small, known error: at most ε, with probability at least 1 − δ. Good sketches are **mergeable**, so each server can summarise its own data and a coordinator combines them. Think of a bouncer who remembers the busiest regulars without writing down every face.

*Tiny example.* Keep one random song from a playlist of unknown length: keep song 1, switch to song 2 with chance 1/2, to song 3 with chance 1/3, and so on. After 4 songs, song 1 survives with probability 1 × ½ × ⅔ × ¾ = **¼**, the same as every other song. That is reservoir sampling.

*You will learn:*
- The streaming model and $(\varepsilon, \delta)$ guarantees; reservoir sampling (and a weighted version).
- Heavy hitters with Misra–Gries and Space-Saving; the Count-Min sketch and its width/depth trade-off.
- HyperLogLog: about 3 KB of registers, standard error 1.04/√m (about 1.6 % with 4,096 registers).
- MinHash + LSH banding for near-duplicate detection, and the S-curve.
- Quantile sketches for p95/p99 latency, and sliding-window counting with DGIM.
- Industry cases: deduplicating a fine-tuning corpus; daily and weekly unique users with HyperLogLog.

*Key takeaway:* trade a tiny, bounded error for orders of magnitude less memory, and never average p99s or add daily unique counts; merge the sketches instead.

### 07 · Computational Geometry and the FFT

*Explained simply.* **Computational geometry** answers questions about points, lines and shapes: is this point inside the field, do these roads cross, what is the smallest fence around these trees? Almost all of it rests on one test, the **orientation** (cross-product) sign: is point c to the left or right of the line from a to b? The second half is the **fast Fourier transform (FFT)**, which multiplies two long polynomials (or convolves a signal with a filter) in O(n log n) instead of O(n²). Think of a music app's equaliser bars: that is an FFT showing which pitches are in the sound.

*Tiny example.* Is (2, 3) left or right of the road from (0, 0) to (4, 0)? Compute (4 − 0)(3 − 0) − (0 − 0)(2 − 0) = **12 > 0**, so left. For (2, −1) you get −4: right. One multiply-and-subtract.

*You will learn:*
- Orientation, segment intersection, and why floating point can flip the answer (wrong in 18 % of a near-degenerate test set).
- Convex hull by Graham scan and Andrew's monotone chain in O(n log n), and the Ω(n log n) lower bound.
- Sweep lines: meeting rooms and a simplified Bentley–Ottmann segment-intersection sweep.
- Point-in-polygon (ray casting), polygon area (shoelace), Voronoi diagrams and Delaunay triangulations.
- A recursive Cooley–Tukey FFT, polynomial and big-integer multiplication, the convolution theorem and zero-padding.
- AI links: CNN layers, FFT long convolutions (S4, Hyena) and spectrograms for speech models.

*Key takeaway:* geometry is the orientation sign done exactly; the FFT turns convolution into pointwise multiplication.

### 08 · Advanced Data Structures

*Explained simply.* A **data structure** is an arrangement of data that makes certain questions fast. This notebook collects specialised arrangements for specialised questions: which meetings clash with this one (interval tree), where does this phrase occur in a huge text (suffix array), which shop is nearest (KD-tree), what did this document look like ten edits ago (persistent structure), and how do databases absorb millions of writes per second (LSM tree). Think of a supermarket that groups products by aisle: a little organising up front saves a lot of searching later.

*Tiny example.* The sorted suffixes of "banana" are a, ana, anana, banana, na, nana, so the **suffix array** is [5, 3, 1, 0, 4, 2]. Neighbouring suffixes share prefixes of length 0, 1, 3, 0, 0, 2 (the **LCP array**). Distinct substrings = 21 − (1 + 3 + 2) = **15**, where 21 = 6·7/2 is the number of all substrings.

*You will learn:*
- Range queries: the sparse table (O(1) minimum on static data) and sqrt decomposition (O(√n) queries, O(1) updates).
- Suffix arrays by prefix doubling and the LCP array by Kasai's O(n) algorithm: substring search, longest repeat, distinct substrings.
- Interval trees for overlap queries; KD-trees with pruning and the curse of dimensionality.
- Red-black trees through 2-3-4 trees, with a left-leaning red-black (LLRB) insert and height ≤ 2 log₂(n + 1).
- Persistent structures by path copying; an LSM tree in miniature (memtable, SSTables, Bloom filters, compaction).
- Gap buffers and ropes for text editors.

*Key takeaway:* pick the structure from the question you must answer most often, and measure, because constant factors still matter.

### 09 · Coding Interview Workbook

*Explained simply.* Interview puzzles are mostly variations of about **15 patterns**, the way most recipes are variations of a few cooking methods. This workbook gives a calm **7-step method** (clarify, examples, brute force, optimise, code, test, analyse) and 45 solved problems, each with a hidden hint, a reference solution, fixed tests and **random tests against a brute-force oracle**. Testing your fast answer against a slow but obviously correct one on hundreds of random inputs is the single most useful habit here. Think of two people searching a sorted bookshelf from both ends and walking towards each other: that is the two-pointer pattern.

*Tiny example.* Toy prices over 6 days: 7, 1, 5, 3, 6, 4. Best single buy-then-sell? Walk once, remembering the cheapest price so far (7, then 1) and the best profit so far; on day 5 the profit is 6 − 1 = **5**. One pass instead of checking all 15 pairs.

*You will learn:*
- The 7-step method, shown end to end on two problems.
- A pattern map from the wording of a question to the technique (two pointers, sliding window, prefix sums, hashing, monotonic stack, binary search on the answer, heaps, intervals, BFS/DFS, topological sort, union-find, DP, backtracking, tries, bits).
- A timing harness that checks a complexity claim from the slope of a log-log plot.
- Python idioms and traps: `collections`, `heapq`, `bisect`, `functools.cache`, recursion limit, aliasing, mutable defaults.
- ML coding questions from scratch: k-means++, ROC AUC, IoU and NMS, temperature/top-k/top-p sampling, a BPE tokenizer, an LRU embedding cache.
- A 4-week practice plan and a self-assessment table.

*Key takeaway:* the brute force is never wasted; it becomes your test oracle.

### 10 · Parallel and External-Memory Algorithms

*Explained simply.* Modern hardware has many workers (CPU cores, thousands of GPU cores, many machines), and the data is often larger than memory. A parallel algorithm is measured by its **work** (total operations) and its **span** (the longest chain of steps that must happen in order); no number of workers can beat the span. **Amdahl's law** says the part that cannot be split limits the speed-up. For data bigger than RAM, the **external-memory model** counts block transfers between disk and memory, because a disk read costs thousands of times more than a memory read. Think of sorting a huge pile of exam papers on a small desk: sort a desk-sized stack at a time, then merge the sorted piles.

*Tiny example.* Adding 8 numbers one at a time takes 7 steps. With 4 helpers: 4 pairs at once (8 → 4), then 2 pairs (4 → 2), then 1 pair (2 → 1). Still **7 additions** of work, but only **3 steps** of span, because log₂ 8 = 3.

*You will learn:*
- The work-span (DAG) and PRAM models, the work and span laws, and Brent's theorem.
- Amdahl's and Gustafson's laws, first in a clean simulation, then measured on real processes.
- Parallel reduction and prefix sum (Hillis–Steele and Blelloch scans), stream compaction, and the associative scan behind Mamba.
- Parallel merge sort and sample sort, real overheads (process start-up, pickling), static vs dynamic scheduling.
- External merge sort with every block I/O counted, and cache-aware blocked matrix multiplication.
- MapReduce (word count, matrix multiply, join) and ring all-reduce, as used by multi-GPU training.

*Key takeaway:* find the serial fraction and the data movement first; they decide the speed-up, not the number of cores.

---

## How this connects to the rest of the repo and to real AI systems

- **Foundations.** Big-O, hashing, graphs, greedy and DP from [`../dsa/`](../dsa/); proofs, recurrences, graph theory and computability from [`../../14_Mathematics/discrete_math/`](../../14_Mathematics/discrete_math/).
- **Search and constraint solving.** NP-hardness explains why classical AI uses heuristics, local search and CSP solvers: [`../classical_ai/04_local_search_and_optimization.ipynb`](../classical_ai/04_local_search_and_optimization.ipynb), [`../classical_ai/06_constraint_satisfaction.ipynb`](../classical_ai/06_constraint_satisfaction.ipynb), and planning and route scheduling in [`../classical_ai/11_industry_route_planning_and_scheduling.ipynb`](../classical_ai/11_industry_route_planning_and_scheduling.ipynb).
- **Optimisation for ML.** LP duality is a special case of the Lagrangian duality in [`../../14_Mathematics/12_convex_optimization_and_duality.ipynb`](../../14_Mathematics/12_convex_optimization_and_duality.ipynb) and [`../../14_Mathematics/06_optimization.ipynb`](../../14_Mathematics/06_optimization.ipynb); the L1-SVM sits next to the [SVM notebook](../../03_Machine_Learning/01_supervised/05_svm.ipynb).
- **Randomness in learning.** SGD and random restarts ([`../../05_Deep_Learning/02_optimizers.ipynb`](../../05_Deep_Learning/02_optimizers.ipynb)), k-means++ ([clustering](../../03_Machine_Learning/02_unsupervised/01_clustering.ipynb)) and randomized SVD.
- **Vision.** The Hungarian matching loss in DETR and per-frame tracking: [`../../06_Computer_Vision/03_object_detection.ipynb`](../../06_Computer_Vision/03_object_detection.ipynb).
- **LLM data and retrieval.** MinHash-LSH and suffix arrays deduplicate training corpora; submodular greedy picks diverse RAG context; KD-trees vs approximate indexes: [`../../08_LLM/02_rag/01_rag_fundamentals.ipynb`](../../08_LLM/02_rag/01_rag_fundamentals.ipynb), [`../../22_ML_System_Design/05_vector_databases.ipynb`](../../22_ML_System_Design/05_vector_databases.ipynb).
- **Production monitoring and feature pipelines.** HyperLogLog, Count-Min and quantile sketches in [`../../15_MLOps/06_monitoring/01_monitoring.ipynb`](../../15_MLOps/06_monitoring/01_monitoring.ipynb) and [`../../15_MLOps/12_feature_stores.ipynb`](../../15_MLOps/12_feature_stores.ipynb); LSM trees under feature stores and logs.
- **Audio and sequence models.** Spectrograms in [`../../07_NLP/08_speech_and_audio.ipynb`](../../07_NLP/08_speech_and_audio.ipynb); convolution in [`../../05_Deep_Learning/03_cnn.ipynb`](../../05_Deep_Learning/03_cnn.ipynb).
- **Distributed training.** Amdahl's law, scans, tiling (the idea behind FlashAttention) and ring all-reduce in [`../../05_Deep_Learning/11_distributed_training.ipynb`](../../05_Deep_Learning/11_distributed_training.ipynb); the tools (threads, processes, the GIL) in [`../../23_Software_Engineering/05_concurrency_and_async.ipynb`](../../23_Software_Engineering/05_concurrency_and_async.ipynb).
- **Testing.** The random-oracle testing in notebook 09 generalises to property-based testing in [`../../23_Software_Engineering/03_testing_ai_code.ipynb`](../../23_Software_Engineering/03_testing_ai_code.ipynb).

---

## Common beginner mistakes

- **Reducing in the wrong direction.** To show X is NP-hard you reduce a *known* NP-hard problem **to** X, not X to it. Reducing X to SAT only shows X is no harder than SAT.
- **Reading "NP" as "not polynomial".** NP means "nondeterministic polynomial time": yes-answers are checkable in polynomial time. Every problem in P is also in NP.
- **Calling the O(nW) knapsack DP polynomial.** W is a number written in about log₂ W bits, so O(nW) is exponential in the input size. It is pseudo-polynomial.
- **Treating "NP-hard" as "unsolvable in practice".** SAT and MILP solvers routinely solve industrial instances with millions of variables; NP-hardness is a statement about the worst case as n grows.
- **Rounding an LP solution and calling it the integer optimum.** The rounded point can be infeasible or far from optimal; use branch-and-bound or a MILP solver, and keep big-M constants as small as possible.
- **Confusing amortized with average-case.** Amortized cost is a guarantee over every sequence of operations, with no probability. Expected (randomized) cost is an average over the algorithm's coin flips.
- **Adding or averaging sketch outputs.** Weekly unique users is not the sum of daily HyperLogLog estimates (the same user is counted many times), and the p99 of a week is not the average of daily p99s. Merge the sketches, then query. In notebook 06, adding seven daily counts gave 130,126 "weekly users" against a true 55,622.
- **Expecting p cores to give p× speed-up.** The serial fraction, process start-up, data copying (pickling) and memory bandwidth all cut into it; measure with Amdahl's law in mind.

---

## Exam / interview quick-revision

1. **Q:** Amortized cost of `append` on an array that doubles when full? **A:** O(1); total copying over n appends is below 2n.
2. **Q:** Cost of m union-find operations with union by rank and path compression? **A:** O(m α(n)), and α(n) ≤ 4 for any practical n.
3. **Q:** Las Vegas vs Monte Carlo? **A:** Las Vegas is always correct with a random running time (randomized quicksort); Monte Carlo has a bounded time and a small error probability (Miller–Rabin, error ≤ 4⁻ᵏ after k rounds).
4. **Q:** How do you prove a new problem X is NP-complete? **A:** Show X ∈ NP (a polynomial verifier), then reduce a known NP-complete problem to X in polynomial time.
5. **Q:** Name a problem in P that looks like an NP-complete one. **A:** 2-SAT vs 3-SAT; Euler circuit vs Hamiltonian cycle; min cut vs max cut; shortest vs longest simple path.
6. **Q:** Approximation ratio of the matching-based vertex cover? **A:** 2, and it is tight (n disjoint edges).
7. **Q:** Best ratio for greedy set cover? **A:** H(n) ≈ ln n, and no polynomial algorithm does much better unless P = NP.
8. **Q:** Why can general TSP not be approximated within any constant? **A:** A ρ-approximation would decide Hamiltonian cycle (give missing edges a huge weight), so P = NP.
9. **Q:** Max-flow min-cut theorem? **A:** The value of a maximum s–t flow equals the capacity of a minimum s–t cut; the vertices reachable from s in the final residual graph form that cut.
10. **Q:** Running time of Edmonds–Karp, Hopcroft–Karp and the Hungarian algorithm? **A:** O(VE²), O(E√V), O(n³).
11. **Q:** Is linear programming in P? Is the simplex method polynomial? **A:** LP is in P (ellipsoid, interior-point methods); simplex is exponential in the worst case (Klee–Minty) but fast in practice.
12. **Q:** What is a shadow price? **A:** The optimal dual variable of a constraint: how much the optimum improves per extra unit of that resource (within the sensitivity range).
13. **Q:** Count-Min sketch dimensions for error εN with probability 1 − δ? **A:** Width ⌈e/ε⌉, depth ⌈ln(1/δ)⌉; it never underestimates.
14. **Q:** HyperLogLog standard error with m registers? **A:** About 1.04/√m, about 1.6 % for m = 4,096.
15. **Q:** Amdahl's law, and the speed-up limit with 5 % serial work? **A:** S(p) = 1 / (s + (1 − s)/p); the limit is 1/s = 20×, and 8 cores give about 5.9×.

---

## Further reading

**Classic textbooks**
- Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms* (CLRS), 4th edition, MIT Press, 2022: amortized analysis, disjoint sets, flows and matchings, linear programming, NP-completeness, approximation, FFT and parallel algorithms. Computational geometry is in the 3rd edition, ch. 33.
- Kleinberg and Tardos, *Algorithm Design*, Pearson, 2005: the clearest treatment of network flow modelling, reductions and approximation.
- Motwani and Raghavan, *Randomized Algorithms*, Cambridge, 1995; Mitzenmacher and Upfal, *Probability and Computing*, 2nd edition, 2017.
- Williamson and Shmoys, *The Design of Approximation Algorithms*, Cambridge, 2011 (free PDF at [designofapproxalgs.com](https://www.designofapproxalgs.com/)); Vazirani, *Approximation Algorithms*, Springer, 2001.
- Garey and Johnson, *Computers and Intractability*, 1979; Sipser, *Introduction to the Theory of Computation*, 3rd edition, ch. 7.
- Bertsimas and Tsitsiklis, *Introduction to Linear Optimization*, 1997; Wolsey, *Integer Programming*, 2nd edition, 2020.
- de Berg, Cheong, van Kreveld and Overmars, *Computational Geometry: Algorithms and Applications*, 3rd edition, 2008.
- Cormode and Yi, *Small Summaries for Big Data*, Cambridge, 2020; Leskovec, Rajaraman and Ullman, *Mining of Massive Datasets* (free at [mmds.org](http://www.mmds.org/)).

**Free resources**
- [MIT OCW 6.046J Design and Analysis of Algorithms](https://ocw.mit.edu/courses/6-046j-design-and-analysis-of-algorithms-spring-2015/) (lectures, notes and problem sets).
- [Tim Roughgarden's Stanford lecture notes](https://theory.stanford.edu/~tim/) on flows, matchings, LP and approximation.
- [Scott Aaronson's P vs NP survey](https://www.scottaaronson.com/papers/pnp.pdf).
- [cp-algorithms](https://cp-algorithms.com/): rigorous write-ups of flows, FFT, geometry, suffix arrays and more.
- [Tech Interview Handbook](https://www.techinterviewhandbook.org/) for interview study plans.
- [SciPy `linprog`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.linprog.html) and [`milp`](https://docs.scipy.org/doc/scipy/reference/generated/scipy.optimize.milp.html) documentation, and the [HiGHS solver](https://highs.dev).
