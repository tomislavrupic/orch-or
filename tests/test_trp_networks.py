from __future__ import annotations

import unittest

from orch_or.trp_networks import (
    anesthetic_damping_proxy,
    estimated_quantum_yield,
    subradiant_retention,
    superradiant_gain,
    tryptophan_network_rows,
)


class TrpNetworkTests(unittest.TestCase):
    def test_gain_is_bounded(self) -> None:
        gain = superradiant_gain(10_000, 0.2)
        self.assertGreaterEqual(gain, 0.0)
        self.assertLess(gain, 10.0)

    def test_quantum_yield_is_bounded(self) -> None:
        qy = estimated_quantum_yield(100_000, 0.1)
        self.assertGreaterEqual(qy, 0.124)
        self.assertLessEqual(qy, 1.0)

    def test_retention_is_bounded(self) -> None:
        retention = subradiant_retention(100_000, 0.1)
        self.assertGreaterEqual(retention, 0.0)
        self.assertLessEqual(retention, 1.0)

    def test_damping_increases_with_strength(self) -> None:
        low = anesthetic_damping_proxy(10_000, 0.1, 0.2)
        high = anesthetic_damping_proxy(10_000, 0.5, 0.2)
        self.assertLess(low, high)

    def test_row_generation(self) -> None:
        rows = tryptophan_network_rows(
            network_sizes=(10, 1000),
            disorders=(0.0, 0.5),
            source_ids=("tryptophan_superradiance_2024", "photoprotection_architectures_2024"),
            note="diagnostic trp sweep",
        )
        self.assertEqual(len(rows), 4)
        self.assertIn("tryptophan_superradiance_2024", rows[0]["source_ids"])


if __name__ == "__main__":
    unittest.main()
