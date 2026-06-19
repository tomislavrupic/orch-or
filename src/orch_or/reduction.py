"""Discrete reduction event diagnostics.

This module adds a bounded event-selection layer on top of the existing
timing and DP helpers. It does not claim to prove consciousness; it
formalizes a menu of alternatives, a threshold crossing, the selected state,
and a reduction event for falsification sweeps.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from orch_or.collapse import collapse_time_s
from orch_or.decoherence import temperature_scaled_decoherence_s
from orch_or.sweep import format_float, format_margin

FIELDNAMES = [
    "scenario",
    "superposition_label",
    "alternative_set",
    "menu_size",
    "mass_distribution_label",
    "orchestration_score",
    "collective_threshold_state",
    "self_energy_j",
    "collapse_time_s",
    "decoherence_time_s",
    "selection_margin_log10",
    "event_time_s",
    "selected_state",
    "selection_rule",
    "gamma_link_hz",
    "decision_bias",
    "predicted_timing_correlate",
    "predicted_gamma_correlate",
    "predicted_behavioral_correlate",
    "classical_model_state",
    "classical_model_gamma_link_hz",
    "classical_model_decision_bias",
    "novel_distinction",
    "source_ids",
    "note",
]

DISTINCTION_FIELDNAMES = [
    "scenario",
    "source_locked_proxy",
    "selection_rule_source",
    "or_on_output",
    "or_off_counterfactual",
    "non_or_quantum_alternative",
    "classical_alternative",
    "observable_neural_correlate",
    "observable_behavioral_correlate",
    "actual_falsifier",
    "source_ids",
    "note",
]

SWEEP_FIELDNAMES = [
    "scenario",
    "superposition_label",
    "temperature_K",
    "noise_scale",
    "menu_size",
    "orchestration_score",
    "collective_threshold_state",
    "self_energy_j",
    "collapse_time_s",
    "decoherence_time_s",
    "selection_margin_log10",
    "selected_state",
    "selection_rule",
    "classical_model_state",
    "classical_distinguishability",
    "novel_distinction",
    "source_ids",
    "note",
]


@dataclass(frozen=True)
class ReductionAlternative:
    label: str
    weight: float
    gamma_link_hz: float
    decision_bias: float

    def __post_init__(self) -> None:
        if self.weight <= 0.0:
            raise ValueError("weight must be positive")
        if self.gamma_link_hz < 0.0:
            raise ValueError("gamma_link_hz must be non-negative")
        if not -1.0 <= self.decision_bias <= 1.0:
            raise ValueError("decision_bias must be in [-1, 1]")


@dataclass(frozen=True)
class ReductionScenario:
    name: str
    mass_distribution_label: str
    self_energy_j: float
    decoherence_time_s: float
    alternatives: tuple[ReductionAlternative, ...]
    source_ids: tuple[str, ...]
    note: str

    def __post_init__(self) -> None:
        if self.self_energy_j <= 0.0:
            raise ValueError("self_energy_j must be positive")
        if self.decoherence_time_s <= 0.0:
            raise ValueError("decoherence_time_s must be positive")
        if not self.alternatives:
            raise ValueError("alternatives must not be empty")


@dataclass(frozen=True)
class TubulinSuperposition:
    """A bounded menu of tubulin-like alternatives before reduction."""

    scenario: ReductionScenario
    selection_pressure: float = 1.0

    def __post_init__(self) -> None:
        if self.selection_pressure <= 0.0:
            raise ValueError("selection_pressure must be positive")


def collective_superposition(scenario: ReductionScenario, selection_pressure: float = 1.0) -> TubulinSuperposition:
    """Return an explicit tubulin superposition menu for the scenario."""

    return TubulinSuperposition(scenario=scenario, selection_pressure=selection_pressure)


def collective_orchestration_score(alternatives: tuple[ReductionAlternative, ...]) -> float:
    if not alternatives:
        raise ValueError("alternatives must not be empty")
    total_weight = sum(alt.weight for alt in alternatives)
    gamma_term = sum(alt.gamma_link_hz for alt in alternatives) / (1.0 + len(alternatives))
    bias_term = sum(alt.decision_bias for alt in alternatives)
    return total_weight + gamma_term / 1.0e3 + bias_term


def select_state(alternatives: tuple[ReductionAlternative, ...], selection_pressure: float) -> ReductionAlternative:
    if selection_pressure <= 0.0:
        raise ValueError("selection_pressure must be positive")
    scored = sorted(
        alternatives,
        key=lambda alt: (alt.weight * selection_pressure) + alt.decision_bias + (alt.gamma_link_hz / 1.0e3),
        reverse=True,
    )
    return scored[0]


def classical_reference_state(alternatives: tuple[ReductionAlternative, ...]) -> ReductionAlternative:
    return max(alternatives, key=lambda alt: (alt.weight, alt.gamma_link_hz))


def reduction_event_row(scenario: ReductionScenario, selection_pressure: float = 1.0) -> dict[str, str]:
    superposition = collective_superposition(scenario, selection_pressure=selection_pressure)
    tau_s = collapse_time_s(superposition.scenario.self_energy_j)
    selected = select_state(superposition.scenario.alternatives, superposition.selection_pressure)
    classical = classical_reference_state(superposition.scenario.alternatives)
    orchestration_score = collective_orchestration_score(superposition.scenario.alternatives)
    collective_threshold_state = "orchestrated_threshold_crossed" if tau_s <= scenario.decoherence_time_s else "threshold_not_reached"
    timing_correlate = "gamma_phase_lock" if selected.gamma_link_hz >= 60.0 else "subgamma_latency_shift"
    gamma_correlate = "enhanced_gamma_link" if selected.gamma_link_hz >= classical.gamma_link_hz else "gamma_link_suppressed"
    behavioral_correlate = "bias_toward_selected_state" if selected.decision_bias >= classical.decision_bias else "bias_shift_harder_to_classical"
    novel_distinction = (
        "OR predicts finite event_time plus menu selection under threshold crossing; "
        "classical baseline keeps the menu but lacks threshold-locked reduction timing."
    )
    return {
        "scenario": scenario.name,
        "superposition_label": f"{scenario.name}:{len(scenario.alternatives)}_alternatives",
        "alternative_set": ";".join(alt.label for alt in scenario.alternatives),
        "menu_size": str(len(scenario.alternatives)),
        "mass_distribution_label": scenario.mass_distribution_label,
        "orchestration_score": format_float(orchestration_score),
        "collective_threshold_state": collective_threshold_state,
        "self_energy_j": format_float(scenario.self_energy_j),
        "collapse_time_s": format_float(tau_s),
        "decoherence_time_s": format_float(scenario.decoherence_time_s),
        "selection_margin_log10": format_margin(math.log10(scenario.decoherence_time_s / tau_s)),
        "event_time_s": format_float(min(tau_s, scenario.decoherence_time_s)),
        "selected_state": selected.label,
        "selection_rule": "max(weight * pressure + bias + gamma_link_hz / 1e3)",
        "gamma_link_hz": format_float(selected.gamma_link_hz),
        "decision_bias": format_float(selected.decision_bias),
        "predicted_timing_correlate": timing_correlate,
        "predicted_gamma_correlate": gamma_correlate,
        "predicted_behavioral_correlate": behavioral_correlate,
        "classical_model_state": classical.label,
        "classical_model_gamma_link_hz": format_float(classical.gamma_link_hz),
        "classical_model_decision_bias": format_float(classical.decision_bias),
        "novel_distinction": novel_distinction,
        "source_ids": ";".join(scenario.source_ids),
        "note": scenario.note,
    }


def reduction_sweep_rows(
    scenarios: tuple[ReductionScenario, ...],
    temperatures_K: tuple[float, ...] = (280.0, 310.0, 350.0),
    noise_scales: tuple[float, ...] = (0.5, 1.0, 2.0),
    temperature_exponent: float = 0.5,
) -> list[dict[str, str]]:
    if not scenarios:
        raise ValueError("scenarios must not be empty")
    if not temperatures_K:
        raise ValueError("temperatures_K must not be empty")
    if not noise_scales:
        raise ValueError("noise_scales must not be empty")
    if temperature_exponent <= 0.0:
        raise ValueError("temperature_exponent must be positive")

    rows: list[dict[str, str]] = []
    for scenario in scenarios:
        for temperature_K in temperatures_K:
            for noise_scale in noise_scales:
                superposition = collective_superposition(scenario, selection_pressure=noise_scale)
                decoherence_time_s = temperature_scaled_decoherence_s(
                    superposition.scenario.decoherence_time_s,
                    temperature_K,
                    exponent=temperature_exponent,
                ) / noise_scale
                tau_s = collapse_time_s(superposition.scenario.self_energy_j)
                selected = select_state(superposition.scenario.alternatives, selection_pressure=superposition.selection_pressure)
                classical = classical_reference_state(superposition.scenario.alternatives)
                rows.append(
                    {
                        "scenario": scenario.name,
                        "superposition_label": f"{scenario.name}:{len(scenario.alternatives)}_alternatives",
                        "temperature_K": format_float(temperature_K),
                        "noise_scale": format_float(noise_scale),
                        "menu_size": str(len(scenario.alternatives)),
                        "orchestration_score": format_float(
                            collective_orchestration_score(superposition.scenario.alternatives)
                        ),
                        "collective_threshold_state": (
                            "orchestrated_threshold_crossed"
                            if tau_s <= decoherence_time_s
                            else "threshold_not_reached"
                        ),
                        "self_energy_j": format_float(scenario.self_energy_j),
                        "collapse_time_s": format_float(tau_s),
                        "decoherence_time_s": format_float(decoherence_time_s),
                        "selection_margin_log10": format_margin(math.log10(decoherence_time_s / tau_s)),
                        "selected_state": selected.label,
                        "selection_rule": "max(weight * pressure + bias + gamma_link_hz / 1e3)",
                        "classical_model_state": classical.label,
                        "classical_distinguishability": format_margin(
                            abs(math.log10(decoherence_time_s / tau_s))
                        ),
                        "novel_distinction": (
                            "OR changes finite event timing under threshold crossing; "
                            "classical reference state stays tied to static weights only."
                        ),
                        "source_ids": ";".join(scenario.source_ids),
                        "note": scenario.note,
                    }
                )
    return rows


def reduction_distinction_rows(scenarios: tuple[ReductionScenario, ...]) -> list[dict[str, str]]:
    if not scenarios:
        raise ValueError("scenarios must not be empty")
    rows: list[dict[str, str]] = []
    for scenario in scenarios:
        event_row = reduction_event_row(scenario)
        rows.append(
            {
                "scenario": scenario.name,
                "source_locked_proxy": "tubulin_superposition_menu_proxy",
                "selection_rule_source": "max(weight * pressure + bias + gamma_link_hz / 1e3)",
                "or_on_output": (
                    f"{event_row['selected_state']} at {event_row['event_time_s']} s; "
                    f"{event_row['predicted_timing_correlate']}; {event_row['predicted_gamma_correlate']}; "
                    f"{event_row['predicted_behavioral_correlate']}"
                ),
                "or_off_counterfactual": (
                    "no objective reduction; no discrete selected_state; collapse timing not instantiated"
                ),
                "non_or_quantum_alternative": (
                    "coherent tubulin dynamics without objective reduction; selection stays interpretive"
                ),
                "classical_alternative": (
                    f"{event_row['classical_model_state']} with deterministic weight-only choice and no reduction timing"
                ),
                "observable_neural_correlate": (
                    "gamma-linked phase locking and timing-window shift if OR-on; otherwise no threshold-locked phase marker"
                ),
                "observable_behavioral_correlate": (
                    "bias toward the selected menu state; falsified if behavior matches classical weights without timing signature"
                ),
                "actual_falsifier": (
                    "the table fails if OR-on and OR-off rows become observationally identical across timing, gamma, and bias"
                ),
                "source_ids": ";".join(scenario.source_ids),
                "note": scenario.note,
            }
        )
    return rows


def default_reduction_scenarios() -> tuple[ReductionScenario, ...]:
    return (
        ReductionScenario(
            name="tubulin_menu_small",
            mass_distribution_label="gaussian_pair_menu",
            self_energy_j=1.0e-31,
            decoherence_time_s=1.0e-6,
            alternatives=(
                ReductionAlternative("state_alpha", 1.0, 40.0, -0.1),
                ReductionAlternative("state_beta", 1.2, 60.0, 0.0),
                ReductionAlternative("state_gamma", 0.8, 80.0, 0.2),
            ),
            source_ids=(
                "diosi_2021_collapse_rate",
                "tegmark_2000_decoherence",
                "hagan_2000_decoherence_reply",
            ),
            note="Minimal menu over three alternatives; used for explicit reduction selection.",
        ),
        ReductionScenario(
            name="tubulin_menu_gamma_linked",
            mass_distribution_label="lattice_proxy_menu",
            self_energy_j=1.0e-29,
            decoherence_time_s=1.0e-4,
            alternatives=(
                ReductionAlternative("choice_left", 0.9, 40.0, -0.2),
                ReductionAlternative("choice_center", 1.4, 80.0, 0.1),
                ReductionAlternative("choice_right", 1.1, 120.0, 0.0),
                ReductionAlternative("choice_suppressed", 0.7, 15.0, -0.4),
            ),
            source_ids=(
                "diosi_2021_collapse_rate",
                "microtubule_structure_nogales_1998",
                "microtubule_lattice_nogales_1999",
                "tubulin_atomic_lowe_2001",
            ),
            note="Lattice proxy menu with gamma-linked alternatives for falsification sweeps.",
        ),
    )
