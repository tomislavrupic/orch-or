from __future__ import annotations

import unittest

from orch_or.data import registry


class DataRegistryTests(unittest.TestCase):
    def test_registry_validate(self) -> None:
        registry.validate()

    def test_geometry_rows_have_source_short(self) -> None:
        rows = registry.load_tubulin_geometry()
        self.assertTrue(all("source_short" in row for row in rows))
        self.assertTrue(any(row["source_short"] == "Nogales et al. 1999" for row in rows))

    def test_primary_structure_rows_are_loaded(self) -> None:
        rows = registry.load_primary_structure()
        self.assertEqual(len(rows), 5)
        self.assertTrue(all("source_short" in row for row in rows))
        self.assertTrue(any(row["source_short"] == "Lowe et al. 2001" for row in rows))


if __name__ == "__main__":
    unittest.main()
