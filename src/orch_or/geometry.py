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

FIELDNAMES = [
    "assumption_label",
    "eg_model",
    "coherent_dimers",
    "coherence_fraction",
    "separation_m",
    "smearing_radius_m",
    "total_dimers",
    "geometry_outer_diameter_m",
    "geometry_mass_density_kg_m3",
    "eg_j",
    "tau_s",
    "source_ids",
]
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


def compute_eg_diosi_regularized(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
    smearing_radius_m: float,
) -> float:
    """Return a conservative Diósi-style regularized proxy.

    This is a bounded diagnostic variant that keeps the same Gaussian regulator
    but softens the shortest-distance behavior a little more aggressively.
    """

    if coherent_dimers <= 0:
        raise ValueError("coherent_dimers must be positive")
    if separation_m <= 0.0:
        raise ValueError("separation_m must be positive")
    if smearing_radius_m <= 0.0:
        raise ValueError("smearing_radius_m must be positive")
    mass = coherence_domain_mass_kg(geometry, coherent_dimers)
    softened_separation = max(separation_m, smearing_radius_m * 0.5)
    return dp_gaussian_self_energy_excess_j(
        mass_kg=mass,
        separation_m=softened_separation,
        smearing_radius_m=smearing_radius_m,
    )


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
    elif eg_model == "diosi_regularized":
        eg = compute_eg_diosi_regularized(geometry, coherent_dimers, separation_m, smearing_radius_m)
    else:
        raise ValueError(f"unknown eg_model {eg_model!r}")
    return eg, collapse_time_s(eg)


def geometry_sweep_rows(
    geometry: MicrotubuleGeometry,
    coherent_dimers_grid: tuple[int, ...],
    coherence_fraction_grid: tuple[float, ...],
    separation_grid_m: tuple[float, ...],
    smearing_radius_m: float,
    eg_model: str,
    source_ids: tuple[str, ...],
    assumption_label: str,
) -> list[dict[str, str]]:
    if not coherent_dimers_grid:
        raise ValueError("coherent_dimers_grid must not be empty")
    if not coherence_fraction_grid:
        raise ValueError("coherence_fraction_grid must not be empty")
    if not separation_grid_m:
        raise ValueError("separation_grid_m must not be empty")
    rows: list[dict[str, str]] = []
    for coherent_dimers in coherent_dimers_grid:
        for coherence_fraction in coherence_fraction_grid:
            if coherence_fraction <= 0.0 or coherence_fraction > 1.0:
                raise ValueError("coherence_fraction must be in (0, 1]")
            effective_dimers = max(1, round(coherent_dimers * coherence_fraction))
            for separation_m in separation_grid_m:
                eg_j, tau_s = collapse_time_for_domain(
                    geometry=geometry,
                    coherent_dimers=effective_dimers,
                    separation_m=separation_m,
                    smearing_radius_m=smearing_radius_m,
                    eg_model=eg_model,
                )
                rows.append(
                    {
                        "assumption_label": assumption_label,
                        "eg_model": eg_model,
                        "coherent_dimers": str(coherent_dimers),
                        "coherence_fraction": f"{coherence_fraction:.6f}",
                        "separation_m": f"{separation_m:.6e}",
                        "smearing_radius_m": f"{smearing_radius_m:.6e}",
                        "total_dimers": str(geometry.total_dimers),
                        "geometry_outer_diameter_m": f"{geometry.outer_diameter_m:.6e}",
                        "geometry_mass_density_kg_m3": f"{geometry.mass_density_kg_m3:.6e}",
                        "eg_j": f"{eg_j:.6e}",
                        "tau_s": f"{tau_s:.6e}",
                        "source_ids": ";".join(source_ids),
                    }
                )
    return rows
