# Probabilistic Graphical Models & Approximate Inference

A **probabilistic graphical model (PGM)** is a way to describe many uncertain quantities at once by drawing a graph: one dot per variable, and a line only between variables that *directly* affect each other. An AI developer needs it because the same ideas sit inside named-entity taggers (CRFs), speech and gene finders (HMMs), Wi-Fi and 5G decoders (belief propagation), topic models (LDA), and the training loss of every VAE and diffusion model (the ELBO). This folder is **optional and MS-level**: it covers the core of a university "Probabilistic Graphical Models" or "Advanced ML" course (Stanford CS228, CMU 10-708) and the questions interviewers ask, such as "derive EM" or "what is the ELBO?".

---

## The whole topic explained simply

Real problems contain many uncertain things at once: symptoms and diseases, words and their tags, pixels and the shapes they show. Writing down a probability for *every* combination is hopeless, because just 30 yes/no variables already have more than a billion combinations. A graphical model draws only the direct links, and the **missing** lines are the useful part: they say "these two do not directly matter to each other", so we can store and compute probabilities piece by piece. Think of **gossip in a friendship network**: what you hear depends directly only on your friends, so once you know what all your friends said, the rest of the school tells you nothing new. That shielding set of friends is called a **Markov blanket**. Answering a question such as "how likely is X, given what I saw?" is called **inference**, and on tree-shaped graphs it can be done exactly by passing small "messages" between neighbours, like a **relay of notes along a row of desks**. On big tangled graphs (an image is a grid of millions of pixels) exact inference is impossible, so we approximate. **EM** is "guess, then improve", like sorting mixed red and green apples in dim light: sort, look at what a typical red apple looks like, re-sort, repeat. **Gibbs sampling** makes many random guesses, each depending on the last, and averages them. **Variational inference** replaces a complicated answer with the closest simple one, like describing an oddly shaped city border by its best-fitting circle.

**A tiny worked example (three friends in a row).** Alice, Bob and Charles sit in a line, Alice–Bob–Charles. Each says yes or no. Every pair of neighbours gets a score of **10 if they agree and 1 if they disagree**, and the score of a whole pattern is the product of its two pair scores.

| Pattern (A, B, C) | Pair scores | Score |
|---|---|---|
| yes, yes, yes | 10 × 10 | 100 |
| yes, yes, no | 10 × 1 | 10 |
| yes, no, yes | 1 × 1 | 1 |
| yes, no, no | 1 × 10 | 10 |
| (the four "Alice = no" patterns mirror these) | | 100 + 10 + 1 + 10 |

The total over all 8 patterns is $Z = 2 \times 121 = 242$; this total is called the **partition function**, and dividing by it turns scores into probabilities. So $P(\text{all yes}) = 100/242 \approx 0.41$. If we learn that Alice said yes, only the first four rows remain (total 121), and Charles says yes in rows 1 and 3: $P(\text{Charles yes} \mid \text{Alice yes}) = (100 + 1)/121 \approx 0.83$. Alice influences Charles **through** Bob. But if we learn Bob said yes, Charles agrees with probability $10/11 \approx 0.91$ **whatever Alice said**: Bob is Charles's Markov blanket. That is the whole subject in miniature: scores on local links, a normalising total, and independence read off the graph.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | MS (or strong BS) students taking a PGM / Advanced ML / Bayesian ML course; engineers who use CRFs, HMMs, LDA or VAEs and want to know what is underneath; interview preparation |
| **Must know first** | Bayesian networks, d-separation basics, variable elimination by hand, HMMs: [`classical_ai/09 Uncertain knowledge and reasoning`](../../00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb) |
| | Conditional probability, independence, Bayes' rule, common distributions: [`14_Mathematics/03 Probability`](../../14_Mathematics/03_probability.ipynb) |
| | Priors and posteriors, conjugacy, Metropolis–Hastings: [`14_Mathematics/07 Bayesian ML`](../../14_Mathematics/07_bayesian_ml.ipynb) |
| **Helpful, not required** | Log-likelihood and gradients: [`01_supervised/02 Logistic regression`](../01_supervised/02_logistic_regression.ipynb). Graphs and trees: [`14_Mathematics/discrete_math/03 Graph theory`](../../14_Mathematics/discrete_math/03_graph_theory.ipynb). Using `GaussianMixture`: [`02_unsupervised/01 Clustering`](../02_unsupervised/01_clustering.ipynb) |
| **Time needed** | About 7–8 hours (notebook 01 about 4 h, notebook 02 about 3–4 h); do the derivations on paper |
| **Runs on** | CPU only, no API key, no internet. numpy, scipy, pandas, matplotlib, networkx, scikit-learn, PyTorch (one section). Each notebook runs in 1–2 minutes |
| **Deeper study guide** | [`notes/17_probabilistic_graphical_models.md`](notes/17_probabilistic_graphical_models.md): every concept in order, with formulas, hand-worked examples, complexity tables and a glossary |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Markov Networks and Exact Inference](01_markov_networks_and_exact_inference.ipynb) | Undirected models, reading independence off a graph, variable elimination and treewidth, belief propagation (exact and loopy), Viterbi, a trainable CRF, and learning Bayesian networks from data | about 4 h |
| 02 | [EM, Variational Inference and Sampling](02_em_variational_inference_and_sampling.ipynb) | What to do when variables are hidden or exact inference is too expensive: EM (GMM, missing data, Baum–Welch), Gibbs sampling (including LDA), MCMC diagnostics, mean-field and stochastic VI, and the reparameterisation trick | 3–4 h |

```
classical_ai/09 (Bayes nets, HMMs)  +  14_Mathematics/03, 07 (probability, Bayes)
                    |
                    v
   01 Markov networks & EXACT inference
      graph -> independence -> factors -> variable elimination -> belief propagation
                                                   |                  |
                                                   v                  v
                                            treewidth too big?   Viterbi / CRF
                    |
                    v
   02 APPROXIMATE inference & learning with hidden variables
      EM  ----------------->  Gibbs / MCMC  ----------------->  Variational inference
      (point estimate)        (samples, slow but accurate)      (fast, a bit over-confident)
                                                                      |
                                                                      v
                                                    VAEs, diffusion, Bayesian neural nets
```

---

## The notebooks one by one

### 01 · Markov Networks and Exact Inference

*Explained simply.* A **Bayesian network** draws arrows ("A causes B") and stores a probability table at each node. A **Markov network** (also called a Markov random field, MRF) draws plain lines and stores a "compatibility score" (a **potential**) for each group of linked variables; the scores are not probabilities until you divide by the grand total $Z$. Once the model is written down, you ask questions of it by multiplying small tables and summing variables out (**variable elimination**), or by passing messages between neighbours (**belief propagation**). The cost depends on how "tangled" the graph is (its **treewidth**), not on how many variables it has. Think of a **company phone tree**: if the tree has no loops, every message reaches everyone exactly once and the result is exact; if people also call each other in circles, rumours echo and the answer becomes approximate.

*Tiny example.* Eliminating variables in a good or bad order gives the same answer at very different cost (a star graph with one hub and 12 leaves, from the notebook):

| Elimination order | Largest intermediate table | Table entries touched | Answer $P(L_1)$ |
|---|---|---|---|
| hub first | $2^{13} = 8{,}192$ entries | 106,492 | [0.6426, 0.3574] |
| leaves first | $2 \times 2 = 4$ entries | 92 | [0.6426, 0.3574] |

Same answer, over 1,000 times less work. On a $40 \times 40$ noisy image, loopy belief propagation cuts the pixel error rate from 12.6% to 0.8%.

*You will learn:*
- Markov networks: potentials, the **Gibbs distribution** $P(x) = \frac{1}{Z}\prod_c \phi_c(x_c)$, and why "a potential is not a marginal" (Koller & Friedman's misconception example, $Z = 7{,}201{,}840$)
- **d-separation** as a linear-time "Bayes ball" algorithm, checked against about a thousand numerical independence tests; **Markov blankets**; **I-maps** and perfect maps
- A small `Factor` class (product, marginalise, reduce) and **variable elimination**, reproducing AIMA's $P(\text{Burglary} \mid j, m) = 0.284$; **induced width**, **treewidth**, min-degree and min-fill orders
- **Sum-product belief propagation**, exact on trees and "loopy" on a grid **Ising model** for image denoising; **max-product / Viterbi** for the single most likely explanation
- A **linear-chain CRF** from scratch: forward–backward, the "observed minus expected counts" gradient (checked by finite differences), L-BFGS training on a toy name/place tagging task
- **Learning Bayesian networks**: maximum-likelihood counts, Dirichlet (Laplace) smoothing, and **BIC hill-climbing** for structure, identifiable only up to Markov equivalence

*Key takeaway:* exact inference costs exponential time in the graph's treewidth, not in its size, so chains and trees are easy and grids need approximation.

### 02 · EM, Variational Inference and Sampling

*Explained simply.* Many models have a **latent** (hidden) variable you never observe: which customer group a shopper belongs to, which die a casino is secretly using, which topic a word came from. If you knew the hidden part, fitting the model would be simple counting; if you knew the model, guessing the hidden part would be simple Bayes. **EM** alternates the two. **Gibbs sampling** redraws one unknown at a time given all the others, and the long-run frequencies match the true posterior. **Variational inference (VI)** turns inference into optimisation: pick the best approximation from a simple family by maximising the **ELBO** (evidence lower bound). Think of **two bags of sweets** mixed together: you guess which bag each sweet came from, compute each bag's average weight from those guesses, re-guess, and stop when nothing moves.

*Tiny example.* One EM step by hand (1-D, two clusters, standard deviation 1, equal weights, current means $\mu_1 = 0$, $\mu_2 = 4$):

| point $x$ | responsibility of cluster 1 | responsibility of cluster 2 |
|---|---|---|
| 1 | 0.982 | 0.018 |
| 3 | 0.018 | 0.982 |
| 2 | 0.5 | 0.5 |

New $\mu_1 = (0.982 \cdot 1 + 0.018 \cdot 3 + 0.5 \cdot 2) / (0.982 + 0.018 + 0.5) \approx 1.357$, and by symmetry $\mu_2 \approx 2.643$. The point $x = 2$ is shared half-and-half: this "soft" assignment is what separates EM from k-means.

*You will learn:*
- Why hidden variables make the likelihood a **log of a sum**: no closed form, **label switching**, local optima
- **EM derived** from Jensen's inequality, with a numerical check that $\log p(x) = \text{ELBO} + \text{KL}$; why the likelihood never decreases
- EM from scratch for a **Gaussian mixture** (matches scikit-learn to about $10^{-6}$), for **missing data** (beats deleting rows and mean imputation), and for an **HMM** (Baum–Welch recovers a casino's transition matrix)
- **Gibbs sampling**: a bivariate normal, a Bayesian GMM, and **collapsed Gibbs for LDA** (recovers three planted topics with purity 1.0)
- **MCMC diagnostics** in numpy: trace plots, autocorrelation, **effective sample size (ESS)** and **split-R̂**, checked against exact AR(1) theory
- **Mean-field VI (CAVI)** compared with an exact posterior, **stochastic VI** in PyTorch, the **reparameterisation trick**, and when to choose EM vs VI vs MCMC

*Key takeaway:* EM gives a point estimate, MCMC gives accurate but slow samples, VI gives a fast but over-confident approximation, and the ELBO ties all three together.

---

## How this connects to the rest of the repo and to real AI systems

- **Where it starts:** Bayesian networks, d-separation, first variable elimination, HMM filtering and Viterbi are introduced in [`classical_ai/09`](../../00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb). Metropolis–Hastings and conjugate priors are in [`14_Mathematics/07_bayesian_ml`](../../14_Mathematics/07_bayesian_ml.ipynb). This folder adds undirected models, the cost analysis of exact inference, learning, and the three approximate-inference families.
- **VAEs are variational inference with a neural network.** The VAE loss in [`05_Deep_Learning/20_generative_models_hands_on`](../../05_Deep_Learning/20_generative_models_hands_on.ipynb) is exactly the negative ELBO from notebook 02: a reconstruction term $\mathbb{E}_q[\log p(x \mid z)]$ plus $\mathrm{KL}(q(z \mid x) \,\|\, p(z))$. Two differences from the CAVI of notebook 02: the encoder is **amortised** (one network outputs $q$'s mean and variance for any input $x$, instead of fitting a separate $q$ per data point), and training uses stochastic gradients through the **reparameterisation trick** $z = \mu + \sigma\varepsilon$, whose low variance notebook 02 measures (about 4 per sample versus about 31 for the score-function estimator). The theory version of the same formulas is in [`05_Deep_Learning/06_generative_models`](../../05_Deep_Learning/06_generative_models.ipynb). Diffusion models are also trained on a (re-weighted) variational bound.
- **HMMs in bioinformatics.** [`18_domain_applications/02_bioinformatics_sequence_ml`](../18_domain_applications/02_bioinformatics_sequence_ml.ipynb) finds CpG islands in DNA with a two-state HMM, decoded by Viterbi and forward–backward, with the parameters **given**. Notebook 01 shows that Viterbi is max-product belief propagation on a chain and that the MAP path can differ from the per-position most likely states; notebook 02 shows how to **learn** those parameters from unlabelled sequences with Baum–Welch (EM). Profile HMMs (HMMER) used for protein families are the same model with insert and delete states.
- **CRFs in NLP:** the linear-chain CRF of notebook 01 is the output layer of BiLSTM-CRF and transformer-CRF taggers for named-entity recognition ([`07_NLP/04_named_entity_recognition`](../../07_NLP/04_named_entity_recognition.ipynb)).
- **Topic models:** collapsed Gibbs for LDA in notebook 02 is the algorithm behind the applied version in [`07_NLP/07_topic_modeling`](../../07_NLP/07_topic_modeling.ipynb).
- **Message passing:** graph neural networks are learned, generalised belief propagation ([`05_Deep_Learning/07_gnn`](../../05_Deep_Learning/07_gnn.ipynb)); LDPC decoders in Wi-Fi and 5G run loopy BP; Kalman filters are BP on Gaussian chains.
- **Clustering:** scikit-learn's `GaussianMixture` used in [`02_unsupervised/01_clustering`](../02_unsupervised/01_clustering.ipynb) is the EM algorithm derived here; k-means is its "hard" limit.
- **Causal inference:** a learned Bayesian network is identifiable only up to Markov equivalence, which is why causal claims need the extra assumptions of [`10_causal_inference`](../10_causal_inference/01_causal_inference.ipynb).
- **Probabilistic programming** (Stan, PyMC, NumPyro, Pyro) automates the samplers, diagnostics and VI implemented by hand here.

---

## Common beginner mistakes

- **Treating a potential as a probability.** In a Markov network a potential $\phi(A, B)$ is only a compatibility score; the true $P(A, B)$ depends on every other potential through $Z$.
- **Forgetting the collider rule.** Two independent causes become *dependent* once their common effect (or any descendant of it) is observed ("explaining away").
- **Thinking inference cost grows with the number of variables.** It grows exponentially with the **induced width** of the elimination order: a chain of a million variables is easy, a $30 \times 30$ grid is not.
- **Taking each variable's most likely value and calling it the best joint answer.** The MAP assignment (Viterbi) can differ from the per-position argmax of the marginals; in notebook 01 the two paths have joint probabilities $6.5 \times 10^{-7}$ and $5.2 \times 10^{-7}$.
- **Writing $\log \sum_z p(x, z) = \sum_z \log p(x, z)$.** The log of a sum is not the sum of logs; that one fact is why EM, VI and MCMC exist.
- **Plugging in $\mathbb{E}[x]^2$ for $\mathbb{E}[x^2]$ in the EM E-step for missing data.** You must add the conditional variance, or the covariance comes out too small.
- **Running forward–backward without scaling or logs.** Products of hundreds of probabilities underflow to exactly 0.
- **Trusting VI's error bars, or judging MCMC by its acceptance rate.** Mean-field VI usually underestimates uncertainty; report ESS and R̂ from several chains for MCMC.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| What does a missing edge in a graphical model mean? | A conditional independence: the two variables do not *directly* interact. |
| Bayesian network vs Markov network? | Directed acyclic graph with normalised CPTs ($Z = 1$) vs undirected graph with unnormalised clique potentials and a global $Z$. |
| What is the partition function? | $Z = \sum_x \prod_c \phi_c(x_c)$, the total that normalises a Markov network; #P-hard to compute in general. |
| Hammersley–Clifford theorem? | A strictly positive distribution has the Markov properties of an undirected graph if and only if it factorises over the graph's cliques. |
| Markov blanket in a Bayesian network? | Parents, children and the children's other parents; in a Markov network, just the neighbours. |
| When is a collider path active? | When the collider or one of its descendants is observed. |
| Cost of variable elimination? | $O(n \cdot d^{w+1})$, where $w$ is the induced width of the order; the best possible $w$ is the treewidth. |
| Treewidth of a tree, a $k \times k$ grid, a complete graph on $n$ nodes? | 1, $k$, $n - 1$. |
| When is belief propagation exact? | On trees (two passes, $O(n d^2)$); on loopy graphs it is approximate and its fixed points are stationary points of the Bethe free energy. |
| What is Viterbi in PGM terms? | Max-product (max-sum in logs) belief propagation on a chain, $O(T S^2)$. |
| HMM vs CRF? | HMM is generative, $P(x, y)$; a linear-chain CRF is discriminative, $P(y \mid x)$, so it can use rich overlapping features of the input. |
| CRF log-likelihood gradient? | Observed feature counts minus expected feature counts (from forward–backward); the objective is concave. |
| Derive EM in two lines. | Jensen gives $\log p(x) \ge \mathcal{L}(q, \theta)$ and $\log p(x) = \mathcal{L} + \mathrm{KL}(q \,\|\, p(z \mid x))$; E-step sets $q$ to the posterior, M-step maximises $\mathbb{E}_q[\log p(x, z \mid \theta)]$. |
| Why is k-means "hard EM"? | It is EM for a GMM with shared covariance $\sigma^2 I$ as $\sigma \to 0$: responsibilities become 0 or 1. |
| Why is Gibbs sampling a special case of Metropolis–Hastings? | Its proposal is the full conditional, so the acceptance probability is exactly 1. |
| What does ESS measure? | How many independent draws your correlated chain is worth: $N / (1 + 2\sum_k \rho_k)$. |
| KL(q‖p) vs KL(p‖q)? | KL(q‖p) (standard VI) is mode-seeking and over-confident; KL(p‖q) (expectation propagation) is mass-covering. |
| Why use the reparameterisation trick? | It moves randomness into $\varepsilon$ so gradients flow through $z = \mu + \sigma\varepsilon$, with much lower variance than the score-function estimator. |

---

## Further reading

- D. Koller and N. Friedman, *Probabilistic Graphical Models: Principles and Techniques*, MIT Press, 2009. The standard graduate text (representation, exact and approximate inference, learning).
- C. M. Bishop, *Pattern Recognition and Machine Learning*, Springer, 2006: ch. 8 (graphical models), 9 (mixtures and EM), 10 (variational inference), 11 (sampling), 13 (HMMs). Free PDF from Microsoft Research.
- K. P. Murphy, *Probabilistic Machine Learning: An Introduction* (2022) and *Advanced Topics* (2023). Free at probml.github.io.
- D. J. C. MacKay, *Information Theory, Inference, and Learning Algorithms*, Cambridge, 2003. Free online; excellent on message passing and Monte Carlo.
- M. J. Wainwright and M. I. Jordan, "Graphical Models, Exponential Families, and Variational Inference", *Foundations and Trends in ML*, 2008.
- D. M. Blei, A. Kucukelbir and J. D. McAuliffe, "Variational Inference: A Review for Statisticians", *JASA*, 2017.
- C. Sutton and A. McCallum, "An Introduction to Conditional Random Fields", 2012 (free on arXiv).
- Free courses: Stanford CS228 notes (ermongroup.github.io/cs228-notes) and CMU 10-708 lecture videos and notes.
