# Robustness and error analysis

## 1. Three-fold cross-validation on training data

A stratified three-fold cross-validation was run using only the UNSW-NB15 training split (175,341 records). Each fold used a fresh preprocessing pipeline fitted only on that fold's training partition. The official test split was not used in this cross-validation.

The same baseline model configurations were retained:
- Logistic Regression: balanced class weights, `max_iter=1500`, `solver=liblinear`, random state 42.
- Random Forest: 40 trees, maximum depth 16, minimum leaf size 4, balanced-subsample class weights, two workers, random state 42.

Metrics below are the mean and sample standard deviation across three folds. The standard deviation describes fold-to-fold variation; with only three folds it should not be interpreted as a precise uncertainty interval.

| Metric | Logistic Regression | Random Forest |
|---|---:|---:|
| Accuracy | 93.23% ± 0.24% | 94.64% ± 0.16% |
| Balanced accuracy | 92.15% ± 0.25% | 94.65% ± 0.16% |
| Attack precision | 94.91% ± 0.15% | 97.44% ± 0.09% |
| Attack recall | 95.16% ± 0.24% | 94.61% ± 0.15% |
| Attack F1-score | 95.04% ± 0.18% | 96.00% ± 0.12% |
| ROC-AUC | 98.43% ± 0.12% | 99.21% ± 0.05% |
| False-positive rate | 10.87% ± 0.31% | 5.30% ± 0.18% |

Across these folds, Random Forest had the higher mean accuracy, balanced accuracy, attack precision, attack F1-score, and ROC-AUC, and the lower mean false-positive rate. Logistic Regression had a slightly higher mean attack recall. This is a useful trade-off to preserve in the discussion rather than claiming one model is better for every operational objective.

## 2. Per-attack-category error analysis on the supplied test split

The category label was used only after prediction to group errors; it was not supplied to either classifier as an input feature. The table reports attack recall and false negatives by attack category.

| Attack category | Support | Logistic Regression recall | Random Forest recall | LR missed | RF missed |
|---|---:|---:|---:|---:|---:|
| Generic | 18,871 | 99.46% | 99.98% | 102 | 4 |
| Exploits | 11,132 | 91.87% | 99.27% | 905 | 81 |
| Fuzzers | 6,062 | 70.69% | 79.08% | 1,777 | 1,268 |
| DoS | 4,089 | 95.84% | 99.80% | 170 | 8 |
| Reconnaissance | 3,496 | 97.03% | 99.83% | 104 | 6 |
| Analysis | 677 | 91.43% | 98.23% | 58 | 12 |
| Backdoor | 583 | 98.46% | 99.66% | 9 | 2 |
| Shellcode | 378 | 95.50% | 98.41% | 17 | 6 |
| Worms | 44 | 93.18% | 100.00% | 3 | 0 |

The most prominent weakness for both models is **Fuzzers**: Random Forest detected 79.08% of these test records, while Logistic Regression detected 70.69%. This category contributes a large number of missed attacks and deserves focused follow-up.

Worms has only 44 test examples. Its recall estimate is therefore unstable and should not be treated as evidence of near-perfect detection for that attack family. The smaller Analysis, Backdoor, and Shellcode categories also have substantially less support than Generic and Exploits.

## 3. Train/test exact duplicate screening

A hash-based comparison of all 45 original columns found **0 exact full-row overlaps** between the training and testing files. This reduces concern about literal duplicate rows crossing the split, but it does not rule out near-duplicates, related flows, temporal dependence, or capture-environment leakage.

## 4. Why cross-validation scores differ from the official test results

The three-fold validation scores on the training file are higher than the earlier official test scores for both models. This gap suggests that the official test split is more difficult or differs in distribution from random folds drawn from the training set. The train/test attack prevalence also differs (68.06% versus 55.06%).

The official test set must remain a one-time benchmark reference. Do not tune hyperparameters or choose decision thresholds based on these already inspected test results. Future model selection should use validation data carved from training data, and final generalisation claims should rely on a separately sourced dataset.

## 5. Limitations

- Only three folds were used.
- The folds are random and stratified; they may share capture-specific patterns.
- The benchmark is not a live enterprise network.
- The test category labels are used only for post-hoc error grouping.
- No independent dataset validation has yet been run.
- The Random Forest configuration is a bounded baseline, not a tuned final model.

## 6. Next step

Run a separate external evaluation on CIC-IDS2017 after downloading its machine-learning CSV package. Because its flow-feature schema differs from UNSW-NB15, define and document a semantically valid common-feature mapping before training or transfer evaluation. Do not simply rename unrelated columns to force compatibility.
