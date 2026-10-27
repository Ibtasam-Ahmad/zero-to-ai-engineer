# Discrete Mathematics & Theory of Computation

Discrete mathematics studies objects you can count one at a time: elements of a set, edges of a graph, characters of a string, steps of a program. This guide walks through the whole `discrete_math/` folder in order. Part I (notebooks 01–03) is the *Discrete Structures* course: sets, relations, functions, proofs, counting, recurrences and graphs. Part II (notebooks 04–05) is the *Theory of Automata / Theory of Computation* course: finite automata, regular expressions, grammars, parsing, Turing machines and the limits of what any computer can do. Every section gives definitions, the intuition, a worked example by hand, the key formulas, and a note on why it matters for AI work.

```
 Part I: Discrete Structures              Part II: Theory of Computation
 ┌──────────────────────────────┐         ┌──────────────────────────────┐
 │ 01 sets, relations, proofs   │         │ 04 DFA, NFA, regex           │
 │ 02 counting, recurrences     │ ──────> │ 05 CFG, PDA, Turing machines │
 │ 03 graphs                    │         │    halting problem           │
 └──────────────────────────────┘         └──────────────────────────────┘
```

---

## Part I. Discrete Structures

## 1. Sets

A **set** is an unordered collection of distinct objects called **elements**. We write $x \in A$ for "x is an element of A". Order and repeats do not matter: $\{1, 2, 2\} = \{2, 1\}$. Sets are written by listing (roster notation, $A = \{1, 2, 3, 4\}$) or by a rule (set-builder notation, $E = \{x \in \mathbb{Z} \mid 0 \le x \le 10,\ x \text{ even}\}$). The **empty set** $\varnothing$ has no elements; the **universal set** $U$ is everything under discussion; the **cardinality** $|A|$ is the number of elements.

$A \subseteq B$ (**subset**) means every element of A is in B. Two sets are equal exactly when $A \subseteq B$ and $B \subseteq A$, which is also how you prove two sets are equal ("element chasing": take an arbitrary $x$ in one side and show it is in the other).

| Operation | Symbol | Meaning | Python |
|---|---|---|---|
| Union | $A \cup B$ | in A or B | `A \| B` |
| Intersection | $A \cap B$ | in both | `A & B` |
| Difference | $A \setminus B$ | in A but not B | `A - B` |
| Symmetric difference | $A \oplus B$ | in exactly one | `A ^ B` |
| Complement | $\overline{A}$ | $U \setminus A$ | `U - A` |

The laws you must know are commutativity, associativity, distributivity, absorption ($A \cup (A \cap B) = A$) and **De Morgan's laws**: $\overline{A \cup B} = \overline{A} \cap \overline{B}$ and $\overline{A \cap B} = \overline{A} \cup \overline{B}$. Set difference is *not* associative: with $A = \{1\}, B = \varnothing, C = \{1\}$, $A - (B - C) = \{1\}$ but $(A - B) - C = \varnothing$. One counterexample is enough to kill a "for all" claim.

The **power set** $\mathcal{P}(A)$ is the set of all subsets of A. If $|A| = n$ then $|\mathcal{P}(A)| = 2^n$, because each element is independently in or out. That "in or out" view is the **bitmask** trick: the integers $0 \dots 2^n - 1$ in binary list every subset. The **Cartesian product** $A \times B = \{(a, b) \mid a \in A, b \in B\}$ is the set of ordered pairs, and $|A \times B| = |A|\,|B|$. A menu with 3 mains and 2 drinks gives $3 \times 2 = 6$ meals.

**Why it matters.** Retrieval precision is $|\text{retrieved} \cap \text{relevant}| / |\text{retrieved}|$ and recall is $|\text{retrieved} \cap \text{relevant}| / |\text{relevant}|$. With 4 retrieved documents, 3 relevant ones and 2 in common, precision is 0.50 and recall 0.67. **Jaccard similarity** $|A \cap B| / |A \cup B|$ is the basis of near-duplicate detection (MinHash). A database table is a subset of the Cartesian product of its column domains.

## 2. Relations

A **binary relation** R from A to B is any subset $R \subseteq A \times B$; we write $a\,R\,b$ for $(a, b) \in R$. A relation on a finite set can be stored as a set of pairs, as a Boolean matrix ($M_{ij} = 1$ iff $i\,R\,j$), or as a directed graph. There are $2^{n^2}$ relations on an n-element set (each of the $n^2$ pairs is in or out).

| Property | Definition | Matrix / graph view |
|---|---|---|
| Reflexive | $\forall a:\ a\,R\,a$ | diagonal all 1; a loop at every node |
| Irreflexive | no $a\,R\,a$ | diagonal all 0 |
| Symmetric | $a\,R\,b \Rightarrow b\,R\,a$ | $M = M^T$; every arrow has a return arrow |
| Antisymmetric | $a\,R\,b \wedge b\,R\,a \Rightarrow a = b$ | no two-way arrows between distinct nodes |
| Transitive | $a\,R\,b \wedge b\,R\,c \Rightarrow a\,R\,c$ | every 2-step path has a shortcut |

Antisymmetric is not "not symmetric": equality is both, and $\{(1,2),(2,1),(1,3)\}$ is neither. A "close to" relation (|x − y| ≤ 1) is reflexive and symmetric but not transitive, which is exactly the trap in similarity-based deduplication: chaining "similar" pairs can merge very different records.

### Equivalence relations and partitions

An **equivalence relation** is reflexive, symmetric and transitive. The **equivalence class** of a is $[a] = \{x \mid x\,R\,a\}$. A **partition** of A is a collection of non-empty, pairwise disjoint blocks whose union is A. The fundamental theorem says equivalence relations and partitions are the same thing: classes are never partly overlapping (if $x$ is in $[a]$ and $[b]$, symmetry and transitivity give $a\,R\,b$, so the classes are equal). Worked example: congruence mod 3 on $\{1, \dots, 10\}$ has classes $\{3, 6, 9\}$, $\{1, 4, 7, 10\}$ and $\{2, 5, 8\}$. The number of equivalence relations on an n-set is the **Bell number** $B_n$ (1, 1, 2, 5, 15, 52, 203, 877, ...); brute force over all 65,536 relations on 4 elements finds exactly 15.

**Why it matters.** Entity resolution ("these records are the same customer") must be an equivalence relation, so pairwise match decisions are closed transitively with **union-find** into clusters.

### Partial orders and topological order

A **partial order** ⪯ is reflexive, antisymmetric and transitive; the pair $(A, \preceq)$ is a **poset**. Elements may be incomparable (neither 4 nor 6 divides the other). A **total order** makes every pair comparable. A **Hasse diagram** draws only the **covering** pairs (b covers a if $a \prec b$ with nothing in between), with larger elements higher; loops and transitive shortcuts are implied. For the 12 divisors of 60 under "divides" there are 42 strict pairs but only 20 covering edges. In this poset the greatest lower bound of two elements is their gcd and the least upper bound is their lcm, so it is a **lattice**.

A **linear extension** (for a DAG, a **topological order**) is a total order consistent with the partial order. Every finite poset has one: repeatedly remove a minimal element. That proof is **Kahn's algorithm**, which runs in $O(V + E)$ with a queue of tasks whose in-degree has reached zero; if some tasks never reach in-degree zero, there is a cycle and no order exists. Counting *all* linear extensions is #P-complete in general.

**Why it matters.** Airflow, Kubeflow and Prefect run pipeline DAGs in topological order, and `loss.backward()` walks the computation graph in reverse topological order.

### Closures and Warshall's algorithm

The **closure** of R under a property is the smallest relation containing R with that property. Reflexive closure adds the diagonal, symmetric closure adds $R^{-1}$, and the **transitive closure** is $R^+ = R \cup R^2 \cup R^3 \cup \dots$ ("reachable in one or more steps"). **Warshall's algorithm** computes it by dynamic programming over allowed intermediate nodes:

$$W^{(k)}[i][j] = W^{(k-1)}[i][j] \lor \big(W^{(k-1)}[i][k] \land W^{(k-1)}[k][j]\big)$$

Three nested loops give $\Theta(n^3)$ time and $\Theta(n^2)$ space; doubling n multiplies the work by 8. It is Floyd–Warshall shortest paths with "or/and" in place of "min/+". For sparse graphs, a BFS from every node, $O(n(n + |E|))$, is faster. The reflexive-transitive closure $R^*$ is the same star that appears in regular expressions.

## 3. Functions and countability

A **function** $f: A \to B$ is a relation in which every $a \in A$ has **exactly one** partner $f(a)$. A is the **domain**, B the **codomain**, and $f(A)$ the **range** (image). A phone book that lists two numbers for one person is not a function.

| Kind | Definition | Finite-set consequence |
|---|---|---|
| Injective (one-to-one) | $f(a_1) = f(a_2) \Rightarrow a_1 = a_2$ | $\lvert A\rvert \le \lvert B\rvert$ |
| Surjective (onto) | every $b$ is hit | $\lvert A\rvert \ge \lvert B\rvert$ |
| Bijective | both | $\lvert A\rvert = \lvert B\rvert$; has an inverse |

Composition $(g \circ f)(a) = g(f(a))$ applies f first. A function has an inverse iff it is bijective. Composites of injections are injective, and of surjections are surjective. Whether a function is onto depends on the declared codomain: $x \mapsto x^2$ is not onto ℝ but is onto $[0, \infty)$.

**Counting functions** from an m-set to an n-set: $n^m$ functions, $n!/(n-m)!$ injections, $n!$ bijections when $m = n$. For 4 inputs into 3 outputs there are $3^4 = 81$ functions and no injections, which is the **pigeonhole principle**.

**Countability.** Two sets have the same cardinality if a bijection exists between them. A set is **countable** if it is finite or can be listed $a_0, a_1, a_2, \dots$. ℤ is countable (0, 1, −1, 2, −2, ...). $\mathbb{N} \times \mathbb{N}$ is countable via the Cantor pairing function $\pi(x, y) = \frac{(x+y)(x+y+1)}{2} + y$, so ℚ is countable. ℝ is **uncountable**: given any claimed list of infinite binary sequences, flip the diagonal (bit i of the new sequence is the opposite of bit i of sequence i), and the result differs from every row. The same trick proves **Cantor's theorem** $|A| < |\mathcal{P}(A)|$ for every set: the set $D = \{x \mid x \notin f(x)\}$ is never in the range of any $f: A \to \mathcal{P}(A)$.

**Why it matters.** Programs are finite strings over a finite alphabet, so there are countably many programs, but there are uncountably many functions $\mathbb{N} \to \{0, 1\}$. Most functions are therefore not computable by any program, and the same diagonal idea proves the halting problem undecidable (Section 11).

## 4. Logic recap and proof techniques

Quantifiers: $\forall x\,P(x)$ ("for all", Python `all`) and $\exists x\,P(x)$ ("there exists", `any`). Negation swaps them: $\lnot\forall x\,P(x) \equiv \exists x\,\lnot P(x)$. Order matters: $\forall x\,\exists y\ (x + y \equiv 0 \bmod 5)$ is true (each x has its own inverse), but $\exists y\,\forall x\ (x + y \equiv 0 \bmod 5)$ is false (no single y works for all x).

A **proof** is a chain of valid steps from definitions, axioms and earlier theorems to the claim.

| Technique | Structure | Typical use |
|---|---|---|
| Direct | assume P, derive Q | algebraic facts |
| Contrapositive | prove $\lnot Q \Rightarrow \lnot P$ | "if $n^2$ is even then n is even" |
| Contradiction | assume P and $\lnot Q$, derive a falsehood | $\sqrt{2}$ irrational, infinitely many primes |
| Cases | split into exhaustive cases | parity, remainders |
| Counterexample | one x where the claim fails | disproving "for all" |
| Induction | base case + step | statements about every $n \ge n_0$ |

*Worked direct proof.* If $a = 2j + 1$ and $b = 2k + 1$ are odd, then $a + b = 2(j + k + 1)$ is even. ∎

*Warning by example.* $n^2 + n + 41$ is prime for $n = 0, \dots, 39$, but at $n = 40$ it equals $1681 = 41^2$. Forty passing tests did not prove the claim.

## 5. Induction and loop invariants

**Ordinary induction** proves $P(n)$ for all $n \ge n_0$ from (1) the **base case** $P(n_0)$ and (2) the **inductive step**: for arbitrary $k \ge n_0$, the **inductive hypothesis** $P(k)$ implies $P(k+1)$. It is valid because of the **well-ordering principle** (every non-empty set of naturals has a least element, so a smallest counterexample would contradict the step).

*Worked example (Gauss).* $1 + \dots + n = n(n+1)/2$. Base: $1 = 1 \cdot 2/2$. Step: $\frac{k(k+1)}{2} + (k+1) = \frac{(k+1)(k+2)}{2}$. ∎ Similarly $\sum_{i=0}^{n} 2^i = 2^{n+1} - 1$ (the number of nodes in a full binary tree of height n), and $2^n > n^2$ for $n \ge 5$ (the base case is 5, because the claim fails at 2, 3 and 4).

**Strong induction** lets the step assume $P(n_0), \dots, P(k)$. It suits problems that split into smaller pieces. Every integer $n \ge 2$ is a product of primes (if $k+1 = ab$ is composite, both factors are smaller). Every amount $n \ge 12$ cents can be paid with 4- and 5-cent stamps: four base cases (12, 13, 14, 15), then add a 4-cent stamp to the solution for $k - 3$. A constructive proof is a recursive algorithm.

The classic fallacy "all horses are the same colour" fails because the step from 1 to 2 horses has no overlap. Always test the step on the first transition.

**Loop invariants** (CLRS chapter 2) apply induction to loops:

| Step | Meaning | Induction analogue |
|---|---|---|
| Initialization | true before the first iteration | base case |
| Maintenance | stays true after each iteration | inductive step |
| Termination | invariant + exit condition gives the result | conclusion |

A **variant** (a natural number that strictly decreases each iteration) proves the loop ends. Insertion sort keeps "the prefix `a[0..j-1]` is the original first j elements, sorted". Euclid's algorithm keeps $\gcd(a, b)$ unchanged, using $\gcd(a, b) = \gcd(b, a \bmod b)$, and b strictly decreases; for example $\gcd(1071, 462) = 21$. Binary search keeps "if the target is present, it is in `a[lo..hi]`", with variant `hi − lo`.

## 6. Counting

**The four basic rules.**

| Rule | Statement | Example |
|---|---|---|
| Sum | disjoint "or": $n_1 + n_2$ | 12 projects in list A or 7 in list B: 19 |
| Product | "and then": $n_1 \cdot n_2$ | 3 breads × 4 fillings × 2 sauces = 24 |
| Subtraction | $\lvert A \cup B\rvert = \lvert A\rvert + \lvert B\rvert - \lvert A \cap B\rvert$ | 8-bit strings starting with 1 or ending 00: 128 + 64 − 32 = 160 |
| Division | each outcome counted d times: divide by d | 5 people round a table: 5!/5 = 24 |

**Choosing r from n.** Ask whether order matters and whether repetition is allowed.

| | Order matters | Order does not matter |
|---|---|---|
| Repetition allowed | $n^r$ (PINs: $10^4$) | $\binom{n+r-1}{r}$ (3 scoops from 4 flavours: $\binom{6}{3} = 20$) |
| No repetition | $P(n, r) = \frac{n!}{(n-r)!}$ (podium of 3 from 8: 336) | $\binom{n}{r} = \frac{n!}{r!(n-r)!}$ (committee of 3 from 8: 56) |

The "with repetition, unordered" case is **stars and bars**: r stars separated into n groups by $n - 1$ bars. Arrangements of a word with repeated letters are **multinomial** coefficients $\frac{n!}{n_1! \cdots n_k!}$ (MISSISSIPPI: $\frac{11!}{1!\,4!\,4!\,2!} = 34{,}650$).

**Binomial theorem.** $(x + y)^n = \sum_{k=0}^{n} \binom{n}{k} x^k y^{n-k}$. **Pascal's rule** $\binom{n}{k} = \binom{n-1}{k-1} + \binom{n-1}{k}$ (a subset either contains a given item or does not) builds Pascal's triangle. Row sums are $2^n$; **Vandermonde's identity** $\sum_k \binom{m}{k}\binom{n}{r-k} = \binom{m+n}{r}$; the **hockey stick** $\sum_{i=r}^{n} \binom{i}{r} = \binom{n+1}{r+1}$. A **double-counting proof** counts one set two ways: choosing a committee of 3 with a chair from 8 people gives $8\binom{7}{2} = 3\binom{8}{3} = 168$.

**Pigeonhole principle.** N objects in k boxes force a box with at least $\lceil N/k \rceil$. 100 people include at least $\lceil 100/12 \rceil = 9$ sharing a birth month. A hash function into m buckets cannot be injective once there are more than m keys, and no lossless compressor can shorten every n-bit file (there are $2^n$ such files but only $2^n - 1$ shorter ones).

**Birthday paradox.** The chance that n people with $m$ equally likely birthdays are all different is

$$P(\text{no match}) = \prod_{i=0}^{n-1}\left(1 - \frac{i}{m}\right) \approx e^{-n(n-1)/(2m)}$$

so the 50% point is at $n \approx \sqrt{2 \ln 2 \cdot m} \approx 1.18\sqrt{m}$. For $m = 365$ that is 23 people (probability 0.5073); 57 people give 99%. With a 20-bit hash ($m \approx 10^6$) collisions show up after about 1,280 keys, which is why 32-bit IDs are unsafe for large datasets and cryptographic hashes use 256 bits.

**Inclusion–exclusion.** $\left|\bigcup A_i\right| = \sum|A_i| - \sum|A_i \cap A_j| + \sum|A_i \cap A_j \cap A_k| - \dots$. Integers from 1 to 10,000 divisible by none of 2, 3, 5, 7: 2,285. **Derangements** (permutations with no fixed point, the hat-check problem): $D_n = n! \sum_{k=0}^{n} \frac{(-1)^k}{k!}$, the nearest integer to $n!/e$; $D_4 = 9$, and the fraction $D_n / n!$ tends to $1/e \approx 0.3679$. **Surjections** from an m-set onto an n-set: $\sum_{k=0}^{n} (-1)^k \binom{n}{k} (n-k)^m = n!\,S(m, n)$; for $m = 4, n = 3$: $81 - 48 + 3 = 36$.

## 7. Recurrences and generating functions

A **recurrence relation** defines $a_n$ from earlier terms; with enough initial conditions it fixes the sequence (by strong induction). Classic models: Tower of Hanoi $H_n = 2H_{n-1} + 1$; bit strings with no two consecutive 1s $a_n = a_{n-1} + a_{n-2}$ (a string ends in 0 or in 01); compound interest $B_n = (1 + r)B_{n-1}$.

**Characteristic-root method** for linear homogeneous recurrences with constant coefficients, $a_n = c_1 a_{n-1} + \dots + c_k a_{n-k}$: try $a_n = r^n$ to get $r^k - c_1 r^{k-1} - \dots - c_k = 0$.

- Distinct roots: $a_n = \alpha_1 r_1^n + \dots + \alpha_k r_k^n$.
- A root of multiplicity m contributes $(\alpha_0 + \alpha_1 n + \dots + \alpha_{m-1} n^{m-1}) r^n$.
- Fit the $\alpha$'s to the initial conditions.

*Worked example 1.* $a_n = 5a_{n-1} - 6a_{n-2}$, $a_0 = 2$, $a_1 = 5$. Roots 2 and 3, so $a_n = \alpha 2^n + \beta 3^n$; the initial conditions give $\alpha = \beta = 1$: $a_n = 2^n + 3^n$ (2, 5, 13, 35, 97, ...).

*Worked example 2 (Fibonacci).* $r^2 - r - 1 = 0$ gives $\varphi = \frac{1 + \sqrt5}{2}$ and $\psi = \frac{1 - \sqrt5}{2}$, so **Binet's formula** is $F_n = \frac{\varphi^n - \psi^n}{\sqrt5}$. Fibonacci numbers grow like $1.618^n$, which is why naive recursive Fibonacci is exponential.

*Worked example 3 (repeated root).* $a_n = 6a_{n-1} - 9a_{n-2}$, $a_0 = 1$, $a_1 = 6$: root 3 twice, so $a_n = (1 + n)3^n$.

**Non-homogeneous** recurrences add one particular solution: for Hanoi, a constant $p = 2p + 1$ gives $p = -1$, so $H_n = 2^n - 1$ (64 discs: about $1.8 \times 10^{19}$ moves).

**Matrix powers.** A linear recurrence is a matrix step: $\begin{pmatrix}1&1\\1&0\end{pmatrix}^n = \begin{pmatrix}F_{n+1}&F_n\\F_n&F_{n-1}\end{pmatrix}$. Repeated squaring needs $O(\log n)$ multiplications and stays exact, while floating-point Binet fails from about $n = 71$.

| Recurrence family | Example | Tool | Answer |
|---|---|---|---|
| Linear, constant coefficients | $F_n = F_{n-1} + F_{n-2}$ | characteristic roots | $\Theta(\varphi^n)$ |
| Divide and conquer | $T(n) = 2T(n/2) + n$ | Master theorem ([`dsa/01`](../../../00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb)) | $\Theta(n \log n)$ |

**Generating functions.** Store a sequence as the coefficients of $G(x) = \sum_{n \ge 0} a_n x^n$. Multiplying generating functions convolves coefficients, which is the product rule summed over every way to split a total. One die is $x + x^2 + \dots + x^6$; in $(x + \dots + x^6)^2$ the coefficient of $x^7$ is 6, so $P(\text{sum} = 7) = 6/36$. Ways to pay n cents with coins 1, 5, 10, 25 are the coefficients of $\frac{1}{(1-x)(1-x^5)(1-x^{10})(1-x^{25})}$; for a dollar there are 242. This is exactly the coin-change DP. A recurrence becomes a rational function: the Fibonacci generating function is $\frac{x}{1 - x - x^2}$.

**Special numbers.**

| Numbers | Formula / recurrence | Counts | First values |
|---|---|---|---|
| Catalan $C_n$ | $\frac{1}{n+1}\binom{2n}{n}$ | binary trees with n nodes, balanced strings of n bracket pairs, bracketings, binary parse trees | 1, 1, 2, 5, 14, 42 |
| Stirling 2nd kind $S(n,k)$ | $kS(n-1,k) + S(n-1,k-1)$ | partitions of n items into k non-empty blocks | $S(4,2) = 7$ |
| Bell $B_n$ | $\sum_k S(n,k)$ | all partitions of n items | 1, 1, 2, 5, 15, 52, 203 |
| Stirling 1st kind $c(n,k)$ | $(n-1)c(n-1,k) + c(n-1,k-1)$ | permutations of n with k cycles | $c(4,2) = 11$ |

**Why it matters: combinatorial explosion.** Five hyperparameters with 4, 5, 3, 6 and 10 values give 3,600 training runs. Feature subsets of 30 features number $2^{30} - 1 \approx 10^9$. An LLM with vocabulary 50,000 has $50{,}000^{20} \approx 10^{94}$ possible 20-token outputs, more than the roughly $10^{80}$ atoms in the observable universe. There are $S(100, 5) \approx 6.6 \times 10^{67}$ ways to put 100 points into 5 clusters, and a 20-word sentence has $C_{19} = 1{,}767{,}263{,}190$ binary bracketings. Hence random search, greedy selection, beam search, local search (k-means) and dynamic programming (CYK) instead of enumeration.

## 8. Graph theory

A **graph** $G = (V, E)$ has vertices and edges. The **degree** of a vertex is the number of edges touching it. **Handshake lemma**: $\sum_v \deg(v) = 2|E|$, so the number of odd-degree vertices is even. The **Havel–Hakimi** algorithm decides whether a degree sequence is possible: (5, 4, 3, 2, 2, 1) has odd sum, so no; (4, 4, 4, 4, 2) has even sum but reduces to a negative entry, so no.

**Walks and connectivity.** With adjacency matrix A, $(A^k)_{ij}$ counts walks of length k from i to j, and $\operatorname{tr}(A^3)/6$ counts triangles. A **bridge** is an edge whose removal disconnects the graph; a **cut vertex** is the same for vertices (Tarjan's DFS finds all of them in linear time).

**Bipartite graphs** split V into two sides with every edge crossing between them (users and items, students and courses). **König (1936):** a graph is bipartite iff it has no odd cycle; BFS 2-colouring either finds the sides or returns an odd cycle.

**Isomorphism.** $G \cong H$ if a bijection of vertices preserves edges exactly. Invariants (degree sequence, triangle count) can only *disprove* isomorphism: $C_6$ and two disjoint triangles have the same degrees but are not isomorphic. The 64 labelled graphs on 4 vertices are only 11 different shapes. The problem has a quasi-polynomial algorithm (Babai, 2015); the Weisfeiler–Lehman test bounds what message-passing GNNs can distinguish.

**Trees.** For a graph with n vertices these are equivalent: connected and acyclic; connected with $n - 1$ edges; acyclic with $n - 1$ edges; exactly one path between every pair; minimally connected; maximally acyclic. Every tree with $n \ge 2$ has at least two leaves (the ends of a longest path). **Cayley's formula**: there are $n^{n-2}$ labelled trees on n vertices (16 for n = 4), proved by the Prüfer-code bijection, in which a vertex appears exactly $\deg - 1$ times. **Kirchhoff's matrix-tree theorem**: the number of spanning trees equals any cofactor of the Laplacian $L = D - A$.

**Euler versus Hamilton.**

| | Euler circuit | Hamiltonian cycle |
|---|---|---|
| Uses every... | edge exactly once | vertex exactly once |
| Exact test | connected and all degrees even (Euler path: 0 or 2 odd vertices) | none known; NP-complete |
| Algorithm | Hierholzer, $O(E)$ | backtracking, exponential worst case |
| Sufficient conditions | (the test is exact) | Dirac: min degree $\ge n/2$; Ore: $\deg u + \deg v \ge n$ for non-adjacent u, v |

The Petersen graph is 3-regular and highly symmetric yet has no Hamiltonian cycle. A **de Bruijn sequence** B(2, 3) is an Euler circuit that contains every 3-bit string exactly once in 8 characters.

**Colouring.** The **chromatic number** $\chi(G)$ is the fewest colours so that adjacent vertices differ. Bounds: $\omega(G) \le \chi(G) \le \Delta(G) + 1$, where ω is the largest clique and Δ the largest degree; **Brooks' theorem** improves this to Δ except for complete graphs and odd cycles; $\chi \le 2$ iff bipartite; the **four colour theorem** says planar graphs need at most 4. Greedy colouring depends on vertex order (a bad order used 6 colours on a 2-colourable crown graph). Triangle-free graphs can still need many colours (the Grötzsch graph needs 4). Applications: exam timetabling and register allocation.

**Planarity.** For a connected planar graph, **Euler's formula** $V - E + F = 2$ (cube: 8 − 12 + 6 = 2). It implies $E \le 3V - 6$ (for $V \ge 3$), and $E \le 2V - 4$ if there are no triangles. $K_5$ has 10 > 9 edges, and $K_{3,3}$ has 9 > 8, so neither is planar. **Kuratowski's theorem**: a graph is planar iff it contains no subdivision of $K_5$ or $K_{3,3}$. The edge bound is necessary, not sufficient (the Petersen graph passes it but is not planar).

**Matchings.** A **matching** is a set of edges with no shared endpoint; it is **maximum** if as large as possible and **perfect** if it covers every vertex. **Berge**: a matching is maximum iff it has no augmenting path. **Hall's theorem**: in a bipartite graph, side L can be fully matched iff $|N(S)| \ge |S|$ for every $S \subseteq L$ (if 3 applicants are together qualified for only 2 jobs, one must be left out). **König–Egerváry**: in bipartite graphs, maximum matching size = minimum vertex cover size.

**Spectral graph theory.** The Laplacian $L = D - A$ is symmetric positive semidefinite. The multiplicity of eigenvalue 0 equals the number of connected components. The second-smallest eigenvalue $\lambda_2$ (the **algebraic connectivity**) is small when the graph has a bottleneck, and the sign pattern of its eigenvector (the **Fiedler vector**) cuts the graph in two. A gap after the first k eigenvalues suggests k communities (the eigengap heuristic). Graph convolutional networks multiply node features by a normalised adjacency, averaging each node with its neighbours, which cancels noise when neighbours share a community.

**Random graphs.** In the Erdős–Rényi model $G(n, p)$ each edge appears independently. With average degree $c = np$, a **giant component** appears when c passes 1 (at c = 2 it holds about 79.7% of the vertices), and the graph becomes connected around $p = \ln n / n$. Real networks differ: **small-world** graphs (Watts–Strogatz) combine high clustering with short paths, and **scale-free** graphs (Barabási–Albert) have power-law degree tails and hubs.

**PageRank** is the stationary distribution of a random surfer who follows a random link with probability $\alpha = 0.85$ and teleports to a random page otherwise:

$$\pi_j = \frac{1 - \alpha}{n} + \alpha \sum_{i \to j} \frac{\pi_i}{\operatorname{outdeg}(i)}$$

Dangling pages (no out-links) are treated as linking everywhere. The teleport makes the chain irreducible and aperiodic, so π is unique, and **power iteration** converges geometrically at rate α.

**Why it matters.** Knowledge graphs and GraphRAG, GNNs, spectral clustering, node2vec random walks, the Hungarian matching loss in DETR, register allocation in ML compilers, and decision trees and computation graphs are all graph theory.

---

## Part II. Theory of Computation

## 9. Languages and finite automata

An **alphabet** Σ is a finite non-empty set of symbols (bits, letters, bytes, or an LLM's token vocabulary). A **string** is a finite sequence of symbols; ε is the empty string; $\Sigma^*$ is the set of all strings (infinite but countable). A **language** is any $L \subseteq \Sigma^*$. The **regular operations** are union, **concatenation** $L_1L_2 = \{xy\}$ and **Kleene star** $L^* = \{\varepsilon\} \cup L \cup LL \cup \dots$. Note $\varnothing \ne \{\varepsilon\}$: $L\varnothing = \varnothing$ but $L\{\varepsilon\} = L$, and $\varnothing^* = \{\varepsilon\}$.

A **deterministic finite automaton (DFA)** is a 5-tuple $(Q, \Sigma, \delta, q_0, F)$: finite states Q, alphabet Σ, transition function $\delta: Q \times \Sigma \to Q$, start state $q_0$ and accepting states F. It accepts w if reading w from $q_0$ ends in F. A language is **regular** if some DFA recognises it. Simulation takes $O(n)$ time and $O(1)$ memory.

*Worked example.* Binary numbers divisible by 3. Reading bit b turns x into $2x + b$, so the remainder r becomes $(2r + b) \bmod 3$:

| state | read 0 | read 1 |
|---|---|---|
| → r0 (accept) | r0 | r1 |
| r1 | r2 | r0 |
| r2 | r1 | r2 |

`110` (= 6): r0 → r1 → r0 → r0, accept. Design rule: decide **what the machine must remember** and make that the state.

An **NFA** may have several next states (or none) per symbol, and an **ε-NFA** may also move without reading: $\delta: Q \times (\Sigma \cup \{\varepsilon\}) \to \mathcal{P}(Q)$. It accepts if *some* sequence of choices ends in F. **Rabin–Scott (1959)**: the **subset construction** turns any NFA into a DFA whose states are sets of NFA states, so nondeterminism adds convenience, not power. The price can be exponential: "the n-th symbol from the end is 1" needs an NFA with n + 1 states but any DFA needs at least $2^n$ (two different n-bit strings must lead to different states).

## 10. Regular expressions, minimisation and limits

**Regular expressions** are built from ∅, ε, single symbols, union $R \mid S$, concatenation $RS$ and star $R^*$. Star binds tightest, then concatenation, then union, so `ab|c*` means `(ab)|(c*)`. Everyday syntax adds sugar without extra power: $R^+ = RR^*$, $R? = R \mid \varepsilon$, `[0-9]`.

**Kleene's theorem (1956):** regex ⇔ NFA ⇔ DFA describe exactly the regular languages. **Thompson's construction (1968)** builds an ε-NFA by gluing fragments, with at most about two states per regex symbol, so its size is linear in the regex. Simulating it with a *set* of current states takes $O(n \cdot |Q|^2)$ time in the worst case and never backtracks.

**DFA minimisation.** Two states are **distinguishable** if some suffix leads one to accept and the other to reject. The **table-filling algorithm** first marks every (accepting, non-accepting) pair, then repeatedly marks pairs whose successors on some symbol are already marked; unmarked pairs merge. The minimal DFA is unique up to renaming, so two regexes are equivalent iff their minimal DFAs are the same. Costs: table filling $O(|Q|^2|\Sigma|)$, Hopcroft's algorithm $O(|\Sigma|\,|Q| \log |Q|)$. Example: strings over {a, b} ending in `abb` need exactly 4 states (seen nothing, a, ab, abb).

**Closure properties.** Regular languages are closed under union, concatenation, star, complement (swap accepting states of a complete DFA), intersection (the **product construction** runs both DFAs on pairs of states), difference and reversal. Membership, emptiness, finiteness and equivalence are all decidable.

**Pumping lemma.** If L is regular there is a p such that every $s \in L$ with $|s| \ge p$ splits as $s = xyz$ with $|y| \ge 1$, $|xy| \le p$ and $xy^iz \in L$ for all $i \ge 0$. *Proof:* reading p symbols visits p + 1 states, so by pigeonhole a state repeats; y is the loop. *Use (a game):* to show $\{a^nb^n\}$ is not regular, pick $s = a^pb^p$; any legal split has y made of a's only, so $xy^2z$ has more a's than b's. You choose s and i; the adversary chooses the split. Balanced parentheses are not regular by closure: if they were, intersecting them with the regular language "some `(` followed by some `)`" (regex `\(*\)*`) would give the strings of n opening brackets followed by n closing ones, which is $a^nb^n$ with renamed letters and therefore not regular. **Myhill–Nerode** is the exact test: L is regular iff it has finitely many classes of pairwise-distinguishable prefixes (for $a^nb^n$, all $a^k$ are distinguishable).

**Regex in production: ReDoS.** Python `re`, Java, JavaScript, .NET, Perl and PCRE are **backtracking** engines. They support backreferences (`(a*)b\1` matches $a^nba^n$, which is not regular) but can take exponential time: `(a+)+$` against `aaa…a!` tries $2^{n-1}$ splits. This caused the Stack Overflow outage of July 2016 and the Cloudflare outage of 2 July 2019. Linear-time engines (RE2, Rust `regex`, Go `regexp`) use automata and drop backreferences. Defences: avoid nested quantifiers, use atomic groups, set timeouts, or use a linear-time engine.

**Mealy and Moore machines** are DFAs with outputs (Moore: output per state; Mealy: output per transition). A chatbot conversation flow modelled as a state machine is testable: you can list every state and prove, by reachability, that the DONE state is reachable only through CONFIRM.

**Constrained decoding.** To force an LLM's output to match a regex: compile it to a DFA, precompute for each (state, vocabulary token) the state reached by running the token's characters, and at each step set the logits of tokens leading to a dead state to −∞, allowing end-of-sequence only in accepting states. Every sample then matches by construction (Willard and Louf, 2023, the approach of the Outlines library).

| Model | Power | Key cost |
|---|---|---|
| DFA | regular | $O(n)$ time, $O(1)$ memory |
| NFA / ε-NFA | regular | set simulation; DFA may need $2^{\lvert Q\rvert}$ states |
| Regex | regular | Thompson NFA linear in regex size |
| Backtracking regex | more than regular | exponential worst case |
| Mealy / Moore | regular transducers | $O(n)$ |

## 11. Grammars, parsing and pushdown automata

Finite memory cannot count without limit, so nesting (brackets, HTML tags, nested JSON, `if … else`) needs more. A **context-free grammar (CFG)** is a 4-tuple $G = (V, \Sigma, R, S)$: variables V, terminals Σ, rules $A \to \alpha$ (one variable on the left), start variable S. A **derivation** rewrites variables until only terminals remain; a **parse tree** records which rules were used. The grammar $S \to aSb \mid \varepsilon$ generates $a^nb^n$: $S \Rightarrow aSb \Rightarrow aaSbb \Rightarrow aabb$.

A grammar is **ambiguous** if some string has two parse trees. $E \to E + E \mid E * E \mid \text{num}$ gives two trees for `2 + 3 * 4` (values 14 and 20). The fix is one variable per precedence level:

```
E -> E + T | T        (lowest precedence, left-associative)
T -> T * F | F
F -> ( E ) | num
```

The **dangling else** (`if a then if b then s1 else s2`) is resolved by attaching the else to the nearest if. Some languages, such as $\{a^ib^jc^k : i = j \text{ or } j = k\}$, are **inherently ambiguous**, and deciding whether a CFG is ambiguous is undecidable.

**Chomsky normal form (CNF):** every rule is $A \to BC$ or $A \to a$ (plus $S \to \varepsilon$ if needed). Every CFG converts to CNF in five steps: START (new start variable), TERM (replace terminals inside long rules), BIN (split long right sides), DEL (remove ε-rules), UNIT (remove $A \to B$ rules).

**CYK parsing** decides $w \in L(G)$ for a CNF grammar by dynamic programming. $T[i][\ell]$ is the set of variables deriving the substring of length ℓ at position i: length 1 uses rules $A \to w_i$, longer spans try every split k and rule $A \to BC$ with $B \in T[i][k]$ and $C \in T[i+k][\ell - k]$; accept iff $S \in T[0][n]$. Time $O(n^3 |R|)$, space $O(n^2 |V|)$.

**Recursive descent** writes one function per variable, chooses the rule by looking at the next token (LL(1) grammars), and runs in $O(n)$. Left recursion ($E \to E + T$) must be rewritten as a loop, which also gives left associativity: $10 - 4 - 3 = 3$. Exponentiation is right-associative: $2^{3^2} = 512$.

A **pushdown automaton (PDA)** is a finite automaton plus an unbounded **stack**: $(Q, \Sigma, \Gamma, \delta, q_0, F)$ with $\delta: Q \times (\Sigma \cup \{\varepsilon\}) \times (\Gamma \cup \{\varepsilon\}) \to \mathcal{P}(Q \times \Gamma^*)$. For $a^nb^n$: push a marker for each a, pop one for each b, accept if the stack is back to the bottom marker when the input ends. **A language is context-free iff some nondeterministic PDA recognises it.** Unlike automata, nondeterministic PDAs are strictly stronger than deterministic ones (even-length palindromes $ww^R$ need a guess of the middle).

**Pumping lemma for CFLs:** long strings split as $uvxyz$ with $|vy| \ge 1$, $|vxy| \le p$ and $uv^ixy^iz \in L$. For $a^pb^pc^p$, the window vxy touches at most two letter blocks, so pumping breaks the equal counts: $\{a^nb^nc^n\}$ is not context-free. CFLs are closed under union, concatenation and star but **not** under intersection or complement.

## 12. The Chomsky hierarchy and Turing machines

| Type | Rules | Languages | Machine | Membership | Example |
|---|---|---|---|---|---|
| 3 | $A \to aB$, $A \to a$, $A \to \varepsilon$ | regular | DFA / NFA | $O(n)$ | `a*b*`, identifiers |
| 2 | $A \to \alpha$ | context-free | PDA | $O(n^3)$ (CYK, Earley) | $a^nb^n$, JSON, arithmetic |
| 1 | $\alpha A \beta \to \alpha\gamma\beta$, $\gamma \ne \varepsilon$ | context-sensitive | linear-bounded automaton | decidable, PSPACE-complete in general | $a^nb^nc^n$, $\{ww\}$ |
| 0 | $\alpha \to \beta$ | recursively enumerable | Turing machine | only semi-decidable | the halting set |

The inclusions are strict: regular ⊊ context-free ⊊ context-sensitive ⊊ decidable ⊊ RE.

A **Turing machine (TM)** is a 7-tuple $(Q, \Sigma, \Gamma, \delta, q_0, q_{\text{accept}}, q_{\text{reject}})$ with an infinite tape, a head that reads and writes, and $\delta: Q \times \Gamma \to Q \times \Gamma \times \{L, R\}$. It may halt (accept or reject) or run forever. A single-tape TM checking palindromes zig-zags and takes about $\tfrac12 n^2$ steps. The **Church–Turing thesis** says every effective procedure can be carried out by a TM; it is a thesis, not a theorem, since "effective procedure" is informal. Python, C and a transformer with an unbounded scratchpad are Turing complete given enough memory. **Busy beaver** step counts grow faster than any computable function: BB(2) = 6, BB(3) = 21, BB(4) = 107, and the 5-state champion runs for over 47 million steps.

## 13. Decidability, the halting problem and Rice's theorem

A language is **decidable** if some TM halts on every input with the right yes/no answer, and **recognisable** (RE, semi-decidable) if some TM accepts exactly its members but may loop on non-members. L is decidable iff both L and its complement are recognisable.

**The halting problem** $\text{HALT} = \{\langle P, x\rangle : P \text{ halts on } x\}$ is recognisable (run P and wait) but **not decidable** (Turing, 1936). Suppose `halts(P, x)` were perfect, and define `paradox(P)`: loop forever if `halts(P, P)`, else return. Then `paradox(paradox)` halts iff it does not halt, a contradiction. It is Cantor's diagonal argument with programs as rows and inputs as columns. Since HALT is recognisable but not decidable, its complement is not even recognisable.

**Rice's theorem (1953):** every non-trivial property of what a program *does* (its input/output behaviour) is undecidable. "Non-trivial" means some programs have it and some do not; behavioural properties differ from syntactic ones such as "does the source contain `while`?". The proof is a **reduction**: given $\langle P, x\rangle$, build Q that runs $P(x)$ and then prints `hello`. A decider for "does Q ever print hello?" would decide HALT. To prove a new problem X undecidable, reduce HALT **to** X.

Practical tools therefore trade something away:

| Strategy | Gives up | Examples |
|---|---|---|
| Sound but incomplete | precision (false alarms) | type checkers, Rust's borrow checker, abstract interpretation |
| Complete but unsound | coverage (missed bugs) | testing, fuzzing, heuristic linters, LLM code review |
| Restrict the language | expressiveness | regex without backreferences, SQL without recursion, total languages (Coq, Agda, Lean) |
| Bounded checking | guarantees beyond the bound | timeouts, step limits, bounded model checking |

## 14. Complexity classes (recap)

Decidability asks whether a problem can be solved; complexity asks how fast.

| Class | Meaning | Example |
|---|---|---|
| P | polynomial time | CFG membership (CYK), shortest paths, sorting |
| NP | yes-answers have certificates checkable in polynomial time | SAT, Hamiltonian cycle, 3-colouring |
| NP-complete | in NP, and every NP problem reduces to it | SAT (Cook–Levin, 1971), TSP decision version |
| PSPACE | polynomial memory | context-sensitive membership |
| EXPTIME | exponential time | generalised chess (EXPTIME-complete) |

$$\text{P} \subseteq \text{NP} \subseteq \text{PSPACE} \subseteq \text{EXPTIME} \subsetneq \text{decidable} \subsetneq \text{RE}$$

P ≠ EXPTIME by the time hierarchy theorem, so at least one inclusion between them is strict, but whether P = NP is still open as of 2026. Reductions and NP-completeness proofs are developed in [`advanced_algorithms/02`](../../../00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb).

**Why it matters for AI.** Grammar-constrained decoding (llama.cpp GBNF grammars, Outlines, XGrammar, the structured-output modes of vLLM and hosted APIs) runs an automaton, often a pushdown automaton because nested JSON is not regular, next to the LLM so every output is syntactically valid; the model's preferences still choose *which* valid string comes out. Tokenizers and lexers are automata, probabilistic CFGs parse natural language, and the halting problem explains why no single checker can certify the safety of arbitrary code an AI writes or runs.

---

## Where to go next

- Algorithms that use these ideas: [`00_AI_Fundamentals/dsa/`](../../../00_AI_Fundamentals/dsa/) and then [`00_AI_Fundamentals/advanced_algorithms/`](../../../00_AI_Fundamentals/advanced_algorithms/).
- The continuous side of the maths folder: [`09_numerical_methods`](../../09_numerical_methods.ipynb), [`10_numerical_linear_algebra`](../../10_numerical_linear_algebra.ipynb), [`11_matrix_calculus_and_autodiff_from_scratch`](../../11_matrix_calculus_and_autodiff_from_scratch.ipynb), [`12_convex_optimization_and_duality`](../../12_convex_optimization_and_duality.ipynb).
- Structured outputs in practice: [`08_LLM/17_structured_outputs`](../../../08_LLM/17_structured_outputs.ipynb).
- The notebooks themselves: [01](../01_sets_relations_functions_and_proofs.ipynb), [02](../02_combinatorics_and_recurrences.ipynb), [03](../03_graph_theory.ipynb), [04](../04_automata_and_regular_languages.ipynb), [05](../05_grammars_parsing_and_computability.ipynb), and the folder [README](../README.md).

---

## Glossary

- **Alphabet (Σ)** — a finite, non-empty set of symbols.
- **Ambiguous grammar** — a grammar in which some string has two or more parse trees.
- **Antisymmetric relation** — $a\,R\,b$ and $b\,R\,a$ together force $a = b$.
- **Bell number $B_n$** — the number of partitions of an n-element set.
- **Bijection** — a function that is both injective and surjective; it has an inverse.
- **Binomial coefficient $\binom{n}{k}$** — the number of k-element subsets of an n-element set.
- **Bipartite graph** — vertices split into two sides with every edge between the sides; equivalently, no odd cycle.
- **Birthday paradox** — collisions among m equally likely values become likely after about $1.18\sqrt{m}$ draws.
- **Cartesian product** — the set of all ordered pairs $(a, b)$ with $a \in A$, $b \in B$.
- **Catalan number $C_n$** — $\binom{2n}{n}/(n+1)$; counts binary trees, balanced brackets and parse trees.
- **Chomsky hierarchy** — regular ⊂ context-free ⊂ context-sensitive ⊂ recursively enumerable languages.
- **Chomsky normal form** — every rule is $A \to BC$ or $A \to a$.
- **Chromatic number χ(G)** — the fewest colours needed so adjacent vertices differ.
- **Church–Turing thesis** — anything computable by an effective procedure is computable by a Turing machine.
- **Closure (of a relation)** — the smallest relation containing R that has a given property.
- **Codomain / range** — the declared target set of a function / the set of values it actually takes.
- **Context-free grammar** — rules with a single variable on the left; describes nesting.
- **Countable set** — finite, or listable as $a_0, a_1, a_2, \dots$.
- **CYK algorithm** — $O(n^3)$ dynamic-programming membership test for grammars in CNF.
- **Decidable language** — one for which a Turing machine always halts with the correct answer.
- **Derangement** — a permutation with no fixed point; about $n!/e$ of them.
- **DFA** — deterministic finite automaton: exactly one next state per state and symbol.
- **Diagonal argument** — build an object that differs from the k-th item of any list at position k.
- **Equivalence relation** — reflexive, symmetric and transitive; corresponds to a partition.
- **Euler circuit** — a closed walk using every edge exactly once.
- **Fiedler vector** — eigenvector of the second-smallest Laplacian eigenvalue; used to bisect a graph.
- **Generating function** — a power series whose coefficients are a sequence of counts.
- **Halting problem** — deciding whether a program halts on an input; undecidable.
- **Hamiltonian cycle** — a cycle visiting every vertex exactly once; NP-complete to find.
- **Handshake lemma** — the degrees of a graph sum to twice the number of edges.
- **Hasse diagram** — a drawing of a partial order showing only covering pairs.
- **Induction** — proof by base case plus the step $P(k) \Rightarrow P(k+1)$.
- **Inclusion–exclusion** — counts a union by alternating sums of intersection sizes.
- **Injective function** — different inputs give different outputs.
- **Kleene star** — zero or more concatenated copies: $L^* = \{\varepsilon\} \cup L \cup LL \cup \dots$.
- **Language** — any set of strings over an alphabet.
- **Laplacian** — $L = D - A$; its zero eigenvalues count connected components.
- **Loop invariant** — a statement true before every iteration of a loop, used to prove correctness.
- **Matching** — a set of edges with no shared endpoints.
- **NFA** — nondeterministic finite automaton; may have several or no next states, and ε-moves.
- **Partial order** — reflexive, antisymmetric and transitive relation.
- **Partition** — a split of a set into non-empty, disjoint blocks that cover it.
- **Pigeonhole principle** — N objects in k boxes put at least $\lceil N/k \rceil$ in some box.
- **Planar graph** — can be drawn without crossing edges; satisfies V − E + F = 2.
- **Power set** — the set of all subsets; has $2^n$ elements.
- **Pumping lemma** — every long string of a regular (or context-free) language can be pumped; used to prove a language is not in the class.
- **Pushdown automaton** — a finite automaton with a stack; recognises exactly the context-free languages.
- **Recognisable (RE) language** — accepted by a Turing machine that may loop on non-members.
- **Recurrence relation** — defines each term of a sequence from earlier terms.
- **Reduction** — transforming instances of one problem into another to transfer hardness or undecidability.
- **Regular language** — recognised by a DFA; equivalently described by a regular expression.
- **ReDoS** — denial of service caused by exponential backtracking in a regex engine.
- **Rice's theorem** — every non-trivial behavioural property of programs is undecidable.
- **Stars and bars** — $\binom{n+r-1}{r}$ ways to choose r items from n types with repetition.
- **Stirling number (2nd kind) $S(n,k)$** — ways to partition n items into k non-empty blocks.
- **Subset construction** — converts an NFA into an equivalent DFA whose states are sets of NFA states.
- **Surjective function** — every element of the codomain is hit.
- **Thompson's construction** — builds an ε-NFA of linear size from a regular expression.
- **Topological order** — an ordering of a DAG's vertices with every edge pointing forward.
- **Transitive closure** — all pairs connected by a path of one or more steps; Warshall computes it in $\Theta(n^3)$.
- **Tree** — a connected acyclic graph; with n vertices it has n − 1 edges.
- **Turing machine** — finite control plus an infinite read/write tape; the standard model of computation.
- **Well-ordering principle** — every non-empty set of natural numbers has a least element.
