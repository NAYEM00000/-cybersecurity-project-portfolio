# Project Demo Guide

Run commands from each project's folder. Use only systems and data you own or are authorized to assess.

## Password Security Analyzer

```bash
cd password-security-analyzer
python password_analyzer.py
```

Choose local password analysis or random password generation. The entered password is hidden and is not stored or transmitted.

## Web Security Header Checker

```bash
python -m pip install -r ../requirements.txt
python header_checker.py https://example.com --json report.json
```

Sends one ordinary GET request. Only check URLs you are authorized to assess.

## Authentication Log Analyzer

```bash
python log_analyzer.py sample_auth.csv --threshold 5
```

CSV columns: `timestamp,username,source_ip,status`. The included sample data is synthetic.

## Network Traffic Anomaly Detector

```bash
python traffic_detector.py sample_flows.csv --ports-threshold 5 --bytes-threshold 10000000
```

CSV columns: `timestamp,src_ip,dst_ip,dst_port,bytes,protocol`. This tool analyzes exported flow data; it does not capture packets.

## Phishing URL Risk Analyzer

```bash
python phishing_analyzer.py "http://login-example.test/verify?account=1"
```

The URL is parsed locally and is never opened. Scores are heuristic indicators, not definitive verdicts.

## Run tests

From the repository root:

```bash
python -m unittest discover -s tests -v
```

These are command-line tools, not graphical applications. Add screenshots only after capturing genuine local runs; do not present illustrative output as real execution evidence.
