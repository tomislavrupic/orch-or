#!/usr/bin/env python3
from __future__ import annotations

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "src"
if str(SRC) not in sys.path:
    sys.path.insert(0, str(SRC))

from orch_or.collapse import collapse_time_s, required_self_energy_j
from orch_or.parameters import DEFAULT_DP_MASS_MODELS, TARGET_COLLAPSE_TIMES_S
from orch_or.thresholds import threshold_rows


OUTPUT = Path(__file__).resolve().parent / "output" / "or_off_comparison.csv"


def rows() -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    threshold_lookup = {
        (row["mass_model"], row["target_tau_s"]): row for row in threshold_rows()
    }
    for model in DEFAULT_DP_MASS_MODELS:
        for target_tau_s in TARGET_COLLAPSE_TIMES_S:
            key = (model.name, f"{target_tau_s:.6e}")
            threshold_row = threshold_lookup[key]
            required_units = float(threshold_row["required_coherent_units"])
            unit_energy = float(threshold_row["unit_dp_energy_j"])
            classical_status = "no_or_collapse_window"
            or_tau = collapse_time_s(required_self_energy_j(target_tau_s))
            out.append(
                {
                    "mass_model": model.name,
                    "target_tau_s": f"{target_tau_s:.6e}",
                    "or_on_tau_s": f"{or_tau:.6e}",
                    "or_off_tau_s": "inf",
                    "required_coherent_units": f"{required_units:.6e}",
                    "unit_dp_energy_j": f"{unit_energy:.6e}",
                    "or_on_status": "finite_collapse_window",
                    "or_off_status": classical_status,
                    "necessity_note": (
                        "Without OR, the repo's collapse-timing result becomes undefined/infinite; "
                        "only microtubule photophysics and perturbation effects remain."
                    ),
                }
            )
    return out


def main() -> int:
    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    data = rows()
    with OUTPUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=[
                "mass_model",
                "target_tau_s",
                "or_on_tau_s",
                "or_off_tau_s",
                "required_coherent_units",
                "unit_dp_energy_j",
                "or_on_status",
                "or_off_status",
                "necessity_note",
            ],
            lineterminator="\n",
        )
        writer.writeheader()
        writer.writerows(data)
    print(f"Wrote {len(data)} rows to {OUTPUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
