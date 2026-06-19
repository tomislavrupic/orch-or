from __future__ import annotations

import unittest

from orch_or.time_crystal import (
    OscillatorMode,
    beat_frequency_hz,
    collapse_trigger_probability,
    coherence_envelope_s,
    floquet_like_response,
    multiscale_oscillation_rows,
)


class TimeCrystalTests(unittest.TestCase):
    def test_beat_frequency(self) -> None:
        a = OscillatorMode("kHz", 1.0e3, 1.0)
        b = OscillatorMode("MHz", 1.0e6, 1.0)
        self.assertEqual(beat_frequency_hz(a, b), 999000.0)

    def test_coherence_envelope(self) -> None:
        mode = OscillatorMode("THz", 1.0e12, 1.0, damping=2.0)
        self.assertAlmostEqual(coherence_envelope_s(mode), 0.5)

    def test_floquet_like_response_is_bounded(self) -> None:
        response = floquet_like_response(60.0, 62.0, coupling=0.8, coherence_time_s=0.5)
        self.assertGreater(response, 0.0)
        self.assertLessEqual(response, 0.8)

    def test_collapse_trigger_probability_bounded(self) -> None:
        mode = OscillatorMode("gamma", 4.0e1, 0.9, phase_rad=1.2, damping=0.1)
        p = collapse_trigger_probability(mode)
        self.assertGreaterEqual(p, 0.0)
        self.assertLessEqual(p, 1.0)

    def test_multiscale_rows(self) -> None:
        modes = (
            OscillatorMode("kHz", 1.0e3, 1.0),
            OscillatorMode("MHz", 1.0e6, 0.8, damping=0.2),
            OscillatorMode("GHz", 1.0e9, 0.5, phase_rad=0.4, damping=0.5),
        )
        rows = multiscale_oscillation_rows(
            modes,
            source_ids=("hameroff_time_crystal_2026", "bandyopadhyay_multiscale_resonance"),
            note="diagnostic time-crystal sweep",
        )
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0]["mode_label"], "kHz")
        self.assertIn("hameroff_time_crystal_2026", rows[0]["source_ids"])


if __name__ == "__main__":
    unittest.main()
