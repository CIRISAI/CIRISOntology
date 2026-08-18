"""Wikipedia ecological stream, v2 — whole-paragraph items, not diff-fragment collages.

v1's defect: it stitched diff context+del vs context+ins into pseudo-sentences, which
garbles structure; a legibility gate kept 10/60 and even those were collages. v2 fetches
BOTH full revisions, cleans markup first, and keeps only edits where EXACTLY ONE
paragraph differs — the item is that paragraph before/after: a real document-local
change. Stream id `wiki2`. Seed pinned before any fetch.
"""
import json, re, sys, time, html, random
from eco_sample import fetch, R

SEED = 20260818 + 5
API = "https://en.wikipedia.org/w/api.php"

def clean(t):
    t = re.sub(r'<!--.*?-->', '', t, flags=re.S)
    for _ in range(3):
        t = re.sub(r'\{\{[^{}]*\}\}', '', t)
    t = re.sub(r'<ref[^>]*/>', '', t)
    t = re.sub(r'<ref[^>]*>.*?</ref>', '', t, flags=re.S)
    t = re.sub(r'\[\[(?:File|Image|Category)[^\]]*\]\]', '', t)
    t = re.sub(r'\[\[(?:[^|\]]*\|)?([^\]]*)\]\]', r'\1', t)
    t = re.sub(r'\[https?://\S+ ([^\]]*)\]', r'\1', t)
    t = re.sub(r'\[https?://\S+\]', '', t)
    t = re.sub(r"'{2,}", '', t)
    t = re.sub(r'<[^>]+>', ' ', t)
    t = html.unescape(t)
    return t

def paras(wikitext):
    out = []
    for p in re.split(r'\n\s*\n', wikitext):
        p = p.strip()
        if p.startswith(('=', '{|', '|', '*', '#', '{{', '[[File', '[[Category')): continue
        c = re.sub(r'\s+', ' ', clean(p)).strip()
        if len(c) < 120 or sum(ch.isalpha() for ch in c)/len(c) < 0.6: continue
        if '||' in c or '|-' in c or c.startswith('}}') or '{|' in c: continue
        out.append(c)
    return out

def rev_content(revid):
    d = json.loads(fetch(f"{API}?action=query&prop=revisions&revids={revid}"
                         "&rvprop=content&rvslots=main&format=json"))
    pages = d.get("query", {}).get("pages", {})
    for p in pages.values():
        for r in p.get("revisions", []):
            return r.get("slots", {}).get("main", {}).get("*", "")
    return ""

def wiki2(n=60):
    rng = random.Random(SEED)
    out, seen, tried = [], set(), 0
    while len(out) < n and tried < 500:
        d = json.loads(fetch(f"{API}?action=query&list=recentchanges&rcnamespace=0&rctype=edit"
                             "&rclimit=50&rcprop=ids|sizes&format=json"
                             f"&rcstart={int(time.time())-rng.randint(0,86400*30)}&rcdir=older"))
        for rc in d["query"]["recentchanges"]:
            if len(out) >= n or tried >= 500: break
            if rc["revid"] in seen: continue
            seen.add(rc["revid"])
            if not (3 <= abs(rc["newlen"]-rc["oldlen"]) <= 400): continue
            tried += 1
            try:
                old = paras(rev_content(rc["old_revid"])); time.sleep(0.4)
                new = paras(rev_content(rc["revid"])); time.sleep(0.4)
            except Exception: continue
            if len(old) != len(new): continue
            diff = [(a, b) for a, b in zip(old, new) if a != b]
            if len(diff) != 1: continue
            b, a = diff[0]
            if len(b) > 1500 or len(a) > 1500: continue
            out.append({"id": f"wiki2-{len(out):02d}", "stream": "wiki2",
                        "before": b, "after": a,
                        "variation_site": "the changed text within the paragraph"})
            print(f"[wiki2] {len(out)}/{n} (tried {tried})", flush=True)
        time.sleep(2)
    return out

if __name__ == "__main__":
    rows = wiki2()
    with open(f"{R}/eco_wiki2.jsonl", "w") as f:
        for r in rows:
            r["kind_target"] = "WILD"; r["ambiguous_with"] = None
            r["difficulty"] = "wild"; r["domain"] = "wiki2"
            f.write(json.dumps(r) + "\n")
    print(f"wiki2: {len(rows)} items")
