# The exact classical maximum of the whole-only share at k = 5

**Status: exact, and attained. Not a sampled lower bound.**
Exact-computed and machine-verified here; **not** mechanized in Lean.

Script: `CLASSICAL_MAX_K5.py` · full run log: `classical_max_k5_full.log` ·
machine-readable: `classical_max_k5_results.json`

---

## Headline

> **The true classical maximum of `shareK` at k = 5, over all pair-uniform
> states, is exactly `2·ln 2 ≈ 1.386294361119891`.**
>
> It is *attained*, by the uniform distribution on any of exactly 60 eight-point
> supports, and by nothing else. `2·ln 2` is not merely the best value known —
> it is the maximum, and no classical five-slot state can beat it.

So the answer to "does anything beat `2·ln 2`?" is **no, and provably nothing
can**. The `2·ln 2` the Lean file records as "the best classical value we know"
is the ceiling itself.

| | value | status |
|---|---|---|
| quantum, AME(5,2) | `5·ln 2 ≈ 3.4657` | ideal ceiling, not mechanized |
| **true classical max** | **`2·ln 2 ≈ 1.3863`** | **exact, this file** |
| Lean's proved cap `(k−2)·ln 2` | `3·ln 2 ≈ 2.0794` | machine-checked, **not tight at k = 5** |

The honest margin statement for the published Bell-test claim therefore has two
tiers, and they must not be blurred:

- **Against what is machine-checked**: quantum `5·ln 2` sits `2·ln 2` above the
  proved cap `3·ln 2`. This is what CI currently enforces and what the hardware
  claim is staked against.
- **Against the truth**: quantum `5·ln 2` sits `3·ln 2` above the true classical
  maximum `2·ln 2`. The real classical headroom is 50 % larger than the proved
  cap admits, but that extra headroom is **not yet mechanized** and must not be
  cited as if it were.

---

## Why the problem reduces to minimizing entropy

`Core/ShareK.lean` defines

```
shareK p = sSup { H(q) : q a probability state with the same pair marginals
                         as p, at every pair of slots }  −  H(p)
```

If `p` on `{0,1}^5` is pair-uniform, its envelope is the whole pair-uniform
polytope `P`, which contains the uniform distribution — and the uniform
distribution attains `5·ln 2`, the global entropy maximum over all states on 32
points. (Pair-uniformity forces every single-slot marginal to be uniform too, so
the `i = j` cases of the envelope condition are met as well.) Hence for every
pair-uniform `p`

```
share(p) = 5·ln 2 − H(p),      max classical share = 5·ln 2 − min_{p ∈ P} H(p).
```

`P` = `{p ∈ Δ₃₁ : p̂(S) = 0 for all 1 ≤ |S| ≤ 2}`, a 16-dimensional polytope
(32 variables, 16 independent equality constraints; null-space dimension
verified = 16).

---

## The exact argument

Four steps. Every one is verified in stage 1 of the script — exhaustively where
the statement is finite, to 15–16 digits where it is analytic.

**(1) Frame identity.** For `v ∈ {0,1}^5` set `u_v = (1, χ₁(v), …, χ₅(v)) ∈ {±1}^6`.
Pair-uniformity says exactly that every entry of `Σ_v p_v u_v u_vᵀ` off the
diagonal vanishes and every diagonal entry is 1:

```
Σ_v p_v u_v u_vᵀ = I₆      for every p ∈ P.
```

*Verified: 300 random interior points of `P`, max deviation `4.4e−16`.*

**(2) Frobenius identity.** Since `u_v · u_w = 6 − 2·d(v,w)`, taking
`‖·‖_F²` of both sides of (1) gives `Σ_{v,w} p_v p_w (6−2d)² = 6`, i.e.

```
Σ_{v,w} p_v p_w (3 − d(v,w))² = 3/2.
```

*Verified: 300 random interior points, max deviation `4.4e−16`.*

**(3) The distance-3 graph on the 5-cube is triangle-free.** `d(v,w) ≡ |v|+|w|
(mod 2)`, so three mutually odd distances would need three pairwise-different
parities in a two-class system. Its clique number is therefore `ω = 2`.

*Verified exhaustively: all `C(32,3) = 4960` triples; 0 triangles; the graph is
10-regular with 160 edges.*

**(4) Motzkin–Straus (1965).** For a graph with clique number `ω`, the maximum
over the simplex of `Σ_{(v,w) ∈ E} p_v p_w` (ordered pairs) is `1 − 1/ω`. With
(3), the weight `S` that any `p` can place on distance-3 pairs satisfies
`S ≤ 1/2`.

*Verified numerically: 4000 replicator-dynamics runs, max `0.500000000000`.*

**(4′) Motzkin–Straus is avoidable here** — which matters for mechanization.
Because `d = 3` is odd, the distance-3 graph is *bipartite* between even- and
odd-weight words, so its edges sit inside the complete bipartite graph and, with
`E = Σ_{|v| even} p_v`, `S ≤ 2·E·(1−E) ≤ 1/2` elementarily.

*Verified: exhaustively, every distance-3 edge is a cross edge; and
`S ≤ 2E(1−E)` asserted on 2000 points of `P` with no violation.*

**The chain.** Write `c = Σ_v p_v²` (collision probability). The diagonal of (2)
contributes `9c`; every off-diagonal term has `(3−d)² ≥ 1` **unless** `d = 3`,
where it is 0. So

```
3/2  =  9c + Σ_{v≠w} p_v p_w (3−d)²  ≥  9c + (1 − c − S)
⇒ 8c ≤ 1/2 + S ≤ 1/2 + 1/2 = 1
⇒ c ≤ 1/8
⇒ H(p) ≥ H₂(p) = −ln c ≥ ln 8 = 3·ln 2.
```

**Equality analysis.** `H = H₂` forces `p` uniform on its support; `c = 1/8`
with `p` uniform forces `|supp| = 8`. So the minimizers are exactly the uniform
distributions on 8-point supports that lie in `P` — the strength-2 orthogonal
arrays `OA(8,5,2,2)`. These exist, so the bound is attained and

```
min H = 3·ln 2,      max classical share = 5·ln 2 − 3·ln 2 = 2·ln 2.
```

---

## The exhibited optimizer, exact

The canonical witness is the `[5,3]` code `C = {x : x·11100 = 0, x·00111 = 0}`
— the dual-distance-3 code the Lean file already names — with the uniform
distribution on it:

| word | p |
|---|---|
| `00000` | `1/8` |
| `00011` | `1/8` |
| `01101` | `1/8` |
| `01110` | `1/8` |
| `10101` | `1/8` |
| `10110` | `1/8` |
| `11000` | `1/8` |
| `11011` | `1/8` |

Rational coordinates recovered by exact `Fraction` Gaussian elimination on the
integer constraint system; all ten pair marginals uniform to exactly 0 deviation.

```
H     = 8 · (1/8) · ln 8  =  ln 8  =  3·ln 2  =  2.079441541679836
share = 5·ln 2 − 3·ln 2   =  2·ln 2           =  1.386294361119891
```

---

## Independent confirmation

**Exhaustive minimal support** (stage 2). Every point of `P` has support ≥ 8, and
the 8-point ones are completely enumerated:

- all `C(32,6) = 906 192` six-subsets: **0** admit a pair-uniform state;
- all `C(32,7) = 3 365 856` seven-subsets: **0** admit a pair-uniform state;
- all `C(32,8) = 10 518 300` eight-subsets, by Fourier-pruned exhaustive DFS:
  exactly **60** are `OA(8,5,2,2)`. On each, exact rational solve returns
  `p = 1/8` uniformly — 0 violations. All 60 are affine translates of linear
  `[5,3]` codes with dual distance 3 (15 codes × 4 cosets).

This also sharpens Rao's bound: Rao gives support ≥ 6 for a state in `P`; the
truth is **exactly 8** (`c ≤ 1/8` plus Cauchy–Schwarz `c ≥ 1/|supp|`), and the
exhaustive sweep confirms it directly.

**Randomized vertex sampling** (stage 4a) — the originally requested method.
20 000 random-objective LPs over `P`, HiGHS: **1685 distinct vertices**, support
sizes 8 to 16 (median 8), minimum `H` found `2.079441541680` = `3·ln 2` to 12
digits, maximum `2.772588722240` = `4·ln 2`. Histogram of `H` over sampled
vertices:

```
[2.0794, 2.1372)  ########################################  14077
[2.1372, 2.3683)                                                0
[2.3683, 2.4260)  ###                                         1289
[2.4260, 2.4838)                                                0
[2.4838, 2.5415)  ##########                                  3639
[2.5415, 2.5993)                                                0
[2.5993, 2.6571)  #                                           514
[2.6571, 2.7148)  #                                           393
[2.7148, 2.7726)                                               88
```

The spectrum is discrete and its bottom bin is the optimum — nothing sits
between `3·ln 2` and the next vertex class.

**Frank–Wolfe entropy minimization** (stage 4b). 5000 random starts, linearize-
and-LP to a vertex: minimum `2.079441541680`, **0 starts of 5000 found anything
below `3·ln 2`** (the proof says none exist), 67.1 % of starts reach the optimum
exactly. The best vertex is always support-8 with all probabilities `1/8`
(verified by exact rational solve).

**Collision probability** (stage 4c). Maximizing the convex `Σ p²` over `P` from
2000 starts gives `0.125000000000` — the proof's `c ≤ 1/8`, saturated.

---

## Bonus: the same argument at general odd k

The `k = 5` argument is an instance of a general one. For odd `k` put
`m = (k+1)/2`; (1) and (2) become `m²c + Σ_{v≠w} p_v p_w (m−d)² = m/2`, and with
`ω_m` the clique number of the distance-`m` graph on `{0,1}^k`,

```
c ≤ (m/2 − 1/ω_m) / (m² − 1),        H ≥ −ln c.
```

`ω_m` has two regimes: for **odd** `m` (`k ≡ 1 mod 4`) the graph is triangle-free
by parity, `ω_m = 2`, giving `c ≤ 1/(k+3)`; for **even** `m` (`k ≡ 3 mod 4`) a
clique is an equidistant code of length `2m−1` and distance `m`, so the Plotkin
bound gives `ω_m ≤ 2m` and `c ≤ 1/(k+1)`. Both collapse to the same statement:

```
min H ≥ ln( 4·⌈(k+1)/4⌉ )      for every odd k,
max classical share ≤ k·ln 2 − ln( 4·⌈(k+1)/4⌉ ).
```

`4·⌈(k+1)/4⌉` is exactly the order of the smallest Hadamard matrix `≥ k+1`, so
the bound is **attained** whenever that Hadamard matrix exists (its `OA(N,k,2,2)`
is the minimizer).

| k | m | ω_m | source of ω_m | min H | true max share | Lean cap `(k−2)ln2` |
|---|---|---|---|---|---|---|
| 3 | 2 | 4 | exact max-clique | `ln 4` | `ln 2` = 0.6931 | 0.6931 — **tight** |
| 5 | 3 | 2 | parity, exact | `ln 8` | `2 ln 2` = 1.3863 | 2.0794 — loose |
| 7 | 4 | 8 | exact max-clique | `ln 8` | `4 ln 2` = 2.7726 | 3.4657 — loose |
| 9 | 5 | 2 | parity, exact | `ln 12` | 3.7534 | 4.8520 — loose |
| 11 | 6 | 12 | Plotkin (upper bd) | `ln 12` | 5.1397 | 6.2383 — loose |
| 13 | 7 | 2 | parity, exact | `ln 16` | 6.2383 | 7.6246 — loose |

The `ω_m` values at `k = 3` and `k = 7` are exact branch-and-bound max-clique
computations on the 8- and 128-vertex graphs, and they match Plotkin exactly.
The table confirms Lean's `(k−2)·ln 2` is **tight at k = 3** (the parity state,
`share_parity`) and **strictly loose for every k ≥ 5** — the k = 3 saturation
recorded in `ShareK.lean` does not extend, and the file should not be read as
implying it does.

---

## The honest gap remaining

1. **Not mechanized.** This is exact computation plus a pen-and-paper argument,
   machine-*verified* but not machine-*checked*. Lean still proves only
   `(k−2)·ln 2`. Any published statement must keep saying `proved` for
   `3·ln 2` and mark `2·ln 2` at the strength this file actually earns —
   the same "exact-computed, not yet mechanized" wording `ShareK.lean`
   already uses.
2. **Two cited theorems are not in the repo's Lean**: Motzkin–Straus (step 4)
   and, for the general-`k` table only, Plotkin. Mechanizing `k = 5` needs
   Motzkin–Straus only for a triangle-free graph, where it reduces to
   `Σ_{v≠w, d=3} p_v p_w ≤ 1/2` — provable directly from
   `(Σ_{even} p)·(Σ_{odd} p) ≤ 1/4` since the distance-3 graph is bipartite
   between even- and odd-weight words. **That is the cheap mechanization
   route** and it avoids Motzkin–Straus entirely.
3. **Attainment at general `k`** rests on Hadamard existence; it is unconditional
   at the orders in the table (4, 8, 12, 16), conjectural in general.
4. **The quantum side is untouched here.** `qShareK(C5) = 5·ln 2` remains
   unmechanized; this file changes only the classical column.

---

## What is safe to say now

- "The classical maximum at k = 5 is exactly `2·ln 2`" — with the label
  *exact-computed here, not machine-checked*.
- "The proved cap `3·ln 2` is not tight; it is tight only at k = 3."
- "Quantum `5·ln 2` exceeds the true classical maximum by `3·ln 2`, and exceeds
  the machine-checked cap by `2·ln 2`."

**Do not** say the `3·ln 2` true margin is proved. It is not, yet.
