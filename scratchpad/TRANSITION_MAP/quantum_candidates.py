"""Sweep contraction maps with M >= N -> candidates for QUANTUM entropy inequalities.
Basis: arXiv:2409.17317 Cor 4.1 (a quantum inequality with M LHS terms needs N <= M),
and the authors' statement that generating quantum inequalities this way is future work.

n=3 is a CONTROL: the 3-party quantum entropy cone is fully characterised by SSA and
weak monotonicity (Pippenger), so nothing genuinely new may survive there. Anything
that does survive is a bug or a known inequality in disguise."""
import itertools, sys
from contraction import exists_contraction, occ, hd

def subsets(n):
    P = list(range(n))
    out = []
    for k in range(1, n + 1):
        for c in itertools.combinations(P, k):
            out.append(frozenset(c))
    return out

def entropy_vec_terms(terms, S):
    return sum(S[t] for t in terms)

def sweep(n, maxM=3, verbose=True):
    terms = subsets(n)
    parties = list(range(n)) + ['O']
    found = []
    for M in range(1, maxM + 1):
        for N in range(1, M + 1):                      # Cor 4.1: N <= M
            for LHS in itertools.combinations(terms, M):
                for RHS in itertools.combinations(terms, N):
                    if set(LHS) & set(RHS):            # skip trivially cancelling
                        continue
                    ok, f, msg = exists_contraction(list(LHS), list(RHS), parties)
                    if ok:
                        found.append((M, N, LHS, RHS))
    return found

def fmt(t):
    return ''.join('ABCD'[i] for i in sorted(t))

if __name__ == '__main__':
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 3
    maxM = int(sys.argv[2]) if len(sys.argv) > 2 else 3
    res = sweep(n, maxM)
    print(f"n={n}, M<={maxM}: {len(res)} candidate (M>=N) inequalities admit contraction maps\n")
    by = {}
    for M, N, L, R in res:
        by.setdefault((M, N), []).append((L, R))
    for k in sorted(by):
        print(f"  M={k[0]} N={k[1]}: {len(by[k])} candidates")
    print("\nsample (up to 12):")
    for M, N, L, R in res[:12]:
        print(f"   {' + '.join('S('+fmt(t)+')' for t in L)}  >=  {' + '.join('S('+fmt(t)+')' for t in R)}")
