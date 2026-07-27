"""Independent check of PUMP_RESULTS.md sec 2: does valve_needs_asymmetry fail at k>=4?
Includes the character-theoretic REASON, checked rather than asserted."""
import itertools, math, sys
import numpy as np
sys.path.insert(0,"/home/emoore/CIRISOntology/scratchpad")
import pump_curve as PC
LN2=math.log(2.0); ok=lambda b:"PASS" if b else "**FAIL**"

def signsym_err(p):
    k=p.ndim; f=p
    for i in range(k): f=np.flip(f,axis=i)
    return float(np.abs(p-f).max())

print("Mechanism: under the global flip a Fourier character chi_S -> (-1)^|S| chi_S,")
print("so sign symmetry kills ODD-|S| coefficients only.  The PAIR-BLIND directions are")
print("|S| >= 3.  At k=3 the only one is |S|=3 (ODD -> killed).  At k=4 there is also")
print("|S|=4 (EVEN -> survives).  So the k=3 vanishing is an accident of k=3.")
print()
print(f"{'k':>3}{'pair-blind |S|':>18}{'odd (killed)':>14}{'even (survive)':>16}")
for k in (3,4,5,6,7):
    tot=[len(list(itertools.combinations(range(k),w))) for w in range(k+1)]
    odd=sum(tot[w] for w in range(3,k+1) if w%2==1)
    ev =sum(tot[w] for w in range(3,k+1) if w%2==0)
    print(f"{k:>3}{str(list(range(3,k+1))):>18}{odd:>14}{ev:>16}")

print()
print("Measured: sign-symmetric input, UNITAL channel (a=0), share of the output.")
print(f"{'k':>3}{'s':>7}{'input share':>14}{'output share':>14}{'signsym err':>13}{'/(k-2)ln2':>11}")
for k in (3,4,5,6,7):
    for s in (0.05,0.1,0.2):
        p=PC.repetition(k)
        q=PC.apply_percell(p,[PC.kernel(0.0,s)]*k)
        si=PC.share_dual(p)["share_upper"] if k>3 else PC.share3(p)[0]
        so=PC.share_dual(q)["share_upper"] if k>3 else PC.share3(q)[0]
        cf=so/((k-2)*LN2)
        print(f"{k:>3}{s:7.2f}{si:14.3e}{so:14.6e}{signsym_err(q):13.1e}{cf:11.4f}")
print()
print("Cross-check the k=4 output's Fourier weight: is the surviving share carried by")
print("the |S|=4 character?")
k=4; q=PC.apply_percell(PC.repetition(k),[PC.kernel(0.0,0.1)]*k).ravel()
cells=np.array(list(itertools.product((0,1),repeat=k))); z=1.0-2.0*cells
for S in itertools.chain.from_iterable(itertools.combinations(range(k),w) for w in range(1,k+1)):
    ch=np.prod(z[:,list(S)],axis=1); c=float(q@ch)
    if abs(c)>1e-12: print(f"   |S|={len(S)} S={S}  coefficient={c:+.6f}")
