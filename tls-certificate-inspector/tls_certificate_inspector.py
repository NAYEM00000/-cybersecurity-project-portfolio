import argparse
import json
import socket
import ssl
from datetime import datetime, timezone


def _format_name(name: tuple) -> str:
    parts = []
    for relative_name in name or ():
        for key, value in relative_name:
            parts.append(f"{key}={value}")
    return ", ".join(parts)


def summarize_certificate(
    certificate: dict,
    hostname: str,
    port: int,
    tls_version: str | None,
    cipher: tuple | None,
    now: datetime | None = None,
) -> dict:
    """Convert the peer certificate details into a JSON-friendly summary."""
    if not certificate or "notAfter" not in certificate:
        raise ValueError("The server did not provide a readable certificate.")

    expiry_timestamp = ssl.cert_time_to_seconds(certificate["notAfter"])
    expires_at = datetime.fromtimestamp(expiry_timestamp, tz=timezone.utc)
    current_time = now or datetime.now(timezone.utc)
    days_remaining = int((expires_at - current_time).total_seconds() // 86400)

    if days_remaining < 0:
        expiry_status = "expired"
    elif days_remaining <= 30:
        expiry_status = "expires_within_30_days"
    else:
        expiry_status = "ok"

    cipher_details = None
    if cipher:
        cipher_details = {
            "name": cipher[0],
            "protocol": cipher[1] if len(cipher) > 1 else None,
            "bits": cipher[2] if len(cipher) > 2 else None,
        }

    return {
        "host": hostname,
        "port": port,
        "certificate_verified": True,
        "tls_version": tls_version,
        "cipher": cipher_details,
        "subject": _format_name(certificate.get("subject", ())),
        "issuer": _format_name(certificate.get("issuer", ())),
        "subject_alt_names": [
            {"type": kind, "value": value}
            for kind, value in certificate.get("subjectAltName", ())
        ],
        "not_before": certificate.get("notBefore"),
        "not_after": expires_at.isoformat(),
        "days_remaining": days_remaining,
        "expiry_status": expiry_status,
    }


def inspect_certificate(hostname: str, port: int = 443, timeout: float = 5.0) -> dict:
    """Make one verified TLS connection and inspect the peer certificate."""
    if not isinstance(hostname, str) or not hostname.strip():
        raise ValueError("Provide a hostname.")
    if any(character.isspace() for character in hostname):
        raise ValueError("The hostname must not contain whitespace.")
    if not isinstance(port, int) or isinstance(port, bool) or not 1 <= port <= 65535:
        raise ValueError("Port must be an integer from 1 to 65535.")
    if timeout <= 0:
        raise ValueError("Timeout must be greater than zero.")

    hostname = hostname.strip()
    context = ssl.create_default_context()

    with socket.create_connection((hostname, port), timeout=timeout) as raw_socket:
        with context.wrap_socket(raw_socket, server_hostname=hostname) as tls_socket:
            certificate = tls_socket.getpeercert()
            return summarize_certificate(
                certificate=certificate,
                hostname=hostname,
                port=port,
                tls_version=tls_socket.version(),
                cipher=tls_socket.cipher(),
            )


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect the TLS certificate presented by one host."
    )
    parser.add_argument("hostname")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--json", dest="output")
    args = parser.parse_args()

    try:
        report = inspect_certificate(args.hostname, args.port, args.timeout)
        rendered = json.dumps(report, indent=2)
        print(rendered)
        if args.output:
            with open(args.output, "w", encoding="utf-8") as output_file:
                output_file.write(rendered + "\n")
        return 0
    except (OSError, ssl.SSLError, ValueError) as error:
        print(f"Error: {error}")
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
