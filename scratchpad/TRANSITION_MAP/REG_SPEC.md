# REG — the Raw Epistemic Grammar (v0.1, 2026-08-21)

Named by the steward. REG is the neutral counterpart of CEG, constructed by taking the
other branch at each fork the CEG representation analysis proved (CEG_REPRESENTATION.md):
composition over C instead of an ordered lattice; group instead of monoid at the record
layer; holonomy observable instead of forbidden; exact conservation default instead of
attenuation. REG is a RESEARCH INSTRUMENT — the lab-frame grammar. It deliberately removes
CEG's anti-attack defenses so the attack sector becomes measurable. IT MUST NEVER BE
DEPLOYED AS TRUST INFRASTRUCTURE; CEG's flatness exists because attacks exist. The pair is
the experiment: REG measures what CEG suppresses.

## States and values

A REG state assigns to each (subject, dimension) an amplitude z in C with |z| <= 1.
|z| is confidence-weight; arg z is STANCE ANGLE: 0 = full assertion, pi = full denial,
intermediate angles = partial reframings (the arc CEG amputates — CEG's phase group is
the Z2 endpoints {0, pi}). Dimensions: the eleven kinds are the default basis (empirically
grounded); nothing in REG fixes eleven — basis adequacy is an input from the corpus
programme, not a REG theorem.

## The five verbs (the U(1) lifts of CEG's 1+4)

| CEG | REG lift | action |
|---|---|---|
| scores | **attest** | add amplitude z to (subject, dimension) |
| delegates_to | **channel** | compose along a scope edge; norm-preserving by default; gain/attenuation a MEASURED edge weight, not a norm |
| supersedes | **rotate** | unitary replacement old -> new (invertible) |
| withdraws | **invert** | the group inverse of a prior attest (removes its amplitude exactly) |
| recants | **flip** | multiply by e^{i pi} — the phase flip; REG's special case of continuous reframing e^{i phi} |

Record layer: the op sequence, group-composable, invertible — loses nothing.
Readout layer: verdict(subject, dim) = |sum of amplitudes|^2 — ordered, lossy,
phase-blind, and the ONLY place order appears. INTERFERENCE IS PERMITTED: two attesters'
amplitudes can cancel or reinforce. This is the substantive dynamical difference from
CEG's lattice aggregation (which can trump but never cancel), and it is REG's first
empirical hook: does wild epistemic aggregation show sub/super-additivity?

Holonomy: channel loops carry accumulated phase/gain — REG's second empirical hook, and
an OBSERVABLE, measured only on substrates that do not defend loop gain (the staked
instrument exclusion stands).

## Status and credits

WAGER-CLASS instrument spec. Credits pending the running prior-art sweep (quantum
cognition; DisCoCat; provenance semirings; gauge theory of finance) — the sweep's verdicts
attach here on arrival and take precedence over any novelty impression. The contraction
conjecture (CEG = REG under kill-phases + order-the-values + attenuate) is the companion
Lean target.

## The two tests (steward-ordered), with the anti-tautology flag

T-REL (relevance to the corpus): the stage-1 alignment protocol re-run verbatim with
REG's five verbs — blind mappers, act-kind + follows, counts rule. Then (second stage) an
encoding check on wild changes.
T-A2A (apples to apples): the six-row table re-derived for REG at the same standard as
CEG's — with every row FLAGGED either BY-CONSTRUCTION (passes because we built it to;
uninformative, and said so) or CONTINGENT (informative). The contingent core: can REG
carry what the corpus actually uses (verdicts, trust decisions) while keeping the A2A
properties — i.e., does the amplitude layer do real work on real traffic, or is it
decoration over a readout that was always sufficient?

## The safety principle (steward, 2026-08-21)

Defining CEG vs REG is STRONGER THAN CEG ALONE as a safety move: with REG as the lab
frame, every CEG defense becomes derivable — "REG minus a named threat" — instead of
asserted. Flatness is not a design taste; it is the measured kill of loop-gain laundering.
Lattice aggregation is not a convenience; it is the measured kill of cancellation attacks
(an adversary attesting in antiphase to erase honest standing — REG makes that attack
EXPRESSIBLE, hence measurable, hence a named thing CEG provably prevents). The safety
posture of the deployed grammar is then a THEOREM about the difference of two grammars,
with the threat model carried in the difference. Armor you can derive is armor you can
audit.

## T-A2A VERDICT (2026-08-21, REG_A2A.md): NO — and the pattern is the finding

REG passes exactly the rows it was built to pass and loses every row that could have gone
either way. The decisive results, adopted into this spec:

1. **REG's entire dynamical group is contained in flavour's GAUGE group** — the diagonal
   torus. Every REG verb is diagonal in the kind basis; no generator carries one nonzero
   off-diagonal element; and independently, the confidence bound makes the state space an
   l-infinity polydisc whose symmetry group is mixing-free. Doubly forced: THE
   ELEVEN-KIND INTERFEROMETER IS NOT IN REG.
2. **The GENERALIZED instrument exclusion** (staked forward in REG_A2A §0, adopted):
   any verdict-producing grammar — any grammar whose readout must be a deterministic
   function of the record — reads zero loop phase BY CONSTRUCTION (flat by readout
   well-definedness, a second mechanism beyond CEG's flat-by-threat-model). Removing the
   threat model is not sufficient. The loop-phase instrument cannot be an accountability
   protocol at all.
3. **{group, invertible, lossless} is unsatisfiable at the record layer** — choosing
   invertibility SPENDS the Record kind. And the Born-form readout DESTROYS POLARITY (an
   internal inconsistency with this spec's own stance-angle requirement).

## REG v0.3 DIRECTION (from REG_A2A §8.3) — the sixth verb, and the number candidate

The missing object is a CROSS-KIND CHANNEL: transport of amplitude from kind d to kind
d' with a complex weight — the mixing matrix's off-diagonal element as a verb. Its moduli
are ALREADY MEASURED: the three confusion boundaries (Premises/Facts, Structure/Manner,
Model/Facts) and BABEL's localized leakage are the candidate non-zero entries. THE
NAME-THE-NUMBER CANDIDATE (per the gate, named before any instrument): the PHASE of a
cross-kind channel, measured as ROUTE INTERFERENCE — whether two routes into the same
kind (e.g. Premises->Facts direct vs Premises->Model->Facts) combine sub- or
super-additively in wild reading, against the classical additive account, with the
deflationary readings (attention, primacy, framing) excluded by design. BABEL-2's
narration effect (11/55) is the existence hint, not the number. Until that number is
staked with its null and its deflation controls, REG v0.3 remains instrument-spec.

## REG v0.3 (2026-08-21, steward-directed): the 5+1

The sixth verb, added: **carries** (plain: "arrives as" — one kind of change arriving as
another; the wearing verb the plain-language stance has used since RATCHET's README: "a
changed assumption arrives as a burst of changed Facts"). Formally: transport of claim
content from kind d to kind d' with complex weight w_dd' — the mixing matrix's
off-diagonal element as an act. SAFETY DIFFERENTIAL ENTRY: CEG forbids this verb by
construction (firewalled dimensions); in threat language the verb is KIND-LAUNDERING — a
change smuggled past a per-kind auditor wearing another kind. CEG walls the attack; REG
v0.3 measures it. The differential now carries three named attacks: loop-gain laundering
(flatness), cancellation erasure (lattice aggregation), kind-laundering (firewalling).

## THE PROGRAM, restated per the steward (the A2A comparand is the PRODUCED dynamics)

The object: 11+1 (the kinds and the Record) instrumented by 5+1 (the verbs and carries).
The measurand: the transition dynamics the instrumented corpus produces — the 11x11
matrix of moduli (already partially measured: the three boundary channels, surface
absorption, BABEL leakage) and the candidate phases (route interference — the named
number). The comparison, EASILY FALSIFIABLE, staked as structure tests against flavor dx:

| stake | flavor-side property | falsified if |
|---|---|---|
| FD1 normalization | rows of the measured mixing object approximately conserve (unitarity analogue) | measured row sums scatter with no conserved normalization under the staked estimator |
| FD2 hierarchy | off-diagonal moduli fall with generation-like distance (CKM's near-diagonal cascade) | measured moduli are flat or non-monotone in every ordering of the kinds |
| FD3 localization | off-diagonals concentrate in few channels (as measured: three boundaries + surface absorption) | new instruments spread the mass diffusely |
| FD4 phase sector | a nonzero Jarlskog-analogue exists: route interference at a staked loop | interference indistinguishable from the additive null with deflations excluded |
| FD5 factorization | the matrix factors consistently with the 4+7 block anatomy | no block structure survives estimation |

Instrument for the moduli: LEG C (the wild revision-chain matrix), ready to run.
Instrument for FD4: the route-interference design, owed its own prereg, bound by the
name-the-number gate. NOTHING here claims flavor physics; the comparison is between two
measured finite structures, and every row above can die.
