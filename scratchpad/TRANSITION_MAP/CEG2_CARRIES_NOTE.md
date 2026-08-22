# CEG2 — the form of carries: not a cursor, a ROOM COUNT (2026-08-22)

Steward's question: CEG is a wire format carrying scores attestations; what form makes
carries effective? Answer: BUDGETED CHANNELS WITH SLOT-CONSUMING TRANSPORTS.

## The design

1. CHANNEL OPENING — delegates_to-shaped (the spec's own extension pattern: moderation
   rode delegates_to scopes; promote rode supersedes). A carries-channel attestation
   declares: (dim_from, dim_to, ceiling R, |w|max weight bound, validity window),
   owner-bound, revocable via withdraws, sub-channels ATTENUATE (R_child <= R_parent,
   the child-scope-subset rule applied to capacity — never amplify, verbatim CEG law).
2. TRANSPORT — rides scores. An ordinary scores attestation gains envelope members:
   transported_via: <channel_id>, slot: k with k in 1..R, slot unique-use. The claim
   lands on dim_to citing its dim_from origin and the room it occupies.
3. THE AUDIT IS A ROOM COUNT: live transported attestations through channel c <= R_c —
   checkable by ANY consumer from the graph alone, no trust required. Aggregate
   transport is the governed object; laundering cannot hide volume in instances.

## Why room-count beats cursor (each reason independently sufficient)

- AGGREGATE AUDITABILITY: the attack is undeclared volume; a ceiling governs volume.
- CONSERVATION ON THE WIRE: FD1/P1 (the physics-likeness conservation criterion) gets a
  wire-format invariant — the atlas's conservation row acquires its CEG2 shadow, and
  declared-vs-measured channel usage becomes the standing audit (RATCHET series metric).
- THE LATTICE'S LESSON: finite occupancy + exact conservation sectors is the combination
  that produced lawful dynamics (2^6 rooms -> FHP -> the holonomy result); unbounded
  amplitude bookkeeping is the combination that produced nothing measurable.
- COMPOSITION FOR FREE: ceilings compose by subset like scopes; no new admission math.
- FAIL-SECURE DEFAULT: no channel declared -> R = 0 -> carries impossible -> CEG1
  recovered exactly. CEG2 is a strict opt-in extension; the 1+4 lockdown survives as
  the R=0 sector.

## Layer honesty

Wire-mechanically this is "1+4 preserved" (channel = delegates_to-shaped; transport =
scores + envelope vocabulary) — the spec's own extension idiom. Semantically it is the
sixth verb (the charter's 1+4+1). Both true at different layers, like promote/supersedes.
The ceiling governs MODULUS only: arg(w) remains unrepresented — CEG2 stays flat, per
the verdict-grammar flatness theorem; phase lives lab-side in REG+ where it belongs.

## The classifier tie-in

H3ERE2's stage-2 carries-inversion consults the channel table as a wire-level prior:
which transports are even lawful here. The classifier and the protocol share one channel
object; the atlas measures actual usage against declared room.
