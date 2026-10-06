# Limitations (GAP-M v0.1.0)

Status: released 2026-10-05. Author review complete within the scope in docs/AUTHOR_REVIEW.md. Written before the technical report's discussion section, so the report cannot claim more than this list allows.

1. **Mapping coverage does not demonstrate compliance or effectiveness.** A mapped element has at least one GAP-M control linked to it. That is a property of the crosswalk. It does not show that any organization complies with 45 CFR 170.315(b)(11) or any other rule, achieves an AI RMF outcome, meets a CPG goal, or monitors effectively.

2. **The four sources are different kinds of documents.** The AI RMF is voluntary guidance. NIST AI 800-4 reports monitoring challenges and sets no requirements. 45 CFR 170.315(b)(11)(iv)(B) is a disclosure requirement on certified Health IT Modules. CPG 2.0 is a set of voluntary practices. GAP-M controls are suggested implementation practices. A link means something different for each kind (see docs/MAPPING_USE_CASE.md); reading all links as if they were compliance mappings is a misuse.

3. **The links are expert judgment, not ground truth.** Each link records a reading, drafted with AI assistance, of whether a GAP-M control supports a source element, with a rationale. NIST IR 8477 notes that relationship types and properties "are unlikely to have exactly the same meaning in different mappings because each use case will be different" (p. 12); other experts could reasonably disagree, especially on `example_of` versus `integral_to`. No inter-rater agreement has been measured in v0.1.0.

4. **The author reviewed a defined subset, not every link.** The necessity audit and the relevance review of the original `example_of` links were carried out by the AI assistant with tooling support. In a guided review (docs/AUTHOR_REVIEW.md) the author reviewed all 32 practice definitions; every `integral_to` and conditional link; a seeded random 25% sample of the other `example_of` links; targeted checks of rewordings and of CPG links the audit had downgraded; and every removal made by the AI-assisted review. The author also spot-checked source text in all four sources. Links the author did not review individually (counted in docs/AUTHOR_REVIEW.md) keep `review_status: proposed` and should not be cited as accepted mappings. Nine links whose necessity is unresolved are kept as conditional `example_of` mappings; the author reviewed and accepted each as conditional. Nothing here is independent expert validation.

5. **Downgraded links had a lighter relevance check.** Links the necessity audit downgraded to `example_of` were not included in the separate relevance review of the original `example_of` links. Their relevance rests on the audit's reasoning, on the author's random sample (24 of 82), and on a targeted check of the 3 remaining CPG links.

6. **The control set is original and unvalidated in practice.** GAP-M controls have not been piloted in a health system or any other deploying organization. Cadences and owner roles are illustrative defaults, not tested recommendations.

7. **Coverage fell during review, and some relevant elements are uncovered.** The relevance review removed weak links instead of keeping them for coverage's sake. Elements left without a link are recorded as uncovered (a real gap in GAP-M v0.1.0), prerequisite, or out of scope, each with a reason.

8. **Coverage counts measure mapping breadth, not monitoring sufficiency.** An element counted as "mapped" has at least one supporting control. That does not mean an organization that implements the control has satisfied the element, met the regulation, or achieved the risk outcome.

9. **Regulatory scope is narrow and dated.** The HTI-1 layer covers only the 31 predictive-DSI source attributes in 45 CFR 170.315(b)(11)(iv)(B), as of the eCFR text dated 2026-10-01. The eCFR is an editorial compilation, not an official legal edition of the CFR; for legal purposes, verify against the official CFR and the Federal Register. Other (b)(11) paragraphs (feedback, configuration, intervention risk management in (b)(11)(vi)) are referenced but not mapped as elements. Certification criteria are amended from time to time; any amendment to (b)(11) requires re-running the registry step and reviewing affected links. GAP-M does not interpret obligations under HIPAA, FDA device rules, state AI laws, or payer and accreditor requirements.

10. **HTI-1 obligations fall on certified health IT developers, not deployers.** The regulation requires a Health IT Module to support these attributes. GAP-M uses the attributes as the content a deploying organization's monitoring keeps current. That framing is GAP-M's, not ONC's.

11. **AI 800-4 is a challenges report, not a control framework.** Its categories and gaps describe what practitioners find hard. Mapping a control to a challenge means the control addresses that challenge inside one organization; it does not resolve the research gap AI 800-4 describes.

12. **GAP-M's HTI-1 change classes are analytic.** The regulation does not classify attributes by how they change; its only currency language, (v)(A)(1) "complete and up-to-date", applies to all attributes and binds the Health IT Module. GAP-M's four classes are an interpretive aid and do not affect which practices are necessary.

13. **AI 800-4 has no fairness category.** Fairness monitoring is placed under Functionality, with Large-Scale Impacts as secondary (judgment call J4). Readers who classify fairness differently will see different category counts.

14. **AI RMF is mapped at subcategory level only.** The AI RMF Playbook's suggested actions and the Generative AI Profile (NIST AI 600-1) are not mapped. The crosswalk is written for predictive systems; generative-AI-specific monitoring (for example output content safety) is not covered.

15. **AI 800-4 focuses on generative AI.** The report states that it "is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning" (p. 4, note 4). GAP-M applies its categories and challenges to predictive systems on that basis; a reader who limits AI 800-4 to generative systems would treat the AI 800-4 links as analogies.

16. **The necessity standard is strict.** After the correction passes, a link is `integral_to` only where the source element, as written, cannot be achieved without the control's narrowed core and no plausible alternative exists. A looser standard would restore some downgraded links (docs/MAPPING_REVIEW.md, section 11).

17. **CPG 2.0 goals are mapped to AI-specific controls, not general IT controls.** Several Protect and Identify goals (listed in the QA report) are treated as hosting-environment prerequisites. An organization that has not met them should not read GAP-M coverage as covering them.

18. **Source text extraction has known edge cases.** AI RMF text is parsed from the PDF layout; line-break hyphens are resolved by a documented rule (QA report, section 1). The CPG 2.0 text comes from an archived copy of the CISA page, shown identical to the live page by hash on 2026-10-05; CISA may revise the page without versioning. The archived page itself is not redistributed; the release includes the 34 parsed goal records, verified by hash.

19. **No official status.** GAP-M is independent work. It is not a NIST, ONC/ASTP, or CISA product, and none of these agencies has reviewed or endorsed it.
