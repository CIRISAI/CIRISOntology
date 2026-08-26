#!/usr/bin/env python3
"""Prereg audit — refuse a freeze the way the axiom audit refuses a sorry.

Usage: prereg_audit.py <PREREG.md> [...]
Checks (per PREREG_STANDARD.md):
  1. every `witness:` Lean name resolves in CIRISOntology/ (or is `none`)
  2. a `defects:` line exists; every cited id exists in DEFECTS_REGISTRY.md;
     registry keyword contact without citation is refused
  3. gauge evidence: a `gauge:` line naming files that exist, whose logs contain
     both a pass and a fired/violation demonstration
  4. numeric bands: every staked arm row contains a digit-bearing band
  5. a family-wise line (Bonferroni/FDR/percentile-with-count)
Exit 0 = freeze admissible; nonzero = refused, reasons printed.
"""
import re, sys, pathlib
ROOT = pathlib.Path(__file__).resolve().parent.parent
REG = (ROOT / "DEFECTS_REGISTRY.md").read_text()
REG_IDS = set(re.findall(r"\*\*(D-[A-Z-]+)\*\*", REG))
# keyword -> registry id contact map (grepped against the prereg text)
CONTACT = {"certify_at": "D-IDENT", "node index": "D-IDENT", "twin": "D-IDENT",
           "prior epoch": "D-EPOCH", "pilot epoch": "D-EPOCH",
           "ideal unitary": "D-GATE", "deterministic": "D-DET",
           "tau_c": "D-RULER-TAU", "first CI touching": "D-RULER-TAU",
           "Dobrushin": "D-BOUND-DOB", "alpha": "D-BOUND-DOB",
           "end-bit": "D-EXOG", "success rate": "D-SATUR", "survival": "D-SATUR"}

def lean_resolves(name):
    if name == "none": return True
    for f in (ROOT / "CIRISOntology").rglob("*.lean"):
        if re.search(rf"(theorem|lemma|def|abbrev|structure)\s+{re.escape(name)}\b", f.read_text()):
            return True
    return False

def audit(path):
    t = pathlib.Path(path).read_text()
    errs = []
    wits = re.findall(r"witness:\s*`?([A-Za-z0-9_.]+)`?", t)
    if not wits: errs.append("no `witness:` lines — every arm needs its theorem or `none`")
    for w in wits:
        if not lean_resolves(w.split(".")[-1]): errs.append(f"witness does not resolve: {w}")
    cited = set(re.findall(r"\b(D-[A-Z-]+)\b", t))
    ghost = cited - REG_IDS
    if ghost: errs.append(f"cited defects not in registry: {ghost}")
    if "defects:" not in t: errs.append("no `defects:` line (cite ids or `none`)")
    for kw, did in CONTACT.items():
        if kw.lower() in t.lower() and did not in cited:
            errs.append(f"registry contact without citation: '{kw}' touches {did}")
    g = re.findall(r"gauge:\s*(\S+)", t)
    if not g: errs.append("no `gauge:` line naming planted-truth evidence")
    for gf in g:
        p = ROOT / gf
        if not p.exists(): errs.append(f"gauge file missing: {gf}")
        else:
            gt = p.read_text().lower()
            if not (("pass" in gt) and any(k in gt for k in ("fire", "violation", "miss", "fail"))):
                errs.append(f"gauge not two-sided (needs a pass AND a fired case): {gf}")
    if not re.search(r"(Bonferroni|FDR|family-wise|familywise)", t, re.I):
        errs.append("no family-wise correction declared")
    stakes = [l for l in t.splitlines() if l.strip().startswith("|") and ("≥" in l or "≤" in l or "<=" in l or ">=" in l)]
    for l in stakes:
        if not re.search(r"\d", l): errs.append(f"non-numeric band: {l.strip()[:60]}")
    return errs

if __name__ == "__main__":
    bad = 0
    for p in sys.argv[1:]:
        errs = audit(p)
        print(f"== {p}: {'ADMISSIBLE' if not errs else 'REFUSED'}")
        for e in errs: print(f"   - {e}"); 
        bad += bool(errs)
    sys.exit(bad)
