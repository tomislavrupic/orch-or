# Literature Queue

This file tracks sources that must be traced before toy values become public scientific parameter sets.

## Status Labels

- `toy`: useful only for code validation and sensitivity plumbing
- `literature_pending`: intended source family known, exact value/source not yet locked
- `literature_traced`: source, value, unit, transformation, and uncertainty recorded

## Initial Source Families To Trace

1. Penrose/Diosi objective reduction timing and gravitational self-energy.
2. Hameroff-Penrose Orch-OR model summaries and tubulin/domain assumptions.
3. Tegmark-style decoherence estimates for brain/microtubule settings.
4. Hagan-Hameroff-Tuszynski responses and alternative decoherence estimates.
5. Contemporary microtubule/tubulin structural parameter references.
6. Anesthesia perturbation models relevant to tubulin or microtubule dynamics.
7. Primary structural references for the microtubule lattice and alpha/beta tubulin dimer.
8. Time-crystal and multiscale microtubule oscillation references linked to the current Hameroff emphasis.
9. Tryptophan superradiance, photoprotection, and microtubule quantum optical channel references.

## Locked Primary Structural Sources

These primary sources now carry locked DOI/page metadata in `docs/source_register.md` and `src/orch_or/sources.py`:

- Nogales, Wolf, Downing 1998, "Structure of the alpha beta tubulin dimer by electron crystallography" (Nature 391, 199-203), DOI `10.1038/34465`.
- Nogales, Whittaker, Milligan, Downing 1999, "High-resolution model of the microtubule" (Cell 96(1), 79-88), DOI `10.1016/S0092-8674(00)80961-7`.
- Lowe, Li, Downing, Nogales 2001, "Refined structure of alpha beta-tubulin at 3.5 A resolution" (Journal of Molecular Biology 313(5), 1045-1057), DOI `10.1006/jmbi.2001.5077`.

Next structural step:
Import a real coordinate table or PDB-derived centroid cloud rather than using dimer-center lattice proxies.

## Time-Crystal Source Targets

These are placeholders for the current time-crystal/multiscale oscillation workstream until the primary citations are locked:

- Hameroff 2026 time-crystal paper referenced in current discussions.
- Bandyopadhyay experimental microtubule resonance work referenced in current discussions.

## Tryptophan / Optical Channel Source Targets

These are placeholders for the current Trp optical-channel workstream until the primary citations are locked:

- Babcock et al. 2024 superradiance paper on tryptophan mega-networks.
- Patwa, Babcock, Kurian 2024 photoprotection paper on neuroprotein architectures.
- Celardo, Angeli, Kurian, Craddock 2018 superradiant excitonic states in microtubules.

## Currently Wired Source IDs

- `diosi_2021_collapse_rate`: traced enough for the DP/OR rate and self-energy-excess formula.
- `tegmark_2000_decoherence`: traced enough for the critical decoherence range.
- `hagan_2000_decoherence_reply`: traced enough for the supportive/contested decoherence ranges.
- `craddock_2017_anesthetic_thz`: traced enough for direction-of-effect anesthesia perturbation predictions.
- `microtubule_structure_secondary`: secondary only; retained as a historical placeholder, but not used in the current geometry defaults.
- `microtubule_structure_nogales_1998`, `microtubule_lattice_nogales_1999`, `tubulin_atomic_lowe_2001`: traced primary structure references used by the geometry and protofilament lattice rows.
- `anesthesia_counterfactual_untraced`: model assumption only.
- `hameroff_time_crystal_2026`, `bandyopadhyay_multiscale_resonance`: model assumptions tied to the current notebook roadmap; keep as placeholders until the primary papers are locked.
- `tryptophan_superradiance_2024`, `photoprotection_architectures_2024`, `superradiant_excitonic_states_2018`: supported-microphysics source rows for the Trp optical-channel layer; keep the citation trail explicit until the repo has direct traces for the exact publication metadata.

See `docs/source_register.md` for URLs and usage boundaries.

## Trace Template

```text
parameter_name:
scope:
source:
quoted_value:
unit:
converted_value_si:
conversion_steps:
uncertainty_or_range:
notes:
```

No row should be promoted to `literature_traced` until the conversion can be repeated from the source.
