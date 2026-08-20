"""GAUGE TEST — freeze the ORIGINAL BASE modals and the untouched population.

Reads the EXISTING BASE judgments on disk (plane_corpus/full_judgments.jsonl). Nothing is
re-derived and nothing model-facing runs here. Convention is the programme's established one,
copied from polarity/build_corpus.py: BASE rows only, unparsed rows dropped as missing votes,
modal = plurality, tie for top -> no modal.
"""
from __future__ import annotations
import collections, json, pathlib

R = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/plane_corpus")
OUT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/gaugetest/originals.json")


def modal_of(votes):
    """Plurality; tie for top -> None. Unparsed votes must already be filtered out."""
    if not votes:
        return None
    c = collections.Counter(votes).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        return None
    return c[0][0]


def main():
    items = [json.loads(l) for l in open(R / "corpus_full.jsonl") if l.strip()]
    ids = [i["id"] for i in items]
    target = {i["id"]: i["kind_target"] for i in items}

    votes = collections.defaultdict(list)
    parse_fail = collections.Counter()
    nrows = 0
    for l in open(R / "full_judgments.jsonl"):
        r = json.loads(l)
        if r.get("condition") != "BASE":
            continue
        nrows += 1
        if not r.get("kind"):
            parse_fail[r["model"]] += 1
            continue
        votes[r["id"]].append(r["kind"])

    modal = {i: modal_of(votes.get(i, [])) for i in ids}
    untouched = [i for i in ids if modal[i] not in (None, "Circumstances", "Structure")]

    out = {"n_items": len(ids),
           "n_base_rows_all_ids": nrows,
           "base_parse_failures": dict(parse_fail),
           "modal": modal,
           "votes": {i: votes.get(i, []) for i in ids},
           "kind_target": target,
           "n_no_modal": sum(1 for i in ids if modal[i] is None),
           "n_modal_circumstances": sum(1 for i in ids if modal[i] == "Circumstances"),
           "n_modal_structure": sum(1 for i in ids if modal[i] == "Structure"),
           "untouched": untouched,
           "n_untouched": len(untouched),
           "modal_distribution": dict(collections.Counter(modal[i] for i in ids).most_common()),
           "target_counts": dict(collections.Counter(target.values())),
           }
    json.dump(out, open(OUT, "w"), indent=1)
    print(f"items {len(ids)}; BASE rows {nrows}; parse failures {dict(parse_fail)}")
    print(f"no modal (tie) {out['n_no_modal']}; modal=Circumstances {out['n_modal_circumstances']}; "
          f"modal=Structure {out['n_modal_structure']}")
    print(f"UNTOUCHED POPULATION N = {len(untouched)}  -> {OUT}")


if __name__ == "__main__":
    main()
