# AMENDMENT 6 — the three §5–§7 changes Stage 0 forced

Written **after** the Stage-0 inventory and **before** any Stage-1 statistic. No `§6` quantity has
been computed on DESI data; nothing in this document was chosen after seeing a result, because no
result exists. The amendment exists because `SKY_BGS_PREREG.md`'s own Stage-0 row requires it:
*any discrepancy changing a §5–§7 choice triggers an amendment before proceeding.*

All three are consequences of measurement, and two of them make the campaign **weaker** than the
prereg assumed. Both are stated at full strength.

---

## A6.1 — §5.1 The sample is `BGS_BRIGHT`, and the prereg expected the other one

**Changed:** the primary sample is **`BGS_BRIGHT`** (NGC), not `BGS_BRIGHT-21.5`.

**By:** RULE S0-A, fixed before any DESI byte was read. `min n̄V_R` at `R = 15` is **19.94** for
`BGS_BRIGHT` against **3.18** for `-21.5` — a 6.27× margin, far outside the 20 % tiebreak, and the
same ordering under both readings of the trim clause.

**Why the prereg guessed wrong, stated plainly:** §5.1 reasoned that `-21.5`'s flat `n̄(z)` would
make it the better instrument despite a smaller density gain. The flatness is real — 2.4× dynamic
range against `BGS_BRIGHT`'s 2418× — but it is **flat at a low normalization**. A uniformly sparse
sample is not a better instrument than a trimmed dense one; it is a uniformly under-occupied one.
`-21.5` sits **5× below BOSS's own occupancy** at the primary scale, which would have made the
confirmation run a weaker instrument than the measurement it exists to confirm.

**What this does not license.** Choosing the denser sample does not recover the commissioned
premise — see A6.3.

---

## A6.2 — §5.2 The redshift range is `0.080 < z < 0.320`

**Changed:** from the assumed `0.1 < z < 0.4` to the **measured** `0.080 – 0.320`, being the span
S0-A's factor-of-3 trim retains on the chosen sample. `N` retained: **2 176 226** of 2 909 876.

**Consequence for the growth lever:** §5.2 already recorded the growth lever as dead on arrival at
`z_eff ≈ 0.3`. The trimmed range moves `z_eff` **down**, not up, so the lever is not merely dead
but further from reach. No claim in §5–§7 depended on it; this is recorded so no later reading
revives it.

---

## A6.3 — §7 `R★` is absent, and the density premise does not survive the selection function

Two separate weakenings, both measured.

**(a) `R★` ABSENT.** No `R ∈ {12, 10, 8, 6}` reaches `min n̄V_R ≥ 16.2`; `R = 12` gives 10.21.
The scored grid falls from *2 caps × up to 3 scales* to **1 cap × 2 scales (`R = 15`, `R = 10`)**.
`R = 10` runs at `min n̄V_R = 5.91` — **below BOSS's reference** — and is therefore an extension
scale with knowingly degraded occupancy. **Every report of an `R = 10` row must carry that
number**; it is not a second confirmation scale and must not be read as one.

**(b) The 10–100× density premise is ~1.2×.** The commission's figure describes `BGS_BRIGHT` at
low `z` over a small volume with a steep selection. Measured against BOSS's `n̄V_R = 16.2` at the
same scale, the usable trimmed sample delivers **19.94 — a 1.23× occupancy gain, not 10–100×.**

The prereg's §4 Route-2 extrapolation projected floor-versus-signal improvement from *"a BGS-like
`n̄V_R` of order 250 [to verify]"*. **The verified number is 19.94.** That extrapolation is
withdrawn: it was built on a figure an order of magnitude above what the selection function
permits, and any power or floor expectation resting on it is void.

**What survives.** The campaign remains a genuine **independent-survey** test of the BOSS reading
— different instrument, different systematics, different selection, ~2.2M objects against BOSS's
sample — which was always the primary reason to run it. What does **not** survive is the claim
that DESI buys a decisive density advantage. It buys independence, and about 20 % more occupancy.

---

## A6.4 — Mock assignment fixed (no change, recorded for completeness)

RULE S0-C is satisfied more strongly than the prereg anticipated. BOSS's Amendment 4 restricted
outcomes because *Patchy is not N-body*; DR1 ships **25 AbacusSummit N-body BGS realizations** plus
**1000 EZmocks**. Assignment: **AbacusSummit** for the closure/consistency arm Patchy could not
serve, **EZmock ×1000** for covariance and dispersion floors. Amendment 1's stream-processing
constraint stands.

---

## A6.5 — What has NOT changed

The kill conditions, the outcome definitions, the blinding discipline, the gate list, `P11`'s
sub-patch redesign (already specified inside RULE S0-B), and the unblind protocol are **unchanged**.
This amendment moves the instrument, not the standard of proof.

**Pre-registered expectation, restated under the amended design and staked now:** with occupancy
at 1.23× BOSS and one fewer scale, the confirmation run is **not** better powered than the
measurement it confirms. If BOSS's wounded reading was a floor artifact, this run should reproduce
the artifact, not the signal. **A confirmation here is worth what an independent instrument with
comparable occupancy is worth — no more — and the campaign will not claim otherwise on the basis
of DESI's raw object count.**
