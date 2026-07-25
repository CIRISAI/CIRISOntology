# The exact classical maximum of the whole-only share at k = 6 and k = 7

**Status: exact, and attained, at both k. Not sampled lower bounds.**
Exact-computed and machine-verified here; **not** mechanized in Lean.

Script: `ARRAY_SCAN_K67.py` — self-contained; the exhaustive support enumerator is
embedded in it as C (`OA_ENUM_C`) and compiled on demand, so the script alone
reproduces every number here. Full run log: `array_scan_k67.log` ·
machine-readable: `array_scan_k67_results.json`

Companion to `CLASSICAL_MAX_K5.md` (k = 5 solved exactly: max share = `2·ln 2`).

---

## Headline

> **The true classical maximum of `shareK` over all pair-uniform states is exactly
> `3·ln 2` at k = 6 and exactly `4·ln 2` at k = 7.**
>
> Both are *attained*: at k = 6 by the uniform distribution on any of exactly
> **240** eight-point supports, at k = 7 by any of exactly **480** — and by
> nothing else. In both cases the entropy minimum is `ln 8`.
>
> **The conjecture `max share(k) = (k − ⌈log₂(k+1)⌉)·ln 2` SURVIVES at k = 6 and
> k = 7**, and it survives against the truth, not merely against a search.

| k | ⌈log₂(k+1)⌉ | conjectured max share | **computed max share** | verdict |
|---|---|---|---|---|
| 6 | 3 | `3·ln 2` = 2.079441541679836 | **`3·ln 2` = 2.079441541679836** | **SURVIVES** (exact) |
| 7 | 3 | `4·ln 2` = 2.772588722239781 | **`4·ln 2` = 2.772588722239781** | **SURVIVES** (exact) |

Nothing beat the code value. Attack (B), the GPU search over the full polytope,
returned the same `ln 8` across 787 492 restarts spanning both k and never went
below it — as it cannot, because attack (A) proves it cannot.

**But the form has a boundary, and it is close.** The same machinery shows
`(k − ⌈log₂(k+1)⌉)·ln 2` is **FALSE from k = 8 through k = 11**, where a
non-power-of-two orthogonal array (order-12 Hadamard) beats every linear code.
k = 6 and k = 7 are the last two values before it breaks. See "Where the form
dies" below — this is the finding to carry forward, because it means the form is
a coincidence of small k, not a law.

---

## Which attack established which number

Every cell is marked **exhaustive** (a complete finite enumeration or a proof) or
**searched** (a lower bound on max share only).

| k | quantity | value | how established | status |
|---|---|---|---|---|
| 6 | min H over `P₆`, lower bound | `≥ ln 8` | analytic: frame + Frobenius identity, parity of odd integers | **exhaustive** (proof) |
| 6 | min H over `P₆`, upper bound | `≤ ln 8` | exhibited witness, verified in exact rationals | **exhaustive** (witness) |
| 6 | number of minimisers | **240** | complete DFS over all `C(64,8)` = 4 426 165 368 eight-subsets | **exhaustive** |
| 6 | min \|C\| over linear codes | 8 | complete enumeration of all **2825** subspaces of `F₂⁶` | **exhaustive** |
| 6 | **max share** | **`3·ln 2`** | the two bounds meet | **EXACT** |
| 6 | GPU search best H | `ln 8` | 449 992 restarts, nothing lower | *searched* |
| 7 | min H over `P₇`, lower bound | `≥ ln 8` | analytic: frame + Frobenius identity, positivity alone | **exhaustive** (proof) |
| 7 | min H over `P₇`, upper bound | `≤ ln 8` | exhibited witness ([7,3,4] simplex code) | **exhaustive** (witness) |
| 7 | number of minimisers | **480** | complete DFS over all `C(128,8)` = 1 429 702 652 400 eight-subsets | **exhaustive** |
| 7 | min \|C\| over linear codes | 8 | complete enumeration of all **29 212** subspaces of `F₂⁷` | **exhaustive** |
| 7 | **max share** | **`4·ln 2`** | the two bounds meet | **EXACT** |
| 7 | GPU search best H | `ln 8` | 337 500 restarts, nothing lower | *searched* |

The GPU rows are corroboration only. They are stated as what they are: a search
gives an **upper bound on min H**, equivalently a **lower bound on max share**,
and never a maximum. Here the search's bound and the proof's bound coincide,
which is the most a search can do.

---

## Why the problem is a minimum-entropy problem

Unchanged from k = 5, so only the one line: for pair-uniform `p` on `{0,1}^k` the
envelope contains the uniform distribution, which attains the global entropy
maximum `k·ln 2`, so

```
share(p) = k·ln 2 − H(p),      max classical share = k·ln 2 − min_{p ∈ P_k} H(p)
```

with `P_k = {p on {0,1}^k : all C(k,2) pair marginals uniform}`. Everything below
is about `min H`.

---

## Attack (A1) — exhaustive over every linear code

**The criterion, in its shortest form.** For `p` uniform on a linear code
`C ⊆ F₂^k`, the Fourier coefficient is `p̂(S) = [S ∈ C^⊥]`. Pair-uniformity is
`p̂(S) = 0` for `1 ≤ |S| ≤ 2`, i.e. `C^⊥` has no word of weight 1 or 2. Reading
that off the generator matrix `G` of `C`:

- `e_i ∈ C^⊥` ⟺ every row of `G` is 0 in position `i` ⟺ **column `i` of `G` is zero**;
- `e_i + e_j ∈ C^⊥` ⟺ every row agrees at `i` and `j` ⟺ **columns `i` and `j` are equal**.

So:

> uniform-on-`C` is pair-uniform ⟺ the `k` columns of `G` are **nonzero and
> pairwise distinct**.

**The arithmetic, worked explicitly.** A dimension-`m` code has its `k` columns in
`F₂^m`, which holds `2^m − 1` nonzero vectors. Distinctness forces

```
k ≤ 2^m − 1   ⇒   2^m ≥ k+1   ⇒   m ≥ ⌈log₂(k+1)⌉
```

which is exactly the Hamming/sphere-packing bound in its shortest form — a
parity-check matrix with distinct nonzero columns *is* a Hamming code. Hence

```
|C| ≥ 2^⌈log₂(k+1)⌉,     min H over linear-code states = ⌈log₂(k+1)⌉·ln 2,
max share over linear-code states = (k − ⌈log₂(k+1)⌉)·ln 2.
```

That is the conjecture, and this is where its shape comes from. Note the
consequence: **the conjectured form is the linear-code answer**, nothing more.
Whether it is also the true answer is a separate question — settled yes here at
k = 6, 7 by attack (A2), and settled **no** at k = 8..11 below.

**k = 6.** `⌈log₂7⌉ = 3` ⇒ `|C| ≥ 8`, `H ≥ 3·ln 2`, share `≤ 3·ln 2`.
**k = 7.** `⌈log₂8⌉ = 3` ⇒ `|C| ≥ 8`, `H ≥ 3·ln 2`, share `≤ 4·ln 2`.

**Exhaustive confirmation.** Every subspace of `F₂^k` was enumerated by its unique
reduced row echelon form — 2825 at k = 6 and 29 212 at k = 7, matching the Galois
numbers `G₆` and `G₇` exactly. The column criterion was cross-checked against a
brute-force dual-distance computation on a sample of subspaces (76 at k = 6, 789
at k = 7): **0 disagreements**.

| k | subspaces | pair-uniform, by \|C\| | min \|C\| | codes at the minimum |
|---|---|---|---|---|
| 6 | 2825 = `G₆` | 8:**30** · 16:175 · 32:42 · 64:1 | **8** | **30** |
| 7 | 29 212 = `G₇` | 8:**30** · 16:1605 · 32:1225 · 64:99 · 128:1 | **8** | **30** |

No code of dimension 0, 1 or 2 is pair-uniform at either k, as the bound requires.

### The k = 7 subtlety, worked carefully

The mission flagged a possible falsification at k = 7. It does not occur, and the
reason is a duality bookkeeping point worth stating plainly, because it is easy to
get backwards:

> It is tempting to say "the perfect Hamming `[7,4,3]` code has `2⁴ = 16`
> codewords, so `|C| = 16`, `H = 4·ln 2`, and the share is `7·ln2 − 4·ln2 = 3·ln 2`
> — contradicting the predicted `4·ln 2`."

That reads the duality the wrong way round. The code that must have distance ≥ 3
is the **dual** `C^⊥`, not `C`. The Hamming `[7,4,3]` code *is* `C^⊥`. So

```
|C^⊥| = 2⁴ = 16,    |C| = 2⁷ / |C^⊥| = 128 / 16 = 8,
H = ln 8 = 3·ln 2,  share = 7·ln 2 − 3·ln 2 = 4·ln 2 = 2.772588722239781.
```

`C` is the `[7,3,4]` **simplex code** — all seven nonzero codewords of weight 4.
The exhaustive enumeration confirms it: the minimising codes at k = 7 have nonzero
weight set exactly `{4}`, and there are **30** of them, which is exactly the number
of distinct Hamming codes of length 7 (`7!/|Aut| = 5040/168 = 30`).

And the conjecture's `⌈log₂(k+1)⌉` is the **redundancy of the dual** (= `dim C`),
not the dual's dimension. `(7 − 3)·ln 2 = 4·ln 2`. **Agrees.** No falsification.

A minimising code at k = 7, explicitly (generator columns `1,2,4,7,6,5,3` — the
seven nonzero vectors of `F₂³`, distinct as required):

```
0000000  0001111  0110011  0111100  1010101  1011010  1100110  1101001
```

All 21 pair marginals verified `= 1/4` in exact rationals.

---

## Attack (A2) — the bound over the FULL polytope

Attack (A1) only covers linear codes. This section covers **every** point of
`P_k`, including non-uniform distributions on supports of any size, and is what
makes the answer exact rather than a best-known.

**The frame identity.** With `u_v = (1, χ₁(v), …, χ_k(v)) ∈ {±1}^{k+1}`,
pair-uniformity says exactly

```
Σ_v p_v u_v u_vᵀ = I_{k+1}      for every p ∈ P_k.
```

*Verified: 200 random interior points, max deviation `6.7e−16` (k=6), `8.9e−16` (k=7).*

**The Frobenius identity.** Taking `‖·‖_F²` of both sides, with
`u_v · u_w = (k+1) − 2·d(v,w)`:

```
Σ_{v,w} p_v p_w ((k+1) − 2 d(v,w))² = k+1.
```

*Verified: max deviation `3.6e−15` at both k.*

Write `c = Σ_v p_v²` for the collision probability. The diagonal (`d = 0`)
contributes `(k+1)² c`.

### k = 7 needs nothing but positivity

Every off-diagonal term `p_v p_w (u_v·u_w)²` is **≥ 0**. Dropping all of them:

```
(k+1)² c ≤ k+1   ⇒   c ≤ 1/(k+1).
```

This is the **Rao bound** (`|supp| ≥ k+1` for a strength-2 orthogonal array),
recovered in one line. At k = 7 it reads `c ≤ 1/8` — **which is already the
answer.** No parity argument, no clique number, no Motzkin–Straus, no Plotkin.

k = 7 is the *cheapest* case in the whole family, because `k+1 = 8` is exactly the
size of the optimal support: Rao is tight there.

### k = 6 needs one extra line (and still no graph theory)

At even `k`, `k+1` is odd, so `(k+1) − 2d` is an **odd integer for every `d`**, and
therefore never zero: `((k+1) − 2d)² ≥ 1` with no exceptions. There is no
zero-cost distance class at all, hence nothing for a clique number to measure:

```
k+1 = (k+1)² c + Σ_{v≠w} p_v p_w ((k+1)−2d)²  ≥  (k+1)² c + (1 − c)
⇒ ((k+1)² − 1) c ≤ k   ⇒   c ≤ k/((k+1)²−1) = 1/(k+2).
```

At k = 6: `c ≤ 1/8`. The finite check it rests on is seven cases,
`(7−2d)² ∈ {49,25,9,1,1,9,25}` for `d = 0..6` — minimum 1, as required.

**Both k = 6 and k = 7 are therefore strictly cheaper to prove than k = 5**, which
needed Motzkin–Straus (or the bipartite trick) because at k = 5 the elementary
bounds give only `c ≤ 1/6`, short of the true `1/8`. This is the main
mechanization finding of this file.

### The chain, and the equality analysis

```
c ≤ 1/8  ⇒  H(p) ≥ H₂(p) = −ln c ≥ ln 8 = 3·ln 2
         ⇒  max share ≤ k·ln 2 − ln 8
         ⇒  |supp(p)| ≥ 1/c ≥ 8      (Cauchy–Schwarz: c ≥ 1/|supp|)
```

`H ≥ H₂` is Rényi monotonicity. **Equality analysis:** `H = ln 8` forces `H = H₂`,
hence `p` uniform on its support; `c = 1/8` with `p` uniform forces `|supp| = 8`.
So every minimiser is the uniform distribution on an 8-point pair-uniform
support — an `OA(8,k,2,2)`. These exist at both k, so the bound is **attained**:

```
k = 6:  min H = ln 8,  max share = 6·ln2 − ln8 = 3·ln 2
k = 7:  min H = ln 8,  max share = 7·ln2 − ln8 = 4·ln 2
```

**Tightness of `c ≤ 1/8`, checked numerically.** Maximizing the convex `Σ p²` over
`P_k` from 4000 GPU restarts returns `0.125000000000` at both k — the bound
saturated, as the equality analysis predicts.

**The k = 5-style refinement, run at k = 7 as an independent cross-check.** Even
though it is not needed, the k = 5 machinery was executed at k = 7 and lands on the
same number: the distance-4 graph on 128 vertices is 35-regular with 2240 edges;
its **exact** maximum clique (branch and bound, exhaustive) is `ω = 8`, matching
the Plotkin bound `A(7,4) ≤ 2⌊4/(2·4−7)⌋ = 8`; the witness clique has all pairwise
distances exactly 4; Motzkin–Straus then gives `S ≤ 1 − 1/8 = 7/8` (numerically
confirmed at `0.875000000000` by 3000 replicator runs), and
`60c ≤ 4 + 4S ≤ 7.5` ⇒ `c ≤ 1/8`. Same answer, longer road.

---

## Attack (A3) — exhaustive enumeration of the minimisers

Supports of size ≤ 7 need no enumeration at all: `c ≤ 1/8` and `c ≥ 1/|supp|` give
`|supp| ≥ 8` outright. Supports of size 8 must carry the uniform distribution, by
the equality analysis. So the complete set of minimisers is the set of 8-point
pair-uniform supports, and that is a finite object that can simply be listed.

The condition on an 8-subset `S` is `Σ_{v∈S} u_v u_vᵀ = 8·I_{k+1}`, i.e. every
off-diagonal partial sum `A_ij` vanishes. The embedded C enumerator does a
depth-first search over subsets in increasing index order with the single prune
`|A_ij| ≤ 8−t` — which is **lossless**, since each of the `8−t` remaining points
moves `A_ij` by exactly ±1. No code-theoretic structure is assumed anywhere in the
search, and no candidate satisfying the condition can be pruned away.

| k | subsets in the search space | **minimisers found** | with 0 forced | translation check | time |
|---|---|---|---|---|---|
| 6 | `C(64,8)` = 4 426 165 368 | **240** | 30 | 30 × 64/8 = 240 ✓ | 0.04 s |
| 7 | `C(128,8)` = 1 429 702 652 400 | **480** | 30 | 30 × 128/8 = 480 ✓ | 0.87 s |

The two columns are independent runs (the second forces `0 ∈ S`, valid because the
solution set is closed under translation `v ↦ v+t` and each solution has 8
translates containing 0); they agree exactly.

**Structure of the minimisers.** All 30 zero-containing minimisers at each k were
checked and **all 30 are linear codes** — so every minimiser is a coset of one of
the 30 minimising codes found independently in attack (A1), and the two attacks
close on each other:

```
k = 6:  240 = 30 codes × 8 cosets      nonzero weight set {3,4}
k = 7:  480 = 30 codes × 16 cosets     nonzero weight set {4}   ([7,3,4] simplex)
```

**Why 30 at both k**, from the column criterion: a minimising code has a `3×k`
generator matrix whose `k` columns are distinct nonzero vectors of `F₂³`, of which
there are exactly 7; two generator matrices give the same code iff they differ by a
change of basis, i.e. by `GL(3,2)`, of order 168. So the count is the number of
ordered `k`-tuples of distinct nonzero vectors, divided by 168:

```
k = 6:  (7·6·5·4·3·2)/168 = 5040/168 = 30
k = 7:  7!/168            = 5040/168 = 30
```

At k = 7 this is the classical count of the distinct Hamming codes of length 7.

Pairwise-distance signatures, both forced by the Frobenius identity and both
confirmed in the enumerated witnesses:

- **k = 6**: `Σ_{v≠w}(u_v·u_w)² = 8·7·(8−7) = 56` over 56 ordered pairs, so every
  `|u_v·u_w| = 1` and every pairwise distance is 3 or 4. *Observed: `{3,4}`.*
- **k = 7**: `Σ_{v≠w}(u_v·u_w)² = 8·8·(8−8) = 0`, so all 8 rows are **mutually
  orthogonal** — `[1|M]` is an 8×8 Hadamard matrix and every pairwise distance is
  exactly 4. *Observed: `{4}`.* This is also why `ω = 8` in attack (A2): the
  minimisers *are* the maximum cliques of the distance-4 graph.

All recorded witnesses passed an exact-rational pair-marginal check (0 failures).

---

## Attack (B) — GPU search over the full polytope

A search, reported as a search. It cannot establish a maximum; it can only fail to
beat one, and that is what it did.

**Method.** Parameterize `p` on `2^k` cells. Project onto `P_k` by iterative
proportional fitting against the `C(k,2)` uniform pair marginals — the natural
I-projection, and embarrassingly parallel as a batched `(B,N)·(N,4)` matmul per
constraint. Minimize `H` by the multiplicative step along `−∇H`, which for
`∇H = −(ln p + 1)` is `p ← p^{1+η}` renormalized, then re-project. `η` annealed
`0.02 → 0.62`. Search in float32; the lowest-entropy candidates are then refined in
float64 with 800 further IPF sweeps and accepted only at feasibility residual
`< 1e−10`.

**Hardware.** NVIDIA GeForce RTX 4090 Laptop (16 GB, CUDA 13 driver / toolkit 12.0,
cupy 14.1.1); measured 546 GFLOPS fp64 and 13.4 TFLOPS fp32. Batches of 200 000
(k=6) and 150 000 (k=7) restarts held resident.

**Three families of restarts** were run at each k: (a) cold random; (b) seeded from
optimal code states perturbed with uniform noise at fractions `1e−4 … 0.9`, a
direct local-optimality probe; (c) a directed attempt to break `ln 8` — 12
annealing schedules crossing outer iterations `{300, 800}` × IPF sweeps `{10, 30}`
× start skew `p^{0.4, 1, 4}`.

| k | cold | seeded | schedules | **total restarts** | **best H found** | beat `ln 8`? | wall |
|---|---|---|---|---|---|---|---|
| 6 | 200 000 | 50 000 | 12 × 16 666 | **449 992** | `2.079441541679836` | **no** | 318 s |
| 7 | 150 000 | 37 500 | 12 × 12 500 | **337 500** | `2.079441541679836` | **no** | 481 s |

`2.079441541679836` is `ln 8` to all 16 digits — the search reproduces the exact
optimum and never goes below it. At **both** k, **0** refined points fell below
`ln 8`, **0** seeded restarts escaped below it, and all 12 annealing schedules
reached the optimum exactly (best = worst = `ln 8`, spread `0.0e+00`).

The histogram of converged local minima is discrete with a clean gap above the
optimum — the search is not merely failing to find something lower, it is landing
in a well-separated bottom bin:

| k | converged feasible | landing on `ln 8` | bottom bin | next occupied bin |
|---|---|---|---|---|
| 6 | 136 537 of 200 000 | 41.0 % | `[3.0000, 3.0673)·ln2` — 56 023 | `[3.5386, …)` |
| 7 | 16 874 of 150 000 | 35.0 % | `[3.0000, 3.0833)·ln2` — 5 900 | `[3.5834, …)` |

Nothing sits between `3·ln 2` and roughly `3.54·ln 2` at either k.

Stated at the strength it has: **max share ≥ 3·ln 2 (k=6) and ≥ 4·ln 2 (k=7) from
the search**; that these are also the maxima comes from attack (A), not from here.

---

## Where the form dies — k = 8 through k = 11

The conjecture is the *linear-code* answer, and linear codes can only produce
supports of size a power of two. The true minimum is `ln N` for `N` the smallest
order of an `OA(N,k,2,2)`, which is a multiple of 4 (conjecturally
`4⌈(k+1)/4⌉`, Hadamard). The two coincide exactly when `4⌈(k+1)/4⌉` is a power of
two — and it stops being one at k = 8.

Explicit witness, constructed and checked here: the Paley type-I **Hadamard matrix
of order 12** (`HᵀH = 12·I`, verified). Its 11 non-constant columns are pairwise
orthogonal and sum to zero, so its 12 rows, read as points of `{0,1}^k` for any
`k ≤ 11`, form an `OA(12,k,2,2)` — every pair marginal exactly `3/12 = 1/4` per
cell. The 12 rows stay distinct for every `k ≥ 8`, so the uniform distribution on
them has `H = ln 12`.

| k | conjectured min H | witness gives min H ≤ | verdict |
|---|---|---|---|
| 8 | `⌈log₂9⌉·ln2 = 4·ln2 = ln 16` | **`ln 12`** | **FALSIFIED** |
| 9 | `⌈log₂10⌉·ln2 = 4·ln2 = ln 16` | **`ln 12`** | **FALSIFIED** |
| 10 | `⌈log₂11⌉·ln2 = 4·ln2 = ln 16` | **`ln 12`** | **FALSIFIED** |
| 11 | `⌈log₂12⌉·ln2 = 4·ln2 = ln 16` | **`ln 12`** | **FALSIFIED** |

At k = 8 that means `max share ≥ 8·ln2 − ln 12 = 3.060271` against a conjectured
`(8−4)·ln 2 = 2.772589`. The conjecture **understates** the truth there, by at
least `ln(16/12) = 0.287682`. All four witnesses passed the exact-rational
pair-marginal check.

So the honest scope of the surviving form is: it is **verified** at k = 3, 5, 6, 7,
and **disproved** at k = 8–11. At k = 12–15 the two formulas happen to agree
arithmetically (`4⌈(k+1)/4⌉ = 16` is a power of two there) but that is not a
verification — it would still need a matching lower bound, which this file does not
supply. From k = 16 the arithmetic diverges again (`4⌈17/4⌉ = 20` vs `2⁵ = 32`).
**k = 6 and k = 7 are the last two values before the form breaks.** They confirm it
at those k and provide no evidence for it anywhere else.

(The exact minima at k = 8..11 are *not* settled here — only that they are below
the conjectured value. The elementary bounds of attack (A2) give
`c ≤ 1/(k+2)` at even k, i.e. `min H ≥ ln 10` at k = 8, which does not meet
`ln 12`. Closing that gap needs the k = 5-style clique machinery and is out of
scope. k = 4 is likewise unsettled by these methods: elementary bounds give only
`min H ≥ ln 6` against an attained `ln 8`.)

---

## Consequence for the Lean cap

`Core/ShareK.lean` proves `shareK ≤ (k−2)·log 2`. Against the truth:

| k | Lean's proved cap `(k−2)·ln2` | **true classical max** | slack |
|---|---|---|---|
| 3 | `1·ln 2` = 0.693147 | `1·ln 2` = 0.693147 | **tight** |
| 5 | `3·ln 2` = 2.079442 | `2·ln 2` = 1.386294 | loose by `ln 2` |
| 6 | `4·ln 2` = 2.772589 | **`3·ln 2` = 2.079442** | loose by `ln 2` |
| 7 | `5·ln 2` = 3.465736 | **`4·ln 2` = 2.772589** | loose by `ln 2` |

The cap is loose by exactly `ln 2` at k = 5, 6 and 7, for one reason: the true
entropy minimum is `ln 8 = 3·ln 2` throughout that range, while the cap subtracts
only `2·ln 2`. The cap is tight only at k = 3, as `CLASSICAL_MAX_K5.md` already
recorded; nothing here changes that, and nothing here is mechanized.

**The cheap mechanization target this file identifies:** the k = 7 bound needs only
the frame identity, the Frobenius identity, and the positivity of squares — no
graph theory, no Motzkin–Straus, no Plotkin, no case analysis. k = 6 adds one
finite check over seven distance values. Both are materially easier to mechanize
than the k = 5 result already in hand.

---

## The honest gap remaining

1. **Not mechanized.** Exact computation plus a pen-and-paper argument,
   machine-*verified*, not machine-*checked*. Lean still proves only `(k−2)·ln 2`.
   Any published statement must keep saying `proved` for the Lean cap and mark
   these values at the strength this file earns — *exact-computed, not mechanized*,
   the same wording `ShareK.lean` already uses for k = 5.
2. **Attack (B) is a search** and is reported as one throughout. It corroborates;
   it establishes nothing.
3. **The conjecture is confirmed only at k = 6 and k = 7**, and is **disproved at
   k = 8..11**. It must not be quoted as a general law. If it appears anywhere in
   the stance or the Lean, it needs the range restriction attached.
4. **k = 4 and k = 8..11 exact minima are open** by these methods (see above).
5. **The quantum side is untouched here.** This file changes only the classical
   column.

---

## What is safe to say now

- "The classical maximum at k = 6 is exactly `3·ln 2`, and at k = 7 exactly
  `4·ln 2`" — labelled *exact-computed here, not machine-checked*.
- "The Hamming form `(k − ⌈log₂(k+1)⌉)·ln 2` holds at k = 6 and k = 7, and fails
  from k = 8" — both halves, never the first alone.
- "The proved cap `(k−2)·ln 2` is loose by exactly `ln 2` at k = 5, 6, 7; it is
  tight only at k = 3."

**Do not** say the conjecture is a theorem for general `k`. It is false at k = 8.
**Do not** cite the `ln 2` slack as proved. It is not, yet.
