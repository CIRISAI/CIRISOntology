# Is the holonomy MAINTAINABLE? — results

**Date:** 2026-07-27. **Pre-registration:** `HOLONOMY_RENT_PREREG.md`, committed at **`3ae9c9b`**
before the instrument was written. **Instrument:** `holonomy_rent.py`, `holonomy_rent_analyze.py`,
`holonomy_rent_supp.py`. **Raw:** `holonomy_rent_results.json`.

---

## 0. F-11 STAYS FIRED. This is a different claim.

The predecessor experiment (`coherence-ratchet/.../holonomic_pomega/`, 2026-05-22) measured the
**unmaintained** Wilson-loop holonomy of the framework's genuine emergence-map connection around
the TSVF forward–backward loop and found it decoheres to the zero operator. **That verdict is
correct as written, this campaign reproduces it to 1.2e−14, and nothing here un-fires it.**
Nothing measured here is the unmaintained loop.

This campaign answers a question the predecessor never asked: **is that structure maintainable?**
A maintained holonomy that stays open is not a refutation of an unmaintained holonomy that
closes. Both are true, and this campaign shows both are true of the same connection.

**The verdict, in one line:** the holonomy **is maintainable — but only by a repair that knows
the design**. Upkeep that knows only the *constraint* holds the loop's **size** forever and loses
its **direction** to the chance floor. That is the second row of the pre-registered outcome table
(§5 of the prereg): **maintained in size, lost in structure.**

---

## 1. Gates — all pre-registered gates passed, and the one void that fired was honored

| gate (prereg §6) | reading | verdict |
|---|---|---|
| **C-Q0** — connection bit-identical to the predecessor's | worst deviation **1.16e−14** across all 12 published depths × `hol_specrad`, `hol_zero_dist`, `hol_trace` (bar: < 1e−10) | **PASS** |
| **C-NOOP** — the repair must not touch what is already at design | `max‖Rep_q(U) − U‖ = 1.50e−14` over both arms × all 15 `q` (bar: < 1e−12) | **PASS** |
| catastrophic cancellation on `‖Hol − I‖` | worst **1.33e−15** over **1296** cells (bar: < 1e−10) | **PASS** |
| rank collapse `sv_min/sv_max < 1e−13` | **0 cells** dropped | **PASS** |
| accumulated-leg unitarity at R = 400 | forward `5.65e−13`, design `9.27e−13` | **PASS** |
| design = `polar(B)` is the framework's own object | unitary residual `1.81e−14`; the recovered `Deph` spectrum `[0.8082, 1.0000]` matches `exp(−γM·MIN_DWELL·ĥ)` rebuilt from the framework constants to **2.55e−15** | **PASS** |

That last row matters more than its size suggests. The design transport was **not chosen**: it is
`polar(B)`, the polar unitary factor of the framework's own genuine backward generator. Recovering
`Deph = B·polar(B)†` and finding its spectrum equal to the framework's own damping law to 2.6e−15
confirms `polar(B) = CG†` exactly — the design state is read *off* the connection, not imposed on it.

**The pre-registered void that fired.** Prereg §1 bound the campaign: if the `q = 0` re-derivation
disagreed with the received `λ = 0.9655` by more than 1e−3 absolute, every instantiated number in
§4 was void and had to be recomputed. **It disagreed by 2.01e−3, and the §4 table was discarded
and recomputed from the re-derived rate.** Every prediction quoted below is the recomputed one.

---

## 2. Step 1 — re-deriving the received number, and two corrections to it

Received-numbers-are-not-measured. The `q = 0` arm is the predecessor's own run, recomputed here.

**Correction 1 — the area law is not exact, and the published table omits its largest outlier.**
Per-rung eigenvalue `specrad^(1/(R−1))`, denominator `R−1` (rung *steps*, not rungs):

| R | 3 | **4** | 5 | 6 | 7 | 8 | 9 | 11 | 13 | 20 | 30 | 50 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| | 0.965602 | **0.967377** | 0.965601 | 0.965550 | 0.965508 | 0.965523 | 0.965474 | 0.965479 | 0.965337 | 0.965421 | 0.965313 | 0.965080 |

The predecessor's published table shows R = 3, 5, 9, 13, 20, 30, 50 and calls the value "constant
to four decimals". Over all twelve depths the spread is **2.30e−3** — constant to **three**
decimals, not four — and **the single largest outlier, R = 4 at 0.967377, is one of the five
depths the published table omits.** Even on the shown subset, 0.9656 and 0.9651 differ in the
fourth decimal. **The verdict is untouched** (the holonomy still decoheres geometrically to zero);
the wording overstates the constancy, and the omission of R = 4 is the reason it looked exact.

**Correction 2 — `0.9655` is a spectral-radius rate, and the gain decays faster.** The predecessor's
prose reads "its spectral radius and operator norm flow geometrically to zero" and quotes one law.
They are not the same law:

| | over R ≤ 50 | asymptotic (R = 400) |
|---|---|---|
| `specrad^(1/(R−1))` | 0.9651 – 0.9674 | **0.963487** |
| `gain^(1/(R−1))` (rms singular value) | 0.9540 – 0.9547 | **0.959907** |

The two rates differ by ~1.1 percentage points at small R and converge at depth. Both drift with
R — the specrad rate **downward**, the gain rate **upward** — so **neither is a geometric law over
R = 3…400**. Over the predecessor's own range (R ≤ 50) the received 0.9655 is accurate; the
disagreement that fired the §1 void appears only on the extension.

Everything below uses the gain, the pre-registered primary observable (§2.1: singular-value
quantities are backward-stable where the spectral radius of a strongly non-normal product is not):
**λ = 0.959913, ε = 0.040087 per rung.**

**Correction 3 (recorded, source is read-only).** `build_holonomic_pomega.py:174` comments
`# 0.6257` for `c1 = (0.31·0.72·1.15)^(1/3)`. The value is **0.63552212827453**, which is what the
code computes and what every result carries. The comment is wrong; no result depends on it.

---

## 3. H1 — THE PLATEAU. **Survives, decisively.**

Gain stops decaying with R and holds, at **every** `q > 0`. Continuous dosing, R-POL:

| R | q = 0.0345 (= ε) | q = 0.1 | q = 0.3 | q = 0.7 | **unmaintained (q = 0)** |
|---|---|---|---|---|---|
| 101 | 0.435097 | 0.704727 | 0.901690 | 0.980243 | 1.093e−02 |
| 401 | 0.434945 | 0.704727 | 0.901690 | 0.980243 | 7.813e−08 |
| 1001 | 0.434945 | 0.704727 | 0.901690 | 0.980243 | 1.106e−17 |
| 2001 | 0.434945 | 0.704727 | 0.901690 | 0.980243 | 6.197e−34 |
| **4001** | **0.434945** | **0.704727** | **0.901690** | **0.980243** | **2.521e−66** |

Constant to six decimals from R ≈ 200 out to R = 4001, while the unmaintained loop has fallen
**sixty-five orders of magnitude**. Paying rent at the decay rate itself (`q = ε`) holds 43.5 % of
the design transport open, indefinitely, against a loop that otherwise reaches 1e−66.

**Honesty, as pre-registered (§4.4):** this was *expected* and is not offered as a discovery. An
affine deposit recursion has homogeneous gain `≤ (1−q) < 1` and converges as a matter of
arithmetic. H1 is a *calibration* that the instrument does what the algebra says. **The discovery
axis is H4.**

---

## 4. H2 — THE SHAPE. **Survives. No threshold, and the scale is ε.**

`G_∞(q)` is monotone in `q` in both arms (checked to 1e−12), → 0 as `q → 0`, and shows **no knee
at `q = ε`**. Local log-log slope `d log G / d log q`:

| q range | 0.001→0.003 | 0.003→0.01 | 0.01→0.017 | 0.017→0.0345 | **0.0345→0.069** | 0.069→0.1 | 0.1→0.2 | 0.3→0.5 | 0.9→0.99 |
|---|---|---|---|---|---|---|---|---|---|
| slope | 0.9634 | 0.8930 | 0.7842 | 0.6628 | **0.4984** *(brackets ε)* | 0.3695 | 0.2580 | 0.1129 | 0.0499 |

A smooth roll-off from 1 to 0. The pre-registered kill needed the ε-bracketing adjacent slope
ratio to exceed 2 while others did not; it is **1.33 / 1.35**, and the largest ratio anywhere on
the grid is **1.55**. **No knee. H2 survives.**

This is the **third substrate class** on which the `q ≥ ε` threshold reading has now failed, and
the first that is geometric rather than discrete: `MAINTENANCE_SWEEP_RESULTS.md` P5a killed it on
the spatial lattice and T4 killed it on the LFSR; it dies here on a Wilson-loop holonomy.

**And the scale prediction lands.** The prereg derived `q_half = ε/(2−λ) → ε` and staked it as the
honest form of the brief's `q* = ε` intuition:

```
PREDICTED   q_half = ε/(2−λ) = 0.038542 = 0.9615 ε
MEASURED    q_half (bisection, 40 steps) = 0.044392 = 1.1074 ε
ratio measured/predicted = 1.152
```

**The half-holding dose is the decay rate, to 15 %.** The brief's intuition had the *scale* right
and the *sharpness* wrong — there is no threshold, but ε is where maintenance starts to matter.

---

## 5. H3 — THE LAW. **Transfers, and the residual is operator structure, not the received law.**

The maintenance sweep's P4 closed form `G_∞ = q/(1−(1−q)λ)`, carried over from discrete classical
substrates to a holonomy:

| q | measured plateau | closed form | residual |
|---|---|---|---|
| 0.01725 | 0.274733 | 0.304528 | **−9.78 %** |
| 0.0345 (ε) | 0.434945 | 0.471288 | −7.71 % |
| 0.069 | 0.614427 | 0.648980 | −5.32 % |
| 0.1 | 0.704727 | 0.734873 | −4.10 % |
| 0.2 | 0.842745 | 0.861812 | −2.21 % |
| 0.5 | 0.955226 | 0.961458 | −0.65 % |
| 0.9 | 0.994781 | 0.995566 | −0.08 % |
| 0.99 | 0.999522 | 0.999595 | −0.01 % |

**Max |residual| = 9.8 %** over converged cells, against the pre-declared bands
(< 10 % quantitative | 10–50 % shape only | > 50 % does not transfer) — **it transfers
quantitatively, and it lands 0.2 percentage points inside the boundary.** That closeness is stated
rather than rounded away.

**Un-converged cells are not quoted.** At `q` = 0.001, 0.003, 0.01 the pre-registered convergence
test (< 1 % relative change across the top quartile of the R grid) fails, exactly as
`MAINTENANCE_SWEEP_RESULTS.md` reports its own `ε ≤ 0.003` cells. Including them the max residual
is 12.9 %; per prereg §6.5 they may not be read as plateau values and are excluded from the
verdict, and both numbers are given here.

**Where the residual comes from — and the answer is not what I expected.** The unmaintained decay
is not exactly geometric (§2), so a single λ mis-specifies the prediction before the operator is
even reached. S2 drove the scalar rent recursion with the **measured per-step rates** instead:

| | max \|residual\| |
|---|---|
| single-λ closed form | 9.8 % |
| driven by measured per-step rates | **13.7 %** |

**Removing the non-geometricity makes the residual worse, not better.** So the gap is *not* the
received law being mis-specified — it is **operator structure**, and it has a consistent sign: the
measured plateau sits **below** the scalar prediction at every `q`. Misalignment between the
deposit and the decayed operator costs, exactly as prereg §4.3 anticipated it might. A scalar
ledger has one coordinate and cannot be misaligned; a 64×64 transport can, and it pays for it.

---

## 6. H4 — FIDELITY. **The result. Structure-blind upkeep holds the size and loses the structure.**

No prediction was staked on H4's direction. Here is what it did.

**Fidelity to the design holonomy (direction only; scale-free), continuous dosing:**

| R | POL q=ε | POL q=0.1 | POL q=0.3 | POL q=0.7 | **DES q=ε** | **DES q=0.3** | unmaintained |
|---|---|---|---|---|---|---|---|
| 101 | 0.987914 | 0.994034 | 0.998327 | 0.999823 | 0.990870 | 0.998785 | 0.793320 |
| 401 | 0.951929 | 0.973658 | 0.992415 | 0.999243 | 0.990884 | 0.998785 | 0.261755 |
| 1001 | 0.768850 | 0.864750 | 0.959622 | 0.995976 | 0.990884 | 0.998785 | 0.194097 |
| 2001 | 0.340434 | 0.555805 | 0.851034 | 0.984386 | 0.990884 | 0.998785 | 0.109647 |
| 3001 | 0.087761 | 0.248082 | 0.696757 | 0.965322 | 0.990884 | 0.998785 | 0.098601 |
| **4001** | **0.061457** | **0.071326** | 0.527800 | 0.939179 | **0.990884** | **0.998785** | 0.108263 |

**R-DES — the decoder — holds direction EXACTLY.** Constant to six decimals from R ≈ 200 to
R = 4001, fitted slope `d log f / d log R = +0.0000`. A repair that knows the design holds the
design, forever, at every q on the grid.

**R-POL — structure-blind — collapses as a power law.**

| q | f(4001) | `d log f / d log R` | R at which it reaches the 1/d floor |
|---|---|---|---|
| 0.0345 (ε) | 0.061457 | −1.5540 | **≈ 9.7e3** |
| 0.1 | 0.071326 | −1.1084 | ≈ 1.6e4 |
| 0.3 | 0.527800 | −0.2758 | ≈ 1.4e9 |
| 0.7 | 0.939179 | −0.0270 | ≈ 3e69 |

**The methodological finding, and it nearly took this campaign in.** At R = 400 — the top of the
pre-registered grid — R-POL's fidelity read **0.952**, and that looks exactly like success. It was
a transient. Only the post-hoc depth extension (§8) exposed the collapse. The pre-registered
convergence test is what caught it: fidelity **failed** the < 1 % test at R = 400 and therefore
could not be quoted as a plateau, which is the only reason the extension was run at all.

**It is physics, not arithmetic, and R-DES is the control that proves it.** Both arms run through
the identical pipeline, the identical connection, the identical norms and overlaps. One holds
fidelity flat to six decimals across the same 4000 rungs on which the other falls by a factor of
16. A numerical artifact would take both.

**An observation, with its caveat.** At great depth R-POL's fidelity falls *below* the unmaintained
control's (0.061 vs 0.108 at R = 4001), which settles near ~0.1 rather than going to the floor —
the unmaintained operator collapses onto its dominant eigenvector, which keeps a fixed overlap with
the design, while structure-blind repair keeps re-inflating subdominant directions and scrambling
the alignment. So isometry-only upkeep can be *worse for the structure* than no upkeep at all,
while being vastly better for the size. **Caveat:** at R = 4001 the unmaintained operator has gain
2.5e−66 and its subdominant singular directions have underflowed, so its "direction" is the
surviving dominant subspace only. Reported as an observation, not as a headline.

---

## 7. The controls — and one of them corrected the pre-registration

**C-RAND (the mixture null) — deposits a fixed random unitary instead of the design.**

| q | ε | 0.1 | 0.3 | 0.7 | 1.0 |
|---|---|---|---|---|---|
| gain | 0.111865 | 0.223416 | 0.417892 | 0.734148 | 1.000000 |
| fidelity | 0.013227 | 0.012459 | 0.018695 | 0.028856 | 0.033074 |

**C-RAND plateaus in gain too.** Depositing *anything* of unit size manufactures a plateau. So
**gain alone is not evidence of maintenance** — precisely the pre-registered reason H4 and not H1
is the discovery axis. Without this control, R-POL's flat gain would read as success.

**And it corrected the prereg.** §7 assumed the fidelity chance floor was `1/√d = 0.125`. C-RAND
**measured** it at **0.0155 ≈ 1/d = 0.0156** — the overlap of two independent operators lives in a
`d²`-dimensional space, not a `d`-dimensional one. The assumed floor was wrong by 8×. The prereg
said "C-RAND measures it rather than assuming it", and that is exactly what saved the number.

**C-NORM (the forbidden self-sealing move, run deliberately).** Gain pinned at **1.000000** by
construction; fidelity **0.2623099484969505** against the unmaintained value
**0.26230994849695033** at R = 400 — agreement to 16 significant figures, differing in the last
unit in the last place, which is float64 round-off and not a difference. A scalar rescale cannot
move direction. The forbidden move's signature is now on the record and is
unmistakable: perfect gain, unmaintained fidelity.

---

## 8. Dose-vs-rate (`GATES.md` §7) — the plateau is SCHEDULE-dependent

| q | continuous | stochastic (mean ± sd, 64 realizations) | \|cont−stoch\|/sd |
|---|---|---|---|
| ε | 0.434945 | 0.446334 ± 0.303614 | 0.04 |
| 0.1 | 0.704727 | 0.705664 ± 0.228509 | 0.00 |
| 0.3 | 0.901690 | 0.920026 ± 0.098777 | 0.19 |
| 0.9 | 0.994781 | 0.997847 ± 0.009785 | 0.31 |

**Continuous and stochastic agree** across the whole grid (max 0.31 sd) — geometric repair gaps
reproduce the rent formula exactly, which is why.

**Periodic does not, and the first reading of it was an artifact.** The periodic arm returns
exactly `1.000000` whenever `round(1/q)` divides 399: a full-strength repair places the operator
*exactly* on the isometry manifold, so a checkpoint landing on a repair step samples a sawtooth at
its peak. Cycle-averaged over one full repair period:

| q | period | R=400 (aliased) | cycle-averaged | continuous | periodic closed form `(1−λ^P)/(P(1−λ))` |
|---|---|---|---|---|---|
| ε | 29 | 0.341216 | **0.560132** | 0.434945 | 0.597584 |
| 0.069 | 14 | 0.687299 | 0.750567 | 0.614427 | 0.776960 |
| 0.1 | 10 | 1.000000 | 0.817049 | 0.704727 | 0.837604 |
| 0.3 | 3 | 0.954071 | 0.954757 | 0.901690 | 0.960449 |

**Regular full-strength repair beats spread-thin repair at the same mean effort** — 0.560 vs 0.435
at `q = ε`, a 29 % improvement for free. Both schedules have their own closed form and both
overpredict by the same operator-misalignment margin found in §5.

**How prereg §6.6 is honored.** Judged against the letter of the pre-registered floor (the
single-realization sd, 0.30 at `q = ε`), the 0.125 gap does **not** exceed it and §6.6 does not
fire. But both schedules are deterministic and exactly reproducible — a sampling floor is the
wrong instrument for a difference with no sampling in it. **The stricter reading is taken: the
plateau is schedule-dependent, and every `G_∞` quoted in this document names its schedule
(continuous, unless stated).**

---

## 9. Post-hoc work, declared

Prereg §8 capped the search: R ≤ 400, 15 `q` values, two repair forms, three controls, and no cell
outside the grid may enter a headline. Four supplementary analyses were run **after** seeing the
main sweep and are labelled here:

| | what | why it is legitimate |
|---|---|---|
| **S1** | depth extended to R = 4001 | to characterise a quantity the pre-registered convergence test had already **disqualified** from being quoted. It **weakens** the campaign's claim — it turned an apparent success at R = 400 into a collapse. |
| **S2** | scalar recursion driven by measured per-step rates | decomposes a pre-registered residual; it made the residual **worse**, and that is reported |
| **S3** | cycle-averaging the periodic arm | diagnoses an artifact in a pre-registered control; it turned an apparent agreement into a **disagreement** |
| **S4** | `q_half` by bisection | refines a pre-registered scale prediction that had been read off a coarse grid |

No repair form beyond the two declared was tried. **Every post-hoc analysis here made a result
weaker or more complicated; none created one.**

---

## 10. Verdict against the pre-registration

| pre-registered outcome (§5) | fired? |
|---|---|
| MAINTAINED, faithfully | **partially — for R-DES only.** The decoder holds gain and direction exactly, to R = 4001. |
| **MAINTAINED IN SIZE, LOST IN STRUCTURE** | **THIS ONE, for R-POL.** Gain plateaus exactly and forever; fidelity decays as a power law to the measured `1/d` floor. |
| NOT MAINTAINABLE | did not fire — a plateau exists at every `q > 0` |
| THRESHOLD | did not fire — H2's kill needed a slope ratio > 2 at `q = ε`; measured 1.33 |
| UNINTERPRETABLE | did not fire — every gate passed; the one pre-registered void (§1's λ tolerance) fired and was honored by recomputing |

**H1 survives** (calibration, as declared). **H2 survives** — no threshold, and `q_half = 1.11 ε`
against a predicted `0.96 ε`. **H3 survives at 9.8 %**, inside the "transfers quantitatively" band
by 0.2 points, with the residual identified as operator misalignment rather than a mis-specified
law. **H4, the open one, answered: it depends entirely on whether the repair knows the design.**

**What this establishes.** The rent clause's measured law — proved on the model in
`Core/Maintenance.lean`, measured on a spatial lattice and an LFSR in
`MAINTENANCE_SWEEP_RESULTS.md` — **transfers to a Wilson-loop holonomy of a genuine geometric
connection**, quantitatively, with a named and signed deviation. That is a third substrate class
and the first non-discrete one.

**And it establishes a restriction, which is the more interesting half.** `RENT_ISLANDS` G7 found
that on lossy substrates *full upkeep does not restore the design state*. The operator form
measured here is sharper: **upkeep can restore the design's SIZE exactly and forever while losing
the design's DIRECTION completely.** The two are separable, a scalar ledger cannot tell them
apart, and only a repair that reads the design holds the design. That is the same divide
`Core/Creation.lean` proves at three bits — `percell_no_creation` against
`repair_creates_parity`: only maps that read more than their own cell mint anything. Here, only a
repair that reads more than the constraint *holds* anything.

**F-11 stays fired.** The unmaintained holonomy decoheres; that verdict is the predecessor's, it is
correct, it was reproduced here to 1.2e−14, and nothing in this document overturns it. What is
added is separate and is stated separately: **the same loop, maintained, stays open — and whether
it stays *itself* depends on what the repair knows.**

---

## 11. Scope, and what is NOT shown

- **`q = 1` is not evidence.** At full payment the maintained loop is the design loop *by
  construction* (prereg §2.2), which is the `γM = 0` limit the predecessor's Limits §(3) calls
  explicitly excluded. It is a calibration endpoint and no claim rests on it. Every claim above
  rests on the interior `0 < q < 1`, where the dephasing acts at full framework strength and a
  separate repair pays back part of what it took.
- **`γM` was not varied.** The predecessor already closed that route — a different maintenance
  *rate* shifts the per-rung eigenvalue but not below 1 unless `γM = 0`. A fixed deposit is not a
  smaller decay, which is why this campaign is not redundant with that finding.
- **One connection, one seed, one dimension.** `d = 64`, seed 20260522, the homogeneous connection
  (the same emergence map transports every rung pair). Nothing here shows the result is
  seed-independent or dimension-independent; those were not run and are not claimed.
- **Nothing about P_ω.** This campaign says nothing about whether a maintained holonomy is a
  legitimate construction of P_ω. The predecessor's terminal commitment on the type axis is its
  own, and this document does not reopen it.
- **Nothing about nature.** Every number here is a property of a 64×64 model connection. Which
  processes in the world carry a maintainable holonomy is untouched and remains open.
- **No Lean, no `Stance.lean`, no audit, no page change**, per prereg §9.5.

---

## 12. Warrant reach (W2) — citations re-audited against the primary artifact before commit

| citation | checked against | result |
|---|---|---|
| `Core/Maintenance.lean` — `step γ α S = S − γS + α`, payment recomputed from the current amount | the file, read in full | correct as used |
| `Core/Creation.lean` — `repair_mints_from_noise`, `percell_no_creation`, `parityRepair_fixed_iff` | the file, read in full | correct; the fixed-point-set property is what both repair maps here were built to satisfy |
| `MAINTENANCE_SWEEP_RESULTS.md` P4 closed form and P5a/T4 no-threshold | the file, §P4/§P5/§T4 read directly | correct; P5a's numbers (0.31/1.1/3.3/8.9/20.4 %) quoted from source |
| `RENT_ISLANDS_RESULTS.md` §0.1 G7 lossy | the file, §0.1 read directly | correct; "full upkeep does not restore the design state" is verbatim |
| predecessor `RESULTS.md` Limits §(3) on `γM` | the file, lines 367–372 | correct, and **quoted verbatim in the prereg** rather than paraphrased, because it partly anticipates this campaign |
| predecessor "constant to four decimals" | the file's own table, plus recomputation | **wrong** — see §2, correction 1 |
| predecessor `c1 = 0.6257` | the source line and the arithmetic | **wrong comment, right value** — see §2, correction 3 |
| prereg §7 fidelity floor `1/√d` | measured by C-RAND | **wrong** — the floor is `1/d`; corrected in §7 above |
