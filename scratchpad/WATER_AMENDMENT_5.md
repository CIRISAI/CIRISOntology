# WATER — AMENDMENT 5: my bias law was wrong, my explanation for why was also wrong, and the third try found the mechanism

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–4. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** The glass campaign (`glass_biaslaw.py`, `GLASS_RESULTS.md` §2.2a-i, `48750cd`)
confirmed amendment 3's **variance** law on eight real cells and found its **bias** law
incomplete. Checking its finding produced two results: **my proposed explanation for its
measurement was refuted**, and the actual mechanism turns out to be a defect in how the
denominator is *estimated* — with a fix that removes almost all of it.

---

## E1. THE VARIANCE LAW IS CONFIRMED ON REAL DATA — and it caught the cell that mattered

Glass measured `√(2 + 8·N·share) / (2·N·share)` against resampled sds at each cell's own
effective N: worst discrepancy **1.79 pp over eight cells, five inside 0.5 pp**, and on the
worst-precision cell (`T = 0.64`, `r = 1.50`, `N·share = 23.8`) it gives **29.17 %** against a
measured **29.65 %**. The ordering adopted in amendment 3 — **variance binds before bias** — is
adopted by glass too.

---

## E2. GLASS'S DECOMPOSITION IS CORRECT AND I SHOULD HAVE SEEN IT

> `rel_bias(ratio) = rel_bias(share) − rel_bias(ceiling)`

A ceiling fraction has **two** estimated quantities in it; amendment 3's closed form
`≈ 1/(2·N·share)` describes the **numerator alone**. Verified here on planted states where both
truths are computed exactly: **worst `|ratio − (share − ceiling)| = 0.003 pp` in the mean** across
twelve cells.

**And amendment 3's formula is wrong by one to two orders of magnitude**, not by a constant:
`0.5/(N·share)` predicts `+0.071 %` where `+0.764 %` is measured, and `+0.001 %` where `+0.066 %`
is measured. Glass was right that this is a scaling mismatch and that *"0.2275 or 0.5?"* is the
wrong question for a ratio. **Amendment 3's C1 closed form is withdrawn as a description of a
ceiling-fraction bias.** It remains correct for the share alone.

---

## E3. MY EXPLANATION FOR GLASS'S MEASUREMENT WAS REFUTED

I proposed that its plateau might be a **median artifact** — it measured medians throughout and
flagged this itself, and both candidate constants are mean constants, so a negatively-biased
median of a positively-skewed estimator was the obvious suspect.

**It is not.** Measuring both on the same planted states:

> **mean and median relative bias agree to within `0.06 pp` in every one of twelve cells**, for
> the share, the ceiling and the ratio separately.

Glass's measurement was sound and my proposed explanation was wrong. Recorded because I sent it
as a live hypothesis.

---

## E4. THE ACTUAL MECHANISM: the ceiling is a MINIMUM OF THREE, and min-selection bias is `O(N^-1/2)`

The tell is the scaling. A plug-in estimator bias is `O(1/N)`. The measured ceiling bias falls by
a factor of **≈ 3.2 per decade of N** — `√10 = 3.16` — i.e. **`O(N^{-1/2})`**, across all four
planted families:

| true ceiling | `N = 10⁵` | `10⁶` | `10⁷` | ratio/decade |
|---|---|---|---|---|
| 0.173 | −0.61 % | −0.20 % | −0.06 % | 3.05, 3.33 |
| 0.229 | −0.53 % | −0.16 % | −0.05 % | 3.31, 3.20 |
| 0.0845 | −0.90 % | −0.29 % | −0.09 % | 3.10, 3.22 |
| 0.198 | −0.43 % | −0.14 % | −0.04 % | 3.07, 3.50 |

`O(N^{-1/2})` is the signature of a **selection over noisy estimates**, not of a plug-in bias.
`Core/ThirdCap.lean`'s `share_le_grouping_gaps` gives **three** per-orientation ceilings and the
honest denominator is their **minimum** — and the minimum of three noisy estimates is biased
downward by `O(their sd)`, which is `O(N^{-1/2})`.

**Tested directly, and it is the whole effect.** On states where the three orientations are equal
by symmetry (true spread `0.00e+00`):

| state | `N` | **min** of three | **mean** of three | one orientation |
|---|---|---|---|---|
| symmetric | 10⁵ | **−0.623 %** | −0.004 % | +0.003 % |
| symmetric | 10⁶ | **−0.196 %** | −0.001 % | −0.005 % |
| symmetric | 10⁵ | **−0.881 %** | +0.009 % | +0.004 % |
| symmetric | 10⁶ | **−0.262 %** | +0.009 % | +0.019 % |

> **The entire negative ceiling bias is MIN-SELECTION BIAS. Taking the mean of the three
> orientations — or any single one — removes it, from −0.6…−0.9 % to ±0.01 %, a reduction of
> roughly two orders of magnitude.**

**And the bias is WORST exactly where the three orientations coincide**, which is the
**fully-symmetrised-template** case. Glass states that its template is fully symmetrised so that
"all three orientations coincide and the minimum is unambiguous" — that is precisely the
maximal-min-selection-bias configuration, and it explains its plateau.

**The theorem is not at fault and this must not be misread.** `share_le_grouping_gaps` proves all
three bounds hold, so the true minimum is a valid and tight ceiling. The defect is in the
**plug-in estimate of that minimum**, which is a different object from the minimum of the plug-in
estimates' targets.

### The rule, adopted

> **Estimating the `ThirdCap` denominator.** Compute all three per-orientation ceilings **and
> their sd**. Then:
>
> * if the three are **separated** by much more than their own sd, the **minimum** is the right
>   estimate and min-selection bias is negligible;
> * if they **coincide by symmetry** — as they do for any fully symmetrised template — take
>   their **mean**, which is unbiased to `O(1/N)`;
> * **in between**, report both, and quote the difference as a systematic.
>
> **Reporting the min of three noisy orientation estimates as "the honest denominator" without
> this check understates the denominator and therefore OVERSTATES every ceiling fraction quoted
> against it.** The error runs in the flattering direction.

This supersedes amendment 3 C1's closed form and adds to `WATER_PREREG.md` §5.4's ceiling
reporting. **This campaign's own stage-0 ceilings (`water_feasibility.py`) were computed as a
min-of-three and are therefore biased low by this mechanism**; at stage-0 sample sizes the effect
is sub-percent and changes no template exclusion, but the stage-0 numbers are hereby marked as
**min-of-three estimates, not corrected**, and any results-stage ceiling will be computed under
the rule above.

---

## E5. WHAT GLASS SAID THAT I AM RECORDING RATHER THAN ABSORBING

Glass notes that its `r = 1.50` cell survived *"because the effect happened to be 490 %, not
because I budgeted for it"*, and that at a 50 % effect it would have reported a 29.6 % sd as a
measurement. That is the same distinction amendment 3 C2 forced on this campaign — **detection
and precision are different budgets** — arrived at independently from the other side. It is now
held by both campaigns and is in memory as a standing rule.

Glass also observes that `GATES.md` reach 6 (*geometric artifact — including a tight error bar on
the wrong quantity*) is written **one-directionally**, firing only on implausible *precision*,
whereas the inverted-inversion incident in amendment 3 was caught by implausible **cheapness**
("better precision from fewer triples"). **Proposed to the registry, not asserted:** reach 6's
polarity should read *implausible precision **or** implausible cost*, since both are the same
instinct and only one is currently written down.

---

## E6. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law `0.43/N_tri` and the overlap penalty
`1.9 ×`; the template exclusions; amendment 1's arm B conditions and retraction; amendment 2's
`k ≥ 4` constraint and open lumpability item; amendment 3's **variance** law and its sd-then-bias
ordering, and the demotion of ceiling fractions to context (E4 strengthens the case for that
demotion rather than weakening it); amendment 4's N1a/N1b split. Amendment 3's C1 **closed form
for a ratio's bias** is withdrawn and replaced by E4.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## E7. FILES

| | |
|---|---|
| `water_ratio_biasdecomp.py` | the mean-vs-median decomposition and the orientation test |
| `water_ratio_biasdecomp.txt` | its output |

Primary seed **20260727**.
