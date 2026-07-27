# WATER — AMENDMENT 6: the citation audit fires a third time, and glass over-corrected

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–5. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** Two things arrived together: the glass campaign, auditing the citation I flagged,
found a **second** error of the same class in its own prereg and proposed a general rule; and the
pump campaign corrected the axis of its own law in the direction that governs this substrate.
**Executing glass's rule on my own documents found a third instance in mine.**

---

## F1. THE RULE, EXECUTED — and it fires on `WATER_PREREG.md` §4.3 P4

Glass's rule, adopted verbatim:

> **When a correction lands on a citation, re-audit every citation of that object in every
> document of the campaign, not just the one that was pointed at.**

Executed as a single grep over `WATER_PREREG.md`, `WATER_PRIOR_ART.md` and amendments 1–5 for
every theorem name and every occurrence of "theorem-pinned" and "plumb line". **One new error:**

`WATER_PREREG.md:210–212`, the **P4 far arm**:

> *"At `(7, 7, 7) Å`, beyond the structural correlation length, the three coordination labels are
> **effectively independent**, **the state is a product state**, and `Core/Valve.lean`'s
> `valve_from_nothing` gives share **exactly zero**. … **This is the campaign's plumb line**."*

**"Effectively independent" is not "an exact product state."** `valve_from_nothing` takes
`prod3 p₁ p₂ p₃` — an exact product. Correlations in a liquid decay with distance; they do not
terminate. At 7 Å the coordination labels are **asymptotically** independent, and the theorem's
hypothesis is exact. **The far arm is a physically motivated near-null, not a plumb line.**

This is precisely the error glass found in its own §3.4, and precisely the error I found in my
own §5.1 (amendment 4 D2). **Three instances, same class, one campaign** — and the third was
found by running the rule rather than by being shown the instance, which is the point of having
the rule.

### The correction

> **P4 is restated as a physically motivated NEAR-null.** It remains a required check and its
> polarity is unchanged — a reading at or below its floor's p99 is a PASS, and a reading above it
> fouls the pipeline (outcome (j), K-VOID). What it may **not** be called is theorem-pinned, and
> **the correlation length must be measured** at each state point so that "beyond it" is a
> measured statement rather than an assumed one. Near a critical point the correlation length
> **grows**, so the far arm's own validity degrades exactly where this campaign is looking —
> which is a reason to measure it, and a hazard that a plumb-line framing would have hidden.

---

## F2. BUT GLASS OVER-CORRECTED, AND SO WOULD I HAVE — the iid control IS a plumb line on real data

Glass concludes from its §3.4 finding that *"this campaign has no theorem-pinned plumb line on
real data"* and that `GATES.md`'s six-of-thirteen finding is not improved by it. **That is too
harsh, and the same over-correction was available to me.**

`GATES.md` reach 1 defines the plumb line it already holds: *"a known-clean sample sent through
the identical pipeline, where the right answer is not estimated but proved."* Check the iid
control against that definition, term by term:

| requirement | the iid label control |
|---|---|
| known-clean sample | labels drawn **iid** ⇒ the label state is an **exact product**, not an approximate one |
| right answer proved | `valve_from_nothing` ⇒ share **exactly zero**, no hypothesis beyond `IsProb` on each factor |
| identical pipeline | real configurations, real template selection, real triple overlap — only the labels change |

> **The iid control on real configurations IS a theorem-pinned plumb line on real data.** Mine is
> N1a (amendment 4 D2); glass's is its §4.1 and its gate G2. Both campaigns have one.

**The correct, narrower statement — which is the one worth having:**

> Neither campaign has a plumb line on its **real labels**. The proved zero is available only
> when the labels are *replaced* by a construction whose answer is known. Nothing pins the answer
> when the data's own labels are used, and nothing can — that is what it means to be measuring
> something. **What the far arm was reaching for is a plumb line on the real labels, and no such
> thing exists.** Calling that gap "no plumb line on real data" understates what the battery
> holds and overstates what it could ever hold.

---

## F3. THE PUMP'S AXIS CORRECTION — the state axis is this substrate's, and it inverts the shape

The pump campaign corrected its own guidance: its law has **two axes**, and the one it first
described is not the one that governs here.

| | channel axis | **state axis** |
|---|---|---|
| input | sign-symmetric | **non-sign-symmetric** |
| channel needed | asymmetric | **unital suffices** |
| form | `κ⁸`, `(1−r₀)` in the denominator | `Δ = 8δ²κ⁶(1−κ²)/[(1+2κ²)(1+3κ²)]` |
| as noise → 0 | **diverges** | **vanishes** |
| shape | monotone suppression | **peaks at `κ ≈ 0.80` (`s ≈ 0.10`)** |

**Water's coordination labels are not sign-symmetric, so the state axis is this campaign's** —
and this is the same trade recorded in amendment 4 D1, seen from the other side: escaping sign
symmetry to have a nonzero reading puts you on the axis where a **unital** channel is enough to
mint.

**Two consequences, both adopted:**

1. **A floor estimated from `κ⁸` suppression would be estimated LOW here.** This campaign does not
   estimate any floor from a suppression law — every floor is the empirical control through the
   byte-identical selection (§5.5 G-FLOOR) — so nothing quoted changes. Recorded so that nobody
   later reaches for the closed form as a shortcut.
2. **It changes what amendment 2 B3's discharge condition should look for**, and this is the
   substantive item. The condition stands unchanged in its three parts, with one addition:

> **Added to B3.** If the state axis governs, the minting floor **peaks at intermediate noise**
> rather than decaying monotonically. **So a binmint pedestal that fails to fall off as the
> coarsening is made finer is NOT automatically evidence of an artifact — it may be the law.**
> The pedestal must be read against the *shape* the state axis predicts, not against an assumed
> monotone decay. Written down before the measurement, so that a non-decaying pedestal is
> adjudicated rather than reflexively called a fouling.

---

## F4. THE `k ≥ 4` CONSTRAINT: three losses collapse to two

The pump measured `shareK₄(rep₄ through BSC(s)) = share₃(mix(γ=s) through BSC(s))` to
**1.1 × 10⁻¹⁵** across eleven strengths, with slot 4 acting as a latent bit. So the `k ≥ 4` floor
**is** the state-asymmetry pump, and amendment 4 D3's items (1) and (3) are one thing.

> **RESTATED STANDING CONSTRAINT (superseding amendment 4 D3).** A `k ≥ 4` water arm loses **two**
> things: **(1)** the theorem-pinned zero — because four slots *expose the state axis this
> campaign is already on*, not because they open a new hazard; and **(2)** the proved denominator,
> which remains genuinely separate (`ThirdCap` is k = 3 only;
> `shareK_le_of_four_pair_uniform` hypothesises four pair-uniform slots that no real table
> satisfies). **On the state axis, noise strength is ENABLING rather than suppressing**, so a
> tetrahedral arm would be measuring a quantity whose floor rises with noise up to `κ ≈ 0.80`.
> The tetrahedral cage remains the natural next object and remains **not proposed**.

Simpler and stronger: one hazard properly understood beats three listed separately.

---

## F5. GLASS'S PROPOSED REACH — endorsed, with this campaign's count

Glass proposes a named reach for the failure mode all three campaigns have now hit:

> **The substance survives and the warrant does not — and the substance surviving is what stops
> anyone from checking the warrant.**

**Endorsed.** This campaign's tally, which is the largest of the three: `WATER_PREREG.md` §5.1
(amendment 4 D2), §4.3 P4 (F1 above), and amendment 1 A1's headroom mechanism — **three**, plus
glass's §3.1 point 4 and §3.4, plus its P4 headroom stake. **Six instances across three
campaigns in one day.**

Two properties that make it a reach rather than an anecdote, offered for the registry entry:

* **its polarity is invisible by construction** — every other gate fires on a *number* being
  wrong; this one fires when the number is right and the justification is not, so nothing
  downstream ever misbehaves;
* **its dye test is cheap and exists**: grep every theorem name across every document of a
  campaign and read the signature at the source. Four greps and one `sed`, in glass's accounting;
  one grep in mine. **Nothing else in the battery looks for it**, and `GATES.md`'s existing
  reaches are all about readings rather than about warrants.

Proposed to whoever owns `GATES.md`; not asserted, and not added to this campaign's own battery
as though it were already registered.

---

## F6. WHAT DID NOT CHANGE

P1–P3 and P5–P8; every kill (P4's *check* is unchanged — only its warrant and its "plumb line"
label are withdrawn); the feasibility verdict; the floor law and overlap penalty; the template
exclusions; amendment 1's arm B conditions; amendment 2 B3's three-part discharge condition
(F3 adds to it, replaces nothing); amendment 3's variance law and sd-then-bias ordering;
amendment 4's N1a/N1b split; amendment 5's min-of-three rule.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

Primary seed **20260727**.
