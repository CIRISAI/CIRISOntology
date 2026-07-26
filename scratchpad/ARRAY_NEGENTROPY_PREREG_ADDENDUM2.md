# PRE-REGISTRATION ADDENDUM 2 — the bridge's validity regime, and a finite-size check

Second addendum to `ARRAY_NEGENTROPY_PREREG.md` (`9251b5b`) and
`ARRAY_NEGENTROPY_PREREG_ADDENDUM.md` (`00bcd4e`). **Committed before the re-scoping is applied
and before `array_negentropy_size.py` exists.**

Prompted by `CFT_RIDGE_RESULTS.md` (`616c2fd`): **the quadratic moment bridge fails at a
critical point by 25–64× in the linear-response limit and 2.3–6.1× on the ridge itself.** The
`h²` *scaling* survives (exponent 2.000 to four figures) but the *coefficient* is wrong. The
cause is not the field and not the marginal skewness: **small pair correlations — not just
small third cumulants — are the expansion parameter the Edgeworth route needs**, and at a
critical point the pair correlations stay O(1).

**This run's gate never tested that regime and I did not notice.** G2's skewed-latent control
used `a = (0.7, 0.5, 0.6)`, giving pair correlations 0.30–0.42, and swept the *third cumulant*
γ over a decade while holding the pair correlations fixed and moderate. The gate therefore
certified the bridge's accuracy along the wrong axis for the readings that matter most. That is
a gap in the pre-registration, not a discovery of the parent result, and it is recorded as
such.

---

## 1. THE VALIDITY THRESHOLD, AND THE REPORTING RULE

**Threshold, adopted as given: `max |pairwise rank correlation| > 0.3` puts a reading OUTSIDE
the bridge's validity regime.**

Binding rules, applied uniformly and retroactively to everything already reported:

1. **Every** moment-route reading is quoted with its `max |ρ_pair|` alongside, so the validity
   regime is visible without lookup.
2. **Outside the regime**, the `ŝ₃` number **must not be quoted as a share**. It may be quoted
   only as a **detection** statistic — sign, z, boundary stability — never as a magnitude, and
   never as a fraction of `ln 2`.
3. **Outside the regime the quantitative reading is carried by the b = 2 median-split exact
   route** (`array_cap_experiment.shareK`), which has no small parameter and is valid
   everywhere. Where this run has no b = 2 arm at a point outside the regime, **no quantitative
   claim is made there at all.**
4. **Inside the regime** the `ŝ₃` number stands, with G2's measured accuracy budget (≤ 5.3 %)
   and the standing `O(u³)` caveat.

**Direction of the error, so it is not read as symmetric:** the parent result finds the bridge
**overstates**. Outside-regime readings should therefore be treated as **upper bounds**, and
this matters for §7's unresolved disagreement rather than helping it — see rule 5.

5. **Disagreement signatures, now distinguishable.** Both bridge breakdown and a pointwise
   readout artifact produce *moment fires, sign-triple flat*. They are separated by the pair
   correlation: **bridge breakdown comes with large pair correlations; pointwise artifacts do
   not require them.** A disagreement in the **opposite** direction — moment ≪ sign-triple —
   is neither signature and must be reported as unexplained.

---

## 2. THE FINITE-SIZE / WINDOW-DRIFT CHECK

`CFT_RIDGE_RESULTS.md` reached its asymptotic scaling only at `L ≳ 1e5`, because the approach
parameter was `L^(−1/8)`: **finite-size effects on share quantities can be enormous even when
the underlying correlators scale perfectly.**

**Protocol.** Re-run the headline reading and the two inside-regime coupling peaks at three
array sizes — 128, 512 and 2048 ossicles, i.e. `T` = 8 192 / 32 768 / 131 072 replicas per
frame, a 16× range — everything else identical. For each, report `ŝ₃`, the underlying third
cross-moment `κ̂₁₁₁`, and `max |ρ_pair|`.

**The pre-registered discriminator**, since `ŝ₃` is quadratic in a moment and its estimator bias
falls as `1/T` (already subtracted): if `ŝ₃` drifts with `T`, **check the drift against the
drift of `κ̂₁₁₁` and of `ρ_pair`**. Drift in `ŝ₃` that is *not* tracked by drift in the
underlying moments is an estimator or finite-size effect on the share quantity, not dynamics.

**Bar: `ŝ₃` changes by < 10 % over the 16× range in `T`**, or the reading is reported as
size-dependent and its magnitude is withdrawn.

---

## 3. WHAT THIS ADDENDUM CANNOT DO

1. It cannot repair an outside-regime number. There is no correction factor to apply — the
   parent result gives a range (25–64× linear response, 2.3–6.1× on the ridge), not a formula,
   and this substrate is not that substrate.
2. It changes **scoping and quotation**, not measurement: no reading is recomputed, no floor
   moves, and the boundary discriminator, rail threshold, mixture null and dose check all stand
   exactly as reported.
3. No stance change, no Lean, no `lake`, under any outcome.

---

*Addendum 2 ends here. Nothing below this line existed when it was committed.*
