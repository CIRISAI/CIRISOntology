"""rent_scaling_q1.py — QUESTION 1: is the restorability boundary exactly algebraic?

Pre-registered in RENT_SCALING_PREREG.md (commit 45b6877) §2. Instrument and gates in
rent_scaling_aut.py.

Roster (prereg §2.5, fixed before any result): every wired Hadamard order
N in {8, 12, 16, 20, 24, 28, 32} and EVERY truncation width k = 3 .. N-1 of each, plus the
linear substrates of the rent_islands roster as the transitivity control.

For each structure:
  * exact |Aut(S)| = |P| * |C| by stabiliser chain (never by enumeration)
  * the orbit partition of the support, and whether the action is transitive
  * the G7 decode-weight profile deviation, exactly, wherever 2^k is affordable
  * the level-set partition induced by R_i(.), for H-ORBIT

LINEARITY SHORTCUT, and it is a theorem not a measurement: if S is a coset of a linear code
then translation by any codeword is an automorphism, so |C| = |S| and the action is transitive.
Applied only to skip the O(|S|^2) orbit search on the big code arms; verified against the full
search on the six small linear substrates in gate Q1-G1/G2.
"""
import sys, os, json, time, argparse
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands_design_check as DC
import rent_scaling_aut as AU

HERE = os.path.dirname(os.path.abspath(__file__))
ORDERS = [8, 12, 16, 20, 24, 28, 32]
KMAX_R = 27                       # the 2^k affordability cut, DECLARED (prereg §2.5)


def is_linear(S):
    """Is the support a coset of a linear code? (translate so 0 in S, then closed under XOR)"""
    S = np.unique(np.asarray(S, dtype=np.int64), axis=0)
    n = len(S)
    if n & (n - 1):
        return False
    S0 = S ^ S[0][None, :]
    codes = set(int(''.join(map(str, r)), 2) for r in S0)
    for a in codes:
        for b in codes:
            if (a ^ b) not in codes:
                return False
    return True


def pair_dev(S):
    """max |pair marginal - 1/4| on the support, by direct counting. Strength-2 check."""
    S = np.unique(np.asarray(S, dtype=np.int64), axis=0)
    n, k = S.shape
    worst = 0.0
    for i in range(k):
        for j in range(i + 1, k):
            c = np.bincount(S[:, i] * 2 + S[:, j], minlength=4)
            worst = max(worst, float(np.abs(c / n - 0.25).max()))
    return worst


def analyse(S, label, want_R=True):
    S = np.unique(np.asarray(S, dtype=np.int64), axis=0)
    n, k = S.shape
    lin = is_linear(S)
    t0 = time.time()
    if lin:
        pord, ok, _ = AU.perm_stab_order_safe(S)
        d = dict(ns=n, k=k, perm_order=pord, n_translations=n, aut_order=pord * n,
                 orbit_sizes=[n], n_orbits=1, transitive=True,
                 orbit_id=[0] * n, exact=ok, zero_orbit_size=n, orbit_route='linear-theorem')
    else:
        d = AU.aut_data(S)
        d['orbit_route'] = 'search'
    d['aut_secs'] = round(time.time() - t0, 2)
    d['label'] = label
    d['linear'] = lin
    d['pair_dev'] = pair_dev(S)
    d['share_max'] = float(k * np.log(2) - np.log(n))
    t0 = time.time()
    if want_R and k <= KMAX_R:
        R, dev = AU.profile_R(S)
        lab, nlev = AU.profile_levels(R)
        d['profile_dev'] = dev
        d['n_levels'] = nlev
        d['level_id'] = lab
        d['level_sizes'] = sorted((lab.count(t) for t in range(nlev)), reverse=True)
        d['equivariant'] = bool(dev < 1e-12)
        # H-ORBIT: orbits always refine levels (theorem). Equal iff no accidental degeneracy.
        d['levels_eq_orbits'] = bool(nlev == d['n_orbits'] and
                                     _same_partition(lab, d['orbit_id']))
        d['orbits_refine_levels'] = bool(_refines(d['orbit_id'], lab))
    else:
        d['profile_dev'] = None
        d['equivariant'] = None
        d['n_levels'] = None
        d['level_sizes'] = None
        d['levels_eq_orbits'] = None
        d['orbits_refine_levels'] = None
    d['R_secs'] = round(time.time() - t0, 2)
    return d


def _same_partition(a, b):
    ma, mb = {}, {}
    for x, y in zip(a, b):
        if ma.setdefault(x, y) != y or mb.setdefault(y, x) != x:
            return False
    return True


def _refines(fine, coarse):
    """every block of `fine` lies inside one block of `coarse`"""
    m = {}
    for f, c in zip(fine, coarse):
        if m.setdefault(f, c) != c:
            return False
    return True


def run(out_path, kmax_r=KMAX_R):
    AU_KMAX = kmax_r
    rows = []
    t_all = time.time()
    for N in ORDERS:
        H = DC.hadamard(N).copy()
        H = H * np.where(H[:, [0]] == -1, -1, 1)
        B = ((1 - H[:, 1:]) // 2).astype(np.int64)
        for k in range(3, N):
            S = B[:, :k]
            uniq = np.unique(S, axis=0)
            lab = f'H{N}/k{k}'
            # R costs a full 2^k pass. Spend it where the question lives: every NON-LINEAR
            # structure up to the declared cut, and linear ones only up to k=20, where they
            # serve as the (T)-check and nothing more. Rule fixed here, before any verdict.
            lin_here = is_linear(S)
            d = analyse(S, lab, want_R=(k <= AU_KMAX and (not lin_here or k <= 20)))
            d['order_N'] = N
            d['rows_distinct'] = bool(len(uniq) == N)
            d['source'] = DC.had_source(N)
            d['is_armA'] = bool(DC.N0(k) == N and k >= 5)
            rows.append(d)
            print(f"  {lab:10s} |S|={d['ns']:3d} distinct={str(d['rows_distinct']):5s} "
                  f"lin={str(d['linear']):5s} |Aut|={d['aut_order']:12d} "
                  f"orbits={str(d['orbit_sizes'])[:26]:26s} trans={str(d['transitive']):5s} "
                  f"pdev={('%.2e' % d['profile_dev']) if d['profile_dev'] is not None else 'skip':>9s} "
                  f"lev={str(d['n_levels']):>4s} [{d['aut_secs']:.1f}+{d['R_secs']:.1f}s]",
                  flush=True)
        json.dump(dict(rows=rows, kmax_R=AU_KMAX, node_budget=AU.NODE_BUDGET),
                  open(out_path, 'w'), indent=1)
    print(f"\ntotal {time.time()-t_all:.0f}s -> {out_path}")
    return rows


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(HERE, 'rent_scaling_q1.json'))
    ap.add_argument('--kmax-r', type=int, default=KMAX_R)
    a = ap.parse_args()
    run(a.out, a.kmax_r)
