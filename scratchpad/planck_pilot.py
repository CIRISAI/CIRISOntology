#!/usr/bin/env python3
"""
PLANCK / WMAP PLUMB LINE — the whole-only order-3 share of the CMB temperature
field, where the answer is a theorem.

Pre-registered in scratchpad/PLANCK_PILOT_PREREG.md, committed before this file
was run on data.  Every template, ladder, surrogate, gate, prediction and VOID
condition below is the one written there.

A Gaussian field split at its own median is sign-symmetric, and
`share_eq_zero_of_signSymmetric` (CIRISOntology/Core/SignSymmetry.lean) says a
sign-symmetric three-bit state has whole-only share EXACTLY ZERO.  So the b=2
reading must be zero, and any significant nonzero reading is this pipeline, not
the universe.

Scratchpad only.  No Lean, no Stance.lean, no audit, no `lake`.
"""
import json, os, sys, time
import numpy as np
import healpy as hp
from astropy.io import fits

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from dalitz_share import share_2x2x2, share_range_given_pairs, entropy, SIGMA  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "planck_pilot")
os.makedirs(OUT, exist_ok=True)

SMICA = "/home/emoore/coherence-ratchet/experiments/cmb_books/data/smica_2048.fits"
WMAP = "/home/emoore/coherence-ratchet/experiments/open_system_pomega/cmb_data/wmap_ilc_9yr_v5.fits"
THEORY = "/home/emoore/coherence-ratchet/experiments/cmb_books/data/planck_bestfit_theory.txt"

SEED_ANCHOR = 20260727          # PREREG 3.3
ARCMIN = np.pi / (180.0 * 60.0)

# PREREG 4.1 — twelve templates, pairwise separations in arcmin
TEMPLATES = {
    "E008": (8, 8, 8),      "E016": (16, 16, 16),   "E032": (32, 32, 32),
    "E064": (64, 64, 64),   "E128": (128, 128, 128), "E256": (256, 256, 256),
    "F016": (16, 16, 32),   "F064": (64, 64, 128),  "F128": (128, 128, 256),
    "S064": (8, 64, 64),    "S128": (16, 128, 128), "S256": (32, 256, 256),
}
TEMPLATE_ORDER = list(TEMPLATES)
BS = (2, 3, 4)                  # PREREG 4.2
N_DRAW = 4_000_000              # PREREG 3.3
OCCUPANCY_MIN = 100             # PREREG 4.2 / V1


# ---------------------------------------------------------------------------
# 1. THE ESTIMATOR
# ---------------------------------------------------------------------------

def ipf_share(P, tol=1e-13, maxit=5000):
    """Order-3 connected information of a b x b x b table by IPF.

    Returns (share, certificate, n_iter).  The certificate is the max absolute
    deviation of the fitted table's three pair marginals from the target's,
    which PREREG 6.8 / V7 requires below 1e-12 before the reading is reported.
    IPF for the all-two-way-interaction log-linear model converges to the
    maximum-entropy distribution carrying those margins.
    """
    P = np.asarray(P, dtype=float)
    P = P / P.sum()
    m12, m13, m23 = P.sum(2), P.sum(1), P.sum(0)
    Q = np.full_like(P, 1.0 / P.size)
    for it in range(maxit):
        for ax, tgt in ((2, m12), (1, m13), (0, m23)):
            cur = Q.sum(ax)
            with np.errstate(divide="ignore", invalid="ignore"):
                r = np.where(cur > 0, tgt / np.where(cur > 0, cur, 1.0), 0.0)
            Q = Q * np.expand_dims(r, ax)
        cert = max(np.abs(Q.sum(2) - m12).max(),
                   np.abs(Q.sum(1) - m13).max(),
                   np.abs(Q.sum(0) - m23).max())
        if cert < tol:
            break
    s = entropy(Q) - entropy(P)
    return float(max(0.0, s)), float(cert), it + 1


def read_triple(x1, x2, x3, b, thresholds=None):
    """PREREG 2/3.6 — one common threshold (b=2) or common quantile cuts (b>=3),
    taken over the POOLED values of all three slots.  Returns the b^3 table, the
    cut points, the tied fraction and the min cell occupancy."""
    pooled = np.concatenate([x1, x2, x3])
    if thresholds is None:
        if b == 2:
            cuts = np.array([np.median(pooled)])
        else:
            cuts = np.quantile(pooled, np.arange(1, b) / b)
    else:
        cuts = np.asarray(thresholds, dtype=float)
    tied = float(np.isin(pooled, cuts).mean())

    def dig(x):
        """Same as searchsorted(cuts, x, 'right') for the few cuts we use, but by
        direct comparison — 15x faster on 4e6 elements and bit-identical."""
        d = np.zeros(x.size, dtype=np.int8)
        for c in cuts:
            d += (x >= c)          # matches searchsorted(side="right") exactly
        return d

    d1, d2, d3 = dig(x1), dig(x2), dig(x3)
    idx = (d1.astype(np.int64) * b + d2) * b + d3
    tab = np.bincount(idx, minlength=b ** 3).astype(float).reshape(b, b, b)
    return tab, cuts, tied, float(tab.min())


def pair_entropies(tab):
    """The three pair-marginal entropies of a b x b x b table, in nats,
    ordered [H(m12), H(m13), H(m23)]."""
    P = np.asarray(tab, dtype=float)
    P = P / P.sum()
    return [entropy(P.sum(2)), entropy(P.sum(1)), entropy(P.sum(0))]


def sign_asymmetry(tab):
    """AMENDMENT 6 — is the table SIGN-SYMMETRIC, i.e. p(s) = p(-s)?

    This is the hypothesis `share_eq_zero_of_signSymmetric` spends, and until now
    this pilot ASSUMED it of the data rather than measuring it.  `pump-curve`'s
    two-axis correction is what forced the question: a state that is not
    sign-symmetric sits on a different pump axis, where even a unital channel
    mints and the a = 0 control is no longer a null.

    Pair each cell with its bin-reversed partner (i, j, k) <-> (b-1-i, b-1-j,
    b-1-k); at b = 2 that is exactly the global sign flip.  Under a truly
    sign-symmetric distribution the count difference of a pair has variance
    n+ + n- under multinomial sampling, so

        chi2 = sum over pairs (n+ - n-)^2 / (n+ + n-)

    is chi-squared with one degree of freedom per pair.  Returns the statistic,
    its dof, the survival probability, and the worst FRACTIONAL asymmetry.
    """
    from scipy import stats
    T = np.asarray(tab, dtype=float)
    b = T.shape[0]
    flat = T.reshape(-1)
    n = flat.size
    rev = T[::-1, ::-1, ::-1].reshape(-1)
    seen, chi2, dof, worst = set(), 0.0, 0, 0.0
    for i in range(n):
        j = n - 1 - i                      # index of the bin-reversed cell
        if i == j or i in seen:
            continue
        seen.add(i); seen.add(j)
        a, c = flat[i], rev[i]             # rev[i] == flat[j]
        if a + c <= 0:
            continue
        chi2 += (a - c) ** 2 / (a + c)
        dof += 1
        worst = max(worst, abs(a - c) / (a + c))
    p = float(stats.chi2.sf(chi2, dof)) if dof else None
    return float(chi2), int(dof), p, float(worst)


def sharp_cap(tab):
    """AMENDMENT 5 — the SHARP, data-computable ceiling of
    `share_le_grouping_gaps` (Core/ThirdCap.lean, commit 8925843):

        share <= H(pair) + H(remaining slot) - H(p)

    in each of the three slot orientations; the honest ceiling is their MINIMUM,
    and each is machine-checked to be at most log 2 on three binary slots.
    Strictly better than the `3*log2 - max H(pair)` bound this pilot was using
    before ThirdCap.lean existed, and unlike it, never worse than log 2.
    """
    P = np.asarray(tab, dtype=float)
    P = P / P.sum()
    Hp = entropy(P)
    m12, m13, m23 = P.sum(2), P.sum(1), P.sum(0)
    m1, m2, m3 = P.sum((1, 2)), P.sum((0, 2)), P.sum((0, 1))
    gaps = [entropy(m12) + entropy(m3) - Hp,
            entropy(m13) + entropy(m2) - Hp,
            entropy(m23) + entropy(m1) - Hp]
    return float(min(gaps)), [float(g) for g in gaps], float(Hp)


def reading(x1, x2, x3, b, thresholds=None, want_range=False, want_ipf=False):
    tab, cuts, tied, occ = read_triple(x1, x2, x3, b, thresholds)
    sc, gaps, Hp = sharp_cap(tab)
    x2, dof, psym, worst = sign_asymmetry(tab)
    out = {"b": b, "n": int(tab.sum()), "tied_frac": tied, "min_occ": occ,
           "cuts": [float(c) for c in cuts],
           "pair_entropies": pair_entropies(tab),
           "sharp_cap": sc, "grouping_gaps": gaps, "entropy": Hp,
           "signsym_chi2": x2, "signsym_dof": dof, "signsym_p": psym,
           "signsym_worst_frac": worst}
    if b == 2:
        out["share"] = float(share_2x2x2(tab))          # exact 1-D solver, no IPF
        if want_range:
            lo, hi = share_range_given_pairs(tab)
            out["lp_width"] = float(hi - lo)
        if want_ipf:                                     # PREREG 6.8, diagnostic only
            s_ipf, cert, nit = ipf_share(tab)
            out["share_ipf"] = s_ipf
            out["ipf_cert"] = cert
            out["ipf_iters"] = nit
    else:
        s_ipf, cert, nit = ipf_share(tab)
        out["share"] = s_ipf
        out["ipf_cert"] = cert
        out["ipf_iters"] = nit
    return out


# ---------------------------------------------------------------------------
# 2. MAPS AND MASKS
# ---------------------------------------------------------------------------

def remove_monodip(m, nside, report=None, name=""):
    """AMENDMENT 2 — exact full-sky ell<2 projection, removed.

    HEALPix is an equal-area grid with exact quadrature for ell <= 1, so the
    full-sky least-squares fit of [1, x, y, z] IS the ell<2 harmonic content:
    monopole = mean(m), d_i = 3*mean(m*v_i).  Subtracting it touches ell<2 and
    NOTHING ELSE — it is not a filter.  The surrogate zeroes ell<2 by
    construction (`phase_randomise`), so the data must too, or the floor is
    drawn against a field the data does not have.
    """
    m = m.astype(np.float64)
    v = np.array(hp.pix2vec(nside, np.arange(m.size)))
    mono = float(m.mean())
    d = 3.0 * np.array([float((m * v[i]).mean()) for i in range(3)])
    out = (m - mono - d[0] * v[0] - d[1] * v[1] - d[2] * v[2]).astype(np.float32)
    if report is not None:
        s = float(m.std())
        report[name] = {"monopole": mono, "dipole": d.tolist(),
                        "dipole_norm": float(np.linalg.norm(d)),
                        "std_before": s, "std_after": float(out.std()),
                        "mono_over_std": abs(mono) / s,
                        "dip_over_std": float(np.linalg.norm(d)) / s}
    return out


def load_planck(report=None):
    with fits.open(SMICA, memmap=True) as h:
        I = np.asarray(h[1].data["I_STOKES"], dtype=np.float64)
        Iinp = np.asarray(h[1].data["I_STOKES_INP"], dtype=np.float64)
        M = np.asarray(h[1].data["TMASK"], dtype=np.float64) > 0.5
        beam = np.asarray(h[2].data["INT_BEAM"], dtype=np.float64)
    I = hp.reorder(I, n2r=True)
    Iinp = hp.reorder(Iinp, n2r=True)
    return (remove_monodip(I, 2048, report, "planck_I"),
            remove_monodip(Iinp, 2048, report, "planck_Iinp"),
            hp.reorder(M.astype(np.int8), n2r=True) > 0, beam)


def load_wmap(report=None):
    with fits.open(WMAP, memmap=True) as h:
        T = np.asarray(h[1].data["TEMPERATURE"], dtype=np.float64)
    return remove_monodip(hp.reorder(T, n2r=True), 512, report, "wmap_T")


def wmap_mask(planck_mask_ring):
    """PREREG 6.3 — Planck TMASK ud_grade'd to NSIDE 512 with the
    fully-unmasked-superpixel rule, so both instruments read the SAME sky cut."""
    m = hp.ud_grade(planck_mask_ring.astype(np.float64), nside_out=512,
                    order_in="RING", order_out="RING")
    return m > 0.999999


def galactic_cut(nside, bmin_deg=30.0):
    """|b| > bmin, RING ordering, galactic coordinates (both maps are galactic)."""
    th, _ = hp.pix2ang(nside, np.arange(hp.nside2npix(nside)))
    return np.abs(90.0 - np.rad2deg(th)) > bmin_deg


# ---------------------------------------------------------------------------
# 3. SURROGATES  (PREREG 5)
# ---------------------------------------------------------------------------

def phase_randomise(alm, lmax, rng):
    """S1 — keep |a_lm| exactly, randomise phase, respect reality.

    healpy stores only m >= 0; the m < 0 coefficients are fixed by
    a_{l,-m} = (-1)^m conj(a_{lm}), so randomising the stored phases and giving
    a_{l0} a random sign is exactly a phase randomisation of the real field.
    C_l is preserved mode by mode, bit for bit.
    """
    out = np.empty_like(alm)
    ls, ms = hp.Alm.getlm(lmax)
    mod = np.abs(alm)
    ph = rng.uniform(0.0, 2.0 * np.pi, alm.size)
    out[:] = mod * np.exp(1j * ph)
    z = ms == 0
    out[z] = mod[z] * rng.choice(np.array([-1.0, 1.0]), int(z.sum()))
    out[ls < 2] = 0.0                       # monopole/dipole are zeroed in the data
    return out


WMAP_LMAX = 1024        # AMENDMENT 1: was 3*nside-1 = 1535
SHT_ITER = 3            # AMENDMENT 1: was 0


class Surrogates:
    def __init__(self, base_map, nside, lmax, tag, n_iter=SHT_ITER):
        self.nside, self.lmax, self.tag = nside, lmax, tag
        t0 = time.time()
        self.alm = hp.map2alm(base_map.astype(np.float64), lmax=lmax, iter=n_iter,
                              use_pixel_weights=False)
        self.cl = hp.alm2cl(self.alm)
        self.t_alm = time.time() - t0

    def s1(self, rng):
        return hp.alm2map(phase_randomise(self.alm, self.lmax, rng),
                          nside=self.nside, lmax=self.lmax).astype(np.float32)

    def s2(self, rng):
        seed = int(rng.integers(0, 2 ** 31 - 1))
        np.random.seed(seed)
        return hp.synfast(self.cl, nside=self.nside, lmax=self.lmax,
                          new=True, verbose=False).astype(np.float32)


def theory_cl(lmax_out, beam):
    """S3 — Planck best-fit TT (D_l in uK^2) -> C_l in K^2, times the beam^2."""
    d = np.loadtxt(THEORY)
    ell = d[:, 0].astype(int)
    dl = d[:, 1] * 1e-12                                  # uK^2 -> K^2
    cl = np.zeros(lmax_out + 1)
    ok = ell <= lmax_out
    l_ = ell[ok]
    cl[l_] = 2.0 * np.pi * dl[ok] / (l_ * (l_ + 1.0))
    nb = min(len(beam) - 1, lmax_out)
    b2 = np.zeros(lmax_out + 1)
    b2[:nb + 1] = beam[:nb + 1] ** 2
    return cl * b2


# ---------------------------------------------------------------------------
# 4. GEOMETRY  (PREREG 3.3-3.5)
# ---------------------------------------------------------------------------

def local_frame(v, psi):
    """Right-handed frame (e1, e2) perpendicular to v, rotated by psi about v."""
    d = v[2]
    a = np.stack([-d * v[0], -d * v[1], 1.0 - d * v[2]])
    a /= np.linalg.norm(a, axis=0)
    b = np.stack([v[1] * a[2] - v[2] * a[1],
                  v[2] * a[0] - v[0] * a[2],
                  v[0] * a[1] - v[1] * a[0]])
    c, s = np.cos(psi), np.sin(psi)
    return a * c + b * s, -a * s + b * c


def build_indices(nside, mask, templates=TEMPLATES, n_draw=N_DRAW, seed=SEED_ANCHOR):
    """One draw of anchors and azimuths, shared across every template
    (PREREG 3.3).  Returns {tag: (i1, i2, i3)} plus a report."""
    rng = np.random.default_rng(seed)
    unmasked = np.flatnonzero(mask)
    anch = unmasked[rng.integers(0, unmasked.size, n_draw)]
    psi = rng.uniform(0.0, 2.0 * np.pi, n_draw)
    v = np.array(hp.pix2vec(nside, anch))
    e1, e2 = local_frame(v, psi)
    idx, rep = {}, {}
    for tag, (t12, t13, t23) in templates.items():
        A, B, C = t12 * ARCMIN, t13 * ARCMIN, t23 * ARCMIN
        cosphi = (np.cos(C) - np.cos(A) * np.cos(B)) / (np.sin(A) * np.sin(B))
        if not (-1.0000001 <= cosphi <= 1.0000001):
            raise ValueError(f"{tag}: spherical triangle inequality violated")
        phi = float(np.arccos(np.clip(cosphi, -1.0, 1.0)))   # fixed chirality, PREREG 3.4
        p2 = v * np.cos(A) + e1 * np.sin(A)
        p3 = v * np.cos(B) + (e1 * np.cos(phi) + e2 * np.sin(phi)) * np.sin(B)
        i2 = hp.vec2pix(nside, p2[0], p2[1], p2[2])
        i3 = hp.vec2pix(nside, p3[0], p3[1], p3[2])
        keep = mask[i2] & mask[i3]
        i1k = anch[keep].astype(np.int32)
        i2k = i2[keep].astype(np.int32)
        i3k = i3[keep].astype(np.int32)
        # realised separations, as a check that the geometry is what was declared
        w = np.array(hp.pix2vec(nside, i1k[:5000]))
        w2 = np.array(hp.pix2vec(nside, i2k[:5000]))
        w3 = np.array(hp.pix2vec(nside, i3k[:5000]))
        sep = lambda a, c: np.rad2deg(np.arccos(np.clip((a * c).sum(0), -1, 1))) * 60.0
        idx[tag] = (i1k, i2k, i3k)
        rep[tag] = {"n_kept": int(i1k.size), "frac_kept": float(i1k.size / n_draw),
                    "declared": [t12, t13, t23],
                    "realised_median": [float(np.median(sep(w, w2))),
                                        float(np.median(sep(w, w3))),
                                        float(np.median(sep(w2, w3)))],
                    "n_distinct_pixels": int(np.unique(np.concatenate(
                        [i1k[:200000], i2k[:200000], i3k[:200000]])).size)}
    return idx, rep


# ---------------------------------------------------------------------------
# 5. THE READING OF ONE MAP OVER THE FULL GRID
# ---------------------------------------------------------------------------

def read_map(m, idx, bs=BS, tags=None, want_range=False, want_ipf=False,
             thresholds=None):
    """One pooled sort per template, not one per b: the cut points for every b in
    `bs` come out of a single np.quantile call on the pooled slot values."""
    tags = tags or list(idx)
    res = {}
    qs, qmap = [], {}
    for b in bs:
        qmap[b] = []
        for j in range(1, b):
            q = j / b
            if q not in qs:
                qs.append(q)
            qmap[b].append(q)
    qs_sorted = sorted(qs)
    for tag in tags:
        i1, i2, i3 = idx[tag]
        x1, x2, x3 = m[i1], m[i2], m[i3]
        if thresholds is None:
            pooled = np.concatenate([x1, x2, x3])
            qv = np.quantile(pooled, qs_sorted)
            lut = dict(zip(qs_sorted, qv))
            del pooled
        for b in bs:
            if thresholds is not None:
                thr = thresholds.get((tag, b))
            else:
                thr = [lut[q] for q in qmap[b]]
            res[f"{tag}|b{b}"] = reading(x1, x2, x3, b, thresholds=thr,
                                         want_range=want_range and b == 2,
                                         want_ipf=want_ipf and b == 2)
    return res


_W = {}


def _init_worker(surr, idx, bs, tags, kind):
    _W.update(surr=surr, idx=idx, bs=bs, tags=tags, kind=kind)


def _one(args):
    i, seed = args
    rng = np.random.default_rng(seed)
    m = _W["surr"].s1(rng) if _W["kind"] == "s1" else _W["surr"].s2(rng)
    return i, read_map(m, _W["idx"], bs=_W["bs"], tags=_W["tags"])


def ensemble(surr, idx, n, kind, base_seed, bs=BS, tags=None, log_every=25,
             label=""):
    """Surrogate ensemble, serial.

    Seeds are spawned deterministically from `base_seed` via SeedSequence, so the
    committed log is REPRODUCIBLE from the committed instrument — the harvest gate
    `gate-log provenance`, whose known-bad anchor is the phi4 gate log at 5e3ff
    that its own committed sampler could not reproduce.

    Serial by measurement, not by default: forked workers were tried at nproc 4
    and 8 and were SLOWER than serial (>62 s/map against 20 s/map).  The inner
    loop is memory-bandwidth bound — 4e6 random gathers into a 200 MB map plus a
    partition over 12e6 values — so extra processes buy contention, not
    throughput, and this box is shared with another campaign.
    """
    seeds = np.random.SeedSequence(base_seed).spawn(n)
    rows = []
    t0 = time.time()
    for i, sd in enumerate(seeds):
        rng = np.random.default_rng(sd)
        m = surr.s1(rng) if kind == "s1" else surr.s2(rng)
        rows.append(read_map(m, idx, bs=bs, tags=tags))
        if (i + 1) % log_every == 0:
            el = time.time() - t0
            print(f"  [{label}{kind}] {i+1}/{n}  {el:.0f}s  "
                  f"({el/(i+1):.2f}s/real)", flush=True)
    return rows


def collect(rows, key, field="share"):
    return np.array([r[key][field] for r in rows], dtype=float)


def null_shape(v):
    v = np.asarray(v, dtype=float)
    med = float(np.median(v))
    return {"n": int(v.size), "median": med, "mean": float(v.mean()),
            "std": float(v.std(ddof=1)), "min": float(v.min()), "max": float(v.max()),
            "p01": float(np.percentile(v, 1)), "p99": float(np.percentile(v, 99)),
            "mean_over_median": float(v.mean() / med) if med > 0 else None,
            "p99_over_median": float(np.percentile(v, 99) / med) if med > 0 else None}


def emp_p(obs, null):
    null = np.asarray(null, dtype=float)
    return float((1.0 + np.sum(null >= obs)) / (1.0 + null.size))


def gamma_p(obs, null):
    """PREREG 6.10 — parametric p from a gamma fit, ALWAYS with its KS p-value."""
    from scipy import stats
    null = np.asarray(null, dtype=float)
    null = null[null > 0]
    if null.size < 30:
        return None, None
    a, loc, sc = stats.gamma.fit(null, floc=0.0)
    ks = stats.kstest(null, "gamma", args=(a, loc, sc))
    return float(stats.gamma.sf(obs, a, loc, sc)), float(ks.pvalue)


def dump(name, obj):
    p = os.path.join(OUT, name)
    with open(p, "w") as f:
        json.dump(obj, f, indent=1, default=float)
    print(f"  wrote {p}", flush=True)


# ---------------------------------------------------------------------------
# STAGE 1 — V8 surrogate sanity.  No data reading.
# ---------------------------------------------------------------------------

def stage1():
    print("STAGE 1 — V8 surrogate sanity (no share is computed on data)", flush=True)
    out = {}
    I, Iinp, M, beam = load_planck()
    nside, lmax = 2048, 4096
    surr = Surrogates(Iinp, nside, lmax, "planck")
    print(f"  planck map2alm {surr.t_alm:.1f}s, lmax {lmax}", flush=True)
    rng = np.random.default_rng(101)
    sk, clr = [], []
    for i in range(8):
        s = surr.s1(rng)
        cl_s = hp.anafast(s.astype(np.float64), lmax=lmax, iter=0)
        r = cl_s[2:] / np.where(surr.cl[2:] > 0, surr.cl[2:], np.nan)
        clr.append([float(np.nanmedian(r)), float(np.nanmax(np.abs(r - 1.0)))])
        u = s[M]
        sk.append(float(((u - u.mean()) ** 3).mean() / u.std() ** 3))
    Iu = I[M]
    out["planck"] = {
        "lmax": lmax, "cl_ratio_median_and_maxdev": clr,
        "surrogate_skew_in_mask": sk,
        "surrogate_skew_mean": float(np.mean(sk)),
        "surrogate_skew_std": float(np.std(sk, ddof=1)),
        "data_skew_in_mask": float(((Iu - Iu.mean()) ** 3).mean() / Iu.std() ** 3),
        "data_std_in_mask": float(Iu.std()),
        "fsky_TMASK": float(M.mean()),
    }
    print("  planck surrogate skew (mask): %s" % np.round(sk, 5), flush=True)
    print("  planck C_l ratio median/maxdev: %s" % clr[0], flush=True)
    del I, Iinp, surr

    T = load_wmap()
    Mw = wmap_mask(M)
    del M
    nsw, lmw = 512, WMAP_LMAX
    sw = Surrogates(T, nsw, lmw, "wmap")
    rng = np.random.default_rng(202)
    skw, clw = [], []
    for i in range(8):
        s = sw.s1(rng)
        cl_s = hp.anafast(s.astype(np.float64), lmax=lmw, iter=0)
        r = cl_s[2:] / np.where(sw.cl[2:] > 0, sw.cl[2:], np.nan)
        clw.append([float(np.nanmedian(r)), float(np.nanmax(np.abs(r - 1.0)))])
        u = s[Mw]
        skw.append(float(((u - u.mean()) ** 3).mean() / u.std() ** 3))
    Tu = T[Mw]
    out["wmap"] = {
        "lmax": lmw, "cl_ratio_median_and_maxdev": clw,
        "surrogate_skew_in_mask": skw,
        "surrogate_skew_mean": float(np.mean(skw)),
        "surrogate_skew_std": float(np.std(skw, ddof=1)),
        "data_skew_in_mask": float(((Tu - Tu.mean()) ** 3).mean() / Tu.std() ** 3),
        "data_std_in_mask": float(Tu.std()),
        "fsky_common_mask_at_512": float(Mw.mean()),
    }
    print("  wmap surrogate skew (mask): %s" % np.round(skw, 5), flush=True)
    dump("stage1_surrogate_sanity.json", out)
    return out


def xi_of_cl(cl, thetas):
    """Two-point correlation function at given separations, from C_l."""
    from scipy.special import eval_legendre
    l = np.arange(cl.size)
    return np.array([float(np.sum((2 * l + 1) / (4 * np.pi) * cl * eval_legendre(l, np.cos(t))))
                     for t in thetas])


def stage1b():
    """AMENDMENT 1 — V8 restated: (1) exactness of construction, (2) pair
    structure at the templates' own separations, (3) skewness.  No data reading."""
    print("STAGE 1b — V8 as amended (no share is computed on data)", flush=True)
    seps = sorted({s for t in TEMPLATES.values() for s in t})
    th = np.array(seps) * ARCMIN
    md = {}
    out = {"separations_arcmin": seps, "monopole_dipole_removed": md}
    for name in ("planck", "wmap"):
        if name == "planck":
            _, base, M, _ = load_planck(md)
            nside, lmax = 2048, 4096
        else:
            _, _, Mp, _ = load_planck()
            base = load_wmap(md)
            M = wmap_mask(Mp)
            del Mp
            nside, lmax = 512, WMAP_LMAX
        s = Surrogates(base, nside, lmax, name)
        s.cl[:2] = 0.0            # AMENDMENT 2 — compare ell >= 2 on both sides
        del base
        # leg 1 — exactness of construction
        a2 = phase_randomise(s.alm, lmax, np.random.default_rng(11))
        ls, _ = hp.Alm.getlm(lmax)
        ok = ls >= 2
        rel = float(np.max(np.abs(np.abs(a2[ok]) - np.abs(s.alm[ok]))
                           / np.maximum(np.abs(s.alm[ok]), 1e-300)))
        # leg 2 — pair structure at the templates' separations
        xd = xi_of_cl(s.cl, th)
        var_d = float(np.sum((2 * np.arange(s.cl.size) + 1) * s.cl) / (4 * np.pi))
        xr, vr, sk = [], [], []
        for k in range(5):
            m = s.s1(np.random.default_rng(900 + k))
            cls = hp.anafast(m.astype(np.float64), lmax=lmax, iter=SHT_ITER)
            cls[:2] = 0.0
            xr.append([float(a / b) for a, b in zip(xi_of_cl(cls, th), xd)])
            vr.append(float(np.sum((2 * np.arange(cls.size) + 1) * cls) / (4 * np.pi) / var_d))
            u = m[M]
            sk.append(float(((u - u.mean()) ** 3).mean() / u.std() ** 3))
        out[name] = {
            "lmax": lmax, "sht_iter": SHT_ITER,
            "leg1_alm_modulus_rel_err": rel,
            "leg1_pass": bool(rel < 1e-12),
            "xi_data": [float(v) for v in xd], "var_data": var_d,
            "leg2_xi_ratios": xr, "leg2_var_ratios": vr,
            "leg2_max_abs_dev": float(max(abs(v - 1) for r in xr for v in r)),
            "leg2_max_var_dev": float(max(abs(v - 1) for v in vr)),
            "leg2_pass": bool(max(abs(v - 1) for r in xr for v in r) < 1e-3
                              and max(abs(v - 1) for v in vr) < 1e-3),
            "leg3_surrogate_skew": sk,
            "leg3_pass": bool(abs(np.mean(sk)) < 3 * np.std(sk, ddof=1) / np.sqrt(len(sk))
                              or abs(np.mean(sk)) < 0.02),
        }
        print(f"  {name}: leg1 rel_err {rel:.3e} ({'PASS' if out[name]['leg1_pass'] else 'FAIL'})  "
              f"leg2 max|xi-1| {out[name]['leg2_max_abs_dev']:.3e} "
              f"max|var-1| {out[name]['leg2_max_var_dev']:.3e} "
              f"({'PASS' if out[name]['leg2_pass'] else 'FAIL'})  "
              f"leg3 skew {np.mean(sk):+.5f}+-{np.std(sk,ddof=1):.5f}", flush=True)
        del s, M
    dump("stage1b_v8_amended.json", out)
    return out


# ---------------------------------------------------------------------------
# STAGE 2 — geometry.  No data reading.
# ---------------------------------------------------------------------------

def stage2():
    print("STAGE 2 — geometry build (no share is computed on data)", flush=True)
    _, _, M, _ = load_planck()
    idx_p, rep_p = build_indices(2048, M)
    np.savez(os.path.join(OUT, "idx_planck.npz"),
             **{f"{t}_{j}": idx_p[t][j] for t in idx_p for j in (0, 1, 2)})
    Mw = wmap_mask(M)
    idx_w, rep_w = build_indices(512, Mw)
    np.savez(os.path.join(OUT, "idx_wmap.npz"),
             **{f"{t}_{j}": idx_w[t][j] for t in idx_w for j in (0, 1, 2)})
    Mc = M & galactic_cut(2048, 30.0)
    idx_pc, rep_pc = build_indices(2048, Mc)
    np.savez(os.path.join(OUT, "idx_planck_cons.npz"),
             **{f"{t}_{j}": idx_pc[t][j] for t in idx_pc for j in (0, 1, 2)})
    Mwc = Mw & galactic_cut(512, 30.0)
    idx_wc, rep_wc = build_indices(512, Mwc)
    np.savez(os.path.join(OUT, "idx_wmap_cons.npz"),
             **{f"{t}_{j}": idx_wc[t][j] for t in idx_wc for j in (0, 1, 2)})
    rep = {"planck": rep_p, "wmap": rep_w,
           "planck_cons": rep_pc, "wmap_cons": rep_wc,
           "fsky": {"planck": float(M.mean()), "wmap": float(Mw.mean()),
                    "planck_cons": float(Mc.mean()), "wmap_cons": float(Mwc.mean())}}
    dump("stage2_geometry.json", rep)
    for t in TEMPLATE_ORDER:
        print(f"  {t}: planck n_kept {rep_p[t]['n_kept']:>8d}  "
              f"realised {np.round(rep_p[t]['realised_median'],2)}  |  "
              f"wmap n_kept {rep_w[t]['n_kept']:>8d}", flush=True)
    return rep


def load_idx(name):
    z = np.load(os.path.join(OUT, f"idx_{name}.npz"))
    return {t: (z[f"{t}_0"], z[f"{t}_1"], z[f"{t}_2"]) for t in TEMPLATE_ORDER}


# ---------------------------------------------------------------------------
# STAGE 3 — floors.  No data reading.
# ---------------------------------------------------------------------------

def stage3(n_s1=300, n_s2=100, n_s3=50):
    print("STAGE 3 — floors (no share is computed on data)", flush=True)
    _, Iinp, M, beam = load_planck()
    idx = load_idx("planck")
    idxc = load_idx("planck_cons")
    surr = Surrogates(Iinp, 2048, 4096, "planck")
    del Iinp
    r1 = ensemble(surr, idx, n_s1, "s1", 3001, label="planck ")
    dump("stage3_planck_s1.json", r1)
    r2 = ensemble(surr, idx, n_s2, "s2", 3021, label="planck ")
    dump("stage3_planck_s2.json", r2)
    r1c = ensemble(surr, idxc, 100, "s1", 3011, label="planckcons ")
    dump("stage3_planck_cons_s1.json", r1c)
    # S3 — theory realisation, Planck only, diagnostic
    cl_t = theory_cl(2508, beam)
    r3 = []
    for i in range(n_s3):
        np.random.seed(4000 + i)
        m = hp.synfast(cl_t, nside=2048, lmax=2508, new=True).astype(np.float32)
        r3.append(read_map(m, idx))
        if (i + 1) % 25 == 0:
            print(f"  [planck s3] {i+1}/{n_s3}", flush=True)
    dump("stage3_planck_s3.json", r3)
    del surr

    T = load_wmap()
    Mw = wmap_mask(M)
    del M
    idxw = load_idx("wmap")
    idxwc = load_idx("wmap_cons")
    sw = Surrogates(T, 512, WMAP_LMAX, "wmap")
    del T
    w1 = ensemble(sw, idxw, n_s1, "s1", 3002, label="wmap ")
    dump("stage3_wmap_s1.json", w1)
    w2 = ensemble(sw, idxw, n_s2, "s2", 3022, label="wmap ")
    dump("stage3_wmap_s2.json", w2)
    w1c = ensemble(sw, idxwc, 100, "s1", 3012, label="wmapcons ")
    dump("stage3_wmap_cons_s1.json", w1c)

    shape = {}
    for name, rows in (("planck_s1", r1), ("planck_s2", r2), ("planck_s3", r3),
                       ("wmap_s1", w1), ("wmap_s2", w2)):
        shape[name] = {k: null_shape(collect(rows, k)) for k in rows[0]}
    dump("stage3_null_shape.json", shape)
    return shape


# ---------------------------------------------------------------------------
# STAGE 4 — dye, boundary and valve arms.  All on surrogates.  No data reading.
# ---------------------------------------------------------------------------

DYE_TAGS = ["E032", "E064", "E128"]
DYE_F = [0.0, 0.003, 0.01, 0.03, 0.1, 0.3]     # AMENDMENT 3: f=0 control added
DYE_FWHM = 60 * ARCMIN
VALVE_EPS = [0.1, 0.5, 1.0]
BOUND_K = [1.0, 1.5, 2.0]


def stage4(n_floor=50, n_valve=20):
    print("STAGE 4 — dye / boundary / valve (all on surrogates)", flush=True)
    _, Iinp, M, beam = load_planck()
    idx = load_idx("planck")
    surr = Surrogates(Iinp, 2048, 4096, "planck")
    del Iinp
    out = {}

    # --- floors: TWO families (AMENDMENT 3) --------------------------------
    # D0 lives on the unsmoothed field; D1 and D2 live on the 60'-smoothed
    # field, which has fewer effective independent triples and therefore a
    # HIGHER floor.  Judging D1 against the unsmoothed floor is the harvest
    # gate `floor matched to sample size` failing on its own arm.  The
    # smoothing operator below is byte-identical to the one D1 uses.
    def smooth(m):
        return hp.smoothing(m.astype(np.float64), fwhm=DYE_FWHM, lmax=4096,
                            iter=0).astype(np.float32)

    fl = ensemble(surr, idx, n_floor, "s1", 5001, bs=(2, 3), tags=DYE_TAGS,
                  log_every=10, label="dyefloor-raw ")
    out["floor"] = {k: null_shape(collect(fl, k)) for k in fl[0]}
    dump("stage4_floor.json", out["floor"])
    fls, t0 = [], time.time()
    for i, sd in enumerate(np.random.SeedSequence(5011).spawn(n_floor)):
        fls.append(read_map(smooth(surr.s1(np.random.default_rng(sd))), idx,
                            bs=(2, 3), tags=DYE_TAGS))
        if (i + 1) % 10 == 0:
            print(f"  [dyefloor-smooth] {i+1}/{n_floor} {time.time()-t0:.0f}s",
                  flush=True)
    out["floor_smoothed"] = {k: null_shape(collect(fls, k)) for k in fls[0]}
    dump("stage4_floor_smoothed.json", out["floor_smoothed"])

    # --- G6 dye ------------------------------------------------------------
    base = surr.s1(np.random.default_rng(5100))
    u = ((base - float(base[M].mean())) / float(base[M].std())).astype(np.float32)
    su = smooth(u)
    v = ((su - float(su[M].mean())) / float(su[M].std())).astype(np.float32)
    del su
    dye = {"base": read_map(base, idx, bs=(2, 3), tags=DYE_TAGS)}
    for f in DYE_F:
        d0 = (u + np.float32(f) * (u * u - np.float32(1.0))).astype(np.float32)
        d1 = smooth(d0)
        d2 = (v + np.float32(f) * (v * v - np.float32(1.0))).astype(np.float32)
        dye[f"D0_f{f}"] = read_map(d0, idx, bs=(2, 3), tags=DYE_TAGS)
        dye[f"D1_f{f}"] = read_map(d1, idx, bs=(2, 3), tags=DYE_TAGS)
        dye[f"D2_f{f}"] = read_map(d2, idx, bs=(2, 3), tags=DYE_TAGS)
        print(f"  dye f={f} done", flush=True)
        del d0, d1, d2
    out["dye"] = dye
    dump("stage4_dye.json", dye)

    # --- G5 boundary: clip vs fold, on the SURROGATE base ------------------
    bnd = {"base": read_map(base, idx, bs=(2, 3), tags=DYE_TAGS)}
    s = float(base[M].std())
    for k in BOUND_K:
        c = np.clip(base, -k * s, k * s)
        fo = base.copy()
        hi, lo = base > k * s, base < -k * s
        fo[hi] = 2 * k * s - base[hi]
        fo[lo] = -2 * k * s - base[lo]
        bnd[f"clip_k{k}"] = read_map(c, idx, bs=(2, 3), tags=DYE_TAGS)
        bnd[f"fold_k{k}"] = read_map(fo, idx, bs=(2, 3), tags=DYE_TAGS)
        bnd[f"flipped_frac_k{k}"] = float(np.mean(np.abs(base[M]) > 2 * k * s))
    out["boundary_surrogate"] = bnd
    dump("stage4_boundary_surrogate.json", bnd)

    # --- G7 valve ----------------------------------------------------------
    val = {}
    rngv = np.random.default_rng(5200)
    npix = base.size
    s_base = float(base[M].std())      # eps is in units of the map's own sigma
    for eps in VALVE_EPS:
        for kind in ("sym", "asym"):
            rows = []
            for j in range(n_valve):
                if kind == "sym":
                    nse = rngv.standard_normal(npix, dtype=np.float32)
                else:
                    nse = (rngv.exponential(1.0, npix).astype(np.float32) - 1.0)
                nse *= np.float32(eps * s_base)
                nse += base
                rows.append(read_map(nse, idx, bs=(2,), tags=DYE_TAGS))
                del nse
            val[f"{kind}_eps{eps}"] = {k: null_shape(collect(rows, k)) for k in rows[0]}
            print(f"  valve {kind} eps={eps} done", flush=True)
    out["valve"] = val
    dump("stage4_valve.json", val)
    return out


# ---------------------------------------------------------------------------
# STAGE 5 — THE DATA READING.  Once, on the frozen grid.
# ---------------------------------------------------------------------------

def stage5():
    print("STAGE 5 — the data reading", flush=True)
    I, _, M, _ = load_planck()
    out = {}
    idx = load_idx("planck")
    out["planck"] = read_map(I, idx, want_range=True, want_ipf=True)
    out["planck_zero_thresh"] = read_map(
        I, idx, bs=(2,), thresholds={(t, 2): [0.0] for t in TEMPLATE_ORDER})
    idxc = load_idx("planck_cons")
    out["planck_cons"] = read_map(I, idxc)
    del idxc
    # boundary arm on the DATA map
    s = float(I[M].std())
    bnd = {}
    for k in BOUND_K:
        c = np.clip(I, -k * s, k * s)
        fo = I.copy()
        hi, lo = I > k * s, I < -k * s
        fo[hi] = 2 * k * s - I[hi]
        fo[lo] = -2 * k * s - I[lo]
        bnd[f"clip_k{k}"] = read_map(c, idx, bs=(2, 3), tags=DYE_TAGS)
        bnd[f"fold_k{k}"] = read_map(fo, idx, bs=(2, 3), tags=DYE_TAGS)
        bnd[f"flipped_frac_k{k}"] = float(np.mean(np.abs(I[M]) > 2 * k * s))
    bnd["base"] = read_map(I, idx, bs=(2, 3), tags=DYE_TAGS)
    out["planck_boundary"] = bnd
    # degrade arm (G4)
    deg = {}
    for ns in (512, 256):
        md = hp.ud_grade(I.astype(np.float64), nside_out=ns,
                         order_in="RING", order_out="RING").astype(np.float32)
        Md = hp.ud_grade(M.astype(np.float64), nside_out=ns,
                         order_in="RING", order_out="RING") > 0.999999
        idxd, repd = build_indices(ns, Md)
        deg[f"nside{ns}"] = {"reading": read_map(md, idxd, bs=(2, 3)),
                             "n_kept": {t: repd[t]["n_kept"] for t in repd},
                             "fsky": float(Md.mean()),
                             "npix": int(Md.size)}
        np.savez(os.path.join(OUT, f"idx_planck_deg{ns}.npz"),
                 **{f"{t}_{j}": idxd[t][j] for t in idxd for j in (0, 1, 2)})
        del idxd, md, Md
    out["planck_degrade"] = deg
    del I, idx

    T = load_wmap()
    Mw = wmap_mask(M)
    del M
    idxw = load_idx("wmap")
    out["wmap"] = read_map(T, idxw, want_range=True, want_ipf=True)
    out["wmap_zero_thresh"] = read_map(
        T, idxw, bs=(2,),
        thresholds={(t, 2): [float(T[Mw].mean())] for t in TEMPLATE_ORDER})
    del idxw
    idxwc = load_idx("wmap_cons")
    out["wmap_cons"] = read_map(T, idxwc)
    dump("stage5_data.json", out)
    return out


# ---------------------------------------------------------------------------
# STAGE 6 — degrade floors (G4 needs a matched floor for the degraded grid)
# ---------------------------------------------------------------------------

def stage6(n=100):
    print("STAGE 6 — degrade-arm floors", flush=True)
    _, Iinp, M, _ = load_planck()
    out = {}
    for ns in (512, 256):
        mi = hp.ud_grade(Iinp.astype(np.float64), nside_out=ns,
                         order_in="RING", order_out="RING")
        z = np.load(os.path.join(OUT, f"idx_planck_deg{ns}.npz"))
        idxd = {t: (z[f"{t}_0"], z[f"{t}_1"], z[f"{t}_2"]) for t in TEMPLATE_ORDER}
        # lmax = 2*nside, healpy's reliable analysis limit (AMENDMENT 1)
        sd = Surrogates(mi.astype(np.float32), ns, 2 * ns, f"deg{ns}")
        rows = ensemble(sd, idxd, n, "s1", 7000 + ns,
                        bs=(2, 3), log_every=25, label=f"deg{ns} ")
        out[f"nside{ns}"] = {k: null_shape(collect(rows, k)) for k in rows[0]}
    dump("stage6_degrade_floor.json", out)
    return out


if __name__ == "__main__":
    st = sys.argv[1] if len(sys.argv) > 1 else "all"
    fns = {"1": stage1, "1b": stage1b, "2": stage2, "3": stage3, "4": stage4,
           "5": stage5, "6": stage6}
    if st == "all":
        for k in ("1", "1b", "2", "3", "4", "5", "6"):
            fns[k]()
    else:
        fns[st]()
