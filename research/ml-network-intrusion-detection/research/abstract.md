# Abstract

**Status: preliminary baseline study.** This abstract reports the first completed experiment on the supplied UNSW-NB15 train/test files. It is not a claim of algorithmic novelty or external validation.

Network intrusion detection is a defensive security task in which network-flow records are classified as normal or attack-related. This study compares Logistic Regression and Random Forest for binary classification using the supplied UNSW-NB15 training split (175,341 records) and test split (82,332 records). Both models use a shared preprocessing pipeline fitted on training data only. The target-derived `attack_cat` field and record identifier `id` are excluded from the input features. Evaluation includes accuracy, balanced accuracy, attack-class precision, recall and F1-score, ROC-AUC, and false-positive rate.

On the supplied test split, Logistic Regression achieved 83.55% accuracy, 86.17% attack F1-score, and 95.60% ROC-AUC. A computationally bounded Random Forest configuration (40 trees, maximum depth 16) achieved 90.82% accuracy, 92.08% attack F1-score, and 98.44% ROC-AUC. Its false-positive rate was 16.67%, compared with 28.11% for Logistic Regression.

These results indicate that the evaluated Random Forest configuration performed better on this particular benchmark split. The class proportions differ between training and testing, and the study uses only one dataset and two baseline models. The findings therefore require robustness checks and external-dataset validation before broader conclusions can be made.
