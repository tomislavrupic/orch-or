"""Microtubule geometry helpers for DP self-energy sensitivity.

These functions are bounded diagnostics, not biological claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from orch_or.collapse import (
    collapse_time_s,
    dp_gaussian_self_energy_excess_j,
    dp_point_mass_far_field_self_energy_j,
)
from orch_or.constants import TUBULIN_DIMER_MASS_KG


@dataclass(frozen=True)
class MicrotubuleGeometry:
    protofilaments: int
    dimers_per_protofilament: int
    outer_diameter_m: float
    wall_thickness_m: float
    tubulin_length_m: float
    dimer_mass_kg: float = TUBULIN_DIMER_MASS_KG

    @property
    def total_dimers(self) -> int:
        return self.protofilaments * self.dimers_per_protofilament

    @property
    def cylinder_length_m(self) -> float:
        return self.dimers_per_protofilament * self.tubulin_length_m

    @property
    def inner_radius_m(self) -> float:
        return max(0.0, self.outer_radius_m - self.wall_thickness_m)

    @property
    def outer_radius_m(self) -> float:
        return self.outer_diameter_m / 2.0

    @property
    def wall_volume_m3(self) -> float:
        outer = math.pi * self.outer_radius_m**2 * self.cylinder_length_m
        inner = math.pi * self.inner_radius_m**2 * self.cylinder_length_m
        return max(0.0, outer - inner)

    @property
    def mass_density_kg_m3(self) -> float:
        return (self.total_dimers * self.dimer_mass_kg) / self.wall_volume_m3


DEFAULT_GEOMETRY = MicrotubuleGeometry(
    protofilaments=13,
    dimers_per_protofilament=8,
    outer_diameter_m=25.0e-9,
    wall_thickness_m=5.0e-9,
    tubulin_length_m=8.0e-9,
)


def gaussian_radius_from_scale(scale_m: float, factor: float = 1.0) -> float:
    if scale_m <= 0.0:
        raise ValueError("scale_m must be positive")
    if factor <= 0.0:
        raise ValueError("factor must be positive")
    return scale_m * factor


def cylinder_mass_kg(geometry: MicrotubuleGeometry) -> float:
    return geometry.total_dimers * geometry.dimer_mass_kg


def coherence_domain_mass_kg(geometry: MicrotubuleGeometry, coherent_dimers: int) -> float:
    if coherent_dimers <= 0:
        raise ValueError("coherent_dimers must be positive")
    return coherent_dimers * geometry.dimer_mass_kg


def compute_eg_gaussian_pair(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
    smearing_radius_m: float,
) -> float:
    return dp_gaussian_self_energy_excess_j(
        mass_kg=coherence_domain_mass_kg(geometry, coherent_dimers),
        separation_m=separation_m,
        smearing_radius_m=smearing_radius_m,
    )


def compute_eg_uniform_cylinder(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
) -> float:
    if coherent_dimers <= 0:
        raise ValueError("coherent_dimers must be positive")
    if separation_m <= 0.0:
        raise ValueError("separation_m must be positive")
    mass = coherence_domain_mass_kg(geometry, coherent_dimers)
    return dp_point_mass_far_field_self_energy_j(mass, max(separation_m, geometry.outer_diameter_m))


def compute_eg_quadrature_validation(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
) -> float:
    """A validation-only proxy using the far-field interaction scale."""

    if coherent_dimers <= 0:
        raise ValueError("coherent_dimers must be positive")
    if separation_m <= 0.0:
        raise ValueError("separation_m must be positive")
    mass = coherence_domain_mass_kg(geometry, coherent_dimers)
    return dp_point_mass_far_field_self_energy_j(mass, separation_m)


def collapse_time_for_domain(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
    smearing_radius_m: float,
    eg_model: str = "gaussian",
) -> tuple[float, float]:
    if eg_model == "gaussian":
        eg = compute_eg_gaussian_pair(geometry, coherent_dimers, separation_m, smearing_radius_m)
    elif eg_model == "uniform_cylinder":
        eg = compute_eg_uniform_cylinder(geometry, coherent_dimers, separation_m)
    elif eg_model == "quadrature":
        eg = compute_eg_quadrature_validation(geometry, coherent_dimers, separation_m)
    else:
        raise ValueError(f"unknown eg_model {eg_model!r}")
    return eg, collapse_time_s(eg)
