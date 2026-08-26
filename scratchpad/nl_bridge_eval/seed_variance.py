#!/usr/bin/env python3
"""Fine-tune run-to-run variance on the frozen 92. Turns a quoted range into an error bar."""
import json, glob, os, statistics, collections
P = os.path.dirname(os.path.abspath(__file__))

runs = []
# the two original runs (seed 20260822, differing only by GPU nondeterminism)
for f, tag in ((f"{P}/pred4_qwen3_ft.jsonl", "orig-run2(seed 20260822)"),):
    if os.path.exists(f):
        r = [json.loads(l) for l in open(f)]
        runs.append((tag, sum(x["pred"] == x["gold"] for x in r) / len(r), r))
for f in sorted(glob.glob(f"{P}/pred4_qwen3_ft_s*.jsonl")):
    r = [json.loads(l) for l in open(f)]
    runs.append((os.path.basename(f).replace("pred4_qwen3_ft_", "").replace(".jsonl", ""),
                 sum(x["pred"] == x["gold"] for x in r) / len(r), r))

print(f"{'run':28s} {'4-way acc':>10s}")
for t, a, _ in runs: print(f"  {t:26s} {a:10.3f}")
accs = [a for _, a, _ in runs]
# the first run (0.783) was scored before the merged-model save; recorded from the log
print(f"  {'orig-run1 (from log)':26s} {0.783:10.3f}   [predictions overwritten by run2]")
allacc = accs + [0.783]
print()
print(f"n runs = {len(allacc)}")
print(f"  mean   = {statistics.mean(allacc):.3f}")
print(f"  sd     = {statistics.pstdev(allacc):.3f}" if len(allacc) > 1 else "")
print(f"  min-max= {min(allacc):.3f} - {max(allacc):.3f}   (spread {max(allacc)-min(allacc):.3f})")
if len(allacc) > 2:
    sd = statistics.stdev(allacc)
    se = sd / len(allacc) ** 0.5
    print(f"  sample sd = {sd:.3f}, SE of mean = {se:.3f}")
    print(f"  95% CI on the MEAN = {statistics.mean(allacc)-1.96*se:.3f} - {statistics.mean(allacc)+1.96*se:.3f}")
    print(f"  expected range of a SINGLE run (mean +/- 1.96sd) = "
          f"{statistics.mean(allacc)-1.96*sd:.3f} - {statistics.mean(allacc)+1.96*sd:.3f}")

# per-item agreement across runs: is the variance concentrated on a few hard items?
if len(runs) > 1:
    byitem = collections.defaultdict(list)
    for _, _, r in runs:
        for x in r: byitem[x["id"]].append(x["pred"] == x["gold"])
    unstable = sum(1 for v in byitem.values() if 0 < sum(v) < len(v))
    always_r = sum(1 for v in byitem.values() if all(v))
    never_r = sum(1 for v in byitem.values() if not any(v))
    print(f"\nper-item stability across {len(runs)} scored runs (n={len(byitem)}):")
    print(f"  always correct {always_r} | never correct {never_r} | UNSTABLE {unstable} "
          f"({unstable/len(byitem):.1%})")
