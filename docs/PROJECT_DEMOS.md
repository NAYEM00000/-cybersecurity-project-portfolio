# Running the projects

These are command-line programs. Run each command from the matching project folder.

## Password Security Analyzer

```bash
cd password-security-analyzer
python password_analyzer.py
```

Choose whether to check a password or generate one. Password input is hidden and is not written to a file.

## Web Security Header Checker

```bash
python -m pip install -r ../requirements.txt
python header_checker.py https://example.com --json report.json
```

Makes one normal HTTP request. Check only URLs you are allowed to assess.

## Authentication Log Analyzer

```bash
python log_analyzer.py sample_auth.csv --threshold 5
```

Expected columns: `timestamp,username,source_ip,status`.

## Network Traffic Anomaly Detector

```bash
python traffic_detector.py sample_flows.csv --ports-threshold 5
```

Expected columns: `timestamp,src_ip,dst_ip,dst_port,bytes,protocol`.

## Phishing URL Risk Analyzer

```bash
python phishing_analyzer.py "http://login-example.test/verify?account=1"
```

The script parses the URL locally and does not visit it.

## File Integrity Monitor

```bash
python file_integrity_monitor.py baseline ./sample-folder --manifest ./baseline.json
python file_integrity_monitor.py verify ./sample-folder --manifest ./baseline.json
```

Keep the baseline outside the monitored folder.

## TLS Certificate Inspector

```bash
python tls_certificate_inspector.py example.com
```

Makes one TLS connection to the specified host and port. Use only hosts you are authorized to check.

## Capture real screenshots

Run the commands on your own machine and capture the terminal after the program has produced its output. Do not use invented terminal output as evidence. On Windows, `Win + Shift + S` opens Snipping Tool; on macOS, use `Shift + Command + 4`.
