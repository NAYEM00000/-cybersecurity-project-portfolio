import importlib.util
import tempfile
import unittest
from datetime import datetime, timedelta, timezone
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]


def load_module(name, relative_path):
    spec = importlib.util.spec_from_file_location(name, ROOT / relative_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


password = load_module(
    "password_analyzer", "password-security-analyzer/password_analyzer.py"
)
header = load_module(
    "header_checker", "web-security-header-checker/header_checker.py"
)
auth = load_module(
    "log_analyzer", "authentication-log-analyzer/log_analyzer.py"
)
traffic = load_module(
    "traffic_detector", "network-traffic-anomaly-detector/traffic_detector.py"
)
phishing = load_module(
    "phishing_analyzer", "phishing-url-risk-analyzer/phishing_analyzer.py"
)
integrity = load_module(
    "file_integrity_monitor", "file-integrity-monitor/file_integrity_monitor.py"
)
tls_inspector = load_module(
    "tls_certificate_inspector",
    "tls-certificate-inspector/tls_certificate_inspector.py",
)


class PasswordTests(unittest.TestCase):
    def test_short_password_gets_length_warning(self):
        self.assertIn(
            "Use at least 12 characters.",
            password.analyze("abc")["issues"],
        )

    def test_generator_uses_all_character_groups(self):
        import string

        generated = password.generate(24)
        self.assertEqual(len(generated), 24)
        self.assertTrue(any(char.islower() for char in generated))
        self.assertTrue(any(char.isupper() for char in generated))
        self.assertTrue(any(char.isdigit() for char in generated))
        self.assertTrue(any(char in string.punctuation for char in generated))

    def test_generator_rejects_out_of_range_length(self):
        with self.assertRaises(ValueError):
            password.generate(8)


class HeaderCheckerTests(unittest.TestCase):
    def test_rejects_non_http_scheme_without_request(self):
        with patch.object(header.requests, "get") as request:
            with self.assertRaises(ValueError):
                header.inspect("file:///etc/passwd")
            request.assert_not_called()

    def test_cookie_flags_require_exact_attributes_on_every_cookie(self):
        class RawHeaders:
            @staticmethod
            def getlist(name):
                return [
                    "session=abc; Secure; HttpOnly; SameSite=Lax",
                    "theme=dark; HttpOnly",
                ]

        response = SimpleNamespace(
            headers={},
            raw=SimpleNamespace(headers=RawHeaders()),
        )
        cookies = header._get_set_cookie_headers(response)
        self.assertEqual(len(cookies), 2)
        self.assertEqual(
            header._cookie_flags(cookies),
            {"secure": False, "httponly": True, "samesite": False},
        )


class AuthenticationLogTests(unittest.TestCase):
    def test_counts_failed_logins(self):
        data = (
            "timestamp,username,source_ip,status\n"
            "2026-01-01T00:00:00Z,alice,192.0.2.10,failed\n"
            "2026-01-01T00:00:01Z,alice,192.0.2.10,failed\n"
            "2026-01-01T00:00:02Z,bob,198.51.100.8,success\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "auth.csv"
            path.write_text(data, encoding="utf-8")
            result = auth.analyze(path, threshold=2)
        self.assertEqual(result["failed_by_ip"]["192.0.2.10"], 2)
        self.assertEqual(len(result["alerts"]), 2)

    def test_rejects_zero_threshold(self):
        with self.assertRaises(ValueError):
            auth.analyze("unused.csv", threshold=0)


class TrafficAnalyzerTests(unittest.TestCase):
    def test_flags_many_ports_and_high_byte_total(self):
        data = (
            "timestamp,src_ip,dst_ip,dst_port,bytes,protocol\n"
            "2026-01-01T00:00:00Z,192.0.2.20,192.0.2.1,22,70,TCP\n"
            "2026-01-01T00:00:01Z,192.0.2.20,192.0.2.1,80,70,TCP\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "flows.csv"
            path.write_text(data, encoding="utf-8")
            alerts = traffic.analyze(path, ports_threshold=2, bytes_threshold=100)
        self.assertEqual(
            {item["type"] for item in alerts},
            {"many_distinct_destination_ports", "high_total_bytes"},
        )

    def test_rejects_negative_bytes(self):
        data = (
            "timestamp,src_ip,dst_ip,dst_port,bytes,protocol\n"
            "2026-01-01T00:00:00Z,192.0.2.20,192.0.2.1,22,-1,TCP\n"
        )
        with tempfile.TemporaryDirectory() as folder:
            path = Path(folder) / "flows.csv"
            path.write_text(data, encoding="utf-8")
            with self.assertRaises(ValueError):
                traffic.analyze(path)


class PhishingAnalyzerTests(unittest.TestCase):
    def test_normal_https_url_has_low_score(self):
        result = phishing.analyze("https://example.com/")
        self.assertEqual(result["risk_level"], "Low")
        self.assertEqual(result["risk_score"], 0)

    def test_ip_and_sensitive_words_raise_score(self):
        result = phishing.analyze("http://192.0.2.8/login/verify")
        self.assertEqual(result["risk_level"], "High")

    def test_rejects_unsupported_scheme(self):
        with self.assertRaises(ValueError):
            phishing.analyze("ftp://example.com/file")


class FileIntegrityTests(unittest.TestCase):
    def test_reports_added_modified_and_removed_files(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "watched"
            root.mkdir()
            manifest = Path(folder) / "baseline.json"
            (root / "keep.txt").write_text("original", encoding="utf-8")
            (root / "remove.txt").write_text("old", encoding="utf-8")
            integrity.create_baseline(root, manifest)

            (root / "keep.txt").write_text("changed", encoding="utf-8")
            (root / "remove.txt").unlink()
            (root / "new.txt").write_text("new file", encoding="utf-8")

            changes = integrity.compare_with_baseline(root, manifest)

        self.assertEqual(changes["added"], ["new.txt"])
        self.assertEqual(changes["modified"], ["keep.txt"])
        self.assertEqual(changes["removed"], ["remove.txt"])

    def test_manifest_must_be_outside_watched_directory(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder) / "watched"
            root.mkdir()
            with self.assertRaises(ValueError):
                integrity.create_baseline(root, root / "baseline.json")


class TLSInspectorTests(unittest.TestCase):
    def test_summarizes_certificate_expiry(self):
        now = datetime(2026, 1, 1, tzinfo=timezone.utc)
        expires = now + timedelta(days=20)
        certificate = {
            "subject": ((("commonName", "example.com"),),),
            "issuer": ((("commonName", "Example CA"),),),
            "subjectAltName": (("DNS", "example.com"),),
            "notBefore": "Jan  1 00:00:00 2025 GMT",
            "notAfter": expires.strftime("%b %d %H:%M:%S %Y GMT"),
        }
        result = tls_inspector.summarize_certificate(
            certificate,
            "example.com",
            443,
            "TLSv1.3",
            ("TLS_AES_256_GCM_SHA384", "TLSv1.3", 256),
            now=now,
        )
        self.assertEqual(result["expiry_status"], "expires_within_30_days")
        self.assertEqual(result["days_remaining"], 20)
        self.assertTrue(result["certificate_verified"])

    def test_rejects_invalid_port_before_connecting(self):
        with patch.object(tls_inspector.socket, "create_connection") as connect:
            with self.assertRaises(ValueError):
                tls_inspector.inspect_certificate("example.com", port=70000)
            connect.assert_not_called()


if __name__ == "__main__":
    unittest.main()
