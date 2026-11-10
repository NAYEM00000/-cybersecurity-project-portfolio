"""Train and evaluate the baseline models on the official UNSW-NB15 split."""
import argparse
import json
import platform
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
import sklearn

from nids.data import load_official_split
from nids.evaluation import evaluate_and_save, save_random_forest_importance
from nids.models import build_pipeline


def parse_args():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/raw", help="Folder containing the official UNSW-NB15 CSV split.")
    parser.add_argument("--output-dir", default="results", help="Folder for metrics, plots, predictions, and models.")
    parser.add_argument(
        "--models", nargs="+",
        choices=["logistic_regression", "random_forest"],
        default=["logistic_regression", "random_forest"],
    )
    return parser.parse_args()


def main():
    args = parse_args()
    X_train, X_test, y_train, y_test = load_official_split(args.data_dir)
    print(f"Training rows: {len(X_train):,}; test rows: {len(X_test):,}")
    print(f"Features: {X_train.shape[1]}")
    print("Training label counts:", y_train.value_counts().sort_index().to_dict())
    print("Test label counts:", y_test.value_counts().sort_index().to_dict())

    summary = {
        "python": platform.python_version(),
        "pandas": pd.__version__,
        "numpy": np.__version__,
        "scikit_learn": sklearn.__version__,
        "train_rows": int(len(X_train)),
        "test_rows": int(len(X_test)),
        "feature_count": int(X_train.shape[1]),
        "models": {},
    }
    root = Path(args.output_dir)
    root.mkdir(parents=True, exist_ok=True)

    for model_name in args.models:
        print(f"\nTraining {model_name} ...")
        model = build_pipeline(model_name)
        model.fit(X_train, y_train)
        model_dir = root / model_name
        model_dir.mkdir(parents=True, exist_ok=True)
        metrics = evaluate_and_save(model, model_name, X_test, y_test, model_dir)
        joblib.dump(model, model_dir / "model.joblib")
        if model_name == "random_forest":
            save_random_forest_importance(model, model_dir)
        summary["models"][model_name] = metrics
        print(json.dumps(metrics, indent=2))

    (root / "experiment_summary.json").write_text(
        json.dumps(summary, indent=2), encoding="utf-8"
    )
    print(f"\nSaved experiment outputs to: {root.resolve()}")


if __name__ == "__main__":
    main()
