import json
import unittest

from gamecrashagent.privacy import Redactor, redact_data
from gamecrashagent.reporting import build_json_report, build_markdown_report


class ReportingTests(unittest.TestCase):
    def test_reports_are_valid_and_do_not_reintroduce_identifiers(self) -> None:
        data = {
            "minidumps": {"directory": r"C:\Users\Alice\Dumps", "items": [], "errors": []},
            "events": {
                "log_name": "System",
                "hours": 6,
                "items": [{"Id": 41, "ProviderName": "Kernel-Power", "Message": "Alice 203.0.113.7 2001:db8::7"}],
                "errors": [],
            },
            "network_adapters": {"items": [], "errors": []},
            "drivers": {"items": [], "errors": []},
            "risk": {"level": "medium", "summary": "Evidence requires review.", "signals": [], "recommendations": []},
        }
        safe = redact_data(data, Redactor(username="Alice", computer_name="HOST-A"))
        markdown = build_markdown_report(safe)
        json_text = build_json_report(safe)
        json.loads(json_text)
        self.assertIn("Initial Risk Assessment", markdown)
        self.assertNotIn("Alice", markdown)
        self.assertNotIn("203.0.113.7", markdown)
        self.assertNotIn("2001:db8::7", markdown)
        self.assertNotIn("Alice", json_text)
        self.assertNotIn("2001:db8::7", json_text)


if __name__ == "__main__":
    unittest.main()
