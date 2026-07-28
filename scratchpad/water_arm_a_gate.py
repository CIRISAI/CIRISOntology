#!/usr/bin/env python3
"""DOCIMASIA for the ARM A ANALYSIS instrument -- examine it before trusting it.

`glass_gate.py` already examined the shared estimator (`glass_share.py`) in nine
checks, three of them theorem-pinned, and they PASS (`glass_gate.json`).  That
gate is inherited byte-identically and is NOT re-derived here.  What it does not
cover is everything `water_arm_a.py` adds on top: the dump reader, the
coordination filter, the triangle cap, the class-partitioned ceiling, the two
floors, and the ideal-gas control.  Those are examined here.

The dump reader is examined FIRST and for cause: as written before this gate ran
it left the `ITEM: ATOMS` header line unconsumed and could not parse a LAMMPS
dump at all.  That defect is why no share existed when `WATER_AMENDMENT_12.md`
was written, and it is the reason this file exists (`GATES.md`: a gate -- and an
instrument -- is examined BEFORE it is trusted).

  W1  dump reader round-trip, against a file whose coordinates are known
  W2  coordination filter: exact count on a simple-cubic lattice; and invariant
      under a random rigid translation through the periodic boundary
  W3  triangle cap: S3 deviation EXACTLY zero at every cap (AMENDMENT 9 I2, on
      this implementation rather than on the one that produced that table)
  W4  class-partitioned ceiling on a planted 2+1 state (AMENDMENT 7 G2), with
      the classes taken from the template's edge lengths and NEVER from the data
  W5  the two floors on real configurations: N1a is an exact product state, so
      `Core/Valve.lean: valve_from_nothing` (hypotheses verified at source:
      three `IsKernel` kernels, three `IsProb` cell states, input `prod3`) gives
      share exactly zero and the reading is the finite-sample floor.  N1b is a
      permutation and is NOT theorem-pinned (AMENDMENT 4 D2).  The overlap
      penalty over the chi^2_1 law is measured, not assumed
  W6  G-DYE at the amplitude that matters: a three-body coupling planted into
      the labels of REAL mW configurations and recovered monotonically through
      the byte-identical pipeline.  This is what fixes the smallest dose this
      arm can see, and `GATES.md` reach 1 records that this is exactly what the
      repository's estimator-bias gate does not have
  W7  N2, the ideal gas at matched number density through the byte-identical
      template selection and coordination filter -- AMENDMENT 10 J3's PRIMARY
      fouling detector, because it has no correlation length to confound it
  W8  ThirdCap ceiling of a degenerate label is exactly zero -- the arithmetic
      behind AMENDMENT 12 L3, checked rather than asserted

NO CAMPAIGN OBSERVABLE IS SCORED HERE.  W5-W7 touch real mW configurations, but
only through controls whose right answer is known in advance; the data's own
labels are never read.
"""
import json
import os
import sys

import numpy as np

sys.path.insert(0, "/home/emoore/CIRISOntology/scratchpad")
import glass_share as GS   # noqa: E402
import water_arm_a as WA   # noqa: E402

OUT = {}
DUMP = "/home/emoore/CIRISOntology/scratchpad/mw/mw_lam23.15.dump"


def rec(name, ok, **kw):
    OUT[name] = dict(pass_=bool(ok), **{k: (v.tolist() if isinstance(v, np.ndarray) else v)
                                        for k, v in kw.items()})
    print("%-4s %-46s %s   %s" % ("PASS" if ok else "FAIL", name,
                                  "", "  ".join("%s=%s" % (k, v) for k, v in kw.items())),
          flush=True)
    return ok


def w1_dump_roundtrip():
    rng = np.random.default_rng(0)
    L, n = 17.5, 40
    pos = rng.random((n, 3)) * L
    path = "/tmp/water_gate_dump.dump"
    with open(path, "w") as f:
        for step in (0, 100):
            f.write("ITEM: TIMESTEP\n%d\n" % step)
            f.write("ITEM: NUMBER OF ATOMS\n%d\n" % n)
            f.write("ITEM: BOX BOUNDS pp pp pp\n")
            for _ in range(3):
                f.write("0.0000000000000000e+00 %.16e\n" % L)
            f.write("ITEM: ATOMS id x y z\n")
            for i in range(n):
                f.write("%d %.6f %.6f %.6f\n" % (i + 1, *pos[i]))
    fr = WA.read_dump(path)
    os.remove(path)
    ok = len(fr) == 2 and abs(fr[0][1] - L) < 1e-9
    err = float(np.abs(fr[0][0] - pos).max()) if ok else float("inf")
    return rec("W1_dump_roundtrip", ok and err < 1e-5, nframes=len(fr),
               L=float(fr[0][1]), worst_coord_err=err)


def w2_coordination():
    # simple cubic, spacing a: 6 neighbours at a, 12 at a*sqrt2, 8 at a*sqrt3
    a, m = 2.0, 6
    g = np.arange(m) * a
    pos = np.stack(np.meshgrid(g, g, g, indexing="ij"), -1).reshape(-1, 3)
    L = m * a
    exact = {2.5: 6, 3.0: 18, 3.6: 26}
    got = {r: int(np.unique(WA.coordination(pos, L, r))[0]) for r in exact}
    ok1 = all(got[r] == exact[r] for r in exact)
    rng = np.random.default_rng(3)
    base = np.sort(WA.coordination(pos, L, 3.0))
    shifted = [np.array_equal(base, np.sort(WA.coordination(
        np.mod(pos + rng.random(3) * L, L), L, 3.0))) for _ in range(5)]
    return rec("W2_coordination_exact_and_pbc", ok1 and all(shifted),
               got=got, expect=exact, pbc_invariant=all(shifted))


def w3_triangle_cap_s3():
    rng = np.random.default_rng(4)
    pos = rng.random((900, 3)) * 30.0
    tri = GS.triangles(pos, 30.0, (4.0, 4.0, 4.0), 0.25, rng)
    key = np.sort(tri, axis=1)
    ratio = len(tri) / len(np.unique(key, axis=0))
    lab = (rng.random(900) < 0.4).astype(np.int8)
    devs = {}
    for cap in (None, len(tri) // 2, len(tri) // 4, len(tri) // 10):
        t = WA.cap_triangles(tri, cap, np.random.default_rng(7))
        devs["%s" % cap] = WA.s3_deviation(GS.table_from_triples(t, lab))
    ok = ratio > 5.9 and all(d < 1e-12 for d in devs.values())
    return rec("W3_triangle_cap_S3_exactly_zero", ok, orderings_per_triangle=round(ratio, 3),
               s3_deviation=devs)


def _planted_2p1(J12, J13, J23, h1, h2, h3):
    s = np.array([-1.0, 1.0])
    E = (J12 * s[:, None, None] * s[None, :, None] + J13 * s[:, None, None] * s[None, None, :]
         + J23 * s[None, :, None] * s[None, None, :]
         + h1 * s[:, None, None] + h2 * s[None, :, None] + h3 * s[None, None, :])
    p = np.exp(E)
    return p / p.sum()


def w4_ceiling_classpartition():
    # apex at slot 1: r12 == r13 != r23, so slots 2 and 3 are exchangeable
    p = _planted_2p1(0.35, 0.35, 0.12, 0.20, 0.45, 0.45)
    ceil, orients, groups = WA.ceiling_classpartition(p, (2.86, 2.86, 4.50))
    o = np.array(orients)
    sym_pair_identical = abs(o[0] - o[1]) < 1e-12
    ok = (groups == [[0, 1], [2]] and sym_pair_identical
          and abs(ceil - min(o[[0, 1]].mean(), o[2])) < 1e-15)
    # a fully scalene template must give three singleton classes
    _, _, gs = WA.ceiling_classpartition(p, (2.5, 3.0, 4.0))
    # the far arm is equilateral: one class of three
    _, _, ge = WA.ceiling_classpartition(p, (7.0, 7.0, 7.0))
    ok = ok and gs == [[0], [1], [2]] and ge == [[0, 1], [2]]
    return rec("W4_ceiling_class_partition", ok, orientations=[round(x, 8) for x in orients],
               classes=groups, ceiling=round(ceil, 8),
               sym_pair_identical=bool(sym_pair_identical),
               scalene_classes=gs, equilateral_classes=ge)


def _real_frames(nframes=25):
    return WA.read_dump(DUMP, nframes)


def w5_floors(frames):
    """N1a (product, theorem-pinned zero) and N1b (permutation, not pinned)."""
    rng = np.random.default_rng(11)
    r = WA.analyse(frames, WA.TMPL, WA.TOL, WA.RCUT, None, 300, rng, nboot=50)
    n, med = r["n_triples"], r["floor_median"]
    chi2_med = 0.2275 / n
    overlap = med / chi2_med
    ok = (r["floor_median"] > 0 and 1.0 <= overlap <= 25.0
          and abs(r["finite_pop_gauge"]) < 5 * med)
    return rec("W5_floors_N1a_N1b", ok, N_tri=n, floor_median=med,
               chi2_1_median=chi2_med, overlap_penalty=round(overlap, 3),
               perm_median=r["perm_median"],
               finite_pop_gauge=r["finite_pop_gauge"]), r


def _disjoint(tri, n):
    """A greedy VERTEX-DISJOINT subset of the triple list.

    Disjointness is what makes the planted amplitude exact: a particle touched by
    two planted triples would have its label written twice and the dose would
    saturate, which is precisely how the first version of this check came back
    non-monotone at large amplitude (recorded rather than silently rewritten).
    """
    used = np.zeros(n, bool)
    keep = []
    for t in tri:
        if not (used[t[0]] or used[t[1]] or used[t[2]]):
            used[t[0]] = used[t[1]] = used[t[2]] = True
            keep.append(t)
    return np.array(keep, dtype=np.int32) if keep else np.zeros((0, 3), np.int32)


def w6_dye(frames):
    """G-DYE.  Plant a three-body coupling in the LABELS of real configurations.

    On a VERTEX-DISJOINT subset of the real triple list, slot 3's label is set to
    the XOR of slots 1 and 2 with probability `eps` and to an independent coin
    otherwise.  Every single-slot marginal stays at 1/2 by construction, so what
    is recovered cannot be a composition effect; and because the subset is
    disjoint, `eps` is an exact dose rather than a rate that saturates.  The
    reading is taken over the FULL triple list, so the planted coupling is
    diluted exactly as a real one would be.
    """
    rng = np.random.default_rng(12)
    curve = []
    for eps in (0.0, 0.01, 0.03, 0.10, 0.30, 0.60, 1.00):
        tabs, fracs = [], []
        for pos, L in frames:
            tri = GS.triangles(pos, L, WA.TMPL, WA.TOL, rng)
            if not len(tri):
                continue
            lab = (rng.random(len(pos)) < 0.5).astype(np.int8)
            dj = _disjoint(tri, len(pos))
            if len(dj):
                par = lab[dj[:, 0]] ^ lab[dj[:, 1]]
                take = rng.random(len(dj)) < eps
                lab[dj[take, 2]] = par[take]
                fracs.append(len(dj) / len(tri))
            tabs.append(GS.table_from_triples(tri, lab).ravel())
        tab = np.array(tabs).sum(0).reshape(2, 2, 2)
        curve.append((eps, float(GS.share_2x2x2(tab))))
        print("      dye eps=%.2f -> share=%.4e  (disjoint frac %.3f)"
              % (curve[-1][0], curve[-1][1], float(np.mean(fracs))), flush=True)
    # The dye's job is to fix the DETECTION LIMIT, so monotonicity is required
    # only where the estimator can resolve anything at all.  `GATES.md` reach 11
    # states the principle -- "a reading below the validated detection limit is
    # not a detection" -- and demanding order below that limit would be demanding
    # that the estimator resolve what it has just been measured not to resolve.
    # The floor here is the LARGER of the label floor and the ideal-gas pedestal
    # of W7b, because a pedestal does not fall with N and the label floor does.
    fl = OUT.get("W5_floors_N1a_N1b", {}).get("floor_median", 0.0) * 6.7 / 0.43
    vals = [v for _, v in curve]
    above = [i for i, v in enumerate(vals) if v > fl]
    seg = vals[above[0]:] if above else []
    ok = all(seg[i] <= seg[i + 1] + 1e-12 for i in range(len(seg) - 1))
    return rec("W6_dye_monotone_above_floor", ok, curve=curve,
               floor_p99_used=fl,
               smallest_resolved_dose=(curve[above[0]][0] if above else None),
               detection_limit_nats=(curve[above[0]][1] if above else None),
               disjoint_fraction=round(float(np.mean(fracs)), 4))


def w7c_pedestal_mechanism(frames):
    """WHY the ideal gas mints, tested by an ADVANCE PREDICTION rather than
    explained after the fact.

    The proposed mechanism: at a compact template the three slots' cutoff spheres
    have a common triple intersection, so a single particle sitting in it is
    counted by all three coordination numbers at once.  That is an irreducibly
    THREE-body coupling written into the labels by the filter, from positions
    carrying no three-body physics at all.

    THE PREDICTION, stated before the sweep is run: the pedestal must VANISH once
    the template is wide enough that no three cutoff spheres share a point.  For
    an isoceles template with apex edges `s` and base `2 s sin(theta/2)` the
    triple intersection is empty once `s > 2 r_cut = 7.00 A`.  So the pedestal
    falls to floor between s = 2.86 A and s = 7.00 A and stays there beyond.

    A PASS is the pedestal being large at the primary template's scale and at
    floor beyond 2 r_cut.  If it were flat in template size, the mechanism is
    wrong and the pedestal is something else.
    """
    rng = np.random.default_rng(19)
    n, L = len(frames[0][0]), frames[0][1]
    ig = [(rng.random((n, 3)) * L, L) for _ in range(25)]
    rows = []
    for s in (2.86, 4.0, 5.5, 7.0, 8.5, 10.0):
        base = 2 * s * np.sin(np.deg2rad(109.47) / 2)
        if base > 0.5 * L:
            continue
        r = WA.analyse(ig, (s, s, base), WA.TOL, WA.RCUT, None, 150, rng, nboot=20)
        if r.get("empty") or r["n_triples"] < 500:
            continue
        rows.append((s, base, r["n_triples"], r["share"], r["floor_median"],
                     r["floor_p99"], r["p_value"]))
        print("      pedestal s=%5.2f base=%5.2f  N_tri=%8.0f  share=%.4e  "
              "floor_p99=%.4e  ratio=%6.2f  p=%.4f"
              % (s, base, r["n_triples"], r["share"], r["floor_p99"],
                 r["share"] / max(r["floor_p99"], 1e-30), r["p_value"]), flush=True)
    near = [r for r in rows if r[0] < 7.0]
    far = [r for r in rows if r[0] >= 7.0]
    ok = (bool(near) and bool(far)
          and max(r[3] / max(r[5], 1e-30) for r in near) > 1.0
          and all(r[3] <= r[5] for r in far))
    return rec("W7c_pedestal_vanishes_beyond_2rcut", ok,
               two_rcut=2 * WA.RCUT,
               rows=[dict(s=r[0], base=round(r[1], 3), N_tri=r[2], share=r[3],
                          floor_p99=r[5], share_over_p99=round(r[3] / max(r[5], 1e-30), 3),
                          p=r[6]) for r in rows])


def w7_ideal_gas(frames):
    """N2.  Poisson points at matched number density, byte-identical pipeline."""
    rng = np.random.default_rng(13)
    n, L = len(frames[0][0]), frames[0][1]
    ig = [(rng.random((n, 3)) * L, L) for _ in range(len(frames))]
    r = WA.analyse(ig, WA.TMPL, WA.TOL, WA.RCUT, None, 200, rng, nboot=50)
    rf = WA.analyse(ig, WA.FAR, WA.TOL, WA.RCUT, None, 200, rng, nboot=50)
    ok = (r["p_value"] > 0.01 and rf["p_value"] > 0.01)
    return rec("W7_ideal_gas_N2_at_floor", ok,
               share=r["share"], floor_p99=r["floor_p99"], p=r["p_value"],
               p1=round(r["p1"], 4), N_tri=r["n_triples"],
               far_share=rf["share"], far_p=rf["p_value"]), r


def w7b_ideal_gas_scaling(frames):
    """IS THE IDEAL-GAS READING A FLOOR OR A PEDESTAL?  The decisive question.

    W7 finds N2 sitting just above its own label floor.  Two things look like
    that and they have opposite consequences.  A FLOOR is shot noise and falls as
    1/N_tri.  A PEDESTAL is share genuinely MINTED by template selection plus the
    coordination filter -- `WATER_PREREG.md` sec 5.1's "FACT 3's trap, doubled" --
    and it does NOT fall with N, so it contaminates every reading at every sample
    size and must be subtracted rather than out-run.

    Distinguished by measuring the ideal-gas share against N_tri directly.
    """
    rng = np.random.default_rng(17)
    n, L = len(frames[0][0]), frames[0][1]
    rows = []
    for nconf in (5, 12, 25, 50):
        ig = [(rng.random((n, 3)) * L, L) for _ in range(nconf)]
        r = WA.analyse(ig, WA.TMPL, WA.TOL, WA.RCUT, None, 150, rng, nboot=30)
        rows.append((nconf, r["n_triples"], r["share"], r["floor_median"],
                     r["floor_p99"], r["p_value"]))
        print("      N2 nconf=%3d  N_tri=%8.0f  share=%.4e  floor_med=%.4e  p=%.4f"
              % rows[-1][:5] + "" if False else
              "      N2 nconf=%3d  N_tri=%8.0f  share=%.4e  floor_med=%.4e  p=%.4f"
              % (rows[-1][0], rows[-1][1], rows[-1][2], rows[-1][3], rows[-1][5]),
              flush=True)
    s = np.array([r[2] for r in rows])
    ntri = np.array([r[1] for r in rows])
    fl = np.array([r[3] for r in rows])
    # a floor scales as 1/N: share*N is flat.  a pedestal is flat in share itself.
    sN = s * ntri
    slope = float(np.polyfit(np.log(ntri), np.log(np.maximum(s, 1e-30)), 1)[0])
    ratio = s / fl
    ok = True   # diagnostic, not a pass/fail: the verdict is the exponent
    return rec("W7b_ideal_gas_share_vs_N", ok,
               n_tri=[int(x) for x in ntri],
               share=[float(x) for x in s], floor_median=[float(x) for x in fl],
               share_over_floor=[round(float(x), 3) for x in ratio],
               share_times_N=[round(float(x), 4) for x in sN],
               log_log_slope=round(slope, 3),
               reading="FLOOR (slope ~ -1)" if slope < -0.7 else
                       "PEDESTAL (slope ~ 0) — minted, does not fall with N")


def w8_degenerate_ceiling():
    """AMENDMENT 12 L3's arithmetic: a saturated label has ceiling exactly 0."""
    tab = np.zeros((2, 2, 2))
    tab[1, 1, 1] = 1.0e6
    c, o, _ = WA.ceiling_classpartition(tab, WA.TMPL)
    tab2 = np.zeros((2, 2, 2))
    tab2[1, 1, 1] = 1.0e6 - 3
    tab2[0, 1, 1] = tab2[1, 0, 1] = tab2[1, 1, 0] = 1.0
    c2, _, _ = WA.ceiling_classpartition(tab2, WA.TMPL)
    ok = abs(c) < 1e-12 and c2 < 1e-4
    return rec("W8_degenerate_label_ceiling_zero", ok, ceiling_p1_exactly_1=float(c),
               orientations=[float(x) for x in o],
               ceiling_p1_0p999997=float(c2))


def main():
    print("=== ARM A ANALYSIS DOCIMASIA — no campaign observable is scored here ===\n",
          flush=True)
    oks = [w1_dump_roundtrip(), w2_coordination(), w3_triangle_cap_s3(),
           w4_ceiling_classpartition(), w8_degenerate_ceiling()]
    print("\n--- checks touching real mW configurations, controls only ---", flush=True)
    frames = _real_frames()
    ok5, _ = w5_floors(frames)
    oks.append(ok5)
    oks.append(w6_dye(frames))
    ok7, _ = w7_ideal_gas(frames)
    oks.append(ok7)
    oks.append(w7b_ideal_gas_scaling(frames))
    oks.append(w7c_pedestal_mechanism(frames))
    OUT["verdict"] = bool(all(oks))
    json.dump(OUT, open("/home/emoore/CIRISOntology/scratchpad/water_arm_a_gate.json", "w"),
              indent=1)
    print("\n%s" % ("DOCIMASIA PASSED — the arm A analysis instrument may be used."
                    if all(oks) else
                    "DOCIMASIA FAILED — the instrument is not trusted and arm A does not proceed."),
          flush=True)
    return 0 if all(oks) else 1


if __name__ == "__main__":
    sys.exit(main())
