# RESULTS — islands of cheapness: does rent/nat sawtooth at the magic sizes?

Pre-registered in `RENT_ISLANDS_PREREG.md`, **committed at `19f80c6` before `rent_islands.py`
existed**. Run: `rent_islands.py --run --kmax 24` → `rent_islands_results.json` (270 rows,
0 dropped), adjudicated by `rent_islands_analyze.py` → `rent_islands_analysis.txt`.
Figures: `rent_islands_figure.png`, `rent_islands_figure_sawtooth.png`.

**SCOPE, unchanged from the prereg §0.** Designed substrates. A **control, not a discovery
about nature**. This measures the *price* of holding whole-only structure in an engineered
system, not its prevalence anywhere. `wild-share` is untouched. **The "island of stability"
name is an ANALOGY**: the only thing shared with nuclear physics is the abstract shape
*"discrete existence constraints create non-monotone stability landscapes"*. There is no
shared mechanism, no shell structure, no nuclear physics anywhere in this run, and no
inference in either direction is licensed. Anyone quoting this must carry that sentence.

---

## Headline

> **The sawtooth is real, and it is the ceiling's own sawtooth showing through.** At every
> `k ≡ 0 (mod 4)` — where the minimum orthogonal-array size `N₀` jumps by 4 and the capacity
> ceiling per slot drops — rent per nat jumps *above its own trend*, by an amount that
> tracks the ceiling's drop. The phase is right in essentially every condition tested
> (**9/10 sign-coherent residual events in 5 of 6 conditions**).
>
> **But the pre-registered primary test came out MIXED (12/20), and that is the verdict of
> record.** The islands show as actual local *minima* of rent/nat only when the target is
> demanding enough that the tooth beats the background decline in `k`; at a 10 %-of-capacity
> target it does not, and rent/nat falls monotonically straight through the magic sizes.
>
> The strongest result is not the island at all. It is the **dissociation**: two arms with
> different size functions tick up at *different* `k`, each at its own steps —
> **8/8 at its own, 0/12 at the other's**. Whatever this is, it is about **packing**, not
> about slot count.
>
> And one prediction died outright: **perfect codes are more expensive on both currencies**,
> including the flips currency where they were predicted to win.

---

## 0. Gates — ALL PASS, and one of them fired as a result

| gate | outcome |
|---|---|
| G1 shared share machinery | PASS (unchanged) |
| G2 every substrate exactly pair-uniform, `share_max = k·ln2 − ln\|S\|` | PASS — `A₁+A₂ ≤ 4e−32`, and for `k ≤ 11` confirmed independently through the IPF estimator |
| G3 Hadamard orders 8,12,16,20,24,28 | PASS — `H Hᵀ = N·I` exactly; strength 2 by direct combination counting, no Fourier |
| G4 Fourier propagator vs brute-force convolution | PASS — `≤ 8.3e−17` |
| G5 solved state IS the fixed point | PASS — drift over 30 exact steps `≤ 3.1e−13` in share, `≤ 7.8e−13` relative in state; and from `p₀` the gap falls `4.4e−6 → 6.9e−12 → 3.8e−14` and sits at the float64 floor |
| G6 `share_∞(q)` monotone, 0 at `q→0`, ceiling at `q=1` | PASS |
| **G7 decoder equivariance** | **MEASURED — and it FIRED. See below.** |
| G8 quotient route vs full route | PASS — `≤ 7.1e−15` including `cost_flips` |

**Hygiene (prereg §5), the whole point of the instrument change:** max relative target
residual **3.9e−14** (drop bar was 1e−6), `q*` inside `[9.8e−3, 0.69]` (rails 1e−9), max
`|mass−1| = 6.7e−16`, no negative probabilities anywhere. **0 of 270 rows dropped.**

### 0.1 G7 fired: most of the large exceptional structures are LOSSY

Pre-registered as a measurement with both outcomes meaningful. The criterion used is exact
and threshold-light: with `R_i(a) = Σ_j Cd[i,j,a]` the decode-weight profile of support
point `i` at distance `a`, upkeep returns uniform-on-`S` for *every* radial noise kernel iff
`R_i(a)` does not depend on `i`. The two populations separate by **12 orders of magnitude**
(`≤ 3.3e−15` vs `≥ 1.8e−4`), so this is not a threshold judgement.

| | |
|---|---|
| **EQUIVARIANT** | `k` = 5, 6, 7 (Sylvester-8), 9, 10, 11 (Paley-12), 12–15 (Sylvester-16), **23 (Paley-24)** |
| **LOSSY** | `k` = **8** (Paley-12 truncated), **16–22** (Paley-20, Paley-24), **24** (Paley-II-28) |

On a lossy substrate **full upkeep does not restore the design state** — the pre-registered
failure mode RC-A of the parent. The attainable ceiling is `0.99962 × share_max` at `k = 8`
and `0.999983 ×` at `k = 16`.

**This refines the parent's expectation and corrects its scope** (`MAINTENANCE_SWEEP_PREREG`
§1.1, which argued from `M₁₂`'s 5-transitivity that equivariance should hold at `k = 11` and
lapse at `k = 8, 9, 10`). Measured: it lapses at **`k = 8` only**, and holds at 9, 10, 11.

The Sylvester-based rows (`k` = 5–7, 12–15) are equivariant for a separate and already-known
reason — those OAs *are* linear codes, so equivariance is algebraic. The interesting split is
**within the non-linear Paley family**, and there it is **not** simply a matter of using the
array at full width: `k = 19` uses all 19 columns of `H₂₀` and is lossy, while `k = 11`
(`H₁₂`) and `k = 23` (`H₂₄`) at full width are exactly equivariant. So among the Paley orders
run here — 12, 20, 24, 28 — the two that yield an equivariant decoder are 12 and 24, which
are also the two with exceptionally large automorphism groups (`M₁₂`, `M₂₄`).
**Stated as an observation, not a theorem: I computed no automorphism group here**, and the
Mathieu reading of the pattern is a conjecture, offered as one.

**Three consequences were handled rather than absorbed**, because each could have faked the
island:

1. The closed form of the parent's §3.3 does not apply. Replaced by an **exact** solve: the
   step map is linear and the decoder has rank `|S|`, so the stationary state is fixed by a
   `|S|×|S|` Perron problem. Cross-checked against warm-started power iteration
   (`≤ 8.2e−14`) and against direct iteration of the exact step map (G5).
2. On a lossy substrate the state is **no longer pair-uniform**, so `k·ln2 − H(p)`
   *over-reads* the share — it initially reported ceilings *above* `share_max`. Corrected to
   the pairwise-maxent top of the envelope, with the `O(leak²)` residual reported per row
   (`≤ 2.9e−5` relative at `k = 8`, `≤ 1.1e−7` at `k = 16`, smaller elsewhere).
3. `cost_erase = q·(H(pre) − ln|S|)` assumes equivariance; replaced by the general
   `q·(H(pre) − H(deposit))` everywhere.

**Confound audit** — could lossiness be *causing* the upticks rather than density?

| step | equivariance matched? | observed tooth | leak correction | upkeep-deposit deficit |
|---|---|---|---|---|
| 7→8 | no | +2.24 % | 0.219 % (9.8 % of tooth) | 0.075 % (3.3 %) |
| 11→12 | **yes** | +0.81 % | 0 | 0 |
| 15→16 | no | +0.30 % | 0.008 % (2.7 % of tooth) | 0.0015 % (0.5 %) |
| 19→20 | **yes** | +0.06 % | 0 | 0 |
| 23→24 | no | −0.04 % | 0.002 % (5.5 % of tooth) | 0.0003 % (0.8 %) |

Two of the five steps (`k = 12`, `k = 20`) are between two exactly-equivariant substrates and
carry **no** lossiness confound at all, and they show the tooth. At the other three the
lossy channels are ≤ 10 % of the tooth. **Lossiness does not explain the sawtooth.**

---

## 1. The instrument change, as a number

The parent's controller settled by free decay and then held wherever it landed. Re-running
it unchanged against the fixed-point definition:

| | old achieved | new achieved | old rent/nat | new rent/nat |
|---|---|---|---|---|
| `H8`→`A8`, ε=.05, frac .5 | 0.283 | **0.500000** | 0.68161 | 0.59133 (−13.2 %) |
| `L11`→`B11`, ε=.05, frac .1 | 0.059 | **0.100000** | 0.90230 | 0.77725 (−13.9 %) |
| `E8`→`B8`, ε=.05, frac .1 | 0.056 | **0.100000** | 1.26528 | 1.03839 (−17.9 %) |

The old rows were off-target by up to a factor of two and the induced error in rent/nat
reaches **18 %** — far larger than every tooth in this study. **The `k ≤ 12` rent table in
`RENT_COMPARISON.md` should not be compared row-to-row with this one**, and its finding 2
(Hadamard beats code at matched `k`) is *re-confirmed here on the fixed instrument*:
`A11` 0.11860 < `B11` 0.12685, `A8` 0.14586 < `B8` 0.16583 (ε=.01, frac .5).

---

## 2. P-ISLAND — **MIXED (12/20)**. Verdict of record.

Pre-registered rule: ≥18/20 confirms, ≤2/20 kills, anything between is MIXED and is reported
as mixed with no post-hoc subsetting.

| condition | k=8 | k=12 | k=16 | k=20 | k=24 |
|---|---|---|---|---|---|
| ε=.01, hold 10 % | UP | UP | down | down | down |
| ε=.01, hold 50 % | UP | UP | **UP** | **UP** | UP |
| ε=.05, hold 10 % | UP | down | down | down | down |
| ε=.05, hold 50 % | UP | UP | **UP** | **UP** | down |

**12/20 total; 4/8 on the out-of-sample `k = 16, 20`; 1/4 at `k = 24`.** The rule returns
MIXED and I am not permitted to rescue it. The `k = 8` and `k = 12` cells were disclosed
in advance as in-sample (prereg §1.3) and cannot be counted as evidence twice.

**Islands as local minima** (below both neighbours), the same data read as a shape:

| condition | k=7 | k=11 | k=15 | k=19 | k=23 |
|---|---|---|---|---|---|
| ε=.01, hold 50 % | MIN | MIN | MIN | MIN | MIN |
| ε=.05, hold 50 % | MIN | MIN | MIN | MIN | no |
| ε=.01, hold 10 % | MIN | MIN | no | no | no |
| ε=.05, hold 10 % | MIN | no | no | no | no |

### 2.1 The pre-registered SECONDARY disagrees with the primary — and the prereg says so

Prereg §4: *"If the frac-matched and abs-matched readings disagree in their verdict on
P-ISLAND, that disagreement is itself the finding and both are reported."* They disagree.

**Holding exactly 1.0 nat — the same amount of pattern on every substrate — gives 9/10
upticks**: UP at `k` = 8, 12, 16, 20, 24 at ε=0.01, and at 8, 12, 16, 20 at ε=0.05. At
ε=0.01 **all five** `k ≡ 3 (mod 4)` are local minima (7, 11, 15, 19, 23); at ε=0.05 the
first four are and `k = 23` is not, matching the one missing uptick. This is the cleanest
island signal in the study, and it is a **pre-registered secondary, not the primary**.

Why the two differ is arithmetic, not interpretation: at a fixed *fraction* of capacity the
absolute nats held also change with `k`, so the frac-matched comparison moves two things at
once. The abs-matched comparison asks the cleaner economic question — *what does the same
nat of pattern cost on this substrate versus that one* — and there the sawtooth is plain.

---

## 3. P-DISSOCIATION — **CONFIRMED, cleanly. The strongest result here.**

ARM A's size function `N₀(k) = 4⌈(k+1)/4⌉` steps at `k` ≡ 0 (mod 4). ARM B's,
`2^⌈log₂(k+1)⌉`, steps only at `k` = 8 and 16. They therefore predict islands at *different*
`k`, fixed by arithmetic before the run.

| | k=8 | k=12 | k=16 | k=20 | k=24 |
|---|---|---|---|---|---|
| ARM B's own step? | **yes** | no | **yes** | no | no |
| ARM B ticks up? (4 conditions) | **4/4** | **0/4** | **4/4** | **0/4** | **0/4** |

**8/8 upticks at ARM B's own steps; 0/12 at ARM A's steps that are not ARM B's.** Perfect
separation. The effect follows each structure's *own* packing arithmetic and is not a
function of slot count. This is the mechanism test, and it is unambiguous.

**The disclosed `d` confound is resolved.** ARM B's selection rule happens to return dual
distance `d = 4` at exactly `k = 8` and `k = 16`, and higher `d` decays faster. The
pre-registered `d = 3`-constrained ARM B′ still ticks up at both, in **4/4** conditions each
(e.g. `k=16`, ε=.05, frac .5: B′ 0.490853 vs 0.456160 at `k=15`). The uptick is **not** a
decay-rate effect.

---

## 4. P-DENSITY — supported in direction and magnitude, not as a strict collapse

Strict monotonicity of rent/nat in density holds at ε=0.01 / hold 50 % and fails elsewhere,
with the inversions always at the step points — i.e. the sawtooth does not fully collapse
onto density.

But the **magnitude** match is the striking part. At ε=0.01, hold 50 %, observed tooth
against the pre-registered density-drop prediction:

| step | k=8 | k=12 | k=16 | k=20 | k=24 |
|---|---|---|---|---|---|
| predicted density drop | 3.4 % | 1.1 % | 0.47 % | 0.23 % | 0.12 % |
| observed tooth | 3.12 % | 1.14 % | 0.45 % | 0.15 % | 0.014 % |
| ratio | 0.92 | 1.04 | 0.97 | 0.66 | 0.12 |

The first three teeth match a prediction made before the run to within 8 %, and the
predicted `~1/k²` shrinkage of the teeth is reproduced. The last two fall below prediction;
`k = 24` is at the edge of resolution.

---

## 5. P-PERFECT — half confirmed, half **DEAD**

Predicted: perfect codes are *not* the cheapness mechanism (they should lose badly on nats,
because they are far less dense), but should *win* on the flips currency, where their
tie-free radius-`t` decoder is optimal.

- **On nats: CONFIRMED, decisively.** ARM C is more expensive at all 12 comparisons.
  At `k = 15`, Hamming `[15,11]` costs **0.309 vs 0.106** for the max-share simplex — 2.9×.
  At `k = 23`, Golay `[23,12,7]` costs **0.185 vs 0.092** — 2.0×. So `k = 15` and `k = 23`
  being "doubly magic" does not make them cheap twice; the perfect-code property is not the
  mechanism, and density is what is doing the work.
- **On flips: the prediction is DEAD.** ARM C is *also* more expensive on flips, at all 12
  comparisons (`k=15`, ε=.05, hold 50 %: 0.266 vs 0.152). A tie-free covering decoder does
  not buy cheaper maintenance in bits flipped. The reasoning behind the prediction — that
  optimal covering means fewer corrective flips per unit of upkeep — was simply wrong: the
  flips bill is dominated by how far the noisy state drifts from a much sparser support, and
  ARM C's support is 128× larger but its capacity per slot is 2.7× smaller.

**Recorded dead, kept in the record, not rescued.**

Note the construction fact stated in the prereg and confirmed here: at `k = 12…15` ARMs A
and B are the *same object* (the Sylvester-16 OA **is** the simplex `[15,4]`, the dual of the
perfect Hamming code), so the `k = 15` double-magic question could only ever be settled
against ARM C, and it was.

---

## 6. P-PLATEAU — the decline does not exhaust in range; the floor is not identifiable

Best fit by AIC is POWER at 3 of 4 conditions; at ε=0.01/hold 50 % the decline-to-floor
model wins by ΔAIC = 0.25, which is no preference at all. In **every** condition the fitted
floor `c` lands at **94.5–97.4 % of the smallest measured rent/nat** — i.e. the fit puts the
floor at the last data point, which is what an unidentifiable parameter looks like.

**P-PLATEAU as pre-registered: supported.** Within `k = 5…24` the scale economy does not
exhaust, and `c` is not resolvable. **No `k > 24` claim is made, and `c` is a curve parameter
over the measured range — it is not "the price of habit".**

---

## 7. POST-HOC — clearly labelled, not evidence

Not pre-registered. Included because the primary and the pre-registered secondary disagreed
and the prereg requires that disagreement to be explained rather than resolved by choosing a
winner.

**(a) The tooth against the local trend.** Taking the step's log-jump minus the mean
log-jump within the run that follows it removes the background decline:

| condition | k=8 | k=12 | k=16 | k=20 |
|---|---|---|---|---|
| ε=.01, hold 10 % | +10.30 pp | +5.50 pp | +3.46 pp | +2.37 pp |
| ε=.01, hold 50 % | +9.97 pp | +5.24 pp | +3.24 pp | +2.19 pp |
| ε=.05, hold 50 % | +7.70 pp | +4.25 pp | +2.71 pp | +1.86 pp |
| ε=.01, hold 1.0 nat | +8.28 pp | +4.90 pp | +3.26 pp | +2.30 pp |
| **the density ceiling's own tooth** | **−10.15 pp** | **−4.29 pp** | **−2.37 pp** | **−1.50 pp** |

The rent tooth is very nearly the **negative image of the ceiling's own tooth**, at every
step and in every condition, with an elasticity near 1 at `k = 8` drifting to ~1.5 by
`k = 20`. **The tooth is present in every condition at similar size; what differs between
hold-10 % and hold-50 % is only the steepness of the trend it sits on.** That is the whole
explanation of the mixed primary.

**(b) Sign of the residual** after removing the fitted `a·k^(−b)`: islands below trend and
steps above trend, **9/10 in five of the six conditions** (6/10 in the sixth, ε=.05 at
1.0 nat). The sawtooth's *phase* is as predicted essentially everywhere.

`k = 24` cannot be trend-corrected: it would need `k = 25, 26, 27`, which were not run.

---

## 8. Limitations

1. **Designed substrates.** Everything here is a price, not a prevalence. Nothing bears on
   `wild-share`.
2. **The primary test is MIXED.** §7 explains why, but §7 is post-hoc. The honest one-line
   summary is *"the sawtooth is there, and whether it makes an island depends on the target"*
   — not *"islands confirmed"*.
3. **`k = 24` is inconclusive.** The predicted tooth (0.12 %) is at the edge of what survives
   the trend, it flips sign between the two ε, and it cannot be trend-corrected without
   `k = 25…27`.
4. **The equivariance/automorphism observation is not a theorem.** I measured that `k = 11`
   and `k = 23` are equivariant and the Paley-20 family is not. I did **not** compute any
   automorphism group, and the `M₁₂`/`M₂₄` reading of that pattern is a conjecture stated as
   one.
5. **No extrapolation.** Nothing about `k → ∞`, no asymptotic cost of habit.
6. **The structural mismatch with `Core/Maintenance.lean` stands unchanged** (parent §3.6):
   payment here is proportional to the *deficit*, not to the *amount*. The substrate
   instantiates `unpaid`/`unpaid_decays` literally and `rent_holds` only in the weaker sense
   that some payment holds the amount steady.
7. **No novelty is claimed** for the classical maximum, the OA/Hadamard equivalence, or any
   of the three perfect codes — Gavinsky–Pudlák 2016, Babai 2013, Lancaster 1965,
   Hedayat–Sloane–Stufken 1999 Thm 7.5. See `HADAMARD_CONNECTION.md` §B.5.
8. **Nothing here is mechanized.** No Lean file touched, no result offered to the audit.
9. **The island-of-stability analogy is a name for a shape in a plot.** §0 governs.
