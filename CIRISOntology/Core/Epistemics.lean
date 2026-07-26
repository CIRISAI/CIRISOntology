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

GATECRAFT. A gate is an instrument, and every rule this repository applies to an
instrument applies to its gates too: a gate has a domain of validity, a power to
detect what it claims to detect, and its own kill. `GateSpec` therefore forces
each gate to carry, at construction, the failure family it catches, the incident
that discovered it, the stored case it MUST catch (`knownBad` — the gate's own
kill: a gate that passes its known-bad is dead), the case it must pass
(`knownGood`), its power certificate, and its scope. Where no stored case exists
the field says so in the honest literal "NONE-YET (recorded gap)" — a visible
hole, never a fabricated anchor. A gate missing its anchors is not a gate; it is
a hypothesis about a gate.

The registry — coverage matrix, lifecycle, the axiological layer, and the
per-incident commit provenance in full — is `GATES.md` at the repository root.
This file carries what the page renders and what the audit reads.

VOCABULARY. The field names here are deliberately neutral and code-stable. The
registry states the same six in older water words, and a reader crossing between
the two should carry this table: `family` is the REACH a gate guards,
`provenance` its HEADWATERS, `knownGood` the PLUMB LINE, `knownBad` the KEPT
TAINT, `power` the DYE TEST (put dye in upstream, verify it appears downstream),
and `domain` the gate's DEPTH — past which it is out of its depth. A reading put
through the gates either RUNS CLEAR, is FOULED, or — taken where no gate holding
a current dye test was standing — is UNGAUGED, which is neither a zero nor a
detection.

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

/-- Everything one gate must carry. No field has a default: a gate is
    constructed with its anchors, its power certificate and its scope, or it is
    not constructed — the same discipline by which `Claim` forces `kill`.

    Adding a constructor to `Gate` therefore breaks the build until a complete
    `GateSpec` is written for it, which is the point: the cost of a new gate is
    paid at the moment it is proposed, not deferred to whoever later has to
    trust it. -/
structure GateSpec where
  /-- Short title, for the published table. -/
  title : String
  /-- The rule, in plain language, for a general reader. -/
  plain : String
  /-- Is this gate mechanically enforced by CI, or is it a commitment a human
      must uphold? Honesty about this distinction is itself a gate. -/
  mechanized : Bool
  /-- The failure family this gate catches — the row it occupies in the coverage
      matrix in `GATES.md`. A family named here that is not in that taxonomy must
      arrive with its own incident. -/
  family : String
  /-- The incident that discovered or validated this gate, with commit hashes.
      Provenance is a pointer into the record, never a restatement of it. -/
  provenance : String
  /-- THE GATE'S OWN KILL: the stored case this gate must catch. If the gate
      passes its known-bad, the gate is dead. The honest literal
      "NONE-YET (recorded gap)" where no such case is stored. -/
  knownBad : String
  /-- The case this gate must pass — the reference against which a false alarm
      is diagnosed. Same honesty rule as `knownBad`. -/
  knownGood : String
  /-- Power certificate: what planted signal this gate has been SHOWN to detect,
      at what size. "UNVERIFIED" where no planted signal has been run past it.
      A null reading from a gate with no power certificate is not an all-clear;
      it is a gate that has not been calibrated. -/
  power : String
  /-- Validity scope, stated. Gates overclaim scope by default — the alphabet
      boundary is the standing example — so the boundary is written down rather
      than inferred from where the gate happened to be run. -/
  domain : String

namespace Gate

/-- All gates, in reporting order. -/
def all : List Gate :=
  [preRegistration, killsStakedFirst, separableKills, nullTypeMatch,
   tiedFractionDisclosed, biasControl, residualNeverSupport, reportTheKill,
   floorIsNotAbsence, noSorry, axiomAudit]

/-- The gates as instruments: each with its anchors, power and scope.

    `mechanized` keeps exactly the meaning it has always had — CI fails the
    build on this gate — and exactly the two `true` values it has always had.
    `floorIsNotAbsence` is still deliberately `false`: its supporting theorem
    (`S_pairwise_identity`) is machine-checked, but the gate is a rule about how
    instrument readings are INTERPRETED, and no build check can enforce an
    interpretation. Advertising the theorem's status as the rule's would be
    rounding up. `reportTheKill` is `false` for the same reason: the audit
    enforces its bookkeeping shadow (a dead claim keeps its killer), never the
    rule itself, which is about prominence.

    Several `power` fields read UNVERIFIED. That is a finding about this
    repository's gates, not a formatting choice; the empty cells are collected
    in `GATES.md`. -/
def spec : Gate → GateSpec
  | preRegistration =>
    { title := "Pre-registration"
    , plain :=
        "Write down exactly how you will measure something, and what each possible answer "
        ++ "would mean, BEFORE you look at any result. Once you have seen the answer you can "
        ++ "no longer choose the method honestly."
    , mechanized := false
    , family := "analysis-freedom (the garden of forking paths)"
    , provenance :=
        "a340eda — the sky measurement pre-registered with mocks-only eyes; 8b0c108 — "
        ++ "amendment 1 dated before any real number, moving the primary scale to R = 15; "
        ++ "f6515b2 — unblinding criteria fixed before the first data number existed."
    , knownBad :=
        "NONE-YET (recorded gap). No stored case of a post-hoc method choice is replayed "
        ++ "against this gate, and none can be: whether a file predates the peek is not "
        ++ "decidable from the artifact. The gate's failure mode is invisible by construction."
    , knownGood :=
        "8b0c108 and f6515b2 — amendments written, dated and committed before any data "
        ++ "number was read. The shape a legitimate mid-course change is supposed to have."
    , power :=
        "UNVERIFIED. No planted post-hoc choice has ever been run past this gate, so its "
        ++ "detection rate against the failure it names is unmeasured."
    , domain :=
        "Any measurement with analysis freedom. It bounds the FILE, not the eye: a timestamp "
        ++ "proves when text existed, never that nobody had already seen a result." }
  | killsStakedFirst =>
    { title := "Kills staked first"
    , plain :=
        "Before adopting an idea, say out loud what observation would prove it wrong. An idea "
        ++ "with no way to fail is not a claim about the world."
    , mechanized := false
    , family := "unfalsifiable-claim"
    , provenance :=
        "f8f9011 — the seed, where `kill` was made non-optional in `Claim`; audit check (4) "
        ++ "in Audit/AxiomAudit.lean, which additionally rejects a blank kill."
    , knownBad :=
        "A `Claim` literal omitting `kill` (does not compile) and one whose kill is "
        ++ "whitespace (audit check (4) refuses it). Both are live regression cases: the "
        ++ "type and the audit are exercised on every build."
    , knownGood :=
        "Every claim in `stance` — all carry a non-empty kill, and the audit passes on them."
    , power :=
        "VERIFIED for the missing/blank failure mode only: the type refuses the absent field, "
        ++ "the audit refuses the empty string. UNVERIFIED against a kill written to be "
        ++ "unreachable, which no check can distinguish from a demanding one."
    , domain :=
        "Claims in the published stance. Kills stated in prose elsewhere in the repository "
        ++ "are outside it." }
  | separableKills =>
    { title := "Separable kills"
    , plain :=
        "Each way of being wrong should take down only the claim it targets. If one bad result "
        ++ "would destroy everything at once, the ideas were tangled together, not tested."
    , mechanized := false
    , family := "coupled-failure (one falsifier takes down more than its target)"
    , provenance :=
        "4936786 — the dark wager split so its halves could die separately; 5789f7e — the "
        ++ "run-2 simulator gate filed separately, which restored run 1's reading."
    , knownBad :=
        "5789f7e — one gate firing had invalidated two runs at once. Separated, run 1 stood. "
        ++ "That is the stored case of the failure this gate exists to catch."
    , knownGood :=
        "4936786 — dark energy and dark matter carry their own kills, and the dark-energy "
        ++ "normalisation kill firing did not take the dark-matter claim with it."
    , power :=
        "UNVERIFIED. No deliberately entangled claim pair has been run past this gate to see "
        ++ "whether the entanglement is noticed."
    , domain :=
        "The structure of claims, not of statistics. A separable kill can still be the wrong "
        ++ "kill; separability says only that its blast radius is bounded." }
  | nullTypeMatch =>
    { title := "Null-type match"
    , plain :=
        "To know whether a pattern is real, compare it against a fake version of your data that "
        ++ "has no pattern in it. That fake must be built the same WAY your real data is — if the "
        ++ "real data is made of discrete counts, the comparison must be too. A mismatched "
        ++ "comparison is the most common way to fool yourself."
    , mechanized := false
    , family := "mixture/manufacture (a null that cannot produce the data's generative structure)"
    , provenance :=
        "9630d81 — the mixture null, under which the ECA order-3 spike collapsed 1886x; "
        ++ "00bcd4e and 4f3092d — P5 retracted after a no-dynamics mixture beat the noise "
        ++ "peak by up to 3.3x."
    , knownBad :=
        "9630d81 — the ECA order-3 spike: survives an iid null, collapses 1886x under a "
        ++ "mixture null that can manufacture it. Any null-type gate that passes this case "
        ++ "is dead."
    , knownGood :=
        "The parity state (`share_parity`): exactly one bit of whole-only share, and no "
        ++ "pair-preserving null can manufacture it. A null-type gate must leave it standing."
    , power :=
        "VERIFIED for the mixture family (9630d81, 1886x collapse) and for autocorrelation in "
        ++ "timeseries (phase randomisation, after iid nulls false-fired at +42 sigma). "
        ++ "UNVERIFIED for non-stationary and heavy-tailed generative structure."
    , domain :=
        "Finite-alphabet readings and stationary timeseries. Surviving a phase-randomised "
        ++ "null is NOT sufficient on its own: a clip artifact survives IAAFT at z = 86." }
  | tiedFractionDisclosed =>
    { title := "Tied-fraction disclosure"
    , plain :=
        "Some methods rank the data before analysing it. If many measurements are tied — for "
        ++ "example, lots of empty bins that are all exactly zero — the ranking has to break "
        ++ "those ties somehow, and that invents structure that was never there. Always report "
        ++ "what fraction was tied, because the false signal grows with it."
    , mechanized := false
    , family := "occupancy/sparsity (ties and empty cells read as structure)"
    , provenance :=
        "95d1b3c — order-3 on sparse data, where iterative proportional fitting is unsafe; "
        ++ "the untrained-model control that fires on tied activations alone."
    , knownBad :=
        "The untrained-model control, which fires on tied activations with no learned "
        ++ "structure present — a rank statistic reading its own tie-break."
    , knownGood :=
        "NONE-YET (recorded gap). No dense, tie-free reference case is stored as the "
        ++ "must-pass, so a false alarm here has nothing to be diagnosed against."
    , power :=
        "UNVERIFIED. The tied fraction is disclosed, but no planted-tie calibration says at "
        ++ "what fraction the gate is obliged to alarm. Disclosure is not detection."
    , domain :=
        "Rank-based and rank-adjacent statistics. Occupancy failures in non-rank estimators "
        ++ "need a separate occupancy gate, which this enumeration does not yet carry." }
  | biasControl =>
    { title := "Bias control"
    , plain :=
        "Any measure of shared structure reads slightly above zero purely from having a limited "
        ++ "amount of data. Shuffle your data to destroy the real structure, measure again, and "
        ++ "subtract that floor."
    , mechanized := false
    , family := "estimator bias (a finite-sample floor read as signal)"
    , provenance :=
        "b6527a8 — shot noise minted 130% of the deliverable, and the pre-registered null "
        ++ "turned out to be a power failure; 2161bee — the valve run that fixed the floor."
    , knownBad :=
        "b6527a8 — a shot-noise-only run reading 130% of the claimed effect. A bias control "
        ++ "that does not flag it is not a bias control."
    , knownGood :=
        "03cee87 — the sign-symmetric column, whose true whole-only share is exactly zero "
        ++ "(1b40fc4, machine-checked): a correct floor returns it to zero without inventing "
        ++ "a negative. Held as a live column, NOT yet pinned as a fixed regression case."
    , power :=
        "PARTIAL. Validated against shot noise at the scale where it mints 130% of the "
        ++ "deliverable (b6527a8). No planted-amplitude sweep exists, so the smallest signal "
        ++ "the gate can still see through its own floor is unmeasured."
    , domain :=
        "Plug-in information estimators on finite samples. It does NOT correct for "
        ++ "autocorrelation — that needs a phase-randomised null, a different gate." }
  | residualNeverSupport =>
    { title := "A residual is never support"
    , plain :=
        "A leftover that your theory does not explain is not evidence FOR your theory. Support "
        ++ "comes only from a specific prediction made in advance and then confirmed."
    , mechanized := false
    , family := "geometric-artifact (a tight error bar on the wrong quantity)"
    , provenance :=
        "c348c02 — Stage 2 withdrawn: the first production run measured a survey-geometry "
        ++ "artifact at sigma = 176, and the implausibly tight error bar was the tell; "
        ++ "2df2748 — headline magnitude withdrawn, 19 of the 20 largest readings outside "
        ++ "the bridge's validity regime."
    , knownBad :=
        "c348c02 — the sigma = 176 production reading that was pure geometry. Any gate "
        ++ "claiming to catch support-from-a-residual must fire on it."
    , knownGood :=
        "NONE-YET (recorded gap). No confirmed advance prediction is stored as the must-pass "
        ++ "case, so this gate has never been shown to let a real result through."
    , power :=
        "UNVERIFIED as an automated check. c348c02 was caught by a human noticing the error "
        ++ "bar was too tight for the quantity, not by any gate. That is the recorded gap."
    , domain :=
        "The interpretation of unexplained residuals. Not mechanizable: no build check can "
        ++ "tell support from leftover." }
  | reportTheKill =>
    { title := "Report the kill"
    , plain :=
        "When a test kills your own favourite result, say so as plainly and prominently as you "
        ++ "would have announced a success. The record keeps the dead claim, marked dead."
    , mechanized := false
    , family := "record-integrity (a fired kill quietly disappearing)"
    , provenance :=
        "02f72eb and e20aca9 — the maintenance-flow pricing of dark energy killed on four "
        ++ "independent legs, by us, within the hour, and published as such; c348c02 — a "
        ++ "withdrawal announced with the same weight the result would have had."
    , knownBad :=
        "A `dead` claim with an empty `killedBy`, or a living claim carrying one. Audit "
        ++ "check (6b) refuses both directions, so the bookkeeping half has a live case."
    , knownGood :=
        "The dead claims currently in `stance`, each with its killer, rendered on the page "
        ++ "in their own section rather than deleted."
    , power :=
        "PARTIAL, and the split matters: the BOOKKEEPING (a dead claim keeps its killer) is "
        ++ "enforced by audit check (6b); the RULE (as plainly as the survival) is not, "
        ++ "because nothing scores prominence. The mechanized flag is false for the rule, "
        ++ "not the shadow — under-claiming, deliberately."
    , domain :=
        "Claims that reached the stance. It cannot see a result killed before anyone wrote it "
        ++ "down, which is the larger and unmeasured population." }
  | floorIsNotAbsence =>
    { title := "A floor is not an absence"
    , plain :=
        "If your instrument is known to be blind to something, its reading zero does not mean "
        ++ "that thing is absent. It means you did not look with an instrument that could see it."
    , mechanized := false
    , family := "power-of-the-control (a null reading from an uncalibrated instrument)"
    , provenance :=
        "0885182 — the doped control failed W3: the doping was the wrong probe, so the null "
        ++ "reading carried no power certificate; a586449 — K-VOID fired on our own solver; "
        ++ "b611a5b — a gate that certified the bridge along the wrong axis."
    , knownBad :=
        "0885182 — a null reading produced by a control that could not have detected the "
        ++ "planted signal. The stored case for 'zero means blind, not absent'."
    , knownGood :=
        "`S_pairwise_identity` — the pair instrument reads exactly zero on the parity state, "
        ++ "whose whole-only share is exactly one bit (`share_parity`). Machine-checked, and "
        ++ "the reference case for the whole rule."
    , power :=
        "The RULE has a machine-checked witness. The GATE has none: no automated check "
        ++ "refuses a write-up that reads a floor as an absence."
    , domain :=
        "Lower-bound instruments. A rule about interpretation, so it holds wherever a reading "
        ++ "can be a floor, and is enforceable nowhere." }
  | noSorry =>
    { title := "No sorry"
    , plain :=
        "In a machine-checked proof, an admitted gap is a hole. No holes reach the published "
        ++ "branch; anything unfinished is named as open rather than quietly assumed."
    , mechanized := true
    , family := "textual/use-position (a check matching the word rather than the use)"
    , provenance :=
        "a843840 — the textual layer cried wolf on this repository's own documentation: the "
        ++ "`admit` arm was written as a bare word while every other arm matched use "
        ++ "position. The semantic replacement is `assert_no_sorry` in Audit/AxiomAudit.lean."
    , knownBad :=
        "A declaration closed by an admitted gap — including one inherited through an import, "
        ++ "and one hidden from Lean's own warning by `#guard_msgs`. `collectAxioms` sees all "
        ++ "three; a grep sees only the first."
    , knownGood :=
        "a843840 — this repository's own prose, which contains the keyword in every "
        ++ "documentation file and must NOT fire. The textual layer failed exactly this case "
        ++ "before the fix, and a gate that cries wolf gets switched off."
    , power :=
        "VERIFIED in both directions at a843840: all four invocation forms still caught, "
        ++ "prose clean. Re-run on every build."
    , domain :=
        "Lean declarations reachable from the library's root import. A declaration outside "
        ++ "that import closure is not audited by this gate." }
  | axiomAudit =>
    { title := "Axiom audit"
    , plain :=
        "Check what each proof actually rests on. A result is only as strong as the assumptions "
        ++ "underneath it, so those assumptions are listed automatically, not from memory."
    , mechanized := true
    , family := "artifact-vs-description (a hand-maintained record drifting from the artifact)"
    , provenance :=
        "edbec73 — the hand-copied audit table was removed from epistemology.md because it "
        ++ "had drifted, exactly as predicted; the exact two-directional pins live in "
        ++ "Audit/AxiomAudit.lean section (3)."
    , knownBad :=
        "A declaration reaching for `native_decide`/`Lean.ofReduceBool`, which a gap-only "
        ++ "check passes; and any theorem whose dependency set CHANGES in either direction, "
        ++ "including becoming stronger, which the exact pins refuse."
    , knownGood :=
        "The current published set: every witness stops at propext / Classical.choice / "
        ++ "Quot.sound, and every pin reproduces its recorded output verbatim."
    , power :=
        "VERIFIED for the axiom-set failure mode — the pins fail on any change, in either "
        ++ "direction. UNVERIFIED, and unverifiable, as a check that a theorem says what its "
        ++ "headline says; that is human by construction."
    , domain :=
        "Declarations NAMED in this audit. A theorem in the library but absent from the list "
        ++ "is unpinned, and the list is hand-extended — a recorded gap in the gate itself." }

/-- Short title. -/
def title (g : Gate) : String := (spec g).title

/-- The rule, in plain language, for a general reader. -/
def plain (g : Gate) : String := (spec g).plain

/-- Is this gate mechanically enforced by CI, or is it a commitment a human
    must uphold? Honesty about this distinction is itself a gate.

    Exactly `noSorry` and `axiomAudit` are `true`, and Audit/AxiomAudit.lean
    section (5) fails the build if that stops matching what it actually runs.
    Every other gate is a commitment a human keeps; see `spec` for why the two
    with machine-checked SUPPORT (`floorIsNotAbsence`, `reportTheKill`) are
    nonetheless flagged `false`. -/
def mechanized (g : Gate) : Bool := (spec g).mechanized

/-- The failure family this gate catches. -/
def family (g : Gate) : String := (spec g).family

/-- The incident that discovered or validated this gate. -/
def provenance (g : Gate) : String := (spec g).provenance

/-- The stored case this gate must catch — the gate's own kill. -/
def knownBad (g : Gate) : String := (spec g).knownBad

/-- The case this gate must pass. -/
def knownGood (g : Gate) : String := (spec g).knownGood

/-- The power certificate: what planted signal it has been shown to detect. -/
def power (g : Gate) : String := (spec g).power

/-- The stated scope of validity. -/
def domain (g : Gate) : String := (spec g).domain

/-- Does this gate have a stored known-bad case, or a recorded gap? Read by the
    published table, so a missing anchor is visible to a reader rather than
    only to whoever opens this file. -/
def hasKnownBad (g : Gate) : Bool := !((spec g).knownBad.startsWith "NONE-YET")

/-- Same, for the must-pass case. -/
def hasKnownGood (g : Gate) : Bool := !((spec g).knownGood.startsWith "NONE-YET")

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
  /-- Every gate carries its own anchors, and where a stored case does not exist
      the field says "NONE-YET (recorded gap)" rather than inventing one. A gate
      is an instrument; an uncalibrated instrument is declared, not disguised. -/
  gate_anchors_are_honest : True

/-- The gates are in force. -/
def honesty_gates : HonestyGates := ⟨trivial, trivial, trivial, trivial⟩

end CIRISOntology.Core
