# Mapping use case (NIST IR 8477, Section 3)

Status: released 2026-10-05.

NIST IR 8477 asks every concept mapping to document its use case, so readers interpret relationship types in the context they were assigned. This is that documentation for GAP-M v0.1.0.

## Purpose
Give an organization that deploys a predictive AI system one set of post-deployment monitoring controls whose evidence can be shown against four federal references at once. The primary setting is a health system deploying a predictive decision support intervention supplied through certified health IT. The controls are written to work in other sectors too.

## Focal and reference documents
- **Focal document (concept A):** the GAP-M control set (original to this work).
- **Reference documents (concept B):**
  - NIST AI 100-1, AI RMF 1.0: subcategories (72).
  - NIST AI 800-4: monitoring categories (6), category-specific gaps and barriers (19, Table 3), cross-cutting gaps and barriers (13, Table 2).
  - 45 CFR 170.315(b)(11)(iv)(B): predictive-DSI source attributes (31).
  - CISA CPG 2.0: goals (34).

## Relationship style
Supportive relationship mapping. Every link is "GAP-M control **supports** reference element", with one IR 8477 property:

| Property | Meaning in GAP-M |
|---|---|
| `integral_to` | The reference element, as written, cannot be achieved without the control's core activity (for an HTI attribute: a populated, current value cannot be produced without it). |
| `example_of` | The control is one way to achieve the element in whole or in part; other ways exist. |
| `precedes` | The control must be in place before the element can be applied (for example, a control that produces an input every way of applying the element requires). None remain in v0.1.0. Outcome labels were tested as a prerequisite: rejected for local fairness, because output-rate parity uses no labels, and held unresolved for local validity (a conditional link), because label-free accuracy estimation exists but assumes the outcome relationship has not shifted. |

Set-theory relationships (IR 8477: subset of, intersects with, equal, superset of, no relationship) are not used. IR 8477 describes set-theory mapping for comparing similar sets of concepts, and lists supportive relationship mapping for sources that "have different but strongly related concept types" (p. 12). GAP-M controls and the reference elements are different but related concept types (monitoring practices versus outcomes, challenges, and regulatory data elements). IR 8477 makes relationship properties optional; GAP-M assigns one to every link.

## Kinds of source

| Reference | Kind of statement | Who it obligates |
|---|---|---|
| AI RMF 1.0 | Voluntary guidance (risk-management outcomes) | No one |
| NIST AI 800-4 | Report of monitoring challenges (gaps, barriers, open questions) | No one; sets no requirements |
| 45 CFR 170.315(b)(11)(iv)(B) | Regulatory disclosure requirement | The certified Health IT Module and its developer |
| CISA CPG 2.0 | Voluntary practices with recommended actions and scope | No one |
| GAP-M controls | Suggested implementation practices | No one |

A link never turns a voluntary or descriptive source into a requirement, and never makes a deploying organization the holder of an obligation that the regulation places on certified health IT. Mapping coverage does not demonstrate compliance or monitoring effectiveness.

## What "achieving" an element means, per reference
- **AI RMF subcategory:** the organization can show the outcome for the deployed system.
- **AI 800-4 category or challenge:** the control addresses that monitoring challenge in the organization's own program. It does not resolve the research gap.
- **HTI-1 source attribute:** the attribute's value is populated and current for the deployed intervention. This is GAP-M's objective, not the regulatory test. The regulation requires the Health IT Module to support access to complete and up-to-date descriptions ((v)(A)(1)), and allows 11 attributes to be shown as not available ((v)(A)(2)).
- **CPG 2.0 goal:** the goal's outcome holds for the AI system and its monitoring data.

## Necessity audit

Every `integral_to` and `precedes` link must pass a necessity audit against the exact source text: the element, as written, cannot be achieved without the control's one-sentence core activity. The audit applies a rule for each kind of source. Under the AI 800-4 rule no practice is ever necessary, because a challenge has no completion condition. Links whose necessity depends on a fact the author or a deploying organization must supply are `unresolved` and held at `example_of`. The audit lives in `mapping/link_audit.yaml`; the report is `docs/MAPPING_REVIEW.md`. The compiler refuses unaudited necessity claims.

## Dispositions
Every reference element is either linked or given a disposition with a reason:
- `prerequisite`: a baseline practice GAP-M assumes is in place for systems that host the AI.
- `out_of_scope`: a design-time, cultural, or research-governance outcome that monitoring evidence does not demonstrate.
- `uncovered`: relevant to post-deployment monitoring, but no GAP-M v0.1.0 control substantively supports it. This marks a known gap, not a scope decision.

## Relevance review

Every link that was `example_of` from the start was reviewed by the AI assistant for relevance, source interpretation, and unsupported claims. Weak links were removed and not replaced. The record is `mapping/example_review.yaml`. This review is tooling-assisted; it is neither independent expert validation nor the author's review.

## Assumptions
- Links and the necessity audit were drafted with AI assistance. The author is the sole reviewer, and links stay `proposed` until she rules on each.
- Reference text is the verbatim source text in `data/registry/elements.csv`, with the vintages in `data/raw/PROVENANCE.txt`.
- "Deployer" means the organization that operates the AI system in production, which may differ from the developer that certified it.
