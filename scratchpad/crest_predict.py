"""
Does the extensive branch PREDICT its crossing redshift, or must it be tuned?

The extensive reading: rho_DE  ∝  S_total per comoving volume, where S_total is
the repo's own equicorrelation coordination (Core/Intensive.lean):

    S(k, rho) = -(k-1) ln(1-rho) - ln(1 + (k-1) rho)

Large-k limit, per comoving volume V (k = n V):

    S/V  ->  n(z) * [ -ln(1 - rho(z)) ]        ==   N * s

  n(z)   = comoving number density of collapsed halos above M_min  (Sheth-Tormen)
  rho(z) = correlation coefficient between two units at their mean separation,
           for the density field smoothed on the unit scale:
              rho = xi_R(d, z) / sigma^2(R, z),   d = n^{-1/3}

Everything is fixed by standard LCDM + the halo threshold M_min. NO free
parameter is tuned to the answer.

Crest (== phantom crossing, since rhodot=0 <=> w=-1):  d/dz [ n * s ] = 0.

The extensive branch's frozen kill window is z_c = 0.59 +/- 0.03.
"""
import numpy as np
from scipy.integrate import simpson
from scipy.optimize import brentq
from scipy.interpolate import CubicSpline

# ---------------- Planck-2018-like LCDM ----------------
Om, Ob, h, ns, s8 = 0.315, 0.0493, 0.674, 0.965, 0.811
OL = 1.0 - Om
Tcmb = 2.7255
rho_crit_0 = 2.775e11 * h**2          # Msun / Mpc^3  (comoving, Omega=1 units)
rho_m_bar = Om * 2.775e11             # Msun/h per (Mpc/h)^3


# ---------------- growth factor ----------------
def E(z):
    return np.sqrt(Om * (1 + z) ** 3 + OL)


def growth_D(z):
    """Linear growth factor, normalised D(0)=1."""
    zz = np.atleast_1d(z).astype(float)
    out = np.empty_like(zz)
    for i, zi in enumerate(zz):
        a = np.linspace(1e-6, 1.0 / (1.0 + zi), 4000)
        integ = 1.0 / (a * E(1.0 / a - 1.0)) ** 3
        out[i] = 2.5 * Om * E(zi) * simpson(integ, x=a)
    a0 = np.linspace(1e-6, 1.0, 4000)
    norm = 2.5 * Om * E(0.0) * simpson(1.0 / (a0 * E(1.0 / a0 - 1.0)) ** 3, x=a0)
    return (out / norm) if out.size > 1 else float(out[0] / norm)


# ---------------- Eisenstein & Hu 1998 transfer function (full, with BAO) ----------
def T_EH98(k_hMpc):
    """k in h/Mpc. Returns transfer function."""
    k = k_hMpc * h                                  # -> 1/Mpc
    theta = Tcmb / 2.7
    omh2, obh2 = Om * h**2, Ob * h**2
    fb = Ob / Om

    zeq = 2.5e4 * omh2 * theta**-4
    keq = 7.46e-2 * omh2 * theta**-2                # 1/Mpc
    b1 = 0.313 * omh2**-0.419 * (1 + 0.607 * omh2**0.674)
    b2 = 0.238 * omh2**0.223
    zd = 1291 * omh2**0.251 / (1 + 0.659 * omh2**0.828) * (1 + b1 * obh2**b2)
    Req = 31.5 * obh2 * theta**-4 * (1000.0 / zeq)
    Rd = 31.5 * obh2 * theta**-4 * (1000.0 / zd)
    s_h = (2.0 / (3 * keq) * np.sqrt(6.0 / Req)
           * np.log((np.sqrt(1 + Rd) + np.sqrt(Rd + Req)) / (1 + np.sqrt(Req))))
    ksilk = 1.6 * obh2**0.52 * omh2**0.73 * (1 + (10.4 * omh2) ** -0.95)

    q = k / (13.41 * keq)
    ks = k * s_h

    a1 = (46.9 * omh2) ** 0.670 * (1 + (32.1 * omh2) ** -0.532)
    a2 = (12.0 * omh2) ** 0.424 * (1 + (45.0 * omh2) ** -0.582)
    alpha_c = a1 ** (-fb) * a2 ** (-(fb**3))
    bb1 = 0.944 / (1 + (458 * omh2) ** -0.708)
    bb2 = (0.395 * omh2) ** -0.0266
    beta_c = 1.0 / (1 + bb1 * ((1 - fb) ** bb2 - 1))

    def T0(kk, ac, bc):
        C = 14.2 / ac + 386.0 / (1 + 69.9 * q**1.08)
        return np.log(np.e + 1.8 * bc * q) / (np.log(np.e + 1.8 * bc * q) + C * q**2)

    f = 1.0 / (1 + (ks / 5.4) ** 4)
    Tc = f * T0(k, 1.0, beta_c) + (1 - f) * T0(k, alpha_c, beta_c)

    y = (1.0 + zeq) / (1.0 + zd)
    Gy = y * (-6 * np.sqrt(1 + y)
              + (2 + 3 * y) * np.log((np.sqrt(1 + y) + 1) / (np.sqrt(1 + y) - 1)))
    alpha_b = 2.07 * keq * s_h * (1 + Rd) ** -0.75 * Gy
    beta_b = 0.5 + fb + (3 - 2 * fb) * np.sqrt((17.2 * omh2) ** 2 + 1)
    beta_node = 8.41 * omh2**0.435
    st = s_h / (1 + (beta_node / ks) ** 3) ** (1.0 / 3.0)

    Tb = (T0(k, 1.0, 1.0) / (1 + (ks / 5.2) ** 2)
          + alpha_b / (1 + (beta_b / ks) ** 3) * np.exp(-((k / ksilk) ** 1.4))) \
        * np.sin(k * st) / (k * st)

    return fb * Tb + (1 - fb) * Tc


# ---------------- power spectrum, normalised to sigma8 ----------------
kgrid = np.logspace(-4, 3, 3000)                    # h/Mpc
Tk = T_EH98(kgrid)
Pk_unnorm = kgrid**ns * Tk**2


def W_th(x):
    x = np.where(x < 1e-6, 1e-6, x)
    return 3.0 * (np.sin(x) - x * np.cos(x)) / x**3


def sigma2_unnorm(R):
    return simpson(kgrid**2 * Pk_unnorm * W_th(kgrid * R) ** 2, x=kgrid) / (2 * np.pi**2)


Anorm = s8**2 / sigma2_unnorm(8.0)
Pk = Anorm * Pk_unnorm                              # z=0 linear P(k)


def sigma_M(M):
    """M in Msun/h -> sigma(M) at z=0."""
    R = (3 * M / (4 * np.pi * rho_m_bar)) ** (1.0 / 3.0)
    return np.sqrt(Anorm * sigma2_unnorm(R)), R


# ---------------- Sheth-Tormen mass function ----------------
dc = 1.686
ST_A, ST_a, ST_p = 0.3222, 0.707, 0.3


def n_above(Mmin, z, nM=140):
    """Comoving number density of halos with M > Mmin, in (h/Mpc)^3."""
    D = growth_D(z)
    lnM = np.linspace(np.log(Mmin), np.log(1e16), nM)
    Ms = np.exp(lnM)
    sig = np.array([sigma_M(M)[0] for M in Ms]) * D
    dlnsig_dlnM = np.gradient(np.log(sig), lnM)
    nu = dc / sig
    fST = ST_A * np.sqrt(2 * ST_a / np.pi) * (1 + (1 / (ST_a * nu**2)) ** ST_p) \
        * nu * np.exp(-ST_a * nu**2 / 2)
    dndlnM = fST * (rho_m_bar / Ms) * (-dlnsig_dlnM)
    return simpson(dndlnM, x=lnM)


# ---------------- correlation of the unit-smoothed field ----------------
def xi_smoothed(r, R, D):
    """xi of the density field smoothed on scale R, at separation r."""
    integ = kgrid**2 * Pk * W_th(kgrid * R) ** 2 * np.sinc(kgrid * r / np.pi)
    return D**2 * simpson(integ, x=kgrid) / (2 * np.pi**2)


def sigma2_smoothed(R, D):
    return D**2 * Anorm * sigma2_unnorm(R)


# ---------------- the coordination density and its crest ----------------
def coordination_density(z, Mmin):
    """N * s  =  n(z) * [ -ln(1 - rho(z)) ]   (per comoving (Mpc/h)^3)."""
    D = growth_D(z)
    n = n_above(Mmin, z)
    _, R = sigma_M(Mmin)
    d = n ** (-1.0 / 3.0)                            # mean separation, Mpc/h
    xi = xi_smoothed(d, R, D)
    s2 = sigma2_smoothed(R, D)
    rho_corr = np.clip(xi / s2, -0.999, 0.999)
    return n * (-np.log(1.0 - rho_corr)), n, rho_corr


def find_crest(Mmin, zlo=0.01, zhi=6.0, nz=48):
    zs = np.linspace(zlo, zhi, nz)
    vals, ns, rhos = [], [], []
    for z in zs:
        v, n, rc = coordination_density(z, Mmin)
        vals.append(v); ns.append(n); rhos.append(rc)
    vals = np.array(vals)
    lg = np.log(vals)
    spl = CubicSpline(zs, lg)
    dspl = spl.derivative()
    # crest = stationary point of ln(N s) in z
    roots = []
    for i in range(len(zs) - 1):
        if dspl(zs[i]) * dspl(zs[i + 1]) < 0:
            roots.append(brentq(dspl, zs[i], zs[i + 1]))
    return zs, vals, np.array(ns), np.array(rhos), roots


if __name__ != "__main__":
    import sys
    sys.modules[__name__].__demo__ = False

_DEMO = (__name__ == "__main__")
if _DEMO:
  print("=" * 72)
  print("EXTENSIVE-BRANCH CREST FROM STANDARD LCDM STRUCTURE FORMATION")
  print("frozen kill window for the crossing:  z_c = 0.59 +/- 0.03")
  print("=" * 72)

  for Mmin in [1e11, 1e12, 1e13, 1e14]:
    zs, vals, ns, rhos, roots = find_crest(Mmin)
    print(f"\nM_min = {Mmin:.0e} Msun/h")
    print(f"  n(z=0) = {ns[0]:.3e} (h/Mpc)^3   mean sep = {ns[0]**(-1/3):.2f} Mpc/h")
    print(f"  rho_corr(z=0) = {rhos[0]:.4f}   rho_corr(z=3) = {rhos[np.argmin(abs(zs-3))]:.4f}")
    if roots:
        print(f"  CREST at z_c = {[f'{r:.3f}' for r in roots]}")
    else:
        mono = "monotonically INCREASING toward z=0" if vals[0] > vals[-1] \
            else "monotonically DECREASING toward z=0"
        print(f"  NO CREST in z=[0.01,6] -- N*s is {mono}")
        print(f"    N*s(z=0)={vals[0]:.4e}  N*s(z=1)={vals[np.argmin(abs(zs-1))]:.4e}"
              f"  N*s(z=3)={vals[np.argmin(abs(zs-3))]:.4e}")
