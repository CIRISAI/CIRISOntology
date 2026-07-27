# WATER — AMENDMENT 4: a theorem hypothesis I under-stated, and a mis-pin of my own it exposed

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–3. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** The pump campaign corrected amendment 2's statement of `valve_needs_asymmetry`
(`fbcb3ea`) and answered the lumpability question in the negative. **Verifying its correction
against the Lean made me check my own citation, and I found the same class of error in my own
frozen §5.1.** That one is the substantive item here.

---

## D1. CORRECTION ADOPTED — `valve_needs_asymmetry` has two hypotheses, and I stated one

`WATER_AMENDMENT_2.md` B2 said: *"`valve_needs_asymmetry` is a THREE-SLOT theorem and does not
generalise."* True but incomplete. Verified in the source
(`CIRISOntology/Core/Valve.lean:719–725`):

```
theorem valve_needs_asymmetry {K₁ K₂ K₃ : Bool → Bool → ℝ} (hK₁ : IsKernel K₁)
    (hK₂ : IsKernel K₂) (hK₃ : IsKernel K₃) (h₁ : IsFlipCovariant K₁)
    (h₂ : IsFlipCovariant K₂) (h₃ : IsFlipCovariant K₃)
    {p : Bool × Bool × Bool → ℝ} (hp : IsProb p) (hps : SignSymmetric p) :
    share (channel3 K₁ K₂ K₃ p) = 0
```

**`(hps : SignSymmetric p)` — the INPUT must be sign-symmetric**, on top of three slots and
flip-covariant kernels. And the consequence is broader than the `k ≥ 4` case that prompted it:

> **`valve_needs_asymmetry` offers no minting protection on a non-sign-symmetric input EVEN AT
> `k = 3`.** This campaign's coordination-number state is generically *not* sign-symmetric — §2
> and §4.3 argue exactly that, since LDL and HDL are not related by any symmetry — so the theorem
> would not have applied here in any case.

---

## D2. A MIS-PIN OF MY OWN — `WATER_PREREG.md` §5.1's N1 is pinned to a theorem it does not satisfy

### What is frozen

§5.1's null table pins **N1** — *"label **permutation** on the byte-identical triple list … only
the labels move"* — with *"`valve_from_nothing`: product state ⇒ share exactly 0"*.

### Why that is wrong

`valve_from_nothing` (`Core/Valve.lean:317–322`) takes its input as `prod3 p₁ p₂ p₃` — an
explicit **product** state. **A permutation of a fixed multiset is not a product state.** It is
an exchangeable draw *without replacement*, carrying a finite-population correlation of order
`1/N`. The theorem does not apply to it.

**The glass campaign got this right and I collapsed it.** `GLASS_PREREG.md` keeps two controls:
§4.1 a product control (iid Bernoulli, correctly pinned by `valve_from_nothing`) and §4.2 a
permutation control, with the explicit note that *"a permutation of a fixed multiset is not iid:
it carries a finite-population correlation of order `1/N`… and is not obviously below the floor"*,
and the difference between them reported as the gauge of that correlation. My §5.1 merged the two
into one row and attached the product state's theorem to the permutation control.

### The correction, superseding §5.1's N1

> **N1a — PRODUCT control (theorem-pinned).** Labels drawn **iid Bernoulli** at the ensemble
> composition, through the byte-identical triple selection. A product state, so
> `valve_from_nothing` gives share **exactly zero** and whatever is read is the finite-sample
> floor. **This is the floor of record.**
>
> **N1b — PERMUTATION control (not theorem-pinned).** Labels **permuted within each
> configuration**, holding the composition exactly. Not a product state; carries a
> finite-population correlation of order `1/N`.
>
> **Both are run, and the DIFFERENCE between them is reported as the gauge of the
> finite-population term. Any reading smaller than that difference is UNGAUGED.**

**Does this change the stage-0 numbers?** No, and the reason is worth stating rather than
assuming: `water_feasibility.py` drew its null by `rng.permutation(lab)` — N1b, not N1a — so the
measured floor law `0.43/N_tri` is a **permutation** floor. At `N ≈ 1700–1900` particles the
finite-population term is of order `1/N ≈ 5 × 10⁻⁴` and enters the share at second order, far
below the measured floor; and the floor law agrees with the independent-sample `χ²₁` benchmark to
a factor of 1.9 that is fully accounted for by triple overlap (amendment 2 B1). **So the number
stands, but it was not entitled to the theorem it was quoted with, and the entitlement is what
this amendment restores.**

**This is the second time in this campaign that a gate was right for a reason I got wrong**
(amendment 1 A1 was the first). Recorded as a pattern, not as two incidents.

---

## D3. THE `k ≥ 4` CONSTRAINT, restated with the third loss

Amendment 2 B2 named two losses above three slots. There are **three**:

> **A `k ≥ 4` water arm loses (1) the theorem-pinned zero minting floor, (2) the proved
> denominator — `ThirdCap` is `k = 3` only and says so, and
> `shareK_le_of_four_pair_uniform` hypothesises four pair-uniform slots, which no real table
> satisfies — and (3) any protection from input symmetry, since `valve_needs_asymmetry`'s second
> hypothesis fails on a non-sign-symmetric state.**
>
> **And a UNITAL channel is enough to mint once either hypothesis goes.** The published instance
> is not ours and is not new: **Schneidman, Still, Berry & Bialek (2003), Fig. 2** shows a
> per-cell unital flip creating **0.0774 bits** on AND — re-measured independently by the pump
> campaign.

The tetrahedral cage remains the natural next object for water, and remains **not proposed**.

---

## D4. LUMPABILITY — answered in the negative, prior strengthened, condition unchanged

Amendment 2 B3 asked whether lumpability holds anywhere for a threshold on an integer count under
a **physically realised** channel. **The answer is no.** The pump campaign's lumpable control was
**constructed by hand** — a four-letter channel built to act identically within each block,
specifically as a dye test proving its instrument could see the law through a coarse-graining at
all. It is an existence proof about an instrument, **not** evidence that any natural partition is
lumpable with respect to any physical channel.

> **B3's three-part discharge condition is unchanged, and its declared prior is strengthened: the
> only known lumpable case in the neighbouring campaign is hand-built, so there is currently NO
> positive evidence anywhere that a physically realised channel is lumpable with respect to a
> natural partition.** §5.2's binmint pedestal is measured, as frozen.

---

## D5. THE OVERLAP PENALTY NOW HAS A MEASURED RANGE ACROSS THREE CAMPAIGNS

Three substrates have now measured the ratio between the enumerated count and the effective
independent count:

| construction | penalty over `χ²₁/(2N)` |
|---|---|
| iid multinomial from an exact 8-cell distribution (pump, arm G) | **1.0 ×** (exact by construction — no tuple overlap) |
| triples subsampled under a cap so collisions are rare (glass) | ~1.0 × |
| triples at a template on a tetrahedral network (water, stage 0) | **1.9 ×** |
| triples sharing particles in a dense liquid (glass) | **5.8 – 7.9 ×** |
| dense ideal gas (glass) | **45 ×** |

> **The enumerated count is not the effective count, the gap ranges over a factor of 45, and it
> must be MEASURED per reading. `0.227/N` is a benchmark and a plumb line, never an operative
> floor on overlapping samples.** Two campaigns reached this independently from different
> substrates, which is stronger than either derivation.

---

## D6. A CORRECTION OWED TO THE GLASS CAMPAIGN

`GLASS_PREREG.md:192` (§3.1 point 4) cites **`valve_needs_asymmetry`** for *"a minting floor of
exactly zero for a design with no asymmetric per-cell channel."* By D1 that theorem also requires
a **sign-symmetric input**, and at 80:20 species composition the state is not sign-symmetric — so
the pin does not hold as cited.

**The substance is probably fine and only the citation is wrong**: that campaign's actual product
control (§4.1, §4.3, gate G2) is an **iid** draw, correctly pinned by `valve_from_nothing` at
three other places in the same document. The one line at §3.1 point 4 reaches for the wrong
theorem. Reported precisely, and not overstated.

---

## D7. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law `0.43/N_tri` and the overlap penalty
`1.9 ×` (D2 explains why the number survives its re-pinning); the template exclusions; amendment
1's arm B conditions; amendment 3's sd-then-bias comparability rule and the demotion of ceiling
fractions to context. Scope unchanged: simulated water models only; nothing bears on
`wild-share`; `Stance.lean` untouched; no Lean file opened; `lake` not run; nothing pushed.

Primary seed **20260727**.
