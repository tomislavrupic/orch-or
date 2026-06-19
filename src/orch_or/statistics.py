"""Deterministic timing-statistics helpers.

This is a compact Monte-Carlo-style harness for frozen timing diagnostics.
It is not a quantum simulation and does not claim physical stochasticity.
"""

from __future__ import annotations

import math

from orch_or.sweep import format_float

FIELDNAMES = [
    "scenario",
    "sample_index",
    "baseline_tau_s",
    "jitter_factor",
    "sampled_tau_s",
    "sampled_status",
    "source_ids",
    "note",
]


def deterministic_jitter_factors(count: int = 9, spread: float = 0.25) -> tuple[float, ...]:
    if count <= 0:
        raise ValueError("count must be positive")
    if spread <= 0.0:
        raise ValueError("spread must be positive")
    center = count // 2
    factors = []
    for index in range(count):
        offset = index - center
        factors.append(math.exp((offset / max(1, center)) * spread))
    return tuple(factors)


def timing_statistics_rows(
    baseline_tau_s: float,
    source_ids: tuple[str, ...],
    scenario: str = "deterministic_timing_sampler",
    count: int = 9,
    spread: float = 0.25,
) -> list[dict[str, str]]:
    if baseline_tau_s <= 0.0:
        raise ValueError("baseline_tau_s must be positive")
    rows: list[dict[str, str]] = []
    for index, jitter_factor in enumerate(deterministic_jitter_factors(count=count, spread=spread)):
        sampled_tau_s = baseline_tau_s * jitter_factor
        rows.append(
            {
                "scenario": scenario,
                "sample_index": str(index),
                "baseline_tau_s": format_float(baseline_tau_s),
                "jitter_factor": format_float(jitter_factor),
                "sampled_tau_s": format_float(sampled_tau_s),
                "sampled_status": "faster" if sampled_tau_s < baseline_tau_s else "slower",
                "source_ids": ";".join(source_ids),
                "note": "Deterministic spread around the baseline timing proxy; not a physical randomness model.",
            }
        )
    return rows
