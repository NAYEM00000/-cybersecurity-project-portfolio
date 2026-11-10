"""Metrics and plots for held-out binary classification evaluation."""
import json
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    balanced_accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
    roc_curve,
)


def evaluate_and_save(model, model_name, X_test, y_test, output_dir):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    predictions = model.predict(X_test)
    probabilities = model.predict_proba(X_test)[:, 1] if hasattr(model, "predict_proba") else None
    tn, fp, fn, tp = confusion_matrix(y_test, predictions, labels=[0, 1]).ravel()
    false_positive_rate = float(fp / (fp + tn)) if (fp + tn) else 0.0

    metrics = {
        "model": model_name,
        "test_samples": int(len(y_test)),
        "accuracy": float(accuracy_score(y_test, predictions)),
        "balanced_accuracy": float(balanced_accuracy_score(y_test, predictions)),
        "precision_attack": float(precision_score(y_test, predictions, pos_label=1, zero_division=0)),
        "recall_attack": float(recall_score(y_test, predictions, pos_label=1, zero_division=0)),
        "f1_attack": float(f1_score(y_test, predictions, pos_label=1, zero_division=0)),
        "false_positive_rate": false_positive_rate,
        "tn": int(tn), "fp": int(fp), "fn": int(fn), "tp": int(tp),
    }
    if probabilities is not None and len(np.unique(y_test)) == 2:
        metrics["roc_auc"] = float(roc_auc_score(y_test, probabilities))
    else:
        metrics["roc_auc"] = None

    report = classification_report(
        y_test, predictions, labels=[0, 1],
        target_names=["normal", "attack"],
        output_dict=True, zero_division=0,
    )
    (output_dir / "metrics.json").write_text(
        json.dumps(metrics, indent=2), encoding="utf-8"
    )
    (output_dir / "classification_report.json").write_text(
        json.dumps(report, indent=2), encoding="utf-8"
    )

    pd.DataFrame({
        "y_true": np.asarray(y_test),
        "y_pred": np.asarray(predictions),
        **({"attack_probability": probabilities} if probabilities is not None else {}),
    }).to_csv(output_dir / "predictions.csv", index=False)

    cm = np.array([[tn, fp], [fn, tp]])
    fig, ax = plt.subplots(figsize=(5.5, 4.5))
    image = ax.imshow(cm, interpolation="nearest")
    ax.set(
        title=f"{model_name}: confusion matrix",
        xlabel="Predicted label",
        ylabel="True label",
        xticks=[0, 1], yticks=[0, 1],
        xticklabels=["Normal", "Attack"],
        yticklabels=["Normal", "Attack"],
    )
    fig.colorbar(image, ax=ax)
    threshold = cm.max() / 2 if cm.size else 0
    for i in range(2):
        for j in range(2):
            ax.text(j, i, f"{cm[i, j]:,}", ha="center", va="center",
                    color="white" if cm[i, j] > threshold else "black")
    fig.tight_layout()
    fig.savefig(output_dir / "confusion_matrix.png", dpi=160)
    plt.close(fig)

    if probabilities is not None and len(np.unique(y_test)) == 2:
        fpr, tpr, _ = roc_curve(y_test, probabilities)
        fig, ax = plt.subplots(figsize=(5.5, 4.5))
        ax.plot(fpr, tpr, label=f"ROC-AUC = {metrics['roc_auc']:.4f}")
        ax.plot([0, 1], [0, 1], linestyle="--", label="Chance")
        ax.set(xlabel="False Positive Rate", ylabel="True Positive Rate",
               title=f"{model_name}: ROC curve", xlim=(0, 1), ylim=(0, 1))
        ax.legend(loc="lower right")
        fig.tight_layout()
        fig.savefig(output_dir / "roc_curve.png", dpi=160)
        plt.close(fig)

    return metrics


def save_random_forest_importance(model, output_dir, top_n=30):
    """Save impurity-based importance as an exploratory aid, not causal evidence."""
    classifier = model.named_steps["classifier"]
    preprocessor = model.named_steps["preprocessor"]
    if not hasattr(classifier, "feature_importances_"):
        return
    names = preprocessor.get_feature_names_out()
    values = classifier.feature_importances_
    table = pd.DataFrame({"feature": names, "importance": values})
    table.sort_values("importance", ascending=False).head(top_n).to_csv(
        Path(output_dir) / "feature_importance.csv", index=False
    )
