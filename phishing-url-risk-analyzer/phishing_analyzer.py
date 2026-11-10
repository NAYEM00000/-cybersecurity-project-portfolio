import argparse, ipaddress
from urllib.parse import urlparse

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "is.gd", "ow.ly"}
SUSPICIOUS_WORDS = {"login", "verify", "account", "secure", "update", "password", "wallet", "confirm"}

def analyze(url):
    parsed = urlparse(url if "://" in url else "http://" + url)
    host = (parsed.hostname or "").lower()
    reasons, score = [], 0
    if parsed.scheme != "https":
        score += 15; reasons.append("URL does not use HTTPS")
    if "@" in parsed.netloc:
        score += 25; reasons.append("Contains @ in authority section")
    try:
        ipaddress.ip_address(host)
        score += 25; reasons.append("Uses an IP address instead of a domain")
    except ValueError:
        pass
    if host in SHORTENERS:
        score += 20; reasons.append("Uses a known URL shortener")
    if len(url) > 100:
        score += 10; reasons.append("Unusually long URL")
    if host.count("-") >= 2:
        score += 10; reasons.append("Domain contains multiple hyphens")
    matches = sorted(w for w in SUSPICIOUS_WORDS if w in (host + parsed.path + parsed.query).lower())
    if matches:
        score += min(20, 5 * len(matches)); reasons.append("Sensitive-action words: " + ", ".join(matches))
    score = min(100, score)
    label = "Low" if score < 25 else "Medium" if score < 50 else "High"
    return {"url": url, "risk_score": score, "risk_level": label, "reasons": reasons}

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Offline phishing URL heuristic; does not visit URLs.")
    p.add_argument("url")
    a = p.parse_args()
    print(analyze(a.url))
