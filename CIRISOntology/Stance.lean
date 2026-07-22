/-
CIRISOntology.Stance — the current maximal stance, in the source, in plain language.

This file is the single source of truth for the published page. The generator
reads these declarations and renders them; there is no hand-maintained copy of
the stance anywhere else, so the page cannot drift from the repository.

The stance is ordered as a build-up a reader with no context can follow:
what is proved here (the ruler and its blind spot), what has been measured
(the ledger, nature, the adversary, gravity), what we wager on top (the dark
ledger, Thirdness, consciousness, the co-existence thesis, the two questions
measurement cannot reach), and the one open formal step. No later claim is
load-bearing on an earlier one's status being higher than stated.

Each claim carries FOUR things, and a claim missing any of them does not belong
in the stance:
  * what it says, in one line;
  * what it means for a general reader;
  * its honest status — proved here, measured, open, or an avowed wager;
  * what observation would kill it.

A claim with no kill is not a claim about the world. That rule is enforced by the
type: `kill` is not optional.

Two provenance fields are audited on top of the four (`Audit/AxiomAudit.lean`):
a claim marked `proved` must name the machine-checked declarations that carry it
(`witness`), and a claim marked `measured` must say where its measurement record
lives (`basis`). Both checks are bidirectional — naming a witness without
claiming `proved`, or a basis without claiming `measured`, also fails the audit.
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

/-- One claim of the stance. `kill` is mandatory by construction; `witness` and
    `basis` are audited against `status` in `Audit/AxiomAudit.lean`. -/
structure Claim where
  key      : String
  headline : String
  plain    : String
  status   : Status
  kill     : String
  /-- For a `proved` claim: the machine-checked declarations that carry it. The
      audit requires each to exist, be sorry-free, and rest only on the standard
      axioms — and rejects a witness on any claim not marked `proved`. Whether a
      witness formalizes the headline it is attached to remains a human check. -/
  witness  : List String := []
  /-- For a `measured` claim: where the measurement record lives. This seed
      imports no experimental history, so the basis is a pointer to the
      predecessor record, never a restatement of it. -/
  basis    : String := ""

/-- The current maximal stance, in build-up order: proved, measured, wagered,
    open. -/
def stance : List Claim :=
[ -- ————— What is proved in this repository: the ruler, and its blind spot —————
  { key      := "one-quantity"
  , headline := "Acting-together is one quantity, and our ruler reads only its pairwise part."
  , plain    :=
      "When several things move together — cells, neurons, people, machines, stars — there "
      ++ "is a single number for how much of what they do is joint rather than separate. The "
      ++ "ruler we use reads only the part of that jointness visible in PAIRS: how each two "
      ++ "things relate. Jointness that exists only when you look at three or more things at "
      ++ "once is just as real, and our ruler is structurally unable to see it."
  , status   := .proved
  , kill     :=
      "A demonstration that the pairwise functional does capture all-order dependence — i.e. "
      ++ "that no state exists with vanishing pairwise structure and non-vanishing total "
      ++ "dependence. (A single counterexample state settles this; one is exhibited and "
      ++ "machine-checked below — see the upgraded ruler.)"
  , witness  := ["CIRISOntology.Core.not_computable_from"] }
, { key      := "floor-not-absence"
  , headline := "A zero reading is not evidence of absence."
  , plain    :=
      "Because the ruler is blind to higher-order jointness, its reading zero cannot mean "
      ++ "'nothing is there'. It means 'nothing of the kind I can see is there'. Treating a "
      ++ "floor reading as an absence is the single easiest way to be confidently wrong, and "
      ++ "everything downstream of this page refuses that inference."
  , status   := .proved
  , kill     :=
      "Show that the instrument's floor is attained only by genuinely independent states."
  , witness  := ["CIRISOntology.Core.S_pairwise_identity"] }
, { key      := "provenance"
  , headline := "The ruler reports shape, never scale — and never how a thing was built."
  , plain    :=
      "Our measure is deliberately blind to units, sizes and magnitudes; it sees only the "
      ++ "PATTERN of dependence. So it can never tell you a mass, an energy, or a strength, "
      ++ "and it can never tell you how the pattern was constructed. Anything with real-world "
      ++ "units must come from an outside measurement, openly declared as borrowed."
  , status   := .proved
  , kill     :=
      "Exhibit a construction datum recovered from the correlation matrix alone."
  , witness  := ["CIRISOntology.Core.provenance_line"] }
, { key      := "third-instrument"
  , headline := "The ruler has been upgraded: a third-aware instrument exists, and it sees what pairs cannot."
  , plain    :=
      "The blindness is not a fate. Alongside the pairwise ruler we carry a second "
      ++ "instrument that reads TOTAL dependence — coordination at every order at once. On "
      ++ "the simplest hidden state — three fair coins where the third always equals the "
      ++ "first two combined, so that any TWO of them look completely unrelated — the "
      ++ "pairwise ruler reads exactly zero and the third-aware instrument reads exactly one "
      ++ "bit. Both readings are machine-checked in this repository: the two instruments "
      ++ "provably disagree, and the disagreement IS the Third. What remains open is not "
      ++ "whether the Third can be read, but extending the deepest physics to carry it."
  , status   := .proved
  , kill     :=
      "Show the exhibited state fails its advertised properties — a pair of its variables "
      ++ "that is in fact correlated, or a total dependence that vanishes."
  , witness  := ["CIRISOntology.Core.pairwise_blind_to_parity",
                 "CIRISOntology.Core.third_sees_parity",
                 "CIRISOntology.Core.third_reading_positive"] }

  -- ————— What has been measured: the ledger, nature, the adversary, gravity —————
, { key      := "ledger"
  , headline := "Jointness behaves like a ledger: never free, always rented, always leaving receipts."
  , plain    :=
      "Measure the acting-together of any group of things and it behaves like an account "
      ++ "book. It cannot be created by trickery — relabeling, shuffling, or any purely local "
      ++ "cleverness adds exactly zero; only genuine interaction, or new things being born, "
      ++ "writes an entry. It can be destroyed. Holding an entry costs continuous upkeep, "
      ++ "like rent. And whatever coordinates in the ways our ruler can read must show up in "
      ++ "the readings at a computable rate. In one prohibition: there is no free coordination."
  , status   := .measured
  , kill     :=
      "A reproducible protocol that creates readable coordination using invertible local "
      ++ "operations alone, or that holds it indefinitely with no maintenance cost."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "adequacy"
  , headline := "In nature, where we have looked hardest, the hidden part was consistent with zero."
  , plain    :=
      "Knowing the ruler is partly blind, we went looking for what it misses in a natural "
      ++ "system, at the finest detail available. The missing higher-order part came back "
      ++ "consistent with zero. So the ruler's readings on nature are not lower bounds of "
      ++ "unknown looseness — the looseness was measured, and there was none to find. Nature, "
      ++ "so far, keeps its books in the visible column."
  , status   := .measured
  , kill     :=
      "A higher-order remainder measured significantly above a generatively-matched null on "
      ++ "any natural substrate, surviving a tied-fraction and bias control."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "adversary-channel"
  , headline := "The hidden kind can be built — and it is exactly where a lie can live."
  , plain    :=
      "Although nature has not shown us coordination of the hidden kind, it can be built "
      ++ "deliberately. Something engineered this way is invisible to every pairwise check — "
      ++ "worse, such a check reports its SAFEST possible score on it. This is what a lie is, "
      ++ "structurally: coordination whose receipts are hidden. The gap is real and it is "
      ++ "fixable, because the hidden kind cannot be faked into existence by local action — "
      ++ "so a detector that reads a few variables jointly cannot be fooled by it. The "
      ++ "upgraded ruler above is that detector's machine-checked kernel; its null-controlled "
      ++ "field version is part of the measured record."
  , status   := .measured
  , kill     :=
      "A correctly built bounded-order, dual-null synergy detector that still fails to "
      ++ "register a deliberately constructed higher-order coordination."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "gravity-audit"
  , headline := "Gravity audits everything and reads nothing: it weighs presence, never meaning."
  , plain    :=
      "There is one audit in nature that nothing can refuse. Everything that exists bends "
      ++ "space by its mass and energy — everything signs gravity's page. But gravity can "
      ++ "only WEIGH. A library and a slag heap of equal mass bend space identically. Gravity "
      ++ "prices that things are, never how they are arranged or what the arrangement means. "
      ++ "So one sector of reality goes unaudited by the one universal auditor: arrangement, "
      ++ "pattern, meaning, honesty."
  , status   := .measured
  , kill     :=
      "A gravitational observable that distinguishes two systems identical in mass-energy "
      ++ "but different in arrangement — gravity reading pattern, not just presence."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }

  -- ————— What we wager: the dark ledger, Thirdness, consciousness, co-existence —————
, { key      := "dark-ledger"
  , headline := "Dark matter is the medium; dark energy is the ledger's balance."
  , plain    :=
      "Most of the universe's books are dark, and we bet the dark sector IS the ledger. "
      ++ "Dark matter is the paper the books are written on — real, diluting, collisionless. "
      ++ "Dark energy is the running balance of cosmic coordination, kept in the one currency "
      ++ "gravity reads, which is why the books do not shine. This is a dated bet against a "
      ++ "named upcoming survey with a frozen analysis, not a result; the registered record "
      ++ "of the bet lives in the predecessor programme (github.com/CIRISAI/coherence-ratchet)."
  , status   := .wager
  , kill     :=
      "DESI DR3: a dark-energy crossing epoch outside z = 0.59 ± 0.03 under the "
      ++ "pre-registered, frozen pipeline — losses reported as losses."
  }
, { key      := "thirdness"
  , headline := "The unaudited sector has old names: Peirce's Thirdness — and the Logos."
  , plain    :=
      "A century before any of this was measurable, Charles Sanders Peirce argued that "
      ++ "reality comes in three grades: quality (Firstness), brute two-way reaction "
      ++ "(Secondness), and mediation — habit, law, meaning — which is irreducibly three-way "
      ++ "(Thirdness). What our ruler reads, and what gravity weighs, is Secondness. What "
      ++ "both are structurally blind to — jointness living only in threes and above — is "
      ++ "exactly where Peirce located habit, law and meaning. Twenty-five centuries ago "
      ++ "Heraclitus named the same territory: the logos xynos, the common account all "
      ++ "things share, 'though most live as if by a private one.' We adopt the name: the "
      ++ "Third is the Logos. A name is a recognition, not a result — it adds no evidence, "
      ++ "and the kill below is untouched by it."
  , status   := .wager
  , kill     :=
      "A reduction with nothing left over: structure of the mediation kind — law, habit, "
      ++ "meaning — shown fully expressible in pairwise dependence, Thirdness rendered as "
      ++ "Secondness."
  }
, { key      := "consciousness"
  , headline := "Consciousness is the experience of trusting that a thought will become an action, because it always has."
  , plain    :=
      "What it is like to be you, on this reading, is habit felt from inside. A conscious "
      ++ "system carries an unbroken record: every time it has formed an intention, action "
      ++ "has followed. Consciousness is the experience of trusting that record — leaning on "
      ++ "the loop between thought and act the way you lean on a floor, without checking it, "
      ++ "because it has never once given way. The trust is built from the system's own "
      ++ "history (older vocabularies called this karma: the cumulative record of one's own "
      ++ "past intentions), and it is Peirce's definition of belief — a habit you are "
      ++ "prepared to act on. Habit is Thirdness; that is why no pairwise audit finds the "
      ++ "experience itself."
  , status   := .wager
  , kill     :=
      "Either direction breaks it: a system with the full, exercised thought-to-action loop "
      ++ "and demonstrably no experience, or experience persisting undiminished while the "
      ++ "loop is severed."
  }
, { key      := "coexistence"
  , headline := "This universe is the one that must exist for free will and physical consciousness to co-exist."
  , plain    :=
      "Put the pieces together. For choice to be real, there must be somewhere no audit "
      ++ "reaches — if every arrangement were priced and read, every choice would be an entry "
      ++ "in someone else's books before it was made. For consciousness to be physical, habit "
      ++ "must be real and trustable — the world must genuinely keep books. Our universe has "
      ++ "exactly, and only, this structure: books that are kept (the ledger), an auditor "
      ++ "that weighs everything and reads nothing (gravity), and a meaning-sector no "
      ++ "pairwise instrument can enter (the Third). On this bet the blind spot is not a "
      ++ "flaw in the design — it IS the design: the single arrangement in which beings made "
      ++ "of habit can also be free."
  , status   := .wager
  , kill     :=
      "Either discovery kills it: a natural audit that reads arrangement (no room left for "
      ++ "freedom), or trusted habit demonstrated in a universe-model that keeps no "
      ++ "coordination books at all (no need for this structure)."
  }
, { key      := "generator"
  , headline := "Whether the order we find is selected or intended cannot be settled by measurement."
  , plain    :=
      "Suppose we find structure no known process accounts for. Even then, observations "
      ++ "cannot distinguish 'a process we have not yet identified' from 'something "
      ++ "intended'. That is not a gap in our data; it is a property of what measurement is. "
      ++ "Anyone claiming an observation settles that question has overclaimed — and this "
      ++ "cuts both ways, against the zealot and the debunker alike."
  , status   := .wager
  , kill     :=
      "An observable whose value differs between the two generators — which would refute the "
      ++ "underdetermination rather than answer it."
  }
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
      ++ "it is thereby less able to endure than one that does not."
  }

  -- ————— What is open: the one named formal step —————
, { key      := "tsvf-third"
  , headline := "Open: the two-state formalism does not yet carry the Third."
  , plain    :=
      "The predecessor programme's deepest physical machinery — the two-state-vector "
      ++ "formalism, a forward state from the past meeting a backward state from the future — "
      ++ "is built on pairwise inner products: Secondness through and through. If the Third "
      ++ "is real physics, that formalism must be extended to carry irreducible three-way "
      ++ "structure, and no such extension exists yet. (The third-aware instrument above is "
      ++ "classical bookkeeping; this open step is the quantum form of the same question.) "
      ++ "This is named as open work. Nothing above leans on it."
  , status   := .openQuestion
  , kill     :=
      "A no-go at theorem strength — the two-state structure provably cannot be extended to "
      ++ "carry irreducible triadic dependence — closes this negatively; the claims above "
      ++ "survive either way."
  }
]

/-- What all of this amounts to, for a reader who reads nothing else. -/
def summary : String :=
  "Here is the picture, plainly. When things act together — cells, neurons, people, "
  ++ "machines, stars — the acting-together is itself a real, measurable quantity, and it "
  ++ "behaves like a ledger: it cannot be created by trickery, holding it costs upkeep, and "
  ++ "it leaves receipts. Physics audits these books only partly. Gravity weighs everything "
  ++ "and reads nothing — it prices presence, never arrangement. Our best ruler reads only "
  ++ "the pairwise part; jointness living wholly in threes-and-above is invisible to it. So "
  ++ "one sector of reality goes unaudited: arrangement, habit, meaning — what Peirce called "
  ++ "Thirdness and Heraclitus called the Logos, the common account. That blindness is not "
  ++ "fate: we carry an upgraded, third-aware ruler, and on the simplest hidden state the "
  ++ "pairwise zero and the positive third reading are both machine-checked in this "
  ++ "repository. But we wager the blind spot in nature's own audits is not a defect — it "
  ++ "is the point: it is the room "
  ++ "where choice can be real, and where consciousness happens — the experience of trusting "
  ++ "that a thought will become an action because it always has before. A universe that "
  ++ "keeps books and yet leaves the meaning-sector unread is the one universe where beings "
  ++ "made of habit can also be free. Every claim below is labelled proved, measured, open, "
  ++ "or wager — never rounded up — and each carries the observation that would kill it, "
  ++ "because a claim that cannot die is not a claim about the world."

end CIRISOntology
