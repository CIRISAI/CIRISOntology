# DARK-STATE LEAKAGE SPECTROSCOPY — FIRST RESULTS

Executed 2026-08-22 against frozen `LEAKAGE_SPECTROSCOPY_PREREG.md` on GitHub Actions run `32586329938`.

The numerical screen itself completed; the workflow gate failed at L2 and therefore the artifact upload was skipped. The failure is preserved here rather than rerun away.

## Exact / closed-system pieces

L1 passes:

`sum_j mu_j = g_DB^2`

with worst absolute discrepancy `8.53e-14`.

L3 passes strongly: the K2.2 weak-breaking spectral-impurity coefficient `L_spec(s)/s^2` at s=1e-4 agrees with

`chi2 = sum_j mu_j/Delta_j^2`

to worst fractional error `6.79e-7`.

This makes the low-loss/closed-system side of the diagnostic triangle quantitative.

## Low-loss open-system sum rule

Frozen P2 passes on every substrate/pair at kappa=1e-4 using s=3e-4. The numerical ratios

`[Gamma/(s^2 kappa)] / chi2`

are:

- CUR-P2 Pri/Prc: `0.99999986`;
- CUR-P2 Str/Cir: `0.99999798`;
- CUR-SP Pri/Prc: `0.99999996`;
- CUR-SP Str/Cir: `0.99999583`.

Thus the open-system linewidth slope at weak loss directly recovers the same spectral susceptibility that controls closed-system eigenvector impurity.

## High-loss numerical issue

The all-kappa L2 gate fails: worst `|Gamma/(s^2 C)-1| = 0.371` among cells with dark overlap >=0.99.

At the specific frozen high-loss endpoint kappa=1e4, s=3e-4, the ratios to the high-loss sum rule `4 g_DB^2` are:

- CUR-P2 Pri/Prc: `1.04097`;
- CUR-P2 Str/Cir: `1.00081`;
- CUR-SP Pri/Prc: `1.02690`;
- CUR-SP Str/Cir: `1.00091`.

The error is strongly anticorrelated with coupling magnitude: the Str/Cir arms, with g_DB^2 tens of times larger, are already at ~0.1%, while the weak Pri/Prc widths are only O(1e-12) and show percent-level error in a double-precision eigenvalue imaginary part. This strongly suggests a numerical-resolution problem, but that is a diagnosis to test, not a retroactive pass.

`LEAKAGE_SPECTROSCOPY_HP_PREREG.md` freezes a high-precision check. The original L2 gate remains failed regardless of that outcome.

## Turnover stake: failed for a useful reason

P3, the single-dominant-detuning turnover rule, fails.

The coupling-weighted low-loss susceptibility can be highly concentrated in one mode (CUR-SP Pri/Prc `86.6%`; CUR-SP Str/Cir `70.8%`) while the maximum of the full Lorentzian sum `C(kappa)` is not located within the frozen 25% window around `2|Delta_dom|`.

This is a substantive correction: **dominance of the low-loss susceptibility does not imply dominance of the entire loss crossover.** Modes with larger detuning can be relatively unimportant at kappa->0 but gain weight as the Lorentzian broadens. The intermediate-loss curve is genuinely a probe of the full coupling-weighted bright spectrum.

## Substrate-dependent resonance diagnosis

P4 passes.

The normalized susceptibility `chi2/g_DB^2` is:

| substrate | Pri/Prc | Str/Cir | Str/Cir / Pri/Prc |
|---|---:|---:|---:|
| CUR-P2 | 0.03224 | 0.33024 | 10.24x |
| CUR-SP | 0.33954 | 0.59116 | 1.74x |

This independently recovers the K2.2 mechanism fork. On CUR-P2, Structure/Circumstances is dramatically more spectrally susceptible per unit structural breaking; on CUR-SP, that extra resonance amplification is much weaker. The measured leakage ordering replicates, but its mechanism is substrate-dependent.

## Current physical reading

The useful triangle is already partly established:

- structural breaking: `g_DB^2 = sum mu_j`;
- closed spectral susceptibility: `chi2 = sum mu_j/Delta_j^2`;
- weak-loss open linewidth: `Gamma/(s^2 kappa) -> chi2`.

The high-loss numerical endpoint still requires a precision audit. The intermediate-loss crossover should be treated as full spectral-measure information rather than summarized by one detuning.

## Fence

The original failed L2/P1/P3 outcomes remain part of the record. Any high-precision follow-up diagnoses numerical conditioning only; it does not erase the failed double-precision gate or revive the failed single-mode turnover hypothesis.
