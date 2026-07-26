# AMENDMENT 2 to SKY_REALDATA_PREREG.md — Stage 2 opening: mock count, and two defects

Committed **before the Stage 2 production run starts** and before any G10 verdict exists.
Nothing in this amendment was informed by a floor-versus-signal comparison; the real galaxy
catalogue remains unread and blinding remains code-enforced.

---

## A2.1 The mock count: 2048 → **128 per cap**, on a measured argument

**Measured cost**, after caching the geometry (the mask and its smoothed denominators come
from the randoms and are shared by every realisation, so they are built once per cap) and
after hoisting the valid-triple mask out of the `b` ladder:

| | per realisation |
|---|---|
| SGC (32.8 M-cell grid) | **26.4 s** |
| NGC (≈2× the volume) | ≈ 55 s |
| both caps, run in parallel | ≈ **55 s wall** |

**2048 realisations per cap is therefore ≈ 60 hours of wall time**, against an approved budget
of ~1 machine-day. The pre-registration's own estimate (~2 min/mock/scale, ~4 h on 32 cores)
was optimistic by an order of magnitude, and this is the measured replacement.

**Adopted: 128 realisations per cap, split 64/64 for the G10 closure test.**

**Why this clears §4.1's precision requirement — with a measured number, not the assumed one.**
§4.1 justified 2048 by "2048 realisations measure a floor to `1/√2048 ≈ 2.2 %` of its
per-realisation scatter", where the scatter was taken from the mock campaign at **≈ 13 %** of
the floor mean. The scatter on the real geometry is now measured and it is **ten times
smaller**:

> per-realisation scatter of `I_C⁽³⁾` = **0.5 – 1.1 %** of the floor mean
> (SGC, `R = 15` and `10`, `b = 4` and `6`, folded).

So the half-suite mean is known to `0.011/√64 ≈ **0.14 %** of the floor` at worst. Against a
G10 bar of **10 % of signal** — and even in the pessimistic case where signal ≈ floor — that
is **~70× inside the bar**. The 2048-realisation argument is not merely preserved at 128; it
is beaten by roughly an order of magnitude, because the quantity being averaged turned out to
be far more stable across realisations than the mock campaign suggested.

**The trade, stated rather than hidden:** 128 buys the *floor mean* to 0.14 % but samples the
*realisation-to-realisation distribution* 16× more coarsely than 2048 would. That matters for
anything requiring the floor's covariance or its tails — which G10 as pre-registered does not,
since it compares half-suite means. **If any later stage needs the covariance rather than the
mean, that stage requires its own amendment and more realisations.** The run writes
incrementally, so extending it is append-only and costs nothing already spent.

## A2.2 Defect: the x10 random suite is too sparse to define a footprint

Stage 1 was validated against the BOSS data randoms (16.6 M objects for SGC, ~50× the galaxy
density). The first Stage-2 run used the Patchy **x10** randoms — 3.4 M after veto, ~0.1
randoms per grid cell — and the mask degenerated to speckle: **the valid fraction collapsed
from 0.104 to 0.001 at `R = 15`**, and every occupancy gate failed for the wrong reason.

Fixed two ways, both adopted:

1. **The x50 Patchy random suite** (17.1 M after veto for SGC), which matches the data
   randoms' density — necessary anyway, because `δ = (n_g − αn_r)/(αn_r)` carries the
   randoms' shot noise in its denominator, and x10 against ~340 k mock galaxies is only 10×.
2. **The footprint is defined on a SMOOTHED random field** (Gaussian, 8 Mpc/h) rather than on
   raw deposited counts. That is what a footprint means, and it is independent of random
   sparsity. Thresholding raw counts was only ever valid because the data randoms happened to
   be dense.

Post-fix geometry, SGC: mask 0.302 of the grid, **valid 0.250 at `R = 15`** (`n_indep`
33 264), 0.266 at `R = 10` (`n_indep` 119 777).

## A2.3 The occupancy gate is applied PER CAP, and that is not a convenience

Pooling triple histograms across NGC and SGC would be averaging two distributions with
**different windows** — a mixture, and `ECA_SPIKE_RESULTS.md`'s correction block records that
mixtures manufacture higher-order structure from none. **Caps are therefore measured
separately and combined only at the level of summary statistics, never by pooling
histograms.** The occupancy gate is consequently per cap, and it can pass for NGC while
failing for SGC at the same `b`.

Measured, SGC: occupancy at `R = 15` is **520** (`b=4`), **154** (`b=6`), **65** (`b=8`) — so
**`b = 8` fails for SGC at the primary scale**, confirming Stage 1. NGC's larger volume may
pass it. The ladder stays `b ∈ {4, 6, 8}` as pre-registered and the gate decides per cap and
per scale; nothing is excluded by hand.

## A2.4 Nothing else moves

No gate threshold, no outcome criterion, no kill, no data choice, no statistic. G10 remains
the go/no-go at 10 % of signal on a held-out half. The §4.2 escape hatch to a denser tracer
remains contingent on G10 failing on density grounds.

---

*Amendment ends. The real galaxy catalogue remains unread; `measure_catalogue()` still raises
without `stage6_unblind=True`.*
