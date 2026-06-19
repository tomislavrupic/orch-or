"""HAOS-OR Orch-OR diagnostic bridge."""

from orch_or.collapse import (
    collapse_time_s,
    dp_gaussian_self_energy_excess_j,
    dp_point_mass_far_field_self_energy_j,
    required_self_energy_j,
    timing_margin_log10,
    timing_status,
    total_self_energy_j,
)
from orch_or.geometry import (
    DEFAULT_GEOMETRY,
    MicrotubuleGeometry,
    collapse_time_for_domain,
    coherence_domain_mass_kg,
    compute_eg_gaussian_pair,
    compute_eg_quadrature_validation,
    compute_eg_uniform_cylinder,
    geometry_sweep_rows,
)
from orch_or.parameters import DEFAULT_PARAMETER_SETS, ParameterSet

__all__ = [
    "DEFAULT_PARAMETER_SETS",
    "DEFAULT_GEOMETRY",
    "ParameterSet",
    "MicrotubuleGeometry",
    "collapse_time_s",
    "collapse_time_for_domain",
    "dp_gaussian_self_energy_excess_j",
    "dp_point_mass_far_field_self_energy_j",
    "coherence_domain_mass_kg",
    "compute_eg_gaussian_pair",
    "compute_eg_quadrature_validation",
    "compute_eg_uniform_cylinder",
    "geometry_sweep_rows",
    "required_self_energy_j",
    "timing_margin_log10",
    "timing_status",
    "total_self_energy_j",
]
