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
from orch_or.trp_networks import FIELDNAMES, tryptophan_network_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "trp_superradiance_table.csv"
EXPECTED = EXAMPLES / "expected_trp_superradiance_table.csv"


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = tryptophan_network_rows(
        network_sizes=(10, 100, 1_000, 10_000, 100_000),
        disorders=(0.0, 0.1, 0.5, 1.0),
        source_ids=(
            "tryptophan_superradiance_2024",
            "photoprotection_architectures_2024",
            "superradiant_excitonic_states_2018",
        ),
        note="Diagnostic tryptophan superradiance sweep; not a consciousness claim.",
        anesthetic_strength=0.3,
    )
    write_rows(GENERATED, rows, FIELDNAMES)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
