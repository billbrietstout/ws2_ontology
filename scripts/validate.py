#!/usr/bin/env python3
"""Parse CoSAI-RM Turtle graphs and check catalog integrity against YAML."""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

try:
    import yaml
    from rdflib import Graph, Namespace, RDF, OWL, URIRef
except ImportError as exc:  # pragma: no cover
    raise SystemExit("Install dependencies: pip install -r requirements.txt") from exc

COSAI = Namespace("https://cosai-oasis.github.io/ontology/cosai-rm#")
TTL_FILES = [
    ROOT / "ontology" / "cosai-rm.ttl",
    ROOT / "ontology" / "catalog.ttl",
    ROOT / "ontology" / "cosai-rm-full.ttl",
    ROOT / "ontology" / "alignments" / "bfo.ttl",
    ROOT / "ontology" / "alignments" / "d3fend.ttl",
    ROOT / "ontology" / "alignments" / "spdx-3.1.ttl",
    ROOT / "ontology" / "alignments" / "frameworks.ttl",
    ROOT / "ontology" / "alignments" / "opencre.ttl",
]


def load_yaml(name: str) -> dict:
    with open(ROOT / "vendor" / "cosai-rm" / "yaml" / name, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def parse_all() -> Graph:
    graph = Graph()
    for path in TTL_FILES:
        if path.name == "cosai-rm-full.ttl":
            continue
        graph.parse(path, format="turtle")
    return graph


def fail(errors: list[str]) -> None:
    for item in errors:
        print(f"FAIL: {item}")
    raise SystemExit(1)


def main() -> None:
    errors: list[str] = []
    for path in TTL_FILES:
        Graph().parse(path, format="turtle")
        print(f"OK parse {path.relative_to(ROOT)}")

    graph = parse_all()
    print(f"OK union triples={len(graph)}")

    equivalent = list(graph.subjects(RDF.type, OWL.equivalentClass))
    if equivalent:
        errors.append(f"owl:equivalentClass present: {equivalent[:5]}")

    for path in TTL_FILES:
        text = path.read_text(encoding="utf-8")
        if "owl:imports <http://d3fend.mitre.org/ontologies/d3fend.owl>" in text:
            errors.append(f"{path.name} imports full D3FEND OWL")
        if "owl:imports <https://spdx.org/rdf/3.1/spdx-model.ttl>" in text:
            errors.append(f"{path.name} imports full SPDX OWL")

    risks = load_yaml("risks.yaml")["risks"]
    controls = load_yaml("controls.yaml")["controls"]
    components = load_yaml("components.yaml")["components"]
    personas = load_yaml("personas.yaml")["personas"]

    for record, rtype in (
        (risks, COSAI.Risk),
        (controls, COSAI.Control),
        (components, COSAI.Component),
        (personas, COSAI.Persona),
    ):
        for item in record:
            uri = COSAI[item["id"]]
            if (uri, RDF.type, rtype) not in graph:
                errors.append(f"missing {rtype} individual {item['id']}")

    for control in controls:
        expected = control.get("risks")
        if expected == "all":
            expected_ids = [r["id"] for r in risks]
        elif isinstance(expected, list):
            expected_ids = expected
        else:
            expected_ids = []
        uri = COSAI[control["id"]]
        actual = {str(obj).rsplit("#", 1)[-1] for obj in graph.objects(uri, COSAI.mitigates)}
        missing = set(expected_ids) - actual
        if missing:
            errors.append(f"{control['id']} missing mitigates {sorted(missing)[:8]}")

    cre_matches = list(graph.triples((None, URIRef("http://www.w3.org/2004/02/skos/core#relatedMatch"), None)))
    cre_matches = [t for t in cre_matches if "opencre.org/cre/" in str(t[2])]
    if len(cre_matches) < 10:
        errors.append(f"too few OpenCRE matches: {len(cre_matches)}")

    d3f_matches = [t for t in graph.triples((None, None, None)) if "d3fend.mitre.org" in str(t[2]) and "skos" in str(t[1])]
    if len(d3f_matches) < 10:
        errors.append(f"too few D3FEND SKOS triples: {len(d3f_matches)}")

    spdx_matches = [t for t in graph.triples((None, None, None)) if "spdx.org/rdf/3.1" in str(t[2]) and "skos" in str(t[1])]
    if len(spdx_matches) < 10:
        errors.append(f"too few SPDX SKOS triples: {len(spdx_matches)}")

    if errors:
        fail(errors)
    print(f"OK catalog risks={len(risks)} controls={len(controls)} components={len(components)} personas={len(personas)}")
    print(f"OK OpenCRE relatedMatch={len(cre_matches)} D3FEND SKOS={len(d3f_matches)} SPDX SKOS={len(spdx_matches)}")


if __name__ == "__main__":
    main()
