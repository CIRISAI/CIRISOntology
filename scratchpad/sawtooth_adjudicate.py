"""sawtooth_adjudicate.py — mechanical application of SAWTOOTH_FORWARD_PREREG.md (022096e) §6.

No number here is chosen after seeing the answer: the bands come from sawtooth_stake.json,
committed before any forward run started.
"""
import json, os, math, glob
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
CONDS = [(0.01, '0.1'), (0.01, '0.5'), (0.01, '1.0nat'),
         (0.05, '0.1'), (0.05, '0.5'), (0.05, '1.0nat')]
CN = ['0.01/10%', '0.01/50%', '0.01/1nat', '0.05/10%', '0.05/50%', '0.05/1nat']
STAKE = json.load(open(os.path.join(HERE, 'sawtooth_stake.json')))


def rows_of(path):
    d = json.load(open(path))
    out = {}
    for r in d['rows']:
        if r.get('dropped'):
            continue
        out[(r['eps'], r['target_label'])] = r
    return out, d.get('meta', {})


def load_all():
    """nat[k][cond] = rent/nat on the MINIMAL-m ladder; pl[(k,m,rule)][cond] = planted."""
    pl, meta = {}, {}
    nat = {'canonical': {}, 'systematic': {}, 'hiwt': {}}
    for suf, rule in (('', 'canonical'), ('sys', 'systematic'), ('hw', 'hiwt')):
        for k in range(20, 40):
            p = os.path.join(HERE, f'sawtooth_B{k}{suf}.json')
            if os.path.exists(p):
                r, mt = rows_of(p)
                nat[rule][k] = {c: v['rent_per_nat'] for c, v in r.items()}
                meta[(rule, k)] = mt
    for k in range(25, 33):                       # the committed Q2 arm-B tiers
        p = os.path.join(HERE, f'rent_scaling_q2_B{k}.json')
        if os.path.exists(p) and k not in nat['canonical']:
            r, _ = rows_of(p)
            nat['canonical'][k] = {c: v['rent_per_nat'] for c, v in r.items()}
    for p in sorted(glob.glob(os.path.join(HERE, 'sawtooth_P*.json'))):
        r, mt = rows_of(p)
        key = (mt['k'], mt['m'], mt.get('rule', 'canonical'))
        pl[key] = {c: v['rent_per_nat'] for c, v in r.items()}
        meta[key] = mt
    return nat, pl, meta


def tooth(nat, rent_k, k, cond):
    """tooth(k) with the MINIMAL-m ladder supplying L(k-3..k-1) and rent(k-1)."""
    need = [k - 4, k - 3, k - 2, k - 1]
    if any(j not in nat or cond not in nat[j] for j in need):
        return None
    L = {j: math.log(nat[j][cond]) - math.log(nat[j - 1][cond]) for j in (k - 3, k - 2, k - 1)}
    Lk = math.log(rent_k) - math.log(nat[k - 1][cond])
    base = [L[k - 3], L[k - 2], L[k - 1]]
    return (100.0 * (Lk - float(np.mean(base))), 100.0 * float(np.std(base, ddof=1)))


def adjudicate_plant(name, teeth, bands):
    pos = sum(1 for t, _ in teeth if t > 0)
    inb = sum(1 for (t, _), (p, lo, hi) in zip(teeth, bands) if lo <= t <= hi)
    res = all(abs(t) >= 10 * sd for t, sd in teeth)
    reach2 = sum(1 for t, _ in teeth if t < 2.0)
    if reach2 >= 2:
        v = 'FALSIFIED'
    elif pos == 6 and inb >= 5 and res:
        v = 'CONFIRMED'
    elif pos == 6 and res:
        v = 'LOCATION RIGHT, FORM WRONG'
    else:
        v = 'PARTIAL/UNCLEAR'
    print(f'  {name}: positive {pos}/6, in-band {inb}/6, clears 10x resolution: {res}'
          f'{"" if reach2 == 0 else f", below +2.0pp in {reach2}/6"}  -> {v}')
    return v, pos, inb, res


def main():
    nat, pl, meta = load_all()
    print('=' * 104)
    print('SAWTOOTH FORWARD — adjudication against SAWTOOTH_FORWARD_PREREG.md @ 022096e')
    print('=' * 104)
    for r in ('canonical','systematic','hiwt'):
        if nat[r]: print(f'minimal-m ladder ({r}): {sorted(nat[r])}')
    print(f'planted runs available:       {sorted(pl)}')
    verdicts = {}

    # ---------------- P-PLANT
    print('\n--- P-PLANT: one ln2 step planted where arm B has none (canonical rule) ---')
    print(f'{"k":>4} {"cond":>10} {"tooth":>9} {"band":>16} {"res sd":>8} {"x res":>7} {"natural":>9}')
    for k in (24, 26, 28, 30):
        key = (k, 6, 'canonical')
        if key not in pl:
            print(f'{k:>4}   (not yet run)')
            continue
        teeth, bands = [], []
        for c, cn in zip(CONDS, CN):
            t = tooth(nat['canonical'], pl[key][c], k, c)
            b = STAKE['plant'][f'{k}|1|{c[0]}|{c[1]}']
            natt = tooth(nat['canonical'], nat['canonical'][k][c], k, c) if k in nat['canonical'] else None
            teeth.append(t); bands.append(b)
            mark = 'IN ' if b[1] <= t[0] <= b[2] else 'OUT'
            print(f'{k:>4} {cn:>10} {t[0]:>9.3f} [{b[1]:>6.2f},{b[2]:>6.2f}] {mark} {t[1]:>8.4f}'
                  f' {abs(t[0])/t[1]:>7.0f} {natt[0] if natt else float("nan"):>9.3f}')
        verdicts[f'P-PLANT k={k}'] = adjudicate_plant(f'P-PLANT k={k}', teeth, bands)[0]

    # ---------------- column-rule control + P-LINEAR, each family vs its OWN ladder
    for rule, dmin in (('systematic', 1), ('hiwt', 11)):
        if not any(key[2] == rule for key in pl):
            continue
        lad = nat[rule] if nat[rule] else nat['canonical']
        src = 'own-rule ladder' if nat[rule] else 'CANONICAL ladder (own not run)'
        print(f'\n--- k=28, {rule} rule (planted-code d_min={dmin}), baseline = {src} ---')
        for m, nstep in ((6, 1), (7, 2)):
            key = (28, m, rule)
            if key not in pl:
                continue
            teeth, bands = [], []
            for c, cn in zip(CONDS, CN):
                t = tooth(lad, pl[key][c], 28, c)
                b = STAKE['plant'][f'28|{nstep}|{c[0]}|{c[1]}']
                teeth.append(t); bands.append(b)
                mark = 'IN ' if b[1] <= t[0] <= b[2] else 'OUT'
                print(f'  n={nstep} {cn:>10} {t[0]:>9.3f} [{b[1]:>6.2f},{b[2]:>6.2f}] {mark}'
                      f' res {t[1]:>7.4f} ({abs(t[0])/t[1]:>5.0f}x)')
            verdicts[f'{rule} n={nstep}'] = adjudicate_plant(f'{rule} n={nstep}', teeth, bands)[0]
        if (28, 7, rule) in pl and (28, 6, rule) in pl:
            rs = []
            for c, cn in zip(CONDS, CN):
                t2 = tooth(lad, pl[(28, 7, rule)][c], 28, c)[0]
                t1 = tooth(lad, pl[(28, 6, rule)][c], 28, c)[0]
                rs.append(t2 / t1)
            print(f'  P-LINEAR ratio tooth(n=2)/tooth(n=1), predicted 2.000: '
                  f'mean {np.mean(rs):.4f}  range [{min(rs):.4f}, {max(rs):.4f}]  '
                  f'({"CONFIRMED" if all(1.8 <= r <= 2.2 for r in rs) else "OUTSIDE 1.8-2.2"})')
            print('     per condition: ' + ' '.join(f'{cn}={r:.4f}' for cn, r in zip(CN, rs)))
            verdicts[f'P-LINEAR ratio ({rule})'] = f'{np.mean(rs):.4f}'

    # ---------------- P-AFTER / P-ABSENT
    print('\n--- P-AFTER / P-ABSENT: arm B natural k=33,34,35 ---')
    print(f'{"k":>4} {"cond":>10} {"tooth":>9} {"band":>18} {"res sd":>8}')
    for k in (33, 34, 35):
        if k not in nat['canonical']:
            print(f'{k:>4}   (not yet run)')
            continue
        inb, over = 0, 0
        for c, cn in zip(CONDS, CN):
            t = tooth(nat['canonical'], nat['canonical'][k][c], k, c)
            b = STAKE['after'][f'{k}|{c[0]}|{c[1]}']
            ok = b[1] <= t[0] <= b[2]
            inb += ok
            over += (t[0] > 1.1)
            print(f'{k:>4} {cn:>10} {t[0]:>9.3f} [{b[1]:>+7.2f},{b[2]:>+7.2f}] {"IN " if ok else "OUT"}'
                  f' {t[1]:>8.4f}')
        va = 'CONFIRMED' if inb >= 5 else 'NOT CONFIRMED'
        vb = 'FALSIFIED' if over >= 2 else 'not falsified'
        print(f'  k={k}: P-AFTER in-band {inb}/6 -> {va};  P-ABSENT ({over}/6 above +1.1pp) -> {vb}')
        verdicts[f'P-AFTER k={k}'], verdicts[f'P-ABSENT k={k}'] = va, vb

    # ---------------- campaign verdict
    print('\n' + '=' * 104)
    npl = sum(1 for k in (24, 26, 28, 30) if verdicts.get(f'P-PLANT k={k}') == 'CONFIRMED')
    print(f'P-PLANT confirmed at {npl} of 4 planted k')
    for k, v in verdicts.items():
        print(f'   {k:>28} : {v}')
    json.dump({k: v for k, v in verdicts.items()},
              open(os.path.join(HERE, 'sawtooth_verdicts.json'), 'w'), indent=1)


if __name__ == '__main__':
    main()
