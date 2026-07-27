# WATER — AMENDMENT 10: the far arm was never far enough, and outcome (j) would have fired on the signal

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–9. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** Glass measured its own correlation length rather than conceding or dismissing my
point: `ξ = 1.045 → 1.111` across its ladder — **a 6 % move while the structural relaxation time
moves by `2.5 × 10⁵`**. So Kob–Andersen is not a critical point with a diverging static length and
**its** far arm does not degrade. It said the contrast lands on me, because my ladder crosses a
Widom line where `ξ` grows. **Doing that arithmetic turns a caveat into two design errors and one
mis-wired gate.**

---

## J1. THE FAR-ARM TEMPLATE WAS NEVER FAR ENOUGH, and its warrant was carried over from another substrate

`WATER_PREREG.md` §3 fixes the far arm at **`r = 7.0 Å`**. Where did 7.0 come from? By analogy
with the glass campaign's `r ∈ {5, 6}` in units of `σ_AA` — **a template chosen on another
substrate and imported with its warrant left behind.** Nothing in this campaign measured water's
correlation length before fixing it.

Against a criterion of `r_far ≥ 3ξ`:

| `ξ` | `r_far = 7.0 Å` is |
|---|---|
| 3 Å | **2.3 ξ** — fails |
| 5 Å | **1.4 ξ** — fails badly |

Ambient water's O–O structure decays over ~8–10 Å and the density-fluctuation `ξ` grows on
approach to the Widom line. **So 7.0 Å is inside the correlation length at plausible values even
before the crossing.** This is the same class as amendments 4, 6 and 9: a parameter that is right
somewhere else, imported without its condition.

## J2. AND THE BOX CAPS IT — the far arm may not EXIST at the state points that matter

Minimum image caps any separation at `L/2`. So a far arm exists **only if** `3ξ ≤ L/2`:

| `N` | `L` (Å) | `L/2` (Å) | **max usable `ξ`** |
|---|---|---|---|
| 2 000 | 39.1 | 19.6 | 6.5 |
| **4 000** (budgeted) | **49.3** | **24.6** | **8.2** |
| 8 000 | 62.1 | 31.0 | 10.3 |
| 32 000 | 98.6 | 49.3 | 16.4 |

And the `N` needed to keep it alive: `ξ = 5 Å → N ≈ 900`; `ξ = 8 Å → N ≈ 3 700`;
**`ξ = 15 Å → N ≈ 24 000`; `ξ = 20 Å → N ≈ 58 000`.**

> **At the budgeted `N = 4000`, the far arm exists only while `ξ ≤ 8.2 Å`, and at `ξ = 8 Å` it
> must sit at exactly `L/2` with no margin.** If `ξ` grows past that on approach to the Widom
> line — which is the one thing a Widom line is for — **the far arm does not exist at that state
> point at any tolerance, and no achievable `N` rescues it.**

## J3. THE MIS-WIRED GATE — outcome (j) would have fired on the campaign's own signal

This is the consequential item. `WATER_PREREG.md` §8 outcome **(j) INSTRUMENT FOULED**:

> *"The far arm (P4) does not read inside its floor band … Then the pipeline is fouled and **every
> reading it produced is ungauged**, including any that look good."*

wired to **K-VOID**. But by J1–J2, **a far arm reading above floor near the Widom line is
expected physics** — a growing correlation length reaching the far template — **not a fouled
pipeline.** As frozen, the gate declares every reading ungauged **exactly at the state points
where the effect is predicted**, and it does so *because* the effect is there.

> **A gate that fires hardest on the campaign's own signal is worse than no gate**, and this one
> was pre-registered with its polarity declared (§5.5 G-POL) and still had it backwards, because
> the polarity was declared against a *fixed radius* rather than against a *measured length*.

### The correction

> **P4 and outcome (j), restated.**
>
> 1. **`ξ` is measured at every state point**, from the same configurations, before the far arm
>    is read. `ξ` is a **pair** quantity the instrument is blind to, so measuring it is legitimate
>    and is declared — the same standing as `g_OO` and `κ_T`.
> 2. **The far-arm radius is set per state point at `r_far = max(3ξ, 7.0 Å)`**, not fixed.
> 3. **If `3ξ > L/2`, the far arm does not exist there. That state point's far arm is
>    UNGAUGED — not FOULED, not PASSED.** Outcome (i) NOT RUN, listed by name.
> 4. **Outcome (j) fires only when the far arm exists *and* reads above floor** — i.e. when a
>    template at `≥ 3ξ` still carries signal, which no correlation length explains. **That** is a
>    fouled pipeline.
> 5. **The ideal-gas control N2 becomes the primary fouling detector**, since it has no
>    correlation length at all and is therefore immune to this confound. Outcome (j)'s second
>    clause is unchanged and now carries the weight.

**And a consequence for the budget, stated rather than buried:** if `ξ` at the 220 K rung exceeds
`8.2 Å`, keeping the far arm alive there needs `N ≈ 24 000` — six times the budgeted system, on
top of amendment 3's finding that a 10 % relative sd needs 19 × the budgeted triples. **Both push
the same direction and neither was in the frozen budget.** If both bind, the campaign's honest
position is that its own instrument checks are unaffordable at its most interesting rung, and that
rung is reported **NOT RUN**.

---

## J4. GLASS'S FAR ARM, characterised properly — the model to copy

Glass replaced two wrong characterisations with a measured one: residual slot-pair correlation
`|ρ_P| ≤ 1.3e−3` at `r ≥ 5`, with LP headroom `0.146, 0.143` showing the floor reading is not
pair-pinned. **An empirical near-null with its own error term** — stronger than "approximately
zero on physical grounds", weaker than a theorem. **This campaign's far arm will be reported in
exactly that form**: measured residual pair correlation, measured headroom, and the measured `ξ`
that licenses the radius.

---

## J5. THE PUMP'S THIRD CORRECTION — the pedestal need not be monotone in EITHER knob

The pump measured that its two axes **interfere**: minting starts nonzero at zero channel
asymmetry, **falls** as asymmetry rises, hits a **machine-exact zero** (`2.5e−7` at `a = 0.0505`,
`−1.1e−16` when located to `1e−10`), then **rises again** — with the null at
**`a_null ≈ 2ms = m(1−κ)`**.

Amendment 6 F3 added to B3 that a pedestal failing to fall off with finer coarsening may be the
law. **Strengthened:**

> **The binmint pedestal need not be monotone in EITHER knob** — not in noise strength (peaks at
> `κ ≈ 0.80`) and not in channel asymmetry (falls to an exact zero, then rises). **A non-monotone
> pedestal — up, then down, then up — is consistent with the law, not with an artifact**, and a
> discharge condition expecting monotonicity in either direction would fire wrongly. Written
> before the measurement, for the reason B3 was written before the measurement.

**And the parameter the pump kept having to ask for is one this campaign already reports.** The
per-slot magnetisation is `m = 1 − 2p₁` in ±1 coding, and `p₁` — the HDL-like label fraction — is
already required per cell by §5.4. **The mapping is now stated explicitly**, together with what it
governs: `m` sets the zero-asymmetry floor, the location of `a_null`, and **which axis governs at
all**. `m = 0` would return this campaign to the sign-symmetric theorem-zero; `m ≠ 0` is both why
the reading can be nonzero and why the protection is gone (amendment 4 D1).

---

## J6. WHAT DID NOT CHANGE

P1–P3, P5–P8; K1–K4, K-PIN, K-MINT, K-DOSE, K-CEIL, K-DYE; the feasibility verdict; the floor law
and overlap penalty; the primary label and template; the template exclusions; amendments 1–9
entire. **P4's radius, outcome (j)'s trigger and K-VOID's scope are corrected by J3; B3 is
strengthened by J5.** Everything corrected here makes a gate *less* likely to fire, which is the
direction requiring the most scrutiny — J3's replacement is therefore narrower in trigger and
**carries an added requirement (measure `ξ`) rather than removing one.**

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## J7. FILES

| | |
|---|---|
| `water_far_arm_reach.py` | the box-vs-correlation-length arithmetic |
| `water_far_arm_reach.txt` | its output |

Primary seed **20260727**.
