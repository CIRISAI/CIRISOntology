# GATE PROPOSAL — a gate correctly declared, correctly implemented, and keyed to the wrong object

**A proposal to `GATES.md`, not an amendment to it.** Filed by the water campaign. The
generalisation is the glass campaign's; the incident that prompted it and two earlier instances
are this campaign's. Companions: `GATE_PROPOSAL_WARRANT.md` (glass), `GATE_PROPOSAL_COST.md`
(water).

**Nothing here is added to any campaign's battery as though registered.** No Lean file opened,
`Stance.lean` untouched, nothing pushed.

---

## The reach

> **A gate whose polarity is correctly declared and correctly implemented, but whose threshold is
> keyed to a PROXY rather than to the object the gate means to bound.**

Both halves of the existing check pass. The declared direction and the implemented direction
agree — so **`GATES.md` reach 8 (probe polarity) is silent** — and no justification is wrong, so
**the warrant reach is silent too.** The gate fires or fails to fire correctly *with respect to
its stated parameter*, and its stated parameter is standing in for something else.

**Distinguished from its two neighbours:**

| | what is wrong |
|---|---|
| reach 8, probe polarity | declared direction ≠ implemented direction |
| the warrant reach (proposed) | right claim, wrong justification |
| **this** | right direction, right implementation, **threshold keyed to a proxy variable** |

## The tell, and it is mechanically scannable

> **A numeric constant in a gate definition, where the quantity being bounded is measurable.**

That is greppable in a way the warrant reach is not: enumerate every literal threshold in a gate
specification and ask, of each, *what measured quantity is this constant standing in for, and why
is it not measured?* A constant is legitimate when the bounded quantity is genuinely fixed
(alphabet size, slot count). It is a proxy whenever the bounded quantity varies with the state
point — which is exactly when a campaign is sweeping something.

## Instances, all already on the record before this proposal was written

**(1) The 3 × ceiling-comparability rule.** `WATER_PREREG.md` §5.4 fixed *"no ceiling fraction is
compared across cells whose ceilings differ by more than 3 ×."* Withdrawn in
`WATER_AMENDMENT_3.md` C1 after the glass campaign adjudicated it against planted values. **Its
own diagnosis used this reach's language before the reach existed:** *"a rule phrased on the ratio
between two cells' ceilings voids comparisons between two large well-measured ceilings that happen
to differ, and permits comparisons between two tiny ones that happen to match — **a proxy for the
real failure mode rather than the failure mode**."* The object was the differential bias; the
proxy was a ceiling ratio.

**(2) Outcome (j) / K-VOID, the far arm.** `WATER_PREREG.md` §8 declared *instrument fouled* when
the far arm at a **fixed `r = 7.0 Å`** reads above floor. The object is *"beyond the correlation
length"*; the proxy is a constant radius. Corrected in `WATER_AMENDMENT_10.md` J3, and the
consequence is the reason this proposal exists: near a Widom line `ξ` grows, so **the gate
declares every reading ungauged exactly where the effect is predicted, and does so because the
effect is there.** A gate that converts a detection into a void is worse than a gate that misses.

**(3) The far-arm radius itself.** The same `7.0 Å`, chosen by analogy with another substrate's
`r ∈ {5, 6} σ_AA`, is `2.3 ξ` at `ξ = 3 Å` — inside the length it was meant to clear
(`WATER_AMENDMENT_10.md` J1).

**A candidate not claimed, because it has not been shown to fail:** `GATES.md` reach 11's
occupancy floor is *"≥ 30 counts per cell"*, a constant standing in for *"the estimator's
asymptotics hold here"*. Whether 30 is a proxy that misfires is unmeasured, and naming it is not
asserting it.

## The remedy

> **Key the gate to the measured quantity, and make the measurement a prerequisite of the gate
> rather than an input to it. Where the measurement is unavailable, the cell is UNGAUGED — not
> PASSED and not FAILED.**

`WATER_AMENDMENT_10.md` J3 is the worked example: `ξ` is measured per state point, the radius
becomes `max(3ξ, 7.0 Å)`, a state point where `3ξ > L/2` has **no far arm at all** and is reported
NOT RUN, and outcome (j) fires only when a far arm that *exists* still reads above floor.

**Note the direction of that correction, because it is the one to be suspicious of:** it makes the
gate **less** likely to fire. It is paid for by **adding a required measurement**, which is the
test a loosening correction should have to pass — a correction that only loosens is a correction
to distrust.

## What is NOT claimed

**No plumb line and no dye test.** Three instances found after the fact, all in one campaign, all
by cross-reading rather than by procedure. This is a hypothesis about how gates fail, not a
validated gate, and by `GATES.md`'s own lifecycle it would enter as **proposed** — which is where
nine of the existing thirteen already sit, and that is an argument for registering it carefully or
not at all.

**It shares the warrant reach's validation problem.** The scannable tell above has never been run
prospectively by anyone, and a catalogue assembled after the rule was written cannot measure its
recall or its false-positive rate. **The same planted-artifact requirement applies**, with the same
condition: planted by one party, scored by another who does not know `n` or whether `n > 0`, on a
document neither wrote, routed through the registry's owner rather than arranged between the
proposers.

---

Proposed 2026-07-27 by the water campaign; generalisation credited to the glass campaign.
Adjudication belongs to whoever owns `GATES.md`.
