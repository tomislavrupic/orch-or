from __future__ import annotations

import unittest

from orch_or.reduction import (
    default_reduction_scenarios,
    reduction_event_row,
    reduction_sweep_rows,
    select_state,
)


class ReductionTests(unittest.TestCase):
    def test_select_state_is_deterministic(self) -> None:
        scenario = default_reduction_scenarios()[0]
        selected = select_state(scenario.alternatives, selection_pressure=1.0)
        self.assertEqual(selected.label, "state_beta")

    def test_event_row_contains_discrete_choice(self) -> None:
        row = reduction_event_row(default_reduction_scenarios()[0])
        self.assertEqual(row["selected_state"], "state_beta")
        self.assertGreater(float(row["collapse_time_s"]), 0.0)
        self.assertIn("state_alpha", row["alternative_set"])
        self.assertIn("gamma_link_hz", row)
        self.assertIn("classical_model_state", row)
        self.assertIn("novel_distinction", row)
        self.assertIn("predicted_timing_correlate", row)

    def test_sweep_rows_change_with_noise(self) -> None:
        rows = reduction_sweep_rows(default_reduction_scenarios())
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["selected_state"] for row in rows))
        self.assertTrue(any(row["selection_margin_log10"].startswith("-") for row in rows))
        self.assertTrue(all(row["classical_model_state"] for row in rows))
        self.assertTrue(any("classical" in row["novel_distinction"] for row in rows))


if __name__ == "__main__":
    unittest.main()
