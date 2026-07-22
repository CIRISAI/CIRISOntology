/-
The site generator. Writes the published page and its figures from the Lean
declarations themselves — `CIRISOntology.stance`, `CIRISOntology.summary` and
`CIRISOntology.Core.Gate.all`. There is no second copy of any of that text, so
the page cannot disagree with the repository.

    lake exe report [output-dir]      -- default: site
-/
import CIRISOntology.Report

def main (args : List String) : IO Unit := do
  let out := args.headD "site"
  IO.FS.createDirAll out
  IO.FS.createDirAll (out ++ "/img")
  IO.FS.writeFile (out ++ "/index.html") CIRISOntology.Report.page
  IO.FS.writeFile (out ++ "/img/triad.svg") CIRISOntology.Report.triadSvg
  IO.FS.writeFile (out ++ "/img/status.svg")
    (CIRISOntology.Report.statusBarSvg CIRISOntology.stance)
  IO.println s!"wrote {out}/index.html and 2 figures \
    ({CIRISOntology.stance.length} claims, {CIRISOntology.Core.Gate.all.length} gates)"
