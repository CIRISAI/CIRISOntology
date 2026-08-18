"""OSM ecological stream, v2 — the reframe the v1 NO-FITs demanded.

v1's defect (recorded in ECOLOGICAL_RESULTS.md): `before` showed the tags AFTER the
edit and `after` was a placeholder, so there was no contrast to classify and the
panel correctly read NO FIT / Facts noise. v2 fetches each modified element's
PREVIOUS version, so both tag states are real and the item is a genuine
registry-entry change. New stream id `osm2`; the v1 rows stay in the record,
marked superseded, per rule 7.

Seed pinned before any fetch, same discipline as eco_sample.py.
"""
import json, re, sys, time, datetime as dt, random
from eco_sample import fetch, R

SEED = 20260818 + 4

def osm2(n=60):
    rng = random.Random(SEED)
    ids = []
    for off in (0, 3600*6, 3600*24, 3600*48, 3600*96):
        t1 = time.time() - off; t0 = t1 - 3600*6
        f = lambda t: dt.datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            d = fetch(f"https://api.openstreetmap.org/api/0.6/changesets?closed=true&time={f(t0)},{f(t1)}").decode()
            ids += re.findall(r'<changeset id="(\d+)"', d)
        except Exception: pass
    rng.shuffle(ids)
    out = []
    for cid in ids[:900]:
        if len(out) >= n: break
        try:
            x = fetch(f"https://api.openstreetmap.org/api/0.6/changeset/{cid}/download").decode()
            mods = re.findall(r'<modify>(.*?)</modify>', x, re.S)
            if len(mods) != 1: continue
            m = mods[0]
            el = re.search(r'<(node|way|relation) ([^>]+)>', m)
            if not el: continue
            typ = el.group(1)
            attrs = dict(re.findall(r'(\w+)="([^"]*)"', el.group(2)))
            eid, ver = attrs.get("id"), int(attrs.get("version", "1"))
            if not eid or ver < 2: continue
            new_tags = dict(re.findall(r'<tag k="([^"]+)" v="([^"]+)"', m))
            prev = fetch(f"https://api.openstreetmap.org/api/0.6/{typ}/{eid}/{ver-1}").decode()
            old_tags = dict(re.findall(r'<tag k="([^"]+)" v="([^"]+)"', prev))
            if not old_tags and not new_tags: continue
            if old_tags == new_tags: continue          # geometry-only edit: no tag contrast to show
            fmt = lambda t: "; ".join(f"{k}={v}" for k, v in sorted(t.items())[:12]) or "(no tags)"
            out.append({"id": f"osm2-{len(out):02d}", "stream": "osm2",
                "before": f"[Map registry entry — a {typ}, its tags:] {fmt(old_tags)}",
                "after":  f"[The same {typ} after one edit, its tags:] {fmt(new_tags)}",
                "variation_site": "the tag(s) that differ between the two lists"})
            time.sleep(0.5)
        except Exception: continue
    return out

if __name__ == "__main__":
    rows = osm2()
    with open(f"{R}/eco_osm2.jsonl", "w") as f:
        for r in rows:
            r["kind_target"] = "WILD"; r["ambiguous_with"] = None
            r["difficulty"] = "wild"; r["domain"] = r["stream"]
            f.write(json.dumps(r) + "\n")
    print(f"osm2: {len(rows)} items")
