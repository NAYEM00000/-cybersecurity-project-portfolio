import argparse, json
from urllib.parse import urlparse
import requests

HEADERS = {
    "strict-transport-security": "Encourages HTTPS-only connections.",
    "content-security-policy": "Restricts permitted content sources.",
    "x-content-type-options": "Helps prevent MIME-sniffing.",
    "x-frame-options": "Helps mitigate clickjacking.",
    "referrer-policy": "Controls referrer information.",
    "permissions-policy": "Restricts browser features."
}

def inspect(url):
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Provide a complete http:// or https:// URL.")
    response = requests.get(url, timeout=10, allow_redirects=True,
                            headers={"User-Agent": "DefensiveHeaderChecker/1.0"})
    found = {k.lower(): v for k, v in response.headers.items()}
    checks = {name: {"present": name in found, "purpose": purpose,
                     "value": found.get(name)} for name, purpose in HEADERS.items()}
    cookies = response.headers.get("Set-Cookie", "")
    return {
        "requested_url": url, "final_url": response.url,
        "status_code": response.status_code,
        "https": urlparse(response.url).scheme == "https",
        "security_headers": checks,
        "cookie_flags": {
            "secure": "secure" in cookies.lower(),
            "httponly": "httponly" in cookies.lower(),
            "samesite": "samesite" in cookies.lower()
        } if cookies else None
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Check common HTTP security headers.")
    parser.add_argument("url")
    parser.add_argument("--json", dest="output")
    args = parser.parse_args()
    try:
        result = inspect(args.url)
        print(json.dumps(result, indent=2))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as f: json.dump(result, f, indent=2)
    except (ValueError, requests.RequestException) as exc:
        raise SystemExit(f"Error: {exc}")
