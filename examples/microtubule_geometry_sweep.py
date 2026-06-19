#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.geometry import DEFAULT_GEOMETRY, FIELDNAMES, geometry_sweep_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED = OUTPUT / "microtubule_geometry_sweep.csv"
EXPECTED = EXAMPLES / "expected_microtubule_geometry_sweep.csv"


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDNAMES)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    source_ids = (
        "diosi_2021_collapse_rate",
        "microtubule_structure_nogales_1998",
        "microtubule_lattice_nogales_1999",
        "tubulin_atomic_lowe_2001",
    )
    rows = geometry_sweep_rows(
        geometry=DEFAULT_GEOMETRY,
        protofilament_count_grid=(1, 2, 3),
        coherent_dimers_grid=(1, 13, 130, 1300, 10_000),
        separation_grid_m=(1.0e-10, 1.0e-9, 1.0e-8),
        smearing_radius_m=1.0e-9,
        eg_model="gaussian",
        source_ids=source_ids,
        assumption_label="primary_trace_candidate",
    )
    write_rows(GENERATED, rows)
    if GENERATED.read_text(encoding="utf-8") != EXPECTED.read_text(encoding="utf-8"):
        raise SystemExit(f"Frozen baseline mismatch: {GENERATED} != {EXPECTED}")
    print(f"Wrote {GENERATED}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
