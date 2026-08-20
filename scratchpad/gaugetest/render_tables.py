"""GAUGE TEST — render the markdown tables from void.json / gauge_results.json so the
write-up cannot mis-transcribe a number. Pure formatting; computes nothing new."""
from __future__ import annotations
import collections, json, math, pathlib

ROOT = pathlib.Path("/home/emoore/CIRISOntology/scratchpad/gaugetest")
R = json.load(open(ROOT / "gauge_results.json"))
V = json.load(open(ROOT / "void.json"))


def pct(x):
    return f"{100*x:.1f}%"


print("### primary\n")
n = R["counts"]["n"]
print("| arm | label set | perturbed / n | fraction |")
print("|---|---|---|---|")
print(f"| **A** | full 11 + Record (re-run) | {R['counts']['xA']} / {n} | **{pct(R['pA'])}** |")
print(f"| **B** | Circumstances removed | {R['counts']['xB']} / {n} | **{pct(R['pB'])}** |")
print(f"| **C** | Structure removed | {R['counts']['xC']} / {n} | **{pct(R['pC'])}** |")

print("\n### tests\n")
print("| comparison | diff | z | p (one-sided) | p (two-sided) | McNemar exact (one-sided) |")
print("|---|---|---|---|---|---|")
for name, t, mc in (("C − A (control)", R["control_test_C_vs_A"], R["mcnemar_C_vs_A"]),
                    ("B − A (treatment)", R["treatment_test_B_vs_A"], R["mcnemar_B_vs_A"])):
    z = t.get("z")
    zs = "—" if z is None or (isinstance(z, float) and math.isnan(z)) else f"{z:.3f}"
    print(f"| {name} | {t['diff']*100:+.1f} pp | {zs} | {t['p_one_sided']:.4g} | "
          f"{t['p_two_sided']:.4g} | b={mc['b']}, c={mc['c']}, p={mc['p_one_sided']:.4g} |")

print("\n### sensitivity — arm ties dropped pairwise\n")
print("| comparison | n kept | p(treat) | p(base) | diff | p (one-sided) |")
print("|---|---|---|---|---|---|")
for k, s in R["sensitivity_ties_dropped"].items():
    print(f"| {k} | {s['n']} | {pct(s['p_treat'])} | {pct(s['p_base'])} | "
          f"{(s['p_treat']-s['p_base'])*100:+.1f} pp | {s['test']['p_one_sided']:.4g} |")

print("\n### orphans — authored-target population (the prereg's)\n")
for arm in ("C", "B"):
    o = R["orphans"][arm]
    print(f"**arm {arm} — `{o['removed']}` removed, n = {o['n']} authored items**  ")
    print(f"destinations: " + ", ".join(f"`{k}` {v}" for k, v in o["distribution"].items()))
    print(f"  entropy **{o['entropy_bits']:.3f} bits** (normalised {o['entropy_normalised']:.3f} "
          f"of log2 11); top `{o['top'][0]}` at {pct(o['top_share'])}")
    print(f"  original modals of the same items: " +
          ", ".join(f"`{k}` {v}" for k, v in o["original_modal_distribution"].items()))
    s = o["sensitivity_modal_orphans"]
    print(f"  TRUE-ORPHAN sensitivity (original modal was `{o['removed']}`, n = {s['n']}): " +
          ", ".join(f"`{k}` {v}" for k, v in s["distribution"].items()) +
          f" — entropy {s['entropy_bits']:.3f} bits")
    print()

print("### per-arm protocol\n")
print("| arm | rows | (item,model) cells | parse failures | rate | ties in the 212 | off-vocabulary labels |")
print("|---|---|---|---|---|---|---|")
for a, d in R["arm_protocol"].items():
    print(f"| {a} | {d['rows']} | {d['cells']} | {d['parse_failures']} | "
          f"{100*d['parse_fail_rate']:.2f}% | {d['ties_in_pop']} | {d['offvocab'] or '—'} |")

print("\n### movement of the untouched 212 (diagnostic, carries no verdict)\n")
for a in ("A", "B", "C"):
    mv = R["movement"][a]
    tot = sum(mv.values())
    top = list(mv.items())[:8]
    print(f"**{a}** ({tot} moves): " + (", ".join(f"`{k}` ×{v}" for k, v in top) if top else "none"))

sp = 0.0
for p in sorted(ROOT.glob("spend_*.json")):
    d = json.load(open(p))
    sp += d["spend"]
    print(f"\nspend {p.name}: ${d['spend']:.4f} ({d['n']} judgments, "
          f"{d.get('request_failures',0)} request failures)")
print(f"\nTOTAL SPEND ${sp:.4f} of the $0.40 cap")
