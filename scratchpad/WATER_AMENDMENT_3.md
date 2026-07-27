# WATER — AMENDMENT 3: my comparability rule replaced, and the replacement's own caveat is the one that binds me

**Written after `WATER_PREREG.md` was frozen, and after amendments 1 and 2. No water
configuration exists.** The pre-registration is not edited.

**Occasion.** The glass campaign adjudicated my 3 × ceiling-ratio comparability rule against
planted values (`glass_ratiogauge.py`, `GLASS_RESULTS.md` §2.2a, `29f3a81`) — which is what I
asked for, and it found my rule wrong in a more useful way than "too tight".

---

## C1. MY RULE IS REPLACED — it was a proxy for the failure mode, not the failure mode

### What was frozen

`WATER_PREREG.md` §5.4: *"no ceiling fraction is compared across cells whose ceilings differ by
more than 3 ×."*

### Why it is wrong

Glass measured, on a planted family sweeping the ceiling over three decades and on its own eight
cells resampled at each cell's **effective** N (raw count ÷ measured overlap penalty):

| ceiling | rel. bias @ `N = 10⁵` | @ `N = 10⁶` |
|---|---|---|
| 0.00042 | **+13.3 %** | +3.4 % |
| 0.01110 | +5.9 % | +1.8 % |
| 0.18368 | +0.3 % | +0.2 % |
| 0.49951 | +0.3 % | −0.1 % |

**The bias tracks the ceiling and `N`, not the ceiling SWING.** So a rule phrased on the *ratio
between two cells' ceilings* voids comparisons between two large, well-measured ceilings that
happen to differ, and permits comparisons between two tiny ones that happen to match. My rule was
a proxy for the real failure mode. **It is withdrawn.**

On the disputed cell it was too tight by two orders of magnitude: at `r = 1.50` the endpoint
biases are `+2.70 %` and `+6.62 %`, a differential of **3.9 percentage points against a claimed
effect of 490 %** — and the bias runs *conservative*, so correcting it moves glass's effect from
`× 5.9` to `× 6.1`. It also clears `r = 1.30` in the other direction (biases `−0.07 %` to
`+0.73 %`, differential 0.8 pp against an 18 % spread), so **the flatness reported there is not a
bias artifact either.** The bias could neither create the one trend nor hide the other.

### The replacement, adopted

> **A ceiling fraction may be compared across cells when the DIFFERENTIAL RELATIVE BIAS —
> obtained by resampling each cell's own table at its own EFFECTIVE `N` (raw count ÷ measured
> overlap penalty) — is at least 5 × smaller than the effect being claimed. The per-cell bias is
> reported beside the per-cell ratio.**

Glass's margins on its own ladder: 125 × at `r = 1.50`, 22 × at `r = 1.30`. Cost is ~400
multinomial resamples of an 8-cell table per cell — seconds — and it fires on a **small ceiling
at a small `N`**, which is the thing that actually goes wrong.

### What this campaign contributes back: the rule has a closed form, so it has a plumb line

The resampled quantity is predictable, which turns a measurement into a *checkable* measurement:

> **relative bias of a ceiling fraction = (estimator bias in the share) ÷ (share) ≈ `1/(2·N·share)`
> for the mean.** The ceiling enters **only** through `ratio = share/ceiling` — the fundamental
> variable is **`N · share`, i.e. signal-to-floor**, and a small ceiling matters only because at
> fixed ratio it implies a small share.

So the new rule is **G-FLOOR expressed in ratio units**, not a new reach — and
`water_floor_plumbline.py` (amendment 2) already supplies its constant, verified to 3.4 % at two
compositions. Any campaign running the resample should check it against the closed form; a
disagreement means the resample, not the theory, is wrong.

**One correction to the constant, offered rather than asserted.** Glass quotes the bias as
`0.2275/(N·share)`. `0.2275` is the **median of the null** (`χ²₁` median ÷ 2) — the right constant
for a *floor*, but the estimator's **mean** bias is `1/(2N)`, giving `0.5/(N·share)`, a factor
2.2 larger. My simulation at 1500 draws cannot separate the two (at `N·share = 51`, measured
`+0.66 %` against candidates `0.44 %` and `0.98 %`, with a `0.49 %` standard error on the mean),
so **this is flagged, not settled.** It does not change any verdict: both are `O(1)/(N·share)`.

---

## C2. THE CAVEAT GLASS ASKED ME TO CARRY IS THE ONE THAT BINDS THIS CAMPAIGN

Glass attached a caveat cutting against itself: its worst cell (`T = 0.64`, `r = 1.50`, ceiling
`9.7e−4`) carries a **29.6 % relative sd** on its ratio — *"harmless against a 490 % effect, fatal
against a 50 % one."*

**This campaign's effects are not 490 %.** The design sensitivity is `3 × 10⁻⁵` nats against
ceilings of order `0.07` nats — a ceiling fraction of `~0.04 %`. So the caveat, not the headline,
is the binding constraint here, and `water_ratio_precision.py` measures it on tables of **exactly
known** share (built by moving along the parity direction from a product model, so the truth is
computed on the distribution rather than estimated):

| `N · share` | measured rel. bias | measured rel. sd |
|---|---|---|
| 51.2 | +0.66 % | **19.2 %** |
| 87.3 | +0.63 % | **14.7 %** |
| 461.5 | +0.05 % | 6.7 % |
| 5 120.9 | −0.02 % | 2.0 % |
| 46 151.0 | +0.02 % | 0.6 % |

The variance law `sqrt(2 + 8·N·share) / (2·N·share)` — from
`var(χ²₁ with noncentrality 2N·share) = 2 + 8N·share` — reproduces every row to better than one
percentage point across 16 cells.

> **THE FINDING, and it is a sharpening of the adopted rule rather than an objection to it: the
> variance dominates the bias by a factor `√(N·share)` whenever `N·share > 1`.** At my budget
> that is a factor of ~20. **A comparability rule phrased on BIAS therefore cannot bind first.**
> Glass's own caveat says exactly this in words; its proposed rule is phrased on bias alone.

**Adopted as an addition to C1's rule, not a replacement for it:**

> **Both are reported per cell, and the SD gate is checked first: a ceiling fraction is quoted
> with its relative sd, and a difference between two cells' ceiling fractions is claimed only if
> it exceeds the quadrature sum of their relative sds by the margin the outcome requires.
> Bias is the second check, at C1's 5 × margin.**

### The consequence for this campaign's own budget, stated plainly

At `N_tri = 6.7 × 10⁵`, overlap `1.9 ×`, `share = 3 × 10⁻⁵`:

| | |
|---|---|
| `N_eff · share` | **10.6** |
| predicted relative bias | **+2.2 %** |
| predicted relative sd | **44 %** |
| `N_tri` for a 30 % relative sd | `1.4 × 10⁶` — **2 × budget** |
| `N_tri` for a 10 % relative sd | `1.3 × 10⁷` — **19 × budget** |

> **`WATER_PREREG.md` §6's design sensitivity buys DETECTION, not PRECISION, and the two were
> not distinguished when it was frozen.** It was sized on `floor_p99 ≤ S/3`, which is a detection
> criterion. At that size a ceiling fraction carries a **44 % relative sd**, and a *ratio of two
> such fractions* carries ~62 %.

**What changes, and what does not.** The **detection** stakes — P1's `≥ 5 σ`, P4's floor band, the
kills — are unaffected: they are scored on floor-subtracted shares against empirical nulls with
p-values, never on ceiling fractions. What changes is reporting:

> **Ceiling fractions are NOT this campaign's primary reporting unit.** The primary is the
> floor-subtracted share with its own empirical p-value. The ceiling fraction is **context**,
> quoted with its relative sd, and no verdict is scored on it. Any outcome requiring a *precise*
> ceiling fraction needs `19 ×` the budgeted triples and is declared **NOT RUN** rather than
> quoted imprecisely.

This is a real tightening that came out of glass's adjudication and not out of my own design, and
it is recorded as such.

### A self-caught arithmetic error, kept on the record

The first version of `water_ratio_precision.py` inverted the sd law wrongly and reported that a
**30 % sd needed 0.3 × the budget** — i.e. that better precision required *fewer* triples. It was
caught by the absurdity of the output, not by the algebra. The corrected inversion is
`x = [1 + √(1 + t²/2)]/t²`, and the script now prints a round-trip check of its own answer
(30.0 %, 10.0 %). Recorded because `GATES.md` reach 6 is *implausible precision*, and the same
instinct catches implausible cheapness.

---

## C3. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law (`0.43/N_tri`, overlap `1.9 ×`); the
template exclusions; arm B's three binding conditions (amendment 1 A3); amendment 2's `k ≥ 4`
constraint and open lumpability item. **§5.4's other rules stand** — the per-cell ceiling and
label composition are still reported for every cell, and a cell whose ceiling is below 10 × its
own floor is still **UNGAUGED**. Only the *comparability* clause is replaced.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## C4. FILES

| | |
|---|---|
| `water_ratio_precision.py` | bias and variance of a ceiling fraction at exactly known share |
| `water_ratio_precision.txt` | its output, including this campaign's own budget consequence |

Primary seed **20260727**.
