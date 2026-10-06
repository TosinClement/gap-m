# Author review record: GAP-M v0.1.0

Status: released 2026-10-05. This file records only the author's own responses, as given. Anything without a response is listed as not individually reviewed.

## Scope so far

Author review: complete. The author individually reviewed all 32 practice definitions, every integral_to link (14), every conditional link (9), a seeded random sample of 66 of the 262 other example_of links (25%, seed 20261005), plus 11 links in targeted checks; ruled on all 32 removals from the earlier AI-assisted review; and spot-checked source text in 4 of the 4 sources. 185 of the 283 current links have not been individually reviewed by the author. Details and the remaining checklist items are in docs/AUTHOR_REVIEW.md.

| Item | Reviewed by the author | Result |
|---|---|---|
| Practice definitions | 32 of 32 | 18 accepted as written, 14 accepted with edits |
| Links in the review set | 100 of 100 | 87 accepted, 11 accepted with reworded text, 2 removed |
| Current links not individually reviewed | 185 of 283 | 16 of these received wording-only consistency edits the author approved |
| Source spot-checks | 4 of 4 sources | ai_rmf: All four match; ai_800_4: All counts match; hti_1: All match; no newer amendment; cpg_2_0: All match |

## Sampling record

- Population: the 262 `example_of` links that were not conditional at the time of the draw (SHA-256 of the sorted ID list: `e73ab392f7e758cf1b409fcd2b5115235165b25434d6aeeee2d48590acf7a0b1`).
- Sample: 66 links (25%, rounded up), seed **20261005**. Seed fixed as the review date before the draw; the draw was run once and not repeated.
- Method: Python random.Random(seed).sample over the sorted list of non-conditional example_of link IDs; selected IDs sorted for presentation. drawn on Python 3.13 (Linux); the same selection reproduced on Python 3.10 (macOS).
- Selected IDs (SHA-256 of the sorted list: `a477ca843e2747e80421ef187258aff49ae73f341013c57f1b7f64807b1422cb`): `GM-CMP-01>CPG:1.A`, `GM-CMP-01>CPG:1.B`, `GM-CMP-02>HTI:B7.iv`, `GM-CMP-02>HTI:B8.ii`, `GM-CMP-02>HTI:B9.ii`, `GM-CMP-03>RMF:MEASURE-2.6`, `GM-FAIR-01>HTI:B7.iv`, `GM-FAIR-02>A84:FUN-B1`, `GM-FAIR-02>HTI:B8.iii`, `GM-FUN-01>A84:FUN-G2`, `GM-FUN-01>HTI:B7.i`, `GM-FUN-01>HTI:B8.ii`, `GM-FUN-02>A84:FUN`, `GM-FUN-02>RMF:MANAGE-2.2`, `GM-FUN-02>RMF:MEASURE-2.5`, `GM-FUN-03>A84:FUN-B1`, `GM-FUN-03>HTI:B4.iv`, `GM-FUN-04>A84:FUN-B2`, `GM-FUN-04>HTI:B8.iv`, `GM-FUN-04>RMF:MAP-2.3`, `GM-FUN-04>RMF:MEASURE-3.2`, `GM-FUN-05>HTI:B9.ii`, `GM-FUN-06>A84:FUN-G2`, `GM-GOV-01>RMF:GOVERN-1.4`, `GM-GOV-01>RMF:GOVERN-1.5`, `GM-GOV-01>RMF:GOVERN-2.1`, `GM-GOV-02>A84:XC-PC-B1`, `GM-GOV-02>CPG:2.A`, `GM-GOV-03>HTI:B6.i`, `GM-GOV-03>HTI:B6.iii`, `GM-GOV-03>HTI:B7.iv`, `GM-GOV-03>RMF:MANAGE-3.2`, `GM-GOV-04>RMF:MANAGE-4.1`, `GM-GOV-05>HTI:B7.v`, `GM-GOV-06>A84:XC-RR-B1`, `GM-GOV-06>RMF:MAP-3.4`, `GM-GOV-07>RMF:MEASURE-2.13`, `GM-HF-01>HTI:B3.ii`, `GM-HF-02>A84:HF-G1`, `GM-HF-02>A84:HF-G2`, `GM-HF-02>HTI:B2.iv`, `GM-HF-02>RMF:MANAGE-4.1`, `GM-HF-02>RMF:MEASURE-2.9`, `GM-HF-03>HTI:B1.iii`, `GM-HF-03>HTI:B6.iii`, `GM-HF-03>HTI:B7.i`, `GM-HF-03>HTI:B7.ii`, `GM-HF-03>HTI:B8.iii`, `GM-HF-03>HTI:B9.ii`, `GM-HF-03>RMF:MAP-2.2`, `GM-HF-03>RMF:MEASURE-2.8`, `GM-LSI-01>A84:LSI-G2`, `GM-LSI-01>HTI:B3.ii`, `GM-LSI-01>RMF:MEASURE-3.1`, `GM-LSI-02>HTI:B7.v`, `GM-OPS-01>A84:FUN-B3`, `GM-OPS-01>A84:OPS`, `GM-OPS-01>RMF:MEASURE-2.4`, `GM-OPS-02>A84:XC-RR-B1`, `GM-OPS-02>RMF:MANAGE-2.1`, `GM-OPS-03>HTI:B9.i`, `GM-OPS-04>RMF:MANAGE-2.1`, `GM-OPS-04>RMF:MEASURE-2.6`, `GM-SEC-01>CPG:4.B`, `GM-SEC-02>CPG:1.D`, `GM-SEC-04>A84:XC-TMT-B3`.

## Practice definitions

| Practice | Response | Edit applied |
|---|---|---|
| GM-GOV-01 | Accept with suggested edit | owner_role: 'approved by the AI governance body' -> 'approved by the AI governance body or equivalent' |
| GM-GOV-02 | Accept with suggested edit | objective: 'current source-attribute record' -> 'a link to or copy of the current source-attribute record' |
| GM-GOV-03 | Accept with suggested edit | objective: 'require timely notice of' -> 'require notice, within contract-defined time frames, of' |
| GM-GOV-04 | Accept as written |  |
| GM-GOV-05 | Accept with suggested edit | objective: added 'and subject to legal and privacy review' to the sharing condition |
| GM-GOV-06 | Accept as written |  |
| GM-GOV-07 | Accept as written |  |
| GM-FUN-01 | Accept with suggested edits | objective: 'developer same-source and external results' -> 'the developer's internal and external validation results'; silent trial 'where feasible' in objective and activity |
| GM-FUN-02 | Accept as written |  |
| GM-FUN-03 | Accept as written |  |
| GM-FUN-04 | Accept with suggested edit | 'ground-truth' -> 'reference-standard' in objective and core (link_audit.yaml cores) |
| GM-FUN-05 | Accept with suggested edit | objective: pre-go-live comparison 'where the organization controls update timing, and otherwise promptly after' |
| GM-FUN-06 | Accept as written |  |
| GM-FAIR-01 | Accept with suggested edit | objective: noted that the (A)(5)-(13) list is given for evidence-based interventions and is used as a reference set |
| GM-FAIR-02 | Accept as written |  |
| GM-OPS-01 | Accept with both edits | objective: store is 'access-controlled, tamper-evident'; inputs 'minimized for protected health information' |
| GM-OPS-02 | Accept as written |  |
| GM-OPS-03 | Accept with suggested edit | objective: 'source attributes' -> 'the organization's source-attribute record' |
| GM-OPS-04 | Accept as written |  |
| GM-HF-01 | Accept as written |  |
| GM-HF-02 | Accept with suggested edit | objective: 'by user role and site' -> 'aggregated by user role and site' |
| GM-HF-03 | Accept as written |  |
| GM-SEC-01 | Accept as written |  |
| GM-SEC-02 | Accept with suggested edit | objective: KEV catalog parenthesis now attached to model-serving software and libraries; 'weaknesses in model artifacts' listed separately |
| GM-SEC-03 | Accept with suggested edit | objective: 'source attributes' -> 'the organization's source-attribute record' |
| GM-SEC-04 | Accept as written |  |
| GM-CMP-01 | Accept as written |  |
| GM-CMP-02 | Accept with suggested edit | cadence: 'before certification or accreditation events' -> 'before accreditation reviews, and after developer certification updates' |
| GM-CMP-03 | Accept as written |  |
| GM-LSI-01 | Accept as written |  |
| GM-LSI-02 | Accept as written |  |
| GM-LSI-03 | Accept as written |  |

## Links in the review set

| Link | Review set | Response | Result | Edit applied |
|---|---|---|---|---|
| `GM-CMP-01>RMF:GOVERN-1.1` | integral_to (all) | Accept | accepted |  |
| `GM-FUN-02>HTI:B8.ii` | integral_to (all) | Accept | accepted |  |
| `GM-FUN-05>RMF:MEASURE-4.3` | integral_to (all) | Accept | accepted |  |
| `GM-FUN-06>RMF:MANAGE-2.4` | integral_to (all) | Accept | accepted |  |
| `GM-GOV-01>RMF:MANAGE-4.1` | integral_to (all) | Accept; tidy audit basis | accepted | audit basis: 'a written plan' -> 'a plan for the system' (link rationale unchanged) |
| `GM-GOV-02>RMF:GOVERN-1.6` | integral_to (all) | Accept; fix rationale | revised | rationale replaced: 'GOVERN 1.6 asks for mechanisms to inventory AI systems; recording deployed AI systems in an inventory is what such a mechanism does.' |
| `GM-GOV-03>CPG:1.D` | integral_to (all) | Accept | accepted |  |
| `GM-HF-01>RMF:MEASURE-3.3` | integral_to (all) | Accept | accepted |  |
| `GM-LSI-01>RMF:MANAGE-4.3` | integral_to (all) | Accept | accepted |  |
| `GM-LSI-03>RMF:MEASURE-3.3` | integral_to (all) | Accept | accepted |  |
| `GM-OPS-01>CPG:3.Q` | integral_to (all) | Accept; narrow core | accepted | GM-OPS-01 core narrowed to logs of AI components 'that the organization operates' (vendor-hosted components fall outside CPG 3.Q's organizational-asset scope) |
| `GM-OPS-03>CPG:3.N` | integral_to (all) | Accept; narrow core | accepted | GM-OPS-03 core narrowed to 'Changes the organization makes to AI models and configuration pass through change control.' |
| `GM-SEC-02>CPG:2.B` | integral_to (all) | Accept | accepted |  |
| `GM-SEC-03>CPG:3.H` | integral_to (all) | Accept | accepted |  |
| `GM-FAIR-02>HTI:B8.iv` | conditional (all) | Accept; correct (A)(5)-(13) phrase | accepted | audit basis: (A)(5)-(13) described as a list for evidence-based interventions that points toward, but does not establish, a group reading |
| `GM-FAIR-02>RMF:MEASURE-2.11` | conditional (all) | Accept; correct (A)(5)-(13) phrase | accepted | audit basis: same (A)(5)-(13) correction as GM-FAIR-02>HTI:B8.iv |
| `GM-FUN-02>RMF:MEASURE-2.4` | conditional (all) | Accept as conditional | accepted |  |
| `GM-FUN-04>HTI:B8.ii` | conditional (all) | Accept as conditional | accepted |  |
| `GM-FUN-06>RMF:MANAGE-1.3` | conditional (all) | Accept; align condition with core | accepted | audit basis and condition now refer to the documented deactivation mechanism (the control's core), not the trigger-action table |
| `GM-GOV-04>CPG:1.C` | conditional (all) | Accept as conditional | accepted |  |
| `GM-HF-03>HTI:B8.ii` | conditional (all) | Accept; soften relevance wording | accepted | relevance basis: 'is how' -> 'is one way' |
| `GM-HF-03>HTI:B8.iv` | conditional (all) | Accept; soften relevance wording | accepted | relevance basis: 'is how' -> 'is one way' |
| `GM-OPS-04>CPG:3.O` | conditional (all) | Accept as conditional | accepted |  |
| `GM-CMP-01>CPG:1.A` | random sample | Accept | accepted |  |
| `GM-CMP-01>CPG:1.B` | random sample | Accept | accepted |  |
| `GM-CMP-02>HTI:B7.iv` | random sample | Accept | accepted |  |
| `GM-CMP-02>HTI:B8.ii` | random sample | Accept | accepted |  |
| `GM-CMP-02>HTI:B9.ii` | random sample | Accept | accepted |  |
| `GM-CMP-03>RMF:MEASURE-2.6` | random sample | Accept | accepted |  |
| `GM-FAIR-01>HTI:B7.iv` | random sample | Accept | accepted |  |
| `GM-FAIR-02>A84:FUN-B1` | random sample | Accept | accepted |  |
| `GM-FAIR-02>HTI:B8.iii` | random sample | Accept | accepted |  |
| `GM-FUN-01>A84:FUN-G2` | random sample | Accept | accepted |  |
| `GM-FUN-01>HTI:B7.i` | random sample | Accept | accepted |  |
| `GM-FUN-01>HTI:B8.ii` | random sample | Accept | accepted |  |
| `GM-FUN-02>A84:FUN` | random sample | Accept | accepted |  |
| `GM-FUN-02>RMF:MANAGE-2.2` | random sample | Accept | accepted |  |
| `GM-FUN-02>RMF:MEASURE-2.5` | random sample | Accept; reword rationale | revised | rationale: 'Ongoing local results show the system stays valid and reliable after deployment.' -> 'Local validity results document how well the system generalizes beyond the conditions under which it was developed.' |
| `GM-FUN-03>A84:FUN-B1` | random sample | Accept | accepted |  |
| `GM-FUN-03>HTI:B4.iv` | random sample | Accept | accepted |  |
| `GM-FUN-04>A84:FUN-B2` | random sample | Accept | accepted |  |
| `GM-FUN-04>HTI:B8.iv` | random sample | Accept | accepted |  |
| `GM-FUN-04>RMF:MAP-2.3` | random sample | Accept | accepted |  |
| `GM-FUN-04>RMF:MEASURE-3.2` | random sample | Accept | accepted |  |
| `GM-FUN-05>HTI:B9.ii` | random sample | Accept | accepted |  |
| `GM-FUN-06>A84:FUN-G2` | random sample | Accept; reword rationale | revised | rationale now attributes the threshold point to practitioners and quotes AI 800-4 p. 18: 'to trigger corrective actions or reviews' |
| `GM-GOV-01>RMF:GOVERN-1.4` | random sample | Accept | accepted |  |
| `GM-GOV-01>RMF:GOVERN-1.5` | random sample | Accept | accepted |  |
| `GM-GOV-01>RMF:GOVERN-2.1` | random sample | Accept | accepted |  |
| `GM-GOV-02>A84:XC-PC-B1` | random sample | Accept | accepted |  |
| `GM-GOV-02>CPG:2.A` | random sample | Accept | accepted |  |
| `GM-GOV-03>HTI:B6.i` | random sample | Accept all three; reword | revised | rationale: 'the notice clause' -> 'the contract's clause requiring notice of new validation results' |
| `GM-GOV-03>HTI:B6.iii` | random sample | Accept all three; reword | revised | rationale: 'the notice clause' -> 'the contract's clause requiring notice of new validation results' |
| `GM-GOV-03>HTI:B7.iv` | random sample | Accept all three; reword | revised | rationale: 'the notice clause' -> 'the contract's clause requiring notice of new validation results' |
| `GM-GOV-03>RMF:MANAGE-3.2` | random sample | Remove | rejected | link removed (recorded in example_review.yaml with scope: author_review, test T2) |
| `GM-GOV-04>RMF:MANAGE-4.1` | random sample | Accept | accepted |  |
| `GM-GOV-05>HTI:B7.v` | random sample | Accept | accepted |  |
| `GM-GOV-06>A84:XC-RR-B1` | random sample | Accept | accepted |  |
| `GM-GOV-06>RMF:MAP-3.4` | random sample | Accept | accepted |  |
| `GM-GOV-07>RMF:MEASURE-2.13` | random sample | Accept | accepted |  |
| `GM-HF-01>HTI:B3.ii` | random sample | Accept | accepted |  |
| `GM-HF-02>A84:HF-G1` | random sample | Accept | accepted |  |
| `GM-HF-02>A84:HF-G2` | random sample | Accept | accepted |  |
| `GM-HF-02>HTI:B2.iv` | random sample | Accept | accepted |  |
| `GM-HF-02>RMF:MANAGE-4.1` | random sample | Accept | accepted |  |
| `GM-HF-02>RMF:MEASURE-2.9` | random sample | Accept | accepted |  |
| `GM-HF-03>HTI:B1.iii` | random sample | Accept all three; reword | revised | rationale: 'the static attribute' -> 'this attribute, which GAP-M classes as set at release' |
| `GM-HF-03>HTI:B6.iii` | random sample | Accept | accepted |  |
| `GM-HF-03>HTI:B7.i` | random sample | Accept all three; reword | revised | rationale: 'the static attribute' -> 'this attribute, which GAP-M classes as set at release' |
| `GM-HF-03>HTI:B7.ii` | random sample | Accept all three; reword | revised | rationale: 'the static attribute' -> 'this attribute, which GAP-M classes as set at release' |
| `GM-HF-03>HTI:B8.iii` | random sample | Accept | accepted |  |
| `GM-HF-03>HTI:B9.ii` | random sample | Accept | accepted |  |
| `GM-HF-03>RMF:MAP-2.2` | random sample | Accept | accepted |  |
| `GM-HF-03>RMF:MEASURE-2.8` | random sample | Accept | accepted |  |
| `GM-LSI-01>A84:LSI-G2` | random sample | Accept | accepted |  |
| `GM-LSI-01>HTI:B3.ii` | random sample | Accept | accepted |  |
| `GM-LSI-01>RMF:MEASURE-3.1` | random sample | Accept | accepted |  |
| `GM-LSI-02>HTI:B7.v` | random sample | Accept | accepted |  |
| `GM-OPS-01>A84:FUN-B3` | random sample | Remove | rejected | link removed (recorded in example_review.yaml with scope: author_review, test T1) |
| `GM-OPS-01>A84:OPS` | random sample | Accept | accepted |  |
| `GM-OPS-01>RMF:MEASURE-2.4` | random sample | Accept | accepted |  |
| `GM-OPS-02>A84:XC-RR-B1` | random sample | Accept | accepted |  |
| `GM-OPS-02>RMF:MANAGE-2.1` | random sample | Accept | accepted |  |
| `GM-OPS-03>HTI:B9.i` | random sample | Accept | accepted |  |
| `GM-OPS-04>RMF:MANAGE-2.1` | random sample | Accept | accepted |  |
| `GM-OPS-04>RMF:MEASURE-2.6` | random sample | Accept | accepted |  |
| `GM-SEC-01>CPG:4.B` | random sample | Accept | accepted |  |
| `GM-SEC-02>CPG:1.D` | random sample | Accept | accepted |  |
| `GM-SEC-04>A84:XC-TMT-B3` | random sample | Accept | accepted |  |
| `GM-GOV-01>RMF:GOVERN-1.2` | targeted check | Accept new rationale | accepted |  |
| `GM-GOV-01>RMF:MEASURE-4.1` | targeted check | Accept new rationale | accepted |  |
| `GM-GOV-02>RMF:MAP-2.1` | targeted check | Accept new rationale | accepted |  |
| `GM-GOV-03>RMF:GOVERN-6.2` | targeted check | Accept new rationale | accepted |  |
| `GM-GOV-03>HTI:B9.i` | targeted check | Accept new rationale | accepted |  |
| `GM-FUN-02>RMF:MEASURE-4.2` | targeted check | Accept new rationale | accepted |  |
| `GM-OPS-01>RMF:MANAGE-4.1` | targeted check | Accept new rationale | accepted |  |
| `GM-OPS-04>RMF:MANAGE-2.4` | targeted check | Accept new rationale | accepted |  |
| `GM-GOV-04>CPG:5.A` | targeted check | Accept | accepted |  |
| `GM-GOV-04>CPG:5.B` | targeted check | Accept; reword to cyber scope | revised | rationale limited to confirmed cybersecurity incidents involving the AI system |
| `GM-GOV-04>CPG:6.A` | targeted check | Accept; replace rationale | revised | rationale replaced: 'Updating the AI annex after each AI incident is one way to refine the incident response plan from lessons learned.' |

## Changes made by the earlier AI-assisted review, ruled on by the author

| Link | Change | Response | Note |
|---|---|---|---|
| `GM-GOV-01>RMF:GOVERN-2.3` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-01>A84:XC-IOC-B1` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-01>CPG:1.A` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-01>CPG:1.B` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-02>HTI:B1.ii` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-02>HTI:B1.iii` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-02>A84:XC-VT-G1` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>RMF:MAP-4.1` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>HTI:B1.i` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>HTI:B5.i` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>HTI:B5.ii` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>HTI:B7.v` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>HTI:B9.ii` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-GOV-03>A84:XC-IOC-B2` | removal | Confirm removal | Answered as one question covering R1-R14: 'Confirm all 14 removals'. |
| `GM-FUN-03>RMF:MAP-2.3` | removal | Confirm R20; keep S20 | Author judged GM-FUN-04's label specification to be documented construct validation (S20 kept) and drift statistics not (R20 removal confirmed). |
| `GM-OPS-02>RMF:MEASURE-2.12` | removal | Confirm; correct the reason | removal basis corrected: dropped the unsourced 'inference energy is marginal' claim; basis now says the control tracks energy cost but does not assess environmental impact |
| `GM-HF-01>A84:HF-G1` | removal | Confirm R24; keep S39 | Author distinguished override/reliance telemetry (S39, kept) from a feedback form (R24, removal confirmed). |
| `GM-GOV-04>RMF:GOVERN-6.2` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-05>A84:LSI-B1` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-05>CPG:5.B` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-06>CPG:3.J` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-07>A84:XC-TMT-G1` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-OPS-02>RMF:MAP-3.2` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-OPS-03>RMF:MANAGE-4.2` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-HF-01>A84:XC-IOC-B3` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-HF-02>RMF:GOVERN-3.2` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-SEC-01>CPG:4.A` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-SEC-02>CPG:2.D` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-SEC-02>CPG:3.S` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-CMP-01>A84:XC-TMT-G1` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-CMP-03>RMF:MANAGE-2.4` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-07>CPG:2.C` | removal | Confirm removal | Answered as one question covering 15 removals in batch 2's table: 'Confirm all 15'. |
| `GM-GOV-01>RMF:GOVERN-1.2` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-GOV-01>RMF:MEASURE-4.1` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-GOV-02>RMF:MAP-2.1` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-GOV-03>RMF:GOVERN-6.2` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-GOV-03>RMF:MANAGE-3.2` | rewording | (no response needed) | Superseded: the author removed this link as S32 earlier on 2026-10-05. |
| `GM-GOV-03>HTI:B9.i` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-FUN-02>RMF:MEASURE-4.2` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-OPS-01>RMF:MANAGE-4.1` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |
| `GM-OPS-04>RMF:MANAGE-2.4` | rewording | Accept new rationale | Answered as one question covering W1-W4 and W6-W9: 'Accept all 8'. |

## Dispositions set by the author

- RMF:MANAGE-3.2: Out of scope. Disposition chosen by the author after removing GM-GOV-03>RMF:MANAGE-3.2 (S32).

## Consistency edits (links still not individually reviewed)

- rationale 'the notice clause' -> 'the contract's clause requiring notice of new validation results'. Author approved applying the S29-S31 wording fix for consistency (2026-10-05). These links were not individually reviewed and remain unreviewed. Links: `GM-GOV-03>HTI:B6.ii`, `GM-GOV-03>HTI:B6.iv`, `GM-GOV-03>HTI:B7.iii`.
- rationale 'the static attribute' -> 'this attribute, which GAP-M classes as set at release'. Author approved applying the S44/S46/S47 wording fix for consistency (2026-10-05). These links were not individually reviewed and remain unreviewed. Links: `GM-HF-03>HTI:B1.i`, `GM-HF-03>HTI:B1.ii`, `GM-HF-03>HTI:B1.iv`, `GM-HF-03>HTI:B2.i`, `GM-HF-03>HTI:B2.ii`, `GM-HF-03>HTI:B2.iii`, `GM-HF-03>HTI:B2.iv`, `GM-HF-03>HTI:B3.i`, `GM-HF-03>HTI:B4.i`, `GM-HF-03>HTI:B4.ii`, `GM-HF-03>HTI:B4.iii`, `GM-HF-03>HTI:B5.i`, `GM-HF-03>HTI:B5.ii`.

## Source spot-checks

- **ai_rmf** (GOVERN 1.4, MAP 1.1, MEASURE 2.4, MANAGE 4.1 against NIST AI 100-1): All four match (2026-10-05).
- **ai_800_4** (Table 1: 6 categories; Table 2: 13 cross-cutting (3 gaps, 10 barriers); Table 3: 19 category items (11 gaps, 8 barriers)): All counts match (2026-10-05).
- **hti_1** (31 attributes in 170.315(b)(11)(iv)(B); (B)(4)(iv), (B)(7)(v), (B)(8)(ii) text; eCFR Timeline shows no amendment after 2025-10-01): All match; no newer amendment (2026-10-05).
- **cpg_2_0** (34 goals; outcome text of 1.D, 3.Q, 4.B on the CISA page): All match (2026-10-05).

## Checklist items still open

- [x] Re-read licensing: all four sources are U.S. government works; nothing restricts redistribution of the quoted text (Checked against 17 U.S.C. 105(a), NIST Technical Series copyright statement, CISA linking policy, and eCFR status page; author approved: NIST worldwide license and credit line added to LICENSE; eCFR non-official status disclosed; Internet Archive snapshot excluded from the release (parsed records committed and hash-verified), 2026-10-05)
- [x] Check every removal from the AI-assisted example_of review (docs/MAPPING_REVIEW.md 5.1; 32 links) and every reworded rationale (5.2; 9 links, 1 of which you later removed) (All 32 removals ruled on (all confirmed; R21's reason corrected) and all 9 rewordings ruled on (8 accepted; 1 superseded by the author's S32 removal), 2026-10-05)
- [x] Spot-check revised (downgraded) necessity links (docs/MAPPING_REVIEW.md section 8). 25 of the 84 fell in your random sample and were reviewed there; decide whether that suffices (Author counted the 24 sampled downgraded links as the spot-check and reviewed the 3 unsampled CPG downgraded links in a targeted check (1 accepted, 2 reworded), 2026-10-05)
- [x] Confirm NIST IR 8477 supportive relationships (supports + integral_to / example_of / precedes) are right for this use case (Checked against NIST IR 8477 section 4.2 (pp. 11-15); usage consistent; author approved three wording fixes (MAPPING_USE_CASE set-theory wording and precedes row; LIMITATIONS item 3 quote), 2026-10-05)
- [x] Revise README, LIMITATIONS, and the technical report in your own voice (Author kept third-person voice, approved edits E1-E4, made no further wording changes, and confirmed review completion (2026-10-05))
- [x] Write ai_statement_final in RELEASE.yaml in your own words, within the scope recorded here; then set author_review: complete (Statement approved and saved; author confirmed review completion and author_review was set to complete (2026-10-05))

## Facts a release statement must stay within

These are counts from this record, not a statement. The author writes `ai_statement_final` in her own words.

- Practice definitions individually reviewed: 32 of 32.
- Links individually reviewed: all 14 integral_to, all 9 conditional, 66 sampled `example_of` links (seed 20261005), and 11 links in targeted checks.
- Earlier AI-review changes ruled on: 32 removals and 9 rewordings.
- Links not individually reviewed: 185 of the current 283.
- Source spot-checks: as listed above; full source verification was done by the automated checks, not by the author.
- The necessity audit and the relevance review of all 210 original `example_of` links were AI-assisted; the author reviewed the subset above.
