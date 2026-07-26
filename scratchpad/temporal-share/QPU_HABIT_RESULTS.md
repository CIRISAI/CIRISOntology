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
