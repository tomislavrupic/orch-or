from __future__ import annotations

import unittest

from orch_or.reduction import default_reduction_scenarios, reduction_distinction_rows


class ReductionDistinctionTests(unittest.TestCase):
    def test_distinction_rows_cover_required_axes(self) -> None:
        rows = reduction_distinction_rows(default_reduction_scenarios())
        self.assertEqual(len(rows), 2)
        first = rows[0]
        self.assertIn("source_locked_proxy", first)
        self.assertIn("or_on_output", first)
        self.assertIn("or_off_counterfactual", first)
        self.assertIn("non_or_quantum_alternative", first)
        self.assertIn("classical_alternative", first)
        self.assertIn("observable_neural_correlate", first)
        self.assertIn("observable_behavioral_correlate", first)
        self.assertIn("actual_falsifier", first)


if __name__ == "__main__":
    unittest.main()
