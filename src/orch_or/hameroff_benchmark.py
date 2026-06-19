"""Hameroff-facing benchmark summaries.

The rows in this module summarize existing diagnostics. They do not add a
new mechanism or promote Orch-OR claims beyond the underlying source rows.
"""

from __future__ import annotations

from orch_or.anesthesia import anesthesia_prediction_rows
from orch_or.sources import require_known_sources
from orch_or.sweep import format_float, format_margin
from orch_or.time_crystal import OscillatorMode, multiscale_oscillation_rows
from orch_or.trp_networks import tryptophan_network_rows


FIELDNAMES = [
    "benchmark",
    "artifact",
    "emphasis",
    "diagnostic_metric",
    "diagnostic_value",
    "stance",
    "source_ids",
    "note",
]

TIME_CRYSTAL_SOURCE_IDS = ("hameroff_time_crystal_2026", "bandyopadhyay_multiscale_resonance")
TRP_SOURCE_IDS = (
    "tryptophan_superradiance_2024",
    "photoprotection_architectures_2024",
    "superradiant_excitonic_states_2018",
)


def default_time_crystal_rows() -> list[dict[str, str]]:
    modes = (
        OscillatorMode("kHz", 1.0e3, 1.0, phase_rad=0.0, damping=0.05),
        OscillatorMode("MHz", 1.0e6, 0.8, phase_rad=0.6, damping=0.1),
        OscillatorMode("GHz", 1.0e9, 0.6, phase_rad=1.0, damping=0.25),
        OscillatorMode("THz", 1.0e12, 0.4, phase_rad=1.3, damping=0.5),
    )
    return multiscale_oscillation_rows(
        modes,
        source_ids=TIME_CRYSTAL_SOURCE_IDS,
        note="Diagnostic multiscale oscillation ladder; not a biological proof.",
    )


def default_trp_rows() -> list[dict[str, str]]:
    return tryptophan_network_rows(
        network_sizes=(10, 100, 1_000, 10_000, 100_000),
        disorders=(0.0, 0.1, 0.5, 1.0),
        source_ids=TRP_SOURCE_IDS,
        note="Diagnostic tryptophan superradiance sweep; not a consciousness claim.",
        anesthetic_strength=0.3,
    )


def default_hameroff_benchmark_rows() -> list[dict[str, str]]:
    return hameroff_benchmark_rows(
        time_crystal_rows=default_time_crystal_rows(),
        trp_rows=default_trp_rows(),
        anesthesia_rows=anesthesia_prediction_rows(),
    )


def hameroff_benchmark_rows(
    time_crystal_rows: list[dict[str, str]],
    trp_rows: list[dict[str, str]],
    anesthesia_rows: list[dict[str, str]],
) -> list[dict[str, str]]:
    if not time_crystal_rows:
        raise ValueError("time_crystal_rows must not be empty")
    if not trp_rows:
        raise ValueError("trp_rows must not be empty")

    volatile_rows = [
        row for row in anesthesia_rows if row["perturbation"].startswith("volatile_anesthetic")
    ]
    if not volatile_rows:
        raise ValueError("anesthesia_rows must include at least one volatile anesthetic row")

    time_source_ids = _source_ids(time_crystal_rows)
    trp_source_ids = _source_ids(trp_rows)
    anesthesia_source_ids = _source_ids(volatile_rows)
    frequencies = [float(row["base_frequency_hz"]) for row in time_crystal_rows]
    collapse_proxies = [float(row["collapse_probability"]) for row in time_crystal_rows]
    quantum_yields = [float(row["estimated_quantum_yield"]) for row in trp_rows]
    damping_proxies = [float(row["anesthetic_damping"]) for row in trp_rows]
    margin_deltas = [float(row["margin_delta_log10"]) for row in volatile_rows]
    frequency_responses = [float(row["frequency_response"]) for row in volatile_rows]

    return [
        {
            "benchmark": "time_crystal_frequency_span",
            "artifact": "time_crystal_multiscale.csv",
            "emphasis": "time_crystal_multiscale",
            "diagnostic_metric": "frequency_span_hz",
            "diagnostic_value": (
                f"min={format_float(min(frequencies))};max={format_float(max(frequencies))}"
            ),
            "stance": "model_assumption",
            "source_ids": ";".join(time_source_ids),
            "note": "Summarizes the frozen kHz-to-THz oscillator ladder; not a biological proof.",
        },
        {
            "benchmark": "time_crystal_phase_trigger_proxy",
            "artifact": "time_crystal_multiscale.csv",
            "emphasis": "time_crystal_multiscale",
            "diagnostic_metric": "max_collapse_trigger_proxy",
            "diagnostic_value": format_float(max(collapse_proxies)),
            "stance": "model_assumption",
            "source_ids": ";".join(time_source_ids),
            "note": "Phase-sensitive trigger proxy only; not an objective-collapse probability.",
        },
        {
            "benchmark": "trp_quantum_yield_proxy",
            "artifact": "trp_superradiance_table.csv",
            "emphasis": "trp_quantum_optics",
            "diagnostic_metric": "max_estimated_quantum_yield",
            "diagnostic_value": format_float(max(quantum_yields)),
            "stance": "supported_microphysics_proxy",
            "source_ids": ";".join(trp_source_ids),
            "note": "Summarizes deterministic Trp-network yield proxies; not a consciousness claim.",
        },
        {
            "benchmark": "trp_anesthetic_damping_proxy",
            "artifact": "trp_superradiance_table.csv",
            "emphasis": "trp_quantum_optics",
            "diagnostic_metric": "max_anesthetic_damping",
            "diagnostic_value": format_float(max(damping_proxies)),
            "stance": "supported_microphysics_proxy",
            "source_ids": ";".join(trp_source_ids),
            "note": "Reports the strongest damping proxy in the frozen Trp sweep.",
        },
        {
            "benchmark": "anesthesia_margin_shift",
            "artifact": "anesthesia_prediction_table.csv",
            "emphasis": "anesthesia_disruption",
            "diagnostic_metric": "min_volatile_margin_delta_log10",
            "diagnostic_value": format_margin(min(margin_deltas)),
            "stance": "model_assumption",
            "source_ids": ";".join(anesthesia_source_ids),
            "note": "Volatile-anesthetic rows reduce the OR timing margin in this proxy model.",
        },
        {
            "benchmark": "anesthesia_frequency_response",
            "artifact": "anesthesia_prediction_table.csv",
            "emphasis": "anesthesia_disruption",
            "diagnostic_metric": "max_frequency_response",
            "diagnostic_value": format_float(max(frequency_responses)),
            "stance": "model_assumption",
            "source_ids": ";".join(anesthesia_source_ids),
            "note": "Frequency-aware perturbation summary; not a clinical potency model.",
        },
    ]


def _source_ids(rows: list[dict[str, str]]) -> tuple[str, ...]:
    seen: list[str] = []
    for row in rows:
        for source_id in row.get("source_ids", "").split(";"):
            if source_id and source_id not in seen:
                seen.append(source_id)
    require_known_sources(tuple(seen))
    return tuple(seen)
