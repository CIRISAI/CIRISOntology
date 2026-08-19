"""Corpus loading, batch provenance, changed-span extraction. No embedding here."""
import json, difflib, os

PC = '/home/emoore/CIRISOntology/scratchpad/plane_corpus'

PLAIN = {'axiotic': 'Priorities', 'deontic': 'Rules', 'pragmatic': 'Manner',
         'ontological': 'Identity', 'epistemic': 'Confidence', 'empirical': 'Facts',
         'contingent': 'Circumstances', 'procedural': 'Process', 'nomological': 'Model',
         'structural': 'Structure', 'axiomatic': 'Premises', 'testimonial': 'Record'}
KINDS = ['axiotic', 'deontic', 'pragmatic', 'ontological', 'epistemic', 'empirical',
         'contingent', 'procedural', 'nomological', 'structural', 'axiomatic', 'testimonial']
KIDX = {k: i for i, k in enumerate(KINDS)}
RECORD = 'testimonial'


def _load(fn):
    return [json.loads(l) for l in open(os.path.join(PC, fn))]


def span_pair(before, after):
    """Mechanical difflib character-diff: (before-side changed text, after-side changed
    text, changed-span char count = sum of max(before-side, after-side) per opcode)."""
    sm = difflib.SequenceMatcher(None, before, after, autojunk=False)
    b, a, n = [], [], 0
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == 'equal':
            continue
        b.append(before[i1:i2])
        a.append(after[j1:j2])
        n += max(i2 - i1, j2 - j1)
    return ' '.join(x for x in b if x), ' '.join(x for x in a if x), n


def corpus_A():
    rows = _load('corpus_full.jsonl')
    part = {}
    for p in ['a', 'b', 'c']:
        for r in _load(f'part_{p}.jsonl'):
            part[r['id']] = p
    for r in rows:
        r['part'] = part[r['id']]
        r['span_before'], r['span_after'], r['span_chars'] = span_pair(r['before'], r['after'])
    return rows


def corpus_held():
    rows = _load('part_d.jsonl')
    for r in rows:
        r['span_before'], r['span_after'], r['span_chars'] = span_pair(r['before'], r['after'])
    return rows


def corpus_babel():
    rows = _load('babel_items.jsonl')
    for r in rows:
        r['span_before'], r['span_after'], r['span_chars'] = span_pair(r['before'], r['after'])
    return rows


def corpus_B():
    rows = []
    for fn in ['eco_corpus.jsonl', 'eco_osm2.jsonl', 'eco_wiki2.jsonl']:
        rows += _load(fn)
    for r in rows:
        r['span_before'], r['span_after'], r['span_chars'] = span_pair(r['before'], r['after'])
    return rows


STOPLIST = ['full retention', 'retention', 'retained', 'survives', 'surviving', 'survived',
            'survive', 'destroyed', 'siblings', 'sibling', 'consulted', 'consult',
            'minimal', 'partial', 'registers', 'register', 'logs', 'log', 'drafts',
            'draft', 'records', 'record']


def strip_stoplist(t):
    import re
    out = t
    for w in STOPLIST:
        out = re.sub(r'(?i)\b' + re.escape(w) + r'\b', ' ', out)
    return re.sub(r'\s+', ' ', out).strip()


def judgments():
    return _load('full_judgments.jsonl')


def ratchet_rationales():
    p = '/home/emoore/RATCHET/release/data_scrubbed_v1/accord_traces.jsonl'
    out = []
    with open(p) as f:
        for line in f:
            try:
                r = json.loads(line)
            except Exception:
                continue
            v = r.get('action_rationale')
            if isinstance(v, str) and v.strip():
                out.append(v)
    return out
