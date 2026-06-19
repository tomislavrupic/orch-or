#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.sweep import write_rows
from orch_or.time_crystal import FIELDNAMES, OscillatorMode, multiscale_oscillation_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "time_crystal_multiscale.csv"
EXPECTED = EXAMPLES / "expected_time_crystal_multiscale.csv"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    modes = (
        OscillatorMode("kHz", 1.0e3, 1.0, phase_rad=0.0, damping=0.05),
        OscillatorMode("MHz", 1.0e6, 0.8, phase_rad=0.6, damping=0.1),
        OscillatorMode("GHz", 1.0e9, 0.6, phase_rad=1.0, damping=0.25),
        OscillatorMode("THz", 1.0e12, 0.4, phase_rad=1.3, damping=0.5),
    )
    rows = multiscale_oscillation_rows(
        modes,
        source_ids=("hameroff_time_crystal_2026", "bandyopadhyay_multiscale_resonance"),
        note="Diagnostic multiscale oscillation ladder; not a biological proof.",
    )
    write_rows(GENERATED, rows, FIELDNAMES)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
