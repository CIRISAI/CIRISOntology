"""PGX-1 scorer. Applies the frozen criteria of POLARITON_GPU_EXT_PREREG.md
mechanically. Written before the arm results are read."""
import json, sys
import numpy as np
from scipy.stats import binomtest

def score_arm1(path='pgx1_arm1.json'):
    rows = json.load(open(path))
    print("=== ARM 1 — the N ladder (E1) ===")
    print(f"{'N':>9} {'sigma':>6} {'A_min_m':>8} {'B_min':>7} {'C_min':>7}")
    for r in rows:
        print(f"{r['N']:>9} {r['sigma']:>6} {str(r.get('A_min_m')):>8} {str(r['B_min']):>7} {str(r['C_min']):>7}")
    print("\nE1 — C_min within +/-20% across the FULL ladder at fixed sigma:")
    for s in sorted({r['sigma'] for r in rows}):
        cs = [(r['N'], r['C_min']) for r in rows if r['sigma'] == s]
        vals = [c for _, c in cs if c is not None]
        if len(vals) < len(cs):
            print(f"  sigma={s}: INCOMPLETE (a cell never reached tolerance) -> E1 FAILS at scale")
            continue
        lo, hi, med = min(vals), max(vals), float(np.median(vals))
        ok = (lo >= 0.8*med) and (hi <= 1.2*med)
        print(f"  sigma={s}: C_min {vals} median {med:.1f} spread [{lo},{hi}] -> {'WITHIN' if ok else 'OUTSIDE'} +/-20% => E1 {'CONFIRMED' if ok else 'FAILS'} at this sigma")
    print("\nE3-at-ladder (Krylov vs C):")
    for r in rows:
        a, c = r.get('A_min_m'), r['C_min']
        if a is not None and c is not None:
            print(f"  N={r['N']:>8} s={r['sigma']}: A={a} C={c} -> {'KRYLOV-CAPTURES' if a <= c else 'C smaller'}")

def score_arm2(path='pgx1_arm2.json'):
    rows = json.load(open(path))
    print("\n=== ARM 2 — the disorder ensemble (E2, decisive) ===")
    cells = sorted({(r['N'], r['sigma']) for r in rows})
    for N, s in cells:
        sub = [r for r in rows if r['N'] == N and r['sigma'] == s]
        # PREREG DEFECT, OWNED: POLARITON_GPU_EXT_PREREG.md did not say how to treat a
        # realization where baseline B never reaches tolerance within its grid (B_min=None).
        # Dropping those pairs biases AGAINST C; counting them as C-wins biases FOR C.
        # Both treatments are reported; the verdict must hold under BOTH to count.
        n_bnone = sum(1 for r in sub if r['B_min'] is None and r['C_min'])
        for treat in ('drop-None', 'None-counts-as-C-win'):
            if treat == 'drop-None':
                pairs = [(r['B_min'], r['C_min']) for r in sub if r['B_min'] and r['C_min']]
                extra_wins = 0
            else:
                pairs = [(r['B_min'], r['C_min']) for r in sub if r['B_min'] and r['C_min']]
                extra_wins = n_bnone
            if len(pairs) + extra_wins < 10:
                print(f"  N={N} sigma={s} [{treat}]: only {len(pairs)+extra_wins} usable -> VOID"); continue
            ratios = np.array([b/c for b, c in pairs]) if pairs else np.array([])
            med = float(np.median(ratios)) if len(ratios) else float('nan')
            wins = int(sum(1 for b, c in pairs if c < b)) + extra_wins
            losses = int(sum(1 for b, c in pairs if c > b))
            n = wins + losses
            p = binomtest(wins, n, 0.5).pvalue if n > 0 else 1.0
            gate = (med >= 2.0) and (p < 0.01)
            print(f"  N={N} sigma={s} [{treat}]: pairs={len(pairs)} B-never-converged={n_bnone} "
                  f"median(B/C)={med:.3f} C-wins {wins}/{n} p={p:.3g} -> E2 {'PASSES' if gate else 'FAILS'}")
        pairs = [(r['B_min'], r['C_min']) for r in sub if r['B_min'] and r['C_min']]
        if not pairs: continue
        print(f"      B_min median {np.median([b for b,_ in pairs]):.1f}  C_min median {np.median([c for _,c in pairs]):.1f}")
        aa = [r.get('A_min_m') for r in sub if r.get('A_min_m')]
        if aa:
            print(f"      A_min_m median {np.median(aa):.1f} -> "
                  f"{'KRYLOV-ALREADY-CAPTURES-REACHABILITY at scale' if np.median(aa) <= np.median([c for _,c in pairs]) else 'C below Krylov'}")

if __name__ == '__main__':
    which = sys.argv[1] if len(sys.argv) > 1 else 'both'
    if which in ('arm1','both'):
        try: score_arm1()
        except FileNotFoundError: print("arm1 results not present yet")
    if which in ('arm2','both'):
        try: score_arm2()
        except FileNotFoundError: print("arm2 results not present yet")
