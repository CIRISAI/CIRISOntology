# STAGE 0 — **BLOCKED.** DESI's data host is unreachable from this machine.

Committed at the stage boundary. **Stage 0 is NOT complete**, and this document says so in its
title rather than reporting partial progress as progress.

**No DESI datum has been read. Every `[to verify]` in `SKY_BGS_PREREG.md` (`ca43208`) is still
`[to verify]`,** and none of the four Stage-0 rules (S0-A sample choice, S0-B disk scoping, S0-C
mock inventory, S0-D the extension scale `R★`) can be applied, because every one of them needs a
header this machine cannot fetch.

---

## S0.1 The blocker, diagnosed rather than asserted

`data.desi.lbl.gov` resolves and does not connect. All eight addresses behind it are on NERSC's
Spin load balancer, and every one refuses at the network layer:

| probe | result |
|---|---|
| DNS `data.desi.lbl.gov` | resolves to **8 addresses**, `128.55.206.106`–`.113` |
| `https://data.desi.lbl.gov/public/dr1/` | HTTP **000**, curl exit **7**, `No route to host` on all 8 |
| same over plain HTTP, port 80 | **000** |
| same **with the sandbox disabled** | **000**, exit 7 — *so the sandbox is not the cause* |
| raw TCP to `128.55.206.106:443` | `No route to host` |
| `https://portal.nersc.gov/cfs/desi/` (same Spin block) | **000** |
| retried after ~15 min | **000** — not transient |

**Controls, run in the same session, to show the machine's network is otherwise healthy:**

| host | result |
|---|---|
| `data.sdss.org` (the BOSS source) | **200** |
| `datalab.noirlab.edu` | **200** |
| `astroarchive.noirlab.edu` | **200** |
| `zenodo.org` | **200** |
| `www.nersc.gov` | **200** — but it is Cloudflare-fronted (`2606:4700::…`), **not** in the Spin block |

**Conclusion: the subnet `128.55.206.0/24` is unroutable from this host, and that subnet serves
all DESI public data.** The failure is `No route to host` from `192.168.50.8`, i.e. an ICMP
host-unreachable from the local side — consistent with a firewall or routing rule on this
network rather than with an outage at NERSC. **This is very likely fixable at Eric's end, and it
is the single thing standing between this campaign and Stage 1.**

## S0.2 The one alternative route, checked, and it does not carry what is needed

NOIRLab's Astro Data Lab is reachable and does host DESI DR1. **It hosts the wrong products.**

Queried over its TAP service (`TAP_SCHEMA`), the `desi_dr1` schema contains 17 tables:
`exposure`, `fiberassign`, `frame`, `photometry`, `potential`, `target`, `tile`, `zpix`,
`ztile`, `agngal`, `mws`, `emfit`, and five cross-match tables.

**What is absent, and each absence is individually fatal:**

* **No LSS catalogues.** There is no `LSScats` product of any version.
* **No randoms.** The randoms **are** the selection function. `δ = (n_g − αn_r)/(αn_r)` cannot
  be formed without them, and this programme's own history is a list of footprint defects: the
  withdrawn Stage 2 run was wrong by 8–15× from a too-permissive footprint, the x10 random suite
  was too sparse to define one at all, and the mask-threshold rule was meaningless on the grid.
  **Building a selection function by hand for a survey whose own randoms I cannot download is
  the most dangerous thing this campaign could do**, and `SKY_REALDATA_PREREG.md` §7.6 already
  names an undisclosed veto mask as a VOID condition.
* **No LSS weights.** `desi_dr1.zpix` carries 107 columns; a case-insensitive search for
  `weight`, `random`, `frac`, `bitweight` returns exactly one hit, `random_id`, which is Data
  Lab's own row-shuffling key. There is no `WEIGHT_COMP`, no `WEIGHT_SYS`, no `WEIGHT_ZFAIL`, no
  `FRACZ_TILELOCID`, no bitweights. **§8's GATE W and GATE W′ are both undischargeable here** —
  W′ needs a per-object completeness column and there is none.
* **No `n̄(z)`**, so RULE S0-A cannot choose between `BGS_BRIGHT` and `BGS_BRIGHT-21.5`, and
  RULE S0-D cannot evaluate `n̄V_R` to fix `R★`.
* **No mocks of any kind.** Neither AbacusSummit nor EZmock, cutsky or cubic.

`zpix` is a **redshift catalogue** — `ra`, `dec`, `z`, `zwarn`, `spectype`, `bgs_target`,
`healpix`, TSNR columns. It is the right raw material for a redshift survey and the wrong raw
material for a clustering measurement.

**Zenodo was searched** for a mirror of either the DR1 LSS catalogues or the DR1 cutsky mocks.
Neither exists there; the DESI-related deposits are papers' plot data, likelihood products and
specialised value-added catalogues (peculiar-velocity, white dwarfs, stellar).

## S0.3 The mock situation, answered as honestly as it can be from here

The commission asked for the DR1 mock situation reported honestly, including whether the
128-per-cap floor-precision argument transports. **The honest answer has two parts and the first
one governs:**

1. **I could not inventory the DR1 mocks, because they are only distributed from the host that
   is unreachable.** Every statement in `SKY_BGS_PREREG.md` §6.2 — that AbacusSummit cutsky
   exists at ~25 realisations, that EZmock exists at ~1000, that either covers BGS in the
   *public* DR1 release — **remains `[to verify]` and I am not going to launder it into a
   finding.** §6.2 already recorded that public BGS cutsky availability is the thing I am least
   sure of, and it is still the thing I am least sure of.

2. **The transport argument itself does not need DESI to be stated, and it is stated.** The
   "128 per cap" figure was never load-bearing: Amendment 2 measured the per-realisation scatter
   of `I_C⁽³⁾` at **0.5–1.1 % of the floor mean**, and *that* is why 128 cleared the G10 bar with
   ~70× margin. The argument transports to any suite size `n` with `0.011/√n` inside the bar —
   satisfied at `n = 25` (0.22 %) and even `n = 8` (0.39 %) — **conditional on the scatter being
   comparable on DESI geometry**, which RULE S2-A measures before any suite size is committed.
   **The `σ` job does not transport the same way**: `σ` from 25 draws is uncertain by ±14 %, and
   BOSS's ±18 % from 16 draws is already a recorded weakness of the priors of record. So a
   25-realisation N-body suite would be **sufficient for the floor and the prediction, and
   insufficient on its own for the significance** — which is exactly what RULE S2-B's cross-suite
   σ closure was written to handle.

**No verdict is offered on whether DR1's public mocks can support the campaign. That verdict
requires reading a directory this machine cannot reach.**

## S0.4 What was done instead — the prerequisite that needed no data

The mission requires the first seven harvest gates to be **mechanized in the driver**. That work
needs no survey data, and it is the highest-value carry-forward, so it was done: **`bgs_gates.py`**,
with `require_discharged()` that reads artifacts off disk and **raises**.

It was then put through the docimasia `GATES.md`'s lifecycle section demands and which that
document says this repository most often skips — a **plumb line** (a stored kept taint the gate
catches) and a **dye test** (a known-true reference it passes). Three of the four views are real
states of the BOSS campaign, stored in this repository:

| gate | pre-A5 | as shipped | +refuter | known-good | state |
|---|---|---|---|---|---|
| **P1** valve floor | **FIRE** | PASS | PASS | PASS | **VALIDATED** |
| **P2** null-construction sweep | **FIRE** | **FIRE** | **FIRE** | PASS | **VALIDATED** |
| **P3** directional claims measured | ABSENT | **FIRE** | **FIRE** | PASS | **VALIDATED** |
| **P4** dispersion sweep | ABSENT | ABSENT | PASS | PASS | **VALIDATED** |
| **P5** same null both sides | ABSENT | ABSENT | ABSENT | PASS | **VALIDATED** |
| **P6** outcome completeness | ABSENT | ABSENT | ABSENT | PASS | **VALIDATED** |
| **P7** gate discharge before unblind | **FIRE** | **FIRE** | **FIRE** | PASS | **VALIDATED** |

`require_discharged()` on the BOSS state **as actually shipped at its unblind** raises with six
undischarged prerequisites. That is the correct behaviour and it is the whole point: **that run
was allowed to unblind.**

### Four findings from the docimasia, none of them flattering

1. **The docimasia caught a bug in my own gate, which is what it is for.** P3 initially
   **cleared** the shipped BOSS state, because that run records eight clipped fractions
   (0.3682, 0.3689, 0.3696, …) and counting distinct values read eight draws of *one*
   construction as a varied mechanism. **Realisation jitter was being scored as variation.** P3
   now clusters values and requires ≥3 separated levels spanning ≥1.5×; it fires on the shipped
   state at "1 distinct level spanning ×1.00 (8 raw values)".

2. **P2 fires on the post-refuter state too, and that is correct, not a bug.** The refuter ran
   its second null family on the **four folded primary rows**, not on all 26. **Twenty-two of
   the twenty-six published rows carry a single null construction to this day** — a fact that is
   in neither results document.

3. **P4 independently reproduced the refuter's number by computing it rather than reading it.**
   Given only the sweep, the gate returns `ε_crit` in **0.00–0.85** against the refuter's
   reported **0.63–0.85** (the 0.00 is the `R = 15` row the refuter reported as "already < 5 σ"),
   with measured `κ` = 1.129 NGC / 1.152 SGC.

4. **P5 and P6 have never passed on any real state of the record.** No BOSS artifact carries a
   null-construction signature, and none carries an outcome tag. Their known-good reference is
   synthetic, which is honest and is labelled — they are new machinery, and machinery that has
   never run on a real campaign is not yet evidence about one.

---

## S0.5 STATE, and what unblocks it

| stage | status |
|---|---|
| **prereg** | **COMPLETE**, committed `ca43208` before any download attempt |
| **0 inventory** | **BLOCKED** — DESI host unroutable; no rule applied; every `[to verify]` still open |
| **driver / P1–P7** | **COMPLETE and VALIDATED** (`bgs_gates.py`, `bgs_gates_docimasia.log`) |
| 1 pipeline adaptation | not started — needs DR1 column names, which need the host |
| 2 floor + G10 | not started |
| 3–7 | not started |

**Three things would unblock this, in order of cost:**

1. **Open routing to `128.55.206.0/24`** from this host. Then Stage 0 runs in about an hour and
   the campaign proceeds as pre-registered. **This is a network change on Eric's side and is very
   likely the whole fix.**
2. Fetch the DR1 BGS LSS catalogues, randoms and one mock suite from a machine that *can* reach
   NERSC, and place them in `/home/emoore/skydata`. Stage 0 would then read headers locally. Note
   the disk constraint is real and unchanged: **43 GB free**, with RULE S0-B's 35 GB scoping
   trigger already fixed in the pre-registration.
3. Abandon DESI and confirm on a different independent survey that is reachable. **No such
   survey has been identified**, and nothing in this document recommends one — that choice would
   need its own pre-registration and it is not the author's to make.

**No amendment to `SKY_BGS_PREREG.md` is proposed.** Nothing in it has been contradicted; it has
simply not been executed. The disk figures, the priors of record, the twelve prerequisites and
all four Stage-0 rules stand exactly as committed.

---

*Stage 0 ends here, blocked. No DESI datum has been read, and none was reachable to read.*
