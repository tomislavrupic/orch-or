"""Traceable source registry for HAOS-OR diagnostics."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Source:
    source_id: str
    title: str
    authors: str
    year: int
    url: str
    status: str
    usage: str
    metadata_gap: str = ""


SOURCE_REGISTRY: dict[str, Source] = {
    "diosi_2021_collapse_rate": Source(
        source_id="diosi_2021_collapse_rate",
        title="On the conjectured gravity-related collapse rate E_delta/hbar of massive quantum superpositions",
        authors="Lajos Diosi",
        year=2021,
        url="https://arxiv.org/abs/2111.04604",
        status="literature_traced",
        usage="DP/OR rate, gravitational self-energy excess, regulator caution.",
    ),
    "tegmark_2000_decoherence": Source(
        source_id="tegmark_2000_decoherence",
        title="The importance of quantum decoherence in brain processes",
        authors="Max Tegmark",
        year=2000,
        url="https://arxiv.org/abs/quant-ph/9907009",
        status="literature_traced",
        usage="Critical decoherence estimate range for brain and microtubule claims.",
    ),
    "hagan_2000_decoherence_reply": Source(
        source_id="hagan_2000_decoherence_reply",
        title="Quantum Computation in Brain Microtubules? Decoherence and Biological Feasibility",
        authors="S. Hagan, S. R. Hameroff, J. A. Tuszynski",
        year=2000,
        url="https://arxiv.org/abs/quant-ph/0005025",
        status="literature_traced",
        usage="Supportive/corrective decoherence estimate ranges asserted against Tegmark.",
    ),
    "craddock_2017_anesthetic_thz": Source(
        source_id="craddock_2017_anesthetic_thz",
        title="Anesthetic Alterations of Collective Terahertz Oscillations in Tubulin Correlate with Clinical Potency",
        authors="T. J. A. Craddock et al.",
        year=2017,
        url="https://www.nature.com/articles/s41598-017-09992-7",
        status="literature_traced",
        usage="Anesthetic perturbation direction for tubulin collective-oscillation predictions.",
    ),
    "microtubule_energy_transport_kalra_2022": Source(
        source_id="microtubule_energy_transport_kalra_2022",
        title="Electronic Energy Migration in Microtubules",
        authors="A. P. Kalra et al.",
        year=2022,
        url="https://arxiv.org/abs/2208.10628",
        status="literature_traced",
        usage="Microtubule exciton transport and anesthetic reduction of diffusion length.",
    ),
    "microtubule_structure_secondary": Source(
        source_id="microtubule_structure_secondary",
        title="Microtubule structural summary",
        authors="Secondary reference; replace with primary structural review before strong claims",
        year=2026,
        url="https://en.wikipedia.org/wiki/Microtubule",
        status="secondary_trace",
        usage="13 protofilaments, approximate tubulin dimer mass, and microtubule geometry defaults.",
    ),
    "microtubule_structure_nogales_1998": Source(
        source_id="microtubule_structure_nogales_1998",
        title="Structure of the alpha beta tubulin dimer by electron crystallography",
        authors="E. Nogales, S. G. Wolf, K. H. Downing",
        year=1998,
        url="https://www.nature.com/articles/391199a0",
        status="literature_pending",
        usage="Primary tubulin-dimer structural reference for geometry and mass-distribution upgrades.",
        metadata_gap="Lock DOI/page metadata and verify the primary article details against a direct source record.",
    ),
    "microtubule_lattice_nogales_1999": Source(
        source_id="microtubule_lattice_nogales_1999",
        title="High-resolution model of the microtubule",
        authors="E. Nogales, M. Whittaker, R. A. Milligan, K. H. Downing",
        year=1999,
        url="https://www.cell.com/cell/fulltext/S0092-8674(00)80712-3",
        status="literature_pending",
        usage="Primary lattice-geometry reference for 13-protofilament organization and cylinder approximations.",
        metadata_gap="Lock issue/page metadata and verify the cited lattice record directly.",
    ),
    "tubulin_atomic_lowe_2001": Source(
        source_id="tubulin_atomic_lowe_2001",
        title="Refined structure of alpha beta-tubulin at 3.5 A resolution",
        authors="J. Lowe, H. Li, K. H. Downing, E. Nogales",
        year=2001,
        url="https://doi.org/10.1016/S0022-2836(01)00989-8",
        status="literature_pending",
        usage="Higher-resolution tubulin coordinates for geometry tightening and Gaussian smearing choices.",
        metadata_gap="Confirm the DOI landing page or journal record and extract the resolution/structure details from a primary source.",
    ),
    "hameroff_time_crystal_2026": Source(
        source_id="hameroff_time_crystal_2026",
        title="Microtubules as time crystals and multiscale oscillators",
        authors="Stuart Hameroff",
        year=2026,
        url="docs/literature_queue.md",
        status="model_assumption",
        usage="Time-crystal framing for multiscale microtubule oscillation diagnostics.",
        metadata_gap="Lock the primary paper citation and publication venue before promoting this row.",
    ),
    "bandyopadhyay_multiscale_resonance": Source(
        source_id="bandyopadhyay_multiscale_resonance",
        title="Experimental multiscale microtubule resonances",
        authors="Anirban Bandyopadhyay",
        year=2026,
        url="docs/literature_queue.md",
        status="model_assumption",
        usage="Experimental resonance proxy for multiscale oscillation diagnostics.",
        metadata_gap="Lock the direct experimental citation and venue before promoting this row.",
    ),
    "anesthesia_counterfactual_untraced": Source(
        source_id="anesthesia_counterfactual_untraced",
        title="Counterfactual microtubule-stabilization perturbation",
        authors="HAOS-OR model assumption",
        year=2026,
        url="docs/literature_queue.md",
        status="model_assumption",
        usage="Executable prediction placeholder pending source-traced stabilizer/anesthesia experiments.",
    ),
}


def require_known_sources(source_ids: tuple[str, ...]) -> None:
    unknown = [source_id for source_id in source_ids if source_id not in SOURCE_REGISTRY]
    if unknown:
        raise ValueError(f"Unknown source ids: {unknown}")
