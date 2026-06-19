"""Deterministic sweep helpers for Orch-OR diagnostics."""

from __future__ import annotations

import csv
from pathlib import Path
from typing import Iterable

from orch_or.collapse import (
    collapse_time_s,
    timing_margin_log10,
    timing_status,
    total_self_energy_j,
)
from orch_or.parameters import DEFAULT_PARAMETER_SETS, ParameterSet

FIELDNAMES = [
    "parameter_set",
    "scope",
    "coherent_units",
    "unit_self_energy_j",
    "coupling",
    "total_self_energy_j",
    "collapse_time_s",
    "decoherence_time_s",
    "timing_margin_log10",
    "status",
]


def format_float(value: float) -> str:
    return f"{value:.6e}"


def format_margin(value: float) -> str:
    return f"{value:.6f}"


def evaluate_parameter_set(parameter_set: ParameterSet) -> dict[str, str]:
    total_energy = total_self_energy_j(
        parameter_set.unit_self_energy_j,
        parameter_set.coherent_units,
        parameter_set.coupling,
    )
    tau = collapse_time_s(total_energy)
    margin = timing_margin_log10(tau, parameter_set.decoherence_time_s)
    return {
        "parameter_set": parameter_set.name,
        "scope": parameter_set.scope,
        "coherent_units": str(parameter_set.coherent_units),
        "unit_self_energy_j": format_float(parameter_set.unit_self_energy_j),
        "coupling": format_float(parameter_set.coupling),
        "total_self_energy_j": format_float(total_energy),
        "collapse_time_s": format_float(tau),
        "decoherence_time_s": format_float(parameter_set.decoherence_time_s),
        "timing_margin_log10": format_margin(margin),
        "status": timing_status(tau, parameter_set.decoherence_time_s),
    }


def default_rows() -> list[dict[str, str]]:
    return [evaluate_parameter_set(parameter_set) for parameter_set in DEFAULT_PARAMETER_SETS]


def write_rows(
    path: Path,
    rows: Iterable[dict[str, str]],
    fieldnames: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames or FIELDNAMES, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
