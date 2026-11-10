# Phishing URL Risk Analyzer

Checks a few URL characteristics and returns an explainable risk score. It does not visit the URL.

```bash
python phishing_analyzer.py "http://login-example.test/verify?account=1"
```

The score is a heuristic, not a reputation lookup or a verdict that a link is malicious. Do not click suspicious links to test them.
