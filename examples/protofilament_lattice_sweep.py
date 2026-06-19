#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.geometry import DEFAULT_GEOMETRY, LATTICE_FIELDNAMES, protofilament_lattice_sweep_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "protofilament_lattice_sweep.csv"
EXPECTED = EXAMPLES / "expected_protofilament_lattice_sweep.csv"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=LATTICE_FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = protofilament_lattice_sweep_rows(
        geometry=DEFAULT_GEOMETRY,
        protofilament_count_grid=(11, 13, 15),
        dimers_per_protofilament_grid=(1, 4, 8),
        coherence_fraction_grid=(1.0, 0.5),
        separation_grid_m=(1.0e-10, 1.0e-9, 1.0e-8),
        source_ids=(
            "microtubule_structure_nogales_1998",
            "microtubule_lattice_nogales_1999",
            "tubulin_atomic_lowe_2001",
        ),
        assumption_label="primary_lattice_proxy",
    )
    write_rows(GENERATED, rows)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
