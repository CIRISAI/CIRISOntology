# holon-sandbox — the certified multiscale sandbox

Sand, in a box, at every zoom tier of one recursive holon. Zoom in until the vacuum,
out until the universe, and throw something at any of it. Rust and WebAssembly own
every holon, contact and certificate; Canvas owns pixels and pointer input and nothing
else.

```sh
cd sim_engine
./crates/holon-sandbox/build-web.sh
cd crates/holon-sandbox/viewer
python3 -m http.server 4188
```

Then open `http://127.0.0.1:4188`, pick a zoom tier, and click the sand.

```sh
cargo test -p holon-sandbox --release
cargo run -p holon-sandbox --example sandbox_report --release
```

## What is actually being claimed

Zoom is not a rendering trick. Each tier is a **re-rooted `RuntimeArena`** with its own
declared grain constant `g0`, and the frontier you see is the one the engine certified
for the throw you made. The certificate has four visible outcomes and three of them are
refusals; the refusals are the point.

The ladder is not a design choice. `GrossState::constituents` is a `u64` and
`Holon::grain_units` is a `u32`, and those two integers decide how far one arena can
zoom: 6.42 decades for a dense 3D scene, 9.63 for the grain ratio whatever the density.
One 0.5 mm quartz grain is 5.216e18 atoms, so the ledger holds about **three and a half
grains of sand** counted in atoms — for THIS chart. `GrossState` has three integer lanes
and which one binds is a property of what the chart writes: this one writes only
`constituents`, but a chart whose leaves carry full REG+ occupancy is bound by the
`occupancy` lane at **0.59 grains**, six times tighter (credit to the 4090 study for
catching that the general bound is not the constituents lane). The sandbox counted in
atoms is 2.5e8 times over, and `checked_combine` returns `None` rather than a wrong
number — which is why zoom here is a re-root, licensed by `CIRIS_HOLON_ENGINE.md`'s own
"there is no absolute maximal holon".

The re-root itself is certified: `tier::reroot` reports whether a zoom lands on exactly
one parent terminal holon, a whole number of them, or inside one, and where it lands on
exactly one the ledger identity is checked to the last constituent.

## Layout

| file | what it holds |
|---|---|
| `src/gauge.rs` | the vacuum tier over `ciris_sim_core::quantum_link`, and the labelling constraint the RouteGauge kill imposes on it |
| `src/incremental.rs` | the certifier: same selector, no restart, `O(n log n)`; the bit-for-bit equivalence gate against `certify_runtime_adaptive`, and five planted mutants it has to catch |
| `src/tier.rs` | the eight tiers as values on one holon, the ledger arithmetic, and `l_ch` per tier |
| `src/chart.rs` | the quadtree chart and exact integer apportionment |
| `src/scene.rs` | the generator, the resolution surrogate, and where a cohesive law is derived or refused |
| `src/sim.rs` | one solver for every tier that runs, and the throw |
| `src/lib.rs` | the WebAssembly boundary: flat `f32` buffers, one JSON blob, scalars |
| `viewer/` | Canvas and pointer input |

## Honesty notes carried in the code, not just here

- The chart is 2D; the ledger is 3D. A cell stands for a column of matter and weighs
  that column.
- Fracture energy is 1 J/m² at the crystal tier and 110 J/m² at the continuum. The
  hundredfold gap is **minted** at the coarse tier, not transported up, so the zoom
  shows two numbers and never interpolates.
- Contact at the sandbox is **softer than quartz** by a declared discrete-element
  criterion, and by how much is shown. Real quartz stiffness cannot be explicitly
  integrated at interactive rates.
- Gravity is chart data, one uniform value, no per-holon field and no stage knob.
- Three tiers have no evaluator in this repository, and each names both the open item
  that causes it AND the gate whose passing would lift it.
- The vacuum tier renders quantum-link physics and must NOT imply that the taxonomy's
  route object and the gauge flux share a carrier — `Core/RouteGauge.lean` killed that
  identification by machine. What it may say, and does, is that link charge conjugation
  acts on the route Hamiltonian as time reversal: one finite symmetry read in two
  languages, a dictionary entry rather than a shared carrier.
- Both tiers that certify sit inside the 1–10^7 s⁻¹ strain-rate band no experiment
  covers. The certificate panel says so where the number is.
