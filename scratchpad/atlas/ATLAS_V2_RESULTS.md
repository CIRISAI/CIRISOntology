# Finite-model atlas v2 — results: the transport layer

**Both staked bridges are DEAD, each with a minimal counterexample small enough to
`decide`. What survives is better than what was hunted: curvature is not a rival of
closure, it is `Held` on the context axis — the SAME relation the rent clause is, applied
to the loop instead of the step. And in the one sector where the presheaf→stack upgrade
actually lives, curvature and closure are linked with the OPPOSITE SIGN to the stake:
nonzero curvature FORCES every context view closed.**

Instruments: `atlas_v2.py` (+ `atlas_v2_core.py`), `atlas_v2_addendum.py`. Stakes in
`ATLAS_V2_STAKES.md`, written to disk before either existed. Logs: `main_run.log`,
`addendum_run.log`.

---

## 0. The gates — the atlas passes its own kill

| gate | reading |
|---|---|
| **D1** `r_loop = id ⇒ γ_loop = id` on `range(q_1)` | **36 864 / 36 864** transportable models out of 2 359 296 enumerated (|X|=4, k=2, all `r12,r23` bijections with `r31` forced). `mediator_fixes_range` reproduced EXACTLY |
| **D2** mode-blind views + mode-only re-roots ⇒ flat | **256 / 256** |
| **D2′** fixed fibration does NOT imply flat once the re-root moves the base | witness at \|S\|=2, k=2 |
| **gauge** relabelling each context's readings preserves flat/non-flat and support | clean on 4 000 random models |

**The D2′ probe's first version returned NOTHING, and the diagnosis is a lesson, not a
footnote.** It was pinned at |S|=3, k=2. A nontrivial holonomy on a mode-blind view needs
the re-root to *permute `q_1`'s fibers*, which needs two fibers of EQUAL size — and a
2-colouring of 3 microstates cannot supply one. The claim was right; the search space
was one state too small to host the witness. The same artifact silently emptied the
first reversible-envelope sweep (§3). **A finite search that comes back empty has two
readings — the claim is false, or the box is too small — and only measuring the box
distinguishes them.**

## 1. Derived in the prereg, verified exactly by the instrument

These were hand-derived in `ATLAS_V2_STAKES.md` before the code existed, so confirming
them is verification of the instrument, not a finding. All exact:

- **D4** (mode-sector holonomy formula) `γ_loop = a_1·(α_1^{-ε31} α_3^{-ε23} α_2^{-ε12})·a_1^{-1}` — 16/16, 40/40, 136/136 at k = 2,3,4.
- **D5** (**transportability is a conjugacy condition**) the carry on edge `i→j` exists ⇔ `ρ_ij α_i ρ_ij^{-1} = α_j^{±1}` — 64/64, 1728/1728, 110 592/110 592 in the mode-only sector, and **373 248/373 248 with `ρ` free**.
- **D6** bijective re-roots ⇒ `γ_loop` is a permutation of `range(q_1)` — all models.
- **D7** `Closed q_i` under the mode advance ⇔ `β_i² = id` — 6/6, 24/24.

**Free reading, not staked: transportability is RARE and highly structured.** In the
mode-only sector only 40 of 1728 (k=3) and 136 of 110 592 (k=4) atlases admit all three
carries, and the surviving `(β_1,β_2,β_3)` always share ONE cycle type. D5 is why.

## 2. The structural collapse that makes bridge (ii) unstatable

**In a transportable atlas the glued view carries EXACTLY the base view.** Enumerated:
1008/1008 transportable atlases have `G = (q_1, q̃_2, q̃_3)` with precisely `q_1`'s
fibers, **0** strictly finer; among obstructed atlases 11 016 of 12 816 are strictly
finer. The reason is one line: each carry is a *function* of the previous reading, so
`G` is a function of `q_1`.

Consequence, confirmed as an exact equivalence on 7 558 272 models: **`Closed G T` ⇔
`Closed q_1 T`**. Gluing adds no information in degree 0. *All* the atlas's content is
in degree 1 — the holonomy. Bridge (ii) asked whether curvature forces the glued view to
fail; the glued view has nothing of its own to fail with.

## 3. THE TWO STAKED BRIDGES — both KILLED, with minimal witnesses

Both die twice: once with degenerate maps, once under full reversibility (`r_loop` and
`T` bijections, `γ_loop` a nontrivial permutation), which is the version that matters.

### B(ii) `nonzero curvature ⇒ closure failure` — **DEAD**. Minimal witness |X| = 2, k = 2

```
X = {0,1}     q1 = qt2 = qt3 = (0,1)      r_loop = (1,0)      T = (0,1) = id
γ_loop = {0↦1, 1↦0}   support 2   Closed(G,T) = Closed(q1,T) = TRUE   Δ_G = 0
```

Maximal curvature — the holonomy moves *every* reading — and the view is perfectly
closed. The quantified form dies with it: the minimum `Δ_G` is **0.0 at every curvature
support**, both in the general class and in the reversible class (|X|=4, k=2), so **no
nondecreasing `f` with `f(support ≥ 1) > 0` can exist.**

### B(i) `zero curvature ⇒ closure` — **DEAD**. Minimal witness |X| = 3, k = 2

```
X = {0,1,2}   q1 = qt2 = qt3 = (0,0,1)    r_loop = (1,0,2) ≠ id    T = (0,2,1)
γ_loop = identity   support 0   Closed(q1,T) = FALSE   Δ_G = 0.4621 nats
```

A genuinely nontrivial loop (`r_loop` swaps two states) that is exactly flat because it
preserves `q_1`'s fibers, over a view the dynamics does not close.

**The prereg's predicted mechanism for B(i) was wrong and the run corrected it.** The
stake predicted the minimal counterexample needed k = 3 (a 3-cycle mismatch with
`β³ = id`). Two microstates fewer suffice, because flatness is far more cheaply obtained
by `r_loop` preserving fibers than by a mismatch cubing to the identity. The staked
mechanism *does* exist — it is the 8 models in the k=3 mode-only sector with an even
number of flipping edges and `β` a 3-cycle (§5) — but it is not minimal.

## 4. THE SURVIVING BRIDGE — curvature is an automorphism of the habit

> **If the loop is a symmetry of the step (`T ∘ r_loop = r_loop ∘ T`) and the view is
> `Closed` under `T` with rate `h`, then `γ_loop ∘ h = h ∘ γ_loop` on `range(q_1)`.**

| check | reading |
|---|---|
| permutation family, all maps `S→S` as dynamics | **100 224 / 100 224** |
| general finite class, \|X\|=3, EXHAUSTIVE (no mode structure, arbitrary views/loops/dynamics) | **183 303 / 183 303** |
| general class, \|X\|=4, random sample of 400 000 | 193 / 193 (only 193 models satisfy both hypotheses — a weak check, reported as such) |
| **both hypotheses load-bearing** | `EQV & C1 ⇒ COMM` survives while NEITHER `EQV` nor `C1` alone does. In the permutation family, explicit commutator violations once equivariance is dropped (first at `K = 2`). Re-checked in the GENERAL class, \|X\|=3 exhaustive: of 559 548 models with closure but **not** equivariance, the commutator **fails in 452 304** — closure alone buys nothing. Closure is load-bearing trivially: without it there is no rate `h` to commute with |

**And curvature is logically independent of closure at the single-antecedent level.** In
the exhaustive implication scan over 7 558 272 models, `HOL` neither implies nor is
implied by any closure feature on its own. It appears only in *pair* antecedents, and
always alongside equivariance. That is the whole shape of the answer to H2: **`D_v` and
`F_γ` do not bound each other; they interact through one hypothesis, and that hypothesis
is a symmetry, not a magnitude.**

**One survivor was convicted as an artifact and is reported as one.** `¬HOL & C1 ⇒ EQV`
held on all 77 760 supporting models of the permutation family and **FAILS** in the
general class (29 079/64 395 at |X|=3). It is an artifact of bijective views, and it is
recorded here because it is exactly the kind of relation this atlas exists to catch
before it becomes a claim.

## 5. THE STRONGEST RESULT — the mode sector, characterized completely

In the mode-only sector (`ρ_ij = id`: the re-root moves only the slow mode — the sector
the presheaf→stack upgrade actually opens), **D5 forces the structure, and the whole
sector is a closed form.** With `k` readings and `#flips` mode-flipping edges:

- transportability forces `α_1 = α_2 = α_3 = α`;
- if `#flips` is **odd** it additionally forces **`α² = id`**;
- `γ_loop = α^{#flips}`, hence **flat for even `#flips`, `= α` for odd**.

So **nonzero curvature ⇔ (`#flips` odd ∧ `α` a nontrivial involution)** — and `α² = id`
is exactly D7's closure condition. Therefore, in this sector:

> ### nonzero curvature ⇒ EVERY context view is Closed under the mode advance.

The staked bridge had the sign backwards. Confirmed exhaustively, with the counts
derived and matched to the unit:

| k | transportable = `4(k! + I(k))` | measured | curvature-carrying = `4(I(k) − 1)` | measured | curvature with `¬closed` |
|---|---|---|---|---|---|
| 3 | 40 | **40** | 12 | **12** | **0** |
| 4 | 136 | **136** | 36 | **36** | **0** |

(`I(k)` = number of involutions in `S_k`, including the identity.) The full 2×2 tables
match term by term: at k=3, (flat, not-all-closed) = 8 = 4 arrangements × 2 three-cycles;
at k=4, 56 = 4 × 14. Curvature appears at **1 or 3** flipping edges and never at 0 or 2.

**Scope, stated plainly:** this is a theorem about the bijective-view family on a
three-context cycle in the mode-only sector. It is not a claim about nature, and it does
not survive `ρ ≠ id` (where the base sector supplies curvature with no state-dependence
at all — D2′).

## 6. Three more readings the run produced

- **B(v) — LOSSY HOLONOMY EXISTS, and the programme has never named it.** Minimal
  witness |X|=2, k=2: `q1=(0,1)`, `qt2=qt3=(0,0)`, `r_loop=(0,0)` gives
  `γ_loop = {0↦0, 1↦0}` — **not injective on `range(q_1)`**. An irreversible re-root
  returns fewer distinctions than it took. D6 says reversibility forbids this, so
  "holonomy is a permutation" is a THEOREM WITH A HYPOTHESIS, and the hypothesis is
  reversible transport. Every holonomy the programme has measured (`RerootTransport`'s
  three-root instrument, the Wilson-loop campaign) sits on the reversible side; nothing
  has yet tested the collapsing side.
- **B(vi) — the loop transports where a leg does not, 64.0% of the time.** Of 12 816
  obstructed atlases, 8 208 still admit a loop-level carry, including non-flat ones
  (witness: legs `(ok, ok, FAIL)` with `γ_loop = {0↦1, 1↦0}`). **A successful round trip
  is not evidence that its legs were licensed** — `comp_failure_convicts_second_leg` read
  backwards, and a fence on any inference from atlas-level coherence to per-edge validity.
- **A5 — closure does not descend the `Factors` order.** With `q_1` closed and `q̃_2` a
  strict coarsening, `q̃_2` is closed in only 77.8% of cases (|X|=3, exhaustive; minimal
  witness `q1=(0,1,2)`, `g=(0,0,1)`, `T=(0,2,0)`, `Δ = 0 → 0.4621` nats). A tier's
  autonomy is not inherited by its own coarsenings; **each context of a transportable
  atlas owes its own closure reading** (this is lumpability's classical non-hereditariness,
  in the object's vocabulary).

## 7. The adiabatic reading — a slow mode does NOT suppress the defect linearly

Closed form identified POST HOC from the p-sweep, then confirmed to machine precision on
**every** `β` for k = 3 and k = 4 at five values of `p`:

```
Δ_v(p) = (1/k) · Σ_f  [ 0                 if β f = f
                      | H₂(p)             if β²f = f ≠ β f
                      | H₂(p) + p·ln 2    otherwise ]
```

Since `H₂(p) ~ p·ln(1/p)`, **the leak is above linear order in the mode rate**: slowness
buys less than a linear-response intuition expects. And an *involutive* mismatch — one
exactly closed under the DETERMINISTIC mode flip by D7 — still carries a nonzero defect
under the STOCHASTIC one. Only `β`'s **fixed points** cost nothing. This is v1's S2
lesson again in a new place: deterministic closure is not stochastic closure.

## 8. The Lean target

The identification first, because it is the finding and it needs no new theorem:

> **Zero curvature is `Held` on the context axis.** Given the carry,
> `γ_loop = id on range(q_1)` ⇔ `q_1 ∘ r_loop = q_1` ⇔ **`Held q_1 r_loop`**; and
> "the loop transports at all" is **`Closed q_1 r_loop`**. So `held_imp_closed` —
> already machine-checked in `Core/Habit.lean` — gives *zero curvature ⇒ the loop
> transports* for free. **Curvature and rent are the same relation on two different
> maps**: `Held v T` is rent paid in full in time, `Held v r_loop` is flatness in
> context. That is why the naive bridge died: it compared one relation's readings on
> two unrelated maps.

The new theorem, `Core/Curvature.lean` or an addition to `Core/RerootTransport.lean`.
**Written out and TYPECHECKED against this repo's toolchain** — `scratchpad/atlas/atlas_v2_target.lean`,
`lake env lean` clean, axiom readings from `#print axioms` below the fold:

```lean
/-- **CURVATURE IS AN AUTOMORPHISM OF THE HABIT.** If the re-root loop is a symmetry
    of the step and the view is Closed with rate `h`, the holonomy commutes with the
    rate on the view's range. Both hypotheses are load-bearing: dropping either
    admits counterexamples (atlas v2, exhaustive at |X| = 3). -/
theorem holonomy_commutes_with_rate
    {X C : Type _} {v : X → C} {T rloop : X → X} {γ h : C → C}
    (hcarry  : v ∘ rloop = γ ∘ v)      -- Closed v rloop, γ the transport witness
    (hclosed : v ∘ T = h ∘ v)          -- Closed v T,     h the rate
    (heqv    : T ∘ rloop = rloop ∘ T)  -- the loop is a symmetry of the step
    (x : X) : γ (h (v x)) = h (γ (v x)) := by
  have hc : ∀ y, γ (v y) = v (rloop y) := fun y => (congrFun hcarry y).symm
  have hr : ∀ y, h (v y) = v (T y)     := fun y => (congrFun hclosed y).symm
  have he : ∀ y, T (rloop y) = rloop (T y) := fun y => congrFun heqv y
  rw [hr, hc, ← he x, hc, hr]
```

`holonomy_commutes_with_rate` **does not depend on any axioms**; `curvature_iff_held`
(brick 1, also written and checked) depends on `Quot.sound` only; `glued_view_collapses`
(brick 2) is `rfl` and axiom-free.

Supporting bricks, all `decide`-able or two-line — 1 and 2 are already written and
typechecked in `atlas_v2_target.lean`; 3–5 are not:

1. `curvature_iff_not_held : (∀ c ∈ Set.range v, γ c = c) ↔ v ∘ rloop = v` — the
   identification above (D3).
2. `glued_view_collapses` : if `q̃₂ = g ∘ q₁` and `q̃₃ = g' ∘ q̃₂` then
   `fun x => (q₁ x, q̃₂ x, q̃₃ x)` factors through `q₁` — why bridge (ii) has no subject.
3. `holonomy_perm_of_bijective` : `r_loop` bijective ⇒ `γ_loop` is a bijection of
   `range v` (D6) — **with `lossy_holonomy_witness` as its non-vacuity fence**, the
   |X|=2 witness of §6 proving the hypothesis is doing work.
4. **The two counterexamples, verbatim as finite data** (`Fin 2` and `Fin 3` views over
   `Fin 2`/`Fin 3`), so `curvature_does_not_force_nonclosure` and
   `flatness_does_not_force_closure` are `by decide`. Data is in §3.
5. `mode_sector_curvature_imp_closed` — §5's theorem for the mode-only sector; the
   hardest of the five and the only one needing group structure (`α² = id` from an odd
   flip count).

## Standing after v2

| bridge | status |
|---|---|
| flat limit (`r_loop = id ⇒ flat`) | **proved** + reproduced 36 864/36 864 |
| fixed fibration ⇒ flat | **FALSE as usually stated** — true only in the mode sector (D2/D2′) |
| transportability ⇔ conjugacy of the mismatches | **new, exact**, 373 248/373 248 |
| zero curvature ⇒ closure/gluing | **DEAD**, minimal witness \|X\|=3, k=2 |
| nonzero curvature ⇒ closure failure | **DEAD**, minimal witness \|X\|=2, k=2; quantified envelope refuted at every support |
| curvature ⇔ `Held` on the context axis | **identification, free from `held_imp_closed`** |
| curvature commutes with the rate under loop-symmetry | **SURVIVES**, exhaustive in and out of the family — the Lean target |
| mode sector: curvature ⇒ every view closed | **SURVIVES with the opposite sign to the stake**, closed-form counts matched at k=3,4 |
| holonomy is a permutation | **true only for reversible transport**; lossy witness exhibited |
| loop transports ⇒ its legs were licensed | **DEAD**, fails 64.0% of the time |

v2 did what v1 did: killed the bridges it was built to hunt, and returned them sharper.
The remainder item 5 of `OBJECT_INVARIANT_HUNT.md` is no longer untested — `D_v` and
`F_γ` are **not** two faces of one magnitude. They are one relation (`Held`/`Closed`)
evaluated on two different maps, and they constrain each other exactly when those two
maps commute.
