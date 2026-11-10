import argparse
import csv
from collections import defaultdict


REQUIRED_COLUMNS = {
    "timestamp", "src_ip", "dst_ip", "dst_port", "bytes", "protocol"
}


def analyze(
    path: str,
    ports_threshold: int = 10,
    bytes_threshold: int = 10_000_000,
) -> list[dict]:
    """Flag source addresses with many destination ports or high byte totals."""
    for name, value in (
        ("ports_threshold", ports_threshold),
        ("bytes_threshold", bytes_threshold),
    ):
        if not isinstance(value, int) or isinstance(value, bool):
            raise TypeError(f"{name} must be an integer")
        if value < 1:
            raise ValueError(f"{name} must be at least 1")

    ports_by_source = defaultdict(set)
    bytes_by_source = defaultdict(int)

    with open(path, newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        if not REQUIRED_COLUMNS.issubset(reader.fieldnames or []):
            raise ValueError(
                "CSV must contain: timestamp, src_ip, dst_ip, "
                "dst_port, bytes, protocol"
            )

        for line_number, row in enumerate(reader, start=2):
            source_ip = (row.get("src_ip") or "").strip()
            if not source_ip:
                continue

            raw_port = (row.get("dst_port") or "").strip()
            destination_port = raw_port or "N/A"
            if raw_port:
                try:
                    port_number = int(raw_port)
                except ValueError as error:
                    raise ValueError(
                        f"Invalid destination port on CSV line {line_number}"
                    ) from error
                if not 0 <= port_number <= 65535:
                    raise ValueError(
                        f"Destination port out of range on CSV line {line_number}"
                    )

            try:
                byte_count = int(row.get("bytes", ""))
            except (TypeError, ValueError) as error:
                raise ValueError(
                    f"Invalid byte count on CSV line {line_number}"
                ) from error
            if byte_count < 0:
                raise ValueError(
                    f"Negative byte count on CSV line {line_number}"
                )

            ports_by_source[source_ip].add(destination_port)
            bytes_by_source[source_ip] += byte_count

    alerts = []
    for source_ip in sorted(set(ports_by_source) | set(bytes_by_source)):
        distinct_ports = len(ports_by_source[source_ip])
        total_bytes = bytes_by_source[source_ip]

        if distinct_ports >= ports_threshold:
            alerts.append({
                "type": "many_distinct_destination_ports",
                "source_ip": source_ip,
                "distinct_ports": distinct_ports,
            })
        if total_bytes >= bytes_threshold:
            alerts.append({
                "type": "high_total_bytes",
                "source_ip": source_ip,
                "bytes": total_bytes,
            })

    return alerts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Review an exported network-flow CSV file."
    )
    parser.add_argument("csv_file")
    parser.add_argument("--ports-threshold", type=int, default=10)
    parser.add_argument("--bytes-threshold", type=int, default=10_000_000)
    args = parser.parse_args()

    try:
        for alert in analyze(
            args.csv_file, args.ports_threshold, args.bytes_threshold
        ):
            print("ALERT:", alert)
    except (OSError, TypeError, ValueError) as error:
        raise SystemExit(f"Error: {error}")
