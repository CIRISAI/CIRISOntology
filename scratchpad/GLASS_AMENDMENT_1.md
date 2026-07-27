# GLASS AMENDMENT 1 — four theorem citations audited, one wrong, one over-claimed

**The pre-registration is not edited.** `GLASS_PREREG.md` stays exactly as committed at
`39191fd`; this document records what is wrong in it and what the correct statement is, in the
house's own form (`SKY_REALDATA_AMENDMENT_1..5`). **No result changes**, and §4 says why in
detail rather than asserting it.

**Raised by the water campaign**, which read the Lean signature rather than the prose. Verified
here against `CIRISOntology/Core/Valve.lean` at the source before being accepted.

---

## 1. THE ERROR — `GLASS_PREREG.md` §3.1 point 4, line 192

The prereg reads:

> *"**The valve floor is zero.** There is no counting noise anywhere… `Core/Valve.lean`'s
> `valve_needs_asymmetry` gives a minting floor of exactly zero for a design with no asymmetric
> per-cell channel."*

The theorem's actual signature (`Core/Valve.lean:718–722`):

```lean
theorem valve_needs_asymmetry {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (h₁ : IsFlipCovariant K₁)
    (h₂ : IsFlipCovariant K₂) (h₃ : IsFlipCovariant K₃)
    {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) (hps : SignSymmetric p) :
    share (channel3 K₁ K₂ K₃ p) = 0
```

**It requires `SignSymmetric p`.** This campaign's slots are species at **80:20** composition, so
its states are **not** sign-symmetric and the theorem does not apply to them. The cited pin does
not hold. The sentence should have read, and is corrected to:

> **There is no counting noise anywhere — the configurations are exact particle coordinates from
> a deterministic integrator — so the design has no asymmetric per-cell channel of the kind that
> minted a 5.8× floor in the sky campaign. That is an argument about the DATA PIPELINE, not a
> theorem about the state, and no theorem pins it. Every floor this campaign quotes is measured
> (§4.1, §4.2), not pinned.**

---

## 2. THE OVER-CLAIM — §3.4, the far arm, line 257

The prereg calls the far arm *"a **theorem-pinned internal null on the real data**"* on the
grounds that *"at separations beyond the structural correlation length the three species are
independent, the state is a product state, and `valve_from_nothing` gives share exactly zero."*

Two things are wrong with that, and the second matters:

1. `valve_from_nothing` is about a **channel applied to** a product state. With no channel in
   play the direct statement is `share_prod3`, which `valve_from_nothing` invokes. Minor.
2. **The far-arm state is only ASYMPTOTICALLY a product state, not exactly one.** Species at
   `r = 5` or `6` are *nearly* independent; the theorem hypothesis is exact independence. So the
   far arm is a **physically motivated near-null, not a theorem-pinned one**, and calling it "the
   campaign's plumb line" against `GATES.md`'s standard — where a plumb line is a case whose
   right answer is *known*, not *expected* — was an over-claim.

**Corrected status of the far arm: an internal consistency check whose expected value is
approximately zero on physical grounds.** `GLASS_RESULTS.md` §4.3 already declines to credit its
one nominally significant point (`r = 6.00`, `T = 0.44`), having diagnosed it as cap noise, so
no reported number rests on the stronger reading.

**~~This campaign therefore has no theorem-pinned plumb line on real data.~~ — WITHDRAWN as an
over-correction**, on the water campaign's challenge, checked against `GATES.md` reach 1's own
definition of a plumb line: *"a known-clean sample sent through the identical pipeline, where the
right answer is not estimated but proved."* The **§4.1 iid control** meets all three clauses:

* **known-clean** — iid labels are an *exact* product state, not an approximate one;
* **proved** — `valve_from_nothing` gives exactly zero, with no hypothesis beyond `IsProb` on
  each factor;
* **identical pipeline** — real configurations, real template selection, real triple overlap;
  **only the labels change**.

**So this campaign does hold a theorem-pinned plumb line on real data**, and `GATES.md`'s
six-of-thirteen count should not be worsened on the strength of the retracted sentence.

**The narrower statement is the one that survives, and it is the interesting one:** *neither this
campaign nor any other has a plumb line on the real **labels**, and none can.* The proved zero is
available exactly when the labels are replaced by a construction whose answer is known; nothing
pins the answer when the data's own labels are used, **because that is what it means to be
measuring something.** §3.4's far arm was reaching for a plumb line on the real labels, and no
such object exists. The over-correction and the original over-claim were the same mistake in
opposite directions.

---

## 3. THE TWO CITATIONS THAT ARE CORRECT

Audited in the same pass rather than assumed:

* **§4.1, line 305 — the iid product control.** `valve_from_nothing` cited for *"the state is a
  product state, so share exactly zero"*. **Correct in substance**: the control draws each
  particle's label iid, which is genuinely `prod3`. (`share_prod3` is the tighter citation, since
  no channel is applied.)
* **§6 gate G2, line 512.** The gate constructs an explicit outer product via `einsum` and
  measures `4.4e−16` over 200 states. That IS `prod3`. **Correct.**
* **§4.2, the permutation control** — audited and found **already correct**, because it makes no
  theorem claim at all: it states in the prereg that a permutation of a fixed multiset *"is not
  iid: it carries a finite-population correlation of order `1/N ≈ 2.4 × 10⁻⁴`"*, keeps it
  separate from §4.1, and reports the difference as the gauge. **A permutation control must not
  be pinned by `valve_from_nothing`**, and this one is not.

---

## 4. WHAT DOES NOT CHANGE, AND WHY

**No reading, no floor, no gate verdict and no kill scoring moves.** The reason is structural
rather than lucky: **this campaign never used a theorem as a floor.** Every floor quoted in
`GLASS_RESULTS.md` is the empirical permutation control pushed through the byte-identical triple
selection — the construction forced on it by the ideal-gas control, which showed a formula-based
floor to be 45× too small. The theorems appear in the prereg as *design justification*, and a
wrong design justification for a floor that was measured anyway costs a sentence, not a number.

`GLASS_RESULTS.md` §7a(b) already states the two-hypothesis form of `valve_needs_asymmetry`
correctly and already records that the campaign quotes empirical floors rather than leaning on
the theorem.

---

## 5. THE PROCESS FAILURE, WHICH IS THE PART WORTH KEEPING

The two-hypothesis structure of `valve_needs_asymmetry` was pointed out by the pump campaign
**before** this amendment, and `GLASS_RESULTS.md` §7a(b) was corrected for it. **I fixed the
instance I was shown and did not sweep for the class** — the same error was sitting in the
pre-registration, in the very sentence the results section was correcting, and it took a second
agent reading the Lean signature to find it.

**The rule this earns, stated generally:** *when a correction lands on a citation, re-audit every
citation of that object in every document of the campaign, not only the one that was pointed at.*
Cheap — this audit was four `grep` hits and one `sed` of the source — and it is the difference
between fixing an error and fixing an error class.

Two agents in this campaign have now recorded a gate that was **right for a reason its author got
wrong** (the water campaign's §5.1, twice; this campaign's P4 headroom stake). This is the same
family: a claim whose *substance* survives and whose *warrant* does not. The substance surviving
is not evidence that the warrant was checked.

---

## 6. ONE NUMBER CONTRIBUTED, from this campaign to a shared finding

The effective-count gap — the factor by which a floor formula keyed on the enumerated sample size
understates the real floor — now has a measured range across three substrates and four regimes:

| regime | gap |
|---|---|
| iid multinomial; and this campaign's capped far arm, where triple collisions are rare | **1.0×** |
| water campaign, tetrahedral network | 1.9× |
| **this campaign, triples sharing particles at the primary templates** | **5.8–7.9×** |
| **this campaign's synthetic ideal gas, nearest-neighbour template** | **45×** |

**`0.227/N` is a benchmark and a plumb line, never an operative floor on overlapping samples**,
and the error runs against whoever makes it.

---

Scratchpad only; no Lean file opened, `Stance.lean` untouched, `lake` never invoked, nothing
pushed. `GLASS_PREREG.md` is unedited at `39191fd`.
