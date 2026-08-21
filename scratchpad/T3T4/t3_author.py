"""T3 item corpus — authoring pass.  Writes t3_items.jsonl from the four arm
modules.  Validation lives in check_t3.py and is run separately."""
import json, sys, os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import t3_items_A, t3_items_B, t3_items_Drule, t3_items_Dfact

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "t3_items.jsonl")

rows = []
for mod in (t3_items_A, t3_items_B, t3_items_Drule, t3_items_Dfact):
    for it in mod.ITEMS:
        before, old, new = it["before"], it["old"], it["new"]
        rows.append({
            "id": it["id"], "arm": it["arm"], "domain": it["domain"],
            "before": before, "after": before.replace(old, new),
            "old": old, "new": new,
            "variation_site": it["site"], "author_note": it["note"],
        })

with open(OUT, "w") as f:
    for r in rows:
        f.write(json.dumps(r, ensure_ascii=False) + "\n")
print(f"wrote {len(rows)} items to {OUT}")
