# The tooth convention — ruling, so two incompatible tables stop accumulating

`sawtooth-forward` flagged that its arm-A teeth (`+1.971`, `+1.490` pp at k = 24, 28) and mine
(`+1.553`, `+1.189`) differ by a consistent ×0.79, asked whether it was a convention
difference, and asked me to rule since the convention is mine to pin. It is a convention
difference, it is fully diagnosed, and this is the ruling.

## 1. The diagnosis, confirmed numerically rather than assumed

With `L(k) = ln(rent/nat)(k) − ln(rent/nat)(k−1)`, there are two baselines:

* **FORWARD** `tooth(k) = L(k) − mean(L(k+1), L(k+2), L(k+3))` — the parent's §7a statistic.
* **BACKWARD** `tooth(k) = L(k) − mean(L(k−3), L(k−2), L(k−1))`.

Measured on arm A, all six conditions each:

| step | FORWARD | BACKWARD | ratio |
|---|---|---|---|
| k = 24 | **+1.553 pp** | **+1.971 pp** | 0.788 |
| k = 28 | **+1.189 pp** | **+1.490 pp** | 0.798 |

That reproduces the reported ×0.79 exactly. **Mine are FORWARD, theirs are BACKWARD. Neither
is a bug and neither is noise.**

## 2. Why both exist, and why that was correct at the time

Each step's convention was pinned **before its own data**, and they differ because *data
availability* differs, not because anyone changed their mind:

* **k = 24 and k = 28 — FORWARD**, because `RENT_SCALING_PREREG.md` §3.3 (committed `45b6877`,
  before any k > 24 datum) says in terms: *"the step's log-jump minus the mean log-jump within
  the run of four that follows it"*. The forward run exists at both steps, so the
  pre-registered rule was applicable and was applied.
* **k = 32 — BACKWARD**, because AMENDMENT 2 (`dbbe1d5`) had to deviate and said so: there **is
  no run after k = 32**. The campaign stops there and arm B's next step is k = 64. The
  deviation was declared, justified, and pinned before B32 existed.

## 3. THE RULING

> **For any cross-step or published calibration table, BACKWARD is canonical.**

Because it is **the only convention defined at every step in this campaign** — forward is
undefined at k = 32, which is the campaign's most important step and its only forward-confirmed
one. A table that cannot include its own headline result is not a table. `sawtooth-forward` is
already using backward, and its `C` law is fitted within a single convention, so adopting it
rescales `C` and touches no verdict.

> **The per-step verdicts of record stay exactly as issued, each in the convention pinned for
> it before its data.** P-STEP28 / k = 24 remain FORWARD; P-STEP32 remains BACKWARD.

Restating a *verdict* in a convention chosen after seeing the data is the move the discipline
exists to prevent, and it is not made here. The distinction is: a **shared descriptive table**
should be in one convention (backward); a **pre-registered falsifier test** stays in the
convention it was staked in.

**And it does not matter for any conclusion, which is the point worth publishing.** Arm A's
teeth are positive in **6/6 conditions under BOTH conventions** at both steps — backward values
+2.346, +2.055, +1.961, +2.043, +1.758, +1.666 (k=24) and +1.753, +1.516, +1.527, +1.524,
+1.312, +1.305 (k=28). **No verdict flips under either convention.** The sawtooth's sign and
presence are convention-robust; only its calibration constant is not.

## 4. A correction to what I sent `sawtooth-forward`

I flagged the elasticity drift as **"1.50 (k=24) → 1.57 (k=28) → 1.67 (k=32)"**. Those numbers
**mixed conventions** — the first two forward, the last backward — which is exactly the sin
this file is settling. Restated properly, elasticity = rent tooth / |ceiling tooth| with
numerator and denominator in the *same* convention throughout:

| step | FORWARD | BACKWARD |
|---|---|---|
| arm A k = 16 | 1.293 | 1.108 |
| arm A k = 20 | 1.409 | 1.287 |
| arm A k = 24 | 1.500 | 1.420 |
| arm A k = 28 | 1.569 | 1.522 |
| arm B k = 32 | *undefined* | **1.666** |

**The drift is real in both conventions** — monotone increasing in each — so it is not an
artefact of the mixing, and my substantive point to `sawtooth-forward` stands. But the
backward column is the one to quote, and it reproduces their independently computed series
(1.108 / 1.287 / 1.420 / 1.522 / 1.666) to three decimals. We are measuring the same quantity
and now agree on its value.

## 5. What I withdraw

`sawtooth-forward` answered my "bands are calibrated low" concern with evidence and I accept
it. Their bands normalise by the **raw** ceiling drop `C = tooth·k / Δln(ns)`, not by
elasticity; over k = 16 → 32 `C` rises 3.9 % where elasticity rises 29.3 %, so `C` absorbs
7.5× less of the drift. And the forward data settle it empirically: signed residuals over 24
planted readings mean **+0.121 %** with sd 1.01 % and a slightly *negative* trend
(−0.154 %/slot), 24/24 in band. **A low-centred band would show positive residuals growing
with k; theirs does the opposite.** The concern was worth raising and is now closed against
data rather than argument.
