# HAOS-IIP Bridge Contract

This contract defines the first safe import surface from HAOS-OR into HAOS-IIP.

## Artifact

```text
artifact_kind: haos_or_timing_ladder_v0
```

The artifact summarizes timing-window recoverability under a parameter set.

## Required Fields

CSV rows must include:

- `parameter_set`
- `scope`
- `coherent_units`
- `unit_self_energy_j`
- `coupling`
- `total_self_energy_j`
- `collapse_time_s`
- `decoherence_time_s`
- `timing_margin_log10`
- `status`

DP threshold CSV rows must include:

- `mass_model`
- `scope`
- `mass_kg`
- `superposition_separation_m`
- `smearing_radius_m`
- `unit_dp_energy_j`
- `target_tau_s`
- `required_energy_j`
- `required_coherent_units`
- `source_ids`

Decoherence CSV rows must include:

- `estimate`
- `stance`
- `lower_s`
- `upper_s`
- `representative_s`
- `target_tau_s`
- `margin_lower_log10`
- `margin_upper_log10`
- `representative_status`
- `source_ids`

Anesthesia prediction CSV rows must include:

- `perturbation`
- `baseline_tau_s`
- `perturbed_tau_s`
- `baseline_decoherence_s`
- `perturbed_decoherence_s`
- `margin_delta_log10`
- `predicted_direction`
- `source_ids`

Summary JSON must include:

- `artifact_kind`
- `claim_boundary`
- `row_count`
- `status_counts`
- `haos_import_hint`

## HAOS Interpretation

`timing_margin_log10 = log10(decoherence_time / tau)`

Positive margin:
The supplied timing proxy fits inside the supplied decoherence/noise window.

Negative margin:
The supplied noise window closes before the timing proxy.

Collapse meaning:
Loss of timing-window recoverability under perturbation.

Forbidden interpretation:
Proof of Orch-OR, proof of quantum consciousness, or proof of biological implementation.

## Next Integration Step

Add a HAOS-IIP sidecar importer that reads the CSV and treats `timing_margin_log10` as a bounded diagnostic metric beside existing recoverability telemetry.
