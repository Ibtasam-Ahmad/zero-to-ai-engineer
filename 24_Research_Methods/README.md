# Research Methods for AI & Data Science

Training a model that scores a bit higher is easy. Showing that it **really** is better, in a way a thesis examiner, a paper reviewer or a sceptical manager will accept, is much harder. This module teaches that second skill, from start to finish. You pick a sharp research question and review the literature. You design a fair experiment, test whether the gain is real, make the result reproducible, write it up and get it published. It is part of the **optional, university-level fundamentals track** and is written at MS-thesis / MPhil level, but it starts from zero: every term is explained the first time it appears.

**Who needs it.**
- **MS / MPhil students writing a thesis** (and BS students doing a final-year project): proposal, literature review, methodology chapter, results with proper statistics, the defence.
- **Anyone who wants to publish** a paper at a workshop, conference or journal.
- **Industry researchers, applied scientists and data scientists** who must prove that a new model, feature or prompt is genuinely better before a product team acts on it. "It scored 0.01 higher on one run" is not evidence.

**How it complements the rest of the repo.** Other modules teach the tools. This module puts them together into a full *research workflow* and adds the parts that are specific to comparing ML models:

| Module | What it already teaches | What this module adds |
|---|---|---|
| [`02_Data_Analysis/08_statistics`](../02_Data_Analysis/08_statistics.ipynb) | general statistics for data science: distributions, hypothesis tests, p-values, confidence intervals | tests **made for comparing ML models**: why the usual t-test on CV folds is wrong, the corrected resampled t-test, McNemar, the paired bootstrap, Friedman + Nemenyi |
| [`14_Mathematics/04_statistics`](../14_Mathematics/04_statistics.ipynb) | the maths behind estimation, CIs, the t-test, effect sizes, Bonferroni/BH, the bootstrap, Bayesian inference | how to **use** these in a thesis or paper: power analysis for test sets, Holm vs BH in a results table, effect sizes for fold/seed data, the Bayesian correlated t-test with a ROPE |
| [`03_Machine_Learning/06_model_evaluation`](../03_Machine_Learning/06_model_evaluation/) | metrics, cross-validation, nested CV, hyper-parameter tuning, champion vs challenger | the **experiment design** around evaluation: baselines, ablations, equal tuning budgets, seeds and variance, group/time splits, threats to validity, pre-registration |
| [`03_Machine_Learning/11_ab_testing`](../03_Machine_Learning/11_ab_testing/) | **online** experiments with real users: power, peeking, Bayesian A/B, bandits | the **offline** research study that comes *before* an A/B test, and the same ideas (randomisation, power, multiple testing) applied to models and benchmarks |
| [`15_MLOps`](../15_MLOps/) experiment tracking ([MLflow](../15_MLOps/01_experiment_tracking/01_mlflow.ipynb), [W&B](../15_MLOps/01_experiment_tracking/02_wandb.ipynb), [DVC](../15_MLOps/02_data_versioning/01_dvc.ipynb)) | the production tools for tracking runs and versioning data | the **research question behind them**, "can someone else get my numbers?": seeds, determinism, configs, checksums, model cards, a reproducibility package, reproducing a paper |
| [`19_AI_Ethics_and_Safety`](../19_AI_Ethics_and_Safety/) | bias, privacy, responsible AI, regulation, copyright | **research ethics**: plagiarism and patchwriting, authorship, consent and ethics approval (IRB), dual use, and the responsible use of AI writing tools |

**When to take it** (see [LEARNING_PATH.md](../LEARNING_PATH.md)):

```
 Stage 3 Data analysis --> Stage 4 Maths --> Stage 5 Classical ML
                                                    |
                                  EARLIEST START ---+
                                                    v
                          24_Research_Methods 01 -> 02 -> 03 -> 04 -> 05 -> 06
                                                    |
                    Stages 6-11 (any order, in parallel is fine)
                                                    v
                      IDEALLY FINISH BEFORE --> Stage 12 Capstone projects
```

- **Earliest:** right after **Stage 5 (classical machine learning)**, once you can train, cross-validate and evaluate a scikit-learn model. Notebooks 02, 03 and 06 assume that.
- **Ideally:** finish it **before the capstone projects (Stage 12)**, so your projects come with seeds, baselines, an ablation and honest error bars. Do the same before you start a thesis proposal.
- Notebook 01 (research questions and the literature) needs only Python and pandas, so a thesis student can read it at any time.

---

## The whole topic explained simply

Research means finding out something new **in a way that other people can check**. A good study is like a fair cooking contest. Every cook gets the same ingredients, the same oven and the same time, and the judges taste the dishes without knowing who made which. In ML this means the same data split, the same tuning effort and the same number of runs for every model. Luck matters a lot. The same model trained twice can score differently, like a batsman who makes 80 one day and 20 the next, so one run proves nothing. Statistics is the referee that tells you whether a difference is bigger than luck. Reproducibility is like a precise recipe ("250 g flour, 180 °C, 35 minutes") that works in anyone's kitchen, not only yours. Finally, writing the paper is like a news article: the headline and the first paragraph tell the whole story, and the details come after.

**Tiny worked example.** Two spam filters are tested on the same 100 e-mails. They agree on 90 of them, so those 90 tell us nothing about which filter is better. On the other 10, filter A is right 7 times and filter B 3 times. Is A better? If both filters were equally good, each of those 10 disagreements would be a coin flip. A split at least as uneven as 7–3 then happens with probability

$$2 \times \frac{\binom{10}{7}+\binom{10}{8}+\binom{10}{9}+\binom{10}{10}}{2^{10}} = 2 \times \frac{120+45+10+1}{1024} = 2 \times \frac{176}{1024} \approx 0.34 .$$

A 34% chance of happening by luck is **not** convincing. You need more e-mails before you claim that A wins. This is McNemar's test (notebook 03), and the question "how many e-mails do I need?" is power analysis (notebook 02).

---

## Who is this for, prerequisites and time

| | |
|---|---|
| **Who** | MS/MPhil thesis students, BS final-year-project students, anyone preparing a paper, and industry data scientists, ML engineers and applied scientists who must defend a "model B is better" claim; also interview prep for research and applied-scientist roles |
| **Must know first** | [Python basics](../01_Python/01_basic.ipynb), [pandas](../02_Data_Analysis/03_pandas.ipynb), [matplotlib](../02_Data_Analysis/04_matplotlib.ipynb), [your first ML model](../03_Machine_Learning/00_start_here_your_first_ml_model.ipynb), [model evaluation and cross-validation](../03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb), [logistic regression](../03_Machine_Learning/01_supervised/02_logistic_regression.ipynb) |
| **Helpful** | [Statistics for data science](../02_Data_Analysis/08_statistics.ipynb), [statistics for ML](../14_Mathematics/04_statistics.ipynb), [maths notation bridge](../14_Mathematics/00_start_here_math_notation_bridge.ipynb), [pipelines and leakage](../03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb), [A/B testing](../03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb), [MLflow](../15_MLOps/01_experiment_tracking/01_mlflow.ipynb) |
| **Time needed** | about 14–18 hours for all 6 notebooks, plus the practice problems |
| **Runs on** | CPU only, no API key, no internet. Uses numpy, pandas, matplotlib, SciPy and scikit-learn (plus PyYAML, and PyTorch and MLflow in notebook 04); statsmodels is used only for optional cross-checks. All papers and records are made up, and every file goes to a temporary folder that is deleted at the end |

---

## Study order

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Research methodology and literature review](01_research_methodology_and_literature_review.ipynb) | Turn a vague idea into a sharp, FINER-checked research question, find and read the literature, build a review matrix, find the gap and plan the proposal | 2–3 h |
| 02 | [Experiment design for ML](02_experiment_design_for_ml.ipynb) | Run a fair experiment: controlled variables, blocking, baselines, ablations, equal tuning budgets, seeds, power analysis, threats to validity and human evaluation | ~3 h |
| 03 | [Statistical significance and reporting](03_statistical_significance_and_reporting.ipynb) | Decide whether a gain is real with the right test (corrected t-test, McNemar, bootstrap, Friedman + Nemenyi, Holm/BH) and report it honestly | 3–4 h |
| 04 | [Reproducibility and research code](04_reproducibility_and_research_code.ipynb) | Make every number re-creatable: seeds, environments, configs, tracking, checksums, datasheets, model cards, licences and a reproduction case study | 2–3 h |
| 05 | [Paper writing and publishing](05_paper_writing_and_publishing.ipynb) | Write the paper or thesis (IMRaD, abstract formula, figures, LaTeX tables, BibTeX), then get it through peer review, the rebuttal and the defence | 2–3 h |
| 06 | 🏭 [Industry project: a research project end to end](06_industry_running_a_research_project_end_to_end.ipynb) | One complete, pre-registered study (fraud-like data, class weights vs threshold moving) from question to decision memo | ~2 h |

---

## The notebooks one by one

### 01 · Research methodology and literature review

*Explained simply.* Research starts with **one sharp question** and with knowing what other people already found, so you do not spend months repeating them. A **literature review** means reading what is known and spotting what is missing. That missing spot is the **research gap**, and your thesis fills it. Finding papers is detective work: one good paper points back to the older papers it cites and forward to the newer papers that cite it. Think of reading every review of a phone before you buy one: you learn what is good, what is weak, and what nobody has tested yet.

*Tiny example.* The notebook's made-up literature matrix of 10 papers, cross-tabulated by theme and language:

| theme | English | Hindi | Multilingual | Swahili | Urdu |
|---|---|---|---|---|---|
| Classical ML | 1 | 0 | 0 | 1 | 0 |
| Augmentation | 0 | 0 | 0 | 1 | 1 |
| Transformers | 0 | 0 | 1 | 0 | 2 |
| LLM prompting | 1 | 1 | 1 | 0 | **0** |

11 of the 20 cells are empty, but only one is an interesting gap: **LLM prompting for Urdu**. So a candidate research question is: "How does few-shot prompting of open LLMs compare with a fine-tuned Urdu BERT for Urdu fake-news detection, under equal compute budgets?"

*You will learn:*
- the types of research (basic/applied, quantitative/qualitative/mixed, empirical/theoretical, exploratory/descriptive/explanatory) and the scientific method;
- the **FINER** criteria (Feasible, Interesting, Novel, Ethical, Relevant), hypotheses, SMART objectives and a contribution statement;
- where to search in 2026 (Google Scholar, Semantic Scholar, arXiv, ACL Anthology, OpenReview, dblp, OpenAlex; Papers with Code shut down in July 2025), Boolean search strings and **snowballing**;
- the **three-pass** reading method, a paper-summary template and red flags of weak evidence;
- the **literature review matrix** in pandas, **PRISMA 2020** flow counts (450 records → 27 included studies), BibTeX and reference managers;
- research ethics (plagiarism, patchwriting, authorship, consent, IRB, dual use, AI writing tools) and the MS/MPhil **proposal** with a Gantt chart.

*Key takeaway:* a literature review **synthesises by theme and ends at a gap**. It is not a list of paper summaries.

### 02 · Experiment design for ML

*Explained simply.* An experiment is a **fair test**: change one thing on purpose, keep everything else the same, and measure the result. In ML, "everything else" means the same data split, the same tuning effort and the same number of runs for every model. Because of random seeds, one run is only one sample, so you run several. You also need **enough test examples**: judging two basketball players on three shots each tells you almost nothing. Think of testing a new fertiliser on tomatoes: both groups get the same sun, water and soil, and only the fertiliser differs.

*Tiny example.* Model A scores 85, 86 and 84 over three seeds (mean 85). Model B is run once and scores 87. A's own scores moved by 2 points just by luck, so B's 2-point lead proves nothing yet. Run B with the same seeds first. The notebook's power analysis shows how big the test set must be to detect a 1-point gain (85% vs 86%) with 80% power at α = 0.05:

| Design | Test examples needed |
|---|---|
| each model on its own independent sample (like an A/B test) | 19,458 per model |
| both models on the **same** test set, disagreeing on 5% of items | 3,923 |
| same test set, disagreeing on 20% of items | 15,696 |

*You will learn:*
- independent, dependent, controlled and **confounding** variables, and why randomisation fixes **Simpson's paradox**;
- blocking (pairing on the same folds) and a real 2³ **factorial design** with interaction effects;
- ML protocols: a locked test set, **nested CV**, `GroupKFold` and `TimeSeriesSplit`, trivial/classical/SOTA **baselines**, **ablation** tables, **equal tuning budgets**, seeds, learning curves and leakage traps;
- **power analysis** and the minimum detectable effect for a given test-set size;
- the four **threats to validity**, benchmark overfitting and dataset shift;
- pre-registration, an analysis plan, human evaluation, **Cohen's kappa** and **Krippendorff's alpha**, and an experiment-plan template.

*Key takeaway:* the comparison must be fair **before** it is analysed. Statistics cannot rescue a biased design.

### 03 · Statistical significance and reporting

*Explained simply.* Statistics answers one question: **is the difference real, or just luck?** The **p-value** says how surprising your result would be if there were really no difference. A **confidence interval** gives a range for the true value, like a weather forecast of "28 to 32 degrees". If you test many things at once, some will win by luck, like buying 20 lottery tickets. Think of a courtroom: the new model is presumed "no better" until the evidence is strong enough, and "not proven" is not the same as "innocent".

*Tiny example.* From the notebook: kNN vs logistic regression over 10×10-fold CV on the same 1,500 examples.

| Test | t | p | Verdict |
|---|---|---|---|
| naive paired t-test on the 100 folds | 5.20 | 0.000001 | "huge win" (wrong) |
| corrected resampled t-test (Nadeau–Bengio) | 1.50 | 0.138 | not significant |

The folds share most of their training data, so the naive test underestimates the variance about 12× (by a factor of 12.1). In a simulation where the two models were truly equal, the naive test declared a "significant" winner **52.5%** of the time instead of 5%.

*You will learn:*
- what a p-value is (and is not), type I/II errors, **effect size vs significance**, and confidence intervals;
- two models on one dataset: the **corrected resampled t-test**, **5×2cv**, **McNemar**, **bootstrap CIs** (accuracy, F1, AUC), the **paired bootstrap** and **permutation tests**, each checked against SciPy/statsmodels;
- many models on many datasets: **Friedman + Nemenyi** and the **critical-difference diagram**;
- **multiple comparisons**: Bonferroni, **Holm** and **Benjamini–Hochberg**;
- effect sizes (Cohen's d, d_z, Hedges' g, Cliff's delta) and the **Bayesian correlated t-test with a ROPE**;
- reporting: SD vs SE vs CI, significant digits, bolding rules, error bars, auto-generated results text, and the statistical sins (p-hacking, HARKing, cherry-picking).

*Key takeaway:* pick the test that matches **how the numbers were produced**, and report the effect size with its uncertainty, not just "p < 0.05".

### 04 · Reproducibility and research code

*Explained simply.* A result is only useful if someone else can get it again. Computers hide many small "random" choices, libraries change between versions, and data files get edited, so the same experiment can quietly give a different answer next month. Reproducibility means writing down **everything that affects a result**: seeds, versions, settings, data fingerprints. Then nobody has to guess. Think of a recipe: "some flour, bake until done" only works in the author's kitchen; "250 g flour, 180 °C, 35 minutes" works in anyone's.

*Tiny example.* Floating-point addition is not associative, so the order of operations matters:

```
(0.1 + 0.2) + 0.3 = 0.6000000000000001
0.1 + (0.2 + 0.3) = 0.6
```

The same numbers summed in four different orders in float32 gave **four different totals**. A GPU that changes the order of additions between runs therefore changes the result slightly, even with perfect seeding. That is why papers should report **variation over several seeds** instead of promising bit-identical numbers.

*You will learn:*
- **repeatable ⊂ reproducible ⊂ replicable**, and famous reproducibility failures in ML;
- seeding Python, NumPy and PyTorch, local generators, `PYTHONHASHSEED`, deterministic PyTorch, and what is **not** guaranteed;
- environment pinning (pinned requirements, lock files, conda, Docker) and recording versions from code;
- a project layout, YAML configs with Hydra-style `key=value` overrides, and **one command per result**;
- experiment tracking (a minimal JSON/CSV tracker, then MLflow), **SHA-256 checksums**, datasheets and model cards generated from code;
- licences, DOIs, `CITATION.cff`, the NeurIPS-style checklist, and **reproducing a paper's number** within a pre-declared tolerance.

*Key takeaway:* every number in your thesis should trace back to a recorded run, from a pinned environment, on data with a known hash.

### 05 · Paper writing and publishing

*Explained simply.* A paper is a short, organised **argument** that your finding is true and useful. It always answers the same questions in the same order: what problem, what was missing, what you did, what you found, how sure you are, and what the limits are. Most readers only read the title, the abstract and the figures, so the main message must be there. After writing, experts (reviewers) check the paper before it is published. Think of a news article: the headline and the first paragraph tell the story, and the details come later.

*Tiny example.* The weak sentence *"Our method was much better."* becomes the strong sentence *"Our method answered 88 of 100 test questions correctly, compared with 84 for the old method."* The second one has numbers, says who did what, and a reader can check it. The **4-sentence abstract formula**:

```
1. Problem   : fraud detectors miss the rare class that matters most.
2. Gap       : class weighting is rarely compared with simply moving the threshold.
3. What we do: we compare both over 10 seeds with nested CV and an ablation.
4. Result    : <the main number with its uncertainty> + what it means.
```

*You will learn:*
- the **IMRaD** structure and its ML-paper variant, with good vs weak examples and a checklist for each section;
- the 4-sentence abstract, the problem → gap → contribution introduction, and clear writing (active voice, defined terms, numbers instead of adjectives);
- writing mathematics, **publication-quality figures** (final size, Okabe–Ito palette plus markers, vector PDF, error bars explained) and LaTeX tables from a DataFrame;
- LaTeX, BibTeX, citation styles and Overleaf, plus responsible use of AI writing tools;
- the publishing pipeline: venue choice and quality, arXiv, double-blind anonymisation, peer review, rebuttals, camera-ready, posters and talks;
- the **thesis** chapters, working with a supervisor, the defence/viva, plagiarism and authorship norms.

*Key takeaway:* write numbers with their uncertainty and a named test; use the word "significant" only for a test you actually ran.

### 06 · 🏭 Industry project: running a research project end to end

*Explained simply.* This notebook runs one complete study, the way a research team in a payments company would. The question: does training a fraud detector to pay more attention to rare fraud cases (**class weighting**) catch more fraud, and is that better than just making the detector more sensitive (**moving the threshold**)? The rules of the test are written down and fingerprinted **before** any model is trained. Then the study is run with 10 seeds and nested CV, tested with the corrected t-test and Holm, and turned into figures, a LaTeX table, a results paragraph and a decision memo. Think of a smoke alarm: making it more sensitive catches more real fires, but it also beeps every time you make toast.

*Tiny example.* Results over 10 seeds × 5 outer folds (synthetic data, 4.4% fraud):

| Condition | Recall | Precision | PR-AUC |
|---|---|---|---|
| B1 unweighted, threshold 0.5 | 0.370 | 0.902 | 0.594 |
| T class-weighted, threshold 0.5 | 0.726 | 0.163 | 0.541 |
| A1 unweighted, threshold = fraud rate | **0.752** | 0.162 | 0.594 |

Weighting doubles recall compared with B1 (H1: +0.356, significant). But simply moving the threshold of the *unweighted* model does just as well (H4: −0.026, Holm p = 0.23, not significant). The pre-registered decision is therefore **do not retrain with weights**. A naive t-test would have called H4 significant (p ≈ 5 × 10⁻⁵) and led to the opposite conclusion.

*You will learn:*
- turning a business question into a research question, four hypotheses and a **smallest effect size of interest (SESOI)**;
- writing a **pre-registered analysis plan** in YAML and locking it with SHA-256;
- designing baselines, a treatment and an **ablation** that isolates one cause (the threshold);
- running 1,300 fits with sanity checks, then corrected t-tests, Holm, bootstrap CIs and Wilcoxon, each checked against SciPy;
- generating figures, a LaTeX table and a **results paragraph from the numbers**, and listing threats to validity;
- building a **reproducibility package** (re-run one fold, verify a manifest) and the research → product handoff (cost-based threshold, shadow → A/B → rollout).

*Key takeaway:* decide the rules first, test against the strongest *cheap* alternative, and let the pre-registered decision rule make the call.

---

## How this connects to the rest of the repo and to real AI systems

- **Model selection at work** uses the same paired tests and bootstrap CIs: see the champion-vs-challenger notebook [model comparison and selection](../03_Machine_Learning/06_model_evaluation/03_industry_model_comparison_and_selection.ipynb).
- **Online experiments** come after the offline study: [A/B testing](../03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb) and the [industry A/B report](../03_Machine_Learning/11_ab_testing/02_industry_ab_test_analysis_report.ipynb).
- **Observational data** (logs, past campaigns) needs causal methods instead of a randomised experiment: [causal inference](../03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb).
- **Regression tables and inference** (OLS, standard errors, diagnostics): [statistical modelling and inference](../02_Data_Analysis/13_statistical_modeling_and_inference.ipynb).
- **LLM evaluation** is experiment design plus statistics: prompts and temperature are factors, benchmark contamination is a threat to validity, and LLM-as-judge needs agreement checks. See [LLM evaluation](../08_LLM/08_evaluation/01_llm_evaluation.ipynb).
- **Leaderboards** (LMArena, MTEB, SWE-bench) report confidence intervals and rank bands: read them like a critical-difference diagram, and remember benchmark overfitting.
- **Tracking and versioning at scale**: [MLflow](../15_MLOps/01_experiment_tracking/01_mlflow.ipynb), [advanced experiment tracking](../15_MLOps/10_advanced_experiment_tracking.ipynb), [DVC](../15_MLOps/02_data_versioning/01_dvc.ipynb), [Git for ML](../20_Git_and_DevOps/02_git_for_ml.ipynb).
- **Ethics, documentation and law**: [responsible AI](../19_AI_Ethics_and_Safety/04_responsible_ai.ipynb), [privacy](../19_AI_Ethics_and_Safety/03_privacy.ipynb), [copyright and AI](../19_AI_Ethics_and_Safety/06_copyright_and_ai.ipynb), [AI regulation](../19_AI_Ethics_and_Safety/05_ai_regulation_compliance.ipynb).
- **Capstones**: re-analyse one of the [projects](../21_Projects/) with seeds, a paired bootstrap and an ablation table. That turns a demo into evidence.
- **Deeper study guide** for this module: [notes/24_Research_Methods.md](notes/24_Research_Methods.md) (includes a "which test do I use?" table and a thesis/paper checklist).

---

## Common beginner mistakes

- **A vague research question** ("Can AI detect fake news?"). It names no data, no metric and no comparison, so nothing can answer it.
- **Comparing with numbers copied from other papers.** Different splits, preprocessing and seeds act as confounders. Re-run the baselines under your own protocol.
- **One run per model, or reporting the best seed.** A single run is one sample, and picking the best seed is cherry-picking.
- **Tuning your method carefully but running the baselines with defaults.** In notebook 02, this made an SVM look +30.9 points better than kNN; with equal budgets the gap was −0.6.
- **A paired t-test on cross-validation folds.** Folds overlap, so the p-values are far too small. Use the corrected resampled t-test or 5×2cv.
- **Running 20 tests and celebrating the one with p < 0.05.** With no real effect at all, that happens 64% of the time. Correct with Holm or BH.
- **Saying "the error bars overlap, so there is no difference"** (or the reverse). It is not a test, and paired designs need a paired test on the differences.
- **`random_state=42` everywhere and calling it reproducible.** That is *repeatable* for one seed. Pin the environment, hash the data, and report several seeds.

---

## Exam / interview quick-revision

1. **What makes a good research question?** → FINER (Feasible, Interesting, Novel, Ethical, Relevant), naming the data, the comparison and the metric.
2. **Literature review vs annotated bibliography?** → A review synthesises papers by theme and points to the gap; a bibliography just lists summaries.
3. **Systematic review vs meta-analysis?** → A systematic review is a reproducible search-and-selection protocol; a meta-analysis statistically pools the results.
4. **What is a confounder?** → A variable that affects both which treatment is used and the outcome, creating a fake or hidden effect.
5. **What is an ablation study?** → Removing or replacing one component at a time to measure its own contribution.
6. **Why nested CV?** → The inner loop tunes and the outer loop scores the whole tuning procedure; the best inner score alone is optimistic.
7. **What is statistical power?** → The probability of detecting an effect that really exists (usually aim for 0.80).
8. **Why is the naive t-test on CV folds wrong?** → The training sets overlap, so the fold scores are correlated and the variance is underestimated.
9. **When do you use McNemar's test?** → Two trained models on the same test set, compared on accuracy using only the items where they disagree.
10. **Friedman + Nemenyi is for?** → Comparing many methods across many datasets using average ranks and a critical difference.
11. **Holm vs Benjamini–Hochberg?** → Holm controls the chance of any false positive (FWER); BH controls the expected share of false discoveries (FDR) and has more power.
12. **What does a p-value of 0.03 mean?** → If H0 were true, data at least this extreme would occur 3% of the time. It is *not* "a 3% chance that H0 is true".
13. **Repeatable vs reproducible vs replicable?** → Same team and setup / a different team with the same code and data / a different team with a new implementation or new data.
14. **What is pre-registration?** → Writing down hypotheses, metrics, tests and decision rules before seeing the results.
15. **What is HARKing?** → Hypothesising After the Results are Known: presenting a post-hoc finding as if it had been planned.

---

## Further reading

**Classic textbooks**
- J. Zobel, *Writing for Computer Science*, 3rd ed., Springer, 2014.
- J. W. Creswell & J. D. Creswell, *Research Design: Qualitative, Quantitative, and Mixed Methods Approaches*, 6th ed., SAGE, 2023.
- D. C. Montgomery, *Design and Analysis of Experiments*, Wiley (randomisation, blocking, factorial designs).
- W. Shadish, T. Cook & D. Campbell, *Experimental and Quasi-Experimental Designs for Generalized Causal Inference*, 2002 (the validity types).
- B. Efron & R. Tibshirani, *An Introduction to the Bootstrap*, Chapman & Hall, 1993.
- N. Japkowicz & M. Shah, *Evaluating Learning Algorithms: A Classification Perspective*, Cambridge University Press, 2011.

**Free papers and resources**
- S. Keshav, "How to Read a Paper", *ACM SIGCOMM CCR*, 2007 (two pages).
- J. Demšar, "Statistical Comparisons of Classifiers over Multiple Data Sets", *JMLR* 7, 2006.
- T. G. Dietterich, "Approximate Statistical Tests for Comparing Supervised Classification Learning Algorithms", *Neural Computation*, 1998.
- S. Raschka, "Model Evaluation, Model Selection, and Algorithm Selection in Machine Learning", arXiv:1811.12808.
- R. Dror et al., "The Hitchhiker's Guide to Testing Statistical Significance in NLP", ACL 2018.
- J. Pineau et al., "Improving Reproducibility in Machine Learning Research", *JMLR*, 2021, and the current NeurIPS paper checklist.
- M. J. Page et al., "The PRISMA 2020 statement", *BMJ*, 2021 (templates at prisma-statement.org).
- R. L. Wasserstein & N. A. Lazar, "The ASA Statement on p-Values", *The American Statistician*, 2016.
- *The Turing Way*, a free community handbook on reproducible and ethical data science.
