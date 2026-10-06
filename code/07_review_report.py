#!/usr/bin/env python3
"""07_review_report.py — mapping-review report from the necessity audit.

Writes docs/MAPPING_REVIEW.md and data/processed/mapping_review.csv. Source text is pulled from
data/registry/elements.json (verbatim, whitespace-normalized; AI RMF line-break hyphens resolved
per the QA report). Numbers come from report/stats.json. Nothing here is the author's review.
"""
import json
import os

import pandas as pd
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
S = J("report", "stats.json")
E = {e["element_id"]: e for e in J("data", "registry", "elements.json")}
links = {l["link_id"]: l for l in J("data", "crosswalk", "gapm_links.json")}
AR_LINKS = yaml.safe_load(open(os.path.join(ROOT, "mapping", "author_review.yaml"), encoding="utf-8"))["links"]
au = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))
CTRL = {c["control_id"]: c for c in J("data", "crosswalk", "gapm_controls.json")}
TYPE_NAME = {"guidance": "Guidance (AI RMF 1.0)", "monitoring_challenge": "Monitoring challenge (NIST AI 800-4)",
             "regulatory_disclosure_requirement": "Regulatory disclosure requirement (HTI-1)", "voluntary_practice": "Voluntary practice (CISA CPG 2.0)"}


def source_text(eid):
    e = E[eid]
    if eid.startswith("CPG:"):
        return (f"Outcome: {e['text']} | Scope: {e['cpg_scope']} | Recommended Action: {e['cpg_recommended_action']}")
    return e["text"]


def main():
    rows = []
    for a in au["links"]:
        lid = a["link"]
        c, t = lid.split(">")
        l = links.get(lid, {"property": "removed", "rationale": "(removed in the relevance review; see section 5)", "review_status": "removed"})
        rows.append({
            "link_id": lid, "control_id": c, "control_title": CTRL[c]["title"], "control_core": au["cores"][c],
            "target_id": t, "target_label": E[t]["label"], "source_type": E[t]["source_type"], "locator": E[t]["locator"],
            "source_text": source_text(t), "original_property": a["was"], "current_property": l["property"],
            "verdict": a["verdict"], "basis": a["basis"].strip(), "condition_for_necessity": a.get("condition"),
            "current_rationale": l["rationale"], "review_status": l["review_status"],
            "relevance_of_example_of": a.get("relevance"), "relevance_basis": a.get("relevance_basis"),
            "pass1_verdict": (a.get("pass1") or {}).get("verdict"), "pass1_property": (a.get("pass1") or {}).get("now"),
            "pass1_basis": (a.get("pass1") or {}).get("basis"),
            "author_ruling": (AR_LINKS.get(lid) or {}).get("response", ""),
        })
    df = pd.DataFrame(rows)
    os.makedirs(os.path.join(ROOT, "data", "processed"), exist_ok=True)
    df.to_csv(os.path.join(ROOT, "data", "processed", "mapping_review.csv"), index=False)

    AU = S["audit"]
    out = []
    w = out.append
    w(f"# GAP-M v{rel['version']}: mapping review (necessity audit and relevance review)")
    w("")
    if rel.get("final"):
        w(f"Status: audit record. Pre-review audit prepared {au['prepared']} with AI assistance; it is not the author's review. "
          "The author's review was completed before release, and her rulings are recorded in `data/processed/mapping_review.csv`.")
        w("")
    elif rel.get("author_review") == "complete":
        w(f"Status: audit record (release candidate; unpublished). Pre-review audit prepared {au['prepared']} with AI assistance; it is not the author's review. "
          f"{S['author_review_scope_text']} Where the author ruled on a link, her ruling is shown below and in `data/processed/mapping_review.csv`.")
        w("")
    else:
        w(f"Status: DRAFT. Pre-review audit prepared {au['prepared']} with AI assistance. **This is not the author's review.** "
          f"Nothing is published. {S['author_review_scope_text']} Where the author has ruled on a link below, her ruling is shown. "
      "The author rules on each item below; rulings go in the `author_ruling` column of `data/processed/mapping_review.csv` "
          "and are applied by editing `mapping/gapm_controls.yaml` and `mapping/link_audit.yaml`.")
        w("")
    w("## 1. What was audited and how")
    w("")
    w(f"Every link that claimed necessity was audited: {AU['audited']} links, of which {AU['audited_integral']} were `integral_to` and {AU['audited_precedes']} were `precedes`. "
      "The test comes from NIST IR 8477. `integral_to` holds only if the source element, read as written, cannot be achieved without the control's **core** activity. "
      "`precedes` holds only if the core must be achieved first. Each control's core is one sentence, listed in `mapping/link_audit.yaml`. "
      "Extras in a control's full text never count toward necessity.")
    w("")
    w("The four sources make different kinds of statements, so the test is applied with a rule for each kind:")
    w("")
    w("| Source kind | What it is | Rule applied |")
    w("|---|---|---|")
    w("| Guidance (AI RMF 1.0) | Voluntary risk-management outcomes | Necessity only where the subcategory's own words name the core activity or an object that cannot exist without it. |")
    w("| Monitoring challenge (NIST AI 800-4) | A report of practitioner challenges, gaps, and barriers; categories defined \"for example\" | Never necessary: a challenge has no completion condition in the source, so a practice can respond to it but cannot be required by it. |")
    w("| Regulatory disclosure requirement (45 CFR 170.315(b)(11)(iv)(B)) | Information a certified Health IT Module must support; obligation on the module and its developer | Necessary only where no party other than the deploying organization can produce the value. Even then, necessity is for a populated value, not for certification: (v)(A)(2) allows \"not available\" for 11 attributes. |")
    w("| Voluntary practice (CISA CPG 2.0) | Baseline practices with an outcome, a scope, and a recommended action | Necessary only where the recommended action, within the goal's stated scope, necessarily reaches the AI system. |")
    w("")
    w("Verdicts:")
    w("- **supported**: the necessity claim stands.")
    w("- **revised**: necessity is not supported. The property becomes `example_of`, and any rationale that implied necessity is reworded.")
    w("- **unresolved**: necessity depends on a fact or judgment only the author or a deploying organization can supply. The link is held at `example_of` until the author rules, and the condition under which it would be necessary is stated.")
    w("")
    w("## 2. Summary")
    w("")
    w("| | Supported | Revised | Unresolved | Total |")
    w("|---|---|---|---|---|")
    for p in ("integral_to", "precedes"):
        v = AU["by_original"][p]
        w(f"| Originally `{p}` | {v['supported']} | {v['revised']} | {v['unresolved']} | {sum(v.values())} |")
    w(f"| **All audited** | **{AU['supported']}** | **{AU['revised']}** | **{AU['unresolved']}** | **{AU['audited']}** |")
    w("")
    w("| Source kind | Supported | Revised | Unresolved |")
    w("|---|---|---|---|")
    for t, v in AU["by_source_type"].items():
        w(f"| {TYPE_NAME[t]} | {v['supported']} | {v['revised']} | {v['unresolved']} |")
    w("")
    w(f"After both reviews (necessity audit, then relevance review), the crosswalk has {S['property_counts']['integral_to']} `integral_to`, {S['property_counts']['precedes']} `precedes`, "
      f"and {S['property_counts']['example_of']} `example_of` links (total {S['n_links']}). The compiler now refuses:")
    w("- any `integral_to` or `precedes` link without a supported audit entry (rule R9);")
    w("- any audit entry that disagrees with the link (rule R10);")
    w("- any `example_of` rationale worded as necessity (rule R11).")
    w("")
    w("## 3. HTI-1 attribute counts, reconciled")
    w("")
    w(f"The earlier draft classed {S['hti_classes']['static_at_release']} attributes as `static_at_release`, but its text said \"13 attributes set at release are kept by periodic review only.\" "
      "The two counts measured different things. Three set-at-release attributes, (B)(2)(i) intended use, (B)(2)(ii) intended population, and (B)(3)(i) cautioned uses, carried "
      "`integral_to` links from GM-CMP-03 (out-of-scope use monitoring), so only 13 had example-only links. The audit downgraded those three links: use monitoring checks conformance to "
      "a description, but the description stays accurate whether or not use conforms.")
    w("")
    w("The change classes are now documented as **GAP-M's analytic classification**. The regulation does not sort attributes by how they change. Its only currency language, "
      "(v)(A)(1) \"complete and up-to-date\", applies to every attribute and is a duty of the Health IT Module. The word \"dynamic\" is retired. Current counts, which sum to 31:")
    w("")
    w("| GAP-M class | Attributes | With integral link | Example-only | May show not available |")
    w("|---|---|---|---|---|")
    for k, v in S["hti_by_class"].items():
        w(f"| `{k}` | {v['attributes']} | {v['with_integral']} | {v['example_only']} | {v['na_flag']} |")
    w(f"| **Total** | **{S['src']['hti_attributes']}** | **{S['hti_with_integral']}** | **{S['hti_example_only']}** | **{S['hti_na_flag']}** |")
    w("")
    w(f"The earlier claim that \"all 15 dynamic attributes have an integral control\" is withdrawn. It relied on GM-HF-03 (attribute register) being necessary. Under (v)(A)(1), "
      "the developer can keep non-local attributes current without the deploying organization, so the register is one route among others. Only the locally measured values "
      f"({', '.join(x.replace('HTI:', '') for x in S['hti_with_integral_ids'])}) keep necessity links.")
    w("")

    # ---------------- ledger
    LED = S["ledger"]
    w("## 4. Link ledger (every link of the original build)")
    w("")
    w("| Original property | Original | Kept as is | Changed to `example_of` | Conditional `example_of` (unresolved) | Removed (AI review) | Removed (author) |")
    w("|---|---|---|---|---|---|---|")
    for p_ in ("integral_to", "precedes"):
        v = LED[p_]
        w(f"| `{p_}` | {v['original']} | {v['still_' + p_]} | {v['to_example_of_revised']} | {v['to_example_of_conditional_unresolved']} | {v['removed_by_example_review']} | {v['removed_by_author_review']} |")
    v = LED["example_of"]
    w(f"| `example_of` | {v['original']} | {v['kept'] + v['kept_rationale_revised']} ({v['kept_rationale_revised']} with reworded rationale) | — | — | {v['removed']} | {v['removed_by_author_review']} |")
    w(f"| **Total** | **{LED['original_total']}** | | | | **{LED['removed_by_example_review_total']}** | **{LED['removed_by_author_review_total']}** |")
    w("")
    w(f"Current crosswalk: {LED['original_total']} − {LED['removed_total']} = **{LED['current_total']} links** "
      f"({S['property_counts']['integral_to']} `integral_to`, {S['property_counts']['precedes']} `precedes`, {S['property_counts']['example_of']} `example_of`, "
      f"of which {LED['conditional_links']} are conditional). The `integral_to` row's single removal is GM-GOV-07>CPG:2.C. The necessity audit had already downgraded it, "
      "and the relevance review then found it not substantive.")
    w("")
    # ---------------- relevance review
    ex = yaml.safe_load(open(os.path.join(ROOT, "mapping", "example_review.yaml"), encoding="utf-8"))
    EXR = S["example_review"]
    w("## 5. Relevance review of the original `example_of` links (tooling-assisted)")
    w("")
    w(f"Reviewer: {ex['reviewer']}. Each of the {EXR['reviewed']} links that were `example_of` from the start was read against the exact source text and the control's own text, using three tests:")
    w("- **T1 relevance:** does the control's stated activity bear on the element as written, not on a neighbouring topic?")
    w("- **T2 interpretation:** does the rationale describe the element's subject, phase (design-time or post-deployment), and scope accurately?")
    w("- **T3 support:** does the rationale claim anything the control's text does not say?")
    w("")
    w("A link was removed if it failed T1, or failed T2 or T3 in a way a rewording could not fix. Removals were not offset to preserve coverage; an element that lost its only link received a disposition instead.")
    w("")
    w(f"Result: {EXR['kept']} kept, {EXR['revised']} kept with a reworded rationale, {EXR['removed']} removed. "
      f"One further link from the audited set was removed for consistency. All {EXR['removed'] + EXR['audited_removed']} removals by failed test: "
      f"T1 {EXR['removed_by_test']['T1']}, T2 {EXR['removed_by_test']['T2']}, T3 {EXR['removed_by_test']['T3']}.")
    w("")
    w("### 5.1 Removed links")
    w("")
    for r in ex["remove"]:
        c, t = r["link"].split(">")
        w(f"- **`{r['link']}`** ({r['test']}{', audited set' if r.get('scope') == 'audited' else ''}). {CTRL[c]['title']} → {E[t]['label']} ({E[t]['locator']}). {r['basis']}")
    w("")
    w("### 5.2 Kept with a reworded rationale")
    w("")
    for r in ex["revise"]:
        w(f"- **`{r['link']}`** ({r['test']}). {r['basis']} New rationale: \"{r['rationale']}\"")
    w("")
    w("### 5.3 Kept")
    w("")
    w(f"{EXR['kept']} links passed all three tests unchanged and are listed in `mapping/example_review.yaml` (`keep`), and in the workbook's Links sheet "
      f"(`example_review = keep`). Default note: \"{ex['default_keep_note']}\" Links kept with a specific caveat:")
    w("")
    for k, v in ex["keep_notes"].items():
        w(f"- `{k}`: {v}")
    w("")
    w("### 5.4 Elements left without links")
    w("")
    disp = {d["element_id"]: d for d in J("data", "crosswalk", "gapm_dispositions.json")}
    for eid in EXR["newly_unmapped"]:
        d = disp[eid]
        w(f"- `{eid}` {d['label']}: **{d['disposition']}**. {d['reason'].replace('(2026-10-05 review) ', '')}")
    w("")
    pd.DataFrame(
        [{"link_id": r["link"], "decision": "remove", "test": r["test"], "basis": r["basis"], "new_rationale": None,
          "scope": r.get("scope", "example_of_review")} for r in ex["remove"]] +
        [{"link_id": r["link"], "decision": "revise", "test": r["test"], "basis": r["basis"], "new_rationale": r["rationale"],
          "scope": "example_of_review"} for r in ex["revise"]] +
        [{"link_id": k, "decision": "keep", "test": None, "basis": ex["keep_notes"].get(k, ex["default_keep_note"]), "new_rationale": None,
          "scope": "example_of_review"} for k in ex["keep"]]
    ).to_csv(os.path.join(ROOT, "data", "processed", "example_review.csv"), index=False)

    def entry(r):
        w(f"#### `{r['link_id']}`")
        if r["author_ruling"]:
            w(f"- **Author's ruling (guided review):** {r['author_ruling']}")
        w(f"- **Control:** {r['control_id']} {r['control_title']}. *Core:* {r['control_core']}")
        kind = {"guidance": "guidance", "monitoring_challenge": "monitoring challenge",
                "regulatory_disclosure_requirement": "disclosure requirement", "voluntary_practice": "voluntary practice"}[r["source_type"]]
        w(f"- **Source ({r['locator']}; {kind}):** \"{r['source_text']}\"")
        w(f"- **Property:** `{r['original_property']}` → `{r['current_property']}`")
        w(f"- **Basis:** {r['basis']}")
        if r["pass1_verdict"]:
            w(f"- **First pass:** {r['pass1_verdict']} (`{r['pass1_property']}`); changed in the second pass.")
        if r["verdict"] == "unresolved":
            w(f"- **Necessity: unresolved.** Condition for necessity: {r['condition_for_necessity']}")
            w(f"- **Relevance of the `example_of` mapping: {r['relevance_of_example_of']}.** {r['relevance_basis']}")
        elif r["condition_for_necessity"]:
            w(f"- **Condition for necessity:** {r['condition_for_necessity']}")
        if r["verdict"] != "supported":
            w(f"- **Current rationale:** {r['current_rationale']}")
        w(f"- **Author ruling:** ☐ agree ☐ change to ______  (review_status: {r['review_status']})")
        w("")

    for title, verdict, intro in [
        ("6. Necessity audit: supported links", "supported", "These necessity claims stood up in both passes against the narrowed control core and the exact source text. They still need the author's ruling."),
        ("7. Necessity audit: unresolved links, kept as conditional `example_of`", "unresolved",
         "For v0.1.0 these are kept as conditional `example_of` mappings and recorded as unresolved. The author reviewed each one and accepted it as a conditional mapping; its necessity stays open. "
         "Necessity and relevance are recorded separately. **Necessity** (whether the link should be `integral_to`) is unresolved for every link here, and each entry states the condition under which it would hold. "
         "**Relevance** (whether the weaker `example_of` mapping is substantively supported) was assessed on its own, against the exact source text. "
         f"It is supported for {S['pass2']['conditional_relevance_supported']} of {AU['unresolved']} and unsupported for {S['pass2']['conditional_relevance_unsupported']}, "
         "so no link here has unresolved relevance."),
        ("8. Necessity audit: revised links", "revised", "Necessity not supported; downgraded to `example_of` (one later removed; see section 5). Grouped by source kind."),
    ]:
        w(f"## {title}")
        w("")
        w(intro)
        w("")
        sub = [r for r in rows if r["verdict"] == verdict]
        if verdict == "revised":
            for t in TYPE_NAME:
                g = [r for r in sub if r["source_type"] == t]
                if g:
                    w(f"### {TYPE_NAME[t]} ({len(g)})")
                    w("")
                    for r in g:
                        entry(r)
        else:
            for r in sub:
                entry(r)

    w("## 9. Wording corrected")
    w("")
    w("- Release wording: the README, report, CITATION.cff, workbook, and OSCAL metadata now say the package is an unpublished draft with author review pending. The report no longer says it is \"released\" or \"archived\". The DOI reads \"not yet assigned\". Licensing is described as planned on release.")
    w("- AI assistance: the draft statement now says what the AI assistant did and that the author's review has not happened. The earlier sentence saying the author \"made and verified every judgment call, link, and number before release\" is removed. A final build is refused unless `author_review: complete` is set and the author has written her own `ai_statement_final` in `RELEASE.yaml`.")
    w("- Tooling versus review: the QA report, README, and report now separate automated checks (pipeline), the pre-review audit (AI-assisted), and the author's review (pending).")
    w("- Source kinds: every element now carries `source_type` and `obligation_holder`. Every link carries `target_source_type`, and every control is labeled `practice_type: suggested_practice`.")
    w("- Coverage: a coverage statement (mapping coverage does not show compliance, achievement of outcomes, or monitoring effectiveness) is in the bundle, README, report, workbook, OSCAL metadata, and QA report.")
    w("- HTI-1: the change classes are labeled analytic everywhere; `post_deployment_class` is renamed `gapm_change_class`; the counts are reconciled as above.")
    w("- Second pass (relevance review): a new disposition, `uncovered`, separates real gaps in GAP-M from scope decisions. Every link now carries `conditional`, `example_review`, and `example_review_note`. The compiler adds rule R12 (every link has an audit entry or a review decision) and rule R13 (removed links stay removed). Coverage figures fell, and the documents say so.")
    w("")
    w("## 10. What the author decides")
    w("")
    w(f"- [ ] Accept keeping the {AU['unresolved']} unresolved links as conditional `example_of` for v0.1.0 (section 7), or rule on any of them individually. "
      "Their relevance has been assessed separately and is supported; only their necessity is open.")
    w("- [ ] Decide whether \"validity\" in (B)(8)(ii) means validity measured against local outcomes. If it does, `GM-FUN-04>HTI:B8.ii` can return to `precedes`; "
      "if label-free estimates under a no-shift assumption also count, it becomes `example_of` (revised). Until then it is a conditional link (section 7). "
      "Fairness in (B)(8)(iv) stays example_of either way, because output-rate parity uses no labels.")
    w(f"- [ ] Confirm or overturn each of the {AU['supported']} supported necessity links (section 6).")
    w("- [ ] Spot-check the revised links (section 8); at minimum, every revised link to guidance and to voluntary practices.")
    w(f"- [ ] Spot-check the relevance review (section 5): every removal, and a sample of the {EXR['kept']} kept links (record the sampling seed).")
    w(f"- [ ] Accept or change the dispositions of the {len(EXR['newly_unmapped'])} elements left without links (section 5.4).")
    w("- [ ] Accept or change the source-kind rules in section 1, especially the rule that no practice is necessary to an AI 800-4 challenge.")
    w("- [ ] Accept or change the GAP-M change classes (J6), now documented as analytic.")
    w("- [ ] Only then set `review_status: accepted` on what you accept, and `author_review: complete` in `RELEASE.yaml`.")
    # ---------------- second correction pass
    P2 = S["pass2"]
    a_all = yaml.safe_load(open(os.path.join(ROOT, "mapping", "link_audit.yaml"), encoding="utf-8"))
    w("")
    w("## 11. Second correction pass (2026-10-05)")
    w("")
    w(f"Prepared by the AI assistant with tooling support at the author's request. It is not independent expert validation and not the author's review. "
      f"All {P2['rechecked']} links still asserting necessity after the first pass were rechecked against a narrowed control core and the exact source text. "
      "Conditions that appeared only in rationales, such as a register format, an approval step, or pre-set triggers, were removed. "
      "Any claim that could not withstand a plausible alternative way of achieving the source element was downgraded.")
    w("")
    w("### 11.1 Property changes")
    w("")
    w("| Link | First pass | Now | Reason |")
    w("|---|---|---|---|")
    A_ = {e["link"]: e for e in a_all["links"]}
    for c in P2["changed"]:
        reason = A_[c["link_id"]]["basis"].replace("Second pass: ", "").replace("|", "/")
        reason = reason[:1].upper() + reason[1:]
        w(f"| `{c['link_id']}` | `{c['pass1_property']}` ({c['pass1_verdict']}) | `{c['property']}` ({c['verdict']}) | {reason} |")
    w("")
    w("### 11.2 Necessity kept, rationale corrected")
    w("")
    for n in S["necessity_links"]:
        w(f"- `{n['link_id']}` (`{n['property']}`): {links[n['link_id']]['rationale']}")
    w("")
    w("### 11.3 Control cores narrowed to the part a source can require")
    w("")
    for c, old in a_all["second_pass"]["cores_previous"].items():
        w(f"- **{c}.** Was: \"{old}\" Now: \"{a_all['cores'][c]}\"")
    w("")
    w("### 11.4 Other corrections")
    w("")
    w("- **GM-HF-03:** now separates the 11 attributes that 170.315(b)(11)(v)(A)(2) allows to be shown as not available from the other 20. For those 20, (v)(A)(1) expects complete and up-to-date descriptions, and a missing value is recorded as a gap to resolve with the developer, not marked not available.")
    w("- **Report claim:** \"none of these documents refers to the others at element level\" is narrowed to the texts actually reviewed. None of the four cites another there. The AI RMF refers to the NIST Cybersecurity Framework (not one of the four), and AI 800-4 cites NIST AI 100-2. The HTI-1 preamble was not reviewed.")
    w("- **AI 800-4 scope:** the report states it \"is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning\" (p. 4, note 4). This is now stated in the README, the report, and LIMITATIONS.")
    w("- **Label-free validity, substantiated (2026-10-05, at the author's request):** the earlier statement that label-free performance estimation is \"a plausible, if weaker\" alternative "
      "was checked against a primary source. Garg et al., *Leveraging Unlabeled Data to Predict Out-of-Distribution Performance* (ICLR 2022, arXiv:2201.04234), propose Average Thresholded Confidence, "
      "which estimates accuracy from unlabeled target data. The same paper shows target accuracy is identifiable only under assumptions on the shift, such as covariate shift with p(y|x) unchanged. "
      "Because an unchanged outcome relationship is part of what local validation tests, the source does not establish that a label-free estimate satisfies (B)(8)(ii). "
      "The explanation was narrowed, and `GM-FUN-04>HTI:B8.ii` moved from revised to unresolved (conditional `example_of`); its property did not change.")
    w("- **Report Table 4** now shows the `precedes` total, and its column headers no longer wrap mid-word.")
    open(os.path.join(ROOT, "docs", "MAPPING_REVIEW.md"), "w", encoding="utf-8").write("\n".join(out) + "\n")
    print(f"mapping review written: {len(rows)} audited links; {EXR['reviewed']} example_of links reviewed")


if __name__ == "__main__":
    main()
