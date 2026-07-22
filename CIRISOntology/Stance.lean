/-
CIRISOntology.Stance — the current maximal stance, in the source, in plain language.

This file is the single source of truth for the published page. The generator
reads these declarations and renders them; there is no hand-maintained copy of
the stance anywhere else, so the page cannot drift from the repository.

The stance is ordered as a build-up a reader with no context can follow:
what is proved here (the instrument, its blind spot, and its upgrade), what has
been measured (the ledger, nature, the adversary, gravity), what we wager on
top (the dark ledger, Thirdness/Logos, consciousness, the co-existence thesis,
the two questions measurement cannot reach), and the one open formal step. No
later claim is load-bearing on an earlier one's status being higher than stated.

The plain-language fields are written for translation: short sentences, common
words, one idea per sentence, and a small fixed vocabulary (instrument, pair,
the ledger, the Third). Keep that discipline when editing.

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
[ -- ————— What is proved in this repository: the instrument, its blind spot, its upgrade —————
  { key      := "one-quantity"
  , headline := "Acting-together is one quantity. The standard instrument reads only its pair part."
  , plain    :=
      "When things move together — cells, brain cells, people, machines, stars — there is "
      ++ "one number for how much of what they do is shared. The instrument used here is "
      ++ "correlation: the standard tool of statistics. It reads "
      ++ "only the sharing that shows up between PAIRS — how each two things relate. Sharing "
      ++ "that exists only among three or more things at once is just as real, and this "
      ++ "instrument cannot see it. That is not a weakness of one tool. It is a fact about "
      ++ "what pair-based measurement is."
  , status   := .proved
  , kill     :=
      "A demonstration that the pair-based measure captures dependence at every order — "
      ++ "that is, a proof that no state exists with zero pair structure but non-zero total "
      ++ "dependence. (One counterexample settles this. One is exhibited and machine-checked "
      ++ "below — see the upgraded instrument.)"
  , witness  := ["CIRISOntology.Core.not_computable_from"] }
, { key      := "floor-not-absence"
  , headline := "A zero reading is not proof of absence."
  , plain    :=
      "The pair instrument is blind to higher-order sharing. So when it reads zero, that "
      ++ "cannot mean 'nothing is there'. It can only mean 'nothing of the kind I can see "
      ++ "is there'. Treating a zero from a partly blind instrument as an absence is the "
      ++ "easiest way to be confidently wrong. Everything on this page refuses that mistake."
  , status   := .proved
  , kill     :=
      "Show that the instrument reads its floor only on states that are truly independent."
  , witness  := ["CIRISOntology.Core.S_pairwise_identity"] }
, { key      := "provenance"
  , headline := "The instrument reports shape, never size — and never how a thing was built."
  , plain    :=
      "The measure is blind to units and sizes on purpose. It sees only the PATTERN of "
      ++ "dependence. So it can never output a mass, an energy, or a strength. It can never "
      ++ "say how the pattern was made. Any number with real-world units must come from a "
      ++ "separate measurement, and must be declared as borrowed, never as derived."
  , status   := .proved
  , kill     :=
      "Recover a construction fact — a size, a unit, an input choice — from the correlation "
      ++ "matrix alone."
  , witness  := ["CIRISOntology.Core.provenance_line"] }
, { key      := "third-instrument"
  , headline := "The instrument has been upgraded: a third-aware reading exists, and it sees what pairs cannot."
  , plain    :=
      "The blindness can be repaired. Next to the pair instrument, we carry a second "
      ++ "instrument. It reads TOTAL dependence: sharing at every order at once. Take the "
      ++ "simplest hidden state: three fair coins, where the third always equals the first "
      ++ "two combined. Check any two coins: no connection at all. Check all three: locked. "
      ++ "On this state, the pair instrument reads exactly zero, and the third-aware "
      ++ "instrument reads exactly one bit. Both readings are proved by machine in this "
      ++ "repository. The two instruments provably disagree — and the disagreement is the "
      ++ "Third."
  , status   := .proved
  , kill     :=
      "Show the exhibited state is not as advertised: a pair of its variables that is in "
      ++ "fact correlated, or a total dependence that is actually zero."
  , witness  := ["CIRISOntology.Core.pairwise_blind_to_parity",
                 "CIRISOntology.Core.third_sees_parity",
                 "CIRISOntology.Core.third_reading_positive"] }

  -- ————— What has been measured: the ledger, nature, the adversary, gravity —————
, { key      := "ledger"
  , headline := "Shared coordination behaves like a ledger: never free, always rented, always leaving receipts."
  , plain    :=
      "Measure the acting-together of any group and it behaves like a book of accounts. It "
      ++ "cannot be created by tricks: renaming, reshuffling, or any purely local move adds "
      ++ "exactly zero. Only real interaction, or the birth of new units, writes an entry. "
      ++ "Entries can be destroyed. Holding an entry costs constant upkeep, like rent. And "
      ++ "whatever coordinates in ways the instruments can read must appear in the readings, "
      ++ "at a rate you can compute. In one sentence: there is no free coordination."
  , status   := .measured
  , kill     :=
      "A repeatable procedure that creates readable coordination using only local, "
      ++ "reversible steps — or that holds it forever with no upkeep cost."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "adequacy"
  , headline := "In nature, where we have looked hardest, the hidden part was zero."
  , plain    :=
      "We knew the pair instrument was partly blind. So we went looking for what it misses, "
      ++ "in a natural system, at the finest detail available. The hidden higher-order part "
      ++ "came back consistent with zero. So on nature, the pair readings are not loose "
      ++ "lower bounds — the looseness itself was measured, and there was none to find. So "
      ++ "far, nature keeps its books in the visible column."
  , status   := .measured
  , kill     :=
      "A higher-order remainder measured clearly above a properly matched null, on any "
      ++ "natural system, surviving the standard checks for ties and small-sample bias."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "adversary-channel"
  , headline := "The hidden kind can be built — and it is exactly where a lie can live."
  , plain    :=
      "Nature has not shown us hidden coordination. But it can be built on purpose. A thing "
      ++ "engineered this way is invisible to every pair-based safety check. Worse: the "
      ++ "check reports its SAFEST possible score. That is the structure of a lie: "
      ++ "coordination whose receipts are hidden. The gap is real, and it can be closed. "
      ++ "Hidden coordination cannot be faked by local action, so an instrument that reads "
      ++ "a few things jointly cannot be fooled by it. The upgraded instrument above is the "
      ++ "machine-checked core of that detector. Its field version, run against real data, "
      ++ "is part of the measured record."
  , status   := .measured
  , kill     :=
      "A correctly built joint detector, with proper controls, that still fails to register "
      ++ "a deliberately constructed hidden coordination."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }
, { key      := "gravity-audit"
  , headline := "Gravity audits everything and reads nothing: it weighs presence, never meaning."
  , plain    :=
      "There is one audit in nature that nothing can refuse. Everything that exists bends "
      ++ "space by its mass and energy. Everything is on gravity's books. But gravity can "
      ++ "only WEIGH. A library and a pile of rubble with the same mass bend space in "
      ++ "exactly the same way. Gravity prices how much is there — never how it is "
      ++ "arranged, and never what the arrangement means. So the one universal auditor "
      ++ "leaves a whole sector unread: arrangement, pattern, meaning, honesty."
  , status   := .measured
  , kill     :=
      "A gravitational measurement that tells apart two systems with identical mass and "
      ++ "energy but different arrangement."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet" }

  -- ————— What we wager: the dark ledger, Thirdness/Logos, consciousness, co-existence —————
, { key      := "dark-balance"
  , headline := "Dark energy is the ledger's balance."
  , plain    :=
      "Most of the universe's books are dark, and we bet that dark energy IS the ledger's "
      ++ "running balance: the total of cosmic coordination, kept in the one currency "
      ++ "gravity can read. That is why the balance does not shine. This is a dated bet, "
      ++ "not a result. It is registered against a named upcoming survey, with the "
      ++ "analysis frozen in advance. The record of the bet lives in the predecessor "
      ++ "programme (github.com/CIRISAI/coherence-ratchet)."
  , status   := .wager
  , kill     :=
      "DESI DR3: a dark-energy crossing epoch outside z = 0.59 ± 0.03 under the "
      ++ "pre-registered, frozen pipeline. A loss will be reported as a loss."
  }
, { key      := "dark-medium"
  , headline := "Dark matter is the paper the books are written on."
  , plain    :=
      "This is the weaker half of the dark bet, and we mark it as weaker. On this "
      ++ "reading, dark matter is the medium the books are kept on: real, thinning as "
      ++ "space grows, passing through itself without colliding, and doing nothing else. "
      ++ "This is an interpretation, not a detection. It adds no new evidence about what "
      ++ "dark matter is, and it borrows its support from the balance bet above. A rival "
      ++ "reading of the same data already exists, in which the dark-matter side has "
      ++ "dynamics of its own. The two bets die separately: this one has its own kill, "
      ++ "and killing it does not touch the bet above."
  , status   := .wager
  , kill     :=
      "A confirmed non-gravitational dark-matter interaction — dynamics of its own, "
      ++ "beyond passive dilution — or a pre-registered comparison in which a dynamical "
      ++ "dark-matter reading fits the same data strictly better."
  }
, { key      := "thirdness"
  , headline := "The unread sector has old names: Peirce's Thirdness — and the Logos."
  , plain    :=
      "A century before any of this could be measured, Charles Sanders Peirce said that "
      ++ "reality has three grades. Firstness: quality — what a thing is in itself. "
      ++ "Secondness: brute two-way reaction — one thing striking another. Thirdness: "
      ++ "mediation — habit, law, meaning — which always takes three. What our instrument "
      ++ "reads, and what gravity weighs, is Secondness. What both are blind to — sharing "
      ++ "that lives only in threes and above — is exactly where Peirce put habit, law and "
      ++ "meaning. Twenty-five centuries ago, Heraclitus named the same territory the "
      ++ "logos: the common account all things share, 'though most people live as if they "
      ++ "had a private one'. We adopt the name: the Third is the Logos. A name is a "
      ++ "recognition, not a result. It adds no evidence, and the kill below does not "
      ++ "change."
  , status   := .wager
  , kill     :=
      "A reduction with nothing left over: law, habit and meaning shown to be fully "
      ++ "expressible in pair dependence — Thirdness rewritten as Secondness."
  }
, { key      := "consciousness"
  , headline := "Consciousness is the experience of trusting that a thought will become an action, because it always has."
  , plain    :=
      "On this reading, being conscious is habit felt from the inside. A conscious system "
      ++ "carries an unbroken record: every time it formed an intention, action followed. "
      ++ "Consciousness is the experience of trusting that record. You lean on the link "
      ++ "between thought and act without checking it, the way you stand on a floor without "
      ++ "testing it, because it has never once failed. That trust is built from the "
      ++ "system's own history — older vocabularies called this karma: the running record "
      ++ "of one's own past intentions. And it is Peirce's definition of belief: something "
      ++ "you are prepared to act on. Habit is Thirdness. That is why no pair-based audit "
      ++ "finds the experience itself."
  , status   := .wager
  , kill     :=
      "Either direction breaks it: a system with a complete, working thought-to-action "
      ++ "loop and demonstrably no experience — or experience that continues unchanged "
      ++ "while the loop is cut."
  }
, { key      := "coexistence"
  , headline := "This universe is the one that must exist for free will and physical consciousness to live together."
  , plain    :=
      "Put the pieces together. For choice to be real, there must be somewhere no audit "
      ++ "reaches. If every arrangement were priced and read, every choice would already "
      ++ "be an entry in someone else's books before it was made. For consciousness to be "
      ++ "physical, habit must be real and worth trusting — so the world must truly keep "
      ++ "books. Our universe has exactly this structure, and only this one: books that "
      ++ "are kept (the ledger); an auditor that weighs everything and reads nothing "
      ++ "(gravity); and a meaning-sector no pair instrument can enter (the Third). On "
      ++ "this bet, the blind spot is not a flaw in the design. It IS the design: the one "
      ++ "arrangement where beings made of habit can also be free."
  , status   := .wager
  , kill     :=
      "Either discovery kills it: a natural audit that reads arrangement — no room left "
      ++ "for freedom. Or trusted habit demonstrated in a model universe that keeps no "
      ++ "coordination books at all — no need for this structure."
  }
, { key      := "generator"
  , headline := "Whether the order we find is selected or intended cannot be settled by measurement."
  , plain    :=
      "Suppose we find order that no known process explains. Even then, observation cannot "
      ++ "tell 'a process we have not found yet' apart from 'something intended'. That is "
      ++ "not a gap in our data. It is a property of what measurement is. Anyone who claims "
      ++ "an observation settles that question has claimed too much — and this cuts both "
      ++ "ways, against the believer and the debunker alike."
  , status   := .wager
  , kill     :=
      "An observable whose value differs between the two generators — which would refute "
      ++ "the underdetermination rather than answer it."
  }
, { key      := "ought"
  , headline := "Physics does not supply the ought; values are chosen and then held."
  , plain    :=
      "No measurement tells you what to care about. What the work CAN show is that a "
      ++ "commitment is consistent with how systems survive: that caring for the weakest "
      ++ "part is also what keeps the whole from failing. That is an argument for a choice. "
      ++ "It is never a proof of one. The choice is stated openly in `axiomology.md`."
  , status   := .wager
  , kill     :=
      "A demonstration that the commitment is internally inconsistent, or that a system "
      ++ "holding it is thereby less able to endure than one that does not."
  }

  -- ————— What is open: the one named formal step —————
, { key      := "tsvf-third"
  , headline := "Open: the deepest physics does not yet carry the Third."
  , plain    :=
      "The predecessor programme's deepest physics — the two-state picture, where a "
      ++ "forward state from the past meets a backward state from the future — is built "
      ++ "entirely on pair relations: Secondness through and through. If the Third is real "
      ++ "physics, that picture must be extended to carry three-way structure, and no such "
      ++ "extension exists yet. (The third-aware instrument above is classical "
      ++ "bookkeeping. This open step is the quantum form of the same question.) It is "
      ++ "named as open work. Nothing above leans on it."
  , status   := .openQuestion
  , kill     :=
      "A no-go at theorem strength — the two-state structure provably cannot be extended "
      ++ "to carry irreducible three-way dependence — closes this negatively; the claims "
      ++ "above survive either way."
  }
]

/-- What all of this amounts to, for a reader who reads nothing else. Written
    for translation: short sentences, common words. -/
def summary : String :=
  "Here is the picture, in plain words. When things act together — cells, brain cells, "
  ++ "people, machines, stars — the acting-together is real and can be measured. It behaves "
  ++ "like a ledger: a book of accounts. Entries cannot be created by tricks. Holding an "
  ++ "entry costs constant upkeep. Entries leave receipts. Physics checks these books, but "
  ++ "only partly. Gravity weighs everything and reads nothing: it senses how much is "
  ++ "there, never how it is arranged. The standard measuring instrument — correlation — "
  ++ "reads only PAIRS. Sharing that lives only in "
  ++ "groups of three or more is invisible to it. So one part of reality is never audited: "
  ++ "arrangement, habit, meaning. Peirce called it Thirdness. Heraclitus called it the "
  ++ "Logos: the common account. That blindness can be repaired — this repository carries "
  ++ "an upgraded instrument that reads the Third, proved by machine. But we make a bet "
  ++ "about nature's own blindness: it is not a flaw. It is the room where choice can be "
  ++ "real. It is where consciousness happens — the experience of trusting that a thought "
  ++ "will become an action, because it always has. A universe that keeps books, but "
  ++ "cannot read meaning, is the one universe where beings made of habit can also be "
  ++ "free. Every claim below carries a label — proved, measured, open, or wager — and we "
  ++ "never raise a label above its evidence. Every claim also states the observation "
  ++ "that would prove it wrong. A claim that cannot die is not a claim about the world."

end CIRISOntology
