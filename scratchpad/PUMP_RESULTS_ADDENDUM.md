# PUMP results — ADDENDUM: the external calibration, run at last; and §2 confirmed independently

**Status.** `PUMP_RESULTS.md` stands and is good work; it has already folded in
`PUMP_INSTRUMENT_GATE.md`'s P-FORM finding faithfully, reporting the fired pointwise kill in its
own verdict grid. This addendum adds three things it does not have, one of which is the campaign's
**only external validation** and appears in it **zero times**.

Artifacts: `pump_schneidman_fig2.py` / `.json` / `.log`, `pump_verify_k4.py` / `.log`.

---

## A1. P-SCHNEIDMAN — the one external calibration, now run. PASSES on all four claims.

Every gate in this campaign so far has been **our own Lean checked against our own solver**.
`PUMP_PRIOR_ART_ADDENDUM.md` §A1 asked for the one that is not, `PUMP_INSTRUMENT_GATE.md` §6
listed it as the outstanding gap, and it is now run.

**Schneidman, Still, Berry & Bialek, PRL 91:238701 (2003).** `Core/Share.lean`'s `share` **is**
their `I_C^(3)` (their Eq. 6), so this is definitional, not analogical. 26-point noise grid, nine
panels, exact solver; spot-checked against the independent dense-grid solver at 18 panel points,
worst deviation **8.882e-16**.

### Fig. 1 — the noiseless table, exact

| gate | our `I` | our `I_C^(3)` | our `I_C^(2)` | paper |
|---|---|---|---|---|
| AND | 0.8113 | **0.0000** | **0.8113** | 0.8113 / 0.0 / 0.8113 |
| OR | 0.8113 | **0.0000** | **0.8113** | 0.8113 / 0.0 / 0.8113 |
| XOR | 1.0000 | **1.0000** | **0.0000** | 1.0 / 1.0 / 0.0 |

Four significant figures against a 2003 PRL table, from independent code.

### Fig. 2 — the published pump curve. All four of the paper's textual claims reproduce.

| the paper says | measured here | |
|---|---|---|
| "pure 2-body interactions such as **AND and OR show a 3-body interaction component** for some types of noise" | AND and OR under **output noise**: `I_C^(3)` rises 0 → **0.0761 bits**, peaking at q ≈ 0.10 | ✓ |
| "(**even for noise sources which are state dependent**)" | OR under **input-dependent** output noise: 0 → **0.6031 bits** | ✓ |
| "**input noise only changes the strength** of the existing interactions, rather than introducing a new kind of effective interaction" | input noise creates **exactly nothing** on all three gates — max `I_C^(3)` equals its q = 0 value in every case | ✓ |
| "for the pure 3-body XOR, **noise may result in the appearance of 2-body interactions**" | XOR under input-dependent output noise: `I_C^(2)` rises 0 → **0.1013 bits** | ✓ |

The AND/OR output-noise panel, in bits, is the published pump curve:

| q | 0.00 | 0.04 | 0.08 | 0.12 | 0.16 | 0.20 | 0.24 | 0.28 | 0.32 |
|---|---|---|---|---|---|---|---|---|---|
| `I_C^(3)` | 0.0000 | 0.0596 | 0.0759 | 0.0761 | 0.0684 | 0.0571 | 0.0449 | 0.0331 | 0.0226 |

**Why this matters beyond instrument validation, and it is the reason it should not have been
left out.** This campaign is *scooped on the phenomenon* by this exact paper
(`PUMP_PRIOR_ART_ADDENDUM.md` §A1). Reproducing its figure is simultaneously the instrument's only
external check **and** the citation being earned. `PUMP_RESULTS.md` §9 attributes the creation of
whole-only share by local noise to Zhou 2009 and Galla & Gühne 2012 — correct for the *theorems*,
but the **measured curve** is Schneidman 2003 Fig. 2, six years earlier and in the paper this
repository already cites for the quantity. §9's attribution paragraph should name it.

**Two further readings worth carrying into any results text:**

1. **The AND/OR output-noise panel has an interior peak** (0.0761 bits at q ≈ 0.10–0.12). Under
   GATES.md reach 3 an interior peak in a swept noise parameter is exactly what needs a mixture
   null. Here it is a **reproduction of a published figure, not a claim of ours**, so no null is
   owed — but the same shape in our own arms would owe one, and the `n`-sweep still does
   (`PUMP_PREREG_ADDENDUM.md` Finding 5).
2. **Symmetric noise creating order-3 at k = 3 is not a contradiction of `valve_needs_asymmetry`.**
   A fixed-probability flip is the binary symmetric channel — unital — and AND is **not**
   sign-symmetric. This is the published instance of the state-asymmetry pump
   (`PUMP_PRIOR_ART_ADDENDUM.md` §A2), and it is the reason the `a = 0` control is theorem-pinned
   **only on sign-symmetric inputs**. `PUMP_RESULTS.md` measures the channel-asymmetry pump; the
   state-asymmetry pump is Schneidman's, is published, and is out of this campaign's scope. That
   sentence belongs in §9.

---

## A2. §2 — the k ≥ 4 failure, independently confirmed, with the mechanism verified

`PUMP_RESULTS.md` §2 claims `valve_needs_asymmetry` is **false at k ≥ 4**. This is the campaign's
most consequential finding, so it was re-run from a separate script. **Confirmed, to the digit:**

| k, s | `PUMP_RESULTS.md` | this check |
|---|---|---|
| k=4, s=0.05 | 1.307e-02 | **1.306685e-02** |
| k=5, s=0.10 | 2.729e-02 | **2.729183e-02** |
| k=6, s=0.10 | 4.281e-02 | **4.280696e-02** |
| k=7, s=0.10 | 5.663e-02 | **5.662864e-02** |

with the input's share at ≤ 9e-15 and the output sign-symmetric to ≤ 5.6e-17 in every case, and
k = 3 flat at 0 to 3.3e-16.

**And the mechanism is now checked rather than asserted.** Under the global flip a Fourier
character transforms as `χ_S → (−1)^|S| χ_S`, so sign symmetry annihilates the **odd-|S|**
coefficients only. The **pair-blind** directions are `|S| ≥ 3`. Hence:

| k | pair-blind orders | odd (killed by sign symmetry) | **even (survive)** |
|---|---|---|---|
| **3** | {3} | 1 | **0** |
| 4 | {3,4} | 4 | **1** |
| 5 | {3,4,5} | 11 | **5** |
| 6 | {3,4,5,6} | 26 | **16** |
| 7 | {3,4,5,6,7} | 57 | **42** |

**The k = 3 vanishing is an accident of k = 3**: three slots is the only case where every
pair-blind direction is odd. Verified directly on the k = 4 output — the only non-zero Fourier
coefficients are the six pair terms at `κ² = 0.640000` and the single `|S| = 4` term at
`κ⁴ = 0.409600`, every odd coefficient identically zero. The surviving share is carried entirely
by that one even character.

This makes §2's finding stronger, not weaker: it is not an empirical surprise but a countable
structural fact, and the count `0, 1, 5, 16, 42` is why the symmetric-noise floor exists at all
and why it grows with k.

---

## A3. One number in the verdict grid is set by a floor-vs-floor comparison

`PUMP_RESULTS.md`'s grid reports **P-QPU-2 as "0.758 – 1.348 over 7 in-band delays."** The §5
table lists **six** rows, running 0.815 – 1.348. The missing seventh is **t = 0**, where:

| | |
|---|---|
| measured | 2.349e-04 nat |
| closed form | 3.097e-04 nat |
| ratio | **0.758** — the grid's lower bound |

At t = 0 **there is no pump**: `a = 5.1e-04`, `s = 3.1e-04`, and `QPU_HABIT_RESULTS.md` itself
calls the ferro arm's t = 0 reading of 0.00023 the hardware floor, not a signal. So the headline
range's lower end is a comparison of two numbers that are both at the readout floor.

**Excluding it, P-QPU-2 reads 0.815 – 1.348 over six delays.** The verdict is unchanged — both
ranges sit inside the staked [0.5, 2.0] — but the tighter number is the honest one, and the grid
and the table should agree. Recommend quoting **0.815 – 1.348, six delays**, with the t = 0 point
named as excluded and why.

---

## A4. WHAT THIS ADDENDUM DOES NOT DO

1. **Does not re-verify §§1, 3, 4, 6, 7.** Arm A's curve, the k-scaling refutation, the dose
   trajectories, the `0.227/N` estimator floor and arm F's lumpability condition are taken as
   `PUMP_RESULTS.md` reports them. §2 and the QPU overlay were re-run; the rest were not.
2. **Does not run Schneidman Fig. 2 with the independent dense-grid solver at every point** — that
   method is far too slow for 9 × 26 panels. It was spot-checked at 18 points (8.9e-16), and the
   two solvers were gated to 8.9e-16 over 4000 random states at `a4d3b38`.
3. **Does not supply the `n`-sweep's missing mixture null.** Still owed
   (`PUMP_PREREG_ADDENDUM.md` Finding 5).
4. **Adds no downstream mapping.** §8's licensing table is unchanged by anything here.

---

## A5. THE THREE AMENDMENTS THIS PLACES ON `PUMP_RESULTS.md`

| # | amendment |
|---|---|
| 1 | **Add P-SCHNEIDMAN to the gate table** — Fig. 1 exact, Fig. 2 all four textual claims — and name Schneidman 2003 Fig. 2 in §9 as the earliest **measured** curve, alongside Zhou 2009 and Galla & Gühne 2012 for the theorems |
| 2 | Add to §9's scope: the `a = 0` control is theorem-pinned **only on sign-symmetric inputs**; the state-asymmetry pump is published (Schneidman's AND/OR panels, a unital channel on an asymmetric state) and is **out of scope**, not absent |
| 3 | Quote P-QPU-2 as **0.815 – 1.348 over six delays**, with t = 0 named as excluded because both its terms sit at the hardware floor |

*No Lean touched, `lake` never run, nothing moves `Stance.lean`. The two repository corrections
named in `PUMP_RESULTS.md` §9 stand, and `PUMP_PRIOR_ART_ADDENDUM.md` §12 adds a third — the Kahle
credit sentence in `Core/Valve.lean`, whose primary text calls the question "unsolved" and whose
systems carry no noise at all.*
