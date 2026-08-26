"""Stamp provenance onto phase0_bakeoff.json and print the anomaly checks."""
import json, os, sys
sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen')
import embed

P = '/home/emoore/CIRISOntology/scratchpad/eigen/out/phase0_bakeoff.json'
V1 = '/home/emoore/CIRISOntology/scratchpad/eigen/out/main_primary.json'


def g(d, *path):
    for p in path:
        d = d[str(p)] if str(p) in d else d[p]
    return d


def main():
    R = json.load(open(P))
    prov = {}
    for m in ('BAAI/bge-large-en-v1.5', 'Qwen/Qwen3-Embedding-0.6B'):
        h, n = embed.cache_sha256(m)
        prov[m] = {'sha256': h, 'bytes': n}
    R['_meta']['cache_manifest'] = prov
    R['_meta']['spend_usd_total'] = embed.total_spend()
    R['_meta']['usage'] = json.load(open(
        '/home/emoore/CIRISOntology/scratchpad/eigen/out/usage.json'))
    json.dump(R, open(P, 'w'), indent=1, default=str)

    C = R['cells']
    print(f'cells: {len(C)}')
    print('ranks(B) distinct :', sorted({round(v["rank_B"], 3) for v in C.values()}))
    print('d_eff distinct    :', sorted({v['d_eff'] for v in C.values()}))
    print('cloud diag        :', json.dumps(R['cloud_diag']))
    print('spend total USD   : %.5f' % embed.total_spend())
    print('cache sha256      :', {k.split("/")[-1]: v['sha256'][:16] for k, v in prov.items()})

    v1 = json.load(open(V1))
    c4 = C.get('C4.bge.res')
    if c4:
        print('\nv1 REPRODUCTION CHECK (C4.bge.res must equal v1 P1a / K1c):')
        print('  Omega(11)       ours %.15f   v1 %.15f' %
              (g(c4, 'omega', 11), v1['P1a']['omega']['11']))
        print('  placebo Omega   ours %.15f   v1 %.15f' %
              (g(c4, 'placebo', 'omega', 11), v1['K1c']['omega_before']))
        print('  null median     ours %.6f          v1 %.6f' %
              (g(c4, 'null_median', 11), v1['P1a']['null_N1_median']))
        print('  p_N1            ours %.6f          v1 %.6f' %
              (g(c4, 'p_N1', 11), v1['P1a']['p_N1']))

    print('\nPASSING cells:')
    for k, v in C.items():
        if v['verdict'] == 'PASS':
            print(f'  {k:22s} Om={g(v,"omega",11):.4f} gap={v["gap"]["obs"]:+.4f} '
                  f'p_gap={v["gap"]["p_gap_N1"]:.4f} '
                  f'share_of_margin_from_placebo='
                  f'{v["gap"]["placebo_omega_minus_null"]/v["gap"]["omega_minus_null"]:.2f}')


if __name__ == '__main__':
    main()
