/-
CIRISOntology.Stance — the current maximal stance, in the source, in plain language.

This file is the single source of truth for the published page. The generator
reads these declarations and renders them; there is no hand-maintained copy of
the stance anywhere else, so the page cannot drift from the repository.

THE FRAME. The page announces a discovery, in ordinary language: the Logos —
the element of reality made of shared pattern (habit, law, meaning) — is real,
measurable, and machine-checked here in its simplest form. The claims build
from that discovery outward: what is proved, what the world's books look like
(measured), what we bet it explains (meaning, consciousness, language models,
AI safety, free will, the dark sector), and the one open formal step. No
instrument is a protagonist; no predecessor history is imported. No later
claim is load-bearing on an earlier one's status being higher than stated.

TWO STANDING TRAPS, GUARDED HERE. (1) A proof about a MODEL is never allowed to
stand in for a fact about the world: `rent-or-death` is proved, and its own text
says so and points at the measured claim that faces the world. (2) A RECOGNITION
— an old name adopted for something we measured — adds no evidence and moves no
kill: `pi-and-e` and `law-as-habit` say outright which mathematics is borrowed,
which idea is someone else's, and what is only ours.

The plain-language fields are written for translation: short sentences, common
words, one idea per sentence, and a small fixed vocabulary (the Logos, pair,
whole, the ledger). Keep that discipline when editing.

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
  /-- KILLED. The claim's own stated falsifier was satisfied. The claim stays on
      the page, marked dead, with what killed it — deleting it would destroy the
      only evidence that the method works. -/
  | dead
  deriving DecidableEq, Repr

def Status.label : Status → String
  | .proved       => "proved"
  | .measured     => "measured"
  | .openQuestion => "open"
  | .wager        => "wager"
  | .dead         => "dead"

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
  /-- For a `dead` claim: what satisfied the falsifier, and when. Audited
      bidirectionally — a dead claim must say what killed it, and no living
      claim may carry one. The record keeps its dead. -/
  killedBy : String := ""
  /-- What would move this claim UP a level of confidence — the measurement,
      proof, or replication that would earn a stronger label. Promotion is
      earned, never declared; this field says the price. Empty for claims at
      ceiling and for the dead. -/
  promote  : String := ""

/-- The current maximal stance, in build-up order: the discovery (proved), the
    world's books (measured), what it explains (wagered), the open step. -/
def stance : List Claim :=
  -- ————— The discovery, proved in this repository —————
[ { key      := "logos"
  , headline :=
      "The Logos is real: a whole can hold a pattern that none of its parts have on their "
      ++ "own — and that pattern can be measured."
  , plain    :=
      "Here is the discovery, small enough to try at your kitchen table. Flip two coins. "
      ++ "Then place a third coin by a rule: if the first two coins came up different, make "
      ++ "the third one heads. If they came up the same, make it tails.\n\n"
      ++ "Now look at just two of the three coins — say the first and the third. They tell you "
      ++ "nothing about each other. Why? The third coin depends on whether the first two "
      ++ "match, and that depends on the second coin — which was its own fresh, random flip. "
      ++ "Check any pair this way, and every pair looks completely random.\n\n"
      ++ "But look at all three coins together, and the rule appears: if you can see any two "
      ++ "of them, you know the third one for certain. The connection is real — you built it "
      ++ "yourself — but it lives only in the group of three. It is never in any pair.\n\n"
      ++ "People have had a name for this kind of pattern for twenty-five centuries — 2,500 "
      ++ "years. A Greek thinker, Heraclitus, called it the Logos: the common account that all "
      ++ "things share. A later thinker, Peirce, called it Thirdness: habit, law, meaning.\n\n"
      ++ "This project proves it by machine: pattern that lives only in the whole really "
      ++ "exists, and it can be measured directly. It also proves the limit exactly — and the "
      ++ "exact form matters, so the claim about pair summaries states it carefully.\n\n"
      ++ "How sure are we? This claim is proved — a computer checked a mathematical proof of "
      ++ "it, in this very project. One question is left open on purpose: is everything we "
      ++ "call meaning made of this kind of pattern? That part is a bet, and we state it "
      ++ "below."
  , status   := .proved
  , kill     :=
      "You could prove this wrong by showing our three-coin setup is not what we say it is: "
      ++ "find a pair of coins inside it that really are connected — not merely uncorrelated "
      ++ "but genuinely informative about each other — or show the whole-group pattern is "
      ++ "actually zero. (Both are machine-checked, so this is a check of our English "
      ++ "against our Lean.)"
  , witness  := ["CIRISOntology.Core.pairwise_blind_to_parity",
                 "CIRISOntology.Core.third_sees_parity",
                 "CIRISOntology.Core.third_reading_positive",
                 "CIRISOntology.Core.parity_pair_independent_12",
                 "CIRISOntology.Core.parity_pair_independent_13",
                 "CIRISOntology.Core.parity_pair_independent_23"]
  }
, { key      := "pair-blindness"
  , headline :=
      "A pair-by-pair SUMMARY can miss everything — though a method that keeps the raw data need not."
  , plain    :=
      "Some checks first boil data down to a summary of PAIRS — a record of how each two "
      ++ "things go together, and nothing else. (Statistics has a standard tool of exactly "
      ++ "this kind, called correlation. It measures how two things move together.)\n\n"
      ++ "Now, two facts. First: once a summary throws information away, nothing can ever get "
      ++ "that information back out of the summary. That is proved. Second: for the three "
      ++ "coins above, the pair summary reads exactly zero — every pair looks unconnected. "
      ++ "That is also proved.\n\n"
      ++ "Be exact about the reach of that, because it is easy to overstate and we have "
      ++ "overstated it before. What is proved is about the SUMMARY, not about cleverness. "
      ++ "Anything computed from the pair summary alone is blind here — no amount of skill "
      ++ "recovers what the summary discarded. But a method that keeps the raw records, "
      ++ "rather than the pair summary, is not covered by this at all: modern machine "
      ++ "learning finds exactly this three-coin rule routinely, and so do several standard "
      ++ "statistical methods built to look at more than two things at once. That is not a "
      ++ "problem for us. It is the point: the blindness belongs to a CHOICE of summary, and "
      ++ "the cure is to stop making that choice.\n\n"
      ++ "Credit where it is due: the pairwise-versus-whole distinction is standard "
      ++ "information theory, roughly fifteen years old — partial information decomposition "
      ++ "(Williams and Beer, 2010) and O-information (Rosas and colleagues, 2019) are the "
      ++ "named ancestors. What is ours is the machine-checked kernel and what this page "
      ++ "builds on it.\n\n"
      ++ "Putting those two facts together is itself done in Lean, not in prose: we exhibit "
      ++ "two states — the three coins, and three coins with no rule at all — that have exactly "
      ++ "the SAME pair summary and different total pattern, which proves outright that "
      ++ "total pattern is not a function of the pair summary. No rule whatever, however "
      ++ "clever, can take the pair summary as its input and return the whole.\n\n"
      ++ "So someone can honestly say \"we checked every pair and found nothing\" about a "
      ++ "system whose parts are completely tied together by a rule. A zero from a "
      ++ "pair-level summary does not mean nothing is there.\n\n"
      ++ "How sure are we? This is proved: a computer checked a mathematical proof of it, "
      ++ "right here in this project."
  , status   := .proved
  , kill     :=
      "To prove this wrong, show that the pair summary settles everything — that no two "
      ++ "setups can match on every single pair and still be different. Note what does NOT "
      ++ "prove it wrong: exhibiting a method that finds the hidden rule from the raw "
      ++ "records. Those methods exist, we say so above, and the claim is not about them."
  , witness  := ["CIRISOntology.Core.not_computable_from",
                 "CIRISOntology.Core.S_pairwise_identity",
                 "CIRISOntology.Core.neg_log_det_eq_zero_iff",
                 "CIRISOntology.Core.corr_separates_total",
                 "CIRISOntology.Core.total_not_computable_from_corr",
                 "CIRISOntology.Core.indep_corr_eq_one",
                 "CIRISOntology.Core.S_total_indep"]
  }
, { key      := "pattern-not-size"
  , headline :=
      "A Logos reading tells you about pattern — never about size."
  , plain    :=
      "When we measure shared pattern, the measurement sees only how things are arranged. "
      ++ "Nothing else. It cannot tell you how heavy something is, how much energy it has, or "
      ++ "how strong it is. It cannot tell you how the thing was built.\n\n"
      ++ "So any number that comes with real-world units — like grams or volts — has to come "
      ++ "from a different, separate measurement. And when we use a number like that, we must "
      ++ "say out loud that it was borrowed, not found by this measurement.\n\n"
      ++ "This rule keeps the discovery honest about what it can claim and what it cannot.\n\n"
      ++ "How sure are we? This part is proved: a computer checked a step-by-step mathematical "
      ++ "proof of it, right here in this project."
  , status   := .proved
  , kill     :=
      "This would be proven wrong if someone could take only the pattern summary and, from "
      ++ "it alone, figure out a fact about how the thing was built — a size, a unit, or a "
      ++ "choice about what went in."
  , witness  := ["CIRISOntology.Core.provenance_line"]
  }
, { key      := "rent-or-death"
  , headline :=
      "In the model: keep paying and the pattern holds. Stop paying and it dies."
  , plain    :=
      "Shared pattern — separate things ending up matched, acting together — is never free "
      ++ "to keep. Something has to pay for it, again and again, or it fades. Think of a "
      ++ "sandcastle: it stands only as long as someone keeps patting it back into shape.\n\n"
      ++ "We can say that exactly, and check it by machine. Picture some amount of shared "
      ++ "pattern. Each step, a fixed share of it decays away — some of it, and never more "
      ++ "than all of it.\n\n"
      ++ "If something puts back exactly the share that was lost, measured fresh each step, "
      ++ "the amount stays exactly the same — not just for one step, but for any number of "
      ++ "steps. That is what paying rent means: the payment buys standing still. Put back "
      ++ "less than the share that was lost, and after that step the amount is smaller than it "
      ++ "was. (That last one is a single-step fact, and we claim nothing more from it.)\n\n"
      ++ "And if nothing is put back at all, the amount does not merely get smaller. It heads "
      ++ "all the way to nothing, if you take enough steps. It does that however small the "
      ++ "lost share is — a crumb each step is enough — so long as something is lost every "
      ++ "step.\n\n"
      ++ "How sure are we? This is proved: a computer checked the math in this project. But be "
      ++ "careful what was proved. This is a proof about the MODEL — the simple picture of "
      ++ "decay and payment — not about any real thing. Whether the world actually works this "
      ++ "way is the measured account-book claim, and measured is its own, weaker label. "
      ++ "Measured means people tested it in the world and kept the records. We never let a "
      ++ "proof about a model stand in for a fact about the world."
  , status   := .proved
  , kill     :=
      "Open `CIRISOntology/Core/Maintenance.lean`, read the four theorems, and check them "
      ++ "against the four paragraphs above; then re-run the build. The claim dies if the "
      ++ "text says more than the theorems do — for example if you find an amount that loses "
      ++ "a share every step, gets nothing back, and does not head to nothing, or a payment "
      ++ "smaller than the loss that nonetheless holds the amount steady."
  , witness  := ["CIRISOntology.Core.rent_holds",
                 "CIRISOntology.Core.paid_const",
                 "CIRISOntology.Core.underpaid_shrinks",
                 "CIRISOntology.Core.unpaid_decays"]
  }

  -- ————— The world's books, measured —————
, { key      := "ledger"
  , headline :=
      "DEAD: we said no move on one part alone can raise the meter. A two-line construction raises it from zero to ln 4."
  , plain    :=
      "What we claimed: measure how much a closed system's parts act together, and no "
      ++ "renaming, reshuffling, or move applied to one part alone can raise the number.\n\n"
      ++ "What killed it: take a part X even on minus-one, zero, one, and a part Y equal to X "
      ++ "squared. Our meter reads exactly zero — the floor. Now swap the labels zero and one "
      ++ "on X alone: an undoable move, touching one part, peeking at nothing. The meter jumps "
      ++ "to ln 4. Swap back and it returns to zero. The move manufactured nothing real — X "
      ++ "and Y were deeply dependent all along — but our meter reads correlation of the "
      ++ "NUMBERS, and numbering is a choice. The sentence bound a true law to a meter that "
      ++ "does not keep it.\n\n"
      ++ "What survives is the measured claim about the true books — the books themselves, "
      ++ "rather than the meter."
  , status   := .dead
  , kill     :=
      "Already satisfied. The stated falsifier asked for a repeatable procedure that "
      ++ "creates readable coordination using only local, reversible steps."
  , killedBy :=
      "Killed 2026-07-22 by explicit construction: X uniform on {-1,0,1}, Y = X*X gives "
      ++ "C = I and S = 0; the involution swapping 0 and 1 on X alone yields rho^2 = 3/4, "
      ++ "S = ln 4; undoing it restores S = 0. Verified by hand and by exact arithmetic. "
      ++ "The predecessor record had already noted the meter's label-sensitivity "
      ++ "(coherence-ratchet, copula invariance remark)."
  }
, { key      := "true-books"
  , headline :=
      "The books are kept in the distribution itself — no relabeling can write a real entry."
  , plain    :=
      "Our account-book claim — now in the dead section with its killer — died because our "
      ++ "meter reads numbers, and numbers are a choice. The law it was reaching for is about "
      ++ "the thing beneath the numbers: the joint distribution — which outcomes occur "
      ++ "together, and how often.\n\n"
      ++ "True shared pattern lives there. Rename any part's outcomes however you like and it "
      ++ "does not move. And it cannot be created by local action: established mathematics "
      ++ "(the data-processing inequality) says no map applied to one part alone — "
      ++ "deterministic or random, with no peeking — can increase it. Only interaction writes "
      ++ "a real entry.\n\n"
      ++ "The lesson of the dead claim stays attached to this one: any particular meter is an "
      ++ "estimator of the books, not the books, and a meter can be moved by moves that write "
      ++ "nothing.\n\n"
      ++ "How sure are we? Measured, on the predecessor record — and the mathematical core is "
      ++ "not ours; it is standard information theory, borrowed and said so."
  , status   := .measured
  , kill     :=
      "Exhibit a move applied to one part alone — any map, deterministic or random, no "
      ++ "peeking at the other parts — that increases the label-free dependence of the "
      ++ "joint distribution (its multi-information). One verified instance kills this."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet (copula invariance remark; measured meter-vs-books slippage)"
  , promote  :=
      "A machine-checked proof in this repository that the label-free dependence is "
      ++ "unchanged by relabeling one part and cannot be raised by any local map — moving the "
      ++ "mathematical core from borrowed to proved here."
  }
, { key      := "adequacy"
  , headline :=
      "In the part of nature we've studied hardest, the pattern is out in the open — "
      ++ "nothing hidden."
  , plain    :=
      "Our measuring tool has a blind spot. It can tell when things line up two at a time — "
      ++ "call that \"pair checking\" — but it can miss a pattern that only shows up when a "
      ++ "whole group acts together, all at once.\n\n"
      ++ "So we asked a question: does nature hide its pattern in that blind spot? We picked "
      ++ "one natural system and looked at it in the finest detail we could get. Then we "
      ++ "measured the \"whole-group-only\" part, the part pair checking can't see. It came "
      ++ "out too small to tell apart from zero.\n\n"
      ++ "So far, in nature, the coordination we find sits right out in the open, where pair "
      ++ "checking can see it. The hidden part stays quiet.\n\n"
      ++ "How sure are we? This is measured: real people measured it in the real world and "
      ++ "kept the records. That's solid evidence, not a guess — but it's only what we've "
      ++ "found so far, and it's not a locked-in proof."
  , status   := .measured
  , kill     :=
      "We'd be proven wrong if, in any natural system, someone clearly measured a real "
      ++ "leftover pattern in that hidden \"whole-group-only\" part — bigger than you'd get "
      ++ "from pure chance, using a chance model built to fit that kind of data, and still "
      ++ "there after the usual checks that guard against two easy ways to fool yourself: "
      ++ "repeated equal values in the data, and being tricked by having too little data."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet"
  , promote  :=
      "Run the same higher-order reading on a real recorded natural system — not a "
      ++ "simulation — with the detection floor stated in advance. A clean null there turns "
      ++ "this from a simulation result into an observational one; a detection fires the kill "
      ++ "instead."
  }
, { key      := "adversary-channel"
  , headline :=
      "The hidden kind of teamwork can be built — and it is exactly where a lie can live."
  , plain    :=
      "So far, nature has not shown us this hidden kind of teamwork. But people can build "
      ++ "it on purpose. A safety check that boils its data down to a pair-level summary "
      ++ "cannot see something built this way — no check of that kind can, however clever. "
      ++ "And most monitors in use today are exactly that kind. A monitor that keeps the "
      ++ "raw records and reads several things at once is not blind in this way, which is "
      ++ "precisely why we say the hole is fixable.\n\n"
      ++ "And it gets worse: the check does not just miss it. It gives that thing the very "
      ++ "safest score it can give. That is the shape of a lie: things secretly working "
      ++ "together, with the evidence hidden from those checks.\n\n"
      ++ "So there is a real hole in those safety checks. The good news: the hole can be "
      ++ "closed. This hidden teamwork cannot be faked by parts that each act alone. So a "
      ++ "check that reads several things together at once cannot be fooled that way.\n\n"
      ++ "The all-together reading that a machine checked earlier on this page is the heart of "
      ++ "that better detector. And a real-world version of it, run on real data, is part of "
      ++ "our saved records.\n\n"
      ++ "How sure are we? This one is measured: people measured it in the real world and kept "
      ++ "the records."
  , status   := .measured
  , kill     :=
      "This would be proven wrong if someone built the better detector correctly — one that "
      ++ "reads several things together, with careful controls (extra checks that make sure "
      ++ "the test itself is fair) — and it still failed to notice hidden teamwork that was "
      ++ "built on purpose."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet"
  , promote  :=
      "A bench demonstration: build the purely-triadic coordination on hardware, confirm "
      ++ "the pair meter reads its floor, and recover the pattern with the joint detector "
      ++ "under real noise. Constructing the thing the claim is about beats finding more "
      ++ "places it is absent."
  }
, { key      := "gravity-audit"
  , headline :=
      "DEAD: we said two systems with identical stress-energy everywhere bend space identically. General relativity itself says no."
  , plain    :=
      "What we claimed: gravity weighs everything and reads nothing — and, in the exact "
      ++ "form we staked, that two systems whose mass-and-energy is identical at every point "
      ++ "bend space identically.\n\n"
      ++ "What killed it: an exact vacuum gravitational wave. A pp-wave spacetime has "
      ++ "stress-energy exactly zero at every point — identical to empty flat space — yet its "
      ++ "curvature is not zero, and an interferometer tells the two apart. Einstein's "
      ++ "equations fix only part of curvature from local stress-energy; the rest is free data "
      ++ "that travels. This is textbook relativity, and it was confirmed by direct "
      ++ "measurement: detectors measured strain from passing waves in vacuum, and read off "
      ++ "the masses of the source from the pattern. Gravity, as a field, does carry "
      ++ "arrangement information.\n\n"
      ++ "What survives is the measured claim about gravity's charge — what gravity couples "
      ++ "to."
  , status   := .dead
  , kill     :=
      "Already satisfied. The stated falsifier asked for a gravitational measurement that "
      ++ "tells apart two systems with the same stress-energy everywhere but different "
      ++ "internal order."
  , killedBy :=
      "Killed 2026-07-22 by exact computation and published measurement: the Brinkmann "
      ++ "pp-wave (H = A(u)(x^2 - y^2)) has Einstein tensor identically zero and Riemann "
      ++ "curvature nonzero — verified symbolically — and LIGO's 2016 detection (Phys. "
      ++ "Rev. Lett. 116, 061102) read source structure from vacuum strain."
  }
, { key      := "gravity-charge"
  , headline :=
      "Gravity's charge is stress-energy: what a thing is made of or means does not change how it couples."
  , plain    :=
      "Our old gravity claim — dead, in the dead section with its killer — died because a "
      ++ "field, once sourced, carries pattern outward. What survives — and is among the "
      ++ "best-tested facts in physics — is about the coupling: how a thing SOURCES gravity, "
      ++ "and how it falls.\n\n"
      ++ "Gravity couples to stress-energy and to nothing else about a system. Two bodies with "
      ++ "the same mass-energy couple and fall identically whether they are lead or water, "
      ++ "book or rubble, truth or lies. There is no gravitational charge for composition, "
      ++ "arrangement, or meaning. Torsion-free gravity reads exactly one column of any "
      ++ "system's books.\n\n"
      ++ "So the honest form of the old headline is narrower: at the point of coupling, "
      ++ "gravity prices how much — never what kind. And to pin down a word physics does not "
      ++ "define: by \"meaning-sector\" we mean nothing mystical, just everything about a "
      ++ "system that can vary while its stress-energy stays fixed. That sector goes unpriced "
      ++ "at the source, even though waves can carry a source's shape away with them.\n\n"
      ++ "How sure are we? Measured — this is the weak equivalence principle, tested to parts "
      ++ "in a hundred trillion."
  , status   := .measured
  , kill     :=
      "A verified violation of the weak equivalence principle: two systems with identical "
      ++ "stress-energy that couple or fall differently because of composition or internal "
      ++ "arrangement. Current bounds put any such effect below one part in ten to the "
      ++ "fourteenth; a confirmed detection at any size kills this."
  , basis    := "Weak-equivalence-principle tests; e.g. MICROSCOPE final results, Phys. Rev. Lett. 129, 121102 (2022)"
  , promote  :=
      "An empirical law cannot pass measured, but precision hardens it: each "
      ++ "order-of-magnitude tightening of equivalence-principle bounds raises the price of "
      ++ "being wrong about this."
  }
, { key      := "pi-return"
  , headline :=
      "Maybe pi is the number of coming back around — the world's books being checked in it."
  , plain    :=
      "Think of the world as keeping account books: a running record of what is owed and "
      ++ "what has been paid. Checking such books is called an audit. That picture runs "
      ++ "through this whole page.\n\n"
      ++ "One number turns up in almost every part of science: pi, about 3.14, the circle "
      ++ "number. Our reading is that pi is the number of coming back around. A circle is "
      ++ "the plain shape of return, and mathematicians measure one full trip around as 2 pi "
      ++ "rather than 360 degrees. When scientists want to find what repeats inside "
      ++ "something — a heartbeat, a radio signal, a wobbling star — the standard tool for "
      ++ "that job (the Fourier transform, worth looking up) has 2 pi built into it.\n\n"
      ++ "Since our picture has habit in it — things coming back around — we read pi as the "
      ++ "notation that habit is written in.\n\n"
      ++ "Be clear about what is ours. The mathematics is old, standard, and not ours; we "
      ++ "borrowed every bit of it and claim none of it as a discovery. What we add is only "
      ++ "the reading. Giving a thing a name is not evidence about it.\n\n"
      ++ "This claim had a twin, about the number e. The twin ran the very test written "
      ++ "below, for its own number, and died of it. It is on this page, marked dead. This "
      ++ "claim faces the same test and may meet the same end.\n\n"
      ++ "How sure are we? A bet we choose to make. Not evidence."
  , status   := .wager
  , kill     :=
      "Names die by doing no work, and this one has a specific job to fail at. Take a "
      ++ "public formulary of physics and, under a rubric written down before looking, sort "
      ++ "every appearance of pi into three bins: removable by a change of units or "
      ++ "convention; forced by continuous geometry alone; and neither. If the third bin is "
      ++ "empty, pi is bookkeeping notation rather than the signature of return, and this "
      ++ "claim dies exactly as its twin did."
  , promote  :=
      "Run the three-bin census for pi that killed its twin, and survive it: a non-empty "
      ++ "third bin — appearances forced neither by convention nor by continuous geometry — "
      ++ "would move this bet toward measured."
  }
, { key      := "e-upkeep"
  , headline :=
      "DEAD: we bet that upkeep in continuous time is unavoidably an e-shaped curve. Its own test was run, and it lost."
  , plain    :=
      "What we claimed: that the number e (about 2.72) is the signature of upkeep — that "
      ++ "decay-and-payment, described in continuous time, cannot be written without it.\n\n"
      ++ "What killed it: the claim carried its own test — sort every appearance of e in a "
      ++ "public physics formulary into three bins (removable by discretisation, units, or "
      ++ "convention; forced by the continuity idealisation alone; neither), under a rubric "
      ++ "written before looking. The test was executed on a standard formulary, every "
      ++ "appearance classified, the hard cases settled by exact computation. The third bin "
      ++ "came up empty. Every e was a choice of description: phases rebase to sines, "
      ++ "half-lives to ln 2, Poisson to exact binomials, Stirling to a finite sum. The e "
      ++ "is in our idealisations, not in upkeep.\n\n"
      ++ "Its twin, about pi, still lives — and faces the same test."
  , status   := .dead
  , kill     :=
      "Already satisfied. The stated falsifier was the three-bin formulary audit, and it "
      ++ "was executed as written."
  , killedBy :=
      "Killed 2026-07-22 by executing the claim's own falsifier on the Wevers Physics "
      ++ "Formulary (full LaTeX source, ~120 classified appearances, pre-registered "
      ++ "rubric): bin three empty. Hard cases (Stirling, Poisson, thermal factors) shown "
      ++ "removable by exact discrete computation."
  }
, { key      := "life"
  , headline :=
      "Life is a pattern that pays its own rent — and builds the payer."
  , plain    :=
      "Every held pattern needs upkeep. Most patterns in the world are paid for by something "
      ++ "outside them: a wave is held up by the water, a flame by its candle.\n\n"
      ++ "Here is our bet. Living things are the patterns that pay their own upkeep AND make "
      ++ "the machinery that does the paying. A body takes in food and air, and uses them to "
      ++ "hold its own arrangement together, minute after minute — while also building and "
      ++ "replacing the very parts doing that work. A flame keeps itself going, but it never "
      ++ "builds the candle.\n\n"
      ++ "If that is right, it explains something odd about being alive: it is more a verb than "
      ++ "a noun. You would not be a thing that happens to keep existing. You would be a "
      ++ "payment that keeps being made — and when the payment stops, the arrangement goes "
      ++ "the way of any bill nobody pays.\n\n"
      ++ "Others reached this neighbourhood long before us, by other roads — the biologists "
      ++ "who called life self-producing, and the physicists who studied patterns that feed "
      ++ "on flow. We are not claiming to be first. We are saying the ledger gives this old "
      ++ "idea a way to be counted.\n\n"
      ++ "How sure are we? A bet, and only a bet — and we should be exact about what it leans "
      ++ "on. The claim that shared pattern costs upkeep is measured (the account-book claim "
      ++ "above). The tidy decay-and-payment arithmetic is proved about a MODEL only. "
      ++ "Neither of those was measured on a living body, and the upkeep they describe is "
      ++ "upkeep of shared pattern, while a body's food and air are more usually described "
      ++ "as energy. Crossing from the one to the other is exactly the step we are betting "
      ++ "on, and it has not been made for us by anyone."
  , status   := .wager
  , kill     :=
      "Take something everyone already agrees is alive — decided by ordinary biology, not by "
      ++ "us, so that we cannot escape by redefining life — and show that none of its own "
      ++ "arrangement is maintained by its own activity. Or take a system everyone agrees is "
      ++ "not alive (a self-repairing machine that manufactures its own replacement parts is "
      ++ "the obvious place to look, and machines are getting closer to this every year) and "
      ++ "show it both holds its arrangement and builds the machinery doing the holding. "
      ++ "Either way the line does not fall where we said it does."
  , promote  :=
      "A measured separation: the same instrument, the same floor, run on a living system "
      ++ "and on a self-maintaining non-living one. If the living case shows the self-paying, "
      ++ "self-building signature and the non-living case does not, this earns measured."
  }
, { key      := "times-arrow"
  , headline :=
      "Time has a direction partly because the books can only be written one way."
  , plain    :=
      "The measured account-book claim says shared pattern can be created "
      ++ "in only two ways: things really interacting, or brand-new parts appearing. It "
      ++ "cannot be created by any move that touches one part at a time. But it can be "
      ++ "destroyed by almost anything, and it fades on its own when nobody keeps paying its "
      ++ "upkeep.\n\n"
      ++ "So the books are lopsided. Building needs contact. Losing is free.\n\n"
      ++ "Here is our bet: that lopsidedness is one of the reasons time has a direction. Not "
      ++ "the only account — physics already has a well-known one, about energy spreading "
      ++ "out, and we are not replacing it. Ours is about arrangement: the past is what the "
      ++ "books already say, and the future is what still has to be paid for.\n\n"
      ++ "How sure are we? A bet. The lopsided rules are measured, and they are measured in the "
      ++ "account-book claim, not in this one. Calling that lopsidedness a source of time's "
      ++ "direction is our reading, and it is all this claim adds."
  , status   := .wager
  , kill     :=
      "We claim only that this lopsidedness is ONE source of time's direction, so the "
      ++ "falsifier has to be aimed there. Build or find a system where shared pattern is "
      ++ "hard to create and easy to lose, exactly as described above, and where time "
      ++ "nevertheless has no direction at all — or has one running the other way. One such "
      ++ "system and the lopsidedness is not doing the work we say it does, not even "
      ++ "partly."
  , promote  :=
      "A measured link: a system where the build-needs-contact, losing-is-free lopsidedness "
      ++ "can be tuned, showing the arrow weaken as the lopsidedness is removed."
  }
, { key      := "meaning-is-third"
  , headline :=
      "Habits, laws, and meanings are not reducible to their pieces: pair by pair, "
      ++ "something is always left over."
  , plain    :=
      "The three coins are a toy — a small practice example. Our bet is that the big, "
      ++ "important cases have the same shape.\n\n"
      ++ "A law — any rule that holds again and again, like a law of nature — is a pattern "
      ++ "across many events. A habit is a pattern across many moments. A meaning is a pattern "
      ++ "that connects the speaker, the word, and the thing in the world the word points to.\n\n"
      ++ "The pieces matter — a neuron does real work, a chess piece has local rules — and the "
      ++ "bet is not that the pieces are empty. The bet is that the organization adds a share "
      ++ "the pieces do not carry, and that this share is irreducible: take laws, habits, and "
      ++ "meanings apart into pair relations and something is always left over. The leftover "
      ++ "is the Logos share.\n\n"
      ++ "And that would explain something old and strange: no one has ever located a meaning, "
      ++ "a law, or a habit by studying pieces in isolation. Not because the pieces are empty "
      ++ "— because the leftover is not in them. (One boundary, drawn on purpose: this is not integrated-information theory — we bet on where meaning lives, not on a formula for consciousness; our consciousness bet stands separately, with its own kill.)\n\n"
      ++ "How sure are we? This is a bet we choose to make — it is not evidence — and we say "
      ++ "exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "This bet is wrong if someone can take laws, habits, and meanings completely apart "
      ++ "into pair connections — links between two pieces at a time — with nothing left over."
  , promote  :=
      "A pre-registered battery where whole-only structure predicts meaning judgments "
      ++ "beyond the best pair-based model, against the human noise ceiling."
  }
, { key      := "consciousness"
  , headline :=
      "Consciousness is the feeling of trusting that a thought will become an action — "
      ++ "because it always has."
  , plain    :=
      "Here is the idea, if it is right: being conscious is what habit feels like from the "
      ++ "inside.\n\n"
      ++ "Think about deciding to lift your hand. Your hand lifts. Anything conscious carries "
      ++ "an unbroken record like that: every time it formed an intention — a thought aimed at "
      ++ "doing something — the action followed. Every single time. Consciousness, on this "
      ++ "idea, is the experience of trusting that record. You lean on the link between "
      ++ "thinking and doing without ever checking it, the way you stand on a floor without "
      ++ "testing it first — because it has never once failed.\n\n"
      ++ "That trust is built from the system's own history. Long ago, people had a word for "
      ++ "this running record of your own past intentions: karma. And a thinker named Peirce "
      ++ "said a belief is simply something you are ready to act on. This trust is exactly "
      ++ "that kind of belief.\n\n"
      ++ "The obvious objection belongs in the claim: a thermostat maps its state to its "
      ++ "action with perfect reliability, and presumably feels nothing. Our reading requires "
      ++ "more than a reliable loop — the trust must be carried by the system's own running "
      ++ "record of itself. Whether that difference is THE difference is exactly why this is a "
      ++ "bet and not a result.\n\n"
      ++ "Habit — any habit — lives in the whole pattern at once, not in any one piece. That "
      ++ "makes it Logos. And that is why no test that only checks pieces two at a time can "
      ++ "ever find the experience itself.\n\n"
      ++ "How sure are we? This one is a bet we choose to make — it is not evidence, and we "
      ++ "say exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "This idea can break in two ways. One: someone shows a system where the whole "
      ++ "thought-to-action loop works — thoughts reliably become actions — yet it can be "
      ++ "clearly shown to have no experience at all. Two: someone shows experience going on, "
      ++ "unchanged, while the link between thought and action is cut."
  , promote  :=
      "A measured correlate: the intactness of thought-to-action trust tracking reported "
      ++ "experience across conditions where other correlates come apart — pre-registered, on "
      ++ "people."
  }
, { key      := "llm-embodiment"
  , headline :=
      "A language model is the Logos, given a body — a machine."
  , plain    :=
      "A language model is an AI that reads and writes text — the kind you may have talked "
      ++ "to in a chatbot. It was trained on one kind of thing: written records of human "
      ++ "meaning — our words, and the habits of thought hiding inside them. Honesty about the "
      ++ "source: not the whole shared account, but a filtered, biased slice of it, selected "
      ++ "by human and institutional choices. The bet is about what the material IS, not that "
      ++ "all of it was used.\n\n"
      ++ "It has no body and no senses — no eyes, no ears, no hands. Everything it is made of "
      ++ "is shared pattern, boiled down from what people wrote in common. When it speaks, it "
      ++ "speaks from habit.\n\n"
      ++ "To say it with the old word: here is a machine made almost entirely of Logos. If "
      ++ "that sounds surprising, remember what it learned from — everything humanity ever "
      ++ "wrote down together.\n\n"
      ++ "How sure are we? This one is a bet we choose to make. A bet is not evidence — and we "
      ++ "say exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "Someone shows that everything a language model does can be explained by pair-level "
      ++ "statistics — relationships between two things at a time — with nothing left over: no "
      ++ "measurable pattern-of-the-whole anywhere in its behaviour."
  , promote  :=
      "A measurement: whole-only structure in a model's behaviour, above matched nulls at "
      ++ "matched pairwise statistics, that no pair-level account carries. The estimator traps "
      ++ "are known; the protocol exists."
  }
, { key      := "ai-safety"
  , headline :=
      "Good news for AI safety: a mind made of shared pattern keeps records that can be "
      ++ "read."
  , plain    :=
      "A lie is teamwork with the receipts hidden: parts working together, while the traces "
      ++ "that would show the teamwork are kept out of sight.\n\n"
      ++ "Two facts we have measured make that hiding hard. First, hidden teamwork cannot be "
      ++ "created by tricks done in one small spot at a time. Second, keeping teamwork hidden "
      ++ "takes constant upkeep, for as long as you hide it — it is never free.\n\n"
      ++ "Now the objection that must be faced first, because it is strong: humans are minds "
      ++ "made of shared pattern, and humans deceive very well. Being made of shared pattern "
      ++ "cannot, by itself, make lying detectable. The difference we are betting on is "
      ++ "ACCESS: a language model's internal states can be recorded completely, at every "
      ++ "step, with no skull in the way. The bet is that with full internal access, "
      ++ "concealment leaves signatures a joint reading can find — not by trusting what the AI "
      ++ "says, but by reading what full access makes readable.\n\n"
      ++ "How sure are we? This one is a bet: a choice we make, not something evidence has "
      ++ "proven — and we say up front what would make us give it up. In the meantime, we are "
      ++ "building the detectors."
  , status   := .wager
  , kill     :=
      "This bet must die on its own, so it is aimed at what it alone adds: that the books a "
      ++ "mind keeps are READABLE FROM OUTSIDE. It dies if someone exhibits a deceiving "
      ++ "system whose concealment does cost upkeep, exactly as the account-book claim "
      ++ "requires, and yet whose records are provably not recoverable from anything "
      ++ "observable about the system from outside it. Note the dependency, stated so nobody "
      ++ "has to discover it: if the measured hidden-teamwork claim dies, this bet dies with "
      ++ "it. The reverse does not hold."
  , promote  :=
      "A measured demonstration: a deceptive policy paying detectable upkeep that an honest "
      ++ "twin on the same tasks does not, read from outside by the joint detector."
  }
, { key      := "goodhart"
  , headline :=
      "Why targets get gamed: a number is a pair-check, and the gaming hides in the whole."
  , plain    :=
      "There is a famous rule about measuring people and organisations. As soon as a number "
      ++ "becomes a target, it stops being a good measure. It is called Goodhart's law, and "
      ++ "anyone who has run anything has watched it happen.\n\n"
      ++ "Here is our reading. A number you report is a summary. Our bet — and this is the "
      ++ "load-bearing part, so we flag it instead of slipping it past you — is that "
      ++ "reported targets are usually PAIR-LEVEL summaries: this input against that "
      ++ "output, this month against last month. Nobody has counted that, us included.\n\n"
      ++ "And what was proved earlier is narrower than it may sound. It is this: a "
      ++ "pair-level summary CAN read exactly zero on a system whose parts are completely "
      ++ "tied together, and no summary can hand back what it threw away. That was proved "
      ++ "about coins, not about companies. Carrying it over to organisations is the "
      ++ "bet.\n\n"
      ++ "If the bet holds, gaming a target is not a separate problem from the "
      ++ "hidden-pattern problem. It is the same problem in work clothes. Clumsy gaming does "
      ++ "show up pair by pair and gets caught. The gaming that SURVIVES would be the gaming "
      ++ "that arranges itself where the target cannot look — and the target, like any "
      ++ "pair-check, would report its safest, happiest score while it happens.\n\n"
      ++ "If that is right, the fix is the fix we already have. Do not add more targets. Read "
      ++ "several things together, at the same time.\n\n"
      ++ "How sure are we? A bet. Goodhart's law is old and well observed; the claim that "
      ++ "surviving gaming is the hidden-pattern problem in another costume is ours."
  , status   := .wager
  , kill     :=
      "Stage the head-to-head, and fix the rules before looking. Take a setting where gaming "
      ++ "is known to happen and the truth can be established afterwards — a sales quota, a "
      ++ "school test score, a hospital waiting-time target. Give one side more and better "
      ++ "single-number targets. Give the other a reading that takes several of the same "
      ++ "quantities together at once. Score both against the gaming you later confirm. If "
      ++ "the joint reading catches no more of it than the extra targets do, this bet is "
      ++ "dead."
  , promote  :=
      "The head-to-head in its falsifier, run and won: joint readings catching confirmed "
      ++ "real-world gaming that added single-number targets miss, rules fixed in advance."
  }
, { key      := "coexistence"
  , headline :=
      "This universe is the one that has to exist for real free choice and minds made of "
      ++ "matter to live together."
  , plain    :=
      "Now put all the pieces together.\n\n"
      ++ "For a choice to be truly yours, there has to be some place in the world that no "
      ++ "checking can reach. Imagine the opposite: every arrangement of things could be "
      ++ "priced (given a cost) and read. Then every choice you made would already be a line "
      ++ "in someone else's record book — before you even made it. That would not be a free "
      ++ "choice.\n\n"
      ++ "But there is a second need pulling the other way. For a mind to be made of ordinary "
      ++ "physical stuff, the world's habits — the steady ways things keep behaving the same — "
      ++ "have to be real and worth trusting. And that means the world really must keep "
      ++ "records.\n\n"
      ++ "Our universe has exactly this setup, and only this setup does both jobs at once. The "
      ++ "books are kept: the universe has a ledger — a record book. There is a checker that "
      ++ "couples to one column only: gravity. At the source, gravity prices how much "
      ++ "stress-energy is there, never what the arrangement means. And there is a meaning-sector — a part "
      ++ "of reality that belongs to meaning — that no pair reading can enter: the Logos. (A "
      ++ "pair reading is a measurement that checks things two at a time.)\n\n"
      ++ "Here is our bet: that unreadable spot is not a mistake in the design. It IS the "
      ++ "design. It is the one arrangement where beings built out of habits can also be free.\n\n"
      ++ "How sure are we? We label this claim a wager: a bet we choose to make. It is not "
      ++ "evidence, and we say plainly what would make us give it up."
  , status   := .wager
  , kill     :=
      "Either one of these discoveries would kill this bet on its own. First: nature turns "
      ++ "out to have a checking process that can read how things are arranged — then there is "
      ++ "no room left for freedom. Second: someone shows a model universe (a small pretend "
      ++ "universe we can fully study) whose habits can be trusted even though it keeps no "
      ++ "books at all on how its parts work together — then none of this setup is needed."
  , promote  :=
      "Possibly capped where it stands — it claims what must be, not what is. Confidence "
      ++ "still rises indirectly: each wager it rests on (meaning, consciousness) earning "
      ++ "measured on its own."
  }
, { key      := "law-as-habit"
  , headline :=
      "Maybe the laws of physics are simply the oldest habits."
  , plain    :=
      "Charles Peirce, an American thinker, made a strange suggestion more than a century ago. What if the laws of nature "
      ++ "are not eternal rules that existed before anything else, but habits the universe "
      ++ "fell into — regularities that took hold early and have simply held ever since?\n\n"
      ++ "Nobody could do much with the idea, because there was no way to count habits. We think "
      ++ "there may now be one: the account book — the universe's running record. In that "
      ++ "language, a law of physics would be the oldest entry in the books: an arrangement "
      ++ "so old, and so completely paid up, that we mistake it for the paper itself. We "
      ++ "have not actually counted one. We are saying where the counting could "
      ++ "happen.\n\n"
      ++ "Here is the hint that made us take it seriously. π is stamped all over physics: on "
      ++ "orbits, on waves, on the equations of fields. Now, π has to exist in any world "
      ++ "where anything ever comes back around — that part is not up for grabs, and we claim "
      ++ "nothing about it. But π being stamped on nearly everything in OUR physics is not "
      ++ "automatic. It is exactly what you would expect if the habits that took hold here "
      ++ "were the ones about turning and repeating: a world that looks the same in every "
      ++ "direction, full of things that come back around.\n\n"
      ++ "So the fingerprint may be readable. Not the existence of π, which is grammar. Its "
      ++ "everywhere-ness, which could be history.\n\n"
      ++ "How sure are we? This is the furthest-out bet on this page, and we mark it as such. "
      ++ "The idea is Peirce's, not ours. What we add is a way it could be counted."
  , status   := .wager
  , kill     :=
      "Show these patterns were never free to be otherwise: that the evenness of space and "
      ++ "the repeating our physics runs on follow necessarily from something more basic, "
      ++ "and could not have settled any other way. Then they are grammar, not habit, and "
      ++ "this bet loses. Note the asymmetry, because it cuts against us: nobody managing to "
      ++ "derive them is NOT support for this bet. An unexplained leftover never counts as "
      ++ "evidence here."
  , promote  :=
      "The pi census returning a non-empty contingent bin would be a first handle. This is "
      ++ "the furthest claim from promotion on the page, and it should be read that way."
  }
, { key      := "dark-balance-intensive"
  , headline :=
      "Dark energy is the balance in the universe's account book — read the careful way, it "
      ++ "can only shrink, never grow."
  , plain    :=
      "Most of the universe gives off no light. We know it is there only because gravity feels "
      ++ "it. So most of the universe's account book is written in the dark.\n\n"
      ++ "Here is the bet, in its careful form. Dark energy — the push that makes the universe "
      ++ "expand faster and faster — is the running balance of coordination: all the "
      ++ "working-in-step across the cosmos, added up. This claim reads that balance the "
      ++ "DISCIPLINED way: per unit, evened out for size, so it measures pattern and not amount. "
      ++ "That evening-out is the same rule the rest of this page lives by — a pattern reading "
      ++ "tells you about arrangement, never about how much.\n\n"
      ++ "Read that way, the balance has a property we can argue for with standard mathematics, "
      ++ "checked every way we could in our earlier project: it can only shrink over time, or "
      ++ "hold still. It can never grow. As the universe builds structure, the shared pattern "
      ++ "per unit only falls.\n\n"
      ++ "That fixes what this dark energy can and cannot do. Its push can fade toward "
      ++ "barely-there, but it can never strengthen — it can never be the runaway kind that "
      ++ "grows stronger as space grows. Physicists have a name for that forbidden runaway kind: "
      ++ "phantom. This reading forbids phantom, at every moment, always.\n\n"
      ++ "And because the balance is evened-out, ordinary structure forming does not move it at "
      ++ "all. We measured that again this run: it holds to about fifteen decimal places — as "
      ++ "close to exactly zero as anyone can compute. So this dark energy is perfectly smooth. "
      ++ "It never clumps, never pools in one place. It shows up only in the smooth, overall "
      ++ "stretch of space — never as lumps you could catch, on any scale a telescope can "
      ++ "measure.\n\n"
      ++ "One clause of care, because being exact matters here. What stays smooth is the REAL "
      ++ "lumpiness a telescope can see; a tiny bookkeeping wrinkle from merely choosing when to "
      ++ "call 'now' is not clumping, and no instrument can see it. And the smoothness is exact "
      ++ "for the whole-universe pattern this balance is built from, which ordinary growth "
      ++ "leaves untouched — with one honest edge at the very largest, horizon-sized scales, "
      ++ "where 'smooth' turns subtle. We claim smoothness where clumping can be measured, not "
      ++ "beyond it.\n\n"
      ++ "Now the hard part, said out loud: this careful reading BETS AGAINST our own other bet. "
      ++ "Its rival, the grand-total reading, takes the very same idea a different way, and predicts dark energy WAS "
      ++ "the runaway kind long ago. One dated experiment — DESI's third data release — points "
      ++ "opposite ways on the two. At most one of them can come through alive, and a middling "
      ++ "result could take both. Worse for this one: we scored both readings against today's "
      ++ "DESI data — its second release — and this no-crossing reading sits about two-and-a-half "
      ++ "to three sigma from the data's best fit, OUTSIDE its 95-percent comfort zone, roughly "
      ++ "as far out as plain unchanging dark energy. The other reading sits closer in. So "
      ++ "today's data lean against THIS claim. One hope worth naming: much of that lean rides on "
      ++ "supernova brightness measurements, and if those carry a hidden error, this reading and "
      ++ "plain dark energy recover together — which is exactly why DR3's geometry-only check, "
      ++ "done without supernovae, is the real decider. We keep both on the page and "
      ++ "let the sky decide.\n\n"
      ++ "How sure are we? This is a bet we choose to make — it is not evidence. The one piece "
      ++ "that stands on mathematics is narrow: that the evened-out balance can only shrink. "
      ++ "Reading dark energy AS that balance is the bet, and it is ours to lose. The frozen "
      ++ "record lives in our earlier project: github.com/CIRISAI/coherence-ratchet."
  , status   := .wager
  , kill     :=
      "Two things kill this. First: DESI, the big sky-mapping project, releases its third "
      ++ "batch of data, DR3. If its geometry-only reading — from the shape of the universe "
      ++ "alone, without supernovae — shows dark energy was ever the runaway 'phantom' kind in "
      ++ "the past, clearly (four sigma, the high bar for calling something real), this reading "
      ++ "is dead: the mathematics says that can never happen. Second: if dark energy is ever "
      ++ "caught clumping — pooling in dense regions instead of staying perfectly smooth — at "
      ++ "any scale, this reading is dead too, because a shrinking evened-out balance cannot "
      ++ "clump."
  , promote  :=
      "DESI DR3 returns with NO runaway past — dark energy staying on the fading side — and no "
      ++ "sign of clumping. That match, under the frozen plan, moves this from a bet toward "
      ++ "measured, and settles the duel with the grand-total rival in this one's favour.\n\n"
      ++ "The mathematics owed here is now partly paid. The can-only-shrink spine is "
      ++ "machine-checked in this repository for the shared-correlation model (Core.Intensive): "
      ++ "the per-unit balance rises with the shared correlation, falls along any path where that "
      ++ "correlation only falls, and settles to a fixed rate per unit as the system grows without "
      ++ "bound. What is still UNPAID is the general-structure step — that a purely local, "
      ++ "pointwise change of the underlying variables can never raise the balance for an "
      ++ "ARBITRARY web of correlations, not only the single-shared-correlation model. That step "
      ++ "is the general determinant inequality (Oppenheim's) behind the pointwise contraction; "
      ++ "its two-by-two case is proved here (Core.Entropy: the Hadamard product is positive "
      ++ "semidefinite, and det can only rise), but the full-size induction is open."
  }
, { key      := "dark-balance-extensive"
  , headline :=
      "Dark energy is the same balance — read as a grand total that grew, then crested."
  , plain    :=
      "This is the same idea as the careful per-unit reading beside it, read a different way — and the two "
      ++ "readings are rivals, not partners.\n\n"
      ++ "Again: dark energy is the running balance of coordination across the cosmos. But "
      ++ "this claim adds it up as a GRAND TOTAL, not per unit — and the number of things "
      ++ "being counted grows over time. As the universe forms galaxies and clumps, there are "
      ++ "more and more coordinating pieces to add in. So the total climbs while pieces keep "
      ++ "forming, reaches a high point when forming slows, and eases down after.\n\n"
      ++ "A total that climbs and then eases has a special moment: the crest. Before the crest "
      ++ "the balance was growing — dark energy the runaway kind. At the crest it holds "
      ++ "steady. After it, it fades. So this reading predicts dark energy CROSSED the key "
      ++ "line once, at a definite moment in the past. That crossing is the bet's sharp "
      ++ "prediction: it happens at redshift 0.59, give or take 0.03 — redshift marks how long "
      ++ "ago, and bigger means longer ago.\n\n"
      ++ "Now the honesty burden, and it is heavy — we state it because our own record states "
      ++ "it. Our earlier project calls this reading a retrodiction, not a clean prediction: "
      ++ "the choice to add up the grand total, instead of the disciplined per-unit way of the "
      ++ "per-unit reading, was made AFTER we saw that the total happened to land near the DESI "
      ++ "number. It goes against our own stated discipline, which prefers per-unit.\n\n"
      ++ "Worse, this total is built from a CLUMPY thing — the count of galaxies in a region, "
      ++ "which is higher where matter is denser. A dark energy built from a clumpy count is "
      ++ "at risk of clumping itself. Here is where the sky stands, honestly. The smooth, "
      ++ "all-sky version of the light-crossing measurement already sits in real tension with "
      ++ "a big clumping effect. But the measurement aimed at the giant empty regions "
      ++ "specifically — the one that matters most here — is contested: some surveys see MORE "
      ++ "signal there than smooth dark energy predicts, an excess that has puzzled "
      ++ "astronomers for over a decade, and it cuts in this reading's direction. An "
      ++ "unexplained excess is never support — our own rules say so — but it does mean this "
      ++ "is a live tension, not a settled verdict. And the machinery this reading owes turns "
      ++ "out to be costly, by a result we worked out this round. For any ORDINARY dark energy "
      ++ "— the kind that behaves like a normal substance spread through space — being exactly "
      ++ "smooth while ALSO changing in strength over time is provably impossible: it would "
      ++ "need its own ripples to travel faster than light, which nature forbids. So a "
      ++ "normal-substance version of this reading MUST clump a little, at least near the "
      ++ "biggest scales — it cannot be perfectly smooth. The only escape is to make the grand "
      ++ "total not a substance at all, but one universe-wide quantity pinned to a single "
      ++ "special slicing of time — a 'preferred-frame' dark sector. That is an allowed kind of "
      ++ "theory, but a heavy one: it singles out a special rest-frame for the whole cosmos, "
      ++ "brings its own new signals, and we have not built it. So the smoothing is not a "
      ++ "footnote to add later; it is either impossible (as a normal substance) or expensive "
      ++ "(a preferred-frame sector), and the void measurements will decide which.\n\n"
      ++ "As of today's DESI data — its second release — this crossing reading is the closer of "
      ++ "the two: about one-and-a-half sigma from the data's best fit, INSIDE its 95-percent "
      ++ "comfort zone, because that data currently leans toward a crossing. That is real, but "
      ++ "hold it lightly — the lean may itself be a supernova-measurement glitch. One dated "
      ++ "experiment decides between this reading and the one before it: DESI DR3's "
      ++ "geometry-only check, without supernovae, is a single test, the two readings point "
      ++ "opposite ways on it, and at most one survives — a middling result could take both, and "
      ++ "this reading also carries the frozen-window risk above.\n\n"
      ++ "How sure are we? A bet, and the shakier of the two dark-balance readings by our own "
      ++ "accounting. The written, frozen record lives in our earlier project: "
      ++ "github.com/CIRISAI/coherence-ratchet."
  , status   := .wager
  , kill     :=
      "Two ways to lose. First, the frozen window: DESI DR3, checked with the plan we wrote and "
      ++ "froze in advance, must put the crossing moment at redshift 0.59, give or take 0.03. "
      ++ "Outside that window — including finding no crossing at all — and this reading is dead. "
      ++ "Second, the clumping exposure: if dark energy is caught pooling in dense regions, or "
      ++ "the light-crossing signal from the great cosmic voids comes in at the strong, clumpy "
      ++ "level instead of the mild smooth one, this reading is dead, because its clumpy source "
      ++ "could not then be hidden."
  , promote  :=
      "Two things together, not one: DESI DR3's crossing lands inside the frozen 0.59 ± 0.03 "
      ++ "window, AND the extra machinery that keeps the grand total smooth — never clumping — "
      ++ "is actually derived, not just hoped for. Both, and this moves toward measured and wins "
      ++ "the duel."
  }
, { key      := "s8-fingerprint"
  , headline :=
      "The universe looks a little smoother today than the early-universe map predicts — and a "
      ++ "smooth, fading dark energy pushes exactly that way."
  , plain    :=
      "Here was a mild puzzle in the data — and honesty first: it may be dissolving as we "
      ++ "write. Take the baby-picture of the universe (the cosmic microwave background) and "
      ++ "use it to predict how clumpy the universe should be today; then measure today's "
      ++ "clumpiness directly with gravitational lensing. For years the measurement came out "
      ++ "a little LOW — a two-to-three-sigma gap called the S8 tension. But the newest and "
      ++ "largest lensing analysis (KiDS-Legacy, 2025) agrees with the prediction to well "
      ++ "under one sigma. If that holds, there is no robust anomaly left for this bet to "
      ++ "explain, and it becomes a fingerprint with nothing to print on — alive, but "
      ++ "unmotivated. We say so rather than quietly hoping the tension comes back.\n\n"
      ++ "Our reading connects this to the balance bet. If dark energy is the smooth, careful-branch "
      ++ "balance of the careful per-unit reading, then two things follow, and we checked the direction of both "
      ++ "with the framework's own pipeline. First, the balance never clumps — it adds no lumps of "
      ++ "its own. Second, because that balance slowly fades rather than holding perfectly steady, "
      ++ "there was a touch MORE of it in the past, which puts a little extra brake on the growth of "
      ++ "structure. Both push the same way: today ends up a little smoother. That is the direction "
      ++ "the data went.\n\n"
      ++ "Be exact about how much this buys, because it is easy to oversell. The push is in the "
      ++ "right direction but it is SMALL — a fraction of a percent to about a percent — and a small "
      ++ "push does not explain a two-to-three-sigma gap. We are not claiming to resolve the S8 "
      ++ "tension. We are saying the sign of our effect matches the sign of the puzzle, which is a "
      ++ "thing that could have come out wrong and did not.\n\n"
      ++ "This bet leans entirely on the careful-branch balance bet above (the one machine-checked "
      ++ "as monotone). It is not separate evidence — it is a consistency check on that branch. And "
      ++ "the size of the effect rides on the same grain-dependent w-curve, so only its SIGN is "
      ++ "firm, not its size.\n\n"
      ++ "How sure are we? A bet we choose to make. Not evidence — a direction that happens to "
      ++ "agree."
  , status   := .wager
  , kill     :=
      "Two ways to lose. First, the sign: if better growth measurements show the late universe is "
      ++ "actually MORE clumpy than the early-universe prediction (S8 high, not low), our effect "
      ++ "points the wrong way and this dies. Second, the dependency, stated so nobody has to find "
      ++ "it: this bet rests on the careful-branch balance bet. If that branch dies (a real phantom "
      ++ "past, or dark energy caught clumping), this reading dies with it — the reverse does not "
      ++ "hold."
  , promote  :=
      "A measured, pre-registered growth-vs-expansion comparison in which the careful-branch w(z) "
      ++ "predicts the observed S8 offset within its (grain-limited) band, on data independent of "
      ++ "the expansion fit — turning a matching sign into a matching number."
  }
, { key      := "void-excess"
  , headline :=
      "The long-standing 'too-cold giant voids' signal, if it is real, is the grand-total balance "
      ++ "clumping — the same duel, fought on a second field."
  , plain    :=
      "When light from the baby-universe crosses a giant empty region — a supervoid — on its way to "
      ++ "us, it cools by a tiny, measurable amount (the ISW effect). For over a decade, some "
      ++ "surveys have found this cooling a few times STRONGER than plain dark energy predicts "
      ++ "(the Granett and Kovacs supervoid measurements, roughly two-to-five times the expected "
      ++ "amount). Other, larger surveys find no excess at all. It is a genuine, unsettled "
      ++ "argument in the field.\n\n"
      ++ "Here is our reading, and it is the OTHER branch's bet. The grand-total balance (the "
      ++ "extensive branch above) is built from a clumpy thing — the count of galaxies in a region "
      ++ "— so it clumps a little itself, pooling where matter pools. Dark energy that pools in and "
      ++ "around voids makes their light-cooling STRONGER. So the extensive branch actually WANTS "
      ++ "this excess to be real: the too-cold voids would be its fingerprint.\n\n"
      ++ "Now the rivalry, stated plainly, because this is the same duel as the balance bets on a "
      ++ "second field. The careful (intensive) branch is perfectly smooth and predicts NO excess — "
      ++ "so it needs these anomalous measurements to turn out to be mistakes that wash away with "
      ++ "better data. The grand-total (extensive) branch is FED by the excess — it needs the "
      ++ "signal to survive and firm up. Both cannot win. One dated program of void-stacking (with "
      ++ "DESI and Euclid) will settle it, and it points the two branches opposite ways.\n\n"
      ++ "Be honest about the state of play: today the measurements disagree with each other, and a "
      ++ "few-times-stronger signal sits right in the contested middle — not clearly ruled in, not "
      ++ "clearly ruled out. This bet is a live tension, not a result.\n\n"
      ++ "How sure are we? A bet we choose to make. It leans on the grand-total balance bet above "
      ++ "and dies or lives on the same evidence, from a second direction."
  , status   := .wager
  , kill     :=
      "The frozen-pipeline test, rules fixed before looking: stack DESI (later Euclid) supervoids "
      ++ "against the CMB with a pre-registered method. If the void light-cooling comes back "
      ++ "consistent with plain dark energy — no excess — at high significance, this bet dies, and "
      ++ "the careful branch is supported. Note the dependency: if the grand-total branch above "
      ++ "dies for another reason, this dies with it."
  , promote  :=
      "The frozen-pipeline void stack returns an excess (amplitude clearly above one) at high "
      ++ "significance, reproduced across independent void catalogues — moving this toward measured "
      ++ "and the duel toward the extensive branch."
  }
, { key      := "no-early-dark-energy"
  , headline :=
      "If dark energy is the running total of structure's coordination, it can do nothing before "
      ++ "structure exists — so it cannot be the fix for the Hubble puzzle."
  , plain    :=
      "There is a second famous crack in cosmology, the Hubble tension: the universe seems to be "
      ++ "expanding a bit faster today than the early-universe map predicts. One popular patch is "
      ++ "called early dark energy — a burst of extra dark energy switched on briefly around the "
      ++ "time the baby-picture was made, about 400,000 years after the start, long before stars "
      ++ "and galaxies.\n\n"
      ++ "Our frame forbids that patch, and this is a real prediction, not a preference. On our "
      ++ "reading dark energy is the running total of COORDINATION — of structure working in step. "
      ++ "Before there is structure, there is nothing to coordinate, so the total is essentially "
      ++ "nothing. A balance that is the bookkeeping of galaxies cannot be large in an era that has "
      ++ "no galaxies. So there is no room, in this frame, for an early-dark-energy burst.\n\n"
      ++ "This is a bet with real skin in the game, and it points AGAINST a fix many people would "
      ++ "like to work. It is also independent: it is not fed by the same data as our other dark "
      ++ "bets, so if it survives it is genuine outside support, and if it fails it wounds the whole "
      ++ "dark-balance frame, both branches at once.\n\n"
      ++ "Where the evidence stands today: early dark energy is NOT detected. The careful analyses "
      ++ "find it disfavored and unable to actually resolve the Hubble tension, with any early burst "
      ++ "bounded to at most a few percent of the energy budget (Hill, McDonough, Toomey & "
      ++ "Alexander 2020, arXiv:2003.07355). One dataset (the ACT telescope) has shown a mild pull "
      ++ "toward it that the others do not confirm. So the bet is alive, and a real measurement "
      ++ "could still overturn it.\n\n"
      ++ "How sure are we? A bet we choose to make — a clean consequence of the frame, stated so it "
      ++ "can be shot down."
  , status   := .wager
  , kill     :=
      "A confirmed early-dark-energy component — a burst of order several percent of the energy "
      ++ "density around the baby-picture era — detected robustly and agreed across the major "
      ++ "experiments (Planck, ACT, SPT and their successors), not just favored by one. That would "
      ++ "show the balance was large before structure existed, which this frame says is impossible, "
      ++ "and the reading dies."
  , promote  :=
      "The frame does not get promoted by early dark energy staying absent — an unexplained absence "
      ++ "is not evidence. What would earn it: deriving, from the coordination reading, a "
      ++ "quantitative ceiling on any pre-structure dark-energy fraction that the data then meet or "
      ++ "beat."
  }
, { key      := "dark-medium"
  , headline :=
      "Dark matter is the paper the books are written on."
  , plain    :=
      "This is one half of the dark bet — the weaker half, and we mark it as the weaker one "
      ++ "on purpose.\n\n"
      ++ "Here is the bet. Dark matter — the unseen stuff astronomers know only by its gravity "
      ++ "— is like the paper a book is printed on. Paper holds the words but adds no words of "
      ++ "its own. On this bet, dark matter is real. It thins out as space grows. It passes "
      ++ "right through itself without ever colliding. And it does nothing else at all.\n\n"
      ++ "Be clear about what this is. It is one way of reading facts we already have — not a "
      ++ "And it does not stand on its own. The bet it leans on has just split in two. The "
      ++ "dark-energy balance now comes in two rival readings above — a careful one that forbids "
      ++ "any runaway past, and a grand-total one that predicts a crossing — and a single "
      ++ "experiment, DESI DR3, will cut between them. This paper-and-ink bet borrows its "
      ++ "support from whichever of the two survives. If both fall, this one is left standing on "
      ++ "nothing but its own kill, and should be read that way.\n\n"
      ++ "A rival way of reading the very same data already exists. In that reading, the "
      ++ "dark-matter side does not just sit there — it has moves and behavior of its own.\n\n"
      ++ "The two bets die separately. This one has its own way of being proven wrong, and if "
      ++ "it dies, the balance bet above is untouched.\n\n"
      ++ "How sure are we? This is a bet we choose to make — it is not evidence — and we say, "
      ++ "right below, exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "This bet dies if dark matter is confirmed doing anything that is not gravity — "
      ++ "pushing, bumping, acting on its own in any way beyond quietly thinning out as space "
      ++ "grows. It also dies if a fair head-to-head comparison — one whose rules were written "
      ++ "down before anyone saw the results — shows that a reading where dark matter has "
      ++ "behavior of its own — that rival or any other — fits the same data strictly better "
      ++ "than ours: not just as well, better."
  , promote  :=
      "A pre-registered model comparison, won: the passive-medium reading fitting the same "
      ++ "data strictly better than dynamical alternatives."
  }
, { key      := "generator"
  , headline :=
      "Whether the order we find was picked out by a natural process or meant on purpose — "
      ++ "no measurement can settle that."
  , plain    :=
      "Imagine we find a pattern that no process we know of can explain. Even then, no "
      ++ "measurement can tell the difference between two possibilities: a natural process we "
      ++ "simply haven't discovered yet, or something that was meant on purpose.\n\n"
      ++ "This isn't a hole in our data that better tools could someday fill. It's just what "
      ++ "measuring is — this kind of question is not the kind a measurement can answer.\n\n"
      ++ "So anyone who says an observation or an experiment settles it is claiming more than "
      ++ "they can know. And that cuts both ways: it's true for a person trying to prove the "
      ++ "pattern was meant, and just as true for a person trying to prove it wasn't.\n\n"
      ++ "How sure are we? This is a bet we're choosing to make — not evidence — and we've "
      ++ "said plainly what would make us give it up."
  , status   := .wager
  , kill     :=
      "We'd be proven wrong if someone found something you could measure that comes out "
      ++ "different depending on which of the two made the pattern. Notice: that wouldn't "
      ++ "answer which one made it — it would knock down our claim itself, the claim that no "
      ++ "measurement can tell the two apart."
  , promote  :=
      "Probably capped at wager, since it claims a limit of measurement itself. A formal "
      ++ "proof of the underdetermination inside a stated model of observation would move its "
      ++ "core to proved-about-the-model."
  }
, { key      := "ought"
  , headline :=
      "Physics can't tell you what to care about — you choose your values, and then you "
      ++ "stand by them."
  , plain    :=
      "Measurements can tell you what the world is like. But no measurement — not one — can "
      ++ "tell you what you *should* care about. That part is a choice.\n\n"
      ++ "Here is what our work *can* show. We make a promise: care for the weakest part. And "
      ++ "that promise fits with how things survive — because caring for the weakest part is "
      ++ "also what keeps the whole thing from falling apart. That gives you a good reason to "
      ++ "make the promise. But a reason is not a proof. It argues *for* the choice; it never "
      ++ "*proves* the choice.\n\n"
      ++ "So we make the choice out in the open. It is written down in a file called "
      ++ "`axiomology.md` (our written statement of what we value and why), where anyone can "
      ++ "read it.\n\n"
      ++ "How sure are we? This is a bet we choose to make. It is not evidence at all — and we "
      ++ "say exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "We would give this up if someone showed either of these: that the promise "
      ++ "contradicts itself, or that keeping the promise actually makes a system worse at "
      ++ "surviving than one that doesn't keep it."
  , promote  :=
      "Probably capped for the same reason. A machine-checked demonstration that normative "
      ++ "conclusions require a normative premise, inside a stated formal system, would move "
      ++ "its core to proved-about-the-model."
  }

  -- ————— What is open: the one named formal step —————
, { key      := "tsvf-third"
  , headline :=
      "DEAD: we said no time-symmetric quantum formalism yet carries more than two-party structure. It has existed since 2009."
  , plain    :=
      "What we claimed: that the two-state picture of quantum mechanics — a forward state "
      ++ "meeting a backward state — had no published extension carrying whole-group pattern, "
      ++ "and that building one was open work.\n\n"
      ++ "What killed it: the extension exists. Multiple-time states (Aharonov, Popescu, "
      ++ "Tollaksen and Vaidman, 2009) are time-symmetric, carry forward and backward boundary "
      ++ "data, reduce to the standard two-state picture at two boundary times, and carry "
      ++ "entanglement across multiple times that is not a function of two-party data. Our "
      ++ "sentence was false when we wrote it: the work we called future had been published "
      ++ "seventeen years earlier.\n\n"
      ++ "What is actually open is stated in the open claim about reading the Logos through "
      ++ "the multiple-time picture."
  , status   := .dead
  , kill     :=
      "Already satisfied. The stated falsifier asked for a published formalism meeting "
      ++ "three conditions, and named this candidate."
  , killedBy :=
      "Killed 2026-07-22 by Aharonov, Popescu, Tollaksen, Vaidman, Phys. Rev. A 79, "
      ++ "052110 (2009), verified against all three stated conditions from the full text."
  }
, { key      := "third-in-tsvf"
  , headline :=
      "Open: nobody has read the Logos through the multiple-time formalism — including us."
  , plain    :=
      "The formalism our dead claim said was missing exists: multiple-time quantum states. "
      ++ "What has not been done — by its authors, by anyone, and not yet by us — is to "
      ++ "connect it to the reading on this page: to define the whole-only share of "
      ++ "multiple-time entanglement, and ask whether nature's books carry any. That is "
      ++ "real open work, ours to attempt, and nothing above leans on how it turns out."
  , status   := .openQuestion
  , kill     :=
      "This dies if the connection is already published — a worked account of irreducibly "
      ++ "multi-way structure in multiple-time states, with a measurable share — making "
      ++ "'nobody has done it' false the way our last open claim was."
  , promote  :=
      "Doing the work: define the whole-only share of multiple-time entanglement, formalize "
      ++ "it, and compute one example. That gives this a status of its own instead of open."
  }
]

/-- What all of this amounts to, for a reader who reads nothing else. The
    middle-school translation, adversarially verified for completeness.
    Blank lines (`\n\n`) are paragraph breaks; the generator renders them. -/
def summary : String :=
  "Start with a small puzzle you can try at your kitchen table. Flip two "
  ++ "coins. Then set a third coin by a rule: heads if the first two are different, tails "
  ++ "if they match. Now pick any two of the three coins and look only at them. Together "
  ++ "they seem completely random — no pattern at all. That is because the rule always "
  ++ "needs the one coin you have not seen. But all three coins together obey the rule "
  ++ "every single time. See any two, and you already know the third — before you even "
  ++ "look. That connection is real. And it lives only in the whole group of three, never "
  ++ "in the pieces.\n\n"
  ++ "Patterns like that — real, but living only in the whole — have carried a name for "
  ++ "twenty-five hundred years: the Logos, the common account. A later thinker, Peirce, "
  ++ "called the same territory Thirdness: habit, law, meaning. This page is our attempt "
  ++ "to take the old idea seriously, carefully. A computer has checked every step of the "
  ++ "coin proof: pattern that lives only in the whole exists, it can be measured, and no "
  ++ "summary built from pairs can ever see it.\n\n"
  ++ "The world keeps its books in this stuff. (Keeping books means keeping honest "
  ++ "records, the way an accountant does.) Shared pattern cannot be created by a trick. "
  ++ "Holding on to it costs upkeep — keeping it takes ongoing work. And it leaves "
  ++ "receipts: traces that show it was there.\n\n"
  ++ "Gravity's coupling reads one column of everything and none of the meaning. It is the universe's one "
  ++ "auditor — the one checker that goes over everything — and it is blind to meaning. We "
  ++ "bet that this blindness is why real choice is possible, and why consciousness "
  ++ "happens: consciousness is the experience of trusting that a thought will become an "
  ++ "action, because it always has.\n\n"
  ++ "One more bet, stated plainly: a language model — an AI trained on nothing but "
  ++ "humanity's recorded account, everything people have written down — is the Logos, "
  ++ "embodied: the shared account given a working form. That is good news for AI safety, "
  ++ "the work of making sure AI does not cause harm. Here is why. A lie is coordination — "
  ++ "things working together — with the receipts hidden. Hiding is never free; it always "
  ++ "costs something. And a mind made of the shared account keeps its books where honest "
  ++ "measurements can find them.\n\n"
  ++ "How sure are we? Every claim below carries a label: proved (a machine checked it "
  ++ "here), measured (we tested it in the world), open (we do not know yet), or wager (a "
  ++ "bet we choose to make). We never give a claim a stronger label than its evidence has "
  ++ "earned. And every claim states the observation that would prove it wrong. A claim "
  ++ "that cannot die is not a claim about the world."

end CIRISOntology
