# RESULTS — the restorability boundary, and whether rent/nat has a floor

Pre-registered in `RENT_SCALING_PREREG.md`, **committed at `45b6877` before `rent_scaling_*.py`
existed**, before any automorphism group in this roster was computed and before any rent number
at `k > 24`. AMENDMENT 1 (`3b32006`) added the column-order control; AMENDMENT 2 (`aac3149`)
added ARM B at `k = 32` and its P-STEP32 adjudicator — **both before the data they govern
existed**.

Q1 run: `rent_scaling_q1.py` → `rent_scaling_q1.json` (119 structures), re-checked by
`rent_scaling_q1_verify.py`, censused by `rent_scaling_q1_census.py`. Q2 run:
`rent_scaling_q2.py --one ARM K` → `rent_scaling_q2_{A25..A31,B25..B32}.json` (15 tiers, 90
rows). Adjudication: `rent_scaling_analyze.py`. Gate logs: `rent_scaling_aut_gate.log`,
`rent_scaling_q2_gate.log`, `rent_scaling_q2_g1_reverify.log`.

**SCOPE, unchanged from the prereg §0 and from both parents, and it governs every line below.**
Designed substrates. A **control, not a discovery about nature**. This measures the *price* of
holding whole-only structure in an engineered system and the *algebra* of when it can be
restored — not its prevalence anywhere. `wild-share` is untouched. `Core/Maintenance.lean` is a
theorem about a model and nothing here is offered as support for it or refutation of it.
Nothing is mechanized; no Lean file was opened; nothing reaches `Stance.lean`. Anyone quoting
this must carry this paragraph.

---

## Provenance of this document — who measured what

Three agents and a coordinator produced this campaign; two hit session limits with the
computation done and the write-up unwritten. Under the **received-numbers-are-not-measured-numbers**
gate, every number below is tagged:

| source | status |
|---|---|
| **Q1 canonical, Q2 all tiers, all fits, all steps, the ceilings, the censuses** | **re-derived by me from the primary JSON**, with my own code (`indep_q2.py`, `indep_q2b.py`, `indep_q2c.py`, scratch), not by reading a sibling's table |
| `RENT_SCALING_Q2_ADJUDICATION.md` (`44329f5`) — the coordinator's mechanical P-STEP32 run | **fragment, folded in and independently re-derived.** The coordinator applied the pinned rule to data neither agent had read; §6.2 reports my own re-derivation, which agrees to the last quoted digit, **and corrects nothing in it** |
| `RENT_SCALING_SUBSET_RESULTS.md` — the sibling's H-SUBSET and censuses | **folded in at §4; every count re-derived from `rent_scaling_q1_census_{12,20,24}.json`**, including the S(4,5,11) block property, which I recomputed rather than accepted |
| `RENT_SCALING_PRIOR_ART.md` (`648ee07`) — the sibling's literature sweep | **received, not re-run.** I did not repeat the searches. Its adjudication binds §5 and I have not weakened it |
| the six Q2 gate outcomes | **read from the committed gate logs, not re-run.** Stated as log entries, not as gates I fired |
| box/memory figures (§0.4) | **received from the predecessor's draft, not re-measured** — the runs are finished and cannot be re-instrumented |

---

## Headline

> **Q1 — the pre-registered bet loses, and the prior art said it would.** Symmetry is
> *sufficient* for restorability and it is **not necessary**. Transitive ⟹ equivariant held
> **20 of 20** with zero violations, as the elementary orbit argument says it must. But two
> structures have an **intransitive** automorphism group and are **exactly** equivariant — one
> of them is `ARM A` at `k = 23`, whose group has order **253 with a fixed point**, not the
> `M₂₄` the parent conjectured. `H20/k19` and `H24/k23` have the **same orbit shape `[n−1, 1]`
> and opposite restorability**: no function of the orbit partition can separate them.
> **H-IFF is dead in the necessity direction, H-ORBIT is dead outright (4 of 74).** The prereg
> staked this as the expected outcome under a well-populated prior, and it was right to.
>
> **And the counterexample is the rule at its own width, not a curiosity.** An exhaustive
> census — all 1981 column subsets of Paley-12 — finds **396 counterexamples, every one at
> `k = 5`, and at `k = 5` all 396 restorable subsets are counterexamples.** But do not
> overcount: the 66 non-restorable 5-subsets are **exactly the blocks of the Steiner system
> S(4,5,11)** (recomputed here: 66 blocks covering all 330 four-subsets exactly once), the 396
> carry identical invariants, and Paley-20 has **no** restorable subset at all in `k = 4…6`.
> It is **one counterexample up to equivalence, occurring 396 times.**
>
> **Q2 — the floor that the parent could not identify at `k ≤ 24` is resolved at `k ≤ 31`, in
> four of six conditions, and the four are not a random four.** The pre-registered verdict of
> record on ARM A is **PLATEAU-WITH-FLOOR + SAWTOOTH-DOMINATED — both fired, and the
> pre-registration wrote them as alternatives when they are not.** The floor resolves in
> **exactly the four fixed-*fraction* target conditions and neither fixed-1-nat condition**.
> It survives absorbing the sawtooth into nuisance parameters (4/6) but **not** restricting to
> `k ≥ 16` (3/6, below the rule's own threshold) — **and ARM B, over an overlapping range of the
> same quantity, returns CONTINUED DECLINE 6 of 6.** A floor identified on one arm and absent on
> the other is not a robust floor, and that is the largest caveat in this document.
> **The curve has not flattened** — at `k = 31` rent/nat is still falling ~1.7 pp per step — so
> "a floor is resolved by the fit" and "the curve is still declining" are both true and neither
> may be quoted without the other. **No `k > 31` claim is made, and the floor is a curve
> parameter over `5 ≤ k ≤ 31`, never an asymptotic cost.**
>
> **Q2's staked steps split.** **P-STEP32 CONFIRMED, 6 of 6, inside the pinned band** — the
> campaign's largest advance-tested tooth, staked before the datum existed. **P-STEP28's
> raw-uptick form FIRED, 0 of 6**, and with it **H-DISSOC-2 fired on its "neither arm ticks"
> falsifier**. The trend-corrected statistic — the one §3.3 said carries the weight — survives
> and separates the arms cleanly (+1.19 pp on A, −0.14 pp on B, every condition). The raw form
> was **arithmetically unwinnable and the prereg's own §1.3 says so**; that is a disclosed
> defect in the pre-registration, not a rescue of the prediction.
>
> **Two inherited instrument defects fired and are fixed.** The parent's `q = 1` ceiling column
> is roundoff below ~1e−9; its radial noise kernel is a Krawtchouk sum that is total
> cancellation and **returns negative probabilities in 10 of 24 cells at `k = 23`**. Blast
> radius bounded: **the rent curve is unaffected (~1e−11 relative); the ceilings were not, and
> are recomputed.** Both defects are now registered gates (`4cf6ba5`).

---

## 0. Gates

### 0.1 Q1 instrument — ALL PASS (`rent_scaling_aut_gate.log`)

| gate | outcome |
|---|---|
| **Q1-G1** exact order vs the enumerated orders in `aut_counts_exact.json` | **PASS** — all ten agree: `H8` 48, `H9` 144, `H10` 720, `H11` 7920, `L5` 64, `L7` 1344, `E8` 21504, `L11` 768, `L12` 9216, `R12` 73728 |
| **Q1-G2** `\|Aut\| = \|P\|·\|C\|`, `\|C\|` = orbit of 0, closure orbits == search orbits | **PASS** on all eight checked, including `H12/k5` `[10,2]` and `H12/k8` `[8,4]` |
| **Q1-G3** the dye test on planted groups | **PASS** — full cube 384, even-weight `[4,3]` 192, repetition `[4,1]` 48, and a deliberately broken 3-point support 2 with orbits `[2,1]` |
| **Q1-G4** `R_i(a)` here vs `rent_islands.py`'s stored `profile_dev` | **PASS** at all eight shared structures |
| **Q1-G5** (T): no transitive structure above the float64 floor | **PASS** — 0 violations in 20 |

**Search caps, per the harvest gate: none bound.** 0 of 119 canonical structures, and 0 of the
45 863 census structures, had a search exhaust the declared 2·10⁷-node budget (re-derived from
the census JSONs: `undetermined = 0` in all three). **Every order in this file is a group
order** from a stabiliser chain of single-solution searches — never a saturated count. That is
the gate that forced `RENT_COMPARISON.md`'s withdrawal, and it is discharged here rather than
assumed.

*Free cross-check against the literature, not sought:* the Sylvester ladder returns
`|Aut| = 319 979 520` at `k = 31`. `|GL(5,2)| = 31·30·28·24·16 = 9 999 360`, and
`9 999 360 × 32 = 319 979 520` — the punctured simplex code's known group. Arithmetic verified
here.

### 0.2 Q2 instrument — **two gates FIRED**, on defects inherited from the parent

*(Diagnoses below are read from `rent_scaling_q2_gate.log` and the predecessor's draft; I did
not re-run the gates. The numbers I did re-derive are marked.)*

**Q2-G1 fired first.** The lean solver was required to reproduce `rent_islands.py`'s rows at
`k = 20…24`, quantity by quantity, to 1e−10. Everything matched to ~1e−14 **except the
`ceiling` column**, which disagreed by 4.2e−10 at `k = 23` and grew with `k`.

*Diagnosis.* At `q = 1` every replica is replaced by its decoded point, so the stationary state
**is** the deposit — supported on `|S| ≤ 32` points. The parent computes its entropy as a sum
over all `2^k` cells, of which `2^k − |S|` are exactly zero and carry roundoff mass ~1e−17 each.
Their contribution is `2^k × 1e−17 × ln(1e−17)` ≈ 3e−9 — the whole signal, because the deficit
being measured is itself 1e−5 and smaller. Replaced by the closed form `k·ln2 − H(c) − ½·leak`
over `|S|` numbers. **The parent's `ceiling_frac` column is not reliable below about 1e−9 and
must not be read as a measurement there.**

**Q2-G6 then fired on something worse.** With the ceiling fixed, `A23` — *exactly* equivariant,
verified in exact integer arithmetic (§2.2) — still returned a non-uniform `q = 1` deposit, off
by 5.4e−9.

*Diagnosis.* Both files computed the noise kernel as `κ(a) = (1/N)·Σ_w λ^w g_w K_w(a)`. Correct
algebra, numerically ruinous: at `k = 23` the Krawtchouk numbers reach `|K_w| = 1 352 078` while
the answer at `a = 23` is 1e−46. The sum is total cancellation with an absolute noise floor of
`ε_machine·max|K_w|/N = 3.5e−17`, and **it returns negative probabilities** — from the gate log:

| `k`, `ε` | cells where the Krawtchouk route came out NEGATIVE | `\|exact − Krawtchouk\|` |
|---|---|---|
| 16, 0.01 | 4 of 17 | 1.58e−17 |
| 20, 0.01 | 6 of 21 | 1.91e−17 |
| **23, 0.01** | **10 of 24** | 1.11e−16 |

*Fix, two routes, both exact and both gated (Q2-G7).* At `q = 1`, `g ≡ 1` and the kernel simply
**is** the binomial noise kernel `ε^a(1−ε)^{k−a}` — closed form, no cancellation. For general
`q`, expanding `1/(1−(1−q)λ^w)` as a geometric series gives
`κ(a) = q·Σ_m (1−q)^m·e_m^a(1−e_m)^{k−a}` with `e_m = (1−λ^{m+1})/2` — every term positive, and
it is not a trick but the physics: the mixture over *how many noise steps since the last
upkeep*. The two agree to ≤ 8.7e−18. The Krawtchouk route survives only as the gate's comparator.

*Blast radius, bounded rather than asserted.* The Krawtchouk error enters `C` as
`≈ q·3.5e−17·N/|S|`, worst exactly at `q = 1` where the exact route now takes over, and it
scales away with `q`. `rent_per_nat` is `q·(H_pre − H_c)/share` with `H_pre − H_c = O(0.1…3)`,
so residual contamination of every rent number in this campaign and the parent's is bounded by
**~1e−11 relative**. **The rent curve is unaffected; the restorability ceilings were not, and
are recomputed here.** *Consistency check I did run:* across all 90 new rows the worst
`pair_leak` is 4.68e−09, worst `Hc_deficit` 5.47e−10, worst `mass_dev` 4.44e−16, `neg_mass`
exactly 0 — all consistent with that bound and none near it.

**Q2-G6's own first version was also wrong, and that is recorded too.** It required criterion
and solve to agree in *both* directions — but only one direction is a theorem. A lossy structure
can read an arbitrarily small residual at small `ε`, because `R_i(a)` differs only at large `a`
and the noise kernel carries weight `ε^a` there: `A20` at `ε = 0.01` reads 9.2e−15 and is
genuinely lossy. That `ε`-dependence is physics and is reported (§2.5), not gated.

**Both defects are now registered as standing gates** — *catastrophic cancellation in
alternating sums* and *zero-cell roundoff swamps small deficits* — in `GATES.md` at `4cf6ba5`.

### 0.3 Q2 instrument — the gates that passed

| gate | outcome |
|---|---|
| **Q2-G1** lean solver vs the parent at `k = 20…24`, both routes | **PASS** after the ceiling fix — worst relative disagreement 2.6e−14 |
| **Q2-G1 re-verification** after two post-gate changes to the shipped code (bracketing-grid cache, and its re-keying off `id(lat)`, which CPython reuses after gc) | **PASS** — 32 rows × 6 quantities, worst 2.09e−13 (`share_pre`), `rent_scaling_q2_g1_reverify.log`. Re-gating the *shipped* code rather than the gated prototype is the gate-log-provenance requirement, and it is discharged |
| **Q2-G2** blocked in-place WHT vs the parent's | **PASS** — bit-identical at `2^18`, `2^20`, `2^22` |
| **Q2-G3** `share_∞(q)` strictly increasing at every new `k` | **PASS** at `A25`, `A28`, `A31`, `B27` |
| **Q2-G4** pair-uniformity and `share_max = k·ln2 − ln\|S\|` at every new substrate | **PASS** — `pair_dev` exactly 0; every Hadamard order verified `H Hᵀ = N·I` |
| **Q2-G6 / Q2-G7** | **PASS** after both fixes |

### 0.4 The per-row error budget — re-derived over all 90 new rows

The prereg promised no error bars and a numerical budget instead, because the instrument is a
population-limit fixed-point solver with no Monte Carlo anywhere. Delivered:

| quantity | worst over 90 rows | prereg's rail |
|---|---|---|
| `target_resid_rel` | 2.32e−12 | drop above 1e−6 — **0 rows dropped** |
| `mass_dev` | 4.44e−16 | — |
| `neg_mass` | **exactly 0** | — |
| `pair_leak` | 4.68e−09 | — |
| `c_err` (fixed-point residual) | 9.55e−15 | — |
| `leak_residual_rel` (the `O(leak²)` term) | 3.13e−18 | — |
| `q*` range | 0.00648 … 0.30002 | both rails (0 and 1) clear by two orders |

**Box discipline** *(received from the predecessor's draft, not re-measured)*: CPU only, no GPU
(another campaign held it at 100 %). The parent's solver classes measured **13.2 GB resident**
at `k = 27`/`31` on a box with 7 GB free and 5 GB of swap already in use; that is why both
routes were re-implemented lean, and the campaign then held inside its declared 6 GB budget.
Worker pool capped at 2–3 against a background of 18–25 of 32 cores. Wall time for the 15 tiers:
11 s (`B25`) to 2767 s (`A27`), `rent_scaling_q2_run.log`.

---

## 1. Q1 — the roster, and the affordability cut as a number

119 structures: every wired Hadamard order `N ∈ {8, 12, 16, 20, 24, 28, 32}` × every truncation
width `k = 3…N−1`.

| | count | note |
|---|---|---|
| structures evaluated | 119 | |
| `R_i(a)` computed exactly | **108** | the `2^k` cut; **11 excluded** |
| excluded, marked **PREDICTED-not-verified** | **11** | exactly `H32/k21 … H32/k31` — all linear, hence transitive, hence restorable by theorem (T). **Excluded from every tally**, never counted as confirmations |
| of the 108, supports whose `N` rows are all distinct | **74** | **the primary tally**, a property of the structure declared before any verdict |
| the other 34 | | column truncation collapsed rows (`\|S\| < N`) |

The cut is more conservative than AMENDMENT 2 required (it named `k ≤ 27` as verifiable and
`k = 28…31` as predicted); the run verified only `k ≤ 20` among the linear Sylvester-32 ladder
and marked `k = 21…31` predicted. Reported as it happened, not as it was licensed.

---

## 2. Q1 — the verdicts

### 2.1 (T) TRANSITIVE ⟹ EQUIVARIANT — 0 violations. Not a discovery, and said so in advance.

The prereg stated this as a theorem, not a prediction: `R_i(a)` is constant on `Aut(S)`-orbits,
because an automorphism is an isometry preserving `S`, so it transports nearest-point sets and
tie multiplicities. **20 transitive structures in the primary tally, max `profile_dev`
7.11e−15** — the float64 floor. A violation would have been an instrument fault; there is none.
Across the 45 863 census structures the same direction holds with **0 violations**, and
`orbits_refine_levels` holds in every one of the 74.

The same argument disposes of every linear substrate for free: translation by a codeword is an
automorphism, so linear ⟹ transitive ⟹ equivariant. That covers the whole Sylvester ladder and
`ARM B`/`B′`/`C`, and it is why the interesting split lives inside the non-linear Paley family.
**This is elementary and is claimed as elementary** (prereg §2.1 said so before the run).

### 2.2 H-IFF — **DEAD in the necessity direction.** Two canonical counterexamples.

| structure | `\|S\|` | `\|Aut\|` | orbits | transitive | `R_i(a)` |
|---|---|---|---|---|---|
| `H12/k5` | 12 | **20** | `[10, 2]` | **no** | **exactly constant** |
| `H24/k23` = **`ARM A` at `k = 23`** | 24 | **253** | `[23, 1]` | **no** | **exactly constant** |

**Both were re-checked by two independent instruments** (`rent_scaling_q1_verify.py`), because a
finding that kills a pre-registered hypothesis does not get to rest on the instrument that found
it:

- *the group*, by **full enumeration of every `(σ, c)` pair** — `aut_counts_exact.py`'s method,
  sharing no code with the stabiliser chain. Both return **20** and **253**. (`H12/k5` has
  `k = 5`, so all `5!·2⁵ = 3840` cube isometries are tested individually: no chain, no node
  budget, no pruning.)
- *the equivariance*, in **exact integer arithmetic**. Grouping the cube by tie multiplicity `t`
  makes `R_i(a) = Σ_t C_t[i,a]/t` with every `C_t[i,a]` an exact integer, so "does `R_i(a)`
  depend on `i`" becomes a rational identity on small integers and float64 never enters. Both
  counterexamples return `max |R_i(a) − R_0(a)| = 0`, **exactly zero**, not 2.7e−15.

Four controls behave on the same exact instrument: `H20/k19` deviates by exactly **90**,
`H12/k8` by **18**, `H24/k22` by **913/30**, and transitive `H12/k11` by **0**.

> **`H20/k19` and `H24/k23` have the same orbit shape `[n−1, 1]` — one large orbit and one fixed
> point — and opposite restorability.** That single pair is the finding: no function of the
> orbit partition can separate them, so the restorability boundary is not the orbit boundary.

**The prereg staked this as a bet against a well-populated prior, and the prior won.** §2.2 said
in advance that a falsification was the expected outcome and would be a full result. It is
reported as the death of "exactly algebraic", not rescued. **Sufficiency stands and is worth
keeping** — a genuine one-way criterion, and the reason every linear substrate is restorable
without computing anything.

### 2.3 H-ORBIT — **DEAD.** 70 of 74 hold; 4 are strict coarsenings.

Orbits refine the `R`-level sets by (T), and that direction held with **0 violations**. Equality
failed at four structures, re-derived here from `rent_scaling_q1.json`:

| structure | orbits | `R`-level sets |
|---|---|---|
| `H12/k5` | `[10, 2]` | `[12]` — one level |
| `H20/k6` | 20 singletons | `[4,2,2,2,1,1,1,1,1,1,1,1,1,1]` |
| `H24/k7` | 24 singletons | `[2,2,2,2,2,2,2,2,1,1,1,1,1,1,1,1]` |
| `H24/k23` | `[23, 1]` | `[24]` — one level |

Accidental degeneracy of the profile across distinct orbits is real, and at two of the four it
**is** the whole counterexample. The sibling's sampling arm found 18 more, all at `k = 6, 7, 8`
on `N = 20, 24, 28`, every one a case where random column selection collapsed the support.

### 2.4 The `ARM A` ladder — rebuilt from the primary JSON

| `k` | `\|S\|` | linear | `\|Aut\|` | orbits | transitive | `profile_dev` | `1 − ceiling` @ε=.01 | @ε=.05 |
|---|---|---|---|---|---|---|---|---|
| 5–7 | 8 | yes | 64 / 192 / 1344 | `[8]` | yes | ≤ 4.4e−16 | — | — |
| **8** | 12 | no | **48** | `[8, 4]` | no | 5.63e−01 | 2.52e−05 | 3.80e−04 |
| 9 | 12 | no | 144 | `[12]` | **yes** | 0 | 0 | 0 |
| 10 | 12 | no | 720 | `[12]` | **yes** | 6.7e−16 | 0 | 0 |
| 11 | 12 | no | **7920 = \|M₁₁\|** | `[12]` | **yes** | 3.3e−16 | 0 | 0 |
| 12–15 | 16 | yes | 768 / 3072 / 21504 / 322560 | `[16]` | yes | ≤ 1.8e−15 | — | — |
| 16 | 20 | no | **1** | 20 singletons | no | 8.59e−02 | 1.28e−06 | 1.66e−05 |
| 17 | 20 | no | **1** | 20 singletons | no | 8.65e−03 | 4.65e−12 | 1.25e−09 |
| 18 | 20 | no | 9 | `[9, 9, 1, 1]` | no | 4.01e−03 | 3.96e−12 | 2.53e−10 |
| 19 | 20 | no | 171 | `[19, 1]` | no | 3.26e−03 | 0 *(below floor)* | 2.87e−13 |
| 20 | 24 | no | **1** | 24 singletons | no | 1.17e−03 | 2.04e−13 | 5.69e−11 |
| 21 | 24 | no | **1** | 24 singletons | no | 8.67e−04 | 4.89e−14 | 8.00e−12 |
| 22 | 24 | no | 11 | `[11, 11, 1, 1]` | no | 1.76e−04 | 1.2e−15 *(below floor)* | 1.2e−15 *(below floor)* |
| **23** | 24 | no | **253** | `[23, 1]` | **no** | **exactly 0** | **0** | **0** |
| 24 | 28 | no | **1** | 28 singletons | no | 3.32e−02 | — | — |
| 25, 26 | 28 | no | 12 | `[12, 12, 2, 2]` | no | 8.07e−04 / 4.41e−04 | — | — |
| 27 | 28 | no | 156 | `[26, 2]` | no | 1.86e−04 | — | — |
| 28–31 | 32 | yes | 73728 / 688128 / 10321920 / **319 979 520** | `[32]` | yes | (T) | — | — |

"—" in the ceiling columns is the **declared** affordability cut `KCEIL = 23`, in the code before
the run, not a selection after it. *(below floor)* marks a deficit at or under 100× the solver's
own residual — per the named-denominator amendment those are **not measurements** and are
reported as unresolved, not as small numbers (§8.2).

**The parent's Mathieu conjecture is half right and half dead.** `RENT_ISLANDS_RESULTS.md` §0.1
offered, explicitly as a conjecture, that equivariance at `k = 11` and `k = 23` tracked
"exceptionally large automorphism groups (`M₁₂`, `M₂₄`)". Measured:

- at `k = 11` the group **is** `7920 = |M₁₁|` and the action **is** transitive. That half stands
  and is now computed rather than conjectured. **It is also somebody else's theorem — see §5.**
- at `k = 23` the group has order **253 = 11 × 23**, with a **fixed point** — not
  `|M₂₄| = 244 823 040`, and not transitive. **The `M₂₄` reading is FALSE and is recorded dead.**
  `k = 23` is equivariant for a reason that is not group-theoretic at all.

*Independent corroboration of both orders, from the construction rather than the search:*
deleting one column deletes one point of the construction's natural action, so `|Aut(S)|` must be
`|G|/N`. `|M₁₂|/12 = 95040/12 = 7920` ✓ and `|PSL(2,23)|/24 = 6072/24 = 253` ✓.

**A second correction, smaller.** The parent quoted the `k = 8` ceiling as `0.99962 × share_max`
while its own JSON column read `0.99997476`. Both are right and neither is a discrepancy: the
ceiling is `ε`-dependent, and those are the `ε = 0.05` and `ε = 0.01` values. Recomputed in
closed form: **`1 − 3.796e−04` at `ε = 0.05` and `1 − 2.524e−05` at `ε = 0.01`.**

### 2.5 The `ε`-dependence is physics, and it makes "lossy" a two-part statement

`R_i(a)` differs only at large `a`; the noise kernel weights distance `a` by `ε^a`. So a
structure that is lossy *in principle* can be arbitrarily close to restorable *at low noise*.
`H24/k22` is the extreme case in this roster: `profile_dev = 1.76e−04`, unambiguously lossy by
the `ε`-free criterion, and yet its ceiling deficit is **1.3e−15 at both `ε`** — below the
solver's own floor at both, and therefore **not measurable at either**. Lossy in principle,
unmeasurably lossy in practice.

**Consequence for language:** "some patterns cannot be restored at any price" is a statement
about the `ε`-free profile criterion only. *How much* is lost is a separate, `ε`-dependent, and
often unmeasurable quantity. Only the first is algebraic.

### 2.6 H-CEILING — **UNRESOLVED, and the predictor is the reason**

Pre-registered: the deposit deficit `ln|S| − H(c*)` at `ε = 0.05` should rank with orbit
imbalance `I`, positively, over the lossy population.

**Denominator named first:** the test ran on **48 lossy structures**, not the 52 lossy in the
primary tally — the four at `k = 24…27` (`H28/k24…k27`) fall outside the declared `KCEIL = 23`
ceiling cut. That is an affordability cut fixed in code before the run, and the 48 is stated
here rather than left to be inferred.

**Measured: Spearman ρ = +0.138, one-sided p = 0.174** against a 200 000-draw permutation null.
**Null shape measured before the p was read** (harvest gate: null-shape-before-z): mean +0.0002,
sd 0.1455, skew +0.003, 5/50/95 quantiles −0.240/0.000/+0.240 — symmetric, so a p is quotable
and no z is quoted anywhere in this campaign. **Sign right, p above 0.05 → UNRESOLVED**, exactly
the outcome the prereg assigned to this case.

**Discipline rule 4, disclosed before the statistic is believed: the tied fraction is 85.4 %.**
41 of 48 points lie in a tie; there are 9 distinct values of `I`; the largest tie block is
**34 of 48 at `I = 1.0000`**, because a trivial automorphism group forces `I = 1` exactly and
most of these structures have one. **The predictor is nearly constant. This rank statistic had
almost no variance to work with, and its verdict is reported, not believed.**

*The prereg promised an exact enumerated permutation null. `48!` is not enumerable; the null is
sampled at 200 000 draws and is labelled sampled. That is a departure from §2.4 and it is stated
rather than glossed.*

**POST-HOC, clearly labelled, not evidence.** Included because leaving it out would hide a fact
in the same table: the *combinatorial* quantity ranks the deficit almost perfectly —
**Spearman(`profile_dev`, deposit deficit) = +0.951**, n = 48, 0 of 200 000 draws as extreme,
tied fraction 4/48, 46 distinct predictor values. The group quantity does not predict how much
restorability is lost; the profile deviation does. That is the same verdict H-IFF returned,
reached from the other side, **and it was not pre-registered.**

---

## 3. Q1 — what it does and does not license

1. **Sufficiency is a usable criterion and is worth keeping.** Transitive ⟹ restorable, with no
   computation beyond the group. Every linear substrate qualifies for free.
2. **Necessity is dead.** "Some patterns, once damaged, cannot be restored at any price, and
   *which ones* is decided by their symmetry group" — the sentence the campaign was built to
   test — is **false as stated**. The correct sentence is: *which ones is decided by a
   combinatorial regularity of the decoder's cells, which symmetry implies but does not exhaust.*
3. **Any confirmation of H-IFF would have been a numerically verified equivalence on a finite
   roster, in a setting where the analogous general statement is known false** (§5). Since it
   was refuted instead, that caveat now applies to sufficiency alone.
4. **No mechanization.** (T) is an elementary orbit argument and would be a cheap Lean brick if
   it were wanted; saying so is not having one.

---

## 4. Q1 — the column-order control and the censuses (the sibling's arm, re-derived)

Full report: `RENT_SCALING_SUBSET_RESULTS.md`. Every count below I re-derived from
`rent_scaling_q1_census_{12,20,24}.json`; the framing is the sibling's and I have not softened it.

### 4.1 H-SUBSET — the pre-registered arm. Verdict: **UNDERPOWERED, not confirmed**

AMENDMENT 1's roster (`N ∈ {12,20,24,28}`, `6 ≤ k ≤ min(N−1,20)`, 5 seeded random `k`-column
subsets each, draws written before the first evaluation) produced 250 structures, 236 distinct
and non-canonical, **0 H-IFF violations, 0 (T) violations, 18 H-ORBIT violations, 0 undetermined.**

**0 of 236 is not support, and the reason was found only after the arm ran.** H-IFF's necessity
direction can only be falsified by a **restorable** structure; the arm produced **6** of those
out of sample. **The effective sample size against the hypothesis under test is 6, not 236** —
quoting 236 would be precisely the failure the harvest gate *floor matched to sample size* names.

**And neither known counterexample was inside the roster.** The amendment fixed
`6 ≤ k ≤ min(N−1,20)` for cost, in advance, with no counterexample known. The canonical
violations sit at `k = 5` (below the floor) and `k = 23` (above the cap). An honestly chosen
cost bound sat exactly one width above the only layer where the phenomenon occurs. **The arm
answers a different question than the one it was written for.**

### 4.2 The censuses — sampling replaced by exhaustion. **Post-hoc, motivation disclosed.**

| order | widths | subsets | restorable | counterexamples | undetermined | (T) violations |
|---|---|---|---|---|---|---|
| Paley-12 | `k = 3…11` (complete) | 1 981 | 628 | **396** (all at `k = 5`) | 0 | 0 |
| Paley-20 | `k = 3…6` | 43 605 | 969 (all the trivial `k=3` collapse) | **0** | 0 | 0 |
| Paley-24 | `k = 21…23` | 277 | 1 | **1** (at `k = 23`) | 0 | 0 |
| **total** | | **45 863** | **1 598** | **397** | **0** | **0** |

At `k = 5` on Paley-12 the census is total: **396 of the 462 five-subsets are restorable, and
all 396 are counterexamples.** Restorability is strongly **non-monotone in `k`** — universal at
3, absent at 4, near-universal at 5, absent at 6–8, universal again at 9–11.

### 4.3 The reason not to overcount — verified here, not accepted

> **The 66 NON-restorable 5-subsets are exactly the blocks of the Steiner system S(4,5,11).**

**Recomputed independently for this document:** the 66 non-restorable 5-subsets are 66 *distinct*
blocks, and the 330 four-subsets of the 11 columns are covered with multiset `{1: 330}` — every
four-subset in exactly one block. The mechanism is visible in `|S|`: the 66 blocks leave
`|S| = 11` (two rows collide, and a collapsed support is not restorable); the 396 non-blocks
leave `|S| = 12` and **every one is restorable and intransitive**. Corroboration at `k = 4`: all
330 four-subsets collapse to `|S| = 11`, and `330 = 66 × 5` is exactly the block/four-subset
incidence count.

All 396 carry **identical invariants** — re-derived: `|Aut| = 20` in all 396, orbits `[10,2]` in
all 396, exactly one `R`-level-set in all 396, `profile_dev` exactly 0.0 in all 396. The natural
reading is a single orbit under the `M₁₁` action: **one counterexample up to equivalence,
occurring 396 times.** *Stated as a reading:* the invariants agree and the Steiner property
holds; **the orbit decomposition of `M₁₁` on 5-subsets was not computed**, so "one equivalence
class" is an inference from matching invariants, not a proof.

**Paley-20 is the control and it is a clean negative:** outside the trivial `k = 3` collapse,
**0 of 42 636** subsets at `k = 4, 5, 6` is restorable at all. The `k = 5` counterexample layer
is *not* a generic width effect — change the Hadamard order and the layer disappears. That is
the strongest available evidence that the 396 is **one structure**.

**Anyone quoting "396 counterexamples" as 396 findings is overcounting by up to 396×.**

---

## 5. Prior art — and it predicted this outcome. Credit in the text, not a footnote.

`RENT_SCALING_PRIOR_ART.md` (`648ee07`), required by prereg §5.2 to run **before** results are
written and to report whatever it found. *(Received from the sibling; searches not re-run.)*
It binds three things:

1. **Gillespie & Praeger, *Uniqueness of certain completely regular Hadamard codes*
   (arXiv:1112.1247, 2011; J. Combin. Theory Ser. A, 2013), classify the `k = 11` object.**
   Binary completely regular codes with `(m, δ) = (12,6)` and `(11,5)` are unique up to
   equivalence, their automorphism groups modulo the kernel of a particular action are
   **Mathieu**, and they are consequently **necessarily completely transitive**. That is our
   Paley-12 substrate. **The Mathieu chain 7920 / 720 / 144 / 48 in `aut_counts_exact.json`
   REPRODUCES A PUBLISHED CLASSIFICATION.** It is the campaign's most striking-looking
   group-theoretic result and it is somebody else's theorem. It is reported as a reproduction.
2. **Completely regular (Delsarte 1973) ⊋ completely transitive (Solé 1990).** "Regularity
   implies symmetry" is *known false* in the neighbouring setting, and complete transitivity is
   a **proper** subfamily. **H-IFF's necessity direction dying is the EXPECTED outcome under
   the literature** — exactly the prior the prereg §2.2 staked in advance, before any group was
   computed. The refutation in §2.2 is therefore not a surprise to the field; the surprise was
   ours. That S(4,5,11) turns up as the exact complement of the counterexample class is
   consistent with it: S(4,5,11) is the `M₁₁` Steiner system, and `M₁₁` is the group the
   classification names.
3. **"Transitive code" is a standard named property** (Rifà–Pujol); the **Best code**
   (length 10, size 40, `d = 4`) is the named witness that transitive ⊅ propelinear. The
   property this campaign computes is not new and has an established name. **Our contribution
   on that side is a computation, not a concept.**

**Not found under any description searched:** the restorability criterion itself — "the
nearest-point decoder with uniform tie-breaking fixes the uniform measure on `S` for every
radial kernel iff `R_i(a)` is `i`-independent" — and H-IFF as a statement. **"Not found" is
weaker than "new"**: four query families over one afternoon, with the survey PDF
(arXiv:1703.08684) failing to extract and therefore **not relied on**. The likeliest hiding
place for a pre-emption is the Voronoi-cell / uniformly-packed literature around Delsarte's
outer distribution, which that PDF would have covered.

**A trap the prior art flags and this document obeys:** our `|C|` is the orbit of the zero word
under the **full isometry group**, `{c : ∃σ, σ(S) = S ⊕ c}`, which permits a permutation and is
therefore **≥ the published kernel** `K(S) = {c : S ⊕ c = S}` (Phelps–Rifà–Villanueva 2005).
`|Aut| = |P|·|C|` is orbit–stabiliser and is correct as written; **it is not the published
kernel and no number here may be compared to a published kernel dimension without that
correction.** No such comparison is made in this document.

---

## 6. Q2 — does rent/nat plateau?

### 6.1 The curve

`ARM A` now runs `k = 5…31` contiguously (27 widths × 6 conditions = 162 rows); `ARM B` runs
`k = 5…32` (28 × 6 = 168). The 15 new tiers contributed 90 rows, **0 dropped**.

`ARM A`, rent per nat, the new tier and the width before it:

| `k` | `\|S\|` | ε=.01/10% | ε=.01/50% | ε=.01/1 nat | ε=.05/10% | ε=.05/50% | ε=.05/1 nat |
|---|---|---|---|---|---|---|---|
| 24 | 28 | 0.11568 | 0.09231 | 0.12132 | 0.51138 | 0.40335 | 0.53495 |
| 25 | 28 | 0.11299 | 0.09077 | 0.11932 | 0.50025 | 0.39735 | 0.52667 |
| 26 | 28 | 0.11052 | 0.08936 | 0.11743 | 0.49004 | 0.39183 | 0.51883 |
| 27 | 28 | 0.10825 | 0.08806 | 0.11564 | 0.48063 | 0.38671 | 0.51142 |
| **28** | **32** | 0.10775 | 0.08801 | 0.11556 | 0.47802 | 0.38636 | 0.51042 |
| 29 | 32 | 0.10574 | 0.08684 | 0.11390 | 0.46968 | 0.38176 | 0.50353 |
| 30 | 32 | 0.10387 | 0.08576 | 0.11233 | 0.46192 | 0.37746 | 0.49699 |
| 31 | 32 | 0.10212 | 0.08475 | 0.11083 | 0.45468 | 0.37345 | 0.49077 |

Over the whole measured range `k = 5 → 31`, rent per nat falls by a factor of **1.27× to 2.68×**
depending on condition (largest at ε=.01/10 %, smallest at ε=.05/1 nat). **The minimum is at
`k = 31` in all six conditions** — the last measured point — and the curve is *not* strictly
monotone anywhere, because of the sawtooth.

### 6.2 The fits — F1–F4, parameters reported honestly

Pre-registered forms fitted to `ln(rent/nat)` over **all** measured `k = 5…31` on ARM A, at each
of the 6 conditions independently, compared by `AIC = n·ln(SSE/n) + 2p`. **This is descriptive
model comparison on exact data, not statistical inference, and the prereg labelled it so — a
label that is doing real work here, see §6.4.**

| condition | best | AIC F1 | AIC F2 | AIC F3 | AIC F4 | `ĉ` | `[c_lo, c_hi]` | `0.98·min` | **resolved?** |
|---|---|---|---|---|---|---|---|---|---|
| ε=.01, 10 % | F2 | −205.96 | **−213.04** | −196.67 | −120.28 | 0.03636 | [0.01593, 0.05147] | 0.10008 | **YES** |
| ε=.01, 50 % | F2 | −197.55 | **−216.01** | −201.44 | −133.59 | 0.05373 | [0.04102, 0.06255] | 0.08306 | **YES** |
| ε=.01, 1 nat | F2 | −206.90 | **−212.67** | −210.94 | −192.51 | 0 | [0, 0.04012] | 0.10862 | no |
| ε=.05, 10 % | F2 | −210.28 | **−220.24** | −202.90 | −122.26 | 0.17187 | [0.09366, 0.23098] | 0.44559 | **YES** |
| ε=.05, 50 % | F2 | −220.23 | **−229.78** | −217.45 | −148.89 | 0.19569 | [0.11502, 0.24648] | 0.36598 | **YES** |
| ε=.05, 1 nat | **F4** | −176.96 | −180.01 | −215.55 | **−217.56** | 0 | [0, 0.23655] | 0.48095 | no |

Fitted parameters, the pre-registered fit (`a·k^{−b}`, `c + a·k^{−b}`, `c + a·e^{−bk}`, `a + b·k`):

| condition | F1 `a`, `b` | F2 `a`, `b`, `c` | F3 `a`, `b`, `c` | F4 `a`, `b` |
|---|---|---|---|---|
| ε=.01, 10 % | 0.6038, 0.5222 | 0.7020, 0.6890, **0.03640** | 0.2907, 0.1220, 0.09823 | 0.2234, −0.004312 |
| ε=.01, 50 % | 0.3126, 0.3866 | 0.4051, 0.7449, **0.05374** | 0.1644, 0.1296, 0.08375 | 0.1524, −0.002431 |
| ε=.01, 1 nat | 0.2463, 0.2248 | 60.81, 0.00051, **−60.59** ⚠ | 0.0928, 0.0505, 0.09256 | 0.1673, −0.001912 |
| ε=.05, 10 % | 2.5272, 0.5047 | 2.9488, 0.6826, **0.17189** | 1.2301, 0.1220, 0.43795 | 0.9698, −0.018350 |
| ε=.05, 50 % | 1.1215, 0.3238 | 1.1800, 0.5493, **0.19536** | 0.5299, 0.1128, 0.36361 | 0.6221, −0.008895 |
| ε=.05, 1 nat | 0.8867, 0.1585 | 274.94, 0.00035, **−274.11** ⚠ | 282.93, 0.00002, **−282.24** ⚠ | 0.6883, −0.006380 |

⚠ **These are degenerate, and reporting "F2 wins" there without saying so would be dishonest.**
In the two `1 nat` conditions F2 (and F3 in one) runs off to an unbounded reparametrisation —
`a → ∞`, `b → 0`, `c → −a` — which is a near-linear function in disguise, not a power law
decaying to a floor. **The pre-registered floor rule caught both**: neither resolves, because the
profile interval contains 0. **And in one of them the LINEAR CONTROL F4 wins outright**, beating
F1 by ΔAIC 40.6. A control winning is a caution about the whole smooth-fit family over this
range, and it is recorded as one.

### 6.3 The verdict of record — and a defect in the pre-registration

| rule | fires? |
|---|---|
| **PLATEAU-WITH-FLOOR** (F2/F3 beats F1 by ΔAIC ≥ 4 **and** `c_lo > 0` **and** `c_hi < 0.98·min`) | **4 / 6** — rule needs ≥ 4 → **FIRES** |
| **CONTINUED DECLINE** (F1 wins, or `[c_lo, c_hi]` contains 0) | 2 / 6 → does not fire |
| **SAWTOOTH-DOMINATED** (step-vs-island residual exceeds the fit's RMS residual) | **5 / 6** → **FIRES** |

> ### *** Q2 VERDICT OF RECORD: PLATEAU-WITH-FLOOR + SAWTOOTH-DOMINATED ***

**Both fired, and the pre-registration wrote them as alternatives when they are not.** "The
trend declines to a nonzero floor" and "the residual about that trend is dominated by the step
structure" are statements about different things and the operationalisation lets both be true at
once. **That is a defect in `RENT_SCALING_PREREG.md` §3.2, stated here rather than resolved by
whichever branch the adjudicating code happened to test first.** Both outcomes are reported;
neither is suppressed.

Sawtooth detail, all six conditions:

| condition | step-minus-island residual | RMS residual | dominant? |
|---|---|---|---|
| ε=.01, 10 % | +0.03162 | 0.02048 | **yes** |
| ε=.01, 50 % | +0.02819 | 0.02394 | **yes** |
| ε=.01, 1 nat | +0.03201 | 0.02013 | **yes** |
| ε=.05, 10 % | +0.02698 | 0.01891 | **yes** |
| ε=.05, 50 % | +0.02363 | 0.01573 | **yes** |
| ε=.05, 1 nat | +0.02952 | 0.03505 | no |

### 6.4 What the floor verdict is worth — four things that qualify it

**(a) The 4 of 6 is structured, not random.** The floor resolves in **exactly the four
fixed-*fraction* target conditions** (10 % and 50 % of `share_max`, at both `ε`) and in
**neither fixed-1-nat condition**. As `k` grows a fixed 1-nat target becomes a vanishing
fraction of `share_max`, so the two `abs` conditions are probing a different regime — which is
also where the F2 parameters degenerate (§6.2). The pattern is systematic and is stated rather
than averaged over.

**(b) The floor is not an artifact of the sawtooth — I tested that.** Absorbing the step
structure into three `k mod 4` dummy offsets (class 3 as reference) and refitting leaves
**PLATEAU-WITH-FLOOR at 4/6**, with the floor intervals essentially unchanged and *tighter*
(e.g. ε=.01/10 %: [0.02614, 0.04779] against [0.01593, 0.05147]). The floor survives the
control. *Post-hoc, not pre-registered, and labelled.*

**(c) The floor is NOT robust to dropping the low-`k` points, and this is the real caveat.**
Refitting over sub-ranges:

| range | PLATEAU-WITH-FLOOR | CONTINUED DECLINE |
|---|---|---|
| `k ≥ 5` (**the pre-registered fit**) | **4 / 6** | 2 / 6 |
| `k ≥ 12` | 5 / 6 | 1 / 6 |
| `k ≥ 16` | **3 / 6 — below the rule's own threshold** | 2 / 6 |

The identification leans on the small-`k` end of the range — which is where the power-law form
does most of its work and where the substrate changes character fastest (`|S|` steps
8→12→16→20 within `k = 5…19`). **A verdict that would flip if the range started eleven widths
later is a weak verdict, and it is reported as one.** *(Sub-range refits are post-hoc.)*

**(d) The AIC is not a likelihood ratio here.** SAWTOOTH-DOMINATED firing 5/6 means the
residuals are systematically structured, not noise, so the Gaussian-SSE AIC form is descriptive
bookkeeping — which is exactly why the prereg pre-labelled it "descriptive model comparison on
exact data, not statistical inference". That label is load-bearing and is not a formality.

**(e) The curve has not flattened.** At `k = 31` rent/nat is still falling at roughly 1.7 pp per
step (ε=.01/10 %: `L(31) = −1.69 pp`). A resolved floor at 0.036 against a measured 0.102 means
the fit *extrapolates* to a nonzero asymptote, not that the data has reached one. **"A floor is
resolved by the fit" and "the curve is still declining at the last point" are both true, and
neither may be quoted without the other.**

> **Per prereg §3.2, inherited from the parent and not weakened by having seven more points: a
> floor, resolved or not, is a curve parameter over `5 ≤ k ≤ 31`. It is never "the price of
> habit" and never an asymptotic cost. NO `k > 31` CLAIM IS MADE IN EITHER DIRECTION.**

### 6.5 What Q2 changed relative to the parent

The parent's P-PLATEAU verdict at `k ≤ 24` was **CONTINUED DECLINE with an unidentifiable
floor**: power decline won by AIC at 3 of 4 conditions and the fitted `c` landed at 94.5–97.4 %
of the smallest measured rent/nat in *every* condition — the signature of a parameter pinned to
the last data point. **Seven more widths moved it.** In the four resolving conditions the floor
now sits at **36–63 % of the `k = 31` value** (profile intervals spanning 16–74 %), with the
interval's upper end comfortably below the `0.98·min` rail rather than jammed against it. That
is the specific thing the extension
was run to find out, and it returned a different answer than the parent's range could support —
with the qualifications of §6.4 attached.

| resolving condition | floor `ĉ` as % of the `k = 31` value | profile interval as % of it |
|---|---|---|
| ε=.01, 10 % | 35.6 % | [15.6 %, 50.4 %] |
| ε=.01, 50 % | 63.4 % | [48.4 %, 73.8 %] |
| ε=.05, 10 % | 37.8 % | [20.6 %, 50.8 %] |
| ε=.05, 50 % | 52.4 % | [30.8 %, 66.0 %] |

---

## 7. Q2 — the staked steps

### 7.1 P-STEP28 (prereg §3.3) — **the raw form FIRED; the trend-corrected form survives**

The prediction had two parts and they part company.

**Raw:** `rent/nat(28) > rent/nat(27)` on ARM A, predicted UP, predicted amplitude 0.063 %.
**Measured: 0 of 6.** The raw uptick does not occur in any condition.

**And it could not have.** The prereg's own §1.3 computed the `k = 28` density tooth as
**+0.063 %** — I re-derive the ceiling's raw log-jump at `k = 28` as **−0.0634 pp**, matching
that arithmetic exactly — while the ongoing decline of rent/nat at `k = 28` runs at **−1.13 to
−1.79 pp per step** depending on condition. A +0.063 % packing tooth cannot flip a trend an order
of magnitude larger. **§1.3 said in advance that a null here
would be "the predicted difficulty and not a surprise"**, and then §3.3/§3.4 staked binary
raw-uptick tests anyway. **That is an internal inconsistency in the pre-registration and it is
disclosed, not used to rescue the prediction.** The raw prediction is recorded FIRED.

**Trend-corrected** — the statistic §3.3 said "carries the weight", `tooth(k₀) = L(k₀) −
mean(L(k₀+1), L(k₀+2), L(k₀+3))`:

| condition | `k=24` raw | `k=24` tooth | elasticity | `k=28` raw | `k=28` tooth | elasticity |
|---|---|---|---|---|---|---|
| ε=.01, 10 % | dn | **+1.737 pp** | 1.68 | dn | **+1.330 pp** | 1.76 |
| ε=.01, 50 % | UP | **+1.587 pp** | 1.53 | dn | **+1.200 pp** | 1.58 |
| ε=.01, 1 nat | UP | **+1.713 pp** | 1.65 | dn | **+1.321 pp** | 1.74 |
| ε=.05, 10 % | dn | **+1.468 pp** | 1.42 | dn | **+1.126 pp** | 1.49 |
| ε=.05, 50 % | dn | **+1.364 pp** | 1.32 | dn | **+1.040 pp** | 1.37 |
| ε=.05, 1 nat | dn | **+1.447 pp** | 1.40 | dn | **+1.115 pp** | 1.47 |

The ceiling's own trend-corrected teeth, re-derived from each arm's own `|S|`: **−1.035 pp at
`k = 24`** and **−0.757 pp at `k = 28`**. Elasticity is the rent tooth over the negated ceiling
tooth.

**§3.3's falsifier — "trend-corrected residual negative at both step points, or elasticity
outside [0.3, 3] at both" — does NOT fire.** Positive at both, 6/6 and 6/6; elasticity
**1.32–1.76**, inside the pre-registered `[0.3, 3]`. The packing account of the sawtooth survives
in the statistic designed to test it.

*One detail reported rather than rounded:* the prereg also said it expected elasticity "in the
1–1.5 band the parent measured at `k ≤ 20`". **6 of the 12 readings sit above 1.5** (max 1.76).
That is not a falsifier — the stated falsifier is `[0.3, 3]` — but the elasticity is running at
or slightly above the parent's range rather than inside it, and half the readings say so.

**The raw uptick decays with `k` while the trend-corrected tooth does not** — upticks per step
point across ARM A: `k=8`: 6/6, `k=12`: 5/6, `k=16`: 4/6, `k=20`: 4/6, `k=24`: 2/6, `k=28`:
**0/6**. The tooth is stable in elasticity; what changes is its size relative to the trend it
must overcome.

### 7.2 P-STEP32 (AMENDMENT 2) — **CONFIRMED, 6 of 6, inside the pinned band**

The adjudicator, the backward baseline `k = 29, 30, 31`, the band `[0.5, 2.0] × 3.869 pp` and
the ≥ 4/6 threshold were all committed at `aac3149` **while B32 was still computing**. The
coordinator ran the rule mechanically after both agents hit their limits
(`RENT_SCALING_Q2_ADJUDICATION.md`, `44329f5`). **I re-derived it from
`rent_scaling_q2_B*.json` with my own code; the numbers agree to the last quoted digit and I
correct nothing.**

ARM B, rent per nat:

| condition | k=25 | 26 | 27 | 28 | 29 | 30 | 31 | **32** |
|---|---|---|---|---|---|---|---|---|
| ε=.01, 10 % | 0.11484 | 0.11229 | 0.10993 | 0.10777 | 0.10574 | 0.10387 | 0.10212 | **0.10809** |
| ε=.01, 50 % | 0.09210 | 0.09062 | 0.08926 | 0.08801 | 0.08684 | 0.08576 | 0.08475 | **0.08919** |
| ε=.01, 1 nat | 0.12112 | 0.11917 | 0.11731 | 0.11557 | 0.11390 | 0.11233 | 0.11083 | **0.11719** |
| ε=.05, 10 % | 0.50728 | 0.49675 | 0.48702 | 0.47806 | 0.46968 | 0.46192 | 0.45468 | **0.47665** |
| ε=.05, 50 % | 0.40234 | 0.39661 | 0.39129 | 0.38638 | 0.38176 | 0.37746 | 0.37345 | **0.39045** |
| ε=.05, 1 nat | 0.53339 | 0.52534 | 0.51768 | 0.51046 | 0.50353 | 0.49699 | 0.49077 | **0.51380** |

| condition | `L(29)` | `L(30)` | `L(31)` | baseline sd | `L(32)` | **tooth(32)** | sign | band |
|---|---|---|---|---|---|---|---|---|
| ε=.01, 10 % | −1.899 | −1.787 | −1.692 | 0.104 pp | +5.676 | **+7.469 pp** | + | in |
| ε=.01, 50 % | −1.337 | −1.254 | −1.182 | 0.078 pp | +5.106 | **+6.363 pp** | + | in |
| ε=.01, 1 nat | −1.456 | −1.391 | −1.339 | 0.059 pp | +5.577 | **+6.972 pp** | + | in |
| ε=.05, 10 % | −1.770 | −1.666 | −1.579 | 0.096 pp | +4.720 | **+6.392 pp** | + | in |
| ε=.05, 50 % | −1.203 | −1.131 | −1.069 | 0.067 pp | +4.450 | **+5.585 pp** | + | in |
| ε=.05, 1 nat | −1.367 | −1.308 | −1.259 | 0.054 pp | +4.586 | **+5.897 pp** | + | in |

**Positive in 6/6** (rule needed ≥ 4/6) and **inside `[1.935, 7.738] pp` in 6/6.** Both clauses
of the pinned CONFIRMED condition are met. Every tooth clears its own baseline scatter by
**67× to 118×** (baseline sd over the three `L` values, `ddof = 1`, the convention in the table
above; the coordinator's `ddof = 0` gives 82× to 145×, which is the source of its "65× to 145×"
— the conventions differ, the conclusion does not). This is not a marginal call under either.

**AMENDMENT 2's `−3.869 pp` ceiling tooth is verified.** *A note on how, because I got it wrong
first:* computing the ceiling from `N₀(k) = 4⌈(k+1)/4⌉` — ARM **A**'s size function — gives
−0.726 pp and would have made the band wrong by 5×. ARM B's own `|S|` steps 32 → 64 at `k = 32`,
and `density_B(k) = ln2 − ln|S_B(k)|/k` gives `L(29), L(30), L(31) = +0.00747, +0.00692,
+0.00643` and `L(32) = −3.1749 pp`, hence **tooth = −3.8689 pp** — the amendment's figure, to
its quoted precision, with its own quoted intermediate values reproduced. **The amendment was
right; my first check was not, and the correction is recorded here rather than silently
dropped.**

Note the amendment's sharp arithmetic feature, which holds: `share_max(B31) = 31·ln2 − ln32` and
`share_max(B32) = 32·ln2 − ln64` are **exactly equal at 18.021827** — at `k = 32` ARM B holds
the same total whole-only share over one more slot, so nothing about the amount of pattern
changes, only the packing. **That is what makes this the campaign's cleanest step.**

### 7.3 H-DISSOC-2 (prereg §3.4) — **FIRED**

> Predicted: ARM A ticks up at `k = 28` in ≥ 4 of 6 conditions **and** ARM B in ≤ 1 of 6.
> Falsifier: both arms tick, **or neither**.

**Measured: ARM A 0/6, ARM B 0/6. Neither ticks. The falsifier fires. H-DISSOC-2 is dead and is
recorded dead.**

It failed for the reason §7.1 gives — the raw-uptick form was arithmetically unwinnable on ARM A
once the prereg's own §1.3 tooth (+0.063 %) is set beside the trend (−1.8 pp/step) — and that is
a defect in the test's design, disclosed. **It is not a rescue to observe that the dissociation
is present in the trend-corrected statistic, but it is a fact and it is reported separately:**

| condition | A tooth(28) | B tooth(28) | A − B |
|---|---|---|---|
| ε=.01, 10 % | +1.330 pp | −0.197 pp | +1.526 pp |
| ε=.01, 50 % | +1.200 pp | −0.154 pp | +1.354 pp |
| ε=.01, 1 nat | +1.321 pp | −0.099 pp | +1.420 pp |
| ε=.05, 10 % | +1.126 pp | −0.184 pp | +1.310 pp |
| ε=.05, 50 % | +1.040 pp | −0.130 pp | +1.170 pp |
| ε=.05, 1 nat | +1.115 pp | −0.093 pp | +1.208 pp |

ARM A's `|S|` steps 28 → 32 at `k = 28`; ARM B's does not (32 → 32). Trend-corrected, **A is
positive 6/6 (mean +1.19 pp) and B is negative 6/6 (mean −0.14 pp)**, separating by +1.17 to
+1.53 pp in every condition. **The dissociation the hypothesis was about is visible in the
statistic the prereg itself said carries the weight — but H-DISSOC-2 was staked on the raw form
and the raw form fired. The stake is dead; a differently-worded stake would have survived; and
writing the second sentence without the first would be the failure this programme exists to
avoid.**

---

## 8. ARM A versus ARM B — the comparison, and the construction facts

### 8.1 Where the arms are the same object

Prereg §3.4 required this be **checked and reported as a construction fact, not a result**.
Re-derived from the tier metadata and the rent values:

| `k` | relation |
|---|---|
| 5, 6, 7 | **identical** (`\|S\| = 8`, rent equal to 0 ulp) |
| 8–11 | **differ**: A is Paley-12 (`\|S\|=12`), B is `[k,4]` (`\|S\|=16`). A is 7–15 % cheaper |
| 12 | differ marginally (`\|S\|=16` both, different codes; A cheaper by 0.25 %) |
| 13, 14, 15 | **identical** |
| 16–27 | **differ**: A is Paley (`\|S\| = 20, 24, 28`), B is `[k,5]` (`\|S\| = 32`) |
| **28** | **different codes, same size 32** — A is the Sylvester truncation, B the exhaustively-best `[28,5]`; **A is cheaper by 1.0e−4 relative**, i.e. all but identical |
| 29, 30, 31 | **identical** — the full Sylvester-32 OA *is* the simplex `[31,5]`, as the prereg predicted |
| 32 | A does not exist (`N₀ = 36` is out of reach); B is `[32,6]`, `\|S\| = 64` |

So the arms differ genuinely at `k = 25, 26, 27` exactly as the prereg said, and at `k = 28` they
are distinct objects that agree to four decimal places. **The `k = 28` dissociation test was
therefore well-posed** (A stepped, B did not) even though its raw form fired.

### 8.2 Where both exist, A is cheaper — and the gap closes as their sizes converge

`(rent_B / rent_A − 1)`, the cost of using the larger linear code instead of the minimum-size OA:

| condition | k=24 | k=25 | k=26 | k=27 | k=28 |
|---|---|---|---|---|---|
| ε=.01, 10 % | +1.671 % | +1.640 % | +1.598 % | +1.551 % | +0.010 % |
| ε=.01, 50 % | +1.503 % | +1.463 % | +1.417 % | +1.370 % | +0.005 % |
| ε=.01, 1 nat | +1.523 % | +1.507 % | +1.478 % | +1.443 % | +0.009 % |
| ε=.05, 10 % | +1.431 % | +1.405 % | +1.370 % | +1.330 % | +0.008 % |
| ε=.05, 50 % | +1.281 % | +1.255 % | +1.221 % | +1.184 % | +0.006 % |
| ε=.05, 1 nat | +1.290 % | +1.277 % | +1.254 % | +1.225 % | +0.007 % |

The penalty is **+1.2 % to +1.7 %** wherever the sizes differ (28 vs 32) and collapses to
**~0.01 %** the moment they coincide.

**This does NOT isolate packing from linearity, and saying it did would be the easy error.**
Across `k = 24…27` the two arms differ in *both* respects at once — A is the non-linear
Paley-II-28 (`|S| = 28`), B is the linear `[k,5]` (`|S| = 32`) — so the +1.5 % is a confounded
comparison. At `k = 28` **both** differences vanish together (both linear, both size 32) and so
does the gap. The one place the confound breaks is `k = 12`, where both arms are linear with
`|S| = 16` and differ only in which code: the gap there is **+0.25 %**, and at `k = 28`, same
size and same linearity again, **+0.010 %**. So code choice alone is worth a few tenths of a
percent at small `k` and essentially nothing by `k = 28`; **the size/linearity split is not
resolved by this data and is not claimed to be.**

### 8.3 The plateau verdict is **arm-dependent**, and that was not pre-registered

Applying the same §3.2 fit machinery to ARM B over `k = 5…32`:

| rule | ARM A (`k=5…31`) | **ARM B (`k=5…32`)** |
|---|---|---|
| PLATEAU-WITH-FLOOR | **4 / 6** | **0 / 6** |
| CONTINUED DECLINE | 2 / 6 | **6 / 6** |
| SAWTOOTH-DOMINATED | 5 / 6 | 5 / 6 |

**ARM B returns CONTINUED DECLINE in all six conditions — the opposite verdict.** The prereg
fixed the plateau question on ARM A (§3.2: "Fit … on `ARM A` over all measured `k`"), so ARM A's
is the **verdict of record** and ARM B's is an unregistered extension. But the disagreement is
real and is reported at the same volume: a plausible structural reason is that ARM B's `|S|`
is **constant at 32 across `k = 16…31`** while ARM A's tracks `N₀(k) ≈ k`, so ARM B's density
`ln2 − ln32/k` rises smoothly with no packing structure to arrest it. *Offered as a reading of
the size columns, not as a result.*

**This is the single largest caveat on §6.3.** A floor identified on one arm and absent on
another, over overlapping ranges of the same quantity, is not a robust floor.

### 8.4 A correction to the coordinator's fragment

`RENT_SCALING_Q2_ADJUDICATION.md` states: *"The plateau question — NO floor in the measured
range … No plateau is identified in this range."* **Re-derived, that sentence is right about
what it measured and wrong as an answer to the pre-registered question.** It is correct that
ARM B declines smoothly and monotonically over `k = 25…31` with the `k = 32` tooth explained by
packing, and correct that ARM B shows no floor — §8.3 confirms ARM B at 0/6. **But the
pre-registered plateau rule is fitted on ARM A over all measured `k`, and there it FIRES at
4/6.** The fragment was explicitly scoped ("does not fit F1/F2/F3") and flagged itself as a
fragment; this paragraph closes it rather than criticises it. **The corrected statement of
record is §6.3 plus §6.4 plus §8.3, and the fragment's plateau paragraph is superseded.**

---

## 9. Ceiling fractions, with their denominators NAMED

Prereg §0 requires every share reading quoted against `share_max(k) = k·ln2 − ln N₀(k)` — the
substrate's own attained maximum, the *sharp* denominator — with the machine-checked cap
tabulated alongside so the two are never confused.

### 9.1 The two denominators, and which theorem licenses which

The machine-checked cap in force is **`Core/HammingCap.shareK_le_of_four_pair_uniform`,
`(k−3)·ln 2`**. `share_max ≤ (k−3)·ln2 ⟺ |S| ≥ 8`, which holds at every `k ≥ 5` in this roster
(`|S| ∈ {8,12,16,20,24,28,32,64}`), so **`share_max` is the tighter denominator and is the one
quoted**; the Lean cap is the cross-substrate comparator.

| tier | `k` | `\|S\|` | `share_max` | `(k−3)·ln2` | `share_max / cap` |
|---|---|---|---|---|---|
| A25 | 25 | 28 | 13.99648 | 15.24924 | 0.9178 |
| A26 | 26 | 28 | 14.68962 | 15.94239 | 0.9214 |
| A27 | 27 | 28 | 15.38277 | 16.63553 | 0.9247 |
| A28–A31 = B28–B31 | 28–31 | 32 | 15.94239 … 18.02183 | 17.32868 … 19.40812 | 0.9200 … 0.9286 |
| B25 | 25 | 32 | 13.86294 | 15.24924 | 0.9091 |
| B26 | 26 | 32 | 14.55609 | 15.94239 | 0.9130 |
| B27 | 27 | 32 | 15.24924 | 16.63553 | 0.9167 |
| **B32** | 32 | 64 | 18.02183 | 20.10127 | **0.8966** |

The two denominators never differ by more than **11 %** anywhere in this roster, so — unlike the
near-independent substrates that motivated the named-denominator gate — **no headroom statement
here is sensitive to which is used.** Stating that is the point of the gate; both are given so a
reader can check it rather than take it.

**The gate's own named denominators do not apply here, and that is a citation check, not an
omission.** `Core/ThirdCap.lean`'s `share_le_log_two` and `share_le_grouping_gaps` are typed on
`Bool × Bool × Bool` — **three binary slots**. They are `k = 3` theorems, they are not used, and
they must not be imported into this table. The prereg said so in §0 and the type signatures
confirm it.

### 9.2 The restorability ceilings, and the floor below which they are not measurements

The share targets themselves (10 %, 50 %, 1 nat of `share_max`) sit orders above any numerical
floor, so their fractions are unambiguous. **The restorability ceiling deficits are the ones
that need a floor**, and the amendment's cap/floor ≥ 100 bar is applied per structure:

- **On all 5 restorable structures in the ceiling pass the ceiling is exactly
  `1.000000000000`** at both `ε` — full upkeep restores the design state to the last digit,
  which is what restorable means, and a free check that the ceiling instrument agrees with the
  `profile_dev` criterion.
- **Of the 48 lossy structures, 47 clear the bar at `ε = 0.05` and 46 at `ε = 0.01`.** The
  failures are named: **`H24/k22` at both `ε`** (deficit 1.33e−15 against a solver residual
  8.7e−16) and **`H20/k19` at `ε = 0.01`** (4.44e−16 against 1.32e−16). For those the deficit is
  **declared unresolved**, not quoted as a small number.
- Among the new Q2 tiers, `A25`, `A26`, `A27` are lossy by the `ε`-free criterion
  (`profile_dev` 8.07e−4, 4.41e−4, 1.86e−4) yet return `q=1` ceiling fractions of
  1.000000000000, 0.999999999992, 0.999999999992 — deficits of order 1e−11, **at the floor the
  zero-cell gate names.** They are reported as *not measurably lossy at these `ε`*, and not as
  measurements.

### 9.3 The economics: losing restorability is expensive for small habits and nearly free for large ones

From the sibling's ceiling pass over all 250 subset structures at `ε = 0.01` (counts re-derived;
the deficit table is theirs):

| `k` (full support) | 6 | 7 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| median deficit `1 − ceiling_frac` | 1.8e−2 | 3.0e−4 | 1.9e−4 | 2.9e−5 | 6.7e−6 | 8.9e−7 | 1.3e−6 | 1.1e−7 | 2.1e−7 |
| worst in cell | 6.3e−2 | 7.8e−4 | 7.6e−4 | 1.7e−4 | 3.2e−5 | 7.6e−6 | 7.9e−6 | 3.4e−7 | 1.7e−6 |

Overall median 5.4e−6, 90th percentile 9.7e−3, maximum **6.3e−2** (`H12/k6/s4`, full support, so
not a collapse artifact). **The sibling corrected its own earlier "never below 0.99999" here —
wrong by four orders at small `k` — and that correction stands in their file.**

**What it means for the campaign's framing.** The transitive/intransitive boundary is exact and
sharp — twelve orders of magnitude separate the two populations in `profile_dev`. Its **price**
is **size-dependent and falls fast**: a small habit that is not restorable forfeits several
percent of its whole-only share under full upkeep; by `k ≈ 20` the same failure costs one part
in 10⁶ or less, and by `k ≈ 25` it is below what the instrument can measure. **So "a limit on
maintenance itself" is fair at small `k` and increasingly empty as `k` grows, and any sentence
using that phrase must say which regime it means.**

---

## 10. W2 — the warrant audit of this document

Applying the PROPOSED **warrant reach** gate's sharpest procedure (W2: sweep the class, not the
instance) to my own text before committing. Every Lean citation checked against its actual
signature; every borrowed number tagged.

| citation | actual hypotheses | our use | verdict |
|---|---|---|---|
| `Core/HammingCap.shareK_le_of_four_pair_uniform` | `emb : Fin 4 → Fin k`; `hp : IsProb p`; `hu :` the four embedded slots have **exactly uniform** pair marginals. Concludes `shareK p ≤ (k−3)·log 2` | quoted as the cap for `share_max` | **SOUND for `share_max`.** These substrates are OA of strength 2, so *every* pair of columns is exactly uniform (`pair_dev` measured exactly 0) and `IsProb` holds for uniform-on-`S`. For a pair-uniform state the pair envelope's sup is `k·ln2`, so `shareK = k·ln2 − ln\|S\| = share_max` exactly, and the cap applies to precisely the quantity we denominate with |
| the same, applied to **stationary** states | same — exact pair-uniformity | `frac_of_lean_cap` is also stored per row for stationary shares | **NOTED, and this is the reach.** The stationary state under partial upkeep is pair-uniform only to `pair_leak ≤ 4.68e−09`, not exactly. The theorem's hypothesis is exact. **No conclusion in this document rests on applying the cap to a stationary state**; the denominators used in §9.1 are all `share_max`, whose hypothesis is exact. The per-row `frac_of_lean_cap` column is reported as stored and is not load-bearing |
| `Core/ThirdCap.share_le_log_two`, `share_le_grouping_gaps` | typed on `Bool × Bool × Bool` — **three binary slots** | **not used** | **CORRECTLY EXCLUDED.** The named-denominator gate names these as *the* two denominators; at `k ≥ 5` they are type-inapplicable. §9.1 substitutes the correct analogues and says so |
| `Core/Maintenance.lean` — `rent_holds`, `underpaid_shrinks`, `unpaid_decays` | `rent_holds (γ S : ℝ) : step γ (γ*S) S = S` — payment `α = γ·S`, proportional to the **amount**, and with **no** positivity hypotheses (it is `ring`). `unpaid_decays` needs `0 < γ ≤ 1` | cited only in the scope paragraph, as a theorem about a model | **SOUND, and the mismatch is the prereg's own.** Payment on this substrate is proportional to the **deficit**, not the amount, so the substrate instantiates `unpaid`/`unpaid_decays` literally and `rent_holds` only weakly. Nothing here is offered as support or refutation |
| `Gavinsky–Pudlák` / `Babai` / `Lancaster`, the OA↔Hadamard equivalence, the Mathieu groups, Paley/Sylvester | — | no novelty claimed on any (prereg §5.2) | **HELD** |
| Gillespie–Praeger; Delsarte; Solé; Rifà–Pujol; Phelps–Rifà–Villanueva | — | §5, credited in the text | **HELD** — and the Mathieu chain is labelled a reproduction, not a discovery, per the sibling's binding adjudication |

**Numbers I did not re-derive, restated:** the six Q2 gate outcomes (read from committed logs,
not re-run); the blast-radius arithmetic of §0.2 (the predecessor's, checked for consistency
against the 90 rows' measured leaks, not re-derived from the Krawtchouk error term); the
box/memory figures of §0.4; the prior-art searches of §5; the ceiling deficit *table* of §9.3
(the sibling's ceiling pass — I re-derived its restorable/lossy counts and the `resolved` flags,
not the per-`k` medians).

**One correction I made to my own work, kept in the record:** my first check of AMENDMENT 2's
ceiling tooth used `N₀(k)` — ARM A's size function — for an ARM B prediction, returning −0.726 pp
against the amendment's −3.869 pp. The amendment was right; §7.2 records both the error and the
corrected derivation, because a 5× discrepancy silently dropped is exactly how a wrong band
survives.

---

## 11. Limits — what this campaign did NOT establish

1. **Nothing about nature.** Designed substrates; a control. `wild-share` is untouched and no
   result here bears on it. Nothing is mechanized, no Lean file was opened, nothing is offered
   to the audit, nothing reaches `Stance.lean`.
2. **No extrapolation past `k = 31` (`k = 32` on ARM B).** The floor of §6.3 is a curve
   parameter over the measured range. There is no `k → ∞` claim and no asymptotic cost of habit.
3. **The floor verdict is weak in three specific ways** and none may be dropped when quoting it:
   it fires in exactly the four fraction-target conditions and neither absolute-target one; it
   fails its own threshold (3/6) if the fit starts at `k = 16`; and **the other arm returns the
   opposite verdict 6/6** (§8.3).
4. **Four pre-registered stakes fired and are recorded dead:** H-IFF's necessity direction,
   H-ORBIT, P-STEP28's raw-uptick form, and H-DISSOC-2. A fifth, H-CEILING, is UNRESOLVED. Of
   the forward predictions only **P-STEP32** and **P-STEP28's trend-corrected form** survived;
   of the two hypotheses the campaign was named for, one direction of one survived.
5. **The pre-registration has two disclosed defects.** Its three Q2 outcome rules are not
   mutually exclusive and two fired together (§6.3); and its §3.3/§3.4 raw-uptick tests were
   arithmetically unwinnable given its own §1.3 amplitude estimate (§7.1). Neither is used to
   soften a fired stake.
6. **H-CEILING is unresolved and its predictor was 85.4 % tied.** The test had almost no
   variance to work with. Its replacement — that `profile_dev` ranks the deficit at ρ = +0.951 —
   is **post-hoc and is not evidence**.
7. **The census generalises to nothing beyond what it enumerates.** `N = 12` complete
   (`k = 3…11`); `N = 20` only `k = 3…6`; `N = 24` only `k = 21…23`; `N = 28` not at all. Full
   censuses of `N = 20` and `N = 28` need `2¹⁹` and `2²⁷` structures and are out of reach. **In
   particular "the counterexample layer is specific to Paley-12" is supported only at `k ≤ 6` on
   Paley-20** — a Paley-20 layer at higher `k` is untested, not excluded.
8. **"One counterexample up to equivalence" is an inference from matching invariants**, not a
   computed `M₁₁` orbit decomposition.
9. **`H24/k22` and `H24/k23` intransitivity rests on the backtracking search** plus the
   construction-side `|G|/N` check and the full `(σ,c)` enumeration; only the `k = 5`
   counterexample has a from-scratch brute-force certificate over all 3840 isometries.
10. **11 structures are PREDICTED-not-verified** (`H32/k21…k31`) and are excluded from every
    tally. Their restorability follows from (T), which is a theorem, but their `R_i(a)` was
    never computed.
11. **The H-SUBSET arm remains underpowered and its 0/236 is not support** (§4.1); the censuses
    that replace it are **post-hoc**, with motivation disclosed.
12. **The prior-art sweep was one afternoon over four query families**, with the key survey PDF
    failing to extract. "Not found" is weaker than "new", and the Voronoi-cell / uniformly-packed
    literature around Delsarte's outer distribution remains the likeliest place a pre-emption
    hides.
13. **`k = 35`, the next Hadamard-attained size named in the brief, was never attempted** — it
    is a `2³⁵` object and out of reach. `k = 31` was declared the ARM A ceiling in the prereg
    §1.4 for that reason, before any curve was seen.
