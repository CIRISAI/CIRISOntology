# AMENDMENT 1 to SKY_REALDATA_PREREG.md — Stage 0 results

Committed **before Stage 1 and before any clustering statistic has been computed on any
catalogue.** Stage 0 reads metadata and the selection function only: counts, redshifts,
weights, `n̄(z)`, effective area. **No order-3 quantity, no correlation function, no power
spectrum has been evaluated on the data.**

Per the reviewer's binding reminder 1, every `[to verify]` number in the pre-registration has
been replaced by a read number, and every discrepancy that touches a §3–§4 choice is recorded
here **before** proceeding rather than adjusted silently.

Catalogues read: `galaxy_DR12v5_CMASSLOWZTOT_{North,South}.fits.gz` (DR12 combined sample,
`0.2 < z < 0.75`), from `data.sdss.org/sas/dr12/boss/lss/`.

---

## A1.1 The `[to verify]` table, resolved

| quantity | prereg said | **measured at Stage 0** | verdict |
|---|---|---|---|
| galaxies, `0.2 < z < 0.75` | *[to verify]* ~1.2 M | **1 198 004** (NGC 864 923, SGC 333 081) | **verified** |
| rows in catalogue (all `z`) | — | NGC 953 255, SGC 372 601 | recorded |
| effective area | not stated | **8 703 deg²** (NGC 6 325, SGC 2 378) | new |
| shell volume `0.2<z<0.75` | not stated | **5.388 (Gpc/h)³** | new |
| **`V_eff` (FKP, `P₀=10⁴`)** | *[to verify]* "≈ 4 (Gpc/h)³" | **2.221 (Gpc/h)³** | **DISCREPANCY, §A1.2** |
| `n̄` typical | *[to verify]* "≈ 4e-4 peak" | **3.05e-04** typical, 4.3e-4 peak | verified, slightly low |
| **`n̄ V_R` at `R=10`** | *[to verify]* "≈ 6" | **4.81** | **verified, slightly worse** |
| `n̄ V_R` at `R=15` | not stated | **16.22** | new, **and it matters — §A1.3** |
| occupancy `b=8`, `R=10` | *[to verify]* ~490/cell | **668/cell** | **verified, gate passes** |
| occupancy `b=16` | *[to verify]* ~60, "expected to fail" | **84 (R=10), 25 (R=15)** | **verified, fails as predicted** |
| **growth lever `D` ratio** | *[to verify]* 1.21 | **1.1095** | **DISCREPANCY, §A1.4** |
| growth precision needed | *[to verify]* 5.7 % | **6.3 %** | verified |

Cosmology used for distances and growth: `Ω_m = 0.31`, flat, `h = 0.68` — as pre-registered.

## A1.2 `V_eff` is 2.22, not ~4 (Gpc/h)³ — recorded, changes nothing

My estimate was 45 % high. It does **not** change a §3–§4 choice:

* The **occupancy gate** counts independent smoothing volumes and correctly uses the *shell*
  volume (5.388 (Gpc/h)³), not `V_eff`. It passes at `b ≤ 8` and fails at `b = 16` exactly as
  pre-registered — so the pre-registered exclusion of `b = 16` was right for the right reason.
* The **statistical** requirement from the mock forecast was `0.11–0.27 (Gpc/h)³`. `V_eff =
  2.22` clears it by 8–20×. §7.8 of the prereg — "nothing here is limited by statistics and
  everything is limited by the floor model" — survives the correction with margin.

## A1.3 THE ONE CHANGE THAT MATTERS: the primary scale moves from `R = 10` to `R = 15`

The density number driving the shot-noise floor is now measured, and it is worse than I
estimated at `R = 10` and much better at `R = 15`:

| scale | `n̄ V_R` | shot-noise floor, interpolated on my measured grid |
|---|---|---|
| `R = 10` | **4.81** | **≈ 95 % of signal** |
| `R = 15` | **16.22** | **≈ 58 % of signal** |

(Interpolated logarithmically between the two measured points of `SKY_FORECAST_RESULTS.md`
§12: `n̄V_R = 1.6` → 130 % of signal, `n̄V_R = 15.7` → 58 %.)

**Amendment: `R = 15` Mpc/h becomes the PRIMARY scale and `R = 10` is demoted to secondary.**
Both remain in the analysis. The reason is that at `R = 15` the largest of the three
manufacturing channels is nearly halved, and my own results say this measurement is limited by
the floor model and not by statistics — the forecast's `z_s = 43` at `R = 15` is far more than
enough, so trading raw significance for a smaller floor is the right trade at every point.

**A consequence I must flag rather than bury: I have no binmint measurement at `R = 15`.** My
mock campaign bracketed it — `R = 10` retained 86–100 % of the signal under the binarization
control, `R = 25` failed at `t_corr = 0.5–0.9` — but `R = 15` itself was never run.
**Stage 4 must run the binmint control at `R = 15` before the primary is read, and if it
behaves like `R = 25` rather than like `R = 10`, the primary reverts to `R = 10` with its
larger shot-noise floor.** That decision is pre-registered here, before any data reading.

## A1.4 The growth lever is weaker than stated: 1.11, not 1.21

Redshift bins split at `z = 0.45`, weighted by `n̄²V`: **low bin `z_eff = 0.329` (`D = 0.8409`),
high bin `z_eff = 0.532` (`D = 0.7579`)**, ratio **1.1095**. With `A ∝ D^{0.82}` the predicted
signal ratio is **1.089**, needing **6.3 %** per-bin precision for 3 σ.

Pushing to the extreme bins does not rescue it: the `z ≈ 0.71` bin has `n̄ = 3.6e-05`, an order
of magnitude below the sample mean, so its shot-noise floor would swamp the gain in lever.

**The §4.3 registration stands and is reinforced: the growth check is a consistency check with
its power stated, not a discriminator.** It is now expected to be *uninformative* rather than
merely weak, and the prereg's instruction to report it as uninformative rather than as a pass
is the branch I expect to take.

## A1.5 Resource plan revised — the approved 150 GB does not fit, and does not need to

Measured, not estimated:

* Available disk: **147 GB** against a planned peak of ~150 GB. **The approved plan does not
  fit.**
* Mock suites are **monolithic** `.tar.gz`: `Patchy-Mocks-DR12NGC-COMPSAM_V6C.tar.gz`
  **41.08 GB**, SGC **15.56 GB**. A `.tar.gz` is not randomly accessible, so **a subset cannot
  be downloaded** — it is all or nothing per cap.
* Sustained download rate measured over a 100 MB ranged request: **5.9 MB/s** ⟹ **≈ 2.8 h** for
  both caps.
* Galaxy catalogues 206 + 79 MB (downloaded); random catalogues 1.88 GB + 716 MB (not yet).

**Amendment: mocks are STREAM-processed, never fully extracted.** Each realisation is read from
the tarball, reduced to its summary statistics, and discarded. Revised peak storage
**≈ 65 GB** (tarballs 56.6 + catalogues/randoms ~3 + working ~5), comfortably inside 147 GB.
This is a reduction against the approved scope, not an increase.

## A1.6 G5 operationalised, per the reviewer's note

The reviewer is right that "must read exactly zero" is unusable as written. Operationalised, as
my own forecast practice already did:

> **G5.** The sign-symmetric Gaussian mock control, through the identical pipeline, must read
> **consistent with zero at the measured mock-scatter precision**: `|mean| / SEM < 3` across
> the control realisations, with **the band quoted in the results** (the forecast's
> corresponding numbers were `t = +1.37` and `+1.40` over six realisations). A reading outside
> that band is pipeline error and **VOIDs** the run, per §6(d).

The theorem behind it is unchanged and is what makes the control meaningful: a sign-symmetric
field's binarized share is exactly zero by `share_eq_zero_of_signSymmetric`, so anything the
control reads *is* pipeline error rather than signal.

## A1.7 Nothing else moves

No gate threshold, no outcome criterion, no kill condition, and no data choice is altered. The
`b ∈ {4, 6, 8}` range, the occupancy gate, the LP pair-pinning gate, G10 mock closure at 10 %
of signal, and all four outcomes stand exactly as pre-registered. BOSS DR12 + Patchy remains
primary; the §4.2 escape hatch to a denser tracer remains a **Stage-2** decision contingent on
G10, not a Stage-0 one, and Stage 0 does not trigger it.

---

*Amendment ends. No clustering statistic has been computed on any real catalogue.*
