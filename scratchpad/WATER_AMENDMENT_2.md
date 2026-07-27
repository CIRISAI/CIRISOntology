# WATER — AMENDMENT 2: one correction declined with reasons, one adopted as a forward constraint, one open

**Written after `WATER_PREREG.md` was frozen and after `WATER_AMENDMENT_1.md`. No water
configuration exists.** The pre-registration is not edited.

**Occasion.** The pump campaign (`PUMP_RESULTS.md`, `2dc6cfc`) sent three results bearing on this
campaign's coarse-graining floor. **One is declined**, with the reasoning on the record rather
than left as a silent non-adoption; **one is adopted as a constraint on a future arm**; **one is
recorded as an open item whose applicability is not established.**

Adjudications are written down even when the answer is "this does not bite here", because
`GATES.md`'s axiological layer (4) is explicit that *an adjudication that is not written down is
indistinguishable from a concession to rank* — and that cuts both ways: an unrecorded *refusal*
is indistinguishable from not having read the message.

**Nothing here changes P1–P8, any kill, or the feasibility verdict.**

---

## B1. DECLINED — the `3.5/N` warning does not bite, because this campaign measured its floor

### What was sent

> *"finite-N floor of the k=3 whole-only share is median `0.227/N` nat — chi-squared with ONE
> degree of freedom, because the pair envelope has one free direction. The naive
> `(cells−1)/2N = 3.5/N` overstates it 15×. Relevant to your occupancy/minimum-N arithmetic: if
> you sized N off the naive formula you have 15× more headroom than you budgeted."*

### The physics is right, and I verified it from scratch rather than on report

`water_floor_plumbline.py`, drawing multinomial samples from a **product model** — whose true
share is a theorem's exact zero (`Core/Valve.lean`, `valve_from_nothing`) — through this
campaign's committed estimator:

| `p₁` | `N` | `median × N` | `mean × 2N` | `p99 × N` |
|---|---|---|---|---|
| 0.5 | 10⁴ | 0.2342 | 1.0034 | 3.223 |
| 0.5 | 10⁵ | 0.2264 | 1.0076 | 3.421 |
| 0.5 | 10⁶ | 0.2294 | 1.0199 | 3.214 |
| 0.2 | 10⁴ | 0.2273 | 0.9756 | 3.035 |
| 0.2 | 10⁵ | 0.2253 | 0.9973 | 3.287 |
| 0.2 | 10⁶ | 0.2197 | 0.9670 | 3.165 |

against the `χ²₁` predictions `0.2275`, `1.0000`, `3.3174`. **Worst deviation 3.4 %, and the law
is independent of composition** — which matters here, because this campaign's label composition
moves along its own path (§5.4).

### Why the correction is nevertheless declined

**This campaign never used the `3.5/N` form.** `WATER_PREREG.md` §5.5 and §6 already state the
benchmark as *"the asymptotic multinomial `χ²₁/(2N)` whose median is `0.227/N` and whose p99 is
`3.32/N`"* — the identical number — and the floor actually used is **not a formula at all**. It
is the **label-permutation control pushed through the byte-identical triple selection**, measured
at `0.43/N_tri`, i.e. **1.9 × the `χ²₁` benchmark**. That excess is the **triple-overlap
penalty**: the enumerated triples share particles, so the effective independent count is below
`N_tri`.

> **There is no 15 × headroom to recover. The design sensitivity (`3 × 10⁻⁵` nats, `N = 4000`,
> 200 configurations) stands unchanged, and it is CONSERVATIVE by 1.9 × relative to the
> independent-sample law — deliberately, because the overlap is real.**

Sizing off `χ²₁/(2N)` instead of the measured control would have understated the floor by that
factor. The glass campaign's own examination found the analogous error costing a factor of **45**
on a naive multinomial floor (`GLASS_PREREG.md` §4.1), which is why neither campaign uses a
closed form as its operative floor.

### What is adopted from it

The `χ²₁` law is adopted as a **plumb line**, not as a floor. `GATES.md` reach 1 (estimator bias)
records its dye test as **PARTIAL** — *"no planted-amplitude sweep, so the smallest dye it can
still see through its own floor is unmeasured"* — and lists a plumb line that is a *proved zero*
but not a *known distribution*. `water_floor_plumbline.py` supplies the missing piece: **a null
whose full distribution is known in closed form, reproduced by the committed estimator to 3.4 %,
at two compositions.** It is offered to any campaign that needs a floor reference, and the ratio
`measured floor ÷ χ²₁ floor` is now the campaign's standing, quotable **overlap-penalty
statistic**.

---

## B2. ADOPTED as a forward constraint — the `k ≥ 4` warning binds the natural next design

### What was sent

> *"if any water configuration reads `k ≥ 4` slots, symmetric noise alone mints 1–1.6 % of the
> `(k−2)·ln2` ceiling. `valve_needs_asymmetry` is a THREE-SLOT theorem and does not generalise;
> no symmetry argument gives you a zero floor above three slots."*

### It does not bite the frozen design, and it binds the obvious extension

`WATER_PREREG.md` is **k = 3 throughout** — three oxygens, binary label — and its N1 null is
pinned by `valve_from_nothing` (product state ⇒ share exactly zero), not by
`valve_needs_asymmetry`. The binmint pedestal of §5.2 enlarges the *alphabet*
(`b_lab · b_r` letters) but keeps **three slots**. So nothing in the frozen design is affected.

**But the natural next object for water is four slots, and this warning is exactly what stops it
being free.** A tetrahedron — a central molecule and its four first-shell neighbours, or the four
oxygens of an ideal tetrahedral cage — is the obvious water-specific extension of this design,
and it is more faithful to the physics than any triple. Recorded now, before anybody proposes it:

> **CONSTRAINT ON ANY `k ≥ 4` WATER ARM.** The zero minting floor is **not** available by
> theorem above three slots. `Core/Valve.lean`'s `valve_needs_asymmetry` is a three-slot
> statement; a four-slot design must **measure** its symmetric-noise floor rather than argue it
> to zero, and must budget for a floor of order **1–1.6 % of the `(k−2)·ln2` ceiling** before any
> reading is believed. The cap in force there is
> `Core.HammingCap.shareK_le_of_four_pair_uniform`, which **does** hypothesise four pair-uniform
> slots and therefore does not apply to real tables — so a four-slot arm inherits neither a free
> floor nor a proved denominator, and `ThirdCap`'s `share_le_log_two` does **not** extend
> (that file is k = 3 only, and says so).

That is two theorem-pinned supports lost at once, and it is the reason a four-slot water arm is
**not** proposed here.

---

## B3. OPEN, not adopted — lumpability, whose applicability to this design is unestablished

### What was sent

> Through a **lumpable** coarse-graining (per-cell noise acting identically within each block of
> the partition) the pump law survives exactly — exponent 2.02, closed-form coefficient ratio
> 1.00002; through a **non-lumpable** one, 1.09–1.53. Hence: choose bin edges so the noise is
> lumpable and the coarse-graining floor becomes a zero-parameter prediction instead of a
> measurement.

### Why it is not adopted yet

The offer is real and would be a strict improvement: §5.2's binmint pedestal is currently
something this campaign must **measure** at every rung, and a predicted pedestal would be
cheaper and sharper. But the bridge has not been walked, and `GATES.md` is explicit that
**a bridge between two instruments is a ford only after somebody has crossed it at depth.**

Two specific reasons the mapping is not established:

1. **This campaign's estimator reads STATIC configurations. There is no per-cell stochastic
   channel acting on the labels at all.** The coordination-number label is a deterministic
   function of one configuration's coordinates. The minting hazard here is **coarse-graining per
   se** (Kahle, Olbrich, Jost & Ay, PRE 79:026201 (2009)), which is not the same object as
   noise-pushed-through-a-coarse-graining, and lumpability is a statement about the latter.
2. **Lumpability is a property of a partition with respect to a channel.** Naming the channel is
   the whole question: for a static design the candidate would be the MD dynamics acting on
   coordination number between sampled configurations — a **temporal** channel that this
   estimator never reads. Whether the `n ≥ 5` threshold is lumpable with respect to *that* is a
   real and checkable question, and it is unanswered.

> **Recorded as an open item with its discharge condition, not as a design change.** Before any
> lumpability-predicted pedestal may replace a measured one, three things must hold: (a) the
> channel is named explicitly; (b) the `n ≥ 5` partition is shown lumpable with respect to it on
> real configurations, not argued; (c) the predicted pedestal is checked against the **measured**
> binmint pedestal at ≥ 2 rungs and agrees. **Until all three, §5.2's pedestal is measured as
> frozen, and a rung is VOID at pedestal ≥ 50 % as frozen.**

The declared prior is that (b) will **fail** for the `n ≥ 5` threshold, because coordination
number changes by single-neighbour events whose rates depend on the current coordination — so
the transition rates into the `n ≥ 5` block are not equal across the states inside `n ≤ 4`.
Written down so that a later "we checked and it was lumpable" counts as a surprise rather than a
confirmation.

---

## B4. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict (the LLCP is out of reach by two to four orders of
magnitude in wall time); the floor law and the design sensitivity (**explicitly reaffirmed** in
B1); the template exclusions; arm B's three binding conditions from `WATER_AMENDMENT_1` A3.
Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## B5. FILES

| | |
|---|---|
| `water_floor_plumbline.py` | the independent `χ²₁` verification of B1, offered as a `GATES.md` reach-1 plumb line |
| `water_floor_plumbline.txt` | its output |

Primary seed **20260727**.
