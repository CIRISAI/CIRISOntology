"""ising_fss.py — outcome (b1) vs (b2): does the order-3 peak grow with lattice size,
and does its locus approach T_c?

(b1) peak locus -> (T_c, 0) as h -> 0 AND peak height grows with L  =>  critical phenomenon
(b2) peak at h = O(1), locus does NOT approach T_c, height L-independent once L >> 1
     =>  local short-range effect with no critical enhancement

Untrustworthy grid points (prereg section 6: min_cell*N_eff < 20, N_eff < 1e3) are
excluded from every peak claim and counted separately.
"""
import sys, os, json
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2.0))
TC = 2.269185314213022


def main():
    rows = json.load(open(os.path.join(HERE, 'ising_mc_fss.json')))
    Ls = sorted({r['Lx'] for r in rows})
    geoms = sorted({r['geom'] for r in rows})

    print("=" * 100)
    print("ARM B — FINITE SIZE.  Is the order-3 peak a critical phenomenon (b1) or a "
          "local one (b2)?")
    print("=" * 100)

    # ---- the h = 0 control, at every lattice size ----
    print("\n(a) THE CONTROL, at size: h = 0 must still read zero.\n")
    h0 = [r for r in rows if r['h'] == 0.0]
    for L in Ls:
        sel = [r for r in h0 if r['Lx'] == L]
        if not sel:
            continue
        mz = max(abs(r['z']) for r in sel)
        mx = max(abs(r['excess']) for r in sel)
        print(f"    L={L:<3} max|z| = {mz:5.2f}   max|excess| = {mx:.2e}   "
              f"{'consistent with zero' if mz < 5 else '*** K1 FIRED AT SIZE ***'}")

    # ---- peak height vs L, per geometry ----
    print("\n\n(b) PEAK EXCESS vs LATTICE SIZE (trustworthy points only)\n")
    print(f"    {'geom':<9}" + "".join(f"{'L='+str(L):>26}" for L in Ls))
    print("    " + "-" * (9 + 26 * len(Ls)))
    table = {}
    for g in geoms:
        cells = []
        for L in Ls:
            sel = [r for r in rows if r['geom'] == g and r['Lx'] == L
                   and r['trustworthy'] and r['h'] > 0]
            if not sel:
                cells.append(f"{'--':>26}"); continue
            b = max(sel, key=lambda r: r['excess'])
            table[(g, L)] = b
            cells.append(f"{b['excess']:>12.3e} @T={b['T']:.2f},h={b['h']:.3f}"[:26].rjust(26))
        print(f"    {g:<9}" + "".join(cells))

    # ---- the verdict ----
    print("\n\n(c) THE (b1)/(b2) ADJUDICATION, per geometry\n")
    print(f"    {'geom':<9}{'trend in peak height':<34}{'peak T/Tc by L':<34}verdict")
    print("    " + "-" * 96)
    for g in geoms:
        hs = [(L, table[(g, L)]['excess']) for L in Ls if (g, L) in table]
        if len(hs) < 2:
            print(f"    {g:<9}{'insufficient trustworthy points':<34}")
            continue
        vals = [v for _, v in hs]
        trend = "GROWS with L" if vals[-1] > vals[0] * 1.5 else (
                "DECAYS with L" if vals[-1] < vals[0] / 1.5 else "flat in L")
        tstr = " ".join(f"{table[(g,L)]['T']/TC:.2f}" for L, _ in hs)
        ratio = vals[-1] / vals[0] if vals[0] > 0 else float('nan')
        verdict = ("(b1)-like: critical enhancement" if trend == "GROWS with L"
                   else "(b2)-like: local, no critical enhancement")
        print(f"    {g:<9}{trend + f'  (x{ratio:.2f} from L={hs[0][0]} to L={hs[-1][0]})':<34}"
              f"{tstr:<34}{verdict}")

    # ---- honesty ledger ----
    print("\n\n(d) HONESTY LEDGER\n")
    tot = len(rows)
    unt = sum(1 for r in rows if not r['trustworthy'])
    print(f"    grid points: {tot};  excluded as untrustworthy: {unt} "
          f"({100*unt/tot:.0f}%)")
    print(f"    tied fraction: 0 at every point — Ising spins are natively binary, so")
    print(f"      there is no analogue quantity being thresholded.  The static-nonlinearity")
    print(f"      artifact channel is STRUCTURALLY ABSENT, not merely checked and found clean.")
    tr = [r for r in rows if r['trustworthy']]
    if tr:
        print(f"    N_eff over trustworthy points: min {min(r['N_eff'] for r in tr):.2e}, "
              f"median {np.median([r['N_eff'] for r in tr]):.2e}, "
              f"max {max(r['N_eff'] for r in tr):.2e}")
        print(f"    variance-inflation F: median {np.median([r['F_max'] for r in tr]):.1f}, "
              f"max {max(r['F_max'] for r in tr):.1f}  "
              f"(nominal N would have understated the floor by this factor)")
        print(f"    tau_int (in units of the {tr[0]['sweeps_total']}-sweep run's gap): "
              f"median {np.median([r['tau_int'] for r in tr]):.2f}, "
              f"max {max(r['tau_int'] for r in tr):.2f}")
    print(f"    ceiling fraction of the largest trustworthy excess: "
          f"{max((r['excess'] for r in tr), default=0)/LN2*100:.4f}% of ln 2")


if __name__ == '__main__':
    main()
