# K2 — second judge, and the first execution of the protocol's length guard (2026-08-24)

New file, for an integrator to fold in. `RESULTS_K2.md` is not edited by this lane.
Design frozen in `SECOND_JUDGE_PREREG.md`, committed `f283522` **before any calibration
call was made**. `judge.py` and `analyze.py` used **unmodified**; frozen 92-item split;
sealed pairing seed 20260822; responses **not** regenerated.

---

## VERDICTS

**1. The fired kill STANDS, unchanged.** Soft-run C over B = 0.531 (26 W / 23 L of 49
decisive), p = 0.7754 — reproduced from `judge_soft92_pairs.jsonl` this session, not quoted
from prose. The second judge cannot overturn it: its reading is length-confounded by the
protocol's own conjunctive test and rests on 17 decisive pairs with 81.5% flips. The
primary's number additionally **passes** the section-5 guard, run here for the first time.

**2. The secondary SURVIVES, restated.** The second judge reversed it in sign — the
escalation condition I staked in advance — and the reversal is a **length artifact**.
Controlling for length, the primary says C is significantly **worse** than the bare 0.6B
model (arm β = −0.907, p = 0.00045 soft; −0.716, p = 0.0020 gold), and the second judge says
C is **indistinguishable** from it (β = +0.218, p = 0.394 soft; +0.346, p = 0.162 gold).
**Once length is controlled, neither judge says C is better than A.** The product-direction
finding is not contradicted; its strongest form is "C is worse, or at best no better".

**3. The single-judge caveat is PARTIALLY discharged — not by concurrence.** Of four
candidate second judges, three failed calibration and the fourth failed the confound guard,
so no second judge can issue a valid verdict. What is now discharged is the *unexplained*
part: the reason there is one judge is measured rather than asserted, and the primary is the
only judge of five that is both sensitive enough and length-clean.

**4. A DEFECT IN THE EXISTING RECORD, found by the protocol's own guard.** The gold-run
side-by-side C-vs-B number in `RESULTS_K2.md` (0.608, p = 0.161) **is length-confounded**
(length p = 0.0396, arm p = 0.098). No verdict changes — it was already reported as not
significant — but that line should carry the caveat.

---

## Judge qualification — gates UNCHANGED, no threshold moved

| judge | family | identical-pair slot-1 | sensitivity (bar 0.90) | status |
|---|---|---|---|---|
| `gemma3:12b` (primary) | Google | 0.868 | 0.902 | PASS |
| `qwen3:14b` (prior DQ) | Alibaba | 1.000 | 0.870 | FAIL |
| `phi4:14b` | Microsoft | 0.837 | 0.859 | FAIL (sens) |
| `mistral-nemo:12b` | Mistral/NVIDIA | 1.000 | 0.728 | FAIL (both) |
| **`llama3.1:8b`** | **Meta** | **0.967** | **0.935** | **PASS — ran the pairs** |

All five recomputed from the `judge_*_calib_*.jsonl` artifacts, not from `judge_all.log`.
Candidates were third-family to **both** the Qwen generator (protocol §3's correlated-prose
concern) and the gemma3 primary. All three new candidates were calibrated regardless of
early success, so the record is not truncated. `llama3.1:8b` has the highest sensitivity of
anything tried, above the primary's own 0.902.

**The 0.90 bar is attainable, checked not assumed.** Three of five candidates missing it
made the gate look harsh, so the positive control was audited: `judge.py` degrades a response
to its first sentence, and on arm A only **2 of 92** items have no gap at all (median
degraded/intact char ratio 0.464). Ceiling ≈ 0.989. The misses are genuine judge limitations.

## Second judge, raw readings (`llama3.1:8b`)

| run | comparison | decisive | flips | C wins | rate | p |
|---|---|---|---|---|---|---|
| soft | C vs B | 17 | 75 (0.815) | 13 / 4 | 0.765 | 0.0490 |
| soft | C vs A | 56 | 36 (0.391) | 43 / 13 | 0.768 | 0.0001 |
| gold | C vs B | 15 | 77 (0.837) | 10 / 5 | 0.667 | 0.3018 |
| gold | C vs A | 49 | 43 (0.467) | 38 / 11 | 0.776 | 0.0001 |

Taken at face value this disagrees with the primary on both comparisons and **reverses the
secondary in sign**. It does not survive the protocol's own guard.

## The length guard — JUDGE_PROTOCOL §5, as SPECIFIED, run for the first time

§5 says: *"Fit `choice ~ length_diff + arm` (logistic). If `length_diff` is significant and
`arm` is not, the comparison is reported as length-confounded and a length-matched re-run is
required before any verdict."* `analyze.py` only ever computed the **marginal** "did the
longer response win"; **the conjunction the protocol actually stated had never been evaluated
for any judge, including the primary.** `length_guard.py` runs it, symmetrically, on both.

| judge | run | cmp | length_diff | arm | §5 |
|---|---|---|---|---|---|
| llama3.1 | soft | C vs B | +5.342, p = 0.036 | +0.331, p = 0.110 | **FIRES** |
| llama3.1 | soft | C vs A | +5.396, p = 0.0029 | +0.218, p = 0.394 | **FIRES** |
| llama3.1 | gold | C vs B | +6.779, p = 0.0195 | +0.248, p = 0.306 | **FIRES** |
| llama3.1 | gold | C vs A | +4.038, p = 0.0147 | +0.346, p = 0.162 | **FIRES** |
| gemma3 | soft | C vs B | +3.035, p = 0.130 | +0.064, p = 0.688 | clean |
| gemma3 | soft | C vs A | +2.470, p = 0.138 | **−0.907, p = 0.00045** | clean, arm survives |
| gemma3 | gold | C vs B | +3.993, p = 0.0396 | +0.264, p = 0.098 | **FIRES** (defect 4) |
| gemma3 | gold | C vs A | +2.435, p = 0.094 | **−0.716, p = 0.0020** | clean, arm survives |

The marginal statistic agrees: `llama3.1` picked the longer response 0.595 (p = 0.0003) soft
and 0.587 (p = 0.0010) gold; `gemma3` 0.466 (p = 0.210) and 0.501 (p = 1.000).

**Model-free confirmation — decisive pairs split by which arm is longer.** C is ~40% longer
than A by construction (78 vs 56 tokens), so this is the check that needs no model:

| judge | run | cmp | C shorter | C longer |
|---|---|---|---|---|
| llama3.1 | soft | C vs B | 4/8 = 0.500 | **9/9 = 1.000** (p = 0.0039) |
| llama3.1 | soft | C vs A | 3/4 = 0.750 | 40/52 = 0.769 |
| llama3.1 | gold | C vs B | 2/7 = 0.286 | **8/8 = 1.000** (p = 0.0078) |
| gemma3 | soft | C vs A | **1/6 = 0.167** | 19/60 = 0.317 |
| gemma3 | gold | C vs A | **2/8 = 0.250** | 23/61 = 0.377 |

The primary's finding is in its **strongest** form: C loses in *both* length strata, and
loses **harder when it is shorter** — the confound runs in C's favour and C still loses.
The second judge's C-vs-B win is carried entirely by the C-longer stratum (17 of 17).

## Inter-judge agreement (protocol §3)

| run | cmp | 3-way raw / κ (n) | both-decisive raw / κ (n) |
|---|---|---|---|
| soft | C vs B | 0.516 / 0.156 (91) | 0.833 / 0.636 (12) |
| soft | C vs A | 0.380 / 0.136 (92) | 0.711 / 0.434 (38) |
| gold | C vs B | 0.462 / 0.077 (91) | 0.700 / −0.154 (10) |
| gold | C vs A | 0.348 / 0.086 (92) | 0.706 / 0.393 (34) |

On items **both** judges found decisive they agree fairly (κ 0.434 / 0.393 on C vs A). The
aggregate reversal is therefore not wholesale disagreement about quality; it is a **selection
effect in which items become decisive**, and the second judge's length preference is what
selects C-longer items into decisiveness. Soft C-vs-A confusion (primary → second):
`A→FLIP 26, C→C 17, FLIP→C 16, A→A 10, A→C 10, FLIP→FLIP 8, FLIP→A 2, C→FLIP 2, C→A 1` —
only **one** item is an outright C-to-A reversal.

## A piece of my own prereg, falsified by measurement

`SECOND_JUDGE_PREREG.md` argued that an identical-pair slot-1 rate of 1.000 is a *de facto*
disqualification because order-balanced scoring would then yield zero decisive pairs. **That
reasoning is wrong, and the data here falsify it.** Identical-pair bias does not transfer to
real pairs — it reverses sign:

| judge | identical-pair slot-1 | slot-1 on REAL pairs (soft) |
|---|---|---|
| gemma3:12b | 0.868 | **0.362** |
| llama3.1:8b | 0.967 | **0.247** |

`llama3.1:8b` measured 0.967 and still returned 56 decisive C-vs-A pairs. Calibration 1
measures **tie-breaking on identical content**, which is a degenerate behaviour, not the
position effect that operates when there is real content to compare. Consequences: the
protocol's Calibration 1 is not a valid predictor of real-pair position behaviour and should
be reported as a tie-break diagnostic only; `qwen3:14b`'s disqualification rests **solely**
on the sensitivity gate (0.870 < 0.90), which is sufficient and untouched; and order-balanced
scoring remains immune to position bias by construction, so no verdict is affected.

## ADDENDUM 2026-08-24 — Calibration 3 exists now, and it separates the two judges

The gate that was missing when this run happened was staked in `AMENDMENT_J2_LENGTH_GATE.md`,
then built and run on all five judges. It pairs each arm-A response against a padded copy of
itself, so content differs only in length, and it consumes no real pair.

| judge | picked the PADDED copy | n | two-sided p | gate |
|---|---|---|---|---|
| `gemma3:12b` (primary) | 0.505 | 91 | 1 | **ADMIT** |
| `llama3.1:8b` (second judge) | 0.783 | 92 | 4.6e-08 | **REJECT** |
| `phi4:14b` | 0.696 | 92 | 2.2e-04 | REJECT |
| `mistral-nemo:12b` | 0.272 | 92 | 1.4e-05 | ADMIT (prefers intact) |
| `qwen3:14b` | 0.478 | 92 | 0.755 | ADMIT |

This confirms the post-hoc diagnosis above on a **constructed** instrument: the length
domination that had to be inferred from the section-5 fits and the 0.595 marginal is directly
measurable, and the second judge picks contentless padding over the identical unpadded text in
both slot positions (0.619 and 0.920). The primary does not (0.505, and not slot-locked at
0.582 slot-1). `mistral-nemo:12b` is slot-locked and its ADMIT here is uninformative — see the
disclosed seed degeneracy in the amendment; it stays disqualified on sensitivity (0.728).

**No number in this document changes, and the two-judge record stands exactly as reported.**
Calibration 3 was added after this verdict closed and does not void completed work; it means a
judge with this failure mode cannot be admitted again — `judge.py pairs` now refuses to judge
a real pair for a model without a passing Calibration 3.

## Artifacts

`SECOND_JUDGE_PREREG.md`, `RESUME_SECOND_JUDGE.md`, `run_calib_second.sh`,
`run_pairs_second.sh`, `calib_second.log`, `pairs_second.log`, `length_guard.py`,
`compare_judges.py`; `judge_soft92_{phi4,nemo,llama31}_calib_{bias,sens}.jsonl`;
`judge_{soft,gold}92_llama31_pairs.jsonl` (368 judgments each). Commits `f283522`
(prereg + build log), `72a1482` (instruments), `b174a97` (calibration evidence).

Calibration 3 artifacts: `AMENDMENT_J2_LENGTH_GATE.md`, `calib3.py`, `calib_length.py`,
`run_calib3.sh`, `gate_calib3.sh`, `calib_length.log`, and
`judge_soft92_{gemma3,llama31,phi4,mistral-nemo,qwen3}_calib_length.jsonl` (92 judgments each).

## Build-verify (owed by `9f95754`) — found broken, then REPAIRED

**Found broken.** `bin/generate` did not compile: `ciris_nl::chat` undeclared (chat.rs
committed at `9f95754` but no lib.rs declared `pub mod chat;`) and `Session::generate`
absent (native.rs had only a private, llguidance-constrained `complete()`). Exit 101, 5
errors. `build_verify.log`, commit `f283522`. Independently reproduced by ci-manager-2 from a
cold `--manifest-path` build — two lanes, two routes, same failure.

**Repaired in `db6b4b7`**, both causes in one commit (a one-line fix for the first alone
would leave the build broken while reading like a success). `bin/generate` now exits 0.
`Session::generate` is a new unconstrained completion sharing `complete()`'s KV-cache
discipline but not its grammar or its brace-balance halt; greedy, hence deterministic.

**The rebuilt generator is proven identical, not plausible.** The lost reconstruction is what
produced the fired kill's responses, so a merely reasonable rebuild would silently change
what K2 was computed over. The original `Qwen3-0.6B-Q4_K_M.gguf` survives and generation is
greedy, so byte equality is testable: regenerating the first 5 items of `encoded_soft92.jsonl`
reproduces `responses_soft92.jsonl` **exactly — 60/60 records** across all three arms and all
ten scramble draws, matching on response text, path and `gen_tokens`. Rerun with
`verify_repro.py repro_soft5.jsonl responses_soft92.jsonl`.

**So the responses CAN now be regenerated from the repository.** (The earlier statement that
they could not was true of `f283522` and is superseded here.) Nothing about the verdict
changes either way — it stands on the judgment artifacts.

**Verified by hand, because `ci-gates.sh` cannot reach this crate:** `cargo test -p ciris-nl`
(6 ok — up from 3, since chat.rs's three tests had never been compiled), `--features native`
builds, `--features web --target wasm32-unknown-unknown` builds, `--features web` tests
(8 ok), h3ere2-eval's own suite (13 ok). `gates.log`. Note `ci-gates.sh` line 51 *does* cover
`ciris-nl --features native`; the coverage gap was only ever h3ere2-eval.

**Build invocation.** The crate carries its own `[workspace]` table, so
`cargo build -p h3ere2-eval` from `sim_engine/` matches **no packages and silently does
nothing** — worse than a failure, because it reads as "nothing to build". Use
`--manifest-path sim_engine/crates/h3ere2-eval/Cargo.toml` or build from inside the crate.
Now stated in the crate header.
