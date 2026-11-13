# Quantum AI: Quantum Computing and Quantum Machine Learning for AI Engineers

Quantum computers store information in **qubits**, which follow the rules of quantum physics instead of the on/off rules of ordinary bits. For a few special problems (factoring large numbers, simulating molecules, some search problems) this can be dramatically faster than any classical computer. For most everyday tasks, including training today's neural networks, it is not. This track teaches quantum computing **from zero** for AI engineers. You build your own small quantum simulator in numpy, run the famous algorithms on it, train quantum machine-learning models, and then look honestly at the tools, the hardware, the noise problem, the industry, and the security change that affects every AI system today: **post-quantum cryptography**. It is an **optional, advanced track**. Every term is explained the first time it appears, and no physics background is assumed.

**The track has two parts.** Quantum AI and quantum ML are built on top of quantum computing, so learn the foundation first:

| Part | Notebooks | Question it answers |
|---|---|---|
| **Part 1: Quantum Computing (00, 01, 02)** | [00 start here](00_start_here_quantum_computing_explained_simply.ipynb), [01 basics](01_quantum_computing_basics.ipynb), [02 algorithms](02_quantum_algorithms.ipynb) | What is a quantum computer, how does it work, and what is it good for? |
| **Part 2: Quantum AI and Quantum ML (03, 04, 05)** | [03 quantum ML](03_quantum_machine_learning.ipynb), [04 tools, hardware and industry](04_quantum_ai_tools_hardware_and_industry.ipynb), [05 QML on sensor data: fall detection](05_quantum_ml_on_sensor_data_fall_detection.ipynb) | Can quantum computers help machine learning, how does AI help quantum computers, and what happens on a realistic task? |

**Start point:** [00_start_here_quantum_computing_explained_simply.ipynb](00_start_here_quantum_computing_explained_simply.ipynb). It assumes no physics and teaches the little maths you need from zero.

**Who needs it.**
- **AI and ML engineers** who keep hearing "quantum AI" and want to judge the claims themselves, and talk about them in interviews.
- **Students** (BS/MS in AI, CS, physics or maths) who want a practical, code-first companion to a quantum computing course.
- **Engineers moving into quantum roles**: quantum software, ML for quantum hardware (decoders, calibration), quantum applications, or post-quantum security.
- **Tech leads and architects** who must plan the move to post-quantum cryptography for systems that hold model weights, training data and user traffic.

**How it complements the rest of the repo.** Other modules teach the classical side. This track reuses them and adds the quantum part:

| Module | What it already teaches | What this track adds |
|---|---|---|
| [`14_Mathematics/01_linear_algebra`](../14_Mathematics/01_linear_algebra.ipynb) | vectors, matrices, eigenvalues | the same tools with **complex numbers**: a qubit is a vector, a gate is a unitary matrix, a Hamiltonian's lowest eigenvalue is a ground-state energy |
| [`14_Mathematics/03_probability`](../14_Mathematics/03_probability.ipynb) | probability, sampling | the **Born rule** (probability = amplitude squared), shots, and estimating values from counts |
| [`03_Machine_Learning/01_supervised/05_svm`](../03_Machine_Learning/01_supervised/05_svm.ipynb) | SVMs and the kernel trick | **quantum kernels** given to `SVC(kernel="precomputed")` |
| [`05_Deep_Learning`](../05_Deep_Learning/01_neural_network_fundamentals.ipynb) | neural networks, gradient descent, optimisers | **variational circuits** as "quantum neural networks", the **parameter-shift rule**, barren plateaus |
| [`00_AI_Fundamentals/classical_ai`](../00_AI_Fundamentals/classical_ai/README.md) | search and optimisation | **Grover search** and **QAOA** for MaxCut, compared with classical search |
| [`19_AI_Ethics_and_Safety`](../19_AI_Ethics_and_Safety/) | privacy, responsible AI | why **post-quantum cryptography** matters for model weights, training data and API traffic |
| [`24_Research_Methods`](../24_Research_Methods/README.md) | fair baselines, ablations, honest reporting | how to read **"quantum advantage"** claims and benchmark QML against strong classical baselines |
| [`26_Sensor_AI/02_imu_activity_recognition_and_fall_detection`](../26_Sensor_AI/02_imu_activity_recognition_and_fall_detection.ipynb) | accelerometer signals, activity recognition and fall detection with classical ML | notebook 05 runs **quantum ML on the same kind of task** and compares it honestly with classical models |

**When to take it:**

```
 Stage 4 Maths (linear algebra, probability) --> Stage 5 Classical ML --> Stage 6 Deep learning
                                                                                |
                                                     EARLIEST START ------------+
                                                                                v
   25_Quantum_AI   Part 1: Quantum Computing        Part 2: Quantum AI and Quantum ML
                   00 -> 01 -> 02          ---->    03 -> 04
                                                     \-> 05 (QML on sensor data)
                   (00 needs only Python; 01 and 02 need the maths stage;
                    03 and 05 need SVMs and gradient descent)
```

- **Earliest:** notebook 00 needs only basic Python, so anyone can start there. Notebooks 01 and 02 need linear algebra, probability and Python with numpy. Notebook 03 also expects SVMs and gradient descent. Notebook 04 builds on 01-03. Notebook 05 builds on 03 and uses the classical ML evaluation ideas (cross-validation, precision/recall).
- **Any time later:** this track does not block anything else in the repo. Section 9 of notebook 04 (post-quantum cryptography) is worth reading for every engineer who ships production systems.

---

## The whole topic explained simply

A normal bit is a coin lying on a table: heads (0) or tails (1). A qubit is like a coin **spinning** in the air. While it spins, it carries two numbers called **amplitudes** that decide the odds of heads and tails. When you catch it (**measure** it) you always get plain heads or tails. Unlike odds, amplitudes can be **negative**, so two paths to the same answer can **cancel out**, like two water waves meeting crest to trough. A quantum algorithm is a recipe that makes the paths to *wrong* answers cancel and the paths to the *right* answer add up, so the right answer is likely when you finally measure. Two qubits can also be **entangled**: each one alone looks random, but their results are linked. All of this only works while the qubits are left undisturbed. Real qubits are fragile, so **noise** is the central engineering problem, and **error correction** (many physical qubits working together as one reliable "logical" qubit) is the way out.

**Tiny worked example (one round of Grover search).** We look for one marked item among 8, using 3 qubits. Start with all 8 amplitudes equal to $1/\sqrt8 \approx 0.354$, so each item has probability 0.125. The **oracle** flips the sign of the marked item: its amplitude becomes −0.354. The average amplitude is now $(7 \times 0.354 - 0.354)/8 \approx 0.265$. The **diffuser** reflects every amplitude about that average ($a \to 2 \times 0.265 - a$): the 7 unmarked items drop to $0.530 - 0.354 = 0.177$, and the marked item jumps to $0.530 + 0.354 = 0.884$. Its probability is $0.884^2 \approx 0.78$, up from 0.125, after a single question to the oracle. A second round brings it to about 0.95. Notebook 02 runs exactly this and plots it.

---

## What quantum AI can and can't do today

> **Can do (as of late 2026):**
> - Run small circuits (tens to a few hundred good qubits, more physical qubits on some platforms) through the cloud, with noticeable noise.
> - Demonstrate quantum error correction working **below threshold** on small codes (reported by several groups since 2024), and logical qubits that outperform the physical ones.
> - Perform carefully chosen sampling and physics-simulation tasks that are hard for classical simulation (these are milestones, not products, and classical methods keep catching up on some of them).
> - Benefit enormously from **AI for quantum**: neural decoders, ML-based calibration and control, LLM help for writing quantum code.
>
> **Can't do (yet):**
> - Break RSA or elliptic-curve cryptography. Published estimates need on the order of a million noisy physical qubits running error-corrected for days; today's machines are far from that. But **"harvest now, decrypt later"** makes the move to post-quantum cryptography urgent anyway.
> - Train neural networks or LLMs faster. There is no evidence for this, and data loading, readout and gradient costs make it very unlikely in the near term.
> - Beat strong classical baselines on any practical machine-learning task with classical data. Several claimed QML speedups were **dequantized** (matched by classical algorithms).
> - Solve optimisation problems (logistics, scheduling, portfolios) better than the best classical solvers, as far as has been demonstrated.
>
> **Most likely first real value:** simulation of chemistry, materials and physics on error-corrected machines. Timelines are uncertain; treat any specific year with caution.

---

## Who is this for, prerequisites and time

| | |
|---|---|
| **Who** | AI/ML engineers, CS/AI/physics students, engineers moving into quantum software, ML-for-quantum or post-quantum security roles; also interview prep for those roles |
| **Must know first** | for notebook 00: only [Python basics](../01_Python/01_basic.ipynb). From notebook 01 on: numpy, [linear algebra](../14_Mathematics/01_linear_algebra.ipynb) (vectors, matrices, matrix-vector product, eigenvalues), [probability](../14_Mathematics/03_probability.ipynb) (probabilities, sampling) |
| **Helpful** | [your first ML model](../03_Machine_Learning/00_start_here_your_first_ml_model.ipynb), [SVMs](../03_Machine_Learning/01_supervised/05_svm.ipynb), [neural network fundamentals](../05_Deep_Learning/01_neural_network_fundamentals.ipynb), [optimisation](../14_Mathematics/06_optimization.ipynb), [maths notation bridge](../14_Mathematics/00_start_here_math_notation_bridge.ipynb) |
| **Time needed** | about 11-16 hours for all 6 notebooks, plus the notes |
| **Runs on** | CPU only, no API key, no internet. Each notebook runs in under a minute, except notebook 05 (about 1.5-2 minutes) |

### Install

The **core notebooks need only numpy** (plus matplotlib for plots, and scipy, scikit-learn and pandas in notebooks 02-05), all already in the repo's [requirements.txt](../requirements.txt). The **optional** cells in notebooks 04 and 05 use the two most popular quantum SDKs:

```bash
pip install qiskit pennylane
```

If they are not installed, those cells print `skipped: pip install qiskit` (or `pennylane`) and the rest of the notebook still runs. No account, token or real quantum hardware is needed; the cloud-hardware examples are shown as text only.

---

## Study order

**Part 1: Quantum Computing (00, 01, 02)** (start with 00)

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 00 | [**Start here:** quantum computing explained simply](00_start_here_quantum_computing_explained_simply.ipynb) | Bits vs qubits, everyday pictures (spinning coin, ripples, a maze where wrong paths cancel) and where they break, the maths from zero (complex numbers, vectors, matrices, probabilities as squared lengths), measurement as sampling, $2^n$ growth, a Bell pair, interference, myths vs facts, a glossary and a quiz | 1-1.5 h |
| 01 | [Quantum computing basics](01_quantum_computing_basics.ipynb) | From bits to qubits: superposition, amplitudes, measurement, the Bloch sphere, gates, tensor products, entanglement, interference and no-cloning, while you **build a statevector simulator in numpy** | 2-3 h |
| 02 | [Quantum algorithms](02_quantum_algorithms.ipynb) | Deutsch-Jozsa, Bernstein-Vazirani, Grover (with an amplitude-amplification plot), QFT and phase estimation, Shor and the threat to RSA, VQE and QAOA, and a table of speedup types | 2-3 h |

**Part 2: Quantum AI and Quantum ML (03, 04, 05)**

| # | Notebook | In one sentence | Time |
|---|---|---|---|
| 03 | [Quantum machine learning](03_quantum_machine_learning.ipynb) | Data encodings, variational circuits, the parameter-shift rule, a **trained variational classifier**, **quantum kernels** with scikit-learn, hybrid models, QRL/QGANs, and the limits (barren plateaus, noise, data loading, dequantization) | 2-3 h |
| 04 | [Tools, hardware and industry](04_quantum_ai_tools_hardware_and_industry.ipynb) | Qiskit and PennyLane versions of the same tasks, hardware modalities, a noise demo, error mitigation vs error correction, AI for quantum (with a learned decoder), industry use cases, post-quantum cryptography, cloud hardware and a career roadmap | 2-3 h |
| 05 | [Quantum ML on sensor data: fall detection](05_quantum_ml_on_sensor_data_fall_detection.ipynb) | Synthetic accelerometer windows for 8 people, features to qubit angles, and an honest leave-one-subject-out comparison of a threshold rule, logistic regression, RBF SVM, MLP, a **variational quantum classifier** and a **quantum-kernel SVM**, with shot noise, simulated hardware noise, encoding choices and training cost | 2 h |

Study notes for the whole track (with diagrams): [notes/25_Quantum_AI.md](notes/25_Quantum_AI.md).

---

## The notebooks one by one

### Part 1: Quantum Computing (00, 01, 02)

#### 00 · Start here: quantum computing explained simply

*Explained simply.* Before any physics: an ordinary computer stores bits, one pattern at a time. A qubit is a list of two numbers; squaring them gives the odds of reading 0 or 1. Three everyday pictures (a spinning coin, ripples on water, a maze where wrong paths cancel) explain the ideas, and the notebook says clearly where each picture stops being true. All the maths is taught from zero with numbers you can check by hand.

*Tiny example.* The arrow `[0.6, 0.8]` has length 1, so it is a valid qubit with probabilities 0.36 and 0.64. A coin flipped twice stays 50/50, but H applied twice brings a qubit back to 0 for sure: the two paths to 1 have amplitudes +0.5 and −0.5 and cancel. A Bell pair measured 1000 times gives only `00` and `11`.

*You will learn:*
- bits, bytes and logic gates; what changes with qubits;
- the **spinning coin**, **ripples** and **maze** pictures, and where each one breaks;
- **complex numbers** (just enough), **vectors** as arrows, **matrices** as machines, **probabilities as squared lengths**;
- a **qubit** as a 2-number list, a **gate** as a 2x2 matrix (X, Z, H), **measurement** as sampling (coin vs qubit simulated);
- why the list **doubles** with each qubit ($2^n$, plotted with memory needs);
- **entanglement** with a simulated Bell pair, and **interference** (H then H);
- **myths vs facts**, the **Quantum Computing vs Quantum AI vs Quantum ML** map, a 20-term **glossary** and a 10-question **self-check quiz**.

*Key takeaway:* a quantum computer is not a faster laptop that tries every answer. Its power comes from interference, and only for problems with special structure.

#### 01 · Quantum computing basics

*Explained simply.* A qubit is a list of two numbers (amplitudes); squaring their sizes gives the odds of reading 0 or 1. Gates are rotations of that list, written as small matrices. Many qubits together need $2^n$ numbers, which is why big quantum systems are so hard to simulate on a laptop. You write the simulator yourself, about 60 lines of numpy, and use it for everything that follows.

*Tiny example.* After H on qubit 0 and a CNOT from qubit 0 to qubit 1, the simulator prints only two amplitudes, $\lvert00\rangle$ and $\lvert11\rangle$, each 0.707. In 1000 shots it measures `00` 503 times and `11` 497 times, and never `01` or `10`. That is the entangled **Bell state**. A "CNOT copier" copies $\lvert0\rangle$ and $\lvert1\rangle$ perfectly (fidelity 1.00), but copying $\lvert+\rangle$ only reaches fidelity 0.50: the **no-cloning theorem** in action.

*You will learn:*
- bits vs qubits, superposition, amplitudes, complex numbers and the **Born rule**;
- **measurement**, collapse and **shots** (error shrinking like $1/\sqrt{\text{shots}}$);
- the **Bloch sphere**, global and relative phase;
- gates **X, Y, Z, H, S, T, RX, RY, RZ, CNOT** as unitary matrices;
- **tensor products**, and the memory needed for 10 to 50 qubits (17 GB at 30 qubits);
- a numpy **statevector simulator** (`QSim`) with `measure(shots)` and histograms, checked against `np.kron`;
- **entanglement** (the four Bell states, GHZ), **interference** (H H = I, H Z H = X) and **no-cloning**.

*Key takeaway:* quantum computing is linear algebra with complex numbers plus random sampling at the end. The power comes from interference, not from "trying all answers at once".

#### 02 · Quantum algorithms

*Explained simply.* Most quantum algorithms follow one pattern: spread the amplitudes out (superposition), mark the answers with a minus sign (an **oracle**), make the marks visible by interference, then measure. Grover search makes the marked answer "louder" every round. Shor's algorithm turns factoring into finding the period of a repeating sequence, which the **quantum Fourier transform** does well. **Variational** algorithms (VQE, QAOA) put a short quantum circuit inside a classical optimisation loop.

*Tiny example.* Grover on 3 qubits finds `101` with probability 0.125 → 0.781 → 0.945 after 0, 1 and 2 rounds, then **overshoots** (0.330 after 3 rounds). Shor's period-finding step for $N = 15$, $a = 7$ finds the period $r = 4$, and $\gcd(7^2 \pm 1, 15)$ gives the factors 3 and 5. VQE reaches the exact ground energy −1.4142 of a 2-qubit Ising model. QAOA on a 4-node graph reaches an approximation ratio of 0.81 with one layer and 0.94 with two, with 85% of shots landing on an optimal cut.

*You will learn:*
- oracles, **phase kickback** and query counting;
- **Deutsch-Jozsa** and **Bernstein-Vazirani** (and why they are teaching examples, not useful speedups);
- **Grover search** and **amplitude amplification**, the $\frac{\pi}{4}\sqrt N$ rule, and its practical limits;
- the **QFT** built from H, controlled-phase and SWAP gates (checked against the matrix and numpy's FFT), and **phase estimation**;
- **Shor's algorithm**, published resource estimates for RSA-2048, and **post-quantum cryptography** (ML-KEM, ML-DSA, SLH-DSA);
- **VQE** (Pauli-term measurement from shots, COBYLA) and **QAOA** for MaxCut (landscape heatmap, p = 1 and p = 2);
- a table of **speedup types**: exponential, quadratic, and none known.

*Key takeaway:* proven big speedups are rare and need error-corrected machines; the heuristic NISQ algorithms (VQE, QAOA) have no demonstrated advantage over strong classical methods.

### Part 2: Quantum AI and Quantum ML (03, 04, 05)

#### 03 · Quantum machine learning

*Explained simply.* QML puts data into a quantum circuit (by turning numbers into rotation angles), lets a circuit with adjustable angles transform it, and reads out an average measurement as the prediction. The angles are trained like neural-network weights. Gradients come from running the circuit twice with an angle shifted by ±90° (the **parameter-shift rule**). It works, but on classical data it does not beat good classical models, and deep random circuits become untrainable (**barren plateaus**).

*Tiny example.* On 100 make_moons points (70 train, 30 test), the 12-angle variational classifier reaches **0.93** test accuracy. Logistic regression gets 0.83, a tiny MLP 0.90 and an RBF SVM **0.93**, each in milliseconds. A quantum-kernel SVM, with its input scale chosen by cross-validation, gets 0.77. In the barren-plateau experiment the gradient variance of deep random circuits falls from 0.12 (2 qubits) to 0.0021 (9 qubits), roughly halving with each extra qubit, while a shallow circuit stays near 0.15.

*You will learn:*
- the **CC / CQ / QC / QQ** map of quantum machine learning;
- **basis, angle and amplitude encoding**, and **data re-uploading** (more repeats = higher Fourier frequencies);
- **variational circuits** as "quantum neural networks", and a batched numpy simulator for training;
- the **parameter-shift rule**, checked against finite differences (agreement to about $10^{-11}$), and why it survives shot noise better;
- training a **variational classifier** with Adam and plotting its **decision boundary**;
- **quantum fidelity kernels**, the ZZ feature map, `SVC(kernel="precomputed")`, cross-validated scaling, and shot costs;
- **hybrid models**, **quantum RL** and **quantum GANs** (conceptual);
- limits: **barren plateaus**, noise, the **data-loading bottleneck**, **dequantization** (Tang 2018), kernel concentration.

*Key takeaway:* QML is a serious research field, but for classical data today, **classical models usually win**. Always ask for the classical baseline.

#### 04 · Tools, hardware and industry

*Explained simply.* The ideas from notebooks 01-03 are written here in the two most popular quantum SDKs, Qiskit and PennyLane. Then the notebook steps back: what qubits are physically made of, why noise is the main enemy, how error correction turns many bad qubits into one good one, how classical AI is already helping to build quantum computers, which industry promises are realistic, and why every AI team should start moving to post-quantum cryptography.

*Tiny example.* With depolarizing noise of p = 0.1 per gate, the Bell state's correlations drop from 1.0 to about 0.77 ($\langle ZZ\rangle$) and 0.61 ($\langle XX\rangle$). Zero-noise extrapolation lifts a noisy 0.82 back to 0.96 (ideal 1.0). In a distance-5 repetition code with correlated "burst" errors, a small neural-network decoder cuts the logical error rate from 0.056 (textbook minimum-weight decoder) to 0.043.

*You will learn:*
- **Qiskit** (`QuantumCircuit`, `Statevector`, `StatevectorSampler`, `StatevectorEstimator`, parameters) and **PennyLane** (QNodes, `qml.probs`, `FlipSign`, `GroverOperator`, autograd training), plus **bit-order** pitfalls; Cirq, Braket, Azure Quantum, CUDA-Q, pytket and Stim;
- **hardware modalities**: superconducting, trapped ion, neutral atom, photonic, spin and topological;
- **decoherence (T1, T2)**, gate and readout errors, and a **depolarizing-noise** simulation;
- **error mitigation** (zero-noise extrapolation) vs **quantum error correction** (repetition code, threshold, **surface code**, logical vs physical qubits, below-threshold results reported since 2024);
- **AI for quantum** (neural decoders, RL for calibration and control, LLMs for quantum code) vs **quantum for AI**;
- realistic **industry use cases** with caveats (chemistry and materials, optimisation, finance);
- **post-quantum cryptography**: ML-KEM, ML-DSA, SLH-DSA, "harvest now, decrypt later", crypto agility, and a toy **learning-with-errors** example;
- how to use **IBM Quantum, Amazon Braket and Azure Quantum** (code shown, not run), and a **career roadmap**.

*Key takeaway:* the most useful thing an AI engineer can do with quantum today is often **AI for quantum** or a **post-quantum migration**, not quantum machine learning.

#### 05 · Quantum ML on sensor data: fall detection

*Explained simply.* A watch or pendant with an accelerometer should call for help when its wearer falls. A fall shows up as a moment of near weightlessness, a hard impact spike, then stillness. This notebook simulates such data for 8 people, turns each 4-second window into 4 features, encodes them as qubit angles, and tests whether quantum classifiers do better than classical ones, using the evaluation a real product team would use: test on people the model has never seen, and count missed falls and false alarms, not just accuracy.

*Tiny example.* Falls are 9% of the 528 windows, so "never alarm" scores 91% accuracy and catches nothing. With leave-one-subject-out testing, the learned classical models and the quantum models all catch most falls with F1 around 0.8-0.9; repeating on new random datasets shows the gaps between them are within noise, with the classical RBF SVM on 4 features best on average. With 10 shots per prediction the variational classifier's F1 drops from 0.86 to 0.67, and at a few percent error per gate simulated hardware noise makes it flag almost everything as a fall.

*You will learn:*
- fall detection as an ML problem: rare events, hard negatives (jumps, sofa drops), new users;
- simulating accelerometer windows and extracting **peak, min, post-impact variance and jerk**;
- **features to angles** (standardise, PCA, min-max to [0, π]) and **qubit count vs feature count**;
- **leave-one-subject-out** cross-validation with **sensitivity, specificity, false alarms and F1**;
- a fair comparison: threshold rule, logistic regression, RBF SVM, MLP, a **variational quantum classifier** (parameter-shift gradients) and a **quantum-kernel SVM**, with matched inputs and repeated datasets;
- **encoding choices**: angle encoding without entanglement and amplitude encoding are classical kernels in disguise;
- **shot noise** and simulated **hardware noise** (density matrix, depolarizing and readout errors);
- the **cost** in circuit runs and shots, and an optional PennyLane/Qiskit cross-check.

*Key takeaway:* on classical sensor data, quantum classifiers at best tie classical ones, while costing far more and suffering from shots and noise. Use classical models for products today; QML research matters most for quantum data. The classical deep dive on this task is [26_Sensor_AI/02_imu_activity_recognition_and_fall_detection.ipynb](../26_Sensor_AI/02_imu_activity_recognition_and_fall_detection.ipynb).

---

## How this connects to the rest of the repo and to real AI systems

- **Linear algebra and probability** are the whole language of this track: [linear algebra](../14_Mathematics/01_linear_algebra.ipynb), [numerical linear algebra](../14_Mathematics/10_numerical_linear_algebra.ipynb), [probability](../14_Mathematics/03_probability.ipynb).
- **Kernels and SVMs**: quantum kernels plug straight into the classical SVM from [05_svm](../03_Machine_Learning/01_supervised/05_svm.ipynb).
- **Gradient-based training**: the variational classifier uses the same loss/optimiser ideas as [neural network fundamentals](../05_Deep_Learning/01_neural_network_fundamentals.ipynb) and [optimizers](../05_Deep_Learning/02_optimizers.ipynb); the parameter-shift rule replaces backpropagation.
- **Optimisation**: VQE and QAOA are hybrid optimisation loops, see [optimization](../14_Mathematics/06_optimization.ipynb) and [local search](../00_AI_Fundamentals/classical_ai/04_local_search_and_optimization.ipynb) for the classical side.
- **Reinforcement learning** for calibration and control (notebook 04) builds on [RL fundamentals](../11_Reinforcement_Learning/01_rl_fundamentals.ipynb).
- **Security of AI systems**: post-quantum cryptography protects model weights, training data and API traffic; see [privacy](../19_AI_Ethics_and_Safety/03_privacy.ipynb) and [deployment](../16_Deployment/).
- **Honest benchmarking**: evaluate any quantum claim like any research claim, with baselines, ablations and error bars, see [experiment design](../24_Research_Methods/02_experiment_design_for_ml.ipynb). Notebook 05 is a worked example.
- **Sensor AI**: notebook 05 applies QML to wearable fall detection; the classical side (signals, features, deep models) is in [26_Sensor_AI/02_imu_activity_recognition_and_fall_detection.ipynb](../26_Sensor_AI/02_imu_activity_recognition_and_fall_detection.ipynb).
- **Deeper study guide** for this track: [notes/25_Quantum_AI.md](notes/25_Quantum_AI.md).

---

## Common beginner mistakes

- **"A quantum computer tries every answer in parallel."** One measurement gives only n bits. The speedup comes from interference, and only for problems with special structure.
- **Forgetting that every number is a shot estimate.** A probability read from hardware has an error of about $1/\sqrt{\text{shots}}$; a 1000-shot estimate is only good to about ±3%.
- **Mixing up bit order.** Qiskit prints qubit 0 as the **right-most** bit; this track (and PennyLane) puts qubit 0 on the left.
- **Running too many Grover rounds.** Success probability goes up and then down again; about $\frac{\pi}{4}\sqrt N$ rounds is best.
- **Counting qubits, not quality.** A machine with more qubits but higher error rates can be less useful. Ask for 2-qubit error rates and whether qubits are physical or logical.
- **Benchmarking QML without a classical baseline.** Notebook 03 shows a quantum classifier merely matching an RBF SVM that trains in milliseconds.
- **Trusting one lucky run.** In notebook 05 a quantum model "wins" on one dataset by 2 windows; repeating on new datasets shows it was noise. Use matched inputs, leave-one-subject-out testing and several runs.
- **Reporting accuracy on rare events.** For fall detection, "never alarm" gets 91% accuracy. Report sensitivity, specificity, false alarms and F1.
- **Using finite differences for gradients on hardware.** Shot noise swamps them; use the parameter-shift rule.
- **Thinking post-quantum cryptography can wait until quantum computers arrive.** Data stolen today can be decrypted later, and migrations take years.

---

## Exam / interview quick-revision

1. **Bit vs qubit?** → A bit is 0 or 1; a qubit has two complex amplitudes, and measuring gives 0 or 1 with probability equal to the squared size of each amplitude.
2. **What makes a gate valid?** → It is a unitary matrix ($U^\dagger U = I$): it keeps total probability at 1 and is reversible.
3. **How do you make a Bell state?** → H on qubit 0, then CNOT from qubit 0 to qubit 1: $(\lvert00\rangle + \lvert11\rangle)/\sqrt2$.
4. **Why is simulating 50 qubits hard?** → A general state needs $2^{50}$ complex amplitudes, about 18 PB of memory.
5. **What does the no-cloning theorem say?** → No operation can copy an unknown quantum state.
6. **Grover's speedup?** → Quadratic: about $\frac{\pi}{4}\sqrt N$ queries instead of about $N/2$.
7. **Which step of Shor is quantum?** → Period finding (phase estimation with the QFT); the rest is classical number theory.
8. **What is VQE?** → A hybrid loop that minimises the measured energy $\langle\psi(\theta)\vert H\vert\psi(\theta)\rangle$ of a parameterised circuit.
9. **Parameter-shift rule?** → $\partial\langle O\rangle/\partial\theta = [\langle O\rangle(\theta+\pi/2) - \langle O\rangle(\theta-\pi/2)]/2$ for Pauli-rotation gates.
10. **What is a quantum kernel?** → $k(x,x') = \lvert\langle\phi(x)\vert\phi(x')\rangle\rvert^2$ for a quantum feature map $\phi$, given to a classical SVM.
11. **What is a barren plateau?** → Gradients whose variance shrinks exponentially with the number of qubits, making training impossible.
12. **What is dequantization?** → A classical algorithm that matches a claimed quantum speedup under comparable data-access assumptions (e.g. Tang's recommendation algorithm).
13. **Error mitigation vs error correction?** → Mitigation post-processes noisy results (more shots); correction encodes logical qubits in many physical qubits and fixes errors during the run.
14. **What does "below threshold" mean?** → Physical errors are rare enough that a bigger error-correcting code lowers the logical error rate.
15. **What are ML-KEM and ML-DSA?** → NIST's lattice-based post-quantum standards (FIPS 203 for key exchange, FIPS 204 for signatures), published in 2024.
16. **Quantum Computing vs Quantum AI vs Quantum ML?** → Quantum computing is the foundation (qubits, gates, algorithms); quantum AI is where it meets AI, in two directions (quantum for AI and AI for quantum); quantum ML is the "quantum for AI" part.
17. **Why does a quantum classifier on accelerometer features rarely help?** → The data is classical and small, one qubit per feature limits the input, shots and noise add error, training costs many circuit runs, and a few-qubit circuit is classically simulable anyway.

---

## Further reading

**Textbooks**
- M. A. Nielsen and I. L. Chuang, *Quantum Computation and Quantum Information*, Cambridge University Press, 10th anniversary edition, 2010. The standard reference.
- M. Schuld and F. Petruccione, *Machine Learning with Quantum Computers*, Springer, 2nd ed., 2021. The standard QML textbook.

**Free courses and documentation**
- Qiskit documentation and IBM Quantum Learning (the successor of the free Qiskit textbook).
- PennyLane documentation and QML demos (pennylane.ai/qml).
- Cirq, Amazon Braket, Azure Quantum and Stim documentation.

**Key papers**
- J. Preskill, "Quantum Computing in the NISQ era and beyond", *Quantum* 2, 79 (2018), arXiv:1801.00862.
- J. R. McClean et al., "Barren plateaus in quantum neural network training landscapes", *Nature Communications* 9 (2018), arXiv:1803.11173.
- V. Havlíček et al., "Supervised learning with quantum-enhanced feature spaces", *Nature* 567 (2019), arXiv:1804.11326.
- P. W. Shor, "Polynomial-Time Algorithms for Prime Factorization and Discrete Logarithms on a Quantum Computer", *SIAM Journal on Computing*, 1997.
- L. K. Grover, "A fast quantum mechanical algorithm for database search", STOC 1996.
- E. Farhi, J. Goldstone and S. Gutmann, "A Quantum Approximate Optimization Algorithm", arXiv:1411.4028 (2014).
- E. Tang, "A quantum-inspired classical algorithm for recommendation systems", STOC 2019, arXiv:1807.04271.
- NIST FIPS 203 (ML-KEM), FIPS 204 (ML-DSA) and FIPS 205 (SLH-DSA), 2024.
