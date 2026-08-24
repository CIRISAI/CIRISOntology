#!/bin/bash
# Gate for JUDGE_PROTOCOL section 5's length guard.
#
# A guard that can only ever pass is not a control. This gate pins BOTH directions against
# real, already-collected data, so a future edit that silently disables the check — or one
# that makes it fire on everything — fails here.
#
#   MUST FIRE     gemma3:12b, GOLD, C vs B.  The primary's own side-by-side comparison is
#                 length-confounded (length p = 0.0396, arm p = 0.098). This is the positive
#                 control, and it is deliberately taken from the PRIMARY judge so the gate
#                 cannot be read as only ever accusing the second judge.
#   MUST NOT FIRE gemma3:12b, SOFT, C vs A.  The primary's secondary finding is length-clean
#                 and the arm term survives at beta = -0.907, p = 0.00045. This is the
#                 negative control: if the guard fires here, it is over-firing and the
#                 K2 secondary would be wrongly voided.
#
# Both expectations were measured BEFORE this gate existed and are recorded in
# RESULTS_K2_SECOND_JUDGE.md. Neither was chosen to make the gate pass.
set -u
H="$(cd "$(dirname "$0")" && pwd)"
P=${PY:-/tmp/rtenv/bin/python}
fail=0
ok()  { echo "  PASS  $1"; }
no()  { echo "  FAIL  $1"; fail=1; }

echo "== section-5 length guard gate =="

# 1. positive control: the guard must FIRE on the primary's gold C-vs-B
out=$($P "$H/length_guard.py" "$H/judge_gold92_pairs.jsonl" 2>&1)
if echo "$out" | awk '/--- C vs B:/{f=1} f&&/PROTOCOL SECTION 5 FIRES/{print;exit}' | grep -q FIRES; then
  ok "MUST-FIRE control fires (gemma3 gold C-vs-B is length-confounded)"
else
  no "MUST-FIRE control did NOT fire — the guard has been disabled or weakened"
fi

# 2. negative control: the guard must NOT fire on the primary's soft C-vs-A
out=$($P "$H/length_guard.py" "$H/judge_soft92_pairs.jsonl" 2>&1)
if echo "$out" | awk '/--- C vs A:/{f=1} f&&/PROTOCOL SECTION 5 FIRES/{print;exit}' | grep -q FIRES; then
  no "MUST-NOT-FIRE control fired — the guard is over-firing; K2's secondary would be wrongly voided"
else
  ok "MUST-NOT-FIRE control stays silent (gemma3 soft C-vs-A is length-clean)"
fi

# 3. the arm coefficient must keep its SIGN and significance on the primary's soft C-vs-A.
#    This is the number the product-direction restatement rests on.
if $P "$H/length_guard.py" "$H/judge_soft92_pairs.jsonl" 2>&1 \
   | awk '/--- C vs A:/{f=1} f&&/arm\(C in slot 1\)/{print;exit}' \
   | grep -qE 'beta= *-0\.9[0-9]+.*p=0\.000'; then
  ok "arm term on gemma3 soft C-vs-A still negative and significant (beta ~ -0.907)"
else
  no "arm term on gemma3 soft C-vs-A changed — the restatement's basis moved"
fi

# 4. the guard must actually be REACHED by analyze.py, not merely present on disk
if $P "$H/analyze.py" "$H/judge_soft92_pairs.jsonl" 2>&1 | grep -q "SECTION 5 LENGTH GUARD"; then
  ok "analyze.py runs the guard by default"
else
  no "analyze.py did NOT run the guard — a pre-registered check that must be remembered is not a control"
fi

echo
[ $fail -eq 0 ] && echo "section-5 gate: ALL PASS" || echo "section-5 gate: FAILURES ABOVE"
exit $fail
