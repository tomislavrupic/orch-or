"""Command-line interface for HAOS-OR."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from orch_or.anesthesia import FIELDNAMES as ANESTHESIA_FIELDNAMES
from orch_or.anesthesia import anesthesia_prediction_rows
from orch_or.collapse import collapse_time_s, required_self_energy_j
from orch_or.decoherence import FIELDNAMES as DECOHERENCE_FIELDNAMES
from orch_or.decoherence import decoherence_rows
from orch_or.haos_contract import build_summary
from orch_or.sweep import default_rows, write_rows
from orch_or.thresholds import FIELDNAMES as THRESHOLD_FIELDNAMES
from orch_or.thresholds import threshold_rows


def _cmd_collapse(args: argparse.Namespace) -> int:
    if args.eg_j is not None:
        print(json.dumps({"self_energy_j": args.eg_j, "collapse_time_s": collapse_time_s(args.eg_j)}))
        return 0
    if args.tau_s is not None:
        print(json.dumps({"target_tau_s": args.tau_s, "required_self_energy_j": required_self_energy_j(args.tau_s)}))
        return 0
    raise SystemExit("Provide --eg-j or --tau-s.")


def _cmd_sweep(args: argparse.Namespace) -> int:
    rows = default_rows()
    output = Path(args.output)
    write_rows(output, rows)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


def _cmd_thresholds(args: argparse.Namespace) -> int:
    rows = threshold_rows()
    output = Path(args.output)
    write_rows(output, rows, THRESHOLD_FIELDNAMES)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


def _cmd_decoherence(args: argparse.Namespace) -> int:
    rows = decoherence_rows()
    output = Path(args.output)
    write_rows(output, rows, DECOHERENCE_FIELDNAMES)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


def _cmd_anesthesia(args: argparse.Namespace) -> int:
    rows = anesthesia_prediction_rows()
    output = Path(args.output)
    write_rows(output, rows, ANESTHESIA_FIELDNAMES)
    print(f"Wrote {len(rows)} rows to {output}")
    return 0


def _cmd_reproduce(_args: argparse.Namespace) -> int:
    from orch_or.sweep import FIELDNAMES

    rows = default_rows()
    summary = build_summary(rows)
    print(json.dumps({"fieldnames": FIELDNAMES, "summary": summary, "rows": rows}, indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="HAOS-OR Orch-OR diagnostic bridge")
    subparsers = parser.add_subparsers(dest="command", required=True)

    collapse = subparsers.add_parser("collapse", help="compute tau=hbar/E_G or the inverse")
    collapse.add_argument("--eg-j", type=float, default=None, help="self-energy E_G in joules")
    collapse.add_argument("--tau-s", type=float, default=None, help="target collapse time in seconds")
    collapse.set_defaults(func=_cmd_collapse)

    sweep = subparsers.add_parser("sweep", help="write default timing sweep CSV")
    sweep.add_argument("--output", default="examples/output/collapse_time_table.csv")
    sweep.set_defaults(func=_cmd_sweep)

    thresholds = subparsers.add_parser("thresholds", help="write DP threshold table CSV")
    thresholds.add_argument("--output", default="examples/output/dp_threshold_table.csv")
    thresholds.set_defaults(func=_cmd_thresholds)

    decoherence = subparsers.add_parser("decoherence", help="write decoherence window table CSV")
    decoherence.add_argument("--output", default="examples/output/decoherence_estimate_table.csv")
    decoherence.set_defaults(func=_cmd_decoherence)

    anesthesia = subparsers.add_parser("anesthesia", help="write anesthesia prediction table CSV")
    anesthesia.add_argument("--output", default="examples/output/anesthesia_prediction_table.csv")
    anesthesia.set_defaults(func=_cmd_anesthesia)

    reproduce = subparsers.add_parser("reproduce", help="print deterministic diagnostic payload")
    reproduce.set_defaults(func=_cmd_reproduce)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return int(args.func(args))


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
