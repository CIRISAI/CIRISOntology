"""M=4 extension: does the contraction-map generator produce anything at n=4, M=4
that is NOT implied by SSA? Ordering: contraction check (rare) first, then LP."""
import itertools, json, time, numpy as np
from quantum_candidates import subsets
from contraction import exists_contraction
from n4_attack import vec, known_inequalities
from scipy.optimize import linprog

terms = subsets(4); parties = list(range(4)) + ['O']
A = known_inequalities()
print(f"known SSA instances: {len(A)}", flush=True)
found, notimp, checked = 0, [], 0
t0 = time.time()
L4 = list(itertools.combinations(terms, 4))
for LHS in L4:
    for N in (1, 2, 3, 4):
        for RHS in itertools.combinations(terms, N):
            if set(LHS) & set(RHS): continue
            checked += 1
            ok, f, msg = exists_contraction(list(LHS), list(RHS), parties)
            if not ok: continue
            found += 1
            c = vec([set(t) for t in LHS], [set(t) for t in RHS])
            r = linprog(c=np.zeros(len(A)), A_eq=A.T, b_eq=c,
                        bounds=[(0, None)]*len(A), method='highs')
            if not r.success:
                notimp.append({'L': [sorted(t) for t in LHS], 'R': [sorted(t) for t in RHS]})
                print(f"  NOT IMPLIED: {[sorted(t) for t in LHS]} >= {[sorted(t) for t in RHS]}", flush=True)
    if checked % 200000 < 2000:
        print(f"  progress: {checked:,} checked, {found} with contraction maps, "
              f"{len(notimp)} not implied, {time.time()-t0:.0f}s", flush=True)
print(f"\nDONE: checked {checked:,}; {found} admit contraction maps; "
      f"{len(notimp)} NOT implied by SSA")
json.dump({'checked': checked, 'with_map': found, 'not_implied': notimp},
          open('n4_M4_results.json', 'w'))
