from __future__ import annotations

import csv
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class ComparisonTests(unittest.TestCase):
    def test_comparison_artifact_generated(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/quick_reproduce.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("OR/decoherence comparison", result.stdout)
        output = ROOT / "examples" / "output" / "or_decoherence_comparison.csv"
        with output.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["comparison"] == "geometry_vs_decoherence" for row in rows))
        self.assertTrue(all(row["or_favorable"] == "no" for row in rows))


if __name__ == "__main__":
    unittest.main()
