#!/usr/bin/env python3
"""08_approval_package.py — concise approval package for the author (docs/APPROVAL_PACKAGE.md).

Numbers come from report/stats.json. This document asks for decisions; it records none.
"""
import json
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
S = J("report", "stats.json")
C, AU, LED, EXR = S["coverage"], S["audit"], S["ledger"], S["example_review"]
disp = {d["element_id"]: d for d in J("data", "crosswalk", "gapm_dispositions.json")}
uncovered = [d for d in disp.values() if d["disposition"] == "uncovered"]


def main():
    if rel.get("author_review") == "complete" and not rel.get("final"):
        open(os.path.join(ROOT, "docs", "APPROVAL_PACKAGE.md"), "w", encoding="utf-8").write(
            f"# GAP-M v{rel['version']}: approval package\n\nAnswered. The author completed her review on 2026-10-05 within the scope recorded in "
            "docs/AUTHOR_REVIEW.md. Her decisions are in docs/AUTHOR_DECISIONS.md and her release statement is in RELEASE.yaml (`ai_statement_final`). "
            "The pre-review approval package is not part of the release.\n")
        print("approval package: answered note written (release candidate)")
        return
    if rel.get("final"):
        open(os.path.join(ROOT, "docs", "APPROVAL_PACKAGE.md"), "w", encoding="utf-8").write(
            f"# GAP-M v{rel['version']}: approval package\n\nSuperseded on release ({rel['release_date']}). The pre-release approval package, "
            "prepared before the author's review, is not part of the release. The author's decisions are in docs/AUTHOR_DECISIONS.md, her review in docs/AUTHOR_REVIEW.md, and her statement in README.md.\n")
        print("approval package: superseded note written (final build)")
        return
    o = []
    w = o.append
    w(f"# GAP-M v{rel['version']}: approval package")
    w("")
    w(f"Status: DRAFT, prepared {rel['build_date']}. **Nothing has been published.** No repository, release, or DOI exists. "
      f"{S['author_review_scope_text']}")
    w("")
    w("## 1. What you would be approving")
    w("")
    w(f"- **{S['n_controls']} suggested monitoring practices** in {S['n_families']} families. They are original, have not been piloted, and are not endorsed by any agency.")
    w(f"- **{LED['current_total']} typed links** to four sources (NIST IR 8477 supportive relationships):")
    w(f"  - {S['property_counts']['integral_to']} `integral_to`")
    w(f"  - {S['property_counts']['precedes']} `precedes`")
    w(f"  - {S['property_counts']['example_of']} `example_of`, of which {LED['conditional_links']} are conditional")
    w(f"- **A disposition for every one of the {S['n_elements_mappable']} source elements**, each with a reason:")
    w(f"  - {S['mapped_total']} mapped ({S['mapped_total_pct']}%)")
    w(f"  - {S['n_uncovered']} uncovered (real gaps)")
    w("  - the rest prerequisite or out of scope")
    w("- **Formats:** JSON with schemas, CSV, an OSCAL 1.1.3 catalog, the reviewer workbook, and a draft technical report.")
    w("")
    w("| Source | Kind | Elements | Mapped | Necessary link | Uncovered | Prerequisite | Out of scope |")
    w("|---|---|---|---|---|---|---|---|")
    names = {"rmf": ("NIST AI RMF 1.0", "voluntary guidance"), "a84": ("NIST AI 800-4", "monitoring-challenges report"),
             "hti": ("45 CFR 170.315(b)(11)(iv)(B)", "disclosure requirement on certified health IT"), "cpg": ("CISA CPG 2.0", "voluntary practices")}
    for k, v in C.items():
        w(f"| {names[k][0]} | {names[k][1]} | {v['elements']} | {v['mapped']} ({v['mapped_pct']}%) | {v['with_integral']} | {v['uncovered']} | {v['prerequisite']} | {v['out_of_scope']} |")
    w("")
    w("Mapping coverage does not demonstrate compliance with any regulation, achievement of any framework outcome, or effective monitoring.")
    w("")
    w("## 2. What has been checked, and by whom")
    w("")
    w("| Check | Done by | Status | What it does not show |")
    w("|---|---|---|---|")
    w(f"| Automated checks: source counts, verbatim text, CPG hash, rules R1–R13, schemas, OSCAL, {S['negative_tests_passed']}/{S['negative_tests_total']} negative tests, clean rebuild | Build pipeline | Pass | That any mapping is right |")
    w(f"| Necessity audit of the {AU['audited']} links that claimed necessity | AI assistant | {AU['supported']} supported, {AU['revised']} revised, {AU['unresolved']} unresolved | Independent or author judgment |")
    w(f"| Relevance review of the {EXR['reviewed']} original `example_of` links | AI assistant, tooling-assisted | {EXR['kept']} kept, {EXR['revised']} reworded, {EXR['removed']} removed | Independent expert validation, or your review |")
    P_ = S["author_review_progress"]
    w(f"| Your guided review | You | In progress: {P_['controls_reviewed']} practices; {P_['links_reviewed']} links ({P_['census_integral_to']} required, {P_['census_conditional']} conditional, {P_['sample_size']} sampled); 4 source spot-checks | The {P_['links_current_unreviewed']} links outside your review set |")
    w("| Independent expert review, inter-rater agreement, pilot | Nobody | Not done | — |")
    w("")
    w("## 3. Link ledger")
    w("")
    w("| Original property | Original | Kept as is | To `example_of` | Conditional `example_of` | Removed (AI review) | Removed (author) |")
    w("|---|---|---|---|---|---|---|")
    for p in ("integral_to", "precedes"):
        v = LED[p]
        w(f"| `{p}` | {v['original']} | {v['still_' + p]} | {v['to_example_of_revised']} | {v['to_example_of_conditional_unresolved']} | {v['removed_by_example_review']} | {v['removed_by_author_review']} |")
    v = LED["example_of"]
    w(f"| `example_of` | {v['original']} | {v['kept'] + v['kept_rationale_revised']} ({v['kept_rationale_revised']} reworded) | — | — | {v['removed']} | {v['removed_by_author_review']} |")
    w(f"| **Total** | **{LED['original_total']}** | | | | **{LED['removed_by_example_review_total']}** | **{LED['removed_by_author_review_total']}** |")
    w("")
    w(f"Current total: {LED['original_total']} − {LED['removed_total']} = {LED['current_total']}.")
    w("")
    w("## 4. Decisions only you can make")
    w("")
    w("Your responses so far are recorded, as given, in docs/AUTHOR_DECISIONS.md. Recording a decision does not complete your review.")
    w("")
    w(f"1. **Conditional links.** Do you accept keeping the {LED['conditional_links']} unresolved necessity links as conditional `example_of` for v0.1.0? "
      "The list is in docs/MAPPING_REVIEW.md section 7.")
    w("   Their relevance as `example_of` mappings was assessed separately from necessity and is supported for "
      f"{S['pass2']['conditional_relevance_supported']} of {LED['conditional_links']}; only necessity is open. "
      "`GM-FAIR-02>HTI:B8.iv` joined this group in the second pass, because the regulation does not define fairness.")
    w("2. **Rules for each kind of source**, especially that no practice is ever *necessary* to an AI 800-4 challenge (section 1 of the review). "
      f"The second pass applied a stricter standard: a necessity claim is downgraded if a plausible alternative way of achieving the element exists. "
      f"It changed {len(S['pass2']['changed'])} links (review section 11): {sum(c['verdict'] == 'revised' for c in S['pass2']['changed'])} downgraded to `example_of`, "
      f"{sum(c['verdict'] == 'unresolved' for c in S['pass2']['changed'])} held as conditional. Accept that standard, or restore any of them with a reason.")
    w("   - **Outcome labels and (B)(8)(ii).** If you read \"validity\" as validity measured against local outcomes, `GM-FUN-04>HTI:B8.ii` can return to `precedes`. "
      "Label-free accuracy estimation exists (Garg et al., ICLR 2022) but assumes the outcome relationship has not shifted, so this link is held as conditional until you rule. "
      "`GM-FUN-04>HTI:B8.iv` stays `example_of` either way, because output-rate parity uses no labels.")
    w("   - **AI 800-4 scope.** AI 800-4 says it focuses on generative AI, with concepts relevant to other AI. Accept applying it to predictive systems on that basis.")
    w(f"3. **Removals.** Do you accept the {EXR['removed'] + EXR['audited_removed']} removals and the resulting drop in coverage (review section 5.1)? Restoring any of them means writing a rationale that passes the three tests.")
    w(f"4. **Uncovered gaps.** {', '.join(d['element_id'] for d in uncovered)}. Leave them as known gaps for v0.1.0, or plan controls for v0.2?")
    w("5. **Standing judgment calls:**")
    w("   - J1: how \"six monitoring-challenge categories\" is read.")
    w("   - J4: where fairness sits.")
    w("   - J5: the scope dispositions.")
    w("   - J6: the HTI attribute change classes, which are GAP-M's analytic classification, not the regulation's.")
    w("6. **Release description.** The original target sentence said the crosswalk maps the four sources \"onto one auditable monitoring control set\". A wording that matches what was built:")
    w("")
    w(f"   > GAP-M v{rel['version']}: a machine-readable crosswalk linking {S['n_controls']} suggested post-deployment monitoring practices to NIST AI RMF 1.0 subcategories, "
      f"the six monitoring categories and associated challenges of NIST AI 800-4, the {S['src']['hti_attributes']} predictive decision support intervention source attributes of "
      f"45 CFR 170.315(b)(11)(iv)(B), and CISA Cross-Sector CPG 2.0 goals, with {LED['current_total']} typed, rationale-bearing links and a recorded disposition for every source element. "
      "Mapping coverage does not demonstrate compliance or monitoring effectiveness.")
    w("")
    w("7. **Your release statement** (`ai_statement_final` in RELEASE.yaml). In your own words: what the AI assistant did, and what you reviewed and how. The build refuses a final release without it.")
    w("")
    w("## 5. Remaining limitations (the full list is in docs/LIMITATIONS.md)")
    w("")
    w(f"- Every link was drafted with AI assistance. You have individually reviewed {S['author_review_progress']['links_current_reviewed']} of the current links; the other {S['author_review_progress']['links_current_unreviewed']} have not been individually reviewed. There is no independent expert validation or inter-rater measure.")
    w(f"- {LED['conditional_links']} links are conditional (unresolved necessity; relevance supported).")
    w("- AI 800-4 focuses on generative AI; GAP-M applies it to predictive systems.")
    w("- For the 20 HTI attributes that may not be shown as not available, GM-HF-03 records a missing value as a gap to raise with the developer; GAP-M cannot make the developer fill it.")
    w("- The practices are not piloted; cadences and owner roles are illustrative.")
    w("- HTI-1 obligations sit with certified Health IT Modules and their developers, not deploying organizations. Only (b)(11)(iv)(B) is mapped, as of the eCFR text dated 2026-10-01.")
    w("- AI 800-4 describes challenges, not requirements. AI RMF and CPG 2.0 are voluntary.")
    w(f"- {S['n_uncovered']} relevant elements are uncovered by any GAP-M practice.")
    w("- The AI RMF Playbook and Generative AI Profile are not mapped; GAP-M is written for predictive systems.")
    w("- CPG 2.0 text comes from an archived page that matched the live page on 2026-10-05; CISA may revise it without versioning.")
    w("")
    w("## 6. If you approve")
    w("")
    w("Follow docs/VERIFY_CHECKLIST.md, then docs/PUBLISH_GUIDE.md:")
    w("1. Reserve a Zenodo DOI.")
    w("2. Set `release_date`, `doi`, `author_review: complete`, `ai_statement_final`, and `final: true` in RELEASE.yaml.")
    w("3. Rebuild with `bash run_all.sh`.")
    w("4. Pass `publish_gate.py`.")
    w("5. Push from your Mac and deposit on Zenodo yourself.")
    w("")
    w("Claude has not published anything and will not publish until you say so.")
    w("")
    w("## 7. Files to review")
    w("")
    w("- `data/crosswalk/GAP-M_crosswalk.xlsx`. Read these sheets first: Links (filter `conditional`, `example_review`), Audit, Removed, Ledger, Dispositions.")
    w("- `report/GAP-M_technical_report.pdf`: draft technical report.")
    w("- `docs/MAPPING_REVIEW.md`: every audited link with exact source text, the full relevance review, and the second correction pass (section 11).")
    w("- `data/processed/mapping_review.csv` and `data/processed/example_review.csv`: review decisions, with an `author_ruling` column on the audit file.")
    w("- `data/processed/qa_report.txt`: automated checks.")
    open(os.path.join(ROOT, "docs", "APPROVAL_PACKAGE.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
    print("approval package written")


if __name__ == "__main__":
    main()
