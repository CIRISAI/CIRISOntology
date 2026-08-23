# SANDBOX_4090 — an atomically-accurate sandbox as many small holon engines on one GPU

Status: design study. Hardware numbers are **measured on the local device**, not published specs.
Prototype numbers are measured; the throughput model is measured on a *structural* kernel, not on a
granular contact solver — that distinction is load-bearing and is marked everywhere it matters.
Date: 2026-08-23.

Frame: `INTEGRATION_FRAME.md` — one holon, values only. A shard is an **arena with a declared g0 and
root**; a boundary relation is a **pair of indices**. No new entity class appears anywhere below.

---

## 0. Two premises of the brief are wrong, and both change the arithmetic

**The GPU is not the desktop 4090.** `nvidia-smi` and `cudaGetDeviceProperties` agree:

| | brief assumed (AD102) | **measured (this device, AD103)** |
|---|---|---|
| part | RTX 4090 | **RTX 4090 *Laptop* GPU**, CC 8.9 |
| SMs / cores | 128 / 16,384 | **76 / 9,728** |
| memory | 24 GB, ~1 TB/s | **15,944 MiB, 576.1 GB/s theoretical / 435.9 measured** |
| f32 | ~83 TFLOPS | **27.40 TFLOP/s sustained** (96.8% of peak at a locked 1455 MHz) |
| f64 | ~1.3 TFLOPS (1/64) | **0.372 TFLOP/s** — ratio **1/63.8**, the 1/64 rate confirmed |
| L2 | — | **64 MiB** |
| power | — | 80 W default cap (175 W max limit); clock pinned at base 1455 MHz, no throttle over 6 sustained rounds |

Every downstream number in this document uses the measured column. The card is **~40% of the
compute and ~66% of the memory** the brief budgeted for.

**The ~3.5-grain ledger cap is the constituents-only cap, and `constituents` is not the binding
lane.** `GrossState` has four integer lanes (`regplus.rs:26-32`): `constituents: u64`,
`occupancy: u64`, `momentum: [i64; 2]`. `occupancy` is the sum of per-leaf REG+ occupancies, each
`0..6` (`regplus.rs:94-111`), so a chart that writes occupancy at *q*× constituents overflows first:

| binding lane | cap in 0.5 mm quartz grains (5.216e18 atoms each) |
|---|---|
| `constituents` alone (u64) | **3.537** |
| `occupancy` at q=1 | 3.537 |
| **`occupancy` at q=2** — the demo's own `aggregate(n, 2n, …)` idiom | **1.768** |
| `occupancy` at q=6 (max REG+) | **0.589** |
| `momentum` (i64, fully aligned) | 1.768 |

So the honest headline is: **the arena counts between 0.59 and 3.54 grains of sand in atoms,
depending on which lanes the chart writes.** A design that budgets 3.54 and then turns on REG+
occupancy overflows at 1/6 of the assumed capacity. This wants a `Tier`-level assertion, not a
comment (gap G6).

---

## 1. Scene and residency arithmetic

Sandbox 0.6 × 0.4 × 0.3 m = 0.0720 m³; 0.5 mm grains, V_grain = 6.5450e-11 m³; 60% packing
→ **9.167e9 grains/m³**, **6.601e8 grains**, **3.443e27 atoms** = **1.87e8× over the u64 cap**.
(This is the brief's scene. `holon-sandbox/tier.rs` declares a *different*, square 0.6 m domain at
fill 0.45; its own three constituent figures disagree with each other — see gap G7.)

**Resident capacity is 2–3× below the brief's 4.3e8**, because 56 B is the header, not the holon:

| what you actually pay per resident holon | B | holons in 15,944 MiB |
|---|---:|---:|
| `RuntimeHolon` header alone (`runtime.rs:31-41`, verified `sizeof` = 56) | 56 | 2.99e8 |
| + `first_child`/`next_sibling` index (2×u32, `runtime.rs:139-145`) | 64 | 2.61e8 |
| + live ledger overlay (`GrossState`, 32 B — the prototype proved this is **mandatory**, §5) | 96 | 1.74e8 |
| + whole-state pool at W=2 (the persisted seed, `descriptor.rs:106`) | **112** | **1.49e8** |

**Realistic resident sets** (geometric estimates at 60% packing, stated assumptions, not measurements):

| state | geometry | grains resident | GB @112 B |
|---|---|---:|---:|
| settled pile, quiescent | free surface 0.24 m², 2 grains deep | 2.20e6 | 0.25 |
| pour | dilute stream + impact apron + standing surface | 4.33e6 | 0.49 |
| ball impact, modest | disturbed hemisphere r = 0.10 m | 1.92e7 | 2.15 |
| **ball impact, large** | disturbed hemisphere r = 0.15 m | **6.48e7** | **7.26** |

**The crater is the sizing case and it fits.** 7.26 GB of 15.9 GB, with the remaining 6.54e8 grains
latent at gross-ledger only. Certificate-directed residency is what makes the scene tractable:
quiescent sand is a `Latent` holon carrying an exact integer ledger and nothing else.

---

## 2. Engine geometry, measured

One block = one engine; holons SoA in shared memory; 40 B/holon of hot state
(u64 constituents + 2×i64 momentum + 4×f32 position/velocity limbs):

- **10,240 B per 256-holon engine** → **10 engines/SM** (shared-memory bound; 102,400 B/SM), 12 by
  the 1,536-threads/SM limit. → **760 concurrent engines = 194,560 holons resident in shared memory.**
- **Kernel launch is 3.0 µs flat**, independent of grid size (measured at 1 and 608 blocks).
  Per-engine kernel launches are therefore impossible: 2.6e6 engines × 3 µs = **7.7 s of pure
  launch overhead**. One persistent kernel, engines grid-strided across blocks, is the only option.

**Structural throughput** (holon-steps/s, 38,912 engines × 256 holons):

| arithmetic | holon-steps/s | vs f64 | crater r=0.15 m, 20 substeps | real-time ceiling (16.7 ms, 20 substeps) |
|---|---:|---:|---:|---:|
| f32 | 2.772e11 | 4.17× | 4.67 ms | 2.32e8 holons |
| **df64 (2×f32)** | **1.710e11** | **2.57×** | **7.57 ms** | **1.43e8 holons** |
| native f64 | 6.650e10 | 1.00× | 19.47 ms | 5.55e7 holons |

> **Honesty bound on this table.** The kernel integrates independent holons (symplectic Euler +
> integer ledger). It contains **no neighbour search, no contact detection, and no contact
> resolution** — the expensive parts of a granular solver. It measures the *arithmetic and memory
> behaviour of the proposed layout*, which is what the arithmetic decision needs, and it is **not** a
> granular frame rate. Real contact solving is plausibly 10–100× more work per holon-step, which
> moves the real-time ceiling to ~5.5e5–5.5e6 holons at f64. The crater fits the *memory*; whether it
> fits the *frame* is unmeasured and is gap G1.

---

## 3. The four design decisions

### D1 — Arithmetic: **native f64 with strict intrinsics**, df64 as a declared values-change

The brief framed this as f64-is-too-slow. The measurement says the trade is real but affordable,
and — decisively — **the cheap option does not buy back the property being paid for**.

Measured: native f64 **0.372 TFLOP/s**; df64 **1.369 Tdf-FLOP/s** (**3.68×** in pure FMA, **2.57×**
in the engine kernel, the gap narrowing because the kernel is shared-memory bound). f32 is a further
1.62× over df64.

The engine's bit-exact tri-target replay (`PORTABILITY.md`) is load-bearing. df64 carries ~48
mantissa bits against f64's 53 and is a **different number system** — it can never reproduce f64 bit
patterns, so choosing it drops the GPU out of the bit-identity claim permanently. Native f64 *can*
stay in it: IEEE-754 add/mul/fma are correctly rounded on both hosts, so with `__dadd_rn`/`__dmul_rn`/
`__fma_rn` (contraction disabled), fixed operation order, and no transcendentals in the stepping
path, the GPU becomes a **fourth bit-exact target** rather than a second-class one.

**Decision: pay the 2.57×.** At realistic crater sizes it is affordable (r = 0.10 m: 5.77 ms at 20
substeps) and it preserves the property the programme actually sells. Offer df64 behind an explicit
declaration with its own error certificate for scenes that need the headroom — a values change, and
one whose kill is "the df64 trajectory leaves the certified band against the f64 reference".

**Integer stays integer.** The REG+ ledger is already 100% integer end-to-end (`regplus.rs`,
`runtime.rs:306`, `descriptor.rs:264-310`) and must remain so: integer addition is exactly
associative, so the ledger is order-independent *by construction* — the one part of the system whose
determinism needs no discipline at all. Measured i64: 4.38 TIOP/s mul-add, 3.49 TIOP/s add-with-
dependency (i32 is 2.7× faster; i64 is emulated on Ada but never the bottleneck here).

### D2 — Layout: **SoA for the hot ledger**, AoS header retired from the device

Measured on 16 M holons, sweeping one field: **AoS 56 B = 1.20 ms; SoA u64 = 0.30 ms — 4.0×.**
The 56 B header drags 56 B of traffic for 8 B of payload. Split on the device: hot lanes
(`constituents`, `occupancy`, `momentum[2]`, position/velocity) as separate SoA arrays; cold topology
(`parent`, `depth`, `grain_units`, `whole_offset/len`, `channels`, flags) in a side array touched
only at materialization. The host `RuntimeArena` keeps its 56 B `repr(C)` header unchanged — this is
a device-side *layout*, not an ontology change.

### D3 — Boundary protocol: **snapshot-then-apply over disjoint pairs**, with a re-planning gate

Taken from the CPU prototype (§5), which proved it exactly conserving and bit-identical. Two
properties, both needed:

1. **snapshot-then-apply** — every transfer is a pure function of a port snapshot published after all
   local steps and before any write. This gives order-independence and per-shard bit-identity.
2. **disjoint pairs** — each link owns its own port holon, so pair writes never overlap. This makes
   the apply phase lock-free (on GPU: no atomics at all on the exchange path).

**What certificate covers a shard boundary:** *the re-planned transfer.* This is the prototype's
most important finding and it is counter-intuitive — **a global-sum gate does not work.** Doubling
*both* sides of a transfer, or dropping *both*, is perfectly conserved and perfectly antisymmetric;
it passes global sum, pair antisymmetry, apply-consistency, local conservation and composition. Only
re-deriving the intended transfer from the published snapshot and comparing catches it. The boundary
certificate must therefore assert **plan-conformance**, not balance.

Atomics measurement drives the reduction design: u64 `atomicAdd` on **1 slot = 0.002 T/s**, on
**4,096 slots = 0.167 T/s** — an **83× spread penalty**. Per-engine private accumulators, reduced
hierarchically in fixed order; never a global ledger atomic.

### D4 — Determinism: parallel **across** engines, sequential **within**

| | status |
|---|---|
| integer ledger composition and exchange | **provably deterministic** — integer + is exactly associative; `checked_add` refuses overflow rather than wrapping |
| boundary exchange ordering | **provably deterministic** — snapshot-then-apply; measured bit-identical across 1–32 threads × 4 repeats on every holon, not just roots |
| engine interior | **deterministic by construction** — one block, fixed loop order, no cross-engine dependency between exchanges |
| f64 stepping with strict intrinsics + fixed order | **deterministic, conditionally** — holds only while contraction is disabled and no transcendental enters the step |
| cross-lane float reductions, float atomics | **not deterministic** — banned on the certified path |
| **seeded materialization** | **NOT portable to device today** — SplitMix64 is integer and fine, but the draw calls `log`/`cos`/`pow` (`descriptor.rs:491-496`); CUDA's libdevice is not bit-identical to `libm`. **Materialization stays on the host** (gap G2). |

---

## 4. What "atomically accurate" honestly means

All-atoms-resident is impossible by 8 orders of magnitude and is not the claim. The claim is the
**certificate chain**, and `DESCRIPTOR_CHAIN.md` is already stricter about it than the brief:

- The chain **bottoms out in measurement, not in a deeper simulation** (`DESCRIPTOR_CHAIN.md:68`),
  and the base certificate is **statistical, not deductive** (`:97`).
- The mechanical channel **terminates at `GrainFloor` at grain/crystal scale by design**; the atomic
  tiers exist to *certify the crystal descriptor's values*, "**not to be materialized in a game
  frame**" (`INTEGRATION_FRAME.md:81-84`).
- Some quantities are **minted at a tier and provably do not transport**: fracture energy's 30–100×
  gap from 2γ ≈ 1–4 J/m² to 110 J/m² is process-zone dissipation created at T4 (`:348`). An
  "atomically accurate G_F" is false *by theorem* — the number has no atomic ancestor.
- Today the flagship chain is **experiment-pinned, not derived**: feldspar (~60% of granite) has no
  fracture-grade certified potential, so `DEMO_CALIBRATION` "cannot be reached bottom-up today for
  any field" (`:164`).

**A 4090 sandbox could certify:** exact integer conservation of the constituent/occupancy/momentum
ledger across every shard and every refinement, globally and per-shard, bit-for-bit; bit-exact replay
of a given scene on a given device; grain-scale contact and cohesive response within T3/T4 validity
domains (250–350 K, strain rate < ~1 s⁻¹, specimen ≥ 20·d50) with signed error bands; and
statistical composition of any materialized ensemble against its descriptor's declared law at
`CERT_Z = 5.0`.

**It must refuse:** sub-d50 crack paths and nucleation sites (`GrainFloor` — "`not_computable_from`
in this tier's clothes", `:195`); fields within ~1 nm of a crack tip; anything requiring bond
rearrangement, excitation or coordination change (T1/T2 floors); damping ratio and restitution as
material constants (falsified as such, `:284`); and — specific to this design — **any claim that a
df64 run reproduces the f64 reference bit-for-bit**. The refusals are the product. A sandbox that
answers every question has stopped certifying anything.

One further refusal is forced by the fanout: at the shipped fracture fanout of 4, **every**
statistical check sits below its resolution floor (`CERT_FLOOR_MEAN = 8`, `CERT_FLOOR_SPREAD = 32`)
and rides along unresolved. A GPU materializer drawing thousands of children per engine is the first
configuration where the descriptor certificate actually has teeth — that is an opportunity, not a
problem, but it means today's passing certificate is *silent*, not *supporting*.

---

## 5. CPU prototype: measured (`crates/holon-swarm`, 3,141 lines, 34 tests passing)

Standalone crate, one dependency (`ciris-sim-core`, `alloc`), no new external deps, no `unsafe`.
A shard *is* a `RuntimeArena`; a port *is* an ordinary holon wearing the `boundary` flag it already
has; a link *is* a pair of indices. No new entity class.

**Conservation: EXACT.** 80 rounds at the strictest gate, global `GrossState` bit-identical in all
four integer lanes (`constituents 32960, occupancy 395287, momentum [66030, −66017]`) while 8 of 8
shard balances moved off their opening values. No epsilon anywhere in the crate.

**Determinism: BIT-IDENTICAL.** Threaded == sequential over threads ∈ {1,2,3,4,8,16,32} × 4 repeats,
compared on every holon's ledger plus every whole-state f64 by `.to_bits()`, and under natural /
reversed / strided visit order. The sequential reference is written independently of the threaded
path, so agreement is evidence rather than tautology.

**Scaling** (release; `nproc` = 32 on a **heavily loaded shared machine** — load average 18–43
throughout, so wall-clock speedups are not defensible and CPU-time-normalised efficiency is):

| N shards | µs/round (16 threads) | ns/holon | efficiency vs cores actually obtained |
|---:|---:|---:|---:|
| 1 | 8454 | 32.25 | 99% |
| 4 | 2326 | 8.87 | 90% |
| 8 | 1058 | 4.04 | 90% |
| 16 | **672** | **2.56** | 62% |

The algorithm holds **≥90% efficiency against the cores it is given through 8 threads**, dropping to
62% at 16 — three `Barrier`s per round make the round as slow as its slowest shard, and on this
hybrid CPU that is whichever thread landed on an E-core. **The barrier is the scaling limit, not the
exchange.** Per boundary pair: **86.5 ns/round** (least-squares slope over pairs ∈ 1…1024).

A load-independent bonus finding that transfers directly to the GPU: sharding alone gives a **1.64×
single-threaded speedup** at fixed total work, purely from working-set locality (16,384 holons ×
32 B = 512 KB fits L2; 262,144 × 32 B = 8 MB does not). Small engines are faster *before* any
parallelism is applied.

**Mutation tests: 9 mutations × 3 gate levels × 2 execution paths, all caught at `Full`.** Credit
without debit, transfer applied twice (one side / both sides), transfer dropped (both sides), sign
swapped, momentum overflow (typed error, no panic), local step minting from nothing, child credited
without parent, root credited without any child.

**Two weaknesses found and pinned by tests, both design inputs rather than defects:**

1. **The obvious gate does not work** — doubling or dropping *both* sides of a transfer passes every
   balance-based leg. Only re-planning from the published snapshot sees it. (→ D3.)
2. **`RuntimeArena::validate()` is structurally vacuous over a stepping shard.** The core exposes
   `holons()` as `&[RuntimeHolon]` with no mutable ledger accessor (only append-only `materialize`),
   so a stepping shard must carry an index-aligned `Vec<GrossState>` overlay. `validate()` reads the
   arena's *stored* gross states, which never change, so it cannot see ledger corruption at all — a
   gate built literally from "sum the roots + call `validate()`" is **blind to a broken composition**.
   Pinned by `weakness_a_ledger_only_gate_is_blind_to_a_broken_composition`, which fails if the
   escape ever stops happening. The non-vacuous form rebuilds through `RuntimeArena::from_specs` and
   costs 84% of a round.

That overlay is not a workaround — **it is exactly the flat device buffer the GPU wants** (32 B/holon
SoA), which is why it appears in the §1 memory table as mandatory.

---

## 6. Gap list

| # | gap | scope |
|---|---|---|
| **G1** | **No contact solver in the throughput model.** §2's rates measure layout, not granular physics. Next measurement: neighbour search + contact resolution on the device, which decides whether the crater fits a frame. **The single largest unknown in this study.** | measure before designing further |
| **G2** | **Materialization cannot run on device.** SplitMix64 is integer and portable; the draw's `log`/`cos`/`pow` are not bit-identical between `libm` and libdevice. Keep materialization host-side, or supply bit-exact software transcendentals. | host-side is the cheap answer |
| **G3** | **No GPU backend exists.** Minimal scope: a separate crate `crates/holon-gpu`, **outside the workspace** (the `engine-compare` precedent, `Cargo.toml:21-25`), so the core's `no_std`/zero-allocation/isolation gates in `ci-gates.sh` stay valid. CUDA via `cust` beats wgpu here: wgpu has **no f64 in WGSL at all**, which forecloses D1 outright. |  new crate, no core deps |
| **G4** | `FractureModel`/`ImpactModel` hold `Rc<RefCell<WallChart>>` (`fracture.rs:348`, `impact.rs:165`) — **`!Send`**, so they cannot cross a thread today, let alone a device. | refactor to a passed workspace |
| **G5** | Every solve allocates fresh `Vec`s. `incremental.rs::Workspace` is the only reusable-workspace precedent; the device needs that pattern everywhere. | mechanical |
| **G6** | **The ledger cap is unasserted.** §0's occupancy-lane overflow is a comment, not a check. A `Tier`-level assertion should compute the cap from the lanes the chart actually writes and refuse at declaration time. | small, high value |
| **G7** | `holon-sandbox/tier.rs` states the sandbox constituent count **three different ways** (header prose 6.60e8; `constituents` field 622,080,000; `fill = 0.45` implies `ledger()` = 777,600,000) and no test asserts they agree. Also `three_tiers_refuse_and_each_names_why` asserts `== 4`. | reported to that lane |
| **G8** | Incremental certifier growth is **cubic** (`incremental.rs:11-15`: 22→1366 materializations costs 0.0001→6.94 s); a single full descent is quadratic and 5,465 holons already takes 12.20 ms. Sharding attacks this directly — 1.64× from locality alone, plus N-way parallelism — but the exponent is unchanged by sharding. | the reason to shard, and its limit |

---

## 7. The design in one paragraph

Shard the sandbox into ~2.6e6 arenas of ~256 holons, each an ordinary `RuntimeArena` with its own
declared g0 and root, related by pairs of boundary indices — values, not a new class. Run them as one
persistent CUDA kernel, one block per engine, 10 engines resident per SM (760 concurrent), holons SoA
in shared memory (4.0× over the 56 B AoS header). Step engine interiors sequentially in native f64
with strict intrinsics, keeping the GPU inside the tri-target bit-identity claim at a measured 2.57×
against df64. Keep the REG+ ledger in integers, where associativity makes determinism free. Exchange
across boundaries by snapshot-then-apply over disjoint pairs, with no atomics on the exchange path,
and certify the boundary by **re-planning the transfer**, because balance-based gates provably miss
double-applied and dropped transfers. Hold the quiescent 6.5e8 grains latent as exact integer
ledgers; make resident only the disturbed set, which for a large ball-impact crater is 6.5e7 holons
and 7.3 GB of 15.9 GB. Then refuse, loudly, every question below d50.
