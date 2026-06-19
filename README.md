# Orch-OR

[![License](https://img.shields.io/badge/license-noncommercial%20research-blue)](LICENSE)
[![Repo](https://img.shields.io/badge/github-tomislavrupic%2Forch--or-181717?logo=github)](https://github.com/tomislavrupic/orch-or)

**Orch-OR diagnostic bridge for recoverability audits.**

This repo is a bounded computational scaffold for Orch-OR-adjacent timing, decoherence, and perturbation checks. It does not claim that Orch-OR is true, that consciousness is solved, or that toy microtubule models are biologically sufficient.

Layer used: Orch-OR diagnostic only.

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
- primary-source protofilament lattice geometry proxy
- discrete reduction events from explicit state menus
- source-locked reduction distinction tables
- critical and supportive decoherence estimate ranges
- anesthesia-style perturbation predictions
- Hameroff-facing benchmark summaries for time-crystal, Trp, and anesthesia diagnostics

The result is a timing audit, not an ontology.

For a traceable literature layer, see `src/orch_or/data.py` and `data/literature/`.

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
python3 examples/protofilament_lattice_sweep.py
python3 examples/hameroff_benchmark.py
python3 examples/reduction_events.py
python3 examples/reduction_sweep.py
python3 examples/reduction_distinction.py
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

- `toy`: code validation only.
- `mixed_assumption`: sourced structure plus explicit model assumptions.
- `critical_assumption`: stress-test values used to challenge the model.
- `supportive_contested`: values reported in supportive literature but still disputed.
- `model_assumption`: executable perturbation, not a clinical or biological claim.

Before any public scientific statement:

1. Replace or add parameter sets with source-traced values.
2. Record each source in `docs/source_register.md` and `docs/literature_queue.md`.
3. Run perturbation sweeps and preserve generated artifacts.
4. Publish only bounded metrics and keep downstream imports optional.

## Repository Map

- `src/orch_or/`: pure-stdlib diagnostic package.
- `examples/`: frozen outputs and one-command reproduction.
- `docs/`: equations, source register, paper matrix, discriminating tests, bridge contract, and roadmap.
- `notebooks/`: executable notebook entry points.
- `tests/`: dependency-free checks.

## Key Files

- [docs/equations.md](docs/equations.md): equations and approximations implemented in code.
- [docs/source_register.md](docs/source_register.md): source IDs used by executable rows.
- [docs/paper_matrix.md](docs/paper_matrix.md): what survives the primary-paper pass.
- [docs/discriminating_tests.md](docs/discriminating_tests.md): model comparison and test ideas.
- [docs/or_necessity.md](docs/or_necessity.md): the OR-on versus OR-off comparison artifact.
- [docs/published_values.md](docs/published_values.md): compact comparison against published values and ranges.
- [docs/orch_or_audit_contract.md](docs/orch_or_audit_contract.md): Orch-OR audit artifact contract.
- [notebooks/01_dp_thresholds.ipynb](notebooks/01_dp_thresholds.ipynb): threshold table walkthrough.
- [notebooks/02_decoherence_anesthesia.ipynb](notebooks/02_decoherence_anesthesia.ipynb): decoherence and anesthesia prediction walkthrough.
- [notebooks/03_microtubule_geometry.ipynb](notebooks/03_microtubule_geometry.ipynb): geometry and `E_G` model comparison walkthrough.
- [images/The_Quantum_Bioserver.pdf](images/The_Quantum_Bioserver.pdf): source poster / full-resolution figure.
- [images/The_Quantum_Bioserver_preview.png](images/The_Quantum_Bioserver_preview.png): GitHub preview image rendered from the PDF.

## Figure Preview

![The Quantum Bioserver preview](images/The_Quantum_Bioserver_preview.png)

## Minimal Orch-OR Audit

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
