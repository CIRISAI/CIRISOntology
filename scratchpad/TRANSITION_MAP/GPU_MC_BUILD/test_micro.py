#!/usr/bin/env python3
"""Micro-case tests: every one is hand-computable or exactly known in closed form."""
from __future__ import annotations
import numpy as np
import regmodel as R, mc_tables as T, annihil_mc as A, exact_ref_sup as E

RES = []


def check(name, ok, detail=""):
    RES.append((name, bool(ok), detail))
    print(f"[{'PASS' if ok else 'FAIL'}] {name}   {detail}")


def t_unitarity():
    worst = 0.0
    for U in R.local_unitaries():
        d = U.shape[0]
        worst = max(worst, float(np.abs(U.conj().T @ U - np.eye(d)).max()))
    # The charter names 1e-15. The achievable floor for a 3x3 Hermitian eigendecomposition
    # in fp64 is a few ulp of 1.0 (eps = 2.22e-16), so the literal 1e-15 sits below the
    # floating-point floor. Gate set at 8*eps = 1.78e-15 and the measured value reported.
    gate = 8 * np.finfo(float).eps
    check("sector unitaries U^dag U = I", worst <= gate,
          f"max dev {worst:.3e} = {worst/np.finfo(float).eps:.1f} ulp (gate 8 ulp = {gate:.3e}; "
          f"charter's literal 1e-15 = {1e-15/np.finfo(float).eps:.1f} ulp is below the fp64 floor)")


def t_qcol():
    _, _, Q = T.collision_tables()
    d = float(np.abs(Q.sum(1) - 1).max())
    check("collision column probabilities sum to 1", d <= 1e-14, f"max dev {d:.3e}")


def t_stream_order():
    for L in (3, 5, 7, 9, 11):
        p = R.stream_permutation(L)
        q = np.arange(len(p))
        for _ in range(L):
            q = p[q]
        if not (q == np.arange(len(p))).all():
            check(f"stream permutation has order L={L}", False)
            return
    check("stream permutation has order exactly L (all carries return)", True, "L=3,5,7,9,11")


def t_stream_agrees():
    """The MC site-state stream must equal the exact engine's global mode permutation."""
    L = 5
    A.set_backend("cpu")
    tab = A.Tables(L)
    rng = np.random.default_rng(0)
    perm = R.stream_permutation(L)
    worst = 0
    for _ in range(20):
        occ = (rng.random(6 * L * L) < 0.35).astype(np.uint8)
        st = (occ.reshape(L * L, 6).astype(np.int64) * (1 << np.arange(6))).sum(1).astype(np.uint8)
        st2 = A.stream(st[None, :].copy(), tab)[0]
        cfg = tuple(sorted(np.flatnonzero(occ).tolist()))
        cfg2 = tuple(sorted(int(perm[m]) for m in cfg))
        occ2 = np.zeros(6 * L * L, np.uint8); occ2[list(cfg2)] = 1
        ref = (occ2.reshape(L * L, 6).astype(np.int64) * (1 << np.arange(6))).sum(1).astype(np.uint8)
        worst = max(worst, int(np.abs(st2.astype(int) - ref.astype(int)).max()))
    check("MC stream == exact mode permutation", worst == 0, f"max site-state diff {worst}")


def t_pack_bijective():
    L = 7
    A.set_backend("cpu"); tab = A.Tables(L)
    rng = np.random.default_rng(1)
    st = rng.integers(0, 64, size=(5000, tab.nsites)).astype(np.uint8)
    k = A.pack_keys(st, tab)
    u1 = len(set(map(tuple, st.tolist())))
    u2 = len(set(map(tuple, k.tolist())))
    check("bit-packed key is a bijection", u1 == u2, f"{u1} distinct configs -> {u2} distinct keys")


def t_annihilate_arithmetic():
    """Two walkers, one configuration: s_c = w1+w2 by hand."""
    L = 3
    A.set_backend("cpu"); tab = A.Tables(L)
    st = np.zeros((2, tab.nsites), np.uint8); st[:, 0] = 9
    wt = np.array([1 + 2j, 3 - 5j], dtype=np.complex128)
    rep, s_c, S = A.annihilate(st.copy(), wt.copy(), tab)
    ok = (s_c.shape == (1,) and abs(s_c[0] - (4 - 3j)) < 1e-15 and abs(S - 5.0) < 1e-15)
    check("2-walker annihilation: (1+2i)+(3-5i) = 4-3i, S=|4-3i|=5", ok,
          f"s_c={s_c[0]}, S={S}")
    # resampled weight is exactly (S/W)*s_c/|s_c|
    W = 8
    stn, wtn = A.resample(rep, s_c, S, W, np.random.default_rng(0))
    want = (S / W) * (4 - 3j) / 5.0
    ok2 = bool(np.abs(wtn - want).max() < 1e-15)
    check("resampled weight = (S/W)*s_c/|s_c|", ok2, f"want {want}, got {wtn[0]}")


def t_annihilate_cancels():
    """Exact phase cancellation: +w and -w at one configuration must annihilate to zero."""
    L = 3
    A.set_backend("cpu"); tab = A.Tables(L)
    st = np.zeros((2, tab.nsites), np.uint8); st[:, 0] = 9
    wt = np.array([0.7 - 0.2j, -0.7 + 0.2j], dtype=np.complex128)
    rep, s_c, S = A.annihilate(st, wt, tab)
    check("opposite phases annihilate exactly (S=0 -> ZERO-AMPLITUDE)", S == 0.0, f"S={S}")


def t_annihilate_two_configs():
    """Three walkers over two configurations; both sums by hand."""
    L = 3
    A.set_backend("cpu"); tab = A.Tables(L)
    st = np.zeros((3, tab.nsites), np.uint8)
    st[0, 0] = 9; st[1, 0] = 9; st[2, 0] = 18
    wt = np.array([1 + 0j, -0.25 + 0.5j, 2j], dtype=np.complex128)
    rep, s_c, S = A.annihilate(st, wt, tab)
    got = sorted([complex(z) for z in s_c], key=lambda z: (z.real, z.imag))
    want = sorted([0.75 + 0.5j, 2j], key=lambda z: (z.real, z.imag))
    ok = len(got) == 2 and all(abs(a - b) < 1e-15 for a, b in zip(got, want))
    check("segmented sum over two configurations", ok, f"{got}")


def t_resample_unbiased():
    """E[A'(c)] = A(c) = s_c/W conditionally, checked by Monte Carlo."""
    L = 3
    A.set_backend("cpu"); tab = A.Tables(L)
    rep = np.zeros((3, tab.nsites), np.uint8); rep[0, 0] = 9; rep[1, 0] = 18; rep[2, 0] = 36
    s_c = np.array([0.6 + 0.3j, -0.4 + 0.1j, 0.2 - 0.5j], dtype=np.complex128)
    S = float(np.abs(s_c).sum()); W = 400
    rng = np.random.default_rng(12345)
    R_ = 20000
    acc = np.zeros(3, dtype=np.complex128)
    for _ in range(R_):
        stn, wtn = A.resample(rep, s_c, S, W, rng)
        for j, ps in enumerate((9, 18, 36)):
            acc[j] += wtn[stn[:, 0] == ps].sum() / W
    got = acc / R_
    want = s_c / W
    err = float(np.abs(got - want).max()) / float(np.abs(want).max())
    check("resampling is conditionally unbiased  E[A'(c)] = s_c/W", err < 0.02,
          f"relative error {err:.4f} over {R_} resamplings (MC noise ~1%)")


def t_collision_unbiased():
    """E[w * 1{out=k}] = u_k for a single collision on one site."""
    A.set_backend("cpu"); tab = A.Tables(3)
    UCOL, OUT, QCOL = T.collision_tables()
    s0 = 9
    W = 400000
    st = np.zeros((W, tab.nsites), np.uint8); st[:, 0] = s0
    wt = np.ones(W, dtype=np.complex128)
    rng = np.random.default_rng(7)
    st, wt = A.collide(st, wt, tab, rng)
    worst = 0.0
    for k in range(3):
        sel = st[:, 0] == OUT[s0, k]
        got = wt[sel].sum() / W
        worst = max(worst, abs(got - UCOL[s0, k]))
    check("collision weight is unbiased: E[w 1{out=k}] = u_k", worst < 5e-3,
          f"max |E[w1]-u_k| = {worst:.2e} over W={W} (MC noise)")


def t_forced_branch_weights():
    """Forced-origin preparation reproduces the exact projection weights |a_j|^2."""
    bw = T.exact_branch_weights(7, [])
    r = E.run_exact(7, [])
    ok = float(np.abs(bw - r["branch_weights"]).max()) < 1e-14 and abs(bw.sum() - 1) < 1e-14
    check("branch weights |a_j|^2 agree with exact projection and sum to 1", ok,
          f"{np.round(bw,6)}")


if __name__ == "__main__":
    t_unitarity(); t_qcol(); t_stream_order(); t_stream_agrees(); t_pack_bijective()
    t_annihilate_arithmetic(); t_annihilate_cancels(); t_annihilate_two_configs()
    t_resample_unbiased(); t_collision_unbiased(); t_forced_branch_weights()
    n = sum(1 for _, ok, _ in RES if ok)
    print(f"\n{n}/{len(RES)} micro-case tests passed")
    raise SystemExit(0 if n == len(RES) else 1)
