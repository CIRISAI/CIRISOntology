#!/usr/bin/env python3
"""Atlas v2 addendum — the four checks the first run made necessary.

Run AFTER atlas_v2.py. Nothing here changes a stake; each part answers an
objection the first run's own output raised:

  A1  the minimal counterexamples to B(i)/B(ii) used CONSTANT maps. Redo the
      search under REVERSIBILITY (r_loop and T bijections, gamma_loop a
      nontrivial permutation) — the non-degenerate minimal witnesses.
  A2  PART 7's implication scan ran on a RESTRICTED dynamics subfamily and did
      not filter constant consequents. Refilter, and re-verify every survivor
      on the full dynamics family.
  A3  the mode-only sector: cross-tabulate curvature against closure, and read
      off what D5's conjugacy condition FORCES there.
  A4  the adiabatic scaling's closed form (identified POST HOC from the p-sweep
      and then confirmed exactly), and the deterministic/stochastic split.
  A5  does closure transport down the Factors order — i.e. is a coarser
      context's view closed whenever a finer one's is?
"""
import itertools, math, random, functools
print = functools.partial(print, flush=True)
from collections import Counter
from atlas_v2_core import (Atlas, closed, closure_defect, rate_map, cond_entropy,
                           perm_family, build_view, build_reroot, pcomp, pinv,
                           cycle_type, H)

print()
print("#" * 78)
print("ADDENDUM")
print("#" * 78)

# ============================================================ A1
print()
print("=" * 78)
print("A1 — non-degenerate minimal counterexamples (reversible transport & dynamics)")
print("=" * 78)

def search_reversible(nX, k, want):
    Xs = list(range(nX))
    views = list(itertools.product(range(k), repeat=nX))
    perms = list(itertools.permutations(Xs))
    idn = tuple(Xs)
    for q1 in views:
        if len(set(q1)) < 2:
            continue                      # a one-reading view has no curvature
        for rl in perms:
            A0 = Atlas(Xs, q1, q1, q1, idn, idn, rl)   # placeholder for flatness
            flat = (A0.qt1p == q1)
            if want == 'i' and not flat:
                continue
            if want == 'ii' and flat:
                continue
            if rl == idn:
                continue          # identity loop is flat by fiat; excluded for BOTH
            for qt2 in views:
                for qt3 in views:
                    A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
                    if not A.legs_ok or not A.gloop_is_perm():
                        continue
                    if want == 'ii' and A.curvature_support() == 0:
                        continue
                    G = A.glued()
                    for T in perms:
                        cg, c1 = closed(G, T), closed(q1, T)
                        if want == 'ii' and cg and c1:
                            return dict(nX=nX, k=k, q1=q1, qt2=qt2, qt3=qt3, rloop=rl,
                                        T=T, gloop={f: A.gloop[f] for f in A.range1},
                                        support=A.curvature_support(),
                                        dG=closure_defect(G, T))
                        if want == 'i' and not (cg and c1):
                            return dict(nX=nX, k=k, q1=q1, qt2=qt2, qt3=qt3, rloop=rl,
                                        T=T, gloop={f: A.gloop[f] for f in A.range1},
                                        support=A.curvature_support(),
                                        dG=closure_defect(G, T))
    return None

for want, label in (
        ('ii', 'B(ii) nonzero curvature => closure failure   [reversible]'),
        ('i',  'B(i)  zero curvature   => closure            [reversible, r_loop != id]')):
    hit = None
    for nX in (2, 3, 4):
        for k in (2, 3):
            if k > nX:
                continue
            hit = search_reversible(nX, k, want)
            if hit:
                break
        if hit:
            break
    print(f"\n{label}")
    if hit:
        print(f"  KILLED, non-degenerately. Minimal witness |X|={hit['nX']}, k={hit['k']}:")
        for key in ('q1', 'qt2', 'qt3', 'rloop', 'T'):
            print(f"    {key:6s} = {hit[key]}")
        print(f"    gamma_loop = {hit['gloop']}  support={hit['support']}  "
              f"Delta_G = {hit['dG']:.4f}")
    else:
        print("  NO reversible counterexample up to |X|=4, k=3 — SURVIVES under reversibility.")

# reversible quantified envelope. |X|=4: a permutation can only move a reading by
# permuting q1's fibers, so EQUAL-SIZED fibers are needed and |X|=3 with k=2 can
# never read support > 0 (the same size artifact that emptied the first D2' probe).
Xs = list(range(4)); idn = tuple(Xs)
views4 = list(itertools.product(range(2), repeat=4))
perms4 = list(itertools.permutations(Xs))
mins = {}
for q1, qt2, qt3 in itertools.product(views4, repeat=3):
    for rl in perms4:
        A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
        if not A.legs_ok:
            continue
        s = A.curvature_support()
        G = A.glued()
        for T in perms4:
            d = round(closure_defect(G, T), 12)
            mins[s] = min(mins.get(s, 9e9), d)
print(f"\n  reversible envelope (|X|=4, k=2), min Delta_G by curvature support: "
      f"{ {s: round(v, 6) for s, v in sorted(mins.items())} }")

# ============================================================ A2
print()
print("=" * 78)
print("A2 — implication scan, refiltered and re-verified on the FULL dynamics family")
print("=" * 78)
n = 3
Xp, ip = perm_family(n)
P = list(itertools.permutations(range(n)))
ID = tuple(range(n))
allS = list(itertools.product(range(n), repeat=n))     # ALL maps S->S

rows = []
for betas in itertools.product(P, repeat=3):
    views = [build_view(Xp, ID, b) for b in betas]
    for eps in itertools.product((0, 1), repeat=3):
        for rhos3 in itertools.product(P, repeat=3):
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, sig[t], rhos3[t]) for t in range(3)]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            if not A.legs_ok:
                continue
            SD = any(b != ID for b in betas)
            MO = all(r == ID for r in rhos3)
            HOL = not A.held_loop()
            G = A.glued()
            for tau in ((0, 1), (1, 0)):
                for t0 in allS:
                    for t1 in allS:
                        T = tuple(ip[(tau[m], (t0 if m == 0 else t1)[s])] for (m, s) in Xp)
                        h = rate_map(A.q1, T)
                        rows.append(dict(
                            HOL=HOL, SD=SD, MODEONLY=MO,
                            EQV=all(T[A.rloop[i]] == A.rloop[T[i]] for i in range(len(Xp))),
                            C1=h is not None,
                            HELD1=tuple(A.q1[T[i]] for i in range(len(Xp))) == A.q1,
                            CG=closed(G, T),
                            COMM=(h is not None and
                                  all(A.gloop[h[f]] == h[A.gloop[f]] for f in A.range1)),
                        ))
feats = ['HOL', 'SD', 'MODEONLY', 'EQV', 'C1', 'HELD1', 'CG', 'COMM']
print(f"models scanned (full dynamics family): {len(rows)}")
const = {f for f in feats if len({r[f] for r in rows}) == 1}
print(f"constant features dropped (vacuous consequents): {sorted(const) or 'none'}")
live = [f for f in feats if f not in const]
lits = [(f, s) for f in live for s in (True, False)]
singles = []
for (fa, sa) in lits:
    ante = [r for r in rows if r[fa] == sa]
    if not ante:
        continue
    for (fb, sb) in lits:
        if fa == fb:
            continue
        if all(r[fb] == sb for r in ante):
            singles.append((f"{'' if sa else '¬'}{fa}", f"{'' if sb else '¬'}{fb}", len(ante)))
print("exact single-antecedent implications:")
for a, b, m in sorted(singles):
    print(f"  {a:9s} => {b:9s}  (support {m})")
sset = {(a, b) for a, b, _ in singles}
print("exact two-antecedent implications (neither half alone suffices):")
pairs = []
for (fa, sa), (fb, sb) in itertools.combinations(lits, 2):
    if fa == fb:
        continue
    ante = [r for r in rows if r[fa] == sa and r[fb] == sb]
    if len(ante) < 50:
        continue
    A_ = f"{'' if sa else '¬'}{fa}"; B_ = f"{'' if sb else '¬'}{fb}"
    for (fc, sc) in lits:
        if fc in (fa, fb):
            continue
        C_ = f"{'' if sc else '¬'}{fc}"
        if (A_, C_) in sset or (B_, C_) in sset:
            continue
        if all(r[fc] == sc for r in ante):
            pairs.append((A_, B_, C_, len(ante)))
for a, b, c, m in sorted(pairs):
    print(f"  {a} & {b:9s} => {c:9s}  (support {m})")

# ============================================================ A3
print()
print("=" * 78)
print("A3 — the mode-only sector: what D5's conjugacy condition FORCES")
print("=" * 78)
for n in (3, 4):
    Xp, ip = perm_family(n)
    P = list(itertools.permutations(range(n)))
    ID = tuple(range(n))
    Tmode = tuple(ip[(1 - m, s)] for (m, s) in Xp)          # pure mode advance
    tab = Counter()
    invol = Counter()
    nflip_tab = Counter()
    for betas in itertools.product(P, repeat=3):
        views = [build_view(Xp, ID, b) for b in betas]
        for eps in itertools.product((0, 1), repeat=3):
            sig = [((1, 0) if e else (0, 1)) for e in eps]
            rr = [build_reroot(Xp, ip, s, ID) for s in sig]
            A = Atlas(Xp, views[0], views[1], views[2], rr[0], rr[1], rr[2])
            if not A.legs_ok:
                continue
            HOL = not A.held_loop()
            allclosed = all(closed(v, Tmode) for v in views)
            tab[(HOL, allclosed)] += 1
            invol[tuple(sorted(cycle_type(b) for b in betas))] += 1
            nflip_tab[(sum(eps), HOL)] += 1
    print(f"\nn={n}, transportable mode-only atlases: {sum(tab.values())}")
    print(f"  (curvature, all three views closed under the mode-advance):")
    for kk in sorted(tab):
        print(f"    HOL={kk[0]!s:5s} allClosed={kk[1]!s:5s} : {tab[kk]}")
    print(f"  cycle types of (beta_1,beta_2,beta_3) that survive transportability:")
    for kk, vv in sorted(invol.items()):
        print(f"    {kk} : {vv}")
    print(f"  curvature by number of mode-flipping edges: "
          f"{dict(sorted(nflip_tab.items()))}")

# ============================================================ A4
print()
print("=" * 78)
print("A4 — the adiabatic closed form (identified post hoc, then confirmed exactly)")
print("=" * 78)
n = 3
Xp, ip = perm_family(n)
def stoch_defect(beta, p):
    v = build_view(Xp, tuple(range(n)), beta)
    joint = Counter()
    for i, (m, s) in enumerate(Xp):
        for mm, pr in ((m, 1 - p), (1 - m, p)):
            if pr <= 0:
                continue
            joint[(v[i], v[ip[(mm, s)]])] += pr
    tot = sum(joint.values())
    marg = Counter()
    for (a, b), c in joint.items():
        marg[a] += c
    return (H([c for c in joint.values()]) - H([c for c in marg.values()]))
def H2(p):
    if p in (0.0, 1.0):
        return 0.0
    return -p * math.log(p) - (1 - p) * math.log(1 - p)
def predicted(beta, p):
    """Closed form identified POST HOC from the p-sweep, then checked on every beta.

    Fiber of the reading f is {(0,f), (1, beta^-1 f)}, each half the fiber. One step:
      * beta f = f            -> the reading is deterministic          : 0
      * beta^2 f = f != beta f-> two outcomes (1-p, p)                 : H2(p)
      * otherwise             -> three outcomes (1-p, p/2, p/2)        : H2(p) + p ln2
    """
    k = len(beta)
    tot = 0.0
    for f in range(k):
        bf = beta[f]
        if bf == f:
            continue
        tot += H2(p) + (0.0 if beta[bf] == f else p * math.log(2))
    return tot / k

print(f"{'beta':>12} {'cycles':>10} {'p':>7} {'measured':>12} {'predicted':>12} {'match':>7}")
allmatch = True
for n_ in (3, 4):
    Xp, ip = perm_family(n_)
    for beta in itertools.permutations(range(n_)):
        for p in (0.001, 0.01, 0.05, 0.25, 0.5):
            v = build_view(Xp, tuple(range(n_)), beta)
            joint = Counter()
            for i, (m, s) in enumerate(Xp):
                for mm, pr in ((m, 1 - p), (1 - m, p)):
                    joint[(v[i], v[ip[(mm, s)]])] += pr
            marg = Counter()
            for (a, b), c in joint.items():
                marg[a] += c
            d = H([c for c in joint.values()]) - H([c for c in marg.values()])
            ok = abs(d - predicted(beta, p)) < 1e-12
            allmatch &= ok
            if n_ == 3 and p in (0.001, 0.5):
                print(f"{str(beta):>12} {str(cycle_type(beta)):>10} {p:7.3f} "
                      f"{d:12.6f} {predicted(beta, p):12.6f} {str(ok):>7}")
print(f"  closed form matches on ALL beta for n=3 and n=4, five p each: {allmatch}")
print("  => the slow mode does NOT suppress the defect linearly: H2(p) ~ p*ln(1/p),")
print("     so a state-dependent fibration leaks at O(p log 1/p), ABOVE linear order.")
print("  => an INVOLUTIVE mismatch, exactly closed under the DETERMINISTIC mode-flip")
print("     (D7), still carries a nonzero defect under the STOCHASTIC one: only the")
print("     FIXED POINTS of beta cost nothing.")

# ============================================================ A5
print()
print("=" * 78)
print("A5 — does closure transport down the Factors order?")
print("=" * 78)
witness = None
for nX in (2, 3, 4):
    Xs = list(range(nX))
    views = list(itertools.product(range(nX), repeat=nX))
    maps = list(itertools.product(Xs, repeat=nX))
    tot = inherited = 0
    for q1 in views:
        for g in itertools.product(range(nX), repeat=nX):
            qt2 = tuple(g[v] for v in q1)
            if len(set(qt2)) == len(set(q1)):
                continue                       # not a strict coarsening
            for T in maps:
                if not closed(q1, T):
                    continue
                tot += 1
                if closed(qt2, T):
                    inherited += 1
                elif witness is None:
                    witness = dict(nX=nX, q1=q1, g=g, qt2=qt2, T=T,
                                   d1=closure_defect(q1, T), d2=closure_defect(qt2, T))
    print(f"|X|={nX}: (q1 closed, qt2 a STRICT coarsening of q1): {tot} cases, "
          f"coarsening also closed in {inherited} ({100*inherited/max(tot,1):.1f}%)")
    if witness:
        break
print(f"  minimal witness that closure does NOT descend: {witness}")
print("  => a tier's autonomy is NOT inherited by its own coarsenings; each context")
print("     of a transportable atlas owes its own closure reading.")


# ============================================================ A6
print()
print("=" * 78)
print("A6 — B(iv) OUTSIDE the permutation family, and which A2 survivors are artifacts")
print("=" * 78)
# The Lean target must be general, so re-test EQV & C1 => COMM on arbitrary finite
# data, and test the other interesting A2 survivor (not-HOL & C1 => EQV) for
# artifacthood. |X|=3 is EXHAUSTIVE; |X|=4 is a labelled random SAMPLE (the full
# class there is ~1e12 models).
def a6(nX, sample=None, seed=7):
    Xs = list(range(nX)); idn = tuple(Xs)
    views = list(itertools.product(range(nX), repeat=nX))
    maps = list(itertools.product(Xs, repeat=nX))
    n_biv = ok_biv = n_art = ok_art = 0
    art_witness = biv_witness = None
    if sample:
        rng = random.Random(seed)
        it = ((rng.choice(views), rng.choice(views), rng.choice(views),
               rng.choice(maps), rng.choice(maps)) for _ in range(sample))
    else:
        it = ((q1, qt2, qt3, rl, T)
              for q1 in views for qt2 in views for qt3 in views
              for rl in maps for T in maps)
    for q1, qt2, qt3, rl, T in it:
        A = Atlas(Xs, q1, qt2, qt3, idn, idn, rl)
        if not A.legs_ok:
            continue
        h = rate_map(q1, T)
        if h is None:
            continue
        eqv = all(T[rl[i]] == rl[T[i]] for i in range(nX))
        if eqv:
            n_biv += 1
            good = all(A.gloop[h[f]] == h[A.gloop[f]] for f in A.range1)
            ok_biv += good
            if not good and biv_witness is None:
                biv_witness = dict(q1=q1, qt2=qt2, qt3=qt3, rloop=rl, T=T)
        if A.held_loop():
            n_art += 1
            if eqv:
                ok_art += 1
            elif art_witness is None:
                art_witness = dict(q1=q1, qt2=qt2, qt3=qt3, rloop=rl, T=T)
    tag = "|X|=%d" % nX + (" (random sample of %d)" % sample if sample else " (exhaustive)")
    print("%s: B(iv)  EQV & C1 => COMM : %d/%d  %s"
          % (tag, ok_biv, n_biv,
             "CONFIRMED" if ok_biv == n_biv else "*** FAILS OUTSIDE THE FAMILY ***"))
    if biv_witness:
        print("    B(iv) FAILURE witness: %s" % biv_witness)
    print("        A2 survivor  not-HOL & C1 => EQV : %d/%d  %s"
          % (ok_art, n_art,
             "holds" if ok_art == n_art else "FAILS - permutation-family ARTIFACT"))
    if art_witness:
        print("    artifact witness: %s" % art_witness)

a6(3)
a6(4, sample=400000)
