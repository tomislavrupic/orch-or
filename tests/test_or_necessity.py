from __future__ import annotations

import csv
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ORNecessityTests(unittest.TestCase):
    def test_or_off_artifact_generated(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/or_off_comparison.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Wrote", result.stdout)
        output = ROOT / "examples" / "output" / "or_off_comparison.csv"
        with output.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["or_off_status"] == "no_or_collapse_window" for row in rows))
        self.assertTrue(all(row["or_on_status"] == "finite_collapse_window" for row in rows))


if __name__ == "__main__":
    unittest.main()
