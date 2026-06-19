"""Anesthesia perturbation predictions for Orch-OR diagnostics."""

from __future__ import annotations

import math

from orch_or.collapse import timing_margin_log10, timing_status
from orch_or.decoherence import representative_time_s
from orch_or.parameters import DEFAULT_ANESTHESIA_PERTURBATIONS, DEFAULT_DECOHERENCE_ESTIMATES
from orch_or.sweep import format_float, format_margin

FIELDNAMES = [
    "perturbation",
    "scope",
    "baseline_tau_s",
    "perturbed_tau_s",
    "baseline_decoherence_s",
    "perturbed_decoherence_s",
    "baseline_margin_log10",
    "perturbed_margin_log10",
    "margin_delta_log10",
    "baseline_status",
    "perturbed_status",
    "predicted_direction",
    "frequency_hz",
    "frequency_response",
    "source_ids",
    "note",
]


def anesthesia_prediction_rows(
    baseline_tau_s: float = 2.5e-2,
    decoherence_estimate_name: str = "hagan_actin_gel_extension",
) -> list[dict[str, str]]:
    estimate = next(
        item for item in DEFAULT_DECOHERENCE_ESTIMATES if item.name == decoherence_estimate_name
    )
    baseline_decoherence_s = representative_time_s(estimate)
    baseline_margin = timing_margin_log10(baseline_tau_s, baseline_decoherence_s)
    rows: list[dict[str, str]] = []

    for perturbation in DEFAULT_ANESTHESIA_PERTURBATIONS:
        energy_multiplier = (
            perturbation.coherent_units_multiplier * perturbation.coupling_multiplier
        )
        if energy_multiplier <= 0.0:
            raise ValueError("Perturbation energy multiplier must be positive")
        frequency_response = perturbation.frequency_hz / perturbation.frequency_scale_hz
        perturbed_tau_s = baseline_tau_s / energy_multiplier
        perturbed_decoherence_s = baseline_decoherence_s * perturbation.decoherence_time_multiplier
        perturbed_margin = timing_margin_log10(perturbed_tau_s, perturbed_decoherence_s)
        rows.append(
            {
                "perturbation": perturbation.name,
                "scope": perturbation.scope,
                "baseline_tau_s": format_float(baseline_tau_s),
                "perturbed_tau_s": format_float(perturbed_tau_s),
                "baseline_decoherence_s": format_float(baseline_decoherence_s),
                "perturbed_decoherence_s": format_float(perturbed_decoherence_s),
                "baseline_margin_log10": format_margin(baseline_margin),
                "perturbed_margin_log10": format_margin(perturbed_margin),
                "margin_delta_log10": format_margin(perturbed_margin - baseline_margin),
                "baseline_status": timing_status(baseline_tau_s, baseline_decoherence_s),
                "perturbed_status": timing_status(perturbed_tau_s, perturbed_decoherence_s),
                "predicted_direction": perturbation.predicted_direction,
                "frequency_hz": format_float(perturbation.frequency_hz),
                "frequency_response": format_float(frequency_response),
                "source_ids": ";".join(perturbation.source_ids),
                "note": perturbation.note,
            }
        )

    return rows


def all_volatile_anesthetics_reduce_margin(rows: list[dict[str, str]]) -> bool:
    return all(
        float(row["margin_delta_log10"]) < 0.0
        for row in rows
        if row["perturbation"].startswith("volatile_anesthetic")
    )
