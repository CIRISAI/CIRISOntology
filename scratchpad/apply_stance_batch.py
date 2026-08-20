"""Apply the approved stance batch (R1-R7) atomically to Stance.lean + CLAUDE.md.
Run ONLY after the axiom-sweep verification passes and its commit lands."""
import sys

S = "CIRISOntology/Stance.lean"
s = open(S).read()

NEW = '''
, { key      := "one-theorem-thrice"
  , headline :=
      "Three of this page's results are ONE theorem: the parity bit, the CP phase, and "
      ++ "whether-the-past-can-be-proven are the same shape — a quantity no collection of "
      ++ "partial views can see."
  , plain    :=
      "This page began with three coins: any two look random, only the whole obeys the "
      ++ "rule. A later season proved a particle-physics phase invisible to every pair "
      ++ "reading. The taxonomy season proved that whether the past can still be "
      ++ "established cannot be read off a document alone — it needs the frame. Three "
      ++ "results, three fields, three different seasons. This season a computer checked "
      ++ "that they are one statement worn three ways: in each case there exist two wholes "
      ++ "that agree under EVERY partial view and still differ — in the third coin's rule, "
      ++ "in the phase, in whether the past survives. One shape: the part that does not "
      ++ "factor into pieces.\\n\\n"
      ++ "What this claim does NOT say: that the three quantities are one THING. That "
      ++ "further step — one ledger read at different depths — is a separate wager below, "
      ++ "with its own kill. This claim is the shape-identity only, and it is "
      ++ "machine-checked."
  , status   := .proved
  , witness  :=
      [ "CIRISOntology.Core.nonfactoring_parity"
      , "CIRISOntology.Core.nonfactoring_cp_phase"
      , "CIRISOntology.Core.nonfactoring_record" ]
  , confidence :=
      "Proved as SHAPE-identity: the three published theorems instantiate one definition "
      ++ "(NonFactoring). The abstraction is deliberately thin — two wholes, all partial "
      ++ "views agree, the quantity differs — because thinness is what keeps three "
      ++ "instances honest rather than manufactured."
  , kill     :=
      "Read the Lean: exhibit a partial-view family that computes one of the three "
      ++ "quantities, breaking its instance; or show the abstraction is gerrymandered — "
      ++ "that materially different notions of partial view were forced into one signature "
      ++ "to fake a unification."
  }
, { key      := "plus-one-is-one-bit"
  , headline :=
      "The +1 is worth exactly one bit: Record's coordinate is binary because time's "
      ++ "whole-only pattern is capped at one remembered bit."
  , plain    :=
      "Two results were proved in different seasons and never introduced to each other. "
      ++ "One: read the three coins as one thing at three MOMENTS, and the pattern only "
      ++ "the whole carries is worth exactly ONE BIT — causality itself caps it there. "
      ++ "Two: the taxonomy's twelfth thing, Record, is not a twelfth kind but a "
      ++ "two-valued relation — the past can be proven, or it cannot; every state of the "
      ++ "reverse-Babel object doubles exactly once. This wager says that is no "
      ++ "coincidence: the frame-bit is binary BECAUSE time's books cap the whole-only "
      ++ "share at one bit. Both halves are machine-checked; the identification between "
      ++ "them is the bet."
  , status   := .wager
  , confidence :=
      "A recognition-class wager in the house sense: the causal one-bit cap is proved, "
      ++ "Record's non-factoring and binarity are proved about the model, and ONLY the "
      ++ "identification is wagered."
  , kill     :=
      "A demonstrated stable THREE-valued Record reading — an artifact-frame pair whose "
      ++ "provability is neither yes nor no and provably not reducible to them; or the "
      ++ "trace test: if the whole-only share of real decision traces fails to behave as "
      ++ "a single frame-conditional bit where Record readings are available, the "
      ++ "identification dies."
  }
, { key      := "the-ledgers-third-name"
  , headline :=
      "The instrument and the taxonomy meet: the whole-only share and the Record "
      ++ "coordinate are one quantity at different depths — the ledger's third name."
  , plain    :=
      "This page's instrument measures pattern that lives only in the whole. Its "
      ++ "taxonomy types the one change-coordinate that needs the frame. This wager says "
      ++ "they are the same thing: what the sky campaigns hunted, what maintenance mints, "
      ++ "and whether-the-past-can-be-proven are one ledger read at different depths. If "
      ++ "true, a working AI agent's conscience needs no new instrument — the original "
      ++ "three-coin meter, pointed at what the agent did, the situation it was in, and "
      ++ "what came of it, IS the Record reading. That is testable on six and a half "
      ++ "thousand real decision traces from a production system that recorded which of "
      ++ "its actions were overridden."
  , status   := .wager
  , confidence :=
      "The furthest new wager of the season. Each of its parents is proved or measured; "
      ++ "only the identity is bet, and its first test is cheap, pre-registered next, and "
      ++ "uses data already in hand."
  , kill     :=
      "The two-column trace test, pre-registered before it runs: on the production trace "
      ++ "corpus, if the whole-only share of action-context-outcome triples fails to "
      ++ "concentrate on the recorded overrides while kind-readings succeed, the identity "
      ++ "is decorative and dies. Separately: it dies on any substrate where the share "
      ++ "and a frame-supplied Record reading are both measurable and decorrelate."
  }
'''

anchor = ', { key      := "wild-share"'
assert anchor in s and s.count(anchor) == 1
assert NEW.strip().startswith(', {')
s = s.replace(anchor, NEW.rstrip() + "\n" + anchor, 1)

# R3: no-early-dark-energy — name the mint corollary in confidence
old3 = 'a burst of order several percent'
assert old3 in s  # sanity that the claim is present
marker3 = ', { key      := "no-early-dark-energy"'
i3 = s.find(marker3)
conf3 = s.find(', confidence :=', i3)
# insert an extra sentence at the START of its confidence string
j3 = s.find('"', conf3) + 1
s = s[:j3] + ("The model-level skeleton is now machine-checked in miniature: maintenance "
  + "CREATES the share (the mint theorems), so a balance existing before any maintainer "
  + "is the model's own contradiction — the wager is that the world works like the "
  + "model. ") + s[j3:]

# R4: eleven-plus-one — geometry-leg honesty + mechanized structure, appended to confidence
m4 = ', { key      := "eleven-plus-one"'
i4 = s.find(m4)
conf4 = s.find(', confidence :=', i4)
j4 = s.find('"', conf4) + 1
s = s[:j4] + ("New since the cash-in: the family structure is mechanized — the eleven "
  + "are the terminal member of a resource-indexed family (7, 10, 11 as expressive "
  + "resources are added), the assertive four are a grounding stack that provably "
  + "terminates, and the direction-of-fit grading 4+3+1+3 is the measured shape of the "
  + "panel's own confusions. And one honest null: the GEOMETRY leg — the kinds as "
  + "directions in an embedding space — was tested and read null on its first "
  + "instrument, whose own placebo convicted the construction (it subtracted away the "
  + "signal carrier); a calibrated successor instrument and a four-times replication "
  + "corpus exist, and that question is open, not supportive. ") + s[j4:]

# R6: precedent-is-bits — one spine sentence in confidence
m6 = ', { key      := "precedent-is-bits"'
i6 = s.find(m6)
conf6 = s.find(', confidence :=', i6)
j6 = s.find('"', conf6) + 1
s = s[:j6] + ("The composition now has a named spine: its record leg is the same "
  + "non-factoring quantity this page proves and measures everywhere else — see "
  + "the-ledgers-third-name. ") + s[j6:]

# R7: ai-safety — the practical route sentence in confidence
m7 = ', { key      := "ai-safety"'
i7 = s.find(m7)
conf7 = s.find(', confidence :=', i7)
j7 = s.find('"', conf7) + 1
s = s[:j7] + ("The practical route gained tools this season: a twelve-instrument suite "
  + "whose honesty flags are theorems (nothing validated until a human ceiling exists), "
  + "a conscience re-orientation licensed by the taxonomy's exhaustiveness, and a "
  + "pre-registered first test on production decision traces. ") + s[j7:]

open(S, "w").write(s)
print("Stance.lean: 3 claims added, 4 re-frames applied")

# CLAUDE.md tallies
C = "CLAUDE.md"
c = open(C).read()
old = "Statuses: 15 proved here, 9 measured, 21 wagers, 1 open, 5 dead (kept, marked)."
new = "Statuses: 16 proved here, 9 measured, 23 wagers, 1 open, 5 dead (kept, marked)."
assert old in c
open(C, "w").write(c.replace(old, new))
print("CLAUDE.md tallies: 16/9/23/1/5")
