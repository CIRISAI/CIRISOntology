# EIGEN2 RUN — RESUME MAP  (keep current; read me first if resumed)

Prereg (GOVERNS, frozen §24): /home/emoore/CIRISOntology/scratchpad/EIGEN2_PREREG.md
Workdir: /home/emoore/CIRISOntology/scratchpad/eigen2run/
Venv: /home/emoore/CIRISOntology/scratchpad/temporal-share/qenv/bin/python  (numpy/scipy; NO sklearn)
System python3 (has sklearn/transformers) is used ONLY for D-B1's TF-IDF+logistic and tokenizers.
v1 machinery (READ-ONLY, never modified): /home/emoore/CIRISOntology/scratchpad/eigen/
Rules: NO git ops. Never print the DeepInfra key. Absolute paths. All long jobs detached
(`setsid nohup ... >> logs/X.log 2>&1 &`); `$!` is the wrapper PID, so pgrep with
`pgrep -af '[q]env/bin/python'`. Deviations from the prereg go in AMENDMENTS.md BEFORE they run.

| # | stage | done-marker | resume command |
|---|---|---|---|
| 0 | §7.2 unit tests | `out/UNITTESTS.done.json` | `qenv/bin/python test_split.py` |
| 1 | §8 gauge (K=11, n=237) | `out/GAUGE.done.json` | `setsid nohup .../python gauge11.py >> logs/gauge.log 2>&1 &` |
| 2 | §20 panel (post-freeze) | `out/PANEL.done.json` | `setsid nohup .../python3 run_panel.py >> logs/panel.log 2>&1 &` |
| 3 | §3.4 token pass + §3.3 embeddings | `out/EMBED.done.json`, `cache/MANIFEST.sha256` | `setsid nohup .../python embed_e2.py >> logs/embed.log 2>&1 &` |
| 4 | §12 positive control (VG2) | `out/POSCTRL.done.json` | `.../python poscontrol.py` |
| 5 | §15-VG1 placebo gate FIRST, then full analysis | `out/ANALYSIS.<arm>.done.json` | `.../python analysis.py <arm>` |
| 6 | §11 diagnostics D-B1/B2/B3/S1 + VG3 | `out/DIAG.done.json` | `.../python diagnostics.py` |
| 7 | results | `/home/emoore/CIRISOntology/scratchpad/EIGEN2_RESULTS.md` | hand-written from out/*.json |

## Status
- **stage 0 DONE, PASS.** `out/unit_tests.json`: 200 draws, 0 violations, ±1 on kind AND
  batch simultaneously, halves exactly 237/237 every draw, 200 distinct splits, min
  half-class 18 (V3 floor 12). Label facts re-verified: 474 items; class counts
  {39,40,40,59,59,37,40×5}; 40 batches (6×11, 34×12); kind×batch cells ∈ {0,1,2} with
  396/39/5; 35 batches carry 11 distinct kinds, 5 carry 10; 10 odd-degree vertices → 484
  edges (even, guard 1 satisfied).
- **stage 1 GAUGE DONE.** `out/gauge11_raw.json`, `out/gauge11_summary.json`,
  `out/gauge_ruling.json`. σ_R = **1.1835** (admissible scales 2.5–6.0) → §8.1 row 2:
  Tier 2's "not 6, not 13" **RETRACTED IN ADVANCE**; V8 does **not** fire. R̂ = 7.04–8.42
  over the admissible scales, so |R̂−10| = 1.58–2.96 > σ_R everywhere → **P1b will be
  UNDECIDED, K2 cannot fire** (§8.2 statement 1 confirmed on v2's own gauge). ρ_gauge
  0.429–0.630 across Scenario A (V3b clear) vs 0.194 at Scenario B's edge (V3b fires) —
  §8.2 statement 2 confirmed. Scale-0 row Ω=0.010545 ≈ k/d=0.010742.
- **stage 2 PANEL** running/near done → `out/panel_base.jsonl`, then `panel_analysis.py`.
- **stage 3 EMBED DONE.** n=474, **no drops** (V7: max 167 tok vs 32768/512), V2 clean on
  all three arms (0.99991/1.00000/0.99991), **V1 fires on no class on any arm** (worst
  per-class median cos 0.9944 qwen / 0.99865 bge / 0.9960 bare, all < 0.999), V1b clear,
  rank(B)=10 everywhere, V3 min class 18, V4 inert (1 pair > 0.99 on qwen, 0 elsewhere).
  Embedding spend $0.0015.
- **stage 4 VG2 DONE, does NOT fire on the primary.** N=99 (prereg predicted 95).
  qwen Ω_PC(3)=0.4435 vs null 0.1469, p=0.0020 (0/500), LOO top-1 0.653 ≥ 0.60 → PASS.
  bge p=0.0020 (0/500) but top-1 **0.5993, one item short of 0.60** (item-LOO 0.6094
  passes) — the sharpest interpretive call in the run; both readings must be reported.
- **stage 6 partial:** D-B1 done — batch lift **0.334×** (undetectable, far below the 1.18×
  that forced the rebuild); kind lift 4.508× from the UNCHANGED text. D-S1 done and read
  BEFORE any N1b p existed: span spread **25.75×**, KW p=4.5e-52 → **> 20×, so an N1b
  failure is reported as SPAN-CONFOUNDED, not as a taxonomy verdict**. VG3 not fired.
- **stage 2 PANEL DONE.** 1422 judgments, $0.1729. Fleiss κ=0.7396 (3 models, 468 items;
  PLANE was 0.687), modal-vs-authored 0.715 (clear 0.701 / hard 0.757), **Record
  false-positive rate 0.0%** (staked 5% threshold does not fire), 0 NO-FIT votes, 6
  off-vocabulary (all null). **Secondary label arm is VOID by V3**: Premises and Structure
  receive ZERO modals and Circumstances has 12, so 3 classes sit below V3's floor.
- **A6 DEFECT FOUND AND HANDLED (see AMENDMENTS.md).** The frozen Z contains the domain and
  batch dummies, which ANNIHILATE the domain-11 rival and D-B2's batch label on the `res`
  arm (‖C_domain11‖ = 2.95e-14 vs 5.68 unresidualized; rank comes back 11 not 10). The
  pinned rival conjunct is therefore STRUCTURALLY UNINFORMATIVE on `res`/`spandom`.
  Corrective post-freeze arms launched: `analysis.py rivalnodom` (Z minus domain) and
  `db2_nobatch.py` (Z minus batch). The `raw` arm was already uncontaminated.
- **stage 5 DONE:** seven configs (primary/witness/ablation/raw/spandom/clearonly +
  rivalnodom), ~1–2 h. Each checkpoints `out/analysis_<cfg>.ckpt.npz` every 50 perms and
  RESUMES from it; re-launch with the same command if killed.
  Verify any finished arm with `.../python verify.py <cfg>` (independent re-derivation).

## Key frozen constants (from the prereg, do not re-derive)
- PRIMARY = instructed `Qwen/Qwen3-Embedding-0.6B`, `res` nuisance arm, k=11 primary with
  k=10 rank-matched co-primary. WITNESS = `BAAI/bge-large-en-v1.5`. ABLATION = bare Qwen.
- Instruction string (verbatim, incl. newline):
  `Instruct: Identify what kind of commitment changed between the two versions.\nQuery: `
- VG1 Gate A: `p_gap_N1 ≤ 0.01`. Gate B: `δ_median ≥ max(0.010, gap-null p99)`.
- Forward bands on Ω*(11): B <0.03 | middle 0.03–0.15 | A 0.15–0.28 | missed-high >0.28.
  Secondaries: δ∈[0.020,0.065], ψ∈[0.15,0.40], Ω*_C1P∈[0.12,0.25].
- Ladder rungs: cell=CHANGE-CARRIED ALIGNMENT (Ω(10) same cell); Ω*≥0.190; ψ≥0.25 point
  AND interval lower bound ≥0.15; WG1 witness replication; ablation not INSTRUCTION-DEPENDENT.
- N_perm=500, 200 splits, spend cap $3.00 total (panel ≤$1.00).

## FINAL STATE (run complete)
- **VERDICT CELL: CHANGE-CARRIED ALIGNMENT** on all seven arms. Instrument VALID (VG1 held,
  Gate B by 1.097x). Omega*(11) = 0.27634 STRONG. **Forward prediction Scenario A CONFIRMED**
  (band [0.15,0.28]). **psi = 0.1389 -> "the reading is mostly context"**.
  **P1b UNDECIDED, K2 cannot fire.** No kill fired, no VOID fired.
  **Ladder: rungs 1,2,4,5 PASS; rung 3 FAILS -> PROMOTION INELIGIBLE.**
- Results: /home/emoore/CIRISOntology/scratchpad/EIGEN2_RESULTS.md (complete)
- Assembled machine-readable summary: out/ASSEMBLED.json
- verify.py (logs/verify_primary.log) is SAME-CODE re-execution, not an independent
  implementation (it imports pipeline.py and re-reads stored perms) — see RESULTS S11. All
  headline numbers match to <=1.1e-15; the ONLY mismatch is the annihilated Omega_domain11
  (6.6e-4 then 1.7e-3), confirming AMENDMENTS A6. The independent leg is the hostile
  verifier's own reimplementation (Omega to 2e-16, fresh 200-split family, every cell held).
- Verifier returned RELEASE-WITH-CORRECTIONS; all 12 items + lows + strengthenings applied
  2026-08-20. Two new amendments: A7 (poscontrol M1 regex, N=99 not 95) and A8 (rivalnodom
  N1b added after an unfavourable cell — ordering stated plainly in RESULTS S18.1).
- Spend $0.174653 of $3.00.
