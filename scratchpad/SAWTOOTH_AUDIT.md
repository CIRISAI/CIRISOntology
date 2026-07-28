# SAWTOOTH AUDIT — is `rent/nat` measuring maintenance, or measuring its own denominator?

**Role:** adversarial audit of the rent campaign's two headline shapes, commissioned to kill them.
**Hypothesis under test (the coordinator's own):** both shapes are arithmetic consequences of how
`rent/nat` is built, not facts about maintenance.
**Scratchpad only.** No Lean touched, no `lake` run, no `Stance.lean` edit, nothing pushed.
**Everything below is re-derived from the primary JSON with my own code**
(`sawtooth_audit_{1..6}.py`, committed here, outputs in `sawtooth_audit_{1..6}.txt`); the campaign's
own published numbers are reproduced to the last
quoted digit before anything is disputed (§0.1).

---

## VERDICT IN ONE LINE EACH

> **S2, THE SAWTOOTH — the hypothesis is REFUTED. The sawtooth is NOT arithmetic.** The campaign
> already ran the decisive control without labelling it as one: two of its six conditions hold the
> denominator **constant by construction**, and the tooth survives there at **69–99 %** of its
> fixed-fraction size at every one of the nine natural steps. Better: on `ARM B` the denominator is
> **exactly invariant at every step** — `k·ln2 − ln|S|` does not move when `k` increments and `|S|`
> doubles — so the entire raw uptick (6/6 at `k` = 8, 16, 32, **+4.45 to +16.2 pp**) is numerator,
> to machine precision. **No null protocol reproduces it.** The campaign's headline is safe.

> **S1, ECONOMIES OF SCALE — the hypothesis is PARTLY CONFIRMED, and the headline number must be
> re-scoped.** In the four fixed-*fraction* conditions the denominator is **defined** to grow with
> `k`; it grows **13.0×** over `k` = 5 → 31 while the cost grows **4.9–7.4×**. Held at a fixed
> amount of pattern instead, the decline is **1.21–1.57×**, not the quoted **1.77–2.68×** — i.e.
> **only 21–46 % of the headline log-decline survives**, and an exponent of **−0.16 to −0.23**, not
> **−0.52**. "The biggest habits are the cheapest per bit" may not be quoted from the 2.68× number
> without also saying that the bigger habit was asked to hold **thirteen times more**.

> **Cost to `law-as-habit`: zero today, because it does not cite this.** I grepped `Stance.lean`,
> `CLAUDE.md` and `GATES.md`: the selection reading cites Wilson, 't Hooft, the SM's two unpaid
> bills and the minting theorems, and **nowhere cites the rent scale economy**. The brief's premise
> that it "currently cites the scale economy as measured support" is **false as of `a3a467f`**. The
> cost is entirely prospective — §6 states exactly what a future citation would be entitled to.

**Prior art: CONVERGENT-ADJACENT.** The *denominator's* staircase is textbook and has been since
1950 — `share_max/k` on `ARM B` is **identically** `ln2·(1 − ⌈log₂(k+1)⌉/k)`, the Hamming-family
parity-overhead staircase, and on `ARM A` it is the Plackett–Burman multiple-of-4 run-size
staircase. The *numerator's* tooth I could not find anywhere. Details in §5.

---

## 0. THE ARITHMETIC, STATED EXPLICITLY

From `rent_scaling_q2.py:551` (`measure_rent`) and its parent, unchanged since `rent_islands.py`:

```
rent_per_nat = cost_erase / achieved
cost_erase   = q* · (H_pre − H_c)
achieved     = target   (to < 1e-12 relative; rows above 1e-6 are DROPPED, not adjusted)
```

and `target` is set by the condition:

| mode | `target` | does the denominator step? |
|---|---|---|
| `frac` (4 of 6 conditions) | `f · share_max(k)`, `f ∈ {0.1, 0.5}` | **yes** — `share_max(k) = k·ln2 − ln\|S(k)\|`, and `\|S\|` is a step function of `k` |
| `abs` (2 of 6 conditions) | **`1.0` nat, constant in `k`** | **no — by construction** |

So, exactly:

```
ln(rent/nat) = ln(cost) − ln(target)
```

and every additive statistic splits. For the campaign's tooth
`T(k₀) = L(k₀) − mean(L of the three-wide baseline run)`, with `L(k) = Δ ln`:

```
T[rent] = T[cost] − T[target]          (identity, exact)
```

The second term is **pure arithmetic**: a function of `k` and `|S|` only, with no dynamics in it.
`−T[target]` is the *denominator-only tooth* — what the ratio does if the numerator holds its own
smooth trend. **In the two `abs` conditions it is identically zero.**

### 0.1 Instrument check — the campaign's numbers, reproduced before they are disputed

| quantity | published | this audit |
|---|---|---|
| `A24` tooth, ε=.01/10 % | +1.737 pp | **+1.7369** |
| `A28` tooth, ε=.01/10 % | +1.330 pp | **+1.3296** |
| `B32` tooth, ε=.01/10 % | +7.469 pp | **+7.4689** |
| `B32` tooth, ε=.01/1nat | +6.972 pp | **+6.9720** |
| `P-PLANT` k=24, ε=.01/10 % | 9.999 pp | **9.9987** |
| `P-PLANT` k=24, ε=.01/1nat | 8.932 pp | **8.9324** |
| `share_max(B31) = share_max(B32)` | 18.021827 | **18.021826694559**, difference −3.6e−15 |

**Nothing in the campaign's arithmetic is wrong.** The audit is about what the arithmetic means.

---

## 1. THE DECOMPOSITION (brief item 1)

### 1.1 The naive split — and why it is the WRONG counterfactual

Every natural step, every condition. `denom-only = −T[target]`; `excess = T[rent] − denom-only`.

| arm | k₀ | `\|S\|` | condition | T[rent] | denom-only | T[cost] | **denom share** |
|---|---|---|---|---|---|---|---|
| A | 8 | 8→12 | ε.01/10 % | 10.3014 | 7.4109 | 2.8905 | **72 %** |
| A | 8 | 8→12 | ε.05/50 % | 7.7000 | 7.4109 | 0.2890 | **96.2 %** |
| A | 8 | 8→12 | ε.01/1nat | 8.2823 | **0.0000** | 8.2823 | **0 %** |
| A | 12 | 12→16 | ε.01/10 % | 5.5016 | 3.0220 | 2.4796 | 55 % |
| A | 16 | 16→20 | ε.01/10 % | 3.4568 | 1.6396 | 1.8171 | 47 % |
| A | 20 | 20→24 | ε.01/10 % | 2.3706 | 1.0286 | 1.3420 | 43 % |
| A | 24 | 24→28 | ε.01/10 % | 1.7369 | 0.7052 | 1.0317 | 41 % |
| A | 24 | 24→28 | ε.05/50 % | 1.3640 | 0.7052 | 0.6589 | 52 % |
| A | 24 | 24→28 | ε.01/1nat | 1.7130 | **0.0000** | 1.7130 | **0 %** |
| A | 28 | 28→32 | ε.01/10 % | 1.3296 | 0.5134 | 0.8162 | 38.6 % |
| A | 28 | 28→32 | ε.01/1nat | 1.3210 | **0.0000** | 1.3210 | **0 %** |
| B | 8 | 8→16 | ε.01/10 % | 26.6922 | 18.6539 | 8.0383 | 70 % |
| B | 16 | 16→32 | ε.01/10 % | 14.1013 | 8.0387 | 6.0625 | 57 % |
| B | 32 | 32→64 | ε.01/10 % | 7.4689 | 4.0867 | 3.3821 | 55 % |
| B | 32 | 32→64 | ε.01/1nat | 6.9720 | **0.0000** | 6.9720 | **0 %** |

*(full 54-row table in `sawtooth_audit_1.txt`; range of the denominator share across the four `frac`
conditions and nine steps: **38.6 % – 97.0 %**.)*

Taken at face value this is damning: **up to 97 % of the fixed-fraction tooth is the stepping
denominator.** But it is the wrong counterfactual, and the campaign is entitled to say so:

> **The numerator is not independent of the denominator. `q*` is *solved* to hit `target`. When the
> target steps down relative to trend, so does the cost required to reach it.** Freezing the
> numerator's trend while the denominator moves is not a protocol anybody ran.

### 1.2 The VALID counterfactual — and the campaign already ran it, in 2 of its 6 conditions

The right question is not "what if the numerator were smooth?" but **"what does this protocol do
with a fixed target?"** — and that is exactly the `1.0 nat` conditions. Denominator constant,
definitional share **zero by construction**.

| arm | k₀ | ε | tooth @ frac 10 % | tooth @ **fixed 1 nat** | **abs / frac** |
|---|---|---|---|---|---|
| A | 8 | .01 | 10.3014 | 8.2823 | 0.804 |
| A | 8 | .05 | 8.9980 | 6.5867 | 0.732 |
| A | 12 | .01 | 5.5016 | 4.8997 | 0.891 |
| A | 16 | .01 | 3.4568 | 3.2613 | 0.943 |
| A | 20 | .01 | 2.3706 | 2.3032 | 0.972 |
| A | 24 | .01 | 1.7369 | 1.7130 | **0.986** |
| A | 28 | .01 | 1.3296 | 1.3210 | **0.994** |
| B | 8 | .05 | 22.6225 | 15.6830 | 0.693 |
| B | 16 | .01 | 14.1013 | 12.3956 | 0.879 |
| B | 32 | .01 | 7.4689 | 6.9720 | **0.933** |
| B | 32 | .05 | 6.3915 | 5.8971 | 0.923 |

**Deleting the denominator entirely costs the tooth between 0.6 % and 31 %, not 38.6–97.0 %** — and at
the two largest `k` on `ARM A` it costs **under 1.5 %**. The naive split overstates the definitional
content by roughly an order of magnitude, for the reason in §1.1.

### 1.3 The single decisive fact: on `ARM B` the denominator does not move at ALL

`ARM B` is the best linear `[k, m]` code with `m = ⌈log₂(k+1)⌉`, so `|S| = 2^m` and

```
share_max(k) = k·ln2 − ln|S| = (k − m)·ln 2
```

is the **redundancy in nats**. `m` increments exactly when `k` crosses `2^m − 1 → 2^m`, so **`k` and
`m` increment together and `share_max` is exactly unchanged at every `ARM B` step.** Verified to
3.6e−15 at `k = 32`; the same identity holds at `k = 8` and `k = 16`.

Therefore at every `ARM B` step, in **all six** conditions including the fixed-fraction ones,
`d ln target ≡ 0` and `d ln rent ≡ d ln cost`:

| arm | k₀ | condition | d ln rent | d ln cost | **d ln target** | uptick |
|---|---|---|---|---|---|---|
| B | 8 | ε.01/10 % | +16.1683 pp | +16.1683 pp | **0.0000 pp** | UP |
| B | 16 | ε.01/10 % | +9.5908 pp | +9.5908 pp | **0.0000 pp** | UP |
| B | 32 | ε.01/10 % | +5.6760 pp | +5.6760 pp | **0.0000 pp** | UP |
| B | 32 | ε.05/50 % | +4.4504 pp | +4.4504 pp | **−0.0000 pp** | UP |
| B | 32 | ε.01/1nat | +5.5765 pp | +5.5765 pp | **−0.0000 pp** | UP |

**6/6 raw upticks at all three `ARM B` steps, and the ratio's denominator contributes exactly
nothing to any of them.** `P-STEP32` — the campaign's largest advance-tested prediction, staked at
`aac3149` before the datum existed — is **100 % numerator in every condition it was scored in.**
That is the strongest single result in the rent campaign and this audit could not dent it.

*(The 55 % denominator share I report for `B32` in §1.1 is the trend-corrected statistic's baseline,
not the step: the denominator's contribution there is that it **stopped growing** relative to
`k` = 29–31, not that it moved at the step. Both readings are correct arithmetic; §1.2 is the one
that answers "is the phenomenon real".)*

### 1.4 What the excess actually is, and where it is thin

The denominator-free step effect (`d ln cost` at fixed 1 nat) decays fast along `ARM A`:

| `ARM A` step | k=8 | 12 | 16 | 20 | 24 | **28** |
|---|---|---|---|---|---|---|
| raw `d ln cost` @ 1 nat | +4.86 pp | +2.35 | +1.11 | +0.46 | +0.115 | **−0.071** |

At `k = 24` and `k = 28` the raw denominator-free step effect is **at or below zero**: the tooth
there is entirely "the decline paused", measured against a −1.4 pp/step trend. It is a real
deviation from trend (§2 gives it 15–26× its own null) but it is **not** a reversal. The reversals —
rent/nat actually going up — live on `ARM B`, where `Δln|S| = ln2` is 5× the `ARM A` step, and
there they are unambiguous. **This is consistent with the campaign's own height law
`tooth ∝ Δln(ns)/k` and is not a new problem; it does mean the `A24`/`A28` teeth should be described
as trend residuals and the `ARM B` teeth as the reversals.** `RENT_SCALING_RESULTS.md` §7.1 already
says the `A28` raw form fired 0/6 and records `H-DISSOC-2` dead on it.

---

## 2. THE TOOTH STATISTIC'S OWN NULL — a defect found, running in the campaign's favour

The campaign quotes each tooth against "baseline sd" = the scatter of the three `L` values in its
own baseline window. **That is not the null distribution of the tooth statistic.** The curve is
convex in log, so the statistic is biased even with no step at all: negative in the forward
convention, **positive in the backward convention** — and `P-STEP32` used the backward one.

`ARM B`, `k = 17…31`, is the only step-free stretch in the study (15 consecutive widths). Measured
there:

| convention | bias at comparable `k` (ε.01/10 %) | bias (ε.01/1nat) |
|---|---|---|
| forward, k=24…28 | −0.20 to −0.27 pp | −0.10 to −0.12 pp |
| **backward, k=28…31** | **+0.20 to +0.26 pp** | **+0.11 to +0.13 pp** |

Correcting `B32` for its own convention-matched, step-free bias:

| condition | tooth | bias | sd(bias) | **step excess** | ×sd | campaign's quoted × |
|---|---|---|---|---|---|---|
| ε.01/10 % | 7.4689 | +0.2252 | 0.0270 | 7.2437 | **268** | 72 |
| ε.01/1nat | 6.9720 | +0.1146 | 0.0106 | 6.8574 | **645** | 118 |
| ε.05/50 % | 5.5847 | +0.1477 | 0.0178 | 5.4370 | **306** | 83 |

**The campaign's clearance factors are conservative by 3–5×, not inflated.** I record this because I
went looking for the opposite and did not find it.

**A genuine structural note it does earn, though:** `ARM A`'s steps have period 4 and the baseline
window is 4 wide, so **no tooth anywhere on `ARM A` has a step-free window** — the arm cannot supply
its own null for the statistic, and the bias must be imported from `ARM B` (−0.2 pp at comparable
`k`, which makes the `ARM A` teeth understated by roughly 15 %). A step's *own* tooth is fine
(`k₀=24` forward uses `L(25),L(26),L(27)`, step-free); it is the non-step teeth that are
uninterpretable on that arm. Worth a line in any future rent prereg.

---

## 3. S1 DECOMPOSED (brief item 2)

OLS of `ln(rent/nat)`, `ln(cost)`, `ln(target)` on `ln k`, `ARM A` `k = 5…31`. `b_rent = b_cost − b_target`.

| condition | `b_rent` | `b_cost` | `b_target` | rent/nat fold | **cost fold** | target fold |
|---|---|---|---|---|---|---|
| ε.01/10 % | −0.5222 | **+0.8061** | **+1.3283** | 2.678× down | **4.85× UP** | 13.0× up |
| ε.01/50 % | −0.3866 | +0.9417 | +1.3283 | 2.119× down | 6.13× UP | 13.0× up |
| ε.01/1nat | **−0.2248** | **−0.2248** | **0** | **1.573× down** | **1.573× down** | **1.000×** |
| ε.05/10 % | −0.5047 | +0.8236 | +1.3283 | 2.578× down | 5.05× UP | 13.0× up |
| ε.05/50 % | −0.3238 | +1.0045 | +1.3283 | 1.855× down | 7.35× UP | 13.0× up |
| ε.05/1nat | **−0.1585** | **−0.1585** | **0** | **1.271× down** | **1.271× down** | **1.000×** |

**In the four fixed-fraction conditions the answer to the coordinator's question is YES, plainly:
"economies of scale" reduces to "the denominator grows faster than the numerator". The numerator
RISES 4.9–7.4×. With the denominator held fixed there is no economy at all in those conditions —
there is a diseconomy.**

### 3.1 What remains

The valid counterfactual again, and here — unlike the sawtooth — it **does** cost the effect:

| arm | ε | hold | `b_rent` | fold 5→31 | **% of the 10 % frac log-decline** |
|---|---|---|---|---|---|
| A | .01 | frac 10 % | −0.5222 | 2.678× | 100 % |
| A | .01 | frac 50 % | −0.3866 | 2.119× | 76.2 % |
| A | .01 | **fixed 1 nat** | **−0.2248** | **1.573×** | **46.0 %** |
| A | .05 | frac 10 % | −0.5047 | 2.578× | 100 % |
| A | .05 | frac 50 % | −0.3238 | 1.855× | 65.2 % |
| A | .05 | **fixed 1 nat** | **−0.1585** | **1.271×** | **25.3 %** |
| B | .05 | **fixed 1 nat** | **−0.1661** | **1.214×** | **21.5 %** |

**21.5 % – 46.0 % of the headline log-decline survives the fixed-amount hold.** The rest is the
protocol asking for more nats as `k` grows.

Why the two holds differ is measurable and not mysterious: the target elasticity
`η = ∂ln(rent/nat)/∂ln(target)` at fixed `k` is **negative** everywhere — −0.29 at `k = 8` rising to
−0.12 at `k = 32`. Holding *more* pattern is cheaper per nat. So the fixed-fraction conditions
compound a **size** economy with a **volume** economy, and report the sum as if it were the first.

**Both are real economies.** Neither is a fiction. But they are different claims, only one of them
is about "bigger structures", and the campaign reports one number.

### 3.2 One correction to the brief, in the campaign's favour

The brief says rent/nat "falls **monotonically** with k". It does not, and
`RENT_SCALING_RESULTS.md` §6.1 already says so: raw upticks occur at `ARM A` `k` = 8 (6/6), 12 (5/6),
16 (4/6), 20 (4/6), 24 (2/6), 28 (0/6) and at `ARM B` `k` = 8, 16, 32 (6/6 each). The monotone
description is the brief's, not the campaign's.

### 3.3 And one point the fixed-amount number understates

At `k = 5`, 1 nat is **72 %** of `share_max`; at `k = 31` it is **5.5 %**. Since `η < 0`, that
falling fraction pushes rent/nat **up** across the range. The fixed-1-nat economy of 1.21–1.57× is
therefore achieved *against* an adverse trend and is a **conservative floor** on the size effect,
not a ceiling. I state this because it is the strongest thing that can honestly be said for S1 and
the audit should not suppress it.

---

## 4. THE NULL MAINTENANCE PROTOCOL (brief item 3) — the decisive control

Four protocols with **no repair dynamics anywhere** — the "cost" is a closed-form function of the
structure — pushed through the identical `rent/nat = cost/target` pipeline over the same ladders.

| null | cost | fixed-**fraction** conditions | fixed-**1 nat** conditions |
|---|---|---|---|
| **N0** | `1` (constant) | tooth **39–77 %** of measured; `b_rent = −1.328` (2.5–4× too steep) | tooth **0**; `b_rent = 0` |
| **N1** | `ε·k` (per slot) | tooth **52–83 %**; `b_rent = −0.328` (within 40 % of measured) | tooth **3–23 %**, and **negative** at `B32`; `b_rent = +1.000` — **wrong sign** |
| **N2** | `\|S\|` | tooth **9.8–13.3× too big**; `b_rent = −0.44…−0.49` | tooth **10–12× too big**; `b_rent = +0.84` — **wrong sign** |
| **N3** | `ε·share_max` | tooth **exactly 0**; `b_rent` **exactly 0** | tooth **−0.39 to −0.69×** — **wrong sign**; `b_rent = +1.336` — **wrong sign** |

**Read it as the brief asked.**

- **In the four fixed-fraction conditions the null protocol reproduces both shapes.** `N1` gets the
  tooth to 52–83 % and the scale exponent to within 40 %, with no maintenance in it at all. Those
  four conditions cannot, on their own, distinguish maintenance from arithmetic. **That is the
  audit's finding and it stands.**
- **In the two fixed-1-nat conditions no null reproduces anything.** Every one either returns zero
  or returns the wrong sign on both shapes. `N2`, the closest in spirit to "the tooth is just `|S|`
  stepping", overshoots by **10–12×**: the measured response to a doubling of `|S|` is about a tenth
  of full proportionality, which is a number no arithmetic account predicts and a dynamical one has
  to earn.

> **Conclusion of the control: the sawtooth is DYNAMICAL and the scale economy is PARTLY
> DEFINITIONAL. The condition set decides which, and the campaign has both kinds of condition in it
> — which is why the audit could be run at all.**

### 4.1 The planted arm survives the same knife

`P-PLANT` (`SAWTOOTH_FORWARD_RESULTS.md`) plants a `ln2` ceiling step at `k` = 24, 26, 28, 30 by
running `m = 6` instead of the minimal `m = 5`. Decomposed:

| k₀ | ε.01/10 % tooth | denom share | **ε.01/1nat tooth** | **denom share** |
|---|---|---|---|---|
| 24 | 9.9987 | 60.8 % | **8.9324** | **0 %** |
| 26 | 9.1377 | 59.3 % | **8.2800** | **0 %** |
| 28 | 8.4752 | 57.7 % | **7.7731** | **0 %** |
| 30 | 7.9383 | 56.1 % | **7.3526** | **0 %** |

**The causal manipulation moves the statistic by 6.2–8.9 pp in the conditions where the denominator
cannot move at all.** P-PLANT's claim — "the ceiling step is the cause, proved by planting it" — is
not a ratio artifact.

### 4.2 One thing the audit does dispute in the height law

`tooth = C·Δln(ns)/k` with "`C` stable at 2.4–3.7". Recomputing `C` from the natural ladder in the
denominator-free condition (ε.01/1nat, forward convention):

| step | A8 | A12 | A16 | A20 | A24 | A28 | B8 | B16 | **B32** |
|---|---|---|---|---|---|---|---|---|---|
| implied `C` | 1.63 | 2.04 | 2.34 | 2.53 | 2.67 | 2.77 | 2.48 | 2.86 | **3.22** |

`C` **drifts monotonically by ~2× across the study**, on top of the substrate-dependence the
campaign's own §4 control already found. The staked `C16`/`C32` (2.31–3.45) were calibrated on
`ARM B` at two widths and interpolated between them, which is why the planted predictions landed to
1 %; the law is a good local interpolant and **not** a constant. `SAWTOOTH_FORWARD_RESULTS.md` §4
already refuted `C`'s universality across column rules; this adds that it is not constant in `k`
either. **Neither finding touches the tooth's sign, existence, or linearity in `Δln(ns)`.**

---

## 5. PRIOR ART (brief item 4) — verdict **CONVERGENT-ADJACENT**

Searched by mathematical object, never by our vocabulary, per the standing rule.

**(A) The denominator's staircase is textbook, and older than most of the programme's references.**
On `ARM B`, `share_max(k) = (k − m)·ln2` with `m = ⌈log₂(k+1)⌉` is the **redundancy of the
Hamming-family code in nats**, and the density ceiling is identically

```
share_max(k)/k = ln2 · (1 − ⌈log₂(k+1)⌉ / k)
```

— `ln2` times one minus the parity-overhead fraction. The staircase of that fraction is the standard
"check bits per data bit" table found in every treatment of Hamming codes since **Hamming (1950)**
(25 information bits need 5 check bits; 89 need 7 — the overhead per data bit falls between
power-of-two boundaries and jumps at them). On `ARM A`, `N₀(k) = 4⌈(k+1)/4⌉` is the
**Plackett–Burman (1946)** minimum run size, the multiple-of-4 staircase, standard in
Hedayat–Sloane–Stufken and **already credited by `RENT_SCALING_PREREG.md` §5.2**.

> **So the coordinator's prior is right about the denominator: coding theorists do know this, it is
> a hundred-year-old staircase, and it must never be presented as a discovery.** The rent campaign
> does not present it as one — `RENT_SCALING_PREREG.md` §1.3 tabulates it as "**Arithmetic, not
> measurement**" before any datum existed. Credit where due: the campaign called this correctly in
> advance.

**(B) "Any quantity with an optimal-code-size denominator inherits a sawtooth" is folklore, not a
citable theorem.** I could not find it stated as a named result. It is obvious once said, and should
be claimed as obvious rather than as a finding, in exactly the way (A) is.

**(C) The numerator's tooth: CLEAR.** The object is *the cost of holding a fixed amount of
whole-only share in the stationary state of a noise-plus-nearest-point-repair map, as a function of
the support size at fixed width*. Swept: finite-time Landauer and erasure cost, energy–error
tradeoffs in quantum error correction, information-friction bounds on decoding energy, noise-erasure
channel capacity, staircase codes, Griesmer-bound step structure and length-optimal code staircases.
**No hit.** Nothing I found scoops the measured claim that doubling `|S|` at fixed `k` raises the
maintenance cost of a fixed target by ~5 %, nor the ~1/10-of-proportional response in §4.

**Verdict: CONVERGENT-ADJACENT.** The shape of the denominator is textbook; the shape of the
numerator is not scooped by anything findable.

---

## 6. WHAT THIS COSTS `law-as-habit`, EXPLICITLY

**Today: nothing.** `law-as-habit` in `Stance.lean` (lines 1810–1960) cites Peirce, Smolin's
precedence, Wilson's survivorship, 't Hooft's protection test, the SM's two unpaid bills, Giudice's
near-criticality, and this repository's substrate and minting theorems. **It does not cite the rent
scale economy, and neither does `CLAUDE.md` or `GATES.md`.** Verified by grep at `a3a467f`. The
prereg's §5.5 ("No promotion — nothing here reaches `Stance.lean` in this campaign") held.

**Prospectively, a citation of S1 would be entitled to exactly this and no more:**

1. **The number is 1.21–1.57×, not 2.68×** — exponent −0.16 to −0.23 — over a **6.2× range of `k`**
   (5 → 31) on **designed substrates**, at a **fixed amount of pattern held**. Quoting 2.68× without
   the denominator named is the failure this audit exists to prevent.
2. **It is a control, not a discovery about nature.** `RENT_SCALING_PREREG.md` §0 governs: nothing
   here bears on `wild-share`, and no natural system is shown to maintain order-3 pattern.
3. **It is convergent with textbook coding theory** — "longer blocks are more efficient per bit" is
   the practical reading of Shannon and has been in print since 1948. Under the programme's own
   convergence rule it is not novel support for anything.
4. **No `k > 31` claim.** The fitted floor is a curve parameter over `5 ≤ k ≤ 31`, arm-dependent
   (`RENT_SCALING_RESULTS.md` §8.3 already flags this as its own largest caveat), and never an
   asymptotic price of habit.
5. **"The biggest habits are the cheapest per bit, which is why laws are the oldest habits"** is, at
   best, licensed by a 1.2–1.6× effect on engineered codes. It cannot carry a selection argument on
   its own, and the selection reading is currently better served by the machinery it actually cites.

**The sawtooth, by contrast, costs `law-as-habit` nothing and could support it if promoted**, since
it survives every knife in this document. It is also not currently cited.

---

## 7. WHAT WOULD STILL KILL EITHER SHAPE

Stated so this audit is falsifiable in its turn.

- **S2 dies** if a fixed-target (`abs`-mode) tooth can be produced by a protocol with no repair
  dynamics — i.e. if some closed-form cost function of `(k, |S|)` reproduces the **~1/10 of
  proportional** response to a doubling of `|S|` at fixed `k` and fixed target, across all nine
  natural steps and the five planted ones. `N0`–`N3` do not; a fifth might. **That is the one test
  this audit did not exhaust and it is cheap.**
- **S1's residue dies** if the fixed-1-nat decline is shown to be the fraction-of-capacity trend in
  disguise. §3.3 argues the sign is wrong for that, but the clean test is a fixed-*fraction-of-a-
  `k`-independent-reference* condition, which the campaign never ran and which costs one more
  target level per tier.

---

## 8. FILES

Primary data re-read, not taken from any prose: `rent_islands_results.json` (270 rows, `k` = 5…24),
`rent_scaling_q2_{A25..A31,B25..B32}.json` (90 rows), `sawtooth_{B20..B24,P24m6,P26m6,P28m6,P30m6}.json`.
Definitions read at source: `rent_scaling_q2.py:551` `measure_rent`, `:504` `solve_q`, `:616`
`sweep_one`.

Audit code and its unedited output, committed alongside this file so every table is reproducible:

| script | output | tables |
|---|---|---|
| `sawtooth_audit_1.py` | `sawtooth_audit_1.txt` | 1 — tooth decomposition, all 9 steps × 6 conditions |
| `sawtooth_audit_2.py` | `sawtooth_audit_2.txt` | 2 — S1 exponents · 3 — tooth at every `k` · 4 — the null protocols |
| `sawtooth_audit_3.py` | `sawtooth_audit_3.txt` | 5 — the `B31→B32` exact-`share_max` control · 6 — the planted arm |
| `sawtooth_audit_4.py` | `sawtooth_audit_4.txt` | 7 — the raw step, split · 8 — local-baseline teeth *(superseded by 9/10: its windows are step-contaminated)* |
| `sawtooth_audit_5.py` | `sawtooth_audit_5.txt` | 9 — curvature bias on step-free stretches · 10 — bias-corrected clearance |
| `sawtooth_audit_6.py` | `sawtooth_audit_6.txt` | 11, 12 — the valid counterfactuals · 13 — target elasticity |

Every table in this document is that printed output, unedited. `sawtooth_audit_{2..6}.py` `exec`
the loader in `sawtooth_audit_1.py`, so run them from this directory.
No `lake`, no Lean, no `Stance.lean`, no push.
