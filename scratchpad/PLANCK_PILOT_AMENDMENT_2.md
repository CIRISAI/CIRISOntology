# AMENDMENT 2 — WMAP carries a monopole and a dipole the surrogate does not

**Prompted by the re-run of Stage 1b under Amendment 1, which still failed. No share has been
computed on Planck or WMAP pixel values. The primary grid, the templates, the ladders, the test
statistic of §7.2 and VOID conditions V1–V7 are untouched.**

Amendment 1 diagnosed the WMAP `C_ℓ` deficit as healpy's analysis quadrature error at
`lmax = 3·nside − 1` and moved WMAP to `lmax = 1024, iter = 3`. **That diagnosis was wrong, and
the fix did not work**: leg 2 came back at `1.682e−02`, the same number to four significant
figures as before the change. The corrected diagnosis is below. Amendment 1's `lmax` and `iter`
changes are retained — they are correct on their own terms and the round trip they fix is real
(`0.99999999984`) — but they were not the cause.

---

## 1. THE NUMBER

The WMAP surrogate reproduced the data's `ξ(θ)` at the template separations to **1.682e−02** and
its total variance to **5.194e−03**, against a required `1e−03`.

The cause, measured directly:

> **`ℓ < 2` carries `5.194e−03` of the WMAP map's weighted harmonic variance** —
> `ℓ = 0`: `8.226e−04`, `ℓ = 1`: `4.372e−03`.

That matches the observed variance deficit to **four significant figures**. `phase_randomise`
zeroes `ℓ < 2` by construction — a monopole has no phase to randomise, and a randomly-oriented
dipole would be a *different sky*, not this one — so the surrogate has no `ℓ < 2` content while
the WMAP data map does.

The delivered maps' `ℓ < 2` content, measured as a full-sky least-squares projection:

| map | monopole / σ | \|dipole\| / σ |
|---|---|---|
| Planck `I_STOKES` | 2.65e−09 | 6.45e−08 |
| Planck `I_STOKES_INP` | 9.25e−05 | 2.34e−03 |
| **WMAP `TEMPERATURE`** | **2.87e−02** | **1.146e−01** |

**The WMAP 9-yr ILC as delivered carries a residual dipole at 11.5 % of the map's own standard
deviation, and a monopole at 2.9 %.** Planck's SMICA maps have theirs removed to 1e−8 and 2e−3.

---

## 2. WHY THIS IS A REAL HAZARD AND NOT A BOOKKEEPING DETAIL

A monopole and a dipole are a **deterministic, position-dependent offset** added to the
anisotropy field. Across the anchor positions the pipeline draws from, that is a *mixture of
shifted distributions*, and a mixture of shifted symmetric distributions is **not symmetric about
a single global threshold**. `share_eq_zero_of_signSymmetric` requires the joint to be invariant
under the global sign flip about the split point; a large-scale gradient breaks exactly that
hypothesis.

So this is not "0.5 % of the power in a band we do not care about." It is a **known minting
channel present in one map and absent from its own floor** — the asymmetry between data and
surrogate that a plumb line exists to catch. It was caught before the reading, which is the
entire reason `PLANCK_PILOT_PREREG.md` §10 orders V8 first.

Whether an 11.5 %-of-σ dipole would in fact have produced a measurable spurious reading is not
established here and is not claimed. What is established is that the data and its floor differed
in a component the theorem is sensitive to, and that the difference has been removed rather than
argued away.

---

## 3. THE AMENDMENT

**Both data maps have their full-sky `ℓ < 2` content removed before anything else is done to
them.** The operation, in `planck_pilot.py::remove_monodip`:

`monopole = mean(m)`, `d_i = 3·mean(m·v_i)`, `m ← m − monopole − d·v̂`.

HEALPix is an equal-area grid with exact quadrature for `ℓ ≤ 1`, so this least-squares fit **is**
the `ℓ < 2` harmonic projection: it removes `ℓ = 0` and `ℓ = 1` exactly and touches nothing else.
**It is not a filter**, and §3.2 of the pre-registration — no filter the instrument did not
already apply — is not breached: no `ℓ ≥ 2` mode is altered by any amount.

Applied to **both** instruments, so the treatment is uniform. On Planck it is a no-op at the
6.4e−08 level; on WMAP it removes the components tabulated above.

**V8 leg 2 compares `ℓ ≥ 2` on both sides**, since both sides now have nothing below it.

---

## 4. THE RESULT — V8 PASSES, ALL THREE LEGS, BOTH INSTRUMENTS

| leg | Planck (`lmax 4096`) | WMAP (`lmax 1024`) | bar |
|---|---|---|---|
| **1** exactness of construction, `max Δ\|a_ℓm\| / \|a_ℓm\|` | **4.014e−16** | **4.014e−16** | `< 1e−12` |
| **2** `ξ(θ)` at the templates' own separations, max \|ratio − 1\| | **1.264e−10** | **6.500e−10** | `< 1e−03` |
| **2** total variance, \|ratio − 1\| | **4.597e−11** | **4.642e−10** | `< 1e−03` |
| **3** surrogate skewness inside the mask | **+0.00425 ± 0.00542** | **+0.02278 ± 0.04716** | consistent with 0 |

Leg 2 improved by **eight orders of magnitude** on Planck and **seven** on WMAP. The residual
`~1e−10` is float64 accumulation in the Legendre sum, not a property of the surrogate.

For contrast, and because the record should carry it: the sky campaign's Stage 3 Gaussian control
failed this same check at a skewness of **+1.6688** (`SKY_REALDATA_RESULTS.md` §6 item 2). Both
surrogates here read `+0.004` and `+0.023` against ensemble scatters of `0.005` and `0.047`.

**V8 is DISCHARGED. Stage 2 may proceed.**

---

## 5. WHAT THIS DOES NOT CHANGE

The primary grid (72 cells), the twelve templates, the `b`-ladder, the surrogate counts, the
primary test statistic and its leave-one-out calibration, the pre-registered expectation of §7.1
and VOID conditions V1–V7 are **untouched**. No data reading has been taken.

Outputs: `scratchpad/planck_pilot/stage1_surrogate_sanity.json`,
`stage1_v8_powerweighted.json`, `stage1b_v8_amended.json`.
