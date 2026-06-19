"""Time-crystal and multiscale oscillation diagnostics.

This module stays bounded and descriptive: it models coupled oscillators,
beat frequencies, and a simple collapse trigger proxy.
"""

from __future__ import annotations

import math
from dataclasses import dataclass


FIELDNAMES = [
    "mode_label",
    "base_frequency_hz",
    "amplitude",
    "phase_rad",
    "damping",
    "coherence_time_s",
    "beat_frequency_hz",
    "collapse_probability",
    "source_ids",
    "note",
]


@dataclass(frozen=True)
class OscillatorMode:
    label: str
    frequency_hz: float
    amplitude: float
    phase_rad: float = 0.0
    damping: float = 0.0

    def __post_init__(self) -> None:
        if self.frequency_hz <= 0.0:
            raise ValueError("frequency_hz must be positive")
        if self.amplitude <= 0.0:
            raise ValueError("amplitude must be positive")
        if self.damping < 0.0:
            raise ValueError("damping must be non-negative")


def beat_frequency_hz(a: OscillatorMode, b: OscillatorMode) -> float:
    return abs(a.frequency_hz - b.frequency_hz)


def coherence_envelope_s(mode: OscillatorMode) -> float:
    if mode.damping == 0.0:
        return math.inf
    return 1.0 / mode.damping


def floquet_like_response(
    drive_hz: float,
    natural_hz: float,
    coupling: float,
    coherence_time_s: float,
) -> float:
    if drive_hz <= 0.0 or natural_hz <= 0.0:
        raise ValueError("frequencies must be positive")
    if coupling < 0.0:
        raise ValueError("coupling must be non-negative")
    if coherence_time_s <= 0.0:
        raise ValueError("coherence_time_s must be positive")
    detuning = abs(drive_hz - natural_hz) / natural_hz
    envelope = math.exp(-1.0 / coherence_time_s)
    return coupling * envelope / (1.0 + detuning)


def collapse_trigger_probability(
    mode: OscillatorMode,
    threshold_phase_rad: float = math.pi / 2.0,
) -> float:
    """Return a bounded proxy for a phase-triggered collapse event.

    The probability is not physical collapse probability; it is a diagnostic
    surrogate for phase-sensitive trigger likelihood.
    """

    if threshold_phase_rad <= 0.0:
        raise ValueError("threshold_phase_rad must be positive")
    phase_distance = abs(math.sin(mode.phase_rad - threshold_phase_rad))
    damping_factor = math.exp(-mode.damping)
    return max(0.0, min(1.0, mode.amplitude * damping_factor * (1.0 - phase_distance)))


def multiscale_oscillation_rows(
    modes: tuple[OscillatorMode, ...],
    source_ids: tuple[str, ...],
    note: str,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for mode in modes:
        rows.append(
            {
                "mode_label": mode.label,
                "base_frequency_hz": f"{mode.frequency_hz:.6e}",
                "amplitude": f"{mode.amplitude:.6e}",
                "phase_rad": f"{mode.phase_rad:.6e}",
                "damping": f"{mode.damping:.6e}",
                "coherence_time_s": (
                    "inf" if mode.damping == 0.0 else f"{coherence_envelope_s(mode):.6e}"
                ),
                "beat_frequency_hz": f"{beat_frequency_hz(mode, modes[0]):.6e}",
                "collapse_probability": f"{collapse_trigger_probability(mode):.6e}",
                "source_ids": ";".join(source_ids),
                "note": note,
            }
        )
    return rows
