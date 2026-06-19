# Source Register

Executable rows use source IDs rather than prose-only citations. Status labels describe how strongly a row may be interpreted.

## `diosi_2021_collapse_rate`

- Status: `literature_traced`
- Source: Lajos Diosi, "On the conjectured gravity-related collapse rate E_delta/hbar of massive quantum superpositions" (2021)
- URL: https://arxiv.org/abs/2111.04604
- Used for: DP/OR collapse rate `1/tau = E_delta/hbar`, gravitational self-energy excess form, and regulator caution.
- Boundary: The source itself frames the proposal as speculative and notes pointlike divergences.

## `tegmark_2000_decoherence`

- Status: `literature_traced`
- Source: Max Tegmark, "The importance of quantum decoherence in brain processes" (2000)
- URL: https://arxiv.org/abs/quant-ph/9907009
- Used for: critical decoherence range `1e-13` to `1e-20` seconds.
- Boundary: This is a critical estimate, not an Orch-OR-supportive parameter.

## `hagan_2000_decoherence_reply`

- Status: `literature_traced`
- Source: S. Hagan, S. R. Hameroff, J. A. Tuszynski, "Quantum Computation in Brain Microtubules? Decoherence and Biological Feasibility" (2000)
- URL: https://arxiv.org/abs/quant-ph/0005025
- Used for: supportive/contested ranges `1e-5` to `1e-4` seconds and `1e-2` to `1e-1` seconds.
- Boundary: These ranges are part of a disputed reply to Tegmark.

## `craddock_2017_anesthetic_thz`

- Status: `literature_traced`
- Source: T. J. A. Craddock et al., "Anesthetic Alterations of Collective Terahertz Oscillations in Tubulin Correlate with Clinical Potency" (Scientific Reports, 2017)
- URL: https://www.nature.com/articles/s41598-017-09992-7
- Used for: direction-of-effect anesthesia perturbation predictions.
- Boundary: The executable model does not reproduce the paper's molecular simulation or clinical potency analysis.

## `microtubule_energy_transport_kalra_2022`

- Status: `literature_traced`
- Source: A. P. Kalra et al., "Electronic Energy Migration in Microtubules" (2022)
- URL: https://arxiv.org/abs/2208.10628
- Used for: microtubule exciton transport, diffusion length, anesthetic reduction of transport, and protofilament-count robustness checks.
- Boundary: This supports transport and photophysics diagnostics, not a consciousness claim.

## `microtubule_structure_secondary`

- Status: `secondary_trace`
- Source: Microtubule structural summary
- URL: https://en.wikipedia.org/wiki/Microtubule
- Used for: approximate tubulin dimer mass and 13-protofilament structural defaults.
- Boundary: Replace with primary structural reviews before promoting these rows to `literature_traced`.

## `microtubule_structure_nogales_1998`

- Status: `literature_pending`
- Source: E. Nogales, S. G. Wolf, K. H. Downing, "Structure of the alpha beta tubulin dimer by electron crystallography" (Nature, 1998)
- URL: https://www.nature.com/articles/391199a0
- Used for: atomic tubulin-dimer geometry and mass-distribution upgrades.
- Boundary: Primary title and journal trace are in place; promote only after DOI/page metadata is fully locked.

## `microtubule_lattice_nogales_1999`

- Status: `literature_pending`
- Source: E. Nogales, M. Whittaker, R. A. Milligan, K. H. Downing, "High-resolution model of the microtubule" (Cell, 1999)
- URL: https://www.cell.com/cell/fulltext/S0092-8674(00)80712-3
- Used for: 13-protofilament lattice organization and cylinder approximations.
- Boundary: Primary lattice reference, not a validated executable parameter set yet.

## `tubulin_atomic_lowe_2001`

- Status: `literature_pending`
- Source: J. Lowe, H. Li, K. H. Downing, E. Nogales, "Refined structure of alpha beta-tubulin at 3.5 A resolution" (Journal of Molecular Biology, 2001)
- URL: https://doi.org/10.1016/S0022-2836(01)00989-8
- Used for: higher-resolution tubulin coordinates and Gaussian-smearing choices.
- Boundary: Use for geometry tightening once the article metadata is fully locked.

## `microtubule_primary_trace_pending`

- Status: `retired_placeholder`
- Source: retired placeholder, replaced by the three traced primary candidates above
- URL: not applicable
- Used for: historical note only.
- Boundary: Do not use this row for new executable defaults.

## `anesthesia_counterfactual_untraced`

- Status: `model_assumption`
- Source: HAOS-OR counterfactual row
- URL: literature queue in this repo
- Used for: executable microtubule-stabilizer rescue prediction placeholder.
- Boundary: Not evidence. It is a hypothesis row waiting for source tracing.

## `radical_pair_microtubule_reorganization`

- Status: `contested_support`
- Source: Hadi Zadeh-Haghighi, Christoph Simon, "Radical pairs may play a role in microtubule reorganization" (2021)
- URL: https://arxiv.org/abs/2109.14055
- Used for: magnetic-field-sensitive radical-pair mechanism as a possible adjacent explanation for microtubule organization.
- Boundary: Does not validate Orch-OR; it only supports a quantum-spin-sensitive adjacent mechanism.

## `microtubule_optical_response_2026`

- Status: `supported_microphysics`
- Source: Lea Gassab, Travis J. A. Craddock, "Engineering quantum optical responses of microtubules through tryptophan-network simulations and ultraviolet spectroscopy" (2026)
- URL: https://arxiv.org/abs/2604.18604
- Used for: tunable microtubule fluorescence, polymerization-sensitive yield, tryptophan quenching.
- Boundary: Supports microtubule photophysics, not consciousness.

## `microtubule_information_flow_2026`

- Status: `supported_microphysics`
- Source: Lea Gassab, Onur Pusuluk, Travis J. A. Craddock, "Quantum Information Flow in Microtubule Tryptophan Networks" (2026)
- URL: https://arxiv.org/abs/2602.02868
- Used for: coherence/coherence-routing diagnostics in tryptophan networks.
- Boundary: Supports nonclassical correlation flow in cytoskeletal chromophore networks, not Orch-OR validation.

## `halothane_binding_proteome_2008`

- Status: `secondary_trace`
- Source: Jonathan Z. Pan et al., "Halothane binding proteome in human brain cortex" (2008)
- URL: not directly fetched in this pass; title recovered from secondary index
- Used for: halothane binding to tubulin monomers alongside other proteins.
- Boundary: Keep as a secondary-trace placeholder until the primary article metadata is fetched directly.

## `microtubule_stability_anthracene_2013`

- Status: `secondary_trace`
- Source: Daniel J. Emerson et al., "Direct Modulation of Microtubule Stability Contributes to Anthracene General Anesthesia" (2013)
- URL: not directly fetched in this pass; title recovered from secondary index
- Used for: microtubule-stability perturbation as a possible anesthesia-adjacent effect.
- Boundary: Does not establish Orch-OR; it only supports microtubule perturbation as a measurable anesthesia-related variable.
