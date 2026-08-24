#!/bin/bash
# Gate for CALIBRATION 3 (length preference) — AMENDMENT_J2_LENGTH_GATE.md.
#
# A gate that exists only in an amendment is a phantom warrant. This script pins the gate
# against the five judge readings ALREADY COLLECTED, in BOTH directions, plus the interlock
# that makes it unskippable. It runs entirely off stored jsonl: no inference, no network.
#
#   MUST ADMIT   gemma3:12b (primary), padded 0.505, p = 1. The amendment pre-committed that
#                this gate CAN reject the primary; that it does not is the reading, not the
#                design. This is the pin that stops the gate being quietly retuned to a bar
#                the primary would fail.
#   MUST REJECT  llama3.1:8b (second judge), padded 0.783, p = 4.6e-08. The judge that walked
#                through both existing gates and was still length-dominated.
#   MUST ADMIT   mistral-nemo:12b, padded 0.272. THE DIRECTION PIN. The amendment says
#                "a judge that prefers the intact one is penalising padding, which is
#                desirable and passes". An implementation that fails on |deviation| instead
#                of on the padded direction rejects this judge -- the first cut of the gate
#                did exactly that -- and fails here.
#   MUST REJECT  phi4:14b, padded 0.696.
#   MUST ADMIT   qwen3:14b, padded 0.478.
#
# Every one of those five numbers was measured BEFORE this gate script existed, in
# calib_length.log, and none was chosen to make the gate pass. The two that matter -- the
# primary admitted, the second judge rejected -- were forward-predicted in the amendment
# from the real-pair length marginals (0.466 p=0.210 vs 0.595 p=0.0003), written down before
# the instrument existed, and the instrument then agreed on both.
set -u
H="$(cd "$(dirname "$0")" && pwd)"
P=${PY:-/tmp/rtenv/bin/python}
fail=0
ok()  { echo "  PASS  $1"; }
no()  { echo "  FAIL  $1"; fail=1; }

echo "== calibration 3 (length preference) gate =="

verdict() {   # verdict <model> -> PASS|FAIL|NONE
  $P - "$1" <<'EOF' 2>/dev/null
import sys, os
sys.path.insert(0, os.environ["H"])
import calib3
v = calib3.verdict_for(sys.argv[1], os.environ["H"])
print("NONE" if v is None else v["verdict"])
EOF
}
export H

# 1-5. the five collected readings, both directions pinned
check() {   # check <model> <expected> <why>
  got=$(verdict "$1")
  if [ "$got" = "$2" ]; then ok "$1 -> $2   ($3)"; else no "$1 -> got '$got', expected '$2'   ($3)"; fi
}
check gemma3:12b       PASS "primary ADMITTED; the gate was pre-committed to be able to reject it"
check llama3.1:8b      FAIL "second judge REJECTED; length-dominated, 0.783"
check mistral-nemo:12b PASS "DIRECTION PIN: penalising padding (0.272) passes, per the amendment"
check phi4:14b         FAIL "0.696"
check qwen3:14b        PASS "0.478"

# 6. the padding text is the one the collected artifacts were produced with, BYTE FOR BYTE.
#    Pinned by hash, not by length: the first cut of this check tested len(PAD)==128 and a
#    mutation that changed a letter without changing the length walked straight through it.
if $P -c "import sys,os,hashlib; sys.path.insert(0,os.environ['H']); import calib3; \
          sys.exit(0 if hashlib.sha256(calib3.PAD.encode()).hexdigest() == \
          '921d00ca575214a78e965b3a81c72d8d9676c1279c419468f56ea6bcf3e78468' \
          and len(calib3.PAD)==128 and calib3.SEED==20260822 else 1)"; then
  ok "PAD hashes to the collected 128-char sentence and SEED is 20260822 (artifacts reproducible)"
else
  no "PAD or SEED changed — the five pinned readings are no longer reproducible from this code"
fi

# 7. THE INTERLOCK IS REACHED: judge.py refuses real pairs for an uncalibrated model, and
#    refuses BEFORE any inference (it never opens the responses file, which does not exist).
out=$($P "$H/judge.py" pairs no-such-model:0b /nonexistent-responses.jsonl /dev/null 2>&1); rc=$?
if [ $rc -ne 0 ] && echo "$out" | grep -q "CALIBRATION 3 NOT RUN"; then
  ok "judge.py pairs FAILS CLOSED for an uncalibrated model (before touching any input)"
else
  no "judge.py pairs did not refuse an uncalibrated model — the gate is skippable (rc=$rc)"
fi

# 8. the interlock rejects a judge that FAILED the gate
out=$($P -c "import sys,os; sys.path.insert(0,os.environ['H']); import judge; \
             judge.require_calib3('llama3.1:8b')" 2>&1); rc=$?
if [ $rc -ne 0 ] && echo "$out" | grep -q "CALIBRATION 3 FAILED"; then
  ok "interlock rejects llama3.1:8b (a failing judge cannot be admitted to real pairs)"
else
  no "interlock admitted llama3.1:8b despite its FAIL (rc=$rc)"
fi

# 9. and is INERT on a judge that passed — proven by calling it directly rather than by a
#    re-run of the sealed verdict, which would mean re-judging 736 closed pairs.
out=$($P -c "import sys,os; sys.path.insert(0,os.environ['H']); import judge; \
             judge.require_calib3('gemma3:12b')" 2>&1); rc=$?
if [ $rc -eq 0 ] && echo "$out" | grep -q "LENGTH PREFERENCE"; then
  ok "interlock is inert for gemma3:12b (returns, reports, writes nothing)"
else
  no "interlock blocked or errored on the admitted primary (rc=$rc): $out"
fi

# 10. MUTATION TEST: the scorer must move when the data moves, in both directions.
tmp=$(mktemp -d)
$P - <<'EOF' "$tmp"
import json, os, sys
H = os.environ["H"]; tmp = sys.argv[1]
rows = [json.loads(l) for l in open(os.path.join(H, "judge_soft92_gemma3_calib_length.jsonl"))]
for name, val in (("all_padded.jsonl", True), ("all_intact.jsonl", False)):
    with open(os.path.join(tmp, name), "w") as f:
        for r in rows:
            r = dict(r); r["chose_padded"] = val if r["pick"] in ("1", "2") else None
            f.write(json.dumps(r) + "\n")
EOF
mut() { $P - "$1" <<'EOF'
import json, sys, os
sys.path.insert(0, os.environ["H"]); import calib3
print(calib3.score([json.loads(l) for l in open(sys.argv[1])])["verdict"])
EOF
}
[ "$(mut "$tmp/all_padded.jsonl")" = FAIL ] \
  && ok "mutation: a judge that always picks the padded response is REJECTED" \
  || no "mutation: an always-padded judge was ADMITTED — the gate does not bite"
[ "$(mut "$tmp/all_intact.jsonl")" = PASS ] \
  && ok "mutation: a judge that always picks the intact response is ADMITTED (direction holds)" \
  || no "mutation: an always-intact judge was REJECTED — the gate is symmetric, not directional"
rm -rf "$tmp"

echo
[ $fail -eq 0 ] && echo "calibration-3 gate: ALL PASS" || echo "calibration-3 gate: FAILURES ABOVE"
exit $fail
