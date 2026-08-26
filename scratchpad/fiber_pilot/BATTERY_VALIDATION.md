# Battery instrument — planted-truth validation (gauging, before any real data)

**The ruler works at the pilot's signal scale, and the NULL control measured the
instrument's honest floor.** Reduced replicate counts (200 perms, 50 surrogates),
declared as gauging, not quoting.

| trace | 0.1 ms | 1 ms | 5 ms | 20 ms |
|---|---|---|---|---|
| **PLANTED** (β=1.5, witness memory ≈ AR(2) time ≈ 0.1 ms) | **+0.0142, 157× surr95, p=0.005** | ~0 | +3e-4, marginal | ~0 |
| **NULL** (β=0) | **+1.4e-4, marginally above surr95, p=0.01** | ~0 | ~0 | ~0 |

Three readings:

1. **Detection at the planted scale, absence beyond it** — the planted witness lives
   in the AR(2) memory (~0.1 ms), and the estimator finds it there and correctly
   loses it by 1 ms. The ruler recovers a planted timescale.
2. **The NULL is not quite zero at the 1e-4 scale.** With β=0 the generative truth is
   exactly zero gain, yet the shortest horizon reads +1.4e-4, marginally above its
   surrogate band. **The instrument's floor is therefore ~2e-4 bits/sample, measured
   — readings below that are not evidence of anything.** The pilot's real-data gains
   (0.025–0.040) sit 100–200× above this floor.
3. The lag-0 autocovariance bug (`x[:-0]` = empty) was caught by the validation run
   itself before any real data.

Fixed by this gauge: any battery cell whose gain is < 5× the NULL floor (i.e.,
< 1e-3 bits) is reported as BELOW-FLOOR, not as a detection, regardless of its p.
