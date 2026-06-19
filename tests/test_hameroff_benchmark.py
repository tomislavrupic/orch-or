from __future__ import annotations

import unittest

from orch_or.hameroff_benchmark import (
    default_hameroff_benchmark_rows,
    default_time_crystal_rows,
    default_trp_rows,
    hameroff_benchmark_rows,
)


class HameroffBenchmarkTests(unittest.TestCase):
    def test_default_rows_cover_requested_emphases(self) -> None:
        rows = default_hameroff_benchmark_rows()
        emphases = {row["emphasis"] for row in rows}
        self.assertIn("time_crystal_multiscale", emphases)
        self.assertIn("trp_quantum_optics", emphases)
        self.assertIn("anesthesia_disruption", emphases)
        self.assertTrue(all(row["source_ids"] for row in rows))
        self.assertTrue(all("consciousness claim" not in row["diagnostic_metric"] for row in rows))

    def test_volatile_anesthetic_rows_required(self) -> None:
        with self.assertRaises(ValueError):
            hameroff_benchmark_rows(
                time_crystal_rows=default_time_crystal_rows(),
                trp_rows=default_trp_rows(),
                anesthesia_rows=[],
            )


if __name__ == "__main__":
    unittest.main()
