#!/usr/bin/env python3
"""04_qa.py — QA report and the stats file every document reads its numbers from.

Writes data/processed/qa_report.txt and report/stats.json.
Also runs negative tests: deliberately broken inputs must be rejected by the checks.
"""
import copy
import json
import os
import statistics
import sys

import jsonschema
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
FW = ["AI RMF 1.0", "NIST AI 800-4", "ONC HTI-1 (b)(11)", "CISA CPG 2.0"]
SHORT = {"AI RMF 1.0": "rmf", "NIST AI 800-4": "a84", "ONC HTI-1 (b)(11)": "hti", "CISA CPG 2.0": "cpg"}
SPOT = ["RMF:GOVERN-1.4", "RMF:MAP-1.1", "RMF:MEASURE-2.4", "RMF:MANAGE-4.1", "A84:HF-G2", "A84:XC-TMT-B3",
        "HTI:B4.iv", "HTI:B7.v", "HTI:B8.ii", "CPG:3.Q", "CPG:1.D", "CPG:4.B"]


def pct(a, b):
    return round(100.0 * a / b, 1) if b else 0.0


def main():
    rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
    rq = J("data", "registry", "registry_qa.json")
    el = J("data", "registry", "elements.json")
    E = {e["element_id"]: e for e in el}
    cc = J("data", "processed", "crosswalk_checks.json")
    controls = J("data", "crosswalk", "gapm_controls.json")
    links = J("data", "crosswalk", "gapm_links.json")
    disp = J("data", "crosswalk", "gapm_dispositions.json")
    hti = J("data", "crosswalk", "gapm_hti_attributes.json") if os.path.exists(
        os.path.join(ROOT, "data", "crosswalk", "gapm_hti_attributes.json")) else J("data", "crosswalk", "gapm_crosswalk.json")["hti_attributes"]

    S = {"version": rel["version"], "build_date": rel["build_date"], "release_date": rel["release_date"], "doi": rel["doi"]}
    S["n_controls"] = len(controls)
    S["n_families"] = len({c["family"] for c in controls})
    S["n_links"] = len(links)
    S["n_elements_mappable"] = len(disp)
    S["src"] = {
        "rmf_functions": 4, "rmf_categories": rq["rmf"]["categories"], "rmf_subcategories": rq["rmf"]["subcategories"],
        "a84_categories": rq["ai800_4"]["categories"], "a84_category_challenges": rq["ai800_4"]["category_challenges"],
        "a84_crosscutting_categories": 5, "a84_crosscutting_items": rq["ai800_4"]["crosscutting_items"],
        "hti_groups": rq["hti"]["groups"], "hti_attributes": rq["hti"]["attributes"],
        "cpg_functions": len(rq["cpg"]["by_function"]), "cpg_goals": rq["cpg"]["goals"],
    }
    # coverage by framework
    cov = {}
    for fw in FW:
        D = [d for d in disp if d["framework"] == fw]
        m = [d for d in D if d["disposition"] == "mapped"]
        cov[SHORT[fw]] = {"elements": len(D), "mapped": len(m), "mapped_pct": pct(len(m), len(D)),
                          "prerequisite": sum(d["disposition"] == "prerequisite" for d in D),
                          "out_of_scope": sum(d["disposition"] == "out_of_scope" for d in D),
                          "uncovered": sum(d["disposition"] == "uncovered" for d in D),
                          "with_integral": sum(d["n_integral"] > 0 for d in D),
                          "with_integral_pct": pct(sum(d["n_integral"] > 0 for d in D), len(D)),
                          "links": sum(l["target_framework"] == fw for l in links)}
    S["coverage"] = cov
    S["mapped_total"] = sum(d["disposition"] == "mapped" for d in disp)
    S["mapped_total_pct"] = pct(S["mapped_total"], len(disp))
    # sub-group coverage
    def group_cov(fw, key):
        out = {}
        for d in [d for d in disp if d["framework"] == fw]:
            g = key(d)
            o = out.setdefault(g, {"elements": 0, "mapped": 0, "with_integral": 0})
            o["elements"] += 1
            o["mapped"] += d["disposition"] == "mapped"
            o["with_integral"] += d["n_integral"] > 0
        return out
    S["rmf_by_function"] = group_cov("AI RMF 1.0", lambda d: d["code"].split()[0])
    S["cpg_by_function"] = group_cov("CISA CPG 2.0", lambda d: E[d["element_id"]]["parent_id"].split(":")[1].title())
    S["hti_by_group"] = group_cov("ONC HTI-1 (b)(11)", lambda d: d["parent_id"].split(":")[1])
    S["a84_by_category"] = group_cov("NIST AI 800-4", lambda d: (d["parent_id"] or d["element_id"]).split(":")[1].split("-")[0] if not d["level"].startswith("crosscutting") else "XC")
    # properties
    S["property_counts"] = {p: sum(l["property"] == p for l in links) for p in ("integral_to", "example_of", "precedes")}
    S["property_pct"] = {p: pct(v, len(links)) for p, v in S["property_counts"].items()}
    lpc = [c["links_total"] for c in controls]
    S["links_per_control"] = {"min": min(lpc), "median": statistics.median(lpc), "max": max(lpc),
                              "max_control": max(controls, key=lambda c: c["links_total"])["control_id"]}
    mapped = [d for d in disp if d["disposition"] == "mapped"]
    cpe = [d["n_controls"] for d in mapped]
    S["controls_per_mapped_element"] = {"min": min(cpe), "median": statistics.median(cpe), "max": max(cpe),
                                        "max_element": max(mapped, key=lambda d: d["n_controls"])["element_id"]}
    S["controls_by_family"] = {f: sum(c["family"] == f for c in controls) for f in dict.fromkeys(c["family"] for c in controls)}
    S["controls_touching_all_four"] = sum(all(c[f"links_{k}"] > 0 for k in ("RMF", "A84", "HTI", "CPG")) for c in controls)
    S["controls_touching_three_plus"] = sum(sum(c[f"links_{k}"] > 0 for k in ("RMF", "A84", "HTI", "CPG")) >= 3 for c in controls)
    # HTI: GAP-M analytic change classes, and how each class is linked (counts reconcile to 31)
    order = ["static_at_release", "process_description", "evidence_accruing", "locally_measured"]
    S["hti_classes"] = {k: sum(h["gapm_change_class"] == k for h in hti) for k in order}
    S["hti_by_class"] = {}
    for k in order:
        H = [h for h in hti if h["gapm_change_class"] == k]
        S["hti_by_class"][k] = {
            "attributes": len(H),
            "with_integral": sum(bool(h["integral_controls"]) for h in H),
            "with_precedes": sum(bool(h["precedes_controls"]) for h in H),
            "example_only": sum(not h["integral_controls"] and not h["precedes_controls"] for h in H),
            "na_flag": sum(h["must_indicate_if_not_available"] for h in H),
            "ids_with_integral": [h["element_id"] for h in H if h["integral_controls"]],
        }
    S["hti_na_flag"] = sum(h["must_indicate_if_not_available"] for h in hti)
    S["hti_with_integral"] = sum(bool(h["integral_controls"]) for h in hti)
    S["hti_with_integral_ids"] = [h["element_id"] for h in hti if h["integral_controls"]]
    S["hti_with_precedes"] = sum(bool(h["precedes_controls"]) for h in hti)
    S["necessity_links"] = [{"link_id": l["link_id"], "property": l["property"], "target_code": l["target_code"],
                             "target_framework": l["target_framework"], "control_id": l["control_id"]}
                            for l in links if l["property"] in ("integral_to", "precedes")]
    _a2 = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))
    S["pass2"] = {"changed": [{"link_id": a["link"], "pass1_verdict": a["pass1"]["verdict"], "pass1_property": a["pass1"]["now"],
                               "verdict": a["verdict"], "property": a["now"]} for a in _a2["links"] if a.get("pass1")],
                  "rechecked": 21,
                  "cores_narrowed": sorted(_a2.get("second_pass", {}).get("cores_previous", {}).keys()),
                  "conditional_relevance_supported": sum(a.get("relevance") == "supported" for a in _a2["links"] if a["verdict"] == "unresolved"),
                  "conditional_relevance_unsupported": sum(a.get("relevance") == "unsupported" for a in _a2["links"] if a["verdict"] == "unresolved")}
    S["hti_example_only"] = sum(not h["integral_controls"] and not h["precedes_controls"] for h in hti)
    S["hti_not_static"] = len(hti) - S["hti_classes"]["static_at_release"]
    assert sum(v["attributes"] for v in S["hti_by_class"].values()) == len(hti) == S["src"]["hti_attributes"]
    # necessity audit
    # audit statistics come from the audit record itself (all 107 entries), so later removals do not change them
    _aud_rec = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))["links"]
    aud = [{"link_id": a["link"], "audit_verdict": a["verdict"], "audit_original_property": a["was"],
            "target_source_type": E[a["link"].split(">")[1]]["source_type"]} for a in _aud_rec]
    S["audit"] = {
        "audited": len(aud),
        "audited_integral": sum(l["audit_original_property"] == "integral_to" for l in aud),
        "audited_precedes": sum(l["audit_original_property"] == "precedes" for l in aud),
        "supported": sum(l["audit_verdict"] == "supported" for l in aud),
        "revised": sum(l["audit_verdict"] == "revised" for l in aud),
        "unresolved": sum(l["audit_verdict"] == "unresolved" for l in aud),
        "by_original": {p: {v: sum(l["audit_original_property"] == p and l["audit_verdict"] == v for l in aud)
                            for v in ("supported", "revised", "unresolved")} for p in ("integral_to", "precedes")},
        "by_source_type": {t: {v: sum(l["target_source_type"] == t and l["audit_verdict"] == v for l in aud)
                               for v in ("supported", "revised", "unresolved")}
                           for t in ("guidance", "monitoring_challenge", "regulatory_disclosure_requirement", "voluntary_practice")},
        "unresolved_ids": [l["link_id"] for l in aud if l["audit_verdict"] == "unresolved"],
        "supported_ids": [l["link_id"] for l in aud if l["audit_verdict"] == "supported"],
    }
    S["author_review"] = rel.get("author_review", "pending")
    # ---- guided author review: what the author has individually reviewed (mapping/author_review.yaml)
    AR = yaml.safe_load(open(os.path.join(ROOT, "mapping", "author_review.yaml"), encoding="utf-8"))
    _present = {l["link_id"] for l in links}
    _targeted = {x for v in AR.get("targeted", {}).values() for x in v}
    _set = set(AR["census"]["integral_to"]) | set(AR["census"]["conditional"]) | set(AR["sampling"]["selected"]) | _targeted
    _resp = AR["links"]
    _status = lambda k: _resp[k].get("status")
    S["author_review_progress"] = {
        "controls_total": len(controls), "controls_reviewed": sum(c in AR["controls"] for c in (x["control_id"] for x in controls)),
        "controls_accepted_as_written": sum(v["response"].startswith("Accept as written") for v in AR["controls"].values()),
        "controls_accepted_with_edits": sum(v["response"].startswith("Accept with") for v in AR["controls"].values()),
        "census_integral_to": len(AR["census"]["integral_to"]), "census_conditional": len(AR["census"]["conditional"]),
        "sample_seed": AR["sampling"]["seed"], "sample_population": AR["sampling"]["population_size"],
        "sample_size": AR["sampling"]["sample_size"], "sample_fraction": AR["sampling"]["fraction"],
        "targeted_checks": len(_targeted),
        "earlier_removals_ruled": sum(v["kind"] == "removal" for v in AR.get("earlier_review_changes", {}).values()),
        "earlier_rewordings_ruled": sum(v["kind"] == "rewording" for v in AR.get("earlier_review_changes", {}).values()),
        "links_in_review_set": len(_set), "links_reviewed": sum(k in _resp for k in _set),
        "links_accepted": sum(k in _resp and _status(k) == "accepted" for k in _set),
        "links_revised": sum(k in _resp and _status(k) == "revised" for k in _set),
        "links_removed": sum(k in _resp and _status(k) == "rejected" for k in _set),
        "links_current_reviewed": len(_present & {k for k in _set if k in _resp}),
        "links_current_unreviewed": len(_present - {k for k in _set if k in _resp}),
        "consistency_edited_unreviewed": len({x for e in AR.get("consistency_edits", []) for x in e["links"]} - _set),
        "spot_checks": {k: v["response"] for k, v in AR.get("spot_checks", {}).items()},
    }
    _p = S["author_review_progress"]
    assert _p["links_current_reviewed"] + _p["links_current_unreviewed"] == len(links)
    _aud = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))["links"]
    _down = [a["link"] for a in _aud if a["verdict"] == "revised" and a["link"] in _present]
    _p["downgraded_current"] = len(_down)
    _p["downgraded_reviewed"] = sum(k in _set and k in _resp for k in _down)
    S["author_review_scope_text"] = (
        f"Author review: {S['author_review']}. " + ("The author individually reviewed" if S["author_review"] == "complete" else "So far the author has individually reviewed") + f" all {_p['controls_reviewed']} practice definitions, "
        f"every integral_to link ({_p['census_integral_to']}), every conditional link ({_p['census_conditional']}), a seeded random sample of "
        f"{_p['sample_size']} of the {_p['sample_population']} other example_of links ({int(_p['sample_fraction'] * 100)}%, seed {_p['sample_seed']}), "
        + (f"plus {_p['targeted_checks']} links in targeted checks; ruled on all {_p['earlier_removals_ruled']} removals from the earlier AI-assisted review; " if _p['targeted_checks'] else "")
        + f"and spot-checked source text in {len(_p['spot_checks'])} of the 4 sources. {_p['links_current_unreviewed']} of the {len(links)} current links have not been individually reviewed by the author. "
        "Details and the remaining checklist items are in docs/AUTHOR_REVIEW.md.")
    # ---- link ledger: every link of the original build, reconciled by original relationship type
    ex = yaml.safe_load(open(os.path.join(ROOT, "mapping", "example_review.yaml"), encoding="utf-8"))
    removed = {r["link"]: r for r in ex["remove"]}
    removed_ex = {k: v for k, v in removed.items() if v.get("scope") != "author_review"}
    removed_auth = {k: v for k, v in removed.items() if v.get("scope") == "author_review"}
    assert len(removed_ex) + len(removed_auth) == len(removed)
    assert len(ex["keep"]) + len(ex["revise"]) + len([k for k in removed_ex if k not in {a["link"] for a in yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))["links"]}]) == 210
    cur = {l["link_id"]: l for l in links}
    aud_all = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))["links"]
    A = {a["link"]: a for a in aud_all}
    orig_ex = [k for k in list(cur) + list(removed) if k not in A]          # example_of from the start
    led = {"integral_to": {}, "precedes": {}, "example_of": {}}
    for p in ("integral_to", "precedes"):
        P = [a for a in aud_all if a["was"] == p]
        led[p] = {"original": len(P),
                  "still_" + p: sum(a["verdict"] == "supported" and a["link"] in cur for a in P),
                  "to_example_of_revised": sum(a["verdict"] == "revised" and a["link"] in cur for a in P),
                  "to_example_of_conditional_unresolved": sum(a["verdict"] == "unresolved" and a["link"] in cur for a in P),
                  "removed_by_example_review": sum(a["link"] in removed_ex for a in P),
                  "removed_by_author_review": sum(a["link"] in removed_auth for a in P)}
        assert sum(v for k, v in led[p].items() if k != "original") == led[p]["original"]
    led["example_of"] = {"original": len(orig_ex),
                         "kept": sum(k in cur and cur[k]["example_review"] == "keep" for k in orig_ex),
                         "kept_rationale_revised": sum(k in cur and cur[k]["example_review"] == "revise" for k in orig_ex),
                         "removed": sum(k in removed_ex for k in orig_ex),
                         "removed_by_author_review": sum(k in removed_auth for k in orig_ex)}
    assert (led["example_of"]["kept"] + led["example_of"]["kept_rationale_revised"] + led["example_of"]["removed"]
            + led["example_of"]["removed_by_author_review"]) == led["example_of"]["original"]
    led["original_total"] = sum(led[p]["original"] for p in ("integral_to", "precedes", "example_of"))
    led["removed_total"] = len(removed)
    led["removed_by_example_review_total"] = len(removed_ex)
    led["removed_by_author_review_total"] = len(removed_auth)
    led["current_total"] = len(links)
    led["current_by_property"] = S["property_counts"]
    assert led["original_total"] - led["removed_total"] == led["current_total"]
    assert led["current_by_property"]["integral_to"] == led["integral_to"]["still_integral_to"]
    assert led["current_by_property"]["precedes"] == led["precedes"]["still_precedes"]
    led["conditional_links"] = sum(l["conditional"] for l in links)
    S["ledger"] = led
    # The AI-assisted example_of review is reported as it was made; later author removals are counted separately.
    S["example_review"] = {"reviewed": led["example_of"]["original"], "kept": len(ex["keep"]),
                           "revised": len(ex["revise"]), "removed": led["example_of"]["removed"],
                           "later_removed_by_author": led["example_of"]["removed_by_author_review"],
                           "audited_removed": led["integral_to"]["removed_by_example_review"] + led["precedes"]["removed_by_example_review"],
                           "removed_by_test": {t: sum(r["test"] == t for r in removed_ex.values()) for t in ("T1", "T2", "T3")},
                           "newly_unmapped": [d["element_id"] for d in disp if d["reason"] and d["reason"].startswith("(2026-10-05 review)")]}
    S["n_uncovered"] = sum(d["disposition"] == "uncovered" for d in disp)
    # weakly supported (mapped, but only example_of)
    S["weak_elements"] = [d["element_id"] for d in mapped if d["strongest_property"] == "example_of"]
    S["n_weak_elements"] = len(S["weak_elements"])
    S["unmapped"] = [{"element_id": d["element_id"], "disposition": d["disposition"]} for d in disp if d["disposition"] != "mapped"]
    S["cpg_hash_match"] = rq["cpg"]["matches_live_capture"]
    S["a84_strings_verified"] = rq["ai800_4"]["strings_checked"]
    S["rmf_dehyphenations"] = len(rq["rmf"]["dehyphenation"])
    S["hti_section_last_amended"] = rq["hti"]["section_last_amended"]

    neg = negative_tests(links, disp)
    S["negative_tests_passed"] = sum(neg.values())
    S["negative_tests_total"] = len(neg)
    _p = S["author_review_progress"]
    # ---- the author's release statement must match the review record (refused in a final build if it drifts)
    _st = str(rel.get("ai_statement_final") or "")
    if _st.strip():
        _words = {16: "Sixteen"}
        need = [f"Of the {len(links)} links in this release, {_p['links_current_unreviewed']} were not individually reviewed",
                f"I reviewed all {_p['controls_reviewed']} practice definitions, accepting {_p['controls_accepted_as_written']} as written and {_p['controls_accepted_with_edits']} with edits",
                f"I individually reviewed {_p['links_reviewed']} links: all {_p['census_integral_to']} `integral_to` links, all {_p['census_conditional']} conditional links",
                f"a random sample of {_p['sample_size']} of the {_p['sample_population']} other `example_of` links",
                f"seed {_p['sample_seed']}", f"and {_p['targeted_checks']} links in targeted checks",
                f"I accepted {_p['links_accepted']} as written, accepted {_p['links_revised']} with reworded rationales, and removed {_p['links_removed']}",
                f"I confirmed its {_p['earlier_removals_ruled']} removals",
                f"{_words.get(_p['consistency_edited_unreviewed'], _p['consistency_edited_unreviewed'])} of them received wording-only consistency edits",
                f"I reviewed {_p['downgraded_reviewed']} of the {_p['downgraded_current']}",
                f"including {S['a84_strings_verified']} strings from NIST AI 800-4",
                f"({S['negative_tests_passed']} of {S['negative_tests_total']} tests)"]
        missing = [n for n in need if n not in _st]
        S["statement_check"] = {"checked": len(need), "mismatched": missing}
        if missing and rel.get("final"):
            raise SystemExit("ai_statement_final no longer matches the review record: " + " | ".join(missing))
    else:
        S["statement_check"] = {"checked": 0, "mismatched": []}

    os.makedirs(os.path.join(ROOT, "report"), exist_ok=True)
    json.dump(S, open(os.path.join(ROOT, "report", "stats.json"), "w"), indent=1)
    write_report(S, rq, cc, E, disp, neg)
    ok = not cc["errors"] and S["cpg_hash_match"] and all(neg.values())
    print("QA", "PASS" if ok else "FAIL")
    if not ok:
        sys.exit(1)


def negative_tests(links, disp):
    """Each corrupted input must FAIL its schema; True means the check caught it."""
    sl = json.load(open(os.path.join(ROOT, "schema", "gapm_links.schema.json")))
    sd = json.load(open(os.path.join(ROOT, "schema", "gapm_dispositions.schema.json")))
    v = lambda s, o: not jsonschema.Draft202012Validator(s).is_valid(o)
    t = {}
    a = copy.deepcopy(links); a[0]["property"] = "related_to"; t["bad_property_rejected"] = v(sl, a)
    a = copy.deepcopy(links); a[0]["target_id"] = "XYZ:1"; t["bad_target_prefix_rejected"] = v(sl, a)
    a = copy.deepcopy(links); a[0]["rationale"] = "no period"; t["rationale_without_period_rejected"] = v(sl, a)
    a = copy.deepcopy(disp); m = next(d for d in a if d["disposition"] == "mapped"); m["n_controls"] = 0
    t["mapped_with_zero_controls_rejected"] = v(sd, a)
    a = copy.deepcopy(disp); u = next(d for d in a if d["disposition"] != "mapped"); u["reason"] = None
    t["unmapped_without_reason_rejected"] = v(sd, a)
    return t


def write_report(S, rq, cc, E, disp, neg):
    L = []
    w = L.append
    w(f"GAP-M v{S['version']} QA report  (build {S['build_date']})")
    w("=" * 72)
    w("Automated tooling checks only. These do not replace the author's review, and mapping coverage")
    w("reported here does not demonstrate compliance or monitoring effectiveness.")
    w("\n1. SOURCE REGISTRIES")
    w(f"  AI RMF 1.0      categories {rq['rmf']['categories']} (expect 19), subcategories {rq['rmf']['subcategories']} (expect 72): {rq['rmf']['by_function']}")
    w(f"                  line-break hyphens resolved: {len(rq['rmf']['dehyphenation'])}; non-trivial decisions:")
    for d in rq["rmf"]["dehyphenation"]:
        if "default" in d or "kept" in d:
            w(f"                    {d}")
    w(f"  NIST AI 800-4   categories {rq['ai800_4']['categories']} (expect 6), category challenges {rq['ai800_4']['category_challenges']}, cross-cutting items {rq['ai800_4']['crosscutting_items']}")
    w(f"                  transcribed strings verified verbatim in PDF: {rq['ai800_4']['strings_checked'] - len(rq['ai800_4']['strings_missing'])}/{rq['ai800_4']['strings_checked']}")
    w(f"  HTI-1 (b)(11)   groups {rq['hti']['groups']}, attributes {rq['hti']['attributes']} (expect 31): {rq['hti']['by_group']}")
    w(f"                  eCFR text date {rq['hti']['ecfr_text_date']}; section last amended {rq['hti']['section_last_amended']}")
    w(f"  CISA CPG 2.0    goals {rq['cpg']['goals']} (expect 34): {rq['cpg']['by_function']}; empty fields: {rq['cpg']['null_fields'] or 'none'}")
    w(f"                  record SHA-256 {rq['cpg']['record_sha256'][:16]}… matches live-page capture: {rq['cpg']['matches_live_capture']}")
    w("\n2. CROSSWALK RULES")
    for r in cc["rules"]:
        w(f"  {r}")
    w(f"  violations: {len(cc['errors'])}")
    for k, v in cc.items():
        if k.startswith("schema_"):
            w(f"  {k:<22} {'valid' if not v else 'INVALID: ' + v[0]}")
    w("\n  Negative tests (corrupted inputs must be rejected):")
    for k, v in neg.items():
        w(f"    {k:<40} {'caught' if v else 'MISSED'}")
    w("\n3. COUNTS")
    w(f"  controls {S['n_controls']} in {S['n_families']} families {S['controls_by_family']}")
    w(f"  links {S['n_links']}; properties {S['property_counts']}")
    w(f"  links per control: min {S['links_per_control']['min']}, median {S['links_per_control']['median']}, max {S['links_per_control']['max']} ({S['links_per_control']['max_control']})")
    w(f"  controls per mapped element: min {S['controls_per_mapped_element']['min']}, median {S['controls_per_mapped_element']['median']}, max {S['controls_per_mapped_element']['max']} ({S['controls_per_mapped_element']['max_element']})")
    w(f"  controls linking all four frameworks: {S['controls_touching_all_four']}; three or more: {S['controls_touching_three_plus']}")
    w("\n4. COVERAGE (mappable elements)")
    w(f"  {'framework':<8}{'elements':>9}{'mapped':>8}{'%':>7}{'integral':>9}{'prereq':>8}{'out':>6}{'uncov':>7}{'links':>7}")
    for k, c in S["coverage"].items():
        w(f"  {k:<8}{c['elements']:>9}{c['mapped']:>8}{c['mapped_pct']:>7}{c['with_integral']:>9}{c['prerequisite']:>8}{c['out_of_scope']:>6}{c['uncovered']:>7}{c['links']:>7}")
    w(f"  total mapped {S['mapped_total']}/{S['n_elements_mappable']} ({S['mapped_total_pct']}%)")
    for name, key in [("AI RMF by function", "rmf_by_function"), ("CPG by function", "cpg_by_function"),
                      ("HTI by group", "hti_by_group"), ("AI 800-4 by category", "a84_by_category")]:
        w(f"  {name}: " + "; ".join(f"{g} {v['mapped']}/{v['elements']}" for g, v in S[key].items()))
    w("\n  Not mapped (with disposition):")
    for d in disp:
        if d["disposition"] != "mapped":
            w(f"    {d['element_id']:<18} {d['disposition']:<13} {d['reason']}")
    w(f"\n  Mapped only by example_of links ({S['n_weak_elements']}): " + ", ".join(S["weak_elements"]))
    w("\n5. HTI-1 ATTRIBUTES BY GAP-M CHANGE CLASS (analytic classification, not source text)")
    w(f"  {'class':<22}{'attrs':>6}{'integral':>9}{'precedes':>9}{'example only':>13}{'NA flag':>8}")
    for k, v in S["hti_by_class"].items():
        w(f"  {k:<22}{v['attributes']:>6}{v['with_integral']:>9}{v['with_precedes']:>9}{v['example_only']:>13}{v['na_flag']:>8}")
    w(f"  {'total':<22}{S['src']['hti_attributes']:>6}{S['hti_with_integral']:>9}{'':>9}{S['hti_example_only']:>13}{S['hti_na_flag']:>8}")
    w(f"  attributes with an integral link: {', '.join(S['hti_with_integral_ids']) or 'none'}")
    w("\n6. NECESSITY AUDIT (pre-review, AI-assisted; NOT the author's review)")
    a = S["audit"]
    w(f"  links audited {a['audited']} (originally integral_to {a['audited_integral']}, precedes {a['audited_precedes']})")
    w(f"  supported {a['supported']}, revised {a['revised']}, unresolved {a['unresolved']}")
    for t, v in a["by_source_type"].items():
        w(f"    {t:<36} supported {v['supported']:>3}  revised {v['revised']:>3}  unresolved {v['unresolved']:>3}")
    w("  unresolved (set to example_of until the author rules): " + ", ".join(a["unresolved_ids"]))
    w(f"  {S['author_review_scope_text']}")
    w(f"  release statement vs review record: {S['statement_check']['checked']} figures checked, "
      + ("all match" if not S['statement_check']['mismatched'] else "MISMATCH: " + " | ".join(S['statement_check']['mismatched'])))
    L_ = S["ledger"]
    w("\n6b. LINK LEDGER (original build -> current), by original relationship type")
    for p in ("integral_to", "precedes", "example_of"):
        w(f"  {p:<12} " + ", ".join(f"{k} {v}" for k, v in L_[p].items()))
    w(f"  total: original {L_['original_total']} - removed {L_['removed_total']} = current {L_['current_total']} {L_['current_by_property']}")
    w(f"  conditional (necessity unresolved, held at example_of; each reviewed and accepted as conditional by the author): {L_['conditional_links']}")
    er = S["example_review"]
    w("\n6c. TOOLING-ASSISTED EXAMPLE_OF REVIEW (AI assistant; not independent expert validation; not the author's review)")
    w(f"  reviewed {er['reviewed']}: kept {er['kept']}, rationale revised {er['revised']}, removed {er['removed']} (+{er['audited_removed']} audited link removed for consistency)")
    w(f"  all {er['removed'] + er['audited_removed']} removals by failed test: {er['removed_by_test']}  (T1 relevance, T2 source interpretation, T3 unsupported claim)")
    w("  elements left without links and given a disposition instead: " + ", ".join(er["newly_unmapped"]))
    w("\n7. NAMED SPOT CHECKS (compare each against the source page by hand)")
    for eid in SPOT:
        e = E[eid]
        d = next(x for x in disp if x["element_id"] == eid)
        w(f"  [{eid}] {e['locator']}")
        w(f"      text: {e['text']}")
        w(f"      GAP-M: {d['disposition']}; controls {d['controls'] or '-'}")
    open(os.path.join(ROOT, "data", "processed", "qa_report.txt"), "w", encoding="utf-8").write("\n".join(L) + "\n")


if __name__ == "__main__":
    main()
