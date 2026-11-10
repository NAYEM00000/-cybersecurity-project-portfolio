# Web Security Header Checker

Checks common HTTP response security headers and cookie flags for a URL you are authorized to assess.

## Install and run
```bash
pip install -r ../requirements.txt
python header_checker.py https://example.com --json report.json
```

Makes one GET request, does not crawl or exploit the target. Network access is required.
