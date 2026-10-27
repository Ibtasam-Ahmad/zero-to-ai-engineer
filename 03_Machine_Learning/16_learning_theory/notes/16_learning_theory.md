# Learning Theory & Kernel Methods

Most of machine learning is practical: load data, fit a model, check a validation score. This guide covers the two theoretical pillars that sit underneath that practice. **Statistical learning theory** explains why a model fitted to a finite sample can be trusted on new data, and how that trust depends on the amount of data and the flexibility of the model. **Kernel methods** show how a linear algorithm can learn curved patterns by working with a similarity function instead of explicit features, and they turn out to describe everything from SVMs and Gaussian processes to very wide neural networks. This is MS/MPhil-level material; it follows the two notebooks in this folder ([`01_statistical_learning_theory`](../01_statistical_learning_theory.ipynb) and [`02_kernel_methods`](../02_kernel_methods.ipynb)) in order.

```
  PART A: why learning works                PART B: kernels
  --------------------------                ---------------
  1 set-up: risk, ERM                       9  feature maps, kernel trick, Mercer
  2 bias-variance                           10 RKHS and the representer theorem
  3 PAC learning (finite class)             11 kernel ridge regression = GP mean
  4 Hoeffding, uniform convergence          12 kernel PCA, kernel k-means
  5 VC dimension                            13 Nystrom, random Fourier features
  6 Rademacher complexity                   14 MMD two-sample test
  7 regularisation, SRM, margins            15 string and graph kernels
  8 double descent, memorisation, NFL       16 neural tangent kernel
```

---

# Part A: Statistical Learning Theory

## 1. The learning set-up: risk, empirical risk and ERM

To prove anything about learning we first need precise words.

- **Distribution $\mathcal D$**: the unknown process that produces examples $(x, y)$. For a spam filter, "all emails in the world, with their true spam/not-spam label".
- **Training sample $S = \{(x_i, y_i)\}_{i=1}^m$**: $m$ examples drawn **i.i.d.** (independent and identically distributed) from $\mathcal D$. The i.i.d. assumption is the foundation of everything in Part A.
- **Hypothesis class $\mathcal H$**: the set of models we allow, for example "all thresholds on one feature", "all linear classifiers", "all trees of depth 5".
- **Loss $\ell(h(x), y)$**: how wrong a prediction is. The **0–1 loss** is $\mathbb 1[h(x) \ne y]$ (1 if wrong, 0 if right); the **squared loss** is $(h(x) - y)^2$.
- **True risk** $R(h) = \mathbb E_{(x,y)\sim\mathcal D}[\ell(h(x), y)]$: the expected loss on new data. This is what we care about; it is also called the **generalisation error**.
- **Empirical risk** $\hat R_S(h) = \frac1m\sum_i \ell(h(x_i), y_i)$: the average loss on the training sample. This is what we can measure.

**Empirical risk minimisation (ERM)** picks the hypothesis with the lowest training error: $\hat h = \arg\min_{h \in \mathcal H}\hat R_S(h)$. Write $h^\star$ for the best hypothesis *in the class* and $R^\star$ for the **Bayes risk**, the lowest error achievable by any function at all (it is above zero when labels are noisy). The excess error of ERM splits into two parts:

$$R(\hat h) - R^\star = \underbrace{R(\hat h) - R(h^\star)}_{\text{estimation error}} + \underbrace{R(h^\star) - R^\star}_{\text{approximation error}}.$$

- **Estimation error** comes from having only a sample; it shrinks as $m$ grows and grows with the richness of $\mathcal H$.
- **Approximation error** comes from the class being too limited; it shrinks as $\mathcal H$ gets richer.

This is the abstract version of the trade-off you have met as under- and over-fitting.

**Worked example (fully known world).** Let $x \sim \text{Uniform}(0, 1)$, true label $y = \mathbb 1[x \ge 0.3]$, flipped with probability $\eta = 0.1$. Use thresholds $h_t(x) = \mathbb 1[x \ge t]$. The threshold $h_t$ disagrees with the clean rule on an interval of length $|t - 0.3|$, where it is wrong with probability $1 - \eta$; elsewhere it is wrong with probability $\eta$. So

$$R(h_t) = \eta(1 - |t - 0.3|) + (1 - \eta)|t - 0.3| = \eta + (1 - 2\eta)|t - 0.3|.$$

At $t = 0.5$: $R = 0.1 + 0.8 \times 0.2 = 0.26$. At $t = 0.3$: $R = 0.1$, the Bayes risk. In the notebook, ERM on 50 points found $\hat t = 0.300$ with training error 0.08 and true error 0.10: the training error is *lower* than the truth, because the threshold was chosen to fit that sample.

**Why it matters:** the training error of the chosen model is a biased, optimistic estimate. Everything that follows is about bounding that optimism.

## 2. The bias–variance decomposition

For regression with squared loss, write $y = f(x) + \varepsilon$ with noise mean 0 and variance $\sigma^2$. A learning algorithm trained on a random sample $S$ gives $\hat f_S$. Fix a test input $x$ and define the **average model** $\bar f(x) = \mathbb E_S[\hat f_S(x)]$ (the prediction you would get by averaging over infinitely many training sets). Then

$$\mathbb E\big[(y - \hat f_S(x))^2\big] = \underbrace{\sigma^2}_{\text{noise}} + \underbrace{\big(f(x) - \bar f(x)\big)^2}_{\text{bias}^2} + \underbrace{\mathbb E_S\big[(\hat f_S(x) - \bar f(x))^2\big]}_{\text{variance}}.$$

**Derivation in three steps.** (1) Substitute $y = f + \varepsilon$; the noise is independent of $S$ with mean 0, so it contributes $\sigma^2$ and no cross term. (2) Add and subtract $\bar f(x)$ inside the remaining square. (3) The cross term $2(f - \bar f)\,\mathbb E_S[\bar f - \hat f_S]$ is zero because $\mathbb E_S[\hat f_S] = \bar f$ by definition.

- **Bias** is how far the *average* model is from the truth: a model family too stiff to bend like the truth.
- **Variance** is how much the model jumps around between different training sets: a model family so flexible it chases each sample's noise.
- **Noise** is the floor: no model can do better than $\sigma^2$.

**Numbers from the notebook** ($f(x) = \sin 2\pi x$, $\sigma = 0.3$, 25 points, 300 training sets):

| Degree | bias² | variance | noise | sum | measured test MSE |
|---|---|---|---|---|---|
| 0 | 0.498 | 0.024 | 0.09 | 0.612 | 0.610 |
| 1 | 0.200 | 0.025 | 0.09 | 0.315 | 0.313 |
| 3 | 0.005 | 0.024 | 0.09 | 0.120 | 0.119 |
| 12 | 288 | 143,758 | 0.09 | 144,046 | 144,046 |

The sum matches the measured error, confirming the identity. The best degree (3) balances the two error sources. At degree 12 the 25-point fits swing so wildly between training sets that variance dominates everything (even the averaged fit is distorted by a few extreme fits).

**Exam notes.** The decomposition is exact only for squared loss; for 0–1 loss there are several competing definitions and bias and variance interact. "Variance" here means variance *over training sets*, not the spread of predictions over test inputs. In practice you cannot draw 300 independent training sets, so the bootstrap is used to approximate these quantities.

## 3. PAC learning with a finite hypothesis class

**PAC** stands for **Probably Approximately Correct**. A class $\mathcal H$ is PAC learnable if there is an algorithm and a sample size $m_{\mathcal H}(\varepsilon, \delta)$ such that, for every distribution and every $\varepsilon, \delta \in (0, 1)$, with $m \ge m_{\mathcal H}(\varepsilon, \delta)$ examples:

$$\Pr_S\big[R(\hat h) \le \varepsilon\big] \ge 1 - \delta.$$

$\varepsilon$ is the **accuracy** parameter ("approximately correct"), $\delta$ the **confidence** parameter ("probably").

**Theorem (finite class, realisable case).** If $\mathcal H$ is finite and contains a perfect hypothesis (the **realisable** case), any ERM learner is PAC with

$$m \ge \frac{1}{\varepsilon}\Big(\ln|\mathcal H| + \ln\frac1\delta\Big).$$

**Proof sketch.**
1. A fixed "bad" hypothesis ($R(h) > \varepsilon$) gets all $m$ i.i.d. examples right with probability $< (1 - \varepsilon)^m \le e^{-\varepsilon m}$.
2. **Union bound** (the probability that at least one of several events happens is at most the sum of their probabilities) over at most $|\mathcal H|$ bad hypotheses: $\Pr[\text{some bad } h \text{ looks perfect}] < |\mathcal H|e^{-\varepsilon m}$.
3. Set this $\le \delta$ and solve for $m$.

**Agnostic case** (no perfect hypothesis, e.g. noisy labels): $m \ge \frac{\ln(2|\mathcal H|/\delta)}{2\varepsilon^2}$ guarantees that **every** hypothesis has $|\hat R_S(h) - R(h)| \le \varepsilon$. The dependence becomes $1/\varepsilon^2$ instead of $1/\varepsilon$: noise makes learning quadratically harder.

**Worked examples by hand.**
- 101 thresholds, $\varepsilon = \delta = 0.05$: $(\ln 101 + \ln 20)/0.05 = (4.615 + 2.996)/0.05 = 152.2$, so **153** examples. Agnostic version: $\ln(2 \cdot 101/0.05)/(2 \cdot 0.0025) = \ln 4040 / 0.005 = 8.304/0.005 = 1{,}661$.
- $|\mathcal H| = 2^{20}$, $\varepsilon = \delta = 0.01$: $100 \times (13.863 + 4.605) = 1{,}846.8$, so **1,847**.

**Why it matters:** the bound depends only on $\ln|\mathcal H|$. Doubling the class costs only $\ln 2/\varepsilon$ extra examples, and a class of $2^{64}$ rules (anything describable in 64 bits) has $\ln|\mathcal H| \approx 44$. Description length is a measure of capacity. In the notebook the observed failure rate was always far below the bound: union-bound arguments are worst-case and conservative.

## 4. Concentration: Hoeffding's inequality and uniform convergence

**Hoeffding's inequality.** If $Z_1, \dots, Z_m$ are independent, each in $[a, b]$, with mean $\bar Z$, then

$$\Pr\big[|\bar Z - \mathbb E\bar Z| \ge \varepsilon\big] \le 2\exp\Big(-\frac{2m\varepsilon^2}{(b - a)^2}\Big).$$

For 0–1 loss on a **fixed** hypothesis, $Z_i \in [0, 1]$, so its training error is within $\varepsilon$ of its true error except with probability $2e^{-2m\varepsilon^2}$.

**Worked example (test-set size).** Solve $2e^{-2n\varepsilon^2} = \delta$ for $n$: $n = \ln(2/\delta)/(2\varepsilon^2)$.

| Goal | Calculation | Test examples |
|---|---|---|
| ±1 point at 95% | $\ln 40 / (2 \times 0.0001) = 3.689/0.0002$ | 18,445 |
| ±4.3 points at 95% | $\ln 40 / (2 \times 0.043^2)$ | about 1,000 |

Hoeffding ignores the variance of the $Z_i$; when error rates are far from 0.5 it is loose, and **Bernstein's inequality**, which uses the variance, is tighter.

**Uniform convergence.** ERM does not use a fixed $h$; it picks $h$ *after* seeing the data. So we need **all** training errors to be close to their true values at once:

$$\sup_{h \in \mathcal H}|\hat R_S(h) - R(h)| \le \varepsilon \quad\Rightarrow\quad R(\hat h) \le R(h^\star) + 2\varepsilon.$$

(The training error of $\hat h$ is at most that of $h^\star$, and each is within $\varepsilon$ of its true value.) For a finite class, Hoeffding plus the union bound gives exactly the agnostic bound of Section 3. In the notebook, the worst deviation over all 1,001 thresholds was about 2.2–2.6 times a single threshold's deviation but still shrank at the $1/\sqrt m$ rate: infinitely many thresholds behave like a small class. Section 5 explains why.

## 5. VC dimension, the growth function and the VC bound

$\ln|\mathcal H|$ is infinite for classes like "all lines in the plane", yet such classes are clearly learnable. Vapnik and Chervonenkis replaced the *number of hypotheses* by the *number of different labellings* the class can produce on $m$ points.

- **Shattering:** $\mathcal H$ shatters a set $C$ of $m$ points if it can produce all $2^m$ labellings of $C$.
- **VC dimension** $d_{VC}(\mathcal H)$: the size of the **largest** set that $\mathcal H$ shatters. To prove $d_{VC} = d$ you must show (1) *some* set of $d$ points is shattered and (2) *no* set of $d + 1$ points is.
- **Growth function** $\Pi_{\mathcal H}(m)$: the maximum number of labellings on any $m$ points.
- **Sauer–Shelah lemma:** if $d_{VC} = d$ then $\Pi_{\mathcal H}(m) \le \sum_{i=0}^{d}\binom mi \le (em/d)^d$, a **polynomial** in $m$ rather than $2^m$. This is what makes infinite classes learnable.

| Class | $d_{VC}$ | The labelling that fails on $d+1$ points |
|---|---|---|
| thresholds $\mathbb 1[x \ge t]$ | 1 | $(+, -)$ for $x_1 < x_2$ |
| intervals $\mathbb 1[a \le x \le b]$ | 2 | $(+, -, +)$ |
| half-planes in $\mathbb R^2$ | 3 | XOR on 4 points, or one point inside the triangle of the others |
| half-spaces in $\mathbb R^d$ | $d + 1$ | Radon's theorem |
| axis-aligned rectangles in $\mathbb R^2$ | 4 | extreme points $+$, the remaining point $-$ |
| $\operatorname{sign}(\sin(\omega x))$ | $\infty$ | none: one parameter, infinite capacity |

**Worked example by hand (intervals).** Two points $x_1 < x_2$: $(-,-)$ use an empty interval; $(+,-)$ an interval around $x_1$ only; $(-,+)$ around $x_2$ only; $(+,+)$ one covering both. All 4 labellings, so 2 points are shattered. Three points: any interval containing $x_1$ and $x_3$ contains $x_2$, so $(+,-,+)$ is impossible. Hence $d_{VC} = 2$. Counting labellings on $m$ points gives $\binom{m+1}{2} + 1$ (choose the first and last positive point, plus the all-negative case): for $m = 3$, $6 + 1 = 7 < 8$. For half-planes on $m$ points in general position, **Cover's theorem** gives $m^2 - m + 2$: at $m = 8$, 58 of the 256 labellings.

**The VC bound** (in the form used in *Learning From Data*): with probability at least $1 - \delta$, for all $h \in \mathcal H$,

$$R(h) \le \hat R_S(h) + \sqrt{\frac{8}{m}\ln\frac{4\,\Pi_{\mathcal H}(2m)}{\delta}}, \qquad \Pi_{\mathcal H}(2m) \le (2m)^{d_{VC}} + 1.$$

Solving "gap $\le 0.1$ with $\delta = 0.1$" by fixed-point iteration gives about 10,947 examples for $d_{VC} = 1$ and 29,300 for $d_{VC} = 3$, roughly 10,000 per unit of VC dimension. The practitioner's rule of thumb "$m \approx 10 \times d_{VC}$" is far smaller and works because the bound is worst-case over all distributions.

**The fundamental theorem of statistical learning.** For binary classification with 0–1 loss, these are equivalent: (1) $\mathcal H$ has uniform convergence; (2) ERM is a PAC learner for $\mathcal H$; (3) $\mathcal H$ is PAC learnable; (4) $d_{VC}(\mathcal H) < \infty$. The sample complexity is $\Theta\big((d + \ln\frac1\delta)/\varepsilon\big)$ in the realisable case and $\Theta\big((d + \ln\frac1\delta)/\varepsilon^2\big)$ in the agnostic case. The VC dimension therefore *exactly characterises* binary learnability.

**Common confusion:** VC dimension is not the parameter count. It happens to match for linear classifiers ($d + 1$ parameters and VC dimension $d + 1$), but not in general; for ReLU networks with $W$ weights and $L$ layers it is $\Theta(WL\log W)$ (Bartlett et al., 2019).

## 6. Rademacher complexity

The VC dimension is a property of the class alone and only works for binary classifiers. **Rademacher complexity** measures capacity *on your data* and works for real-valued functions. Draw **Rademacher variables** $\sigma_1, \dots, \sigma_m$, each $+1$ or $-1$ with probability ½ (random coin-flip labels), and ask how well the best function in the class can correlate with them:

$$\hat{\mathfrak R}_S(\mathcal F) = \mathbb E_\sigma\Big[\sup_{f \in \mathcal F}\frac1m\sum_{i=1}^m \sigma_i f(x_i)\Big].$$

A class that can fit any random labelling has complexity near 1 (for ±1-valued functions); a class that can barely fit noise has complexity near 0.

**Generalisation bound** (Mohri et al., Theorem 3.3, losses in $[0,1]$): with probability $\ge 1 - \delta$, for all $f$,

$$R(f) \le \hat R_S(f) + 2\hat{\mathfrak R}_S(\ell \circ \mathcal F) + 3\sqrt{\frac{\ln(2/\delta)}{2m}}.$$

**Worked example by hand.** Thresholds as ±1 classifiers on $m = 2$ sorted points can produce three behaviours: $(+,+)$, $(-,+)$, $(-,-)$. Go through the four equally likely $\sigma$ vectors and take the best correlation $\frac12(\sigma_1 h_1 + \sigma_2 h_2)$:

| $\sigma$ | best behaviour | best correlation |
|---|---|---|
| $(+,+)$ | $(+,+)$ | 1 |
| $(+,-)$ | $(+,+)$ or $(-,-)$ | 0 |
| $(-,+)$ | $(-,+)$ | 1 |
| $(-,-)$ | $(-,-)$ | 1 |

Average: $\hat{\mathfrak R}_S = 3/4 = 0.75$. Thresholds miss only the labelling $(+,-)$. **Massart's lemma** gives the upper bound $\sqrt{2\ln N/m}$ for a class with $N$ behaviours: here $\sqrt{2\ln 3/2} = 1.05$, valid but loose.

**Norm-bounded linear models.** For $\mathcal F_B = \{x \mapsto w^\top x : \lVert w\rVert_2 \le B\}$, Cauchy–Schwarz gives the supremum exactly: $\sup_{\lVert w\rVert \le B} w^\top v = B\lVert v\rVert$ with $v = \frac1m\sum_i\sigma_i x_i$. Hence

$$\hat{\mathfrak R}_S(\mathcal F_B) = \frac Bm\,\mathbb E_\sigma\Big\lVert\sum_i\sigma_i x_i\Big\rVert \le \frac{B\max_i\lVert x_i\rVert}{\sqrt m}.$$

The complexity is **linear in the weight norm $B$**, shrinks like $1/\sqrt m$, and **does not depend on the input dimension**. In the notebook, doubling $B$ exactly doubled the estimate, and going from $m = 20$ to $m = 2000$ cut it by about 10.

**Why it matters:** this is the theoretical reason weight decay works in high dimensions. Keeping $\lVert w\rVert$ small keeps capacity small regardless of how many features you have.

## 7. Regularisation, structural risk minimisation and margins

**Regularisation as capacity control.** Ridge regression minimises $\lVert Xw - y\rVert^2 + \lambda\lVert w\rVert^2$. By Lagrangian duality (see [`14_Mathematics/12_convex_optimization_and_duality`](../../../14_Mathematics/12_convex_optimization_and_duality.ipynb)) this is equivalent to minimising the squared error subject to $\lVert w\rVert \le B(\lambda)$, so a larger $\lambda$ means a smaller $B$ and smaller Rademacher complexity. A related measure is the **effective degrees of freedom**

$$\mathrm{df}(\lambda) = \sum_j \frac{s_j^2}{s_j^2 + \lambda},$$

where $s_j$ are the singular values of $X$ (see [`14_Mathematics/10_numerical_linear_algebra`](../../../14_Mathematics/10_numerical_linear_algebra.ipynb)). It falls smoothly from the number of features at $\lambda = 0$ to 0 as $\lambda \to \infty$. For one feature with $s^2 = 4$ and $\lambda = 4$, $\mathrm{df} = 0.5$: half a parameter's worth of freedom. In the notebook a degree-12 polynomial on 25 points went from a test MSE of about 88,000 ($\lambda = 0$) to about 0.14 ($\lambda = 1$): **capacity is controlled by the norm, not just by the number of parameters**.

**Structural risk minimisation (SRM).** Choose a nested sequence $\mathcal H_1 \subset \mathcal H_2 \subset \cdots$ and minimise *training error + complexity penalty* over the index $k$, not training error alone. To make the guarantee hold for all $k$ at once, give class $k$ confidence $\delta_k = \delta/(k(k+1))$, which sums to at most $\delta$. In the notebook's "constant on $k$ bins" example (Bayes risk 0.2454):

| Selection rule | chosen $k$ | true risk |
|---|---|---|
| oracle (best in hindsight) | 3 | 0.2454 |
| SRM with VC penalty | 1 | 0.4151 (far too simple) |
| SRM with Rademacher penalty | 3 | 0.2454 |
| validation set | 31 | 0.2514 |
| training error alone | 39 | 0.2528 |

Lessons: worst-case VC penalties are too conservative; data-dependent penalties can be sharp; validation is a strong default.

**Margin bounds.** For linear classifiers that separate data lying inside a ball of radius $R$ with **margin** $\gamma$ (the distance from the boundary to the nearest point), the VC dimension is at most $\min(d, R^2/\gamma^2) + 1$. Capacity depends on the **margin, not on the dimension**. In the notebook, 200 points in 500 dimensions had plain VC dimension 501 (a useless bound) but $R^2/\gamma^2 \approx 32.5$. This is the justification for SVMs ([`05_svm`](../../01_supervised/05_svm.ipynb)) and for kernels, which work in huge or infinite dimensions. A separate bound: the expected leave-one-out error of an SVM is at most $\mathbb E[\#\text{support vectors}]/m$.

## 8. Modern phenomena: double descent, memorisation, no free lunch

**Double descent** (Belkin et al., 2019). The classical picture is a U-shaped test-error curve against capacity. If you keep adding capacity *past the interpolation threshold* (where the model can fit the training data exactly), test error can fall again. In the notebook (random ReLU features, $m = 50$ training points, minimum-norm least squares):

| features $p$ | 20 | 45 | 50 | 55 | 100 | 1000 |
|---|---|---|---|---|---|---|
| test MSE | 0.67 | 2.26 | 58.0 | 1.63 | 0.43 | 0.26 |

At $p = m$ there is exactly one interpolating solution and fitting the noise forces a huge weight norm. With $p \gg m$ there are many interpolating solutions, and the **minimum-norm** one (which gradient descent from zero converges to) is smooth. Parameter count is the wrong capacity measure; the norm of the solution actually found is the right one.

**Memorising random labels** (Zhang et al., 2017). Standard networks reach 100% training accuracy on CIFAR-10 even with random labels. The notebook reproduces this in miniature: a two-hidden-layer MLP on 500 digit images reached 100% training accuracy with both true and random labels, with test accuracy 0.954 (true) vs 0.128 (random; chance is 0.1). Any bound that depends only on the class must therefore be **vacuous** for this network. Explaining deep-learning generalisation needs *algorithm- and data-dependent* quantities: norms, margins, flatness, compression and PAC-Bayes bounds.

**No free lunch** (Wolpert, 1996). Averaged over *all* possible target functions, every learner has the same off-training-set accuracy, 50% for binary labels. The notebook checks this by brute force over all $2^8 = 256$ Boolean functions on 3 bits: majority vote, 1-nearest-neighbour and a deliberately silly "anti-majority" all score exactly 0.5000 on unseen inputs. Learning beyond chance requires an **inductive bias** (assumptions such as smoothness or locality) that matches the real world; CNNs and transformers are carefully chosen inductive biases.

## Consequences for practice

| Question | Formula | Example |
|---|---|---|
| test-set size for ±$\varepsilon$ at confidence $1-\delta$ | $n \ge \ln(2/\delta)/(2\varepsilon^2)$ | $\varepsilon = 0.01$, $\delta = 0.05$: 18,445 |
| best of $K$ models on one validation set | replace $\ln(2/\delta)$ by $\ln(2K/\delta)$ | $n = 1000$: ±4.3 points for 1 model, ±6.4 for best of 100 |
| training size, finite class, realisable | $m \ge \frac1\varepsilon(\ln\lvert\mathcal H\rvert + \ln\frac1\delta)$ | $2^{20}$ rules, $\varepsilon = \delta = 0.01$: 1,847 |
| training size, VC class (rule of thumb) | $m \approx 10\,d_{VC}$ | linear model in 50-D: about 500 |

**Limits of the bounds:** they are worst-case over all distributions (loose for yours); class-based bounds ignore the optimiser's implicit bias; and they all assume i.i.d. data, so **distribution shift** breaks them (monitor drift, see [`15_MLOps/06_monitoring`](../../../15_MLOps/06_monitoring/01_monitoring.ipynb)). Their **shapes** are what you keep: error falls like $1/\sqrt m$ (agnostic) or $1/m$ (realisable), norms and margins measure capacity, and model selection on one validation set costs $\ln K$.

---

# Part B: Kernel Methods

## 9. Feature maps, the kernel trick and Mercer's condition

A **feature map** $\phi$ sends each input to a (possibly huge) feature vector. A **kernel** returns the inner product of two feature vectors directly:

$$k(x, z) = \langle\phi(x), \phi(z)\rangle.$$

The **Gram matrix** of points $x_1, \dots, x_n$ is the $n \times n$ table $K_{ij} = k(x_i, x_j)$. Any algorithm that touches the data only through inner products (the SVM dual, ridge regression, PCA, k-means, distances) can be **kernelised** by replacing $x^\top z$ with $k(x, z)$. This is the **kernel trick**.

| Kernel | Formula | Feature space |
|---|---|---|
| linear | $x^\top z$ | the inputs themselves |
| polynomial | $(x^\top z + c)^p$ | all monomials up to degree $p$: $\binom{d+p}{p}$ dimensions |
| RBF (Gaussian) | $\exp(-\gamma\lVert x - z\rVert^2)$ | infinite-dimensional |
| Laplacian | $\exp(-\gamma\lVert x - z\rVert_1)$ | infinite-dimensional, rougher functions |

**Worked example by hand.** For 2-D inputs, $(x^\top z + 1)^2$ has the explicit map $\phi(x) = (x_1^2, x_2^2, \sqrt2 x_1x_2, \sqrt2 x_1, \sqrt2 x_2, 1)$. With $x = (1,2)$ and $z = (3,1)$: kernel $= (3 + 2 + 1)^2 = 36$; features $\phi(x) = (1, 4, 2.83, 1.41, 2.83, 1)$ and $\phi(z) = (9, 1, 4.24, 4.24, 1.41, 1)$, whose dot product is $9 + 4 + 12 + 6 + 4 + 1 = 36$. With $d = 100$ inputs and degree $p = 3$ the explicit map would have $\binom{103}{3} = 176{,}851$ features; the kernel still costs one dot product. The RBF kernel's feature space is infinite: in 1-D, $e^{-(x-z)^2/2} = e^{-x^2/2}e^{-z^2/2}\sum_{n \ge 0}\frac{(xz)^n}{n!}$, an infinite sum of feature products (the notebook shows truncations converging).

**Mercer / Moore–Aronszajn theorem.** A symmetric function $k$ is a valid kernel (equals $\langle\phi(x), \phi(z)\rangle$ for *some* feature map) **if and only if** every Gram matrix it produces is **positive semidefinite (PSD)**: $c^\top Kc \ge 0$ for every vector $c$, equivalently all eigenvalues $\ge 0$. One Gram matrix with a negative eigenvalue proves a function is not a kernel.

**Worked counter-example.** $k(x, z) = \lVert x - z\rVert^2$ on two points at squared distance 4 gives $K = \begin{pmatrix}0 & 4\\ 4 & 0\end{pmatrix}$ with eigenvalues $\pm 4$. Not PSD. In general its Gram matrix has zero trace (sum of eigenvalues) but is not the zero matrix, so some eigenvalue is negative. The "sigmoid kernel" $\tanh(a\,x^\top z + c)$ offered by libraries is also not PSD for many parameter values.

**Building kernels from kernels.** If $k_1$ and $k_2$ are kernels, so are: $ak_1$ ($a \ge 0$), $k_1 + k_2$, $k_1 k_2$, $f(x)k_1(x,z)f(z)$ for any function $f$, $p(k_1)$ for a polynomial with non-negative coefficients, $\exp(k_1)$, and $k_1(\psi(x), \psi(z))$ for any map $\psi$. A **difference** $k_1 - k_2$ is not guaranteed to be a kernel. The RBF kernel itself is $f(x)\exp(2\gamma x^\top z)f(z)$ with $f(x) = e^{-\gamma\lVert x\rVert^2}$.

**Why it matters:** an invalid "kernel" can make the SVM dual non-convex, so solvers fail or return nonsense. Symmetry and "bigger for similar items" are not enough.

## 10. The RKHS and the representer theorem

Every valid kernel comes with its own space of functions, the **reproducing kernel Hilbert space (RKHS)** $\mathcal H_k$. Build it from "bumps" $k(x_i, \cdot)$ centred at points: take all functions $f = \sum_i\alpha_i k(x_i, \cdot)$ and their limits, with inner product $\langle k(x, \cdot), k(z, \cdot)\rangle_{\mathcal H} = k(x, z)$.

- **Reproducing property:** $f(x) = \langle f, k(x, \cdot)\rangle_{\mathcal H}$. Evaluating a function is an inner product with a bump.
- **Norm = complexity:** for $f = \sum_i\alpha_i k(x_i, \cdot)$, $\lVert f\rVert^2_{\mathcal H} = \alpha^\top K\alpha$. For the RBF kernel a small norm means a smooth function. Penalising $\lVert f\rVert_{\mathcal H}$ is the kernel version of weight decay, and it is exactly the norm that appears in the Rademacher and margin bounds of Part A.

**Representer theorem** (Kimeldorf & Wahba, 1971; Schölkopf, Herbrich & Smola, 2001). For any loss $L$ and any strictly increasing $\Omega$, every minimiser of

$$\sum_{i=1}^n L\big(y_i, f(x_i)\big) + \Omega\big(\lVert f\rVert_{\mathcal H}\big)$$

over the whole RKHS has the form $f^\star = \sum_{i=1}^n\alpha_i k(x_i, \cdot)$.

**Proof idea.** Split $f = f_\parallel + f_\perp$, where $f_\parallel$ lies in the span of the training bumps and $f_\perp$ is orthogonal to it. By the reproducing property $f_\perp(x_i) = \langle f_\perp, k(x_i, \cdot)\rangle = 0$, so $f_\perp$ does not change any prediction on the training data, but it adds $\lVert f_\perp\rVert^2$ to the norm. The best choice is $f_\perp = 0$.

The notebook confirms this: allowing 30 extra bump centres at non-training locations produced the same function (to $10^{-9}$) and the same RKHS norm. **Why it matters:** an optimisation over an infinite-dimensional function space becomes a finite problem in $n$ coefficients. This makes SVMs, kernel ridge regression and GPs computable, and is also why their cost grows with $n$.

## 11. Kernel ridge regression and the Gaussian-process connection

**Kernel ridge regression (KRR)** minimises $\sum_i(y_i - f(x_i))^2 + \lambda\lVert f\rVert^2_{\mathcal H}$. Substituting the representer form gives $\lVert y - K\alpha\rVert^2 + \lambda\alpha^\top K\alpha$; setting the gradient to zero:

$$\alpha = (K + \lambda I)^{-1}y, \qquad \hat f(x) = k(x, X)(K + \lambda I)^{-1}y.$$

$K + \lambda I$ is positive definite, so it is solved with a **Cholesky factorisation** and two triangular solves rather than an explicit inverse.

**Worked example by hand.** Two training points $x_1 = 0$, $x_2 = 1$ with $y = (1, 0)$, RBF kernel with $\gamma = 1$, $\lambda = 0.1$. Then $k(0, 1) = e^{-1} = 0.368$, so

$$K + \lambda I = \begin{pmatrix}1.1 & 0.368\\ 0.368 & 1.1\end{pmatrix},\quad \det = 1.21 - 0.135 = 1.075,\quad \alpha = \frac{1}{1.075}\begin{pmatrix}1.1\\ -0.368\end{pmatrix} = \begin{pmatrix}1.024\\ -0.342\end{pmatrix}.$$

Prediction at $x = 0.5$: both kernel values are $e^{-0.25} = 0.779$, so $\hat f(0.5) = 0.779 \times (1.024 - 0.342) = 0.531$. At $x = 0$: $1.024 - 0.368 \times 0.342 = 0.898$, slightly below the label 1 because $\lambda$ shrinks the fit.

**Complexity.**

| | Linear ridge | Kernel ridge |
|---|---|---|
| training | $O(nd^2 + d^3)$ | $O(n^2 d)$ to build $K$ + $O(n^3)$ to solve |
| memory | $O(d^2)$ | $O(n^2)$ |
| prediction | $O(d)$ | $O(nd)$ |
| cheaper when | $n \gg d$ | $d \gg n$ (or infinite-dimensional features) |

**Two hyper-parameters.** The bandwidth $\gamma$ (large means narrow bumps and wiggly functions) and the regularisation $\lambda$. They interact: in the notebook's validation grid the good region is a diagonal band, where wider kernels need less regularisation. The best validation MSE (0.107) sat just above the noise variance 0.09.

**KRR vs SVR.** Same function class and the same RKHS regulariser, different loss. KRR uses squared loss: closed-form solution, every $\alpha_i$ non-zero. Support vector regression uses the $\varepsilon$-insensitive loss: needs a quadratic-programming solver but gives a sparse set of support vectors.

**The Gaussian-process view.** A **Gaussian process** $f \sim \mathcal{GP}(0, k)$ is a prior over functions where any finite set of values is jointly Gaussian with covariance $K$. With noisy observations $y = f(X) + \varepsilon$, $\varepsilon \sim \mathcal N(0, \sigma^2 I)$:

$$\mu(x_*) = k(x_*, X)(K + \sigma^2 I)^{-1}y, \qquad \operatorname{Var}(x_*) = k(x_*, x_*) - k(x_*, X)(K + \sigma^2 I)^{-1}k(X, x_*).$$

The **posterior mean is exactly the KRR predictor with $\lambda = \sigma^2$** (the notebook matches them to $10^{-14}$). KRR is the frequentist view (a penalised fit); the GP is the Bayesian view and adds **error bars**, which grow away from the data. This is why GPs drive Bayesian optimisation. Subtlety: GP *sample paths* are almost surely not in the RKHS (they are rougher), although the posterior mean is. Note scikit-learn's `RBF(length_scale=ℓ)` corresponds to $\gamma = 1/(2\ell^2)$.

## 12. Kernel PCA and kernel k-means

PCA and k-means use only dot products and distances, so they can be kernelised to find curved structure.

**Kernel PCA** (Schölkopf, Smola & Müller, 1998):
1. **Centre the Gram matrix** in feature space: $\tilde K = HKH$ with $H = I - \frac1n\mathbf 1\mathbf 1^\top$.
2. Eigen-decompose $\tilde K = U\Lambda U^\top$.
3. The coordinate of training point $i$ on component $k$ is $\sqrt{\lambda_k}\,U_{ik}$.

Forgetting step 1 is a classic bug: without centring, the first component mostly captures the feature-space mean rather than variance.

**Kernel k-means.** The squared distance from $\phi(x_i)$ to the mean of cluster $C$ needs only kernel values:

$$\lVert\phi(x_i) - \mu_C\rVert^2 = K_{ii} - \frac{2}{|C|}\sum_{j \in C}K_{ij} + \frac{1}{|C|^2}\sum_{j, l \in C}K_{jl}.$$

On two concentric rings, linear PCA only rotates the rings (they still overlap), while RBF kernel PCA separates them on the first component; kernel k-means recovers the rings perfectly (adjusted Rand index 1.000) while ordinary k-means scores about 0. Both need $O(n^2)$ memory; kernel PCA needs an $O(n^3)$ eigendecomposition (or $O(n^2k)$ for the top $k$ with iterative solvers), and kernel k-means costs $O(n^2)$ per iteration. Kernel k-means is closely related to **spectral clustering** (Dhillon, Guan & Kulis, 2004).

## 13. Scaling up: Nyström and random Fourier features

With $n = 10^6$ points the Gram matrix has $10^{12}$ entries (8 TB in 64-bit floats) and an $O(n^3)$ solve is impossible. Both fixes build an explicit $D$-dimensional feature map $z(x)$ with $z(x)^\top z(x') \approx k(x, x')$, after which ordinary linear methods apply at cost $O(nD^2)$.

**Nyström method** (Williams & Seeger, 2001). Pick $D$ landmark points (for example random training points). With $C = K(X, \text{landmarks})$ ($n \times D$) and $W = K(\text{landmarks}, \text{landmarks})$, approximate $K \approx CW^{+}C^\top$ and use features $z(x) = W^{-1/2}k(\text{landmarks}, x)$ ($W^+$ is the pseudo-inverse). It is **data-dependent** and excellent when the kernel's eigenvalues decay fast.

**Random Fourier features** (Rahimi & Recht, 2007). **Bochner's theorem** says a shift-invariant kernel $k(x - z)$ is the Fourier transform of a probability distribution. For the RBF kernel $e^{-\gamma\lVert x - z\rVert^2}$, draw $w_j \sim \mathcal N(0, 2\gamma I)$ and $b_j \sim U(0, 2\pi)$, and set

$$z(x) = \sqrt{2/D}\,\big[\cos(w_j^\top x + b_j)\big]_{j=1}^D.$$

The approximation is unbiased with error $O(1/\sqrt D)$ and is **data-independent**, which suits streaming data and fixed feature pipelines.

| Method | Training cost | Memory | Best when |
|---|---|---|---|
| exact kernel | $O(n^3)$ | $O(n^2)$ | $n \lesssim 10^4$ |
| Nyström, $D$ landmarks | $O(nD^2 + D^3)$ | $O(nD)$ | fast eigen-decay, data available |
| random Fourier features | $O(nD^2)$ (+ $O(ndD)$ to build) | $O(nD)$ | shift-invariant kernels, streaming |

In the notebook's approximation-error table, Nyström with 100 landmarks had error 0.005 vs 0.17 for 100 random features, and Nyström closely tracked the best possible rank-$D$ approximation. On $n = 3000$, Nyström with 300 landmarks nearly matched exact KRR's test error while training faster; the gap grows quickly with $n$ because exact KRR is cubic and the approximations are linear in $n$.

## 14. The kernel two-sample test (MMD)

"Do these two piles of data come from the same distribution?" The **maximum mean discrepancy** is the distance between the two distributions' average positions (**mean embeddings**) in the RKHS:

$$\mathrm{MMD}^2(P, Q) = \lVert\mu_P - \mu_Q\rVert^2_{\mathcal H} = \mathbb E[k(x, x')] + \mathbb E[k(y, y')] - 2\,\mathbb E[k(x, y)].$$

For a **characteristic** kernel such as the RBF, $\mathrm{MMD} = 0$ if and only if $P = Q$, so it detects *any* difference. The unbiased estimator (Gretton et al., 2012) averages within-sample kernel values excluding the diagonal and subtracts twice the average cross-sample value. A **permutation test** gives the p-value: shuffle the pooled sample, recompute the statistic many times, and count how often it exceeds the observed value. The bandwidth is set by the **median heuristic** ($1/\gamma$ = the median squared pairwise distance).

**Drift-detection results from the notebook:**

| Scenario | MMD detects? | Per-feature t-tests detect? |
|---|---|---|
| no drift | no (p = 0.21) | no |
| mean shift in one feature | yes | yes |
| variance change, same mean | yes | no |
| new correlation, same marginals | yes | no |

A t-test compares only means, and every univariate test (even Kolmogorov–Smirnov) misses a correlation change, because each feature's marginal distribution is unchanged. Cost: $O((m+n)^2 d)$ for the Gram matrix. **Pitfall:** choosing the bandwidth by maximising the statistic on the same data you test invalidates the p-value. The **kernel inception distance (KID)** used to evaluate image generators is an MMD with a polynomial kernel on network features.

## 15. Kernels for structured data: strings and graphs

Kernels let us compare objects that are not vectors by counting shared building blocks.

**Spectrum kernel for strings** (Leslie, Eskin & Noble, 2002). $\phi_k(s)$ counts every length-$k$ substring (**$k$-mer**) of $s$; the kernel is the dot product of counts. It is valid by construction (an explicit feature map) and is computed with hash maps without enumerating all $4^k$ possible DNA $k$-mers. **By hand:** for $s = $ `GATTA` and $t = $ `ATTAC` with $k = 2$, $s$ has `GA, AT, TT, TA` and $t$ has `AT, TT, TA, AC`; three shared 2-mers, each counted once, so $k(s, t) = 3$. In the notebook, detecting a planted `GATTACA` motif rose from 0.63 accuracy ($k = 1$, letter counts) to 1.00 ($k = 5$).

**Weisfeiler–Lehman (WL) subtree kernel** (Shervashidze et al., 2011). Start with node labels (for example degrees). In each iteration, relabel every node by the pair (its label, the sorted multiset of its neighbours' labels), compressed to a new label. The graph's feature vector counts labels across iterations; the kernel is the dot product. Iteration $h$ looks $h$ steps into each node's neighbourhood. This relabelling is the message passing of a **graph neural network**, and a standard message-passing GNN is at most as powerful as the 1-WL test at telling graphs apart (Xu et al., 2019). 1-WL cannot distinguish two regular graphs with the same degree, and cannot count triangles in general. In the notebook, graphs vs degree-preserving shuffles were indistinguishable at $h = 0$ (accuracy 0.37) and reached about 0.72 at $h = 2$.

## 16. The neural tangent kernel

For a network $f(x; \theta)$, the **neural tangent kernel** (NTK; Jacot, Gabriel & Hongler, 2018) is

$$\Theta(x, x') = \nabla_\theta f(x; \theta)^\top\nabla_\theta f(x'; \theta).$$

Under gradient flow on squared loss, the training outputs evolve as $\dot f = -\Theta(f - y)$. In the **infinite-width limit** (with the NTK parameterisation $f = \frac{1}{\sqrt m}\sum_j a_j\,\mathrm{relu}(w_j^\top x)$): the weights move only $O(1/\sqrt m)$ relative to their size, $\Theta$ stays essentially constant during training, and the trained network equals **kernel regression with $\Theta$**, started from the initial function. For discrete gradient descent with step $\eta$ for $T$ steps, the linearised model is

$$f_T(x) = f_0(x) - \Theta(x, X)\Theta(X, X)^{-1}\big(I - (I - \eta\Theta(X, X))^T\big)\big(f_0(X) - y\big).$$

In the notebook, as width grew from 10 to 10,000 the relative weight change fell from 1.61 to 0.034 (roughly $1/\sqrt{\text{width}}$) and the trained network converged onto the kernel prediction.

**Why it matters:** this **lazy training** regime explains why very wide networks are easy to optimise (the problem becomes a convex kernel regression) and lets kernel theory make statements about them. It also marks the limitation: a network in the kernel regime **does not learn features**, because its kernel is frozen at initialisation. Real finite-width networks do learn features, a big part of why they beat kernel methods on images and text (Chizat, Oyallon & Bach, 2019).

## Kernel methods at a glance

| Method | What the kernel replaces | Training cost | Prediction cost | Notes |
|---|---|---|---|---|
| kernel ridge regression | $x^\top z$ in ridge | $O(n^3)$ | $O(n)$ kernel evaluations | closed form; equals GP mean |
| SVM / SVR | $x^\top z$ in the QP dual | $O(n^2)$–$O(n^3)$ (SMO) | $O(\#\text{SV})$ | sparse |
| Gaussian process | covariance function | $O(n^3)$ | $O(n)$ mean, $O(n^2)$ variance | uncertainty |
| kernel PCA | covariance → centred Gram | $O(n^3)$ or $O(n^2k)$ | $O(n)$ per point | non-linear dimensionality reduction |
| kernel k-means | feature-space distances | $O(n^2)$ per iteration | $O(n)$ | related to spectral clustering |
| MMD test | difference of mean embeddings | $O(n^2)$ per permutation | – | detects any distribution change |
| Nyström / RFF | the Gram matrix | $O(nD^2)$ | $O(D)$ | turns kernels into linear models |
| NTK | gradient inner products | implicit | – | infinite-width network limit |

## How it all fits together

- **Norms are the common language.** Rademacher bounds depend on $\lVert w\rVert$; margin bounds on $R/\gamma$; kernel methods regularise $\lVert f\rVert_{\mathcal H}$; double descent is explained by the norm of the minimum-norm interpolator. "Small norm = low capacity" links both halves of this module.
- **Attention is a kernel smoother.** Softmax attention $\sum_j\frac{\exp(q^\top k_j)}{\sum_l\exp(q^\top k_l)}v_j$ is Nadaraya–Watson kernel regression with an exponential kernel; Performer-style linear attention replaces it with random features to get linear cost in sequence length ([`05_Deep_Learning/05_transformers_architecture`](../../../05_Deep_Learning/05_transformers_architecture.ipynb)).
- **Benchmarks and LLMs.** The $\ln K$ penalty for reusing a validation set is why heavily reused public benchmarks (and contamination) inflate reported scores; empirical scaling laws are the data-driven successor to sample-complexity bounds.
- **Practical tools:** test-set sizing (Hoeffding), drift detection (MMD), Bayesian optimisation (GPs), graph learning (WL and GNNs, [`05_Deep_Learning/07_gnn`](../../../05_Deep_Learning/07_gnn.ipynb)), and distribution-free guarantees in [conformal prediction](../../14_conformal_prediction/01_conformal_prediction.ipynb).

## Glossary

- **Agnostic learning**: learning without assuming that a perfect hypothesis exists in the class (labels may be noisy).
- **Approximation error**: $R(h^\star) - R^\star$, the error caused by the class being too limited.
- **Bayes risk**: the lowest possible true risk of any function for a given distribution.
- **Bias (statistical)**: how far the average model over training sets is from the true function.
- **Bochner's theorem**: a shift-invariant kernel is the Fourier transform of a non-negative measure; the basis of random Fourier features.
- **Characteristic kernel**: a kernel for which MMD is zero only when the two distributions are equal (e.g. RBF).
- **Double descent**: test error that falls, peaks at the interpolation threshold, then falls again as capacity grows.
- **Effective degrees of freedom**: $\sum_j s_j^2/(s_j^2 + \lambda)$, a smooth measure of ridge-regression capacity.
- **Empirical risk**: the average loss on the training sample.
- **Empirical risk minimisation (ERM)**: choosing the hypothesis with the smallest training loss.
- **Estimation error**: $R(\hat h) - R(h^\star)$, the error caused by learning from a finite sample.
- **Feature map**: a function $\phi$ that turns an input into a feature vector.
- **Gaussian process**: a prior over functions whose values at any finite set of points are jointly Gaussian with a kernel covariance.
- **Gram matrix**: the $n \times n$ matrix of pairwise kernel values $K_{ij} = k(x_i, x_j)$.
- **Growth function**: the maximum number of distinct labellings a class can produce on $m$ points.
- **Hoeffding's inequality**: a bound $2e^{-2m\varepsilon^2}$ on the probability that an average of bounded independent variables deviates from its mean by $\varepsilon$.
- **Hypothesis class**: the set of models a learning algorithm may choose from.
- **i.i.d.**: independent and identically distributed; the core assumption of learning-theory bounds.
- **Inductive bias**: the assumptions a learner makes that let it generalise beyond the training data.
- **Interpolation threshold**: the capacity at which a model can just fit the training data exactly.
- **Kernel**: a function $k(x, z) = \langle\phi(x), \phi(z)\rangle$; a similarity score equal to a dot product of features.
- **Kernel trick**: replacing dot products in an algorithm by kernel evaluations to work in feature space implicitly.
- **Kernel ridge regression (KRR)**: ridge regression in the RKHS, $\alpha = (K + \lambda I)^{-1}y$.
- **Lazy training**: the regime in which a very wide network barely moves its weights and behaves like a fixed kernel method.
- **Margin**: the distance from a classifier's decision boundary to the nearest training point.
- **Massart's lemma**: Rademacher complexity of a class with $N$ behaviours is at most $\sqrt{2\ln N/m}$ (for ±1 values).
- **Maximum mean discrepancy (MMD)**: the RKHS distance between two distributions' mean embeddings; used as a two-sample test.
- **Median heuristic**: setting the RBF bandwidth from the median pairwise squared distance.
- **Mercer's condition**: a symmetric function is a valid kernel iff every Gram matrix it produces is PSD.
- **Neural tangent kernel (NTK)**: the kernel formed by inner products of a network's parameter gradients.
- **No-free-lunch theorem**: averaged over all targets, every learner has chance-level accuracy on unseen points.
- **Nyström method**: a low-rank kernel approximation built from a subset of landmark points.
- **PAC learning**: "probably approximately correct": error at most $\varepsilon$ with probability at least $1 - \delta$.
- **Positive semidefinite (PSD)**: a symmetric matrix with $c^\top Kc \ge 0$ for all $c$ (all eigenvalues non-negative).
- **Rademacher complexity**: the expected best correlation between a function class and random ±1 labels on the data.
- **Random Fourier features (RFF)**: random cosine features whose dot products approximate a shift-invariant kernel.
- **RBF kernel**: the Gaussian kernel $\exp(-\gamma\lVert x - z\rVert^2)$.
- **Realisable case**: the class contains a hypothesis with zero true error.
- **Representer theorem**: regularised risk minimisers in an RKHS are weighted sums of kernel bumps at the training points.
- **RKHS**: reproducing kernel Hilbert space, the function space associated with a kernel, where $f(x) = \langle f, k(x, \cdot)\rangle$.
- **Sauer–Shelah lemma**: a class of VC dimension $d$ produces at most $\sum_{i \le d}\binom mi$ labellings on $m$ points.
- **Shattering**: realising all $2^m$ labellings of a set of $m$ points.
- **Spectrum kernel**: a string kernel that counts shared length-$k$ substrings.
- **Structural risk minimisation (SRM)**: minimising training error plus a complexity penalty over nested classes.
- **True risk**: the expected loss on new data from the distribution (generalisation error).
- **Uniform convergence**: all empirical risks in a class being close to their true risks simultaneously.
- **Union bound**: $\Pr[A_1 \cup \dots \cup A_K] \le \sum_k\Pr[A_k]$.
- **Variance (statistical)**: how much a learned model's predictions change across different training sets.
- **VC dimension**: the size of the largest set of points a class can shatter.
- **Weisfeiler–Lehman kernel**: a graph kernel built from iterated neighbourhood relabelling, closely tied to GNN message passing.
