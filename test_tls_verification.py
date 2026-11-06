"""Regression tests for TLS verification in the WAF detector."""

import ast
import unittest
from pathlib import Path


class TLSVerificationTests(unittest.TestCase):
    def test_requests_never_disable_certificate_verification(self):
        source = Path(__file__).with_name("firewall_detector.py").read_text(encoding="utf-8")
        tree = ast.parse(source)
        disabled = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Call):
                for keyword in node.keywords:
                    if (
                        keyword.arg == "verify"
                        and isinstance(keyword.value, ast.Constant)
                        and keyword.value.value is False
                    ):
                        disabled.append(node.lineno)
        self.assertEqual(disabled, [], "TLS certificate verification must remain enabled.")
        self.assertNotIn('url.replace("https://", "http://")', source)


if __name__ == "__main__":
    unittest.main()
