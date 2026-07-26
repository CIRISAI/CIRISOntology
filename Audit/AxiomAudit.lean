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
-- Core.Intensive — the intensive (per-unit) limit.
assert_no_sorry CIRISOntology.Core.Sfun_div_k_tendsto
-- Core.Third — relabeling-invariance of the total-dependence instrument.
assert_no_sorry CIRISOntology.Core.S_total_relabel_fst

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
-- Core.Intensive — the intensive (per-unit) limit.
assert_standard_axioms CIRISOntology.Core.Sfun_div_k_tendsto
-- Core.Third — relabeling-invariance of the total-dependence instrument.
assert_standard_axioms CIRISOntology.Core.S_total_relabel_fst

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

/-- info: 'CIRISOntology.Core.parityRepair_not_percell' depends on axioms: [propext] -/
#guard_msgs in
#print axioms CIRISOntology.Core.parityRepair_not_percell

/-- info: 'CIRISOntology.Core.majorityRepair_not_percell' depends on axioms: [propext] -/
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

/-- info: 'CIRISOntology.Core.bool_const_of_eq' depends on axioms: [propext] -/
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
