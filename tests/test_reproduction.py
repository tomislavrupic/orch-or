from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "examples") not in sys.path:
    sys.path.insert(0, str(ROOT / "examples"))

import quick_reproduce


class ReproductionTests(unittest.TestCase):
    def test_quick_reproduce_baselines(self) -> None:
        self.assertEqual(quick_reproduce.main(), 0)

    def test_expected_summary_is_bounded(self) -> None:
        summary = json.loads((ROOT / "examples" / "expected_haos_or_summary.json").read_text(encoding="utf-8"))
        self.assertIn("toy rows are not biological", summary["claim_boundary"])


if __name__ == "__main__":
    unittest.main()
