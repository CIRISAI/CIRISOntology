# PRE-REGISTRATION — pricing the *flow* (maintenance) reading of dark energy

**Status: scratchpad study. Wager-tier pricing exercise. NOT a stance change. No Lean
touched, no `lake` run, no push.**

Frozen and committed **before** any number in the results document was computed. The
companion artifacts will be `flow_pricing.py` (all numerics) and `FLOW_PRICING_RESULTS.md`
(the report). Nothing numeric in the results will be hand-copied.

**Honesty declaration about this prereg.** During task scoping an order-of-magnitude
envelope was worked by hand — enough to know roughly which decade the answer sits in, not
enough to know any tabulated value. The decision thresholds in §6 are therefore chosen from
*physical* arguments (independent clocks and bounds that exist in the problem regardless of
the answer), and I state that reasoning inline so a reader can check that they were not
drawn around a known result. Everything in §7 (the failure modes) was written before any
script existed.

---

## 1. What is being priced, and how it differs from the thing already killed

The predecessor study `scratchpad/temporal-share/DE_LEDGER_MODEL.md` priced a **STOCK**:

```
    rho_DE  =  N_total * kB * T * ln2                      (STOCK — already killed, K4)
```

and it failed by 3–5 orders of magnitude for every self-consistent pairing of a bit count
`N` with a temperature `T`. It reached the observed value only in Gough's pairing, which
multiplies the *radiation field's* bit count by the *gas's* temperature — two different sets
of degrees of freedom. That kill has fired and is not re-litigated here.

The reformulated wager prices a **FLOW**:

> Dark energy is the universe's maintenance bill: the Landauer cost, per unit volume per
> unit time, of the error correction that keeps existing pattern from decaying.

The motivation is internal and is the one honest thing the reformulation has going for it:
`Core/Maintenance.lean` prices maintenance against decay, not storage, and Landauer prices
*erasure*, not storage. An idealised stored bit is free; each **correction** is an erasure.
So the object to price is a power density, not an energy density.

### 1.1 The dimensional bridge — stated explicitly, and flagged as an IMPORT

Maintenance is a **power** density (W/m³). Dark energy is an **energy** density (J/m³). The
bridge asserted by the wager:

> A constant `rho_Lambda` occupying an expanding volume `V ∝ a³` holds a total energy
> `E = rho_Lambda V` that grows as `dE/dt = 3 H rho_Lambda V`. Read that as a required power
> input per unit volume, `P = 3 H rho_Lambda`.

Hence the prediction to be tested:

```
    rho_DE  =  P / (3H),        P  =  N_maint * lambda * kB * T * ln2        (FLOW)
```

with `N_maint` the number of *actively maintained* bits per m³, `lambda` the maintenance
(error-correction) rate, `T` the temperature of the reservoir the erasure heat enters.

**B1 [IMPORTED — load-bearing, and the flow picture's analogue of the stock picture's A5].**
General relativity does **not** require this power input. Covariant conservation
`d(rho)/dt = -3H(1+w)rho` makes `rho` constant at `w = -1` with no source at all: the
negative pressure does the work, and GR has no global energy conservation law that would
forbid it. The step `P = 3 H rho_Lambda` is therefore an *interpretation* — the claim that
the constancy is **maintained** rather than automatic — not a derivation. It is imported,
exactly as A5 was, and it is recorded here so it cannot be laundered later.

**B2 [DEFINITIONAL, and NOT the only option].** `rho_DE = P/(3H)` is a third distinct
identification, and I record the alternatives so the choice is visible:
- *stock*: `rho_DE = N kB T ln2` (the record's energy **is** the dark energy) — killed;
- *rate-matched*: maintenance power equals the record's decay power, `P = lambda rho_rec`,
  which returns `rho_rec = N kB T ln2` — algebraically **identical to the stock model**;
- *flow* (this study): `rho_DE = P/(3H)`.

Only the third has any chance of differing from the killed model, and §2 states by exactly
how much it can differ.

---

## 2. THE FIRST DELIVERABLE — the collapse test, stated before it is run

Dividing the flow formula by the stock formula, at fixed `(N, T)`:

```
    rho_DE(flow)  /  rho_DE(stock)   =   lambda / (3H)
```

**The entire content of the reformulation is the single factor `lambda/(3H)`.** Therefore:

- If `lambda = H`, the flow answer is the stock answer divided by three, and the
  reformulation inherits the stock model's 3–5 dex failure intact, *worsened* by 0.5 dex.
- The flow picture helps **only** if `lambda >> H`, and it must supply the whole shortfall:
  the required rate is
  ```
      lambda / H0  =  3 * rho_DE / (N * kB * T * ln2)   =   3 / f,
      f  ==  (stock energy density at that N,T) / rho_DE
  ```
  i.e. **required `lambda/H0` = 3 × (the stock model's shortfall factor)** at the same
  `(N, T)`.

First deliverable: that number, for every defensible `(N, T)`.

**A consequence to state now, because it pushes the answer the wrong way.** The flow picture
must count only *maintained* bits. `N_maint <= N_total` necessarily, and plausibly
`N_maint << N_total` (most entropy is not error-corrected anything). Every reduction of `N`
raises the required `lambda` proportionally. The reformulation's own physical discipline
therefore makes its arithmetic problem **worse**, not better. Any rescue of the form "each
decayed bit needs `m` correction operations" is algebraically a rescue of the form
`N -> mN`, and is therefore a demand for exactly the bits the stock model already failed to
find. The failure, if it occurs, is closed under that class of rescue.

---

## 3. Candidate `N_maint` (bits per m³) — the full list, to be defended or rejected

Each will be defended or rejected in the results, and *no candidate may be silently
dropped*.

1. **Stellar baryons only** — bits carried by matter locked in stars.
2. **All baryons** — one bit per baryon, and the thermodynamic-entropy count of the gas.
3. **CMB photons** — computed directly from `s = (4/3) a_rad T³ / kB`, not taken from a table.
4. **Non-CMB (starlight + dust) photons** — Gough's radiation-field count, ~10⁸⁶ in the
   observable universe.
5. **Holographic / horizon bound** — `A / (4 l_P² ln2)` on the Hubble horizon.
6. **Stars and gas from Egan & Lineweaver's entropy budget** (arXiv:0909.3983), converted to
   a density.

**A volume-consistency check is pre-registered as mandatory**, because the predecessor study
may have made an error here: Egan & Lineweaver quote totals within the *particle horizon*
while the K4 table compared them against an energy computed in the *Hubble volume*. Those
differ by more than a decade in volume. This study will work **entirely in densities**, will
recompute the CMB entropy density from first principles, and will report the volume implied
by E&L's own CMB total as a cross-check. If the predecessor's shortfalls move, that is
reported as a correction to the predecessor, whichever way it moves.

---

## 4. Candidate `T` — the same discipline

**The correct `T` is the temperature of the reservoir the erasure heat is dumped into**, and
it must belong to the same physical system whose bits are being counted. Pairing `N` from
one system with `T` from another is precisely the error that produced the published
agreement, and any pairing that does it will be labelled **ILLEGITIMATE** in the table and
excluded from the verdict, however well it scores.

Candidates: CMB 2.7255 K; dust re-emission ~30 K; stellar surfaces / starlight ~5×10³ K;
warm IGM ~10⁶ K; hot IGM / WHIM ~10⁷ K; de Sitter horizon `T_dS = hbar H / (2 pi kB)`.

Legitimate pairings (system's own bits at its own temperature) will be marked; the
Gough pairing (photon `N` at gas `T`) will be carried in the table explicitly labelled as
the illegitimate control.

---

## 5. Pre-registered additional legs

These are stated now so that they cannot be presented later as post-hoc rescues or post-hoc
attacks.

**L1 — the `lambda` consistency test.** `lambda` in the flow formula and `lambda` in
`Core/Maintenance.lean`'s ledger are **the same parameter**: `rent_holds` says an entry is
held steady when the payment equals the decay, so in steady state the maintenance rate *is*
the decay rate. The predecessor study measured that decay rate against DESI DR2 from the
*shape* of `w(z)`: `lambda_shape = 1.67 H0`, 68% interval `[1.33, 2.02] H0`. The magnitude
leg computed here yields `lambda_mag`. **Pre-registered criterion: if `lambda_mag` and
`lambda_shape` disagree by more than a factor of 10, the model is internally inconsistent —
it requires one symbol to take two values in one equation — and that is a kill.** Factor 10
is chosen because the shape fit's own interval is a factor 1.5 wide and the `(N,T)` menu
spans about a decade of defensible choices; a factor of 10 is generous to the model.

**L2 — the free-energy budget.** The flow picture demands that `P` be *supplied* and then
*dissipated*. Integrated over a Hubble time the demand is `P t_H ≈ 3 rho_DE`, a fixed
multiple of the critical density, independent of `N`, `T` and `lambda`. It will be compared
against: (i) the total matter energy density `Omega_m rho_crit c²`; (ii) a rigorous upper
bound on the power star formation can deliver, `psi_MD14(0) × 0.007 c²` (every gram formed
burned instantly at full hydrogen-to-helium efficiency), using the already-verified MD14
eq. 15 normalisation. **If the required power exceeds the available free energy, the kill
fires and it fires independently of every parameter choice in §3 and §4.**

**L3 — the waste heat.** The erasure heat must appear in the reservoir. For the CMB
reservoir the injection will be expressed as a Compton-`y` distortion and compared to
COBE/FIRAS (`|y| < 1.5e-5`). For the IGM reservoir it will be compared to the IGM's actual
thermal energy density. For the de Sitter horizon reservoir it will be compared to the
horizon entropy. **A reservoir that cannot absorb the heat without an already-excluded
observational signature is a kill for that pairing.**

**L4 — rate bounds (task 5).** The required `N lambda` operations per second per m³ will be
checked against the Margolus–Levitin bound `nu <= 2E/(pi hbar)` evaluated on the energy
actually present, and against the fastest physical clocks available in each system. **A
required rate exceeding the bound is a hard kill.** Recorded in advance: because both the
Bekenstein–Hawking entropy and the Gibbons–Hawking temperature are built from the same
constants, the holographic/de Sitter pairing is *expected* to sit at the Margolus–Levitin
bound to within a pure number made of `2π`, `4`, `ln2` and `π`. If it does, that is evidence
the pairing is a **thermodynamic identity carrying no maintenance content**, not evidence
the model works. This is written down now precisely so that outcome cannot be claimed as a
success later.

**L5 — `w(z)` under the flow reading.** The flow model predicts `rho_DE ∝ n(t)/H(t)`, where
`n` is the maintained stock obeying the ledger `dn/dt = Y psi(t) - lambda n(t)`. This is
**not** the stock model's `rho ∝ n`: there is an extra `1/H`. Since
`w = -1 - (1/3) dln rho / dln a`, the flow model's `w` differs from the stock model's by
`+(1/3) dlnH/dlna`, which is negative, so the flow reading is **more phantom** at every
redshift. Predicted in advance: this moves the model *away* from the DESI supernova
combinations, which already sat 2.0–2.7σ off in `w_a`. `DE_LEDGER_MODEL.py`'s solver, DESI
DR2 BAO data, and CMB-lite likelihood will be reused unchanged, with only the density
mapping altered.

---

## 6. Decision thresholds for `lambda`, fixed now

Chosen from clocks that exist in the problem, not from the envelope:

| required `lambda/H0` | meaning |
|---|---|
| `< 10` | **the `lambda ≈ H` regime.** The reformulation buys nothing; it is the stock model divided by three. Outcome (d). |
| `10` – `10³` | mild hierarchy. Survivable **only if** the implied timescale `1/lambda` coincides with an independent, named physical clock of the same system whose bits are counted — not merely "an astrophysical timescale exists near there". |
| `> 10³` | strong hierarchy. Requires a named clock at that rate **and** must still pass L1–L4. |
| exceeding L4's bound | hard kill regardless of everything else. |

The "named clock" requirement is the load-bearing part of this table, and it is deliberately
strict: the space of astrophysical timescales is dense, so *finding* a process near the
required rate is not evidence. The model must have predicted the clock.

---

## 7. Pre-registered outcomes — the meaning of every possible answer

- **(a) SURVIVES.** A defensible `(N, T, lambda)` triple exists: `N` and `T` from the same
  degrees of freedom, `lambda` matching a named clock of that same system, consistent with
  `lambda_shape` to within a factor of 10 (L1), affordable (L2), with absorbable waste heat
  (L3), under the rate bound (L4). → the wager survives its first pricing and phase 2 is
  worth building.
- **(b) HARD KILL ON RATE.** Required `lambda` exceeds a physical bound. → reported loudly;
  the flow reformulation is dead on physics, not on taste.
- **(c) SAME FAILURE MODE AS THE STOCK MODEL.** The target is reached only for an `N` or `T`
  that cannot be justified, or only by pairing degrees of freedom that do not belong
  together. → reported as *the identical error the predecessor diagnosed*, now one level up.
- **(d) EMPTY REFORMULATION.** `lambda ≈ H` comes out required. → the flow picture collapses
  back to the stock model and inherits its fired kill; nothing was bought.
- **(e) INTERNAL INCONSISTENCY (L1).** `lambda_mag` and `lambda_shape` are the same symbol in
  the same equation and disagree by more than a factor of 10. → the model cannot be made
  self-consistent; magnitude and shape cannot both be right.
- **(f) BUDGET / WASTE-HEAT KILL (L2, L3).** The required power is unavailable, or the heat
  is not where it would have to be. → parameter-independent kill; the strongest available
  verdict, because it does not depend on any choice in §3 or §4.

**More than one of (b)–(f) may fire, in different regimes of the table. All that fire will
be reported, with the regime each applies to.** A single surviving cell does not rescue the
model if it survives only by an illegitimate pairing.

**Stated expectation, so there is no temptation to rescue: this is expected to fail.** A
clean, well-diagnosed failure is the deliverable. No parameter will be tuned to reach the
answer. What is *required* will be reported, and then judged.

---

## 8. Inputs fixed now

| quantity | value | source |
|---|---|---|
| `H0` | 67.4 km/s/Mpc | Planck 2018; the value already used by `DE_LEDGER_MODEL.py` |
| `Omega_Lambda` | 0.6847 | Planck 2018 TT,TE,EE+lowE+lensing |
| `Omega_m` | 0.315 | Planck 2018 |
| `Omega_b` | 0.0493 | Planck 2018 (`omega_b h² = 0.02237`) |
| `Omega_*` | 0.0027 | Fukugita & Peebles 2004 — **flagged: from memory, ±50 %** |
| `T_CMB` | 2.7255 K | Fixsen 2009 |
| SFH | MD14 eq. 15, `psi(0) = 0.015` | verified from the arXiv PDF by the predecessor study |
| entropy budget | E&L 2010 §2.1, Table 1 | verified from the arXiv PDF by the predecessor study |
| `lambda_shape` | `1.67 H0`, 68 % `[1.33, 2.02] H0` | `DE_LEDGER_MODEL.md` §4 |
| FIRAS | `|y| < 1.5e-5`, `|mu| < 9e-5` | COBE/FIRAS — **flagged: from memory** |
| DESI DR2 | `w0`,`wa` per combination; BAO Table IV | verified from the arXiv PDF by the predecessor study |

Any number entering the verdict that is flagged "from memory" must be shown not to change
the verdict at an order of magnitude, or the verdict must be withheld.

Numerics: numpy 2.5.1 / scipy 1.18.0 in `scratchpad/temporal-share/qenv`.
