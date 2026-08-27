#!/usr/bin/env python3
"""Two-sided gauge for NABLA-1's V1 arm: bands pearson >= 0.99, slope in [0.90, 1.10].
Drives the real leg/loop machinery on planted fields."""
import numpy as np
from nabla_adjudicate import leg
rng = np.random.default_rng(20260827)
NY, NX = 16, 32

def planted(mass_ratio, coeff_err=1.0, drop_cross=False):
    """Smooth field + lumpy-or-not mass; returns (H_meas, H_pred) interior."""
    y, x = np.mgrid[0:NY, 0:NX]
    Hm_all, Hp_all = [], []
    for k in range(8):
        phi = np.sin(2*np.pi*(x/NX + 0.13*k)) * np.cos(2*np.pi*(y/NY - 0.07*k)) + 0.3*rng.standard_normal((NY, NX))*0
        m0 = 1.0 + (mass_ratio-1.0)*rng.random((NY, NX))
        g = [{"mass": m0, "phi": phi}]
        # charts 1-3 mass fields: same lumpiness pattern (static scene approx)
        for _ in range(3): g.append({"mass": m0})
        p = leg(phi, g[0]["mass"],'x',True); p = leg(p, g[1]["mass"],'y',True)
        p = leg(p, g[2]["mass"],'x',False); p = leg(p, g[3]["mass"],'y',False)
        H = p - phi
        Dx = np.full_like(phi, np.nan); Dy = np.full_like(phi, np.nan)
        Dx[:,1:-1] = phi[:,2:]-2*phi[:,1:-1]+phi[:,:-2]
        Dy[1:-1,:] = phi[2:,:]-2*phi[1:-1,:]+phi[:-2,:]
        Dxy = np.full_like(phi, np.nan)
        Dxy[1:-1,1:-1] = Dx[2:,1:-1]-2*Dx[1:-1,1:-1]+Dx[:-2,1:-1]
        Hp = coeff_err*(Dx/4 + Dy/4) + (0 if drop_cross else Dxy/16)
        ok = np.isfinite(H) & np.isfinite(Hp)
        ok[0,:]=ok[-1,:]=False; ok[:,0]=ok[:,-1]=False
        Hm_all.append(H[ok]); Hp_all.append(Hp[ok])
    Hm, Hp = np.concatenate(Hm_all), np.concatenate(Hp_all)
    return float(np.corrcoef(Hm,Hp)[0,1]), float(np.polyfit(Hp,Hm,1)[0]), len(Hm)

def band(r, sl): return r >= 0.99 and 0.90 <= sl <= 1.10

r, sl, n = planted(1.1)
print(f"planted truth (mass ratio 1.1, true operator): r={r:.5f} slope={sl:.4f} n={n} -> {'PASS' if band(r,sl) else 'BAND ERROR'}")
assert band(r, sl)
r2, sl2, _ = planted(1.1, coeff_err=2.0)
print(f"planted wrong coefficient (x2): r={r2:.5f} slope={sl2:.4f} -> {'FIRE slope' if not band(r2,sl2) else 'MISSED'}")
assert not band(r2, sl2)
r3, sl3, _ = planted(1.1, coeff_err=0.5)
print(f"planted wrong coefficient (/2): slope={sl3:.4f} -> {'FIRE slope' if not band(r3,sl3) else 'MISSED'}")
assert not band(r3, sl3)
# uniform-weight null control: mass ratio exactly 1 -> H == Hp to machine precision
y, x = np.mgrid[0:NY, 0:NX]
phi = np.sin(2*np.pi*x/NX)*np.cos(2*np.pi*y/NY)
m1 = np.ones((NY, NX))
p = leg(phi, m1,'x',True); p = leg(p, m1,'y',True); p = leg(p, m1,'x',False); p = leg(p, m1,'y',False)
H = p - phi
Dx = np.full_like(phi, np.nan); Dy = np.full_like(phi, np.nan)
Dx[:,1:-1] = phi[:,2:]-2*phi[:,1:-1]+phi[:,:-2]; Dy[1:-1,:] = phi[2:,:]-2*phi[1:-1,:]+phi[:-2,:]
Dxy = np.full_like(phi, np.nan); Dxy[1:-1,1:-1] = Dx[2:,1:-1]-2*Dx[1:-1,1:-1]+Dx[:-2,1:-1]
Hp = Dx/4+Dy/4+Dxy/16
ok = np.isfinite(H)&np.isfinite(Hp); ok[0,:]=ok[-1,:]=False; ok[:,0]=ok[:,-1]=False
nullmax = float(np.abs(H-Hp)[ok].max())
print(f"uniform-weight NULL CONTROL: max|H-Hp| = {nullmax:.2e} -> {'premise OK' if nullmax <= 1e-12 else 'PIPELINE DEFECT'}")
assert nullmax <= 1e-12
print("gauge verdict: V1 PASSES the true operator, FIRES on coefficient errors both ways,")
print("and the uniform-weight null control validates the derivation is EXACT. Two-sided.")
