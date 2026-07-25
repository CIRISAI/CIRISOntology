"""Focused convergence study: where does the bias-subtracted binned share converge to,
and does it agree with the continuum bridge?  Exact, no sampling."""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np, sky_pilot as sp

zg, wg, _ = sp.gauss_nodes()
out = {}
for a in [(0.5, 0.5, 0.5), (0.8, 0.6, 0.4)]:
    for gam in [0.2, 0.05]:
        z, w, ge = sp.std_gamma_nodes(gam)
        C, zeta = sp.latent_C_zeta(a, ge)
        B = sp.route_B(C, zeta)[0]
        cd = {ai: sp.latent_marginal_cdf(ai, z, w) for ai in set(a)}
        print(f"\na={a} gamma={gam}  Route B (continuum) = {B:.6e}")
        print(f"  {'b':>5} {'A(b)':>13} {'G(b)':>13} {'A-G':>13} {'(A-G)/B':>9}")
        rows = []
        for b in [4, 8, 16, 32, 64, 96, 128, 160]:
            ec = {ai: sp.quantile_edges_of(cd[ai], b) for ai in cd}
            A = sp.share_b(sp.latent_cells(a, [ec[x] for x in a], z, w))['share_KL']
            G = sp.share_b(sp.latent_cells(a, [sp.quantile_edges_gauss(b)]*3, zg, wg))['share_KL']
            rows.append(dict(b=b, A=A, G=G, sub=A-G))
            print(f"  {b:5d} {A:13.6e} {G:13.6e} {A-G:13.6e} {(A-G)/B:9.4f}")
        # Richardson on the last three subtracted points
        xs = np.array([r['b'] for r in rows[-3:]], float)
        ys = np.array([r['sub'] for r in rows[-3:]])
        al = np.log(abs((ys[1]-ys[0])/(ys[2]-ys[1])))/np.log(xs[1]/xs[0])
        Ainf = ys[2] + (ys[2]-ys[1])/((xs[2]/xs[1])**al - 1.0)
        A2 = sp.share_b(sp.latent_cells(a, [sp.quantile_edges_of(cd[x],2) for x in a], z, w))['share_KL']
        print(f"  extrapolated A_inf = {Ainf:.6e}  (alpha={al:.2f})   B/A_inf = {B/Ainf:.4f}"
              f"   A(b=2)/A_inf = {A2/Ainf:.4f}")
        out[f"{a}_{gam}"] = dict(rows=rows, B=B, A_inf=float(Ainf), alpha=float(al),
                                 A_b2=A2, B_over_Ainf=float(B/Ainf))
json.dump(out, open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                 'sky_bconv.json'), 'w'), indent=1, default=float)
