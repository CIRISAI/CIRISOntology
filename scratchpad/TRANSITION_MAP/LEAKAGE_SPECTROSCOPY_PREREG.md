# DARK-STATE LEAKAGE SPECTROSCOPY / SUM RULES — PREREG

Frozen 2026-08-22 after K2.2 and K2.3, before any extended-loss sweep or sum-rule comparison is executed.

## Purpose

K2.2 separates structural defect (`g_DB`) from closed-system spectral susceptibility (`L_spec`). K2.3 shows that opening the bright sector produces a parameter-free second-order linewidth

`C(kappa) = sum_j mu_j kappa / (Delta_j^2 + (kappa/2)^2)`,

where `mu_j=|<b_j|V_odd|d>|^2`, `Delta_j=E_d-E_j`, and the numerical dark linewidth satisfies `Gamma ~ s^2 C` at weak breaking.

The same function is the Lorentzian/Poisson transform of the coupling-weighted bright spectral measure. The question is whether its two loss limits quantitatively unify the three diagnostics already measured: structural coupling, spectral impurity, and open-system leakage.

No novelty is claimed for resolvent/Lorentzian spectroscopy, Fermi-golden-rule broadening, or quantum-Zeno asymptotics. The potentially useful contribution is the explicit diagnostic triangle on the measured K11 twin substrates.

## Exact/perturbative targets

Because `sum_j mu_j = g_DB^2`, the high-loss limit is

`lim_{kappa->infty} kappa C(kappa) = 4 g_DB^2`.

If every coupled bright detuning is nonzero, the low-loss limit is

`lim_{kappa->0} C(kappa)/kappa = chi_2 := sum_j mu_j/Delta_j^2`.

For a nondegenerate dark eigenbranch, ordinary eigenvector perturbation theory gives

`L_spec(s) = s^2 chi_2 + O(s^3)`.

Thus the frozen triangle is:

- high-loss linewidth tail -> structural dark/bright coupling `g_DB^2`;
- low-loss linewidth slope -> closed-system spectral susceptibility `chi_2`;
- intermediate kappa shape -> detuning distribution / resonance structure.

## Frozen substrates

Use the same CUR-P2 and CUR-SP coupling matrices, both twin pairs, restored symmetric H0 and measured odd perturbation V_odd as K2.2/K2.3.

Weak breaking `s=1e-4` and `3e-4` for numerical non-Hermitian linewidth extraction. Loss grid:

`kappa = 10^x`, x from -4 to 4 in steps of 0.25.

Attach the same bright-sector loss convention as K2.3. Track the dark branch continuously from s=0 by maximal overlap, with ambiguity reported rather than repaired.

## Gates

L1. Direct spectral sum `sum mu_j` agrees with `g_DB^2` to <1e-10 relative/absolute floor.

L2. The analytic C(kappa) reproduces numerical `Gamma/s^2` within 1% in the same weak-breaking regime wherever branch overlap >=0.99.

L3. K2.2 finite-difference coefficient `L_spec(s)/s^2` at s=1e-4 agrees with `chi_2` within 1% when the same nondegenerate branch is used.

Failure of a gate localizes a convention/perturbation issue and voids the corresponding bridge statement.

## Scientific stakes

P1 — high-loss sum rule: at kappa=1e4, `kappa Gamma/s^2` is within 1% of `4 g_DB^2` on every substrate/pair.

P2 — low-loss sum rule: at kappa=1e-4, `Gamma/(s^2 kappa)` is within 1% of `chi_2` on every nondegenerate arm.

P3 — turnover localization: define kappa_peak maximizing analytic C. If one bright mode carries >=70% of the weighted susceptibility `mu_j/Delta_j^2`, then kappa_peak is within 25% of `2|Delta_dom|`. Otherwise report the turnover as genuinely multimode; do not force a single-detuning interpretation.

P4 — substrate diagnosis: compare the ratio `chi_2/g_DB^2` with the measured K2.2 leakage asymmetry. If CUR-P2 Str/Cir has much larger `chi_2/g_DB^2` than Pri/Prc while CUR-SP does not, the open-loss spectrum recovers the preregistered substrate-dependent resonance mechanism independently of the s=1 spectral impurity.

## Why this matters

If L1-L3/P1-P4 pass, the loss sweep is a controlled spectroscopy of *why* a nominal dark state leaks:

- total symmetry-breaking strength is in the high-loss tail;
- resonant susceptibility is in the low-loss slope;
- spectral structure is in the crossover.

That is a physics diagnostic even if it buys zero simulation speedup. It also gives a concrete falsifiable bridge to experiments/simulations where radiative or dissipative linewidth can be tuned while structural disorder remains fixed.

## Fence

This is a perturbative/open-system diagnostic, not a claim of new non-Hermitian physics. Any experimental relevance requires a platform where the loss channel and disorder can be varied independently and the effective bright-sector loss model is justified.
