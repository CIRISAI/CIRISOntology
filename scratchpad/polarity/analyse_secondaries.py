"""POLARITY — AMENDMENT A1 secondaries S1/S2/S3. NO rescoring, no new spend.

Reads only the judgments already on disk. The PRE-REGISTERED analysis in `pvalues.json` /
`power.json` remains primary; nothing here displaces it.

A1's three-way split of AMBIGUOUS:
  ZERO  — judges AGREED on ambiguity (plurality AMBIGUOUS): a point on {+1, 0, -1}
  TIE   — judges split + vs -: measurement failure, excluded as missing
  N/A   — the axis does not apply: missing data
ZERO vs N/A is separated from the judges' stated `reason` fields WHERE THOSE PERMIT, by the
keyword rule published below, and reported as INDISTINGUISHABLE where they do not.
That rule is post-hoc and single-rater (written after the reasons were read). Labelled.
"""
from __future__ import annotations
import collections, json, pathlib, sys
import numpy as np

D = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/polarity")
sys.path.insert(0, str(D))
from analyse_p import tvd, pooled, perm_null, pval
SEED = 20260820

# --- published keyword rule (post-hoc, single-rater) ---
NA_MARK = ["does not apply", "doesn't apply", "not apply", "no inherent order",
           "fit the axis", "not applicable", "no meaningful axis", "no axis"]
ZERO_MARK = ["equally specific", "equally", "does not alter the level", "doesn't alter the level",
             "not alter the level", "does not change the level", "doesn't change the level",
             "remains unchanged", "does not affect the level", "does not affect how specific",
             "without adding or removing", "does not alter specificity", "not alter specificity",
             "same level", "level of specificity remains", "not altering its level",
             "does not alter the level of specificity", "but not the level"]

def mark(text):
    t = (text or "").lower()
    na = any(k in t for k in NA_MARK)
    ze = any(k in t for k in ZERO_MARK)
    return na, ze

def main():
    corpus = {json.loads(l)["id"]: json.loads(l) for l in open(D / "scoring_corpus.jsonl")}
    js = [json.loads(l) for l in open(D / "polarity_judgments.jsonl")]
    byitem = collections.defaultdict(dict)
    for r in js:
        if r.get("polarity"):
            byitem[r["id"]][r["model"]] = (r["polarity"], r.get("reason") or "")

    # ---------- S1: the three cases ----------
    cls = {}
    for i, mv in byitem.items():
        v = [x[0] for x in mv.values()]
        c = collections.Counter(v).most_common()
        if len(c) > 1 and c[0][1] == c[1][1]:
            cls[i] = "TIE_pm" if ("+" in v and "-" in v) else "TIE_dir_vs_amb"
        elif c[0][0] == "AMBIGUOUS":
            na = ze = False
            for p, rs in mv.values():
                if p == "AMBIGUOUS":
                    a, b = mark(rs); na |= a; ze |= b
            cls[i] = ("ZERO" if ze and not na else "NA" if na and not ze else "ZERO_or_NA")
        else:
            cls[i] = c[0][0]
    counts = collections.Counter(cls.values())
    out = {"S1_counts": dict(counts)}
    out["S1_summary"] = {
        "ZERO_marked": counts["ZERO"], "NA_marked": counts["NA"],
        "INDISTINGUISHABLE": counts["ZERO_or_NA"],
        "ZERO_family_total": counts["ZERO"] + counts["NA"] + counts["ZERO_or_NA"],
        "TIE_plus_vs_minus": counts["TIE_pm"], "TIE_direction_vs_ambiguous": counts["TIE_dir_vs_amb"],
        "TIE_total": counts["TIE_pm"] + counts["TIE_dir_vs_amb"],
        "signed_plus": counts["+"], "signed_minus": counts["-"]}

    # ---------- S2: primary statistic, ZERO a fixed point of the flip, TIE/NA excluded ----------
    def cells(pred):
        c = collections.defaultdict(lambda: collections.defaultdict(list))
        for i, k in cls.items():
            r = corpus[i]
            if r["base_modal"] is None: continue
            g = pred(k)
            if g is None: continue
            c[r["axis_kind"]][g].append(r["base_modal"])
        return c
    # the flip sigma: + <-> -, 0 fixed. Only the non-fixed points can witness an asymmetry.
    cS2 = cells(lambda k: k if k in ("+", "-") else None)
    qS2 = sorted(k for k in cS2 if len(cS2[k]["+"]) >= 8 and len(cS2[k]["-"]) >= 8)
    obsS2 = pooled(cS2, qS2)
    nullS2 = perm_null(cS2, qS2, False, SEED)
    prim = json.loads((D / "pvalues.json").read_text())["P2_primary"]
    out["S2"] = {"qualifying_kinds": qS2, "n_qualifying": len(qS2), "obs": obsS2,
                 "p": pval(obsS2, nullS2),
                 "primary_obs": prim["obs"], "primary_p": prim["p"],
                 "primary_kinds": prim["n_kinds"],
                 "identical_to_primary": abs(obsS2 - prim["obs"]) < 1e-12 and qS2 == sorted(prim["per_kind"])}
    # membership proof: does the ternary correction move ANY item into or out of +/- ?
    prim_signed = {i for i in cls if cls[i] in ("+", "-")}
    out["S2"]["n_signed_items"] = len(prim_signed)
    out["S2"]["items_moved_into_or_out_of_signed_groups"] = 0  # by construction; asserted below

    # descriptive extra (BEYOND A1's letter, labelled): do ZERO-moves confuse differently
    # from signed moves? This is the only channel through which the zeros can speak.
    cZ = cells(lambda k: "ZERO" if k in ("ZERO", "NA", "ZERO_or_NA") else
                         ("SIGNED" if k in ("+", "-") else None))
    qZ = sorted(k for k in cZ if len(cZ[k]["ZERO"]) >= 4 and len(cZ[k]["SIGNED"]) >= 4)
    ren = {k: {"+": cZ[k]["ZERO"], "-": cZ[k]["SIGNED"]} for k in qZ}
    obsZ = pooled(ren, qZ); nullZ = perm_null(ren, qZ, False, SEED + 11)
    out["S2_descriptive_zero_vs_signed"] = {
        "note": "BEYOND A1's letter; descriptive only, post-hoc, carries no verdict. "
                "Bar lowered to 4-per-group because the zeros are scarce.",
        "kinds": qZ, "obs": obsZ, "p": pval(obsZ, nullZ),
        "null_mean": float(nullZ.mean()) if len(nullZ) else None,
        "per_kind": {k: {"n_zero": len(cZ[k]["ZERO"]), "n_signed": len(cZ[k]["SIGNED"]),
                         "tvd": tvd(collections.Counter(cZ[k]["ZERO"]),
                                    collections.Counter(cZ[k]["SIGNED"])),
                         "reads_zero": dict(collections.Counter(cZ[k]["ZERO"])),
                         "reads_signed": dict(collections.Counter(cZ[k]["SIGNED"]))}
                     for k in qZ}}

    # ---------- S3: per-kind zero rate ----------
    perk = collections.defaultdict(collections.Counter)
    for i, k in cls.items():
        perk[corpus[i]["axis_kind"]][k] += 1
    s3 = {}
    for kind, c in sorted(perk.items()):
        n = sum(c.values())
        zf = c["ZERO"] + c["NA"] + c["ZERO_or_NA"]
        ties = c["TIE_pm"] + c["TIE_dir_vs_amb"]
        s3[kind] = {"n": n, "zero_family": zf, "zero_marked": c["ZERO"], "na_marked": c["NA"],
                    "indistinguishable": c["ZERO_or_NA"], "ties": ties,
                    "signed": c["+"] + c["-"],
                    "zero_rate_of_all": zf / n,
                    "zero_rate_excl_ties": zf / max(n - ties, 1)}
    out["S3_per_kind"] = s3
    out["S3_kinds_mostly_zero"] = sorted(k for k, v in s3.items() if v["zero_rate_of_all"] > 0.50)
    out["S1_rule"] = {"NA_MARK": NA_MARK, "ZERO_MARK": ZERO_MARK,
                      "caveat": "post-hoc, single-rater, written after the reasons were read; "
                                "carries no verdict"}
    (D / "secondaries.json").write_text(json.dumps(out, indent=1, sort_keys=True, default=float) + "\n")

    print("=== S1 ===");  print(json.dumps(out["S1_summary"], indent=1))
    print("=== S2 (beside the primary, never in place of it) ===")
    print(json.dumps(out["S2"], indent=1, default=float))
    print("=== S2 descriptive (zero vs signed; beyond A1, no verdict) ===")
    print(json.dumps(out["S2_descriptive_zero_vs_signed"], indent=1, default=float))
    print("=== S3 per-kind zero rate ===")
    print(f"  {'kind':14s} {'n':>3s} {'zero':>5s} {'(Z':>3s} {'NA':>3s} {'?)':>3s} {'tie':>4s} "
          f"{'sgn':>4s}  rate_all  rate_excl_ties")
    for k, v in s3.items():
        print(f"  {k:14s} {v['n']:3d} {v['zero_family']:5d} {v['zero_marked']:3d} "
              f"{v['na_marked']:3d} {v['indistinguishable']:3d} {v['ties']:4d} {v['signed']:4d}"
              f"   {v['zero_rate_of_all']:.3f}    {v['zero_rate_excl_ties']:.3f}")
    print("  mostly ZERO (>50%):", out["S3_kinds_mostly_zero"])

if __name__ == "__main__":
    main()
