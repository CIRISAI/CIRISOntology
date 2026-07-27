"""rent_scaling_q1_subset_analyze.py — the H-SUBSET verdict, by the rules AMENDMENT 1 fixed.

Written before the run finished, so the adjudication is by rule and not by eye.

AMENDMENT 1's outcome table, restated verbatim as the rule this file applies:
  * H-IFF holds on canonical AND on random subsets -> the characterisation is a fact about
    the support, not about a column order.
  * H-IFF holds on canonical but FAILS on >= 1 random subset -> that is the primary result of
    Q1, reported as the headline: the canonical ladder is unrepresentative.
  * H-IFF fails on both -> H-IFF is simply dead and the subset arm is concordant.

TALLY DISCIPLINE. Three exclusions, all fixed before any verdict is read:
  1. rows with exact=False (search budget exhausted) are UNDETERMINED and excluded;
  2. draws identical to the canonical first-k truncation are NOT out of sample;
  3. repeated draws within an (N,k) cell are counted once.
The out-of-sample tally is quoted against what survives all three.
"""
import sys, os, json, argparse
from collections import defaultdict


def main(src, canon=None):
    D = json.load(open(src))
    rows, meta = D['rows'], D['meta']
    print("=" * 88)
    print(f"H-SUBSET — {len(rows)} of {meta['n_planned']} evaluated   "
          f"seed {meta['seed']}   node budget {meta['node_budget']:.0e}")
    print("=" * 88)

    und = [r for r in rows if not r['exact']]
    dec = [r for r in rows if r['exact']]
    seen, uniq = set(), []
    for r in dec:
        key = (r['order'], tuple(r['cols']))
        if key in seen:
            continue
        seen.add(key)
        uniq.append(r)
    oos = [r for r in uniq if tuple(r['cols']) != tuple(range(r['k']))]

    print(f"\nTALLY\n  evaluated              {len(rows)}")
    print(f"  UNDETERMINED (excluded){len(und):>5}")
    print(f"  decided                {len(dec)}")
    print(f"  distinct column sets   {len(uniq)}")
    print(f"  distinct AND non-canonical (the out-of-sample tally) {len(oos)}")

    iff_bad = [r for r in oos if not r['iff_ok']]
    orb_bad = [r for r in oos if not r['orbit_eq_levels']]
    ref_bad = [r for r in oos if not r['orbits_refine_levels']]
    rest = [r for r in oos if r['restorable']]
    trans = [r for r in oos if r['transitive']]

    print(f"\nPOPULATIONS (out-of-sample, n={len(oos)})")
    print(f"  restorable   {len(rest):>4}   intransitive {len(oos)-len(trans):>4}")
    print(f"  transitive   {len(trans):>4}   lossy        {len(oos)-len(rest):>4}")

    print(f"\nVERDICTS")
    print(f"  (T) transitive => restorable   violations: {len(ref_bad)}"
          f"   <-- MUST be 0; nonzero = instrument fault")
    print(f"  H-IFF  restorable <=> transitive violations: {len(iff_bad)}")
    for r in iff_bad:
        print(f"      {r['label']:16s} orbits={r['orbit_sizes']} |Aut|={r['aut_order']} "
              f"dev={r['profile_dev']:.3e} restorable={r['restorable']} "
              f"transitive={r['transitive']}")
    print(f"  H-ORBIT level sets == orbits    violations: {len(orb_bad)}")
    by = defaultdict(int)
    for r in orb_bad:
        by[(r['order'], r['k'])] += 1
    for kk in sorted(by):
        print(f"      N={kk[0]} k={kk[1]}: {by[kk]}")

    if canon and os.path.exists(canon):
        C = json.load(open(canon))
        crows = C['rows'] if isinstance(C, dict) and 'rows' in C else C
        cbad = [r for r in crows
                if r.get('profile_dev') is not None and r.get('transitive') is not None
                and (r['profile_dev'] < meta['equiv_tol']) != r['transitive']]
        print(f"\nCANONICAL ARM (sibling's sweep, for the amendment's decision table)")
        print(f"  rows {len(crows)}   H-IFF violations {len(cbad)}: "
              f"{[r.get('label') for r in cbad]}")
        v = 'H-IFF fails on BOTH arms -> subset arm CONCORDANT, H-IFF simply dead' \
            if cbad and iff_bad else \
            ('H-IFF holds on canonical but FAILS on a random subset -> THE CANONICAL LADDER '
             'IS UNREPRESENTATIVE (primary result)' if iff_bad else
             ('H-IFF fails on canonical, holds on every random subset -> the counterexamples '
              'are SPECIAL to the canonical ordering; report as such' if cbad else
              'H-IFF holds on BOTH -> a fact about supports, not a column order'))
        print(f"\n  AMENDMENT 1 VERDICT: {v}")

    if und:
        print(f"\nUNDETERMINED rows (reported, never counted either way):")
        for r in und:
            print(f"      {r['label']}")


if __name__ == '__main__':
    HERE = os.path.dirname(os.path.abspath(__file__))
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=os.path.join(HERE, 'rent_scaling_q1_subset.json'))
    ap.add_argument('--canon', default=os.path.join(HERE, 'rent_scaling_q1.json'))
    a = ap.parse_args()
    main(a.src, a.canon)
