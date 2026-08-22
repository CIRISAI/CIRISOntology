"""Worker harness: dispatch a design/critique prompt to DeepInfra families, log spend."""
import json,os,sys,time,urllib.request,threading
from concurrent.futures import ThreadPoolExecutor
KEY=open(os.path.expanduser('~/.deepinfra_key')).read().strip()
MODELS=["deepseek-ai/DeepSeek-V3.1","Qwen/Qwen3-235B-A22B-Instruct-2507","zai-org/GLM-4.5"]
PRICE={"deepseek-ai/DeepSeek-V3.1":(0.27,1.00),
       "Qwen/Qwen3-235B-A22B-Instruct-2507":(0.13,0.60),
       "zai-org/GLM-4.5":(0.35,1.55)}
LEDGER=os.path.join(os.path.dirname(os.path.abspath(__file__)),'spend.jsonl')
_lock=threading.Lock()
def ask(model,prompt,max_tokens=2500,tag="?"):
    body=json.dumps({"model":model,"temperature":0.0,"max_tokens":max_tokens,
        "messages":[{"role":"user","content":prompt}]}).encode()
    for att in range(4):
        try:
            req=urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
                data=body,headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
            with urllib.request.urlopen(req,timeout=300) as r: d=json.loads(r.read())
            u=d.get("usage",{}); ti=u.get("prompt_tokens",0); to=u.get("completion_tokens",0)
            pi,po=PRICE.get(model,(0.3,1.0))
            with _lock:
                open(LEDGER,'a').write(json.dumps({"t":time.time(),"tag":tag,"model":model,
                    "in":ti,"out":to,"usd":ti*pi/1e6+to*po/1e6})+"\n")
            return d["choices"][0]["message"].get("content") or ""
        except Exception as e:
            if att==3: return f"__ERROR__ {e}"
            time.sleep(6*(att+1))
    return ""
def spend():
    if not os.path.exists(LEDGER): return 0.0,0,0
    tot=ti=to=0.0
    for l in open(LEDGER):
        try:
            r=json.loads(l); tot+=r["usd"]; ti+=r["in"]; to+=r["out"]
        except Exception: pass
    return tot,int(ti),int(to)
if __name__=="__main__":
    if sys.argv[1]=="spend":
        t,i,o=spend(); print(f"spend ${t:.4f}  in={i} out={o}")
    else:
        pf=sys.argv[1]; out=sys.argv[2]; tag=sys.argv[3] if len(sys.argv)>3 else "design"
        p=open(pf).read()
        res={}
        def one(m): res[m]=ask(m,p,tag=tag)
        with ThreadPoolExecutor(max_workers=3) as ex: list(ex.map(one,MODELS))
        json.dump(res,open(out,'w'),indent=1)
        t,i,o=spend(); print(f"wrote {out}; cumulative worker spend ${t:.4f}")
