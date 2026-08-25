# Quantum short-circuit comparison

**Status: diagnostic evidence, not a gate and not a SOTA claim.** Recorded
2026-08-24 at the exact seam `N=8, U=16, t=1, Ne=8, 2Sz=0`, open boundaries,
with declared `chi=32`. The live exact Door is q-seam:
`E0 = -1.262136132334283`.

The short circuit separates two questions that a single external package would
otherwise confound:

1. **Did q8 optimize the state?** Compare against an independent mature DMRG
   Habit (TeNPy 1.1.0).
2. **Does q8 report the state it actually returned?** Freeze that MPS and
   contract its claims through an independent Rust View (TNC 1.0.1/TBLIS), then
   compare with an explicit state-vector View and q-seam.

## Optimizer comparison

| Habit / start / mixer | absolute energy error | sweeps | wall | canonical residual | variance |
|---|---:|---:|---:|---:|---:|
| q8 / Neel | 8.594628e-7 | 7 | 11.432 s | left defect 2.020 | 1.993322e-5 |
| q8 / doublon-hole | 8.940115e-7 | 6 | 7.497 s | left defect 3.183 | 2.069877e-5 |
| TeNPy / Neel / none | 7.188013e-7 | 13 | 1.622 s | 4.780e-15 | 1.757996e-5 |
| TeNPy / Neel / subspace expansion | 7.192804e-7 | 11 | 1.436 s | 5.582e-16 | 1.755911e-5 |
| TeNPy / doublon-hole / none | 6.036984e-7 | 15 | 1.633 s | 7.644e-15 | 1.554602e-5 |
| TeNPy / doublon-hole / subspace expansion | 6.046537e-7 | 12 | 1.266 s | 2.526e-15 | 1.554810e-5 |

TeNPy is modestly closer to the exact Door in all four arms and returns a
canonical state to machine precision. Subspace expansion reduces the sweep
count in both starts, but its removal does not worsen final energy at this
point; this run therefore does **not** validate expansion as q8's remedy.

The wall column is descriptive, not a fair speed ranking. TeNPy uses one
four-state tensor per Hubbard site with particle-number and Sz symmetries; q8
uses two unconstrained two-state interleaved Jordan-Wigner orbitals. Their
declared `chi` values coincide only at physical-site cuts, and the implementations
do not perform identical work.

## Independent Rust claim View

For each q8 state, `tools/q-tnc-claim-view` performed 97 fixed-path TNC
contractions covering norm, Hubbard energy, the erased-JW-string mutant,
density, magnetization, and double occupancy.

| frozen q8 World | max TNC/direct defect | q8-report/TNC defect | erased-JW energy move | TNC View wall |
|---|---:|---:|---:|---:|
| Neel start | 1.221245e-14 | 1.174749e-11 | 2.487094 | 0.077 s |
| doublon-hole start | 1.487699e-14 | 3.419265e-12 | 2.487092 | 0.075 s |

This acquits the reporting boundary at this seam. The approximately `9e-7`
error belongs to the returned state, not to q8's energy label or MPO
observation. Both q8 starts reach nearly the same state energy (separation
`3.454873e-8`) while both retain local Lanczos residuals near `1e-3` and broken
left-canonical form. The next repair target is therefore q8's local solve and
canonical sweep, followed by the predeclared high-chi/two-start discriminator;
another output adapter cannot repair it.

## Evidence

- `tools/q-tnc-claim-view/receipts/n8-u16-chi32.log` — exact TNC stdout receipt.
- `output/q_sota/*.json` — four complete TeNPy ledgers, including model,
  representation, schedule, observables, diagnostics, and exact reference.
- `crates/q8-mps/examples/object_claim_transport.rs` — zero-external-dependency
  exact-seam localization View.
- `crates/q8-mps/tests/habit_conveyance.rs` — finite dynamic fiber witness across
  an admissible orthogonal MPS rechart.

## Repair unlocked by the comparison

The comparison's asymmetric diagnostic was causal: q8's accumulated right singular vectors were
orthogonal while its normalized left vectors were not. The Jacobi SVD had used an absolute Gram
off-norm as its convergence criterion; scale-separated Schmidt columns can satisfy that absolute
test while retaining large relative overlaps. The repair now tests normalized column correlation,
routes wide matrices through the transposed tall problem, and rejects SVD non-convergence.

On the same `N=8,U=16,chi=32` two-start probe, canonical defects fall from `2.020 / 3.183` to at
most `9.1e-14`; the direct returned-state View continues to match q8's label within `2.4e-12`.
The energy error remains `8.35e-7` to `8.59e-7` at this deliberately truncated ledger, which is the
same scale as the TeNPy arms rather than evidence of a reporting defect. Increasing only the
ledger to `chi=64` now converges in five monotone sweeps with absolute exact-door error
`1.27e-10`; `chi=256` reaches `7.61e-13`. The former high-chi regression was therefore a broken
canonical correspondence, not a need for another optimizer adapter or subspace-expansion remedy.

## OBJECT audit: claim transport is not Habit conveyance

The original short circuit used the maximal object unevenly. It used **World**
(the returned MPS), several genuinely independent **Views** (q8 report, direct
state vector, and TNC contraction), and the exact **Door** (q-seam) strongly.
It used **Habit** only by naming `dmrg::run_from` as the step. A named step is
not yet conveyance: `Core/Habit.lean::Closed` requires a named View `v` to
determine its successor, `v ∘ T = h ∘ v`.

`tests/habit_conveyance.rs` now supplies the first finite witness of that
dynamic condition. At `N=4,U=16,chi=16`, it takes two distinct canonical MPS
charts of exactly the same physical state, related by an orthogonal rotation
on an internal bond, and advances each by one full sweep. The raw chart move is
`3.62e-1`; the normalized physical-state View defect is `5.55e-17` before the
sweep and `6.66e-16` after it. The test therefore visits one nontrivial fiber
and observes one common successor View.

This remains deliberately narrower than a theorem: it does not prove
`Closed` over every admissible MPS chart, and it says nothing about the noisy
half of Habit. The canonicality regression is the companion admissibility
gate. A non-orthogonal chart can represent the same physical state while
changing the block overlap metric; q8's ordinary local eigensolver is warranted
only when that metric is the identity. The Q8 failure was exactly this split:
frozen-state claims transported correctly, while the next optimization step
was computed in a broken chart. The repair restores the chart witness; the new
test checks that one admissible change of chart does not change the induced
physical successor.
