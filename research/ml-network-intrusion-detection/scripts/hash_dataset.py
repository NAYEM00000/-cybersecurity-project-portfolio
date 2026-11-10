"""Print SHA-256 hashes for the two official UNSW-NB15 split files."""
import argparse
import hashlib
from pathlib import Path

from nids.data import TRAIN_FILE, TEST_FILE


def sha256(path):
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", default="data/raw")
    args = parser.parse_args()
    folder = Path(args.data_dir)
    for name in (TRAIN_FILE, TEST_FILE):
        path = folder / name
        if not path.exists():
            raise FileNotFoundError(path)
        print(f"{sha256(path)}  {path}")


if __name__ == "__main__":
    main()
