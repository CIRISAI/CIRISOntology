#!/usr/bin/env python3
"""Emit WATER_RESULTS.md's numeric tables straight from the JSONs.

Transcribing numbers by hand from a log into a document is the same operation as
taking a number from a sibling's message: it is HEARSAY until it is re-derived
from the primary artifact (`GATES.md`, *received numbers are not measured
numbers*).  The rule is usually applied across campaigns; it applies at least as
strongly within one, between a run's JSON and the paragraph that quotes it.
Every table this prints is generated from the artifact it describes.
"""
import json
import sys

import numpy as np

S = "/home/emoore/CIRISOntology/scratchpad/"
LN2 = float(np.log(2.0))


def ladder(path=S + "water_arm_a_final.json"):
    r = json.load(open(path))
    print("cap (triangles/config, G-DOSE): %d\n" % r["cap"])
    for tag in ("full", "matched"):
        if tag not in r["cells"]:
            continue
        print("**%s count**\n" % tag)
        print("| `λ` | `P` (atm) | `p₁` | `N_tri` | share (nats) | floor median | "
              "excess | `p` | sharp ceiling | ceil/floor | headroom | rel sd |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for k in sorted(r["cells"][tag], key=float):
            c = r["cells"][tag][k]
            print("| %s | %+.0f | %.3f | %.2e | %.3e | %.3e | %+.3e | %.4f | %.5f | %.0f | %.3f | %.0f %% |"
                  % (k, c.get("press") or float("nan"), c["p1"], c["n_triples"],
                     c["share"], c["floor_median"], c["excess"], c["p_value"],
                     c["ceiling"], c["ceiling_over_floor"], c["headroom"],
                     100 * c["rel_sd_ratio"]))
        print()
    print("**far arm**\n")
    print("| `λ` | `ξ` (Å) | `r_far` (Å) | far `N_tri` | far share | far floor p99 | far `p` |")
    print("|---|---|---|---|---|---|---|")
    for k in sorted(r["cells"]["full"], key=float):
        c = r["cells"]["full"][k]
        f = c.get("far")
        pre = r["pre"][k]
        print("| %s | %.2f | %.2f | %.2e | %.3e | %.3e | %.4f |"
              % (k, pre["xi"], c["far_radius"],
                 f["n_triples"] if f else float("nan"),
                 f["share"] if f else float("nan"),
                 f["floor_p99"] if f else float("nan"),
                 f["p_value"] if f else float("nan")))
    print()
    # monotonicity of the matched-count ladder
    tag = "matched" if "matched" in r["cells"] else "full"
    ks = sorted(r["cells"][tag], key=float)
    sh = [r["cells"][tag][k]["share"] for k in ks]
    ex = [r["cells"][tag][k]["excess"] for k in ks]
    ps = [r["cells"][tag][k]["p_value"] for k in ks]
    print("monotone in share?   %s" % all(sh[i] <= sh[i + 1] for i in range(len(sh) - 1)))
    print("monotone in excess?  %s" % all(ex[i] <= ex[i + 1] for i in range(len(ex) - 1)))
    print("cells with p < 0.05: %s of %d" % ([k for k, p in zip(ks, ps) if p < 0.05], len(ks)))
    print("cells with p < 0.01: %s" % [k for k, p in zip(ks, ps) if p < 0.01])
    print("share range: %.3e .. %.3e" % (min(sh), max(sh)))


def armb(path=S + "water_arm_b.json", n2path=S + "water_arm_b_n2.json"):
    r = json.load(open(path))
    try:
        n2 = json.load(open(n2path))
    except FileNotFoundError:
        n2 = None
    print("KA: N=%d L=%.4f rho=%.4f;  r_cut(B-own)=%.4f (its own g(r) first min %.3f);"
          "  r_cut(B-matched)=%.4f\n"
          % (r["N"], r["L"], r["rho"], r["rcut_own"], r["gr_first_min"], r["rcut_matched"]))
    for v in r["cells"]:
        print("**%s — `r_cut = %.4f σ`**\n" % (v, r["rcut_own"] if v == "B_own" else r["rcut_matched"]))
        print("| template | `T` | `p₁` | `N_tri` | share (nats) | floor median | `p` | "
              "sharp ceiling | share/ceiling | share/ln2 | headroom | min cell |")
        print("|---|---|---|---|---|---|---|---|---|---|---|---|")
        for t in r["cells"][v]:
            for T in sorted(r["cells"][v][t], key=float):
                c = r["cells"][v][t][T]
                cf = c["share"] / c["ceiling"] if c["ceiling"] > 0 else float("nan")
                print("| %s | %s | %.3f | %.2e | %.4e | %.3e | %.4f | %.5f | %.3f %% | %.2e | %.4f | %.0f |"
                      % (t, T, c["p1"], c["n_triples"], c["share"], c["floor_median"],
                         c["p_value"], c["ceiling"], 100 * cf, c["share"] / LN2,
                         c["headroom"], c["min_cell"]))
        print()
        # temperature trend, both denominators
        for t in r["cells"][v]:
            Ts = sorted(r["cells"][v][t], key=float)
            sh = [r["cells"][v][t][T]["share"] for T in Ts]
            ce = [r["cells"][v][t][T]["ceiling"] for T in Ts]
            if len(sh) < 2 or max(sh) == 0:
                continue
            fr = [s / c if c > 0 else float("nan") for s, c in zip(sh, ce)]
            print("  %s %s: raw cold/hot = x%.2f ; against SHARP ceiling = x%.2f "
                  "(ceiling itself x%.2f) ; monotone in T: %s"
                  % (v, t, sh[0] / sh[-1] if sh[-1] else float("nan"),
                     fr[0] / fr[-1] if fr[-1] else float("nan"),
                     ce[0] / ce[-1] if ce[-1] else float("nan"),
                     all(sh[i] >= sh[i + 1] for i in range(len(sh) - 1))))
        print()
    if n2:
        print("**arm B's own ideal-gas control (glass's `SYNTH_ideal`, %d configs)**\n"
              % n2["nconf"])
        print("| variant | template | `p₁` | `N_tri` | share | floor median | `p` |")
        print("|---|---|---|---|---|---|---|")
        for v in n2["cells"]:
            for t in n2["cells"][v]:
                c = n2["cells"][v][t]
                print("| %s | %s | %.3f | %.2e | %.4e | %.3e | %.4f |"
                      % (v, t, c["p1"], c["n_triples"], c["share"],
                         c["floor_median"], c["p_value"]))


if __name__ == "__main__":
    which = sys.argv[1] if len(sys.argv) > 1 else "all"
    if which in ("all", "ladder"):
        print("### LADDER\n")
        try:
            ladder()
        except FileNotFoundError as e:
            print("NOT AVAILABLE:", e)
    if which in ("all", "armb"):
        print("\n### ARM B\n")
        try:
            armb()
        except FileNotFoundError as e:
            print("NOT AVAILABLE:", e)
