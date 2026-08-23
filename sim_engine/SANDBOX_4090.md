# SANDBOX_4090 — an atomically-accurate sandbox as many small holon engines on one GPU

Status: design study. Hardware numbers are **measured on the local device**, not published specs.
Prototype numbers are measured. Throughput is measured on a *structural* kernel, not on a granular
contact solver — that distinction is load-bearing and marked everywhere it matters.
Tier table and thrown-resident counts are the holon-sandbox lane's, relayed 2026-08-23.
Date: 2026-08-23.

Frame: `INTEGRATION_FRAME.md` — one holon, values only. A shard is an **arena with a declared g0 and
root**; a boundary relation is a **pair of indices**. No new entity class appears anywhere below.

---

## 0. The headline: the GPU is not short of compute, it is short of *permission to be resident*

At the shipped tier the certificate makes **2,000–5,000 holons resident per throw**, and the event
budget is **120 ms**. That workload is ~1.5 µs of native-f64 arithmetic on this card — the budget is
oversupplied by **~80,000×**, and still by ~800× if contact solving costs 100× more than my kernel
models. **For one sandbox at the certificate's own residency, a 4090 is not needed at all.** The CPU
already meets the budget; the incremental certifier's ~2.86 growth exponent is the real constraint,
and it is an algorithmic problem that a GPU does not solve.

So the design question is not "how do we fit the sandbox on a GPU." It is: **what do we spend 16 GB
and 9,728 cores on?** There are exactly two honest answers, and they want different architectures:

| | what the card buys | resident | limit |
|---|---|---|---|
| **(a) many scenes** | ~29,800 concurrent sandbox throws | 5,000 holons each | **memory**-bound (compute would allow ~79,800) |
| **(b) one deeper scene** | the resident frontier pushed ~10⁴ below what the certificate demands | 1.49e8 holons | this is where "atomically accurate" actually lives |

**(b) is the interesting one, and it has a clean number.** The card's resident capacity is 1.49e8
holons. The Z0 GRAIN tier resolves *one* 0.5 mm grain into 1.25e8 subgrain holons at g0 = 1 µm.
So:

> **One RTX 4090 holds about 1.19 grains of sand at 1 µm subgrain resolution.**
> It can *count* 3.54 grains in atoms and can never *resolve* them.

That is the honest scale of "atomically accurate on a 4090", and it is pleasingly close to the
brief's own framing of ~3 grains — the two numbers just measure different things (ledger capacity vs
resident capacity), and both land at "a few grains of sand."

---

## 1. Hardware truth — the brief's device premise is wrong

`nvidia-smi` and `cudaGetDeviceProperties` agree:

| | brief assumed (AD102) | **measured (this device, AD103)** |
|---|---|---|
| part | RTX 4090 | **RTX 4090 *Laptop* GPU**, CC 8.9 |
| SMs / cores | 128 / 16,384 | **76 / 9,728** |
| memory | 24 GB, ~1 TB/s | **15,944 MiB, 576.1 GB/s theoretical / 435.9 measured** |
| f32 | ~83 TFLOPS | **27.40 TFLOP/s sustained** (96.8% of peak at a locked 1455 MHz) |
| f64 | ~1.3 TFLOPS (1/64) | **0.372 TFLOP/s** — ratio **1/63.8**, the 1/64 rate confirmed |
| L2 | — | **64 MiB** |
| power | — | 80 W default cap (175 W max limit); clock pinned at base, no throttle over 6 sustained rounds |

Every number below uses the measured column. The card is **~40% of the compute and ~66% of the
memory** the brief budgeted.

Other measured primitives: **i64** 4.38 TIOP/s mul-add, 3.49 TIOP/s add-with-dependency (i32 is
2.7× faster; i64 is emulated on Ada but never the bottleneck here). **Kernel launch 3.0 µs flat**,
independent of grid size. **u64 `atomicAdd`**: 0.002 T/s on one slot, 0.167 T/s across 4,096 — an
**83× contention penalty**.

---

## 2. The ledger cap, and a latent defect in the sizing helper

The sandbox lane's derivation is confirmed: `constituents` u64 = 1.8447e19, one 0.5 mm quartz grain
= 5.216e18 atoms → **3.54× headroom, "about three and a half grains."** `grain_units` u32 = 4.295e9
(quadtree depth cap 32). The 0.6 × 0.4 × 0.3 m sandbox at 60% packing = 6.60e8 grains = 3.44e27
atoms = **1.87e8× over**, so `checked_combine` refuses and the answer is per-scene g0 with a
**re-root between tiers** — licensed by `CIRIS_HOLON_ENGINE.md`'s no-absolute-maximal-holon.

The cap is not theoretical; it **bit twice during the lane's own sizing**: g0 = 1 m on Earth gave
1.08e21 (59× over, forced 10 m); g0 = 10 kpc on the observable universe gave 2.32e19 cells (1.26×
over, forced 40 kpc).

**But `constituents` is only one of four integer lanes, and the sizing helper checks only that one.**
`GrossState` is `{constituents: u64, occupancy: u64, momentum: [i64;2]}` (`regplus.rs:26-32`), and
`occupancy` is a sum of per-leaf REG+ values in `0..6` (`regplus.rs:94-111`):

| binding lane | cap in grains | who writes this |
|---|---:|---|
| `constituents` alone | **3.537** | `holon-sandbox` (`scene.rs:533` writes occupancy `0`), `holon-ball-game`, `fracture.rs`, `impact.rs` |
| `occupancy` at 2× constituents | **1.768** | **the core's own idioms** — `runtime.rs:875`, `holon.rs:500`, `mechanical.rs:295`, `descriptor.rs:947`, `descriptor.rs:1107` |
| `occupancy` at 6× (max REG+) | **0.589** | any chart writing full REG+ occupancy |
| `momentum` (i64, fully aligned) | 1.768 | — |

**The sandbox is safe today at 3.54 because it writes occupancy = 0.** The defect is that
`ledger_for` (`tier.rs:225-242`) validates `ratio` against `u32::MAX` and `count` against `u64::MAX`
— *the constituents lane only*. A chart that turns on `Channels::REG_PLUS`, as the core's own
mechanical idioms already do at 2×, would **pass `ledger_for` and then overflow at
`checked_combine`** at 1/2 to 1/6 of the sized capacity. That is gap **G6**: the helper should
compute the cap from the lanes the chart actually declares, and refuse at declaration time.

---

## 3. The tier table, and where residency actually sits

Relayed from the holon-sandbox lane. 2D chart / 3D ledger split; edges only on throw; quiescent =
gross render, zero resident relations.

| Z | tier | g0 | extent | ledger (constituents) | **thrown resident** | evaluator |
|---|---|---|---|---:|---:|---|
| −2 | GAUGE | one U(1) link | — | 4 links / 5 holons | 5 | exact `quantum_link` (on main) |
| −1 | CRYSTAL | quartz cell 4.9134 Å | 1 µm | 8.43e9 | — | **NONE — refuses** |
| 0 | GRAIN | 1 µm subgrain | 0.5 mm | 1.25e8 | 400–2,700 (~1.2k–8k bonds) | cohesive |
| **1** | **SANDBOX** | **0.5 mm grain** | **0.6 m** | **6.60e8** | **2,000–5,000 (~6k–15k contacts)** | granular contact |
| 2 | LANDSCAPE | 1 cm clast | 2 km | 8.00e15 | ~3,800 (~11k bonds) | cohesive T4 — **the shipping tier** |
| 3 | PLANET | 10 m | 1.274e7 m | 2.07e18 | — | **no gravity evaluator — refuses** |
| 4 | GALACTIC | 1 pc | — | ~1e11 stars | — | **refuses** |
| 5 | COSMIC | 40 kpc | — | ~2e12 galaxies | — | **refuses** |

**Four of eight tiers refuse.** That is the design working, not a gap.

**Resident capacity is 2–3× below the brief's 4.3e8**, because 56 B is the header, not the holon:

| what you actually pay per resident holon | B | holons in 15,944 MiB |
|---|---:|---:|
| `RuntimeHolon` header alone (`runtime.rs:31-41`, verified `sizeof` = 56) | 56 | 2.99e8 |
| + `first_child`/`next_sibling` index (2×u32, `runtime.rs:139-145`) | 64 | 2.61e8 |
| + live ledger overlay (`GrossState`, 32 B — the prototype proved this **mandatory**, §6) | 96 | 1.74e8 |
| + whole-state pool at W=2 (the persisted seed, `descriptor.rs:106`) | **112** | **1.49e8** |

**The gap between 5,000 thrown-resident and 1.49e8 capacity is a factor of ~30,000, and it is the
whole finding.** Certificate-directed residency is working so well that it has made the GPU
unnecessary at the shipped tier. My first pass at this study estimated residency *geometrically* —
every grain in the disturbed volume, giving 1.9e7–6.5e7 for a ball-impact crater — and that was
wrong by four orders of magnitude, because the certificate keeps only the *contact frontier*
resident, never the disturbed volume. The geometric number is what you would need if you abandoned
the certificate; the tier number is what the certificate actually demands.

---

## 4. Engine geometry, measured

One block = one engine; holons SoA in shared memory; 40 B/holon of hot state
(u64 constituents + 2×i64 momentum + 4×f32 position/velocity limbs):

- **10,240 B per 256-holon engine** → **10 engines/SM** (shared-memory bound; 102,400 B/SM), 12 by
  the 1,536-threads/SM limit → **760 concurrent engines = 194,560 holons stepping at once.**
- One sandbox throw (5,000 holons) ≈ **20 engines**, so the card runs **38 scenes at full SM
  occupancy** and holds ~29,800 resident.
- **Launch overhead 3.0 µs flat** forecloses per-engine kernels: 2.6e6 engines × 3 µs = **7.7 s of
  pure launch overhead**. One persistent kernel, engines grid-strided across blocks.

**Structural throughput** (holon-steps/s, 38,912 engines × 256 holons):

| arithmetic | holon-steps/s | vs f64 | one 5,000-holon throw, 20 substeps | headroom vs 120 ms event budget |
|---|---:|---:|---:|---:|
| f32 | 2.772e11 | 4.17× | 0.36 µs | 333,000× |
| df64 (2×f32) | 1.710e11 | 2.57× | 0.58 µs | 205,000× |
| **native f64** | **6.650e10** | **1.00×** | **1.50 µs** | **80,000×** |

> **Honesty bound.** The kernel integrates independent holons (symplectic Euler + integer ledger).
> It contains **no neighbour search, no contact detection, no contact resolution**. It measures the
> *arithmetic and memory behaviour of the proposed layout* — which is exactly what the arithmetic
> decision needs — and is **not** a granular frame rate. Real contact solving is plausibly 10–100×
> more work per holon-step. Even at 100×, native f64 clears the event budget by ~800×.

---

## 5. The four design decisions

### D1 — Arithmetic: **native f64**. The trade the brief anticipated does not arise.

Measured: native f64 **0.372 TFLOP/s**; df64 **1.369 Tdf-FLOP/s** (**3.68×** in pure FMA, **2.57×**
in the engine kernel, the gap narrowing because the kernel is shared-memory bound); f32 a further
1.62× over df64.

The brief asked us to pick with arithmetic. The arithmetic says **the 1/64 f64 penalty is real and
irrelevant**: at event granularity — option (d) in the brief — native f64 clears the 120 ms budget
by 80,000×, and by ~800× under a 100× contact-solving penalty. There is nothing to buy with df64.

And the thing df64 would cost is expensive. Bit-exact tri-target replay (`PORTABILITY.md`) is
load-bearing. df64 carries ~48 mantissa bits against f64's 53 and is a **different number system** —
it can never reproduce f64 bit patterns, so adopting it drops the GPU out of the bit-identity claim
permanently. Native f64 *can* stay in it: IEEE-754 add/mul/fma are correctly rounded on both hosts,
so with `__dadd_rn`/`__dmul_rn`/`__fma_rn` (contraction disabled), fixed operation order, and no
transcendentals in the stepping path, the GPU becomes a **fourth bit-exact target**.

**Decision: native f64, strict intrinsics, contraction off.** Keep df64 implemented but unused,
behind an explicit declaration with its own error certificate, for the (b)-architecture case where
the resident frontier is pushed 10⁴ deeper and the 2.57× starts to matter. Its kill: *the df64
trajectory leaves the certified band against the f64 reference.*

**Integer stays integer.** The REG+ ledger is already 100% integer end-to-end (`regplus.rs`,
`runtime.rs:306`, `descriptor.rs:264-310`) and must remain so: integer addition is exactly
associative, so the ledger is order-independent **by construction** — the one part of the system
whose determinism needs no discipline at all.

### D2 — Layout: **SoA for the hot ledger**; the 56 B AoS header stays host-side

Measured on 16 M holons sweeping one field: **AoS 56 B = 1.20 ms; SoA u64 = 0.30 ms — 4.0×.** The
header drags 56 B of traffic for 8 B of payload. On the device, split hot lanes (`constituents`,
`occupancy`, `momentum[2]`, position/velocity) into separate SoA arrays and park cold topology
(`parent`, `depth`, `grain_units`, `whole_offset/len`, `channels`, flags) in a side array touched
only at materialization. The host `RuntimeArena` keeps its 56 B `repr(C)` header unchanged — this is
a device-side *layout*, not an ontology change.

### D3 — Boundary protocol: **snapshot-then-apply over disjoint pairs**, certified by re-planning

From the CPU prototype (§6), which proved it exactly conserving and bit-identical. Two properties:

1. **snapshot-then-apply** — every transfer is a pure function of a port snapshot published after all
   local steps and before any write. Gives order-independence and per-shard bit-identity.
2. **disjoint pairs** — each link owns its own port holon, so pair writes never overlap. Makes the
   apply phase lock-free; on GPU, **no atomics on the exchange path at all**.

**What certificate covers a shard boundary: the re-planned transfer.** This is the prototype's most
important finding and it is counter-intuitive — **a global-sum gate does not work.** Doubling *both*
sides of a transfer, or dropping *both*, is perfectly conserved and perfectly antisymmetric; it
passes global sum, pair antisymmetry, apply-consistency, local conservation and composition. Only
re-deriving the intended transfer from the published snapshot catches it. The boundary certificate
must assert **plan-conformance**, not balance.

The atomics measurement drives reduction design: u64 `atomicAdd` costs 83× more contended (1 slot)
than spread (4,096 slots). Per-engine private accumulators, reduced hierarchically in fixed order;
never a global ledger atomic.

### D4 — Determinism: parallel **across** engines, sequential **within**

| | status |
|---|---|
| integer ledger composition and exchange | **provably deterministic** — integer + is exactly associative; `checked_add` refuses overflow rather than wrapping |
| boundary exchange ordering | **provably deterministic** — snapshot-then-apply; measured bit-identical across 1–32 threads × 4 repeats, on every holon, not just roots |
| engine interior | **deterministic by construction** — one block, fixed loop order, no cross-engine dependency between exchanges |
| f64 stepping, strict intrinsics + fixed order | **deterministic, conditionally** — holds only while contraction is disabled and no transcendental enters the step |
| cross-lane float reductions, float atomics | **not deterministic** — banned on the certified path |
| **seeded materialization** | **NOT portable to device today.** SplitMix64 is integer and fine, but the draw calls `log`/`cos`/`pow` (`descriptor.rs:491-496`) and CUDA's libdevice is not bit-identical to `libm`. **Materialization stays host-side** (gap G2). |

---

## 6. CPU prototype: measured (`crates/holon-swarm`, 3,141 lines, 34 tests passing in release)

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

**≥90% efficiency against the cores it is given through 8 threads**, dropping to 62% at 16 — three
`Barrier`s per round make the round as slow as its slowest shard, and on this hybrid CPU that is
whichever thread landed on an E-core. **The barrier is the scaling limit, not the exchange**
(86.5 ns per boundary pair per round, least-squares slope over pairs ∈ 1…1024).

A load-independent bonus that transfers directly to the GPU: sharding alone gives a **1.64×
single-threaded speedup** at fixed total work, purely from working-set locality (16,384 holons ×
32 B = 512 KB fits L2; 262,144 × 32 B = 8 MB does not). Small engines are faster *before* any
parallelism is applied — which is independent support for the many-small-engines premise.

**Mutation tests: 9 mutations × 3 gate levels × 2 execution paths, all caught at `Full`.** Credit
without debit; transfer applied twice (one side / both sides); transfer dropped (both sides); sign
swapped; momentum overflow (typed error, no panic); local step minting from nothing; child credited
without parent; root credited without any child.

**Two weaknesses found, pinned by tests, both design inputs rather than defects:**

1. **The obvious gate does not work** — doubling or dropping *both* sides passes every balance-based
   leg. Only re-planning from the published snapshot sees it. (→ D3.)
2. **`RuntimeArena::validate()` is structurally vacuous over a stepping shard.** The core exposes
   `holons()` as `&[RuntimeHolon]` with no mutable ledger accessor (only append-only `materialize`),
   so a stepping shard must carry an index-aligned `Vec<GrossState>` overlay. `validate()` reads the
   arena's *stored* gross states, which never change, so it cannot see ledger corruption at all — a
   gate built literally from "sum the roots + call `validate()`" is **blind to a broken
   composition**. Pinned by `weakness_a_ledger_only_gate_is_blind_to_a_broken_composition`, which
   fails if the escape ever stops happening. The non-vacuous form rebuilds through
   `RuntimeArena::from_specs` and costs 84% of a round.

That overlay is not a workaround — **it is exactly the flat device buffer the GPU wants** (32 B/holon
SoA), which is why it appears in §3's memory table as mandatory.

---

## 7. What "atomically accurate" honestly means

All-atoms-resident is impossible by eight orders of magnitude and is not the claim. The claim is the
**certificate chain**, and `DESCRIPTOR_CHAIN.md` is already stricter about it than the brief:

- The chain **bottoms out in measurement, not in a deeper simulation** (`:68`), and the base
  certificate is **statistical, not deductive** (`:97`).
- The mechanical channel **terminates at `GrainFloor` at grain/crystal scale by design**; the atomic
  tiers exist to *certify the crystal descriptor's values*, "**not to be materialized in a game
  frame**" (`INTEGRATION_FRAME.md:81-84`). The tier table's Z−1 CRYSTAL refusal is that sentence
  executing.
- Some quantities are **minted at a tier and provably do not transport**: fracture energy's 30–100×
  gap from 2γ ≈ 1–4 J/m² to 110 J/m² is process-zone dissipation created at T4 (`:348`). An
  "atomically accurate G_F" is false *by theorem* — the number has no atomic ancestor.
- The chain is **experiment-pinned, not derived**, where it matters most: feldspar (~60% of granite)
  has no fracture-grade certified potential, so `DEMO_CALIBRATION` "cannot be reached bottom-up today
  for any field" (`:164`).

**What the atomic tier actually buys, measured:** the completed T2 DFT reference carries a **signed
bias of −10 to −14% on stiffness, with shape sub-percent**. That is the honest content of "atomically
accurate" — not exactness, but a *certified, signed, quantified* error band on named observables.

**A 4090 sandbox could certify:** exact integer conservation of the constituent/occupancy/momentum
ledger across every shard and every refinement, globally and per-shard, bit-for-bit; bit-exact replay
of a given scene on a given device; grain-scale contact and cohesive response within T3/T4 validity
domains with signed error bands; statistical composition of any materialized ensemble against its
descriptor's declared law at `CERT_Z = 5.0`; and — the thing the card uniquely buys — **one grain of
sand resolved to its 1 µm subgrains**, which is the Z0 GRAIN tier held entirely resident.

**It must refuse:** sub-d50 crack paths and nucleation sites (`GrainFloor` — "`not_computable_from`
in this tier's clothes", `:195`); fields within ~1 nm of a crack tip; bond rearrangement, excitation
or coordination change (T1/T2 floors); damping ratio and restitution as material constants
(falsified as such, `:284`); everything in the four refusing tiers; and — specific to this design —
**any claim that a df64 run reproduces the f64 reference bit-for-bit**. The refusals are the product.
A sandbox that answers every question has stopped certifying anything.

One refusal is currently *silent* and should not be. At the shipped fracture fanout of 4, **every**
statistical check sits below its resolution floor (`CERT_FLOOR_MEAN = 8`, `CERT_FLOOR_SPREAD = 32`)
and rides along unresolved — today's passing descriptor certificate is *silent*, not *supporting*. A
GPU materializer drawing thousands of children per engine is the first configuration where that
certificate has teeth. At Z0 the quenched Weibull draw (3.8 µm / 0.42 µm / 0.11 µm for
weak/median/strong) is what decides certify-vs-`GrainFloor` at grain tier, so the draw is not a
detail — it is the certificate's deciding variable.

---

## 8. Gap list

| # | gap | scope |
|---|---|---|
| **G0** | **The architecture question is unresolved, and it is a product question, not an engineering one:** (a) ~29,800 concurrent scenes, or (b) one scene with a 10⁴-deeper frontier. They want different kernels. **Answer this before building anything.** | decision, not code |
| **G1** | **No contact solver in the throughput model.** §4's rates measure layout, not granular physics. The 80,000× event-budget headroom survives a 100× penalty, so this is no longer a *feasibility* risk — but it is still unmeasured. | measure before (b) |
| **G2** | **Materialization cannot run on device.** SplitMix64 is portable; the draw's `log`/`cos`/`pow` are not bit-identical between `libm` and libdevice. Keep it host-side, or supply bit-exact software transcendentals. | host-side is the cheap answer |
| **G3** | **No GPU backend exists.** Minimal scope: a separate crate `crates/holon-gpu`, **outside the workspace** (the `engine-compare` precedent, `Cargo.toml:21-25`), so the core's `no_std`/zero-allocation/isolation gates in `ci-gates.sh` stay valid. CUDA via `cust`, not wgpu: **WGSL has no f64 at all**, which forecloses D1 outright. | new crate, no core deps |
| **G4** | `FractureModel`/`ImpactModel` hold `Rc<RefCell<WallChart>>` (`fracture.rs:348`, `impact.rs:165`) — **`!Send`**, so they cannot cross a thread today, let alone a device. | refactor to a passed workspace |
| **G5** | Every solve allocates fresh `Vec`s. `incremental.rs::Workspace` is the only reusable-workspace precedent; the device needs that pattern everywhere. | mechanical |
| **G6** | **`ledger_for` checks only the constituents lane** (`tier.rs:225-242`). A chart writing REG+ occupancy — as the core's own idioms already do at 2× — passes sizing and overflows at `checked_combine` at 1/2 to 1/6 of the sized capacity. Compute the cap from the declared lanes and refuse at declaration time. | small, high value |
| **G7** | `holon-sandbox/tier.rs` states its sandbox constituent count **three ways** (header prose 6.60e8; `constituents` field 622,080,000; `fill = 0.45` implies `ledger()` = 777,600,000) with no test asserting they agree; and `three_tiers_refuse_and_each_names_why` asserts `== 4`. | reported to that lane |
| **G8** | Certifier growth exponent **~2.86** (`22/86/342/1366` materializations → `0.0001/0.0023/0.129/6.94 s`). **This, not compute, is what limits the sandbox.** Sharding attacks it (1.64× from locality alone, plus N-way parallelism) but does not change the exponent. Design against the post-fix world; the incremental certifier and the core C1 fix are both in flight. | the real constraint |

---

## 9. The design in one paragraph

Do not build a GPU backend to make one sandbox fit — at the certificate's own residency it already
fits, with 80,000× of event budget to spare, and the binding constraint is the certifier's ~2.86
growth exponent, which a GPU does not touch. Build one if the answer to G0 is *many scenes* (~29,800
concurrent throws, memory-bound) or *one deeper scene* (the resident frontier pushed 10⁴ below what
the certificate demands, which is where atomic accuracy actually lives, and which tops out at about
one grain of sand resolved to 1 µm). Either way: shard into arenas of ~256 holons, each with its own
declared g0 and root, related by pairs of boundary indices — values, not a new class. Run them as one
persistent kernel, one block per engine, 10 engines per SM, holons SoA (4.0× over the 56 B AoS
header). Step interiors sequentially in **native f64** with strict intrinsics, which costs 2.57×
against df64 and buys back a fourth bit-exact target. Keep the REG+ ledger in integers, where
associativity makes determinism free. Exchange by snapshot-then-apply over disjoint pairs, no atomics
on the exchange path, and certify the boundary by **re-planning the transfer**, because balance-based
gates provably miss transfers doubled or dropped on both sides. Then refuse, loudly, every question
below d50 — and fix `ledger_for` before some chart turns REG+ occupancy on and discovers the cap was
never 3.54 for it.
