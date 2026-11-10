import argparse
import json
from urllib.parse import urlparse

import requests


SECURITY_HEADERS = {
    "strict-transport-security": "Encourages HTTPS-only connections.",
    "content-security-policy": "Restricts permitted content sources.",
    "x-content-type-options": "Helps prevent MIME sniffing.",
    "x-frame-options": "Helps reduce clickjacking risk.",
    "referrer-policy": "Controls referrer information.",
    "permissions-policy": "Restricts browser features.",
}


def _get_set_cookie_headers(response) -> list[str]:
    """Return individual Set-Cookie values when the HTTP library exposes them."""
    raw_headers = getattr(getattr(response, "raw", None), "headers", None)
    getlist = getattr(raw_headers, "getlist", None)
    if callable(getlist):
        values = getlist("Set-Cookie")
        if values:
            return list(values)

    value = response.headers.get("Set-Cookie")
    return [value] if value else []


def _cookie_flags(cookie_headers: list[str]) -> dict | None:
    if not cookie_headers:
        return None

    attributes_by_cookie = []
    for cookie in cookie_headers:
        attributes = set()
        for part in cookie.split(";")[1:]:
            name = part.strip().partition("=")[0].lower()
            if name:
                attributes.add(name)
        attributes_by_cookie.append(attributes)

    # True means every cookie in the response has that attribute.
    return {
        flag: all(flag in attributes for attributes in attributes_by_cookie)
        for flag in ("secure", "httponly", "samesite")
    }


def inspect(url: str) -> dict:
    """Fetch one URL and report common response security headers."""
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Provide a complete http:// or https:// URL.")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("Do not include credentials in the URL.")
    try:
        parsed.port
    except ValueError as error:
        raise ValueError("The URL contains an invalid port.") from error

    response = requests.get(
        url,
        timeout=10,
        allow_redirects=True,
        headers={"User-Agent": "HeaderChecker/1.0"},
    )

    response_headers = {
        name.lower(): value for name, value in response.headers.items()
    }
    checks = {
        name: {
            "present": name in response_headers,
            "purpose": purpose,
            "value": response_headers.get(name),
        }
        for name, purpose in SECURITY_HEADERS.items()
    }

    return {
        "requested_url": url,
        "final_url": response.url,
        "status_code": response.status_code,
        "https": urlparse(response.url).scheme == "https",
        "security_headers": checks,
        "cookie_count": len(_get_set_cookie_headers(response)),
        "cookie_flags": _cookie_flags(_get_set_cookie_headers(response)),
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check common HTTP response security headers."
    )
    parser.add_argument("url")
    parser.add_argument("--json", dest="output")
    args = parser.parse_args()

    try:
        report = inspect(args.url)
        print(json.dumps(report, indent=2))
        if args.output:
            with open(args.output, "w", encoding="utf-8") as output_file:
                json.dump(report, output_file, indent=2)
    except (ValueError, requests.RequestException) as error:
        raise SystemExit(f"Error: {error}")
