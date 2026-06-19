"""Export helpers for later HAOS-IIP import."""

from __future__ import annotations

from datetime import UTC, datetime


def build_summary(rows: list[dict[str, str]]) -> dict[str, object]:
    open_count = sum(row["status"] == "or_window_open" for row in rows)
    preempted_count = sum(row["status"] == "decoherence_preempts_or" for row in rows)
    return {
        "artifact_kind": "haos_or_timing_ladder_v0",
        "generated_at_utc": datetime.now(UTC).replace(microsecond=0).isoformat(),
        "claim_boundary": (
            "Diagnostic timing audit only; toy rows are not biological or ontological claims."
        ),
        "row_count": len(rows),
        "status_counts": {
            "or_window_open": open_count,
            "decoherence_preempts_or": preempted_count,
        },
        "haos_import_hint": {
            "metric": "timing_margin_log10",
            "perturbation_axis": "self_energy_or_decoherence_time",
            "collapse_definition": "loss of timing-window recoverability under perturbation",
        },
    }
