import argparse, csv
from collections import defaultdict

def analyze(path, ports_threshold, bytes_threshold):
    ports, totals = defaultdict(set), defaultdict(int)
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        required = {"timestamp", "src_ip", "dst_ip", "dst_port", "bytes", "protocol"}
        if not required.issubset(reader.fieldnames or []):
            raise ValueError("CSV must contain: timestamp, src_ip, dst_ip, dst_port, bytes, protocol")
        for row in reader:
            src = row["src_ip"]
            ports[src].add(row["dst_port"])
            totals[src] += int(row["bytes"])
    alerts = []
    for src in set(ports) | set(totals):
        if len(ports[src]) >= ports_threshold:
            alerts.append({"type": "many_distinct_destination_ports", "source_ip": src,
                           "distinct_ports": len(ports[src])})
        if totals[src] >= bytes_threshold:
            alerts.append({"type": "high_total_bytes", "source_ip": src, "bytes": totals[src]})
    return alerts

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("csv_file")
    p.add_argument("--ports-threshold", type=int, default=10)
    p.add_argument("--bytes-threshold", type=int, default=10_000_000)
    a = p.parse_args()
    try:
        for alert in analyze(a.csv_file, max(2, a.ports_threshold), max(1, a.bytes_threshold)):
            print("ALERT:", alert)
    except (OSError, ValueError) as e:
        raise SystemExit(f"Error: {e}")
