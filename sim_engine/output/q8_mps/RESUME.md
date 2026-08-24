# q8-mps full-grid gate run — RESUME

**Started:** 2026-08-23 (this session). **Command:**
```
setsid cargo test --release --manifest-path crates/q8-mps/Cargo.toml --test full_grid_gates \
  -- --ignored --nocapture > output/q8_mps/full_grid_gates.log 2>&1 &
```

**What it's doing:** `tests/full_grid_gates.rs`'s single `#[ignore]`d test, the staked
N=8,10,12 x U/t in {0,1,4,16} grid, chi=256, gating G2/G3-secondary/G6/G0-2/G7 per
`Q8_MPS_PREREG.md` §4. N=12's exact reference is a FRESH q-seam Lanczos solve (dim 853776,
~2.7GB resident) — `Q_SEAM_PREREG.md` D3 excluded N=12 only from the Q6 share pass, not from
ground-state computation, so this is new compute, not a reuse.

**Expected runtime:** unknown precisely; a chi=128 timing spot-check at N=8 took ~30s per
config, chi=256 roughly 4x that. Extrapolated to the full 12-config grid across N=8,10,12,
very roughly 45-90 minutes. Progress lines print per configuration to the log (stdout via
`--nocapture`, `eprintln!` used deliberately so they are not test-harness-captured/suppressed).

**Done marker:** `output/q8_mps/full_grid_gates.DONE` — written by the wrapper shell only
after the `cargo test` process exits, containing its exit code. Absence means still running
OR the session died before it could write the marker; check `full_grid_gates.log`'s tail and
whether the process is still alive (`pgrep -af full_grid_gates`) before assuming either.

**On resume:** tail `output/q8_mps/full_grid_gates.log` for the last progress line and any
per-configuration `FAILED` lines already printed; check `full_grid_gates.DONE` for the final
exit code once present. A nonzero exit with failure lines in the log is a real gate finding
(report it, do not re-run with loosened tolerances). A crash/OOM (most likely at N=12) shows
up as the log stopping mid-configuration with no DONE marker — report which configuration was
in flight, do not silently drop N=12 from the results.
