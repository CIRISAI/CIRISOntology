#!/usr/bin/env python3
"""AMENDMENT_A2's two BINDING pre-judging measurements, reported before any judging.

1. Distinct arm-C path count: 'materially above 4' or A2 failed on its own terms.
   Counted at the level the treatment operates: the rendered path STRING (what the
   renderer sees), not internal arrival steps.
2. Entropy of the four-way softmax (computed at encode time; summarised here per item
   actually generated): if most items are near one-hot, soft collapsed to hard and the
   bottleneck is classifier confidence.

Also reports per-arm path diversity and the C-vs-B path-divergence rate (the pair is
vacuous on items where C's path equals the assigned B's path).
"""
import json, sys, math, collections

def main(respfile):
    rows = [json.loads(l) for l in open(respfile)]
    byarm = collections.defaultdict(list)
    for r in rows: byarm[r["arm"]].append(r)

    cpaths = [r["path"] for r in byarm["C"]]
    n_items = len(cpaths)
    distinct_c = len(set(cpaths))
    print(f"MEASUREMENT 1 -- distinct arm-C paths: {distinct_c} across {n_items} items")
    top = collections.Counter(cpaths).most_common(5)
    for p, c in top: print(f"    {c:3d}x  {p[:100]}")
    verdict = "PASS (materially above 4)" if distinct_c > 8 else \
              ("MARGINAL" if distinct_c > 4 else "FAIL -- A2 failed on its own terms; report, do not judge")
    print(f"  gate: {verdict}")

    ent = [r.get("entropy") for r in byarm["C"] if r.get("entropy") is not None]
    if ent:
        ent = sorted(ent)
        onehot = sum(e < 0.10 for e in ent)
        print(f"\nMEASUREMENT 2 -- softmax entropy on generated items (ln4={math.log(4):.3f}):")
        print(f"  mean={sum(ent)/len(ent):.3f} median={ent[len(ent)//2]:.3f} "
              f"min={ent[0]:.3f} max={ent[-1]:.3f}")
        print(f"  effectively one-hot (H<0.10): {onehot}/{len(ent)} = {onehot/len(ent):.1%}")

    # distinct paths per arm + the per-pair divergence the comparison rests on
    print("\npath diversity per arm:")
    for a in sorted(byarm):
        ps = {r["path"] for r in byarm[a] if r.get("path")}
        print(f"  {a}: distinct={len(ps)} of n={len(byarm[a])}")
    bees = collections.defaultdict(dict)
    for r in byarm["B"]: bees[r["id"]][r.get("scramble_id")] = r["path"]
    cby = {r["id"]: r["path"] for r in byarm["C"]}
    same = 0; tot = 0
    for iid, cp in cby.items():
        for s, bp in bees[iid].items():
            tot += 1; same += (cp == bp)
    print(f"\nC path == B path (all 10 draws x items): {same}/{tot} = {same/tot:.3f} "
          f"(a high rate would make C-vs-B trivially null)")

if __name__ == "__main__":
    main(sys.argv[1])
