"""Diosi-Penrose threshold tables for tubulin-scale sensitivity checks."""

from __future__ import annotations

import math

from orch_or.collapse import dp_gaussian_self_energy_excess_j, required_self_energy_j
from orch_or.parameters import DEFAULT_DP_MASS_MODELS, TARGET_COLLAPSE_TIMES_S, DPMassModel
from orch_or.sweep import format_float

FIELDNAMES = [
    "mass_model",
    "scope",
    "mass_kg",
    "superposition_separation_m",
    "smearing_radius_m",
    "unit_dp_energy_j",
    "target_tau_s",
    "required_energy_j",
    "required_coherent_units",
    "source_ids",
    "note",
]


def required_units_for_target(model: DPMassModel, target_tau_s: float) -> float:
    unit_energy = dp_gaussian_self_energy_excess_j(
        model.mass_kg,
        model.superposition_separation_m,
        model.smearing_radius_m,
    )
    return required_self_energy_j(target_tau_s) / unit_energy


def threshold_rows(
    models: tuple[DPMassModel, ...] = DEFAULT_DP_MASS_MODELS,
    target_times_s: tuple[float, ...] = TARGET_COLLAPSE_TIMES_S,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for model in models:
        unit_energy = dp_gaussian_self_energy_excess_j(
            model.mass_kg,
            model.superposition_separation_m,
            model.smearing_radius_m,
        )
        for target_tau_s in target_times_s:
            required_energy = required_self_energy_j(target_tau_s)
            required_units = required_energy / unit_energy
            rows.append(
                {
                    "mass_model": model.name,
                    "scope": model.scope,
                    "mass_kg": format_float(model.mass_kg),
                    "superposition_separation_m": format_float(model.superposition_separation_m),
                    "smearing_radius_m": format_float(model.smearing_radius_m),
                    "unit_dp_energy_j": format_float(unit_energy),
                    "target_tau_s": format_float(target_tau_s),
                    "required_energy_j": format_float(required_energy),
                    "required_coherent_units": f"{required_units:.6e}",
                    "source_ids": ";".join(model.source_ids),
                    "note": model.note,
                }
            )
    return rows


def nearest_target_row(target_tau_s: float = 2.5e-2, model_name: str = "tubulin_dimer_angstrom_smear") -> dict[str, str]:
    for row in threshold_rows():
        if row["mass_model"] == model_name and math.isclose(float(row["target_tau_s"]), target_tau_s):
            return row
    raise ValueError(f"No threshold row for model={model_name!r}, tau={target_tau_s!r}")
