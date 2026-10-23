# DARK-STATE K2.3 RESULTS — quasi-dark linewidth under a lossy bright sector

Executed 2026-08-22 against frozen `DARK_STATE_K23_PREREG.md` on GitHub Actions run `32584589179`, runner `dark_state_k23.py`. Artifact: `9478697987` (`dark-state-k23-results`), uploaded ZIP SHA256 `2f9b3cfff7fe29958a112ebbde2239d1bbad871ad67329f69f09f551930831ea`.

## Verdict

**O1–O3 all PASS on every arm, pair, and kappa.** The independent absorbing-sink Lindblad cross-check also passes at machine precision.

This establishes a controlled model window in which the exact twin dark state turns into a quasi-dark resonance whose linewidth is predicted, without fitting, from the symmetry-restored bright spectrum and the measured symmetry-breaking operator.

## Dye / convention gates

- O1, exact protection at `s=0`: `Gamma` at numerical floor for all 20 `(arm,pair,kappa)` families.
- Lindblad absorbing-sink vs non-Hermitian system-population equality, worst absolute discrepancy across the four pair/arm checks: `8.66e-15`.
- O2 weak linewidth slopes: all within `2.0000 ± 0.0003`, far inside the frozen `2 ± 0.01` band.
- O3 parameter-free coefficient prediction: median absolute fractional errors range from `2.44e-7` to `4.56e-6`, far inside the 1% PASS bar.

The coefficient test is the strongest result here: the curve was not merely fit to `s^2`; its coefficient was computed first from

`C(kappa) = sum_j |<b_j|Vodd|d>|^2 kappa / ((Ed-Ej)^2 + (kappa/2)^2)`.

## Predicted weak-linewidth coefficients C(kappa)

### CUR-P2

| pair | k=0.1 | 0.3 | 1 | 3 | 10 |
|---|---:|---:|---:|---:|---:|
| Pri/Prc | 0.00572 | 0.01705 | 0.05316 | 0.11972 | 0.22014 |
| Str/Cir | 2.32977 | 6.76459 | 17.5487 | **25.2195** | 20.4702 |

### CUR-SP

| pair | k=0.1 | 0.3 | 1 | 3 | 10 |
|---|---:|---:|---:|---:|---:|
| Pri/Prc | 0.06660 | 0.18316 | 0.33646 | 0.35169 | 0.35539 |
| Str/Cir | 3.22216 | 9.26355 | 21.4220 | **22.1213** | 14.6738 |

The Str/Cir families show a resolved turnover between resonance enhancement and strong-loss/Zeno suppression: both peak near `kappa≈3` on this coarse frozen grid and decline by `kappa=10`. Pri/Prc does not show the same turnover within the grid on CUR-P2 and is nearly plateaued by `kappa=3–10` on CUR-SP. This is consistent with the K2 spectral-denominator distinction, not a new fitted parameter.

## Measured-endpoint (`s=1`) behavior

At `kappa=1`:

| arm | pair | Gamma(s=1) | dark overlap of selected resonance | first branch-ambiguous s |
|---|---|---:|---:|---:|
| CUR-P2 | Pri/Prc | 0.05080 | 0.9492 | none |
| CUR-P2 | Str/Cir | 0.62463 | 0.3754 | 0.3 |
| CUR-SP | Pri/Prc | 0.36793 | 0.6321 | none |
| CUR-SP | Str/Cir | 0.66341 | 0.3366 | 0.3 |

Thus K2's branch-competition asymmetry survives opening the bright sector. Both Str/Cir arms become branch-ambiguous by `s=0.3` at moderate loss, while neither Pri/Prc arm becomes ambiguous anywhere on the frozen grid.

At the measured endpoint the weak perturbative formula is not used as a fit. The reported linewidth is the full eigenvalue result.

## Exact relation between dark weight and linewidth in this open-channel model

There is a useful algebraic identity beyond the preregistered perturbative coefficient. For any normalized right eigenvector `|psi>` of

`H_eff = H - i (kappa/2) Q_B`, with `Q_B = I - |d><d|`,

multiplying the eigenvalue equation by `<psi|` and taking imaginary parts gives

`Gamma = -2 Im(lambda) = kappa <psi|Q_B|psi>`

and therefore

`Gamma = kappa (1 - |<d|psi>|^2)`.

So in this deliberately uniform bright-loss model, the resonance linewidth is exactly the bright weight of that resonance times the loss rate. In the `kappa→0` limit on a continuously tracked branch, this reduces directly to the K2 spectral-impurity observable times `kappa`.

This identity should be treated as a model theorem candidate. It is not a statement about arbitrary Lindblad baths or mode-dependent continuum couplings.

## Physics / chemistry reading

The controlled tier matches established symmetry-protected BIC → quasi-BIC structure: exact symmetry gives zero radiative width, the forbidden coupling opens linearly, and the linewidth opens quadratically. That physical mechanism is prior art; the contribution here is the explicit defect→coupling→linewidth diagnostic and its use as a compiler criterion.

The molecular-polariton opportunity remains stronger than the photonic analogy. Current MPS–HEOM work finds that disorder and phonon timescales activate dark/gray degrees of freedom, with bright→dark transfer controlling the system size needed for thermodynamic convergence. K2.3 supplies a concrete quantity to test in such a solver: whether the disorder-induced bright↔dark coupling has a compressible low-rank / low-reachability structure before the full dark manifold becomes active.

## What is and is not bought

**Bought:** an external computational benchmark of a soft-symmetry reduction, because O1–O3 pass and a controlled window exists.

**Not bought:** a simulation-SOTA claim. Exact permutation reductions already exist (e.g. PIQS for Lindblad ensembles, CUT-E/d-CUT-E for collective molecular polaritons), and current MPS–HEOM already achieves linear-in-N tensor-network propagation under dynamic disorder. The next contribution has to live specifically in the gap between exact symmetry methods and fully symmetry-broken non-Markovian simulation.

The benchmark must therefore compare against those baselines and report a named resource at fixed physical-observable error.
