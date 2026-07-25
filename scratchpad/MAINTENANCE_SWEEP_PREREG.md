# PRE-REGISTRATION — the maintenance sweep: can any dynamics HOLD whole-only share, and what does holding cost?

**Frozen and committed BEFORE any dynamics is run.** Script to be written after this file is
committed: `scratchpad/maintenance_sweep.py`. Results: `scratchpad/MAINTENANCE_SWEEP_RESULTS.md`.

Scratchpad only. No Lean file, no `Stance.lean`, no audit, no `lake`. Nothing pushed.

---

## 0. SCOPE — read this before anything else

The substrate below is **designed to obey the rent clause**. It is a **control, not a
discovery about nature**. If every prediction in §4 survives, the only thing established is
that a system built to hold whole-only structure does hold it, and that the machinery can
measure the holding. **Nothing here bears on the `wild-share` open claim, and nothing here
is evidence that any natural system maintains order-3 pattern.**

What such a control is *for*: the sibling run (`HABIT_DYNAMICS_RESULTS.md`, `6b97e15`) found
the congealed-habit corner — pattern both strong and persistent — reached at **0 of 70** grid
points on the chaotic logistic lattice, with whole-only share dying in 2 kernel iterations
against 16 for pairwise. That is a negative result about one substrate. It leaves open
whether the corner is reachable *at all*, and what it would cost. A designed substrate
answers exactly that and nothing more: it establishes **reachability and price**, not
prevalence.

The failure modes that make this a real test rather than a tautology are named in §7. They
are not hypothetical: the Hadamard arm (§6) has a specific reason it may fail to obey the
design, and the estimator has a specific reason it may misreport.

---

## 1. WHAT IS ALREADY ESTABLISHED, AND WHAT WAS COMPUTED BEFORE THIS FILE WAS WRITTEN

**Disclosed in full, because the predictions in §4 are *derived* from it rather than
guessed.** Guessing would have been weaker science, but a derived prediction is only honest
if the derivation is on the record first.

Inherited (sibling agents, not re-derived here):

- The maximum-share states on `k` slots with uniform pair marginals are exactly the uniform
  distributions on minimum-size strength-2 binary orthogonal arrays;
  `maxshare(k) = k·ln2 − ln N₀(k)`, `N₀(k) = 4⌈(k+1)/4⌉` where the Hadamard matrix exists
  (`CLASSICAL_MAX_K5.md`, `ARRAY_SCAN_K67.md`, `HAMMING_FORM_SCAN.md`).
- At `k = 8…11` the maximizer is the order-12 Paley/Hadamard OA, **not** a linear code
  (`HAMMING_FORM_SCAN.md` §2).
- The classical maximum and its Hadamard equivalence are **not ours** — Gavinsky–Pudlák 2016,
  Babai 2013, Lancaster 1965 (`HADAMARD_CONNECTION.md` §B.5). Nothing in this file claims
  otherwise, and no result below is a novelty claim about that maximum.

Computed by me before writing this file, in `scratchpad/design_check.py` →
`design_check.json`. **These are construction facts about static objects. No dynamics was
run, and no maintenance quantity was computed.** All are exact (integer / exact-rational
support arithmetic; entropies are `ln` of integers).

For a state `p` uniform on support `S ⊆ {0,1}^k`, write `p̂(T) = Σ_v p_v (−1)^{T·v}` and
`A_w = Σ_{|T|=w} p̂(T)²`. Pair-uniform ⟺ `A_1 = A_2 = 0`. Let **`d`** = the lowest `w ≥ 1`
with `A_w > 0` (for a linear code, `d` is the dual distance).

| id | k | structure | \|S\| | `share_max` (nats) | /ln2 | **d** | `A_d` |
|---|---|---|---|---|---|---|---|
| `L5` | 5 | linear `[5,3]` | 8 | 1.386294 | 2.0000 | 3 | 2.0000 |
| `L7` | 7 | simplex `[7,3]` | 8 | 2.772589 | 4.0000 | 3 | 7.0000 |
| **`H8`** | 8 | **Hadamard-12 OA** | **12** | **3.060271** | 4.4150 | **3** | 6.2222 |
| **`E8`** | 8 | ext-Hamming `[8,4,4]` | 16 | 2.772589 | 4.0000 | **4** | 14.0000 |
| `H9` | 9 | Hadamard-12 OA | 12 | 3.753418 | 5.4150 | 3 | 9.3333 |
| `H10` | 10 | Hadamard-12 OA | 12 | 4.446565 | 6.4150 | 3 | 13.3333 |
| `H11` | 11 | Hadamard-12 OA | 12 | 5.139712 | 7.4150 | 3 | 18.3333 |
| `L11` | 11 | best `m=4` linear | 16 | 4.852030 | 7.0000 | 3 | 12.0000 |
| `L12` | 12 | best `m=4` linear | 16 | 5.545177 | 8.0000 | 3 | 16.0000 |
| `R12` | 12 | `m=5` affine hyperplane | 32 | 4.852030 | 7.0000 | 4 | 39.0000 |

Every row verified pair-uniform exactly (`A_1 = A_2 = 0` to `< 1e−12`) and
`share_max = k·ln2 − ln|S|` to 15 digits.

The Paley type-I `H₁₂` is rebuilt here from quadratic residues mod 11 and checked
`H₁₂H₁₂ᵀ = 12·I₁₂` exactly. `E8` and the `m=4` rows are selected by a rule fixed before the
search ran: **maximise dual distance `d` first, then the code's minimum distance** — i.e. the
linear comparator is chosen to be as *strong* as possible, which is the conservative choice
against every claim below that a Hadamard structure wins.

### 1.1 The M12 claim — VERIFIED, and it does not transfer to `k < 11`

The brief flagged that the automorphism group of the order-12 Hadamard matrix is *believed*
related to `M12`, and said not to assert it unverified. **It is verified, from two
independent sources, and it is stronger than "related":**

> "This analysis is due to Marshall Hall [1]. He showed that there is, up to equivalence, a
> unique Hadamard matrix `H` of order 12. Moreover, if `G = Aut(H)`, and `Z` is the central
> subgroup generated by `(−I, −I)`, then `G/Z` is isomorphic to the sporadic simple group
> `M12` (the Mathieu group), and has its two **5-transitive** representations on the rows and
> columns."
> — P. J. Cameron, *Hadamard matrices*, Encyclopaedia of Design Theory, 31 July 2002, §3.
> [1] = **M. Hall, Jr., *Note on the Mathieu group M₁₂*, Arch. Math. 13 (1962), 334–340.**

> "There is up to equivalence only a single Hadamard matrix of order 12. Its automorphism
> group is the Schur cover of `M12` which has order **190,080**."
> — P. Ó Catháin, *Group actions on Hadamard matrices*, MSc thesis, NUI Galway, §"Order 12".

Hall 1962 is the primary source; I did not open it, and cite it as quoted by Cameron.

**The load-bearing consequence, and the reason this is not decoration.** 5-transitivity on the
rows means the automorphism group of the *full* 11-column array is transitive on its 12 rows.
A decoder that is equivariant under a row-transitive group returns a **uniform** distribution
on the 12 rows, which is what makes the closed form of §3.4 exact. But this run uses `k = 8, 9,
10` columns as well, and **restricting to a proper subset of columns keeps only the setwise
stabiliser of that subset**, which need not be row-transitive. So the property that makes the
linear substrates exactly analysable is **guaranteed at `k = 11` and not guaranteed at
`k = 8, 9, 10`.** That is a pre-registered discriminator, tested in §6, not an assumption.

---

## 2. THE SUBSTRATE, EXACTLY

A population of `M` replicas, each a point `x ∈ {0,1}^k`. Initial state: every replica an
independent uniform draw from `S`. The measured object is the **empirical distribution across
replicas at one time**, not a time series — so there is no autocorrelation exposure and no
need for a phase-randomisation null (contrast `whole-only-null-autocorrelation`; the failure
mode that memo records cannot arise here, and I say why rather than merely asserting it:
replicas are drawn i.i.d. and evolved with independent noise, so the samples entering the
estimator at a fixed `t` are exactly independent by construction).

**One step**, applied in this order:

1. **Drift `D`** — a structure-preserving map applied identically to every replica.
   - `ARM-AUT` (primary): a uniformly random element of `Aut(S)` (coordinate permutation `σ`
     plus translation `c` with `σ(S) + c = S`).
   - `ARM-PERM`: a uniformly random permutation of the `k` coordinates, generically *not* an
     automorphism, so the structure wanders to `σ(S)`.
   - `ARM-NONE` (default for the main sweep): identity.
2. **Noise `N(ε)`** — every bit of every replica flipped independently with probability `ε`.
3. **Upkeep `U(q)`** — each replica independently, with probability `q`, replaced by
   `dec(x)`, the nearest point of `S` in Hamming distance. **Ties broken uniformly at
   random** (primary; this is symmetric under every automorphism, so it cannot itself
   manufacture an asymmetry). Sensitivity: lexicographically-least tie-break.

Measurement convention: **after step 3** (primary — it is the state of the system), with the
post-noise / pre-upkeep state recorded alongside at every step.

Two controls, run once each:

- `ARM-SCRAMBLE`: apply one uniformly random bijection of `{0,1}^k`. Entropy is exactly
  preserved (`ln|S|`); the structure is destroyed. Isolates that share is about **structure,
  not entropy**.
- `ARM-MISMATCH`: run `ARM-PERM` drift while the decoder keeps decoding to the *original*
  `S`. Asks whether upkeep works when the maintainer has the wrong pattern.

---

## 3. THE ANALYTIC BACKBONE — derived before running, so that the run is a check

Everything in this section is a derivation from §1's construction facts. It is stated in
advance so that agreement is a *confirmation* and disagreement is a *kill*, and so that no
result below can be presented as a surprise that was quietly expected.

**3.1 Noise cannot break pair-uniformity.** The bit-flip channel acts diagonally in Fourier:
`p̂_{t+1}(T) = λ^{|T|} p̂_t(T)`, `λ := 1 − 2ε`. Since `p̂_0(T) = 0` for `1 ≤ |T| ≤ 2`, it stays
zero. **So the state is exactly pair-uniform at every time**, and therefore

```
share_t  =  k·ln2 − H(p_t)     exactly, at all t.
```

The pair envelope's supremum is the uniform state, which is in the envelope. This is why the
substrate is analysable at all, and it is a design fact, not a finding.

**3.2 Free decay (`q = 0`) is exactly geometric, asymptotically, with a rate set by `d`.**
`p̂_t(T) = p̂_0(T) λ^{t|T|}`, and for small share
`share_t ≈ ½ Σ_{w≥d} A_w λ^{2wt} → ½ A_d λ^{2dt}`. Hence

```
share_{t+1} / share_t  →  λ^{2d} = (1−2ε)^{2d} ,     τ_{1/e} = 1 / (2 d ln(1/λ)).
```

**This is exactly `unpaid` of `Core/Maintenance.lean`, with `γ = 1 − (1−2ε)^{2d}`.** The
decay side of the Lean model is instantiated *literally*, not by analogy.

**Higher `d` decays FASTER.** Noise is a low-pass filter on Fourier weight, so a structure
whose lowest surviving coefficient sits at weight 4 loses it faster than one sitting at
weight 3. This is counter-intuitive if one reads `d` as "error-correcting strength", and it
is the reason the head-to-head in §6 comes out the way §4 predicts.

**3.3 Upkeep gives a strictly positive stationary share for every `q > 0`.** With upkeep
probability `q` per step, a replica's age since its last decode is `Geometric(q)`, so
(for a decoder that returns the uniform distribution on `S` — see 3.4)

```
p̂_∞(T)  =  p̂_0(T) · g_{|T|} ,      g_w = q / (1 − (1−q) λ^w)  ≈  q / (q + 2εw)  for small q, ε.
```

Hence `share_∞ ≈ ½ Σ_w A_w g_w²`, and the dial is the dimensionless ratio `ρ = q/(2εd)`:
retention `≈ (ρ/(1+ρ))²`. **`q = 1` gives `share_∞ = share_max` exactly; `q = 0` gives 0;
every intermediate `q` gives a level strictly between.** Note this is *not* the brief's
"`q ≥ ε` holds, `q < ε` loses" — see §4, P5, where both readings are pre-registered and the
run adjudicates between them.

**3.4 The closed form needs decoder equivariance, which is guaranteed for linear codes and
is a measured question for the Hadamard OA.** If `p` is invariant under `x ↦ x + c` for all
`c ∈ C` then `p̂(T) = 0` unless `T ∈ C^⊥`, so a `C`-equivariant decoder (syndrome → fixed
coset leader, or random tie-break) returns exactly uniform-on-`C`. The Hadamard OA has no
group structure; it must earn the same property from its automorphism group, and §1.1 says
the guarantee holds at `k = 11` and lapses at `k = 8, 9, 10`.

**3.5 The cost identity.** For an equivariant decoder, `H(dec#p) = ln|S|` exactly, so the
entropy erased per replica per step is

```
cost_erase  =  q · [ H(p_pre) − ln|S| ]  =  q · ( share_max − share_pre )      nats/replica/step,
```

i.e. **the rent bill is `q` times the current share deficit.** Meanwhile the entropy the
noise actually injects per step, at stationarity, is `rent = share_∞ − share_pre`. Because
mixing raises entropy, `H((1−q)p_pre + q·dec#p_pre) ≥ (1−q)H(p_pre) + q·ln|S|`, so

```
cost_erase  ≥  rent ,
```

with the gap being the entropy of not knowing which replicas were corrected. **The bill
exceeds the damage.** Both are measured; the inequality is a pre-registered check.

**3.6 One honest mismatch with the Lean model, stated now rather than discovered later.**
`Core/Maintenance.lean` has payment `α` compared against `γ·S`, i.e. decay proportional to the
*amount*. Here the decay is amount-proportional (3.2 — matches), but the payment is
proportional to the **deficit** `share_max − share`, not to the amount (3.5 — does not match).
The substrate therefore instantiates `unpaid`/`unpaid_decays` literally and `rent_holds`
only in the weaker sense that some payment holds the amount steady. **This will be reported
as a structural mismatch whatever the numbers do.**

---

## 4. PRE-REGISTERED PREDICTIONS, each with its own falsifier

Separable: each falsifier takes down its own line and nothing beneath it (discipline rule 2).

| # | prediction | falsifier — fires if |
|---|---|---|
| **P1** | The state is exactly pair-uniform at every `t`, every `ε`, every `q`: max pair-marginal deviation from ¼ below Monte-Carlo error. | any systematic pair deviation exceeding sampling error |
| **P2** | `q = 0`: `share_t → 0`, with `share_{t+1}/share_t → λ^{2d}` for every substrate. | ratio converging to anything else, or share not tending to 0 for `ε > 0` |
| **P3** | `q = 1` (measured post-upkeep): `share = share_max` at every `t`, for every substrate **whose decoder is equivariant**. | share below `share_max` under full upkeep on a linear substrate |
| **P4** | `0 < q < 1`: `share_t` decreases monotonically from `share_max` to a stationary `share_∞` with `0 < share_∞ < share_max`, matching `k·ln2 − H(p_∞)` from `p̂_∞ = p̂_0·g_{\|T\|}` (§3.3) to estimator precision on linear substrates. | non-monotone approach; `share_∞` at 0 or at `share_max`; closed form off by more than error |
| **P5** | The `q` vs `ε` threshold reading in the brief (`q ≥ ε` holds, `q < ε` strictly loses) is **WRONG as stated**; the true dial is `ρ = q/(2εd)` and there is **no threshold at all** — retention is continuous in `ρ`, `≈ (ρ/(1+ρ))²`. | any genuine threshold/knee at `q = ε`; or retention not collapsing onto `ρ` across `(ε, q, d)` |
| **P6** | `cost_erase = q·(share_max − share_pre)` exactly on linear substrates, and `cost_erase ≥ rent` everywhere. | either identity or the inequality failing beyond error |
| **P7** | **Capacity and persistence are ALIGNED on these substrates, not traded off.** Across the roster, higher `share_max` at fixed `k` goes with lower `d`, hence slower decay: `H8` beats `E8` on both; `L12` beats `R12` on both. | any roster pair where the higher-capacity structure decays strictly faster |
| **P8** | `H8` ≥ `E8` at every `t ≥ 0` under free decay: equal-or-above at `t = 0` (3.060 vs 2.773, exact) and asymptotically above (ratio `λ⁶` vs `λ⁸`). | the two curves crossing at any `t` |
| **P9** | `ARM-AUT` is exactly share-neutral, and this is a **triviality** (an automorphism maps the state to itself) — reported as such, not as a finding. | any share change under `ARM-AUT` beyond floating-point |
| **P10** | `ARM-SCRAMBLE` collapses share to near zero in one step while entropy is exactly unchanged at `ln\|S\|`. | entropy changing, or share surviving |
| **P11** | `ARM-MISMATCH`: upkeep to the wrong structure fails to hold share and is worse than no upkeep at all. | mismatched upkeep holding share |

Derived numbers the run must hit (from §1's `A_w`, `d`, and §3):

- asymptotic per-step ratio `λ^{2d}` — `d=3`: 0.9415 / 0.8858 / 0.7828 / 0.5314 / 0.2621 /
  0.04666 at `ε` = 0.005 / 0.01 / 0.02 / 0.05 / 0.10 / 0.20; `d=4`: 0.9227 / 0.8508 / 0.7214 /
  0.4305 / 0.1678 / 0.01680.
- `τ_{1/e}` in steps — `d=3`: 16.58 / 8.25 / 4.08 / 1.582 / 0.747 / 0.326; `d=4`: 12.44 /
  6.19 / 3.06 / 1.186 / 0.560 / 0.245.
- asymptotic `H8`/`E8` amplitude ratio `A_3^{H8}/A_4^{E8} = 6.2222/14 = 0.4444`, so if the
  curves were in their asymptotic regime from `t=0` they would cross at
  `t* = ln(2.25)/(2 ln(1/λ))` = 40.3 / 20.1 / 9.93 / 3.85 / 1.82 / 0.794 at those `ε`.
  **P8 predicts no such crossing occurs**, because `H8` is already above at `t = 0`; if a
  crossing IS seen near `t*`, P8 dies and the asymptotic reading is what survives.
- `H11` / `L11` asymptotic ratio → `18.3333/12 = 1.5278` (same `d = 3`, so no crossing).

---

## 5. TASK 1 — THE MAINTENANCE SWEEP

**Grid.** `ε ∈ {0.005, 0.01, 0.02, 0.05, 0.10, 0.20}` × `q ∈ {0, 0.001, 0.003, 0.01, 0.03,
0.1, 0.3, 1.0}` × all 10 substrates × `T = 400` steps. Every cell computed **exactly** by
propagating `p` in the `2^k` Fourier basis (`k ≤ 12` ⇒ ≤ 4096 coefficients), which is the
population limit and carries no sampling error.

**Monte-Carlo arm, with the sibling-matched floors.** The exact arm is the ground truth; the
MC arm is what shows the *instrument* reads it correctly, using the identical estimator and
floors as `array_cap_experiment.py` / `habit_dynamics.py`:

- `shareK` by IPF over all `C(k,2)` pair marginals (`array_cap_experiment.shareK`);
- **matched pairwise-maxent multinomial surrogate null** (`n_surr = 60`) — the estimator-bias
  floor; **excess = share − null_mean**, `z = (share − null_mean)/null_sd`;
- **shuffle floor** (`n_shuf = 10`), independent permutation of each channel;
- cap compliance checked every cell (`shareK ≤ k·ln2 − max_pair H(pair)` and `≤ (k−2)·ln2`);
- **tied fraction is exactly 0 by construction** — the states are already binary, there is no
  binarisation threshold, so discipline rule 4 is satisfied trivially and is recorded as
  trivial rather than as a pass.

MC conditions: `ε ∈ {0.02, 0.05}` × `q ∈ {0, 0.01, 0.1, 1.0}` × `{L5, L7, E8, H8, H11, L12}`,
`M = 500 000` replicas, `T = 64` steps, **5 independent seeds**; error bars are the
across-seed sd / √5. Primary seed 20260725; seeds {20260725, 99, 7, 1337, 4242}.

**The rent-targeting controller** — the direct empirical form of `rent_holds`. Hold `share`
at a target level by choosing `q_t` each step to make `share_{t+1} = share_t` (bisection on
the exact propagator). Report the steady `q*(ε, structure, target)` and its `cost_erase`.
**That cost, in bits per slot per step, is the deliverable "rent".**

**Deliverable — the maintenance cost curve.** For every `(ε, q, substrate)`: retained share
`share_∞` (nats and as a fraction of `share_max`) against `cost_erase` (nats/replica/step)
and against `cost_flips` (mean bits actually flipped by the decoder per replica per step).
Reported in bits throughout, with the `ρ = q/(2εd)` collapse tested as P5 specifies.

---

## 6. TASK 2 — THE EXCEPTIONAL STRUCTURE AT 12

Head-to-head at **fixed `k`**, so that nothing depends on comparing across slot counts:

- `k = 8`: `H8` (Hadamard-12, `|S|=12`, `d=3`, cap 3.0603) vs `E8` (ext-Hamming `[8,4,4]`,
  `|S|=16`, `d=4`, cap 2.7726).
- `k = 11`: `H11` (`|S|=12`, `d=3`, cap 5.1397) vs `L11` (`|S|=16`, `d=3`, cap 4.8520).
- `k = 7` and `k = 12` linear anchors (`L7`, `L12`) on either side of the exceptional window.

**The decoder-equivariance test, pre-registered with both outcomes' meanings** (this is the
measurement §1.1 sets up):

> Apply `dec` to `uniform(S) ⊛ noise(ε)` and read the induced distribution on `S`.
> **Uniform ⇒** the closed form of §3.3 is exact for the Hadamard substrate too, and the
> `k = 11` guarantee from 5-transitivity has extended to `k = 8, 9, 10` for a reason worth
> naming. **Non-uniform ⇒** the Hadamard substrate's upkeep is *lossy in a way the linear
> substrates' is not*: full upkeep would not restore `share_max`, and P3 is expected to fail
> on `H8`/`H9`/`H10` while holding on `H11` and on every linear substrate.

Either outcome is a result. The second would be the more interesting one — a concrete
respect in which the exceptional maximizer is **harder to maintain than a linear code**, and
it would be predicted in advance by the column-restriction argument rather than found by
inspection.

---

## 7. WHAT WOULD FALSIFY THE RENT-CLAUSE READING

Named in advance, as the brief requires, and these are the reasons this run is a test of the
design rather than a restatement of it:

- **RC-A — share dies even at full upkeep.** `q = 1` and `share_∞ < share_max − 5σ` on a
  substrate whose decoder is equivariant. Would mean upkeep cannot buy standing still.
  *(Expected to fire on `H8`/`H9`/`H10` if and only if the §6 equivariance test comes back
  non-uniform. That is a scoped, predicted failure of P3, not a failure of the rent clause,
  and it will be reported under that distinction.)*
- **RC-B — share survives with no upkeep.** `q = 0`, `ε > 0`, and `share_t` plateaus above
  the floor. Would mean pattern is free.
- **RC-C — no strict loss when underpaying.** Some `0 < q < 1` holding `share_max` exactly,
  or some `q` giving a stationary level above `share_max`.
- **RC-D — decay is not the model's shape.** `share_{t+1}/share_t` at `q = 0` not converging
  to `λ^{2d}`, i.e. the free decay not geometric.

**Any of RC-A…RC-D firing is reported as prominently as a survival** (discipline rule 7), and
the dead prediction stays in the record marked dead.

**And the standing limitation, which no outcome removes:** all four legs are *engineered*.
Surviving them says the substrate does what it was built to do. It is a measurement of
**price**, not of **prevalence**.

---

## 8. GATES — all must PASS before any measurement is read

| gate | what it establishes |
|---|---|
| **G1** share machinery | `array_cap_experiment.gate()` PASSes unchanged (k=3 parity → ln2 exactly; independence → 0; k=5 code state → 2·ln2; IPF residual 0) |
| **G2** structures | every roster entry exactly pair-uniform, support size and `share_max = k·ln2 − ln\|S\|` as tabled, via the **IPF estimator** and not only via the closed form |
| **G3** Paley `H₁₂` | `H₁₂H₁₂ᵀ = 12·I` exactly; strength 2 by direct combination counting on the 12 rows (each of the 4 symbol pairs exactly 3 times in every column pair) — the independent route, no Fourier |
| **G4** propagator | exact Fourier propagation reproduces brute-force convolution of the full `2^k` distribution to `< 1e−12`, at several `(ε, t)` |
| **G5** MC ↔ exact | the replica simulator's empirical distribution matches the exact `p_t` within multinomial error at several `(ε, q, t)`; and MC excess matches exact share within the surrogate floor |
| **G6** floors fire and floor | surrogate + shuffle floors read ≈ 0 excess on an exactly independent state and recover `share_max` on the exact code state |
| **G7** decoder | `dec` maps every point of `S` to itself; and is exactly `C`-equivariant on linear substrates (checked, not assumed) |

A failed gate stops the run; it is not worked around.

---

## 9. WHAT WILL NOT BE CLAIMED

1. **No claim about nature.** Designed substrate; control. `wild-share` is untouched.
2. **No novelty on the classical maximum.** That is Gavinsky–Pudlák / Babai / Lancaster
   (`HADAMARD_CONNECTION.md` §B.5). This run uses their objects; it does not re-derive or
   re-claim them.
3. **No world-claim from the rent clause, and no refutation of it.** `Core/Maintenance.lean`
   is a theorem about a model. A designed substrate obeying that model is not evidence the
   world does.
4. **No claim that the congealed-habit corner is reachable in general.** Reaching it here is
   the *definition* of the substrate, not a discovery. The transferable content is the price.
5. **No quantum content anywhere.**
6. **The `M12` fact is cited, not used as evidence for anything physical.** It enters solely
   as the reason to expect a `k = 11` vs `k ≤ 10` asymmetry in decoder equivariance.
7. **Nothing here is mechanized.** No Lean file is touched and no result below is offered for
   the audit.

---

Frozen. `design_check.py` / `design_check.json` are committed with this file as the record of
what was computed before it.
