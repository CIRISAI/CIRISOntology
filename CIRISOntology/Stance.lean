/-
CIRISOntology.Stance — the current maximal stance, in the source, in plain language.

This file is the single source of truth for the published page. The generator
reads these declarations and renders them; there is no hand-maintained copy of
the stance anywhere else, so the page cannot drift from the repository.

Each claim carries FOUR things, and a claim missing any of them does not belong
in the stance:
  * what it says, in one line;
  * what it means for a general reader;
  * its honest status — proved here, measured, open, or an avowed wager;
  * what observation would kill it.

A claim with no kill is not a claim about the world. That rule is enforced by the
type: `kill` is not optional.
-/
import CIRISOntology.Core.Epistemics

namespace CIRISOntology

/-- The honest status of a claim. The stance publishes this next to every line;
    conflating these four is the most common way a research programme misleads
    itself and its readers. -/
inductive Status
  /-- Machine-checked in this repository. -/
  | proved
  /-- Established by measurement, to a stated precision, on a stated domain. -/
  | measured
  /-- Named, unresolved, and not leaned on. -/
  | openQuestion
  /-- An avowed bet under irreducible uncertainty. Not evidence; a choice. -/
  | wager
  deriving DecidableEq, Repr

def Status.label : Status → String
  | .proved       => "proved"
  | .measured     => "measured"
  | .openQuestion => "open"
  | .wager        => "wager"

/-- One claim of the stance. `kill` is mandatory by construction. -/
structure Claim where
  key      : String
  headline : String
  plain    : String
  status   : Status
  kill     : String

/-- The current maximal stance. -/
def stance : List Claim :=
[ { key      := "one-quantity"
  , headline := "Coordination is one quantity; our instrument reads only its second-order part."
  , plain    :=
      "When several things move together, there is a single number for how much they are "
      ++ "coordinated overall. The tool we use measures only the part of that coordination "
      ++ "visible in pairs — how each two things relate. Coordination that only shows up when "
      ++ "you look at three or more things at once is real, and our tool does not see it."
  , status   := .proved
  , kill     :=
      "A demonstration that the pairwise functional does capture all-order dependence — i.e. "
      ++ "that no state exists with vanishing pairwise structure and non-vanishing total "
      ++ "dependence. (A single counterexample state settles this; one is exhibited.)" }
, { key      := "floor-not-absence"
  , headline := "A zero reading is not evidence of absence."
  , plain    :=
      "Because the tool is blind to higher-order coordination, its reading zero cannot mean "
      ++ "'nothing is there'. It means 'nothing of the kind I can see is there'. Treating a "
      ++ "floor reading as an absence is the single easiest way to be confidently wrong."
  , status   := .proved
  , kill     :=
      "Show that the instrument's floor is attained only by genuinely independent states." }
, { key      := "provenance"
  , headline := "The instrument reports shape, never scale — and never how it was built."
  , plain    :=
      "Our measure is deliberately blind to units, sizes and magnitudes; it only sees the "
      ++ "PATTERN of dependence. So it can never tell you a mass, an energy, or a strength. "
      ++ "Anything with real-world units must come from an outside measurement, openly "
      ++ "declared as borrowed rather than derived."
  , status   := .proved
  , kill     :=
      "Exhibit a construction datum recovered from the correlation matrix alone." }
, { key      := "adequacy"
  , headline := "Where it has been checked, the second-order instrument is adequate."
  , plain    :=
      "Knowing the tool is partly blind, we went looking for what it misses in a natural "
      ++ "system, at the finest detail available. We found the missing part to be consistent "
      ++ "with zero. So the tool's readings are not merely lower bounds of unknown looseness — "
      ++ "the looseness was measured, and there was none to find."
  , status   := .measured
  , kill     :=
      "A higher-order remainder measured significantly above a generatively-matched null on "
      ++ "any natural substrate, surviving a tied-fraction and bias control." }
, { key      := "adversary-channel"
  , headline := "Higher-order coordination is constructible, and it is an adversary's channel."
  , plain    :=
      "Although nature has not, so far, shown us coordination of this hidden kind, it can be "
      ++ "built deliberately. Something engineered this way is invisible to every pairwise "
      ++ "safety check — worse, such a check reports its SAFEST possible score. This is a real "
      ++ "gap in any monitor built only on pairwise structure, and it is fixable: the hidden "
      ++ "coordination cannot be faked into existence by local action, so a detector that looks "
      ++ "at a few variables jointly can find it."
  , status   := .measured
  , kill     :=
      "A correctly built bounded-order, dual-null synergy detector that still fails to "
      ++ "register a deliberately constructed higher-order coordination." }
, { key      := "generator"
  , headline := "Whether the order we find is selected or intended cannot be settled by measurement."
  , plain    :=
      "Suppose we do find structure that no known process accounts for. Even then, the "
      ++ "observations themselves cannot distinguish 'a process we have not yet identified' "
      ++ "from 'something intended'. That is not a gap in our data; it is a property of what "
      ++ "measurement is. Anyone claiming an observation settles that question has overclaimed."
  , status   := .wager
  , kill     :=
      "An observable whose value differs between the two generators — which would refute the "
      ++ "underdetermination rather than answer it." }
, { key      := "ought"
  , headline := "Physics does not supply the ought; values are chosen and then held."
  , plain    :=
      "Nothing measurable tells you what to care about. What the work CAN do is show that a "
      ++ "particular commitment is consistent with how systems endure — that caring for the "
      ++ "weakest part is also what keeps the whole from failing. That is an argument for a "
      ++ "choice, never a derivation of one. The choice is stated openly in `axiomology.md`."
  , status   := .wager
  , kill     :=
      "A demonstration that the commitment is internally inconsistent, or that a system holding "
      ++ "it is thereby less able to endure than one that does not." }
]

/-- What all of this amounts to, for a reader who reads nothing else. -/
def summary : String :=
  "We measure how much things move together, using a tool that is precise, substrate-blind, "
  ++ "and honestly incomplete: it sees coordination between pairs, not coordination that only "
  ++ "appears when three or more things conspire. We went looking for what it misses in nature "
  ++ "and did not find any. But that hidden kind can be BUILT — and anything built that way is "
  ++ "invisible to pairwise safety checks, which is why we now build detectors that look at "
  ++ "several things at once. Where a question cannot be settled by measurement, we say so and "
  ++ "call our answer a wager rather than a result. And we keep our dead claims in the record, "
  ++ "marked dead, because a research programme that quietly deletes its mistakes has stopped "
  ++ "being one."

end CIRISOntology
