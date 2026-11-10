import importlib.util
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


password = load_module("password_analyzer", "password-security-analyzer/password_analyzer.py")
header = load_module("header_checker", "web-security-header-checker/header_checker.py")
auth = load_module("log_analyzer", "authentication-log-analyzer/log_analyzer.py")
traffic = load_module("traffic_detector", "network-traffic-anomaly-detector/traffic_detector.py")
phishing = load_module("phishing_analyzer", "phishing-url-risk-analyzer/phishing_analyzer.py")


class PasswordTests(unittest.TestCase):
    def test_short_password_reports_length_issue(self):
        self.assertIn("Use at least 12 characters.", password.analyze("abc")["issues"])

    def test_generated_password_has_required_classes(self):
        import string
        value = password.generate(24)
        self.assertEqual(len(value), 24)
        self.assertTrue(any(c.islower() for c in value))
        self.assertTrue(any(c.isupper() for c in value))
        self.assertTrue(any(c.isdigit() for c in value))
        self.assertTrue(any(c in string.punctuation for c in value))


class HeaderTests(unittest.TestCase):
    def test_rejects_invalid_scheme_before_network_request(self):
        with patch.object(header.requests, "get") as request:
            with self.assertRaises(ValueError):
                header.inspect("file:///etc/passwd")
            request.assert_not_called()

    def test_reads_security_headers_and_cookie_flags(self):
        response = SimpleNamespace(
            url="https://example.test/",
            status_code=200,
            headers={
                "Content-Security-Policy": "default-src 'self'",
                "Set-Cookie": "sid=abc; Secure; HttpOnly; SameSite=Lax",
            },
        )
        with patch.object(header.requests, "get", return_value=response):
            result = header.inspect("https://example.test/")
        self.assertTrue(result["security_headers"]["content-security-policy"]["present"])
        self.assertEqual(result["cookie_flags"], {
            "secure": True, "httponly": True, "samesite": True
        })


class CsvAnalyzerTests(unittest.TestCase):
    def test_authentication_failures_are_counted(self):
        data = (
            "timestamp,username,source_ip,status\n"
            "2026-01-01T00:00:00Z,alice,192.0.2.10,failed\n"
            "2026-01-01T00:00:01Z,alice,192.0.2.10,failed\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "auth.csv"
            path.write_text(data, encoding="utf-8")
            result = auth.analyze(path, 2)
        self.assertEqual(result["failed_by_ip"]["192.0.2.10"], 2)
        self.assertEqual(len(result["alerts"]), 2)

    def test_flow_analyzer_flags_ports_and_bytes(self):
        data = (
            "timestamp,src_ip,dst_ip,dst_port,bytes,protocol\n"
            "2026-01-01T00:00:00Z,192.0.2.20,192.0.2.1,22,70,TCP\n"
            "2026-01-01T00:00:01Z,192.0.2.20,192.0.2.1,80,70,TCP\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "flows.csv"
            path.write_text(data, encoding="utf-8")
            alerts = traffic.analyze(path, 2, 100)
        self.assertEqual({a["type"] for a in alerts}, {
            "many_distinct_destination_ports", "high_total_bytes"
        })


class PhishingTests(unittest.TestCase):
    def test_https_normal_url_scores_low(self):
        result = phishing.analyze("https://example.com/")
        self.assertEqual(result["risk_level"], "Low")
        self.assertEqual(result["risk_score"], 0)

    def test_suspicious_url_scores_high(self):
        result = phishing.analyze("http://192.0.2.8/login/verify")
        self.assertEqual(result["risk_level"], "High")

if __name__ == "__main__":
    unittest.main()
