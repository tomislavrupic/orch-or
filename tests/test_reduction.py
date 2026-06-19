from __future__ import annotations

import unittest

from orch_or.reduction import (
    default_reduction_scenarios,
    collective_superposition,
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
        self.assertIn("superposition_label", row)
        self.assertIn("state_alpha", row["alternative_set"])
        self.assertIn("gamma_link_hz", row)
        self.assertIn("classical_model_state", row)
        self.assertIn("novel_distinction", row)
        self.assertIn("predicted_timing_correlate", row)

    def test_collective_superposition_wraps_scenario(self) -> None:
        scenario = default_reduction_scenarios()[0]
        superposition = collective_superposition(scenario, selection_pressure=1.25)
        self.assertEqual(superposition.scenario, scenario)
        self.assertGreater(superposition.selection_pressure, 1.0)

    def test_sweep_rows_change_with_noise(self) -> None:
        rows = reduction_sweep_rows(default_reduction_scenarios())
        self.assertGreater(len(rows), 0)
        self.assertTrue(all(row["selected_state"] for row in rows))
        self.assertTrue(any(row["selection_margin_log10"].startswith("-") for row in rows))
        self.assertTrue(all(row["classical_model_state"] for row in rows))
        self.assertTrue(all(row["superposition_label"] for row in rows))
        self.assertTrue(any("classical" in row["novel_distinction"] for row in rows))


if __name__ == "__main__":
    unittest.main()
