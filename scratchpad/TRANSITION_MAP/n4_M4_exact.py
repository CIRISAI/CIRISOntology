"""Exact stage after the GPU boundary filter: run the real contraction CSP on the
survivors, then LP-test whether any is NOT implied by SSA."""
import json, time, numpy as np
from quantum_candidates import subsets
from contraction import exists_contraction
from n4_attack import vec, known_inequalities
from scipy.optimize import linprog

terms = subsets(4); parties = list(range(4)) + ['O']
surv = json.load(open('n4_M4_survivors.json'))
A = known_inequalities()
print(f"{len(surv):,} survivors from the GPU filter; {len(A)} SSA instances")
with_map, not_implied = 0, []
t0 = time.time()
for k, (li, ri) in enumerate(surv):
    LHS = [terms[i] for i in li]; RHS = [terms[i] for i in ri]
    ok, f, msg = exists_contraction(LHS, RHS, parties)
    if not ok: continue
    with_map += 1
    c = vec([set(t) for t in LHS], [set(t) for t in RHS])
    r = linprog(c=np.zeros(len(A)), A_eq=A.T, b_eq=c,
                bounds=[(0, None)]*len(A), method='highs')
    if not r.success:
        not_implied.append({'L': [sorted(t) for t in LHS], 'R': [sorted(t) for t in RHS]})
        print("  NOT IMPLIED:", [sorted(t) for t in LHS], ">=", [sorted(t) for t in RHS], flush=True)
    if k % 8000 == 0 and k:
        print(f"   {k:,}/{len(surv):,}  maps={with_map}  notimplied={len(not_implied)}  {time.time()-t0:.0f}s", flush=True)
print(f"\nM=4 RESULT: {with_map:,} admit contraction maps; {len(not_implied)} NOT implied by SSA")
json.dump({'survivors': len(surv), 'with_map': with_map, 'not_implied': not_implied},
          open('n4_M4_results.json','w'))
