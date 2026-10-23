# DARK-STATE K2 RESULTS — defect → coupling → spectral impurity

Executed 2026-08-22 against the frozen `DARK_STATE_K2_PREREG.md` on GitHub Actions run `32584405235`, artifact `9478650637` (`dark-state-k2-results`, SHA256 of uploaded zip `09d360ca98cf4e3c8fcf602919c10ec1624661d6631f1964f5f4ea70c387bb38`). Runner: `dark_state_k2.py`.

The first CI attempt (`32584371043`) did **not** execute K2: `actions/setup-python` rejected `cache: pip` because this repository has no `requirements.txt`/`pyproject.toml`. The cache declaration was removed; the failed run is plumbing provenance, not a scientific result.

## Gates

All preregistered execution gates pass on the second run:

- exact identity `g_DB = Delta_sigma/(2 sqrt(2))`: worst reported residual `1.776e-15`;
- exactly restored `H0=(H+PHP)/2`: dark→bright coupling at machine floor;
- PHYS-K11-1 `L_spec` reproduced on all four arm/pair combinations to the published three-decimal rounding;
- weak-breaking slopes of `Delta_sigma` and `g_DB`: 1.000 to numerical precision;
- weak-breaking slope of `L_spec`: 1.99945–2.00000 across all four arm/pair combinations.

Thus the pipeline reproduces the old observable before interpreting the new ones.

## K2.1 — measured matrices

| arm | pair | Delta_sigma | g_DB | L_spec | exact-H0 nearest bright gap |
|---|---|---:|---:|---:|---:|
| CUR-P2 | Pri/Prc | 3.76942 | 1.33269 | 0.054168 | 1.05432 |
| CUR-P2 | Str/Cir | 23.8100 | 8.41810 | 0.624736 | 0.237143 |
| CUR-SP | Pri/Prc | 3.98437 | 1.40869 | 0.411445 | 0.431114 |
| CUR-SP | Str/Cir | 20.9392 | 7.40313 | 0.663506 | 0.532858 |

Cross-pair ratios, Str/Cir over Pri/Prc:

| arm | Delta ratio | g_DB ratio | L_spec ratio | (L_spec/g_DB^2) ratio |
|---|---:|---:|---:|---:|
| CUR-P2 | 6.3166 | 6.3166 | 11.5333 | 0.2891 |
| CUR-SP | 5.2553 | 5.2553 | 1.6126 | 0.05839 |

### Frozen interpretation fork

**The mechanism is substrate-dependent.**

On CUR-P2, the Str/Cir symmetry-breaking dose is already 6.32× larger, so stronger breaking explains most of the direction. But the exact-symmetry dark level is also only 0.237 from its nearest bright eigenvalue versus 1.054 for Pri/Prc — roughly 4.45× tighter spectral placement. The measured leakage ratio (11.53×) therefore cannot be read as a simple copy of the defect ratio; spectral susceptibility matters before the observable saturates.

On CUR-SP, the breaking dose ratio is similarly large (5.26×) while the final leakage ratio is only 1.61×. There the large Str/Cir dose runs into spectral-impurity saturation/branch competition rather than amplifying the ratio. The PHYS-K11-1 sign replicates; the detailed mechanism does not. Per prereg, **no universal 11.5× mechanism is claimed**.

The raw `L_spec/g_DB^2` ratios are reported only descriptively. At the measured endpoint the Str/Cir arms are far outside the weak-breaking regime, so this quotient is not a perturbative susceptibility estimator.

## K2.2 — measured-direction continuation

The continuation is fixed by the measured odd component:

`H(s) = (H+PHP)/2 + s (H-PHP)/2`, with `s=0` exact symmetry and `s=1` the measured matrix.

### Weak-breaking tier

All four cases recover the scoped perturbative law:

- `Delta_sigma ~ s^1`;
- `g_DB ~ s^1`;
- `L_spec ~ s^2`.

Fitted low-s `L_spec` slopes:

- CUR-P2 Pri/Prc: `1.9999993`;
- CUR-P2 Str/Cir: `1.9997343`;
- CUR-SP Pri/Prc: `1.9999927`;
- CUR-SP Str/Cir: `1.9994523`.

This is the clean bridge to the standard symmetry-protected BIC → quasi-BIC pattern: linear opening of the forbidden coupling, quadratic opening of loss/impurity in the perturbative regime. It is a structural analogue, not a claim that the semantic graph is a photonic material.

### Nonperturbative continuation — the new diagnostic

The two twin directions diverge strongly away from small `s`.

**CUR-P2 Pri/Prc** remains on one smooth dark-like eigenbranch: `L_spec` is 0.000572 at `s=0.1`, 0.01418 at `s≈0.50`, and 0.05417 at `s=1`; its local log-slope only softens from ~2 to ~1.90 near the measured endpoint.

**CUR-P2 Str/Cir** leaves the perturbative regime rapidly: `L_spec` is 0.1909 at `s=0.1`, 0.4877 at `s≈0.20`, 0.6862 at `s≈0.316`, and ~0.70 around `s=0.5–0.7`. The eigenvalue carrying maximum dark overlap jumps between widely separated branches as `s` increases. At `s=1`, `L_spec` falls back to 0.6247 after this branch competition. A single quadratic extrapolation from `s≈0` is therefore invalid at the measured point.

**CUR-SP Pri/Prc** is intermediate: it bends continuously from the quadratic law, reaching `L_spec=0.4114` at `s=1`, with local slope falling to ~1.26 near the endpoint.

**CUR-SP Str/Cir** again enters branch competition early: 0.2315 at `s=0.1`, 0.5526 near `s=0.20`, 0.7523 near `s=0.316`, peaking around 0.76 near `s≈0.5`, then ending at 0.6635. Its maximizing dark-overlap eigenbranch also switches.

So the K2.2 stake fires in the informative direction: **Str/Cir exhibits strong nonquadratic spectral amplification/branch competition before the measured endpoint on both substrates; Pri/Prc does not do so nearly as sharply.** This is a mechanism candidate for why an otherwise exact twin dark mode becomes much less identifiable under the measured aspect breaking.

## What this buys

K2.3 is bought by the preregistered spend rule. The specific question is now narrow: if the bright sector is opened to a loss channel, does the same measured-direction continuation turn the exact twin dark state into a quasi-dark resonance whose linewidth is quadratic at small `s` and resonance-enhanced / nonperturbative in the Str/Cir direction?

This is worth testing because it distinguishes a merely spectral diagnostic from a dynamical lifetime effect, and it maps cleanly onto current dark→gray / bright→dark problems in open light–matter simulations.

## Fence

K2 is a model computation on measured semantic couplings. It does not establish a physical dark state in nature, and it does not establish a simulation-SOTA improvement. The latter still requires an external benchmark with a named resource saving at fixed observable error.
