# The temporal whole-only share — definition pre-registration

**Date:** 2026-07-24. **Status:** written BEFORE any proof below was attempted, per
`epistemology.md` L1. This memo fixes the definition, the borrowed mathematics, and the
meaning of every possible formal outcome. The measurement phase (phase 3) is NOT
pre-registered here and must be pre-registered separately before any backend is touched.

## The object and the debt

The stance's open claim (`third-in-tsvf`) asks for the whole-only SHARE of a multi-time
state, defined on the object itself — the state over times / process tensor — not on
readings of it. The 2026-07-24 kill-check (three sweeps, disputed candidate read in full)
found no published pairwise-blind share for any multi-time quantum object.

**The mathematics is openly borrowed**, as with e/π. The construction is connected
information / max-entropy irreducible correlation: Schneidman, Still, Berry & Bialek
(2003) classically; Zhou (Phys. Rev. A 77, 022113, 2008) for the quantum max-ent form on
spatial states. What is ours is the *recognition*: applying it to the state-over-times,
where (per the kill-check) it has never been put, and mechanizing it.

## The definition (phase 1 — classical alphabets, this brick)

For a state `p` over three time slots with finite alphabets `A₁ × A₂ × A₃`:

- **pair envelope of p** := the set of entropies of all probability states `q` on
  `A₁ × A₂ × A₃` whose three two-slot marginals equal those of `p`.
- **share(p)** := sup(pair envelope of p) − entropy(p).

Instrument-free: a variational functional of the state alone. Natural-log units, matching
the repository's `entropy`. This covers every state-over-times with classical outcomes —
the diagonal sector of the three-slot process state.

**Phase 2 (quantum lift, next brick):** identical variational form on density operators —
von Neumann entropy via the eigenvalue distribution, two-slot marginals via partial trace
of the Choi/state-over-times object. Defined, then computed on an exhibited process. Not
in this brick.

> **Phase 2 outcome (2026-07-24, same day, `Core/ShareQuantum.lean`):** executed as
> staked. `vnEntropy` via the eigenvalue distribution, pair partial traces, `qShare` in
> the same variational form, over any RCLike field. Quantum Gibbs bound proved from the
> classical stone; the diagonal bridge (`vnEntropy_diagEmbed`) proved by pinning the
> eigenvalue multiset of a diagonal matrix (determinant of linear factors +
> `Polynomial.funext` + `roots_multiset_prod_X_sub_C`). Exhibited computation:
> `qShare (diagEmbed parity) = log 2 = share parity` — the supremum now ranges over
> every density carrying the parity pair data, coherent and entangled included, and none
> beats the diagonal maximizer. The share of the exhibited state survives the quantum
> lift unchanged. Still open: causal-ordering (process-tensor) constraint on the
> envelope; the share of any non-diagonal density; nature.

**Phase 3 (measurement):** process-tensor tomography of one natural process on quantum
hardware. Requires its own pre-registration (nulls for shot noise and readout error, kill
staked before counts are seen). Not in this brick.

## Pre-registered meanings of the formal outcomes (phase 1)

1. **Well-definedness.** The envelope contains `entropy p` (take `q = p`) and is bounded
   above by `log |A₁×A₂×A₃|` (the Gibbs bound). If either step is unprovable, the
   definition is ill-formed and is recorded as such — no repair is attempted in the same
   session that discovers the failure.
2. **share(parity) = log 2 — exactly one bit.** This is the advance prediction. The
   parity state's pair marginals are uniform, so the constrained max-ent problem must be
   solved by the unconstrained maximizer (uniform on 8), giving 3 log 2 − 2 log 2.
   - If the proof yields a DIFFERENT value: the "one bit" reading of the temporal Logos
     (`temporal-memory`, `temporal_logos_is_memory`) is mis-stated and the stance's
     temporal prose must be re-scoped before anything else proceeds.
   - If it yields log 2: the share, the memory cost (one bit,
     `memory_realizes_parity`), and the whole-reading (`third_sees_parity` = log 2) are
     one number by theorem, not analogy. That sentence may then be considered for the
     stance — with the refuter pass required before any page change.
3. **share ≥ 0** on every probability state. If unprovable, the definition is broken.
4. **share = 0 on a pairwise-determined state** (two copied bits × one free bit) — the
   discriminator separating the share from `S_total` (which is positive there). This
   requires grouping subadditivity of the bespoke entropy (Gibbs with absolute
   continuity, which holds automatically for a state against its own marginal product).
   Registered as the NEXT obligation: if it fails on attempt, the share does not isolate
   whole-only content and the definition is wrong — recorded, not patched.

## What this does and does not touch

Does: pays the "define + formalize + compute one example" of the open claim's promote
condition for the classical sector of the state-over-times. Does not: close the open
claim (the quantum lift and the measured natural process remain), change any claim
status, or touch the page. Stance updates are batched for review after the avenue closes.
