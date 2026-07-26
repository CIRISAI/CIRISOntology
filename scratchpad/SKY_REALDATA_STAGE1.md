# STAGE 1 — pipeline built and validated. State note at the stage boundary.

Committed at the Stage 1 → Stage 2 boundary per the reviewer's binding reminder 5.
**No clustering statistic has been computed on the real galaxy catalogue.** Stage 1 validated
on the RANDOM catalogue only, which carries the survey geometry and by construction carries no
clustering signal.

Blinding is enforced in code, not by intention: `sky_realdata.measure_catalogue()` raises
unless `stage6_unblind=True`, and nothing in Stages 1–5 passes it.

---

## S1.1 What was built

`sky_realdata.py` — the full pre-registered path: sky → comoving Cartesian (fiducial
`Ω_m=0.31, h=0.68`) → interlaced CIC deposit onto a 5-smooth grid → local-mean density with
mask → masked smoothing `W*(δM)/(W*M)` → quantile binning over valid cells → triple histogram
with all three cells inside the footprint → `I_C⁽³⁾(b)` by IPF with the KL certificate → the
LP pair-pinning interval.

**Grid sizing.** Power-of-two padding costs 4.5× here; 5-smooth dimensions give NGC ≈ 60 M
cells at `cell = 6` Mpc/h instead of 268 M. SGC measured: `(270, 450, 270)` = 32.8 M cells,
0.12 GB float32.

## S1.2 Two real defects the validation caught

**(a) The survey-edge threshold was inflating a pure shot-noise null by 6.6×.** On the
split-randoms null — half the randoms play "galaxies", so the truth is pure Poisson noise with
no clustering — the field read `σ = 0.66` against an analytic shot-noise prediction of `0.116`.
Cause: cells whose smoothing kernel straddles the survey boundary divide by a small
denominator in `W*(δM)/(W*M)`, amplifying edge noise. Measured recovery:

| mask `frac` | kernel threshold | valid cells | `σ` | predicted |
|---|---|---|---|---|
| 0.25 | 0.50 | 9 027 529 | **0.660** | 0.116 |
| 0.25 | 0.99 | 3 445 768 | 0.206 | 0.116 |
| **0.80** | **0.99** | **3 401 617** | **0.147** | **0.101** |

Adopted: `frac = 0.80`, kernel threshold `0.99` (≥99 % of the smoothing kernel on valid
cells). The residual 1.45× is the ~10× variation of `n̄(z)` across the sample, which the
uniform-density prediction does not capture. **It costs 2.6× in valid cells, which is the
right trade when statistics are not the limit** — the same logic that moved the primary scale
to `R = 15` in Amendment 1.

**(b) I had implemented the occupancy gate wrongly.** The pre-registration says occupancy must
be counted from **independent smoothing volumes**, not galaxies — and my first implementation
used raw triple counts, which are grid cells and overstate independence by ~250× at `R = 15`.
It reported `b = 8` passing at 50 000 per cell when the honest number is 27. Fixed to
`n_indep = N_valid · cell³ / (2π)^{3/2}R³`.

## S1.3 The occupancy gate now bites, as designed

SGC alone, corrected mask and corrected occupancy:

| `R` | valid cells | independent volumes | `b=4` | `b=6` | `b=8` |
|---|---|---|---|---|---|
| **15** | 3 401 617 | 13 823 | **216 PASS** | 64 **FAIL** | 27 **FAIL** |
| 10 | 3 708 471 | 50 860 | **795 PASS** | **236 PASS** | 99 **FAIL** |

Scaling by NGC's ~2.7× larger footprint, the combined sample is expected to give at `R = 15`:
`b=4 ≈ 800`, `b=6 ≈ 237`, `b=8 ≈ 100` — **marginal at `b = 8`.**

**This needs no amendment.** The pre-registration set the gate precisely to make this call and
says "any `b` failing that is not reported". The gate is working; the practical range at the
primary scale is narrowing to `b ∈ {4, 6}`, and `b = 8` will be reported only if the combined
footprint clears 100.

## S1.4 Numbers that Stage 2 needs, now measured rather than estimated

* **IPF certificates**: `4.5e-15` to `2.8e-12` across all configurations — four orders inside
  the pre-registered `1e-9` void threshold. **G9 passes.**
* **Cost**: SGC deposit 29 s (both halves), then **16 s per (field, scale)**. A full SGC
  realisation at two scales ≈ **61 s**; NGC ≈ 2.7× ≈ **165 s**; **≈ 226 s per mock across both
  caps.**
* **Consequence, flagged now rather than at the wall:** 2048 realisations × 226 s ≈ **128
  hours**, against an approved budget of ~1 machine-day. **The mock count must be reduced, and
  Stage 2 will open with an amendment carrying this measured cost** — not a guess. The
  precision argument is already in hand: the floor's per-realisation scatter was ~13 % of its
  mean in the mock campaign, so a few hundred realisations put the floor mean far inside G10's
  10 %-of-signal bar. The amendment will state the count and the resulting floor precision
  before any mock is read.

## S1.5 The split-randoms null is not zero, and that is the expected reading

The null returns `I_C⁽³⁾ = 4.8e-04` (`R=15`, `b=4`) to `3.9e-03` (`R=10`, `b=6`) nats. **This
is not a failure**: randoms carry the window and are Poisson-sampled, so this reading *is* the
window-plus-shot-noise floor that the pre-registration requires to be forward-modelled rather
than assumed small. It is the quantity G10 must reproduce on held-out mocks to 10 % of signal.

Recording it plainly because it is an early warning: it is large. Direct comparison with the
mock campaign's gravity signal is not available (different binning, different geometry, no
matched-Gaussian subtraction here), and manufacturing that comparison would be exactly the
error this programme keeps catching. **The honest statement is that the floor has been
measured for the first time on the real geometry and that G10, not statistics, decides this
measurement — which is what §7.8 of the pre-registration said before any data was touched.**

## S1.6 State

| stage | status |
|---|---|
| 0 — inventory | **COMPLETE**, Amendment 1 committed (`8b0c108`) |
| 1 — pipeline | **COMPLETE**, this note; two defects caught and fixed |
| 2 — floor model + **G10 go/no-go** | **BLOCKED on download**; opens with the mock-count amendment |
| 3–5 — controls, G1/G2, N-body prediction | not started |
| 6 — unblind | not started; blinding enforced in code |
| 7 — write-up | not started |

Download in progress to `/home/emoore/skydata` (outside the repo): galaxy and random
catalogues complete (2.9 GB); Patchy SGC 15.56 GB and NGC 41.08 GB pulling at a measured
5.9 MB/s, ETA ≈ 2.7 h from 23:44. Disk after completion ≈ 88 GB free of 147 GB.

**Stages 2–7 are a multi-session job and are not being improvised into this one.**
