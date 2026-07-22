/-
CIRISOntology.Core.Epistemics — the honesty gates, as machine-readable commitments.

These are the rules by which a claim is allowed to enter the stance. They are
carried here, in the source, rather than in prose alone, so that (a) the CI can
mechanically enforce the subset that is mechanically enforceable, and (b) the
published page can render the whole set in plain language directly from this
file — no hand-maintained copy to drift.

The split is deliberate and is stated on the page: some gates are PROVED or
MECHANIZED (the CI fails the build if they are violated); the rest are RECORDED
COMMITMENTS that a human reviewer must uphold. Pretending a process commitment
is machine-checked would itself violate the gates, so the distinction is a
first-class field (`mechanized`).

See `epistemology.md` for the reasoning behind each gate and the CI recipe.
-/

namespace CIRISOntology.Core

/-- The honesty gates. Enumerable so the published report can render all of them
    without a hand-maintained duplicate. -/
inductive Gate
  /-- Method frozen, in writing, before any result is seen. -/
  | preRegistration
  /-- A claim enters the stance only with its falsifiers named first. -/
  | killsStakedFirst
  /-- Each falsifier kills its own claim and nothing beneath it. -/
  | separableKills
  /-- The null model must match the data's generative structure. -/
  | nullTypeMatch
  /-- Rank statistics must report the tied fraction before they are believed. -/
  | tiedFractionDisclosed
  /-- Finite-sample estimator bias must carry its own control. -/
  | biasControl
  /-- An unexplained residual is never evidence for the hypothesis. -/
  | residualNeverSupport
  /-- A fired kill is reported as plainly as a survival. -/
  | reportTheKill
  /-- A floor reading from a lower-bound instrument is not absence. -/
  | floorIsNotAbsence
  /-- No `sorry` reaches the main branch. -/
  | noSorry
  /-- Declarations depend only on the intended axioms. -/
  | axiomAudit
  deriving DecidableEq, Repr

namespace Gate

/-- All gates, in reporting order. -/
def all : List Gate :=
  [preRegistration, killsStakedFirst, separableKills, nullTypeMatch,
   tiedFractionDisclosed, biasControl, residualNeverSupport, reportTheKill,
   floorIsNotAbsence, noSorry, axiomAudit]

/-- Short title. -/
def title : Gate → String
  | preRegistration       => "Pre-registration"
  | killsStakedFirst      => "Kills staked first"
  | separableKills        => "Separable kills"
  | nullTypeMatch         => "Null-type match"
  | tiedFractionDisclosed => "Tied-fraction disclosure"
  | biasControl           => "Bias control"
  | residualNeverSupport  => "A residual is never support"
  | reportTheKill         => "Report the kill"
  | floorIsNotAbsence     => "A floor is not an absence"
  | noSorry               => "No sorry"
  | axiomAudit            => "Axiom audit"

/-- The rule, in plain language, for a general reader. -/
def plain : Gate → String
  | preRegistration =>
      "Write down exactly how you will measure something, and what each possible answer "
      ++ "would mean, BEFORE you look at any result. Once you have seen the answer you can "
      ++ "no longer choose the method honestly."
  | killsStakedFirst =>
      "Before adopting an idea, say out loud what observation would prove it wrong. An idea "
      ++ "with no way to fail is not a claim about the world."
  | separableKills =>
      "Each way of being wrong should take down only the claim it targets. If one bad result "
      ++ "would destroy everything at once, the ideas were tangled together, not tested."
  | nullTypeMatch =>
      "To know whether a pattern is real, compare it against a fake version of your data that "
      ++ "has no pattern in it. That fake must be built the same WAY your real data is — if the "
      ++ "real data is made of discrete counts, the comparison must be too. A mismatched "
      ++ "comparison is the most common way to fool yourself."
  | tiedFractionDisclosed =>
      "Some methods rank the data before analysing it. If many measurements are tied — for "
      ++ "example, lots of empty bins that are all exactly zero — the ranking has to break "
      ++ "those ties somehow, and that invents structure that was never there. Always report "
      ++ "what fraction was tied, because the false signal grows with it."
  | biasControl =>
      "Any measure of shared structure reads slightly above zero purely from having a limited "
      ++ "amount of data. Shuffle your data to destroy the real structure, measure again, and "
      ++ "subtract that floor."
  | residualNeverSupport =>
      "A leftover that your theory does not explain is not evidence FOR your theory. Support "
      ++ "comes only from a specific prediction made in advance and then confirmed."
  | reportTheKill =>
      "When a test kills your own favourite result, say so as plainly and prominently as you "
      ++ "would have announced a success. The record keeps the dead claim, marked dead."
  | floorIsNotAbsence =>
      "If your instrument is known to be blind to something, its reading zero does not mean "
      ++ "that thing is absent. It means you did not look with an instrument that could see it."
  | noSorry =>
      "In a machine-checked proof, an admitted gap is a hole. No holes reach the published "
      ++ "branch; anything unfinished is named as open rather than quietly assumed."
  | axiomAudit =>
      "Check what each proof actually rests on. A result is only as strong as the assumptions "
      ++ "underneath it, so those assumptions are listed automatically, not from memory."

/-- Is this gate mechanically enforced by CI, or is it a commitment a human
    must uphold? Honesty about this distinction is itself a gate. -/
def mechanized : Gate → Bool
  | noSorry               => true
  | axiomAudit            => true
  | floorIsNotAbsence     => true   -- carried by a proved theorem, not a promise
  | _                     => false

end Gate

/-- The gates, recorded as the standing commitment of this repository. -/
structure HonestyGates where
  /-- Every gate in `Gate.all` is in force for every claim in the stance. -/
  all_gates_in_force : True
  /-- The `mechanized` flag is truthful: no process commitment is advertised as
      machine-checked. CI enforces exactly the gates flagged `true`. -/
  mechanization_claims_are_truthful : True
  /-- Dead claims stay in the record, marked dead, rather than being deleted. -/
  the_record_keeps_its_dead : True

/-- The gates are in force. -/
def honesty_gates : HonestyGates := ⟨trivial, trivial, trivial⟩

end CIRISOntology.Core
