# AutoML: Automated Machine Learning

Building a good machine learning model involves a long chain of decisions: how to clean and encode the data, which features to engineer, which algorithm to use (random forest? gradient boosting? a neural network?), and for whichever algorithm you pick what values to give its many **hyperparameters** (a hyperparameter is a configuration you set *before* training, like the number of trees or the learning rate, as opposed to the parameters the model *learns*). Done by hand, this is slow, requires expertise, and is easy to do suboptimally because the search space is enormous.

**AutoML (Automated Machine Learning)** is the practice of automating these decisions letting a system search over preprocessing steps, algorithms, and hyperparameters to find a strong pipeline with little manual effort. This guide teaches the concepts and tools in `01_automl.ipynb`, centered on **Optuna** for hyperparameter optimization, with **H2O AutoML**, **TPOT**, and neural architecture search rounding out the landscape.

## What AutoML Automates

A full ML pipeline, and the stages AutoML can take over:

```
Raw Data
  → Data Preprocessing (imputation, encoding, scaling)
  → Feature Engineering (interactions, polynomial features)
  → Algorithm Selection (RF, XGBoost, SVM, neural nets…)
  → Hyperparameter Optimization (HPO)
  → Ensemble Construction (combining several models)
  → Final Model
```

Different tools automate different slices. Some (like Optuna) focus purely on the **hyperparameter optimization (HPO)** stage. Others (like H2O or TPOT) attempt the whole pipeline. The notebook surveys the tool landscape:

| Tool | Approach | Best for |
|------|----------|----------|
| **Optuna** | Bayesian / TPE optimization | Custom, flexible HPO |
| **AutoSklearn** | Bayesian HPO + meta-learning + ensembles | Tabular data |
| **H2O AutoML** | Many algorithms + stacked ensembles | Fast, business-ready results |
| **TPOT** | Genetic programming | Discovering novel pipelines |
| **Ray Tune** | Distributed HPO | Large-scale search |
| **AutoKeras** | Neural architecture search | Deep learning |
| **Ludwig** | Declarative, config-driven ML | No-code modeling |

## The Heart of AutoML: Hyperparameter Optimization

At its core, HPO is a search problem. You have a **search space** (the set of all hyperparameter combinations to consider) and an **objective** (a score, like cross-validated accuracy, to maximize). The challenge is that evaluating one combination means training and validating a whole model slow so you cannot try them all. Different **search strategies** trade off thoroughness against efficiency:

- **Grid search** try every combination on a predefined grid. Exhaustive but explodes combinatorially; ten settings for four hyperparameters is ten thousand models.
- **Random search** sample combinations at random. Surprisingly effective, because it does not waste effort exhaustively varying hyperparameters that do not matter.
- **Bayesian optimization** the smart approach: build a probabilistic model of how hyperparameters relate to the score, and use it to *choose the most promising next combination to try*, learning from every result. This finds good values in far fewer trials than grid or random search.

The HPO search loop, where each trial's result informs the next suggestion until the budget is spent:

```mermaid
flowchart LR
    Suggest[Suggest hyperparameters] --> Train[Train and validate]
    Train --> Score[Score the trial]
    Score --> Update[Update search model]
    Update --> Budget{Budget left?}
    Budget -->|yes| Suggest
    Budget -->|no| Best[Return best trial]
```

## Optuna in Depth

Optuna is a modern, Python-native HPO framework and the notebook's main vehicle. Its design is "define-by-run": you write an **objective function** that takes a `trial` object and, inside it, *asks the trial to suggest* each hyperparameter. A **trial** is one attempt one set of hyperparameters and its resulting score. A **study** is the whole optimization: a collection of trials searching for the best.

The notebook's objective function does something powerful it searches over the **algorithm itself**, not just its hyperparameters. It first calls `trial.suggest_categorical('classifier', ['rf', 'gbm', 'svm'])` to let Optuna pick a model family, then suggests the relevant hyperparameters for whichever family was chosen (`n_estimators` and `max_depth` for random forest, `learning_rate` and `subsample` for gradient boosting, `C` and `kernel` for SVM). Each trial is scored by 5-fold cross-validation. This is *combined algorithm selection and hyperparameter optimization* in a single search the essence of tabular AutoML. Over 30 trials using Optuna's default **TPE (Tree-structured Parzen Estimator)** sampler its Bayesian engine the notebook finds that a linear-kernel SVM with `C≈0.07` scores best (≈0.977 accuracy).

### Note on the suggestion API

The `suggest_*` calls also encode the *type* and *scale* of each hyperparameter: `suggest_int` for integer ranges, `suggest_float(..., log=True)` for values like learning rates that should be explored on a logarithmic scale (because 0.001 vs 0.01 matters as much as 0.1 vs 1.0), and `suggest_categorical` for discrete choices. Choosing the right scale is what makes the search efficient.

### Multi-objective optimization

Real deployments care about more than accuracy a model must also be fast and small. Optuna supports **multi-objective optimization**, where you optimize several goals at once that may conflict. The notebook minimizes both `1 − accuracy` *and* a proxy for inference cost (`n_estimators`) using the `NSGAIISampler`. The result is not a single best model but a **Pareto front**: the set of models where you cannot improve one objective without sacrificing another. A tiny 26-tree model and a larger 68-tree model both appear on the front, letting you consciously trade accuracy for speed.

### Pruning: stopping losers early

Much HPO compute is wasted finishing trials that were clearly going to be bad. **Pruning** kills unpromising trials early. The notebook explains **Hyperband / ASHA**-style pruning: during training you periodically `trial.report()` an intermediate score, and `trial.should_prune()` tells you whether Optuna has decided this trial is hopeless compared to its peers at which point you abort it and free the compute for promising trials. Pruning can multiply the number of configurations you can afford to explore.

## Whole-Pipeline AutoML

Beyond pure HPO, the notebook shows tools that automate the entire modeling process:

- **H2O AutoML.** With a single `train()` call it trains many models of different types and builds **stacked ensembles** (models that combine the predictions of other models). It produces a **leaderboard** ranking every model by performance, and you simply take the leader. It is the "press one button, get a strong model" option, popular in business settings.
- **TPOT.** Uses **genetic programming** an evolutionary algorithm that treats whole ML pipelines as organisms, breeding and mutating them across generations to *discover* novel preprocessing-plus-model combinations. It can then export the best pipeline as readable Python code, so the automation hands you maintainable source rather than a black box.

## Neural Architecture Search

For deep learning, the analogue of HPO is **Neural Architecture Search (NAS)** automatically discovering the *structure* of a neural network (how many layers, which operations, how they connect) rather than just tuning a fixed network. The notebook introduces **DARTS (Differentiable Architecture Search)**, which makes the discrete choice of architecture continuous so it can be optimized with gradient descent: it relaxes "which operation goes here?" into learnable weights `α` and solves a nested optimization that trains the network weights and the architecture weights together. At the practical end, **AutoKeras** wraps NAS behind a scikit-learn-style `fit` interface, so structured-data classification becomes a few lines and the discovered network can be exported as a standard Keras model.

## How AutoML Fits Into MLOps

AutoML is a force multiplier inside the broader MLOps machinery rather than a replacement for it. Every trial Optuna runs is an **experiment** that belongs in the experiment tracker (`01_experiment_tracking`) logging each trial's params and score is exactly what trackers are for, and HPO studies are commonly logged as parent-and-child (nested) runs. The winning model from an AutoML search flows into the **model registry** (`05_model_registry`) and through the same promotion **gates** as any other model. AutoML can even run *inside* an orchestrated retraining **pipeline** (`03_pipeline_orchestration`), automatically re-searching for the best model when monitoring detects drift.

A word of caution the field stresses: AutoML automates the *search*, not the *judgment*. It still needs you to define a sound objective, prevent data leakage, choose meaningful validation, and check the result for fairness and robustness (`07_testing_in_ml`). Used well, it frees experts from tedious tuning so they can focus on the problems automation cannot solve framing the task, curating the data, and deciding whether the model is truly fit to deploy.
