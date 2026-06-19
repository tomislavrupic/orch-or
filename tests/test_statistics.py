from __future__ import annotations

import csv
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class StatisticsTests(unittest.TestCase):
    def test_timing_statistics_artifact_generated(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/quick_reproduce.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Timing statistics", result.stdout)
        output = ROOT / "examples" / "output" / "timing_statistics_table.csv"
        with output.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 9)
        self.assertEqual(rows[4]["sampled_status"], "slower")
        self.assertEqual(rows[0]["sampled_status"], "faster")


if __name__ == "__main__":
    unittest.main()
