"""ising_analyze.py — read the Arm A / Arm B outputs and print the pre-registered readout.

Prints, in the order the prereg demands it: the h=0 control column FIRST, then peaks per
geometry per lattice, then where the ORDINARY measures peak on the same distributions,
then the finite-size behaviour that separates outcome (b1) from (b2).
"""
import sys, os, json
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
LN2 = float(np.log(2.0))
TC = 2.269185314213022
HERE = os.path.dirname(os.path.abspath(__file__))


def peak_of(A, Ts, hs, skip_h0=True):
    A = np.asarray(A, dtype=float)
    B = A.copy()
    if skip_h0:
        B[:, 0] = -np.inf
    i = int(np.nanargmax(B))
    a, b = divmod(i, len(hs))
    return float(A[a, b]), float(Ts[a]), float(hs[b]), a, b


def main():
    ex = json.load(open(os.path.join(HERE, 'ising_exact.json')))
    Ts, hs = np.array(ex['T']), np.array(ex['h'])
    print("=" * 92)
    print("ARM A — EXACT ENUMERATION.  No sampling, no estimator, no bias.")
    print(f"  grid: {len(Ts)} temperatures x {len(hs)} fields (h=0 exact), T_c = {TC:.6f}")
    print("=" * 92)

    # -------- the control column, first, per the prereg --------
    print("\n(a) THE CONTROL COLUMN — h = 0 exactly.  The sign-symmetry lemma says this")
    print("    must be zero at EVERY temperature.  Anything else voids the run.\n")
    worst = 0.0
    for key, L in ex['lattices'].items():
        for g, d in L['geoms'].items():
            v = float(np.abs(np.array(d['ic3'])[:, 0]).max())
            worst = max(worst, v)
        print(f"    {key:<5} max|I_C^(3)| over all T at h=0, all geometries: "
              f"{max(float(np.abs(np.array(d['ic3'])[:,0]).max()) for d in L['geoms'].values()):.3e}")
    print(f"\n    WORST OVER EVERYTHING: {worst:.3e}   -> "
          f"{'PASS, outcome (a) confirmed' if worst < 1e-12 else '*** K1 FIRED, RUN VOID ***'}")

    # -------- the map --------
    print("\n\n(b) THE MAP — peak of the pairwise-blind I_C^(3) over h != 0\n")
    hdr = (f"    {'lattice':<7}{'geom':<9}{'peak I_C3 (nats)':>18}{'CF vs ln2':>11}"
           f"{'T':>8}{'T/Tc':>8}{'h':>9}{'|m|':>8}")
    print(hdr); print("    " + "-" * (len(hdr) - 4))
    peaks = {}
    for key, L in ex['lattices'].items():
        mabs = np.array(L['m_abs'])
        for g, d in L['geoms'].items():
            A = np.array(d['ic3'])
            v, T, h, a, b = peak_of(A, Ts, hs)
            peaks[(key, g)] = (v, T, h, abs(float(mabs[a, b])))
            print(f"    {key:<7}{g:<9}{v:>18.6e}{v/LN2*100:>10.4f}%{T:>8.3f}"
                  f"{T/TC:>8.3f}{h:>9.4f}{abs(float(mabs[a,b])):>8.3f}")

    # -------- geometry ordering: prereg kill K4 --------
    print("\n\n(K4) MECHANISM — I predicted `star` (three spins sharing one neighbour)")
    print("     would carry the largest peak, because integrating out that shared")
    print("     neighbour is what generates an effective three-body coupling.\n")
    for key, L in ex['lattices'].items():
        order = sorted(((peaks[(key, g)][0], g) for g in L['geoms']), reverse=True)
        s = "  >  ".join(f"{g} ({v:.2e})" for v, g in order)
        win = order[0][1]
        print(f"    {key:<6} {s}")
        print(f"           winner = {win}  ->  "
              f"{'prediction HOLDS' if win == 'star' else 'K4 FIRED: prediction wrong'}")

    # -------- the ordinary measures on the SAME distributions --------
    print("\n\n(c) THE ORDINARY MEASURES, on exactly the same distributions.")
    print("    This is the survey's thesis tested inside one canonical model.\n")
    hdr2 = (f"    {'lattice':<7}{'geom':<9}{'quantity':<10}{'peak':>12}{'T':>8}{'T/Tc':>8}"
            f"{'h':>9}   I_C^(3) THERE")
    print(hdr2); print("    " + "-" * (len(hdr2) - 4))
    for key, L in ex['lattices'].items():
        for g, d in L['geoms'].items():
            A3 = np.array(d['ic3'])
            for qn in ('tc', 'omega'):
                Q = np.array(d[qn])
                v, T, h, a, b = peak_of(Q, Ts, hs, skip_h0=False)
                print(f"    {key:<7}{g:<9}{qn:<10}{v:>12.6f}{T:>8.3f}{T/TC:>8.3f}"
                      f"{h:>9.4f}   {A3[a,b]:.3e}")
        break   # one lattice is enough to make the point; full table is in the json

    # -------- finite size, exact arm --------
    print("\n\n(d) FINITE SIZE within the exact arm (peak height by lattice):\n")
    for g in ex['lattices']['4x4']['geoms']:
        row = []
        for key in ex['lattices']:
            if g in ex['lattices'][key]['geoms']:
                row.append(f"{key}={peaks[(key,g)][0]:.4e}")
        print(f"    {g:<9} " + "   ".join(row))

    # -------- Arm B --------
    for fn, title in (('ising_mc_crossarm.json', 'ARM B CROSS-ARM (kill K5)'),
                      ('ising_mc_refuter.json', 'ARM B REFUTER (cross-run, true zero)'),
                      ('ising_mc_fss.json', 'ARM B FINITE SIZE (b1 vs b2)')):
        p = os.path.join(HERE, fn)
        if not os.path.exists(p):
            continue
        rows = json.load(open(p))
        print(f"\n\n{'='*92}\n{title}\n{'='*92}")
        for r in rows:
            print(f"  L={r['Lx']}x{r['Ly']} T={r['T']:.3f} h={r['h']:.4f} "
                  f"{r['geom']:<10} raw={r['share_raw']:.3e} floor={r['floor_neff']:.3e} "
                  f"excess={r['excess']:+.3e} z={r['z']:+8.2f} N_eff={r['N_eff']:.2e} "
                  f"F={r['F_max']:.1f} {'' if r['trustworthy'] else 'UNTRUSTWORTHY'}")


if __name__ == '__main__':
    main()
