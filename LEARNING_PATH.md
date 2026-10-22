# 🧭 Learning Path: What to Study, in What Order

> **Who is this for?** Anyone who opens this repo and asks: *"There are 260 notebooks. Where do I start, and what can I skip?"*
>
> **Not set up yet?** Do [`START_HERE.md`](START_HERE.md) first. Unknown word? Check [`GLOSSARY.md`](GLOSSARY.md). Something not working? See the troubleshooting table in [`START_HERE.md`](START_HERE.md#6-troubleshooting).

---

## How to read this page

The folders are numbered `00` to `22`, but **the numbers are not the study order**. For example, you need Git (`20`) and some maths (`14`) long before you need deployment (`16`). This page gives you the order.

Each stage lists what to do, marked like this:

| Mark | Meaning |
|---|---|
| ⭐ **Core** | Do it. Everything later builds on it. |
| ✅ **Recommended** | Do it if you can; it makes you noticeably stronger. |
| 🔹 **Optional** | Advanced or specialised. Skip on your first pass and come back when you need it. |
| 🌱 | A **Start Here** notebook: a gentle, fully runnable introduction written for complete beginners. |
| 🏭 | An **industry** notebook: the same topic done the way a company would do it. |
| 🔑 | Needs a paid API key to run fully (you can still read it; free alternatives are listed). |

**Every folder also has a `notes/` file** (for example `03_Machine_Learning/notes/03_Machine_Learning.md`). It explains the ideas in plain English with diagrams. A good routine for every topic:

1. Read the notes file for the topic.
2. Run the 🌱 Start Here notebook, if there is one.
3. Run the core notebooks **cell by cell**. Change numbers, break things, and see what happens.
4. Do the 🏭 industry notebook.
5. Write 3–5 sentences explaining what you learned, in your own words.

**Time estimates** assume about **10–15 hours per week**. Going slower is completely fine.

---

## The big picture

```
 Stage 0  Setup ─► Stage 1  Big picture & ethics ─► Stage 2  Python & tools
                                                          │
 Stage 5  Machine learning ◄─ Stage 4  Maths bridge ◄─ Stage 3  Data analysis
     │
     ├─► Stage 6  Forecasting (optional track)
     ▼
 Stage 7  Deep learning ─► Stage 8  Vision & language ─► Stage 9  LLMs & prompting
                                                               │
 Stage 12 Capstone projects ◄─ Stage 11 Shipping & MLOps ◄─ Stage 10  Agents
     │
     ▼
 Stage 13 System design & career     (+ optional tracks: RL, advanced safety, advanced MLOps)
```

The core path (⭐ only) takes roughly **6–9 months** at 10–15 h/week.

---

## Stage 0: Setup (1–2 days)

| | What | Why |
|---|---|---|
| ⭐ | [`START_HERE.md`](START_HERE.md) | Install Python and the packages, open Jupyter (or use Google Colab) |
| ⭐🌱 | `01_Python/00_start_here_jupyter_terminal_and_debugging.ipynb` | How notebooks, the terminal, `pip`, error messages and Git work |

## Stage 1: The big picture & responsible AI (3–5 days)

| | What | Why |
|---|---|---|
| ⭐🌱 | `00_AI_Fundamentals/00_start_here_what_is_ai.ipynb` | What AI / ML / deep learning / LLMs are, the key vocabulary, and a map of this repo |
| ⭐ | `00_AI_Fundamentals/notes/00_AI_Fundamentals.md` | Why fairness, transparency and safety matter |
| ✅ | `00_AI_Fundamentals/01_bias_and_fairness.ipynb`, `06_responsible_ai_and_ethics.ipynb` | The two most important ethics topics, hands-on |
| 🔹 | `00_AI_Fundamentals/02`–`05`, 🏭 `07_industry_responsible_ai_product_review.ipynb` | These use ML terms you will learn in Stage 5. Coming back to them after Stage 5 is perfectly fine. |

## Stage 2: Python & everyday tools (2–3 weeks)

| | What | Why |
|---|---|---|
| ⭐ | `01_Python/01_basic.ipynb` → `02_industrial.ipynb` | The Python you will use everywhere |
| ✅ | `01_Python/03_advanced.ipynb` | Decorators, generators, typing: useful, but not needed yet |
| ⭐🏭 | `01_Python/04_industry_from_notebook_to_production_code.ipynb` | Writing code other people can use |
| ⭐ | `20_Git_and_DevOps/01_git_basics.ipynb` | **Learn Git now**, not at the end. Save every exercise in a Git repo. |
| ✅🏭 | `20_Git_and_DevOps/05_industry_team_git_workflow_for_ml.ipynb` | Branches and pull requests, as teams use them |

## Stage 3: Data analysis (3–4 weeks)

Do `02_Data_Analysis` in **this** order. `01_data_preprocessing` uses tools taught in the later notebooks, so it comes last here.

| | What | Why |
|---|---|---|
| ⭐ | `02_Data_Analysis/02_numpy.ipynb` → `03_pandas.ipynb` | Arrays and tables: the foundation of all data work |
| ⭐ | `04_matplotlib.ipynb` → `05_seaborn.ipynb` | Plotting |
| ⭐ | `07_eda.ipynb` → `08_statistics.ipynb` | Exploring data and basic statistics |
| ⭐ | `01_data_preprocessing.ipynb` | Cleaning data. It mentions SMOTE and pipelines; those are explained fully in Stage 5. |
| ⭐🏭 | `11_industry_eda_report_for_stakeholders.ipynb` | Turning analysis into a report people act on |
| ✅ | `13_Databases/01_sql/01_sql_fundamentals.ipynb`, 🏭 `02_industry_sql_for_ml_feature_extraction.ipynb` | SQL is asked for in almost every data or AI job |
| 🔹 | `06_plotly.ipynb`, `09_polars.ipynb`, `10_duckdb.ipynb` | Faster or interactive alternatives |

## Stage 4: Maths bridge (2–3 weeks, can run in parallel with Stage 5)

| | What | Why |
|---|---|---|
| ⭐🌱 | `14_Mathematics/00_start_here_math_notation_bridge.ipynb` | From high-school maths to ML notation: Σ, vectors, derivatives, probability, formula → code |
| ⭐ | `14_Mathematics/01_linear_algebra.ipynb`, `02_calculus.ipynb`, `03_probability.ipynb`, `04_statistics.ipynb` | The four pillars. Aim for intuition; you don't need to master proofs. |
| ✅🏭 | `14_Mathematics/08_industry_math_in_practice.ipynb` | Where the maths shows up in real work |
| 🔹 | `05_information_theory.ipynb`, `06_optimization.ipynb`, `07_bayesian_ml.ipynb` | Read when a later notebook needs them (e.g. cross-entropy for deep learning, Bayesian methods for A/B testing) |

## Stage 5: Classical machine learning (6–8 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `03_Machine_Learning/00_start_here_your_first_ml_model.ipynb` | A complete first project: split, baseline, train, evaluate, overfitting, leakage, saving |
| ⭐ | `03_Machine_Learning/01_supervised/`: `00_preprocessing`, `01_linear_regression`, `02_logistic_regression`, `03_decision_trees`, `04_ensemble_methods`, `09_pipeline_and_leakage`, `10_end_to_end_project` | The core supervised algorithms and the habits that keep you honest |
| ⭐🏭 | `01_supervised/14_industry_churn_prediction.ipynb`, `15_industry_house_price_regression.ipynb` | Classification and regression done professionally |
| ✅ | `01_supervised/05_svm`, `06_naive_bayes`, `07_knn`, `13_model_calibration` | More algorithms worth knowing |
| ⭐ | `02_unsupervised/01_clustering`, `02_dimensionality_reduction`, 🏭 `04_industry_customer_segmentation` | Finding structure without labels |
| ⭐ | `05_feature_engineering/` (all three) | Usually the biggest lever on model quality |
| ⭐ | `06_model_evaluation/` (all three) | Choosing metrics, tuning, comparing models fairly |
| ✅ | `07_explainability/` (all three), `10_evaluation_metrics_comprehensive.ipynb` | Explaining predictions; the full metrics reference |
| ✅ | `11_ab_testing/` | How companies decide whether a model actually helps |
| 🔹 | `01_supervised/08`, `11`, `12`; `02_unsupervised/03`; `03_semi_supervised/`, `04_uncommon_models/`, `08_anomaly_detection/`, `09_recommendation_systems/`, `10_causal_inference/`, `12_online_learning/`, `13_active_learning/`, `14_conformal_prediction/`, `15_synthetic_tabular_data/` | Specialisations: pick the ones that match your interests or job. Each has a 🏭 notebook. |

## Stage 6 (optional track): Forecasting (3–4 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `04_Forecasting/00_start_here_forecasting_done_right.ipynb` | Baselines, time-based splits, honest backtesting, and the leakage traps |
| ⭐ | `01_time_series_basics.ipynb` → `02_classical_methods.ipynb` | Trend, seasonality, ARIMA, exponential smoothing |
| ⭐🏭 | `11_industry_retail_demand_forecasting.ipynb`, `12_industry_call_center_staffing_forecast.ipynb` | Real forecasting work |
| 🔹 | `03`–`10` | ML and deep-learning forecasting, Prophet, multivariate models, GARCH, probabilistic forecasts, anomaly detection |

## Stage 7: Deep learning (5–6 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `05_Deep_Learning/00_start_here_pytorch_from_zero.ipynb` | Tensors, autograd and the training loop, all actually trained on CPU |
| ⭐ | `01_neural_network_fundamentals.ipynb` → `02_optimizers.ipynb` | What happens inside a network, and how it learns |
| ⭐🏭 | `16_industry_pytorch_training_pipeline.ipynb` | **Do this right after 01–02.** It is the most practical PyTorch notebook in the repo. |
| ⭐ | `03_cnn.ipynb`, `04_rnn_lstm_gru.ipynb`, `05_transformers_architecture.ipynb` | The three architecture families. `05` is essential for LLMs. |
| ✅🏭 | `17_industry_model_export_and_inference.ipynb` | Getting a trained model out of the notebook |
| 🔹 | `06`–`15` | Generative models, GNNs, compression, self-supervised learning, PEFT, distributed training… (some need a GPU) |

## Stage 8: Computer vision & NLP (4–6 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `06_Computer_Vision/00_start_here_images_and_your_first_cnn.ipynb` | Pixels, convolutions, and a CNN trained on CPU |
| ⭐ | `06_Computer_Vision/01_image_basics_opencv.ipynb`, `02_image_classification.ipynb`, 🏭 `11_industry_visual_defect_inspection.ipynb` | Core vision skills |
| ✅ | `03_object_detection`, `05_vision_transformers`, 🏭 `12_industry_visual_product_search` | |
| 🔹 | `04`, `06`–`10` | Segmentation, generation, OCR, video, 3-D, medical imaging |
| ⭐🌱 | `07_NLP/00_start_here_text_to_numbers.ipynb` | Tokens, TF-IDF, embeddings, semantic search |
| ⭐ | `07_NLP/01_text_preprocessing`, `02_word_embeddings`, `03_text_classification`, 🏭 `12_industry_support_ticket_routing`, 🏭 `13_industry_semantic_search_engine` | Core NLP |
| 🔹 | `07_NLP/04`–`11` | NER, generation, QA, topic models, speech, multilingual |

## Stage 9: LLMs & prompt engineering (5–6 weeks)

| | What | Why |
|---|---|---|
| ⭐🌱 | `08_LLM/00_start_here_how_llms_work.ipynb` | Next-token prediction, sampling, chat templates, and a tiny GPT trained from scratch |
| ⭐🌱 | `09_Prompt_Engineering/00_start_here_prompting_with_a_free_local_model.ipynb` | Every basic prompting technique, actually running, with no key |
| ⭐🔑 | `09_Prompt_Engineering/01_basics.ipynb` → `02_techniques.ipynb` → `03_advanced.ipynb` | The full prompting toolkit |
| ⭐ | `09_Prompt_Engineering/04_adversarial.ipynb` | Prompt injection: attacks, defences, and how to test a filter with known attacks |
| ⭐🏭 | `09_Prompt_Engineering/05_industry_prompt_development_workflow.ipynb` | Prompts treated as tested, versioned code |
| ⭐🔑 | `08_LLM/01_chatbots/`, `08_LLM/02_rag/01_rag_fundamentals.ipynb`, `02_advanced_rag.ipynb` | Chatbots and Retrieval-Augmented Generation |
| ⭐🏭 | `08_LLM/19_industry_rag_pipeline.ipynb`, `20_industry_llm_application_patterns.ipynb` | RAG and reliable LLM calls, running locally |
| ✅ | `08_LLM/08_evaluation/`, `16_llm_security.ipynb`, `17_structured_outputs.ipynb`, `04_different_llms/`, `05_slms/` | Evaluation, security, structured output, choosing a model |
| 🔹 | `08_LLM/02_rag/03`–`04`, `03_fine_tuning/`, `06_vision_llm/`, `07_prompt_engineering/`, `09_knowledge_graphs/`, `10_synthetic_data/`, `11_multimodal/`, `12`–`15`, `18`; `09_Prompt_Engineering/ai_tools/` | Advanced topics (fine-tuning needs a GPU) |

## Stage 10: Agents (3–4 weeks)

| | What | Why |
|---|---|---|
| ⭐🔑 | `10_Agents/01_agent_fundamentals.ipynb` → `02_memory_and_planning.ipynb` | The agent loop: think, act with tools, observe |
| ⭐🏭 | `10_Agents/09_industry_tool_using_agent.ipynb` | **Do this early.** It runs offline and shows a complete, safe agent. |
| ✅🔑 | `03_langgraph.ipynb`, `05_mcp_and_tools.ipynb`, `08_agent_security.ipynb` | Frameworks, tool protocols, security |
| 🔹 | `04_multi_agent_frameworks`, `06_agent_observability`, `07_advanced_agent_frameworks` | |

## Stage 11: Shipping AI: APIs, deployment & MLOps (5–7 weeks)

| | What | Why |
|---|---|---|
| ⭐ | `12_FastAPI/01`–`03`, 🏭 `04_industry_production_ml_api.ipynb` | Serving a model behind an API |
| ⭐ | `17_Docker/01_docker_basics.ipynb`, `02_docker_for_ml.ipynb`, 🏭 `04_industry_containerizing_an_ml_service.ipynb` | Packaging your app so it runs anywhere |
| ⭐ | `16_Deployment/01_deployment_concepts.ipynb`, `02_streamlit_gradio.ipynb`, 🏭 `05_industry_safe_model_rollout_strategies.ipynb` | Demos, deployment options, safe rollouts |
| ⭐ | `15_MLOps/01_experiment_tracking/01_mlflow.ipynb`, `05_model_registry/`, `06_monitoring/`, `07_testing_in_ml/`, 🏭 `15_industry_end_to_end_mlops_pipeline.ipynb` | Tracking, versioning, testing and monitoring models |
| ✅ | `20_Git_and_DevOps/02`–`04`, `13_Databases/03_vector_db/`, `18_Cloud/01_aws_for_ai.ipynb`, 🏭 `18_Cloud/05_industry_cloud_ml_architecture_and_cost_planning.ipynb` | CI/CD, vector databases, cloud basics |
| 🔹 | Rest of `13_Databases`, `15_MLOps`, `16_Deployment`, `17_Docker/03` + `kubernetes/`, `18_Cloud/02`–`04` | Many cells here *show* code for services you would need to install or pay for |

## Stage 12: Capstone projects (4–8 weeks)

Build these in order. Each folder has a `README.md` with tested run steps and its known issues.

| | Project | Uses stages |
|---|---|---|
| ⭐ | `21_Projects/01_ml_pipeline/` | 5, 11 |
| ⭐ | `21_Projects/02_rag_chatbot/` | 9, 11 |
| ✅ | `21_Projects/03_computer_vision_app/` | 8, 11 |
| ✅ | `21_Projects/04_forecasting_dashboard/` | 6, 11 |
| 🔹🔑 | `21_Projects/05_multi_agent_system/` | 10, 11 |
| ⭐ | `21_Projects/06_production_model/` | 11 |

**Then build one project of your own**, on data you care about. That is what employers remember.

## Stage 13: System design & career

| | What | Why |
|---|---|---|
| ✅ | `22_ML_System_Design/01`–`07`, 🏭 `08_industry_system_design_case_study.ipynb` | How to design whole ML systems; asked in most ML engineering interviews |
| ✅ | The [career checklist](#-after-the-path-portfolio--job-checklist) below | |

## Optional tracks (any time after Stage 7)

| Track | Where | Start with |
|---|---|---|
| Reinforcement learning | `11_Reinforcement_Learning/` | `01_rl_fundamentals` → `07_multi_armed_bandits` (simplest) → `02`–`05` → 🏭 `08_industry_inventory_control_with_rl` → `06_advanced_rl` |
| Advanced AI safety & policy | `19_AI_Ethics_and_Safety/` | `01`, `02`, `04`, `05`, then 🏭 `09_industry_ai_incident_response_and_red_teaming` |
| Advanced MLOps | `15_MLOps/02`–`04`, `08`–`14` | `02_data_versioning`, `03_pipeline_orchestration` |

---

## 🧰 Extra installs per module

[`requirements-beginner.txt`](requirements-beginner.txt) covers all 🌱 Start Here notebooks and most core notebooks. Some modules need extra packages. Install them only when you reach that module:

| Module | Install when you reach it | Optional (the notebook still runs without them) |
|---|---|---|
| `00_AI_Fundamentals` | nothing extra | - |
| `01_Python` | nothing extra | - |
| `02_Data_Analysis` | `pip install duckdb polars` | `imbalanced-learn` |
| `03_Machine_Learning` | `pip install ctgan dowhy imbalanced-learn lifelines MAPIE mlxtend optuna river` | `catboost`, `faiss-cpu`, `featuretools`, `interpret`, `lime`, `pyod`, `sacrebleu`, `scikit-surprise` |
| `04_Forecasting` | `pip install neuralforecast stumpy` | `arch`, `chronos-forecasting`, `gpytorch`, `MAPIE`, `neuralprophet`, `ngboost`, `pmdarima`, `prophet`, `pytorch-forecasting`, `timesfm` |
| `05_Deep_Learning` | `pip install evaluate onnx onnxruntime peft` | `torchdiffeq` |
| `06_Computer_Vision` | `pip install faiss-cpu opencv-python-headless scikit-image timm` | `monai`, `pydicom` |
| `07_NLP` | `pip install faiss-cpu gensim keybert nltk rank-bm25 spacy yake` | `bertopic`, `fastcoref`, `langdetect`, `laserembeddings`, `librosa`, `mteb`, `openai`, `rouge-score`, `voyageai` |
| `08_LLM` | `pip install anthropic faiss-cpu google-genai haystack-ai langchain-community langchain-core langchain-openai langchain-text-splitters llama-index nltk ollama openai peft rank-bm25 rouge-score trl` | `cohere`, `FlagEmbedding`, `instructor` |
| `09_Prompt_Engineering` | `pip install anthropic dspy google-genai instructor openai` | - |
| `10_Agents` | `pip install ag2 crewai crewai-tools langchain-core langchain-openai langgraph langsmith nest-asyncio openai pydantic-ai smolagents` | `anthropic`, `faiss-cpu` |
| `11_Reinforcement_Learning` | `pip install gymnasium stable-baselines3` | - |
| `12_FastAPI` | `pip install pyjwt "pwdlib[bcrypt]" pytest` | - |
| `13_Databases` | `pip install duckdb` | - |
| `14_Mathematics` | `pip install arviz pymc` | - |
| `15_MLOps` | `pip install aim arize-phoenix ax-platform bentoml boto3 clearml comet-llm comet-ml dagshub google-genai great-expectations mlflow neptune optuna pandera prefect pytest sacred sagemaker wandb` | `feast`, `langfuse`, `tensorflow` |
| `16_Deployment` | `pip install onnxruntime` | - |
| `17_Docker` | nothing extra | - |
| `18_Cloud` | `pip install boto3 sagemaker` | - |
| `19_AI_Ethics_and_Safety` | nothing extra | - |
| `20_Git_and_DevOps` | nothing extra | - |
| `21_Projects` | Each project has its own `requirements.txt`; follow the `README.md` inside the project folder | - |
| `22_ML_System_Design` | `pip install faiss-cpu` | - |

> 💡 The pip name is sometimes different from the import name: `cv2` → `opencv-python-headless`, `faiss` → `faiss-cpu`, `sklearn` → `scikit-learn`, `imblearn` → `imbalanced-learn`. The complete, pinned list for everything is the root `requirements.txt` (Python 3.12+).

**API keys, GPUs and external services:** 🔑 notebooks use a paid API only if you set its key (e.g. `OPENAI_API_KEY`). Without one they fall back to a free local model or print a clear *"skipped: needs X"* message. No notebook requires a GPU: GPU-heavy parts use small CPU stand-ins or skip with a message. Cells that need a cloud account or a database server (`13_Databases`, `16`–`18`) show the example code and explain what you would need to run it for real; the 🏭 notebooks in those folders run fully offline.

---

## 🎯 After the path: portfolio & job checklist

- [ ] **GitHub profile** with 3–5 pinned projects. Each needs a README with: the problem, the data, the approach, the results (with a baseline), how to run it, and what you would do next.
- [ ] **At least one end-to-end project** you can demo live: data → model → API → simple UI, deployed somewhere free.
- [ ] **One project with an LLM** (RAG or an agent) that includes an evaluation, not just a demo.
- [ ] **Explain every project in 2 minutes**: what, why, how you measured it, and what went wrong.
- [ ] **Interview basics:** Python and SQL exercises; the ML fundamentals from Stage 5 (bias/variance, leakage, metrics, cross-validation); ML system design (Stage 13).
- [ ] **Keep learning:** follow the resources in the main [`README.md`](README.md#-mega-resource-library), read one paper or blog post a week, and write about what you build.
