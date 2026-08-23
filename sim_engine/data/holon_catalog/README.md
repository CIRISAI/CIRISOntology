# CIRISHolon chemistry/material catalog

Machine-readable source data for descriptor holons. This directory is intentionally
**not** a second material ontology: element/species/material records become descriptor
holons, and realization-specific charts decide which warranted properties they consume.

## Files

- `elements.csv` — all 118 named elements. CIAAW 2024 abridged standard atomic weights
  are numeric where a standard atomic weight exists; blanks are semantically `unresolved`,
  especially for radioactive elements. Never substitute atomic number or a guessed isotope mass.
- `electron_configurations.csv` — NIST neutral ground configurations H through U. The
  source itself scopes the table to H-U; Z>92 is deliberately absent rather than extrapolated.
- `species.csv` — starter molecule/mineral identities, formulas, configuration hints and
  molar masses. NIST WebBook masses are retained for covered molecular species; mineral
  formula weights are derived from `elements.csv` using the stated CIAAW abridged basis.
- `materials.jsonl` — specimen/grade/composition/property records. Properties carry their
  own source and conditions. A composition record is not automatically a constitutive law.
- `mixture_rules.json` — explicit conversions and effective-property models. Definitions,
  bounds and estimates are labeled separately. Strength/fracture fields have no generic
  mixing rule and therefore fail closed.
- `provenance.json` — source registry. Every `source_id` in the catalog must resolve here.
- `manifest.json` — version, unit convention and fail-closed behavior.

## Simulator contract

The runtime should compile a selected subset of these files into static Rust tables; it
should not parse CSV/JSON inside the `no_std` stepping loop. A descriptor compiler should:

1. resolve an element/species/material ID;
2. copy composition and source IDs into descriptor-holon state;
3. select conditions (T, P, phase, porosity, heat treatment, loading mode);
4. resolve only properties warranted at those conditions;
5. apply a named mixing/homogenization model when one is explicitly selected;
6. return an unresolved/refinement error rather than manufacture a missing property.

This maps cleanly onto the current architecture: composition is descriptor `Structure/Facts`,
conditions are `Circumstances`, the selected constitutive/mixing law is `Model/Rules`, and
source/specimen identity is `Record/Warrant`.

## Important scope boundaries

Atomic weight is not isotope mass. CIAAW standard atomic weights describe normal-material
isotopic composition and can be intervals in the full table. The abridged values here are
convenient recommended values with uncertainties for ordinary molar-mass work; isotope-resolved
quantum/nuclear simulations need an isotope catalog, not a replacement value in this table.

Likewise, alloy composition does not uniquely determine strength, fracture energy, fatigue,
damping or friction. Those depend strongly on processing, microstructure, geometry and loading.
The material records therefore mark such simulator fields `unresolved` until a warranted
specimen/grade/property source is added.

## Next data layers

The schema is ready to extend without changing the holon type: isotope masses/abundances,
oxidation/ionic states, crystal cells/space groups, bond/force-field parameters, phase diagrams,
thermochemical tables, and specimen-level fracture/fatigue datasets can all be additional
Record-backed descriptor data rather than new object classes.
