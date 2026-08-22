# DARK-STATE K2 PREREG — defect → coupling → spectral impurity

Frozen on 2026-08-22 before the K2 analysis is executed. This is a follow-on to PHYS-K11-1 and `Core/DarkState.lean`. It does **not** alter PHYS-K11-1's stakes or reinterpret its reported leakage after seeing K2.

## Question

PHYS-K11-1 measured the twin dark-state spectral impurity

`L_spec = 1 - max_j |<v_j|d>|^2`

and found the staked ordering Structure/Circumstances > Priorities/Process on both CUR-P2 and CUR-SP. K2 asks *why*. We separate two ingredients that PHYS-K11-1 did not measure:

1. **symmetry-breaking dose** `Delta_sigma = ||H - P_sigma H P_sigma||_F`;
2. **instantaneous dark→bright coupling** `g_DB = ||(I-dd^T) H d||_2`;
3. the already-defined **spectral impurity** `L_spec`.

For a single transposition of a real symmetric H, the exact algebra predicts

`g_DB = Delta_sigma / (2 sqrt(2))`.

This identity is a pipeline/dye-test tier, not a corpus prediction.

## Inputs — frozen to the PHYS-K11-1 artifacts

- primary: `panel2_validation.jsonl` + `plane_corpus/corpus_full.jsonl`;
- replicate: `plane_corpus/full_judgments.jsonl` + the same corpus targets;
- coupling construction copied byte-for-byte in logic from `phys_k11.py`: row-stochastic confusion matrix, symmetrize `(M+M.T)/2`, zero diagonal, PHYS-K11-1 A2 mean-channel normalization;
- twin pairs exactly as PHYS-K11-1: Priorities/Process and Structure/Circumstances.

No matrix is reconstructed from published summary numbers.

## K2.1 — measured matrices

For each arm and twin pair report:

- `Delta_sigma` and `Delta_sigma/||H||_F`;
- `g_DB`;
- identity residual `|g_DB - Delta_sigma/(2 sqrt(2))|`;
- `L_spec` (must reproduce PHYS-K11-1 to rounding; otherwise VOID);
- dark expectation `E_d = d^T H d`;
- minimum distance from `E_d` to the eigenvalues of the P-even bright block;
- `L_spec/g_DB^2` as a **descriptive susceptibility only**, never as a perturbative estimate when `L_spec` is large.

### Staked interpretation fork

- If the Str/Cir : Pri/Prc ratio in `Delta_sigma` is comparable to the ratio in `L_spec`, the 11.5× primary contrast is mainly a stronger symmetry-breaking dose.
- If the `Delta_sigma` ratio is materially smaller while `L_spec` is much larger, spectral placement / near-resonance amplification is doing substantial work.
- If CUR-P2 and CUR-SP disagree on that mechanism while preserving the PHYS-K11 sign, report the mechanism as **substrate-dependent**, not universal.

No numeric band for “comparable” is staked because the two observables have different perturbative order. The raw ratios are the result.

## K2.2 — measured-direction symmetry-breaking continuation

For each arm/pair define, from the **measured H itself**,

`H0 = (H + P H P)/2`,
`Vodd = (H - P H P)/2`,
`H(s) = H0 + s Vodd`.

Thus `s=0` restores exactly the chosen twin symmetry and `s=1` is the measured matrix. This avoids choosing a random perturbation direction after seeing the answer.

Sweep `s` on a fixed log grid from `1e-4` to `1`, plus `0`. Report:

- exact dark residual at `s=0`;
- `Delta_sigma(s)`, `g_DB(s)`, `L_spec(s)`;
- weak-breaking log slopes over the lowest decade(s) with non-floor values;
- the minimum bright-block energy denominator at `s=0`;
- whether `L_spec(s)` remains approximately quadratic or bends strongly before `s=1`;
- any avoided-crossing / eigenvector-switch point visible as a sharp change in the identity of the eigenvector maximizing dark overlap.

### Stakes

1. `Delta_sigma` and `g_DB` slope = 1 to numerical precision; failure is an implementation defect.
2. `L_spec` weak-breaking slope should approach 2 **only when the nearest bright denominator is nonzero and the overlap remains on one analytic eigenbranch**. This is a scoped perturbative expectation, not a universal theorem.
3. If Str/Cir develops strong nonquadratic amplification before `s=1` while Pri/Prc does not, that is the specific mechanism candidate for the PHYS-K11 leakage asymmetry.

## Anti-hype gate

K2 is about reduction diagnostics. It is **not** evidence of simulation SOTA. A later soft-symmetry compiler earns that phrase only on an external benchmark if it reduces a named computational resource (Krylov dimension, tensor-network bond dimension, HEOM auxiliary count, memory, or wall time) at fixed observable error.

## Spend rule

K2.3 (open-system / quasi-BIC loss) is bought only if K2.2 cleanly resolves the defect→leakage mechanism or identifies a specific resonance regime worth testing. External polariton benchmarking comes only after K2.3.
