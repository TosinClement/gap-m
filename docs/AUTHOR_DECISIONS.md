# Author decisions: GAP-M v0.1.0

Status: released 2026-10-05.

| # | Decision | Options offered | Author's response | Date |
|---|---|---|---|---|
| 1 | How to handle the 9 links whose necessity is unresolved (conditional `example_of`) for v0.1.0 | Keep all 9 conditional (recommended); rule on them one by one; promote some to `integral_to`; remove some | Keep all 9 conditional | 2026-10-05 |
| 2 | Per-source necessity rules and the stricter plausible-alternative standard | Accept both (recommended); accept rules but restore some links; loosen the standard; change a source-kind rule | Accept both | 2026-10-05 |
| 3 | The 32 link removals and the 3 uncovered elements (RMF MAP 3.2, RMF MEASURE 2.12, AI 800-4 XC-IOC-B1) | Accept, gaps to v0.2 (recommended); accept, gaps stay out of scope with no v0.2 plan; restore some removed links; add a control now | Accept; gaps to v0.2 | 2026-10-05 |
| 4A | J1: reading of AI 800-4's "six monitoring-challenge categories" (Table 1 categories, Table 3 challenges beneath, Table 2 secondary) and its application to predictive systems | Accept (recommended); change the reading; narrow the claim to analogies | Accept | 2026-10-05 |
| 4B | J4: fairness placed under Functionality, with Large-Scale Impacts secondary | Accept (recommended); Large-Scale Impacts primary; other placement | Accept | 2026-10-05 |
| 4C | J5: the 9 out-of-scope and 13 prerequisite dispositions | Accept (recommended); accept with exceptions; reject and revisit all | Accept | 2026-10-05 |
| 4D | J6: the four HTI attribute change classes as GAP-M's own analytic classification | Accept (recommended); accept with changes; drop the classes | Accept | 2026-10-05 |
| 5 | Release description | Recommended wording (below); original target sentence without "auditable"; author's own wording | Use recommended wording | 2026-10-05 |

Release description adopted in decision 5 (counts as of the 2026-10-05 build; regenerate if they change). The link count later changed from 285 to 283 when the author removed two links in her guided review; the regenerated wording is in docs/APPROVAL_PACKAGE.md history and the release notes:

> GAP-M v0.1.0: a machine-readable crosswalk linking 32 suggested post-deployment monitoring practices to NIST AI RMF 1.0 subcategories, the six monitoring categories and associated challenges of NIST AI 800-4, the 31 predictive decision support intervention source attributes of 45 CFR 170.315(b)(11)(iv)(B), and CISA Cross-Sector CPG 2.0 goals, with 285 typed, rationale-bearing links and a recorded disposition for every source element. Mapping coverage does not demonstrate compliance or monitoring effectiveness.
| 6 | Release statement (`ai_statement_final`) | Write it after the author's own review (recommended); receive a fill-in outline now; write it now | Write it after my review | 2026-10-05 |

## Still open (the author's own review, not yet done)
- J2: review the 32 control definitions.
- J3: review the links (minimum: every `integral_to` link, every conditional link, and a random 25% of other `example_of` links, with the seed recorded); then set `review_status`.
- Source spot-checks and the remaining items in docs/VERIFY_CHECKLIST.md.
- Write `ai_statement_final` in the author's own words; then set `author_review: complete`.

Until these are done, author review is pending and nothing is published.
