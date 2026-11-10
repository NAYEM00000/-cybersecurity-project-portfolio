# Results analysis template

Complete this document only after running the experiment.

## 1. Dataset verification

Report the exact files, row counts, class distributions, missing values, duplicate counts, and SHA-256 hashes.

## 2. Model comparison

Insert the generated metrics for Logistic Regression and Random Forest. Compare class-wise precision, recall, F1-score, balanced accuracy, ROC-AUC, and false-positive rate.

## 3. Confusion-matrix analysis

Explain false positives and false negatives in the context of defensive network monitoring. Do not treat these errors as equally costly without explaining the operational context.

## 4. Feature analysis

If Random Forest feature importance is reported, explain that impurity-based importance is not causal and may be biased. Consider permutation importance on a validation set as a later extension.

## 5. Hypothesis review

For each hypothesis, state supported / not supported / inconclusive and cite the generated metric or plot.

## 6. Limitations

Discuss benchmark representativeness, possible dataset artefacts, class imbalance, and lack of external validation.

## 7. Conclusion

State only what the experiment supports. Avoid claims such as “detects all attacks”, “real-world accurate”, or “production-ready”.
