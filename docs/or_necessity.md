# OR Necessity Test

The repo needs at least one artifact that changes when Objective Reduction is removed.

## Null Hypothesis

Without Objective Reduction, the repo should not produce a finite gravity-collapse timing window from `tau = hbar / E_G`.

## Comparison Artifact

`examples/or_off_comparison.py` writes `examples/output/or_off_comparison.csv`.
`examples/reduction_events.py` writes `examples/output/reduction_events.csv`.
`examples/reduction_sweep.py` writes `examples/output/reduction_sweep.csv`.

Columns:

- `or_on_tau_s`
- `or_off_tau_s`
- `decoherence_estimate`
- `decoherence_time_s`
- `decoherence_margin_log10`
- `or_on_status`
- `or_off_status`
- `necessity_note`

Interpretation:

- `or_on_tau_s` is finite by construction from the DP timing relation.
- `or_off_tau_s` is `inf` because the collapse window is removed.
- This does not validate Orch-OR; it only shows the repo's collapse-time results are conditional on OR being present.

The reduction artifact adds the next layer: a menu of alternatives, a selected state, and an event-time stamp produced when the menu is reduced.
The reduction sweep adds the falsification layer: temperature and noise change the selected state, the threshold state, and the contrast with a classical reference state.

## Why This Matters

This artifact separates:

1. microtubule photophysics
2. microtubule structural dynamics
3. anesthesia-related perturbations
4. decoherence-window assumptions
5. the gravity-collapse timing claim itself

Only the fourth item disappears when OR is removed.
