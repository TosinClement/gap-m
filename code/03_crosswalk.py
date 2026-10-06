#!/usr/bin/env python3
"""03_crosswalk.py — compile the GAP-M control set and crosswalk, validate it, write outputs.

Inputs : data/registry/elements.json, mapping/gapm_controls.yaml, mapping/dispositions.yaml,
         RELEASE.yaml
Outputs: data/crosswalk/
           gapm_controls.json|csv        control set (one row per control)
           gapm_links.json|csv           crosswalk (one row per control x source element)
           gapm_dispositions.json|csv    every mappable source element and its disposition
           gapm_hti_attributes.csv       the 31 HTI-1 attributes with maintaining controls
           gapm_catalog_oscal.json       OSCAL 1.1.3 catalog of the control set
           gapm_crosswalk.json           everything above in one file
           GAP-M_crosswalk.xlsx          reviewer workbook
         data/processed/crosswalk_checks.json  validation results for 04_qa.py

Exits non-zero if any structural rule fails (see RULES below).
"""
import json
import os
import re
import sys
import uuid

import jsonschema
import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
REG = os.path.join(ROOT, "data", "registry")
OUT = os.path.join(ROOT, "data", "crosswalk")
PROC = os.path.join(ROOT, "data", "processed")
SCHEMA = os.path.join(ROOT, "schema")
NS = uuid.uuid5(uuid.NAMESPACE_URL, "https://github.com/TosinClement/gap-m")
PROPS = {"integral_to", "example_of", "precedes"}
STRENGTH = {"integral_to": 3, "precedes": 2, "example_of": 1}
FW_SHORT = {"AI RMF 1.0": "RMF", "NIST AI 800-4": "A84", "ONC HTI-1 (b)(11)": "HTI", "CISA CPG 2.0": "CPG"}

RULES = """
R1 every link target exists in the registry and is mappable
R2 every link property is integral_to, example_of, or precedes
R3 no control links the same target twice
R4 control ids are unique and every control has a family defined in the YAML
R5 every mappable element is either linked or dispositioned, never both
R6 every control has objective, activity, evidence, cadence, owner_role
R7 every link has a non-empty rationale ending in a period
R8 every JSON output validates against its schema
R9 every integral_to or precedes link has a necessity-audit entry with verdict 'supported'
R10 every audit entry matches the link's current property, and every audited control has a core statement
R11 no example_of rationale asserts necessity (cannot, must, requires, only if, depends on, needs)
R12 every link outside the necessity audit has an example_of review decision (keep or revise)
R13 no link removed by the example_of review is present; every removal names a test and a basis
"""
NECESSITY_WORDS = re.compile(r"\b(cannot|can't|must|requires?|only (if|when|safe)|depends on|needs?)\b", re.I)
SOURCE_TYPES = {
    "guidance": "Voluntary risk-management outcomes (NIST AI RMF 1.0). Not requirements.",
    "monitoring_challenge": "Monitoring challenges, gaps, and barriers reported by NIST AI 800-4. Not requirements and not controls.",
    "regulatory_disclosure_requirement": "Source-attribute disclosure requirements that a certified Health IT Module must support (45 CFR 170.315(b)(11)(iv)(B)). The obligation is on the module and its developer, not on deploying organizations.",
    "voluntary_practice": "Voluntary baseline cybersecurity practices with recommended actions (CISA CPG 2.0).",
    "suggested_practice": "GAP-M controls: suggested implementation practices authored for this work. Not requirements and not endorsed by any agency.",
}
COVERAGE_STATEMENT = ("A mapped element has at least one GAP-M control linked to it. Mapping coverage is a property of the crosswalk, "
                      "not of any organization: it does not show that an organization complies with a regulation, meets a framework "
                      "outcome, or monitors effectively.")


def load():
    rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
    el = json.load(open(os.path.join(REG, "elements.json"), encoding="utf-8"))
    cy = yaml.safe_load(open(os.path.join(ROOT, "mapping", "gapm_controls.yaml"), encoding="utf-8"))
    dy = yaml.safe_load(open(os.path.join(ROOT, "mapping", "dispositions.yaml"), encoding="utf-8"))
    au = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))
    ex = yaml.safe_load(open(os.path.join(ROOT, "mapping", "example_review.yaml"), encoding="utf-8"))
    return rel, el, cy, dy, au, ex


def main():
    rel, el, cy, dy, au, ex = load()
    E = {e["element_id"]: e for e in el}
    AUD = {a["link"]: a for a in au["links"]}
    EXR = {x: ("keep", ex["keep_notes"].get(x, ex["default_keep_note"])) for x in ex["keep"]}
    EXR.update({r["link"]: ("revise", r["basis"]) for r in ex["revise"]})
    REMOVED = {r["link"]: r for r in ex["remove"]}
    errors = []
    status = cy.get("review_status", "proposed")
    AR = yaml.safe_load(open(os.path.join(ROOT, "mapping", "author_review.yaml"), encoding="utf-8"))
    AR_SCOPE = {**{x: "census_integral_to" for x in AR["census"]["integral_to"]},
                **{x: "census_conditional" for x in AR["census"]["conditional"]},
                **{x: "random_sample" for x in AR["sampling"]["selected"]},
                **{x: "targeted_check" for k, v in AR.get("targeted", {}).items() for x in v}}

    def ar_status(entry):
        """Map a recorded author response to review_status; no response leaves the global status."""
        if not entry:
            return status
        if entry.get("status"):
            return entry["status"]
        r = entry["response"].lower()
        if r.startswith("accept as written") or r == "accept":
            return "accepted"
        if r.startswith("accept"):
            return "revised"
        if r.startswith("reject") or r.startswith("remove"):
            return "rejected"
        return status

    # ---------------- controls and links
    controls, links = [], []
    seen = set()
    for c in cy["controls"]:
        if c["id"] in seen:
            errors.append(f"R4 duplicate control {c['id']}")
        seen.add(c["id"])
        fam = cy["families"].get(c["family"])
        if not fam:
            errors.append(f"R4 unknown family {c['family']} on {c['id']}")
        for k in ("objective", "activity", "evidence", "cadence", "owner_role"):
            if not str(c.get(k, "")).strip():
                errors.append(f"R6 {c['id']} missing {k}")
        tgts = set()
        for t, prop, why in c["links"]:
            if t not in E or not E[t]["mappable"]:
                errors.append(f"R1 {c['id']} -> {t} not a mappable registry element")
                continue
            if prop not in PROPS:
                errors.append(f"R2 {c['id']} -> {t} bad property {prop}")
            if t in tgts:
                errors.append(f"R3 {c['id']} links {t} twice")
            tgts.add(t)
            if not why or not why.strip().endswith("."):
                errors.append(f"R7 {c['id']} -> {t} rationale")
            e = E[t]
            links.append({
                "link_id": f"{c['id']}>{t}", "control_id": c["id"], "target_id": t,
                "target_framework": e["framework"], "target_level": e["level"], "target_code": e["code"],
                "target_label": e["label"], "relationship": "supports", "property": prop,
                "rationale": why.strip(), "review_status": ar_status(AR["links"].get(f"{c['id']}>{t}")),
                "author_response": (AR["links"].get(f"{c['id']}>{t}") or {}).get("response", "not_reviewed"),
                "author_review_scope": AR_SCOPE.get(f"{c['id']}>{t}", "not_sampled"),
                "mapping_style": "NIST IR 8477 supportive relationship mapping",
                "target_source_type": e["source_type"],
                "audit_verdict": AUD[f"{c['id']}>{t}"]["verdict"] if f"{c['id']}>{t}" in AUD else "not_audited",
                "audit_original_property": AUD[f"{c['id']}>{t}"]["was"] if f"{c['id']}>{t}" in AUD else prop,
                "audit_basis": AUD[f"{c['id']}>{t}"]["basis"] if f"{c['id']}>{t}" in AUD else None,
                "audit_condition": AUD.get(f"{c['id']}>{t}", {}).get("condition"),
                "conditional": AUD.get(f"{c['id']}>{t}", {}).get("verdict") == "unresolved",
                "audit_relevance": AUD.get(f"{c['id']}>{t}", {}).get("relevance"),
                "audit_relevance_basis": AUD.get(f"{c['id']}>{t}", {}).get("relevance_basis"),
                "audit_pass1_property": (AUD[f"{c['id']}>{t}"].get("pass1") or {}).get("now") if f"{c['id']}>{t}" in AUD else None,
                "example_review": EXR[f"{c['id']}>{t}"][0] if f"{c['id']}>{t}" in EXR else ("not_applicable" if f"{c['id']}>{t}" in AUD else "missing"),
                "example_review_note": EXR.get(f"{c['id']}>{t}", (None, None))[1],
            })
            lid = f"{c['id']}>{t}"
            if prop in ("integral_to", "precedes") and AUD.get(lid, {}).get("verdict") != "supported":
                errors.append(f"R9 {lid} asserts {prop} without a supported audit entry")
            if lid in AUD and AUD[lid]["now"] != prop:
                errors.append(f"R10 {lid} audit says {AUD[lid]['now']} but link is {prop}")
            if lid in REMOVED:
                errors.append(f"R13 {lid} was removed by the example_of review but is still present")
            if lid not in AUD and lid not in EXR:
                errors.append(f"R12 {lid} has no necessity audit and no example_of review decision")
            if prop == "example_of" and NECESSITY_WORDS.search(why):
                errors.append(f"R11 {lid} example_of rationale asserts necessity: {why}")
        n = {fw: sum(1 for l in links if l["control_id"] == c["id"] and l["target_framework"] == fw) for fw in FW_SHORT}
        controls.append({
            "control_id": c["id"], "family": c["family"], "family_name": fam["name"] if fam else None,
            "a84_primary_category": fam["a84_primary"] if fam else None,
            "title": c["title"], "practice_type": "suggested_practice",
            "core": au["cores"].get(c["id"]), "objective": c["objective"], "activity": c["activity"],
            "evidence": c["evidence"], "cadence": c["cadence"], "owner_role": c["owner_role"],
            "links_total": sum(n.values()), **{f"links_{FW_SHORT[fw]}": v for fw, v in n.items()},
            "review_status": ar_status(AR["controls"].get(c["id"])),
            "author_response": (AR["controls"].get(c["id"]) or {}).get("response", "not_reviewed"),
        })

    # ---------------- dispositions
    linked = {}
    for l in links:
        linked.setdefault(l["target_id"], []).append(l)
    disp_in = dy["elements"]
    dispositions = []
    for e in el:
        if not e["mappable"]:
            continue
        eid = e["element_id"]
        L = linked.get(eid, [])
        if L and eid in disp_in:
            errors.append(f"R5 {eid} both linked and dispositioned")
        if not L and eid not in disp_in:
            errors.append(f"R5 {eid} neither linked nor dispositioned")
        best = max((l["property"] for l in L), key=lambda p: STRENGTH[p], default=None)
        dispositions.append({
            "element_id": eid, "framework": e["framework"], "level": e["level"], "parent_id": e["parent_id"],
            "code": e["code"], "label": e["label"], "source_type": e["source_type"],
            "disposition": "mapped" if L else disp_in[eid]["disposition"],
            "reason": None if L else disp_in[eid]["reason"],
            "n_controls": len(L), "n_integral": sum(l["property"] == "integral_to" for l in L),
            "strongest_property": best, "controls": ";".join(sorted(l["control_id"] for l in L)),
            "review_status": status,
        })
    present = {l["link_id"] for l in links}
    for lid, r in REMOVED.items():
        if not r.get("test") or not r.get("basis"):
            errors.append(f"R13 removal {lid} lacks a test or basis")
    for lid in EXR:
        if lid not in present and REMOVED.get(lid, {}).get("scope") != "author_review":
            errors.append(f"R12 review decision for missing link {lid}")
    for lid, a in AUD.items():
        cid = lid.split(">")[0]
        if lid not in present and lid not in REMOVED:
            errors.append(f"R10 audit entry for missing link {lid}")
        if cid not in au["cores"]:
            errors.append(f"R10 no core statement for {cid}")
    for eid in disp_in:
        if eid not in E or not E[eid]["mappable"]:
            errors.append(f"R5 disposition for unknown element {eid}")

    # ---------------- HTI attribute maintenance table
    hti = []
    for e in el:
        if e["level"] != "source_attribute":
            continue
        L = linked.get(e["element_id"], [])
        hti.append({
            "element_id": e["element_id"], "cfr_paragraph": e["locator"], "attribute": e["label"],
            "gapm_change_class": e.get("hti_gapm_change_class"),
            "must_indicate_if_not_available": bool(e.get("hti_na_flag")),
            "integral_controls": ";".join(sorted(l["control_id"] for l in L if l["property"] == "integral_to")),
            "precedes_controls": ";".join(sorted(l["control_id"] for l in L if l["property"] == "precedes")),
            "example_controls": ";".join(sorted(l["control_id"] for l in L if l["property"] == "example_of")),
        })

    # ---------------- OSCAL catalog
    oscal = build_oscal(rel, cy, controls, links, el)

    bundle = {
        "gapm_version": rel["version"], "release_date": rel["release_date"], "doi": rel["doi"],
        "mapping_style": "NIST IR 8477 supportive relationship mapping (doi:10.6028/NIST.IR.8477)",
        "review_status": status,
        "author_review": rel.get("author_review", "pending"),
        "coverage_statement": COVERAGE_STATEMENT,
        "source_types": SOURCE_TYPES,
        "sources": sources_meta(),
        "removed_links": [{"link_id": k, "test": v["test"], "basis": v["basis"],
                           "scope": v.get("scope", "example_of_review")} for k, v in REMOVED.items()],
        "controls": controls, "links": links, "dispositions": dispositions, "hti_attributes": hti,
    }

    # ---------------- schemas
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(PROC, exist_ok=True)
    checks = {}
    for name, obj, sch in [("controls", controls, "gapm_controls.schema.json"),
                           ("links", links, "gapm_links.schema.json"),
                           ("dispositions", dispositions, "gapm_dispositions.schema.json"),
                           ("bundle", bundle, "gapm_crosswalk.schema.json"),
                           ("elements", el, "elements.schema.json")]:
        s = json.load(open(os.path.join(SCHEMA, sch)))
        jsonschema.Draft202012Validator.check_schema(s)
        errs = sorted(jsonschema.Draft202012Validator(s).iter_errors(obj), key=lambda x: list(x.path))
        checks[f"schema_{name}"] = [f"{list(x.path)}: {x.message}" for x in errs[:10]]
        if errs:
            errors.append(f"R8 {name} schema: {errs[0].message}")
    # The OSCAL token pattern uses Unicode property classes that Python's re lacks;
    # translate \p{L} -> [^\W\d_] (letters) and \p{N} -> \d before validating.
    osc_txt = open(os.path.join(SCHEMA, "vendor", "oscal_catalog_schema.json"), encoding="utf-8").read()
    osc_txt = osc_txt.replace("\\\\p{L}", "[^\\\\W\\\\d_]").replace("\\\\p{N}", "\\\\d")
    osc_s = json.loads(osc_txt)
    oerrs = list(jsonschema.Draft7Validator(osc_s).iter_errors(oscal))
    checks["schema_oscal"] = [f"{list(x.path)}: {x.message}" for x in oerrs[:10]]
    if oerrs:
        errors.append(f"R8 OSCAL schema: {oerrs[0].message}")

    # ---------------- write
    def dump(name, obj):
        json.dump(obj, open(os.path.join(OUT, name), "w", encoding="utf-8"), ensure_ascii=False, indent=1)

    dump("gapm_controls.json", controls)
    dump("gapm_links.json", links)
    dump("gapm_dispositions.json", dispositions)
    dump("gapm_catalog_oscal.json", oscal)
    dump("gapm_crosswalk.json", bundle)
    pd.DataFrame(controls).to_csv(os.path.join(OUT, "gapm_controls.csv"), index=False)
    pd.DataFrame(links).to_csv(os.path.join(OUT, "gapm_links.csv"), index=False)
    pd.DataFrame(dispositions).to_csv(os.path.join(OUT, "gapm_dispositions.csv"), index=False)
    pd.DataFrame(hti).to_csv(os.path.join(OUT, "gapm_hti_attributes.csv"), index=False)
    workbook(rel, controls, links, dispositions, hti, el, bundle["removed_links"], AUD)

    checks["errors"] = errors
    checks["rules"] = RULES.strip().splitlines()
    checks["counts"] = {"controls": len(controls), "links": len(links), "dispositions": len(dispositions)}
    json.dump(checks, open(os.path.join(PROC, "crosswalk_checks.json"), "w"), indent=1)
    print(json.dumps(checks["counts"]), "errors:", len(errors))
    for e in errors[:40]:
        print("  ", e)
    if errors:
        sys.exit(1)


def sources_meta():
    return [
        {"id": "S1", "framework": "AI RMF 1.0", "title": "Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
         "publisher": "National Institute of Standards and Technology", "identifier": "NIST AI 100-1",
         "doi": "10.6028/NIST.AI.100-1", "date": "2023-01", "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf"},
        {"id": "S2", "framework": "NIST AI 800-4", "title": "Challenges to the Monitoring of Deployed AI Systems",
         "publisher": "National Institute of Standards and Technology", "identifier": "NIST AI 800-4",
         "doi": "10.6028/NIST.AI.800-4", "date": "2026-03", "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf"},
        {"id": "S3", "framework": "ONC HTI-1 (b)(11)", "title": "45 CFR 170.315(b)(11) Decision support interventions, paragraph (iv)(B)",
         "publisher": "Office of the National Coordinator for Health IT (ASTP/ONC), HHS",
         "identifier": "HTI-1 Final Rule, 89 FR 1192 (2024-01-09); eCFR text as of 2026-10-01", "doi": None,
         "date": "2026-10-01", "url": "https://www.ecfr.gov/current/title-45/subtitle-A/subchapter-D/part-170/subpart-C/section-170.315"},
        {"id": "S4", "framework": "CISA CPG 2.0", "title": "Cybersecurity Performance Goals 2.0 (CPG 2.0)",
         "publisher": "Cybersecurity and Infrastructure Security Agency", "identifier": "CPG 2.0",
         "doi": None, "date": "2025-12-10", "url": "https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0"},
    ]


def uid(*parts):
    return str(uuid.uuid5(NS, "/".join(parts)))


def build_oscal(rel, cy, controls, links, el):
    E = {e["element_id"]: e for e in el}
    res = {s["framework"]: uid("resource", s["id"]) for s in sources_meta()}
    groups = []
    for fam, meta in cy["families"].items():
        ctrls = []
        for c in [c for c in controls if c["family"] == fam]:
            props = [{"name": "label", "value": c["control_id"]},
                     {"name": "a84-primary-category", "ns": "https://w3id.org/gap-m/ns", "value": c["a84_primary_category"]},
                     {"name": "review-status", "ns": "https://w3id.org/gap-m/ns", "value": c["review_status"]}]
            for l in [l for l in links if l["control_id"] == c["control_id"]]:
                props.append({"name": "supports", "ns": "https://w3id.org/gap-m/ns", "value": l["target_id"],
                              "class": l["property"],
                              "remarks": f"{l['rationale']} Pre-review audit: {l['audit_verdict'].replace('_', ' ')}."})
            fws = sorted({l["target_framework"] for l in links if l["control_id"] == c["control_id"]})
            ctrls.append({
                "id": c["control_id"].lower(), "class": "gap-m-control", "title": c["title"], "props": props,
                "links": [{"href": f"#{res[f]}", "rel": "reference", "text": f} for f in fws],
                "parts": [
                    {"id": f"{c['control_id'].lower()}_smt", "name": "statement", "prose": c["objective"]},
                    {"id": f"{c['control_id'].lower()}_act", "name": "guidance", "title": "Monitoring activity", "prose": c["activity"]},
                    {"id": f"{c['control_id'].lower()}_obj", "name": "assessment-objective", "title": "Evidence", "prose": c["evidence"]},
                    {"id": f"{c['control_id'].lower()}_cad", "name": "guidance", "title": "Cadence", "prose": c["cadence"]},
                    {"id": f"{c['control_id'].lower()}_own", "name": "guidance", "title": "Owner role", "prose": c["owner_role"]},
                ],
            })
        groups.append({"id": fam.lower(), "class": "family", "title": meta["name"], "controls": ctrls})
    ts = f"{rel['build_date']}T00:00:00Z"
    return {"catalog": {
        "uuid": uid("catalog", rel["version"]),
        "metadata": {
            "title": rel["title"], "last-modified": ts, "version": rel["version"], "oscal-version": "1.1.3",
            "props": [{"name": "marking", "value": "FINAL" if rel.get("final") else ("RELEASE-CANDIDATE" if (rel.get("author_review") == "complete" and not rel.get("final")) else "DRAFT")}],
            "roles": [{"id": "creator", "title": "Author"}],
            "parties": [{"uuid": uid("party", "clement"), "type": "person", "name": "Tosin Clement",
                         "external-ids": [{"scheme": "http://orcid.org/", "id": "0009-0001-2055-5113"}],
                         "email-addresses": ["clementtosin92@gmail.com"]}],
            "responsible-parties": [{"role-id": "creator", "party-uuids": [uid("party", "clement")]}],
            "remarks": ("" if rel.get("final") else "Unpublished draft; links are proposed and not author-reviewed. ") + "Mapping coverage does not demonstrate compliance or effectiveness. GAP-M controls are original to this work. Each 'supports' prop names a source element (NIST AI RMF 1.0, NIST AI 800-4, 45 CFR 170.315(b)(11)(iv)(B), CISA CPG 2.0); prop class gives the NIST IR 8477 relationship property; remarks give the rationale. Not a NIST, ONC, or CISA product.",
        },
        "groups": groups,
        "back-matter": {"resources": [
            {"uuid": res[s["framework"]], "title": s["title"],
             "citation": {"text": f"{s['publisher']}. {s['title']}. {s['identifier']}." + (f" doi:{s['doi']}" if s["doi"] else "")},
             "rlinks": [{"href": s["url"]}]} for s in sources_meta()]},
    }}


def workbook(rel, controls, links, dispositions, hti, el, removed, AUD):
    path = os.path.join(OUT, "GAP-M_crosswalk.xlsx")
    from openpyxl.styles import Font, PatternFill, Alignment
    readme = pd.DataFrame({"GAP-M crosswalk workbook": [
        f"{rel['title']} v{rel['version']} ({'FINAL' if rel.get('final') else ('release candidate: author review complete; not for citation until released' if (rel.get('author_review') == 'complete' and not rel.get('final')) else 'DRAFT: not for citation until released')})",
        "Controls: the GAP-M monitoring control set.",
        "Links: one row per control and source element, with NIST IR 8477 property and rationale.",
        "Dispositions: every mappable source element and whether it is mapped, a prerequisite, or out of scope.",
        "HTI_attributes: the 31 predictive-DSI source attributes and the controls that keep each current.",
        "Matrix: link counts by control and framework.",
        "Registry: verbatim source text with locators.",
        "Audit: necessity audit of every link that asserted integral_to or precedes (pre-review, AI-assisted; not author review).",
        "Links columns example_review / example_review_note: tooling-assisted relevance review of the original example_of links by the AI assistant (not independent expert validation; not author review).",
        f"Links column conditional = TRUE: the {sum(1 for l in links if l.get('conditional'))} unresolved necessity links, kept as conditional example_of mappings; necessity recorded as unresolved; each reviewed and accepted as conditional by the author. "
        "Their relevance as example_of mappings is assessed separately (columns audit_relevance, audit_relevance_basis).",
        "Removed: every link removed during review, with the failed test (T1 relevance, T2 source interpretation, T3 unsupported claim) and the basis.",
        "Ledger: every link of the original build reconciled by its original relationship type.",
        "SourceTypes: what kind of statement each source makes (guidance, monitoring challenge, regulatory disclosure requirement, voluntary practice) and what GAP-M controls are (suggested practices).",
        COVERAGE_STATEMENT,
        "review_status: per control and link, from the author's recorded responses (mapping/author_review.yaml). Columns author_response and author_review_scope show what the author individually reviewed; links without a response keep 'proposed'. " + ("Author review is complete within the scope recorded in docs/AUTHOR_REVIEW.md." if rel.get("author_review") == "complete" else "Author review is pending."),
        "Edit mapping/gapm_controls.yaml, not this workbook; the workbook is regenerated by code/03_crosswalk.py.",
        "License: CC BY 4.0. Cite as: Clement, T. GAP-M (see CITATION.cff).",
    ]})
    m = pd.DataFrame(links).pivot_table(index="control_id", columns="target_framework", values="link_id",
                                        aggfunc="count", fill_value=0)
    reg = pd.DataFrame(el)[["element_id", "framework", "source_type", "obligation_holder", "level", "parent_id", "code", "label", "text", "locator", "mappable"]]
    aud = pd.DataFrame([l for l in links if l["audit_verdict"] != "not_audited"])[
        ["link_id", "audit_original_property", "audit_pass1_property", "property", "audit_verdict", "audit_basis", "audit_condition",
         "audit_relevance", "audit_relevance_basis", "rationale"]]
    st = pd.DataFrame([{"source_type": k, "meaning": v} for k, v in SOURCE_TYPES.items()])
    rm = pd.DataFrame(removed)
    rm["original_property"] = [AUD[r["link_id"]]["was"] if r["link_id"] in AUD else "example_of" for r in removed]
    rows = []
    for p in ("integral_to", "precedes"):
        A_ = [a for a in AUD.values() if a["was"] == p]
        present = {l["link_id"] for l in links}
        rows.append({"original_property": p, "original": len(A_),
                     "kept_as_is": sum(a["verdict"] == "supported" and a["link"] in present for a in A_),
                     "to_example_of": sum(a["verdict"] == "revised" and a["link"] in present for a in A_),
                     "conditional_example_of_unresolved": sum(a["verdict"] == "unresolved" and a["link"] in present for a in A_),
                     "removed": sum(a["link"] not in present for a in A_)})
    ex_now = [l for l in links if l["audit_verdict"] == "not_audited"]
    ex_rm = [r for r in removed if r["link_id"] not in AUD]
    rows.append({"original_property": "example_of", "original": len(ex_now) + len(ex_rm), "kept_as_is": len(ex_now),
                 "to_example_of": None, "conditional_example_of_unresolved": None, "removed": len(ex_rm)})
    rows.append({"original_property": "TOTAL", "original": sum(r["original"] for r in rows),
                 "kept_as_is": None, "to_example_of": None, "conditional_example_of_unresolved": None, "removed": len(removed)})
    ledger = pd.DataFrame(rows)
    with pd.ExcelWriter(path, engine="openpyxl") as w:
        readme.to_excel(w, sheet_name="README", index=False)
        pd.DataFrame(controls).to_excel(w, sheet_name="Controls", index=False)
        pd.DataFrame(links).to_excel(w, sheet_name="Links", index=False)
        pd.DataFrame(dispositions).to_excel(w, sheet_name="Dispositions", index=False)
        pd.DataFrame(hti).to_excel(w, sheet_name="HTI_attributes", index=False)
        aud.to_excel(w, sheet_name="Audit", index=False)
        ledger.to_excel(w, sheet_name="Ledger", index=False)
        rm.to_excel(w, sheet_name="Removed", index=False)
        st.to_excel(w, sheet_name="SourceTypes", index=False)
        m.to_excel(w, sheet_name="Matrix")
        reg.to_excel(w, sheet_name="Registry", index=False)
        for ws in w.book.worksheets:
            ws.freeze_panes = "B2"
            for cell in ws[1]:
                cell.font = Font(bold=True, color="FFFFFF")
                cell.fill = PatternFill("solid", fgColor="1F3A5F")
            for col in ws.columns:
                width = min(60, max(10, max(len(str(c.value or "")) for c in col[:50]) + 2))
                ws.column_dimensions[col[0].column_letter].width = width
                for c in col[1:]:
                    c.alignment = Alignment(wrap_text=width >= 60, vertical="top")
        import datetime as _dt
        fixed = _dt.datetime.fromisoformat(rel["build_date"])
        w.book.properties.created = fixed
        w.book.properties.modified = fixed
    normalize_zip(path, rel["build_date"])


def normalize_zip(path, build_date):
    """Rewrite the .xlsx archive with fixed entry timestamps so rebuilds are byte-identical."""
    import zipfile
    y, m, d = (int(x) for x in build_date.split("-"))
    with zipfile.ZipFile(path) as z:
        items = [(i.filename, z.read(i.filename)) for i in z.infolist()]
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in items:
            if name == "docProps/core.xml":  # openpyxl stamps the save time into dcterms:modified
                import re as _re
                data = _re.sub(rb"(<dcterms:(?:created|modified)[^>]*>)[^<]*(</dcterms:)",
                               lambda mm: mm.group(1) + f"{build_date}T00:00:00Z".encode() + mm.group(2), data)
            zi = zipfile.ZipInfo(name, date_time=(y, m, d, 0, 0, 0))
            zi.compress_type = zipfile.ZIP_DEFLATED
            zi.external_attr = 0o644 << 16
            z.writestr(zi, data)


if __name__ == "__main__":
    main()
