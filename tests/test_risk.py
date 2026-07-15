import unittest

from gamecrashagent.risk import analyze_risk


class RiskTests(unittest.TestCase):
    def test_high_when_crash_and_both_driver_stacks_exist(self) -> None:
        data = {
            "events": {
                "items": [
                    {"Id": 1001, "ProviderName": "Microsoft-Windows-WER-SystemErrorReporting"},
                    {"Id": 41, "ProviderName": "Microsoft-Windows-Kernel-Power"},
                ]
            },
            "drivers": {
                "items": [
                    {"path": r"C:\Windows\System32\drivers\ACE-BASE.sys", "exists": True},
                    {"path": r"C:\Windows\System32\drivers\rtwlane.sys", "exists": True},
                ]
            },
            "network_adapters": {"items": []},
        }
        result = analyze_risk(data)
        self.assertEqual(result["level"], "high")
        self.assertGreaterEqual(len(result["signals"]), 4)

    def test_low_without_crash_signal(self) -> None:
        result = analyze_risk(
            {
                "events": {"items": []},
                "drivers": {"items": []},
                "network_adapters": {"items": []},
            }
        )
        self.assertEqual(result["level"], "low")


if __name__ == "__main__":
    unittest.main()
