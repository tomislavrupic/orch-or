"""Microtubule geometry helpers for DP self-energy sensitivity.

These functions are bounded diagnostics, not biological claims.
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Iterable

from orch_or.collapse import (
    collapse_time_s,
    dp_gaussian_self_energy_excess_j,
    dp_point_mass_far_field_self_energy_j,
)
from orch_or.constants import TUBULIN_DIMER_MASS_KG
from orch_or.sources import require_known_sources

FIELDNAMES = [
    "assumption_label",
    "eg_model",
    "protofilament_count",
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
LATTICE_FIELDNAMES = [
    "assumption_label",
    "protofilament_count",
    "dimers_per_protofilament",
    "helical_start_number",
    "coherence_fraction",
    "selected_dimers",
    "lattice_radius_m",
    "lattice_length_m",
    "cloud_rms_radius_m",
    "separation_m",
    "eg_j",
    "tau_s",
    "source_ids",
    "note",
]
Point3D = tuple[float, float, float]


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


@dataclass(frozen=True)
class CoordinateMassCloud:
    """Simple smeared-mass proxy derived from a coordinate cloud.

    This is a bounded diagnostic helper, not an atomistic reconstruction.
    """

    points_m: tuple[Point3D, ...]
    masses_kg: tuple[float, ...]

    def __post_init__(self) -> None:
        if not self.points_m:
            raise ValueError("points_m must not be empty")
        if len(self.points_m) != len(self.masses_kg):
            raise ValueError("points_m and masses_kg must have the same length")
        if any(m <= 0.0 for m in self.masses_kg):
            raise ValueError("masses_kg must contain only positive masses")

    @property
    def total_mass_kg(self) -> float:
        return sum(self.masses_kg)

    @property
    def center_of_mass_m(self) -> Point3D:
        total_mass = self.total_mass_kg
        x = sum(m * p[0] for p, m in zip(self.points_m, self.masses_kg)) / total_mass
        y = sum(m * p[1] for p, m in zip(self.points_m, self.masses_kg)) / total_mass
        z = sum(m * p[2] for p, m in zip(self.points_m, self.masses_kg)) / total_mass
        return (x, y, z)

    def rms_radius_m(self) -> float:
        center = self.center_of_mass_m
        total_mass = self.total_mass_kg
        variance = 0.0
        for point, mass in zip(self.points_m, self.masses_kg):
            dx = point[0] - center[0]
            dy = point[1] - center[1]
            dz = point[2] - center[2]
            variance += mass * (dx * dx + dy * dy + dz * dz)
        return math.sqrt(variance / total_mass)


def coordinate_cloud_from_points(
    points_m: Iterable[Point3D],
    masses_kg: Iterable[float],
) -> CoordinateMassCloud:
    return CoordinateMassCloud(tuple(points_m), tuple(masses_kg))


def gaussian_smearing_radius_from_cloud(cloud: CoordinateMassCloud, scale_factor: float = 1.0) -> float:
    if scale_factor <= 0.0:
        raise ValueError("scale_factor must be positive")
    return cloud.rms_radius_m() * scale_factor


def cylinder_mass_density_from_cloud(cloud: CoordinateMassCloud, volume_m3: float) -> float:
    if volume_m3 <= 0.0:
        raise ValueError("volume_m3 must be positive")
    return cloud.total_mass_kg / volume_m3


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


def compute_eg_uniform_sphere(
    geometry: MicrotubuleGeometry,
    coherent_dimers: int,
    separation_m: float,
) -> float:
    """Return a uniform-sphere far-field diagnostic proxy.

    This is a deliberately coarse comparison model. It uses the equivalent
    sphere radius for the coherent mass domain and the same point-mass
    far-field interaction scale as a bounded surrogate.
    """

    if coherent_dimers <= 0:
        raise ValueError("coherent_dimers must be positive")
    if separation_m <= 0.0:
        raise ValueError("separation_m must be positive")
    mass = coherence_domain_mass_kg(geometry, coherent_dimers)
    sphere_radius_m = (3.0 * mass / (4.0 * math.pi * geometry.mass_density_kg_m3)) ** (1.0 / 3.0)
    return dp_point_mass_far_field_self_energy_j(mass, max(separation_m, 2.0 * sphere_radius_m))


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


def protofilament_lattice_points(
    geometry: MicrotubuleGeometry,
    protofilament_count: int,
    dimers_per_protofilament: int,
    helical_start_number: int = 3,
) -> tuple[Point3D, ...]:
    if protofilament_count <= 0:
        raise ValueError("protofilament_count must be positive")
    if dimers_per_protofilament <= 0:
        raise ValueError("dimers_per_protofilament must be positive")
    if helical_start_number < 0:
        raise ValueError("helical_start_number must be non-negative")

    lattice_radius_m = max(0.0, geometry.outer_radius_m - geometry.wall_thickness_m / 2.0)
    points: list[Point3D] = []
    for dimer_index in range(dimers_per_protofilament):
        axial_z_m = dimer_index * geometry.tubulin_length_m
        row_offset = helical_start_number * dimer_index
        for protofilament_index in range(protofilament_count):
            angle = 2.0 * math.pi * (protofilament_index + row_offset) / protofilament_count
            points.append(
                (
                    lattice_radius_m * math.cos(angle),
                    lattice_radius_m * math.sin(angle),
                    axial_z_m,
                )
            )
    return tuple(points)


def protofilament_lattice_sweep_rows(
    geometry: MicrotubuleGeometry,
    protofilament_count_grid: tuple[int, ...],
    dimers_per_protofilament_grid: tuple[int, ...],
    coherence_fraction_grid: tuple[float, ...],
    separation_grid_m: tuple[float, ...],
    source_ids: tuple[str, ...],
    assumption_label: str,
    helical_start_number: int = 3,
    note: str = "Dimer-center protofilament lattice proxy; not an atomistic mass distribution.",
) -> list[dict[str, str]]:
    if not protofilament_count_grid:
        raise ValueError("protofilament_count_grid must not be empty")
    if not dimers_per_protofilament_grid:
        raise ValueError("dimers_per_protofilament_grid must not be empty")
    if not coherence_fraction_grid:
        raise ValueError("coherence_fraction_grid must not be empty")
    if not separation_grid_m:
        raise ValueError("separation_grid_m must not be empty")
    require_known_sources(source_ids)

    rows: list[dict[str, str]] = []
    for protofilament_count in protofilament_count_grid:
        for dimers_per_protofilament in dimers_per_protofilament_grid:
            points = protofilament_lattice_points(
                geometry=geometry,
                protofilament_count=protofilament_count,
                dimers_per_protofilament=dimers_per_protofilament,
                helical_start_number=helical_start_number,
            )
            lattice_radius_m = max(0.0, geometry.outer_radius_m - geometry.wall_thickness_m / 2.0)
            lattice_length_m = dimers_per_protofilament * geometry.tubulin_length_m
            for coherence_fraction in coherence_fraction_grid:
                if coherence_fraction <= 0.0 or coherence_fraction > 1.0:
                    raise ValueError("coherence_fraction must be in (0, 1]")
                selected_dimers = max(1, round(len(points) * coherence_fraction))
                selected_points = points[:selected_dimers]
                cloud = coordinate_cloud_from_points(
                    selected_points,
                    (geometry.dimer_mass_kg for _ in selected_points),
                )
                smearing_radius_m = max(
                    gaussian_smearing_radius_from_cloud(cloud),
                    geometry.tubulin_length_m * 0.5,
                )
                total_mass_kg = cloud.total_mass_kg
                for separation_m in separation_grid_m:
                    if separation_m <= 0.0:
                        raise ValueError("separation_m must be positive")
                    eg_j = dp_gaussian_self_energy_excess_j(
                        mass_kg=total_mass_kg,
                        separation_m=separation_m,
                        smearing_radius_m=smearing_radius_m,
                    )
                    rows.append(
                        {
                            "assumption_label": assumption_label,
                            "protofilament_count": str(protofilament_count),
                            "dimers_per_protofilament": str(dimers_per_protofilament),
                            "helical_start_number": str(helical_start_number),
                            "coherence_fraction": f"{coherence_fraction:.6f}",
                            "selected_dimers": str(selected_dimers),
                            "lattice_radius_m": f"{lattice_radius_m:.6e}",
                            "lattice_length_m": f"{lattice_length_m:.6e}",
                            "cloud_rms_radius_m": f"{smearing_radius_m:.6e}",
                            "separation_m": f"{separation_m:.6e}",
                            "eg_j": f"{eg_j:.6e}",
                            "tau_s": f"{collapse_time_s(eg_j):.6e}",
                            "source_ids": ";".join(source_ids),
                            "note": note,
                        }
                    )
    return rows


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
    elif eg_model == "uniform_sphere":
        eg = compute_eg_uniform_sphere(geometry, coherent_dimers, separation_m)
    elif eg_model == "quadrature":
        eg = compute_eg_quadrature_validation(geometry, coherent_dimers, separation_m)
    elif eg_model == "diosi_regularized":
        eg = compute_eg_diosi_regularized(geometry, coherent_dimers, separation_m, smearing_radius_m)
    else:
        raise ValueError(f"unknown eg_model {eg_model!r}")
    return eg, collapse_time_s(eg)


def geometry_sweep_rows(
    geometry: MicrotubuleGeometry,
    protofilament_count_grid: tuple[int, ...],
    coherent_dimers_grid: tuple[int, ...],
    coherence_fraction_grid: tuple[float, ...],
    separation_grid_m: tuple[float, ...],
    smearing_radius_m: float,
    eg_model: str,
    source_ids: tuple[str, ...],
    assumption_label: str,
) -> list[dict[str, str]]:
    if not protofilament_count_grid:
        raise ValueError("protofilament_count_grid must not be empty")
    if not coherent_dimers_grid:
        raise ValueError("coherent_dimers_grid must not be empty")
    if not coherence_fraction_grid:
        raise ValueError("coherence_fraction_grid must not be empty")
    if not separation_grid_m:
        raise ValueError("separation_grid_m must not be empty")
    rows: list[dict[str, str]] = []
    for protofilament_count in protofilament_count_grid:
        if protofilament_count <= 0:
            raise ValueError("protofilament_count must be positive")
        for coherent_dimers in coherent_dimers_grid:
            for coherence_fraction in coherence_fraction_grid:
                if coherence_fraction <= 0.0 or coherence_fraction > 1.0:
                    raise ValueError("coherence_fraction must be in (0, 1]")
                effective_dimers = max(1, round(coherent_dimers * coherence_fraction * protofilament_count))
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
                            "protofilament_count": str(protofilament_count),
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
