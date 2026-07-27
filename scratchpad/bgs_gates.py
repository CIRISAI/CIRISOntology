#!/usr/bin/env python3
"""
bgs_gates.py -- the mechanized half of the SKY_BGS_PREREG.md gate battery.

GATES.md's closing harvest registers twelve gates minted by the BOSS run and its refutation,
with the standing consequence that all twelve are prerequisites for the next survey-class run
and that THE FIRST SEVEN ARE MECHANIZABLE IN THE PIPELINE DRIVER ITSELF.  This is that driver.

    P1  valve floor                     the null carries shot-noise NON-Gaussianity
    P2  null-construction sweep         >= 2 defensible nulls per row, spread quoted
    P3  directional claims are measured a "conservative direction" is TESTED, not argued
    P4  dispersion sweep                eps swept; eps_crit and the margin reported
    P5  same null both sides            prediction and data scored against identical nulls
    P6  outcome completeness            the emitted verdict is one of the enumerated outcomes
    P7  gate discharge before unblind   NO unblind while any VOID gate is undischarged

require_discharged() reads every artifact OFF DISK and raises.  Nothing here is satisfied by
recollection -- that is the entire content of P7, which was minted because the BOSS campaign's
pre-registered section-7.5 weight-variation VOID gate was never run and its results document's
gate register was headed "all passed" without listing it.

DOCIMASIA (GATES.md lifecycle, "Validated"): a gate is not validated by being written.  It
needs a PLUMB LINE -- a stored kept taint it catches -- and a DYE TEST -- a known-true
reference it passes.  Both are supplied by `python3 bgs_gates.py`, which runs the battery
against four states, three of them real and stored in this repository:

    view 0  the Stage 6 reading BEFORE Amendment 5   -- no valve floor at all; P1's kept taint
    view 1  the campaign AS SHIPPED at its unblind   -- the kept taint for P2, P3, P7
    view 2  the campaign PLUS the refuter's own runs -- what the refuter actually closed (P4)
    view 3  a synthetic fully-discharged campaign    -- the known-true reference; all must clear

A gate that fires on every view is not discriminating -- it spends standing it never earned
(GATES.md design rule 2) -- and a gate that fires on none is not a gate.  The matrix is printed
so the difference is visible, and a gate is labelled VALIDATED only if it does both.

Two things this docimasia caught in the gates themselves, recorded rather than quietly fixed:

  * P3 initially CLEARED the shipped BOSS state, because that run records eight clipped
    fractions (0.3682, 0.3689, 0.3696, ...) which are eight draws of ONE construction.  Counting
    distinct values mistook realisation jitter for a varied mechanism.  P3 now clusters.
  * P2 still fires on view 2, and that is correct: the refuter ran its second null family on the
    four folded primary rows, not on all 26.  22 rows carry a single construction to this day.

This file reads no survey data and never will; it reads JSON summaries only.
"""
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))

# The outcome set enumerated in SKY_BGS_PREREG.md section 9.  P6 asserts the driver's emitted
# tag is one of these.  Outcome (e) exists because the BOSS unblind produced a reading that fit
# no pre-registered outcome and the document had nowhere to put it.
OUTCOMES = ('a_confirmation', 'c_null_above_floors', 'd_void', 'e_not_decomposed')

PASS, FIRE, ABSENT = 'PASS', 'FIRE', 'ABSENT'


class GateUndischarged(RuntimeError):
    pass


class CampaignView:
    """Everything the mechanized gates need, loaded from artifacts.  A field left None means
    the artifact does not exist -- which is a FIRE, not a pass by default."""

    def __init__(self, name):
        self.name = name
        self.rows = []            # [{cap,R,b,geom, valve, targets:{tag: value}, sigma}]
        self.clip_values = None   # [float] distinct clipped fractions the null was run at
        self.clip_floor = None    # [(clip, floor)] for the SIGN of d(floor)/d(clip)
        self.eps_values = None    # [float] super-Poisson dispersions swept
        self.eps_targets = None   # {(row_key): {eps: target}}
        self.kappa = None         # {cap: <w^2>/<w>} measured off the catalogue
        self.null_signature = None  # {'mock': str, 'data': str}
        self.outcome_tag = None
        self.weight_verdict = None  # {'scheme': max |shift/sigma|} for GATE W / W'

    def row_keys(self):
        return [(r['cap'], r['R'], r['b'], r['geom']) for r in self.rows]


def _finite(x):
    return isinstance(x, (int, float)) and math.isfinite(x)


# ---------------------------------------------------------------- the seven gates

def p1_valve_floor(v):
    """The null must carry shot-noise NON-Gaussianity, not only its power.  Anchor: the
    uncashable 61.7 sigma, where the Stage 6 reading was (gravity)+(valve), unseparated."""
    if not v.rows:
        return ABSENT, 'no rows'
    bad = [k for k, r in zip(v.row_keys(), v.rows) if not _finite(r.get('valve'))]
    if bad:
        return FIRE, f'{len(bad)} row(s) carry no finite valve floor'
    n = len(v.rows)
    return PASS, f'valve floor measured on all {n} rows'


def p2_null_sweep(v):
    """Every surrogate-normalised reading reported under >= 2 defensible null constructions;
    the spread is a quoted systematic.  Anchor: refuter A9 cut the target 30-52 %."""
    if not v.rows:
        return ABSENT, 'no rows'
    thin = [k for k, r in zip(v.row_keys(), v.rows)
            if len([t for t in r.get('targets', {}).values() if _finite(t)]) < 2]
    if thin:
        return FIRE, (f'{len(thin)}/{len(v.rows)} row(s) carry a single null construction; '
                      'the reading is construction-dependent and unquantified')
    spreads = []
    for r in v.rows:
        t = [x for x in r['targets'].values() if _finite(x)]
        spreads.append((max(t) - min(t)) / max(abs(max(t)), 1e-300))
    return PASS, (f'>=2 nulls on all {len(v.rows)} rows; spread '
                  f'{min(spreads):.3f}-{max(spreads):.3f} of the larger target')


def p3_direction_measured(v):
    """Any 'conservative direction' / 'lower bound' argument is TESTED by varying the
    mechanism, never argued from plausibility.  Anchor: Amendment 5 section A5.3's lower-bound
    framing was falsified IN SIGN -- less clipping produced a LARGER floor, not a smaller one.

    The bar is >= 3 values, per SKY_BGS_PREREG.md P3: two points can falsify a sign but cannot
    characterise the response, and a directional claim is a claim about the response."""
    if not v.clip_values:
        return ABSENT, 'the null mechanism was never varied; any directional claim is argued'
    # A DESIGNED variation, not realisation jitter.  Caught by this gate's own docimasia: the
    # BOSS campaign's eight nulls record eight clipped fractions (0.3682, 0.3689, 0.3696, ...)
    # that differ only in the fourth decimal.  Counting distinct values cleared the gate on a
    # run that never varied the mechanism at all.  Values are therefore CLUSTERED, and the
    # variation must also be material end to end.
    vals = sorted(set(v.clip_values))
    clusters = [[vals[0]]]
    for x in vals[1:]:
        (clusters[-1].append(x) if x - clusters[-1][-1] < 0.20 * max(clusters[-1][-1], 1e-12)
         else clusters.append([x]))
    n, span = len(clusters), vals[-1] / max(vals[0], 1e-12)
    if n < 3 or span < 1.5:
        return FIRE, (f'mechanism varied at {n} distinct level(s) spanning x{span:.2f} '
                      f'({len(vals)} raw values); two points can falsify a sign but cannot '
                      'characterise the response, and jitter is not variation')
    sign = ''
    if v.clip_floor and len(v.clip_floor) >= 2:
        cf = sorted(v.clip_floor)
        d = cf[-1][1] - cf[0][1]
        sign = f'; d(floor)/d(clip) {"+" if d > 0 else "-"}'
    return PASS, f'mechanism varied at {n} values{sign}'


def p4_dispersion_sweep(v):
    """Poisson nulls swept to literature-plausible super-Poisson dispersion; report eps_crit
    and the margin.  Anchor: BOSS margin 1.3-1.7x, and the catalogue's OWN weights were already
    13-15 % super-Poisson while the null carried none of it.

    The gate COMPUTES eps_crit from the sweep rather than trusting a reported field."""
    if not v.eps_values or not v.eps_targets:
        return ABSENT, 'no dispersion sweep'
    if len(set(v.eps_values)) < 3:
        return FIRE, f'only {len(set(v.eps_values))} dispersion value(s) swept'
    if not v.kappa:
        return FIRE, "the catalogue's own weight super-Poissonity (kappa) was never measured"
    crits = {}
    for key, curve in v.eps_targets.items():
        s = next((r.get('sigma') for r in v.rows
                  if (r['cap'], r['R'], r['b'], r['geom']) == key), None)
        if not _finite(s) or s <= 0:
            continue
        pts = sorted((e, t / s) for e, t in curve.items() if _finite(t))
        crit = None
        for (e0, d0), (e1, d1) in zip(pts, pts[1:]):
            if d0 >= 5.0 > d1:
                crit = e0 + (d0 - 5.0) * (e1 - e0) / (d0 - d1)
                break
        if crit is None and pts and pts[0][1] < 5.0:
            crit = 0.0
        crits[key] = crit
    got = [c for c in crits.values() if c is not None]
    if not got:
        return FIRE, 'sweep present but eps_crit not computable on any row'
    k = ', '.join(f'{c}={x:.3f}' for c, x in sorted(v.kappa.items()))
    return PASS, (f'eps_crit computed on {len(got)}/{len(crits)} row(s), '
                  f'range {min(got):.2f}-{max(got):.2f}; measured kappa {k}')


def p5_same_null_both_sides(v):
    """Prediction and data scored against IDENTICALLY constructed nulls.  Anchor: the 30 %-low
    apples-to-oranges near-miss, dodged on the record by care rather than by construction."""
    if not v.null_signature:
        return ABSENT, ('no null-construction signature recorded; the mock side and the data '
                        'side were not mechanically verified to share a null')
    m, d = v.null_signature.get('mock'), v.null_signature.get('data')
    if not m or not d:
        return FIRE, 'null signature incomplete'
    if m != d:
        return FIRE, f'null signature MISMATCH mock={m} data={d}'
    return PASS, f'null signature identical both sides ({m})'


def p6_outcome_completeness(v):
    """Before unblinding, the emitted verdict must be one of the enumerated outcomes.  Anchor:
    the BOSS unblind produced a large, well-controlled reading whose decomposition had not been
    performed -- an outcome the pre-registration had not enumerated and could not name."""
    if v.outcome_tag is None:
        return ABSENT, ('no outcome tag emitted; a reading that fits no enumerated outcome is '
                        'exactly the failure this gate was minted from')
    if v.outcome_tag not in OUTCOMES:
        return FIRE, f'outcome {v.outcome_tag!r} is not in the enumerated set {OUTCOMES}'
    return PASS, f'outcome {v.outcome_tag!r} is enumerated'


def p7_discharge_before_unblind(v, prior):
    """NO unblind while any pre-registered VOID gate is undischarged; discharge is verified
    against the record, not memory.  Anchor: section 7.5's weight-variation VOID gate was never
    run, the reading was sensitive to that channel at 2.5-2.9 sigma, and the results document's
    gate register was headed 'all passed' without listing it."""
    unresolved = [g for g, (s, _) in prior.items() if s != PASS]
    if v.weight_verdict is None:
        unresolved.append('GATE W/W-prime')
    if unresolved:
        return FIRE, 'undischarged at the unblind boundary: ' + ', '.join(unresolved)
    return PASS, 'every mechanized prerequisite discharged, weight gate run'


GATES = (('P1', 'valve floor', p1_valve_floor),
         ('P2', 'null-construction sweep', p2_null_sweep),
         ('P3', 'directional claims measured', p3_direction_measured),
         ('P4', 'dispersion sweep', p4_dispersion_sweep),
         ('P5', 'same null both sides', p5_same_null_both_sides),
         ('P6', 'outcome completeness', p6_outcome_completeness))


def run_battery(v):
    out = {}
    for tag, name, fn in GATES:
        s, d = fn(v)
        out[tag] = (s, d)
    s, d = p7_discharge_before_unblind(v, out)
    out['P7'] = (s, d)
    return out


def require_discharged(v, stage='unblind'):
    """The unblind entry point calls this.  It RAISES.  It does not warn."""
    res = run_battery(v)
    bad = {g: r for g, r in res.items() if r[0] != PASS}
    if bad:
        lines = [f'  {g}  {s}  {d}' for g, (s, d) in sorted(bad.items())]
        raise GateUndischarged(
            f'{len(bad)} prerequisite(s) undischarged at stage {stage!r}:\n' + '\n'.join(lines))
    return res


# ---------------------------------------------------------------- BOSS adapters (dye test)

def _boss_view(with_refuter):
    """Build the campaign view from the BOSS artifacts actually on disk.

    view 1 (with_refuter=False) is the state AS SHIPPED at the BOSS unblind: one null (N2),
    one clipping level, no dispersion sweep, no weight-variation run, no null signature, no
    outcome tag.  That is the kept taint.

    view 2 (with_refuter=True) adds what the refuter ran afterwards: the N2m/N2mw null family,
    the eps dispersion sweep, the measured kappa, and the A2 weight-variation.
    """
    v = CampaignView('BOSS as shipped' if not with_refuter else 'BOSS + refuter')
    verdict = json.load(open(f'{HERE}/sky_stage7_verdict.json'))
    valve = json.load(open(f'{HERE}/sky_stage7_valve.json'))

    # sigma per row, from the campaign's own 16-mock ensemble, via the refuter's report which
    # records it row by row (the campaign's sigma is the one every quoted significance used).
    sig = {}
    for cap in ('SGC', 'NGC'):
        p = f'{HERE}/refuter_a2_report_{cap}.json'
        if os.path.exists(p):
            for r in json.load(open(p)):
                sig[(cap, float(r['R']), int(r['b']), 'folded')] = r.get('sigma')

    for r in verdict:
        key = (r['cap'], float(r['R']), int(r['b']), r['geom'])
        v.rows.append(dict(cap=r['cap'], R=float(r['R']), b=int(r['b']), geom=r['geom'],
                           valve=r.get('valve'), sigma=sig.get(key),
                           targets={'N2pipe': r.get('target')}))

    # The campaign ran every null at ONE clipping level -- the clipped fractions recorded in
    # sky_stage7_valve.json are eight draws of the same construction, not a variation of it.
    v.clip_values = [round(c, 4) for c in valve['SGC']['clipped']]

    if not with_refuter:
        return v

    ana = json.load(open(f'{HERE}/refuter_analyze.json'))
    eps_t, eps_v = {}, set()
    for cap in ('SGC', 'NGC'):
        blk = ana.get(cap)
        if not blk:
            continue
        for r in blk.get('rows', []):
            key = (r['cap'], float(r['R']), int(r['b']), 'folded')
            tag = r['null']
            for row in v.rows:
                if (row['cap'], row['R'], row['b'], row['geom']) == key:
                    row['targets'][tag] = r.get('target')
            if tag.startswith('N2eps'):
                e = float(tag[5:])
                eps_v.add(e)
                eps_t.setdefault(key, {})[e] = r.get('target')
            elif tag == 'N2mw':
                eps_t.setdefault(key, {})[0.0] = r.get('target')
    v.eps_values, v.eps_targets = sorted(eps_v | {0.0}), eps_t

    # The refuter DID vary the clipping mechanism: N2m drops the clipped fraction from 37 % to
    # 3.5 % and the floor went UP, which is what falsified the lower-bound framing in sign.
    v.clip_values = sorted(set(v.clip_values) | {0.035})
    v.clip_floor = [(0.369, 3.03e-4), (0.035, 4.35e-4)]

    kap = {}
    for cap, f in (('SGC', 'refuter_nulls_SGC.json'), ('NGC', 'refuter_fast_NGC.json')):
        p = f'{HERE}/{f}'
        if os.path.exists(p):
            kap[cap] = json.load(open(p)).get('kappa')
    v.kappa = kap or None

    wv = {}
    for cap in ('SGC', 'NGC'):
        p = f'{HERE}/refuter_a2_report_{cap}.json'
        if os.path.exists(p):
            for r in json.load(open(p)):
                s = abs(r.get('shift_over_sigma') or 0.0)
                wv[r['scheme']] = max(wv.get(r['scheme'], 0.0), s)
    v.weight_verdict = wv or None
    return v


def _boss_view_stage6():
    """P1's plumb line: the BOSS Stage 6 reading AS FIRST TAKEN, before Amendment 5 existed.
    Its target is I(data) - I(plain phase-randomised surrogate), with NO valve floor anywhere
    in it -- the reading that was cashed at 61.7 sigma and could not be cashed, because it was
    (gravity)+(valve) unseparated.  P1 must fire on this and does not fire on the post-
    Amendment-5 artifact, which is the whole distinction the gate exists to draw."""
    v = CampaignView('BOSS Stage 6, pre-Amendment-5')
    d = json.load(open(f'{HERE}/sky_stage6_data.json'))
    for key, blk in d.items():
        cap, tag = key.split('|')
        if tag != 'full':
            continue
        res = blk['res']
        for R, rec in res['mock'].items():
            for b, bb in rec['b'].items():
                for geom, e in bb.items():
                    if not e.get('occupancy_pass'):
                        continue
                    s = res['surr'][R]['b'][b][geom]
                    v.rows.append(dict(cap=cap, R=float(R), b=int(b), geom=geom,
                                       valve=None, sigma=None,
                                       targets={'N1': e['I'] - s['I']}))
    return v


def _synthetic_discharged_view():
    """The known-true reference: a campaign in which every mechanized prerequisite HAS been
    discharged.  Without it P5 and P6 would have a plumb line and no dye test, and a gate that
    has never been shown to clear is sitting in `proposed` while being used as though
    validated -- the exact state GATES.md's lifecycle section says this repository most often
    ships.  These numbers describe no measurement; they exercise the battery."""
    v = CampaignView('synthetic, fully discharged')
    for b in (4, 6, 8):
        v.rows.append(dict(cap='NGC', R=15.0, b=b, geom='folded', valve=1.0e-4, sigma=5.0e-5,
                           targets={'N_A': 5.0e-4, 'N_B': 4.2e-4, 'N_C': 3.0e-4}))
    v.clip_values = [0.02, 0.10, 0.35]
    v.clip_floor = [(0.02, 4.4e-4), (0.10, 3.9e-4), (0.35, 3.0e-4)]
    v.eps_values = [0.0, 0.25, 0.5, 1.0, 2.0]
    v.eps_targets = {(r['cap'], r['R'], r['b'], r['geom']):
                     {0.0: 5.0e-4, 0.25: 4.6e-4, 0.5: 4.0e-4, 1.0: 3.0e-4, 2.0: 1.0e-4}
                     for r in v.rows}
    v.kappa = {'NGC': 1.04}
    v.null_signature = {'mock': 'N_B/v1/sha:deadbeef', 'data': 'N_B/v1/sha:deadbeef'}
    v.outcome_tag = 'a_confirmation'
    v.weight_verdict = {'default': 0.0, 'pip': 0.4}
    return v


def dye_test():
    v0 = _boss_view_stage6()
    v1, v2 = _boss_view(False), _boss_view(True)
    v3 = _synthetic_discharged_view()
    r0, r1, r2 = run_battery(v0), run_battery(v1), run_battery(v2)
    r3 = run_battery(v3)
    print('=' * 100)
    print('DOCIMASIA for the mechanized gates -- run against the BOSS campaign\'s own artifacts')
    print('  view 0 : the Stage 6 reading BEFORE Amendment 5 -- no valve floor at all')
    print('  view 1 : the campaign AS SHIPPED at its unblind (the kept taint)')
    print('  view 2 : the same campaign PLUS the refuter\'s own runs')
    print('  view 3 : a synthetic campaign with every prerequisite discharged (known-good)')
    print('=' * 100)
    print(f'{"":4} {"gate":32} {"pre-A5":>8} {"shipped":>8} {"+refut":>7} {"good":>6}   state')
    for tag, name, _ in list(GATES) + [('P7', 'gate discharge before unblind', None)]:
        z, a, b, c = r0[tag][0], r1[tag][0], r2[tag][0], r3[tag][0]
        # VALIDATED requires both halves: it catches the kept taint AND clears a known-true
        # reference.  Anything else is `proposed`, and is labelled so rather than rounded up.
        caught = (a != PASS) or (z != PASS)
        state = ('VALIDATED' if (caught and c == PASS) else
                 'proposed (no plumb line)' if c == PASS else
                 'BROKEN -- clears nothing')
        print(f'{tag:4} {name:32} {z:>8} {a:>8} {b:>7} {c:>6}   {state}')
    print()
    for label, r in (('VIEW 0  (pre-Amendment-5)', r0), ('VIEW 1  (as shipped)', r1),
                     ('VIEW 2  (+ refuter)', r2), ('VIEW 3  (known-good)', r3)):
        print(label)
        for tag in ('P1', 'P2', 'P3', 'P4', 'P5', 'P6', 'P7'):
            s, d = r[tag]
            print(f'   {tag} {s:<7} {d}')
        print()
    print("VALIDATED = the gate catches the kept taint AND clears the known-true reference.")

    print('A battery that fired on every view would be spending standing it never earned '
          '(GATES.md design rule 2).')
    print()
    print('require_discharged() against view 1 -- this is what the unblind entry point does:')
    try:
        require_discharged(v1)
        print('   NO RAISE -- THE DRIVER IS BROKEN, the shipped BOSS state must not clear')
    except GateUndischarged as e:
        print('   RAISED, correctly:')
        for ln in str(e).splitlines():
            print('     ' + ln)
    return r1, r2


if __name__ == '__main__':
    dye_test()
    sys.exit(0)
