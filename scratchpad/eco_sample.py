"""Ecological sampler — seed-pinned wild changes from four unrelated streams.
Per ECOLOGICAL_PREREG.md: 60/stream, single localized changes, provenance stripped.
Seeds pinned here before any fetch. Output: one jsonl per stream."""
import json, random, re, subprocess, sys, time, urllib.request, urllib.parse
SEED = 20260818
R = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"

def fetch(url, headers=None):
    req = urllib.request.Request(url, headers=headers or {"User-Agent":"CIRISOntology-eco-sampler/0.2 (https://github.com/CIRISAI/CIRISOntology; research corpus sampling)"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()

def wiki(n=60):
    """Random recent Wikipedia revision diffs, single-paragraph changes only."""
    rng = random.Random(SEED)
    out = []
    seen = set()
    while len(out) < n:
        d = json.loads(fetch("https://en.wikipedia.org/w/api.php?action=query&list=recentchanges"
            "&rcnamespace=0&rctype=edit&rclimit=50&rcprop=ids|sizes&format=json"
            f"&rcstart={int(time.time())-rng.randint(0,86400*30)}&rcdir=older"))
        for rc in d["query"]["recentchanges"]:
            if len(out) >= n: break
            key = rc["revid"]
            if key in seen or abs(rc["newlen"]-rc["oldlen"]) > 400 or abs(rc["newlen"]-rc["oldlen"]) < 3: continue
            seen.add(key)
            try:
                c = json.loads(fetch("https://en.wikipedia.org/w/api.php?action=compare"
                    f"&fromrev={rc['old_revid']}&torev={rc['revid']}&format=json&prop=diff"))
                html = c["compare"]["*"]
                dels = re.findall(r'<del[^>]*>(.*?)</del>', html, re.S)
                ins  = re.findall(r'<ins[^>]*>(.*?)</ins>', html, re.S)
                ctx  = re.findall(r'<td class="diff-context"[^>]*>(?:<div>)?(.*?)(?:</div>)?</td>', html, re.S)
                clean = lambda x: re.sub(r'<[^>]+>','',x).strip()
                if not (dels or ins): continue
                before_frag = " ".join(clean(x) for x in ctx[:2]) + " " + " ".join(clean(x) for x in dels)
                after_frag  = " ".join(clean(x) for x in ctx[:2]) + " " + " ".join(clean(x) for x in ins)
                if before_frag.strip()==after_frag.strip() or len(before_frag)>1500: continue
                out.append({"id": f"wiki-{len(out):02d}", "stream":"wikipedia",
                    "before": before_frag.strip(), "after": after_frag.strip(),
                    "variation_site": "the changed text within the shown passage"})
            except Exception: continue
        time.sleep(4)
        if len(seen)>600: break
    return out

def github(n=60):
    """Small single-hunk commits from popular repos via gh api."""
    rng = random.Random(SEED+1)
    repos = ["torvalds/linux","python/cpython","kubernetes/kubernetes","rust-lang/rust",
             "home-assistant/core","microsoft/vscode","godotengine/godot","ansible/ansible"]
    out=[]
    for repo in repos:
        if len(out)>=n: break
        try:
            commits=json.loads(subprocess.check_output(
                ["gh","api",f"repos/{repo}/commits?per_page=40"],text=True))
        except Exception: continue
        rng.shuffle(commits)
        for c in commits:
            if len(out)>=n: break
            try:
                full=json.loads(subprocess.check_output(
                    ["gh","api",f"repos/{repo}/commits/{c['sha']}"],text=True))
                fs=full.get("files",[])
                if len(fs)!=1: continue
                p=fs[0].get("patch","")
                hunks=p.count("@@")//2
                if hunks!=1 or len(p)>1200: continue
                lines=p.splitlines()
                before=[l[1:] for l in lines if not l.startswith("+")and not l.startswith("@@")]
                after=[l[1:] for l in lines if not l.startswith("-")and not l.startswith("@@")]
                out.append({"id":f"gh-{len(out):02d}","stream":"github",
                    "before":"\n".join(before)[:1400],"after":"\n".join(after)[:1400],
                    "variation_site":"the changed lines within the shown hunk"})
            except Exception: continue
    return out

def fedreg(n=60):
    """Federal Register rule documents: abstract of correcting/amending docs vs what they amend."""
    rng=random.Random(SEED+2); out=[]
    page=1
    while len(out)<n and page<12:
        d=json.loads(fetch("https://www.federalregister.gov/api/v1/documents.json?"
            "conditions%5Btype%5D%5B%5D=RULE&per_page=60&fields%5B%5D=abstract&fields%5B%5D=title"
            f"&fields%5B%5D=action&page={page}"))
        for doc in d.get("results",[]):
            if len(out)>=n: break
            ab=doc.get("abstract") or ""; ti=doc.get("title") or ""; ac=doc.get("action") or ""
            # amendment docs describe a change: use action+title as 'before-context' and abstract as the change description
            m=re.search(r'(amend|revis|correct|remov|add|updat|chang)\w*', ab, re.I)
            if not m or len(ab)<80 or len(ab)>1200: continue
            out.append({"id":f"fr-{len(out):02d}","stream":"fedreg",
                "before":f"[Regulation as it stood, per its title:] {ti}",
                "after":f"[The amending action:] {ac}. {ab}",
                "variation_site":"the amendment the abstract describes"})
        page+=1
    return out

def osm(n=60):
    """OSM changesets with comments: tag-level edits."""
    rng=random.Random(SEED+3); out=[]
    ids=[]
    for off in (0, 3600*6, 3600*24, 3600*48, 3600*96):
        t1=time.time()-off; t0=t1-3600*6
        import datetime as dt
        f=lambda t: dt.datetime.utcfromtimestamp(t).strftime('%Y-%m-%dT%H:%M:%SZ')
        try:
            d=fetch(f"https://api.openstreetmap.org/api/0.6/changesets?closed=true&time={f(t0)},{f(t1)}").decode()
            ids += re.findall(r'<changeset id="(\d+)"', d)
        except Exception: pass
    ids=ids[:600]
    for cid in ids:
        if len(out)>=n: break
        try:
            x=fetch(f"https://api.openstreetmap.org/api/0.6/changeset/{cid}/download").decode()
            mods=re.findall(r'<modify>(.*?)</modify>', x, re.S)
            if len(mods)!=1: continue
            m=mods[0]
            if len(m)>1200: continue
            tags=re.findall(r'<tag k="([^"]+)" v="([^"]+)"', m)
            if not tags: continue
            out.append({"id":f"osm-{len(out):02d}","stream":"osm",
                "before":f"[Map element before this edit; its tags after the edit read:] "+ "; ".join(f"{k}={v}" for k,v in tags[:12]),
                "after":"[The same element, carrying the shown tags, as modified by one changeset]",
                "variation_site":"the modified tags shown"})
        except Exception: continue
        time.sleep(0.3)
    return out

if __name__=="__main__":
    which=sys.argv[1]
    fn={"wiki":wiki,"github":github,"fedreg":fedreg,"osm":osm}[which]
    rows=fn()
    with open(f"{R}/eco_{which}.jsonl","w") as f:
        for r in rows:
            r["kind_target"]="WILD"; r["ambiguous_with"]=None; r["difficulty"]="wild"; r["domain"]=r["stream"]
            f.write(json.dumps(r)+"\n")
    print(f"{which}: {len(rows)} items")
