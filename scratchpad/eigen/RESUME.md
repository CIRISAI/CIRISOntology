# Eigen-alignment run — interruption-recovery protocol

Every stage checkpoints to disk; agents and sessions hold NO state that matters.
After ANY interruption, run the stage table top to bottom; each stage is skipped
if its artifact exists.

| stage | artifact (done-marker) | resume command (from scratchpad/eigen/) |
|---|---|---|
| gauge | out/gauge_verdict.json | qenv/bin/python gauge.py && python gauge_verdict.py |
| embeddings | cache/eigen_cache_*.jsonl (sha256 in cache manifest) | qenv/bin/python run_embed.py (idempotent; reuses cache) |
| P2-pos arm | out/p2pos.json | qenv/bin/python run_p2pos.py |
| RATCHET arms | out/ratchet.json, out/ratchet_embed.json | qenv/bin/python run_ratchet.py; run_ratchet_embed.py |
| extras/secondary | out/extras.log ends "[sec-N1] null done" | qenv/bin/python run_extras.py |
| MAIN analysis | out/main_primary.json | setsid nohup qenv/bin/python run_main.py >> out/main.log 2>&1 & (PID → out/main.pid; NOT resumable mid-run — restarts its permutations from seed 20260819, reuses all caches, ~no API cost) |
| results doc | ../EIGEN_ALIGNMENT_RESULTS.md | qenv/bin/python summary.py (needs main_primary.json) |
| verify | verifier agent verdict in session record | orchestrator spawns the N9-VERIFY agent per the Round-2 script |

qenv = /home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python
Spend so far: $0.0039 embeddings (usage.json). run_main makes ZERO API calls.
Rule: long compute runs DETACHED (setsid nohup) with disk logs — session death
must never kill the computation, only the narration.
