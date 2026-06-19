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
from orch_or.parameters import DEFAULT_PARAMETER_SETS, ParameterSet

__all__ = [
    "DEFAULT_PARAMETER_SETS",
    "ParameterSet",
    "collapse_time_s",
    "dp_gaussian_self_energy_excess_j",
    "dp_point_mass_far_field_self_energy_j",
    "required_self_energy_j",
    "timing_margin_log10",
    "timing_status",
    "total_self_energy_j",
]
