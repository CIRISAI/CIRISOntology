/-
Audit/AxiomAudit.lean — the load-bearing verification gate.

Run in CI as `lake env lean Audit/AxiomAudit.lean`. This file's ELABORATION is
the gate: anything that fails below is a build error, not a warning.

WHY THIS FILE EXISTS RATHER THAN A GREP. Three weaker gates are commonly used
and each is defeatable:

  * a textual search for the admitted-gap keyword flags prose that merely
    *mentions* it (this repository's own documentation trips such a check) and
    misses gaps introduced by a tactic rather than by the literal keyword;
  * `lake build --wfail` relies on Lean's own "declaration uses 'sorry'"
    warning, which `#guard_msgs` swallows;
  * neither sees a gap inherited transitively from an imported declaration.

Asking the proof assistant what a theorem actually depends on is the check that
cannot be talked around. It is the same principle as the rest of our method:
**check the artifact, not the text describing the artifact.**
-/
import CIRISOntology

open Lean Elab Command

/-- Fail if `n` transitively depends on the admitted-gap axiom. Mathlib ships
    the same eight lines as `assert_no_sorry`; inlined here so the gate has no
    dependency that could be relaxed elsewhere. -/
elab "assert_no_sorry " n:ident : command => do
  let name ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo n
  let axs ← liftCoreM <| collectAxioms name
  if axs.contains ``sorryAx then
    throwError "AUDIT FAILURE: {n} transitively depends on sorryAx"

/-- Fail if `n` depends on any axiom outside the standard three. Catches
    `Lean.ofReduceBool` / `native_decide` creep, which a sorry-only check
    cannot see. -/
elab "assert_standard_axioms " n:ident : command => do
  let name ← liftCoreM <| realizeGlobalConstNoOverloadWithInfo n
  let axs ← liftCoreM <| collectAxioms name
  for a in axs do
    unless a == ``propext || a == ``Classical.choice || a == ``Quot.sound do
      throwError "AUDIT FAILURE: {n} depends on non-standard axiom {a}"

section Gate

open CIRISOntology CIRISOntology.Core

-- (1) No published theorem carries an admitted gap.
assert_no_sorry CIRISOntology.Core.S_pairwise_identity
assert_no_sorry CIRISOntology.Core.not_computable_from
assert_no_sorry CIRISOntology.Core.provenance_line
assert_no_sorry CIRISOntology.Core.parity_corr_eq_one
assert_no_sorry CIRISOntology.Core.pairwise_blind_to_parity
assert_no_sorry CIRISOntology.Core.third_sees_parity
assert_no_sorry CIRISOntology.Core.third_reading_positive
assert_no_sorry CIRISOntology.Core.parity_pair_independent_12
assert_no_sorry CIRISOntology.Core.parity_pair_independent_13
assert_no_sorry CIRISOntology.Core.parity_pair_independent_23
assert_no_sorry CIRISOntology.Core.indep_corr_eq_one
assert_no_sorry CIRISOntology.Core.S_total_indep
assert_no_sorry CIRISOntology.Core.corr_separates_total
assert_no_sorry CIRISOntology.Core.total_not_computable_from_corr
-- Core.Temporal — temporal parity needs memory; one remembered bit suffices.
assert_no_sorry CIRISOntology.Core.parity_needs_memory
assert_no_sorry CIRISOntology.Core.memory_realizes_parity
assert_no_sorry CIRISOntology.Core.memory_realizer_is_probability
assert_no_sorry CIRISOntology.Core.temporal_logos_is_memory
-- Core.Share — the whole-only share, defined on the state itself.
assert_no_sorry CIRISOntology.Core.entropy_le_log_card
assert_no_sorry CIRISOntology.Core.entropy_nonneg
assert_no_sorry CIRISOntology.Core.pairEnvelope_bddAbove
assert_no_sorry CIRISOntology.Core.share_nonneg
assert_no_sorry CIRISOntology.Core.share_parity
assert_no_sorry CIRISOntology.Core.share_parity_positive
assert_no_sorry CIRISOntology.Core.entropy_grouping
assert_no_sorry CIRISOntology.Core.share_copied
assert_no_sorry CIRISOntology.Core.S_total_copied
assert_no_sorry CIRISOntology.Core.S_total_copied_positive
-- Core.ShareQuantum — the whole-only share lifted to density operators.
assert_no_sorry CIRISOntology.Core.trace_eq_sum_eigenvalues_rclike
assert_no_sorry CIRISOntology.Core.vnEntropy_le_log_card
assert_no_sorry CIRISOntology.Core.vnEntropy_nonneg
assert_no_sorry CIRISOntology.Core.qPairEnvelope_bddAbove
assert_no_sorry CIRISOntology.Core.qShare_nonneg
assert_no_sorry CIRISOntology.Core.isDensity_diagEmbed
assert_no_sorry CIRISOntology.Core.vnEntropy_diagEmbed
assert_no_sorry CIRISOntology.Core.ptr₁₂_diagEmbed
assert_no_sorry CIRISOntology.Core.qShare_parity
assert_no_sorry CIRISOntology.Core.qShare_eq_share_parity
-- Core.ShareK — the k-slot share and the classical cap (the Bell bound).
assert_no_sorry CIRISOntology.Core.entropy_map_le
assert_no_sorry CIRISOntology.Core.shareK_le_log_sub_pair
assert_no_sorry CIRISOntology.Core.shareK_le_of_pair_uniform
assert_no_sorry CIRISOntology.Core.pushforward_pair_parity
assert_no_sorry CIRISOntology.Core.share_le_log_sub_pair₃
assert_no_sorry CIRISOntology.Core.temporal_third_saturates
assert_no_sorry CIRISOntology.Core.qPairEnvelopeK_bddAbove
assert_no_sorry CIRISOntology.Core.qShareK_nonneg
assert_no_sorry CIRISOntology.Core.qShareK_le_log_card
-- Core.EntropyIneq — the Araki-Lieb ladder and the causal past-view bound.
assert_no_sorry CIRISOntology.Core.mul_log_jensen
assert_no_sorry CIRISOntology.Core.vnEntropy_conj_unitary
assert_no_sorry CIRISOntology.Core.vnEntropy_le_entropy_diagRe
assert_no_sorry CIRISOntology.Core.entropy_grouping₂
assert_no_sorry CIRISOntology.Core.vnEntropy_subadd
assert_no_sorry CIRISOntology.Core.vnEntropy_ptr_complementary
assert_no_sorry CIRISOntology.Core.vnEntropy_triangle
assert_no_sorry CIRISOntology.Core.vnEntropy_causal_past
-- Core.BellCeiling — the ideal quantum ceiling: qShareK(C5) = 5 log 2.
assert_no_sorry CIRISOntology.Core.isDensity_PsiC5
assert_no_sorry CIRISOntology.Core.vnEntropy_PsiC5
assert_no_sorry CIRISOntology.Core.pairPtr_PsiC5
assert_no_sorry CIRISOntology.Core.bell_ceiling
assert_no_sorry CIRISOntology.Core.bell_ceiling_exceeds_cap
assert_no_sorry CIRISOntology.Core.qShareK_max_five
-- Core.HammingCap — the tightened classical cap: (k-3) log 2 for k >= 4.
assert_no_sorry CIRISOntology.Core.kern_eq
assert_no_sorry CIRISOntology.Core.kern_real
assert_no_sorry CIRISOntology.Core.inversion
assert_no_sorry CIRISOntology.Core.sum_sq_le_eighth
assert_no_sorry CIRISOntology.Core.entropy_ge_three_log_two
assert_no_sorry CIRISOntology.Core.shareK_le_of_pair_uniform_four
assert_no_sorry CIRISOntology.Core.shareK_le_of_pair_uniform_ge_four
assert_no_sorry CIRISOntology.Core.shareK_le_of_four_pair_uniform
assert_no_sorry CIRISOntology.Core.entropy_ge_of_sum_sq_le
assert_no_sorry CIRISOntology.Core.rent_holds
assert_no_sorry CIRISOntology.Core.paid_const
assert_no_sorry CIRISOntology.Core.underpaid_shrinks
assert_no_sorry CIRISOntology.Core.unpaid_succ
assert_no_sorry CIRISOntology.Core.unpaid_decays
-- Core.SignSymmetry — global sign symmetry forces the whole-only share to zero.
assert_no_sorry CIRISOntology.Core.sum_comp_signFlip
assert_no_sorry CIRISOntology.Core.symmetrize_signSymmetric
assert_no_sorry CIRISOntology.Core.symmetrize_isProb
assert_no_sorry CIRISOntology.Core.entropy_le_symmetrize
assert_no_sorry CIRISOntology.Core.samePairs_symmetrize
assert_no_sorry CIRISOntology.Core.eq_of_signSymmetric_of_samePairs
assert_no_sorry CIRISOntology.Core.share_eq_zero_of_signSymmetric
assert_no_sorry CIRISOntology.Core.share_indep
assert_no_sorry CIRISOntology.Core.ferro_isProb
assert_no_sorry CIRISOntology.Core.ferro_signSymmetric
assert_no_sorry CIRISOntology.Core.share_ferro
assert_no_sorry CIRISOntology.Core.S_total_ferro
assert_no_sorry CIRISOntology.Core.parity_not_signSymmetric
-- Core.Creation — MAINTENANCE IS CREATION: one application of a code's repair
-- map to pure noise mints that code's whole-only share exactly, and the
-- sign-symmetry lemma governs which repairs can mint. The no-creation half is
-- general in the input state: a map that reads no cell but its own can never
-- raise the share.
assert_no_sorry CIRISOntology.Core.parityRepair_idempotent
assert_no_sorry CIRISOntology.Core.parityRepair_fixed_iff
assert_no_sorry CIRISOntology.Core.majority_eq
assert_no_sorry CIRISOntology.Core.majorityRepair_idempotent
assert_no_sorry CIRISOntology.Core.majorityRepair_fixed_iff
assert_no_sorry CIRISOntology.Core.pushforward_equiv
assert_no_sorry CIRISOntology.Core.pushforward_parityRepair_indep
assert_no_sorry CIRISOntology.Core.repair_creates_parity
assert_no_sorry CIRISOntology.Core.repair_mints_from_noise
assert_no_sorry CIRISOntology.Core.S_total_parityRepair
assert_no_sorry CIRISOntology.Core.parityRepair_pays_one_bit
assert_no_sorry CIRISOntology.Core.pushforward_majorityRepair_indep
assert_no_sorry CIRISOntology.Core.repair_creates_ferro
assert_no_sorry CIRISOntology.Core.S_total_majorityRepair
assert_no_sorry CIRISOntology.Core.majorityRepair_pays_two_bits
assert_no_sorry CIRISOntology.Core.parityRepair_not_percell
assert_no_sorry CIRISOntology.Core.majorityRepair_not_percell
assert_no_sorry CIRISOntology.Core.entropy_reindex
assert_no_sorry CIRISOntology.Core.entropy_reidx
assert_no_sorry CIRISOntology.Core.isProb_reidx
assert_no_sorry CIRISOntology.Core.samePairs_reidx
assert_no_sorry CIRISOntology.Core.pairEnvelope_reidx
assert_no_sorry CIRISOntology.Core.share_reidx
assert_no_sorry CIRISOntology.Core.bool_bijective_of_ne
assert_no_sorry CIRISOntology.Core.bool_const_of_eq
assert_no_sorry CIRISOntology.Core.share_pushforward_percell_of_bijective
assert_no_sorry CIRISOntology.Core.entropy_grouping₂₃
assert_no_sorry CIRISOntology.Core.entropy_grouping₁₃
assert_no_sorry CIRISOntology.Core.marg₁_of_samePairs
assert_no_sorry CIRISOntology.Core.marg₂_of_samePairs
assert_no_sorry CIRISOntology.Core.marg₃_of_samePairs
assert_no_sorry CIRISOntology.Core.entropy_point_mass
assert_no_sorry CIRISOntology.Core.share_eq_zero_of_entropy_maximal
assert_no_sorry CIRISOntology.Core.share_eq_zero_of_third_det
assert_no_sorry CIRISOntology.Core.share_eq_zero_of_first_det
assert_no_sorry CIRISOntology.Core.share_eq_zero_of_second_det
assert_no_sorry CIRISOntology.Core.share_pushforward_percell_of_const₁
assert_no_sorry CIRISOntology.Core.share_pushforward_percell_of_const₂
assert_no_sorry CIRISOntology.Core.share_pushforward_percell_of_const₃
assert_no_sorry CIRISOntology.Core.percell_no_creation
-- Core.Valve — THE ONE-WAY VALVE: under per-cell STOCHASTIC channels, order
-- flows UP the hierarchy (valve_upward — pure pair order mints strictly
-- positive whole-only share, which no DETERMINISTIC per-cell map can do),
-- never DOWN (valve_no_downward — the parity habit's decay never deposits
-- pairwise correlation, under any three kernels), and never FROM NOTHING
-- (valve_from_nothing — a product state in, whole-only share exactly zero out).
assert_no_sorry CIRISOntology.Core.push1_isProb
assert_no_sorry CIRISOntology.Core.channel3_isProb
assert_no_sorry CIRISOntology.Core.channel3_prod3
assert_no_sorry CIRISOntology.Core.isProb_prod2
assert_no_sorry CIRISOntology.Core.prod3_isProb
assert_no_sorry CIRISOntology.Core.entropy_prod2
assert_no_sorry CIRISOntology.Core.entropy_prod3
assert_no_sorry CIRISOntology.Core.marg₁₂_prod3
assert_no_sorry CIRISOntology.Core.marg₃_prod3
assert_no_sorry CIRISOntology.Core.share_prod3
assert_no_sorry CIRISOntology.Core.valve_from_nothing
assert_no_sorry CIRISOntology.Core.unifBool_isProb
assert_no_sorry CIRISOntology.Core.indep_eq_prod3
assert_no_sorry CIRISOntology.Core.valve_from_nothing_indep
assert_no_sorry CIRISOntology.Core.marg₁₂_channel3
assert_no_sorry CIRISOntology.Core.marg₁₃_channel3
assert_no_sorry CIRISOntology.Core.marg₂₃_channel3
assert_no_sorry CIRISOntology.Core.marg₁₂_channel3_of_prod
assert_no_sorry CIRISOntology.Core.marg₁₃_channel3_of_prod
assert_no_sorry CIRISOntology.Core.marg₂₃_channel3_of_prod
assert_no_sorry CIRISOntology.Core.marg₁_channel3
assert_no_sorry CIRISOntology.Core.marg₂_channel3
assert_no_sorry CIRISOntology.Core.marg₃_channel3
assert_no_sorry CIRISOntology.Core.marg₁₂_parity
assert_no_sorry CIRISOntology.Core.marg₁₃_parity
assert_no_sorry CIRISOntology.Core.marg₂₃_parity
assert_no_sorry CIRISOntology.Core.marg₁_parity
assert_no_sorry CIRISOntology.Core.marg₂_parity
assert_no_sorry CIRISOntology.Core.marg₃_parity
assert_no_sorry CIRISOntology.Core.valve_no_downward_12
assert_no_sorry CIRISOntology.Core.valve_no_downward_13
assert_no_sorry CIRISOntology.Core.valve_no_downward_23
assert_no_sorry CIRISOntology.Core.valve_no_downward
assert_no_sorry CIRISOntology.Core.damp_isKernel
assert_no_sorry CIRISOntology.Core.channel3_damp_ferro
assert_no_sorry CIRISOntology.Core.bulge_isProb
assert_no_sorry CIRISOntology.Core.bulgeWitness_isProb
assert_no_sorry CIRISOntology.Core.bulgeWitness_samePairs
assert_no_sorry CIRISOntology.Core.entropy_bulge
assert_no_sorry CIRISOntology.Core.entropy_bulgeWitness
assert_no_sorry CIRISOntology.Core.entropy_bulge_lt_bulgeWitness
assert_no_sorry CIRISOntology.Core.valve_upward
assert_no_sorry CIRISOntology.Core.valve_upward_bound
assert_no_sorry CIRISOntology.Core.valve_upward_strict
assert_no_sorry CIRISOntology.Core.stochastic_percell_can_create
-- Core.Valve, the pump: the odd sector is fed only by asymmetry. A flip-
-- covariant kernel (the binary symmetric channel) commutes with the global
-- sign flip, so it mints exactly zero from any sign-symmetric state; the
-- upward flow REQUIRES a channel that breaks the flip symmetry, and damping
-- does (damp_not_flipCovariant).
assert_no_sorry CIRISOntology.Core.isFlipCovariant_of_symm
assert_no_sorry CIRISOntology.Core.signSymmetric_channel3
assert_no_sorry CIRISOntology.Core.valve_needs_asymmetry
assert_no_sorry CIRISOntology.Core.valve_needs_asymmetry_ferro
assert_no_sorry CIRISOntology.Core.damp_not_flipCovariant
-- Core.ThirdCap — THE DENOMINATOR: three binary slots carry at most one bit of
-- whole-only share, with NO hypothesis on the pair marginals. With share_parity
-- (attainment) this makes log 2 the EXACT maximum, so the ceiling fraction
-- every campaign reports now divides by a proved number rather than an argued
-- one. The sharp form (share_le_pair_third_gap, and all three orientations in
-- share_le_grouping_gaps) is data-computable and can be far tighter.
assert_no_sorry CIRISOntology.Core.entropy_marg₁₂_le
assert_no_sorry CIRISOntology.Core.marg₃_eq_of_samePairs
assert_no_sorry CIRISOntology.Core.marg₃_isProb
assert_no_sorry CIRISOntology.Core.share_le_pair_third_gap
assert_no_sorry CIRISOntology.Core.share_le_log_card_third
assert_no_sorry CIRISOntology.Core.share_le_log_two
assert_no_sorry CIRISOntology.Core.share_max_eq_log_two
assert_no_sorry CIRISOntology.Core.share_le_grouping_gaps
-- Core.Entropy — the entropic-contraction spine.
assert_no_sorry CIRISOntology.Core.trace_eq_sum_eigenvalues
assert_no_sorry CIRISOntology.Core.neg_log_det_nonneg
assert_no_sorry CIRISOntology.Core.S_pairwise_nonneg
assert_no_sorry CIRISOntology.Core.neg_log_det_eq_zero_iff
assert_no_sorry CIRISOntology.Core.hadamard_posSemidef
assert_no_sorry CIRISOntology.Core.IsUnitDiag.hadamard
assert_no_sorry CIRISOntology.Core.oppenheim_two
assert_no_sorry CIRISOntology.Core.S_pairwise_hadamard_le_two
assert_no_sorry CIRISOntology.Core.neg_log_det_hadamard_nonneg
assert_no_sorry CIRISOntology.Core.one_le_det_one_add_posSemidef
assert_no_sorry CIRISOntology.Core.det_le_det_add_of_posDef_posSemidef
assert_no_sorry CIRISOntology.Core.posSemidef_det_nonneg
assert_no_sorry CIRISOntology.Core.posDef_of_posSemidef_det_pos
assert_no_sorry CIRISOntology.Core.det_le_det_add_of_posSemidef
assert_no_sorry CIRISOntology.Core.hadamard_fromBlocks
assert_no_sorry CIRISOntology.Core.hadamard_vecMulVec
assert_no_sorry CIRISOntology.Core.submatrix_hadamard
assert_no_sorry CIRISOntology.Core.posSemidef_vecMulVec
assert_no_sorry CIRISOntology.Core.schur_hadamard_identity
assert_no_sorry CIRISOntology.Core.schur_oneScalar
assert_no_sorry CIRISOntology.Core.posDef_diag_pos
assert_no_sorry CIRISOntology.Core.det_schur_reduce
assert_no_sorry CIRISOntology.Core.posSemidef_smul
assert_no_sorry CIRISOntology.Core.isHermitian_hadamard
assert_no_sorry CIRISOntology.Core.posDef_fin_one
assert_no_sorry CIRISOntology.Core.schur_posSemidef
assert_no_sorry CIRISOntology.Core.oppenheim_det
assert_no_sorry CIRISOntology.Core.S_pairwise_hadamard_le
-- Core.OppenheimRCLike — the complex-general (RCLike) Oppenheim spine.
assert_no_sorry CIRISOntology.Core.Herm.posSemidef_vecMulVec
assert_no_sorry CIRISOntology.Core.Herm.hadamard_vecMulVec
assert_no_sorry CIRISOntology.Core.Herm.schur_hadamard_identity
assert_no_sorry CIRISOntology.Core.Herm.schur_oneScalar
assert_no_sorry CIRISOntology.Core.Herm.posDef_diag_pos
assert_no_sorry CIRISOntology.Core.Herm.posDef_fin_one
assert_no_sorry CIRISOntology.Core.Herm.isHermitian_hadamard
assert_no_sorry CIRISOntology.Core.Herm.posSemidef_smul
assert_no_sorry CIRISOntology.Core.Herm.submatrix_hadamard
assert_no_sorry CIRISOntology.Core.Herm.hadamard_fromBlocks
assert_no_sorry CIRISOntology.Core.Herm.posSemidef_det_nonneg
assert_no_sorry CIRISOntology.Core.Herm.posDef_of_posSemidef_isUnit_det
assert_no_sorry CIRISOntology.Core.Herm.one_le_det_one_add_posSemidef
assert_no_sorry CIRISOntology.Core.Herm.det_le_det_add_of_posDef_posSemidef
assert_no_sorry CIRISOntology.Core.Herm.det_le_det_add_of_posSemidef
assert_no_sorry CIRISOntology.Core.Herm.hadamard_posSemidef
assert_no_sorry CIRISOntology.Core.Herm.det_schur_reduce
assert_no_sorry CIRISOntology.Core.Herm.schur_posSemidef
assert_no_sorry CIRISOntology.Core.Herm.oppenheim_det
assert_no_sorry CIRISOntology.Core.Herm.posSemidef_diag_nonneg
assert_no_sorry CIRISOntology.Core.Herm.eq_ofReal_re_of_nonneg
assert_no_sorry CIRISOntology.Core.Herm.diag_conj_entry
assert_no_sorry CIRISOntology.Core.Herm.oppenheim_prod
-- Core.Flavor — the Jarlskog CP-violation cap (cp-cap).
assert_no_sorry CIRISOntology.Core.jarlskogMax_nonneg
assert_no_sorry CIRISOntology.Core.abs_jarlskog_le_max
assert_no_sorry CIRISOntology.Core.jarlskogMax_zero_at_no_mixing
assert_no_sorry CIRISOntology.Core.jarlskogMax_zero_at_max_13mixing
-- Core.FlavorBridge — the flavour bridge: the Jarlskog coordinate IS the share.
assert_no_sorry CIRISOntology.Core.parityChar_signFlip
assert_no_sorry CIRISOntology.Core.cpState_isProb
assert_no_sorry CIRISOntology.Core.cpState_zero
assert_no_sorry CIRISOntology.Core.cpState_neg_eq_signFlip
assert_no_sorry CIRISOntology.Core.symmetrize_cpState
assert_no_sorry CIRISOntology.Core.cpState_signSymmetric_iff
assert_no_sorry CIRISOntology.Core.cp_phase_invisible_to_pairs
assert_no_sorry CIRISOntology.Core.cpState_corr_eq_one
assert_no_sorry CIRISOntology.Core.cpShare_neg
assert_no_sorry CIRISOntology.Core.cpShare_zero
assert_no_sorry CIRISOntology.Core.entropy_cpState
assert_no_sorry CIRISOntology.Core.share_cpState
assert_no_sorry CIRISOntology.Core.cpShare_nonneg
assert_no_sorry CIRISOntology.Core.cpShare_pos
assert_no_sorry CIRISOntology.Core.share_zero_of_cp_even
assert_no_sorry CIRISOntology.Core.share_pos_of_cp_odd
assert_no_sorry CIRISOntology.Core.share_cpState_eq_zero_iff
assert_no_sorry CIRISOntology.Core.share_symmetrize_cpState
assert_no_sorry CIRISOntology.Core.mul_log_convex
assert_no_sorry CIRISOntology.Core.entropy_concave
assert_no_sorry CIRISOntology.Core.cpState_mix
assert_no_sorry CIRISOntology.Core.cpShare_mul_le
assert_no_sorry CIRISOntology.Core.abs_jarlskog_le_one
assert_no_sorry CIRISOntology.Core.abs_jarlskogMax_le_one
assert_no_sorry CIRISOntology.Core.share_cpFamily_le_phase
assert_no_sorry CIRISOntology.Core.share_cpFamily_le_jarlskogMax
assert_no_sorry CIRISOntology.Core.share_cpFamily_zero_of_cp_even
assert_no_sorry CIRISOntology.Core.cpFamily_signSymmetric_of_cp_even
assert_no_sorry CIRISOntology.Core.share_cpFamily_zero_at_no_mixing
assert_no_sorry CIRISOntology.Core.share_cpFamily_zero_at_max_13mixing
assert_no_sorry CIRISOntology.Core.share_cpFamily_pos
assert_no_sorry CIRISOntology.Core.share_cpFamily_eq_zero_iff
assert_no_sorry CIRISOntology.Core.cpShare_one
assert_no_sorry CIRISOntology.Core.share_cpState_one
assert_no_sorry CIRISOntology.Core.cpState_neg_one
assert_no_sorry CIRISOntology.Core.share_parity_eq_cpShare
-- Core.Intensive — the intensive (per-unit) limit.
assert_no_sorry CIRISOntology.Core.Sfun_div_k_tendsto
-- Core.Third — relabeling-invariance of the total-dependence instrument.
assert_no_sorry CIRISOntology.Core.S_total_relabel_fst

-- COVERAGE COMPLETION, 2026-08-19. The two lists in this file are maintained by
-- hand, and had fallen behind the library: six modules added since the lists
-- were written (WrongKind, Generator, Instrument, Confront, Scan, Stack) were
-- absent from them entirely, and six analytic modules were only partly covered.
-- The entries below close that gap. The enumeration gate at the foot of section
-- (2) is what keeps it closed: it walks the environment rather than a list, so
-- a theorem added tomorrow is audited whether or not anyone remembers to name
-- it here.

-- Core.Share, the remainder: the supporting lemmas of the share construction.
assert_no_sorry CIRISOntology.Core.mul_log_mul
assert_no_sorry CIRISOntology.Core.entropy_parity'
assert_no_sorry CIRISOntology.Core.entropy_indep'
assert_no_sorry CIRISOntology.Core.indep_isProb
assert_no_sorry CIRISOntology.Core.indep_samePairs
assert_no_sorry CIRISOntology.Core.log_card_eight
assert_no_sorry CIRISOntology.Core.mul_log_sub_le

-- Core.ShareQuantum, the remainder: the density-operator lifting lemmas.
assert_no_sorry CIRISOntology.Core.vnEntropy_of_isHermitian
assert_no_sorry CIRISOntology.Core.isHermitian_diagEmbed
assert_no_sorry CIRISOntology.Core.ptr₁₃_diagEmbed
assert_no_sorry CIRISOntology.Core.ptr₂₃_diagEmbed
assert_no_sorry CIRISOntology.Core.smul_one_sub_diagonal
assert_no_sorry CIRISOntology.Core.det_smul_one_sub
assert_no_sorry CIRISOntology.Core.det_smul_one_sub_diagEmbed
assert_no_sorry CIRISOntology.Core.eval_prod_linear
assert_no_sorry CIRISOntology.Core.multiset_eq_of_prod_linear
assert_no_sorry CIRISOntology.Core.sum_mul_log_multiset
assert_no_sorry CIRISOntology.Core.entropy_congr_multiset

-- Core.EntropyIneq, the remainder: the ladder's supporting inequalities.
assert_no_sorry CIRISOntology.Core.vnEntropy_congr_of_det
assert_no_sorry CIRISOntology.Core.vnEntropy_reindex
assert_no_sorry CIRISOntology.Core.ptrR_isHermitian
assert_no_sorry CIRISOntology.Core.ptrL_isHermitian
assert_no_sorry CIRISOntology.Core.trace_ptrR
assert_no_sorry CIRISOntology.Core.trace_ptrL
assert_no_sorry CIRISOntology.Core.ptrR_posSemidef
assert_no_sorry CIRISOntology.Core.ptrL_posSemidef
assert_no_sorry CIRISOntology.Core.isDensity_ptrR
assert_no_sorry CIRISOntology.Core.isDensity_ptrL
assert_no_sorry CIRISOntology.Core.kronecker_conjTranspose'
assert_no_sorry CIRISOntology.Core.isDensity_conj_unitary
assert_no_sorry CIRISOntology.Core.isProb_diagRe
assert_no_sorry CIRISOntology.Core.ptrR_conj_kronecker
assert_no_sorry CIRISOntology.Core.ptrL_conj_kronecker
assert_no_sorry CIRISOntology.Core.diagRe_ptrR
assert_no_sorry CIRISOntology.Core.diagRe_ptrL
assert_no_sorry CIRISOntology.Core.diagRe_diagonal
assert_no_sorry CIRISOntology.Core.vnEntropy_mul_conjTranspose_comm
assert_no_sorry CIRISOntology.Core.posSemidef_vecMulVec_star
assert_no_sorry CIRISOntology.Core.ptrR_purifyVec
assert_no_sorry CIRISOntology.Core.vnEntropy_kron_unif

-- Core.BellCeiling, the remainder: the C5 ring state's combinatorial core.
assert_no_sorry CIRISOntology.Core.sum5
assert_no_sorry CIRISOntology.Core.card_five_slots
assert_no_sorry CIRISOntology.Core.updBit_eq_update
assert_no_sorry CIRISOntology.Core.sgnZ_mul_self
assert_no_sorry CIRISOntology.Core.star_psiC5
assert_no_sorry CIRISOntology.Core.PsiC5_apply
assert_no_sorry CIRISOntology.Core.PsiC5_diag
assert_no_sorry CIRISOntology.Core.signF_sum
assert_no_sorry CIRISOntology.Core.mixF_sum
assert_no_sorry CIRISOntology.Core.pairPtr_PsiC5_apply
assert_no_sorry CIRISOntology.Core.isDensity_mixed5
assert_no_sorry CIRISOntology.Core.pairPtr_mixed5_apply
assert_no_sorry CIRISOntology.Core.pairPtr_mixed5_eq_PsiC5

-- Core.HammingCap, the remainder: the four-slot collision rung.
assert_no_sorry CIRISOntology.Core.sum4
assert_no_sorry CIRISOntology.Core.card_four_slots
assert_no_sorry CIRISOntology.Core.funext4
assert_no_sorry CIRISOntology.Core.sgn_eq
assert_no_sorry CIRISOntology.Core.sum_pushforward
assert_no_sorry CIRISOntology.Core.sum_chr1_zero
assert_no_sorry CIRISOntology.Core.sum_chr2_zero
assert_no_sorry CIRISOntology.Core.sgn_xor
assert_no_sorry CIRISOntology.Core.sgn_mul_self
assert_no_sorry CIRISOntology.Core.chr4_mul_chr4
assert_no_sorry CIRISOntology.Core.chr3_mul_self
assert_no_sorry CIRISOntology.Core.chr4_mul_chr3
assert_no_sorry CIRISOntology.Core.chr3_mul_chr3
assert_no_sorry CIRISOntology.Core.isProb_pushforward
assert_no_sorry CIRISOntology.Core.pushforward_comp
assert_no_sorry CIRISOntology.Core.pairMarg_pushforward

-- Core.Intensive, the remainder: the per-unit limit's supporting lemmas.
assert_no_sorry CIRISOntology.Core.equicorr_eq_smul
assert_no_sorry CIRISOntology.Core.equicorr_det_factored
assert_no_sorry CIRISOntology.Core.equicorr_det
assert_no_sorry CIRISOntology.Core.equicorr_det_pos
assert_no_sorry CIRISOntology.Core.Sfun_eq
assert_no_sorry CIRISOntology.Core.Sfun_nonneg
assert_no_sorry CIRISOntology.Core.Sfun_pos
assert_no_sorry CIRISOntology.Core.Sfun_zero
assert_no_sorry CIRISOntology.Core.Sclosed_hasDerivAt
assert_no_sorry CIRISOntology.Core.Sclosed_monotoneOn
assert_no_sorry CIRISOntology.Core.Sfun_monotoneOn
assert_no_sorry CIRISOntology.Core.Sfun_antitone_of_rho_antitone

-- Core.WrongKind — THE TAXONOMY OF CHANGE: eleven artifact-local kinds carried
-- in plain words, plus Record, the one frame-relation. The negative result
-- (repairable_does_not_factor) is what puts Record outside the base plane.
assert_no_sorry CIRISOntology.Core.basePlane_card
assert_no_sorry CIRISOntology.Core.one_frame_dependent
assert_no_sorry CIRISOntology.Core.zero_design_dependent
assert_no_sorry CIRISOntology.Core.no_label_moves_with_both
assert_no_sorry CIRISOntology.Core.contingent_is_the_only_marker
assert_no_sorry CIRISOntology.Core.marker_matches_disposition
assert_no_sorry CIRISOntology.Core.binding_never_varies
assert_no_sorry CIRISOntology.Core.axiomatic_binds_by_varying
assert_no_sorry CIRISOntology.Core.repairability_not_intrinsic
assert_no_sorry CIRISOntology.Core.frameInvariant_of_artifact_only
assert_no_sorry CIRISOntology.Core.repairable_not_frameInvariant
assert_no_sorry CIRISOntology.Core.repairable_does_not_factor
assert_no_sorry CIRISOntology.Core.self_declared_frame_undetermined
assert_no_sorry CIRISOntology.Core.testimonial_has_corpus
assert_no_sorry CIRISOntology.Core.warrant_invisible_to_kind
assert_no_sorry CIRISOntology.Core.warrant_invisible_to_policy

-- Core.Generator — the kinds derived rather than stipulated: the exact image of
-- a speech-act-grounded site model, with Record provably not site-generated.
assert_no_sorry CIRISOntology.Core.every_site_classified
assert_no_sorry CIRISOntology.Core.generator_image
assert_no_sorry CIRISOntology.Core.generator_injective
assert_no_sorry CIRISOntology.Core.record_not_site_generated
assert_no_sorry CIRISOntology.Core.contingent_site_exists

-- Core.Instrument — the reading record (a Record reading always carries its
-- frame) and the instrument suite, shipped with its honesty pin unflipped.
assert_no_sorry CIRISOntology.Core.reading_record_has_frame
assert_no_sorry CIRISOntology.Core.no_reading_owes_design
assert_no_sorry CIRISOntology.Core.suite_covers_every_kind
assert_no_sorry CIRISOntology.Core.suite_ships_unvalidated

-- Core.Confront — the twelve wild confrontations: every domain encoded, the
-- candidate table exhausted, and abc read as frame-relativity in the wild.
assert_no_sorry CIRISOntology.Core.abc_repairability_is_frame_relative
assert_no_sorry CIRISOntology.Core.circumstances_asserts_nothing
assert_no_sorry CIRISOntology.Core.confrontations_constructed
assert_no_sorry CIRISOntology.Core.only_the_record_entry_carries_a_frame
assert_no_sorry CIRISOntology.Core.record_entry_has_frame
assert_no_sorry CIRISOntology.Core.stake_is_the_reading
assert_no_sorry CIRISOntology.Core.domains_encoded
assert_no_sorry CIRISOntology.Core.every_domain_encoded
assert_no_sorry CIRISOntology.Core.chemistry_present
assert_no_sorry CIRISOntology.Core.candidate_table_exhausted
assert_no_sorry CIRISOntology.Core.kinds_not_reached

-- Core.Scan — THE FORCE BUDGET: which kinds an illocutionary budget buys, the
-- 7 -> 10 -> 11 chain, and why the three-force scan is terminal rather than
-- merely largest-so-far.
assert_no_sorry CIRISOntology.Core.Force.mem_all
assert_no_sorry CIRISOntology.Core.carriers_are_the_neutral_sites
assert_no_sorry CIRISOntology.Core.site_all_nodup
assert_no_sorry CIRISOntology.Core.scan_nodup
assert_no_sorry CIRISOntology.Core.scan_assertive
assert_no_sorry CIRISOntology.Core.scan_assertive_card
assert_no_sorry CIRISOntology.Core.scan_assertive_directive
assert_no_sorry CIRISOntology.Core.scan_assertive_directive_card
assert_no_sorry CIRISOntology.Core.scan_full
assert_no_sorry CIRISOntology.Core.scan_full_card
assert_no_sorry CIRISOntology.Core.scan_full_card_eq_basePlane
assert_no_sorry CIRISOntology.Core.scan_full_is_basePlane
assert_no_sorry CIRISOntology.Core.record_in_no_scan
assert_no_sorry CIRISOntology.Core.availableSites_mono
assert_no_sorry CIRISOntology.Core.scan_mono
assert_no_sorry CIRISOntology.Core.scan_le_full
assert_no_sorry CIRISOntology.Core.availableSites_univ
assert_no_sorry CIRISOntology.Core.scan_terminal
assert_no_sorry CIRISOntology.Core.scan_terminal_card
assert_no_sorry CIRISOntology.Core.scan_lattice
assert_no_sorry CIRISOntology.Core.carriers_survive_everything
assert_no_sorry CIRISOntology.Core.scan_floor
assert_no_sorry CIRISOntology.Core.carriers_in_every_scan
assert_no_sorry CIRISOntology.Core.scanAlt_chain_agrees
assert_no_sorry CIRISOntology.Core.scanAlt_floor
assert_no_sorry CIRISOntology.Core.scanAlt_directive_only

-- Core.Stack — the grounding stack: four rungs, injective into the site model,
-- climbing by one and stopping at a fixed point rather than an infinite ladder.
assert_no_sorry CIRISOntology.Core.stack_card
assert_no_sorry CIRISOntology.Core.every_rung_listed
assert_no_sorry CIRISOntology.Core.stack_kinds
assert_no_sorry CIRISOntology.Core.stack_plain
assert_no_sorry CIRISOntology.Core.rung_kind_injective
assert_no_sorry CIRISOntology.Core.rung_site_injective
assert_no_sorry CIRISOntology.Core.four_sites_in_stack
assert_no_sorry CIRISOntology.Core.seven_sites_outside_stack
assert_no_sorry CIRISOntology.Core.rung_site_inStack
assert_no_sorry CIRISOntology.Core.ground_climbs
assert_no_sorry CIRISOntology.Core.ground_moves
assert_no_sorry CIRISOntology.Core.top_is_maximal
assert_no_sorry CIRISOntology.Core.ground_top_fixed
assert_no_sorry CIRISOntology.Core.modulate_const
assert_no_sorry CIRISOntology.Core.modulate_site
assert_no_sorry CIRISOntology.Core.modulate_top
assert_no_sorry CIRISOntology.Core.modulate_idempotent
assert_no_sorry CIRISOntology.Core.modulate_nested
assert_no_sorry CIRISOntology.Core.modulate_eq_climb
assert_no_sorry CIRISOntology.Core.ground_three
assert_no_sorry CIRISOntology.Core.ground_reaches_top
assert_no_sorry CIRISOntology.Core.ground_terminal
assert_no_sorry CIRISOntology.Core.iterate_site_in_stack
assert_no_sorry CIRISOntology.Core.iterate_site_is_one_of_four
assert_no_sorry CIRISOntology.Core.terminal_kind

-- (2) No published theorem rests on anything exotic.
assert_standard_axioms CIRISOntology.Core.S_pairwise_identity
assert_standard_axioms CIRISOntology.Core.not_computable_from
assert_standard_axioms CIRISOntology.Core.provenance_line
assert_standard_axioms CIRISOntology.Core.parity_corr_eq_one
assert_standard_axioms CIRISOntology.Core.pairwise_blind_to_parity
assert_standard_axioms CIRISOntology.Core.third_sees_parity
assert_standard_axioms CIRISOntology.Core.third_reading_positive
assert_standard_axioms CIRISOntology.Core.parity_pair_independent_12
assert_standard_axioms CIRISOntology.Core.parity_pair_independent_13
assert_standard_axioms CIRISOntology.Core.parity_pair_independent_23
assert_standard_axioms CIRISOntology.Core.indep_corr_eq_one
assert_standard_axioms CIRISOntology.Core.S_total_indep
assert_standard_axioms CIRISOntology.Core.corr_separates_total
assert_standard_axioms CIRISOntology.Core.total_not_computable_from_corr
assert_standard_axioms CIRISOntology.Core.rent_holds
assert_standard_axioms CIRISOntology.Core.paid_const
assert_standard_axioms CIRISOntology.Core.underpaid_shrinks
assert_standard_axioms CIRISOntology.Core.unpaid_succ
assert_standard_axioms CIRISOntology.Core.unpaid_decays
-- Core.Share — the whole-only share, defined on the state itself.
assert_standard_axioms CIRISOntology.Core.entropy_le_log_card
assert_standard_axioms CIRISOntology.Core.entropy_nonneg
assert_standard_axioms CIRISOntology.Core.pairEnvelope_bddAbove
assert_standard_axioms CIRISOntology.Core.share_nonneg
assert_standard_axioms CIRISOntology.Core.share_parity
assert_standard_axioms CIRISOntology.Core.share_parity_positive
assert_standard_axioms CIRISOntology.Core.entropy_grouping
assert_standard_axioms CIRISOntology.Core.share_copied
assert_standard_axioms CIRISOntology.Core.S_total_copied
assert_standard_axioms CIRISOntology.Core.S_total_copied_positive
-- Core.ShareQuantum — the whole-only share lifted to density operators.
assert_standard_axioms CIRISOntology.Core.trace_eq_sum_eigenvalues_rclike
assert_standard_axioms CIRISOntology.Core.vnEntropy_le_log_card
assert_standard_axioms CIRISOntology.Core.vnEntropy_nonneg
assert_standard_axioms CIRISOntology.Core.qPairEnvelope_bddAbove
assert_standard_axioms CIRISOntology.Core.qShare_nonneg
assert_standard_axioms CIRISOntology.Core.isDensity_diagEmbed
assert_standard_axioms CIRISOntology.Core.vnEntropy_diagEmbed
assert_standard_axioms CIRISOntology.Core.ptr₁₂_diagEmbed
assert_standard_axioms CIRISOntology.Core.qShare_parity
assert_standard_axioms CIRISOntology.Core.qShare_eq_share_parity
-- Core.ShareK — the k-slot share and the classical cap (the Bell bound).
assert_standard_axioms CIRISOntology.Core.entropy_map_le
assert_standard_axioms CIRISOntology.Core.shareK_le_log_sub_pair
assert_standard_axioms CIRISOntology.Core.shareK_le_of_pair_uniform
assert_standard_axioms CIRISOntology.Core.pushforward_pair_parity
assert_standard_axioms CIRISOntology.Core.share_le_log_sub_pair₃
assert_standard_axioms CIRISOntology.Core.temporal_third_saturates
assert_standard_axioms CIRISOntology.Core.qPairEnvelopeK_bddAbove
assert_standard_axioms CIRISOntology.Core.qShareK_nonneg
assert_standard_axioms CIRISOntology.Core.qShareK_le_log_card
-- Core.EntropyIneq — the Araki-Lieb ladder and the causal past-view bound.
assert_standard_axioms CIRISOntology.Core.mul_log_jensen
assert_standard_axioms CIRISOntology.Core.vnEntropy_conj_unitary
assert_standard_axioms CIRISOntology.Core.vnEntropy_le_entropy_diagRe
assert_standard_axioms CIRISOntology.Core.entropy_grouping₂
assert_standard_axioms CIRISOntology.Core.vnEntropy_subadd
assert_standard_axioms CIRISOntology.Core.vnEntropy_ptr_complementary
assert_standard_axioms CIRISOntology.Core.vnEntropy_triangle
assert_standard_axioms CIRISOntology.Core.vnEntropy_causal_past
-- Core.BellCeiling — the ideal quantum ceiling: qShareK(C5) = 5 log 2.
assert_standard_axioms CIRISOntology.Core.isDensity_PsiC5
assert_standard_axioms CIRISOntology.Core.vnEntropy_PsiC5
assert_standard_axioms CIRISOntology.Core.pairPtr_PsiC5
assert_standard_axioms CIRISOntology.Core.bell_ceiling
assert_standard_axioms CIRISOntology.Core.bell_ceiling_exceeds_cap
assert_standard_axioms CIRISOntology.Core.qShareK_max_five
-- Core.HammingCap — the tightened classical cap: (k-3) log 2 for k >= 4.
assert_standard_axioms CIRISOntology.Core.kern_eq
assert_standard_axioms CIRISOntology.Core.kern_real
assert_standard_axioms CIRISOntology.Core.inversion
assert_standard_axioms CIRISOntology.Core.sum_sq_le_eighth
assert_standard_axioms CIRISOntology.Core.entropy_ge_three_log_two
assert_standard_axioms CIRISOntology.Core.shareK_le_of_pair_uniform_four
assert_standard_axioms CIRISOntology.Core.shareK_le_of_pair_uniform_ge_four
assert_standard_axioms CIRISOntology.Core.shareK_le_of_four_pair_uniform
assert_standard_axioms CIRISOntology.Core.entropy_ge_of_sum_sq_le
-- Core.SignSymmetry — global sign symmetry forces the whole-only share to zero.
assert_standard_axioms CIRISOntology.Core.sum_comp_signFlip
assert_standard_axioms CIRISOntology.Core.symmetrize_signSymmetric
assert_standard_axioms CIRISOntology.Core.symmetrize_isProb
assert_standard_axioms CIRISOntology.Core.entropy_le_symmetrize
assert_standard_axioms CIRISOntology.Core.samePairs_symmetrize
assert_standard_axioms CIRISOntology.Core.eq_of_signSymmetric_of_samePairs
assert_standard_axioms CIRISOntology.Core.share_eq_zero_of_signSymmetric
assert_standard_axioms CIRISOntology.Core.share_indep
assert_standard_axioms CIRISOntology.Core.ferro_isProb
assert_standard_axioms CIRISOntology.Core.ferro_signSymmetric
assert_standard_axioms CIRISOntology.Core.share_ferro
assert_standard_axioms CIRISOntology.Core.S_total_ferro
assert_standard_axioms CIRISOntology.Core.parity_not_signSymmetric
-- Core.Creation — MAINTENANCE IS CREATION: one application of a code's repair
-- map to pure noise mints that code's whole-only share exactly, and the
-- sign-symmetry lemma governs which repairs can mint. The no-creation half is
-- general in the input state: a map that reads no cell but its own can never
-- raise the share.
assert_standard_axioms CIRISOntology.Core.parityRepair_idempotent
assert_standard_axioms CIRISOntology.Core.parityRepair_fixed_iff
assert_standard_axioms CIRISOntology.Core.majority_eq
assert_standard_axioms CIRISOntology.Core.majorityRepair_idempotent
assert_standard_axioms CIRISOntology.Core.majorityRepair_fixed_iff
assert_standard_axioms CIRISOntology.Core.pushforward_equiv
assert_standard_axioms CIRISOntology.Core.pushforward_parityRepair_indep
assert_standard_axioms CIRISOntology.Core.repair_creates_parity
assert_standard_axioms CIRISOntology.Core.repair_mints_from_noise
assert_standard_axioms CIRISOntology.Core.S_total_parityRepair
assert_standard_axioms CIRISOntology.Core.parityRepair_pays_one_bit
assert_standard_axioms CIRISOntology.Core.pushforward_majorityRepair_indep
assert_standard_axioms CIRISOntology.Core.repair_creates_ferro
assert_standard_axioms CIRISOntology.Core.S_total_majorityRepair
assert_standard_axioms CIRISOntology.Core.majorityRepair_pays_two_bits
assert_standard_axioms CIRISOntology.Core.parityRepair_not_percell
assert_standard_axioms CIRISOntology.Core.majorityRepair_not_percell
assert_standard_axioms CIRISOntology.Core.entropy_reindex
assert_standard_axioms CIRISOntology.Core.entropy_reidx
assert_standard_axioms CIRISOntology.Core.isProb_reidx
assert_standard_axioms CIRISOntology.Core.samePairs_reidx
assert_standard_axioms CIRISOntology.Core.pairEnvelope_reidx
assert_standard_axioms CIRISOntology.Core.share_reidx
assert_standard_axioms CIRISOntology.Core.bool_bijective_of_ne
assert_standard_axioms CIRISOntology.Core.bool_const_of_eq
assert_standard_axioms CIRISOntology.Core.share_pushforward_percell_of_bijective
assert_standard_axioms CIRISOntology.Core.entropy_grouping₂₃
assert_standard_axioms CIRISOntology.Core.entropy_grouping₁₃
assert_standard_axioms CIRISOntology.Core.marg₁_of_samePairs
assert_standard_axioms CIRISOntology.Core.marg₂_of_samePairs
assert_standard_axioms CIRISOntology.Core.marg₃_of_samePairs
assert_standard_axioms CIRISOntology.Core.entropy_point_mass
assert_standard_axioms CIRISOntology.Core.share_eq_zero_of_entropy_maximal
assert_standard_axioms CIRISOntology.Core.share_eq_zero_of_third_det
assert_standard_axioms CIRISOntology.Core.share_eq_zero_of_first_det
assert_standard_axioms CIRISOntology.Core.share_eq_zero_of_second_det
assert_standard_axioms CIRISOntology.Core.share_pushforward_percell_of_const₁
assert_standard_axioms CIRISOntology.Core.share_pushforward_percell_of_const₂
assert_standard_axioms CIRISOntology.Core.share_pushforward_percell_of_const₃
assert_standard_axioms CIRISOntology.Core.percell_no_creation
-- Core.Valve — THE ONE-WAY VALVE: under per-cell STOCHASTIC channels, order
-- flows UP the hierarchy (valve_upward — pure pair order mints strictly
-- positive whole-only share, which no DETERMINISTIC per-cell map can do),
-- never DOWN (valve_no_downward — the parity habit's decay never deposits
-- pairwise correlation, under any three kernels), and never FROM NOTHING
-- (valve_from_nothing — a product state in, whole-only share exactly zero out).
assert_standard_axioms CIRISOntology.Core.push1_isProb
assert_standard_axioms CIRISOntology.Core.channel3_isProb
assert_standard_axioms CIRISOntology.Core.channel3_prod3
assert_standard_axioms CIRISOntology.Core.isProb_prod2
assert_standard_axioms CIRISOntology.Core.prod3_isProb
assert_standard_axioms CIRISOntology.Core.entropy_prod2
assert_standard_axioms CIRISOntology.Core.entropy_prod3
assert_standard_axioms CIRISOntology.Core.marg₁₂_prod3
assert_standard_axioms CIRISOntology.Core.marg₃_prod3
assert_standard_axioms CIRISOntology.Core.share_prod3
assert_standard_axioms CIRISOntology.Core.valve_from_nothing
assert_standard_axioms CIRISOntology.Core.unifBool_isProb
assert_standard_axioms CIRISOntology.Core.indep_eq_prod3
assert_standard_axioms CIRISOntology.Core.valve_from_nothing_indep
assert_standard_axioms CIRISOntology.Core.marg₁₂_channel3
assert_standard_axioms CIRISOntology.Core.marg₁₃_channel3
assert_standard_axioms CIRISOntology.Core.marg₂₃_channel3
assert_standard_axioms CIRISOntology.Core.marg₁₂_channel3_of_prod
assert_standard_axioms CIRISOntology.Core.marg₁₃_channel3_of_prod
assert_standard_axioms CIRISOntology.Core.marg₂₃_channel3_of_prod
assert_standard_axioms CIRISOntology.Core.marg₁_channel3
assert_standard_axioms CIRISOntology.Core.marg₂_channel3
assert_standard_axioms CIRISOntology.Core.marg₃_channel3
assert_standard_axioms CIRISOntology.Core.marg₁₂_parity
assert_standard_axioms CIRISOntology.Core.marg₁₃_parity
assert_standard_axioms CIRISOntology.Core.marg₂₃_parity
assert_standard_axioms CIRISOntology.Core.marg₁_parity
assert_standard_axioms CIRISOntology.Core.marg₂_parity
assert_standard_axioms CIRISOntology.Core.marg₃_parity
assert_standard_axioms CIRISOntology.Core.valve_no_downward_12
assert_standard_axioms CIRISOntology.Core.valve_no_downward_13
assert_standard_axioms CIRISOntology.Core.valve_no_downward_23
assert_standard_axioms CIRISOntology.Core.valve_no_downward
assert_standard_axioms CIRISOntology.Core.damp_isKernel
assert_standard_axioms CIRISOntology.Core.channel3_damp_ferro
assert_standard_axioms CIRISOntology.Core.bulge_isProb
assert_standard_axioms CIRISOntology.Core.bulgeWitness_isProb
assert_standard_axioms CIRISOntology.Core.bulgeWitness_samePairs
assert_standard_axioms CIRISOntology.Core.entropy_bulge
assert_standard_axioms CIRISOntology.Core.entropy_bulgeWitness
assert_standard_axioms CIRISOntology.Core.entropy_bulge_lt_bulgeWitness
assert_standard_axioms CIRISOntology.Core.valve_upward
assert_standard_axioms CIRISOntology.Core.valve_upward_bound
assert_standard_axioms CIRISOntology.Core.valve_upward_strict
assert_standard_axioms CIRISOntology.Core.stochastic_percell_can_create
-- Core.Valve, the pump: the odd sector is fed only by asymmetry. A flip-
-- covariant kernel (the binary symmetric channel) commutes with the global
-- sign flip, so it mints exactly zero from any sign-symmetric state; the
-- upward flow REQUIRES a channel that breaks the flip symmetry, and damping
-- does (damp_not_flipCovariant).
assert_standard_axioms CIRISOntology.Core.isFlipCovariant_of_symm
assert_standard_axioms CIRISOntology.Core.signSymmetric_channel3
assert_standard_axioms CIRISOntology.Core.valve_needs_asymmetry
assert_standard_axioms CIRISOntology.Core.valve_needs_asymmetry_ferro
assert_standard_axioms CIRISOntology.Core.damp_not_flipCovariant
-- Core.ThirdCap — THE DENOMINATOR: three binary slots carry at most one bit of
-- whole-only share, with NO hypothesis on the pair marginals.
assert_standard_axioms CIRISOntology.Core.entropy_marg₁₂_le
assert_standard_axioms CIRISOntology.Core.marg₃_eq_of_samePairs
assert_standard_axioms CIRISOntology.Core.marg₃_isProb
assert_standard_axioms CIRISOntology.Core.share_le_pair_third_gap
assert_standard_axioms CIRISOntology.Core.share_le_log_card_third
assert_standard_axioms CIRISOntology.Core.share_le_log_two
assert_standard_axioms CIRISOntology.Core.share_max_eq_log_two
assert_standard_axioms CIRISOntology.Core.share_le_grouping_gaps
-- Core.Entropy — the entropic-contraction spine.
assert_standard_axioms CIRISOntology.Core.trace_eq_sum_eigenvalues
assert_standard_axioms CIRISOntology.Core.neg_log_det_nonneg
assert_standard_axioms CIRISOntology.Core.S_pairwise_nonneg
assert_standard_axioms CIRISOntology.Core.neg_log_det_eq_zero_iff
assert_standard_axioms CIRISOntology.Core.hadamard_posSemidef
assert_standard_axioms CIRISOntology.Core.IsUnitDiag.hadamard
assert_standard_axioms CIRISOntology.Core.oppenheim_two
assert_standard_axioms CIRISOntology.Core.S_pairwise_hadamard_le_two
assert_standard_axioms CIRISOntology.Core.neg_log_det_hadamard_nonneg
assert_standard_axioms CIRISOntology.Core.one_le_det_one_add_posSemidef
assert_standard_axioms CIRISOntology.Core.det_le_det_add_of_posDef_posSemidef
assert_standard_axioms CIRISOntology.Core.posSemidef_det_nonneg
assert_standard_axioms CIRISOntology.Core.posDef_of_posSemidef_det_pos
assert_standard_axioms CIRISOntology.Core.det_le_det_add_of_posSemidef
assert_standard_axioms CIRISOntology.Core.hadamard_fromBlocks
assert_standard_axioms CIRISOntology.Core.hadamard_vecMulVec
assert_standard_axioms CIRISOntology.Core.submatrix_hadamard
assert_standard_axioms CIRISOntology.Core.posSemidef_vecMulVec
assert_standard_axioms CIRISOntology.Core.schur_hadamard_identity
assert_standard_axioms CIRISOntology.Core.schur_oneScalar
assert_standard_axioms CIRISOntology.Core.posDef_diag_pos
assert_standard_axioms CIRISOntology.Core.det_schur_reduce
assert_standard_axioms CIRISOntology.Core.posSemidef_smul
assert_standard_axioms CIRISOntology.Core.isHermitian_hadamard
assert_standard_axioms CIRISOntology.Core.posDef_fin_one
assert_standard_axioms CIRISOntology.Core.schur_posSemidef
assert_standard_axioms CIRISOntology.Core.oppenheim_det
assert_standard_axioms CIRISOntology.Core.S_pairwise_hadamard_le
-- Core.OppenheimRCLike — the complex-general (RCLike) Oppenheim spine.
assert_standard_axioms CIRISOntology.Core.Herm.posSemidef_vecMulVec
assert_standard_axioms CIRISOntology.Core.Herm.hadamard_vecMulVec
assert_standard_axioms CIRISOntology.Core.Herm.schur_hadamard_identity
assert_standard_axioms CIRISOntology.Core.Herm.schur_oneScalar
assert_standard_axioms CIRISOntology.Core.Herm.posDef_diag_pos
assert_standard_axioms CIRISOntology.Core.Herm.posDef_fin_one
assert_standard_axioms CIRISOntology.Core.Herm.isHermitian_hadamard
assert_standard_axioms CIRISOntology.Core.Herm.posSemidef_smul
assert_standard_axioms CIRISOntology.Core.Herm.submatrix_hadamard
assert_standard_axioms CIRISOntology.Core.Herm.hadamard_fromBlocks
assert_standard_axioms CIRISOntology.Core.Herm.posSemidef_det_nonneg
assert_standard_axioms CIRISOntology.Core.Herm.posDef_of_posSemidef_isUnit_det
assert_standard_axioms CIRISOntology.Core.Herm.one_le_det_one_add_posSemidef
assert_standard_axioms CIRISOntology.Core.Herm.det_le_det_add_of_posDef_posSemidef
assert_standard_axioms CIRISOntology.Core.Herm.det_le_det_add_of_posSemidef
assert_standard_axioms CIRISOntology.Core.Herm.hadamard_posSemidef
assert_standard_axioms CIRISOntology.Core.Herm.det_schur_reduce
assert_standard_axioms CIRISOntology.Core.Herm.schur_posSemidef
assert_standard_axioms CIRISOntology.Core.Herm.oppenheim_det
assert_standard_axioms CIRISOntology.Core.Herm.posSemidef_diag_nonneg
assert_standard_axioms CIRISOntology.Core.Herm.eq_ofReal_re_of_nonneg
assert_standard_axioms CIRISOntology.Core.Herm.diag_conj_entry
assert_standard_axioms CIRISOntology.Core.Herm.oppenheim_prod
-- Core.Flavor — the Jarlskog CP-violation cap (cp-cap).
assert_standard_axioms CIRISOntology.Core.jarlskogMax_nonneg
assert_standard_axioms CIRISOntology.Core.abs_jarlskog_le_max
assert_standard_axioms CIRISOntology.Core.jarlskogMax_zero_at_no_mixing
assert_standard_axioms CIRISOntology.Core.jarlskogMax_zero_at_max_13mixing
-- Core.FlavorBridge — the flavour bridge: the Jarlskog coordinate IS the share.
assert_standard_axioms CIRISOntology.Core.parityChar_signFlip
assert_standard_axioms CIRISOntology.Core.cpState_isProb
assert_standard_axioms CIRISOntology.Core.cpState_zero
assert_standard_axioms CIRISOntology.Core.cpState_neg_eq_signFlip
assert_standard_axioms CIRISOntology.Core.symmetrize_cpState
assert_standard_axioms CIRISOntology.Core.cpState_signSymmetric_iff
assert_standard_axioms CIRISOntology.Core.cp_phase_invisible_to_pairs
assert_standard_axioms CIRISOntology.Core.cpState_corr_eq_one
assert_standard_axioms CIRISOntology.Core.cpShare_neg
assert_standard_axioms CIRISOntology.Core.cpShare_zero
assert_standard_axioms CIRISOntology.Core.entropy_cpState
assert_standard_axioms CIRISOntology.Core.share_cpState
assert_standard_axioms CIRISOntology.Core.cpShare_nonneg
assert_standard_axioms CIRISOntology.Core.cpShare_pos
assert_standard_axioms CIRISOntology.Core.share_zero_of_cp_even
assert_standard_axioms CIRISOntology.Core.share_pos_of_cp_odd
assert_standard_axioms CIRISOntology.Core.share_cpState_eq_zero_iff
assert_standard_axioms CIRISOntology.Core.share_symmetrize_cpState
assert_standard_axioms CIRISOntology.Core.mul_log_convex
assert_standard_axioms CIRISOntology.Core.entropy_concave
assert_standard_axioms CIRISOntology.Core.cpState_mix
assert_standard_axioms CIRISOntology.Core.cpShare_mul_le
assert_standard_axioms CIRISOntology.Core.abs_jarlskog_le_one
assert_standard_axioms CIRISOntology.Core.abs_jarlskogMax_le_one
assert_standard_axioms CIRISOntology.Core.share_cpFamily_le_phase
assert_standard_axioms CIRISOntology.Core.share_cpFamily_le_jarlskogMax
assert_standard_axioms CIRISOntology.Core.share_cpFamily_zero_of_cp_even
assert_standard_axioms CIRISOntology.Core.cpFamily_signSymmetric_of_cp_even
assert_standard_axioms CIRISOntology.Core.share_cpFamily_zero_at_no_mixing
assert_standard_axioms CIRISOntology.Core.share_cpFamily_zero_at_max_13mixing
assert_standard_axioms CIRISOntology.Core.share_cpFamily_pos
assert_standard_axioms CIRISOntology.Core.share_cpFamily_eq_zero_iff
assert_standard_axioms CIRISOntology.Core.cpShare_one
assert_standard_axioms CIRISOntology.Core.share_cpState_one
assert_standard_axioms CIRISOntology.Core.cpState_neg_one
assert_standard_axioms CIRISOntology.Core.share_parity_eq_cpShare
-- Core.Intensive — the intensive (per-unit) limit.
assert_standard_axioms CIRISOntology.Core.Sfun_div_k_tendsto
-- Core.Third — relabeling-invariance of the total-dependence instrument.
assert_standard_axioms CIRISOntology.Core.S_total_relabel_fst

-- Core.Share, the remainder: the supporting lemmas of the share construction.
assert_standard_axioms CIRISOntology.Core.mul_log_mul
assert_standard_axioms CIRISOntology.Core.entropy_parity'
assert_standard_axioms CIRISOntology.Core.entropy_indep'
assert_standard_axioms CIRISOntology.Core.indep_isProb
assert_standard_axioms CIRISOntology.Core.indep_samePairs
assert_standard_axioms CIRISOntology.Core.log_card_eight
assert_standard_axioms CIRISOntology.Core.mul_log_sub_le

-- Core.ShareQuantum, the remainder: the density-operator lifting lemmas.
assert_standard_axioms CIRISOntology.Core.vnEntropy_of_isHermitian
assert_standard_axioms CIRISOntology.Core.isHermitian_diagEmbed
assert_standard_axioms CIRISOntology.Core.ptr₁₃_diagEmbed
assert_standard_axioms CIRISOntology.Core.ptr₂₃_diagEmbed
assert_standard_axioms CIRISOntology.Core.smul_one_sub_diagonal
assert_standard_axioms CIRISOntology.Core.det_smul_one_sub
assert_standard_axioms CIRISOntology.Core.det_smul_one_sub_diagEmbed
assert_standard_axioms CIRISOntology.Core.eval_prod_linear
assert_standard_axioms CIRISOntology.Core.multiset_eq_of_prod_linear
assert_standard_axioms CIRISOntology.Core.sum_mul_log_multiset
assert_standard_axioms CIRISOntology.Core.entropy_congr_multiset

-- Core.EntropyIneq, the remainder: the ladder's supporting inequalities.
assert_standard_axioms CIRISOntology.Core.vnEntropy_congr_of_det
assert_standard_axioms CIRISOntology.Core.vnEntropy_reindex
assert_standard_axioms CIRISOntology.Core.ptrR_isHermitian
assert_standard_axioms CIRISOntology.Core.ptrL_isHermitian
assert_standard_axioms CIRISOntology.Core.trace_ptrR
assert_standard_axioms CIRISOntology.Core.trace_ptrL
assert_standard_axioms CIRISOntology.Core.ptrR_posSemidef
assert_standard_axioms CIRISOntology.Core.ptrL_posSemidef
assert_standard_axioms CIRISOntology.Core.isDensity_ptrR
assert_standard_axioms CIRISOntology.Core.isDensity_ptrL
assert_standard_axioms CIRISOntology.Core.kronecker_conjTranspose'
assert_standard_axioms CIRISOntology.Core.isDensity_conj_unitary
assert_standard_axioms CIRISOntology.Core.isProb_diagRe
assert_standard_axioms CIRISOntology.Core.ptrR_conj_kronecker
assert_standard_axioms CIRISOntology.Core.ptrL_conj_kronecker
assert_standard_axioms CIRISOntology.Core.diagRe_ptrR
assert_standard_axioms CIRISOntology.Core.diagRe_ptrL
assert_standard_axioms CIRISOntology.Core.diagRe_diagonal
assert_standard_axioms CIRISOntology.Core.vnEntropy_mul_conjTranspose_comm
assert_standard_axioms CIRISOntology.Core.posSemidef_vecMulVec_star
assert_standard_axioms CIRISOntology.Core.ptrR_purifyVec
assert_standard_axioms CIRISOntology.Core.vnEntropy_kron_unif

-- Core.BellCeiling, the remainder: the C5 ring state's combinatorial core.
assert_standard_axioms CIRISOntology.Core.sum5
assert_standard_axioms CIRISOntology.Core.card_five_slots
assert_standard_axioms CIRISOntology.Core.updBit_eq_update
assert_standard_axioms CIRISOntology.Core.sgnZ_mul_self
assert_standard_axioms CIRISOntology.Core.star_psiC5
assert_standard_axioms CIRISOntology.Core.PsiC5_apply
assert_standard_axioms CIRISOntology.Core.PsiC5_diag
assert_standard_axioms CIRISOntology.Core.signF_sum
assert_standard_axioms CIRISOntology.Core.mixF_sum
assert_standard_axioms CIRISOntology.Core.pairPtr_PsiC5_apply
assert_standard_axioms CIRISOntology.Core.isDensity_mixed5
assert_standard_axioms CIRISOntology.Core.pairPtr_mixed5_apply
assert_standard_axioms CIRISOntology.Core.pairPtr_mixed5_eq_PsiC5

-- Core.HammingCap, the remainder: the four-slot collision rung.
assert_standard_axioms CIRISOntology.Core.sum4
assert_standard_axioms CIRISOntology.Core.card_four_slots
assert_standard_axioms CIRISOntology.Core.funext4
assert_standard_axioms CIRISOntology.Core.sgn_eq
assert_standard_axioms CIRISOntology.Core.sum_pushforward
assert_standard_axioms CIRISOntology.Core.sum_chr1_zero
assert_standard_axioms CIRISOntology.Core.sum_chr2_zero
assert_standard_axioms CIRISOntology.Core.sgn_xor
assert_standard_axioms CIRISOntology.Core.sgn_mul_self
assert_standard_axioms CIRISOntology.Core.chr4_mul_chr4
assert_standard_axioms CIRISOntology.Core.chr3_mul_self
assert_standard_axioms CIRISOntology.Core.chr4_mul_chr3
assert_standard_axioms CIRISOntology.Core.chr3_mul_chr3
assert_standard_axioms CIRISOntology.Core.isProb_pushforward
assert_standard_axioms CIRISOntology.Core.pushforward_comp
assert_standard_axioms CIRISOntology.Core.pairMarg_pushforward

-- Core.Intensive, the remainder: the per-unit limit's supporting lemmas.
assert_standard_axioms CIRISOntology.Core.equicorr_eq_smul
assert_standard_axioms CIRISOntology.Core.equicorr_det_factored
assert_standard_axioms CIRISOntology.Core.equicorr_det
assert_standard_axioms CIRISOntology.Core.equicorr_det_pos
assert_standard_axioms CIRISOntology.Core.Sfun_eq
assert_standard_axioms CIRISOntology.Core.Sfun_nonneg
assert_standard_axioms CIRISOntology.Core.Sfun_pos
assert_standard_axioms CIRISOntology.Core.Sfun_zero
assert_standard_axioms CIRISOntology.Core.Sclosed_hasDerivAt
assert_standard_axioms CIRISOntology.Core.Sclosed_monotoneOn
assert_standard_axioms CIRISOntology.Core.Sfun_monotoneOn
assert_standard_axioms CIRISOntology.Core.Sfun_antitone_of_rho_antitone

-- Core.WrongKind — THE TAXONOMY OF CHANGE: eleven artifact-local kinds carried
-- in plain words, plus Record, the one frame-relation. The negative result
-- (repairable_does_not_factor) is what puts Record outside the base plane.
assert_standard_axioms CIRISOntology.Core.basePlane_card
assert_standard_axioms CIRISOntology.Core.one_frame_dependent
assert_standard_axioms CIRISOntology.Core.zero_design_dependent
assert_standard_axioms CIRISOntology.Core.no_label_moves_with_both
assert_standard_axioms CIRISOntology.Core.contingent_is_the_only_marker
assert_standard_axioms CIRISOntology.Core.marker_matches_disposition
assert_standard_axioms CIRISOntology.Core.binding_never_varies
assert_standard_axioms CIRISOntology.Core.axiomatic_binds_by_varying
assert_standard_axioms CIRISOntology.Core.repairability_not_intrinsic
assert_standard_axioms CIRISOntology.Core.frameInvariant_of_artifact_only
assert_standard_axioms CIRISOntology.Core.repairable_not_frameInvariant
assert_standard_axioms CIRISOntology.Core.repairable_does_not_factor
assert_standard_axioms CIRISOntology.Core.self_declared_frame_undetermined
assert_standard_axioms CIRISOntology.Core.testimonial_has_corpus
assert_standard_axioms CIRISOntology.Core.warrant_invisible_to_kind
assert_standard_axioms CIRISOntology.Core.warrant_invisible_to_policy

-- Core.Generator — the kinds derived rather than stipulated: the exact image of
-- a speech-act-grounded site model, with Record provably not site-generated.
assert_standard_axioms CIRISOntology.Core.every_site_classified
assert_standard_axioms CIRISOntology.Core.generator_image
assert_standard_axioms CIRISOntology.Core.generator_injective
assert_standard_axioms CIRISOntology.Core.record_not_site_generated
assert_standard_axioms CIRISOntology.Core.contingent_site_exists

-- Core.Instrument — the reading record (a Record reading always carries its
-- frame) and the instrument suite, shipped with its honesty pin unflipped.
assert_standard_axioms CIRISOntology.Core.reading_record_has_frame
assert_standard_axioms CIRISOntology.Core.no_reading_owes_design
assert_standard_axioms CIRISOntology.Core.suite_covers_every_kind
assert_standard_axioms CIRISOntology.Core.suite_ships_unvalidated

-- Core.Confront — the twelve wild confrontations: every domain encoded, the
-- candidate table exhausted, and abc read as frame-relativity in the wild.
assert_standard_axioms CIRISOntology.Core.abc_repairability_is_frame_relative
assert_standard_axioms CIRISOntology.Core.circumstances_asserts_nothing
assert_standard_axioms CIRISOntology.Core.confrontations_constructed
assert_standard_axioms CIRISOntology.Core.only_the_record_entry_carries_a_frame
assert_standard_axioms CIRISOntology.Core.record_entry_has_frame
assert_standard_axioms CIRISOntology.Core.stake_is_the_reading
assert_standard_axioms CIRISOntology.Core.domains_encoded
assert_standard_axioms CIRISOntology.Core.every_domain_encoded
assert_standard_axioms CIRISOntology.Core.chemistry_present
assert_standard_axioms CIRISOntology.Core.candidate_table_exhausted
assert_standard_axioms CIRISOntology.Core.kinds_not_reached

-- Core.Scan — THE FORCE BUDGET: which kinds an illocutionary budget buys, the
-- 7 -> 10 -> 11 chain, and why the three-force scan is terminal rather than
-- merely largest-so-far.
assert_standard_axioms CIRISOntology.Core.Force.mem_all
assert_standard_axioms CIRISOntology.Core.carriers_are_the_neutral_sites
assert_standard_axioms CIRISOntology.Core.site_all_nodup
assert_standard_axioms CIRISOntology.Core.scan_nodup
assert_standard_axioms CIRISOntology.Core.scan_assertive
assert_standard_axioms CIRISOntology.Core.scan_assertive_card
assert_standard_axioms CIRISOntology.Core.scan_assertive_directive
assert_standard_axioms CIRISOntology.Core.scan_assertive_directive_card
assert_standard_axioms CIRISOntology.Core.scan_full
assert_standard_axioms CIRISOntology.Core.scan_full_card
assert_standard_axioms CIRISOntology.Core.scan_full_card_eq_basePlane
assert_standard_axioms CIRISOntology.Core.scan_full_is_basePlane
assert_standard_axioms CIRISOntology.Core.record_in_no_scan
assert_standard_axioms CIRISOntology.Core.availableSites_mono
assert_standard_axioms CIRISOntology.Core.scan_mono
assert_standard_axioms CIRISOntology.Core.scan_le_full
assert_standard_axioms CIRISOntology.Core.availableSites_univ
assert_standard_axioms CIRISOntology.Core.scan_terminal
assert_standard_axioms CIRISOntology.Core.scan_terminal_card
assert_standard_axioms CIRISOntology.Core.scan_lattice
assert_standard_axioms CIRISOntology.Core.carriers_survive_everything
assert_standard_axioms CIRISOntology.Core.scan_floor
assert_standard_axioms CIRISOntology.Core.carriers_in_every_scan
assert_standard_axioms CIRISOntology.Core.scanAlt_chain_agrees
assert_standard_axioms CIRISOntology.Core.scanAlt_floor
assert_standard_axioms CIRISOntology.Core.scanAlt_directive_only

-- Core.Stack — the grounding stack: four rungs, injective into the site model,
-- climbing by one and stopping at a fixed point rather than an infinite ladder.
assert_standard_axioms CIRISOntology.Core.stack_card
assert_standard_axioms CIRISOntology.Core.every_rung_listed
assert_standard_axioms CIRISOntology.Core.stack_kinds
assert_standard_axioms CIRISOntology.Core.stack_plain
assert_standard_axioms CIRISOntology.Core.rung_kind_injective
assert_standard_axioms CIRISOntology.Core.rung_site_injective
assert_standard_axioms CIRISOntology.Core.four_sites_in_stack
assert_standard_axioms CIRISOntology.Core.seven_sites_outside_stack
assert_standard_axioms CIRISOntology.Core.rung_site_inStack
assert_standard_axioms CIRISOntology.Core.ground_climbs
assert_standard_axioms CIRISOntology.Core.ground_moves
assert_standard_axioms CIRISOntology.Core.top_is_maximal
assert_standard_axioms CIRISOntology.Core.ground_top_fixed
assert_standard_axioms CIRISOntology.Core.modulate_const
assert_standard_axioms CIRISOntology.Core.modulate_site
assert_standard_axioms CIRISOntology.Core.modulate_top
assert_standard_axioms CIRISOntology.Core.modulate_idempotent
assert_standard_axioms CIRISOntology.Core.modulate_nested
assert_standard_axioms CIRISOntology.Core.modulate_eq_climb
assert_standard_axioms CIRISOntology.Core.ground_three
assert_standard_axioms CIRISOntology.Core.ground_reaches_top
assert_standard_axioms CIRISOntology.Core.ground_terminal
assert_standard_axioms CIRISOntology.Core.iterate_site_in_stack
assert_standard_axioms CIRISOntology.Core.iterate_site_is_one_of_four
assert_standard_axioms CIRISOntology.Core.terminal_kind

-- (2b) THE ENUMERATION GATE. Everything above this line is a hand-maintained
--      list, and a hand-maintained list is exactly the kind of check that goes
--      quietly stale: six modules had been added to the library without ever
--      being named here, so their theorems were shipping unaudited while the
--      file above still passed. This gate asks the ENVIRONMENT which theorems
--      the library declares rather than asking a list, so a module added
--      tomorrow is covered whether or not anyone remembers to write it down.
--      It subsumes both tests above — `sorryAx` is simply one more axiom
--      outside the standard three — and it covers private and compiler-
--      generated declarations, which no hand-written list ever will.
--
--      The traversal is done ONCE with a shared visited set. `collectAxioms`
--      re-walks the whole transitive closure on every call, which costs
--      minutes across a library this size; one walk costs seconds. The slow
--      per-theorem walk is kept for the FAILURE path only, where it buys the
--      name of the offending theorem and runs only when the gate has already
--      fired.
run_cmd do
  let env ← getEnv
  let mods := env.header.moduleNames
  let data := env.header.moduleData
  let mut names : Array Name := #[]
  for i in [0:mods.size] do
    let m := mods[i]!
    if m == `CIRISOntology || (`CIRISOntology).isPrefixOf m then
      for c in data[i]!.constNames do
        match env.find? c with
        | some (.thmInfo _) => names := names.push c
        | _ => pure ()
  let act : CollectAxioms.M Unit := names.forM CollectAxioms.collect
  let (_, st) := (act.run env).run {}
  for a in st.axioms do
    unless a == ``propext || a == ``Classical.choice || a == ``Quot.sound do
      for n in names do
        if (← liftCoreM <| collectAxioms n).contains a then
          throwError "AUDIT FAILURE: {n} depends on non-standard axiom {a}"
      throwError "AUDIT FAILURE: this library depends on non-standard axiom {a}"
  logInfo s!"enumeration gate: {names.size} theorems declared by CIRISOntology.*, \
    none admitted, none outside the standard three"

-- (3) EXACT pinning, in both directions. These fail if the dependency set
--     changes at all — including if a theorem becomes *stronger* than recorded.
--     Under-declaring a dependency and over-declaring one are both failures;
--     the published table is regenerated from these, never hand-maintained.

/-- info: 'CIRISOntology.Core.not_computable_from' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.not_computable_from

/-- info: 'CIRISOntology.Core.provenance_line' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.provenance_line

/--
info: 'CIRISOntology.Core.S_pairwise_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_pairwise_identity

/--
info: 'CIRISOntology.Core.pairwise_blind_to_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pairwise_blind_to_parity

/--
info: 'CIRISOntology.Core.third_sees_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.third_sees_parity

/--
info: 'CIRISOntology.Core.third_reading_positive' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.third_reading_positive

/--
info: 'CIRISOntology.Core.total_not_computable_from_corr' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.total_not_computable_from_corr

/--
info: 'CIRISOntology.Core.rent_holds' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.rent_holds

/--
info: 'CIRISOntology.Core.unpaid_decays' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.unpaid_decays

/--
info: 'CIRISOntology.Core.paid_const' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.paid_const

-- Core.Entropy — the entropic-contraction spine. Every result stops at the
-- standard three; nothing here mints an axiom or leans on native_decide.

/--
info: 'CIRISOntology.Core.trace_eq_sum_eigenvalues' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.trace_eq_sum_eigenvalues

/--
info: 'CIRISOntology.Core.neg_log_det_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.neg_log_det_nonneg

/--
info: 'CIRISOntology.Core.S_pairwise_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_pairwise_nonneg

/--
info: 'CIRISOntology.Core.neg_log_det_eq_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.neg_log_det_eq_zero_iff

/--
info: 'CIRISOntology.Core.hadamard_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.hadamard_posSemidef

/--
info: 'CIRISOntology.Core.IsUnitDiag.hadamard' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.IsUnitDiag.hadamard

/--
info: 'CIRISOntology.Core.oppenheim_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.oppenheim_two

/--
info: 'CIRISOntology.Core.S_pairwise_hadamard_le_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_pairwise_hadamard_le_two

/--
info: 'CIRISOntology.Core.neg_log_det_hadamard_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.neg_log_det_hadamard_nonneg

/--
info: 'CIRISOntology.Core.one_le_det_one_add_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.one_le_det_one_add_posSemidef

/--
info: 'CIRISOntology.Core.det_le_det_add_of_posDef_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.det_le_det_add_of_posDef_posSemidef

/--
info: 'CIRISOntology.Core.posSemidef_det_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posSemidef_det_nonneg

/--
info: 'CIRISOntology.Core.posDef_of_posSemidef_det_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posDef_of_posSemidef_det_pos

/--
info: 'CIRISOntology.Core.det_le_det_add_of_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.det_le_det_add_of_posSemidef

/--
info: 'CIRISOntology.Core.hadamard_fromBlocks' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.hadamard_fromBlocks

/--
info: 'CIRISOntology.Core.hadamard_vecMulVec' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.hadamard_vecMulVec

/--
info: 'CIRISOntology.Core.submatrix_hadamard' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.submatrix_hadamard

/--
info: 'CIRISOntology.Core.posSemidef_vecMulVec' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posSemidef_vecMulVec

/--
info: 'CIRISOntology.Core.schur_hadamard_identity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.schur_hadamard_identity

/--
info: 'CIRISOntology.Core.schur_oneScalar' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.schur_oneScalar

/--
info: 'CIRISOntology.Core.posDef_diag_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posDef_diag_pos

/--
info: 'CIRISOntology.Core.det_schur_reduce' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.det_schur_reduce

/--
info: 'CIRISOntology.Core.posSemidef_smul' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posSemidef_smul

/--
info: 'CIRISOntology.Core.isHermitian_hadamard' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isHermitian_hadamard

/--
info: 'CIRISOntology.Core.posDef_fin_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.posDef_fin_one

/--
info: 'CIRISOntology.Core.schur_posSemidef' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.schur_posSemidef

/--
info: 'CIRISOntology.Core.oppenheim_det' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.oppenheim_det

/--
info: 'CIRISOntology.Core.S_pairwise_hadamard_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_pairwise_hadamard_le

-- Core.OppenheimRCLike — the complex-general Oppenheim (headline).
/--
info: 'CIRISOntology.Core.Herm.oppenheim_det' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Herm.oppenheim_det

/--
info: 'CIRISOntology.Core.Herm.oppenheim_prod' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Herm.oppenheim_prod

-- Core.Flavor — the Jarlskog CP-violation cap (cp-cap witnesses).
/--
info: 'CIRISOntology.Core.jarlskogMax_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.jarlskogMax_nonneg

/--
info: 'CIRISOntology.Core.abs_jarlskog_le_max' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.abs_jarlskog_le_max

/--
info: 'CIRISOntology.Core.jarlskogMax_zero_at_no_mixing' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.jarlskogMax_zero_at_no_mixing

/--
info: 'CIRISOntology.Core.jarlskogMax_zero_at_max_13mixing' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.jarlskogMax_zero_at_max_13mixing

-- Core.FlavorBridge — the flavour bridge (Jarlskog coordinate = whole-only share).
/--
info: 'CIRISOntology.Core.parityChar_signFlip' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.parityChar_signFlip

/--
info: 'CIRISOntology.Core.cpState_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_isProb

/--
info: 'CIRISOntology.Core.cpState_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_zero

/--
info: 'CIRISOntology.Core.cpState_neg_eq_signFlip' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_neg_eq_signFlip

/--
info: 'CIRISOntology.Core.symmetrize_cpState' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.symmetrize_cpState

/--
info: 'CIRISOntology.Core.cpState_signSymmetric_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_signSymmetric_iff

/--
info: 'CIRISOntology.Core.cp_phase_invisible_to_pairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cp_phase_invisible_to_pairs

/--
info: 'CIRISOntology.Core.cpState_corr_eq_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_corr_eq_one

/--
info: 'CIRISOntology.Core.cpShare_neg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_neg

/--
info: 'CIRISOntology.Core.cpShare_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_zero

/--
info: 'CIRISOntology.Core.entropy_cpState' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_cpState

/--
info: 'CIRISOntology.Core.share_cpState' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpState

/--
info: 'CIRISOntology.Core.cpShare_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_nonneg

/--
info: 'CIRISOntology.Core.cpShare_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_pos

/--
info: 'CIRISOntology.Core.share_zero_of_cp_even' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_zero_of_cp_even

/--
info: 'CIRISOntology.Core.share_pos_of_cp_odd' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_pos_of_cp_odd

/--
info: 'CIRISOntology.Core.share_cpState_eq_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpState_eq_zero_iff

/--
info: 'CIRISOntology.Core.share_symmetrize_cpState' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_symmetrize_cpState

/--
info: 'CIRISOntology.Core.mul_log_convex' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.mul_log_convex

/--
info: 'CIRISOntology.Core.entropy_concave' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_concave

/--
info: 'CIRISOntology.Core.cpState_mix' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_mix

/--
info: 'CIRISOntology.Core.cpShare_mul_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_mul_le

/--
info: 'CIRISOntology.Core.abs_jarlskog_le_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.abs_jarlskog_le_one

/--
info: 'CIRISOntology.Core.abs_jarlskogMax_le_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.abs_jarlskogMax_le_one

/--
info: 'CIRISOntology.Core.share_cpFamily_le_phase' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_le_phase

/--
info: 'CIRISOntology.Core.share_cpFamily_le_jarlskogMax' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_le_jarlskogMax

/--
info: 'CIRISOntology.Core.share_cpFamily_zero_of_cp_even' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_zero_of_cp_even

/--
info: 'CIRISOntology.Core.cpFamily_signSymmetric_of_cp_even' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpFamily_signSymmetric_of_cp_even

/--
info: 'CIRISOntology.Core.share_cpFamily_zero_at_no_mixing' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_zero_at_no_mixing

/--
info: 'CIRISOntology.Core.share_cpFamily_zero_at_max_13mixing' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_zero_at_max_13mixing

/--
info: 'CIRISOntology.Core.share_cpFamily_pos' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_pos

/--
info: 'CIRISOntology.Core.share_cpFamily_eq_zero_iff' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpFamily_eq_zero_iff

/--
info: 'CIRISOntology.Core.cpShare_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpShare_one

/--
info: 'CIRISOntology.Core.share_cpState_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_cpState_one

/--
info: 'CIRISOntology.Core.cpState_neg_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.cpState_neg_one

/--
info: 'CIRISOntology.Core.share_parity_eq_cpShare' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_parity_eq_cpShare


-- Core.Intensive — the intensive (per-unit) limit `S/k → −ln(1−ρ)`.
/--
info: 'CIRISOntology.Core.Sfun_div_k_tendsto' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Sfun_div_k_tendsto

-- Core.Third — relabeling-invariance of the total-dependence instrument.
/--
info: 'CIRISOntology.Core.S_total_relabel_fst' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_relabel_fst

-- Core.Temporal — the temporal reading: parity across three times is
-- unrealizable by any memoryless process and exactly realized with one
-- remembered bit.
/--
info: 'CIRISOntology.Core.parity_needs_memory' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.parity_needs_memory

/--
info: 'CIRISOntology.Core.memory_realizes_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.memory_realizes_parity

/--
info: 'CIRISOntology.Core.memory_realizer_is_probability' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.memory_realizer_is_probability

/--
info: 'CIRISOntology.Core.temporal_logos_is_memory' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.temporal_logos_is_memory

-- Core.Share — the whole-only share, defined on the state itself: the Gibbs
-- bound makes the pair envelope honest, and the parity state's share is
-- exactly one bit.
/--
info: 'CIRISOntology.Core.entropy_le_log_card' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_le_log_card

/--
info: 'CIRISOntology.Core.entropy_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_nonneg

/--
info: 'CIRISOntology.Core.pairEnvelope_bddAbove' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pairEnvelope_bddAbove

/--
info: 'CIRISOntology.Core.share_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_nonneg

/--
info: 'CIRISOntology.Core.share_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_parity

/--
info: 'CIRISOntology.Core.share_parity_positive' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_parity_positive

/--
info: 'CIRISOntology.Core.entropy_grouping' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_grouping

/--
info: 'CIRISOntology.Core.share_copied' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_copied

/--
info: 'CIRISOntology.Core.S_total_copied' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_copied

/--
info: 'CIRISOntology.Core.S_total_copied_positive' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_copied_positive

-- Core.ShareQuantum — the quantum lift: von Neumann entropy through the
-- eigenvalue distribution, the quantum Gibbs bound, the diagonal bridge,
-- and the exhibited state's share surviving the lift unchanged.
/--
info: 'CIRISOntology.Core.trace_eq_sum_eigenvalues_rclike' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.trace_eq_sum_eigenvalues_rclike

/--
info: 'CIRISOntology.Core.vnEntropy_le_log_card' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_le_log_card

/--
info: 'CIRISOntology.Core.vnEntropy_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_nonneg

/--
info: 'CIRISOntology.Core.qPairEnvelope_bddAbove' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qPairEnvelope_bddAbove

/--
info: 'CIRISOntology.Core.qShare_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShare_nonneg

/--
info: 'CIRISOntology.Core.isDensity_diagEmbed' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isDensity_diagEmbed

/--
info: 'CIRISOntology.Core.vnEntropy_diagEmbed' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_diagEmbed

/--
info: 'CIRISOntology.Core.ptr₁₂_diagEmbed' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.ptr₁₂_diagEmbed

/--
info: 'CIRISOntology.Core.qShare_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShare_parity

/--
info: 'CIRISOntology.Core.qShare_eq_share_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShare_eq_share_parity

-- Core.EntropyIneq — quantum entropy inequalities from two tricks:
-- pinching, subadditivity, complementary spectra, Araki-Lieb, and the
-- causal bound that makes the temporal no-go a theorem.
/--
info: 'CIRISOntology.Core.mul_log_jensen' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.mul_log_jensen

/--
info: 'CIRISOntology.Core.vnEntropy_conj_unitary' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_conj_unitary

/--
info: 'CIRISOntology.Core.vnEntropy_le_entropy_diagRe' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_le_entropy_diagRe

/--
info: 'CIRISOntology.Core.entropy_grouping₂' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_grouping₂

/--
info: 'CIRISOntology.Core.vnEntropy_subadd' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_subadd

/--
info: 'CIRISOntology.Core.vnEntropy_ptr_complementary' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_ptr_complementary

/--
info: 'CIRISOntology.Core.vnEntropy_triangle' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_triangle

/--
info: 'CIRISOntology.Core.vnEntropy_causal_past' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_causal_past


-- Core.ShareK — the k-slot share and the classical cap: coarse-graining
-- never raises classical entropy, so a classical k-slot state with a
-- uniform pair marginal has share at most (k − 2)·log 2. The Bell bound
-- the hardware experiment is staked against, proved before any data.
/--
info: 'CIRISOntology.Core.entropy_map_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_map_le

/--
info: 'CIRISOntology.Core.shareK_le_log_sub_pair' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.shareK_le_log_sub_pair

/--
info: 'CIRISOntology.Core.shareK_le_of_pair_uniform' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.shareK_le_of_pair_uniform

/--
info: 'CIRISOntology.Core.qPairEnvelopeK_bddAbove' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qPairEnvelopeK_bddAbove

/--
info: 'CIRISOntology.Core.qShareK_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShareK_nonneg

/--
info: 'CIRISOntology.Core.qShareK_le_log_card' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShareK_le_log_card

-- The classical third in time, complete: parity saturates the 3-slot cap.
/--
info: 'CIRISOntology.Core.pushforward_pair_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pushforward_pair_parity

/--
info: 'CIRISOntology.Core.share_le_log_sub_pair₃' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_le_log_sub_pair₃

/--
info: 'CIRISOntology.Core.temporal_third_saturates' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.temporal_third_saturates

-- Core.BellCeiling — the five-qubit ring state: pure, all ten pair traces
-- maximally mixed, share exactly 5 log 2 — above the machine-checked cap.
/--
info: 'CIRISOntology.Core.isDensity_PsiC5' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isDensity_PsiC5

/--
info: 'CIRISOntology.Core.vnEntropy_PsiC5' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.vnEntropy_PsiC5

/--
info: 'CIRISOntology.Core.pairPtr_PsiC5' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pairPtr_PsiC5

/--
info: 'CIRISOntology.Core.bell_ceiling' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bell_ceiling

/--
info: 'CIRISOntology.Core.bell_ceiling_exceeds_cap' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bell_ceiling_exceeds_cap

/--
info: 'CIRISOntology.Core.qShareK_max_five' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.qShareK_max_five

-- Core.HammingCap — pair-uniformity forces three bits of entropy onto any
-- four-bit state (the Hamming bound, via the collision probability), so the
-- classical cap drops a full bit from four slots up.
/--
info: 'CIRISOntology.Core.kern_eq' does not depend on any axioms
-/
#guard_msgs in
#print axioms CIRISOntology.Core.kern_eq

/--
info: 'CIRISOntology.Core.kern_real' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.kern_real

/--
info: 'CIRISOntology.Core.inversion' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.inversion

/--
info: 'CIRISOntology.Core.sum_sq_le_eighth' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.sum_sq_le_eighth

/--
info: 'CIRISOntology.Core.entropy_ge_three_log_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_ge_three_log_two

/--
info: 'CIRISOntology.Core.shareK_le_of_pair_uniform_four' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.shareK_le_of_pair_uniform_four

/--
info: 'CIRISOntology.Core.shareK_le_of_pair_uniform_ge_four' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.shareK_le_of_pair_uniform_ge_four

/--
info: 'CIRISOntology.Core.shareK_le_of_four_pair_uniform' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.shareK_le_of_four_pair_uniform

/--
info: 'CIRISOntology.Core.entropy_ge_of_sum_sq_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_ge_of_sum_sq_le

-- Core.SignSymmetry — a state invariant under the GLOBAL sign flip has
-- whole-only share exactly zero, at any correlation strength. The place not to
-- look: every zero-field Ising model is sign-symmetric at every temperature,
-- criticality included. The edge is exhibited both ways — `parity` is sign-odd
-- (so `share_parity = log 2` stands), and `ferro` is maximally pair-correlated
-- yet sign-symmetric (so the zero is not an absence of order).
/--
info: 'CIRISOntology.Core.sum_comp_signFlip' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.sum_comp_signFlip

/--
info: 'CIRISOntology.Core.symmetrize_signSymmetric' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.symmetrize_signSymmetric

/--
info: 'CIRISOntology.Core.symmetrize_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.symmetrize_isProb

/--
info: 'CIRISOntology.Core.entropy_le_symmetrize' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_le_symmetrize

/--
info: 'CIRISOntology.Core.samePairs_symmetrize' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.samePairs_symmetrize

/--
info: 'CIRISOntology.Core.eq_of_signSymmetric_of_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.eq_of_signSymmetric_of_samePairs

/--
info: 'CIRISOntology.Core.share_eq_zero_of_signSymmetric' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_eq_zero_of_signSymmetric

/--
info: 'CIRISOntology.Core.share_indep' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_indep

/--
info: 'CIRISOntology.Core.ferro_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.ferro_isProb

/--
info: 'CIRISOntology.Core.ferro_signSymmetric' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.ferro_signSymmetric

/--
info: 'CIRISOntology.Core.share_ferro' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_ferro

/--
info: 'CIRISOntology.Core.S_total_ferro' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_ferro

/--
info: 'CIRISOntology.Core.parity_not_signSymmetric' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.parity_not_signSymmetric

-- Core.Creation — the one-step minting, its price in entropy, and the
-- no-creation half for per-cell maps.

/-- info: 'CIRISOntology.Core.parityRepair_idempotent' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.parityRepair_idempotent

/-- info: 'CIRISOntology.Core.parityRepair_fixed_iff' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.parityRepair_fixed_iff

/-- info: 'CIRISOntology.Core.majority_eq' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.majority_eq

/-- info: 'CIRISOntology.Core.majorityRepair_idempotent' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.majorityRepair_idempotent

/-- info: 'CIRISOntology.Core.majorityRepair_fixed_iff' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.majorityRepair_fixed_iff

/--
info: 'CIRISOntology.Core.pushforward_equiv' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pushforward_equiv

/--
info: 'CIRISOntology.Core.pushforward_parityRepair_indep' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pushforward_parityRepair_indep

/--
info: 'CIRISOntology.Core.repair_creates_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.repair_creates_parity

/--
info: 'CIRISOntology.Core.repair_mints_from_noise' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.repair_mints_from_noise

/--
info: 'CIRISOntology.Core.S_total_parityRepair' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_parityRepair

/--
info: 'CIRISOntology.Core.parityRepair_pays_one_bit' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.parityRepair_pays_one_bit

/--
info: 'CIRISOntology.Core.pushforward_majorityRepair_indep' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pushforward_majorityRepair_indep

/--
info: 'CIRISOntology.Core.repair_creates_ferro' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.repair_creates_ferro

/--
info: 'CIRISOntology.Core.S_total_majorityRepair' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.S_total_majorityRepair

/--
info: 'CIRISOntology.Core.majorityRepair_pays_two_bits' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.majorityRepair_pays_two_bits

/-- info: 'CIRISOntology.Core.parityRepair_not_percell' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.parityRepair_not_percell

/-- info: 'CIRISOntology.Core.majorityRepair_not_percell' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.majorityRepair_not_percell

/--
info: 'CIRISOntology.Core.entropy_reindex' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_reindex

/--
info: 'CIRISOntology.Core.entropy_reidx' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_reidx

/--
info: 'CIRISOntology.Core.isProb_reidx' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isProb_reidx

/--
info: 'CIRISOntology.Core.samePairs_reidx' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.samePairs_reidx

/--
info: 'CIRISOntology.Core.pairEnvelope_reidx' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.pairEnvelope_reidx

/--
info: 'CIRISOntology.Core.share_reidx' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_reidx

/--
info: 'CIRISOntology.Core.bool_bijective_of_ne' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bool_bijective_of_ne

/-- info: 'CIRISOntology.Core.bool_const_of_eq' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.bool_const_of_eq

/--
info: 'CIRISOntology.Core.share_pushforward_percell_of_bijective' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_pushforward_percell_of_bijective

/--
info: 'CIRISOntology.Core.entropy_grouping₂₃' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_grouping₂₃

/--
info: 'CIRISOntology.Core.entropy_grouping₁₃' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_grouping₁₃

/--
info: 'CIRISOntology.Core.marg₁_of_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁_of_samePairs

/--
info: 'CIRISOntology.Core.marg₂_of_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂_of_samePairs

/--
info: 'CIRISOntology.Core.marg₃_of_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_of_samePairs

/--
info: 'CIRISOntology.Core.entropy_point_mass' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_point_mass

/--
info: 'CIRISOntology.Core.share_eq_zero_of_entropy_maximal' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_eq_zero_of_entropy_maximal

/--
info: 'CIRISOntology.Core.share_eq_zero_of_third_det' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_eq_zero_of_third_det

/--
info: 'CIRISOntology.Core.share_eq_zero_of_first_det' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_eq_zero_of_first_det

/--
info: 'CIRISOntology.Core.share_eq_zero_of_second_det' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_eq_zero_of_second_det

/--
info: 'CIRISOntology.Core.share_pushforward_percell_of_const₁' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_pushforward_percell_of_const₁

/--
info: 'CIRISOntology.Core.share_pushforward_percell_of_const₂' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_pushforward_percell_of_const₂

/--
info: 'CIRISOntology.Core.share_pushforward_percell_of_const₃' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_pushforward_percell_of_const₃

/--
info: 'CIRISOntology.Core.percell_no_creation' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.percell_no_creation

-- Core.Valve — the one-way valve: up, never down, never from nothing.

/--
info: 'CIRISOntology.Core.push1_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.push1_isProb

/--
info: 'CIRISOntology.Core.channel3_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.channel3_isProb

/--
info: 'CIRISOntology.Core.channel3_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.channel3_prod3

/--
info: 'CIRISOntology.Core.isProb_prod2' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isProb_prod2

/--
info: 'CIRISOntology.Core.prod3_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.prod3_isProb

/--
info: 'CIRISOntology.Core.entropy_prod2' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_prod2

/--
info: 'CIRISOntology.Core.entropy_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_prod3

/--
info: 'CIRISOntology.Core.marg₁₂_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₂_prod3

/--
info: 'CIRISOntology.Core.marg₃_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_prod3

/--
info: 'CIRISOntology.Core.share_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_prod3

/--
info: 'CIRISOntology.Core.valve_from_nothing' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_from_nothing

/--
info: 'CIRISOntology.Core.unifBool_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.unifBool_isProb

/--
info: 'CIRISOntology.Core.indep_eq_prod3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.indep_eq_prod3

/--
info: 'CIRISOntology.Core.valve_from_nothing_indep' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_from_nothing_indep

/--
info: 'CIRISOntology.Core.marg₁₂_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₂_channel3

/--
info: 'CIRISOntology.Core.marg₁₃_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₃_channel3

/--
info: 'CIRISOntology.Core.marg₂₃_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂₃_channel3

/--
info: 'CIRISOntology.Core.marg₁₂_channel3_of_prod' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₂_channel3_of_prod

/--
info: 'CIRISOntology.Core.marg₁₃_channel3_of_prod' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₃_channel3_of_prod

/--
info: 'CIRISOntology.Core.marg₂₃_channel3_of_prod' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂₃_channel3_of_prod

/--
info: 'CIRISOntology.Core.marg₁_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁_channel3

/--
info: 'CIRISOntology.Core.marg₂_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂_channel3

/--
info: 'CIRISOntology.Core.marg₃_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_channel3

/--
info: 'CIRISOntology.Core.marg₁₂_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₂_parity

/--
info: 'CIRISOntology.Core.marg₁₃_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁₃_parity

/--
info: 'CIRISOntology.Core.marg₂₃_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂₃_parity

/--
info: 'CIRISOntology.Core.marg₁_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₁_parity

/--
info: 'CIRISOntology.Core.marg₂_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₂_parity

/--
info: 'CIRISOntology.Core.marg₃_parity' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_parity

/--
info: 'CIRISOntology.Core.valve_no_downward_12' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_no_downward_12

/--
info: 'CIRISOntology.Core.valve_no_downward_13' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_no_downward_13

/--
info: 'CIRISOntology.Core.valve_no_downward_23' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_no_downward_23

/--
info: 'CIRISOntology.Core.valve_no_downward' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_no_downward

/--
info: 'CIRISOntology.Core.damp_isKernel' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.damp_isKernel

/--
info: 'CIRISOntology.Core.channel3_damp_ferro' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.channel3_damp_ferro

/--
info: 'CIRISOntology.Core.bulge_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bulge_isProb

/--
info: 'CIRISOntology.Core.bulgeWitness_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bulgeWitness_isProb

/--
info: 'CIRISOntology.Core.bulgeWitness_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.bulgeWitness_samePairs

/--
info: 'CIRISOntology.Core.entropy_bulge' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_bulge

/--
info: 'CIRISOntology.Core.entropy_bulgeWitness' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_bulgeWitness

/--
info: 'CIRISOntology.Core.entropy_bulge_lt_bulgeWitness' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_bulge_lt_bulgeWitness

/--
info: 'CIRISOntology.Core.valve_upward' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_upward

/--
info: 'CIRISOntology.Core.valve_upward_bound' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_upward_bound

/--
info: 'CIRISOntology.Core.valve_upward_strict' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_upward_strict

/--
info: 'CIRISOntology.Core.stochastic_percell_can_create' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.stochastic_percell_can_create

-- Core.Valve, the pump: the upward flow requires an asymmetric channel.

/--
info: 'CIRISOntology.Core.isFlipCovariant_of_symm' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.isFlipCovariant_of_symm

/--
info: 'CIRISOntology.Core.signSymmetric_channel3' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.signSymmetric_channel3

/--
info: 'CIRISOntology.Core.valve_needs_asymmetry' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_needs_asymmetry

/--
info: 'CIRISOntology.Core.valve_needs_asymmetry_ferro' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.valve_needs_asymmetry_ferro

/--
info: 'CIRISOntology.Core.damp_not_flipCovariant' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.damp_not_flipCovariant

-- Core.ThirdCap — THE DENOMINATOR: log 2 is the EXACT maximum of the whole-only
-- share on three binary slots. share_parity gives attainment; share_le_log_two
-- gives the cap with NO hypothesis on the pair marginals — the gap the Planck
-- pilot's provenance audit found. share_le_pair_third_gap and
-- share_le_grouping_gaps are the sharp data-computable forms.

/--
info: 'CIRISOntology.Core.entropy_marg₁₂_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.entropy_marg₁₂_le

/--
info: 'CIRISOntology.Core.marg₃_eq_of_samePairs' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_eq_of_samePairs

/--
info: 'CIRISOntology.Core.marg₃_isProb' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.marg₃_isProb

/--
info: 'CIRISOntology.Core.share_le_pair_third_gap' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_le_pair_third_gap

/--
info: 'CIRISOntology.Core.share_le_log_card_third' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_le_log_card_third

/--
info: 'CIRISOntology.Core.share_le_log_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_le_log_two

/--
info: 'CIRISOntology.Core.share_max_eq_log_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_max_eq_log_two

/--
info: 'CIRISOntology.Core.share_le_grouping_gaps' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.share_le_grouping_gaps

-- (3b) THE AXIOM-FREE FLOOR, pinned. Every theorem below was proved through
--      `simp`, `decide` or a Mathlib list lemma at some point, and every one of
--      those routes silently costs `propext` — `List` membership decides via
--      `decidable_of_iff`, and `simp` rewrites propositions by extensionality.
--      Each is now proved from constructors and case analysis instead, and
--      depends on NOTHING: not choice, not extensionality, not quotients. That
--      is a property of the PROOFS, not of the statements, so nothing but a pin
--      protects it — a later `simp` would restore the axiom and no other gate
--      in this file would notice. These pins are bidirectional like the rest:
--      they fail the moment a dependency appears.

/-- info: 'CIRISOntology.Core.no_label_moves_with_both' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.no_label_moves_with_both

/-- info: 'CIRISOntology.Core.marker_matches_disposition' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.marker_matches_disposition

/-- info: 'CIRISOntology.Core.binding_never_varies' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.binding_never_varies

/-- info: 'CIRISOntology.Core.repairability_not_intrinsic' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.repairability_not_intrinsic

/-- info: 'CIRISOntology.Core.repairable_not_frameInvariant' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.repairable_not_frameInvariant

/-- info: 'CIRISOntology.Core.repairable_does_not_factor' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.repairable_does_not_factor

/-- info: 'CIRISOntology.Core.self_declared_frame_undetermined' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.self_declared_frame_undetermined

/-- info: 'CIRISOntology.Core.testimonial_has_corpus' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.testimonial_has_corpus

/-- info: 'CIRISOntology.Core.every_site_classified' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.every_site_classified

/-- info: 'CIRISOntology.Core.generator_injective' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.generator_injective

/-- info: 'CIRISOntology.Core.record_not_site_generated' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.record_not_site_generated

/-- info: 'CIRISOntology.Core.reading_record_has_frame' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.reading_record_has_frame

/-- info: 'CIRISOntology.Core.suite_covers_every_kind' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.suite_covers_every_kind

/-- info: 'CIRISOntology.Core.suite_ships_unvalidated' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.suite_ships_unvalidated

/-- info: 'CIRISOntology.Core.abc_repairability_is_frame_relative' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.abc_repairability_is_frame_relative

/-- info: 'CIRISOntology.Core.record_entry_has_frame' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.record_entry_has_frame

/-- info: 'CIRISOntology.Core.every_domain_encoded' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.every_domain_encoded

/-- info: 'CIRISOntology.Core.chemistry_present' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.chemistry_present

/-- info: 'CIRISOntology.Core.Force.mem_all' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.Force.mem_all

/-- info: 'CIRISOntology.Core.scan_full_is_basePlane' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.scan_full_is_basePlane

/-- info: 'CIRISOntology.Core.record_in_no_scan' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.record_in_no_scan

/-- info: 'CIRISOntology.Core.every_rung_listed' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.every_rung_listed

/-- info: 'CIRISOntology.Core.rung_kind_injective' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.rung_kind_injective

/-- info: 'CIRISOntology.Core.rung_site_injective' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.rung_site_injective

/-- info: 'CIRISOntology.Core.ground_climbs' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.ground_climbs

/-- info: 'CIRISOntology.Core.ground_moves' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.ground_moves

/-- info: 'CIRISOntology.Core.iterate_site_is_one_of_four' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.iterate_site_is_one_of_four




-- (4) The stance is non-empty, claim keys are unique, and every claim carries
--     a falsifier. The `kill` field is non-optional in `Claim`, so "has a kill"
--     is enforced at construction; this checks the stance was not silently
--     emptied, that no key is silently shadowed, and that no kill is a
--     placeholder.
run_cmd do
  let n := CIRISOntology.stance.length
  if n = 0 then throwError "AUDIT FAILURE: the stance is empty"
  let keys := CIRISOntology.stance.map (·.key)
  for k in keys do
    if (keys.filter (· == k)).length > 1 then
      throwError "AUDIT FAILURE: duplicate claim key '{k}'"
  for c in CIRISOntology.stance do
    if c.kill.trim.isEmpty then
      throwError "AUDIT FAILURE: claim '{c.key}' has an empty kill condition"
    if c.plain.trim.isEmpty then
      throwError "AUDIT FAILURE: claim '{c.key}' has no plain-language statement"
  logInfo s!"stance: {n} claims, keys unique, all with a non-empty kill condition"

-- (5) Mechanization honesty. The gates advertised as machine-checked must be
--     exactly those this file actually enforces. If a gate is flipped to
--     `mechanized := true` without a corresponding check here, this fails.
run_cmd do
  let claimed := CIRISOntology.Core.Gate.all.filter (·.mechanized)
  let enforced : List CIRISOntology.Core.Gate :=
    [.noSorry, .axiomAudit]
  if claimed.length ≠ enforced.length then
    throwError "AUDIT FAILURE: {claimed.length} gates advertised as mechanized, \
      but {enforced.length} are actually enforced by this audit"
  for g in claimed do
    unless enforced.contains g do
      throwError "AUDIT FAILURE: gate '{g.title}' is advertised as machine-checked \
        but nothing in this audit enforces it"
  logInfo s!"mechanization claims are truthful: {claimed.length} gates enforced"

-- (6) `proved` is witnessed, not declared. Every claim marked `proved` names
--     the machine-checked declarations that carry it; each witness must exist,
--     be sorry-free, and rest on nothing outside the standard three. The check
--     is bidirectional: a witness on a claim not marked `proved` also fails.
--     (The Equational Theories Project's idea — status backed by the axiom
--     set — applied to the one tier a proof assistant can vouch for. Whether a
--     witness actually formalizes the headline it is attached to remains a
--     human judgment; epistemology.md §4 says so.)
run_cmd do
  for c in CIRISOntology.stance do
    if c.status = .proved then
      if c.witness.isEmpty then
        throwError "AUDIT FAILURE: claim '{c.key}' is marked proved \
          but names no witness declaration"
      for w in c.witness do
        let nm := w.toName
        unless (← getEnv).contains nm do
          throwError "AUDIT FAILURE: witness '{w}' of claim '{c.key}' \
            is not a declaration in this build"
        let axs ← liftCoreM <| collectAxioms nm
        if axs.contains ``sorryAx then
          throwError "AUDIT FAILURE: witness '{w}' of claim '{c.key}' \
            transitively depends on sorryAx"
        for a in axs do
          unless a == ``propext || a == ``Classical.choice || a == ``Quot.sound do
            throwError "AUDIT FAILURE: witness '{w}' of claim '{c.key}' \
              depends on non-standard axiom {a}"
    else
      unless c.witness.isEmpty do
        throwError "AUDIT FAILURE: claim '{c.key}' names a proof witness \
          but is not marked proved"
  logInfo "proved claims are witnessed by machine-checked declarations"

-- (6b) THE RECORD KEEPS ITS DEAD. A claim marked `dead` must say what killed
--      it; no living claim may carry a killedBy. Bidirectional, so a dead claim
--      cannot be quietly resurrected by deleting its epitaph, and a live claim
--      cannot borrow the credibility of having survived something.
run_cmd do
  for c in CIRISOntology.stance do
    if c.status = .dead then
      if c.killedBy.trim.isEmpty then
        throwError "AUDIT FAILURE: claim '{c.key}' is marked dead \
          but does not say what killed it"
    else
      unless c.killedBy.trim.isEmpty do
        throwError "AUDIT FAILURE: claim '{c.key}' records a killer \
          but is not marked dead"
  let n := (CIRISOntology.stance.filter (·.status = .dead)).length
  logInfo s!"the record keeps its dead: {n} claim(s) marked dead, each with its killer"

-- (7) `measured` names its basis. This seed imports no experimental history,
--     so every measured claim must say where its measurement record lives.
--     Bidirectional: a basis on a claim not marked `measured` also fails.
run_cmd do
  for c in CIRISOntology.stance do
    if c.status = .measured then
      if c.basis.trim.isEmpty then
        throwError "AUDIT FAILURE: claim '{c.key}' is marked measured \
          but names no basis (where the measurement record lives)"
    else
      unless c.basis.trim.isEmpty do
        throwError "AUDIT FAILURE: claim '{c.key}' carries a measurement basis \
          but is not marked measured"
  logInfo "measured claims name the record their measurement lives in"

end Gate

-- Generator2 (the freeze-consistency check; T1 primary NULL — see the file header)
/-- info: 'CIRISOntology.Core.generator2_image' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.generator2_image
/-- info: 'CIRISOntology.Core.generator2_injective' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.generator2_injective
/-- info: 'CIRISOntology.Core.record_not_rsite_generated' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.record_not_rsite_generated
/-- info: 'CIRISOntology.Core.generator2_transport' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.generator2_transport
/-- info: 'CIRISOntology.Core.transport_injective' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.transport_injective

-- Interferometer counting (wager bookkeeping; see the file header)
/-- info: 'CIRISOntology.Core.ifo_cycle_rank_45' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.ifo_cycle_rank_45
/-- info: 'CIRISOntology.Core.ifo_phase_count_agrees' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.ifo_phase_count_agrees
/-- info: 'CIRISOntology.Core.ifo_param_count' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.ifo_param_count

-- Pointing (R2 discharged; see `CIRISOntology/Core/Pointing.lean`'s header and
-- OBJECT.md's residue ledger). Pinned exactly because the SPLIT is the content:
-- the discharge — factoring alone forces the constant the pointing merely names
-- — is choice-free, while the vacuity fence buys its case split with classical
-- decidability. If the first three ever acquire `Classical.choice`, something
-- has been proved by a route the derivation does not claim.
/-- info: 'CIRISOntology.Core.Pointing.factors_const_of_residual_eq' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CIRISOntology.Core.Pointing.factors_const_of_residual_eq

/-- info: 'CIRISOntology.Core.Pointing.clean_value_forced' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CIRISOntology.Core.Pointing.clean_value_forced

/-- info: 'CIRISOntology.Core.Pointing.fires_at_pinned_convicts' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CIRISOntology.Core.Pointing.fires_at_pinned_convicts

/--
info: 'CIRISOntology.Core.Pointing.exists_step_with_rest_eq' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Pointing.exists_step_with_rest_eq

-- Habit (the third component of the maximal object; see
-- `CIRISOntology/Core/Habit.lean`'s header). Pinned because the SPLIT is again
-- the content, in three places.
--
--   * The VACUITY FENCE is axiom-FREE. `exists_closed_view` is `⟨T, rfl⟩`: every
--     step map closes a view, so "T closes some view" excludes nothing. A fence
--     that needed axioms would be a fence one could argue with; this one is not.
--     `not_closed_witness` is likewise axiom-free, which is what makes closure a
--     non-vacuous RELATION rather than a universal one.
--   * `cfl_admissible` — the scale/time compatibility condition — is propext
--     only. It is locality ARITHMETIC and claims to be nothing else. If it ever
--     acquires `Classical.choice`, the Habit/View condition has been proved by
--     an analytic route this file does not claim, and the derivation is wrong
--     about what it rests on.
--   * Everything denominated in `Real` carries all three, as `Real` always does.
--     That includes the second law, the H-theorem, and Landauer's counting face.
/-- info: 'CIRISOntology.Core.Habit.exists_closed_view' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.exists_closed_view

/-- info: 'CIRISOntology.Core.Habit.not_closed_witness' does not depend on any axioms -/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.not_closed_witness

/-- info: 'CIRISOntology.Core.Habit.cfl_admissible' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.cfl_admissible

/--
info: 'CIRISOntology.Core.Habit.production_nonneg_of_closed' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_nonneg_of_closed

/--
info: 'CIRISOntology.Core.Habit.production_neg_witness' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_neg_witness

/--
info: 'CIRISOntology.Core.Habit.production_eq_zero_iff_rate_injective' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_eq_zero_iff_rate_injective

/--
info: 'CIRISOntology.Core.Habit.frameEntropy_iterate_mono' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.frameEntropy_iterate_mono

/--
info: 'CIRISOntology.Core.Habit.production_id_eq_log_degree' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_id_eq_log_degree

/--
info: 'CIRISOntology.Core.Habit.injective_of_lipschitz_step' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.injective_of_lipschitz_step

/--
info: 'CIRISOntology.Core.Habit.log_support_drop_eq_production' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.log_support_drop_eq_production

/--
info: 'CIRISOntology.Core.Habit.mint_and_production_differ_on_majority' depends on axioms: [propext,
 Classical.choice,
 Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.mint_and_production_differ_on_majority

/--
info: 'CIRISOntology.Core.Locality.restrict_factors_through_collar' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Locality.restrict_factors_through_collar

-- Habit, the engine-facing pair: the one CONSTITUTIVE producer and its
-- same-type control. `production_pos_of_max_update` models the irreversible
-- damage update (`damage = damage.max(target)`), whose `max` is many-to-one
-- precisely because damage never heals; `production_cycle_zero` runs an
-- INVERTIBLE step on the SAME three-state world and reads exactly zero. A
-- positive production reading is worth nothing without that control, so the two
-- are pinned together and must stay together.
/--
info: 'CIRISOntology.Core.Habit.production_pos_of_max_update' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_pos_of_max_update

/--
info: 'CIRISOntology.Core.Habit.production_cycle_zero' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.production_cycle_zero

-- And both sides of the scale/time condition: at halo two the rate-one habit
-- can be stepped twice, at halo one it cannot (`shift_not_depends_within_one`,
-- below). An admissibility condition that only ever holds is not a condition.
/--
info: 'CIRISOntology.Core.Habit.shift_two_depends_within_two' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.shift_two_depends_within_two

/-- info: 'CIRISOntology.Core.Habit.shift_not_depends_within_one' depends on axioms: [propext, Quot.sound] -/
#guard_msgs in
#print axioms CIRISOntology.Core.Habit.shift_not_depends_within_one

-- Mixing (the contraction row of the fiber ladder; see
-- `CIRISOntology/Core/Mixing.lean`'s header). Pinned as a TRIPLE because the
-- content is the CONTRAST, not either half: the keystone bound, the
-- deterministic 0/1 dichotomy that makes contraction impossible without noise,
-- and the identification of the zero case with `Habit.Closed`. A pin on the
-- bound alone would let the vacuity fence rot; a pin on the witnesses alone
-- would let the theorem rot.
/--
info: 'CIRISOntology.Core.Mixing.defect_le_alpha_pow' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.defect_le_alpha_pow

/--
info: 'CIRISOntology.Core.Mixing.det_defect_zero_or_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.det_defect_zero_or_one

/--
info: 'CIRISOntology.Core.Mixing.det_defect_eq_zero_iff_closed' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.det_defect_eq_zero_iff_closed

-- The two exhibited non-contraction witnesses, pinned together with the noisy
-- corollary that contradicts them: the same first-slot view on the same
-- two-slot world reads defect 1 forever under a deterministic step and at most
-- (1-eps)^m once the step carries noise. Either half alone is quotable in the
-- wrong direction.
/--
info: 'CIRISOntology.Core.Mixing.swap_defect_odd' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.swap_defect_odd

/--
info: 'CIRISOntology.Core.Mixing.copySecond_defect_succ' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.copySecond_defect_succ

/--
info: 'CIRISOntology.Core.Mixing.defect_noisy_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.defect_noisy_le

-- The Dobrushin machinery itself, since Mathlib v4.14 supplies none of it.
/--
info: 'CIRISOntology.Core.Mixing.tv_app_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.tv_app_le

/--
info: 'CIRISOntology.Core.Mixing.alpha_le_one_sub_card_mul' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.Mixing.alpha_le_one_sub_card_mul

-- And the sorry-free bar on the same set.
assert_no_sorry CIRISOntology.Core.Mixing.defect_le_alpha_pow
assert_no_sorry CIRISOntology.Core.Mixing.det_defect_zero_or_one
assert_no_sorry CIRISOntology.Core.Mixing.det_defect_eq_zero_iff_closed
assert_no_sorry CIRISOntology.Core.Mixing.swap_defect_odd
assert_no_sorry CIRISOntology.Core.Mixing.copySecond_defect_succ
assert_no_sorry CIRISOntology.Core.Mixing.defect_noisy_le
assert_no_sorry CIRISOntology.Core.Mixing.tv_app_le
assert_no_sorry CIRISOntology.Core.Mixing.alpha_le_one_sub_card_mul
assert_standard_axioms CIRISOntology.Core.Mixing.defect_le_alpha_pow
assert_standard_axioms CIRISOntology.Core.Mixing.det_defect_zero_or_one
assert_standard_axioms CIRISOntology.Core.Mixing.det_defect_eq_zero_iff_closed
assert_standard_axioms CIRISOntology.Core.Mixing.swap_defect_odd
assert_standard_axioms CIRISOntology.Core.Mixing.copySecond_defect_succ
assert_standard_axioms CIRISOntology.Core.Mixing.defect_noisy_le
assert_standard_axioms CIRISOntology.Core.Mixing.tv_app_le
assert_standard_axioms CIRISOntology.Core.Mixing.alpha_le_one_sub_card_mul

-- MuChannel — R3's successor: relative entropy, the data processing inequality,
-- and the monotone `σ_m = D(p Tᵐ ‖ π)`. Pinned because this is the object
-- `Core/StochasticHabit.lean` named and declined to build; a `sorry` anywhere in
-- it would leave R3's second half open while the header says it is closed.
-- The three-axiom reading is expected: every declaration here is real-valued.
assert_no_sorry CIRISOntology.Core.MuChannel.logSum_le
assert_no_sorry CIRISOntology.Core.MuChannel.klDiv_nonneg
assert_no_sorry CIRISOntology.Core.MuChannel.klDiv_push_le
assert_no_sorry CIRISOntology.Core.MuChannel.sigma_antitone
assert_no_sorry CIRISOntology.Core.MuChannel.sigma_nonneg
assert_standard_axioms CIRISOntology.Core.MuChannel.klDiv_push_le
assert_standard_axioms CIRISOntology.Core.MuChannel.sigma_antitone

/--
info: 'CIRISOntology.Core.MuChannel.logSum_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.logSum_le

/--
info: 'CIRISOntology.Core.MuChannel.klDiv_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.klDiv_nonneg

/--
info: 'CIRISOntology.Core.MuChannel.klDiv_push_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.klDiv_push_le

/--
info: 'CIRISOntology.Core.MuChannel.sigma_succ_le' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.sigma_succ_le

/--
info: 'CIRISOntology.Core.MuChannel.sigma_antitone' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.sigma_antitone

/--
info: 'CIRISOntology.Core.MuChannel.sigma_nonneg' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.sigma_nonneg

-- The reconciliation with `StochasticHabit`'s reset witness, both halves, pinned
-- TOGETHER: the full-support reset satisfies the new monotone from `m = 0` while
-- STILL strictly lowering Shannon entropy (that pairing is the whole point), and
-- the point-mass reset shows the absolute-continuity hypothesis is load-bearing
-- by breaking the monotone when it is dropped. A pin on either half alone would
-- let the other be deleted, and the claim is the pair.
/--
info: 'CIRISOntology.Core.MuChannel.sigma_softReset_antitone' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.sigma_softReset_antitone

/--
info: 'CIRISOntology.Core.MuChannel.softReset_lowers_shannon' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.softReset_lowers_shannon

/--
info: 'CIRISOntology.Core.MuChannel.hardReset_not_absCont' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.hardReset_not_absCont

/--
info: 'CIRISOntology.Core.MuChannel.hardReset_sigma_zero_lt_one' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.hardReset_sigma_zero_lt_one

/--
info: 'CIRISOntology.Core.MuChannel.sigma_softReset_strict_drop' depends on axioms: [propext, Classical.choice, Quot.sound]
-/
#guard_msgs in
#print axioms CIRISOntology.Core.MuChannel.sigma_softReset_strict_drop
