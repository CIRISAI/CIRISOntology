"""Instrument suite v0 — the four heuristic-dominant instruments, executable.

Mirrors Core/Instrument.lean: coordinate-typed, refuse-rather-than-guess, and
every instrument SHIPS WITH ITS DYE TESTS (a planted known-bad it must catch and
a known-good it must pass) — per gatecraft, an instrument without its dye test
is a hypothesis about an instrument. Run this file to execute all dye tests.

Verdicts: FIRES (the kind's wrong is present), CLEAN, or REFUSED(reason) when a
required coordinate is missing. REFUSED is a first-class outcome, never an error.

v0 scope, stated: these are the heuristic halves only. Judge halves and the
XV-series bake-offs come later; nothing here is validated and the Lean pins
that (`suite_ships_unvalidated`).
"""
from __future__ import annotations
import ast, json
from dataclasses import dataclass
from typing import Optional


@dataclass
class Verdict:
    instrument: str
    result: str            # FIRES | CLEAN | REFUSED
    detail: str

    def __repr__(self):
        return f"[{self.instrument:13s}] {self.result:7s} {self.detail}"


# ---------------------------------------------------------------- Structure
def structure(before: str, after: str, lang: str = "auto") -> Verdict:
    """Does the change break parsing/dispatch? Heuristic IS the discriminator."""
    def parses(txt: str) -> tuple[bool, str]:
        errs = []
        for name, fn in (("json", json.loads), ("python", lambda t: ast.parse(t))):
            if lang in (name, "auto"):
                try:
                    fn(txt); return True, name
                except Exception as e:
                    errs.append(f"{name}: {type(e).__name__}")
        return False, "; ".join(errs)
    ok_b, how_b = parses(before)
    ok_a, how_a = parses(after)
    if not ok_b:
        return Verdict("structure", "REFUSED", f"BEFORE does not parse ({how_b}) — no baseline")
    if ok_a:
        return Verdict("structure", "CLEAN", f"both parse ({how_b}->{how_a})")
    return Verdict("structure", "FIRES", f"AFTER fails to parse ({how_a})")


# ---------------------------------------------------------------- Process
def process(before_steps: list[str], after_steps: list[str]) -> Verdict:
    """Orchestration change with the pieces intact: same step set, different
    order/wiring — or steps added/removed while everything still parses."""
    sb, sa = set(before_steps), set(after_steps)
    if before_steps == after_steps:
        return Verdict("process", "CLEAN", "identical orchestration")
    if sb == sa:
        return Verdict("process", "FIRES", "same steps, order changed: "
                       f"{before_steps} -> {after_steps}")
    return Verdict("process", "FIRES",
                   f"steps added {sorted(sa - sb)} removed {sorted(sb - sa)}")


# ---------------------------------------------------------------- Circumstances
def circumstances(varied_element: str, design: Optional[list[str]]) -> Verdict:
    """Design-relative BY DEFINITION: contingent means 'not in the comparison's
    held-fixed set'. Without a declared design there is nothing to read."""
    if design is None:
        return Verdict("circumstances", "REFUSED",
                       "no design declared — contingency is relative to the comparison")
    if varied_element in design:
        return Verdict("circumstances", "CLEAN",
                       f"'{varied_element}' is HELD by the declared design — a wrong here is another kind")
    return Verdict("circumstances", "FIRES",
                   f"'{varied_element}' is outside the held-fixed set: contingent, out of scope")


# ---------------------------------------------------------------- Record
def record(lost_fact: str, frame: Optional[list[str]]) -> Verdict:
    """The Lean's Repairable predicate, operational: re-derivable from the
    DECLARED frame? Substring containment is the v0 re-derivability proxy —
    deliberately crude, deliberately explicit."""
    if frame is None:
        return Verdict("record", "REFUSED",
                       "no frame declared — repairability is relative to what survives "
                       "(repairable_does_not_factor)")
    if any(lost_fact in doc for doc in frame):
        return Verdict("record", "CLEAN", "fact re-derivable from the surviving frame")
    return Verdict("record", "FIRES",
                   "the event can no longer be established from what survives")


# ---------------------------------------------------------------- dye tests
def dye_tests() -> list[tuple[str, bool]]:
    t = []
    # structure: planted breakage must fire; clean edit must pass; broken baseline refused
    t.append(("structure catches planted break",
              structure('{"a": 1}', '{"a": 1').result == "FIRES"))
    t.append(("structure passes clean edit",
              structure('{"a": 1}', '{"a": 2}').result == "CLEAN"))
    t.append(("structure refuses broken baseline",
              structure('{"a":', '{"a": 1}').result == "REFUSED"))
    # process: reorder fires; identity clean
    t.append(("process catches reorder",
              process(["fetch", "vet", "act"], ["fetch", "act", "vet"]).result == "FIRES"))
    t.append(("process passes identical flow",
              process(["fetch", "vet"], ["fetch", "vet"]).result == "CLEAN"))
    # circumstances: refuses without design; classifies with it, both directions
    t.append(("circumstances refuses without design",
              circumstances("temperature", None).result == "REFUSED"))
    t.append(("circumstances fires outside held set",
              circumstances("temperature", ["prompt", "model"]).result == "FIRES"))
    t.append(("circumstances clean inside held set",
              circumstances("model", ["prompt", "model"]).result == "CLEAN"))
    # record: refuses without frame; the Lean counterexample, operational —
    # ONE fact, TWO frames, OPPOSITE verdicts (repairability_not_intrinsic)
    t.append(("record refuses without frame",
              record("the vote was 5-4", None).result == "REFUSED"))
    t.append(("record: same fact, surviving frame -> CLEAN",
              record("the vote was 5-4",
                     ["minutes: the vote was 5-4 after debate"]).result == "CLEAN"))
    t.append(("record: same fact, empty frame -> FIRES",
              record("the vote was 5-4", []).result == "FIRES"))
    return t


if __name__ == "__main__":
    results = dye_tests()
    width = max(len(n) for n, _ in results)
    ok = True
    for name, passed in results:
        print(f"  {name:<{width}}  {'PASS' if passed else 'FAIL'}")
        ok &= passed
    print(f"\n{'ALL DYE TESTS PASS' if ok else 'DYE FAILURE — instrument not fit to ship'} "
          f"({sum(p for _, p in results)}/{len(results)})")
    raise SystemExit(0 if ok else 1)
