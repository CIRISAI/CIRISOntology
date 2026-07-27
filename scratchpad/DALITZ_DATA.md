# DALITZ DATA — public-data inventory, honest

**Question.** What exists publicly as a **binned Dalitz distribution** — or as event-level
`(m²₁₂, m²₁₃)` from which one can be built — with a **charge/flavour tag** so CP conjugates can
be separated, and with **efficiency and background treatment stated**? As opposed to fitted
amplitude-model parameters, which are the field's normal deliverable and are **not** a
distribution.

Written before `DALITZ_PREREG.md` and before any measurement. Scratchpad only.

**Verification policy.** Every row below is marked with how it was checked. `[V]` = I fetched
the primary record or file myself and read its contents. `[R]` = reported by a search agent and
**not** independently verified — treat as a lead, not a fact. Four of the seventeen `[R]`
HEPData rows were spot-checked by me and all four confirmed, which raises confidence in the rest
without establishing it.

---

## HEADLINE

**One dataset can carry this measurement, and it is not a binned distribution — it is a raw
ntuple we would have to bin ourselves.**

1. **LHCb open data record 4900** (`B± → h±h⁺h⁻`, 2011, 8.55 M candidates) is the **only**
   public event-level three-body dataset with a charge tag. It gives full three-momenta per
   event, so we can build `(m²₁₂, m²₁₃)` under any mass hypothesis, and the per-track charges
   give the parent `B` charge, so **`B⁺` and `B⁻` are fully separable**. It ships with **no
   efficiency map, no background model, no sWeights, and no detector simulation.** `[V]`
2. **KLOE-2 `η → π⁺π⁻π⁰`** (HEPData ins1416990, Table 1) is the **only public 2-D binned Dalitz
   distribution I could find anywhere** — 371 cells, acceptance-corrected and unfolded. But `η`
   is self-conjugate, so **there is no CP conjugate**; the available conjugation is **C**, which
   acts on the Dalitz plane as `X → −X`. `[V]`
3. **Everything else** — every BaBar, Belle, BESIII, LHCb and CLEO-c three-body record I or the
   search agent examined — is **one-dimensional mass projections** or **amplitude-fit
   parameters**. There is no public 2-D binned Dalitz distribution for any charm or beauty mode.
   `[V]` on four records, `[R]` on thirteen more.

**Consequence for the campaign.** The two candidate datasets are *complementary and both
partial*: LHCb has the CP conjugation but no released efficiency; KLOE-2 has the released,
corrected 2-D distribution but no CP conjugation. Neither alone delivers the headline
measurement in its strongest form. The prereg must therefore choose deliberately, and say which
weakness it is accepting.

---

## 1. LHCb OPEN DATA, RECORD 4900 — the only CP-separable event-level set

| | |
|---|---|
| **record** | https://opendata.cern.ch/record/4900 `[V]` |
| **title** | *Matter Antimatter Differences (B meson decays to three hadrons) — Data Files* |
| **collaboration / year** | LHCb, 2011 data at √s = 7 TeV, released 2017 `[V]` |
| **DOI** | 10.7483/OPENDATA.LHCB.AOF7.JH09 `[R]` |
| **files** | `B2HHH_MagnetDown.root` (666 484 974 B), `B2HHH_MagnetUp.root` (444 723 234 B), `PhaseSpaceSimulation.root` (2 272 072 B) `[V]`, byte sizes from the record API |
| **HTTP access** | `https://opendata.cern.ch/eos/opendata/lhcb/AntimatterMatters2017/data/<file>` returns HTTP 200 `[V]` — no xrootd client needed |
| **companions** | record 4901 (instructions PDF), 4902 (project notebook, GPL-3.0) `[R]` |

**Schema, read off the downloaded files themselves with `uproot`** `[V]`. `B2HHH_MagnetDown.root`
carries tree **`DecayTree` with 5 135 823 entries and 26 branches**; `PhaseSpaceSimulation.root`
carries tree `PhaseSpaceTree` with 50 000 entries and the same 26 branches. MagnetUp adds the
remainder toward the record's stated 8.55 M total.

```
B_FlightDistance, B_VertexChi2                                        (double)
H{1,2,3}_PX, _PY, _PZ            three-momenta, MeV/c                 (double)
H{1,2,3}_ProbK, _ProbPi          PID likelihoods                      (double)
H{1,2,3}_Charge                                                       (int32)
H{1,2,3}_IPChi2                                                       (double)
H{1,2,3}_isMuon                                                       (int32)
```

**What this gives us.**
- Three full 3-momenta ⇒ any invariant mass pair, under any mass hypothesis ⇒ the Dalitz point.
- `Σ H_Charge` = the `B` charge ⇒ **CP conjugates separable event by event.** This is the one
  thing no other public source provides. **Verified** `[V]`: over the first 200 000 MagnetDown
  entries the charge sum is `±1` on every event, splitting 101 640 `B⁺` / 98 360 `B⁻`. That
  **3.3 % raw excess of `B⁺`** is not a physics asymmetry — it is production plus detection
  asymmetry, it is exactly the nuisance every CP measurement in this field must control, and it
  is a standing warning for us: **our conjugate-difference observable must be insensitive to a
  pure normalisation difference between the two samples, and the prereg must demonstrate that
  rather than assume it.**
- `ProbK` / `ProbPi` ⇒ we choose the final state ourselves: `K±K⁺K⁻`, `K±π⁺π⁻`, `π±π⁺π⁻`,
  `π±K⁺K⁻`. The physics benchmark for all four is LHCb PRD 90 (2014) 112004
  (arXiv:1408.5373), which measured large CP asymmetries in exactly these modes and studied
  them as functions of Dalitz position.
- Reconstructed `B` mass is computable from the momenta ⇒ **sideband background subtraction is
  possible and is entirely ours to do.**

**What it does NOT give us — and each of these is a named weakness the prereg must handle.**

1. **No efficiency map.** None, in any form. The Dalitz-plane acceptance of LHCb's trigger and
   selection is strongly non-uniform (it cuts on track `p_T`, momentum, IP χ², and `B` vertex
   quality), and it is **not** released.
2. **`PhaseSpaceSimulation.root` is NOT an efficiency map.** The record states in its own
   abstract that this file "has not been passed through a simulation of the detector response"
   `[V]` — it is a generator-level flat-phase-space reference. Using it as an efficiency proxy
   would be a fabrication.
3. **No background model, no sWeights, no MC truth.**
4. **The selection is documented in prose, not as a function.** We cannot invert it.

**Why the missing efficiency is the central methodological problem, not a footnote.** A
non-uniform acceptance across the Dalitz plane is a *multiplicative reweighting of the joint
density*. It generically **changes the pair marginals and the whole-only share together**, and
there is no reason for it to leave the share invariant. So an uncorrected share on this dataset
is a share of `efficiency × truth`, not of truth. **However** — and this is the reason the
dataset is still usable — the acceptance is to an excellent approximation **the same for `B⁺`
and `B⁻`** (LHCb's detector asymmetries are small and are the subject of their own dedicated
corrections). So the **CP-conjugate difference of the share** is far better protected than
either share alone. **That is an argument for making the difference the primary observable and
the absolute share a secondary, explicitly-caveated one** — and it is an argument that must
itself be tested, not asserted, because `GATES.md` reach 8 (probe polarity) and the sky
campaign's `directional claims are measured` gate both exist because we have previously argued
a direction from plausibility and been wrong in sign.

---

## 2. KLOE-2 `η → π⁺π⁻π⁰` — the only public 2-D binned Dalitz

| | |
|---|---|
| **record** | https://www.hepdata.net/record/ins1416990 `[V]` |
| **paper** | *Precision measurement of the η→π⁺π⁻π⁰ Dalitz plot distribution with the KLOE detector*, arXiv:1601.06985 `[V]` title from record |
| **Table 1** | `x_count = 2`, **371 values**, headers `X`, `Y`, `N/N₀`, each with a symmetric error `[V]` — fetched and parsed the table JSON myself |
| **binning** | `X` bin width 0.06451 (≈ 2/31), `Y` bin width 0.1, over the physical region `[V]` from the bin edges |
| **Tables 2–18** | 17 one-dimensional `Y`-slices `[R]` |
| **statistics** | ~4.7 × 10⁶ events, efficiency 37.6 %, S/B = 133 `[R]` |

**Critical caveats, all load-bearing.**

1. **The released values are `N/N₀` — normalised densities, background-subtracted and
   unfolded** `[V]` on the headers, `[R]` on the unfolding description. They are **not counts.**
   Every occupancy gate, every shot-noise floor, every multinomial null in our battery is
   defined on **counts**, and none of them can be applied to a density without reconstructing an
   effective count per cell. The stated per-cell symmetric errors are the only handle on that,
   and using them that way is an assumption to be pre-registered, not a free move.
2. **The acceptance-and-smearing matrix `S_ij` is described in the paper but not released**
   `[R]`. So the unfolding cannot be undone or varied — we inherit KLOE-2's unfolding choice
   with no ability to test its effect. This is a **`GATES.md` reach-6 exposure** (geometric
   artifact) with no available lever.
3. **`η` is its own antiparticle: there is no CP conjugate and no CP-difference measurement
   here.** What *does* exist is **C**: charge conjugation maps `π⁺ ↔ π⁻`, which on the Dalitz
   plane is `X → −X`. A C-conserving decay has a Dalitz density even in `X`, and KLOE and its
   predecessors measured the left-right, quadrant and sextant charge asymmetries and found them
   consistent with zero. **This makes the dataset a genuine theorem-pinned control rather than a
   CP measurement**: if the three slots are constructed so that `X → −X` acts as the *global*
   sign flip of all three bits, then `share_eq_zero_of_signSymmetric` (`Core/SignSymmetry.lean`)
   forces the symmetrized distribution's share to be **exactly zero**, and the measured share of
   the symmetrized data is then a pure read of our own pipeline's floor. Whether the slot
   construction can be made to satisfy that hypothesis is a **design obligation for the prereg**,
   not something to be assumed.

---

## 3. EVERYTHING ELSE — 1-D projections and fit parameters

**Spot-checked by me, all confirmed 1-D** `[V]`:

| record | mode | what it actually contains |
|---|---|---|
| [ins1289224](https://www.hepdata.net/record/ins1289224) | Belle `D⁰→K⁰_Sπ⁺π⁻` | 3 tables: `π⁺π⁻`, `K⁰_Sπ⁺`, `K⁰_Sπ⁻` mass distributions. 1-D. |
| [ins1086537](https://www.hepdata.net/record/ins1086537) | BaBar `B⁺→K⁺K⁻K⁺`, `B⁰→K⁺K⁻K_S`, `B⁺→K_SK_SK⁺` | 15 tables, all 1-D mass distributions — **but `B⁺` and `B⁻` are given separately** (Tables 4/5, 6/7). 1-D. |
| [ins853279](https://www.hepdata.net/record/ins853279) | BaBar `D⁰→K⁰_Sπ⁺π⁻`, `K⁰_SK⁺K⁻` | 6 tables, 1-D mass distributions. |
| [ins1376484](https://www.hepdata.net/record/ins1376484) | BESIII `η→π⁺π⁻π⁰`, `η,η′→3π⁰` | 4 tables: `X`, `Y`, `Z` distributions. **1-D only — no 2-D**, despite being the same decay KLOE-2 released in 2-D. |

**Reported and not independently verified** `[R]`: the same 1-D-only pattern for BESIII
`D⁰→K_{S,L}π⁺π⁻` (ins2615968), BESIII `D⁰→K_SK⁺K⁻` (ins1799437), LHCb `D⁰→K_SK±π∓`
(ins1394391), LHCb `D⁺→K⁻K⁺K⁺` (ins1720423), CLEO-c / FOCUS / E791 `D⁺→K⁻π⁺π⁺` (ins780363,
ins750701, ins585322), BaBar and BESIII `D_s⁺→π⁺π⁻π⁺` (ins792597, ins1909391), BESIII
`ω→π⁺π⁻π⁰` (ins1703033), LHCb `Λ_b⁰→J/ψpK⁻` (ins1728691). The BaBar `Kπ` S-wave record
(ins1403544) is **fit output, not data**.

**Reported to have NO HEPData record at all** `[R]` — and this list matters, because it is
exactly the set of papers whose physics we would most want to compare against:
LHCb arXiv:1306.1246, 1310.4740, **1408.5373** (the flagship phase-space CPV measurement),
1909.05211/1909.05212, 2206.02038, 2206.07622, 2208.03300; BaBar hep-ex/0408032; LHCb
1507.03414; KLOE 2008 (0707.2355); WASA-at-COSY; Crystal Ball/MAMI.

**Independent cross-check** `[R]`: a scan of the full Rivet analysis tree found 84 analyses
mentioning Dalitz plots and **exactly one** carrying 2-D reference data —
`KLOE2_2016_I1416990`, i.e. the KLOE-2 table above. Every other Dalitz analysis books a 2-D
histogram for Monte-Carlo output only, with 1-D reference data. This is consistent with the
HEPData picture and was reached by a different route, which is why it is worth recording.

---

## 4. BINNED DALITZ *MAPS* THAT ARE NOT DISTRIBUTIONS — the `(cᵢ, sᵢ)` programme

The `D⁰ → K⁰_Sπ⁺π⁻` strong-phase measurements (CLEO-c arXiv:1010.2817; BESIII arXiv:2002.12791,
2003.00091, 2007.07959) partition the Dalitz plane into bins of equal strong-phase difference
and report per-bin quantities. **None of these has a HEPData record** `[R]` (all four reported
404). What the papers themselves contain `[R]`:

- **CLEO-c** Tables 7–10: per-bin flavour-tagged **fractions** `F_i` (%) for four binning
  schemes — the per-bin yields in normalised form, not raw counts. Tables 13–17: `cᵢ`, `sᵢ`.
  Tables 25–38: correlation matrices.
- **The binning look-up tables themselves** — the actual `(m²_{K_Sπ⁺}, m²_{K_Sπ⁻}) → bin index`
  maps at 0.0054 GeV⁴ granularity — were **EPAPS supplementary material, not in the arXiv
  tarball**, and circulate as ROOT 2-D histograms inside analysis repositories. This is the
  closest public thing to a released 2-D Dalitz-plane *object* for this mode.
- **BESIII arXiv:2003.00091 Table 3** is a genuine **per-Dalitz-bin efficiency/migration matrix
  `ε_ij`** — released, in the paper only, coarse (Dalitz-bin granularity), one tag mode.

**Why this is nearly useless to us despite looking perfect.** These binnings have **of order 8
to 16 bins** across the whole plane, chosen to maximise sensitivity to `γ`, and the released
numbers are fractions rather than counts. Our instrument needs a **joint distribution on three
slots** at a resolution where occupancy is defensible; an 8-bin partition of a 2-D plane cannot
supply it, and the recent optimal-binning work (Bovill, Jurik & Malde, arXiv:2606.13948)
confirms that the field's binnings are Fisher-information-optimised for `γ`, not for anything
we want. **Recorded as understood and set aside, not as an untried option.**

---

## 5. EFFICIENCY AND ACCEPTANCE MAPS — essentially nothing is public

| source | efficiency information | status |
|---|---|---|
| LHCb open data 4900 | **none**; the phase-space file is generator-level and explicitly not detector-simulated `[V]` | unavailable |
| KLOE-2 ins1416990 | data are already unfolded; the smearing matrix `S_ij` is **not** released `[R]` | inherited, not variable |
| BESIII 2003.00091 | per-Dalitz-bin `ε_ij`, in the paper, coarse, one tag mode `[R]` | wrong resolution for us |
| every other record examined | none found `[V]` on four records, `[R]` on the rest | unavailable |

**This is the single largest gap in the inventory** and it is the reason the campaign's primary
observable should be a *difference between conjugates* rather than an absolute share.

---

## 6. THE FALLBACK, STATED EXPLICITLY BEFORE IT IS TEMPTING

Published amplitude models for all these modes are abundant: isobar and K-matrix fits with
released masses, widths, fit fractions and phases, and open fitters (`Laura++`, arXiv:1711.09854;
`VecAmpFit`, arXiv:2603.20066) that will evaluate them on a grid. It would be easy — a
day's work — to generate a high-statistics Dalitz density from a published model and measure its
whole-only share to arbitrary precision, with perfect knowledge of the efficiency (there is
none) and the background (there is none).

**If we do that, the following labelling is mandatory and non-negotiable:**

> A whole-only share computed from a published amplitude model's predicted density is a
> measurement **of that model**, not of the decay. It inherits every assumption of the isobar
> or K-matrix parametrisation, including the resonance content, the lineshapes, and the
> assumption that the amplitude is a finite sum of the terms someone chose to fit. It cannot
> falsify anything about nature, it cannot support any `measured` claim, and it may not be
> reported with a significance against a physical null. Its only legitimate uses are (a) as a
> **positive control** — checking that our instrument reads a nonzero share where a model with
> interference says structure exists — and (b) as an **advance prediction** to be tested later
> against data.

This mirrors the standing scope line on `CIRISArray`: our own designed substrate is not nature,
and a model's predicted distribution is not data.

---

## 7. RECOMMENDATION TO THE PREREG

**Primary target: LHCb open data record 4900**, mode chosen from the four available final
states, with the **CP-conjugate difference of the whole-only share as the primary observable**
and the absolute share reported as secondary and efficiency-caveated. Reasons: it is the only
dataset with the conjugation the campaign is about; it is event-level, so we control the binning
ladder and can compute counts (which every gate in the battery requires); and the missing
efficiency is common-mode between `B⁺` and `B⁻` to good approximation — an approximation the
prereg must then *test* rather than assume.

**Secondary target and theorem-pinned control: KLOE-2 ins1416990 Table 1.** It is the only
public 2-D binned Dalitz, it is efficiency-corrected, and its `X → −X` C-conjugation gives us
the sign-flip under which `Core/SignSymmetry.lean` forces an exact zero. It cannot carry the CP
headline, and it should not be asked to.

**Named as unavailable, so nobody looks again:** there is no public 2-D binned Dalitz
distribution with CP conjugates separated, for any charm or beauty mode. If we want one we build
it from record 4900.

---

## FILES

| | |
|---|---|
| `DALITZ_PRIOR_ART.md` | convergent-art adjudication (committed first) |
| this document | data inventory |
| `DALITZ_PREREG.md` | pre-registration (next, before any number) |
| `scratchpad/dalitz/data/` | downloaded LHCb open data — **not committed**, 1.1 GB |

Inventory compiled 2026-07-26. Primary-artifact verification (`[V]`) performed against the
CERN Open Data record API, direct HTTP HEAD on the data files, `uproot` on the phase-space file,
and the HEPData record and table JSON endpoints.
