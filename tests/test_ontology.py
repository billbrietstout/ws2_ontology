"""Catalog integrity tests for the CoSAI-RM ontology."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

import yaml
from rdflib import Graph, Namespace, RDF, OWL, URIRef, SKOS

ROOT = Path(__file__).resolve().parents[1]
COSAI = Namespace("https://cosai-oasis.github.io/ontology/cosai-rm#")
YAML_DIR = ROOT / "vendor" / "cosai-rm" / "yaml"


def load_union() -> Graph:
    graph = Graph()
    for path in [
        ROOT / "ontology" / "cosai-rm.ttl",
        ROOT / "ontology" / "catalog.ttl",
        ROOT / "ontology" / "alignments" / "bfo.ttl",
        ROOT / "ontology" / "alignments" / "d3fend.ttl",
        ROOT / "ontology" / "alignments" / "spdx-3.1.ttl",
        ROOT / "ontology" / "alignments" / "frameworks.ttl",
        ROOT / "ontology" / "alignments" / "opencre.ttl",
    ]:
        graph.parse(path, format="turtle")
    return graph


def load_yaml(name: str) -> dict:
    with open(YAML_DIR / name, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def test_generate_is_current() -> None:
    catalog = ROOT / "ontology" / "catalog.ttl"
    assert catalog.exists()
    subprocess.check_call([sys.executable, str(ROOT / "scripts" / "generate.py")], cwd=ROOT)
    assert catalog.exists()


def test_counts_match_yaml() -> None:
    graph = load_union()
    risks = load_yaml("risks.yaml")["risks"]
    controls = load_yaml("controls.yaml")["controls"]
    components = load_yaml("components.yaml")["components"]
    personas = load_yaml("personas.yaml")["personas"]
    assert len(list(graph.subjects(RDF.type, COSAI.Risk))) == len(risks)
    assert len(list(graph.subjects(RDF.type, COSAI.Control))) == len(controls)
    assert len(list(graph.subjects(RDF.type, COSAI.Component))) == len(components)
    assert len(list(graph.subjects(RDF.type, COSAI.Persona))) == len(personas)


def test_no_equivalent_class() -> None:
    graph = load_union()
    assert not list(graph.subject_objects(OWL.equivalentClass))
    assert not list(graph.subject_objects(OWL.sameAs))


def test_prompt_injection_has_controls_and_cre() -> None:
    graph = load_union()
    risk = COSAI.riskPromptInjection
    controls = list(graph.objects(risk, COSAI.mitigatedBy))
    assert controls
    cres = [
        obj
        for obj in graph.objects(risk, SKOS.relatedMatch)
        if str(obj).startswith("https://www.opencre.org/cre/")
    ]
    assert cres, "prompt injection should join to at least one CRE via ATLAS or OWASP LLM"


def test_model_maps_to_spdx_aipackage() -> None:
    graph = load_union()
    targets = set(graph.objects(COSAI.componentTheModel, SKOS.closeMatch))
    assert URIRef("https://spdx.org/rdf/3.1/terms/AI/AIPackage") in targets


def test_integrity_control_maps_to_d3fend_fim() -> None:
    graph = load_union()
    targets = set(graph.objects(COSAI.controlModelAndDataIntegrityManagement, SKOS.closeMatch))
    assert URIRef("http://d3fend.mitre.org/ontologies/d3fend.owl#FileIntegrityMonitoring") in targets
