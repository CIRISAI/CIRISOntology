# RESULTS — the maintenance sweep: what it costs to HOLD whole-only pattern

Pre-registered at **`5d597fe`** (spatial) and **`a8d7491`** (temporal / LFSR addendum), both
frozen *before* the corresponding runs. Construction facts in `design_check.py` and
`lfsr_design_check.py`, committed with the preregs. Scratchpad only; no Lean file,
`Stance.lean` or audit was touched, and `lake` was never run.

---

## SCOPE — read before anything else

**These are DESIGNED substrates. This is a control, not a discovery about nature.** Both
were built to hold whole-only structure: a population on a maximum-share orthogonal-array
support, and an LFSR whose recurrence *is* a three-time parity. That they hold it is not a
result about the world. **Nothing here bears on the `wild-share` open claim, and nothing
here is evidence that any natural system maintains order-3 pattern.**

What is transferable is exactly two things: **the price** of holding the pattern, in bits;
and **what the measurement can and cannot see** — which turned out to be the sharpest
finding in the run and is the one with consequences for the programme's method.

---

## VERDICT

**The congealed-habit corner is reachable, permanently, and the rent is exactly the noise
rate.** On the LFSR the whole-only temporal share sits at `ln 2` — the machine-checked
`k = 3` maximum — and stays there for as long as you pay; unpaid it decays *geometrically*,
which is the shape both fitted families were rejected for on the chaotic lattice. Full
upkeep costs **exactly `ε` corrected bits per recorded bit per step**, and partial upkeep is
strictly *less* efficient per bit of pattern retained.

Three findings that were not asked for and matter more than the confirmations:

1. **The probe geometry the sibling used is blind to this substrate.** A substrate carrying
   the *maximum possible* temporal whole-only share, permanently and deterministically, reads
   **`≤ 1.1 × 10⁻⁶` nats — indistinguishable from zero — on every equally-spaced `(Δ, 2Δ)`
   probe**, while the matched `(5,9)` probe reads `0.693147`. That is a factor of
   **6 × 10⁵**. A null on the equally-spaced grid does not establish absence of temporal
   order-3.
2. **Capacity and persistence are ALIGNED on these substrates, not traded off** — the
   opposite of the "strong xor long-lived" pattern the chaotic lattice showed. Every
   head-to-head at fixed `k` has **zero crossings**: the higher-capacity structure also
   decays more slowly, at every noise level.
3. **Two of my own pre-registered predictions died** (P5b, P11) and one died in a scoped,
   predicted way (P3 on `H8`). All three are reported below as prominently as the survivals.

**τ_share / τ_pair is INFINITE on the LFSR** — the pairwise channel carries no information at
any lag, at any noise level, while the whole-only share is maximal. Against the sibling's
0.087–0.188 (whole dies *first*), this is the first substrate where whole-only pattern
outlives pairwise pattern. **It does so by construction and is reported as a construction,
not a discovery.**

---

## GATES — 7 spatial + 5 temporal, all PASS

Two gates failed on first run and **both failures were bugs in my test code, not in the
substrate**; both are recorded because a gate that is silently "fixed" is not a gate.

| gate | result |
|---|---|
| G1 share machinery | PASS — `array_cap_experiment.gate()` unchanged: k=3 parity → `ln2` exactly, independence → 0, k=5 code state → `2 ln2`, IPF residual 0 |
| G2 structures | PASS — all 10 roster entries exactly pair-uniform (dev `0.00e+00`), `share_max = k·ln2 − ln\|S\|` recovered by the **IPF estimator** to `< 1e−9` |
| G3 Paley `H₁₂` | PASS — `H₁₂H₁₂ᵀ = 12·I` exactly; every column pair shows each symbol pair exactly 3× (direct counting, no Fourier); 12 rows distinct |
| G4 propagator | PASS — Fourier propagation vs brute-force convolution, max dev `6.9e−17` |
| G5 MC ↔ exact | PASS — replica simulator matches the exact distribution within `2.7σ` multinomial |
| G6 floors | PASS — independence: excess `−1.0e−05`, `z = −0.30`; exact code state recovered to `2.8e−04` |
| **G7 decoder** | **PASS after fixing the test.** First run reported `C`-equivariance FALSE for L7/L11/L12/R12. The test compared the *set of decode-target-sets across a sample* instead of checking each `x`. Rewritten to check `dec(x+c) = dec(x)+c` per `x` for every codeword `c`: **all linear substrates pass exactly**, as the translation-invariance argument requires. |
| TG1 LFSR maximality | PASS — period `511 = 2⁹−1` |
| **TG2 clean marginal** | **PASS after fixing the test.** First run asserted the `(5,9)` marginal was *uniform* (`0.125`); it is the **parity** distribution (`0.25` on the four even-parity cells, `0` elsewhere). Corrected assertion: parity distribution exactly, pair deviation `0.0e+00`, share `= 0.693147180560 = ln2` to 12 digits. |
| TG3 decoder | PASS — fixes every codeword; outputs always codewords; codeword histogram uniform (max `z = 3.35`); decoded population reproduces the parity marginal to `4.7e−04` |
| TG4 MC vs closed form | PASS — reported in T3 below |
| TG5 floors | PASS — independent bits excess `9.6e−07` (`z = 0.22`); clean substrate `0.693147177` vs `ln2` |

---

# PART A — THE TEMPORAL ARMS (LFSR). The priority result.

Substrate: `y_t = y_{t−4} ⊕ y_{t−9}`, period `511 = 2⁹−1` verified. `M = 20 000` replicas,
each a 128-bit record; 48 steps; 3 seeds at `ε > 0`. Each step: every recorded bit flipped
with probability `ε`, then with probability `q` the record is decoded to the nearest of the
512 codewords (ties broken uniformly at random). Readout: the sibling's estimator with the
matched pairwise-maxent surrogate null and a shuffle floor; **tied fraction exactly 0** (the
data are already binary, so discipline rule 4 is satisfied trivially and is recorded as
trivial).

**The parity sits at offsets `(b−a, b) = (5, 9)`, not at the tap lags `(4, 9)`** — substituting
the recurrence gives `y_t ⊕ y_{t+5} ⊕ y_{t+9} = 0`. Recorded because the brief said "tap
lags", and the tap lags are not where the structure is.

## T0 — THE PROBE IS BLIND. **CONFIRMED**, and this is the finding with consequences.

Of all 276 lag pairs `(i,j)` with `i < j ≤ 24`, **exactly two carry any share** — `(5,9)` and
`(10,18)` — and both carry **exactly `ln 2`**. That is 0.7 % of the grid. Neither has
`j = 2i`, so the equally-spaced probe misses both.

| arm | `(1,2)` | `(2,4)` | `(3,6)` | `(4,8)` | `(5,10)` | `(6,12)` | `(8,16)` | `(12,24)` | **matched `(5,9)`** |
|---|---|---|---|---|---|---|---|---|---|
| ε=0, q=0 | 2.8e−07 | 1.9e−07 | 1.6e−07 | 2.0e−07 | 5.5e−07 | 3.1e−07 | 3.5e−07 | 2.8e−07 | **0.693147** |
| ε=0.01, q=0 | 4.6e−07 | 2.6e−07 | 2.4e−07 | 3.2e−07 | 4.6e−07 | 2.3e−07 | 2.5e−07 | 4.3e−07 | **0.693147** |
| ε=0.01, q=1 | 8.9e−08 | 6.4e−08 | 1.5e−07 | 8.9e−08 | 1.2e−07 | 2.2e−07 | 8.9e−08 | 2.2e−07 | **0.693147** |
| ε=0.1, q=0.3 | 6.0e−07 | 1.2e−06 | 6.8e−07 | 4.7e−07 | 2.2e−07 | 3.5e−07 | 7.2e−07 | 5.9e−07 | **0.693147** |
| ε=0.03, q=0.1 | 3.7e−07 | 7.1e−07 | 2.6e−07 | 3.5e−07 | 4.2e−07 | 7.3e−07 | 2.5e−07 | 8.8e−07 | **0.693147** |

Worst `|excess|` on **any** equally-spaced probe, any arm, any step: **`1.15e−06` nats**,
i.e. at the estimator floor. The matched probe reads **6.0 × 10⁵ times** that.

**What this licenses, and what it does not.** It licenses one methodological statement:
*a null on the equally-spaced `(Δ, 2Δ)` grid does not establish absence of temporal order-3,
because maximal, permanent order-3 can live entirely off that grid.* It does **not** say the
chaotic lattice had hidden order-3 — that substrate was measured on its own terms and its
null stands on its own terms. What follows for future work is narrower and concrete: a
temporal order-3 hunt should scan the **full lag-pair grid**, not the diagonal.

## T1 — ε = 0 holds `ln 2` forever. **CONFIRMED.**

| probe | excess at t=0 | min over 48 steps | max &#124;excess − ln2&#124; | cap-compliant |
|---|---|---|---|---|
| `(5,9)` | 0.693146857572 | 0.693146720547 | 4.60e−07 | yes |
| `(10,18)` | 0.693146707288 | 0.693146579517 | 6.01e−07 | yes |

Zero decay over the whole run; the residual `~5e−07` is the estimator floor, not drift.
**The congealed-habit corner — pattern both maximal and permanent — is reached. It is
reached because the substrate was built to reach it.**

## T2 — the whole outlives the parts, absolutely. **CONFIRMED, BY CONSTRUCTION.**

Max pairwise mutual information over **every** arm, probe and step: **`1.48e−06` nats** — at
the floor. The pairwise channel carries no information at any lag, at any `ε`, at any `q`,
because bit-flip noise preserves pairwise independence exactly.

| substrate | τ_share / τ_pair |
|---|---|
| chaotic logistic lattice (sibling, `6d8c524`) | **0.087 – 0.188** — whole dies *first* |
| **LFSR (this run)** | **∞** — τ_pair = 0 while τ_share > 0 |

This is the inversion the brief asked to be flagged prominently, and it is flagged with its
caveat attached: **an LFSR is defined by a relation that is invisible to pairs. Getting
`∞` out is getting back what was put in.** The two numbers bracket what is possible; neither
says anything about which one nature resembles.

## T3 — unpaid decay is GEOMETRIC. **CONFIRMED.**

Closed form derived in the addendum §3 before running:
`share_t = ln2 − H_b((1 + λ^{3t})/2)`, `λ = 1 − 2ε`; asymptotically `≈ ½ λ^{6t}`.

| ε | predicted `λ⁶` | measured MC ratio | rel. err | exact-form ratio | live MC points |
|---|---|---|---|---|---|
| 0.001 | 0.988060 | 0.984922 | 0.32 % | — (48 steps too few) | 49 |
| 0.003 | 0.964536 | 0.961034 | 0.36 % | 0.964536 | 49 |
| 0.01 | 0.885842 | 0.884508 | 0.15 % | 0.885842 | 49 |
| 0.03 | 0.689870 | 0.688803 | 0.15 % | 0.689870 | 22 |
| 0.10 | 0.262144 | 0.257415 | 1.80 % | 0.262144 | 6 |

Max `|MC − closed form|` over the whole trajectory: `2.1e−04` to `9.8e−04`. The exact
closed-form ratio equals `λ⁶` to six digits at every resolvable `ε`; the MC ratio matches to
0.15–0.36 % wherever more than a handful of points clear the floor, and the 1.8 % at
`ε = 0.1` is six live points, not a discrepancy in the law.

**This is `unpaid` of `Core/Maintenance.lean` instantiated literally**, with
`γ = 1 − (1−2ε)⁶`. It is also **the exact shape that both pre-registered families were
rejected for on the chaotic lattice** (exponential over-predicting by 6 580 σ, power law by
10 600 σ). The cliff there was the substrate, not the estimator — this run shows the same
estimator reading a clean geometric decay when a geometric decay is present.

## T4 — the rent test. **CONFIRMED; the brief's `q ≥ ε` reading is FALSIFIED.**

Retained fraction of `ln 2` after 48 steps:

| ε \ q | 0 | 0.001 | 0.003 | 0.01 | 0.03 | 0.1 | 0.3 | **1** |
|---|---|---|---|---|---|---|---|---|
| 0.001 | 0.4557 | 0.4632 | 0.4781 | 0.5292 | 0.6434 | 0.8275 | 0.9400 | **1.00000** |
| 0.003 | 0.1319 | 0.1384 | 0.1533 | 0.2085 | 0.3497 | 0.6345 | 0.8573 | **1.00000** |
| 0.01 | 0.0022 | 0.0033 | 0.0060 | 0.0220 | 0.0904 | 0.3330 | 0.6702 | **1.00000** |
| 0.03 | −0.0000 | 0.0000 | 0.0002 | 0.0023 | 0.0169 | 0.1145 | 0.4093 | **1.00000** |
| 0.10 | 0.0000 | 0.0000 | 0.0000 | 0.0003 | 0.0025 | 0.0245 | 0.1627 | **1.00000** |

- **`q = 1` restores `ln 2` exactly at every ε** — full upkeep buys standing still, forever.
- **`q = 0` → 0** at every ε ≥ 0.01 (the ε ≤ 0.003 rows have not finished decaying in 48
  steps; their `q=0` entries are un-converged transient, not a plateau, and the T3 geometric
  rate says where they are going).
- Every intermediate `q` lands strictly between.
- **There is no knee at `q = ε`.** At `q = ε` the substrate retains 46 %, 15 %, 2.2 %, 1.7 %,
  2.4 % as ε rises — a smooth function of `q`, not a threshold, and at the larger ε it holds
  a few percent rather than "holding indefinitely". **The brief's reading is dead on this
  substrate as it was on the spatial one.**

Closed-form stationary check (`g₃ = q/(1−(1−q)λ³)`): agreement is `2.3e−05` to `1.5e−03`
wherever the trajectory has actually reached stationarity (ε ≥ 0.03, all q; and every ε at
q ≥ 0.3). At ε ≤ 0.01 with small q the 48-step run has **not** converged, and those cells
are reported as un-converged rather than as closed-form failures — the free-decay curve at
ε = 0.001 is still at 0.456 of maximum after 48 steps, exactly as `λ⁶ᵗ = 0.988⁴⁸ = 0.56`
predicts.

## T5 / deliverable (d) — THE MAINTENANCE COST, in bits

Cost measured as **corrected bits per recorded bit per step** — the physical operations the
maintainer must perform.

| ε | q | retained | **cost (bits/bit/step)** | cost per bit of share held |
|---|---|---|---|---|
| 0.01 | 0.003 | 0.006 | 0.000529 | 0.0878 |
| 0.01 | 0.03 | 0.090 | 0.003859 | 0.0427 |
| 0.01 | 0.3 | 0.670 | 0.009135 | 0.0136 |
| **0.01** | **1** | **1.000** | **0.010020** | **0.0100** |
| 0.03 | 0.03 | 0.017 | 0.007449 | 0.4421 |
| 0.03 | 0.3 | 0.409 | 0.025267 | 0.0617 |
| **0.03** | **1** | **1.000** | **0.030020** | **0.0300** |
| 0.10 | 0.1 | 0.024 | 0.029345 | 1.1983 |
| 0.10 | 0.3 | 0.163 | 0.063979 | 0.3931 |
| **0.10** | **1** | **1.000** | **0.100017** | **0.1000** |

**The rent for perfect maintenance is exactly the noise rate.** At full upkeep the cost is
`0.010020`, `0.030020`, `0.100017` at ε = 0.01, 0.03, 0.10 — i.e. `ε` corrected bits per
recorded bit per step, to four digits. Nothing is saved and nothing is wasted: you repair
precisely what rotted.

**And underpaying is inefficient, not merely insufficient.** The last column — bits spent per
bit of pattern retained — is *minimised at `q = 1`* and rises monotonically as `q` falls: at
ε = 0.03 it goes 0.030 → 0.062 → 0.147 → 0.442 → 1.26 → 4.67 → 13.7 as `q` drops from 1 to
0.001. Partial maintenance buys pattern at up to **460× the marginal price** of full
maintenance. That is the sharpest quantitative content of "rent" this run produced.

---

# PART B — THE SPATIAL ARMS

10 substrates, exact population-limit propagation over the full `2^k` distribution
(`k ≤ 12`), `ε ∈ {0.005…0.2} × q ∈ {0…1}` = 480 cells, 400 steps each; plus a Monte-Carlo
arm at `M = 500 000` replicas × 5 seeds with the sibling-matched floors.

| id | k | structure | \|S\| | `share_max` | /ln2 | d |
|---|---|---|---|---|---|---|
| L5 | 5 | linear [5,3] | 8 | 1.386294 | 2.0000 | 3 |
| L7 | 7 | simplex [7,3] | 8 | 2.772589 | 4.0000 | 3 |
| **E8** | 8 | ext-Hamming [8,4,4] | 16 | 2.772589 | 4.0000 | **4** |
| **H8** | 8 | **Hadamard-12 OA** | **12** | **3.060271** | 4.4150 | 3 |
| H9 / H10 / H11 | 9/10/11 | Hadamard-12 OA | 12 | 3.753 / 4.447 / 5.140 | — | 3 |
| L11 / L12 | 11/12 | best m=4 linear | 16 | 4.852 / 5.545 | 7 / 8 | 3 |
| R12 | 12 | m=5 affine hyperplane | 32 | 4.852030 | 7.0000 | **4** |

## P1, P2 — pair-uniformity and the decay law. **BOTH CONFIRMED.**

Free decay is exactly geometric with ratio `λ^{2d}`, where `d` is the lowest nonzero Fourier
weight (= dual distance for a linear code): **0 of 60 cells deviate by more than 1 %**, and
most agree to 4 decimal places (e.g. L5 at ε=0.05: measured 0.53132 vs predicted 0.53144).
`d = 4` structures decay *faster* than `d = 3` ones — noise is a low-pass filter on Fourier
weight, so higher-order structure is the more fragile.

## P3 — full upkeep holds `share_max`. **HOLDS on 9 of 10. FAILS on `H8` — RC-A fires.**

| substrate | gap from `share_max` at `q = 1` (worst ε) | verdict |
|---|---|---|
| L5, L7, E8, H9, H10, H11, L11, L12, R12 | `≤ 2.2e−12` | **HOLDS (exact)** |
| **H8** (Hadamard-12 at k=8) | **4.03e−03 nats** | **FAILS** |

This is the pre-registered kill **RC-A**, firing exactly where the addendum said it would
fire and nowhere else, and it is the Task-2 result. See Part C.

## P4 — the closed form for the stationary state. **CONFIRMED.**

`p̂_∞(T) = p̂_0(T)·q/(1−(1−q)λ^{|T|})` reproduces the exact stationary share on every linear
substrate; approach is monotone from `share_max` down to a level strictly between 0 and
`share_max` for every `0 < q < 1`.

## P5 — splits: **P5a CONFIRMED, P5b FALSIFIED (my own prediction).**

**P5a — no threshold at `q = ε`: CONFIRMED**, decisively. Retention at `q/ε` = 0.25, 0.5, 1,
2, 4 runs 0.31 %, 1.1 %, 3.3 %, 8.9 %, 20.4 % (L7, ε = 0.02) — a smooth curve through
`q = ε`, where the substrate holds ~3 %, not "indefinitely". The brief's reading is dead on
both substrates.

**P5b — retention collapses onto `ρ = q/(2εd)` as `(ρ/(1+ρ))²`: FALSIFIED.** The spread
*within* a `ρ` bin is as large as the trend across bins (e.g. at `ρ ∈ [0.3,1)`: retained
`0.333 ± 0.293`), and the predicted values are wrong by factors of 1.5–4. **The diagnosis is
mine to own:** I dropped the amplitude prefactor when converting from share to *fraction of*
share, and I kept only the `w = d` Fourier mode. The correct second-order form is
`share_∞ ≈ ½ Σ_w A_w g_w²` over the whole weight spectrum, which reproduces the exact
stationary share to **0.25 %** when `share_∞ < 1e−5` and degrades as the share grows (as a
small-share expansion must). The single-mode correction factor
`C = Σ_w A_w (d/w)² / A_d` ranges from **1.02** (E8) to **5.21** (L12) across the roster —
so retention is *not* a one-parameter family, and cannot be.

## P6 — the cost identity and inequality. **CONFIRMED.**

`cost_erase ≥ rent` holds in every cell, with equality **only** at `q = 1`:

| substrate | ε | held at | `q*` | cost_erase | rent | **cost/rent** |
|---|---|---|---|---|---|---|
| L5 | 0.05 | 100 % | 1.000 | 0.765657 | 0.765657 | **1.000** |
| L5 | 0.05 | 45 % | 0.415 | 0.443708 | 0.304256 | 1.458 |
| L5 | 0.05 | 6 % | 0.091 | 0.122256 | 0.041870 | 2.920 |
| L5 | 0.20 | 3.7 % | 0.163 | 0.225279 | 0.048715 | **4.624** |
| L7 | 0.01 | 48 % | 0.120 | 0.189138 | 0.138882 | 1.362 |
| L12 | 0.05 | 34 % | 0.237 | 1.045 | 0.778 | 1.343 |

**The bill exceeds the damage by up to 4.6×**, and the gap is the entropy of not knowing
which replicas were corrected — the same "partial maintenance is inefficient" fact the LFSR
cost table shows from the other side.

## P7 / P8 — capacity and persistence are ALIGNED. **BOTH CONFIRMED, zero crossings.**

| fixed k | higher capacity | comparator | crossings, ε = 0.02 / 0.05 / 0.10 |
|---|---|---|---|
| 8 | **H8** (3.0603, d=3) | E8 (2.7726, d=4) | **0 / 0 / 0** |
| 11 | **H11** (5.1397, d=3) | L11 (4.8520, d=3) | **0 / 0 / 0** |
| 12 | **L12** (5.5452, d=3) | R12 (4.8520, d=4) | **0 / 0 / 0** |

In every pair the higher-capacity structure is also the slower-decaying one, at every step
and every noise level. **This is the direct opposite of the chaotic lattice, where strength
and persistence were never simultaneously available (congealed-habit corner: 0 of 70 grid
points).** On designed maximum-share supports the two axes are not in tension.

## P9, P10, P11 — the drift arms. **P9 confirmed (trivially); P10 and P11 FALSIFIED.**

**P9 — automorphism drift is exactly share-neutral: CONFIRMED**, max `|Δshare| = 4.4e−16`
over the 1–60 automorphisms found per substrate. (Those counts come from a bounded random
search plus, for linear codes, the guaranteed translations — they are **not** automorphism
group orders, and nothing is inferred from them.) Pre-registered as a triviality and reported as one:
an automorphism maps the state to itself.

**P10 — scramble collapses share to near zero: FALSIFIED.** A random bijection of `{0,1}^k`
keeps entropy at exactly `ln|S|` (confirmed) but leaves a **large** share residue:

| substrate | L7 | H11 | L12 | L5 | H8 | L11 | E8 | R12 |
|---|---|---|---|---|---|---|---|---|
| share after scramble, % of max | 10.6 % | 5.2 % | 20.4 % | 22.4 % | 24.2 % | 35.8 % | 49.1 % | **71.9 %** |

The prediction said "near zero"; the truth is 5–72 %, with large scatter. The honest reading:
**a random small support in a large cube genuinely carries order-3 structure** — these are
exact distributions, so this is real structure, not estimator bias. What is special about a
code is not that it *has* whole-only share but that its share is *maximal* and
*maintainable*. This is a useful warning against over-reading a nonzero share.

**P11 — upkeep pointed at the wrong structure fails: FALSIFIED.** Drifting the structure by
a random coordinate permutation while decoding to the *original* support still holds most of
the share (L7: 2.718 of 2.773; E8: 2.773 of 2.773 — exactly full; L12: 5.094 of 5.545;
H8: 2.823 of 3.060), against 0.000 with no upkeep at all. **Why the prediction was wrong:**
a coordinate permutation of a code is *another code of the same quality*, so decoding to the
original still lands the population uniformly on a maximum-share support. Maintenance does
not require knowing *which* pattern — only *a* pattern of the right kind. That is a more
interesting fact than the one I predicted.

## Monte-Carlo arm — the instrument reads the exact curve

384 (substrate × ε × q × t) cells, `M = 500 000`, 5 seeds, matched pairwise-maxent surrogate
null (n=40) + shuffle floor (n=10), cap-compliance checked in every cell:
**median `|MC excess − exact share| = 2.6e−04`, max `4.1e−03`** (worst at `L12`, `k = 12`,
where 4096 cells at `M = 500 000` gives the largest estimator bias). Tied fraction exactly 0
throughout.

---

# PART C — TASK 2: THE EXCEPTIONAL STRUCTURE AT 12

## The M12 fact — VERIFIED against primary sources, with a correction to the brief

> "This analysis is due to Marshall Hall [1]. He showed that there is, up to equivalence, a
> unique Hadamard matrix `H` of order 12. Moreover, if `G = Aut(H)`, and `Z` is the central
> subgroup generated by `(−I, −I)`, then `G/Z` is isomorphic to the sporadic simple group
> `M12` (the Mathieu group), and has its two **5-transitive** representations on the rows and
> columns."
> — **P. J. Cameron**, *Hadamard matrices*, Encyclopaedia of Design Theory, 31 July 2002, §3.
> [1] = **M. Hall, Jr., *Note on the Mathieu group M₁₂*, Arch. Math. 13 (1962), 334–340.**

Second, independent source: **P. Ó Catháin**, *Group actions on Hadamard matrices*, MSc
thesis, NUI Galway — "Its automorphism group is the Schur cover of `M12` which has order
**190,080**."

**Correction to the brief:** the brief attributes this to "Soicher, designtheory.org". The
encyclopaedia PDF I fetched and read is signed **Peter J. Cameron**, and the result is
**Hall 1962**. The credit line should read *Hall 1962, via Cameron's encyclopaedia entry*.
Hall's paper itself was not opened; it is cited as quoted by Cameron.

## The 5-transitivity does NOT survive column deletion — and that is the finding

5-transitivity on the rows means the automorphism group of the **full 11-column** array is
row-transitive, which forces a nearest-point decoder to return the **uniform** distribution
on the 12 rows. Restricting to `k < 11` columns keeps only the setwise stabiliser of the
chosen columns, and the addendum pre-registered that the guarantee might lapse. **It lapses,
at exactly one value of `k`:**

| k | row distance profiles | Voronoi cell masses | decoder returns uniform? |
|---|---|---|---|
| 11 | 1 class: every row at distance 6 from all 11 others | 12 × 170.667 (= 2¹¹/12) | **yes**, to 1.2e−16 |
| 10 | 1 class: {5:6, 6:5} | 12 × 85.333 | **yes**, to 1.1e−16 |
| 9 | 1 class: {4:3, 5:6, 6:2} | 12 × 42.667 | **yes**, to 5.6e−17 |
| **8** | **2 classes: 8 rows {3:1,4:6,5:3,6:1}, 4 rows {3:2,4:3,5:6}** | **8 × 20.625 + 4 × 22.75** | **NO — dev 2.5e−03** |

At `k = 11` the 12 rows are equidistant (all pairwise distances 6). As columns are deleted
the distance spectrum spreads — {5,6} at k=10, {4,5,6} at k=9 — and at **k = 8** it splits the
rows into two orbits of 8 and 4, which no automorphism can connect. The decoder's Voronoi
cells then have unequal mass (8 × 20.625 + 4 × 22.75 = 256 = 2⁸), so decoding returns a
**non-uniform** distribution on the support.

**The consequence is a real maintenance failure, not a cosmetic one.** Under full upkeep at
ε = 0.05, `H8` settles at share `3.059123` against `share_max = 3.060271` — short by
`1.148e−03` nats — and, more tellingly, the state is **pushed off the pair-uniform polytope
entirely** (pair deviation `1.8e−02`, so the IPF estimator is required where every other
substrate stays exactly pair-uniform). The gap grows with noise: `1.4e−07`, `6.5e−06`,
`1.5e−04`, `1.1e−03`, `2.6e−03`, `4.0e−03` at ε = 0.005 … 0.2.

(The approach to this stationary level is slow: the gap reads `6.7e−04` at 60 steps,
`1.130e−03` at 200 and `1.148e−03` at 400. The 400-step figure is the converged one and is
what the table above reports — an earlier 60-step spot-check of mine was transient and is
recorded here so the two numbers are not mistaken for a disagreement.)

## Does the exceptional maximizer maintain share BETTER, WORSE, or the same?

**Both, and the two answers are about different things — which is why the question needed
splitting:**

- **Under free decay: BETTER.** `H8` beats `E8` at every step and every noise level (zero
  crossings), because its lowest Fourier weight is 3 against E8's 4, so it decays as `λ⁶`
  rather than `λ⁸`. Same at k = 11 against `L11`. The exceptional maximizer is both
  higher-capacity and slower-decaying.
- **Under maintenance: WORSE, and uniquely so.** `H8` is the **only** substrate in the
  roster of ten whose decoder is not equivariant, and therefore the only one where full
  upkeep cannot restore the maximum. Every linear code gets equivariance free from
  translation invariance; the Hadamard array has to earn it from its automorphism group, and
  at `k = 8` the group is not big enough.

So the exceptional symmetry buys **capacity and noise-robustness**, and costs **maintainability**
— but only in the window where column deletion has broken the row orbit, which is `k = 8`
alone. At `k = 9, 10, 11` the exceptional maximizer is strictly better on every axis measured.

---

## WHAT IS NOT CLAIMED

1. **No claim about nature.** Both substrates were designed to obey the rent clause. Their
   obeying it is not evidence that anything in the world does. **`wild-share` is untouched.**
2. **T1 and T2 are constructions, not discoveries**, and are labelled so wherever they appear.
   An LFSR was built to satisfy a three-time parity invisible to pairs; recovering `ln 2` and
   `τ_share/τ_pair = ∞` is recovering the design.
3. **No world-claim from the rent clause, and no refutation of it.**
   `Core/Maintenance.lean` is a theorem about a model. **One honest structural mismatch,
   pre-registered in advance and confirmed:** the decay side matches the Lean model literally
   (`unpaid`, geometric, `γ = 1 − (1−2ε)^{2d}`), but the payment side does **not** — the
   substrate's payment is proportional to the share *deficit* (`cost_erase = q·(share_max −
   share_pre)`), not to the amount, so `rent_holds`'s `α = γ·S` is instantiated only in the
   weak sense that *some* payment holds the amount steady.
4. **No claim that the congealed-habit corner is reachable in general.** Reaching it here is
   the definition of the substrate, not a discovery. The transferable content is the price.
5. **No novelty claim on the classical maximum.** That is Gavinsky–Pudlák 2016 / Babai 2013 /
   Lancaster 1965 (`HADAMARD_CONNECTION.md` §B.5). This run uses those objects; it does not
   re-derive or re-claim them. m-sequence properties are textbook (Golomb).
6. **T0 is a statement about our instrument, not about the world.** It does **not** say the
   chaotic lattice had hidden order-3.
7. **No quantum content anywhere. Nothing here is mechanized**, and no result is offered for
   the audit.

## LIMITATIONS

- The LFSR run is 48 steps; at ε ≤ 0.003 the free decay has not converged, so those `q = 0`
  cells are transient, not stationary, and are marked as such rather than compared to the
  stationary closed form.
- The MC estimator floor is `~1e−06` nats; T0's "blindness" is a statement at that floor, not
  a proof of exact zero — though the *exact* construction check in `lfsr_design_check.py`
  does give exactly `0.000000000` on the equally-spaced grid.
- One trinomial recurrence (`4, 9`) and one record length (128) were run; the comb's sparsity
  was scanned only to lag 24.
- `H8`'s equivariance failure is established for the nearest-point decoder with uniform
  tie-breaking. A cleverer decoder might restore uniformity; that was not tested.

## FILES

- `scratchpad/MAINTENANCE_SWEEP_PREREG.md` — frozen at `5d597fe`
- `scratchpad/MAINTENANCE_SWEEP_PREREG_ADDENDUM.md` — frozen at `a8d7491`
- `scratchpad/design_check.py`, `lfsr_design_check.py` — construction facts, committed with the preregs
- `scratchpad/maintenance_sweep.py`, `lfsr_sweep.py` — the runs
- `scratchpad/maintenance_report.py`, `lfsr_report.py` — adjudication (read-only)
- `scratchpad/maintenance_sweep_results.json`, `lfsr_results.json`, `exact_arm_results.json` — raw
- `scratchpad/maintenance_report.txt`, `lfsr_report.txt` — full tables

Primary seed 20260725; spatial MC across {20260725, 99, 7, 1337, 4242}, LFSR across the
first three. Research → scratchpad memo → Eric's review. Nothing pushed.
