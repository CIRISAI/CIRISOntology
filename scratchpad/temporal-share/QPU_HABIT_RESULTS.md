# The lifecycle of a habit on a quantum processor — results

**Device:** ibm_marrakesh (Heron), qubits 6 – 7 – 8. **Pre-registration:**
`QPU_HABIT_PREREG.md`, committed `bdcbcf2`; addendum 1 committed `4ec64b2`, both before
the runs they govern. **Jobs:** A run 1 `d9immeqbr2fc73e4u02g` (VOID, 72 s), screen
`d9imr2rjf64c739fp9rg` (6 s), A run 2 `d9imu8gii2cc73edq0bg` (75 s), B
`d9imvhqbr2fc73e4ucd0` (35 s). **188 QPU seconds** total; 212 s of the 600 s allocation
remain.

---

## THE KILL FIRED

**The pre-registered rent-shape test FAILS on shape, and passes on rate.** Stated as
plainly as a survival would be:

| pre-registered test | staked | measured | verdict |
|---|---|---|---|
| **K-RATE** `R_D = rate_D / Γ₁` | [0.864, 1.154] | **1.072** | **passes** |
| **K-SHAPE** χ² of log\|D̂\|, slope fixed at −Γ₁, dof 9 | ≤ 26.46 | **153.1** | **FAILS** |
| **K-FAMILY** ΔAIC(exponential − power law) | ≤ +10 | **+67.1** | **FAILS** |

The unpaid decay of a whole-only habit on this device is **not** a single exponential at
the rate its own relaxation times fix. It decays at very nearly the right *rate* — within
7 %, inside a band that allowed 15 % — but with the wrong *shape*, and the wrong shape is
resolved at enormous significance, not marginally.

**What this kills, exactly:** the claim that the rent clause's geometric decay
(`Core/Maintenance.lean`, `unpaid_decays`) is the shape a real unmaintained habit takes.
It is not, on the substrate textbook physics says is friendliest to it. **What it does not
touch:** `unpaid_decays` and `rent_holds` themselves, which are theorems about a model and
remain true of that model; the mint theorems; and anything about nature's wild processes,
on which this run bears not at all.

**Validity, checked before the verdict was read:** readout assignment fidelity 0.9911
(floor 0.95), calibration drift across the job 0.0012, all ten null controls ≤ 1.2 × 10⁻⁴
(threshold 1.5 × 10⁻³), all three in-job T1 in range, Γ₁ measured to 1.16 %. No VOID
condition fired. All ten delay points cleared the SNR ≥ 5 fit rule (SNR 9.3 to 127).

## Where the failure is — post-hoc diagnosis, labelled as such

Nothing here un-fires the kill. It only locates it, and it locates it in the substrate
rather than in the habit.

**The device's own one-body relaxation is not exponential either.** Fitting the in-job T1
audit with a stretched exponential `exp(−(t/T)^β)`:

| qubit | β | χ² stretched (dof 2) | χ² pure exponential (dof 3) |
|---|---|---|---|
| 6 | 0.955 | 0.8 | 2.9 |
| 8 | **0.872** | 2.7 | **34.1** |
| 7 | 0.958 | 2.9 | 4.8 |

On qubit 8 the single exponential is rejected outright by the *one-body* data alone.

**And the three-body correlator is stretched by the same amount, at the rate the parts
fix.** Fitting D(t) directly:

- stretched: β = **0.879**, 1/T = 0.01810 /µs, χ² = **6.0** (dof 7)
- pure exponential: r = 0.01734 /µs, χ² = **26.8** (dof 8)
- mean one-body β = 0.928 vs three-body β = 0.879; 1/T_stretched / Γ₁ = **1.051**

So the honest reading is: **the ledger's rate survives and its exponential shape does not,
because the hardware is not the memoryless channel it is idealised as.** A superconducting
qubit's T1 fluctuates in time (the standard TLS story — Klimov et al., PRL 121, 090502,
2018; Burnett et al., npj QI 5, 54, 2019), and an average over fluctuating T1 is always a
stretched exponential: faster early, slower late. That is exactly the residual pattern
(the measured share sits −5.7σ, −10.7σ, −6.0σ, −4.3σ, −3.6σ below the model at the first
five delays and lands on it at the last five).

**One diagnostic came back inconclusive and is reported as such.** The model-free product
test — does D(t) equal κ₁κ₂κ₃ with the parts' decays read off the *same* circuits, no
exponential assumed — shows a +4.8σ upward trend (ratio 1.05 → 1.37). It should not be
believed at that face value: extracting κ from the parity state's marginals needs the
equilibrium level m_q, which this job measures only through the single-exponential audit
fit now known to be misspecified, and the ratio already reads 1.05 at t = 0 where it must
read exactly 1. The design fix is named: measure the parts' decay on the *same delay grid*
as the whole, from a |111⟩ arm that saturates. Until then, whether the whole comes apart
on a schedule of its own is **open**, and we do not claim it either way.

## The two habits, born equal, dying at different rates

Both preparations carry exactly one bit at t = 0, and the same instrument reads both.
The 2 × 2 table (prep × basis) at t = 0, against an ideal of (ln 2, 0; 0, ln 2):

| | read in Z | read in X |
|---|---|---|
| **classical parity mixture** | **0.6553** | 0.00012 |
| **GHZ** | −0.00000 | **0.6475** |

The quantum habit is the same parity habit, written in a basis you must know to read; read
in the wrong basis each reads zero, and those two zeros are the instrument's false-positive
floor, sitting at 10⁻⁴.

Measured decay rates in share units: **classical 0.0320 /µs, quantum 0.0601 /µs — the
quantum habit dies 1.88× faster**, against a calibration prediction of 1.87×. That
agreement is the demonstration working; the ordering itself is a property of *these
qubits* (T2 < T1 here) and was stated in advance to be conditional, not a law. Nothing
about the physics is new — this is GHZ decoherence (Monz et al. 2011) re-read in share
units.

## JOB B — mint, wrong code, and the price of rent in erased bits

**The mint.** One circuit carries both sides of `repair_mints_from_noise`: its mid-circuit
record is the input, its final record the output, on the same shots.

| arm | share in | share out | S_total out | per-shot map held |
|---|---|---|---|---|
| **MINT** (c := a ⊕ b) | 0.00025 | **0.6180** | 0.6198 | 95.09 % |
| **COPY** (wrong code, c := a) | 0.00000 | **0.00015** | 0.6241 | 96.98 % |
| **NONE** (no repair) | 0.00003 | 0.00000 | 0.00018 | 94.10 % |

One application of the parity code's repair to pure noise moved the whole-only share from
0.00025 to 0.6180 nat, paying one physical bit erasure (the `reset`) to do it. The wrong
code, run on the same noise through the same machinery, minted **zero** whole-only share
(0.00015, at the floor) while minting ordinary correlation (S_total 0.624) — the control
that makes the mint mean something.

Honest gap: 0.6180 is **below** the pre-registered band [0.653, 0.705], by about 4 sd. The
theorem is not falsified — it is a theorem — the device's execution of it is, and the cause
is visible in the controls: the NONE arm, which does nothing at all, preserves its three
bits on only 94.10 % of shots. The ~5 % loss is the mid-circuit measurement chain, not the
repair; the repair arm actually held its map *more* often than the no-op control held its
bits.

**The rent, in bits erased.** Same total idle time, different numbers of payments:

| total idle | bits erased (resets) | share retained | vs unpaid |
|---|---|---|---|
| 44.7 µs | 0 | 0.1593 | — |
| | **1** | **0.5477** | **3.4×** |
| | 2 | 0.5429 | |
| | 4 | 0.5200 | |
| 92.7 µs | 0 | 0.0568 | — |
| | **1** | **0.4313** | **7.6×** |
| | 2 | 0.4070 | |
| | 4 | 0.4009 | |

**The first erased bit buys 0.39 nat of held habit at 44.7 µs and 0.37 nat at 92.7 µs.
Every further erasure buys nothing, and costs a little.** The paid arms are flat-to-
decreasing in n with spread 0.028 and 0.030, inside the pre-registered ceiling of 0.03 —
the prediction we registered precisely because it was unflattering: this code's repair is
a projection (`parityRepair_idempotent`), so it restores the *relation* and never the
*values*, and only the last payment does any work. That is the hardware face of
idempotence, and it is what the rent on this ledger actually costs: one bit, once.

## Scope

Engineered hardware, not nature. Nothing here bears on `wild-share`. Three of the four
legs are demonstrations of textbook physics executed as Lean theorems and are labelled as
such throughout; the one genuine test is leg 3, and it failed on shape. No stance change
is proposed from this run, and none should be made without the refuter pass.

## What run 1 cost, and what it bought

Job A run 1 VOIDed on readout fidelity (0.9047 against a 0.95 floor) and is kept in the
record. It cost 72 QPU seconds and bought two things: an analysis bug of ours (readout
corrections applied to permuted slots — fixed, regression-tested, and nearly invisible
because D's correction is a *product*), and the lesson that on this device the published
calibration is not something to select on. It listed P(0|1) = 0.0098 for qubit 13 where a
6-second screening job measured **0.127**. Run 2 selected on measurement and returned a
readout fidelity of 0.9911.

## Named next steps

1. Measure the parts' decay on the same delay grid as the whole, so the model-free product
   test has the precision to settle whether the whole comes apart on its own schedule.
2. If the substrate's stretched exponential is the story, the interesting pre-registration
   is the one that predicts β for the whole from β of the parts — under fluctuating T1 the
   three-body correlator should stretch *more* than the one-body (we measured 0.879 vs
   0.928, in that direction, with no advance prediction staked).
3. The mint arm is limited by the mid-circuit measurement chain (~5 %), not by the repair.
   A fresh-ancilla variant would separate them.

---

# Run 3 — the sector-flow dichotomy (job `d9in8jrjf64c739fprqg`, 100 QPU s)

Pre-registered in addendum 2, committed `5d1780a` before submission. Screen 6 s + job
100 s. **106 s of the 600 s allocation remain.** Valid run: readout fidelity 0.9907
(floor 0.95), calibration drift across the job 0.0009 (ceiling 0.02). No VOID.

## Verdict: four of five pass, one fires

| pre-registered test | staked | measured | |
|---|---|---|---|
| **K-CURVE** χ² of the bulge vs a curve built from measured decays, dof 12, **zero free parameters** | ≤ 32.21 | **24.44** | **PASS** |
| **K-PEAK-t** bulge peak location | ∈ {20.6 … 65.6 µs} | **49.5 µs** | **PASS** |
| **K-PEAK-h** bulge peak height | ∈ [0.0433, 0.0569] | **0.05405** | **PASS** |
| **K-PAIRMULT** cov/(κᵢκⱼcov₀) | ∈ [0.832, 1.176] | **[0.940, 1.308]** | **FAILS** |
| — its "no rise" half | no cov above its t=0 value | **+0.0000** | **PASS** |
| **K-PAIRZERO** max pair MI on the parity arm | ≤ 9.40 × 10⁻⁴ | **9.09 × 10⁻⁴** | **PASS** (at 97 % of threshold) |
| **K-NULL-Z** product arm | ≤ 5.41 × 10⁻⁴ | **1.21 × 10⁻⁴** | **PASS** |
| **K-NULL-X** \|+++⟩ arm | ≤ 1.70 × 10⁻³ | **9.80 × 10⁻⁴** | **PASS** |

## The one-way valve, measured

**Order flows up, and never down.** Three preparations, identical single-site noise:

- **Whole-only pattern is created out of pairwise pattern.** The ferro habit (order-2 only,
  share exactly 0 at t = 0, measured 0.00023) grew a whole-only bulge to **0.0541 nat** at
  49.5 µs and decayed away again — while its pair covariances fell monotonically from
  ~0.99 to ~0.08. Single-site noise, which cannot read any pair of qubits, nonetheless
  moved pattern from the pair sector into the whole-only sector.
- **It is never created out of nothing.** The independent-bits arm stayed at
  1.2 × 10⁻⁴ nat across 169 µs of idling — the entire single-qubit error budget (T1, T2,
  readout, thermal) provably cannot move it, and did not. Likewise the coherent \|+++⟩ arm
  in the X basis, at 9.8 × 10⁻⁴.
- **It never flows back down.** The parity habit (order-3 only) shed its whole-only share
  from 0.655 to 0.017, and its pair sector stayed at 9 × 10⁻⁴ nat throughout — no pairwise
  bulge, at any delay, on any pair. Exactly as the multiplicative law requires.

The bulge curve is the strongest result: **χ² 24.4 on twelve points with no free parameter
and no functional form assumed anywhere.** The audit arm rode the bulge arm's exact delay
grid, so each qubit's decay κ_q(t) was measured at every point and fed straight into the
exact k = 3 solver. That design was forced by run 2's finding that this substrate is not a
single exponential — and it works: run 2's shape kill was a consequence of assuming an
exponential, and run 3, assuming nothing, fits.

## The fired criterion, reported as loudly

**K-PAIRMULT failed at its upper edge:** the ratio cov_ij(t)/(κ_i κ_j cov_ij(0)) should sit
at 1 and reached **1.308**, outside the staked [0.832, 1.176]. The exact multiplicative law
`cov → κ_i κ_j cov` is elementary and machine-verified to 10⁻¹⁶, so a genuine violation
would mean the device's noise is not single-site.

Post-hoc, labelled: the deviation is confined to the **tail**. The ratios are 0.99–1.03 out
to 37.5 µs and only drift upward from ~88 µs, and they drift in exactly the direction an
**overestimated p_exc** produces. p_exc was taken from a saturation point at 784 µs, which
is only 2.8 T1 for qubit 7 — leaving ~6 % unrelaxed population — and qubit 7 carries the
largest fitted p_exc (0.0905) and the largest ratio drift. An overestimated p_exc
underestimates κ at late times, which inflates the ratio. The same κ values pass K-CURVE on
the same circuits, which is evidence they are good where the bulge lives.

**But the criterion was staked and it fired, and it stays fired.** Named fix, not a rescue:
measure p_exc from a dedicated long-idle \|0⟩ arm rather than from the tail of the \|1⟩
decay, and extend the saturation delay past 5 T1.

## A secondary reading, offered as a bound and not a claim

Two independent arms show small excesses at the same scale: the parity arm's pair MI
(9.1 × 10⁻⁴, at the 97th percentile of its null) and the \|+++⟩ arm's share, which grows
with delay from 1.3 × 10⁻⁷ at t = 0 to ~10⁻³ by 16 µs. Both are within their staked bands
and neither is claimed. Both are where **two-site** noise would show up, and the \|+++⟩ arm
is background-free against every single-site channel by theorem. Read as a bound: correlated
noise on this triple contributes **< 10⁻³ nat** of whole-only share over 60 µs. Making that
a measurement rather than a bound needs a longer lever arm and a ZZ-rate prediction to test
against — named, not attempted.

## Scope

Still engineered hardware. What is new here is not the physics — the multiplicative decay
of correlations under local noise is elementary — but the observable: that the three order
sectors form a one-way valve under single-site noise, stated as a measurable and measured
with a parameter-free, model-free curve. The claim that single-site noise cannot create
whole-only share **at all** is false, and we refuted it ourselves before spending budget on
it; the true statement is narrower and sharper, and is what run 3 confirms.

---

# Addendum — diagnosing run 2's shape failure (POST-HOC, no new QPU seconds)

**The fired kills stand exactly as staked and are not retracted.** Run 2's K-SHAPE
(χ² 153.1 vs ≤ 26.46) and K-FAMILY (ΔAIC +67.1 vs ≤ +10) failed; K-RATE passed at 1.072.
Nothing below un-fires them. This section only asks *why*, using data already in hand.

## Which observable K-SHAPE was staked on, and why it matters

**D, the connected three-body moment `M₁₂₃ − M₁M₂M₃` — not the share.** The
pre-registration says so and says why: staking on the absolute share would fire on
preparation fidelity. The concern that a nonlinear readout broke the shape by itself is
therefore ruled out by construction — and it is a real concern, because the share *is* a
singular readout of D: with uniform marginals `share = ½[(1+D)ln(1+D) + (1−D)ln(1−D)]`,
whose derivative `½ln((1+D)/(1−D))` diverges logarithmically as D → 1, giving the share a
`t·ln(1/t)` term at early times. Staking shape on the share would have been an error. It
was not made.

## Candidate 1 (the cascade) — ruled out by algebra, not by fitting

For the parity state under **any** independent single-site channel, the exact channel
algebra gives

```
raw        M₁₂₃(t) = κ₁κ₂κ₃ + b₁b₂b₃     <- carries exactly the drift/cascade term
connected  D(t)    = κ₁κ₂κ₃              <- the b-term cancels IDENTICALLY
```

because the parity state's one- and two-body moments are zero and stay zero
(`cov → κᵢκⱼcov`, and cov(0) = 0). Verified to **2.8 × 10⁻¹⁷ over 400 random asymmetric
channels**. So the staked observable is a *pure product of the three survival factors* — it
cannot be a sum of exponentials at hierarchy rates. The cascade is real in the raw moment
and was already subtracted away.

Its other signature is absent too: a decaying whole-only pattern depositing transient pair
correlation is forbidden by the same multiplicative law, and run 3 measured the parity
arm's pair sector flat at |cov| ≤ 4.2 × 10⁻² (consistent with a prep offset at the
1/√N ≈ 1.1 × 10⁻² shot-noise scale) with no significant rise at any delay.

**The naivety was not in the composition law. It was in assuming the factors κ are
exponential.**

## Candidate 2 (device rate fluctuation) — confirmed on three independent marks

**(i) The singles bend.** Run 3's audit measured each qubit's decay at 14 delays:

| qubit | β (stretched) | χ² pure exponential (dof 11) | χ² stretched (dof 10) |
|---|---|---|---|
| 6 | 0.935 | 49.1 | 16.2 |
| **8** | **0.853** | **257.9** | **9.1** |
| 7 | 1.022 | 22.6 | 20.0 |

Under candidate 1 the singles would stay pure exponentials. Two of three bend, one
decisively. The effect is per-qubit, dominated by qubit 8.

**(ii) The rates wander between jobs.** Same three qubits, ~30 minutes apart:
T1(q6) 258.7 → 196.3 µs (**−24.1 %**), T1(q8) 104.9 → 126.7 µs (**+20.8 %**),
T1(q7) 261.6 → 304.3 µs (**+16.3 %**). Tens of percent on the timescale of a job, with the
readout calibration meanwhile stable to 0.0009 — so this is relaxation wander, not a
general instrument drift. This is the standard TLS picture, credited: Klimov et al.,
PRL 121, 090502 (2018); Burnett et al., npj QI 5, 54 (2019).

**(iii) The composition law survives once the factors are measured rather than assumed.**
Run 3's parity arm gives D(t); its audit arm gives κ_q(t) directly. Testing the identity
D(t) = κ₁κ₂κ₃ with **no functional form anywhere** and the shot noise of *both*
measurements propagated:

| t (µs) | 0 | 11.3 | 32.3 | 64.6 | 106.6 | 161.5 |
|---|---|---|---|---|---|---|
| D/Πκ | 0.989 | 1.002 | 1.002 | 1.100 | 1.016 | 1.237 |
| ± | 0.011 | 0.015 | 0.021 | 0.038 | 0.063 | 0.143 |
| σ from 1 | −1.0 | +0.1 | +0.1 | **+2.6** | +0.3 | +1.7 |

**χ² = 10.74 on 6 points, p = 0.097 — consistent.** Against χ² 153 on 9 points for the
single-exponential form on the same kind of data.

One systematic had to be fixed first, and it is the same one that fired run 3's
K-PAIRMULT: p_exc was read off a saturation point at only 2.6 T1 for qubit 7, which
overestimates it (0.0905 against a saturation-corrected 0.0156) and thereby underestimates
κ at long delay. Correcting it moved the ratio spread from sd 0.124 to sd 0.087. This is a
**named design fault with a named fix** (take p_exc from a dedicated long-idle |0⟩ arm, or
extend saturation past 5 T1), not a free parameter.

## Verdict

**Candidate 2: device rate fluctuation — a hardware fact, credited to the TLS literature.**
Run 2's shape kill fired because the pre-registered reduced form assumed the survival
factors were exponential and on this device they are not. The framework's composition law —
that the whole-only correlator is the product of the parts' survival factors — is intact
and, when the factors are measured instead of assumed, fits.

**This is not a survival of anything.** The kills stay fired. Claiming the composition law
requires it to be pre-registered *as* the prediction and tested on fresh data. Note that
this has already partly happened: run 3's K-CURVE staked exactly this measured-κ
construction in advance, on the ferro arm, and **passed at χ² 24.4 on 12 points with zero
free parameters**. The parity arm's version has not been pre-registered.

## Proposed next run — stated, not run

Not the run the cascade hypothesis would have motivated, since the cascade is excluded. The
right one is a re-stake of run 2's kill in the corrected form: parity arm and audit arm on
a **shared** delay grid, D(t) vs Πκ_q(t) pre-registered as the prediction, with p_exc from a
dedicated |0⟩ saturation arm past 5 T1. Estimated **45–55 QPU s** against **106 s
remaining**, which would leave the 60 s reserve intact only at the low end. It is a real
decision about the last of the budget, so it is put to you rather than taken: it would
convert an explained failure into a pre-registered test of the composition law, on the one
arm where that law has not yet been staked in advance.
