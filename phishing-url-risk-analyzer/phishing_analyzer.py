import argparse
import ipaddress
from urllib.parse import urlparse


SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "ow.ly"}
SUSPICIOUS_WORDS = {
    "login", "verify", "account", "secure",
    "update", "password", "wallet", "confirm",
}


def _is_shortener(host: str) -> bool:
    return any(
        host == domain or host.endswith("." + domain)
        for domain in SHORTENERS
    )


def analyze(url: str) -> dict:
    """Score a few URL warning signs without making a network request."""
    if not isinstance(url, str) or not url.strip():
        raise ValueError("Provide a non-empty URL.")

    url = url.strip()
    if any(character.isspace() for character in url):
        raise ValueError("The URL must not contain whitespace.")

    candidate = url if "://" in url else "http://" + url
    parsed = urlparse(candidate)
    if parsed.scheme.lower() not in {"http", "https"} or not parsed.hostname:
        raise ValueError("Provide a valid http:// or https:// URL.")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError("The URL contains user information before the host.")
    try:
        parsed.port
    except ValueError as error:
        raise ValueError("The URL contains an invalid port.") from error

    host = parsed.hostname.lower().rstrip(".")
    reasons = []
    score = 0

    if parsed.scheme.lower() != "https":
        score += 15
        reasons.append("The URL does not use HTTPS.")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        score += 25
        reasons.append("The host is an IP address rather than a domain.")

    if _is_shortener(host):
        score += 20
        reasons.append("The URL uses a known shortening service.")
    if len(url) > 100:
        score += 10
        reasons.append("The URL is unusually long.")
    if host.count("-") >= 2:
        score += 10
        reasons.append("The domain contains several hyphens.")

    matched_words = sorted(
        word
        for word in SUSPICIOUS_WORDS
        if word in (host + parsed.path + parsed.query).lower()
    )
    if matched_words:
        score += min(20, 5 * len(matched_words))
        reasons.append(
            "Sensitive-action words appear in the URL: "
            + ", ".join(matched_words)
        )

    score = min(score, 100)
    if score < 25:
        risk_level = "Low"
    elif score < 50:
        risk_level = "Medium"
    else:
        risk_level = "High"

    return {
        "url": url,
        "risk_score": score,
        "risk_level": risk_level,
        "reasons": reasons,
    }


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Check URL warning signs offline; the URL is not opened."
    )
    parser.add_argument("url")
    args = parser.parse_args()

    try:
        print(analyze(args.url))
    except ValueError as error:
        raise SystemExit(f"Error: {error}")
