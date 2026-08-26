# `f` against the existing record — four substrates, parameter-free

**Instrument:** `gcost_confront.py`; raw output `gcost_confront.out`.
**No instrument belonging to another campaign was re-run.** Every measured number is quoted from
a published results file, or read out of the raw JSON that file was written from
(`scratchpad/maintenance_sweep_results.json`). Every predicted number comes from
`GCOST_DERIVATION.md` with **zero fitted parameters**; the only inputs are `q` (the dose, chosen
by the experiment), `δ` (the target, chosen by the experiment) and `λ` (a spectral quantity of the
substrate's own induced chain, read off its own `q = 0` arm or forced by its own noise model).

**The law and the function under test.**

```
G_∞(q) = q / (ε + qλ)                      ε = 1 − λ = per-step loss of the tracked mode of T_c
W*(γ, δ) = (1−δ)γ / (γ + δ(1−γ))           minimum dose holding retention ≥ 1−δ
```

---

## Verdict table

| substrate | mapping | what was compared | result |
|---|---|---|---|
| **atlas 2-bit code** (the kill that motivated this brick) | **defined**, `γ = 1−(1−2ε)²`, `δ = 0.02` | published `W*` at `P(in code) ≥ 0.99` | **4/4 exact to the last published digit** |
| **spatial lattice** (L5, L7, E8) | **defined**, per-mode `λ^{|T|}` | exactly-propagated stationary share, 45 cells | **max relative residual 9.3e−13** |
| **LFSR record** | **defined**, `λ = (1−2ε)³` | T4 retained-fraction table | **15 stationary cells, mean \|resid\| 0.0006, max 0.0021** |
| **Wilson-loop holonomy** | **defined for the scalar reduction; the operator correction is a bound, not a point** | plateau, `q_half`, periodic arm | **3/3 derived sign-and-shape predictions confirmed; `W*` floor holds at 1.152×** |
| **chained erasure** (`CHAINED_RESULTS.md`) | **NOT DEFINED** | — | **not scored** — §5 says exactly what is missing |

---

## 1. Atlas v1 — the table that killed `f(Δ_v)` is priced exactly by `f(γ, δ)`

`ATLAS_V1_RESULTS.md` H1 reports `Δ_v ≡ 0.00000` at every `ε` while `W*` runs 0.794 → 0.970.
`W*` there is *"min `w` such that stationary `P(in code) ≥ 0.99`"* (`atlas_v1.py:81`), searched on
`np.linspace(0,1,2001)`, first grid point that clears the bar.

Mapping, forced not chosen: the view is the parity `a⊕b`; iid flip noise flips it with probability
`2ε(1−ε)`, so the induced two-state chain has `λ = (1−2ε)²` and `γ = 1 − (1−2ε)²`. The ledger's
zero is that chain's own equilibrium (`π₀ = ½`, assumption A2), so `P(in code) ≥ 0.99` is
`G = 2π₀ − 1 ≥ 0.98`, i.e. `δ = 0.02`.

| ε | Δ_v (published) | γ | `f(γ, 0.02)` | on the atlas grid | at 3 dp | published `W*` | match |
|---|---|---|---|---|---|---|---|
| 0.02 | **0.00000** | 0.078400 | 0.793457 | 0.7935 | 0.794 | **0.794** | ✔ |
| 0.05 | **0.00000** | 0.190000 | 0.903007 | 0.9035 | 0.904 | **0.904** | ✔ |
| 0.10 | **0.00000** | 0.360000 | 0.946352 | 0.9465 | 0.947 | **0.947** | ✔ |
| 0.20 | **0.00000** | 0.640000 | 0.969098 | 0.9695 | 0.970 | **0.970** | ✔ |

**4/4 to the last published digit, no free parameter.** The atlas's own conclusion is unchanged
and sharpened: `Δ_v` is identically zero in every row — it *cannot* price `W*` — while the
induced chain's gap prices all four exactly. **The successor named by the kill now has a function
attached, and it lands on the kill's own data.**

Independent confirmation of the mapping, from the numeric check: E8 of `gcost_check.py` solves the
exact 4-state stationary distribution of that chain and finds `G = q/(ε+qλ)` to `1.9e−15` at
16 `(ε, q)` cells.

---

## 2. Spatial lattice — the derived law reproduces the exactly propagated share

`maintenance_sweep_results.json:exact_sweep` carries `share_inf`, the exact population-limit
stationary share of the maintained dynamics. The three standard members were **reconstructed from
their names** (simplex [7,3], extended Hamming [8,4,4], the [5,3] linear code) and the
reconstruction verified against the roster's published dual weight enumerators before use —
all three reproduce `A` exactly.

Prediction, per cell, parameter-free: apply the derived law to **every** Fourier mode,
`p̂_∞(T) = q/(1 − (1−q)λ^{|T|})` with `λ = 1−2ε`, rebuild the distribution, and take its share.
(This is §4.3 of the derivation: the law lives on the amplitude, the published observable is a
nonlinear function of it.)

| substrate | d | cells | max relative residual |
|---|---|---|---|
| L5 (linear [5,3]) | 3 | 15 | 7.7e−13 |
| L7 (simplex [7,3]) | 3 | 15 | 2.7e−13 |
| E8 (ext-Hamming [8,4,4]) | 4 | 15 | 9.3e−13 |

Machine-precision agreement across `ε ∈ {0.02, 0.05, 0.10} × q ∈ {0.01, 0.03, 0.1, 0.3, 1}`,
including the `d = 4` substrate (whose modes decay at `λ⁴`, a different rate from the other two).

**What this is and is not.** It is a re-derivation of P4, not an independent second measurement:
the sweep's own `closed_form_share` field holds the same object, and P4 already reported the
agreement. Its content here is that the constant P4 carried as a measured form is **forced** by
the induced chain's spectrum, and that the multi-mode sum is the correct object — which is also
the derivation of P5b's own falsification (§4.2: retention is a weighted average over modes, so it
*cannot* be a one-parameter family; the sweep's measured single-mode correction factor running
1.02–5.21 across the roster is that spread).

Note the repair here is a **decoder**, not an affine deposit — a state-dependent channel — and the
law still holds exactly. That is E9 of the numeric check in the field: on an exactly-lumpable
structure the two repair models coincide.

---

## 3. LFSR record — 15 stationary cells, residual at the quoting precision

T4 publishes the retained fraction of `ln 2` after 48 steps. Mapping: the tracked component is the
weight-3 parity amplitude, `λ = (1−2ε)³` (this is T3's own closed form,
`share_t = ln2 − H_b((1+λ^{3t})/2)`, read for its decay rate). Prediction: amplitude
`g = q/(ε_c + qλ)`, then `share retention = [ln2 − H_b((1+g)/2)]/ln2`.

**Only the cells the results file itself calls stationary are scored** — `ε ≥ 0.03` at all `q`,
and every `ε` at `q ≥ 0.3` — per its own note that "at ε ≤ 0.01 with small q the 48-step run has
**not** converged".

| | |
|---|---|
| scored cells | **15** |
| mean \|residual\| | **0.0006** |
| max \|residual\| | **0.0021** (ε = 0.03, q = 0.3) |

on a quantity published to four decimals and measured by a 48-step Monte-Carlo run.

**The un-converged cells behave exactly as they should, and that is the check's control.** At
`ε = 0.001, q = 0.001` the residual is **+0.4484** — the measured value is far *above* the
stationary prediction because the trajectory has not finished decaying, precisely where the
results file says it has not. The residual is large where and only where convergence is absent;
scoring those cells would have been a false kill of `f`, and excluding them was pre-committed by
the source, not chosen after seeing them.

**Cost side, derived and confirmed (different currency, stated as such).** T5 measures full-upkeep
cost at `0.010020 / 0.030020 / 0.100017` corrected-bits-per-bit-per-step at `ε = 0.01/0.03/0.10`.
Derivation: at `q = 1` and stationarity the record begins each step at design, the noise flips
each bit with probability `ε`, and the decoder corrects exactly those bits — so the expected
operation count is **exactly `ε`**, confirmed to four digits with the residual (2 parts in 10³ at
ε = 0.01) being mis-decode events. This is the `δ → 0` limit of `f` in **operation count**, not in
work; see §5.

---

## 4. Wilson-loop holonomy — where the scalar `f` is a bound, and it bounds correctly

`λ = 0.959913`, `ε = 0.040087`, both re-derived by that campaign from its own `q = 0` arm (its §2;
these superseded the received `0.9655` and fired the campaign's own pre-registered void).

This is the substrate where assumption **A6 fails**: the ledger entry is a 64×64 operator, so the
deposit and the decayed state can be **misaligned**. §5 of the derivation makes three
parameter-free predictions from the triangle inequality alone, and refuses to fit the misalignment
angle. All three were tested:

| q | measured plateau | `q/(ε+qλ)` | relative residual |
|---|---|---|---|
| 0.01725 | 0.274733 | 0.304526 | **−9.78 %** |
| 0.0345 | 0.434945 | 0.471286 | −7.71 % |
| 0.069 | 0.614427 | 0.648978 | −5.32 % |
| 0.1 | 0.704727 | 0.734871 | −4.10 % |
| 0.2 | 0.842745 | 0.861810 | −2.21 % |
| 0.5 | 0.955226 | 0.961458 | −0.65 % |
| 0.9 | 0.994781 | 0.995566 | −0.08 % |
| 0.99 | 0.999522 | 0.999595 | −0.01 % |

- **(P-i) sign — negative at every `q`: 8/8.** Derived, not observed after the fact: the deposit
  can only add less than its norm unless it is parallel, so `G_operator ≤ G_scalar` in any norm.
- **(P-ii) magnitude monotone decreasing in `q`: true, 8/8 ordered.**
- **(P-iii) residual → 0 as `q → 1`: 0.01 % at `q = 0.99`.**

**The `W*` floor holds, and in the derived direction.** `f(γ, δ=0.5) = 0.038542 = 0.9615 ε`; the
campaign's bisected `q_half = 0.044392 = 1.1074 ε`. **Measured / predicted = 1.152 ≥ 1** — the
operator must *overpay* the scalar rent by 15 %, which is §5's inequality `W*_operator ≥ f(γ,δ)`
and is the same 15 % the campaign reported against its own prereg.

**Second, independent schedule — same signed deficit.** The periodic arm, cycle-averaged, against
the derived `(1−λ^P)/(P(1−λ))` of §4.4:

| q | P | measured (cycle-avg) | derived | rel. residual |
|---|---|---|---|---|
| 0.0345 | 29 | 0.560132 | 0.597581 | −6.27 % |
| 0.069 | 14 | 0.750567 | 0.776958 | −3.40 % |
| 0.1 | 10 | 0.817049 | 0.837602 | −2.45 % |
| 0.3 | 3 | 0.954757 | 0.960449 | −0.59 % |

All negative, magnitude decreasing in `q`. **The misalignment penalty is a property of the
operator, not of the dosing scheme** — which is what §5 requires and what a schedule artifact would
not produce.

**The fit I declined to make, and the data says declining was right.** §5 gives the deficit as
`≈ (1−q)λ(1−cosθ)`. Had I fitted a single misalignment angle, `residual/(1−q)` would be constant.
It is not — it runs −0.0995, −0.0799, −0.0572, −0.0456, −0.0277, −0.0130, −0.0079, −0.0073. The
angle itself moves with `q` (as it must: at `q → 1` the maintained operator *is* the design). The
**FIT-FLAG** in the derivation named this before the numbers were looked at, and a one-angle fit
would have been wrong by a factor of 13 across the grid.

---

## 5. Where the mapping is NOT defined — the chained-erasure substrate

`scratchpad/erasure/CHAINED_RESULTS.md` is in the brief and is **not scored here**, because `f`
has no defined image on it. Stated rather than stretched:

**What C3 measures.** `ΔW(Q4−Q1) = ΔKE`, ratio 1.36 (Basic), 0.607 (OptSingle), −0.081 (OptMulti,
staked below 0.5 and confirmed). This is a **work-vs-incoming-kinetic-energy identity across
quartiles of a bit-erasure protocol**. There is no retention target, no repair-dose axis, and no
tracked component decaying under an induced chain. `f` takes `(γ, δ)` and returns a dose; none of
`γ`, `δ` or the dose exists in C3's design. Forcing a mapping would require inventing at least two
of the three.

**What comes closest, and why it still falls short.** The post-hoc KE-persistence diagnostic gives
`corr(KE_k, KE_{k+m})` = 0.102–0.179 at `m = 1`, ~0 at `m = 2` — a genuine per-step decay of a
tracked component, i.e. a readable `λ ≈ 0.1–0.18` per erasure (consistent with `τ_R = 2.04 ms`
against back-to-back `2t₀` erasures). So **one of the two arguments of `f` is measurable on that
substrate and the other is not**: nothing in the chained design varies a repair dose at a fixed
retention target. The substrate can supply `γ`; it cannot supply a `W*` to compare against.
Also, that diagnostic is explicitly post-hoc grade in its own file, so it could not carry a
rule-6 stake even if the dose axis existed.

**What that substrate is actually needed for — the half of H1′ this brick does not close.**
`f` is a **rate**, not a **work**. Turning `W*` (repair dose per step) into `βW*` (free energy per
step) needs the thermodynamic cost of one repair operation, and the only currency this brick
derives is *operation count* (§3: exactly `ε` corrected bits per bit per step at full upkeep,
confirmed to four digits). The erasure platform is the one place in the repo that measures repair
in **joules per kT**, and it has never been run with a dose axis. **The experiment that would close
H1′'s work half:** the chained-erasure protocol run at partial maintenance — several repair doses
`q` at a fixed retention target — so that `βW*(q)` can be read against `f(γ, δ)` with `γ` taken
from the KE-persistence decay. That is a design, not a result, and it is offered as one.

---

## 6. What would falsify `f`, restated against what has now been measured

The five falsifiers were frozen in `GCOST_DERIVATION.md` §7. Standing after the confrontation:

| falsifier | standing |
|---|---|
| 1. stationary retention ≠ `q/(ε+qλ)` on a finite ergodic quotient with an affine deposit | **not fired** — exact to 1e−13 (spatial), 1e−15 (atlas chain, simulated chains) |
| 2. a measured `W*` strictly **below** `f(γ,δ)` | **not fired** — atlas sits exactly on it (single-mode, aligned, as the derivation requires for equality); holonomy sits 15 % above it, the derived direction; 240 simulated cells, 0 violations |
| 3. an operator-substrate residual with the **wrong sign** | **not fired** — 8/8 negative on the continuous arm, 4/4 on the periodic arm |
| 4. a knee at `q = ε` | **not fired** — now four substrates without one (LFSR T4, lattice P5a, holonomy H2, and the simulated chains, where the alternative reading (a) is run as control E6 and diverges by >100 % as it must) |
| 5. `W*` insensitive to `γ` at fixed `δ` | **not fired** — the atlas row *is* this test: `γ` moves 0.0784 → 0.640 across the four cells and `W*` tracks it to the last published digit while `Δ_v` stays pinned at zero |

**The strongest single line.** The one dataset in the repo that was published as a *refutation* of
"maintenance is priced by a view invariant" — the atlas H1 table — is reproduced to the last
published digit by a two-argument function of the induced chain's spectral gap and the retention
target, with nothing fitted. The kill stands (it killed `f(Δ_v)`, and `Δ_v` is still zero in every
row); its named successor now has the function the kill said must exist.

## 7. Scope lines, carried forward

- `f` is exact only where the tracked component is a **single mode** of `T_c` and a **scalar
  coordinate**. Off single-mode it is a floor (§4.2, checked: 0 violations in 240 cells); off
  scalar it is a floor (§5, checked: the holonomy overpays by 15 %).
- `f` prices the **continuous / stochastic** dose. A **periodic** maintainer holds the same target
  for strictly less mean effort (derived and confirmed exactly, E5; the mechanism is mean age, not
  extra repair). So `f` is the worst-case-schedule rent.
- `f` says nothing about **deterministic quotients** (`γ = 0`), which is atlas B3's finding as a
  scope line: no mixing, no decay, no rent.
- **Lumpability is load-bearing** where the repair is damage-conditional: on a non-lumpable
  partition the law deviates at 4.8e−3 (E10), against 2e−15 on a lumpable one.
- `f` is a **rate**. The work bridge is open (§5).
- Everything here is a property of models and of previously published model measurements.
  Nothing in this file is a claim about nature.
