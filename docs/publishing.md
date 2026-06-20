# Publishing Checklist

This repo is ready for a GitHub-side release, but the final click still happens on GitHub itself.

## Ready Now

- `v0.1.0` tag exists locally and on `main`
- `CHANGELOG.md` captures the release summary
- `RELEASE_v0.1.md` lists the assets to attach
- `release_assets_v0.1.txt` enumerates the frozen files
- CI runs `examples/quick_reproduce.py` and the full test suite

## GitHub Actions To Finish

1. Create a GitHub Release for `v0.1.0`.
2. Upload the files listed in `release_assets_v0.1.txt`.
3. Attach `CHANGELOG.md` and `RELEASE_v0.1.md` as release notes if desired.
4. Set the repository social preview to `images/The_Quantum_Bioserver_preview.png`.
5. After the release exists, enable the Zenodo DOI badge.
6. Share a short dashboard screenshot or CLI capture in the repo README or social post.

## Why This Matters

These steps convert the local reproducible state into something a visitor can star, fork, and cite without hunting for context.
