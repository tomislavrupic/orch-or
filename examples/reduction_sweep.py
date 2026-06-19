#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.reduction import SWEEP_FIELDNAMES, default_reduction_scenarios, reduction_sweep_rows
from orch_or.sweep import write_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "reduction_sweep.csv"
EXPECTED = EXAMPLES / "expected_reduction_sweep.csv"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = reduction_sweep_rows(default_reduction_scenarios())
    write_rows(GENERATED, rows, SWEEP_FIELDNAMES)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
