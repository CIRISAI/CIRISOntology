"""S20 panel diagnostics + the S5 secondary label arm's label vector.

Uses, exhaustive per S20: (a) the secondary label arm of S5 (subject to V3's support floor);
(b) reported diagnostics — three-model kappa, modal-vs-authored agreement, per-kind confusion
against v1's three predicted boundaries (Premises/Facts, Structure/Manner, Model/Facts), the
Record false-positive rate (staked reading: a modal of Record on > 5% of 474 artifact-only
changes means annotators read the relation as a content category), the modal no-fit rate, and
the modal agreement rate split by difficulty.

Off-vocabulary rule, verbatim from v1 S2.3: any vote whose `kind` is not one of the 12 plain
names (including NO FIT, Scope, Version, null) is dropped before the modal is taken; if fewer
than 2 in-vocabulary votes remain the item leaves the panel arm and the drop count is reported.

FORBIDDEN (S20): the panel may not filter, re-label, re-weight or drop any item from the
primary arm.  Nothing here writes to the primary arm.
"""
import collections, json, os, sys, time

import numpy as np

sys.path.insert(0, '/home/emoore/CIRISOntology/scratchpad/eigen2run')
import e2lib as L

PLAIN12 = ['Priorities', 'Rules', 'Manner', 'Identity', 'Confidence', 'Facts',
           'Circumstances', 'Process', 'Model', 'Structure', 'Premises', 'Record']
INV = {v: k for k, v in L.PLAIN.items()}

rows = L.load_e2()
auth = {r['id']: L.PLAIN[r['kind_target']] for r in rows}
diff = {r['id']: r['difficulty'] for r in rows}

votes = collections.defaultdict(dict)
raw_n = 0
offvocab = collections.Counter()
for line in open(os.path.join(L.OUT, 'panel_base.jsonl')):
    try:
        r = json.loads(line)
    except Exception:
        continue
    raw_n += 1
    k = r.get('kind')
    if isinstance(k, str):
        k = k.strip()
    if k in PLAIN12:
        votes[r['id']][r['model']] = k
    else:
        offvocab[str(k)] += 1

R = {'ts': time.strftime('%Y-%m-%dT%H:%M:%S'), 'raw_judgments': raw_n,
     'n_items_with_votes': len(votes),
     'offvocab_counts': dict(offvocab.most_common(12)),
     'offvocab_total': int(sum(offvocab.values()))}

modal, dropped = {}, []
for i, vv in votes.items():
    v = list(vv.values())
    if len(v) < 2:
        dropped.append(i)
        continue
    c = collections.Counter(v).most_common()
    if len(c) > 1 and c[0][1] == c[1][1]:
        # tie: no modal.  Recorded, and the item leaves the secondary label arm.
        dropped.append(i)
        continue
    modal[i] = c[0][0]
R['items_dropped_from_panel_arm'] = len(dropped) + (len(rows) - len(votes))
R['n_modal'] = len(modal)

# three-model Fleiss-style kappa on the in-vocabulary votes
items = [i for i in votes if len(votes[i]) == 3]
cats = PLAIN12
M = np.zeros((len(items), len(cats)))
for a, i in enumerate(items):
    for v in votes[i].values():
        M[a, cats.index(v)] += 1
nrate = 3
P_i = ((M ** 2).sum(1) - nrate) / (nrate * (nrate - 1))
p_j = M.sum(0) / (len(items) * nrate)
Pbar, Pe = float(P_i.mean()), float((p_j ** 2).sum())
R['fleiss_kappa_3model'] = (Pbar - Pe) / (1 - Pe)
R['kappa_n_items_all3'] = len(items)
R['PLANE_comparison_kappa'] = 0.687

agree = [modal[i] == auth[i] for i in modal]
R['modal_vs_authored_agreement'] = float(np.mean(agree))
for d in ('clear', 'hard'):
    a = [modal[i] == auth[i] for i in modal if diff[i] == d]
    R[f'agreement_{d}'] = {'n': len(a), 'rate': float(np.mean(a)) if a else None}

rec = [i for i in modal if modal[i] == 'Record']
R['record_false_positive'] = {'n': len(rec), 'rate_of_474': len(rec) / len(rows),
                              'staked_threshold': 0.05,
                              'FIRES': bool(len(rec) / len(rows) > 0.05),
                              'reading': ('a modal of Record on > 5% of artifact-only '
                                          'changes means annotators read the relation as a '
                                          'content category — a label-level finding, '
                                          'touching no geometry verdict')}
nofit = sum(1 for v in offvocab.elements() if str(v).upper().replace('_', ' ') == 'NO FIT')
R['modal_nofit_rate'] = {'raw_nofit_votes': int(offvocab.get('NO FIT', 0)),
                         'items_with_modal_nofit': 0,
                         'note': 'NO FIT is off-vocabulary and is dropped before the modal '
                                 '(v1 S2.3), so no item can carry a modal of NO FIT; the '
                                 'raw vote count is reported instead'}

conf = collections.Counter((auth[i], modal[i]) for i in modal if modal[i] != auth[i])
R['top_confusions'] = [{'authored': a, 'modal': m, 'n': n}
                       for (a, m), n in conf.most_common(15)]
pred = [('Premises', 'Facts'), ('Structure', 'Manner'), ('Model', 'Facts')]
tot_off = sum(conf.values())
inpred = sum(n for (a, m), n in conf.items()
             if (a, m) in pred or (m, a) in pred)
R['predicted_boundary_share'] = {'pairs': [list(p) for p in pred],
                                 'n_in_predicted': inpred, 'n_total_disagreements': tot_off,
                                 'share': inpred / tot_off if tot_off else None}

# secondary label arm: modal mapped back to internal names, Record-modal items excluded
# (there is no Record class in the 11-way geometry)
lab = {}
for i, m in modal.items():
    if m == 'Record':
        continue
    lab[i] = INV[m]
per = collections.Counter(lab.values())
R['secondary_arm'] = {'n_items': len(lab),
                      'per_class': dict(sorted(per.items())),
                      'min_class': min(per.values()) if per else 0,
                      'classes_present': len(per),
                      'V3_note': ('the secondary arm needs >= 12 per class in a fitting '
                                  'half, i.e. >= ~24 per class overall')}
L.atomic_json({'labels': lab}, os.path.join(L.OUT, 'panel_labels.json'))
L.atomic_json(R, os.path.join(L.OUT, 'panel_analysis.json'))
print(json.dumps({k: v for k, v in R.items() if k != 'top_confusions'}, indent=1))
