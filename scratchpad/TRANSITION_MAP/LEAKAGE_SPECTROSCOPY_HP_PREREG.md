# LEAKAGE SPECTROSCOPY HIGH-PRECISION DIAGNOSTIC — PREREG

Frozen 2026-08-22 after the original double-precision L2/P1 gates failed, before any high-precision output is computed.

## Purpose

The original spectroscopy run showed percent-to-tens-of-percent errors only where the predicted weak dark linewidth becomes comparable to double-precision eigenvalue-imaginary-part resolution. The strong-coupling Str/Cir arms already satisfy the high-loss sum rule to ~0.1%, while weak Pri/Prc arms miss by 2.7–4.1% at kappa=1e4 and the all-grid L2 maximum is 37%.

This diagnostic asks whether those failures are numerical conditioning or real breakdown. It does **not** retroactively change the failed original gates.

## Frozen calculation

Use exactly the same CUR-P2/CUR-SP matrices, restored H0, V_odd, dark vector and bright loss projector as `LEAKAGE_SPECTROSCOPY_PREREG.md`.

Evaluate only the high-loss region

`kappa in {100, 316.22776601683796, 1000, 3162.2776601683795, 10000}`

and weak breaking `s in {1e-4, 3e-4}`.

Use `mpmath` at 80 decimal digits to diagonalize

`H_eff = H0 + s V_odd - i kappa Q_B/2`.

In this high-loss regime, identify the quasi-dark eigenvalue as the eigenvalue with imaginary part closest to zero; cross-check that its real part remains near Ed and that the next-slowest mode is separated by O(kappa).

Compare

`Gamma_hp = -2 Im(lambda_dark)`

with the same analytic second-order coefficient C(kappa).

## Stakes

HP1. For every pair/substrate at kappa=1e4 and s=3e-4, `|Gamma_hp/(s^2 C)-1| <= 0.01`.

HP2. Across all frozen high-loss cells, median high-precision coefficient error is at least 10x smaller than the corresponding double-precision error from the same matrix/eigenvalue convention.

HP3. For cells where double precision already has <0.5% error, high precision changes Gamma by <0.5%. This checks that the high-precision branch selector is not simply choosing a different mode.

HP4. The analytic finite-kappa high-loss ratio `kappa*C/(4 g_DB^2)` is reported separately. Any remaining deviation of that ratio from 1 is finite-kappa asymptotics, not numerical extraction error.

## Interpretation

- HP1-HP3 pass: original L2/P1 failure is a double-precision conditioning failure at tiny linewidth, while the high-loss physical sum rule survives. The original gate remains recorded as failed.
- HP1 fails with a well-resolved quasi-dark root: the high-loss second-order asymptotic itself fails under the frozen conditions.
- HP3 fails: branch identification is suspect; no physical conclusion.

## Fence

This is a numerical-conditioning audit, not an additional free chance to tune the theory. No kappa, s, precision, branch rule or tolerance may be changed after outputs are inspected.
