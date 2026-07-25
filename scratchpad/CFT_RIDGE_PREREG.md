# PRE-REGISTRATION — is the critical ridge the 2D Ising CFT?

Written and committed **before** `cft_ridge.py` existed and before any number in it was
computed. Scratchpad only: no Lean file, no `Stance.lean`, no audit, `lake` never run.

**Scope, first and load-bearing.** The 2D Ising model is a **model system**, not nature.
Nothing here bears on the `wild-share` open claim. If the hypothesis below survives, the
conclusion is that a *known* object was measured with our instrument — that is the good
outcome, and it is a modest one.

---

## 0. THE FINDING TO BE EXPLAINED

`ISING_FIELD_RESULTS.md` (commit `03cee87`) mapped the pairwise-blind order-3 connected
information `I_C^(3)` over the (T,h) plane. Two regimes:

- **fixed field** — local, `star` geometry wins, scales as `h²`, converges in `L`.
- **critical ridge** (`T = T_c`, `h* ∝ L^(−15/8)`) — **collective**: the share *grows* with
  triple separation and saturates (L=32: 5.09e-4, 1.80e-3, 3.31e-3, 4.57e-3, 4.73e-3 at
  r = 1,2,4,8,12), and the peak amplitude is **flat in L** (3.7–4.9e-3 nats over L = 8→64).

Two things need explaining: (i) growth-then-saturation in `r`, (ii) flatness in `L`.

## 1. THE HYPOTHESIS

At `T = T_c` the 2D Ising model is a CFT with `c = 1/2`. Its primaries and the constants
this pre-registration will use, all standard and none of them ours:

| | |
|---|---|
| spin field `σ` | `Δ_σ = 1/8` (`h = h̄ = 1/16`) |
| energy field `ε` | `Δ_ε = 1` (`h = h̄ = 1/2`) |
| OPE | `σ × σ = 1 + C_σσε ε + …`, `C_σσε = 1/2` |
| Z2 selection rule | `C_σσσ = 0`, so `⟨σσσ⟩ ≡ 0` |
| magnetic RG eigenvalue | `y_h = 2 − Δ_σ = 15/8` |
| exponents | `β/ν = Δ_σ = 1/8`, `η = 2Δ_σ = 1/4` |

**`⟨σσσ⟩ = 0` by Z2 is the continuum statement of `Core/SignSymmetry.lean`.** The lemma says
a sign-symmetric three-bit state has share exactly zero; the CFT says the same selection
rule kills the three-point function of the odd primary. That correspondence is the reason
`h = 0` reads machine zero at *every* temperature, criticality included.

## 2. THE DERIVATION

### Step A — the instrument as an exact function of five moments. **EXACT.**

Three ±1 variables: `p(s) = (1/8)[1 + Σ mᵢ sᵢ + Σ_{i<j} c_ij sᵢsⱼ + τ s₁s₂s₃]`. The pair
envelope is the one-parameter family that varies `τ` at fixed `(m, c)` (7 cells, 7
constraints — this is the one-dimensionality `ising_field.py` already exploits). Write
`S(τ)` for the entropy along it. Then `S'(τ_q) = 0` at the maxent member and
`S''(τ) = −(1/64) Σ_s p_s^(−1)`, so

> **`I_C^(3) = (1/128) · [Σ_s p_s^(−1)] · (τ_p − τ_q)² + O(Δτ³)`**,  `Δτ := τ_p − τ_q`.

and `Σ_s p_s^(−1) = 64 [1 + Σmᵢ² + Σc_ij² + τ² + …]`. So

> **`I_C^(3) = ½ (Δτ)² · [1 + O(m², c²)] + O(Δτ³)`.**  … (A)

The bracket and the cubic remainder are the **weak-coupling approximation**. Everything
before them is exact. Note the sign: the bracket is `≥ 1`, so (A) *understates* the share
when the moments are large.

### Step B — `Δτ` is the Ursell three-point function. **LEADING ORDER.**

For the pairwise-maxent `q` (same `m`, `c`), expanding `q ∝ exp(aΣsᵢ + bΣs_isⱼ)` gives
`τ_q = 3ab + a³ + 3ab² + …` with `a ≈ m`, `b ≈ c − m²`; to leading order that equals the
disconnected completion `Σᵢ mᵢ c_jk − 2m₁m₂m₃`. Hence

> **`Δτ = U + higher order`,  `U := ⟨s₁s₂s₃⟩_c` (Ursell/connected three-point).** … (B)

This is the step the Lean file's own caveat warns about — *"a large three-point correlation
function is NOT order-3 structure"*. Correct: it is the **connected** one, minus what the
pair marginals already imply, and (B) says those agree only at leading order. **Step B will
be checked numerically before it is used** (gate G5).

Combining (A)+(B): **`I_C^(3) ≈ ½ U²`** — the "quadratic-in-the-connected-correlator" route
the mission names. It is an approximation, valid when all moments are ≪ 1, and **only then**.

### Step C — scaling of `U`. **EXACT given universality.**

At `T = T_c` on an `L×L` torus the lattice spin is `s(x) = B σ(x) + irrelevant`, and the
field couples to `∫σ` with eigenvalue `y_h = 15/8`. Scale covariance then forces

> **`U(r; h, L) = L^(−3Δ_σ) Ψ(r/L, h L^(y_h)) = L^(−3/8) Ψ(r/L, h L^(15/8))`** … (C)

with `Ψ` universal up to the non-universal amplitudes `B³` and the metric factor on `h`.
Likewise `m = L^(−1/8) f(u)`, `c(d) = L^(−1/4) ĝ(d/L, u)`, `τ = L^(−3/8) t̂(r/L, u)`, where
`u := h L^(15/8)`. **Every moment carries one power of `λ := L^(−1/8)` per spin.**

### Step D — where `⟨σσε⟩` does and does not enter. **A CORRECTION TO THE STATED HYPOTHESIS.**

The mission proposes that the leading nonzero three-point structure is "governed by
`⟨σσε⟩` with `C_σσε = 1/2`". Stated that way it is **not right**, and the pre-registration
records the disagreement in advance rather than discovering it later:

- Our triple is three **spins**, so the object is `⟨σσσ⟩` in the *field-perturbed* theory,
  not `⟨σσε⟩`. At first order in `h`, `U = h ∫d²y ⟨σσσ σ(y)⟩_Ursell` — the kernel is the
  σ **four**-point function. Its s-channel decomposition contains the identity and `ε`
  with weight `C_σσε² = 1/4`, so `C_σσε` enters, **squared and alongside the identity
  block**; `I_C^(3)` is not proportional to it.
- `⟨σσε⟩` with its `x₁₂^(3/4)/(x₁₃x₂₃)` form governs the *short-distance* corrections
  (`⟨σ(0)σ(r)⟩ = B²r^(−1/4)[1 + C_σσε r ⟨ε⟩ + …]`), i.e. the `r ≪ ξ` end, not the ridge.
- **The ridge sits at `u = O(1)`, which is not perturbative in `h` at all.** There no single
  OPE coefficient controls the amplitude; the content of the CFT there is the *scaling form*
  (C) and the exponents in it, not a closed-form number. Predicting the ridge **amplitude**
  from first principles is out of scope; predicting its **exponents** is not.

### Step E — the linear-response regime, for completeness. **DERIVED.**

For `u ≪ 1`, `Ψ(x,u) ≈ u ψ(x)`, so `U ∝ h L^(3/2) ψ(r/L)` and
`I_C^(3) ∝ h² L³ ψ(r/L)²` with the exponent `3 = 2(y_h − 3Δ_σ)`. The small-`x` behaviour of
`ψ` is **not** pre-registered: the `y`-integral is IR-dominated and the σ-cluster channel
suggests `ψ(x) ~ x^(−1/4)` (share *decreasing* in `r`, opposite to the ridge), but the
coefficient could cancel. That fit is **exploratory**, and labelled so.

## 3. PRE-REGISTERED PREDICTIONS

All at `T = T_c = 2/ln(1+√2)`, `L×L` periodic, collinear triples at sites `(0, r, 2r)`.

| # | prediction | number | status |
|---|---|---|---|
| **E1** | ridge locus: `h*(L) ∝ L^(−y_h)` | **`y_h = 1.875`** | CFT test |
| **E2** | ridge amplitude, fixed `r/L`: `I_C^(3) ∝ L^(−6Δ_σ)` | **`−0.75`** | CFT + weak-coupling |
| **E3** | small-`h`, fixed `L,r`: `I_C^(3) ∝ h^2` | **`2`** | **gate, not evidence** — follows from Z2 + analyticity alone (see §5) |
| **E4** | moment collapse at fixed `(r/L, u)`: `m·L^(1/8)`, `c·L^(1/4)`, `τ·L^(3/8)`, `U·L^(3/8)` are `L`-independent | exponents `1/8, 1/4, 3/8, 3/8` | **the CFT content, entropy-route-free** |
| **E5** | share collapse: `L^(3/4)·I_C^(3)` is a function of `(r/L, u)` only | — | E2 in collapse form |
| **E6** | saturation scale for `h > h*(L)`: `r_sat ∝ h^(−1/y_h)` | **`−0.533`** | CFT test, independent observable |
| **E7** | **moment-rescaling test (PRIMARY).** Take the exactly computed moments at `L₁`; multiply by `(L₂/L₁)^(−1/8), ^(−1/4), ^(−3/8)`; compute `I_C^(3)` **exactly** from them; compare to the directly computed value at `L₂` at matched `(r/L, u)`. | agreement | **parameter-free; no weak-coupling, no amplitudes** |
| **E8** | `r`-dependence on the ridge is a **crossover in `r/L`, not a power law**, with `W(x→0) = 0` (a coincident triple is degenerate and has share exactly 0) and saturation for `x = O(1)` | — | this is why the sibling's K4 fired |

**Pass/fail thresholds, fixed now.** Data from the exact arm carries no statistical error,
so criteria are about corrections to scaling. Let `σ_local(L)` be the two-point log-slope
between successive lattice sizes.

- **E1 survives** if `σ_local` for `h*(L)` lies in `−1.875 ± 0.06` at the two largest `L`
  pairs, **fires** if it is outside `±0.15` and not trending in.
- **E2 survives** if `σ_local` for the ridge amplitude is in `−0.75 ± 0.10` at the largest
  pair or is trending monotonically toward it. **E2 FIRES** if the largest-`L` local slope is
  shallower than `−0.45` **and** flat or non-monotone.
- **E4 survives** if each rescaled moment collapses to within **2 %** across the largest
  factor-2 change in `L`; fires above **8 %**.
- **E6 survives** if the fitted exponent is in `−0.533 ± 0.08`.
- **E7 survives** if predicted and directly computed `I_C^(3)` agree to within **3 %** at the
  largest `L` pair and the residual shrinks with `L`; **fires** above **12 %**.

## 4. WHAT EACH OUTCOME MEANS — written before seeing any of it

1. **E1 + E4 + E7 survive, E2 fires.** Then the CFT identifies the ridge *at the correlator
   level* — `β/ν = 1/8` and `y_h = 15/8` are the mechanism — while the `L^(−3/4)` asymptote
   is simply **not reached at accessible `L`**, because the approach parameter is
   `λ = L^(−1/8)` (a 8 % change per doubling; `λ ≈ 0.65` at `L = 32`, and `λ < 0.2` needs
   `L > 10^6`). The flatness would then be a fact about the *instrument's* nonlinearity, not
   about the physics, and I would say exactly that. **This is the outcome I consider most
   likely**, and I am recording that guess in advance so it cannot be claimed afterwards.
2. **E1, E2, E4, E7 all survive.** The ridge is the CFT magnetisation sector, full stop.
   Known physics, measured with a new instrument. Credit Ising/Onsager/BPZ, claim nothing.
3. **E4 fires.** The moments do not carry `Δ_σ`. Then the ridge is *not* the σ sector and the
   CFT route is wrong — the interesting outcome, to be reported as such with the measured
   exponents in place of `1/8, 1/4, 3/8`.
4. **E1 fires.** We were never on the ridge; the sibling's grid placement (`h* ∝ L^(−15/8)`,
   disclosed there as physics-motivated, never fitted) was wrong, and everything downstream
   of it is re-opened. This would be a correction to the record.
5. **E7 survives while E2 fires and E6 fires.** Scaling of the moments right, saturation
   mechanism wrong — report the saturation as unexplained.

**No outcome promotes anything to `Stance.lean`.** Any stance change needs a separate
refuter pass and Eric's review.

## 5. METHOD, fixed in advance

**Arm A (primary) — EXACT transfer matrix on the torus.** The sibling's weakest point is
Monte Carlo at criticality in a field: no cluster algorithm applies, `F` reached `5.5e4`,
`N_eff` fell to `3.8e3`, and 26 % of grid points were discarded. The exact arm removes that
entirely. Symmetric row-to-row transfer matrix `T = D^{1/2} V D^{1/2}` on `{±1}^L`, with
`D(σ) = exp[K Σσᵢσ_{i+1} + βh Σσᵢ]` and `V = ⊗ᵢ [[e^K, e^(−K)],[e^(−K), e^K]]`. The exact
single-row marginal on the `L×L` torus is `w(σ) ∝ [T^L]_{σσ}`, from which **every** moment of
a collinear triple follows to machine precision. Two independent implementations:

- `full`: apply `T` `L` times to the identity in column chunks, read the diagonal. No
  truncation whatsoever. Used for `L ≤ 14`.
- `lanczos`: `w(σ) ∝ Σₙ λₙ^L vₙ(σ)²` from the top-`k` eigenpairs. Used for `L ≥ 16`,
  **validated against `full`** and with `k` doubled to confirm convergence.

**Arm B (secondary) — GPU Metropolis** at `L = 24…64`, reported only if it reproduces Arm A
at `L = 16`. Same estimator apparatus as the sibling (`N_eff`, not nominal `N`).

**Gates — all must pass before any prediction is scored.**

| | |
|---|---|
| G1 | Arm A reproduces the sibling's exact `4×4` enumeration (`ising_exact.json`) for `m`, `c(d)`, `τ`, `I_C^(3)` to `< 1e-10` |
| G2 | `h = 0` gives `I_C^(3) < 1e-12` at every `L`, every `r` — the lemma |
| G3 | `lanczos` agrees with `full` at `L = 12, 14` to `< 1e-10`, and `k → 2k` changes nothing at `1e-8` |
| G4 | `T_c`, `h=0`, large `L`: `c(1) → 0.7071` (Onsager `√2/2`) as `L` grows |
| G5 | **Step B checked**: `|Δτ − U| / |Δτ| < 5 %` wherever the weak-coupling route is *used*; where it is larger, (A)+(B) is reported as inapplicable rather than applied |
| G6 | Arm A reproduces the sibling's growth-then-saturation in `r` qualitatively at `L = 16`. If it does not, the sibling's MC separation scan is suspect and that is reported as a correction. |

**Disclosures made in advance.** (i) `E3` is a gate, not evidence: `I_C^(3) ∝ h²` follows from
`U` being odd in `h` and analytic at finite `L`, whatever the mechanism — so the sibling's
measured exponent `2.000`, which the mission calls "a strong hint the quadratic route is
right", is **consistent with but not diagnostic of** the CFT. Recording that before looking.
(ii) The ridge amplitude is not predicted, only its exponent (Step D). (iii) `Ψ`'s small-`x`
form is exploratory. (iv) Arm A gives collinear (single-row) triples only; `star` spans two
rows and is out of Arm A's reach.

## 6. FILES

`CFT_RIDGE_PREREG.md` (this file, committed first) → `cft_ridge.py` → `CFT_RIDGE_RESULTS.md`.
</content>
</invoke>
