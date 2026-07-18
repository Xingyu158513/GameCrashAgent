import unittest

from gamecrashagent.privacy import Redactor, redact_data


class PrivacyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.redactor = Redactor(username="Alice", computer_name="DESKTOP-SECRET")

    def test_redacts_common_identifiers(self) -> None:
        source = (
            r"C:\Users\Alice\Desktop\case.txt on DESKTOP-SECRET "
            "from 203.0.113.42 using 00-11-22-33-44-55"
        )
        result = self.redactor.text(source)
        self.assertNotIn("Alice", result)
        self.assertNotIn("DESKTOP-SECRET", result)
        self.assertNotIn("203.0.113.42", result)
        self.assertNotIn("00-11-22-33-44-55", result)
        self.assertIn(r"C:\Users\[REDACTED]", result)
        self.assertIn("[REDACTED-HOST]", result)
        self.assertIn("[REDACTED-IP]", result)
        self.assertIn("[REDACTED-MAC]", result)

    def test_redacts_nested_values_without_mutating_source(self) -> None:
        source = {"events": {"items": [{"Message": "Alice at 192.0.2.10"}]}}
        result = redact_data(source, self.redactor)
        self.assertEqual(source["events"]["items"][0]["Message"], "Alice at 192.0.2.10")
        self.assertNotIn("Alice", result["events"]["items"][0]["Message"])
        self.assertTrue(result["privacy"]["redacted"])

    def test_redacts_common_ipv6_forms(self) -> None:
        source = (
            "global 2001:db8::1, link-local [fe80::abcd%12]:443, "
            "mapped ::ffff:192.0.2.128."
        )
        result = self.redactor.text(source)
        self.assertNotIn("2001:db8::1", result)
        self.assertNotIn("fe80::abcd%12", result)
        self.assertNotIn("::ffff:192.0.2.128", result)
        self.assertEqual(result.count("[REDACTED-IP]"), 3)
        self.assertIn("[REDACTED-IP].", result)

    def test_does_not_redact_non_ip_colon_text(self) -> None:
        source = "Event time 12:34:56, ratio 1:2:3, and path C:\\Windows\\System32"
        self.assertEqual(self.redactor.text(source), source)


if __name__ == "__main__":
    unittest.main()
