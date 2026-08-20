"""Stack Exchange ecological stream — the FORWARD stake's never-sampled stream.

Per GROSS4_FORWARD_PREREG.md (frozen 2026-08-19): api.stackexchange.com/2.3, sites
superuser + english + diy, recent edited posts (sort=activity), single-revision body
diffs (revision.body vs revision.last_body), the mechanical one-clean-paragraph gate
EXACTLY as eco_sample_wiki2.py, provenance stripped, target n=60, VOID below 45.

Gate translation, wikitext -> HTML (mechanical, thresholds unchanged):
  wiki2 dropped structural lines (=heading, {|table, |row, *bullet, #list, {{template,
  [[File, [[Category) from the paragraph list and kept prose only. Here the same drop is
  <pre>/<code-block>, <blockquote>, <ul>, <ol>, <table>, <h1..h6>, <hr>, <img>; prose is
  the <p> blocks. Legibility thresholds IDENTICAL: cleaned length >= 120, alphabetic
  fraction >= 0.6, differing pair capped at 1500 chars. Candidate size window IDENTICAL:
  3 <= |len(body) - len(last_body)| <= 400. Exactly one cleaned paragraph must differ and
  the paragraph counts must match.

Stream id `stackex`. Seed pinned before any fetch. Resumable: items are appended to the
output jsonl as they are accepted, and the funnel counters are written beside them.
"""
import gzip, html, json, os, random, re, sys, time, urllib.parse, urllib.request

SEED = 20260819
R = "/home/emoore/CIRISOntology/scratchpad/plane_corpus"
OUT = f"{R}/eco_stackex.jsonl"
STATS = f"{R}/eco_stackex_funnel.json"
API = "https://api.stackexchange.com/2.3"
SITES = ["superuser", "english", "diy"]
TARGET = 60
UA = ("CIRISOntology-eco-sampler/0.3 (https://github.com/CIRISAI/CIRISOntology; "
      "research corpus sampling)")
REQ_BUDGET = 260          # daily unauthenticated quota is 300; leave headroom
BATCH = 20                # post ids per /posts/{ids}/revisions call
PAGES_PER_SITE = 8        # /posts pages available to the seeded page order

_state = {"requests": 0, "quota": None}


def get(url):
    """One API call, gzip-aware, honouring backoff and the request budget."""
    if _state["requests"] >= REQ_BUDGET:
        raise RuntimeError("request budget exhausted")
    for attempt in range(4):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA,
                                                       "Accept-Encoding": "gzip"})
            with urllib.request.urlopen(req, timeout=90) as r:
                raw = r.read()
                if r.headers.get("Content-Encoding") == "gzip":
                    raw = gzip.decompress(raw)
            d = json.loads(raw)
            _state["requests"] += 1
            _state["quota"] = d.get("quota_remaining", _state["quota"])
            if d.get("backoff"):
                time.sleep(float(d["backoff"]) + 1)
            return d
        except urllib.error.HTTPError as e:
            _state["requests"] += 1
            if e.code in (429, 502, 503):
                time.sleep(20 * (attempt + 1))
                continue
            raise
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * (attempt + 1))
    raise RuntimeError("unreachable")


def make_filter():
    inc = ";".join(["revision.body", "revision.last_body", "revision.revision_type",
                    "revision.post_id", "revision.revision_number", "revision.post_type",
                    "post.post_id", "post.last_edit_date", "post.post_type"])
    d = get(f"{API}/filters/create?base=default&unsafe=false&include="
            + urllib.parse.quote(inc, safe=";"))
    return d["items"][0]["filter"]


# --- the one-clean-paragraph gate, thresholds exactly as eco_sample_wiki2.py ---

_BLOCKS = re.compile(r'<(pre|blockquote|ul|ol|table|h[1-6])\b[^>]*>.*?</\1\s*>',
                     re.S | re.I)


def paras(body_html):
    t = _BLOCKS.sub(' ', body_html or '')
    t = re.sub(r'<(hr|img)\b[^>]*/?>', ' ', t, flags=re.I)
    out = []
    for m in re.finditer(r'<p\b[^>]*>(.*?)</p\s*>', t, flags=re.S | re.I):
        c = re.sub(r'<br\s*/?>', ' ', m.group(1), flags=re.I)
        c = re.sub(r'<[^>]+>', ' ', c)
        c = html.unescape(c)
        c = re.sub(r'\s+', ' ', c).strip()
        if len(c) < 120 or sum(ch.isalpha() for ch in c) / len(c) < 0.6:
            continue
        out.append(c)
    return out


def last_body_edit(revs):
    """The post's most recent body-changing single-user revision."""
    cand = [r for r in revs
            if r.get("revision_type") == "single_user"
            and r.get("body") is not None and r.get("last_body") is not None
            and r["body"] != r["last_body"]]
    if not cand:
        return None
    return max(cand, key=lambda r: r.get("revision_number", 0))


def main():
    rng = random.Random(SEED)
    F = make_filter()
    funnel = {s: dict(posts_seen=0, edited=0, size_window=0, para_count_match=0,
                      exactly_one_diff=0, accepted=0) for s in SITES}

    out, seen_ids = [], set()
    if os.path.exists(OUT):                       # resume
        for line in open(OUT):
            if line.strip():
                out.append(json.loads(line))
        seen_ids = {r["post_key"] for r in out if "post_key" in r}
        print(f"[resume] {len(out)} items already on disk", flush=True)

    # seeded page order per site, then a round-robin batch queue so all three
    # sub-communities contribute (genre spread is the reason the prereg names three)
    pages = {s: rng.sample(range(1, PAGES_PER_SITE + 1), PAGES_PER_SITE) for s in SITES}
    pending = {s: [] for s in SITES}              # post ids awaiting a revisions call
    page_ix = {s: 0 for s in SITES}
    exhausted = {s: False for s in SITES}
    fh = open(OUT, "a")

    def refill(site):
        if exhausted[site] or page_ix[site] >= PAGES_PER_SITE:
            exhausted[site] = True
            return
        pg = pages[site][page_ix[site]]
        page_ix[site] += 1
        d = get(f"{API}/posts?order=desc&sort=activity&site={site}"
                f"&pagesize=100&page={pg}&filter={urllib.parse.quote(F)}")
        items = d.get("items", [])
        funnel[site]["posts_seen"] += len(items)
        fresh = [it["post_id"] for it in items
                 if it.get("last_edit_date") and it["post_id"] not in seen_ids]
        funnel[site]["edited"] += len(fresh)
        pending[site].extend(fresh)
        if not d.get("has_more"):
            exhausted[site] = True
        time.sleep(0.5)

    while len(out) < TARGET and _state["requests"] < REQ_BUDGET - 4:
        progressed = False
        for site in SITES:
            if len(out) >= TARGET or _state["requests"] >= REQ_BUDGET - 4:
                break
            if len(pending[site]) < BATCH and not exhausted[site]:
                refill(site)
            if not pending[site]:
                continue
            progressed = True
            batch, pending[site] = pending[site][:BATCH], pending[site][BATCH:]
            for pid in batch:
                seen_ids.add(pid)
            ids = ";".join(str(p) for p in batch)
            try:
                d = get(f"{API}/posts/{urllib.parse.quote(ids, safe=';')}/revisions"
                        f"?site={site}&pagesize=100&page=1&filter={urllib.parse.quote(F)}")
            except Exception as e:
                print(f"[{site}] revisions call failed: {e}", flush=True)
                continue
            by_post = {}
            for rv in d.get("items", []):
                by_post.setdefault(rv.get("post_id"), []).append(rv)
            for pid, revs in by_post.items():
                if len(out) >= TARGET:
                    break
                rv = last_body_edit(revs)
                if rv is None:
                    continue
                nb, ob = rv["body"], rv["last_body"]
                if not (3 <= abs(len(nb) - len(ob)) <= 400):
                    continue
                funnel[site]["size_window"] += 1
                old, new = paras(ob), paras(nb)
                if len(old) != len(new) or not old:
                    continue
                funnel[site]["para_count_match"] += 1
                diff = [(a, b) for a, b in zip(old, new) if a != b]
                if len(diff) != 1:
                    continue
                funnel[site]["exactly_one_diff"] += 1
                before, after = diff[0]
                if len(before) > 1500 or len(after) > 1500:
                    continue
                funnel[site]["accepted"] += 1
                rec = {"id": f"sx-{len(out):02d}", "stream": "stackex",
                       "before": before, "after": after,
                       "variation_site": "the changed text within the paragraph",
                       "kind_target": "WILD", "ambiguous_with": None,
                       "difficulty": "wild", "domain": "stackex",
                       "post_key": pid, "sub": site}
                out.append(rec)
                fh.write(json.dumps(rec) + "\n")
                fh.flush()
                print(f"[stackex] {len(out)}/{TARGET} ({site}) "
                      f"req={_state['requests']} quota={_state['quota']}", flush=True)
            json.dump({"funnel": funnel, "requests": _state["requests"],
                       "quota_remaining": _state["quota"], "n": len(out)},
                      open(STATS, "w"), indent=1)
            time.sleep(0.4)
        if not progressed and all(exhausted[s] and not pending[s] for s in SITES):
            print("[stackex] all sites exhausted", flush=True)
            break

    fh.close()
    json.dump({"funnel": funnel, "requests": _state["requests"],
               "quota_remaining": _state["quota"], "n": len(out)},
              open(STATS, "w"), indent=1)
    print(f"stackex: {len(out)} items, {_state['requests']} API requests, "
          f"quota_remaining={_state['quota']}")
    for s in SITES:
        print(f"  {s}: {funnel[s]}")


if __name__ == "__main__":
    main()
