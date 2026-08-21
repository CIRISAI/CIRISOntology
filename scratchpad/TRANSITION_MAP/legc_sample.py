"""LEG C chain sampler — per TRANSITION_MAP_PREREG.md (frozen 2026-08-21).

Same API, sites, UA, budget discipline and prose-cleaning as eco_sample_stackex.py
(the gross-four stream's frozen recipe). DIFFERENCE, recorded: chains not single edits —
posts with >= 3 single-user body revisions; each successive pair is one change-item.
The one-clean-paragraph acceptance gate is NOT applied per link (it would empty chains);
cleaning and caps are identical, links whose cleaned prose is identical are dropped and
counted. Seed 20260821. Target 100 chains; stop at request budget.
"""
import gzip, html, json, os, random, re, sys, time, urllib.parse, urllib.request

SEED = 20260821
OUT = "/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/legc_chains.jsonl"
STATS = "/home/emoore/CIRISOntology/scratchpad/TRANSITION_MAP/legc_funnel.json"
API = "https://api.stackexchange.com/2.3"
SITES = ["superuser", "english", "diy"]
TARGET = 100
UA = ("CIRISOntology-legc-sampler/0.1 (https://github.com/CIRISAI/CIRISOntology; "
      "research corpus sampling)")
REQ_BUDGET = 250
BATCH = 20
PAGES_PER_SITE = 10
_state = {"requests": 0}

def get(url):
    if _state["requests"] >= REQ_BUDGET: raise RuntimeError("budget")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA, "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=90) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip": raw = gzip.decompress(raw)
            d = json.loads(raw); _state["requests"] += 1
            if d.get("backoff"): time.sleep(float(d["backoff"]) + 1)
            return d
        except urllib.error.HTTPError as e:
            _state["requests"] += 1
            if e.code in (429, 502, 503): time.sleep(20*(attempt+1)); continue
            raise
        except Exception:
            if attempt == 3: raise
            time.sleep(5*(attempt+1))

_BLOCKS = re.compile(r'<(pre|blockquote|ul|ol|table|h[1-6])\b[^>]*>.*?</\1\s*>', re.S|re.I)
def clean(body_html):
    t = _BLOCKS.sub(' ', body_html or '')
    t = re.sub(r'<(hr|img)\b[^>]*/?>', ' ', t, flags=re.I)
    ps=[]
    for m in re.finditer(r'<p\b[^>]*>(.*?)</p\s*>', t, flags=re.S|re.I):
        c = re.sub(r'<br\s*/?>', ' ', m.group(1), flags=re.I)
        c = re.sub(r'<[^>]+>', ' ', c); c = html.unescape(c)
        c = re.sub(r'\s+',' ',c).strip()
        if c: ps.append(c)
    return "\n\n".join(ps)

def main():
    rng = random.Random(SEED)
    inc = ";".join(["revision.body","revision.last_body","revision.revision_type",
                    "revision.post_id","revision.revision_number","post.post_id"])
    F = get(f"{API}/filters/create?base=default&unsafe=false&include="+urllib.parse.quote(inc,safe=";"))["items"][0]["filter"]
    chains=[]; seen=set()
    if os.path.exists(OUT):
        for l in open(OUT):
            if l.strip(): r=json.loads(l); chains.append(r); seen.add(r["post_key"])
    funnel=dict(posts=0, ge3=0, links=0, identical_dropped=0, chains=len(chains))
    fh=open(OUT,"a")
    pages={s: rng.sample(range(1,PAGES_PER_SITE+1),PAGES_PER_SITE) for s in SITES}
    for pi in range(PAGES_PER_SITE):
        for s in SITES:
            if len(chains)>=TARGET: break
            try:
                d=get(f"{API}/posts?site={s}&sort=activity&order=desc&pagesize=50&page={pages[s][pi]}&filter=default")
            except RuntimeError: break
            ids=[str(it["post_id"]) for it in d.get("items",[])]
            funnel["posts"]+=len(ids)
            for i in range(0,len(ids),BATCH):
                if len(chains)>=TARGET: break
                try:
                    rd=get(f"{API}/posts/{';'.join(ids[i:i+BATCH])}/revisions?site={s}&pagesize=100&filter={F}")
                except RuntimeError: break
                byp={}
                for rev in rd.get("items",[]):
                    if rev.get("revision_type")=="single_user" and rev.get("body") and rev.get("last_body"):
                        byp.setdefault(rev["post_id"],[]).append(rev)
                for pid,revs in byp.items():
                    key=f"{s}:{pid}"
                    if key in seen: continue
                    revs.sort(key=lambda r:r.get("revision_number",0))
                    if len(revs)<2: continue   # need >=2 body edits => >=3 states => >=1 transition
                    funnel["ge3"]+=1
                    links=[]
                    for rev in revs:
                        b,a=clean(rev["last_body"]),clean(rev["body"])
                        if b==a: funnel["identical_dropped"]+=1; continue
                        links.append({"rev":rev.get("revision_number"),"before":b[:1500],"after":a[:1500]})
                    if len(links)<2: continue
                    funnel["links"]+=len(links)
                    rec={"post_key":key,"site":s,"links":links}
                    chains.append(rec); seen.add(key)
                    fh.write(json.dumps(rec,ensure_ascii=False)+"\n"); fh.flush()
                    funnel["chains"]=len(chains)
            json.dump({**funnel,"requests":_state["requests"]},open(STATS,"w"),indent=1)
        if len(chains)>=TARGET: break
    json.dump({**funnel,"requests":_state["requests"]},open(STATS,"w"),indent=1)
    print("DONE", json.dumps(funnel), "requests", _state["requests"], flush=True)

if __name__=="__main__": main()
