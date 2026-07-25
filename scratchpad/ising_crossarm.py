"""ising_crossarm.py — kill K5.  Does the Monte Carlo pipeline reproduce the answer we
already know EXACTLY?

Arm B is only reportable if its bias-corrected excess recovers Arm A's exact value on the
lattices Arm A solved by enumeration.  Pre-registered tolerance: agreement within 2
combined standard errors at every grid point, and no systematic sign to the residual.
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import ising_field as IF

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2.0))


_HIST = {}


def exact_at(Lx, Ly, T, h, geom):
    """Exact I_C^(3) at one (T,h) — recomputed directly, not interpolated off a grid.
    The 2^N enumeration is cached per lattice; only the cheap contraction repeats."""
    if (Lx, Ly) not in _HIST:
        try:
            import cupy as cp
            xp = cp if Lx * Ly >= 22 else np
        except Exception:
            xp = np
        _HIST[(Lx, Ly)] = IF.exact_histogram(Lx, Ly, xp, verbose=False)
    counts, nb, N = _HIST[(Lx, Ly)]
    p = IF.exact_grid_fast(counts[geom], nb, N, [T], [h])[0, 0]
    return float(IF.share3(p)[0])


def main():
    rows = json.load(open(os.path.join(HERE, 'ising_mc_crossarm.json')))
    print("=" * 104)
    print("KILL K5 — Monte Carlo vs EXACT, on the lattices where the exact answer is known")
    print("=" * 104)
    print(f"{'lattice':<8}{'T':>8}{'h':>9}{'geom':<9}{'EXACT':>13}{'MC excess':>13}"
          f"{'MC sd':>11}{'resid':>12}{'resid/sd':>10}  verdict")
    print("-" * 104)
    cache, nsig, resids = {}, 0, []
    for r in rows:
        key = (r['Lx'], r['Ly'], r['T'], r['h'], r['geom'])
        if key not in cache:
            cache[key] = exact_at(r['Lx'], r['Ly'], r['T'], r['h'], r['geom'])
        ex = cache[key]
        sd = max(r['boot_sd'], r['floor_sd'])
        resid = r['excess'] - ex
        rs = resid / sd if sd > 0 else float('nan')
        bad = abs(rs) > 2.0
        nsig += bad
        resids.append(rs)
        print(f"{r['Lx']}x{r['Ly']:<5}{r['T']:>8.3f}{r['h']:>9.4f}{r['geom']:<9}"
              f"{ex:>13.6e}{r['excess']:>13.6e}{sd:>11.2e}{resid:>+12.2e}{rs:>+10.2f}"
              f"  {'*** >2sd' if bad else 'ok'}")
    resids = np.array(resids)
    print("-" * 104)
    print(f"grid points: {len(rows)};  beyond 2 sd: {nsig};  "
          f"mean resid/sd = {resids.mean():+.3f} (systematic sign check);  "
          f"max |resid/sd| = {np.abs(resids).max():.2f}")
    ok = (nsig == 0) and abs(resids.mean()) < 1.0
    print(f"\nK5 VERDICT: {'PASS — Arm B reproduces the exact answer, so its larger-L '
                          'readings are reportable' if ok else '*** K5 FIRED — Arm B not reported ***'}")

    ref = os.path.join(HERE, 'ising_mc_refuter.json')
    if os.path.exists(ref):
        print("\n" + "=" * 104)
        print("CROSS-RUN REFUTER — slot j from an independent run; true share is zero by "
              "construction.  |z| > 5 would prove the null mis-specified.")
        print("=" * 104)
        for r in json.load(open(ref)):
            print(f"  L={r['Lx']}x{r['Ly']} T={r['T']:.3f} h={r['h']:.4f}: "
                  f"raw={r['share_raw']:.3e} floor={r['floor_neff']:.3e} "
                  f"excess={r['excess']:+.3e} z={r['z']:+.2f}  -> "
                  f"{'*** NULL MIS-SPECIFIED' if abs(r['z']) > 5 else 'clean'}")


if __name__ == '__main__':
    main()
