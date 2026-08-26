# CoSAI-RM ontology

OWL 2 DL representation of the [Coalition for Secure AI Risk Map](https://github.com/cosai-oasis/secure-ai-tooling/tree/main/risk-map), with SKOS alignments to OpenCRE, BFO 2020, MITRE D3FEND 1.5.0, and SPDX 3.1.

This repository implements [secure-ai-tooling#388](https://github.com/cosai-oasis/secure-ai-tooling/issues/388) through Phase 2, plus the four alignments named in that issue. Catalog rows come from CoSAI-RM YAML at commit `3a896b8`.

Workstream 2 also holds RFC 0.1 of the [AI Jailbreak Prevention Framework](rfc/jpf-0.1.md). Scoring and controls are in `data/`. References include [Redeploying Fable 5](https://www.anthropic.com/news/redeploying-fable-5), [Recommendations from the Hugging Face Autonomous Attack](https://www.linkedin.com/pulse/recommendations-from-hugging-face-autonomous-attack-bill-stout-el4ic), and [Who is responsible for what](https://www.linkedin.com/pulse/who-responsible-what-accountability-assessment-openai-bill-stout-s1dsc/).

## Graphs

| File | Contents |
| --- | --- |
| `ontology/cosai-rm.ttl` | TBox: classes and properties |
| `ontology/catalog.ttl` | Named individuals for 36 risks, 35 controls, 23 components, 10 personas |
| `ontology/alignments/bfo.ttl` | MIREOT BFO 2020 + IAO placement |
| `ontology/alignments/d3fend.ttl` | SKOS matches to D3FEND defensive techniques and digital artifacts |
| `ontology/alignments/spdx-3.1.ttl` | SKOS matches to SPDX 3.1 AI, Dataset, Software, Security, and Core classes |
| `ontology/alignments/opencre.ttl` | SKOS matches to CRE nodes, joined through ATLAS and OWASP LLM |
| `ontology/alignments/frameworks.ttl` | Native YAML mappings (ATLAS, NIST AI RMF, STRIDE, OWASP LLM, ISO 22989, EU AI Act) |
| `ontology/cosai-rm-full.ttl` | `owl:imports` of the files above |
| `ontology/catalog-v001.xml` | Protege catalog |

Term IRIs use `https://cosai-oasis.github.io/ontology/cosai-rm#`. YAML ids are local names: `cosai:riskDataPoisoning`, `cosai:controlInputValidationAndSanitization`.

Load `cosai-rm-full.ttl` for SPARQL. Do not import `d3fend.owl` or `spdx-model.ttl` unless you want those reasoners to run on the upstream ontologies. See [modeling decisions](docs/modeling-decisions.md).

## Query examples

From the repository root, after `pip install -r requirements.txt`:

```bash
python scripts/generate.py
python scripts/validate.py
pytest
```

Example: controls that mitigate prompt injection, with OpenCRE nodes:

```sparql
PREFIX cosai: <https://cosai-oasis.github.io/ontology/cosai-rm#>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>

SELECT ?control ?cre
WHERE {
  ?control cosai:mitigates cosai:riskPromptInjection .
  OPTIONAL {
    ?control skos:relatedMatch ?cre .
    FILTER(STRSTARTS(STR(?cre), "https://www.opencre.org/cre/"))
  }
}
```

The `queries/` directory has SPARQL for risk lists, control gaps, D3FEND matches, SPDX artifact types, BFO kinds, and persona obligations.

## Regeneration

`scripts/generate.py` reads `vendor/cosai-rm/yaml` and `vendor/opencre` and writes `catalog.ttl`, `alignments/frameworks.ttl`, and `alignments/opencre.ttl`. Hand-edited files are the TBox and the BFO, D3FEND, and SPDX alignment graphs.

To refresh the YAML snapshot from upstream:

```bash
# from a clone of cosai-oasis/secure-ai-tooling
cp risk-map/yaml/{risks,controls,components,personas,frameworks,lifecycle-stage,impact-type,actor-access}.yaml \
  path/to/this/repo/vendor/cosai-rm/yaml/
```

Then run `python scripts/generate.py`.

## Design constraints

1. Catalog rows are individuals. Categories are classes.
2. Matching uses SKOS. There is no `owl:equivalentClass` and no `owl:sameAs`.
3. D3FEND 1.5.0 and SPDX 3.1 are referenced by IRI, not imported.
4. OpenCRE links are a join of CoSAI's ATLAS/OWASP mappings onto OpenCRE's published links for those standards. Each join has an `AlignmentAssertion` recording the native identifier.

## License

Apache License 2.0. YAML under `vendor/cosai-rm` is copied from CoSAI Tooling under the same license. D3FEND, SPDX, BFO, IAO, and OpenCRE remain under their own terms; this repository stores only IRI-level alignments.
