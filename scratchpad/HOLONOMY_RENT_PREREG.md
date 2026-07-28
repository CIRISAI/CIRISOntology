# Is the holonomy MAINTAINABLE? — pre-registration

**Date:** 2026-07-27. **Campaign:** maintained-holonomy.
**Written and committed BEFORE any maintained number is computed.**
**Instrument:** `scratchpad/holonomy_rent.py` (to be written after this file is committed).
**Raw:** `scratchpad/holonomy_rent_results.json`. **Results:** `HOLONOMY_RENT_RESULTS.md`.

---

## 0. What this campaign does NOT do

**F-11 stays fired, on its own terms.** The predecessor experiment
(`coherence-ratchet/experiments/open_system_pomega/assumption_audit/holonomic_pomega/`,
dated 2026-05-22) measured the *unmaintained* Wilson-loop holonomy of the framework's genuine
emergence-map connection around the TSVF forward–backward loop, and found it decoheres
geometrically: `hol_specrad(R) = 0.9655^(R−1)`, flowing to the zero operator, not to the
identity. **That verdict is correct as written and this campaign does not un-fire it.** Nothing
measured here can, because nothing measured here is the unmaintained loop.

What this campaign can establish is a **different claim**: whether that structure is
*maintainable* — whether a repair step applied per rung holds the loop open, and whether it does
so along the law this repository's rent clause states. A maintained holonomy that stays open is
not a refutation of an unmaintained holonomy that closes. Both can be true and, if the rent
clause is right about this object, both are.

**The reframe that licenses the re-test, and its whole warrant — stated with the one exception
the grep actually found.** The predecessor's *pre-registration* contains no maintenance, repair,
rent, upkeep or threshold term: grep over `PREREGISTRATION.md` for `repair`, `maintain`,
`maintenance`, `upkeep`, `threshold` returns nothing, and `rent` matches only inside the word
"different". It pre-registered the unpaid case only, because on 2026-05-22 the phase boundary did
not exist yet.

**But `RESULTS.md` is not silent, and the exception must be carried, not buried.** Its Limits
§(3) reads: *"The backward dephasing rate is `γM = GAMMA·M_BASE` — the framework's
active-management strength; a different maintenance rate shifts the per-rung eigenvalue but not
below 1 unless `γM = 0`, which is the unmaintained chaos limit the framework explicitly excludes.
The area law is `γM`-independent across the framework-faithful range."* So the predecessor **did**
consider one maintenance-shaped move, post hoc, and closed it: **varying the decay rate `γM` does
not rescue the area law**, and this campaign takes that as settled and does not re-run it.

**This campaign is a different move, and the distinction is load-bearing.** It does not vary
`γM`. The dephasing acts at the framework's full measured strength at every rung, exactly as the
predecessor built it; what is added is a **separate repair operation** that pays back part of
what the dephasing took. Reading (b) of §4.1 is precisely the difference: a fixed deposit is not
a smaller decay, and `S_{k+1} = (1−q)λS_k + qS_0` is not `S_{k+1} = λ'S_k` for any `λ'`. Credit
where it is due — the rate-variation route was already closed by the predecessor, and had this
campaign been about `γM` it would have been redundant before it started.

So `0.9655` per rung is read here not as an absence but as a well-characterised measurement of a
decay rate, `ε = 1 − 0.9655 = 0.0345` per rung, against which a *payment* — which the predecessor
never introduced — can now be priced. This repository has since proved the rent clause on the
model (`Core/Maintenance.lean`) and measured it on real substrates
(`scratchpad/MAINTENANCE_SWEEP_RESULTS.md`).

---

## 1. The received numbers, and the commitment to re-derive them

Per the received-numbers-are-not-measured gate, every number below that comes from the
predecessor is marked RECEIVED and is re-derived by this campaign's own `q = 0` arm before
anything is built on it.

| quantity | RECEIVED value | source |
|---|---|---|
| per-rung holonomy eigenvalue `λ` | 0.9655 | `RESULTS.md` headline; `results_holonomic.json` |
| per-rung decay `ε = 1 − λ` | 0.0345 | derived from the above |
| cross-rung coupling `c1` (g/J geomean) | 0.63552212827453 | `results_holonomic.json` `meta.c1_rg` |
| rung reference dimension `d` | 64 | `meta.d_rung` |
| seed | 20260522 | `meta.seed` |
| `‖W†W − I‖` | 1.1e−14 | `RESULTS.md` |
| `‖B − W†‖` | 5.05 | `RESULTS.md` |

**Two received-number discrepancies already found by reading the primary artifact, recorded
here before the run so they cannot be back-dated:**

1. **`c1`'s docstring value is wrong in the source.** `build_holonomic_pomega.py` line 174 states
   `# 0.6257` for `(0.31*0.72*1.15)**(1/3)`; the arithmetic gives 0.6355, and both `RESULTS.md`
   and `results_holonomic.json` carry 0.6355. The *computed* value is correct everywhere; only
   the inline comment is wrong. No result depends on the comment. Recorded, not corrected (the
   file is read-only to this campaign).
2. **"constant to four decimals" overstates the predecessor's own table.** `RESULTS.md`'s
   per-rung eigenvalue row reads 0.9656, 0.9656, 0.9655, 0.9653, 0.9654, 0.9653, 0.9651 across
   R = 3…50 — that is constant to *three* decimals with a slow monotone drift downward, not four.
   The area law is therefore approximate, not exact. This does not change the verdict (the
   holonomy still decoheres geometrically) and is recorded as a wording correction. This
   campaign will quote λ with its measured spread across R rather than as a single constant.

**Binding:** if the `q = 0` re-derivation disagrees with the received `λ` by more than 1e−3
absolute, every instantiated number in §4 is void and is recomputed from the re-derived λ before
any maintained cell is read. The predictions in §4 are stated symbolically in λ first, and
instantiated at the RECEIVED λ second, precisely so this substitution is mechanical.

---

## 2. What is being maintained, and what the repair is

### 2.1 The ledger entry

The decaying quantity is the **loop's transport gain**: the size of the holonomy operator, which
the predecessor measured as `hol_specrad` (largest |eigenvalue|) and `hol_zero_dist` (rms
singular value, `‖Hol‖_F/√d`). Both are reported. **The primary reading is `hol_zero_dist`**,
because it is a singular-value quantity and therefore backward-stable, where the spectral radius
of a strongly non-normal product is not; `hol_specrad` is reported alongside for direct
comparability with the predecessor's published law. If the two give per-rung rates differing by
more than 1% at `q = 0`, the spectral-radius reading is declared instrument-limited and the
campaign reports on the singular-value reading only, flagging the predecessor's law as such.

### 2.2 The design state — declared, and intrinsic

The structure being maintained is the connection's **isometry**. This is not a target chosen by
this campaign: it is the framework's own stated property of `W_n`
(`construct_p_omega_mera.py`: "W0, W1 are isometries, W†W = I"), and the predecessor verified it
to 1.1e−14 *specifically so that a null could not be manufactured by modelling W as a generic
contraction*. The forward leg already sits at design. The backward leg does not:
`B = Deph · CG†` with `Deph` Hermitian positive-definite, so `B`'s polar decomposition is
`B = P·U` with `P = Deph` and `U = CG†`. **The design backward step is therefore `CG†`, the
polar unitary factor of the framework's own genuine backward generator** — read off `B`, not
chosen.

The **design holonomy** is the loop with both legs at their isometric parts:

```
Hol_des(R) = (CG†)^(R−1) · W^(R−1)          — unitary, gain exactly 1 at every R
```

**Scope warning, stated before the run because it will otherwise be misread.** `Hol_des` is
also the `γM = 0` loop, which the predecessor's Limits §(3) calls "the unmaintained chaos limit
the framework explicitly excludes". Two things follow and both are binding:

- **At `q = 1` this campaign's maintained loop is exactly `Hol_des` by construction.** The `q = 1`
  endpoint is therefore *not independent evidence of anything*: it is the excluded limit,
  reached by definition. It is reported as a calibration endpoint and no claim rests on it.
- The interior `0 < q < 1` is **not** the same as reducing `γM`. The dephasing still acts at the
  framework's full measured strength at every rung; a separate repair operation pays back part
  of what it took. That is the rent clause's actual structure — decay and payment both act —
  and it is the only regime in which this campaign has content.

### 2.3 The repair maps — declared in full, not hand-tuned

Two repair forms, both affine deposits with the same `q` semantics as the maintenance sweep
("with weight `q`, deposit the decoded design; otherwise leave it"), so that `q` here is the
*same parameter* as `q` there and the sweep's closed form can be staked quantitatively.

**R-POL — the structure-blind repair (PRIMARY ARM).**

```
Rep_q^POL(A) = (1 − q)·A + q·polar(A),      polar(A) = A(A†A)^(−1/2)
```

It reads the current operator and returns it moved toward the nearest isometry. It knows the
*constraint* (be norm-preserving) but **not the design** — it does not know where the loop was
supposed to point. This is the honest analogue of a decoder that reads the state and projects it
onto its code.

**R-DES — the decoder repair (CALIBRATION ARM).**

```
Rep_q^DES(A; k) = (1 − q)·A + q·D_k,        D_k = (CG†)^k
```

It deposits the actual design operator at that depth. This is the literal analogue of the
maintenance sweep's decoder and of `Core/Creation.lean`'s `parityRepair` — a map that knows the
code and writes it back.

**Both maps satisfy the property `Core/Creation.lean` insists on and checks rather than
assumes** (`parityRepair_fixed_iff`: "it changes nothing already well maintained and nothing
else is left alone"). For R-POL the fixed-point set is exactly the isometries: `(1−q)A + q·polar(A) = A`
iff `polar(A) = A` iff every singular value is 1, for every `q ∈ (0,1]`. For R-DES the fixed
point at depth `k` is exactly `D_k`. **Both are verified numerically as gate C-NOOP below.**

**Placement in the loop.** Repair acts after every transport step on both legs:

```
H_0 = I ;   H_{k+1} = Rep_q(B · H_k)  for k = 0 … R−2 ;   Hol_q(R) = H_{R−1} · Rep-maintained W-leg
```

On the forward leg the accumulated operator `W^k` is unitary, so both repairs are exactly the
identity there — asserted here, verified as C-NOOP, not assumed.

**What is forbidden, named in advance.** Any repair that restores the norm by a scalar multiple
is the self-sealing move the predecessor's own pre-registration prohibits ("if the construction
finds itself choosing the connection to manufacture a corridor holonomy, it STOPS"). It is not
merely avoided here; it is **run explicitly as control C-NORM** so the genuine arms can be read
against a manufactured plateau.

**Search cap, declared.** Exactly **two** repair forms (R-POL, R-DES) and **three** controls
(C-NORM, C-RAND, C-NOOP) are pre-registered. No further repair form will be introduced. If one
is, it is reported as post-hoc, in its own section, and no headline may rest on it.

---

## 3. The G7 hazard, and why gain alone cannot settle this

`RENT_ISLANDS_RESULTS.md` §0.1 measured that **most large exceptional structures are LOSSY**:
on a lossy substrate *full upkeep does not restore the design state*, and the two populations
separated by twelve orders of magnitude. Whether the holonomy's connection is equivariant in the
relevant sense is exactly the open question here, and it is settled by measurement, not
assumption.

The operator setting makes the hazard concrete, and it is the reason this campaign has two
observables rather than one. **A repair can hold the holonomy's size while its direction wanders
off the design.** A scalar ledger has one coordinate and cannot express this; a 64×64 transport
operator can. So:

| observable | definition | denominator, named |
|---|---|---|
| **gain** `G(R,q)` | `‖Hol_q(R)‖_F / √d` (rms singular value) | `√d`, d = 64 the rung reference dimension |
| **fidelity** `F(R,q)` | `\|⟨Hol_des(R), Hol_q(R)⟩_F\| / (‖Hol_des(R)‖_F · ‖Hol_q(R)‖_F)` | the product of the two Frobenius norms — scale-free by construction, so it reads direction only |
| per-rung rate | `G(R,q)^(1/(R−1))`, `specrad(R,q)^(1/(R−1))` | **R−1**, the number of rung *steps*, not rungs |

**Gain alone is not evidence of maintenance, and control C-RAND is what proves it.**

---

## 4. The predictions, derived

### 4.1 What the rent clause actually says

`Core/Maintenance.lean` fixes the model exactly: `step γ α S = S − γ·S + α`, and `paid`
recomputes the payment from the *current* amount each step. Two readings of the payment are
available and they predict different things, so the derivation must choose, and say why.

**Reading (a) — proportional payment**, `α = c·S`. Then `S_{k+1} = (1 − ε + c)·S_k`. This holds
the entry iff `c = ε` **exactly**, and is a knife-edge: below, geometric decay; above, geometric
growth. This is `rent_holds` read literally with `α = γ·S`, and it predicts a sharp threshold at
`q* = ε`.

**Reading (b) — fixed deposit**, `α = q·S_0`: the repair writes back a fixed amount of design
structure per step, independent of how much survives. Then

```
S_{k+1} = (1−q)·λ·S_k + q·S_0        ⟹        S_∞/S_0 = q / (1 − (1−q)·λ)
```

nonzero for **every** `q > 0`, monotone, → 0 as `q → 0`, exactly 1 at `q = 1`. **No threshold.**

**This repository has already adjudicated between (a) and (b), empirically, and (b) won.**
`Core/Creation.lean` implements (b) — `repair_mints_from_noise`: the repair creates the code's
share from *pure noise*, so its deposit cannot be proportional to what survives, there being
nothing there. And `MAINTENANCE_SWEEP_RESULTS.md` measured it on two substrates: **P4 confirmed
the closed form** `p̂_∞ = p̂_0·q/(1−(1−q)λ^{|T|})` exactly, and **P5a falsified the `q ≥ ε`
threshold reading decisively** — retention at `q/ε` = 0.25, 0.5, 1, 2, 4 runs a smooth
0.31 %, 1.1 %, 3.3 %, 8.9 %, 20.4 % with no knee, and T4 reports "there is no knee at `q = ε`"
on the LFSR as well.

**So the rent clause, as this repository proves and measures it, predicts NO threshold — and the
brief's `q* = ε` intuition is not thereby wrong about the scale, only about the sharpness.**
Setting `g(q) = 1/2`:

```
q_half  =  ε / (2 − λ)          →  ε   as  ε → 0
```

**This is the campaign's sharpest pre-registered prediction and it is the honest form of "the
threshold sits where the rent clause says it must": there is no threshold, but the half-holding
dose equals the decay rate, exactly in the small-ε limit and within 1/(2−λ) of it here.**

### 4.2 Instantiated at the RECEIVED λ = 0.9655 (void if §1's re-derivation disagrees)

`g(q) = q / (ε + q·λ)`, `ε = 0.0345`:

| q | 0.001 | 0.003 | 0.01 | 0.01725 (ε/2) | 0.0345 (ε) | 0.069 (2ε) | 0.1 | 0.2 | 0.3 | 0.5 | 0.7 | 0.9 | 0.99 | 1 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| **g** | 0.0282 | 0.0802 | 0.2265 | 0.3372 | 0.5088 | 0.6824 | 0.7631 | 0.8787 | 0.9255 | 0.9666 | 0.9854 | 0.9962 | 0.9997 | 1.0000 |

`q_half = 0.0345/1.0345 = 0.03335`, i.e. **0.967 ε**.

### 4.3 The four staked hypotheses

- **H1 — PLATEAU.** For every `q > 0` the gain `G(R,q)` stops decaying with R and settles at a
  nonzero plateau `G_∞(q)`. **Kill:** any `q > 0` at which `G(R,q)` continues to decay
  geometrically out to the largest converged R with no plateau.
- **H2 — SHAPE.** `G_∞(q)` is monotone increasing in `q`, → 0 as `q → 0`, and shows **no knee**
  at `q = ε`. **Kill:** non-monotonicity beyond the numerical floor, or a knee at `q = ε`
  (defined as a discontinuity in `d log G_∞ / d log q` exceeding a factor of 2 between the
  bracketing grid points `q = ε/2` and `q = 2ε` while adjacent bracketing pairs show none).
  *A fired H2 kill would mean the holonomy behaves as reading (a) where two prior substrates
  behaved as reading (b) — a genuine and reportable difference, not a failure of the campaign.*
- **H3 — THE LAW.** `G_∞(q) = q/(ε + qλ)`, the maintenance sweep's P4 closed form, transfers to
  a Wilson-loop holonomy. Pre-declared readings of the residual, max over the q grid:
  **< 10 % relative** ⇒ the scalar rent law transfers quantitatively; **10–50 %** ⇒ transfers in
  shape only; **> 50 %, or the wrong sign of curvature** ⇒ does not transfer. The residual is
  reported per q whatever it is. *This is a point prediction, not a bound:* the scalar reduction
  assumes the per-step contraction acts as the scalar λ on the accumulated operator and that the
  deposit is aligned with it, and neither holds exactly for a non-normal 64×64 product. **The
  deviation is the operator content of this campaign and is reported as a finding, not as noise.**
- **H4 — FIDELITY, the open one.** Does the maintained holonomy stay *pointed at the design*, or
  merely stay *large*? `F(R,q)` for R-POL is the genuinely open quantity: R-POL knows only "be an
  isometry", not where the design points. **No prediction is staked on H4's direction.** Both
  outcomes are named in §5.

### 4.4 Honesty note on what is and is not discovery

**H1 for R-DES is near-structural and is not offered as a finding.** `H_{k+1} = (1−q)B H_k + q D_k`
is an affine recursion whose homogeneous part has gain `≤ (1−q)·‖B‖₂ = (1−q) < 1` for every
`q > 0`, so it converges to a bounded nonzero trajectory as a matter of arithmetic. R-DES is a
**calibration arm**: its content is the plateau *value* against H3 and its fidelity against H4,
not the existence of the plateau. The same caution applies to R-POL's gain in the scalar limit,
where both arms reduce to the same recursion `σ ↦ (1−q)λσ + q`. **The two arms are designed to
be indistinguishable in gain and to differ in fidelity — that is the whole design, and it is
why H4 and not H1 is the discovery axis.**

---

## 5. The outcome meanings, all of them, including the null

| outcome | reading |
|---|---|
| **MAINTAINED, faithfully** — H1, H2, H3 hold and R-POL's fidelity stays high and R-DES's does too | The holonomy is maintainable. The rent clause's measured law transfers from discrete classical substrates to a Wilson-loop holonomy of a genuine geometric connection — a third substrate class for a law measured on two. **F-11 stays fired**: the unmaintained loop still closes. The new claim is separate and is stated separately. |
| **MAINTAINED IN SIZE, LOST IN STRUCTURE** — H1/H2/H3 hold but R-POL's fidelity decays to the C-RAND floor while R-DES's stays high | The holonomy is **lossy under structure-blind upkeep**: isometry alone is not enough, and holding this structure requires a repair that *knows the design*. This is the operator form of `RENT_ISLANDS` G7 and of `Core/Creation.lean`'s divide — only maps that read more than their own cell mint anything. This would be the campaign's most interesting positive result and it is a *restriction* on maintainability, not a licence. |
| **NOT MAINTAINABLE** — no `q < 1` produces a plateau; only the `q = 1` endpoint (which is the design loop by construction, §2.2) holds | The structure cannot be held at any price short of total rebuild. **Stronger and more interesting than F-11**, and it would connect directly to `RENT_ISLANDS` G7's lossy substrates where full upkeep provably cannot restore the design state. Reported as loudly as any positive. |
| **THRESHOLD** — a genuine knee at some `q* > 0` | H2's kill has fired. The holonomy behaves as payment-reading (a) where the LFSR and the spatial lattice behaved as (b). The value of `q*` against `ε` is then the number, and the divergence from two prior substrates is the finding. |
| **UNINTERPRETABLE** | See §6. Reported as VOID, not as any of the above. |

---

## 6. What would make the result UNINTERPRETABLE — declared in advance

Any of these voids the affected reading, and a voided reading is reported as **ungauged**, which
per `GATES.md` is a first-class outcome and not a null:

1. **The connection is not identical.** The `q = 0` arm must reproduce the predecessor's twelve
   published `hol_trace` / `hol_specrad` / `hol_zero_dist` rows to `< 1e−10` absolute. Anything
   worse means the connection differs and **nothing in this campaign is comparable to F-11** —
   whole campaign VOID.
2. **The repair damages what is healthy.** C-NOOP: `‖Rep_q(U) − U‖_F < 1e−12` for the accumulated
   unitary forward leg, at every `q` in the grid, for both arms. Failure means the map is not a
   repair — whole campaign VOID.
3. **Numerical rank collapse.** Any cell with `sv_min/sv_max < 1e−13` is dropped as ungauged and
   *reported as dropped with its count*, never silently. (At `q = 0, R = 50` the predecessor's own
   `sv_min` is 0.034, so this bites only at the extended depths.)
4. **Catastrophic cancellation.** `‖Hol − I‖_F` computed directly must agree with
   `√(‖Hol‖_F² − 2·Re Tr Hol + d)` to `< 1e−10` relative. Disagreement voids the identity-distance
   column for that cell.
5. **Non-convergence read as a plateau.** A cell counts as plateaued only if `G(R,q)` changes by
   `< 1 %` relative across the top quartile of the R grid. Otherwise it is reported as
   **un-converged**, exactly as `MAINTENANCE_SWEEP_RESULTS.md` reports its `ε ≤ 0.003, q = 0`
   cells, and it may not be quoted as a plateau value.
6. **Dose-vs-rate disagreement.** If the three dosing schemes (§7) disagree beyond the stochastic
   floor, the plateau is scheme-dependent and **no single `G_∞(q)` curve may be quoted** — the
   disagreement itself is then the result.
7. **The spectral-radius instrument.** If `specrad` and `G` per-rung rates differ by `> 1 %` at
   `q = 0`, `specrad` is declared instrument-limited (§2.1) and every specrad-based statement,
   including the comparison to the predecessor's published law, carries that flag.

---

## 7. The controls, and what each one is for

| control | construction | what it gates | expectation, staked |
|---|---|---|---|
| **C-Q0** | `q = 0`, both arms | that the connection is bit-identical to the predecessor's | reproduces §1's RECEIVED table to < 1e−10 |
| **C-NOOP** | `Rep_q` applied to the unitary forward leg | that the repair is a repair — it must not touch what is at design (`parityRepair_fixed_iff`) | `< 1e−12` at every q, both arms |
| **C-NORM** (the forbidden move, run deliberately) | `H ← H·√d/‖H‖_F` — pure scalar rescale | that a manufactured plateau is distinguishable from a real one | gain plateaus at exactly 1 by construction; fidelity **identical to `q = 0`'s**, because a scalar rescale cannot move direction |
| **C-RAND** (the mixture null) | deposit a *fixed random unitary* `U_rand` in place of `D_k`, backward leg only, matched q | **that gain alone cannot support a maintenance claim** | gain plateaus like R-DES; fidelity ≈ the `1/√d` chance floor. If C-RAND's gain plateau matches the genuine arms', then gain is not evidence and only fidelity discriminates — which is the pre-registered reason H4 is the discovery axis |
| **C-DOSE** | three dosing schemes at matched mean effort `q`: (i) continuous strength `q` every rung; (ii) stochastic, full-strength repair with probability `q`; (iii) periodic, full-strength every `round(1/q)` rungs | `GATES.md` §7 dose-vs-rate: is the plateau set by total effort, or by how the effort is parcelled? | agreement within the stochastic floor ⇒ the plateau is a rent quantity. Disagreement ⇒ §6.6 fires |

**Floors matched to sample size.** The stochastic dosing arm runs **64 realizations** per `(R,q)`
cell, seeds `20260727 + i` for `i = 0…63`, and reports mean ± sd; the sd across realizations
**is** the floor against which scheme agreement is judged. The deterministic arms are exact
linear algebra with no sampling and therefore no shuffle floor is meaningful for them — that is
stated rather than a floor being invented for them. The chance floor for fidelity between two
independent `d×d` operators is `≈ 1/√d = 0.125` at `d = 64`; C-RAND measures it rather than
assuming it.

---

## 8. The grid, fixed now

- **R** = {3, 4, 5, 6, 7, 8, 9, 11, 13, 20, 30, 50} (the predecessor's, verbatim, for C-Q0)
  ∪ {75, 100, 150, 200, 300, 400} (the extension needed to separate a plateau from slow decay:
  at `q = 0.01` the approach rate is `(1−q)λ = 0.956`, a ~22-rung timescale, so 400 is ≳ 18
  timescales).
- **q** = {0, 0.001, 0.003, 0.01, 0.01725, 0.0345, 0.069, 0.1, 0.2, 0.3, 0.5, 0.7, 0.9, 0.99, 1.0}
  — 15 values, bracketing `ε` at ε/2, ε, 2ε, mirroring the maintenance sweep's grid.
- **arms** = {R-POL, R-DES} × **dosing** = {continuous, stochastic, periodic}, plus C-NORM,
  C-RAND, C-NOOP.
- **Cells:** 18 R × 15 q × 2 arms × 3 dosings = 1620 deterministic-equivalent cells, plus the
  stochastic arm's 64 realizations each. All exact linear algebra on 64×64 complex128 matrices.
  **This is the entire search. No cell outside this grid enters a headline.**
- **Determinism:** connection seed **20260522** (the predecessor's), so `W`, `B`, `CG`, `H_corr`
  are bit-identical to the run being extended. Stochastic dosing seeds as in §7.
- **Precision:** complex128 throughout, as the predecessor. Polar factors via SVD (backward
  stable), never via `(A†A)^(−1/2)` formed explicitly.

---

## 9. Reporting commitments

1. `HOLONOMY_RENT_RESULTS.md` states **in its first section** that F-11 stays fired on its own
   terms and that a maintained result is a different claim, and repeats it in the bottom line.
   Nothing in this campaign may be phrased as overturning the predecessor.
2. The `q = 1` endpoint is reported with its §2.2 caveat attached every time it is quoted.
3. Every fired kill is reported as plainly as every survival; dropped and un-converged cells are
   reported with counts.
4. Warrant-reach W2 is applied before commit: every citation in the prereg and the results — to
   `Core/Maintenance.lean`, `Core/Creation.lean`, `MAINTENANCE_SWEEP_RESULTS.md`,
   `RENT_ISLANDS_RESULTS.md`, and the predecessor's three files — is re-checked against the
   primary artifact, and the check is recorded in the results.
5. No Lean, no `Stance.lean`, no audit, no page change. This campaign produces two markdown files,
   one script and one JSON, in `scratchpad/`. Nothing is pushed.
