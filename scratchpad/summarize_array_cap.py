"""summarize_array_cap.py — apply the PRE-REGISTERED verdict rules to the sweep output.

Rules are quoted from scratchpad/ARRAY_CAP_PREREG.md; nothing here is chosen after data.
"""
import json, sys, os
import numpy as np

LN2 = float(np.log(2))
P = os.path.dirname(os.path.abspath(__file__))
rows = json.load(open(os.path.join(P, 'array_cap_results.json')))

def key(r):
    return (r['tag'], r['kappa'], r['seed'])

# ---------------- JOB 1: cap compliance ----------------
print("=" * 96)
print("JOB 1 — CAP COMPLIANCE (instrument control for the Bell claim)")
print("=" * 96)
viol = [r for r in rows if not r['chk_cap_robust']]
eng1 = [r for r in rows if not r['chk_entropy_map_le']]
eng2 = [r for r in rows if not r['chk_maxent_le_logcard']]
hl = [r for r in rows if not r['chk_cap_headline']]
print(f"readings total                              : {len(rows)}")
print(f"VIOLATIONS of proved robust cap k*ln2-H(pair): {len(viol)}   <-- VOID if > 0")
print(f"engine  H(pair pushforward) <= H(whole)      : {'HOLDS' if not eng1 else 'FAILS'} "
      f"({len(rows)} readings x C(k,2) pairs)")
print(f"engine  H(maxent) <= k*ln2                   : {'HOLDS' if not eng2 else 'FAILS'}")
print(f"exceedances of headline cap (k-2)*ln2        : {len(hl)}")
worst = min(rows, key=lambda r: r['margin_robust'])
print(f"tightest robust-cap margin observed          : {worst['margin_robust']:.6f} nats "
      f"({worst['tag']} kappa={worst['kappa']} {worst['boundary']} seed={worst['seed']})")
p3 = [r for r in rows if r['tag'] == 'P3-inject']
print("\nCAP-SATURATING STRESS TEST (P3-inject f=1; three-coin parity saturates the k=3 cap):")
for r in p3:
    print(f"  boundary={r['boundary']:<5} share={r['share']:.6f}  cap=(3-2)ln2={r['cap_headline']:.6f}  "
          f"share/cap={r['share']/r['cap_headline']:.4f}  margin={r['margin_headline']:+.6f}  "
          f"z={r['z']:.0f}  ROB_OK={r['chk_cap_robust']}  HL_OK={r['chk_cap_headline']}")
ctrl = [r for r in rows if r['tag'] in ('S3-phase', 'S5-phase')]
fired = [r for r in ctrl if r['z'] > 5]
print(f"\nARCHITECTURALLY-UNCOUPLED CONTROLS (S3-phase,S5-phase): {len(ctrl)} readings, "
      f"{len(fired)} with z>5")
if fired:
    for r in sorted(fired, key=lambda r: -r['z'])[:8]:
        print(f"  FIRED: {r['tag']} kappa={r['kappa']} {r['boundary']} seed={r['seed']} "
              f"share={r['share']:.6f} z={r['z']:.1f} tie={r['tie_max']:.4f} "
              f"clip_rate={r['clip_rate']:.3e}")

if hl:
    print("\nHEADLINE-CAP EXCEEDANCES — hypothesis audit (theorem requires a UNIFORM pair marginal):")
    for r in hl:
        print(f"  {r['tag']} k={r['k']} kappa={r['kappa']} {r['boundary']}: share={r['share']:.4f} "
              f"> {r['cap_headline']:.4f}; pair_dev_Linf={r['pair_dev_linf']:.4f} "
              f"(uniform=0), robust cap={r['cap_robust']:.4f}, still compliant={r['chk_cap_robust']}")

# ---------------- JOB 2: ceiling fraction + clip/fold stability ----------------
def verdict(rc, rf):
    """PRE-REGISTERED stability criterion, verbatim."""
    a, b = rc['CF_headline'], rf['CF_headline']
    d = abs(a - b)
    m = max(abs(a), abs(b))
    agree = (rc['z'] > 5) == (rf['z'] > 5)
    rel = d / m if m > 1e-12 else 0.0
    if not agree or rel > 1.0:
        return 'ARTIFACT'
    if d <= 0.02 or rel <= 0.20:
        return 'STABLE'
    return 'MARGINAL'

print("\n" + "=" * 96)
print("JOB 2 — CEILING FRACTION  CF = (share - null_mean) / cap , with clip/fold discriminator")
print("NOT a claim of order-3 discovery: order-3 in this lattice is EXPECTED and clip-prone (prereg).")
print("=" * 96)
tags = ['S3-state', 'T3-state', 'T5-state', 'X5-state', 'S3-phase', 'S5-phase']
kappas = sorted({r['kappa'] for r in rows if r['seed'] == 20260725 and r['tag'] in tags})
idx = {(r['tag'], r['kappa'], r['boundary']): r for r in rows if r['seed'] == 20260725}
crate = {k: idx[('S3-state', k, 'clip')]['clip_rate'] for k in kappas if ('S3-state', k, 'clip') in idx}
frate = {k: idx[('S3-state', k, 'fold')]['clip_rate'] for k in kappas if ('S3-state', k, 'fold') in idx}

print(f"\nclamp-binding rate by coupling (fraction of clamp applications that actually bound):")
print("  kappa : " + "  ".join(f"{k:>7.2f}" for k in kappas))
print("  clip  : " + "  ".join(f"{crate.get(k,float('nan')):>7.1e}" for k in kappas))
print("  fold  : " + "  ".join(f"{frate.get(k,float('nan')):>7.1e}" for k in kappas))

for tag in tags:
    print(f"\n--- {tag} " + "-" * (88 - len(tag)))
    print(f"{'kappa':>6} {'CF_clip':>9} {'CF_fold':>9} {'z_clip':>10} {'z_fold':>10} "
          f"{'tie_clip':>8} {'tie_fold':>8} {'verdict':>9} {'quotable':>9}")
    for k in kappas:
        rc = idx.get((tag, k, 'clip')); rf = idx.get((tag, k, 'fold'))
        if rc is None or rf is None:
            continue
        v = verdict(rc, rf)
        trivial = (rc['clip_rate'] == 0.0 and rf['clip_rate'] == 0.0)
        tiebad = max(rc['tie_max'], rf['tie_max']) > 0.01
        q = 'no'
        if v == 'STABLE' and not trivial and not tiebad:
            q = 'YES'
        elif v == 'STABLE' and trivial:
            q = 'trivial'
        elif tiebad:
            q = 'tie-cont'
        print(f"{k:>6.2f} {rc['CF_headline']:>9.5f} {rf['CF_headline']:>9.5f} "
              f"{rc['z']:>10.1f} {rf['z']:>10.1f} {rc['tie_max']:>8.4f} {rf['tie_max']:>8.4f} "
              f"{v:>9} {q:>9}")

# k=5 also against the exact classical max
print("\n--- k=5 readings against BOTH caps (tiers kept unblurred) ---")
print(f"{'tag':>9} {'kappa':>6} {'bnd':>5} {'share':>9} {'CF vs 3ln2':>11} {'CF vs 2ln2':>11} "
      f"{'(proved)':>9} {'(exact)':>9}")
for tag in ('T5-state', 'X5-state', 'S5-phase'):
    for k in kappas:
        for b in ('clip', 'fold'):
            r = idx.get((tag, k, b))
            if r is None:
                continue
            print(f"{tag:>9} {k:>6.2f} {b:>5} {r['share']:>9.5f} {r['CF_headline']:>11.5f} "
                  f"{r['CF_exact']:>11.5f} {2.079442:>9.4f} {1.386294:>9.4f}")

# replication
print("\n--- replication at kappa=0.05, seeds 20260725 / 99 / 7 ---")
print(f"{'tag':>9} {'bnd':>5} " + " ".join(f"{'CF@'+str(s):>12}" for s in (20260725, 99, 7)))
for tag in tags:
    for b in ('clip', 'fold'):
        vals = []
        for s in (20260725, 99, 7):
            m = [r for r in rows if r['tag'] == tag and r['kappa'] == 0.05
                 and r['boundary'] == b and r['seed'] == s]
            vals.append(m[0]['CF_headline'] if m else float('nan'))
        print(f"{tag:>9} {b:>5} " + " ".join(f"{v:>12.6f}" for v in vals))
