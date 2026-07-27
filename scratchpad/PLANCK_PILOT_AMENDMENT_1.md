# AMENDMENT 1 — V8's criterion, and the WMAP band

**Prompted by Stage 1 (V8 surrogate sanity), which is the stage `PLANCK_PILOT_PREREG.md` §10
runs first precisely so that this kind of thing is found before any data reading. No share has
been computed on Planck or WMAP pixel values. The primary grid, the templates, the ladders, the
test statistic of §7.2 and the VOID conditions are untouched.**

The numbers that prompted this amendment are stated first, per the sky campaign's amendment
discipline.

---

## 1. THE NUMBER

`PLANCK_PILOT_PREREG.md` §8, **V8** reads:

> *If the S1 ensemble's own `C_ℓ` does not match the data's to machine precision, or its measured
> skewness inside the mask is not consistent with zero at the ensemble's own scatter, the
> surrogate is fouled and everything downstream of it is void.*

Stage 1 ran it. **The skewness leg passed cleanly.** The `C_ℓ` leg, read literally, **fired**:

| instrument | median per-`ℓ` ratio | max \|ratio − 1\| | where |
|---|---|---|---|
| Planck, `lmax = 4096` | 1.0000010 | **46.2** | `ℓ = 2518`, where `C_ℓ = 7.7e−25 K²` |
| WMAP, `lmax = 1535` | — | — | a uniform ~0.5 % power deficit at **every** `ℓ` |

Broken out by band, Planck:

| `ℓ` band | median ratio | max \|r−1\| | median `C_ℓ` (K²) |
|---|---|---|---|
| 2–2500 | 1.00000 | **≤ 1.0e−4** | 1.6e−10 → 2.0e−17 |
| 2500–3000 | 5.38 | 40.9 | **2.6e−23** |
| 3000–4096 | 12.1 – 18.4 | 40.3 | **1.4e−23 → 9.7e−25** |

---

## 2. THE DIAGNOSIS — the criterion was measuring the verifier, not the surrogate

Two separate causes, and neither is a defect in the surrogate.

**(a) Planck.** The deviation lives entirely above `ℓ = 2500`, where the SMICA map's power has
fallen **six decades** below the band that carries the signal. A per-`ℓ` *ratio* criterion is
meaningless there: a factor of 40 on `1e−25 K²` against a map variance of `1.17e−8 K²` is
`4e−15` of the variance, and it is *added* high-`ℓ` power, which is white and symmetric and
therefore mints exactly nothing (`valve_needs_asymmetry`). The smallest template in the ladder
(8′) corresponds to `ℓ ≈ 1350`, entirely inside the band where the ratio is 1 to 1e−4.

**(b) WMAP.** The uniform 0.5 % deficit is **healpy's analysis quadrature error**, not the
surrogate's. `map2alm` at `iter = 0` with `lmax = 3·nside − 1 = 1535` under-integrates; the
surrogate is built from those under-integrated `a_ℓm` and then measured with the *same*
under-integrating estimator, so the bias is applied twice and the ratio reads `≈ 1 − b`.

**The decisive check, which the original criterion did not ask for.** The surrogate's harmonic
content is the data's extracted `a_ℓm` with moduli preserved — that is what phase randomisation
*is*, and it can be verified directly rather than through a round trip:

> `max | |a_ℓm^surr| − |a_ℓm^data| | = 1.69e−21`, **relative 4.17e−16** (Planck, `ℓ ≥ 2`,
> 8 388 606 modes).

That is machine precision, and it is exact by construction. And the operationally relevant
quantity — the two-point correlation function **at the twelve templates' own separations**, which
is the pair structure the pipeline actually reads — matches:

| instrument | `ξ(θ)` agreement over 8, 16, 32, 64, 128, 256′, 5 realisations | total variance |
|---|---|---|
| **Planck**, `lmax 4096`, `iter 0` | max \|ratio − 1\| = **1.47e−05** | 1.8e−06 |
| **WMAP**, `lmax 1535`, `iter 0` | max \|ratio − 1\| = **1.68e−02** | 5.2e−03 |
| **WMAP**, `lmax 1024`, `iter 3` (round trip) | median per-`ℓ` ratio **0.99999999984**, variance ratio **0.99999999965** | 3.5e−10 |

WMAP carries **1.3e−06** of its harmonic variance above `ℓ = 1024` (it is delivered smoothed to
1° FWHM), so capping there discards nothing measurable and removes the aliased band where
`iter = 0` analysis is unreliable.

---

## 3. THE AMENDMENT

**(i) V8's `C_ℓ` leg is restated in the form that tests the surrogate rather than the verifier.**
It now has three legs, all three required:

1. **Exactness of construction** — `max | |a_ℓm^surr| − |a_ℓm^data| | / |a_ℓm^data| < 1e−12`
   over `ℓ ≥ 2`. This is the leg that says the surrogate carries the data's `C_ℓ`. Planck:
   **4.17e−16, PASS.**
2. **Pair structure at the templates' own separations** — `|ξ_surr(θ)/ξ_data(θ) − 1| < 1e−3` at
   every separation appearing in the ladder (8, 16, 32, 64, 128, 256′), and the same bound on
   the total variance. This is the leg that says the surrogate reproduces what the pipeline
   reads. Planck: **1.47e−05, PASS.** WMAP after (ii): to be reported in Stage 1b.
3. **Skewness inside the mask consistent with zero at the ensemble's own scatter** — unchanged.

The superseded per-`ℓ` "machine precision" wording is **withdrawn as unmeasurable**: it cannot be
satisfied by any synthesised map in a band where `C_ℓ` has fallen below the analysis operator's
own noise, and a criterion no correct implementation can pass is a gate that would have to be
switched off. Recording the withdrawal rather than quietly reinterpreting it.

**(ii) WMAP's surrogate band changes from `lmax = 1535` to `lmax = 1024`, and both instruments'
base `a_ℓm` extraction changes from `iter = 0` to `iter = 3`.** Justification is the table in §2;
cost is one extra transform per instrument, paid once. `lmax = 1024 = 2·nside` is healpy's own
reliable analysis limit at `nside = 512`.

**Nothing else changes.** Planck stays at `lmax = 4096`, unsmoothed, undegraded, at native
`NSIDE`, because §3.2 of the pre-registration forbids adding a filter the instrument did not
already apply — and truncating the surrogate's band while leaving the data's intact would be
exactly such a filter, applied to one side only.

---

## 4. WHAT THIS DOES NOT CHANGE

The primary grid (72 cells), the twelve templates, the `b`-ladder, the surrogate counts, the
primary test statistic and its leave-one-out calibration (§7.2), the pre-registered expectation
(§7.1) and VOID conditions V1–V7 are **untouched**. No data reading has been taken. The Stage 1
outputs that prompted this amendment are
`scratchpad/planck_pilot/stage1_surrogate_sanity.json` and
`scratchpad/planck_pilot/stage1_v8_powerweighted.json`, both committed with it.
