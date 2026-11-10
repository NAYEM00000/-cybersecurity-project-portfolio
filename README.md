# Cybersecurity Project Portfolio

[![Python CI](https://github.com/NAYEM00000/-cybersecurity-project-portfolio/actions/workflows/python-ci.yml/badge.svg)](https://github.com/NAYEM00000/-cybersecurity-project-portfolio/actions/workflows/python-ci.yml)
![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![License](https://img.shields.io/badge/License-MIT-green)
![Focus](https://img.shields.io/badge/Focus-Defensive%20Security-0A7EA4)

A beginner-to-intermediate portfolio of five practical **defensive cybersecurity** tools written in Python.

## Projects

| Project | Purpose | Run from its project folder |
|---|---|---|
| Password Security Analyzer | Local password feedback and secure random password generation | `python password_analyzer.py` |
| Web Security Header Checker | Check HTTP security headers and cookie attributes | `python header_checker.py https://example.com` |
| Authentication Log Analyzer | Identify repeated failed logins in CSV exports | `python log_analyzer.py sample_auth.csv --threshold 5` |
| Network Traffic Anomaly Detector | Flag unusual flow volumes and many destination ports | `python traffic_detector.py sample_flows.csv --ports-threshold 5` |
| Phishing URL Risk Analyzer | Offline URL-risk heuristics; never visits submitted URLs | `python phishing_analyzer.py "http://login-example.test/verify"` |

## Quick start

Requirements: Python 3.10 or newer.

```bash
git clone https://github.com/NAYEM00000/-cybersecurity-project-portfolio.git
cd -cybersecurity-project-portfolio
python -m pip install -r requirements.txt
```

Run each tool from its own directory. The web checker requires `requests`; the other tools use the Python standard library.

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

GitHub Actions runs the tests and compile check on pushes and pull requests.

## Responsible use

Use these tools only on systems, URLs, and data you own or are explicitly authorized to assess. The web checker sends one ordinary GET request; it does not crawl or exploit targets. The traffic detector analyzes CSV exports and does not capture packets. The phishing analyzer is offline and does not open submitted URLs. Passwords entered into the password analyzer are not saved or transmitted.

## Limitations

All detections are heuristic and may produce false positives or false negatives. Entropy estimates are not guarantees; URL scores are not reputation verdicts; traffic thresholds need environment-specific tuning. These educational projects are not substitutes for professional security testing, SIEM, endpoint protection, or incident response.

## License

MIT. See [LICENSE](LICENSE).
