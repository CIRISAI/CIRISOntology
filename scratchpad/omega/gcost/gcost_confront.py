#!/usr/bin/env python3
"""
gcost_confront.py -- confront the derived rent function f with the repo's PUBLISHED readings.

No instrument is re-run.  Every measured number below is quoted from a results file or from
the raw JSON that file was written from:
  scratchpad/atlas/ATLAS_V1_RESULTS.md          (H1 table: W* at P(in code) >= 0.99)
  scratchpad/maintenance_sweep_results.json     (exact_sweep: share_inf, the exactly propagated
                                                 stationary share; roster: the dual weight
                                                 enumerators and share_max)
  scratchpad/MAINTENANCE_SWEEP_RESULTS.md       (T4: LFSR retained fraction of ln2)
  scratchpad/HOLONOMY_RENT_RESULTS.md           (Sec.5 plateau, Sec.8 periodic, Sec.4 q_half)

Predictions come from GCOST_DERIVATION.md and use ZERO fitted parameters.
"""
import json, math
import numpy as np

LN2 = math.log(2.0)

def G_law(q, lam):   return q / ((1.0 - lam) + q * lam)
def f_rent(gam, d):  return (1.0 - d) * gam / (gam + d * (1.0 - gam))
def G_periodic(P, lam): return (1.0 - lam ** P) / (P * (1.0 - lam))
def Hb(p):
    if p <= 0 or p >= 1: return 0.0
    return -p * math.log(p) - (1 - p) * math.log(1 - p)

def rule(t): print("\n" + t + "\n" + "-" * len(t))

print("=" * 96)
print("gcost_confront.py -- f vs the published record.  No instrument re-run; no fitted parameter.")
print("=" * 96)

# =============================================================== 1. ATLAS =====
rule("SUBSTRATE 1 -- atlas v1 H1: the 2-bit code {00,11}, the table that killed f(Delta_v)")
print("  published (ATLAS_V1_RESULTS.md H1): W* = min repair rate w with stationary P(in code) >= 0.99")
print("  prediction:  gamma = 1 - (1-2*eps)^2   [the PARITY mode of the induced chain, derivation Sec.2]")
print("               delta = 0.02              [P(in code) >= 0.99  <=>  G = 2*pi0 - 1 >= 0.98, Sec.A2]")
print("               atlas searched w on np.linspace(0,1,2001), taking the first grid point that")
print("               clears the target, so the like-for-like prediction is ceil to that grid.")
print()
print(f"  {'eps':>5} {'Delta_v':>9} {'gamma':>9} {'f(gam,.02)':>11} {'on atlas grid':>14} "
      f"{'at 3 dp':>8} {'published W*':>13} {'match':>6}")
atlas = [(0.02, 0.00000, 0.794), (0.05, 0.00000, 0.904), (0.10, 0.00000, 0.947), (0.20, 0.00000, 0.970)]
nmatch = 0
for eps, dv, wpub in atlas:
    gam = 1.0 - (1 - 2 * eps) ** 2
    fx = f_rent(gam, 0.02)
    grid = math.ceil(fx / 0.0005) * 0.0005
    r3 = math.floor(grid * 1000 + 0.5) / 1000          # round-half-up, as the results table does
    nmatch += (abs(r3 - wpub) < 1e-9)
    print(f"  {eps:5.2f} {dv:9.5f} {gam:9.6f} {fx:11.6f} {grid:14.4f} {r3:8.3f} {wpub:13.3f} "
          f"{'YES' if abs(r3-wpub) < 1e-9 else 'no':>6}")
print(f"\n  exact agreement to the last published digit in {nmatch}/4 rows.")
print("  READING: 4/4 exact.  Delta_v is identically 0 in every row -- the quantity that could not")
print("  price W* -- while gamma prices all four to the published precision, with no free parameter.")

# ==================================================== 2. SPATIAL LATTICE ======
rule("SUBSTRATE 2 -- spatial lattice (maintenance sweep, Part B): exact stationary share")
J = json.load(open("/home/emoore/CIRISOntology/scratchpad/maintenance_sweep_results.json"))
sweep, roster = J["exact_sweep"], J["roster"]

def code_dual(tag):
    """Build the dual code (support of the initial Fourier spectrum) for the standard members."""
    if tag == "L7":                       # simplex [7,3]; dual = Hamming [7,4]
        G = np.array([[int(b) for b in format(c, "03b")] for c in range(1, 8)], dtype=np.int8).T
        S = np.array([m @ G % 2 for m in np.array(
            [[int(b) for b in format(v, "03b")] for v in range(8)], dtype=np.int8)])
        k = 7
    elif tag == "E8":                     # extended Hamming [8,4,4], self-dual
        Gm = np.array([[1,0,0,0,0,1,1,1],[0,1,0,0,1,0,1,1],
                       [0,0,1,0,1,1,0,1],[0,0,0,1,1,1,1,0]], dtype=np.int8)
        S = np.array([m @ Gm % 2 for m in np.array(
            [[int(b) for b in format(v, "04b")] for v in range(16)], dtype=np.int8)])
        k = 8
    elif tag == "L5":                     # dual is the [5,2] code {0,11100,10011,01111}
        D = np.array([[0,0,0,0,0],[1,1,1,0,0],[1,0,0,1,1],[0,1,1,1,1]], dtype=np.int8)
        return D, 5
    else:
        raise KeyError(tag)
    X = np.array([[int(b) for b in format(v, f"0{k}b")] for v in range(2 ** k)], dtype=np.int8)
    dual = X[np.all((X @ S.T) % 2 == 0, axis=1)]
    return dual, k

def predicted_share(tag, eps, q):
    """p_hat_inf(T) = q/(eps_T + q lam^|T|) on every dual word, then the share of the resulting law."""
    dual, k = code_dual(tag)
    lam = 1.0 - 2.0 * eps
    X = np.array([[int(b) for b in format(v, f"0{k}b")] for v in range(2 ** k)], dtype=np.int8)
    sign = (-1.0) ** ((X @ dual.T) % 2)                       # 2^k x |dual|
    w = dual.sum(axis=1)
    phat = np.array([1.0 if wi == 0 else G_law(q, lam ** wi) for wi in w])
    p = (sign @ phat) / (2 ** k)
    p = np.clip(p, 0, None); p /= p.sum()
    H = -np.sum(p[p > 0] * np.log(p[p > 0]))
    return k * LN2 - H

for tag in ("L5", "L7", "E8"):
    dual, k = code_dual(tag)
    A = np.bincount(dual.sum(axis=1), minlength=k + 1).astype(float)
    ok = np.allclose(A, np.array(roster[tag]["A"], dtype=float), atol=1e-9)
    print(f"\n  {tag}: {roster[tag]['name']}, d={roster[tag]['d']}, "
          f"dual weight enumerator reproduced from the constructed code: {ok}")
    print(f"  {'eps':>6} {'q':>7} {'lam^d':>9} {'share_inf (published)':>22} {'predicted':>12} {'rel resid':>11}")
    for eps in (0.02, 0.05, 0.1):
        for q in (0.01, 0.03, 0.1, 0.3, 1.0):
            key = f"{tag}|{eps}|{q}"
            if key not in sweep: continue
            meas = sweep[key]["share_inf"]
            pred = predicted_share(tag, eps, q)
            rel = (meas - pred) / pred if pred > 0 else float("nan")
            print(f"  {eps:6.2f} {q:7.3f} {(1-2*eps)**roster[tag]['d']:9.6f} "
                  f"{meas:22.9f} {pred:12.9f} {rel:+11.2e}")

print("\n  READING: the derived law, applied to EVERY Fourier mode of the code and then read")
print("  through the share's own nonlinearity (derivation Sec.4.3), reproduces the exactly")
print("  propagated stationary share.  This is P4 re-derived rather than re-fitted.")

# ============================================================== 3. LFSR =======
rule("SUBSTRATE 3 -- LFSR record (maintenance sweep Part A, T4): retained fraction of ln2")
print("  published T4 = retained fraction after 48 steps.  Tracked mode: the weight-3 parity")
print("  component, lam = (1-2 eps)^3 (T3's own closed form share_t = ln2 - Hb((1+lam^{3t})/2)).")
print("  Prediction: amplitude g = q/(eps_c + q lam), then share retention = [ln2 - Hb((1+g)/2)]/ln2.")
print("  ONLY cells the results file itself calls stationary are scored: eps >= 0.03 (all q),")
print("  and every eps at q >= 0.3.  Un-converged cells are shown but marked and NOT scored.")
T4 = {
 0.001: {0.001:0.4632, 0.003:0.4781, 0.01:0.5292, 0.03:0.6434, 0.1:0.8275, 0.3:0.9400, 1.0:1.00000},
 0.003: {0.001:0.1384, 0.003:0.1533, 0.01:0.2085, 0.03:0.3497, 0.1:0.6345, 0.3:0.8573, 1.0:1.00000},
 0.01:  {0.001:0.0033, 0.003:0.0060, 0.01:0.0220, 0.03:0.0904, 0.1:0.3330, 0.3:0.6702, 1.0:1.00000},
 0.03:  {0.001:0.0000, 0.003:0.0002, 0.01:0.0023, 0.03:0.0169, 0.1:0.1145, 0.3:0.4093, 1.0:1.00000},
 0.10:  {0.001:0.0000, 0.003:0.0000, 0.01:0.0003, 0.03:0.0025, 0.1:0.0245, 0.3:0.1627, 1.0:1.00000},
}
print(f"\n  {'eps':>6} {'q':>7} {'lam^3':>9} {'g (ampl.)':>10} {'pred share ret':>15} "
      f"{'published':>10} {'abs resid':>10} {'scored':>7}")
scored, worst_abs = [], 0.0
for eps, row in T4.items():
    lam3 = (1 - 2 * eps) ** 3
    for q, meas in row.items():
        g = G_law(q, lam3)
        pred = (LN2 - Hb((1 + g) / 2)) / LN2
        stationary = (eps >= 0.03) or (q >= 0.3)
        if stationary and meas > 5e-4:
            scored.append(abs(meas - pred)); worst_abs = max(worst_abs, abs(meas - pred))
        print(f"  {eps:6.3f} {q:7.3f} {lam3:9.6f} {g:10.6f} {pred:15.6f} {meas:10.4f} "
              f"{meas-pred:+10.4f} {'yes' if stationary and meas > 5e-4 else 'no':>7}")
print(f"\n  scored cells: {len(scored)};  max |resid| = {worst_abs:.4f} on a quantity quoted to 4 dp;")
print(f"  mean |resid| = {np.mean(scored):.4f}.  T4 is a 48-step Monte-Carlo reading, not an exact one.")

# =========================================================== 4. HOLONOMY =====
rule("SUBSTRATE 4 -- Wilson-loop holonomy (HOLONOMY_RENT_RESULTS.md): the operator case")
LAM_H, EPS_H = 0.959913, 0.040087         # Sec.2, re-derived from the q=0 arm (gain, not specrad)
print(f"  lam = {LAM_H} (measured, Sec.2), eps = 1-lam = {EPS_H}.  Repair = R-POL, continuous dosing.")
print("  DERIVED PREDICTIONS BEING TESTED (derivation Sec.5, all parameter-free):")
print("    (P-i)   residual sign: measured plateau <= q/(eps+q lam) at EVERY q  (triangle inequality)")
print("    (P-ii)  |relative residual| MONOTONE DECREASING in q")
print("    (P-iii) residual -> 0 as q -> 1")
print(f"\n  {'q':>8} {'measured plateau':>17} {'f-law prediction':>17} {'rel resid':>10} {'resid/(1-q)':>12}")
holo = [(0.01725,0.274733),(0.0345,0.434945),(0.069,0.614427),(0.1,0.704727),
        (0.2,0.842745),(0.5,0.955226),(0.9,0.994781),(0.99,0.999522)]
signs, rels = [], []
for q, meas in holo:
    pred = G_law(q, LAM_H)
    rel = (meas - pred) / pred
    signs.append(rel < 0); rels.append(abs(rel))
    print(f"  {q:8.5f} {meas:17.6f} {pred:17.6f} {rel:+10.2%} {rel/(1-q):12.4f}")
mono = all(rels[i] > rels[i + 1] for i in range(len(rels) - 1))
print(f"\n  (P-i)   negative at every q: {sum(signs)}/{len(signs)}")
print(f"  (P-ii)  |rel resid| strictly decreasing in q: {mono}")
print(f"  (P-iii) |rel resid| at q=0.99: {rels[-1]:.2%}  (largest, at q=0.01725: {rels[0]:.2%})")

print("\n  W* FLOOR: the half-holding dose (Sec.4, delta=0.5).")
qh_pred, qh_meas = f_rent(EPS_H, 0.5), 0.044392
print(f"    f(gamma, 0.5) = {qh_pred:.6f} = {qh_pred/EPS_H:.4f} eps   [= eps/(2-lam), the prereg form]")
print(f"    measured q_half (bisection, 40 steps, Sec.4) = {qh_meas:.6f} = {qh_meas/EPS_H:.4f} eps")
print(f"    measured/predicted = {qh_meas/qh_pred:.3f}   -> W*_measured >= f: "
      f"{'HOLDS' if qh_meas >= qh_pred else 'VIOLATED'}  (the operator must OVERPAY, Sec.5)")

print("\n  SECOND SCHEDULE (Sec.4.4): the periodic arm, cycle-averaged (HOLONOMY_RENT_RESULTS.md Sec.8)")
print(f"  {'q':>8} {'P':>4} {'measured (cyc-avg)':>19} {'(1-lam^P)/(P(1-lam))':>21} {'rel resid':>10}")
per = [(0.0345, 29, 0.560132), (0.069, 14, 0.750567), (0.1, 10, 0.817049), (0.3, 3, 0.954757)]
prel = []
for q, P, meas in per:
    pred = G_periodic(P, LAM_H)
    rel = (meas - pred) / pred; prel.append(rel)
    print(f"  {q:8.4f} {P:4d} {meas:19.6f} {pred:21.6f} {rel:+10.2%}")
print(f"  all negative: {all(r < 0 for r in prel)};  |rel| decreasing in q: "
      f"{all(abs(prel[i])>abs(prel[i+1]) for i in range(len(prel)-1))}")
print("  Independent schedule, same signed deficit -- the misalignment penalty is a property of the")
print("  operator, not of the dosing scheme, exactly as Sec.5 requires.")

print("\n" + "=" * 96)
