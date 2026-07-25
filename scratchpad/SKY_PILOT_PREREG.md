# PRE-REGISTRATION — the bispectrum bridge, simulation pilot

Frozen and committed **before** `sky_pilot.py` existed and before any number was computed.
Scratchpad only: no Lean file, no `Stance.lean`, no audit, `lake` never run. **No real survey
data is touched anywhere in this experiment, and nothing here will be a claim about the sky.**

---

## 0. SCOPE, FIRST AND LOAD-BEARING

This is a **simulation pilot**. Every field in it is one I generate, with a non-Gaussianity I
put there myself. The question is whether a proposed *estimator bridge* — from the whole-only
order-3 share to the three-point function — is usable, and where it breaks, on cases whose
truth is known analytically.

It establishes **nothing about nature**, nothing about the `wild-share` open claim, and
nothing about any cosmological observable. If the bridge holds, the deliverable is a **design**
— which survey, which scales, which systematic dominates — not a result.

---

## 1. THE PROPOSAL BEING TESTED, AND TWO PLACES I THINK IT IS WRONG

The brief proposes: (i) a Gaussian field has zero whole-only share, so the share measures
non-Gaussianity (the known quantity **negentropy**; Comon 1994, Hyvärinen–Oja 2000 — credited,
not claimed); (ii) at weak coupling the share goes as the **square** of the connected
three-point function, so it is computable from the **bispectrum**, sidestepping entropy
estimation; (iii) a **lognormal** field, having known skewness, is the positive control.

I accept (i), sharpen it, and **derive (ii) explicitly** below. **I reject (iii) in advance**,
by a theorem, and I stake that rejection here as the pilot's sharpest pre-registered
prediction. I also reject the brief's implicit assumption that discretisation is a nuisance to
be bounded rather than a term with a sign and a parity rule.

Everything in §2 is derivation, done before any code was written. It is not a result; it is
what fixes the predictions in §4 so they can be wrong.

---

## 2. DERIVATIONS (all analytic, all before computing)

Notation. Three real variables `X = (X₁,X₂,X₃)` with density `p`, covariance `C`, connected
third cumulants `ζ_abc = cum(X_a,X_b,X_c)` for `a,b,c ∈ {1,2,3}` **including repeats**. `φ_C`
is the Gaussian with the same mean and covariance. `⟨·,·⟩` is the `L²(φ_C)` inner product. The
share is the repository's: `share p = sup{H(q) : q carries p's three pair marginals} − H(p)`
(`Core/Share.lean`), i.e. the order-3 connected information `I_C⁽³⁾`.

### 2.1 The variational form at second order

Write `p = φ_C(1+u)`. Because `p` and `φ_C` share moments through order 2,
`⟨u,1⟩ = ⟨u,x_i⟩ = ⟨u,x_i x_j⟩ = 0`, and

    H(p) = H(φ_C) − ½‖u‖² + O(u³).                                        (2.1)

Let `W ⊂ L²(φ_C)` be the closed span of all functions of **at most two** coordinates.
A competitor `q = φ_C(1+v)` carries `p`'s pair marginals iff `⟨v,g⟩ = ⟨u,g⟩` for every
`g ∈ W`, i.e. `P_W v = P_W u`. By (2.1), maximising `H(q)` is minimising `‖v‖²`, so the
maximiser is `v = P_W u`. Therefore

    **I_C⁽³⁾ = ½ ‖P_{W^⊥} u‖² + O(u³).**                                   (2.2)

The share is the squared length of the part of the state that no pair can see. This is exact
at second order and is the engine of everything below.

### 2.2 The bridge, derived

Grade `L²(φ_C)` by Hermite degree; the grading is orthogonal and `W` is graded (the degree-`d`
part of `L²(x_i,x_j)` is orthogonal to every ambient polynomial of degree `< d`, because
`E[x_k^m | x_i,x_j]` is a degree-`m` polynomial in `x_i,x_j`). At leading order in the
non-Gaussianity `u` is pure degree 3: `u₃ = (1/3!) ζ_abc h^{abc}`, with the tensor Hermites
`h^{abc}` dual to the monomials, `⟨h^{abc}, x_l x_m x_n⟩ = Σ_{σ∈S₃} δ^a_{σ(l)}δ^b_{σ(m)}δ^c_{σ(n)}`,
so `⟨u₃, x_l x_m x_n⟩ = ζ_lmn`.

`dim(P₃) = 10`; the three pairs contribute `3·4 − 3 = 9` to `W ∩ P₃` (four degree-3 Hermites
per pair, the three single-variable ones shared). So **`W^⊥ ∩ P₃` is one-dimensional**, and it
is spanned by `h^{123}`: duality gives `⟨h^{123}, x_l x_m x_n⟩ = 0` whenever `{l,m,n}` omits an
index, which is exactly the spanning set of `W ∩ P₃`. With `A := C^{-1}`,

    ⟨u₃, h^{123}⟩ = A_{1a}A_{2b}A_{3c} ζ_abc ,      ‖h^{123}‖² = perm(A).

**THE BRIDGE:**

    **I_C⁽³⁾ = ½ · [ Σ_abc (C⁻¹)_{1a}(C⁻¹)_{2b}(C⁻¹)_{3c} ζ_abc ]² / perm(C⁻¹) + O(ζ³)**   (B)

with `perm` the permanent. Quadratic in the three-point function, as the brief expects — but
**contracted with `C⁻¹` and summed over coincident indices**, which is not what "the
bispectrum" delivers, and that difference is the whole story.

Two checks fixed in advance:

* `C = I` ⟹ `I_C⁽³⁾ = ½ ζ₁₂₃²`.
* Explicit three-body coupling `p ∝ exp(K s₁s₂s₃)` on ±1 spins: pair marginals uniform so
  `C = I`, all repeated-index cumulants vanish, `ζ₁₂₃ = tanh K`, so (B) gives `½tanh²K ≈ ½K²`.
  The exact closed form is `K tanh K − ln cosh K` (`ISING_FIELD_RESULTS.md` §2), whose
  expansion is `K²/2`. **These must agree**; at `K = 0.9` the exact value is `0.284836`.

### 2.3 THE POINTWISE-TRANSFORM THEOREM — why the lognormal is a NULL, not a control

**Theorem.** Let `T₁,T₂,T₃` be strictly monotone maps and `Y_i = T_i(X_i)`. Then
`I_C⁽³⁾(Y) = I_C⁽³⁾(X)` exactly, at every amplitude.

*Proof.* `T = T₁×T₂×T₃` acts coordinatewise, so `q` carries `p`'s pair marginals iff `T_*q`
carries `T_*p`'s. Differential entropy transforms as `H(T_*q) = H(q) + Σ_i E_q[ln|T_i′|]`, and
the correction depends only on the **one**-dimensional marginals, which every member of the
envelope shares. The envelope is therefore translated by one constant and the state's entropy
by the same constant; the difference is unchanged. ∎ For discrete readings the same holds
provided bin edges are carried along — i.e. **quantile binning is transform-invariant**.

**Corollary, staked.** A **lognormal field is a per-cell monotone transform of a Gaussian
field, so its whole-only share is EXACTLY ZERO** — at every triple of positions, every
smoothing scale, every amplitude — **while its bispectrum is large and is the standard
analytic non-Gaussian mock.** The brief's positive control is a second null, and a far sharper
one than the Gaussian, because it separates "has a bispectrum" from "has whole-only share".

This is the continuous-field form of a trap already recorded in the repository:
`Core/SignSymmetry.lean` warns that "a large three-point correlation function is NOT order-3
structure … the correlator is a moment; the share is what the pair marginals cannot
reconstruct."

**Consistency of (B) with the theorem, verified analytically before committing.** For the weak
pointwise quadratic transform `X_i = g_i + ½(g_i²−σ²)` one has
`ζ_abc = C_ab C_ac + C_ab C_bc + C_ac C_bc`. Contracting each term with `A=C⁻¹` collapses two
factors to Kronecker deltas with mismatched indices, e.g.
`A_{1a}A_{2b}A_{3c}C_ab C_ac = A_{12}·δ³₂ = 0`, and **all three terms vanish identically**.
The derived bridge annihilates the pointwise-transform bispectrum shape on its own. Two
independent routes to the same zero.

### 2.4 DISCRETISATION HAS A PARITY RULE — `b=2` is protected, `b≥3` is not

Route A must bin. Counting the whole-only directions: the pairwise family on three `b`-level
variables has codimension `(b−1)³` (from `b³−1 = 3(b−1)+3(b−1)²+(b−1)³`). Impose the global
flip `s ↦ (b−1)−s`, which a symmetric field's quantile binning respects. Each variable's
contrast space splits into flip-even and flip-odd parts; a whole-only direction is
flip-invariant iff it has an **even number of odd factors**.

* **`b=2`:** the contrast space is one-dimensional and flip-**odd**. The single whole-only
  direction has three odd factors, hence is flip-anti-invariant: **no flip-symmetric whole-only
  direction exists, so the binned share of any symmetric field is EXACTLY ZERO.** This
  re-derives `share_eq_zero_of_signSymmetric` (`Core/SignSymmetry.lean`) by dimension count,
  and it says median-binarisation is the one discretisation with a *theorem* under it.
* **`b=3`:** contrasts split 1 odd + 1 even, so the flip-invariant whole-only directions are
  `(e,e,e)` and the three `(o,o,e)` permutations — **4 of them.** The pairwise family does not
  exhaust the symmetric space, so **the binned share of a Gaussian is generically nonzero at
  `b ≥ 3`: a pure discretisation artifact with no signal behind it.**

Consequence, staked as a prediction: since the continuous Gaussian share is zero and the `b=2`
share is zero but the `b=3` share is not, **the discrete share is NOT monotone under bin
refinement.** (Aside, not tested here: the same parity count explains the survey's numerical
finding that sign symmetry kills every *odd* order.)

---

## 3. WHAT WILL BE COMPUTED

Two arms. The first has **no sampling anywhere** and is the primary; the second is the
realistic one and inherits every estimator trap in the memory of past failures.

### ARM 1 — EXACT (analytic densities, quadrature, no Monte Carlo, no estimator)

Positive control chosen so the truth is computable: the **skewed-latent triple**
`X_i = a_i Z + √(1−a_i²) ε_i`, `ε_i` iid standard normal, `Z` standardised with third cumulant
`γ`. Then `C_ij = a_i a_j (i≠j)`, `C_ii = 1`, `ζ_abc = γ a_a a_b a_c`, and every bin
probability is a **one-dimensional quadrature** — machine precision at any `b`, any `γ`. It is
also the mechanism the Ising ridge invoked (three spins reading one skewed latent), so it is
not an arbitrary toy.

| # | computation | why |
|---|---|---|
| A1 | Gaussian triple, quantile bins `b = 2…64`, grid of `C` | the discretisation bias, exactly |
| A2 | lognormal triple, same bins | transform invariance, at machine precision |
| A3 | skewed latent, `γ` swept over ≥4 decades, `b = 2…64` | Route A vs Route B, and the breakdown point |
| A4 | Route B closed form on the same models | the bridge |

`A_∞` := Route A extrapolated in `b` (Richardson on the fitted `A(b) = A_∞ − c b^{−α}`), with
`A(b_max)` also reported as a plain lower bound; both are quoted, never just the extrapolate.

### ARM 2 — FIELDS (3D, sampled, all the traps live here)

`N = 256³` cells, box `1000 Mpc/h`, CDM-like `P(k)` with a **stated** transfer function
(Eisenstein–Hu no-wiggle; `n_s=0.96, Ω_m=0.31, h=0.68`), Gaussian-smoothed at radius `R`.

* **(a) Gaussian** — primary control, must read zero.
* **(b) Lognormal** — `δ = exp(g − σ_g²/2) − 1`. Second null, by §2.3.
* **(c) Local `f_NL`** — `Φ = φ + f_NL(φ² − ⟨φ²⟩)`, `δ(k) = M(k)Φ(k)`. This is a pointwise
  transform **of the potential**, followed by a scale-dependent filter, so it is *not* a
  pointwise transform of `δ`: it is the genuine positive control. Amplitude swept from weak to
  absurd (`f_NL` up to values far outside any physical range — that is the point).

Route A: triples of cells at chosen separations, median-binarised (`b=2`, the protected
discretisation), pooled over placements. Route B: `ξ` and the connected `ζ` — **including the
collapsed and coincident-point terms** — measured with FFT estimators, fed to (B).

### Estimator discipline (Arm 2), non-negotiable

Every reported number carries: **tied fraction**; **shuffle floor**; **matched
pairwise-maxent surrogate floor** drawn at `N_eff`, not nominal `N`; a **variance-inflation
factor** from the measured correlation between triple placements; and a **cross-realisation
refuter** (slots drawn from independent realisations, true share zero by construction, must
floor at `|z| ≤ 5` or the null is mis-specified). Excess over the measured floor is what is
reported; raw and floor are both logged. IPF residuals are logged for every solve, per the
precision caution in `ISING_FIELD_RESULTS.md` §2.

---

## 4. PREDICTIONS — every possible answer, and what it would mean

| # | prediction | if it fails |
|---|---|---|
| P1 | **Gaussian, `b=2`, exact arm: identically 0** (`< 1e-12`) | pipeline broken → **VOID** (K1) |
| P2 | **Lognormal quantile-binned share = Gaussian's, to `< 1e-12`, at every amplitude, while its bispectrum is manifestly nonzero** | the transform theorem is wrong or misapplied (K2) |
| P3 | Gaussian at `b ≥ 3` is **nonzero**, and `A(b)` is **non-monotone** in `b` | the parity count in §2.4 is wrong; discretisation is benign after all |
| P4 | Skewed latent, weak `γ`: `d log A_∞ / d log γ = 2.00 ± 0.05` | the quadratic route is wrong (K3) |
| P5 | Weak regime: `|B/A_∞ − 1| ≤ 0.15` | bridge unusable at any amplitude → clean negative (K4) |
| P6 | The bridge **breaks** at strong coupling; `γ*` (first `γ` with `|B/A_∞−1| > 0.25`) is finite and locatable | if it never breaks, the quadratic form is exact for this family and I must say why |
| P7 | Field arm: Gaussian and lognormal fields both floor; local `f_NL` fires | (c) failing to fire ⟹ no positive control in the field arm (K5) |

**The primary agreement criterion, fixed now:** the bridge is judged **USABLE** iff P4 and P5
both hold and `γ*` exists and is reported. Anything else is a negative and is reported as
plainly as a survival, per house rule 7.

---

## 5. KILLS — separable, each taking down its own claim and nothing beneath it

| kill | fires when | what dies |
|---|---|---|
| **K1** | Gaussian exact-arm `b=2` share `> 1e-12` | **everything** — the run is VOID |
| **K2** | lognormal binned share differs from Gaussian's by `> 1e-12` | the "standard mock is a null" claim only |
| **K3** | fitted weak-coupling slope `∉ 2.00 ± 0.05` | derivation (B) only; Route A survives |
| **K4** | `|B/A_∞ − 1| > 0.15` in the weakest decade | Route B only; the bridge is declared unusable |
| **K5** | sampled Gaussian field fails to floor (`|z| > 5` vs matched surrogate), or the cross-realisation refuter fires | **field arm only**; the exact arm is untouched |
| **K6** | `b=3` discretisation bias exceeds the `f_NL` signal at plausible amplitudes | not a failure — a **design conclusion** that `b=2` is mandatory on real data |

---

## 6. WHAT THIS CANNOT DELIVER, WRITTEN DOWN NOW SO IT CANNOT BE CLAIMED LATER

1. **Nothing about the sky.** No survey data, no catalogue, no claim about nature.
2. **No stance change.** No promotion to `Stance.lean` from this run under any outcome; that
   would need a separate refuter pass and Eric's review.
3. **No priority claim.** (B) is an Edgeworth/connected-information calculation and may well
   be known; I searched the framing, not the literature exhaustively. The negentropy framing is
   openly borrowed and credited.
4. **The field arm cannot settle the continuum limit.** It reads `b=2` only, which by §2.4 is
   a strict lower bound on the continuous share.
5. **No claim that the skewed latent resembles a cosmological field.** It is the case where
   the answer is computable; that is its whole job.

---

*Pre-registration ends here. Nothing below this line existed when it was committed.*
