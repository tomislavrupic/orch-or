from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

from orch_or.lattice import build_cylindrical_lattice, deterministic_edge_drop, edge_retention


class LatticeTests(unittest.TestCase):
    def test_default_lattice_shape(self) -> None:
        lattice = build_cylindrical_lattice()
        self.assertEqual(lattice.nodes, 13 * 8)
        self.assertEqual(len(lattice.edges), (13 * 8) + (13 * 7))

    def test_deterministic_edge_drop_retention(self) -> None:
        lattice = build_cylindrical_lattice(protofilaments=4, rings=4)
        perturbed = deterministic_edge_drop(lattice.edges, 0.25)
        self.assertLess(len(perturbed), len(lattice.edges))
        self.assertAlmostEqual(edge_retention(lattice.edges, perturbed), 0.75)


if __name__ == "__main__":
    unittest.main()
