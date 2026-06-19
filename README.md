# HAOS-OR

**Orch-OR diagnostic bridge for HAOS-IIP style recoverability audits.**

This sub repo is a computational scaffold for testing Orch-OR-adjacent timing claims under explicit perturbation. It does not claim that Orch-OR is true, that consciousness is solved, or that toy microtubule models are biologically sufficient.

Layer used: HAOS/OR diagnostic only.

## Scope

The executable spine starts from one cheap invariant:

```text
tau = hbar / E_G
```

It then adds bounded diagnostics for:

- total gravitational self-energy proxy `E_G`
- objective reduction timing proxy `tau`
- timing margin against a supplied decoherence/noise time
- Diosi-Penrose threshold sensitivity for tubulin-scale mass assumptions
- critical and supportive decoherence estimate ranges
- anesthesia-style perturbation predictions

The result is a timing audit, not an ontology.

## Quick Start

From this repo root:

```bash
python3 examples/quick_reproduce.py
```

Expected result:

```text
Orch-OR diagnostic spine passed.
```

You can also run the package CLI without installing by exposing `src`:

```bash
PYTHONPATH=src python3 -m orch_or collapse --eg-j 1e-31
PYTHONPATH=src python3 -m orch_or sweep --output examples/output/collapse_time_table.csv
PYTHONPATH=src python3 -m orch_or thresholds --output examples/output/dp_threshold_table.csv
PYTHONPATH=src python3 -m orch_or decoherence --output examples/output/decoherence_estimate_table.csv
PYTHONPATH=src python3 -m orch_or anesthesia --output examples/output/anesthesia_prediction_table.csv
```

For editable install:

```bash
python3 -m pip install -e .
python3 -m orch_or reproduce
```

## Repo Structure

```text
src/orch_or/                 core pure-stdlib diagnostic package
examples/quick_reproduce.py  one-command deterministic reproduction spine
examples/expected_*.csv/json frozen expected public outputs
tests/                       low-cost unit checks
docs/                        bridge contract and literature queue
notebooks/                   executable notebook entry points
```

## Claim Boundaries

Rows are explicitly scoped:

- `toy`: code validation only
- `mixed_assumption`: sourced structure plus explicit model assumptions
- `critical_assumption`: stress-test values used to challenge the model
- `supportive_contested`: values asserted in supportive literature but still disputed
- `model_assumption`: executable perturbation, not a clinical or biological claim

Before any public scientific statement:

1. Replace or add parameter sets with source-traced values.
2. Record each source in `docs/source_register.md` and `docs/literature_queue.md`.
3. Run perturbation sweeps and preserve generated artifacts.
4. Import only bounded metrics into HAOS-IIP.

## Key Files

- [docs/equations.md](docs/equations.md): equations and approximations implemented in code.
- [docs/source_register.md](docs/source_register.md): source IDs used by executable rows.
- [docs/haos_iip_bridge_contract.md](docs/haos_iip_bridge_contract.md): HAOS-IIP import contract.
- [notebooks/01_dp_thresholds.ipynb](notebooks/01_dp_thresholds.ipynb): threshold table walkthrough.
- [notebooks/02_decoherence_anesthesia.ipynb](notebooks/02_decoherence_anesthesia.ipynb): decoherence and anesthesia prediction walkthrough.

## Minimal HAOS Test

Claim or task:
Build a reproducible Orch-OR timing diagnostic.

Constraints:
No solved-consciousness claims. No hidden biological validity claims. Toy values stay toy.

Cheap perturbations:
Vary `E_G`, coherent domain size, coupling, and decoherence time by orders of magnitude.

Pass condition:
The code produces deterministic tables, and the interpretation remains bounded when parameters move.

Minimal next step:
Replace the secondary microtubule structural source with primary structural references and add one independently checked anesthesia experiment row.
