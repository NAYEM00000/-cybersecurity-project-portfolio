"""Loading and validating the official UNSW-NB15 CSV split."""
from pathlib import Path
import pandas as pd

TRAIN_FILE = "UNSW_NB15_training-set.csv"
TEST_FILE = "UNSW_NB15_testing-set.csv"
TARGET = "label"
EXCLUDED_FEATURES = {"id", "attack_cat", "srcip", "dstip"}


def normalise_columns(frame: pd.DataFrame) -> pd.DataFrame:
    """Trim headers and remove a possible UTF-8 BOM."""
    result = frame.copy()
    result.columns = [str(col).replace("\ufeff", "").strip() for col in result.columns]
    if len(set(result.columns)) != len(result.columns):
        raise ValueError("Duplicate column names found after normalisation.")
    return result


def split_features_target(frame: pd.DataFrame):
    """Return X, y while excluding target-derived and identifier columns."""
    frame = normalise_columns(frame)
    target_col = next((c for c in frame.columns if c.casefold() == TARGET), None)
    if target_col is None:
        raise ValueError("Required binary target column 'label' was not found.")

    y = pd.to_numeric(frame[target_col], errors="coerce")
    if y.isna().any():
        raise ValueError("Target 'label' contains missing or non-numeric values.")
    values = set(y.unique().tolist())
    if not values.issubset({0, 1}) or len(values) != 2:
        raise ValueError(
            f"Expected both binary labels 0 and 1; found {sorted(values)}."
        )

    excluded = {target_col}
    excluded.update(c for c in frame.columns if c.casefold() in EXCLUDED_FEATURES)
    X = frame.drop(columns=sorted(excluded), errors="ignore")
    if X.empty:
        raise ValueError("No usable feature columns remain after exclusions.")

    # Convert +/- infinity to missing values; imputers handle missing values later.
    numeric_cols = X.select_dtypes(include=["number"]).columns
    if len(numeric_cols):
        X.loc[:, numeric_cols] = X.loc[:, numeric_cols].replace(
            [float("inf"), float("-inf")], float("nan")
        )
    return X, y.astype("int8")


def load_official_split(data_dir):
    """Load UNSW-NB15's published train and test CSV files."""
    data_dir = Path(data_dir)
    train_path = data_dir / TRAIN_FILE
    test_path = data_dir / TEST_FILE
    missing = [str(p) for p in (train_path, test_path) if not p.exists()]
    if missing:
        raise FileNotFoundError(
            "Missing dataset file(s): " + ", ".join(missing)
            + ". See data/README.md for download instructions."
        )

    train = pd.read_csv(train_path, low_memory=False)
    test = pd.read_csv(test_path, low_memory=False)
    X_train, y_train = split_features_target(train)
    X_test, y_test = split_features_target(test)

    # Align test columns to the training schema. Extra test-only columns are excluded.
    X_test = X_test.reindex(columns=X_train.columns)
    if X_train.shape[1] != X_test.shape[1]:
        raise ValueError("Training and test feature schemas could not be aligned.")
    return X_train, X_test, y_train, y_test
