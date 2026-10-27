# Discrete Mathematics & Theory of Computation

**Discrete mathematics** is the maths of things you can count one by one (people, files, words, program steps), as opposed to smooth quantities like temperature. This 5-notebook module covers the two core first- and second-year courses of BS AI, BS CS and BS Data Science programmes: **Discrete Structures** (notebooks 01–03: sets, relations, functions, proofs, counting, recurrences, graphs) and **Theory of Automata / Theory of Computation** (notebooks 04–05: finite automata, regular expressions, grammars, parsing, Turing machines and the limits of computation). It is an **optional, university-level track**: the rest of the course does not depend on it, but it is strongly recommended for BS/MS AI students and for exam or interview preparation.

**Why an AI developer needs it.**

1. **Proofs and induction for algorithms.** A test shows that code works on the inputs you tried; a proof (often by induction or a loop invariant) shows it works on *every* input. That is how you know binary search, Euclid's algorithm or a scheduler is correct.
2. **Counting for probability.** Every probability on a finite sample space is "favourable outcomes ÷ all outcomes", so counting (permutations, combinations, inclusion–exclusion) comes first. Counting also tells you *before you write code* that a grid search, a brute-force feature selection or an exhaustive decoder is hopeless.
3. **Graphs everywhere.** Knowledge graphs, graph neural networks, PageRank, task DAGs in ML pipelines, the computation graph behind `loss.backward()`, matching losses in object detectors: all of these are graph theory.
4. **Regex, automata and grammars for parsing and constrained LLM decoding.** Every tokenizer, input validator and config loader is a finite automaton or a parser, and when an LLM is forced to emit valid JSON, a regex-derived automaton or a grammar is masking its tokens.
5. **Computability limits.** The halting problem and Rice's theorem prove that no tool can perfectly detect every bug, every piece of malware or every unsafe program, which tells you what static analysers and AI-safety checkers can and cannot promise.

> **When to take it:** do it **alongside [`00_AI_Fundamentals/dsa/`](../../00_AI_Fundamentals/dsa/)** (DSA gives the algorithms, this module gives the maths that proves and counts them) and **before [`00_AI_Fundamentals/advanced_algorithms/`](../../00_AI_Fundamentals/advanced_algorithms/)** (NP-completeness, network flows and randomised algorithms all assume the proofs, counting and graph theory taught here).
>
> **Related reading in the parent folder:** four new numerical notebooks sit next to this folder and complement it from the "continuous" side: [`09_numerical_methods`](../09_numerical_methods.ipynb) (root finding, interpolation, numerical integration, ODE solvers), [`10_numerical_linear_algebra`](../10_numerical_linear_algebra.ipynb), [`11_matrix_calculus_and_autodiff_from_scratch`](../11_matrix_calculus_and_autodiff_from_scratch.ipynb) (the computation graph and its reverse topological order from notebook 01 show up again here) and [`12_convex_optimization_and_duality`](../12_convex_optimization_and_duality.ipynb). Notebook 05 ends by pointing you to 09.

---

## The whole topic explained simply

Discrete maths is the grammar of computer science. A **set** is a group of things with no repeats, like the contacts in your phone; a **relation** says which pairs are connected, like "follows" on Instagram; a **function** is a vending machine that gives exactly one snack per button. **Counting** is the art of knowing how many options there are without listing them, the way a café knows that 3 breads, 4 fillings and 2 sauces make 24 sandwiches. A **graph** is dots joined by lines, which is all a road map, a social network or a web of hyperlinks really is. A **finite automaton** is a machine with a few "moods" (states) that reads text one letter at a time, like a metro turnstile that is either locked or unlocked. A **grammar** is a rule book for which sentences are allowed, and a **parser** is a program that checks a sentence against it, like a calculator deciding that `2 + 3 × 4` means `2 + 12`. At the top sits the **Turing machine**, a model of every possible computer, and the surprising result that some questions ("will this program ever stop?") can never be answered by any program. Finally, a **proof** is an argument that covers every case at once, the way scaling every ingredient shows a recipe works for any number of guests, not only the 2, 4 and 6 you tested.

**Tiny worked example (real numbers).** Six students must be paired for a project, and each possible pair is drawn as a line between two dots.

| Question | Tool | Answer |
|---|---|---|
| How many different pairs are possible? | combinations (notebook 02): $\binom{6}{2} = \frac{6 \cdot 5}{2}$ | **15** |
| How many lines does the picture have? | the complete graph $K_6$ (notebook 03) | **15**, one per pair |
| How many lines touch each student? | degree | **5** (everyone else) |
| Check: sum of all degrees | handshake lemma: sum of degrees = 2 × lines | 6 × 5 = **30** = 2 × 15 ✓ |
| Is "is in the same pair as" (after pairing) an equivalence relation? | reflexive, symmetric, transitive (notebook 01) | **yes**: 3 classes of 2 students |

Counting, graphs and relations answered three views of the same small situation, and they agree.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | Beginners who know basic Python and high-school maths; university students revising *Discrete Structures* or *Theory of Automata / Computation* for an exam; anyone preparing for algorithms, ML-engineering or compiler-style interview questions. |
| **Prerequisites** | [Python basics](../../01_Python/01_basic.ipynb) (sets, dicts, functions, loops, recursion). Helpful: the [maths notation bridge](../00_start_here_math_notation_bridge.ipynb), [logic in classical AI](../../00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb) (truth tables, quantifiers), [complexity and recursion](../../00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb), [linear algebra](../01_linear_algebra.ipynb) (eigenvalues, for spectral graph theory) and [probability](../03_probability.ipynb). |
| **Time needed** | About 15 to 18 hours in total (3 to 4 hours per notebook), more if you do every practice problem. |
| **Runs on** | CPU only, no API key, no internet. Libraries: Python standard library, numpy, pandas, matplotlib, networkx. Each notebook runs in about a minute or less. |
| **Optional?** | Yes. University-level fundamentals track; recommended, not required. |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Sets, relations, functions and proofs](01_sets_relations_functions_and_proofs.ipynb) | The basic objects of discrete maths (sets, relations, partial orders, functions, countability) and the proof techniques, including induction and loop invariants, used to show code is correct. | 3 h |
| 02 | [Combinatorics and recurrences](02_combinatorics_and_recurrences.ipynb) | Counting without listing (permutations, combinations, pigeonhole, inclusion–exclusion), solving recurrences, generating functions, and Catalan and Stirling numbers. | 3 h |
| 03 | [Graph theory](03_graph_theory.ipynb) | The theorems behind graphs: handshake lemma, trees and Cayley's formula, Euler vs Hamilton, colouring, planarity, matchings, spectral graph theory, random graphs and PageRank. | 3–4 h |
| 04 | [Automata and regular languages](04_automata_and_regular_languages.ipynb) | DFAs, NFAs, a from-scratch regex engine, DFA minimisation, the pumping lemma, ReDoS, and constrained LLM decoding with an automaton. | 3–4 h |
| 05 | [Grammars, parsing and computability](05_grammars_parsing_and_computability.ipynb) | Context-free grammars, CYK and recursive-descent parsers, pushdown automata, the Chomsky hierarchy, Turing machines, the halting problem and grammar-constrained decoding. | 3–4 h |

Notebooks 01 → 02 → 03 are the *Discrete Structures* half; 04 → 05 are the *Theory of Computation* half. Notebook 04 needs 01 (sets, closure, proofs) and 03 (directed graphs); notebook 05 starts exactly where 04 stops.

```
 01 sets, relations, proofs ──> 02 counting, recurrences ──> 03 graphs
          │                                                     │
          └──────────────────────> 04 automata, regex <─────────┘
                                         │
                                         v
                              05 grammars, Turing machines
```

---

## The notebooks one by one

### 01 · Sets, Relations, Functions and Proofs

*Explained simply.* A set is a bag of distinct things where order does not matter; a relation records which pairs are linked; a function gives exactly one output for each input. Relations come in useful kinds: an **equivalence relation** sorts things into non-overlapping bins of "the same for my purposes", and a **partial order** says what must come before what. A **proof** shows a statement is true for every case, and **induction** proves it for every number n by showing the first case and that each case pushes over the next. Think of a school timetable: you must take Maths 1 before Maths 2, but Art and History can go in either order; that is a partial order, and any valid semester plan is a topological order.

*Tiny example.* Ali's friends are {Sara, Bilal, Zoya}; Sara's friends are {Ali, Bilal, Omar}.

| Operation | Result | Size |
|---|---|---|
| Friends in common (intersection) | {Bilal} | 1 |
| Everyone either knows (union) | {Sara, Bilal, Zoya, Ali, Omar} | 5, not 6 (Bilal counted once) |

And a proof that one test is not enough: $n^2 + n + 41$ is prime for n = 0 … 39, but n = 40 gives $1681 = 41^2$.

*You will learn*
- Set operations, De Morgan's laws, power sets ($2^n$ subsets) and Cartesian products, all checked by brute force.
- The four relation properties (reflexive, symmetric, antisymmetric, transitive), equivalence classes and partitions.
- Partial orders, Hasse diagrams, topological order with Kahn's algorithm, and Warshall's transitive-closure algorithm.
- Injective, surjective and bijective functions, and how many functions exist between finite sets.
- Countability and Cantor's diagonal argument (the integers and fractions are countable, the reals are not).
- Direct proof, contrapositive, contradiction, cases, counterexample, induction, strong induction and loop invariants.

*Key takeaway:* testing is evidence, a proof is a guarantee, and induction is the proof tool that matches loops and recursion.

### 02 · Combinatorics and Recurrences

*Explained simply.* Combinatorics is counting without listing: "or" usually means add and "and then" usually means multiply. Choosing r things from n depends on two questions: does order matter, and is repetition allowed? A **recurrence** describes a count using smaller counts ("ways to climb 10 stairs = ways to climb 9 + ways to climb 8"), and solving it gives a direct formula. Think of a phone PIN: 4 digits with 10 choices each give 10 × 10 × 10 × 10 = 10,000 possibilities, so a random guess succeeds once in 10,000 tries.

*Tiny example.* You own 3 T-shirts (red, blue, green) and 2 pairs of jeans.

| Question | Order matters? | Count |
|---|---|---|
| Outfits (one shirt and one pair of jeans) | product rule | 3 × 2 = **6** |
| Pack 2 of the 3 shirts | no | $\binom{3}{2}$ = **3** |
| Choose Monday's and Tuesday's shirt (different) | yes | 3 × 2 = **6** |

And the birthday paradox: with only 23 people, the chance that two share a birthday is already 50.7%.

*You will learn*
- The sum, product, subtraction and division rules, permutations, combinations and "stars and bars".
- The binomial theorem, Pascal's triangle and multinomial coefficients.
- The pigeonhole principle, the birthday paradox and why hash collisions arrive after about $1.18\sqrt{m}$ keys.
- Inclusion–exclusion, derangements ($\approx n!/e$) and counting onto functions.
- Solving linear recurrences with characteristic roots, and Fibonacci in O(log n) with matrix powers.
- Generating functions, Catalan numbers (trees, brackets, parse trees) and Stirling and Bell numbers (set partitions, clusterings).

*Key takeaway:* counting tells you, before running anything, whether brute force is possible or whether you need heuristics, DP or sampling.

### 03 · Graph Theory

*Explained simply.* A graph is dots (vertices) joined by lines (edges). Graph theory asks questions about the picture: can I walk every road exactly once, how few colours keep neighbours different, which single road would cut the city in two? Some of these have neat answers (Euler circuits), some are famously hard (Hamiltonian cycles), and knowing which is which tells an engineer when to use an exact algorithm and when to settle for a good-enough one. Think of an exam timetable: draw a line between two exams whenever a student takes both, and the minimum number of time slots is the graph's **chromatic number**.

*Tiny example.* Ali knows Sara and Bilal, Sara knows Bilal, and Zoya knows only Sara.

| Person | Friends (degree) |
|---|---|
| Ali | 2 |
| Sara | 3 |
| Bilal | 2 |
| Zoya | 1 |
| **Total** | **8 = 2 × 4 friendships** (handshake lemma) |

*You will learn*
- Degrees, the handshake lemma, walks counted by matrix powers, connectivity, bipartite graphs and isomorphism.
- Six equivalent definitions of a tree, Cayley's formula $n^{n-2}$ and the matrix-tree theorem.
- Euler circuits (easy, all degrees even) versus Hamiltonian cycles (NP-complete).
- Graph colouring, planarity and Euler's formula $V - E + F = 2$, and why $K_5$ and $K_{3,3}$ are not planar.
- Matchings, Hall's marriage theorem and König's theorem.
- The Laplacian, the Fiedler vector, random graphs (Erdős–Rényi, small worlds, scale-free) and PageRank from scratch.

*Key takeaway:* the matrices of a graph (adjacency, Laplacian) carry its shape, which is exactly what spectral clustering, GNNs and PageRank exploit.

### 04 · Automata and Regular Languages

*Explained simply.* A **finite automaton** has a fixed, small number of states, reads input one symbol at a time, and at the end says accept or reject. Its only memory is its current state, so it cannot count without limit. A **regular expression** (regex) is a compact way to write the same thing, and every regex can be turned mechanically into an automaton. Think of a turnstile: two states (locked, unlocked), a coin unlocks it, a push locks it again.

*Tiny example.* A DFA that accepts binary numbers divisible by 3 keeps only the remainder r, and reading bit b changes it to (2r + b) mod 3. Trace of `110` (= 6):

```
start r0 --1--> r1 --1--> r0 --0--> r0     ends in r0 (remainder 0): accept
```

*You will learn*
- Alphabets, strings, languages and the regular operations (union, concatenation, Kleene star).
- DFAs, NFAs and the subset construction, including the $2^n$ worst-case blow-up.
- A working regex engine via Thompson's construction, tested against Python's `re`.
- DFA minimisation, closure properties and the product construction.
- The pumping lemma and Myhill–Nerode, proving that $a^nb^n$ and balanced brackets are not regular.
- Catastrophic backtracking (ReDoS), Mealy/Moore machines, and constrained decoding of a toy LLM with a DFA mask.

*Key takeaway:* regex ⇔ NFA ⇔ DFA, finite memory means no unbounded counting, and an automaton can make an LLM's invalid output impossible.

### 05 · Grammars, Parsing and Computability

*Explained simply.* A **grammar** is a small set of rules for which sentences are allowed, and a **parser** checks a sentence against the rules and builds a tree of how the pieces fit. Grammars can describe **nesting** (brackets inside brackets), which regex cannot, and their matching machine is a **pushdown automaton**: a finite automaton with a stack. At the top of the ladder, a **Turing machine** can run any algorithm, yet some questions (does this program halt?) no program can answer for every input. Think of checking brackets like stacking plates: each `(` adds a plate, each `)` removes one, and the brackets are wrong if you take from an empty pile or plates are left at the end.

*Tiny example.* Rule: "a sentence is empty, or `a` + sentence + `b`".

| Wraps | String | Allowed? |
|---|---|---|
| 0 | (empty) | yes |
| 1 | `ab` | yes |
| 3 | `aaabbb` | yes |
| — | `aabbb` | no: the rule always adds one `a` and one `b` together |

*You will learn*
- Context-free grammars, derivations, parse trees and ambiguity (arithmetic precedence, the dangling else).
- Chomsky normal form and the CYK parser, which decides membership in $O(n^3)$.
- Recursive-descent parsers for arithmetic and a JSON subset, and pushdown automata.
- The Chomsky hierarchy: regular ⊂ context-free ⊂ context-sensitive ⊂ recursively enumerable.
- Turing machines, the Church–Turing thesis and busy beavers.
- The halting problem, Rice's theorem, a recap of P and NP, and grammar-constrained LLM decoding.

*Key takeaway:* nesting needs a stack, and every non-trivial question about what a program *does* is undecidable, so real tools always trade something away.

---

## How this connects to the rest of the repo and to real AI systems

- **Algorithms:** [`dsa/01`](../../00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb) solves divide-and-conquer recurrences; notebook 02 solves linear ones. [`dsa/07`](../../00_AI_Fundamentals/dsa/07_graphs.ipynb) teaches graph *algorithms*; notebook 03 teaches graph *theorems*. [`dsa/09`](../../00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb) computes recurrences, and Warshall and CYK are dynamic programs. [`dsa/04`](../../00_AI_Fundamentals/dsa/04_hashing.ipynb) handles the collisions that pigeonhole forces.
- **Advanced algorithms:** union-find ([`advanced_algorithms/01`](../../00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb)), NP-completeness and reductions ([`advanced_algorithms/02`](../../00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb)) and network flows and the Hungarian algorithm ([`advanced_algorithms/04`](../../00_AI_Fundamentals/advanced_algorithms/04_network_flows_and_matching.ipynb)) build directly on notebooks 01, 03 and 05.
- **Logic and search:** propositional and first-order logic live in [`classical_ai/07`](../../00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb); grammar derivations are a state-space search like [`classical_ai/02`](../../00_AI_Fundamentals/classical_ai/02_uninformed_search.ipynb).
- **LLMs:** constrained decoding (notebooks 04 and 05) is the mechanism behind JSON mode in [`08_LLM/17_structured_outputs`](../../08_LLM/17_structured_outputs.ipynb); knowledge graphs and GraphRAG are in [`08_LLM/09_knowledge_graphs`](../../08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb); $V^L$ possible outputs explain why decoding uses greedy, beam search or sampling ([`07_NLP/05`](../../07_NLP/05_language_models_and_generation.ipynb)).
- **Deep learning:** GNNs multiply by a normalised adjacency matrix ([`05_Deep_Learning/07_gnn`](../../05_Deep_Learning/07_gnn.ipynb)); autograd walks the computation graph in reverse topological order ([`05_Deep_Learning/01`](../../05_Deep_Learning/01_neural_network_fundamentals.ipynb), [`14_Mathematics/11`](../11_matrix_calculus_and_autodiff_from_scratch.ipynb)).
- **NLP:** text cleaning with regex ([`07_NLP/01`](../../07_NLP/01_text_preprocessing.ipynb)) and CKY parsing of English ([`07_NLP/10`](../../07_NLP/10_advanced_nlp_tasks.ipynb)).
- **Data and MLOps:** a database table is a relation ([`13_Databases/00_dbms_fundamentals/03`](../../13_Databases/00_dbms_fundamentals/03_relational_model_and_relational_algebra.ipynb)); pipelines are task DAGs run in topological order ([`15_MLOps/03_pipeline_orchestration`](../../15_MLOps/03_pipeline_orchestration/01_orchestration.ipynb)); retrieval precision and recall are set sizes ([`08_LLM/02_rag/01`](../../08_LLM/02_rag/01_rag_fundamentals.ipynb)).
- **Machine learning:** grid search, feature selection and optimal decision trees explode combinatorially ([`03_Machine_Learning/06_model_evaluation/02`](../../03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb), [`03_Machine_Learning/01_supervised/03`](../../03_Machine_Learning/01_supervised/03_decision_trees.ipynb)); k-means is a local search because there are $S(n, k)$ possible clusterings.
- **Probability:** counting is the foundation of [`14_Mathematics/03_probability`](../03_probability.ipynb), and PageRank is a Markov chain's stationary distribution.

---

## Common beginner mistakes

- **"Antisymmetric" means "not symmetric".** It does not: `=` is both symmetric and antisymmetric, and {(1,2), (2,1), (1,3)} is neither.
- **Writing `{}` for the empty set in Python.** `{}` is an empty dict; the empty set is `set()`. In theory, the empty language ∅ is also not {ε} (one empty string).
- **Wrong base case or an induction step that fails on the first transition** (the "all horses are the same colour" fallacy). Check that the step works for the smallest k, and that you have as many base cases as the step reaches back.
- **Confusing codomain with range.** $f(x) = x^2$ from ℝ to ℝ is not onto, but from ℝ to $[0, \infty)$ it is.
- **Using the wrong counting formula.** Always ask "does order matter?" and "is repetition allowed?" first. For a repeated characteristic root, the second basis term is $n r^n$, not another $r^n$.
- **Mixing up Euler and Hamilton.** Euler uses every *edge* once (easy, check degrees); Hamilton visits every *vertex* once (NP-complete).
- **Choosing the split in a pumping-lemma proof.** You choose the string and the pump count i; the adversary chooses the split $xyz$, so your argument must work for *every* legal split.
- **Using regex for nested data** (HTML, nested JSON, balanced brackets), or writing nested quantifiers like `(a+)+` in a backtracking engine. The first is impossible, the second invites ReDoS.
- **Reducing in the wrong direction.** To show problem X is undecidable or NP-hard, reduce the *known-hard* problem (HALT, SAT) **to** X, not X to it.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| How many subsets does an n-element set have? | $2^n$ |
| Equivalence relation = ? | reflexive + symmetric + transitive; it corresponds one-to-one to a partition |
| Partial order = ? | reflexive + antisymmetric + transitive; drawn as a Hasse diagram |
| Is ℚ countable? Is ℝ? | ℚ yes (pairs of integers); ℝ no (Cantor's diagonal argument) |
| Two parts of an induction proof? | base case and inductive step $P(k) \Rightarrow P(k+1)$ |
| r-combinations with repetition from n types? | $\binom{n+r-1}{r}$ (stars and bars) |
| How many people for a 50% shared birthday? | 23 |
| Handshake lemma? | sum of degrees = 2·E, so the number of odd-degree vertices is even |
| When does a connected graph have an Euler circuit? | when every vertex has even degree |
| Euler's formula for connected planar graphs? | V − E + F = 2, hence E ≤ 3V − 6 |
| Are NFAs more powerful than DFAs? | no; same languages, but a DFA may need $2^n$ states |
| Show $a^nb^n$ is not regular? | pumping lemma (or Myhill–Nerode) |
| CYK running time? | $O(n^3 \cdot \lvert R \rvert)$ for a grammar in Chomsky normal form |
| Is the halting problem decidable? | no (Turing 1936), but it is recognisable |
| Rice's theorem? | every non-trivial property of a program's behaviour is undecidable |

---

## Further reading

**Classic textbooks**
- K. H. Rosen, *Discrete Mathematics and Its Applications*, 8th ed. (2019): the standard *Discrete Structures* text (chapters 1, 2, 5, 6, 8–11 match notebooks 01–03).
- R. L. Graham, D. E. Knuth and O. Patashnik, *Concrete Mathematics*, 2nd ed. (1994): binomials, special numbers, generating functions.
- D. J. Velleman, *How to Prove It*, 3rd ed. (2019): the best book for learning to write proofs.
- D. B. West, *Introduction to Graph Theory*, 2nd ed. (2001).
- M. Sipser, *Introduction to the Theory of Computation*, 3rd ed. (2012): the standard *Theory of Computation* text (chapters 1–5 and 7 match notebooks 04–05).
- J. E. Hopcroft, R. Motwani and J. D. Ullman, *Introduction to Automata Theory, Languages, and Computation*, 3rd ed. (2006).
- A. V. Aho, M. S. Lam, R. Sethi and J. D. Ullman, *Compilers: Principles, Techniques, and Tools* ("the Dragon Book"), 2nd ed., chapter 4 (parsing).

**Free resources**
- E. Lehman, F. T. Leighton and A. R. Meyer, *Mathematics for Computer Science* (MIT, free PDF; MIT OpenCourseWare course 6.1200J, formerly 6.042J).
- H. S. Wilf, *generatingfunctionology* (free PDF from the author).
- R. Diestel, *Graph Theory* (free electronic edition) and D. A. Spielman, *Spectral and Algebraic Graph Theory* (Yale lecture notes).
- A.-L. Barabási, *Network Science* (free online at networksciencebook.com).
- MIT OpenCourseWare 18.404J *Theory of Computation* (Sipser's own lectures) and Stanford CS103 *Mathematical Foundations of Computing* notes.
- R. Cox, "Regular Expression Matching Can Be Simple And Fast" (2007, swtch.com).
- B. T. Willard and R. Louf, "Efficient Guided Generation for Large Language Models" (arXiv:2307.09702, 2023): regex- and grammar-constrained decoding.

For a deeper, concept-by-concept study guide with formulas, worked examples and a glossary, read [`notes/discrete_math.md`](notes/discrete_math.md).
