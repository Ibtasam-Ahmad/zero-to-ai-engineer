# Classical AI: how AI reaches goals by searching, reasoning and planning

Classical AI is the part of artificial intelligence where a program reaches a goal by **thinking ahead with knowledge it has been given**: it searches through possible moves, reasons with facts and rules, and plans a sequence of actions. It needs no training data. An AI developer needs it because today's best systems still rely on it: map apps run A\* search, chess engines run alpha-beta, schedulers run constraint solvers, and LLM agents plan, act and replan. This folder is **optional but recommended for beginners**, and **essential for university students**: it covers the material of the standard **"Artificial Intelligence" course in a BS/MS in AI** (or computer science), the course usually taught from Russell & Norvig's *Artificial Intelligence: A Modern Approach* (AIMA).

**Where Classical AI sits under the AI umbrella.** "AI" is the whole field: any program that chooses what to do in a smart way. Inside it are two big families. **Classical (symbolic) AI** writes knowledge down by hand as symbols, rules and models of actions, and then uses **search, logic and planning**. **Machine learning (ML)** learns the rules from data instead. Deep learning is one kind of machine learning (large neural networks), and LLMs (large language models such as ChatGPT or Claude) are one kind of deep learning.

```
+-------------------------------------------------------------------+
|  ARTIFICIAL INTELLIGENCE (AI)                                     |
|                                                                   |
|  +-----------------------------+  +----------------------------+  |
|  | CLASSICAL / SYMBOLIC AI     |  | MACHINE LEARNING (ML)      |  |
|  | knowledge written by people |  | knowledge learned from data|  |
|  | - search (BFS, A*)          |  |  +----------------------+  |  |
|  | - logic and inference       |  |  | DEEP LEARNING        |  |  |
|  | - planning (STRIPS, PDDL)   |  |  | (neural networks)    |  |  |
|  | - constraint solving        |  |  |  +----------------+  |  |  |
|  | (this folder also covers    |  |  |  | LLMs           |  |  |  |
|  |  Bayes nets, fuzzy logic    |  |  |  | (GPT, Claude)  |  |  |  |
|  |  and expert systems)        |  |  |  +----------------+  |  |  |
|  +-----------------------------+  |  +----------------------+  |  |
|              ^                    +----------------------------+  |
|              |                                                    |
|        THIS FOLDER          Hybrids use both: AlphaGo (search +   |
|                             neural nets), LLM agents (LLM + plans)|
+-------------------------------------------------------------------+
```

---

## The whole topic explained simply

Imagine you want a computer to get something done without showing it a single example. You tell it **where it is, what moves it may make, and what counts as "done"**, and it works out the rest by thinking ahead. A **sat-nav** does exactly this: it knows the road map and tries routes in its head before you drive a metre. A **chess player** does it too, but must also ask "what will my opponent reply?". A **detective** does a third version: from a few facts and rules she works out new facts that *must* be true. When the world is uncertain, the computer keeps a number from 0 to 1 for how sure it is, the way a weather app says "70% chance of rain". When the job is filling a timetable, it fills one slot at a time and backs up as soon as a rule breaks, like doing a Sudoku in pencil. All of this is **classical AI**: search, reasoning and planning over knowledge that people wrote down.

**A tiny worked example (A\* route finding).** You are in town A and want to reach town D. There are two routes: A → B → D is 4 + 5 = **9 km**, and A → C → D is 2 + 9 = **11 km**. A quick guess of the distance still to go ("as the crow flies") says B is 4 km from D and C is 8 km from D. The A\* algorithm scores each town as *distance travelled so far + guessed distance still to go*: B scores 4 + 4 = 8 and C scores 2 + 8 = 10. It continues from B (the smaller score) and reaches D with 9 km. C's score of 10 is already worse than 9, so A\* stops: 9 km is guaranteed to be the best route, and it never even had to look at the road from C to D. That "skip what cannot win" idea is the heart of the whole folder.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | Beginners who want to understand how AI works *before* (or alongside) machine learning; BS/MS students taking the "Artificial Intelligence" course; anyone preparing for an AI exam or a job interview |
| **Must know first** | Python functions, lists, dicts, classes and recursion: [`01_Python/01_basic.ipynb`](../../01_Python/01_basic.ipynb). What AI is, in plain words: [`00_start_here_what_is_ai.ipynb`](../00_start_here_what_is_ai.ipynb) |
| **Maths needed** | High-school maths. For notebooks 09 and 10: [`14_Mathematics/00_start_here_math_notation_bridge.ipynb`](../../14_Mathematics/00_start_here_math_notation_bridge.ipynb) and (recommended) [`14_Mathematics/03_probability.ipynb`](../../14_Mathematics/03_probability.ipynb) |
| **Helpful, not required** | Graphs and backtracking from the DSA module: [`../dsa/07_graphs.ipynb`](../dsa/07_graphs.ipynb), [`../dsa/10_backtracking.ipynb`](../dsa/10_backtracking.ipynb) |
| **Time needed** | About 25 to 30 hours for all 11 notebooks (2 to 4 hours each) |
| **Runs on** | CPU only, no API key, no internet. Python, numpy, pandas, matplotlib, networkx |
| **Can I skip it?** | Yes, you can go straight to [`03_Machine_Learning`](../../03_Machine_Learning/00_start_here_your_first_ml_model.ipynb). But agents, states and search come back in Reinforcement Learning and LLM agents, so we recommend at least notebooks 01 to 03 |
| **Deeper study guide** | [`notes/classical_ai.md`](notes/classical_ai.md): every concept in order, with formulas, hand-worked examples and a glossary |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Types of AI and Intelligent Agents](01_types_of_ai_and_intelligent_agents.ipynb) | What kinds of AI exist, what an agent is, and how to write a problem down so a computer can search it | 2-3 h |
| 02 | [Uninformed Search](02_uninformed_search.ipynb) | Six "blind" ways to search a map or a maze (BFS, DFS, DLS, IDS, UCS, bidirectional), and when each finds the best answer | 2-3 h |
| 03 | [Informed (Heuristic) Search](03_informed_search.ipynb) | Searching with a sense of direction: heuristics, greedy best-first, A\*, IDA\* and weighted A\* | 2-3 h |
| 04 | [Local Search and Optimization](04_local_search_and_optimization.ipynb) | Improving one complete answer step by step: hill climbing, simulated annealing, beam search, genetic algorithms | 2 h |
| 05 | [Adversarial Search and Games](05_adversarial_search_and_games.ipynb) | Planning against an opponent: minimax, alpha-beta, evaluation functions, expectimax and Monte Carlo Tree Search | 2-2.5 h |
| 06 | [Constraint Satisfaction Problems](06_constraint_satisfaction.ipynb) | Filling in choices that must obey rules (maps, Sudoku, timetables) with backtracking and constraint propagation | 2 h |
| 07 | [Knowledge Representation and Logic](07_knowledge_representation_and_logic.ipynb) | Storing facts and rules and proving new facts: propositional logic, SAT solvers, first-order logic, Prolog-style reasoning | 3-4 h |
| 08 | [Reasoning and Planning](08_reasoning_and_planning.ipynb) | The kinds of reasoning (deduction, induction, abduction ...) and automated planning with STRIPS/PDDL | 3 h |
| 09 | [Uncertain Knowledge and Reasoning](09_uncertain_knowledge_and_reasoning.ipynb) | Reasoning with probabilities: Bayes' rule, Bayesian networks, hidden Markov models and decision theory | 2.5-3.5 h |
| 10 | [Fuzzy Logic and Expert Systems](10_fuzzy_logic_and_expert_systems.ipynb) | Degrees of truth for vague words, fuzzy controllers, and rule-based expert systems that explain themselves | 2-2.5 h |
| 11 | [🏭 Industry Project: Route Planning and Driver Scheduling](11_industry_route_planning_and_scheduling.ipynb) | A delivery company uses Dijkstra, A\*, 2-opt and a CSP solver on messy real-style data, with every answer checked | 2 h |

```
01 agents & problems
   |
   +--> 02 blind search --> 03 heuristic search --> 04 local search
   |                                 |
   |                                 +--> 05 games (search vs an opponent)
   |
   +--> 06 constraint satisfaction
   |
   +--> 07 logic --> 08 reasoning & planning --> 09 probability --> 10 fuzzy & expert systems
   |
   +----------------------------------------------> 11 industry project (uses 02, 03, 04, 06)
```

---

## The notebooks one by one

### 01 · Types of AI and Intelligent Agents

*Explained simply.* An **agent** is anything that senses its surroundings and acts on them: a robot vacuum, a sat-nav, a game character, an LLM that calls tools. This notebook sorts out which kinds of AI really exist (all of today's AI is "narrow" AI; general AI is still hypothetical) and builds five robot vacuums, from one with no memory to one that learns. It then shows the first step of every search method: **formulating the problem** (start, moves, goal, cost). Think of planning a trip: before you look at a single route, you must know your home city, the roads, the destination and how you will measure "best" (km, time or money).

*Tiny example.* Two rooms, A and B, both dirty, robot starts in A. The rule "if dirty, suck; otherwise go to the other room" cleans the flat in 3 actions (Suck, Right, Suck), but then walks back and forth forever. On a bigger 6 × 6 floor with a step cost, the average scores over the same 300 random floors were:

| Agent type | Average score |
|---|---|
| Simple reflex (no memory) | -24.5 |
| Model-based reflex (remembers where it has been) | 31.5 |
| Goal-based (searches for the nearest unvisited square) | 38.6 |
| Utility-based (heads for the likely-dirty kitchen) | 44.6 |

*You will learn:*
- A short history of AI: symbolic AI vs machine learning, and the two AI winters (about 1974-1980 and 1987-1993)
- Types of AI by capability (narrow, general, super) and by functionality (reactive, limited memory, theory of mind, self-aware)
- Percepts, actions, the agent function vs the agent program, **rationality** and **PEAS** (Performance, Environment, Actuators, Sensors)
- The 7 environment properties (observable, agents, deterministic, episodic, static, discrete, known)
- The 5 agent types: simple reflex, model-based, goal-based, utility-based, learning
- Problem formulation, state-space graph vs search tree, with the 8-puzzle, route finding, missionaries & cannibals and the water jug

*Key takeaway:* a rational agent maximises its *expected* performance measure, and before any search you must write down the initial state, actions, transition model, goal test and path cost.

### 02 · Uninformed Search

*Explained simply.* **Uninformed** (blind) search finds a way from start to goal when it has no idea which direction is better. It keeps a to-do list (the **frontier**) of places it knows about but has not checked yet; the only real difference between the algorithms is *which place it checks next*. **BFS** (breadth-first search) checks everything 1 step away, then 2 steps, and so on; **DFS** (depth-first search) follows one path as far as possible and backs up only at a dead end; **UCS** (uniform-cost search, which is Dijkstra's algorithm) always extends the cheapest route found so far. Think of looking for a lost child: BFS checks every nearby street before going further, DFS follows one road all the way out of town first.

*Tiny example.* On the notebook's 12-town road map, from Ashford to Lakeside:

| Search | Route found | Roads | km |
|---|---|---|---|
| BFS (fewest roads) | via Harborview | 5 | 172 |
| DFS (first route it stumbles on) | long detour | 8 | 276 |
| UCS (cheapest km) | via Glenwood and Kingsport | 5 | **141** (optimal) |

*You will learn:*
- Search vocabulary: node, frontier, expand, reached/explored set
- Tree search vs graph search, and why forgetting where you have been can blow up or loop forever
- BFS, DFS, depth-limited (DLS), iterative deepening (IDS), uniform-cost (UCS) and bidirectional search, written from scratch
- The comparison table: complete? optimal? time? space?, in the notation $b$, $d$, $m$, $C^*$, $\epsilon$
- Solving the water jug (6 actions) and missionaries & cannibals (11 crossings) puzzles

*Key takeaway:* the frontier's data structure *is* the algorithm: a FIFO queue gives BFS, a stack gives DFS, a priority queue on path cost gives UCS.

### 03 · Informed (Heuristic) Search

*Explained simply.* Informed search adds a **heuristic**: a quick, cheap guess of how far the goal still is, such as the straight-line distance on a map. **Greedy best-first search** always goes to the place that *looks* closest, which is fast but can be fooled. **A\*** adds the distance already travelled to the guess and continues from the smallest total; if the guess **never overestimates** (an **admissible** heuristic), A\* is guaranteed to find the best path. Think of driving to the seaside: you prefer roads heading towards the sea, but you still count the kilometres you have already driven.

*Tiny example.*

| Search | Ashford → Lakeside route | Cost |
|---|---|---|
| Greedy ($f = h$) | via Juniper (it looked 0.2 km closer) | 149 km, not optimal |
| A\* ($f = g + h$) | via Glenwood | 141 km, optimal |

On one 20-move 8-puzzle: UCS expanded 61,768 states, A\* with "misplaced tiles" 2,760, and A\* with "Manhattan distance" only 169.

*You will learn:*
- Admissible and consistent heuristics, with plain-word proofs that A\* is optimal
- Dominance between heuristics and how to invent heuristics from **relaxed problems**
- The 8-puzzle: why exactly half of all layouts are unsolvable (counting inversions)
- The **effective branching factor** $b^*$: one number for how good a heuristic is
- IDA\* (A\* with tiny memory), weighted A\* (faster, bounded loss), RBFS and SMA\*
- How an inadmissible heuristic returns a non-optimal path

*Key takeaway:* A\* with an admissible heuristic is optimal, and the better (larger but still admissible) the heuristic, the less work it does.

### 04 · Local Search and Optimization

*Explained simply.* Sometimes you do not need a route to the answer, only a *good answer*: a seating plan, a short delivery round, a timetable. **Local search** starts from any complete answer and keeps making small changes that improve it. The danger is getting stuck on a **local maximum**: the best answer nearby, but not the best overall, like a hiker in fog who climbs the nearest small hill and thinks it is the mountain top. The tricks (restart, sometimes accept a worse step, keep several candidates, breed good answers) all exist to get unstuck. Think of straightening a picture on the wall: nudge, step back, keep the nudge if it looks better.

*Tiny example.* Four friends sit in a row, A B C D; A and B always argue, and so do C and D. "A B C D" has 2 arguing neighbour pairs. Swap B and C: "A C B D" has 0. One local move fixed it. On 200 random 8-queens boards:

| Method | Boards solved |
|---|---|
| Steepest-ascent hill climbing | 16.5% |
| + up to 100 sideways moves | 95.5% |
| Random-restart hill climbing | 100% |

*You will learn:*
- The state-space landscape: global and local maxima, plateaus, shoulders, ridges
- Hill climbing in five flavours (steepest-ascent, sideways, first-choice, stochastic, random-restart)
- **Simulated annealing** and its acceptance probability $e^{\Delta E / T}$
- Local beam search, stochastic beam search, and the beam search used to decode LLM text
- **Genetic algorithms** (selection, crossover, mutation) and tabu search
- A 15-city travelling salesperson problem checked against the exact optimum, and gradient descent as local search in continuous space

*Key takeaway:* local search uses almost no memory and scales to huge problems, but it needs an escape mechanism (restarts, randomness or a population) to avoid local optima.

### 05 · Adversarial Search and Games

*Explained simply.* In a game, an opponent moves too and is trying to make you lose, so for every move you must ask "and what is their best reply?". **Minimax** assumes the opponent plays perfectly and picks the move whose *worst* outcome is best. **Alpha-beta pruning** gets exactly the same answer while skipping moves that cannot change the decision. For huge games, programs look only a few moves ahead and score the position with an **evaluation function**, or, like AlphaGo, play many quick random games (**Monte Carlo Tree Search**). Think of chess: "if I take that pawn, they take my queen, so I won't."

*Tiny example.* You pick a box; your rival then picks which coin from that box you get. Box 1 holds £1 and £10, Box 2 holds £4 and £5. Worst case of Box 1 = £1, worst case of Box 2 = £4, so minimax picks **Box 2**. In full tic-tac-toe:

| Method | Positions visited | Result |
|---|---|---|
| Plain minimax | 549,946 | draw (value 0) |
| Alpha-beta, natural move order | 18,297 (3.3%) | draw |
| Alpha-beta, perfect move order | 2,312 | draw |

*You will learn:*
- Games as search: zero-sum, perfect information, game trees and utilities
- Minimax traced by hand, and a perfect tic-tac-toe player
- Alpha-beta pruning, move ordering and the best case $O(b^{m/2})$
- Depth-limited search with evaluation functions (a Connect-4 player) and the horizon effect
- Expectimax for dice games, and Monte Carlo Tree Search (UCT) from scratch
- The real history: Deep Blue (1997), AlphaGo (2016), AlphaZero, MuZero

*Key takeaway:* alpha-beta never changes the minimax answer; it only saves work, and good move ordering lets it search about twice as deep.

### 06 · Constraint Satisfaction Problems

*Explained simply.* Many puzzles are "choices plus rules": a timetable (every lesson needs a slot and a room, no teacher in two places), a seating plan, a Sudoku. A **constraint satisfaction problem (CSP)** lists the **variables** (things to decide), their **domains** (allowed values) and the **constraints** (rules). A solver fills in one choice at a time, goes back as soon as a rule breaks (**backtracking**), and after each choice crosses out options that are now impossible (**constraint propagation**). Think of pencil marks in Sudoku: you erase candidates as soon as a digit is placed.

*Tiny example.* Three countries A, B, C all touch each other. With 2 colours: A = red, B = green, C has nothing left, so it is impossible. With 3 colours: A = red, B = green, C = blue. For the map of Australia (7 regions, 3 colours) there are $3^7 = 2{,}187$ complete colourings but only 18 valid ones; with a bad variable order plain backtracking needed 41 assignments, while the **MRV** heuristic ("choose the variable with the fewest options left") needed 7.

*You will learn:*
- Variables, domains, unary, binary and global constraints, and the constraint graph
- Four classic CSPs: map colouring, Sudoku, N-Queens and a university timetable
- Backtracking with **MRV**, the degree heuristic and **LCV** (least-constraining value)
- **Forward checking**, **arc consistency (AC-3)** and **MAC**
- **Min-conflicts** local search solving 1,000-queens and 10,000-queens in a few dozen steps
- Tree-structured CSPs solved in $O(nd^2)$, and cutset conditioning

*Key takeaway:* "fail first" (MRV) for choosing variables plus propagation (forward checking or AC-3) turns hopeless searches into tiny ones.

### 07 · Knowledge Representation and Logic

*Explained simply.* This notebook teaches a computer to **know facts and work out new facts that must be true**. We write what is true in a **knowledge base** (KB) and the computer follows strict rules of logic; it only concludes something when it is *certain*. That makes it trustworthy, but someone has to type all the facts in. Think of a family-tree app: you type "Ali is Sara's father" and "Sara is Omar's mother", and it works out by itself that Ali is Omar's grandfather.

*Tiny example.* KB: "if it rains, the ground is wet" ($R \Rightarrow W$) and "it rains" ($R$). Then $W$ (the ground is wet) follows for certain: that is **modus ponens**. But from $R \Rightarrow W$ and $W$ alone you may **not** conclude $R$ (a sprinkler could have done it). The truth table shows why:

| R | W | R ⇒ W |
|---|---|---|
| F | F | T |
| F | T | T |
| T | F | **F** |
| T | T | T |

*You will learn:*
- Knowledge-based agents (TELL and ASK); semantic networks, frames, ontologies and production rules
- Propositional logic: syntax, truth tables, validity, satisfiability and **entailment** ($KB \models \alpha$)
- CNF conversion, **resolution** proofs, Horn clauses, forward and backward chaining
- SAT solvers: **DPLL** and **WalkSAT**, and the 3-SAT threshold near $m/n \approx 4.27$
- The Wumpus world: a logical agent that proves which squares are safe
- First-order logic, translating English, **unification**, Prolog-style backward chaining, and the limits of logic

*Key takeaway:* $KB \models \alpha$ exactly when $KB \land \lnot\alpha$ is unsatisfiable, so every proof can be turned into a satisfiability check.

### 08 · Reasoning and Planning

*Explained simply.* **Reasoning** is drawing conclusions, and there are several kinds: **deduction** (certain), **induction** (a general rule from examples, may be wrong), **abduction** (the best explanation, like a doctor's diagnosis), analogy and common sense. **Planning** means working out, before acting, a sequence of actions that reaches a goal. A planner needs to know what each action *requires* (preconditions) and what it *changes* (effects). Think of making breakfast: you cannot butter toast before toasting the bread.

*Tiny example (the Sussman anomaly).* Three blocks: C is on A, B is on the table. Goal: A on B and B on C. The optimal plan has 6 actions:

```
1. unstack(C, A)   2. put-down(C)   3. pick-up(B)
4. stack(B, C)     5. pick-up(A)    6. stack(A, B)
```

Achieving "A on B" first means you later have to take A off again; the goals interact, so the order really matters.

*You will learn:*
- Deductive, inductive, abductive, analogical and common-sense reasoning, each with a small code demo
- Monotonic vs **non-monotonic** (default) reasoning: "birds fly" until you learn it is a penguin
- STRIPS and **PDDL**: preconditions, add lists, delete lists, parsed from real PDDL text
- Forward (progression) planning with BFS and A\* using relaxation heuristics; backward (regression) planning
- The blocks world, air cargo, partial-order planning, GraphPlan and hierarchical task networks (HTN)
- Plan, execute, monitor, replan: the classical ancestor of plan-and-execute LLM agents

*Key takeaway:* a STRIPS action changes the state by $\text{RESULT}(s, a) = (s - \text{DEL}) \cup \text{ADD}$, and everything it does not mention stays the same.

### 09 · Uncertain Knowledge and Reasoning

*Explained simply.* Real life is full of "probably", and plain logic breaks when rules have exceptions. Here the computer keeps a **degree of belief** between 0 and 1 and updates it when clues arrive. A **Bayesian network** is a drawing of what causes what plus a few small tables of chances; it answers questions such as "the alarm rang and both neighbours called: how likely is a burglary?". The same ideas track hidden things over time (**hidden Markov models**) and choose the action with the best expected result (**decision theory**). Think of a weather app: "70% chance of rain" is a belief, and whether you take an umbrella also depends on how much you hate getting wet.

*Tiny example (Bayes' rule).* A disease affects 1% of people; a test is positive for 90% of sick people and for 9% of healthy people. Out of 100,000 people:

| | Count | Test positive |
|---|---|---|
| Sick (1%) | 1,000 | 900 |
| Healthy (99%) | 99,000 | 8,910 |

$P(\text{sick} \mid +) = 900 / (900 + 8{,}910) \approx 0.092$: only about **9%** of positives are sick. A second independent positive test raises it to about 50%.

*You will learn:*
- The qualification problem, full joint distributions, independence and **conditional independence**
- Bayes' rule, the base-rate fallacy, and naive Bayes as a reasoning engine
- Bayesian networks: CPTs, the chain rule and **d-separation** (including "explaining away")
- Exact inference (enumeration, variable elimination) and sampling (rejection, likelihood weighting, Gibbs)
- Markov chains and HMMs: filtering, smoothing and Viterbi; brief notes on Kalman filters and Dempster-Shafer theory
- Utility, expected utility, the **value of information**, and a first Markov decision process (MDP)

*Key takeaway:* $P(\text{cause} \mid \text{effect}) = P(\text{effect} \mid \text{cause})\,P(\text{cause}) / P(\text{effect})$, and the prior (base rate) matters enormously.

### 10 · Fuzzy Logic and Expert Systems

*Explained simply.* People use vague words: "warm", "tall", "a bit too fast". **Fuzzy logic** gives each word a **degree of truth** from 0 to 1 instead of a hard yes/no, so 24 °C can be "mostly warm and a little hot". A fuzzy controller turns simple human rules ("if the room is hot, run the fan fast") into one smooth, precise number. An **expert system** stores a specialist's know-how as many IF-THEN rules and can explain exactly which rules led to its answer. Think of a mechanic's checklist: "if the engine does not turn and the lights are dim, check the battery".

*Tiny example.* "Warm" rises from 0 at 15 °C to 1 at 25 °C, so at 20 °C the room is warm to degree $(20 - 15)/(25 - 15) = 0.5$. In the notebook's tipping controller, service = 3 and food = 8 out of 10 fire the rules "cheap" at 0.135, "average" at 0.411 and "generous" at 0.5; the **centroid** of the combined shape gives a tip of about **18.0%** (the "mean of maximum" method gives 25%).

*You will learn:*
- Crisp vs fuzzy sets; triangular, trapezoidal and Gaussian membership functions
- Linguistic variables and hedges ("very" = $\mu^2$, "somewhat" = $\sqrt{\mu}$)
- Fuzzy AND/OR/NOT with t-norms and t-conorms (min, product, Łukasiewicz)
- **Mamdani** inference step by step (fuzzify, evaluate rules, aggregate, defuzzify) and **Sugeno** inference
- Expert system architecture, forward chaining with conflict resolution, "how" and "why" explanations
- MYCIN-style certainty factors (historical) and where these systems are still used

*Key takeaway:* fuzzy logic models **vagueness** (degrees of truth), probability models **uncertainty** (degrees of belief); they answer different questions.

### 11 · 🏭 Industry Project: Route Planning and Driver Scheduling

*Explained simply.* A fictional delivery company with 3 vans and 8 drivers has two daily puzzles: which roads each van should take and in which order to visit its stops, and who works which shift this week. The first is solved with search (Dijkstra and A\*) and local search (2-opt); the second is a CSP. The notebook works like a real job: it cleans messy data, checks every answer with an independent validator, and reports savings in minutes and money. Think of a map app picking your fastest way home, plus a school timetable, run every morning for a business.

*Tiny example.* One van, three stops. In the order the orders arrived (school, shop, bakery) the round trip takes 10 + 12 + 9 + 7 = 38 minutes; in the order bakery, school, shop it takes 7 + 5 + 12 + 8 = 32 minutes. Same stops, 6 minutes saved. For the whole fleet:

| Method | Driving minutes per day | km per day |
|---|---|---|
| Dispatch order (today) | 198 | 120.5 |
| Nearest neighbour + 2-opt | 111 | 63.4 |

That is 44% less driving, about $68 per day (roughly $17,000 per year) under the notebook's cost assumptions.

*You will learn:*
- Cleaning and validating a road table (duplicates, missing speeds, impossible lengths, closures)
- Dijkstra vs A\* with a provably admissible heuristic (A\* expanded about half the nodes)
- Multi-stop routes: nearest neighbour, 2-opt, and re-planning after a road closure
- A driver roster as a CSP with backtracking, MRV and forward checking (32 slots, 39 search nodes)
- Diagnosing an infeasible week and offering the manager concrete options
- How companies run this in production (OR-Tools/CP-SAT, time windows, monitoring)

*Key takeaway:* in production the algorithm is only half the job; validated data, an independent checker and a clear report when no solution exists are the other half.

---

## How this connects to the rest of the repo and to real AI systems

- **LLM agents are agents in the sense of notebook 01**, and their plan-act-observe-replan loop is classical planning (notebook 08): see [`10_Agents/01_agent_fundamentals.ipynb`](../../10_Agents/01_agent_fundamentals.ipynb) and [`10_Agents/02_memory_and_planning.ipynb`](../../10_Agents/02_memory_and_planning.ipynb).
- **Reinforcement learning** is the learning agent at scale; MDPs (notebook 09) and MCTS (notebook 05) lead straight into [`11_Reinforcement_Learning/01_rl_fundamentals.ipynb`](../../11_Reinforcement_Learning/01_rl_fundamentals.ipynb), [`02_dynamic_programming.ipynb`](../../11_Reinforcement_Learning/02_dynamic_programming.ipynb) and [`07_multi_armed_bandits.ipynb`](../../11_Reinforcement_Learning/07_multi_armed_bandits.ipynb) (the UCB1 rule inside MCTS).
- **Beam search** (notebook 04) is how translation models and some LLMs choose their words: [`07_NLP/05_language_models_and_generation.ipynb`](../../07_NLP/05_language_models_and_generation.ipynb).
- **Gradient descent is local search in continuous space** (notebook 04): [`14_Mathematics/06_optimization.ipynb`](../../14_Mathematics/06_optimization.ipynb) and [`05_Deep_Learning/02_optimizers.ipynb`](../../05_Deep_Learning/02_optimizers.ipynb).
- **Ontologies and semantic networks** (notebook 07) became knowledge graphs and GraphRAG: [`08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb`](../../08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb).
- **Reasoning LLMs** that search over chains of thought reuse search and planning ideas: [`08_LLM/18_reasoning_models.ipynb`](../../08_LLM/18_reasoning_models.ipynb).
- **Naive Bayes and induction** (notebooks 08 and 09) are the doorway to machine learning: [`03_Machine_Learning/00_start_here_your_first_ml_model.ipynb`](../../03_Machine_Learning/00_start_here_your_first_ml_model.ipynb).
- **Graphs, backtracking and complexity** are shared with the DSA module: [`../dsa/07_graphs.ipynb`](../dsa/07_graphs.ipynb), [`../dsa/10_backtracking.ipynb`](../dsa/10_backtracking.ipynb); why SAT and TSP are hard is covered in [`../advanced_algorithms/02_np_completeness_and_reductions.ipynb`](../advanced_algorithms/02_np_completeness_and_reductions.ipynb), and industrial solvers in [`../advanced_algorithms/05_linear_and_integer_programming.ipynb`](../advanced_algorithms/05_linear_and_integer_programming.ipynb).
- **Real systems today:** Dijkstra and A\* in map apps and internet routing (OSPF), alpha-beta in chess engines such as Stockfish, MCTS in AlphaZero, SAT solvers in chip verification and package managers, constraint solvers in airline and hospital rostering, Bayesian networks in diagnosis, fuzzy controllers in washing machines and rice cookers, rule engines in banks and insurance.

---

## Common beginner mistakes

- **Confusing a state with a node.** A state is a situation of the world; a node is a search-tree record holding a state, its parent, the action and the path cost. One state can appear in many nodes.
- **Using tree search on a graph with cycles.** Without a reached/explored set, the search tree can be infinite even when the map has only 4 towns.
- **Stopping UCS or A\* when the goal is first *generated*.** The goal test must happen when the goal is *expanded* (taken off the priority queue), or you can return a more expensive route (172 km instead of 141 km in notebook 02).
- **Multiplying a heuristic "to make it stronger".** Once $h$ overestimates, A\* is no longer guaranteed to be optimal; that is weighted A\*, with cost bounded by $w \cdot C^*$.
- **Mixing up MRV and LCV.** MRV picks the variable *most* likely to fail (fail first); LCV picks the value *least* likely to fail (keep options open).
- **Pairing quantifiers with the wrong connective.** "All students are smart" is $\forall x\, \text{Student}(x) \Rightarrow \text{Smart}(x)$; "some student is lazy" is $\exists x\, \text{Student}(x) \land \text{Lazy}(x)$.
- **Ignoring the base rate.** A 90%-sensitive test for a 1%-prevalence disease gives only about a 9% chance of disease after one positive result.
- **Treating fuzzy membership as probability.** "0.7 tall" means the person is fairly tall, not that there is a 70% chance they are tall.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| What is a rational agent? | One that chooses the action that maximises its expected performance measure, given its percepts and knowledge |
| Five parts of a search problem? | Initial state, actions, transition model, goal test, path cost |
| Time and space of BFS? | $O(b^d)$ and $O(b^d)$; complete, optimal when all step costs are equal |
| Why use iterative deepening? | BFS's completeness and optimality (for unit costs) with DFS's $O(bd)$ memory |
| When is A\* optimal? | When $h$ is admissible (tree-like search or with re-opening) or consistent (graph search) |
| Admissible vs consistent? | Admissible: $h(n) \le h^*(n)$. Consistent: $h(n) \le c(n, a, n') + h(n')$. Consistent implies admissible |
| Simulated annealing acceptance rule? | Accept a worse move with probability $e^{\Delta E / T}$; high $T$ explores, low $T$ exploits |
| Alpha-beta best-case leaves? | About $b^{m/2}$ (exactly $b^{\lceil d/2\rceil} + b^{\lfloor d/2\rfloor} - 1$ at depth $d$), so it can search about twice as deep |
| What does AC-3 cost? | $O(c\,d^3)$ for $c$ binary constraints and domain size $d$ |
| How do you prove $KB \models \alpha$ by resolution? | Add $\lnot\alpha$ to the KB, convert to CNF and derive the empty clause |
| Forward vs backward chaining? | Forward is data-driven (facts to conclusions); backward is goal-driven (from the query down, as in Prolog) |
| What is the frame problem, and how does STRIPS handle it? | Saying what an action does *not* change; STRIPS assumes everything not in the add or delete list stays the same |
| What is "explaining away"? | In $B \to A \leftarrow E$, observing $A$ makes $B$ and $E$ dependent: learning $E$ lowers belief in $B$ |
| What are the three HMM tasks? | Filtering (now), smoothing (the past, using later evidence), Viterbi (most likely sequence) |
| Mamdani vs Sugeno? | Mamdani outputs fuzzy sets and defuzzifies (e.g. centroid); Sugeno outputs functions or constants and takes a weighted average |

---

## Further reading

**Classic textbooks**
- Stuart Russell and Peter Norvig, *Artificial Intelligence: A Modern Approach*, 4th ed. (2020). The standard textbook for this course; chapters 1-17 cover notebooks 01-09 (fuzzy logic and expert systems are covered better by Negnevitsky, below).
- Nils J. Nilsson, *The Quest for Artificial Intelligence* (2010): the history of AI by one of the inventors of A\*.
- Michael Negnevitsky, *Artificial Intelligence: A Guide to Intelligent Systems*, 3rd ed.: expert systems and fuzzy logic with worked examples.
- Judea Pearl, *Probabilistic Reasoning in Intelligent Systems* (1988): the book that introduced Bayesian networks.
- Ghallab, Nau and Traverso, *Automated Planning and Acting* (2016): planning in depth.
- Rossi, van Beek and Walsh (eds.), *Handbook of Constraint Programming* (2006).

**Free resources**
- AIMA code in Python: <https://github.com/aimacode/aima-python>
- UC Berkeley CS188 "Introduction to Artificial Intelligence" (lectures, notes and Pacman projects): <https://inst.eecs.berkeley.edu/~cs188/>
- MIT OpenCourseWare 6.034 "Artificial Intelligence" (Patrick Winston's lectures): <https://ocw.mit.edu/courses/6-034-artificial-intelligence-fall-2010/>
- Amit Patel's "Red Blob Games" pages on A\* and pathfinding: <https://www.redblobgames.com/pathfinding/a-star/introduction.html>
- Google OR-Tools documentation (routing and CP-SAT): <https://developers.google.com/optimization>
- The study guide for this folder: [`notes/classical_ai.md`](notes/classical_ai.md), and the repo-wide [`GLOSSARY.md`](../../GLOSSARY.md) and [`LEARNING_PATH.md`](../../LEARNING_PATH.md)
