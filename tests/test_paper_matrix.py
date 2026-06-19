from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PaperMatrixTests(unittest.TestCase):
    def test_paper_matrix_mentions_primary_sources(self) -> None:
        text = (ROOT / "docs" / "paper_matrix.md").read_text(encoding="utf-8")
        self.assertIn("Tegmark 2000", text)
        self.assertIn("Hagan, Hameroff, Tuszynski 2000", text)
        self.assertIn("Diósi 2021", text)
        self.assertIn("Kalra et al. 2022", text)
        self.assertIn("Babcock et al. 2023", text)

    def test_paper_matrix_keeps_supported_and_unproven_separate(self) -> None:
        text = (ROOT / "docs" / "paper_matrix.md").read_text(encoding="utf-8")
        self.assertIn("supported_microphysics", text)
        self.assertIn("unproven_interpretation", text)
        self.assertIn("supported_structure", text)
        self.assertIn("supported_network_biology", text)

    def test_discriminating_tests_exist(self) -> None:
        text = (ROOT / "docs" / "discriminating_tests.md").read_text(encoding="utf-8")
        self.assertIn("Orch-OR prediction", text)
        self.assertIn("Classical neurobiology prediction", text)


if __name__ == "__main__":
    unittest.main()
