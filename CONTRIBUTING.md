# Contributing

Thanks for helping keep this repo honest and useful.

## What To Add

- New literature rows in `data/literature/`
- New loaders or validation helpers in `src/orch_or/data.py`
- New bounded diagnostics in `src/orch_or/`
- New tests that exercise the executable spine

## How To Add A Literature Row

1. Add the source metadata to `data/literature/sources.json`.
2. Add a row to the relevant CSV.
3. Keep units, uncertainty, and notes explicit.
4. If the row feeds a diagnostic, add a test for the derived output.

## Before Opening A PR

- Run `python3 examples/quick_reproduce.py`
- Run `PYTHONPATH=src python3 -m unittest discover -s tests`
- Keep claim boundaries in the README and docs unchanged unless the new row really justifies the update
