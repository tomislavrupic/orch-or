from __future__ import annotations

import math
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from orch_or.collapse import (
    collapse_time_s,
    dp_gaussian_self_energy_excess_j,
    dp_point_mass_far_field_self_energy_j,
    required_self_energy_j,
    timing_margin_log10,
    timing_status,
    total_self_energy_j,
)
from orch_or.constants import HBAR_J_S


class CollapseTests(unittest.TestCase):
    def test_collapse_time_inverse(self) -> None:
        tau = 0.025
        energy = required_self_energy_j(tau)
        self.assertTrue(math.isclose(collapse_time_s(energy), tau, rel_tol=1.0e-12))

    def test_total_self_energy_linear_toy_model(self) -> None:
        self.assertAlmostEqual(total_self_energy_j(1.0e-34, 1_000, 2.0), 2.0e-31)

    def test_dp_gaussian_energy_is_positive_and_regulated(self) -> None:
        energy = dp_gaussian_self_energy_excess_j(1.0e-22, 1.0e-10, 1.0e-10)
        self.assertGreater(energy, 0.0)
        far_field = dp_point_mass_far_field_self_energy_j(1.0e-22, 1.0e-6)
        self.assertGreater(far_field, 0.0)

    def test_timing_status_boundary(self) -> None:
        tau = HBAR_J_S / 1.0e-26
        self.assertGreater(timing_margin_log10(tau, 1.0e-6), 0.0)
        self.assertEqual(timing_status(tau, 1.0e-6), "or_window_open")
        self.assertEqual(timing_status(1.0e-3, 1.0e-6), "decoherence_preempts_or")

    def test_invalid_self_energy_rejected(self) -> None:
        for bad_value in (0.0, -1.0):
            with self.subTest(bad_value=bad_value):
                with self.assertRaises(ValueError):
                    collapse_time_s(bad_value)


if __name__ == "__main__":
    unittest.main()
