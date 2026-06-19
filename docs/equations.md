# Equations

This repo implements a small diagnostic subset of Orch-OR-adjacent calculations.

## Objective Reduction Timing

```text
tau = hbar / E_G
```

`tau` is the timing proxy. `E_G` is the gravitational self-energy excess or ambiguity term. In this repo the equation is a timing diagnostic only.

## Diosi-Penrose Self-Energy Excess

The source-level expression is represented as:

```text
E_delta proportional to G double_integral [
  (rho_1(x) - rho_2(x)) (rho_1(x') - rho_2(x')) / |x - x'|
] d3x d3x'
```

The proportionality constant and short-distance regulator are model-sensitive. Point masses diverge, so executable rows use an explicit Gaussian regulator.

## Gaussian Regulator Approximation

For two equal Gaussian mass distributions of mass `m`, separation `d`, and smearing radius `R0`, the implemented diagnostic approximation is:

```text
E_delta = G m^2 [1/(sqrt(pi) R0) - erf(d/(2 R0))/d]
```

For very small `d/R0`, the code uses the leading Taylor term:

```text
E_delta ~= G m^2 d^2 / (12 sqrt(pi) R0^3)
```

This prevents numerical cancellation. It does not make the regulator biologically correct.

## Coordinate-Cloud Smearing Proxy

For a finite set of atomic-style coordinates `x_i` with masses `m_i`, the notebook-friendly proxy uses:

```text
x_com = sum(m_i x_i) / sum(m_i)
r_rms = sqrt(sum(m_i |x_i - x_com|^2) / sum(m_i))
```

The code then uses `r_rms` as a diagnostic smearing radius for Gaussian-regulated rows. This is a geometry proxy, not an atomistic force-field calculation.

## Timing Margin

```text
timing_margin_log10 = log10(decoherence_time / tau)
```

Positive margin:
The timing proxy fits inside the supplied decoherence/noise window.

Negative margin:
The supplied noise window closes before the timing proxy.

## Anesthesia Perturbation Proxy

Anesthesia rows scale the effective coherent energy by:

```text
effective_energy_multiplier = coherent_units_multiplier * coupling_multiplier
perturbed_tau = baseline_tau / effective_energy_multiplier
perturbed_decoherence_time = baseline_decoherence_time * decoherence_time_multiplier
```

These are perturbation predictions, not pharmacology, dosing, or clinical claims.
