# Published-Values Comparison

This note compares a small set of published values with the repo's frozen diagnostic outputs.
It is a cross-check, not a claim of biological validity.

| Topic | Published value / range | Repo artifact | Repo value / range | Notes |
| --- | --- | --- | --- | --- |
| Tegmark decoherence | `1e-20` to `1e-13` s | `decoherence_estimate_table.csv` | `tegmark_microtubule_critical` | Used as the critical decoherence benchmark. |
| Hagan/Hameroff/Tuszynski reply | `1e-5` to `1e-4` s | `decoherence_estimate_table.csv` | `hagan_corrected_orch_or` | Supportive but contested range. |
| Actin-gel extension | `1e-2` to `1e-1` s | `decoherence_estimate_table.csv` | `hagan_actin_gel_extension` | Additional supportive range, still contested. |
| Ion-collision damping proxy | `1e-15` to `1e-11` s | `decoherence_estimate_table.csv` | `ion_collision_damping_proxy` | Model-assumption row for fast environmental damping. |
| Water/MAP protection proxy | `1e-4` to `1e-1` s | `decoherence_estimate_table.csv` | `water_map_protection_proxy` | Model-assumption row for slower protective damping. |
| Temperature sweep | `280 K` / `310 K` / `350 K` | `temperature_decoherence_sweep.csv` | `temperature_sweep_rows()` | Deterministic temperature-sensitivity harness for the same decoherence estimates. |
| Microtubule transport | `~6.6 nm` diffusion length | `or_decoherence_comparison.csv` | Geometry-vs-decoherence no OR-favorable islands in current band | Transport is supported, but it does not rescue the current OR timing band. |
| Trp superradiance | `15.7%` to `19.5%` quantum yield | `trp_superradiance_table.csv` | `tryptophan_network_rows()` | Deterministic Trp-network yield and damping proxy harness. |
| UV superradiance | `15.7%` to `19.5%` quantum yield | `paper_matrix.md` | `supported_microphysics` row | Supports photophysics, not consciousness. |
| Anesthetic perturbation | Collective oscillation / transport reduction | `anesthesia_prediction_table.csv` | Frequency-aware perturbation rows | The repo treats this as a bounded diagnostic only. |
| Timing statistics | Deterministic spread around `tau = 2.5e-2 s` | `timing_statistics_table.csv` | 9 fixed spread samples | This is a pseudo-Monte Carlo harness for reproducible timing sensitivity. |

Repo interpretation:

1. The timing spine reproduces the source ranges it cites.
2. The geometry sweep does not yet produce OR-favorable islands in the current parameter band.
3. The perturbation layer keeps the mechanism claims bounded and source-traced.
