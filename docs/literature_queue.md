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

## Strong Candidate Primary Structural Sources

These are the next primary sources to trace directly if we want to finish locking the structural metadata behind the already-wired executable defaults:

- Nogales, Wolf, Downing 1998, "Structure of the alpha beta tubulin dimer by electron crystallography" (Nature).
- Nogales, Whittaker, Milligan, Downing 1999, "High-resolution model of the microtubule" (Cell).
- Lowe, Li, Downing, Nogales 2001, "Refined structure of alpha beta-tubulin at 3.5 A resolution" (Journal of Molecular Biology).

## Currently Wired Source IDs

- `diosi_2021_collapse_rate`: traced enough for the DP/OR rate and self-energy-excess formula.
- `tegmark_2000_decoherence`: traced enough for the critical decoherence range.
- `hagan_2000_decoherence_reply`: traced enough for the supportive/contested decoherence ranges.
- `craddock_2017_anesthetic_thz`: traced enough for direction-of-effect anesthesia perturbation predictions.
- `microtubule_structure_secondary`: secondary only; retained as a historical placeholder, but not used in the current geometry defaults.
- `microtubule_structure_nogales_1998`, `microtubule_lattice_nogales_1999`, `tubulin_atomic_lowe_2001`: literature pending; use for geometry upgrades once metadata is locked.
- `anesthesia_counterfactual_untraced`: model assumption only.

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
