#!/usr/bin/env python3
"""Two-sided gauge for the TIER-3 dose arms, driving dose_adjudicate.adjudicate."""
from dose_adjudicate import adjudicate
mk = lambda r, p75: {"T_organize": {"momx_resid": r, "rand_p75": p75}}
r = adjudicate(mk(14.0, 5.0), mk(6.0, 4.0))
assert all(v["pass"] for v in r.values()), r
print("planted truth (14.0 -> 6.0, in band): PASS all three")
r = adjudicate(mk(3.0, 5.0), mk(6.0, 4.0))
assert not r["D1_organization_at_30"]["pass"] and not r["D2_monotone"]["pass"]
print("planted no-organization-at-30 + inverted dose: FIRE D1, FIRE D2")
r = adjudicate(mk(14.0, 5.0), mk(1.2, 4.0))
assert not r["D3_interpolation"]["pass"] and r["D2_monotone"]["pass"]
print("planted out-of-band 120 (1.2 < 2.53): FIRE D3 alone -- prong named")
r = adjudicate(mk(14.0, 5.0), mk(13.5, 4.0))
assert not r["D3_interpolation"]["pass"]
print("planted high-side 120 (13.5 > 12.34): FIRE D3 high prong")
print("gauge verdict: dose arms PASS planted truth and FIRE each prong by name. Two-sided.")
