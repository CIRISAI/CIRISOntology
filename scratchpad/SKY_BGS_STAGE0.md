# STAGE 0 — **COMPLETE.** DESI DR1 BGS inventoried; all four rules applied; one §5 choice inverted.

Supersedes the BLOCKED version of this document (`SKY_BGS_STAGE0.md` at the stage boundary,
which recorded an unreachable host and applied no rule). Every number below is read from a DESI
header or measured from a DESI byte count on **2026-08-09**. Nothing here is recalled.

**The unblind order is still not the author's to give. No `§6` statistic has been computed and no
`δ`, `z`, or `p` appears in this document.** Stage 0 is inventory and rule-application only.

---

## S0.0 The blocker is cleared

`data.desi.lbl.gov` is reachable from this host for the first time since the campaign was staked.
The outage placeholder ("*Currently data.desi.lbl.gov is down due to power outage maintenance of
the underlying Spin service at NERSC*") is gone.

| probe | previous | now |
|---|---|---|
| `https://data.desi.lbl.gov/public/` | HTTP **000**, `No route to host` | **200** |
| `https://data.desi.lbl.gov/public/dr1/` | **000** | **200** |
| `.../dr1/survey/catalogs/dr1/LSS/` | unreachable | **200**, lists `iron/` + `random0/`…`random17/` |
| `https://data.desi.lbl.gov/public/dr2/` | — | **401** — collaboration-only, not used |

The randoms are the thing whose absence killed the earlier attempt (the Data Lab route carried
DR1 redshifts but no LSS catalogues, randoms or mocks, so no density field could be built).
**Eighteen random realizations are present.**

---

## S0.1 RULE S0-B — applied first, because it scopes everything else

Measured `Content-Length` from `HEAD`, `.../LSS/iron/LSScats/v1.5/`:

| file | size |
|---|---|
| `BGS_BRIGHT_NGC_clustering.dat.fits` | 324.7 MB |
| `BGS_BRIGHT_SGC_clustering.dat.fits` | 116.9 MB |
| `BGS_BRIGHT-21.5_NGC_clustering.dat.fits` | 24.3 MB |
| `BGS_BRIGHT-21.5_SGC_clustering.dat.fits` | 9.2 MB |
| `BGS_BRIGHT*_NGC_0_clustering.ran.fits` (one of 18) | 1579.4 MB |
| `BGS_BRIGHT*_SGC_0_clustering.ran.fits` (one of 18) | 647.7 MB |

Randoms are cap-specific and shared across the two magnitude cuts.

* both caps, 18 randoms each: 27.76 + 11.39 GB randoms + 0.44 GB data = **39.6 GB**
* NGC only, 18 randoms: 27.76 + 0.32 GB = **28.1 GB**

**39.6 GB exceeds the 35 GB threshold fixed in the pre-registration.** RULE S0-B therefore
**fires**: the campaign is **scoped to NGC only**.

Consequence, as the rule already specified rather than as a discovery: the NGC-vs-SGC
cap-consistency check is unavailable, and **P11 is satisfied by ≥4 volume-matched sub-patches
within NGC**, scored against mock-predicted dispersion. The prereg calls this a redesign of the
check rather than a waiver, and notes it carries more degrees of freedom than the two-cap version.

---

## S0.2 RULE S0-A — the sample choice, and it **inverts** §5.1's stated expectation

`n̄V_R` computed at `R = 15 Mpc/h` (`V = 14 137 (Mpc/h)³`) from the per-object `NX` column of the
NGC clustering catalogues, trimmed per the rule to keep `n̄V_R` within a factor of 3 of its median.

| | `BGS_BRIGHT-21.5` | `BGS_BRIGHT` |
|---|---|---|
| `N` (NGC) | 217 614 | 2 909 876 |
| `z` span in file | 0.100 – 0.400 | 0.010 – 0.500 |
| `n̄` (median `NX`) | 3.63e-4 | 7.35e-3 |
| `n̄` dynamic range | **2.4×** | **2418×** |
| trimmed `z` range | 0.100 – 0.400 (no trim) | 0.080 – 0.320 |
| `N` retained | 217 614 | 2 176 226 |
| median `n̄V_R` | 5.13 | 120.84 |
| **min `n̄V_R`** (the rule's criterion) | **3.18** | **19.94** |

**`BGS_BRIGHT` wins by 6.27×. The choice is not a tie (rule threshold 20 %), so the tiebreak
toward `-21.5` does not apply.**

**Robustness.** The rule's phrase "the *range* is trimmed to keep `n̄V_R` within a factor of 3 of
its median" admits two readings. Both were computed and both choose `BGS_BRIGHT`:

| reading | `-21.5` min | `BRIGHT` min |
|---|---|---|
| A — trim by per-object occupancy, span the kept objects | 3.18 | 19.94 |
| B — trim by binned `n̄(z)` profile (0.02 bins, ≥200 objects) | 3.18 (binned 4.84) | 15.54 (binned 26.02) |

**This inverts §5.1.** The prereg reasoned that *"the sample with a usable selection function may
be the one with only a 2–3× density gain"* — i.e. that `-21.5`'s flat `n̄(z)` would beat
`BGS_BRIGHT`'s steep one. The flatness is real and confirmed (2.4× vs 2418×), but it is flat **at
a low normalization**: `-21.5` reaches only `n̄V_R = 3.18`, which is **5× below BOSS's own 16.2 at
the same scale**. `BGS_BRIGHT`, trimmed, clears BOSS at 19.94.

The rule was fixed in advance and it decided against the author's stated expectation. That is what
it was for. **Recorded as an inverted prior, not as a confirmation.**

---

## S0.3 RULE S0-D — `R★` is **ABSENT**

`R★` is defined as the smallest `R ∈ {12, 10, 8, 6}` at which the read `n̄V_R ≥ 16.2`. On the
S0-A-chosen sample over its trimmed range:

| `R` | min `n̄V_R` | median | `≥ 16.2`? |
|---|---|---|---|
| 15 | 19.94 | 120.84 | **yes** |
| 12 | 10.21 | 61.87 | no |
| 10 | 5.91 | 35.80 | no |
| 8 | 3.02 | 18.33 | no |
| 6 | 1.28 | 7.73 | no |

**No `R` in the extension set qualifies. `R★` is recorded as ABSENT**, which the prereg's
scoring table explicitly permits ("`R★` fixed by RULE S0-D, **or recorded as absent**").

Consequence: the extension arm loses its third scale. Rows scored fall from "2 caps × up to 3
scales" to **1 cap × 2 scales (`15`, `10`)** — and `R = 10` runs at `min n̄V_R = 5.91`, below BOSS's
reference, so it is an extension scale carrying a known-degraded occupancy rather than a
confirmation scale. **This must be stated wherever `R = 10` is reported.**

---

## S0.4 RULE S0-C — mock inventory

`.../dr1/survey/catalogs/dr1/mocks/` lists two suites, both with a `bright/` (BGS) branch:

| suite | branch | realizations | kind |
|---|---|---|---|
| **AbacusSummit** | `bright/v1/altmtl0…24` | **25** | **N-body** |
| **EZmock** | `bright/v1/mock1…1000` | **1000** | approximate (fast, for covariance) |

**This is a material improvement on the BOSS campaign.** Amendment 4 there restricted outcomes
because *Patchy is not N-body* — the available mocks could not support the discrimination the
design wanted. DR1 ships **25 genuine N-body BGS realizations**, so the suite assignment is:

* **AbacusSummit (N-body)** — the closure/consistency arm that Patchy could not serve.
* **EZmock (1000)** — covariance and dispersion floors, where realization count matters more
  than per-realization fidelity.

Mocks are **stream-processed and never fully extracted**, per Amendment 1, which stands unchanged.

---

## S0.5 Every `[to verify]` in §5.1–5.2, resolved

| item | prereg guess | measured | verdict |
|---|---|---|---|
| `-21.5` = mag-cut sample for full-shape | asserted | confirmed by file naming | ✓ |
| `-21.5` `N` | ~300 000 | **217 614** (NGC) | close; NGC-only accounts for it |
| `-21.5` `n̄` | "roughly flat, 5e-4–1e-3" | **flat (2.4×), 3.63e-4** | flat ✓, normalization **low by ~1.5–3×** |
| `-21.5` `z` range | `0.1 < z < 0.4` | **0.1001 – 0.4000** | exact ✓ |
| `BRIGHT` `n̄` | "reaches ~1e-2 at `z<0.2`, falls steeply" | **1.29e-1 max, 2418× range** | steep ✓, **more extreme than guessed** |
| `BRIGHT` `z` span | not stated | 0.010 – 0.500 | — |
| columns | not stated | `TARGETID Z NTILE RA DEC PHOTSYS FRAC_TLOBS_TILES WEIGHT_ZFAIL WEIGHT_SYS WEIGHT WEIGHT_COMP flux_{g,r,z,w1,w2}_dered NX WEIGHT_FKP` | — |
| `n̄(z)` column name | not stated | **`NX`** (no `NZ` column) | — |
| mock suites exist for BGS | uncertain | **AbacusSummit 25 (N-body) + EZmock 1000** | ✓ better than expected |

**Density-gain premise, checked.** The commission's "10–100× BOSS" figure describes `BGS_BRIGHT`
at low `z` over a small volume. Against BOSS's `n̄V_R = 16.2` at `R = 15`, the honest gain on the
**usable** trimmed range is **19.94 / 16.2 ≈ 1.23× in occupancy** — not 10–100×. The prereg
anticipated this reading ("the sample with a usable selection function may be the one with only a
2–3× density gain"); the measured answer is that even the steep sample, once trimmed to a usable
selection, buys ~1.2× rather than an order of magnitude. **The premise as commissioned does not
survive contact with the selection function, and §7's power expectations must be re-derived.**

---

## S0.6 Scoring-table status

| # | rule | status |
|---|---|---|
| 2 | S0-A sample choice, both computations recorded | **applied** — `BGS_BRIGHT`, 19.94 vs 3.18, both readings recorded |
| 3 | S0-B scoping with measured byte count | **applied** — 39.6 GB > 35 GB → **NGC only** |
| 4 | S0-C mock suites inventoried, assignment fixed | **applied** — AbacusSummit N-body (closure) + EZmock ×1000 (covariance) |
| 5 | S0-D `R★` fixed or recorded absent | **applied** — **ABSENT** |

## S0.7 Amendment trigger

The prereg's Stage-0 row states: *any discrepancy changing a §5–§7 choice triggers an amendment
before proceeding.* **Three fire:**

1. **§5.1** — the sample choice inverted (`BGS_BRIGHT`, not `-21.5`).
2. **§5.2** — the redshift range is `0.080 < z < 0.320` (S0-A's trim), not the `0.1 < z < 0.4` the
   section assumed.
3. **§7** — `R★` absent removes a scale; the density-gain premise is ~1.2× not 10–100×, so the
   power expectations built on it do not hold as written.

`SKY_BGS_AMENDMENT_6.md` carries these before any Stage-1 statistic is computed.
