# Probabilistic Graphical Models & Approximate Inference

A probabilistic graphical model describes a joint probability distribution over many variables by drawing a graph whose edges show which variables interact directly. This guide walks through every concept in the two notebooks of this folder in order: first how to **represent** a distribution with a graph and do **exact inference** on it (notebook 01), then what to do when variables are **hidden** or exact inference is too expensive: EM, sampling and variational inference (notebook 02). It assumes you have met Bayes' rule, Bayesian networks and HMMs in [`classical_ai/09`](../../../00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb), probability in [`14_Mathematics/03_probability`](../../../14_Mathematics/03_probability.ipynb), and priors, posteriors and Metropolis–Hastings in [`14_Mathematics/07_bayesian_ml`](../../../14_Mathematics/07_bayesian_ml.ipynb).

## The Vocabulary You Need First

- **Random variable**: a quantity whose value is uncertain, such as "the patient has flu" (yes/no) or "the colour of pixel (3, 7)". Written with capital letters, $X$; a particular value is lower case, $x$.
- **Joint distribution** $P(X_1, \dots, X_n)$: one probability for every combination of values. With $n$ binary variables it has $2^n - 1$ free numbers, which is why we never store it directly.
- **Conditional independence** $X \perp Y \mid Z$: once you know $Z$, learning $Y$ tells you nothing more about $X$. Formally $P(X \mid Y, Z) = P(X \mid Z)$.
- **Inference**: computing something from the model, usually a **marginal** $P(X_i)$, a **conditional** $P(Q \mid e)$ given evidence $e$, or the **MAP assignment** (the single most likely complete configuration).
- **Learning**: estimating the numbers (parameters) and possibly the graph (structure) from data.
- **Latent variable**: a variable that is part of the model but never observed, such as the cluster of a data point or the hidden state of an HMM.

Why it matters: a chain-structured Bayesian network over 10 binary variables needs only 19 numbers instead of 1,023. The graph's missing edges buy that saving, and the saving grows exponentially with the number of variables.

---

# Part 1 · Markov Networks and Exact Inference (notebook 01)

## 1. Directed and Undirected Models

### Bayesian networks (recap)

A **Bayesian network (BN)** is a directed acyclic graph (DAG) plus one **conditional probability table (CPT)** per node:

$$P(X_1, \dots, X_n) = \prod_i P(X_i \mid \mathrm{Pa}(X_i)),$$

where $\mathrm{Pa}(X_i)$ are the parents of $X_i$. Every factor is already a normalised probability, so the product sums to 1 automatically. Arrows suggest a causal or generative story ("disease causes symptom").

### Markov networks

A **Markov network**, also called a **Markov random field (MRF)**, uses an **undirected** graph. For each **clique** $c$ (a set of nodes that are all connected to each other) we choose a non-negative **potential** (or **factor**) $\phi_c(x_c)$: a compatibility score, **not** a probability. The distribution is the **Gibbs distribution**

$$P(x) = \frac{1}{Z}\prod_c \phi_c(x_c), \qquad Z = \sum_x \prod_c \phi_c(x_c).$$

$Z$ is the **partition function**. It sums over every joint assignment, so computing it is the hard part (it is #P-hard in general). Writing **energies** $E_c = -\log\phi_c$ gives $P(x) \propto e^{-\sum_c E_c(x_c)}$, the Boltzmann distribution of physics; modern **energy-based models** use exactly this form.

| | Bayesian network | Markov network |
|---|---|---|
| Graph | directed, acyclic | undirected |
| Local parameters | CPTs $P(X \mid \mathrm{Pa})$, normalised | potentials $\phi_c \ge 0$, unnormalised |
| Normalisation | automatic ($Z = 1$) | global $Z$ needed |
| Natural for | causal / generative stories | symmetric interactions (pixels, spins, social ties) |
| Reading independence | d-separation | plain graph separation |
| Learning from complete data | closed-form counts | iterative (needs $Z$ and its gradient) |

**Worked example: the misconception network** (Koller & Friedman, section 4.1). Four students study in pairs around a ring A–B–C–D–A. Potentials reward agreement, except C–D who like to disagree; for example $\phi_1(A, B)$ has entries $a^0b^0{:}30$, $a^0b^1{:}5$, $a^1b^0{:}1$, $a^1b^1{:}10$, and the other three use 100 for the favoured pairs and 1 otherwise. Brute force over the 16 assignments gives $Z = 7{,}201{,}840$, and the most likely assignment $(a^0, b^1, c^1, d^0)$ has probability about 0.69. The key lesson: $\phi_1$ alone strongly favours $a^0b^0$, but the true marginal $P(A, B)$ puts most mass (0.694) on $a^0b^1$, because Bob is pulled towards Charles by a much stronger potential. **A potential is not a marginal**; every potential's influence depends on all the others through $Z$.

**Hammersley–Clifford theorem.** A *strictly positive* distribution satisfies the independence (Markov) properties of an undirected graph $H$ if and only if it factorises as a Gibbs distribution over the cliques of $H$. This is the formal link between "the graph" and "the formula".

**Factor graphs** draw one node per variable and one node per factor, with an edge when a factor mentions a variable. They represent both BNs and MRFs and are the natural data structure for message passing.

## 2. Reading Conditional Independence off the Graph

### d-separation

In a DAG, a path (trail) between $X$ and $Y$ is **active** given evidence $Z$ if every consecutive triple on it is active:

| Triple | Name | Active when |
|---|---|---|
| $A \to B \to C$ | chain | $B$ not observed |
| $A \leftarrow B \to C$ | fork (common cause) | $B$ not observed |
| $A \to B \leftarrow C$ | collider / v-structure (common effect) | $B$ **or one of its descendants** is observed |

$X$ and $Y$ are **d-separated** by $Z$ if no active trail exists. **Soundness**: d-separation implies $X \perp Y \mid Z$ in *every* distribution that factorises over the graph. The converse almost always holds too: for randomly chosen parameters, "not d-separated" means "dependent" except on a set of measure zero. A distribution whose independencies are exactly those of the graph is called **faithful**.

The notebook implements the linear-time **reachability ("Bayes ball") algorithm** (Koller & Friedman, Algorithm 3.1): first mark $Z$ and its ancestors (these are the colliders that can be activated), then do a breadth-first search over (node, direction-of-arrival) pairs. Tested against random 7-node networks, all 344 d-separated pairs were numerically independent and all 664 non-d-separated pairs were dependent.

**Explaining away** in the burglary network: Burglary and Earthquake are independent, but become dependent once the Alarm, or even just JohnCalls (a descendant of the alarm), is observed. If you know the alarm went off and then hear there was an earthquake, a burglary becomes less likely.

### Markov blankets

The **Markov blanket** of $X$ is the smallest set that makes $X$ independent of everything else.
- In a BN: parents, children, and the children's other parents (co-parents).
- In a Markov network: simply the neighbours.

The notebook verifies this numerically: once the blanket is fixed, changing every other variable changes $P(X = 1 \mid \text{rest})$ by at most about $10^{-16}$. Gibbs sampling uses this fact: each update only needs the blanket.

### I-maps and perfect maps

Let $\mathcal{I}(G)$ be the independencies a graph asserts and $\mathcal{I}(P)$ those true in a distribution. $G$ is an **I-map** of $P$ if $\mathcal{I}(G) \subseteq \mathcal{I}(P)$: everything the graph claims is true. A complete graph is a useless I-map of everything; we want a **minimal** I-map, ideally a **perfect map** ($\mathcal{I}(G) = \mathcal{I}(P)$). Neither family can express everything: the four-node ring (with $A \perp C \mid \{B, D\}$ and $B \perp D \mid \{A, C\}$) has no perfect BN, and a v-structure has no perfect Markov network. That is why both families are needed.

## 3. Factors: the Building Blocks of Exact Inference

A **factor** $\phi(X_1, \dots, X_k)$ is a table with one non-negative number per joint assignment. CPTs, potentials, evidence indicators and every intermediate result are factors. Four operations are enough for all exact algorithms:

| Operation | Definition | Example |
|---|---|---|
| Product | $(\phi_1 \cdot \phi_2)(x \cup y) = \phi_1(x)\,\phi_2(y)$, matching shared variables | $P(A)\,P(B \mid A) = P(A, B)$ |
| Marginalise (sum out) | $\psi(Y) = \sum_x \phi(x, Y)$ | $\sum_A P(A, B) = P(B)$ |
| Reduce (evidence) | $\psi(Y) = \phi(x_{\text{obs}}, Y)$ | $P(A = 1, B)$ as a function of $B$ |
| Normalise | divide by the total | $P(B, e) \to P(B \mid e)$ |

The notebook stores each factor as a numpy array with one axis per variable and uses broadcasting for products. Using it, the misconception $Z$ and $P(A, B)$ come out exactly as in the brute-force table, and $P(B \mid A = 1) = [0.769, 0.231]$.

## 4. Variable Elimination, Elimination Order and Treewidth

### The algorithm

**Variable elimination (VE)** computes $P(Q \mid e)$:
1. Reduce every factor by the evidence.
2. For each hidden variable $X$ in a chosen order: multiply all factors that mention $X$, sum $X$ out, put the new factor back.
3. Multiply what remains and normalise.

It is just the distributive law $\sum_x a \cdot b(x) = a \sum_x b(x)$ applied systematically: push each sum as far inside the product as it will go.

**Worked example by hand (chain A–B–C).** Take the three-friends chain from the README, with $\phi(u, v) = 10$ if $u = v$ and 1 otherwise. To get $P(C \mid A = 1)$, eliminate B: $m(C) = \sum_B \phi(1, B)\,\phi(B, C)$. For $C = 1$: $10 \cdot 10 + 1 \cdot 1 = 101$. For $C = 0$: $10 \cdot 1 + 1 \cdot 10 = 20$. Normalise: $P(C = 1 \mid A = 1) = 101/121 \approx 0.835$. Two small multiplications replace a sum over all patterns.

The notebook's VE reproduces the AIMA burglary query $P(\text{Burglary} \mid \text{JohnCalls}, \text{MaryCalls}) = 0.284$.

### Cost, induced width and treewidth

Each elimination step creates an intermediate factor over $X$ and all its current neighbours. Eliminating $X$ also connects all of its neighbours to each other (these new edges are called **fill edges**). With domain size $d$, VE costs

$$O(n \cdot d^{\,w+1}),$$

where $w$ is the **induced width** of the order: the largest number of neighbours any variable has at the moment it is eliminated. The minimum induced width over all orders is the **treewidth** of the graph (for a BN, of its **moral graph**: connect co-parents and drop arrow directions).

| Graph | Treewidth | Exact inference |
|---|---|---|
| Tree, chain, HMM | 1 | linear in $n$ |
| $k \times k$ grid | $k$ | $O(n \cdot d^{k+1})$ |
| Complete graph on $n$ nodes | $n - 1$ | exponential in $n$ |

Finding the optimal order is NP-hard, so we use greedy heuristics:
- **Min-degree**: eliminate the variable with the fewest current neighbours.
- **Min-fill**: eliminate the variable whose elimination adds the fewest fill edges (usually better).

**Measured in the notebook:**
- **Star graph** (one hub, 12 leaves): eliminating the hub first creates a $2^{13} = 8{,}192$-entry table and touches 106,492 entries; eliminating leaves first never exceeds $2 \times 2$ and touches 92. Same answer.
- **4 × 4 Ising grid:** min-degree and min-fill both reach width 4, the grid's treewidth (5 when the query variable is forced to stay until the end); a random order is worse.

Why it matters: a $100 \times 100$ binary image has treewidth 100, so exact inference would need tables with $2^{101}$ entries. Exact inference is hopeless for images; approximation is necessary.

## 5. Belief Propagation

### Sum-product on a pairwise MRF

For a **pairwise MRF** $P(x) \propto \prod_i \phi_i(x_i) \prod_{(i,j)} \psi_{ij}(x_i, x_j)$, the **message** from node $i$ to neighbour $j$ is

$$m_{i \to j}(x_j) = \sum_{x_i} \phi_i(x_i)\,\psi_{ij}(x_i, x_j) \prod_{k \in N(i) \setminus j} m_{k \to i}(x_i),$$

and the **belief** (estimated marginal) is $b_i(x_i) \propto \phi_i(x_i) \prod_{k \in N(i)} m_{k \to i}(x_i)$.

Intuition: $m_{i \to j}$ is node $i$'s summary of "everything I have heard from the part of the graph behind me", expressed as a vote over $j$'s values.

```
   leaves                root                leaves
   x1 ---m1->2---> x2 ---m2->3---> x3 <---m4->3--- x4
                                    |
   pass 1: leaves -> root     pass 2: root -> leaves
   after both passes every node holds its exact marginal
```

- **On a tree** BP is exact. It is VE for *all* marginals at once, reusing shared work: two passes, $O(n d^2)$ in total. In the notebook, BP on a 12-node tree with 3 states matched the $3^{12} = 531{,}441$-entry brute-force marginals to $10^{-14}$, converging after one sweep more than the tree's diameter.
- **On graphs with loops**, iterating the same updates is **loopy BP**. It is not guaranteed to converge or to be exact, because evidence can travel around a cycle and be counted twice, but it often works very well. **Damping** (mixing old and new messages) helps convergence. Loopy BP is the decoder for LDPC and turbo codes used in Wi-Fi, 5G and deep-space links. Its fixed points are the stationary points of the **Bethe free energy** (Yedidia, Freeman & Weiss), which links BP to variational inference.
- The **junction tree** algorithm makes BP exact on any graph by running it on a tree of cliques, at cost exponential in the treewidth.

### Image denoising with the Ising model

A binary image $x \in \{-1, +1\}^{H \times W}$ is observed through a channel that flips each pixel with probability $p$, giving $y$. The **Ising model** prior says neighbours usually agree:

$$P(x \mid y) \propto \prod_i \exp(h\,x_i y_i) \prod_{(i,j) \in \text{grid}} \exp(J\,x_i x_j), \qquad h = \tfrac{1}{2}\ln\frac{1-p}{p}.$$

The unary term is the exact log-likelihood ratio of the noise; $J > 0$ rewards smoothness. On a $40 \times 40$ image with $p = 0.15$ and $J = 0.8$, 40 damped sweeps of loopy BP cut the pixel error from 12.6% to 0.8%. Remaining errors sit at corners and thin parts, where the smoothness prior fights the true edges.

## 6. MAP Inference: Max-Product and Viterbi

The **MAP assignment** is $x^\star = \arg\max_x P(x \mid e)$. Replacing $\sum$ by $\max$ in VE or BP gives the **max-product** algorithm (**max-sum** in log space). On a chain this is the **Viterbi algorithm**:

$$\delta_t(s) = \max_{s'}\big[\delta_{t-1}(s') + \log A_{s's}\big] + \log B_s(o_t),$$

with back-pointers to recover the path. Cost $O(T S^2)$ for $T$ steps and $S$ states, versus $S^T$ by brute force.

**MAP is not the same as per-variable argmax.** In the notebook's 3-state weather HMM over 8 days, Viterbi's best path is "Sunny every day" with joint probability $6.457 \times 10^{-7}$. Taking each day's most likely state from its marginal gives a jumpy Sunny–Cloudy–…–Rainy–…–Sunny sequence whose joint probability is only $5.202 \times 10^{-7}$. Use MAP when you need one coherent labelling (speech, tagging); use marginals when you need per-position confidence.

## 7. Linear-Chain Conditional Random Fields

An HMM models $P(x, y)$, the words *and* the tags, so it must also model how words are generated; rich overlapping features ("capitalised", "previous word is *in*") are awkward there. A **linear-chain conditional random field** (Lafferty, McCallum & Pereira, 2001) models only $P(y \mid x)$:

$$P(y \mid x) = \frac{1}{Z(x)} \exp\Big(\sum_t \big[w_{y_t}^\top f(x, t) + T_{y_{t-1}, y_t}\big]\Big), \qquad Z(x) = \sum_{y'} \exp(\text{score}(x, y')).$$

It is an undirected chain over the tags, conditioned on the whole input: multinomial logistic regression over entire label sequences.

| | HMM | Linear-chain CRF |
|---|---|---|
| Models | $P(x, y)$, generative | $P(y \mid x)$, discriminative |
| Features | one emission per state | any features of the whole input |
| Training | counts (or Baum–Welch if unlabelled) | convex optimisation (L-BFGS, SGD) |
| Inference | forward–backward, Viterbi | the same, on the CRF scores |

- **Inference:** the forward algorithm gives $\log Z(x)$ in $O(TK^2)$ for $K$ tags; forward–backward gives node and pair marginals; Viterbi gives the best tag sequence.
- **Learning:** the log-likelihood is concave, with the classic exponential-family gradient: $\frac{\partial \log P(y \mid x)}{\partial w_k} = (\text{observed count of feature } k) - \mathbb{E}_{y' \sim P(\cdot \mid x)}[\text{count of feature } k]$.

On the notebook's toy tagging task (O / PER / LOC) with test names and cities never seen in training, the CRF reached 0.993 token accuracy and 0.980 entity-token accuracy against 0.692 and 0.081 for a most-frequent-tag baseline, and tagged the ambiguous words "Jordan" and "Florence" correctly 95.5% of the time from context. The gradient was checked by finite differences, and $\log Z$ by brute force. BiLSTM-CRF and transformer-CRF taggers replace the hand-made features with neural ones and keep exactly this layer on top.

## 8. Learning Bayesian Networks

### Parameters from complete data

With fully observed data the BN likelihood **decomposes** into one independent term per CPT row, and the **maximum-likelihood estimate** is a ratio of counts:

$$\hat\theta_{x \mid u} = \frac{N(x, u)}{N(u)}.$$

With little data, counts of 0 give probabilities of exactly 0 (and parent configurations never seen give 0/0). A **Dirichlet prior** adds $\alpha$ pseudo-counts to every cell:

$$\hat\theta_{x \mid u} = \frac{N(x, u) + \alpha}{N(u) + \alpha\,|\mathrm{Val}(X)|},$$

and $\alpha = 1$ is **Laplace smoothing**. On the student network (Difficulty, Intelligence → Grade; Intelligence → SAT; Grade → Letter) with 10 samples, plain MLE left 5.75% of entries undefined and 44% at exactly 0 or 1; smoothing fixed both and lowered the error. As $N$ grows the prior's influence vanishes and both estimators converge, with error shrinking like $1/\sqrt{N}$.

### Structure from data

**Score-based** learning searches over DAGs for the best score. The **BIC score** is log-likelihood minus a complexity penalty:

$$\mathrm{BIC}(G) = \sum_i \Big[\log \hat L_i - \frac{\ln N}{2}\,\#\text{params}_i\Big].$$

It decomposes over nodes and their parent sets, so a local move changes only one or two terms. **Greedy hill-climbing**: start from the empty graph, repeatedly apply the single edge addition, deletion or reversal that most improves BIC while staying acyclic, and stop at a local optimum. **Constraint-based** methods (the PC algorithm) instead run conditional-independence tests and orient edges using v-structures.

**Markov equivalence.** Graphs with the same **skeleton** (undirected edges) and the same **v-structures** encode the same independencies, so data alone cannot tell them apart. $I \to S$ and $S \to I$ are indistinguishable; the collider $D \to G \leftarrow I$ is identifiable. In the notebook, a single hill-climb from the empty graph got stuck at BIC $-12{,}250.9$ (wrong skeleton) while the true graph scores $-12{,}247.0$; the best of 10 random restarts found the true skeleton and v-structure. Do not read learned arrows as causal: causal claims need interventions or extra assumptions ([`10_causal_inference`](../../10_causal_inference/01_causal_inference.ipynb)).

### Summary of Part 1

| Task | Algorithm | Exact? | Cost |
|---|---|---|---|
| Marginal / conditional | enumeration | yes | $O(d^n)$ |
| Marginal / conditional | variable elimination | yes | $O(n\,d^{w+1})$ |
| All marginals, tree | sum-product BP | yes | $O(n\,d^2)$ |
| All marginals, loopy graph | loopy BP | no | $O(\text{iters} \cdot \lvert E\rvert\, d^2)$ |
| All marginals, any graph | junction tree | yes | $O(n\,d^{w+1})$ |
| MAP | max-product / Viterbi | yes on trees | as sum-product |
| Sequence labelling | linear-chain CRF | yes | $O(nK^2)$ per sentence |
| BN parameters | counts + Dirichlet | closed form | $O(N n)$ |
| BN structure | BIC hill-climbing | local optimum | many score evaluations |

---

# Part 2 · EM, Variational Inference and Sampling (notebook 02)

## 9. Why Latent Variables Make Learning Hard

A **latent-variable model** generates data in two steps: draw a hidden $z$, then draw the visible $x$ given $z$. The **Gaussian mixture model (GMM)** picks a cluster $z \in \{1, \dots, K\}$ with probability $\pi_k$ and then $x \sim \mathcal{N}(\mu_z, \Sigma_z)$. We want to maximise the **marginal (incomplete-data) log-likelihood**

$$\log p(x \mid \theta) = \log \sum_z p(x, z \mid \theta).$$

| Problem | Why | Consequence |
|---|---|---|
| Log of a sum | the log cannot move inside the sum | no closed-form maximiser |
| Many configurations | $N$ points, $K$ clusters give $K^N$ assignments | brute force impossible unless the sum factorises |
| Non-convex, symmetric surface | swapping labels gives the same likelihood ($K!$ equivalent modes), plus genuine local optima | answer depends on initialisation |

The **complete-data** log-likelihood $\log p(x, z \mid \theta)$ is easy: if we knew every point's cluster, each mean would be an average. EM exploits exactly this. For a 1-D two-component mixture the notebook plots two identical likelihood peaks, at about $(-2, 2)$ and $(2, -2)$: **label switching**.

## 10. EM Derived from Jensen's Inequality

Pick any distribution $q(z)$ over the latents, multiply and divide by it, and use **Jensen's inequality** ($\log \mathbb{E}[Y] \ge \mathbb{E}[\log Y]$, because log is concave):

$$\log p(x \mid \theta) = \log \sum_z q(z) \frac{p(x, z \mid \theta)}{q(z)} \;\ge\; \sum_z q(z) \log \frac{p(x, z \mid \theta)}{q(z)} =: \mathcal{L}(q, \theta).$$

$\mathcal{L}$ is the **evidence lower bound (ELBO)**. The gap is exactly a KL divergence:

$$\log p(x \mid \theta) = \mathcal{L}(q, \theta) + \mathrm{KL}\big(q(z) \,\|\, p(z \mid x, \theta)\big), \qquad \mathrm{KL} \ge 0.$$

**EM is coordinate ascent on the ELBO:**
- **E-step:** fix $\theta$, maximise over $q$. The best $q$ makes the KL zero: $q(z) = p(z \mid x, \theta_{\text{old}})$, the posterior ("responsibilities").
- **M-step:** fix $q$, maximise over $\theta$. The entropy of $q$ does not depend on $\theta$, so this maximises the **expected complete-data log-likelihood** $Q(\theta, \theta_{\text{old}}) = \mathbb{E}_q[\log p(x, z \mid \theta)]$, which usually has a closed form.

**Monotonicity:** $\log p(x \mid \theta_{\text{new}}) \ge \mathcal{L}(q, \theta_{\text{new}}) \ge \mathcal{L}(q, \theta_{\text{old}}) = \log p(x \mid \theta_{\text{old}})$. The likelihood never decreases; EM converges to a stationary point (usually a local maximum), not necessarily the global one.

```
 log p(x|theta)  (true curve)
      ^         ____
      |      __/    \__        E-step: build the lower bound L(q, .)
      |    _/  .--.    \_               that touches the curve at theta_old
      |   /  .'    '.    \     M-step: jump to the top of that bound
      |  / .'        '.   \    repeat: each step can only go uphill
      +---------------------->  theta
           old   new
```

Numerical check in the notebook (one point, a 3-component mixture): for a uniform $q$ the ELBO is $-3.442$ and the KL is $1.187$; for a random $q$, $-3.099$ and $0.844$; for the exact posterior, $-2.255$ and $0$. Every row sums to $\log p(x) = -2.255$.

## 11. EM for a Gaussian Mixture

**E-step:** $r_{nk} = \dfrac{\pi_k\,\mathcal{N}(x_n \mid \mu_k, \Sigma_k)}{\sum_j \pi_j\,\mathcal{N}(x_n \mid \mu_j, \Sigma_j)}$.

**M-step** (with $N_k = \sum_n r_{nk}$): $\pi_k = N_k/N$, $\mu_k = \frac{1}{N_k}\sum_n r_{nk} x_n$, $\Sigma_k = \frac{1}{N_k}\sum_n r_{nk}(x_n - \mu_k)(x_n - \mu_k)^\top$.

**Worked example by hand.** 1-D, $K = 2$, $\sigma = 1$ fixed, $\pi = \tfrac12$, current $\mu_1 = 0$, $\mu_2 = 4$, data $\{1, 3, 2\}$. Unnormalised densities $e^{-(x-\mu)^2/2}$: for $x = 1$, $0.607$ and $0.011$, so $r = (0.982, 0.018)$; for $x = 3$, the reverse; for $x = 2$, both $0.135$, so $r = (0.5, 0.5)$. New $\mu_1 = (0.982 + 0.054 + 1.0)/1.5 = 2.036/1.5 \approx 1.357$ and $\mu_2 \approx 2.643$.

Practical points from the notebook:
- Work in **log space** with `logsumexp` and use a **Cholesky** factorisation for the log-determinant and Mahalanobis distance, so tiny densities do not underflow.
- The from-scratch EM stopped after 46 E-steps and matched scikit-learn's `GaussianMixture` (same start) to about $10^{-6}$ in the means.
- On a harder 8-blob problem, only 5 of 10 random starts reached the best log-likelihood ($-1864.1$; the worst was $-1924.8$). That is why scikit-learn has `n_init` and initialises with k-means.
- **Degenerate maxima:** a component collapsing onto one point sends its variance to 0 and the likelihood to infinity. Adding $\epsilon I$ to each covariance (`reg_covar`) or a prior (MAP-EM) prevents it.
- **k-means is hard EM:** with shared covariance $\sigma^2 I$ and $\sigma \to 0$, responsibilities become 0/1 (nearest centroid) and the M-step becomes "average of assigned points".

| | Cost per iteration | Memory |
|---|---|---|
| E-step + covariance updates | $O(NKD^2)$ | $O(NK)$ responsibilities |
| Cholesky factorisations | $O(KD^3)$ | |

EM converges **linearly**, and slowly when clusters overlap heavily.

## 12. EM for Missing Data

A missing value is just another latent variable. For pairs $(x_1, x_2) \sim \mathcal{N}(\mu, \Sigma)$ with some $x_2$ missing, the E-step uses the bivariate-normal conditional

$$\mathbb{E}[x_2 \mid x_1] = \mu_2 + \frac{\Sigma_{12}}{\Sigma_{11}}(x_1 - \mu_1), \qquad \mathrm{Var}[x_2 \mid x_1] = \Sigma_{22} - \frac{\Sigma_{12}^2}{\Sigma_{11}},$$

and accumulates the expected **sufficient statistics** $\mathbb{E}[x_2]$, $\mathbb{E}[x_2^2] = \mathrm{Var} + \mathbb{E}[x_2]^2$ and $\mathbb{E}[x_1 x_2] = x_1\mathbb{E}[x_2]$. The M-step sets $\mu$ to the average expected $x$ and $\Sigma$ to the average expected $xx^\top$ minus $\mu\mu^\top$.

| Mechanism | Meaning | Valid methods |
|---|---|---|
| MCAR (missing completely at random) | missingness unrelated to any value | deletion is unbiased, just wasteful |
| MAR (missing at random) | depends only on observed values | likelihood methods (EM), multiple imputation |
| MNAR (missing not at random) | depends on the missing value itself | need a model of the missingness |

In the notebook, 254 of 500 rows lost $x_2$, more often when $x_1$ was large (MAR). The true mean of $x_2$ is 2.0: complete-case analysis gave 1.487, mean imputation 1.487 (and shrank the variance to 0.610 against a true 1.5), while EM gave 2.011, essentially the full-data estimate. Forgetting the variance term in $\mathbb{E}[x_2^2]$ reproduces the "regression imputation" bias of an underestimated $\Sigma$.

## 13. EM for an HMM: Baum–Welch

An HMM has initial distribution $\pi$, transition matrix $A_{ij} = P(z_{t+1} = j \mid z_t = i)$ and emission matrix $B_{io} = P(x_t = o \mid z_t = i)$. The hidden states are dependent over time, so the sum over $K^T$ paths does not factorise per step; **forward–backward** computes the needed posteriors by dynamic programming:
- **E-step:** $\gamma_t(i) = P(z_t = i \mid x)$ and $\xi_t(i, j) = P(z_t = i, z_{t+1} = j \mid x)$.
- **M-step:** $\pi = \gamma_1$, $A_{ij} = \sum_t \xi_t(i, j) / \sum_t \gamma_t(i)$, $B_{io} = \sum_{t : x_t = o} \gamma_t(i) / \sum_t \gamma_t(i)$. Expected counts replace observed counts.

Cost: $O(TK^2)$ time and $O(TK)$ memory per sequence per iteration, versus $O(K^T)$ by brute force. Always scale or work in logs: unscaled forward values underflow to 0 after a few hundred steps. In the notebook's "occasionally dishonest casino" (fair vs loaded die), Baum–Welch on 40 sequences of 100 rolls learned $A \approx \begin{bmatrix}0.954 & 0.046 \\ 0.097 & 0.903\end{bmatrix}$ against a true $\begin{bmatrix}0.95 & 0.05 \\ 0.1 & 0.9\end{bmatrix}$, and posterior decoding labelled 82% of rolls correctly. This is the learning step that the CpG-island HMM in [`18_domain_applications/02_bioinformatics_sequence_ml`](../../18_domain_applications/02_bioinformatics_sequence_ml.ipynb) skips by assuming known parameters.

## 14. Gibbs Sampling

**Markov chain Monte Carlo (MCMC)** builds a random walk whose long-run distribution (its **stationary distribution**) is the target posterior, then averages over the visited states. **Gibbs sampling** visits each variable in turn and redraws it from its **full conditional** $p(x_i \mid x_{-i})$, which by Section 2 depends only on its Markov blanket. It is Metropolis–Hastings with the full conditional as proposal, so every proposal is accepted (acceptance probability exactly 1). No step size to tune, but you need conditionals you can sample.

**Bivariate normal.** With correlation $\rho$: $x_1 \mid x_2 \sim \mathcal{N}(\rho x_2, 1 - \rho^2)$ and vice versa. Gibbs moves parallel to the axes ("staircase"). At $\rho = 0.5$ it explores freely; at $\rho = 0.99$ the target is a thin diagonal ridge, each step is tiny, and consecutive samples are highly correlated. Strong correlation between variables is Gibbs sampling's main weakness.

**Bayesian GMM** (1-D, $\sigma = 1$, $\pi \sim \mathrm{Dirichlet}(\alpha)$, $\mu_k \sim \mathcal{N}(0, \tau_0^2)$). Every full conditional is conjugate:

| Variable | Full conditional |
|---|---|
| $z_n$ | $P(z_n = k \mid \cdot) \propto \pi_k\,\mathcal{N}(x_n \mid \mu_k, 1)$ |
| $\pi$ | $\mathrm{Dirichlet}(\alpha + n_1, \dots, \alpha + n_K)$ |
| $\mu_k$ | $\mathcal{N}(m, v)$ with $v = 1/(1/\tau_0^2 + n_k)$, $m = v\sum_{n : z_n = k} x_n$ |

Unlike EM's single estimate, Gibbs returns a **distribution**: posterior means $-3.95, 0.18, 5.00$ for true $-4, 0, 5$, with posterior standard deviations near $1/\sqrt{n_k}$. Label switching is handled by sorting the means at each sweep (fine for well-separated components).

**Collapsed Gibbs for LDA.** **Latent Dirichlet Allocation** gives each document topic proportions $\theta_d \sim \mathrm{Dir}(\alpha)$, each topic a word distribution $\phi_k \sim \mathrm{Dir}(\beta)$, and each word a topic $z \sim \mathrm{Cat}(\theta_d)$ then a word $w \sim \mathrm{Cat}(\phi_z)$. **Collapsing** integrates $\theta$ and $\phi$ out analytically (Dirichlet–multinomial conjugacy) and samples only the topic assignments (Griffiths & Steyvers, 2004):

$$P(z_i = k \mid z_{-i}, w) \propto (n_{dk}^{-i} + \alpha)\,\frac{n_{kw}^{-i} + \beta}{n_k^{-i} + V\beta},$$

"how much this document likes topic $k$" times "how much topic $k$ likes this word", with counts excluding the current word. On a toy corpus of 40 documents and 800 tokens, 100 sweeps recovered the planted sports, food and tech topics with purity 1.0. One sweep costs $O(N_{\text{tokens}} K)$. Collapsing leaves fewer variables and usually mixes much faster.

## 15. MCMC Diagnostics

MCMC samples are correlated, and we never know for certain that a chain has reached its stationary distribution. Diagnostics cannot prove convergence, but they reliably catch common failures.

- **Autocorrelation at lag $k$:** $\rho_k = \mathrm{Corr}(x_t, x_{t+k})$.
- **Effective sample size:** $\mathrm{ESS} = N / (1 + 2\sum_{k \ge 1}\rho_k)$. The variance of the chain's mean is about $\mathrm{Var}(x)/\mathrm{ESS}$. The sum is truncated with **Geyer's initial positive sequence** (add autocorrelations in pairs until a pair turns negative).
- **Split-R̂ (Gelman–Rubin):** run $M$ chains from spread-out starts, split each in half, compare within-chain variance $W$ and between-chain variance $B$: $\hat R = \sqrt{\big(\frac{n-1}{n}W + \frac{1}{n}B\big)/W}$. A common modern rule is $\hat R < 1.01$ (Vehtari et al., 2021).

**Exact check.** The $x_1$-chain of the bivariate Gibbs sampler is an AR(1) process with coefficient $\phi = \rho^2$, so $\rho_k = \phi^k$ and $\mathrm{ESS}/N = (1 - \phi)/(1 + \phi)$:

| $\rho$ | $\phi = \rho^2$ | ESS/N (estimate) | ESS/N (theory) |
|---|---|---|---|
| 0.50 | 0.25 | 0.609 | 0.600 |
| 0.90 | 0.81 | 0.114 | 0.105 |
| 0.99 | 0.98 | 0.008 | 0.010 |

At $\rho = 0.99$, 20,000 sweeps are worth only about 170–200 independent draws. Split-R̂ after 400 sweeps from four spread-out starts was 1.004 at $\rho = 0.5$ and 1.319 at $\rho = 0.99$ (not converged).

**Worked example.** If $\rho_k = 0.9^k$ and you ran 10,000 iterations, $\mathrm{ESS} = 10{,}000 \times 0.1/1.9 \approx 526$; for an ESS of 1,000 you need about 19,000 iterations.

For random-walk Metropolis on $\mathcal{N}(0, 1)$, a tiny step accepts almost everything but crawls, a huge step is almost always rejected, and a step near $2.4\sigma$ (acceptance about 44%, the classic optimal scaling in one dimension) gives the highest ESS. Burn-in discards samples taken before the chain reached the typical set; **thinning** saves memory but never adds information.

## 16. Mean-Field Variational Inference (CAVI)

**Variational inference** chooses the best approximation $q$ from a simple family by minimising $\mathrm{KL}(q \,\|\, p(\theta \mid x))$, which is the same as maximising the ELBO (Section 10). The **mean-field** family factorises: $q(\theta) = \prod_j q_j(\theta_j)$. **Coordinate ascent VI (CAVI)** updates one factor at a time:

$$\log q_j^\star(\theta_j) = \mathbb{E}_{q_{-j}}\big[\log p(x, \theta)\big] + \text{const}.$$

For conjugate-exponential models each update has a closed form, and none can decrease the ELBO, so a monotone ELBO curve is a good debugging check, just like EM's likelihood.

**Gaussian with unknown mean and precision** (Bishop PRML section 10.1.3): $x_n \sim \mathcal{N}(\mu, \tau^{-1})$, $\mu \mid \tau \sim \mathcal{N}(\mu_0, (\lambda_0\tau)^{-1})$, $\tau \sim \mathrm{Gamma}(a_0, b_0)$. The exact posterior is Normal-Gamma, with $\mu$ and $\tau$ dependent. Mean-field sets $q(\mu, \tau) = q(\mu)q(\tau)$:

| Factor | Update |
|---|---|
| $q(\mu) = \mathcal{N}(\mu_N, \lambda_N^{-1})$ | $\mu_N = (\lambda_0\mu_0 + N\bar x)/(\lambda_0 + N)$, $\lambda_N = (\lambda_0 + N)\,\mathbb{E}[\tau]$ |
| $q(\tau) = \mathrm{Gamma}(a_N, b_N)$ | $a_N = a_0 + (N+1)/2$, $b_N = b_0 + \tfrac12\mathbb{E}_\mu\big[\sum_n(x_n - \mu)^2 + \lambda_0(\mu - \mu_0)^2\big]$ |

With 12 data points, the final ELBO was $-17.700$ against an exact log evidence of $-17.665$ (gap = KL = 0.035). The means were exact, but VI's standard deviation of $\mu$ was 0.246 against an exact 0.266. **Mean-field VI tends to underestimate posterior uncertainty**, because an axis-aligned $q(\mu)q(\tau)$ cannot capture the pear-shaped dependence.

**Bayesian GMM by CAVI** (Blei et al., 2017): with $q(\mu_k) = \mathcal{N}(m_k, s_k^2)$ and $q(c_n) = \mathrm{Cat}(\varphi_n)$, the updates are $\varphi_{nk} \propto \exp(m_k x_n - (s_k^2 + m_k^2)/2)$, $s_k^2 = 1/(1/\sigma^2 + \sum_n \varphi_{nk})$ and $m_k = s_k^2 \sum_n \varphi_{nk} x_n$. The $\varphi$ update is the EM responsibility with $\mu_k$ replaced by its expectation and an extra $-s_k^2/2$ penalty for uncertainty. CAVI converged in 14 iterations (0.014 s) to almost the same means as Gibbs, which took seconds.

**Which KL?** $\mathrm{KL}(q \,\|\, p)$ is **mode-seeking** ("zero-forcing"): it is huge wherever $q$ has mass and $p$ does not, so on a bimodal posterior $q$ locks onto one mode. $\mathrm{KL}(p \,\|\, q)$, used by **expectation propagation**, is **mass-covering**: for an equal mixture of $\mathcal{N}(-3, 1)$ and $\mathcal{N}(3, 1)$ it gives the moment-matched $\mathcal{N}(0, 10)$, which puts most of its mass in the gap.

## 17. Stochastic VI and the Reparameterisation Trick

CAVI needs closed-form updates and touches all the data every step. **Stochastic VI** (Hoffman et al., 2013), and more generally **black-box VI**, maximises the ELBO by stochastic gradient ascent using a minibatch of data (scaled by $N/B$) and a few Monte Carlo samples from $q$. The difficulty is the gradient $\nabla_\varphi \mathbb{E}_{q_\varphi(z)}[f(z)]$, because the distribution depends on $\varphi$:

| Estimator | Formula | Needs | Variance |
|---|---|---|---|
| Score function (REINFORCE) | $\mathbb{E}[f(z)\nabla_\varphi \log q_\varphi(z)]$ | only $\nabla \log q$; $f$ may be non-differentiable | high |
| Reparameterisation (pathwise) | write $z = \mu + \sigma\varepsilon$, $\varepsilon \sim \mathcal{N}(0, 1)$; use $\mathbb{E}_\varepsilon[\nabla_\varphi f(\mu + \sigma\varepsilon)]$ | $f$ differentiable, $q$ reparameterisable | usually much lower |

Toy check with $\nabla_\mu \mathbb{E}_{z \sim \mathcal{N}(\mu, 1)}[z^2] = 2\mu$ at $\mu = 1$: both estimators are unbiased (means about 2.0), but the per-sample variance is 30.7 for the score function against 4.0 for reparameterisation (exactly $\mathrm{Var}[2z] = 4\sigma^2$). For Bayesian logistic regression, stochastic VI in PyTorch (minibatch 100, 8 samples, decaying learning rate) matched a long Metropolis chain's posterior means closely, with slightly narrower standard deviations.

**The VAE connection.** A variational autoencoder ([`05_Deep_Learning/20_generative_models_hands_on`](../../../05_Deep_Learning/20_generative_models_hands_on.ipynb)) maximises exactly this ELBO, $\mathbb{E}_{q(z \mid x)}[\log p(x \mid z)] - \mathrm{KL}(q(z \mid x) \,\|\, p(z))$, with two twists: the encoder is **amortised** (one network outputs $q$'s parameters for any $x$, instead of a separate $q$ per data point), and gradients flow through $z = \mu + \sigma\varepsilon$. Its negative ELBO is an upper bound on $-\log p(x)$, and its tendency to blurry samples and "posterior collapse" are VI phenomena.

## 18. EM vs VI vs MCMC

| | EM | Variational inference | MCMC (Gibbs, MH, HMC) |
|---|---|---|---|
| Output | point estimate $\hat\theta$ + posterior over latents given $\hat\theta$ | approximate posterior $q$ over all unknowns | samples from the exact posterior (asymptotically) |
| Bias | none by definition, but local optima | biased by the family of $q$ (often over-confident) | asymptotically unbiased; error shrinks like $1/\sqrt{\mathrm{ESS}}$ |
| Cost per iteration | one E + one M step | like EM (CAVI) or a minibatch gradient (SVI) | one sweep, but thousands needed |
| Convergence check | log-likelihood stops rising | ELBO stops rising | ESS, R̂, trace plots (never certain) |
| Scales to huge data | yes (online EM) | yes (SVI, amortisation) | hard |
| Parameter uncertainty | no | approximate | accurate |
| Typical use | GMMs, HMMs, missing data | VAEs, LDA at scale, Bayesian NNs | small/medium Bayesian models (Stan, PyMC) |

Rule of thumb: a good fit of a latent-variable model, use EM; calibrated uncertainty on a small model, use MCMC (HMC/NUTS for continuous parameters); uncertainty at scale or inside a neural network, use VI. Developing with MCMC on a subset and deploying with VI is common.

## Why All of This Matters

- **NLP:** CRF output layers for NER and slot filling; LDA topic models.
- **Communications and robotics:** loopy BP decodes LDPC codes in Wi-Fi and 5G; Kalman filters are Gaussian BP on a chain.
- **Deep learning:** GNNs are learned message passing; VAEs and diffusion models are trained on variational bounds; energy-based models are Gibbs distributions with an intractable $Z$.
- **Bioinformatics and speech:** HMMs with Viterbi and Baum–Welch segment genomes (CpG islands, gene finding) and powered classic HMM-GMM speech recognisers.
- **Statistics and science:** probabilistic programming systems (Stan, PyMC, NumPyro) automate the samplers, diagnostics and VI of Part 2.

---

## Glossary

- **Amortised inference** — a network maps each input to its approximate posterior's parameters, instead of optimising a separate $q$ per data point.
- **Ancestral sampling** — sampling a BN by drawing each variable after its parents.
- **Baum–Welch** — EM for HMMs, using forward–backward expected counts.
- **Bayesian network** — DAG plus CPTs; joint = product of $P(X_i \mid \mathrm{Pa}(X_i))$.
- **Belief propagation (sum-product)** — message passing that computes marginals; exact on trees.
- **Bethe free energy** — the approximation whose stationary points are loopy BP's fixed points.
- **BIC score** — log-likelihood minus $\frac{\ln N}{2}$ times the number of parameters.
- **CAVI** — coordinate ascent variational inference; updates one mean-field factor at a time.
- **Clique** — a set of nodes all connected to each other.
- **Collapsed Gibbs** — Gibbs sampling after integrating some variables out analytically.
- **Collider (v-structure)** — $A \to B \leftarrow C$; blocks the path unless $B$ or a descendant is observed.
- **Complete-data likelihood** — $p(x, z \mid \theta)$, the likelihood as if latents were observed.
- **CPT** — conditional probability table $P(X \mid \mathrm{Pa}(X))$.
- **CRF (conditional random field)** — an undirected model of $P(y \mid x)$; linear-chain CRFs label sequences.
- **d-separation** — graphical test for conditional independence in a DAG.
- **Damping** — mixing old and new BP messages to help convergence.
- **Dirichlet prior / Laplace smoothing** — pseudo-counts added to every cell; $\alpha = 1$ is Laplace.
- **E-step / M-step** — set $q$ to the posterior / maximise expected complete-data log-likelihood.
- **Effective sample size (ESS)** — the number of independent draws a correlated chain is worth.
- **ELBO** — evidence lower bound $\mathcal{L}(q, \theta) = \mathbb{E}_q[\log p(x, z) - \log q(z)]$.
- **Explaining away** — observing a common effect makes its independent causes dependent.
- **Factor** — a non-negative table over a set of variables.
- **Factor graph** — bipartite graph of variable nodes and factor nodes.
- **Faithful distribution** — one whose independencies are exactly those of the graph.
- **Forward–backward** — dynamic programming for chain marginals in $O(TK^2)$.
- **Gibbs distribution** — $P(x) = \frac{1}{Z}\prod_c\phi_c(x_c)$.
- **Gibbs sampling** — MCMC that redraws each variable from its full conditional.
- **Hammersley–Clifford theorem** — positive distributions with an MRF's Markov properties factorise over its cliques, and vice versa.
- **I-map / perfect map** — a graph whose independencies all hold in $P$ / exactly equal those of $P$.
- **Induced width** — the largest neighbour count at elimination time for a given order.
- **Ising model** — binary pairwise MRF with $\exp(J x_i x_j)$ couplings; used for image denoising.
- **Junction tree** — exact BP on a tree of cliques; cost exponential in treewidth.
- **KL divergence** — $\mathrm{KL}(q \| p) = \mathbb{E}_q[\log q - \log p] \ge 0$; asymmetric.
- **Label switching** — permuting cluster labels gives the same likelihood.
- **Latent variable** — a modelled but unobserved variable.
- **LDA** — latent Dirichlet allocation, a mixture model for documents over topics.
- **Loopy BP** — belief propagation iterated on a graph with cycles; approximate.
- **MAP assignment** — the single most probable complete configuration.
- **MAR / MCAR / MNAR** — missing at random / completely at random / not at random.
- **Markov blanket** — the set that shields a variable from all others (parents, children, co-parents; or neighbours).
- **Markov equivalence** — same skeleton and v-structures, hence same independencies.
- **Markov network (MRF)** — undirected graph with clique potentials and a partition function.
- **Max-product (max-sum)** — BP with max instead of sum; finds MAP assignments.
- **MCMC** — Markov chain Monte Carlo: sampling by a Markov chain whose stationary distribution is the target.
- **Mean-field** — a variational family that factorises over groups of variables.
- **Min-degree / min-fill** — greedy heuristics for choosing an elimination order.
- **Moral graph** — a BN's undirected version with co-parents joined.
- **Partition function $Z$** — the normalising sum of an MRF.
- **Potential** — a non-negative compatibility score on a clique; not a probability.
- **Reparameterisation trick** — writing $z = \mu + \sigma\varepsilon$ so gradients pass through sampling.
- **Responsibility** — $r_{nk}$, the posterior probability that point $n$ came from component $k$.
- **Score-function estimator (REINFORCE)** — gradient estimator $\mathbb{E}[f(z)\nabla\log q(z)]$; unbiased, high variance.
- **Split-R̂** — convergence diagnostic comparing between- and within-chain variance; aim for below 1.01.
- **Stochastic VI** — maximising the ELBO with minibatch, Monte Carlo gradients.
- **Treewidth** — the minimum induced width over all elimination orders.
- **Variable elimination** — exact inference by summing variables out one at a time.
- **Variational inference** — approximating a posterior by optimising over a simple family.
- **Viterbi** — max-product on a chain; finds the most likely hidden-state path in $O(TS^2)$.
