# Domain Applications (Electives): how machine learning changes in specialised fields

Most of this repo teaches machine learning on "ordinary" tables, images and text. Real jobs often come with data that has its own shape: rows that sit on a **map**, or rows that are **strings of DNA or protein letters**. This folder shows, with two worked domains, what changes when you move ML into such a field and what stays the same. It is an **optional elective track** at university level (the kind of course a BS/MS in AI or Data Science offers as "Spatial Data Science" or "Bioinformatics"); skip it if you are a beginner, and come back when a project or an interview takes you into one of these areas.

```
                 ordinary ML (rest of the repo)
       features -> model -> metric -> random train/test split
                              |
          what a specialised domain changes
          |                                     |
  GEOSPATIAL (notebook 01)              BIOINFORMATICS (notebook 02)
  rows have a location                  rows are long strings (A,C,G,T)
  - distance on a round Earth           - alignment by dynamic programming
  - nearby rows are alike               - related sequences are alike
  - split by AREA, not at random        - split by FAMILY, not at random
  - metric: error in a new district     - metric: F1 / AUC, E-values
  - privacy: location traces            - privacy: genomes identify people
```

---

## The whole topic explained simply

A domain is a field with its own kind of data, its own vocabulary and its own rules, such as maps, medicine, biology, finance or weather. Machine learning works in all of them, but you cannot just pour the data into a model and hope. Think of a good doctor who moves from one hospital to another: her medical knowledge travels with her, but she still has to learn the local equipment and the local rules. ML is the same: models, losses and optimisers travel; **distance, features, validation and ethics** must be re-thought for each domain.

Three lessons transfer to every domain. First, **split the data the way you will use the model**. If nearby houses or related genes are alike, a random split lets a near-copy of each test row sit in the training set, like letting a student see the exam paper's twin the night before. Second, **choose a metric that matches the real question**: when only 9% of a genome is the thing you are looking for, "91% accuracy" can mean the model found nothing at all. Third, **domain data is often personal**: a location trace shows where you sleep, and your DNA is shared with your relatives and cannot be changed like a password.

**A tiny worked example with real numbers.** Karachi and Lahore are about 6.7 degrees apart in latitude and 7.4 degrees in longitude. Treat the degrees as flat squares: $\sqrt{6.7^2 + 7.4^2} \approx 9.9$ degrees, and at 111.2 km per degree that is about **1,100 km** (the notebook's exact coordinates give 1,103.5 km). Measured properly on the round Earth (the haversine formula) the distance is about **1,033 km**, so the flat method is **7% too long**. And in notebook 01, a house-price model that looked good under a random split (error 0.099) turned out to have error **0.140** on a district it had never seen, about 30% worse than the random split promised. Both mistakes come from ignoring what is special about the domain.

---

## Who is this for / prerequisites / time needed

| | |
|---|---|
| **Who is this for** | Learners who finished the core ML material; BS/MS students taking a spatial data science, GIS, bioinformatics or computational biology elective; anyone preparing for interviews at mapping, delivery, insurance, climate, biotech or health-AI companies |
| **Must know first** | Python: [`01_Python/01_basic.ipynb`](../../01_Python/01_basic.ipynb). Supervised learning: [linear regression](../01_supervised/01_linear_regression.ipynb), [logistic regression](../01_supervised/02_logistic_regression.ipynb), [KNN](../01_supervised/07_knn.ipynb). Validation: [model evaluation and cross-validation](../06_model_evaluation/01_model_evaluation.ipynb) |
| **Algorithms used** | [Graphs and Dijkstra](../../00_AI_Fundamentals/dsa/07_graphs.ipynb) (notebook 01), [dynamic programming / edit distance](../../00_AI_Fundamentals/dsa/09_dynamic_programming.ipynb) (notebook 02) |
| **Helpful extras** | [Gaussian processes](../../14_Mathematics/07_bayesian_ml.ipynb) (section 4), [KD-trees and suffix arrays](../../00_AI_Fundamentals/advanced_algorithms/08_advanced_data_structures.ipynb), [streaming and sketching](../../00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb), [HMMs](../../00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb) (section 11), [PyTorch from zero](../../05_Deep_Learning/00_start_here_pytorch_from_zero.ipynb) and [CNNs](../../05_Deep_Learning/03_cnn.ipynb) (notebook 02) |
| **Biology or GIS background** | None. Every domain term is explained in the notebooks |
| **Time needed** | About 6–7 hours in total (about 3 h + 3–4 h) |
| **Runs on** | CPU only, no API key, no internet. All data is synthetic and generated inside the notebooks; each notebook runs in one to two minutes. geopandas/shapely are optional |

---

## Study order

The two notebooks are independent; take either one alone, or both in this order.

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 01 | [Geospatial machine learning](01_geospatial_machine_learning.ipynb) | Measure distance on a round Earth, build spatial indexes and features, and validate by area instead of at random | ~3 h |
| 02 | [Bioinformatics and sequence ML](02_bioinformatics_sequence_ml.ipynb) | Treat DNA and proteins as text: align them, sketch them, search them, decode them with HMMs, classify them with a 1-D CNN, and protect the people behind them | ~3–4 h |

---

## The notebooks one by one

### 01 · Geospatial Machine Learning

*Explained simply.* Much data has a hidden column: **where** it happened. Latitude and longitude are angles on a ball, not kilometres, so ordinary distance formulas give wrong answers, worst far from the equator and across the ±180° line. Nearby places have similar values (**spatial autocorrelation**), which helps prediction but fools a random train/test split. The notebook turns locations into useful features, fills in maps between sensors with **kriging** (Gaussian-process regression), finds hotspots with DBSCAN and predicts delivery times on a road graph. Think of an orange: the lines from top to bottom are far apart in the middle and squeeze together at the top, so "one step east" is short near the pole and long at the equator.

*Tiny example.* One degree of longitude is $111.2\cos(\text{latitude})$ km:

| latitude | km per degree of longitude | error of "degrees x 111.2" |
|---|---|---|
| 0° | 111.2 | 0% |
| 50° | 71.5 | +56% |
| 60° | 55.6 | +100% |

And the house-price lesson (error of log price): random 5-fold CV 0.099, 4 km spatial blocks 0.141, truly unseen district 0.140. Only the block split told the truth.

*You will learn.*
- Coordinate reference systems (CRS), map projections (Web Mercator, UTM) and the haversine distance from scratch
- Spatial indexes: a grid, a geohash encoder/decoder and a Ball tree, and why you must always search the 8 neighbouring cells
- Spatial features (distance to stations, counts within 500 m, kernel density, neighbour prices computed only from training data)
- Moran's I, the correlogram and **spatial block cross-validation**
- Interpolation with IDW and Gaussian-process kriging (with uncertainty), and DBSCAN hotspots with the haversine metric
- A two-stage ETA model (learned edge speeds + Dijkstra) and point-in-polygon spatial joins

*Key takeaway.* Use haversine or project first, and validate by holding out whole areas, because near things are alike.

### 02 · Bioinformatics and Sequence ML

*Explained simply.* Every living thing carries an instruction book written in four letters (A, C, G, T); proteins are written in 20 letters. So biology is full of very long texts, and many text tools work here. The central question is "how similar are these two sequences?", answered by **alignment**: line them up, allow gaps, and score the matches with dynamic programming. The notebook then counts short words (**k-mers**), compares whole genomes from tiny **MinHash** sketches, finds patterns with suffix arrays, uses an **HMM** to find hidden regions, trains a 1-D CNN that learns a motif by itself, and shows why genomic data needs special privacy care. Think of a spell-checker suggesting "receive" for "recieve": it lines up the two words and counts the differences, exactly what alignment does with genes.

*Tiny example.* Align `ACGT` with `AGT` (match +1, gap −1):

```
A C G T
A - G T      3 matches (+3) and 1 gap (-1)  ->  score 2, the best possible
```

On the motif-detection task: k-mer bag-of-words + logistic regression test AUC 0.82, 1-D CNN 0.95, oracle that knows the motif 0.97.

*You will learn.*
- DNA/protein alphabets, reverse complement, GC content, the genetic code and position weight matrices (PWMs)
- Needleman–Wunsch (global) and Smith–Waterman (local) alignment, BLOSUM62 and affine gaps
- k-mers, the Count-Min sketch, MinHash Jaccard and the Mash distance, enough to rebuild a family tree of genomes
- Suffix arrays, the BWT/FM-index and seed-and-verify read mapping (pigeonhole principle)
- HMM decoding of CpG islands with Viterbi and forward–backward, and why accuracy misleads there
- A 1-D CNN versus k-mer features, protein language models, and genomic data ethics with a membership-inference demo

*Key takeaway.* Sequences are text with biology attached: dynamic programming, hashing and HMMs do the heavy lifting, and related sequences must never straddle the train/test split.

---

## What transfers to any domain

The two notebooks look very different, but they teach the same three habits. These are the parts to carry into finance, medicine, climate, retail or any other field.

| Habit | Geospatial version | Bioinformatics version | Time-series version | Graph version |
|---|---|---|---|---|
| **Data-specific CV splits**: hold out what you will meet in production | spatial blocks or leave-one-region-out | split by gene family or chromosome; cluster by identity first | walk-forward (train on the past, test on the future) | hold out whole sub-graphs or future edges |
| **Domain metrics**: measure the real question | error on an unseen district, residual Moran's I, ETA error and route regret | island F1 (not letter accuracy), AUC, E-values for multiple testing | error at the forecast horizon, interval coverage | ranking metrics on held-out links |
| **Ethics and privacy** | location traces reveal home, work and habits | genomes identify people and their relatives; aggregate statistics leak membership | customer histories can be re-identified | social graphs leak who knows whom |

Before modelling in a new domain, ask: (1) *Which rows are secretly related, and how will I keep them apart in validation?* (2) *What number would a domain expert actually care about?* (3) *Who could be harmed if this data or model leaked?*

---

## How this connects to the rest of the repo and to real AI systems

- **Forecasting (time is the other "where").** Random CV leaks in time just as it does in space; see [Forecasting done right](../../04_Forecasting/00_start_here_forecasting_done_right.ipynb), [ML for forecasting](../../04_Forecasting/03_ml_for_forecasting.ipynb) (walk-forward validation) and [probabilistic forecasting](../../04_Forecasting/09_probabilistic_forecasting.ipynb). Sensors and stores are spatio-temporal: [multivariate forecasting](../../04_Forecasting/07_multivariate_forecasting.ipynb).
- **Graph ML.** Road networks (notebook 01) and molecules and protein interactions (notebook 02) are graphs: [graphs and Dijkstra](../../00_AI_Fundamentals/dsa/07_graphs.ipynb), [GNNs](../../05_Deep_Learning/07_gnn.ipynb), [graph ML hands-on](../../05_Deep_Learning/21_graph_machine_learning_hands_on.ipynb), [route planning](../../00_AI_Fundamentals/classical_ai/11_industry_route_planning_and_scheduling.ipynb). Google Maps predicts ETAs with GNNs; GraphCast forecasts weather with a graph network on a spherical mesh.
- **PGMs and HMMs.** CpG-island decoding is a hidden Markov model: [HMMs in classical AI](../../00_AI_Fundamentals/classical_ai/09_uncertain_knowledge_and_reasoning.ipynb) (section 11), [Markov networks and exact inference](../17_probabilistic_graphical_models/01_markov_networks_and_exact_inference.ipynb), [EM, variational inference and sampling](../17_probabilistic_graphical_models/02_em_variational_inference_and_sampling.ipynb) (Baum–Welch), [uncommon models](../04_uncommon_models/01_uncommon_ml_models.ipynb). Kriging is a Gaussian process: [Bayesian ML](../../14_Mathematics/07_bayesian_ml.ipynb), [kernel methods](../16_learning_theory/02_kernel_methods.ipynb), [GP for process optimisation](../04_uncommon_models/02_industry_gaussian_process_process_optimization.ipynb).
- **CNNs.** The 1-D CNN in notebook 02 is the same idea as an image CNN with one fewer dimension: [CNNs](../../05_Deep_Learning/03_cnn.ipynb), [your first image CNN](../../06_Computer_Vision/00_start_here_images_and_your_first_cnn.ipynb), [image classification](../../06_Computer_Vision/02_image_classification.ipynb) (satellite imagery uses the same transfer learning), [medical image analysis](../../06_Computer_Vision/10_medical_image_analysis.ipynb).
- **Ethics and privacy.** [Privacy in ML](../../19_AI_Ethics_and_Safety/03_privacy.ipynb) (membership inference, differential privacy), [bias and fairness](../../19_AI_Ethics_and_Safety/01_bias_fairness.ipynb) (genomic studies over-represent European ancestry), [responsible AI](../../19_AI_Ethics_and_Safety/04_responsible_ai.ipynb), [AI regulation](../../19_AI_Ethics_and_Safety/05_ai_regulation_compliance.ipynb) (GDPR Article 9), [privacy and security basics](../../00_AI_Fundamentals/04_privacy_and_security.ipynb).
- **Evaluation and research practice.** [Model evaluation](../06_model_evaluation/01_model_evaluation.ipynb), [evaluation metrics](../10_evaluation_metrics_comprehensive.ipynb), [experiment design for ML](../../24_Research_Methods/02_experiment_design_for_ml.ipynb), [research methodology](../../24_Research_Methods/01_research_methodology_and_literature_review.ipynb) (turning a domain project into a thesis).
- **Algorithms and systems underneath.** Geohash and k-mer hashing: [hashing](../../00_AI_Fundamentals/dsa/04_hashing.ipynb). Count-Min and MinHash: [streaming and sketching](../../00_AI_Fundamentals/advanced_algorithms/06_streaming_and_sketching_algorithms.ipynb) (MinHash also deduplicates LLM training data). Point-in-polygon: [computational geometry](../../00_AI_Fundamentals/advanced_algorithms/07_computational_geometry_and_fft.ipynb). Nearest-neighbour search in high dimensions: [vector databases](../../22_ML_System_Design/05_vector_databases.ipynb).
- **Earlier domain examples.** Lat/lon features in the [house-price project](../01_supervised/15_industry_house_price_regression.ipynb); DBSCAN on ordinary features in [clustering](../02_unsupervised/01_clustering.ipynb); bag-of-words in [text classification](../../07_NLP/03_text_classification.ipynb); protein language models are Transformers like [LLMs](../../08_LLM/00_start_here_how_llms_work.ipynb).
- **Study guide.** The deeper written guide for this folder is [`notes/18_domain_applications.md`](notes/18_domain_applications.md).

---

## Common beginner mistakes

- **Euclidean distance on raw latitude/longitude.** At 60°N it doubles east–west distances and fails completely across the ±180° line. Use haversine, or project to UTM first.
- **Mixing up axis order.** GIS libraries want `(lon, lat)`; scikit-learn's haversine metric wants `[lat, lon]` **in radians**.
- **Random K-fold on spatial, temporal or related data.** Nearby houses, consecutive days or near-identical genes leak across the split; the score looks great and production collapses.
- **Target features computed on the whole dataset.** "Mean price of the 10 nearest houses" must be built from training rows only, inside each fold.
- **Trusting accuracy on rare targets.** CpG islands cover 9% of the sequence, so "always background" scores 91% accuracy and finds nothing; report F1, AUC or segment counts.
- **Forgetting the other DNA strand.** A motif can sit on either strand; scan the reverse complement too, or count canonical k-mers.
- **Calling data "anonymous" because names were removed.** Genomes, location traces and even published averages can identify people.
- **Using k-means for hotspots.** It needs $k$, forces noise into clusters and uses means that are meaningless on raw degrees; use DBSCAN/HDBSCAN with the haversine metric.

---

## Exam / interview quick-revision

| Question | Answer |
|---|---|
| Why is Euclidean distance on degrees wrong? | One degree of longitude is $111.2\cos\varphi$ km, so east–west distances are stretched away from the equator. |
| Haversine formula? | $a = \sin^2(\Delta\varphi/2) + \cos\varphi_1\cos\varphi_2\sin^2(\Delta\lambda/2)$, $d = 2R\arcsin\sqrt a$. |
| Why does a geohash radius query search 9 cells? | Close points can sit on opposite sides of a cell border with different prefixes. |
| What does Moran's I measure? | Spatial autocorrelation: $I > 0$ means neighbours are alike; $E[I] = -1/(n-1)$ with no pattern. |
| How big should spatial CV blocks be? | At least the autocorrelation range read from the correlogram or semivariogram. |
| Kriging in ML language? | Gaussian-process regression with a stationary kernel; it also gives an uncertainty. |
| DBSCAN radius for haversine? | $\varepsilon_{\text{rad}} = \varepsilon_{\text{km}} / 6371$, with coordinates in radians. |
| Two stages of a production ETA model? | Learned per-edge speeds, then shortest-path search (plus an optional trip-level correction). |
| Global vs local alignment? | Needleman–Wunsch for whole related sequences; Smith–Waterman (borders 0, `max(0, ...)`, trace back from the best cell) for a shared region. |
| Time of pairwise alignment? | $O(nm)$; BLAST uses seed-and-extend heuristics to search databases fast. |
| What does MinHash estimate? | Jaccard similarity of two k-mer sets: $P[\min h(A) = \min h(B)] = J$. |
| Why compute Viterbi in log space? | Products like $0.25^{1000}$ underflow to 0 in float64; logs turn them into sums. |
| What does a first-layer filter of a genomics CNN learn? | A motif, roughly a position weight matrix. |
| How do you avoid leakage with sequences? | Split by gene family or chromosome, after clustering sequences by identity. |
| How can published allele frequencies leak privacy? | Summed over many SNPs, a participant's tiny pull on each average reveals membership (Homer et al., 2008). |

---

## Further reading

- S. Rey, D. Arribas-Bel and L. J. Wolf, *Geographic Data Science with Python* (CRC Press, 2023), free online at [geographicdata.science/book](https://geographicdata.science/book/intro.html).
- N. Cressie and C. K. Wikle, *Statistics for Spatio-Temporal Data* (Wiley, 2011).
- C. E. Rasmussen and C. K. I. Williams, *Gaussian Processes for Machine Learning* (MIT Press, 2006), free at [gaussianprocess.org/gpml](http://gaussianprocess.org/gpml/).
- D. R. Roberts et al., "Cross-validation strategies for data with temporal, spatial, hierarchical, or phylogenetic structure", *Ecography* 40 (2017): the one paper behind this folder's main lesson.
- R. Durbin, S. Eddy, A. Krogh and G. Mitchison, *Biological Sequence Analysis* (Cambridge, 1998).
- N. C. Jones and P. A. Pevzner, *An Introduction to Bioinformatics Algorithms* (MIT Press, 2004); P. Compeau and P. Pevzner, *Bioinformatics Algorithms*, free at [bioinformaticsalgorithms.org](https://www.bioinformaticsalgorithms.org/).
- D. Gusfield, *Algorithms on Strings, Trees and Sequences* (Cambridge, 1997).
- Free practice: [Rosalind](https://rosalind.info/) (bioinformatics programming problems).
