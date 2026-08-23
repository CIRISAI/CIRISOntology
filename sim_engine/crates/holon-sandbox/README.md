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
grains of sand** counted in atoms. The sandbox in this demo is 1.9e8 times over that,
and `checked_combine` returns `None` rather than a wrong number — which is why zoom here
is a re-root, licensed by `CIRIS_HOLON_ENGINE.md`'s own "there is no absolute maximal
holon".

## Layout

| file | what it holds |
|---|---|
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
- Three tiers have no evaluator in this repository and say which open item is the
  reason.
