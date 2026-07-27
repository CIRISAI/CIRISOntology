# PUMP campaign — pre-registration

**Frozen before any curve was computed.** Written after `PUMP_PRIOR_ART.md` (commit `8125797`)
and before any numerical value of the pump curve existed anywhere. The analytic derivations in
§4 were done by hand on paper, in this document, before the instrument in §6 was written; that
is stated so a reader knows exactly which numbers here are predictions and which are fits, and
the answer is that **every number in this document is a prediction. There are no fits in it.**

---

## 0. What is being measured, and what is not

`Core/Valve.lean` proves four qualitative facts about per-cell stochastic channels on the k = 3
binary model: never from nothing, never downward, upward strictly, and the pump is asymmetry not
strength. `PUMP_PRIOR_ART.md` establishes that the first two are published (Zhou 2009,
Galla & Gühne 2012) and the third is one step from a published discord result (Streltsov et al.
2011). **The only leg where the literature search came back empty is the rate.**

So this campaign measures one thing:

> **At what rate does per-cell stochastic noise convert pair structure into whole-only
> structure, as a function of the channel's asymmetry?**

**Out of scope, explicitly.** Nothing here bears on `wild-share` — which of nature's processes
carry whole-only structure. Nothing here moves `Stance.lean`; a stance change would need a
separate refuter pass. Every substrate below is designed or simulated; the single hardware point
is a cross-check against a reading already in the record, not a new measurement.

**The alphabet boundary is load-bearing and is honoured.** `Core/Valve.lean` and
`Core/Creation.lean` are proved for SAME-ALPHABET per-cell maps only. Arms A–E below are
same-alphabet. Arm F crosses the boundary deliberately, is labelled exploratory, carries its own
separable verdict, and **is not permitted to contribute to the primary rate law** whatever it
finds.

---

## 1. The channel family, and its two coordinates

A per-cell binary kernel is two numbers. Write them as the two error probabilities

- `p01 = P(read 0 | was 1)` — the relaxation direction
- `p10 = P(read 1 | was 0)` — the excitation direction

and define the campaign's coordinates:

| | | |
|---|---|---|
| **asymmetry** | `a = p01 − p10` | how differently the kernel treats the two cell values |
| **strength** | `s = (p01 + p10)/2` | how much noise there is, irrespective of direction |

Feasibility: `p01 = s + a/2`, `p10 = s − a/2`, both in `[0,1]`, so

> **`|a| ≤ 2·min(s, 1−s)`**

**The correspondence to the repository's own moment code, checked by hand.** In the ±1 basis
(`z = (−1)^x`) a per-cell kernel acts affinely, `z ↦ κz + b`, and

> **`κ = 1 − 2s` and `b = a`.**

The repository's `qpu_habit_pipeline.apply_product_channel(M, kappa, b)` therefore already takes
this campaign's two coordinates as its arguments, with `b` **being** the asymmetry. Two named
points on the family:

- **Flip-covariant / binary symmetric / unital:** `a = 0`, i.e. `b = 0`, any `s`. This is the
  line `Core/Valve.lean`'s `IsFlipCovariant` picks out, and `valve_needs_asymmetry` says it mints
  exactly zero from any sign-symmetric state at any strength. **This is the theorem-pinned
  control.**
- **`Core/Valve.lean`'s `damp` (γ = ½):** `p01 = 1/2`, `p10 = 0`, so `a = 1/2`, `s = 1/4`,
  `κ = 1/2`, `b = 1/2`. It sits on the feasibility boundary `a = 2s` — maximal asymmetry at its
  strength. This is why the file's headline example pumps as hard as it does, and it is a
  boundary point of the family, not an interior one. Stated here because a reader of that file
  could reasonably assume it was a typical channel. It is the extreme one.
- **Amplitude damping toward a thermal population `p_exc`** (the hardware's channel):
  `p01 = (1−p_exc)(1−κ)`, `p10 = p_exc(1−κ)`, giving `a = (1−2p_exc)·(1−κ)` and `s = (1−κ)/2`.
  So along a physical idling trajectory **`a` and `s` are locked together**, `a = 2s·α` with a
  fixed **asymmetry ratio** `α ≡ 1 − 2p_exc`. A perfectly cold bath is `α = 1` (the boundary); an
  infinitely hot one is `α = 0` (the unital line). This is the single number that places any
  physical relaxation channel on the curve, and it is the number the hardware cross-check turns on.

---

## 2. Substrates

**Arm A — the reference substrate.** `ferro`: `p(000) = p(111) = 1/2`. Maximal pair correlation
on three bits, sign-symmetric, whole-only share **exactly zero** (`share_ferro`, machine-checked).
This is `valve_upward`'s own input.

**Arm B — varying input pair strength.** `p_ρ = ρ·ferro + (1−ρ)·uniform` for `ρ ∈ (0,1]`. Every
member is sign-symmetric, so every member has share exactly zero before the channel
(`share_eq_zero_of_signSymmetric`), and its pair correlation is exactly `⟨z_i z_j⟩ = ρ`. This is
the family that answers "does the pump feed on pair structure in proportion to how much there is?"

**Arm C — k-scaling, primary.** The repetition code at k slots: `p(0^k) = p(1^k) = 1/2`, for
k = 3,4,5,6,7. Sign-symmetric at every k, hence share exactly zero at every k, and the direct
generalisation of `ferro`.

**Arm D — k-scaling, secondary (declared, run if the box allows).** The `RENT_ISLANDS` G7
**equivariant** roster — the code supports on which upkeep provably restores the design state:
k = 5, 6, 7 (Sylvester-8). Uniform on the code. Declared because the brief asks whether the pump
scales with the *ceiling* rather than the slot count, and these substrates have different
ceilings at the same k. **Not** the lossy ones (k = 8, 16–22, 24) — restorability failing there
confounds the reading, which is the whole content of G7.

**Arm E — robustness.** (i) Non-identical channels: the three kernels drawn independently, which
is what hardware actually is. (ii) A non-permutation-symmetric sign-symmetric input, to check the
law is not an artifact of the symmetric parametrization.

**Arm F — the coarse-graining probe (EXPLORATORY, separable, cannot feed the primary).** A
4-letter cell pushed through a 4-letter per-cell channel and then binarized. This crosses the
alphabet boundary `Core/Valve.lean` explicitly does not cover, and is the κ-edge's open question.
Its verdict is reported separately and is not permitted to modify anything in §4.

---

## 3. Observables

For a state `p` and a per-cell channel triple `K`:

1. **Minted share, one step:** `Δ(a,s) = share(K·p) − share(p)`. On every arm above `share(p) = 0`
   exactly, so `Δ = share(K·p)`.
2. **Saturation and transient, many steps:** `share(K^n·p)` as a function of `n`. Report the peak
   value, the `n` at which it peaks, and the decay beyond. The fixed point of any per-cell channel
   with `s > 0` is a product state, whose share is exactly zero (`share_prod3`), so the curve
   **must** be a bulge: this is a prediction of the existing theorems, not of this campaign, and
   its failure would indict the instrument, not the physics.
3. **The exponent:** `n_a ≡ d log Δ / d log a` at fixed `s`, in the small-`a` limit.
4. **The coefficient:** `C(s) ≡ lim_{a→0} Δ/a²`, and its functional form in `s`.

Everything is in **nats**. Ceiling fractions, where quoted, divide by `ln 2` at k = 3 on the
authority of `Core/ThirdCap.lean`'s `share_le_log_two`, which proves the denominator with no
hypothesis on the pair data.

---

## 4. THE PRE-REGISTERED PREDICTIONS

These were derived by hand before the instrument was written. Each is stated with what would
falsify it and what a failure would mean.

### 4.1 P-EVEN — the curve is exactly even in `a`. Structural.

Under the global sign flip, the repetition-code input is invariant, and swapping `p01 ↔ p10`
(i.e. `a ↦ −a` at fixed `s`) conjugates the channel by that flip. The share is invariant under
any per-slot relabelling. Hence

> **`Δ(−a, s) = Δ(a, s)` exactly, at every `s`, at every k.**

**Kill:** any measured asymmetry between `+a` and `−a` above the solver floor. **Meaning of a
failure:** the instrument is broken, not the physics — this is a symmetry of the definition.
P-EVEN is therefore a **dye test on the instrument**, and it is the first thing run.

**Consequence, and it is why the exponent hypothesis is sharp:** an odd leading exponent is
*impossible*. Measuring `n_a ≈ 1` would mean the share is non-smooth at `a = 0`, which given
P-EVEN would mean a `|a|` cusp.

### 4.2 P-EXP — the exponent is 2. Staked band `n_a ∈ [1.90, 2.10]`.

`Δ ≥ 0` always and `Δ(0,s) = 0` exactly (`valve_needs_asymmetry`), so `a = 0` is a global minimum.
The map `a ↦ p_a` is polynomial, the k = 3 envelope maximiser is interior and unique (the entropy
is strictly concave along the one-dimensional competitor line), so by the implicit function
theorem `Δ` is smooth near `a = 0`. Smooth, even, minimised at zero ⇒ leading term `a²`.

| measured | what it would mean |
|---|---|
| **`n_a = 2`** | the staked answer. `a = 0` is a smooth, non-degenerate minimum |
| `n_a = 4` | the quadratic coefficient vanishes identically — a hidden degeneracy, and the more interesting outcome, because it would mean the pump is *far* weaker at small asymmetry than the smoothness argument allows |
| `n_a = 1` | the share is non-smooth at the unital line. Given P-EVEN this means a cusp, which would contradict the interiority of the envelope maximiser and would be a genuine discovery about the geometry |
| anything else | the instrument, checked against P-EVEN and §5's plumb lines first |

### 4.3 P-FORM — the closed form. **The campaign's sharpest stake.**

Derived by hand for a permutation-symmetric sign-symmetric input with pair correlation `ρ`, three
identical per-cell kernels, writing `r₀ ≡ κ²ρ = (1−2s)²ρ` for the **surviving pair correlation**:

> **`Δ(a, s; ρ) = 18·r₀⁴·a² / [ (1 + 2r₀)(1 + 3r₀)(1 − r₀) ] + O(a⁴)`**

The derivation, so it can be checked rather than believed. In the sign basis with all singles
equal to `m`, all pairs to `r`, triple `c`, the four cell values by Hamming weight are
`p₀ = (1+3m+3r+c)/8`, `p₁ = (1+m−r−c)/8`, `p₂ = (1−m−r+c)/8`, `p₃ = (1−3m+3r−c)/8`. The channel
sends the input to `m = a`, `r = r₀ + a²`, `c = 3r₀a + a³`. The pair envelope is the line in `c`
alone; its maximiser solves `p₀p₂³ = p₁³p₃` (this is Galla & Gühne's Eq. 17 and the root our
exact solver brackets), which to first order gives `c* = 3r₀a/(1+2r₀)`, so the state sits
`Δc = −6r₀²a/(1+2r₀)` off the maximiser, and `|g''| = (1+2r₀)/[(1+3r₀)(1−r₀)]` converts that
displacement into entropy at `Δ = ½|g''|(Δc)²`.

**Two consequences worth naming separately, because they are separately falsifiable:**

- **P-FORM-κ:** at fixed `ρ = 1`, `C(s) = 18κ⁸/[(1+2κ²)(1+3κ²)(1−κ²)]` with `κ = 1−2s`. Note the
  **eighth power** of the survival factor: the pump is savagely suppressed by noise strength even
  though asymmetry is what drives it. Strength is not the pump — but strength is a very effective
  brake.
- **P-FORM-ρ:** the coefficient goes as the **fourth power** of the surviving pair correlation,
  `C ∝ r₀⁴` at small `r₀`. Halving the input pair correlation cuts the pump by sixteen.

**Kill:** measured `Δ/a²` departing from the closed form by more than **2 %** anywhere in
`κ ∈ [0.1, 0.95]`, in the regime where the expansion is declared valid (§4.6).

**Meaning of a failure, and it is not symmetric.** If the closed form fails while P-EXP holds, the
hand derivation is the first suspect and will be checked before anything else is claimed; a
derivation slip is noise, not signal, and saying so in advance is how it stays that way. If it
fails *in a specific reproducible way* after the algebra is verified, the failure is the finding.

### 4.4 P-K — k-scaling. Three named alternatives, one staked.

P-EVEN's argument runs at every k, so exponent 2 is staked at every k on the roster. What is open
is how the **coefficient** grows.

| hypothesis | prediction | what it would mean |
|---|---|---|
| **K-CEILING** | `C_k` grows like the whole-only ceiling, `∝ (k−2)` or `(k−3)` | the pump fills the available room; the ceiling is the right normalisation and every campaign's ceiling fraction is the right observable |
| **K-COUNT** *(staked)* | `C_k` grows like the number of slots or of triples, `∝ k` or `k³` | the pump is local and additive over sub-structures; the ceiling is irrelevant to the rate |
| **K-NEITHER** | `C_k` saturates or falls | the pump is a k = 3 phenomenon and does not scale, which would be the strongest possible limit on every downstream mapping |

**Staked: K-COUNT**, on the reasoning that the minting mechanism in §4.3 is a local displacement
off the pair-maxent manifold and such displacements add over the structures that carry them. Held
loosely — this is the leg with the least analytic backing, and it is labelled as the least
confident of the four.

**Kill:** the fitted growth exponent of `C_k` in k, over k = 3…7, excluding all three brackets.

### 4.5 P-QPU — the hardware cross-check.

**Blinding declared honestly: there is none, and there cannot be.** Run 3's ferro bulge
(0.0541 nat at 49.5 µs, K-CURVE χ² = 24.44 on 12 dof, zero free parameters) is already published
in `scratchpad/temporal-share/QPU_HABIT_RESULTS.md`. Nothing derived from it is a blind
prediction, and no claim in this campaign rests on it. What the overlay buys is a **cross-substrate
consistency check**: does a superconducting qubit triple, idling, sit on the curve a designed
three-bit system traces?

Staked, from the measured per-qubit `κ_q(t)` and `p_exc,q` in
`qpu_sector_verdict_C_d9in8jrjf64c739fprqg.json`:

- **QPU-1 (exactness):** the exact solver applied to the exact channel output, with the same
  measured `(κ_q, b_q)` the published analysis used, reproduces the published `ferro_pred` column
  to within **1 %** at every delay. This is a reproduction gate on our instrument against the
  repository's own, not a new result.
- **QPU-2 (the law):** at delays where the small-`a` expansion is declared valid (§4.6), the ratio
  of the measured hardware share to the closed form of §4.3, evaluated at the hardware's own
  `(a, s)`, lies in **[0.5, 2.0]**. Wide, deliberately: the hardware has three unequal channels, a
  stretched-exponential substrate, and readout correction, and a factor-of-two agreement between a
  four-line closed form and a quantum processor is the claim, not a percent-level one.
- **QPU-3 (the placement):** the device's asymmetry ratio `α = 1 − 2p_exc` is quoted per qubit and
  the operating trajectory drawn on the `(a, s)` plane, so a reader can see where hardware lives
  relative to the unital line and to `damp`'s boundary point.

**Kill:** QPU-1 outside 1 % fouls **our instrument** and stops the campaign until fixed. QPU-2
outside its band is reported as a **failure of the designed-substrate law to transfer to
hardware**, which is a finding about the unification and is stated as such.

### 4.6 Validity of the expansion, declared in advance

The closed form is a small-`a` expansion. It is declared valid where **`|a| ≤ 0.25`**, chosen
before any curve was computed, on the grounds that the next term is `O(a⁴)` and `0.25² = 6 %`
is the scale at which a 2 % kill band stops being meaningful. Outside that region only the exact
solver is quoted, and the closed form is plotted as an extrapolation, visibly labelled.

---

## 5. The gate battery — and which gates are vacuous here, said plainly

`GATES.md` is written for **sampled estimators**. The primary arms of this campaign are **exact
computations on exactly specified distributions**: there is no data, no sample, and no shot noise.
Running a shuffle floor on a closed-form probability vector would be theatre. So the battery is
mapped reach by reach, and the vacuous cells are marked vacuous rather than quietly passed.

| GATES.md reach | applies? | how it is discharged here |
|---|---|---|
| **1. Estimator bias** | **vacuous in arms A–E** (no estimation), **live in arm G** | arm G (§5.1) is added precisely so this reach is not simply skipped |
| **3. Mixture / manufacture** | **LIVE, and it is the theorem-pinned control** | the null that must not reproduce the effect is the **same channel with `a` set to zero at the same `s`**: identical noise strength, identical everything, no asymmetry. `valve_needs_asymmetry` says it must read exactly zero. This is a mixture null with a *proved* answer, which is stronger than any of the repository's other mixture nulls |
| **5. Coarse-graining minting** | **out of scope in A–E, and that is a scope statement not a pass**; **live in arm F** | arm F is the probe, separably reported |
| **7. Dose-vs-rate** | **LIVE** | the per-step minted share must be step-count invariant, or the transient must be characterised (§3.2). A rate law read off a single step of a transient is exactly this reach's failure mode |
| **9. Sampling / shot noise** | **vacuous in A–E**, **live in arm G** | see §5.1 |
| **11. Occupancy / sparsity** | **LIVE** | states with cells at or near zero are where the envelope maximiser hits the boundary and the smoothness argument of §4.2 fails. Configurations with any cell below `1e−12` are declared **ungauged** and excluded, in advance |
| **12. Solver / relaxation gap** | **LIVE, and it is the load-bearing one** | §5.2 |
| **13. Power of the control** | **LIVE** | P-EVEN is a dye test with a known answer; the plumb lines in §5.2 are planted dye with exactly computable values |
| 2, 6, 8, 10 | vacuous | no boundary convention, no residual, no probe direction, no Lean text |

**Search caps declared:** golden-section 90 iterations or interval `< 1e−14`; bisection 200
iterations; IPF capped at 5000 sweeps with the residual reported, never the iteration count. A
saturated search is reported as a bound, never as a value.

**Null shape before z:** no z-scores are quoted anywhere in this campaign's primary arms, because
there is no null distribution — there are exact numbers and their solver tolerances. Where arm G
quotes a significance it will report the null's shape first, per the Dalitz D7 lesson.

### 5.1 Arm G — the sampled arm, added so reaches 1 and 9 are not skipped

Draw `N` samples from the exact channel output and read the share with the same solver. Sweep
`N ∈ {10², 10³, 10⁴, 10⁵, 10⁶}`. Report the **finite-`N` floor** — the share read on samples from
a state whose true share is exactly zero (the `a = 0` control), which is pure estimator bias.

**This arm exists to separate two things the downstream mappings are at risk of conflating**, and
the separation is pre-registered because it is the most likely way this campaign could mislead:

- **The valve** changes the *true* share of the *exact* distribution. It is physics.
- **Finite-`N` minting** leaves the true share at zero and moves the *estimator*. It is bias, it
  is χ²-shaped (memory: `share-null-is-chi2-shaped`), and it scales as roughly (cells−1)/2N.

The sky campaign's 130 %-of-signal shot-noise floor is a member of the **second** family.
Whether it is *also* a member of the first — Poisson sampling is genuinely an asymmetric per-cell
channel — is a real question and is named in §7, not assumed in either direction.

### 5.2 The certificates, and the plumb lines

**k = 3, exact.** The competitor set is the one-parameter line `p + tχ` (`χ` = the parity
character), so the envelope maximum is a scalar problem. Two independent solvers are run on every
single configuration and must agree:

- **primal:** golden-section on `H(p + tχ)` over the feasible interval — the method of
  `SHEARER_NUMERIC.py`, reused rather than rewritten;
- **root:** bisection on the stationarity condition `p₀p₂³ = p₁³p₃` — the method of
  `qpu_habit_pipeline.pairwise_maxent_exact`, reused.

**Agreement bracket staked: `≤ 1e−12` nat on every configuration.** Wider anywhere ⇒ that
configuration is **ungauged** and is dropped with a count reported.

**k ≥ 4, two-sided.** The maxent under all pair marginals is an Ising fit, and the certificate is
primal-versus-dual, not a single fitted solution (GATES.md reach 12, and the memory
`ipf-sharek-boundary-drift`: IPF **one-sidedly overstates** the share near determinism, by five
orders of magnitude in the stored case):

- **upper bound:** `min_θ [ log Z(θ) − θ·μ ] − H(p)`. Because it is a minimum of a convex
  function, *any* `θ` evaluates to a rigorous upper bound; the returned `θ*` therefore certifies.
- **lower bound:** the entropy of the fitted `q_θ*`, with its pair-marginal residual reported, is
  a rigorous lower bound once the residual is discharged.
- **staked bracket width: `≤ 1e−6` nat.** Wider ⇒ ungauged.
- **IPF is run alongside and is reported as a third number, never as the answer.** If IPF sits
  outside the bracket, that is filed as a fresh instance of the stored taint, with the
  configuration kept.

**Plumb lines — planted dye with exactly known answers, run before anything else:**

| state | true share | source |
|---|---|---|
| `parity` | exactly `ln 2` | `Core/Share.share_parity` |
| `ferro` | exactly `0` | `Core/SignSymmetry.share_ferro` |
| `indep` / uniform | exactly `0` | `Core/SignSymmetry.share_indep` |
| any product state **on three binary slots** | exactly `0` | `Core/Valve.share_prod3` — signature `{p₁ p₂ p₃ : Bool → ℝ}` |
| any sign-symmetric state **on three binary slots** | exactly `0` | `Core/SignSymmetry.share_eq_zero_of_signSymmetric` — signature `{p : Bool × Bool × Bool → ℝ}` |
| `bulge` = `damp³·ferro` | `≥ ln2 + (3/4)ln3 − (17/32)ln17 ≈ 0.011958` | `Core/Valve.valve_upward_bound` |
| every reading **on three binary slots** | `≤ ln 2` | `Core/ThirdCap.share_le_log_two` — signature `{p : Bool × Bool × Bool → ℝ}` |

**[AMENDED — AMENDMENT 9. The three rows above originally read "any product state", "any
sign-symmetric state" and "every reading, any state", with no slot count. All three theorems are
`Bool × Bool × Bool` only, and this campaign then ran arms at k = 4…7 against a table that, as
written, licensed applying them there. Found by running `water`'s citation-class audit on my own
documents after they suggested it. No number moved — every k ≥ 4 reading was reported as
*measured* — but the table was wrong and would have misled a reader who trusted it.]**

The `bulge` row is the sharpest available: a machine-checked **lower bound** on a specific number
this campaign will compute. If the instrument returns less than 0.011958 nat at `damp³·ferro`, the
instrument contradicts a theorem and the campaign stops.

**Cap compliance:** every reading at every k is checked against the cap in force
(`share_le_log_two` at k = 3; `HammingCap`'s tiers above, with the hypothesis checked before the
cap is applied, not assumed). Violations are reported as instrument failures.

---

## 6. Instrument and box discipline

One Python file, `scratchpad/pump_curve.py`, in `scratchpad/temporal-share/qenv`. CPU only, at
most 4 worker processes and `OMP_NUM_THREADS=2`: the box is shared (glass, Planck, water and
rent-scaling are running; load average 22–30 and the GPU at 100 % when this was written), the
k ≤ 7 exact computations are microseconds each, and **no GPU is requested**. Every JSON and log
is committed beside the results.

Determinism: every random draw seeded from a constant recorded in the output. The instrument is
re-runnable and the committed log must be bitwise reproducible from the committed instrument —
the `gate-log provenance` gate minted at `d54e015`.

---

## 7. Downstream mappings — declared in advance, with their conditions

The brief's claim is that a definite curve converts four separately-measured nuisance floors into
one law with one parameter. That is worth stating **in advance, with the conditions under which
it would and would not hold**, so it cannot be asserted afterwards on the strength of whatever
turns up.

| downstream | is it the same object? | condition for the mapping to hold |
|---|---|---|
| **QPU bulge** | **yes** — same-alphabet per-cell channel on an exact distribution | P-QPU passes. Then the hardware floor is a *prediction* from `α = 1 − 2p_exc` |
| **Planck pilot's valve floor** | **yes if** the instrument noise is same-alphabet per-pixel | the mapping is licensed only if the Planck noise model is per-cell and does not change the alphabet. To be checked against `PLANCK_PILOT_*`, not assumed |
| **sky shot-noise minting (130 %)** | **partly, and the parts must be separated** | Poisson sampling *is* an asymmetric per-cell channel, so a real valve contribution exists — but the 130 % figure is dominated by **finite-`N` estimator bias**, a different mechanism (arm G). The mapping holds only for the first part, and the sky number is not licensed to be reinterpreted wholesale |
| **glass / water coarse-graining floors** | **no, on current theorems** | binarizing a continuous or many-letter observable is an *alphabet-reducing* map, which `Core/Valve.lean` explicitly does not cover. Arm F probes it. If arm F shows the same `a²` law survives coarse-graining, the mapping is licensed and glass and water's floors become predictions; if it does not, the honest outcome is that these two campaigns' floors stay separately measured |

**The negative outcome is a result and is pre-committed as one.** If the curve has no single
shape across arms A–E — if the exponent or the coefficient's functional form differs by
substrate — then the unification is dead, four floors stay four floors, and this document's §7 is
reported as **refuted**. That is stated here so it cannot later be presented as "the curve was
richer than expected".

---

## 8. Verdict grid — every outcome has a meaning assigned before it is seen

| P-EVEN | P-EXP | P-FORM | verdict |
|---|---|---|---|
| pass | pass | pass | **the rate law stands.** §7's licensed mappings become predictions |
| pass | pass | fail | the exponent is right and the coefficient is not. Check the hand algebra first; if it survives, the closed form is replaced by the measured `C(s)` and the campaign delivers a *measured* rate law rather than a derived one — a weaker but real result |
| pass | fail (=4) | n/a | a degeneracy at the unital line. The pump is far weaker at small asymmetry than smoothness allows, and every downstream floor built on a linear-in-noise intuition is **over-estimated**. The most consequential outcome on the grid |
| pass | fail (=1) | n/a | a cusp at the unital line, contradicting the interiority of the envelope maximiser. Instrument suspected first, then reported as a geometric finding |
| **fail** | — | — | **instrument fouled.** No physics is reported from this run at all |

Separability: P-EXP failing does not touch P-FORM's status (it supersedes it), P-K failing touches
neither, P-QPU failing touches none of A–E, and arm F failing touches nothing above it. Each kill
takes down its own claim and nothing beneath it.

---

## 9. What this campaign may and may not conclude

**May:** that the rate at which per-cell noise converts pair structure to whole-only structure, on
designed same-alphabet binary substrates, follows a stated law in the channel's asymmetry,
strength and the input's pair correlation; that a superconducting qubit triple does or does not
sit on that law; that the law does or does not scale with slot count.

**May not:** anything about nature's wild processes. Anything about coarse-grained substrates
beyond arm F's own separable verdict. Any change to `Stance.lean`. Any claim that the *creation*
of whole-only share by local noise is a discovery of this programme — it is Zhou 2009 and
Galla & Gühne 2012, and `PUMP_PRIOR_ART.md` says so.
