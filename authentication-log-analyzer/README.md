# Authentication Log Analyzer

Analyzes a simple CSV export of authentication events and highlights repeated failed logins.

## CSV format
`timestamp,username,source_ip,status`

Status should be `success` or `failed`.

## Run
```bash
python log_analyzer.py sample_auth.csv --threshold 5
```

Use only logs you are authorized to access. The sample data is synthetic.
