#!/usr/bin/env python3
"""Generate CoSAI-RM catalog and alignment graphs from vendored YAML.

Reads vendor/cosai-rm/yaml and vendor/opencre, writes Turtle under ontology/.
Does not import D3FEND or SPDX OWL. Crosswalks use SKOS plus provenance.
"""

from __future__ import annotations

import json
import re
from collections import defaultdict
from pathlib import Path

try:
    import yaml
except ImportError as exc:  # pragma: no cover
    raise SystemExit("PyYAML is required: pip install pyyaml") from exc

ROOT = Path(__file__).resolve().parents[1]
VENDOR_YAML = ROOT / "vendor" / "cosai-rm" / "yaml"
VENDOR_CRE = ROOT / "vendor" / "opencre"
OUT_DIR = ROOT / "ontology"
ALIGN_DIR = OUT_DIR / "alignments"

NS = "https://cosai-oasis.github.io/ontology/cosai-rm#"
ONTOLOGY_IRI = "https://cosai-oasis.github.io/ontology/cosai-rm"
SOURCE_REPO = "https://github.com/cosai-oasis/secure-ai-tooling"
SOURCE_COMMIT = "3a896b8a1b2c8f1949cf524a2f2bba349a9cc83a"
YAML_BLOB = f"{SOURCE_REPO}/blob/{SOURCE_COMMIT}/risk-map/yaml"

RISK_CLASS = {
    "risksSupplyChainAndDevelopment": "SupplyChainAndDevelopmentRisk",
    "risksDeploymentAndInfrastructure": "DeploymentAndInfrastructureRisk",
    "risksRuntimeInputSecurity": "RuntimeInputSecurityRisk",
    "risksRuntimeDataSecurity": "RuntimeDataSecurityRisk",
    "risksRuntimeOutputSecurity": "RuntimeOutputSecurityRisk",
}

CONTROL_CLASS = {
    "controlsData": "DataControl",
    "controlsInfrastructure": "InfrastructureControl",
    "controlsModel": "ModelControl",
    "controlsApplication": "ApplicationControl",
    "controlsAssurance": "AssuranceControl",
    "controlsGovernance": "GovernanceControl",
}

COMPONENT_CLASS = {
    "componentsInfrastructure": "InfrastructureComponent",
    "componentsModel": "ModelComponent",
    "componentsApplication": "ApplicationComponent",
}

FRAMEWORK_BASE = {
    "mitre-atlas": {
        "technique": "https://atlas.mitre.org/techniques/{id}",
        "mitigation": "https://atlas.mitre.org/mitigations/{id}",
    },
    "nist-ai-rmf": "https://airc.nist.gov/airmf-resources/airmf/",
    "stride": "https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats",
    "owasp-top10-llm": "https://genai.owasp.org/llmrisk/",
    "iso-22989": "https://www.iso.org/standard/74296.html",
    "eu-ai-act": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj",
}

HEADER = """\
@prefix cosai: <https://cosai-oasis.github.io/ontology/cosai-rm#> .
@prefix cre: <https://www.opencre.org/cre/> .
@prefix dcterms: <http://purl.org/dc/terms/> .
@prefix owl: <http://www.w3.org/2002/07/owl#> .
@prefix prov: <http://www.w3.org/ns/prov#> .
@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

"""


def ttl_escape(text: str) -> str:
    return (
        text.replace("\\", "\\\\")
        .replace('"', '\\"')
        .replace("\r\n", "\n")
        .replace("\r", "\n")
        .replace("\n", "\\n")
    )


def literal(text: str | None, lang: str = "en") -> str | None:
    if not text:
        return None
    cleaned = re.sub(r"\s+", " ", str(text)).strip()
    if not cleaned:
        return None
    return f'"{ttl_escape(cleaned)}"@{lang}'


def prose(value) -> str:
    if value is None:
        return ""
    if isinstance(value, list):
        return " ".join(prose(v) for v in value if v)
    return str(value).strip()


def catalog_comment(*candidates) -> str:
    """Short rdfs:comment from YAML. Prefer shortDescription. Strip em dashes and control-addresses glue."""
    raw = ""
    for candidate in candidates:
        text = prose(candidate)
        if text:
            raw = text
            break
    if not raw:
        return ""
    raw = raw.replace("\u2014", ", ").replace("\u2013", " to ")
    raw = re.sub(r"(?i)\s*This control addresses[^.]*\.", "", raw)
    return re.sub(r"\s+", " ", raw).strip(" ,;")


def load_yaml(name: str) -> dict:
    with open(VENDOR_YAML / name, encoding="utf-8") as handle:
        return yaml.safe_load(handle)


def split_mapping(value: str) -> tuple[str, str | None]:
    if "@" in value:
        ident, version = value.rsplit("@", 1)
        return ident, version
    return value, None


def atlas_kind(ident: str) -> str:
    return "mitigation" if ident.startswith("AML.M") else "technique"


def local_term_id(framework: str, ident: str) -> str:
    safe = re.sub(r"[^A-Za-z0-9]+", "_", ident).strip("_")
    fw = framework.replace("-", "_")
    return f"term_{fw}_{safe}"


def load_opencre_index() -> dict[str, list[tuple[str, str]]]:
    """Map ATLAS/OWASP native IDs to (cre_id, cre_name) pairs."""
    index: dict[str, list[tuple[str, str]]] = defaultdict(list)
    seen: set[tuple[str, str, str]] = set()
    files = [
        VENDOR_CRE / "atlas-p1.json",
        VENDOR_CRE / "atlas-p2.json",
        VENDOR_CRE / "atlas-p3.json",
        VENDOR_CRE / "owasp-llm.json",
    ]
    for path in files:
        data = json.loads(path.read_text(encoding="utf-8"))
        for section in data.get("standards", []):
            section_id = section.get("sectionID")
            if not section_id:
                continue
            for link in section.get("links", []):
                doc = link.get("document") or {}
                if doc.get("doctype") != "CRE":
                    continue
                cre_id = doc.get("id")
                name = doc.get("name") or cre_id
                key = (section_id, cre_id, name)
                if key in seen:
                    continue
                seen.add(key)
                index[section_id].append((cre_id, name))
    return index


def lookup_cres(index: dict[str, list[tuple[str, str]]], ident: str) -> list[tuple[str, str]]:
    if ident in index:
        return index[ident]
    # Parent technique fallback: AML.T0024.002 -> AML.T0024
    if "." in ident:
        parent = ident.rsplit(".", 1)[0]
        if parent in index:
            return index[parent]
    return []


def emit_individual(lines: list[str], local: str, rdf_types: list[str], label: str,
                    comment: str | None, ident: str, source_file: str,
                    extra: list[str] | None = None, deprecated: bool = False) -> None:
    types = ", ".join(f"cosai:{t}" if not t.startswith("cosai:") and ":" not in t else t for t in rdf_types)
    lines.append(f"cosai:{local} a {types} ;")
    lines.append(f"    rdfs:label {literal(label)} ;")
    if comment:
        lines.append(f"    rdfs:comment {literal(comment)} ;")
    lines.append(f'    dcterms:identifier "{ident}" ;')
    lines.append(f"    dcterms:source <{YAML_BLOB}/{source_file}> ;")
    if deprecated:
        lines.append("    owl:deprecated true ;")
    extras = extra or []
    for i, stmt in enumerate(extras):
        sep = " ;" if i < len(extras) - 1 or True else " ."
        lines.append(f"    {stmt}{sep}")
    if extras:
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    else:
        lines[-1] = lines[-1].rstrip(" ;") + " ."
    lines.append("")


def ref_list(values: list[str], prefix: str = "cosai:") -> str:
    return ", ".join(f"{prefix}{v}" for v in values)


def stage_local(stage_id: str) -> str:
    return stage_id.replace("-", "_")


def impact_local(impact_id: str) -> str:
    return f"impact_{impact_id.replace('-', '_')}"


def access_local(access_id: str) -> str:
    return f"access_{access_id.replace('-', '_')}"


def normalize_multi(value, all_ids: list[str], none_ok: bool = False):
    if value is None:
        return []
    if value == "all":
        return list(all_ids)
    if value == "none":
        return []
    if isinstance(value, list):
        return value
    return [value]


def build_catalog(risks, controls, components, personas, lifecycle, impact, actor) -> str:
    risk_ids = [r["id"] for r in risks["risks"]]
    component_ids = [c["id"] for c in components["components"]]
    lines = [
        HEADER.rstrip(),
        "",
        f"# Generated from {YAML_BLOB} at commit {SOURCE_COMMIT}.",
        f"# Do not edit by hand. Regenerated by scripts/generate.py.",
        "",
        f"<{ONTOLOGY_IRI}/catalog> a owl:Ontology ;",
        f"    owl:versionIRI <{ONTOLOGY_IRI}/catalog/0.1.0> ;",
        f"    owl:imports <{ONTOLOGY_IRI}> ;",
        '    dcterms:title "CoSAI-RM Catalog"@en ;',
        f'    dcterms:source <{SOURCE_REPO}/tree/{SOURCE_COMMIT}/risk-map/yaml> ;',
        '    rdfs:comment "Named individuals for CoSAI-RM catalog entries. Categories are OWL classes in the TBox; catalog rows are individuals."@en .',
        "",
    ]

    for stage in lifecycle["lifecycleStages"]:
        extra = [f"cosai:stageOrder {int(stage['order'])}"]
        emit_individual(
            lines, stage_local(stage["id"]), ["LifecycleStage"],
            stage["title"], catalog_comment(stage.get("description")), stage["id"],
            "lifecycle-stage.yaml", extra,
        )

    for item in impact["impactTypes"]:
        emit_individual(
            lines, impact_local(item["id"]), ["ImpactType"],
            item["title"], catalog_comment(item.get("description")), item["id"],
            "impact-type.yaml",
        )

    for item in actor["actorAccessLevels"]:
        emit_individual(
            lines, access_local(item["id"]), ["ActorAccessLevel"],
            item["title"], catalog_comment(item.get("description")), item["id"],
            "actor-access.yaml",
        )

    for persona in personas["personas"]:
        emit_individual(
            lines, persona["id"], ["Persona"],
            persona["title"], catalog_comment(persona.get("description")),
            persona["id"], "personas.yaml",
            deprecated=bool(persona.get("deprecated")),
        )

    for component in components["components"]:
        klass = COMPONENT_CLASS[component["category"]]
        extra = []
        edges = component.get("edges") or {}
        tos = edges.get("to") or []
        frs = edges.get("from") or []
        if tos:
            extra.append(f"cosai:feeds {ref_list(tos)}")
        if frs:
            extra.append(f"cosai:fedBy {ref_list(frs)}")
        emit_individual(
            lines, component["id"], [klass, "Component"],
            component["title"], catalog_comment(component.get("description")),
            component["id"], "components.yaml", extra,
        )

    for risk in risks["risks"]:
        klass = RISK_CLASS[risk["category"]]
        extra = []
        personas_r = risk.get("personas") or []
        if personas_r:
            extra.append(f"cosai:affectsPersona {ref_list(personas_r)}")
        ctrls = risk.get("controls") or []
        if ctrls:
            extra.append(f"cosai:mitigatedBy {ref_list(ctrls)}")
        stages = normalize_multi(risk.get("lifecycleStage"), [])
        if stages and stages != ["all"] and "all" not in stages:
            extra.append("cosai:inLifecycleStage " + ", ".join(f"cosai:{stage_local(s)}" for s in stages))
        elif risk.get("lifecycleStage") == "all":
            extra.append(
                "cosai:inLifecycleStage "
                + ", ".join(f"cosai:{stage_local(s['id'])}" for s in lifecycle["lifecycleStages"])
            )
        impacts = normalize_multi(risk.get("impactType"), [])
        if impacts:
            extra.append("cosai:hasImpactType " + ", ".join(f"cosai:{impact_local(i)}" for i in impacts))
        access = normalize_multi(risk.get("actorAccess"), [])
        if access:
            extra.append("cosai:requiresActorAccess " + ", ".join(f"cosai:{access_local(a)}" for a in access))
        emit_individual(
            lines, risk["id"], [klass, "Risk"],
            risk["title"], catalog_comment(risk.get("shortDescription")),
            risk["id"], "risks.yaml", extra,
        )

    for control in controls["controls"]:
        klass = CONTROL_CLASS[control["category"]]
        extra = []
        personas_c = control.get("personas") or []
        if personas_c:
            extra.append(f"cosai:enactedBy {ref_list(personas_c)}")
        risk_vals = normalize_multi(control.get("risks"), risk_ids)
        if risk_vals:
            extra.append(f"cosai:mitigates {ref_list(risk_vals)}")
        comp_vals = normalize_multi(control.get("components"), component_ids)
        if comp_vals:
            extra.append(f"cosai:protects {ref_list(comp_vals)}")
        stages = normalize_multi(control.get("lifecycleStage"), [])
        if control.get("lifecycleStage") == "all":
            extra.append(
                "cosai:inLifecycleStage "
                + ", ".join(f"cosai:{stage_local(s['id'])}" for s in lifecycle["lifecycleStages"])
            )
        elif stages:
            extra.append("cosai:inLifecycleStage " + ", ".join(f"cosai:{stage_local(s)}" for s in stages))
        impacts = normalize_multi(control.get("impactType"), [])
        if impacts:
            extra.append("cosai:hasImpactType " + ", ".join(f"cosai:{impact_local(i)}" for i in impacts))
        emit_individual(
            lines, control["id"], [klass, "Control"],
            control["title"], catalog_comment(control.get("description")),
            control["id"], "controls.yaml", extra,
        )

    return "\n".join(lines) + "\n"


def collect_framework_terms(risks, controls, personas) -> dict[str, dict]:
    terms: dict[str, dict] = {}
    records = list(risks["risks"]) + list(controls["controls"]) + list(personas["personas"])
    for record in records:
        mappings = record.get("mappings") or {}
        for framework, values in mappings.items():
            if not values:
                continue
            for raw in values:
                ident, version = split_mapping(raw)
                key = f"{framework}:{ident}"
                if key not in terms:
                    iri = None
                    if framework == "mitre-atlas":
                        pattern = FRAMEWORK_BASE["mitre-atlas"][atlas_kind(ident)]
                        iri = pattern.format(id=ident)
                    terms[key] = {
                        "local": local_term_id(framework, ident),
                        "framework": framework,
                        "ident": ident,
                        "version": version,
                        "iri": iri,
                    }
                elif version and not terms[key]["version"]:
                    terms[key]["version"] = version
    return terms


def build_frameworks(risks, controls, personas, frameworks) -> str:
    terms = collect_framework_terms(risks, controls, personas)
    lines = [
        HEADER.rstrip(),
        "",
        f"<{ONTOLOGY_IRI}/alignments/frameworks> a owl:Ontology ;",
        f"    owl:imports <{ONTOLOGY_IRI}/catalog> ;",
        '    dcterms:title "CoSAI-RM mappings to ATLAS, NIST AI RMF, STRIDE, OWASP LLM, ISO 22989, and the EU AI Act"@en ;',
        '    rdfs:comment "Framework terms are named individuals. Links use skos:relatedMatch or skos:closeMatch. This graph does not assert owl:equivalentClass."@en .',
        "",
    ]

    fw_local = {
        "mitre-atlas": "frameworkMitreAtlas",
        "nist-ai-rmf": "frameworkNistAiRmf",
        "stride": "frameworkStride",
        "owasp-top10-llm": "frameworkOwaspLlm",
        "iso-22989": "frameworkIso22989",
        "eu-ai-act": "frameworkEuAiAct",
    }

    for fw in frameworks["frameworks"]:
        local = fw_local[fw["id"]]
        extra_comment = catalog_comment(fw.get("description"))
        lines.append(f"cosai:{local} a cosai:Framework ;")
        lines.append(f"    rdfs:label {literal(fw.get('fullName') or fw['name'])} ;")
        if extra_comment:
            lines.append(f"    rdfs:comment {literal(extra_comment)} ;")
        lines.append(f'    dcterms:identifier "{fw["id"]}" ;')
        if fw.get("baseUri"):
            lines.append(f"    rdfs:seeAlso <{fw['baseUri']}> ;")
        if fw.get("version"):
            lines.append(f'    owl:versionInfo "{fw["version"]}" ;')
        lines[-1] = lines[-1].rstrip(" ;") + " ."
        lines.append("")

    for term in terms.values():
        lines.append(f"cosai:{term['local']} a cosai:FrameworkTerm ;")
        lines.append(f'    rdfs:label "{ttl_escape(term["ident"])}" ;')
        lines.append(f'    dcterms:identifier "{ttl_escape(term["ident"])}" ;')
        lines.append(f"    cosai:inFramework cosai:{fw_local[term['framework']]} ;")
        if term["version"]:
            lines.append(f'    owl:versionInfo "{ttl_escape(term["version"])}" ;')
        if term["iri"]:
            lines.append(f"    rdfs:seeAlso <{term['iri']}> ;")
        lines[-1] = lines[-1].rstrip(" ;") + " ."
        lines.append("")

    def emit_maps(record):
        mappings = record.get("mappings") or {}
        if not mappings:
            return
        rid = record["id"]
        for framework, values in mappings.items():
            if not values:
                continue
            match = "skos:closeMatch" if framework in {"mitre-atlas", "owasp-top10-llm"} else "skos:relatedMatch"
            for raw in values:
                ident, _version = split_mapping(raw)
                local = local_term_id(framework, ident)
                lines.append(f"cosai:{rid} {match} cosai:{local} ;")
                lines.append(f"    cosai:mapsTo cosai:{local} .")
                lines.append("")

    for record in list(risks["risks"]) + list(controls["controls"]) + list(personas["personas"]):
        emit_maps(record)

    return "\n".join(lines) + "\n"


def build_opencre(risks, controls, personas) -> str:
    index = load_opencre_index()
    lines = [
        HEADER.rstrip(),
        "",
        f"<{ONTOLOGY_IRI}/alignments/opencre> a owl:Ontology ;",
        f"    owl:imports <{ONTOLOGY_IRI}/catalog> ;",
        '    dcterms:title "CoSAI-RM to OpenCRE alignments"@en ;',
        '    rdfs:comment "CRE links are inferred from CoSAI native mappings to MITRE ATLAS and OWASP Top 10 for LLM, joined to OpenCRE published links for those standards. Predicate is skos:relatedMatch. Provenance is recorded with dcterms:source and cosai:alignmentMethod."@en .',
        "",
    ]

    declared: set[str] = set()
    links: list[tuple[str, str, str, str]] = []  # subject, cre_id, via, native_id

    def consider(record, framework_key: str):
        mappings = record.get("mappings") or {}
        values = mappings.get(framework_key) or []
        for raw in values:
            ident, _version = split_mapping(raw)
            for cre_id, cre_name in lookup_cres(index, ident):
                if cre_id not in declared:
                    lines.append(f"cre:{cre_id} a skos:Concept ;")
                    lines.append(f"    skos:prefLabel {literal(cre_name)} ;")
                    lines.append(f'    dcterms:identifier "{cre_id}" ;')
                    lines.append(f"    rdfs:seeAlso <https://www.opencre.org/cre/{cre_id}> .")
                    lines.append("")
                    declared.add(cre_id)
                links.append((record["id"], cre_id, framework_key, ident))

    for record in list(risks["risks"]) + list(controls["controls"]) + list(personas["personas"]):
        consider(record, "mitre-atlas")
        consider(record, "owasp-top10-llm")

    # Deduplicate subject-CRE pairs, keep first via
    seen_pair = set()
    for subject, cre_id, via, ident in links:
        pair = (subject, cre_id)
        if pair in seen_pair:
            continue
        seen_pair.add(pair)
        lines.append(f"cosai:{subject} skos:relatedMatch cre:{cre_id} .")
        lines.append(f"[] a cosai:AlignmentAssertion ;")
        lines.append(f"    cosai:alignmentSubject cosai:{subject} ;")
        lines.append(f"    cosai:alignmentObject cre:{cre_id} ;")
        lines.append(f'    cosai:alignmentMethod "transitive-join" ;')
        lines.append(f'    cosai:alignmentVia "{ttl_escape(via)}" ;')
        lines.append(f'    dcterms:source "{ttl_escape(ident)}" ;')
        lines.append('    rdfs:comment "Join of a CoSAI native mapping onto an OpenCRE published link for the same ATLAS or OWASP LLM identifier. Not a community-reviewed exact match."@en .')
        lines.append("")

    lines.append(f"# CRE concepts declared: {len(declared)}")
    lines.append(f"# Alignment pairs: {len(seen_pair)}")
    return "\n".join(lines) + "\n"


def main() -> None:
    risks = load_yaml("risks.yaml")
    controls = load_yaml("controls.yaml")
    components = load_yaml("components.yaml")
    personas = load_yaml("personas.yaml")
    frameworks = load_yaml("frameworks.yaml")
    lifecycle = load_yaml("lifecycle-stage.yaml")
    impact = load_yaml("impact-type.yaml")
    actor = load_yaml("actor-access.yaml")

    ALIGN_DIR.mkdir(parents=True, exist_ok=True)
    catalog = build_catalog(risks, controls, components, personas, lifecycle, impact, actor)
    (OUT_DIR / "catalog.ttl").write_text(catalog, encoding="utf-8")
    (ALIGN_DIR / "frameworks.ttl").write_text(
        build_frameworks(risks, controls, personas, frameworks), encoding="utf-8"
    )
    (ALIGN_DIR / "opencre.ttl").write_text(
        build_opencre(risks, controls, personas), encoding="utf-8"
    )
    print("Wrote ontology/catalog.ttl")
    print("Wrote ontology/alignments/frameworks.ttl")
    print("Wrote ontology/alignments/opencre.ttl")
    print(
        f"Counts: risks={len(risks['risks'])} controls={len(controls['controls'])} "
        f"components={len(components['components'])} personas={len(personas['personas'])}"
    )


if __name__ == "__main__":
    main()
