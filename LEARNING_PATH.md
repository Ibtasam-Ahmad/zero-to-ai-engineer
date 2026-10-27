# 🧭 Learning Path: What to Study, in What Order

> **Who is this for?** Anyone who opens this repo and asks: *"There are 355 notebooks. Where do I start, and what can I skip?"*
>
> **Studying for a degree, or want degree-level depth?** Pick a route in [🎓 Choose your route](#-choose-your-route), then check your coverage in the [🗺️ Degree map](#degree-map).
>
> **Not set up yet?** Do [`START_HERE.md`](START_HERE.md) first. Unknown word? Check [`GLOSSARY.md`](GLOSSARY.md). Something not working? See the troubleshooting table in [`START_HERE.md`](START_HERE.md#6-troubleshooting).

---

## How to read this page

The folders are numbered `00` to `24`, but **the numbers are not the study order**. For example, you need Git (`20`) and some maths (`14`) long before you need deployment (`16`). This page gives you the order.

Each stage lists what to do, marked like this:

| Mark | Meaning |
|---|---|
| ⭐ **Core** | Do it. Everything later builds on it. |
| ✅ **Recommended** | Do it if you can; it makes you noticeably stronger. |
| 🔹 **Optional** | Advanced or specialised. Skip on your first pass and come back when you need it. |
| 🌱 | A **Start Here** notebook: a gentle, fully runnable introduction written for complete beginners. |
| 🏭 | An **industry** notebook: the same topic done the way a company would do it. |
| 🔑 | Needs a paid API key to run fully (you can still read it; free alternatives are listed). |
| 🎓 | **Degree core**: university-course material (DSA, DBMS, discrete maths, classical AI…). Optional on the job route (a), core on the degree routes (b) and (c). |
| 🔬 | **MS / MPhil level**: graduate theory and research. Optional on routes (a) and (b), core on route (c). |

**Every folder also has a `notes/` file** (for example `03_Machine_Learning/notes/03_Machine_Learning.md`). It explains the ideas in plain English with diagrams. A good routine for every topic:

1. Read the notes file for the topic.
2. Run the 🌱 Start Here notebook, if there is one.
3. Run the core notebooks **cell by cell**. Change numbers, break things, and see what happens.
4. Do the 🏭 industry notebook.
5. Write 3–5 sentences explaining what you learned, in your own words.

**Time estimates** assume about **10–15 hours per week**. Going slower is completely fine.

---

## 🎓 Choose your route

The same stages serve three goals. Pick one; you can always switch later, because the routes share the same core.

| Route | Who it is for | Do these marks | Rough time at 10–15 h/week |
|---|---|---|---|
| **(a) Job-ready AI developer** (core path) | You want to build and ship AI products at work | ⭐ always, ✅ when you can | **8–11 months** |
| **(b) BS AI / BS Data Science equivalent** | You want what a 4-year bachelor's teaches in AI/DS and computing | ⭐ ✅ 🎓, plus 2–3 electives | **18–24 months** |
| **(c) MS / MPhil equivalent** | You want graduate theory and to do research | everything in (b), plus 🔬 and a thesis | **+10–14 months after (b)** (about 10–14 months if you already hold a BS in CS/AI/DS) |

### (a) Job-ready AI developer (core path)

- **Stages:** 0 → 1 → 2 → 2b (✅ rows only) → 3 → 4 (⭐ rows) → 5 → 7 → 8 → 9 → 10 → 11 → 12 → 13. Add Stage 6 if your job involves forecasting.
- **Include:** every ⭐ row and as many ✅ rows as you can. The production-skills rows matter most: testing (`23_Software_Engineering/03`), security (`08`), observability (`15_MLOps/16`) and LLM evaluation (`08_LLM/22`).
- **Skip on the first pass:** every row that starts with 🔹 (including 🔹🎓 and 🔹🔬), Stage 1b, Stage 13b and the optional tracks. Come back when a job or a project needs them.
- **Before interviews:** DSA (Stage 2b), the [coding interview workbook](00_AI_Fundamentals/advanced_algorithms/09_coding_interview_workbook.ipynb), and Stage 13 system design.

### (b) BS AI / BS Data Science equivalent

- **Stages:** all of 0–13, including Stage 1b (classical AI), Stage 2b (DSA) and Stage 13b (research methods, notebooks `01`–`05`).
- **Include:** every ⭐, ✅ and 🎓 row, Stage 6 (forecasting), and **2–3 electives** from the 🔹 rows or the [optional tracks](#optional-tracks-any-time-after-stage-7) (for example RL, NLP depth, computer vision depth, a domain elective).
- **Skip:** 🔬 rows (they are MS level) and the 🔹 specialisations you did not choose as electives.
- **Final Year Project:** Stage 12 capstones, then one project of your own written up as a short report using `24_Research_Methods/05`.
- **Check your coverage** against the [🗺️ Degree map](#degree-map).

### (c) MS / MPhil equivalent (adds theory and research)

- **Before you start:** finish route (b), or hold a BS in CS, AI, DS, maths or engineering. Skim the 🎓 rows to fill gaps (DSA, DBMS and discrete maths are the usual ones).
- **Include:** every 🔬 row: advanced algorithms (Stage 2b), convex optimisation (Stage 4), learning theory, kernels and probabilistic graphical models (Stage 5), graph ML (Stage 7), the full RL track, and all of Stage 13b.
- **Specialise:** pick one area for your thesis (LLMs/NLP, vision, RL, forecasting, causal inference, AI safety or a domain elective) and do every 🔹 row in that area.
- **Thesis:** Stage 13b plus a **4–6 month research project** = capstone + research. See [Stage 13b](#stage-13b-research-methods--thesis-degree-routes-46-weeks--thesis).
- **Skip:** 🔹 specialisations outside your thesis area.

---

## The big picture

```
 Stage 0  Setup ─► Stage 1  Big picture & ethics ─► Stage 2  Python & tools
                         │                                │
                         └─► Stage 1b Classical AI        ├─► Stage 2b DSA (+ advanced algorithms)
                                                          │
 Stage 5  Machine learning ◄─ Stage 4  Maths bridge ◄─ Stage 3  Data analysis (+ SQL & DBMS)
     │
     ├─► Stage 6  Forecasting (optional track)
     ▼
 Stage 7  Deep learning ─► Stage 8  Vision & language ─► Stage 9  LLMs & prompting
                                                               │
 Stage 12 Capstone projects ◄─ Stage 11 Shipping & MLOps ◄─ Stage 10  Agents
     │
     ▼
 Stage 13 System design & career ─► Stage 13b Research methods & thesis (degree routes)

 (+ optional tracks: RL, advanced safety, advanced MLOps, domain electives)
```

The core path (⭐ only) takes roughly **6–9 months** at 10–15 h/week. Each route in [🎓 Choose your route](#-choose-your-route) adds to it.

---

## Stage 0: Setup (1–2 days)

| | What | Why |
|---|---|---|
| ⭐ | [`START_HERE.md`](START_HERE.md) | Install Python and the packages, open Jupyter (or use Google Colab) |
| ⭐🌱 | `01_Python/00_start_here_jupyter_terminal_and_debugging.ipynb` | How notebooks, the terminal, `pip`, error messages and Git work |

## Stage 1: The big picture & responsible AI (3–5 days)

| | What | Why |
|---|---|---|
| ⭐🌱 | `00_AI_Fundamentals/00_start_here_what_is_ai.ipynb` | What AI / ML / deep learning / LLMs are, the key vocabulary, and a map of this repo |
| ⭐ | `00_AI_Fundamentals/notes/00_AI_Fundamentals.md` | Why fairness, transparency and safety matter |
| ✅ | `00_AI_Fundamentals/01_bias_and_fairness.ipynb`, `06_responsible_ai_and_ethics.ipynb` | The two most important ethics topics, hands-on |
| 🔹 | `00_AI_Fundamentals/02`–`05`, 🏭 `07_industry_responsible_ai_product_review.ipynb` | These use ML terms you will learn in Stage 5. Coming back to them after Stage 5 is perfectly fine. |

## Stage 1b: Classical AI: search, logic & planning (2–3 weeks)

The university "Artificial Intelligence" course: how a computer reaches a goal by searching and reasoning, with no training data at all. Folder guide: [`00_AI_Fundamentals/classical_ai/`](00_AI_Fundamentals/classical_ai/README.md). It needs basic Python, so do it **after `01_Python/01_basic`** (alongside Stage 2 or Stage 5 is fine). Core for the degree routes; optional on the job route.

| | What | Why |
|---|---|---|
| 🔹🎓 | `00_AI_Fundamentals/classical_ai/01_types_of_ai_and_intelligent_agents.ipynb` | What an "agent" is and which kinds of AI really exist, built as five robot vacuums |
| 🔹🎓 | `02_uninformed_search.ipynb` | Finding a route with no hints: breadth-first, depth-first and uniform-cost search |
| 🔹🎓 | `03_informed_search.ipynb` | Search with a sense of direction: heuristics and A*, the idea inside every sat-nav |
| 🔹🎓 | `04_local_search_and_optimization.ipynb` | Improving a good answer step by step: hill climbing, simulated annealing, genetic algorithms |
| 🔹🎓 | `05_adversarial_search_and_games.ipynb` | Planning against an opponent: minimax, alpha-beta pruning and Monte Carlo Tree Search |
| 🔹🎓 | `06_constraint_satisfaction.ipynb` | Choices that must obey rules (timetables, Sudoku): backtracking and constraint propagation |
| 🔹🎓 | `07_knowledge_representation_and_logic.ipynb` | Storing facts and working out new ones with logic, resolution and SAT solvers |
| 🔹🎓 | `08_reasoning_and_planning.ipynb` | Kinds of reasoning, and planning a sequence of actions with STRIPS/PDDL |
| 🔹🎓 | `09_uncertain_knowledge_and_reasoning.ipynb` | Reasoning with "probably": Bayes' rule and Bayesian networks |
| 🔹🎓 | `10_fuzzy_logic_and_expert_systems.ipynb` | Vague words like "warm" turned into numbers, and rule-based expert systems |
| 🔹🎓🏭 | `11_industry_route_planning_and_scheduling.ipynb` | Delivery-van routes and driver schedules, solved the way a logistics company would |

## Stage 2: Python & everyday tools (3–4 weeks)

| | What | Why |
|---|---|---|
| ⭐ | `01_Python/01_basic.ipynb` → `02_industrial.ipynb` | The Python you will use everywhere |
| ✅ | `01_Python/03_advanced.ipynb` | Decorators, generators, typing: useful, but not needed yet |
| ⭐🏭 | `01_Python/04_industry_from_notebook_to_production_code.ipynb` | Writing code other people can use |
| ⭐ | `20_Git_and_DevOps/01_git_basics.ipynb` | **Learn Git now**, not at the end. Save every exercise in a Git repo. |
| ✅🏭 | `20_Git_and_DevOps/05_industry_team_git_workflow_for_ml.ipynb` | Branches and pull requests, as teams use them |

Software engineering basics, from [`23_Software_Engineering/`](23_Software_Engineering/README.md) (notebooks `04`–`12` come in Stage 11):

| | What | Why |
|---|---|---|
| ✅🎓 | `23_Software_Engineering/01_oop_and_solid_principles.ipynb` | Classes, inheritance vs composition and the SOLID rules, so big programs stay easy to change |
| ✅ | `23_Software_Engineering/02_design_patterns_for_ai_code.ipynb` | Proven recipes (factory, strategy, adapter, observer…) applied to model and LLM code |
| ⭐ | `23_Software_Engineering/03_testing_ai_code.ipynb` | pytest, mocking LLM calls, property-based tests and coverage: a smoke alarm for your code |

## Stage 2b: Data structures & algorithms (3–4 weeks; advanced algorithms +3–4 weeks)

How to make code fast and how to reason about it: the "DSA" course of every CS degree and the core of coding interviews. Folder guide: [`00_AI_Fundamentals/dsa/`](00_AI_Fundamentals/dsa/README.md). Do it alongside or right after Stage 2; from `05` on you need classes (`01_Python/03_advanced`). The ✅ rows are worth doing on the job route too.

| | What | Why |
|---|---|---|
| ✅🎓 | `00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb` | Big-O: predicting how slow code gets as data grows, plus recursion |
| ✅🎓 | `02_arrays_strings_and_techniques.ipynb` | Arrays, strings and the classic tricks: two pointers, sliding window, prefix sums |
| ✅🎓 | `03_searching_and_sorting.ipynb` | Binary search and the main sorting algorithms, and when each one wins |
| ✅🎓 | `04_hashing.ipynb` | How dictionaries and sets find things instantly, and consistent hashing |
| ✅🎓 | `05_linked_lists_stacks_queues.ipynb` | Linked lists, stacks, queues and an LRU cache built from them |
| ✅🎓 | `06_trees_bst_and_heaps.ipynb` | Trees, binary search trees and heaps (priority queues) |
| ✅🎓 | `07_graphs.ipynb` | Graphs: BFS/DFS, shortest paths, spanning trees, topological sort |
| 🔹🎓 | `08_greedy_and_divide_and_conquer.ipynb` | Two big strategies: grab the best option now, or split the problem in half |
| ✅🎓 | `09_dynamic_programming.ipynb` | Never work the same thing out twice: write answers down and reuse them |
| 🔹🎓 | `10_backtracking.ipynb` | Trying every possibility without wasting time on hopeless ones (N-Queens, Sudoku) |
| 🔹🎓 | `11_advanced_tries_strings_and_range_queries.ipynb` | Tries, fast string matching, range queries and number theory for programmers |
| ✅🎓🏭 | `12_industry_dsa_in_ai_systems.ipynb` | The DSA hiding inside real AI products: top-k retrieval, tokenizers, dedup, caching |

**Advanced algorithms** (after DSA, optional): graduate-level algorithms. Folder guide: [`00_AI_Fundamentals/advanced_algorithms/`](00_AI_Fundamentals/advanced_algorithms/README.md). Do discrete maths (Stage 4) first if you can.

| | What | Why |
|---|---|---|
| 🔹🔬 | `00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb` | Average cost over many operations, and algorithms that use randomness on purpose |
| 🔹🔬 | `02_np_completeness_and_reductions.ipynb` | Why some problems are easy to check but (probably) hard to solve: P vs NP |
| 🔹🔬 | `03_approximation_and_parameterized_algorithms.ipynb` | Fast answers with a proven "at most twice as bad" guarantee for hard problems |
| 🔹🔬 | `04_network_flows_and_matching.ipynb` | Max flow, min cut and matching: pipes, assignments and image segmentation |
| 🔹🔬 | `05_linear_and_integer_programming.ipynb` | Finding the best plan under limited resources, with the simplex method from scratch |
| 🔹🔬 | `06_streaming_and_sketching_algorithms.ipynb` | Counting and sampling data too big to store: Count-Min, HyperLogLog, MinHash |
| 🔹🔬 | `07_computational_geometry_and_fft.ipynb` | Points, lines and shapes (convex hulls, Voronoi), and the fast Fourier transform |
| 🔹🔬 | `08_advanced_data_structures.ipynb` | Suffix arrays, KD-trees, red-black trees, persistent structures, LSM trees |
| ✅ | `09_coding_interview_workbook.ipynb` | A step-by-step method and pattern map for coding interviews. **Do it before job interviews.** |
| 🔹🔬 | `10_parallel_and_external_memory_algorithms.ipynb` | Algorithms for many CPU cores and for data bigger than memory |

## Stage 3: Data analysis (3–4 weeks; +3–4 weeks for the 🎓 rows)

Do `02_Data_Analysis` in **this** order. `01_data_preprocessing` uses tools taught in the later notebooks, so it comes last here.

| | What | Why |
|---|---|---|
| ⭐ | `02_Data_Analysis/02_numpy.ipynb` → `03_pandas.ipynb` | Arrays and tables: the foundation of all data work |
| ⭐ | `04_matplotlib.ipynb` → `05_seaborn.ipynb` | Plotting |
| ⭐ | `07_eda.ipynb` → `08_statistics.ipynb` | Exploring data and basic statistics |
| ⭐ | `01_data_preprocessing.ipynb` | Cleaning data. It mentions SMOTE and pipelines; those are explained fully in Stage 5. |
| ⭐🏭 | `11_industry_eda_report_for_stakeholders.ipynb` | Turning analysis into a report people act on |
| ✅ | `13_Databases/01_sql/01_sql_fundamentals.ipynb`, 🏭 `02_industry_sql_for_ml_feature_extraction.ipynb` | SQL is asked for in almost every data or AI job |
| 🔹 | `06_plotly.ipynb`, `09_polars.ipynb`, `10_duckdb.ipynb` | Faster or interactive alternatives |
| ✅ | `02_Data_Analysis/12_data_acquisition_apis_scraping_and_formats.ipynb` | Collecting data yourself: REST APIs, polite web scraping, CSV/JSON/Parquet/Excel |
| ✅🎓 | `13_statistical_modeling_and_inference.ipynb` | Regression for *explaining* (not just predicting): reading coefficients, p-values and diagnostics |
| 🔹🎓 | `14_design_of_experiments.ipynb` | Planning fair tests: randomisation, blocking, factorial designs and sample size |
| ✅🎓 | `15_data_visualization_principles_and_storytelling.ipynb` | Choosing the right chart, avoiding misleading ones, colour-blind-safe colours, telling a story |

**DBMS fundamentals** (university database theory, next to the SQL notebooks). Folder guide: [`13_Databases/00_dbms_fundamentals/`](13_Databases/00_dbms_fundamentals/README.md). Do `01`, then `13_Databases/01_sql/01_sql_fundamentals`, then `02`–`10`. Core for the degree routes.

| | What | Why |
|---|---|---|
| 🔹🎓 | `13_Databases/00_dbms_fundamentals/01_dbms_introduction_and_architecture.ipynb` | What a database management system is, why files are not enough, and what is inside one |
| 🔹🎓 | `02_er_model_and_eer.ipynb` | Drawing the plan of a database (ER diagrams) and turning it into tables |
| 🔹🎓 | `03_relational_model_and_relational_algebra.ipynb` | The maths behind SQL tables: keys, constraints and relational algebra |
| ✅🎓 | `04_functional_dependencies_and_normalization.ipynb` | Normalisation: storing every fact in exactly one place (1NF to BCNF) |
| 🔹🎓 | `05_transactions_and_concurrency_control.ipynb` | All-or-nothing changes and many users at once: ACID, locks, deadlocks |
| 🔹🎓 | `06_recovery_and_storage.ipynb` | How a database survives crashes: write-ahead logs, ARIES, buffers, RAID |
| ✅🎓 | `07_indexing_b_trees_and_hashing.ipynb` | Indexes and B+ trees: why some queries are instant and others crawl |
| 🔹🎓 | `08_query_processing_and_optimization.ipynb` | How the database turns your SQL into a fast plan (join algorithms, cost models) |
| 🔹🎓 | `09_distributed_databases_warehousing_and_security.ipynb` | Data spread over many machines, CAP, data warehouses (OLAP) and database security |
| ✅🎓🏭 | `10_industry_designing_a_database_end_to_end.ipynb` | Designing a real database from requirements to tuned queries |

## Stage 4: Maths bridge (2–3 weeks, can run in parallel with Stage 5; +3–4 weeks for the 🎓/🔬 rows)

| | What | Why |
|---|---|---|
| ⭐🌱 | `14_Mathematics/00_start_here_math_notation_bridge.ipynb` | From high-school maths to ML notation: Σ, vectors, derivatives, probability, formula → code |
| ⭐ | `14_Mathematics/01_linear_algebra.ipynb`, `02_calculus.ipynb`, `03_probability.ipynb`, `04_statistics.ipynb` | The four pillars. Aim for intuition; you don't need to master proofs. |
| ✅🏭 | `14_Mathematics/08_industry_math_in_practice.ipynb` | Where the maths shows up in real work |
| 🔹 | `05_information_theory.ipynb`, `06_optimization.ipynb`, `07_bayesian_ml.ipynb` | Read when a later notebook needs them (e.g. cross-entropy for deep learning, Bayesian methods for A/B testing) |
| 🔹🎓 | `14_Mathematics/09_numerical_methods.ipynb` | How computers solve maths with no neat formula: root finding, integration, ODEs, rounding error |
| 🔹🎓 | `10_numerical_linear_algebra.ipynb` | How `solve`, least squares and eigenvalues really work (LU, QR, iterative solvers, PageRank) |
| ✅🎓 | `11_matrix_calculus_and_autodiff_from_scratch.ipynb` | Gradients of whole matrices, and a tiny autograd engine: what PyTorch does in `.backward()` |
| 🔹🔬 | `12_convex_optimization_and_duality.ipynb` | Problems with one best answer: duality, KKT conditions, the SVM dual, proximal methods, ADMM |

**Discrete mathematics & theory of computation** (+1–2 weeks). Folder guide: [`14_Mathematics/discrete_math/`](14_Mathematics/discrete_math/README.md). Best done alongside DSA (Stage 2b) and before advanced algorithms. Core for the degree routes.

| | What | Why |
|---|---|---|
| 🔹🎓 | `14_Mathematics/discrete_math/01_sets_relations_functions_and_proofs.ipynb` | Sets, relations, functions and how to write a proof (including induction) |
| 🔹🎓 | `02_combinatorics_and_recurrences.ipynb` | Counting without listing, and solving recurrences (the maths behind Big-O) |
| 🔹🎓 | `03_graph_theory.ipynb` | Dots and lines: trees, Euler and Hamilton paths, colouring, planar graphs, matchings |
| 🔹🎓 | `04_automata_and_regular_languages.ipynb` | Machines that read text one character at a time, and how regular expressions work |
| 🔹🎓 | `05_grammars_parsing_and_computability.ipynb` | Grammars and parsers, Turing machines, and problems no computer can ever solve |

## Stage 5: Classical machine learning (6–8 weeks; +3–4 weeks for the 🔬 rows)

| | What | Why |
|---|---|---|
| ⭐🌱 | `03_Machine_Learning/00_start_here_your_first_ml_model.ipynb` | A complete first project: split, baseline, train, evaluate, overfitting, leakage, saving |
| ⭐ | `03_Machine_Learning/01_supervised/`: `00_preprocessing`, `01_linear_regression`, `02_logistic_regression`, `03_decision_trees`, `04_ensemble_methods`, `09_pipeline_and_leakage`, `10_end_to_end_project` | The core supervised algorithms and the habits that keep you honest |
| ⭐🏭 | `01_supervised/14_industry_churn_prediction.ipynb`, `15_industry_house_price_regression.ipynb` | Classification and regression done professionally |
| ✅ | `01_supervised/05_svm`, `06_naive_bayes`, `07_knn`, `13_model_calibration` | More algorithms worth knowing |
| ⭐ | `02_unsupervised/01_clustering`, `02_dimensionality_reduction`, 🏭 `04_industry_customer_segmentation` | Finding structure without labels |
| ⭐ | `05_feature_engineering/` (all three) | Usually the biggest lever on model quality |
| ⭐ | `06_model_evaluation/` (all three) | Choosing metrics, tuning, comparing models fairly |
| ✅ | `07_explainability/` (all three), `10_evaluation_metrics_comprehensive.ipynb` | Explaining predictions; the full metrics reference |
| ✅ | `11_ab_testing/` | How companies decide whether a model actually helps |
| 🔹 | `01_supervised/08`, `11`, `12`; `02_unsupervised/03`; `03_semi_supervised/`, `04_uncommon_models/`, `08_anomaly_detection/`, `09_recommendation_systems/`, `10_causal_inference/`, `12_online_learning/`, `13_active_learning/`, `14_conformal_prediction/`, `15_synthetic_tabular_data/` | Specialisations: pick the ones that match your interests or job. Each has a 🏭 notebook. |
| 🔹🎓 | `02_unsupervised/05_clustering_and_manifold_learning_in_depth.ipynb` | k-means, hierarchical, DBSCAN/HDBSCAN and spectral clustering from scratch, plus t-SNE/UMAP-style maps |
| 🔹 | `09_recommendation_systems/03_neural_and_sequential_recommenders.ipynb` | Modern recommenders: two-tower retrieval, "what comes next" models, retrieve → rank → re-rank |
| 🔹 | `15_MLOps/08_automl/02_automl_from_scratch.ipynb` | How AutoML picks models and settings: Hyperband, Bayesian optimisation, ensemble selection |

**MS-level machine learning theory** (+3–4 weeks). Core for route (c); needs Stage 4 maths (probability and linear algebra).

| | What | Why |
|---|---|---|
| 🔹🔬 | [`03_Machine_Learning/16_learning_theory/`](03_Machine_Learning/16_learning_theory/README.md) `01_statistical_learning_theory.ipynb` | Why learning from a sample works at all: PAC learning, VC dimension, generalisation bounds |
| 🔹🔬 | `16_learning_theory/02_kernel_methods.ipynb` | Curved patterns with linear maths: the kernel trick, kernel ridge/PCA, MMD drift tests |
| 🔹🔬 | [`03_Machine_Learning/17_probabilistic_graphical_models/`](03_Machine_Learning/17_probabilistic_graphical_models/README.md) `01_markov_networks_and_exact_inference.ipynb` | Many uncertain things at once: Markov networks, variable elimination, belief propagation |
| 🔹🔬 | `17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb` | Models with hidden parts: EM, variational inference (the ELBO) and MCMC sampling |

## Stage 6 (optional track): Forecasting (3–4 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `04_Forecasting/00_start_here_forecasting_done_right.ipynb` | Baselines, time-based splits, honest backtesting, and the leakage traps |
| ⭐ | `01_time_series_basics.ipynb` → `02_classical_methods.ipynb` | Trend, seasonality, ARIMA, exponential smoothing |
| ⭐🏭 | `11_industry_retail_demand_forecasting.ipynb`, `12_industry_call_center_staffing_forecast.ipynb` | Real forecasting work |
| 🔹 | `03`–`10` | ML and deep-learning forecasting, Prophet, multivariate models, GARCH, probabilistic forecasts, anomaly detection |

## Stage 7: Deep learning (5–6 weeks; +2–3 weeks for the hands-on rows `18`–`21`)

| | What | Why |
|---|---|---|
| ⭐🌱 | `05_Deep_Learning/00_start_here_pytorch_from_zero.ipynb` | Tensors, autograd and the training loop, all actually trained on CPU |
| ⭐ | `01_neural_network_fundamentals.ipynb` → `02_optimizers.ipynb` | What happens inside a network, and how it learns |
| ⭐🏭 | `16_industry_pytorch_training_pipeline.ipynb` | **Do this right after 01–02.** It is the most practical PyTorch notebook in the repo. |
| ⭐ | `03_cnn.ipynb`, `04_rnn_lstm_gru.ipynb`, `05_transformers_architecture.ipynb` | The three architecture families. `05` is essential for LLMs. |
| ✅🏭 | `17_industry_model_export_and_inference.ipynb` | Getting a trained model out of the notebook |
| 🔹 | `06`–`15` | Generative models, GNNs, compression, self-supervised learning, PEFT, distributed training… (some need a GPU) |
| ✅🎓 | `05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb` | Build a whole network in plain NumPy (layers, backprop, optimisers, dropout, batch norm, a tiny CNN) |
| ✅ | `19_sequence_models_hands_on.ipynb` | RNN, LSTM and GRU cells from scratch, seq2seq with attention, and beam search (hands-on partner of `04`) |
| 🔹🎓 | `20_generative_models_hands_on.ipynb` | VAE, GAN, a diffusion model and a normalizing flow, each trained on CPU (hands-on partner of `06`) |
| 🔹🔬 | `21_graph_machine_learning_hands_on.ipynb` | Learning on networks: spectral embeddings, node2vec and GNNs from scratch (hands-on partner of `07`) |

## Stage 8: Computer vision & NLP (4–6 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `06_Computer_Vision/00_start_here_images_and_your_first_cnn.ipynb` | Pixels, convolutions, and a CNN trained on CPU |
| ⭐ | `06_Computer_Vision/01_image_basics_opencv.ipynb`, `02_image_classification.ipynb`, 🏭 `11_industry_visual_defect_inspection.ipynb` | Core vision skills |
| ✅ | `03_object_detection`, `05_vision_transformers`, 🏭 `12_industry_visual_product_search` | |
| 🔹 | `04`, `06`–`10` | Segmentation, generation, OCR, video, 3-D, medical imaging |
| ⭐🌱 | `07_NLP/00_start_here_text_to_numbers.ipynb` | Tokens, TF-IDF, embeddings, semantic search |
| ⭐ | `07_NLP/01_text_preprocessing`, `02_word_embeddings`, `03_text_classification`, 🏭 `12_industry_support_ticket_routing`, 🏭 `13_industry_semantic_search_engine` | Core NLP |
| 🔹 | `07_NLP/04`–`11` | NER, generation, QA, topic models, speech, multilingual |

## Stage 9: LLMs & prompt engineering (6–7 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `08_LLM/00_start_here_how_llms_work.ipynb` | Next-token prediction, sampling, chat templates, and a tiny GPT trained from scratch |
| ⭐🌱 | `09_Prompt_Engineering/00_start_here_prompting_with_a_free_local_model.ipynb` | Every basic prompting technique, actually running, with no key |
| ⭐🔑 | `09_Prompt_Engineering/01_basics.ipynb` → `02_techniques.ipynb` → `03_advanced.ipynb` | The full prompting toolkit |
| ⭐ | `09_Prompt_Engineering/04_adversarial.ipynb` | Prompt injection: attacks, defences, and how to test a filter with known attacks |
| ⭐🏭 | `09_Prompt_Engineering/05_industry_prompt_development_workflow.ipynb` | Prompts treated as tested, versioned code |
| ⭐🔑 | `08_LLM/01_chatbots/`, `08_LLM/02_rag/01_rag_fundamentals.ipynb`, `02_advanced_rag.ipynb` | Chatbots and Retrieval-Augmented Generation |
| ⭐🏭 | `08_LLM/19_industry_rag_pipeline.ipynb`, `20_industry_llm_application_patterns.ipynb` | RAG and reliable LLM calls, running locally |
| ✅ | `08_LLM/08_evaluation/`, `16_llm_security.ipynb`, `17_structured_outputs.ipynb`, `04_different_llms/`, `05_slms/` | Evaluation, security, structured output, choosing a model |
| ✅ | `08_LLM/22_llm_evaluation_hands_on.ipynb` | Marking an LLM's homework properly: metrics from scratch, LLM judges, RAG metrics, statistics, regression tests |
| ✅ | `08_LLM/21_fine_tuning_hands_on_cpu.ipynb` | Teaching a tiny model to follow instructions on a CPU: SFT, LoRA from scratch, forgetting, DPO |
| 🔹 | `08_LLM/02_rag/03`–`04`, `03_fine_tuning/`, `06_vision_llm/`, `07_prompt_engineering/`, `09_knowledge_graphs/`, `10_synthetic_data/`, `11_multimodal/`, `12`–`15`, `18`; `09_Prompt_Engineering/ai_tools/` | Advanced topics (fine-tuning needs a GPU) |

## Stage 10: Agents (3–4 weeks)

| | What | Why |
|---|---|---|
| ⭐🔑 | `10_Agents/01_agent_fundamentals.ipynb` → `02_memory_and_planning.ipynb` | The agent loop: think, act with tools, observe |
| ⭐🏭 | `10_Agents/09_industry_tool_using_agent.ipynb` | **Do this early.** It runs offline and shows a complete, safe agent. |
| ✅🔑 | `03_langgraph.ipynb`, `05_mcp_and_tools.ipynb`, `08_agent_security.ipynb` | Frameworks, tool protocols, security |
| 🔹 | `04_multi_agent_frameworks`, `06_agent_observability`, `07_advanced_agent_frameworks` | |

## Stage 11: Shipping AI: APIs, deployment & MLOps (5–7 weeks; +3–4 weeks for the software-engineering and data-engineering rows)

| | What | Why |
|---|---|---|
| ⭐ | `12_FastAPI/01`–`03`, 🏭 `04_industry_production_ml_api.ipynb` | Serving a model behind an API |
| ⭐ | `17_Docker/01_docker_basics.ipynb`, `02_docker_for_ml.ipynb`, 🏭 `04_industry_containerizing_an_ml_service.ipynb` | Packaging your app so it runs anywhere |
| ⭐ | `16_Deployment/01_deployment_concepts.ipynb`, `02_streamlit_gradio.ipynb`, 🏭 `05_industry_safe_model_rollout_strategies.ipynb` | Demos, deployment options, safe rollouts |
| ⭐ | `15_MLOps/01_experiment_tracking/01_mlflow.ipynb`, `05_model_registry/`, `06_monitoring/`, `07_testing_in_ml/`, 🏭 `15_industry_end_to_end_mlops_pipeline.ipynb` | Tracking, versioning, testing and monitoring models |
| ✅ | `20_Git_and_DevOps/02`–`04`, `13_Databases/03_vector_db/`, `18_Cloud/01_aws_for_ai.ipynb`, 🏭 `18_Cloud/05_industry_cloud_ml_architecture_and_cost_planning.ipynb` | CI/CD, vector databases, cloud basics |
| 🔹 | Rest of `13_Databases`, `15_MLOps`, `16_Deployment`, `17_Docker/03` + `kubernetes/`, `18_Cloud/02`–`04` | Many cells here *show* code for services you would need to install or pay for |
| ✅ | `15_MLOps/16_observability_hands_on.ipynb` | Seeing a live model from the outside: JSON logs, Prometheus metrics, OpenTelemetry traces, SLOs, drift alerts |
| ✅🎓 | `13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb` | Data bigger than your RAM: MapReduce from scratch, chunking, Parquet, DuckDB/Polars |
| 🔹🎓 | `13_Databases/06_data_engineering/03_spark_locally.ipynb` | Apache Spark on your laptop: RDDs, shuffles, DataFrames and Spark SQL (needs Java; otherwise cells skip) |
| 🔹🎓 | `13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb` | Answers that update as data arrives: windows, watermarks, exactly-once, backpressure |

Software engineering for production, from [`23_Software_Engineering/`](23_Software_Engineering/README.md) (notes: `23_Software_Engineering/notes/23_Software_Engineering.md`). Do it before or alongside the rows above:

| | What | Why |
|---|---|---|
| ✅ | `23_Software_Engineering/04_debugging_and_profiling.ipynb` | Finding *why* code is wrong or slow: tracebacks, logging, `pdb`, profilers, memory |
| ✅ | `05_concurrency_and_async.ipynb` | Doing many things at once: threads, processes, the GIL, `asyncio`, request batching |
| 🔹🎓 | `06_operating_systems_for_developers.ipynb` | The OS course for developers: processes, scheduling, memory, file systems, signals |
| ✅🎓 | `07_computer_networks_for_ai_apps.ipynb` | How apps talk: DNS, TCP, HTTP, TLS, REST, streaming (SSE/WebSockets) and CORS |
| ⭐🎓 | `08_security_for_ai_applications.ipynb` | Keeping attackers out: OWASP Top 10 (web and LLM), auth, secrets, supply chain |
| ✅ | `09_system_design_fundamentals.ipynb` | Keeping an app working for millions: load balancing, caching, queues, rate limits |
| ✅ | `10_connecting_ai_to_a_frontend.ipynb` | Putting a web page in front of your model: FastAPI backend plus a plain HTML/JS frontend |
| ⭐🏭 | `11_industry_building_and_shipping_an_ai_feature.ipynb` | One AI feature from design doc to tests, security review, CI and canary rollout |
| 🔹🎓 | `12_computer_architecture_for_ai_performance.ipynb` | Bits, CPUs, caches, SIMD and GPUs: why some AI code is fast and some is slow |

## Stage 12: Capstone projects (4–8 weeks)

Build these in order. Each folder has a `README.md` with tested run steps and its known issues.

| | Project | Uses stages |
|---|---|---|
| ⭐ | `21_Projects/01_ml_pipeline/` | 5, 11 |
| ⭐ | `21_Projects/02_rag_chatbot/` | 9, 11 |
| ✅ | `21_Projects/03_computer_vision_app/` | 8, 11 |
| ✅ | `21_Projects/04_forecasting_dashboard/` | 6, 11 |
| 🔹🔑 | `21_Projects/05_multi_agent_system/` | 10, 11 |
| ⭐ | `21_Projects/06_production_model/` | 11 |

**Then build one project of your own**, on data you care about. That is what employers remember.

## Stage 13: System design & career

| | What | Why |
|---|---|---|
| ✅ | `22_ML_System_Design/01`–`07`, 🏭 `08_industry_system_design_case_study.ipynb` | How to design whole ML systems; asked in most ML engineering interviews |
| ✅ | The [career checklist](#-after-the-path-portfolio--job-checklist) below | |

## Stage 13b: Research methods & thesis (degree routes; 4–6 weeks + thesis)

How to ask a research question, run a fair study and write it up so others can check it. Folder guide: [`24_Research_Methods/`](24_Research_Methods/README.md). Route (b) does `01`–`05` for its final-year project; route (c) does all six and then the thesis. On the job route it is optional, but `02`–`04` make you much better at proving that a model really helps.

| | What | Why |
|---|---|---|
| 🔹🎓 | `24_Research_Methods/01_research_methodology_and_literature_review.ipynb` | Turning a topic into a research question, finding and reading papers, a literature review, the MS/MPhil proposal |
| 🔹🎓 | `02_experiment_design_for_ml.ipynb` | Fair tests for models: baselines, controls, power analysis, threats to validity, pre-registration |
| 🔹🎓 | `03_statistical_significance_and_reporting.ipynb` | Is the improvement real or luck? Paired tests, multiple comparisons, effect sizes, honest reporting |
| 🔹🎓 | `04_reproducibility_and_research_code.ipynb` | Making results someone else can re-run: seeds, pinned environments, configs, tracking, datasheets |
| 🔹🎓 | `05_paper_writing_and_publishing.ipynb` | Writing a paper: structure, clear sentences, figures, tables, LaTeX, peer review |
| 🔹🔬🏭 | `06_industry_running_a_research_project_end_to_end.ipynb` | A complete small study, from question and pre-registered plan to statistics and a written report |

**The thesis = capstone + research project.** Take one Stage 12 capstone (or your own project) as the engineering base, then add a real research question on top of it: a literature review (`01`), a pre-registered plan (`02`), baselines and ablations over several seeds (`02`–`03`), reproducible code (`04`) and a written thesis or paper (`05`). Allow **4–6 months** at 10–15 h/week. Use `06` as the worked example.

## Optional tracks (any time after Stage 7)

| Track | Where | Start with |
|---|---|---|
| Reinforcement learning (🔬 core for route (c)) | `11_Reinforcement_Learning/` | `01_rl_fundamentals` → `07_multi_armed_bandits` (simplest) → `02`–`05` → 🏭 `08_industry_inventory_control_with_rl` → `06_advanced_rl`. Hands-on, all on CPU: `09_tabular_rl_from_scratch` (GridWorld with dynamic programming, Monte Carlo, Q-learning and SARSA, built by hand) and `10_deep_rl_on_cpu` (DQN, REINFORCE, A2C and PPO from scratch on CartPole) |
| Advanced AI safety & policy | `19_AI_Ethics_and_Safety/` | `01`, `02`, `04`, `05`, then 🏭 `09_industry_ai_incident_response_and_red_teaming` |
| Advanced MLOps | `15_MLOps/02`–`04`, `08`–`14` | `02_data_versioning`, `03_pipeline_orchestration` |
| Domain electives (🔹) | [`03_Machine_Learning/18_domain_applications/`](03_Machine_Learning/18_domain_applications/README.md) | `01_geospatial_machine_learning` (ML on maps: coordinates, spatial features, spatial cross-validation, hotspots) and `02_bioinformatics_sequence_ml` (ML on DNA and proteins: alignment, k-mers, HMMs, sequence classifiers) |

---

<a id="degree-map"></a>

## 🗺️ Degree map

Use these tables to check that your study covers a typical degree. Course names vary between universities; match yours by topic. General-education courses (English, physics, humanities) and a university's exams and credits are not covered: this repo gives you the knowledge, not the certificate.

### BS AI / BS Data Science courses

| Typical BS course | Where in this repo | Stage |
|---|---|---|
| Programming Fundamentals | `01_Python/00`–`02`, `04` | 0, 2 |
| Object-Oriented Programming | `01_Python/03_advanced`, `23_Software_Engineering/01`–`02` | 2 |
| Data Structures & Algorithms | [`00_AI_Fundamentals/dsa/`](00_AI_Fundamentals/dsa/README.md) | 2b |
| Discrete Structures | [`14_Mathematics/discrete_math/`](14_Mathematics/discrete_math/README.md) `01`–`03` | 4 |
| Theory of Automata / Computation | `14_Mathematics/discrete_math/04`–`05` | 4 |
| Database Systems (DBMS) | [`13_Databases/00_dbms_fundamentals/`](13_Databases/00_dbms_fundamentals/README.md), `13_Databases/01_sql/`, `02_nosql/` | 3 |
| Operating Systems | `23_Software_Engineering/06`, `05` (concurrency) | 11 |
| Computer Networks | `23_Software_Engineering/07` | 11 |
| Computer Organisation & Architecture | `23_Software_Engineering/12` | 11 |
| Software Engineering | [`23_Software_Engineering/`](23_Software_Engineering/README.md), `20_Git_and_DevOps/`, `22_ML_System_Design/` | 2, 11, 13 |
| Linear Algebra | `14_Mathematics/01`, `10` | 4 |
| Calculus (incl. multivariable) | `14_Mathematics/02`, `11` | 4 |
| Probability & Statistics | `14_Mathematics/03`–`04`, `02_Data_Analysis/08`, `13` | 3, 4 |
| Numerical Computing | `14_Mathematics/09`–`10` | 4 |
| Artificial Intelligence | [`00_AI_Fundamentals/classical_ai/`](00_AI_Fundamentals/classical_ai/README.md) | 1b |
| Machine Learning | `03_Machine_Learning/` (⭐ and ✅ rows) | 5 |
| Deep Learning | `05_Deep_Learning/` (incl. `18` from scratch) | 7 |
| Natural Language Processing | `07_NLP/` | 8 |
| Computer Vision | `06_Computer_Vision/` | 8 |
| Data Mining | `03_Machine_Learning/02_unsupervised/` (incl. `05`), `03_association_rules`, `08_anomaly_detection/`, `09_recommendation_systems/` | 5 |
| Big Data Analytics | `13_Databases/06_data_engineering/` `02`–`04`, `02_Data_Analysis/09_polars`, `10_duckdb` | 3, 11 |
| Data Visualisation | `02_Data_Analysis/04`–`06`, `15` | 3 |
| Data Acquisition & Wrangling | `02_Data_Analysis/01`, `12` | 3 |
| Information Security | `23_Software_Engineering/08`, `00_AI_Fundamentals/04`, `08_LLM/16`, `09_Prompt_Engineering/04`, `10_Agents/08` | 9–11 |
| Professional Ethics / Responsible AI | `00_AI_Fundamentals/01`–`07`, `19_AI_Ethics_and_Safety/` | 1, tracks |
| Cloud Computing (elective) | `17_Docker/`, `18_Cloud/`, `16_Deployment/` | 11 |
| Time Series / Forecasting (elective) | `04_Forecasting/` | 6 |
| Research Methodology | [`24_Research_Methods/`](24_Research_Methods/README.md) `01`–`05` | 13b |
| Final Year Project | `21_Projects/` + your own project, written up with `24_Research_Methods/05` | 12, 13b |

### MS / MPhil AI & Data Science courses

| Typical MS / MPhil course | Where in this repo | Stage |
|---|---|---|
| **Core:** Advanced Algorithms / Design & Analysis of Algorithms | [`00_AI_Fundamentals/advanced_algorithms/`](00_AI_Fundamentals/advanced_algorithms/README.md) | 2b |
| **Core:** Statistical Learning Theory | [`03_Machine_Learning/16_learning_theory/`](03_Machine_Learning/16_learning_theory/README.md), `03_Machine_Learning/06_model_evaluation/` | 5 |
| **Core:** Probabilistic Graphical Models | [`03_Machine_Learning/17_probabilistic_graphical_models/`](03_Machine_Learning/17_probabilistic_graphical_models/README.md), `14_Mathematics/07_bayesian_ml`, `00_AI_Fundamentals/classical_ai/09` | 5 |
| **Core:** Advanced Machine Learning | `16_learning_theory/02` (kernels), `02_unsupervised/05`, `03_semi_supervised/`, `10_causal_inference/`, `13_active_learning/`, `14_conformal_prediction/` (all in `03_Machine_Learning/`) | 5 |
| **Core:** Optimisation | `14_Mathematics/06`, `12`, `00_AI_Fundamentals/advanced_algorithms/05` | 4 |
| **Core:** Research Methods | [`24_Research_Methods/`](24_Research_Methods/README.md) (all six) | 13b |
| Elective: Advanced Deep Learning | `05_Deep_Learning/06`–`15`, `19`–`21` | 7 |
| Elective: Reinforcement Learning | `11_Reinforcement_Learning/` (incl. `09`–`10`) | track |
| Elective: Large Language Models | `08_LLM/` (incl. `21`–`22`), `09_Prompt_Engineering/`, `10_Agents/` | 9, 10 |
| Elective: Advanced NLP | `07_NLP/04`–`11` | 8 |
| Elective: Advanced Computer Vision | `06_Computer_Vision/04`–`10` | 8 |
| Elective: Graph Machine Learning | `05_Deep_Learning/07_gnn`, `21` | 7 |
| Elective: Information Theory | `14_Mathematics/05` | 4 |
| Elective: Big Data & Distributed Systems | `13_Databases/06_data_engineering/`, `00_dbms_fundamentals/09`, `05_Deep_Learning/11`, `advanced_algorithms/10` | 3, 7, 11 |
| Elective: Production ML Systems / MLOps | `15_MLOps/`, `22_ML_System_Design/`, `23_Software_Engineering/09`–`11` | 11, 13 |
| Elective: AI Safety & Ethics | `19_AI_Ethics_and_Safety/` | track |
| Elective: Domain applications | [`03_Machine_Learning/18_domain_applications/`](03_Machine_Learning/18_domain_applications/README.md) | track |
| **Thesis** = capstone + research project | a `21_Projects/` capstone (or your own) + `24_Research_Methods/06` as the model + 4–6 months of your own research | 12, 13b |

---

## 🧰 Extra installs per module

[`requirements-beginner.txt`](requirements-beginner.txt) covers all 🌱 Start Here notebooks and most core notebooks. Some modules need extra packages. Install them only when you reach that module:

| Module | Install when you reach it | Optional (the notebook still runs without them) |
|---|---|---|
| `00_AI_Fundamentals` (incl. `classical_ai/`, `dsa/`, `advanced_algorithms/`) | `pip install networkx` (usually already installed with `torch`) | `numba`, `ortools`, `pulp` |
| `01_Python` | nothing extra | - |
| `02_Data_Analysis` | `pip install beautifulsoup4 duckdb polars pyarrow` | `imbalanced-learn`, `openpyxl` |
| `03_Machine_Learning` | `pip install ctgan dowhy imbalanced-learn lifelines MAPIE mlxtend optuna river` | `catboost`, `faiss-cpu`, `featuretools`, `geopandas`, `interpret`, `lime`, `pyod`, `sacrebleu`, `scikit-surprise`, `shapely`, `umap-learn` |
| `04_Forecasting` | `pip install neuralforecast stumpy` | `arch`, `chronos-forecasting`, `gpytorch`, `MAPIE`, `neuralprophet`, `ngboost`, `pmdarima`, `prophet`, `pytorch-forecasting`, `timesfm` |
| `05_Deep_Learning` | `pip install evaluate onnx onnxruntime peft` | `torchdiffeq`, `torch-geometric` |
| `06_Computer_Vision` | `pip install faiss-cpu opencv-python-headless scikit-image timm` | `monai`, `pydicom` |
| `07_NLP` | `pip install faiss-cpu gensim keybert nltk rank-bm25 spacy yake` | `bertopic`, `fastcoref`, `langdetect`, `laserembeddings`, `librosa`, `mteb`, `openai`, `rouge-score`, `voyageai` |
| `08_LLM` | `pip install anthropic faiss-cpu google-genai haystack-ai langchain-community langchain-core langchain-openai langchain-text-splitters llama-index nltk ollama openai peft pytest rank-bm25 rouge-score trl` | `cohere`, `FlagEmbedding`, `instructor`, `sacrebleu` |
| `09_Prompt_Engineering` | `pip install anthropic dspy google-genai instructor openai` | - |
| `10_Agents` | `pip install ag2 crewai crewai-tools langchain-core langchain-openai langgraph langsmith nest-asyncio openai pydantic-ai smolagents` | `anthropic`, `faiss-cpu` |
| `11_Reinforcement_Learning` | `pip install gymnasium stable-baselines3` | - |
| `12_FastAPI` | `pip install pyjwt "pwdlib[bcrypt]" pytest` | - |
| `13_Databases` (incl. `00_dbms_fundamentals/`, `06_data_engineering/`) | `pip install duckdb networkx psutil pyarrow` | `dask`, `polars`, `pyspark` (Spark also needs Java 17 or 21) |
| `14_Mathematics` (incl. `discrete_math/`) | `pip install arviz networkx pymc` | `cvxpy` |
| `15_MLOps` | `pip install aim arize-phoenix ax-platform bentoml boto3 clearml comet-llm comet-ml dagshub google-genai great-expectations mlflow neptune opentelemetry-sdk optuna pandera prefect prometheus-client pytest sacred sagemaker wandb` | `feast`, `langfuse`, `tensorflow` |
| `16_Deployment` | `pip install onnxruntime` | - |
| `17_Docker` | nothing extra | - |
| `18_Cloud` | `pip install boto3 sagemaker` | - |
| `19_AI_Ethics_and_Safety` | nothing extra | - |
| `20_Git_and_DevOps` | nothing extra | - |
| `21_Projects` | Each project has its own `requirements.txt`; follow the `README.md` inside the project folder | - |
| `22_ML_System_Design` | `pip install faiss-cpu` | - |
| `23_Software_Engineering` | `pip install pytest` | `coverage`, `hypothesis`, `line_profiler`, `numba`, `psutil`, `pwdlib`, `pydantic-settings`, `pyjwt`, `pytest-cov`, `ruff`, `safetensors`, `websockets` |
| `24_Research_Methods` | `pip install mlflow` | - |

> 💡 The pip name is sometimes different from the import name: `cv2` → `opencv-python-headless`, `faiss` → `faiss-cpu`, `sklearn` → `scikit-learn`, `imblearn` → `imbalanced-learn`, `bs4` → `beautifulsoup4`, `umap` → `umap-learn`, `torch_geometric` → `torch-geometric`, `jwt` → `pyjwt`. The complete, pinned list for everything is the root `requirements.txt` (Python 3.12+).

**API keys, GPUs and external services:** 🔑 notebooks use a paid API only if you set its key (e.g. `OPENAI_API_KEY`). Without one they fall back to a free local model or print a clear *"skipped: needs X"* message. No notebook requires a GPU: GPU-heavy parts use small CPU stand-ins or skip with a message. Cells that need a cloud account or a database server (`13_Databases`, `16`–`18`) show the example code and explain what you would need to run it for real; the 🏭 notebooks in those folders run fully offline.

---

## 🎯 After the path: portfolio & job checklist

- [ ] **GitHub profile** with 3–5 pinned projects. Each needs a README with: the problem, the data, the approach, the results (with a baseline), how to run it, and what you would do next.
- [ ] **At least one end-to-end project** you can demo live: data → model → API → simple UI, deployed somewhere free.
- [ ] **One project with an LLM** (RAG or an agent) that includes an evaluation, not just a demo.
- [ ] **Explain every project in 2 minutes**: what, why, how you measured it, and what went wrong.
- [ ] **Production habits in every project:** tests, logging, a security check and a short design doc (`23_Software_Engineering/03`, `08`, `11`).
- [ ] **Degree routes:** a written report (BS) or thesis (MS/MPhil) with a literature review, baselines, several seeds and significance tests (Stage 13b).
- [ ] **Interview basics:** Python, DSA (Stage 2b and the `advanced_algorithms/09` coding interview workbook) and SQL exercises; the ML fundamentals from Stage 5 (bias/variance, leakage, metrics, cross-validation); ML system design (Stage 13).
- [ ] **Keep learning:** follow the resources in the main [`README.md`](README.md#-mega-resource-library), read one paper or blog post a week, and write about what you build.
