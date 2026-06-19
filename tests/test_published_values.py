from __future__ import annotations

from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]


class PublishedValuesTests(unittest.TestCase):
    def test_published_values_note_exists_and_is_linked(self) -> None:
        text = (ROOT / "docs" / "published_values.md").read_text(encoding="utf-8")
        self.assertIn("Tegmark decoherence", text)
        self.assertIn("Hagan/Hameroff/Tuszynski reply", text)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("docs/published_values.md", readme)


if __name__ == "__main__":
    unittest.main()
