"""Part-D (wild-discovered boundaries, authored) + eco v2 streams (wiki2, osm2) analysis.
Same conventions as the PLANE/ECOLOGICAL analyses: BASE modal vs target for boundaries;
NO-FIT rates and label spread for wild streams; disagreement pairs for T3."""
import json, collections, itertools, sys

R = "plane_corpus"
PLAIN = {"axiotic":"Priorities","deontic":"Rules","pragmatic":"Manner","ontological":"Identity",
 "epistemic":"Confidence","empirical":"Facts","contingent":"Circumstances","procedural":"Process",
 "nomological":"Model","structural":"Structure","axiomatic":"Premises","testimonial":"Record"}

def load(p):
    return [json.loads(l) for l in open(p)]

# ---- part D ----
pj = load(f"{R}/partd_judgments.jsonl")
corpus = {r["id"]: r for r in load(f"{R}/part_d.jsonl")}
base = collections.defaultdict(list)
allc = collections.defaultdict(lambda: collections.defaultdict(list))
for r in pj:
    if not r.get("kind"): continue
    allc[r["id"]][r["condition"]].append(r["kind"])
    if r["condition"] == "BASE": base[r["id"]].append(r["kind"])
print("== PART D — the wild-discovered boundaries, authored and measured ==")
hits = 0
for iid in sorted(base):
    t = PLAIN[corpus[iid]["kind_target"]]
    votes = collections.Counter(base[iid])
    m, _ = votes.most_common(1)[0]
    ok = m == t
    hits += ok
    print(f"  {iid:26s} target={t:9s} modal={m:9s} votes={dict(votes)} {'OK' if ok else '<-- MISS (amb: '+PLAIN[corpus[iid]['ambiguous_with']]+')'}")
print(f"  BASE modal accuracy: {hits}/{len(base)}")
# mobility count across all conditions (flip = any condition's modal differs from BASE modal)
flips = 0
for iid, conds in allc.items():
    bm = collections.Counter(conds.get("BASE", ["?"])).most_common(1)[0][0]
    for c, ks in conds.items():
        if c == "BASE": continue
        if collections.Counter(ks).most_common(1)[0][0] != bm:
            flips += 1
print(f"  condition flips (modal vs BASE, {len(allc)} items x 6 conds): {flips}")

# ---- eco v2 ----
print("\n== ECO v2 streams ==")
ej = [r for r in load(f"{R}/eco2_judgments.jsonl")] if __import__('os').path.exists(f"{R}/eco2_judgments.jsonl") else []
try: ej += load(f"{R}/eco2_wiki_judgments.jsonl")
except FileNotFoundError: pass
byitem = collections.defaultdict(list)
for r in ej:
    if r.get("kind"): byitem[r["id"]].append(r["kind"])
for stream in ("osm2", "wiki2"):
    items = {k: v for k, v in byitem.items() if k.startswith(stream)}
    if not items: continue
    modal = {k: collections.Counter(v).most_common(1)[0][0] for k, v in items.items()}
    dist = collections.Counter(modal.values())
    nofit_modal = sum(1 for v in modal.values() if v.upper().startswith("NO"))
    nofit_any = sum(1 for v in items.values() if any(x.upper().startswith("NO") for x in v))
    print(f"  {stream}: n={len(items)} modal-dist={dict(dist.most_common())}")
    print(f"    modal NO-FIT: {nofit_modal}  any-vote NO-FIT: {nofit_any}")
    pairs = collections.Counter()
    for v in items.values():
        u = sorted(set(v))
        for a, b in itertools.combinations(u, 2): pairs[(a, b)] += 1
    print(f"    top disagreement pairs: {pairs.most_common(5)}")
