"""Score the GROSS4 forward stake against GROSS4_FORWARD_PREREG.md.

Modal rule is the frozen one used to produce the 91.4% baseline
(analyze_partd_eco2.py): per item, Counter(non-null BASE kinds).most_common(1)[0][0],
ties broken by first-encountered. Step 0 recomputes the baseline from the archived
judgment files as a calibration of this scorer against the number it must compare to.
"""
import collections, json, os, sys

R = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"
PLAIN12 = ["Priorities", "Rules", "Manner", "Identity", "Confidence", "Facts",
           "Circumstances", "Process", "Model", "Structure", "Premises", "Record"]
GROSS4 = {"Facts", "Rules", "Manner", "Identity"}


def load(p):
    return [json.loads(l) for l in open(p) if l.strip()]


def modals(judgments, prefix=None):
    """item -> (modal label, vote list, models that answered)."""
    votes = collections.defaultdict(list)
    who = collections.defaultdict(set)
    for r in judgments:
        if r.get("condition") != "BASE":
            continue
        if prefix and not r["id"].startswith(prefix):
            continue
        who[r["id"]].add(r["model"])
        if r.get("kind"):
            votes[r["id"]].append(r["kind"])
    out = {}
    for iid, v in votes.items():
        out[iid] = (collections.Counter(v).most_common(1)[0][0], v, who[iid])
    return out


def share(md):
    dist = collections.Counter(m for m, _, _ in md.values())
    g4 = sum(c for k, c in dist.items() if k in GROSS4)
    return dist, g4, len(md)


# ---------- step 0: calibrate on the frozen 279-item baseline ----------
base = []
for f, pre in (("eco_judgments.jsonl", None), ("eco2_judgments.jsonl", "osm2"),
               ("eco2_wiki_judgments.jsonl", "wiki2")):
    p = f"{R}/{f}"
    if os.path.exists(p):
        base += [r for r in load(p) if not pre or r["id"].startswith(pre)]
bm = modals(base)
bdist, bg4, bn = share(bm)
print(f"BASELINE recomputed: n={bn}  gross-four={bg4}/{bn} = {bg4/bn:.4f}")
print(f"  dist: {dict(bdist.most_common())}\n")

# ---------- the forward run ----------
J = load(f"{R}/stackex_judgments.jsonl")
corpus = load(f"{R}/eco_stackex.jsonl")
md = modals(J)
dist, g4, n = share(md)

models_seen = collections.Counter(r["model"] for r in J if r.get("condition") == "BASE")
answered = collections.Counter(r["model"] for r in J
                               if r.get("condition") == "BASE" and r.get("kind"))
full_panel = sum(1 for _, (_, v, w) in md.items() if len(w) == 3 and len(v) == 3)

offtax = {i: m for i, (m, _, _) in md.items() if m not in PLAIN12}
threeway = [i for i, (_, v, _) in md.items()
            if len(v) == 3 and len(set(v)) == 3]

print(f"FORWARD n(items with >=1 usable judgment) = {n}   corpus items = {len(corpus)}")
print(f"  full 3-model panels: {full_panel}/{len(corpus)}")
print(f"  judgments per model: {dict(models_seen)}")
print(f"  parsed (non-null) per model: {dict(answered)}")
print(f"  modal distribution: {dict(dist.most_common())}")
print(f"  three-way-tie items (modal set by first-encountered): {len(threeway)} {threeway}")
print(f"  off-taxonomy modals: {len(offtax)} ({len(offtax)/n:.3%}) {offtax}\n")

g4share = g4 / n
mp = dist.get("Model", 0) + dist.get("Premises", 0)
top = dist.most_common(1)[0][0]

print("=== STAKES ===")
print(f"1 PRIMARY  gross-four share = {g4}/{n} = {g4share:.4f}   band [0.78,0.97] -> "
      f"{'LANDS' if 0.78 <= g4share <= 0.97 else 'MISSES'}"
      f"   kill(<0.6667) -> {'FIRED' if g4share < 2/3 else 'not fired'}")
print(f"2 SECONDARY Model+Premises modal count = {mp}  (<=2) -> "
      f"{'LANDS' if mp <= 2 else 'FAILS'}   [Model {dist.get('Model',0)}, "
      f"Premises {dist.get('Premises',0)}]")
print(f"3 ORDERING modal #1 = {top}  in {{Facts,Manner}} -> "
      f"{'LANDS' if top in ('Facts','Manner') else 'MISSES'}")
print(f"   runner-up: {dist.most_common(3)}")
print("\n=== VOID GATES ===")
print(f"  n usable = {n} (>=45) -> {'ok' if n >= 45 else 'VOID'}")
print(f"  off-taxonomy modal rate = {len(offtax)/n:.3%} (<=10%) -> "
      f"{'ok' if len(offtax)/n <= 0.10 else 'VOID'}")
print(f"  all three judge models present -> "
      f"{'ok' if len(answered) == 3 and min(answered.values()) > 0 else 'VOID'}")

# sensitivity: drop the three-way ties entirely
keep = {i: v for i, v in md.items() if i not in set(threeway)}
d2, g2, n2 = share(keep)
print(f"\n[sensitivity, not the verdict] ties dropped: {g2}/{n2} = {g2/n2:.4f}")

# per-sub-community breakdown (free analysis)
sub = {r["id"]: r["sub"] for r in corpus}
print("\n[free analysis] per sub-community modal profile")
for s in ("superuser", "english", "diy"):
    sm = {i: v for i, v in md.items() if sub.get(i) == s}
    d3, g3, n3 = share(sm)
    print(f"  {s:10s} n={n3:2d} gross-four={g3}/{n3}={g3/n3:.3f}  {dict(d3.most_common())}")

json.dump({"n": n, "gross4": g4, "gross4_share": g4share,
           "dist": dict(dist), "model_plus_premises": mp, "top": top,
           "offtax": offtax, "threeway_ties": threeway,
           "baseline_n": bn, "baseline_share": bg4 / bn},
          open(f"{R}/stackex_score.json", "w"), indent=1)
