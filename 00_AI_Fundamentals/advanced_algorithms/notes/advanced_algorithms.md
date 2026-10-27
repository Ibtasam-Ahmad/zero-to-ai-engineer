# Advanced Algorithms: Study Guide

This guide is the conceptual companion to the ten notebooks in [`00_AI_Fundamentals/advanced_algorithms/`](../). It follows the notebooks in order, defines each term the first time it appears, works small examples by hand, and states the key formulas and bounds. Near the end are a **complexity-class cheat sheet** and a **"which algorithm for which problem" table**, followed by a glossary. The notebooks contain the runnable code, plots and measurements; this guide explains the ideas behind them.

The module is the second half of a university algorithms sequence. Do the core [DSA module](../../dsa/) and the [discrete mathematics module](../../../14_Mathematics/discrete_math/) first; the [DSA study guide](../../dsa/notes/dsa.md) has the big-O cheat sheet for the basic structures this guide builds on.

---

## 1. Amortized and Randomized Algorithms

### Amortized analysis

**Amortized analysis** bounds the **total** cost of any sequence of $n$ operations, then divides by $n$. There is no probability: the bound holds for the worst possible sequence. It answers "an operation is sometimes expensive, but how expensive can a long run be?"

Three methods give the same answer from different angles:

| Method | Idea | Binary counter (increment) |
|---|---|---|
| Aggregate | sum the actual costs of all $n$ operations, divide by $n$ | bit $i$ flips every $2^i$ steps, so total $\le \sum_i n/2^i < 2n$ |
| Accounting | charge each operation a fixed fee; surplus is stored as **credit** on the data structure and pays for expensive steps later | charge 2 per set bit: 1 pays for setting it, 1 is saved to pay for clearing it later |
| Potential | define $\Phi(D_i) \ge \Phi(D_0)$; amortized cost $\hat c_i = c_i + \Phi(D_i) - \Phi(D_{i-1})$; the sum telescopes | $\Phi$ = number of 1-bits; each increment has $\hat c_i = 2$ |

**Worked example (the counter by hand).** From 0 to 8 the flips are 1, 2, 1, 3, 1, 2, 1, 4: total 15 for 8 increments, under $2n = 16$.

**Dynamic arrays.** Growing by a constant **factor** $r > 1$ gives $O(1)$ amortized append, because total copying is a geometric series $n + n/r + n/r^2 + \dots \le \frac{r}{r-1} n$. Growing by a constant **amount** $k$ gives $\Theta(n^2/k)$ total copies, which is $\Theta(n)$ per append. CPython lists grow by about 1.125×. A classic exam trap: if an array doubles when full and halves when **half** full, alternating push/pop at the boundary costs $\Theta(n)$ each; the fix is to halve only at **one quarter** full.

### Union-find (disjoint-set union)

Union-find maintains a partition of elements into sets with `find(x)` (which set?) and `union(x, y)`. Each set is a tree whose root is its representative. Two heuristics:
- **Union by rank (or size):** attach the shorter tree under the taller one, so heights stay $O(\log n)$.
- **Path compression:** during `find`, point every visited node straight at the root.

Together, $m$ operations cost $O(m\,\alpha(n))$, where $\alpha$ is the inverse Ackermann function. The Ackermann function grows so fast ($A_3(1) = 2047$, $A_4(1)$ is astronomically larger than $10^{100}$) that $\alpha(n) \le 4$ for any $n$ that fits in the universe. **Why it matters:** Kruskal's MST, connected components, clustering near-duplicate documents and Karger's min-cut all run on it.

### Randomized algorithms

A **randomized algorithm** makes random choices. Two kinds:

| Kind | Always correct? | Running time | Examples |
|---|---|---|---|
| **Las Vegas** | yes | random; we bound its expectation | randomized quicksort, quickselect, skip lists, treaps |
| **Monte Carlo** | no, small error probability | bounded | Miller–Rabin, Karger's min-cut, Bloom-filter lookups |

**Amplification.** If one Monte Carlo run fails with probability at most $p$ and runs are independent, $k$ runs all fail with probability at most $p^k$. A Las Vegas algorithm that succeeds with probability $p$ per try needs $1/p$ tries in expectation (a geometric distribution).

**Randomized quicksort.** Choose the pivot uniformly at random. Elements $z_i < z_j$ (in sorted order) are compared exactly when one of them is the first pivot chosen from $\{z_i, \dots, z_j\}$, which has probability $\frac{2}{j - i + 1}$. Summing over pairs gives $E[\text{comparisons}] = 2(n+1)H_n - 4n \approx 2n \ln n \approx 1.39\, n \log_2 n$ on **every** input. **Quickselect** recurses into one side only and finds the $k$-th smallest in $O(n)$ expected time.

**Universal hashing.** A family $\mathcal{H}$ of hash functions is **universal** if for every pair of distinct keys $x \ne y$, $\Pr_{h \in \mathcal{H}}[h(x) = h(y)] \le 1/m$. The classic family is $h_{a,b}(x) = ((ax + b) \bmod p) \bmod m$ with a prime $p$ larger than every key. Because $h$ is chosen at random **after** the adversary picks the keys, no fixed input is bad. The notebook shows Python's `hash(x) % m` sending 2,000 crafted keys into one bucket while a random universal function spreads them.

**Skip lists and treaps.** A **skip list** is a sorted linked list with express lanes: each node is promoted to the next level with probability ½, so level $i$ holds about $n/2^i$ nodes, total pointers $\approx 2n$, and search, insert and delete take $O(\log n)$ expected time. A **treap** is a BST on keys that is also a heap on random priorities; its shape is that of a BST built from a random insertion order, so its height is $O(\log n)$ expected even if keys arrive sorted.

**Miller–Rabin.** Write $n - 1 = 2^s d$ with $d$ odd. For a random base $a$, $n$ passes if $a^d \equiv 1$ or $a^{2^r d} \equiv -1 \pmod n$ for some $0 \le r < s$. Every prime passes; a composite passes for at most ¼ of bases, so $k$ rounds give error $\le 4^{-k}$. Fermat's simpler test is fooled by Carmichael numbers such as 561.

**Karger's min-cut.** Repeatedly contract a random edge until two super-vertices remain; the edges between them form a cut. One run finds a specific minimum cut with probability at least $\frac{2}{n(n-1)} = 1/\binom{n}{2}$. Running $\binom{n}{2}\ln n$ times drives the failure probability below $1/n$.

**Why it matters for AI.** SGD is a randomized algorithm (an unbiased gradient estimate from a random mini-batch); random restarts make hill climbing a Las Vegas search; randomized SVD finds the top singular vectors by multiplying with a small random matrix (about 8× faster in the notebook, with the same top-10 singular values); HNSW vector indexes assign each vector a random top layer exactly like a skip list.

---

## 2. NP-Completeness and Reductions

### Decision problems and the classes

Complexity classes are defined for **decision problems** (yes/no answers), measured against the input length in **bits**. An optimisation problem ("smallest vertex cover") becomes a decision problem ("is there a cover of size $\le k$?"); binary search over $k$ recovers the optimum with $O(\log n)$ calls.

- **P:** solvable in polynomial time $O(n^c)$.
- **NP:** every yes-instance has a polynomial-size **certificate** that a polynomial-time **verifier** accepts. NP stands for *nondeterministic polynomial*, not "non-polynomial". $P \subseteq NP$.
- **co-NP:** no-instances have short certificates (e.g. TAUTOLOGY: a falsifying assignment certifies "no").
- **Polynomial-time (Karp) reduction** $A \le_p B$: a polynomial-time function $f$ with $x \in A \iff f(x) \in B$. Read it as "A is no harder than B".
- **NP-hard:** every NP problem reduces to it (it need not be in NP, or even decidable).
- **NP-complete:** NP-hard **and** in NP.

**Recipe for proving X NP-complete:** (1) show X ∈ NP by writing a verifier; (2) reduce a **known** NP-complete problem **to** X. Getting the direction backwards is the most common exam error.

### Cook–Levin and the catalogue

The **Cook–Levin theorem** (1971/1973) says SAT is NP-complete. Proof idea: any NP verifier runs for $p(n)$ steps, so its whole computation is a $p(n) \times p(n)$ table; Boolean variables describe each cell, and clauses check that every small window follows the machine's rules and that the last row accepts. The formula is satisfiable exactly when some certificate makes the verifier accept. Karp (1972) then showed 21 problems NP-complete by chains of reductions.

| NP-complete | Look-alike in P |
|---|---|
| 3-SAT | 2-SAT (implication graph + strongly connected components, linear time) |
| 3-colouring | 2-colouring (bipartiteness by BFS) |
| Hamiltonian cycle | Euler circuit (connected, all degrees even) |
| longest simple path | shortest path |
| max cut | min cut (max flow) |
| integer LP feasibility | LP |
| 0/1 knapsack, subset sum | fractional knapsack (greedy) |

### SAT solving

**DPLL** improves brute force with **unit propagation** (a clause with one unassigned literal forces it), **pure-literal elimination** and branching with backtracking. Modern **CDCL** solvers add clause learning and restarts. On random 3-SAT with $n$ variables and $m$ clauses, the probability of satisfiability drops sharply near $m/n \approx 4.26$ (the **phase transition**), and that is where instances are hardest.

### Reductions by hand

**3-SAT ≤ₚ Independent Set:** for each clause make a triangle of its three literals; connect every literal to its negation in other triangles; ask for an independent set of size $k$ = number of clauses. Picking one true literal per clause gives such a set, and vice versa.

**Independent Set ⇔ Vertex Cover:** $S$ is independent iff $V \setminus S$ is a vertex cover, so "IS of size $\ge k$" ⇔ "VC of size $\le n - k$". **Independent Set ⇔ Clique:** $S$ is independent in $G$ iff it is a clique in the complement graph $\bar G$.

### Pseudo-polynomial time

The knapsack DP runs in $O(nW)$. The input stores $W$ in about $\log_2 W$ bits, so $O(nW) = O(n \cdot 2^{\text{bits}})$: exponential in the input length. Such algorithms are **pseudo-polynomial**, and problems that have them are **weakly NP-hard** (knapsack, subset sum, partition). Problems that stay NP-hard even when all numbers are small (TSP, bin packing, 3-partition) are **strongly NP-hard** and have no pseudo-polynomial algorithm unless P = NP.

### Coping with NP-hardness

Being NP-hard means choosing which guarantee to drop: polynomial time (smart exponential search, branch-and-bound, DP over subsets), optimality (approximation), generality (special structure such as trees or bipartite graphs), all exponential dependence except on a small parameter (FPT), any guarantee (heuristics such as simulated annealing and 2-opt), or control (call a SAT/MILP/CP solver).

**Why it matters for AI.** Exact Bayesian-network inference, learning the smallest decision tree, best-subset feature selection, optimal k-means (even for $k = 2$) and training a tiny 3-node network to fit data exactly are all NP-hard. This is *why* ML relies on greedy splitting (CART), the lasso, Lloyd's algorithm, sampling and SGD.

---

## 3. Approximation and Parameterized Algorithms

### Approximation ratios

A **ρ-approximation** returns, on **every** input, a solution of cost $\le \rho \cdot OPT$ (minimisation) or value $\ge OPT/\rho$ (maximisation; some books write $\ge \rho \cdot OPT$ with $\rho < 1$). Because OPT is unknown, proofs compare the answer with a computable **lower bound on OPT**.

| Problem | Algorithm | Ratio | Lower bound used |
|---|---|---|---|
| Vertex cover | both endpoints of a maximal matching | 2 | any cover must contain one endpoint of each matched edge, so $OPT \ge \lvert M \rvert$ |
| Set cover | repeatedly take the set covering the most uncovered elements | $H(n) \approx \ln n + 0.58$ | charging argument |
| Metric TSP | double the MST, take an Euler tour, shortcut repeats | 2 | deleting one edge of the optimal tour gives a spanning tree, so $MST \le OPT$ |
| Metric TSP | Christofides: MST + min-weight perfect matching on odd-degree vertices | 1.5 | the matching costs $\le OPT/2$ |
| k-center | farthest-first traversal | 2 | pigeonhole: two of $k+1$ far-apart points share an optimal center |
| Max coverage / monotone submodular | greedy by marginal gain | $1 - 1/e \approx 0.632$ | Nemhauser–Wolsey–Fisher |

**Worked example (vertex cover).** Path A–B–C–D. Matching {A–B, C–D} gives cover {A, B, C, D} of size 4; $OPT = 2$ ({B, C}); ratio exactly 2. Ten disjoint edges show the bound is tight: the algorithm takes 20 vertices, OPT is 10. Taking only one endpoint per matched edge fails: {A, D} leaves B–C uncovered.

**Schemes.** A **PTAS** gives ratio $1 + \varepsilon$ for any fixed $\varepsilon > 0$ in time polynomial in $n$ (possibly like $n^{1/\varepsilon}$). An **FPTAS** is polynomial in both $n$ and $1/\varepsilon$. The knapsack FPTAS rounds values down to multiples of $K = \varepsilon v_{\max}/n$, runs the DP over (scaled) values, and returns value $\ge (1 - \varepsilon)OPT$ in $O(n^3/\varepsilon)$.

**Inapproximability.** General (non-metric) TSP has **no** constant-ratio approximation unless P = NP: give graph edges weight 1 and non-edges weight $\rho n + 1$; a tour of cost $\le \rho n$ exists iff the graph has a Hamiltonian cycle. Set cover cannot be approximated within $(1 - \varepsilon)\ln n$ unless P = NP, so greedy is essentially optimal.

### Parameterized complexity

A problem is **fixed-parameter tractable (FPT)** in parameter $k$ if it can be solved in $f(k) \cdot n^{O(1)}$ time. **Vertex cover** by bounded search: pick any edge $(u, v)$; one endpoint must be in the cover, so branch on $u$ or $v$ with budget $k - 1$. The tree has $\le 2^k$ leaves, giving $O(2^k (n + m))$. **Kernelization** shrinks the input first: a vertex of degree $> k$ must be in any cover of size $\le k$; after removing those, a yes-instance has at most $k^2$ edges. The notebook solves $n = 1000$, $k = 12$ instantly where brute force would check $10^{15}$+ subsets.

### Submodularity

A set function $f$ is **submodular** (diminishing returns) if for $S \subseteq T$ and $x \notin T$:
$$f(S \cup \{x\}) - f(S) \ge f(T \cup \{x\}) - f(T).$$
For monotone submodular $f$ with $f(\emptyset) = 0$, greedy achieves $f(S) \ge (1 - 1/e)\,OPT$, and beating that is NP-hard. **Why it matters:** choosing $k$ chunks for an LLM's context that are relevant *and* diverse (the facility-location objective), extractive summarisation and training-data subset selection. In the notebook, greedy reached 99 % of the exhaustive optimum and covered all 4 topics, while plain top-k relevance covered 1.

---

## 4. Network Flows and Matching

### Definitions

A **flow network** is a directed graph with a source $s$, a sink $t$ and capacities $c(u, v) \ge 0$. A **flow** satisfies the **capacity constraint** $0 \le f(u, v) \le c(u, v)$ and **conservation** (inflow = outflow at every vertex except $s$ and $t$). Its value $|f|$ is the net flow out of $s$. The **residual graph** $G_f$ has a forward edge with capacity $c - f$ wherever capacity is unused, and a **backward** edge with capacity $f$ wherever flow could be undone. An **augmenting path** is an $s$–$t$ path in $G_f$.

### Algorithms

| Algorithm | Rule | Time |
|---|---|---|
| Ford–Fulkerson | any augmenting path | $O(E \cdot \lvert f^* \rvert)$ with integer capacities; may not terminate with irrational ones |
| Edmonds–Karp | shortest augmenting path (BFS) | $O(VE^2)$ |
| Dinic | blocking flows on BFS level graphs | $O(V^2 E)$; $O(E\sqrt V)$ on unit bipartite graphs |
| Push–relabel | local pushes with height labels | $O(V^3)$ (FIFO) |

The notebook's "unlucky" Ford–Fulkerson needs $2C$ augmentations on a 4-node graph with capacity $C$, while Edmonds–Karp needs 2 regardless of $C$.

**Max-flow min-cut theorem.** An $s$–$t$ **cut** $(S, T)$ splits vertices with $s \in S$, $t \in T$; its capacity is the sum of capacities from $S$ to $T$. For any flow and any cut, $|f| \le c(S, T)$ (weak duality). When no augmenting path remains, let $S$ be the vertices reachable from $s$ in $G_f$: every edge out of $S$ is saturated, so $|f| = c(S, T)$. Hence max flow = min cut, and the cut is a **certificate** of optimality. With integer capacities there is always an integral maximum flow.

**Worked example.** S → A (3), A → T (2), S → B (4), B → T (5). Push 2 on S–A–T and 4 on S–B–T: value 6. Residual reachability from S: A (1 unit left on S → A), but not T via A (A → T full), and not B (S → B full). Cut $S = \{S, A\}$: edges A → T (2) and S → B (4), capacity 6. Equal, so optimal.

### Matching and assignment

**Bipartite matching** = max flow with unit capacities from $s$ to the left side, left to right along allowed pairs, right side to $t$. **Hopcroft–Karp** augments along a maximal set of shortest vertex-disjoint augmenting paths per phase; $O(\sqrt V)$ phases give $O(E\sqrt V)$. **Hall's theorem:** a bipartite graph has a matching saturating the left side $L$ iff $|N(X)| \ge |X|$ for every $X \subseteq L$; when it fails, the alternating-path search produces the violating $X$. **König's theorem:** in bipartite graphs, maximum matching size = minimum vertex cover size.

The **assignment problem** (min-cost perfect matching in a complete bipartite graph with an $n \times n$ cost matrix) is solved by the **Hungarian algorithm** in $O(n^3)$ using dual potentials and tight edges; in practice use `scipy.optimize.linear_sum_assignment`. **Min-cost flow** adds a per-unit cost to each edge and supplies/demands at nodes; it generalises shortest paths, max flow and assignment, and with integer data it has integral optima.

**Why it matters for AI.** DETR-style detectors match predicted boxes to ground truth with the Hungarian algorithm before computing the loss; SORT/ByteTrack trackers do per-frame assignment; graph-cut segmentation (GrabCut) is a min cut; optimal transport (Wasserstein distances, Sinkhorn) generalises min-cost flow; routing requests to replicas or tickets to skilled agents is min-cost max-flow (in the notebook it assigned 30 of 35 tickets where greedy managed 28).

---

## 5. Linear and Integer Programming

### Formulation

An LP in standard inequality form:
$$\max_{x} \; c^\top x \quad \text{s.t.} \quad Ax \le b,\; x \ge 0.$$
**Worked model.** $x$ desks, $y$ chairs (profits in hundreds of dollars): maximise $3x + 5y$ subject to $x \le 4$, $2y \le 12$, $3x + 2y \le 18$, $x, y \ge 0$. Corners of the feasible polygon: (0, 0) → 0, (4, 0) → 12, (4, 3) → 27, (2, 6) → 36, (0, 6) → 30. Optimum (2, 6), profit 36 = $3,600.

### Geometry and the simplex method

The feasible set is a convex **polytope**. A linear objective over it, if bounded, attains its optimum at a **vertex** (a **basic feasible solution**). The **simplex method** moves from vertex to adjacent better vertex: choose an entering variable with positive **reduced cost**, use the **ratio test** to find the leaving variable, pivot. **Two-phase simplex** first finds a feasible vertex for $\ge$ and $=$ constraints. **Degeneracy** (a basic variable equal to 0) can make the method **cycle**; **Bland's rule** (smallest index enters and leaves) prevents it. Dantzig's rule takes $2^n - 1$ pivots on the **Klee–Minty cube**, so simplex is exponential in the worst case, yet LP is in **P** via the ellipsoid method (Khachiyan, 1979) and interior-point methods (Karmarkar, 1984). In practice simplex and interior point (both in HiGHS) solve LPs with millions of variables.

### Duality

The dual of $\max\{c^\top x : Ax \le b, x \ge 0\}$ is $\min\{b^\top y : A^\top y \ge c, y \ge 0\}$.
- **Weak duality:** any feasible $x, y$ satisfy $c^\top x \le b^\top y$.
- **Strong duality:** if either has a finite optimum, both do and they are equal.
- **Complementary slackness:** at optimality, $y_i > 0$ only for tight constraints, and $x_j > 0$ only for tight dual constraints.

The optimal $y_i$ is the **shadow price** of resource $i$. In the desk/chair model $y = (0, 1.5, 1)$: an extra hour on machine A is worth nothing (it has slack), on machine B $150, on machine C $100, valid within the **sensitivity range** (for machine C, between 12 and 24 hours; the notebook's grid search reports about 12.25 to 23.75). Max-flow min-cut is LP duality for the flow LP.

### Integer programming

An **ILP** requires integer variables; a **MILP** mixes integer and continuous ones. Even 0/1 ILP feasibility is NP-hard. Rounding the **LP relaxation** fails: in the notebook the LP optimum is (1.857, 0) with value 39, while the integer optimum is (0, 3) with value 33, far from any rounding.

**Branch-and-bound:** solve the LP relaxation (an upper bound for maximisation); if the solution is fractional in $x_j = 1.857$, branch into $x_j \le 1$ and $x_j \ge 2$; prune a node if its LP is infeasible, integral (a new **incumbent**), or its bound is no better than the incumbent. The gap between the LP bound and the integer optimum is the **integrality gap**; a **tight formulation** (one whose LP relaxation is close to the integer hull) shrinks the tree. The notebook's strong facility-location formulation has gap 0 % and is solved at the root, while an aggregated formulation has a 22 % gap.

**Totally unimodular** constraint matrices (flows, bipartite matching, transportation) have integral vertices, so the LP gives integer solutions for free.

### Modelling tricks

| Need | Linear trick |
|---|---|
| $t = \lvert r \rvert$ in a minimisation | $t \ge r$, $t \ge -r$ |
| minimise the maximum (makespan) | variable $T$ with $T \ge \text{load}_k$ for every $k$; minimise $T$ |
| "if $z = 0$ then $q = 0$" (fixed charge) | $q \le M z$, $z \in \{0, 1\}$, with $M$ as small as valid |
| at most $k$ of a set of options | $\sum z_i \le k$ |
| either constraint 1 or constraint 2 | big-M on each with a binary selector |

Huge big-M values weaken the LP relaxation and cause numerical trouble. When a model is infeasible, find an **irreducible infeasible subset (IIS)**: a set of constraints that is infeasible but becomes feasible if any one is removed.

**Why it matters for AI.** Least-absolute-deviation regression ($\min \sum |r_i|$) and the L1-SVM are LPs; MAP inference in graphical models is an ILP with an LP relaxation; verifying a ReLU network against adversarial inputs is a MILP with big-M per ReLU; GPU job scheduling, LLM batch serving and ad-budget allocation are MILPs/LPs whose duals give "is one more GPU-hour worth buying?".

---

## 6. Streaming and Sketching Algorithms

### The model

In the **data-stream model** the input $a_1, \dots, a_N$ is read **once, in order**, with memory sublinear in $N$ and in the universe size, and fast per-item updates. Exact answers often need linear space (exact distinct counting needs $\Omega(n)$ bits), so we accept an **$(\varepsilon, \delta)$ guarantee**: error at most $\varepsilon$ with probability at least $1 - \delta$. A **sketch** is the small summary; it is **mergeable** if $\text{sketch}(A \cup B)$ can be computed from $\text{sketch}(A)$ and $\text{sketch}(B)$.

### The sketches

| Question | Sketch | Memory | Guarantee |
|---|---|---|---|
| uniform sample of $k$ | reservoir sampling (Algorithm R) | $O(k)$ | exact uniformity |
| items with frequency $> N/(k+1)$ | Misra–Gries ($k$ counters) | $O(k)$ | under-counts by at most $N/(k+1)$ |
| top-$k$ | Space-Saving | $O(k)$ | over-counts by at most $N/k$ |
| frequency of any item | Count-Min | $\lceil e/\varepsilon\rceil \times \lceil \ln(1/\delta)\rceil$ counters | $\hat f \le f + \varepsilon N$ w.p. $\ge 1 - \delta$; never under |
| number of distinct items | HyperLogLog | $m$ small registers | relative std. error $\approx 1.04/\sqrt m$ |
| Jaccard similarity | MinHash ($k$ hashes) | $O(k)$ per set | std. error $\le 0.5/\sqrt k$ |
| p95 / p99 | log-bucket (DDSketch-style) or KLL compactors | small | relative-value error $\alpha$, or rank error $\varepsilon$ |
| 1s in the last $W$ bits | DGIM exponential histogram | $O(\log^2 W)$ bits | at most 50 % error |

**Reservoir sampling by hand.** Keep the first $k$ items; item $i > k$ replaces a random slot with probability $k/i$. Induction shows each of the first $i$ items is in the reservoir with probability $k/i$. For $k = 1$ and 4 items, item 1 survives with $1 \cdot \tfrac12 \cdot \tfrac23 \cdot \tfrac34 = \tfrac14$.

**Count-Min.** $d$ rows of $w$ counters, one hash per row; an update adds to one counter per row, a query takes the **minimum** over rows (every row over-counts because of collisions; the minimum over-counts least). With $w = \lceil e/\varepsilon \rceil$, the expected excess in one row is $\le N/w$, Markov's inequality gives $\Pr[\text{excess} > \varepsilon N] \le 1/e$, and $d = \lceil \ln(1/\delta)\rceil$ independent rows push it to $\le \delta$. Example: $\varepsilon = 0.001$, $\delta = 0.01$ → $2719 \times 5$ counters.

**HyperLogLog.** Hash each item; the first $p$ bits choose one of $m = 2^p$ registers, which stores the maximum position of the first 1-bit in the rest. Seeing a run of $\rho$ leading zeros suggests about $2^\rho$ distinct items; a harmonic mean across registers with a bias correction gives the estimate. 4,096 six-bit registers (3 KB) give about 1.6 % error; the notebook measured 3.2 % on one stream of 10,060 distinct items and under 2 % on daily-user counts. Merge two sketches by taking the register-wise **max**.

**MinHash and LSH.** For a random permutation (hash) $h$, $\Pr[\min h(A) = \min h(B)] = J(A, B) = \frac{|A \cap B|}{|A \cup B|}$. With $k$ hashes split into $b$ **bands** of $r$ rows, two sets become candidates if any band matches entirely: $\Pr = 1 - (1 - s^r)^b$, an S-curve with threshold near $(1/b)^{1/r}$. Only candidates are compared exactly, turning all-pairs $O(n^2)$ into near-linear work. In the notebook, LSH found 74 of 76 near-duplicate pairs with 76 comparisons instead of 79,800.

**Why it matters for AI.** MinHash dedup of pre-training and fine-tuning corpora; HyperLogLog for unique users and fraud features ("distinct devices per account in 24 h"); Count-Min and the hashing trick for high-cardinality features; quantile sketches for p99 latency and token counts in LLMOps dashboards; reservoir samples of production traffic for evaluation sets. Spark, BigQuery, Redis and DuckDB ship these sketches.

---

## 7. Computational Geometry and the FFT

### Primitives

For points $a, b, c$ the **orientation** is the cross product
$$\text{orient}(a, b, c) = (b_x - a_x)(c_y - a_y) - (b_y - a_y)(c_x - a_x),$$
positive if $c$ is left of $\vec{ab}$ (counter-clockwise turn), negative if right, zero if collinear. Two segments properly intersect iff each one's endpoints lie on opposite sides of the other (plus special collinear cases). With floating point, near-collinear inputs can get the **wrong sign**, so use integers, exact fractions or robust predicates (Shewchuk).

### Algorithms

| Problem | Algorithm | Time |
|---|---|---|
| Convex hull | Graham scan (sort by angle) or Andrew's monotone chain (sort by x, build lower and upper hulls, pop while not a left turn) | $O(n \log n)$; lower bound $\Omega(n \log n)$ by reduction from sorting |
| Meeting rooms / interval overlap | sweep over sorted start and end events | $O(n \log n)$ |
| All segment intersections | Bentley–Ottmann sweep (test only neighbours in the sweep order) | $O((n + k)\log n)$ for $k$ intersections |
| Point in polygon | ray casting (odd number of crossings = inside) | $O(n)$ |
| Polygon area | shoelace: $A = \tfrac12 \sum_i (x_i y_{i+1} - x_{i+1} y_i)$ | $O(n)$; sign gives orientation |
| Voronoi / Delaunay | Fortune's sweep, or incremental flips | $O(n \log n)$ |

The **Voronoi diagram** splits the plane into cells of points closest to each site; the **Delaunay triangulation** is its dual, with the **empty-circumcircle** property, $O(n)$ edges, and it contains the Euclidean minimum spanning tree. A 1-nearest-neighbour classifier's decision regions are unions of Voronoi cells, and k-means assigns points to the Voronoi cells of its centroids.

### The FFT

The **discrete Fourier transform** of $a_0, \dots, a_{n-1}$ evaluates the polynomial $A(x) = \sum a_j x^j$ at the $n$-th **roots of unity** $\omega_n^k = e^{2\pi i k/n}$ (sign conventions vary; NumPy uses $e^{-2\pi i jk/n}$). **Cooley–Tukey** splits into even and odd coefficients: $A(x) = A_{\text{even}}(x^2) + x A_{\text{odd}}(x^2)$, and since $(\omega_n^k)^2 = \omega_{n/2}^k$ the two halves are DFTs of size $n/2$. Also $\omega_n^{k + n/2} = -\omega_n^k$, so
$$y_k = E_k + \omega_n^k O_k, \qquad y_{k + n/2} = E_k - \omega_n^k O_k,$$
giving $T(n) = 2T(n/2) + O(n) = O(n \log n)$.

**Polynomial multiplication.** Evaluate both polynomials at $\ge \deg + 1$ points with the FFT, multiply pointwise, interpolate with the inverse FFT. **Worked example:** $(1 + 2x)(3 + x)$: at the 4 points $1, i, -1, -i$ the values are $3, 1+2i, -1, 1-2i$ and $4, 3+i, 2, 3-i$; pointwise products $12, 1+7i, -2, 1-7i$; the inverse FFT returns $3 + 7x + 2x^2$. The **convolution theorem** $\mathcal{F}(a * b) = \mathcal{F}(a)\cdot\mathcal{F}(b)$ makes convolution $O(n \log n)$; pad both sequences to length $\ge n + m - 1$, otherwise the result is **circular** and the tail wraps onto the start. Note that deep-learning "convolution" layers actually compute cross-correlation (no kernel flip).

**Why it matters for AI.** CNN layers and FFT-based long convolutions (S4, Hyena) for sequences of thousands of tokens; spectrograms (short-time FFTs) as the input to speech models; IoU, convex hulls and point-in-polygon in vision and geospatial ML; Voronoi geometry behind nearest-neighbour methods.

---

## 8. Advanced Data Structures

| Structure | Supports | Cost |
|---|---|---|
| Sparse table | range min/max/gcd on static data | build $O(n \log n)$, query $O(1)$ (two overlapping power-of-two blocks; needs an **idempotent** operation) |
| Sqrt decomposition | range sums with point updates | query $O(\sqrt n)$, update $O(1)$ |
| Segment tree (from `dsa/11`) | range queries with updates | $O(\log n)$ each |
| Suffix array + LCP | substring search, repeats, distinct substrings | build $O(n \log^2 n)$ by prefix doubling with comparison sort ($O(n \log n)$ with radix sort), LCP $O(n)$ by Kasai, search $O(m \log n)$ |
| Interval tree | all intervals overlapping a query | $O(\log n + k)$ for $k$ results when balanced |
| KD-tree | nearest neighbour, range search in low dimension | build $O(n \log n)$; queries fast for small $d$, near brute force for large $d$ |
| Red-black tree (LLRB) | ordered map | height $\le 2\log_2(n+1)$, $O(\log n)$ operations |
| Persistent tree (path copying) | access every past version | $O(\log n)$ new nodes per update |
| LSM tree | write-heavy key-value store | fast sequential writes; reads check memtable then SSTables (Bloom filters skip most) |
| Gap buffer / rope | text editing | gap buffer $O(1)$ at the cursor, $O(d)$ to move it; rope $O(\log n)$ split/concat/index |

**Suffix array by hand.** For "banana" the suffixes sorted are a(5), ana(3), anana(1), banana(0), na(4), nana(2): SA = [5, 3, 1, 0, 4, 2], LCP = [0, 1, 3, 0, 0, 2]. Every occurrence of a pattern is a contiguous block of SA, found by binary search. The longest repeated substring is the maximum LCP ("ana", length 3). Distinct substrings $= \frac{n(n+1)}{2} - \sum \text{LCP} = 21 - 6 = 15$.

**Interval tree.** A BST keyed by start, where each node also stores `max_end`, the largest end in its subtree. When searching for overlaps with $[lo, hi]$, skip any subtree whose `max_end` $< lo$. Two intervals $[a, b)$ and $[c, d)$ overlap iff $a < d$ and $c < b$.

**KD-tree and the curse of dimensionality.** Split at the median, alternating axes. Nearest-neighbour search descends to the query's leaf, then backtracks into the far side of a split only if the splitting plane is closer than the best distance so far. In 2-D the notebook's tree visited 0.4 % of nodes; as dimension rises nearly every node must be visited, because in high dimensions almost all points are about equally far away. That is why embedding search uses approximate indexes (HNSW, IVF).

**Red-black trees as 2-3-4 trees.** A red link glues a node to its parent, forming a 3-node or 4-node; the invariants (no two reds in a row, equal black height on every root-to-leaf path) are exactly "a 2-3-4 tree with all leaves at the same depth", which forces height $\le 2\log_2(n+1)$. LLRB insertion needs only rotate-left, rotate-right and colour-flip. Sorted inserts give a plain BST of height $n$; the LLRB stays logarithmic.

**LSM tree.** Writes go to an in-memory sorted **memtable**; when full, it is flushed as an immutable sorted **SSTable**; background **compaction** merges SSTables. A Bloom filter per SSTable makes lookups for absent keys cheap. The trade-off versus a B+ tree is **write amplification** (data rewritten during compaction) for fast sequential writes. RocksDB and Cassandra are LSM engines.

**Why it matters for AI.** Suffix arrays deduplicate exact repeated substrings in LLM corpora and power infini-gram $n$-gram counts over trillions of tokens; KD-trees serve exact kNN in scikit-learn; LSM trees sit under feature stores and event logs; persistence is how JAX and data-versioning tools keep old versions cheaply.

---

## 9. The Coding Interview Method

The workbook teaches a **7-step method**: (1) **clarify** inputs, sizes and edge cases; (2) work small **examples** by hand; (3) state a **brute force** and its complexity; (4) **optimise** by spotting a pattern; (5) **code** cleanly; (6) **test** with fixed cases and random cases against the brute force; (7) **analyse** time and space. The brute force from step 3 becomes the **test oracle** in step 6.

**Pattern map.**

| The question says... | Pattern | Typical cost |
|---|---|---|
| sorted array, pair/triplet with a target | two pointers | $O(n)$ after sorting |
| longest/shortest contiguous window with a monotone condition | sliding window | $O(n)$ |
| count subarrays with sum $k$ (negatives allowed) | prefix sums + hash map | $O(n)$ |
| seen before, complement, group by canonical form | hash map / set | $O(n)$ expected |
| brackets, next greater element, histogram | (monotonic) stack | $O(n)$ |
| "minimum X such that a monotone check passes" | binary search on the answer | $O(n \log M)$ |
| k largest, merge k sorted, running median | heap | $O(n \log k)$ |
| meetings, overlaps | sort + sweep, or greedy by end time | $O(n \log n)$ |
| grid regions, fewest steps, spreading | BFS / DFS | $O(RC)$ |
| prerequisites, build order | topological sort | $O(V + E)$ |
| merging groups, undirected cycle | union-find | $O(\alpha(n))$ per op |
| count ways / min cost with overlapping subproblems | dynamic programming | states × transitions |
| all subsets / permutations / placements | backtracking | exponential, output-sensitive |
| many prefix queries over words | trie | $O(L)$ per query |
| pairs cancel, small sets as masks | bit manipulation | $O(n)$ or $O(2^n)$ |

**Checking complexity empirically.** Time the function at doubling sizes and fit the slope of $\log t$ against $\log n$: slope ≈ 1 means linear, ≈ 2 quadratic. The notebook measured slope 2.18 for brute-force Two Sum.

**ML-flavoured questions** expect building blocks from scratch: Lloyd's k-means with k-means++ seeding; ROC AUC as the probability a random positive outranks a random negative (the rank formula); IoU $= \frac{|A \cap B|}{|A \cup B|}$ and greedy non-maximum suppression; temperature, top-k and top-p (nucleus) sampling; BPE merges; an $O(1)$ LRU cache (hash map + doubly linked list, or `OrderedDict`).

---

## 10. Parallel and External-Memory Algorithms

### Work, span and scheduling

Model a parallel computation as a DAG of unit tasks. **Work** $T_1$ = number of tasks (time on one processor); **span** $T_\infty$ = longest path (time with unlimited processors); **parallelism** $= T_1/T_\infty$. With $p$ processors:
$$T_p \ge T_1/p \;\;(\text{work law}), \qquad T_p \ge T_\infty \;\;(\text{span law}), \qquad T_p \le T_1/p + T_\infty \;\;(\text{greedy scheduler, Brent/Graham}).$$
Summing $n$ numbers with a tree: $T_1 = n - 1$, $T_\infty = \lceil\log_2 n\rceil$; for $n = 2^{20}$ that is about a million additions in 20 rounds. **Speed-up** $S_p = T_1/T_p$; **efficiency** $= S_p/p$. The **PRAM** is the shared-memory model in which $p$ processors run in lock-step.

### Amdahl and Gustafson

If a fraction $s$ of the work is serial:
$$S_{\text{Amdahl}}(p) = \frac{1}{s + (1 - s)/p} \;\le\; \frac{1}{s}, \qquad S_{\text{Gustafson}}(p) = s + p(1 - s).$$
**Worked example.** $s = 0.05$, $p = 8$: Amdahl gives $1/(0.05 + 0.11875) = 5.93$, limit 20; Gustafson (the problem grows with $p$) gives $0.05 + 8 \times 0.95 = 7.65$. Amdahl describes **strong scaling** (fixed job), Gustafson **weak scaling** (bigger job on more workers), which is how large models are trained.

### Scan (prefix sum)

| Algorithm | Work | Span |
|---|---|---|
| Sequential | $n - 1$ | $n - 1$ |
| Hillis–Steele (inclusive) | $O(n \log n)$ | $\log_2 n$ |
| Blelloch (exclusive; up-sweep then down-sweep) | $O(n)$ (about $2(n-1)$) | $2\log_2 n$ |

Example: input [3, 1, 7, 0, 4, 1, 6, 3] → inclusive [3, 4, 11, 11, 15, 16, 22, 25], exclusive [0, 3, 4, 11, 11, 15, 16, 22]. Scan works for any **associative** operator, which is how stream compaction, radix sort and linear recurrences $h_t = a_t h_{t-1} + b_t$ (the selective scan in Mamba) are parallelised.

**Parallel sorting.** Parallel merge sort is limited by the merge step unless the merge is also parallel. **Sample sort** picks $p - 1$ splitters from a random sample, sends each element to its bucket, and sorts buckets independently. Real speed-ups are lower than the models predict because of process start-up, pickling (data copying between processes), memory bandwidth and load imbalance; **dynamic scheduling** and **longest-processing-time-first** fix uneven tasks, **chunking** fixes tiny ones.

### External memory and caches

In the **external-memory (I/O) model** (Aggarwal and Vitter, 1988), memory holds $M$ items and data moves in blocks of $B$ items; cost = number of block transfers. Scanning costs $\lceil N/B \rceil$. **External merge sort**: form $\lceil N/M \rceil$ sorted runs, then merge $k = M/B - 1$ runs at a time. I/Os:
$$\frac{2N}{B}\left(1 + \left\lceil \log_{M/B - 1} \frac{N}{M} \right\rceil\right).$$
**Worked example.** $N = 200{,}000$, $M = 10{,}000$, $B = 500$: 20 runs, fan-in 19, 2 merge passes, $2 \times 400 \times 3 = 2{,}400$ I/Os, which the notebook measured exactly. Binary merges would need 5 passes and 4,800 I/Os. The sorting lower bound is $\Theta\!\left(\frac{N}{B}\log_{M/B}\frac{N}{B}\right)$.

**Cache blocking.** Naive $ijk$ matrix multiply streams a column of $B$ with stride $n$, missing on almost every access; the $ikj$ order or $b \times b$ **tiles** that fit in cache reduce misses to $\Theta\!\left(\frac{n^3}{B\sqrt M}\right)$. **Cache-oblivious** algorithms (recursive halving) achieve this without knowing $M$ or $B$. FlashAttention applies the same tiling to keep attention blocks in on-chip GPU memory.

### Distributed

**MapReduce:** map emits (key, value) pairs, the framework **shuffles** by key, reduce aggregates each key. Costs are the shuffled volume and skew (one overloaded reducer). **Ring all-reduce:** $p$ workers in a ring do a reduce-scatter then an all-gather, each sending $2(p-1)N/p$ values for a length-$N$ vector, nearly independent of $p$, versus $(p - 1)N$ through a single root. PyTorch DDP and NCCL use it for gradient averaging.

---

## Complexity-Class Cheat Sheet

```
   harder
     ^
     |  EXP       solvable in exponential time       (e.g. generalised n x n chess)
     |  PSPACE    solvable in polynomial memory      (e.g. classical STRIPS planning, QBF)
     |  ---------------------------------------------------------------
     |  NP-hard        at least as hard as every NP problem; may lie outside NP
     |                 (halting problem, optimisation versions of TSP and ILP)
     |  NP-complete    NP-hard AND in NP (SAT, 3-SAT, clique, vertex cover,
     |                 Hamiltonian cycle, subset sum, 3-colouring, TSP decision)
     |  NP             yes-answers checkable in polynomial time
     |                 (also factoring and graph isomorphism, not known NP-complete)
     |  P              solvable in polynomial time
     |                 (sorting, shortest paths, max flow, matching, LP, 2-SAT, primality)
   easier

   Known:    P  is in  NP  is in  PSPACE  is in  EXP,   and  P != EXP.
   Open:     P = NP ?   NP = co-NP ?   P = PSPACE ?
   Picture above assumes P != NP (widely believed, unproven as of 2026).
```

| Class | Definition | Example problems | Notes |
|---|---|---|---|
| **P** | decision problems solvable in $O(n^c)$ time | sorting, shortest path, max flow, bipartite matching, LP, 2-SAT, primality (AKS 2002) | "tractable" |
| **NP** | yes-instances have poly-size certificates checkable in poly time | all of P; SAT; subset sum; factoring (decision) | $P \subseteq NP$ |
| **co-NP** | no-instances have poly-size certificates | TAUTOLOGY, UNSAT | factoring is in $NP \cap co\text{-}NP$ |
| **NP-hard** | every NP problem reduces to it | halting problem, TSP optimisation, ILP | need not be in NP |
| **NP-complete** | NP-hard and in NP | SAT, 3-SAT, vertex cover, clique, independent set, Hamiltonian cycle, 3-colouring, subset sum, partition, bin packing (decision) | a poly algorithm for one gives P = NP |
| **Weakly NP-hard** | NP-hard, but pseudo-polynomial algorithms exist | knapsack, subset sum, partition | $O(nW)$ DP |
| **Strongly NP-hard** | NP-hard even with numbers bounded by a polynomial in $n$ | TSP, bin packing, 3-partition | no pseudo-poly algorithm unless P = NP |
| **PSPACE** | polynomial memory | QBF, generalised geography, STRIPS planning | contains NP and co-NP |
| **EXP** | $2^{n^c}$ time | generalised $n \times n$ chess and Go (with suitable rules) | strictly contains P |
| **Undecidable** | no algorithm at all | halting problem | beyond every class above |
| **RP / co-RP** | poly-time randomized, one-sided error | polynomial identity testing (co-RP) | $RP \subseteq NP$ |
| **ZPP** | expected poly-time Las Vegas | $ZPP = RP \cap co\text{-}RP$ | |
| **BPP** | poly-time randomized, two-sided error $\le 1/3$ | everything in RP and co-RP (e.g. compositeness testing with Miller–Rabin is in RP) | believed to equal P |
| **FPT** | $f(k)\cdot n^{O(1)}$ time for parameter $k$ | vertex cover ($2^k n$), $k$-path | parameterized complexity |
| **FPTAS** | $(1 + \varepsilon)$-approx in poly$(n, 1/\varepsilon)$ | knapsack | strongly NP-hard problems (with polynomially bounded objective) have none unless P = NP |
| **PTAS** | $(1 + \varepsilon)$-approx in poly$(n)$ for each fixed $\varepsilon$ | Euclidean TSP (Arora 1998), makespan scheduling on identical machines | |
| **APX** | some constant-ratio approximation | vertex cover (2), metric TSP (1.5), k-center (2), max-cut (0.878) | APX-hard problems have no PTAS unless P = NP |
| **No constant ratio** | | general TSP; set cover ($\Theta(\log n)$); max clique ($n^{1-\varepsilon}$ hard) | |

**Reduction rules to remember.** If $A \le_p B$: $B \in P \Rightarrow A \in P$, and $A$ NP-hard $\Rightarrow B$ NP-hard. The reverse implications do not hold. Reductions compose (a polynomial of a polynomial is a polynomial).

**Algorithm-family bounds at a glance.**

| Algorithm | Bound |
|---|---|
| Dynamic array append | $O(1)$ amortized |
| Union-find ($m$ ops) | $O(m\,\alpha(n))$ |
| Randomized quicksort | $\approx 1.39\, n\log_2 n$ expected comparisons |
| Quickselect | $O(n)$ expected |
| Skip list / treap | $O(\log n)$ expected per op |
| Miller–Rabin ($k$ rounds) | error $\le 4^{-k}$ |
| Karger (one run) | success $\ge 2/(n(n-1))$ |
| DPLL / brute-force SAT | $O(2^n)$ worst case |
| Held–Karp TSP | $O(n^2 2^n)$ time, $O(n 2^n)$ space |
| Knapsack DP / FPTAS | $O(nW)$ / $O(n^3/\varepsilon)$ |
| FPT vertex cover | $O(2^k(n + m))$ |
| Edmonds–Karp / Dinic / Hopcroft–Karp / Hungarian | $O(VE^2)$ / $O(V^2E)$ / $O(E\sqrt V)$ / $O(n^3)$ |
| Simplex | exponential worst case, fast in practice; LP itself in P |
| Convex hull / Bentley–Ottmann | $O(n\log n)$ / $O((n + k)\log n)$ |
| FFT | $O(n\log n)$ |
| Suffix array (doubling) / Kasai LCP | $O(n\log^2 n)$ / $O(n)$ |
| Blelloch scan | $O(n)$ work, $O(\log n)$ span |
| External merge sort | $\frac{2N}{B}(1 + \lceil\log_{M/B-1}(N/M)\rceil)$ I/Os |
| Ring all-reduce | $2(p-1)N/p$ values sent per worker |

---

## Which Algorithm for Which Problem

| You need to... | Use | Guarantee / cost | Notebook | Library |
|---|---|---|---|---|
| keep merging groups and asking "same group?" | union-find (rank + path compression) | $O(\alpha(n))$ amortized | 01 | `scipy.cluster.hierarchy.DisjointSet` |
| find the $k$-th smallest / median | quickselect | $O(n)$ expected | 01 | `np.partition` |
| hash keys an adversary might choose | universal hashing | collision $\le 1/m$ per pair | 01 | |
| test whether a huge number is prime | Miller–Rabin | error $\le 4^{-k}$ | 01 | `sympy.isprime` |
| find a global min cut in an undirected graph | Stoer–Wagner (exact) or Karger (randomized) | $O(VE + V^2\log V)$ / repeated runs | 01, 04 | `networkx.stoer_wagner` |
| top singular vectors of a big matrix | randomized SVD | near-exact top-$k$, much faster | 01 | `sklearn.utils.extmath.randomized_svd` |
| decide satisfiability of Boolean constraints | CDCL SAT solver (DPLL + learning) | exponential worst case, fast in practice | 02 | PySAT, Kissat, Z3 |
| show a new problem is hard | reduce a known NP-complete problem to it | polynomial reduction | 02 | |
| small vertex cover | matching 2-approx; FPT $2^k$ if $k$ small; MILP if exact needed | ratio 2 / exact | 03, 05 | `networkx.algorithms.approximation` |
| cover all elements with few sets | greedy set cover | $\ln n$ ratio | 03 | |
| short tour through metric points | Christofides + 2-opt; Held–Karp if $n \le 20$ | 1.5 ratio / exact | 03 | `networkx.algorithms.approximation.christofides`, OR-Tools |
| pick $k$ diverse, relevant items | greedy on a monotone submodular objective | $1 - 1/e$ | 03 | |
| place $k$ centers minimising max distance | farthest-first traversal | ratio 2 | 03 | |
| knapsack with huge capacities | FPTAS (value scaling) or MILP | $(1 - \varepsilon)$ / exact | 03, 05 | `scipy.optimize.milp` |
| maximum throughput / bottleneck | max flow (Edmonds–Karp, Dinic, push–relabel) | exact, polynomial | 04 | `networkx.maximum_flow` |
| separate foreground from background with pairwise costs | s–t min cut (graph cut) | exact for binary labels | 04 | `networkx.minimum_cut`, PyMaxflow |
| pair up as many as possible | Hopcroft–Karp | $O(E\sqrt V)$ | 04 | `networkx.bipartite.maximum_matching` |
| pair up at minimum total cost | Hungarian algorithm | $O(n^3)$ | 04 | `scipy.optimize.linear_sum_assignment` |
| ship goods with supplies, demands and per-unit costs | min-cost flow / transportation LP | exact, integral | 04, 05 | `networkx.min_cost_flow` |
| best plan under linear limits, continuous amounts | LP (simplex or interior point) | exact, polynomial | 05 | `scipy.optimize.linprog(method="highs")` |
| best plan with yes/no or whole-number choices | MILP (branch-and-bound / cut) | exact, exponential worst case | 05 | `scipy.optimize.milp`, OR-Tools, PuLP |
| value of one more unit of a resource | LP dual / shadow prices | exact within the sensitivity range | 05 | `linprog` result `.ineqlin.marginals` |
| uniform sample from a stream of unknown length | reservoir sampling | exact uniformity, $O(k)$ memory | 06 | |
| most frequent items in a stream | Space-Saving / Misra–Gries | error $\le N/k$ | 06 | |
| approximate frequency of any item | Count-Min | $+\varepsilon N$ w.p. $1 - \delta$ | 06 | |
| count distinct items | HyperLogLog | $\approx 1.04/\sqrt m$ | 06 | Redis `PFCOUNT`, `approx_count_distinct` |
| find near-duplicate documents | MinHash + LSH banding | tunable S-curve threshold | 06 | `datasketch` |
| streaming p95/p99 | DDSketch / KLL | relative-value or rank error | 06 | DuckDB `approx_quantile` |
| smallest enclosing convex polygon | Andrew's monotone chain | $O(n\log n)$ | 07 | `scipy.spatial.ConvexHull` |
| is this point inside this region? | ray casting | $O(n)$ per query | 07 | `matplotlib.path.Path.contains_points`, shapely |
| nearest site regions / triangulate points | Voronoi / Delaunay | $O(n\log n)$ | 07 | `scipy.spatial.Voronoi`, `Delaunay` |
| multiply long polynomials, big integers, convolve | FFT + convolution theorem | $O(n\log n)$ | 07 | `np.fft`, `scipy.signal.fftconvolve` |
| range minimum on static data | sparse table | $O(1)$ query | 08 | |
| substring search, repeats, distinct substrings in a big text | suffix array + LCP | $O(m\log n)$ search | 08 | |
| all intervals overlapping a query | interval tree | $O(\log n + k)$ | 08 | `intervaltree` |
| nearest neighbour in 2–10 dimensions | KD-tree / ball tree | fast in low $d$ | 08 | `sklearn.neighbors.KDTree` |
| nearest neighbour for embeddings (hundreds of dims) | approximate index (HNSW, IVF) | approximate | 08 | FAISS, vector databases |
| ordered map with guaranteed $O(\log n)$ | red-black / LLRB tree | height $\le 2\log_2(n+1)$ | 08 | `sortedcontainers` |
| keep every past version cheaply | persistent structure (path copying) | $O(\log n)$ per update | 08 | `pyrsistent` |
| very write-heavy key-value storage | LSM tree | sequential writes, compaction | 08 | RocksDB |
| sum or prefix-sum on many cores / GPU | tree reduction, Blelloch scan | $O(n)$ work, $O(\log n)$ span | 10 | `torch.cumsum` |
| sort data larger than RAM | external merge sort with large fan-in | $\frac{2N}{B}(1 + \lceil\log_{M/B-1}\frac{N}{M}\rceil)$ I/Os | 10 | DuckDB, Spark |
| fast dense matrix multiply | blocked / cache-aware loops | fewer cache misses | 10 | NumPy (BLAS) |
| average gradients across GPUs | ring all-reduce | $2(p-1)N/p$ per worker | 10 | PyTorch DDP, NCCL |

---

## Glossary

- **Amortized cost**: total cost of a worst-case sequence of operations divided by its length; no probability involved.
- **Potential function**: a non-negative "stored energy" $\Phi$ of a data structure used to prove amortized bounds.
- **Inverse Ackermann α(n)**: an extremely slowly growing function, at most 4 for any practical $n$.
- **Las Vegas algorithm**: randomized, always correct, random running time.
- **Monte Carlo algorithm**: randomized, bounded running time, small probability of a wrong answer.
- **Amplification**: repeating a randomized algorithm to shrink its error probability exponentially.
- **Universal hash family**: a set of hash functions where a random member makes any two keys collide with probability at most $1/m$.
- **Skip list**: a sorted linked list with randomly promoted express levels; $O(\log n)$ expected operations.
- **Treap**: a BST by key that is also a heap by random priority.
- **Decision problem**: a problem with a yes/no answer.
- **Certificate / verifier**: a short proof of a yes-answer and the polynomial-time algorithm that checks it.
- **P / NP / co-NP**: solvable in polynomial time / yes-answers checkable in polynomial time / no-answers checkable in polynomial time.
- **Reduction ($A \le_p B$)**: a polynomial-time, answer-preserving transformation from instances of $A$ to instances of $B$.
- **NP-hard / NP-complete**: at least as hard as every NP problem / NP-hard and in NP.
- **Cook–Levin theorem**: SAT is NP-complete.
- **DPLL / CDCL**: backtracking SAT algorithm with unit propagation / its modern clause-learning version.
- **Phase transition (3-SAT)**: the sharp change from mostly satisfiable to mostly unsatisfiable near 4.26 clauses per variable.
- **Pseudo-polynomial**: polynomial in the numeric value of the input, exponential in its bit length.
- **Approximation ratio**: the worst-case factor between an algorithm's answer and the optimum.
- **PTAS / FPTAS**: a family of $(1 + \varepsilon)$-approximations polynomial in $n$ / in both $n$ and $1/\varepsilon$.
- **APX**: problems with some constant-ratio polynomial approximation.
- **Fixed-parameter tractable (FPT)**: solvable in $f(k)\cdot n^{O(1)}$ for a parameter $k$.
- **Kernelization**: polynomial preprocessing that shrinks an instance to a size depending only on $k$.
- **Submodular function**: a set function with diminishing marginal returns.
- **Flow network**: a directed graph with capacities, a source and a sink.
- **Residual graph**: the graph of remaining forward capacity and undoable backward flow.
- **Augmenting path**: a source-to-sink path in the residual graph.
- **Cut (s–t)**: a split of vertices separating source from sink; its capacity is the total capacity crossing it.
- **Max-flow min-cut theorem**: the maximum flow value equals the minimum cut capacity.
- **Hall's theorem**: a bipartite graph saturates side $L$ iff every subset $X$ of $L$ has at least $|X|$ neighbours.
- **Hungarian algorithm**: $O(n^3)$ algorithm for minimum-cost assignment.
- **Min-cost flow**: sending required flow at minimum total per-unit cost.
- **Linear program (LP)**: optimising a linear objective under linear constraints with continuous variables.
- **ILP / MILP**: (mixed) integer linear program; some variables must be integers.
- **Polytope / vertex / basic feasible solution**: the feasible region of an LP / its corner / the algebraic form of a corner.
- **Simplex method**: walks from vertex to better adjacent vertex.
- **Reduced cost / ratio test**: objective change per unit of a non-basic variable / how far a pivot can move before a basic variable hits zero.
- **Degeneracy / cycling / Bland's rule**: zero-valued basic variables / the simplex repeating bases forever / the smallest-index rule that prevents it.
- **Duality / shadow price**: every LP has a paired dual LP with the same optimum / the optimal dual value of a constraint.
- **LP relaxation / integrality gap**: the LP obtained by dropping integrality / the difference between its bound and the integer optimum.
- **Branch-and-bound**: splitting on fractional variables and pruning branches whose bound cannot beat the incumbent.
- **Big-M**: a large constant times a binary variable that switches a constraint on or off.
- **IIS**: an irreducible infeasible subset of constraints.
- **Totally unimodular**: a constraint matrix whose LPs have integral vertices.
- **Streaming model**: one pass over the data, sublinear memory.
- **Sketch / mergeable**: a small summary of a stream / combinable from per-shard summaries.
- **$(\varepsilon, \delta)$ guarantee**: error at most $\varepsilon$ with probability at least $1 - \delta$.
- **Reservoir sampling**: uniform sampling of $k$ items from a stream of unknown length.
- **Misra–Gries / Space-Saving**: counter-based heavy-hitter algorithms that under- / over-count.
- **Count-Min sketch**: a $d \times w$ counter array answering frequency queries with one-sided error.
- **HyperLogLog**: a distinct-count sketch based on leading zeros of hashes.
- **Jaccard similarity**: $|A \cap B| / |A \cup B|$.
- **MinHash / LSH banding**: Jaccard estimation by minimum hash values / grouping signatures into bands to find likely-similar pairs.
- **KLL / DDSketch**: quantile sketches with rank error / relative-value error.
- **DGIM**: exponential-histogram counting of recent events in a sliding window.
- **Orientation test**: the sign of a 2-D cross product; left turn, right turn or collinear.
- **Convex hull**: the smallest convex polygon containing all points.
- **Sweep line**: processing geometric events in sorted order while maintaining an active set.
- **Shoelace formula**: polygon area from vertex coordinates.
- **Voronoi diagram / Delaunay triangulation**: nearest-site regions / their dual triangulation with empty circumcircles.
- **Roots of unity**: complex numbers $\omega$ with $\omega^n = 1$, the FFT's evaluation points.
- **FFT (Cooley–Tukey)**: $O(n\log n)$ divide-and-conquer DFT.
- **Convolution theorem**: the Fourier transform turns convolution into pointwise multiplication.
- **Sparse table / sqrt decomposition**: $O(1)$ static range queries / $O(\sqrt n)$ blocks for queries with updates.
- **Suffix array / LCP array**: sorted suffix start positions / longest common prefix of neighbouring suffixes.
- **Interval tree**: a BST of intervals augmented with subtree maximum end points.
- **KD-tree**: a binary space partition alternating split axes.
- **Curse of dimensionality**: in high dimensions distances concentrate and space-partitioning pruning fails.
- **Red-black / LLRB tree**: balanced BST equivalent to a 2-3-4 tree / its left-leaning 2-3 variant.
- **Persistent data structure / path copying**: every version remains accessible / copying only the nodes on the modified path.
- **LSM tree / memtable / SSTable / compaction**: write-optimised store / in-memory buffer / immutable sorted file / merging files.
- **Write amplification**: bytes written to storage per byte of user data.
- **Gap buffer / rope**: an array with a movable gap at the cursor / a balanced tree of string pieces.
- **Test oracle**: a slow, obviously correct solution used to check a fast one.
- **Work / span / parallelism**: total operations / longest dependent chain / their ratio.
- **PRAM**: idealised shared-memory parallel machine running in lock-step.
- **Brent's theorem**: a greedy scheduler achieves $T_p \le T_1/p + T_\infty$.
- **Amdahl's law / Gustafson's law**: speed-up limit from the serial fraction / scaled speed-up when the job grows with $p$.
- **Strong vs weak scaling**: fixed problem size / problem size growing with workers.
- **Scan (prefix sum)**: all running totals of an associative operation; Hillis–Steele and Blelloch are parallel versions.
- **Stream compaction**: keeping only selected elements, computed with a scan.
- **Sample sort**: parallel sort by splitter-defined buckets.
- **Static vs dynamic scheduling / LPT**: fixed chunks per worker / workers pull tasks as they finish / longest tasks first.
- **External-memory model ($M$, $B$)**: cost counted in block transfers between a memory of $M$ items and disk in blocks of $B$.
- **Fan-in**: the number of runs merged at once in external merge sort.
- **Cache-aware / cache-oblivious**: tuned to known cache sizes / efficient for all cache sizes via recursion.
- **MapReduce / shuffle / skew**: map, group by key, reduce / the grouping step / uneven load across reducers.
- **Ring all-reduce**: bandwidth-optimal reduce-scatter plus all-gather around a ring of workers.
