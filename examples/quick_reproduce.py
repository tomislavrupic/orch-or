#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.anesthesia import FIELDNAMES as ANESTHESIA_FIELDNAMES
from orch_or.anesthesia import anesthesia_prediction_rows
from orch_or.decoherence import FIELDNAMES as DECOHERENCE_FIELDNAMES
from orch_or.decoherence import decoherence_rows
from orch_or.geometry import DEFAULT_GEOMETRY, FIELDNAMES as GEOMETRY_FIELDNAMES, geometry_sweep_rows
from orch_or.haos_contract import build_summary
from orch_or.sweep import default_rows, write_rows
from orch_or.thresholds import FIELDNAMES as THRESHOLD_FIELDNAMES
from orch_or.thresholds import threshold_rows

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED_TABLE = OUTPUT / "collapse_time_table.csv"
GENERATED_THRESHOLDS = OUTPUT / "dp_threshold_table.csv"
GENERATED_DECOHERENCE = OUTPUT / "decoherence_estimate_table.csv"
GENERATED_ANESTHESIA = OUTPUT / "anesthesia_prediction_table.csv"
GENERATED_GEOMETRY = OUTPUT / "microtubule_geometry_sweep.csv"
GENERATED_SUMMARY = OUTPUT / "haos_or_summary.json"
EXPECTED_TABLE = EXAMPLES / "expected_collapse_time_table.csv"
EXPECTED_THRESHOLDS = EXAMPLES / "expected_dp_threshold_table.csv"
EXPECTED_DECOHERENCE = EXAMPLES / "expected_decoherence_estimate_table.csv"
EXPECTED_ANESTHESIA = EXAMPLES / "expected_anesthesia_prediction_table.csv"
EXPECTED_GEOMETRY = EXAMPLES / "expected_microtubule_geometry_sweep.csv"
EXPECTED_SUMMARY = EXAMPLES / "expected_haos_or_summary.json"


def compare_exact(path: Path, expected_path: Path) -> bool:
    return path.read_text(encoding="utf-8") == expected_path.read_text(encoding="utf-8")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = default_rows()
    write_rows(GENERATED_TABLE, rows)
    dp_rows = threshold_rows()
    decoherence_estimates = decoherence_rows()
    anesthesia_predictions = anesthesia_prediction_rows()
    geometry_rows = geometry_sweep_rows(
        geometry=DEFAULT_GEOMETRY,
        coherent_dimers_grid=(1, 13, 130, 1300, 10_000),
        separation_grid_m=(1.0e-10, 1.0e-9, 1.0e-8),
        smearing_radius_m=1.0e-9,
        eg_model="gaussian",
        source_ids=(
            "diosi_2021_collapse_rate",
            "microtubule_structure_nogales_1998",
            "microtubule_lattice_nogales_1999",
            "tubulin_atomic_lowe_2001",
        ),
        assumption_label="primary_trace_candidate",
    )
    write_rows(GENERATED_THRESHOLDS, dp_rows, THRESHOLD_FIELDNAMES)
    write_rows(GENERATED_DECOHERENCE, decoherence_estimates, DECOHERENCE_FIELDNAMES)
    write_rows(GENERATED_ANESTHESIA, anesthesia_predictions, ANESTHESIA_FIELDNAMES)
    write_rows(GENERATED_GEOMETRY, geometry_rows, GEOMETRY_FIELDNAMES)

    summary = build_summary(rows)
    summary["generated_at_utc"] = "FROZEN"
    summary["artifact_tables"] = {
        "collapse_time_table": GENERATED_TABLE.name,
        "dp_threshold_table": GENERATED_THRESHOLDS.name,
        "decoherence_estimate_table": GENERATED_DECOHERENCE.name,
        "anesthesia_prediction_table": GENERATED_ANESTHESIA.name,
    }
    summary["dp_threshold_rows"] = len(dp_rows)
    summary["decoherence_rows"] = len(decoherence_estimates)
    summary["anesthesia_prediction_rows"] = len(anesthesia_predictions)
    summary["geometry_sweep_rows"] = len(geometry_rows)
    GENERATED_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    table_matches = compare_exact(GENERATED_TABLE, EXPECTED_TABLE)
    thresholds_match = compare_exact(GENERATED_THRESHOLDS, EXPECTED_THRESHOLDS)
    decoherence_matches = compare_exact(GENERATED_DECOHERENCE, EXPECTED_DECOHERENCE)
    anesthesia_matches = compare_exact(GENERATED_ANESTHESIA, EXPECTED_ANESTHESIA)
    geometry_matches = compare_exact(GENERATED_GEOMETRY, EXPECTED_GEOMETRY)
    summary_matches = compare_exact(GENERATED_SUMMARY, EXPECTED_SUMMARY)
    if (
        not table_matches
        or not thresholds_match
        or not decoherence_matches
        or not anesthesia_matches
        or not geometry_matches
        or not summary_matches
    ):
        raise SystemExit(
            "Frozen baseline mismatch.\n"
            f"table_matches={table_matches}\n"
            f"thresholds_match={thresholds_match}\n"
            f"decoherence_matches={decoherence_matches}\n"
            f"anesthesia_matches={anesthesia_matches}\n"
            f"geometry_matches={geometry_matches}\n"
            f"summary_matches={summary_matches}\n"
            f"generated_table={GENERATED_TABLE}\n"
            f"generated_thresholds={GENERATED_THRESHOLDS}\n"
            f"generated_decoherence={GENERATED_DECOHERENCE}\n"
            f"generated_anesthesia={GENERATED_ANESTHESIA}\n"
            f"generated_geometry={GENERATED_GEOMETRY}\n"
            f"generated_summary={GENERATED_SUMMARY}"
        )

    print("Orch-OR diagnostic spine passed.")
    print(f"Table: {GENERATED_TABLE}")
    print(f"DP thresholds: {GENERATED_THRESHOLDS}")
    print(f"Decoherence estimates: {GENERATED_DECOHERENCE}")
    print(f"Anesthesia predictions: {GENERATED_ANESTHESIA}")
    print(f"Geometry sweep: {GENERATED_GEOMETRY}")
    print(f"Summary: {GENERATED_SUMMARY}")
    print(
        "Statement: tau=hbar/E_G timing diagnostics, DP threshold sensitivity, "
        "decoherence windows, geometry sweeps, and anesthesia perturbation predictions reproduce. "
        "No biological, consciousness, or ontology claim is introduced."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
