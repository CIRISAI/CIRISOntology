# The Hamming form of the classical whole-only maximum: where it holds and where it breaks

**Status: exact where marked exact. Not mechanized in Lean.**
Script: `HAMMING_FORM_SCAN.py` · full log: `hamming_form_scan.log` ·
machine-readable: `hamming_form_scan_results.json` ·
method inherited from `CLASSICAL_MAX_K5.py` / `CLASSICAL_MAX_K5.md` (sibling agent).

---

## Headline

> The conjecture **`maxshare(k) = (k − ⌈log₂(k+1)⌉)·ln 2`** is **true for k = 2…7**
> — proved here, not sampled — and **false for k = 8, 9, 10, 11**, where the true
> maximum is strictly larger. The correct general form is the
> **orthogonal-array** one, not the Hamming one:
>
> ```
> maxshare(k) = k·ln 2 − ln N₀(k),      N₀(k) = 4·⌈(k+1)/4⌉
> ```
>
> `2^⌈log₂(k+1)⌉` and `4·⌈(k+1)/4⌉` agree for k ≤ 7 and again for k = 12…15; they
> **diverge at k = 8…11** (16 vs 12), and that is exactly where the conjecture fails.
> The counterexample is explicit and exactly checked: the **Paley Hadamard matrix of
> order 12** gives a 12-point pair-uniform state on 8…11 slots with `H = ln 12 < ln 16`.

Second headline, and the reason this was worth doing:

> The **auxiliary conjecture (a)** (max atom ≤ 1/8) is **dead** — the exact maximum
> atom at k = 4 is **1/6**. The **auxiliary conjecture (b)** (Fourier mass ≤ 1,
> equivalently collision probability ≤ 1/8) is **exactly true and tight**, and it has
> a **one-line proof** that a Lean agent can follow (§4). That proof also
> **re-proves the sibling's k = 5 result more cheaply** — no Motzkin–Straus, no
> bipartite/clique argument, no max-clique computation — and it extends to
> k = 5, 6, 7 for free by marginalization.

---

## 1. The table

`share(p) = k·ln 2 − H(p)` for pair-uniform `p` (the pair envelope's top is the
uniform state, which is itself pair-uniform), so the whole question is
`min H` over the pair-uniform polytope `P_k`.

| k | Hamming form | true max share | how | attaining supports (k = 8 row: best known, not known to attain) |
|---|---|---|---|---|
| 2 | `0` | **`0`** | exhaustive vertex enum (1 vertex) | 1 (the uniform state) |
| 3 | `1·ln2` = 0.693147 | **`1·ln2`** | **exhaustive** vertex enum (8 bases) | 2 (the two parity classes) |
| 4 | `1·ln2` = 0.693147 | **`1·ln2`** | **exhaustive** vertex enum (4368 bases, 26 vertices) | 10 (support 8) |
| 5 | `2·ln2` = 1.386294 | **`2·ln2`** | proved: §4 ladder + `[5,3]` code | 60 (support 8) |
| 6 | `3·ln2` = 2.079442 | **`3·ln2`** | proved: §4 ladder + punctured simplex code | 240 (support 8, linear ones) |
| 7 | `4·ln2` = 2.772589 | **`4·ln2`** | proved: §4 ladder + `[7,3]` simplex code | 480 (support 8, linear ones) |
| 8 | `4·ln2` = 2.772589 | **∈ [3.060271, 3.242592]** — **> Hamming** | construction (exact) + frame bound | ≥ 1 (support 12) |
| 9 | `5·ln2` = 3.465736 | **`9·ln2 − ln12`** = 3.753418 | frame/parity bound + Hadamard-12 OA | ≥ 1 (support 12) |
| 10 | `6·ln2` = 4.158883 | **`10·ln2 − ln12`** = 4.446565 | frame bound + Hadamard-12 OA | ≥ 1 (support 12) |
| 11 | `7·ln2` = 4.852030 | **`11·ln2 − ln12`** = 5.139712 | frame + Plotkin + Hadamard-12 OA | ≥ 1 (support 12) |
| 12 | `8·ln2` = 5.545177 | ∈ [5.545177, 5.678709] — consistent, **not** exact | 16-run simplex code + frame bound | — |
| 13 | `9·ln2` = 6.238325 | **`9·ln2`** | frame/parity bound + 16-run simplex code | — |
| 14 | `10·ln2` = 6.931472 | **`10·ln2`** | frame bound + 16-run simplex code | — |
| 15 | `11·ln2` = 7.624619 | **`11·ln2`** | frame + Plotkin + 16-run simplex code | — |

**Verdict per row**: CONFIRMED for k = 2…7 and k = 13, 14, 15; **FALSIFIED** for
k = 8, 9, 10, 11; consistent-but-open at k = 12.

Exhaustive vs searched, stated plainly:

- **k = 2, 3, 4 are proved by exhaustion.** `H` is concave, so its minimum over the
  compact polytope `P_k` is attained at a vertex; the vertices of `{A p = b, p ≥ 0}`
  are the basic feasible solutions; we enumerate **every** column basis
  (`C(4,4) = 1`, `C(8,7) = 8`, `C(16,11) = 4368`) with exact rational arithmetic.
  Nothing is sampled.
- **k = 5, 6, 7 are proved**, but by argument (§4) rather than by exhaustion —
  a lower bound `min H ≥ ln 8` plus a construction attaining it. Vertex enumeration
  is out of reach here (`dim P₆ = 42`, `C(64,22) ≈ 5·10¹⁷`).
- **k = 8…15 constructions are exact**; the matching lower bounds on `min H` come
  from the frame/collision argument (§5) and are tight at every k in 2…15 **except
  k = 4, 8, 12** (i.e. k ≡ 0 mod 4). k = 4 is closed by the new lemma; **k = 8 and
  k = 12 remain open**, and that is the only gap in the table.
- The **searches** at k = 6, 7, 8 (stage 5) are labelled SAMPLED and are used only
  as confirmation. They were calibrated first at k = 4 and k = 5, where the answer
  is known exactly, and recovered `3·ln2` there. At k = 6 and 7 they recover
  `3·ln2`; at k = 8 they independently rediscover the 12-point state (`ln 12`) and
  **200 seeded perturbations of it fail to beat it**.

---

## 2. The counterexample at k = 8…11, exactly

Paley type-I construction on `q = 11` gives a Hadamard matrix `H₁₂` (verified:
`H₁₂H₁₂ᵀ = 12·I`). Normalizing the first column to `+1` and deleting it yields
`OA(12, 11, 2, 2)`: 12 runs, 11 binary factors, every pair of columns showing each
of the four combinations exactly 3 times. The uniform distribution on its 12 rows,
restricted to any k of the columns, is pair-uniform — checked **exactly**, with
`Fraction` arithmetic, for k = 8, 9, 10, 11 (all 12 rows stay distinct):

```
H = ln 12 = 2.484906649788   <   ln 16 = 4·ln 2 = 2.772588722240
```

so at k = 8, `share = 8·ln2 − ln12 = 3.060271 > (8−4)·ln2 = 2.772589`. The
conjecture is falsified by an explicit state, not by a bound.

Re-checked by a second, independent route (stage 9): direct combination counting on
the 12 rows — all 28 pairs of the 8 columns show each of the four combinations
exactly 3 times, and all 12 rows stay distinct — no Fourier transform and no
polytope machinery involved.

**Why the linear-code reasoning misses it.** For a state uniform on a *linear* code
`C`, pair-uniformity ⟺ dual distance ≥ 3, and the Hamming bound forces
`|C| = 2^m ≥ k+1`, hence `H = ⌈log₂(k+1)⌉·ln2`. But a pair-uniform state need not be
uniform on a linear code. The correct constraint is the orthogonal-array one: `N`
runs with `4 | N` (strength 2) and `N ≥ k+1` (Rao), i.e. `N₀(k) = 4·⌈(k+1)/4⌉`
whenever the matching Hadamard matrix exists. 12 is a Hadamard order and is not a
power of 2 — that is the whole of the discrepancy.

---

## 3. The two auxiliary conjectures

Both were tested **exactly**, not searched.

### (a) max atom ≤ 1/8 — **FALSE at k = 4. Route dead.**

The maximum atom is computed exactly by symmetry reduction: `P_k` and the objective
`p(0)` are invariant under coordinate permutations `S_k`, so averaging any optimum
over `S_k` gives a weight-symmetric optimum `p(v) = p_{|v|}`; in those `k+1`
unknowns there are just 3 equations (normalization and the two Krawtchouk
conditions), so enumerating all `C(k+1,3)` bases with `Fraction` arithmetic is
**exhaustive**. (Cross-checked against the full vertex enumeration at k = 3, 4.)

| k | exact max atom | threshold `1/N₀(k)` | verdict |
|---|---|---|---|
| 3 | **1/4** | 1/4 | works at k = 3 (tight) |
| 4 | **1/6** | 1/8 | **DEAD** — 1/6 > 1/8 |
| 5 | **1/6** | 1/8 | **DEAD** |
| 6 | **1/8** | 1/8 | works (tight) |
| 7 | **1/8** | 1/8 | works (tight) |
| 8 | **1/10** | 1/12 | DEAD at k = 8 |

The k = 4 maximizer is explicit and pretty: the weight-symmetric state
`p₀ = 1/6`, `p₂ = p₃ = 1/12` (support 11), i.e. one atom of `1/6`, six of `1/12` at
Hamming weight 2 and four of `1/12` at weight 3. It is pair-uniform and has
`H = 2.369382 > 3·ln2`, so it is nowhere near the entropy minimum — the max-atom
functional and the entropy functional simply peak in different corners of `P₄`.

### (b) Fourier mass `Σ_{|S|≥3} p̂(S)² ≤ 1` at k = 4 — **TRUE, exactly, and tight.**

`Q` is convex, so its maximum over `P₄` is attained at a vertex, and stage 1
enumerated every vertex: **`max Q = 1` exactly**. Equivalently, via the Parseval
identity `Σ_v p_v² = (1 + Q)/2^k`:

```
max over P₄ of  Σ_v p_v²  =  1/8   exactly, attained.
```

So Rényi-2 ≥ `ln 8` and hence Shannon ≥ `ln 8`. **This is the route.** It is not a
k = 4 accident: it propagates to every k ≥ 4 by marginalization (§4, Lemma B), and
the searched maxima of `Σ p²` at k = 5, 6, 7 all sit at exactly `0.125000000000`,
against the proved ceiling `1/8`.

---

## 4. The proof sketch (for a Lean agent)

Notation: `p` a probability state on `{0,1}^k`; `χ_S(v) = (−1)^{|S∩v|}`;
`E[f] = Σ_v p_v f(v)`. Pair-uniform means `E[χ_S] = 0` for all `1 ≤ |S| ≤ 2`.

### Lemma A (base case, k = 4). Pair-uniform on 4 bits ⇒ `Σ_v p_v² ≤ 1/8`.

Let `t = χ_{1234}`, and for each `S ⊆ {1,2,3,4}` with `|S| ≤ 1` (five of them: `∅`
and the four singletons) set `c_S := E[t·χ_S]`.

1. **Orthonormality of the low-degree characters under `p`.** For `|S|, |S'| ≤ 1`,
   `χ_S·χ_{S'} = χ_{S Δ S'}` and `|S Δ S'| ≤ 2`, so
   `E[χ_S χ_{S'}] = δ_{S,S'}` — the diagonal because `χ² = 1`, the off-diagonal
   because pair-uniformity kills degrees 1 and 2. *(This is the only place the
   hypothesis is used.)*
2. **One square.** Put `y := t − Σ_{|S|≤1} c_S χ_S`. Expanding with step 1,
   ```
   0 ≤ E[y²] = 1 − 2·Σ c_S² + Σ c_S² = 1 − Σ_{|S|≤1} c_S² ,
   ```
   using `E[t²] = 1` and `E[t χ_S] = c_S`. Hence `Σ_{|S|≤1} c_S² ≤ 1`.
3. **Parseval.** For any state, `Σ_v p_v² = 2^{−k}·Σ_S E[χ_S]²`. At k = 4 with
   pair-uniformity only `S = ∅` (contributing 1) and `|S| ≥ 3` survive. Since
   `t·χ_S = χ_{Sᶜ}`, we have `c_S = E[χ_{Sᶜ}]`, and `S ↦ Sᶜ` is a bijection from
   `{|S| ≤ 1}` onto `{|S| ≥ 3}`. So `Σ_{|T|≥3} E[χ_T]² = Σ_{|S|≤1} c_S² ≤ 1` and
   ```
   Σ_v p_v²  =  (1 + Σ_{|T|≥3} E[χ_T]²)/16  ≤  2/16  =  1/8.   ∎
   ```

*Lean shape.* Everything is a polynomial identity in the 16 reals `p_v`. The whole
lemma is: given the 10 linear constraints (4 singles + 6 pairs), normalization, and
`p_v ≥ 0`, conclude `Σ p_v² ≤ 1/8`. The certificate is exactly

```
1/8 − Σ_v p_v²  =  (1/16)·Σ_v p_v · y(v)²
```

a cubic identity whose right-hand side is a sum of 16 manifestly nonnegative terms
(`p_v ≥ 0` times a square). Supplying those 16 products as hints should let
`nlinarith` close it; `ring_nf` alone proves the identity.

**This certificate was checked exactly** (stage 9): as a rational identity on all
26 vertices of `P₄` and on 300 random rational points of `P₄`, with 0 failures.
That is the object to hand to Lean — not the Fourier prose above it.

### Lemma B (propagation). For every k ≥ 4, pair-uniform ⇒ `Σ_v p_v² ≤ 1/8`.

The marginal of a pair-uniform state on any 4 of the slots is pair-uniform (its pair
marginals are a subset of the original's), and marginalizing merges atoms, which
cannot decrease the collision probability:
`Σ_x (Σ_y p(x,y))² ≥ Σ_{x,y} p(x,y)²` since all terms are nonnegative. Apply
Lemma A to the marginal.

### Lemma C (Shannon ≥ collision). `H(p) ≥ −ln Σ_v p_v²`.

Elementary route, no Jensen machinery needed: with `c = Σ_v p_v² > 0`, use
`ln x ≤ x − 1` (Mathlib: `Real.log_le_sub_one_of_pos`) at `x = p_v/c` for each `v`
in the support, multiply by `p_v ≥ 0` and sum:

```
Σ_v p_v ln p_v − ln c  =  Σ_v p_v ln(p_v/c)  ≤  Σ_v p_v (p_v/c − 1)  =  c/c − 1  =  0,
```

i.e. `−H ≤ ln c`, i.e. `H ≥ −ln c`.

### Conclusion.

`H ≥ −ln(1/8) = 3·ln 2` for every pair-uniform state on k ≥ 4 slots, hence
`shareK p = k·ln2 − H(p) ≤ (k−3)·ln 2`. Attained at k = 4, 5, 6, 7 by the code
states above, so the bound is exactly the maximum there.

**Two remarks the Lean agent should not miss.**

1. **The same three-lemma shape with the trivial base `k = 2` reproves the existing
   Lean cap.** A pair-uniform state on 2 bits *is* the uniform state on 4 points, so
   `c = 1/4`, so `H ≥ 2·ln2` and `share ≤ (k−2)·ln2` for all k ≥ 2 — which is
   `shareK_le_of_pair_uniform`. Lemma A is precisely the next rung of the same
   ladder: base at 4 slots instead of 2, ceiling `1/8` instead of `1/4`.
2. **The hypothesis is stronger than the current cap's.** `shareK_le_of_pair_uniform`
   needs *one* uniform pair marginal. The `(k−3)·ln2` statement needs *four slots all
   of whose six pair marginals are uniform*. That is the honest statement to prove:
   "if there are four slots whose six pair marginals are all uniform, then
   `shareK p ≤ (k−3)·log 2`."

Equality analysis (for a tightness statement): `H = −ln c` forces `p` uniform on its
support, and `c = 1/8` then forces `|supp| = 8`, so the minimizers are exactly the
uniform states on `OA(8,k,2,2)` supports.

---

## 5. The general-k frame bound (what is proved at each k, and the two gaps)

With `u_v = (1, χ₁(v), …, χ_k(v)) ∈ {±1}^{k+1}`, pair-uniformity says
`Σ_v p_v u_v u_vᵀ = I_{k+1}`, and `u_v·u_w = (k+1) − 2d(v,w)`. Taking `‖·‖_F²`:

```
Σ_{v,w} p_v p_w ((k+1) − 2d(v,w))²  =  k+1 .
```

*(Both identities verified to ~10⁻¹⁵ on random interior points of `P_k`, k ≤ 9.)*

- **Even k** (new here; the sibling's file treats odd k only): `k+1` is odd, so
  `(k+1) − 2d` is odd, hence nonzero, hence its square is ≥ 1 for every `d ≥ 1`.
  With `c = Σ_v p_v²` this gives `(k+1) ≥ (k+1)²c + (1−c)`, i.e.
  **`c ≤ 1/(k+2)`**. Tight for `k ≡ 2 mod 4`; loose by one Hadamard step for
  `k ≡ 0 mod 4`.
- **Odd k**: the sibling's argument, `m = (k+1)/2`, `c ≤ (m/2 − 1/ω_m)/(m²−1)` with
  `ω_m` the clique number of the distance-`m` graph. Recomputed here: `ω = 2` by
  parity for odd `m`; exact max-clique `ω = 4` at k = 3 and `ω = 8` at k = 7; the
  Plotkin bound `A(2m−1, m) ≤ 2⌊m/(2m−(2m−1))⌋ = 2m` for even `m` beyond that.

| k | proved `c ≤` | `1/N₀(k)` | tight? |
|---|---|---|---|
| 2, 3 | 1/4 | 1/4 | yes |
| **4** | 1/6 | **1/8** | **no — closed by Lemma A** |
| 5, 6, 7 | 1/8 | 1/8 | yes |
| **8** | 1/10 | **1/12** | **no — OPEN** |
| 9, 10, 11 | 1/12 | 1/12 | yes |
| **12** | 1/14 | **1/16** | **no — OPEN** |
| 13, 14, 15 | 1/16 | 1/16 | yes |

So the frame bound is tight at every k in 2…15 except `k ≡ 0 mod 4`, and Lemma A is
exactly the repair at k = 4. **The k = 8 and k = 12 repairs are open**; Lemma A does
not obviously generalize, because its step 1 relies on the k = 4 coincidence that
every character of degree ≥ 3 equals `χ_{1234}` times a character of degree ≤ 1.

---

## 6. What is safe to say, and what is not

**Safe:**

- "The classical maximum of the whole-only share is `(k−3)·ln2` for k = 4, 5, 6, 7,
  and `ln2` at k = 3" — with the label *exact-computed / proved here, not
  machine-checked*.
- "The conjectured Hamming form is right for k ≤ 7, and wrong from k = 8 on, where
  the truth is governed by orthogonal-array existence (`4·⌈(k+1)/4⌉`), not by the
  Hamming bound on linear codes."
- "The k = 5 value `2·ln2` (sibling's result) now has a second, cheaper proof that
  needs neither Motzkin–Straus nor a clique computation."
- "The max-atom route to a Lean proof is dead; the collision-probability
  (Rényi-2) route works and is three lemmas long."

**Not safe:**

- Nothing here is mechanized. `Core/ShareK.lean` still proves only `(k−2)·ln2`.
- k = 8 and k = 12 are **not** settled: at k = 8 the truth is somewhere in
  `[8·ln2 − ln12, 8·ln2 − ln10] = [3.060271, 3.242592]`. The falsification of the
  Hamming form at k = 8 does not depend on closing that gap (the *construction*
  already beats the conjectured value), but the exact value does.
- The attaining-support counts at k = 6, 7 (240, 480) count cosets of linear codes.
  They are complete counts only if every `OA(8,k,2,2)` is affine — true at k = 4
  (exhaustive here) and k = 5 (exhaustive in the sibling's file), and classical for
  order-8 Hadamard matrices, but **not verified here**.
- The k = 11 and k = 15 rows use the Plotkin bound, which is cited, not proved here.
- Hadamard existence at orders 4, 8, 12, 16 is unconditional (constructed here for
  12), so no row of the table rests on the Hadamard conjecture.

---

## 7. Bearing on the published stance

None of this changes what CI enforces. It changes what the honest margin *is*, in
the same two-tier way the sibling file already set out, and it adds one line to the
"what could be mechanized next" list:

- Lean proves `share ≤ (k−2)·ln2`. That is the `k = 2` rung of a ladder whose
  `k = 4` rung (`share ≤ (k−3)·ln2`, for states with four fully pair-uniform slots)
  now has a three-lemma proof with no external theorems and no analysis beyond
  `Real.log_le_sub_one_of_pos`. It is the cheapest available strengthening of the
  cap, and unlike the sibling's k = 5 route it needs no Motzkin–Straus.
- The claim "`(k−2)·ln2` is tight only at k = 3" stands, and is sharpened: the true
  maximum is `ln2` at both k = 3 and k = 4, and the cap over-states by exactly `ln2`
  at every k in 4…7.
