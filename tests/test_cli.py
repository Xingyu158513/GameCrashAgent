import argparse
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from gamecrashagent.cli import run


class CliTests(unittest.TestCase):
    def test_run_writes_both_reports(self) -> None:
        fake_data = {
            "minidumps": {"directory": r"C:\Windows\Minidump", "items": [], "errors": []},
            "events": {"log_name": "System", "hours": 6, "items": [], "errors": []},
            "network_adapters": {"items": [], "errors": []},
            "drivers": {"items": [], "errors": []},
        }
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config = root / "config.json"
            config.write_text("{}", encoding="utf-8")
            args = argparse.Namespace(
                config=config,
                format="both",
                output=root / "report.md",
                json_output=root / "report.json",
                redaction="standard",
            )
            with patch("gamecrashagent.cli.collect_all", return_value=fake_data):
                written = run(args)
            self.assertEqual(len(written), 2)
            self.assertTrue(args.output.exists())
            self.assertTrue(args.json_output.exists())
            json.loads(args.json_output.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
