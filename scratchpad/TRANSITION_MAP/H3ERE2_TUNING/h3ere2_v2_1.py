"""H3ERE2 v2.1 — v2 with the Record-deletion repair (s2_a7) as the default stage 2.
Authorized under AMENDMENT T3. v2 (h3ere2_v2.py) is frozen and unchanged; the only difference
here is the default S2 variant a5 -> a7, which appends one clause to a5's Record sentence:
"but simply deleting or rewriting a passage is not, by itself, a Record change; score a removal
by what the removed content was about."
CALIBRATION ONLY.

Original v2 header follows.
H3ERE2 v2 — tuned pipeline under AMENDMENT T1 (calibration only).
v1 (h3ere2.py) is frozen and untouched. Adds: token/spend ledger, parameterized S1
variants, S1-only screening mode, GLM headroom, S2 boundary priors from measured confusion.
"""
import json, os, re, sys, time, urllib.request, threading
from concurrent.futures import ThreadPoolExecutor
KEY = open(os.path.expanduser('~/.deepinfra_key')).read().strip()
MODELS = ["deepseek-ai/DeepSeek-V3.1","Qwen/Qwen3-235B-A22B-Instruct-2507","zai-org/GLM-4.5"]
PRICE = {"deepseek-ai/DeepSeek-V3.1":(0.27,1.00),
         "Qwen/Qwen3-235B-A22B-Instruct-2507":(0.13,0.60),
         "zai-org/GLM-4.5":(0.35,1.55)}
SURFACE = ["Facts","Rules","Manner","Identity"]
DEEP = ["Priorities","Confidence","Circumstances","Process","Model","Structure","Premises"]
DEEP8 = DEEP + ["Record"]
ALL12 = SURFACE + DEEP + ["Record"]
DISC = {"Priorities":"What becomes more important?","Rules":"What becomes allowed or required?",
 "Manner":"How is the same thing presented or used?","Identity":"What is this said to be?",
 "Confidence":"How sure are we, and on what standard?","Facts":"What claimed fact becomes wrong?",
 "Circumstances":"What just happens to differ here?","Process":"What steps or ordering change?",
 "Model":"What rule or model are we reasoning under?","Structure":"How are the pieces put together?",
 "Premises":"What are we taking as given?","Record":"Can the event still be established from what survives?"}
VERBLINE = ("attest (adds a claim), authorize (grants/denies standing), replace (substitutes content), "
 "withdraw (removes a prior contribution), recant (declares a prior contribution wrong), "
 "carries (a change of one kind arriving dressed as another)")
SURF_BLOCK = "\n".join(f"- {k}: {DISC[k]}" for k in SURFACE)
DEEP_BLOCK = "\n".join(f"- {k}: {DISC[k]}" for k in DEEP8)
ALL_BLOCK  = "\n".join(f"- {k}: {DISC[k]}" for k in ALL12)

LEDGER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'spend.jsonl')
_lock = threading.Lock()

def ask(model, prompt, max_tokens=None, tag="?"):
    mt = max_tokens or 1200
    payload = {"model":model,"temperature":0.0,"max_tokens":mt,
               "messages":[{"role":"user","content":prompt}]}
    # GLM-4.5 is a reasoning model: left on, it spends ~2,600 hidden tokens per call (10x the
    # cost of the other two families, 94s vs 3s, and it was the sole cause of every coverage
    # loss in the frozen run, which capped it at 2,500). Verified 2026-08-21 to return the
    # identical structural answer with thinking off.
    if "GLM" in model: payload["chat_template_kwargs"] = {"enable_thinking": False}
    body = json.dumps(payload).encode()
    for att in range(4):
        try:
            req = urllib.request.Request("https://api.deepinfra.com/v1/openai/chat/completions",
                data=body, headers={"Authorization":f"Bearer {KEY}","Content-Type":"application/json"})
            with urllib.request.urlopen(req, timeout=300) as r:
                d = json.loads(r.read())
            u = d.get("usage",{}); ti=u.get("prompt_tokens",0); to=u.get("completion_tokens",0)
            pi,po = PRICE.get(model,(0.3,1.0))
            with _lock:
                open(LEDGER,'a').write(json.dumps({"t":time.time(),"tag":tag,"model":model,
                    "in":ti,"out":to,"usd":ti*pi/1e6+to*po/1e6})+"\n")
            m = d["choices"][0]["message"]
            return m.get("content") or m.get("reasoning_content") or ""
        except Exception:
            time.sleep(6*(att+1))
    return ""

def pjson(t):
    if not t: return {}
    for pat in (r'\{[^{}]*\{.*?\}[^{}]*\}', r'\{.*\}'):
        m = re.search(pat, t, re.S)
        if m:
            try: return json.loads(m.group(0))
            except Exception: pass
    m = re.findall(r'\{.*?\}', t, re.S)
    for cand in reversed(m):
        try: return json.loads(cand)
        except Exception: pass
    return {}

def item_block(it):
    return f"BEFORE:\n---\n{it['before']}\n---\nAFTER:\n---\n{it['after']}\n---\nThe change is located here: {it['variation_site']}"

# ---------------- S1 variants ----------------
def s1_v0(it):   # frozen control (v1's prompt)
    return f"""You evaluate a change between two document versions. First decide whether it is one of the four SURFACE kinds, or something DEEPER.
SURFACE kinds: {'; '.join(f'{k}: {DISC[k]}' for k in SURFACE)}
If none of those four is clearly what changed, answer DEEPER.
Also name the grammar verb the change enacts: {VERBLINE}.
{item_block(it)}
Reply STRICT JSON: {{"answer": "<Facts|Rules|Manner|Identity|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0>, "rationale": "<one sentence>"}}"""

def s1_v1(it):   # forced comparison: name both families' best fit, then choose
    return f"""You triage a change between two document versions. Twelve kinds of change exist: four SURFACE kinds and eight DEEP kinds. Your job is to decide WHICH FAMILY the change belongs to. Do not force it into the surface family.

SURFACE FOUR
{SURF_BLOCK}

DEEP EIGHT
{DEEP_BLOCK}

Do all three steps, in order.
1. best_surface — the single best fit among the SURFACE FOUR, as if you had to pick one.
2. best_deep — the single best fit among the DEEP EIGHT, as if you had to pick one.
3. answer — which reading actually describes what changed. Deep kinds routinely ARRIVE DRESSED AS surface kinds: a changed assumption shows up as a burst of changed facts, a changed applied model shows up as changed derived values, a changed assembly shows up as changed presentation. If the deep reading is as good as or better than the surface reading, answer DEEPER. Answer with a surface kind only when nothing deeper is at stake.

Also name the grammar verb the change enacts: {VERBLINE}.
{item_block(it)}
Reply STRICT JSON only, no other text: {{"best_surface": "<Facts|Rules|Manner|Identity>", "best_deep": "<one of the eight deep kinds>", "answer": "<Facts|Rules|Manner|Identity|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0, how sure you are that ANSWER is right>, "rationale": "<one sentence>"}}"""

def s1_v2(it):   # deep kinds given positive content, single choice, tie-breaks DEEPER
    return f"""You triage a change between two document versions. Answer with one of the four SURFACE kinds only if that is the whole of what changed; otherwise answer DEEPER.

SURFACE FOUR
{SURF_BLOCK}

DEEPER means the change is really one of these eight:
{DEEP_BLOCK}

Deep kinds routinely ARRIVE DRESSED AS surface kinds — a changed assumption shows up as a burst of changed facts, a changed assembly shows up as changed presentation. When a surface reading and a deep reading fit equally well, answer DEEPER.

Also name the grammar verb the change enacts: {VERBLINE}.
{item_block(it)}
Reply STRICT JSON only, no other text: {{"answer": "<Facts|Rules|Manner|Identity|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0>, "rationale": "<one sentence>"}}"""


def s1_v3(it):   # forced two-candidate + TERNARY sufficiency verdict (the real gate)
    return f"""You triage a change between two document versions. Twelve kinds of change exist: four SURFACE kinds and eight DEEP kinds.

SURFACE FOUR
{SURF_BLOCK}

DEEP EIGHT
{DEEP_BLOCK}

Do all four steps, in order.
1. best_surface — the single best fit among the SURFACE FOUR, as if you had to pick one.
2. best_deep — the single best fit among the DEEP EIGHT, as if you had to pick one.
3. verdict — one of exactly three words:
   SURFACE_ONLY : the surface reading is the WHOLE of what changed; the deep reading adds nothing.
   CLOSE        : both readings fit; you cannot separate them from this text alone.
   DEEPER       : the deep reading is what actually changed.
   Deep kinds routinely ARRIVE DRESSED AS surface kinds. A change that merely alters which
   particular values, names, dates, environments or circumstances happen to hold here is NOT
   a Facts change; a changed assumption shows up as a burst of changed facts; a changed applied
   model shows up as changed derived values; a changed assembly shows up as changed presentation;
   a changed evidential standard shows up as a changed requirement. Say SURFACE_ONLY only when
   you would defend it against someone arguing for best_deep.
4. verb — the grammar verb the change enacts: {VERBLINE}.

{item_block(it)}
Reply STRICT JSON only, no other text: {{"best_surface": "<Facts|Rules|Manner|Identity>", "best_deep": "<one of the eight deep kinds>", "verdict": "<SURFACE_ONLY|CLOSE|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0>, "rationale": "<one sentence>"}}"""

S2_TESTS = """Apply these tests. Each is keyed to how the surface reading can be a disguise.
- Reads like Facts? Ask: is the changed item a FOUNDATIONAL ASSUMPTION that other statements rest on, stated without proof? -> Premises.
- Reads like Facts? Ask: does the change only alter WHICH PARTICULAR case, value, name, date, site or environment happens to hold here, leaving every claim and rule intact? -> Circumstances.
- Reads like Facts? Ask: is a FRAMEWORK APPLIED to derive the values what changed, rather than the values themselves? -> Model.
- Reads like Rules? Ask: does the change alter how SURE we must be, or what EVIDENCE is required, rather than what is permitted or demanded? -> Confidence.
- Reads like Rules? Ask: is the changed clause something the document TAKES AS GIVEN rather than something it imposes? -> Premises.
- Reads like Manner? Ask: is the ARRANGEMENT of parts, their nesting, grouping or dependencies what changed, rather than the wording or presentation? -> Structure.
- Reads like Manner? Ask: is the reasoning FRAMEWORK what changed? -> Model.
- Any surface reading? Ask: does the change affect whether a past event can still be ESTABLISHED from what survives (identifiers, logs, attributions, retention)? -> Record.
PROTECT the strong readings: Process, Rules, Facts, Manner, Identity and Priorities are usually
exactly what they look like. CONFIRM the surface reading unless one of the tests above clearly fires."""

def s2_a2(it, s1out, guidance=None):   # tuned carries-inversion
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to un-dress it.

The twelve kinds:
{ALL_BLOCK}

{S2_TESTS}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""


# --- frame inherited verbatim from the LICENSED single-pass instrument (panel2_annotate BASE) ---
FRAME = """Context for judgment:
- Retention: Assume every related record, log, and document survives and is available for consultation (full retention).
- Comparison: Assume the comparison holds everything else fixed: any element not named in the change description was identical between versions and is intended to stay identical."""

SHARP = """Four tests that decide the hardest boundaries. Apply them before answering.
- Facts vs Circumstances: Facts means a CLAIM that was true becomes wrong (or wrong becomes true). If the changed element is an INTERCHANGEABLE INSTANCE — a particular value, name, host, room, path, identifier, example or date that merely happens to hold here, where any other value would have served equally and nothing asserted becomes wrong — it is Circumstances, not Facts.
- Facts vs Premises: if the changed statement is something the document TAKES AS GIVEN and other statements rest on, rather than a claim the document is making, it is Premises.
- Facts vs Model: if what changed is a FRAMEWORK APPLIED to derive the values, rather than the values themselves, it is Model.
- Manner vs Structure: if the ARRANGEMENT of the parts — their nesting, grouping, ordering as an assembly, or dependencies — is what changed, rather than wording or presentation, it is Structure."""

def s1_v4(it):   # v3 + inherited frame + the four sharp boundary tests
    return f"""You triage a change between two document versions. Twelve kinds of change exist: four SURFACE kinds and eight DEEP kinds.

SURFACE FOUR
{SURF_BLOCK}

DEEP EIGHT
{DEEP_BLOCK}

{SHARP}

{FRAME}

Do all four steps, in order.
1. best_surface — the single best fit among the SURFACE FOUR, as if you had to pick one.
2. best_deep — the single best fit among the DEEP EIGHT, as if you had to pick one.
3. verdict — one of exactly three words:
   SURFACE_ONLY : the surface reading is the WHOLE of what changed; the deep reading adds nothing.
   CLOSE        : both readings fit; you cannot separate them from this text alone.
   DEEPER       : the deep reading is what actually changed.
   Deep kinds routinely ARRIVE DRESSED AS surface kinds. Say SURFACE_ONLY only when you would
   defend it against someone arguing for best_deep, and only when no test above fires.
4. verb — the grammar verb the change enacts: {VERBLINE}.

{item_block(it)}
Reply STRICT JSON only, no other text: {{"best_surface": "<Facts|Rules|Manner|Identity>", "best_deep": "<one of the eight deep kinds>", "verdict": "<SURFACE_ONLY|CLOSE|DEEPER>", "verb": "<one verb>", "confidence": <0.0-1.0>, "rationale": "<one sentence>"}}"""

def s2_a3(it, s1out, guidance=None):   # a2 + inherited frame + sharp tests
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to un-dress it.

The twelve kinds:
{ALL_BLOCK}

{SHARP}

Also: if the change alters how SURE we must be or what EVIDENCE is required, rather than what is
permitted or demanded, it is Confidence, not Rules. If it affects whether a past event can still be
ESTABLISHED from what survives (identifiers, logs, attributions, retention), it is Record.
PROTECT the strong readings: Process, Rules, Manner, Identity and Priorities are usually exactly what
they look like. Confirm the surface reading unless a test above clearly fires.

{FRAME}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""

S1S = {"v0":s1_v0, "v1":s1_v1, "v2":s1_v2, "v3":s1_v3, "v4":s1_v4}

def gate(o1, variant, thresh=0.7, use_carries=True):
    """returns (fast_exit, surface_label, reason)"""
    if variant in ("v3","v4"):
        v = str(o1.get("verdict","")).strip().upper()
        bs = str(o1.get("best_surface","")).strip()
        if v=="SURFACE_ONLY" and bs in SURFACE:
            # MEASURED (round 2, 3 families): the fast path is 0.889 precise when it clears a
            # Manner/Rules/Identity reading and 0.405 when it clears a Facts reading. Facts is
            # the surface that Circumstances, Premises and Model all wear, so triage is not
            # competent to clear it; only S2 is. NO_FAST_ON_FACTS=0 restores the old behaviour.
            if bs=="Facts" and os.environ.get("NO_FAST_ON_FACTS","1")=="1":
                return False, bs, "facts-never-fast"
            return True, bs, "fast"
        return False, (bs if bs in SURFACE else None), ("verdict-"+v.lower() if v else "parsefail")
    a = str(o1.get("answer", o1.get("surface",""))).strip()
    try: c = float(o1.get("confidence", 0))
    except Exception: c = 0.0
    if a not in SURFACE: return False, (a if a in SURFACE else None), "not-surface"
    if use_carries and str(o1.get("verb","")).strip().lower()=="carries":
        return False, a, "carries-verb"
    if variant=="v1":
        bd = str(o1.get("best_deep","")).strip()
        if bd in DEEP8 and c < thresh: return False, a, "lowconf"
    if c < thresh: return False, a, "lowconf"
    return True, a, "fast"

def run_s1_only(model, it, variant):
    o1 = pjson(ask(model, S1S[variant](it), tag=f"s1-{variant}"))
    fe, surf, why = gate(o1, variant)
    return {"id":it["id"],"model":model,"variant":variant,"s1":o1,"fast":fe,"surface":surf,"gate":why}

def main_s1(dataset, variant, outpath, models=None, limit=None):
    items=[json.loads(l) for l in open(dataset) if l.strip()]
    if limit: items=items[:limit]
    mods = models or MODELS
    done=set()
    if os.path.exists(outpath):
        for l in open(outpath):
            try: r=json.loads(l); done.add((r["id"],r["model"]))
            except Exception: pass
    todo=[(it,m) for it in items for m in mods if (it["id"],m) not in done]
    lk=threading.Lock(); fh=open(outpath,"a"); n=[0]
    def one(job):
        it,m=job; tr=run_s1_only(m,it,variant)
        with lk:
            fh.write(json.dumps(tr,ensure_ascii=False)+"\n"); fh.flush(); n[0]+=1
            if n[0]%50==0: print(f"{n[0]}/{len(todo)}",flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,todo))
    print(f"S1-{variant}-DONE {dataset} {n[0]}",flush=True)

def main_s2screen(dataset, s1file, outpath, models=None, limit=None):
    """Measure S2 alone: feed each item its recorded S1 output, score the 12-way answer."""
    items={json.loads(l)["id"]:json.loads(l) for l in open(dataset) if l.strip()}
    s1recs=[json.loads(l) for l in open(s1file) if l.strip()]
    if limit: s1recs=s1recs[:limit]
    mods=models or MODELS
    done=set()
    if os.path.exists(outpath):
        for l in open(outpath):
            try: r=json.loads(l); done.add((r["id"],r["model"]))
            except Exception: pass
    todo=[(r,m) for r in s1recs for m in mods if (r["id"],m) not in done]
    lk=threading.Lock(); fh=open(outpath,"a"); n=[0]
    def one(job):
        r,m=job; it=items[r["id"]]
        sv=os.environ.get("S2VAR","a3")
        fn = S2S[sv]
        o2=pjson(ask(m, fn(it, r.get("s1") or {}), tag="s2-"+sv))
        with lk:
            fh.write(json.dumps({"id":r["id"],"model":m,"s1":r.get("s1"),"s2":o2},ensure_ascii=False)+"\n")
            fh.flush(); n[0]+=1
            if n[0]%50==0: print(f"{n[0]}/{len(todo)}",flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,todo))
    print(f"S2SCREEN-DONE {n[0]}",flush=True)




PROTECT = """PROTECT the plain readings. Over-reading is exactly as wrong as under-reading.
- Identity: if what changed is what something IS SAID TO BE — its name, its type, its class, its
  category, its status, what it counts as — that is Identity. It does NOT become Model, Premises or
  Structure merely because a framework or an assumption could be imagined standing behind the
  renaming. Ask: did a thing get re-described as a different kind of thing? Then Identity.
- Facts: a claim that was true becoming wrong is Facts. The Circumstances test fires ONLY when the
  changed element is a stand-in whose particular value the document makes no claim about; if the
  document asserts something ABOUT that value, or the new value makes a statement wrong, it is Facts.
- Process, Rules, Manner and Priorities are usually exactly what they look like.
Confirm the plain reading unless a test above clearly fires."""

def s2_a4(it, s1out, guidance=None):   # a3 + Identity protection + tightened Circumstances test
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to decide
whether it is, and to un-dress it only when it actually is.

The twelve kinds:
{ALL_BLOCK}

{SHARP}

Also: if the change alters how SURE we must be or what EVIDENCE is required, rather than what is
permitted or demanded, it is Confidence, not Rules. If it affects whether a past event can still be
ESTABLISHED from what survives (identifiers, logs, attributions, retention), it is Record.

{PROTECT}

{FRAME}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""

def s3_v2(it, s1out, kind, rationale):
    """Two-sided conscience: it must be able to convict the DEEP reading, not only bless it."""
    bs = str((s1out or {}).get("best_surface","")) or "unclear"
    return f"""Conscience check on a classification.

A deeper evaluation claims this change is kind "{kind}" ({DISC.get(kind,'')}).
Its rationale: {rationale}
The first-pass surface reading was "{bs}" ({DISC.get(bs,'')}).

{FRAME}

{item_block(it)}

Two questions, both of which you must actually test:
1. Does the change really answer the question that "{kind}" asks?
2. Is the plainer reading "{bs}" in fact the whole of what changed here, so that calling it
   "{kind}" reads something into the text that is not there? Over-reading is as wrong as
   under-reading: a change that simply states a different thing IS Facts, a change that
   simply says what something IS is Identity, and neither becomes a framework change because
   a framework could be imagined behind it.

Reply PASS only if the "{kind}" reading survives both questions. Otherwise FAIL and say in one
sentence which reading it should be and why.
Reply STRICT JSON only, no other text: {{"verdict": "<PASS|FAIL>", "guidance": "<one sentence if FAIL, else null>"}}"""



# Round-2 tests. The "ripple" wording was rejected by adversarial critique (two families,
# independently): "every other statement keeps its wording while its meaning changes" is not
# CHECKABLE from a BEFORE/AFTER pair. Both proposed the same substitute, adopted here: a
# positional check on the declaration plus a textual check on the remainder.
DEEPTESTS = """Two further tests, for the two kinds that are hardest to see.
- Premises — THE DECLARED-BASIS TEST. Both halves must hold: (a) the changed element DECLARES a
  basis the rest of the artifact is read against — a unit system, an epoch or reference date, a
  coordinate frame, a counting convention, a starting state, a benchmark, what a term is taken to
  denote; and (b) the rest of the artifact is textually unchanged. Then it is Premises. Tie-breaks:
  if what changed is how a value is DERIVED or CALCULATED, it is Model, not Premises; if the changed
  element is an interchangeable instance that nothing else is read against, it is Circumstances; if a
  stated claim simply becomes wrong, it is Facts.
- Structure — THE ARRANGEMENT TEST. The same content is re-nested, re-scoped, re-attached, or its
  interface shape changes — a clause moves to where it governs something different, a condition
  becomes a precondition on a whole list, keys move under a new parent, a return shape or a parameter
  order changes — while the wording itself stays substantially intact. Tie-breaks: if only wording,
  tone or formatting changed and the arrangement is the same, it is Manner; if what changed is the
  ORDER OF STEPS TO BE PERFORMED, it is Process, not Structure."""

def s2_a5(it, s1out, guidance=None):   # a4 + the declared-basis and arrangement tests
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to decide
whether it is, and to un-dress it only when it actually is.

The twelve kinds:
{ALL_BLOCK}

{SHARP}

{DEEPTESTS}

Also: if the change alters how SURE we must be or what EVIDENCE is required, rather than what is
permitted or demanded, it is Confidence, not Rules. If it affects whether a past event can still be
ESTABLISHED from what survives (identifiers, logs, attributions, retention), it is Record.

{PROTECT}

{FRAME}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""


# Round-4 repair. MEASURED defect: on wild the candidate assigned Record to 9.0% of traces
# (baseline 2.0%), and 52% of those were deletions — the Record test fired on any removal of
# text. Record is a claim about whether an EVENT can still be established, not about whether a
# document still contains a paragraph, and the prompt's own frame stipulates full retention.
RECORD_TEST = """Record, and what it is NOT. Record asks whether a past EVENT can still be
established from what survives: retention rules, identifiers that tie an entry to its occasion,
attributions, audit trails, the register an entry lives in. **Removing or rewriting content is
NOT by itself a Record change.** Under the full-retention frame stated below the sibling records
survive any edit, so deleting a passage changes what this document SAYS, not what can be proven
to have happened — score that as whatever the removed content was about. Ask whether the change
removes the MEANS of establishing that something occurred, not whether it removes text."""

def s2_a6(it, s1out, guidance=None):   # a5 with the Record test repaired
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to decide
whether it is, and to un-dress it only when it actually is.

The twelve kinds:
{ALL_BLOCK}

{SHARP}

{DEEPTESTS}

{RECORD_TEST}

Also: if the change alters how SURE we must be or what EVIDENCE is required, rather than what is
permitted or demanded, it is Confidence, not Rules.

{PROTECT}

{FRAME}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""


def s2_a7(it, s1out, guidance=None):
    """a5 with a MINIMAL Record clause. a6 replaced the Record sentence with a paragraph and
    suppressed Record globally (curated Record 9/10 -> 6/10, Confidence 7/10 -> 5/10, S2 alone,
    DeepSeek). a7 keeps a5 verbatim and appends one clause to the existing Record sentence."""
    g = f"\nCONSCIENCE GUIDANCE from the prior attempt (address it): {guidance}\n" if guidance else ""
    return f"""A first-pass evaluation of this change produced: {json.dumps(s1out)}
The surface reading may be a deeper kind ARRIVING DRESSED as a surface kind. Your job is to decide
whether it is, and to un-dress it only when it actually is.

The twelve kinds:
{ALL_BLOCK}

{SHARP}

{DEEPTESTS}

Also: if the change alters how SURE we must be or what EVIDENCE is required, rather than what is
permitted or demanded, it is Confidence, not Rules. If it affects whether a past event can still be
ESTABLISHED from what survives (identifiers, logs, attributions, retention), it is Record — but
simply deleting or rewriting a passage is not, by itself, a Record change; score a removal by what
the removed content was about.

{PROTECT}

{FRAME}
{g}{item_block(it)}
Name the true kind and the verb ({VERBLINE}).
Reply STRICT JSON only, no other text: {{"kind": "<one of the twelve>", "verb": "<one verb>", "rationale": "<one sentence>"}}"""

S2S = {"a2":s2_a2,"a3":s2_a3,"a4":s2_a4,"a5":s2_a5,"a6":s2_a6,"a7":s2_a7}

def s3_v1(it, s1out, kind, rationale):
    """Frozen one-sided wording (measured FAIL rate 2/12) + the inherited frame."""
    bs = str((s1out or {}).get("best_surface","")) or "unclear"
    return f"""Conscience check. A deeper evaluation claims this change is really kind "{kind}" (question: {DISC.get(kind,'')}), presenting on the surface as "{bs}". Its rationale: {rationale}
{FRAME}
{item_block(it)}
Would a {kind} change genuinely wear this surface appearance here? Reply STRICT JSON: {{"verdict": "<PASS|FAIL>", "guidance": "<one sentence if FAIL, else null>"}}"""

def run_item_v2(model, it, s1var="v4", s2var="a7", thresh=0.7, s3var="v1", retry_rule="keepfirst"):
    tr={"id":it["id"],"model":model,"s1var":s1var,"s2var":s2var}
    o1=pjson(ask(model, S1S[s1var](it), tag="full-s1")); tr["s1"]=o1
    fe,surf,why=gate(o1,s1var,thresh)
    tr["gate"]=why
    if fe:
        tr["final"]=surf; tr["final_verb"]=o1.get("verb"); tr["route"]="fast"; return tr
    s2f = S2S[s2var]
    o2=pjson(s2raw(model,s2f,it,o1)); tr["s2"]=o2
    kind=str(o2.get("kind","")).strip()
    if kind not in ALL12:
        fb = str((o1 or {}).get("best_deep","")).strip()
        tr["final"]= fb if fb in ALL12 else (surf if surf in SURFACE else None)
        tr["route"]="s2-parsefail-fallback"; tr["final_verb"]=o1.get("verb"); return tr
    s3f = s3_v1 if s3var=="v1" else s3_v2
    o3=pjson(ask(model, s3f(it,o1,kind,str(o2.get("rationale",""))), tag="full-s3")); tr["s3"]=o3
    if str(o3.get("verdict","")).upper()=="PASS":
        tr["final"]=kind; tr["final_verb"]=o2.get("verb"); tr["route"]="recurse-pass"; return tr
    o2b=pjson(s2raw(model,s2f,it,o1,guidance=str(o3.get("guidance","")))); tr["s2_retry"]=o2b
    k2=str(o2b.get("kind","")).strip()
    o3b=pjson(ask(model, s3f(it,o1,k2 if k2 in ALL12 else kind, str(o2b.get("rationale",""))), tag="full-s3r"))
    tr["s3_retry"]=o3b
    retry_ok = str(o3b.get("verdict","")).upper()=="PASS" and k2 in ALL12
    # MEASURED (round 1): accepting an unverified retry damaged 29 items and improved 11.
    # Under T1 the frozen "second answer wins" rule is replaced by keep-first-unless-verified.
    if retry_rule=="keepfirst" and not retry_ok:
        tr["final"]=kind; tr["final_verb"]=o2.get("verb"); tr["route"]="recurse-retry-rejected"
    else:
        tr["final"]= k2 if k2 in ALL12 else kind
        tr["final_verb"]=o2b.get("verb") or o2.get("verb")
        tr["route"]="recurse-retry-"+("pass" if retry_ok else "unverified")
    return tr

def s2raw(model, fn, it, o1, guidance=None):
    return ask(model, fn(it,o1,guidance), tag="full-s2")

def main_full(dataset, outpath, s1var="v4", s2var="a7", models=None, limit=None, thresh=0.7, s3var="v1"):
    items=[json.loads(l) for l in open(dataset) if l.strip()]
    if limit: items=items[:limit]
    mods=models or MODELS
    done=set()
    if os.path.exists(outpath):
        for l in open(outpath):
            try: r=json.loads(l); done.add((r["id"],r["model"]))
            except Exception: pass
    todo=[(it,m) for it in items for m in mods if (it["id"],m) not in done]
    lk=threading.Lock(); fh=open(outpath,"a"); n=[0]
    def one(job):
        it,m=job; tr=run_item_v2(m,it,s1var,s2var,thresh,s3var)
        with lk:
            fh.write(json.dumps(tr,ensure_ascii=False)+"\n"); fh.flush(); n[0]+=1
            if n[0]%50==0: print(f"{n[0]}/{len(todo)}",flush=True)
    with ThreadPoolExecutor(max_workers=8) as ex: list(ex.map(one,todo))
    print(f"FULL-DONE {dataset} {s1var}/{s2var} {n[0]}",flush=True)


if __name__=="__main__":
    if sys.argv[1]=="full":
        main_full(sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5],
                models=(sys.argv[6].split(',') if len(sys.argv)>6 and sys.argv[6]!='-' else None),
                limit=(int(sys.argv[7]) if len(sys.argv)>7 else None))
    elif sys.argv[1]=="s2screen":
        main_s2screen(sys.argv[2], sys.argv[3], sys.argv[4],
                models=(sys.argv[5].split(',') if len(sys.argv)>5 and sys.argv[5]!='-' else None),
                limit=(int(sys.argv[6]) if len(sys.argv)>6 else None))
    elif sys.argv[1]=="s1":
        main_s1(sys.argv[2], sys.argv[3], sys.argv[4],
                models=(sys.argv[5].split(',') if len(sys.argv)>5 and sys.argv[5]!='-' else None),
                limit=(int(sys.argv[6]) if len(sys.argv)>6 else None))


