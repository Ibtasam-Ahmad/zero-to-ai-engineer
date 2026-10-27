# Data Structures & Algorithms: Study Guide

This guide is the conceptual companion to the twelve notebooks in [`00_AI_Fundamentals/dsa/`](../). It walks through every idea in the same order as the notebooks, defines each term the first time it appears, works small examples by hand, and ends with a **big-O cheat sheet** covering every structure and algorithm in the module, followed by a glossary. Read a section before or after the matching notebook; the notebooks contain the runnable code, the plots and the measurements.

The module follows the order of a typical university DSA course (the CLRS textbook) and the GeeksforGeeks DSA tutorial, so it also serves as coding-interview revision. It is an optional, university-level track: do it alongside or after [`01_Python`](../../../01_Python/). The follow-up track on advanced algorithms is in [`00_AI_Fundamentals/advanced_algorithms/`](../../advanced_algorithms/).

---

## 1. Measuring Algorithms: Complexity and Recursion

### What an algorithm is

An **algorithm** is a finite sequence of exact steps that turns an input into an output. To compare algorithms without depending on a particular computer, we use the **RAM model** (random-access machine): every simple operation (an addition, a comparison, reading one memory cell) costs one unit of time, and we count how many units an algorithm uses as a function of the **input size** $n$.

Counting by hand: summing a list of $n$ numbers does one initialisation and $n$ additions, about $n + 1$ operations. Checking every pair of $n$ items for a duplicate does $\binom{n}{2} = n(n-1)/2$ comparisons. For $n = 1000$ that is 499,500 comparisons.

### Asymptotic notation

We care about how the count **grows** for large $n$, ignoring constant factors and small terms.

| Notation | Meaning | Formal definition |
|---|---|---|
| $f(n) = O(g(n))$ | $f$ grows **at most** like $g$ (upper bound) | there exist $c > 0, n_0$ with $f(n) \le c\,g(n)$ for all $n \ge n_0$ |
| $f(n) = \Omega(g(n))$ | $f$ grows **at least** like $g$ (lower bound) | there exist $c > 0, n_0$ with $f(n) \ge c\,g(n)$ for all $n \ge n_0$ |
| $f(n) = \Theta(g(n))$ | $f$ grows **exactly** like $g$ (tight bound) | both $O(g)$ and $\Omega(g)$ |
| $f(n) = o(g(n))$ | $f$ grows **strictly slower** than $g$ | $f(n)/g(n) \to 0$ |

**Worked example.** Show $3n^2 + 5n + 2 = O(n^2)$. For $n \ge 1$, $5n \le 5n^2$ and $2 \le 2n^2$, so $3n^2 + 5n + 2 \le 10n^2$. Take $c = 10$, $n_0 = 1$. It is also $\Omega(n^2)$ (take $c = 3$), hence $\Theta(n^2)$.

In everyday speech (and interviews) "Big-O" is often used to mean the tight bound. Strictly, $O$ is only an upper bound: binary search is $O(n)$ too, just not tightly.

### Common growth rates

$$1 < \log n < \sqrt{n} < n < n \log n < n^2 < n^3 < 2^n < n!$$

At roughly $10^8$ simple operations per second, $n = 10^6$ gives: $O(n)$ about 0.01 s, $O(n \log n)$ about 0.2 s, $O(n^2)$ about 3 hours, $O(2^n)$ longer than the age of the universe. **Why it matters:** if your dataset grows tenfold, an $O(n)$ preprocessing step takes 10× longer, an $O(n^2)$ one takes 100× longer.

### Best, average, worst and amortised cost

The **worst case** is the maximum cost over all inputs of size $n$; the **best case** is the minimum; the **average case** is the expected cost under some input distribution. Insertion sort is $\Theta(n)$ on sorted input (best) but $\Theta(n^2)$ on reversed input (worst).

**Amortised analysis** averages the cost over a *sequence* of operations, with no probability involved. A Python `list` grows its storage geometrically: when full, it allocates a bigger block and copies everything. A single append can cost $O(n)$, but over $n$ appends the total copying is about $1 + 2 + 4 + \dots + n < 2n$, so each append is **$O(1)$ amortised**.

### Space complexity

**Space complexity** counts the extra memory (auxiliary space) an algorithm needs, including the recursion stack. You can often trade memory for time: storing previously computed answers (memoisation) uses more memory and saves recomputation.

### Measuring for real

Theory predicts growth; measurement confirms it. Time code with `timeit` (take the minimum of several repeats), double $n$ several times, and plot time against $n$ on log-log axes. A straight line of slope $k$ means time $\propto n^k$: slope 1 is linear, slope 2 is quadratic.

### Recursion

A function is **recursive** when it calls itself on a smaller input. It needs a **base case** (an input answered directly) and **progress** toward it. Each call gets a frame on the **call stack**, so recursion depth costs memory. Python has **no tail-call optimisation** and a default recursion limit of 1000 frames, so very deep recursion should be rewritten as a loop.

A **recursion tree** draws every call as a node. For naive Fibonacci, $F(n) = F(n-1) + F(n-2)$, the tree has about $\varphi^n$ nodes ($\varphi \approx 1.618$): computing $F(30)$ makes about 2.7 million calls. **Memoisation** (caching each result) cuts this to $n$ distinct calls, the first glimpse of dynamic programming.

### Recurrences and the Master theorem

The running time of a recursive algorithm is a **recurrence**. Merge sort: $T(n) = 2T(n/2) + \Theta(n)$. Three ways to solve recurrences:

1. **Substitution:** guess a solution and prove it by induction.
2. **Recursion tree:** add the work level by level. For merge sort each of the $\log_2 n$ levels does $\Theta(n)$ work, total $\Theta(n \log n)$.
3. **Master theorem:** for $T(n) = a\,T(n/b) + f(n)$ with $a \ge 1, b > 1$, compare $f(n)$ with $n^{\log_b a}$:

| Case | Condition | Result | Example |
|---|---|---|---|
| 1 (leaves dominate) | $f(n) = O(n^{\log_b a - \varepsilon})$ | $T(n) = \Theta(n^{\log_b a})$ | $T = 8T(n/2) + n^2 \Rightarrow \Theta(n^3)$ |
| 2 (balanced) | $f(n) = \Theta(n^{\log_b a})$ | $T(n) = \Theta(n^{\log_b a} \log n)$ | $T = 2T(n/2) + n \Rightarrow \Theta(n \log n)$ |
| 3 (root dominates) | $f(n) = \Omega(n^{\log_b a + \varepsilon})$ and regularity | $T(n) = \Theta(f(n))$ | $T = 2T(n/2) + n^2 \Rightarrow \Theta(n^2)$ |

Binary search, $T(n) = T(n/2) + 1$: $a = 1, b = 2$, $n^{\log_2 1} = 1$, case 2, so $\Theta(\log n)$.

**Why it matters:** the first speed-up in real Python is usually choosing the right container. Membership in a `list` is $O(n)$, in a `set` it is $O(1)$ average; `list.pop(0)` is $O(n)$, `deque.popleft()` is $O(1)$.

---

## 2. Arrays, Strings and Problem-Solving Patterns

### Arrays and memory

An **array** stores elements in one contiguous block of memory, so element $i$ lives at address $\text{base} + i \times \text{size}$, and access by index is $O(1)$. A **static array** has fixed size; a **dynamic array** (Python `list`) resizes geometrically. A Python list actually stores *pointers* to objects scattered in memory, while a NumPy array stores raw numbers side by side, which is why NumPy is much faster for numeric work and why tensors in PyTorch are arrays with **strides** (steps between elements along each dimension).

**2-D arrays** (matrices) are stored row-major in C and NumPy. Rotating a square matrix 90° clockwise equals transposing it and then reversing each row.

### Strings

A **string** is an array of characters. Python strings are **immutable**: `s += c` in a loop may copy the whole string each time ($O(n^2)$ total), so build strings with `"".join(parts)`. Two words are **anagrams** if their character counts match; a **palindrome** reads the same both ways.

### The six patterns

| Pattern | Idea | Turns |
|---|---|---|
| Two pointers | one pointer at each end of a sorted array (or a slow and a fast pointer) moving inward | $O(n^2)$ pair search into $O(n)$ |
| Sliding window | keep a running result for a contiguous window and update it as the window slides | recomputing every window into $O(n)$ |
| Prefix sums | $P[i] = a_0 + \dots + a_{i-1}$, so $\text{sum}(i..j) = P[j+1] - P[i]$ | each range sum into $O(1)$ |
| Kadane | best sum ending here $= \max(x, \text{best ending at previous} + x)$ | maximum subarray into $O(n)$ |
| Stock buy/sell | track the minimum price so far, or add every positive day-to-day difference | $O(n^2)$ into $O(n)$ |
| Dutch national flag | three regions (less, equal, greater) maintained by three pointers | 3-way partition in one pass, $O(1)$ space |

**Worked example (two pointers).** Sorted `[1, 3, 4, 6, 8, 11]`, target 10. Left = 1, right = 11: sum 12 > 10, move right inward. 1 + 8 = 9 < 10, move left. 3 + 8 = 11 > 10, move right. 3 + 6 = 9 < 10, move left. 4 + 6 = 10: found, after 5 steps instead of checking 15 pairs.

**Worked example (Kadane).** `[-2, 1, -3, 4, -1, 2, 1, -5, 4]`. Running best-ending-here: −2, 1, −2, 4, 3, 5, **6**, 1, 5. The answer is 6 (the subarray `[4, −1, 2, 1]`).

**Prefix sums with a hash map** count subarrays summing to $k$ even with negative numbers: for each prefix $P$, add the number of earlier prefixes equal to $P - k$. A **difference array** does the reverse job: add $v$ to a whole range $[l, r]$ in $O(1)$ by `d[l] += v; d[r+1] -= v`, then take one prefix sum at the end.

### Bit manipulation

Integers are stored in binary. `x & (x - 1)` clears the lowest set bit (so `x & (x-1) == 0` tests a power of two for $x > 0$); `x ^ x = 0` and `x ^ 0 = x`, so XOR-ing all elements of an array in which every value appears twice except one leaves the single value. A **bitmask** of $n$ bits represents a subset of $n$ items.

**Why it matters:** sliding windows are rolling features in forecasting and sliding-window attention in some LLMs; prefix sums are `np.cumsum`, used when sampling a token from cumulative probabilities; bit packing is how 4-bit and 8-bit quantisation stores model weights.

---

## 3. Searching and Sorting

### Searching

**Linear search** checks every item: $O(n)$, works on anything. **Binary search** works on sorted data: compare with the middle element and discard half, $O(\log n)$. Use a consistent convention: a half-open interval `[lo, hi)` with `while lo < hi`. **Lower bound** is the first index with value $\ge x$ (`bisect_left`); **upper bound** is the first index with value $> x$ (`bisect_right`).

Binary search generalises to any **monotone predicate**: if `ok(x)` is false up to some point and true afterwards, binary search finds the boundary. This is **binary search on the answer** (e.g. the smallest ship capacity that ships all packages in $D$ days). In a **rotated sorted array**, one half around the middle is always sorted, which tells you which half to keep.

### Elementary sorts

- **Bubble sort** swaps adjacent out-of-order pairs; with an early exit it is $\Theta(n)$ on sorted input, $\Theta(n^2)$ otherwise.
- **Selection sort** repeatedly selects the minimum of the unsorted part: always $\Theta(n^2)$ comparisons but only $O(n)$ swaps.
- **Insertion sort** slides each element left into place, like sorting a hand of cards: $\Theta(n)$ on nearly sorted data, which is why Timsort uses it on small runs.

### Divide-and-conquer sorts

**Merge sort** splits the array in half, sorts each half recursively and merges the two sorted halves in linear time: $\Theta(n \log n)$ always, stable, $\Theta(n)$ extra space.

**Quick sort** picks a **pivot**, partitions the array into "less than pivot" and "greater than pivot" (Lomuto or Hoare scheme), and recurses. Expected $\Theta(n \log n)$ with a random pivot, but $\Theta(n^2)$ if the pivot is always extreme (e.g. first element of sorted input). It sorts in place and is not stable.

**Heap sort** builds a max-heap in $O(n)$ and repeatedly swaps the maximum to the end: $\Theta(n \log n)$ always, in place, not stable.

### Non-comparison sorts

These beat $n \log n$ by exploiting the structure of keys rather than comparing them. **Counting sort** counts occurrences of each key in a range of size $k$: $\Theta(n + k)$. **Radix sort** sorts by each digit from least significant to most significant with a stable counting sort: $\Theta(d(n + b))$ for $d$ digits in base $b$. **Bucket sort** scatters uniformly distributed values into $n$ buckets and sorts each: $\Theta(n)$ expected.

### Stability, in-place, and the lower bound

A sort is **stable** if equal keys keep their input order (essential when sorting by several keys in turn, and for radix sort). It is **in place** if it uses $O(1)$ (or $O(\log n)$) extra memory.

**Why comparison sorts need $\Omega(n \log n)$:** any comparison sort can be drawn as a binary **decision tree** whose leaves are the $n!$ possible orderings. A binary tree with $n!$ leaves has height at least $\log_2(n!)$, and by Stirling's approximation $\log_2(n!) = \Theta(n \log n)$.

**Timsort** (Python's `sorted` and `list.sort`) finds already-sorted **runs** in the data, extends short runs with insertion sort, and merges runs cleverly. It is stable, $O(n)$ on presorted data and $O(n \log n)$ in the worst case. Use it by default.

### Quickselect and intervals

**Quickselect** finds the $k$-th smallest element by partitioning like quick sort but recursing into only one side: expected $O(n)$. NumPy's `argpartition` uses the same idea. **Merging intervals:** sort by start, then sweep, extending the current interval while the next one overlaps.

**Why it matters:** returning the 5 most relevant documents in RAG is a top-$k$ selection problem, and nucleus (top-p) sampling in LLMs sorts token probabilities and binary-searches the cumulative sum.

---

## 4. Hashing

### From direct addressing to hash tables

If keys were small integers, we could use them directly as array indices (**direct addressing**). Real keys (strings, IDs) come from a huge universe $U$, so a **hash function** $h: U \to \{0, \dots, m-1\}$ maps each key to one of $m$ **slots** (also called buckets). A good hash spreads keys uniformly and is fast to compute.

- **Division method:** $h(k) = k \bmod m$, with $m$ a prime not close to a power of 2.
- **Multiplication method:** $h(k) = \lfloor m \cdot \text{frac}(kA) \rfloor$ with a constant $0 < A < 1$ (Knuth suggests $A \approx 0.618$); works well with $m = 2^p$.
- **Strings:** a **polynomial hash** $h(s) = \left(\sum_i s_i \cdot p^{i}\right) \bmod M$.

Python randomises the hash of `str` and `bytes` per process (SipHash, controlled by `PYTHONHASHSEED`) to defend against **hash flooding** attacks, where an attacker sends many colliding keys. Never store `hash()` values across runs. **Hashing is not encryption:** a hash is one-way and fixed-size; encryption is reversible with a key.

### Collisions

Two keys with the same slot form a **collision**; by the pigeonhole principle collisions are unavoidable when $|U| > m$.

- **Separate chaining:** each slot holds a list of keys. With **load factor** $\alpha = n/m$, a successful search inspects about $1 + \alpha/2$ keys on average.
- **Open addressing:** all keys live in the table itself; on a collision, **probe** other slots. **Linear probing** tries $h, h+1, h+2, \dots$ and suffers **primary clustering**; **quadratic probing** tries $h + i^2$; **double hashing** uses a second hash for the step size and behaves close to ideal uniform hashing. Deletion needs **tombstones** (markers saying "something was here, keep probing"). With linear probing, an unsuccessful search costs about $\frac{1}{2}\left(1 + \frac{1}{(1-\alpha)^2}\right)$ probes, which explodes as $\alpha \to 1$.

**Rehashing:** when $\alpha$ exceeds a threshold, allocate a table about twice as big and reinsert everything. Like list growth, this keeps inserts $O(1)$ amortised.

CPython's `dict` uses open addressing with a perturbed probe sequence, keeps the table at most about 2/3 full, and stores entries in a compact array that preserves insertion order. A class with a constant `__hash__` puts every key in one probe chain and turns $O(1)$ into $O(n)$.

### Classic problems

Hashing solves many interview problems in $O(n)$: **two-sum** (store each value's index; look up `target − x`), counting frequencies, grouping anagrams by their sorted letters, longest consecutive sequence, subarray sum equals $k$, and the first unique character.

### Hashing at scale

- **Consistent hashing** places servers and keys on a ring; each key goes to the next server clockwise. Adding or removing one of $N$ servers moves only about $1/N$ of the keys (plain `hash mod N` moves almost all of them).
- **Bloom filter:** a bit array of $m$ bits and $k$ hash functions. Insert sets $k$ bits; a query answers "definitely not present" if any bit is 0, otherwise "probably present". There are **no false negatives**. The false-positive rate is about $(1 - e^{-kn/m})^k$, minimised at $k = (m/n)\ln 2$, which gives about 9.6 bits per item for a 1% false-positive rate.
- **Feature hashing** (the hashing trick) maps words or categories straight to column indices of a fixed-size vector, so a model never needs a vocabulary dictionary.
- **MinHash** estimates the **Jaccard similarity** $|A \cap B| / |A \cup B|$ of two sets: the probability that two sets have the same minimum hash value equals their Jaccard similarity. **Locality-sensitive hashing (LSH)** groups MinHash signatures into bands so that only likely-similar documents are compared, avoiding all $O(n^2)$ pairs.

**Why it matters:** caches of LLM answers, deduplication of web-scale training data, sharding across servers, and crawlers all rely on hashing.

---

## 5. Linked Lists, Stacks and Queues

### Linked lists

A **linked list** is a chain of **nodes**, each holding a value and a **pointer** (reference) to the next node. There is no random access: reaching position $i$ takes $O(i)$ steps. But inserting or deleting next to a node you already hold is $O(1)$, because only pointers change.

- **Singly linked:** each node has `next`. Push/pop at the front is $O(1)$; with a tail pointer, push at the back is $O(1)$, but pop at the back is $O(n)$ (you need the node *before* the tail).
- **Doubly linked:** each node has `prev` and `next`, so deleting a known node is $O(1)$.
- **Circular:** the last node points back to the first (used for round-robin and the **Josephus problem**).
- **Sentinel (dummy) nodes** at the ends remove special cases for empty lists.

**Worked example: insert 7 after node B in `A → B → C`.** Create node 7, set `7.next = B.next` (so 7 → C), then `B.next = 7`. The order matters: doing `B.next = 7` first would lose the pointer to C.

Classic techniques: **reverse** a list by re-pointing each `next` backward with three variables (prev, current, next); **Floyd's tortoise and hare** detects a cycle with a slow pointer (1 step) and a fast pointer (2 steps) that meet inside any cycle; the same slow/fast pair finds the **middle node**; a gap of $n$ between two pointers finds the **$n$-th node from the end**.

**Arrays vs. linked lists:** arrays win on random access and on **cache locality** (neighbouring elements sit in the same memory cache line); linked lists win when you hold node references and insert or delete often.

### LRU cache

An **LRU (least recently used) cache** of capacity $C$ evicts the item that was used longest ago. Combine a **hash map** (key → node, for $O(1)$ lookup) with a **doubly linked list** ordered by recency (move a node to the front on every access, evict from the back): every `get` and `put` is $O(1)$. Python's `OrderedDict` and `functools.lru_cache` provide the same behaviour. An **LFU (least frequently used)** cache evicts by access count, using frequency buckets.

### Stacks

A **stack** is **LIFO** (last in, first out): `push` adds to the top, `pop` removes from the top, both $O(1)$. Applications:

- **Balanced brackets:** push openers; on a closer, the top must be the matching opener.
- **Shunting-yard** (Dijkstra) converts infix `3 + 4 * 2` to postfix `3 4 2 * +`; **postfix evaluation** pushes numbers and applies operators to the top two: $4 \times 2 = 8$, $3 + 8 = 11$.
- **Undo/redo** with two stacks; the **call stack** that runs recursion.
- **Monotonic stack:** keep the stack increasing or decreasing to find each element's **next greater element** in $O(n)$ total, and the largest rectangle in a histogram.
- **Min-stack:** store the minimum so far alongside each element for $O(1)$ `get_min`.

### Queues and deques

A **queue** is **FIFO** (first in, first out): `enqueue` at the back, `dequeue` at the front. A **circular queue (ring buffer)** reuses a fixed array with indices taken modulo the capacity. A **priority queue** always removes the smallest key (implemented with a heap; see section 6). A **deque** (double-ended queue, `collections.deque`) supports $O(1)$ operations at both ends.

The **sliding-window maximum** keeps a deque of indices whose values are decreasing; each index is added and removed at most once, so the whole pass is $O(n)$. Queues also drive **BFS**, **round-robin scheduling** and stream processing. A queue can be built from **two stacks** in $O(1)$ amortised per operation: push onto the in-stack; when the out-stack is empty, pour the in-stack into it.

**Why it matters:** request queues in front of model servers, LRU caches for LLM responses and KV caches, and undo stacks in AI-assisted editors are all these structures.

---

## 6. Trees, Binary Search Trees and Heaps

### Vocabulary

A **tree** is a connected structure of $n$ nodes and $n - 1$ edges with no cycles; one node is the **root**, every other node has exactly one **parent**, and nodes without children are **leaves**. The **depth** of a node is the number of edges from the root; the **height** of the tree is the number of edges on the longest root-to-leaf path. A **binary tree** gives each node at most two children.

| Kind | Definition |
|---|---|
| Full | every node has 0 or 2 children |
| Complete | every level is full except possibly the last, which is filled from the left |
| Perfect | all internal nodes have 2 children and all leaves are at the same depth; $2^{h+1} - 1$ nodes |

A complete binary tree fits in an array without pointers: the children of index $i$ are $2i + 1$ and $2i + 2$; its parent is $\lfloor (i-1)/2 \rfloor$.

### Traversals

| Traversal | Order | Uses |
|---|---|---|
| Preorder | node, left, right | copying or serialising a tree |
| Inorder | left, node, right | sorted output of a BST |
| Postorder | left, right, node | deleting a tree, computing heights (children first) |
| Level order | level by level (BFS with a queue) | views, shortest depth |

Depth-first traversals use $O(h)$ stack space; level order uses $O(w)$ queue space, where $w$ is the maximum width. Most tree problems follow one shape: "solve the left and right subtrees, combine at the node". The **diameter** (longest path between any two nodes) is the maximum over nodes of left height + right height + 2 (edges convention); the **lowest common ancestor (LCA)** of two nodes is the deepest node that has both in its subtree.

### Binary search trees

A **binary search tree (BST)** keeps every key in the left subtree smaller than the node and every key in the right subtree larger. Search, insert and delete walk one root-to-leaf path, so they cost $O(h)$. **Deletion** has three cases: a leaf (just remove it), one child (replace the node by its child), two children (replace the key by its **inorder successor**, the smallest key in the right subtree, then delete that successor). If keys arrive in sorted order the BST degenerates into a chain with $h = n - 1$ and operations become $O(n)$.

### Balanced trees

- **AVL tree:** every node's **balance factor** (left height minus right height) is −1, 0 or 1. After an insertion, at most one **rotation** pattern (LL, RR, LR, RL) restores balance. Height is less than about $1.44 \log_2 n$.
- **Red-black tree:** nodes are coloured red or black with rules (no red node has a red child; every root-to-leaf path has the same number of black nodes) that guarantee $h \le 2 \log_2(n + 1)$, with fewer rotations than AVL. Used in C++ `std::map` and Java `TreeMap`.
- **B-tree / B+ tree:** each node holds many keys and has many children (minimum degree $t$), so the tree is wide and shallow, $O(\log_t n)$ levels. This minimises slow disk reads, which is why databases and file systems index with B+ trees.

### Heaps

A **binary heap** is a complete binary tree stored in an array with the **heap property**: every parent is $\le$ its children (min-heap) or $\ge$ (max-heap). The minimum is at index 0, so `peek` is $O(1)$. **Push** appends at the end and **sifts up** (swaps with the parent while smaller); **pop** moves the last element to the root and **sifts down**. Both are $O(\log n)$.

**Why heapify is $O(n)$.** Building a heap bottom-up sifts down every internal node. About $n/2^{h+1}$ nodes have height $h$, and sifting one of them costs $O(h)$, so the total is $\sum_h \frac{n}{2^{h+1}} \cdot h = O\!\left(n \sum_h \frac{h}{2^h}\right) = O(2n) = O(n)$.

**Worked example (top-$k$ with a min-heap).** Top 3 of `5, 1, 9, 3, 7, 8`. Fill the heap with 5, 1, 9 (top = 1). 3 > 1: replace, heap {3, 5, 9}. 7 > 3: heap {5, 7, 9}. 8 > 5: heap {7, 8, 9}. Cost $O(n \log k)$ time and $O(k)$ memory, instead of sorting everything in $O(n \log n)$.

Python's `heapq` is a min-heap on a list; for a max-heap push negated keys. A priority queue that supports changing priorities can use **lazy deletion**: push the new entry and ignore stale ones when popped.

**Why it matters:** decision trees and gradient-boosted ensembles are binary trees; top-$k$ retrieval, beam search and schedulers use heaps; databases and feature stores use B+ trees.

---

## 7. Graphs

### Vocabulary and representations

A **graph** $G = (V, E)$ has $n = |V|$ **vertices** (nodes) and $m = |E|$ **edges**. Edges can be **directed** (one-way) or **undirected**, and **weighted** (a cost per edge) or not. The **degree** of a vertex is its number of edges. A **path** is a sequence of vertices joined by edges; a **cycle** is a path returning to its start. A **DAG** is a directed acyclic graph. A graph is **bipartite** if its vertices split into two groups with every edge going between the groups.

| Representation | Space | Edge test $(u, v)$ | Iterate neighbours | Best for |
|---|---|---|---|---|
| Adjacency matrix | $\Theta(n^2)$ | $O(1)$ | $O(n)$ | dense graphs |
| Adjacency list | $\Theta(n + m)$ | $O(\deg u)$ | $O(\deg u)$ | sparse graphs (most real ones) |
| Edge list | $\Theta(m)$ | $O(m)$ | $O(m)$ | edge-centric algorithms such as Kruskal |

A social network with $10^6$ users and 200 friends each needs about 125 GB as a bit matrix but about 1.6 GB as an adjacency list.

### BFS and DFS

**Breadth-first search (BFS)** uses a queue and visits vertices in layers of increasing distance, so it finds **shortest paths in unweighted graphs**. **Depth-first search (DFS)** uses recursion or an explicit stack and goes as deep as possible before backtracking; it records discovery and finish times. Both are $O(n + m)$ with an adjacency list.

From these come: **connected components** (repeat BFS/DFS from each unvisited vertex), **cycle detection** (undirected: reaching a visited vertex that is not your parent; directed: reaching a "grey" vertex still on the DFS stack), and the **bipartite check** (2-colour with BFS; a conflict means an odd cycle).

### Topological sort

A **topological order** of a DAG lists vertices so every edge goes from earlier to later (do prerequisites first). **Kahn's algorithm** repeatedly removes a vertex of in-degree 0; if some vertices are never removed, there is a cycle. The DFS method lists vertices in decreasing finish time. Both are $O(n + m)$.

### Shortest paths

- **Dijkstra's algorithm** (1959) grows a set of finalised vertices, always taking the unfinalised vertex with the smallest tentative distance from a min-heap and **relaxing** its edges ($d[v] = \min(d[v], d[u] + w(u,v))$). It requires **non-negative weights**: with a negative edge, a vertex might be finalised before a cheaper path through the negative edge is found. $O((n + m) \log n)$ with a binary heap.
- **Bellman-Ford** relaxes every edge $n - 1$ times: $O(nm)$. It handles negative weights, and a further improvement on an $n$-th round reveals a **negative cycle**.
- **Floyd-Warshall** computes all-pairs shortest paths with the DP $d_{ij} = \min(d_{ij}, d_{ik} + d_{kj})$ over intermediate vertices $k$: $O(n^3)$ time, $O(n^2)$ space.
- **0-1 BFS** handles weights 0 and 1 with a deque (push 0-edges to the front, 1-edges to the back): $O(n + m)$.

**Worked example.** Edges Home–Park 1, Park–Shop 2, Home–Shop 4. Dijkstra from Home: finalise Home (0); tentative Park 1, Shop 4. Finalise Park (1); relax Park–Shop: $1 + 2 = 3 < 4$, so Shop becomes 3. Finalise Shop (3).

### Minimum spanning trees and Union-Find

A **minimum spanning tree (MST)** connects all vertices of a weighted undirected graph with $n - 1$ edges of minimum total weight. Both classic algorithms rely on the **cut property**: the lightest edge crossing any cut belongs to some MST.

- **Kruskal:** sort edges by weight and add each edge unless it would create a cycle. Cycle checks use **Union-Find** (disjoint-set union, DSU): `find` returns a set's representative, `union` merges two sets. With **path compression** and **union by rank** each operation costs $O(\alpha(n))$ amortised, where $\alpha$ is the inverse Ackermann function ($\le 4$ for any practical $n$). Total $O(m \log m)$.
- **Prim:** grow one tree from a start vertex, always adding the cheapest edge leaving it, using a heap: $O(m \log n)$.

### Strongly connected components, bridges, grids

A **strongly connected component (SCC)** of a directed graph is a maximal set of vertices that can all reach each other. **Kosaraju's** algorithm runs DFS twice (once on the reversed graph); **Tarjan's** runs one DFS with **low-link** values. Both are $O(n + m)$, and contracting SCCs leaves a DAG. A **bridge** is an edge whose removal disconnects the graph; an **articulation point** is such a vertex: single points of failure, found with the same low-link DFS. A **grid** is an implicit graph (cells are vertices, neighbouring cells are edges); "number of islands" is connected components, and "rotting oranges" is **multi-source BFS** from all rotten cells at once.

**Why it matters:** classical AI search (uniform-cost search is Dijkstra; A* adds a heuristic), vector-database indexes (HNSW is a proximity graph), knowledge graphs, graph neural networks, ML pipelines and LangGraph agent workflows (DAGs and cyclic graphs), and backpropagation (reverse topological order over the computation graph).

---

## 8. Greedy Algorithms and Divide & Conquer

### Greedy algorithms

A **greedy algorithm** makes the locally best choice at each step and never revisits it. It is optimal when the problem has the **greedy-choice property** (some optimal solution starts with the greedy choice) and **optimal substructure** (the rest is an optimal solution of the remaining subproblem). Prove correctness with an **exchange argument**: take any optimal solution, swap in the greedy choice, and show the result is no worse.

**When greedy fails:** coins {1, 3, 4} for amount 6 (greedy 4 + 1 + 1 = 3 coins; optimal 3 + 3 = 2 coins), and 0/1 knapsack (taking the best value-per-weight item first can block a better combination). A coin system where greedy is always optimal is **canonical**; by the Kozen-Zaks bound, if greedy fails at all, it fails for some amount below the sum of the two largest coins.

| Problem | Greedy rule | Time |
|---|---|---|
| Activity selection | always take the compatible activity that **finishes earliest** | $O(n \log n)$ |
| Fractional knapsack | take items by decreasing value/weight, splitting the last | $O(n \log n)$ |
| Job sequencing with deadlines | highest profit first, into the latest free slot before its deadline | $O(n \log n + n \cdot d)$ simple; near $O(n \log n)$ with DSU |
| Minimum platforms | sweep sorted arrivals and departures, track the maximum in use | $O(n \log n)$ |
| Huffman coding | repeatedly merge the two least frequent nodes (min-heap) | $O(n \log n)$ |
| Kruskal, Prim, Dijkstra | cheapest safe edge / closest vertex | see section 7 |

**Huffman worked example** (CLRS): frequencies a:5, b:9, c:12, d:13, e:16, f:45. Merge 5+9 = 14, 12+13 = 25, 14+16 = 30, 25+30 = 55, 45+55 = 100. Code lengths: f 1 bit; c, d, e 3 bits; a, b 4 bits. Cost $45 + 3(12+13+16) + 4(5+9) = 224$ bits vs. 300 for a fixed 3-bit code. The average length $L$ per symbol satisfies $H \le L < H + 1$ where $H$ is the entropy.

### Divide and conquer

**Divide and conquer (D&C)** splits a problem into independent subproblems, solves them recursively, and **combines** the answers; analyse it with the Master theorem.

| Algorithm | Recurrence | Result |
|---|---|---|
| Merge sort, counting inversions | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ |
| Maximum subarray (D&C) | $T(n) = 2T(n/2) + O(n)$ | $\Theta(n \log n)$ (Kadane is $\Theta(n)$) |
| Closest pair of points | $T(n) = 2T(n/2) + O(n)$ (after presorting) | $\Theta(n \log n)$ |
| Karatsuba multiplication | $T(n) = 3T(n/2) + O(n)$ | $\Theta(n^{\log_2 3}) \approx \Theta(n^{1.585})$ |
| Strassen matrix multiplication | $T(n) = 7T(n/2) + O(n^2)$ | $\Theta(n^{\log_2 7}) \approx \Theta(n^{2.807})$ |
| Fast exponentiation | $T(n) = T(n/2) + O(1)$ | $\Theta(\log n)$ multiplications |

**Counting inversions** (pairs $i < j$ with $a_i > a_j$) piggy-backs on merging: when an element from the right half is placed before remaining left-half elements, it forms an inversion with each of them. **Karatsuba** computes $(a \cdot 10^h + b)(c \cdot 10^h + d)$ with three products, $ac$, $bd$ and $(a+b)(c+d)$, instead of four. **Fast exponentiation:** $x^{13} = x^{8} \cdot x^{4} \cdot x^{1}$ (13 = 1101 in binary), using repeated squaring.

| | Greedy | Divide & conquer | Dynamic programming |
|---|---|---|---|
| Core move | commit to the best choice now | split into independent parts, combine | solve overlapping subproblems once, store them |
| Proof | exchange argument | induction on size | induction over the recurrence |
| Examples | Huffman, Kruskal, activity selection | merge sort, closest pair, Karatsuba | knapsack, LCS, edit distance |

**Why it matters:** greedy decoding in LLMs (take the most probable token each step) is not globally optimal, which is why beam search exists; decision trees are grown greedily; BPE tokenizers greedily merge the most frequent pair; distributed training and MapReduce follow divide/conquer/combine.

---

## 9. Dynamic Programming

### The two conditions

**Dynamic programming (DP)**, named by Richard Bellman in the 1950s ("programming" meant filling a table), applies when a problem has **optimal substructure** and **overlapping subproblems**: the same smaller problems recur, so each is solved once and stored.

- **Top-down memoisation** keeps the natural recursion and caches results (e.g. `functools.lru_cache`); watch Python's recursion limit.
- **Bottom-up tabulation** fills a table in dependency order, avoids recursion, and allows **space optimisation** (keep only the rows the next step needs).

### The recipe

1. **State:** what does `dp[i]` (or `dp[i][j]`) mean, in words?
2. **Transition:** how is a state computed from smaller states?
3. **Base case:** which states are known directly?
4. **Order:** in which order to fill the table so dependencies are ready?
5. **Answer:** which state (or combination) is the final answer?

Complexity = (number of states) × (work per state).

### Worked examples

**Climbing stairs** (1 or 2 steps at a time): $dp[i] = dp[i-1] + dp[i-2]$, $dp[0] = dp[1] = 1$. For 5 stairs: 1, 1, 2, 3, 5, **8** ways.

**Coin change, minimum coins** with coins {1, 3, 4}: $dp[a] = 1 + \min_c dp[a - c]$, $dp[0] = 0$. Table for $a = 0..6$: 0, 1, 2, 1, 1, 2, **2** (6 = 3 + 3), where greedy gave 3.

**0/1 knapsack:** $dp[i][c] = \max(dp[i-1][c],\ v_i + dp[i-1][c - w_i])$. In the one-row version, loop capacities **downward** so each item is used at most once (looping upward gives the unbounded knapsack). Time $\Theta(nW)$ is **pseudo-polynomial**: polynomial in the *value* $W$, exponential in the number of bits needed to write it.

**Edit distance (Levenshtein)** between "kitten" and "sitting": $dp[i][j]$ = minimum insertions, deletions and substitutions turning the first $i$ characters of one string into the first $j$ of the other:
$$dp[i][j] = \begin{cases} dp[i-1][j-1] & \text{if } a_i = b_j \\ 1 + \min(dp[i-1][j],\ dp[i][j-1],\ dp[i-1][j-1]) & \text{otherwise} \end{cases}$$
The answer is 3 (k→s, e→i, insert g).

**Longest common subsequence (LCS):** $dp[i][j] = dp[i-1][j-1] + 1$ on a match, else $\max(dp[i-1][j], dp[i][j-1])$. **Longest increasing subsequence (LIS):** $O(n^2)$ with $dp[i]$ = length of the LIS ending at $i$, or $O(n \log n)$ with a "tails" array and binary search.

**Interval DP** solves problems over substrings or subarrays $[i, j]$ by increasing length: **matrix-chain multiplication** ($\Theta(n^3)$) and **longest palindromic subsequence** ($\Theta(n^2)$). **Partition equal subset sum** is a boolean knapsack; **word break** asks whether a prefix of the string can be split into dictionary words.

### Bitmask DP and tree DP

**Bitmask DP** uses a subset (a bitmask) as part of the state. The **Held-Karp** algorithm for the travelling salesman problem uses $dp[S][j]$ = shortest path visiting exactly the set $S$ and ending at $j$: $\Theta(2^n n^2)$ time, far better than $n!$ but still exponential. **DP on trees** computes each node's answer from its children in post-order (e.g. maximum independent set: for each node, the best with and without it).

### DP in AI

- **Viterbi** finds the most likely sequence of hidden states in a hidden Markov model with $\delta_t(s) = \max_{s'} \delta_{t-1}(s')\, P(s \mid s')\, P(o_t \mid s)$: $O(nT^2)$ for $n$ observations and $T$ states, instead of $T^n$ sequences.
- **Word error rate (WER)** in speech recognition is edit distance over words divided by the reference length.
- **Bellman equations** in reinforcement learning, $V(s) = \max_a \left[ R(s,a) + \gamma \sum_{s'} P(s' \mid s,a)\, V(s') \right]$, are solved by value iteration, a DP.
- Also: dynamic time warping, CTC loss in speech models, CYK parsing, sequence alignment in biology.

---

## 10. Backtracking

**Backtracking** builds candidate solutions one choice at a time and abandons a partial solution as soon as it cannot be completed. The template is **choose → explore → un-choose**: modify a shared state, recurse, then restore the state exactly. It is a depth-first search of the **state-space tree** (root = empty partial solution, edges = choices, leaves = complete candidates or dead ends), and keeps memory at $O(\text{depth})$.

**Pruning** cuts off branches early: **feasibility** pruning (a constraint is already broken), **bound** pruning (the branch cannot beat the best found so far, i.e. *branch and bound*), and **symmetry/duplicate** pruning. **Ordering** helps too: the **MRV** (minimum remaining values) heuristic fills the most constrained cell first, which makes Sudoku solving fast.

| Problem | Search space | Key trick |
|---|---|---|
| Subsets | $2^n$ | each element in or out |
| Permutations | $n!$ | with duplicates: sort, skip a value whose equal previous copy is unused |
| Combinations / combination sum | $\binom{n}{k}$ / bounded | sorted candidates, `break` once the sum is too big |
| N-Queens | at most $n!$ placements | sets for used columns and both diagonals |
| Sudoku | up to $9^{\text{empty}}$ | row/column/box sets + MRV |
| Rat in a maze, word search | up to $4 \cdot 3^{L-1}$ paths per start | mark and unmark visited cells |
| Graph m-colouring | $m^n$ | check neighbours' colours |
| Hamiltonian path | $n!$ | visited set |
| Balanced parentheses | Catalan number $C_n \approx 4^n / (n^{3/2}\sqrt{\pi})$ | open count ≥ close count |
| Palindrome partitioning | $2^{n-1}$ cut patterns | DP table of palindromic substrings |

N-Queens solution counts for $n = 1..10$: 1, 0, 0, 2, 10, 4, 40, 92, 352, 724. Balanced parentheses for $n = 3$ pairs: $C_3 = 5$ strings.

**Choosing a technique:** need to **list every** solution? Backtracking (the output itself is exponential). Need only a **count** or an **optimum**, and the future depends on a small state? DP. Tiny input or a test oracle? Brute force.

**Why it matters:** constraint satisfaction solvers (backtracking + forward checking + arc consistency), SAT solvers (DPLL/CDCL), Prolog, minimax with alpha-beta pruning in game AI, branch-and-bound in integer programming, and tree-of-thoughts-style LLM reasoning that backtracks from dead ends.

---

## 11. Advanced: Tries, String Matching, Range Queries and Number Theory

### Tries

A **trie** (prefix tree) stores strings character by character along paths from the root; words sharing a prefix share a path, and a flag marks where words end. Insert, search and prefix search cost $O(L)$ for a word of length $L$, **independent of how many words are stored**. Counters on nodes give prefix counts and allow safe deletion; caching the top suggestions at each node gives ranked autocomplete. A **radix tree** (compressed trie) merges chains of single-child nodes. A **binary trie** stores integers bit by bit from the most significant bit; to maximise $x \oplus y$, walk down preferring the opposite bit at every level, $O(B)$ per query for $B$-bit numbers.

### String matching

Find a pattern of length $m$ in a text of length $n$:

- **Naive:** try every alignment, $O(nm)$ worst case.
- **Rabin-Karp:** compare a **rolling hash** of each window with the pattern's hash, updating the hash in $O(1)$ per shift; verify on a hash match to rule out **spurious hits**. $O(n + m)$ expected, $O(nm)$ worst case.
- **KMP (Knuth-Morris-Pratt):** precompute the **LPS array** (for each prefix of the pattern, the length of its longest proper prefix that is also a suffix). On a mismatch, the LPS value says how far the pattern can shift without re-reading text characters. $O(n + m)$ guaranteed. Example: pattern `ababaca` has LPS `0 0 1 2 3 0 1`.
- **Z-algorithm:** $Z[i]$ = length of the longest substring starting at $i$ that matches a prefix of the string; run it on `pattern + "$" + text`. $O(n + m)$.
- **Longest palindromic substring:** expand around each of the $2n - 1$ centres in $O(n^2)$, or **Manacher's algorithm** in $O(n)$ by reusing mirror information.

In real Python, `str.find` and `re` are fast C implementations; write your own matcher when you need streaming input, many patterns or fingerprints.

### Range queries

Answer "sum (or min, max) of $a[l..r]$" when values change.

- **Prefix sums:** $O(1)$ query but $O(n)$ per update.
- **Segment tree:** a binary tree where each node stores the aggregate of a segment; build $O(n)$, query and point update $O(\log n)$. Works for any associative operation. **Lazy propagation** postpones range updates by storing pending changes at nodes, so range updates are also $O(\log n)$.
- **Fenwick tree (binary indexed tree, BIT):** a compact array where index $i$ stores the sum of a block whose size is the lowest set bit of $i$ (`i & -i`). Prefix-sum query and point update in $O(\log n)$, less memory and simpler code than a segment tree.
- **Sparse table:** precompute minima of all ranges of length $2^k$ in $O(n \log n)$; for static data a range-minimum query is the min of two overlapping blocks, $O(1)$.

### Number theory

- **GCD by Euclid:** $\gcd(a, b) = \gcd(b, a \bmod b)$, $O(\log \min(a,b))$; $\text{lcm}(a,b) = ab / \gcd(a,b)$. Example: $\gcd(48, 18) = \gcd(18, 12) = \gcd(12, 6) = \gcd(6, 0) = 6$. **Extended Euclid** also finds $x, y$ with $ax + by = \gcd(a,b)$.
- **Sieve of Eratosthenes:** cross out multiples of each prime starting at $p^2$: all primes up to $n$ in $O(n \log \log n)$.
- **Prime factorisation** by trial division up to $\sqrt{n}$, or with a smallest-prime-factor sieve for many queries.
- **Modular arithmetic** ("clock arithmetic"): $(a + b) \bmod m$ and $(a \cdot b) \bmod m$ can be reduced at every step. **Fast modular exponentiation** computes $a^e \bmod m$ with $O(\log e)$ multiplications.
- **Modular inverse:** $a^{-1} \bmod m$ exists iff $\gcd(a, m) = 1$; find it with extended Euclid, or as $a^{p-2} \bmod p$ for a prime $p$ (**Fermat's little theorem**).
- **Euler's totient** $\varphi(n)$ counts integers in $1..n$ coprime to $n$: $\varphi(n) = n \prod_{p \mid n}(1 - 1/p)$. **Euler's theorem:** $a^{\varphi(n)} \equiv 1 \pmod n$ when $\gcd(a, n) = 1$.
- $\binom{n}{r} \bmod p$: precompute factorials and inverse factorials in $O(N)$, then each query is $O(1)$; Lucas' theorem handles huge $n$ with a small prime.
- **RSA (textbook):** $n = pq$, choose $e$ coprime to $\varphi(n) = (p-1)(q-1)$, $d = e^{-1} \bmod \varphi(n)$; encrypt $c = m^e \bmod n$, decrypt $m = c^d \bmod n$. Toy example: $p = 61, q = 53, n = 3233, e = 17, d = 2753$; $65 \mapsto 2790$. Security rests on factoring being hard for huge $n$ (2048 bits or more today).

**Why it matters:** tokenizers walk tries (WordPiece greedy longest-match); stop-sequence detection and PII redaction are string matching; prioritized experience replay in RL samples with a sum tree (a segment tree); universal hashing and MinHash work modulo a prime; TLS protects every model API call.

---

## 12. DSA Inside Real AI Systems

The industry notebook applies the module to eight production-style problems, each as scenario → naive approach → better structure → measured gain → production notes:

| Task | Better structure | Why it wins |
|---|---|---|
| Top-$k$ retrieval and shard merging | size-$k$ heap, `argpartition` | $O(n \log k)$ time, $O(k)$ memory |
| Autocomplete, longest-match tokenisation | trie with cached top-$k$ | cost depends on the prefix length, not on the log or vocabulary size |
| BPE tokenizer training | pair-count hash map + inverted index + heap | only affected words are updated per merge |
| Exact and near-duplicate removal | hash set of digests; MinHash + LSH | $O(n)$ instead of $O(n^2)$ pairs |
| "Seen this URL?" | Bloom filter | about 9.6 bits per URL at 1% false positives |
| Related items, page importance | adjacency list + BFS; sparse PageRank power iteration | $O(V + E)$ memory instead of $O(N^2)$ |
| Fuzzy matching, POS tagging | banded edit-distance DP; Viterbi | polynomial instead of exponential |
| LLM response cache | hash map + doubly linked list (LRU) + TTL | $O(1)$ per request, fewer paid API calls |
| Rate limiting, latency monitoring | deque per client, running sum, monotonic deque | $O(1)$ amortised per event |
| Threshold tuning, first bad model version | binary search on a monotone condition | $O(\log T)$ expensive evaluations |

Production lessons: **measure first** with real data sizes; **prefer the library** (heapq, NumPy, a vector database, Redis, a tokenizer library) once you understand it; **verify** every optimisation against the simple version on random inputs; and **document the error rate** of approximate structures (LSH, Bloom filters, approximate nearest neighbours).

---

## Big-O Cheat Sheet

$n$ = number of elements, $h$ = tree height, $k$ = size of an argument or output, $V = n$ vertices and $E = m$ edges for graphs. "avg" = average/expected, "amort." = amortised.

### Python built-in containers

| Operation | `list` | `dict` | `set` | `collections.deque` |
|---|---|---|---|---|
| index `x[i]` | $O(1)$ | — | — | $O(1)$ at ends, $O(n)$ middle |
| membership / key lookup | $O(n)$ | $O(1)$ avg, $O(n)$ worst | $O(1)$ avg, $O(n)$ worst | $O(n)$ |
| append / add at end | $O(1)$ amort. | $O(1)$ avg | $O(1)$ avg | $O(1)$ |
| insert / remove at front | $O(n)$ | — | — | $O(1)$ |
| pop from end | $O(1)$ | `popitem` $O(1)$ | `pop` $O(1)$ | $O(1)$ |
| insert / delete in middle | $O(n)$ | delete $O(1)$ avg | remove $O(1)$ avg | $O(n)$ |
| iterate, copy, `min`/`max` | $O(n)$ | $O(n)$ | $O(n)$ | $O(n)$ |
| sort | $O(n \log n)$ | — | — | — |
| slice `x[a:b]` | $O(k)$ | — | — | — |

### Arrays, strings and patterns

| Technique | Time | Extra space |
|---|---|---|
| Array access by index | $O(1)$ | — |
| Insert / delete in a dynamic array (middle) | $O(n)$ | — |
| String concatenation in a loop vs. `"".join` | $O(n^2)$ vs. $O(n)$ | $O(n)$ |
| Two pointers (pair sum, remove duplicates, container with most water) | $O(n)$ | $O(1)$ |
| 3-sum (sort + two pointers) | $O(n^2)$ | $O(1)$ extra |
| Sliding window (fixed or variable) | $O(n)$ | $O(1)$ or $O(\text{alphabet})$ |
| Prefix sums: build / range query | $O(n)$ / $O(1)$ | $O(n)$ |
| Subarray sum equals $k$ (prefix sums + hash map) | $O(n)$ | $O(n)$ |
| Difference array: range update / rebuild | $O(1)$ / $O(n)$ | $O(n)$ |
| Kadane's maximum subarray | $O(n)$ | $O(1)$ |
| Stock buy/sell (one or unlimited trades) | $O(n)$ | $O(1)$ |
| Dutch national flag partition | $O(n)$ | $O(1)$ |
| Matrix transpose / rotate / spiral | $O(n^2)$ for $n \times n$ | $O(1)$ in place (square) |
| Bit tricks (set/clear/test, `x & (x-1)`, XOR single number) | $O(1)$ per op, $O(n)$ over an array | $O(1)$ |

### Searching and sorting

| Algorithm | Best | Average | Worst | Extra space | Stable | In place |
|---|---|---|---|---|---|---|
| Linear search | $O(1)$ | $O(n)$ | $O(n)$ | $O(1)$ | — | — |
| Binary search / `bisect` / lower-upper bound | $O(1)$ | $O(\log n)$ | $O(\log n)$ | $O(1)$ | — | — |
| Binary search on the answer | — | $O(\log R \cdot \text{check})$ | same | $O(1)$ | — | — |
| Bubble sort (early exit) | $\Theta(n)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | $O(1)$ | yes | yes |
| Selection sort | $\Theta(n^2)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | $O(1)$ | no | yes |
| Insertion sort | $\Theta(n)$ | $\Theta(n^2)$ | $\Theta(n^2)$ | $O(1)$ | yes | yes |
| Merge sort | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $\Theta(n)$ | yes | no |
| Quick sort (random pivot) | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $\Theta(n^2)$ | $O(\log n)$ stack | no | yes |
| Heap sort | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $O(1)$ | no | yes |
| Counting sort (key range $k$) | $\Theta(n + k)$ | $\Theta(n + k)$ | $\Theta(n + k)$ | $\Theta(n + k)$ | yes | no |
| Radix sort ($d$ digits, base $b$) | $\Theta(d(n + b))$ | $\Theta(d(n + b))$ | $\Theta(d(n + b))$ | $\Theta(n + b)$ | yes | no |
| Bucket sort (uniform data) | $\Theta(n)$ | $\Theta(n)$ | $\Theta(n^2)$ | $\Theta(n)$ | yes* | no |
| Timsort (`sorted`) | $\Theta(n)$ | $\Theta(n \log n)$ | $\Theta(n \log n)$ | $O(n)$ | yes | no |
| Quickselect ($k$-th smallest) | $O(n)$ | $O(n)$ | $O(n^2)$ | $O(1)$ | — | yes |
| Merge intervals | — | $O(n \log n)$ | $O(n \log n)$ | $O(n)$ | — | — |
| Lower bound for any comparison sort | — | — | $\Omega(n \log n)$ | — | — | — |

\* if the per-bucket sort is stable.

### Hashing

| Structure / operation | Average | Worst | Space |
|---|---|---|---|
| Hash table (chaining) search / insert / delete | $O(1 + \alpha)$ | $O(n)$ | $O(n + m)$ |
| Hash table (open addressing) search / insert / delete | $O(1/(1-\alpha))$ | $O(n)$ | $O(m)$ |
| Rehash (table doubling) | $O(1)$ amort. per insert | $O(n)$ for one resize | $O(n)$ |
| Classic problems (two-sum, frequencies, anagram groups, consecutive sequence, first unique) | $O(n)$ | $O(n^2)$ with bad hashing | $O(n)$ |
| Consistent hashing lookup (sorted ring + binary search) | $O(\log N)$ servers | $O(\log N)$ | $O(N \cdot \text{replicas})$ |
| Bloom filter insert / query ($k$ hashes) | $O(k)$ | $O(k)$ | $m$ bits ($\approx 9.6$ bits/item at 1% FP) |
| Feature hashing of a document with $t$ tokens | $O(t)$ | $O(t)$ | fixed vector of size $D$ |
| MinHash signature ($p$ permutations, set size $s$) | $O(ps)$ | $O(ps)$ | $O(p)$ per set |
| LSH near-duplicate search over $n$ docs | $\approx O(n)$ + candidates | $O(n^2)$ if all collide | $O(np)$ |

### Linked lists, stacks and queues

| Structure / operation | Time | Space |
|---|---|---|
| Singly linked list: push/pop front | $O(1)$ | $O(n)$ |
| Singly linked list: push back (tail pointer) / pop back | $O(1)$ / $O(n)$ | |
| Linked list: access / search by position | $O(n)$ | |
| Doubly linked list: push/pop both ends, delete known node | $O(1)$ | $O(n)$, 2 pointers per node |
| Circular list: rotate by one | $O(1)$ | |
| Reverse, Floyd cycle detection, middle, merge two sorted, remove $n$-th from end | $O(n)$ | $O(1)$ (recursive reverse: $O(n)$ stack) |
| Josephus problem (simulation with circular list) | $O(nk)$ | $O(n)$ |
| LRU cache get / put | $O(1)$ avg | $O(C)$ |
| LFU cache get / put | $O(1)$ avg | $O(C)$ |
| Stack push / pop / peek (array) | $O(1)$ amort. | $O(n)$ |
| Stack push / pop / peek (linked) | $O(1)$ worst | $O(n)$ |
| Balanced brackets, shunting-yard, postfix evaluation | $O(n)$ | $O(n)$ |
| Monotonic stack (next greater element, histogram) | $O(n)$ | $O(n)$ |
| Min-stack `get_min` | $O(1)$ | $O(n)$ |
| Queue (linked or circular array) enqueue / dequeue | $O(1)$ | $O(n)$ / $O(\text{capacity})$ |
| Deque operations at either end | $O(1)$ | $O(n)$ |
| Sliding-window maximum (monotonic deque) | $O(n)$ | $O(k)$ |
| Queue from two stacks | $O(1)$ amort. | $O(n)$ |
| Stack from one queue (push / pop) | $O(n)$ / $O(1)$ | $O(n)$ |

### Trees and heaps

| Structure / operation | Average | Worst | Space |
|---|---|---|---|
| Traversals (pre/in/post/level order) | $O(n)$ | $O(n)$ | $O(h)$ stack or $O(w)$ queue |
| Height, diameter, LCA, path sum, symmetric, views, serialise | $O(n)$ | $O(n)$ | $O(h)$ or $O(n)$ |
| BST search / insert / delete | $O(\log n)$ | $O(n)$ (skewed) | $O(n)$ |
| BST $k$-th smallest (inorder walk) | $O(h + k)$ | $O(n)$ | $O(h)$ |
| BST validation | $O(n)$ | $O(n)$ | $O(h)$ |
| AVL search / insert / delete | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Red-black search / insert / delete | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| B-tree search (minimum degree $t$) | $O(\log_t n)$ disk reads | $O(\log_t n)$ | $O(n)$ |
| Heap peek | $O(1)$ | $O(1)$ | |
| Heap push / pop / decrease-key | $O(\log n)$ | $O(\log n)$ | $O(n)$ |
| Heapify (bottom-up) | $O(n)$ | $O(n)$ | $O(1)$ extra |
| Heap sort | $O(n \log n)$ | $O(n \log n)$ | $O(1)$ extra |
| Search an arbitrary key in a heap | $O(n)$ | $O(n)$ | |
| Top-$k$ with a size-$k$ heap | $O(n \log k)$ | $O(n \log k)$ | $O(k)$ |
| Merge $k$ sorted lists (heap) | $O(N \log k)$ | $O(N \log k)$ | $O(k)$ |
| Running median (two heaps) | $O(\log n)$ per insert | $O(\log n)$ | $O(n)$ |

### Graphs

| Algorithm | Time | Extra space | Notes |
|---|---|---|---|
| Adjacency matrix / list / edge list | — | $\Theta(n^2)$ / $\Theta(n + m)$ / $\Theta(m)$ | |
| BFS, DFS | $O(n + m)$ | $O(n)$ | BFS gives unweighted shortest paths |
| Connected components | $O(n + m)$ | $O(n)$ | |
| Cycle detection (undirected / directed) | $O(n + m)$ | $O(n)$ | parent check / grey vertices |
| Bipartite check | $O(n + m)$ | $O(n)$ | BFS 2-colouring |
| Topological sort (Kahn / DFS) | $O(n + m)$ | $O(n)$ | DAGs only |
| Dijkstra (binary heap) | $O((n + m) \log n)$ | $O(n + m)$ | non-negative weights |
| Bellman-Ford | $O(nm)$ | $O(n)$ | negative weights, detects negative cycles |
| Floyd-Warshall | $O(n^3)$ | $O(n^2)$ | all pairs |
| 0-1 BFS | $O(n + m)$ | $O(n)$ | weights 0 or 1 |
| Union-Find (rank + path compression) | $O(\alpha(n))$ amort. per op | $O(n)$ | |
| Kruskal | $O(m \log m)$ | $O(n + m)$ | sorting dominates |
| Prim (binary heap) | $O(m \log n)$ | $O(n + m)$ | |
| Kosaraju / Tarjan SCC | $O(n + m)$ | $O(n + m)$ / $O(n)$ | |
| Bridges and articulation points | $O(n + m)$ | $O(n)$ | low-link DFS |
| Grid BFS (islands, rotting oranges) | $O(R \cdot C)$ | $O(R \cdot C)$ | |
| PageRank (sparse power iteration) | $O(m)$ per iteration | $O(n + m)$ | |

### Greedy and divide & conquer

| Algorithm | Time | Space |
|---|---|---|
| Activity selection | $O(n \log n)$ | $O(n)$ |
| Fractional knapsack | $O(n \log n)$ | $O(n)$ |
| Job sequencing with deadlines (slot array / DSU) | $O(n \log n + n d)$ / $\approx O(n \log n)$ | $O(n)$ |
| Minimum platforms (sweep line) | $O(n \log n)$ | $O(n)$ |
| Huffman coding | $O(n \log n)$ | $O(n)$ |
| Greedy coin change (canonical systems) | $O(\text{number of coin types})$ with division | $O(1)$ |
| Merge sort / counting inversions | $\Theta(n \log n)$ | $\Theta(n)$ |
| Maximum subarray: brute force / D&C / Kadane | $\Theta(n^2)$ / $\Theta(n \log n)$ / $\Theta(n)$ | $O(1)$ / $O(\log n)$ / $O(1)$ |
| Closest pair of points | $\Theta(n \log n)$ | $O(n)$ |
| Karatsuba multiplication ($n$ digits) | $\Theta(n^{1.585})$ | $O(n)$ |
| Fast exponentiation | $\Theta(\log n)$ multiplications | $O(1)$ iterative |
| Strassen matrix multiplication | $\Theta(n^{2.807})$ | $O(n^2)$ |

### Dynamic programming

| Problem | Time | Space (optimised) |
|---|---|---|
| Fibonacci: naive recursion / memo / table | $\Theta(\varphi^n)$ / $\Theta(n)$ / $\Theta(n)$ | $O(n)$ / $O(n)$ / $\Theta(1)$ |
| Climbing stairs, house robber, decode ways | $\Theta(n)$ | $\Theta(1)$ |
| Coin change, min coins or number of ways (amount $A$) | $\Theta(nA)$ | $\Theta(A)$ |
| Unique grid paths, minimum path sum ($m \times n$) | $\Theta(mn)$ | $\Theta(n)$ |
| 0/1 knapsack (capacity $W$) | $\Theta(nW)$ | $\Theta(W)$ |
| LCS, edit distance | $\Theta(mn)$ | $\Theta(\min(m, n))$ |
| LIS: DP / tails + binary search | $\Theta(n^2)$ / $\Theta(n \log n)$ | $\Theta(n)$ |
| Matrix-chain multiplication | $\Theta(n^3)$ | $\Theta(n^2)$ |
| Longest palindromic subsequence | $\Theta(n^2)$ | $\Theta(n^2)$ (or $\Theta(n)$) |
| Partition equal subset sum (target $T$) | $\Theta(nT)$ | $\Theta(T)$ |
| Word break (max word length $L$) | $O(nL^2)$ | $\Theta(n)$ |
| TSP by Held-Karp bitmask DP | $\Theta(2^n n^2)$ | $\Theta(2^n n)$ |
| DP on trees | $\Theta(n)$ | $O(n)$ |
| Viterbi ($n$ steps, $T$ states) | $O(nT^2)$ | $O(nT)$ |

### Backtracking

| Problem | Time (worst case) | Space |
|---|---|---|
| All subsets | $O(n \cdot 2^n)$ | $O(n)$ + output |
| All permutations | $O(n \cdot n!)$ | $O(n)$ + output |
| Combinations $\binom{n}{k}$ | $O(k \binom{n}{k})$ | $O(k)$ + output |
| Combination sum | exponential, bounded by pruning | $O(\text{target}/\min)$ depth |
| N-Queens | $O(n!)$ | $O(n)$ |
| Sudoku | $O(9^{e})$ for $e$ empty cells | $O(e)$ |
| Rat in a maze (all paths) | $O(4^{RC})$ bound, far less with visited marks | $O(RC)$ |
| Word search (word length $L$, grid $R \times C$) | $O(RC \cdot 4 \cdot 3^{L-1})$ | $O(L)$ |
| Graph m-colouring | $O(m^n)$ | $O(n)$ |
| Hamiltonian path | $O(n!)$ | $O(n)$ |
| Balanced parentheses ($n$ pairs) | $O(n \cdot C_n) \approx O(4^n / \sqrt{n})$ | $O(n)$ |
| Palindrome partitioning | $O(n \cdot 2^n)$ | $O(n^2)$ with palindrome table |

### Tries, strings, range queries and number theory

| Structure / algorithm | Time | Space |
|---|---|---|
| Trie insert / search / prefix search / delete (word length $L$) | $O(L)$ | $O(\text{total characters})$ |
| Radix (compressed) trie | $O(L)$ | $O(\text{number of words})$ nodes |
| Binary trie, maximum XOR pair ($B$ bits) | $O(nB)$ | $O(nB)$ |
| Naive string search | $O(nm)$ | $O(1)$ |
| Rabin-Karp | $O(n + m)$ expected, $O(nm)$ worst | $O(1)$ |
| KMP (LPS array) | $O(n + m)$ | $O(m)$ |
| Z-algorithm | $O(n + m)$ | $O(n + m)$ |
| Longest palindromic substring: expand-around-centre / Manacher | $O(n^2)$ / $O(n)$ | $O(1)$ / $O(n)$ |
| Segment tree: build / query / point update | $O(n)$ / $O(\log n)$ / $O(\log n)$ | $O(n)$ |
| Segment tree with lazy propagation: range update / query | $O(\log n)$ | $O(n)$ |
| Fenwick tree: prefix query / point update / build | $O(\log n)$ / $O(\log n)$ / $O(n)$ | $O(n)$ |
| Sparse table (static RMQ): build / query | $O(n \log n)$ / $O(1)$ | $O(n \log n)$ |
| GCD / LCM / extended Euclid | $O(\log \min(a, b))$ | $O(1)$ |
| Sieve of Eratosthenes | $O(n \log \log n)$ | $O(n)$ |
| Prime factorisation by trial division | $O(\sqrt{n})$ | $O(\log n)$ |
| Fast modular exponentiation $a^e \bmod m$ | $O(\log e)$ | $O(1)$ |
| Modular inverse (extended Euclid or Fermat) | $O(\log m)$ | $O(1)$ |
| Euler's totient by factorisation | $O(\sqrt{n})$ | $O(1)$ |
| $\binom{n}{r} \bmod p$: precompute / query | $O(N)$ / $O(1)$ | $O(N)$ |
| RSA encrypt / decrypt ($k$-bit modulus) | $O(k)$ modular multiplications | $O(1)$ |
| Disjoint-set union | $O(\alpha(n))$ amort. | $O(n)$ |

### AI-system tasks (from the industry notebook)

| Task | Naive | Better | Time (better) | Memory (better) |
|---|---|---|---|---|
| Top-$k$ of $n$ scores | full sort $O(n \log n)$ | size-$k$ heap / `argpartition` | $O(n \log k)$ / $O(n)$ avg | $O(k)$ |
| Merge results from $s$ shards | concatenate + sort | heap merge of local top-$k$ | $O(sk \log k)$ | $O(sk)$ |
| Prefix autocomplete | scan log $O(NL)$ | trie with cached top-$k$ | $O(L)$ per keystroke | $O(\text{total chars})$ |
| Longest-match tokenisation | try every vocab entry | trie walk | $O(\text{match length})$ per position | $O(\text{vocab chars})$ |
| BPE training | recount all pairs per merge | hash map + inverted index + heap | $O(\text{affected words})$ per merge | $O(\text{corpus})$ |
| Exact dedup | pairwise $O(n^2)$ | hash set of digests | $O(n)$ | 16 bytes per doc |
| Near-duplicate detection | all pairs $O(n^2)$ | MinHash + LSH | $\approx O(n)$ + candidates | $O(n \cdot \text{perms})$ |
| "Seen before?" for billions of keys | hash set | Bloom filter | $O(k)$ | $\approx 9.6$ bits/item at 1% FP |
| Related items | scan all orders | adjacency list + BFS | $O(\deg)$ / $O(V + E)$ | $O(V + E)$ |
| Node importance | dense matrix $O(N^2)$ | sparse power iteration | $O(E)$ per iteration | $O(N + E)$ |
| Fuzzy string match | full DP for every name | length filter + banded DP | $O(kL)$ per pair | $O(L)$ |
| Sequence labelling (HMM) | enumerate $T^n$ sequences | Viterbi | $O(nT^2)$ | $O(nT)$ |
| Response cache | none / unbounded dict | LRU + TTL | $O(1)$ | $O(\text{capacity})$ |
| Rate limiting, moving stats | rescan history | deque, running sum, monotonic deque | $O(1)$ amort. | $O(w)$ |
| Threshold / regression search | try all $T$ options | binary search | $O(\log T)$ evaluations | $O(1)$ |

---

## Glossary

- **Algorithm** — a finite sequence of exact steps that turns an input into an output.
- **Amortised cost** — the average cost per operation over a worst-case sequence of operations.
- **Articulation point** — a vertex whose removal disconnects a graph.
- **AVL tree** — a self-balancing BST in which subtree heights differ by at most 1 at every node.
- **B-tree / B+ tree** — a wide, shallow balanced search tree designed for disks and databases.
- **Backtracking** — building candidates one choice at a time and undoing choices that lead to dead ends.
- **Balance factor** — left subtree height minus right subtree height of a node.
- **Base case** — an input a recursive function answers directly without recursing.
- **Bellman-Ford** — shortest paths with negative edge weights in $O(nm)$; detects negative cycles.
- **BFS (breadth-first search)** — graph exploration in layers using a queue.
- **Big-O / Big-Ω / Big-Θ** — upper, lower and tight asymptotic bounds on growth.
- **Binary search** — finding a value in sorted data by halving the search range each step.
- **Binary search tree (BST)** — a binary tree with smaller keys on the left and larger keys on the right.
- **Bit manipulation** — using bitwise operators (`& | ^ ~ << >>`) on the binary form of integers.
- **Bitmask** — an integer whose bits represent membership of items in a subset.
- **Bloom filter** — a bit array answering "definitely not present" or "probably present", with no false negatives.
- **Branch and bound** — backtracking that prunes branches which cannot beat the best solution found so far.
- **Bridge** — an edge whose removal disconnects a graph.
- **Call stack** — the stack of active function frames that implements function calls and recursion.
- **Catalan number** — $C_n = \frac{1}{n+1}\binom{2n}{n}$; counts balanced parenthesis strings, BST shapes and more.
- **Collision** — two different keys hashing to the same slot.
- **Consistent hashing** — mapping keys and servers onto a ring so that a server change moves only about $1/N$ of the keys.
- **Counting sort** — sorting small-integer keys by counting occurrences, $\Theta(n + k)$.
- **Cut property** — the lightest edge crossing any cut of a graph belongs to some minimum spanning tree.
- **DAG** — directed acyclic graph.
- **Depth / height** — edges from the root to a node / edges on the longest root-to-leaf path.
- **Deque** — a double-ended queue with $O(1)$ operations at both ends.
- **DFS (depth-first search)** — graph exploration that goes as deep as possible before backtracking.
- **Difference array** — an array allowing $O(1)$ range updates, recovered by one prefix sum.
- **Dijkstra's algorithm** — single-source shortest paths for non-negative weights using a priority queue.
- **Divide and conquer** — split into independent subproblems, solve recursively, combine.
- **Double hashing** — open addressing whose probe step is given by a second hash function.
- **Dutch national flag** — a one-pass, in-place partition into three groups.
- **Dynamic programming** — solving overlapping subproblems once and reusing stored answers.
- **Edit distance (Levenshtein)** — the minimum number of insertions, deletions and substitutions turning one string into another.
- **Exchange argument** — proving a greedy algorithm optimal by swapping its choice into any optimal solution.
- **Feature hashing** — mapping features directly to vector indices with a hash function.
- **Fenwick tree (BIT)** — a compact array structure for prefix sums with $O(\log n)$ updates and queries.
- **Floyd-Warshall** — all-pairs shortest paths by DP over intermediate vertices, $O(n^3)$.
- **Floyd's tortoise and hare** — cycle detection with a slow and a fast pointer.
- **Graph** — a set of vertices connected by edges.
- **Greedy algorithm** — an algorithm that commits to the locally best choice at every step.
- **Hash function** — a function mapping keys to slot indices.
- **Hash table** — an array of slots indexed by a hash function, giving $O(1)$ average operations.
- **Heap (binary)** — a complete binary tree in an array where each parent is ≤ (min-heap) or ≥ (max-heap) its children.
- **Heapify** — building a heap from an unordered array in $O(n)$.
- **Huffman coding** — an optimal prefix code built by repeatedly merging the two least frequent symbols.
- **In-place** — using only $O(1)$ (or $O(\log n)$) extra memory.
- **Inorder successor** — the next key in sorted order; the smallest key in a node's right subtree.
- **Inversion** — a pair $i < j$ with $a_i > a_j$.
- **Kadane's algorithm** — $O(n)$ maximum-sum contiguous subarray.
- **Karatsuba** — multiplication with three half-size products instead of four, $\Theta(n^{1.585})$.
- **KMP** — linear-time string matching using the LPS (failure) array.
- **Kruskal / Prim** — greedy minimum-spanning-tree algorithms (edge-sorted with Union-Find / heap-grown tree).
- **Linked list** — a chain of nodes each pointing to the next (and, if doubly linked, the previous).
- **Load factor** — $\alpha = n/m$, the number of stored keys per slot.
- **LCA (lowest common ancestor)** — the deepest node that has two given nodes as descendants.
- **LPS array** — for each pattern prefix, the length of its longest proper prefix that is also a suffix.
- **LRU / LFU cache** — a bounded cache evicting the least recently / least frequently used item.
- **LSH (locality-sensitive hashing)** — hashing that puts similar items in the same bucket with high probability.
- **Manacher's algorithm** — longest palindromic substring in $O(n)$.
- **Master theorem** — the closed-form solution of $T(n) = aT(n/b) + f(n)$.
- **Memoisation** — caching the results of function calls (top-down DP).
- **MinHash** — signatures whose agreement rate estimates Jaccard similarity.
- **Minimum spanning tree** — a set of $n - 1$ edges connecting all vertices with minimum total weight.
- **Modular inverse** — $x$ with $ax \equiv 1 \pmod m$; exists iff $\gcd(a, m) = 1$.
- **Monotonic stack / deque** — a stack or deque kept sorted so each element is pushed and popped once.
- **MRV heuristic** — choose the variable (cell) with the fewest remaining legal values first.
- **Open addressing** — collision handling by probing other slots inside the table.
- **Optimal substructure** — an optimal solution contains optimal solutions to subproblems.
- **Overlapping subproblems** — a naive recursion solves the same subproblems repeatedly.
- **PageRank** — vertex importance from a random-surfer model, computed by power iteration.
- **Prefix sum** — running total array giving any range sum by one subtraction.
- **Priority queue** — a collection that always removes the item with the smallest (or largest) key.
- **Pruning** — skipping branches of a search that cannot lead to a valid or better solution.
- **Pseudo-polynomial** — polynomial in a numeric input's value but exponential in its bit length.
- **Queue** — a first-in, first-out (FIFO) collection.
- **Quickselect** — expected $O(n)$ selection of the $k$-th smallest element.
- **Rabin-Karp** — string matching by comparing rolling hashes.
- **Radix sort** — stable digit-by-digit sorting, $\Theta(d(n + b))$.
- **RAM model** — the cost model in which every simple operation takes one time unit.
- **Recurrence** — an equation expressing a running time in terms of smaller inputs.
- **Recursion** — a function solving a problem by calling itself on smaller instances.
- **Red-black tree** — a self-balancing BST using node colours, height ≤ $2\log_2(n+1)$.
- **Rehashing** — moving all keys to a larger table when the load factor gets too high.
- **Relaxation** — updating a tentative distance if a shorter path through an edge is found.
- **RSA** — public-key cryptosystem based on modular exponentiation and the hardness of factoring.
- **Segment tree** — a tree of segment aggregates for $O(\log n)$ range queries and updates.
- **Sentinel node** — a dummy node that removes special cases at list boundaries.
- **Separate chaining** — collision handling by keeping a list of keys per slot.
- **Sieve of Eratosthenes** — finding all primes up to $n$ in $O(n \log \log n)$.
- **Sliding window** — maintaining a result over a moving contiguous range.
- **Space complexity** — the extra memory an algorithm needs as a function of input size.
- **Sparse table** — precomputed power-of-two range minima for $O(1)$ static range-minimum queries.
- **Stable sort** — a sort that keeps equal keys in their input order.
- **Stack** — a last-in, first-out (LIFO) collection.
- **State-space tree** — the tree of partial solutions explored by backtracking.
- **Strongly connected component** — a maximal set of vertices in a directed graph that all reach each other.
- **Tail recursion** — a recursive call as the very last action; Python does not optimise it.
- **Timsort** — Python's stable, adaptive merge/insertion hybrid sort.
- **Topological sort** — an ordering of a DAG's vertices with every edge pointing forward.
- **Trie** — a prefix tree storing strings character by character.
- **Two pointers** — scanning with two indices that move toward each other or at different speeds.
- **Union-Find (DSU)** — a disjoint-set structure with near-constant `find` and `union`.
- **Viterbi algorithm** — DP for the most likely hidden-state sequence in an HMM.
- **Z-algorithm** — linear-time computation of longest prefix matches at every position.
