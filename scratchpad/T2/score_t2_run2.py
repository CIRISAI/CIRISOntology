import json, re, collections
from items import ITEMS
MODELS = ["meta-llama/Llama-4-Scout-17B-16E-Instruct","openai/gpt-oss-120b","google/gemma-3-27b-it"]
PLAINSET = {"Priorities","Rules","Manner","Identity","Confidence","Facts","Circumstances",
            "Process","Model","Structure","Premises","Record","NO-FIT"}
raw = json.load(open('t2_raw_run2.json'))
def parse(txt):
    m = re.search(r'\{.*\}', txt, re.S)
    if not m: return None
    try: d = json.loads(m.group(0))
    except Exception:
        try: d = json.loads(m.group(0).replace("'",'"'))
        except Exception: return None
    k = str(d.get('kind','')).strip()
    if k not in PLAINSET: k = 'PARSE-FAIL:'+k
    so = str(d.get('survives_outside','')).strip().lower()
    so = 'yes' if so.startswith('y') else ('no' if so.startswith('n') else '?')
    return {'kind':k, 'second':d.get('second'), 'reason':str(d.get('reason',''))[:200], 'so':so}
table = {}
for iid in ITEMS:
    row = []
    for m in MODELS:
        e = raw.get(f"{iid}|{m}")
        row.append(parse(e['text']) if e else None)
    table[iid] = row
# determinacy per A2 MAJOR-3 counts
verdicts = {}
for iid,row in table.items():
    kinds = [r['kind'] if r else 'MISSING' for r in row]
    c = collections.Counter(kinds)
    top,n = c.most_common(1)[0]
    v = 'DETERMINATE' if n==3 else ('WEAK-2/3' if n==2 else 'SPLIT')
    so_yes = all(r and r['so']=='yes' for r in row)
    verdicts[iid] = {'kinds':kinds,'verdict':v,'modal':top,'record_analogue': so_yes}
# D over the nine dimensions, artifact-local determinate only
NINE = [k for k in ITEMS if k.startswith('dim_')]
D = sum(1 for k in NINE if verdicts[k]['verdict']=='DETERMINATE'
        and verdicts[k]['modal'] not in ('NO-FIT','Record') and not verdicts[k]['modal'].startswith('PARSE'))
# Fleiss kappa over all 17 items, categories = observed kinds
cats = sorted({k for v in verdicts.values() for k in v['kinds']})
N=len(verdicts); n=3; k=len(cats)
import math
Pbar=0; pj=collections.Counter()
for v in verdicts.values():
    c=collections.Counter(v['kinds'])
    Pbar += (sum(x*x for x in c.values())-n)/(n*(n-1))
    for kk,x in c.items(): pj[kk]+=x
Pbar/=N
Pe=sum((pj[c2]/(N*n))**2 for c2 in cats)
kappa=(Pbar-Pe)/(1-Pe) if Pe<1 else float('nan')
out={'verdicts':verdicts,'D':D,'kappa':round(kappa,4),
     'record_analogue_items':[k for k,v in verdicts.items() if v['record_analogue']],
     'determinate_nofit':[k for k,v in verdicts.items() if v['verdict']=='DETERMINATE' and v['modal']=='NO-FIT']}
json.dump(out, open('t2_scored_run2.json','w'), indent=1)
print(json.dumps({k:v for k,v in out.items() if k!='verdicts'}, indent=1))
for iid,v in verdicts.items():
    print(f"{iid:22} {v['verdict']:11} modal={v['modal']:13} kinds={v['kinds']} SO-unanimous-yes={v['record_analogue']}")
