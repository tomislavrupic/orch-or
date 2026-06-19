# Notebooks

Executable notebook path:

1. `01_dp_thresholds.ipynb`
   - derive and sweep `tau = hbar / E_G`
   - backsolve `E_G` for target timing bands
   - compare against traced parameter sets when available

2. `02_decoherence_anesthesia.ipynb`
   - compare target collapse times against critical and supportive decoherence ranges
   - run deterministic anesthesia perturbation predictions
   - preserve claim boundaries for every scenario

3. `03_microtubule_geometry.ipynb`
   - compare Gaussian, cylinder, and quadrature `E_G` approximations
   - sweep coherent domain size and dimer separation
   - keep the structural source trail explicit

4. `04_time_crystals_multiscale.ipynb`
   - model microtubules as time-crystal-like multiscale oscillators
   - sweep kHz to THz modes and beat-frequency proxies
   - keep the source placeholders explicit until the primary citations are locked

5. `05_trp_superradiance.ipynb`
   - sweep tryptophan network size and disorder
   - track bounded quantum-yield, superradiant gain, and anesthetic damping proxies
   - keep the source placeholders explicit until the primary citations are locked

Comparison note:
- `docs/published_values.md`
  - summarizes how the frozen outputs line up with the cited paper ranges
  - keeps the comparison explicit instead of burying it in narrative prose

Run notebooks from the repo root or keep the first cell's `sys.path` setup intact.
