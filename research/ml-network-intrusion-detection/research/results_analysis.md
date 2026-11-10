# Results and analysis — first baseline experiment

## 1. Study question

How do Logistic Regression and Random Forest compare for binary normal-versus-attack classification on the official UNSW-NB15 training/testing files when both use the same train-fitted preprocessing pipeline?

## 2. Dataset checks

The supplied files contain 175,341 training rows and 82,332 test rows, each with 45 columns. No missing values, duplicate rows, or numeric infinite values were found in either file.

After excluding the record identifier (`id`), target-derived category (`attack_cat`), and target (`label`), 42 features remained. The model task is binary classification: `0 = normal`, `1 = attack`.

The class proportions differ between the supplied splits: attacks make up 68.06% of training records and 55.06% of test records. This difference should be considered when interpreting the results and when designing future validation.

## 3. Method

The same preprocessing approach was used for both models:

- Numeric columns: median imputation and standard scaling.
- Categorical columns: most-frequent imputation and one-hot encoding.
- All preprocessing was fitted on the training data only.
- Unknown test categories were ignored safely.
- The supplied test file was reserved for evaluation and was not used for tuning.

Two baselines were evaluated:

1. Logistic Regression with balanced class weights, `max_iter=1500`, `solver=liblinear`, and random seed 42.
2. Random Forest with 40 trees, maximum depth 16, minimum leaf size 4, balanced-subsample class weights, two worker processes, and random seed 42.

The Random Forest configuration is a computationally bounded baseline, not an optimised configuration.

## 4. Results

Positive class: attack (`label=1`).

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 83.55% | 90.82% |
| Balanced accuracy | 82.48% | 90.13% |
| Attack precision | 80.22% | 87.69% |
| Attack recall | 93.06% | 96.94% |
| Attack F1-score | 86.17% | 92.08% |
| ROC-AUC | 95.60% | 98.44% |
| False-positive rate | 28.11% | 16.67% |

### Confusion matrix counts

| Model | True negatives | False positives | False negatives | True positives |
|---|---:|---:|---:|---:|
| Logistic Regression | 26,599 | 10,401 | 3,145 | 42,187 |
| Random Forest | 30,831 | 6,169 | 1,387 | 43,945 |

## 5. Interpretation

The Random Forest baseline achieved higher values for accuracy, balanced accuracy, attack precision, attack recall, attack F1-score, and ROC-AUC on this test split. Its false-positive rate was lower.

Compared with Logistic Regression, Random Forest produced 4,232 fewer false positives (40.7% fewer relative to the Logistic Regression count) and 1,758 fewer false negatives (55.9% fewer relative to the Logistic Regression count).

This does not establish that Random Forest is universally superior. It establishes only that this particular Random Forest configuration performed better on this particular supplied benchmark split. A different threshold, dataset, network environment, or model configuration may change the comparison.

## 6. Feature importance

The Random Forest's impurity-based feature importance is saved in `results/random_forest/feature_importance.csv`. The leading features are exploratory signals only. Impurity-based importance can be biased and does not demonstrate causation. Permutation importance on a training-derived validation set and domain-based review are recommended before interpreting feature relevance.

## 7. Limitations

1. The experiment uses one benchmark dataset and one official split.
2. The training and test attack proportions differ.
3. UNSW-NB15 reflects a particular data-generation and capture environment; it is not a current live enterprise network.
4. The task is binary, so differences among attack categories are not modelled.
5. Only two baseline models were evaluated.
6. The Random Forest has a bounded configuration and has not been tuned.
7. No external dataset validation has been completed.
8. The result does not establish production readiness or real-world detection rates.

## 8. Conclusion

For the supplied UNSW-NB15 test split, the 40-tree Random Forest baseline outperformed the Logistic Regression baseline across the selected aggregate metrics and had a lower false-positive rate. The finding is preliminary and dataset-specific. The next research stage should focus on error analysis, robustness checks, and external validation rather than claiming a novel or production-ready intrusion detector.


## 9. Internal cross-validation and attack-category error analysis

A stratified three-fold cross-validation was run on the training split only. Fold-level metrics and mean ± sample standard deviation are available in `results/cross_validation_folds.csv` and `results/cross_validation_summary.csv`. The summary is documented in `research/robustness_and_error_analysis.md`. Random Forest had the stronger mean balanced accuracy, attack precision, F1-score and ROC-AUC; Logistic Regression had slightly higher mean attack recall. This is internal validation, not a second independent test set.

Post-hoc attack-category recall on the official test predictions is available in `results/attack_category_recall.csv`. Fuzzers had the lowest recall for both models and should be the focus of the next error-analysis iteration. The category labels were not used as model features.

A full-row hash screen found no exact 45-column row duplicates across the supplied train/test split. This does not rule out near-duplicate flows or temporal/capture-related leakage. External validation on CIC-IDS2017 remains pending a documented feature mapping.
