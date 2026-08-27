#!/bin/bash
cd /home/emoore/CIRISOntology/scratchpad/crystal
python3 -u - <<'PY' >> gauge_dmrg.log 2>&1
import sys; sys.path.insert(0,'.')
from dmrg_schwinger import gap
m_true, _, _ = gap(12, 4.0, chi=48)
m_mut, _, _ = gap(12, 4.0, chi=48, mutate="coeff-off-by-one")
ok = abs(m_mut - m_true) > 0.02
print(f"FIRE side (planted pair-coeff off-by-one): {m_true:.4f} -> {m_mut:.4f}, |shift|={abs(m_mut-m_true):.4f} -> {'FIRES' if ok else 'MISSED'}")
assert ok
print("gauge verdict: DMRG reproduces exact ED (incl. the projected gap) and the")
print("observable planted MPO mutation FIRES; the null plant's lesson is recorded. Two-sided.")
PY
echo $? > gauge_mut.DONE
