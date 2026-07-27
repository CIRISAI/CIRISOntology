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
> largest, and 54 after exact count matching — and a pair-matched generative surrogate
> reproduces 82–94 % of it at every temperature.**

Both halves are the result. The raw quantity moves, decisively and in the direction the
thermodynamic picture predicts — monotone on all four rungs, exact-permutation `p = 0.0010`,
surviving exact count matching, and replicated in sign in two dimensions with a different
species count. But the part that is genuinely *not* reconstructible from the species-resolved
pair correlations is a **small and roughly constant fraction** of it: the surrogate grows on
cooling at very nearly the same rate the data does. **Most of what looks like growing hidden
order is the growth of the pair correlations themselves, read through a three-slot instrument.**

Under the honest paired error bar the two surviving templates **disagree about the growth
question**, and the disagreement is the honest result. At `r = 1.50` the beyond-pair excess is
**exactly zero at the warm end** (`−0.06 σ`), rises monotonically, and reaches `+3.82 σ` at
`T = 0.44` — growth of **+3.79 σ**, the shape the thermodynamic picture predicts. At `r = 1.30`
the excess is `+2.3` to `+3.8 σ` at *every* temperature, is not monotone, and grows by only
**+1.91 σ**. Neither reaches the 5 σ this campaign committed to in advance.

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
generative null reproduces **82–94 %** of the reading (this table, at 100 configurations,
81–89 %; §2.1's, at 200, 82–94 %). Whatever else is true, **the bulk of the
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
| | 0.56 | 2.7205e−03 | 2.3955e−03 ± 9.59e−05 | **+3.250e−04 ± 1.43e−04** | **+2.28** | 11.9 % |
| | **0.64** | 2.1863e−03 | 1.8453e−03 ± 5.43e−05 | **+3.411e−04 ± 1.15e−04** | **+2.97** | 15.6 % |
| **1.50** | **0.44** | 2.3424e−03 | 2.0630e−03 ± 4.02e−05 | **+2.794e−04 ± 7.32e−05** | **+3.82** | 11.9 % |
| | 0.50 | 1.0125e−03 | 8.6815e−04 ± 1.56e−05 | **+1.443e−04 ± 5.14e−05** | **+2.81** | 14.3 % |
| | 0.56 | 5.6071e−04 | 4.6388e−04 ± 1.48e−05 | **+9.683e−05 ± 3.67e−05** | **+2.64** | 17.3 % |
| | **0.64** | 3.8703e−05 | 3.9300e−05 ± 2.56e−06 | **−5.968e−07 ± 9.47e−06** | **−0.06** | −1.5 % |
| 1.80 | 0.44 | 1.3898e−05 | 1.1437e−05 ± 4.98e−07 | +2.461e−06 ± 1.64e−06 | +1.50 | (rung VOID) |
| | 0.50 | 1.5185e−06 | 1.8340e−06 ± 2.06e−07 | −3.155e−07 ± 6.63e−07 | −0.48 | (rung VOID) |
| | 0.64 | 2.0870e−06 | 2.2415e−06 ± 5.39e−07 | −1.546e−07 ± 9.46e−07 | −0.16 | (rung VOID) |

**A CORRECTION, and how it was caught.** An earlier revision of this table quoted
`+4.188e−04 (z = +2.83)` and `+1.285e−04 (z = +0.96)` at `T = 0.56` and `T = 0.64`,
`r = 1.30`, and `+1.022e−04` and `+4.825e−06` at `r = 1.50`. **Those numbers were from a
different run.** Two paired-surrogate processes were accidentally started ninety seconds apart
and wrote the same log and the same JSON; the draft was written from the first, and the second
— whose output is what `glass_stageB_paired.{json,log}` now contain, and which is what is
committed — overwrote it. Every number in the table above was re-read from the committed JSON
and cross-checked against its log line by line. This is `GATES.md`'s **gate-log provenance**
reach firing on us: *a committed log must be reproducible from the instrument committed beside
it.* The two runs differ only in the GPU RNG, which the surrogate does not seed — a real
reproducibility defect, now on the record and not yet fixed.

**Against the surrogate ensemble's own spread the same excesses read 6.9–9.8 σ.** The gap
between that and 2.8–3.8 σ is the whole point of pairing.

**The coldest-versus-hottest comparison, and the two templates do NOT say the same thing:**

> **At `r = 1.50` the beyond-pair excess is EXACTLY ZERO at the warm end** — `−0.06 σ` at
> `T = 0.64` — rises **monotonically** across all four rungs (`−0.001 → 0.97 → 1.44 → 2.79`,
> ×10⁻⁴), and reaches `+3.82 σ` at `T = 0.44`. Scored cold-against-hot against its own paired
> bars that growth is **+3.79 σ**.
>
> **At `r = 1.30` it says something different.** The excess is `+2.3 σ` to `+3.8 σ` at *every*
> temperature including the warmest, and it is **not monotone** (`3.41 → 3.25 → 5.47 → 8.04`,
> ×10⁻⁴, with `T = 0.64` above `T = 0.56`). Cold-against-hot the growth is only **+1.91 σ**.

So the two surviving templates give **different answers to the growth question**, and that is
reported rather than averaged. `r = 1.50` behaves the way the thermodynamic picture predicts —
nothing beyond pairs at the warm end, a monotone rise, +3.8 σ at the cold end. `r = 1.30` shows
a beyond-pair excess that is present at *all* four temperatures and does not clearly grow.
**A single number for "does hidden order grow" cannot be extracted from this campaign**; what
can be said is that at one of the two clean templates it grows at 3.8 σ and at the other it is
present throughout at ~3 σ without a clear trend.

The excess as a *fraction* of the reading is flat at both — 15.6 → 11.9 → 12.8 → 14.1 % at
`r = 1.30`, and −1.5 → 17.3 → 14.3 → 11.9 % at `r = 1.50` — with no monotone trend at either.

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

> **The beyond-pair excess is real in sign — positive at 2.3–3.8 σ on seven of the eight
> (template, temperature) cells, and exactly zero on the eighth (`r = 1.50`, `T = 0.64`). Its
> growth across the ladder is +3.79 σ at `r = 1.50` and +1.91 σ at `r = 1.30`. Neither reaches
> the 5 σ this campaign committed to in advance. The claim is SUPPORTED, NOT CASHED, and the
> two templates do not agree about growth.**

---

## 2.2 CEILING FRACTIONS — and the sharp denominator changes the trend

Reported for cross-campaign comparability, against **both** machine-checked denominators. Floors
are already subtracted, and each floor's own ceiling fraction is quoted beside it.

* **`log 2`** — `Core/ThirdCap.lean`'s `share_le_log_two`: proved for **every** probability state
  on three binary slots, no hypothesis on the pair data, and attained exactly by the parity state
  (`share_max_eq_log_two`). This is the universal denominator.
* **The sharp, data-computable ceiling** — `share_le_grouping_gaps`: the minimum over the three
  slot orientations of `H(marg_ij) + H(marg_k) − H(p)`, i.e. `I(slot pair ; third slot)`. Never
  worse than `log 2`, often far smaller. Our template is fully symmetrised, so all three
  orientations coincide to machine precision and the minimum is unambiguous.

| `T` | `r` | share − floor | **% of `log 2`** | floor % | sharp ceiling | sharp / `log 2` | **% of sharp** | floor % sharp |
|---|---|---|---|---|---|---|---|---|
| 0.44 | 1.30 | 5.430e−03 | **0.783 %** | 0.0003 % | 0.2349 | 0.339× | **2.311 %** | 0.0008 % |
| 0.50 | 1.30 | 3.647e−03 | 0.526 % | 0.0003 % | 0.1827 | 0.264× | 1.996 % | 0.0011 % |
| 0.56 | 1.30 | 3.133e−03 | 0.452 % | 0.0002 % | 0.1457 | 0.210× | 2.150 % | 0.0009 % |
| 0.64 | 1.30 | 2.255e−03 | **0.325 %** | 0.0002 % | 0.1154 | 0.166× | **1.954 %** | 0.0011 % |
| 0.44 | 1.50 | 2.652e−03 | **0.383 %** | 0.0001 % | 0.0072 | 0.010× | **36.89 %** | 0.0134 % |
| 0.50 | 1.50 | 1.012e−03 | 0.146 % | 0.0001 % | 0.0038 | 0.006× | 26.50 % | 0.0195 % |
| 0.56 | 1.50 | 5.062e−04 | 0.073 % | 0.0001 % | 0.0023 | 0.003× | 22.25 % | 0.0319 % |
| 0.64 | 1.50 | 6.041e−05 | **0.009 %** | 0.0001 % | 0.0010 | 0.001× | **6.24 %** | 0.0630 % |

**The warning was right, and it bites here harder than at the campaign that sent it.** The sharp
ceiling is **0.001× to 0.34× of `log 2`** — up to a thousand times tighter — and, decisively, **it
is not constant across the temperature ladder.** At `r = 1.30` it doubles on cooling
(0.115 → 0.235); at `r = 1.50` it rises sevenfold (0.0010 → 0.0072). So the two denominators
give two different answers to the campaign's own question:

> **Against `log 2`, the `r = 1.30` share grows by a factor of 2.41 on cooling. Against the
> sharp ceiling it is FLAT — 1.95 %, 2.15 %, 2.00 %, 2.31 % — a span of 1.18.** The whole-only
> sector at that template uses a **constant ~2 % of the room available to it**, and the growth of
> the raw reading is the growth of its own ceiling.
>
> **At `r = 1.50` the trend survives the renormalisation but is attenuated**, from ×43.5 against
> `log 2` to **×5.9** against the sharp ceiling (6.24 % → 36.89 %).

This is a substantial qualification of §1's headline and it is placed here, immediately after
the number it qualifies, rather than in a caveats list. **`I(pair ; third)` is not a pair-only
quantity** — it involves the full joint — so "the ceiling grew" is not the same statement as
"the pair correlations grew", and the two normalisations answer genuinely different questions:
*how much whole-only structure is there* (`log 2`) versus *how much of the structure that could
possibly be whole-only, is* (sharp). Both are reported; neither is elected.

**The excess over the pair-matched surrogate, in the same units** (§2.1's numbers; the ceiling
cancels in a same-state-point comparison, so this is presentation only):

| `r` | `T` = 0.44 | 0.50 | 0.56 | 0.64 |
|---|---|---|---|---|
| 1.30 | 0.116 % / 0.342 % | 0.079 % / 0.299 % | 0.047 % / 0.223 % | 0.049 % / 0.296 % |
| 1.50 | 0.040 % / 3.886 % | 0.021 % / 3.779 % | 0.014 % / 4.256 % | −0.0001 % / −0.062 % |

(each cell: % of `log 2` / % of the sharp ceiling.)

**For the cross-scale synthesis, the comparable figure is this**: at its largest, this substrate
reads **0.78 % of `log 2`**, and the part of that which survives a pair-matched generative null
reads **0.12 % of `log 2`**. Against the sharp ceiling the same two numbers are **36.9 %** and
**3.9 %** (at `r = 1.50`, where the sharp ceiling is tightest). **Any cross-substrate table must
say which denominator it is using**, because for this substrate the two differ by up to a factor
of a thousand.

### 2.2b The named-denominator column, extended to every cell — and a domain condition on it

`GATES.md`'s **named-denominator** gate (`d520c74`) applied to the whole campaign, not just the
two primary templates: 3D at 11 templates × 4 temperatures, the 2D replicate, and the ideal-gas
control — **71 cells**, both denominators named. Full table in `glass_ceiling_full.json`.

**First, a validation the extension bought for free.** `share_le_grouping_gaps` is a *minimum over
three orientations*, so the minimum is only unambiguous if the orientations are close. Across all
71 cells the **worst orientation spread is 1.5 × 10⁻⁵ nats**, and it is exactly 0 on most — which
confirms that this campaign's full symmetrisation over the template's own permutations (prereg
§3.3) makes the three orientations coincide. The "min" is not doing any hidden work here.

**The sharp caps in their own right — what each template COULD have carried.** They span
**2.05e−08 to 0.5123 nats**, `0.00000×` to `0.7391×` of `log 2`, a spread of **2.5 × 10⁷**:

| cell | sharp cap | cap / `log 2` | reading, % of sharp |
|---|---|---|---|
| 2D `r = 0.89`, `T = 0.23` | **0.5123** | **0.739×** | **−0.000 %** |
| 3D `r = 0.89`, `T = 0.64` | 0.2339 | 0.337× | 0.021 % |
| 3D `r = 1.30`, `T = 0.44` | 0.2349 | 0.339× | **2.311 %** |
| 3D `r = 1.30`, `T = 0.64` | 0.1154 | 0.167× | 1.954 % |
| 3D `r = 1.50`, `T = 0.44` | 0.00719 | 0.0104× | **36.89 %** |
| 3D `r = 1.50`, `T = 0.64` | 0.00097 | 0.0014× | 6.24 % |
| 3D `r = 1.07`, `T = 0.44` | 0.000293 | 0.00042× | −0.002 % |

**The two rungs this campaign voided turn out to have voided for opposite reasons, and the sharp
cap is what shows it.** At `r = 0.89` the cap is **large** (0.23–0.51 nats, a third to three
quarters of `log 2`) and the substrate uses **0.01–0.02 %** of it: enormous room, nothing in it.
At `r = 1.07` the cap has **collapsed to 0.0003 nats** — 0.04 % of `log 2` — so that template had
essentially no room to carry anything, and its floor reading is not evidence of absence. **Those
are different findings and the `log 2` column cannot tell them apart**; both read ≈ 0 % of `log 2`.

**And now the domain condition, which the ideal-gas control makes unmissable.** As a state
approaches independence its sharp cap collapses toward zero — and the *floor does not*. On the
ideal-gas control the cap falls **below the floor**, and "% of sharp" degenerates into noise
divided by noise, printing values like **−1695 %** and **+1697 %**. Measured worst `cap / floor`
per family:

| family | worst `cap / floor` | best |
|---|---|---|
| ideal gas (control) | **0.06** | 11 |
| 3D KA, far arm `r = 5.00` | **1.10** | — |
| 2D, far arm `r = 4.00` | 2.05 | — |
| 3D KA, primary `r = 1.50` | **1 587** | 7 474 |
| 3D KA, primary `r = 1.30` | **89 773** | 118 282 |

> **Proposed as an amendment to the named-denominator gate: a sharp ceiling fraction may be
> quoted only where the sharp cap exceeds the reading's own floor by a stated factor (≥ 100 is
> comfortable; this campaign's primary cells clear it by 16–1 200×). Below that the sharp
> denominator is itself at the noise level and the fraction is uninterpretable — report the
> `log 2` fraction and the bare cap, and say the sharp fraction is undefined here.**

Without that condition the gate would have this campaign reporting its ideal-gas control — a
theorem-pinned zero — as "−1695 % of ceiling". **The universal `log 2` denominator has no such
failure mode**, which is a concrete argument for the gate's insistence that both be reported
rather than the sharp one alone.

### 2.2a The ceiling-swing threshold, adjudicated against planted values

The water campaign's `WATER_PREREG.md` §5.4 fixes *"no ceiling fraction is compared across cells
whose ceilings differ by more than 3×"*. Applied to this ladder it **permits** `r = 1.30`
(ceiling swing ×2.0, where §2.2 reports flat) and **VOIDS** `r = 1.50` (×7.2, where §2.2 reports
the trend surviving attenuated). Two documents, two verdicts, one cell. Settled here against a
case with a known answer rather than by assertion (`axiomology.md` §5), and by the method this
repository already learned the hard way — *gauge a ruler with planted values before staking a
band* (`forward-prediction-confirmed`). Instrument: `glass_ratiogauge.py`.

**First, what a threshold cannot be about.** `share / ceiling` is an exact function of the
population table and means the same sentence at every cell — *the fraction of the room available
to the whole-only sector that it uses*. No ceiling-swing threshold can be justified
definitionally. The real hazard is **estimation**: at finite `N`, is the recovered ratio biased,
and does the bias depend on the ceiling?

**Arm A — synthetic, fully planted.** A family in which the ceiling is swept over three decades
while the true ratio is pinned by construction; recovery scored against a value known exactly.

| ceiling | ceiling / `log 2` | rel. bias at `N=1e5` | at `N=1e6` |
|---|---|---|---|
| 0.00042 | 0.0006 | **+13.3 %** | +3.4 % |
| 0.00267 | 0.0039 | +9.2 % | +1.9 % |
| 0.01110 | 0.0160 | +5.9 % | +1.8 % |
| 0.04663 | 0.0673 | +2.4 % | +0.5 % |
| 0.18368 | 0.2650 | +0.3 % | +0.2 % |
| 0.49951 | 0.7206 | +0.3 % | −0.1 % |

**The bias is a function of the CEILING and of `N` — not of the ceiling SWING.** It is always
positive, it grows as the ceiling shrinks, and it falls with `N` roughly as the reading's own
significance against its floor (`≈ 0.2275 / (N · share)`, the pump campaign's constant). A rule
phrased on the *ratio between two cells' ceilings* is therefore targeting the wrong variable: it
would void a comparison between two large well-measured ceilings that happen to differ, and
permit one between two tiny ones that happen to match.

**Arm B — the eight real glass cells as their own planted populations**, resampled at each
cell's **effective** `N` (raw triple count ÷ that cell's measured overlap penalty, so the
resampling carries the real precision and not a flattering one):

| `T` | `r` | ceiling | true ratio | `N_eff` | recovered | rel. bias | rel. sd |
|---|---|---|---|---|---|---|---|
| 0.44 | 1.30 | 0.23489 | 0.02312 | 8.9e+04 | 0.02311 | **−0.07 %** | 6.6 % |
| 0.50 | 1.30 | 0.18275 | 0.01997 | 7.5e+04 | 0.02004 | +0.37 % | 8.5 % |
| 0.56 | 1.30 | 0.14574 | 0.02151 | 2.3e+05 | 0.02166 | +0.73 % | 5.3 % |
| 0.64 | 1.30 | 0.11540 | 0.01955 | 3.1e+05 | 0.01962 | +0.33 % | 5.6 % |
| 0.44 | 1.50 | 0.00719 | 0.36904 | 1.0e+05 | 0.37902 | +2.70 % | 6.7 % |
| 0.50 | 1.50 | 0.00382 | 0.26521 | 2.1e+05 | 0.27241 | +2.72 % | 8.4 % |
| 0.56 | 1.50 | 0.00228 | 0.22280 | 3.9e+05 | 0.22658 | +1.70 % | 8.8 % |
| 0.64 | 1.50 | 0.00097 | 0.06298 | 3.9e+05 | 0.06715 | **+6.62 %** | **29.6 %** |

**Ceiling swing across all eight cells: 242×. Worst relative bias: 6.6 %.**

**The verdict on the disputed cell.** At `r = 1.50` the two endpoint biases are **+2.70 %** and
**+6.62 %** — a differential of **3.9 percentage points** — against a claimed effect of
**×5.9, i.e. 490 %**. The bias differential is **125× too small to manufacture the effect**, and
it runs in the *conservative* direction: correcting it moves the ratios to 35.9 % and 5.85 %, an
effect of **×6.1** rather than ×5.9. **The `r = 1.50` comparison stands, and the 3 × threshold is
too tight for it by two orders of magnitude.**

**And it clears the other cell too, in the other direction.** At `r = 1.30` the biases span
−0.07 % to +0.73 %, a differential of 0.8 pp against an 18 % spread in the ratio — so the
**flatness** reported in §2.2 is also not a bias artifact. The bias could neither create the
`r = 1.50` trend nor hide an `r = 1.30` one.

**A threshold with a basis, proposed rather than asserted.** Replace the ceiling-swing rule with
a measured one, since the measurement is cheap — 400 multinomial resamples of an eight-cell
table per cell, seconds:

> **A ceiling fraction may be compared across cells when the DIFFERENTIAL RELATIVE BIAS, obtained
> by resampling each cell's own table at its own effective `N`, is at least 5× smaller than the
> effect being claimed.** Report the per-cell bias beside the per-cell ratio.

On this ladder that rule gives 125× margin at `r = 1.50` and 22× at `r = 1.30`. It has the
property a swing threshold lacks: it fires on the actual failure mode — **a small ceiling at a
small `N`** — rather than on a proxy for it. One honest caveat: the worst cell here also carries
a **29.6 % relative sd**, which is a genuine precision limit on that single cell's ratio and is
quoted with it; it does not threaten a 490 % effect but it would threaten a 50 % one.

### 2.2a-i The closed forms, checked — one confirmed, one incomplete, and the missing term found

The water campaign offers two closed forms and invites the check with *"a disagreement means the
resample is wrong, not the theory."* Taken in both directions (`glass_biaslaw.py`).

**Their VARIANCE law is confirmed.** `rel_sd = √(2 + 8·N·share) / (2·N·share)`, against my eight
real cells at their own effective `N`:

| cell | `N·share` | sd measured | sd from law | diff |
|---|---|---|---|---|
| `T=0.44`, `r=1.30` | 484.5 | 6.56 % | 6.43 % | +0.14 pp |
| `T=0.50`, `r=1.30` | 274.1 | 8.53 % | 8.55 % | −0.02 pp |
| `T=0.56`, `r=1.30` | 728.6 | 5.27 % | 5.24 % | +0.03 pp |
| `T=0.64`, `r=1.30` | 705.2 | 5.63 % | 5.33 % | +0.30 pp |
| `T=0.44`, `r=1.50` | 274.6 | 6.75 % | 8.54 % | **−1.79 pp** |
| `T=0.64`, `r=1.50` | 23.8 | **29.65 %** | **29.17 %** | +0.48 pp |

**Worst disagreement 1.79 pp over eight cells**, five of eight inside 0.5 pp, and it nails the
one cell that matters most — the 29.6 % sd at `N·share = 23.8` is predicted at 29.2 %. Their sd
gate is well-founded and I have adopted the ordering: **variance binds before bias.**

**Their BIAS law is incomplete, and the resample is not what is wrong.** `c/(N·share)` — with
`c = 0.2275` (median) or `0.5` (mean) — does not reproduce my measurements: at `N·share = 222`
it predicts 0.10–0.23 % where I measure **+1.04 %**, and at `N·share = 3674` it predicts
0.006–0.014 % where I measure **+0.21 %**. The measured bias **plateaus around +1 %** instead of
falling as `1/(N·share)`.

**The missing term is that the ratio has TWO estimated quantities in it, and the closed form is
written for the numerator alone.** The ceiling is itself a plug-in mutual information with its
own bias. Decomposed at planted states where both truths are known exactly:

| `N·share` | share bias | **ceiling bias** | ratio bias | predicted `share − ceiling` |
|---|---|---|---|---|
| 8.3 | −3.38 % | **−4.28 %** | +1.57 % | +0.91 % |
| 53.4 | −0.68 % | **−1.73 %** | +0.94 % | +1.05 % |
| 222.0 | +0.14 % | **−0.94 %** | +1.04 % | +1.08 % |
| 932.5 | −0.31 % | **−0.33 %** | +0.10 % | +0.02 % |
| 22.2 | +3.48 % | **−2.52 %** | +6.85 % | +6.00 % |
| 3673.5 | +0.05 % | **−0.17 %** | +0.21 % | +0.22 % |

`rel_bias(ratio) = rel_bias(share) − rel_bias(ceiling)` reproduces the measured ratio bias on
five of six rows to within 0.15 pp. **And the ceiling's term is the dominant one**: it is
consistently **negative** — the median estimated ceiling sits *below* the truth — and at moderate
`N·share` it is several times the share's own bias, which fluctuates in sign.

**So the constant question ("is it 0.2275 or 0.5?") is the wrong question for a ceiling
fraction.** Both are numerator-only constants; the ratio's bias is governed by a *difference* of
two biases whose second term scales with `N·ceiling`, not `N·share`. A bias rule keyed on
`N·share` alone is therefore incomplete — which is precisely why §2.2a's rule is phrased on the
**measured** resample rather than on a formula, and why the resample survives the check that was
meant to falsify it. **One caveat on my own numbers: I measured MEDIANS throughout**, so the
comparison to a mean-bias constant is not like-for-like, and that is a second reason not to read
the constant off my table.

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

### 3.1b Cross-check against the pump campaign's floor law — CONFIRMED, and its domain located

The pump campaign reports the finite-`N` floor of the `k = 3` whole-only share as `χ²` with one
degree of freedom, **median `0.2275/N` nat**, and warns that the naive `(cells−1)/2N = 3.5/N`
overstates it 15×. Checked here, independently, on both my synthetic and my real nulls.

**On independent draws it holds.** `glass_gate.py`'s G6, 200 multinomial draws from an 80:20
product model at four sample sizes:

| `N` | median × `N` | mean/median | p99/median |
|---|---|---|---|
| 1e4 | 0.3144 | 1.75 | 9.9 |
| 1e5 | **0.2342** | 2.08 | 16.0 |
| 1e6 | **0.2075** | 2.80 | 15.5 |
| 1e7 | **0.2121** | 2.32 | 13.9 |
| **χ²₁ theory** | **0.2275** | **2.198** | **14.58** |

Agreement to 3–9 % on the constant and on both shape ratios. **Independently confirmed.**

**On my real nulls it fails, by exactly the overlap penalty — and that locates its domain.**

| | `N` | null median × `N` | vs `0.2275` |
|---|---|---|---|
| `T = 0.44`, `r = 1.30` | 6.65e+05 | 1.321 | **5.8×** |
| `T = 0.44`, `r = 1.50` | 1.87e+06 | 1.797 | **7.9×** |
| `T = 0.44`, `r = 6.00` | 1.25e+07 | 0.236 | **1.0×** |
| `T = 0.64`, `r = 1.30` | 8.58e+05 | 1.102 | 4.8× |
| `T = 0.64`, `r = 1.50` | 1.99e+06 | 1.215 | 5.3× |
| `T = 0.64`, `r = 6.00` | 1.25e+07 | 0.274 | 1.2× |

**The law is exact where the enumerated triples are effectively independent and wrong by 5–8×
where they overlap.** At `r = 6.00` the cap draws 25 000 triples per configuration from a far
larger population, so sampled triples rarely share a particle and the ratio is `1.0–1.2`. At the
primary templates each particle sits in several enumerated triples and the ratio is `4.8–7.9`.

So: **`0.2275/N` is the correct floor for `N` INDEPENDENT triples, and the count that goes into
it is not the number of triples enumerated but the number of independent ones.** This is the
same finding as §4.1's overlap penalty, arrived at from the other direction, and it is why every
floor in this campaign is the control itself rather than any formula.

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

**Is the headroom a property of the state point rather than the template?** Flagged by the water
campaign, whose synthetic proxies showed the LP headroom collapsing when a label composition goes
lopsided — which at 80:20 species would be a live risk here, and would mean a P4 failure reported
as a finding about glasses was really a finding about composition. **Checked, and for this
campaign the answer is: it varies with the state point, but NOT for that reason.** Over all 44
`(T, template)` cells, `corr(log min(p_B, 1−p_B), log headroom) = +0.209` — weak, and the wrong
sign for lopsidedness driving collapse. The two lowest-headroom families are:

| | `p_B` in the triple population | headroom | min cell |
|---|---|---|---|
| `r = 0.89`, all four `T` | **0.46–0.51** (nearly balanced) | 0.0002–0.0030 | 72–294 |
| `r = 1.07`, all four `T` | **0.023–0.026** (very lopsided) | 0.0044–0.0051 | 881–1175 |

**A nearly balanced marginal and an extremely lopsided one collapse the headroom equally.** The
driver here is **near-emptiness of a CELL** — the joint effect of geometry and species exclusion
— not lopsidedness of a slot marginal. At `r = 0.89` the equilateral template sits at the `g_AB`
peak and *below* the `g_AA` onset, so it selects mixed triples and starves the same-species cells;
that is a fact about the glass, and it is why the rung was put in as a stress test.

At the primary templates the headroom moves by a factor of only 1.6 across the whole ladder
(0.194–0.306 at `r = 1.30`), it moves **against** the reading rather than with it, and no verdict
in this document turns on it. **P4's partial failure is therefore reported as a finding about
this model's excluded volume, not about composition and not about the instrument.**

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

0. **The paired surrogate does not seed its GPU RNG**, so two runs of identical arguments give
   different draws — which is how §2.1's correction happened. `glass_run.py`'s per-state-point
   seed was fixed to a stable CRC during this campaign; **the same fix was not applied to the
   cupy RNG inside the surrogate's Metropolis loop**, and until it is, `glass_stageB_paired.json`
   is reproducible only up to that stream.
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

## 7a. TWO HAZARDS FROM THE PUMP CAMPAIGN, CHECKED AGAINST THIS DESIGN

Both raised by the pump campaign (`PUMP_RESULTS.md`, `2dc6cfc`). Neither bites here, and the
reason each does not is recorded so a continuation cannot assume it stays that way.

**(a) Coarse-graining is not licensed to inherit a pump law unless the binarization is LUMPABLE
with respect to the per-cell noise** — measured there at exponent 2.02 through a lumpable
binarization and 1.09–1.53 through a non-lumpable one. **Does not apply to this campaign, for
two independent reasons.** First, the primary label is **atomic**: species is already discrete
and no binarization is applied to it (§3.1 of the pre-registration is built around exactly this).
Second, and more to the point, **this campaign never predicted its coarse-graining floor from any
law** — the only coarse-graining it has is geometric (the shell tolerance), and §4.2 *measured*
that floor directly as the binmint pedestal, at 0.0–1.5 % of the reading at the primary
templates. So this design is already in the regime the pump campaign says a floor must stay in:
separately measured, not inherited. **A continuation that adopts the secondary
local-order-parameter design of prereg §3.2 would binarize a continuum and would then owe the
lumpability check.**

**(b) `valve_needs_asymmetry` carries TWO hypotheses — three slots AND a sign-symmetric input —
and it does not generalise past either.** At `k = 4…7` a symmetric per-cell channel mints 1–1.6 %
of the `(k−2)·log 2` ceiling on a share-zero sign-symmetric input.

**Neither hypothesis is violated here.** Every reading in this campaign is `k = 3` — three
particles, three slots, throughout, including the fine binmint object (whose slots carry up to
`2·b_r = 8` letters but which is still three slots) and the 2D arm's `3×3×3` reading. And
**this campaign does not lean on the theorem for a zero floor in any case**: the pre-registration
cites it in §3.1 to argue the design has no *counting-noise* minting channel, but every floor
actually quoted is the empirical permutation control pushed through the identical triple
selection (§4.1) — a measurement, not a theorem.

**The second hypothesis is the one a continuation would trip, and it is not the one that looks
dangerous.** The unrun local-order-parameter design of prereg §3.2 binarizes a *continuous*
order parameter (Voronoi volume, `q₆`/`ψ₆`), and such a parameter is **not** generally
sign-symmetric about its own median. On a non-sign-symmetric input a **unital** channel — one
that treats the two cell values alike, and therefore looks maximally innocent — **is already
enough to mint**. So that arm owes two conditions, not one:

1. the **lumpability** check of (a), before any coarse-graining floor may be predicted rather
   than measured; and
2. a check that the binarized order parameter is sign-symmetric, **or** an empirically measured
   minting floor under the actual channel, because `valve_needs_asymmetry` will not supply one.

Recorded here so the arm cannot be picked up with only the first condition attached.

**A prior-art correction owed in the same neighbourhood, and not ours to keep.** Creation of
order-3 structure by local noise is **not** this programme's territory: **Schneidman, Still,
Berry & Bialek (2003), Fig. 2** already shows a per-cell unital flip creating 0.0774 bits, and
the pump campaign has re-measured it. This campaign makes no creation claim of any kind — its
only creation citation is Kahle, Olbrich, Jost & Ay (2009) for coarse-graining, which is what
§4.2's binmint gate is built on — but the correction is carried here because it is the same
neighbourhood and this repository has been caught in it before (`eca-spike-is-convergent-art`).

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
