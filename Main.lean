/-
The site generator. Writes the published pages and their figures from the
repository's own sources — `CIRISOntology.stance`, `CIRISOntology.summary` and
`CIRISOntology.Core.Gate.all` for the Pursuits tab, and the governing documents
`epistemology.md` and `axiomology.md` for the Process and Values tabs. There is
no second copy of any of that text, so the site cannot disagree with the
repository.

    lake exe report [output-dir]      -- default: site
-/
import CIRISOntology.Report

def main (args : List String) : IO Unit := do
  let out := args.headD "site"
  IO.FS.createDirAll out
  IO.FS.createDirAll (out ++ "/img")
  let epistemology ← IO.FS.readFile "epistemology.md"
  let axiomology ← IO.FS.readFile "axiomology.md"
  IO.FS.writeFile (out ++ "/index.html") CIRISOntology.Report.pursuitsPage
  IO.FS.writeFile (out ++ "/process.html") (CIRISOntology.Report.processPage epistemology)
  IO.FS.writeFile (out ++ "/values.html") (CIRISOntology.Report.valuesPage axiomology)
  IO.FS.writeFile (out ++ "/img/triad.svg") CIRISOntology.Report.triadSvg
  IO.FS.writeFile (out ++ "/img/status.svg")
    (CIRISOntology.Report.statusBarSvg CIRISOntology.stance)
  IO.println s!"wrote {out}/index.html, process.html, values.html and 2 figures \
    ({CIRISOntology.stance.length} claims, {CIRISOntology.Core.Gate.all.length} gates)"
