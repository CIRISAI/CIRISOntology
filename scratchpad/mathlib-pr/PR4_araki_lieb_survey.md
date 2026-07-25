# Araki–Lieb ladder vs Mathlib master — survey and port plan

**Checked against:** mathlib4 master @ `c8830a1d9ceaffabd7c8c7493d9a9be3ead6ea74`
(2026-07-25 09:21 UTC, toolchain `leanprover/lean4:v4.33.0-rc1`; sparse clone of
`Mathlib/` + `docs/`). This is ~2 days newer than the master used for
`MASTER_FINDINGS.md` (`bbc4475e`).

**Method, stated honestly:** this is a *source-reading* survey. Nothing was
built, elaborated, or type-checked. Every "ALREADY UPSTREAM" claim below quotes
a file path and line number in master and can be re-checked by opening it.
Every "ABSENT" claim rests on exhaustive `grep` over all 8291 master `.lean`
files, plus a GitHub API sweep of open and closed PRs. Claims that a proposed
*proof route* works (as opposed to a claim that a lemma exists) are marked as
unverified predictions, because they are.

Our side of the comparison is `CIRISOntology/Core/EntropyIneq.lean` (1049 lines)
and `CIRISOntology/Core/ShareQuantum.lean` (370 lines), both sorry-free against
our pinned v4.14.

---

## Headline: the quantum half is a green field; the spectral half is now redundant

Two findings, pulling in opposite directions.

**1. There is no quantum information theory in Mathlib. At all.** No von
Neumann entropy, no density operator, no partial trace, no Araki–Lieb, no
subadditivity — and no *classical* Shannon entropy of a finite distribution
either. Nor has anyone ever tried: a GitHub search over every mathlib4 PR ever
opened for "von Neumann entropy" / "Araki" / "Schur-Horn" / "partial trace"
returns three false-positive hits about `HasLineDerivAt`. Our ladder's summits
(pinching, subadditivity, Araki–Lieb) are genuinely new to Mathlib and nobody
is racing us.

**2. Our entire spectrum-bookkeeping substructure is redundant.** In the two
years since our pin, master grew `Matrix.charpoly` machinery that does
everything our bespoke `det(x•1 − A)` + `Polynomial.funext` bridge does, and
does it better. `Matrix.IsHermitian.roots_charpoly_eq_eigenvalues` *is* our
multiset bridge; `Matrix.charpoly_mul_comm'` *is* our Weinstein–Aronszajn
step, already in zero-padded form; `charpoly_reindex` / `charpoly_transpose` /
`charpoly_units_conj` *are* our three spectrum-blindness lemmas. Roughly 400
lines of our 1419 exist upstream in better form.

The port is therefore not a port. It is a rewrite of the top of the ladder onto
an upstream base that did not exist when we built the bottom of it.

---

## 1. What master has (everything quoted, all verified by opening the file)

### Scalar groundwork — present, and better than ours

| Object | Master name | Where |
|---|---|---|
| `x ↦ x log x` | `Real.mul_log`-prefixed lemmas | `Analysis/SpecialFunctions/Log/NegMulLog.lean` |
| `x ↦ −x log x` | `Real.negMulLog` | `…/NegMulLog.lean:164` |
| convexity of `x log x` on `[0,∞)` | `Real.convexOn_mul_log` | `…/NegMulLog.lean:144` |
| strict version | `Real.strictConvexOn_mul_log` | `…/NegMulLog.lean:137` |
| concavity of `negMulLog` | `Real.concaveOn_negMulLog` | `…/NegMulLog.lean:227` |
| `x − 1 ≤ x log x` (our Gibbs trick) | `Real.self_sub_one_le_mul_log` | `…/NegMulLog.lean:39` |
| continuity of `negMulLog` | `Real.continuous_negMulLog` | `…/NegMulLog.lean:186` |
| finite Jensen, convex direction | `ConvexOn.map_sum_le` | `Analysis/Convex/Jensen.lean:67` |

### Matrix spectral theory — present, and much stronger than at our pin

| Object | Master name | Where |
|---|---|---|
| charpoly factors over eigenvalues | `Matrix.IsHermitian.charpoly_eq` | `Analysis/Matrix/Spectrum.lean:155` |
| **eigenvalue multiset = charpoly roots** | `Matrix.IsHermitian.roots_charpoly_eq_eigenvalues` | `Analysis/Matrix/Spectrum.lean:159` |
| eigenvalues determined by charpoly | `Matrix.IsHermitian.eigenvalues_eq_eigenvalues_iff` | `Analysis/Matrix/Spectrum.lean:180` |
| trace = sum of eigenvalues | `Matrix.IsHermitian.trace_eq_sum_eigenvalues` | `Analysis/Matrix/Spectrum.lean:238` |
| det = product of eigenvalues | `Matrix.IsHermitian.det_eq_prod_eigenvalues` | `Analysis/Matrix/Spectrum.lean:191` |
| spectral theorem | `Matrix.IsHermitian.spectral_theorem` | `Analysis/Matrix/Spectrum.lean:141` |
| **rectangular Weinstein–Aronszajn, charpoly form** | `Matrix.charpoly_mul_comm'` | `LinearAlgebra/Matrix/Charpoly/Basic.lean:238` |
| … and its one-sided form | `Matrix.charpoly_mul_comm_of_le` | `…/Charpoly/Basic.lean:261` |
| square version | `Matrix.charpoly_mul_comm` | `…/Charpoly/Basic.lean:268` |
| charpoly under relabeling | `Matrix.charpoly_reindex` | `…/Charpoly/Basic.lean:168` |
| charpoly under transpose | `Matrix.charpoly_transpose` | `…/Charpoly/Basic.lean:165` |
| charpoly under conjugation by a unit | `Matrix.charpoly_units_conj` | `…/Charpoly/Basic.lean:280` |
| charpoly of a diagonal | `Matrix.charpoly_diagonal` | `…/Charpoly/Basic.lean:150` |
| charpoly of `vecMulVec` | `Matrix.charpoly_vecMulVec` | `…/Charpoly/Basic.lean:271` |
| classical Weinstein–Aronszajn | `Matrix.det_one_add_mul_comm` | `LinearAlgebra/Matrix/SchurComplement.lean:401` |

### Matrix positivity — present

| Object | Master name | Where |
|---|---|---|
| `vecMulVec a (star a)` is PSD | `Matrix.posSemidef_vecMulVec_self_star` | `LinearAlgebra/Matrix/PosDef.lean:412` |
| diagonal PSD iff entries ≥ 0 | `Matrix.posSemidef_diagonal_iff` | `LinearAlgebra/Matrix/PosDef.lean:71` |
| PSD trace ≥ 0 | `Matrix.PosSemidef.trace_nonneg` | `LinearAlgebra/Matrix/PosDef.lean:349` |
| PSD eigenvalues ≥ 0 | `Matrix.PosSemidef.eigenvalues_nonneg` | `Analysis/Matrix/PosDef.lean:42` |
| PSD ⟺ Hermitian + nonneg eigenvalues | `Matrix.IsHermitian.posSemidef_iff_eigenvalues_nonneg` | `Analysis/Matrix/PosDef.lean:34` |
| Kronecker of PSD is PSD | `Matrix.PosSemidef.kronecker` | `Analysis/Matrix/Order.lean:213` |
| PSD under `submatrix` by an equiv | `Matrix.posSemidef_submatrix_equiv` | `LinearAlgebra/Matrix/PosDef.lean:144` |
| trace as a positive linear map | `Matrix.tracePositiveLinearMap` | `Analysis/Matrix/Order.lean:280` |
| real diagonal of a Hermitian | `Matrix.IsHermitian.coe_re_diag` | `Analysis/Matrix/Hermitian.lean:39` |

### The matrix logarithm — present, via CFC, and this changes the design question

| Object | Master name | Where |
|---|---|---|
| **operator/matrix logarithm** | `CFC.log a := cfc Real.log a` | `Analysis/SpecialFunctions/ContinuousFunctionalCalculus/ExpLog/Basic.lean:121` |
| `log` operator monotone | `CFC.log_monotoneOn`, `CFC.log_le_log` | `…/ExpLog/Order.lean:76,96` |
| `log` operator concave | `CFC.concaveOn_log` | `…/ExpLog/Order.lean:102` |
| CFC instance on matrices | `Matrix.instIsometricContinuousFunctionalCalculus` | `Analysis/Matrix/Order.lean:345` |
| CFC of a Hermitian = `U · diagonal (f ∘ λ) · U*` | `Matrix.IsHermitian.cfc`, `cfc_eq` | `Analysis/Matrix/HermitianFunctionalCalculus.lean:132,143` |
| **charpoly of `cfc f A`** | `Matrix.IsHermitian.charpoly_cfc_eq` | `Analysis/Matrix/HermitianFunctionalCalculus.lean:152` |

The load-bearing remark is in the docstring at
`Analysis/Matrix/HermitianFunctionalCalculus.lean:128-130`: *"this actually
operates on bare functions since every function is continuous on the spectrum
of a matrix, since the spectrum is finite."* So `cfc f A` is well-behaved on a
matrix for **any** `f : ℝ → ℝ`, including ones discontinuous at 0. This removes
the usual objection to defining von Neumann entropy through a functional
calculus.

### Adjacent, and relevant to how we should NOT state things

| Object | Master name | Where |
|---|---|---|
| doubly stochastic matrices | `doublyStochastic` | `Analysis/Convex/DoublyStochasticMatrix.lean:42` |
| Birkhoff–von Neumann | `doublyStochastic_eq_convexHull_permMatrix` | `Analysis/Convex/Birkhoff.lean:166` |
| binary / q-ary entropy (scalar) | `Real.binEntropy`, `Real.qaryEntropy` | `Analysis/SpecialFunctions/BinaryEntropy.lean` |
| KL divergence (measure-theoretic) | `klDiv`, `klFun` | `InformationTheory/KullbackLeibler/` |
| Kraft–McMillan | `kraft_mcmillan_inequality` | `InformationTheory/Coding/KraftMcMillan.lean` |
| topological entropy (unrelated) | `coverEntropy`, `netEntropy` | `Dynamics/TopologicalEntropy/` |

---

## 2. What master does NOT have (each verified by exhaustive grep)

- **von Neumann entropy** — `grep -ril "von Neumann entropy" Mathlib` → zero hits.
- **Shannon entropy of a finite distribution** — the complete list of
  identifiers in master containing "entropy" is `binEntropy*`, `qaryEntropy*`,
  and the `coverEntropy*`/`netEntropy*` dynamics family. There is no
  `∑ i, negMulLog (p i)` anywhere: `grep -rn negMulLog Mathlib` outside
  `Analysis/SpecialFunctions/` returns nothing. No `measureEntropy`,
  `condEntropy`, or `mutualInfo` in `Mathlib/Probability` or
  `Mathlib/MeasureTheory` either — the PFR-project entropy was never upstreamed.
- **Density operators / partial trace / anything quantum** — `grep -rin
  "partialTrace|partial trace|traceLeft|traceRight"` → zero hits;
  `densityMatrix` → zero hits. The only quantum content in master is
  `Algebra/Star/CHSH.lean` (Tsirelson's bound), which shares no API with us.
- **Araki–Lieb** — `grep -rin "\baraki\b"` → zero hits (the case-insensitive
  substring hits are all the author name "Karatarakis").
- **Schur–Horn** — one hit, and it is a *docstring comment* at
  `Analysis/InnerProductSpace/Spectrum.lean:46-48` explaining why eigenvalues
  are listed in decreasing order: *"For example the Schur-Horn theorem states
  that the diagonal … is majorized by the eigenvalue sequence."* The theorem
  itself is not proved.
- **Majorization** — not in master; explicitly a TODO at
  `Analysis/Convex/Birkhoff.lean:29`. **But it is contested in flight**, see
  Risks below.
- **Unistochastic matrices** — `grep -rin unistochastic` → zero hits. Nothing
  connects a unitary to a doubly stochastic matrix.
- **Operator Jensen / Klein's inequality / Golden–Thompson / Peierls** — none.
  Master's operator-convexity stock is exactly `rpow` and `log`
  (`…/Rpow/Order.lean`, `…/ExpLog/Order.lean`); the file headers cite Carlen's
  *"Trace inequalities and quantum entropies"* as a reference but no trace
  inequality from it is formalized.
- **Eigenvalue lemmas we might have hoped for** — no `eigenvalues_diagonal`,
  no `eigenvalues_conj`, no `eigenvalues_submatrix`, no `eigenvalues_kronecker`.
  These are all *reachable* through the charpoly lemmas above, which is why
  nobody has stated them directly.

---

## 3. Stone-by-stone classification

Three buckets, as asked. "SUPERSEDED" is a fourth that the brief did not
anticipate but the evidence forces: the *statement* is absent from master, but
our *proof* is obsolete because master now has a better route, so what we would
port is a short corollary rather than the machinery we wrote.

### ShareQuantum.lean

| Our stone | Verdict | Master counterpart / note |
|---|---|---|
| `IsDensity` | ABSENT-and-portable | trivial def; but see §4 on whether Mathlib wants it |
| `ptr₁₂ / ptr₁₃ / ptr₂₃` | ABSENT-and-portable | 3-slot form is ours; Mathlib wants the bipartite form |
| `vnEntropy` | ABSENT-but-**design-mismatch** | our `dite`-on-`IsHermitian` def is not idiomatic; see §4 |
| `vnEntropy_of_isHermitian` | n/a | disappears under the recommended def |
| `trace_eq_sum_eigenvalues_rclike` | **ALREADY UPSTREAM** | `Matrix.IsHermitian.trace_eq_sum_eigenvalues`, `Analysis/Matrix/Spectrum.lean:238` |
| `vnEntropy_le_log_card` (quantum Gibbs) | ABSENT-and-portable | blocked on finite entropy landing first |
| `diagEmbed`, `isHermitian_diagEmbed`, `isDensity_diagEmbed` | ABSENT-but-trivial | `Matrix.diagonal` + `posSemidef_diagonal_iff` (`LinearAlgebra/Matrix/PosDef.lean:71`) do the work |
| `smul_one_sub_diagonal`, `det_smul_one_sub`, `det_smul_one_sub_diagEmbed` | **SUPERSEDED** | replaced by `charpoly` + `charpoly_diagonal` |
| `eval_prod_linear`, `multiset_eq_of_prod_linear` | **SUPERSEDED** | replaced by `roots_charpoly_eq_eigenvalues` (`Spectrum.lean:159`) |
| `eigenvalues_diagEmbed_multiset` | **SUPERSEDED** | `charpoly_diagonal` + `eigenvalues_eq_eigenvalues_iff` |
| `sum_mul_log_multiset`, `entropy_congr_multiset` | ABSENT-but-trivial | ships with the finite-entropy file |
| `vnEntropy_diagEmbed` (diagonal bridge) | ABSENT-and-portable | the `S(diagonal p) = H(p)` bridge; keep, reprove via charpoly |
| `qShare`, `qPairEnvelope`, `QSamePairs`, parity computations | **DO NOT PORT** | repo-specific; this is our science, not Mathlib's |

### EntropyIneq.lean

| Our stone | Verdict | Master counterpart / note |
|---|---|---|
| `vnEntropy_congr_of_det` | **SUPERSEDED** | the charpoly route makes this unnecessary as a named lemma |
| `vnEntropy_conj_unitary` | ABSENT-statement, **SUPERSEDED proof** | `Matrix.charpoly_units_conj` (`Charpoly/Basic.lean:280`); a unitary is a unit |
| `vnEntropy_reindex` | ABSENT-statement, **SUPERSEDED proof** | `Matrix.charpoly_reindex` (`Charpoly/Basic.lean:168`) |
| `vnEntropy_transpose` | ABSENT-statement, **SUPERSEDED proof** | `Matrix.charpoly_transpose` (`Charpoly/Basic.lean:165`, `@[simp]`) |
| `mul_log_jensen` | **SUPERSEDED** | `Real.convexOn_mul_log` (`NegMulLog.lean:144`) + `ConvexOn.map_sum_le` (`Jensen.lean:67`). Our calculus-free Gibbs proof is a nice artifact but not upstreamable content. |
| `diagRe` | ABSENT-but-realign | should be `RCLike.re ∘ Matrix.diag ρ`; master has `IsHermitian.coe_re_diag` (`Analysis/Matrix/Hermitian.lean:39`) for the round trip |
| **`vnEntropy_le_entropy_diagRe` (pinching)** | **ABSENT — and the prize** | Schur–Horn's consequence. See §4 for why our route is the *right* one to upstream. |
| `entropy_grouping₂` (classical subadditivity) | ABSENT-and-portable | blocked on finite entropy |
| `ptrR`, `ptrL` + Hermitian/trace/PSD/density lemmas | ABSENT-and-portable | the natural bipartite partial-trace API |
| `kronecker_conjTranspose'` | **ALREADY UPSTREAM** | `Matrix.conjTranspose_kronecker` (`LinearAlgebra/Matrix/Kronecker.lean:408`) |
| `isDensity_conj_unitary`, `isProb_diagRe`, `conj_kron_entry`, `ptrR_conj_kronecker`, `ptrL_conj_kronecker` | ABSENT-and-portable | bookkeeping; ships with the partial-trace API |
| `diagRe_ptrR`, `diagRe_ptrL`, `diagRe_diagonal` | ABSENT-but-trivial | bookkeeping |
| **`vnEntropy_subadd` (quantum subadditivity)** | **ABSENT — headline** | nothing comparable in master |
| `vnEntropy_eq_of_padded` | ABSENT-and-portable | becomes cleaner: `roots (X^k * p) = replicate k 0 + roots p` |
| `vnEntropy_mul_conjTranspose_comm` | ABSENT-statement, **SUPERSEDED proof** | `Matrix.charpoly_mul_comm'` (`Charpoly/Basic.lean:238`) is *literally* the zero-padded rectangular identity we built by hand from `det_one_add_mul_comm` |
| `vnEntropy_ptr_complementary` | ABSENT-and-portable | pure-state complementarity |
| `posSemidef_vecMulVec_star` | **ALREADY UPSTREAM** | `Matrix.posSemidef_vecMulVec_self_star` (`LinearAlgebra/Matrix/PosDef.lean:412`) |
| `purifyVec`, `ptrR_purifyVec` | ABSENT-and-portable | purification of a density operator |
| **`vnEntropy_triangle` (Araki–Lieb)** | **ABSENT — the prize** | nothing comparable |
| `vnEntropy_kron_unif` | ABSENT-and-portable | `S(σ ⊗ 1/d) = S(σ) + log d` |
| `vnEntropy_causal_past` | **DO NOT PORT** | our application; belongs in our repo, not Mathlib |

Counting: 4 stones already upstream verbatim, 8 superseded in proof, ~22
absent-and-portable, 1 design-mismatch (`vnEntropy` itself), 4 do-not-port.

---

## 4. Design decisions to settle before writing any Lean

### 4a. Define `vnEntropy` through the CFC, not through `eigenvalues`

Our definition is
```
noncomputable def vnEntropy (ρ) : ℝ := if h : ρ.IsHermitian then entropy h.eigenvalues else 0
```
which bakes a `dite` and a junk convention into the definition, forces every
downstream statement to carry an `IsHermitian` hypothesis just to unfold, and
does not generalize past matrices. Mathlib will not take it in that shape.

The idiomatic definition, given what master now has, is
```
noncomputable def vnEntropy (ρ : Matrix n n 𝕜) : ℝ := RCLike.re (cfc Real.negMulLog ρ).trace
```
Why this one and not `-(ρ * CFC.log ρ).trace.re`:

- `Real.negMulLog` is **continuous everywhere** (`NegMulLog.lean:186`), so the
  `cfc` side condition discharges by `fun_prop` with no argument about the
  spectrum. The `CFC.log` route needs `Real.log` continuous on the spectrum,
  which for matrices is true only because the spectrum is finite — fine here
  (`HermitianFunctionalCalculus.lean:128-130` says so explicitly) but it does
  not survive generalization to infinite-dimensional algebras, and it makes the
  singular-density case an argument rather than a triviality.
- It is **total**: no `dite`, no `IsHermitian` in the signature. Non-Hermitian
  input gets `cfc`'s own junk value, which is Mathlib's existing convention
  rather than a new one we impose.
- The bridge to our formulation is short and uses only upstream lemmas:
  `Matrix.IsHermitian.cfc_eq` (`HermitianFunctionalCalculus.lean:143`) plus
  `Matrix.IsHermitian.charpoly_cfc_eq` (`:152`) plus
  `Matrix.IsHermitian.trace_eq_sum_eigenvalues` (`Spectrum.lean:238`) should
  give `vnEntropy ρ = ∑ i, Real.negMulLog (hρ.eigenvalues i)`. *(Unverified
  prediction — not built. This is the single step most likely to cost a day.)*
- It generalizes verbatim to a C⋆-algebra with a trace, which is the statement
  a Mathlib reviewer will eventually want.

**Recommendation:** define via `cfc Real.negMulLog`, immediately prove the
eigenvalue-sum bridge, and state every theorem in the ladder against the
bridge. Keep the eigenvalue form as the working lemma; keep the CFC form as
the definition.

### 4b. Prove pinching *without* majorization

Our `vnEntropy_le_entropy_diagRe` is Schur–Horn's corollary, but our proof does
not go through majorization at all: it observes that `D i j = ‖U i j‖²` has
nonnegative entries with unit row sums (from `U * star U = 1` alone), then
applies Jensen to `t log t` term-wise. That is a virtue, not an accident — see
Risks. The reusable, genuinely-new intermediate is

> **`Matrix.unitary_map_normSq_mem_doublyStochastic`** (name to be bikeshed):
> for `U ∈ Matrix.unitaryGroup n 𝕜`, the matrix `fun i j => ‖U i j‖ ^ 2` lies in
> `doublyStochastic ℝ n`.

This is a two-line consequence of `mem_unitaryGroup_iff` and
`mem_doublyStochastic_iff_sum` (`Analysis/Convex/DoublyStochasticMatrix.lean:56`),
it is absent from master, it is the missing half of the Schur–Horn theorem that
master's own docstring advertises, and it is useful to people who care nothing
about entropy. It is the best standalone PR in the whole ladder.

### 4c. The Mathlib-idiomatic Araki–Lieb over `m × n`

Master has no `TensorProduct` presentation of matrix algebras that we would
want here; the Kronecker/product-index presentation is the one in use
(`Matrix (m × n) (m × n) 𝕜`, `Matrix.kroneckerMap`, `Matrix.trace_kronecker`).
So the statement should be indexed exactly as ours is, with the partial traces
named as a Mathlib API rather than as ad-hoc `Matrix.of fun … => ∑ …`:

```
/-- **Araki–Lieb triangle inequality**. -/
theorem Matrix.vnEntropy_traceRight_le
    {m n : Type*} [Fintype m] [Fintype n] [DecidableEq m] [DecidableEq n]
    {ρ : Matrix (m × n) (m × n) 𝕜} (hρ : ρ.PosSemidef) (hρ1 : ρ.trace = 1) :
    vnEntropy ρ.traceRight ≤ vnEntropy ρ + vnEntropy ρ.traceLeft
```
with the density hypothesis spelled out as two arguments rather than bundled in
an `IsDensity` structure. Mathlib's taste runs against one-field-plus-one-field
predicate bundles that exist only to be destructured; `PosSemidef` is already
the standing idiom and `trace = 1` is one extra hypothesis. **Do not upstream
`IsDensity`.** (Ours stays in our repo; only the theorems change shape.)

Names for the partial traces: `Matrix.traceRight : Matrix (m × n) (m × n) R →
Matrix m m R` (trace *out* the right factor) and `Matrix.traceLeft`, matching
our `ptrR`/`ptrL` semantics. This is the one name I would raise on Zulip first,
because "traceLeft" could reasonably mean either "trace over the left factor"
or "the left factor that survives", and getting it backwards is the kind of
thing that costs a review cycle.

### 4d. Home files

| Content | Proposed home | Rationale |
|---|---|---|
| bipartite partial trace + API | `Mathlib/LinearAlgebra/Matrix/PartialTrace.lean` | purely algebraic (`∑` over a `Fintype`), no analysis import needed |
| unitary ⇒ doubly stochastic | `Mathlib/Analysis/Matrix/DoublyStochastic.lean` (new) | needs `RCLike` norms; imports `Analysis/Convex/DoublyStochasticMatrix` |
| finite Shannon entropy | `Mathlib/InformationTheory/Entropy/Basic.lean` (new) | parallels the existing `InformationTheory/KullbackLeibler/` and `InformationTheory/Coding/` subdirectory shape |
| von Neumann entropy + ladder | `Mathlib/Analysis/Matrix/Entropy.lean` (new) | sits next to `Analysis/Matrix/Spectrum.lean`, whose API it consumes; a reviewer may prefer `InformationTheory/VonNeumannEntropy.lean`, and that is a fine outcome |

### 4e. Finite entropy vs the measure-theoretic tradition

Master's information theory is measure-theoretic (`klDiv` between `Measure`s,
`Analysis/…/KullbackLeibler/`), authored by RemyDegenne, who is the natural
reviewer. There is a real risk a maintainer says "define entropy for measures,
then specialize" rather than accepting `∑ i, negMulLog (p i)` over a `Fintype`.

Arguments to have ready: `klDiv` does **not** subsume finite entropy (it is a
relative quantity between two measures, and the entropy is not `klDiv` against
counting measure without a sign and a finiteness argument); `Real.binEntropy`
already establishes that master accepts non-measure-theoretic entropy when the
setting is finite; and every theorem in this ladder is finite-dimensional, so a
measure-theoretic definition would be pure overhead at every use site. If the
maintainer insists anyway, the fallback is to define the finite version as an
abbreviation and prove the ladder against it — costly but not fatal.

**This question should be asked on Zulip before any code is written.** It is
the single largest scope risk in the plan.

---

## 5. Port plan — ordered PR sequence

Each stage is independently useful and independently reviewable; each depends
only on its predecessors. Sizes are rough line counts of *new* Mathlib content,
not of our existing files.

**PR-A — Bipartite partial trace.** `Matrix.traceLeft` / `Matrix.traceRight`,
plus: Hermitian-preservation, `trace_traceRight = trace`, PSD-preservation,
behaviour on `kroneckerMap`, and reindexing. ~150 lines. No entropy, no
analysis, no controversy. **Independent of everything else — this can go first
and can go in parallel with the det-monotonicity PR.**

**PR-B — Unitary ⇒ doubly stochastic.** The `‖U i j‖²` lemma of §4b, plus the
`Schur–Horn`-flavoured docstring pointing at
`Analysis/InnerProductSpace/Spectrum.lean:46`. ~40 lines. Also independent, also
uncontroversial, and it pays a debt master has already written down.

**PR-C — Finite Shannon entropy.** `∑ i, Real.negMulLog (p i)`, with: nonnegativity
on a distribution, the Gibbs bound `H(p) ≤ log |α|`, permutation/multiset
invariance, `H` of a point mass, and two-slot grouping subadditivity
(`entropy_grouping₂`). Proofs come from `Real.convexOn_mul_log` +
`ConvexOn.map_sum_le`, replacing our hand-rolled Gibbs arguments. ~200 lines.
**Gated on the Zulip answer in §4e.**

**PR-D — von Neumann entropy, definition and spectrum blindness.** The `cfc
Real.negMulLog` definition, the eigenvalue-sum bridge, `S(diagonal p) = H(p)`,
and invariance under unitary conjugation / reindexing / transpose — each a
corollary of an existing `charpoly` lemma. ~150 lines. Depends on PR-C.

**PR-E — Pinching.** `S(ρ) ≤ H(diag ρ)`. Depends on PR-B and PR-D. ~80 lines.
This is where the ladder starts being interesting to a physicist.

**PR-F — Quantum subadditivity.** `S(ρ) ≤ S(ρ.traceRight) + S(ρ.traceLeft)`, by
pinching in the product eigenbasis of the marginals. Depends on PR-A, PR-C
(grouping), PR-E. ~250 lines — the bulk of our `ptrR_conj_kronecker` /
`ptrL_conj_kronecker` bookkeeping lives here and does not get shorter upstream.

**PR-G — Complementary spectra and purification.** `S(M Mᴴ) = S(Mᴴ M)` via
`charpoly_mul_comm'`, plus `purify` and `S(traceRight ψψ*) = S(traceLeft ψψ*)`.
Depends on PR-D. ~150 lines, of which our zero-padding argument shrinks
substantially against the upstream identity.

**PR-H — Araki–Lieb.** `S(A) ≤ S(AB) + S(B)`. Depends on PR-F and PR-G.
~100 lines. This is the summit and the thing worth having our name on.

`vnEntropy_kron_unif` rides along in PR-D or PR-H. `vnEntropy_causal_past`
never goes up.

---

## 6. Risks

**R1 — Majorization lands underneath us and reframes pinching.** Two open PRs
compete to add majorization: **#33406** (dupuisf, "add basics of majorization",
opened 2025-12-30, 752 additions, labels `WIP` / `awaiting-author` /
`merge-conflict`, assigned to j-loreaux, last touched 2026-06-10 — stalled) and
**#41898** (marcinbugaj, "majorization preorder and T-transform decomposition",
opened 2026-07-18, 782 additions, mergeable-clean, `new-contributor`, updated
this morning — live). If either lands, a reviewer may ask for pinching to be
restated as "diag ρ ≺ eigenvalues ρ, and entropy is Schur-concave". *Mitigation:*
our proof does not use majorization, so PR-B and PR-E stand on their own either
way; the majorization framing becomes an easy follow-up corollary rather than a
rewrite. This is an argument for shipping PR-B early, while the ground is
unclaimed.

**R2 — The entropy-definition bikeshed (§4e).** Highest-variance item. Could add
weeks. Ask first, code second.

**R3 — The CFC bridge in §4a is an unverified prediction.** I did not build it.
If `charpoly_cfc_eq` + `trace_eq_sum_eigenvalues` do not compose as cleanly as
the statements suggest, PR-D grows. *Mitigation:* this is checkable in an hour
against a master checkout, and should be checked before promising PR-D.

**R4 — Our proofs are written against v4.14 and will not compile on master.**
Beyond the renames in `MASTER_FINDINGS.md`, this ladder adds one more:
`Mathlib.Data.Matrix.Kronecker` → **`Mathlib.LinearAlgebra.Matrix.Kronecker`**
(`Mathlib/Data/Matrix/Kronecker.lean` no longer exists). Our
`EntropyIneq.lean:33` imports the old path. `Mathlib.LinearAlgebra.Matrix.SchurComplement`
(our line 34) is unchanged.

**R5 — Volume.** Eight PRs is a large campaign for a first-time author in this
area. Mathlib reviewers are more willing when the first PR is small, clean, and
obviously useful. PR-A and PR-B are exactly that; PR-C onward is where review
bandwidth becomes the binding constraint.

**R6 — Sunk-cost pressure.** Roughly 400 of our 1419 lines are now redundant
against master. The temptation is to port them anyway because they work. Don't:
a PR that reintroduces `det(x•1 − A)` machinery alongside master's `charpoly`
API will be rejected, correctly.

---

## 7. Recommendation: after the det-monotonicity PR, not before

**Land `PR_det_monotonicity_MASTER.lean` first, alone, and wait for it to merge.**

The reasons are about us, not about the mathematics:

1. **We have never had a PR accepted into Mathlib.** The det-monotonicity PR is
   four lemmas, already master-verified, in an area (the Löwner order) master
   just built out and visibly cares about. It is the cheapest possible way to
   learn the review process, the naming expectations, and the new module-system
   style — before spending that learning budget on an eight-PR campaign.
2. **Nobody is racing us on the quantum side.** Zero PRs in mathlib4's entire
   history touch von Neumann entropy, Araki–Lieb, partial trace, or Schur–Horn.
   The cost of waiting a few weeks is close to zero. This is *not* true of
   majorization (R1), which is why PR-B is the exception below.
3. **The ladder needs a rewrite regardless.** Section 3 shows the bottom half of
   our development is superseded. That work has to happen whether we submit now
   or later, and it is easier to do once we have seen what a Mathlib reviewer
   actually asks for.

**The one exception:** PR-B (unitary ⇒ doubly stochastic, ~40 lines) is
independent of everything, is contested ground under R1, and pays a debt master
has already documented. If Eric wants a second small PR in flight alongside
det-monotonicity, that is the one — not Araki–Lieb.

**Concrete next actions, in order:**
1. Open the det-monotonicity PR (Eric's call, Eric's account — unchanged from
   `README.md`).
2. Post the §4e question on Zulip `#mathlib4` — "would a finite-`Fintype`
   Shannon entropy be welcome, or should it be measure-theoretic?" — and the
   §4c naming question. Both are free to ask and both gate real work.
3. Verify R3 (the CFC bridge) against a master checkout. One hour, and it
   de-risks the whole design.
4. Only then start PR-A / PR-B.

**What this survey does not claim:** that any of the proposed Lean compiles.
Nothing here was built. The absence claims are solid (exhaustive grep over
master's source, quoted); the presence claims are solid (file and line quoted);
the port plan is a plan, and its line counts are estimates.
