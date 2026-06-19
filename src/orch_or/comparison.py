"""Orch-OR versus decoherence comparison tables."""

from __future__ import annotations

import math

from orch_or.decoherence import DEFAULT_DECOHERENCE_ESTIMATES, representative_time_s
from orch_or.geometry import DEFAULT_GEOMETRY, geometry_sweep_rows

FIELDNAMES = [
    "comparison",
    "coherent_dimers",
    "separation_m",
    "eg_model",
    "eg_j",
    "tau_s",
    "decoherence_estimate",
    "decoherence_s",
    "or_favorable",
    "margin_log10",
    "geometry_source_ids",
    "decoherence_source_ids",
    "note",
]


def comparison_rows() -> list[dict[str, str]]:
    geometry_rows = geometry_sweep_rows(
        geometry=DEFAULT_GEOMETRY,
        coherent_dimers_grid=(13, 130, 1300, 10_000),
        separation_grid_m=(1.0e-9, 1.0e-8),
        smearing_radius_m=1.0e-9,
        eg_model="gaussian",
        source_ids=(
            "diosi_2021_collapse_rate",
            "microtubule_structure_nogales_1998",
            "microtubule_lattice_nogales_1999",
            "tubulin_atomic_lowe_2001",
        ),
        assumption_label="geometry_comparison",
    )
    rows: list[dict[str, str]] = []
    for geometry_row in geometry_rows:
        tau_s = float(geometry_row["tau_s"])
        margin_sources = geometry_row["source_ids"]
        for estimate in DEFAULT_DECOHERENCE_ESTIMATES:
            decoherence_s = representative_time_s(estimate)
            margin = decoherence_s / tau_s
            rows.append(
                {
                    "comparison": "geometry_vs_decoherence",
                    "coherent_dimers": geometry_row["coherent_dimers"],
                    "separation_m": geometry_row["separation_m"],
                    "eg_model": geometry_row["eg_model"],
                    "eg_j": geometry_row["eg_j"],
                    "tau_s": geometry_row["tau_s"],
                    "decoherence_estimate": estimate.name,
                    "decoherence_s": f"{decoherence_s:.6e}",
                    "or_favorable": "yes" if margin >= 1.0 else "no",
                    "margin_log10": f"{math.log10(margin):.6f}",
                    "geometry_source_ids": margin_sources,
                    "decoherence_source_ids": ";".join(estimate.source_ids),
                    "note": estimate.note,
                }
            )
    return rows
