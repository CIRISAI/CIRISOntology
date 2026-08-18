# PRE-REGISTRATION — the cross-pair experiment: do independent Bell pairs leave receipts on each other?

Frozen before any circuit is submitted. This concretizes the stance's named-but-unnamed
instrument — "a quantum-sector wild measurement" — as the cheapest discriminating experiment
the lake can currently run. **Expected outcome: NULL.** Standard quantum mechanics predicts
exactly zero cross-pair correlation between independently prepared Bell pairs, and a null
with gauged sensitivity is the house product. The run is simultaneously an upper bound on
bulk-mediated-entanglement models and a crosstalk characterization the QPU programme needs
anyway.

## 1. The three sources this design draws from, and what each contributes

**The entropic-gravity import** (`precedent-is-bits`; cosmo_entropic_potential): the ledger
reading — capacity, writer, record — with the lake's own addition that the record must be
CLASSICAL because time's causal cap allows no quantum discount. Its qualitative prediction
here: **if two "independent" pairs share a mediating record, receipts appear across them.**
If they do not, the pairs are kinematically independent and the record — if any — is not
shared at this scale.

**The named loophole** (`Core/Temporal.lean` scope note, added with this prereg): every
temporal cap in the lake assumes a SINGLE causal order. arXiv:2606.12457 (Pettini,
speculative gen-ph, graded as such) proposes entanglement mediated by a bulk field in a
second time dimension, and stakes a falsifier: **cross-pair correlations between independent
Bell pairs scaling as the separation ratio squared.** We do not adopt the model; we adopt
the falsifier, because it is the rare concrete kill in this neighbourhood.

**The shadow license** (`coherence-ratchet/experiments/entanglement_ledger`): the classical
outcome-correlation instrument tracks the TRUE quantum corridor at Spearman +0.97 to +1.00
in the order-parameter basis and is blind in the conjugate basis. This licenses reading
cross-pair structure with classical correlators — PROVIDED both bases are measured, and the
basis-dependence itself is reported. One basis is not a measurement; it is half of one.

## 2. What we already have, checked (received-numbers discipline)

`scratchpad/pump_qpu.json`: 12 rows, single-pair damping sweeps — **no simultaneous
multi-pair data exists anywhere in the lake or its ancestors.** The array's 124
cap-compliance readings are a chaotic classical substrate. This measurement is genuinely
new, not a re-read.

## 3. Design

**Hardware**: IBM QPU, banked time. Screening per house memory: never select on
`backend.properties()`; measured P(0|1) screen (~6 s) first; qubits chosen on the screen.

**Circuits**: two Bell pairs (A on qubits a1–a2, B on b1–b2), prepared in the same circuit
with no gate connecting the pairs. Geometry sweep: pair separation d(A,B) on the coupling
map at ≥4 values, with intra-pair distance held fixed; both measurement bases (ZZ and XX per
pair), 4 basis combinations. Shots: ≥8192 per cell.

**The observable**: cross-pair correlators `E(A,B) = <(a1⊕a2)(b1⊕b2)>` per basis pair — the
correlation between pair A's parity and pair B's parity — plus the full 4-bit distribution
for the LP/share instruments.

**THE LOAD-BEARING CONTROL — the manufactured floor.** Real hardware has crosstalk, and
shared substrate MINTS cross-structure (the valve, in silicon). So the identical geometry
sweep runs with **unentangled control pairs** (|00⟩ and |++⟩ preparations, no CX): every
cross-pair correlator measured there is pipeline-plus-substrate, not physics. The Bell-pair
reading is reported ONLY as an excess over the matched control at the same qubits, same
session, interleaved scheduling (drift control).

## 4. Stakes and kills, separable

* **S1 (the QM null, primary).** Excess cross-pair correlation consistent with zero at
  every separation. OUTCOME: an upper bound `|E_excess| < ε(d)` per separation, published
  with the control floor on the same line. This is the expected result and it is the
  deliverable.
* **S2 (the adopted falsifier).** If any excess survives the control at >5σ with the
  dose–response discipline (shots-split halves agree; excess stable under qubit-set
  permutation), fit the separation dependence. The Pettini form predicts scaling with
  separation RATIO squared; hardware crosstalk falls with coupling-map DISTANCE
  (approximately exponentially). **The discriminant is the shape**, staked now: a
  power law in ratio that survives the exponential-in-distance alternative on AIC by ≥10
  is the only reading that counts as S2-shaped. Anything else is substrate.
* **K1 (instrument kill).** If the CONTROL pairs show excess structure that the
  interleaving cannot remove, the session is VOID for S2 purposes and reported as a
  crosstalk characterization only.
* **The ledger tie, stated honestly.** S1-null is CONSISTENT with `precedent-is-bits` (a
  classical record cannot carry quantum correlations, per the lake's own causal-cap
  clause) and lends it no support. S2-positive would CONTRADICT the record-is-classical
  clause and support a bulk-mediation reading — the composed wager would need surgery
  either way. No outcome here "confirms the ledger"; the asymmetry is stated so it cannot
  be oversold later.

## 5. Feasibility and order

Screen (~6 s) → controls + Bell sweep interleaved (est. ≤60 s QPU time at 4 separations ×
4 bases × 2 preparations × 8192 shots, batched) → analysis offline. Fits inside banked
time. Analysis instruments reused: the exact k≤4 solvers, LP pinning, floors matched to
sample size, null-shape-before-z.

## 6. What this does not do

It does not test (3,2) spacetime — a QPU's pairs share a chip, not a cosmology, and a
positive here would first be a solid-state finding. It does not touch `wild-share`'s
classical nulls. And it cannot promote anything: whatever happens, the result enters the
record as a bound or a characterization, and the stance moves only on review.
