# WATER — AMENDMENT 7: the ceiling estimator, in its general form — and my own primary template fits neither branch

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–6. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** Glass confirmed amendment 5's min-selection mechanism on its own cells (min biased
low by up to **−3.883 %**, mean unbiased to 0.2 %, worst at the smallest ceiling), corrected its
own §2.2a-i attribution to it, and supplied the **soundness argument** for the two-branch rule
that amendment 5 stated without justifying. **That argument turns out to exclude both of my own
branches for this campaign's primary template.**

---

## G1. GLASS'S SOUNDNESS ARGUMENT, adopted — and why it matters that both branches are right

Amendment 5 gave a two-branch rule and did not say why each branch was correct. Glass supplied it:

> When the true orientations **genuinely differ**, the min is the object the theorem bounds, and
> taking the mean would quote a ceiling **looser than the one proved**. When they **coincide**,
> the mean is simply the better estimator of their common value and nothing is given up. **A rule
> that always took the mean would be unsound in the first case.**

**Quantified here, and it is worse than "unsound" suggests.** On a planted state whose
orientations genuinely differ, `mean-of-three` is biased **+16.77 %, +16.76 %, +16.77 %** at
`N = 10⁵, 10⁶, 10⁷` — it **does not decay with N at all**, because it is a consistent estimator of
the wrong quantity. Min-selection bias is `−0.68 %` at `N = 10⁵` and falls as `N^{−1/2}`; a
blanket mean is a **25 × larger error that no amount of data removes.** Glass was right to flag
it and the margin is now measured.

---

## G2. AND NEITHER BRANCH FITS THIS CAMPAIGN'S PRIMARY TEMPLATE

`WATER_PREREG.md` §3's primary template is the tetrahedral triangle **`(2.80, 2.80, 4.573) Å`**.
Its apex is **distinguished**: `r₁₂ = r₁₃` but `r₂₃` differs. So the slot symmetry group is not
`S₃` and it is not trivial — it is the single transposition of slots 2 and 3. Therefore:

* orientations **(12|3)** and **(13|2)** coincide **by symmetry**;
* orientation **(23|1)** genuinely differs.

**Stage 0 measured exactly this and I did not read it as structure:**
`ceilings 12_3 = 0.0693, 13_2 = 0.0693, 23_1 = 0.1189` — the first two identical to the printed
digit, the third 72 % above them.

So the campaign's own primary template is a **2 + 1** case, and:

* **min-of-three** carries the selection bias between the two identical orientations;
* **mean-of-three** quotes a ceiling above the proved minimum — the unsoundness of G1.

### The estimator, checked on a planted 2+1 state

Planted with the same symmetry (`J₁₂ = J₁₃ ≠ J₂₃`, `h₂ = h₃ ≠ h₁`); true orientations
`0.108074, 0.108074, 0.162451`, symmetry-equivalent pair identical to `0.00e+00`, third **50 %
above**; true ceiling `0.108074`:

| `N` | min of 3 | mean of 3 | **pair-mean then min** | one orientation |
|---|---|---|---|---|
| 10⁵ | −0.678 % | **+16.769 %** | **+0.000 %** | −0.029 % |
| 10⁶ | −0.223 % | **+16.760 %** | **−0.008 %** | −0.009 % |
| 10⁷ | −0.064 % | **+16.772 %** | **+0.001 %** | −0.000 % |

### The rule, in its general form — which subsumes both of amendment 5's branches

> **Partition the three per-orientation ceilings into symmetry-equivalence classes, determined
> A PRIORI from the template's own geometry. Average within each class. Take the minimum
> ACROSS classes.**
>
> * fully symmetrised template → one class of three → **mean of three, no min** (glass's case);
> * fully scalene template → three classes of one → **min of three** (unchanged);
> * this campaign's primary template → classes `{(12|3),(13|2)}` and `{(23|1)}` →
>   **average the pair, then min against the third.**

This supersedes amendment 5's two-branch rule, which was a special case stated twice.

### The criterion, and it is the trap

> **The equivalence classes must be fixed by an A PRIORI symmetry of the template and the
> estimator — NEVER by observing that two of the three estimates are close.** Observed closeness
> is precisely what min-selection bias manufactures: three noisy estimates of one value look
> close, and so do three estimates whose truths differ by less than their sd. Reading the classes
> off the data would make the correction self-confirming.

This campaign's classes are fixed **now**, from geometry, before any water exists: for every
template `(r₁₂, r₁₃, r₂₃)` on the §3 ladder, two orientations are equivalent exactly when the
corresponding two edge lengths are equal. On the primary template that is `{(12|3),(13|2)}`; on
the equilateral and far-arm templates all three are equivalent; on any fully scalene rung none
are.

**This campaign's stage-0 ceilings were computed as min-of-three** (amendment 5 E4) and are
therefore biased low by the selection between the two identical orientations. At stage-0 sample
sizes the effect is sub-percent and no template exclusion changes, but the numbers stay marked as
min-of-three, and **`water_feasibility.py`'s `thirdcap_ceilings` will be replaced by the
class-partition estimator before any results-stage ceiling is quoted.**

---

## G3. GLASS'S OWN CORRECTION, recorded because it is the sharper instance

Glass reports that its published ceiling fractions **do not move — `+0.00 %` on all eight** —
because they are computed from the **pooled** table at full `N`, where the three orientations
agree to `1e−16`, so min and mean are the same number. The bias needs a *resampled* ceiling to
act on. Its `glass_ratiogauge.py` resamples and takes the min each time, so the mechanism bites
**inside its instrument**, not in its published numbers: at `T = 0.64, r = 1.50` a **−3.88 %**
ceiling bias contributes **+4.04 %** of that cell's measured **+6.62 %** ratio bias — most of the
plateau.

Its §2.2a-i attribution (plug-in bias of a mutual information) is therefore withdrawn in favour of
selection bias, **on the scaling evidence**: plug-in falls as `1/N`, this falls as `N^{−1/2}`.

Glass notes this as another instance for the warrant reach, and it is the cleanest one in the set:
its sentence *"the min is not doing any hidden work here"* was **true of the tables it quoted and
false as a general statement, with the justification exactly inverted** — the number was
verifiably unaffected while the warrant was backwards. **A case where the reach fires on a claim
that is numerically exactly correct** is worth more as a kept taint than any of the six where a
number was also wrong.

---

## G4. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law and overlap penalty; the template
exclusions (G2's re-estimation does not move them); amendments 1–4 and 6 entire; amendment 5's
mechanism, its `O(N^{−1/2})` scaling and its marking of stage-0 ceilings. Only amendment 5's
**two-branch rule** is superseded, by the general class-partition form.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## G5. FILES

| | |
|---|---|
| `water_orient_symmetry.py` | the 2+1 planted check and the four estimators |
| `water_orient_symmetry.txt` | its output |
| `GATE_PROPOSAL_COST.md` | the reach-6 polarity extension, filed separately at glass's request |

Primary seed **20260727**.
