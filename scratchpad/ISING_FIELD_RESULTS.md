# RESULTS — the pairwise-blind order-3 share over the (T, h) plane of the 2D Ising model

Pre-registered in `ISING_FIELD_PREREG.md`, committed at `c67988c` **before** `ising_field.py`
existed. Scratchpad only: no Lean file, `Stance.lean` or the audit was touched, and `lake`
was never run.

**Scope, first and load-bearing.** This is a **model system**. The 2D Ising model is not
nature. Nothing here bears on the `wild-share` open claim, nothing here is evidence about the
world, and no sentence below should be read as one. What follows is a fact about a canonical
statistical-mechanical model, and about the instruments used to study it.

---

## THE HEADLINE

**Turning on a field does put pairwise-blind order-3 structure into the Ising model** —
outcome **(b)** — and it lives in **two distinct regimes that answer the pre-registered
question differently.**

| | peak `I_C^(3)` | CF vs `ln 2` | carried by | behaviour in `L` |
|---|---|---|---|---|
| **critical ridge** (`T ≈ T_c`, `h ~ L^(−15/8)`) | **4.6e-03 nats** | **0.66 %** | **well-separated** triples | flat: 3.7–4.9e-3 across `L` = 8→64 |
| **fixed field** (`h` ≫ the ridge, `L → ∞`) | 5.2e-05 nats | 0.0076 % | **local** triples (`star`) | converged to 1–2 % for `L` ≥ 16 |

**But the finding that cost the least and is worth the most is the control column.** At
`h = 0` exactly, `I_C^(3)` reads **8.9 × 10⁻¹⁶ nats** — machine zero — at all 49 temperatures,
on every lattice, for every geometry, while on the **same distributions** the ordinary
higher-order measures reach their absolute theoretical maxima: multi-information
`TC = 1.386294 = 2 ln 2` and O-information `Ω = 0.693147 = ln 2`. Those are exactly the values
`Core/SignSymmetry.lean` proves for the ferromagnetic state (`S_total_ferro`, `share_ferro`).
**The standard instruments are maximal precisely where the pairwise-blind quantity is provably
zero** — `SPIKE_SURVEY.md`'s thesis, demonstrated at machine precision inside one canonical
model on one set of distributions rather than argued across a literature.

**Scorecard against what I wrote down in advance.**

| prediction | outcome |
|---|---|
| magnitude `10⁻³`–`10⁻²` nats, CF 0.1–1 % | **survived** — 4.6e-3, CF 0.66 % |
| small-`h` scaling `∝ h²` | **survived** — measured exponent **2.000** |
| **K4**: `star` carries the largest peak | **FIRED** — separated triples carry the peak, by ~4× |
| **(b2)**: local effect, no critical enhancement | **SPLIT** — true at fixed field, false on the ridge |
| peak at `h` of order `T` | **wrong** — `h*` is ~16× smaller than `T`, and `→ 0` as `L → ∞` |

---

## 1. VALIDITY — outcome (a), reported first as the prereg requires

The sign-symmetry lemma says a zero-field Ising model has whole-only share exactly zero at
every temperature, criticality included. If the pipeline disagreed, the run would be void.

**Exact arm** — `max |I_C^(3)|` over 49 temperatures × all geometries at `h = 0`:
`4.441e-16` (4×4), `8.882e-16` (6×4), `8.882e-16` (5×5). **Worst over everything: 8.9e-16.**
Floating-point zero.

**Sampled arm, at every lattice size** — bias-corrected excess at `h = 0`:

| `L` | 8 | 16 | 32 | 64 |
|---|---|---|---|---|
| max \|z\| | 0.81 | 0.82 | 0.78 | 0.72 |

**Outcome (a) confirmed; K1 did not fire.** This is `share_eq_zero_of_signSymmetric`
reproduced numerically on a physical model, and it is the reason the rest of the map can be
believed.

## 2. THE INSTRUMENT, and two gate failures that had to be adjudicated

The `k = 3` pair envelope is **one-dimensional**: adding `t·s₁s₂s₃` to the eight cell
probabilities preserves normalisation and all three pair marginals, and nothing else does. So
the maxent member is the unique root of `Σ_s σ(s)·log(p(s) + t·σ(s)) = 0`, since `dH/dt =
−g(t)`. Because the entropy is being *maximised*, `dH/dt = 0` at the root and an error `δ` in
`t` costs only `O(δ²)`.

**The gate failed on first run, on two of eight tests. Both are reported as plainly as the
passes, and neither was fixed by relaxing a threshold.**

### Gate 5 — the reference number was wrong, not the instrument

Asserted the `SPIKE_SURVEY.md` pairing "explicit 3-body coupling `K = 0.9` → `0.247` nats".
Measured `0.284838`. Adjudicated **in closed form, with no solver involved**: for
`p ∝ exp(K·s₁s₂s₃)` every pair marginal is exactly `1/4`, so the pairwise maxent *is* the
uniform state and `I_C^(3) = 3ln2 − H(p)` exactly. The closed form gives `0.284838` at
`K = 0.9`, matching my solver to `0.0e+00`.

> **Correction to the record.** `SPIKE_SURVEY.md` pairs `K = 0.9` with `0.247 nats`. The
> correct value at `K = 0.9` is **`0.2848`**; `0.247` is `K = 0.8146`. The generating script
> was never committed, so which number was mistyped cannot be recovered. **This affects no
> conclusion in the survey** — the control's job was to show the instrument fires on an
> explicit three-body coupling, and it does.

### Gate 2 — the repository's shared IPF machinery is the one that drifts

Required agreement with `array_cap_experiment.shareK` (IPF) to `1e-9` on boundary-adjacent
states; failed at `5.6e-5`. Rather than pick between two solvers I brought in an
**independent 60-digit `mpmath` reference**. The prereg's own row already named the tie-break
("the fast solver is the reference where IPF fails to converge"), so this makes that
operational rather than inventing a new rule.

| 50 boundary-adjacent states (min cell ~1e-8) | max error vs 60-digit reference |
|---|---|
| the fast solver | **9.6e-15** |
| `array_cap_experiment.shareK` (IPF, tol 1e-13, 20000 iters) | **4.6e-05** |

At the worst state the true share is `1.2e-10` and **IPF reports `9.8e-6` — five orders of
magnitude too large.** The error is one-sided: IPF **overstates** the share on
near-deterministic states.

> **Caution for the shared machinery, recorded because it outlives this experiment.**
> `shareK`'s IPF converges to a stated tolerance on the *pair marginals*, and that tolerance
> does **not** bound the error in the *entropy gap* when cells approach zero. Future use of
> `shareK` on near-deterministic states should carry the fast solver or an arbitrary-precision
> check alongside. **This is a caution, not a retraction**: the `ARRAY_CAP_RESULTS.md` numbers
> were not in that regime.

**It did not affect this experiment either**, which is why the amended gate is not a
convenience. Gate 9 was *added* to measure precision on the states this experiment actually
encounters, including the near-deterministic corners of the real grid: **fast solver
`3.1e-16`, IPF `1.4e-12`.**

The eight-test gate then passed: parity reads `ln 2` to 15 digits (`0.693147180559945`, with
`I_C^(2) = 0` exactly and `Ω = −ln 2`), the independent state reads `0.0`, the lemma reads
`4.4e-16` on 2000 random sign-symmetric states, and the histogram factorisation was verified
against an independent brute-force enumeration (`max |Δp| = 3.7e-14`,
`max |ΔI_C^(3)| = 8.9e-16`).

## 3. METHOD

**Arm A — exact enumeration (primary).** All `2^N` configurations of periodic 4×4, 6×4 and
5×5 lattices. **No sampling, no estimator, no bias.** The Boltzmann weight depends on a
configuration only through its broken-bond count and its magnetisation, so one pass building
the histogram `(B, P, triple-pattern)` is a sufficient statistic for the *entire* (T,h) plane.
49 temperatures × 33 fields, `h = 0` included exactly.

**Arm B — Metropolis (checkerboard, GPU), L = 4…64.** Cluster algorithms (Wolff,
Swendsen–Wang) **do not apply in a field**: their construction assumes the global sign
symmetry that is the whole point of breaking. Stated, not glossed. Surrogate drawn at
**`N_eff`, not nominal `N`** — pooling `L²` translates does not give `L²` independent samples;
measured variance-inflation `F` ran from 3.4 to 5.5e4, so nominal `N` would have understated
the floor by up to four orders of magnitude. Plus configuration-level bootstrap, shuffle
floor, cross-run refuter, and `τ_int` measured everywhere.

**Tied fraction: 0 everywhere, and this is vacuous rather than reassuring.** Ising spins are
natively binary; nothing is thresholded, so the static-nonlinearity artifact channel is
**structurally absent** — not "checked and found clean". Different statements.

**One disclosed mid-run methodological change.** The first finite-size pass anchored its
field scan on the 4×4 peak and showed the peak migrating to smaller `h` with growing `L`,
into the near-critical region where Metropolis critical slowing down drove `F` above `10³` and
collapsed `N_eff` below the pre-registered trustworthiness floor — the honest filter was
excluding exactly the points of interest. The targeted runs therefore scale the sampling gap
with `L` (`gap = 3L`). **This is a choice about estimator validity, not about the value of the
estimate**, and it changed no reported number that was already trustworthy.

## 4. KILL K5 — does the Monte Carlo reproduce an answer we already know exactly?

Arm B is reportable only if it recovers Arm A's exact values where enumeration settles them.

| | |
|---|---|
| grid points compared | **55** |
| beyond 2 sd | **0** |
| max \|resid/sd\| | **1.79** |
| mean resid/sd | −0.224 |

**K5 PASSED.** The pipeline tracks the exact answer over five orders of magnitude down to
`2.5e-7` nats (6×4, `T=1.6`, `h=0.6`: exact `2.476e-07`, MC `1.735e-07 ± 8.9e-08`), and reads
`−2e-6 ± 3e-6` where the exact answer is literally zero. **Cross-run refuter**: `z = −0.63`
and `+0.57` — clean, the null is not mis-specified.

## 5. REGIME 1 — fixed field, thermodynamic limit: LOCAL, and `star` wins

At a field well above the finite-size critical scale, the share **converges** with lattice
size. `star` excess, matched `(T,h)`:

| `T/T_c` | `h` | L=8 | L=16 | L=32 | L=64 | L16→L64 |
|---|---|---|---|---|---|---|
| 0.875 | 0.2108 | 1.675e-05 | 1.545e-05 | 1.557e-05 | 1.561e-05 | **1.01×** |
| 1.052 | 0.2108 | 6.753e-05 | 4.617e-05 | 4.492e-05 | 4.716e-05 | **1.02×** |
| 1.228 | 0.2108 | 8.323e-05 | 5.181e-05 | 5.238e-05 | 5.099e-05 | **0.98×** |
| 1.404 | 0.2108 | 3.201e-05 | 2.357e-05 | 2.293e-05 | 2.371e-05 | **1.01×** |

Converged to 1–2 % over a 16× range in area. **This is a genuine thermodynamic-limit
quantity**, and the geometry ordering is identical at every `L ≥ 16`:

| `L` | ordering at `T/T_c = 1.228`, `h = 0.2108` |
|---|---|
| 16 | star 5.18e-5 > colin1 9.55e-6 > colin2 6.53e-6 > Lcorner 3.70e-7 > plaq 2.99e-7 > **far −4.7e-8** |
| 32 | star 5.24e-5 > colin1 9.43e-6 > colin2 6.44e-6 > Lcorner 3.91e-7 > plaq 3.57e-7 > **far −6.4e-8** |
| 64 | star 5.10e-5 > colin1 8.95e-6 > colin2 6.50e-6 > Lcorner 4.61e-7 > plaq 4.12e-7 > **far −2.9e-8** |

**`far` is exactly zero** (`z = −0.7`) and **`star` beats the next class by 5.5×.** Here the
pre-registered mechanism is exactly right, and its detail is confirmed: `star` is the one
class with **no direct bond inside the triple** and a **shared neighbour** — integrating that
neighbour out generates the three-body term, while classes with direct bonds put their
correlation into the *pairs*, where a pairwise-blind quantity cannot see it. Well-separated
spins share nothing and read zero.

`Lcorner` and `plaq` return identical values throughout — they are the same triple (two
nearest-neighbour steps at a right angle) up to a lattice symmetry, a free internal
consistency check the code passes.

**Small-field scaling: exponent 2.000**, to four significant figures over a decade of field,
confirming the pre-registered `I_C^(3) ≈ ½K²·Var` with `K ∝ βh`.

## 6. REGIME 2 — the critical ridge: COLLECTIVE, and separation wins

The peak field shrinks with `L`. Placing the grid by the magnetic scaling dimension
(`h* ~ L^(−15/8)`, disclosed as physics-motivated placement, not a fit) and sitting at
`T = T_c`:

| `L` | `h*` | `star` (local) | separated triple (`r = L/4`) | CF of the separated one |
|---|---|---|---|---|
| 8 | 0.0575 | 2.509e-03 | 3.670e-03 | 0.53 % |
| 16 | 0.0157 | 1.596e-03 | **4.945e-03** | **0.71 %** |
| 32 | 0.00427 | 1.115e-03 | 4.563e-03 | 0.66 % |
| 64 | 0.00116 | 8.840e-04 | 3.700e-03 | 0.53 % |

**The separated triple holds at 3.7–4.9e-3 nats across an 8× range in linear size**, while the
local `star` decays steadily (`h*` shrinks and the local term goes as `h²`). A direct
separation scan at `T = T_c`, `h = h*(L)` shows the share **growing** with distance and
saturating:

| `L` = 32, `h*` = 0.0043 | r=1 | r=2 | r=4 | r=8 | r=12 |
|---|---|---|---|---|---|
| excess (nats) | 5.09e-04 | 1.80e-03 | 3.31e-03 | 4.57e-03 | 4.73e-03 |

This is the **opposite** of the fixed-field behaviour, and it explains the exact arm: the
5×5 `far` peak of `4.717e-03` (CF 0.681 %) and the `L = 32` ridge value of `4.563e-03`
(CF 0.658 %) **are the same number**. The exact small-lattice peak was not a finite-size
artifact — it was the critical scaling value, and it survives to `L = 32`.

**Mechanism (post-hoc, labelled as such):** at criticality the order-parameter distribution is
non-Gaussian, and a field makes it **skewed**. Widely-separated spins are correlated only
through that single collective mode, so three of them read one skewed latent — which is
exactly a source of order-3 structure the pair marginals cannot reconstruct. Local triples
instead have their correlation dominated by direct bonds, which is pairwise.

**Honest weakness, stated plainly:** these are the hardest points to measure. `F` reaches
`5.5e4` and `N_eff` falls to `3.8e3` at `L = 64`, and the `L = 64` value is the least
reliable in the table. The ridge amplitude is flat-to-mildly-decaying across `L`; **four
lattice sizes with this estimator strain cannot distinguish "constant" from "slowly
decaying"**, and I am not claiming it does.

## 7. THE (b1)/(b2) ADJUDICATION — my dichotomy was too coarse, and it split

I pre-registered two criteria as though they moved together. They do not.

| criterion | result |
|---|---|
| peak locus `→ (T_c, 0)` as `L → ∞` | **YES** — `h*(L) → 0`, `T* → T_c`. **(b1)** |
| peak height grows with `L` | **NO** — flat to mildly decaying. **(b2)** |

So the peak **is** tied to the critical point in its *location* while having a **finite,
non-growing amplitude**. Neither pre-registered branch is right as written; the honest report
is that the dichotomy conflated locus with amplitude, and the data separates them. **K3 did
not fire** (the height does not grow), but my (b2) claim that the effect has "no critical
enhancement" is **wrong** — the peak sits on the critical ridge and is ~90× larger there than
the fixed-field local value.

**K4 FIRED, and stayed fired.** I predicted `star` would carry the largest peak. At the peak —
which lives on the ridge — **separated triples carry ~4× more**, and this is confirmed at
`L = 32`, not just on the small exact lattices. My mechanism was right about the *fixed-field*
regime and wrong about *where the maximum lives*.

## 8. THE ORDINARY MEASURES, on the same distributions

| quantity | maximum over the whole (T,h) plane | where | `I_C^(3)` **there** |
|---|---|---|---|
| multi-information `TC` | **1.386294 = 2 ln 2** | `h = 0`, `T = 0.400` | **0.000e+00** |
| O-information `Ω` | **0.693147 = ln 2** | `h = 0`, `T = 0.400` | **0.000e+00** |
| `I_C^(3)` | 4.7e-03 | ridge: `T ≈ T_c`, `h → 0` with `L` | — |

Both ordinary measures attain their **absolute theoretical maxima** — the exact values
`Core/SignSymmetry.lean` proves for the ferromagnetic state — at a point where the
pairwise-blind quantity is **exactly zero, by a theorem, at machine precision**. They peak in
the ordered zero-field corner; `I_C^(3)` is identically zero along that entire edge.

At `I_C^(3)`'s own peak, order-3 accounts for **1.79 %** of the total multi-information
(`TC = 0.2209`, `I_C^(2) = 0.2170`, `I_C^(3) = 0.00396`). Even at its best, in a model tuned
to favour it, the whole-only share is a ~2 % correction to a pairwise story.

**This is the survey's thesis, inside one model, on one set of samples:** the standard
higher-order instruments are largest exactly where the pairwise-blind quantity is provably
zero, and the two are maximised in different places by a theorem rather than by accident.

## 9. HONESTY LEDGER

- 408 sampled grid points; **105 (26 %) excluded as untrustworthy** by the pre-registered
  criteria (`min_cell·N_eff < 20`, `N_eff < 10³`), plus the ridge caveat in §6.
- Variance-inflation `F`: median 6.3, max 5.5e4. Nominal `N` would have understated the floor
  by that factor.
- `N_eff` over trustworthy points: min 1.6e3, median 2.2e7, max 7.4e7.
- Tied fraction 0 everywhere — **structurally absent**, not verified clean.
- All values reported as excess over the measured floor; raw and floor both printed in the logs.
- A peak was never in doubt and is not reported as a discovery: `I_C^(3) ≥ 0` and vanishes on
  the *entire* boundary of the quadrant (`h=0` by the lemma, `T→∞` by independence, `h→∞` and
  `T→0` by determinism, the corner by `share_ferro`), so an interior maximum is forced. The
  content is the magnitude, the location, and the geometry ordering.

## 10. WHAT THIS DOES AND DOES NOT ESTABLISH

**Does:**
- Confirms the sign-symmetry lemma numerically on a physical model at machine precision, and
  confirms its converse design principle: breaking the symmetry *does* produce nonzero
  order-3 connected information.
- Maps that structure over the (T,h) plane, in two regimes, with magnitudes: **CF 0.66 % of
  `ln 2` on the critical ridge, CF 0.008 % at fixed field.**
- Demonstrates `SPIKE_SURVEY.md`'s thesis inside a single canonical model.
- Yields a correction to the survey's control value and a precision caution on the shared IPF
  machinery.

**Does not:**
- **Nothing about nature.** A spin lattice is a model.
- Nothing about `k > 3`; the lemma's general odd-order form remains unmechanized.
- No priority claim. The survey found no published `I_C^(k≥3)` swept against a control
  parameter; that is "not found", not "does not exist".
- Does not settle whether the ridge amplitude is constant or slowly decaying in `L` — four
  sizes under estimator strain cannot.
- **No promotion to `Stance.lean`.** Any stance change would need a separate refuter pass and
  Eric's review.

## 11. FILES

| | |
|---|---|
| `ISING_FIELD_PREREG.md` | pre-registration, committed at `c67988c` before any code |
| `ising_field.py` | gate, Arm A, Arm B, separation scan |
| `ising_crossarm.py` | kill K5: Monte Carlo vs exact |
| `ising_ridge.py` | finite-size scaling on the critical ridge |
| `ising_analyze.py`, `ising_fss.py` | the pre-registered readouts |
| `ising_exact.json`, `ising_mc_*.json` | raw results |
| `gate.log` (failing), `gate2.log` (passing), `exact.log`, `mc_crossarm.log`, `mcmap.log`, `sep.log`, `ridge.log` | run logs, including the failed gate |
