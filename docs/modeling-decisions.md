# Modeling decisions

CoSAI-RM 0.1.0 is an OWL 2 DL TBox plus a catalog of named individuals. It answers issue [388](https://github.com/cosai-oasis/secure-ai-tooling/issues/388) through Phase 2 of that plan, with SKOS alignments for OpenCRE, BFO 2020, MITRE D3FEND 1.5.0, and SPDX 3.1.

## Catalog entries are individuals

Each YAML row becomes one named individual, typed by its category class (`SupplyChainAndDevelopmentRisk`, `DataControl`, `ModelComponent`, `Persona`). Categories are OWL classes. Rows are not subclasses. SPARQL can list risks without punning. A later operational graph can instantiate `RiskDisposition`, `ControlImplementation`, or `PersonaRole` and point at a catalog entry with `cosai:exemplifies`.

## Two layers: catalog and world

A catalog entry is an information content entity. It is about a kind of risk, control, component, or persona. It is not that world entity.

| Catalog class | World class | BFO parent of the world class |
| --- | --- | --- |
| `Risk` | `RiskDisposition` | disposition (`BFO_0000016`) |
| `Control` | `ControlImplementation` | process (`BFO_0000015`) |
| `Persona` | `PersonaRole` | role (`BFO_0000023`) |
| `Component` | (varies) | recorded per individual with `cosai:describesBfoClass` |

Component kinds split three ways: training data and the model are information content entities; storage and serving are material entities; training, evaluation, and I/O handling are processes.

## SKOS instead of OWL equivalence

`owl:equivalentClass`, `owl:equivalentProperty`, and `owl:sameAs` are not used. SPDX maintainers measured the reasoning cost of those axioms on versioned IRIs ([iribench](https://github.com/bact/iribench)). Issue 388 records that finding. This ontology uses `skos:closeMatch` when the CoSAI entry and the external concept pick out the same kind of thing, and `skos:relatedMatch` when they overlap but are not interchangeable.

## No `owl:imports` of D3FEND or SPDX

D3FEND 1.5.0 is a large OWL distribution with punning and existential restrictions. SPDX 3.1 ships SHACL and OWL together. Importing either file pulls those axioms into every CoSAI reasoning run. Alignment files declare the external IRIs they mention (MIREOT) and stop there. Consumers who need D3FEND inference load `d3fend.owl` themselves. ATT&CK links then follow from D3FEND's existing mappings.

BFO 2020 is also not imported as a whole. `alignments/bfo.ttl` declares the dozen BFO and IAO classes this TBox needs.

## OpenCRE links are a join, not a new CRE

CoSAI-RM YAML already maps risks and controls to MITRE ATLAS and OWASP Top 10 for LLM. OpenCRE already links those ATLAS and OWASP identifiers to CRE nodes. `scripts/generate.py` joins the two published maps and emits `skos:relatedMatch` plus an `AlignmentAssertion` blank node that records the native identifier and the method `transitive-join`. Those triples are not community-reviewed exact matches. Direct CRE hyperlinks in future YAML, following [OpenCRE's self-maintaining method](https://github.com/OWASP/OpenCRE/blob/main/docs/CONTRIBUTING.md), would replace the join for those rows.

## Framework terms stay native

ATLAS technique IDs, NIST AI RMF subcategory IDs, STRIDE names, OWASP LLM IDs, ISO 22989 role strings, and EU AI Act article references are `FrameworkTerm` individuals copied from YAML. They use `cosai:mapsTo` plus a SKOS match. Version suffixes such as `@5.0.1` become `owl:versionInfo` on the term.

## Namespace

The term namespace is `https://cosai-oasis.github.io/ontology/cosai-rm#`. Issue 388 proposed a GitHub Pages ontology root. A w3id.org redirect can be added later without renaming local names. Catalog IRIs reuse YAML ids (`cosai:riskDataPoisoning`).

## OWL profile

The TBox stays inside OWL 2 DL. Inverse properties are declared. There are no property chains, no qualified cardinality, and no `owl:unionOf` on CoSAI classes. Domain and range are `rdfs:domain` / `rdfs:range`. HermiT or ELK can check the TBox plus catalog; they will not see D3FEND or SPDX axioms unless a user imports those files.

## What 0.1.0 does not claim

OCSF, CSA AI Controls, MIT AI Risk Repository, and DoD Zero Trust are named in issue 388 Phase 3 and Phase 4. They are not in this release. NIST AI RMF and OWASP LLM coverage is only as complete as the YAML mappings in the vendored snapshot (`3a896b8`). Several newer agentic risks have STRIDE and ATLAS rows but no OWASP LLM row; OpenCRE joins follow that gap.

CCO, OMG Commons, and SEMIC are mid-level options noted in issue 388. This release uses BFO plus IAO only. CCO can sit between BFO and CoSAI later without renaming catalog IRIs.
