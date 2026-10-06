#!/usr/bin/env python3
"""09_author_review.py: the record of the author's guided review (docs/AUTHOR_REVIEW.md, data/processed/author_review.csv).

Built from mapping/author_review.yaml, which holds only the author's recorded responses. Items with no
response are reported as not individually reviewed. This builder writes no review content of its own.
"""
import csv
import json
import os

import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
AR = yaml.safe_load(open(os.path.join(ROOT, "mapping", "author_review.yaml"), encoding="utf-8"))
S = J("report", "stats.json")
P = S["author_review_progress"]
links = {l["link_id"]: l for l in J("data", "crosswalk", "gapm_links.json")}
controls = {c["control_id"]: c for c in J("data", "crosswalk", "gapm_controls.json")}
SCOPE = {**{x: "integral_to (all)" for x in AR["census"]["integral_to"]},
         **{x: "conditional (all)" for x in AR["census"]["conditional"]},
         **{x: "random sample" for x in AR["sampling"]["selected"]},
         **{x: "targeted check" for v in AR.get("targeted", {}).values() for x in v}}


def main():
    o = []
    w = o.append
    w("# Author review record: GAP-M v0.1.0")
    w("")
    rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml"), encoding="utf-8"))
    if rel.get("author_review") == "complete" and not rel.get("final"):
        w("Status: author review complete (2026-10-05) within the scope recorded below; release candidate, unpublished. This file records only the author's own responses, as given. "
          "Anything without a response is listed as not individually reviewed.")
    elif rel.get("final"):
        w(f"Status: released {rel['release_date']}. This file records only the author's own responses, as given. "
          "Anything without a response is listed as not individually reviewed.")
    else:
        w("Status: DRAFT. Guided author review in progress. This file records only the author's own responses, as given. "
          "Anything without a response is listed as not individually reviewed.")
    w("")
    w("## Scope so far")
    w("")
    w(S["author_review_scope_text"])
    w("")
    w("| Item | Reviewed by the author | Result |")
    w("|---|---|---|")
    w(f"| Practice definitions | {P['controls_reviewed']} of {P['controls_total']} | {P['controls_accepted_as_written']} accepted as written, {P['controls_accepted_with_edits']} accepted with edits |")
    w(f"| Links in the review set | {P['links_reviewed']} of {P['links_in_review_set']} | {P['links_accepted']} accepted, {P['links_revised']} accepted with reworded text, {P['links_removed']} removed |")
    w(f"| Current links not individually reviewed | {P['links_current_unreviewed']} of {P['links_current_reviewed'] + P['links_current_unreviewed']} | {P['consistency_edited_unreviewed']} of these received wording-only consistency edits the author approved |")
    w(f"| Source spot-checks | {len(P['spot_checks'])} of 4 sources | " + "; ".join(f"{k}: {v}" for k, v in P["spot_checks"].items()) + " |")
    w("")
    sm = AR["sampling"]
    w("## Sampling record")
    w("")
    w(f"- Population: the {sm['population_size']} `example_of` links that were not conditional at the time of the draw (SHA-256 of the sorted ID list: `{sm['population_sha256']}`).")
    w(f"- Sample: {sm['sample_size']} links ({int(sm['fraction'] * 100)}%, rounded {sm['rounding']}), seed **{sm['seed']}**. {sm['seed_note']}")
    w(f"- Method: {sm['method']}. {sm['python']}.")
    w(f"- Selected IDs (SHA-256 of the sorted list: `{sm['selected_sha256']}`): " + ", ".join(f"`{x}`" for x in sm["selected"]) + ".")
    w("")
    w("## Practice definitions")
    w("")
    w("| Practice | Response | Edit applied |")
    w("|---|---|---|")
    for cid, v in AR["controls"].items():
        w(f"| {cid} | {v['response']} | {v.get('edit_applied', '')} |")
    w("")
    w("## Links in the review set")
    w("")
    w("| Link | Review set | Response | Result | Edit applied |")
    w("|---|---|---|---|---|")
    for lid in AR["census"]["integral_to"] + AR["census"]["conditional"] + AR["sampling"]["selected"] + [x for v in AR.get("targeted", {}).values() for x in v]:
        v = AR["links"].get(lid)
        if v:
            w(f"| `{lid}` | {SCOPE[lid]} | {v['response']} | {v['status']} | {v.get('edit_applied', '')} |")
        else:
            w(f"| `{lid}` | {SCOPE[lid]} | (no response yet) | not reviewed | |")
    w("")
    if AR.get("earlier_review_changes"):
        w("## Changes made by the earlier AI-assisted review, ruled on by the author")
        w("")
        w("| Link | Change | Response | Note |")
        w("|---|---|---|---|")
        for k, v in AR["earlier_review_changes"].items():
            w(f"| `{k}` | {v['kind']} | {v['response']} | {v.get('edit_applied', '') or v.get('note', '')} |")
        w("")
    if AR.get("dispositions"):
        w("## Dispositions set by the author")
        w("")
        for k, v in AR["dispositions"].items():
            w(f"- {k}: {v['response']}. {v.get('note', '')}")
        w("")
    w("## Consistency edits (links still not individually reviewed)")
    w("")
    for e in AR.get("consistency_edits", []):
        w(f"- {e['edit']}. {e['authorized']} Links: " + ", ".join(f"`{x}`" for x in e["links"]) + ".")
    w("")
    w("## Source spot-checks")
    w("")
    for k, v in AR.get("spot_checks", {}).items():
        w(f"- **{k}** ({v['items']}): {v['response']} ({v['date']}).")
    w("")
    w("## Checklist items still open")
    w("")
    for c in AR.get("checklist_open", []):
        w(f"- [{'x' if c['status'] == 'done' else ' '}] {c['item']}" + (f" ({c['response']})" if c.get("response") else ""))
    w("")
    w("## Facts a release statement must stay within")
    w("")
    w("These are counts from this record, not a statement. The author writes `ai_statement_final` in her own words.")
    w("")
    w(f"- Practice definitions individually reviewed: {P['controls_reviewed']} of {P['controls_total']}.")
    w(f"- Links individually reviewed: all {P['census_integral_to']} integral_to, all {P['census_conditional']} conditional, {P['sample_size']} sampled `example_of` links (seed {P['sample_seed']}), and {P['targeted_checks']} links in targeted checks.")
    w(f"- Earlier AI-review changes ruled on: {P['earlier_removals_ruled']} removals and {P['earlier_rewordings_ruled']} rewordings.")
    w(f"- Links not individually reviewed: {P['links_current_unreviewed']} of the current {P['links_current_reviewed'] + P['links_current_unreviewed']}.")
    w("- Source spot-checks: as listed above; full source verification was done by the automated checks, not by the author.")
    w("- The necessity audit and the relevance review of all 210 original `example_of` links were AI-assisted; the author reviewed the subset above.")
    open(os.path.join(ROOT, "docs", "AUTHOR_REVIEW.md"), "w", encoding="utf-8").write("\n".join(o) + "\n")
    with open(os.path.join(ROOT, "data", "processed", "author_review.csv"), "w", newline="", encoding="utf-8") as f:
        cw = csv.writer(f)
        cw.writerow(["item_type", "item_id", "review_set", "author_response", "result", "edit_applied", "date"])
        for cid, v in AR["controls"].items():
            cw.writerow(["control", cid, "all", v["response"], "", v.get("edit_applied", ""), v["date"]])
        for lid in sorted(set(links) | set(AR["links"])):
            v = AR["links"].get(lid)
            cw.writerow(["link", lid, SCOPE.get(lid, "not sampled"), v["response"] if v else "not_reviewed",
                         v["status"] if v else "not_reviewed", (v or {}).get("edit_applied", ""), (v or {}).get("date", "")])
    outline(P)
    print(f"author review record written: {P['links_reviewed']} links and {P['controls_reviewed']} practices with author responses")


def outline(P):
    """Write an outline for ai_statement_final: fixed facts from the review record, blanks for the author's words."""
    rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml"), encoding="utf-8"))
    path = os.path.join(ROOT, "docs", "RELEASE_STATEMENT_OUTLINE.md")
    if rel.get("final") or rel.get("author_review") == "complete":
        if os.path.exists(path):
            try:
                os.remove(path)  # the outline is superseded by the author's own statement
            except OSError as e:
                print(f"warning: could not remove {path} ({e}); delete it by hand before release")
        return
    n_cur = P["links_current_reviewed"] + P["links_current_unreviewed"]
    o = []
    w = o.append
    w("# Release statement outline (for `ai_statement_final`)")
    w("")
    w("Status: DRAFT. An outline only. The author writes the statement in her own words; nothing here is her statement. "
      "The numbers below are generated from mapping/author_review.yaml and change if the review record changes.")
    w("")
    w("## 1. What the AI assistant did (facts to state)")
    w("")
    w("- Wrote the retrieval, parsing, validation, and document-building code.")
    w("- Drafted the 32 practice definitions, every link and rationale, the dispositions, and the document text.")
    w("- Carried out the necessity audit (two passes) and the relevance review of the 210 original `example_of` links, with tooling support.")
    w("- Ran the automated checks (source counts, verbatim text checks, schema and OSCAL validation, rebuild checks).")
    w("")
    w("## 2. What you reviewed, and how (facts, then your words)")
    w("")
    w(f"- Practice definitions: all {P['controls_reviewed']} ({P['controls_accepted_as_written']} accepted as written, {P['controls_accepted_with_edits']} with edits).")
    w(f"- Links reviewed individually: all {P['census_integral_to']} `integral_to`; all {P['census_conditional']} conditional; "
      f"a random sample of {P['sample_size']} of {P['sample_population']} other `example_of` links ({int(P['sample_fraction'] * 100)}%, seed {P['sample_seed']}); "
      f"{P['targeted_checks']} more in targeted checks. Results: {P['links_accepted']} accepted, {P['links_revised']} accepted with reworded text, {P['links_removed']} removed.")
    w(f"- Changes made by the AI-assisted review that you ruled on: {P['earlier_removals_ruled']} removals and {P['earlier_rewordings_ruled']} rewordings.")
    w("- Decisions recorded in docs/AUTHOR_DECISIONS.md (conditional links, necessity standard, removals and gaps, interpretive calls J1/J4/J5/J6, release description).")
    w("- Source spot-checks against the original documents: " + "; ".join(f"{k}: {v}" for k, v in P["spot_checks"].items()) + ".")
    w("- *Your words:* how you worked through the review (for example, guided batches with the source text shown beside each link), and what you changed.")
    w("")
    w("## 3. What you did not review (state plainly)")
    w("")
    w(f"- {P['links_current_unreviewed']} of the {n_cur} current links were not individually reviewed by you; they keep `review_status: proposed`.")
    w(f"- {P['consistency_edited_unreviewed']} of those received wording-only consistency edits you approved, without reviewing each link.")
    w("- Source text was verified in full by the automated checks; your own check was a spot-check of named items.")
    w("- No independent expert review, no inter-rater agreement, and no pilot in a deploying organization.")
    w("")
    w("## 4. What the statement must not say")
    w("")
    w("- That you reviewed every link, or that the crosswalk is validated, certified, endorsed, or demonstrates compliance.")
    w("- That the AI-assisted reviews were independent or expert validation.")
    w("")
    if str(rel.get("ai_statement_final") or "").strip():
        w("## Status")
        w("")
        w("A statement drafted from this outline was approved by the author and saved as `ai_statement_final` in RELEASE.yaml. "
          "The build checks its figures against the review record (QA report). `author_review` stays pending until the author confirms completion.")
        w("")
    w("## 5. Where it goes")
    w("")
    w("Write it as `ai_statement_final` in RELEASE.yaml, then set `author_review: complete` only when you confirm the review is complete. "
      "It replaces the draft AI-assistance paragraph in the README and report.")
    open(path, "w", encoding="utf-8").write("\n".join(o) + "\n")


if __name__ == "__main__":
    main()
