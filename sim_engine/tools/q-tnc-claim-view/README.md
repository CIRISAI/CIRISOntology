# q-tnc-claim-view

This is a diagnostic-only, independent contraction View over a frozen `q8-mps`
state. It is deliberately a standalone Cargo workspace: TNC does not enter q8's
zero-runtime-dependency graph and cannot participate in the Habit it audits.

## OBJECT mapping

| OBJECT term | This instrument |
|---|---|
| World | the immutable MPS returned by one q8 DMRG solve |
| Habit | `q8_mps::dmrg::run_from` |
| View A | explicit expansion and bare fermionic Hamiltonian application |
| View B | TNC/TBLIS contractions of norm, energy, and local content |
| correspondence `R` | q8 `[s][left][right]` tensors plus `[empty,up,down,full] <-> [up,down]` |
| Door | live `q-seam` exact solve |
| Record | both-start receipt, fixed contraction path, thresholds, and mutation |

The content square uses identity transport for physical scalar claims. It passes
only if the direct and TNC Views agree within `1e-10`. The planted mutant removes
the intervening Jordan-Wigner `Z` string and must move the energy by more than
`1e-6`.

## Build and run

Prerequisites are Rust 1.85 or newer, a C/C++ build toolchain, CMake,
`pkg-config`, and `libclang` for TBLIS bindgen.

```sh
./bootstrap.sh
cargo run --release -- 8 16 32
```

`bootstrap.sh` checks out
[`qc-tum/TNC@0b35c581`](https://github.com/qc-tum/TNC/commit/0b35c58146751cafeadcf31684cd51ae8f4602c2)
under the ignored `vendor/` directory and applies the small pinned
`local-only` feature patch. Upstream TNC supports local contraction in its API,
but its manifest currently makes MPI, HDF5, KaHyPar, and path-finding machinery
unconditional build dependencies. The patch gates those modules without
changing tensor representation or contraction code. This packaging misfit is
kept visible; it is not silently absorbed into q8.

## Recorded N=8, U=16, chi=32 receipt

Run on 2026-08-24 with `OMP_NUM_THREADS=1`:
the exact stdout receipt is tracked at `receipts/n8-u16-chi32.log`.

| measurement | Neel start | doublon-hole start |
|---|---:|---:|
| q-seam energy | -1.262136132334283 | -1.262136132334283 |
| q8 reported energy | -1.262135272883228 | -1.262135238326167 |
| direct returned-state energy | -1.262135272871493 | -1.262135238322762 |
| TNC returned-state energy | -1.262135272871480 | -1.262135238322747 |
| max TNC/direct claim defect | 1.221245e-14 | 1.487699e-14 |
| TNC/q-seam energy defect | 8.594628e-7 | 8.940115e-7 |
| erased-JW-string energy move | 2.487094 | 2.487092 |
| worst left-canonical defect | 2.020 | 3.183 |
| worst local Lanczos residual | 9.854e-4 | 1.012e-3 |

The two returned-state energies differ by only `3.454873e-8`. TNC acquits the
q8 report/MPO observation boundary at this point: the reported value is the
global energy of the returned MPS to `1.18e-11` or better. The remaining
roughly `9e-7` exact error travels with the state and coincides with broken
left-canonical form and local-solve residuals around `1e-3`; the live repair
target is therefore the Habit, not another reporting adapter.

This is a narrow, mutation-checked content-bearing claim-transport instance. It
does not establish general cross-root transport, nontrivial holonomy, a Q10
gate, or SOTA performance.
