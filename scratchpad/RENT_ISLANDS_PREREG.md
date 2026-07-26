# PRE-REGISTRATION — islands of cheapness: does rent/nat sawtooth at the magic sizes?

**Frozen and committed BEFORE `rent_islands.py` exists and before any rent number at
`k > 12` is computed.** Results will go to `scratchpad/RENT_ISLANDS_RESULTS.md`.

Scratchpad only. No Lean file, no `Stance.lean`, no audit, no `lake`. Nothing pushed.

Parent pre-registration: `MAINTENANCE_SWEEP_PREREG.md` (commit `5d597fe`). This file
extends it to larger `k` and changes exactly one thing about the instrument (§5).

---

## 0. SCOPE, AND THE ONE ANALOGY THAT MUST NOT BE MISREAD

**Same scope as the parent.** The substrates below are **designed** to obey the rent clause.
This is a **control, not a discovery about nature**. It measures the *price* of holding
whole-only structure in an engineered system, not its prevalence anywhere. Nothing here
bears on the `wild-share` open claim, and nothing here is evidence that any natural system
maintains order-3 pattern.

**The "island of stability" language is an ANALOGY and is used only as a name.** The nuclear
"island of stability" is a claim about nuclear shell structure — magic proton and neutron
numbers, spin-orbit coupling, fission barriers. **Nothing of that kind is present here and
none of it is being claimed.** The only thing shared is an abstract shape:

> *discrete existence constraints create non-monotone stability landscapes.*

That is the whole of the resemblance. There is **no shared mechanism**, no nuclear physics
anywhere in this run, and no inference in either direction is licensed. If the sawtooth is
found, the correct statement is "the combinatorial existence constraint `4 | N` makes the
capacity ceiling a step function, and the cost inherits the steps" — **not** "habit has magic
numbers like nuclei do". Anyone quoting this must carry this paragraph with it.

---

## 1. WHAT WAS COMPUTED BEFORE THIS FILE WAS WRITTEN — full disclosure

Predictions below are **derived**, not guessed, and a derived prediction is only honest if
the derivation is on the record first.

### 1.1 Inherited structure theory (siblings; not re-derived here)

- The maximum whole-only share on `k` slots with uniform pair marginals is attained by the
  uniform distribution on a **minimum-size strength-2 binary orthogonal array**, and
  `maxshare(k) = k·ln2 − ln N₀(k)` with `N₀(k) = 4⌈(k+1)/4⌉` wherever the Hadamard matrix of
  that order exists (`HAMMING_FORM_SCAN.md`, `HADAMARD_CONNECTION.md`, `CLASSICAL_MAX_K5.md`).
- **This maximum is NOT ours** — Gavinsky–Pudlák 2016 (Thms 3.1/3.2/4.1), conjectured by
  Babai 2013, extending Lancaster 1965; the OA↔Hadamard equivalence is Hedayat–Sloane–Stufken
  1999 Thm 7.5. Our residue is only the sharpening at `k ≢ 3 (mod 4)`. **No novelty is
  claimed here for any of it**, and this run uses those objects rather than re-deriving them.
- The k ≤ 12 rent measurements: `maintenance_sweep_results.json`, `RENT_COMPARISON.md`.

### 1.2 Construction facts, computed by me before writing this file

`scratchpad/rent_islands_design_check.py` → `rent_islands_design_check.json`, committed with
this file. **No dynamics was run and no maintenance quantity was computed.** Every Hadamard
matrix was verified `H Hᵀ = N·I` exactly, and every substrate was verified strength-2 by
**direct combination counting** on its rows (each of the four symbol pairs exactly `|S|/4`
times in every column pair) — the Fourier-free route.

| order | construction | verified |
|---|---|---|
| 8, 16 | Sylvester | ✓ |
| 12, 20, 24 | Paley type I (`q` = 11, 19, 23) | ✓ |
| 28 | Paley type II (`q` = 13) | ✓ |

**The density ceiling `maxshare(k)/k`, which is the whole basis of the prediction:**

| k | 5 | 6 | **7** | *8* | 9 | 10 | **11** | *12* | 13 | 14 | **15** | *16* | 17 | 18 | **19** | *20* | 21 | 22 | **23** | *24* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `N₀` | 8 | 8 | 8 | 12 | 12 | 12 | 12 | 16 | 16 | 16 | 16 | 20 | 20 | 20 | 20 | 24 | 24 | 24 | 24 | 28 |
| density | .2773 | .3466 | **.3961** | *.3825* | .4170 | .4447 | **.4672** | *.4621* | .4799 | .4951 | **.5083** | *.5059* | .5169 | .5267 | **.5355** | *.5342* | .5418 | .5487 | **.5550** | *.5543* |

Bold = `k ≡ 3 (mod 4)`, where the density peaks. Italic = the four `k` at which the density
**falls** relative to `k−1`. This is arithmetic, not a measurement: `N₀` is constant on runs
of four and steps by 4 at `k ≡ 0 (mod 4)`, so `ln2 − ln N₀(k)/k` rises within a run and drops
at each step. **The sawtooth in the CEILING is a fact. Whether the COST inherits it is the
open question this run answers.**

Predicted relative size of each tooth, `Δdensity/density ≈ ln(1 + 4/N₀)/(k·density)`:
**3.4 % at k=8, 1.1 % at 12, 0.47 % at 16, 0.23 % at 20, 0.12 % at 24.** The teeth shrink
like ~`1/k²`. This matters: the late teeth are small enough that structure-specific
differences between one Hadamard matrix and another could swamp them, and that possibility is
pre-registered here rather than discovered later.

### 1.3 The hint already in the k ≤ 12 table — disclosed, because it is why this is being run

I read `maintenance_sweep_results.json` before writing this file. Recomputing
`cost_erase/share_held` from it: the two step points inside the old range are `k=8` and
`k=12`, and **rent/nat ticks UP at both, at all four matched conditions (8/8)**:

| condition | L7 (k=7) | H8 (k=8) | H11 (k=11) | L12 (k=12) |
|---|---|---|---|---|
| ε=.01, frac .1 | 0.2151 | **0.2168 ↑** | 0.1677 | **0.1708 ↑** |
| ε=.01, frac .5 | 0.1424 | **0.1472 ↑** | 0.1190 | **0.1208 ↑** |
| ε=.05, frac .1 | 0.9356 | **0.9702 ↑** | 0.8040 | **0.8138 ↑** |
| ε=.05, frac .5 | 0.6615 | **0.6816 ↑** | 0.5408 | **0.5473 ↑** |

**This is a hint, not a result, and it is confounded** — the old controller did not land on
its stated target (achieved fractions ranged 0.28–0.48 for "frac = 0.5"), and rent/nat depends
on the level actually held. So the 8/8 could be an artifact of which structure happened to
settle higher. **`k=8` and `k=12` are therefore IN-SAMPLE and are re-measured on the fixed
instrument as a confirmatory check only. The out-of-sample predictions are `k = 16, 20, 24`,
and they carry the weight.** I am not permitted to count 8 and 12 as evidence twice.

---

## 2. THE PREDICTION

### P-ISLAND (primary, out-of-sample)

> **Rent per nat is not smooth in `k`. It falls within each run of four and ticks UP at every
> `k ≡ 0 (mod 4)`, so `k ≡ 3 (mod 4)` — 7, 11, 15, 19, 23 — are local minima: islands of
> cheapness at the Hadamard-attained sizes.**

Operationalised as **20 binary events**: for each step point `k₀ ∈ {8, 12, 16, 20, 24}` and
each of the four matched conditions, the event `rent/nat(k₀) > rent/nat(k₀−1)` on **ARM A**.

| outcome | verdict |
|---|---|
| ≥ 18 / 20 upticks, **including ≥ 5/8 of the out-of-sample events at k = 16, 20** | **P-ISLAND CONFIRMED** |
| ≤ 2 / 20 upticks | **P-ISLAND DEAD** — rent/nat is monotone in `k`; the magic structure is irrelevant to cost |
| anything between | **MIXED** — reported as mixed, with the pattern of which teeth appear; no rescue, no post-hoc subsetting |

**A smooth, island-free decline is a fully acceptable outcome and will be reported as the
death of a pretty hypothesis, not rescued.** So will a plateau.

### P-DENSITY (mechanism, secondary, separable)

> The `k`-dependence of rent/nat is **mediated by the density ceiling** `maxshare(k)/k`:
> plotting rent/nat against density (not against `k`) collapses the sawtooth into a single
> monotone decreasing curve, and the observed tooth amplitudes track the predicted
> 3.4 / 1.1 / 0.47 / 0.23 / 0.12 % pattern of §1.2.

*Falsifier:* rent/nat non-monotone in density, or the `k ≡ 3 (mod 4)` points sitting
systematically off the curve traced by the other residues, or tooth amplitudes not decaying.
**P-DENSITY can die while P-ISLAND lives** (the islands would then be real but caused by
something other than packing density) and vice versa.

### P-DISSOCIATION (the sharp mechanism test — this is the strongest thing in the file)

ARM A's size function is `N₀(k) = 4⌈(k+1)/4⌉` (steps at `k ≡ 0 mod 4`). ARM B's is
`2^⌈log₂(k+1)⌉` (steps at `k = 8, 16` only, in this range). **The two arms therefore predict
islands at DIFFERENT `k`, and the difference is fixed by arithmetic before any run:**

| k | 8 | 12 | 16 | 20 | 24 |
|---|---|---|---|---|---|
| ARM A ceiling steps down? | yes | **yes** | yes | **yes** | yes |
| ARM B ceiling steps down? | yes | **no** | yes | **no** | no |

> **P-DISSOCIATION: each arm ticks up at its OWN step points and not at the other's.**
> In particular ARM B must show **no** uptick at `k = 12` or `k = 20`, where ARM A must.

*Falsifier:* both arms ticking at the same `k` regardless of their own size functions (that
would mean a `k`-effect, not a structure effect), or neither tracking its own steps.
This is what makes the run a test of *packing* rather than a test of *slot count*.

*Disclosed confound:* the ARM B selection rule (maximise dual distance `d`, then minimum
distance — inherited unchanged from the parent prereg) happens to return `d = 4` at exactly
`k = 8` and `k = 16`, and `d = 3` everywhere else. Since higher `d` decays **faster**
(parent §3.2), ARM B's upticks at 8 and 16 are confounded with `d`. **A `d = 3`-constrained
ARM B′ is therefore run at `k = 8` and `k = 16` to separate them.** Recorded now, not later.

### P-PERFECT (the `k = 15` double-magic disambiguation)

`k = 15` is doubly special: Hadamard-attained (`N₀ = 16`) **and** a perfect-code length. But
the two arms **cannot** separate this, and the reason is a construction fact from §1.2 that
must be stated up front rather than discovered mid-run:

> **At `k = 12…15`, ARM A and ARM B are the SAME OBJECT.** The Sylvester Hadamard OA of order
> 16 *is* the simplex code `[15,4]`, the dual of the perfect Hamming code, and `2^⌈log₂16⌉ =
> N₀ = 16`. The same coincidence holds at `k = 5…7` (both are the `[7,3]` simplex, order-8
> Sylvester). The arms genuinely differ only at `k = 8…11` and `k = 16…24`.

So the disambiguation is done against a third arm: **ARM C = the three binary perfect codes**,
Hamming `[7,4]`, Hamming `[15,11]`, Golay `[23,12,7]` — one at each of three island `k`.
Perfect codes have covering radius exactly `t` and **no decoder ties**: upkeep is maximally
efficient in bits physically flipped.

> **P-PERFECT: the perfect-code property is NOT the cheapness mechanism. ARM C will be
> substantially MORE expensive per nat than ARM A at the same `k`, because it is far less
> dense** (density 0.297 / 0.185 / 0.332 vs 0.396 / 0.508 / 0.555 at k = 7 / 15 / 23).
> It should nonetheless **win on the flips currency** `cost_flips/nat`, where its tie-free
> radius-`t` decoder is optimal.

*Falsifier:* ARM C cheaper per nat than ARM A at any of the three `k` — which would make
perfect covering, not density, the mechanism, and would make `k = 15` and `k = 23` doubly
magic for two different reasons. *Second falsifier, separate:* ARM C not winning on flips.

### P-PLATEAU (the scale-economy question)

Fit rent/nat vs `k` on ARM A, **within the measured range only, no extrapolation**, to three
pre-registered forms: power decline `a·k^{−b}`, decline-to-floor `c + a·e^{−bk}`, and linear
`a + bk` (control). Report AIC and the fitted floor `c` with its range of support.

> **P-PLATEAU: within `k = 5…24` the decline does not exhaust — the decline-to-floor fit
> either prefers `c ≈ 0` or its `c` is not resolvable from the data.**

*Falsifier:* decline-to-floor decisively preferred with a floor `c` bounded away from zero.
**Either answer is reported. No `k > 24` claim is made in either case**, and the fitted `c`
is never quoted as "the price of habit" — it is a curve parameter over `5 ≤ k ≤ 24`.

---

## 3. THE SUBSTRATES

Identical dynamics to the parent (§2 there): drift (identity for this run) → per-bit flip
noise `N(ε)` → upkeep `U(q)`, each replica independently with probability `q` replaced by the
nearest point of `S` (ties uniform). Measured after upkeep.

| arm | rule | `k` | `\|S\|` |
|---|---|---|---|
| **A — MAXSHARE** | the minimum-size OA: `H_{N₀(k)}` normalised, first column dropped, truncated to `k` columns | 5…24 | `N₀(k)` = 8,12,16,20,24,28 |
| **B — POWER-OF-TWO** | best linear code with `m = ⌈log₂(k+1)⌉`; columns maximise dual distance then min distance (exhaustive where `C(2^m−1,k) ≤ 2·10⁴`, else the canonical affine-first list) | 5…24 | `2^m` = 8,16,32 |
| **B′ — d-MATCHED** | as B but constrained to `d = 3`, run only at the two `k` where B's rule returns `d = 4` | 8, 16 | 16, 32 |
| **C — PERFECT** | Hamming `[7,4]`, Hamming `[15,11]`, Golay `[23,12,7]` | 7, 15, 23 | 16, 2048, 4096 |

All verified pair-uniform by direct counting (§1.2). **ARM A has `d = 3` at every `k`** —
so free-decay rate is identical across the whole of the primary arm, and any rent/nat
difference within ARM A is about capacity, not about decay speed. This is checked, not
assumed, and recorded per row.

---

## 4. CONDITIONS

`ε ∈ {0.01, 0.05}` × target `∈ {0.1, 0.5}` of `share_max`. **ε = 0.20 and frac = 1.0 are
excluded by design** — the parent flagged both as controller-artifact regimes
(`RENT_COMPARISON.md` caveats 1–2), and frac = 1.0 is a genuine boundary (it requires `q = 1`
exactly). Excluded before any number is seen, not after.

**Pre-registered secondary: the absolute-level condition.** Fixed-fraction matching lets the
absolute nats held grow with `k`. Also measured: hold **exactly 1.0 nat** (feasible for every
`k ≥ 5`) at both `ε`. If the frac-matched and abs-matched readings disagree in their verdict
on P-ISLAND, **that disagreement is itself the finding** and both are reported; the
frac-matched reading is primary, for continuity with the k ≤ 12 table.

---

## 5. THE INSTRUMENT — the one thing changed from the parent, and why

The parent's controller settled by free decay until `share ≤ target`, then held whatever
value it had landed on. Two consequences, both visible in `maintenance_sweep_results.json`:
it overshot (achieved 0.28–0.48 where 0.50 was asked), and it could saturate. Since rent/nat
depends on the level held, **the old rent/nat comparison across structures is confounded by
which structure overshot least.**

**Replacement — the fixed-point definition, which removes both artifacts by construction:**

> The rent at level `s` is the **constant** `q*` whose stationary state has share exactly `s`.

Found by bisection on `q ∈ (0,1)`. It is the same object the parent's controller was
converging to — at its fixed point `q_t → q*` and the state → the stationary state of that
constant `q` — but it is defined at the fixed point instead of approached from a transient.

For a decoder that returns exactly uniform-on-`S`, the stationary state is closed-form
(parent §3.3): `p̂_∞(T) = g_{|T|}·p̂₀(T)`, `g_w = q/(1 − (1−q)λ^w)`, `λ = 1−2ε`, `g_0 = 1`.
This is `O(N log N)` per evaluation and is what makes `k = 24` reachable.

- `share_∞ = k·ln2 − H(p_∞)` — exact, because pair-uniformity is preserved (parent §3.1).
- `share_pre = k·ln2 − H(noise(p_∞))`.
- **rent** `= cost_erase = q*·(share_max − share_pre)` nats erased per replica per step.
- **rent/nat** `= cost_erase / s` — the currency, unchanged from `RENT_COMPARISON.md`.
- secondary: `cost_flips = q*·Σ_x p_pre(x)·dist(x, S)` bits physically flipped.

**Hygiene, reported per row without exception:**
1. **achieved fraction** `share_∞(q*)/share_max` and its residual from target — a row whose
   residual exceeds `10⁻⁶` relative is **DROPPED, not adjusted**;
2. **no saturation** — `q*` strictly inside `(10⁻⁹, 1−10⁻⁹)`; a row at either rail is DROPPED;
3. **monotonicity of `share_∞(q)`** verified on a grid before bisecting, so the root is unique;
4. the closed form is **verified against direct iteration of the exact step map** at every
   structure (gate G5); where it fails, that structure is measured by iteration instead and
   **flagged in the results table**.

The parent's controller is additionally re-run unchanged at `k = 11, 12` and compared, so the
change of instrument is documented as a number, not asserted.

---

## 6. GATES — all must PASS before any measurement is read

| gate | what it establishes |
|---|---|
| **G1** | `array_cap_experiment.gate()` passes unchanged (the shared share machinery) |
| **G2** | every substrate exactly pair-uniform (`A₁ = A₂ = 0 < 1e−12`) and `share_max = k·ln2 − ln\|S\|` to 12 digits; for `k ≤ 11` also via the independent IPF estimator |
| **G3** | every Hadamard order used verified `H Hᵀ = N·I` exactly, **and** strength 2 by direct combination counting on the rows — no Fourier |
| **G4** | the Fourier noise propagator reproduces brute-force convolution of the full `2^k` distribution to `< 1e−12` |
| **G5** | **closed-form stationary state == direct iteration of the exact step map** (500 steps) to `< 1e−10` in share, at every structure and several `q` — this is the decoder-equivariance test, and it is what licenses the fast path |
| **G6** | `share_∞(q)` is strictly increasing in `q` on a 200-point grid, with `share_∞(0⁺) → 0` and `share_∞(1) = share_max` |
| **G7** | the decoder fixes `S` pointwise; `dec#(uniform(S) ⊛ noise)` uniform on `S` to `< 1e−12` |
| **G8** | GPU and CPU paths agree to `< 1e−12` on every quantity, at every `k` where both are affordable |

A failed gate stops the run; it is not worked around. If **G5 or G7 fails on the Paley-20 /
24 / 28 arms** — a live possibility, since the parent showed column-truncation destroys the
row-transitivity that guarantees equivariance — that is a *result*, reported as "the
larger exceptional structures are lossy to maintain in a way the small ones are not", and
those rows are then measured by iteration.

---

## 7. WHAT WILL NOT BE CLAIMED

1. **No claim about nature.** Designed substrate; a control. `wild-share` untouched.
2. **No novelty on the classical maximum, on Hadamard/OA theory, or on any of the three
   perfect codes.** All are long-published; see §1.1 for the credit line.
3. **No nuclear physics.** §0 governs. The word "island" is a label for a shape in a plot.
4. **No extrapolation beyond `k = 24`.** No claim about `k → ∞`, no "asymptotic cost of
   habit", and the fitted floor `c` of P-PLATEAU is a curve parameter over the measured range
   and nothing more.
5. **No world-claim from the rent clause and no refutation of it.** `Core/Maintenance.lean`
   is a theorem about a model. The parent's structural mismatch (§3.6 there — payment here is
   proportional to the *deficit*, not to the *amount*) stands unchanged and is restated in the
   results.
6. **Nothing here is mechanized.** No Lean file is touched; no result is offered to the audit.
7. **`k ≡ 3 (mod 4)` being "magic" is a statement about orthogonal-array existence**, i.e.
   about when `4 | N` and the Rao bound `N ≥ k+1` can be met simultaneously. It is
   arithmetic. It is not a claim that these slot counts are special in any physical system.

---

Frozen. `rent_islands_design_check.py` / `.json` are committed with this file as the record of
exactly what was computed before it.
