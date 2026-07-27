# WATER — ARM A, THE DOCIMASIA: the mW instrument, examined before it reads anything

**Stage 2 of the water campaign**, pre-registered in `WATER_PREREG.md` §11 and §4.3 (P5) and run
**before any share was computed on any configuration**. The only quantities here are **density**
and **`g(r)`** — pair and thermodynamic quantities this instrument is blind to by construction —
and an engine-availability check. **No share, and no campaign observable of any kind, is computed
in this document.**

**Why arm A first.** `WATER_PREREG.md` §7 fixes the order A → B → C → D deliberately: **the two
arms that can kill the campaign's premise cost nothing**, so they run before the expensive ones.
Arm A is the three-body **dose** (P5), and its failure fires **K1**, which takes down the campaign
and stops any atomistic water arm from being worth starting.

---

## 1. THE ENGINE — obtained, and the obstacle recorded

| | |
|---|---|
| engine | **LAMMPS 20250722**, `pip install lammps` (85.8 MB wheel), no root |
| obstacle | the wheel links `libmpi.so.12` (MPICH), absent on this box. `pip install mpich` (13.2 MB) supplies it but installs to `<venv>/lib`, **not** on the loader path — so every invocation needs `LD_LIBRARY_PATH=<venv>/lib`. Recorded because it cost two failed starts and will cost the next person the same |
| verified | `pair_style sw` present (`has_style('pair','sw') → True`) |

**A second obstacle, recorded rather than silently patched:** `compute rdf` at an 8 Å cutoff
exceeds the ghost-atom range, because the SW cutoff is only `1.8 σ = 4.31 Å`. Fixed with
`comm_modify cutoff 12.0`. A short-ranged three-body potential does not automatically give you a
communication shell wide enough to *measure* structure at the range the campaign's templates need
— and this campaign's far arm sits at 7 Å or beyond.

## 2. THE MODEL — parameters are Molinero & Moore's and are not fitted here

mW (**Molinero & Moore, JPCB 113:4008 (2009)**): `ε = 6.189 kcal/mol`, `σ = 2.3925 Å`, `a = 1.8`,
**`λ = 23.15`**, `γ = 1.2`, `cos θ₀ = −1/3`, `A = 7.049556277`, `B = 0.6022245584`, `p = 4`,
`q = 0`. **`λ` is the only parameter this campaign moves.**

## 3. THE EXAMINATION — three checks, all PASS

`N = 2000`, `dt = 5 fs`, 20 000 steps equilibration + 20 000 production, NPT at 298 K / 1 atm.

| | check | result | verdict |
|---|---|---|---|
| **G1** | density reproduces the published **0.997 g/cm³** | **1.0023 g/cm³**, `+0.53 %` | **PASS** |
| **G2** | `g(r)` shows a tetrahedral network, not close packing | peak₁ **2.86 Å** (g = 2.08), min **3.50 Å** (g = 0.84), peak₂ **4.50 Å** (g = 1.18) | **PASS** |
| **G3** | `λ = 0` is a *different liquid* — the three-body term gone | **2.4090 g/cm³**, `2.40 ×` denser; peak₂/peak₁ = **1.913** | **PASS** |

**G1 is the sharpest of the three** because `0.997 g/cm³` is a number mW was *parameterised* to
hit: failing it would mean the implementation is wrong, not that the model is.

**G2 carries a quantitative signature, not just two peaks.** The measured
`peak₂/peak₁ = 4.50/2.86 = 1.573` against the **ideal tetrahedral ratio
`2·sin(109.47°/2) = 1.633`** — 3.7 % below it, which is what thermal disorder in a liquid does to
a perfect network. **And it independently confirms this campaign's primary template geometry**:
`WATER_PREREG.md` §3 fixed the tetrahedral template's third edge at
`4.573 Å = 2 × 2.80 × sin(109.47°/2)` from the tetrahedral angle, before any simulation existed.
The mW liquid puts its second shell at **4.50 Å**. The template was not fitted to this and agrees
with it to 1.6 %.

## 4. WHAT G3 MEASURED THAT CHANGES THE SWEEP — and it is not a caveat

**At the same temperature and the same pressure, removing the three-body term makes the liquid
2.40 × denser.** That is the whole physics of the model — tetrahedral open packing versus
close packing — and it has a consequence for P5 that this gate has now quantified:

> **The `λ` sweep must be run at MATCHED DENSITY (NVT), never at matched pressure (NPT).** Under
> NPT the density would move by a factor of **2.4** across the sweep, and the share would track
> *density* rather than `λ` — G-DOSE (`WATER_PREREG.md` §5.5) in its sharpest possible form,
> with the nuisance varying by more than the driver plausibly does.

`WATER_PREREG.md` §4.3's P5 already says *"at matched density and matched reduced temperature"*.
**This gate is what makes that phrase load-bearing rather than decorative**, and it is the reason
to have run the examination before the sweep rather than after: had the sweep been run under NPT
because NPT is the natural default, the result would have been a large, clean, entirely spurious
`λ` dependence.

**Stated in advance, since it follows:** at matched density `ρ = 1.0 g/cm³` the `λ = 0` liquid sits
at a large **negative** pressure — it is being held open at a density its own potential does not
want. That is legitimate in NVT and it is what "matched density" costs. It is disclosed here, and
the pressure at every `λ` will be reported in `WATER_RESULTS.md` beside the share.

## 5. WHAT THIS DOCUMENT DOES NOT ESTABLISH

1. **No share has been computed.** Not on mW, not on anything. P5 is unrun and K1 is unfired.
2. **The docimasia is on published properties only**, so it establishes that the engine and the
   model are what they claim to be — nothing about whether the *campaign's* observable behaves.
3. **`N = 2000` and 100 ps windows** are gate-sized, not measurement-sized. The design sensitivity
   of `WATER_PREREG.md` §6 (`3 × 10⁻⁵` nats, 200 independent configurations) applies to the sweep,
   not to this.
4. **Nothing bears on `wild-share`**; `Stance.lean` untouched; no Lean file opened; `lake` not run;
   nothing pushed.

## 6. FILES

| | |
|---|---|
| `water_mw.py` | the arm A instrument; `--gate` is this document's examination |
| `water_mw_gate.json` | its output, including both full `g(r)` curves |

Primary seed **20260727**.
