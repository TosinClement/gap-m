#!/usr/bin/env python3
"""06_documents.py — build README.md, CITATION.cff and the technical report PDF.

Every number is read from report/stats.json (written by 04_qa.py). Nothing numeric is typed
into prose. While RELEASE.yaml has final: false, every document says it is an unpublished draft
with author review pending. A final build is refused unless author_review is 'complete' and the
author has written ai_statement_final in RELEASE.yaml in her own words.
"""
import json
import os
import sys

import yaml
from reportlab.lib import colors
from reportlab import rl_config

rl_config.invariant = 1  # fixed PDF ID and timestamps, so rebuilds are byte-identical
from reportlab.lib.enums import TA_CENTER
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Image, KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
S = J("report", "stats.json")
A = J("AUTHORS.json")["authors"][0]
controls = J("data", "crosswalk", "gapm_controls.json")
bundle = J("data", "crosswalk", "gapm_crosswalk.json")
FINAL = bool(rel.get("final"))
if FINAL and (rel.get("author_review") != "complete" or not str(rel.get("ai_statement_final", "")).strip()):
    sys.exit("Refusing a final build: set author_review: complete and write ai_statement_final in RELEASE.yaml first.")
REVIEWED = rel.get("author_review") == "complete" and bool(str(rel.get("ai_statement_final", "")).strip())
RC = REVIEWED and not FINAL  # release candidate: author review complete, not yet released (no DOI)
_UNREV = S["author_review_progress"]["links_current_unreviewed"]
STATUS = (f"Released {rel['release_date']}" if FINAL else
          (f"Release candidate, unpublished; author review complete within the scope in docs/AUTHOR_REVIEW.md ({_UNREV} links not individually reviewed remain proposed); not for citation until released" if RC else
           "DRAFT, unpublished; author review in progress (see docs/AUTHOR_REVIEW.md); unreviewed links are proposed; not for citation"))
DOI_TXT = rel["doi"] if FINAL else "not yet assigned"
C = S["coverage"]
AU = S["audit"]
SRC_ROWS = [
    ("NIST AI RMF 1.0 (NIST AI 100-1)", "Voluntary guidance: risk-management outcomes", "No one (voluntary)",
     f"{S['src']['rmf_subcategories']} subcategories"),
    ("NIST AI 800-4", "Report on monitoring challenges: categories, gaps, barriers", "No one (describes challenges; sets no requirements)",
     f"{S['src']['a84_categories']} categories; {S['src']['a84_category_challenges']} category and {S['src']['a84_crosscutting_items']} cross-cutting gaps/barriers"),
    ("45 CFR 170.315(b)(11)(iv)(B) (ONC HTI-1)", "Regulatory disclosure requirement for certified health IT",
     "The certified Health IT Module and its developer, not deploying organizations", f"{S['src']['hti_attributes']} source attributes"),
    ("CISA CPG 2.0", "Voluntary practices with recommended actions", "No one (voluntary)", f"{S['src']['cpg_goals']} goals"),
    ("GAP-M controls (this work)", "Suggested implementation practices", "No one; not endorsed by any agency", f"{S['n_controls']} controls"),
]
COVERAGE_CAVEAT = bundle["coverage_statement"]
LED = S["ledger"]
EXR = S["example_review"]


def necessity_list():
    by = {}
    for n in S["necessity_links"]:
        by.setdefault(n["target_framework"], []).append(f"{n['target_code']} ({n['control_id']})")
    order = ["AI RMF 1.0", "CISA CPG 2.0", "ONC HTI-1 (b)(11)", "NIST AI 800-4"]
    short = {"AI RMF 1.0": "AI RMF", "CISA CPG 2.0": "CPG 2.0", "ONC HTI-1 (b)(11)": "HTI-1", "NIST AI 800-4": "AI 800-4"}
    return "; ".join(f"{short[k]}: {', '.join(by[k])}" for k in order if k in by)


def notmapped(v):
    parts = [f"{v[k]} {lab}" for k, lab in (("uncovered", "uncovered"), ("prerequisite", "prerequisite"), ("out_of_scope", "out of scope")) if v[k]]
    return ", ".join(parts) or "0"


CLS_LABEL = {"static_at_release": "set at release", "process_description": "process description",
             "evidence_accruing": "new evidence possible", "locally_measured": "measured locally"}


def readme():
    srcrows = "\n".join(f"| {a} | {b} | {c} | {d} |" for a, b, c, d in SRC_ROWS)
    clsrows = "\n".join(f"| {CLS_LABEL[k]} (`{k}`) | {v['attributes']} | {v['with_integral']} | {v['example_only']} | {v['na_flag']} |"
                        for k, v in S["hti_by_class"].items())
    if FINAL or RC:
        verification = ("Author review completed before release. " if FINAL else "Author review complete; release pending. ") + "The author's statement:\n\n" + str(rel["ai_statement_final"]).strip()
        cite = (f"{A['family']}, {A['given'][0]}. ({rel['release_date']}). *{rel['title']}* (Version {rel['version']}) [Data set]. Zenodo. {rel['doi']}" if FINAL
                else "Release candidate; please do not cite until release. A citation and DOI will be added on release.")
    else:
        verification = ("**Automated checks (done by the build pipeline):** source counts, verbatim checks of transcribed text, "
                        "crosswalk rules R1–R13, JSON Schema and OSCAL validation, and negative tests. Results are in "
                        "`data/processed/qa_report.txt`. These are tooling checks; they are not review.\n\n"
                        "**Necessity audit (pre-review, AI-assisted):** every link that claimed a control was necessary was tested "
                        "against the exact source text. Results are in [docs/MAPPING_REVIEW.md](docs/MAPPING_REVIEW.md). This is input "
                        "to the author's review, not a substitute for it.\n\n"
                        "**Example_of review (tooling-assisted, by the AI assistant):** every link that was `example_of` from the start was checked for "
                        "relevance, source interpretation, and unsupported claims, and weak links were removed. This is not independent expert validation "
                        "and not the author's review.\n\n"
                        f"**Conditional links:** {LED['conditional_links']} links whose necessity is unresolved are kept as conditional `example_of` mappings. "
                        "Their necessity is unresolved and is recorded as such; the author reviewed each one and accepted it as a conditional mapping.\n\n"
                        f"**{S['author_review_scope_text']}** Links the author has not reviewed keep `review_status: proposed`; "
                        "the README, limitations, and report text have not yet been revised by the author.")
        cite = "Unpublished draft; please do not cite. A citation and DOI will be added on release."
    t = f"""# {rel['title']}

**Status:** {STATUS} · version {rel['version']} · DOI: {DOI_TXT}

GAP-M is a machine-readable crosswalk. It links one set of suggested post-deployment monitoring practices for predictive AI systems to four U.S. federal sources. **The four sources are different kinds of documents, and the crosswalk keeps them distinct:**

| Source | What kind of statement | Who it obligates | Elements |
|---|---|---|---|
{srcrows}

GAP-M has **{S['n_controls']} controls** in {S['n_families']} families. They are joined to the sources by **{S['n_links']} links**, each using NIST IR 8477's supportive-relationship vocabulary (`supports`, with property `integral_to`, `example_of`, or `precedes`) and a one-sentence rationale. Every mappable source element has a recorded disposition, each with a reason: mapped, uncovered (relevant but not supported by any GAP-M control), prerequisite baseline, or out of monitoring scope.

## What the coverage numbers mean, and what they do not

{COVERAGE_CAVEAT}

| Source | Elements | Mapped | With a link judged necessary (integral_to) | Not mapped |
|---|---|---|---|---|
| AI RMF 1.0 subcategories | {C['rmf']['elements']} | {C['rmf']['mapped']} ({C['rmf']['mapped_pct']}%) | {C['rmf']['with_integral']} | {notmapped(C['rmf'])} |
| NIST AI 800-4 categories and challenges | {C['a84']['elements']} | {C['a84']['mapped']} ({C['a84']['mapped_pct']}%) | {C['a84']['with_integral']} | {notmapped(C['a84'])} |
| HTI-1 predictive-DSI source attributes | {C['hti']['elements']} | {C['hti']['mapped']} ({C['hti']['mapped_pct']}%) | {C['hti']['with_integral']} | {notmapped(C['hti'])} |
| CISA CPG 2.0 goals | {C['cpg']['elements']} | {C['cpg']['mapped']} ({C['cpg']['mapped_pct']}%) | {C['cpg']['with_integral']} | {notmapped(C['cpg'])} |
| **Total** | **{S['n_elements_mappable']}** | **{S['mapped_total']} ({S['mapped_total_pct']}%)** | | **{S['n_elements_mappable'] - S['mapped_total']}** |

Coverage fell during review because weak links were removed rather than kept for coverage's sake.

For AI 800-4, "mapped" means a control is one response to a reported challenge. It does not mean the challenge is solved. For HTI-1, the disclosure obligation sits with the certified Health IT Module. GAP-M links describe how a deploying organization's monitoring can supply or check attribute content. They are not a compliance pathway.

## Link review and ledger

Every link in the original build has been through one of two reviews, both prepared by the AI assistant: a necessity audit for links that claimed a practice was necessary, and a relevance review for links that were `example_of` from the start. Neither is independent expert validation or the author's review. The author's own review of a subset, and her rulings on these reviews' removals and rewordings, are recorded in docs/AUTHOR_REVIEW.md.

| Original property | Original links | Kept as is | Changed to `example_of` | Conditional `example_of` (unresolved) | Removed (AI review) | Removed (author) |
|---|---|---|---|---|---|---|
| `integral_to` | {LED['integral_to']['original']} | {LED['integral_to']['still_integral_to']} | {LED['integral_to']['to_example_of_revised']} | {LED['integral_to']['to_example_of_conditional_unresolved']} | {LED['integral_to']['removed_by_example_review']} | {LED['integral_to']['removed_by_author_review']} |
| `precedes` | {LED['precedes']['original']} | {LED['precedes']['still_precedes']} | {LED['precedes']['to_example_of_revised']} | {LED['precedes']['to_example_of_conditional_unresolved']} | {LED['precedes']['removed_by_example_review']} | {LED['precedes']['removed_by_author_review']} |
| `example_of` | {LED['example_of']['original']} | {LED['example_of']['kept'] + LED['example_of']['kept_rationale_revised']} (rationale reworded for {LED['example_of']['kept_rationale_revised']}) | — | — | {LED['example_of']['removed']} | {LED['example_of']['removed_by_author_review']} |
| **Total** | **{LED['original_total']}** | | | | **{LED['removed_by_example_review_total']}** | **{LED['removed_by_author_review_total']}** |

The current crosswalk has **{LED['current_total']} links**: {S['property_counts']['integral_to']} `integral_to`, {S['property_counts']['precedes']} `precedes`, and {S['property_counts']['example_of']} `example_of`. Of the `example_of` links, {LED['conditional_links']} are conditional. Their necessity is unresolved and recorded as such; the author reviewed each one and accepted it as a conditional mapping.

### Necessity audit

All {AU['audited']} links that originally claimed necessity ({AU['audited_integral']} `integral_to`, {AU['audited_precedes']} `precedes`) were tested against the exact source text: could the source element, as written, be achieved without the control's core activity? Results:
- {AU['supported']} supported
- {AU['revised']} downgraded to `example_of`
- {AU['unresolved']} unresolved, kept as conditional `example_of` mappings for v0.1.0

No necessity claim to an AI 800-4 element survived. The report describes challenges and sets no completion condition, so necessity cannot be read from its text.

### Relevance review of the original `example_of` links

Each of the {EXR['reviewed']} links was tested for three things against the exact source text and the control's own text:
- relevance: does the control's activity bear on the element as written?
- source interpretation: is the element's subject, phase, and scope read correctly?
- unsupported claims: does the rationale claim anything the control does not say?

Results:
- {EXR['kept']} kept
- {EXR['revised']} kept with a reworded rationale
- {EXR['removed']} removed

One further link from the audited set was removed for consistency. {len(EXR['newly_unmapped'])} elements lost their only links and now carry a disposition instead.

Details are in [docs/MAPPING_REVIEW.md](docs/MAPPING_REVIEW.md).

## HTI-1 attributes and GAP-M's change classes

GAP-M sorts the {S['src']['hti_attributes']} attributes into four **analytic** classes by what most often changes their value after deployment. The regulation draws no such distinction. Its only currency language, 170.315(b)(11)(v)(A)(1), requires "complete and up-to-date" descriptions of *every* attribute, and places that duty on the Health IT Module.

| GAP-M class | Attributes | With an integral link | Example-only links | Must show "not available" when missing |
|---|---|---|---|---|
{clsrows}
| **Total** | **{S['src']['hti_attributes']}** | **{S['hti_with_integral']}** | **{S['hti_example_only']}** | **{S['hti_na_flag']}** |

Only {', '.join(x.replace('HTI:', '') for x in S['hti_with_integral_ids'])} (validity of the intervention in local data) keeps a link judged necessary: measuring validity in the deploying organization's own data. That necessity holds only for a populated value, since 170.315(b)(11)(v)(A)(2) lets the module show this attribute as not available. Two related points:
- **(B)(8)(iv), local fairness:** the necessity link is now conditional, because the regulation does not define fairness.
- **Outcome labels:** these are not treated as a prerequisite for local fairness, because fairness measures such as output-rate parity use no labels. Whether labels are a prerequisite for local validity is unresolved. Label-free accuracy estimation exists (Garg et al., ICLR 2022), but it rests on the assumption that the outcome relationship has not shifted, which local validation is meant to test.

The not-available allowance applies only to the {S['hti_na_flag']} attributes listed in (v)(A)(2). For the other {S['src']['hti_attributes'] - S['hti_na_flag']}, (v)(A)(1) expects complete and up-to-date descriptions, so GAP-M records a missing value as a gap to resolve with the developer.

## Verification status

{verification}

## What's in the repository

| Path | What it is |
|---|---|
| `data/crosswalk/gapm_crosswalk.json` | Everything in one file (controls, links with audit fields, dispositions, HTI attribute table, source types, sources) |
| `data/crosswalk/gapm_controls.csv` · `gapm_links.csv` · `gapm_dispositions.csv` · `gapm_hti_attributes.csv` | The same content as flat tables |
| `data/crosswalk/gapm_catalog_oscal.json` | The control set as an OSCAL 1.1.3 catalog; links are `supports` props |
| `data/crosswalk/GAP-M_crosswalk.xlsx` | Reviewer workbook (includes Audit and SourceTypes sheets) |
| `data/registry/elements.csv` | Verbatim source text for all four sources, with source type and locators |
| `mapping/` | Human-edited inputs: controls and links, dispositions, necessity audit, example_of review, AI 800-4 table text, HTI change classes |
| `docs/APPROVAL_PACKAGE.md` | What the author is being asked to approve, the open decisions, and the remaining limitations |
| `docs/AUTHOR_DECISIONS.md` | The author's responses to the open decisions, recorded as given |
| `docs/AUTHOR_REVIEW.md` | The author's guided review: what she individually reviewed, her responses, the sampling seed, spot-checks, and open checklist items |
| `docs/RELEASE_STATEMENT_OUTLINE.md` | Pre-release only: an outline of facts the author's release statement must stay within (removed on release) |
| `docs/MAPPING_REVIEW.md` · `data/processed/mapping_review.csv` | Necessity-audit report: supported, revised, and unresolved links, with exact source text |
| `data/processed/qa_report.txt` | Automated QA report |
| `report/` | Technical report (PDF), figures, `stats.json` |
| `docs/` | Build spec, codebook, mapping use case (IR 8477 §3), limitations, verification checklist, next steps, publish guide |

## Reproduce

```bash
pip install -r requirements.txt
bash run_all.sh            # rebuild from the committed source files in data/raw/
bash run_all.sh --fetch    # or re-download the sources first (see data/raw/PROVENANCE.txt)
```

The build fails if any of these happen:
- a source count changes
- a transcribed string is not found verbatim
- the CPG record hash changes
- any crosswalk rule or schema check fails, including the rules that every necessity claim has a supported audit entry and that no `example_of` rationale asserts necessity

**Reproducibility, as checked on 2026-10-05.** Two different claims are made, and only these two:
- **Same environment, byte-identical.** A clean rebuild in the build environment (Linux, Python 3.13, matplotlib 3.11) reproduced every generated file byte for byte (all files compared by SHA-256). The workbook and PDF carry fixed timestamps for this purpose.
- **Across environments, matching data and text.** A rebuild on macOS (Python 3.10, matplotlib 3.10) reproduced every data file, schema, JSON, CSV, and Markdown document byte for byte. The workbook matched cell for cell, and the PDF matched in extracted text. The workbook, PDF, and PNG figures differ in bytes, because rendering and compression libraries differ between the environments.

Byte identity is not claimed across environments.

Edit `mapping/*.yaml`, never the generated files.

## Sources

| ID | Source | Vintage |
|---|---|---|
| S1 | NIST AI 100-1, AI RMF 1.0. doi:10.6028/NIST.AI.100-1 | January 2023 |
| S2 | NIST AI 800-4, Challenges to the Monitoring of Deployed AI Systems. doi:10.6028/NIST.AI.800-4 | March 2026 |
| S3 | 45 CFR 170.315(b)(11) (ONC HTI-1 Final Rule, 89 FR 1192), eCFR point-in-time text | 2026-10-01 (section last amended {S['hti_section_last_amended']}) |
| S4 | CISA Cybersecurity Performance Goals 2.0 | released 2025-12-10; captured 2026-10-05 |

Mapping vocabulary: NIST IR 8477 (2024), doi:10.6028/NIST.IR.8477.

NIST AI 800-4 states that it "is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning" (p. 4, note 4). GAP-M applies its categories and challenges to predictive systems on that basis.

GAP-M is independent work. It is not a NIST, ONC/ASTP, or CISA product and has not been reviewed or endorsed by them.

## License

On release: code under MIT; data, crosswalk, schemas, figures, and documents under CC BY 4.0. Quoted source text is U.S. Government work, not subject to copyright in the United States (17 U.S.C. 105); NIST grants a worldwide license for its publications and requests the credit line "Republished courtesy of the National Institute of Standards and Technology." See [LICENSE](LICENSE).

## Citation

{cite}

## Maintainer

{A['name']} · {A['affiliation']} · ORCID [{A['orcid']}](https://orcid.org/{A['orcid']}) · {A['email']}
"""
    open(os.path.join(ROOT, "README.md"), "w", encoding="utf-8").write(t)


def citation():
    lines = [
        "cff-version: 1.2.0",
        f'message: "{"If you use GAP-M, please cite it as below." if FINAL else ("Release candidate; please do not cite until release." if RC else "Unpublished draft; please do not cite until release.")}"',
        "type: dataset",
        f'title: "{rel["title"]}"',
        f'version: "{rel["version"]}"',
    ]
    if FINAL:
        lines += [f'date-released: "{rel["release_date"]}"', f'doi: "{rel["doi"]}"']
    lines += [
        "license: CC-BY-4.0",
        f'repository-code: "{rel["repository"]}"',
        "abstract: >-",
        f"  A machine-readable crosswalk linking {S['n_controls']} suggested post-deployment monitoring practices to",
        "  NIST AI RMF 1.0 subcategories (voluntary guidance), the monitoring categories and challenges of",
        f"  NIST AI 800-4 (a challenges report), the {S['src']['hti_attributes']} predictive decision support intervention source",
        "  attributes of 45 CFR 170.315(b)(11)(iv)(B) (a disclosure requirement for certified health IT), and CISA",
        f"  Cybersecurity Performance Goals 2.0 (voluntary practices), with {S['n_links']} links typed using NIST IR 8477",
        "  supportive relationships. Mapping coverage does not demonstrate compliance or monitoring effectiveness.",
        "keywords:",
    ] + [f"  - {k}" for k in ["AI governance", "post-deployment monitoring", "NIST AI RMF", "NIST AI 800-4", "HTI-1",
                             "decision support interventions", "CISA CPG", "crosswalk", "OSCAL"]] + [
        "authors:",
        f'  - family-names: "{A["family"]}"',
        f'    given-names: "{A["given"]}"',
        f'    orcid: "https://orcid.org/{A["orcid"]}"',
        f'    email: "{A["email"]}"',
        f'    affiliation: "{A["affiliation"]}"',
    ]
    open(os.path.join(ROOT, "CITATION.cff"), "w", encoding="utf-8").write("\n".join(lines) + "\n")


# ------------------------------------------------------------------ technical report
def report():
    for n, f in [("Serif", "DejaVuSerif"), ("Serif-B", "DejaVuSerif-Bold"), ("Sans", "DejaVuSans"), ("Sans-B", "DejaVuSans-Bold")]:
        pdfmetrics.registerFont(TTFont(n, f"/usr/share/fonts/truetype/dejavu/{f}.ttf"))
    from reportlab.pdfbase.pdfmetrics import registerFontFamily
    registerFontFamily("Serif", normal="Serif", bold="Serif-B", italic="Serif", boldItalic="Serif-B")
    registerFontFamily("Sans", normal="Sans", bold="Sans-B", italic="Sans", boldItalic="Sans-B")
    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["Normal"], fontName="Serif", fontSize=9.6, leading=13.4, spaceAfter=6)
    small = ParagraphStyle("s", parent=body, fontSize=8, leading=10.5)
    h1 = ParagraphStyle("h1", parent=body, fontName="Sans-B", fontSize=12, leading=15, spaceBefore=10, spaceAfter=5, keepWithNext=1)
    h2 = ParagraphStyle("h2", parent=body, fontName="Sans-B", fontSize=10, leading=13, spaceBefore=6, spaceAfter=3, keepWithNext=1)
    title = ParagraphStyle("t", parent=body, fontName="Sans-B", fontSize=16, leading=20, alignment=TA_CENTER)
    sub = ParagraphStyle("st", parent=body, fontName="Sans", fontSize=10.5, leading=14, alignment=TA_CENTER)
    cap = ParagraphStyle("c", parent=small, fontName="Sans", textColor=colors.HexColor("#52514e"))
    cell = ParagraphStyle("cell", parent=small, fontName="Sans", fontSize=7.4, leading=9.2, spaceAfter=0)
    note = ParagraphStyle("n", parent=small, fontName="Sans", fontSize=8.2, leading=11)
    P = lambda t, s=body: Paragraph(t, s)

    def box(text, fg="#8a1f1f", bg="#fbe9e9", edge="#b33a3a"):
        return Table([[P(text, ParagraphStyle("bx", parent=note, textColor=colors.HexColor(fg)))]], colWidths=[6.5 * inch],
                     style=[("BACKGROUND", (0, 0), (-1, -1), colors.HexColor(bg)), ("BOX", (0, 0), (-1, -1), 0.6, colors.HexColor(edge)),
                            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("TOPPADDING", (0, 0), (-1, -1), 4), ("BOTTOMPADDING", (0, 0), (-1, -1), 4)])

    st = []
    if RC:
        st += [box("<b>Release candidate. Unpublished.</b> Author review complete within the scope stated in section 8; "
                   f"{_UNREV} links not individually reviewed by the author remain <i>proposed</i>. DOI not yet assigned. Not for citation until released."), Spacer(1, 8)]
    elif not FINAL:
        st += [box("<b>DRAFT. Unpublished.</b> Author review in progress: the author has reviewed a defined subset (section 8); "
                   f"{S['author_review_progress']['links_current_unreviewed']} links are not individually reviewed and remain <i>proposed</i>. "
                   "Numbers and wording may change. Not for citation."), Spacer(1, 8)]
    st += [P("GAP-M: Governance-Aligned Post-deployment Monitoring", title), Spacer(1, 4),
           P("A machine-readable crosswalk of NIST AI RMF, NIST AI 800-4, ONC HTI-1 predictive-DSI source attributes, and CISA CPG 2.0", sub),
           Spacer(1, 8),
           P(f"{A['name']}<super>1</super><br/><font size=8><super>1</super>{A['affiliation']} · ORCID {A['orcid']} · {A['email']}</font>", sub),
           Spacer(1, 3),
           P(f"Technical report · Version {rel['version']} · {rel['release_date'] if FINAL else ('release candidate build ' if RC else 'draft build ') + rel['build_date']} · DOI: {DOI_TXT}",
             ParagraphStyle("m", parent=sub, fontSize=8.5)),
           Spacer(1, 10)]

    st.append(P("Abstract", h1))
    st.append(P(
        f"{'This report' if FINAL else ('This release candidate' if RC else 'This draft')} describes GAP-M, an open, machine-readable set of {S['n_controls']} suggested post-deployment monitoring "
        f"practices for predictive AI systems. It also describes a crosswalk that links each practice to elements of four U.S. federal sources of different kinds: "
        f"voluntary guidance (the {S['src']['rmf_subcategories']} subcategories of the NIST AI Risk Management Framework); "
        f"a report on monitoring challenges (NIST AI 800-4: {S['src']['a84_categories']} monitoring categories, {S['src']['a84_category_challenges']} category-specific and "
        f"{S['src']['a84_crosscutting_items']} cross-cutting gaps and barriers); a regulatory disclosure requirement for certified health IT (the "
        f"{S['src']['hti_attributes']} predictive decision support intervention source attributes of 45 CFR 170.315(b)(11)(iv)(B)); and voluntary cybersecurity "
        f"practices (the {S['src']['cpg_goals']} goals of CISA CPG 2.0). The {S['n_links']} links use NIST IR 8477's supportive-relationship vocabulary, and every one "
        f"of the {S['n_elements_mappable']} mappable source elements has a recorded disposition. At least one practice is linked to {S['mapped_total']} elements "
        f"({S['mapped_total_pct']}%). A necessity audit tested every link that claimed a practice was necessary against the exact source text. "
        f"After a second, stricter pass, {AU['supported']} of {AU['audited']} claims are supported, {AU['revised']} were downgraded, and {AU['unresolved']} remain unresolved and are kept as conditional example_of mappings. "
        f"A tooling-assisted relevance review of the {EXR['reviewed']} original example_of links removed {EXR['removed']} and reworded {EXR['revised']}, leaving {LED['current_total']} links. "
        f"No necessity claim to an AI 800-4 element survived, because that report describes challenges and sets no requirements. "
        f"Mapping coverage is a property of the crosswalk, not of any organization; it does not demonstrate regulatory compliance or monitoring effectiveness."
        + ("" if FINAL else (f" The author's review is complete within the scope stated in section 8 ({S['author_review_progress']['links_current_reviewed']} of the links individually reviewed); the package is unpublished." if RC else f" Author review is in progress: the author has individually reviewed {S['author_review_progress']['links_current_reviewed']} of the links, and the package is unpublished."))))

    st.append(P("1. Why a crosswalk", h1))
    st.append(P(
        "Post-deployment monitoring is addressed, in different ways, by several federal documents. The NIST AI RMF describes the outcome that post-deployment monitoring plans are implemented "
        "(MANAGE 4.1). NIST AI 800-4 reports that practitioners lack trusted monitoring standards and find baselines, ground truth, and longitudinal tracking hard to sustain. "
        "ONC's HTI-1 rule requires certified health IT to support source attributes for predictive decision support interventions, including validity and fairness in local data. "
        "CISA's CPG 2.0 sets out voluntary baseline cybersecurity practices for critical infrastructure, including health care. "
        "In the texts used here, none of the four sources cites another. These texts are the AI RMF 1.0 document, the AI 800-4 report, the eCFR text of 170.315(b)(11), and the CPG 2.0 goal page. "
        "The AI RMF refers to the NIST Cybersecurity Framework, which is not one of the four, and AI 800-4 cites a different NIST AI report (AI 100-2). "
        "The HTI-1 preamble was not reviewed for this work and may discuss NIST guidance. No element-level correspondence among the four was found in the texts reviewed. "
        "GAP-M offers one set of suggested practices, plus a typed, machine-readable record of how each practice relates to each source element."))

    st.append(P("2. Four kinds of source", h1))
    st.append(tbl([["Source", "Kind of statement", "Who it obligates", "Elements used"]] + [list(r) for r in SRC_ROWS],
                  [1.55, 1.75, 1.75, 1.45], cell))
    st.append(Spacer(1, 4))
    st.append(P(
        "The crosswalk interprets a link differently for each kind of source. An AI RMF subcategory is an outcome an organization may choose to pursue. An AI 800-4 gap or barrier is a challenge "
        "practitioners report; a practice can respond to it but cannot satisfy it. An HTI-1 source attribute is information a certified Health IT Module must support. The obligation sits "
        "with the module and its developer, and GAP-M links only describe how a deploying organization's monitoring can supply or check attribute content. A CPG 2.0 goal is a voluntary practice "
        "with a stated scope. GAP-M's own controls are suggested implementation practices, not requirements."))
    st.append(P(
        f"All four sources are U.S. government works. AI RMF text is parsed from the PDF layout, and line-break hyphens are resolved by a documented rule. AI 800-4 table text is transcribed and "
        f"checked verbatim against the PDF ({S['a84_strings_verified']} strings). HTI-1 text comes from the eCFR point-in-time XML dated 2026-10-01; the section was last amended {S['hti_section_last_amended']}. The eCFR is an editorial compilation, not an official legal edition of the CFR. "
        "CPG 2.0 goals are parsed from an archived copy of the CISA page whose parsed records hash identically to those parsed from the live page on 2026-10-05; "
        "the release includes the parsed records, not the archived page. "
        "NIST AI 800-4 states that it \"is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning\" (p. 4, note 4); "
        "GAP-M applies its categories and challenges to predictive systems on that basis."))

    st.append(P("3. Method", h1))
    st.append(P("3.1 Suggested practices", h2))
    fams = "; ".join(f"{k} ({v})" for k, v in S["controls_by_family"].items())
    st.append(P(
        f"GAP-M's {S['n_controls']} controls are original. They are grouped into {S['n_families']} families: one governance family, and families that follow AI 800-4's six monitoring categories, "
        f"with fairness as its own family under Functionality because AI 800-4 has no fairness category ({fams}). Each control states an objective, activity, evidence artifact, cadence, owner role, "
        "and a one-sentence <i>core</i> activity. Only the core counts when necessity is judged."))
    st.append(P("3.2 Mapping vocabulary and the necessity audit", h2))
    st.append(P(
        "Every link reads <i>control supports element</i>, with one NIST IR 8477 property. <b>integral_to</b>: the element cannot be achieved without the control's core activity. "
        "<b>precedes</b>: the core must be achieved first. <b>example_of</b>: the core is one way to achieve the element. "
        "Every link that claimed integral_to or precedes was audited against the exact source text, with a rule for each kind of source. "
        "For AI RMF, necessity is supported only where the subcategory's own words name the core activity. For AI 800-4, necessity is never supported, because a challenge has no completion condition. "
        "For HTI-1, necessity is supported only where no party other than the deploying organization can produce the attribute's value, and then only for a populated value, not for certification. "
        "For CPG 2.0, necessity is supported only where the goal's recommended action, within its stated scope, necessarily reaches the AI system. "
        "Links whose necessity depends on a fact or judgment only the author or a deploying organization can supply are marked <b>unresolved</b> and held at example_of. "
        "The pipeline now refuses any integral_to or precedes link without a supported audit entry, and any example_of rationale that asserts necessity."))
    st.append(P("3.3 Relevance review of example_of links", h2))
    st.append(P(
        f"The {EXR['reviewed']} links that were example_of from the start were reviewed by the AI assistant against the exact source text and the control's own text. "
        "Each was checked for relevance (does the control's activity bear on the element as written), source interpretation (is the element's subject, phase, and scope read correctly), "
        "and unsupported claims (does the rationale say anything the control does not). A link failing relevance, or failing the other two in a way rewording could not fix, was removed. "
        "Removals were not offset to preserve coverage: an element that lost its only link received a disposition instead. This review is tooling-assisted. It is not independent expert "
        "validation and not the author's review."))
    st.append(P("3.4 Dispositions and GAP-M change classes", h2))
    st.append(P(
        "Every mappable element is either linked or given a disposition with a reason: <b>uncovered</b> (relevant to post-deployment monitoring, but no GAP-M control substantively supports it), "
        "<b>prerequisite</b> (a hosting-environment baseline GAP-M assumes), or <b>out of scope</b> "
        "(a design-time, cultural, or research-governance outcome that monitoring evidence does not show). "
        "GAP-M also sorts the HTI-1 attributes into four analytic change classes (Section 5). These classes are GAP-M's, not the regulation's."))

    st.append(P("4. Results", h1))
    st.append(box(f"<b>What coverage means.</b> {COVERAGE_CAVEAT}", fg="#1f3a5f", bg="#eef3f9", edge="#1f3a5f"))
    st.append(Spacer(1, 6))
    cov = [["Source", "Elements", "Mapped", "With integral_to", "Not mapped", "Links"]]
    nm = {"rmf": "AI RMF 1.0 subcategories", "a84": "AI 800-4 categories + challenges", "hti": "HTI-1 source attributes", "cpg": "CPG 2.0 goals"}
    for k, v in C.items():
        cov.append([nm[k], v["elements"], f"{v['mapped']} ({v['mapped_pct']}%)", f"{v['with_integral']} ({v['with_integral_pct']}%)",
                    notmapped(v), v["links"]])
    cov.append(["Total", S["n_elements_mappable"], f"{S['mapped_total']} ({S['mapped_total_pct']}%)",
                f"{sum(v['with_integral'] for v in S['coverage'].values())} ({100 * sum(v['with_integral'] for v in S['coverage'].values()) / S['n_elements_mappable']:.1f}%)",
                f"{sum(v['uncovered'] for v in S['coverage'].values())} uncovered", S["n_links"]])
    st.append(KeepTogether([P("Table 1. Mapping coverage of each source after both reviews. Coverage fell during review because weak links were removed, not replaced.", cap),
                            tbl(cov, [1.75, 0.75, 1.0, 1.05, 1.45, 0.5], cell)]))
    st.append(Spacer(1, 6))
    aud = [["Source kind", "Supported", "Downgraded", "Unresolved"]]
    names = {"guidance": "Guidance (AI RMF)", "monitoring_challenge": "Monitoring challenges (AI 800-4)",
             "regulatory_disclosure_requirement": "Disclosure requirement (HTI-1)", "voluntary_practice": "Voluntary practice (CPG 2.0)"}
    for t, v in AU["by_source_type"].items():
        aud.append([names[t], v["supported"], v["revised"], v["unresolved"]])
    aud.append(["Total", AU["supported"], AU["revised"], AU["unresolved"]])
    st.append(KeepTogether([P(f"Table 2. Necessity audit of the {AU['audited']} links that claimed integral_to ({AU['audited_integral']}) or precedes ({AU['audited_precedes']}).", cap),
                            tbl(aud, [2.6, 1.3, 1.3, 1.3], cell)]))
    st.append(Spacer(1, 6))
    led = [["Original property", "Original", "Kept as is", "To example_of", "Conditional (unresolved)", "Removed (AI review)", "Removed (author)"]]
    for p in ("integral_to", "precedes"):
        v = LED[p]
        led.append([p, v["original"], v["still_" + p], v["to_example_of_revised"], v["to_example_of_conditional_unresolved"], v["removed_by_example_review"], v["removed_by_author_review"]])
    v = LED["example_of"]
    led.append(["example_of", v["original"], f"{v['kept'] + v['kept_rationale_revised']} ({v['kept_rationale_revised']} reworded)", "—", "—", v["removed"], v["removed_by_author_review"]])
    led.append(["Total", LED["original_total"], "", "", "", LED["removed_by_example_review_total"], LED["removed_by_author_review_total"]])
    st.append(KeepTogether([P(f"Table 3. Link ledger: every link of the original build by its original property. Current total {LED['current_total']} = {LED['original_total']} − {LED['removed_total']}.", cap),
                            tbl(led, [1.15, 0.7, 1.25, 0.9, 1.05, 0.8, 0.8], cell)]))
    st.append(Spacer(1, 6))
    st.append(P(
        f"After both reviews the crosswalk holds {S['property_counts']['integral_to']} integral_to, {S['property_counts']['precedes']} precedes, and {S['property_counts']['example_of']} example_of links. "
        f"Most links therefore say a practice is <i>one way</i> to pursue an element, not that it is required. "
        f"The {S['property_counts']['integral_to']} remaining necessity claims are those where the source names the control's core activity, or where a CPG goal's scope necessarily reaches the AI system: "
        f"{necessity_list()}. A second pass rechecked every remaining necessity claim against a narrowed control core and changed {len(S['pass2']['changed'])} of them: {sum(c['verdict'] == 'revised' for c in S['pass2']['changed'])} downgraded where a plausible alternative exists, "
        f"and {sum(c['verdict'] == 'unresolved' for c in S['pass2']['changed'])} held as unresolved where necessity turns on how the source is read "
        f"(docs/MAPPING_REVIEW.md, section 11). The {LED['conditional_links']} unresolved links are kept as conditional example_of mappings. Their necessity is unresolved; the author reviewed each and accepted it as a conditional mapping. The condition under which each would be necessary is listed in docs/MAPPING_REVIEW.md. "
        f"Controls carry a median of {S['links_per_control']['median']:g} links (range {S['links_per_control']['min']}–{S['links_per_control']['max']}). "
        f"{S['controls_touching_three_plus']} of {S['n_controls']} controls link to at least three of the four sources."))
    st.append(KeepTogether([Image(os.path.join(ROOT, "report", "figures", "fig1_coverage.png"), width=6.5 * inch, height=6.5 * inch * 660 / 1584),
                            P("Figure 1. Share of each source's elements by disposition and strongest link property, after both reviews.", cap)]))
    short = lambda e: e.split(":", 1)[1].replace("-", " ")
    byd = {d: [short(u["element_id"]) for u in S["unmapped"] if u["disposition"] == d] for d in ("uncovered", "out_of_scope", "prerequisite")}
    st.append(P(
        f"<b>Uncovered</b>, a known gap in GAP-M v0.1.0 ({len(byd['uncovered'])}): {', '.join(byd['uncovered'])}. "
        f"<b>Out of monitoring scope</b> ({len(byd['out_of_scope'])}): {', '.join(byd['out_of_scope'])}. "
        f"<b>Prerequisite baseline</b> for the systems hosting the AI ({len(byd['prerequisite'])}): CPG {', '.join(byd['prerequisite'])}. "
        "Each carries its reason in data/crosswalk/gapm_dispositions.csv."))
    st.append(KeepTogether([Image(os.path.join(ROOT, "report", "figures", "fig2_family_by_source.png"), width=6.5 * inch, height=6.5 * inch * 813 / 2000),
                            P("Figure 2. Links by GAP-M control family (rows; control count in parentheses) and source group (columns).", cap)]))

    st.append(P("5. HTI-1 source attributes and GAP-M change classes", h1))
    st.append(P(
        "The regulation's only language about currency is 170.315(b)(11)(v)(A)(1). It requires the Health IT Module to give access to \"complete and up-to-date\" descriptions of every attribute "
        "of a developer-supplied intervention. That requirement applies to all attributes alike, and the duty sits with the module and its developer. Paragraph (v)(A)(2) lets "
        f"{S['hti_na_flag']} attributes be shown as not available, and (v)(B) lets identified users record and change attributes. "
        "GAP-M's four change classes are an analytic classification of what most often changes an attribute's value after deployment. The source text does not establish them, and they do not decide "
        f"which practices are necessary. The {S['hti_not_static']} attributes outside the set-at-release class are what earlier drafts called dynamic; that term is retired."))
    hrows = [["GAP-M change class", "Attributes", "With integral_to", "With precedes", "Example_of only", "Not-available allowed"]]
    for k, v in S["hti_by_class"].items():
        hrows.append([CLS_LABEL[k], v["attributes"], v["with_integral"], v["with_precedes"], v["example_only"], v["na_flag"]])
    hrows.append(["Total", S["src"]["hti_attributes"], S["hti_with_integral"], S["hti_with_precedes"], S["hti_example_only"], S["hti_na_flag"]])
    st.append(KeepTogether([P("Table 4. HTI-1 attributes by GAP-M change class. Rows sum to the regulation's attribute count.", cap),
                            tbl(hrows, [1.65, 0.85, 1.0, 0.95, 1.05, 1.0], cell)]))
    st.append(Spacer(1, 6))
    st.append(P(
        f"After both reviews, only {', '.join(x.replace('HTI:', '') for x in S['hti_with_integral_ids'])} (validity of the intervention in local data) has a practice judged necessary: measuring validity in the deploying "
        "organization's own data. That necessity is for a populated value, not for certification. For (B)(8)(iv), local fairness, necessity is conditional, because the regulation does not define fairness "
        "and individual-fairness measures are an alternative to group comparisons. Outcome labels are not treated as a prerequisite for local fairness, because output-rate parity uses no labels. "
        "Whether they are a prerequisite for local validity is unresolved: label-free accuracy estimation exists [8], but the same work shows that target accuracy is identifiable "
        "only under assumptions on the shift, such as an unchanged outcome relationship p(y|x), which local validation is meant to test. Whether the deploying organization must also record local values itself, rather than send them to the "
        f"developer, is unresolved. Missing information is handled by attribute. The {S['hti_na_flag']} attributes listed in (v)(A)(2) may be shown as not available. For the other "
        f"{S['src']['hti_attributes'] - S['hti_na_flag']}, (v)(A)(1) expects complete and up-to-date descriptions, so GAP-M (GM-HF-03) records a missing value as a gap to raise with the developer, "
        "not as not available. Figure 3 shows every attribute-practice link."))
    st.append(KeepTogether([Image(os.path.join(ROOT, "report", "figures", "fig3_hti_attribute_maintenance.png"), width=5.6 * inch, height=5.6 * inch * 1848 / 1892),
                            P("Figure 3. The 31 HTI-1 predictive-DSI source attributes (rows, with GAP-M change class) and the GAP-M controls linked to each, by IR 8477 property.", cap)]))

    st.append(P("6. The suggested practices", h1))
    rows = [["ID", "Control", "RMF", "800-4", "HTI", "CPG"]]
    for c in controls:
        rows.append([c["control_id"], c["title"], c["links_RMF"] or "", c["links_A84"] or "", c["links_HTI"] or "", c["links_CPG"] or ""])
    st.append(P("Table 5. GAP-M controls and their link counts per source. Full definitions are in data/crosswalk/gapm_controls.csv.", cap))
    st.append(tbl(rows, [0.85, 3.85, 0.45, 0.45, 0.45, 0.45], cell, repeat=1))

    st.append(P("7. Limitations", h1))
    st.append(P(
        "Mapping coverage does not demonstrate compliance with any regulation, achievement of any framework outcome, or effective monitoring. "
        "The links, the necessity audit, and the relevance review are judgment prepared with AI assistance; none is independent expert validation. "
        f"{S['n_uncovered']} relevant elements are uncovered by any GAP-M control. "
        + (f"The author has individually reviewed {S['author_review_progress']['links_current_reviewed']} of the {LED['current_total']} links; the other {S['author_review_progress']['links_current_unreviewed']} have not been individually reviewed, and no inter-rater agreement has been measured. ")
        + "The practices have not been piloted. HTI-1 obligations fall on certified health IT, not on deploying organizations, and only paragraph (b)(11)(iv)(B) is mapped. "
        "AI 800-4 describes challenges, not requirements, and focuses on generative AI; GAP-M applies it to predictive systems. GAP-M's attribute change classes are analytic. "
        "The AI RMF Playbook and Generative AI Profile are not mapped. "
        "GAP-M has no official status. The full list is in docs/LIMITATIONS.md."))

    st.append(P("8. Verification status", h1))
    if FINAL or RC:
        st.append(P("<b>Author's statement.</b> " + ("Author review completed before release." if FINAL else "Author review complete; release pending.")))
        for para in str(rel["ai_statement_final"]).strip().split("\n\n"):
            st.append(P(para.replace("`", "").replace("\n", " ")))
    else:
        st.append(P("<b>Automated checks (completed by the build pipeline).</b> These include source element counts against the documents, verbatim checks of transcribed text, the CPG record hash against the live-page capture, "
                    f"crosswalk rules R1–R13, JSON Schema validation of every output, OSCAL validation against NIST's 1.1.3 schema, and {S['negative_tests_passed']} of {S['negative_tests_total']} negative tests. "
                    "These checks confirm the package is internally consistent and faithful to the source text as parsed. They do not confirm that any mapping is right."))
        st.append(P("<b>Reproducibility.</b> A clean rebuild in the same environment (Linux, Python 3.13) reproduces every generated file byte for byte. A rebuild on macOS (Python 3.10) "
                    "reproduced every data, schema, and Markdown file byte for byte; the workbook matched cell for cell and this PDF matched in extracted text, but these binary files and "
                    "the figures differ in bytes because rendering libraries differ. Byte identity is not claimed across environments."))
        st.append(P("<b>Necessity audit (pre-review, two passes).</b> Prepared with AI assistance as input to the author's review (docs/MAPPING_REVIEW.md). The second pass rechecked every remaining "
                    "necessity claim against a narrowed control core, and assessed the relevance of each conditional link separately from its necessity. It is not the author's review."))
        st.append(P(f"<b>Relevance review of example_of links (tooling-assisted).</b> Carried out by the AI assistant on the {EXR['reviewed']} original example_of links. It is not independent expert validation and not the author's review."))
        st.append(P(f"<b>Conditional links.</b> {LED['conditional_links']} links are kept as conditional example_of mappings because their necessity is unresolved. Their necessity is unresolved; the author reviewed each and accepted it as a conditional mapping."))
        st.append(P(f"<b>Author review (in progress).</b> {S['author_review_scope_text']} Links the author has not reviewed are marked proposed. The author has not yet revised this text."))
        st.append(P("AI assistance", h2))
        st.append(P(
            "This draft was prepared with substantial assistance from an AI assistant (Anthropic's Claude). The assistant wrote the retrieval, parsing, validation, and document-building code; "
            "drafted the control definitions, link rationales, the necessity audit, and this text; and ran the automated checks. The author set the project scope and target. "
            "A statement of the author's own review will replace this paragraph on release, written by the author once that review is complete."))

    st.append(P("9. Availability", h1))
    if FINAL:
        st.append(P(f"Released under CC BY 4.0 (data, schemas, figures, report) and MIT (code) at {rel['repository']}, archived at Zenodo, DOI {rel['doi']}."))
    else:
        st.append(P(f"Not yet published. On the author's approval the package is planned for release at {rel['repository']}, with a Zenodo archive and DOI, under CC BY 4.0 "
                    "(data, schemas, figures, report) and MIT (code). Until then it should not be cited or redistributed as a release."))

    st.append(P("References", h1))
    refs = [
        "National Institute of Standards and Technology. Artificial Intelligence Risk Management Framework (AI RMF 1.0). NIST AI 100-1, 2023. doi:10.6028/NIST.AI.100-1",
        "Rao AK, Keller AJ, Kalra N, Steed R, Kwegyir-Aggrey K, Klyman K, Staheli D, Bergman AS. Challenges to the Monitoring of Deployed AI Systems. NIST AI 800-4, 2026. doi:10.6028/NIST.AI.800-4",
        "Office of the National Coordinator for Health Information Technology. Health Data, Technology, and Interoperability: Certification Program Updates, Algorithm Transparency, and Information Sharing (HTI-1) Final Rule. 89 FR 1192, January 9, 2024.",
        "45 CFR 170.315(b)(11), Decision support interventions. Electronic Code of Federal Regulations, text as of October 1, 2026.",
        "Cybersecurity and Infrastructure Security Agency. Cybersecurity Performance Goals 2.0 (CPG 2.0). December 2025. https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0",
        "National Institute of Standards and Technology. Mapping Relationships Between Documentary Standards, Regulations, Frameworks, and Guidelines. NIST IR 8477, 2024. doi:10.6028/NIST.IR.8477",
        "National Institute of Standards and Technology. Open Security Controls Assessment Language (OSCAL), version 1.1.3.",
        "Garg S, Balakrishnan S, Lipton ZC, Neyshabur B, Sedghi H. Leveraging Unlabeled Data to Predict Out-of-Distribution Performance. "
        "International Conference on Learning Representations (ICLR), 2022. arXiv:2201.04234",
    ]
    for i, r in enumerate(refs, 1):
        st.append(P(f"[{i}] {r}", small))

    def deco(canvas, doc):
        canvas.saveState()
        canvas.setFont("Sans", 7.5)
        canvas.setFillColor(colors.HexColor("#8a8984"))
        canvas.drawString(inch, 0.55 * inch, f"GAP-M v{rel['version']} · Clement, T." + (" · CC BY 4.0" if FINAL else ""))
        canvas.drawRightString(7.5 * inch, 0.55 * inch, f"{doc.page}")
        if not FINAL:
            canvas.setFillColor(colors.HexColor("#b33a3a"))
            canvas.drawCentredString(4.25 * inch, 0.55 * inch, "Release candidate — unpublished; DOI pending" if RC else "DRAFT — unpublished; author review pending")
        canvas.restoreState()

    out = os.path.join(ROOT, "report", "GAP-M_technical_report.pdf")
    doc = SimpleDocTemplate(out, pagesize=letter, leftMargin=inch, rightMargin=inch, topMargin=0.85 * inch,
                            bottomMargin=0.85 * inch, title=rel["title"] + ("" if FINAL else (" (release candidate)" if RC else " (unpublished draft)")), author=A["name"],
                            subject="Machine-readable crosswalk for post-deployment AI monitoring",
                            keywords="AI RMF, NIST AI 800-4, HTI-1, CPG 2.0, monitoring, crosswalk, OSCAL")
    doc.build(st, onFirstPage=deco, onLaterPages=deco)


def tbl(rows, widths, cell, repeat=1):
    hstyle = ParagraphStyle("hh", parent=cell, textColor=colors.white, fontName="Sans-B")
    data = [[Paragraph(str(x), hstyle if i == 0 else cell) for x in r] for i, r in enumerate(rows)]
    t = Table(data, colWidths=[w * inch for w in widths], repeatRows=repeat)
    t.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#1f3a5f")),
        ("LINEBELOW", (0, 0), (-1, -1), 0.3, colors.HexColor("#d9d8d4")),
        ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ("TOPPADDING", (0, 0), (-1, -1), 2.5), ("BOTTOMPADDING", (0, 0), (-1, -1), 2.5),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f5f4f1")]),
    ]))
    return t


if __name__ == "__main__":
    readme(); citation(); report()
    print("documents written", "(FINAL)" if FINAL else ("(RELEASE CANDIDATE)" if RC else "(DRAFT)"))
