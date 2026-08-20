#!/usr/bin/env python3
"""The unreachable-module check: every CIRISOntology/Core/*.lean must be imported
(directly or transitively) from the root module CIRISOntology.lean.

Why this exists (2026-08-19): the axiom audit's enumeration gate walks the
ENVIRONMENT — whatever the root imports. A Core module never wired into the root
compiles standalone, ships in the repo, and is invisible to the build, the audit,
and the gate alike. This check closes the one hole no in-environment gate can see.
Exit 1 with the orphan list on failure."""
import re, sys, pathlib

root = pathlib.Path(__file__).resolve().parent.parent
core = {p.stem for p in (root / "CIRISOntology" / "Core").glob("*.lean")}

seen, todo = set(), ["CIRISOntology"]
while todo:
    mod = todo.pop()
    if mod in seen: continue
    seen.add(mod)
    f = root / (mod.replace(".", "/") + ".lean")
    if not f.exists(): continue
    for m in re.findall(r"^import\s+([\w.]+)", f.read_text(), re.M):
        todo.append(m)

reachable = {m.split(".")[-1] for m in seen if m.startswith("CIRISOntology.Core.")}
orphans = sorted(core - reachable)
if orphans:
    print("UNREACHABLE Core modules (exist on disk, never imported from the root):")
    for o in orphans: print("  -", o)
    sys.exit(1)
print(f"reachability OK: all {len(core)} Core modules imported from the root")
