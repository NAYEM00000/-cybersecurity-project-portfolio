import math
import secrets
import string
import getpass

def analyze(password: str) -> dict:
    pool = 0
    if any(c.islower() for c in password): pool += 26
    if any(c.isupper() for c in password): pool += 26
    if any(c.isdigit() for c in password): pool += 10
    if any(c in string.punctuation for c in password): pool += len(string.punctuation)
    entropy = len(password) * math.log2(pool) if pool else 0
    issues = []
    if len(password) < 12: issues.append("Use at least 12 characters.")
    if not any(c.islower() for c in password): issues.append("Add lowercase letters.")
    if not any(c.isupper() for c in password): issues.append("Add uppercase letters.")
    if not any(c.isdigit() for c in password): issues.append("Add numbers.")
    if not any(c in string.punctuation for c in password): issues.append("Add symbols.")
    common = {"password", "123456", "qwerty", "admin", "letmein"}
    if password.lower() in common: issues.append("This is a commonly used password.")
    score = min(100, int(entropy * 1.6))
    label = "Weak" if score < 35 else "Moderate" if score < 60 else "Strong" if score < 80 else "Very strong"
    return {"score": score, "label": label, "estimated_entropy_bits": round(entropy, 1), "issues": issues}

def generate(length=20):
    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        value = "".join(secrets.choice(alphabet) for _ in range(length))
        if (any(c.islower() for c in value) and any(c.isupper() for c in value)
            and any(c.isdigit() for c in value) and any(c in string.punctuation for c in value)):
            return value

if __name__ == "__main__":
    print("Password Security Analyzer (local-only)")
    choice = input("[1] Analyze password  [2] Generate password: ").strip()
    if choice == "2":
        try: length = max(12, min(128, int(input("Length (12-128): "))))
        except ValueError: length = 20
        print("Generated password:", generate(length))
    else:
        pwd = getpass.getpass("Enter password (hidden; not stored): ")
        result = analyze(pwd)
        print(f"\nResult: {result['label']} ({result['score']}/100)")
        print("Estimated entropy:", result["estimated_entropy_bits"], "bits")
        for issue in result["issues"]: print("-", issue)
        if not result["issues"]: print("No basic composition issues detected.")
