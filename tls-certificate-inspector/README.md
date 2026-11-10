# TLS Certificate Inspector

This script opens one TLS connection to a host and prints details from the certificate presented by the server. It uses Python's default SSL context, so normal certificate-chain and hostname verification are enabled.

## Run

```bash
python tls_certificate_inspector.py example.com
```

Use a different port or save the report as JSON:

```bash
python tls_certificate_inspector.py example.com --port 443 --json certificate-report.json
```

## What it reports

- TLS version and negotiated cipher
- Certificate subject and issuer
- Subject Alternative Names (SANs)
- Validity end date and days remaining

## Scope and limitations

This makes one connection to the host and port you specify. Only inspect hosts you own or are authorized to assess. It is not a port scanner or a full TLS configuration audit. It does not test every protocol version, cipher suite, certificate revocation status, or application endpoint.
