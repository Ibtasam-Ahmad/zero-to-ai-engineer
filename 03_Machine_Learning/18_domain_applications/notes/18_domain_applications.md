# Domain Applications (Electives): Geospatial ML and Bioinformatics

This study guide covers the two elective notebooks in `03_Machine_Learning/18_domain_applications/`. Each one takes the ordinary machine-learning toolkit (features, models, cross-validation, metrics) into a specialised field and shows what has to change. The first field is **geospatial** data, where every row has a location on the Earth. The second is **bioinformatics**, where every row is a long string of DNA or protein letters. The guide follows the notebooks section by section, explains every term the first time it appears, works small examples by hand and collects the key formulas and complexities. A glossary closes the guide.

The guide is optional, university-level material. You need the core supervised-learning ideas (training, features, overfitting, cross-validation) before you start.

## Part 0: Why Domains Matter

A **domain** is an area of application with its own data types, vocabulary, standard methods and rules, such as geography, biology, medicine or finance. Three things almost always change when ML enters a domain:

1. **Structure in the data.** Rows are not independent. Houses on the same street have similar prices; genes from related species are near-copies; today's sales resemble yesterday's. This structure is useful for prediction, but it breaks the assumption behind a random train/test split.
2. **The right metric.** The domain decides what a good model is. A delivery company cares about minutes of ETA error and about picking the fastest route; a genome annotator cares about finding the rare regions, not about overall letter accuracy.
3. **Ethics, privacy and law.** Location traces and genomes are among the most identifying data there are, and laws such as the EU GDPR treat genetic data as a special category.

Keep these three in mind; both notebooks return to them again and again.

```
 domain data --> domain distance / features --> ordinary ML model
                                                    |
          validation that matches deployment <------+
                    |
          domain metric + ethics review --> deploy
```

---

## Part 1: Geospatial Machine Learning

### 1.1 Coordinates, CRS and projections

**Latitude** ($\varphi$) is the angle north or south of the equator, from −90° to +90°. **Longitude** ($\lambda$) is the angle east or west of the Greenwich meridian, from −180° to +180°. Both are **angles measured from the centre of the Earth**, not distances.

A **coordinate reference system (CRS)** is the full recipe that turns numbers into places: a model of the Earth's shape (the **datum** or **ellipsoid**, for example WGS 84), units and axis order. GPS coordinates are WGS 84 geographic coordinates, code **EPSG:4326**.

A **map projection** flattens the curved surface onto a plane, $(\varphi, \lambda) \mapsto (x, y)$. Every projection distorts something (area, shape, distance or direction), so you choose what to keep:

| Projection | Code | Preserves | Distorts | Typical use |
|---|---|---|---|---|
| Web Mercator | EPSG:3857 | local angles (conformal) | areas by $1/\cos^2\varphi$ | web maps |
| UTM (60 zones, 6° wide) | e.g. EPSG:32632 | distances within a zone to about 0.1% | anything far outside the zone | national and city work in metres |
| Local equirectangular | none | distances inside a small area | everything far from the centre | quick city-scale features |

The UTM zone number is $\lfloor(\lambda + 180)/6\rfloor + 1$; for 10°E that is zone 32, and the northern-hemisphere code is EPSG:32632. The local equirectangular projection around a reference latitude $\varphi_0$ is $x = R\,\Delta\lambda\cos\varphi_0$, $y = R\,\Delta\varphi$ (angles in radians). Inside the notebook's 20 km × 20 km synthetic city it is within 0.2% of the true distance.

**Why raw degrees are wrong.** One degree of latitude is always about 111.2 km ($2\pi R/360$ with $R = 6371$ km). One degree of longitude is $111.2\cos\varphi$ km, because the circles of latitude shrink towards the poles:

| Latitude | km per degree of longitude | Error of "degrees × 111.2" east–west |
|---|---|---|
| 0° | 111.2 | 0% |
| 30° | 96.3 | +15% |
| 50° | 71.5 | +56% |
| 60° | 55.6 | +100% |

The error is $1/\cos\varphi - 1$, so it depends on direction (north–south steps are fine, east–west steps are stretched) and on latitude. Across the antimeridian (±180°) the naive method fails completely: two points on the equator at longitudes 179.9 and −179.9 are 22 km apart, but naive subtraction puts them about 40,000 km apart.

**Why it matters.** Wrong distances mean wrong nearest neighbours, wrong radius counts and wrong clusters. The safe rule is **project first, then compute**, or use a spherical formula.

### 1.2 The haversine distance

The **great-circle distance** is the shortest path between two points along the surface of a sphere. The **haversine formula** computes it in a numerically stable way:

$$a = \sin^2\frac{\Delta\varphi}{2} + \cos\varphi_1\cos\varphi_2\sin^2\frac{\Delta\lambda}{2}, \qquad d = 2R\arcsin\sqrt{a}.$$

Results from the notebook:

| Pair | Haversine (km) | Naive degrees (km) | Naive error |
|---|---|---|---|
| Karachi–Lahore | 1,033.0 | 1,103.5 | +6.8% |
| London–Paris | 343.6 | 403.6 | +17.5% |
| New York–London | 5,570.2 | 8,302.1 | +49% |

The Earth is actually an ellipsoid (flattened by about 1/298), so haversine can be off by up to about 0.5%. Surveying uses ellipsoidal formulas (Vincenty's or Karney's algorithms); for ML features haversine is the standard choice. Cost: $O(1)$ per pair, $O(n^2)$ for an all-pairs matrix.

> A common bug is axis order: GIS libraries usually take `(lon, lat)` as `(x, y)`, while scikit-learn's haversine metric takes `[lat, lon]` in **radians**.

### 1.3 Spatial indexing

Finding "all drivers within 500 m" by measuring the distance to every driver costs $O(n)$ per query. A **spatial index** is a catalogue that lets you look only in the right places, like a library catalogue that sends you to one aisle.

- **Grid index.** Cut the plane into square cells of side $c$ and store the points of each cell. A radius-$r$ query only inspects cells within $\lceil r/c\rceil$ cells of the query. Excellent for roughly uniform data; poor when many points crowd into a few cells.
- **Geohash.** Encode (lat, lon) as a short string by repeatedly halving the longitude and latitude ranges, interleaving the bits (longitude first) and writing 5 bits per base-32 character (alphabet `0123456789bcdefghjkmnpqrstuvwxyz`, which has no a, i, l, o). Each extra character makes the cell 32 times smaller: precision 5 is about 4.9 km, precision 6 about 1.2 km × 0.6 km, precision 7 about 153 m.
- **Tree indexes.** KD-trees split one coordinate at a time (projected data); **Ball trees** split into nested balls and work with any true metric, including haversine. **R-trees** index rectangles and polygons and are used by spatial databases such as PostGIS.
- **Hexagonal grids.** Uber's **H3** uses hexagons because all 6 neighbours of a hexagon are the same distance away, unlike the 8 neighbours of a square.

**Worked example by hand: the first geohash character of (42.6°N, 5.6°W).**

| Bit | Coordinate | Interval | Midpoint | Value ≥ mid? | Bit |
|---|---|---|---|---|---|
| 1 | lon −5.6 | [−180, 180] | 0 | no | 0 |
| 2 | lat 42.6 | [−90, 90] | 0 | yes | 1 |
| 3 | lon −5.6 | [−180, 0] | −90 | yes | 1 |
| 4 | lat 42.6 | [0, 90] | 45 | no | 0 |
| 5 | lon −5.6 | [−90, 0] | −45 | yes | 1 |

Bits `01101` = 13, and character 13 of the alphabet is `e`. Continuing gives `ezs42`.

**The edge effect.** Same prefix implies close, but close does **not** imply same prefix. In the notebook, two points 1.4 m apart across the Greenwich meridian get `gcpuzgr` and `u10hb52`. A radius query must therefore search the query's cell **plus its 8 neighbours**.

| Method | Build | Query | Notes |
|---|---|---|---|
| Brute force | none | $O(n)$ | 30,000 distances per query in the notebook |
| Grid / geohash | $O(n)$ | $O(1)$ cell lookup + candidates | about 170 candidates per query in the notebook |
| Ball / KD-tree | $O(n\log n)$ | about $O(\log n + k)$ in low dimensions | exact; Ball tree supports haversine |

All three methods returned identical neighbour sets; the indexes were roughly 20–100 times faster.

### 1.4 Spatial features

A model cannot see a map, so we turn location into numbers:

- **Distance to a point of interest (POI)**: distance from each row to the nearest station, school or hospital, via a nearest-neighbour query.
- **Count within a radius**: for example parks within 500 m.
- **Kernel density estimate (KDE)**: a smooth "how crowded is it here" score, $\hat f(\mathbf s) \propto \sum_i K\big(d(\mathbf s, \mathbf s_i)/h\big)$ with bandwidth $h$.
- **Neighbourhood aggregate**: for example the mean price of the 10 nearest training houses. Because it uses the target, this is **spatial target encoding** and must be computed from training rows only, inside each fold, and never from a row's own price.

In the notebook's 3,000-house synthetic city, a gradient-boosting model on a random split gave:

| Feature set | RMSE (log price) | MAPE |
|---|---|---|
| A: size, rooms, age | 0.222 | 18.2% |
| B: A + raw lat/lon | 0.102 | 8.1% |
| C: A + engineered spatial features | 0.098 | 7.7% |

Raw lat/lon lets trees carve the map into rectangles and memorise local price levels. Engineered features describe the **mechanism** (closeness to transport, parks, the local price level), and their real advantage appears when we predict far from the training data (next section). With a tree index, building the features costs $O(n\log m)$ for $n$ houses and $m$ POIs instead of $O(nm)$.

### 1.5 Spatial autocorrelation and Moran's I

**Tobler's first law of geography**: "everything is related to everything else, but near things are more related than distant things". **Spatial autocorrelation** is the statistical name for this.

**Moran's I** measures it. Given values $x_i$, deviations $z_i = x_i - \bar x$, a **spatial weights matrix** $W$ ($w_{ij} > 0$ if $i$ and $j$ are neighbours, $w_{ii} = 0$) and $S_0 = \sum_{ij} w_{ij}$:

$$I = \frac{n}{S_0}\,\frac{\sum_i\sum_j w_{ij} z_i z_j}{\sum_i z_i^2}.$$

$I > 0$ means clustering (neighbours alike), $I < 0$ means a checkerboard. With no pattern $E[I] = -1/(n-1)$. Significance comes from a **permutation test**: shuffle the values over the locations many times and count how often the shuffled $I$ is as large as the observed one.

**Worked example by hand.** Four cells in a row, neighbours share an edge, so $S_0 = 6$ (each of the 3 neighbour pairs counted twice).

- Values 1, 2, 3, 4: $z = (-1.5, -0.5, 0.5, 1.5)$, $\sum z^2 = 5$. Neighbour products: $0.75, -0.25, 0.75$, sum 1.25, doubled 2.5. $I = \frac{4}{6}\cdot\frac{2.5}{5} = +0.333$.
- Values 1, 4, 1, 4: $z = (-1.5, 1.5, -1.5, 1.5)$, $\sum z^2 = 9$. Each product is $-2.25$, sum $-6.75$, doubled $-13.5$. $I = \frac{4}{6}\cdot\frac{-13.5}{9} = -1.0$.

Since $E[I] = -1/3$ here, the smooth row is clustered and the alternating row is perfectly dispersed. On the synthetic house prices (8-nearest-neighbour weights) $I = 0.426$ with permutation p-value 0.002.

**The correlogram.** Computing $I$ for distance bands of increasing width shows how far the similarity reaches. In the notebook $I \approx 0.44$ within 0.5 km and falls below 0.1 at about 5 km: the **range** of autocorrelation is about 4–5 km.

**Residual Moran's I** measures how much spatial signal a model left unexplained. Out-of-fold residuals gave $I = 0.78$ for feature set A, 0.34 for B and 0.22 for C.

Cost: $O(nk)$ for a sparse weights matrix with $k$ neighbours per row, $O(Pnk)$ for $P$ permutations.

### 1.6 Spatial block cross-validation

With random K-fold, almost every test house has a training house a few hundred metres away, inside the autocorrelation range. A flexible model memorises local levels and copies them to the neighbour. That is fine if production always predicts inside covered areas, and badly optimistic if it will predict in a new district or city.

**Spatial block CV** cuts space into blocks of side $b$, assigns whole blocks to folds, and so keeps test points far from most training points. Choose $b$ at least as large as the autocorrelation range. **Buffered CV** also removes training points within a distance $h$ of the test fold.

| RMSE of log price | Random 5-fold | Block 1 km | Block 2 km | Block 4 km | Unseen NE district |
|---|---|---|---|---|---|
| B: raw lat/lon | 0.099 | 0.105 | 0.115 | 0.141 | 0.140 |
| C: spatial features | 0.095 | 0.099 | 0.105 | 0.119 | 0.135 |

Read it this way: as blocks grow to the range, the CV estimate for B rises until it matches the truly unseen district. Random CV underestimated the deployment error by about 30%. Mechanistic features (C) transfer better to new places.

| Validation scheme | Leaks through autocorrelation? | Estimates the error for |
|---|---|---|
| Random K-fold | yes | new points inside covered areas |
| Spatial block K-fold (block ≥ range) | mostly no | new areas about the size of a block |
| Buffered leave-one-out | no, if buffer ≥ range | isolated new locations |
| Leave-one-region-out | no | a new district or city |

**Why it matters.** The rule "validate the way you will deploy" is the most portable lesson in this folder. Roberts et al. (2017) give the same advice for temporal, hierarchical and phylogenetic structure.

### 1.7 Spatial interpolation: IDW and kriging

**Interpolation** guesses the value between measurement sites, for example a pollution map from 60 sensors.

**Inverse distance weighting (IDW)**: $\hat z(\mathbf s) = \sum_i w_i z_i / \sum_i w_i$ with $w_i = d(\mathbf s, \mathbf s_i)^{-p}$. It is simple and exact at the sensors, but it gives no uncertainty, the power $p$ is a guess, and it produces "bull's-eyes" around noisy sensors.

The **semivariogram** $\gamma(h) = \tfrac12 E[(Z(\mathbf s) - Z(\mathbf s + h))^2]$ is half the expected squared difference between values $h$ apart. It starts at the **nugget** (measurement noise), rises, and flattens at the **sill** (total variance) after the **range**.

**Kriging** is the best linear unbiased predictor under a covariance model. In ML language it is **Gaussian-process (GP) regression** with a stationary kernel, for example the RBF kernel $k(h) = \sigma_f^2 e^{-h^2/2\ell^2}$, with noise $\sigma_n^2$:

$$\mu(\mathbf s_*) = m + \mathbf k_*^\top (K + \sigma_n^2 I)^{-1}(\mathbf z - m), \qquad \sigma^2(\mathbf s_*) = k(0) - \mathbf k_*^\top (K + \sigma_n^2 I)^{-1}\mathbf k_*.$$

With a known mean $m$ this is **simple kriging**; **ordinary kriging** estimates a constant mean. The variogram and the kernel are two views of one covariance: $\gamma(h) = \sigma_n^2 + k(0) - k(h)$ for $h > 0$.

| Method | LOO RMSE at sensors | RMSE against the true surface |
|---|---|---|
| Nearest sensor | 1.79 | 1.76 |
| IDW, p = 2 | 1.98 | 2.15 |
| IDW, p = 3 | 1.60 | 1.76 |
| GP kriging | 0.89 | 0.72 |

The GP's 95% band covered the truth at about 91% of grid points, a little low because the noise variance was underestimated; always check calibration when you can. The kriging standard-deviation map is high in the gaps between sensors, so it also tells you where to install the next sensor, which is the idea behind Bayesian optimisation and active learning.

Cost: IDW $O(nm)$ for $n$ sensors and $m$ query points; GP $O(n^3)$ to factorise once, then $O(n)$ per mean and $O(n^2)$ per variance.

### 1.8 Hotspots with DBSCAN

**DBSCAN** has a radius $\varepsilon$ and a count `min_samples`. A **core point** has at least `min_samples` points (itself included) within $\varepsilon$; clusters are chains of core points within $\varepsilon$ of each other, plus the **border points** they reach; everything else is **noise** (label −1). It finds clusters of any shape without being told how many.

For geographic data use `metric="haversine"`, coordinates in radians and $\varepsilon_{\text{rad}} = \varepsilon_{\text{km}}/R$. In the notebook this found exactly the 4 planted hotspots (adjusted Rand index 0.90). Using "the same" radius on raw degrees made the neighbourhood an ellipse too narrow east–west (161 m instead of 250 m at 50°N), so it found 5 clusters and more noise.

k-means is a poor fit for hotspots: it needs $k$, forces noise into clusters, assumes round clusters of similar size, and averages raw degrees. Choose $\varepsilon$ from the "knee" of the sorted distances to each point's `min_samples`-th neighbour. Cost: $O(n\log n)$ on average with a tree index, $O(n^2)$ worst case.

### 1.9 Routing and ETA

A **road graph** has intersections as nodes and road segments as edges; the routing weight of edge $e$ at time $t$ is the travel time $\ell_e / v_e(t)$. A common production **ETA** (estimated time of arrival) design has two stages: (1) a **speed model** per edge learned from GPS probe data, (2) a **shortest-path** search (Dijkstra or A\*) over the predicted edge times, often followed by a trip-level correction model.

| Method | ETA MAE | ETA MAPE | Route regret |
|---|---|---|---|
| Shortest distance + average speed | 4.34 min | 17.8% | 22.2% |
| Learned speed model + fastest path | 0.35 min | 1.8% | 0.1% |

**Route regret** is how much slower the chosen route is than the best possible one. It is a domain metric: an ETA can be accurate for a bad route. Real systems use **time-dependent shortest paths**; Dijkstra stays correct if the network is FIFO (leaving later never makes you arrive earlier). Dijkstra with a binary heap costs $O((V + E)\log V)$.

### 1.10 Polygons and spatial joins

**Ray casting** (the even–odd rule): a point is inside a simple polygon if a ray from it crosses the boundary an odd number of times, $O(V)$ per test for $V$ vertices. A **spatial join** attaches attributes from one layer to another using a spatial predicate (`within`, `intersects`, `nearest`), the geographic version of an SQL join. In practice an R-tree first finds candidate polygons by bounding box, then the exact test runs. Never compute areas in degrees: project first (for example to UTM).

### 1.11 Geospatial summary

| Task | Method | Cost |
|---|---|---|
| Distance | haversine; ellipsoidal (Vincenty/Karney) for surveying | $O(1)$ |
| Local geometry | project to UTM or local CRS, then Euclidean | $O(1)$ per point |
| Radius / kNN query | grid, geohash, H3 (+ neighbours); Ball/KD-tree | $O(1)$ + candidates; $O(\log n + k)$ |
| Interpolation | IDW; GP kriging | $O(nm)$; $O(n^3)$ fit |
| Hotspots | DBSCAN / HDBSCAN with haversine | $O(n\log n)$ typical |
| ETA | learned edge speeds + Dijkstra | $O((V+E)\log V)$ per query |

---

## Part 2: Bioinformatics and Sequence ML

### 2.1 Biological sequences as strings

**DNA** is a string over $\{A, C, G, T\}$ (RNA uses U instead of T). The two strands pair A–T and C–G and run in opposite directions, so the partner strand of `ATGC`, read in its own direction, is its **reverse complement** `GCAT`. **GC content** is the fraction of G and C letters.

A **codon** is a triplet of DNA letters. The **genetic code** maps the 64 codons to 20 amino acids plus 3 **stop** codons (`TAA`, `TAG`, `TGA`); `ATG` codes for methionine (M) and usually marks the start of a gene. The code is **degenerate**: leucine, serine and arginine each have 6 codons. A **protein** is a string over the 20 amino-acid letters.

**Worked example.** `ATGGCCTAA` reads `ATG` → M, `GCC` → A, `TAA` → stop, so the protein is `MA`. GC content is 4/9 ≈ 0.44, and the reverse complement is `TTAGGCCAT`.

A **motif** is a short recurring pattern with a function, such as a transcription-factor binding site. Real motifs are fuzzy, so they are described by a **position weight matrix (PWM)**: the probability of each letter at each position. The **information content** of a column is

$$IC = 2 + \sum_b p_b \log_2 p_b \text{ bits},$$

with a maximum of 2 bits for 4 letters. In the notebook, strict positions (95% one letter) carry about 1.6 bits and fuzzy positions (40%) about 0.1 bits.

Remember the other strand: a motif or gene can sit on either strand, so searches scan both, and k-mer tools count **canonical** k-mers (the smaller of a k-mer and its reverse complement).

### 2.2 Pairwise alignment

An **alignment** of $x$ (length $n$) and $y$ (length $m$) inserts gap symbols so both have the same length, then scores each column: $s(a, b)$ for a match or mismatch, $g < 0$ for a gap (a **linear** gap cost).

**Global alignment (Needleman–Wunsch, 1970)** maximises the score over full-length alignments. With $F(i, 0) = ig$ and $F(0, j) = jg$:

$$F(i,j) = \max\{F(i-1,j-1) + s(x_i, y_j),\; F(i-1,j) + g,\; F(i,j-1) + g\}.$$

**Local alignment (Smith–Waterman, 1981)** finds the best-scoring pair of substrings. Three changes: borders are 0, a 0 is added inside the max (start fresh anywhere), and traceback starts from the **largest cell** and stops at the first 0.

**Worked example by hand.** `ACG` (rows) vs `AG` (columns), match +1, mismatch −1, gap −1:

|   | – | A | G |
|---|---|---|---|
| – | 0 | −1 | −2 |
| A | −1 | **1** | 0 |
| C | −2 | **0** | 0 |
| G | −3 | −1 | **1** |

For example $F(1,1) = \max(0 + 1, -1 - 1, -1 - 1) = 1$. Tracing back from the bottom-right: diagonal G/G, up C/–, diagonal A/A, giving `ACG` / `A-G` with score 1.

This is the edit-distance DP with scores instead of costs. The notebook checks both algorithms against exhaustive search: even strings of length 6 and 5 already have 3,653 possible alignments, while DP fills a 7 × 6 table.

**Scoring matrices.** For proteins, **BLOSUM62** gives log-odds scores of how often two amino acids replace each other in conserved blocks of related proteins (62 = blocks clustered at 62% identity). W–W scores +11 (tryptophan is rare and rarely replaced), I–L scores +2 (similar residues), dissimilar pairs are negative.

**Affine gaps** cost $g_{\text{open}} + (L-1)g_{\text{extend}}$ for a gap of length $L$, because one long insertion is more likely than many short ones. **Gotoh's algorithm** handles them with three DP matrices (ending in a match column, a gap in $x$, or a gap in $y$) in the same $O(nm)$ time.

| Variant | Time | Space | Use |
|---|---|---|---|
| Needleman–Wunsch | $O(nm)$ | $O(nm)$; score alone $O(\min(n,m))$ | whole related sequences of similar length |
| Smith–Waterman | $O(nm)$ | $O(nm)$ | shared domain, short query in a long sequence |
| Hirschberg | $O(nm)$ | $O(n + m)$ | global alignment in linear space |
| BLAST | heuristic, near-linear | index | database search: exact seeds, then extend |

### 2.3 k-mers, Count-Min and MinHash

The **k-mers** of a string of length $n$ are its $n - k + 1$ overlapping substrings of length $k$. There are $4^k$ possible DNA k-mers; with $k \approx 16$–$31$ almost every k-mer is unique in a genome.

The **Count-Min sketch** keeps $d$ rows of $w$ counters. Each item increments one counter per row (one hash per row); the estimate is the minimum over rows. It never under-counts, and over-counts by at most $\varepsilon N$ with probability $1 - \delta$ when $w = \lceil e/\varepsilon\rceil$ and $d = \lceil\ln(1/\delta)\rceil$. In the notebook, 4 × 2,048 counters for 34,241 distinct 8-mers had mean over-count about 18 and maximum 39, all under the $\varepsilon N \approx 66$ bound.

The **Jaccard similarity** of two sets is $J(A, B) = |A\cap B| / |A\cup B|$. **MinHash** estimates it: for a random hash function $h$, $P[\min h(A) = \min h(B)] = J$. A **bottom-$s$ sketch** keeps the $s$ smallest hash values of a set. The **Mash distance** turns $J$ into an estimated per-letter mutation rate:

$$D = -\frac{1}{k}\ln\frac{2J}{1+J}.$$

**Worked example by hand.** 3-mers of `ACGTAC`: `ACG, CGT, GTA, TAC`. 3-mers of `ACGTTC`: `ACG, CGT, GTT, TTC`. Shared: 2; union: 6; $J = 2/6 = 0.33$. A single substitution destroyed two of the four 3-mers (in general up to $k$), which is why $J$ falls quickly with mutation and why the formula divides by $k$.

In the notebook, four genomes evolved along a known tree were each summarised by 1,000 hash values. The MinHash Jaccard matched the exact Jaccard closely, the Mash distance tracked the true fraction of differing letters, and average-linkage clustering (UPGMA) recovered the true tree ((A, B), (C, D)). Sketching is $O(n)$ hashing; comparing two sketches is $O(s)$, independent of genome size. The same MinHash idea deduplicates web text for LLM training.

### 2.4 Suffix arrays, the BWT and read mapping

The **suffix array** $SA$ of $s\$$ (with a unique smallest end marker `$`) lists the start positions of all suffixes in sorted order. All occurrences of a pattern form one contiguous block of $SA$, found by two binary searches in $O(|P|\log n)$. **Prefix doubling** builds it in $O(n\log^2 n)$ by sorting on the first 1, 2, 4, … letters.

The **Burrows–Wheeler transform** is $BWT[i] = s[SA[i] - 1]$, the letter before each sorted suffix. With the **FM-index** (counts $C[c]$ and an occurrence table $Occ(c, i)$), **backward search** counts the occurrences of $P$ in $O(|P|)$ steps using memory close to the compressed genome. Read aligners such as BWA and Bowtie are built on it.

**Worked example by hand.** For `banana$` the sorted suffixes are `$` (6), `a$` (5), `ana$` (3), `anana$` (1), `banana$` (0), `na$` (4), `nana$` (2). So $SA = [6, 5, 3, 1, 0, 4, 2]$ and $BWT$ = `annb$aa`. The pattern `ana` occupies rows 2–3, so it occurs twice, at positions 3 and 1.

**Read mapping** places millions of short sequencing **reads** on a reference genome despite errors. **Pigeonhole seeding**: split a read into $e + 1$ pieces; if it has at most $e$ errors, at least one piece matches exactly. In the notebook, exact search placed only error-free reads, while 3 seeds of 13 letters per 40-letter read placed every read with up to 2 errors. Shorter seeds are more sensitive but produce more random hits (a 13-mer appears about $n/4^{13}$ times by chance), the classic speed/sensitivity trade-off.

### 2.5 Hidden Markov models: CpG islands and profiles

In vertebrate genomes the dinucleotide CG is rare except in stretches of a few hundred to a few thousand letters called **CpG islands**, which often mark the starts of genes. Finding them is a textbook HMM problem.

A **hidden Markov model (HMM)** has hidden states $z_t$, a transition matrix $A_{kl} = P(z_{t+1} = l \mid z_t = k)$, an initial distribution $\pi$ and emission probabilities $B_k(x) = P(x_t = x \mid z_t = k)$. Here the hidden states are "island" (+) and "background" (−), which prefer different letters.

- **Viterbi** finds the most likely state path by DP: $v_l(t) = B_l(x_t)\max_k v_k(t-1)A_{kl}$, done in **log space**.
- **Forward–backward** computes posteriors $P(z_t = k \mid x)$ from $\alpha_k(t) = P(x_{1..t}, z_t = k)$ and $\beta_k(t) = P(x_{t+1..T} \mid z_t = k)$, using scaling or log-sum-exp.
- Both cost $O(TK^2)$ for $T$ letters and $K$ states. Learning the parameters from unlabelled data uses EM (the Baum–Welch algorithm).

**Why log space?** $0.25^{1000} \approx 10^{-602}$, far below the smallest float64 (about $10^{-308}$), so it becomes 0. Logs turn products into sums, and since log is monotone the argmax is unchanged.

| Method | Letter accuracy | Island F1 | Segments found |
|---|---|---|---|
| Viterbi | 0.980 | 0.874 | 2 |
| Posterior $P(+ \mid x) > 0.5$ | 0.979 | 0.872 | 2 |
| GC in a 100-letter window > 0.5 | 0.972 | 0.843 | 19 |
| Always background | 0.909 | 0.000 | 0 |

The truth had 4 islands covering 9.1% of the sequence. **Accuracy is misleading** here: predicting "background" everywhere already scores 0.91. The HMM wins on F1 and returns clean segments, because its transition probabilities encode prior knowledge of segment lengths, so it does not switch at every local run of C and G. It missed the two short islands (19 and 40 letters): too little evidence to pay the cost of switching states, a real limitation of HMM segmenters.

**Profile HMMs** (HMMER, Pfam) extend a PWM to whole protein families by adding insert and delete states at every position. The gap-free special case is a **PWM log-odds scan**: score each window $w$ by $\sum_i \log_2(PWM[i, w_i]/0.25)$. Its best-window score detected the planted motif with AUC 0.94. Because a 300-letter sequence has about 290 windows, chance high scores happen; this multiple-testing effect is why tools report **E-values** (the expected number of chance hits at that score in a database of that size).

### 2.6 Sequence classification: k-mers vs a 1-D CNN

**Task.** 3,000 sequences of 100 letters. Positives contain one motif instance at a random position; negatives contain a **decoy**: the same motif letters shuffled, so the composition is identical and only the order differs.

- **k-mer bag-of-words + logistic regression**: count all k-mers for $k = 3, 4, 5$ (64 + 256 + 1,024 features) and fit an L2-regularised logistic regression. Position-invariant, but it sees only short words.
- **1-D CNN** (in the style of DeepBind, 2015): one-hot input of shape 4 × 100, `Conv1d` with 16 filters of width 12, ReLU, **global max pooling** ("is the pattern anywhere?"), and a linear output. A first-layer filter acts as a learnable PWM.

| Model | Test AUC |
|---|---|
| k-mer (3, 4, 5) logistic regression | 0.819 |
| 1-D CNN (16 filters × 12) | 0.951 |
| Oracle PWM scan (knows the motif) | 0.973 |

The CNN's most important filter correlated 0.93 with the true PWM, and its consensus `TTGACGTCATGC` is the true `TGACGTCATGCA` shifted by one. Reading first-layer filters as motifs is the classic way to interpret genomics CNNs. Cost: k-mer features $O(nL)$; the CNN $O(F \cdot w \cdot 4 \cdot L)$ per sequence for $F$ filters of width $w$ on length $L$.

**Leakage with sequences.** Splitting related sequences (the same gene from close species, overlapping windows of one chromosome) across train and test lets the model recognise near-copies. Split by gene family or chromosome, after clustering sequences by identity. This is the sequence version of spatial leakage.

### 2.7 Embeddings, clustering and protein language models

The notebook simulates 5 protein families (40 members each, 30% substitutions plus small insertions and deletions) and clusters them without alignment, scoring with the **adjusted Rand index (ARI)** (1 = perfect, 0 = chance):

| Embedding | ARI |
|---|---|
| 1-mer composition (20 dims) → PCA 10 → k-means | 0.881 |
| 2-mer composition (400 dims) → PCA 10 → k-means | 1.000 |

2-mers also capture order; about half of each ancestor's 2-mers survive 30% substitution ($0.7^2 \approx 0.49$), enough to separate the families.

A **protein language model (pLM)** is a Transformer trained on hundreds of millions of natural protein sequences with **masked-token prediction**: hide about 15% of the residues and predict them from the rest. To succeed it must learn which residues co-vary across evolution, which reflects 3-D contacts and function, so its hidden states are useful **embeddings** for structure, function and mutation-effect prediction.

| Model | Year | What it does |
|---|---|---|
| AlphaFold2 | 2021 | structure from sequence + alignments; near-experimental accuracy at CASP14 |
| ESM-2 / ESMFold | 2022–23 | pLM up to 15B parameters; structure from a single sequence |
| AlphaFold 3 | 2024 | complexes with DNA/RNA and ligands, diffusion-based structure module |
| ESM3 | 2024–25 | generative model over sequence, structure and function |
| DNABERT, Nucleotide Transformer, Evo / Evo 2 | 2021–25 | the same idea on DNA |

The 2024 Nobel Prize in Chemistry went to David Baker (computational protein design) and to Demis Hassabis and John Jumper (AlphaFold). A toy masked-prediction model in the notebook, which looks up the (left, right) context in other family members, reached 20.8% accuracy against a 6.3% baseline (5% for random guessing): a tiny echo of why pLMs work.

### 2.8 Data ethics for genomic data

Genomic data is identifying, shared with relatives and permanent: you cannot change your genome like a password.

- **Identifiability.** Gymrek et al. (2013) inferred surnames of anonymous research participants from Y-chromosome markers and public genealogy databases. Investigators have identified suspects through relatives in consumer genealogy databases (the 2018 Golden State Killer case).
- **Aggregate statistics leak.** Homer et al. (2008) showed that published allele frequencies reveal whether a person is part of a study. The notebook reproduces this on synthetic genotypes: membership-inference AUC was 0.72 with 100 SNPs, 0.93 with 1,000 and 1.00 with 5,000. Each average is pulled slightly towards each participant; summed over many SNPs the bias becomes a strong test.
- **Consent and governance.** Broad versus specific consent, withdrawal, return of incidental findings and community engagement (the HeLa cell line, taken from Henrietta Lacks in 1951 without consent). Controlled-access archives (dbGaP, EGA), data access committees and GA4GH standards govern sharing.
- **Law.** GDPR Article 9 lists genetic data as a special category. In the US, HIPAA covers health providers and GINA (2008) bans genetic discrimination in health insurance and employment, but not life insurance.
- **Consumer genomics.** The 2023 credential-stuffing attack on 23andMe exposed millions of users through its relative-matching feature; the company's 2025 bankruptcy raised the question of what happens to customers' genomes when a company is sold.
- **Fairness.** Most genomic studies over-represent people of European ancestry, so models can be much less accurate for others. Report the ancestry make-up and evaluate per group.

Defences include controlled access, publishing fewer or noisier statistics (**differential privacy**) and data-use agreements. Membership inference applies to any ML model trained on personal data.

### 2.9 Bioinformatics summary

| Problem | Method | Time |
|---|---|---|
| Global similarity | Needleman–Wunsch | $O(nm)$ |
| Shared region | Smith–Waterman | $O(nm)$ |
| Database search | BLAST (seed and extend) | heuristic |
| Genome-scale similarity | k-mers + MinHash (Mash) | $O(n)$ sketch, $O(s)$ compare |
| Frequent k-mers in little memory | Count-Min sketch | $O(d)$ per k-mer |
| Exact substring search | suffix array; FM-index | $O(\lvert P\rvert\log n)$; $O(\lvert P\rvert)$ |
| Reads with errors | pigeonhole seeds + verification | seeds × hits |
| Segmentation | HMM + Viterbi / posterior | $O(TK^2)$ |
| Sequence to label | k-mer BoW + LR; 1-D CNN; pLM embeddings | linear; $O(FwL)$; Transformer |

---

## Part 3: What Transfers to Any Domain

| Habit | Geospatial | Bioinformatics | General rule |
|---|---|---|---|
| Validation split | spatial blocks ≥ autocorrelation range; leave-one-region-out | split by family or chromosome after identity clustering | hold out whatever is new in production (areas, families, future dates, new customers) |
| Metric | error on an unseen district; residual Moran's I; ETA error and route regret | island F1 and segment counts, AUC, E-values | pick the number a domain expert acts on; beware accuracy on rare classes |
| Distance / similarity | haversine or projected Euclidean | alignment score, Jaccard, Mash distance | use the distance the domain's geometry demands |
| Features | mechanistic features (distance to POIs) transfer; raw coordinates memorise | k-mers, PWMs, learned filters, pLM embeddings | features that describe a mechanism generalise to new settings |
| Ethics | location traces reveal home and habits | genomes identify people and relatives; aggregates leak | assume "anonymous" data can be re-identified; plan consent, access control and privacy |

Time series follow the same logic: random K-fold leaks the future, so forecasting uses walk-forward validation (see `04_Forecasting/`). Graph data does too: random edge splits can leak through neighbours, so graph ML holds out nodes, sub-graphs or future edges (see `05_Deep_Learning/07_gnn.ipynb`).

**Why it matters.** Most published failures of ML in specialised fields are not bad models but bad validation: leaked neighbours, near-duplicate sequences or future data in the training set. An engineer who asks "which rows are secretly related?" before training avoids most of them.

---

## Glossary

- **Adjusted Rand index (ARI)**: agreement between two clusterings, corrected for chance; 1 is perfect, 0 is random.
- **Affine gap**: gap cost $g_{\text{open}} + (L-1)g_{\text{extend}}$, making one long gap cheaper than many short ones.
- **Alignment**: lining up two sequences with gaps so that similar letters share columns.
- **Antimeridian**: the ±180° longitude line, where naive longitude subtraction breaks.
- **Ball tree**: a nearest-neighbour index of nested balls that works with any metric, including haversine.
- **BLAST**: a fast heuristic database search that finds exact seeds and extends them.
- **BLOSUM62**: a log-odds substitution matrix for amino acids.
- **Burrows–Wheeler transform (BWT)**: the letter before each sorted suffix; the basis of the FM-index.
- **Canonical k-mer**: the smaller of a k-mer and its reverse complement, so both strands count the same.
- **Codon**: a triplet of DNA letters coding for one amino acid or a stop.
- **Coordinate reference system (CRS)**: the full recipe (datum, units, axis order) that turns coordinates into places.
- **Correlogram**: Moran's I as a function of distance; shows the range of autocorrelation.
- **Count-Min sketch**: a small table of counters that estimates frequencies and never under-counts.
- **CpG island**: a C- and G-rich genome region where the CG pair is unusually common, often near gene starts.
- **DBSCAN**: density-based clustering that finds arbitrary-shaped clusters and labels noise, with no need for $k$.
- **E-value**: the expected number of chance hits at a given score in a search of a given size.
- **EPSG code**: a standard number identifying a CRS (4326 for WGS 84 lat/lon, 3857 for Web Mercator).
- **ETA**: estimated time of arrival.
- **FM-index**: a compressed index over the BWT that counts pattern occurrences in $O(|P|)$.
- **Forward–backward**: HMM algorithm for posterior state probabilities.
- **GC content**: fraction of G and C letters in a DNA sequence.
- **Geohash**: a base-32 string encoding a lat/lon cell; shared prefixes mean the same cell.
- **Great-circle distance**: the shortest path between two points on a sphere's surface.
- **H3**: Uber's hierarchical hexagonal grid index.
- **Haversine formula**: a numerically stable formula for great-circle distance.
- **Hidden Markov model (HMM)**: a model of hidden states that switch with fixed probabilities and emit observed symbols.
- **Information content**: how strict a PWM column is, in bits (up to 2 for DNA).
- **Inverse distance weighting (IDW)**: interpolation by a distance-weighted average of nearby measurements.
- **Jaccard similarity**: size of the intersection divided by the size of the union of two sets.
- **k-mer**: a substring of length $k$.
- **Kernel density estimate (KDE)**: a smooth density surface built by summing a kernel around each point.
- **Kriging**: best linear unbiased spatial interpolation; Gaussian-process regression in ML terms.
- **Map projection**: a mapping from the curved Earth to a flat plane; always distorts something.
- **Mash distance**: $-\frac1k\ln\frac{2J}{1+J}$, an estimate of per-letter divergence from MinHash Jaccard.
- **Membership inference**: deciding whether a person's data was used in a study or a model's training set.
- **MinHash**: a sketch whose matching minimum hash values estimate Jaccard similarity.
- **Moran's I**: a statistic for spatial autocorrelation.
- **Motif**: a short, recurring sequence pattern with a biological function.
- **Needleman–Wunsch**: dynamic-programming global alignment.
- **Nugget, sill, range**: the semivariogram's starting value (noise), plateau (total variance) and the distance where it flattens.
- **Pigeonhole seeding**: splitting a read into $e+1$ pieces so one matches exactly if there are at most $e$ errors.
- **Point of interest (POI)**: a mapped place such as a station, school or park.
- **Position weight matrix (PWM)**: per-position letter probabilities describing a fuzzy motif.
- **Profile HMM**: an HMM with match, insert and delete states per position, modelling a sequence family.
- **Protein language model (pLM)**: a Transformer trained by masked-residue prediction on protein sequences.
- **R-tree**: a spatial index of bounding rectangles, used for polygons in spatial databases.
- **Ray casting**: point-in-polygon test counting boundary crossings of a ray.
- **Read mapping**: placing short sequencing reads on a reference genome.
- **Reverse complement**: the other DNA strand, complemented (A↔T, C↔G) and reversed.
- **Route regret**: how much slower a chosen route is than the best one.
- **Semivariogram**: half the expected squared difference between values a distance $h$ apart.
- **Smith–Waterman**: dynamic-programming local alignment.
- **Spatial autocorrelation**: the tendency of nearby locations to have similar values.
- **Spatial block cross-validation**: CV that assigns whole spatial blocks to folds to stop neighbour leakage.
- **Spatial join**: attaching attributes from one map layer to another by a spatial predicate.
- **Spatial target encoding**: a feature built from the target values of nearby rows; must use training rows only.
- **Suffix array**: the sorted start positions of all suffixes of a string.
- **Tobler's first law**: near things are more related than distant things.
- **UTM**: Universal Transverse Mercator, 60 metric projection zones each 6° wide.
- **Viterbi algorithm**: DP that finds the most likely hidden-state path of an HMM.
- **Walk-forward validation**: time-series CV that always trains on the past and tests on the future.
- **WGS 84**: the global datum used by GPS (EPSG:4326 for lat/lon).
