"""Print basic data-quality information without training a model."""
import argparse
from pathlib import Path
import pandas as pd

from nids.data import TRAIN_FILE, TEST_FILE, normalise_columns


def inspect(path):
    frame = normalise_columns(pd.read_csv(path, low_memory=False))
    print(f"\n{path.name}")
    print(f"Shape: {frame.shape[0]:,} rows x {frame.shape[1]} columns")
    if "label" in frame.columns:
        print("Label counts:", frame["label"].value_counts(dropna=False).to_dict())
    print("Duplicate rows:", int(frame.duplicated().sum()))
    missing = frame.isna().sum()
    print("Columns with missing values:")
    print(missing[missing > 0].sort_values(ascending=False).to_string() or "None")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/raw")
    args = parser.parse_args()
    folder = Path(args.data_dir)
    for filename in (TRAIN_FILE, TEST_FILE):
        path = folder / filename
        if not path.exists():
            raise FileNotFoundError(f"Missing {path}. Read data/README.md.")
        inspect(path)


if __name__ == "__main__":
    main()
