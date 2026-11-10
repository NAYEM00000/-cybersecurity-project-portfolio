import argparse, csv
from collections import Counter, defaultdict

def analyze(path, threshold):
    failed_by_ip, failed_by_user = Counter(), Counter()
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"timestamp", "username", "source_ip", "status"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain: timestamp, username, source_ip, status")
        for row in reader:
            if row["status"].strip().lower() == "failed":
                failed_by_ip[row["source_ip"]] += 1
                failed_by_user[row["username"]] += 1
    alerts = [{"type": "repeated_failures_from_ip", "indicator": ip, "count": n}
              for ip, n in failed_by_ip.items() if n >= threshold]
    alerts += [{"type": "repeated_failures_for_user", "indicator": user, "count": n}
               for user, n in failed_by_user.items() if n >= threshold]
    return {"failed_by_ip": dict(failed_by_ip), "failed_by_user": dict(failed_by_user), "alerts": alerts}

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("csv_file")
    p.add_argument("--threshold", type=int, default=5)
    a = p.parse_args()
    try:
        result = analyze(a.csv_file, max(2, a.threshold))
        print("Failed logins by IP:", result["failed_by_ip"])
        print("Failed logins by username:", result["failed_by_user"])
        print("Alerts:")
        for alert in result["alerts"]: print(alert)
        if not result["alerts"]: print("No threshold-based alerts.")
    except (OSError, ValueError) as e:
        raise SystemExit(f"Error: {e}")
