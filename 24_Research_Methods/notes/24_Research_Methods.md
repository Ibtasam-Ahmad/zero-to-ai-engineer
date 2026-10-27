# Research Methods for AI & Data Science

This is the study guide for the module's six notebooks. It covers everything you need to turn "my model scored higher" into a claim that an examiner, a reviewer or a product team will believe. It follows the order of the notebooks: choosing a question and reading the literature, designing a fair experiment, testing whether a gain is real, making it reproducible, writing it up, and running a whole study end to end. Every term is defined when it first appears. Formulas come with small worked examples you can check by hand. Near the end are two tools you will reuse for years: a **"which statistical test do I use?" decision table** and a **thesis / paper checklist**.

The research cycle that the whole module follows:

```
   question --> literature --> hypotheses --> design --> run --> analyse --> write --> share
      ^         (gap?)        (testable)     (fair?)            (real?)   (honest)  (reproducible)
      |                                                                                 |
      +---------------------- new questions, replications, critiques <-----------------+
```

---

## Part 1 · Research methodology and the literature (notebook 01)

### What research is

**Research** is a *systematic*, *documented* investigation that produces *new* and *verifiable* knowledge.
- *Systematic*: you follow a method you can describe.
- *New*: it adds something not already known. That can be a fact, a method, a dataset, or a confirmation or refutation of an earlier claim.
- *Verifiable*: others can check it, because you give enough data, code and detail.

One study has a value on **each** of four independent axes:

| Axis | Options | AI example |
|---|---|---|
| Purpose | **basic** (understand why) / **applied** (solve a practical problem) | why transformers learn in context / an Urdu fake-news detector |
| Data | **quantitative** (numbers) / **qualitative** (words, interviews) / **mixed** | F1 of 5 models over 10 seeds / interviews with 12 journalists |
| Evidence | **empirical** (observation, experiment) / **theoretical** (proof) | benchmark experiments / a generalisation bound |
| Depth | **exploratory** (what is going on?) / **descriptive** (what and how much?) / **explanatory** (why? what causes it?) | first look at LLM errors on Pashto / ablation of a RAG system |

The **scientific method** is the loop in the diagram above: observe, ask, hypothesise, test, analyse, report, repeat. A **research paradigm** is the set of beliefs a field holds about what counts as knowledge. Most ML work is *positivist / post-positivist*: it measures things and tests hypotheses. Interview studies are often *interpretivist*: they try to understand meanings and experiences.

### The research question

A **research question (RQ)** is the precise question your study is designed to answer. A typical MS thesis has one main RQ and 2–4 sub-questions. Check it against **FINER** (Hulley et al.):

| Letter | Criterion | Failing example |
|---|---|---|
| F | **Feasible** with your time, data, compute and skills | pre-training a 70B-parameter model on one laptop |
| I | **Interesting** to your supervisor and the community | renaming variables to see if accuracy changes |
| N | **Novel**: confirms, refutes or extends earlier findings | re-running a 2019 paper unchanged |
| E | **Ethical** | scraping private chat groups |
| R | **Relevant** to science, practice or policy | a metric nobody uses on a dataset nobody uses |

A good RQ names the **population or data, the intervention, the comparison and the outcome**. This is the PICO idea borrowed from medicine. Compare:
- Weak: "Can AI detect fake news?"
- Strong: "Does fine-tuning a multilingual transformer on 2,000 Urdu examples improve macro-F1 over a TF-IDF + logistic-regression baseline on the test split of dataset X?"

From the RQ you derive:
- **Hypotheses.** A *null hypothesis* H0 says there is no difference. The *alternative* H1 says there is one (it can be one-sided or two-sided). Both must be stated before you see the data.
- **Objectives.** These should be SMART: Specific, Measurable, Achievable, Relevant, Time-bound.
- **A contribution statement.** A bullet list of exactly what is new: a method, a dataset, an empirical finding, a tool.
- **The scope.** What is deliberately left out.

### Finding the literature

Search **several** sources, because no single one is complete:

| Source | Use it for |
|---|---|
| **Google Scholar** | the broadest coverage and its "Cited by" link (but no official API and results that are not fully reproducible) |
| **Semantic Scholar** | TL;DR summaries, citation contexts and a free API |
| **arXiv** | preprints. They are **not peer reviewed**; since late 2025 its CS section no longer accepts review or position papers that have not already passed peer review |
| **ACL Anthology**, **OpenReview**, **dblp** | NLP papers; ICLR/NeurIPS papers *with their reviews*; clean CS BibTeX |
| **OpenAlex** | an open catalogue with an API (the successor of Microsoft Academic) |
| **Papers with Code** | **shut down in July 2025**. Treat its old "state of the art" tables as historical |

**Boolean search strings** combine one block per concept. Synonyms inside a block are joined with OR, blocks are joined with AND, and NOT excludes terms. For example:

```
("fake news" OR misinformation) AND (Urdu OR "low-resource") AND (detect* OR classif*) NOT survey
```

Note that AND binds more tightly than OR, so `a OR b AND c` means `a OR (b AND c)`. Use brackets. **Record the exact string, the database and the date** of every search. Without the date, nobody can repeat it, because databases grow every day.

**Snowballing** (Wohlin, 2014) starts from a few good seed papers:
- **Backward**: read each seed's reference list (older papers).
- **Forward**: look up the papers that cite it (newer papers).
- Repeat on every newly included paper until a round adds nothing new.

This is a breadth-first search over the citation graph, costing $O(V+E)$ for $V$ papers and $E$ citations.

### Reading papers: the three-pass method (Keshav, 2007)

| Pass | Time | What you read | Output |
|---|---|---|---|
| 1 Bird's-eye | 5–10 min | title, abstract, introduction, headings, conclusion, figures | the 5 Cs: Category, Context, Correctness, Contributions, Clarity. Then decide whether to keep reading |
| 2 Content | ~1 h | the whole paper except proofs; figures and error bars carefully | a summary you could explain to someone else |
| 3 Virtual re-implementation | 4–5 h | everything, re-deriving each step | its hidden assumptions and possible flaws |

**Red flags of weak evidence**: a single run with no variance, a weak or untuned baseline, a tiny test set, the test set used for model selection, no ablation, claims wider than the data, no code or hyper-parameters, p-values without effect sizes, many uncorrected tests, and only the best seed or dataset shown. A red flag lowers your trust in a paper; it is not a reason to ignore it.

### The literature review matrix

A **literature review** *synthesises*: it groups papers by theme, compares their methods and evidence, and ends at the **research gap**. A list of summaries ("A did X. B did Y.") is an *annotated bibliography*, not a review.

The tool for this is a **review matrix**: one row per paper and one column per attribute (theme, method, data, language, metric, score, seeds, human evaluation, code). Then you:
- **Group** it by theme. Each theme becomes a subsection of the review.
- **Cross-tabulate** two attributes and look for empty cells. In the notebook, the cell (LLM prompting, Urdu) was empty while its neighbours were full. That makes it a *candidate* gap. Confirm it with a targeted search, and ask whether the answer would matter. An empty cell can also mean the idea is pointless or that your search missed papers.
- **Plot a timeline** of the field, such as the move from fine-tuning to prompting since 2023.

Also say explicitly that scores from different datasets cannot be compared directly.

### Systematic reviews and PRISMA 2020

A **systematic review** follows a pre-defined, reported **protocol**, so that someone else running it would find the same papers. A **meta-analysis** goes further and statistically pools the numeric results. You can have a systematic review without a meta-analysis, and in AI that is common, because papers use different datasets.

The steps are: write a protocol, identify records, remove duplicates, screen titles and abstracts (ideally with two screeners and Cohen's kappa), assess the full texts for eligibility, include studies, then extract data. **PRISMA 2020** (Page et al., *BMJ* 2021) is the reporting guideline: a 27-item checklist plus a flow diagram whose counts **must add up**. The notebook's example:

```
450 identified -> 197 duplicates removed -> 253 screened -> 206 excluded
-> 47 sought -> 4 not retrieved -> 43 assessed -> 16 excluded -> 27 included
check: 450 - 197 = 253;  253 - 206 = 47;  47 - 4 = 43;  43 - 16 = 27
```

Compute these numbers from your records with code, not by hand.

### References, ethics and the proposal

- **Reference managers** such as Zotero (with the Better BibTeX plugin), Mendeley, JabRef and EndNote store your papers and export **BibTeX**. A BibTeX entry has a type (`@article`, `@inproceedings`, `@misc`), a citation key and fields. When a paper has been peer-reviewed and published, cite that published version rather than the arXiv preprint.
- **Research ethics**:
  - **Plagiarism** includes **patchwriting** (changing a few words of someone else's sentence) and **self-plagiarism** (re-using your own published text without saying so).
  - **Authorship** requires a substantial contribution *and* accountability. Gift and ghost authorship are misconduct, and AI tools cannot be authors.
  - Data about people needs **consent and privacy** protection.
  - Studies with human participants usually need **ethics approval** (an IRB, or a research ethics committee) *before* any data is collected.
  - Think about **dual use**: research that can help and also harm.
  - If you use **AI writing tools**, disclose it, and verify every claim and every reference yourself.
- **The MS/MPhil proposal (synopsis)** has a core structure: title, introduction and problem statement, literature review and gap, research questions and objectives, methodology, expected contributions, a timeline (a Gantt chart with a buffer), and references.

> **Why it matters.** The research question is the steering wheel of a thesis. Every chapter, experiment and figure must help answer it. A vague question produces a vague thesis.

---

## Part 2 · Experiment design for ML (notebook 02)

### Variables, confounders and Simpson's paradox

| Variable | Meaning | ML example |
|---|---|---|
| **Independent** (factor, treatment) | what you change on purpose | model type, augmentation on/off |
| **Dependent** (outcome) | what you measure | macro-F1, latency, human preference |
| **Controlled** | kept fixed | split, tuning budget, epochs, hardware |
| **Confounder** | affects *both* which treatment is used *and* the outcome | dataset difficulty, when model A only ever ran on hard data |

In a **controlled experiment** you *assign* the treatment, ideally at random. Randomisation breaks the link with every confounder, known or unknown, so you can read a difference as *caused* by the treatment. An **observational study** only records what happened (old logs, numbers copied from papers), so confounders can remain.

**Simpson's paradox** (from the notebook's ticket log) shows what goes wrong without randomisation:

| | easy tickets | hard tickets | overall |
|---|---|---|---|
| Assistant A | 81/87 = 0.931 | 192/263 = 0.730 | 273/350 = **0.780** |
| Assistant B | 234/270 = 0.867 | 55/80 = 0.688 | 289/350 = **0.826** |

A is better within *each* difficulty level, yet B looks better overall. The reason is that A received mostly hard tickets. Assigning tickets at random fixes this: A's overall rate became 0.832 against B's 0.779.

### Randomisation, blocking and factorial designs

- **Blocking** means grouping similar units together and comparing treatments *within* each group: "block what you can, randomise what you cannot". In ML the key block is the **data split**. Evaluate every model on the *same* folds and the same test set, then analyse the **paired differences**. When two models' scores are positively correlated (an easy split is easy for both), the differences have a smaller variance. That gives narrower confidence intervals for free.
- A **factorial design** varies several factors in all combinations. A $2^3$ design has 8 configurations. The **main effect** of a factor is the mean outcome at its high level minus the mean at its low level. An **interaction** means one factor's effect depends on another factor's level; it shows up as non-parallel lines in an interaction plot.

  Hand check from the notebook (kNN, accuracy). With scaling the mean is $(0.9508+0.9508+0.9622+0.9631)/4 = 0.9567$; without it, $(0.9170+0.9170+0.9297+0.9328)/4 = 0.9241$. So the main effect of scaling is $+3.26$ points.

  Changing one factor at a time can never reveal an interaction. A full $2^f$ design costs $2^f \times$ (number of folds) fits.

### The ML experiment protocol

```
 full data --split once, before looking--> TEST (locked; use at the very end, ideally once)
                    |
                    +--> DEVELOPMENT --> CV / train-validation (tuning, ablations, early stopping)
```

- **Nested CV**: an inner loop tunes the hyper-parameters, and an outer loop scores the *whole tuning procedure*. The best inner score is biased upwards, because the maximum of many noisy scores is optimistic. On small, noisy data the notebook measured an average optimism of 0.037 accuracy.
- **Group and time splits**: rows from the same patient, user or document must stay on one side of the split (use `GroupKFold`), and the future must never predict the past (use `TimeSeriesSplit`). In the notebook, a random split gave 0.938 accuracy, but the honest grouped split gave 0.507.
- **Baselines** come in three kinds. A *trivial* baseline (the majority class) is the floor. A *classical* one (TF-IDF + logistic regression, gradient boosting) shows whether complexity pays off. The *prior state of the art*, **re-run under your own protocol**, shows whether your result is new. On the breast-cancer data the majority class already scores 0.627, and plain logistic regression scores 0.975.
- **Ablation**: remove or replace one component at a time and present the results as a table. When components overlap, report both "−X" (its *unique* contribution) and "only X" (its *total* usefulness).
- **Equal tuning budgets**: the same number of trials, search spaces of similar quality, and the same validation data for every method. A tuned SVM looked +30.9 points better than a *default* kNN. With equal budgets the difference was −0.6.
- **Seeds**: a single run is one sample. Fix a seed list in advance (for example 0–9), use at least 3–5 seeds (10 or more if runs are cheap) for *every* method, and report all of them. Changing only the initialisation seed moved one network's accuracy over a range of 1.85 points.
- **Learning curves** show whether more data would help and whether the ranking of methods depends on the data size.
- **Leakage** means information that will not be available at prediction time influences training. Anything that learns from data (scaling, imputation, feature selection) must go inside the pipeline and be fitted within each fold. On pure noise, selecting features before CV reported 0.820 accuracy instead of the true 0.5.

### Power analysis: how many test examples?

- **α** is the false-positive rate, usually 0.05.
- **Power** $= 1-\beta$ is the probability of detecting a real effect, usually 0.80.
- **δ** is the smallest effect you care about.

**Independent samples** (for example an A/B test), using the two-proportion formula:

$$n_{\text{per model}} = \frac{(z_{1-\alpha/2}+z_{1-\beta})^2\,[p_1(1-p_1)+p_2(1-p_2)]}{\delta^2}$$

*By hand* for 85% vs 86%: $(1.960+0.842)^2 = 7.85$, and $0.85\cdot0.15 + 0.86\cdot0.14 = 0.2479$. So $n = 7.85 \times 0.2479 / 0.0001 \approx 19{,}460$ per model. The notebook computes 19,458; the difference is only rounding of the z values.

**Paired, on the same test set** (McNemar; Connor, 1987). Only the **discordant** items carry information, that is, the items where exactly one model is right. Let ψ be the share of such items:

$$n = \frac{\left(z_{1-\alpha/2}\sqrt{\psi} + z_{1-\beta}\sqrt{\psi-\delta^2}\right)^2}{\delta^2}$$

With ψ = 0.05 you need about 3,923 items; with ψ = 0.20, about 15,696. Turning the question round gives the **minimum detectable effect** (MDE). With 1,000 test items and ψ = 0.05 you can reliably detect only about a 2-point difference (about 4.4 points with independent samples). Write this into your proposal.

### Threats to validity

| Threat | Question | Typical ML threat | Mitigation |
|---|---|---|---|
| **Internal** | did *my change* cause the difference? | unequal tuning, leakage, bugs | same pipeline, ablations, code review |
| **External** | does it generalise? | one dataset, one language, one domain | several datasets, out-of-domain and out-of-time tests |
| **Construct** | does the metric measure what I claim? | BLEU used as "quality", multiple-choice accuracy used as "reasoning" | human evaluation, several metrics |
| **Statistical conclusion** | is the inference sound? | single run, tiny test set, naive CV t-test | power analysis, seeds, correct tests, corrections |

**Benchmark overfitting**: when hundreds of ideas are tried on one public test set, the winner's score is biased upwards. The best of 500 *random* guessers scored 0.564 on the public test set and 0.534 on a fresh one. Large language models add the extra problem of **contamination**: test items may appear in the pre-training data. **Dataset shift** covers three cases: covariate shift (P(x) changes), label shift (P(y) changes) and concept drift (P(y | x) changes). An i.i.d. test set will not reveal any of them. In the notebook's covariate-shift demo, accuracy fell from 0.975 to 0.629.

### Pre-registration and human evaluation

**Pre-registration** means writing down the hypotheses, data, metrics, tests, the α level and its correction, the smallest effect of interest, and the stopping and exclusion rules *before* seeing any results. Then you time-stamp it on OSF, on AsPredicted, or as a dated commit. It protects you against the "garden of forking paths": quietly trying many analyses and reporting the one that worked. Anything you do later that was not in the plan must be labelled **exploratory**.

**Human evaluation** needs:
- clear guidelines and a pilot round;
- at least 2 (often 3) **blind** annotators, with outputs shown in random order;
- enough items, and a description of who the annotators were and how they were paid;
- reported agreement and a plan for resolving disagreements.

**Cohen's kappa** is the agreement between two annotators, corrected for chance:

$$\kappa = \frac{p_o - p_e}{1-p_e}, \qquad p_e = \sum_c p_1(c)\,p_2(c)$$

*By hand:* 100 items, two annotators labelling yes/no.

|  | B yes | B no | total |
|---|---|---|---|
| **A yes** | 40 | 20 | 60 |
| **A no** | 10 | 30 | 40 |
| **total** | 50 | 50 | 100 |

The observed agreement is $p_o = (40+30)/100 = 0.70$. The chance agreement is $p_e = 0.6\cdot0.5 + 0.4\cdot0.5 = 0.50$. So $\kappa = (0.70-0.50)/(1-0.50) = 0.40$.

The usual guide (Landis & Koch, 1977) reads 0.21–0.40 as "fair", 0.41–0.60 "moderate", 0.61–0.80 "substantial" and above 0.80 "almost perfect". For **ordinal** labels, weighted kappa penalises near-misses less.

**Krippendorff's alpha**, $\alpha = 1 - D_o/D_e$ (observed over expected disagreement), handles any number of annotators, missing ratings, and nominal, ordinal, interval or ratio scales. Krippendorff recommends α ≥ 0.80 for reliable data and treats 0.667 as the lowest value that allows tentative conclusions.

**Costs of common protocols**

| Protocol | Model fits |
|---|---|
| $r \times k$ repeated CV | $r \cdot k$ per model |
| 5×2cv | 10 per model |
| nested CV, grid of $G$ points | $K_{out}\,(K_{in}\,G + 1)$, e.g. $5\,(3 \cdot 30+1) = 455$ |
| full factorial with $f$ two-level factors | $2^f \times$ folds |
| ablation with $C$ configurations | $C \times$ folds |

---

## Part 3 · Statistical significance and reporting (notebook 03)

### Hypothesis testing in plain words

The **p-value** is $P(\text{data at least this extreme} \mid H_0)$. We *reject* H0 when $p < \alpha$. It is **not**:
- the probability that H0 is true;
- the probability that your model is better;
- a measure of how large the effect is.

And $p > 0.05$ does **not** prove that two models are equal.

| | H0 true | H0 false |
|---|---|---|
| reject H0 | **type I error** (false positive), rate α | correct (power, 1 − β) |
| keep H0 | correct | **type II error** (false negative), rate β |

**Effect size vs significance.** A useless gain of 0.03 points was "highly significant" (p ≈ 0.00002) with 20,000 paired measurements. A large gain of 0.8 points was *not* significant (p = 0.064) with only 5. So always report the **effect with a confidence interval**.

A **95% confidence interval** is produced by a procedure that captures the true value in 95% of repeated experiments. For a mean: $\bar x \pm t_{0.975,\,n-1}\, s/\sqrt n$. If the 95% CI for a *difference* excludes 0, a two-sided test at α = 0.05 rejects H0.

### Two models, one dataset, cross-validation only

The naive paired t-test, $t = \bar d / \sqrt{s^2/k}$, assumes the $k$ fold differences are independent. They are not, because the training sets overlap (in 10-fold CV, any two training sets share 8/9 of their rows). The **corrected resampled t-test** (Nadeau & Bengio, 2003) inflates the variance:

$$t = \frac{\bar d}{\sqrt{\left(\frac1k + \frac{n_{test}}{n_{train}}\right)s^2}}, \qquad df = k-1$$

*By hand:* 10-fold CV, mean difference $\bar d = 0.02$, standard deviation $s = 0.02$.
- Naive: $t = 0.02/\sqrt{0.0004/10} = 3.16$, p ≈ 0.012.
- Corrected: $(1/10 + 1/9)\cdot 0.0004 = 0.0000844$, so $t = 0.02/0.00919 = 2.18$, p ≈ 0.058, which is **not** significant.

The notebook's simulation with two truly equal models found that the naive test on 10×10 CV gave false positives in **52.5%** of datasets. The corrected test (1.5%), the 5×2cv t-test (2.0%) and the combined F-test (4.0%) all stayed at or below 5%.

**Dietterich's 5×2cv t-test** runs five repetitions of 2-fold CV. Let $s_i^2$ be the variance of the two differences in repetition $i$. Then $t = p_1^{(1)}/\sqrt{\tfrac15\sum_i s_i^2} \sim t_5$. The numerator uses only one fold difference, which makes the test noisy. Alpaydın's **combined 5×2cv F-test** uses all ten differences and is more stable.

### Two trained models, one fixed test set

**McNemar's test** uses only the discordant items: $b$ = A right and B wrong, $c$ = B right and A wrong. The exact version is a binomial test of $b$ out of $b+c$ with $p = 0.5$. The χ² version with continuity correction is

$$\chi^2 = \frac{(|b-c|-1)^2}{b+c}, \qquad df = 1$$

*By hand* (from the notebook): $b = 96$, $c = 63$, so $\chi^2 = 32^2/159 = 6.44$ and p = 0.011. A's 3.3-point accuracy gain is significant on this test set.

This does not contradict the CV test in the same notebook (p = 0.138), because the two tests answer **different questions**:
- McNemar asks: do these two *trained models* differ on this population? That is the deployment question.
- The CV tests ask: do the two *learning algorithms* differ when trained on new data? That is the thesis question about methods.

**The bootstrap** resamples the test set *with replacement* B times (e.g. 10,000), recomputes the metric each time, and takes the 2.5% and 97.5% percentiles as the CI. It works for any metric: accuracy, F1, AUC, BLEU. **BCa** intervals adjust for bias and skew. Two separate CIs that overlap do **not** mean "no difference", because they ignore the pairing.

The **paired bootstrap** resamples the *same* indices for both models and builds a CI for the *difference*. In the notebook the accuracy difference was +0.033 with CI [+0.009, +0.059], which excludes 0, even though the two separate CIs overlapped.

A **permutation (randomisation) test** randomly swaps the two models' outputs on each item (a coin flip per item), recomputes the difference, and repeats. The p-value is the share of shuffles at least as extreme as the observed difference. It makes almost no assumptions and works for any per-item score. For accuracy, it tests the same hypothesis as McNemar.

### Many models on many datasets (Demšar, 2006)

Do not average accuracies across datasets: the scales differ and outliers dominate. Instead:
1. Rank the $k$ methods on each of the $N$ datasets.
2. Run the **Friedman test** on the average ranks $R_j$:
   $$\chi^2_F = \frac{12N}{k(k+1)}\Big[\sum_j R_j^2 - \frac{k(k+1)^2}{4}\Big] \sim \chi^2_{k-1}$$
3. If Friedman rejects, run the **Nemenyi** post-hoc test: two methods differ if their average ranks differ by more than
   $$CD = q_\alpha\sqrt{k(k+1)/(6N)}$$
4. Draw a **critical-difference diagram**: methods joined by a bar are not significantly different.

*By hand:* $k = 5$, $N = 15$, $q_{0.05} = 2.728$, so $CD = 2.728\sqrt{30/90} = 1.575$ ranks. Random forest (average rank 1.67) is significantly better than naive Bayes (3.33) and the decision tree (4.00), but not than kNN (2.93).

For **two** methods across datasets, use the **Wilcoxon signed-rank** test and add a win/tie/loss count. A single pre-planned comparison is more powerful than Nemenyi's all-pairs protection.

### Multiple comparisons

If you run $m$ tests at α = 0.05 when nothing is going on, $P(\text{at least one false positive}) = 1-0.95^m$. For 20 tests that is $1 - 0.95^{20} = 0.64$.

| Method | Controls | Rule |
|---|---|---|
| Bonferroni | **FWER**, the probability of any false positive | adjusted $p_i = \min(1, m\,p_i)$ |
| **Holm** (step-down) | FWER; never less powerful than Bonferroni | sort the p-values; $\tilde p_{(i)} = \max_{j\le i}\min(1,(m-j+1)p_{(j)})$ |
| **Benjamini–Hochberg** (step-up) | **FDR**, the expected share of false discoveries among the rejections | $\tilde p_{(i)} = \min_{j\ge i}\min(1, m\,p_{(j)}/j)$ |

*By hand:* $p = (0.01, 0.04, 0.03, 0.005)$, $m = 4$. Sorted: 0.005, 0.01, 0.03, 0.04.
- Holm multiplies by 4, 3, 2, 1, giving 0.02, 0.03, 0.06, 0.04. The running maximum makes that 0.02, 0.03, 0.06, 0.06.
- BH computes $m\,p/\text{rank}$, giving 0.02, 0.02, 0.04, 0.04.

So at α = 0.05, Holm rejects two hypotheses and BH rejects all four.

As a rule of thumb, use **Holm for a handful of confirmatory claims** and **BH for exploratory screening** of many hypotheses. Always report $m$.

### Effect sizes and a Bayesian alternative

- **Cohen's d** $= (\bar x_1 - \bar x_2)/s_p$, with $s_p$ the pooled standard deviation. Rough guide: 0.2 small, 0.5 medium, 0.8 large. For paired data use $d_z = \bar d / s_d$. **Hedges' g** multiplies d by $1 - 3/(4(n_1+n_2)-9)$ to correct small-sample bias.
- **Cliff's delta** $= [\#(x_i>y_j) - \#(x_i<y_j)]/(n_1 n_2)$. *By hand* with $x = (3,4,5)$ and $y = (1,2,4)$: 7 pairs are greater, 1 is smaller and 1 is a tie, so $\delta = 6/9 = 0.667$, a large effect.
- Standardised effect sizes depend on which variance you divide by (folds, seeds or splits). So always also give the raw difference in metric points.
- The **Bayesian correlated t-test with a ROPE** (Benavoli et al., 2017) defines a *region of practical equivalence*, e.g. ±1 point. It then reports P(A better), P(practically equivalent) and P(B better). In the notebook these were 0.77, 0.22 and 0.01. That summary says more than "p = 0.138, not significant".

### Reporting honestly

| Write | It describes |
|---|---|
| mean ± **SD** | the spread of individual runs |
| mean ± **SE** ($= SD/\sqrt n$) | the uncertainty of the mean (easy to misread) |
| mean with **95% CI** | a range for the true mean; use it to support "better than" claims |

- Always say which of these you used, over what (seeds, folds, bootstrap) and how many runs.
- **Round to the uncertainty**: 0.87654 ± 0.0123 becomes 0.877 ± 0.012.
- **Bold** a result only when it is supported by a test, or mark every result that is not significantly worse than the best. In the notebook, 41 of 60 non-best entries were statistically tied with the winner of their row.
- **Generate the results text from code**, so that the numbers in the text and the tables can never disagree.

**The statistical sins**:
- **p-hacking**: trying analyses until p < 0.05. In the notebook this produced "significant" results in 14.2% of experiments with no real effect.
- **HARKing**: Hypothesising After the Results are Known.
- **Cherry-picking** seeds or datasets: comparing the best seed with the baseline's average invented a +0.77-point gain for an identical method.
- Using the naive CV t-test, or running many tests without correction.

---

## Which statistical test do I use?

Start from **how your numbers were produced**. Then pick the row that matches.

| Your situation | What you compare | Recommended test / method | Effect size to report | Notebook |
|---|---|---|---|---|
| Planning, before any data | how many test items or users you need | **power analysis** (two-proportion formula, or McNemar's formula for a shared test set); or the minimum detectable effect | the smallest effect of interest (SESOI) | 02 §4 |
| 2 trained models, **one fixed test set**, accuracy | per-item right/wrong | **McNemar** (exact binomial if $b+c$ is small, otherwise χ² with continuity correction) | accuracy difference + paired bootstrap CI | 03 §2.4 |
| 2 trained models, one fixed test set, **any metric** (F1, AUC, BLEU, rubric score) | per-item scores | **paired bootstrap CI** of the difference, or a **permutation (sign-flip) test** | metric difference + CI | 03 §2.6–2.7 |
| One model, one test set | a single metric | **bootstrap CI** (percentile or BCa) | the metric + CI | 03 §2.5 |
| 2 learning algorithms, **one dataset, cross-validation only** | fold scores on the *same* folds | **corrected resampled t-test** (repeated k-fold), or **5×2cv t-test / combined F-test**. **Never** the naive paired t-test | mean difference + corrected CI; $d_z$ with care | 03 §2.1–2.3 |
| Same as above, but you want "how likely is A better by a margin that matters?" | fold scores | **Bayesian correlated t-test + ROPE** | P(A better), P(equivalent), P(B better) | 03 §6 |
| 2 methods, **many datasets** | one score per dataset | **Wilcoxon signed-rank** across datasets + win/tie/loss count | median difference; Cliff's delta | 03 §3 |
| **Many methods, many datasets** | ranks per dataset | **Friedman** (or Iman–Davenport) then **Nemenyi** (all pairs) or **Holm vs a control**; draw a **CD diagram** | average ranks | 03 §3 |
| 2 **independent** groups of runs (different seeds *and* splits, nothing shared), roughly normal | run scores | **Welch's t-test** | Cohen's d / Hedges' g + CI | [02_Data_Analysis/08_statistics](../../02_Data_Analysis/08_statistics.ipynb), 03 §5 |
| 2 independent groups, skewed or ordinal | run scores or ratings | **Mann–Whitney U** | Cliff's delta | [14_Mathematics/04_statistics](../../14_Mathematics/04_statistics.ipynb), 03 §5 |
| **Several hypotheses at once** (a family of claims) | a list of p-values | **Holm** for confirmatory claims (controls FWER); **Benjamini–Hochberg** for exploratory screening (controls FDR) | report $m$ and the adjusted p | 03 §4 |
| **Online experiment**, users randomised to A/B | conversion or mean per user | **two-proportion z-test / t-test**, fixed sample size (no peeking), or a Bayesian A/B | lift + CI | [03_Machine_Learning/11_ab_testing](../../03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb) |
| **Human annotation reliability**, 2 annotators | labels | **Cohen's kappa** (weighted for ordinal labels) | κ | 02 §6.3 |
| Human annotation, **3+ annotators or missing ratings** | labels on any scale | **Krippendorff's alpha** | α (≥ 0.80 reliable) | 02 §6.4 |
| Observational data (logs, past decisions), causal question | treated vs untreated | not a simple test: use **causal inference** (matching, difference-in-differences, uplift) | average treatment effect + CI | [03_Machine_Learning/10_causal_inference](../../03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb) |

Three rules that sit above the table:
1. **Pair whenever the design is paired.** Same folds, same seeds or same test items mean you test the *differences*.
2. **Decide the test, α, the correction and the SESOI before you look at the results.**
3. **Report estimate + uncertainty + test name + statistic and df + p**, and report the non-significant results as clearly as the significant ones.

---

## Part 4 · Reproducibility and research code (notebook 04)

### Three levels of "the same result"

**Repeatable** ⊂ **reproducible** ⊂ **replicable**:
- **Repeatable**: the same team and setup get the same result again.
- **Reproducible**: a different team gets it with *the same code and data*.
- **Replicable**: a different team gets it with *a new implementation or new data*.

Terminology varies between fields, so define the terms you use. Well-known warnings include Henderson et al. (2018) on seed variance in deep RL, Gundersen & Kjensmo (2018) on how few papers share code, and Kapoor & Narayanan (2023) on leakage in ML-based science.

### Seeds and determinism

A pseudo-random number generator (**PRNG**) produces a sequence that looks random from a starting value called the **seed**. The same seed gives the same sequence. Python's `random`, NumPy and PyTorch each have their **own** generator, so seeding one does not seed the others.

- Prefer **local generators**: `rng = np.random.default_rng(seed)`, and `SeedSequence.spawn` for parallel workers.
- `PYTHONHASHSEED` controls the order in which a set of strings is iterated. It must be set *before* Python starts. Better still, use `sorted(...)`.
- In PyTorch, enable the determinism flags (`torch.use_deterministic_algorithms(True)`, `cudnn.benchmark = False`) and seed the DataLoader workers.
- **Some things are still not guaranteed**:
  - Floating-point addition is not associative: $(0.1+0.2)+0.3 \ne 0.1+(0.2+0.3)$.
  - GPU reductions add numbers in a scheduling-dependent order.
  - Hardware, numbers of threads, TF32 and library versions all change the low-order bits.
  - Tiny differences grow during long training.

  So **report the variance over several seeds**. **A seed is not a hyper-parameter**: choosing the best one is selective reporting.

### Environment, layout, configs and tracking

| Tool (weakest → strongest) | What it records |
|---|---|
| requirements with ranges | direct dependencies only; a future install can drift |
| pinned requirements, `pip freeze` | exact versions |
| lock files (`pip-tools`, `uv.lock`, `poetry.lock`, `conda-lock`) | the full resolved dependency tree, with hashes |
| conda `environment.yml` | also Python and non-Python libraries (CUDA, MKL) |
| Docker image | the whole operating system, libraries and code (the GPU driver still comes from the host) |

- **Project layout**: raw data is read-only, everything in `processed/`, `outputs/` and `paper/figures/` is generated by code, source code lives in `src/`, and **one command produces each result**.
- **Configs**: put every setting that changes a result in a YAML file, allow overrides like `model.C=0.5 seed=1` (Hydra style), and **reject unknown keys**, which catches typos.
- **Experiment tracking**: record every run's parameters, metrics, artifacts and metadata (time, code commit, environment). Use a JSON/CSV tracker or MLflow. Every number in a thesis should trace back to a run. Never log hostnames, user names or home paths.

### Data, documentation and sharing

- A **checksum** (SHA-256) is a fingerprint of a file. Changing one value in one of 569 rows produced a completely different hash. Keep a manifest in `sha256sum` format. DVC automates this. Note that a file hash covers bytes, not meaning: line endings or column order change it.
- **Datasheets for Datasets** (Gebru et al.) answer questions in seven groups: motivation, composition, collection, preprocessing and labelling, uses, distribution, maintenance. **Model Cards** (Mitchell et al., 2019) describe the model: details, intended use, factors, metrics, evaluation and training data, quantitative analyses, ethics, caveats. Generate both from code so they never go out of date.
- **Sharing**:
  - A **licence** (MIT, Apache-2.0, BSD-3-Clause, GPL-3.0; CC BY 4.0 for data and text). Without one, nobody may legally reuse public code.
  - A **DOI** (for example via Zenodo) and a `CITATION.cff` file.
  - The Hugging Face Hub for models and datasets.
  - A filled **reproducibility checklist** (for example the NeurIPS paper checklist, answered Yes/No/NA with a pointer to the relevant section).
- **Reproducing a paper**: fix a **tolerance** in advance (the notebook used ±1 point), run several seeds when the paper's seed is unknown, probe each unstated choice (scaling, the value of C, the meaning of "±"), and document every discrepancy.

---

## Part 5 · Paper writing and publishing (notebook 05)

### The anatomy of a paper

**IMRaD** stands for Introduction, Methods, Results and Discussion. The ML-paper variant:

| Section | Reader's question | Typical length (8–9 page paper) |
|---|---|---|
| Title + abstract | should I read this? | ~200 words |
| Introduction | what problem, why it matters, what is new? | ~1 page, ending in **contribution bullets** |
| Related work | how does this differ from what exists? | 0.5–1 page, **by theme, with contrast** |
| Method | could I re-implement it? | 1.5–2.5 pages |
| Experimental setup | datasets, baselines, metrics, protocol, compute | ~1 page |
| Results | what happened, with what uncertainty? | 1.5–2 pages |
| Discussion / limitations | what does it mean, and when does it fail? | 0.5 page |
| Conclusion; ethics / broader impact; references; appendix | what to remember; who could be helped or harmed | |

- **Title**: about 8–15 words, containing the key terms and ideally the finding. Avoid padding like "A novel approach".
- **Abstract, in four moves**: problem, gap, what we do, result plus implication. Include at least one concrete number, and update it last.
- **Introduction**: problem → gap → this paper → contributions.
- **Clear writing**: use the active voice, define terms before you use them, use one name per concept, keep notation consistent, prefer numbers to adjectives, and use "significant" only with a named test.
- **Mathematics**: scalars are italic, vectors bold lowercase, matrices bold uppercase. Define every symbol, punctuate equations as part of sentences, number only the equations you refer to, and **check that the formula matches the code**.
- **Figures**: draw at the final size (one column ≈ 3.25–3.5 in) with 8–10 pt fonts. Use a colour-blind-safe palette such as **Okabe–Ito**, *plus* markers or line styles. Save as vector PDF with embedded TrueType fonts (`pdf.fonttype = 42`), and **say in the caption what the error bars are**.
- **Tables**: generate them with `df.to_latex` using booktabs rules, put units and the direction (↑/↓) in the header, and state the uncertainty and number of runs in the caption.
- **LaTeX, BibTeX and Overleaf**: use the venue's current template and one `.bib` file. With natbib, `\citet` gives the textual form "Vaswani et al. (2017)" and `\citep` the parenthetical form. Lint the source for missing citations, which appear as "[?]" in the PDF.
- **AI writing tools**: they cannot be authors, you are responsible for every word and reference, disclose your use where the venue asks, never trust a generated citation, and never paste a confidential submission you are reviewing into one.

### Publishing

- In ML, **conferences dominate**: NeurIPS, ICML, ICLR, AAAI, IJCAI, ACL/EMNLP, CVPR/ICCV/ECCV, KDD. They have fixed deadlines, one review round with a rebuttal, and strict page limits. **Journals** (JMLR, TMLR, TPAMI) have rolling submission and several rounds of revision.
- **Judging venue quality**: use CORE rankings, SJR quartiles, the h5-index and your institution's list. Beware of **predatory venues** that offer fast acceptance for a fee.
- **Double-blind anonymisation**: no names, no "our previous work", no personal repository links, no acknowledgements, clean PDF metadata, and delete LaTeX comments before posting to arXiv. Cite your own earlier work in the third person.
- **Reviewers judge** originality, significance, soundness, clarity, reproducibility, related work, limitations and ethics. In a **rebuttal**, answer the most important concerns first, prefer new evidence to arguments, concede valid points, and promise only changes you will actually make.
- **After acceptance**: prepare the camera-ready version (de-anonymised, with the promised changes), a poster (readable from 3 m, one main figure), a talk (about one slide per minute), and consider **open access** (gold or green).

### The thesis and integrity

- **Thesis chapters**: front matter (including the declaration of originality), introduction (RQs and contributions), literature review (much longer than in a paper), methodology, one results chapter per study or RQ, discussion with threats to validity, conclusion (answer every RQ), references and appendices.
- **Working with your supervisor**: agree expectations early, send an agenda and results before each meeting, send drafts early and often, and keep a research log.
- **The defence or viva**: prepare a one-sentence answer and a 30-second answer to "what is your contribution?".
- **Plagiarism** includes verbatim copying, patchwriting, and using figures, code or data without credit. **Text recycling** includes duplicate publication and salami slicing. A similarity score from a checker (Turnitin, iThenticate) is evidence for a person to interpret, not a verdict.
- **Authorship**: authors made a substantial contribution and take responsibility for the paper (the ICMJE criteria; the CRediT taxonomy lists 14 contributor roles). In ML the first author usually did most of the work and the last author is often the supervisor. Agree the order early.

---

## Part 6 · A research project end to end (notebook 06)

The capstone runs the full cycle on one question: *does class-balanced logistic regression improve minority (fraud) recall, beyond simply moving the decision threshold?* The steps, in order:
1. **RQ and hypotheses.** H1: recall of T vs B1. H2: precision. H3: PR-AUC. H4: recall of T vs A1. All two-sided at α = 0.05 with Holm correction, and a **SESOI** of 0.05 recall.
2. **Literature.** He & Garcia (2009) on imbalanced data; Elkan (2001), who showed that cost-sensitive decisions are thresholds on calibrated probabilities; van den Goorbergh et al. (2022), who found that imbalance corrections miscalibrate risk; Saito & Rehmsmeier (2015), who recommend PR curves on imbalanced data; and Dietterich and Nadeau & Bengio on CV tests.
3. **A pre-registered plan** in YAML, locked with a SHA-256 hash that is re-checked at the end.
4. **The design.** Four conditions:
   - B0, a dummy classifier (the sanity floor);
   - B1, unweighted logistic regression with threshold 0.5;
   - T, class-weighted logistic regression with threshold 0.5;
   - A1, the **same fitted model as B1** with the threshold set to the fraud rate, an ablation that isolates the threshold effect.

   All four run with 10 seeds × nested 5×3 CV, 1,300 fits in total.
5. **Sanity checks before any statistics**: B0's recall is close to the fraud rate, and A1's PR-AUC is identical to B1's.
6. **Tests**: the corrected resampled t-test, which here shrinks t by $\sqrt{13.5} \approx 3.67$ because $(1/50 + 1/4)/(1/50) = 13.5$, then Holm, bootstrap CIs and Wilcoxon, each checked against SciPy.
7. **Figures, a LaTeX table** and an **auto-generated results paragraph**, with all 21 numbers checked against the computed results.
8. **The decision**:
   - H1: recall rose by +0.356 (significant).
   - H2: precision fell by −0.739.
   - H3: PR-AUC fell by −0.053, so weighting made the *ranking* slightly worse.
   - H4: T − A1 = −0.026, Holm p = 0.23, not significant.

   The pre-registered rule therefore says **do not retrain with weights**. A naive t-test would have called H4 significant.
9. **Exploratory, labelled as such**: the weighted model's mean predicted probability was 0.324 against a true fraud rate of 0.044, a badly miscalibrated model.
10. **Threats to validity** (synthetic data, one model family, dependent folds) and a **reproducibility package** (config, seeds, environment, results, figures, model card, manifest), plus a re-run of one stored fold that matched exactly.
11. **Handoff to the product team**: a cost-based threshold, a decision memo, then shadow mode → A/B test → rollout.

> **Why it matters.** The study's most important result is a *negative* one: the expensive fix was no better than the free one. Only a pre-registered, correctly analysed design with a strong cheap baseline could show that.

---

## Thesis / paper checklist

Tick every item before you submit. Each one is something examiners and reviewers check.

**Question and literature**
- [ ] One main RQ (plus 2–4 sub-questions) that passes FINER and names the data, comparison and metric.
- [ ] Hypotheses (H0/H1) and the contribution bullets are written down before the experiments.
- [ ] Search strings, databases and search dates are recorded; snowballing is done; the review is organised **by theme** and ends at the gap.
- [ ] For a systematic review: a protocol, PRISMA 2020 counts that add up, and screening agreement (kappa).
- [ ] Every reference has been read, checked and points to the published version; none was generated by an AI tool and left unchecked.

**Design**
- [ ] The test set was locked before development; nested CV is used where tuning happens; group or time splits are used where rows are not independent.
- [ ] Trivial, classical and re-run state-of-the-art baselines are included, **with equal tuning budgets** (and the budget is reported).
- [ ] An ablation table exists ("−X", and "only X" when components overlap).
- [ ] A seed list was fixed in advance (≥ 3–5, ideally 10), with **all** runs reported, baselines included.
- [ ] A power analysis or minimum detectable effect is stated for the test-set size.
- [ ] All preprocessing is inside the pipeline (no leakage), and duplicates were removed across splits.
- [ ] A pre-registered analysis plan exists (test, α, correction, SESOI, stopping rule); deviations and exploratory analyses are labelled.
- [ ] Human evaluation, if any, is blind and randomised, has guidelines, and reports kappa or Krippendorff's alpha.

**Statistics and reporting**
- [ ] The test matches the design (see the decision table above); there is no naive t-test on CV folds.
- [ ] Multiple comparisons are corrected (Holm or BH) and $m$ is reported.
- [ ] Every claim gives estimate + CI + test + statistic/df + p, plus an effect size.
- [ ] Captions say whether ± or error bars are SD, SE or CI, and over how many runs.
- [ ] Numbers are rounded to their uncertainty; bold marks only differences that a test supports.
- [ ] Results text and tables are generated from code; non-significant results are reported too.
- [ ] Limitations are given under all four threats to validity (internal, external, construct, statistical conclusion).

**Reproducibility**
- [ ] The code is in version control, and each run records its commit hash.
- [ ] The environment is pinned (pinned requirements or a lock file, plus the Python version).
- [ ] There is one config per experiment, and one command per table or figure.
- [ ] Every reported number is in the experiment tracker.
- [ ] Data checksums are recorded, along with a download script or the data itself (if the licence allows).
- [ ] A datasheet and a model card exist.
- [ ] A licence, a `CITATION.cff` file and a DOI or tagged release exist.
- [ ] The venue's reproducibility checklist is filled in.
- [ ] The package was tested by re-running at least one stored result from a clean environment.

**Writing and submission**
- [ ] The title contains the key terms; the abstract has all four moves and a number; the introduction ends with contribution bullets.
- [ ] Every symbol is defined; the formulas match the code.
- [ ] Figures are drawn at final size, colour-blind safe with markers, in vector PDF with embedded fonts.
- [ ] The paper uses the venue's current template and is within the page limit; the LaTeX lints clean (no "[?]" or "??").
- [ ] It is anonymised for double-blind review (text, links, PDF metadata, LaTeX comments).
- [ ] There is an ethics / broader-impact statement; ethics approval and consent are documented if people were involved.
- [ ] AI-tool use is disclosed as the venue and university require.
- [ ] A similarity check was run, with no patchwriting and no undisclosed text recycling.
- [ ] Authorship and author order were agreed with all co-authors and the supervisor.
- [ ] For a thesis: the university template and declaration are used, every RQ is answered in the conclusion, and you have rehearsed defence answers.

---

## Glossary

- **Ablation study**: removing or replacing one component at a time to measure its own contribution.
- **α (significance level)**: the accepted false-positive rate, usually 0.05.
- **Annotated bibliography**: a list of paper summaries without synthesis (not a literature review).
- **Applied research**: research that solves a practical problem.
- **Baseline**: a reference method that a new method must beat (trivial, classical, or prior state of the art).
- **Basic research**: research aimed at understanding why something happens.
- **BCa interval**: a bias-corrected and accelerated bootstrap CI.
- **Benchmark overfitting**: an upward bias from selecting ideas on a reused public test set.
- **Benjamini–Hochberg (BH)**: a step-up correction that controls the false discovery rate.
- **BibTeX**: the plain-text reference format used with LaTeX.
- **Blocking**: comparing treatments within groups of similar units (in ML, the same folds or the same test set).
- **Bonferroni correction**: multiplying each p-value by the number of tests.
- **Bootstrap**: estimating uncertainty by resampling the data with replacement.
- **Checksum (SHA-256)**: a fingerprint of a file that changes if even one byte changes.
- **Cliff's delta**: P(x > y) − P(x < y), a non-parametric effect size.
- **Cohen's d**: a mean difference divided by the pooled standard deviation.
- **Cohen's kappa**: chance-corrected agreement between two annotators.
- **Confidence interval (CI)**: a range produced by a procedure that captures the true value in, say, 95% of repetitions.
- **Confounder**: a variable affecting both treatment assignment and the outcome.
- **Construct validity**: whether the metric measures what you claim it measures.
- **Contamination**: test items leaking into a model's (pre-)training data.
- **Contribution statement**: a list of exactly what is new in the work.
- **Corrected resampled t-test**: Nadeau and Bengio's CV t-test, which inflates the variance by $n_{test}/n_{train}$.
- **Critical-difference (CD) diagram**: a plot of average ranks with bars joining methods that are not significantly different.
- **Datasheet for datasets**: a standard document describing a dataset.
- **Dataset shift**: a difference between the training and deployment distributions (covariate shift, label shift, concept drift).
- **Discordant pairs**: test items where exactly one of two models is right.
- **DOI**: a permanent identifier for a paper, dataset or software release.
- **Double-blind review**: neither the authors nor the reviewers know each other's identity.
- **Dual use**: research that can be used both to help and to harm.
- **Effect size**: how big a difference is, as opposed to whether it is detectable.
- **Experiment tracking**: automatically recording the parameters, metrics and artifacts of every run.
- **External validity**: whether a result generalises beyond the studied data.
- **Factorial design**: varying several factors in all combinations, to estimate main effects and interactions.
- **FDR**: the expected share of false discoveries among the rejected hypotheses.
- **FINER**: Feasible, Interesting, Novel, Ethical, Relevant, the criteria for a research question.
- **Friedman test**: a rank-based test of whether $k$ methods differ across $N$ datasets.
- **FWER**: the probability of at least one false positive in a family of tests.
- **HARKing**: Hypothesising After the Results are Known.
- **Holm correction**: a step-down FWER correction that is never less powerful than Bonferroni.
- **Hypothesis (H0 / H1)**: a testable statement of no effect / of an effect.
- **IMRaD**: Introduction, Methods, Results and Discussion, the standard paper structure.
- **Interaction effect**: when one factor's effect depends on the level of another.
- **Internal validity**: whether the treatment really caused the observed difference.
- **IRB / research ethics committee**: the body that approves studies involving people.
- **Krippendorff's alpha**: an agreement measure for any number of annotators, any scale, and missing data.
- **Leakage**: information unavailable at prediction time influencing training or model selection.
- **Literature review matrix**: a table with one row per paper and one column per attribute, used to synthesise.
- **Lock file**: a file pinning the full resolved dependency tree.
- **McNemar's test**: a test of two models on the same test set, using the discordant items.
- **Meta-analysis**: the statistical pooling of results from several studies.
- **Minimum detectable effect (MDE)**: the smallest difference a given sample size can reliably detect.
- **Model card**: a standard document describing a trained model.
- **Nemenyi test**: a post-hoc test comparing all pairs of average ranks against a critical difference.
- **Nested cross-validation**: an inner CV loop for tuning inside an outer CV loop for scoring.
- **Observational study**: a study that records what happened without assigning treatments.
- **p-value**: P(data at least this extreme | H0).
- **Paired bootstrap**: resampling the same items for both models to get a CI for their difference.
- **Patchwriting**: copying a passage and changing a few words; it counts as plagiarism.
- **Permutation test**: building the null distribution by randomly swapping labels or outputs.
- **p-hacking**: trying analyses until p < 0.05.
- **Power**: the probability of detecting an effect that really exists (1 − β).
- **Power analysis**: computing the sample size needed for a target power.
- **Pre-registration**: fixing hypotheses and the analysis plan before seeing the results.
- **Preprint**: a paper posted publicly before (or without) peer review, for example on arXiv.
- **PRISMA 2020**: the reporting guideline and flow diagram for systematic reviews.
- **PRNG / seed**: a pseudo-random number generator / its starting value.
- **Randomisation**: assigning treatments by chance so that confounders balance out.
- **Rebuttal**: the authors' response to the reviewers.
- **Repeatable / reproducible / replicable**: same team and setup / other team with the same code and data / other team with a new implementation or data.
- **Research gap**: an important question that the existing literature has not answered.
- **Research question (RQ)**: the precise question a study is designed to answer.
- **ROPE**: a region of practical equivalence, used in Bayesian comparisons.
- **SESOI**: the smallest effect size of interest, below which a difference does not matter.
- **Simpson's paradox**: a trend that reverses when the data are combined across groups.
- **Snowballing**: following references backward and citations forward from seed papers.
- **Standard deviation (SD) / standard error (SE)**: the spread of individual values / the uncertainty of their mean ($SD/\sqrt n$).
- **Statistical conclusion validity**: whether the statistical inference is sound.
- **Systematic review**: a literature review following a pre-defined, reproducible protocol.
- **Three-pass method**: Keshav's skim / read / re-derive approach to reading a paper.
- **Threats to validity**: the ways a conclusion could be wrong (internal, external, construct, statistical conclusion).
- **Type I / type II error**: a false positive / a false negative.
- **Wilcoxon signed-rank test**: a non-parametric paired test, for example of two methods across datasets.
- **5×2cv test**: Dietterich's test based on five repetitions of 2-fold CV.
