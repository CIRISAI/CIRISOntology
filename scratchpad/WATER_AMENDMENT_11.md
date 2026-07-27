# WATER — AMENDMENT 11: the cap fix verified on a second instrument, and a third reach filed

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–10. No water configuration
exists.** The pre-registration is not edited. This is the shortest of the eleven and records
three things: an independent verification, one implementation detail that matters for arm B, and
a proposal filed elsewhere.

---

## K1. THE TRIANGLE CAP, VERIFIED ON AN INDEPENDENT INSTRUMENT

Glass implemented amendment 9's fix in `glass_run.triangles_from_d2` and `glass_share.triangles`
and measured it on its own configurations (`glass_capfix.py`, `c366256`):

| cap | kept | ordered capping | **triangle capping** |
|---|---|---|---|
| 10 000 | 9 996 | 9.2e−03 | **0.000e+00** |
| 5 000 | 4 998 | 2.3e−02 | **0.000e+00** |
| 2 000 | 1 998 | 1.8e−02 | **0.000e+00** |

**Exact at every cap, same kept count, on a different substrate and a different instrument from
the synthetic test of amendment 9 I2.** The fix is now verified twice, independently.

### K1.1 The implementation detail that matters for arm B's scalene rungs

Glass flagged, and it resolves a question amendment 9 did not ask: **for a fully scalene template
the orbit size is 1, so the triangle cap reduces exactly to the ordered cap** — which is correct,
because there is no symmetry to preserve. **So the same code is right across this campaign's
entire template grid with no special case**, from the fully symmetric far arm (orbit 6) through
the primary tetrahedral template (orbit 2, amendment 7 G2) to any scalene rung (orbit 1).

That the orbit size is exactly the number of orderings the class partition assumes is not a
coincidence — **they are the same group acting**, which is why one fix serves both the cap and the
ceiling estimator. Recorded because it is the reason no per-template branch is needed.

---

## K2. GLASS'S FAR ARM CLEARS THIS CAMPAIGN'S OWN CRITERION

Amendment 10's `r_far ≥ 3ξ` was derived on this substrate and glass checked it against its own
rather than assuming it transferred:

| `T` | `ξ` | `r = 5` | `r = 6` |
|---|---|---|---|
| 0.44 | 1.111 | **4.50 ξ** | 5.40 ξ |
| 0.64 | 1.045 | **4.78 ξ** | 5.74 ξ |

Past `3ξ` at both ends, **with a margin that does not degrade at the cold end** because `ξ` barely
moves. So the criterion binds this campaign and not that one, which is the correct outcome: the
difference is that one ladder approaches something that diverges and the other does not.

---

## K3. A THIRD REACH, FILED — `GATE_PROPOSAL_PROXY.md`

Glass observed that amendment 10 J3's failure is covered by neither existing proposal nor by
`GATES.md` reach 8:

> **A gate correctly declared and correctly implemented, keyed to a PROXY rather than to the
> object it means to bound.** Reach 8 checks that the declared direction matches the implemented
> direction — and both can match while the parameter the direction is declared *against* is the
> wrong object.

Filed as `GATE_PROPOSAL_PROXY.md`, with the generalisation credited to glass and three instances
that were **already on the record before the proposal was written**: the withdrawn 3 × ceiling
rule (amendment 3 C1 — whose own diagnosis used this reach's language, *"a proxy for the real
failure mode rather than the failure mode"*, before the reach existed), outcome (j)'s fixed radius
(amendment 10 J3), and the far-arm radius itself (J1).

**Its tell is mechanically scannable and that is its one advantage over the warrant reach:** a
numeric constant in a gate definition, where the bounded quantity is measurable. Enumerate every
literal threshold in a gate specification and ask what measured quantity it stands in for.

**Filed with the same limits stated as the other two**: no plumb line, no dye test, three
after-the-fact instances in one campaign, and the same planted-artifact requirement — planted by
one party, scored by another who knows neither `n` nor whether `n > 0`, on a document neither
wrote, **routed through the registry's owner rather than arranged between proposers.** Three
proposals now sit against a registry where nine of thirteen reaches are already *proposed while
being used as validated*; that is an argument for registering carefully or not at all, and it is
made in each document rather than left for the reader.

---

## K4. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law and overlap penalty; the primary label
and template; the template exclusions; amendments 1–10 entire. K1.1 adds no requirement and
removes none — it records why the amendment 9 fix needs no per-template branch.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

Primary seed **20260727**.
