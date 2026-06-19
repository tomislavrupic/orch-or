from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from orch_or.anesthesia import all_volatile_anesthetics_reduce_margin, anesthesia_prediction_rows
from orch_or.decoherence import decoherence_rows
from orch_or.parameters import DEFAULT_DP_MASS_MODELS
from orch_or.thresholds import required_units_for_target, threshold_rows


class DiagnosticTableTests(unittest.TestCase):
    def test_threshold_rows_cover_all_models(self) -> None:
        rows = threshold_rows()
        self.assertEqual(len(rows), 12)
        self.assertTrue(all(float(row["required_coherent_units"]) > 0.0 for row in rows))

    def test_required_units_decrease_for_shorter_tau(self) -> None:
        slow = required_units_for_target(model=DEFAULT_DP_MASS_MODELS[0], target_tau_s=1.0e-1)
        fast = required_units_for_target(model=DEFAULT_DP_MASS_MODELS[0], target_tau_s=1.0e-3)
        self.assertGreater(fast, slow)

    def test_decoherence_rows_include_critical_and_supportive_ranges(self) -> None:
        rows = decoherence_rows()
        stances = {row["stance"] for row in rows}
        self.assertIn("critical", stances)
        self.assertIn("supportive_contested", stances)

    def test_volatile_anesthesia_predictions_reduce_margin(self) -> None:
        rows = anesthesia_prediction_rows()
        self.assertTrue(all_volatile_anesthetics_reduce_margin(rows))


if __name__ == "__main__":
    unittest.main()
