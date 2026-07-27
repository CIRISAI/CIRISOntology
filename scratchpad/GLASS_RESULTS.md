# RESULTS — the whole-only order-3 reading of a supercooled liquid, swept in temperature

Pre-registered in `GLASS_PREREG.md` (commit `39191fd`), committed **before any share was
computed on any real configuration**, with the instrument and both of its examinations
(`glass_gate.py`, `glass_calib.py`) committed alongside it and run on synthetic data only. The
inventory (`GLASS_DATA.md`, `80a2d13`) came first and computed no share.

**SCOPE, first.** Two **simulated** glass formers — the 3D Kob–Andersen binary Lennard-Jones
mixture and a 2D ternary mixture, from `GlassBench` — **not experimental glasses**. A
measurement contributing to a decades-old dispute, **not a solution to the glass transition**.
The ladder bottoms out at the mode-coupling temperature and **does not reach `T_g`**. **Nothing
here bears on `wild-share`; nothing here moves `Stance.lean`.** No Lean file was opened, `lake`
was never invoked, nothing was pushed.

---

## THE HEADLINE

> **The whole-only compositional share grows strongly and monotonically as the liquid is
> supercooled — by a factor of 44 over the accessible ladder at the template where it is
> largest — and a pair-matched generative surrogate reproduces 82–89 % of it at every
> temperature.**

Both halves are the result. The raw quantity moves, decisively and in the direction the
thermodynamic picture predicts — monotone on all four rungs, exact-permutation `p = 0.0010`,
surviving exact count matching, and replicated in sign in two dimensions with a different
species count. But the part that is genuinely *not* reconstructible from the species-resolved
pair correlations is a **small and roughly constant fraction** of it: the surrogate grows on
cooling at very nearly the same rate the data does. **Most of what looks like growing hidden
order is the growth of the pair correlations themselves, read through a three-slot instrument.**

Under the honest paired error bar the beyond-pair excess is **consistent with zero at the warm
end of the ladder (`+0.96 σ`, `+0.46 σ` at `T = 0.64`) and `+3.8 σ` at the cold end**, rising
monotonically across all four rungs by factors of 6.3 and 58. Its growth, scored cold-against-hot
against its own paired bars, is **+2.7 σ and +3.7 σ** — support in the direction of the
thermodynamic picture, at a significance **below the 5 σ this campaign committed to in
advance**.

The reading is carried by **B-rich triples**. At `r = 1.30` the eight-cell state is dominated by
`AAA` (0.681) and `BBB` (0.130) — a **twelve-fold enrichment** of the all-small-particle triple
over its independent expectation — and **`P(BBB)` doubles on cooling**, 0.064 → 0.130 from
`T = 0.64` to `T = 0.44`. That is the small B species clustering at its own preferred separation
(`g_BB` peaks at 1.39), and it is the physical content of the signal.

---

## 1. THE SWEEP — 3D Kob–Andersen, 500 configurations per state point

Equilateral template of side `r`, tolerance 0.10, slots = species, exact `share_2x2x2`, no IPF.
Null = the **permutation control pushed through the byte-identical triple selection** (same
configurations, same triples; only the labels change). `p` is an **exact rank test** over 300
null draws, so `p = 0.0033` is its resolution floor and means *no null draw reached the data*.

| `r` | T = 0.44 | T = 0.50 | T = 0.56 | T = 0.64 | verdict |
|---|---|---|---|---|---|
| 0.89 | 2.37e−05 | 3.11e−05 | 4.19e−05 | 5.13e−05 | **VOID — pinned** (§4.1) |
| 1.07 | 5.6e−08 (p=0.53) | 5.5e−07 | 1.5e−08 (p=0.45) | 1.5e−06 | at floor; capped |
| **1.30** | **5.4315e−03** | **3.6490e−03** | **3.1346e−03** | **2.2563e−03** | **PRIMARY** |
| **1.50** | **2.6531e−03** | **1.0129e−03** | **5.0691e−04** | **6.1014e−05** | **PRIMARY** |
| 1.80 | 1.14e−05 | 2.90e−06 | −4.9e−09 | 6.9e−07 | **VOID — manufactured** (§4.2) |
| 2.10 | 7.5e−07 | 2.9e−06 | 1.6e−06 | 1.1e−06 | capped; non-monotone |
| 2.50 | 1.12e−05 | 1.22e−05 | 4.2e−06 | 6.4e−06 | capped; non-monotone |
| 3.00 | 1.08e−05 | 8.3e−06 | 3.8e−06 | 1.8e−06 | capped; cap noise 13.9× null |
| 4.00 | 3.8e−08 (p=0.45) | −6.2e−09 | −1.9e−08 | 1.3e−07 | **far arm, at floor** |
| 5.00 | 2.0e−10 (p=0.97) | −8.1e−09 | 1.6e−08 | 2.3e−08 | **far arm, at floor** |
| 6.00 | 5.5e−07 | 1.2e−07 | 4.1e−08 | 4.0e−08 | far arm; see §4.3 |

**Only two rungs survive every gate: `r = 1.30` and `r = 1.50`.** They are also, and not by
coincidence, the only two templates whose triples are **never capped** — see §4.3, where that
turns out to be the difference between a bit-reproducible reading and one that is not.

### 1.1 The trend, by an exact configuration-permutation test

The verdict is scored by pooling the two temperatures' **per-configuration** tables, reassigning
configurations at random to two groups of the original sizes, and reading the p-value off the
rank (2 000 permutations). This needs no error bar, which matters because §6.1 of the
pre-registration measured our block bootstrap to be **inflated by ~2.2×**.

| `r` | T = 0.44 | T = 0.64 | difference | `p` (two-sided) | exact `z` |
|---|---|---|---|---|---|
| **1.30** | 5.4315e−03 | 2.2563e−03 | **+3.1751e−03** | **0.0010** | **+10.2** |
| **1.50** | 2.6531e−03 | 6.1014e−05 | **+2.5921e−03** | **0.0010** | **+21.4** |

`p = 0.0010` is the resolution floor of 2 000 permutations: **no permutation of configuration
membership reproduced the observed difference.** Across the full four-point ladder both rungs
are **monotone**, with no exception:

* `r = 1.30`: 5.43 → 3.65 → 3.13 → 2.26 (×10⁻³) — a factor of **2.41** cold-to-hot.
* `r = 1.50`: 2.653 → 1.013 → 0.507 → 0.061 (×10⁻³) — a factor of **43.5**.

---

## 2. THE LOAD-BEARING GATE — the pair-matched generative surrogate

Positions held **fixed**; species resampled from the maximum-entropy distribution over species
assignments whose radial species correlation matches the data's, fitted by iterative Boltzmann
inversion (Shell's `S_rel` programme used to *build* the null), sampled with
composition-conserving swap moves. 100 configurations, 40 IBI iterations, 30 replicas.

**The surrogate reads nonzero, exactly as §4.4 said it would**, because a pair ensemble has
genuine triplet structure — the Kirkwood-superposition-violation physics. The deliverable is
the difference.

| `r` | T | data | surrogate | excess | **excess / data** |
|---|---|---|---|---|---|
| **1.30** | 0.44 | 5.3126e−03 | 4.5707e−03 ± 1.24e−04 | +7.42e−04 | **14.0 %** |
| | 0.50 | 3.7788e−03 | 3.1239e−03 ± 6.18e−05 | +6.55e−04 | 17.3 % |
| | 0.56 | 2.8426e−03 | 2.3186e−03 ± 5.92e−05 | +5.24e−04 | 18.4 % |
| **1.50** | 0.44 | 2.2370e−03 | 1.9853e−03 ± 5.57e−05 | +2.52e−04 | **11.2 %** |
| | 0.50 | 9.4133e−04 | 7.6261e−04 ± 3.49e−05 | +1.79e−04 | 19.0 % |
| | 0.56 | 4.5864e−04 | 3.7952e−04 ± 1.08e−05 | +7.91e−05 | 17.2 % |

**This table is SUPERSEDED by §2.1 and is kept only for what it establishes on its own: the
size of the surrogate.** At every temperature and both primary templates the pair-matched
generative null reproduces **81–89 %** of the reading. Whatever else is true, **the bulk of the
whole-only compositional share of a supercooled liquid is a restatement of its species-resolved
pair correlations.** The excess column here carries the WRONG error bar and no verdict is scored
on it; §2.1 rescores it with the right one, at 200 configurations and all four temperatures.

**Why the bar in that table is wrong.**
The data side carries its own configuration-level uncertainty, and it is comparable to the
excess. The right instrument is a **paired configuration bootstrap** — data and surrogate read
the *same* configurations and the *same* triples, so their common fluctuation cancels in the
difference. It was run at 200 configurations and 400 paired resamples:

### 2.1 The paired bootstrap, and what it does to K1

200 configurations, 400 paired resamples, all four temperatures:

| `r` | `T` | data | surrogate | **excess ± paired SD** | `z` paired | excess/data |
|---|---|---|---|---|---|---|
| **1.30** | **0.44** | 5.7173e−03 | 4.9137e−03 ± 8.16e−05 | **+8.036e−04 ± 2.14e−04** | **+3.76** | 14.1 % |
| | 0.50 | 4.2620e−03 | 3.7147e−03 ± 4.45e−05 | **+5.472e−04 ± 1.79e−04** | **+3.05** | 12.8 % |
| | 0.56 | 2.7205e−03 | 2.3017e−03 ± 8.45e−05 | **+4.188e−04 ± 1.48e−04** | **+2.83** | 15.4 % |
| | **0.64** | 2.1863e−03 | 2.0578e−03 ± 8.87e−05 | **+1.285e−04 ± 1.33e−04** | **+0.96** | 5.9 % |
| **1.50** | **0.44** | 2.3424e−03 | 2.0630e−03 ± 4.02e−05 | **+2.794e−04 ± 7.32e−05** | **+3.82** | 11.9 % |
| | 0.50 | 1.0125e−03 | 8.6815e−04 ± 1.56e−05 | **+1.443e−04 ± 5.14e−05** | **+2.81** | 14.3 % |
| | 0.56 | 5.6071e−04 | 4.5849e−04 ± 1.32e−05 | **+1.022e−04 ± 3.41e−05** | **+3.00** | 18.2 % |
| | **0.64** | 3.8703e−05 | 3.3878e−05 ± 2.60e−06 | **+4.825e−06 ± 1.04e−05** | **+0.46** | 12.5 % |
| 1.80 | 0.44 | 1.3898e−05 | 1.1437e−05 ± 4.98e−07 | +2.461e−06 ± 1.64e−06 | +1.50 | (rung VOID) |
| | 0.50 | 1.5185e−06 | 1.8340e−06 ± 2.06e−07 | −3.155e−07 ± 6.63e−07 | −0.48 | (rung VOID) |
| | 0.64 | 2.0870e−06 | 2.2415e−06 ± 5.39e−07 | −1.546e−07 ± 9.46e−07 | −0.16 | (rung VOID) |

**Against the surrogate ensemble's own spread the same excesses read 6.9–9.8 σ.** The gap
between that and 2.8–3.8 σ is the whole point of pairing.

**And the coldest-versus-hottest comparison is the campaign's sharpest single statement:**

> **At `T = 0.64` the beyond-pair excess is consistent with ZERO** — `+0.96 σ` at `r = 1.30` and
> `+0.46 σ` at `r = 1.50`. **At `T = 0.44` it is `+3.8 σ` at both.** The excess rises
> monotonically across all four rungs: `1.29 → 4.19 → 5.47 → 8.04` (×10⁻⁴) at `r = 1.30`, a
> factor of **6.3**, and `0.048 → 1.02 → 1.44 → 2.79` (×10⁻⁴) at `r = 1.50`, a factor of **58**.
> Scored cold-against-hot against their own paired bars, that growth is **+2.68 σ** at
> `r = 1.30` and **+3.72 σ** at `r = 1.50`.

So the beyond-pair sector is **not detectable at the warm end of the ladder and is detectable at
the cold end**, and its growth is a 2.7–3.7 σ effect. That is **support**, in the direction of
the thermodynamic picture, at a significance this campaign pre-committed to calling
insufficient. The excess as a *fraction* of the reading tells a flatter story — 5.9 → 15.4 →
12.8 → 14.1 % at `r = 1.30`, and 12.5 → 18.2 → 14.3 → 11.9 % at `r = 1.50` — with no monotone
trend at all.

**This makes the scoring of K1 turn on which σ is used, and that must be said plainly rather
than settled in the favourable direction.** K1's letter reads *"…fails to exceed the pair-matched
surrogate's share by more than **5 σ of the surrogate ensemble**"*. By that letter the excess
clears the bar at 9.8 σ and 6.9 σ and **K1 does not fire**. By the **paired** bootstrap — which
is the honest error bar, and which the pre-registration did not name because it was built after
the fact — the excess is **3.8 σ at both templates, below the 5 σ the pre-registration
demanded**, and by that reading **K1 fires**.

**We report the paired reading as the one to believe.** The pre-registration chose the wrong σ:
a surrogate-ensemble spread measures how much the *surrogate* wobbles between replicas and says
nothing about how much the *data* wobbles between configurations. So the correct verdict is:

> **The beyond-pair excess is real in sign at the three colder rungs (2.8–3.8 σ each) and
> consistent with zero at the warmest. Its growth across the ladder is +2.7 σ and +3.7 σ.
> Neither reaches the 5 σ this campaign committed to in advance. The claim is SUPPORTED, NOT
> CASHED.**

---

## 3. THE CONTROLS

### 3.1 The ideal-gas control — PASSES at every template

200 random configurations at matched density and matched composition, through the
byte-identical pipeline. **The template selection manufactures nothing:**

| `r` | 0.89 | 1.07 | 1.30 | 1.50 | 1.80 | 2.10 | 2.50 | 3.00 | 4.00 | 5.00 | 6.00 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| `p` | 0.98 | 0.17 | 0.54 | 0.28 | 0.97 | 0.59 | 0.35 | 0.94 | 0.93 | 0.81 | 0.08 |

No template reaches `p = 0.05`. This is the check on **template-selection minting** — selecting
triples by a geometric template is a selection on the configuration, and selection is a filter.
It reads clean.

It also gives the contrast that identifies the `r = 0.89` failure as **physics, not pipeline**:
the ideal gas has headroom **0.141** there, the glass **0.0002**.

### 3.1a The 2D replicate — P6 confirmed

The 2D ternary mixture, 300 configurations per temperature, ladder scaled to its own measured
first peak (0.89 against the 3D model's 1.07), species merged to binary (type 1 versus {2,3}),
`τ_α = 918 306` at `T = 0.23` against `2 200` at `T = 0.30` — a factor of **417** in relaxation
time across two points.

| `r` | T = 0.23 | T = 0.30 | cold / hot | gate |
|---|---|---|---|---|
| 0.89 | 7.3e−11 | 5.7e−09 | — | **VOID** — min cell 0 |
| 1.08 | 1.1995e−04 | 4.7704e−06 | **×25** | clean (headroom 0.35) |
| 1.25 | 3.6399e−03 | 1.0256e−03 | ×3.5 | **VOID** — min cell 0 / 24, headroom 0.013 |
| 1.50 | 1.8091e−03 | 9.6199e−05 | **×19** | clean (headroom 0.18–0.23) |
| **1.75** | **2.4452e−03** | **8.3013e−04** | **×2.9** | **best-gated**: headroom 0.37–0.39, min cell 28 698 |
| 2.08 | 7.8015e−04 | 1.0006e−03 | ×0.78 | opposite sign |
| 2.50 | 1.3460e−04 | 4.5668e−05 | ×2.9 | clean |
| 4.00 | 2.0062e−05 (p=0.31) | 2.8102e−05 (p=0.25) | — | **far arm, at floor** |

**P6 is CONFIRMED**: on every rung that passes its gates and is not the far arm, the share is
larger at the colder temperature — ×25, ×19, ×2.9 and ×2.9 — including the best-occupied rung
`r = 1.75`, where both temperatures read `p = 0.0033` with a min cell near 30 000. The one
sign disagreement, `r = 2.08` (×0.78), is disclosed rather than dropped. **A different
dimension, a different species count, a different interaction and a different reduced
temperature scale, and the direction replicates.**

The 2D far arm also reads at floor, which is a second, independent confirmation of P1.

Two structural differences from the 3D arm are worth stating and not smoothing over: the 2D
signal peaks at `r = 1.75`, i.e. **1.97× its own first-peak distance**, where the 3D signal
peaks at **1.21–1.40×** its own; and the 2D arm required an **alphabet merge** (3 species → 2),
which the 3D arm did not, so it carries a coarse-graining channel the primary design does not.

### 3.2 The product and permutation controls

Both read the floor at every template, and the difference between them — the finite-population
correction from holding the composition exactly — is below every quoted reading. The
**overlap penalty**, the factor by which the naive multinomial floor understates the real one, is
measured per reading and runs **2.7×–18.1×** at the primary templates. Using the naive floor
would have understated every null in this campaign by roughly an order of magnitude.

---

## 4. THE GATE REGISTER — three gates fired, and they took rungs down

### 4.1 G-LP, pair-pinning — **FIRED at `r = 0.89`**, exactly where §5.1 said it would

The pre-registration named this rung in advance: *"at the smallest template excluded volume may
make some species cells nearly empty (B–B contacts are strongly disfavoured in KA), which
squeezes the feasible interval… That is the cell to watch."*

Measured: headroom **0.0002** at `r = 0.89` against a reading of 2.37e−05 — a ratio of 12, above
the K-PIN bar of 3, but the minimum cell holds **72 counts** against the pre-registered floor of
**30**, and at `T = 0.44` the headroom is three orders of magnitude below every other template's.
**The rung is reported as VOID.** The prediction that made it a stress test was correct.

At the two primary templates the gate reads clean and wide: headroom **0.194–0.306** at
`r = 1.30` and **0.460–0.536** at `r = 1.50`, with headroom/reading ratios of **36–136** and
**202–7534**. **P4's numeric bar (headroom ≥ 0.30) is met at `r = 1.50` at every temperature and
at `r = 1.30` only at `T = 0.64`** — see the scorecard.

### 4.2 G-BINMINT, coarse-graining — **FIRED at `r = 1.80`**, and cleared the primaries

The fine object (slot = species × radial sub-bin), its pair-maxent at fine resolution, merged to
the analysis alphabet. The pedestal is share manufactured by the merge and by nothing else:

Pedestal as a percentage of the reading, all four temperatures, `b_r ∈ {2,3,4}`:

| `r` | T = 0.44 | T = 0.50 | T = 0.56 | T = 0.64 | verdict |
|---|---|---|---|---|---|
| **1.30** | 1.2–1.5 % | 1.1–1.5 % | 0.7–1.3 % | 0.7–1.1 % | **clean** |
| **1.50** | 0.2 % | 0.0 % | 0.0–0.1 % | 0.0–0.1 % | **clean** |
| 1.80 | 26–49 % | 214–343 % | 250–800 % | 106–213 % | **VOID — K-MINT fires** |

**At `r = 1.80` the geometric coarse-graining manufactures between one and eight times the whole
reading**, and the rung is dead at three of four temperatures outright (`≥ 50 %`); at `T = 0.44`
it sits in the 10–50 % band, which the pre-registration says must be carried as a quoted
systematic on every number in that rung — so nothing is cited from it either way. At the two
primary templates it manufactures **at most 1.5 %**, which is the design choice of §3.1 paying
off: with an atomic species alphabet the only coarse-graining left is geometric, and here it is
negligible.

### 4.2a G-DOSE, count-matched — **the trend survives exact count matching**

A second full pass with a cap of 1300 triples per configuration, which binds at every
temperature and both templates:

| `T` | `r = 1.30`: N | share | `r = 1.50`: N | share |
|---|---|---|---|---|
| 0.44 | 6.374e+05 | **5.4194e−03** | **6.500e+05** | **2.7416e−03** |
| 0.50 | 6.486e+05 | 3.6798e−03 | **6.500e+05** | 9.1674e−04 |
| 0.56 | 6.500e+05 | 3.1617e−03 | **6.500e+05** | 5.1812e−04 |
| 0.64 | 6.500e+05 | 2.2794e−03 | **6.500e+05** | 5.0944e−05 |

**At `r = 1.50` all four temperatures now carry an identical triple count — 650 000, to the
digit — and the share still spans a factor of 53.8**, larger than the 43.5 measured without
matching. At `r = 1.30` the residual count spread is 2 % and the span is 2.38. **The trend is
not a count effect**, and this is measured rather than argued.

### 4.3 A gate the pre-registration did NOT have, and it took four more rungs

Two Stage A runs, differing only in a per-state-point RNG seed, **agreed to the last digit on
the templates whose triples were not capped and disagreed on every capped one.** The seed was
irreproducible (`abs(hash(pt))`, salted per Python process) — a real bug, now fixed to a stable
CRC — but the disagreement it exposed is not a bug, it is a **hole in the null**:

> the empirical null holds the **triple selection fixed** and varies only the labels. It carries
> the label noise and the triple-overlap structure. It does **not** carry the variance the cap
> introduces by randomly subsampling the enumerated triples.

Measured directly (`glass_capnoise.py`, 8 independent cap draws, 150 configurations):

| `r` | capped? | reading | SD over cap draws | **cap SD / null median** |
|---|---|---|---|---|
| **1.30** | **no** | 5.5121e−03 | **0.00e+00** | **0.00** |
| **1.50** | **no** | 2.2807e−03 | **0.00e+00** | **0.00** |
| 1.80 | yes | 1.67e−05 | 8.87e−07 | **4.36** |
| 3.00 | yes | 9.64e−06 | 1.82e−06 | **13.89** |
| 5.00 | yes | 3.87e−07 | 4.09e−07 | **4.85** |
| 6.00 | yes | 1.35e−07 | 9.61e−08 | **1.58** |

**The two primary templates are bit-for-bit reproducible across independent cap draws — the
standard deviation is exactly zero, because they are never capped.** Every capped template
carries cap noise of **1.6× to 13.9×** its quoted null, so **its p-value is understated by that
factor and is not credited.** In particular:

* the nominally significant `r = 3.00` monotone trend (`z_exact = +4.76`) sits under a cap noise
  **13.9×** its null and is **not** reported as a detection;
* the `r = 6.00` far-arm point at `T = 0.44` read `p = 0.0033` in one run and `p = 0.85` in
  another with a different cap draw. **It is a cap fluctuation, not a signal.** Its magnitude,
  ~1e−7 nats, is **four orders of magnitude** below the primary reading.

This gate is offered to `GATES.md` as a new reach: **a null that fixes a random subsample is
blind to the subsampling.** Its known-bad anchor is this campaign's own `r = 6.00` point.

### 4.4 G-CERT, the solver bracket — **fires marginally, and is reported not waived**

The primary 2×2×2 reading is exact and uses no solver. For the fine binmint tables both IPF and
a dual/L-BFGS solve were run. `|ΔH(Q)|` ranges **2.4e−11 to 1.46e−8** against a pre-registered
bar of **1e−9**, and **20 of 36 rungs exceed it**.

**Reported as fired, with our reading, rather than re-scored quietly.** The bar was set without
allowing for the conditioning of a 512-cell IPF. What the two solvers actually disagree about is
`H(Q)` at the 1e−8 level; what they are being used to compute is the **pedestal**, and there
`ped_ipf` and `ped_dual` **agree to every digit printed on all 36 rungs** (e.g. `6.367e−05` and
`6.367e−05`). The verdicts the pedestal carries — 1.2 % versus 343 % — are nowhere near a
boundary that 1e−8 in `H(Q)` could move. This is the same treatment `REFUTER_RESULTS.md` §A5
gave its own float-precision band: the letter of the pre-registration is quoted, the reading is
given, and the disagreement between them is left visible.

### 4.5 G-DOSE — the count confound, and why it cannot carry the trend

Triples per configuration **rise with temperature**: 1330 → 1715 at `r = 1.30` (+29 %) and
3737 → 3981 at `r = 1.50` (+6.5 %). That is the **same direction** a floor artifact would take,
so it must be excluded rather than waved past. It is excluded by arithmetic: the null median at
`r = 1.30` is **1.99e−06** against a reading of **5.43e−03**, a ratio of **2 700**, so a 29 %
change in the floor moves the reading by ~6e−07 where the observed change is **3.2e−03** — five
thousand times larger. The count-matched pass (a cap of 1300, binding at every temperature and
both templates) is reported in §7.

---

## 5. THE SCORECARD — every pre-registered prediction, scored

| | prediction | outcome |
|---|---|---|
| **P1** | far arm (`r ≥ 5`) reads at floor | **CONFIRMED in magnitude** (≤ 5e−7 nats, 4 orders below primary); its **p-value is UNGAUGED** because the far arm is capped and §4.3's cap noise is 1.6–4.9× the null |
| **P2** | share **largest at the nearest-neighbour template**, decaying with `r` | **FAILED, decisively.** At `r = 1.07`, the measured `g_AA` first peak, the share is **at the floor** (`p = 0.53`). The structure lives at `r = 1.30–1.50`, between the first peak and the first minimum, and at the B–B preferred separation |
| **P3** | product control at floor; permutation control indistinguishable | **CONFIRMED** — both at floor at every template; ideal-gas control clean at all 11 (§3.1) |
| **P4** | LP headroom ≥ 0.30 nats at every read template | **SPLIT.** Met at `r = 1.50` (0.46–0.54) at all four temperatures; met at `r = 1.30` only at `T = 0.64` (0.306), reading 0.194–0.262 elsewhere; **failed outright at `r = 0.89`** (0.0002), which is the rung it was put in to catch |
| **P5** | ordering across `T` is monotone | **CONFIRMED at both primary templates**, all four rungs, no exception — and separately for the surrogate-subtracted **excess**, which is also monotone on all four (§2.1). Not monotone at the capped templates, which §4.3 explains |
| **P6** | 2D replicate agrees in sign | **CONFIRMED** (§3.1a) — cold exceeds hot by ×25, ×19, ×2.9, ×2.9 on every gated non-far rung of the 2D ternary mixture, including the best-occupied one; one rung (`r = 2.08`, ×0.78) disagrees and is disclosed |
| **P7** | binmint pedestal < 30 % at `Δ = 0.10` | **CONFIRMED with a large margin at the primaries** — 0.0–1.5 % — and **violated by an order of magnitude at `r = 1.80`** (214–800 %), which is why that rung is void |

**Two advance predictions failed (P2 outright, P4 in part) and both failures are informative.**
P2's failure relocates the phenomenon: whole-only compositional structure is *not* a
first-coordination-shell effect. P4's partial failure is the LP gate catching the rung it was
designed to catch.

---

## 6. THE KILLS

| kill | fired? | |
|---|---|---|
| **K1** — the campaign's own claim | **SPLIT — and it fires on the better error bar** | By K1's own letter ("5 σ **of the surrogate ensemble**") the excess clears at 9.8 σ and 6.9 σ and K1 does **not** fire. By the **paired** configuration bootstrap (§2.1), which is the honest bar, the excess is **3.8 σ** at `T = 0.44`, **2.8–3.0 σ** at the two middle rungs and **consistent with zero at `T = 0.64`** — all below the pre-registered 5 σ, so K1 **does** fire. We report the paired reading. The excess is **supported in sign, not cashed at the bar we set** |
| **K2** — the growth claim | **DID NOT FIRE** | monotone growth at both primary templates, exact permutation `p = 0.0010`, `z = +10.2` and `+21.4` |
| **K-VOID** — the instrument | **DID NOT FIRE** | far arm at ≤ 5e−7 nats, ideal-gas control clean at every template. The `r = 6.00` excursion is diagnosed as cap noise (§4.3), not as a fouled pipeline — and the diagnosis is a measurement, not an argument |
| **K-PIN** | **FIRED at `r = 0.89`** | headroom 0.0002. That rung is VOID; it takes nothing else with it |
| **K-MINT** | **FIRED at `r = 1.80`** | pedestal 214–800 % of the reading. That rung is VOID; it takes nothing else with it |
| **K-DOSE** | **DID NOT FIRE** | the count confound is 5 000× too small to carry the trend (§4.5) |
| **K-DYE** | **not discharged** | the surrogate's own dye test — plant a three-body species coupling and confirm the surrogate fails to reproduce it — **was not run**. §7 |

---

## 7. WHAT DID NOT COMPLETE — named, not omitted

`GLASS_PREREG.md` §7(h) requires every pre-registered arm that did not run to be listed by name
with its reason, and forbids scoring a verdict on it.

1. **A second, independent surrogate family.** Everything in §2.1 rests on ONE null generator —
   a radial-pair Ising model on the fixed point pattern. `GATES.md`'s harvest gate
   *null-construction sweep* requires any surrogate-normalised reading to be reported under at
   least two defensible null constructions, with the spread quoted as a systematic. **Only one
   was built.** That is the largest undischarged requirement on this result.
2. **`T = 0.64` in the surrogate arm.** The first Stage B run crashed on a `KeyError` before its
   fourth state point (the inventory file predated that data's arrival) and dumped only at the
   end, so its JSON was lost; the three completed state points survive in its log and are what
   §2 reports. Checkpointing was added afterwards. **The unpaired surrogate comparison spans
   three temperatures, not four.**
3. **The high-temperature liquid at matched density** (prereg §4.5): **not run.** GlassBench
   contains no such state point and it would have to be simulated by us. The pair-matched
   surrogate supersedes it on its own terms, but the field's own framing of the control is not
   discharged.
4. **The secondary local-order-parameter design** (prereg §3.2): **not run.** So nothing here
   reaches *geometric* amorphous order.
5. **The surrogate's dye test** (K-DYE): **not run.** By the pre-registration's own rule, a
   control that has not been shown to see the dye returns **ungauged**, not clean — so §2 and
   §2.1's surrogate comparison, and K1's scoring, both inherit that caveat.
6. **The scalene template grid and the tolerance ladder** (prereg §3.4): **not run.** Only the
   equilateral diagonal was scanned, which is exactly what `order3-probe-geometry` warns
   against, and the warning is recorded here as undischarged rather than argued away.
7. **The surrogate's residual sensitivity.** The IBI converged to `rms = 0.0065–0.0084` in
   `⟨σσ⟩` over 17–18 live radial bins, worst bin `0.025–0.028`, and was still falling at 40
   iterations. The `--sens` arm that would convert that residual into a **quoted systematic on
   the excess** — by deliberately de-converging `J` and measuring how far the excess moves — was
   implemented and **not run**. Since the excess is 11–18 % of the reading, a pair mismatch of a
   few per cent is not obviously negligible against it, and **this is the second-largest
   undischarged item after the missing second surrogate family**.

**Completed after the first draft of this document and folded in:** the count-matched pass
(§4.2a), the 2D replicate (§3.1a, P6), the full binmint table (§4.2), the cap-noise gauge
(§4.3), and the `T = 0.44` paired bootstrap (§2.1).

**The outcome-completeness entry, §7(g), is not invoked**: the decomposition of the reading into
signal, floor, pedestal and surrogate *was* performed at the two primary templates, and it is
what §2 and §4.2 report.

---

## 8. WHAT IS NOT CLAIMED

1. **Nothing about experimental glasses.** Two simulated model liquids.
2. **Nothing about the glass transition.** The ladder stops at `T_MCT = 0.435`; `T_g ≈ 0.3` is
   not reached, and no equilibrated dataset for this model reaches it.
3. **Nothing about geometric amorphous order.** This design reads the **compositional** channel
   only. A one-component glass has no species. The `r = 1.30` signal is B-particle clustering,
   and that is what it may be called.
4. **No priority.** `GLASS_PREREG.md` §1 records five prior programmes on the same physical
   question, including **Banerjee, Nandi, Sastry & Maitra Bhattacharyya (JCP 145:034502, 2016)**,
   who already traced the species-resolved `s_2` and `S_ex − S_2` **across temperature on this
   exact model**. The most this campaign may claim is a **different, non-negative** object and a
   sweep of it, and the honest novelty is narrower than the survey that commissioned it stated.
5. **No claim that the reading is large.** 5.4e−03 nats is **0.78 % of `ln 2`**, the
   machine-checked one-slot ceiling.
6. **No stance implication.** `wild-share` does not move.
7. **No claim about the surrogate's completeness.** It matches the radial species correlation to
   a residual of `rms = 0.0065–0.0084` (worst bin 0.028) after 40 IBI iterations, still falling,
   and the sensitivity of the excess to that residual was **not** measured. Nor was a second,
   independently constructed null built, which `GATES.md`'s null-construction-sweep gate
   requires before any surrogate-normalised number is quoted.

---

## 9. FILES

| | |
|---|---|
| `GLASS_DATA.md` | the inventory, no share computed — `80a2d13` |
| `GLASS_PREREG.md` | the pre-registration and the credit block — `39191fd` |
| `glass_share.py` | the instrument: exact 2×2×2 share, headroom LP, triangle enumeration |
| `glass_gate.py`, `glass_gate.json` | nine estimator checks, three theorem-pinned; synthetic only |
| `glass_calib.py`, `glass_calib.json` | the full-chain examination: null shape, overlap penalty, the difference test |
| `glass_run.py`, `glass_stageA.{json,log}` | the sweep, its controls and floors |
| `glass_surrogate.py`, `glass_stageB.log` | the pair-matched generative surrogate |
| `glass_gates.py`, `glass_gates.{json,log}` | the binmint pedestal, the fine LP, the IPF/dual certificate |
| `glass_capnoise.py`, `glass_capnoise.{json,log}` | §4.3, the cap-subsampling variance |
| `glass_analyze.py`, `glass_scorecard.json` | the exact configuration-permutation trend test |
| `glass_inventory.py`, `glass_inventory.json` | box, density, composition, `g_αβ(r)` |

Data held outside the repository. Primary seed **20260727**. Scratchpad only; no Lean file, no
`Stance.lean`, no audit, `lake` never run, nothing pushed. Research → scratchpad memo → Eric's
review.
