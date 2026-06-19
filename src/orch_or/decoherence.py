"""Decoherence-window comparison helpers."""

from __future__ import annotations

import math

from orch_or.collapse import timing_margin_log10, timing_status
from orch_or.parameters import DEFAULT_DECOHERENCE_ESTIMATES, TARGET_COLLAPSE_TIMES_S, DecoherenceEstimate
from orch_or.sweep import format_float, format_margin

FIELDNAMES = [
    "estimate",
    "stance",
    "lower_s",
    "upper_s",
    "representative_s",
    "target_tau_s",
    "margin_lower_log10",
    "margin_upper_log10",
    "representative_status",
    "source_ids",
    "note",
]


def representative_time_s(estimate: DecoherenceEstimate) -> float:
    return math.sqrt(estimate.lower_s * estimate.upper_s)


def decoherence_rows(
    estimates: tuple[DecoherenceEstimate, ...] = DEFAULT_DECOHERENCE_ESTIMATES,
    target_times_s: tuple[float, ...] = TARGET_COLLAPSE_TIMES_S,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for estimate in estimates:
        representative = representative_time_s(estimate)
        for target_tau_s in target_times_s:
            rows.append(
                {
                    "estimate": estimate.name,
                    "stance": estimate.stance,
                    "lower_s": format_float(estimate.lower_s),
                    "upper_s": format_float(estimate.upper_s),
                    "representative_s": format_float(representative),
                    "target_tau_s": format_float(target_tau_s),
                    "margin_lower_log10": format_margin(
                        timing_margin_log10(target_tau_s, estimate.lower_s)
                    ),
                    "margin_upper_log10": format_margin(
                        timing_margin_log10(target_tau_s, estimate.upper_s)
                    ),
                    "representative_status": timing_status(target_tau_s, representative),
                    "source_ids": ";".join(estimate.source_ids),
                    "note": estimate.note,
                }
            )
    return rows
