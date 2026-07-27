# PRE-REGISTRATION — the restorability boundary, and whether rent/nat has a floor

**Frozen and committed BEFORE `rent_scaling.py` exists, before any automorphism group in the
`rent_islands` roster is computed, and before any rent number at `k > 24` is computed.**
Results will go to `scratchpad/RENT_SCALING_RESULTS.md`.

Scratchpad only. No Lean file, no `Stance.lean`, no audit, no `lake`. Nothing pushed.

Parents: `MAINTENANCE_SWEEP_PREREG.md` (`5d597fe`) → `RENT_ISLANDS_PREREG.md` (`19f80c6`) →
`RENT_ISLANDS_RESULTS.md`. Their scope paragraph (§0 of each) is inherited verbatim and is
restated in §0 below. This file asks two questions the parents left standing.

---

## 0. SCOPE — inherited unchanged, and it governs everything below

**Designed substrates. A control, not a discovery about nature.** Everything measured here is
the *price* of holding whole-only structure in an engineered system, and the *algebra* of when
that structure can be restored. Nothing bears on the `wild-share` open claim. Nothing here is
evidence that any natural system maintains order-3 pattern.

**No nuclear physics.** The parent's "island of stability" is a name for a shape in a plot and
carries no shared mechanism. It is not re-used as an argument here.

**`Core/Maintenance.lean` is a theorem about a model.** The parent's structural mismatch stands
unchanged: payment on this substrate is proportional to the *deficit*, not to the *amount*, so
the substrate instantiates `unpaid` / `unpaid_decays` literally and `rent_holds` only in the
weaker sense that some payment holds the amount steady. Nothing below is offered as support
for, or refutation of, the Lean.

**Ceiling fractions, per the standing requirement.** Every share reading is quoted as a
fraction of `share_max(k) = k·ln2 − ln N₀(k)` — the substrate's own attained maximum. The
machine-checked cap in force at these `k` is `Core/HammingCap.shareK_le_of_four_pair_uniform`,
`(k−3)·ln2`, whose four-pair-uniform hypothesis these substrates satisfy exactly. Since
`share_max(k) ≤ (k−3)·ln2` ⟺ `N₀ ≥ 8`, which holds at every `k ≥ 5` in range, **`share_max` is
the tighter denominator and is the one quoted**; the fraction against the Lean cap is tabulated
alongside so the two are never confused. `Core/ThirdCap.lean`'s `log 2` and its per-orientation
`share_le_grouping_gaps` are `k = 3` results and **do not apply here**; they are not used and
must not be imported into this table.

---

## 1. FULL DISCLOSURE — everything already computed, before this file was written

A derived prediction is only honest if the derivation is on the record first, and an
out-of-sample claim is only honest if the in-sample part is named.

### 1.1 On record for Q1 (restorability)

- `rent_islands_results.json` already carries, for every substrate in that roster, the exact
  decode-weight profile deviation `profile_dev`, the equivariance flag, the measured
  `equiv_dev`, `Hc_deficit`, and `ceiling_frac`. **I have read all of them.** The split is:
  EQUIVARIANT at `k` = 5, 6, 7, 9, 10, 11, 12–15, 23; LOSSY at `k` = 8, 16–22, 24, with
  `profile_dev` separating `≤ 3.3e−15` from `≥ 1.8e−4`.
- `aut_counts_exact.json` already carries exact automorphism orders for the *k ≤ 12
  maintenance-sweep* roster: `H8` 48, `H9` 144, `H10` 720, `H11` 7920 (the Mathieu stabiliser
  chain), `L5` 64, `L7` 1344, `E8` 21504, `L11` 768, `L12` 9216, `R12` 73728. `H8`–`H11` are
  the same objects as `A8`–`A11` here.
- **`RENT_COMPARISON.md`'s correction block already states the hypothesis this file tests, and
  states it from `k = 8`:** "by k=8 the surviving M8 has orbits 8+4 on the 12 rows, the
  decoder's cells go unequal, and full upkeep can no longer restore the maximum." **`k = 8` is
  therefore IN-SAMPLE. It is where the hypothesis was generated and it cannot be counted as
  evidence for it.** The out-of-sample content of Q1 is every other truncation — in particular
  the whole Paley-20, Paley-24 and Paley-II-28 ladders (`k` = 16–24), which are exactly where
  the split is currently unexplained.
- No automorphism group of any `k ≥ 13` structure has been computed. No orbit structure of any
  structure in this roster has been computed. No level set of `R_i(a)` has been computed.

### 1.2 On record for Q2 (scaling)

- The entire `k = 5…24` rent table (`rent_islands_results.json`, 270 rows) is on record and I
  have read it. **All of `k ≤ 24` is IN-SAMPLE for Q2.** The out-of-sample points are
  `k = 25…31`.
- The parent's P-PLATEAU verdict is on record: power decline wins by AIC at 3 of 4 conditions;
  the fitted floor `c` lands at 94.5–97.4 % of the smallest measured rent/nat in *every*
  condition — the signature of an unidentifiable parameter. Q2 exists because the parent said
  the floor was not identifiable **in that range**, and named the extension as the way to find
  out.
- The parent could not trend-correct `k = 24` because `k = 25, 26, 27` were never run
  (`RENT_ISLANDS_RESULTS.md` §7, limitation 3). Running them is part of Q2.

### 1.3 Arithmetic, not measurement — computed before this file, no dynamics run

`N₀(k) = 4⌈(k+1)/4⌉` and the density ceiling `share_max(k)/k = ln2 − ln N₀(k)/k`, extended past
the parent's table. This is arithmetic; it is the *prediction*, not a result.

| k | 24 | 25 | 26 | **27** | *28* | 29 | 30 | **31** | *32* | … | **35** | *36* |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| `N₀` | 28 | 28 | 28 | 28 | 32 | 32 | 32 | 32 | 36 | | 36 | 40 |
| density | .55431 | .55986 | .56499 | **.56973** | *.56937* | .57364 | .57762 | **.58135** | *.58116* | | **.59076** | *.59068* |
| step drop | +0.120 % | | | | **+0.063 %** | | | | +0.032 % | | | +0.014 % |

Bold = `k ≡ 3 (mod 4)`, the Hadamard-attained sizes. Italic = the `k` where the ceiling falls.
**The predicted tooth at `k = 28` is 0.063 %** — half the size of `k = 24`'s, which the parent
already called "at the edge of resolution". This is stated now, before the run, so that a null
at `k = 28` is read as the predicted difficulty and not as a surprise.

### 1.4 Feasibility, computed before this file — a resource fact, not a result

Constructions wired in `rent_islands_design_check.py`: Sylvester `2^n`; Paley-I for `N−1` prime
`≡ 3 (mod 4)`; Paley-II for `N/2−1` prime `≡ 1 (mod 4)`. Hence `N₀ = 28` (Paley-II q=13),
`32` (Sylvester), `36` (Paley-II q=17) exist; **`N₀ = 40` is not wired** by any of the three.

The exact solvers cost: `2^(k−m)` for a linear substrate (quotient route over the dual) and
`2^k` for a non-linear OA (full route). Measured WHT time on this box: 2.5 s at `2^23`, 11 s at
`2^25`, 23 s at `2^26`. Therefore:

| block | `k` | route | cost | verdict |
|---|---|---|---|---|
| Paley-II-28 | 25, 26, 27 | full `2^k` | `2^27` worst | **reachable** (memory-lean solver required) |
| Sylvester-32 | 28…31 | quotient `2^(k−5)` | `2^26` worst | **reachable** |
| Paley-II-36 | 32…35 | full `2^k` | `2^35` | **OUT OF REACH** — 34 G states |

**`k = 31` is the declared ceiling of this campaign, and the reason is the `2^k` barrier at the
next non-linear Hadamard order, not a choice made after seeing a curve.** The Hadamard-attained
size `k = 35` named in the brief is unreachable and is not attempted.

---

## 2. QUESTION 1 — is the restorability boundary exactly algebraic?

### 2.1 The two criteria, and the connection between them (stated before the run)

**The G7 criterion (the sibling's, inherited).** With `W_{x,i}` the uniform-tie-break
nearest-point decode weight of `x` onto support point `i`, and
`R_i(a) = Σ_x W_{x,i} · #{j : |x ⊕ s_j| = a}`, the deposit under *any* radial kernel `κ` is

  `dec#(uniform(S) ⊛ κ)_i = (1/|S|) · Σ_a κ(a) · R_i(a)`,

so **full upkeep returns the design state for every radial noise kernel iff `R_i(a)` does not
depend on `i`.** Exact, threshold-light, and `ε`-free.

**The group criterion (this file's hypothesis).** `Aut(S) = {(σ,c) : σ(S) ⊕ c = S}` — the
subgroup of the Hamming cube's isometry group `Z₂^k ⋊ S_k` stabilising the support.

**The connection, which is an elementary argument and is not a discovery:** if `g ∈ Aut(S)`
sends `s_i ↦ s_{π(i)}`, then `g` is an isometry with `g(S) = S`, so nearest-point sets and tie
multiplicities transport, `W_{g(x),π(i)} = W_{x,i}`, and the inner count is unchanged. Hence

> **`R_i(a)` is constant on `Aut(S)`-orbits of the support.**

Two immediate consequences, both stated **before** any group is computed:

- **(T) TRANSITIVE ⟹ EQUIVARIANT.** This is a theorem, not a prediction. A violation is a bug
  in one of the two instruments, and will be treated as one.
- Every **linear** substrate is transitive (translation by any codeword is an automorphism),
  hence equivariant. This explains the Sylvester and code arms with no computation, and it is
  why the interesting split lives inside the non-linear Paley family. Also not a discovery —
  `RENT_ISLANDS_RESULTS.md` §0.1 already says the linear ones are equivariant "for a separate
  and already-known reason".

### 2.2 The hypothesis, and why it is a real bet

> **H-IFF: full upkeep restores the design state IFF `Aut(S)` acts transitively on the
> support.** Sufficiency is (T). **The claim under test is NECESSITY: equivariant ⟹
> transitive.**

**This is a bet against a well-populated prior, and it is stated as one.** Combinatorial
regularity routinely fails to imply group transitivity — distance-regular graphs that are not
distance-transitive, and 2-designs with trivial automorphism groups, exist in abundance. So the
design-theory prior says an intransitive-but-equivariant structure should exist somewhere. The
question this run answers is **whether one exists inside the Hadamard family at `k ≤ 31`**, and
if so, where the characterisation first breaks. **A falsification is the expected outcome under
the prior, is a full result, and will be reported as the death of the "exactly algebraic"
reading.**

| outcome | verdict |
|---|---|
| every equivariant structure transitive **and** every lossy structure intransitive, across the whole out-of-sample roster (`k` = 9–24 non-linear, plus every truncation of every wired order) | **H-IFF CONFIRMED** — the restorability boundary is exactly the orbit boundary |
| ≥ 1 intransitive structure with `profile_dev` at the float64 floor | **H-IFF DEAD in the necessity direction.** Transitivity remains sufficient (T); the characterisation is one-way, and the counterexample is named and described |
| ≥ 1 transitive structure with `profile_dev` above the floor | **INSTRUMENT FAULT** — (T) is a theorem. The run stops and the bug is found before anything is read |

### 2.3 The sharper hypothesis, separable from H-IFF

> **H-ORBIT: the level-set partition of the support induced by `R_i(·)` equals the `Aut(S)`-orbit
> partition, structure by structure.**

Orbits always refine level sets by (T); H-ORBIT says there is no accidental coincidence of
profile values across distinct orbits. *Falsifier:* any structure where a level set is a strict
union of two or more orbits. **H-ORBIT can die while H-IFF lives** (accidental degeneracy does
not create restorability) and, less obviously, H-IFF can die while H-ORBIT lives on every
structure where both are defined. They are reported separately.

**Pre-registered in-sample check:** `RENT_COMPARISON.md` predicts orbits `8 + 4` on the 12 rows
at `k = 8`. That prediction is on record and is verified here as a *dye test of the new
instrument*, not as evidence for H-IFF.

### 2.4 The ceiling, for every lossy case

For every structure, measured and tabulated regardless of verdict:

- the **attainable ceiling fraction** `share_∞(q = 1) / share_max` — what fraction of the
  design state's whole-only share full upkeep can actually hold, at each `ε`;
- the **deposit deficit** `ln|S| − H(c*)` at `q = 1`, which is zero exactly when the deposit is
  uniform on `S` and is the noise-free-est available measure of the failure;
- the **restorability distance** `TV(p_∞(q=1), uniform(S)) = ½ Σ_i |c*_i − 1/|S||`.

> **H-CEILING: among lossy structures the ceiling deficit is a function of the orbit
> structure** — specifically, it is monotone in the orbit-size imbalance
> `I = 1 − |S|⁻²·Σ_orbits |O|²`·(normalisation stated in the code), with **larger imbalance ⇒
> larger deficit**. Operationalised as a Spearman rank correlation between `I` and the deposit
> deficit `ln|S| − H(c*)` at `ε = 0.05`, across all lossy structures in the roster.

*Reporting rule, fixed now:* the lossy population is small (currently 9 structures at `k ≤ 24`)
and **a rank correlation on ≤ 12 points is quoted with its exact permutation p-value and with
the number of points, never as a σ.** There is no stochastic null in this campaign anywhere
else; here the null is the exact permutation distribution over orbit-imbalance labels, and its
shape is a discrete distribution enumerated in full, not sampled. *Falsifier:* correlation of
the wrong sign, or a p-value above 0.05 with the sign right (reported as UNRESOLVED at this
sample size, which is the honest reading of a 9-point test).

### 2.5 The Q1 roster — fixed now, no selection after any result

Every wired Hadamard order `N ∈ {8, 12, 16, 20, 24, 28, 32}`, and **every truncation width**
`k = 3 … N−1` of each — the full ladder, not only the widths `ARM A` happens to use. Plus every
linear substrate in the `rent_islands` roster (`ARM B`, `B′`, `C`) as the transitivity control.
Orbits and exact group orders are computed for the whole ladder. The `R_i(a)` criterion is
computed exactly wherever `2^k` is affordable; **the affordability cut is declared in the
results as a number, and every structure past it is marked PREDICTED-not-verified, never
counted as a confirmation.**

---

## 3. QUESTION 2 — does rent/nat plateau?

### 3.1 The extension

`ARM A` (the minimum-size OA, the primary arm of the parent) at `k = 25, 26, 27` (Paley-II-28,
non-linear, full route) and `k = 28…31` (Sylvester-32, linear, quotient route). `ARM B` (best
linear `[k, ⌈log₂(k+1)⌉]` code) at `k = 25…31` — where `m = 5` throughout, so **`ARM B`'s size
function does not step anywhere in this window while `ARM A`'s steps at `k = 28`.** That is a
free out-of-sample extension of the parent's strongest result and is pre-registered as one
(§3.4).

Conditions unchanged from the parent: `ε ∈ {0.01, 0.05}` × target `∈ {0.1·share_max,
0.5·share_max, 1.0 nat}` = 6 conditions. `ε = 0.20` and `frac = 1.0` remain excluded, for the
reasons the parent gave, before any number is seen.

**There are no error bars because there is no sampling.** The brief anticipated reduced replica
counts and widened bars; that does not apply — the instrument is a population-limit fixed-point
solver with no Monte Carlo anywhere. The honest error budget is numerical, and is reported per
row exactly as the parent did: target residual (row DROPPED, not adjusted, above `1e−6`
relative), `q*` off both rails, mass deviation, negative-mass check, and the `O(leak²)` residual
on non-equivariant substrates.

### 3.2 The fits — forms and outcome rules, fixed before any point at `k > 24` exists

Fit `ln(rent/nat)` against `k` on `ARM A` over **all** measured `k` (`5 … 31`), at each of the
6 conditions independently, to four pre-registered forms:

| | form | free |
|---|---|---|
| F1 | power `a·k^{−b}` | 2 |
| F2 | power-to-floor `c + a·k^{−b}` | 3 |
| F3 | exponential-to-floor `c + a·e^{−bk}` | 3 |
| F4 | linear `a + b·k` (control) | 2 |

Compared by AIC in the Gaussian-SSE form `AIC = n·ln(SSE/n) + 2p`. **This is descriptive model
comparison on exact data, not statistical inference, and is labelled as such.**

**Floor identifiability, operationalised now.** Profile the floor: `[c_lo, c_hi]` is the set of
`c` whose best refit satisfies `SSE(c) ≤ SSE_min · exp(4/n)` (i.e. `ΔAIC ≤ 4`). Then

| verdict | rule (must hold in **≥ 4 of the 6** conditions) |
|---|---|
| **PLATEAU-WITH-FLOOR** | F2 or F3 beats F1 by `ΔAIC ≥ 4`, **and** `c_lo > 0`, **and** `c_hi < 0.98 × min(measured rent/nat)` |
| **CONTINUED DECLINE** | F1 wins on AIC, **or** the profile interval `[c_lo, c_hi]` contains 0 |
| **SAWTOOTH-DOMINATED** | after the best smooth fit, `mean residual at k ≡ 0 (mod 4) − mean residual at k ≡ 3 (mod 4)` exceeds the RMS residual of that fit |
| **MIXED** | anything else — reported as mixed, no post-hoc subsetting, no rescue |

The third clause of PLATEAU-WITH-FLOOR is the parent's own diagnosis turned into a rule: a
floor pinned at the last data point is an unidentifiable parameter, and it will not be reported
as a floor no matter how well it fits.

> **A floor, if it is resolved, is still a curve parameter over `5 ≤ k ≤ 31` and is never
> quoted as "the price of habit" or as an asymptotic cost. No `k > 31` claim is made in either
> direction.** This clause is inherited from the parent and is not weakened by having more
> points.

### 3.3 The step at `k = 28` — out-of-sample, and small by prediction

6 binary events, one per condition: `rent/nat(28) > rent/nat(27)` on `ARM A`. Predicted UP by
the density-ceiling account, with predicted amplitude **0.063 %** (§1.3).

**Trend-corrected reading, and it is the one that carries the weight** — the parent's §7(a)
statistic, which `k = 24` could not receive because `k = 25, 26, 27` were missing: the step's
log-jump minus the mean log-jump within the run of four that follows it. Both `k = 24` and
`k = 28` become correctable here. Predicted: positive residual at both, of order the negative
of the ceiling's own trend-corrected tooth, with elasticity in the 1–1.5 band the parent
measured at `k ≤ 20`. *Falsifier:* trend-corrected residual negative at both step points, or
elasticity outside `[0.3, 3]` at both.

### 3.4 The dissociation, extended out-of-sample

`ARM A` steps at `k = 28`; `ARM B` (m = 5 throughout `k = 25…31`) steps nowhere in the window.

> **H-DISSOC-2: `ARM A` ticks up at `k = 28` in ≥ 4 of 6 conditions and `ARM B` in ≤ 1 of 6.**

*Falsifier:* both arms tick (a `k`-effect, not a packing effect), or neither. Note in advance:
`ARM A` and `ARM B` are the **same object at `k = 31`** (the full Sylvester-32 OA *is* the
simplex `[31,5]`), and may coincide at `k = 28…30` as well; the arms differ genuinely only at
`k = 25, 26, 27`, where `ARM A` has `|S| = 28` and `ARM B` has `|S| = 32`. **Whether they
coincide is a construction fact, checked and reported, not a result.**

---

## 4. INSTRUMENTS AND GATES — all must PASS before any measurement is read

**Q1 instrument.** Exact automorphism order **without enumeration**, so that the answer is a
group order and not a saturated search count — the failure that forced `RENT_COMPARISON.md`'s
correction. Translating so `0 ∈ S`, `|Aut(S)| = |P| · |C|` where `P = {σ ∈ S_k : σ(S) = S}` and
`C = {c ∈ S : ∃σ, σ(S) = S ⊕ c}` is the orbit of `0`; `|P|` comes from a stabiliser chain,
`|P| = Π_t |orbit of t under the pointwise stabiliser of 0…t−1|`, each orbit membership decided
by a **single-solution** backtracking search with prefix row-multiset pruning. Orbits on the
support come from the same search: `s_i ~ s_j` iff some coordinate permutation carries
`S ⊕ s_i` onto `S ⊕ s_j`.

**Search caps, declared per the harvest gate.** Each single-solution search carries a node
budget of `2·10⁷`. A search that exhausts its budget returns **UNDETERMINED**, never a count
and never a decision; the structure is then excluded from the primary tally, with that
exclusion stated in the results table. No number in this campaign is a saturated search result.

| gate | what it establishes |
|---|---|
| **Q1-G1** | the new exact-order instrument reproduces all ten enumerated orders in `aut_counts_exact.json` (`H8` 48 … `R12` 73728) |
| **Q1-G2** | `|Aut|` divisible by `|C|`, `|C|` = size of the orbit of `0`, orbit partition consistent under composition (closure spot-check on random found elements) |
| **Q1-G3** | the dye test: on planted structures with known groups — a linear code (transitive, `|Aut| = |PAut|·|S|`), the full cube, and a deliberately broken support with an isolated point — the instrument returns the known answers |
| **Q1-G4** | `R_i(a)` recomputed here matches `rent_islands.py`'s stored `profile_dev` at every shared structure to `< 1e−12` |
| **Q1-G5** | (T) holds on every structure computed: no transitive structure has `profile_dev` above the float64 floor |
| **Q2-G1** | the lean solver reproduces `rent_islands_results.json` rows at `k = 20…24`, every quantity, to `< 1e−10` relative |
| **Q2-G2** | the faster WHT matches the parent's WHT bit-for-bit within `1e−13` relative at `2^20…2^24` |
| **Q2-G3** | `share_∞(q)` strictly increasing on a grid at every new `k`, so the root is unique |
| **Q2-G4** | every new substrate exactly pair-uniform and `share_max = k·ln2 − ln|S|` to 12 digits; every Hadamard order used verified `H Hᵀ = N·I` and strength 2 by direct combination counting |
| **Q2-G5** | closed-form/quotient stationary state versus direct iteration of the exact step map at every new linear substrate |

A failed gate stops the run; it is not worked around. **Box discipline:** this box is shared
with three other running campaigns. CPU only, no GPU, worker pool capped at 4, memory budget
capped at 6 GB resident for this campaign, and the cap is stated again in the results with what
was actually used.

**No z-scores appear in this campaign.** The instrument is exact and there is no sampling null
to shape — the harvest gate "null-shape before z" is satisfied vacuously and is recorded as
such rather than silently skipped. The single place a null appears at all is H-CEILING's rank
correlation, whose null is the exact permutation distribution, enumerated rather than sampled
(§2.4).

---

## 5. WHAT WILL NOT BE CLAIMED

1. **No claim about nature.** Designed substrates; a control. `wild-share` untouched.
2. **No novelty** on the classical maximum (Gavinsky–Pudlák 2016, conj. Babai 2013, ext.
   Lancaster 1965), on the OA↔Hadamard equivalence (Hedayat–Sloane–Stufken 1999 Thm 7.5), on
   the Mathieu groups, on Paley or Sylvester constructions, or on the perfect codes. The
   observation that `R` is constant on `Aut`-orbits is elementary and is claimed as elementary.
   A prior-art sweep for "when does a nearest-point decoder fix the uniform measure on a code"
   — the coding-theory phrase is likely *completely regular* / *completely transitive* codes,
   Delsarte 1973 and Solé — **is run before the results are written, and whatever it finds is
   reported in the results whether or not it pre-empts H-IFF.**
3. **No extrapolation beyond `k = 31`.** No `k → ∞` claim, no asymptotic cost of habit, and any
   fitted floor is a curve parameter over the measured range.
4. **Nothing is mechanized.** No Lean file is touched; no result is offered to the audit. If
   H-IFF survives, the correct next step is a Lean brick, and saying so is not the same as
   having one.
5. **No promotion.** Nothing here reaches `Stance.lean` in this campaign.
6. **A null on either question is a full result** and will be reported at the same volume as a
   confirmation, with the dead prediction kept in the record and marked dead.

---

Frozen. `rent_scaling.py` does not yet exist.

---

## AMENDMENT 1 (2026-07-27) — the column-order control, added before any amended number

**Status when written:** `rent_scaling_aut.py` exists and its four gates PASS
(`rent_scaling_aut_gate.log`). **No Q1 sweep has been run.** The only automorphism numbers
seen are the ten in `aut_counts_exact.json` (already disclosed in §1.1), the gate's four
planted dye cases, and — disclosed here — the exact order of the canonical Paley-20
truncation at `k = 16`, which came back as **1** during a cost benchmark before this
amendment was written. That structure is hereby **in-sample alongside `k = 8`** and is
excluded from the confirmation tally. **No random-subset structure has been evaluated in any
way.**

**Why this is needed.** §2.5 fixes the roster as "every truncation width", and every
truncation in the parents is the **first `k` columns** of the normalised array. For a
non-linear array the column order is arbitrary. As registered, a CONFIRMED H-IFF would
strictly speaking be a fact about `rent_islands_design_check.py`'s column ordering, not about
supports. §5's "what will not be claimed" does not cover this and it should.

> **H-SUBSET (added to the primary roster, out-of-sample in full).** For every wired order
> `N ∈ {12, 20, 24, 28}` and every width `k` with `6 ≤ k ≤ min(N−1, 20)`, draw **5 random
> `k`-column subsets** with `numpy.random.default_rng(20260727)`, all draws made before any
> is evaluated. H-IFF and H-ORBIT must hold on each. These count toward the out-of-sample
> tally on the same terms as the canonical truncations.

| outcome | meaning |
|---|---|
| H-IFF holds on canonical **and** random subsets | the characterisation is a fact about the support, not about a column order |
| H-IFF holds on canonical, **fails** on ≥ 1 random subset | **that is the primary result of Q1** and is reported as the headline: the canonical ladder is unrepresentative, and every equivariance statement in `RENT_ISLANDS_RESULTS.md` §0.1 is a statement about one column ordering |
| H-IFF fails on both | H-IFF is simply dead; the subset arm adds nothing and is reported as concordant |

The Sylvester orders are excluded from H-SUBSET because every truncation of a linear array is
linear, hence transitive, hence equivariant by theorem (T) — there is nothing to test and
their inclusion would inflate the tally. Stated now, not after counting.

---

## AMENDMENT 2 (2026-07-27) — ARM B at k = 32, declared before the point is computed

**Status when written:** Q2's instrument is built and gated (`rent_scaling_q2_gate.log`,
Q2-G1 reproduces `rent_islands` at k = 20…24 to ≤ 2.3e−14 relative) and the sibling's run is
in flight over `A/B 25…31`. **No k = 32 point exists, and none has been computed.**

**Why the declared ceiling does not bind here.** §1.4 named `k = 31` the campaign ceiling, and
its reason is explicitly ARM A's: the next ARM A size is `N₀ = 36`, a **non-linear** Paley-II
order whose exact route is a `2³⁶` object. That argument says nothing about ARM B. **ARM B at
`k = 32` is a linear `[32, 6]` code**, so it takes the quotient route over its dual with
`r = k − m = 32 − 6 = 26` — `2²⁶` states, **the same cost class as `B31`, which is running
now** (0.54 GB per array; measured, not estimated). The ceiling was correct for the arm it was
about and over-broad for this one.

**Why it is worth the point.** `k = 32` is where ARM B's own size function steps (`|S|`: 32 →
64). §4.3's staked prediction P-STEP32 has **no data at all** as the campaign stands, and it
is the *largest* forward-testable tooth in the whole study — a **3.125 % raw density drop**
against A28's 0.063 %, roughly 50×. Leaving it unrun means the campaign stakes its biggest
prediction and then declines to test it.

**A sharp feature of this particular step, arithmetic and noted before the run:**

> `share_max(B31) = 31·ln2 − ln32 = 18.021827` and
> `share_max(B32) = 32·ln2 − ln64 = 18.021827` — **exactly equal.**

So at `k = 32` ARM B holds the *same total whole-only share* spread over *one more slot*, with
per-slot density dropping 0.581349 → 0.563182. The step is therefore unusually clean: nothing
about the amount of pattern held changes, only the packing.

### Predictions, staked now

**The trend-correction convention, pinned before any data — and a self-correction.** The
parent's §7a statistic is the step's log-jump minus the mean log-jump of the run that follows
it. **There is no run after `k = 32`** — the campaign stops there and ARM B's next step is at
`k = 64` — so the baseline must be the run *before*, which is what this amendment named when
it specified `k = 29, 30, 31`. That is not a compromise here: **ARM B has no step anywhere in
`k = 17…31`**, so those log-jumps are pure trend (`L(29) = +0.00747`, `L(30) = +0.00692`,
`L(31) = +0.00643`), a cleaner baseline than the parent had at any of its own steps.

Writing `L(k) = ln(rent/nat)(k) − ln(rent/nat)(k−1)`, the statistic is

> `tooth(32) = L(32) − mean(L(29), L(30), L(31))`.

Under that convention the ceiling's own tooth is **−3.869 pp**, not the −3.828 pp first
written above — that figure used the forward run `k = 33, 34, 35`, which does not exist. The
two differ by 1 %, so the staked band is unchanged to the quoted precision; the number is
corrected here rather than left to be noticed later. Applying the same elasticity band
`[1.0, 2.0]` that §4.3 used for P-STEP28:

> **P-STEP32.** ARM B's trend-corrected rent/nat residual at `k = 32` is **positive**, of size
> **+3.87 to +7.74 pp**, in ≥ 4 of the 6 conditions.

| outcome | rule | meaning |
|---|---|---|
| **CONFIRMED** | positive in ≥ 4 of 6 conditions and size inside `[0.5, 2.0] ×` 3.869 pp | the sawtooth's packing account holds at the largest tooth staked, out of sample, on the arm whose step it is |
| **FIRED** | negative in ≥ 4 of 6 conditions | the sawtooth reading is wounded where it should have been easiest to see, and that is the headline |
| **BELOW RESOLUTION** | anything else | reported as such with the k = 29–31 residual scatter quoted as the resolution |

**Unlike P-STEP28 this one is not expected to be marginal**: the predicted tooth is ~50× the
`k = 28` tooth and ~30× the `k = 24` tooth that was already "at the edge of resolution", so a
null here is informative rather than merely underpowered.

**Discipline.** Run with the sibling's gated `rent_scaling_q2.py`, unmodified, via
`--one B 32`, which writes its own `rent_scaling_q2_B32.json` and touches no other worker's
output. Trend correction needs `k = 29, 30, 31`, which the sibling's run produces; if those
rows are unavailable the residual is **not** computed and P-STEP32 is reported as
**NOT EVALUABLE** rather than assessed against a substitute baseline.

**The affordability cut is unchanged and is arithmetic:** `profile_R` is a full `2^k` pass, so
the criterion is verified for `k ≤ 27` and *predicted, not verified*, above it. Every
Sylvester-32 truncation at `k = 28…31` is therefore reported as PREDICTED-not-verified and is
excluded from the tally, exactly as §2.5 requires.
