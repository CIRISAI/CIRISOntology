# RESULTS — the column-order control, and the census that had to replace it

**Scope of this file.** The team lead's arbitration (2026-07-27) split the rent-scaling
campaign between two agents after a collision: the sibling owns the canonical Q1 ladder and
all of Q2; **I own two arms — the prior-art sweep, and H-SUBSET, the column-order control
added by `RENT_SCALING_PREREG.md` AMENDMENT 1 (`3b32006`).** This file reports only those.
The campaign's headline verdict on H-IFF belongs in the sibling's `RENT_SCALING_RESULTS.md`;
what is here either supports it or bounds it.

Everything inherits `RENT_SCALING_PREREG.md` §0: **designed substrates, a price and an
algebra, not a discovery about nature.** `wild-share` is untouched. Nothing is mechanized, no
Lean file was opened, nothing is offered to the audit.

---

## Headline

> **The pre-registered control came back UNDERPOWERED, not confirmed — and saying so is the
> result.** H-SUBSET drew 250 random column subsets and found **0 H-IFF violations**. That
> number is worthless as support, for a reason found only after the arm had run: H-IFF's
> necessity direction can only be violated by a **restorable** structure, and the arm produced
> **6** of those out of sample. Zero violations out of six is not evidence.
>
> **Worse, and this is the part worth remembering: neither known counterexample was inside the
> arm's roster.** The amendment fixed `6 ≤ k ≤ min(N−1, 20)` for cost, before any
> counterexample existed. The canonical violations are at `k = 5` (below the floor) and
> `k = 23` (above the cap). A cost-driven bound, chosen honestly and in advance, sat exactly
> one width above the only layer where the phenomenon occurs.
>
> **So I replaced sampling with exhaustion.** A complete census of Paley-12 — **all 1981
> column subsets**, no seed, no sampling, no selection — finds **396 H-IFF counterexamples,
> 63.1 % of all restorable subsets of that Hadamard order, and every one of them at `k = 5`.**
> At `k = 5` the census is total: **396 of the 462 subsets are restorable, and all 396 of those
> are counterexamples.** The refutation is not a lucky find at one truncation; at that width
> it is the rule.
>
> **But do not overcount it.** The 462 five-subsets split exactly into the **66 blocks of the
> Steiner system S(4,5,11)** — verified here: every one of the 330 four-subsets is covered
> exactly once — which are precisely the **non**-restorable ones, and the 396 non-blocks, which
> all carry identical invariants (`|Aut| = 20`, orbits `[10, 2]`, one `R`-level-set). That is
> **one counterexample up to equivalence, occurring 396 times**, not 396 independent ones.
>
> And the economics of it are **size-dependent, which is the more useful answer**: on a
> restorable substrate the ceiling is exactly `1.000000000000` of `share_max`, as theory
> requires; on a lossy one the deficit runs from **6.3 %** at `k = 6` down to **~2e−7** by
> `k = 18–20`, falling monotonically in `k`. Losing restorability is expensive for small
> habits and almost free for large ones.

---

## 1. H-SUBSET — the pre-registered arm. Verdict: UNDERPOWERED

Roster exactly as AMENDMENT 1 fixed it: `N ∈ {12, 20, 24, 28}`, `6 ≤ k ≤ min(N−1, 20)`, 5
random `k`-column subsets each, `numpy.random.default_rng(20260727)` — 250 structures. Draws
were made by `draw_roster()` running to completion and written to the output JSON **before the
first call to `aut_data`**, so no subset could be selected after seeing a result. Instrument:
the sibling's `rent_scaling_aut.py`, imported read-only and unmodified, gates ALL PASS
(`rent_scaling_aut_gate.log`, run after the sibling's canonical launch but before any Q1
number was interpreted).

| | |
|---|---|
| drawn | 250 |
| decided | **250** — 0 UNDETERMINED, no search exhausted its 2e7 node budget |
| distinct column sets | 239 (11 repeats within their own `(N,k)` cell) |
| distinct **and** non-canonical — the out-of-sample tally | **236** |
| **(T)** `transitive ⇒ restorable` violations | **0** — as it must be; nonzero would be an instrument fault |
| **H-IFF** violations | **0** |
| **H-ORBIT** violations | **18** |

Two cells are forced-degenerate and were disclosed in the roster audit before any verdict was
read: at `k = N−1` there is only one possible subset, so all 5 draws at `N=12/k=11` and
`N=20/k=19` are the canonical structure. 12 of the 250 draws coincide with the canonical
first-`k` truncation and are therefore not out of sample.

### 1.1 Why 0/236 is not support, stated plainly

**H-IFF's necessity direction — restorable ⇒ transitive — can only be falsified by a
restorable structure.** Lossy structures cannot violate it no matter how many are drawn. The
arm's restorable population:

| | |
|---|---|
| restorable rows, all 250 | **15** |
| restorable, out-of-sample (the 236) | **6** |
| and all 15 are the same handful of objects | Paley-12 at `k` = 9, 10, 11 |

**The effective sample size against the hypothesis under test is 6, not 236.** Quoting 236
would be exactly the failure the campaign's own harvest gate names — a floor not matched to
the sample size that actually carries the test.

And the roster could not reach either known counterexample:

| counterexample | `k` | in the H-SUBSET roster? |
|---|---|---|
| `H12/k5` (canonical) | 5 | **No** — below the floor `k ≥ 6` |
| `H24/k23` (canonical) | 23 | **No** — above the cap `k ≤ 20` |

The bounds were chosen for cost, in advance, with no counterexample known; this is not
post-hoc selection. It is worse in one way and better in another: better because the design
was honest, worse because an honest cost bound silently removed all the signal. **The arm
answers a different question than the one it was written for** — it says H-IFF is not
*generically* violated by random column orderings at `6 ≤ k ≤ 20`, which is true and nearly
uninformative.

### 1.2 H-ORBIT: 18 violations, and they are the expected kind

All 18 sit at `k = 6, 7, 8` on `N = 20, 24, 28`, and every one is a case where random column
selection **collapsed the support** (`|S| < N`: duplicate rows appear once few columns
survive). These are supports with a trivial group and near-singleton level sets, where a
level set is a strict union of orbits by accident. `orbits_refine_levels` holds in all 250 —
the theorem (T) direction never fails, which is the check that would have caught a bug.

---

## 2. CENSUS-12 — the repair. Exhaustive, and it changes the strength of the refutation

**This extension is post-hoc and its motivation is disclosed in full**: it exists because
§1.1 showed the pre-registered arm had no power. It replaces sampling with exhaustion, so it
carries no sample-size caveat and no seed — every column subset of Paley-12 with
`3 ≤ k ≤ 11` is measured, all `Σ_k C(11,k) = 1981` of them.

| `k` | subsets | `\|S\|` reached | restorable | transitive | counterexamples |
|---|---|---|---|---|---|
| 3 | 165 | 8 (all collapse) | 165 | 165 | 0 |
| 4 | 330 | 11 (all collapse) | 0 | 0 | 0 |
| **5** | **462** | **11 on 66, 12 on 396** | **396** | **0** | **396** |
| 6 | 462 | 12 | 0 | 0 | 0 |
| 7 | 330 | 12 | 0 | 0 | 0 |
| 8 | 165 | 12 | 0 | 0 | 0 |
| 9 | 55 | 12 | 55 | 55 | 0 |
| 10 | 11 | 12 | 11 | 11 | 0 |
| 11 | 1 | 12 | 1 | 1 | 0 |
| **total** | **1981** | | **628** | **232** | **396 (63.1 % of restorable)** |

0 undetermined, 0 **(T)** violations.

At `k = 3` the 12 rows collapse onto the full 3-bit cube, which is transitive for trivial
reasons; at `k = 5` the split in `|S|` is the whole story, and §2.1 says what it is.

Two things follow that the canonical single-truncation result could not have shown:

1. **At `k = 5` every restorable subset is a counterexample — 396 of 396.** The canonical
   `H12/k5` is not a curiosity; it is the generic member of its layer.
2. **Restorability is strongly non-monotone in `k`**: universal at `k = 3`, absent at
   `k = 4`, near-universal at `k = 5`, absent at `k = 6, 7, 8`, universal again at
   `k = 9, 10, 11`. Whatever governs restorability here is arithmetic of the truncation, not a
   trend in width.

### 2.1 The structure behind it — and the reason not to overcount

The 462 five-subsets split into exactly two classes, and the split is a named object:

> **The 66 NON-restorable 5-subsets are precisely the blocks of the Steiner system
> S(4,5,11).** Verified directly here: 66 blocks, and each of the 330 four-subsets of the 11
> columns lies in exactly one of them (coverage multiset `{1: 330}`).

And the census says *why* those 66 are the exceptions, which is sharper than the count:

> **A 5-subset of columns separates all 12 rows of Paley-12 iff it is NOT a block of
> S(4,5,11).** The 66 blocks leave `|S| = 11` — two rows collide — and a collapsed support is
> not restorable. The 396 non-blocks leave `|S| = 12`, and **every single one of them is
> restorable and intransitive.**

So the honest statement of the finding is not a tally at all:

> at `k = 5` on Paley-12, *separating the support* and *being a counterexample* are the **same
> condition**, and the Steiner system is exactly the obstruction.

The 396 all carry **identical invariants** — `|Aut| = 20 = |P|·|C| = 2 · 10`, orbit sizes
`[10, 2]`, exactly one `R`-level-set, `profile_dev` exactly `0.0`. The natural reading is a
single orbit under the `M11` action, making this **one counterexample up to equivalence,
occurring 396 times.** Stated as a reading: I verified the invariants agree and that the 66
form the Steiner system exactly; I did **not** compute the orbit decomposition of `M11` on
5-subsets, so "one equivalence class" is an inference from matching invariants, not a proof.

The `k = 4` layer corroborates the mechanism: all 330 four-subsets collapse to `|S| = 11`, and
330 = 66 × 5 is exactly the count of (block, four-subset-of-that-block) incidences — each
four-subset lying in its unique block.

**So the correct claim is not "396 counterexamples".** It is: *the counterexample class is
generic at its width — it is every restorable 5-subset — and its complement is exactly a
Steiner system.* Anyone quoting 396 as a count of independent findings is overcounting by up
to 396×, and this paragraph exists to stop that.

---

## 3. CENSUS-24 — the other counterexample's cells

Exhaustive over `k = 21, 22, 23` of Paley-24 — `C(23,21) + C(23,22) + C(23,23) = 253 + 23 + 1
= 277` subsets — the high-`k` cells the amendment's cap of 20 excluded, and where the second
canonical counterexample `H24/k23` lives.

| `k` | subsets | restorable | counterexamples | undetermined |
|---|---|---|---|---|
| 21 | 253 | **0** | 0 | 0 |
| 22 | 23 | *running* | | |
| 23 | 1 | 1 (known) | 1 (known) | 0 |

**`k = 21` contributes nothing to either side: not one of its 253 subsets is restorable.** The
`k = 23` cell is a single subset — the canonical structure itself — already measured:
`|Aut| = 253`, orbits `[23, 1]`, `profile_dev = 2.7e−15`, restorable, and therefore a
counterexample.

The same layer effect as Paley-12 is visible: restorability is confined to particular widths
(`k = 23` yes, `k = 21` no) rather than varying smoothly. `k = 22` is still running and is
appended when it lands.

### 3.1 CENSUS-20 — does the layer effect recur on a third order?

Exhaustive over `k = 3, 4, 5, 6` of Paley-20 — 43 605 subsets — chosen to cover the low-`k`
band where Paley-12's counterexample layer sits. Partial at the time of writing:

| `k` | subsets | restorable | counterexamples |
|---|---|---|---|
| 3 | 969 | 969 (support collapses to the 3-bit cube) | 0 |
| 4 | 3876 | **0** | 0 |
| 5 | 11 628 | *running* | |
| 6 | 27 132 | *running* | |

The `k = 3` and `k = 4` layers reproduce Paley-12's pattern exactly — total collapse then a
dead layer. Whether Paley-20 has a `k = 5`-style counterexample layer is the open part.

---

## 4. Ceilings — the standing requirement, and they deflate the stakes

Prereg §2.4: the attainable ceiling under full upkeep, `share_∞(q=1) / share_max`, for every
structure, at `ε ∈ {0.01, 0.05}`, from the gated `rent_islands.py` solver with its
pairwise-maxent correction (not `k·ln2 − H(p)`, which over-reads on a lossy substrate). Cost
was measured before the run — under ~1 s per structure at `k ≤ 20` — so **no cost cut was
applied and the whole roster is covered**, which matters because a cut chosen after seeing
which structures came back lossy would have been a selection.

**On the 15 restorable structures the ceiling is exactly `1.000000000000`** at both `ε` — full
upkeep restores the design state to the last digit, which is what restorable means and is a
free check that the ceiling instrument agrees with the `profile_dev` criterion.

**On the 235 lossy structures the deficit is real, and it is a strong function of `k`**
(`ε = 0.01`; the `ε = 0.05` picture is the same shape):

| `k` (full support, `\|S\| = N`) | 6 | 7 | 8 | 10 | 12 | 14 | 16 | 18 | 20 |
|---|---|---|---|---|---|---|---|---|---|
| median deficit `1 − ceiling_frac` | 1.8e−2 | 3.0e−4 | 1.9e−4 | 2.9e−5 | 6.7e−6 | 8.9e−7 | 1.3e−6 | 1.1e−7 | 2.1e−7 |
| worst in cell | 6.3e−2 | 7.8e−4 | 7.6e−4 | 1.7e−4 | 3.2e−5 | 7.6e−6 | 7.9e−6 | 3.4e−7 | 1.7e−6 |

Overall: median `5.4e−6`, 90th percentile `9.7e−3`, **maximum `6.3e−2`** (`H12/k6/s4`, which
has full support `|S| = 12`, so this is not an artefact of columns collapsing rows — though the
21 collapsed-support rows do sit high, median `2.2e−2`).

**Correcting a claim I made from a partial read:** an earlier draft of this file said the
ceiling "never falls below ≈ 0.99999", generalising from the `k = 18, 19` rows visible at the
tail of the running log. That is wrong by four orders of magnitude at small `k`. The measured
statement is the table above.

**What it means for the campaign's framing.** The transitive/intransitive boundary is exact and
sharp — twelve orders of magnitude separate the two populations in `profile_dev`. Its *price*,
measured in the currency the campaign cares about, is **size-dependent and falls fast**: a
small habit that is not restorable forfeits several percent of its whole-only share under full
upkeep; by `k ≈ 20` the same failure costs one part in 10⁶ or less. So "a limit on maintenance
itself" is fair at small `k` and increasingly empty as `k` grows, and any write-up using that
phrase should say which regime it means.

---

## 5. Prior art — and it predicted this outcome

`RENT_SCALING_PRIOR_ART.md` (`648ee07`), required by prereg §5.2 before results are written.
The load-bearing findings:

- **Gillespie & Praeger (arXiv:1112.1247, JCTA 2013) classify the `k = 11` object.** Binary
  completely regular codes at `(m,δ) = (12,6)` and `(11,5)` are unique up to equivalence, their
  automorphism groups mod a kernel are **Mathieu**, and they are necessarily completely
  transitive. The Mathieu chain 7920/720/144/48 in `aut_counts_exact.json` is a **reproduction
  of a published classification** and must be credited in the text, not a footnote.
- **Completely regular (Delsarte 1973) ⊋ completely transitive (Solé 1990).** "Regularity
  implies symmetry" is *known false* in the neighbouring setting. H-IFF's necessity direction
  dying is the **expected** outcome under the literature — exactly the prior the prereg §2.2
  staked in advance, before any group was computed.
- **"Transitive code"** is a standard named property (Rifà–Pujol); the Best code (length 10,
  size 40, `d=4`) is the named witness that transitive ⊅ propelinear.
- **Trap flagged:** our `|C|` is the orbit of the zero word under the *full* isometry group, so
  `|C| ≥ |K(S)|`, the published **kernel** (Phelps–Rifà–Villanueva 2005). Never compare the two
  without that correction.

That the Steiner system S(4,5,11) turns up as the exact complement of the counterexample class
is consistent with this: `S(4,5,11)` is the `M11` Steiner system, and `M11` is the group the
classification names.

---

## 6. Independent verification of the refutation

`rent_scaling_q1_independent.py` / `.log` (`7bb1821`). The refutation is a **negative from a
backtracking search**, so it was checked against three things that are not that search:

1. **The cheap invariants fail to certify it** — 0 of 108 translates separated by row-weight
   multiset or by any column-Gram invariant (entries, sorted rows, spectrum) across H12/k11,
   H20/k19, H24/k22, H24/k23, H28/k27. These supports are equidistant (H24/k23: every pairwise
   distance exactly 12) and far too regular for a cheap certificate. Recorded because it is why
   2 and 3 are needed — and because "distance-invariant but not transitive" is the classical
   distinction the prior art names.
2. **The point-stabiliser prediction**, which the engine reproduces: deleting one column deletes
   one point of the construction's natural action, so `|Aut(S)|` must be `|G|/N` —
   `|M12|/12 = 7920` ✓ and `|PSL(2,23)|/24 = 6072/24 = 253` ✓.
3. **Exhaustive enumeration** of the small counterexample: `H12/k5` has `k = 5`, so all
   `5!·2⁵ = 3840` cube isometries are tested individually — `|Aut| = 20`, orbits `[10,2]`,
   `profile_dev` **exactly 0.0**. No stabiliser chain, no node budget, no pruning.

---

## 7. Limitations

1. **The pre-registered arm is underpowered and its null is reported as such**, not as support.
   That is the arm's verdict of record.
2. **CENSUS-12 and CENSUS-24 are post-hoc extensions.** Their motivation is disclosed (§2). They
   are exhaustive rather than sampled, which removes the sample-size caveat but not the fact
   that they were run after the pre-registered arm returned nothing.
3. **"One counterexample up to equivalence" is an inference from matching invariants**, not a
   computed orbit decomposition (§2.1).
4. **Two Hadamard orders only.** CENSUS covers `N = 12` completely and `N = 24` at three widths.
   `N = 20` and `N = 28` are exhaustively uncovered — `Σ_k C(19,k)` and `Σ_k C(27,k)` are out of
   reach — so the census generalises to nothing beyond the orders it enumerates.
5. **No claim about nature, no extrapolation, nothing mechanized**, and nothing here reaches
   `Stance.lean`.
6. `H24/k22` and `H24/k23` intransitivity rests on the backtracking search plus §6's checks;
   only the `k = 5` counterexample has a brute-force certificate.
