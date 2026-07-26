# Pre-registration — the lifecycle of a habit on a quantum processor

**Date:** 2026-07-26 (UTC). **Status:** written and committed BEFORE any hardware job
of this campaign is submitted. The simulator gate has passed; the bands below are
SIMULATION-DERIVED, per the run-1 lesson (`HW_RESULTS.md`: never stake a criterion the
noisy device cannot meet). Nothing in this file may move after data.

**Artifacts frozen with it:** `qpu_habit_freeze.json` (the pinned qubits + the
calibration snapshot), `qpu_habit_pipeline.py` (circuits, instrument, runners),
`qpu_habit_gate.py` (the gate), `qpu_habit_bands.py` (every band), `qpu_habit_gate.json`,
`qpu_habit_bands.json`.

---

## 0. What is being attempted, in one paragraph

A habit is minted from noise, held under paid maintenance, and defaulted when payment
stops — on real hardware, read in **share units** (the whole-only share `I_C^(3)`, nats),
with a machine-checked predicted value at each stage. Three of the four legs are
**demonstrations**: they execute theorems of `Core/Creation.lean` and `Core/Maintenance.lean`
on a physical device, and their physics is textbook. **One leg is a genuine
parameter-free test with a real kill** — the shape and rate of the unpaid decay, predicted
with zero adjustable parameters from independently measured relaxation times. Its
falsification will be reported as loudly as its survival.

**Scope, stated once and not softened.** This is engineered hardware, not nature. Nothing
here bears on `wild-share` (which of nature's processes carry whole-only share); nothing
here is evidence that any natural system obeys the rent clause. A superconducting qubit
idling is a *designed* memoryless channel, and that is precisely why it is the right place
to ask whether the rent clause's *shape* survives contact with a real substrate — the
chaotic CIRISArray refused both decay families (`HABIT_DYNAMICS_RESULTS.md`), and the
honest reading of that was "this substrate is not a rent-clause substrate." Here the
substrate is one that textbook physics says *should* be. If the shape fails even here,
the rent clause has no physical reading at all.

## 1. The instrument

`I_C^(3)` = H(pairwise maxent carrying the same pair marginals) − H(state), in nats, on
three binary slots; the maxent is the EXACT k = 3 bisection solver (numpy port of the
validated `eca_spike.py:pairwise_maxent_exact`; IPF is not used anywhere, because IPF
one-sidedly overstates the share near the boundary — `ipf-sharek-boundary-drift` — and the
late-delay points of this experiment live exactly there).

Verified against the machine-checked values before any use:

| state | instrument | Lean |
|---|---|---|
| parity | share = 0.693147180560 | `share_parity` = log 2 |
| indep (uniform) | share = 0.000000 | `share_indep` = 0 |
| ferro | share = 0.000000, S_total = 2 log 2 | `share_ferro` = 0, `S_total_ferro` |

`S_total` (total correlation) is reported alongside everywhere, because the difference
between the two is the whole point: ordinary correlation is cheap, whole-only share is not.

## 2. The device, the qubits, and the frozen calibration

Backend **ibm_marrakesh** (Heron, 156 qubits). The qubit triple is pinned by a rule fixed
before it was evaluated (`cmd_freeze`): over all paths a–c–b with c adjacent to both,
keep those with readout error ≤ 0.015 on all three, cz error ≤ 0.004 on both edges,
T1 ∈ [120, 400] µs and T2 ≥ 30 µs on all three; among survivors minimise
Σ readout + 10 · Σ cz error; tie-break on max min(T2).

**Selected: physical qubits 13 – 14 – 15**, slots (a, b, c) = (13, 15, **14**), the check
bit c on the middle qubit so both CNOTs are nearest-neighbour.

Frozen calibration (`qpu_habit_freeze.json`, pulled 2026-07-26T01:48:31Z):

| slot | qubit | T1 (µs) | T2 (µs) | P(1\|0) | P(0\|1) |
|---|---|---|---|---|---|
| a | 13 | 219.1 | 197.9 | 0.00049 | 0.00977 |
| b | 15 | 280.5 | 40.5 | 0.00098 | 0.01025 |
| c | 14 | 355.6 | 122.3 | 0.00146 | 0.00684 |

cz error 13–14 = 0.00141, 14–15 = 0.00138.

**Calibration drift is real and is why the primary anchor is measured in-job.** Two pulls
fifteen minutes apart gave T1(15) = 318.8 then 280.5 µs, T2(15) = 33.7 then 40.5 µs — a
12 % and 20 % move with no intervention. The primary prediction below is therefore
anchored on T1 values measured **in the same job, on the same qubits, in an independent
arm**; the frozen published numbers above are the pre-registered secondary.

## 3. Convergent art — what is already known, and what is ours

Assume convergence (`convergent-art-pattern`); credit first, claim narrowly.

- **GHZ decoherence and its measurement** is a mature field: Monz et al., PRL 106, 130506
  (2011) measured N-qubit GHZ coherence decay and its super-decoherence scaling in trapped
  ions; the coherence-vs-populations method (parity oscillations) is Sackett et al., Nature
  404, 256 (2000) and Leibfried et al. All of Job A's quantum arm is a **re-reading of that
  known physics in share units**. We claim nothing new about the physics.
- **Amplitude damping / T1 relaxation as an asymmetric classical bit-flip channel** is
  textbook (Nielsen–Chuang §8.3). The moment-contraction algebra used for the prediction is
  standard.
- **Reset/ancilla-based repair and repetition-code demonstrations** on superconducting
  hardware are IBM's own well-trodden ground (Ristè et al., Córcoles et al. 2015, and the
  whole repetition-code QEC line). Our repair circuits are trivial members of that family.
- **Landauer/Szilard accounting** of an erasure as the price of created order is textbook,
  and `Core/Creation.lean` says so in its header.

**What is ours, narrowly:** (i) the share-unit instrument and the fact that these states'
readings are machine-checked constants; (ii) the theorem linkage — a Lean theorem executed
as a circuit, with its predicted value fixed by a proof committed before the data;
(iii) the wrong-code arm as a *control on minting*; (iv) the parameter-free rent-shape
test of leg 3, tying a 3-body decay rate to independently measured 1-body rates; (v) the
method (a hardware run whose thresholds are theorems and simulator-derived bands, both
committed first).

## 4. JOB A — the two-sector decay ordering, and the rent-shape kill

One job. All delays are dt-aligned (multiples of 64 ns). Readout calibration circuits
(|000⟩, |111⟩) ride along; every arm is reported RAW and readout-CORRECTED.

### The two habits, born equal

Both preparations carry **exactly one bit of whole-only share at t = 0**, and the SAME
instrument reads both:

- **QUANTUM-SPATIAL (arm A2/A3).** GHZ = (|000⟩+|111⟩)/√2, read in the X basis. Its
  X-basis outcome distribution is exactly the parity state ⇒ share = ln 2. (Read in Z it
  is ferro ⇒ share 0. The quantum habit is a parity habit *written in a basis you must
  know to read*.)
- **CLASSICAL-TEMPORAL (arm A1).** The same three qubits collapsed by mid-circuit
  measurement (the validated technique from `BELL_PREREG.md` addendum 1) into the classical
  parity mixture, read in Z ⇒ share = ln 2. (Read in X it is uniform ⇒ share 0.)

The 2 × 2 table (prep × basis) is thus (ln 2, 0; 0, ln 2) at t = 0, and the two zero cells
are genuine null controls of the instrument.

### The arms

| arm | prep | basis | delays (µs) | shots | what it is |
|---|---|---|---|---|---|
| A1 | classical parity mixture | ZZZ | 0, 18.0, 46.0, 79.6, 117.2, 158.5, 202.8, 249.6, 298.9 | 8192 | **the kill leg** |
| A2 | GHZ | XXX | 0, 9.8, 25.0, 43.3, 63.8, 86.2 | 4096 | quantum habit |
| A3 | GHZ | YXX | same | 4096 | phase tracking (ZZ-crosstalk-safe magnitude) |
| A4 | GHZ | ZZZ | 0, 79.6, 202.8 | 4096 | ferro habit; channel cross-check |
| A5 | classical | XXX | 0, 79.6, 202.8 | 4096 | **null control** (predicted 0 at all t) |
| A6 | independent bits | ZZZ | 0, 202.8 | 4096 | **null control** (predicted 0 at all t) |
| A7 | \|111⟩ | ZZZ | 0, 85.5, 199.6, 342.1, 513.2 | 4096 | **in-job T1 audit**; also a null control |
| A8 | \|000⟩, \|111⟩ | ZZZ | 0 | 8192 | readout calibration |

A4 is **not** a null: the gate showed that damping a sign-symmetric habit MINTS whole-only
share (the surviving |000⟩ against the decaying |111⟩ is a mixture of products, which
generically carries some). Its exact predicted curve is staked instead, as a second test
of the same channel on a different initial state. Catching this before hardware is what
the gate is for.

### The physics being predicted (leg 3), with zero free parameters

Under idle, each qubit undergoes amplitude damping: in the Heisenberg picture
`Z_q → e^(−t/T1_q) Z_q + (1 − e^(−t/T1_q)) m_q`, independently. The classical parity
mixture has all 1- and 2-body Z-moments zero and ⟨Z₁Z₂Z₃⟩ = 1, and independent channels
preserve that structure exactly, so at every t the state is

  **p_t = (product of its own 1-marginals) + (D(t)/8)·(−1)^(x₁+x₂+x₃)**,
  **D(t) = exp(−t · Σ_q 1/T1_q)**,

and the whole-only share is an exact function of D and the three marginals — no free
parameter anywhere. Two consequences are staked:

1. **Shape.** The exact predicted share curve (asymptotically ∝ D² ⇒ exponential with
   rate 2·Σ_q 1/T1_q; the transient is computed exactly, not approximated).
2. **Rate.** The 3-body decay rate is exactly **twice the sum of the three independently
   measured 1-body relaxation rates**. The 1-body rates come from arm A7 — a different
   arm, a different observable, the same job. Readout error contracts D by a constant
   factor and therefore **cannot** move the rate.

Also staked and reported: the classical arm is immune to ZZ crosstalk (a diagonal state is
unmoved by ZZ), which is why the kill rides on it and not on the quantum arm.

### THE KILL (leg 3) — pre-registered, separable, parameter-free

**The coordinate the kill is stated in, and why.** The share is an exact, monotone
function of D given the marginals, and the marginals are separately measured; so a test on
D is a test on the share, expressed in the coordinate where the estimator is unbiased and
the one unavoidable nuisance is exactly one number. That nuisance is `c₀` in
`D(t) = c₀ · exp(−Γ₁ t)`: a **time-independent** contraction absorbing state-preparation
infidelity and any residual readout mis-correction. **`c₀` cannot absorb a wrong rate or a
wrong shape** — which is exactly what is under test. Stating the kill on the absolute
share instead would fire on preparation fidelity, which the noisy model does not claim to
know, and that would be run 1's authoring error in new clothes.

Let `rate_D` be the weighted log-linear fit of |D̂(t)| over the nine points (intercept and
slope both free), and `Γ₁ = Σ_q 1/T̂1_q` from the A7 fit.

- **K-RATE (primary):** `R_D := rate_D / Γ₁` must lie in the simulation-derived band of
  §6. **Outside ⇒ the rent-clause hardware reading FAILS on rate.**
- **K-SHAPE (primary):** χ² of log|D̂(t)| against the model with slope **fixed** at −Γ₁ and
  intercept fitted (dof 8) must not exceed the simulation-derived 99th percentile of §6.
  **Exceeding it ⇒ FAILS on shape.**
- **K-FAMILY (secondary, the discriminator the array campaign used):** a power law
  `|D| ∝ (1 + t/τ)^(−α)` must NOT beat the exponential by ΔAIC > 10. If it does, the decay
  is reported as non-exponential and the rent-clause shape reading fails, whatever the rate
  does. (D is predicted to be a *pure* exponential with no transient, so the family
  comparison is well posed on D and would not be on the share.)
- **VOID conditions** (no claim in either direction, reported loudly, re-registered):
  readout assignment fidelity < 0.95; ANY of the ten null-control readings (A5×3, A6×2,
  A7×5) exceeding 1.5 × 10⁻³ nat (the pipeline manufactures share); the A7 T1 fit failing
  to converge or returning T1 outside [50, 800] µs.

A failure here kills **only** the hardware reading of the rent clause's shape. It does not
touch `rent_holds` / `unpaid_decays` (theorems about a model, and true regardless), and it
does not touch the mint theorems of Job B. That is the separability requirement.

### The two-sector ordering (demonstration, not a test)

From the frozen calibration the predicted share-decay rates are
2·Σ1/T1 = 0.02188 /µs (classical, half-life 31.7 µs) and 2·Σ1/T2 = 0.07587 /µs
(quantum, half-life 9.1 µs) — the quantum habit is predicted to die **3.47× faster**.
This is a *consequence of the device's own calibration*, not a law: on a device with
T_φ ≫ T1 the ordering would reverse, and we say so in advance. What is tested is that each
arm decays at the rate its own calibration predicts; the ordering is then read off. Any
report of "quantum in space dies first" is explicitly conditional on these qubits.

## 5. JOB B — mint, wrong code, and the price of rent in erased bits

One job, 13 circuits, on the same three qubits.

| arm | circuit | predicted share | predicted S_total | authority |
|---|---|---|---|---|
| MINT | H×3 → mid-circuit measure (uniform noise) → **reset c** → c := a⊕b | 0 → **ln 2** | 0 → **ln 2** | `repair_creates_parity`, `S_total_parityRepair` |
| COPY (wrong code) | same, but c := a | **0** | ln 2 | computed exactly (not machine-checked) |
| NONE (floor) | same, but no repair | 0 | 0 | false-positive floor |
| RENT | birth the parity habit, then n ∈ {1,2,4} cycles of [idle T/n, reset c, recompute c] | see §6 | | `parityRepair_idempotent` |
| DEFAULT | same birth, then idle T, no repair (n = 0) | leg-3 curve at T | | `unpaid_decays` |

with T ∈ {79.6, 158.5} µs.

**The single circuit that is the theorem.** The MINT circuit's mid-circuit measurement
record IS the input state (uniform noise, share 0) and its final record IS the output
(parity, share ln 2) — the same shots, both sides of `repair_mints_from_noise`, plus a
per-shot check that c = a ⊕ b on every shot.

**The rent is countable and it is physical.** The repair's third-slot `reset` is a physical
erasure of one bit into the fridge — exactly the ledger entry
`parityRepair_pays_one_bit` (entropy(indep) − entropy(pushforward) = ln 2) charges. The
deliverable is the table **share retained vs. bits erased**: n resets bought how much share.

**A prediction that is pre-registered because it might be embarrassing.** The parity code's
repair reads only a and b and rewrites c; it restores the *relation*, never the *values*.
So the share held at the end is set by the LAST payment, and the earlier ones buy nothing
except accumulated gate noise. We therefore predict **share flat-to-decreasing in n at
fixed T** — i.e. that paying 4× is waste. This is the hardware face of
`parityRepair_idempotent`. If instead share *increases* with n, our reading of the code is
wrong and we say so.

## 6. Every band, from the noisy model

Source: `qpu_habit_bands.json` (400 replicates of the full pipeline: exact channel →
readout channel → multinomial shots → simulated readout calibration → readout correction →
exact share solver), `qpu_habit_bands2.json` (the same, jointly with a simulated A7 audit
so the anchor's own error is inside the band), `qpu_habit_bands3.json` (the shape and
family statistics), `qpu_habit_gate.json` (calibration-matched Aer for the gate-bearing
Job B arms, 25 repetitions).

### 6.1 The kill (arm A1)

| statistic | model expectation | **STAKED band** |
|---|---|---|
| `R_D = rate_D / Γ₁` | 0.9961 ± 0.0205 (99 % joint MC [0.9412, 1.0516]) | **[0.847, 1.157]** |
| χ² of log\|D̂\|, slope fixed at −Γ₁, dof 8 | mean 9.98 | **≤ 26.59** (MC p99; p999 = 36.0) |
| ΔAIC(exponential − power law) on \|D̂\| | −2.55 (p99 +1.28, max +4.33) | **must not exceed +10** |

The K-RATE band is the 99 % joint Monte-Carlo interval **widened by ±10 %** as a stated
systematic allowance for T1 drift *within* the job (between the A7 arm and the A1 arm) and
for non-exponential relaxation — both real, both unmodelled. The raw statistical interval
is quoted alongside in the results, so the reader can see how much of the band is
allowance. The in-job anchor itself is good to 1.67 % (§6.2), which is why the allowance
dominates it.

### 6.2 The anchor (arm A7) and the null controls

- T1 recovery from 5 delays × 4096 shots: q13 219.1 → 219.1 ± 5.3 µs (2.4 %),
  q15 280.5 → 279.9 ± 7.7 µs (2.7 %), q14 355.6 → 356.9 ± 12.4 µs (3.5 %).
  **Γ₁ = Σ1/T1 recovered to 1.67 %**, 0 fit failures in 400. The audit can do its job.
- Null-control floor at 4096 shots: mean 1.1 × 10⁻⁴, p99 7.7 × 10⁻⁴, p999 9.5 × 10⁻⁴;
  at 8192 shots mean 6.0 × 10⁻⁵. **VOID threshold staked at 1.5 × 10⁻³** per reading
  (above p999, keeping the family-wise false-VOID rate over ten readings near 1 %).

### 6.3 Arm A1 per-point predictions (frozen calibration; recomputed at the in-job anchor)

| t (µs) | 0 | 18.0 | 46.0 | 79.6 | 117.2 | 158.5 | 202.8 | 249.6 | 298.9 |
|---|---|---|---|---|---|---|---|---|---|
| share, model | .6830 | .4116 | .2301 | .1260 | .0674 | .0366 | .0191 | .0100 | .0051 |
| ± sd | .0065 | .0075 | .0064 | .0045 | .0035 | .0026 | .0020 | .0014 | .0010 |
| SNR over floor | 105 | 55 | 36 | 28 | 20 | 14 | 9.8 | 7.4 | 5.2 |
| D | 1.000 | .821 | .604 | .419 | .277 | .177 | .109 | .065 | .038 |

Every point clears SNR 5; all nine enter the fit. (Ideal share at t = 0 is ln 2 = 0.6931;
the model reads 0.6830 because readout correction at finite shots is not free. Comparing
hardware to 0.6931 rather than to 0.6830 would be the run-1 error.)

### 6.4 Arm A2/A3 (quantum) and A4 (ferro)

- Quantum share, model: 0.6809, 0.2624, 0.0771, 0.0187, 0.0040, 0.0008 at
  t = 0, 9.8, 25.0, 43.3, 63.8, 86.2 µs; last two are below SNR 5 and are excluded from the
  fit by the pre-registered SNR ≥ 5 rule. `R_share` for this arm bands at
  1.1719 ± 0.0302 — **note it is not 1**, because the fit range includes the ln 2 plateau;
  this is reported, not staked as a kill.
- A4 ferro read in Z, model share: 0.0000 → 0.0530 → 0.0167 at t = 0, 79.6, 202.8 µs, with
  S_total 1.386 → 0.485 → 0.133. **Damping mints whole-only share out of a
  sign-symmetric habit.** Reported as a channel cross-check on a different initial state.

### 6.5 Job B (calibration-matched Aer, 25 repetitions; bands are mean ± 3 sd)

| arm | share (corrected) | **band** | S_total |
|---|---|---|---|
| MINT parity | 0.6766 ± 0.0074 | [0.654, 0.699] | 0.6768 |
| COPY (wrong code) | 0.00010 ± 0.00021 | ≤ 0.0010 | 0.6767 |
| NONE (floor) | 0.00008 ± 0.00013 | ≤ 0.0010 | 0.0003 |
| RENT T=79.6, n=1 / 2 / 4 | 0.6038 / 0.6060 / 0.6075 (± ~0.009) | [0.575, 0.635] | 0.677 |
| DEFAULT T=79.6, n=0 | 0.1242 ± 0.0044 | [0.111, 0.138] | 0.124 |
| RENT T=158.5, n=1 / 2 / 4 | 0.4583 / 0.4568 / 0.4590 (± ~0.010) | [0.427, 0.490] | 0.656 |
| DEFAULT T=158.5, n=0 | 0.0363 ± 0.0023 | [0.029, 0.043] | 0.036 |

Predicted paid:unpaid ratio **4.9× at T = 79.6 µs and 12.6× at T = 158.5 µs**.
The n-dependence of the paid arm is **flat within ±0.01** in the noisy model — the
pre-registered "paying more buys nothing" prediction, made sharp: |share(n=4) −
share(n=1)| ≤ 0.03 at both T. Larger than that, in either direction, contradicts our
reading of the code and is reported as such.

## 7. Meaning of every outcome, fixed in advance

- **K-RATE and K-SHAPE both pass, controls clean:** the rent clause's decay shape has a
  physical reading on a real substrate — geometric decay at the rate the substrate's own
  independently measured relaxation fixes, with no free parameter. Stated at exactly that
  strength: a *hardware reading of the model's shape*, on an engineered memoryless channel,
  not evidence about nature's wild processes, and not a promotion of anything to `measured`
  without Eric's review and a refuter pass.
- **Either fails:** the rent-clause hardware reading FAILS. Reported in the results file's
  first paragraph, in the same size type as a survival, and carried into the record marked
  dead. The Lean theorems are untouched; what dies is the claim that the model's shape is
  the shape a real decaying habit takes.
- **Mint arm ≠ ln 2 beyond its band:** the theorem is not falsified (it is a theorem); the
  *device's* ability to execute it is, and the gap is reported as an instrument result.
- **Controls fire:** VOID; no claim in any direction.
- **Any arm below its sensitivity floor:** claimed as nothing, per run-1's rule.

## 8. Budget

400 s remain of the 600 s free allocation (200 s already spent: 66 s run 1, 134 s Bell).
Estimated: **Job A ≈ 68 s, Job B ≈ 35 s, total ≈ 103 s**, from a model calibrated on the
Bell run (488 × 1024 shots = 134 s ⇒ 252 µs/shot repetition overhead + circuit duration).
Reserve after both jobs ≈ 297 s, well above the 60 s floor. Actual consumed seconds are
reported per job. No adaptive re-runs; any further job requires a new addendum.

## 9. Discipline checklist (`epistemology.md`)

1. Pre-registered: this file, committed before submission. ✓
2. Kills staked first and separable: §4, one kill, its own claim only. ✓
3. Null matched to the generative structure: the null for every share reading is the
   matched INDEPENDENT surrogate at the same shot count (product of the measured
   marginals), not an iid/Gaussian null. ✓ (`whole-only-null-autocorrelation`)
4. Tied fraction: not applicable — no rank statistic is used anywhere.
5. Estimator bias controlled by the matched surrogate floor, subtracted before every fit,
   with its own simulation-derived spread. ✓
6. No residual is support: the only support claimed is from the advance prediction of §4,
   confirmed or not. ✓
7. The fired kill is reported as plainly as the survival, and kept in the record. ✓

---

# Addendum 1 (2026-07-26) — run 1 VOIDed; what changes, and what does not

Written after job A run 1 (`d9immeqbr2fc73e4u02g`, 72 QPU s) and BEFORE any run-2
submission. Run 1's data is kept in the record, marked VOID, and reported in the results
file as plainly as a survival would be.

## A1. The VOID, by the pre-registered letter

**Readout assignment fidelity = 0.9047, below the staked floor of 0.95 ⇒ VOID.**
No claim in any direction is made from run 1. For the record, and *not* as a claim: the
kill statistic landed at R_D = 1.149 (inside the staked band [0.847, 1.157]) while the
shape χ² landed at 109 against a staked ceiling of 26.6 — i.e. run 1 would have failed
K-SHAPE. It is void, so it fails nothing.

## A2. Two defects, both found, both fixed

**(a) An analysis bug of ours.** `counts_to_p` returned a (2,2,2) array whose axis order
was the *reverse* of the slot order used to build the readout assignment matrices, so each
qubit's correction was applied to the wrong slot, and the per-qubit T1 labels were
permuted. Fixed; regression-tested by pushing a state through a deliberately lopsided
readout channel (P(0|1) = 0.10, 0.002, 0.03) and recovering share = 0.693147181 and
D = 1.000000000 exactly. The kill statistics are nearly immune to this bug (D's leading
correction is a *product* of the three factors, so permuting them does not change it) —
which is why it was caught by inspection of the raw counts rather than by a wrong answer.
Reported anyway: an undetected-by-luck bug is still a bug.

**(b) The published calibration is not something to select on.** A screening job
(`qpu_habit_screen.py`, 3 circuits, 3.7 QPU s, job `d9imr2rjf64c739fp9rg`) measured
readout and a one-point T1 on 24 candidate qubits:

| qubit | P(0\|1) published | P(0\|1) **measured** | T1 published | T1 **measured** |
|---|---|---|---|---|
| 13 | 0.0098 | **0.1267** | 219 µs | 174 µs |
| 15 | 0.0103 | **0.0251** | 281 µs | 142 µs |
| 14 | 0.0068 | 0.0063 | 356 µs | 277 µs |

Thirteen-fold on the qubit that VOIDed the run. This is the whole explanation of run 1,
and it is a lesson with a name: **on this device, published calibration selects badly;
measure, then select.**

## A3. What changes for run 2

1. **New triple, chosen on measured readout.** Rule, fixed before the screen was read:
   among screened candidate triples take the one minimising the worst measured readout
   error, requiring that worst ≤ 0.015 and all three screened T1 ∈ [60, 500] µs.
   **Selected: qubits 6 – 7 – 8**, slots (a, b, c) = (6, 8, **7**). Measured
   P(1|0) = 0.0010 / 0.0024 / 0.0000 and P(0|1) = 0.0039 / 0.0083 / 0.0076 — the worst is
   0.0083, fifteen times better than run 1's worst. Screened T1 = 280 / 100 / 259 µs;
   published T2 = 160.6 / 65.3 / 89.6 µs (no in-job T2 audit — the quantum arm is a
   demonstration, and says so).
2. **Delay grid from the measured Γ₁, with margin.** Run 1's grid was built on published
   T1s that proved 63 % optimistic, so three of nine points landed below the sensitivity
   the pre-registered SNR ≥ 5 rule requires, and the rule (correctly) discarded them after
   the fact. Run 2's grid is built at a rate 15 % *faster* than the screen implies (the
   screen's one-point T1 ignores the excited-state floor and therefore overstates T1).
   Ten points, 0 to 128.4 µs; the noisy model puts every one of them at SNR ≥ 9.2.
3. **Readout calibration at BOTH ends of the job, and the anchor interleaved with the kill
   arm.** Run 1 took its single calibration last, and it disagreed with an identical
   circuit taken first by 7 points on one qubit. Run 2 measures |000⟩ and |111⟩ before the
   first arm and after the last, uses the average, and reports the difference as a drift
   diagnostic. A1 (kill) and A7 (anchor) circuits alternate, so the two see the same
   device state.
4. **Bands re-derived at the new triple** (§A4). Nothing about their *form* changes.

**What does NOT change:** the instrument, the circuits, the theorems, the arm structure,
the kill's form (K-RATE / K-SHAPE / K-FAMILY on D), the ±10 % systematic allowance, the
VOID rules, the null-control threshold of 1.5 × 10⁻³, and the meaning of every outcome.
No criterion is loosened. K-SHAPE's ceiling moves only because the number of fit points
moves (dof 9 rather than 8), and it is re-derived by the same Monte Carlo.

## A4. Run-2 bands (`qpu_habit_bands*_v2.json`, 300 replicates; gate re-passed on the new triple)

| statistic | model expectation | **STAKED** |
|---|---|---|
| `R_D = rate_D / Γ₁` | 1.0016 ± 0.0162 (99 % joint [0.9600, 1.0489]) | **[0.864, 1.154]** |
| χ² of log\|D̂\|, slope fixed at −Γ₁, dof 9 | mean 10.08 | **≤ 26.46** (p999 = 33.3) |
| ΔAIC(exp − power law) on \|D̂\| | −2.25 (p99 +3.64, max +7.79) | **must not exceed +10** |
| Γ₁ recovered by the A7 audit | 0.017449 → 0.017395 ± 0.000203 | **1.16 %**, 0/300 fit failures |
| null controls | mean 1.3 × 10⁻⁴, p999 1.2 × 10⁻³ | **≤ 1.5 × 10⁻³** each |

Arm A1 model share at t = 0, 7.4, 18.2, 30.8, 44.7, 59.8, 75.8, 92.7, 110.2, 128.4 µs:
0.6865, 0.4805, 0.3245, 0.2166, 0.1435, 0.0955, 0.0630, 0.0413, 0.0270, 0.0173
(± 0.0055 … 0.0019); SNR 125 down to 9.2.

Quantum arm model share: 0.6834, 0.3337, 0.1435, 0.0561, 0.0206, 0.0070 at
t = 0, 8.1, 19.9, 33.7, 49.1, 65.6 µs; the last is below SNR 5 and the rule drops it.
Predicted rates: classical 2Σ1/T1 = 0.03490 /µs (half-life 19.9 µs), quantum
2Σ1/T2 = 0.06541 /µs (10.6 µs) — **the quantum habit predicted to die 1.87× faster** on
these qubits. Weaker separation than run 1's triple, and stated in advance.

Job B bands (calibration-matched Aer, 25 repetitions, mean ± 3 sd):
MINT 0.6791 ± 0.0086 → [0.653, 0.705]; COPY 0.00013 ≤ 0.001; NONE 0.00010 ≤ 0.001;
RENT T = 44.7 µs n = 1/2/4: 0.6079 / 0.6077 / 0.6035 vs DEFAULT 0.1447 (**4.2×**);
RENT T = 92.7 µs: 0.4629 / 0.4621 / 0.4660 vs DEFAULT 0.0408 (**11.4×**).
Paid-arm spread over n stays within ±0.01 in the model; staked at ≤ 0.03.

## A5. Budget

600 s allocation. Spent: 66 (phase-3 run 1) + 134 (Bell) + 72 (job A run 1, VOID)
+ 3.7 (screen) = 275.7 s. Remaining 324.3 s. Run 2 estimated: job A 71.2 s, job B 31.8 s
= 103 s, leaving ≈ 221 s — above the 60 s reserve floor with room for one more VOID.

---

# Addendum 2 (2026-07-26) — the sector-flow dichotomy

Directive received: *"make sure we test the unique prediction, everything else is just
validation."* Correct, and this addendum re-points the campaign at it. But two of the three
briefed primary premises are **contradicted by our own theorem's scope and by data already
in hand**, and are refuted here BEFORE any budget is spent on them. Written before the
run-3 submission; screen job (6 s) already run.

## B1. Refutation 1 — single-site noise CAN create whole-only share

The brief states: "under IDLE, starting from a share-zero state (e.g. the ferro mixture …)
the measured share must stay at its floor … BY THEOREM."

**It must not.** `Core/Creation.lean`'s `percell_no_creation` is general in the input state
but is a statement about **deterministic** per-cell maps, and its proof runs on the
dichotomy *every `Bool → Bool` is a bijection or a constant*. Single-site **noise** is a
stochastic mixture of such maps, and the bound does not survive mixing: the share is a
max-entropy divergence, not a linear or concave functional.

Elementary counterexample: the ferro mixture ½(000) + ½(111) under symmetric single-site
damping with γ = 0.1 has share **0.0547 nat**. (By hand: the damped state depends only on
the Hamming weight, with ln p = −0.575, −2.773, −2.773, −2.773 at k = 0,1,2,3 — not a
quadratic in k, hence not pairwise-representable, hence share > 0.)

**And we already measured it.** Run 2's A4 arm was exactly this experiment: ferro read in
Z, idling, share **0.0000 → 0.0487 → 0.0264** at t = 0, 44.7, 110.2 µs against a
parameter-free prediction of 0.0000 → 0.0452 → 0.0186. Run as briefed, P1 would have
fired its outcome (iii) — "the KILL on the no-creation reading" — against our own theorem,
on a premise that mis-states the theorem's scope. Run 1 already cost 72 s to a mis-staked
criterion; this would have cost ~100 s more.

**What survives, and it is the good half of the brief:** the background-free claim is true
for a **product** state, where independence is exactly preserved by any product channel, so
the entire single-qubit error budget provably cannot move the reading off zero. That arm is
kept and is a genuine background-free witness.

## B2. Refutation 2 — the cascade runs UP, not down

The brief predicts the parity habit sheds order downward into a transient pairwise bulge.
**Under any independent single-site channel the pair covariance transforms exactly
multiplicatively**, cov_ij → κ_i κ_j cov_ij (verified to 1.1 × 10⁻¹⁶ over 600 random
state/channel checks). For binary variables zero covariance *is* independence, and the
parity state starts at cov = 0, so **every pair stays exactly independent at every delay**
— pair MI at machine epsilon (10⁻¹⁶–10⁻¹⁷) from t = 0 to t = 800 µs. There is no bulge and
no downward cascade; there provably cannot be one.

The real phenomenon is the mirror image, and it is more interesting: the **ferro** state
(all order-2, zero order-3) develops a transient **whole-only** bulge — 0 → peak 0.047 nat
at ≈ 37 µs → decay — while its pair covariances fall monotonically. **Order flows up, 2 → 3,
never down.** Note this separates the share from the third cumulant: ferro's third cumulant
is zero and stays exactly zero (multiplicative law), while its share rises from zero. The
share is not a cumulant, and single-site noise is what shows the difference.

## B3. What run 3 tests: the SECTOR-FLOW DICHOTOMY (the unique composite)

One job, four idle-and-read arms on classical preparations differing only in **which order
sector holds the pattern**, plus the audit:

| arm | prep | read | sector at t=0 | prediction |
|---|---|---|---|---|
| **C1** | ferro (collapsed, order-2 only) | Z | pair 1.0, share 0 | share **rises** 0 → 0.047 → falls; pair cov decays multiplicatively |
| **C3** | parity mixture (order-3 only) | Z | pair 0, share ln 2 | share decays; **pair MI stays exactly 0** |
| **C4** | independent bits | Z | nothing | **stays at the floor forever** (background-free) |
| **C5** | \|+++⟩ | X | nothing (product in X) | **stays at the floor** unless two-site coupling acts |
| **C2** | \|111⟩, **same delay grid as C1** | Z | — | measures κ_q(t) directly |

**One-way valve, stated as the claim:** single-site noise cannot create whole-only share
from nothing, can convert pairwise pattern into it, and can never convert whole-only
pattern back down. Three arms, three directions, one composite.

**The prediction assumes no functional form at all.** The audit arm C2 rides C1's exact
delay grid, so κ_q(t) = (P₁(t) − p_exc)/(1 − p_exc) is measured **at every point**, and the
predicted ferro curve is built from those measured numbers through the exact channel and
the exact k = 3 solver. Zero free parameters and zero model — which matters, because run 2
showed this substrate is not a single exponential (β ≈ 0.88–0.93), so any exponential-based
prediction would be staking a criterion the device cannot meet. This is run 2's named next
step 1, executed.

**The crosstalk witness, corrected.** The brief proposes predicting a ZZ-driven minting
rate. A *classical* (diagonal) probe is **blind to ZZ by construction** — ZZ is diagonal in
the computational basis and cannot move a diagonal state — so C4 bounds correlated
*relaxation*, not ZZ. The coherent arm C5 is the genuine background-free ZZ witness:
\|+++⟩ is a product state in the X basis, every single-site channel (T1, T2 *and* readout)
contracts X-moments independently and so keeps the X distribution exactly product, while
two-site coupling does not. Its share is therefore zero under the entire single-site error
budget by theorem, and any excess is correlated noise. We do not stake a predicted ZZ rate
(published per-pair ZZ is not in this backend's properties); C5's deliverable is a **bound**.

## B4. Convergent art

ZZ-crosstalk characterization is a standard, mature field (Sheldon et al. PRA 93, 060302
(2016); Ku et al. PRL 125, 200504 (2020); IBM's own simultaneous-RB and ZZ-free gate work).
We claim no new crosstalk measurement. What is ours is the framing: a witness whose
insensitivity to the single-site error budget is a **theorem about the statistic** rather
than a calibration achievement. Likewise the up-only sector flow is elementary for anyone
who computes it; we have found it stated nowhere as an observable, and we state it as one.

## B5. Bands (`qpu_sector_bands.json`, 250 replicates; ideal gate re-passed on all four preps)

| statistic | model | **STAKED** |
|---|---|---|
| **K-CURVE** χ² of C1's 12 shares vs the κ-built curve, dof 12, zero free params | mean 12.22 | **≤ 32.21** (p99; p999 44.9) |
| **K-PEAK-t** bulge peak location | mode 37.5 µs | **∈ {20.6 … 65.6 µs}** (full MC support) |
| **K-PEAK-h** bulge peak height | 0.0491 ± 0.0029 | **∈ [0.0433, 0.0569]** |
| **K-PAIRMULT** cov_ij/(κ_iκ_j cov_ij(0)) on C1 | 1.0003 ± 0.0412 | **∈ [0.832, 1.176]**, and no pair covariance may exceed its own t = 0 value |
| **K-PAIRZERO** max pair MI on C3, any delay | 1.3 × 10⁻⁴ | **≤ 9.4 × 10⁻⁴** |
| **K-NULL-Z** C4 share, any delay | 5.9 × 10⁻⁵ | **≤ 5.4 × 10⁻⁴** |
| **K-NULL-X** C5 share, any delay | 1.4 × 10⁻⁴ | **≤ 1.7 × 10⁻³** (excess = correlated-noise reading) |

C1 model curve (share at t = 0, 6.4, 12.7, 20.6, 29.2, 37.5, 49.5, 65.6, 88.1, 120.0,
168.8, 243.8 µs): 0.0000, 0.0194, 0.0319, 0.0409, 0.0460, 0.0465, 0.0454, 0.0395, 0.0301,
0.0191, 0.0084, 0.0021 (± 0.0002 … 0.0038).

**Meaning of each outcome.** All pass ⇒ the sector-flow dichotomy holds on hardware, with a
model-free parameter-free curve; the one-way valve is a measured fact about single-site
noise, and the share is demonstrated to be a background-free witness. K-CURVE or K-PEAK
fails ⇒ the conversion prediction fails, reported as loudly as a survival. K-PAIRZERO fails
⇒ the exact multiplicative law is violated on hardware, which would mean the device's noise
is not single-site (a device finding) or our instrument leaks — either way, loud.
K-NULL fails ⇒ the background-free claim fails. VOID as before: readout fidelity < 0.95, or
calibration drift across the job > 0.02.

## B6. Budget and what the secondaries already cost

Consumed: 275.7 (through run 2's addendum) + 75 (A run 2) + 35 (B) + 6 (re-screen) = 388 s
of 600. **212 s remain**; run 3 is estimated at **95.4 s**, leaving ≈ 116 s — above the 60 s
reserve floor with room for one VOID.

The secondary/validation arms the directive de-prioritised are **already secured and paid
for**: the mint and wrong-code theorem execution and the ancilla rent ladder ran as job B
(35 s, reported), and the GHZ two-sector ordering ran inside job A run 2. No further
budget is requested for them.
