# PHYS-K11-1 PREREG (FROZEN 2026-08-23, before any run) — the K11 confrontation battery

Runs S1–S4 + S6-slice of the cheap high-sigma programme (MAXIMAL_OBJECT.md §7),
under the alignment protocol §8. Spend order enforced: exact tiers license the
pipeline before any discovery number is read. S7 (MC) runs ONLY if S3 finds
response and only in a follow-up with its own frozen targets.

## U1 DECISION (frozen): the couplings
c_ij = symmetrized sealed anchor: (M_ij + M_ji)/2 from the CUR-P2 row-stochastic
confusion matrix (atlas defs), zero diagonal. NORMALIZATION (A2): c ← c / mean of
its 110 off-diagonal entries — the time unit is the mean channel strength.
Replicate arm: CUR-SP same construction (reported alongside, not primary).

## Constructions
- H(c, A) on K11; gauge: star spanning tree at node 0 (Priorities), 45 chords
  (i,j), 1≤i<j≤10; chord flux Φ_ij = the (0,i,j) triangle's Wilson phase.
- Dynamics for transport: dephasing Lindblad dρ/dt = −i[H,ρ] + γ Σ_i(P_iρP_i − ρ),
  site dephasing. ν-analogue := spectral gap of the Liouvillian (121×121).
  Dephased comparator (A1/Sornette): γ→large limit — classical, flux-blind.
- σ-projected control coupling c̄ := automorphism-group average of c (exact twin
  symmetry restored).

## S1 — twin dark states (exact tier + one staked sign)
THEOREM-BACKED (derived in this prereg, before running): if c is σ-invariant for
twin (a,b), then (|a⟩−|b⟩)/√2 is an EXACT eigenvector of H(c̄, A=0) with eigenvalue
−c̄_ab, decoupled from the rest of the graph.
- S1a (exact, pipeline license): on c̄, both twin dark states reproduce eigenvalue
  −c̄_ab and leakage 0 at machine floor (report decades below 1e-12).
- S1b (STAKED SIGN on real c): leakage L(pair) := 1 − max_v |⟨ψ_dark|v⟩|² obeys
  L(Structure/Circumstances) > L(Priorities/Process) — the measured lifting order
  δ₂ > δ₁ carried into spectra. PASS/FAIL, one bit, staked now.

## S2 — K11 return evenness (exact tier)
With a full random gauge field A (all 45 chords, seed 20260823), verify
|U(A)_ii| = |U(−A)_ii| for all i at machine floor (the H(−A) = H(A)ᵀ theorem,
RouteSymmetry generalized). Any excess is pipeline error; license gate.

## S3 — the 45-loop flux-response map (discovery, expectations staked)
ν(Φ_l) per chord l, 12-point grid Φ ∈ [0, 2π), γ ∈ {0.1, 0.5, 2.0} (in A2 units),
all other fluxes 0.
- STAKED: (i) ν even in each Φ_l (transpose symmetry survives site dephasing);
  (ii) response → 0 in the dephased comparator (flux-blindness of the classical
  limit) — the Sornette gate for anything S3 finds.
- DISCOVERY (no stake, mapped): which loops respond, at what magnitude, and
  whether response concentrates on loops through particular kinds. The
  Record-sector conjecture would LIKE concentration; the map decides. Look-elsewhere:
  45 loops — any single-loop claim from this map is exploratory until re-staked.
- REPORTING FLOOR: |Δν|/ν(0) < 1e-6 counts as null for that loop.

## S4 — ε-sweep spectral precursor (diagnostic staked, answer free)
H from pure depth family c_ij = ε^{|d_i−d_j|} (DepthCharge.lean's family, pinned
d), ε ∈ logspace(0.05, 5, 41). Diagnostic staked: mean eigenvector IPR and its
derivative vs ln ε; the question is crossover sharpness near ε = 1. No band
staked — this gates U9 spending, nothing else.

## S6-slice — two-excitation interference (exploratory instrument test)
Hard-core pair sector (dim 55) under H(c, single chord flux at the S3-loudest
loop): pair-transfer probabilities' flux dependence, even-harmonic check only.

## Meanings
S1a/S2 fail → pipeline defect: fix and rerun (not a physics result). S1b fail →
the spectral carrier of the twin lifting is NOT the dark-state leakage — the
aspect reading loses its first dynamical support; report plainly. S3 all-null at
every γ → the K11 semantic graph does not transport holonomy at single-particle
level — a real bound on the object (and S7 is NOT bought). S3 response passing
its two staked gates → first flux-sensitive transport on a measured semantic
graph; goes to the ledger as CANDIDATE pending the corpus side (BS-2/3 unchanged).
