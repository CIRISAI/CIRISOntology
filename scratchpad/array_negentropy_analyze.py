"""array_negentropy_analyze.py — apply the pre-registered verdict rules of
ARRAY_NEGENTROPY_PREREG.md to the sweep output.  No new measurement is made here."""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2))
RAIL_MAX = 0.01          # pre-set in the prereg
ZBAR = 5.0

def load(name):
    with open(os.path.join(HERE, name)) as f:
        return json.load(f)

def key(r):
    return (r['tag'], round(r['kappa'], 4), r['sigma'])

def classify(c, f):
    """Pre-registered boundary discriminator.  c, f are the clip and fold rows."""
    if c is None or f is None:
        return 'MISSING'
    if max(c['clip_rate'], f['clip_rate']) == 0.0:
        return 'TRIVIAL'                      # clamp never binds: no robustness info,
                                              # but also artifact-free by construction
    cz = abs(c['z']) > ZBAR and abs(c['z_cons']) > ZBAR
    fz = abs(f['z']) > ZBAR and abs(f['z_cons']) > ZBAR
    if not cz and not fz:
        return 'FLOOR'
    if cz != fz:
        return 'ARTIFACT'
    a, b = c['s_deb'], f['s_deb']
    if min(a, b) <= 0:
        return 'ARTIFACT'
    return 'STABLE' if max(a / b, b / a) <= 2.0 else 'LEVEL-ARTIFACT'

def main():
    rows = load('array_negentropy_sweep.json')
    by = {}
    for r in rows:
        by.setdefault(key(r), {})[r['boundary']] = r
    tags = sorted({r['tag'] for r in rows},
                  key=lambda t: (t[0] != 'S', t[0] != 'C', len(t), t))
    kaps = sorted({round(r['kappa'], 4) for r in rows})
    sigs = sorted({r['sigma'] for r in rows})

    # ---------- floors -------------------------------------------------------------
    print("=" * 100)
    print("FLOORS — the pre-registered controls (K2 fires on any |z| > 5)")
    print("=" * 100)
    for t in ('FARP', 'SHIFT'):
        zs = np.array([r['z'] for r in rows if r['tag'] == t])
        bad = [r for r in rows if r['tag'] == t and abs(r['z']) > ZBAR]
        print(f"  {t:<6} n={len(zs):>4}  mean z={zs.mean():+.3f}  sd={zs.std():.3f}  "
              f"max|z|={np.abs(zs).max():.2f}  exceeding 5: {len(bad)}")
        for r in bad[:6]:
            print(f"      kappa={r['kappa']} sigma={r['sigma']} {r['boundary']} "
                  f"z={r['z']:+.2f} rail={r['rail']:.4f}")

    # ---------- rails --------------------------------------------------------------
    print("\n" + "=" * 100)
    print("RAIL FRACTION — the clamp diagnostic, reported like a tied fraction")
    print("=" * 100)
    for b in ('clip', 'fold'):
        print(f"  {b}:")
        print("        sigma " + "".join(f"{s:>9g}" for s in sigs))
        for k in kaps:
            cells = []
            for s in sigs:
                m = [r['rail'] for r in rows if r['boundary'] == b and
                     round(r['kappa'], 4) == k and r['sigma'] == s]
                cells.append(f"{max(m):>9.4f}" if m else f"{'-':>9}")
            print(f"  k={k:<6.2f}" + "".join(cells))

    # ---------- the maps -----------------------------------------------------------
    for t in ('S3', 'C3', 'T3d1', 'T3d2', 'T3d4'):
        print("\n" + "=" * 100)
        print(f"{t} — s_deb (nats), pre-registered verdict per cell "
              f"[S=stable L=level-artifact A=artifact F=floor T=trivial R=railed]")
        print("=" * 100)
        print("        sigma " + "".join(f"{s:>12g}" for s in sigs))
        for k in kaps:
            cells = []
            for s in sigs:
                d = by.get((t, k, s), {})
                c, f = d.get('clip'), d.get('fold')
                if not c or not f:
                    cells.append(f"{'-':>12}"); continue
                v = classify(c, f)
                railed = max(c['rail'], f['rail']) > RAIL_MAX
                mark = 'R' if railed else v[0]
                cells.append(f"{f['s_deb']:>+10.3e}{mark} ")
            print(f"  k={k:<6.2f}" + "".join(cells))
        print("   (value shown is the FOLD arm — the smooth boundary; see rail table)")

    # ---------- the ridge ----------------------------------------------------------
    print("\n" + "=" * 100)
    print("THE RIDGE — best boundary-stable, rail-clean reading, both z bars cleared")
    print("=" * 100)
    good = []
    for kk, d in by.items():
        t, k, s = kk
        if t in ('FARP', 'SHIFT'):
            continue
        c, f = d.get('clip'), d.get('fold')
        if not c or not f:
            continue
        v = classify(c, f)
        if max(c['rail'], f['rail']) > RAIL_MAX:
            continue
        if v not in ('STABLE', 'TRIVIAL'):
            continue
        if not (abs(f['z']) > ZBAR and abs(f['z_cons']) > ZBAR):
            continue
        good.append((min(c['s_deb'], f['s_deb']), t, k, s, v, c, f))
    good.sort(reverse=True)
    print(f"  {len(good)} readings qualify.  Top 15 by the CONSERVATIVE (smaller-arm) value:")
    print("   rank  reading  kappa  sigma      s_clip       s_fold    ratio   CF(fold)  "
          "z_fold  z_cons  verdict  clamp")
    for i, (v, t, k, s, ver, c, f) in enumerate(good[:15]):
        print(f"   {i+1:>4}  {t:<7} {k:<6} {s:<8g} {c['s_deb']:+.4e} {f['s_deb']:+.4e} "
              f"{max(c['s_deb'],f['s_deb'])/max(min(c['s_deb'],f['s_deb']),1e-99):>6.2f} "
              f"{f['s_deb']/LN2:>9.5f} {f['z']:>+8.0f} {f['z_cons']:>+8.0f}  {ver:<8} "
              f"{f['clip_rate']:.1e}")

    # ---------- TIER B: fold-only (clip rail-disqualified) --------------------------
    print("\n" + "=" * 100)
    print("TIER B — where the CLIP arm is rail-disqualified, so the boundary discriminator")
    print("is UNAVAILABLE rather than failed.  Fold is rail-free everywhere; these readings")
    print("are internally valid but carry NO boundary-stability certificate.")
    print("=" * 100)
    fo = []
    for kk, d in by.items():
        t, k, s = kk
        if t in ('FARP', 'SHIFT'):
            continue
        c, f = d.get('clip'), d.get('fold')
        if not c or not f or c['rail'] <= RAIL_MAX:
            continue                                  # tier A handled above
        if f['rail'] > RAIL_MAX:
            continue
        if not (abs(f['z']) > ZBAR and abs(f['z_cons']) > ZBAR):
            continue
        fo.append((f['s_deb'], t, k, s, c, f))
    fo.sort(reverse=True)
    print(f"  {len(fo)} fold-only readings clear both z bars.  Top 12:")
    print("   rank  reading  kappa  sigma     s_fold    CF(fold)   z_fold  z_cons   "
          "clip_rail  s_clip(disqualified)")
    for i, (v, t, k, s, c, f) in enumerate(fo[:12]):
        print(f"   {i+1:>4}  {t:<7} {k:<6} {s:<8g} {v:+.4e} {v/LN2:>9.5f} {f['z']:>+8.0f} "
              f"{f['z_cons']:>+8.0f}   {c['rail']:.4f}    {c['s_deb']:+.3e}")

    # ---------- interior maxima (P4, P5) -------------------------------------------
    print("\n" + "=" * 100)
    print("P4 / P5 — interior maxima in coupling and in noise (FOLD arm, rail-clean)")
    print("=" * 100)
    for t in ('S3', 'C3', 'T3d1'):
        print(f"\n  {t}:")
        # P4: vs kappa at each sigma
        for s in sigs:
            vals = []
            for k in kaps:
                d = by.get((t, k, s), {})
                f = d.get('fold')
                vals.append(f['s_deb'] if f and f['rail'] <= RAIL_MAX else np.nan)
            vals = np.array(vals)
            if np.all(np.isnan(vals)):
                continue
            j = int(np.nanargmax(vals))
            interior = 0 < j < len(kaps) - 1
            print(f"    sigma={s:<8g} argmax_kappa = {kaps[j]:<6} "
                  f"s = {vals[j]:+.4e}  {'INTERIOR' if interior else 'EDGE'}"
                  f"   (kappa=0 value {vals[0]:+.3e}, ratio {vals[j]/vals[0]:.2f})"
                  if vals[0] > 0 else
                  f"    sigma={s:<8g} argmax_kappa = {kaps[j]:<6} s = {vals[j]:+.4e}")
        # P5: vs sigma at each kappa
        print("    --- noise axis ---")
        for k in kaps:
            vals = []
            for s in sigs:
                d = by.get((t, k, s), {})
                f = d.get('fold')
                vals.append(f['s_deb'] if f and f['rail'] <= RAIL_MAX else np.nan)
            vals = np.array(vals)
            if np.all(np.isnan(vals)):
                continue
            j = int(np.nanargmax(vals))
            print(f"    kappa={k:<6} argmax_sigma = {sigs[j]:<8g} s = {vals[j]:+.4e}  "
                  f"{'INTERIOR' if 0 < j < len(sigs)-1 else 'EDGE'}  "
                  f"[sigma=0: {vals[0]:+.3e}, sigma=0.1: {vals[-1]:+.3e}]")

    # ---------- P6 separation ------------------------------------------------------
    print("\n" + "=" * 100)
    print("P6 — temporal separation: argmax over Delta of T3d(Delta), FOLD, rail-clean")
    print("=" * 100)
    deltas = sorted(int(t[3:]) for t in tags if t.startswith('T3d'))
    print("        Delta " + "".join(f"{d:>12}" for d in deltas))
    for k in kaps:
        for s in (1e-3,) if True else ():
            vals = []
            for d in deltas:
                r = by.get((f'T3d{d}', k, s), {}).get('fold')
                vals.append(r['s_deb'] if r and r['rail'] <= RAIL_MAX else np.nan)
            if np.all(np.isnan(vals)):
                continue
            j = int(np.nanargmax(vals))
            print(f"  k={k:<6.2f}" + "".join(f"{v:>+12.2e}" for v in vals) +
                  f"   argmax = Delta {deltas[j]}")

if __name__ == '__main__':
    main()
