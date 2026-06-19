"""Tryptophan-network photophysics diagnostics.

Bounded superradiance and damping proxies for microtubule-associated Trp
networks. These are descriptive sweeps, not full excitonic simulations.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

FIELDNAMES = [
    "network_label",
    "site_count",
    "disorder",
    "base_quantum_yield",
    "superradiant_gain",
    "estimated_quantum_yield",
    "subradiant_retention",
    "anesthetic_damping",
    "source_ids",
    "note",
]


@dataclass(frozen=True)
class TryptophanNetwork:
    label: str
    site_count: int
    disorder: float
    base_quantum_yield: float = 0.124
    superradiant_gain: float = 0.0

    def __post_init__(self) -> None:
        if self.site_count <= 0:
            raise ValueError("site_count must be positive")
        if self.disorder < 0.0:
            raise ValueError("disorder must be non-negative")
        if not 0.0 < self.base_quantum_yield <= 1.0:
            raise ValueError("base_quantum_yield must be in (0, 1]")
        if self.superradiant_gain < 0.0:
            raise ValueError("superradiant_gain must be non-negative")


def site_count_scale(site_count: int) -> float:
    if site_count <= 0:
        raise ValueError("site_count must be positive")
    return math.log10(site_count + 1.0)


def superradiant_gain(site_count: int, disorder: float) -> float:
    if disorder < 0.0:
        raise ValueError("disorder must be non-negative")
    scale = site_count_scale(site_count)
    return max(0.0, 0.5 * scale / (1.0 + disorder))


def estimated_quantum_yield(
    site_count: int,
    disorder: float,
    base_quantum_yield: float = 0.124,
) -> float:
    if not 0.0 < base_quantum_yield <= 1.0:
        raise ValueError("base_quantum_yield must be in (0, 1]")
    gain = superradiant_gain(site_count, disorder)
    yield_estimate = base_quantum_yield * (1.0 + gain)
    return min(1.0, yield_estimate)


def subradiant_retention(site_count: int, disorder: float) -> float:
    """Return a bounded retention proxy for dark-state persistence."""

    if disorder < 0.0:
        raise ValueError("disorder must be non-negative")
    return max(0.0, min(1.0, 1.0 / (1.0 + disorder + 0.25 * math.log1p(site_count))))


def anesthetic_damping_proxy(
    site_count: int,
    anesthetic_strength: float,
    disorder: float,
) -> float:
    if anesthetic_strength < 0.0:
        raise ValueError("anesthetic_strength must be non-negative")
    gain = superradiant_gain(site_count, disorder)
    damping = anesthetic_strength * (1.0 + disorder) / (1.0 + gain)
    return max(0.0, damping)


def tryptophan_network_rows(
    network_sizes: tuple[int, ...],
    disorders: tuple[float, ...],
    source_ids: tuple[str, ...],
    note: str,
    anesthetic_strength: float = 0.3,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for site_count in network_sizes:
        for disorder in disorders:
            gain = superradiant_gain(site_count, disorder)
            qy = estimated_quantum_yield(site_count, disorder)
            retention = subradiant_retention(site_count, disorder)
            damping = anesthetic_damping_proxy(site_count, anesthetic_strength, disorder)
            rows.append(
                {
                    "network_label": f"Trp_{site_count}",
                    "site_count": str(site_count),
                    "disorder": f"{disorder:.6e}",
                    "base_quantum_yield": f"{0.124:.6e}",
                    "superradiant_gain": f"{gain:.6e}",
                    "estimated_quantum_yield": f"{qy:.6e}",
                    "subradiant_retention": f"{retention:.6e}",
                    "anesthetic_damping": f"{damping:.6e}",
                    "source_ids": ";".join(source_ids),
                    "note": note,
                }
            )
    return rows
