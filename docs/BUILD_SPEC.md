# GAP-M build spec (v0.1.0)

Status: released 2026-10-05 (spec written 2026-10-04 CT, before any mapping code).

```
PROJECT:   GAP-M — Governance-Aligned Post-deployment Monitoring.
           Archetypes: (1) open dataset / machine-readable crosswalk, plus (9) a short technical report.

QUESTION:  If an organization deploys a predictive AI system (for example, a predictive decision
           support intervention in a certified EHR), which monitoring controls do they need so that
           one set of monitoring evidence satisfies NIST AI RMF, addresses NIST AI 800-4's monitoring
           challenges, keeps the 31 HTI-1 predictive-DSI source attributes current, and fits CISA's
           CPG 2.0 baseline? And which parts of each framework does that control set cover or leave out?

SOURCES (all U.S. government works, public domain in the U.S.):
  S1  NIST AI 100-1, AI Risk Management Framework 1.0 (Jan 2023). doi:10.6028/NIST.AI.100-1
      https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf  — Core: 4 functions, 19 categories,
      72 subcategories (Tables 1–4).
  S2  NIST AI 800-4, Challenges to the Monitoring of Deployed AI Systems (Mar 2026). doi:10.6028/NIST.AI.800-4
      https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf  — Table 1: 6 monitoring categories;
      Table 3: 19 category-specific gaps and barriers; Table 2: 5 cross-cutting challenge categories
      (13 gaps/barriers); Table 4: 5 open-question themes.
  S3  45 CFR 170.315(b)(11)(iv)(B), as finalized by ONC HTI-1 (89 FR 1192, Jan 9 2024), current eCFR
      text as of 2026-10-01 (last amended 2025-10-01): 9 groups, 31 predictive-DSI source attributes.
      https://www.ecfr.gov/api/versioner/v1/full/2026-10-01/title-45.xml?part=170&section=170.315
  S4  CISA Cybersecurity Performance Goals 2.0 (released Dec 10 2025): 6 functions, 34 goals.
      https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0 (captured live 2026-10-05 via
      browser; archived copy web.archive.org/web/20260928190145 parses to a byte-identical record set).

UNIT:      A source element (one RMF subcategory, one 800-4 category/challenge, one HTI-1 attribute,
           one CPG goal) and a GAP-M control. The crosswalk is the set of control × element links.

MEASURES:
  - Link relationship: NIST IR 8477 (doi:10.6028/NIST.IR.8477) supportive relationship mapping —
    "GAP-M control supports source element", with the IR 8477 property (integral to / example of /
    precedes), a one-sentence rationale, and the control evidence field that carries the proof.
    Use-case documentation per IR 8477 Section 3 in docs/MAPPING_USE_CASE.md.
  - Element disposition: every source element is either mapped (≥1 link) or explicitly marked
    out of monitoring scope with a reason, so coverage is total and auditable.
  - Coverage: share of elements mapped, per framework and per RMF function / CPG function /
    HTI group / 800-4 category; links per control; controls per element.
  - HTI attribute maintenance: for each of the 31 attributes, the control that keeps it current after
    deployment and whether the attribute is static (set at certification) or dynamic (changes with
    monitoring results).

OUTPUTS:
  data/registry/*.csv|json         four source registries, verbatim text, with source locators
  data/crosswalk/gapm_controls.*   the control set (JSON, CSV)
  data/crosswalk/gapm_links.*      long-form crosswalk (JSON, CSV)
  data/crosswalk/gapm_dispositions.csv   every source element with its disposition
  data/crosswalk/gapm_catalog_oscal.json OSCAL 1.x catalog of the control set, with mapping props
  data/crosswalk/GAP-M_crosswalk.xlsx    reviewer workbook
  schema/*.schema.json             JSON Schemas; every JSON output validates
  data/processed/qa_report.txt, report/stats.json, report/figures/*
  report/GAP-M_technical_report.pdf  short technical report built from stats.json

VENUES:    GitHub (TosinClement/gap-m) → Zenodo (dataset, DOI) after verification.
           Later options: arXiv cs.CY, or a response to a NIST/ONC request for information.

VERIFY POINTS (the author rules on these):
  J1  Interpretation of "six monitoring-challenge categories" = AI 800-4 Table 1 categories, with
      Table 3 challenges as sub-elements; Table 2 cross-cutting challenges included as a secondary layer.
  J2  Every control definition (objective, activity, evidence, cadence, owner).
  J3  Every link and its relationship type. All links ship as status "proposed" until accepted.
  J4  Fairness monitoring placement (800-4 has no fairness category; mapped to Functionality and
      Large-Scale Impacts).
  J5  Out-of-scope dispositions (which RMF subcategories and CPG goals are not monitoring controls).
  J6  GAP-M analytic change classes for the 31 HTI attributes (not established by the regulation;
      'dynamic' retired 2026-10-05).
  J7  Necessity audit verdicts and the per-source-kind rules (docs/MAPPING_REVIEW.md).

LICENSE:   Code MIT; data and documents CC BY 4.0. Source texts are U.S. government works.

ASSUMPTIONS (proceeding without confirmation; author can overturn):
  A1  Author block from claude/author-block.md (sole author, Independent Researcher).
  A2  Scope is HTI-1 paragraph (b)(11)(iv)(B) only (the 31 predictive attributes); other (b)(11)
      paragraphs (feedback, risk management) are cited as context, not mapped as elements.
  A3  AI RMF mapped at subcategory level and rolled up to functions.
  A4  The GAP-M control set is a new, original control set authored for this release; it is not a
      NIST, ONC, or CISA product and claims no endorsement.
  A5  Release date and DOI stay as placeholders until the author approves.
```
