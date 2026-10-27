# Data Structures & Algorithms

A **data structure** is a way of arranging data so the jobs you do most often are fast; an **algorithm** is a step-by-step recipe that turns an input into an answer. This 12-notebook module teaches both from zero, in the order of a typical university DSA course (CLRS-style) and the [GeeksforGeeks DSA tutorial](https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/), so it also works as revision for exams and for **coding interviews**. It is an **optional, university-level track**: the rest of the course does not depend on it, but it is strongly recommended for BS/MS AI students and anyone heading into technical interviews.

**Why an AI developer needs DSA.** A model is only one part of an AI product. Around it sits ordinary code that searches, ranks, counts, caches and filters, and that code decides whether the product answers in 50 ms or 5 s and whether it costs $100 or $10,000 a month. Two reasons stand out:

1. **Performance.** Picking the top 10 of a million retrieval scores with a heap instead of sorting, or deduplicating training data with a hash set instead of comparing all pairs, turns hours into seconds. Big-O lets you predict this *before* you run anything.
2. **The data structures inside AI systems.** Tensors are arrays, tokenizers are tries and hash maps, vector databases are graphs (HNSW), decision trees are binary trees, beam search and top-k sampling use heaps, LLM response caches are LRU caches, Viterbi and Bellman equations are dynamic programming, and agent workflows are graphs. Knowing the structure lets you read, debug and tune these systems instead of treating them as magic.

> **When to take it:** do it **alongside or after [`01_Python`](../../01_Python/)**. You need functions, loops, lists, dicts and (from notebook 05 on) classes. If you have just finished [`01_Python/01_basic.ipynb`](../../01_Python/01_basic.ipynb) you are ready for notebook 01.
>
> **What comes next:** a follow-up **advanced algorithms** track (amortised and randomised algorithms, NP-completeness, approximation, network flows, linear programming, streaming and sketching, and more) lives in [`00_AI_Fundamentals/advanced_algorithms/`](../advanced_algorithms/). Its [README](../advanced_algorithms/README.md) gives the study order and an easy explanation of each of its 10 notebooks.

---

## The whole topic explained simply

Imagine you run a library. If the books are dumped in one big pile, finding one means checking every book; if they are sorted on labelled shelves, you walk straight to the right shelf. That choice of *arrangement* is a data structure, and the walk you take to find the book is an algorithm. DSA is the study of good arrangements and good walks, and of how to **measure** them. We do not measure in seconds, because seconds depend on the computer; we measure how the number of steps **grows** when the input grows, and we write that growth with **Big-O** notation. O(n) means "double the input, double the work"; O(log n) means "double the input, add just one step"; O(n²) means "double the input, four times the work". A cloakroom ticket is hashing (ticket 37 means hook 37, no searching); a pile of plates is a stack (last in, first out); the line at a coffee shop is a queue (first in, first out). Bigger ideas reuse smaller ones: a road map is a graph, the shortest drive home is a shortest-path algorithm, and "remember answers you have already worked out" is dynamic programming.

**Tiny worked example (real numbers).** You need to find one ID among **1,000,000** sorted IDs.

| Method | How it works | Looks needed (worst case) |
|---|---|---|
| Linear search, O(n) | check IDs one by one | 1,000,000 |
| Binary search, O(log n) | open the middle, throw away the half that cannot contain it, repeat | 20 (because 2²⁰ = 1,048,576) |
| Hash table, O(1) average | compute the ID's "box number" and look only there | about 1 |

Same question, same data: the only difference is the arrangement and the walk. That is the whole subject in one table.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | Beginners who know basic Python and want to understand why some code is fast and some is slow; university students revising for a DSA or algorithms exam; anyone preparing for coding interviews or ML-engineering / system-design interviews. |
| **Prerequisites** | [Python basics](../../01_Python/01_basic.ipynb) (functions, loops, lists, dicts); classes from [Python advanced](../../01_Python/03_advanced.ipynb) from notebook 05 on; high-school algebra (powers and logarithms). The [maths notation bridge](../../14_Mathematics/00_start_here_math_notation_bridge.ipynb) helps if Σ or log look scary; [NumPy](../../02_Data_Analysis/02_numpy.ipynb) and [probability](../../14_Mathematics/03_probability.ipynb) help in notebooks 02, 04 and 12 but are not required. |
| **Time needed** | About 35 to 45 hours in total (2 to 5 hours per notebook), more if you do every practice problem. |
| **Runs on** | CPU only, no API key, no internet. Each notebook executes in about one to two minutes or less. |
| **Optional?** | Yes. University-level fundamentals track; recommended, not required. |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Complexity analysis and recursion](01_complexity_analysis_and_recursion.ipynb) | How to measure an algorithm with Big-O and how to analyse recursive code with recurrences and the Master theorem. | 2–3 h |
| 02 | [Arrays, strings and techniques](02_arrays_strings_and_techniques.ipynb) | Six patterns (two pointers, sliding window, prefix sums, Kadane, stock trading, Dutch flag) plus bit tricks that turn O(n²) array problems into O(n). | 3 h |
| 03 | [Searching and sorting](03_searching_and_sorting.ipynb) | Binary search and its variants, ten sorting algorithms built from scratch, the n log n lower bound and how Python's Timsort works. | 3 h |
| 04 | [Hashing](04_hashing.ipynb) | How `dict` and `set` achieve O(1) lookups, collision handling, and hashing at scale: consistent hashing, Bloom filters, MinHash/LSH. | 3 h |
| 05 | [Linked lists, stacks and queues](05_linked_lists_stacks_queues.ipynb) | The three "line-shaped" structures, the classic pointer problems, and an O(1) LRU cache. | 3–4 h |
| 06 | [Trees, BSTs and heaps](06_trees_bst_and_heaps.ipynb) | Traversals, binary search trees, self-balancing AVL/red-black trees, B-trees, and heaps as priority queues. | 4 h |
| 07 | [Graphs](07_graphs.ipynb) | BFS, DFS, topological sort, shortest paths, minimum spanning trees with Union-Find, and SCCs, all checked against networkx. | 4–5 h |
| 08 | [Greedy and divide & conquer](08_greedy_and_divide_and_conquer.ipynb) | When "take the best choice now" is provably optimal, when it fails, and how splitting a problem in halves gives fast algorithms. | 2–3 h |
| 09 | [Dynamic programming](09_dynamic_programming.ipynb) | A five-step recipe for "remember sub-answers" problems, applied to 16 classics from Fibonacci to edit distance and TSP. | 3–4 h |
| 10 | [Backtracking](10_backtracking.ipynb) | Choose → explore → un-choose: listing subsets, permutations, N-Queens and Sudoku solutions, with pruning measured. | 2–3 h |
| 11 | [Advanced: tries, strings and range queries](11_advanced_tries_strings_and_range_queries.ipynb) | Tries, KMP/Z/Rabin-Karp string matching, segment and Fenwick trees, and number theory up to textbook RSA. | 3–4 h |
| 12 | [🏭 Industry: DSA inside real AI systems](12_industry_dsa_in_ai_systems.ipynb) | Eight measured case studies: top-k retrieval, tokenizers, dedup, PageRank, Viterbi, LLM caching, rate limiting and binary search in ML ops. | 3 h |

```
 01 Big-O + recursion
   |
 02 arrays/strings ---> 03 search/sort ---> 04 hashing
                                              |
 05 lists/stacks/queues ---> 06 trees/heaps ---> 07 graphs
                                                   |
 08 greedy + D&C ---> 09 dynamic programming ---> 10 backtracking
                                                   |
                           11 tries/strings/range queries
                                                   |
                           12 industry: DSA in AI systems
```

The deeper conceptual study guide for the whole module, including a full **big-O cheat sheet**, is in [`notes/dsa.md`](notes/dsa.md).

---

## The notebooks one by one

### 01 · Complexity Analysis and Recursion

*Explained simply.* An algorithm is a recipe, and two recipes can give the same answer with very different amounts of work. Instead of timing with a stopwatch, we count how the number of steps grows as the input grows, and write it as Big-O. Recursion is a recipe that calls a smaller copy of itself, like Russian dolls; its cost is described by a *recurrence* such as "T(n) = 2T(n/2) + n", which the Master theorem solves. Think of shaking hands at a party: 10 people make 45 handshakes, but 100 people make 4,950, ten times more people and about a hundred times more work, which is O(n²).

*Tiny example.*

| n | log₂ n | n log₂ n | n² |
|---|---|---|---|
| 10 | 3.3 | 33 | 100 |
| 1,000 | 10 | 10,000 | 1,000,000 |
| 1,000,000 | 20 | 20,000,000 | 10¹² (hours of work) |

*You will learn:*
- The RAM model and counting operations by hand; Big-O, Big-Ω, Big-Θ with the constants c and n₀, and little-o.
- Best, average and worst case, and amortised analysis (why `list.append` is O(1) on average).
- Space complexity and the time vs. space trade-off.
- Measuring growth with `timeit` and log-log plots.
- Recursion: base case, call stack, recursion trees, Python's recursion limit (1000), memoisation.
- Solving recurrences by substitution, recursion trees and the Master theorem; the cost of every `list`/`dict`/`set`/`deque` operation.

*Key takeaway:* growth rate beats raw speed; an O(n log n) algorithm on a slow laptop eventually beats an O(n²) one on a supercomputer.

### 02 · Arrays, Strings and Problem-Solving Techniques

*Explained simply.* An array is a row of numbered boxes side by side in memory, so the computer can jump straight to box 500. A string is an array of characters. Most array puzzles can be solved by trying every possibility, but six tricks avoid repeated work, for example keeping a running total and adjusting it instead of re-adding everything. Think of a train passenger looking out of a window: as the train moves one house appears and one disappears, so there is no need to recount every house (the sliding window).

*Tiny example.* Best 3-day total of daily steps `[3, 1, 4, 1, 5, 9, 2]`:

```
3+1+4 = 8 -> 8-3+1 = 6 -> 6-1+5 = 10 -> 10-4+9 = 15 -> 15-1+2 = 16   best = 16
```

One subtraction and one addition per step instead of re-adding three numbers.

*You will learn:*
- Static vs. dynamic arrays, memory layout, Python lists vs. NumPy arrays, matrix tricks (transpose, rotate, spiral).
- Strings: immutability, building them with `"".join`, palindromes and anagrams.
- Two pointers and sliding windows (fixed and variable size).
- Prefix sums, difference arrays and "subarray sum equals k" with a hash map.
- Kadane's maximum subarray, stock buy/sell problems, the Dutch national flag partition.
- Bit manipulation: `& | ^ ~ << >>`, the XOR single-number trick, bitmasks as subsets.

*Key takeaway:* most O(n²) array problems become O(n) once you spot the right pattern.

### 03 · Searching and Sorting

*Explained simply.* Searching finds an item; sorting puts items in order; and once data is sorted, binary search finds anything by halving the search area every look. Simple sorts compare neighbours over and over and are slow; clever sorts split the list, sort the halves and merge them; special sorts do not compare at all but count. Think of the guessing game "a number from 1 to 100": guess 50, hear "higher", guess 75, and you never need more than 7 guesses.

*Tiny example.* Find 23 in `[2, 5, 8, 12, 16, 23, 38]`: middle is 12, so go right; middle of `[16, 23, 38]` is 23. Found in **2 looks** instead of 6.

*You will learn:*
- Linear and binary search, lower/upper bound, `bisect`, rotated arrays, binary search on the answer.
- Bubble, selection and insertion sort, and why insertion sort is good on nearly sorted data.
- Merge sort, quick sort (Lomuto, Hoare, random pivot), heap sort, and counting, radix and bucket sort.
- Stability and in-place sorting, with a full comparison table and a benchmark.
- Why comparison sorts need Ω(n log n) comparisons, and how Timsort exploits real-world runs.
- Quickselect (k-th smallest in expected O(n)) and merging intervals.

*Key takeaway:* use `sorted()` by default, but know why it is fast and when counting/radix sort or quickselect beats it.

### 04 · Hashing

*Explained simply.* Hashing turns any key into a number that says which box to put it in, so later you go straight to that box instead of searching. Sometimes two keys want the same box (a *collision*), and a hash table needs a rule for that: share the box, or try the next one. The same "fingerprint" idea spots duplicate documents, splits data across servers and checks "have I seen this URL before?" with tiny memory. Think of a cloakroom: ticket 37 means hook 37, so nobody searches the coats.

*Tiny example.* 10 boxes, rule "box = ID mod 10":

| ID | 1234 | 5678 | 9012 | 3334 |
|---|---|---|---|---|
| box | 4 | 8 | 2 | 4 (collision with 1234) |

To check 5678, look only in box 8.

*You will learn:*
- Direct addressing, the division and multiplication methods, polynomial string hashing.
- Python's `hash()`, randomised string hashing (`PYTHONHASHSEED`), and hashing vs. encryption.
- Separate chaining and open addressing (linear probing, quadratic probing, double hashing), with tombstones for deletion.
- Load factor α = n/m, measured probe counts vs. the textbook formulas, and rehashing.
- How CPython's `dict` and `set` really work, and how a bad `__hash__` makes O(1) become O(n).
- Consistent hashing, Bloom filters, feature hashing and MinHash/LSH for near-duplicates.

*Key takeaway:* a hash table gives O(1) average lookups as long as the hash spreads keys well and the table never gets too full.

### 05 · Linked Lists, Stacks and Queues

*Explained simply.* A linked list is a treasure hunt: each clue says where the next clue is, so inserting a clue is easy, but reaching clue 50 means following 49 clues. A stack is a pile of plates, last in first out, which is how the undo button and Python's function calls work. A queue is a line at a coffee shop, first in first out, which is how printers and requests waiting for an AI model are served. Think of the browser's back button: every page you visit goes on a stack, and "back" pops the top one.

*Tiny example.* Type `c`, `a`, `t`: the undo stack is `[c, a, t]`. Undo removes `t` (text `ca`), undo again removes `a` (text `c`). A party queue that receives songs A, B, C plays A, then B, then C.

*You will learn:*
- Singly, doubly and circular linked lists built from scratch, with sentinel nodes and the Josephus problem.
- The classic pointer problems: reverse, Floyd's cycle detection, middle node, merge two sorted lists, remove the n-th from the end.
- When to choose an array and when a linked list.
- An O(1) LRU cache from a hash map plus a doubly linked list (and what an LFU cache is).
- Stacks: balanced brackets, shunting-yard and postfix evaluation, undo/redo, monotonic stacks, min-stack.
- Queues: circular queue, priority queue preview, `collections.deque`, sliding-window maximum, BFS and round-robin scheduling.

*Key takeaway:* every structure makes one kind of job fast; pick the one whose fast job is the one you do most.

### 06 · Trees, Binary Search Trees and Heaps

*Explained simply.* A tree arranges items in levels where every item has exactly one parent, like folders on your computer. A binary search tree keeps "smaller to the left, bigger to the right", so finding a value is a guessing game of about log₂ n questions. Inserting values in sorted order can turn it into a long chain, so balanced trees (AVL, red-black) tidy themselves with rotations. Think of a hospital emergency room: a heap always keeps the most urgent patient on top, ready to be treated next.

*Tiny example.* Insert 50, 30, 70, 20, 40 into a BST:

```
        50
       /  \
     30    70
    /  \
  20    40
```

Finding 40 checks 50 → 30 → 40: three looks instead of five.

*You will learn:*
- Tree vocabulary (root, leaf, depth, height) and full, complete and perfect binary trees, plus the array representation.
- Preorder, inorder, postorder and level-order traversals, recursive and iterative.
- Classic problems: height, diameter, LCA, views, path sum, symmetric tree, serialise/deserialise.
- BST search, insert, the three delete cases, validation, and the degenerate sorted-input case (measured).
- AVL rotations (LL, RR, LR, RL), red-black trees conceptually, B-trees and B+ trees.
- Binary heaps: sift-up/down, O(n) heapify with the proof, heap sort, a priority-queue class, `heapq`.

*Key takeaway:* trees give O(log n) operations only while they stay balanced; heaps give the minimum in O(1) and updates in O(log n).

### 07 · Graphs

*Explained simply.* A graph is a set of dots (nodes) joined by lines (edges): cities and roads, people and friendships, web pages and links. Many questions are graph questions: the quickest route home, whether everyone can reach everyone, in which order to do tasks that depend on each other, the cheapest way to connect every house. BFS explores like ripples in a pond (everything 1 step away, then 2 steps); DFS explores like walking a maze, deep first, backing up at dead ends. Think of a sat-nav: it runs a shortest-path algorithm over a road graph.

*Tiny example.* Home→Shop is 4 km, Home→Park is 1 km, Park→Shop is 2 km. Dijkstra finds Home → Park → Shop = 1 + 2 = **3 km**, beating the direct 4 km road.

*You will learn:*
- Vocabulary (directed, weighted, degree, path, cycle, DAG, bipartite) and the adjacency matrix, adjacency list and edge list.
- BFS and DFS, connected components, cycle detection and the bipartite check.
- Topological sort (Kahn's algorithm and DFS).
- Shortest paths: Dijkstra (and why negative edges break it), Bellman-Ford, Floyd-Warshall, 0-1 BFS.
- Minimum spanning trees with Kruskal + Union-Find and Prim; SCCs (Kosaraju, Tarjan), bridges and articulation points.
- Grid graphs: number of islands and rotting oranges (multi-source BFS).

*Key takeaway:* model the problem as a graph and a textbook algorithm usually solves it in O(n + m) or O((n + m) log n).

### 08 · Greedy Algorithms and Divide & Conquer

*Explained simply.* A greedy algorithm always takes the choice that looks best right now and never looks back; it is fast, but only correct for problems with the right structure, which you prove with an *exchange argument*. Divide and conquer splits a problem into independent halves, solves them, and combines the answers. Think of a cashier giving change with euro coins: always handing over the largest coin that fits works for euros, but with coins {1, 3, 4} it fails for 6 (greedy gives 4 + 1 + 1, three coins; the best is 3 + 3, two coins).

*Tiny example.* Huffman coding of `a:5, b:9, c:12, d:13, e:16, f:45` (100 characters) merges the two rarest repeatedly and needs **224 bits** instead of 300 bits with a fixed 3-bit code.

*You will learn:*
- The greedy-choice property, optimal substructure and exchange-argument proofs; counterexamples where greedy fails.
- Activity selection, fractional knapsack, job sequencing, minimum platforms, Huffman coding, canonical coin systems.
- The divide-and-conquer paradigm and the Master theorem.
- Counting inversions, maximum subarray (D&C vs. Kadane), closest pair of points in O(n log n).
- Karatsuba multiplication, fast exponentiation and the idea behind Strassen's matrix multiplication.
- How to choose between greedy, divide & conquer and dynamic programming.

*Key takeaway:* try a greedy rule first and break it with a tiny counterexample; if it breaks, look at whether the subproblems overlap (DP) or are independent (D&C).

### 09 · Dynamic Programming

*Explained simply.* Dynamic programming (DP) means never solving the same subproblem twice: store each answer in a table and reuse it. It works when the best answer is built from best answers to smaller pieces (*optimal substructure*) and the same pieces come up again and again (*overlapping subproblems*). A five-step recipe (state, transition, base case, order, answer) cracks almost every DP problem. Think of a friend who has just counted "1+1+1+1+1+1+1+1 = 8": add "+1" and they say 9 instantly, because they remembered the previous answer.

*Tiny example.* Fibonacci with a table: `F = [0, 1, 1, 2, 3, 5, 8, 13]`. Each new entry is the sum of the two before it, so F(7) = 13 takes 6 additions, whereas naive recursion makes 41 calls and naive F(30) makes about 2.7 million.

*You will learn:*
- Top-down memoisation vs. bottom-up tabulation, and space optimisation.
- 1-D DP: climbing stairs, house robber, coin change (minimum coins and number of ways), decode ways.
- 2-D DP: grid paths, minimum path sum, 0/1 knapsack with reconstruction, LCS, edit distance, LIS in O(n log n).
- Interval DP (matrix-chain multiplication, longest palindromic subsequence), partition subset sum, word break.
- Bitmask DP for the travelling salesman problem (Held-Karp) and DP on trees.
- DP inside AI: Viterbi for HMMs, word error rate, Bellman equations in reinforcement learning.

*Key takeaway:* DP cost = (number of states) × (work per state); define the state in words first.

### 10 · Backtracking

*Explained simply.* Backtracking builds a solution one choice at a time and, the moment a partial solution cannot work, undoes the last choice and tries the next one. It is a depth-first walk over a tree of partial solutions (the *state-space tree*), and *pruning* skips whole branches that cannot lead anywhere. It is the natural tool when you must list *every* solution. Think of a maze: at a dead end you walk back to the last junction and try a corridor you have not tried.

*Tiny example.* Subsets of {1, 2, 3}: at each level decide "in" or "out" for one element, giving 2³ = **8** leaves: {}, {3}, {2}, {2,3}, {1}, {1,3}, {1,2}, {1,2,3}. N-Queens on an 8×8 board has **92** solutions.

*You will learn:*
- The choose → explore → un-choose template and the state-space tree.
- Pruning by feasibility, bounds and symmetry, and measuring how much it saves.
- Subsets, permutations (with and without duplicates), combinations and combination sum.
- N-Queens, Sudoku (with the MRV heuristic), rat in a maze and word search.
- Graph m-colouring, Hamiltonian paths, balanced parentheses, palindrome partitioning.
- When to use backtracking vs. DP vs. brute force, and how backtracking becomes constraint satisfaction in AI.

*Key takeaway:* backtracking is still exponential in the worst case, but pruning and good ordering make it practical.

### 11 · Advanced: Tries, String Matching, Range Queries and Number Theory

*Explained simply.* Some questions are asked over and over: "which words start with these letters?", "where does this word appear in a long text?", "what is the total between day 40 and day 90?". The trick is to organise the data once so each later question takes a few steps. A trie is like the thumb tabs of a dictionary; a range-query tree is a shop manager who already knows each week's and month's totals; number theory is "clock arithmetic" (9 o'clock plus 5 hours is 2 o'clock) that keeps hashing and encryption working. Think of your phone keyboard: the suggestions as you type come from walking a trie.

*Tiny example.* Daily sales `3, 5, 2, 6`; running totals `0, 3, 8, 10, 16`. Sales from day 2 to day 4 = 16 − 3 = **13** (check: 5 + 2 + 6). Fenwick and segment trees keep this working when values change.

*You will learn:*
- Tries (insert, search, prefix search, delete, ranked autocomplete), radix trees and binary tries for maximum XOR.
- String matching: naive, Rabin-Karp, KMP (the LPS array), the Z-algorithm, Manacher's longest palindrome.
- Segment trees with lazy propagation, Fenwick trees and sparse tables for range queries.
- Number theory: GCD/LCM and extended Euclid, the sieve, factorisation, fast modular exponentiation, modular inverse, Euler's totient, nCr mod p, textbook RSA.
- A recap of disjoint-set union.
- Verifying every algorithm against a brute force.

*Key takeaway:* pre-processing once (a trie, an LPS array, a tree of partial sums) turns repeated slow questions into fast ones.

### 12 · 🏭 Industry Project: DSA Inside Real AI Systems

*Explained simply.* This notebook takes the structures from 01–11 into realistic AI-engineering scenarios, each in the same pattern: scenario, naive approach, better data structure, measured gain, production notes. You pick the top 10 products with a heap, deduplicate training data with hashing, cache LLM answers with an LRU + TTL cache, rate-limit clients with a sliding window, and find the first bad model version with binary search. Think of a talent-show judge who only keeps a shortlist of 10 in hand and swaps someone out when a better act appears, instead of ranking all million contestants.

*Tiny example.* Top 3 of `5, 1, 9, 3, 7, 8` with a shortlist of 3: `{1,5,9}` → 3 beats 1 → `{3,5,9}` → 7 beats 3 → `{5,7,9}` → 8 beats 5 → `{7,8,9}`. Each score is looked at once; nothing is fully sorted.

Some gains measured in the notebook (ratios differ slightly between machines):

| Case | Naive | Better | Gain |
|---|---|---|---|
| top-10 of 1M scores (NumPy) | `argsort` | `argpartition` | about 30× faster |
| autocomplete per keystroke | scan the query log | trie + cached top-5 | about 770× faster |
| HMM tagging, 8 words | brute force 4⁸ sequences | Viterbi | about 10,000× faster |
| "seen this URL?" memory | set of strings | Bloom filter (1% false positives) | about 130× smaller |

*You will learn:*
- Heaps for top-k retrieval and merging results from shards.
- Tries for autocomplete and longest-match tokenisation; a tiny BPE tokenizer trainer on hash maps + a priority queue.
- Exact and near-duplicate detection (MinHash + LSH) and a Bloom filter for a crawler.
- BFS recommendations and PageRank by sparse power iteration.
- Edit distance for fuzzy matching and Viterbi for part-of-speech tagging.
- LRU + TTL caching for LLM calls, sliding-window rate limiting, and binary search for threshold tuning and model bisection.

*Key takeaway:* the model is rarely the only bottleneck; the right data structure around it often gives a 10× to 1000× win.

---

## How this connects to the rest of the repo and to real AI systems

- **Arrays → tensors.** NumPy and PyTorch tensors are contiguous strided arrays: [`02_Data_Analysis/02_numpy.ipynb`](../../02_Data_Analysis/02_numpy.ipynb), [`14_Mathematics/01_linear_algebra.ipynb`](../../14_Mathematics/01_linear_algebra.ipynb).
- **Sliding windows → rolling features.** Rolling means for forecasting: [`04_Forecasting/01_time_series_basics.ipynb`](../../04_Forecasting/01_time_series_basics.ipynb).
- **Trees → decision trees and ensembles.** Each node is a test, each leaf a prediction: [`03_Machine_Learning/01_supervised/03_decision_trees.ipynb`](../../03_Machine_Learning/01_supervised/03_decision_trees.ipynb).
- **Heaps → top-k retrieval in RAG and beam search.** [`08_LLM/02_rag/01_rag_fundamentals.ipynb`](../../08_LLM/02_rag/01_rag_fundamentals.ipynb), [`07_NLP/05_language_models_and_generation.ipynb`](../../07_NLP/05_language_models_and_generation.ipynb).
- **Graphs → vector databases, GNNs, knowledge graphs, agent workflows.** HNSW is a proximity graph: [`13_Databases/03_vector_db/01_vector_databases.ipynb`](../../13_Databases/03_vector_db/01_vector_databases.ipynb), [`05_Deep_Learning/07_gnn.ipynb`](../../05_Deep_Learning/07_gnn.ipynb), [`08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb`](../../08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb), [`10_Agents/03_langgraph.ipynb`](../../10_Agents/03_langgraph.ipynb).
- **Tries and hash maps → tokenizers.** [`07_NLP/01_text_preprocessing.ipynb`](../../07_NLP/01_text_preprocessing.ipynb), [`08_LLM/00_start_here_how_llms_work.ipynb`](../../08_LLM/00_start_here_how_llms_work.ipynb).
- **Dynamic programming → reinforcement learning and NLP.** Bellman equations and value iteration: [`11_Reinforcement_Learning/02_dynamic_programming.ipynb`](../../11_Reinforcement_Learning/02_dynamic_programming.ipynb); Viterbi for tagging: [`07_NLP/04_named_entity_recognition.ipynb`](../../07_NLP/04_named_entity_recognition.ipynb).
- **Segment trees → prioritized experience replay** (a sum tree): [`11_Reinforcement_Learning/04_deep_q_networks.ipynb`](../../11_Reinforcement_Learning/04_deep_q_networks.ipynb).
- **BFS, DFS, Dijkstra, backtracking → classical AI search and constraint satisfaction.** [`../classical_ai/02_uninformed_search.ipynb`](../classical_ai/02_uninformed_search.ipynb), [`../classical_ai/03_informed_search.ipynb`](../classical_ai/03_informed_search.ipynb), [`../classical_ai/06_constraint_satisfaction.ipynb`](../classical_ai/06_constraint_satisfaction.ipynb).
- **Caching and rate limiting → production LLM apps and APIs.** [`08_LLM/20_industry_llm_application_patterns.ipynb`](../../08_LLM/20_industry_llm_application_patterns.ipynb), [`12_FastAPI/04_industry_production_ml_api.ipynb`](../../12_FastAPI/04_industry_production_ml_api.ipynb).
- **The full pipeline.** After notebook 12, see everything working together in [`08_LLM/19_industry_rag_pipeline.ipynb`](../../08_LLM/19_industry_rag_pipeline.ipynb).
- **Going further.** NP-completeness, approximation, flows, linear programming and streaming sketches: [`00_AI_Fundamentals/advanced_algorithms/`](../advanced_algorithms/).

---

## Common beginner mistakes

- **Using `x in my_list` inside a loop.** Membership in a list is O(n), so the loop becomes O(n²). Convert to a `set` once and lookups become O(1) on average.
- **Using `list.pop(0)` or `list.insert(0, x)` as a queue.** Both shift every element (O(n)). Use `collections.deque` with `popleft()` / `appendleft()`.
- **Off-by-one errors in binary search.** Mixing closed `[lo, hi]` and half-open `[lo, hi)` conventions causes infinite loops or missed elements. Pick one convention and keep it, or use `bisect`.
- **Forgetting the base case (or progress) in recursion.** The function never stops and Python raises `RecursionError` after about 1000 calls. Every recursive call must move toward a base case.
- **Assuming greedy is always optimal.** It fails for coin change with {1, 3, 4} and for 0/1 knapsack. Test a greedy idea on tiny cases before trusting it.
- **Using Dijkstra with negative edge weights.** It can finalise a vertex too early and return a wrong distance. Use Bellman-Ford instead.
- **Forgetting the "un-choose" step in backtracking.** The shared state is not restored and the search silently misses solutions. Check against a brute force on small inputs.
- **Thinking O(1) means "instant" and Big-O is the whole story.** Big-O hides constants and memory effects; NumPy's O(n log n) sort can beat a pure-Python O(n) loop for realistic n. Always measure as well.

---

## Exam / interview quick-revision

1. **Q:** Time of binary search on n sorted items? **A:** O(log n); at most ⌊log₂ n⌋ + 1 comparisons.
2. **Q:** Why is `list.append` O(1) if the list sometimes copies itself? **A:** The capacity grows geometrically, so copying costs O(1) amortised per append.
3. **Q:** Master theorem result for T(n) = 2T(n/2) + n? **A:** Θ(n log n) (merge sort).
4. **Q:** Lower bound for comparison sorting? **A:** Ω(n log n), because a decision tree must have n! leaves and log₂(n!) = Θ(n log n).
5. **Q:** Quick sort worst case and when? **A:** Θ(n²), when pivots are always the smallest or largest (e.g. a sorted input with a first-element pivot); a random pivot gives Θ(n log n) expected.
6. **Q:** Which common sorts are stable? **A:** Insertion, merge, counting, radix and Timsort; selection, quick and heap sort are not.
7. **Q:** Average and worst lookup in a hash table? **A:** O(1) average with a good hash and bounded load factor; O(n) worst case when keys collide.
8. **Q:** What can a Bloom filter never return? **A:** A false negative; "not present" is always correct.
9. **Q:** How do you build an O(1) LRU cache? **A:** A hash map from key to node plus a doubly linked list ordered by recency.
10. **Q:** How do you detect a cycle in a linked list in O(1) space? **A:** Floyd's tortoise and hare: a slow and a fast pointer meet if there is a cycle.
11. **Q:** Cost of building a heap from n items? **A:** O(n) with bottom-up heapify (not O(n log n)).
12. **Q:** Which traversal of a BST gives sorted order? **A:** Inorder (left, node, right).
13. **Q:** BFS vs. DFS: data structure and use? **A:** BFS uses a queue and finds shortest paths in unweighted graphs; DFS uses a stack or recursion and suits cycle detection and topological sort. Both are O(n + m).
14. **Q:** Two conditions for dynamic programming? **A:** Optimal substructure and overlapping subproblems.
15. **Q:** Time of edit distance between strings of lengths m and n? **A:** Θ(m·n), with Θ(min(m, n)) space if you keep only two rows.

---

## Further reading

**Classic textbooks**
- Cormen, Leiserson, Rivest and Stein, *Introduction to Algorithms* (CLRS), 4th edition, MIT Press, 2022. The standard university text; the notebooks reference its chapters throughout.
- Skiena, *The Algorithm Design Manual*, 3rd edition, Springer, 2020. Practical, with a "catalogue" of problems.
- Sedgewick and Wayne, *Algorithms*, 4th edition, Addison-Wesley, 2011. Clear Java-based explanations and visualisations.
- Kleinberg and Tardos, *Algorithm Design*, Pearson, 2005. Excellent on greedy, divide and conquer, DP and network flow.
- Leskovec, Rajaraman and Ullman, *Mining of Massive Datasets* (free at [mmds.org](http://www.mmds.org/)). MinHash, LSH, Bloom filters and PageRank at scale.

**Free resources**
- [GeeksforGeeks DSA tutorial](https://www.geeksforgeeks.org/learn-data-structures-and-algorithms-dsa-tutorial/), which this module follows topic by topic.
- [MIT OpenCourseWare 6.006 Introduction to Algorithms](https://ocw.mit.edu/courses/6-006-introduction-to-algorithms-spring-2020/) (lectures, notes and problem sets).
- [Python wiki: TimeComplexity](https://wiki.python.org/moin/TimeComplexity), the cost of every built-in operation.
- [VisuAlgo](https://visualgo.net/), animations of sorting, trees, heaps, hashing and graph algorithms.
- [LeetCode](https://leetcode.com/) and [NeetCode](https://neetcode.io/) problem lists for interview practice by pattern.
