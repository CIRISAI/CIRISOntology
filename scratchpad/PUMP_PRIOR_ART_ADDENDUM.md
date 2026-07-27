# PUMP prior art — ADDENDUM from an independent second sweep

**Status.** `PUMP_PRIOR_ART.md` (committed `8125797`) stands. This document does not replace it and
does not repeat it. It records what a **second, independently-run** object-directed sweep found that
the first did not — including **one finding that falsifies a sentence of the parent's L4 verdict**,
and one that changes how `PUMP_RESULTS.md` is allowed to word its headline.

**Why a second sweep at all.** House rule `second-guess-subagent-results`, and the standing memory
`eca-spike-is-convergent-art`, whose one-line form is: *read the defining paper's figures before
claiming a first.* That memory was written about the paper in §A1 below, and the first sweep did not
open its figures.

Search date 2026-07-27. Two primaries pulled to local text and quoted from their own text layer
(`physics/0307072`, `0806.2552`); everything else from abstracts and indexed full text, marked where
it matters. **The parent document's sources (Galla–Gühne, Girolami et al., Streltsov et al.) were not
re-verified here** — this addendum is additive and its own citations are the ones it vouches for.

---

## A1. THE PUMP CURVE IS PUBLISHED — Schneidman et al. 2003, Figure 2

**This amends the parent's L4.** The parent writes:

> "Searched for, and not found: any expression, **curve**, fit, or scaling for how much whole-only
> share … a local stochastic channel creates, as a function of the channel's parameters."

A curve exists, it is twenty-three years old, and it is in **the paper that defines our measure** —
already cited in `Core/Share.lean` and in the parent's own credit paragraph, but for the quantity
rather than for the phenomenon.

**E. Schneidman, S. Still, M. J. Berry II, W. Bialek**, *"Network information and connected
correlations"*, **PRL 91, 238701 (2003)**, arXiv:physics/0307072.

Their Eq. (6) is our `share`: `I_C^(k) = S[P̃^(k−1)] − S[P̃^(k)]`, `P̃^(k)` the maxent distribution
matching all `k`-th order marginals. Their **Fig. 1** tabulates AND and OR at `I_C^(3) = 0`,
`I_C^(2) = 0.8113` bits — **pure pair structure, zero whole-only share**, the same starting condition
as `ferro`. Their **Fig. 2 caption**, verbatim from the PDF text layer:

> "Correlated–information of orders 2 and 3 and the multi–information for 3 variables whose joint
> probability distribution is given by noisy logical functions. Each panel presents the `I_C`'s and
> `I` values for a noisy version of one boolean gate (XOR in first row, OR in second, AND in third),
> **as a function of noise amplitude**. The three types of noise are **output noise** (probability of
> flipping σ₃), **input noise** (probability of flipping σ₁) and **input-dependent output noise**
> (probability of flipping σ₃, given that σ₁ = 1 and σ₂ = 1)."

Nine panels, each sweeping a per-cell flip probability across `[0, 0.5]`. And the body text:

> "When we add noise either to the input or output of the boolean functions (Fig. 2) we degrade the
> correlations, but more interestingly we find that **pure 2-body interactions such as AND and OR
> show a 3-body interaction component for some types of noise** (even for noise sources which are
> state dependent). … For these three functions, **input noise only changes the strength of the
> existing interactions, rather than introducing a new kind of effective interaction.**"

### What this costs, precisely

| the parent's claim | after this |
|---|---|
| L1 (creation) **SCOOPED**, "from 2009" | **SCOOPED from 2003**, and by a paper we already cite. Zhou 2009 and Galla–Gühne 2012 are the *theorems*; Schneidman 2003 is the *measurement*, six years earlier |
| L4: no **curve** of the created share against a channel parameter exists | **false as written.** A nine-panel curve exists |
| L4 **CLEAR** | **survives, narrowed.** What is genuinely absent is below |

### What is still absent, checked line by line against the full text

| leg | in Schneidman 2003? |
|---|---|
| `I_C^(3)` vs a per-cell noise parameter, plotted | **YES** — Fig. 2, nine panels |
| an explicit **asymmetry** parameter separating `a = p01 − p10` from strength `s` | no — one flip probability per panel |
| a fitted **exponent**, coefficient, or small-parameter expansion | no — no fit, no number quoted off the curves |
| **saturation** value or time constant; iterated application | no — a single application |
| a **theorem** pinning a zero of the pump | no |
| **k-scaling** | no — `k = 3` throughout |
| never-from-nothing / never-downward as statements | no |
| **cross-substrate** check | no |

So the campaign's deliverable survives and is now sharper: **not "a curve exists", which is 2003, but
the asymmetry-resolved law — exponent, coefficient, pinned zero, `k`-scaling, hardware overlay.**
`PUMP_PREREG.md` and `PUMP_RESULTS.md` must be written to that scope and must not describe the bare
existence of a noise-vs-share curve as a new observation.

### One reading we could not extract — and it becomes an instrument gate, not a claim

The text layer gives the caption and the sentence but **not the plotted values**, so *which* of the
three noise columns creates order-3 on AND is a figure reading we do not have. "Input noise only
changes the strength" excludes the input column; the parenthetical "even for noise sources which are
state dependent" implies the plain output column is the base case. **That is an inference, not a
quotation, and it is marked as one.**

**Therefore, for `PUMP_PREREG.md`: reproducing Schneidman Fig. 2 is a pre-registered instrument
validation gate.** Nine panels, exactly computable on eight cells, a free calibration against a
published figure. If our reproduction disagrees with the published panels, the instrument is wrong
before any pump curve is believed. This is the cheapest gauge gate available to the campaign and it
was not in the plan.

---

## A2. "THE PUMP IS ASYMMETRY" IS ABOUT A **PAIR** — and Schneidman is the published instance

The parent's L3 has the logical point already:

> "our statement carries a hypothesis theirs does not: the input must be **sign-symmetric**. Drop
> that and the theorem is false — a unital kernel on a non-sign-symmetric pair-correlated state can
> move the share."

Correct, and now it has a **published measured instance** rather than being a caveat: Schneidman's
AND and OR panels are exactly that case. Flipping σ₃ with a fixed probability is the **binary
symmetric channel**, which is flip-covariant, hence **unital**; and AND is not sign-symmetric, since
`AND(0,0) = 0 ≠ 1 = AND(1,1)`. A unital per-cell channel on an asymmetric pair-structured state,
minting order-3, measured in 2003.

The honest general statement:

> The whole-only share is created only when the **composite** (input state, channel) fails to be
> invariant under a symmetry that forces the share to zero. Sign-symmetry is one such symmetry
> (`share_eq_zero_of_signSymmetric`). The asymmetry may be supplied by the **channel** (`damp` on
> `ferro`) **or by the state** (a BSC on AND). Either suffices, and they are independent axes.

**What this costs `PUMP_PREREG.md`, and it is design-level:**

1. The `a = 0` line is a **theorem-pinned null only on sign-symmetric inputs**. On `ferro` it is a
   valid zero-control and must verify to estimator precision. On any input that is not
   sign-symmetric it is **not** a null and must not be used as one. The prereg's pair-strength
   family must therefore be built **within** the sign-symmetric family, or the control silently
   stops being a control halfway along the second axis.
2. There are **two** pump mechanisms. A curve swept only in channel asymmetry measures one. The
   prereg must either add the state-asymmetry axis or state plainly that the state-asymmetry
   mechanism (Schneidman's) is published and out of scope.
3. The mission's downstream unification — one law behind the Planck valve floor, the sky shot-noise
   minting, the glass and water coarse-graining floors, and the QPU bulge — **cannot be claimed from
   a channel-asymmetry curve alone.** At least the coarse-graining floors are state-asymmetry-driven,
   and at least one of them is alphabet-reducing, which no theorem in `Core/Valve.lean` covers (§A4).

---

## A3. THE EXPONENT IS TEXTBOOK — the single most important wording constraint on the results

Not addressed in the parent, and it governs how the headline may be phrased.

**Amari & Nagaoka**, *Methods of Information Geometry*, AMS (2000); **Amari**, IEEE TIT 47:1701
(2001). The standing fact:

> A KL divergence from a point to an exponential family is **locally quadratic** in the displacement,
> with the Fisher metric as its Hessian.

Our `share` is a KL divergence from the pairwise family in exactly that geometry. So the mission's
leading hypothesis — *"minting is QUADRATIC in the asymmetry at small `a`, because the `a = 0` line
is a minimum by the theorem and smooth functions with a zero minimum start quadratically"* — is
sound reasoning **and is also precisely what information geometry already requires**, whenever the
state's displacement from the pairwise family is analytic and linear in `a`.

| measured exponent | what it means |
|---|---|
| **2** | the expected answer. Confirms a standard expansion. **A calibration of the instrument, not a discovery**, and must be reported as one |
| **1** | the displacement from the pairwise family is not differentiable at `a = 0`, or `a = 0` is not an interior minimum. A real finding, and it would need a mechanism |
| **4** | the linear-in-`a` displacement lies **inside** the pairwise family — the first-order term is pair-visible and only the second order is pair-blind. A structural statement about which direction the channel pushes relative to the parity character `χ`, and genuinely interesting |
| non-integer, or **state-dependent** | the unification fails. This is the mission's own stated negative outcome and is equally a result |

**Consequence, stated as a rule for `PUMP_RESULTS.md`:** an exponent of 2 may **not** be reported as
"the pump law". It must be reported as *"the pump obeys the expansion information geometry requires,
with coefficient `C(pair strength, k)` measured to be …"* — and **the coefficient, not the exponent,
is the deliverable**, because the coefficient is the number the sibling campaigns need to turn four
separately-measured nuisance floors into one law. Pre-register that wording now, before the number
is seen.

**Related, and it closes a hole rather than opening one:** information monotonicity under Markov maps
(Čencov) constrains the **total** divergence, not the individual `I^(k)`. That is the formal reason
the classical data-processing literature never forbade the pump, and it is why no DPI paper is a
scoop.

---

## A4. THE THRESHOLD / DICHOTOMIZED-GAUSSIAN FAMILY — it lands on `Core/Valve.lean`'s OPEN boundary

Not in the parent, not in the mission brief, and it is the second most consequential hit.

- **S. Amari, H. Nakahara, S. Wu, Y. Sakai**, *"Synchronous firing and higher-order interactions in
  neuron pool"*, **Neural Computation 15, 127 (2003)**.
- **J. H. Macke, M. Opper, M. Bethge**, *"Common input explains higher-order correlations and entropy
  in a simple model of neural population activity"*, **PRL 106, 208102 (2011)**, arXiv:1009.2855.

**The mechanism.** A multivariate Gaussian carrying **only pairwise structure** is pushed through a
**per-cell threshold**, `y_i = 1` iff `u_i > θ`. The output carries **higher-order correlations**.
The field's own statement: the DG inputs "have no interactions beyond the second order in their
inputs; however, they can induce higher-order correlations in the outputs", and "small changes in
second-order correlations can lead to large changes in higher correlations."

**Why this matters here.** A per-cell threshold is a per-cell **alphabet-reducing** map — continuous
in, binary out. `Core/Valve.lean`'s BOUNDARY note (lines 96–114) says exactly this case is **not
covered** by `percell_no_creation` or by any valve theorem, and calls whether per-cell
coarse-graining can create whole-only share **"open here"**, naming the κ-edge work as the live
adjudication. **The neuroscience literature has been answering the empirical version since 2003, and
its answer is yes.** That does not close the Lean question — a threshold is deterministic and
alphabet-reducing, the theorems are stochastic and same-alphabet — but it means the question is open
*in this repository*, not in the world, and no prereg, results document or stance text may present it
as open in the world.

**And the asymmetry axis reappears, on the state side.** In the DG model the created higher-order
structure depends on the **threshold**, equivalently on the mean rate. At the symmetric point (a
zero-mean Gaussian thresholded at its median) the output is invariant under the global flip, so by
`share_eq_zero_of_signSymmetric` its whole-only share is **exactly zero**. The DG literature's
"higher-order correlations grow as you move off `p = ½`" is therefore **the same asymmetry law this
campaign proposes to measure, on the state axis, in a different substrate.**

*Marked honestly:* the qualitative DG claim is not in doubt and is quoted from the field's standard
statement of the model. The **vanishing at `p = ½`** is my own symmetry argument applied to their
model, not a quotation from either primary — neither primary was opened. If the campaign leans on
it, open Macke 2011 first.

---

## A5. THE CLOSEST RECENT WORK — and it lacks our gates

**P. Orio, P. A. M. Mediano, F. E. Rosas**, *"Dynamical noise can enhance high-order statistical
structure in complex systems"*, **arXiv:2305.13454** (2023). Not in the parent, which reaches a
different 2026 paper on environment-driven emergence.

Elementary cellular automata; **dynamical noise** as the probability `P_n` of flipping an agent's
state in violation of the rule — a **symmetric** per-cell bit flip swept from 0 to ½; O-information
`Ω = TC − DTC` and S-information `Σ = TC + DTC` measured against `P_n`. Finding: high-order
interdependencies are not merely robust to noise but can be **enhanced** by it, with a **biphasic**
response — structure rising at intermediate noise before decaying.

**CONVERGENT-ADJACENT, and the closest work of the last five years.** Same qualitative claim, same
substrate family as our own ECA episode, swept noise parameter, interior peak. What leaves our
question open: the measure is **O-information**, not the maxent gap (`share-is-not-negentropy`
records how badly adjacent measures diverge from ours); the noise is **symmetric only**, no asymmetry
axis, no vanishing condition; **no fitted form, exponent or scaling law**; and — the point our own
battery insists on — an **interior peak in a swept noise parameter reported without a mixture null or
a dose-vs-rate control**, which is the exact failure mode that killed our own ECA spike
(`eca-pairwise-blind-spike`; GATES.md §3's kept taint at `9630d81`, a 1886× collapse under a mixture
null). We may not point at that gap unless our own peak passes both gates. The prereg requires them.

---

## A6. KAHLE — three things wrong in `Core/Valve.lean`'s credit, and the fix makes it stronger

The parent quotes the right sentence and names the right correction (cite Zhou 2009 and Galla–Gühne
alongside). It does not say what is actually **wrong** with the sentence in the Lean.
`Core/Valve.lean` lines 130–136:

> "That mixing a state with per-cell noise can CREATE higher-order interaction — the mechanism
> `valve_upward` exhibits — is known: Kahle, Olbrich, Jost and Ay … **study exactly which interaction
> orders a mixture can raise**."

| | |
|---|---|
| "study exactly which interaction orders a mixture can raise" | their own text calls it **"the more general and unsolved problem"** |
| "mixing a state with **per-cell noise**" | their mixture is of **two dynamical phases**. Verified against the full text: their systems are coupled tent maps and cellular automata, **deterministic**; the only randomness is the initial condition. No channel, no noise model, anywhere in the paper |
| the citation sits in the wrong place | the correct citation for *per-cell-noise-creates-order-3* is **Schneidman et al. 2003, Fig. 2** — cited two sentences earlier for the measure, uncredited for the phenomenon |

**And a bonus worth one line in the prereg.** Kahle's `I^(3)` peak at the synchronisation onset is,
by their own diagnosis, **a mixture of two metastable phases** — precisely the artifact
`broken-phase-metastability-artifact` records from our own φ⁴ campaign (a frozen two-phase mixture
reading 300× the real ridge, invisible to `τ_int` and `U₄`). They found the peak, separated the
phases by hand, and reported that the peak *was* the mixing. That makes Kahle et al. **the standing
cautionary precedent for our own mixture-null gate on any interior peak** — a role at least as useful
as the credit they were given, and one they actually earn.

---

## A7. STOCHASTIC THERMODYNAMICS — the parent's flagged incomplete search, partially closed

The parent flags this literature as "an incomplete search, not an all-clear", correctly. One line of
it is now swept, and it does not reach us:

- **J. Karbowski**, *"Bounds on the rates of statistical divergences and mutual information via
  stochastic thermodynamics"*, **Phys. Rev. E 109, 054126 (2024)**, arXiv:2308.05597 — upper bounds
  on the **time-derivatives** of f-divergences and of mutual information, in terms of temporal Fisher
  information and entropy production. A genuine rate law for correlation change. Objects:
  f-divergences and **pairwise** mutual information. **Higher-order / connected information does not
  appear.**
- **K. Ptaszyński & M. Esposito**, *"Dissipation enables robust extensive scaling of multipartite
  correlations"*, arXiv:2410.13375 — multipartite, and about **scaling with system size**, the
  nearest neighbour to our `k`-scaling leg. Quantity is **mutual information**; result is about
  extensivity at fixed points versus limit cycles, not creation by a local channel.

**Status: still CLEAR at order 3.** The rate-bound line is swept; the wider literature is not, and
the parent's warning stands. If our measured coefficient turns out bounded by an
entropy-production-like quantity, Karbowski's bound is the frame to state it in, and the honest
description would be "the order-3 analogue of a bound published for order 2".

**Adjacent, for the `k`-scaling leg specifically:** **Olbrich, Bertschinger, Ay & Jost**, *"How
should complexity scale with system size?"*, **Eur. Phys. J. B 63, 407 (2008)** — on excess entropy
and neural complexity rather than `I_C^(3)`, so not prior art on our scaling, but it is the paper a
referee would name.

---

## A8. VOCABULARY BRIDGE — so an information theorist can find us, and one fact about where our two data points sit

The parent's L3 supplies the right bridge on the symmetry side: flip-covariant = binary symmetric
channel = **unital** binary channel. The complementary bridge, for the asymmetry axis:

Our family — flip probabilities `(p01, p10)`, asymmetry `a = p01 − p10`, strength
`s = (p01 + p10)/2` — is the **binary asymmetric channel (BAC)**. The `a = 0` line is the **BSC**.
The edge `p01 = 0` is the **Z-channel**.

**And the fact that follows, which belongs in the prereg.** `Core/Valve.lean`'s `damp` is
`K y x = if x then 1/2 else if y then 0 else 1` — true→false with probability ½, false→true with
probability 0. That is exactly the **Z-channel at crossover ½**: `p01 = 0`, `p10 = ½`, hence
`a = −½`, `s = ¼`. At `s = ¼` the largest attainable `|a|` is ½. So **`damp` sits on the
extreme-asymmetry corner of the family at its own strength, not in the interior** — and the QPU's
amplitude-damping arm, being a Z-channel with crossover `γ(t) = 1 − e^{−t/T₁}` plus a small thermal
`p01`, sits on the same corner. **Both the theorem's witness and the only hardware point are corner
points.** A curve fitted through the interior and then extrapolated to the corner to meet the QPU is
doing an extrapolation, not an interpolation, and `PUMP_RESULTS.md` must say which it did.

---

## SUMMARY OF AMENDMENTS TO `PUMP_PRIOR_ART.md`

| parent section | amendment |
|---|---|
| L1 | **SCOOPED from 2003, not 2009** — Schneidman et al. Fig. 2 is the measurement; Zhou 2009 and Galla–Gühne 2012 are the theorems (§A1) |
| L3 | the sign-symmetry caveat has a **published measured instance** — a unital channel minting from AND, 2003. Two independent asymmetry axes, state and channel (§A2) |
| L4 | **"no curve exists" is false as written**; the verdict CLEAR survives only for the *asymmetry-resolved law with an exponent and coefficient* (§A1) |
| L4 | the exponent-2 hypothesis is **textbook information geometry**; the coefficient is the deliverable, and the wording is pre-registered here (§A3) |
| L4 | Orio–Mediano–Rosas 2023 is the closest recent work and is missing from the parent (§A5) |
| L4 | stochastic-thermodynamics rate-bound line swept via Karbowski 2024; still clear at order 3 (§A7) |
| new | the dichotomized-Gaussian family, bearing on `Core/Valve.lean`'s OPEN coarse-graining boundary (§A4) |
| credit | three specific errors in `Core/Valve.lean`'s Kahle sentence, and Kahle's better role as the mixture-artifact precedent (§A6) |

## NEW REQUIREMENTS THIS PLACES ON `PUMP_PREREG.md`

1. **Instrument gate:** reproduce Schneidman Fig. 2 (nine panels) before any pump curve is believed.
2. **Control scope:** the `a = 0` null is theorem-pinned **only on sign-symmetric inputs**; build the
   pair-strength family inside the sign-symmetric family, or the control lapses along the second axis.
3. **Wording, pre-registered:** exponent 2 is a calibration; the **coefficient** is the deliverable.
4. **Corner vs interior:** declare in advance whether the QPU comparison is an interpolation or an
   extrapolation. Both `damp` and the hardware sit on the Z-channel corner.
5. **Scope honesty:** the state-asymmetry mechanism is published (Schneidman 2003; the DG family);
   either sweep it or declare it out of scope.
6. **Mixture null and dose-vs-rate on any interior peak** — mandatory, and Kahle et al. 2009 is the
   named precedent for why.

## CORRECTIONS OWED TO `Core/Valve.lean` — named, not made

This campaign does not touch Lean and nothing here moves `Stance.lean`.

| lines | what is wrong | what it should say |
|---|---|---|
| 130–136 (CREDIT) | credits Kahle with studying "exactly which interaction orders a mixture can raise"; their text says **unsolved**, and their systems carry **no noise** | credit **Schneidman et al. 2003 Fig. 2** for the measured phenomenon and **Zhou, PRA 80, 022113 (2009)** / **Galla–Gühne, PRE 85, 046209 (2012)** for the theorems; keep Kahle for the exponential-family formulation and as the mixture-artifact precedent |
| 34–44, 710–726 | "the odd sector is fed only by asymmetry" reads as a statement about the **channel**; the hypothesis also requires a **sign-symmetric input**, and Schneidman's AND panels are the published counterexample | say the composite (state, channel) must break the symmetry, and that either factor can supply it |
| 96–114 (BOUNDARY) | "open here" is accurate as scoped but is easily misread as open in the world | keep "open here"; add that the dichotomized-Gaussian literature answers the empirical version affirmatively in a different (deterministic, alphabet-reducing) setting |

*Also recorded:* the mission brief attributes the Kahle convex-combination note to `GATES.md`.
`GATES.md` does not mention Kahle anywhere — grep returns zero hits. The only in-repo Kahle credit is
`Core/Valve.lean:131`.

## WHAT THIS SWEEP DID **NOT** DO

1. **Did not re-verify the parent's sources.** Galla–Gühne 2012, Girolami et al. 2017 and
   Streltsov et al. 2011 are taken as the first sweep reported them.
2. **Did not extract figure values from Schneidman Fig. 2** — caption and body sentence only. §A1
   converts that into a gate rather than a claim.
3. **Did not open Amari–Nakahara 2003 or Macke 2011.** §A4's qualitative claim is the field's
   standard statement; its `p = ½` vanishing is my own symmetry argument on their model, marked.
4. **Did not sweep the PID literature** (Williams–Beer, Ince, Φ-ID). `novelty-check-spike-train-maxent`
   governs the spike-train side and records ΦID was never the threat; O-information is covered in §A5.
5. **Did not close the stochastic-thermodynamics search** — one line of it, §A7.
6. **Search caps:** 13 web queries, 8 primary fetches, 2 PDFs to text. No conclusion here rests on a
   search that saturated a result cap.
