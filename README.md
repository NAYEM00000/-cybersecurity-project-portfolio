# Cybersecurity Project Portfolio

A beginner-to-intermediate defensive cybersecurity portfolio containing five practical Python projects.

## Projects

| Project | Purpose | Main features |
|---|---|---|
| Password Security Analyzer | Assess password quality locally | Strength checks, entropy estimate, secure password generation |
| Web Security Header Checker | Review a website's HTTP security posture | HTTPS check, security headers, cookie flags, JSON report |
| Authentication Log Analyzer | Detect suspicious login patterns in logs | Failed-login aggregation, brute-force indicators, CSV report |
| Network Traffic Anomaly Detector | Analyze exported flow records | Port-scan and traffic-volume heuristics from CSV |
| Phishing URL Risk Analyzer | Flag suspicious URL characteristics | Explainable heuristic score, safe offline analysis |

## Requirements

- Python 3.10+
- Install optional dependencies with `pip install -r requirements.txt`
- Run each project from its own directory. See its README.

## Responsible use

These tools are intended for systems and data you own or are explicitly authorized to assess. The web checker sends a single ordinary HTTP GET request to the URL you provide. The traffic detector analyzes CSV data; it does not sniff networks or intercept traffic. The phishing analyzer does not visit submitted URLs.

## Repository structure

```text
cybersecurity-project-portfolio/
├── password-security-analyzer/
├── web-security-header-checker/
├── authentication-log-analyzer/
├── network-traffic-anomaly-detector/
├── phishing-url-risk-analyzer/
├── README.md
├── LICENSE
└── .gitignore
```

## Disclaimer

Detection results are heuristic and can produce false positives or false negatives. They are educational aids, not substitutes for professional security testing, endpoint protection, SIEM, or incident response.
