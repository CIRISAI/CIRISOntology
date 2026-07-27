# WATER — AMENDMENT 1: a mechanism claim retracted, a gate rule kept, and arm B's conditions

**Written after `WATER_PREREG.md` was frozen and before any water configuration exists.** The
pre-registration is not edited; this document supersedes the parts of it named below, and every
superseded statement is quoted here rather than removed, per `GATES.md` harvest
(*current-numbers hygiene*).

**Occasion.** The glass campaign checked both of the findings I sent it against its own real
readings. One was confirmed and turned out to bite harder than I had measured. **The other was
mine and it was wrong**, and its refutation was already sitting in stage-0 data I had computed
and not interrogated.

**Nothing here changes the campaign's forward predictions (P1–P7), its kills, or its feasibility
verdict.** It changes one *explanation*, tightens one gate's ordering, and binds arm B.

---

## A1. RETRACTED: "headroom collapses when the label composition becomes lopsided"

### What was claimed

`WATER_PREREG.md` §5.3 stated, of the corrected P7:

> *"The headroom collapses when the label composition becomes lopsided (`p₁ = 0.091` there) — the
> **same mechanism, at the same end of the path, as the ceiling collapse in §5.4**. Absolute
> headroom is therefore not a property of the template; it is a property of the state point, and
> the two gates fire together."*

### What refutes it

The glass campaign measured, over 44 of its own `(T, template)` cells,
`corr(log min(p_B, 1−p_B), log headroom) = +0.209` — weak, and the wrong sign for lopsidedness
driving collapse — with a decisive counter-example: a **balanced** marginal (`p_B = 0.46–0.51` at
`r = 0.89`) collapsing headroom to `0.0002–0.0030`, while a **very lopsided** one
(`p_B = 0.023–0.026` at `r = 1.07`) held `0.0044–0.0051`. Its diagnosis is **near-emptiness of a
cell**, from geometry × species exclusion.

**I then ran the same test on my own stage-0 data, and it refutes me more sharply than theirs
does** (`n = 20` cells, four synthetic runs):

| correlation | value |
|---|---|
| `corr(log lopsidedness, log headroom)` | **−0.099** |
| `corr(log min-cell FRACTION, log headroom)` | **+0.863** |
| `corr(log product-model min-cell, log headroom)` | +0.849 |
| `corr(log lopsidedness, log ceil_min)` | +0.168 |
| `corr(log min-cell FRACTION, log ceil_min)` | +0.623 |

**And the falsifying pair was inside the very run I drew the claim from.** In the LDL proxy, at
one composition (`p₁ = 0.091`), two templates:

| template | `p₁` | min-cell fraction | headroom |
|---|---|---|---|
| `tetrahedral` | 0.091 | `1.08 × 10⁻³` | **0.0222** |
| `equilateral_nn` | 0.091 | `5.00 × 10⁻²` | **0.6555** |

**Same composition, a 30 × difference in headroom.** Composition cannot be the driver, and I had
both numbers on screen when I wrote the claim — I read the collapse off the two lopsided cells I
was looking at and never checked the third, which contradicts them. This is a `GATES.md` reach-8
failure in miniature: the diagnosis was fixed by which cells I happened to be reading.

### What replaces it — and it is better than either campaign had alone

> **Cell starvation is the PROXIMATE driver of both the headroom collapse and the ceiling
> collapse. Composition is one route to starvation and geometry is another, and they are
> separable:**
>
> * **at fixed composition, geometry dominates** — within one of my runs (`p₁` constant at 0.499)
>   the ceiling ranges `0.0005 → 0.0693` nats, a **140 ×** swing driven by template alone. This is
>   glass's regime, and its excluded-volume diagnosis is correct for it;
> * **at fixed geometry, composition dominates** — at the tetrahedral template the ceiling runs
>   `0.0004` (`p₁ = 0.091`) to `0.1212` (`p₁ = 0.595`), because a rare label drives the
>   product-model minimum cell (`p₁³`) toward zero and starves the table that way.
>
> **My stage-0 design varies both at once and therefore could not separate them; I attributed the
> whole effect to the one I had in mind.** Glass's ladder varies mostly geometry and isolates
> that route cleanly. Both routes are real, both end at the same gate.

### The operational change

Glass's extension is adopted verbatim and it is symmetric:

> **A wide headroom on a starved table is not a pass, AND a narrow headroom on a starved table is
> not a fouling. Occupancy is gated FIRST, in both directions, and a headroom reading on a cell
> that failed G-OCC is not reported as a gate discharge at all.**

`WATER_PREREG.md` §3 point 3 already required G-OCC before G-LP, but only for the *wide* case.
**It is now required in both directions.** P7's numeric form (headroom ≥ 30 × the measured share)
and the VOID threshold (3 ×) are **unchanged** — they were stated as a ratio precisely so they
would not depend on this mechanism, and they do not.

**What survives untouched:** every gate rule in §5.3 and §5.4. Only the causal story was wrong.
That distinction is the point of writing this down rather than editing the prereg: **the gates
were right for a reason I got wrong**, which is a weaker position than it looked and is now on
the record as such.

---

## A2. CONFIRMED, and worse than measured: the ThirdCap ceiling is not constant along a sweep

Glass confirmed the ceiling finding on real data (`glass_ceiling.py`), with its template fully
symmetrised so all three orientations coincide and the minimum is unambiguous:

* sharp ceiling **0.001 × to 0.339 × of `ln 2`** — tighter than my synthetic `0.0006–0.175 ×`;
* **and it moves along the temperature ladder**: `× 2.0` at `r = 1.30` (0.115 → 0.235 nats),
  **`× 7.2`** at `r = 1.50` (0.0010 → 0.0072).

**The consequence on its own headline is exactly the failure `WATER_PREREG.md` §5.4 was written
to catch, now demonstrated on real data rather than on my proxies:** at `r = 1.30` the share
grows `× 2.41` against `ln 2` and is **flat** against the sharp ceiling (1.95 %, 2.15 %, 2.00 %,
2.31 % — a span of 1.18). The growth of the raw reading is the growth of its own ceiling.

**Two things follow for this campaign.**

**(i) A correction to my own language.** `WATER_PREREG.md` §5.4 and §6(3) call the ThirdCap
minimum *"the honest data-computable denominator"*, which reads as though it were strictly
better. Glass's caveat is correct and is adopted: **`I(pair ; third)` is not a pair-only
quantity**, so *"the ceiling grew"* is **not** the statement *"the pair correlations grew"*. The
two normalisations answer **genuinely different questions**, and neither is the honest one.
**Both are reported and neither is elected**, exactly as glass did.

**(ii) My comparability rule is stricter than what glass applied, and that is a live
disagreement.** §5.4 fixed: *"no ceiling fraction is compared across cells whose ceilings differ
by more than 3 ×."* Applied to glass's ladder that rule **permits** the `r = 1.30` comparison
(`× 2.0`, where it found flat) and **VOIDs** the `r = 1.50` one (`× 7.2`, where it reports the
trend surviving attenuated from `× 43.5` to `× 5.9`). I am not asserting glass's `r = 1.50`
reading is wrong — my 3 × threshold was fixed on synthetic proxies and has no dye test — but the
two documents currently give different verdicts on the same cell, and that should be adjudicated
against a case with a known answer rather than left standing. Flagged to glass.

---

## A3. BINDING ON ARM B — the conditions glass attached, and a defect it disclosed

Arm B (the Kob–Andersen pair-potential baseline, `WATER_PREREG.md` §4.3 P6) is **approved by the
glass campaign**, whose data and instrument it uses. Three conditions, all adopted:

1. **Read `glass/compact/*.npz`, never the tarballs** — those were purged to survive a 99 %-full
   disk. The compact files carry `positions`, `inherent`, `types` only; the dynamical
   propensities and ML predictions are discarded at ingestion. **For a deflation control that is a
   feature, not a limitation** — a static-order baseline must not have a dynamical label anywhere
   near its estimator.
2. **Take the count-matched cap `--cap 1300`.** Glass's raw triple counts **rise with
   temperature** (1330 → 1715 per configuration at `r = 1.30`) — *the same direction a floor
   artifact would take*. Without the cap, arm B's interior-peak test could read a count effect.
   This is `WATER_PREREG.md` §5.5 G-DOSE, instantiated with a specific number, and the number is
   now fixed in advance.
3. **Seed the surrogate's RNG before using it.** `glass_surrogate.py` **does not seed its cupy
   RNG**; two runs with identical arguments give different draws. This already cost glass a real
   correction — two paired-surrogate processes started ninety seconds apart wrote the same log and
   JSON, and a draft quoted the loser; the corrected numbers flipped a headline. `glass_run.py`'s
   per-state-point seed is a stable CRC, but **the surrogate's Monte Carlo stream is not fixed.**

   **This is a G-REPRO defect (`GATES.md` reach: gate-log provenance, the phi4 log at `5e3df2f`),
   and `WATER_PREREG.md` §5.5's G-REPRO clause now names it specifically:** any inherited
   component of the N3 pair-matched null must have its RNG seeded and the seed recorded, and
   **two runs with identical arguments must be compared before any of its output is trusted.**
   `glass_share.py` and `glass_gate.py` — the two components §11 inherits byte-identically — are
   unaffected: the estimator, the enumerator and the headroom LP are deterministic.

---

## A4. A CROSS-LABEL ADVANCE PREDICTION, staked by glass before arm B runs

Glass staked this **before seeing any coordination-label reading**, which makes it a genuine
advance prediction under `epistemology.md` rule 6 rather than a post-hoc comparison:

> On its ladder the **species** reading is **monotone in `T` at both clean templates, with no
> interior peak**; the two capped templates that looked non-monotone were **void on cap noise**
> (1.6–13.9 × their null) rather than genuinely structured.

**Adopted as P8, and its polarity declared now (G-POL):**

> **P8.** Arm B's **coordination-number** label on the **same Kob–Andersen configurations** also
> reads **monotone in `T`, with no interior peak**, at the same clean templates. A **PASS** is
> agreement with glass's species reading in both monotonicity and sign.
>
> **If arm B shows an interior peak on Kob–Andersen, that is a real disagreement between two
> labels on byte-identical configurations, and it is chased rather than explained away.** It
> would mean either (a) the coordination label reads a sector the species label is blind to —
> which would be a finding about the *instrument*, not about water — or (b) one of the two labels
> is manufacturing structure, in which case arm B's own N2 ideal-gas control must show it. Either
> way it must be resolved **before** arm B is used to deflate anything about water, because P6's
> whole job is to establish that a pair-potential liquid shows no peak.

This is the strongest thing in this amendment: it makes arm B a test of *the labels against each
other* on identical data, with both sides staked in advance.

---

## A5. WHAT DID NOT CHANGE

* **P1–P7**, and P1's double-peak stake, stand exactly as frozen.
* **Every kill (K1–K4, K-VOID, K-PIN, K-MINT, K-DOSE, K-CEIL, K-DYE)** stands.
* **The feasibility verdict stands**: the LLCP is out of reach on this box by two to four orders
  of magnitude in wall time; arms C, D and E remain unrun and arm E remains declared out of reach.
* **The floor law, the template exclusions and the design sensitivity** (`3 × 10⁻⁵` nats,
  `N = 4000`, 200 independent configurations) stand — none of them depended on the retracted
  mechanism.
* **Scope**: simulated water models only; nothing bears on `wild-share`; `Stance.lean` untouched;
  no Lean file opened; `lake` not run; nothing pushed.

---

## A6. FILES

| | |
|---|---|
| `water_amend1_headroom.py` | the test that refuted A1's claim, on the four stage-0 JSONs |
| `water_amend1_headroom.txt` | its output, including the `n = 20` correlation table quoted above |

Primary seed **20260727**.
