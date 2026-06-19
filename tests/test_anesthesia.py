from __future__ import annotations

import csv
import subprocess
import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


class AnesthesiaTests(unittest.TestCase):
    def test_frequency_fields_and_counterfactual_trace(self) -> None:
        result = subprocess.run(
            [sys.executable, "examples/quick_reproduce.py"],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            check=True,
        )
        self.assertIn("Anesthesia predictions", result.stdout)
        output = ROOT / "examples" / "output" / "anesthesia_prediction_table.csv"
        with output.open("r", encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        self.assertGreater(len(rows), 0)
        self.assertTrue(all("frequency_hz" in row for row in rows))
        self.assertTrue(all("frequency_response" in row for row in rows))
        stabilizer = next(row for row in rows if row["perturbation"] == "microtubule_stabilizer_counterfactual")
        self.assertIn("microtubule_energy_transport_kalra_2022", stabilizer["source_ids"])
        self.assertEqual(stabilizer["frequency_hz"], "2.000000e+01")


if __name__ == "__main__":
    unittest.main()
