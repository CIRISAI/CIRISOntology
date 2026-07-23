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

/-- Render a plain-text block as HTML paragraphs: blank lines in the source
    are paragraph breaks. A wall of text is a readability bug, not a style. -/
def paras (s : String) : String :=
  String.join ((s.splitOn "\n\n").filterMap fun p =>
    let t := p.trim
    if t.isEmpty then none else some s!"  <p>{esc t}</p>\n")

def statusClass : Status → String
  | .proved       => "proved"
  | .measured     => "measured"
  | .openQuestion => "open"
  | .wager        => "wager"
  | .dead         => "dead"

/-- What each strength label licenses — printed next to the badge so a reader
    cannot mistake one for another. -/
def statusGloss : Status → String
  | .proved       => "machine-checked in this repository, from stated assumptions"
  | .measured     => "established by observation, to a stated precision, on a stated domain"
  | .openQuestion => "named, unresolved, and not leaned on"
  | .wager        => "an avowed choice under uncertainty — not evidence"
  | .dead         => "KILLED — its own falsifier was satisfied. Kept on the page, marked dead"

def countBy (st : Status) (cs : List Claim) : Nat :=
  cs.foldl (fun n c => if c.status = st then n + 1 else n) 0

/-- THE CENTRAL FIGURE, in three dimensions. The flat plane is everything a
    pair instrument can see; the three coins A, B, C sit on it with no pair
    connection at all. The three-way lock is real, but it lives ABOVE the
    plane, in a separate dimension the pair instruments cannot enter. This is
    the whole claim in one picture. -/
def triadSvg : String :=
  "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 520 430\" width=\"520\" height=\"430\" role=\"img\" aria-label=\"Three coins A, B and C on a flat plane, every pair unlinked; a translucent pyramid rises to a point above the plane — the shared rule, which pair-by-pair checking cannot see\">\n" ++
  "  <defs><style>\n" ++
  "    .plane{fill:#8fa3b8;fill-opacity:.16;stroke:#8fa3b8;stroke-width:1;}\n" ++
  "    .face{fill:#e4572e;fill-opacity:.10;}\n" ++
  "    .node{fill:#2f6fb2;}\n" ++
  "    .lbl{font:600 15px system-ui,sans-serif;fill:#fff;text-anchor:middle;}\n" ++
  "    .coin{font:11px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "    .edge{stroke:#9aa5b1;stroke-width:2;stroke-dasharray:5 4;}\n" ++
  "    .edgelbl{font:11px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "    .tbond{stroke:#e4572e;stroke-width:2.5;stroke-opacity:.85;}\n" ++
  "    .tnode{fill:#e4572e;}\n" ++
  "    .tlbl{font:600 14px system-ui,sans-serif;fill:#e4572e;text-anchor:middle;}\n" ++
  "    .tsub{font:11px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "    .cap{font:11px system-ui,sans-serif;fill:#7b8794;text-anchor:middle;}\n" ++
  "  </style></defs>\n" ++
  "  <polygon class=\"plane\" points=\"40,285 260,210 480,285 260,360\"/>\n" ++
  "  <line class=\"edge\" x1=\"150\" y1=\"296\" x2=\"370\" y2=\"296\"/>\n" ++
  "  <line class=\"edge\" x1=\"150\" y1=\"296\" x2=\"260\" y2=\"238\"/>\n" ++
  "  <line class=\"edge\" x1=\"370\" y1=\"296\" x2=\"260\" y2=\"238\"/>\n" ++
  "  <text class=\"edgelbl\" x=\"260\" y=\"316\">no link</text>\n" ++
  "  <text class=\"edgelbl\" x=\"160\" y=\"258\">no link</text>\n" ++
  "  <text class=\"edgelbl\" x=\"360\" y=\"258\">no link</text>\n" ++
  "  <polygon class=\"face\" points=\"150,296 370,296 260,100\"/>\n" ++
  "  <line class=\"tbond\" x1=\"260\" y1=\"100\" x2=\"150\" y2=\"296\"/>\n" ++
  "  <line class=\"tbond\" x1=\"260\" y1=\"100\" x2=\"370\" y2=\"296\"/>\n" ++
  "  <line class=\"tbond\" x1=\"260\" y1=\"100\" x2=\"260\" y2=\"238\"/>\n" ++
  "  <circle class=\"tnode\" cx=\"260\" cy=\"100\" r=\"12\"/>\n" ++
  "  <text class=\"tlbl\" x=\"260\" y=\"46\">the Logos</text>\n" ++
  "  <text class=\"tsub\" x=\"260\" y=\"64\">the shared rule, above the plane — one coin-flip's worth of pattern</text>\n" ++
  "  <circle class=\"node\" cx=\"150\" cy=\"296\" r=\"22\"/><text class=\"lbl\" x=\"150\" y=\"301\">A</text>\n" ++
  "  <circle class=\"node\" cx=\"370\" cy=\"296\" r=\"22\"/><text class=\"lbl\" x=\"370\" y=\"301\">B</text>\n" ++
  "  <circle class=\"node\" cx=\"260\" cy=\"238\" r=\"22\"/><text class=\"lbl\" x=\"260\" y=\"243\">C</text>\n" ++
  "  <text class=\"coin\" x=\"100\" y=\"335\">a fair coin</text>\n" ++
  "  <text class=\"coin\" x=\"420\" y=\"335\">a fair coin</text>\n" ++
  "  <text class=\"cap\" x=\"260\" y=\"388\">C is set by the rule: heads if A and B differ, tails if they match.</text>\n" ++
  "  <text class=\"cap\" x=\"260\" y=\"406\">The grey plane holds everything pair-by-pair checking can see —</text>\n" ++
  "  <text class=\"cap\" x=\"260\" y=\"421\">on these three coins, the whole plane reads exactly zero.</text>\n" ++
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
  let dd := countBy .dead cs
  let x1 := seg p
  let x2 := seg (p + m)
  let x3 := seg (p + m + o)
  let x4 := seg (p + m + o + g)
  "<svg xmlns=\"http://www.w3.org/2000/svg\" viewBox=\"0 0 440 96\" width=\"440\" height=\"96\" role=\"img\" aria-label=\"How many claims are proved, measured, open, or wagers\">\n" ++
  "  <defs><style>.t{font:12px system-ui,sans-serif;fill:#5b6774}.k{font:600 12px system-ui,sans-serif}</style></defs>\n" ++
  s!"  <rect x=\"10\" y=\"18\" width=\"{x1}\" height=\"26\" fill=\"#2e7d32\"/>\n" ++
  s!"  <rect x=\"{10 + x1}\" y=\"18\" width=\"{x2 - x1}\" height=\"26\" fill=\"#2f6fb2\"/>\n" ++
  s!"  <rect x=\"{10 + x2}\" y=\"18\" width=\"{x3 - x2}\" height=\"26\" fill=\"#b08900\"/>\n" ++
  s!"  <rect x=\"{10 + x3}\" y=\"18\" width=\"{x4 - x3}\" height=\"26\" fill=\"#7b4fa8\"/>\n" ++
  s!"  <rect x=\"{10 + x4}\" y=\"18\" width=\"{w - x4}\" height=\"26\" fill=\"#8b2c2c\"/>\n" ++
  s!"  <text class=\"t\" x=\"10\" y=\"64\">proved {p}</text>\n" ++
  s!"  <text class=\"t\" x=\"110\" y=\"64\">measured {m}</text>\n" ++
  s!"  <text class=\"t\" x=\"230\" y=\"64\">open {o}</text>\n" ++
  s!"  <text class=\"t\" x=\"300\" y=\"64\">wager {g}</text>\n" ++
  s!"  <text class=\"t\" x=\"370\" y=\"64\">dead {dd}</text>\n" ++
  s!"  <text class=\"t\" x=\"10\" y=\"86\">{n} claims — each carries an observation that would prove it wrong. Dead ones stay, marked dead.</text>\n" ++
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
  let killer :=
    if c.killedBy.isEmpty then ""
    else s!"  <p class=\"killer\"><span>What killed it:</span> {esc c.killedBy}</p>\n"
  let promote :=
    if c.promote.isEmpty then ""
    else s!"  <p class=\"promote\"><span>What would move this up a level:</span> {esc c.promote}</p>\n"
  "<article class=\"claim\">\n" ++
  s!"  <h3>{esc c.headline}</h3>\n" ++
  s!"  <p class=\"badge {statusClass c.status}\">{c.status.label}</p>\n" ++
  s!"  <p class=\"gloss\">{esc (statusGloss c.status)}</p>\n" ++
  (if c.confidence.isEmpty then ""
   else s!"  <p class=\"conf\"><span>How strong:</span> {esc c.confidence}</p>\n") ++
  paras c.plain ++
  witness ++ basis ++ killer ++
  (if c.status = .dead then
     s!"  <p class=\"kill\"><span>The falsifier it carried:</span> {esc c.kill}</p>\n"
   else
     s!"  <p class=\"kill\"><span>What would prove this wrong:</span> {esc c.kill}</p>\n") ++
  promote ++
  "</article>\n"

def gateRow (g : Gate) : String :=
  let mark := if g.mechanized then "<td class=\"yes\">checked by machine</td>"
              else "<td class=\"no\">upheld by people</td>"
  s!"<tr><th>{esc g.title}</th><td>{esc g.plain}</td>{mark}</tr>\n"

/-- The claims, grouped by strength: strongest first, the dead last. Order
    within a group follows the stance list. -/
def groupedClaims : String :=
  let groups : List (Status × String × String) :=
    [ (.proved,   "Proved here",
       "Machine-checked in this repository. The live risk is our English saying more than our Lean — the falsifiers invite exactly that check."),
      (.measured, "Measured",
       "Established by observation, with the record named. A measurement is a statement about an instrument and a domain, never about the world alone."),
      (.openQuestion, "Open",
       "Named, unresolved, and not leaned on."),
      (.wager,    "Wagers",
       "Bets we choose to make. A bet is not evidence. Each one says what would kill it — and what would earn it a stronger label."),
      (.dead,     "Dead",
       "Claims whose own falsifiers were satisfied. They stay on the page, marked, with their killers — deleting them would destroy the evidence that the method works.") ]
  String.join (groups.map fun (st, title, gloss) =>
    let cs := stance.filter (·.status = st)
    if cs.isEmpty then ""
    else s!"<h3 class=\"grouphead\">{title} ({cs.length})</h3>\n<p class=\"groupgloss\">{esc gloss}</p>\n"
         ++ String.join (cs.map claimCard))

/-- The whole page. -/
def page : String :=
  let claims := groupedClaims
  let gates  := String.join (Gate.all.map gateRow)
  "<!doctype html>\n<html lang=\"en\"><head><meta charset=\"utf-8\">\n" ++
  "<meta name=\"viewport\" content=\"width=device-width,initial-scale=1\">\n" ++
  "<title>What we think is true — and how you could prove us wrong</title>\n" ++
  "<style>\n" ++
  ":root{color-scheme:light dark;--fg:#1b1f24;--bg:#fff;--mut:#5b6774;--line:#e2e6ea;--card:#fafbfc}\n" ++
  "@media (prefers-color-scheme:dark){:root{--fg:#e6e9ec;--bg:#14171a;--mut:#9aa5b1;--line:#2a2f35;--card:#1b1f23}}\n" ++
  "*{box-sizing:border-box}body{margin:0;padding:2.5rem 1.25rem 4rem;font:16px/1.65 system-ui,sans-serif;color:var(--fg);background:var(--bg)}\n" ++
  "main{max-width:52rem;margin:0 auto}h1{font-size:1.9rem;line-height:1.25;margin:0 0 .5rem}\n" ++
".lede{margin:0 0 2rem}.lede p{font-size:1.08rem;color:var(--mut);margin:0 0 .9rem}\n" ++
".claim p{margin:.6rem 0}\n" ++
  "h2{font-size:1.3rem;margin:2.75rem 0 .75rem;padding-bottom:.35rem;border-bottom:1px solid var(--line)}\n" ++
  "h3{font-size:1.05rem;margin:0 0 .5rem}.lede{font-size:1.1rem;color:var(--mut);margin:0 0 2rem}\n" ++
  "figure{margin:1.5rem 0;text-align:center}figcaption{color:var(--mut);font-size:.9rem;margin-top:.5rem}\n" ++
  "svg{max-width:100%;height:auto}\n" ++
  ".claim{border:1px solid var(--line);background:var(--card);border-radius:10px;padding:1.1rem 1.25rem;margin:1rem 0}\n" ++
  ".badge{display:inline-block;font:600 11px/1 system-ui,sans-serif;letter-spacing:.06em;text-transform:uppercase;padding:.35rem .55rem;border-radius:5px;color:#fff;margin:0}\n" ++
  ".proved{background:#2e7d32}.measured{background:#2f6fb2}.open{background:#b08900}.wager{background:#7b4fa8}\n" ++
".dead{background:#8b2c2c}\n" ++
".claim:has(.dead){border-color:#8b2c2c;border-style:dashed;opacity:.92}\n" ++
".killer{border-left:3px solid #8b2c2c;padding-left:.8rem;color:var(--mut);font-size:.94rem}\n" ++
".killer span{color:#8b2c2c;font-weight:600}\n" ++
".promote{border-left:3px solid #2e7d32;padding-left:.8rem;color:var(--mut);font-size:.94rem;margin-top:.5rem}\n" ++
".promote span{color:#2e7d32;font-weight:600}\n" ++
".grouphead{margin-top:2.2rem}\n" ++
".groupgloss{color:var(--mut);font-size:.95rem;margin:.2rem 0 1rem}\n" ++
  ".gloss{color:var(--mut);font-size:.85rem;margin:.4rem 0 .8rem}\n" ++
".conf{font-size:.9rem;margin:.2rem 0 .8rem;padding:.4rem .6rem;background:var(--card);border:1px solid var(--line);border-radius:6px}\n" ++
".conf span{font-weight:600;color:var(--fg)}\n" ++
".src{color:var(--mut);font-size:.85rem;margin:.4rem 0}.src span{font-weight:600}\n" ++
".src code{font-family:ui-monospace,SFMono-Regular,monospace;font-size:.9em}\n" ++
  ".kill{border-left:3px solid #e4572e;padding-left:.8rem;color:var(--mut);font-size:.94rem}\n" ++
  ".kill span{color:#e4572e;font-weight:600}\n" ++
  "table{border-collapse:collapse;width:100%;font-size:.93rem;margin-top:1rem}\n" ++
  "th,td{text-align:left;vertical-align:top;padding:.6rem .7rem;border-bottom:1px solid var(--line)}\n" ++
  "th{width:12rem;font-weight:600}.yes{color:#2e7d32;font-weight:600;width:11rem}.no{color:var(--mut);width:11rem}\n" ++
  "footer{margin-top:3rem;padding-top:1rem;border-top:1px solid var(--line);color:var(--mut);font-size:.9rem}\n" ++
  "</style></head><body><main>\n" ++
  "<h1>What we think is true &mdash; and how you could prove us wrong</h1>\n" ++
  "<div class=\"lede\">\n" ++ paras summary ++ "</div>\n" ++
  "<h2>The one picture that matters</h2>\n" ++
  "<figure>" ++ triadSvg ++
  "<figcaption>Three coins. A and B are ordinary flips. C is set by a rule: heads if A " ++
  "and B differ, tails if they match. Pick any two coins: they look completely random " ++
  "together, because the rule always needs the coin you did not pick. But see any two " ++
  "and you already know the third — the rule fixes it before you look. The grey plane " ++
  "is everything pair-by-pair checking can see, and on that plane this state reads " ++
  "exactly zero. The rule itself lives above the plane, in the whole. That is the " ++
  "Logos: Heraclitus&rsquo;s common account, Peirce&rsquo;s Thirdness. Both readings — " ++
  "zero on the plane, one coin-flip&rsquo;s worth of pattern above it — are proved by " ++
  "machine in this repository.</figcaption></figure>\n" ++
  "<h2>What we claim</h2>\n" ++
  "<figure>" ++ statusBarSvg stance ++
  "<figcaption>Every claim is labelled by how strongly it is established. We never raise a label above its evidence.</figcaption></figure>\n" ++
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
