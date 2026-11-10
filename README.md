# Cybersecurity Projects

A collection of defensive security utilities and a machine-learning study of network intrusion detection.

## Projects

| Project | Purpose |
|---|---|
| [Password Security Analyzer](password-security-analyzer/) | Provides basic password-strength feedback and local password generation. |
| [Web Security Header Checker](web-security-header-checker/) | Reviews common HTTP security headers and cookie attributes for a specified URL. |
| [Authentication Log Analyzer](authentication-log-analyzer/) | Analyses CSV authentication logs and identifies repeated failed sign-ins. |
| [Network Traffic Anomaly Detector](network-traffic-anomaly-detector/) | Flags unusual patterns in exported network-flow records. |
| [Phishing URL Risk Analyzer](phishing-url-risk-analyzer/) | Evaluates URL characteristics without opening the submitted link. |
| [File Integrity Monitor](file-integrity-monitor/) | Uses SHA-256 hashes to identify added, changed, or removed files. |
| [TLS Certificate Inspector](tls-certificate-inspector/) | Reports details from a verified TLS connection to a specified host. |
| [ML-Based Network Intrusion Detection](research/ml-network-intrusion-detection/) | Compares Logistic Regression and Random Forest using the UNSW-NB15 benchmark. |

## Project screenshots

The screenshots show outputs from local runs. The log and flow tools use the included synthetic CSV records. HTTP and TLS checks use temporary local test servers. The URL analyser works offline.

### Password Security Analyzer
![Password Security Analyzer](docs/screenshots/01-password-security-analyzer.png)

### Web Security Header Checker
![Web Security Header Checker](docs/screenshots/02-web-security-header-checker.png)

### Authentication Log Analyzer
![Authentication Log Analyzer](docs/screenshots/03-authentication-log-analyzer.png)

### Network Traffic Anomaly Detector
![Network Traffic Anomaly Detector](docs/screenshots/04-network-traffic-anomaly-detector.png)

### Phishing URL Risk Analyzer
![Phishing URL Risk Analyzer](docs/screenshots/05-phishing-url-risk-analyzer.png)

### File Integrity Monitor
![File Integrity Monitor](docs/screenshots/06-file-integrity-monitor.png)

### TLS Certificate Inspector
![TLS Certificate Inspector](docs/screenshots/07-tls-certificate-inspector.png)

## Network intrusion detection research

The research study evaluates binary normal-versus-attack classification on the supplied UNSW-NB15 training and testing files. It includes dataset provenance, train-only preprocessing, baseline metrics, a stratified three-fold cross-validation on the training split, and post-hoc attack-category error analysis.

- [Research project overview](research/ml-network-intrusion-detection/README.md)
- [Experimental protocol](research/ml-network-intrusion-detection/research/experiment_protocol.md)
- [Initial results analysis](research/ml-network-intrusion-detection/research/results_analysis.md)
- [Cross-validation and error analysis](research/ml-network-intrusion-detection/research/robustness_and_error_analysis.md)
- [External validation plan](research/ml-network-intrusion-detection/research/external_validation_plan.md)

The initial Random Forest baseline performed better on most aggregate metrics in the supplied test split and training-only cross-validation. Fuzzers had the lowest category-specific recall for both models and remain a priority for further analysis. These findings are benchmark-specific; external validation has not yet been completed.

## Run locally

Python 3.10 or newer is recommended.

```bash
git clone https://github.com/NAYEM00000/-cybersecurity-project-portfolio.git
cd -cybersecurity-project-portfolio
python -m pip install -r requirements.txt
```

Each project has its own README with setup and usage instructions.

## Tests

```bash
python -m unittest discover -s tests -v
python -m compileall -q .
```

GitHub Actions runs automated checks for changes in the repository.

## Scope and responsible use

These tools are intended for learning and authorised defensive security checks. They are not substitutes for professional security assessments. Do not test systems, URLs, or networks without permission.

The intrusion-detection results describe one benchmark dataset and its supplied split. They do not establish production readiness or performance on live networks.

## License

MIT. See [LICENSE](LICENSE).
