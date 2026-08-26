"""Render phase0_bakeoff.json as the markdown tables for EIGEN2_PHASE0.md."""
import json, sys

P = '/home/emoore/CIRISOntology/scratchpad/eigen/out/phase0_bakeoff.json'
NAME = {'C1': 'C1 span-in-context', 'C2': 'C2 concatenated pair',
        'C3': 'C3 residualized after', 'C4': 'C4 v1 baseline Δ',
        'C5': 'C5 sentence-level Δ *(added)*'}
EMB = {'bge': 'bge-large', 'qwen': 'Qwen3 +instr', 'qwen_noinstr': 'Qwen3 no instr'}
CONS = ('C1', 'C2', 'C3', 'C4', 'C5')
ARMS = ('bge', 'qwen', 'qwen_noinstr')


def g(d, *path):
    for p in path:
        d = d[str(p)] if str(p) in d else d[p]
    return d


def main(nuis):
    R = json.load(open(P))
    C = R['cells']
    print(f'#### nuisance arm: `{nuis}`\n')
    print('| construction | embedder | Ω(11) | rank(B) | null med | null p99 | p(N1) '
          '| placebo Ω(11) | placebo p(N1) | gap | gap null med | p(gap) | p paired '
          '| frac splits | verdict |')
    print('|---|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|')
    for e in ARMS:
        for c in CONS:
            k = f'{c}.{e}.{nuis}'
            if k not in C:
                continue
            d = C[k]
            pp, gp = d['placebo_paired'], d['gap']
            print(f'| {NAME[c]} | {EMB[e]} | **{g(d,"omega",11):.4f}** | '
                  f'{d["rank_B"]:.0f} | {g(d,"null_median",11):.4f} | '
                  f'{g(d,"null_p99",11):.4f} | '
                  f'{g(d,"p_N1",11):.4f} | {g(d,"placebo","omega",11):.4f} | '
                  f'{g(d,"placebo","p_N1",11):.4f} | {gp["obs"]:+.4f} | '
                  f'{gp["null_median"]:+.4f} | {gp["p_gap_N1"]:.4f} | '
                  f'{pp["p_paired"]:.4f} | {pp["frac_splits_gt"]:.2f} | {d["verdict"]} |')
    print()


def margins(nuis):
    R = json.load(open(P))
    C = R['cells']
    print(f'#### null-corrected margins, `{nuis}` arm\n')
    print('| construction | embedder | Ω−null | placebo Ω−null | ratio | evr(top 11) |')
    print('|---|---|---:|---:|---:|---:|')
    for e in ARMS:
        for c in CONS:
            k = f'{c}.{e}.{nuis}'
            if k not in C:
                continue
            d = C[k]
            m, pm = d['gap']['omega_minus_null'], d['gap']['placebo_omega_minus_null']
            r = m / pm if pm else float('nan')
            print(f'| {NAME[c]} | {EMB[e]} | {m:+.4f} | {pm:+.4f} | {r:.2f} | '
                  f'{d["evr_top11"]:.3f} |')
    print()


if __name__ == '__main__':
    for n in (sys.argv[1:] or ['res', 'raw']):
        main(n)
    for n in (sys.argv[1:] or ['res', 'raw']):
        margins(n)
