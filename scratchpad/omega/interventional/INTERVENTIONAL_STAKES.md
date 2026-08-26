# INTERVENTIONAL SIGNATURE — stakes, written before `interventional.py` exists

*2026-08-26. Theory: `INTERVENTIONAL_SIGNATURE.md` (written first). This file freezes the
planted-truth validation and its adjudication before a line of instrument code is written.
Everything below is synthetic: the truth is planted by construction, so the stakes are a
test of the INSTRUMENT, not of nature. Nothing here licenses a claim about the world.*

## Disclosure, first, because the discipline requires it

Two things were seen before this file was written and must be declared:

1. **The head of `scratchpad/composition/s2/arm_K.csv` was read** (frames 240–258). The
   first recorded row is `div_px = 1.9209e-3`, `div_pos = 1.2261e2` — **not zero**, at the
   frame the probe is applied, where §4.3 of the theory note says a deterministic twin pair
   must read exactly zero. So the engine reading below is not blind to the existence of a
   pedestal. What is NOT yet known, and is what §E stakes, is the pedestal's size relative
   to the B4 window and whether B4's `K = 1.0012` survives its subtraction.
2. **The mechanism of COMPOSITION-2's misses is known** (its RESULTS file). The synthetic
   cases below are designed to reproduce that mechanism, not to discover it.

## Frozen instrument parameters

Fixed now, not tuned later. Any change is an amendment with its own file.

| parameter | value |
|---|---|
| local map | logistic `f(u) = 4u(1−u)` on `[0,1]` |
| sector size | `L = 16` sites, periodic ring |
| diffusive coupling within a ring | `ε = 0.3` (`u_i ← (1−ε) f(u_i) + (ε/2)(f(u_{i−1}) + f(u_{i+1}))`) |
| cross-sector link | one-way, `driven_0 ← (1−c)·(ring update) + c·f(driver_15)`, `c = 0.4` |
| burn-in before probe | `t0 = 500` steps |
| response window | `1500` steps after the probe |
| small probe | `x_p ← reflect(x_p + 1e-6)`, site `p = 8` |
| large probe (distributional arms) | amplitude `0.4`, site as named per case |
| sham probe | amplitude `0`, i.e. `δ = id` |
| view | `v(u) = (u > 0.5)` per site — a 16-bit coarse reading of the sector |
| raw response | `R_raw(t) = max_i |u'_i(t) − u_i(t)|` |
| view response | `R_view(t) = Hamming(v(u'(t)), v(u(t)))` |
| noise (stochastic cases) | additive `σ = 1e-3`, drawn ONCE into an array indexed `[t, sector, site]` and consumed in that order — **A-blind by construction** (theory §4.1) |
| boundary handling | reflect at 0 and 1 (`u<0 ↦ −u`, `u>1 ↦ 2−u`) |
| observational comparison series | `24000` steps (matching the engine's frame count) |
| seeds | `20260826` and derived; every case fixed and recorded |

## The light-cone predictions, staked as exact integers

The lattice has interaction radius 1, so the response front moves exactly one site per
step. With the probe at site 8 and the cross-link leaving from site 15 of the driver into
site 0 of the driven sector, the ring distance is `min(7, 9) = 7`. Therefore:

* **P1.** Probe driver at site 8 → **first nonzero `R_raw` in the DRIVEN sector at lag
  exactly 8** (7 steps to reach driver site 15, 1 step across the link).
* **P2.** Same probe → first nonzero `R_raw` in the driver's OWN sector at lag exactly 0.
* **P3.** Common-driver case, probe the hidden driver `C` at site 8 → first nonzero
  `R_raw` in **both** `A` and `B` at lag exactly 8.

These are forward predictions of integers with no free parameter. A miss on any of them
means the instrument's topology is not the topology this file claims, and every other
number it prints is void until repaired.

## The four planted cases and their pass criteria

Exact-zero means **exactly `0.0` in IEEE double**, at every lag in the window — not "below
a floor". That is the point of the deterministic interventional signature: the null value
of a null arm is the integer zero.

### (a) Deterministic coupled pair, one-way A→B — *the signature must find the arrow and its direction*

Topology: ring `A` autonomous; ring `B` driven by `A` at site 0 from `A`'s site 15.

* **a.1** Probe A, read B: `R_raw > 0` somewhere in the window. **PASS/MISS**
* **a.2** Onset latency of a.1 `== 8` exactly (P1). **PASS/MISS**
* **a.3** Probe B, read A: `R_raw(t) == 0.0` at **every** lag in the window. **PASS/MISS**
* **a.4** `R_view` in B reaches at least 1 bit (the coarse view, not just the raw state,
  registers the intervention). **PASS/MISS**

### (b) Deterministic independent pair — *the case where the observational detector false-fired*

Topology: two autonomous rings, same law, independent initial conditions, no link.

* **b.1** Probe A read B and probe B read A: `R_raw == 0.0` at every lag, both
  directions. **PASS/MISS**
* **b.2** (reported, not staked) the observational cross-defect estimator and its
  permutation floor on the same two series, both directions.

### (c) Common driver — *the case that kills the observational route, reported by Theorem 3*

Topology: hidden ring `C` autonomous; `A` and `B` each driven by `C` (site 15 → site 0),
`A` and `B` never read each other.

* **c.1** Probe A read B, and probe B read A: `R_raw == 0.0` at every lag, **both
  directions**. **PASS/MISS**
* **c.2** Positive control: probe C, read A and read B — both respond, onset latency `== 8`
  in each (P3). **PASS/MISS**
* **c.3** **The crux.** The observational cross-defect exceeds its own 99th-percentile
  permutation floor in **at least one direction** on the A,B series, while c.1 holds.
  **PASS/MISS.** If c.3 misses, the demonstration that intervention separates what
  observation confounds is NOT made on this substrate, and I say so.
* **c.4** (reported) Pearson correlation of the A and B scalar summaries.

### (d) Stochastic one-way pair with coupled-noise twins — *and its planted trap*

Topology (d): as (a), plus additive `σ = 1e-3` noise from an A-blind stream, shared between
twins.

* **d.1** Probe A read B: `R_raw > 0`, onset latency `== 8` exactly. **PASS/MISS**
* **d.2** Probe B read A: `R_raw == 0.0` at every lag. **PASS/MISS**
* **d.3** Distributional arm, fixed initial state, `N = 400` independent noise streams,
  large probe: the probed and unprobed B-ensembles differ at lag 20 with permutation
  `p < 0.01`. **PASS/MISS**

Topology (d′) — **the planted trap of theory §4.1**: `A` and `B` both autonomous, NO causal
link; `B`'s noise draw at each step is taken from slot `k = [x_0 > 0.5]` of two i.i.d.
streams. The kernel is A-independent, so there is **no causal effect**, but the coupled-twin
pathwise comparison must false-fire.

* **d′.1** Pathwise: probe A at site 0 (large), read B: `R_raw > 0`. **This arm must FIRE —
  it is the planted defect, and a silent planted defect convicts the instrument.**
* **d′.2** Distributional arm, same design as d.3: permutation `p > 0.05` — no causal
  effect. **PASS/MISS**
* **d′.3** The adjudication rule, pre-registered: **coupling is claimed only when the
  pathwise AND distributional arms both fire.** Under this rule (d) reads coupled and (d′)
  reads uncoupled. If the rule fails to separate them, the stochastic version of the
  signature is not usable as written and I record that.
* **d′.4** (reported) fraction of steps at which the twins' noise-slot selectors differ.

## Kills for the instrument itself

* **K-I1.** The sham probe (`δ = id`) must give `R_raw == 0.0` everywhere, in every case,
  both directions. Any nonzero sham response means the twins are not twins and **every
  number in the run is void**.
* **K-I2.** Any of P1/P2/P3 missing its staked integer voids the run (topology mismatch).
* **K-I3.** Case (a) must pass a.1 and a.3 together. A detector that fires in both
  directions on a one-way planted truth has no direction and the brick fails.

## §E — the engine demonstration reading (`scratchpad/composition/s2/arm_K.csv`)

**Labelled a DEMONSTRATION throughout. It stakes nothing and can pass nothing**: the series
is a whole-state divergence over one probed/unprobed twin pair with no sector view and no
recorded pre-probe window, so by construction it cannot carry a directional reading. What
it can do is exhibit the shape of a real interventional response and expose what a proper
engine version would have to record. Computed, with the meaning of each answer written
here first:

1. **The pedestal.** `div_pos` and `div_px` at the probe frame (240). Theory §4.3 says a
   deterministic twin pair, compared over pre-existing nodes only, must read exactly 0 at
   the probe frame. *Nonzero ⇒ the probe changed the code path (re-certification /
   mesh refinement / node renumbering), and the instrument has an unadjudicated
   pedestal.* (Already known nonzero — see Disclosure.)
2. **The pedestal's weight in B4's window.** B4 used frames 245–1199. Report
   `(div at frame 240) / (median div over the window)`. *If that ratio is near 1, the
   window is pedestal-dominated and `K ≈ 1` is partly an instrument reading, not only a
   dynamics reading.*
3. **`K` recomputed** exactly as `s2_analyze.py` computed it (median of consecutive
   `div_pos` ratios over `dpos[5:960]`), then recomputed on the **pedestal-subtracted**
   series `div_pos − div_pos[0]`. *A large gap between the two means the pedestal was
   carrying the K reading; a small gap means B4's number survives the diagnostic.*
4. **The response shape** over the full 23760 frames: total growth factor, log-slope of the
   early response, and the lag at which growth departs from exponential. *Reported as the
   shape of a real interventional response, nothing more.*
5. **What is missing**, enumerated against the theory note's requirements.

## What this brick does NOT claim

No claim about nature. No claim that Ω(c) is the maximal object. No promotion of anything
to the stance. The deliverable is: a theorem set, an instrument validated on planted truth,
and an honest reading of one existing engine series.
