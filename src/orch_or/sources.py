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
    "microtubule_structure_secondary": Source(
        source_id="microtubule_structure_secondary",
        title="Microtubule structural summary",
        authors="Secondary reference; replace with primary structural review before strong claims",
        year=2026,
        url="https://en.wikipedia.org/wiki/Microtubule",
        status="secondary_trace",
        usage="13 protofilaments, approximate tubulin dimer mass, and microtubule geometry defaults.",
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
