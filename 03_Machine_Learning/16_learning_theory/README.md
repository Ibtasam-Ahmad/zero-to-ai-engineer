# Learning Theory & Kernel Methods

This module answers two questions that every serious machine-learning course asks after you can already train models: **why does learning from a limited sample work at all**, and **how can a simple linear method learn curved patterns** by using a similarity function called a *kernel*. An AI developer needs these ideas to reason about how much data is enough, why regularisation works, why huge neural networks still generalise, and what is going on inside SVMs, Gaussian processes and even transformer attention. This is an **optional, university-level (MS/MPhil) module**: it fits **after the core ML stage** (Stage 5 in [`LEARNING_PATH.md`](../../LEARNING_PATH.md)) and is **essential if you are studying for an MS or MPhil** in AI or data science, or preparing for research interviews.

---

## The whole topic explained simply

A model only ever sees a **sample** of the world, for example 1,000 labelled emails out of billions. Learning theory asks: if the model does well on the examples it has seen, how sure can we be that it will do well on new ones? The answer depends on **how many examples** you have and **how flexible** the model family is. Think of a student who memorises last year's exam papers: they score 100% on those papers and can still fail the real exam, because memorising proves nothing about understanding. A very flexible model is like that student; it can "explain" anything, even pure noise, so a perfect training score tells you little. Learning theory gives formulas for the gap between the "practice score" (training error) and the "real exam score" (error on new data), and these formulas shrink as the sample grows and grow as the model becomes more flexible.

The second half is about **kernels**. A kernel is a **similarity score** between two examples that secretly equals a dot product of many hidden features. Think of a music app: it does not need a list of every property of every song, only "how similar is song A to song B". Algorithms that only use similarities (SVMs, ridge regression, PCA, k-means) can then work as if they had thousands or even infinitely many features, without ever building them. Think of trying to separate a ring of red dots around a cluster of blue dots with a straight ruler: impossible on flat paper, but easy if you lift the outer ring into the air (add a "distance from centre" feature) and slide a flat sheet between them. A kernel does that lifting for you.

**Tiny worked example (theory).** You test a finished model on **1,000** held-out examples and measure 90% accuracy. Hoeffding's inequality (a formula for how far an average of many independent 0/1 outcomes can drift from its true value) says that with 95% confidence the true accuracy is within

```
eps = sqrt( ln(2 / 0.05) / (2 * 1000) ) = sqrt( 3.689 / 2000 ) = 0.043
```

so the true accuracy is between about **85.7% and 94.3%**, whatever the data looks like. To get within ±1 point you would need about **18,445** test examples.

**Tiny worked example (kernels).** For $x = (1, 2)$ and $z = (3, 1)$ the dot product is $1 \cdot 3 + 2 \cdot 1 = 5$, and the polynomial kernel gives $k(x, z) = (5 + 1)^2 = 36$. The same 36 is the dot product of two 6-number feature vectors $(x_1^2, x_2^2, \sqrt2 x_1 x_2, \sqrt2 x_1, \sqrt2 x_2, 1)$: $9 + 4 + 12 + 6 + 4 + 1 = 36$. The kernel got the answer with one multiplication, one addition and one square.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | Learners who can already train scikit-learn models and want the *why*; BS/MS/MPhil AI and data-science students; anyone preparing for research or ML-theory interviews |
| **Level** | Optional, university level (MS/MPhil "Advanced Machine Learning" course). Comes **after the core ML stage** (Stage 5) |
| **Prerequisites** | [Supervised learning](../01_supervised/) (especially [linear regression](../01_supervised/01_linear_regression.ipynb) and [SVMs](../01_supervised/05_svm.ipynb)); [model evaluation](../06_model_evaluation/01_model_evaluation.ipynb) (train/validation/test splits); [probability](../../14_Mathematics/03_probability.ipynb) and [statistics](../../14_Mathematics/04_statistics.ipynb); [linear algebra](../../14_Mathematics/01_linear_algebra.ipynb) (eigenvalues, positive semidefinite matrices); [PCA](../02_unsupervised/02_dimensionality_reduction.ipynb) |
| **Strongly related maths notebooks** | [`12_convex_optimization_and_duality`](../../14_Mathematics/12_convex_optimization_and_duality.ipynb) (Lagrangian duality, the SVM dual where kernels first appear, ridge as a norm constraint) and [`10_numerical_linear_algebra`](../../14_Mathematics/10_numerical_linear_algebra.ipynb) (Cholesky solves, eigendecompositions, low-rank approximation, conditioning: the machinery behind kernel ridge regression, kernel PCA and Nyström) |
| **Time needed** | About 3–4 hours per notebook, 6–8 hours in total (plus practice problems) |
| **Runs on** | CPU only, no API key, no internet; each notebook runs in about 1–2 minutes. Uses numpy, pandas, matplotlib, scipy, scikit-learn, plus PyTorch (notebook 01, one small network) and networkx (notebook 02, graph kernels) |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [`01_statistical_learning_theory.ipynb`](01_statistical_learning_theory.ipynb) | Why a model trained on a finite sample works on new data: risk, bias–variance, PAC learning, Hoeffding, VC dimension, Rademacher complexity, margins, double descent and no free lunch | 3–4 h |
| 02 | [`02_kernel_methods.ipynb`](02_kernel_methods.ipynb) | What a kernel is and how to build, scale and apply kernel methods: Mercer's condition, RKHS, representer theorem, kernel ridge regression, kernel PCA/k-means, Nyström, random Fourier features, MMD, Gaussian processes, string/graph kernels and the neural tangent kernel | 3–4 h |

```
 01 Statistical learning theory            02 Kernel methods
 ------------------------------            -----------------------------
 risk, ERM, bias-variance                  feature maps -> kernel trick
 PAC, Hoeffding, VC, Rademacher   ---->    RKHS norm = model complexity
 norms and margins control capacity        representer theorem, KRR, GP
 double descent, memorisation              Nystrom / RFF, MMD, NTK
```

Do notebook 01 first: notebook 02 relies on its ideas of capacity, norms and margins.

---

## The notebooks

### 01 · Statistical Learning Theory

**Explained simply.** We write down exactly what "learning from examples" means: an unknown world (a probability distribution) produces examples; we pick a model from a family (the *hypothesis class*) using only the training sample; we care about the error on *new* data (the *true risk*), but we can only measure the error on the sample (the *empirical risk*). The notebook then shows how to bound the gap between the two using the number of examples and a measure of how flexible the family is. Think of a tailor: a suit cut for one exact pose (too flexible) looks wrong as soon as you move, a one-size-fits-all suit (too rigid) fits nobody, and the best suit is in between. That is the **bias–variance trade-off**, and the notebook derives and measures it.

**Tiny example.** Fitting polynomials to 25 noisy points of a sine wave, averaged over 300 training sets (numbers from the notebook):

| Polynomial degree | bias² | variance | noise σ² | test MSE |
|---|---|---|---|---|
| 0 (a flat line) | 0.498 | 0.024 | 0.09 | 0.61 |
| 3 (the sweet spot) | 0.005 | 0.024 | 0.09 | 0.12 |
| 12 (far too flexible) | 288 | 143,758 | 0.09 | 144,046 |

And a PAC sample-size calculation: with 101 candidate thresholds, target error $\varepsilon = 0.05$ and failure probability $\delta = 0.05$, you need $m \ge (\ln 101 + \ln 20)/0.05 = 152.2$, so **153** examples.

**You will learn:**
- The formal set-up: distribution, hypothesis class, loss, **true risk vs empirical risk**, and **empirical risk minimisation (ERM)**; estimation error vs approximation error
- The **bias–variance decomposition**, derived line by line and checked by simulation
- **PAC learning**, the finite-class bound $m \ge \frac1\varepsilon(\ln|\mathcal H| + \ln\frac1\delta)$, **Hoeffding's inequality** and **uniform convergence**
- **VC dimension** with brute-force shattering demos (intervals, half-planes, rectangles), the growth function, Sauer's lemma and the VC bound
- **Rademacher complexity** for norm-bounded linear models, **regularisation as capacity control**, **structural risk minimisation** and **margin bounds**
- Modern surprises: **double descent**, a network **memorising random labels**, and the **no-free-lunch** theorem, plus what it all means for test-set size and model selection

**Key takeaway:** the generalisation gap shrinks with more data and grows with capacity, and capacity is measured by norms and margins, not by the number of parameters.

### 02 · Kernel Methods

**Explained simply.** A kernel $k(x, z)$ returns one number per pair of examples: how similar they are. A valid kernel always equals a dot product of some feature vectors, so any algorithm written only in terms of dot products can be "kernelised" by swapping $x^\top z$ for $k(x, z)$; this is the **kernel trick**. Not every similarity qualifies: the test is that every table of pairwise similarities (the *Gram matrix*) must be **positive semidefinite** (PSD: no direction in which it "goes negative"). Think of comparing two handwriting samples by overlaying them and measuring the overlap: one number that silently compares thousands of pixel features at once.

**Tiny example.** Is the squared distance $\lVert x - z\rVert^2$ a kernel? Take two points at squared distance 4. The Gram matrix is

```
K = [ 0  4 ]      eigenvalues: +4 and -4
    [ 4  0 ]      a negative eigenvalue -> not PSD -> NOT a kernel
```

whereas the RBF kernel $e^{-\gamma\lVert x - z\rVert^2}$ always gives a PSD Gram matrix. In the notebook, kernel k-means with an RBF kernel separates two concentric rings perfectly (adjusted Rand index 1.000) while ordinary k-means scores about 0.

**You will learn:**
- **Feature maps vs kernels**, **Mercer's condition** (valid kernel iff every Gram matrix is PSD) and the rules for building new kernels from old ones
- The **RKHS** (reproducing kernel Hilbert space, the function space that comes with a kernel) and the **representer theorem**, checked numerically
- **Kernel ridge regression** from scratch, its two hyper-parameters (bandwidth and regularisation), and its exact match with the **Gaussian-process** posterior mean
- **Kernel PCA** and **kernel k-means** from scratch on data that linear methods cannot handle
- Scaling to big data with the **Nyström** method and **random Fourier features**, and the **MMD** kernel two-sample test for data-drift detection
- Kernels for **strings** (spectrum kernel) and **graphs** (Weisfeiler–Lehman), and the **neural tangent kernel** of very wide networks

**Key takeaway:** a kernel lets a linear method work in a huge feature space through similarities alone; the price is an $n \times n$ matrix, which Nyström and random features make affordable.

---

## How this connects to the rest of the repo and to real AI systems

- **Builds on** [`01_supervised/`](../01_supervised/): notebook 01 explains *why* the over- and under-fitting you saw with [linear regression](../01_supervised/01_linear_regression.ipynb) and [decision trees](../01_supervised/03_decision_trees.ipynb) happens; notebook 02 is the theory behind `SVC(kernel="rbf")` in [`05_svm`](../01_supervised/05_svm.ipynb).
- **Maths you will use:** ridge regression as a norm constraint, the SVM dual and the margin come from [`14_Mathematics/12_convex_optimization_and_duality`](../../14_Mathematics/12_convex_optimization_and_duality.ipynb); Cholesky solves, eigendecompositions and low-rank approximations (kernel ridge, kernel PCA, Nyström) come from [`14_Mathematics/10_numerical_linear_algebra`](../../14_Mathematics/10_numerical_linear_algebra.ipynb).
- **Why test sets work:** the Hoeffding bound is the theory behind [`06_model_evaluation`](../06_model_evaluation/01_model_evaluation.ipynb) and the "touch the test set once" rule in [`24_Research_Methods/03_statistical_significance_and_reporting`](../../24_Research_Methods/03_statistical_significance_and_reporting.ipynb).
- **Gaussian processes and Bayesian optimisation:** kernel ridge regression equals the GP posterior mean; GPs drive [`04_uncommon_models/02_industry_gaussian_process_process_optimization`](../04_uncommon_models/02_industry_gaussian_process_process_optimization.ipynb), [hyper-parameter optimisation](../06_model_evaluation/02_hyperparameter_optimization.ipynb) and [`14_Mathematics/07_bayesian_ml`](../../14_Mathematics/07_bayesian_ml.ipynb).
- **Data-drift monitoring:** the MMD test is a drop-in drift detector for [`15_MLOps/06_monitoring`](../../15_MLOps/06_monitoring/01_monitoring.ipynb).
- **Transformers and LLMs:** softmax attention is a kernel smoother, and linear-attention transformers (Performer) use random features ([`05_Deep_Learning/05_transformers_architecture`](../../05_Deep_Learning/05_transformers_architecture.ipynb)); double descent and the failure of parameter counts as capacity are why huge over-parameterised models still generalise.
- **Graph neural networks:** the Weisfeiler–Lehman relabelling is exactly GNN message passing ([`05_Deep_Learning/07_gnn`](../../05_Deep_Learning/07_gnn.ipynb)).
- **Related theory modules:** [conformal prediction](../14_conformal_prediction/01_conformal_prediction.ipynb) (distribution-free guarantees), [active learning](../13_active_learning/01_active_learning.ipynb) (beating passive sample complexity), and next in the track, [probabilistic graphical models](../17_probabilistic_graphical_models/).

---

## Common beginner mistakes

- **Reporting training error as "the accuracy".** The model was chosen to make training error small, so it is an optimistic, biased estimate of the true error.
- **"VC dimension = number of parameters."** True for linear classifiers, false in general: $\operatorname{sign}(\sin(\omega x))$ has one parameter and infinite VC dimension.
- **"Big network, small dataset, so it must overfit."** Class-based bounds give *no guarantee* for such networks, but "no guarantee" is not "must overfit"; the norm of the solution the optimiser actually finds matters.
- **Treating the bounds as exact numbers.** They are worst-case over every possible distribution, so their constants are pessimistic (often above 1, i.e. vacuous). Use their *shape* (how they scale with data and capacity).
- **Comparing many models on one validation set and trusting the winner's score.** Picking the best of $K$ models costs a $\ln K$ term; keep a final test set you touch once.
- **Assuming any symmetric similarity is a kernel.** It must be PSD; the popular "sigmoid kernel" often is not, and a difference of two kernels need not be one.
- **Tuning the MMD bandwidth on the same data you test.** That invalidates the p-value; use the median heuristic or a separate split.
- **Using exact kernel methods on a million rows.** The Gram matrix alone would be 8 TB; switch to Nyström or random Fourier features.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| True risk vs empirical risk? | Expected loss on new data from the distribution vs average loss on the training sample |
| Bias–variance decomposition (squared loss)? | Test MSE = noise σ² + bias² + variance (variance over training sets) |
| What does PAC stand for? | Probably (confidence $1-\delta$) Approximately (error $\le \varepsilon$) Correct |
| Finite-class realisable sample size? | $m \ge \frac1\varepsilon(\ln\lvert\mathcal H\rvert + \ln\frac1\delta)$ |
| Hoeffding for a test set? | $\lvert\hat R - R\rvert \le \sqrt{\ln(2/\delta)/(2n)}$ with probability $\ge 1-\delta$ |
| Define VC dimension. | Size of the largest set of points the class can label in all $2^m$ ways (shatter) |
| VC dimension of half-planes in 2-D? Half-spaces in $\mathbb R^d$? | 3; $d + 1$ |
| Fundamental theorem of statistical learning? | For binary 0–1 loss, PAC learnable iff uniform convergence iff ERM works iff $d_{VC} < \infty$ |
| What is Rademacher complexity? | How well the class can correlate with random ±1 labels on your data |
| Rademacher complexity of $\{w^\top x : \lVert w\rVert \le B\}$? | At most $B\max_i\lVert x_i\rVert/\sqrt m$, independent of dimension |
| What is double descent? | Test error falls, spikes at the interpolation threshold ($p \approx m$), then falls again as capacity keeps growing |
| No-free-lunch theorem? | Averaged over all target functions, every learner has 50% off-training-set accuracy, so inductive bias is unavoidable |
| When is a function a valid kernel? | When it is symmetric and every Gram matrix is positive semidefinite (Mercer) |
| Representer theorem? | The regularised risk minimiser over the RKHS is $\sum_i \alpha_i k(x_i, \cdot)$ |
| Kernel ridge regression solution and cost? | $\alpha = (K + \lambda I)^{-1}y$; $O(n^3)$ time, $O(n^2)$ memory |
| KRR vs GP? | KRR prediction equals the GP posterior mean with $\lambda = \sigma^2$; the GP also gives variance |
| KRR vs SVR? | Same function class; squared loss (closed form, dense) vs $\varepsilon$-insensitive loss (QP, sparse support vectors) |
| Nyström vs random Fourier features? | Nyström uses landmark points (data-dependent, great with fast eigen-decay); RFF samples random frequencies (data-independent, error $O(1/\sqrt D)$) |
| What is the NTK regime? | Very wide networks barely move their weights and behave like kernel regression with a fixed kernel, so they do not learn features |

---

## Further reading

**Classic textbooks**
- S. Shalev-Shwartz and S. Ben-David, *Understanding Machine Learning: From Theory to Algorithms*, Cambridge University Press, 2014 (chapters 2–7 and 26; free PDF on the authors' website).
- M. Mohri, A. Rostamizadeh and A. Talwalkar, *Foundations of Machine Learning*, 2nd ed., MIT Press, 2018 (chapters 2–3 and 6; free online).
- T. Hastie, R. Tibshirani and J. Friedman, *The Elements of Statistical Learning*, 2nd ed., Springer, 2009 (chapter 7; free PDF from the authors).
- B. Schölkopf and A. Smola, *Learning with Kernels*, MIT Press, 2002.
- J. Shawe-Taylor and N. Cristianini, *Kernel Methods for Pattern Analysis*, Cambridge University Press, 2004.
- C. E. Rasmussen and C. K. I. Williams, *Gaussian Processes for Machine Learning*, MIT Press, 2006 (free at gaussianprocess.org).

**Free resources**
- Y. Abu-Mostafa, *Learning From Data*, Caltech CS156 lectures (free video course; the gentlest route to the VC bound).
- F. Bach, *Learning Theory from First Principles*, MIT Press, 2024 (free draft PDF on the author's website).
- The scikit-learn user guide sections on kernel ridge regression, kernel approximation and Gaussian processes.
- Key papers: Belkin et al., "Reconciling modern machine-learning practice and the classical bias–variance trade-off" (PNAS 2019); Zhang et al., "Understanding deep learning requires rethinking generalization" (ICLR 2017); Rahimi and Recht, "Random Features for Large-Scale Kernel Machines" (NeurIPS 2007); Gretton et al., "A Kernel Two-Sample Test" (JMLR 2012); Jacot et al., "Neural Tangent Kernel" (NeurIPS 2018).

For the deeper conceptual study guide with derivations and worked examples, read [`notes/16_learning_theory.md`](notes/16_learning_theory.md).
