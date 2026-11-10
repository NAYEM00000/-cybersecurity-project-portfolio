# Research proposal

## Working title

**A Reproducible Baseline Comparison of Logistic Regression and Random Forest for Binary Network Intrusion Detection on UNSW-NB15**

## 1. Background

Network intrusion detection analyses network activity to identify flows associated with malicious behaviour. Machine-learning methods can learn patterns from labelled flow records, but benchmark performance can be affected by class imbalance, preprocessing choices, dataset artefacts, and differences between training and deployment environments.

This project establishes a transparent baseline comparison using the official UNSW-NB15 training and testing files. It is deliberately scoped as a reproducible empirical study rather than a claim of a new detection algorithm.

## 2. Problem statement

A classifier may achieve high overall accuracy while still missing important attack traffic or generating an operationally unacceptable number of false alarms. A careful evaluation must therefore compare class-wise precision and recall, F1-score, ROC-AUC, and false-positive rate using a held-out test set.

## 3. Research question

On the official UNSW-NB15 split, how do Logistic Regression and Random Forest compare for binary normal-versus-attack flow classification when both use the same training-fitted preprocessing and are evaluated with class-sensitive metrics?

## 4. Objectives

1. Prepare the official training and testing CSV files using a documented, repeatable pipeline.
2. Exclude direct target information and record identifiers from the input features.
3. Train Logistic Regression and Random Forest baselines with class weighting.
4. Evaluate both models on the untouched official test split.
5. Compare accuracy, balanced accuracy, precision, recall, F1-score, ROC-AUC, and false-positive rate.
6. Inspect the confusion matrix and the most influential Random Forest features.
7. Document limitations and propose a cautious next-stage external validation.

## 5. Research hypotheses

- **H1:** The two baseline classifiers will show different precision/recall trade-offs on the official test set.
- **H2:** Overall accuracy alone will not fully describe the operational usefulness of either classifier.
- **H3:** False-positive and false-negative counts will provide information that is not visible from a single aggregate score.

These are hypotheses to be tested. No outcome is assumed in advance.

## 6. Scope

- Dataset: official UNSW-NB15 train/test CSV split.
- Task: binary classification (`label`: normal or attack).
- Models: Logistic Regression and Random Forest.
- Evaluation: fixed held-out test set.
- Excluded from this first phase: live packet capture, active scanning, malware execution, and deployment as a production IDS.

## 7. Expected contribution

The expected contribution is a clearly documented and reproducible comparison of two conventional baselines, including transparent preprocessing, test-set evaluation, error analysis, and limitations. The project does not claim algorithmic novelty.
