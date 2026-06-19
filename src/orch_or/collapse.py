"""Small, auditable Orch-OR timing helpers."""

from __future__ import annotations

import math

from orch_or.constants import GRAVITATIONAL_CONSTANT_M3_KG_S2, HBAR_J_S


def _require_positive(name: str, value: float) -> None:
    if value <= 0.0:
        raise ValueError(f"{name} must be positive; got {value!r}")


def collapse_time_s(self_energy_j: float) -> float:
    """Return tau = hbar / E_G in seconds."""

    _require_positive("self_energy_j", self_energy_j)
    return HBAR_J_S / self_energy_j


def required_self_energy_j(target_tau_s: float) -> float:
    """Return the E_G required to produce a target collapse time."""

    _require_positive("target_tau_s", target_tau_s)
    return HBAR_J_S / target_tau_s


def total_self_energy_j(
    unit_self_energy_j: float,
    coherent_units: int,
    coupling: float = 1.0,
) -> float:
    """Return a linear toy aggregation of self-energy over a coherent domain.

    This is intentionally not a biological claim. It is the cheapest possible
    aggregation model for sensitivity plumbing.
    """

    _require_positive("unit_self_energy_j", unit_self_energy_j)
    if coherent_units <= 0:
        raise ValueError(f"coherent_units must be positive; got {coherent_units!r}")
    _require_positive("coupling", coupling)
    return unit_self_energy_j * coherent_units * coupling


def dp_point_mass_far_field_self_energy_j(mass_kg: float, separation_m: float) -> float:
    """Return a point-mass far-field DP energy proxy.

    Point masses make the DP self-terms divergent. This helper is only the
    long-separation interaction scale G m^2 / d, useful as a coarse check.
    """

    _require_positive("mass_kg", mass_kg)
    _require_positive("separation_m", separation_m)
    return GRAVITATIONAL_CONSTANT_M3_KG_S2 * mass_kg * mass_kg / separation_m


def dp_gaussian_self_energy_excess_j(
    mass_kg: float,
    separation_m: float,
    smearing_radius_m: float,
) -> float:
    """Return a finite Gaussian-smeared DP self-energy excess.

    Model:
        E_delta = G m^2 [1/(sqrt(pi) R0) - erf(d/(2 R0))/d]

    The expression is a regulator-backed diagnostic approximation for two
    equal Gaussian mass distributions separated by d. The short-distance limit
    is handled with the leading Taylor term to avoid cancellation.
    """

    _require_positive("mass_kg", mass_kg)
    _require_positive("separation_m", separation_m)
    _require_positive("smearing_radius_m", smearing_radius_m)

    ratio = separation_m / smearing_radius_m
    prefactor = GRAVITATIONAL_CONSTANT_M3_KG_S2 * mass_kg * mass_kg
    if ratio < 1.0e-5:
        return prefactor * separation_m * separation_m / (
            12.0 * math.sqrt(math.pi) * smearing_radius_m**3
        )
    return prefactor * (
        1.0 / (math.sqrt(math.pi) * smearing_radius_m)
        - math.erf(separation_m / (2.0 * smearing_radius_m)) / separation_m
    )


def timing_margin_log10(tau_s: float, decoherence_time_s: float) -> float:
    """Return log10(decoherence_time / tau).

    Positive values mean the OR timing proxy is shorter than the supplied noise
    time. Negative values mean decoherence preempts the timing proxy.
    """

    _require_positive("tau_s", tau_s)
    _require_positive("decoherence_time_s", decoherence_time_s)
    return math.log10(decoherence_time_s / tau_s)


def timing_status(tau_s: float, decoherence_time_s: float) -> str:
    """Classify whether the timing proxy survives the supplied noise window."""

    return (
        "or_window_open"
        if timing_margin_log10(tau_s, decoherence_time_s) >= 0.0
        else "decoherence_preempts_or"
    )
