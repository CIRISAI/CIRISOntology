"""rent_scaling_q2.py — QUESTION 2: does rent/nat plateau beyond k = 24?

Pre-registered in RENT_SCALING_PREREG.md (commit 45b6877) §3. Extends the parent's
k = 5..24 curve (rent_islands.py) to the box's declared ceiling of k = 31, which is set by the
2^k barrier at the next non-linear Hadamard order (prereg §1.4), not by any curve.

WHAT IS NEW HERE, AND WHAT IS NOT.

  * The DEFINITION of rent is unchanged: the constant q* whose stationary state holds share
    exactly `target`, and rent/nat = q*(H_pre - H_deposit)/share. Every formula is the
    parent's; this file only makes them affordable at larger k.
  * BOTH routes are re-implemented lean, and the reason is a measurement, not a preference:
    the parent's classes run to 13 GB resident at k = 27/31 on a box that had 7 GB free and
    5 GB of swap already in use, and this campaign declared a 6 GB budget (prereg §4). The
    parent materialises seven 2^k arrays in the full route and keeps the whole 2^(k-m) dual
    codeword list in the quotient route; the lean versions hold two buffers and one, discard
    the dual words once their weights are taken, accumulate entropies chunkwise, and take the
    weight enumerator from the |S|x|S| distance matrix through Krawtchouk instead of from a
    2^k Fourier pass. Gate Q2-G1 requires BOTH to reproduce the parent's own rows, quantity by
    quantity, at k = 20..24 -- the arithmetic is the parent's and is checked to be.
  * The ROOT-FINDER is a monotone bracketing grid followed by Brent, instead of 50 bisections,
    because at k = 31 each evaluation is two transforms of 2^26 doubles. Same root, fewer
    evaluations; the prereg's 1e-6 relative target-residual bar is enforced unchanged and a
    row that misses it is DROPPED, not adjusted.

There is no sampling anywhere in this file. No replicas, no Monte Carlo, no error bars --
the reported error budget is numerical and is attached to every row.
"""
import sys, os, json, time, argparse
import numpy as np
from scipy.optimize import brentq

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import rent_islands as RI
import rent_islands_design_check as DC

HERE = os.path.dirname(os.path.abspath(__file__))
LN2 = float(np.log(2))
CHUNK = 1 << 22


# =====================================================================================
# the transform
# =====================================================================================

def fwht_ip(a, temp_elems=1 << 22):
    """In-place Walsh-Hadamard transform, blocked so the scratch never exceeds
    `temp_elems`. Same convention as rent_islands.wht: out[T] = sum_v a_v (-1)^{T.v}."""
    n = a.size
    h = 1
    while h < n:
        b = a.reshape(-1, 2 * h)
        rows = b.shape[0]
        step = max(1, temp_elems // h)
        for r0 in range(0, rows, step):
            blk = b[r0:r0 + step]
            lo = blk[:, :h]
            hi = blk[:, h:]
            t = lo - hi
            lo += hi
            hi[...] = t
        h *= 2
    return a.reshape(n)


def fast_wht(a, xp=np):
    """Drop-in for rent_islands.wht: copies, then transforms in place."""
    return fwht_ip(np.array(a, dtype=np.float64, copy=True))


def entropy_chunked(p, chunk=CHUNK):
    tot = 0.0
    for lo in range(0, p.size, chunk):
        q = p[lo:lo + chunk]
        q = np.maximum(q, 0.0)
        m = q > 0
        if m.any():
            qq = q[m]
            tot -= float(np.sum(qq * np.log(qq)))
    return tot


def lean_popcount(n, chunk=1 << 24):
    """popcount over arange(n) as int8, without ever holding an int64 array of size n.
    The parent's version materialises arange(n) plus a temporary per bit -- 3 GB at k=27."""
    pc = np.empty(n, dtype=np.int8)
    for lo in range(0, n, chunk):
        hi = min(lo + chunk, n)
        idx = np.arange(lo, hi, dtype=np.int64)
        acc = np.zeros(hi - lo, dtype=np.int8)
        b = 0
        while (1 << b) < n:
            acc += ((idx >> b) & 1).astype(np.int8)
            b += 1
        pc[lo:hi] = acc
    return pc


# =====================================================================================
# the lean quotient route: a LINEAR substrate, everything over the dual
# =====================================================================================

class LeanQuotient:
    """Exact stationary quantities for a linear substrate, holding ONE 2^(k-m) float64
    buffer instead of the parent's half-dozen.

    The mathematics is the parent's `_stat_quotient` unchanged: p_inf is constant on cosets
    of the code, so p_hat = g_{|u|} on the dual and one Walsh-Hadamard transform of size 2^r
    gives the per-coset probability. What changes is bookkeeping -- the dual codeword array
    is discarded once its weights are taken, the entropy is accumulated chunkwise, and the
    coset-leader BFS expands its frontier in blocks. Gate Q2-G1 requires agreement with the
    parent to 1e-10 on every quantity.
    """

    def __init__(self, tag, arm, k, G, name=''):
        self.tag, self.arm, self.k, self.name = tag, arm, k, name
        self.route, self.kind = 'quotient-lean', 'linear'
        G = np.asarray(G, dtype=np.int8) % 2
        self.m = G.shape[0]
        self.S = RI.MS.linear_code(k, G)
        self.ns = 1 << self.m
        assert len(set(map(tuple, self.S.tolist()))) == self.ns, 'generator not full rank'
        self.r = k - self.m
        self.N = 1 << k
        self.share_max = k * LN2 - np.log(self.ns)
        self.density = self.share_max / k
        Hchk = RI.f2_rank_nullspace(G)
        masks = RI.rows_to_masks(Hchk, k)
        words = np.zeros(1 << self.r, dtype=np.int64)
        for i in range(self.r):
            h = 1 << i
            words[h:2 * h] = words[:h] ^ masks[i]
        self.dual_w = RI.popcount64(words).astype(np.int8)
        del words
        assert self.dual_w[0] == 0
        A = np.bincount(self.dual_w.astype(np.int64), minlength=k + 1).astype(float)
        self.A = A
        self.d = int(next((w for w in range(1, k + 1) if A[w] > 0), -1))
        # bit order is load-bearing; see the parent's comment in Lattice._init_linear
        self.colsyn = np.array([sum(int(Hchk[i, j]) << i for i in range(self.r))
                                for j in range(k)], dtype=np.int64)
        self.leader_w = None
        self.equivariant, self.equiv_dev, self.profile_dev = True, 0.0, 0.0
        self._buf = None

    def _leaders(self):
        """min weight per syndrome, by BFS with a BLOCKED frontier expansion."""
        if self.leader_w is not None:
            return self.leader_w
        n = 1 << self.r
        lead = np.full(n, -1, dtype=np.int16)
        lead[0] = 0
        frontier = np.array([0], dtype=np.int64)
        w, filled = 0, 1
        while filled < n:
            w += 1
            found = []
            block = max(1, (1 << 22) // max(1, self.k))
            for lo in range(0, frontier.size, block):
                nxt = (frontier[lo:lo + block, None] ^ self.colsyn[None, :]).ravel()
                nxt = np.unique(nxt)
                nxt = nxt[lead[nxt] < 0]
                if nxt.size:
                    lead[nxt] = w
                    found.append(nxt)
            if not found:
                raise RuntimeError('coset BFS stalled')
            frontier = np.unique(np.concatenate(found))
            filled += int(frontier.size)
        self.leader_w = lead
        return lead

    def _buffer(self):
        if self._buf is None:
            self._buf = np.empty(1 << self.r, dtype=np.float64)
        return self._buf

    def _coset(self, weights):
        """pq = wht(weights[dual_w]) / N, in the single buffer."""
        buf = self._buffer()
        n = buf.size
        for lo in range(0, n, CHUNK):
            hi = min(lo + CHUNK, n)
            buf[lo:hi] = weights[self.dual_w[lo:hi]]
        fwht_ip(buf)
        buf /= self.N
        return buf

    def ceiling_share(self, eps):
        """share_inf(q=1), in closed form. At q = 1 every replica is replaced by the
        decoded point, so the stationary state IS the deposit; on a linear substrate the
        decoder is equivariant (Q1: every linear support is transitive) so the deposit is
        uniform on S and the ceiling is share_max exactly. Computing it instead as
        k*ln2 - H(p) over 2^k cells adds roundoff-level mass to the 2^k - |S| cells that are
        exactly zero, which is what gate Q2-G1 caught in the parent's `ceiling` column."""
        return self.share_max

    def stat_share(self, q, eps, want=()):
        lam = 1.0 - 2.0 * eps
        g = RI.g_vec(q, eps, self.k)
        mult = float(self.ns)
        pq = self._coset(g)
        Hp, mass, neg = self._acc(pq, mult)
        out = dict(share=self.k * LN2 - Hp, share_raw=self.k * LN2 - Hp, H=Hp,
                   H_c=float(np.log(self.ns)), mass=mass, neg=neg,
                   leak=0.0, c_iters=0, c_err=0.0)
        if want:
            pqp = self._coset((lam ** np.arange(self.k + 1)) * g)
            Hpre, mass_pre, neg_pre = self._acc(pqp, mult)
            out.update(H_pre=Hpre, share_pre=self.k * LN2 - Hpre,
                       mass_pre=mass_pre, neg_pre=neg_pre, leak_pre=0.0)
            if 'flips' in want:
                lead = self._leaders()
                tot = 0.0
                for lo in range(0, pqp.size, CHUNK):
                    hi = min(lo + CHUNK, pqp.size)
                    tot += float(np.sum(np.maximum(pqp[lo:hi], 0.0)
                                        * lead[lo:hi].astype(np.float64)))
                out['flips'] = q * mult * tot
        return out

    def _acc(self, pq, mult):
        H, mass, neg = 0.0, 0.0, 0.0
        for lo in range(0, pq.size, CHUNK):
            v = pq[lo:lo + CHUNK]
            mass += float(v.sum())
            neg = min(neg, float(v.min()))
            m = v > 0
            if m.any():
                vv = v[m]
                H -= float(np.sum(mult * vv * np.log(vv)))
        return H, mult * mass, neg * mult

    def pair_dev(self):
        S = np.asarray(self.S, dtype=np.int8)
        worst = 0.0
        for i in range(self.k):
            for j in range(i + 1, self.k):
                cnt = np.bincount(S[:, i].astype(int) * 2 + S[:, j].astype(int),
                                  minlength=4)
                worst = max(worst, float(np.abs(cnt / self.ns - 0.25).max()))
        return worst

    def free(self):
        self._buf = None
        self.leader_w = None
        self.dual_w = None


# =====================================================================================
# the lean full route: a non-linear OA support at large k
# =====================================================================================

class LeanFull:
    """Exact stationary quantities for a general (non-linear) pair-uniform support.

    Holds two 2^k float64 buffers and two 2^k int8 vectors. Everything else is |S|-sized.
    """

    def __init__(self, tag, arm, k, S, name=''):
        self.tag, self.arm, self.k, self.name = tag, arm, k, name
        self.route, self.kind = 'full-lean', 'oa'
        S = np.unique(np.asarray(S, dtype=np.int8), axis=0)
        self.S = S
        self.ns = len(S)
        self.m = None
        self.N = 1 << k
        self.sidx = RI.MS.bits_to_idx(S)
        assert len(np.unique(self.sidx)) == self.ns
        self.share_max = k * LN2 - np.log(self.ns)
        self.density = self.share_max / k
        self.pc = lean_popcount(self.N)
        # weight enumerator WITHOUT a 2^k Fourier pass:
        #   sum_{|T|=w} phat0(T)^2 = (1/|S|^2) sum_{i,j} K_w(|s_i ^ s_j|)
        Dij = np.zeros((self.ns, self.ns), dtype=np.int64)
        for i in range(self.ns):
            Dij[i] = (S[i][None, :] != S).sum(axis=1)
        self._kr = self._krawtchouk()
        self.A = np.array([float(self._kr[w][Dij].sum()) / self.ns ** 2
                           for w in range(k + 1)])
        self.d = int(next((w for w in range(1, k + 1) if self.A[w] > 1e-9), -1))
        self.mindist = self._build_mindist()
        self._cd = self._build_cd()
        R = self._cd.sum(axis=1)
        self.profile_dev = float(np.abs(R - R.mean(axis=0, keepdims=True)).max()
                                 / (self.N / self.ns))
        self.equivariant = bool(self.profile_dev < 1e-12)
        self.equiv_dev = self.profile_dev            # same criterion, exact and eps-free
        self._buf = None
        self._buf2 = None
        # sign tables for the low-order Fourier coefficients (the leak), |T| = 1 and 2
        self._lowT = [(j,) for j in range(k)] + [(j, l) for j in range(k)
                                                 for l in range(j + 1, k)]
        self._lowsign = np.array([(-1.0) ** (S[:, list(T)].sum(axis=1) % 2)
                                  for T in self._lowT])          # (n_low, ns)
        self._loww = np.array([len(T) for T in self._lowT])

    def _krawtchouk(self):
        from math import comb
        k = self.k
        Kr = np.zeros((k + 1, k + 1))
        for w in range(k + 1):
            for a in range(k + 1):
                Kr[w, a] = sum((-1) ** i * comb(a, i) * comb(k - a, w - i)
                               for i in range(0, min(a, w) + 1) if w - i <= k - a)
        return Kr

    def _hblock(self, lo, hi):
        x = np.arange(lo, hi, dtype=np.int64)[:, None]
        return self.pc[x ^ self.sidx[None, :]]

    def _build_mindist(self):
        out = np.empty(self.N, dtype=np.int8)
        for lo in range(0, self.N, 1 << 18):
            hi = min(lo + (1 << 18), self.N)
            out[lo:hi] = self._hblock(lo, hi).min(axis=1)
        return out

    def _build_cd(self):
        """Cd[i,j,a] = decode weight onto i, summed over x at distance a from s_j.
        q-independent; built once (parent's §_build_cd, chunked identically)."""
        ns, k = self.ns, self.k
        Cd = np.zeros((ns, ns, k + 1))
        colbase = np.arange(ns, dtype=np.int64)[None, :] * (k + 1)
        for lo in range(0, self.N, 1 << 16):
            hi = min(lo + (1 << 16), self.N)
            D = self._hblock(lo, hi)
            tie = (D == D.min(axis=1, keepdims=True))
            W = tie / tie.sum(axis=1, keepdims=True)
            Di = D.astype(np.int64)
            for i in range(ns):
                wi = W[:, i]
                nz = wi > 0
                if not nz.any():
                    continue
                idx = colbase + Di[nz]
                wts = np.broadcast_to(wi[nz][:, None], idx.shape)
                Cd[i] += np.bincount(idx.ravel(), weights=wts.ravel(),
                                     minlength=ns * (k + 1)).reshape(ns, k + 1)
        return Cd

    def kappa(self, q, eps, route='auto'):
        """The x-space kernel of noise-then-resolvent, as a function of Hamming weight.

        WHY THIS IS NOT JUST THE KRAWTCHOUK SUM. The parent computes
        kappa(a) = (1/N) sum_w lam^w g_w K_w(a), which is correct algebra and numerically
        ruinous: |K_w(a)| reaches 1.35e6 at k=23 while the answer at a=23 is 1e-46, so the
        sum is 100 % cancellation and returns NEGATIVE kernel values with an absolute noise
        floor of eps_machine * max|K_w| / N = 3.5e-17. Gate Q2-G6 caught it: on A23, which
        is EXACTLY equivariant (verified in exact integer arithmetic by
        rent_scaling_q1_verify.py), the q=1 deposit came out non-uniform by 5.4e-9.

        Two routes, and which one is used is recorded:
          'exact'  -- at q = 1, g == 1 and the kernel IS the binomial noise kernel,
                      eps^a (1-eps)^(k-a). Closed form, no cancellation, machine exact.
          'series' -- the general q: expanding 1/(1-(1-q)lam^w) as a geometric series gives
                      kappa(a) = q * sum_m (1-q)^m * e_m^a (1-e_m)^(k-a),  e_m = (1-lam^(m+1))/2,
                      every term positive -- this is just "how many noise steps since the
                      last upkeep", so the mixture form is the physics, not a trick. The
                      tail beyond M is added analytically as 2^-k (1-q)^M / q, since
                      e_m -> 1/2.
          'kraw'   -- the parent's route, kept for the gate.
        Default: exact at q=1, series where it is affordable, Krawtchouk below that -- and
        the Krawtchouk error scales as q * 3.5e-17 * N/|S|, so it is worst exactly where the
        exact route now takes over.
        """
        k, lam = self.k, 1.0 - 2.0 * eps
        a = np.arange(k + 1)
        if route == 'exact' or (route == 'auto' and q >= 1.0 - 1e-15):
            return eps ** a * (1.0 - eps) ** (k - a)
        if route == 'series' or (route == 'auto' and q >= 1e-3):
            M = int(min(2e5, max(64, np.ceil(np.log(1e-20) / np.log(max(1e-12, 1 - q))))))
            m = np.arange(M)
            e = 0.5 * (1.0 - lam ** (m + 1))
            w = q * (1.0 - q) ** m
            out = (w[:, None] * (e[:, None] ** a[None, :]
                                 * (1.0 - e[:, None]) ** (k - a[None, :]))).sum(axis=0)
            return out + (1.0 - q) ** M * 2.0 ** (-k)
        g = RI.g_vec(q, eps, k)
        return (((lam ** a) * g)[:, None] * self._kr).sum(axis=0) / self.N

    def solve_c(self, q, eps, route='auto'):
        kappa = self.kappa(q, eps, route)
        C = (self._cd * kappa[None, None, :]).sum(axis=2)
        A = C - np.eye(self.ns)
        A[-1, :] = 1.0
        b = np.zeros(self.ns)
        b[-1] = 1.0
        c = np.linalg.solve(A, b)
        return c, float(np.abs(C.sum(axis=0) - 1.0).max())

    def _buffers(self, two):
        if self._buf is None:
            self._buf = np.empty(self.N, dtype=np.float64)
        if two and self._buf2 is None:
            self._buf2 = np.empty(self.N, dtype=np.float64)

    def ceiling_share(self, eps):
        """share_inf(q=1) in closed form -- see LeanQuotient.ceiling_share for why the
        2^k entropy route must not be used here. At q = 1, g_w = 1 for every w, so the
        stationary state is exactly the deposit c on S: H(p_inf) = H(c) on |S| numbers, and
        the low-order Fourier leak is sum_{1<=|T|<=2} chat(T)^2, also on |S| numbers."""
        if self.equivariant:
            # NOT a numerical result and not rounded to one. R_i(a) is i-independent, so
            # dec# of (uniform on S) convolved with ANY radial kernel is uniform on S --
            # that is the criterion itself, and the noise kernel is radial. The deposit at
            # q=1 IS uniform, H = ln|S|, and the ceiling IS share_max. Going through the
            # |S|x|S| Perron solve instead would return share_max +/- 1e-8, because at small
            # eps the subdominant eigenvalue crowds 1 and the solve is ill-conditioned; that
            # 1e-8 would be reported as a restorability deficit and it would be fiction.
            return self.share_max
        c, _ = self.solve_c(1.0, eps)
        Hc = float(-np.sum(np.where(c > 0, c * np.log(np.maximum(c, 1e-320)), 0.0)))
        leak = float(np.sum((self._lowsign @ c) ** 2))
        return self.k * LN2 - Hc - 0.5 * leak

    def ceiling_residual(self, eps):
        """How far the q=1 deposit solve is from its own fixed-point equation, and how far
        the uniform deposit is from being one. Reported so the deficit column carries its
        own error bar instead of an assertion."""
        kap = self.kappa(1.0, eps, 'exact')
        C = (self._cd * kap[None, None, :]).sum(axis=2)
        u = np.full(self.ns, 1.0 / self.ns)
        c, _ = self.solve_c(1.0, eps)
        return dict(resid_solved=float(np.abs(C @ c - c).max()),
                    resid_uniform=float(np.abs(C @ u - u).max()),
                    colsum_dev=float(np.abs(C.sum(axis=0) - 1.0).max()))

    def stat_share(self, q, eps, want=()):
        full = ('flips' in want) or ('pre' in want)
        self._buffers(full)
        lam = 1.0 - 2.0 * eps
        g = RI.g_vec(q, eps, self.k)
        c, colsum = self.solve_c(q, eps)
        buf = self._buf
        buf[:] = 0.0
        buf[self.sidx] = c
        fwht_ip(buf)                                            # buf = chat
        if full:
            self._buf2[:] = buf
        # p = wht(g[pc] * chat) / N, done chunkwise so no full-size temporary appears
        for lo in range(0, self.N, CHUNK):
            hi = min(lo + CHUNK, self.N)
            buf[lo:hi] *= g[self.pc[lo:hi]]
        # the leak: low-order Fourier mass, exactly, from |S|-sized sums
        chat_low = self._lowsign @ c
        phat_low = g[self._loww] * chat_low
        leak = float(np.sum(phat_low ** 2))
        fwht_ip(buf)
        buf /= self.N
        Hp = entropy_chunked(buf)
        mass = float(buf.sum())
        neg = float(min(0.0, float(buf.min())))
        Hc = float(-np.sum(np.where(c > 0, c * np.log(np.maximum(c, 1e-320)), 0.0)))
        out = dict(share=self.k * LN2 - Hp - 0.5 * leak,
                   share_raw=self.k * LN2 - Hp, H=Hp, H_c=Hc, mass=mass, neg=neg,
                   leak=leak, c_iters=0, c_err=colsum)
        if full:
            b2 = self._buf2
            for lo in range(0, self.N, CHUNK):
                hi = min(lo + CHUNK, self.N)
                w = self.pc[lo:hi]
                b2[lo:hi] *= (lam ** w) * g[w]
            leak_pre = float(np.sum(((lam ** self._loww) * phat_low) ** 2))
            fwht_ip(b2)
            b2 /= self.N
            Hpre = entropy_chunked(b2)
            out['H_pre'] = Hpre
            out['share_pre'] = self.k * LN2 - Hpre - 0.5 * leak_pre
            out['mass_pre'] = float(b2.sum())
            out['neg_pre'] = float(min(0.0, float(b2.min())))
            out['leak_pre'] = leak_pre
            if 'flips' in want:
                tot = 0.0
                for lo in range(0, self.N, CHUNK):
                    hi = min(lo + CHUNK, self.N)
                    tot += float(np.sum(np.maximum(b2[lo:hi], 0.0)
                                        * self.mindist[lo:hi].astype(np.float64)))
                out['flips'] = q * tot
        return out

    def pair_dev(self):
        S = self.S
        worst = 0.0
        for i in range(self.k):
            for j in range(i + 1, self.k):
                cnt = np.bincount(S[:, i].astype(int) * 2 + S[:, j].astype(int),
                                  minlength=4)
                worst = max(worst, float(np.abs(cnt / self.ns - 0.25).max()))
        return worst

    def free(self):
        self._buf = self._buf2 = None
        self.pc = self.mindist = None


# =====================================================================================
# the rent measurement — same definitions as the parent, fewer evaluations
# =====================================================================================

_GRID = {}


def _share_of(lat, q, eps):
    return lat.stat_share(q, eps)['share']


def solve_q(lat, eps, target, ngrid=9):
    """The constant q whose stationary share is exactly `target`.

    Bracket on a log-spaced grid (share_inf is increasing in q, gate Q2-G3), then Brent.
    The ceiling is share_inf(q=1), NOT share_max: on a substrate whose decoder is not
    equivariant full upkeep does not restore the design state.
    """
    s_hi = lat.ceiling_share(eps)
    if target > s_hi:
        return None, dict(reason=f'target {target:.6f} above attainable ceiling '
                                 f'{s_hi:.6f} (share_max {lat.share_max:.6f})'), s_hi
    # The bracketing grid depends on (substrate, eps) only, NOT on the target, so it is
    # computed once and reused by all three targets at that eps. At k=27 an evaluation is
    # two transforms of 2^27 doubles; recomputing the grid per target was two thirds of the
    # run. Nothing about the root changes -- Brent still brackets and converges on the
    # same interval.
    # Cached ON THE LATTICE, not in a module dict keyed by id(lat). The first version of
    # this used `id(lat)` as the key; CPython reuses ids after garbage collection, so a
    # freshly built substrate could inherit the previous one's grid and brentq would be
    # handed a bracket that does not bracket. It surfaced as a hard ValueError on the
    # fourth substrate of a re-verification loop, not as a wrong number -- and the
    # per-substrate run jobs were never exposed, because each builds exactly one lattice.
    cache = getattr(lat, '_grid_cache', None)
    if cache is None:
        cache = lat._grid_cache = {}
    key = round(eps, 12)
    grid_s = cache.get(key)
    grid = np.concatenate([[1e-9], np.logspace(-4, 0, ngrid)])
    if grid_s is None:
        grid_s = [lat.stat_share(float(q), eps)['share'] if q < 1.0 else s_hi
                  for q in grid]
        cache[key] = grid_s
    lo, hi = grid[0], 1.0
    for i in range(len(grid) - 1):
        if grid_s[i] <= target <= grid_s[i + 1]:
            lo, hi = grid[i], grid[i + 1]
            break
    q = brentq(lambda x: _share_of(lat, x, eps) - target, lo, hi,
               xtol=1e-13, rtol=1e-14, maxiter=200)
    r = lat.stat_share(q, eps, want=('flips', 'pre'))
    return q, r, s_hi


def measure_rent(lat, eps, target, mode, target_label):
    """One pre-registered row, schema identical to rent_islands.measure_rent."""
    q, r, s_hi = solve_q(lat, eps, target)
    row = dict(tag=lat.tag, arm=lat.arm, k=lat.k, ns=lat.ns, m=lat.m,
               d=lat.d, kind=lat.kind, route=lat.route, name=lat.name,
               equivariant=bool(getattr(lat, 'equivariant', True)),
               equiv_dev=float(getattr(lat, 'equiv_dev', 0.0)),
               profile_dev=float(getattr(lat, 'profile_dev', 0.0)),
               share_max=lat.share_max, density=lat.density,
               eps=eps, mode=mode, target_label=target_label, target=float(target))
    if q is None:
        row.update(dropped=True, drop_reason=r['reason'])
        return row
    achieved = r['share']
    resid = abs(achieved - target) / max(target, 1e-30)
    cost_erase = q * (r['H_pre'] - r['H_c'])
    row.update(
        q_star=float(q), achieved=float(achieved),
        achieved_frac=float(achieved / lat.share_max),
        ceiling=float(s_hi), ceiling_frac=float(s_hi / lat.share_max),
        target_resid_rel=float(resid), share_pre=float(r['share_pre']),
        cost_erase=float(cost_erase), cost_flips=float(r.get('flips', np.nan)),
        rent_per_nat=float(cost_erase / achieved),
        flips_per_nat=float(r.get('flips', np.nan) / achieved),
        mass_dev=float(abs(r['mass'] - 1.0)), neg_mass=float(r['neg']),
        pair_leak=float(r.get('leak', 0.0)),
        Hc_deficit=float(np.log(lat.ns) - r['H_c']),
        share_raw=float(r.get('share_raw', achieved)),
        leak_correction_rel=float(0.5 * r.get('leak', 0.0) / achieved),
        leak_residual_rel=float(r.get('leak', 0.0) ** 2 / achieved),
        c_iters=int(r.get('c_iters', 0)), c_err=float(r.get('c_err', 0.0)),
        # ceiling fractions, per the standing requirement (prereg §0)
        frac_of_share_max=float(achieved / lat.share_max),
        frac_of_lean_cap=float(achieved / ((lat.k - 3) * LN2)),
        dropped=False, drop_reason='')
    if resid > 1e-6:
        row.update(dropped=True, drop_reason=f'target residual {resid:.2e} > 1e-6')
    if not (1e-9 < q < 1 - 1e-9):
        row.update(dropped=True, drop_reason=f'q* saturated at {q:.3e}')
    return row


# =====================================================================================
# roster for the extension
# =====================================================================================

def build_one(arm, k):
    """ARM A: the minimum-size OA at k. ARM B: best linear [k, ceil(log2(k+1))]."""
    if arm == 'A':
        n0 = DC.N0(k)
        if (n0 & (n0 - 1)) == 0:
            G = RI.simplex_generator(k, int(np.log2(n0)))
            L = LeanQuotient(f'A{k}', 'A', k, G,
                             name=f'OA({n0},{k},2,2) [{DC.had_source(n0)}]')
        else:
            L = LeanFull(f'A{k}', 'A', k, DC.maxshare_oa(k),
                         name=f'OA({n0},{k},2,2) [{DC.had_source(n0)}]')
        return L
    m, cols, how = DC.armB_columns(k)
    L = LeanQuotient(f'B{k}', 'B', k, RI.MS.cols_to_G(m, cols),
                     name=f'linear [{k},{m}] ({how})')
    L.cols = list(map(int, cols))
    return L


EPS = [0.01, 0.05]
FRACS = [0.1, 0.5]
ABS_LEVELS = [1.0]


def sweep_one(arm, k):
    t0 = time.time()
    L = build_one(arm, k)
    rows = []
    for eps in EPS:
        for fr in FRACS:
            rows.append(measure_rent(L, eps, fr * L.share_max, 'frac', f'{fr}'))
        for s in ABS_LEVELS:
            if s < 0.98 * L.share_max:
                rows.append(measure_rent(L, eps, s, 'abs', f'{s}nat'))
    meta = dict(tag=L.tag, arm=arm, k=k, ns=L.ns, route=L.route, name=L.name,
                share_max=L.share_max, density=L.density, d=L.d,
                pair_dev=float(L.pair_dev()),
                profile_dev=float(getattr(L, 'profile_dev', 0.0)),
                secs=round(time.time() - t0, 1))
    if hasattr(L, 'free'):
        L.free()
    return rows, meta


# =====================================================================================
# GATES
# =====================================================================================

def gates():
    print("=" * 84)
    print("Q2 GATES (prereg §4)")
    print("=" * 84)
    ok = True

    print("\n--- Q2-G2: blocked in-place WHT == the parent's, 2^18..2^22 ---")
    g2 = True
    rng = np.random.default_rng(7)
    for r in (18, 20, 22):
        a = rng.standard_normal(1 << r)
        x, y = RI.wht(a), fast_wht(a)
        rel = float(np.abs(x - y).max() / max(1e-30, np.abs(x).max()))
        good = rel < 1e-13
        g2 &= good
        print(f"  2^{r}: max rel diff {rel:.2e}  {'OK' if good else 'FAIL'}")
    print(f"  Q2-G2 {'PASS' if g2 else 'FAIL'}")
    ok &= g2

    print("\n--- Q2-G4: new substrates pair-uniform, share_max = k ln2 - ln|S| ---")
    g4 = True
    for N in (28, 32):
        H = DC.hadamard(N)
        assert np.array_equal(H @ H.T, N * np.eye(N, dtype=int))
    for arm, k in (('A', 25), ('A', 27), ('A', 28), ('A', 31), ('B', 25), ('B', 31)):
        L = build_one(arm, k)
        pd = L.pair_dev()
        sm = k * LN2 - np.log(L.ns)
        good = pd < 1e-12 and abs(sm - L.share_max) < 1e-12
        g4 &= good
        print(f"  {arm}{k:<3d} |S|={L.ns:3d} route={L.route:12s} pair_dev={pd:.2e} "
              f"share_max={L.share_max:.10f}  {'OK' if good else 'FAIL'}")
        if hasattr(L, 'free'):
            L.free()
    print(f"  Q2-G4 {'PASS' if g4 else 'FAIL'}")
    ok &= g4

    print("\n--- Q2-G1: lean solver reproduces rent_islands rows at k = 20..24 ---")
    RJ = json.load(open(os.path.join(HERE, 'rent_islands_results.json')))
    want = {}
    for r in RJ['rows']:
        if r.get('dropped'):
            continue
        want[(r['tag'], r['eps'], r['mode'], r['target_label'])] = r
    g1 = True
    for arm, k in (('A', 20), ('A', 22), ('A', 23), ('A', 24),
                   ('B', 20), ('B', 22), ('B', 24), ('A', 13), ('A', 15)):
        L = build_one(arm, k)
        for eps in (0.01, 0.05):
            for fr in (0.1, 0.5):
                key = (f'{arm}{k}', eps, 'frac', f'{fr}')
                if key not in want:
                    continue
                w = want[key]
                got = measure_rent(L, eps, fr * L.share_max, 'frac', f'{fr}')
                # `ceiling` is deliberately NOT in this list: at q=1 the parent sums an
                # entropy over 2^k cells of which 2^k - |S| are exactly zero, so its last
                # ~9 digits are roundoff. The lean solver uses the closed form instead and
                # is checked against it by Q2-G6. Everything else must match to 1e-10.
                fields = ('q_star', 'achieved', 'rent_per_nat', 'cost_erase',
                          'cost_flips', 'share_pre')
                worst, wf = 0.0, ''
                for f in fields:
                    a, b = w[f], got[f]
                    rel = abs(a - b) / max(1e-30, abs(a))
                    if rel > worst:
                        worst, wf = rel, f
                good = worst < 1e-10
                g1 &= good
                print(f"  {arm}{k:<3d} eps={eps} frac={fr}: worst rel {worst:.2e} ({wf})"
                      f"  {'OK' if good else 'MISMATCH'}")
        if hasattr(L, 'free'):
            L.free()
    print(f"  Q2-G1 {'PASS' if g1 else 'FAIL'}")
    ok &= g1

    print("\n--- Q2-G6: the q=1 ceiling, closed form vs the 2^k entropy sum ---")
    print("  (this gate exists because Q2-G1 FIRED on the parent's `ceiling` column: the")
    print("   2^k route pollutes it with roundoff mass on cells that are exactly zero)")
    g6 = True
    for arm, k in (('A', 16), ('A', 20), ('A', 23), ('A', 24), ('B', 20)):
        L = build_one(arm, k)
        eq = getattr(L, 'equivariant', True)
        for eps in (0.01, 0.05):
            exact = L.ceiling_share(eps)
            summed = L.stat_share(1.0, eps)['share']
            good = abs(exact - summed) < 1e-6
            extra = ''
            if hasattr(L, 'ceiling_residual'):
                rr = L.ceiling_residual(eps)
                extra = (f" resid(solved) {rr['resid_solved']:.1e}"
                         f" resid(uniform) {rr['resid_uniform']:.1e}")
                # ONE direction only, and the first version of this clause got it wrong.
                # The theorem says equivariant => the uniform deposit is EXACTLY a fixed
                # point, so resid(uniform) must be at machine zero there. It does NOT say
                # the converse: a lossy structure can read an arbitrarily small residual at
                # small eps, because R_i(a) differs only at large a and the noise kernel
                # carries weight eps^a there. A20 at eps=0.01 reads 9.2e-15 and is lossy.
                # That eps-dependence is physics and is reported in the results, not gated.
                good &= ((not eq) or rr['resid_uniform'] < 1e-13)
            g6 &= good
            print(f"  {arm}{k:<3d} eps={eps}: ceiling {exact:.14f}  2^k-sum {summed:.14f}"
                  f"  equiv={eq}{extra}  {'OK' if good else 'FAIL'}")
        if hasattr(L, 'free'):
            L.free()
    print(f"  Q2-G6 {'PASS' if g6 else 'FAIL'}")
    ok &= g6

    print("\n--- Q2-G7: the noise kernel, three routes (the Q2-G6 defect, quantified) ---")
    g7 = True
    for k in (16, 20, 23):
        L = build_one('A', k)
        for eps in (0.01, 0.05):
            ke = L.kappa(1.0, eps, 'exact')
            ks = L.kappa(1.0, eps, 'series')
            kk = L.kappa(1.0, eps, 'kraw')
            d_es = float(np.abs(ke - ks).max())
            d_ek = float(np.abs(ke - kk).max())
            neg = int((kk < 0).sum())
            good = d_es < 1e-15
            g7 &= good
            print(f"  A{k:<3d} eps={eps}: |exact-series| {d_es:.2e}   "
                  f"|exact-Krawtchouk| {d_ek:.2e}   Krawtchouk cells that came out "
                  f"NEGATIVE: {neg}/{k+1}  {'OK' if good else 'FAIL'}")
        L.free()
    print(f"  Q2-G7 {'PASS' if g7 else 'FAIL'}")
    ok &= g7

    print("\n--- Q2-G3: share_inf(q) strictly increasing at every new k ---")
    g3 = True
    for arm, k in (('A', 25), ('A', 28), ('A', 31), ('B', 27)):
        L = build_one(arm, k)
        qs = np.logspace(-4, -0.02, 12)
        ss = [L.stat_share(float(q), 0.05)['share'] for q in qs]
        mono = all(ss[i] < ss[i + 1] for i in range(len(ss) - 1))
        g3 &= mono
        print(f"  {arm}{k:<3d} monotone={mono}  share range "
              f"[{ss[0]:.3e}, {ss[-1]:.4f}] of {L.share_max:.4f}")
        if hasattr(L, 'free'):
            L.free()
    print(f"  Q2-G3 {'PASS' if g3 else 'FAIL'}")
    ok &= g3

    print("\n" + "=" * 84)
    print(f"Q2 GATES: {'ALL PASS' if ok else 'FAILURE — run stops'}")
    print("=" * 84)
    return ok


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate', action='store_true')
    ap.add_argument('--one', nargs=2, metavar=('ARM', 'K'))
    ap.add_argument('--out', default=None)
    a = ap.parse_args()
    RI.wht = fast_wht                     # the quotient route uses the blocked transform
    if a.gate:
        t = time.time()
        good = gates()
        print(f"[{time.time()-t:.1f}s]")
        sys.exit(0 if good else 1)
    if a.one:
        arm, k = a.one[0], int(a.one[1])
        rows, meta = sweep_one(arm, k)
        out = a.out or os.path.join(HERE, f'rent_scaling_q2_{arm}{k}.json')
        json.dump(dict(rows=rows, meta=meta), open(out, 'w'), indent=1)
        print(f"{arm}{k}: {len(rows)} rows, {meta['secs']}s -> {out}")
