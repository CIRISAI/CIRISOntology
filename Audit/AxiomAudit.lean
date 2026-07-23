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
assert_no_sorry CIRISOntology.Core.rent_holds
assert_no_sorry CIRISOntology.Core.paid_const
assert_no_sorry CIRISOntology.Core.underpaid_shrinks
assert_no_sorry CIRISOntology.Core.unpaid_succ
assert_no_sorry CIRISOntology.Core.unpaid_decays
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
