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
from orch_or.decoherence import TEMPERATURE_SWEEP_FIELDNAMES
from orch_or.decoherence import temperature_sweep_rows
from orch_or.comparison import FIELDNAMES as COMPARISON_FIELDNAMES
from orch_or.comparison import comparison_rows
from orch_or.geometry import DEFAULT_GEOMETRY, FIELDNAMES as GEOMETRY_FIELDNAMES, geometry_sweep_rows
from orch_or.haos_contract import build_summary
from orch_or.hameroff_benchmark import FIELDNAMES as HAMEROFF_FIELDNAMES
from orch_or.hameroff_benchmark import default_time_crystal_rows, default_trp_rows
from orch_or.hameroff_benchmark import hameroff_benchmark_rows
from orch_or.sweep import default_rows, write_rows
from orch_or.thresholds import FIELDNAMES as THRESHOLD_FIELDNAMES
from orch_or.thresholds import threshold_rows
from orch_or.statistics import FIELDNAMES as STATISTICS_FIELDNAMES
from orch_or.statistics import timing_statistics_rows
from orch_or.trp_networks import FIELDNAMES as TRP_FIELDNAMES
from orch_or.time_crystal import FIELDNAMES as TIME_CRYSTAL_FIELDNAMES

EXAMPLES = Path(__file__).resolve().parent
OUTPUT = EXAMPLES / "output"
GENERATED_TABLE = OUTPUT / "collapse_time_table.csv"
GENERATED_THRESHOLDS = OUTPUT / "dp_threshold_table.csv"
GENERATED_DECOHERENCE = OUTPUT / "decoherence_estimate_table.csv"
GENERATED_TEMPERATURE_SWEEP = OUTPUT / "temperature_decoherence_sweep.csv"
GENERATED_ANESTHESIA = OUTPUT / "anesthesia_prediction_table.csv"
GENERATED_GEOMETRY = OUTPUT / "microtubule_geometry_sweep.csv"
GENERATED_COMPARISON = OUTPUT / "or_decoherence_comparison.csv"
GENERATED_STATISTICS = OUTPUT / "timing_statistics_table.csv"
GENERATED_TIME_CRYSTAL = OUTPUT / "time_crystal_multiscale.csv"
GENERATED_TRP = OUTPUT / "trp_superradiance_table.csv"
GENERATED_HAMEROFF = OUTPUT / "hameroff_benchmark.csv"
GENERATED_SUMMARY = OUTPUT / "haos_or_summary.json"
EXPECTED_TABLE = EXAMPLES / "expected_collapse_time_table.csv"
EXPECTED_THRESHOLDS = EXAMPLES / "expected_dp_threshold_table.csv"
EXPECTED_DECOHERENCE = EXAMPLES / "expected_decoherence_estimate_table.csv"
EXPECTED_TEMPERATURE_SWEEP = EXAMPLES / "expected_temperature_decoherence_sweep.csv"
EXPECTED_ANESTHESIA = EXAMPLES / "expected_anesthesia_prediction_table.csv"
EXPECTED_GEOMETRY = EXAMPLES / "expected_microtubule_geometry_sweep.csv"
EXPECTED_COMPARISON = EXAMPLES / "expected_or_decoherence_comparison.csv"
EXPECTED_STATISTICS = EXAMPLES / "expected_timing_statistics_table.csv"
EXPECTED_TIME_CRYSTAL = EXAMPLES / "expected_time_crystal_multiscale.csv"
EXPECTED_TRP = EXAMPLES / "expected_trp_superradiance_table.csv"
EXPECTED_HAMEROFF = EXAMPLES / "expected_hameroff_benchmark.csv"
EXPECTED_SUMMARY = EXAMPLES / "expected_haos_or_summary.json"


def compare_exact(path: Path, expected_path: Path) -> bool:
    return path.read_text(encoding="utf-8") == expected_path.read_text(encoding="utf-8")


def main() -> int:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    rows = default_rows()
    write_rows(GENERATED_TABLE, rows)
    dp_rows = threshold_rows()
    decoherence_estimates = decoherence_rows()
    temperature_sweep = temperature_sweep_rows()
    anesthesia_predictions = anesthesia_prediction_rows()
    geometry_rows = geometry_sweep_rows(
        geometry=DEFAULT_GEOMETRY,
        protofilament_count_grid=(1, 2, 3),
        coherent_dimers_grid=(1, 13, 130, 1300, 10_000),
        coherence_fraction_grid=(1.0, 0.5, 0.1),
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
    comparison = comparison_rows()
    statistics_rows = timing_statistics_rows(
        baseline_tau_s=2.5e-2,
        source_ids=(
            "diosi_2021_collapse_rate",
            "hagan_2000_decoherence_reply",
            "tegmark_2000_decoherence",
        ),
        scenario="deterministic_timing_sampler",
        count=9,
        spread=0.25,
    )
    time_crystal_rows = default_time_crystal_rows()
    trp_rows = default_trp_rows()
    hameroff_benchmark = hameroff_benchmark_rows(
        time_crystal_rows=time_crystal_rows,
        trp_rows=trp_rows,
        anesthesia_rows=anesthesia_predictions,
    )
    write_rows(GENERATED_THRESHOLDS, dp_rows, THRESHOLD_FIELDNAMES)
    write_rows(GENERATED_DECOHERENCE, decoherence_estimates, DECOHERENCE_FIELDNAMES)
    write_rows(GENERATED_TEMPERATURE_SWEEP, temperature_sweep, TEMPERATURE_SWEEP_FIELDNAMES)
    write_rows(GENERATED_ANESTHESIA, anesthesia_predictions, ANESTHESIA_FIELDNAMES)
    write_rows(GENERATED_GEOMETRY, geometry_rows, GEOMETRY_FIELDNAMES)
    write_rows(GENERATED_COMPARISON, comparison, COMPARISON_FIELDNAMES)
    write_rows(GENERATED_STATISTICS, statistics_rows, STATISTICS_FIELDNAMES)
    write_rows(GENERATED_TIME_CRYSTAL, time_crystal_rows, TIME_CRYSTAL_FIELDNAMES)
    write_rows(GENERATED_TRP, trp_rows, TRP_FIELDNAMES)
    write_rows(GENERATED_HAMEROFF, hameroff_benchmark, HAMEROFF_FIELDNAMES)

    summary = build_summary(rows)
    summary["generated_at_utc"] = "FROZEN"
    summary["artifact_tables"] = {
        "collapse_time_table": GENERATED_TABLE.name,
        "dp_threshold_table": GENERATED_THRESHOLDS.name,
        "decoherence_estimate_table": GENERATED_DECOHERENCE.name,
        "anesthesia_prediction_table": GENERATED_ANESTHESIA.name,
        "geometry_sweep_table": GENERATED_GEOMETRY.name,
        "or_decoherence_comparison_table": GENERATED_COMPARISON.name,
        "timing_statistics_table": GENERATED_STATISTICS.name,
        "time_crystal_multiscale_table": GENERATED_TIME_CRYSTAL.name,
        "trp_superradiance_table": GENERATED_TRP.name,
        "hameroff_benchmark_table": GENERATED_HAMEROFF.name,
    }
    summary["dp_threshold_rows"] = len(dp_rows)
    summary["decoherence_rows"] = len(decoherence_estimates)
    summary["temperature_sweep_rows"] = len(temperature_sweep)
    summary["anesthesia_prediction_rows"] = len(anesthesia_predictions)
    summary["geometry_sweep_rows"] = len(geometry_rows)
    summary["or_decoherence_comparison_rows"] = len(comparison)
    summary["timing_statistics_rows"] = len(statistics_rows)
    summary["time_crystal_rows"] = len(time_crystal_rows)
    summary["trp_rows"] = len(trp_rows)
    summary["hameroff_benchmark_rows"] = len(hameroff_benchmark)
    summary["coherence_fraction_grid"] = [1.0, 0.5, 0.1]
    summary["protofilament_count_grid"] = [1, 2, 3]
    summary["timing_statistics_spread"] = 0.25
    GENERATED_SUMMARY.write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")

    table_matches = compare_exact(GENERATED_TABLE, EXPECTED_TABLE)
    thresholds_match = compare_exact(GENERATED_THRESHOLDS, EXPECTED_THRESHOLDS)
    decoherence_matches = compare_exact(GENERATED_DECOHERENCE, EXPECTED_DECOHERENCE)
    temperature_sweep_matches = compare_exact(GENERATED_TEMPERATURE_SWEEP, EXPECTED_TEMPERATURE_SWEEP)
    anesthesia_matches = compare_exact(GENERATED_ANESTHESIA, EXPECTED_ANESTHESIA)
    geometry_matches = compare_exact(GENERATED_GEOMETRY, EXPECTED_GEOMETRY)
    comparison_matches = compare_exact(GENERATED_COMPARISON, EXPECTED_COMPARISON)
    statistics_matches = compare_exact(GENERATED_STATISTICS, EXPECTED_STATISTICS)
    time_crystal_matches = compare_exact(GENERATED_TIME_CRYSTAL, EXPECTED_TIME_CRYSTAL)
    trp_matches = compare_exact(GENERATED_TRP, EXPECTED_TRP)
    hameroff_matches = compare_exact(GENERATED_HAMEROFF, EXPECTED_HAMEROFF)
    summary_matches = compare_exact(GENERATED_SUMMARY, EXPECTED_SUMMARY)
    if (
        not table_matches
        or not thresholds_match
        or not decoherence_matches
        or not temperature_sweep_matches
        or not anesthesia_matches
        or not geometry_matches
        or not comparison_matches
        or not statistics_matches
        or not time_crystal_matches
        or not trp_matches
        or not hameroff_matches
        or not summary_matches
    ):
        raise SystemExit(
            "Frozen baseline mismatch.\n"
            f"table_matches={table_matches}\n"
            f"thresholds_match={thresholds_match}\n"
            f"decoherence_matches={decoherence_matches}\n"
            f"temperature_sweep_matches={temperature_sweep_matches}\n"
            f"anesthesia_matches={anesthesia_matches}\n"
            f"geometry_matches={geometry_matches}\n"
            f"comparison_matches={comparison_matches}\n"
            f"statistics_matches={statistics_matches}\n"
            f"time_crystal_matches={time_crystal_matches}\n"
            f"trp_matches={trp_matches}\n"
            f"hameroff_matches={hameroff_matches}\n"
            f"summary_matches={summary_matches}\n"
            f"generated_table={GENERATED_TABLE}\n"
            f"generated_thresholds={GENERATED_THRESHOLDS}\n"
            f"generated_decoherence={GENERATED_DECOHERENCE}\n"
            f"generated_anesthesia={GENERATED_ANESTHESIA}\n"
            f"generated_geometry={GENERATED_GEOMETRY}\n"
            f"generated_comparison={GENERATED_COMPARISON}\n"
            f"generated_statistics={GENERATED_STATISTICS}\n"
            f"generated_hameroff={GENERATED_HAMEROFF}\n"
            f"generated_summary={GENERATED_SUMMARY}"
        )

    print("Orch-OR diagnostic spine passed.")
    print(f"Table: {GENERATED_TABLE}")
    print(f"DP thresholds: {GENERATED_THRESHOLDS}")
    print(f"Decoherence estimates: {GENERATED_DECOHERENCE}")
    print(f"Temperature sweep: {GENERATED_TEMPERATURE_SWEEP}")
    print(f"Anesthesia predictions: {GENERATED_ANESTHESIA}")
    print(f"Geometry sweep: {GENERATED_GEOMETRY}")
    print(f"OR/decoherence comparison: {GENERATED_COMPARISON}")
    print(f"Timing statistics: {GENERATED_STATISTICS}")
    print(f"Time crystal sweep: {GENERATED_TIME_CRYSTAL}")
    print(f"Trp sweep: {GENERATED_TRP}")
    print(f"Hameroff benchmark: {GENERATED_HAMEROFF}")
    print(f"Summary: {GENERATED_SUMMARY}")
    print(
        "Statement: tau=hbar/E_G timing diagnostics, DP threshold sensitivity, "
        "decoherence windows, geometry sweeps, OR/decoherence comparison, timing statistics, anesthesia perturbation predictions, "
        "and Hameroff-facing benchmark summaries reproduce. "
        "No biological, consciousness, or ontology claim is introduced."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
