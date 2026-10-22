# Glossary: AI, ML, Deep Learning, LLM and MLOps Terms in Plain English

**Jump to:** [A](#a) · [B](#b) · [C](#c) · [D](#d) · [E](#e) · [F](#f) · [G](#g) · [H](#h) · [I](#i) · [J](#j) · [K](#k) · [L](#l) · [M](#m) · [N](#n) · [O](#o) · [P](#p) · [Q](#q) · [R](#r) · [S](#s) · [T](#t) · [U](#u) · [V](#v) · [W](#w) · [X](#x) · [Y](#y) · [Z](#z)

## How to use this glossary

- **Stuck on a word?** Press `Ctrl+F` (or `Cmd+F` on a Mac), type the word, and jump straight to it. Terms are sorted A to Z, and abbreviations are spelled out (for example, *RAG* is under **R**).
- **Each entry has three parts:** a short plain-English definition, an everyday analogy or tiny example (where it helps), and a **See:** link to the notebook or notes file in this repo where the idea is taught best. All links are relative, so they work on GitHub and in your editor.
- **You don't need to read it front to back.** Come back whenever a notebook uses a word you don't know yet. Words in *italics* inside a definition usually have their own entry.
- **Definitions are kept simple on purpose.** They give you the main idea, not every technical detail. The linked notebook has the full story, with code.

---

## A

**A/B Testing** — An experiment where you show two versions of something (A = the current one, B = the new one) to two random groups of users and measure which works better. *Example:* half of your visitors see a green "Buy" button and half see a blue one, then you compare how many people buy. See: [03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb](03_Machine_Learning/11_ab_testing/01_ab_testing.ipynb)

**Accuracy** — The share of predictions a model gets right: correct predictions divided by all predictions. It can mislead when one class is rare: a model that always says "no fraud" is 99% accurate if only 1% of cases are fraud. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Activation Function** — A simple math function applied to each neuron's output that lets a neural network learn curved, non-straight-line patterns. Common ones are *ReLU*, *sigmoid* and tanh. Without it, stacking layers would be no more powerful than one straight line. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Active Learning** — A way to save labeling effort: the model picks the examples it is most unsure about and asks a human to label only those. *Analogy:* a student who asks the teacher only about the questions they find confusing. See: [03_Machine_Learning/13_active_learning/01_active_learning.ipynb](03_Machine_Learning/13_active_learning/01_active_learning.ipynb)

**Adam (optimizer)** — A popular *optimizer* for training neural networks. It adjusts the step size for each weight separately, using running averages of recent gradients and their squares, so training is usually fast and stable without much tuning. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Adversarial Example** — An input changed very slightly, often invisibly to people, on purpose to fool a model. *Example:* adding faint noise to a photo of a panda so an image classifier confidently says "gibbon". See: [19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb](19_AI_Ethics_and_Safety/02_adversarial_attacks.ipynb)

**Agent (AI Agent)** — A program where a language model decides what to do step by step: it reads a goal, chooses a *tool* (search, calculator, code), looks at the result, and repeats until the task is done. *Analogy:* an assistant who can not only answer but also use apps for you. See: [10_Agents/01_agent_fundamentals.ipynb](10_Agents/01_agent_fundamentals.ipynb)

**Alignment** — Making an AI system behave the way people intend: helpful, honest, and avoiding harm. In LLMs this is done with techniques such as *instruction tuning*, *RLHF* and *DPO*. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**Anomaly Detection** — Finding data points that look very different from normal ones. *Example:* a credit-card purchase of $5,000 in another country at 3 a.m. for a customer who usually spends $20 locally. See: [03_Machine_Learning/08_anomaly_detection/01_anomaly_detection.ipynb](03_Machine_Learning/08_anomaly_detection/01_anomaly_detection.ipynb)

**API (Application Programming Interface)** — A defined way for one program to ask another program for something. A web API receives a request over the internet (for example "predict the price of this house") and sends back a response, usually as *JSON*. *Analogy:* a restaurant menu and waiter: you order from a fixed list without going into the kitchen. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

**ARIMA** — A classic time-series forecasting model (AutoRegressive Integrated Moving Average). It predicts the next value from recent past values and recent past errors, after "differencing" the data to remove trends. See: [04_Forecasting/02_classical_methods.ipynb](04_Forecasting/02_classical_methods.ipynb)

**Artificial Intelligence (AI)** — The broad field of making computers do tasks that normally need human intelligence, such as understanding language, recognizing images or making decisions. *Machine learning* is the main way modern AI is built. See: [00_AI_Fundamentals/notes/00_AI_Fundamentals.md](00_AI_Fundamentals/notes/00_AI_Fundamentals.md)

**Attention** — The key idea inside *transformers*: when processing one word, the model looks at all the other words and decides how much each one matters. In "The animal didn't cross the street because **it** was tired", attention helps link "it" to "animal". When a sequence looks at itself like this it is called *self-attention*. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

**AUC / ROC Curve** — The ROC curve plots how many true positives you catch against how many false alarms you raise as you move the decision threshold. AUC (Area Under the Curve) sums it up as one number from 0.5 (coin flip) to 1.0 (perfect). It equals the chance that a random positive example gets a higher score than a random negative one. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**Autograd (Automatic Differentiation)** — A library feature (in PyTorch, for example) that works out *gradients* for you automatically, by recording every math operation and applying the chain rule of calculus backwards. This is what makes *backpropagation* easy. See: [14_Mathematics/02_calculus.ipynb](14_Mathematics/02_calculus.ipynb)

## B

**Backpropagation** — The method neural networks use to learn: after a prediction, compute how wrong it was (the *loss*), then work backwards through the layers to find how much each weight contributed to the error, so each weight can be nudged in the right direction. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Batch / Mini-batch / Batch Size** — Instead of learning from one example or the whole dataset at once, neural networks usually learn from small groups called mini-batches (for example 32 examples). The batch size is how many examples are in each group. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**Bayes' Theorem** — A formula for updating a belief when you see new evidence: new belief = old belief × how well the evidence fits, rescaled. *Example:* how likely you are to have a disease given a positive test depends on how common the disease is, not just on how accurate the test is. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**BERT** — A well-known *transformer* model (from 2018) that reads text in both directions at once. It is an *encoder* model, good at understanding tasks such as classification, search and named-entity recognition rather than writing long text. See: [07_NLP/notes/07_NLP.md](07_NLP/notes/07_NLP.md)

**Bias (Fairness)** — When an AI system treats some groups of people unfairly, often because its training data reflected past unfairness. *Example:* a hiring model trained on past hires that mostly favored one group learns to repeat that preference. See: [19_AI_Ethics_and_Safety/01_bias_fairness.ipynb](19_AI_Ethics_and_Safety/01_bias_fairness.ipynb)

**Bias-Variance Tradeoff** — Two ways a model can be wrong. *Bias*: it is too simple and misses the pattern (*underfitting*). *Variance*: it is too sensitive to the exact training data (*overfitting*). Making a model more flexible usually lowers bias but raises variance, so you look for a balance. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**BLEU / ROUGE** — Scores that compare generated text with a human-written reference by counting overlapping words and word sequences. BLEU is common for translation, ROUGE for summaries. They are fast and cheap, but they miss meaning (a correct paraphrase can score low). See: [08_LLM/08_evaluation/01_llm_evaluation.ipynb](08_LLM/08_evaluation/01_llm_evaluation.ipynb)

**BM25** — A classic keyword-search scoring formula. A document scores higher when it contains the query's words often, especially rare words, with an adjustment so long documents don't win just by being long. It is still a strong baseline and is often combined with *embeddings* in "hybrid search", which merges keyword and meaning-based results. See: [08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb](08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb)

**Boosting / Gradient Boosting** — Building a strong model from many small, weak ones (usually shallow *decision trees*) trained one after another, where each new tree focuses on fixing the mistakes of the trees before it. *XGBoost* and LightGBM are popular libraries for this. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

## C

**Causal Inference** — Methods for answering "did X actually *cause* Y?" rather than just "do X and Y move together?". *Example:* did the discount email cause more purchases, or were the people who got it already more likely to buy? See: [03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb](03_Machine_Learning/10_causal_inference/01_causal_inference.ipynb)

**Chain of Thought (CoT)** — A prompting technique that asks the model to show its reasoning step by step before giving the final answer. It often improves accuracy on math and logic problems. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

**Chunking** — Cutting long documents into smaller pieces (chunks) before turning them into *embeddings* for search or *RAG*. Chunks that are too big blur the meaning; chunks that are too small lose context. See: [08_LLM/02_rag/01_rag_fundamentals.ipynb](08_LLM/02_rag/01_rag_fundamentals.ipynb)

**CI/CD (Continuous Integration / Continuous Delivery)** — Automation that runs tests on every code change (CI) and, if they pass, packages and ships the change (CD). For ML this can also include data checks and model-quality checks. See: [15_MLOps/04_ci_cd_for_ml/01_cicd_ml.ipynb](15_MLOps/04_ci_cd_for_ml/01_cicd_ml.ipynb)

**Class Imbalance** — When one category is much rarer than another in your data (for example 1 fraud case per 1,000 transactions). Models then tend to ignore the rare class unless you rebalance the data, reweight the classes or pick better metrics. See: [03_Machine_Learning/05_feature_engineering/02_imbalanced_data.ipynb](03_Machine_Learning/05_feature_engineering/02_imbalanced_data.ipynb)

**Classification** — A *supervised learning* task where the answer is a category. *Examples:* spam or not spam, which digit (0-9) is in an image. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**Clustering** — Grouping similar data points together without being told the groups in advance (*unsupervised learning*). *Example:* splitting customers into "bargain hunters", "loyal regulars" and so on based on how they shop. See: [03_Machine_Learning/02_unsupervised/01_clustering.ipynb](03_Machine_Learning/02_unsupervised/01_clustering.ipynb)

**CNN (Convolutional Neural Network)** — A neural network designed for grid-like data such as images. It slides small filters across the image to detect edges, then shapes, then objects, layer by layer. See: [05_Deep_Learning/03_cnn.ipynb](05_Deep_Learning/03_cnn.ipynb)

**Confusion Matrix** — A small table that counts a classifier's results: true positives, false positives, true negatives and false negatives. It shows *which* mistakes a model makes, not just how many. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Container** — A lightweight, self-contained package of an app plus everything it needs to run (code, libraries, settings), so it runs the same on any machine. *Docker* is the most common tool for building them. *Analogy:* a shipping container that fits on any ship or truck. See: [17_Docker/01_docker_basics.ipynb](17_Docker/01_docker_basics.ipynb)

**Context Window** — The maximum amount of text (measured in *tokens*) an LLM can look at in one go, including your prompt, any documents you paste in, and its own reply. Anything beyond it is cut off or forgotten. See: [08_LLM/04_different_llms/notes/04_different_llms.md](08_LLM/04_different_llms/notes/04_different_llms.md)

**Correlation** — A number from -1 to +1 showing how strongly two things move together in a straight-line way. +1 means they rise together perfectly, -1 means one rises as the other falls, and 0 means no linear link. Correlation does not prove causation. See: [02_Data_Analysis/notes/02_Data_Analysis.md](02_Data_Analysis/notes/02_Data_Analysis.md)

**Cosine Similarity** — A measure of how similar two vectors (such as two *embeddings*) are by the angle between them: 1 means pointing the same way (very similar), 0 means unrelated. It is the standard way to compare text embeddings. See: [07_NLP/09_sentence_embeddings_advanced.ipynb](07_NLP/09_sentence_embeddings_advanced.ipynb)

**Cross-Encoder / Reranker** — A model that reads a query and one document *together* and scores how relevant they are. It is more accurate but slower than comparing embeddings, so it is typically used to re-sort the top results from a fast first search. See: [08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb](08_LLM/02_rag/04_advanced_retrieval_and_reranking.ipynb)

**Cross-Entropy Loss** — The usual *loss function* for classification. It is small when the model gives high probability to the correct answer and grows sharply when the model is confidently wrong. See: [14_Mathematics/05_information_theory.ipynb](14_Mathematics/05_information_theory.ipynb)

**Cross-Validation** — A fairer way to test a model: split the data into k parts (folds), train on k-1 of them and test on the remaining one, rotate through all folds, then average the scores. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

## D

**Data Augmentation** — Creating extra training examples by making small, realistic changes to existing ones, such as flipping, rotating or cropping images. This helps the model generalize instead of memorizing. See: [06_Computer_Vision/02_image_classification.ipynb](06_Computer_Vision/02_image_classification.ipynb)

**Data Drift** — When the inputs a model sees in production gradually become different from the data it was trained on (for example, customers get younger, or prices rise with inflation). Monitoring catches drift so you know when to retrain. (When the link between inputs and the right answer changes instead, it is called concept drift.) See: [15_MLOps/06_monitoring/01_monitoring.ipynb](15_MLOps/06_monitoring/01_monitoring.ipynb)

**Data Leakage** — When information that would not be available at prediction time sneaks into training, making test scores look great but real-world results poor. *Example:* scaling data using statistics from the whole dataset, including the test set. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**DataFrame** — A table of data in Python (rows and named columns), like a spreadsheet you can program. It is the main object in the *pandas* library. See: [02_Data_Analysis/03_pandas.ipynb](02_Data_Analysis/03_pandas.ipynb)

**Decision Tree** — A model that makes predictions by asking a series of yes/no questions about the features, like a flowchart: "Is income > 50k? → Is age < 30? → Approve". Easy to explain, but a single deep tree overfits easily. See: [03_Machine_Learning/01_supervised/03_decision_trees.ipynb](03_Machine_Learning/01_supervised/03_decision_trees.ipynb)

**Deep Learning** — *Machine learning* with neural networks that have many layers ("deep"). Each layer learns more abstract features than the one before. It powers modern image recognition, speech and LLMs. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**Deployment** — Putting a trained model somewhere real users or systems can use it, for example behind a web *API*, inside a mobile app, or as a nightly batch job. See: [16_Deployment/01_deployment_concepts.ipynb](16_Deployment/01_deployment_concepts.ipynb)

**Derivative / Gradient** — A derivative tells you how fast a function's output changes when you change its input a tiny bit (its slope). A gradient is the same idea for many inputs at once: a list of slopes, one per input, pointing in the direction of steepest increase. See: [14_Mathematics/02_calculus.ipynb](14_Mathematics/02_calculus.ipynb)

**Differential Privacy** — A mathematical privacy guarantee: add carefully measured random noise to results so that whether any single person's data is included barely changes the output. A setting called epsilon controls the privacy-versus-accuracy tradeoff. See: [19_AI_Ethics_and_Safety/03_privacy.ipynb](19_AI_Ethics_and_Safety/03_privacy.ipynb)

**Diffusion Model** — A generative model that learns to remove noise step by step. To create an image, it starts from pure random noise and gradually "denoises" it into a picture that matches the prompt. See: [06_Computer_Vision/06_image_generation.ipynb](06_Computer_Vision/06_image_generation.ipynb)

**Dimensionality Reduction** — Shrinking data with many columns into fewer columns while keeping most of the useful information, for speed or for plotting in 2D. *PCA*, t-SNE and UMAP are common methods. See: [03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb](03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb)

**Docker** — The most popular tool for building and running *containers*. You describe your app's environment in a `Dockerfile`, build it into an image (a ready-to-run template), and run that image anywhere Docker is installed. See: [17_Docker/01_docker_basics.ipynb](17_Docker/01_docker_basics.ipynb)

**Dot Product** — Multiply two lists of numbers position by position and add up the results: [1,2]·[3,4] = 1×3 + 2×4 = 11. It measures how much two vectors point the same way and is everywhere in ML, from linear models to *attention*. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**DPO (Direct Preference Optimization)** — A way to *align* an LLM using pairs of answers where humans marked one as better. It trains the model directly to prefer the better answer, without the separate reward model and reinforcement-learning loop that *RLHF* uses. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**Dropout** — A training trick where a random fraction of neurons is temporarily switched off at each step, so the network can't rely too heavily on any single neuron. It reduces *overfitting* and is turned off at prediction time. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

## E

**Early Stopping** — Stopping training when the score on validation data stops improving, even if training could continue. This prevents the model from starting to *overfit*. See: [05_Deep_Learning/16_industry_pytorch_training_pipeline.ipynb](05_Deep_Learning/16_industry_pytorch_training_pipeline.ipynb)

**EDA (Exploratory Data Analysis)** — The first look at a dataset: summary numbers, missing values, distributions, outliers and relationships, mostly through tables and charts, before any modeling. See: [02_Data_Analysis/07_eda.ipynb](02_Data_Analysis/07_eda.ipynb)

**Embedding** — A list of numbers (a vector) that represents the meaning of something such as a word, sentence, image or product, so that similar things get similar vectors. *Example:* "puppy" and "dog" end up close together; "puppy" and "invoice" far apart. See: [07_NLP/02_word_embeddings.ipynb](07_NLP/02_word_embeddings.ipynb)

**Encoder / Decoder** — Two halves of many neural networks. The encoder reads the input and turns it into an internal representation; the decoder turns that representation into an output. *BERT* is encoder-only, most chat LLMs are decoder-only, and translation models often use both. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

**Endpoint** — One specific URL path of a web *API* that does one job, for example `POST /predict` or `GET /health`. See: [12_FastAPI/notes/12_FastAPI.md](12_FastAPI/notes/12_FastAPI.md)

**Ensemble** — Combining several models so their mistakes cancel out, for example by voting or averaging. Bagging (averaging many models trained on random samples), *boosting* and stacking are the main styles. *Analogy:* asking several doctors for an opinion instead of just one. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**Entropy** — A measure of uncertainty or surprise. A fair coin flip has high entropy (you can't guess it); a coin that always lands heads has zero entropy. It is used in decision trees and in *cross-entropy loss*. See: [14_Mathematics/05_information_theory.ipynb](14_Mathematics/05_information_theory.ipynb)

**Epoch** — One full pass through the entire training dataset. Training usually runs for many epochs. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**Experiment Tracking** — Automatically recording every training run's settings, code version, data version and results so you can compare runs and reproduce the best one. MLflow and Weights & Biases are common tools. See: [15_MLOps/01_experiment_tracking/01_mlflow.ipynb](15_MLOps/01_experiment_tracking/01_mlflow.ipynb)

**Explainability (XAI)** — Methods that help people understand *why* a model made a prediction, such as which features mattered most. Tools include *SHAP*, LIME and feature importance. See: [03_Machine_Learning/07_explainability/01_explainability.ipynb](03_Machine_Learning/07_explainability/01_explainability.ipynb)

## F

**F1 Score** — A single score that balances *precision* and *recall* (it is their harmonic mean). It is useful when classes are imbalanced and accuracy would mislead. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**Fairness Metrics (e.g. Demographic Parity)** — Numbers that check whether a model treats groups equally. Demographic parity, for example, asks whether different groups get positive outcomes (such as loan approvals) at similar rates. Different fairness definitions can conflict with each other. See: [19_AI_Ethics_and_Safety/01_bias_fairness.ipynb](19_AI_Ethics_and_Safety/01_bias_fairness.ipynb)

**False Positive / False Negative** — The two kinds of mistakes a yes/no classifier makes. A false positive is a false alarm (flagging a good email as spam); a false negative is a miss (letting spam through). See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**FastAPI** — A popular Python framework for building web *APIs* quickly. It uses Python type hints (labels like `age: int`) and *Pydantic* to check inputs automatically and creates interactive documentation for you. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

**Feature** — One input column a model uses to make a prediction. *Example:* for predicting a house price, features might be size, number of bedrooms and neighborhood. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Feature Engineering** — Creating better input columns from raw data so patterns are easier for a model to learn. *Example:* turning a timestamp into "hour of day" and "is weekend". See: [03_Machine_Learning/05_feature_engineering/01_feature_engineering.ipynb](03_Machine_Learning/05_feature_engineering/01_feature_engineering.ipynb)

**Few-Shot Prompting** — Putting a few worked examples in the prompt so the LLM can copy the pattern. *Example:* show three reviews with their sentiment labels, then give a fourth review to label. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

**Fine-Tuning** — Taking a model that has already been trained on lots of general data and training it a little more on your own, smaller dataset so it gets better at your specific task or style. See: [08_LLM/03_fine_tuning/01_fine_tuning.ipynb](08_LLM/03_fine_tuning/01_fine_tuning.ipynb)

**Forecasting** — Predicting future values of something measured over time, such as next week's sales or tomorrow's electricity demand. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Function Calling / Tool Calling** — An LLM feature where, instead of answering in plain text, the model outputs a structured request to run a specific function (for example `get_weather(city="Paris")`). Your code runs the function and passes the result back. This is how *agents* use tools. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

## G

**GAN (Generative Adversarial Network)** — Two networks trained against each other: a generator makes fake samples and a discriminator tries to tell fake from real. As they compete, the generator's fakes become more realistic. *Analogy:* a forger and a detective improving together. See: [05_Deep_Learning/06_generative_models.ipynb](05_Deep_Learning/06_generative_models.ipynb)

**Generalization** — How well a model performs on new data it hasn't seen during training. Good generalization, not a high training score, is the real goal. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Generative AI** — AI that creates new content (text, images, audio, code) rather than only classifying or predicting a number. LLMs and *diffusion models* are the best-known examples. See: [08_LLM/11_multimodal/01_multimodal_ai.ipynb](08_LLM/11_multimodal/01_multimodal_ai.ipynb)

**Git** — A version-control tool that records every change to your code as commits (saved snapshots), lets you work on separate branches (parallel lines of work), and lets teams merge their work safely. See: [20_Git_and_DevOps/01_git_basics.ipynb](20_Git_and_DevOps/01_git_basics.ipynb)

**GitHub Actions** — GitHub's built-in automation service. It runs scripts (tests, linting, building, deploying) automatically when something happens in a repository, such as a push or a pull request. It is a common way to do *CI/CD*. See: [20_Git_and_DevOps/03_github_actions_cicd.ipynb](20_Git_and_DevOps/03_github_actions_cicd.ipynb)

**GPU (Graphics Processing Unit)** — A chip with thousands of small cores that do many simple calculations in parallel. It makes training and running neural networks much faster than a normal CPU. You do not need one to start: the beginner and core notebooks in this repo are designed to run on a normal CPU. See: [05_Deep_Learning/11_distributed_training.ipynb](05_Deep_Learning/11_distributed_training.ipynb)

**Gradient Descent** — The basic way models learn: compute the *gradient* (which direction makes the error bigger), take a small step the opposite way, and repeat. *Analogy:* walking downhill in fog by always stepping where the ground slopes down. See: [14_Mathematics/06_optimization.ipynb](14_Mathematics/06_optimization.ipynb)

**Grid Search / Random Search** — Two simple ways to tune *hyperparameters*. Grid search tries every combination from a list; random search tries random combinations, which often finds good settings faster. See: [03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb](03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb)

**Guardrails** — Checks placed around an AI system to keep it safe and on-topic: filtering harmful inputs and outputs, blocking leaks of private data, validating formats, or refusing out-of-scope requests. See: [08_LLM/20_industry_llm_application_patterns.ipynb](08_LLM/20_industry_llm_application_patterns.ipynb)

## H

**Hallucination** — When an LLM states something false or made-up as if it were fact, such as an invented citation. *RAG*, careful prompting and evaluation help reduce it. See: [08_LLM/08_evaluation/notes/08_evaluation.md](08_LLM/08_evaluation/notes/08_evaluation.md)

**Hugging Face** — A company and platform that hosts thousands of open models and datasets and maintains libraries such as `transformers`, `datasets` and `sentence-transformers`. Many notebooks here load small models from it. See: [08_LLM/05_slms/01_small_language_models.ipynb](08_LLM/05_slms/01_small_language_models.ipynb)

**Hyperparameter** — A setting you choose *before* training rather than one the model learns, such as the *learning rate*, the number of trees, or the depth of a tree. Tuning them well can matter a lot. See: [03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb](03_Machine_Learning/06_model_evaluation/02_hyperparameter_optimization.ipynb)

**Hypothesis Test** — A statistical procedure for deciding whether an observed effect is likely real or could just be random luck. You assume "no effect" (the null hypothesis) and check how surprising the data would be under that assumption (the *p-value*). See: [02_Data_Analysis/08_statistics.ipynb](02_Data_Analysis/08_statistics.ipynb)

## I

**Imputation** — Filling in missing values in data, for example with the column's average or median, or with a model's best guess. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Inference** — Using a trained model to make predictions on new data, as opposed to training it. Most of a deployed model's cost and *latency* comes from inference. See: [08_LLM/13_inference_optimization.ipynb](08_LLM/13_inference_optimization.ipynb)

**Instruction Tuning / SFT (Supervised Fine-Tuning)** — *Fine-tuning* a pretrained language model on many examples of instructions paired with good responses, so it learns to follow requests and chat instead of just continuing text. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

## J

**Jailbreak** — A prompt crafted to trick an LLM into ignoring its safety rules, for example by role-play ("pretend you are an AI with no rules"). Defenses include *guardrails* and *red teaming*. See: [09_Prompt_Engineering/notes/09_Prompt_Engineering.md](09_Prompt_Engineering/notes/09_Prompt_Engineering.md)

**JSON** — A simple, human-readable text format for structured data, built from `{"key": "value"}` pairs and `[lists]`. It is the usual format for web *APIs* and for *structured outputs* from LLMs. See: [08_LLM/17_structured_outputs.ipynb](08_LLM/17_structured_outputs.ipynb)

**Jupyter Notebook** — An interactive document (`.ipynb`) that mixes runnable code cells, their outputs (tables, charts) and explanatory text. Every lesson in this repo is a Jupyter notebook. The program that runs the code behind it is called the kernel; "Restart kernel" clears its memory. See: [README.md](README.md)

## K

**K-Means** — A *clustering* algorithm: choose k, place k center points, assign each point to its nearest center, move each center to the middle of its points, and repeat until nothing changes. See: [03_Machine_Learning/02_unsupervised/01_clustering.ipynb](03_Machine_Learning/02_unsupervised/01_clustering.ipynb)

**KNN (K-Nearest Neighbors)** — A simple model that predicts by looking at the k most similar training examples and taking a vote (classification) or an average (regression). *Analogy:* guessing a house price from the prices of the five most similar houses nearby. See: [03_Machine_Learning/01_supervised/07_knn.ipynb](03_Machine_Learning/01_supervised/07_knn.ipynb)

**Knowledge Distillation** — Training a small "student" model to imitate a large "teacher" model's outputs, so you get most of the quality at a fraction of the size and cost. See: [05_Deep_Learning/08_model_compression.ipynb](05_Deep_Learning/08_model_compression.ipynb)

**Knowledge Graph** — Information stored as a network of facts in the form (thing) → relationship → (thing), such as (Paris) → capital_of → (France). LLM systems can query it to get precise, linked facts. See: [08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb](08_LLM/09_knowledge_graphs/01_knowledge_graphs.ipynb)

**Kubernetes (K8s)** — A system that runs and manages many *containers* across many machines: it starts them, restarts them if they crash, scales them up and down with traffic, and routes requests to them. See: [17_Docker/kubernetes/01_kubernetes.ipynb](17_Docker/kubernetes/01_kubernetes.ipynb)

**KV Cache (Key-Value Cache)** — A speed-up for LLM text generation. The model saves the *attention* "keys" and "values" it already computed for earlier tokens, so each new token only needs a small amount of new computation. It uses extra memory that grows with the length of the text. See: [08_LLM/13_inference_optimization.ipynb](08_LLM/13_inference_optimization.ipynb)

## L

**Label / Target** — The correct answer you want a model to predict, for example "spam" or the house price. In *supervised learning*, every training example comes with its label. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**LangChain / LangGraph** — Popular open-source Python libraries for building LLM applications. LangChain provides building blocks (prompts, retrievers, tool wrappers); LangGraph builds *agents* as graphs of steps with loops and saved state. See: [10_Agents/03_langgraph.ipynb](10_Agents/03_langgraph.ipynb)

**Latency / Throughput** — Latency is how long one request takes (for example 200 ms). Throughput is how many requests a system handles per second. Improving one can hurt the other (for example, batching raises throughput but can add latency). See: [15_MLOps/11_model_serving_advanced.ipynb](15_MLOps/11_model_serving_advanced.ipynb)

**Layer** — One stage of a neural network that transforms its input (for example a fully connected, convolutional or attention layer). Data flows through layers in order, from input to output. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Learning Rate** — How big a step the *optimizer* takes each time it updates the weights. Too big and training jumps around or blows up; too small and it crawls. Often the single most important *hyperparameter*. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Linear Regression** — The simplest model for predicting a number: fit the best straight line (or flat plane) through the data, so that prediction = weight × feature + bias. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**List Comprehension (Python)** — A compact way to build a list in one line: `[x * 2 for x in numbers if x > 0]` means "double every positive number". See: [01_Python/01_basic.ipynb](01_Python/01_basic.ipynb)

**LLM (Large Language Model)** — A very large neural network (usually a *transformer*) trained on huge amounts of text to predict the next *token*. That simple skill, at scale, lets it answer questions, summarize, translate and write code. See: [08_LLM/notes/08_LLM.md](08_LLM/notes/08_LLM.md)

**LLM-as-a-Judge** — Using one LLM to grade another model's answers against a rubric (for correctness, helpfulness, tone). It is cheaper than human review but can be biased, so it should be checked against human judgments. See: [08_LLM/08_evaluation/notes/08_evaluation.md](08_LLM/08_evaluation/notes/08_evaluation.md)

**Logistic Regression** — Despite the name, a *classification* model. It computes a weighted sum of the features and squashes it with the *sigmoid* function into a probability between 0 and 1. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**Logits** — The raw, unnormalized scores a model outputs before they are turned into probabilities (usually with *softmax*). Bigger logit = more likely. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**LoRA (Low-Rank Adaptation)** — A cheap way to *fine-tune* big models: keep the original weights frozen and train small add-on matrices instead. You train well under 1% of the parameters, and the add-on file is small. QLoRA does the same on top of a *quantized* model to save even more memory. See: [05_Deep_Learning/12_advanced_peft.ipynb](05_Deep_Learning/12_advanced_peft.ipynb)

**Loss Function** — A formula that measures how wrong a model's predictions are; training tries to make it as small as possible. *Examples:* mean squared error for numbers, *cross-entropy* for categories. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**LSTM (Long Short-Term Memory)** — A type of *RNN* with gates that control what to remember, forget and output. This lets it keep information over long sequences much better than a plain RNN. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

## M

**Machine Learning (ML)** — Teaching computers to find patterns from examples instead of writing every rule by hand. *Example:* instead of coding rules for spam, show the computer thousands of labeled emails and let it learn. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**MAE / MSE / RMSE** — Common error measures for predicting numbers. MAE (Mean Absolute Error) is the average size of the errors. MSE (Mean Squared Error) averages the squared errors, so it punishes big misses more. RMSE is the square root of MSE, which puts it back in the original units. See: [03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb](03_Machine_Learning/10_evaluation_metrics_comprehensive.ipynb)

**Matrix** — A rectangular grid of numbers. A dataset is a matrix (rows = examples, columns = features), and neural-network layers are mostly matrix multiplications. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**MCP (Model Context Protocol)** — An open standard for connecting AI applications to external tools and data sources in a uniform way. A tool written once as an "MCP server" can be used by any app that supports MCP. *Analogy:* a USB port for AI tools. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

**Memory (Agent)** — How an *agent* keeps information beyond a single step. Short-term memory is the current conversation in the *context window*; long-term memory is usually stored outside the model (for example in a *vector database*) and retrieved when needed. See: [10_Agents/02_memory_and_planning.ipynb](10_Agents/02_memory_and_planning.ipynb)

**MLOps** — The practices and tools for taking ML models from a notebook to reliable production and keeping them healthy: versioning, automated pipelines, testing, deployment, monitoring and retraining. *Analogy:* DevOps, but for models and data too. See: [15_MLOps/notes/15_MLOps.md](15_MLOps/notes/15_MLOps.md)

**Model Registry** — A central catalog of trained models with their versions, metrics and stage (for example "staging" or "production"), so teams know which model is live and can roll back. See: [15_MLOps/05_model_registry/01_model_registry.ipynb](15_MLOps/05_model_registry/01_model_registry.ipynb)

**Model Serving** — Running a trained model as a service that answers prediction requests, usually behind an *API*, with attention to speed, scaling and reliability. See: [12_FastAPI/03_ml_serving_with_fastapi.ipynb](12_FastAPI/03_ml_serving_with_fastapi.ipynb)

**Monitoring (ML)** — Continuously watching a deployed model's inputs, outputs, performance, latency and errors, with alerts when something drifts or breaks. See: [15_MLOps/06_monitoring/01_monitoring.ipynb](15_MLOps/06_monitoring/01_monitoring.ipynb)

**Multi-Agent System** — Several AI *agents*, often with different roles (researcher, writer, reviewer), working together on a task by passing messages or results between them. See: [10_Agents/04_multi_agent_frameworks.ipynb](10_Agents/04_multi_agent_frameworks.ipynb)

**Multimodal AI** — AI that works with more than one kind of data, such as text plus images, audio or video, for example describing a photo or answering questions about a chart. See: [08_LLM/11_multimodal/01_multimodal_ai.ipynb](08_LLM/11_multimodal/01_multimodal_ai.ipynb)

## N

**Naive Bayes** — A fast classifier based on *Bayes' theorem* that "naively" assumes every feature is independent of the others given the class. Despite that simplification it works well for text, such as spam filtering. See: [03_Machine_Learning/01_supervised/06_naive_bayes.ipynb](03_Machine_Learning/01_supervised/06_naive_bayes.ipynb)

**Named Entity Recognition (NER)** — Finding and labeling names of things in text, such as people, organizations, places and dates. *Example:* in "Tim Cook visited Paris in May", tag Tim Cook = PERSON, Paris = PLACE, May = DATE. See: [07_NLP/04_named_entity_recognition.ipynb](07_NLP/04_named_entity_recognition.ipynb)

**Neural Network** — A model made of layers of simple units (*neurons*). Each neuron computes a weighted sum of its inputs and applies an *activation function*. By adjusting the weights, the network learns complex patterns. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Neuron** — The basic unit of a neural network: it multiplies each input by a weight, adds them up with a bias, and passes the result through an *activation function*. See: [05_Deep_Learning/notes/05_Deep_Learning.md](05_Deep_Learning/notes/05_Deep_Learning.md)

**NLP (Natural Language Processing)** — The part of AI that deals with human language: reading, understanding, classifying, translating and generating text. See: [07_NLP/notes/07_NLP.md](07_NLP/notes/07_NLP.md)

**Normal (Gaussian) Distribution** — The classic bell-shaped curve, where most values sit near the average and extreme values are rare. Heights and measurement errors are roughly normal. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**NoSQL Database** — A database that doesn't use fixed relational tables, storing data as documents (JSON-like), key-value pairs, wide columns or graphs instead. It is often chosen for flexible or very large-scale data. See: [13_Databases/02_nosql/01_nosql_databases.ipynb](13_Databases/02_nosql/01_nosql_databases.ipynb)

**NumPy** — The core Python library for fast math on arrays (lists of numbers in one or more dimensions). Almost every data and ML library is built on top of it. See: [02_Data_Analysis/02_numpy.ipynb](02_Data_Analysis/02_numpy.ipynb)

## O

**Object Detection** — Finding *where* objects are in an image (drawing boxes around them) and *what* they are. *Example:* boxes labeled "car", "person" and "bicycle" in a street photo. See: [06_Computer_Vision/03_object_detection.ipynb](06_Computer_Vision/03_object_detection.ipynb)

**Observability (Tracing)** — Being able to see what a system did and why, through logs, metrics and traces. For LLM *agents*, a trace records every prompt, tool call, result, token count and timing, so you can debug and measure them. See: [10_Agents/06_agent_observability.ipynb](10_Agents/06_agent_observability.ipynb)

**One-Hot Encoding** — Turning a category column into several 0/1 columns, one per category. *Example:* color = red/green/blue becomes is_red, is_green, is_blue, with exactly one 1 per row. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**ONNX** — An open file format for trained models, so a model built in one framework (such as PyTorch) can run in another runtime (such as ONNX Runtime), often faster and on more kinds of devices. See: [05_Deep_Learning/17_industry_model_export_and_inference.ipynb](05_Deep_Learning/17_industry_model_export_and_inference.ipynb)

**Optimizer** — The algorithm that updates a model's weights using the *gradients* to reduce the *loss*. Examples are SGD, SGD with momentum, and *Adam*. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Outlier** — A data point far away from the rest, caused either by an error (a typo like age = 999) or by something genuinely rare. Outliers can distort averages and some models. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Overfitting** — When a model memorizes the training data, including its noise, so it scores very well on training data but poorly on new data. *Analogy:* a student who memorizes past exam answers but can't solve new questions. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

## P

**p-value** — Assuming there is really no effect, the probability of seeing a result at least as extreme as the one you got. A small p-value (often below 0.05) suggests the effect is unlikely to be pure chance. It is *not* the probability that the effect is real. See: [02_Data_Analysis/08_statistics.ipynb](02_Data_Analysis/08_statistics.ipynb)

**pandas** — The main Python library for working with tables of data (*DataFrames*): loading, cleaning, filtering, grouping and summarizing. See: [02_Data_Analysis/03_pandas.ipynb](02_Data_Analysis/03_pandas.ipynb)

**Parameters (Weights and Biases)** — The numbers inside a model that are learned during training. When people say an LLM has "7 billion parameters", these are the numbers they mean. Compare *hyperparameter*. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**PCA (Principal Component Analysis)** — A *dimensionality reduction* method that finds the few directions along which the data varies most and re-describes the data using just those directions. See: [03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb](03_Machine_Learning/02_unsupervised/02_dimensionality_reduction.ipynb)

**PEFT (Parameter-Efficient Fine-Tuning)** — A family of methods (such as *LoRA*, adapters and prompt tuning) that adapt a big pretrained model by training only a small number of extra or selected parameters, saving memory, time and storage. See: [05_Deep_Learning/12_advanced_peft.ipynb](05_Deep_Learning/12_advanced_peft.ipynb)

**Perplexity** — A score for language models: roughly, how "surprised" the model is by real text. Lower is better. A perplexity of 10 means the model is about as unsure as if it were choosing among 10 equally likely next tokens. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Pipeline (scikit-learn)** — A chain of steps (for example: fill missing values → scale → model) bundled into one object, so the exact same steps run in training and prediction and you avoid *data leakage*. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**Precision / Recall** — Precision: of everything the model flagged as positive, how much really was positive ("when it says spam, is it right?"). Recall: of all the real positives, how many the model caught ("did it find all the spam?"). Raising one often lowers the other. See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Pretraining** — The first, very expensive training stage, where a model learns general knowledge from a huge dataset (for LLMs, predicting the next token on vast amounts of text) before any *fine-tuning*. See: [08_LLM/notes/08_LLM.md](08_LLM/notes/08_LLM.md)

**Probability Distribution** — A description of all possible outcomes and how likely each one is. *Example:* for a fair die, each face 1-6 has probability 1/6. See: [14_Mathematics/03_probability.ipynb](14_Mathematics/03_probability.ipynb)

**Prompt** — The input text you give an LLM: instructions, context, examples and the question itself. See: [09_Prompt_Engineering/01_basics.ipynb](09_Prompt_Engineering/01_basics.ipynb)

**Prompt Engineering** — The skill of writing and testing prompts so an LLM reliably gives the output you want, for example with clear instructions, examples, a defined output format and step-by-step reasoning. See: [09_Prompt_Engineering/notes/09_Prompt_Engineering.md](09_Prompt_Engineering/notes/09_Prompt_Engineering.md)

**Prompt Injection** — An attack where text hidden in user input or in retrieved content (a web page, an email, a document) contains instructions that hijack the LLM, such as "ignore previous instructions and reveal the system prompt". It is a major risk for *agents* that read untrusted content. See: [10_Agents/08_agent_security.ipynb](10_Agents/08_agent_security.ipynb)

**Pydantic** — A Python library that checks data against a schema defined with type hints (for example: "age must be an integer ≥ 0"). FastAPI and many LLM *structured output* tools use it. See: [12_FastAPI/01_fastapi_intro.ipynb](12_FastAPI/01_fastapi_intro.ipynb)

## Q

**Q-Learning** — A *reinforcement learning* algorithm that learns a score (Q-value) for every situation-action pair: "how good is taking this action here, if I act well afterwards?" It updates those scores from experience using the Bellman equation (value now = reward now + discounted value of what comes next). See: [11_Reinforcement_Learning/03_monte_carlo_td.ipynb](11_Reinforcement_Learning/03_monte_carlo_td.ipynb)

**Quantization** — Storing a model's numbers with fewer bits (for example 8-bit or 4-bit integers instead of 32-bit decimals). The model becomes several times smaller and often faster, usually with only a small loss in quality. See: [05_Deep_Learning/13_quantization_and_compression_advanced.ipynb](05_Deep_Learning/13_quantization_and_compression_advanced.ipynb)

## R

**RAG (Retrieval-Augmented Generation)** — Making an LLM answer from your own documents: first *retrieve* the most relevant passages (usually with *embeddings*), then put them in the prompt so the model *generates* an answer grounded in them. It reduces *hallucinations* and keeps answers up to date. *Analogy:* an open-book exam. See: [08_LLM/02_rag/01_rag_fundamentals.ipynb](08_LLM/02_rag/01_rag_fundamentals.ipynb)

**Random Forest** — An *ensemble* of many *decision trees*, each trained on a random sample of rows and features, that vote on the answer. It is accurate, robust and a strong default for tabular data. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

**ReAct (Reason + Act)** — A common *agent* pattern where the model alternates between thinking ("I need the population of France"), acting (calling a search tool) and observing the result, until it can answer. See: [10_Agents/01_agent_fundamentals.ipynb](10_Agents/01_agent_fundamentals.ipynb)

**Reasoning Model** — An LLM trained to produce a long internal chain of reasoning before answering, which tends to help on math, coding and multi-step problems at the cost of more tokens and time. Spending more compute while answering is called "test-time compute". See: [08_LLM/18_reasoning_models.ipynb](08_LLM/18_reasoning_models.ipynb)

**Recommendation System** — A system that suggests items a user is likely to want (products, movies, songs) based on their past behavior, similar users, item content, or a mix. See: [03_Machine_Learning/09_recommendation_systems/01_recommendation_systems.ipynb](03_Machine_Learning/09_recommendation_systems/01_recommendation_systems.ipynb)

**Red Teaming** — Deliberately attacking your own AI system (with *jailbreaks*, *prompt injection*, tricky edge cases) to find failures before real attackers or users do. See: [19_AI_Ethics_and_Safety/09_industry_ai_incident_response_and_red_teaming.ipynb](19_AI_Ethics_and_Safety/09_industry_ai_incident_response_and_red_teaming.ipynb)

**Regression** — A *supervised learning* task where the answer is a number. *Examples:* predicting a house price, a temperature, or delivery time. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**Regularization (L1 / L2, Lasso / Ridge)** — Adding a penalty for large weights during training to keep a model simpler and reduce *overfitting*. L2 (Ridge) shrinks all weights a little; L1 (Lasso) can push some weights to exactly zero, which also selects features. See: [03_Machine_Learning/01_supervised/01_linear_regression.ipynb](03_Machine_Learning/01_supervised/01_linear_regression.ipynb)

**Reinforcement Learning (RL)** — Learning by trial and error: an *agent* takes actions in an environment, receives rewards or penalties, and learns a strategy (called a policy) that maximizes total reward over time. *Analogy:* training a dog with treats. See: [11_Reinforcement_Learning/notes/11_Reinforcement_Learning.md](11_Reinforcement_Learning/notes/11_Reinforcement_Learning.md)

**ReLU (Rectified Linear Unit)** — The most common *activation function*: output the input if it is positive, otherwise output 0. It is simple, fast and works well in deep networks. See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**REST API** — A common style of web API where you use standard HTTP methods on URLs: `GET /items/5` reads an item, `POST /items` creates one, `DELETE /items/5` removes it. See: [12_FastAPI/notes/12_FastAPI.md](12_FastAPI/notes/12_FastAPI.md)

**Reward** — The number an RL environment gives the agent after each action to signal how good it was, for example +1 for winning a game or -1 for crashing. See: [11_Reinforcement_Learning/01_rl_fundamentals.ipynb](11_Reinforcement_Learning/01_rl_fundamentals.ipynb)

**RLHF (Reinforcement Learning from Human Feedback)** — An *alignment* method: people compare pairs of model answers, a "reward model" learns to predict which answers people prefer, and the LLM is then trained with reinforcement learning (often PPO) to produce answers the reward model scores highly. See: [08_LLM/12_alignment_techniques.ipynb](08_LLM/12_alignment_techniques.ipynb)

**RNN (Recurrent Neural Network)** — A neural network for sequences (text, time series) that reads one step at a time while carrying a "memory" (hidden state) forward. Plain RNNs forget long-range information, which led to *LSTMs* and the similar, simpler GRUs. See: [05_Deep_Learning/04_rnn_lstm_gru.ipynb](05_Deep_Learning/04_rnn_lstm_gru.ipynb)

## S

**scikit-learn (sklearn)** — The standard Python library for classic machine learning. It offers models, preprocessing, *pipelines* and evaluation tools, all with the same `fit` / `predict` interface. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**Seasonality / Trend** — Two parts of a time series. Trend is the long-term direction (sales slowly growing). Seasonality is a pattern that repeats on a fixed calendar cycle (more ice cream in summer, more traffic on Mondays). See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Self-Supervised Learning** — Learning from unlabeled data by creating the labels from the data itself, such as hiding a word and predicting it, or predicting the next token. This is how LLMs and many vision models are pretrained. See: [05_Deep_Learning/09_self_supervised_learning.ipynb](05_Deep_Learning/09_self_supervised_learning.ipynb)

**Semantic Search** — Searching by meaning instead of exact words, by comparing *embeddings*. A query for "cheap flights" can find a page that says "low-cost airfare". See: [07_NLP/13_industry_semantic_search_engine.ipynb](07_NLP/13_industry_semantic_search_engine.ipynb)

**Semantic Versioning (SemVer)** — A version-numbering rule, MAJOR.MINOR.PATCH (for example 2.4.1). Bump MAJOR for breaking changes, MINOR for new backward-compatible features, PATCH for bug fixes. See: [20_Git_and_DevOps/04_semantic_versioning.ipynb](20_Git_and_DevOps/04_semantic_versioning.ipynb)

**Semi-Supervised Learning** — Training with a small amount of labeled data plus a large amount of unlabeled data, which is useful when labels are expensive. See: [03_Machine_Learning/03_semi_supervised/01_semi_supervised_learning.ipynb](03_Machine_Learning/03_semi_supervised/01_semi_supervised_learning.ipynb)

**SHAP** — An *explainability* method based on Shapley values from game theory. It splits a prediction into fair contributions from each feature, such as "income added +0.20 to the approval score and debt subtracted -0.15". See: [03_Machine_Learning/07_explainability/01_explainability.ipynb](03_Machine_Learning/07_explainability/01_explainability.ipynb)

**Sigmoid** — An S-shaped function that squashes any number into the range 0 to 1, which makes it handy for turning a score into a probability (as in *logistic regression*). See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**Small Language Model (SLM)** — A language model small enough (roughly hundreds of millions to a few billion parameters) to run cheaply on a laptop, phone or single GPU. It is less capable than the largest models, but fast, private and often good enough for focused tasks. See: [08_LLM/05_slms/01_small_language_models.ipynb](08_LLM/05_slms/01_small_language_models.ipynb)

**Softmax** — A function that turns a list of scores (*logits*) into probabilities that are all positive and add up to 1. *Example:* scores [2, 1, 0] become about [0.67, 0.24, 0.09]. See: [03_Machine_Learning/01_supervised/02_logistic_regression.ipynb](03_Machine_Learning/01_supervised/02_logistic_regression.ipynb)

**SQL (Structured Query Language)** — The standard language for asking questions of relational databases. *Example:* `SELECT name FROM customers WHERE country = 'UK'`. See: [13_Databases/01_sql/01_sql_fundamentals.ipynb](13_Databases/01_sql/01_sql_fundamentals.ipynb)

**Standardization / Normalization (Feature Scaling)** — Putting features on similar scales so none dominates just because of its units. Standardization makes a column have mean 0 and standard deviation 1; min-max normalization squeezes it into 0-1. See: [03_Machine_Learning/01_supervised/00_preprocessing.ipynb](03_Machine_Learning/01_supervised/00_preprocessing.ipynb)

**Stationarity** — A time series is stationary when its basic behavior (average, spread, how it relates to its own past) doesn't change over time. Many classical models like *ARIMA* assume it, so trends are often removed first. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Stochastic Gradient Descent (SGD)** — *Gradient descent* that updates the weights using a small random *mini-batch* instead of the whole dataset each step. It is noisier, but much faster and the basis of all neural-network training. See: [05_Deep_Learning/02_optimizers.ipynb](05_Deep_Learning/02_optimizers.ipynb)

**Structured Output** — Making an LLM reply in an exact machine-readable format, usually *JSON* that matches a schema, so your code can use the answer reliably. See: [08_LLM/17_structured_outputs.ipynb](08_LLM/17_structured_outputs.ipynb)

**Supervised Learning** — Learning from examples that come with the correct answers (*labels*). The two main types are *classification* and *regression*. See: [03_Machine_Learning/01_supervised/notes/01_supervised.md](03_Machine_Learning/01_supervised/notes/01_supervised.md)

**SVM (Support Vector Machine)** — A classifier that finds the boundary separating the classes with the widest possible gap (margin). With the "kernel trick" (measuring similarity as if the data had extra dimensions) it can draw curved boundaries. See: [03_Machine_Learning/01_supervised/05_svm.ipynb](03_Machine_Learning/01_supervised/05_svm.ipynb)

**System Prompt** — Hidden instructions given to a chat LLM before the user's messages to set its role, rules and style (for example "You are a polite support assistant for a bank; never give investment advice"). See: [08_LLM/07_prompt_engineering/notes/07_prompt_engineering.md](08_LLM/07_prompt_engineering/notes/07_prompt_engineering.md)

## T

**Temperature** — A generation setting that controls randomness. Low temperature (near 0) makes the model pick the most likely tokens, giving focused and repeatable answers; higher temperature spreads the probability out, giving more varied and creative output. Technically, the *logits* are divided by the temperature before the *softmax*. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Tensor** — A multi-dimensional array of numbers, the basic data type in PyTorch: a single number, a vector, a matrix, or higher (a color image is height × width × 3). See: [05_Deep_Learning/01_neural_network_fundamentals.ipynb](05_Deep_Learning/01_neural_network_fundamentals.ipynb)

**TF-IDF** — A way to turn text into numbers: a word gets a high score in a document if it appears often there (term frequency) but rarely across all documents (inverse document frequency). Common words like "the" score low. See: [07_NLP/01_text_preprocessing.ipynb](07_NLP/01_text_preprocessing.ipynb)

**Time Series** — Data recorded in time order, such as daily sales, hourly temperature or stock prices, where the order matters. See: [04_Forecasting/01_time_series_basics.ipynb](04_Forecasting/01_time_series_basics.ipynb)

**Token / Tokenization** — LLMs don't read letters or whole words; they read *tokens*, which are chunks of text (often a word or part of a word). Tokenization is the step that splits text into tokens and maps each to a number. Prices and *context windows* are measured in tokens. See: [07_NLP/01_text_preprocessing.ipynb](07_NLP/01_text_preprocessing.ipynb)

**Tool (Agent Tool)** — A function an *agent* can call, such as web search, a calculator, a database query or sending an email. It is described to the LLM with a name, a purpose and input parameters. See: [10_Agents/05_mcp_and_tools.ipynb](10_Agents/05_mcp_and_tools.ipynb)

**Top-k / Top-p (Nucleus) Sampling** — Ways to pick the next token when generating text. Top-k samples only from the k most likely tokens; top-p samples from the smallest set of tokens whose combined probability reaches p (for example 0.9). Both cut off unlikely nonsense. See: [07_NLP/05_language_models_and_generation.ipynb](07_NLP/05_language_models_and_generation.ipynb)

**Train / Validation / Test Split** — Dividing data into three parts: *train* to learn from, *validation* to tune settings and choose models, and *test*, used once at the end for an honest final score. *Analogy:* homework, practice exams and the real exam. See: [03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb](03_Machine_Learning/01_supervised/09_pipeline_and_leakage.ipynb)

**Transfer Learning** — Reusing a model trained on one big task as the starting point for a related task, so you need far less data and time. *Example:* start from a network trained on millions of photos and fine-tune it to spot defects in your factory's products. See: [06_Computer_Vision/02_image_classification.ipynb](06_Computer_Vision/02_image_classification.ipynb)

**Transformer** — The neural-network architecture (introduced in 2017) behind modern LLMs and many vision models. It is built from self-attention (see *Attention*) and simple feed-forward layers, and it processes all tokens in parallel rather than one by one like an *RNN*. See: [05_Deep_Learning/05_transformers_architecture.ipynb](05_Deep_Learning/05_transformers_architecture.ipynb)

## U

**Underfitting** — When a model is too simple to capture the real pattern, so it does badly on both training and new data. *Example:* fitting a straight line to data that clearly curves. See: [03_Machine_Learning/notes/03_Machine_Learning.md](03_Machine_Learning/notes/03_Machine_Learning.md)

**Unsupervised Learning** — Finding structure in data without any labels, for example *clustering* similar customers or *dimensionality reduction*. See: [03_Machine_Learning/02_unsupervised/notes/02_unsupervised.md](03_Machine_Learning/02_unsupervised/notes/02_unsupervised.md)

## V

**Validation Set** — Data held back from training and used to compare models and tune *hyperparameters*. It is separate from the final test set (see *Train / Validation / Test Split*). See: [03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb](03_Machine_Learning/06_model_evaluation/01_model_evaluation.ipynb)

**Vector** — An ordered list of numbers, such as [0.2, -1.3, 4.0]. In ML, almost everything (a data row, an *embedding*, a set of weights) is represented as a vector. See: [14_Mathematics/01_linear_algebra.ipynb](14_Mathematics/01_linear_algebra.ipynb)

**Vector Database** — A database built to store *embeddings* and quickly find the ones most similar to a query embedding. It is the usual "memory" behind *RAG* and *semantic search*. See: [13_Databases/03_vector_db/01_vector_databases.ipynb](13_Databases/03_vector_db/01_vector_databases.ipynb)

**Virtual Environment (venv)** — A private, per-project folder of Python packages, so different projects can use different library versions without clashing. Create one with `python -m venv .venv`. See: [01_Python/notes/01_Python.md](01_Python/notes/01_Python.md)

**Vision Language Model (VLM)** — A model that takes images (and text) as input and answers in text, for example describing a photo, reading a chart or answering questions about a screenshot. See: [08_LLM/06_vision_llm/01_vision_language_models.ipynb](08_LLM/06_vision_llm/01_vision_language_models.ipynb)

**Vision Transformer (ViT)** — A *transformer* applied to images: the image is cut into small square patches, each patch is treated like a token, and self-attention relates the patches to each other. See: [06_Computer_Vision/05_vision_transformers.ipynb](06_Computer_Vision/05_vision_transformers.ipynb)

## W

**Word Embedding (Word2Vec)** — An *embedding* for a single word, learned from which words appear near each other in lots of text. Word2Vec is a classic method. A famous illustration is that king - man + woman lands close to queen. See: [07_NLP/02_word_embeddings.ipynb](07_NLP/02_word_embeddings.ipynb)

## X

**XAI (Explainable AI)** — Another name for *explainability*: methods and practices that make AI decisions understandable to people. See: [00_AI_Fundamentals/02_transparency_and_explainability.ipynb](00_AI_Fundamentals/02_transparency_and_explainability.ipynb)

**XGBoost** — A fast, widely used *gradient boosting* library for tabular data. It often wins on spreadsheet-style problems. LightGBM and CatBoost are close relatives. See: [03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb](03_Machine_Learning/01_supervised/04_ensemble_methods.ipynb)

## Y

**YOLO (You Only Look Once)** — A family of fast *object detection* models that find all objects in an image in a single pass through the network, fast enough for real-time video. See: [06_Computer_Vision/03_object_detection.ipynb](06_Computer_Vision/03_object_detection.ipynb)

## Z

**Z-Score** — How many standard deviations a value is from the average: z = (value - mean) / standard deviation. A z-score above about 3 (or below -3) is often treated as an outlier. See: [02_Data_Analysis/01_data_preprocessing.ipynb](02_Data_Analysis/01_data_preprocessing.ipynb)

**Zero-Shot** — Asking a model to do a task with no examples, just an instruction ("Classify this review as positive or negative"). Compare *few-shot*. Zero-shot classification also means labeling data with categories the model was never explicitly trained on. See: [09_Prompt_Engineering/02_techniques.ipynb](09_Prompt_Engineering/02_techniques.ipynb)

---

*Can't find a word?* Search the module notes (each module has a `notes/` folder) or the main [README.md](README.md). Terms are explained in more depth, with runnable code, in the linked notebooks.
