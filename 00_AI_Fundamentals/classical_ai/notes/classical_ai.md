# Classical AI: Study Guide

Classical AI is the branch of artificial intelligence in which a program reaches a goal by **searching, reasoning and planning** over knowledge that people have written down, instead of learning that knowledge from data. This guide walks through every concept in the eleven notebooks of this folder, in order, with definitions, intuition, small examples worked by hand, the key formulas, and comparison tables. It matches the standard university "Artificial Intelligence" course (Russell & Norvig, *AIMA*, 4th ed.), so it doubles as exam and interview revision. The front door for this folder is [`../README.md`](../README.md).

## 1. Where Classical AI Fits

**Artificial intelligence (AI)** is any program that chooses what to do in a smart way. It has two big families:

- **Classical / symbolic AI** (also called **GOFAI**, "Good Old-Fashioned AI", a name coined by John Haugeland in 1985): people write the knowledge as symbols, rules and models of actions, and the program uses **search, logic, planning and constraint solving**.
- **Machine learning (ML)**: the program learns its rules from examples. **Deep learning** is ML with large neural networks, and **LLMs** (large language models) are deep-learning models trained on text.

```
AI
 +-- Classical / symbolic AI : search, logic, planning, CSPs  (+ Bayes nets, fuzzy logic in this course)
 +-- Machine learning
      +-- Deep learning
           +-- LLMs
```

Until about 1990 most progress came from the symbolic camp; since 2012 (AlexNet) most headlines come from learning. Two **AI winters** (about 1974-1980 and 1987-1993) followed periods of over-promising. The most famous recent systems are **hybrids**: AlphaGo combines tree search with neural networks, and LLM agents combine a learned model with planning and tool use.

**Why it matters:** search, planning and logic are the "thinking ahead" layer that learning alone does not provide. Every map app, chess engine, scheduler and agent framework uses it.

## 2. Agents and Environments (notebook 01)

An **agent** perceives its **environment** through **sensors** and acts on it through **actuators**. A **percept** is what it senses at one moment; the **percept sequence** is everything it has ever sensed. The **agent function** maps percept sequences to actions (a mathematical description); the **agent program** is the code that implements it. A table-driven agent function needs $\sum_{t=1}^{T} |P|^t$ entries: with only 4 possible percepts and a 20-step lifetime that is about $1.5 \times 10^{12}$, so the real challenge of AI is writing *small programs* that behave rationally.

**Rationality.** A **rational agent** chooses the action that maximises the **expected** value of its **performance measure**, given its percepts and built-in knowledge. Rational is not omniscient: it can be unlucky. Rationality also depends on the measure: in the 2-room vacuum world, a reflex agent is rational if moving is free, but not if each move costs a point (it then walks back and forth forever).

**PEAS** describes a task: **P**erformance measure, **E**nvironment, **A**ctuators, **S**ensors. For a delivery drone: P = on-time undamaged parcels, safety, battery use; E = city airspace, weather, buildings; A = rotors, winch; S = GPS, cameras, lidar, IMU.

**Seven environment properties:**

| Property | Easy value | Hard value |
|---|---|---|
| Observable | fully | partially |
| Agents | single | multi |
| Deterministic | deterministic | stochastic |
| Episodic | episodic | sequential |
| Static | static | dynamic |
| Discrete | discrete | continuous |
| Known | known | unknown |

The 8-puzzle and crosswords are easy on every axis; taxi driving is hard on every axis.

**Five agent types:**

| Type | Decides using | Weakness |
|---|---|---|
| Simple reflex | current percept + condition-action rules | no memory; loops |
| Model-based reflex | internal state updated by a transition and sensor model | no lookahead |
| Goal-based | search/planning towards an explicit goal | goal is yes/no only |
| Utility-based | maximise expected utility $U(s)$ | needs probabilities and utilities |
| Learning | any of the above, improved by experience | needs exploration |

In the notebook's 6 × 6 vacuum world, the average scores rose with each step: -24.5, 31.5, 38.6, 44.6, and the learning agent climbed from 38.0 to 42.6 as it discovered the dirty kitchen.

**Types of AI.** By capability: **narrow AI (ANI)** does specific tasks and is the only kind that exists (including today's LLMs); **AGI** and **ASI** are hypothetical. By functionality: **reactive machines** and **limited memory** systems exist; **theory of mind** and **self-aware** AI do not.

## 3. Problem Formulation

A **search problem** has five parts: **initial state**, **actions** $\text{ACTIONS}(s)$, **transition model** $\text{RESULT}(s, a)$, **goal test**, and **path cost** (the sum of step costs). Choosing what to leave out is **abstraction**.

The **state-space graph** has one node per state and is a property of the problem. A **search tree** is what an algorithm builds; each tree node stands for a *path*, so one state can appear many times, and a graph with a cycle gives an infinite tree. On a 4-state graph with a cycle, the tree had 2,629 nodes at depth 8; on an open grid, 65,536 paths of length 8 visit only 145 distinct squares.

| Problem | State | Reachable states | Shortest solution |
|---|---|---|---|
| 8-puzzle | tuple of 9 tiles | $9!/2 = 181{,}440$ | up to 31 moves |
| Route finding (12 towns) | current town | 12 | 141 km |
| Missionaries & cannibals | $(m, c, b)$ | 16 safe | 11 crossings |
| Water jug (4 L and 3 L) | $(x, y)$ | 14 of 20 | 6 actions |

**Branching factor** $b$ = number of successors; the 8-puzzle has 2 to 4 (about 2.7 on average).

## 4. Uninformed Search (notebook 02)

A **node** stores a state, a parent pointer, the action and the path cost $g(n)$. The **frontier** holds generated but unexpanded nodes; **expanding** a node generates its children. **Tree search** keeps no memory of visited states; **graph search** keeps a **reached (explored) set** and never expands a state twice. The frontier's data structure *is* the strategy.

| Strategy | Frontier | Expands next |
|---|---|---|
| Breadth-first (BFS) | FIFO queue | shallowest node |
| Depth-first (DFS) | LIFO stack | deepest node |
| Depth-limited (DLS) | stack, depth $\le \ell$ | deepest node within the limit |
| Iterative deepening (IDS) | DLS with $\ell = 0, 1, 2, \dots$ | deepest within the current limit |
| Uniform-cost (UCS, Dijkstra) | priority queue on $g$ | cheapest path so far |
| Bidirectional | two frontiers | from start and from goal |

**Notation:** $b$ branching factor, $d$ depth of the shallowest goal, $m$ maximum depth, $\ell$ depth limit, $C^*$ optimal cost, $\epsilon$ smallest step cost.

| Criterion | BFS | UCS | DFS | DLS | IDS | Bidirectional |
|---|---|---|---|---|---|---|
| Complete? | yes¹ | yes¹² | no | no | yes¹ | yes¹⁴ |
| Optimal? | yes³ | yes | no | no | yes³ | yes³⁴ |
| Time | $O(b^d)$ | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | $O(b^m)$ | $O(b^\ell)$ | $O(b^d)$ | $O(b^{d/2})$ |
| Space | $O(b^d)$ | $O(b^{1+\lfloor C^*/\epsilon\rfloor})$ | $O(bm)$ | $O(b\ell)$ | $O(bd)$ | $O(b^{d/2})$ |

¹ if $b$ is finite and a solution exists (or the space is finite); ² if every step cost $\ge \epsilon > 0$; ³ if all step costs are equal; ⁴ if both directions are BFS or UCS.

**Why IDS is cheap.** IDS regenerates shallow levels, but most nodes are at the bottom: $N_{IDS} = d\,b + (d-1)\,b^2 + \dots + 1 \cdot b^d$. For $b = 10$, $d = 5$: $50 + 400 + 3{,}000 + 20{,}000 + 100{,}000 = 123{,}450$, against BFS's $10 + 100 + 1{,}000 + 10{,}000 + 100{,}000 = 111{,}110$: only 11% more, with $O(bd)$ memory. The overhead tends to $b/(b-1)$. Caution: on graphs with many loops (the notebook's maze), tree-like IDS re-expands states once per path and exploded to 243,596 expansions where BFS needed 221.

**UCS worked example.** From Ashford, UCS pops Ashford:0, Brookvale:26, Cedar Falls:28, Dunmore:51, Elmstead:52 and so on, always the cheapest. Lakeside first enters the frontier at **172 km** (via Harborview), but UCS waits until Lakeside is the cheapest item on the queue and returns **141 km** (via Glenwood and Kingsport). That is why the goal test must happen on **expansion**, not generation.

**Bidirectional search** runs two searches of depth $d/2$: for $b = 10$, $d = 6$, that is $2 \times 10^3 = 2{,}000$ nodes against $10^6$. It needs reversible actions (or predecessors) and an explicit goal state.

## 5. Informed (Heuristic) Search (notebook 03)

A **heuristic** $h(n)$ estimates the cost from $n$ to the nearest goal; $h^*(n)$ is the true cost. **Best-first search** expands the node with the lowest $f(n)$:

| Algorithm | $f(n)$ | Optimal? |
|---|---|---|
| UCS | $g(n)$ | yes |
| Greedy best-first | $h(n)$ | no |
| A\* | $g(n) + h(n)$ | yes, if $h$ admissible |
| Weighted A\* | $g(n) + w\,h(n)$, $w > 1$ | cost $\le w \cdot C^*$ |

**Admissible:** $h(n) \le h^*(n)$ for every $n$ (never overestimates). **Consistent (monotone):** $h(n) \le c(n, a, n') + h(n')$ for every edge (a triangle inequality), with $h(\text{goal}) = 0$.

- *Consistent implies admissible:* by induction on the number of steps to the goal: $h(n) \le c(n, n') + h(n') \le c(n, n') + h^*(n') = h^*(n)$ along an optimal path.
- *A\* with admissible $h$ is optimal:* suppose A\* returned a goal $G_2$ with $g(G_2) > C^*$. Some node $n$ on an optimal path is still on the frontier, with $f(n) = g(n) + h(n) \le g(n) + h^*(n) = C^* < f(G_2)$. A\* would have expanded $n$ before $G_2$: contradiction.
- *With consistent $h$*, $f$ never decreases along a path, so the first expansion of every state is via its cheapest path and graph search never needs to re-open a state. With an admissible but inconsistent $h$, a closed list that never re-opens can return a wrong answer (cost 7 instead of 5 in the notebook's counter-example).

**Greedy vs A\* on the map.** At Elmstead, Juniper looked 52.0 km from Lakeside and Glenwood 52.2 km. Greedy took Juniper and paid 149 km. A\* expanded nodes in order of $f$ (Ashford 109.6, Cedar Falls 115.1, Elmstead 118.0, ..., Lakeside 141.0) and returned the optimal 141 km.

**Heuristics for the 8-puzzle.** $h_1$ = number of misplaced tiles; $h_2$ = sum of Manhattan distances of tiles from their goal squares. Both are admissible and consistent (checked on all 181,440 states). Since $h_2 \ge h_1$ everywhere, $h_2$ **dominates** $h_1$, and A\* with $h_2$ never expands more nodes. On one 20-move puzzle: UCS expanded 61,768, A\*($h_1$) 2,760 and A\*($h_2$) 169. Heuristics come from **relaxed problems**: if a tile could move anywhere, the cost is $h_1$; if it could move to any adjacent square, the cost is $h_2$. The $\max$ of several admissible heuristics is admissible and dominates each of them.

**Solvability.** An **inversion** is a pair of tiles in the wrong order when read row by row (ignoring the blank). On a 3 × 3 board a layout is solvable iff its number of inversions is even, so exactly half of the $9! = 362{,}880$ layouts are solvable.

**Effective branching factor** $b^*$: if A\* generates $N$ nodes for a solution at depth $d$, then $N + 1 = 1 + b^* + (b^*)^2 + \dots + (b^*)^d$. For $N = 52$, $d = 5$: $b^* \approx 1.92$. Closer to 1 means a better heuristic.

**Memory-bounded variants.**

| Algorithm | Idea | Memory | Optimal? |
|---|---|---|---|
| IDA\* | DFS with an $f$-cutoff, raised to the smallest $f$ that exceeded it | $O(bd)$ | yes (admissible $h$) |
| RBFS | best-first using linear space, remembers the best alternative $f$ | $O(bd)$ | yes |
| SMA\* | A\* that drops the worst leaf when memory is full | as much as given | yes, if the solution fits |
| Beam search | keep only the best $k$ nodes per level | $O(kd)$ | no, and incomplete |

On 24-move 8-puzzles, A\* stored about 1,677 nodes on average while IDA\* stored a path of 25, at the cost of about 3× more expansions.

## 6. Local Search and Optimization (notebook 04)

When only the final state matters (8-queens, a timetable, a TSP tour), **local search** keeps one or a few **complete** states and moves to **neighbours**. It uses $O(1)$ memory and works on huge spaces, but is usually neither complete nor optimal.

The **state-space landscape** plots the **objective function** (to maximise) or **cost** (to minimise) over states. Traps: **local maxima**, **plateaus** (flat areas), **shoulders** (flat areas that later rise), and **ridges** (a rising crest that every allowed move steps off).

**8-queens, complete-state formulation:** one queen per column, state = row of each queen; $8^8 = 16{,}777{,}216$ states, each with $8 \times 7 = 56$ neighbours; cost $h$ = number of attacking pairs.

| Method | Rule | Notebook result on 8-queens |
|---|---|---|
| Steepest-ascent hill climbing | move to the best neighbour if strictly better | 16.5% solved (AIMA: 14%) |
| + sideways moves (limit 100) | also accept equal neighbours | 95.5% (AIMA: 94%) |
| First-choice / stochastic | first better neighbour / random uphill neighbour | 15% / 12% |
| Random-restart | restart until solved; expected $1/p$ runs | 100% |
| Simulated annealing | accept worse moves with probability $e^{\Delta E/T}$ | solves nearly all |
| Local beam ($k$ states) | keep the best $k$ of all successors | solves nearly all |
| Genetic algorithm | selection, crossover, mutation over a population | solves nearly all |
| Tabu search | best non-tabu neighbour, even if worse | solves nearly all |

**Simulated annealing** (Kirkpatrick, Gelatt & Vecchi, 1983): pick a random neighbour; if it is better, take it; if it is worse by $\Delta E < 0$, take it with probability $e^{\Delta E / T}$. For $\Delta E = -2$: at $T = 10$, $e^{-0.2} = 0.819$; at $T = 1$, $e^{-2} = 0.135$; at $T = 0.1$, $e^{-20} \approx 2 \times 10^{-9}$. High $T$ explores, low $T$ exploits. The usual schedule is geometric, $T_t = T_0 \alpha^t$ with $\alpha$ just below 1.

**Local beam search** is not $k$ independent restarts: all $k$ states share one pool of successors, so effort flows to promising regions. **Stochastic beam search** samples the $k$ survivors in proportion to quality. **LLM beam search** applies the same "keep the best $k$" idea to partial sentences: in the notebook, greedy decoding found "The cat sat" (probability $0.5 \times 0.4 \times 0.5 = 0.1$) while beam $k = 2$ found "A dog barked" ($0.4 \times 0.9 \times 0.6 = 0.216$).

**Genetic algorithm** (Holland, 1975): encode a state as a string; **fitness** (e.g. 28 minus the attacking pairs); **selection** proportional to fitness; **crossover** cuts two parents and swaps tails; **mutation** changes a random gene with small probability. Without mutation the population can only recombine genes it already has.

**TSP:** a 15-city tour has $(n-1)!/2 = 14!/2 \approx 4.4 \times 10^{10}$ possibilities. The exact Held-Karp dynamic programme costs $O(n^2 2^n)$; **2-opt** (reverse a segment to remove crossings) is the standard local move. A single 2-opt climb was up to 3.75% above optimum; 10 random restarts found the optimum every time.

**Gradient descent** is steepest-ascent hill climbing in continuous space: $\mathbf{x} \leftarrow \mathbf{x} - \alpha \nabla f(\mathbf{x})$ to minimise. In very high dimensions most stationary points are saddle points rather than bad local minima, which is one reason it works so well for deep learning.

## 7. Adversarial Search and Games (notebook 05)

A two-player, **zero-sum**, **perfect-information** game is defined by $S_0$, TO-MOVE$(s)$, ACTIONS$(s)$, RESULT$(s, a)$, IS-TERMINAL$(s)$ and UTILITY$(s, p)$. Zero-sum means one number describes the outcome for both players.

**Minimax** assumes both sides play perfectly:

$$\text{MINIMAX}(s) = \begin{cases} \text{UTILITY}(s) & \text{terminal} \\ \max_a \text{MINIMAX}(\text{RESULT}(s,a)) & \text{MAX to move} \\ \min_a \text{MINIMAX}(\text{RESULT}(s,a)) & \text{MIN to move} \end{cases}$$

Time $O(b^m)$, space $O(bm)$. *Worked example (AIMA Fig. 5.2):* MIN node B has leaves 3, 12, 8, so $B = 3$; C has 2, 4, 6, so $C = 2$; D has 14, 5, 2, so $D = 2$; root $= \max(3, 2, 2) = 3$. Tic-tac-toe has 549,946 tree nodes, 255,168 complete games and 5,478 distinct positions; its minimax value is 0 (a draw).

**Alpha-beta pruning.** $\alpha$ = best value MAX can already guarantee on the path (starts at $-\infty$); $\beta$ = best value MIN can guarantee (starts at $+\infty$). Prune a node's remaining children as soon as $\alpha \ge \beta$. In the example, after B the root has $\alpha = 3$; C's first leaf 2 makes $C \le 2 \le \alpha$, so C's other two leaves are pruned. The root value is unchanged. With perfect move ordering alpha-beta examines $b^{\lceil d/2 \rceil} + b^{\lfloor d/2 \rfloor} - 1$ leaves (Knuth & Moore, 1975): for $b = 4$, $d = 6$, that is 127 instead of 4,096. So the time becomes about $O(b^{m/2})$ (about $O(b^{3m/4})$ with random ordering), and the program can search about twice as deep. On tic-tac-toe, alpha-beta visited 18,297 nodes in natural order, 7,275 with centre-first ordering and 2,312 with perfect ordering.

**Depth limits.** Real games are too deep, so search is cut off and leaves are scored by an **evaluation function** EVAL$(s)$, usually a weighted sum of features (Shannon, 1950). Problems and fixes: the **horizon effect** (a disaster pushed just beyond the cutoff) is reduced by **quiescence search**; **iterative deepening** gives good move ordering and an anytime answer; **transposition tables** cache repeated positions.

**Expectimax** adds **chance nodes** whose value is the probability-weighted average: $\text{value}(c) = \sum_r P(r)\,\text{value}(\text{child}_r)$. Unlike minimax, its decisions change under order-preserving rescaling of the utilities, so the evaluation must be proportional to expected payoff.

**Monte Carlo Tree Search** (Coulom 2006; UCT by Kocsis & Szepesvári 2006) repeats four steps: **selection** (descend by UCB1), **expansion** (add a child), **simulation** (random playout to the end), **back-propagation** (update win counts). UCB1 picks the child maximising

$$\frac{U(n)}{N(n)} + C\sqrt{\frac{\ln N(\text{parent})}{N(n)}}$$

(exploitation plus exploration, $C \approx \sqrt{2}$). MCTS needs no evaluation function and converges to minimax. Deep Blue (1997) was alpha-beta on custom hardware; AlphaGo (2016), AlphaGo Zero (2017), AlphaZero (2017/2018) and MuZero (2019/2020) are MCTS guided by neural networks trained by self-play.

## 8. Constraint Satisfaction Problems (notebook 06)

A **CSP** has **variables** $X_1..X_n$, **domains** $D_i$ and **constraints** (a scope plus allowed combinations). Constraints are **unary** (one variable), **binary** (two), **global** (e.g. Alldiff over a Sudoku row) or **soft** (preferences). A **solution** is a **complete** and **consistent** assignment. The **constraint graph** links variables that share a constraint.

**Backtracking search** assigns one variable at a time and undoes the last choice when a constraint breaks: complete, worst case $O(d^n)$, $O(n)$ space. Heuristics:

- **MRV** (minimum remaining values, "fail first"): pick the variable with the fewest legal values.
- **Degree heuristic**: break ties by the variable in most constraints with unassigned variables.
- **LCV** (least-constraining value, "fail last"): try the value that rules out the fewest options for neighbours.

Every variable must be assigned, so failing early saves work; but only one value needs to work, so try the most promising first.

**Inference.** **Forward checking** deletes inconsistent values from unassigned neighbours after each assignment. **Arc consistency**: arc $X_i \to X_j$ is consistent if every value in $D_i$ has some support in $D_j$. **AC-3** (Mackworth, 1977) queues all arcs, revises each, and re-queues arcs into any variable whose domain shrank; it costs $O(c\,d^3)$ for $c$ binary constraints. **MAC** runs AC-3 after every assignment.

*Worked example (Australia, colours R, G, B):*

| Step | WA | NT | SA | Q | NSW | V | T |
|---|---|---|---|---|---|---|---|
| start | RGB | RGB | RGB | RGB | RGB | RGB | RGB |
| WA = R, forward check | R | GB | GB | RGB | RGB | RGB | RGB |
| Q = G, forward check | R | B | B | G | RB | RGB | RGB |

Forward checking sees no empty domain, but NT and SA are neighbours that can both only be blue. AC-3 revises NT → SA, deletes blue from NT, and detects the failure immediately.

**Results.** Australia has $3^7 = 2{,}187$ colourings and 18 solutions. With a bad variable order plain backtracking needed 41 assignments and 34 backtracks; MRV needed 7 and 0. On the "hard" Sudoku, MAC + MRV + LCV used the fewest assignments (3,730). Arc consistency alone solved the easy Sudoku with no search.

**Min-conflicts** (Minton et al., 1992): start from a complete assignment, repeatedly pick a conflicted variable and give it the value with the fewest conflicts. From a greedy start it solved 1,000-queens in 8 steps and 10,000-queens in 51.

**Tree-structured CSPs** are solvable in $O(n d^2)$: order variables topologically, make each parent arc-consistent with its child from the leaves upward, then assign from the root downward without backtracking. **Cutset conditioning** assigns a small set of variables (SA in Australia) so that the rest becomes a tree.

| Method | Complete? | Worst time | Best for |
|---|---|---|---|
| Backtracking (+ MRV, LCV) | yes | $O(d^n)$ | small and medium problems |
| + forward checking / MAC | yes | $O(d^n)$, far less in practice | Sudoku, scheduling |
| AC-3 alone | no | $O(c\,d^3)$ | preprocessing |
| Min-conflicts | no | often near-constant steps | huge problems with many solutions |
| Tree algorithm | yes (trees) | $O(n d^2)$ | tree-shaped graphs |

## 9. Knowledge Representation and Logic (notebook 07)

A **knowledge-based agent** keeps a **knowledge base (KB)**, **TELL**s it observations and **ASK**s it questions. Knowledge is **declarative** (facts) rather than **procedural** (code). Structured representation schemes:

| Scheme | Core idea | Modern descendant |
|---|---|---|
| Semantic network | nodes + labelled edges (is-a, part-of) with inheritance | knowledge graphs |
| Frame | object with slots, defaults, inheritance, if-needed procedures | object-oriented classes |
| Ontology | classes, properties, subClassOf, constraints | RDF/OWL, schema.org, Wikidata |
| Production rules | IF conditions THEN action, match-resolve-act | business rule engines |

**Propositional logic.** Sentences are built from symbols with $\lnot, \land, \lor, \Rightarrow, \Leftrightarrow$ (precedence in that order). A **model** assigns True/False to every symbol. $P \Rightarrow Q$ is false only when $P$ is true and $Q$ false.

- **Valid:** true in every model ($P \lor \lnot P$). **Satisfiable:** true in some model. **Unsatisfiable:** true in none ($P \land \lnot P$).
- **Entailment** $KB \models \alpha$: $\alpha$ is true in every model of the KB. Key theorem: $KB \models \alpha$ iff $KB \Rightarrow \alpha$ is valid iff $KB \land \lnot \alpha$ is unsatisfiable.
- **Model checking** (TT-ENTAILS) enumerates all $2^n$ models: sound and complete, $O(2^n)$.

**Equivalences and CNF.** Useful laws: contraposition $A \Rightarrow B \equiv \lnot B \Rightarrow \lnot A$ (but the converse $B \Rightarrow A$ is *not* equivalent), implication elimination $A \Rightarrow B \equiv \lnot A \lor B$, De Morgan, distributivity. **CNF** (conjunctive normal form) is an AND of **clauses**, each an OR of literals. Conversion: eliminate $\Leftrightarrow$ and $\Rightarrow$, move $\lnot$ inwards, distribute $\lor$ over $\land$. Worked: $B_{11} \Leftrightarrow (P_{12} \lor P_{21})$ becomes $(\lnot B_{11} \lor P_{12} \lor P_{21}) \land (\lnot P_{12} \lor B_{11}) \land (\lnot P_{21} \lor B_{11})$. Distribution can blow up exponentially; the Tseitin transformation avoids that with new symbols.

**Resolution.** From $(\ell \lor A)$ and $(\lnot \ell \lor B)$ infer $(A \lor B)$. To prove $\alpha$, add $\lnot \alpha$ and derive the **empty clause** $\square$. *Worked:* KB = the CNF above plus $\lnot B_{11}$; query $\lnot P_{12}$, so add $P_{12}$. Resolve $(\lnot P_{12} \lor B_{11})$ with $P_{12}$ to get $B_{11}$; resolve $B_{11}$ with $\lnot B_{11}$ to get $\square$. So $KB \models \lnot P_{12}$. Resolution is refutation-complete but can generate exponentially many clauses.

**Horn clauses** have at most one positive literal; **definite clauses** exactly one, i.e. $(L_1 \land \dots \land L_k) \Rightarrow H$. For them **forward chaining** (data-driven; each rule keeps a count of unsatisfied premises) and **backward chaining** (goal-driven, depth-first, with a loop check) run in time linear in the KB size. *Worked:* rules $P \Rightarrow Q$, $L \land M \Rightarrow P$, $B \land L \Rightarrow M$, $A \land P \Rightarrow L$, $A \land B \Rightarrow L$ with facts $A, B$: forward chaining derives $L$, then $M$, then $P$, then $Q$.

**SAT solvers.** SAT was the first problem proved NP-complete (Cook, 1971). **DPLL** (1962) is backtracking with early termination, **pure symbols** and **unit propagation**; modern **CDCL** solvers add clause learning. **WalkSAT** is local search: flip a variable in a random unsatisfied clause, sometimes randomly, sometimes greedily; it can find models but never proves unsatisfiability. Random 3-SAT switches from almost-always satisfiable to almost-never near $m/n \approx 4.27$ clauses per variable, where instances are hardest.

**Wumpus world.** From "no breeze in [1,1]", "breeze in [2,1]", "stench but no breeze in [1,2]", the agent proved [2,2] safe, a pit in [3,1] and the wumpus in [1,3], checked by both DPLL and the truth table (262,144 models).

**First-order logic (FOL)** adds **objects**, **predicates**, **functions** and **quantifiers**. Rule of thumb: $\forall$ pairs with $\Rightarrow$, $\exists$ pairs with $\land$. "All students are smart": $\forall x\, \text{Student}(x) \Rightarrow \text{Smart}(x)$. Quantifier order matters: $\forall x \exists y\, \text{Loves}(x, y)$ (everybody loves somebody) differs from $\exists y \forall x\, \text{Loves}(x, y)$ (someone is loved by everybody).

**Unification** finds a substitution $\theta$ that makes two expressions identical. $\text{UNIFY}(\text{Knows}(John, x), \text{Knows}(y, \text{Mother}(y))) = \{y/John,\ x/\text{Mother}(John)\}$. The **occurs check** refuses to bind $y$ to a term containing $y$ (e.g. $F(G(y))$). **Generalized modus ponens** applies a lifted rule to matching facts; forward chaining with it derived Criminal(West) in the classic crime example, and Prolog-style backward chaining (depth-first, left to right, variables standardised apart) found the same answer. Left-recursive rules make Prolog loop forever even when the KB is correct. FOL **resolution** (Robinson, 1965) needs CNF with **Skolemization** (replace $\exists$ by new constants or functions); it is refutation-complete, and FOL entailment is **semi-decidable** (a proof is found if one exists, but the search may never stop otherwise).

**Limits of logic:** uncertainty, the **qualification problem** (rules have endless exceptions), the **frame problem** (stating what an action does not change), monotonicity, computational cost, and the **knowledge acquisition bottleneck** (experts' knowledge is slow and expensive to type in). Machine learning attacks the last one by learning from data.

| Algorithm | Complete for | Worst time |
|---|---|---|
| TT-ENTAILS | all propositional KBs | $O(2^n)$ |
| Resolution | all (refutation) | exponential |
| Forward/backward chaining | Horn/definite clauses | linear |
| DPLL / CDCL | all propositional KBs | $O(2^n)$, fast in practice |
| WalkSAT | none (incomplete) | bounded by flips |

## 10. Reasoning and Planning (notebook 08)

| Reasoning type | From → to | Guaranteed? | Example |
|---|---|---|---|
| Deductive | general rules + facts → consequences | yes (sound) | all humans are mortal; Socrates is human; so Socrates is mortal |
| Inductive | examples → general rule | no | Find-S learned "Sunny ∧ Warm ∧ Strong wind ⇒ EnjoySport" |
| Abductive | observation → best explanation | no | no crank + dim lights → dead battery |
| Analogical | known base → new target | no | atom as a solar system |
| Common-sense | background knowledge → everyday conclusions | no | "the trophy doesn't fit in the suitcase because it is too big": it = trophy |

Two invalid look-alikes of deduction: **affirming the consequent** ($A \Rightarrow B$, $B$, so $A$) and **denying the antecedent** ($A \Rightarrow B$, $\lnot A$, so $\lnot B$). Abduction is defeasible: when the lights are fine and the radio works, the faulty starter becomes the best explanation instead.

**Monotonic vs non-monotonic.** In classical logic, adding facts never removes conclusions; adding "Tweety is a penguin" to "birds fly" makes the KB inconsistent. **Non-monotonic** reasoning lets new facts withdraw conclusions: **default logic** (Reiter, 1980), **circumscription** (McCarthy, 1980), and **negation as failure** under the **closed-world assumption** (Prolog, databases). The more specific default (penguins do not fly) beats the general one.

**Classical planning (STRIPS/PDDL).** A state is a set of ground facts (closed world). An action schema has **parameters**, **preconditions**, an **add list** and a **delete list**:

$$\text{RESULT}(s, a) = (s - \text{DEL}(a)) \cup \text{ADD}(a)$$

and everything else stays the same (the **STRIPS assumption**, which sidesteps the frame problem). STRIPS dates from Fikes & Nilsson (1971); **PDDL** (1998) is the standard text format used in planning competitions.

- **Forward (progression) planning** searches states from the initial state with BFS or A\*.
- **Backward (regression) planning** starts from the goal and regresses through relevant actions: before stack$(a, b)$ we need holding$(a)$ and clear$(b)$. State invariants prune impossible goal sets (1,082 expanded without them, 13 with them).
- **Domain-independent heuristics** come from relaxations. Ignore delete lists: $h_{max}$ (cost of the most expensive goal fact, admissible) and $h_{add}$ (sum of costs, more informative but not admissible). At the Sussman start: goal count 2, $h_{max} = 3$, $h_{add} = 5$, true optimum 6.

**Sussman anomaly** (1975): with C on A and B on the table, goals on(A, B) and on(B, C) interfere whichever is achieved first, so a planner that solves one goal at a time and never undoes it fails. The optimal 6-step plan interleaves them: unstack(C, A), put-down(C), pick-up(B), stack(B, C), pick-up(A), stack(A, B).

**Other planners.** **Partial-order planning (POP)** keeps only necessary orderings: socks before shoes, left and right independent, so one partial plan stands for 6 linear plans. **GraphPlan** (Blum & Furst) builds alternating fact and action layers with **mutex** links and extracts a plan backwards. **HTN** planning decomposes compound tasks with expert-written methods (walk, taxi or train, depending on distance and cash).

**Planning vs search vs RL:** search treats states as black boxes; planning uses the factored structure of states and actions to derive heuristics automatically; reinforcement learning learns what to do when the model is unknown. **Execution monitoring and replanning** (check preconditions in the real state before each action; replan when they fail) is the classical ancestor of plan-and-execute LLM agents.

## 11. Uncertain Knowledge and Reasoning (notebook 09)

Logic fails where rules have endless exceptions; probability summarises **laziness** (too many exceptions to list) and **ignorance** (missing theory or facts). Basics: $P(a \mid b) = P(a \land b)/P(b)$; product rule $P(a \land b) = P(a \mid b)P(b)$; **marginalisation** $P(a) = \sum_b P(a, b)$; **normalisation** $\alpha$ rescales a vector to sum to 1.

**Full joint distribution.** With the dentist table (Toothache, Catch, Cavity): $P(\text{cavity}) = 0.2$, $P(\text{cavity} \lor \text{toothache}) = 0.28$, $P(\text{cavity} \mid \text{toothache}) = 0.12/0.2 = 0.6$, rising to 0.871 if the probe also catches. With $n$ Boolean variables the table has $2^n$ rows.

**Independence:** $P(a, b) = P(a)P(b)$. **Conditional independence:** $P(a, b \mid c) = P(a \mid c)P(b \mid c)$. Toothache and Catch are dependent, but independent given Cavity. One cause with $n - 1$ conditionally independent effects needs $2n - 1$ numbers instead of $2^n - 1$: exponential to linear.

**Bayes' rule:**

$$P(\text{cause} \mid \text{effect}) = \frac{P(\text{effect} \mid \text{cause})\,P(\text{cause})}{P(\text{effect})}$$

*Worked:* prevalence 1%, sensitivity 90%, false-positive rate 9%: $P(\text{sick} \mid +) = \frac{0.9 \times 0.01}{0.9 \times 0.01 + 0.09 \times 0.99} = \frac{0.009}{0.0981} \approx 0.092$. Ignoring the prior is the **base-rate fallacy**. A second independent positive gives about 0.50.

**Naive Bayes** assumes effects are conditionally independent given the cause: $P(C \mid e_1..e_n) = \alpha\, P(C) \prod_i P(e_i \mid C)$.

**Bayesian networks.** A **DAG** plus a **conditional probability table (CPT)** per node, giving

$$P(x_1, \dots, x_n) = \prod_i P(x_i \mid \text{parents}(X_i)).$$

*Worked (burglary network):* $P(B) = 0.001$, $P(E) = 0.002$, $P(A \mid \lnot b, \lnot e) = 0.001$, $P(J \mid a) = 0.90$, $P(M \mid a) = 0.70$. Then $P(j, m, a, \lnot b, \lnot e) = 0.90 \times 0.70 \times 0.001 \times 0.999 \times 0.998 \approx 0.000628$. The whole network needs 10 numbers instead of 31. Inference gives $P(\text{burglary} \mid j, m) \approx 0.284$.

**d-separation.** In a **chain** $X \to Z \to Y$ or a **fork** $X \leftarrow Z \to Y$, observing $Z$ blocks the path. In a **collider** $X \to Z \leftarrow Y$, the path is blocked *unless* $Z$ or a descendant is observed. That is **explaining away**: $P(b) = 0.001$, $P(b \mid a) = 0.374$, but $P(b \mid a, e) = 0.003$ once the earthquake explains the alarm.

**Inference.** **Enumeration** sums the chain-rule product over hidden variables: $O(2^n)$ time, $O(n)$ space. **Variable elimination** does the sums inside out and stores **factors** (dynamic programming); its cost depends on the elimination order, and exact inference is NP-hard in general. **Sampling** estimates with error shrinking like $1/\sqrt{N}$:

| Sampler | Idea | Weakness |
|---|---|---|
| Prior | sample every variable top-down | ignores evidence |
| Rejection | discard samples that contradict the evidence | wastes almost all samples for rare evidence (kept 0.2%) |
| Likelihood weighting | fix evidence, weight by its likelihood | weights degenerate |
| Gibbs (MCMC) | resample one variable from its Markov blanket | slow mixing |

**Temporal models.** A **Markov chain** assumes $P(X_t \mid X_{0:t-1}) = P(X_t \mid X_{t-1})$. An **HMM** adds a hidden state and a sensor model $P(E_t \mid X_t)$. **Filtering** (forward algorithm): predict $P(X_{t+1} \mid e_{1:t}) = \sum_{x_t} P(X_{t+1} \mid x_t) P(x_t \mid e_{1:t})$, then update with $\alpha\, P(e_{t+1} \mid X_{t+1})$. *Worked (umbrella world, stay-probability 0.7, $P(u \mid r) = 0.9$, $P(u \mid \lnot r) = 0.2$, prior 0.5):* day 1 with an umbrella: $\alpha\langle 0.9 \times 0.5,\ 0.2 \times 0.5\rangle = \langle 0.818, 0.182\rangle$. Day 2: predict $0.818 \times 0.7 + 0.182 \times 0.3 = 0.627$; update $\alpha\langle 0.9 \times 0.627,\ 0.2 \times 0.373\rangle = \langle 0.883, 0.117\rangle$. **Smoothing** (forward-backward) revises past days with later evidence; **Viterbi** finds the most likely whole sequence. All three cost $O(t S^2)$. The **Kalman filter** is the same idea for linear-Gaussian continuous states.

**Alternatives (historical).** **Dempster-Shafer theory** gives belief and plausibility intervals and behaves strangely under strong conflict. **Certainty factors** (MYCIN) were a fast but inconsistent approximation; both were largely replaced by Bayesian networks.

**Decision theory.** Choose the action with maximum **expected utility** $EU(a \mid e) = \sum_{s'} P(s' \mid a, e)\,U(s')$. The **value of information** is the expected gain from observing before deciding; it is never negative, and it is zero if no possible observation would change the decision. In the notebook's umbrella decision, EU was 73 without information, 85 with an 80%-accurate forecast (value 12) and 94 with perfect information (value 21). An **MDP** (states, actions, $P(s' \mid s, a)$, rewards, discount $\gamma$) extends this to sequences of decisions, solved by **value iteration** with the Bellman equation $U(s) = \max_a \sum_{s'} P(s' \mid s, a)\,[R(s, a, s') + \gamma U(s')]$. When the model is unknown, the agent must learn: that is reinforcement learning.

## 12. Fuzzy Logic and Expert Systems (notebook 10)

**Fuzzy sets** (Zadeh, 1965) model **vagueness** with a membership function $\mu_A : X \to [0, 1]$. A crisp "tall ≥ 180 cm" flips at one centimetre; a fuzzy "tall" gives 0.70 at 179 cm and 0.80 at 181 cm. Fuzziness is about **degrees of truth**; probability is about **degrees of belief**.

**Membership functions:** triangular $\mu(x) = \max(\min(\frac{x-a}{b-a}, \frac{c-x}{c-b}), 0)$; trapezoidal; Gaussian $e^{-(x-c)^2/(2\sigma^2)}$. Example: triangle $(2, 5, 8)$ at $x = 4$ gives $\min(2/3, 4/3) = 0.667$. A **linguistic variable** (temperature) has a universe (0 to 40 °C) and overlapping terms (cold, warm, hot); at 27 °C, warm = 0.125 and hot = 0.625 (degrees need not sum to 1). **Hedges**: very $= \mu^2$, somewhat $= \sqrt{\mu}$, not $= 1 - \mu$.

**Operators.** NOT $= 1 - \mu$. AND is a **t-norm**, OR its dual **t-conorm**. For $a = 0.7$, $b = 0.6$:

| Pair | AND $T(a, b)$ | OR $S(a, b)$ |
|---|---|---|
| min / max (Zadeh) | 0.60 | 0.70 |
| product / probabilistic sum | 0.42 | 0.88 |
| Łukasiewicz $\max(0, a+b-1)$ / $\min(1, a+b)$ | 0.30 | 1.00 |
| drastic | 0.00 | 1.00 |

**Mamdani inference** (Mamdani & Assilian, 1975) in four steps: (1) **fuzzify** crisp inputs; (2) compute each rule's **firing strength** (AND = min) and **clip** its output set at that height; (3) **aggregate** the clipped sets with max; (4) **defuzzify**, usually by the **centroid** $z^* = \int z\,\mu(z)\,dz / \int \mu(z)\,dz$, or by mean of maximum. *Worked (tipping):* service 3 is poor 0.135 and good 0.411; food 8 is delicious 0.5. Rules fire cheap 0.135, average 0.411, generous 0.5; the centroid tip is about 18.0%, mean of maximum 25%. The centroid gives a smooth **control surface** (about 5% to 25%); mean of maximum gives jumps. **Sugeno (TSK, 1985)** uses constants or linear functions as outputs and a weighted average $z = \sum_i w_i z_i / \sum_i w_i$: faster and smooth, with no integration.

**Expert systems** have a **knowledge base** (rules), **working memory** (facts of the current case), an **inference engine** and an **explanation facility**. **Forward chaining** cycles match → conflict resolution → act. **Conflict resolution** strategies: **refraction** (a rule fires once per match), **salience** (priority, e.g. safety rules first), **specificity** (more conditions win) and **recency** (newest facts win). Pure rule order lost important advice in the notebook ("jump-start the car" beat "replace the old battery"); specificity fixed it. **Backward chaining** asks the user only what the current goal needs, so it can answer **WHY** a question is asked; **HOW** explanations replay the proof tree.

**Certainty factors** (MYCIN, 1970s) range over $[-1, 1]$. Conclusion CF = rule CF × min of premise CFs. Combine two positives with $CF_1 + CF_2(1 - CF_1)$; opposite signs with $(CF_1 + CF_2)/(1 - \min(|CF_1|, |CF_2|))$. *Worked:* $0.48 + 0.30 \times 0.52 = 0.636$; adding $-0.15$ gives $(0.636 - 0.15)/(1 - 0.15) \approx 0.572$.

**Where they live today:** fuzzy controllers in appliances, cameras and trains; rule engines in banking, insurance, tax and compliance, where auditability matters more than flexibility.

## 13. Putting It Together: The Industry Project (notebook 11)

The delivery-company project combines sections 4 to 8 into a production-style pipeline:

```
raw roads + orders --> clean & validate --> road graph
   --> Dijkstra vs A* --> travel-time matrix --> nearest neighbour --> 2-opt --> report
drivers + rules --> CSP (backtracking + MRV + forward checking) --> independent validator --> report
```

- **Admissibility from data.** With $h(n) = \text{straight-line distance}(n, \text{goal}) / V_{max}$, A\* is optimal only if every road is at least as long as the straight line and no road is faster than $V_{max}$. The cleaning step asserts both; a new 100 km/h bypass with a stale $V_{max} = 80$ would silently break optimality.
- **Results.** A\* expanded about half as many intersections as Dijkstra (median 109 vs 202) with identical answers on 300 trips. Nearest neighbour + 2-opt cut fleet driving from 198 to 111 minutes per day (44%).
- **Scheduling.** 32 shift slots were filled with 39 search nodes and 7 backtracks; plain backtracking needed hundreds. On tighter weeks, heavy-tailed run times appear, and **randomised restarts** tame them.
- **Infeasibility.** When Saturday needed 4 different drivers but only 3 were available, a cheap pre-check explained why in microseconds, and the solver separately **proved** no schedule existed ("proven infeasible" is different from "gave up").
- **Validation.** An independent checker re-derives every rule, and is itself tested by breaking schedules on purpose.

## 14. Which Technique for Which Problem?

| Problem shape | Technique | Notebook |
|---|---|---|
| Path from start to goal, no guidance | BFS, UCS, IDS | 02 |
| Path with a good distance estimate | A\*, IDA\*, weighted A\* | 03 |
| Only the final configuration matters | hill climbing, simulated annealing, GA | 04 |
| An opponent moves too | minimax, alpha-beta, MCTS | 05 |
| Choices that must satisfy rules | backtracking + MRV + propagation, min-conflicts | 06 |
| Certain facts and rules, need proofs | resolution, chaining, SAT | 07 |
| Sequence of actions with preconditions and effects | STRIPS/PDDL planning, HTN | 08 |
| Uncertain evidence, need degrees of belief | Bayes nets, HMMs, decision theory | 09 |
| Vague words, smooth control, explainable rules | fuzzy control, expert systems | 10 |

## Glossary

- **Abduction** — inferring the most plausible explanation for an observation.
- **AC-3** — algorithm that enforces arc consistency by repeatedly revising arcs.
- **Admissible heuristic** — never overestimates the true remaining cost.
- **Agent** — anything that perceives through sensors and acts through actuators.
- **Agent function / program** — the mapping from percept sequences to actions / the code that implements it.
- **Alpha-beta pruning** — minimax that skips branches that cannot affect the decision.
- **Arc consistency** — every value of one variable has a supporting value in its neighbour.
- **Backtracking search** — assign variables one at a time, undo when a constraint breaks.
- **Bayes' rule** — $P(a \mid b) = P(b \mid a)P(a)/P(b)$.
- **Bayesian network** — a DAG with a CPT per node that defines a joint distribution.
- **Beam search** — keep only the best $k$ candidates at each step.
- **Branching factor ($b$)** — number of successors of a node.
- **Certainty factor** — MYCIN's number in $[-1, 1]$ for how strongly evidence supports a conclusion.
- **CNF** — conjunctive normal form: an AND of OR-clauses.
- **Consistent heuristic** — $h(n) \le c(n, a, n') + h(n')$; implies admissible.
- **Constraint satisfaction problem (CSP)** — variables, domains and constraints; solved by a complete consistent assignment.
- **CPT** — conditional probability table of a node given its parents.
- **d-separation** — graphical test for conditional independence in a Bayesian network.
- **Deduction** — conclusions guaranteed true if the premises are true.
- **Defuzzification** — turning an aggregated fuzzy set into one crisp number (e.g. centroid).
- **DPLL** — complete SAT algorithm with unit propagation, pure symbols and backtracking.
- **Effective branching factor ($b^*$)** — branching factor of a uniform tree with the same node count; measures heuristic quality.
- **Entailment ($\models$)** — $\alpha$ is true in every model of the KB.
- **Evaluation function** — estimate of a game position's value at a depth cutoff.
- **Expected utility** — probability-weighted average utility of an action's outcomes.
- **Expectimax** — game search where chance nodes take expected values.
- **Expert system** — knowledge base + working memory + inference engine + explanation facility.
- **First-order logic (FOL)** — logic with objects, predicates, functions and quantifiers.
- **Forward checking** — after an assignment, delete inconsistent values from neighbours' domains.
- **Forward / backward chaining** — data-driven / goal-driven inference with rules.
- **Frame problem** — the difficulty of stating everything an action does not change.
- **Frontier** — generated but not yet expanded nodes.
- **Fuzzy set** — a set with degrees of membership in $[0, 1]$.
- **Genetic algorithm** — population search with selection, crossover and mutation.
- **Graph search** — search that remembers reached states and never expands one twice.
- **Heuristic ($h$)** — estimate of the cost from a node to the goal.
- **Hidden Markov model (HMM)** — hidden Markov chain plus a sensor model.
- **Hill climbing** — repeatedly move to a better neighbour; stops at local optima.
- **Horn clause** — clause with at most one positive literal.
- **Induction** — generalising a rule from examples.
- **Iterative deepening** — depth-limited search with limits 0, 1, 2, ...
- **Knowledge base (KB)** — the set of sentences an agent believes.
- **LCV** — least-constraining value: try the value that rules out the fewest options.
- **Local maximum** — a state better than all its neighbours but not the best overall.
- **Mamdani inference** — fuzzify, fire rules, aggregate, defuzzify.
- **Markov decision process (MDP)** — states, actions, transition probabilities, rewards and a discount.
- **Minimax** — game value assuming both players play optimally.
- **Min-conflicts** — local search for CSPs that reassigns a conflicted variable to its least-conflicting value.
- **Monte Carlo Tree Search (MCTS)** — selection (UCB1), expansion, random playout, back-propagation.
- **MRV** — minimum remaining values: choose the variable with fewest legal values.
- **Node vs state** — a search-tree record (state, parent, action, cost) vs a configuration of the world.
- **Non-monotonic reasoning** — reasoning where new facts can withdraw conclusions.
- **PDDL** — Planning Domain Definition Language, the standard planning file format.
- **PEAS** — Performance measure, Environment, Actuators, Sensors.
- **Problem formulation** — initial state, actions, transition model, goal test, path cost.
- **Rational agent** — maximises expected performance given its percepts and knowledge.
- **Relaxed problem** — a problem with fewer restrictions; its optimal cost is an admissible heuristic.
- **Resolution** — inference rule combining two clauses with complementary literals.
- **SAT** — deciding whether a propositional formula has a satisfying model.
- **Simulated annealing** — local search that accepts worse moves with probability $e^{\Delta E/T}$.
- **Skolemization** — replacing existential variables with new constants or functions.
- **STRIPS** — action representation with preconditions, add lists and delete lists.
- **t-norm / t-conorm** — general fuzzy AND / OR operators.
- **Unification** — finding a substitution that makes two logical expressions identical.
- **Uniform-cost search** — expands the cheapest path first (Dijkstra's algorithm).
- **Utility** — a number saying how desirable a state is.
- **Value of information** — expected improvement in decision quality from observing before acting.
- **Variable elimination** — exact Bayesian-network inference by summing out variables with stored factors.
- **Viterbi algorithm** — finds the most likely sequence of hidden states in an HMM.
