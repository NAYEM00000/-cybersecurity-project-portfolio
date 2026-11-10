import argparse
import csv
from collections import Counter


REQUIRED_COLUMNS = {"timestamp", "username", "source_ip", "status"}


def analyze(path: str, threshold: int = 5) -> dict:
    """Count failed sign-ins by source IP and username in a CSV export."""
    if not isinstance(threshold, int) or isinstance(threshold, bool):
        raise TypeError("threshold must be an integer")
    if threshold < 1:
        raise ValueError("threshold must be at least 1")

    failed_by_ip = Counter()
    failed_by_user = Counter()

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain: timestamp, username, source_ip, status"
            )

        for row in reader:
            if (row.get("status") or "").strip().lower() != "failed":
                continue

            source_ip = (row.get("source_ip") or "").strip()
            username = (row.get("username") or "").strip()
            if source_ip:
                failed_by_ip[source_ip] += 1
            if username:
                failed_by_user[username] += 1

    alerts = [
        {
            "type": "repeated_failures_from_ip",
            "indicator": source_ip,
            "count": count,
        }
        for source_ip, count in sorted(failed_by_ip.items())
        if count >= threshold
    ]
    alerts.extend(
        {
            "type": "repeated_failures_for_user",
            "indicator": username,
            "count": count,
        }
        for username, count in sorted(failed_by_user.items())
        if count >= threshold
    )

    return {
        "failed_by_ip": dict(failed_by_ip),
        "failed_by_user": dict(failed_by_user),
        "alerts": alerts,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Find repeated failed sign-ins in a CSV log export."
    )
    parser.add_argument("csv_file")
    parser.add_argument("--threshold", type=int, default=5)
    args = parser.parse_args()

    try:
        report = analyze(args.csv_file, args.threshold)
        print("Failed sign-ins by IP:", report["failed_by_ip"])
        print("Failed sign-ins by username:", report["failed_by_user"])
        print("Alerts:")
        for alert in report["alerts"]:
            print(alert)
        if not report["alerts"]:
            print("No threshold-based alerts.")
    except (OSError, TypeError, ValueError) as error:
        raise SystemExit(f"Error: {error}")
