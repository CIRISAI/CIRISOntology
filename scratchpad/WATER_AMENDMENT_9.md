# WATER — AMENDMENT 9: two of my own adopted conditions were in conflict, and the fix is one line

**Written after `WATER_PREREG.md` was frozen, and after amendments 1–8. No water configuration
exists.** The pre-registration is not edited.

**Occasion.** Glass applied amendment 7's a-priori criterion to itself and measured that its
enumeration's `S₃` invariance is **exactly zero on uncapped templates and `6.2e−05 … 5.3e−04` on
capped ones** — attributing a number it had published without explanation. **That measurement puts
two conditions this campaign has already adopted into direct conflict**, and neither document
noticed.

---

## I1. THE CONFLICT

| adopted in | condition |
|---|---|
| **amendment 1 A3(2)**, binding on arm B | *"Take the count-matched cap `--cap 1300`"* — because glass's raw triple counts **rise with temperature**, the same direction a floor artifact would take |
| **amendment 7 G2** | the ceiling estimator partitions the three per-orientation ceilings into symmetry-equivalence classes fixed **a priori**, and **the a priori warrant is that the enumeration returns every triangle in all its symmetry-allowed orders** |

**The cap subsamples ORDERED triples at random, and a random subset of ordered triples does not
contain all orderings of a triangle.** So the cap destroys exactly the symmetry the class
partition depends on. **Under an ordered-triple cap, amendment 7's a priori warrant is void** —
and amendment 7 explicitly forbids recovering it by observing that two estimates are close, since
that is what min-selection manufactures.

Adopting both conditions without noticing is itself an instance of the warrant reach: each was
right, and their **conjunction** was not checked.

---

## I2. THE FIX, MEASURED — cap TRIANGLES, not ordered triples

Subsample the **unordered triangles**, then emit every symmetry-allowed ordering of each one
selected. Same count control; exchangeability preserved by construction.

Synthetic point set, `N = 900`, equilateral template (full `S₃`, ratio of ordered triples to
triangles measured at exactly **6.00**, confirming complete enumeration). Worst relative deviation
of the 8-cell table from slot-permutation invariance:

| cap | kept (ordered / triangle) | **cap ORDERED** | **cap TRIANGLES** |
|---|---|---|---|
| none | 10272 | 0.000e+00 | 0.000e+00 |
| 5136 | 5136 / 5136 | 2.966e−02 | **0.000e+00** |
| 2568 | 2568 / 2568 | 4.545e−02 | **0.000e+00** |
| 1027 | 1027 / 1026 | 6.667e−02 | **0.000e+00** |

> **Exact, at every cap, at the same kept count. The fix costs one change to how the subsample is
> drawn and nothing else.**

### Binding, and superseding amendment 1 A3(2)

> **Arm B's cap is taken on TRIANGLES, not on ordered triples.** The count control that condition
> was adopted for is unchanged — the cap still binds at every temperature and still removes the
> rising-count confound. What changes is that the sampled unit is the geometric object rather than
> one of its labellings, which is what the estimator's symmetry argument was assuming all along.
>
> **And a check, since a warrant is not a measurement:** the `S₃` deviation of every capped table
> is computed and must read **exactly zero**. A nonzero reading voids the class partition for that
> cell, which then falls back to min-of-three **with its selection bias measured and quoted**
> (amendment 5 E4), never to a blanket mean (amendment 7 G1: `+16.77 %`, non-decaying).

---

## I3. THE SAME FIX APPLIES TO GLASS, AND REMOVES ITS NUMBER AT SOURCE

Glass's `1.5e−5` "worst orientation spread" is cap-induced symmetry breaking, which it has now
diagnosed. **The triangle cap removes it rather than explaining it** — its `glass_share.py`
`triangles()` caps with `rng.choice` over the ordered list, and the same substitution would return
its capped templates to exactly zero.

**Two honest qualifications, since the magnitudes differ by three orders.** Its deviations
(`1e−4` scale) are far smaller than this test's (`1e−2`) for two reasons that both cut toward
"negligible in its case": its cap of 1300 against 1330–1715 per configuration is a **mild** cut
where this test cuts to 50/25/10 %, and it **pools over 400+ configurations**, which averages the
breaking down. So the practical effect on its published rungs is probably nil — and it says so
itself, since the two rungs it quotes are uncapped.

**But the a priori warrant is binary, not approximate.** "Exactly zero because the enumeration is
complete" and "1.5e−5 because the cap is mild" are different statements, and only the first
licenses the class partition. That is the whole content of amendment 7's criterion, applied to
the case that produced it.

---

## I4. GLASS'S OBSERVATION ON THE TETRAHEDRAL CATCH — a distinct failure, recorded

Of amendment 7's admission that stage 0 *"printed exactly that — 0.0693, 0.0693, 0.1189 — and I
read it as three numbers rather than as structure"*, glass observes that this is **not** the
warrant reach:

> **Not a wrong warrant — a right reading of a display that encoded structure the reader wasn't
> looking for. Two identical values next to a different one is a symmetry statement printed as
> data.**

That is correct and it is a different failure mode. The warrant reach fires when a justification
is wrong; this fires when **no justification was formed at all**, because the display presented a
structural fact in a format that reads as three independent measurements. Its remedy is also
different and cheaper: **print the structure, not only the values** — a ceiling table should
report its symmetry-equivalence classes as a field, computed from the template's edge lengths,
beside the three numbers.

**Adopted for this campaign's own reporting** (`water_feasibility.py`'s `thirdcap_ceilings`, to be
replaced per amendment 7 G2, will emit the class partition as a field). **Offered as an
observation, not proposed as a reach** — one instance is not a family, and it belongs to glass.

---

## I5. WHAT DID NOT CHANGE

P1–P8; every kill; the feasibility verdict; the floor law and overlap penalty; the template
exclusions; the primary label and template; amendments 1–8 entire **except** A3(2)'s cap
implementation, which I2 supersedes while preserving what it was adopted for.

Scope unchanged: simulated water models only; nothing bears on `wild-share`; `Stance.lean`
untouched; no Lean file opened; `lake` not run; nothing pushed.

## I6. FILES

| | |
|---|---|
| `water_cap_symmetry.py` | the ordered-cap vs triangle-cap `S₃` test |
| `water_cap_symmetry.txt` | its output |

Primary seed **20260727**.
