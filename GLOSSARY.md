# Glossary: AI, ML, Computer Science, Data and MLOps Terms in Plain English

**Jump to:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x) · [Y](#y) · [Z](#z)

## How to use this glossary

- **Stuck on a word?** Press `Ctrl+F` (or `Cmd+F` on a Mac), type the word, and jump straight to it. Terms are sorted A to Z, and abbreviations are spelled out (for example, *RAG* is under **R**).
- **Each entry has three parts:** a short plain-English definition, an everyday analogy or tiny example (where it helps), and a **See:** link to the notebook or notes file in this repo where the idea is taught best. All links are relative, so they work on GitHub and in your editor.
- **You don't need to read it front to back.** Come back whenever a notebook uses a word you don't know yet. Words in *italics* inside a definition usually have their own entry.
- **It covers the whole repo:** AI and machine learning, deep learning and LLMs, plus the computer-science foundations (algorithms, databases, discrete math, software engineering, networking, security) and research methods. 459 terms in all.
- **Definitions are kept simple on purpose.** They give you the main idea, not every technical detail. The linked notebook has the full story, with code.

---

## A

**A\* Search** — A pathfinding algorithm that always expands the node with the lowest *f = g + h*, where *g* is the cost so far and *h* is a *heuristic* guess of the cost still to go. With an *admissible heuristic* it is guaranteed to find the cheapest path. *Example:* map apps use the straight-line distance to the destination as *h*. See: [00_AI_Fundamentals/classical_ai/03_informed_search.ipynb](00_AI_Fundamentals/classical_ai/03_informed_search.ipynb)

**A/B Testing** — An experiment where you show two versions of something (A = the current one, B = the new one) to two random groups of users and measure which works better. *Example:* half of your visitors see a green "Buy" button and half see a blue one, then you compare how many people buy. See: [03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb](03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb)

**Ablation Study** — An experiment that removes or replaces one part of a system at a time to measure how much that part really contributes. *Example:* train the model without data augmentation, then without the attention layer, and compare each with the full model. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Accuracy** — The share of predictions a model gets right: correct predictions divided by all predictions. It can mislead when one class is rare: a model that always says "no fraud" is 99% accurate if only 1% of cases are fraud. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**ACID** — The four guarantees of a database *transaction*: **A**tomicity (all of it happens or none of it), **C**onsistency (rules such as "balance ≥ 0" stay true), **I**solation (concurrent transactions do not see each other's half-done work) and **D**urability (once committed, it survives a crash). *Example:* a bank transfer must never take money from one account without adding it to the other. See: [13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb](13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb)

**Activation Function** — A simple math function applied to each neuron's output that lets a neural network learn curved, non-straight-line patterns. Common ones are *ReLU*, *sigmoid* and tanh. Without it, stacking layers would be no more powerful than one straight line. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Active Learning** — A way to save labeling effort: the model picks the examples it is most unsure about and asks a human to label only those. *Analogy:* a student who asks the teacher only about the questions they find confusing. See: [03_Machine_Learning/13_active_learning/01_active_learning.ipynb](03_Machine_Learning/13_active_learning/01_active_learning.ipynb)

**Actor-Critic (A2C)** — A reinforcement-learning method with two parts: the *actor* (the policy that picks actions) and the *critic* (a value function that scores how good the action turned out compared with expectation, called the advantage). The critic's feedback lowers the noise of plain *policy gradient*. See also *PPO*. See: [11_Reinforcement_Learning/05_policy_gradient.ipynb](11_Reinforcement_Learning/05_policy_gradient.ipynb)

**Adam (optimizer)** — A popular *optimizer* for training neural networks. It adjusts the step size for each weight separately, using running averages of recent gradients and their squares, so training is usually fast and stable without much tuning. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Admissible Heuristic** — A *heuristic* that never overestimates the true remaining cost to the goal. It is what makes *A\* search* optimal. *Example:* straight-line distance is admissible for road travel, because no road is shorter than a straight line. See: [00_AI_Fundamentals/classical_ai/03_informed_search.ipynb](00_AI_Fundamentals/classical_ai/03_informed_search.ipynb)

**Adversarial Example** — An input changed very slightly, often invisibly to people, on purpose to fool a model. *Example:* adding faint noise to a photo of a panda so an image classifier confidently says "gibbon". See: [19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb](19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb)

**Agent (AI Agent)** — A program where a language model decides what to do step by step: it reads a goal, chooses a *tool* (search, calculator, code), looks at the result, and repeats until the task is done. *Analogy:* an assistant who can not only answer but also use apps for you. See: [10_Agents/01_agent_fundamentals.ipynb](10_Agents/01_agent_fundamentals.ipynb)

**Alignment** — Making an AI system behave the way people intend: helpful, honest, and avoiding harm. In LLMs this is done with techniques such as *instruction tuning*, *RLHF* and *DPO*. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**All-Reduce (Ring All-Reduce)** — A collective operation where every worker ends up with the sum (or average) of all workers' values. In the ring version each worker passes chunks to its neighbour, so bandwidth per worker stays constant as you add more. It is how gradients are averaged in data-parallel training. See: [00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb)

**Alpha-Beta Pruning** — A speed-up for *minimax* game search that skips branches which cannot change the final decision. It gives exactly the same answer as plain minimax, but with good move ordering it can search about twice as deep in the same time. See: [00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb](00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb)

**Amdahl's Law** — The limit on speed-up from adding processors when part of a job must run serially: speed-up = 1 / (s + (1 − s)/p), where *s* is the serial fraction and *p* the number of processors. *Example:* if 10% of a program is serial, even infinite cores give at most a 10× speed-up. See: [00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb)

**Amortized Analysis** — Measuring the average cost per operation over a whole worst-case sequence, so a rare expensive step is "paid for" by many cheap ones. *Example:* appending to a Python list is O(1) amortized even though the list occasionally doubles its storage and copies everything. See: [00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb)

**Anomaly Detection** — Finding data points that look very different from normal ones. *Example:* a credit-card purchase of $5,000 in another country at 3 a.m. for a customer who usually spends $20 locally. See: [03_Machine_Learning/08_anomaly_detection/01_anomaly_detection.ipynb](03_Machine_Learning/08_anomaly_detection/01_anomaly_detection.ipynb)

**ANOVA (Analysis of Variance)** — A statistical test of whether the means of three or more groups differ, by comparing the variation between groups with the variation within groups. *Example:* testing whether three learning rates give different average accuracy across repeated runs. See: [02_Data_Analysis/14_design_of_experiments.ipynb](02_Data_Analysis/14_design_of_experiments.ipynb)

**API (Application Programming Interface)** — A defined way for one program to ask another program for something. A web API receives a request over the internet (for example "predict the price of this house") and sends back a response, usually as *JSON*. *Analogy:* a restaurant menu and waiter: you order from a fixed list without going into the kitchen. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

**Approximation Algorithm / Approximation Ratio** — A fast algorithm for a hard (*NP-hard*) problem that is guaranteed to come within a fixed factor of the best answer. That factor is the approximation ratio. *Example:* a simple vertex-cover method that is never more than 2× the optimum has ratio 2. See: [00_AI_Fundamentals/advanced_algorithms/03_approximation_and_parameterized_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/03_approximation_and_parameterized_algorithms.ipynb)

**Arc Consistency (AC-3)** — A *CSP* technique that removes any value of a variable that has no compatible value in a neighbouring variable, repeating until nothing changes. It shrinks the search before or during *backtracking*. See: [00_AI_Fundamentals/classical_ai/06_constraint_satisfaction.ipynb](00_AI_Fundamentals/classical_ai/06_constraint_satisfaction.ipynb)

**ARIMA** — A classic time-series forecasting model (AutoRegressive Integrated Moving Average). It predicts the next value from recent past values and recent past errors, after "differencing" the data to remove trends. See: [04_Forecasting/02_classical_methods.ipynb](04_Forecasting/02_classical_methods.ipynb)

**Artificial Intelligence (AI)** — The broad field of making computers do tasks that normally need human intelligence, such as understanding language, recognizing images or making decisions. *Machine learning* is the main way modern AI is built. See: [00_AI_Fundamentals/notes/00_AI_Fundamentals.md](00_AI_Fundamentals/notes/00_AI_Fundamentals.md)

**asyncio** — Python's library for running many tasks concurrently on a single thread. Functions declared with `async def` pause at each `await` (for example while waiting for a network reply) so an *event loop* can run other tasks meanwhile. *Example:* sending 100 LLM API calls at once instead of one after another. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**Attention** — The key idea inside *transformers*: when processing one word, the model looks at all the other words and decides how much each one matters. In "The animal didn't cross the street because **it** was tired", attention helps link "it" to "animal". When a sequence looks at itself like this it is called *self-attention*. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

**AUC / ROC Curve** — The ROC curve plots how many true positives you catch against how many false alarms you raise as you move the decision threshold. AUC (Area Under the Curve) sums it up as one number from 0.5 (coin flip) to 1.0 (perfect). It equals the chance that a random positive example gets a higher score than a random negative one. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**Authentication / Authorization** — Authentication proves *who* you are (password, API key, *JWT*); authorization decides *what* you are allowed to do (read, write, admin). *Analogy:* showing your ID at the door versus the wristband that says which rooms you may enter. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

**Autodiff Modes (Forward / Reverse)** — The two ways *automatic differentiation* can apply the chain rule. Forward mode pushes derivatives from inputs to outputs (cheap when there are few inputs); reverse mode, which *backpropagation* uses, pulls them from the output back to all inputs (cheap when there is one loss and millions of weights). See: [14_Mathematics/11_matrix_calculus_and_autodiff_from_scratch.ipynb](14_Mathematics/11_matrix_calculus_and_autodiff_from_scratch.ipynb)

**Autoencoder** — A neural network trained to copy its input to its output through a narrow middle layer (the bottleneck), so it must learn a compact summary of the data. Used for compression, denoising and anomaly detection. The *VAE* is its generative cousin. See: [05_Deep_Learning/20_generative_models_hands_on.ipynb](05_Deep_Learning/20_generative_models_hands_on.ipynb)

**Autograd (Automatic Differentiation)** — A library feature (in PyTorch, for example) that works out *gradients* for you automatically, by recording every math operation and applying the chain rule of calculus backwards. This is what makes *backpropagation* easy. See: [14_Mathematics/02_calculus.ipynb](14_Mathematics/02_calculus.ipynb)

**Automaton (DFA / NFA)** — A simple abstract machine that reads a string one symbol at a time, moves between a finite set of states, and accepts or rejects. A DFA has exactly one next state per symbol; an NFA may have several. Both recognise exactly the *regular languages*. *Example:* a vending machine that tracks how much money has been inserted. See: [14_Mathematics/discrete_math/04_automata_and_regular_languages.ipynb](14_Mathematics/discrete_math/04_automata_and_regular_languages.ipynb)

**AutoML (Automated Machine Learning)** — Tools that automatically try models, features and *hyperparameters* and pick the best combination under a time or compute budget. *Examples:* Optuna, H2O AutoML, auto-sklearn. You still have to define the problem, the metric and a clean validation set. See: [15_MLOps/08_automl/01_automl.ipynb](15_MLOps/08_automl/01_automl.ipynb)

## B

**B+ Tree** — The standard database index: a wide, shallow, always-balanced search tree whose leaves hold the keys in sorted order and are linked together. Because each node fills a whole disk page, finding one row among millions takes only 3 or 4 page reads, and range queries just walk along the leaves. See: [13_Databases/00_dbms_fundamentals/07_indexing_b_trees_and_hashing.ipynb](13_Databases/00_dbms_fundamentals/07_indexing_b_trees_and_hashing.ipynb)

**Backpressure** — A way for a slow consumer to make a fast producer slow down instead of being flooded, usually with a bounded queue that blocks when full. *Analogy:* a restaurant that stops seating people when the kitchen is full. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Backpropagation** — The method neural networks use to learn: after a prediction, compute how wrong it was (the *loss*), then work backwards through the layers to find how much each weight contributed to the error, so each weight can be nudged in the right direction. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Backtracking** — Building a solution one choice at a time and undoing the last choice as soon as it leads to a dead end. *Example:* solving a Sudoku by trying a digit, moving on, and erasing it when a conflict appears. Used for puzzles, *CSPs* and generating all combinations. See: [00_AI_Fundamentals/dsa/10_backtracking.ipynb](00_AI_Fundamentals/dsa/10_backtracking.ipynb)

**Batch / Mini-batch / Batch Size** — Instead of learning from one example or the whole dataset at once, neural networks usually learn from small groups called mini-batches (for example 32 examples). The batch size is how many examples are in each group. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**Batch Normalization** — A layer that rescales each feature inside a neural network to mean 0 and variance 1 over the current mini-batch, then applies a learned scale and shift. It usually makes training faster and more stable. Transformers use the related layer normalization instead. See: [05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb](05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb)

**Bayes' Theorem** — A formula for updating a belief when you see new evidence: new belief = old belief × how well the evidence fits, rescaled. *Example:* how likely you are to have a disease given a positive test depends on how common the disease is, not just on how accurate the test is. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**Bayesian Network** — A graph of random variables where arrows show direct influence and each node stores a table of probabilities given its parents. Together they define a full joint probability you can query. *Example:* Burglary → Alarm ← Earthquake, so hearing the alarm raises the chance of both causes. See: [00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb](00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb)

**Bayesian Optimization** — A sample-efficient way to tune *hyperparameters*: fit a cheap surrogate model (often a *Gaussian process*) to the results so far, then pick the next setting where an acquisition function (such as expected improvement) is highest. It needs far fewer expensive training runs than *grid search*. See: [15_MLOps/08_automl/02_automl_from_scratch.ipynb](15_MLOps/08_automl/02_automl_from_scratch.ipynb)

**BCNF (Boyce-Codd Normal Form)** — A strict *normal form*: for every *functional dependency* X → Y in a table, X must be a key. It removes redundancy that 3NF can still allow. *Example:* if each instructor teaches one course, store (instructor, course) in its own table instead of repeating it on every student row. See: [13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb](13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb)

**Beam Search** — A decoding method that keeps the *k* most likely partial outputs at each step instead of only the single best (greedy) one. It often finds better overall sequences in translation or summarization, at *k* times the cost. See: [05_Deep_Learning/19_sequence_models_hands_on.ipynb](05_Deep_Learning/19_sequence_models_hands_on.ipynb)

**Belief Propagation** — An inference algorithm for graphical models where nodes pass "messages" (summaries of what they know) to their neighbours. It gives exact marginal probabilities on tree-shaped graphs and good approximations on graphs with loops (loopy BP). See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

**Bellman Equation** — The recursive rule at the heart of reinforcement learning: the value of a state equals the immediate *reward* plus the discounted value of the next state. *Value iteration*, *Q-learning* and *DQN* are all ways of solving it. See: [11_Reinforcement_Learning/01_rl_fundamentals.ipynb](11_Reinforcement_Learning/01_rl_fundamentals.ipynb)

**BERT** — A well-known *transformer* model (from 2018) that reads text in both directions at once. It is an *encoder* model, good at understanding tasks such as classification, search and named-entity recognition rather than writing long text. See: [07_NLP/notes/07_NLP.md](07_NLP/notes/07_NLP.md)

**BFS / DFS (Breadth-First / Depth-First Search)** — The two basic ways to explore a graph. BFS visits nodes layer by layer with a queue and finds shortest paths when every edge costs the same; DFS goes as deep as possible with a stack (or recursion) before backing up, and is used for cycle detection and *topological sort*. See: [00_AI_Fundamentals/dsa/07_graphs.ipynb](00_AI_Fundamentals/dsa/07_graphs.ipynb)

**Bias (Fairness)** — When an AI system treats some groups of people unfairly, often because its training data reflected past unfairness. *Example:* a hiring model trained on past hires that mostly favored one group learns to repeat that preference. See: [19_AI_Ethics_and_Safety/01_bias_fairness.ipynb](19_AI_Ethics_and_Safety/01_bias_fairness.ipynb)

**Bias-Variance Tradeoff** — Two ways a model can be wrong. *Bias*: it is too simple and misses the pattern (*underfitting*). *Variance*: it is too sensitive to the exact training data (*overfitting*). Making a model more flexible usually lowers bias but raises variance, so you look for a balance. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Big-O / Big-Θ / Big-Ω** — Notation for how running time or memory grows with input size *n*, ignoring constants. O is an upper bound, Ω a lower bound, Θ a tight bound (both). *Example:* scanning a list is O(n); binary search is O(log n); comparing every pair is O(n²). See: [00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb](00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb)

**Binary Search** — Finding a value in sorted data by checking the middle and throwing away the half that cannot contain it, so a million items need only about 20 checks (O(log n)). *Analogy:* opening a dictionary near the middle and flipping toward the right letter. See: [00_AI_Fundamentals/dsa/03_searching_and_sorting.ipynb](00_AI_Fundamentals/dsa/03_searching_and_sorting.ipynb)

**Binary Search Tree (BST)** — A tree where every node's left subtree holds smaller keys and its right subtree larger keys, so search, insert and delete take time proportional to the tree's height. Unbalanced trees can degrade to a list; see *self-balancing BST*. See: [00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb](00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb)

**BLEU / ROUGE** — Scores that compare generated text with a human-written reference by counting overlapping words and word sequences. BLEU is common for translation, ROUGE for summaries. They are fast and cheap, but they miss meaning (a correct paraphrase can score low). See: [08_LLM/08_evaluation/01_llm_evaluation.ipynb](08_LLM/08_evaluation/01_llm_evaluation.ipynb)

**Bloom Filter** — A compact bit array that answers "is this item in the set?" with either "definitely not" or "probably yes". It never gives false negatives, uses far less memory than storing the items, and is used to skip pointless disk or network lookups. See: [00_AI_Fundamentals/dsa/04_hashing.ipynb](00_AI_Fundamentals/dsa/04_hashing.ipynb)

**BM25** — A classic keyword-search scoring formula. A document scores higher when it contains the query's words often, especially rare words, with an adjustment so long documents don't win just by being long. It is still a strong baseline and is often combined with *embeddings* in "hybrid search", which merges keyword and meaning-based results. See: [08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb](08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb)

**Boosting / Gradient Boosting** — Building a strong model from many small, weak ones (usually shallow *decision trees*) trained one after another, where each new tree focuses on fixing the mistakes of the trees before it. *XGBoost* and LightGBM are popular libraries for this. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**Bootstrap** — Estimating the uncertainty of any statistic by resampling your data with replacement many times and recomputing the statistic each time. The spread of those results gives a *confidence interval*. *Example:* a 95% CI for a model's F1 score from 1,000 resampled test sets. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**BPTT (Backpropagation Through Time)** — How an *RNN* is trained: unroll it over the time steps of a sequence and run ordinary *backpropagation* through the unrolled copy. Long sequences make gradients vanish or explode, which motivated *LSTM*, *GRU* and gradient clipping. See: [05_Deep_Learning/19_sequence_models_hands_on.ipynb](05_Deep_Learning/19_sequence_models_hands_on.ipynb)

**Branch and Bound** — A smart exhaustive search for optimisation problems: split the problem into cases (branch) and drop any case whose best possible value (bound) cannot beat the best solution found so far. It is how solvers handle *integer programming*. See: [00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb](00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb)

## C

**Caching (Cache-Aside, TTL)** — Keeping copies of slow-to-get results in fast storage so repeated requests are quick. In cache-aside the app checks the cache first and fills it on a miss; a TTL (time to live) makes entries expire so data does not go stale. *Example:* caching identical LLM prompts to save cost. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**CAP Theorem** — In a distributed data store, when the network splits (a partition), you must choose between Consistency (every read sees the latest write) and Availability (every request gets an answer). *Example:* a bank ledger prefers consistency; a social-media like counter prefers availability. *PACELC* extends it to normal operation (latency vs consistency). See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Catastrophic Forgetting** — When fine-tuning a model on a new task makes it lose skills it had before. Common fixes are mixing some original data back in (replay), using *LoRA* or other *PEFT* methods, and lower learning rates. See: [08_LLM/21_fine_tuning_hands_on_cpu.ipynb](08_LLM/21_fine_tuning_hands_on_cpu.ipynb)

**Causal Inference** — Methods for answering "did X actually *cause* Y?" rather than just "do X and Y move together?". *Example:* did the discount email cause more purchases, or were the people who got it already more likely to buy? See: [03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb](03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb)

**Chain of Thought (CoT)** — A prompting technique that asks the model to show its reasoning step by step before giving the final answer. It often improves accuracy on math and logic problems. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

**Chat Template** — The exact text format a chat model expects, with special tokens marking system, user and assistant turns. Fine-tuning data must use the model's own template, and usually only the assistant's tokens are counted in the loss (loss masking). See: [08_LLM/21_fine_tuning_hands_on_cpu.ipynb](08_LLM/21_fine_tuning_hands_on_cpu.ipynb)

**Chomsky Hierarchy** — The ladder of language classes, each recognised by a more powerful machine: regular (finite automata) ⊂ context-free (pushdown automata) ⊂ context-sensitive ⊂ recursively enumerable (*Turing machines*). See: [14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb](14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb)

**Chunking** — Cutting long documents into smaller pieces (chunks) before turning them into *embeddings* for search or *RAG*. Chunks that are too big blur the meaning; chunks that are too small lose context. See: [08_LLM/02_rag/01_rag_fundamentals.ipynb](08_LLM/02_rag/01_rag_fundamentals.ipynb)

**CI/CD (Continuous Integration / Continuous Delivery)** — Automation that runs tests on every code change (CI) and, if they pass, packages and ships the change (CD). For ML this can also include data checks and model-quality checks. See: [15_MLOps/04_ci_cd_for_ml/01_cicd_ml.ipynb](15_MLOps/04_ci_cd_for_ml/01_cicd_ml.ipynb)

**Circuit Breaker** — A resilience pattern that stops calling a dependency that keeps failing, returns a fallback straight away, and tries again after a cool-down. *Analogy:* the breaker in your house that trips instead of letting a faulty appliance start a fire. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Class Imbalance** — When one category is much rarer than another in your data (for example 1 fraud case per 1,000 transactions). Models then tend to ignore the rare class unless you rebalance the data, reweight the classes or pick better metrics. See: [03_Machine_Learning/05_feature_engineering/02_imbalanced_data.ipynb](03_Machine_Learning/05_feature_engineering/02_imbalanced_data.ipynb)

**Classification** — A *supervised learning* task where the answer is a category. *Examples:* spam or not spam, which digit (0-9) is in an image. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**Clustering** — Grouping similar data points together without being told the groups in advance (*unsupervised learning*). *Example:* splitting customers into "bargain hunters", "loyal regulars" and so on based on how they shop. See: [03_Machine_Learning/02_unsupervised/01_clustering.ipynb](03_Machine_Learning/02_unsupervised/01_clustering.ipynb)

**CNN (Convolutional Neural Network)** — A neural network designed for grid-like data such as images. It slides small filters across the image to detect edges, then shapes, then objects, layer by layer. See: [05_Deep_Learning/03_cnn.ipynb](05_Deep_Learning/03_cnn.ipynb)

**Cohen's Kappa** — A measure of how much two annotators agree beyond what chance alone would give: 1 is perfect agreement, 0 is chance level. Used to check label quality and LLM-judge reliability. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Columnar Storage / Parquet** — Storing a table column by column instead of row by row. Analytical queries then read only the columns they need, and similar values compress very well. Parquet is the standard columnar file format for data lakes and ML datasets. See: [13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb](13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb)

**Concurrency vs Parallelism** — Concurrency is juggling several tasks so they make progress in overlapping time (good for waiting on networks); parallelism is literally running tasks at the same instant on several cores (good for heavy computation). *Analogy:* one cook switching between pots vs several cooks. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**Condition Number** — How much a problem's output can change when its input changes slightly. A large condition number (ill-conditioned) means small rounding errors can produce big errors in the answer. *Example:* solving with a nearly singular matrix. See: [14_Mathematics/10_numerical_linear_algebra.ipynb](14_Mathematics/10_numerical_linear_algebra.ipynb)

**Confidence Interval (CI)** — A range computed from data that, if you repeated the whole study many times, would contain the true value in (say) 95% of repetitions. Reporting "accuracy 0.84 (95% CI 0.81–0.87)" is far more honest than "0.84" alone. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**Confounder** — A hidden variable that affects both the "treatment" and the outcome, creating a fake link between them. *Example:* ice-cream sales and drowning both rise in summer; temperature is the confounder. Randomization removes confounding. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Confusion Matrix** — A small table that counts a classifier's results: true positives, false positives, true negatives and false negatives. It shows *which* mistakes a model makes, not just how many. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Consistent Hashing** — Placing servers and keys on a circular hash ring so each key belongs to the next server clockwise. Adding or removing a server moves only about 1/N of the keys, instead of nearly all of them as with `hash(key) % N`. Used in caches and sharded databases. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Constraint Satisfaction Problem (CSP)** — A problem described by variables, the values each may take (domains), and rules between them (constraints); a solution assigns every variable without breaking a rule. *Examples:* Sudoku, map colouring, exam timetabling. Solved with *backtracking* plus tricks such as *arc consistency*. See: [00_AI_Fundamentals/classical_ai/06_constraint_satisfaction.ipynb](00_AI_Fundamentals/classical_ai/06_constraint_satisfaction.ipynb)

**Container** — A lightweight, self-contained package of an app plus everything it needs to run (code, libraries, settings), so it runs the same on any machine. *Docker* is the most common tool for building them. *Analogy:* a shipping container that fits on any ship or truck. See: [17_Docker/01_docker_basics.ipynb](17_Docker/01_docker_basics.ipynb)

**Contamination (Benchmark / Data Contamination)** — When test questions, or close copies, were in a model's training data, so its benchmark score overstates real ability. Checked with n-gram overlap searches and fresh, private test sets. See: [08_LLM/22_llm_evaluation_hands_on.ipynb](08_LLM/22_llm_evaluation_hands_on.ipynb)

**Context Window** — The maximum amount of text (measured in *tokens*) an LLM can look at in one go, including your prompt, any documents you paste in, and its own reply. Anything beyond it is cut off or forgotten. See: [08_LLM/04_different_llms/notes/04_different_llms.md](08_LLM/04_different_llms/notes/04_different_llms.md)

**Context-Free Grammar (CFG)** — A set of rewrite rules such as `Expr → Expr + Term`, each with one symbol on the left, that generates a language with nesting (balanced brackets, arithmetic, most programming-language syntax). A parser recovers the parse tree; a pushdown automaton recognises the same languages. See: [14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb](14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb)

**Convex Optimization / Convexity** — A function is convex if the straight line between any two points on its graph lies on or above the graph (a bowl shape). Minimising a convex function over a convex set has no bad local minima, so any minimum found is the global one. Linear and logistic regression and SVMs are convex; deep networks are not. See: [14_Mathematics/12_convex_optimization_and_duality.ipynb](14_Mathematics/12_convex_optimization_and_duality.ipynb)

**Correlation** — A number from -1 to +1 showing how strongly two things move together in a straight-line way. +1 means they rise together perfectly, -1 means one rises as the other falls, and 0 means no linear link. Correlation does not prove causation. See: [02_Data_Analysis/notes/02_Data_Analysis.md](02_Data_Analysis/notes/02_Data_Analysis.md)

**CORS (Cross-Origin Resource Sharing)** — The browser rule that blocks a web page from reading responses from a different origin (domain, port or scheme) unless that server explicitly allows it with `Access-Control-Allow-Origin` headers. It is why a front end on port 3000 cannot call your API on port 8000 until you configure CORS. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Cosine Similarity** — A measure of how similar two vectors (such as two *embeddings*) are by the angle between them: 1 means pointing the same way (very similar), 0 means unrelated. It is the standard way to compare text embeddings. See: [07_NLP/09_sentence_embeddings_advanced.ipynb](07_NLP/09_sentence_embeddings_advanced.ipynb)

**Count-Min Sketch** — A tiny table of counters, updated through several hash functions, that estimates how often each item appeared in a huge stream. It may overestimate but never underestimates. *Example:* finding the most frequent search queries without storing every query. See: [00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb)

**CRF (Conditional Random Field)** — A probabilistic model for labelling sequences that scores whole label sequences, so neighbouring labels influence each other. Classic for *named entity recognition* and part-of-speech tagging; decoded with the *Viterbi algorithm*. See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

**Cross-Encoder / Reranker** — A model that reads a query and one document *together* and scores how relevant they are. It is more accurate but slower than comparing embeddings, so it is typically used to re-sort the top results from a fast first search. See: [08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb](08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb)

**Cross-Entropy Loss** — The usual *loss function* for classification. It is small when the model gives high probability to the correct answer and grows sharply when the model is confidently wrong. See: [14_Mathematics/05_information_theory.ipynb](14_Mathematics/05_information_theory.ipynb)

**Cross-Validation** — A fairer way to test a model: split the data into k parts (folds), train on k-1 of them and test on the remaining one, rotate through all folds, then average the scores. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**CUPED** — A variance-reduction method for A/B tests that adjusts each user's outcome using the same metric measured before the experiment. Removing that predictable part shrinks noise, so the test needs fewer users or less time for the same *statistical power*. See: [02_Data_Analysis/14_design_of_experiments.ipynb](02_Data_Analysis/14_design_of_experiments.ipynb)

**Curse of Dimensionality** — The many problems that appear as the number of features grows: data becomes sparse, distances between points become nearly equal, and tree indexes such as KD-trees stop helping. It is why *dimensionality reduction* and approximate nearest-neighbour search matter. See: [00_AI_Fundamentals/advanced_algorithms/08_advanced_data_structures.ipynb](00_AI_Fundamentals/advanced_algorithms/08_advanced_data_structures.ipynb)

## D

**d-Separation** — A graphical rule for reading a *Bayesian network*: if every path between two variables is blocked by the evidence, they are conditionally independent. It tells you which observations matter for a query. See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

**Data Augmentation** — Creating extra training examples by making small, realistic changes to existing ones, such as flipping, rotating or cropping images. This helps the model generalize instead of memorizing. See: [06_Computer_Vision/02_image_classification.ipynb](06_Computer_Vision/02_image_classification.ipynb)

**Data Contract** — A written, testable agreement between whoever produces a dataset and whoever uses it: column names, types, allowed ranges, freshness and who owns it. Checks run automatically in CI so breaking changes are caught before they reach a model. See: [15_MLOps/14_data_contracts.ipynb](15_MLOps/14_data_contracts.ipynb)

**Data Drift** — When the inputs a model sees in production gradually become different from the data it was trained on (for example, customers get younger, or prices rise with inflation). Monitoring catches drift so you know when to retrain. (When the link between inputs and the right answer changes instead, it is called concept drift.) See: [15_MLOps/06_monitoring/01_monitoring.ipynb](15_MLOps/06_monitoring/01_monitoring.ipynb)

**Data Leakage** — When information that would not be available at prediction time sneaks into training, making test scores look great but real-world results poor. *Example:* scaling data using statistics from the whole dataset, including the test set. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**Data Skew / Salting** — Skew is when a few keys hold most of the data, so one worker does most of the work while others sit idle. Salting splits a hot key into several sub-keys (adding a random suffix) so the load spreads out, then combines the partial results. See: [13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb](13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb)

**Data Versioning (DVC)** — Tracking versions of datasets and models the way *Git* tracks code, so any experiment can be rerun on the exact same data. Tools such as DVC store large files elsewhere and keep small pointer files in Git. See: [15_MLOps/02_data_versioning/01_dvc.ipynb](15_MLOps/02_data_versioning/01_dvc.ipynb)

**Data Warehouse** — A central database built for analysis rather than day-to-day transactions: it collects cleaned, historical data from many systems, usually in a *star schema*. *Examples:* Snowflake, BigQuery, Redshift. See also *OLAP vs OLTP*. See: [13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb](13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb)

**DataFrame** — A table of data in Python (rows and named columns), like a spreadsheet you can program. It is the main object in the *pandas* library. See: [02_Data_Analysis/03_pandas.ipynb](02_Data_Analysis/03_pandas.ipynb)

**Deadlock** — When two or more tasks each hold a resource and wait forever for one the other holds. *Example:* thread 1 locks A then waits for B, while thread 2 locks B then waits for A. Avoided by always taking locks in the same order or using timeouts. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**Decision Tree** — A model that makes predictions by asking a series of yes/no questions about the features, like a flowchart: "Is income > 50k? → Is age < 30? → Approve". Easy to explain, but a single deep tree overfits easily. See: [03_Machine_Learning/01_supervised/03_decision_trees.ipynb](03_Machine_Learning/01_supervised/03_decision_trees.ipynb)

**Deep Learning** — *Machine learning* with neural networks that have many layers ("deep"). Each layer learns more abstract features than the one before. It powers modern image recognition, speech and LLMs. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**Delivery Semantics (At-Most / At-Least / Exactly-Once)** — The guarantee a messaging or streaming system gives: messages may be lost (at-most-once), may be repeated (at-least-once), or are processed exactly once in effect. Exactly-once is usually built from at-least-once delivery plus *idempotent* writes and checkpoints. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Denormalization** — Deliberately storing duplicate data (undoing some *normalization*) to make reads faster, at the cost of more storage and harder updates. *Example:* storing the customer's name on every order row so a dashboard needs no join. See: [13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb](13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb)

**Dependency Injection** — Passing the things an object needs (a database client, an LLM client) in from outside instead of creating them inside. Code becomes easier to test, because a test can inject a fake. *Example:* `Summarizer(llm=FakeLLM())` in tests and `Summarizer(llm=RealLLM())` in production. See: [23_Software_Engineering/02_design_patterns_for_ai_code.ipynb](23_Software_Engineering/02_design_patterns_for_ai_code.ipynb)

**Deployment** — Putting a trained model somewhere real users or systems can use it, for example behind a web *API*, inside a mobile app, or as a nightly batch job. See: [16_Deployment/01_deployment_concepts.ipynb](16_Deployment/01_deployment_concepts.ipynb)

**Derivative / Gradient** — A derivative tells you how fast a function's output changes when you change its input a tiny bit (its slope). A gradient is the same idea for many inputs at once: a list of slopes, one per input, pointing in the direction of steepest increase. See: [14_Mathematics/02_calculus.ipynb](14_Mathematics/02_calculus.ipynb)

**Design of Experiments (DOE)** — Planning experiments so they give clear answers with few runs, using randomization (removes bias), replication (measures noise) and blocking (compares like with like). Includes *factorial designs* and response-surface methods. See: [02_Data_Analysis/14_design_of_experiments.ipynb](02_Data_Analysis/14_design_of_experiments.ipynb)

**Design Pattern** — A named, reusable solution to a common software design problem. *Examples:* Factory (create objects without naming their class), Strategy (swap algorithms), Observer (notify subscribers, like training callbacks), Adapter (wrap a different API in the interface you expect). See: [23_Software_Engineering/02_design_patterns_for_ai_code.ipynb](23_Software_Engineering/02_design_patterns_for_ai_code.ipynb)

**Differential Privacy** — A mathematical privacy guarantee: add carefully measured random noise to results so that whether any single person's data is included barely changes the output. A setting called epsilon controls the privacy-versus-accuracy tradeoff. See: [19_AI_Ethics_and_Safety/03_privacy.ipynb](19_AI_Ethics_and_Safety/03_privacy.ipynb)

**Diffusion Model** — A generative model that learns to remove noise step by step. To create an image, it starts from pure random noise and gradually "denoises" it into a picture that matches the prompt. See: [06_Computer_Vision/06_image_generation.ipynb](06_Computer_Vision/06_image_generation.ipynb)

**Dijkstra's Algorithm** — Finds the shortest paths from one starting node to all others in a graph with non-negative edge weights, by always settling the closest unsettled node next using a *priority queue*. Runs in O((V + E) log V). Negative weights need Bellman-Ford instead. See: [00_AI_Fundamentals/dsa/07_graphs.ipynb](00_AI_Fundamentals/dsa/07_graphs.ipynb)

**Dimensionality Reduction** — Shrinking data with many columns into fewer columns while keeping most of the useful information, for speed or for plotting in 2D. *PCA*, t-SNE and UMAP are common methods. See: [03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb](03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb)

**Divide and Conquer** — Split a problem into independent smaller pieces, solve each recursively, and combine the answers. *Examples:* merge sort, binary search, the *FFT*. The *Master theorem* gives its running time. See: [00_AI_Fundamentals/dsa/08_greedy_and_divide_and_conquer.ipynb](00_AI_Fundamentals/dsa/08_greedy_and_divide_and_conquer.ipynb)

**DNS (Domain Name System)** — The internet's phone book: it turns a name such as `api.example.com` into an IP address computers can connect to. Answers are cached for a set time (TTL), which is why DNS changes can take a while to spread. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Docker** — The most popular tool for building and running *containers*. You describe your app's environment in a `Dockerfile`, build it into an image (a ready-to-run template), and run that image anywhere Docker is installed. See: [17_Docker/01_docker_basics.ipynb](17_Docker/01_docker_basics.ipynb)

**Dot Product** — Multiply two lists of numbers position by position and add up the results: [1,2]·[3,4] = 1×3 + 2×4 = 11. It measures how much two vectors point the same way and is everywhere in ML, from linear models to *attention*. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**Double Descent** — The observation that as model size grows, test error first falls, then rises near the point where the model can exactly fit the training data, then falls again for much larger models. It explains why huge, over-parameterized networks can still generalize. See: [03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb](03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb)

**DPO (Direct Preference Optimization)** — A way to *align* an LLM using pairs of answers where humans marked one as better. It trains the model directly to prefer the better answer, without the separate reward model and reinforcement-learning loop that *RLHF* uses. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**DQN (Deep Q-Network)** — *Q-learning* with a neural network instead of a table, so it can handle large inputs such as game screens. Two tricks make it stable: an experience replay buffer (train on random past transitions) and a slowly updated target network. See: [11_Reinforcement_Learning/04_deep_q_networks.ipynb](11_Reinforcement_Learning/04_deep_q_networks.ipynb)

**Dropout** — A training trick where a random fraction of neurons is temporarily switched off at each step, so the network can't rely too heavily on any single neuron. It reduces *overfitting* and is turned off at prediction time. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

**Duality (Lagrangian Duality)** — Every constrained optimization problem (the primal) has a partner problem (the dual) built from the *Lagrangian*, whose optimum gives a bound on the primal one. For *convex* problems the two usually match, and the dual can be easier to solve; the SVM is the classic example. See: [14_Mathematics/12_convex_optimization_and_duality.ipynb](14_Mathematics/12_convex_optimization_and_duality.ipynb)

**Dynamic Programming (DP)** — Solving a problem by breaking it into overlapping subproblems, solving each once, and storing the answers for reuse (in a table or with *memoization*). *Examples:* edit distance, knapsack, shortest paths, the *Viterbi algorithm*. See: [00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb](00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb)

## E

**Early Stopping** — Stopping training when the score on validation data stops improving, even if training could continue. This prevents the model from starting to *overfit*. See: [05_Deep_Learning/16_industry_pytorch_training_pipeline.ipynb](05_Deep_Learning/16_industry_pytorch_training_pipeline.ipynb)

**EDA (Exploratory Data Analysis)** — The first look at a dataset: summary numbers, missing values, distributions, outliers and relationships, mostly through tables and charts, before any modeling. See: [02_Data_Analysis/07_eda.ipynb](02_Data_Analysis/07_eda.ipynb)

**Edit Distance (Levenshtein Distance)** — The fewest single-character insertions, deletions and substitutions needed to turn one string into another. *Example:* "kitten" → "sitting" has distance 3. Computed with *dynamic programming* and used in spell-checkers and fuzzy matching. See: [00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb](00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb)

**Effect Size** — How *big* a difference is, as opposed to whether it is statistically detectable. *Examples:* Cohen's d (mean difference in standard-deviation units) or simply "+2.1 accuracy points". With enough data even a tiny, useless effect gets a small *p-value*, so always report the effect size. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**ELBO (Evidence Lower Bound)** — A quantity that is always less than or equal to the log-probability of the data and is much easier to compute. Maximizing it is how *EM*, *variational inference* and *VAEs* train models with hidden variables. See: [03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb)

**EM Algorithm (Expectation-Maximization)** — A way to fit models with hidden variables by alternating two steps: E-step, guess the hidden values (as probabilities) using the current parameters; M-step, update the parameters as if those guesses were true. *Example:* fitting a *Gaussian mixture model* when you do not know which cluster each point came from. See: [03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb)

**Embedding** — A list of numbers (a vector) that represents the meaning of something such as a word, sentence, image or product, so that similar things get similar vectors. *Example:* "puppy" and "dog" end up close together; "puppy" and "invoice" far apart. See: [07_NLP/02_word_embeddings.ipynb](07_NLP/02_word_embeddings.ipynb)

**Encoder / Decoder** — Two halves of many neural networks. The encoder reads the input and turns it into an internal representation; the decoder turns that representation into an output. *BERT* is encoder-only, most chat LLMs are decoder-only, and translation models often use both. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

**Endpoint** — One specific URL path of a web *API* that does one job, for example `POST /predict` or `GET /health`. See: [12_FastAPI/notes/12_FastAPI.md](12_FastAPI/notes/12_FastAPI.md)

**Ensemble** — Combining several models so their mistakes cancel out, for example by voting or averaging. Bagging (averaging many models trained on random samples), *boosting* and stacking are the main styles. *Analogy:* asking several doctors for an opinion instead of just one. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**Entropy** — A measure of uncertainty or surprise. A fair coin flip has high entropy (you can't guess it); a coin that always lands heads has zero entropy. It is used in decision trees and in *cross-entropy loss*. See: [14_Mathematics/05_information_theory.ipynb](14_Mathematics/05_information_theory.ipynb)

**Epoch** — One full pass through the entire training dataset. Training usually runs for many epochs. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**ER Model (Entity-Relationship Model)** — A diagram-based way to design a database before writing SQL: entities (Student, Course), their attributes (name, credits) and the relationships between them (Student *enrolls in* Course, many-to-many). It is then mapped to tables. See: [13_Databases/00_dbms_fundamentals/02_er_model_and_eer.ipynb](13_Databases/00_dbms_fundamentals/02_er_model_and_eer.ipynb)

**Event Loop** — The scheduler inside *asyncio* that runs coroutines and resumes each one when the thing it awaited (a network reply, a timer) is ready. One blocking call inside it freezes every task. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**Event Time vs Processing Time** — Event time is when something actually happened (the click); processing time is when your system sees it. Late or out-of-order events make the two differ, so correct streaming results group by event time and use *watermarks*. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Experiment Tracking** — Automatically recording every training run's settings, code version, data version and results so you can compare runs and reproduce the best one. MLflow and Weights & Biases are common tools. See: [15_MLOps/01_experiment_tracking/01_mlflow.ipynb](15_MLOps/01_experiment_tracking/01_mlflow.ipynb)

**Expert System** — An early AI program that encodes a specialist's knowledge as if-then rules plus an inference engine that chains them to reach conclusions and explain them. *Example:* MYCIN, which recommended antibiotics in the 1970s. See: [00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb](00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb)

**Explainability (XAI)** — Methods that help people understand *why* a model made a prediction, such as which features mattered most. Tools include *SHAP*, LIME and feature importance. See: [03_Machine_Learning/07_explainability/01_explainability.ipynb](03_Machine_Learning/07_explainability/01_explainability.ipynb)

**Exploration vs Exploitation** — The basic trade-off in learning by trial: exploit what you already know works, or explore other options that might be better. Simple strategies include ε-greedy (try a random action ε of the time), UCB and Thompson sampling. See: [11_Reinforcement_Learning/01_rl_fundamentals.ipynb](11_Reinforcement_Learning/01_rl_fundamentals.ipynb)

**Exponential Backoff (with Jitter)** — Retrying a failed request after waiting longer each time (1 s, 2 s, 4 s, ...) plus a random amount (jitter), so many clients do not all retry at the same moment and overload the server again. Standard for rate-limited LLM APIs. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**External Merge Sort** — Sorting data too big for memory: sort chunks that fit in RAM, write them to disk as sorted runs, then merge the runs in a single streaming pass. Databases and big-data tools do this when a sort "spills" to disk. See: [00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/10_parallel_and_external_memory_algorithms.ipynb)

## F

**F1 Score** — A single score that balances *precision* and *recall* (it is their harmonic mean). It is useful when classes are imbalanced and accuracy would mislead. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**Factorial Design** — An experiment that tests every combination of several factors (for example 2 learning rates × 2 batch sizes × 2 optimizers = 8 runs) so you can see each factor's effect and how factors interact. Fractional factorials run only a planned subset. See: [02_Data_Analysis/14_design_of_experiments.ipynb](02_Data_Analysis/14_design_of_experiments.ipynb)

**Fairness Metrics (e.g. Demographic Parity)** — Numbers that check whether a model treats groups equally. Demographic parity, for example, asks whether different groups get positive outcomes (such as loan approvals) at similar rates. Different fairness definitions can conflict with each other. See: [19_AI_Ethics_and_Safety/01_bias_fairness.ipynb](19_AI_Ethics_and_Safety/01_bias_fairness.ipynb)

**False Positive / False Negative** — The two kinds of mistakes a yes/no classifier makes. A false positive is a false alarm (flagging a good email as spam); a false negative is a miss (letting spam through). See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**FastAPI** — A popular Python framework for building web *APIs* quickly. It uses Python type hints (labels like `age: int`) and *Pydantic* to check inputs automatically and creates interactive documentation for you. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

**Feature** — One input column a model uses to make a prediction. *Example:* for predicting a house price, features might be size, number of bedrooms and neighborhood. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Feature Engineering** — Creating better input columns from raw data so patterns are easier for a model to learn. *Example:* turning a timestamp into "hour of day" and "is weekend". See: [03_Machine_Learning/05_feature_engineering/01_feature_engineering.ipynb](03_Machine_Learning/05_feature_engineering/01_feature_engineering.ipynb)

**Feature Flag** — A configuration switch that turns a feature on or off (for everyone or for a share of users) without redeploying code. Used for gradual (canary) rollouts and as an instant kill switch if a new model misbehaves. See: [23_Software_Engineering/11_industry_building_and_shipping_an_ai_feature.ipynb](23_Software_Engineering/11_industry_building_and_shipping_an_ai_feature.ipynb)

**Feature Store** — A central system that computes, stores and serves ML *features* so training and live prediction use exactly the same definitions. It provides point-in-time-correct training data and low-latency lookups. *Examples:* Feast, Tecton. See: [15_MLOps/12_feature_stores.ipynb](15_MLOps/12_feature_stores.ipynb)

**Federated Learning** — Training a shared model across many devices or organisations without collecting their raw data: each client trains locally and sends only model updates, which a server averages (FedAvg). *Example:* phone keyboards learning next-word prediction while typing stays on the phone. See: [15_MLOps/09_federated_learning/01_federated_learning.ipynb](15_MLOps/09_federated_learning/01_federated_learning.ipynb)

**Few-Shot Prompting** — Putting a few worked examples in the prompt so the LLM can copy the pattern. *Example:* show three reviews with their sentiment labels, then give a fourth review to label. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

**FFT (Fast Fourier Transform)** — An O(n log n) algorithm for converting a signal into its frequency components (the Discrete Fourier Transform), instead of the naive O(n²). It makes long convolutions, polynomial multiplication and audio spectrograms fast. See: [00_AI_Fundamentals/advanced_algorithms/07_computational_geometry_and_fft.ipynb](00_AI_Fundamentals/advanced_algorithms/07_computational_geometry_and_fft.ipynb)

**Fine-Tuning** — Taking a model that has already been trained on lots of general data and training it a little more on your own, smaller dataset so it gets better at your specific task or style. See: [08_LLM/03_fine_tuning/01_fine_tuning.ipynb](08_LLM/03_fine_tuning/01_fine_tuning.ipynb)

**First-Order Logic (FOL)** — A formal logic that talks about objects, their properties and relations, with "for all" (∀) and "there exists" (∃). *Example:* ∀x Human(x) → Mortal(x). More expressive than *propositional logic*. See: [00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb](00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb)

**Floating Point (IEEE 754)** — How computers store real numbers: a sign, an exponent and a fraction, with limited precision. That is why `0.1 + 0.2 != 0.3` in Python, and why formats such as float16 and bfloat16 trade precision for speed and memory in deep learning. See: [23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb](23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb)

**Forecasting** — Predicting future values of something measured over time, such as next week's sales or tomorrow's electricity demand. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Forward / Backward Chaining** — Two ways to reason with if-then rules. Forward chaining starts from known facts and fires rules until nothing new appears (data-driven); backward chaining starts from a goal and works back to find facts that prove it (goal-driven). See: [00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb](00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb)

**Function Calling / Tool Calling** — An LLM feature where, instead of answering in plain text, the model outputs a structured request to run a specific function (for example `get_weather(city="Paris")`). Your code runs the function and passes the result back. This is how *agents* use tools. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

**Functional Dependency (FD)** — A rule X → Y meaning rows with the same X value must have the same Y value. *Example:* student_id → student_name. FDs decide what a table's keys are and how to split it during *normalization*. See: [13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb](13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb)

**Fuzzy Set / Fuzzy Logic** — Sets where membership is a degree between 0 and 1 rather than yes or no. *Example:* 28 °C might be "hot" to degree 0.7. Fuzzy logic combines such degrees with if-then rules and is used in simple controllers such as washing machines and thermostats. See: [00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb](00_AI_Fundamentals/classical_ai/10_fuzzy_logic_and_expert_systems.ipynb)

## G

**GAN (Generative Adversarial Network)** — Two networks trained against each other: a generator makes fake samples and a discriminator tries to tell fake from real. As they compete, the generator's fakes become more realistic. *Analogy:* a forger and a detective improving together. See: [05_Deep_Learning/06_generative_models.ipynb](05_Deep_Learning/06_generative_models.ipynb)

**Gaussian Mixture Model (GMM)** — A model that explains data as a blend of several bell-shaped (Gaussian) clusters, each with its own centre, spread and weight. Unlike *K-means* it gives soft, probabilistic cluster memberships. Fitted with the *EM algorithm*. See: [03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb)

**Gaussian Process (GP)** — A Bayesian model that places a probability distribution over whole functions, defined by a *kernel* that says how similar nearby inputs are. It predicts a value *and* an uncertainty band at every point, which makes it the usual surrogate in *Bayesian optimization*. See: [14_Mathematics/07_bayesian_ml.ipynb](14_Mathematics/07_bayesian_ml.ipynb)

**Generalization** — How well a model performs on new data it hasn't seen during training. Good generalization, not a high training score, is the real goal. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Generative AI** — AI that creates new content (text, images, audio, code) rather than only classifying or predicting a number. LLMs and *diffusion models* are the best-known examples. See: [08_LLM/11_multimodal/01_multimodal_ai.ipynb](08_LLM/11_multimodal/01_multimodal_ai.ipynb)

**Genetic Algorithm** — An optimisation method inspired by evolution: keep a population of candidate solutions, select the fittest, combine pairs (crossover), make small random changes (mutation), and repeat over generations. See: [00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb](00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb)

**GIL (Global Interpreter Lock)** — A lock in standard CPython that lets only one thread run Python bytecode at a time. Threads still help when waiting on I/O (network, disk), but CPU-heavy Python code needs multiprocessing, NumPy (which releases the GIL) or the newer free-threaded build. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**Git** — A version-control tool that records every change to your code as commits (saved snapshots), lets you work on separate branches (parallel lines of work), and lets teams merge their work safely. See: [20_Git_and_DevOps/01_git_basics.ipynb](20_Git_and_DevOps/01_git_basics.ipynb)

**GitHub Actions** — GitHub's built-in automation service. It runs scripts (tests, linting, building, deploying) automatically when something happens in a repository, such as a push or a pull request. It is a common way to do *CI/CD*. See: [20_Git_and_DevOps/03_github_actions_cicd.ipynb](20_Git_and_DevOps/03_github_actions_cicd.ipynb)

**GNN (Graph Neural Network)** — A neural network that works directly on graphs: each node repeatedly collects ("message passing") and combines information from its neighbours to build its representation. Used for molecules, social networks, recommendations and fraud rings. *Examples:* GCN, GraphSAGE, GAT. See: [05_Deep_Learning/07_gnn.ipynb](05_Deep_Learning/07_gnn.ipynb)

**GPU (Graphics Processing Unit)** — A chip with thousands of small cores that do many simple calculations in parallel. It makes training and running neural networks much faster than a normal CPU. You do not need one to start: the beginner and core notebooks in this repo are designed to run on a normal CPU. See: [05_Deep_Learning/11_distributed_training.ipynb](05_Deep_Learning/11_distributed_training.ipynb)

**Gradient Clipping** — Capping the size (norm) of the gradient before each update so one huge gradient cannot blow up training. Standard for *RNNs* and transformers. See: [05_Deep_Learning/19_sequence_models_hands_on.ipynb](05_Deep_Learning/19_sequence_models_hands_on.ipynb)

**Gradient Descent** — The basic way models learn: compute the *gradient* (which direction makes the error bigger), take a small step the opposite way, and repeat. *Analogy:* walking downhill in fog by always stepping where the ground slopes down. See: [14_Mathematics/06_optimization.ipynb](14_Mathematics/06_optimization.ipynb)

**Greedy Algorithm** — An algorithm that makes the choice that looks best right now and never reconsiders. It is optimal for some problems (making change with standard coins, minimum spanning trees, Huffman coding) and only an approximation for others. See: [00_AI_Fundamentals/dsa/08_greedy_and_divide_and_conquer.ipynb](00_AI_Fundamentals/dsa/08_greedy_and_divide_and_conquer.ipynb)

**Grid Search / Random Search** — Two simple ways to tune *hyperparameters*. Grid search tries every combination from a list; random search tries random combinations, which often finds good settings faster. See: [03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb](03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb)

**gRPC** — A fast framework for calls between services that sends compact binary messages (Protocol Buffers) over HTTP/2 and supports streaming. Common between internal microservices and model servers; *REST* with JSON is easier for public APIs. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**GRU (Gated Recurrent Unit)** — A simpler cousin of the *LSTM* with two gates (update and reset) instead of three. It handles long-range dependencies almost as well with fewer parameters. See: [05_Deep_Learning/19_sequence_models_hands_on.ipynb](05_Deep_Learning/19_sequence_models_hands_on.ipynb)

**Guardrails** — Checks placed around an AI system to keep it safe and on-topic: filtering harmful inputs and outputs, blocking leaks of private data, validating formats, or refusing out-of-scope requests. See: [08_LLM/20_industry_llm_application_patterns.ipynb](08_LLM/20_industry_llm_application_patterns.ipynb)

## H

**Hallucination** — When an LLM states something false or made-up as if it were fact, such as an invented citation. *RAG*, careful prompting and evaluation help reduce it. See: [08_LLM/08_evaluation/notes/08_evaluation.md](08_LLM/08_evaluation/notes/08_evaluation.md)

**Halting Problem** — The proven fact that no program can decide, for every program and input, whether that program will eventually stop or run forever. It is the classic *undecidable* problem and sets hard limits on what automatic code analysis can do. See: [14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb](14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb)

**Hash Table** — A data structure that stores key-value pairs in an array, using a hash function to turn each key into a slot number, so lookups, inserts and deletes take O(1) time on average. Python's `dict` and `set` are hash tables. Two keys landing in one slot is a collision. See: [00_AI_Fundamentals/dsa/04_hashing.ipynb](00_AI_Fundamentals/dsa/04_hashing.ipynb)

**Heap / Priority Queue** — A heap is a tree stored in an array where every parent is smaller (min-heap) or larger (max-heap) than its children, so the smallest item is always on top. It implements a priority queue: O(log n) insert and remove-min. Used in *Dijkstra's algorithm*, schedulers and top-k queries (Python's `heapq`). See: [00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb](00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb)

**Heuristic (Search)** — A quick estimate of how far a state is from the goal, used to guide search toward promising options. *Example:* in the 8-puzzle, the number of misplaced tiles. See: [00_AI_Fundamentals/classical_ai/03_informed_search.ipynb](00_AI_Fundamentals/classical_ai/03_informed_search.ipynb)

**Hidden Markov Model (HMM)** — A model of a sequence where an unseen state changes over time according to a Markov chain and each state produces an observation. *Example:* inferring weather (hidden) from whether someone carries an umbrella (observed). The *Viterbi algorithm* finds the most likely hidden sequence. See: [00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb](00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb)

**Hill Climbing** — A local search that keeps moving to a better neighbouring solution until none is better. Fast and simple, but it can get stuck on a local peak; random restarts or *simulated annealing* help. See: [00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb](00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb)

**HTTP / HTTPS** — The request-response protocol of the web. A client sends a method (GET, POST, PUT, DELETE), a path, headers and an optional body; the server replies with a status code (200 OK, 404 Not Found, 429 Too Many Requests, 500 Server Error), headers and a body. HTTPS is HTTP inside *TLS* encryption. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Hugging Face** — A company and platform that hosts thousands of open models and datasets and maintains libraries such as `transformers`, `datasets` and `sentence-transformers`. Many notebooks here load small models from it. See: [08_LLM/05_slms/01_small_language_models.ipynb](08_LLM/05_slms/01_small_language_models.ipynb)

**Hyperband / Successive Halving** — Hyperparameter search that starts many configurations on a small budget (few epochs), keeps only the best fraction, gives survivors more budget, and repeats. Bad settings are dropped early, saving most of the compute. See: [15_MLOps/08_automl/02_automl_from_scratch.ipynb](15_MLOps/08_automl/02_automl_from_scratch.ipynb)

**HyperLogLog** — A sketch that estimates how many *distinct* items a huge stream contains using only a few kilobytes, with about 1–2% error. It looks at the longest run of leading zeros in hashed values. *Example:* counting unique daily users across billions of events. See: [00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb)

**Hyperparameter** — A setting you choose *before* training rather than one the model learns, such as the *learning rate*, the number of trees, or the depth of a tree. Tuning them well can matter a lot. See: [03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb](03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb)

**Hypothesis Test** — A statistical procedure for deciding whether an observed effect is likely real or could just be random luck. You assume "no effect" (the null hypothesis) and check how surprising the data would be under that assumption (the *p-value*). See: [02_Data_Analysis/08_statistics.ipynb](02_Data_Analysis/08_statistics.ipynb)

## I

**Idempotent Operation** — An operation that gives the same result whether you run it once or many times. *Example:* "set balance to 100" is idempotent; "add 10" is not. Retries and *at-least-once* pipelines are only safe when writes are idempotent (for example upserts keyed by ID). See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Imputation** — Filling in missing values in data, for example with the column's average or median, or with a model's best guess. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Incremental Load / Upsert** — Loading only new or changed records since the last run (tracked with a high-water mark such as the latest timestamp) and writing them with an upsert: update if the key exists, insert if not. Re-running the job then creates no duplicates. See: [02_Data_Analysis/12_data_acquisition_apis_scraping_and_formats.ipynb](02_Data_Analysis/12_data_acquisition_apis_scraping_and_formats.ipynb)

**Index (Database Index)** — An extra data structure (usually a *B+ tree*, sometimes a hash table) that lets the database find rows by a column's value without scanning the whole table. *Analogy:* the index at the back of a book. It speeds up reads but slows writes and uses space. See: [13_Databases/00_dbms_fundamentals/07_indexing_b_trees_and_hashing.ipynb](13_Databases/00_dbms_fundamentals/07_indexing_b_trees_and_hashing.ipynb)

**Inference** — Using a trained model to make predictions on new data, as opposed to training it. Most of a deployed model's cost and *latency* comes from inference. See: [08_LLM/13_inference_optimization.ipynb](08_LLM/13_inference_optimization.ipynb)

**Instruction Tuning / SFT (Supervised Fine-Tuning)** — *Fine-tuning* a pretrained language model on many examples of instructions paired with good responses, so it learns to follow requests and chat instead of just continuing text. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**Integer Programming (MILP)** — *Linear programming* where some variables must be whole numbers (for example yes/no decisions such as "open this warehouse"). Much harder in general (*NP-hard*), and solved with *branch and bound*. Used for scheduling, routing and facility location. See: [00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb](00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb)

**Isolation Level** — How strictly a database separates concurrent transactions. From weakest to strongest: read uncommitted, read committed, repeatable read, *serializable*. Weaker levels are faster but allow anomalies such as reading data that later changes. See: [13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb](13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb)

## J

**Jacobian / Hessian** — The Jacobian is the matrix of all first derivatives of a vector-valued function (how each output changes with each input). The Hessian is the matrix of second derivatives of a scalar function, describing curvature. Backpropagation multiplies by Jacobians without ever building them in full. See: [14_Mathematics/11_matrix_calculus_and_autodiff_from_scratch.ipynb](14_Mathematics/11_matrix_calculus_and_autodiff_from_scratch.ipynb)

**Jailbreak** — A prompt crafted to trick an LLM into ignoring its safety rules, for example by role-play ("pretend you are an AI with no rules"). Defenses include *guardrails* and *red teaming*. See: [09_Prompt_Engineering/notes/09_Prompt_Engineering.md](09_Prompt_Engineering/notes/09_Prompt_Engineering.md)

**Join Algorithms (Nested-Loop / Hash / Sort-Merge)** — The ways a database combines two tables. Nested loop compares every pair (fine for tiny inputs or with an index); hash join builds a hash table on the smaller table and probes it; sort-merge sorts both on the key and walks them together. The *query optimizer* picks one. See: [13_Databases/00_dbms_fundamentals/08_query_processing_and_optimization.ipynb](13_Databases/00_dbms_fundamentals/08_query_processing_and_optimization.ipynb)

**JSON** — A simple, human-readable text format for structured data, built from `{"key": "value"}` pairs and `[lists]`. It is the usual format for web *APIs* and for *structured outputs* from LLMs. See: [08_LLM/17_structured_outputs.ipynb](08_LLM/17_structured_outputs.ipynb)

**Jupyter Notebook** — An interactive document (`.ipynb`) that mixes runnable code cells, their outputs (tables, charts) and explanatory text. Every lesson in this repo is a Jupyter notebook. The program that runs the code behind it is called the kernel; "Restart kernel" clears its memory. See: [README.md](README.md)

**JWT (JSON Web Token)** — A compact signed token (`header.payload.signature`) that a server gives a client after login; the client sends it with each request to prove who it is. Anyone can read the payload, so never put secrets in it, and always verify the signature and expiry. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

## K

**K-Means** — A *clustering* algorithm: choose k, place k center points, assign each point to its nearest center, move each center to the middle of its points, and repeat until nothing changes. See: [03_Machine_Learning/02_unsupervised/01_clustering.ipynb](03_Machine_Learning/02_unsupervised/01_clustering.ipynb)

**Kafka (Apache Kafka)** — A distributed event log: producers append messages to topics, which are split into ordered partitions, and consumers read them at their own pace and remember their position (offset). It is the usual backbone for streaming pipelines and real-time features. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**KD-Tree** — A tree that splits space along one coordinate at a time to speed up nearest-neighbour and range searches in low dimensions. It loses its advantage in high dimensions (*curse of dimensionality*), where approximate methods such as HNSW are used. See: [00_AI_Fundamentals/advanced_algorithms/08_advanced_data_structures.ipynb](00_AI_Fundamentals/advanced_algorithms/08_advanced_data_structures.ipynb)

**Kernel Trick** — Computing similarities as if data had been mapped into a much higher-dimensional feature space, without ever building those features, by using a kernel function k(x, z). It lets linear methods such as SVMs and ridge regression learn curved boundaries. *Example:* the RBF (Gaussian) kernel. See: [03_Machine_Learning/16_learning_theory/02_kernel_methods.ipynb](03_Machine_Learning/16_learning_theory/02_kernel_methods.ipynb)

**KKT Conditions (Karush-Kuhn-Tucker)** — The equations and inequalities that the solution of a constrained optimization problem must satisfy: the gradient balance with the *Lagrange multipliers*, feasibility, and "complementary slackness" (a constraint's multiplier is zero unless the constraint is tight). For *convex* problems they are also sufficient. See: [14_Mathematics/12_convex_optimization_and_duality.ipynb](14_Mathematics/12_convex_optimization_and_duality.ipynb)

**KNN (K-Nearest Neighbors)** — A simple model that predicts by looking at the k most similar training examples and taking a vote (classification) or an average (regression). *Analogy:* guessing a house price from the prices of the five most similar houses nearby. See: [03_Machine_Learning/01_supervised/07_knn.ipynb](03_Machine_Learning/01_supervised/07_knn.ipynb)

**Knowledge Distillation** — Training a small "student" model to imitate a large "teacher" model's outputs, so you get most of the quality at a fraction of the size and cost. See: [05_Deep_Learning/08_model_compression.ipynb](05_Deep_Learning/08_model_compression.ipynb)

**Knowledge Graph** — Information stored as a network of facts in the form (thing) → relationship → (thing), such as (Paris) → capital_of → (France). LLM systems can query it to get precise, linked facts. See: [08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb](08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb)

**Kubernetes (K8s)** — A system that runs and manages many *containers* across many machines: it starts them, restarts them if they crash, scales them up and down with traffic, and routes requests to them. See: [17_Docker/kubernetes/01_kubernetes.ipynb](17_Docker/kubernetes/01_kubernetes.ipynb)

**KV Cache (Key-Value Cache)** — A speed-up for LLM text generation. The model saves the *attention* "keys" and "values" it already computed for earlier tokens, so each new token only needs a small amount of new computation. It uses extra memory that grows with the length of the text. See: [08_LLM/13_inference_optimization.ipynb](08_LLM/13_inference_optimization.ipynb)

## L

**Label / Target** — The correct answer you want a model to predict, for example "spam" or the house price. In *supervised learning*, every training example comes with its label. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Lagrange Multipliers / Lagrangian** — A way to handle constraints in optimization: add each constraint to the objective multiplied by a new variable (its multiplier), forming the Lagrangian. A multiplier tells you how much the optimum would improve if that constraint were relaxed slightly (a "shadow price"). See: [14_Mathematics/12_convex_optimization_and_duality.ipynb](14_Mathematics/12_convex_optimization_and_duality.ipynb)

**LangChain / LangGraph** — Popular open-source Python libraries for building LLM applications. LangChain provides building blocks (prompts, retrievers, tool wrappers); LangGraph builds *agents* as graphs of steps with loops and saved state. See: [10_Agents/03_langgraph.ipynb](10_Agents/03_langgraph.ipynb)

**Latency / Throughput** — Latency is how long one request takes (for example 200 ms). Throughput is how many requests a system handles per second. Improving one can hurt the other (for example, batching raises throughput but can add latency). See: [15_MLOps/11_model_serving_advanced.ipynb](15_MLOps/11_model_serving_advanced.ipynb)

**Layer** — One stage of a neural network that transforms its input (for example a fully connected, convolutional or attention layer). Data flows through layers in order, from input to output. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Learning Rate** — How big a step the *optimizer* takes each time it updates the weights. Too big and training jumps around or blows up; too small and it crawls. Often the single most important *hyperparameter*. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Linear Programming (LP)** — Optimizing a linear objective subject to linear inequality constraints, for example maximizing profit given limits on materials and hours. The optimum lies at a corner of the feasible region; the simplex method and interior-point methods find it quickly even with thousands of variables. See: [00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb](00_AI_Fundamentals/advanced_algorithms/05_linear_and_integer_programming.ipynb)

**Linear Regression** — The simplest model for predicting a number: fit the best straight line (or flat plane) through the data, so that prediction = weight × feature + bias. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**List Comprehension (Python)** — A compact way to build a list in one line: `[x * 2 for x in numbers if x > 0]` means "double every positive number". See: [01_Python/01_basic.ipynb](01_Python/01_basic.ipynb)

**Literature Review / Systematic Review** — A literature review summarizes and connects what existing research knows about a question and where the gaps are. A systematic review follows a pre-written, reproducible search and selection protocol (for example PRISMA) so others could repeat it. See: [24_Research_Methods/01_research_methodology_and_literature_review.ipynb](24_Research_Methods/01_research_methodology_and_literature_review.ipynb)

**LLM (Large Language Model)** — A very large neural network (usually a *transformer*) trained on huge amounts of text to predict the next *token*. That simple skill, at scale, lets it answer questions, summarize, translate and write code. See: [08_LLM/notes/08_LLM.md](08_LLM/notes/08_LLM.md)

**LLM-as-a-Judge** — Using one LLM to grade another model's answers against a rubric (for correctness, helpfulness, tone). It is cheaper than human review but can be biased, so it should be checked against human judgments. See: [08_LLM/08_evaluation/notes/08_evaluation.md](08_LLM/08_evaluation/notes/08_evaluation.md)

**Load Balancer** — A component that spreads incoming requests across several servers (round robin, least connections, or by hashing) and stops sending traffic to unhealthy ones. It lets a service scale out and survive single-server failures. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Logistic Regression** — Despite the name, a *classification* model. It computes a weighted sum of the features and squashes it with the *sigmoid* function into a probability between 0 and 1. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**Logits** — The raw, unnormalized scores a model outputs before they are turned into probabilities (usually with *softmax*). Bigger logit = more likely. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**LoRA (Low-Rank Adaptation)** — A cheap way to *fine-tune* big models: keep the original weights frozen and train small add-on matrices instead. You train well under 1% of the parameters, and the add-on file is small. QLoRA does the same on top of a *quantized* model to save even more memory. See: [05_Deep_Learning/12_advanced_peft.ipynb](05_Deep_Learning/12_advanced_peft.ipynb)

**Loss Function** — A formula that measures how wrong a model's predictions are; training tries to make it as small as possible. *Examples:* mean squared error for numbers, *cross-entropy* for categories. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**LSH (Locality-Sensitive Hashing)** — Hashing designed so similar items land in the same bucket with high probability, which makes finding near-duplicates or nearest neighbours fast without comparing every pair. Used to deduplicate web-scale training data. See: [00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb)

**LSTM (Long Short-Term Memory)** — A type of *RNN* with gates that control what to remember, forget and output. This lets it keep information over long sequences much better than a plain RNN. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

**LU / QR / Cholesky Decomposition** — Ways to factor a matrix into simpler triangular or orthogonal pieces so linear systems and least-squares problems can be solved quickly and stably. LU is for general square systems, QR for least squares, Cholesky for symmetric positive-definite matrices (about twice as fast as LU). See: [14_Mathematics/10_numerical_linear_algebra.ipynb](14_Mathematics/10_numerical_linear_algebra.ipynb)

## M

**Machine Learning (ML)** — Teaching computers to find patterns from examples instead of writing every rule by hand. *Example:* instead of coding rules for spam, show the computer thousands of labeled emails and let it learn. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**MAE / MSE / RMSE** — Common error measures for predicting numbers. MAE (Mean Absolute Error) is the average size of the errors. MSE (Mean Squared Error) averages the squared errors, so it punishes big misses more. RMSE is the square root of MSE, which puts it back in the original units. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**MapReduce** — A programming model for processing huge datasets on many machines: *map* turns each record into key-value pairs, the system *shuffles* pairs so equal keys meet, and *reduce* combines each key's values. *Example:* word count. *Spark* generalized it and is much faster. See: [13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb](13_Databases/06_data_engineering/02_big_data_processing_on_one_machine.ipynb)

**Markov Decision Process (MDP)** — The formal setting of reinforcement learning: states, actions, transition probabilities, *rewards* and a discount factor γ. "Markov" means the next state depends only on the current state and action, not the whole history. See: [11_Reinforcement_Learning/01_rl_fundamentals.ipynb](11_Reinforcement_Learning/01_rl_fundamentals.ipynb)

**Markov Network (Markov Random Field)** — A probabilistic graphical model with undirected edges, where connected variables are tied by compatibility scores (potentials) rather than conditional probability tables. Natural for symmetric relations, such as neighbouring pixels in an image. See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

**Master Theorem** — A shortcut for solving divide-and-conquer recurrences of the form T(n) = a·T(n/b) + f(n). *Example:* merge sort, T(n) = 2T(n/2) + O(n), comes out as O(n log n). See: [00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb](00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb)

**Matrix** — A rectangular grid of numbers. A dataset is a matrix (rows = examples, columns = features), and neural-network layers are mostly matrix multiplications. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**Max-Flow / Min-Cut** — The maximum flow problem asks how much can be pushed from a source to a sink through a network of capacity-limited edges. The max-flow min-cut theorem says this equals the total capacity of the cheapest set of edges whose removal disconnects them. Used for matching, image segmentation and scheduling. See: [00_AI_Fundamentals/advanced_algorithms/04_network_flows_and_matching.ipynb](00_AI_Fundamentals/advanced_algorithms/04_network_flows_and_matching.ipynb)

**MCMC (Markov Chain Monte Carlo)** — A family of methods (such as Metropolis-Hastings and Gibbs sampling, which resamples one variable at a time) that draw samples from a complicated probability distribution by running a random walk whose long-run behaviour matches it. Used to compute Bayesian posteriors. Diagnostics such as trace plots and R-hat check that it has converged. See: [03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb)

**McNemar's Test** — A test of whether two classifiers differ in accuracy on the *same* test set. It looks only at the items where exactly one model is right; if those split far from 50/50, the difference is significant. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**MCP (Model Context Protocol)** — An open standard for connecting AI applications to external tools and data sources in a uniform way. A tool written once as an "MCP server" can be used by any app that supports MCP. *Analogy:* a USB port for AI tools. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

**Memoization** — Caching a function's results for inputs it has already seen, so repeated calls return instantly. It turns many slow recursive solutions into fast top-down *dynamic programming*. In Python: `@functools.lru_cache`. See: [00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb](00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb)

**Memory (Agent)** — How an *agent* keeps information beyond a single step. Short-term memory is the current conversation in the *context window*; long-term memory is usually stored outside the model (for example in a *vector database*) and retrieved when needed. See: [10_Agents/02_memory_and_planning.ipynb](10_Agents/02_memory_and_planning.ipynb)

**Memory Hierarchy** — The layers of storage from tiny-and-fast to large-and-slow: CPU registers, L1/L2/L3 caches, RAM, SSD, network. Code that reads memory in order (contiguous arrays) uses the caches well and can be many times faster than code that jumps around. See: [23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb](23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb)

**Merge Sort / Quicksort** — The two classic O(n log n) sorting algorithms. Merge sort splits the list in half, sorts each half and merges them (stable, always O(n log n)); quicksort partitions around a pivot (in-place and usually faster in practice, O(n²) worst case). See: [00_AI_Fundamentals/dsa/03_searching_and_sorting.ipynb](00_AI_Fundamentals/dsa/03_searching_and_sorting.ipynb)

**Message Queue** — A buffer service that lets one part of a system drop off work (messages) for another to process later, so the sender does not wait. It absorbs traffic spikes and decouples services. *Examples:* RabbitMQ, Amazon SQS, Redis queues, *Kafka*. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**MinHash** — A short signature of a set (for example the word shingles of a document) such that the share of matching signature entries estimates the Jaccard similarity of two sets. Combined with *LSH* to find near-duplicate documents at scale. See: [00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb)

**Minimax** — The game-search rule for two-player, zero-sum games: assume you pick the move that maximizes your score and the opponent picks the one that minimizes it, and look ahead through the game tree. Usually sped up with *alpha-beta pruning*. See: [00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb](00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb)

**Minimum Spanning Tree (MST)** — The cheapest set of edges that connects every node in a weighted graph without cycles. Found greedily by Kruskal's or Prim's algorithm. *Example:* laying the least cable needed to connect all buildings. See: [00_AI_Fundamentals/dsa/07_graphs.ipynb](00_AI_Fundamentals/dsa/07_graphs.ipynb)

**MLOps** — The practices and tools for taking ML models from a notebook to reliable production and keeping them healthy: versioning, automated pipelines, testing, deployment, monitoring and retraining. *Analogy:* DevOps, but for models and data too. See: [15_MLOps/notes/15_MLOps.md](15_MLOps/notes/15_MLOps.md)

**Mocking** — Replacing a real dependency (an LLM API, a database, the network) with a fake object in tests, which returns scripted answers and records how it was called. Tests become fast, free and deterministic. See: [23_Software_Engineering/03_testing_ai_code.ipynb](23_Software_Engineering/03_testing_ai_code.ipynb)

**Model Registry** — A central catalog of trained models with their versions, metrics and stage (for example "staging" or "production"), so teams know which model is live and can roll back. See: [15_MLOps/05_model_registry/01_model_registry.ipynb](15_MLOps/05_model_registry/01_model_registry.ipynb)

**Model Serving** — Running a trained model as a service that answers prediction requests, usually behind an *API*, with attention to speed, scaling and reliability. See: [12_FastAPI/03_ml_serving_with_fastapi.ipynb](12_FastAPI/03_ml_serving_with_fastapi.ipynb)

**Monitoring (ML)** — Continuously watching a deployed model's inputs, outputs, performance, latency and errors, with alerts when something drifts or breaks. See: [15_MLOps/06_monitoring/01_monitoring.ipynb](15_MLOps/06_monitoring/01_monitoring.ipynb)

**Monte Carlo Tree Search (MCTS)** — A game-search method that grows a tree by repeatedly selecting promising moves, playing random games to the end, and backing up the results. It powered AlphaGo, combined with neural networks. See: [00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb](00_AI_Fundamentals/classical_ai/05_adversarial_search_and_games.ipynb)

**Multi-Agent System** — Several AI *agents*, often with different roles (researcher, writer, reviewer), working together on a task by passing messages or results between them. See: [10_Agents/04_multi_agent_frameworks.ipynb](10_Agents/04_multi_agent_frameworks.ipynb)

**Multimodal AI** — AI that works with more than one kind of data, such as text plus images, audio or video, for example describing a photo or answering questions about a chart. See: [08_LLM/11_multimodal/01_multimodal_ai.ipynb](08_LLM/11_multimodal/01_multimodal_ai.ipynb)

**Multiple Comparisons Correction (Bonferroni / Holm / BH)** — Adjustments needed when you run many statistical tests, because with 20 tests at α = 0.05 you expect one false "discovery" by chance. Bonferroni and Holm control the chance of any false positive; Benjamini-Hochberg (BH) controls the expected share of false discoveries. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**Mutex (Lock)** — A lock that only one thread can hold at a time, used to protect shared data from *race conditions*. In Python: `with threading.Lock():`. A semaphore is the generalization that allows up to *k* holders. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**MVCC (Multiversion Concurrency Control)** — A database technique that keeps several versions of each row so readers see a consistent snapshot while writers create new versions, meaning readers never block writers. Used by PostgreSQL, MySQL InnoDB and Oracle. See: [13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb](13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb)

## N

**Naive Bayes** — A fast classifier based on *Bayes' theorem* that "naively" assumes every feature is independent of the others given the class. Despite that simplification it works well for text, such as spam filtering. See: [03_Machine_Learning/01_supervised/06_naive_bayes.ipynb](03_Machine_Learning/01_supervised/06_naive_bayes.ipynb)

**Named Entity Recognition (NER)** — Finding and labeling names of things in text, such as people, organizations, places and dates. *Example:* in "Tim Cook visited Paris in May", tag Tim Cook = PERSON, Paris = PLACE, May = DATE. See: [07_NLP/04_named_entity_recognition.ipynb](07_NLP/04_named_entity_recognition.ipynb)

**Nested Cross-Validation** — An inner cross-validation loop for choosing hyperparameters inside an outer loop that only measures performance. It prevents the optimistic bias you get when the same folds are used both to tune and to score. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Neural Network** — A model made of layers of simple units (*neurons*). Each neuron computes a weighted sum of its inputs and applies an *activation function*. By adjusting the weights, the network learns complex patterns. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Neuron** — The basic unit of a neural network: it multiplies each input by a weight, adds them up with a bias, and passes the result through an *activation function*. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**NLP (Natural Language Processing)** — The part of AI that deals with human language: reading, understanding, classifying, translating and generating text. See: [07_NLP/notes/07_NLP.md](07_NLP/notes/07_NLP.md)

**No Free Lunch Theorem** — Averaged over all possible problems, no learning algorithm beats any other. An algorithm only works well because its built-in assumptions (inductive bias) match the problems you care about. See: [03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb](03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb)

**Normal (Gaussian) Distribution** — The classic bell-shaped curve, where most values sit near the average and extreme values are rare. Heights and measurement errors are roughly normal. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**Normalization (Database) / Normal Forms** — Splitting tables so each fact is stored once, which prevents update, insert and delete anomalies. The normal forms are increasingly strict: 1NF (atomic values), 2NF, 3NF, *BCNF*. Not to be confused with feature *normalization* (scaling) in ML. See: [13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb](13_Databases/00_dbms_fundamentals/04_functional_dependencies_and_normalization.ipynb)

**Normalizing Flow** — A generative model built from a chain of invertible transformations that turn simple noise into data. Because every step can be reversed, it can compute the exact probability of any sample. *Example:* RealNVP. See: [05_Deep_Learning/20_generative_models_hands_on.ipynb](05_Deep_Learning/20_generative_models_hands_on.ipynb)

**NoSQL Database** — A database that doesn't use fixed relational tables, storing data as documents (JSON-like), key-value pairs, wide columns or graphs instead. It is often chosen for flexible or very large-scale data. See: [13_Databases/02_nosql/01_nosql_databases.ipynb](13_Databases/02_nosql/01_nosql_databases.ipynb)

**NP-Complete / NP-Hard** — A problem is in NP if a proposed answer can be checked quickly. NP-hard problems are at least as hard as every NP problem; NP-complete ones are NP-hard and also in NP. No fast (polynomial-time) algorithm is known for any of them. *Examples:* SAT, the travelling salesman problem, graph colouring. See: [00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb](00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb)

**Numerical Stability** — Whether a computation keeps rounding errors small. Unstable formulas can overflow, underflow or lose precision. *Example:* computing softmax as exp(x)/sum(exp(x)) overflows for large x; subtracting max(x) first fixes it. See: [14_Mathematics/09_numerical_methods.ipynb](14_Mathematics/09_numerical_methods.ipynb)

**NumPy** — The core Python library for fast math on arrays (lists of numbers in one or more dimensions). Almost every data and ML library is built on top of it. See: [02_Data_Analysis/02_numpy.ipynb](02_Data_Analysis/02_numpy.ipynb)

## O

**Object Detection** — Finding *where* objects are in an image (drawing boxes around them) and *what* they are. *Example:* boxes labeled "car", "person" and "bicycle" in a street photo. See: [06_Computer_Vision/03_object_detection.ipynb](06_Computer_Vision/03_object_detection.ipynb)

**Object-Oriented Programming (OOP)** — Organising code into classes that bundle data with the methods that act on it. Key ideas: encapsulation (hide internals), inheritance (reuse a parent class), polymorphism (different classes, same interface). PyTorch's `nn.Module` and scikit-learn estimators are OOP designs. See: [23_Software_Engineering/01_oop_and_solid_principles.ipynb](23_Software_Engineering/01_oop_and_solid_principles.ipynb)

**Observability (Tracing)** — Being able to see what a system did and why, through logs, metrics and traces. For LLM *agents*, a trace records every prompt, tool call, result, token count and timing, so you can debug and measure them. See: [10_Agents/06_agent_observability.ipynb](10_Agents/06_agent_observability.ipynb)

**Off-Policy vs On-Policy Learning** — On-policy methods (such as SARSA) learn about the policy they are actually following; off-policy methods (such as *Q-learning*) learn about a different, usually greedy, policy while behaving more exploratively. Off-policy learning can reuse old data. See: [11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb](11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb)

**OLAP vs OLTP** — OLTP (online transaction processing) systems handle many small, fast reads and writes, such as placing orders. OLAP (online analytical processing) systems run large aggregating queries over history, such as monthly revenue by region. They are usually separate databases, with ETL between them. See: [13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb](13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb)

**OLS (Ordinary Least Squares)** — The standard way to fit *linear regression*: choose coefficients that minimize the sum of squared residuals. Statistics packages also report standard errors, t-tests and confidence intervals for each coefficient. See: [02_Data_Analysis/13_statistical_modeling_and_inference.ipynb](02_Data_Analysis/13_statistical_modeling_and_inference.ipynb)

**One-Hot Encoding** — Turning a category column into several 0/1 columns, one per category. *Example:* color = red/green/blue becomes is_red, is_green, is_blue, with exactly one 1 per row. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**ONNX** — An open file format for trained models, so a model built in one framework (such as PyTorch) can run in another runtime (such as ONNX Runtime), often faster and on more kinds of devices. See: [05_Deep_Learning/17_industry_model_export_and_inference.ipynb](05_Deep_Learning/17_industry_model_export_and_inference.ipynb)

**Optimizer** — The algorithm that updates a model's weights using the *gradients* to reduce the *loss*. Examples are SGD, SGD with momentum, and *Adam*. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**OSI / TCP-IP Model** — Layered descriptions of how networks work. Simplified: link (Wi-Fi, Ethernet) → network (*IP* addresses) → transport (*TCP*/UDP and ports) → application (*HTTP*, *DNS*). Each layer relies only on the one below it. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Outlier** — A data point far away from the rest, caused either by an error (a typo like age = 999) or by something genuinely rare. Outliers can distort averages and some models. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Overfitting** — When a model memorizes the training data, including its noise, so it scores very well on training data but poorly on new data. *Analogy:* a student who memorizes past exam answers but can't solve new questions. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**OWASP Top 10** — The widely used list of the most critical web-application security risks (broken access control, injection, security misconfiguration, and so on), from the OWASP foundation. A separate OWASP Top 10 covers LLM applications, with *prompt injection* first. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

## P

**P vs NP** — The famous open question of whether every problem whose answer can be *checked* quickly (NP) can also be *solved* quickly (P). Most experts believe P ≠ NP; much of cryptography relies on it. See *NP-complete*. See: [00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb](00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb)

**p-Hacking / HARKing** — p-hacking is trying many analyses, subsets or metrics until something gives p < 0.05; HARKing is Hypothesizing After the Results are Known and presenting it as planned. Both produce false findings. *Pre-registration* is the main defence. See: [02_Data_Analysis/13_statistical_modeling_and_inference.ipynb](02_Data_Analysis/13_statistical_modeling_and_inference.ipynb)

**p-value** — Assuming there is really no effect, the probability of seeing a result at least as extreme as the one you got. A small p-value (often below 0.05) suggests the effect is unlikely to be pure chance. It is *not* the probability that the effect is real. See: [02_Data_Analysis/08_statistics.ipynb](02_Data_Analysis/08_statistics.ipynb)

**PAC Learning (Probably Approximately Correct)** — A framework that asks how many examples a learner needs so that, with high probability (1 − δ), its error is small (at most ε). It turns "will this generalize?" into a sample-size question that depends on the model's complexity (see *VC dimension*). See: [03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb](03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb)

**PageRank** — Google's original measure of a web page's importance: the long-run share of time a random surfer, who follows links and sometimes jumps to a random page, spends on it. It is the leading eigenvector of the link matrix, computed by power iteration. See: [14_Mathematics/10_numerical_linear_algebra.ipynb](14_Mathematics/10_numerical_linear_algebra.ipynb)

**pandas** — The main Python library for working with tables of data (*DataFrames*): loading, cleaning, filtering, grouping and summarizing. See: [02_Data_Analysis/03_pandas.ipynb](02_Data_Analysis/03_pandas.ipynb)

**Parameters (Weights and Biases)** — The numbers inside a model that are learned during training. When people say an LLM has "7 billion parameters", these are the numbers they mean. Compare *hyperparameter*. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**PCA (Principal Component Analysis)** — A *dimensionality reduction* method that finds the few directions along which the data varies most and re-describes the data using just those directions. See: [03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb](03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb)

**PEFT (Parameter-Efficient Fine-Tuning)** — A family of methods (such as *LoRA*, adapters and prompt tuning) that adapt a big pretrained model by training only a small number of extra or selected parameters, saving memory, time and storage. See: [05_Deep_Learning/12_advanced_peft.ipynb](05_Deep_Learning/12_advanced_peft.ipynb)

**Permutation Test** — A test that builds the "no effect" distribution by randomly shuffling group labels many times and recomputing the statistic. The p-value is the share of shuffles at least as extreme as the real result. It needs almost no assumptions. See: [02_Data_Analysis/13_statistical_modeling_and_inference.ipynb](02_Data_Analysis/13_statistical_modeling_and_inference.ipynb)

**Perplexity** — A score for language models: roughly, how "surprised" the model is by real text. Lower is better. A perplexity of 10 means the model is about as unsure as if it were choosing among 10 equally likely next tokens. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Pipeline (scikit-learn)** — A chain of steps (for example: fill missing values → scale → model) bundled into one object, so the exact same steps run in training and prediction and you avoid *data leakage*. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**Policy Gradient (REINFORCE)** — Reinforcement-learning methods that directly adjust the policy's parameters to make actions that led to high return more likely. REINFORCE is the simplest version; subtracting a baseline reduces its high variance. *Actor-critic* and *PPO* build on it. See: [11_Reinforcement_Learning/05_policy_gradient.ipynb](11_Reinforcement_Learning/05_policy_gradient.ipynb)

**PPO (Proximal Policy Optimization)** — A popular, stable *policy-gradient* method that limits how much the policy can change in one update by clipping the probability ratio between new and old policies. Often paired with GAE for advantage estimates. It was the RL algorithm in the original *RLHF* recipe for ChatGPT. See: [11_Reinforcement_Learning/10_deep_rl_on_cpu.ipynb](11_Reinforcement_Learning/10_deep_rl_on_cpu.ipynb)

**Pre-Registration** — Writing down your hypotheses, metrics and analysis plan (and ideally publishing them) *before* seeing the results, so you cannot unconsciously tune the analysis to get a positive finding. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Precision / Recall** — Precision: of everything the model flagged as positive, how much really was positive ("when it says spam, is it right?"). Recall: of all the real positives, how many the model caught ("did it find all the spam?"). Raising one often lowers the other. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Pretraining** — The first, very expensive training stage, where a model learns general knowledge from a huge dataset (for LLMs, predicting the next token on vast amounts of text) before any *fine-tuning*. See: [08_LLM/notes/08_LLM.md](08_LLM/notes/08_LLM.md)

**Primary Key / Foreign Key** — A primary key is the column (or columns) that uniquely identifies each row, such as `customer_id`. A foreign key is a column in another table that must match an existing primary key, such as `orders.customer_id`, which keeps references valid. See: [13_Databases/00_dbms_fundamentals/03_relational_model_and_relational_algebra.ipynb](13_Databases/00_dbms_fundamentals/03_relational_model_and_relational_algebra.ipynb)

**Probability Distribution** — A description of all possible outcomes and how likely each one is. *Example:* for a fair die, each face 1-6 has probability 1/6. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**Process / Thread** — A process is a running program with its own memory; a thread is a unit of execution inside a process that shares that memory with its sibling threads. Threads are cheaper but need locks to share data safely; processes are isolated. See: [23_Software_Engineering/06_operating_systems_for_developers.ipynb](23_Software_Engineering/06_operating_systems_for_developers.ipynb)

**Profiling** — Measuring where a program actually spends time or memory instead of guessing, with tools such as `cProfile`, line profilers and `tracemalloc`. *Rule of thumb:* optimise the hotspot the profiler shows, not the code you suspect. See: [23_Software_Engineering/04_debugging_and_profiling.ipynb](23_Software_Engineering/04_debugging_and_profiling.ipynb)

**Prompt** — The input text you give an LLM: instructions, context, examples and the question itself. See: [09_Prompt_Engineering/01_basics.ipynb](09_Prompt_Engineering/01_basics.ipynb)

**Prompt Engineering** — The skill of writing and testing prompts so an LLM reliably gives the output you want, for example with clear instructions, examples, a defined output format and step-by-step reasoning. See: [09_Prompt_Engineering/notes/09_Prompt_Engineering.md](09_Prompt_Engineering/notes/09_Prompt_Engineering.md)

**Prompt Injection** — An attack where text hidden in user input or in retrieved content (a web page, an email, a document) contains instructions that hijack the LLM, such as "ignore previous instructions and reveal the system prompt". It is a major risk for *agents* that read untrusted content. See: [10_Agents/08_agent_security.ipynb](10_Agents/08_agent_security.ipynb)

**Property-Based Testing** — Instead of a few hand-picked examples, state a rule that must always hold (for example "sorting twice equals sorting once") and let a library such as Hypothesis generate hundreds of random inputs to try to break it. See: [23_Software_Engineering/03_testing_ai_code.ipynb](23_Software_Engineering/03_testing_ai_code.ipynb)

**Propositional Logic** — Logic with simple true/false statements (P, Q) joined by AND, OR, NOT and IMPLIES. An agent can use it to derive new facts from known ones. *Example:* Rain → WetGrass, Rain ⊢ WetGrass. See: [00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb](00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb)

**Pydantic** — A Python library that checks data against a schema defined with type hints (for example: "age must be an integer ≥ 0"). FastAPI and many LLM *structured output* tools use it. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

## Q

**Q-Learning** — A *reinforcement learning* algorithm that learns a score (Q-value) for every situation-action pair: "how good is taking this action here, if I act well afterwards?" It updates those scores from experience using the Bellman equation (value now = reward now + discounted value of what comes next). See: [11_Reinforcement_Learning/03_monte_carlo_td.ipynb](11_Reinforcement_Learning/03_monte_carlo_td.ipynb)

**Quantization** — Storing a model's numbers with fewer bits (for example 8-bit or 4-bit integers instead of 32-bit decimals). The model becomes several times smaller and often faster, usually with only a small loss in quality. See: [05_Deep_Learning/13_quantization_and_compression_advanced.ipynb](05_Deep_Learning/13_quantization_and_compression_advanced.ipynb)

**Query Optimizer** — The database component that turns a SQL query into the cheapest execution plan it can find, choosing join order, *join algorithms* and *indexes* from estimates of how many rows each step returns. `EXPLAIN` shows the plan it chose. See: [13_Databases/00_dbms_fundamentals/08_query_processing_and_optimization.ipynb](13_Databases/00_dbms_fundamentals/08_query_processing_and_optimization.ipynb)

## R

**Race Condition** — A bug where the result depends on the unpredictable timing of threads or tasks. *Example:* two threads both read a counter of 5, both add 1, both write 6, and one increment is lost. Fixed with locks, atomic operations or by avoiding shared state. See: [23_Software_Engineering/05_concurrency_and_async.ipynb](23_Software_Engineering/05_concurrency_and_async.ipynb)

**RAG (Retrieval-Augmented Generation)** — Making an LLM answer from your own documents: first *retrieve* the most relevant passages (usually with *embeddings*), then put them in the prompt so the model *generates* an answer grounded in them. It reduces *hallucinations* and keeps answers up to date. *Analogy:* an open-book exam. See: [08_LLM/02_rag/01_rag_fundamentals.ipynb](08_LLM/02_rag/01_rag_fundamentals.ipynb)

**Random Forest** — An *ensemble* of many *decision trees*, each trained on a random sample of rows and features, that vote on the answer. It is accurate, robust and a strong default for tabular data. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**Random Seed** — The starting value of a pseudo-random number generator. Fixing it makes shuffling, initialization and sampling repeatable. Report results over several seeds, because a single lucky seed can mislead; a seed is not a hyperparameter to tune. See: [24_Research_Methods/04_reproducibility_and_research_code.ipynb](24_Research_Methods/04_reproducibility_and_research_code.ipynb)

**Randomized Algorithm** — An algorithm that flips coins to make choices. Las Vegas algorithms are always correct but have random running time (randomized quicksort); Monte Carlo algorithms have fixed time but may be wrong with small probability (Miller-Rabin primality test). See: [00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/01_amortized_and_randomized_algorithms.ipynb)

**Rate Limiting (Token Bucket)** — Capping how many requests a client may make per time window, to protect a service and share it fairly. In the token-bucket algorithm a bucket refills at *r* tokens per second up to a maximum *b*, and each request spends one token, which allows short bursts. Over the limit, APIs answer HTTP 429. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Rational Agent** — In classical AI, an agent that perceives its environment and chooses the action expected to maximize its performance measure, given what it has seen and knows. Tasks are often described with PEAS: Performance measure, Environment, Actuators, Sensors. See: [00_AI_Fundamentals/classical_ai/01_types_of_ai_and_intelligent_agents.ipynb](00_AI_Fundamentals/classical_ai/01_types_of_ai_and_intelligent_agents.ipynb)

**ReAct (Reason + Act)** — A common *agent* pattern where the model alternates between thinking ("I need the population of France"), acting (calling a search tool) and observing the result, until it can answer. See: [10_Agents/01_agent_fundamentals.ipynb](10_Agents/01_agent_fundamentals.ipynb)

**Reasoning Model** — An LLM trained to produce a long internal chain of reasoning before answering, which tends to help on math, coding and multi-step problems at the cost of more tokens and time. Spending more compute while answering is called "test-time compute". See: [08_LLM/18_reasoning_models.ipynb](08_LLM/18_reasoning_models.ipynb)

**Recommendation System** — A system that suggests items a user is likely to want (products, movies, songs) based on their past behavior, similar users, item content, or a mix. See: [03_Machine_Learning/09_recommendation_systems/01_recommendation_systems.ipynb](03_Machine_Learning/09_recommendation_systems/01_recommendation_systems.ipynb)

**Recurrence Relation** — An equation that defines each term of a sequence from earlier terms, such as Fibonacci F(n) = F(n − 1) + F(n − 2). Algorithm running times are often recurrences, solved by unrolling, the *Master theorem* or generating functions. See: [14_Mathematics/discrete_math/02_combinatorics_and_recurrences.ipynb](14_Mathematics/discrete_math/02_combinatorics_and_recurrences.ipynb)

**Recursion** — A function that solves a problem by calling itself on smaller versions of it until it reaches a simple base case. *Example:* factorial(n) = n × factorial(n − 1), with factorial(0) = 1. Each call uses stack space, so very deep recursion can overflow. See: [00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb](00_AI_Fundamentals/dsa/01_complexity_analysis_and_recursion.ipynb)

**Red Teaming** — Deliberately attacking your own AI system (with *jailbreaks*, *prompt injection*, tricky edge cases) to find failures before real attackers or users do. See: [19_AI_Ethics_and_Safety/09_industry_ai_incident_response_and_red_teaming.ipynb](19_AI_Ethics_and_Safety/09_industry_ai_incident_response_and_red_teaming.ipynb)

**Reduction** — Transforming every instance of problem A into an instance of problem B, so a solver for B also solves A. Reductions prove hardness: if a known *NP-complete* problem reduces to your problem in polynomial time, your problem is NP-hard too. See: [00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb](00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb)

**Regression** — A *supervised learning* task where the answer is a number. *Examples:* predicting a house price, a temperature, or delivery time. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**Regular Expression (Regex)** — A compact pattern language for matching text, such as `\d{3}-\d{4}` for a phone-number fragment. Regexes describe exactly the regular languages that finite automata recognise. Badly written patterns can backtrack exponentially (ReDoS). See: [14_Mathematics/discrete_math/04_automata_and_regular_languages.ipynb](14_Mathematics/discrete_math/04_automata_and_regular_languages.ipynb)

**Regularization (L1 / L2, Lasso / Ridge)** — Adding a penalty for large weights during training to keep a model simpler and reduce *overfitting*. L2 (Ridge) shrinks all weights a little; L1 (Lasso) can push some weights to exactly zero, which also selects features. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**Reinforcement Learning (RL)** — Learning by trial and error: an *agent* takes actions in an environment, receives rewards or penalties, and learns a strategy (called a policy) that maximizes total reward over time. *Analogy:* training a dog with treats. See: [11_Reinforcement_Learning/notes/11_Reinforcement_Learning.md](11_Reinforcement_Learning/notes/11_Reinforcement_Learning.md)

**Relational Algebra** — The small set of operations on tables that underlies SQL: select (filter rows), project (pick columns), join, union, difference and rename. Databases translate SQL into relational algebra before optimizing it. See: [13_Databases/00_dbms_fundamentals/03_relational_model_and_relational_algebra.ipynb](13_Databases/00_dbms_fundamentals/03_relational_model_and_relational_algebra.ipynb)

**ReLU (Rectified Linear Unit)** — The most common *activation function*: output the input if it is positive, otherwise output 0. It is simple, fast and works well in deep networks. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Reparameterization Trick** — Writing a random sample as a deterministic function of the parameters plus independent noise (z = μ + σ·ε, with ε ~ N(0, 1)) so gradients can flow through the sampling step. It is what makes *VAEs* trainable with backpropagation. See: [05_Deep_Learning/20_generative_models_hands_on.ipynb](05_Deep_Learning/20_generative_models_hands_on.ipynb)

**Replication** — Keeping copies of the same data on several machines for safety and read speed. In leader-follower replication one node accepts writes and copies them to the followers; replication lag means followers can briefly return stale data. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Reproducibility** — Being able to get the same results again: repeatable (same team, same setup), reproducible (another team, same code and data) and replicable (another team, new implementation or data). It needs fixed *random seeds*, pinned environments, versioned data and logged configurations. See: [24_Research_Methods/04_reproducibility_and_research_code.ipynb](24_Research_Methods/04_reproducibility_and_research_code.ipynb)

**REST API** — A common style of web API where you use standard HTTP methods on URLs: `GET /items/5` reads an item, `POST /items` creates one, `DELETE /items/5` removes it. See: [12_FastAPI/notes/12_FastAPI.md](12_FastAPI/notes/12_FastAPI.md)

**Reward** — The number an RL environment gives the agent after each action to signal how good it was, for example +1 for winning a game or -1 for crashing. See: [11_Reinforcement_Learning/01_rl_fundamentals.ipynb](11_Reinforcement_Learning/01_rl_fundamentals.ipynb)

**Reward Shaping** — Adding extra reward signals to guide an RL agent toward the goal faster. Done carelessly it changes the optimal behaviour (the agent "games" the bonus); potential-based shaping is the provably safe form. See: [11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb](11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb)

**RLHF (Reinforcement Learning from Human Feedback)** — An *alignment* method: people compare pairs of model answers, a "reward model" learns to predict which answers people prefer, and the LLM is then trained with reinforcement learning (often PPO) to produce answers the reward model scores highly. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**RNN (Recurrent Neural Network)** — A neural network for sequences (text, time series) that reads one step at a time while carrying a "memory" (hidden state) forward. Plain RNNs forget long-range information, which led to *LSTMs* and the similar, simpler GRUs. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

**Roofline Model** — A chart that shows whether a computation is limited by compute speed (FLOP/s) or memory bandwidth (bytes/s), based on its arithmetic intensity (FLOPs per byte moved). *Example:* LLM token generation does little math per weight loaded, so it is memory-bound. See: [23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb](23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb)

## S

**SARSA** — An *on-policy* temporal-difference control method named after the tuple it learns from (State, Action, Reward, next State, next Action). It updates Q(s, a) toward r + γ·Q(s′, a′) using the action actually taken, so it learns safer paths than *Q-learning* when exploration is risky. See: [11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb](11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb)

**SAT (Boolean Satisfiability)** — Deciding whether some true/false assignment makes a logical formula true. It was the first problem proved *NP-complete* (Cook-Levin), yet modern SAT solvers handle millions of variables in practice and are used for hardware verification and scheduling. See: [00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb](00_AI_Fundamentals/advanced_algorithms/02_np_completeness_and_reductions.ipynb)

**scikit-learn (sklearn)** — The standard Python library for classic machine learning. It offers models, preprocessing, *pipelines* and evaluation tools, all with the same `fit` / `predict` interface. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**Seasonality / Trend** — Two parts of a time series. Trend is the long-term direction (sales slowly growing). Seasonality is a pattern that repeats on a fixed calendar cycle (more ice cream in summer, more traffic on Mondays). See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Self-Balancing BST (AVL / Red-Black Tree)** — A *binary search tree* that rotates nodes after inserts and deletes to keep its height O(log n), so operations never degrade to a slow list. AVL trees are more strictly balanced; red-black trees do fewer rotations and are used in many standard libraries. See: [00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb](00_AI_Fundamentals/dsa/06_trees_bst_and_heaps.ipynb)

**Self-Supervised Learning** — Learning from unlabeled data by creating the labels from the data itself, such as hiding a word and predicting it, or predicting the next token. This is how LLMs and many vision models are pretrained. See: [05_Deep_Learning/09_self_supervised_learning.ipynb](05_Deep_Learning/09_self_supervised_learning.ipynb)

**Semantic Search** — Searching by meaning instead of exact words, by comparing *embeddings*. A query for "cheap flights" can find a page that says "low-cost airfare". See: [07_NLP/13_industry_semantic_search_engine.ipynb](07_NLP/13_industry_semantic_search_engine.ipynb)

**Semantic Versioning (SemVer)** — A version-numbering rule, MAJOR.MINOR.PATCH (for example 2.4.1). Bump MAJOR for breaking changes, MINOR for new backward-compatible features, PATCH for bug fixes. See: [20_Git_and_DevOps/04_semantic_versioning.ipynb](20_Git_and_DevOps/04_semantic_versioning.ipynb)

**Semi-Supervised Learning** — Training with a small amount of labeled data plus a large amount of unlabeled data, which is useful when labels are expensive. See: [03_Machine_Learning/03_semi_supervised/01_semi_supervised_learning.ipynb](03_Machine_Learning/03_semi_supervised/01_semi_supervised_learning.ipynb)

**Seq2Seq (Sequence-to-Sequence)** — An *encoder-decoder* model that reads an input sequence and generates an output sequence of possibly different length, as in translation or summarization. Adding *attention* to RNN seq2seq models led directly to the *transformer*. See: [05_Deep_Learning/19_sequence_models_hands_on.ipynb](05_Deep_Learning/19_sequence_models_hands_on.ipynb)

**Serializability** — The gold standard of correctness for concurrent transactions: the outcome equals what you would get by running them one at a time in some order. Usually checked with a precedence graph (no cycles means conflict-serializable) and enforced by *two-phase locking* or similar. See: [13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb](13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb)

**Server-Sent Events (SSE)** — A simple way for a server to push a stream of text events to a browser over one long-lived HTTP response (`Content-Type: text/event-stream`). It is how most chat apps stream LLM tokens as they are generated. For two-way messaging use a *WebSocket*. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**SHAP** — An *explainability* method based on Shapley values from game theory. It splits a prediction into fair contributions from each feature, such as "income added +0.20 to the approval score and debt subtracted -0.15". See: [03_Machine_Learning/07_explainability/01_explainability.ipynb](03_Machine_Learning/07_explainability/01_explainability.ipynb)

**Sharding (Partitioning)** — Splitting a large dataset across several machines by a key (for example user_id), so each machine stores and serves only part of it. A badly chosen key creates "hot" shards that get most of the traffic. See: [23_Software_Engineering/09_system_design_fundamentals.ipynb](23_Software_Engineering/09_system_design_fundamentals.ipynb)

**Sigmoid** — An S-shaped function that squashes any number into the range 0 to 1, which makes it handy for turning a score into a probability (as in *logistic regression*). See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**SIMD / Vectorization** — Single Instruction, Multiple Data: CPU instructions that apply one operation to several numbers at once. NumPy's vectorized operations use them (and avoid Python loops), which is why `a + b` on arrays is far faster than a `for` loop. See: [23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb](23_Software_Engineering/12_computer_architecture_for_ai_performance.ipynb)

**Simpson's Paradox** — A trend that appears in every subgroup but reverses when the groups are combined, caused by unequal group sizes or a *confounder*. *Example:* model A beats B on both easy and hard test items, but B looks better overall because it was tested on more easy items. See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Simulated Annealing** — A local search that sometimes accepts worse moves, with a probability that shrinks as a "temperature" cools, so it can escape local optima early and settle down later. Inspired by slowly cooling metal. See: [00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb](00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb)

**Sketch (Streaming Algorithm)** — A small summary of a huge data stream that answers approximate questions (counts, distinct items, quantiles) in one pass with bounded memory. *Examples:* *Count-Min sketch*, *HyperLogLog*, t-digest for p99 latency. See: [00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb](00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb)

**SLI / SLO / Error Budget** — An SLI (service level indicator) is a measured number, such as the share of requests answered in under 500 ms. An SLO (objective) is its target, such as 99.9% over 30 days. The error budget is the failure the SLO allows (0.1%); while budget remains you can ship risky changes, and when it runs out you focus on reliability. See: [15_MLOps/16_observability_hands_on.ipynb](15_MLOps/16_observability_hands_on.ipynb)

**Sliding Window** — A technique for problems about contiguous ranges: move a window across the array, adding the new element and removing the old one, instead of recomputing from scratch. Turns many O(n²) problems into O(n). See: [00_AI_Fundamentals/dsa/02_arrays_strings_and_techniques.ipynb](00_AI_Fundamentals/dsa/02_arrays_strings_and_techniques.ipynb)

**Small Language Model (SLM)** — A language model small enough (roughly hundreds of millions to a few billion parameters) to run cheaply on a laptop, phone or single GPU. It is less capable than the largest models, but fast, private and often good enough for focused tasks. See: [08_LLM/05_slms/01_small_language_models.ipynb](08_LLM/05_slms/01_small_language_models.ipynb)

**Softmax** — A function that turns a list of scores (*logits*) into probabilities that are all positive and add up to 1. *Example:* scores [2, 1, 0] become about [0.67, 0.24, 0.09]. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**SOLID** — Five object-oriented design principles: Single responsibility (one reason to change), Open/closed (extend without editing), Liskov substitution (subclasses must work wherever the parent does), Interface segregation (small, focused interfaces), Dependency inversion (depend on abstractions, not concrete classes). See: [23_Software_Engineering/01_oop_and_solid_principles.ipynb](23_Software_Engineering/01_oop_and_solid_principles.ipynb)

**Spark (Apache Spark)** — A distributed engine for processing big data across a cluster with DataFrame and SQL APIs. It builds a lazy plan of transformations and only runs it when an action (such as `count()`) needs a result; shuffles (moving data between machines) are the expensive part. PySpark is its Python API. See: [13_Databases/06_data_engineering/03_spark_locally.ipynb](13_Databases/06_data_engineering/03_spark_locally.ipynb)

**Spatial Cross-Validation** — Splitting geographic data into folds by area (spatial blocks) instead of at random. Nearby points are similar (spatial autocorrelation), so random splits leak information and overstate how well a model works in new places. See: [03_Machine_Learning/18_domain_applications/01_geospatial_machine_learning.ipynb](03_Machine_Learning/18_domain_applications/01_geospatial_machine_learning.ipynb)

**SQL (Structured Query Language)** — The standard language for asking questions of relational databases. *Example:* `SELECT name FROM customers WHERE country = 'UK'`. See: [13_Databases/01_sql/01_sql_fundamentals.ipynb](13_Databases/01_sql/01_sql_fundamentals.ipynb)

**SQL Injection** — An attack where user input is pasted into a SQL query and changes its meaning. *Example:* a name of `' OR 1=1 --` returns every row. Prevented by always using parameterized queries, never string formatting. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

**Stack / Queue** — Two basic collections. A stack is last-in, first-out (LIFO), like a pile of plates: push and pop at the top (undo history, function calls). A queue is first-in, first-out (FIFO), like a checkout line (task queues, *BFS*). See: [00_AI_Fundamentals/dsa/05_linked_lists_stacks_queues.ipynb](00_AI_Fundamentals/dsa/05_linked_lists_stacks_queues.ipynb)

**Standardization / Normalization (Feature Scaling)** — Putting features on similar scales so none dominates just because of its units. Standardization makes a column have mean 0 and standard deviation 1; min-max normalization squeezes it into 0-1. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**Star Schema** — The standard *data warehouse* layout: a central fact table of events or measurements (sales: amount, quantity) linked to surrounding dimension tables that describe them (date, product, store). Simple to query for reports. See: [13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb](13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb)

**Stationarity** — A time series is stationary when its basic behavior (average, spread, how it relates to its own past) doesn't change over time. Many classical models like *ARIMA* assume it, so trends are often removed first. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Statistical Power / Power Analysis** — Power is the probability that a test detects an effect that really exists (commonly targeted at 80%). Power analysis works out the sample size you need to detect the smallest effect you care about (the minimum detectable effect). See: [24_Research_Methods/02_experiment_design_for_ml.ipynb](24_Research_Methods/02_experiment_design_for_ml.ipynb)

**Stochastic Gradient Descent (SGD)** — *Gradient descent* that updates the weights using a small random *mini-batch* instead of the whole dataset each step. It is noisier, but much faster and the basis of all neural-network training. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**STRIPS** — A classic language for AI planning that describes each action by its preconditions and its effects (facts added and facts deleted). A planner then searches for a sequence of actions that turns the start state into the goal. PDDL is its modern successor. See: [00_AI_Fundamentals/classical_ai/08_reasoning_and_planning.ipynb](00_AI_Fundamentals/classical_ai/08_reasoning_and_planning.ipynb)

**Structured Logging** — Writing logs as machine-readable records (usually JSON with fields such as timestamp, level, request_id, latency_ms) instead of free text, so they can be searched, filtered and aggregated. A request ID ties together every log line from one request. See: [15_MLOps/16_observability_hands_on.ipynb](15_MLOps/16_observability_hands_on.ipynb)

**Structured Output** — Making an LLM reply in an exact machine-readable format, usually *JSON* that matches a schema, so your code can use the answer reliably. See: [08_LLM/17_structured_outputs.ipynb](08_LLM/17_structured_outputs.ipynb)

**Supervised Learning** — Learning from examples that come with the correct answers (*labels*). The two main types are *classification* and *regression*. See: [03_Machine_Learning/01_supervised/notes/01_supervised.md](03_Machine_Learning/01_supervised/notes/01_supervised.md)

**SVD (Singular Value Decomposition)** — Factoring any matrix as A = UΣVᵀ: rotate, stretch along independent directions by the singular values, rotate again. Keeping only the largest singular values gives the best low-rank approximation, which is the basis of *PCA*, compression and recommender systems. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**SVM (Support Vector Machine)** — A classifier that finds the boundary separating the classes with the widest possible gap (margin). With the "kernel trick" (measuring similarity as if the data had extra dimensions) it can draw curved boundaries. See: [03_Machine_Learning/01_supervised/05_svm.ipynb](03_Machine_Learning/01_supervised/05_svm.ipynb)

**System Prompt** — Hidden instructions given to a chat LLM before the user's messages to set its role, rules and style (for example "You are a polite support assistant for a bank; never give investment advice"). See: [08_LLM/07_prompt_engineering/notes/07_prompt_engineering.md](08_LLM/07_prompt_engineering/notes/07_prompt_engineering.md)

## T

**TCP / UDP** — The two main transport protocols. TCP gives a reliable, ordered byte stream (lost packets are re-sent) and is used by HTTP, databases and SSH. UDP sends independent packets with no guarantees but lower delay, used for video calls, games and DNS. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**TD Learning (Temporal-Difference Learning)** — Learning value estimates from every step by nudging the current estimate toward the observed reward plus the estimated value of the next state, rather than waiting for the episode to end. *Q-learning* and *SARSA* are TD methods. See: [11_Reinforcement_Learning/03_monte_carlo_td.ipynb](11_Reinforcement_Learning/03_monte_carlo_td.ipynb)

**TDD (Test-Driven Development)** — Writing a failing test first (red), then the simplest code that passes it (green), then cleaning up (refactor), in short cycles. It forces you to define behaviour before implementation. See: [23_Software_Engineering/03_testing_ai_code.ipynb](23_Software_Engineering/03_testing_ai_code.ipynb)

**Temperature** — A generation setting that controls randomness. Low temperature (near 0) makes the model pick the most likely tokens, giving focused and repeatable answers; higher temperature spreads the probability out, giving more varied and creative output. Technically, the *logits* are divided by the temperature before the *softmax*. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Tensor** — A multi-dimensional array of numbers, the basic data type in PyTorch: a single number, a vector, a matrix, or higher (a color image is height × width × 3). See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**TF-IDF** — A way to turn text into numbers: a word gets a high score in a document if it appears often there (term frequency) but rarely across all documents (inverse document frequency). Common words like "the" score low. See: [07_NLP/01_text_preprocessing.ipynb](07_NLP/01_text_preprocessing.ipynb)

**Threat Modeling (STRIDE)** — Systematically listing how a system could be attacked before building defences. STRIDE is a checklist: Spoofing, Tampering, Repudiation, Information disclosure, Denial of service, Elevation of privilege. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

**Time Series** — Data recorded in time order, such as daily sales, hourly temperature or stock prices, where the order matters. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**TLS (Transport Layer Security)** — The encryption layer behind HTTPS. It verifies the server's identity with a certificate and then encrypts traffic so nobody in between can read or change it. The padlock in the browser means TLS is active. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Token / Tokenization** — LLMs don't read letters or whole words; they read *tokens*, which are chunks of text (often a word or part of a word). Tokenization is the step that splits text into tokens and maps each to a number. Prices and *context windows* are measured in tokens. See: [07_NLP/01_text_preprocessing.ipynb](07_NLP/01_text_preprocessing.ipynb)

**Tool (Agent Tool)** — A function an *agent* can call, such as web search, a calculator, a database query or sending an email. It is described to the LLM with a name, a purpose and input parameters. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

**Top-k / Top-p (Nucleus) Sampling** — Ways to pick the next token when generating text. Top-k samples only from the k most likely tokens; top-p samples from the smallest set of tokens whose combined probability reaches p (for example 0.9). Both cut off unlikely nonsense. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Topological Sort** — Ordering the nodes of a directed acyclic graph (DAG) so every edge points forward, meaning each task comes after the tasks it depends on. *Examples:* build systems, pipeline orchestrators such as Airflow, course prerequisites. See: [00_AI_Fundamentals/dsa/07_graphs.ipynb](00_AI_Fundamentals/dsa/07_graphs.ipynb)

**Train / Validation / Test Split** — Dividing data into three parts: *train* to learn from, *validation* to tune settings and choose models, and *test*, used once at the end for an honest final score. *Analogy:* homework, practice exams and the real exam. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**Transfer Learning** — Reusing a model trained on one big task as the starting point for a related task, so you need far less data and time. *Example:* start from a network trained on millions of photos and fine-tune it to spot defects in your factory's products. See: [06_Computer_Vision/02_image_classification.ipynb](06_Computer_Vision/02_image_classification.ipynb)

**Transformer** — The neural-network architecture (introduced in 2017) behind modern LLMs and many vision models. It is built from self-attention (see *Attention*) and simple feed-forward layers, and it processes all tokens in parallel rather than one by one like an *RNN*. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

**Trie (Prefix Tree)** — A tree that stores strings character by character, so all words sharing a prefix share a path. It makes autocomplete and prefix search fast, and is used inside tokenizers. See: [00_AI_Fundamentals/dsa/11_advanced_tries_strings_and_range_queries.ipynb](00_AI_Fundamentals/dsa/11_advanced_tries_strings_and_range_queries.ipynb)

**Turing Machine** — The standard mathematical model of a computer: a finite set of rules reading and writing symbols on an unlimited tape. The Church-Turing thesis says anything that can be computed by a step-by-step procedure can be computed by one. See: [14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb](14_Mathematics/discrete_math/05_grammars_parsing_and_computability.ipynb)

**Two-Phase Commit (2PC)** — A protocol that makes a transaction spanning several databases all-or-nothing. A coordinator first asks every participant to prepare and vote, then tells all of them to commit only if every vote is yes; otherwise all abort. See: [13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb](13_Databases/00_dbms_fundamentals/09_distributed_databases_warehousing_and_security.ipynb)

**Two-Phase Locking (2PL)** — A locking rule that guarantees *serializability*: each transaction first only acquires locks (growing phase), then only releases them (shrinking phase). Strict 2PL holds write locks until commit to avoid cascading aborts. It can cause *deadlocks*. See: [13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb](13_Databases/00_dbms_fundamentals/05_transactions_and_concurrency_control.ipynb)

**Type I / Type II Error** — A Type I error is a false positive (declaring an effect that is not real; its rate is α, often 0.05). A Type II error is a false negative (missing a real effect; its rate is β, and *statistical power* = 1 − β). See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

## U

**Underfitting** — When a model is too simple to capture the real pattern, so it does badly on both training and new data. *Example:* fitting a straight line to data that clearly curves. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Unification** — Finding a substitution of variables that makes two logical expressions identical. *Example:* Knows(John, x) and Knows(y, Mother(y)) unify with y = John, x = Mother(John). It is the core step of reasoning in *first-order logic* and Prolog. See: [00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb](00_AI_Fundamentals/classical_ai/07_knowledge_representation_and_logic.ipynb)

**Uniform-Cost Search** — A search that always expands the cheapest path found so far, so it finds the lowest-cost path when step costs differ. It is essentially *Dijkstra's algorithm*, and *A\* search* is uniform-cost search plus a heuristic. See: [00_AI_Fundamentals/classical_ai/02_uninformed_search.ipynb](00_AI_Fundamentals/classical_ai/02_uninformed_search.ipynb)

**Union-Find (Disjoint Set Union)** — A structure that tracks which items belong to the same group, with near-constant-time `union` (merge two groups) and `find` (which group?) thanks to path compression and union by rank. Used in Kruskal's MST algorithm and clustering. See: [00_AI_Fundamentals/dsa/07_graphs.ipynb](00_AI_Fundamentals/dsa/07_graphs.ipynb)

**Unit Test / Integration Test** — A unit test checks one small piece (a function or class) in isolation, usually with *mocks*; an integration test checks that several pieces work together (API + model + database). Most suites follow the testing pyramid: many unit tests, fewer integration tests, very few end-to-end tests. See: [23_Software_Engineering/03_testing_ai_code.ipynb](23_Software_Engineering/03_testing_ai_code.ipynb)

**Unsupervised Learning** — Finding structure in data without any labels, for example *clustering* similar customers or *dimensionality reduction*. See: [03_Machine_Learning/02_unsupervised/notes/02_unsupervised.md](03_Machine_Learning/02_unsupervised/notes/02_unsupervised.md)

## V

**VAE (Variational Autoencoder)** — A generative *autoencoder* whose encoder outputs a probability distribution (mean and variance) for each input instead of a single point, and whose latent space is pushed toward a standard normal. Sampling a random latent vector and decoding it produces new data. Trained by maximizing the *ELBO* with the *reparameterization trick*. See: [05_Deep_Learning/06_generative_models.ipynb](05_Deep_Learning/06_generative_models.ipynb)

**Validation Set** — Data held back from training and used to compare models and tune *hyperparameters*. It is separate from the final test set (see *Train / Validation / Test Split*). See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Value Iteration / Policy Iteration** — Dynamic-programming methods for solving an *MDP* when its model is known. Value iteration repeatedly applies the *Bellman* optimality update until values stop changing; policy iteration alternates evaluating the current policy and improving it greedily. See: [11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb](11_Reinforcement_Learning/09_tabular_rl_from_scratch.ipynb)

**Vanishing / Exploding Gradients** — In deep or recurrent networks, gradients are multiplied through many layers and can shrink toward zero (early layers stop learning) or grow huge (training blows up). Fixes include ReLU, careful *weight initialization*, normalization layers, residual connections and *gradient clipping*. See: [05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb](05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb)

**Variable Elimination** — An exact inference algorithm for graphical models that sums out variables one at a time, storing intermediate tables so nothing is computed twice. A good elimination order keeps those tables small. See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

**Variational Inference (VI)** — Approximating a hard-to-compute posterior distribution with a simpler one (for example independent Gaussians) and tuning it to be as close as possible by maximizing the *ELBO*. It turns Bayesian inference into optimization, which is faster than *MCMC* but approximate. See: [03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb)

**VC Dimension** — A measure of a model class's capacity: the largest number of points it can label in every possible way (shatter). *Example:* straight lines in 2-D have VC dimension 3. Higher VC dimension means more data is needed to guarantee *generalization*. See: [03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb](03_Machine_Learning/16_learning_theory/01_statistical_learning_theory.ipynb)

**Vector** — An ordered list of numbers, such as [0.2, -1.3, 4.0]. In ML, almost everything (a data row, an *embedding*, a set of weights) is represented as a vector. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**Vector Database** — A database built to store *embeddings* and quickly find the ones most similar to a query embedding. It is the usual "memory" behind *RAG* and *semantic search*. See: [13_Databases/03_vector_db/01_vector_databases.ipynb](13_Databases/03_vector_db/01_vector_databases.ipynb)

**Virtual Environment (venv)** — A private, per-project folder of Python packages, so different projects can use different library versions without clashing. Create one with `python -m venv .venv`. See: [01_Python/notes/01_Python.md](01_Python/notes/01_Python.md)

**Virtual Memory** — The OS gives each process its own large, private address space and maps it in fixed-size pages to physical RAM (or disk). Touching a page that is not in RAM causes a page fault. It is how `mmap` lets you open model files larger than free memory. See: [23_Software_Engineering/06_operating_systems_for_developers.ipynb](23_Software_Engineering/06_operating_systems_for_developers.ipynb)

**Vision Language Model (VLM)** — A model that takes images (and text) as input and answers in text, for example describing a photo, reading a chart or answering questions about a screenshot. See: [08_LLM/06_vision_llm/01_vision_language_models.ipynb](08_LLM/06_vision_llm/01_vision_language_models.ipynb)

**Vision Transformer (ViT)** — A *transformer* applied to images: the image is cut into small square patches, each patch is treated like a token, and self-attention relates the patches to each other. See: [06_Computer_Vision/05_vision_transformers.ipynb](06_Computer_Vision/05_vision_transformers.ipynb)

**Viterbi Algorithm** — A *dynamic-programming* algorithm that finds the single most likely sequence of hidden states in an *HMM* or *CRF*. *Example:* the most likely part-of-speech tags for a sentence, or genes in a DNA sequence. See: [03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb](03_Machine_Learning/17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb)

## W

**WAL (Write-Ahead Logging)** — The rule that a change must be written to a durable log *before* the data pages it modifies are written to disk. After a crash the database replays the log to redo committed work and undo unfinished work. It is the D in *ACID*. See: [13_Databases/00_dbms_fundamentals/06_recovery_and_storage.ipynb](13_Databases/00_dbms_fundamentals/06_recovery_and_storage.ipynb)

**Watermark (Streaming)** — A stream processor's estimate that "all events up to time T have probably arrived". When the watermark passes the end of a window, the window's result is emitted and later events are dropped or handled separately. A longer delay gives more complete results but higher latency. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Web Scraping** — Extracting data from web pages programmatically (for example with BeautifulSoup). Polite scraping checks `robots.txt` and terms of service, rate-limits requests, identifies itself and prefers an official API when one exists. See: [02_Data_Analysis/12_data_acquisition_apis_scraping_and_formats.ipynb](02_Data_Analysis/12_data_acquisition_apis_scraping_and_formats.ipynb)

**WebSocket** — A persistent, two-way connection between browser and server, opened by upgrading an HTTP request. Either side can send messages at any time, which suits chat, live collaboration and voice agents. For one-way token streaming, *SSE* is simpler. See: [23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb](23_Software_Engineering/07_computer_networks_for_ai_apps.ipynb)

**Weight Initialization (Xavier / He)** — Choosing random starting weights with the right scale so signals neither shrink nor blow up as they pass through layers. Xavier (Glorot) suits tanh/sigmoid; He initialization suits *ReLU*. All-zero initialization fails because every neuron learns the same thing. See: [05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb](05_Deep_Learning/18_neural_networks_from_scratch_numpy.ipynb)

**Wilcoxon Signed-Rank Test** — A non-parametric paired test that ranks the differences between two methods (for example across several datasets) instead of assuming they are normally distributed. A common choice for comparing two ML models across many datasets. See: [24_Research_Methods/03_statistical_significance_and_reporting.ipynb](24_Research_Methods/03_statistical_significance_and_reporting.ipynb)

**Windowing (Tumbling / Sliding / Session)** — Grouping an endless stream into finite chunks for aggregation. Tumbling windows are fixed and non-overlapping (every 5 minutes), sliding windows overlap (the last 5 minutes, updated every minute), session windows close after a gap of inactivity. See: [13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb](13_Databases/06_data_engineering/04_stream_processing_from_scratch.ipynb)

**Word Embedding (Word2Vec)** — An *embedding* for a single word, learned from which words appear near each other in lots of text. Word2Vec is a classic method. A famous illustration is that king - man + woman lands close to queen. See: [07_NLP/02_word_embeddings.ipynb](07_NLP/02_word_embeddings.ipynb)

## X

**XAI (Explainable AI)** — Another name for *explainability*: methods and practices that make AI decisions understandable to people. See: [00_AI_Fundamentals/02_transparency_and_explainability.ipynb](00_AI_Fundamentals/02_transparency_and_explainability.ipynb)

**XGBoost** — A fast, widely used *gradient boosting* library for tabular data. It often wins on spreadsheet-style problems. LightGBM and CatBoost are close relatives. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**XSS (Cross-Site Scripting)** — An attack where untrusted text (user input or even LLM output) is inserted into a web page as HTML and runs as JavaScript in another user's browser. Prevented by escaping output (`textContent`, not `innerHTML`) and a Content Security Policy. See: [23_Software_Engineering/08_security_for_ai_applications.ipynb](23_Software_Engineering/08_security_for_ai_applications.ipynb)

## Y

**YOLO (You Only Look Once)** — A family of fast *object detection* models that find all objects in an image in a single pass through the network, fast enough for real-time video. See: [06_Computer_Vision/03_object_detection.ipynb](06_Computer_Vision/03_object_detection.ipynb)

## Z

**Z-Score** — How many standard deviations a value is from the average: z = (value - mean) / standard deviation. A z-score above about 3 (or below -3) is often treated as an outlier. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Zero-Shot** — Asking a model to do a task with no examples, just an instruction ("Classify this review as positive or negative"). Compare *few-shot*. Zero-shot classification also means labeling data with categories the model was never explicitly trained on. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

---

*Can't find a word?* Search the module notes (each module has a `notes/` folder) or the main [README.md](README.md). Terms are explained in more depth, with runnable code, in the linked notebooks.
