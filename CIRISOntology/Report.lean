/-
CIRISOntology.Report — the published page, generated from the source of truth.

Every word of prose and every number in the figures on the published site is read
from `Stance.lean` and `Core/Epistemics.lean` by the code below. There is no
second copy of the stance anywhere, so the page cannot drift from the repository:
to change what we claim in public you must change the Lean and let CI republish.

The figures are emitted as plain SVG strings built here rather than through a
widget toolkit, so they render on a static page with no JavaScript and no
external assets.
-/
import CIRISOntology.Stance

namespace CIRISOntology.Report

open CIRISOntology.Core

/-- Escape the few characters that would otherwise break the markup. -/
def esc (s : String) : String :=
  s.replace "&" "&amp;" |>.replace "<" "&lt;" |>.replace ">" "&gt;"

def statusClass : Status → String
  | .proved       => "proved"
  | .measured     => "measured"
  | .openQuestion => "open"
  | .wager        => "wager"

/-- What each strength label licenses — printed next to the badge so a reader
    cannot mistake one for another. -/
def statusGloss : Status → String
  | .proved       => "machine-checked in this repository, from stated assumptions"
  | .measured     => "established by observation, to a stated precision, on a stated domain"
  | .openQuestion => "named, unresolved, and not leaned on"
  | .wager        => "an avowed choice under uncertainty — not evidence"

def countBy (st : Status) (cs : List Claim) : Nat :=
  cs.foldl (fun n c => if c.status = st then n + 1 else n) 0

/-- THE CENTRAL FIGURE. Three things, every pair independent, yet the triple
    fully determined — the situation in which our instrument reads exactly zero
    while real coordination is present. This is the whole claim in one picture. -/
def triadSvg : String :=
  "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 460 300\" width=\"460\" height=\"300\" role=\"img\" aria-label=\"Three variables, pairwise independent, jointly coordinated\">\n" ++
  "  <defs><style>\n" ++
  "    .node{fill:#2f6fb2;}\n" ++
  "    .lbl{font:600 15px system-ui,sans-serif;fill:#fff;text-anchor:middle;}\n" ++
  "    .edge{stroke:#b9c2cc;stroke-width:2;stroke-dasharray:5 4;}\n" ++
  "    .edgelbl{font:12px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "    .fill{fill:#e4572e;fill-opacity:.14;stroke:#e4572e;stroke-width:1.5;}\n" ++
  "    .cap{font:13px system-ui,sans-serif;fill:#e4572e;text-anchor:middle;font-weight:600;}\n" ++
  "    .sub{font:12px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "  </style></defs>\n" ++
  "  <polygon class=\"fill\" points=\"230,70 120,225 340,225\"/>\n" ++
  "  <line class=\"edge\" x1=\"230\" y1=\"70\" x2=\"120\" y2=\"225\"/>\n" ++
  "  <line class=\"edge\" x1=\"230\" y1=\"70\" x2=\"340\" y2=\"225\"/>\n" ++
  "  <line class=\"edge\" x1=\"120\" y1=\"225\" x2=\"340\" y2=\"225\"/>\n" ++
  "  <text class=\"edgelbl\" x=\"158\" y=\"142\">no link</text>\n" ++
  "  <text class=\"edgelbl\" x=\"303\" y=\"142\">no link</text>\n" ++
  "  <text class=\"edgelbl\" x=\"230\" y=\"244\">no link</text>\n" ++
  "  <text class=\"cap\" x=\"230\" y=\"170\">all the coordination is here</text>\n" ++
  "  <circle class=\"node\" cx=\"230\" cy=\"70\" r=\"26\"/><text class=\"lbl\" x=\"230\" y=\"75\">A</text>\n" ++
  "  <circle class=\"node\" cx=\"120\" cy=\"225\" r=\"26\"/><text class=\"lbl\" x=\"120\" y=\"230\">B</text>\n" ++
  "  <circle class=\"node\" cx=\"340\" cy=\"225\" r=\"26\"/><text class=\"lbl\" x=\"340\" y=\"230\">C</text>\n" ++
  "  <text class=\"sub\" x=\"230\" y=\"285\">Check any two: independent. Check all three: perfectly locked together.</text>\n" ++
  "</svg>\n"

/-- The ledger of claim strengths, drawn from the stance itself. -/
def statusBarSvg (cs : List Claim) : String :=
  let n := cs.length
  let w : Nat := 420
  let seg (k : Nat) : Nat := if n = 0 then 0 else w * k / n
  let p := countBy .proved cs
  let m := countBy .measured cs
  let o := countBy .openQuestion cs
  let g := countBy .wager cs
  let x1 := seg p
  let x2 := seg (p + m)
  let x3 := seg (p + m + o)
  "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 440 96\" width=\"440\" height=\"96\" role=\"img\" aria-label=\"How many claims are proved, measured, open, or wagers\">\n" ++
  "  <defs><style>.t{font:12px system-ui,sans-serif;fill:#5b6774}.k{font:600 12px system-ui,sans-serif}</style></defs>\n" ++
  s!"  <rect x=\"10\" y=\"18\" width=\"{x1}\" height=\"26\" fill=\"#2e7d32\"/>\n" ++
  s!"  <rect x=\"{10 + x1}\" y=\"18\" width=\"{x2 - x1}\" height=\"26\" fill=\"#2f6fb2\"/>\n" ++
  s!"  <rect x=\"{10 + x2}\" y=\"18\" width=\"{x3 - x2}\" height=\"26\" fill=\"#b08900\"/>\n" ++
  s!"  <rect x=\"{10 + x3}\" y=\"18\" width=\"{w - x3}\" height=\"26\" fill=\"#7b4fa8\"/>\n" ++
  s!"  <text class=\"t\" x=\"10\" y=\"64\">proved {p}</text>\n" ++
  s!"  <text class=\"t\" x=\"110\" y=\"64\">measured {m}</text>\n" ++
  s!"  <text class=\"t\" x=\"230\" y=\"64\">open {o}</text>\n" ++
  s!"  <text class=\"t\" x=\"320\" y=\"64\">wager {g}</text>\n" ++
  s!"  <text class=\"t\" x=\"10\" y=\"86\">{n} claims — each one carries an observation that would prove it wrong.</text>\n" ++
  "</svg>\n"

def claimCard (c : Claim) : String :=
  let witness :=
    if c.witness.isEmpty then ""
    else "  <p class=\"src\"><span>Machine-checked by:</span> "
         ++ String.intercalate ", " (c.witness.map fun w => s!"<code>{esc w}</code>")
         ++ "</p>\n"
  let basis :=
    if c.basis.isEmpty then ""
    else s!"  <p class=\"src\"><span>Where the measurement record lives:</span> {esc c.basis}</p>\n"
  "<article class=\"claim\">\n" ++
  s!"  <h3>{esc c.headline}</h3>\n" ++
  s!"  <p class=\"badge {statusClass c.status}\">{c.status.label}</p>\n" ++
  s!"  <p class=\"gloss\">{esc (statusGloss c.status)}</p>\n" ++
  s!"  <p>{esc c.plain}</p>\n" ++
  witness ++ basis ++
  s!"  <p class=\"kill\"><span>What would prove this wrong:</span> {esc c.kill}</p>\n" ++
  "</article>\n"

def gateRow (g : Gate) : String :=
  let mark := if g.mechanized then "<td class=\"yes\">checked by machine</td>"
              else "<td class=\"no\">upheld by people</td>"
  s!"<tr><th>{esc g.title}</th><td>{esc g.plain}</td>{mark}</tr>\n"

/-- The whole page. -/
def page : String :=
  let claims := String.join (stance.map claimCard)
  let gates  := String.join (Gate.all.map gateRow)
  "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n" ++
  "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n" ++
  "<title>What we think is true, and how you could prove us wrong</title>\n" ++
  "<style>\n" ++
  ":root{color-scheme:light dark;--fg:#1b1f24;--bg:#fff;--mut:#5b6774;--line:#e2e6ea;--card:#fafbfc}\n" ++
  "@media (prefers-color-scheme:dark){:root{--fg:#e6e9ec;--bg:#14171a;--mut:#9aa5b1;--line:#2a2f35;--card:#1b1f23}}\n" ++
  "*{box-sizing:border-box}body{margin:0;padding:2.5rem 1.25rem 4rem;font:16px/1.65 system-ui,sans-serif;color:var(--fg);background:var(--bg)}\n" ++
  "main{max-width:52rem;margin:0 auto}h1{font-size:1.9rem;line-height:1.25;margin:0 0 .5rem}\n" ++
  "h2{font-size:1.3rem;margin:2.75rem 0 .75rem;padding-bottom:.35rem;border-bottom:1px solid var(--line)}\n" ++
  "h3{font-size:1.05rem;margin:0 0 .5rem}.lede{font-size:1.1rem;color:var(--mut);margin:0 0 2rem}\n" ++
  "figure{margin:1.5rem 0;text-align:center}figcaption{color:var(--mut);font-size:.9rem;margin-top:.5rem}\n" ++
  "svg{max-width:100%;height:auto}\n" ++
  ".claim{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:1.1rem 1.25rem;margin:1rem 0}\n" ++
  ".badge{display:inline-block;font:600 11px/1 system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:.35rem .55rem;border-radius:5px;color:#fff;margin:0}\n" ++
  ".proved{background:#2e7d32}.measured{background:#2f6fb2}.open{background:#b08900}.wager{background:#7b4fa8}\n" ++
  ".gloss{color:var(--mut);font-size:.85rem;margin:.4rem 0 .8rem}\n" ++
".src{color:var(--mut);font-size:.85rem;margin:.4rem 0}.src span{font-weight:600}\n" ++
".src code{font-family:ui-monospace,SFMono-Regular,monospace;font-size:.9em}\n" ++
  ".kill{border-left:3px solid #e4572e;padding-left:.8rem;color:var(--mut);font-size:.94rem}\n" ++
  ".kill span{color:#e4572e;font-weight:600}\n" ++
  "table{border-collapse:collapse;width:100%;font-size:.93rem;margin-top:1rem}\n" ++
  "th,td{text-align:left;vertical-align:top;padding:.6rem .7rem;border-bottom:1px solid var(--line)}\n" ++
  "th{width:12rem;font-weight:600}.yes{color:#2e7d32;font-weight:600;width:11rem}.no{color:var(--mut);width:11rem}\n" ++
  "footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--mut);font-size:.9rem}\n" ++
  "</style></head><body><main>\n" ++
  "<h1>What we think is true, and how you could prove us wrong</h1>\n" ++
  s!"<p class=\"lede\">{esc summary}</p>\n" ++
  "<h2>The one picture that matters</h2>\n" ++
  "<figure>" ++ triadSvg ++
  "<figcaption>Our main tool measures how things move together <em>in pairs</em>. " ++
  "Here every pair is independent, yet the three together are perfectly coordinated. " ++
  "The tool reads exactly zero. That is not an error — it is the limit of what it can see, " ++
  "and it is why a zero reading never means &ldquo;nothing is there&rdquo;. " ++
  "Structure of this kind — real only in the three-together, never in any pair — is what " ++
  "Peirce called <em>Thirdness</em> and Heraclitus called the <em>Logos</em>: the grade of " ++
  "reality where habit, law and meaning live. On this exact state, both readings — the " ++
  "pairwise zero and the positive three-way reading — are machine-checked in this " ++
  "repository. Everything on this page builds toward, and is disciplined by, this one " ++
  "picture.</figcaption></figure>\n" ++
  "<h2>What we claim</h2>\n" ++
  "<figure>" ++ statusBarSvg stance ++
  "<figcaption>Every claim is labelled by how strongly it is established. We never round one up into another.</figcaption></figure>\n" ++
  claims ++
  "<h2>The rules we hold ourselves to</h2>\n" ++
  "<p>Some of these a computer checks on every change. The rest are commitments people have " ++
  "to keep. We mark which is which, because claiming a promise is machine-checked when it " ++
  "isn&rsquo;t would be its own kind of dishonesty.</p>\n" ++
  "<table><thead><tr><th>Rule</th><td><strong>What it means</strong></td><td><strong>Enforced by</strong></td></tr></thead><tbody>\n" ++
  gates ++ "</tbody></table>\n" ++
  "<footer><p>This page is generated from the repository&rsquo;s own source. The claims, their " ++
  "status, and the tests that would falsify them are read directly from the machine-checked " ++
  "files — there is no separately written copy that could drift from what we actually hold. " ++
  "If you can satisfy any of the falsification conditions above, we want to know.</p></footer>\n" ++
  "</main></body></html>\n"

end CIRISOntology.Report
