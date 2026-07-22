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

-- (2) No published theorem rests on anything exotic.
assert_standard_axioms CIRISOntology.Core.S_pairwise_identity
assert_standard_axioms CIRISOntology.Core.not_computable_from
assert_standard_axioms CIRISOntology.Core.provenance_line

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

-- (4) The stance is non-empty and every claim carries a falsifier. The `kill`
--     field is non-optional in `Claim`, so "has a kill" is enforced at
--     construction; this checks the stance was not silently emptied and that no
--     kill is a placeholder.
run_cmd do
  let n := CIRISOntology.stance.length
  if n = 0 then throwError "AUDIT FAILURE: the stance is empty"
  for c in CIRISOntology.stance do
    if c.kill.trim.isEmpty then
      throwError "AUDIT FAILURE: claim '{c.key}' has an empty kill condition"
    if c.plain.trim.isEmpty then
      throwError "AUDIT FAILURE: claim '{c.key}' has no plain-language statement"
  logInfo s!"stance: {n} claims, all with a non-empty kill condition"

-- (5) Mechanization honesty. The gates advertised as machine-checked must be
--     exactly those this file actually enforces. If a gate is flipped to
--     `mechanized := true` without a corresponding check here, this fails.
run_cmd do
  let claimed := CIRISOntology.Core.Gate.all.filter (·.mechanized)
  let enforced : List CIRISOntology.Core.Gate :=
    [.noSorry, .axiomAudit, .floorIsNotAbsence]
  if claimed.length ≠ enforced.length then
    throwError "AUDIT FAILURE: {claimed.length} gates advertised as mechanized, \
      but {enforced.length} are actually enforced by this audit"
  for g in claimed do
    unless enforced.contains g do
      throwError "AUDIT FAILURE: gate '{g.title}' is advertised as machine-checked \
        but nothing in this audit enforces it"
  logInfo s!"mechanization claims are truthful: {claimed.length} gates enforced"

end Gate
