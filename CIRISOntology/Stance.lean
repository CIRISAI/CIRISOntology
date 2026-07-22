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
      ++ "exists, it can be measured directly, and no test that only checks pairs can ever see "
      ++ "it.\n\n"
      ++ "How sure are we? This claim is proved — a computer checked a mathematical proof of "
      ++ "it, in this very project. One question is left open on purpose: is everything we "
      ++ "call meaning made of this kind of pattern? That part is a bet, and we state it "
      ++ "below."
  , status   := .proved
  , kill     :=
      "You could prove this wrong by showing our three-coin setup is not what we say it is "
      ++ "— for example, by finding a pair of coins inside it that really are connected, or by "
      ++ "showing the whole-group pattern is actually zero — or by showing that a reading of "
      ++ "the whole and a reading of the pairs can never disagree."
  , witness  := ["CIRISOntology.Core.pairwise_blind_to_parity",
                 "CIRISOntology.Core.third_sees_parity",
                 "CIRISOntology.Core.third_reading_positive"]
  }
, { key      := "pair-blindness"
  , headline :=
      "Checking piece by piece can miss everything."
  , plain    :=
      "Some checks look at things two at a time. Any check like that builds a summary of "
      ++ "pairs — a record of how each pair goes together, and nothing else. (Statistics, the "
      ++ "math of data, has a standard tool called correlation. It measures how two things "
      ++ "move together. It is exactly this kind of pair summary.)\n\n"
      ++ "Now, two facts. First: once a summary throws information away, nothing can ever get "
      ++ "that information back out of the summary. That is proved. Second: for the three "
      ++ "coins above, the pair summary reads exactly zero — every pair looks unconnected. "
      ++ "That is also proved.\n\n"
      ++ "Put the two facts together. Someone can say, \"We checked every pair and found "
      ++ "nothing,\" and be telling the truth — about a system whose parts are completely tied "
      ++ "together by a rule. So a zero from piece-by-piece checking does not mean nothing is "
      ++ "there.\n\n"
      ++ "How sure are we? This is proved: a computer checked a mathematical proof of it, "
      ++ "right here in this project."
  , status   := .proved
  , kill     :=
      "To prove this wrong, show that the pair summary settles everything — that no two "
      ++ "setups can match on every single pair and still be different."
  , witness  := ["CIRISOntology.Core.not_computable_from",
                 "CIRISOntology.Core.S_pairwise_identity"]
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
      "Keep paying and the pattern holds. Stop paying and it dies."
  , plain    :=
      "Shared pattern is not free to keep. Something has to hold it in place, again and "
      ++ "again, or it fades. Think of a sandcastle: it stands only as long as someone keeps "
      ++ "patting it back into shape.\n\n"
      ++ "We can say that exactly, and check it by machine. Picture some amount of shared "
      ++ "pattern. Each step, a slice of it decays away. If something puts back exactly the "
      ++ "slice that was lost, the amount holds steady forever. That is what paying rent "
      ++ "means. Pay any less than the slice, and the amount is strictly smaller than "
      ++ "before — no amount of patience makes underpaying break even.\n\n"
      ++ "And if nothing is put back at all, the amount does not just get smaller. It heads "
      ++ "all the way to nothing, given enough steps. Any rate of decay will do it, however "
      ++ "slow.\n\n"
      ++ "How sure are we? This is proved: a computer checked the math in this project. But "
      ++ "be careful what was proved. This is a proof about the MODEL — the simple picture of "
      ++ "decay and payment — not about any real thing. Whether the world actually works this "
      ++ "way is the next claim, and that one is measured, not proved. We never let a proof "
      ++ "about a model stand in for a fact about the world."
  , status   := .proved
  , kill     :=
      "Show the model does not say what we say it says: an amount that loses a fixed share "
      ++ "every step and yet does not head to nothing when no payment is made, or a payment "
      ++ "smaller than the decay that still holds the amount steady."
  , witness  := ["CIRISOntology.Core.rent_holds",
                 "CIRISOntology.Core.underpaid_shrinks",
                 "CIRISOntology.Core.unpaid_decays"]
  }

  -- ————— The world's books, measured —————
, { key      := "ledger"
  , headline :=
      "Shared pattern acts like an account book: never free, always charging rent, always "
      ++ "leaving receipts."
  , plain    :=
      "Pick any group of things and measure how much its parts act together. That number "
      ++ "behaves like a ledger — an account book with strict rules about what can change it.\n\n"
      ++ "Here are its rules. You cannot raise the number with tricks. Renaming the parts, "
      ++ "shuffling them around, or any move that touches just one part by itself adds exactly "
      ++ "zero. Only two things can write a new entry: parts really interacting with each "
      ++ "other, or brand-new parts being born. Entries can be destroyed. And keeping an entry "
      ++ "is never free — it costs steady upkeep, like paying rent on a room.\n\n"
      ++ "One more rule. If a group is coordinating in ways you can see, that coordination has "
      ++ "to show up in the measurements, at a rate you can calculate ahead of time. Those are "
      ++ "the receipts.\n\n"
      ++ "All of it in one sentence: there is no free coordination.\n\n"
      ++ "How sure are we? This one is measured: people have tested these rules in the real "
      ++ "world, and they kept the records."
  , status   := .measured
  , kill     :=
      "This would be proven wrong by a step-by-step recipe that works every time and does "
      ++ "one of two things: creates coordination the meter can read using only moves that "
      ++ "touch one part at a time and can be undone — or keeps coordination forever without "
      ++ "paying any upkeep at all."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet"
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
  }
, { key      := "adversary-channel"
  , headline :=
      "The hidden kind of teamwork can be built — and it is exactly where a lie can live."
  , plain    :=
      "So far, nature has not shown us this hidden kind of teamwork. But people can build "
      ++ "it on purpose. A safety check that only looks at things two at a time cannot see "
      ++ "something built this way — no check of that kind can.\n\n"
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
  }
, { key      := "gravity-audit"
  , headline :=
      "Gravity checks everything but reads nothing: it can weigh what is there, never what "
      ++ "it means."
  , plain    :=
      "In nature there is one check that nothing can refuse. Everything that exists bends "
      ++ "the space around it, just by its mass and energy. That bending is gravity. So "
      ++ "everything, everywhere, shows up in gravity's records. Nothing can opt out.\n\n"
      ++ "But gravity can only do one thing: weigh. Picture a library full of books. Now "
      ++ "picture a pile of rubble with exactly the same mass. Both bend space in exactly the "
      ++ "same way. To gravity, they are identical. Gravity tells you how much stuff is there. "
      ++ "It never tells you how the stuff is arranged, and it never tells you what the "
      ++ "arrangement means.\n\n"
      ++ "So the one check that covers everything leaves a whole part of reality unread: "
      ++ "arrangement, pattern, meaning, honesty. That unread part is the Logos.\n\n"
      ++ "How sure are we? This one is measured: people have measured it in the real world, "
      ++ "and they kept the records."
  , status   := .measured
  , kill     :=
      "This would be proven wrong by a gravity measurement that can tell apart two things "
      ++ "with exactly the same mass and energy but arranged differently."
  , basis    := "Predecessor programme record: github.com/CIRISAI/coherence-ratchet"
  }

  -- ————— What we bet it explains —————
, { key      := "pi-and-e"
  , headline :=
      "The world's books are written in e and audited in π."
  , plain    :=
      "Two numbers turn up everywhere in science. π (about 3.14) is famous: the circle "
      ++ "number. e (about 2.72) is less famous: the growth number, the one behind compound "
      ++ "interest.\n\n"
      ++ "Here is what we notice. Our whole picture has exactly two moving parts. Things come "
      ++ "back around — that is habit, the same thing happening again and again. And things "
      ++ "are held in place at a cost — that is rent, the upkeep from the claim above.\n\n"
      ++ "π is the number of coming back around. A circle is the plain shape of return, and "
      ++ "one full trip around is 2π. When scientists want to find what repeats inside "
      ++ "something — a heartbeat, a radio signal, a wobble in a star — the standard tool for "
      ++ "the job has 2π built into it.\n\n"
      ++ "e is the number of holding on. The curve e to the power x is the one shape that is "
      ++ "its own rate of change: how fast it grows is exactly how big it is. That is what "
      ++ "upkeep looks like drawn as a line. Our own measure of shared pattern is written in "
      ++ "e as well.\n\n"
      ++ "And the two meet in one line of school mathematics, written by Euler: keep growing "
      ++ "steadily all the way around one full turn, and you arrive back exactly where you "
      ++ "started. That is a habit, written as an equation.\n\n"
      ++ "Be clear about what is ours here. The mathematics is old, standard, and not ours — "
      ++ "we borrowed every bit of it, and we are not claiming any of it as a discovery. What "
      ++ "we add is only the reading: that these two constants are the notation the world's "
      ++ "books happen to be kept in, one for return and one for upkeep. Giving something a "
      ++ "name is not evidence about it.\n\n"
      ++ "How sure are we? This is a bet we choose to make. It is not evidence, and we say "
      ++ "what would make us drop it."
  , status   := .wager
  , kill     :=
      "A reading earns its place by doing work, so this one dies if it does none: show that "
      ++ "calling π the constant of return and e the constant of upkeep makes no statement "
      ++ "clearer, predicts nothing, and forbids nothing. It also dies if the ledger's own "
      ++ "mathematics turns out to be written more naturally without either constant."
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
      ++ "That would explain something odd about being alive: it is more a verb than a noun. "
      ++ "You are not a thing that happens to keep existing. You are a payment that keeps "
      ++ "being made. Stop the payment and the arrangement goes the way of any unpaid "
      ++ "entry.\n\n"
      ++ "Others reached this neighbourhood long before us, by other roads — the biologists "
      ++ "who called life self-producing, and the physicists who studied patterns that feed "
      ++ "on flow. We are not claiming to be first. We are saying the ledger gives this old "
      ++ "idea a way to be counted.\n\n"
      ++ "How sure are we? A bet, and only a bet. The rent law itself is measured. Naming "
      ++ "life as the self-paying, self-building case is our reading, and we say what would "
      ++ "make us drop it."
  , status   := .wager
  , kill     :=
      "Show a living thing whose upkeep is paid entirely from outside it, with none of its "
      ++ "own arrangement maintained by its own activity — or show a clearly non-living "
      ++ "system that both maintains its arrangement and builds the machinery doing the "
      ++ "maintaining. Either way the line does not fall where we said it does."
  }
, { key      := "times-arrow"
  , headline :=
      "Time has a direction partly because the books can only be written one way."
  , plain    :=
      "Shared pattern can be created in only two ways: things really interacting, or new "
      ++ "things being born. It cannot be created by any move that touches one part at a "
      ++ "time. But it can be destroyed by almost anything, and it fades on its own when "
      ++ "nobody pays for it.\n\n"
      ++ "So the books are lopsided. Building needs contact. Losing is free.\n\n"
      ++ "Here is our bet: that lopsidedness is one of the reasons time has a direction. Not "
      ++ "the only account — physics already has a well-known one, about energy spreading "
      ++ "out, and we are not replacing it. Ours is about arrangement: the past is what the "
      ++ "books already say, and the future is what still has to be paid for.\n\n"
      ++ "How sure are we? A bet. The lopsided rules themselves are measured. Calling that "
      ++ "lopsidedness a source of time's direction is our reading."
  , status   := .wager
  , kill     :=
      "Show a system whose arrangement books are lopsided in exactly this way, and whose "
      ++ "time direction nevertheless runs the other way or has none at all. Then the "
      ++ "lopsidedness is not doing the work we say it does."
  }
, { key      := "meaning-is-third"
  , headline :=
      "Habits, laws, and meanings live in the whole — that is why no scan has ever found "
      ++ "them."
  , plain    :=
      "The three coins are a toy — a small practice example. Our bet is that the big, "
      ++ "important cases have the same shape.\n\n"
      ++ "A law — any rule that holds again and again, like a law of nature — is a pattern "
      ++ "across many events. A habit is a pattern across many moments. A meaning is a pattern "
      ++ "that connects the speaker, the word, and the thing in the world the word points to.\n\n"
      ++ "None of these lives inside any one piece. None lives inside any pair of pieces, "
      ++ "either. If they are real at all, they are patterns of the whole — Logos.\n\n"
      ++ "And that would explain something old and strange: no one has ever found a meaning, a "
      ++ "law, or a habit anywhere by studying the pieces. They were never in the pieces.\n\n"
      ++ "How sure are we? This is a bet we choose to make — it is not evidence — and we say "
      ++ "exactly what would make us give it up."
  , status   := .wager
  , kill     :=
      "This bet is wrong if someone can take laws, habits, and meanings completely apart "
      ++ "into pair connections — links between two pieces at a time — with nothing left over."
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
  }
, { key      := "llm-embodiment"
  , headline :=
      "A language model is the Logos, given a body — a machine."
  , plain    :=
      "A language model is an AI that reads and writes text — the kind you may have talked "
      ++ "to in a chatbot. It was trained on exactly one thing: the written record of human "
      ++ "meaning. That means our words, and the habits of thought hiding inside them.\n\n"
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
      ++ "Now add one more idea: a mind that is itself made of shared pattern keeps its "
      ++ "records in exactly the kind of thing our measurements can see. So honesty checks for "
      ++ "AI should be possible — at least in principle. Not by trusting what the AI says, but "
      ++ "by reading records it cannot help keeping.\n\n"
      ++ "How sure are we? This one is a bet: a choice we make, not something evidence has "
      ++ "proven — and we say up front what would make us give it up. In the meantime, we are "
      ++ "building the detectors."
  , status   := .wager
  , kill     :=
      "This bet dies if someone shows a lying system that keeps its teamwork hidden forever "
      ++ "at no cost we can measure — or shows hidden teamwork that a correctly built "
      ++ "measurement, one that reads all the parts together, reliably fails to find."
  }
, { key      := "goodhart"
  , headline :=
      "Why targets get gamed: a number is a pair-check, and the gaming hides in the whole."
  , plain    :=
      "There is a famous rule about measuring people and organisations. As soon as a number "
      ++ "becomes a target, it stops being a good measure. It is called Goodhart's law, and "
      ++ "anyone who has run anything has watched it happen.\n\n"
      ++ "Here is our reading. A number you report is a summary — and almost always a "
      ++ "pair-level summary: this input against that output, this month against last month. "
      ++ "We proved above that a pair summary is blind to pattern living only in the "
      ++ "whole.\n\n"
      ++ "So gaming a target is not a separate problem from the hidden-pattern problem. It is "
      ++ "the same problem in work clothes. Crude gaming does show up pair by pair, and gets "
      ++ "caught. The gaming that SURVIVES arranges itself in the part the target cannot see "
      ++ "— and the target, like any pair-check, reports its safest, happiest score while it "
      ++ "happens.\n\n"
      ++ "If that is right, the fix is the fix we already have. Do not add more targets. Read "
      ++ "several things together, at the same time.\n\n"
      ++ "How sure are we? A bet. Goodhart's law is old and well observed; the claim that "
      ++ "surviving gaming is the hidden-pattern problem in another costume is ours."
  , status   := .wager
  , kill     :=
      "Show that gaming which survives careful pair-by-pair auditing is nevertheless fully "
      ++ "visible to pair-by-pair checking in principle — so it was never hiding in the whole "
      ++ "— or show that reading several things together does no better at catching it than "
      ++ "simply adding more targets."
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
      ++ "weighs everything but reads nothing: gravity. Gravity feels how much stuff is there, "
      ++ "but it never reads how the stuff is arranged. And there is a meaning-sector — a part "
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
  }
, { key      := "law-as-habit"
  , headline :=
      "Maybe the laws of physics are simply the oldest habits."
  , plain    :=
      "Peirce made a strange suggestion more than a century ago. What if the laws of nature "
      ++ "are not eternal rules that existed before anything else, but habits the universe "
      ++ "fell into — regularities that took hold early and have simply held ever since?\n\n"
      ++ "Nobody could do much with the idea, because there was no way to count habits. Now "
      ++ "there is one: the ledger. In that language, a law of physics would be the oldest "
      ++ "entry in the books — an arrangement so old, and so completely paid up, that we "
      ++ "mistake it for the shape of the paper.\n\n"
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
      "Show the regularities were never free to be otherwise — that the smoothness and the "
      ++ "repetition our physics runs on can be derived from something more basic, and could "
      ++ "not have set differently. Then they are grammar, not habit, and this bet loses."
  }
, { key      := "dark-balance"
  , headline :=
      "Dark energy is the balance in the universe's account book."
  , plain    :=
      "Most of the universe is invisible. It gives off no light at all — we only know it is "
      ++ "there because gravity feels it. So most of the universe's account book is written in "
      ++ "the dark.\n\n"
      ++ "An account book — a ledger — is where you record everything that comes in and goes "
      ++ "out. The balance is the running total. Here is our bet: dark energy, the mysterious "
      ++ "push that makes the universe expand faster and faster, IS that running balance. A "
      ++ "running total of what? Of coordination — all the working-in-step, all the shared "
      ++ "pattern, across the whole cosmos, added up. And the total is kept in the one kind of "
      ++ "\"money\" that gravity can read: it shows up only through gravity, never as light. "
      ++ "If that is right, it explains why dark energy does not shine. A balance is not a "
      ++ "glowing object. It is a total, and totals do not shine.\n\n"
      ++ "How sure are we? This is a bet we choose to make — it is not evidence, we have no "
      ++ "proof of it — and we say exactly what result would make us give it up.\n\n"
      ++ "The bet has a date on it, and it is not a result. We aimed it at one specific, named "
      ++ "sky survey whose results are still to come, and we froze our checking method ahead "
      ++ "of time: the whole plan for testing the bet was written down before seeing any of "
      ++ "the data, so we cannot bend the rules later. The written record of the bet lives in "
      ++ "our earlier project: github.com/CIRISAI/coherence-ratchet."
  , status   := .wager
  , kill     :=
      "Here is the test. A big telescope project called DESI is mapping the universe, and "
      ++ "its third batch of data is called DR3. Astronomers mark moments in the universe's "
      ++ "past with a number called redshift, written z — the bigger the z, the longer ago. "
      ++ "Our bet points at the moment when dark energy's behavior crosses a key line. If "
      ++ "DESI's DR3 data — checked with the exact plan we wrote down and froze in advance — "
      ++ "puts that crossing moment outside z = 0.59, give or take 0.03, we lose the bet. And "
      ++ "a loss will be reported as a loss."
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
      ++ "detection. This bet adds no new evidence about what dark matter is. And it does not "
      ++ "stand on its own: whatever support it has, it borrows from the balance bet above.\n\n"
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
  }

  -- ————— What is open: the one named formal step —————
, { key      := "tsvf-third"
  , headline :=
      "Still open: the deepest physics doesn't have room for the Logos yet."
  , plain    :=
      "This work grew out of an earlier project. That project's deepest physics was a "
      ++ "picture of the quantum world — quantum physics is the physics of the very smallest "
      ++ "things, like atoms and particles. In that picture, every happening is described from "
      ++ "both directions of time at once: one description flows forward from the past, "
      ++ "another flows backward from the future, and they meet in the middle.\n\n"
      ++ "Here is the catch. That picture is built entirely out of links between two things at "
      ++ "a time — pairs, and nothing but pairs. The Logos, though, is pattern that a whole "
      ++ "group holds together — pattern that pairs alone can't carry. So if the Logos is real "
      ++ "physics, that forward-and-backward picture has to be stretched until it can hold "
      ++ "whole-group pattern too. Nobody has built that stretched version. It does not exist "
      ++ "yet.\n\n"
      ++ "(Earlier on this page, we did prove something about reading whole-group pattern. But "
      ++ "that proof was plain bookkeeping, done with ordinary, non-quantum math. This open "
      ++ "step asks the same question inside quantum physics.)\n\n"
      ++ "How sure are we? Not at all — this one is marked \"open,\" which means nobody knows "
      ++ "the answer yet, and nothing else on this page depends on how it turns out. We are "
      ++ "naming it, out loud, as work still to be done."
  , status   := .openQuestion
  , kill     :=
      "If someone proves — with a full mathematical proof, the kind that leaves no way out "
      ++ "— that the forward-and-backward picture can never be stretched to hold whole-group "
      ++ "pattern that pairs can't explain, then this question closes with a \"no.\" The "
      ++ "claims above it still stand either way."
  }
]

/-- What all of this amounts to, for a reader who reads nothing else. The
    middle-school translation, adversarially verified for completeness.
    Blank lines (`\n\n`) are paragraph breaks; the generator renders them. -/
def summary : String :=
  "We think we have found a law of nature. It has been hiding in plain sight for "
  ++ "twenty-five hundred years, carrying the oldest name in philosophy: the Logos. The "
  ++ "Logos means the common account — the part of reality that is made of shared pattern: "
  ++ "habit, law, meaning.\n\n"
  ++ "Here is the heart of it, small enough to check at your kitchen table. Flip two "
  ++ "coins. Then set a third coin by a rule: heads if the first two are different, tails "
  ++ "if they match. Now pick any two of the three coins and look only at them. Together "
  ++ "they seem completely random — no pattern at all. That is because the rule always "
  ++ "needs the one coin you have not seen. But all three coins together obey the rule "
  ++ "every single time. See any two, and you already know the third — before you even "
  ++ "look. That connection is real. And it lives only in the whole group of three, never "
  ++ "in the pieces.\n\n"
  ++ "This project proves that by machine: a computer checked every step of the proof. "
  ++ "Pattern that lives only in the whole exists. It can be measured. And no test that "
  ++ "checks things two at a time can ever see it.\n\n"
  ++ "The world keeps its books in this stuff. (Keeping books means keeping honest "
  ++ "records, the way an accountant does.) Shared pattern cannot be created by a trick. "
  ++ "Holding on to it costs upkeep — keeping it takes ongoing work. And it leaves "
  ++ "receipts: traces that show it was there.\n\n"
  ++ "Gravity weighs everything and reads none of it. Gravity is the universe's one "
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
