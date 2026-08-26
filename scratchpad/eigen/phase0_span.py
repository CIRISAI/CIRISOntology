"""Phase-0 mechanical span extraction and change-reading renderings.

NO authored field is ever read here (`variation_site`, `author_note`, `kind_target`,
`difficulty` are all untouched).  The only inputs are `before` and `after`.

Extraction: longest-common-prefix / longest-common-suffix decomposition (a single
contiguous changed region per side), then WIDENED to the full sentence(s) of each
version that the region overlaps.  Sentence boundaries are `.`/`!`/`?` followed by
whitespace-then-capital, plus hard newlines (the corpus has a title line).

This is deliberately different from v1's `corpora.span_pair`, which used difflib
character opcodes and produced shredded fragments ('arteria u schoo f n ag').
"""
import re

C1_TEMPLATE = 'A passage changed. Before: {b} After: {a}'
QWEN_PREFIX = ('Instruct: Identify what kind of commitment changed between the two '
               'versions.\nQuery: ')


def lcp_lcs(before, after):
    """(b_lo, b_hi, a_lo, a_hi): the single contiguous changed region on each side."""
    n = min(len(before), len(after))
    p = 0
    while p < n and before[p] == after[p]:
        p += 1
    s = 0
    while s < n - p and before[len(before) - 1 - s] == after[len(after) - 1 - s]:
        s += 1
    return p, len(before) - s, p, len(after) - s


def sentence_spans(text):
    """[(start, end)] covering the non-blank content of `text`."""
    spans, start, i, n = [], 0, 0, len(text)
    while i < n:
        c = text[i]
        if c == '\n':
            if text[start:i].strip():
                spans.append((start, i))
            j = i
            while j < n and text[j] in '\n\r \t':
                j += 1
            start = i = j
            continue
        if c in '.!?':
            j = i + 1
            while j < n and text[j] in ' \t':
                j += 1
            if j >= n or text[j] == '\n' or text[j].isupper() or text[j] in '"“(':
                if text[start:i + 1].strip():
                    spans.append((start, i + 1))
                start = i = j
                continue
        i += 1
    if text[start:n].strip():
        spans.append((start, n))
    return spans


def widen(text, lo, hi):
    """The concatenated sentence(s) of `text` overlapping [lo, hi)."""
    sp = sentence_spans(text)
    if not sp:
        return text.strip()
    hit = [(a, b) for a, b in sp if a < max(hi, lo + 1) and b > lo]
    if not hit:
        # insertion/deletion landing exactly on a boundary: take the nearest sentence
        hit = [min(sp, key=lambda ab: min(abs(ab[0] - lo), abs(ab[1] - lo)))]
    return ' '.join(text[a:b].strip() for a, b in hit)


def context_pair(before, after):
    """(sentence_before, sentence_after, changed_chars) — mechanical, no authored fields."""
    blo, bhi, alo, ahi = lcp_lcs(before, after)
    return (widen(before, blo, bhi), widen(after, alo, ahi),
            max(bhi - blo, ahi - alo))


def attach(rows):
    """Add ctx_before / ctx_after / ctx_chars to every row, in place."""
    for r in rows:
        cb, ca, n = context_pair(r['before'], r['after'])
        r['ctx_before'], r['ctx_after'], r['ctx_chars'] = cb, ca, n
    return rows


def c1_text(cb, ca):
    return C1_TEMPLATE.format(b=cb, a=ca)


def qwen(t):
    return QWEN_PREFIX + t
