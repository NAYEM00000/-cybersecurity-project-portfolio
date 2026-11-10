import argparse
import hashlib
import json
import os
import tempfile
from pathlib import Path


FORMAT_VERSION = 1
HASH_ALGORITHM = "sha256"


def _hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as file_handle:
        for chunk in iter(lambda: file_handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _validate_paths(directory: str | Path, manifest: str | Path) -> tuple[Path, Path]:
    root = Path(directory).expanduser().resolve()
    manifest_path = Path(manifest).expanduser().resolve()

    if not root.exists() or not root.is_dir():
        raise ValueError("The monitored path must be an existing directory.")
    try:
        manifest_path.relative_to(root)
    except ValueError:
        return root, manifest_path

    raise ValueError(
        "Keep the baseline file outside the monitored directory."
    )


def scan_directory(directory: str | Path) -> dict[str, str]:
    """Return SHA-256 hashes for regular files; do not follow symlinks."""
    root = Path(directory).expanduser().resolve()
    if not root.exists() or not root.is_dir():
        raise ValueError("The monitored path must be an existing directory.")

    hashes = {}
    for current, directories, filenames in os.walk(root, followlinks=False):
        current_path = Path(current)
        directories[:] = sorted(
            name for name in directories
            if not (current_path / name).is_symlink()
        )

        for filename in sorted(filenames):
            file_path = current_path / filename
            if file_path.is_symlink() or not file_path.is_file():
                continue
            relative_path = file_path.relative_to(root).as_posix()
            hashes[relative_path] = _hash_file(file_path)

    return dict(sorted(hashes.items()))


def create_baseline(directory: str | Path, manifest: str | Path) -> dict:
    root, manifest_path = _validate_paths(directory, manifest)
    manifest_path.parent.mkdir(parents=True, exist_ok=True)

    data = {
        "format_version": FORMAT_VERSION,
        "algorithm": HASH_ALGORITHM,
        "files": scan_directory(root),
    }

    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=manifest_path.parent,
            prefix=manifest_path.name + ".",
            suffix=".tmp",
            delete=False,
        ) as temporary_file:
            temporary_path = Path(temporary_file.name)
            json.dump(data, temporary_file, indent=2)
            temporary_file.write("\n")
        os.replace(temporary_path, manifest_path)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()

    return data


def load_baseline(manifest: str | Path) -> dict:
    with Path(manifest).expanduser().open(encoding="utf-8") as manifest_file:
        data = json.load(manifest_file)

    if data.get("format_version") != FORMAT_VERSION:
        raise ValueError("Unsupported baseline format version.")
    if data.get("algorithm") != HASH_ALGORITHM:
        raise ValueError("The baseline must use SHA-256.")
    if not isinstance(data.get("files"), dict):
        raise ValueError("The baseline does not contain a valid files map.")
    for name, digest in data["files"].items():
        if not isinstance(name, str) or not isinstance(digest, str):
            raise ValueError("The baseline contains an invalid file entry.")
        if len(digest) != 64 or any(c not in "0123456789abcdef" for c in digest):
            raise ValueError(f"Invalid SHA-256 digest for {name!r}.")

    return data


def compare_with_baseline(directory: str | Path, manifest: str | Path) -> dict:
    root, manifest_path = _validate_paths(directory, manifest)
    baseline = load_baseline(manifest_path)["files"]
    current = scan_directory(root)

    baseline_names = set(baseline)
    current_names = set(current)

    added = sorted(current_names - baseline_names)
    removed = sorted(baseline_names - current_names)
    modified = sorted(
        name for name in baseline_names & current_names
        if baseline[name] != current[name]
    )

    return {"added": added, "modified": modified, "removed": removed}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Create or check a SHA-256 baseline for a directory."
    )
    commands = parser.add_subparsers(dest="command", required=True)

    baseline_parser = commands.add_parser("baseline", help="Create a baseline.")
    baseline_parser.add_argument("directory")
    baseline_parser.add_argument("--manifest", required=True)

    verify_parser = commands.add_parser("verify", help="Compare files with a baseline.")
    verify_parser.add_argument("directory")
    verify_parser.add_argument("--manifest", required=True)

    args = parser.parse_args()
    try:
        if args.command == "baseline":
            result = create_baseline(args.directory, args.manifest)
            print(f"Baseline saved. Files recorded: {len(result['files'])}")
            return 0

        changes = compare_with_baseline(args.directory, args.manifest)
        for category in ("added", "modified", "removed"):
            print(f"{category.title()}:")
            for filename in changes[category]:
                print(f"  {filename}")
            if not changes[category]:
                print("  None")

        changed = any(changes.values())
        print("Changes found." if changed else "No changes found.")
        return 1 if changed else 0
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print(f"Error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
