# GAP-M: Governance-Aligned Post-deployment Monitoring

**Status:** Released 2026-10-05 · version 0.1.0 · DOI: 10.5281/zenodo.23178136

GAP-M is a machine-readable crosswalk. It links one set of suggested post-deployment monitoring practices for predictive AI systems to four U.S. federal sources. **The four sources are different kinds of documents, and the crosswalk keeps them distinct:**

| Source | What kind of statement | Who it obligates | Elements |
|---|---|---|---|
| NIST AI RMF 1.0 (NIST AI 100-1) | Voluntary guidance: risk-management outcomes | No one (voluntary) | 72 subcategories |
| NIST AI 800-4 | Report on monitoring challenges: categories, gaps, barriers | No one (describes challenges; sets no requirements) | 6 categories; 19 category and 13 cross-cutting gaps/barriers |
| 45 CFR 170.315(b)(11)(iv)(B) (ONC HTI-1) | Regulatory disclosure requirement for certified health IT | The certified Health IT Module and its developer, not deploying organizations | 31 source attributes |
| CISA CPG 2.0 | Voluntary practices with recommended actions | No one (voluntary) | 34 goals |
| GAP-M controls (this work) | Suggested implementation practices | No one; not endorsed by any agency | 32 controls |

GAP-M has **32 controls** in 8 families. They are joined to the sources by **283 links**, each using NIST IR 8477's supportive-relationship vocabulary (`supports`, with property `integral_to`, `example_of`, or `precedes`) and a one-sentence rationale. Every mappable source element has a recorded disposition, each with a reason: mapped, uncovered (relevant but not supported by any GAP-M control), prerequisite baseline, or out of monitoring scope.

## What the coverage numbers mean, and what they do not

A mapped element has at least one GAP-M control linked to it. Mapping coverage is a property of the crosswalk, not of any organization: it does not show that an organization complies with a regulation, meets a framework outcome, or monitors effectively.

| Source | Elements | Mapped | With a link judged necessary (integral_to) | Not mapped |
|---|---|---|---|---|
| AI RMF 1.0 subcategories | 72 | 61 (84.7%) | 7 | 2 uncovered, 9 out of scope |
| NIST AI 800-4 categories and challenges | 38 | 36 (94.7%) | 0 | 1 uncovered, 1 out of scope |
| HTI-1 predictive-DSI source attributes | 31 | 31 (100.0%) | 1 | 0 |
| CISA CPG 2.0 goals | 34 | 21 (61.8%) | 5 | 13 prerequisite |
| **Total** | **175** | **149 (85.1%)** | | **26** |

Coverage fell during review because weak links were removed rather than kept for coverage's sake.

For AI 800-4, "mapped" means a control is one response to a reported challenge. It does not mean the challenge is solved. For HTI-1, the disclosure obligation sits with the certified Health IT Module. GAP-M links describe how a deploying organization's monitoring can supply or check attribute content. They are not a compliance pathway.

## Link review and ledger

Every link in the original build has been through one of two reviews, both prepared by the AI assistant: a necessity audit for links that claimed a practice was necessary, and a relevance review for links that were `example_of` from the start. Neither is independent expert validation or the author's review. The author's own review of a subset, and her rulings on these reviews' removals and rewordings, are recorded in docs/AUTHOR_REVIEW.md.

| Original property | Original links | Kept as is | Changed to `example_of` | Conditional `example_of` (unresolved) | Removed (AI review) | Removed (author) |
|---|---|---|---|---|---|---|
| `integral_to` | 100 | 14 | 77 | 8 | 1 | 0 |
| `precedes` | 7 | 0 | 5 | 1 | 0 | 1 |
| `example_of` | 210 | 178 (rationale reworded for 8) | — | — | 31 | 1 |
| **Total** | **317** | | | | **32** | **2** |

The current crosswalk has **283 links**: 14 `integral_to`, 0 `precedes`, and 269 `example_of`. Of the `example_of` links, 9 are conditional. Their necessity is unresolved and recorded as such; the author reviewed each one and accepted it as a conditional mapping.

### Necessity audit

All 107 links that originally claimed necessity (100 `integral_to`, 7 `precedes`) were tested against the exact source text: could the source element, as written, be achieved without the control's core activity? Results:
- 14 supported
- 84 downgraded to `example_of`
- 9 unresolved, kept as conditional `example_of` mappings for v0.1.0

No necessity claim to an AI 800-4 element survived. The report describes challenges and sets no completion condition, so necessity cannot be read from its text.

### Relevance review of the original `example_of` links

Each of the 210 links was tested for three things against the exact source text and the control's own text:
- relevance: does the control's activity bear on the element as written?
- source interpretation: is the element's subject, phase, and scope read correctly?
- unsupported claims: does the rationale claim anything the control does not say?

Results:
- 170 kept
- 9 kept with a reworded rationale
- 31 removed

One further link from the audited set was removed for consistency. 12 elements lost their only links and now carry a disposition instead.

Details are in [docs/MAPPING_REVIEW.md](docs/MAPPING_REVIEW.md).

## HTI-1 attributes and GAP-M's change classes

GAP-M sorts the 31 attributes into four **analytic** classes by what most often changes their value after deployment. The regulation draws no such distinction. Its only currency language, 170.315(b)(11)(v)(A)(1), requires "complete and up-to-date" descriptions of *every* attribute, and places that duty on the Health IT Module.

| GAP-M class | Attributes | With an integral link | Example-only links | Must show "not available" when missing |
|---|---|---|---|---|
| set at release (`static_at_release`) | 16 | 0 | 16 | 0 |
| process description (`process_description`) | 4 | 0 | 4 | 2 |
| new evidence possible (`evidence_accruing`) | 9 | 0 | 9 | 7 |
| measured locally (`locally_measured`) | 2 | 1 | 1 | 2 |
| **Total** | **31** | **1** | **30** | **11** |

Only B8.ii (validity of the intervention in local data) keeps a link judged necessary: measuring validity in the deploying organization's own data. That necessity holds only for a populated value, since 170.315(b)(11)(v)(A)(2) lets the module show this attribute as not available. Two related points:
- **(B)(8)(iv), local fairness:** the necessity link is now conditional, because the regulation does not define fairness.
- **Outcome labels:** these are not treated as a prerequisite for local fairness, because fairness measures such as output-rate parity use no labels. Whether labels are a prerequisite for local validity is unresolved. Label-free accuracy estimation exists (Garg et al., ICLR 2022), but it rests on the assumption that the outcome relationship has not shifted, which local validation is meant to test.

The not-available allowance applies only to the 11 attributes listed in (v)(A)(2). For the other 20, (v)(A)(1) expects complete and up-to-date descriptions, so GAP-M records a missing value as a gap to resolve with the developer.

## Verification status

Author review completed before release. The author's statement:

GAP-M v0.1.0 was prepared with substantial assistance from an AI assistant, Claude (Anthropic). I set the project's scope and target. The assistant wrote the code that retrieves, parses, and validates the sources and builds the documents; drafted the 32 practice definitions, every link and its rationale, the source-element dispositions, and the text of the README, technical report, and supporting documents; and carried out, with tooling support, a necessity audit of every link that claimed a practice was necessary and a relevance review of the 210 links that were `example_of` from the start.

I then reviewed the work in a guided process. For each item the assistant showed the exact source text, the practice's core, the proposed relationship and rationale, and a recommendation, and I recorded my decision. I reviewed all 32 practice definitions, accepting 18 as written and 14 with edits. I individually reviewed 100 links: all 14 `integral_to` links, all 9 conditional links, a random sample of 66 of the 262 other `example_of` links (25%, drawn once with seed 20261005), and 11 links in targeted checks. Of these I accepted 87 as written, accepted 11 with reworded rationales, and removed 2. I also ruled on every change made by the AI-assisted review: I confirmed its 32 removals and accepted 8 of its 9 reworded rationales (the ninth applied to a link I had removed). I made the open framing decisions recorded in docs/AUTHOR_DECISIONS.md, and I spot-checked named passages and counts in all four sources against the original documents. In nearly every case I accepted the assistant's recommended option, and I ruled on many links as groups after reading each one.

Separately from my review, the build pipeline runs automated checks that the assistant wrote and ran. They compare source element counts with the documents; check transcribed text verbatim, including 55 strings from NIST AI 800-4; compare the CPG 2.0 records against a hash of the live CISA page; enforce the crosswalk's consistency rules; validate every output against its JSON Schema and the OSCAL catalog against NIST's OSCAL 1.1.3 schema; and confirm that corrupted inputs are rejected (5 of 5 tests). A clean rebuild in the same environment reproduces every file byte for byte; a rebuild on a second computer reproduces the data and text exactly. These checks show that the package is internally consistent and faithful to the source text as parsed. They do not show that any mapping is correct, and they are not part of my review.

My review covered a defined subset. Of the 283 links in this release, 185 were not individually reviewed by me; they rest on the assistant's drafting and the AI-assisted reviews, and they are marked `review_status: proposed` and `author_response: not_reviewed` in the data. Sixteen of them received wording-only consistency edits that I approved without reviewing each link. Links that the necessity audit downgraded to `example_of` had a lighter relevance check than the rest: I reviewed 27 of the 82, through my random sample and one targeted check. My source check was a spot-check of named items; full verification of the transcribed text was done by the automated checks.

Neither my review nor the AI-assisted reviews is independent expert validation, and no inter-rater agreement has been measured. The practices have not been piloted in any deploying organization. GAP-M is independent work; it is not a product of NIST, ONC/ASTP, or CISA, and none of these agencies has reviewed or endorsed it. Mapping coverage does not demonstrate compliance with any regulation, achievement of any framework outcome, or effective monitoring. I take responsibility for the decisions recorded in docs/AUTHOR_REVIEW.md and docs/AUTHOR_DECISIONS.md.

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
| S3 | 45 CFR 170.315(b)(11) (ONC HTI-1 Final Rule, 89 FR 1192), eCFR point-in-time text | 2026-10-01 (section last amended 2025-10-01) |
| S4 | CISA Cybersecurity Performance Goals 2.0 | released 2025-12-10; captured 2026-10-05 |

Mapping vocabulary: NIST IR 8477 (2024), doi:10.6028/NIST.IR.8477.

NIST AI 800-4 states that it "is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning" (p. 4, note 4). GAP-M applies its categories and challenges to predictive systems on that basis.

GAP-M is independent work. It is not a NIST, ONC/ASTP, or CISA product and has not been reviewed or endorsed by them.

## License

On release: code under MIT; data, crosswalk, schemas, figures, and documents under CC BY 4.0. Quoted source text is U.S. Government work, not subject to copyright in the United States (17 U.S.C. 105); NIST grants a worldwide license for its publications and requests the credit line "Republished courtesy of the National Institute of Standards and Technology." See [LICENSE](LICENSE).

## Citation

Clement, T. (2026-10-05). *GAP-M: Governance-Aligned Post-deployment Monitoring* (Version 0.1.0) [Data set]. Zenodo. 10.5281/zenodo.23178136

## Maintainer

Tosin Clement · Independent Researcher · ORCID [0009-0001-2055-5113](https://orcid.org/0009-0001-2055-5113) · clementtosin92@gmail.com
