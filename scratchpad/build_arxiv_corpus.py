"""UNIV-2 fresh substrate: arXiv v1->vN abstract revisions.
Genuinely unseen — no arXiv text or judgment appears in any prior sealed analysis.
Polite crawl: 1.1s between requests, identifying UA."""
import json, re, time, urllib.request, sys, difflib
UA={'User-Agent':'CIRISOntology-research/1.0 (academic change-taxonomy study)'}
def get(url):
    req=urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=60) as r: return r.read().decode('utf-8','replace')
def abstract(aid, v):
    h=get(f"https://arxiv.org/abs/{aid}v{v}")
    m=re.search(r'name="citation_abstract" content="(.*?)"', h, re.S)
    if not m: return None
    return re.sub(r'\s+',' ', m.group(1)).strip()
def listing(cat, start, n=100):
    u=(f"http://export.arxiv.org/api/query?search_query=cat:{cat}"
       f"&start={start}&max_results={n}&sortBy=submittedDate&sortOrder=descending")
    x=get(u)
    return re.findall(r'<id>http://arxiv\.org/abs/([0-9.]+)v(\d+)</id>', x)
def changed_span(a,b):
    """the first substantive changed region, with a little context"""
    sm=difflib.SequenceMatcher(None, a.split(), b.split())
    for tag,i1,i2,j1,j2 in sm.get_opcodes():
        if tag!='equal' and (i2-i1)+(j2-j1) >= 3:
            pa=' '.join(a.split()[max(0,i1-12):i2+12]); pb=' '.join(b.split()[max(0,j1-12):j2+12])
            return pa,pb
    return None
CATS=['cs.SE','q-bio.PE','econ.GN','stat.AP','physics.soc-ph','math.HO']
out=[]; seen=set(); target=int(sys.argv[1]) if len(sys.argv)>1 else 260
for cat in CATS:
    for start in (0,100,200,300):
        if len(out)>=target: break
        try: ids=listing(cat,start)
        except Exception as e: print('listing fail',cat,e,flush=True); continue
        time.sleep(1.1)
        for aid,ver in ids:
            if len(out)>=target: break
            if int(ver)<2 or aid in seen: continue
            seen.add(aid)
            try:
                a1=abstract(aid,1); time.sleep(1.1)
                a2=abstract(aid,int(ver)); time.sleep(1.1)
            except Exception: continue
            if not a1 or not a2 or a1==a2: continue
            sp=changed_span(a1,a2)
            if not sp: continue
            pa,pb=sp
            if len(pa)<40 or len(pb)<40: continue
            out.append({"id":f"arx-{len(out):04d}","stream":"arxiv_abstract_revision",
                        "before":pa,"after":pb,
                        "variation_site":"the changed text within the shown passage",
                        "kind_target":"WILD","ambiguous_with":None,"difficulty":"wild",
                        "domain":"arxiv","source_id":f"{aid} v1->v{ver}"})
            if len(out)%20==0: print(f"  collected {len(out)}",flush=True)
with open('plane_corpus/arxiv_rev.jsonl','w') as f:
    for r in out: f.write(json.dumps(r)+"\n")
print("WROTE", len(out), "items to plane_corpus/arxiv_rev.jsonl")
