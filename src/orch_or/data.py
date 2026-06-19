"""Traceable literature data loaders for Orch-OR diagnostics.

This is a lightweight stdlib registry rather than a pandas-heavy layer.
It keeps raw values, provenance, and simple validation close together so
future notebooks can consume the same source-locked rows as the executable
timing spine.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass
from pathlib import Path

PACKAGE_ROOT = Path(__file__).resolve().parent
PROJECT_ROOT = PACKAGE_ROOT.parent.parent
DATA_ROOT = PROJECT_ROOT / "data"
LITERATURE_ROOT = DATA_ROOT / "literature"
PROCESSED_ROOT = DATA_ROOT / "processed"


@dataclass(frozen=True)
class LiteratureSource:
    short: str
    doi: str
    url: str


def _read_csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def _require_columns(rows: list[dict[str, str]], required: tuple[str, ...], path: Path) -> None:
    if not rows:
        raise ValueError(f"{path} is empty")
    missing = [column for column in required if column not in rows[0]]
    if missing:
        raise ValueError(f"{path} is missing columns: {missing}")


class LiteratureRegistry:
    """Central place for curated literature values with provenance."""

    def __init__(self) -> None:
        self.sources = self._load_sources()

    def _load_sources(self) -> dict[str, LiteratureSource]:
        path = LITERATURE_ROOT / "sources.json"
        raw = json.loads(path.read_text(encoding="utf-8"))
        return {
            source_id: LiteratureSource(
                short=record["short"],
                doi=record["doi"],
                url=record["url"],
            )
            for source_id, record in raw.items()
        }

    def load_tubulin_geometry(self) -> list[dict[str, str]]:
        rows = _read_csv_rows(LITERATURE_ROOT / "tubulin_geometry.csv")
        _require_columns(rows, ("parameter", "value", "uncertainty", "unit", "source_id", "notes"), LITERATURE_ROOT / "tubulin_geometry.csv")
        for row in rows:
            row["source_short"] = self.sources.get(row["source_id"], LiteratureSource("unknown", "", "")).short
        return rows

    def load_resonance_frequencies(self) -> list[dict[str, str]]:
        rows = _read_csv_rows(LITERATURE_ROOT / "resonance_frequencies.csv")
        _require_columns(rows, ("frequency_hz", "conductance", "source_id", "notes"), LITERATURE_ROOT / "resonance_frequencies.csv")
        for row in rows:
            frequency = float(row["frequency_hz"])
            if frequency < 1.0e2:
                row["scale"] = "sub-hz"
            elif frequency < 1.0e5:
                row["scale"] = "Hz"
            elif frequency < 1.0e8:
                row["scale"] = "kHz"
            elif frequency < 1.0e10:
                row["scale"] = "MHz"
            elif frequency < 1.0e12:
                row["scale"] = "GHz"
            else:
                row["scale"] = "THz"
            row["source_short"] = self.sources.get(row["source_id"], LiteratureSource("unknown", "", "")).short
        return rows

    def load_decoherence(self) -> list[dict[str, str]]:
        rows = _read_csv_rows(LITERATURE_ROOT / "decoherence_estimates.csv")
        _require_columns(rows, ("estimate", "lower_s", "upper_s", "source_id", "notes"), LITERATURE_ROOT / "decoherence_estimates.csv")
        for row in rows:
            row["source_short"] = self.sources.get(row["source_id"], LiteratureSource("unknown", "", "")).short
        return rows

    def load_anesthesia(self) -> list[dict[str, str]]:
        rows = _read_csv_rows(LITERATURE_ROOT / "anesthesia_effects.csv")
        _require_columns(rows, ("perturbation", "value", "unit", "source_id", "notes"), LITERATURE_ROOT / "anesthesia_effects.csv")
        for row in rows:
            row["source_short"] = self.sources.get(row["source_id"], LiteratureSource("unknown", "", "")).short
        return rows

    def validate(self) -> None:
        self.load_tubulin_geometry()
        self.load_resonance_frequencies()
        self.load_decoherence()
        self.load_anesthesia()


registry = LiteratureRegistry()
