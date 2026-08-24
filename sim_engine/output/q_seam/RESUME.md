# Q-SEAM RESUME — detached run ledger

## Q5 sweep (running)
- Launch: `setsid nohup ./target/release/q_seam_run > output/q_seam/q5.log 2>&1`
- Done marker: `output/q_seam/q5.DONE` (contains the exit code)
- Output: `output/q_seam/q5.json`, log `output/q_seam/q5.log`
- Covers: 5 N x 14 U = 70 configurations, exactness gates + chart + certificate + mutants.
- If the marker is absent, the run is still going or the box died; rerun the launch line, it is
  fully deterministic (pinned Lanczos seed, pinned SCF guesses) and overwrites its own output.
