import getpass
import math
import secrets
import string


MIN_LENGTH = 12
MAX_LENGTH = 128
COMMON_PASSWORDS = {"password", "123456", "qwerty", "admin", "letmein"}


def analyze(password: str) -> dict:
    """Return a simple, local estimate of password strength.

    The entropy value assumes characters are chosen randomly from the detected
    character groups. Real passwords often are not random, so treat the score
    as guidance rather than a security guarantee.
    """
    if not isinstance(password, str):
        raise TypeError("password must be a string")

    pool_size = 0
    groups = (
        (string.ascii_lowercase, "Add lowercase letters."),
        (string.ascii_uppercase, "Add uppercase letters."),
        (string.digits, "Add numbers."),
        (string.punctuation, "Add symbols."),
    )
    issues = []

    for characters, message in groups:
        if any(char in characters for char in password):
            pool_size += len(characters)
        else:
            issues.append(message)

    if len(password) < MIN_LENGTH:
        issues.insert(0, f"Use at least {MIN_LENGTH} characters.")

    if password.lower() in COMMON_PASSWORDS:
        issues.append("This is a commonly used password.")

    entropy = len(password) * math.log2(pool_size) if pool_size else 0.0
    score = min(100, int(entropy * 1.6))
    if score < 35:
        label = "Weak"
    elif score < 60:
        label = "Moderate"
    elif score < 80:
        label = "Strong"
    else:
        label = "Very strong"

    return {
        "score": score,
        "label": label,
        "estimated_entropy_bits": round(entropy, 1),
        "issues": issues,
    }


def generate(length: int = 20) -> str:
    """Generate a password with all four character groups using secrets."""
    if not isinstance(length, int) or isinstance(length, bool):
        raise TypeError("length must be an integer")
    if not MIN_LENGTH <= length <= MAX_LENGTH:
        raise ValueError(
            f"length must be between {MIN_LENGTH} and {MAX_LENGTH}"
        )

    alphabet = string.ascii_letters + string.digits + string.punctuation
    while True:
        password = "".join(secrets.choice(alphabet) for _ in range(length))
        if (
            any(char.islower() for char in password)
            and any(char.isupper() for char in password)
            and any(char.isdigit() for char in password)
            and any(char in string.punctuation for char in password)
        ):
            return password


if __name__ == "__main__":
    print("Password Security Analyzer")
    choice = input("[1] Check a password  [2] Generate a password: ").strip()

    if choice == "2":
        try:
            requested_length = int(input("Length (12-128): "))
            print("Generated password:", generate(requested_length))
        except ValueError as error:
            print(f"Error: {error}")
    else:
        entered_password = getpass.getpass("Password (input is hidden): ")
        result = analyze(entered_password)
        print(f"\nEstimate: {result['label']} ({result['score']}/100)")
        print(f"Estimated entropy: {result['estimated_entropy_bits']} bits")
        for issue in result["issues"]:
            print("-", issue)
        if not result["issues"]:
            print("No basic composition issues found.")
