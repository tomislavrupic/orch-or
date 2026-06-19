"""Parameter sets for the first HAOS-OR timing spine."""

from __future__ import annotations

from dataclasses import dataclass

from orch_or.constants import TUBULIN_DIMER_MASS_KG
from orch_or.sources import require_known_sources


@dataclass(frozen=True)
class ParameterSet:
    """A bounded parameter set for a timing diagnostic."""

    name: str
    scope: str
    coherent_units: int
    unit_self_energy_j: float
    decoherence_time_s: float
    coupling: float = 1.0
    source_ids: tuple[str, ...] = ()
    note: str = ""

    def __post_init__(self) -> None:
        require_known_sources(self.source_ids)


@dataclass(frozen=True)
class DPMassModel:
    """A mass-distribution assumption for DP self-energy sensitivity."""

    name: str
    scope: str
    mass_kg: float
    superposition_separation_m: float
    smearing_radius_m: float
    source_ids: tuple[str, ...]
    note: str

    def __post_init__(self) -> None:
        require_known_sources(self.source_ids)


@dataclass(frozen=True)
class DecoherenceEstimate:
    """A sourced decoherence-time range."""

    name: str
    stance: str
    lower_s: float
    upper_s: float
    source_ids: tuple[str, ...]
    note: str

    def __post_init__(self) -> None:
        require_known_sources(self.source_ids)


@dataclass(frozen=True)
class AnesthesiaPerturbation:
    """A bounded perturbation scenario for anesthesia predictions."""

    name: str
    scope: str
    coherent_units_multiplier: float
    coupling_multiplier: float
    decoherence_time_multiplier: float
    source_ids: tuple[str, ...]
    predicted_direction: str
    note: str

    def __post_init__(self) -> None:
        require_known_sources(self.source_ids)


DEFAULT_PARAMETER_SETS: tuple[ParameterSet, ...] = (
    ParameterSet(
        name="toy_low_energy",
        scope="toy",
        coherent_units=1_000,
        unit_self_energy_j=1.0e-34,
        decoherence_time_s=1.0e-6,
        source_ids=(),
        note="Toy lower-energy timing check; not literature traced.",
    ),
    ParameterSet(
        name="toy_mid_energy",
        scope="toy",
        coherent_units=1_000_000,
        unit_self_energy_j=1.0e-32,
        decoherence_time_s=1.0e-6,
        source_ids=(),
        note="Toy mid-energy timing check; not literature traced.",
    ),
    ParameterSet(
        name="toy_high_energy",
        scope="toy",
        coherent_units=1_000_000_000,
        unit_self_energy_j=1.0e-30,
        decoherence_time_s=1.0e-6,
        source_ids=(),
        note="Toy high-energy timing check; not literature traced.",
    ),
)


DEFAULT_DP_MASS_MODELS: tuple[DPMassModel, ...] = (
    DPMassModel(
        name="tubulin_dimer_angstrom_smear",
        scope="mixed_assumption",
        mass_kg=TUBULIN_DIMER_MASS_KG,
        superposition_separation_m=1.0e-10,
        smearing_radius_m=1.0e-10,
        source_ids=("diosi_2021_collapse_rate", "microtubule_structure_secondary"),
        note="Tubulin mass is structural; separation and smearing are explicit sensitivity assumptions.",
    ),
    DPMassModel(
        name="tubulin_dimer_nm_smear",
        scope="mixed_assumption",
        mass_kg=TUBULIN_DIMER_MASS_KG,
        superposition_separation_m=1.0e-9,
        smearing_radius_m=1.0e-9,
        source_ids=("diosi_2021_collapse_rate", "microtubule_structure_secondary"),
        note="Nanometer-scale regulator sensitivity row; not an asserted Orch-OR biological value.",
    ),
    DPMassModel(
        name="tubulin_dimer_tegmark_24nm_challenge",
        scope="critical_assumption",
        mass_kg=TUBULIN_DIMER_MASS_KG,
        superposition_separation_m=24.0e-9,
        smearing_radius_m=1.0e-9,
        source_ids=(
            "diosi_2021_collapse_rate",
            "tegmark_2000_decoherence",
            "hagan_2000_decoherence_reply",
            "microtubule_structure_secondary",
        ),
        note="Challenge-scale displacement used as a sensitivity stressor, not as a settled model input.",
    ),
)


TARGET_COLLAPSE_TIMES_S: tuple[float, ...] = (
    1.0e-1,
    2.5e-2,
    1.0e-3,
    1.0e-5,
)


DEFAULT_DECOHERENCE_ESTIMATES: tuple[DecoherenceEstimate, ...] = (
    DecoherenceEstimate(
        name="tegmark_microtubule_critical",
        stance="critical",
        lower_s=1.0e-20,
        upper_s=1.0e-13,
        source_ids=("tegmark_2000_decoherence",),
        note="Tegmark's critical brain/microtubule decoherence range.",
    ),
    DecoherenceEstimate(
        name="hagan_corrected_orch_or",
        stance="supportive_contested",
        lower_s=1.0e-5,
        upper_s=1.0e-4,
        source_ids=("hagan_2000_decoherence_reply",),
        note="Hagan/Hameroff/Tuszynski corrected estimate range.",
    ),
    DecoherenceEstimate(
        name="hagan_actin_gel_extension",
        stance="supportive_contested",
        lower_s=1.0e-2,
        upper_s=1.0e-1,
        source_ids=("hagan_2000_decoherence_reply",),
        note="Additional actin-gel enhancement range asserted by Hagan/Hameroff/Tuszynski.",
    ),
)


DEFAULT_ANESTHESIA_PERTURBATIONS: tuple[AnesthesiaPerturbation, ...] = (
    AnesthesiaPerturbation(
        name="volatile_anesthetic_mild",
        scope="model_assumption",
        coherent_units_multiplier=0.7,
        coupling_multiplier=0.7,
        decoherence_time_multiplier=0.5,
        source_ids=("craddock_2017_anesthetic_thz",),
        predicted_direction="reduced_or_window",
        note="Mild executable proxy for anesthetic disruption of tubulin collective modes.",
    ),
    AnesthesiaPerturbation(
        name="volatile_anesthetic_strong",
        scope="model_assumption",
        coherent_units_multiplier=0.25,
        coupling_multiplier=0.25,
        decoherence_time_multiplier=0.1,
        source_ids=("craddock_2017_anesthetic_thz",),
        predicted_direction="strongly_reduced_or_window",
        note="Strong stress-test proxy, not a clinical dose model.",
    ),
    AnesthesiaPerturbation(
        name="microtubule_stabilizer_counterfactual",
        scope="model_assumption",
        coherent_units_multiplier=1.2,
        coupling_multiplier=1.0,
        decoherence_time_multiplier=2.0,
        source_ids=("anesthesia_counterfactual_untraced",),
        predicted_direction="expanded_or_window",
        note="Counterfactual rescue prediction; trace experimental basis before public claims.",
    ),
)
