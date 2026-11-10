# Experiment protocol

This protocol must be followed before interpreting or publishing results.

## Dataset and split

Use the official UNSW-NB15 files supplied by UNSW:

- `UNSW_NB15_training-set.csv`
- `UNSW_NB15_testing-set.csv`

Use the provided training file for fitting and the provided testing file once for final evaluation. Do not merge the files and randomly resplit them for the primary result. Record file hashes, byte sizes, download date, and row/column counts.

## Target and excluded fields

- Target: `label` (`0 = normal`, `1 = attack`).
- Exclude `attack_cat`, because it describes the attack class and is not available as an independent feature for this binary task.
- Exclude `id`, which is a record identifier.
- Exclude source/destination IP columns if present, to reduce host-identity memorisation.
- Keep other documented flow fields unless a data-quality review identifies a specific reason to remove them. Any additional exclusion must be documented before model evaluation.

## Preprocessing

Fit all preprocessing using training data only:

- numeric: median imputation, then standard scaling;
- categorical: most-frequent imputation, then one-hot encoding;
- unseen test categories: ignore safely.

The same preprocessing strategy is used for both classifiers. The pipeline ensures that imputation, scaling, and category discovery are not fitted on the test data.

## Baseline models

1. Logistic Regression (`class_weight="balanced"`, fixed random state, bounded iteration count).
2. Random Forest (`class_weight="balanced_subsample"`, fixed random state, documented tree count).

The exact hyperparameters are stored in the source code and must be recorded with the run.

## Evaluation metrics

Report at minimum:

- accuracy;
- balanced accuracy;
- precision, recall, and F1-score for each class;
- macro and weighted averages;
- ROC-AUC, when both classes are present;
- confusion matrix;
- false-positive rate: FP / (FP + TN).

Do not compare models using accuracy alone. Interpret false positives and false negatives separately.

## Leakage and test-set discipline

- Do not use `label` or `attack_cat` as input features.
- Do not fit preprocessing on the test set.
- Do not tune hyperparameters against the official test results.
- Do not repeatedly choose models based on the test set and then report the same test set as an unbiased final estimate.
- If tuning is later needed, split the official training set into training/validation partitions or use cross-validation within training only. Keep the official test set untouched until final evaluation.

## Reproducibility

Record:

- dataset URL and download date;
- SHA-256 for both CSV files;
- Python and package versions;
- Git commit;
- exact command;
- model hyperparameters;
- output folder;
- any warnings or deviations.

Use `research/run_log_template.md`.

## Interpretation

Benchmark results are evidence about this dataset and split only. They do not establish production readiness, detection of every attack, or performance on current networks. A future external validation should use a separate dataset and a predeclared evaluation protocol.
