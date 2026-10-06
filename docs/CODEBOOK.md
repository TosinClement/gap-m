# Codebook (GAP-M v0.1.0)

Status: released 2026-10-05.

## Identifiers
| Prefix | Source | Example | Meaning |
|---|---|---|---|
| `RMF:` | NIST AI 100-1 | `RMF:MEASURE-2.4` | AI RMF subcategory MEASURE 2.4. `RMF:MEASURE-2` is the category, `RMF:MEASURE` the function. |
| `A84:` | NIST AI 800-4 | `A84:FUN`, `A84:FUN-B1`, `A84:XC-TMT-G1` | Monitoring category; category challenge (G = gap, B = barrier, from Table 3); cross-cutting item (Table 2). |
| `HTI:` | 45 CFR 170.315(b)(11)(iv)(B) | `HTI:B8.ii` | Paragraph (b)(11)(iv)(B)(8)(ii). `HTI:B8` is the attribute group. |
| `CPG:` | CISA CPG 2.0 | `CPG:3.Q` | CPG 2.0 goal 3.Q. `CPG:PROTECT` is the function. |
| `GM-` | GAP-M | `GM-FUN-02` | GAP-M control: family code and sequence number. |

## data/registry/elements.csv (and .json)
| Column | Definition |
|---|---|
| element_id | Identifier as above. |
| framework | `AI RMF 1.0`, `NIST AI 800-4`, `ONC HTI-1 (b)(11)`, or `CISA CPG 2.0`. |
| level | Element type: function, category, subcategory, monitoring_category, category_gap, category_barrier, crosscutting_category, crosscutting_gap, crosscutting_barrier, attribute_group, source_attribute, goal. |
| parent_id | Parent element, if any. |
| code | Native code in the source (e.g. `MEASURE 2.4`, `(B)(8)(ii)`, `3.Q`). |
| label | Short label (CPG goal title; HTI attribute without trailing punctuation). |
| text | Verbatim source text (whitespace normalized; AI RMF line-break hyphens resolved per QA report). For CPG goals, the goal's Outcome text. |
| locator | Where the text is found in the source (printed page, table, or CFR paragraph). |
| source_type | `guidance` (AI RMF), `monitoring_challenge` (AI 800-4), `regulatory_disclosure_requirement` (HTI-1), or `voluntary_practice` (CPG 2.0). |
| obligation_holder | Who, if anyone, the source obligates. |
| mappable | `true` for the elements GAP-M maps (AI RMF subcategories, AI 800-4 categories and challenges, HTI attributes, CPG goals). |
| hti_gapm_change_class | HTI attributes only: GAP-M's **analytic** classification of what most often changes the value after deployment (`static_at_release`, `process_description`, `evidence_accruing`, `locally_measured`). Not established by the regulation (J6). |
| hti_gapm_change_note | HTI attributes only: note on the classification. |
| hti_na_flag | HTI attributes only: `true` if 170.315(b)(11)(v)(A)(2) requires the module to indicate when information is not available. |
| cpg_risk_addressed, cpg_scope, cpg_recommended_action, cpg_cost, cpg_impact, cpg_ease | CPG goals only: verbatim fields from the CPG 2.0 page. |

## data/crosswalk/gapm_controls.csv (and .json)
| Column | Definition |
|---|---|
| control_id | GAP-M control identifier. |
| family, family_name | Control family code and name (GOV, FUN, FAIR, OPS, HF, SEC, CMP, LSI). |
| a84_primary_category | AI 800-4 category the family sits under (`XC` = cross-cutting governance). |
| practice_type | Always `suggested_practice`. |
| core | One-sentence core activity; the only part of the control counted when necessity is judged. |
| title, objective, activity, evidence, cadence, owner_role | Control definition. `evidence` names the artifact an auditor would ask for. |
| links_total, links_RMF, links_A84, links_HTI, links_CPG | Number of links from the control, total and per framework. |
| review_status | `proposed` (no author response), `accepted`, `revised` (accepted with the author's edits), or `rejected`. Set from mapping/author_review.yaml. |

## data/crosswalk/gapm_links.csv (and .json)
| Column | Definition |
|---|---|
| link_id | `control_id>target_id`. |
| control_id | GAP-M control (concept A). |
| target_id, target_framework, target_level, target_code, target_label | Source element (concept B). |
| relationship | Always `supports` (NIST IR 8477 supportive relationship mapping). |
| property | `integral_to`, `example_of`, or `precedes` (see docs/MAPPING_USE_CASE.md). |
| rationale | One sentence explaining the link. |
| review_status | As above. |
| mapping_style | Mapping style reference. |
| target_source_type | Source kind of the target element. |
| audit_verdict | Necessity audit: `supported`, `revised`, `unresolved`, or `not_audited` (link never claimed necessity). Pre-review, AI-assisted; not the author's review. |
| audit_original_property | Property before the audit. |
| audit_basis | Reason for the verdict, citing the source text. |
| audit_condition | For `unresolved`: the condition under which the link would be necessary. |
| audit_pass1_property | For links changed in the second correction pass: the property after the first pass. Empty otherwise. |
| audit_relevance | For `unresolved` (conditional) links: whether the weaker `example_of` mapping is substantively relevant (`supported` or `unsupported`), assessed separately from necessity. |
| audit_relevance_basis | Reason for the relevance assessment, citing the source text. |
| conditional | `true` for the unresolved necessity links, kept as conditional `example_of` mappings for v0.1.0. Their necessity is recorded as unresolved; the author reviewed each and accepted it as conditional. |
| author_response | The author's recorded response from the guided review (docs/AUTHOR_REVIEW.md), or `not_reviewed`. Also on controls. |
| author_review_scope | `census_integral_to`, `census_conditional`, `random_sample` (seed in mapping/author_review.yaml), or `not_sampled`. |
| example_review | Tooling-assisted relevance review by the AI assistant of links that were `example_of` from the start: `keep`, `revise` (rationale reworded), or `not_applicable` (link was in the necessity audit). Not independent expert validation; not the author's review. |
| example_review_note | Basis for the review decision. |

## data/crosswalk/gapm_dispositions.csv (and .json)
One row per mappable source element.

| Column | Definition |
|---|---|
| element_id, framework, level, parent_id, code, label | From the registry. |
| source_type | Source kind. |
| disposition | `mapped`, `uncovered` (relevant but no GAP-M control supports it), `prerequisite`, or `out_of_scope`. |
| reason | Required when not mapped. |
| n_controls | Number of GAP-M controls linked. |
| n_integral | Number of those links with property `integral_to`. |
| strongest_property | Strongest property among the links (integral_to > precedes > example_of). |
| controls | Semicolon-separated control ids. |
| review_status | As above. |

## data/crosswalk/gapm_hti_attributes.csv
One row per HTI-1 predictive-DSI source attribute: CFR paragraph, attribute text, GAP-M change class (`gapm_change_class`, analytic), the not-available flag, and the controls linked to it, grouped by property.

## data/processed/mapping_review.csv
One row per audited link: control and its core, target, source kind, locator, exact source text (for CPG: outcome, scope, and recommended action), original and current property, verdict, basis, condition, current rationale, relevance of the `example_of` mapping and its basis (unresolved links only), first-pass verdict and property (links changed in the second pass), and an empty `author_ruling` column.

## data/processed/author_review.csv
One row per practice and per link: review set (`integral_to (all)`, `conditional (all)`, `random sample`, or `not sampled`), the author's response or `not_reviewed`, the result, and any edit applied.

## data/processed/example_review.csv
One row per original `example_of` link reviewed (plus one audited link removed for consistency): decision (`keep`, `revise`, `remove`), failed test (T1 relevance, T2 source interpretation, T3 unsupported claim), basis, and any new rationale. Removed links are also listed in `gapm_crosswalk.json` under `removed_links` and in the workbook's Removed sheet.

## data/crosswalk/gapm_catalog_oscal.json
OSCAL 1.1.3 catalog. Groups are GAP-M families. Each control has `statement`, `guidance` (activity, cadence, owner role) and `assessment-objective` (evidence) parts. Every crosswalk link is a prop named `supports` in namespace `https://w3id.org/gap-m/ns`, with `value` = source element id, `class` = IR 8477 property, and `remarks` = rationale. Back-matter resources cite the four sources.

## data/crosswalk/gapm_crosswalk.json
All of the above in one file, plus source metadata. Schema: `schema/gapm_crosswalk.schema.json`.

## data/crosswalk/GAP-M_crosswalk.xlsx
Reviewer workbook regenerated from the YAML; do not edit it directly.

## mapping/ (human-edited inputs)
| File | Content |
|---|---|
| gapm_controls.yaml | Control definitions and every link with property and rationale. The single source of truth. |
| dispositions.yaml | Reasons for every unmapped element. |
| ai800_4_elements.yaml | AI 800-4 table text, checked verbatim against the PDF by the pipeline. |
| hti_attribute_classes.yaml | GAP-M analytic change class for each HTI attribute. |
| example_review.yaml | Relevance review of original `example_of` links: removals and rewordings with test and basis, and the full kept list. |
| author_review.yaml | The author's guided review: sampling seed and IDs, and her recorded response to each practice, link, disposition, and spot-check. Only her responses are recorded; items without one are unreviewed. |
| link_audit.yaml | Necessity audit: core statement per control, and a verdict with basis for every link that claimed necessity. Links changed in the second correction pass carry `pass1` (first-pass verdict, property, basis); unresolved links carry `relevance` and `relevance_basis`; `second_pass` records the date, scope, and previous wording of narrowed cores. |
