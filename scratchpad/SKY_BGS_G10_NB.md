# G10 under the NULL OF RECORD — the equilateral row has **no signal at all**, and the field is shot-noise dominated

`N_B` implemented and run on all 25 AbacusSummit realizations at `R = 10, b = 4`. This is the
construction the prereg registered for outcome (a), so **this — not the `N_A` run — is G10.**
**Still blind: mocks only.**

---

## NB.1 The prediction I recorded before running it, and how it landed

`SKY_BGS_G10.md` §G10.3 staked, before `N_B` existed: *on BOSS, `N_A → N_B` raised the floor by
24–50 %; if that transfers, equilateral's 8.2 % miss does not survive.* Measured:

| config | floor `N_A` | floor `N_B` | change |
|---|---|---|---|
| folded | 2.937e-4 | 4.264e-4 | **+45.2 %** |
| equilateral | 1.910e-3 | 2.252e-3 | **+17.9 %** |
| squeezed | 1.327e-3 | 1.325e-3 | −0.2 % |

**The floors rose, in the predicted direction and mostly in the predicted band** (+45 % and +18 %
against BOSS's 24–50 %). And the clipped fraction fell **0.350 → 0.109**, the same direction as
BOSS's 37 % → 3.5 %, though a 3.2× reduction rather than 10×.

The consequence I staked did land, but not by the route I named — see NB.2.

---

## NB.2 The verdict, and a defect in my own scoring caught before it was reported

| config | reading | floor | **floor / reading** | signal | miss | **G10** |
|---|---|---|---|---|---|---|
| folded | 7.968e-4 | 4.264e-4 | **53.5 %** | 3.704e-4 | 6.9 % | **PASS** |
| equilateral | 2.241e-3 | 2.252e-3 | **100.5 %** | **−1.07e-5** | — | **VOID — no signal** |
| squeezed | 1.352e-3 | 1.325e-3 | **98.0 %** | 2.685e-5 | 9.8 % | PASS (2 % headroom) |

**The equilateral floor now EXCEEDS the reading.** The manufactured component is larger than
everything the pipeline measures, so the gravitational signal is negative — there is no headroom
to close against, and the row is **VOID**.

**My scoring flag got this exactly backwards, and I am recording it rather than fixing it
quietly.** The coded criterion was `miss / signal ≤ 10 %` with no requirement that `signal` be
positive. With a negative signal it evaluated **PASS** — the worst possible reading of the worst
possible outcome. Corrected to require `signal > 0 AND miss ≤ 10 % of it`, and the stored JSON is
rescored. **The number was right and the verdict was inverted**, which is precisely the
substance-survives-warrant-fails failure this programme has a gate for; it was caught by looking
at *why* a −80.5 % figure printed, not by any check.

**And `squeezed`'s pass is not a result.** Its floor is 98.0 % of the reading, so its "signal" is
2 % of what is measured, and a 9.8 % closure on 2 % of a reading is a closure on nothing. Only
**folded** — floor 53.5 %, the configuration the manufacturing channel reaches least — has real
headroom and a real pass.

---

## NB.3 The number that explains all of it: **96 % of Fourier modes hit the shot-noise floor**

`fourier_clipped = 0.9598`. The shot-noise subtraction `|F|² − P_shot` zeroes **96 % of the
spectrum**. I built that diagnostic into the construction precisely because a subtraction that
zeroes most of the spectrum is a low-pass filter rather than a shot-noise removal — and it is
worth stating that this is **not** an implementation artefact but the physics of the cell:

At `R = 10` the sample carries `n̄V_R = 5.91` galaxies per smoothing volume (S0-D). A field with
~6 objects per resolution element **is** shot-noise dominated, and the measured `P_shot` sitting
at essentially the mean modal power is the direct statement of that. **There is very little
clustering signal above shot noise at this scale on this sample**, which is the same fact Stage 1
expressed as a trade-off and Amendment 6.3 expressed as "1.23× occupancy, not 10–100×."

---

## NB.4 G10 verdict, and where the campaign stands

**G10, under the null of record, on the only cell Stage 1 left admissible:**

> **folded PASS · equilateral VOID (no signal) · squeezed PASS on 2 % headroom**

One of three configurations survives with genuine margin. Per the prereg's table a G10 failure is
**VOID per row**, so `equilateral` is void at this cell — and `R = 15`, where equilateral would
have had headroom, is already dead on occupancy.

**What this campaign can still honestly do:** a measurement in the **folded** configuration at
`R = 10, b = 4`, carrying (i) a floor that is 53.5 % of the reading, (ii) an ensemble `σ` uncertain
by **±14.4 %** from suite size alone (RULE S2-A, whole-suite `n = 25`), (iii) **no cross-suite `σ`
closure** (RULE S2-B not runnable), and (iv) one configuration, not three, so no
shape-consistency check across configurations.

**What it cannot do:** confirm or refute BOSS's wounded reading at BOSS's own scale or in BOSS's
own configurations, because the scale is dead and two of three configurations are void or empty.

**My recommendation, and it is unchanged in substance from Stage 1 though the reasons are now
measured rather than projected: report this as a measured infeasibility with the folded row's
availability stated, and name DR2 as the successor instrument.** Running a single-configuration
measurement whose floor is half the reading, with a ±14 % σ and no cross-suite check, to
adjudicate a claim already wounded by its own refuter, buys a number that no one — including us —
should update on.

`wild-share` stays **open**. The BOSS reading stays **wounded and not cashed**. Nothing in this
campaign touched either, and that is the correct outcome for an instrument that was tested before
it was believed.
