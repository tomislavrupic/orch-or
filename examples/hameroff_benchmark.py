#!/usr/bin/env python3
from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.hameroff_benchmark import FIELDNAMES, default_hameroff_benchmark_rows
from orch_or.sweep import write_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "hameroff_benchmark.csv"
EXPECTED = EXAMPLES / "expected_hameroff_benchmark.csv"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = default_hameroff_benchmark_rows()
    write_rows(GENERATED, rows, FIELDNAMES)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
