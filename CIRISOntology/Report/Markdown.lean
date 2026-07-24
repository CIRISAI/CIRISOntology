/-
CIRISOntology.Report.Markdown — a small renderer for the repository's own
governing prose (`epistemology.md`, `axiomology.md`), so the published Process
and Values tabs are generated from the same files the repository actually
lives by, with no separately written copy that could drift.

It covers exactly the constructs those documents use: ATX headings, paragraphs,
unordered and ordered lists with indented continuation lines, blockquotes, pipe
tables, horizontal rules, and the inline forms **bold**, *italic*, `code`, and
[text](url). Nothing more — a full CommonMark engine would be a liability
here, not a feature. Where input is malformed (unbalanced delimiters), the text
is passed through untouched rather than guessed at.
-/

namespace CIRISOntology.Report.Markdown

/-- Escape the characters that would otherwise break the markup. -/
def esc (s : String) : String :=
  s.replace "&" "&amp;" |>.replace "<" "&lt;" |>.replace ">" "&gt;"

/-- Rewrite every `[text](url)` in an already-escaped run as an anchor.
    A run with no complete link comes back unchanged. -/
partial def links (s : String) : String :=
  match s.splitOn "](" with
  | a :: b :: rest =>
    let tail := String.intercalate "](" (b :: rest)
    match a.splitOn "[" with
    | [] | [_] => s
    | aParts =>
      let text := aParts.getLast!
      let before := String.intercalate "[" aParts.dropLast
      match tail.splitOn ")" with
      | [] => s
      | url :: after =>
        before ++ s!"<a href=\"{url}\">{text}</a>"
          ++ links (String.intercalate ")" after)
  | _ => s

/-- Wrap alternate segments of `s` (split on `delim`) in `<tag>…</tag>`.
    Unbalanced delimiters leave the string untouched. -/
def alternate (delim tag : String) (s : String) : String :=
  let rec go : List String → Bool → String
    | [], _ => ""
    | p :: ps, inside =>
      (if inside then s!"<{tag}>{p}</{tag}>" else p) ++ go ps !inside
  let ps := s.splitOn delim
  if ps.length % 2 = 1 then go ps false else s

/-- Inline markup on one line's worth of text: escape, then code spans (whose
    contents are left verbatim), then links, bold, italic on what remains. -/
def inline (raw : String) : String :=
  let fmt (t : String) : String := alternate "*" "em" (alternate "**" "strong" (links t))
  let rec go : List String → Bool → String
    | [], _ => ""
    | p :: ps, insideCode =>
      (if insideCode then s!"<code>{p}</code>" else fmt p) ++ go ps !insideCode
  let ps := (esc raw).splitOn "`"
  if ps.length % 2 = 1 then go ps false else fmt (esc raw)

/-- A line beginning `1. ` / `12. ` — an ordered-list item. -/
def isOrdered (l : String) : Bool :=
  let d := l.takeWhile Char.isDigit
  !d.isEmpty && (l.drop d.length).startsWith ". "

/-- Lines that open a block other than a paragraph — where paragraph
    accumulation must stop. -/
def isBlockStart (l : String) : Bool :=
  l.startsWith "#" || l.startsWith "- " || l.startsWith ">" ||
  l.startsWith "|" || l == "---" || isOrdered l

/-- Group marker-led lines with their indented continuation lines into whole
    items, marker stripped. -/
def items (isMarker : String → Bool) (strip : String → String)
    (lines : List String) : List String :=
  lines.foldl (init := []) fun acc x =>
    let y := x.trimRight
    if isMarker y then acc ++ [strip y]
    else match acc.getLast? with
      | some last => acc.dropLast ++ [last ++ " " ++ y.trimLeft]
      | none => acc

/-- Split a `| a | b |` row into trimmed cells. -/
def rowCells (l : String) : List String :=
  let core := l.trim
  let core := if core.startsWith "|" then core.drop 1 else core
  let core := if core.endsWith "|" then core.dropRight 1 else core
  (core.splitOn "|").map String.trim

/-- The `|---|---|` header separator. -/
def isSepRow (cells : List String) : Bool :=
  !cells.isEmpty && cells.all fun c =>
    !c.isEmpty && c.all fun ch => ch == '-' || ch == ':'

/-- Render a run of contiguous `|`-led lines as a table. -/
def renderTable (lines : List String) : String :=
  let cell (tag c : String) : String := s!"<{tag}>{inline c}</{tag}>"
  let row (tag : String) (cs : List String) : String :=
    "<tr>" ++ String.join (cs.map (cell tag)) ++ "</tr>\n"
  match lines.map rowCells with
  | header :: sep :: body =>
    if isSepRow sep then
      "<table><thead>" ++ row "th" header ++ "</thead><tbody>\n"
        ++ String.join (body.map (row "td")) ++ "</tbody></table>\n"
    else
      "<table><tbody>\n" ++ String.join ((header :: sep :: body).map (row "td"))
        ++ "</tbody></table>\n"
  | rows =>
    "<table><tbody>\n" ++ String.join (rows.map (row "td")) ++ "</tbody></table>\n"

/-- Render a document, line-list form. -/
partial def blocks : List String → String
  | [] => ""
  | l :: rest =>
    let t := l.trimRight
    if t.isEmpty then blocks rest
    else if t == "---" then "<hr>\n" ++ blocks rest
    else if t.startsWith "### " then s!"<h3>{inline (t.drop 4)}</h3>\n" ++ blocks rest
    else if t.startsWith "## " then s!"<h2>{inline (t.drop 3)}</h2>\n" ++ blocks rest
    else if t.startsWith "# " then s!"<h1>{inline (t.drop 2)}</h1>\n" ++ blocks rest
    else if t.startsWith ">" then
      let (qs, rest') := (l :: rest).span fun x => x.trimRight.startsWith ">"
      let text := String.intercalate " "
        (qs.map fun x => (x.trimRight.drop 1).trimLeft)
      s!"<blockquote><p>{inline text}</p></blockquote>\n" ++ blocks rest'
    else if t.startsWith "|" then
      let (tl, rest') := (l :: rest).span fun x => x.trimRight.startsWith "|"
      renderTable (tl.map String.trimRight) ++ blocks rest'
    else if t.startsWith "- " then
      let (block, rest') := (l :: rest).span fun x =>
        let y := x.trimRight
        y.startsWith "- " || (!y.isEmpty && x.startsWith " ")
      let lis := items (·.startsWith "- ") (·.drop 2) block
      "<ul>\n" ++ String.join (lis.map fun i => s!"<li>{inline i}</li>\n")
        ++ "</ul>\n" ++ blocks rest'
    else if isOrdered t then
      let (block, rest') := (l :: rest).span fun x =>
        let y := x.trimRight
        isOrdered y || (!y.isEmpty && x.startsWith " ")
      let strip (y : String) : String := y.drop ((y.takeWhile Char.isDigit).length + 2)
      let lis := items isOrdered strip block
      "<ol>\n" ++ String.join (lis.map fun i => s!"<li>{inline i}</li>\n")
        ++ "</ol>\n" ++ blocks rest'
    else
      let (ps, rest') := (l :: rest).span fun x =>
        let y := x.trimRight
        !y.isEmpty && !isBlockStart y
      s!"<p>{inline (String.intercalate " " (ps.map String.trim))}</p>\n" ++ blocks rest'

/-- Render a whole markdown document to HTML body content. -/
def render (md : String) : String :=
  blocks (md.splitOn "\n")

end CIRISOntology.Report.Markdown
