# Experiment outputs

The first baseline experiment has been run on the supplied UNSW-NB15 train/test files.

- `model_comparison.csv`: aggregate metric comparison.
- `class_distribution.csv`: normal/attack distribution in each split.
- `experiment_summary_2026-11-11.json`: machine-readable dataset and model summary.
- Each model folder contains metrics, class-wise report, predictions, confusion matrix, and ROC curve.
- Random Forest feature importance is exploratory and not causal.

See `../research/results_analysis.md` and `../research/run_log_2026-11-11.md` for methodology, provenance, interpretation, and limitations. Raw dataset files and fitted model binaries are not included in this repository update.
