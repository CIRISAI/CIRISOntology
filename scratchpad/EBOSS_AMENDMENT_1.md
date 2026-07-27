# AMENDMENT 1 to EBOSS_PREREG.md — the occupancy gate has FIRED, and my Stage-0 estimate was calibrated against a superseded number

Committed at the Stage-1 boundary, **before any Stage-2 computation and before any share has
been read on any eBOSS field.** The eBOSS galaxy catalogue's order-3 statistic remains unread
and blinding remains code-enforced.

This amendment records **an error of mine in `EBOSS_STAGE0.md`**, the control that caught it, and
the two design consequences that follow. Per the pre-registration's own discipline, a discrepancy
that changes a §5 choice is recorded here **before** proceeding rather than adjusted silently.

---

## A1.1 The error, and it is exactly the failure gate P12 was minted for

`EBOSS_STAGE0.md` §S0.4 estimated occupancy from the **survey shell volume** and defended that
estimate as calibrated:

> *"Amendment 2 measured BOSS SGC `n_indep = 33 264` at `R = 15` from the valid-cell count
> against this method's **31 291** — agreement to 6 %, so the estimate is not systematically
> generous."*

**That calibration was against a superseded number.** `SKY_REALDATA_AMENDMENT_2` §A2.2's
`n_indep = 33 264` describes an interim state of the BOSS pipeline; the BOSS campaign's own
**final** artifacts record something else, and Amendment 3 refers to "the corrected Stage 2 run"
that superseded it. Read off the committed files:

| source | BOSS SGC `n_indep` at `R = 15` |
|---|---|
| `SKY_REALDATA_AMENDMENT_2` §A2.2 (**superseded**) | 33 264 |
| `sky_stage2_SGC.json` — the mock geometry actually used | **13 935** |
| `sky_stage6_data.json` — the data geometry actually unblinded | **13 719** |

**I calibrated against the one number of the three that the campaign did not use.** That is
prerequisite **P12, current-numbers hygiene**, and I registered it as a prerequisite in
`EBOSS_PREREG.md` §3 one commit before violating it.

## A1.2 The control that caught it, and it clears the pipeline

`eboss_stage1_bosscheck.py` runs `sky_stage6.DataGeometry` — the BOSS campaign's own committed
geometry code, untouched — on BOSS DR12 SGC and compares to the campaign's recorded artifact:

| quantity | this run | `sky_stage6_data.json` |
|---|---|---|
| `n_indep` at `R = 15` | `13719.066868616923` | `13719.066868616923` |
| `n_indep` at `R = 10` | `52935.354391200985` | `52935.354391200985` |
| occupancy `R=15`, `b = 4 / 6 / 8` | 214 / 64 / 27 | 214 / 64 / 27 |

**Bit-identical.** So the eBOSS shortfall below the Stage-0 estimate is **real geometry, not a
bug in the eBOSS adapter** — which is the only question worth asking before writing down a gate
verdict, and it is why the control was run before the verdict rather than after it.

## A1.3 The correction, measured

The shell-volume estimator over-counts **uniformly by ≈ 2× for contiguous caps and by 3–6× for
ELG's thin, chunked footprints** — the direction §S0.4 predicted qualitatively and badly
under-estimated in magnitude.

| sample | R | Stage-0 estimate | **Stage-1 measured** | ratio |
|---|---|---|---|---|
| BOSS NGC | 15 | 83 928 | **41 767** | 2.01 |
| BOSS SGC | 15 | 31 291 | **13 719** | 2.28 |
| **LRG NGC** | 15 | 36 072 | **17 359** | 2.08 |
| **LRG SGC** | 15 | 23 058 | **9 574** | 2.41 |
| **LRG NGC** | 10 | 121 744 | **68 134** | 1.79 |
| **LRG SGC** | 10 | 77 819 | **39 127** | 1.99 |
| **ELG NGC** | 15 | 11 887 | **3 781** | 3.14 |
| **ELG SGC** | 15 | 12 324 | **1 986** | **6.21** |
| **ELG NGC** | 10 | 40 117 | **15 006** | 2.67 |
| **ELG SGC** | 10 | 41 595 | **9 516** | 4.37 |

**The *relative ranking* of the samples in `EBOSS_STAGE0.md` survives** — the factor is roughly
common across the contiguous samples — **and the absolute pass/fail against the `> 100` threshold
does not.** §S0.4's occupancy table is superseded by the table in A1.4 and is to be read only
with that label.

**And `n̄V_R`, `κ`, the areas, the independence fractions and the mock inventory are untouched**,
because none of them depends on the shell volume: `n̄V_R` is read from the shipped `NZ` column,
`κ` from the weight columns, the areas from the randoms directly. **The Stage-0 finding that
density is the binding constraint stands unmodified.** What moves is occupancy, and it moves
against the campaign.

## A1.4 THE GATE VERDICT — measured occupancy, and outcome (a) is unreachable at the primary scale

Occupancy `= n_indep / b³`, gate G9 requires `> 100`, per cap and per tracer, never pooled.

| sample | R | **b = 4** | **b = 6** | rungs passing | two-rung clause |
|---|---|---|---|---|---|
| *BOSS NGC (the detection being confirmed)* | 15 | *653* | *193* | *4, 6* | *met* |
| *BOSS SGC* | 15 | *214* | *64* | *4* | *not met — as the record already says* |
| **LRG NGC** | **15** | **271** | **80** | **4 only** | **FAILS** |
| **LRG SGC** | **15** | **150** | **44** | **4 only** | **FAILS** |
| **ELG NGC** | **15** | **59** | **18** | **none** | **FAILS** |
| **ELG SGC** | **15** | **31** | **9** | **none** | **FAILS** |
| **ELG NGC** | **10** | **234** | **69** | **4 only** | **FAILS** |
| **ELG SGC** | **10** | **149** | **44** | **4 only** | **FAILS** |
| **LRG NGC** | **10** | **1064** | **315** | **4, 6** | **met** |
| **LRG SGC** | **10** | **611** | **181** | **4, 6** | **met** |

Two consequences, and both are design-level:

> **1. At `R = 15` — the primary scale, and the scale at which BOSS's surviving 6.0 σ / 9.7 σ
> detection lives — NO eBOSS sample fields two `b` rungs. Outcome (a) is unreachable at the
> primary scale on every eBOSS sample, whatever the data reads.**
>
> **2. `EBOSS_PREREG.md` §5.3's secondary arm — ELG at `R = 10`, `b ∈ {4, 6}` — is dead as
> designed.** It fields one rung in both caps (69 and 44 at `b = 6`). ELG cannot satisfy
> outcome (a) anywhere.

**The only surviving two-rung configuration in the entire survey is LRG at `R = 10`**, in both
caps — where Stage 0 measured `n̄V_R = 1.18 / 1.16` and projected a floor of **140 % of signal,
extrapolated beyond the campaign's own measured density grid**.

## A1.5 What this amendment does NOT change

**No gate threshold, no outcome criterion, no kill condition, no null construction, no target
statistic, and no sample-exclusion decision moves.** In particular:

* The occupancy threshold stays at **100**. It is not lowered to rescue a rung. Lowering a
  pre-registered threshold after seeing that it fails is the move this entire apparatus exists to
  prevent, and `kappa-edge`'s VOID rungs are the stored case for why.
* `b = 8` and `b = 16` remain excluded; ELG at `R = 15` remains excluded (§5.3), now by
  measurement rather than by estimate.
* The mask parameters — `MASK_FRAC = 0.50`, `MASK_SMOOTH = 8.0`, `DEN_THR = 0.99` — are **not
  retuned.** They are BOSS's, applied unchanged, which is what makes the two surveys comparable
  at all. `DEN_THR = 0.99` costs 2.6× in valid cells and was adopted on BOSS precisely because
  `0.5` inflated a pure shot-noise null by 6.6×. **Relaxing it here would buy occupancy by
  reinflating the floor**, which is not a trade, and any change to these constants is a new
  pre-registration rather than an amendment.
* **`EBOSS_PREREG.md` §2.4's registered expectation stands and has, so far, been correct in the
  direction it named**: the campaign was expected to fail the primary-scale two-rung clause. It
  fails it for a reason the projection did not name — occupancy rather than significance — which
  is a worse failure than the one forecast, because it does not depend on what the data reads.

## A1.6 What proceeds, and what stops

**Stops here, pending Eric's review, because the pre-registered design no longer describes a
campaign that can reach its own primary outcome:**

* Stage 2 (the G10 mock closure) on the arms as pre-registered. Running G10 on an arm that cannot
  satisfy outcome (a) would be spending a machine-day to gauge an instrument already known not to
  reach.
* Any re-designation of `R = 10` as the primary scale. **That is a pre-registration-level choice,
  it would be made after seeing a gate fire, and it is not the author's to make silently.** The
  §5 arms were fixed before any reading precisely so that this move would require a signature.

**The three options, stated without a recommendation being smuggled in as a finding:**

1. **Re-designate LRG `R = 10` as primary** (the only two-rung configuration), accepting a floor
   of ~140 % of signal that is *extrapolated beyond the campaign's own measured grid* — i.e.
   accepting that outcome (e), "not decomposed", is the likely landing.
2. **Run the campaign for outcome (c) only** — an honest upper bound at `R = 15`, single-rung,
   reported with its ceiling fraction. This needs no design change: outcome (c) has no two-rung
   clause, and §9(c) already records that an eBOSS null is a substantive result about BOSS's
   systematics.
3. **Stop at Stage 1** and record eBOSS as measured-and-insufficient, leaving `wild-share` open
   with DESI still named as the instrument and the network block still the thing to fix.

**Option 2 is the only one that needs no amendment to §5 and no post-hoc scale change, and it is
the one this document proceeds under if no other order is given** — with the explicit note that a
single-rung bound is a weaker deliverable than the campaign was commissioned for, and that saying
so is the point.

**Proceeds now, because none of it depends on the choice above:** nothing. Stage 1 is complete;
its results are in `EBOSS_STAGE1.md`.

---

*Amendment ends. No eBOSS share has been read; the galaxy catalogue's order-3 statistic remains
unmeasured, and `measure_catalogue` still raises without `stage6_unblind=True`.*
