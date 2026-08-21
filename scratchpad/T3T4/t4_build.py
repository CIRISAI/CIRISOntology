"""Emit t4_items.jsonl from t4_author.ITEMS. Offsets are computed here, never authored."""
from __future__ import annotations
import json, sys
from t4_author import ITEMS

OUT = "/home/emoore/CIRISOntology/scratchpad/T3T4/t4_items.jsonl"


def build():
    lines = []
    for it in ITEMS:
        ident = it["id"]
        before, old, new, cut = it["before"], it["old"], it["new"], it["cut"]
        assert before.count(old) == 1, f"{ident}: old occurs {before.count(old)}x"
        assert before.count(cut) == 1, f"{ident}: cut occurs {before.count(cut)}x"
        assert old in cut, f"{ident}: old not inside cut"
        after = before.replace(old, new)
        cs = before.index(cut)
        ce = cs + len(cut)
        os_ = before.index(old)
        oe = os_ + len(old)
        rec = {
            "id": ident, "arm": it["arm"], "domain": it["domain"],
            "before": before, "after": after, "old": old, "new": new,
            "cut_start": cs, "cut_end": ce,
            "variation_site": it["site"], "author_note": it["note"],
        }
        if it["arm"] == "M":
            old_a, new_a, side = it["old_a"], it["new_a"], it["cutb_side"]
            assert old.startswith(old_a) and len(old_a) < len(old), f"{ident}: old_a"
            assert new.startswith(new_a) and len(new_a) < len(new), f"{ident}: new_a"
            split_b, split_a = os_ + len(old_a), os_ + len(new_a)
            if side == "head":
                rec.update(cutb_side="head", cutb_start=0, cutb_end=split_b,
                           cutb_after_start=0, cutb_after_end=split_a)
            elif side == "tail":
                delta = len(new) - len(old)
                rec.update(cutb_side="tail", cutb_start=split_b, cutb_end=len(before),
                           cutb_after_start=split_a, cutb_after_end=len(before) + delta)
            else:
                raise AssertionError(f"{ident}: cutb_side {side!r}")
            rec["cutb_framing"] = it["framing"]
        lines.append(json.dumps(rec, ensure_ascii=False))
    with open(OUT, "w") as f:
        f.write("\n".join(lines) + "\n")
    print(f"wrote {len(lines)} items to {OUT}")


if __name__ == "__main__":
    sys.exit(build())
