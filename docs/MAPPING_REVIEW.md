# GAP-M v0.1.0: mapping review (necessity audit and relevance review)

Status: audit record. Pre-review audit prepared 2026-10-05 with AI assistance; it is not the author's review. The author's review was completed before release, and her rulings are recorded in `data/processed/mapping_review.csv`.

## 1. What was audited and how

Every link that claimed necessity was audited: 107 links, of which 100 were `integral_to` and 7 were `precedes`. The test comes from NIST IR 8477. `integral_to` holds only if the source element, read as written, cannot be achieved without the control's **core** activity. `precedes` holds only if the core must be achieved first. Each control's core is one sentence, listed in `mapping/link_audit.yaml`. Extras in a control's full text never count toward necessity.

The four sources make different kinds of statements, so the test is applied with a rule for each kind:

| Source kind | What it is | Rule applied |
|---|---|---|
| Guidance (AI RMF 1.0) | Voluntary risk-management outcomes | Necessity only where the subcategory's own words name the core activity or an object that cannot exist without it. |
| Monitoring challenge (NIST AI 800-4) | A report of practitioner challenges, gaps, and barriers; categories defined "for example" | Never necessary: a challenge has no completion condition in the source, so a practice can respond to it but cannot be required by it. |
| Regulatory disclosure requirement (45 CFR 170.315(b)(11)(iv)(B)) | Information a certified Health IT Module must support; obligation on the module and its developer | Necessary only where no party other than the deploying organization can produce the value. Even then, necessity is for a populated value, not for certification: (v)(A)(2) allows "not available" for 11 attributes. |
| Voluntary practice (CISA CPG 2.0) | Baseline practices with an outcome, a scope, and a recommended action | Necessary only where the recommended action, within the goal's stated scope, necessarily reaches the AI system. |

Verdicts:
- **supported**: the necessity claim stands.
- **revised**: necessity is not supported. The property becomes `example_of`, and any rationale that implied necessity is reworded.
- **unresolved**: necessity depends on a fact or judgment only the author or a deploying organization can supply. The link is held at `example_of` until the author rules, and the condition under which it would be necessary is stated.

## 2. Summary

| | Supported | Revised | Unresolved | Total |
|---|---|---|---|---|
| Originally `integral_to` | 14 | 78 | 8 | 100 |
| Originally `precedes` | 0 | 6 | 1 | 7 |
| **All audited** | **14** | **84** | **9** | **107** |

| Source kind | Supported | Revised | Unresolved |
|---|---|---|---|
| Guidance (AI RMF 1.0) | 8 | 21 | 3 |
| Monitoring challenge (NIST AI 800-4) | 0 | 31 | 0 |
| Regulatory disclosure requirement (HTI-1) | 1 | 26 | 4 |
| Voluntary practice (CISA CPG 2.0) | 5 | 6 | 2 |

After both reviews (necessity audit, then relevance review), the crosswalk has 14 `integral_to`, 0 `precedes`, and 269 `example_of` links (total 283). The compiler now refuses:
- any `integral_to` or `precedes` link without a supported audit entry (rule R9);
- any audit entry that disagrees with the link (rule R10);
- any `example_of` rationale worded as necessity (rule R11).

## 3. HTI-1 attribute counts, reconciled

The earlier draft classed 16 attributes as `static_at_release`, but its text said "13 attributes set at release are kept by periodic review only." The two counts measured different things. Three set-at-release attributes, (B)(2)(i) intended use, (B)(2)(ii) intended population, and (B)(3)(i) cautioned uses, carried `integral_to` links from GM-CMP-03 (out-of-scope use monitoring), so only 13 had example-only links. The audit downgraded those three links: use monitoring checks conformance to a description, but the description stays accurate whether or not use conforms.

The change classes are now documented as **GAP-M's analytic classification**. The regulation does not sort attributes by how they change. Its only currency language, (v)(A)(1) "complete and up-to-date", applies to every attribute and is a duty of the Health IT Module. The word "dynamic" is retired. Current counts, which sum to 31:

| GAP-M class | Attributes | With integral link | Example-only | May show not available |
|---|---|---|---|---|
| `static_at_release` | 16 | 0 | 16 | 0 |
| `process_description` | 4 | 0 | 4 | 2 |
| `evidence_accruing` | 9 | 0 | 9 | 7 |
| `locally_measured` | 2 | 1 | 1 | 2 |
| **Total** | **31** | **1** | **30** | **11** |

The earlier claim that "all 15 dynamic attributes have an integral control" is withdrawn. It relied on GM-HF-03 (attribute register) being necessary. Under (v)(A)(1), the developer can keep non-local attributes current without the deploying organization, so the register is one route among others. Only the locally measured values (B8.ii) keep necessity links.

## 4. Link ledger (every link of the original build)

| Original property | Original | Kept as is | Changed to `example_of` | Conditional `example_of` (unresolved) | Removed (AI review) | Removed (author) |
|---|---|---|---|---|---|---|
| `integral_to` | 100 | 14 | 77 | 8 | 1 | 0 |
| `precedes` | 7 | 0 | 5 | 1 | 0 | 1 |
| `example_of` | 210 | 178 (8 with reworded rationale) | — | — | 31 | 1 |
| **Total** | **317** | | | | **32** | **2** |

Current crosswalk: 317 − 34 = **283 links** (14 `integral_to`, 0 `precedes`, 269 `example_of`, of which 9 are conditional). The `integral_to` row's single removal is GM-GOV-07>CPG:2.C. The necessity audit had already downgraded it, and the relevance review then found it not substantive.

## 5. Relevance review of the original `example_of` links (tooling-assisted)

Reviewer: AI assistant (tooling-assisted); not independent expert validation; not the author's review. Each of the 210 links that were `example_of` from the start was read against the exact source text and the control's own text, using three tests:
- **T1 relevance:** does the control's stated activity bear on the element as written, not on a neighbouring topic?
- **T2 interpretation:** does the rationale describe the element's subject, phase (design-time or post-deployment), and scope accurately?
- **T3 support:** does the rationale claim anything the control's text does not say?

A link was removed if it failed T1, or failed T2 or T3 in a way a rewording could not fix. Removals were not offset to preserve coverage; an element that lost its only link received a disposition instead.

Result: 170 kept, 9 kept with a reworded rationale, 31 removed. One further link from the audited set was removed for consistency. All 32 removals by failed test: T1 13, T2 7, T3 12.

### 5.1 Removed links

- **`GM-GOV-01>RMF:GOVERN-2.3`** (T3). Monitoring plan and accountable owner → GOVERN 2.3 (NIST AI 100-1, p. 23). GOVERN 2.3 is about executive leadership taking responsibility for AI risk decisions. GM-GOV-01 has the plan approved by 'the AI governance body', not by executive leadership; the rationale's 'executive approval' is not in the control.
- **`GM-GOV-01>A84:XC-IOC-B1`** (T1). Monitoring plan and accountable owner → Balancing competitive pressures with necessary oversight (NIST AI 800-4, Table 2, p. 9). The barrier concerns organizational incentives (competitive pressure versus oversight). A per-system plan does not address incentives; the rationale is speculative.
- **`GM-GOV-01>CPG:1.A`** (T3). Monitoring plan and accountable owner → Establish Cybersecurity Responsibilities (CISA CPG 2.0, goal 1.A). CPG 1.A concerns cybersecurity program roles. GM-GOV-01's RACI covers AI monitoring roles; security monitoring responsibilities are not in the control text.
- **`GM-GOV-01>CPG:1.B`** (T1). Monitoring plan and accountable owner → Manage Cybersecurity Oversight (CISA CPG 2.0, goal 1.B). CPG 1.B concerns the cybersecurity risk management strategy and policies. Sharing an annual review cadence is a coincidence of schedule, not substantive support.
- **`GM-GOV-02>HTI:B1.ii`** (T3). AI system and model inventory → Funding source of the technical implementation for the intervention(s) development (45 CFR 170.315(b)(11)(iv)(B)(1)(ii)). The inventory's listed fields (version, developer, task and output type, sites, inputs, plan, attribute record) do not include funding source.
- **`GM-GOV-02>HTI:B1.iii`** (T3). AI system and model inventory → Description of value that the intervention produces as an output (45 CFR 170.315(b)(11)(iv)(B)(1)(iii)). The inventory records output type, not a description of the value the intervention produces; the attribute is better supported by GM-HF-03.
- **`GM-GOV-02>A84:XC-VT-G1`** (T1). AI system and model inventory → Lack of direct visibility into model properties (NIST AI 800-4, Table 2, p. 9). The gap is lack of visibility into model properties (internals, behavior). A version-level inventory records which system is deployed, not its properties.
- **`GM-GOV-03>RMF:MAP-4.1`** (T1). Developer monitoring obligations in contracts → MAP 4.1 (NIST AI 100-1, p. 27). MAP 4.1 concerns mapping technology and legal risks of components, including intellectual-property infringement. GM-GOV-03 is about notice clauses, not legal risk mapping.
- **`GM-GOV-03>HTI:B1.i`** (T1). Developer monitoring obligations in contracts → Name and contact information for the intervention developer (45 CFR 170.315(b)(11)(iv)(B)(1)(i)). Duplicates GM-GOV-02 and GM-HF-03; a notice clause does not maintain the developer-contact attribute in any way they do not.
- **`GM-GOV-03>HTI:B5.i`** (T3). Developer monitoring obligations in contracts → Description of the approach the intervention developer has taken to ensure that the intervention's output is fair (45 CFR 170.315(b)(11)(iv)(B)(5)(i)). GM-GOV-03's notice obligations list model updates, known-risk changes, validation results, security incidents, and vulnerabilities. Changes to the developer's fairness approach are not among them.
- **`GM-GOV-03>HTI:B5.ii`** (T3). Developer monitoring obligations in contracts → Description of approaches to manage, reduce, or eliminate bias (45 CFR 170.315(b)(11)(iv)(B)(5)(ii)). As for (B)(5)(i): bias-management approaches are not among the control's notice obligations.
- **`GM-GOV-03>HTI:B7.v`** (T3). Developer monitoring obligations in contracts → References to evaluation of use of the intervention on outcomes, including, bibliographic citations or hyperlinks to evaluations of how well the intervention reduced morbidity, mortality, length of stay, or other outcomes (45 CFR 170.315(b)(11)(iv)(B)(7)(v)). Outcome evaluations are not 'validation results' as listed in the control; the rationale extends the clause beyond its text.
- **`GM-GOV-03>HTI:B9.ii`** (T1). Developer monitoring obligations in contracts → Description of frequency by which the intervention's performance is corrected when risks related to validity and fairness are identified (45 CFR 170.315(b)(11)(iv)(B)(9)(ii)). Correction frequency is not something a notice clause produces or checks; the link is too indirect to be substantive.
- **`GM-GOV-03>A84:XC-IOC-B2`** (T2). Developer monitoring obligations in contracts → Lower prioritization for ecosystem-wide transparency (NIST AI 800-4, Table 2, p. 9). The barrier concerns ecosystem-wide transparency. A bilateral contract between one deployer and one developer does not bear on it.
- **`GM-GOV-04>RMF:GOVERN-6.2`** (T3). AI incident response integration → GOVERN 6.2 (NIST AI 100-1, p. 24). The control text does not mention third-party AI failures or contingency processes for them; the rationale adds content the control does not have.
- **`GM-GOV-05>A84:LSI-B1`** (T1). External sharing of monitoring findings → Capturing downstream effects of open-weight models (NIST AI 800-4, Table 3, p. 17). The barrier concerns downstream effects of open-weight model releases, a developer and ecosystem issue. GAP-M addresses deployers of predictive interventions; the link is not substantive.
- **`GM-GOV-05>CPG:5.B`** (T2). External sharing of monitoring findings → Establish Incident Reporting Procedures (CISA CPG 2.0, goal 5.B). CPG 5.B concerns reporting confirmed cybersecurity incidents. Cyber incidents involving AI are already covered through GM-GOV-04; extending 5.B to non-cyber AI findings misreads its scope.
- **`GM-GOV-06>CPG:3.J`** (T3). Monitoring resources and competence → Implement Cybersecurity Training (CISA CPG 2.0, goal 3.J). CPG 3.J is cybersecurity awareness training. GM-GOV-06 trains users on the intervention's intended use and limits; 'misuse and security awareness' is not in the control.
- **`GM-GOV-07>A84:XC-TMT-G1`** (T1). Independent assessment of monitoring → Lack of trusted guidelines or standards for methods and tools (NIST AI 800-4, Table 2, p. 9). An internal independent review does not bear on the field-level absence of trusted standards; the rationale ('makes up in part') is speculative.
- **`GM-FUN-03>RMF:MAP-2.3`** (T2). Input data and population drift detection → MAP 2.3 (NIST AI 100-1, p. 27). MAP 2.3 is a design-time outcome (TEVV considerations identified and documented). Post-deployment drift detection does not identify or document those considerations.
- **`GM-OPS-02>RMF:MEASURE-2.12`** (T1). Service level and cost telemetry → MEASURE 2.12 (NIST AI 100-1, p. 30). MEASURE 2.12 concerns assessing the environmental impact and sustainability of AI model training and management. GM-OPS-02 tracks energy cost but does not assess environmental impact. (Reason corrected by the author on 2026-10-05; the earlier wording relied on an unsourced claim that inference energy is marginal.)
- **`GM-OPS-02>RMF:MAP-3.2`** (T2). Service level and cost telemetry → MAP 3.2 (NIST AI 100-1, p. 27). MAP 3.2 concerns costs that result from AI errors and trustworthiness failures. GM-OPS-02 tracks operating and monitoring costs, which are a different cost.
- **`GM-OPS-03>RMF:MANAGE-4.2`** (T1). Change and configuration control for AI components → MANAGE 4.2 (NIST AI 100-1, p. 33). MANAGE 4.2 concerns measurable continual-improvement activities and engagement. Change control prevents unauthorized change; it does not produce improvement.
- **`GM-HF-01>A84:HF-G1`** (T2). User feedback capture and adjudication → Insufficient research on human-AI feedback loops (NIST AI 800-4, Table 3, p. 17). The gap is insufficient research on human-AI feedback loops. An operational feedback form is not research, and the rationale overstates what it studies.
- **`GM-HF-01>A84:XC-IOC-B3`** (T1). User feedback capture and adjudication → Administrative burden (NIST AI 800-4, Table 2, p. 9). The barrier is the administrative burden of monitoring on organizations. A low-effort feedback button does not bear on it.
- **`GM-HF-02>RMF:GOVERN-3.2`** (T2). Interaction and override telemetry → GOVERN 3.2 (NIST AI 100-1, p. 23). GOVERN 3.2 concerns policies that define roles for human-AI configurations. Telemetry by role does not define or differentiate roles.
- **`GM-SEC-01>CPG:4.A`** (T3). Adversarial input, misuse, and anomalous behavior detection → Establish Malicious Code Detection (CISA CPG 2.0, goal 4.A). CPG 4.A is malicious code detection. GM-SEC-01 detects anomalous inputs and outputs; scanning model files is not in the control.
- **`GM-SEC-02>CPG:2.D`** (T3). Vulnerability management for AI components → Maintain Vulnerability Disclosure/Reporting Process (CISA CPG 2.0, goal 2.D). CPG 2.D is a public vulnerability disclosure route for outside reporters. GM-SEC-02 requires developer disclosure, which is CPG 1.D; the control does not operate a public route.
- **`GM-SEC-02>CPG:3.S`** (T3). Vulnerability management for AI components → Secure Internet Facing Devices (CISA CPG 2.0, goal 3.S). The control does not mention internet-facing assets; whether model endpoints face the internet is deployment-specific.
- **`GM-CMP-01>A84:XC-TMT-G1`** (T1). Requirements register for the deployed system → Lack of trusted guidelines or standards for methods and tools (NIST AI 800-4, Table 2, p. 9). The rationale describes the GAP-M crosswalk itself, not the control. A requirements register does not address the lack of trusted monitoring standards.
- **`GM-CMP-03>RMF:MANAGE-2.4`** (T2). Out-of-scope and policy-violating use monitoring → MANAGE 2.4 (NIST AI 100-1, p. 32). MANAGE 2.4 concerns systems whose performance or outcomes are inconsistent with intended use. Out-of-scope use is a use pattern, not system performance or outcome.
- **`GM-GOV-07>CPG:2.C`** (T1, audited set). Independent assessment of monitoring → Obtain Independent Validation of Cybersecurity Controls (CISA CPG 2.0, goal 2.C). The necessity audit already found that CPG 2.C is third-party validation of cybersecurity defenses and that a review of AI monitoring design is not that activity. The remaining example_of rationale (scheduling alongside) is not substantive support.
- **`GM-GOV-03>RMF:MANAGE-3.2`** (T2). Developer monitoring obligations in contracts → MANAGE 3.2 (NIST AI 100-1, p. 32). Removed by the author in the guided review (2026-10-05). MANAGE 3.2 concerns pre-trained models that an organization uses for development; a deploying organization using a vendor's finished intervention is not using a pre-trained model for development, so the link misread the source.
- **`GM-OPS-01>A84:FUN-B3`** (T1). Central, tamper-protected monitoring logs → Overhead of longitudinal tracking (NIST AI 800-4, Table 3, p. 17). Removed by the author in the guided review (2026-10-05). The barrier is the overhead of longitudinal tracking; central logging is an input to tracking but does not reduce its overhead. FUN-B3 remains covered by GM-FUN-05.

### 5.2 Kept with a reworded rationale

- **`GM-GOV-01>RMF:GOVERN-1.2`** (T2). GOVERN 1.2 concerns organizational policies; a per-system plan is a procedure, not policy. New rationale: "Listing validity, fairness, security, and privacy measures in each monitoring plan is one practice through which trustworthy characteristics enter monitoring procedures."
- **`GM-GOV-01>RMF:MEASURE-4.1`** (T3). The old rationale said the plan records who was consulted; the control does not require consultation. New rationale: "The plan documents the measurement approaches chosen for the specific deployment context."
- **`GM-GOV-02>RMF:MAP-2.1`** (T2). MAP 2.1 is about defining tasks and methods (design time); the inventory records them. New rationale: "The inventory records the defined task and method of each deployed system, keeping that definition visible after deployment."
- **`GM-GOV-03>RMF:GOVERN-6.2`** (T3). 'Remedy clauses' are not in the control. New rationale: "Contractual notice of developer incidents is an input to contingency processes for third-party AI failures."
- **`GM-GOV-03>RMF:MANAGE-3.2`** (T3). 'Brings them into routine monitoring' overstated what a notice does. New rationale: "Notice of changes to the underlying model gives the deployer's routine monitoring a trigger to re-check it."
- **`GM-GOV-03>HTI:B9.i`** (T3). The control is a notice clause; the update process itself is not a contract term in the control. New rationale: "Developer notices of model updates show how often the intervention is actually updated."
- **`GM-FUN-02>RMF:MEASURE-4.2`** (T3). Review by domain experts is not in the control. New rationale: "Local validity results are measurement results on whether the system performs consistently as intended in its deployment context."
- **`GM-OPS-01>RMF:MANAGE-4.1`** (T2). MANAGE 4.1 lists specific mechanisms; logging is not one of them. New rationale: "Logs provide the record that the plan's incident-response and change-management mechanisms rely on."
- **`GM-OPS-04>RMF:MANAGE-2.4`** (T3). 'Deactivation is only safe if a fallback exists' asserted necessity in an example_of rationale. New rationale: "A fallback workflow lets the system be disengaged without interrupting the work it supported."

### 5.3 Kept

170 links passed all three tests unchanged and are listed in `mapping/example_review.yaml` (`keep`), and in the workbook's Links sheet (`example_review = keep`). Default note: "Passes T1–T3: the control's stated activity bears on the element as written, and the rationale matches the source text and the control text." Links kept with a specific caveat:

- `GM-GOV-03>CPG:1.E`: Applies only where the developer hosts or operates the model (conditional on deployment).
- `GM-FAIR-02>A84:LSI`: Depends on judgment call J4 (fairness placed under Functionality with Large-Scale Impacts secondary).
- `GM-HF-02>A84:HF-G1`: Kept, unlike GM-HF-01's link to the same gap: reliance and override trends observed over time are direct evidence about a human-AI feedback loop, not a stand-in for research.
- `GM-CMP-02>HTI:B6.i`: The not-available indication is an obligation of the Health IT Module ((v)(A)(2)); the deployer's audit checks the module's behaviour, it does not meet the obligation.
- `GM-GOV-04>A84:XC-TMT-G1`: Grounded in AI 800-4 section 3.1.1 text on missing guidance for 'what the plan is for when an anomaly is detected'.

### 5.4 Elements left without links

- `RMF:GOVERN-2.3` GOVERN 2.3: **out_of_scope**. Executive leadership responsibility for AI risk decisions is a governance-structure outcome; GAP-M controls name a governance body, not executive accountability.
- `RMF:GOVERN-3.2` GOVERN 3.2: **out_of_scope**. Defining roles for human-AI configurations is a policy-design activity; GAP-M telemetry observes roles but does not define them.
- `RMF:MAP-3.2` MAP 3.2: **uncovered**. Costs that result from AI errors and trustworthiness failures are relevant after deployment, but no GAP-M v0.1.0 control measures them; operating-cost tracking (GM-OPS-02) is a different cost.
- `RMF:MAP-4.1` MAP 4.1: **out_of_scope**. Mapping technology and legal (including intellectual-property) risks of components is a pre-deployment legal-review activity.
- `RMF:MEASURE-2.12` MEASURE 2.12: **uncovered**. No GAP-M v0.1.0 control assesses environmental impact or sustainability.
- `A84:LSI-B1` Capturing downstream effects of open-weight models: **out_of_scope**. Downstream effects of open-weight model releases are a developer and ecosystem matter; GAP-M addresses organizations deploying predictive interventions.
- `A84:XC-IOC-B1` Balancing competitive pressures with necessary oversight: **uncovered**. Balancing competitive pressure against oversight is an incentive problem; no GAP-M v0.1.0 control addresses organizational incentives.
- `CPG:2.C` Obtain Independent Validation of Cybersecurity Controls: **prerequisite**. Third-party validation of cybersecurity defenses (penetration tests, exercises) is a hosting-environment baseline; GAP-M assumes it.
- `CPG:2.D` Maintain Vulnerability Disclosure/Reporting Process: **prerequisite**. A public vulnerability disclosure route is an enterprise baseline; GAP-M assumes it.
- `CPG:3.J` Implement Cybersecurity Training: **prerequisite**. Cybersecurity awareness training is an enterprise baseline; GAP-M's user training covers intended use, not security awareness.
- `CPG:3.S` Secure Internet Facing Devices: **prerequisite**. Securing internet-facing assets is a hosting-environment baseline; whether model endpoints face the internet is deployment-specific.
- `CPG:4.A` Establish Malicious Code Detection: **prerequisite**. Malicious code detection is a hosting-environment baseline; GAP-M assumes it.

## 6. Necessity audit: supported links

These necessity claims stood up in both passes against the narrowed control core and the exact source text. They still need the author's ruling.

#### `GM-GOV-01>RMF:MANAGE-4.1`
- **Author's ruling (guided review):** Accept; tidy audit basis
- **Control:** GM-GOV-01 Monitoring plan and accountable owner. *Core:* A post-deployment monitoring plan covering the system exists.
- **Source (NIST AI 100-1, p. 33; guidance):** "Post-deployment AI system monitoring plans are implemented, including mechanisms for capturing and evaluating input from users and other relevant AI actors, appeal and override, decommissioning, incident response, recovery, and change management."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MANAGE 4.1 reads 'Post-deployment AI system monitoring plans are implemented'; a plan cannot be implemented unless it exists, so a plan for the system is a component of the outcome.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-02>RMF:GOVERN-1.6`
- **Author's ruling (guided review):** Accept; fix rationale
- **Control:** GM-GOV-02 AI system and model inventory. *Core:* Deployed AI systems are recorded in an inventory.
- **Source (NIST AI 100-1, p. 23; guidance):** "Mechanisms are in place to inventory AI systems and are resourced according to organizational risk priorities."
- **Property:** `integral_to` → `integral_to`
- **Basis:** GOVERN 1.6 reads 'Mechanisms are in place to inventory AI systems'; the core (AI systems recorded in an inventory) is what the subcategory names.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: revised)

#### `GM-GOV-03>CPG:1.D`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-03 Developer monitoring obligations in contracts. *Core:* Contracts with the developer require notice of security incidents and vulnerabilities.
- **Source (CISA CPG 2.0, goal 1.D; voluntary practice):** "Outcome: Organizations more rapidly learn about and respond to known incidents or breaches across vendors and service providers | Scope: Third-party vendors and service providers. | Recommended Action: Procurement documents and contracts, such as service-level agreements (SLAs), stipulate that vendors and/or service providers notify the procuring customer of security incidents and vulnerabilities within a risk-informed time frame as determined by the organization.OT: Organizations with OT assets need to document and track serial numbers, checksums, digital certificates/signatures, or other identifying features that can enable them to verify the authenticity of vendor-provided OT hardware, software and firmware."
- **Property:** `integral_to` → `integral_to`
- **Basis:** CPG 1.D's Recommended Action is that contracts 'stipulate that vendors and/or service providers notify the procuring customer of security incidents and vulnerabilities'; Scope is third-party vendors. For the AI developer as vendor, the notice clause is the action itself. Only the security-incident and vulnerability clauses are integral; model-change clauses are extras.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-02>HTI:B8.ii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(ii); disclosure requirement):** "Validity of intervention in local data;"
- **Property:** `integral_to` → `integral_to`
- **Basis:** 'Validity of intervention in local data' can only be produced by measuring validity in the deploying organization's data, which only the deployer (or someone it gives the data to) can do. Scope note: necessary for a populated, current value (GAP-M's objective); (v)(A)(2) lets the module show this attribute as not available, so the control is not necessary for certification.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-05>RMF:MEASURE-4.3`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-05 Longitudinal record and version comparison. *Core:* Performance results from earlier points in time remain available for comparison.
- **Source (NIST AI 100-1, p. 31; guidance):** "Measurable performance improvements or declines based on consultations with relevant AI actors, including affected communities, and field data about context-relevant risks and trustworthiness characteristics are identified and documented."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MEASURE 4.3 requires that 'measurable performance improvements or declines ... are identified and documented'; an improvement or decline is a comparison across time, which needs results retained from more than one point in time. Version comparison is an extra and not integral.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-06>RMF:MANAGE-2.4`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-06 Correction and deactivation triggers. *Core:* A mechanism with assigned authority exists to supersede, disengage, or deactivate the system.
- **Source (NIST AI 100-1, p. 32; guidance):** "Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems that demonstrate performance or outcomes inconsistent with intended use."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MANAGE 2.4 reads 'Mechanisms are in place and applied, and responsibilities are assigned and understood, to supersede, disengage, or deactivate AI systems'; the core (a deactivation mechanism with an assigned authority) is what the subcategory names. Pre-set numeric triggers are extras.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-OPS-01>CPG:3.Q`
- **Author's ruling (guided review):** Accept; narrow core
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (CISA CPG 2.0, goal 3.Q; voluntary practice):** "Outcome: Enhance visibility to detect and respond to cyber incidents while ensuring security logs are protected from unauthorized access and tampering. | Scope: Organizational assets on all assets, where safe and technically feasible. | Recommended Action: Administrative and security-focused logs (e.g., operating systems, applications, and services; intrusion detection systems/intrusion prevention systems; firewalls; data loss prevention; virtual private networks) are collected and stored for use in both detection and incident response activities (e.g., forensics).Logs are stored in a central system, such as a security information and event management tool or central database and can only be accessed or modified by authorized and authenticated users. Logs are stored for a duration informed by risk or pertinent regulatory guidelines.Security teams are notified when a critical log function is disabled.OT: For OT assets where logs are non-standard or not available, network traffic and communications between those assets and other assets is collected."
- **Property:** `integral_to` → `integral_to`
- **Basis:** CPG 3.Q's Recommended Action requires logs from 'operating systems, applications, and services' to be collected, stored centrally with restricted access, and an alert when a critical log function is disabled; its Scope is 'all assets, where safe and technically feasible'. The AI system is an application and service asset, so its logs must be in scope. Inference-level content (input hashes, monitoring results) is an extra.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-OPS-03>CPG:3.N`
- **Author's ruling (guided review):** Accept; narrow core
- **Control:** GM-OPS-03 Change and configuration control for AI components. *Core:* Changes the organization makes to AI models and configuration pass through change control.
- **Source (CISA CPG 2.0, goal 3.N; voluntary practice):** "Outcome: Policies and procedures exist to manage system changes and configurations. | Scope: Organizational assets. | Recommended Action: Implement policies and processes to develop, document, and maintain secure change management for technology platforms and enforce configuration restrictions to prevent unauthorized changes.Technical configuration change control processes are in place, prohibiting unauthorized changes unless approved. Test and document proposed changes in a non-production environment and analyze potential security impacts before implementation.OT: Implement limited functionality by permitting only specific functions, protocols, and services necessary for OT operations."
- **Property:** `integral_to` → `integral_to`
- **Basis:** CPG 3.N's Recommended Action requires change management for technology platforms and configuration change control 'prohibiting unauthorized changes unless approved'; Scope is organizational assets. Model versions and AI configuration are configuration of an organizational asset. Updating the baseline and source attributes after a change is an extra.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-01>RMF:MEASURE-3.3`
- **Author's ruling (guided review):** Accept
- **Control:** GM-HF-01 User feedback capture and adjudication. *Core:* End users can report problems with outputs, and the reports are integrated into monitoring metrics.
- **Source (NIST AI 100-1, p. 31; guidance):** "Feedback processes for end users and impacted communities to report problems and appeal system outcomes are established and integrated into AI system evaluation metrics."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MEASURE 3.3 reads 'Feedback processes for end users ... to report problems ... are established and integrated into AI system evaluation metrics'; the core (end-user problem reporting fed into monitoring metrics) is the end-user half of what the subcategory names. The impacted-community half is GM-LSI-03.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-SEC-02>CPG:2.B`
- **Author's ruling (guided review):** Accept
- **Control:** GM-SEC-02 Vulnerability management for AI components. *Core:* AI software components the organization operates are in its vulnerability management program.
- **Source (CISA CPG 2.0, goal 2.B; voluntary practice):** "Outcome: Reduced likelihood of threat actors exploiting known vulnerabilities to breach organizational networks. | Scope: All organizational assets, to include those that face the internet. | Recommended Action: Implement a vulnerability management program to patch and mitigate misconfigured software in a timely manner.Monitor risk response progress through tools such as plan of action and milestones (POA&M), risk registers, and risk detail reports.Document potential risks of proposed changes and provide rollback guidance. Assign responsibilities and ensure procedures are followed for processing and responding to cybersecurity threats, vulnerabilities, or incident disclosures from various stakeholders. Incorporate compensating security controls (e.g., defense in depth) to address legacy systems, where possible.OT: For assets where patching is either not possible or may substantially compromise availability or safety, compensating controls are applied (e.g., segmentation, monitoring) and recorded. Sufficient controls either make the asset inaccessible from the public internet or reduce the ability of threat actors to exploit the vulnerabilities in these assets."
- **Property:** `integral_to` → `integral_to`
- **Basis:** CPG 2.B's Scope is 'All organizational assets' and its Recommended Action is a vulnerability management program to patch and mitigate software; AI serving software and libraries are organizational software assets. AI-specific weaknesses (beyond CVEs) are an extra.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-SEC-03>CPG:3.H`
- **Author's ruling (guided review):** Accept
- **Control:** GM-SEC-03 Access control over models, configuration, and monitoring data. *Core:* Access to AI configuration and monitoring data follows least privilege.
- **Source (CISA CPG 2.0, goal 3.H; voluntary practice):** "Outcome: Minimizes unauthorized access to systems, data, and processes, reduces human error, and prevents malicious actions; helping ensure the organization's sensitive information and critical assets remain protected. | Scope: All organizational accounts. | Recommended Action: All user accounts, system roles, and processes operate with the minimum privileges necessary to perform their tasks.Perform quarterly reviews of access permissions and role assignments to verify compliance with established policies."
- **Property:** `integral_to` → `integral_to`
- **Basis:** CPG 3.H's Recommended Action is that 'All user accounts, system roles, and processes operate with the minimum privileges necessary' (Scope: all organizational accounts); accounts with access to AI configuration and monitoring data are included.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-CMP-01>RMF:GOVERN-1.1`
- **Author's ruling (guided review):** Accept
- **Control:** GM-CMP-01 Requirements register for the deployed system. *Core:* Applicable AI legal and regulatory requirements are documented.
- **Source (NIST AI 100-1, p. 22; guidance):** "Legal and regulatory requirements involving AI are understood, managed, and documented."
- **Property:** `integral_to` → `integral_to`
- **Basis:** GOVERN 1.1 requires legal and regulatory requirements involving AI to be 'documented'; the core (a documented record of applicable AI requirements, organization-level or system-level) is that documentation. The per-system evidence mapping is an extra.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-LSI-01>RMF:MANAGE-4.3`
- **Author's ruling (guided review):** Accept
- **Control:** GM-LSI-01 AI incident and near-miss log with impact fields. *Core:* AI incidents and errors are recorded.
- **Source (NIST AI 100-1, p. 33; guidance):** "Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MANAGE 4.3 requires processes for 'tracking ... incidents and errors' to be followed and documented; incidents cannot be tracked unless they are recorded. Impact fields are an extra.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-LSI-03>RMF:MEASURE-3.3`
- **Author's ruling (guided review):** Accept
- **Control:** GM-LSI-03 Affected-community engagement and appeals. *Core:* Patients and affected communities have a route to report problems and appeal outcomes, fed into metrics.
- **Source (NIST AI 100-1, p. 31; guidance):** "Feedback processes for end users and impacted communities to report problems and appeal system outcomes are established and integrated into AI system evaluation metrics."
- **Property:** `integral_to` → `integral_to`
- **Basis:** MEASURE 3.3 reads 'Feedback processes for ... impacted communities to report problems and appeal system outcomes are established and integrated into AI system evaluation metrics'; the core of LSI-03 is that route.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

## 7. Necessity audit: unresolved links, kept as conditional `example_of`

For v0.1.0 these are kept as conditional `example_of` mappings and recorded as unresolved. The author reviewed each one and accepted it as a conditional mapping; its necessity stays open. Necessity and relevance are recorded separately. **Necessity** (whether the link should be `integral_to`) is unresolved for every link here, and each entry states the condition under which it would hold. **Relevance** (whether the weaker `example_of` mapping is substantively supported) was assessed on its own, against the exact source text. It is supported for 9 of 9 and unsupported for 0, so no link here has unresolved relevance.

#### `GM-GOV-04>CPG:1.C`
- **Author's ruling (guided review):** Accept as conditional
- **Control:** GM-GOV-04 AI incident response integration. *Core:* The incident response plan addresses AI-specific incidents.
- **Source (CISA CPG 2.0, goal 1.C; voluntary practice):** "Outcome: Identify improvements by practicing cybersecurity and incident response (IR) plans to maintain and update the organization’s cybersecurity program. | Scope: Organization-wide. | Recommended Action: Organizations develop, maintain, update, and regularly exercise IR plans for common and organizationally specific (e.g., by sector, locality) threat scenarios and tactics, techniques, and procedures (TTPs). Ensure drills are realistic and include all relevant stakeholders. IR plans should be reviewed and drilled, at a minimum, on an annual basis.OT: OT IR plans account for specific safety and containment considerations, which differ from existing IT plans and priorities."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 1.C asks for IR plans covering 'common and organizationally specific ... threat scenarios'. Whether compromise of an AI model or its data is an organizationally specific scenario is a risk judgment the deploying organization makes; CPG 1.C also covers only cybersecurity incidents, while GM-GOV-04 adds non-cyber AI incidents.
- **Necessity: unresolved.** Condition for necessity: integral_to for the cybersecurity subset (model or data compromise) if the author judges that subset an organizationally specific threat scenario for the intended deployers.
- **Relevance of the `example_of` mapping: supported.** CPG 1.C's action is to develop and regularly exercise IR plans for 'common and organizationally specific ... threat scenarios'. GM-GOV-04 adds AI scenarios, including compromise of the model or its data, to the IR plan and exercises one annually. The cybersecurity subset of the control is relevant; non-cyber AI incidents are outside CPG 1.C.
- **Current rationale:** Adding AI compromise scenarios to the IR plan is one way to cover organizationally specific threats.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-02>RMF:MEASURE-2.4`
- **Author's ruling (guided review):** Accept as conditional
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (NIST AI 100-1, p. 29; guidance):** "The functionality and behavior of the AI system and its components – as identified in the MAP function – are monitored when in production."
- **Property:** `integral_to` → `example_of`
- **Basis:** MEASURE 2.4 requires functionality and behavior to be 'monitored when in production'. Behavior can be monitored through proxies (output distributions, alert volumes) without outcome-based validity. Whether a predictive system's 'functionality' can be monitored without measuring validity is a judgment about what the system's function is.
- **Necessity: unresolved.** Condition for necessity: integral_to if the author holds that a predictive intervention's functionality is its predictive validity, so production monitoring of functionality entails measuring validity.
- **Relevance of the `example_of` mapping: supported.** MEASURE 2.4 asks that 'the functionality and behavior of the AI system ... are monitored when in production'. Measuring a predictive intervention's validity in local production data is monitoring its functionality.
- **Current rationale:** Measuring validity in production is one way to monitor the system's functionality.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-04>HTI:B8.ii`
- **Author's ruling (guided review):** Accept as conditional
- **Control:** GM-FUN-04 Outcome label acquisition. *Core:* Reference-standard outcome labels are obtained for monitored cases.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(ii); disclosure requirement):** "Validity of intervention in local data;"
- **Property:** `precedes` → `example_of`
- **Basis:** Second pass, as substantiated on 2026-10-05: outcome-based validity measures (discrimination, calibration, positive predictive value) use local outcome labels. Label-free performance estimation exists in the literature: Garg et al. (ICLR 2022, arXiv:2201.04234) propose Average Thresholded Confidence (ATC), which predicts accuracy "as the fraction of unlabeled examples for which model confidence exceeds that threshold" learned on labeled source data. The same paper shows that "absent further assumptions, accuracy on the target is identifiable iff p_t(y|x) is uniquely identified", and names covariate shift (p_s(y|x) = p_t(y|x)) and label shift as conditions under which estimation can work; it estimates accuracy only and was evaluated on image benchmarks. A label-free estimate of local validity therefore rests on an assumption that the outcome relationship has not shifted, which is part of what local validation would test. Whether such an estimate counts as "validity of intervention in local data" is an interpretive question, so the precedes claim is neither supported nor refuted; it is held as unresolved.
- **First pass:** supported (`precedes`); changed in the second pass.
- **Necessity: unresolved.** Condition for necessity: Labels must come first if "validity of intervention in local data" means validity measured against local outcomes, rather than estimated from unlabeled local data under an assumption that p(y|x) is unchanged from the development setting.
- **Relevance of the `example_of` mapping: supported.** (B)(8)(ii) names "Validity of intervention in local data". GM-FUN-04 obtains local outcome labels, which every outcome-based validity measure uses. The control is therefore one substantive way to support the attribute even if labels are not strictly required.
- **Current rationale:** Local outcome labels come first for outcome-based validity measures such as discrimination and calibration; whether every local validity value is label-based is unresolved.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-06>RMF:MANAGE-1.3`
- **Author's ruling (guided review):** Accept; align condition with core
- **Control:** GM-FUN-06 Correction and deactivation triggers. *Core:* A mechanism with assigned authority exists to supersede, disengage, or deactivate the system.
- **Source (NIST AI 100-1, p. 32; guidance):** "Responses to the AI risks deemed high priority, as identified by the MAP function, are developed, planned, and documented. Risk response options can include mitigating, transferring, avoiding, or accepting."
- **Property:** `integral_to` → `example_of`
- **Basis:** MANAGE 1.3 covers responses to risks 'deemed high priority, as identified by the MAP function'. A documented mechanism to supersede, disengage, or deactivate the system (this control's core) is necessary only if performance degradation is among the deploying organization's high-priority risks, which GAP-M cannot know.
- **Necessity: unresolved.** Condition for necessity: integral_to if the author scopes GAP-M to deployments where performance degradation is mapped as high priority (arguably every clinical predictive intervention), so that a documented deactivation mechanism is a necessary response.
- **Relevance of the `example_of` mapping: supported.** MANAGE 1.3 asks that responses to high-priority risks be 'developed, planned, and documented', with options including mitigation. A documented trigger-action table for performance breaches is a planned mitigation response for performance risk.
- **Current rationale:** A trigger-action table is a documented response plan for performance risks the organization rates high priority.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FAIR-02>HTI:B8.iv`
- **Author's ruling (guided review):** Accept; correct (A)(5)-(13) phrase
- **Control:** GM-FAIR-02 Local fairness monitoring. *Core:* Fairness of the intervention is measured in the deploying organization's own data (subgroup performance and output disparities).
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iv); disclosure requirement):** "Fairness of intervention in local data; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** Second pass: 'Fairness of intervention in local data' does not define fairness. Necessity holds only if fairness is read as a comparison across groups (the regulation lists demographic characteristics in (A)(5)–(13) for evidence-based interventions, which points toward, but does not establish, a group reading); individual-fairness measures are an alternative. This is the same condition as GM-FAIR-02>RMF:MEASURE-2.11.
- **First pass:** supported (`integral_to`); changed in the second pass.
- **Necessity: unresolved.** Condition for necessity: integral_to if the author adopts a group-based reading of fairness for (B)(8)(iv).
- **Relevance of the `example_of` mapping: supported.** (B)(8)(iv) is 'Fairness of intervention in local data'. Measuring fairness in the deploying organization's own data produces that value.
- **Current rationale:** Measuring subgroup performance and output disparities in local data is one way to produce the local fairness value.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FAIR-02>RMF:MEASURE-2.11`
- **Author's ruling (guided review):** Accept; correct (A)(5)-(13) phrase
- **Control:** GM-FAIR-02 Local fairness monitoring. *Core:* Fairness of the intervention is measured in the deploying organization's own data (subgroup performance and output disparities).
- **Source (NIST AI 100-1, p. 30; guidance):** "Fairness and bias – as identified in the MAP function – are evaluated and results are documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** Necessity depends on two readings of MEASURE 2.11: that 'evaluated' means evaluated in production on an ongoing basis (the AI RMF asks users to keep applying MEASURE as risks evolve), and that fairness is measured by group comparison (the regulation lists demographic characteristics in (A)(5)-(13) for evidence-based interventions, which points toward, but does not establish, a group reading). Both are defensible; neither is in the subcategory text.
- **Necessity: unresolved.** Condition for necessity: integral_to if the author adopts both readings.
- **Relevance of the `example_of` mapping: supported.** MEASURE 2.11 asks that 'fairness and bias ... are evaluated and results are documented'. Measuring subgroup performance and disparities in production, and documenting breaches, is a fairness evaluation.
- **Current rationale:** Measuring subgroup performance in production is one ongoing fairness evaluation.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-OPS-04>CPG:3.O`
- **Author's ruling (guided review):** Accept as conditional
- **Control:** GM-OPS-04 Fallback and recovery. *Core:* AI artifacts and configuration are backed up and restorable; a fallback workflow exists.
- **Source (CISA CPG 2.0, goal 3.O; voluntary practice):** "Outcome: Organizations reduce data loss and service disruption risks while efficiently managing, responding to, and recovering from incidents to maintain continuous service delivery. | Scope: Organizational assets necessary for business operations. | Recommended Action: Develop a list of all maintained backups, including installation media, license keys, configuration information, and backup retention period of the information.Back up critical operations systems in near-real-time, and frequently back up all systems necessary for operations on a regular schedule consistent with the needs of the organization.Securely store backups offsite and offline. Test backups and recovery on a recurring basis, no less than once per year.Before initiating restoration, validate the integrity of backups and other assets intended for restoration. This verification process is to ensure that data is intact, accurate, and reliable, minimizing the risk of data corruption during the restoration process.Check restoration assets for indicators of compromise, file corruption, and other integrity issues before use.Regularly test backup information to verify media reliability and information integrity.OT: Stored information for OT assets includes, at a minimum, device configurations, roles, engineering drawings, and tools."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 3.O's Scope is 'organizational assets necessary for business operations'. Whether a predictive intervention is such an asset depends on the deployment; GM-OPS-04's own fallback workflow is meant to make the intervention non-essential.
- **Necessity: unresolved.** Condition for necessity: integral_to for the backup-and-restore part if the deploying organization classifies the AI system as necessary for business operations.
- **Relevance of the `example_of` mapping: supported.** CPG 3.O's action includes backing up 'configuration information' and testing recovery for systems necessary for operations. GM-OPS-04 backs up AI artifacts and configuration and tests restore annually, which is that action applied to the AI system. Whether CPG 3.O's scope reaches a given AI system is the open necessity question, not a relevance question.
- **Current rationale:** Backing up model artifacts and configuration applies the backup practice to the AI system.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-03>HTI:B8.ii`
- **Author's ruling (guided review):** Accept; soften relevance wording
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(ii); disclosure requirement):** "Validity of intervention in local data;"
- **Property:** `integral_to` → `example_of`
- **Basis:** Only the deployer holds local data, so some deployer action is necessary for a current local validity value. That action can be recording it in the module under (v)(B)(1) (HF-03) or sending results to the developer to publish. HF-03 is necessary only if the deployer records the value itself.
- **Necessity: unresolved.** Condition for necessity: integral_to if GAP-M specifies that deploying organizations record local values themselves under (v)(B)(1).
- **Relevance of the `example_of` mapping: supported.** (B)(8)(ii) is 'Validity of intervention in local data'. Recording each new local validity result in the attribute record is one way a measured value reaches the record.
- **Current rationale:** Recording each new local validity result is one way the value shown to users stays current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-03>HTI:B8.iv`
- **Author's ruling (guided review):** Accept; soften relevance wording
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iv); disclosure requirement):** "Fairness of intervention in local data; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(8)(ii): deployer action is necessary, but HF-03's recording route is one of two routes.
- **Necessity: unresolved.** Condition for necessity: integral_to if GAP-M specifies that deploying organizations record local values themselves under (v)(B)(1).
- **Relevance of the `example_of` mapping: supported.** (B)(8)(iv) is 'Fairness of intervention in local data'. Recording each new local fairness result in the attribute record is one way a measured value reaches the record.
- **Current rationale:** Recording each new local fairness result is one way the value shown to users stays current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

## 8. Necessity audit: revised links

Necessity not supported; downgraded to `example_of` (one later removed; see section 5). Grouped by source kind.

### Guidance (AI RMF 1.0) (21)

#### `GM-GOV-01>RMF:GOVERN-1.5`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-01 Monitoring plan and accountable owner. *Core:* A post-deployment monitoring plan covering the system exists.
- **Source (NIST AI 100-1, p. 23; guidance):** "Ongoing monitoring and periodic review of the risk management process and its outcomes are planned and organizational roles and responsibilities clearly defined, including determining the frequency of periodic review."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 1.5 concerns monitoring and periodic review of the risk management process and its outcomes, not monitoring of the AI system; a per-system monitoring plan feeds that review but is not required for it.
- **Current rationale:** The plan's review cycle and named roles feed the organization's periodic review of its risk management process.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-01>RMF:GOVERN-2.1`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-01 Monitoring plan and accountable owner. *Core:* A post-deployment monitoring plan covering the system exists.
- **Source (NIST AI 100-1, p. 23; guidance):** "Roles and responsibilities and lines of communication related to mapping, measuring, and managing AI risks are documented and are clear to individuals and teams throughout the organization."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 2.1 asks that AI risk roles be documented and clear 'throughout the organization'; an enterprise governance charter can achieve this without a per-system RACI.
- **Current rationale:** The plan's RACI is one place monitoring roles and lines of communication are documented.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-03>RMF:MANAGE-3.1`
- **Control:** GM-GOV-03 Developer monitoring obligations in contracts. *Core:* Contracts with the developer require notice of security incidents and vulnerabilities.
- **Source (NIST AI 100-1, p. 32; guidance):** "AI risks and benefits from third-party resources are regularly monitored, and risk controls are applied and documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MANAGE 3.1 asks that third-party AI risks be regularly monitored; the deployer can monitor through its own testing (GM-FUN-02, GM-FUN-03) without contractual notice.
- **Current rationale:** Contractual notice of developer changes is one input to regular monitoring of third-party AI risk.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-04>RMF:MANAGE-4.3`
- **Control:** GM-GOV-04 AI incident response integration. *Core:* The incident response plan addresses AI-specific incidents.
- **Source (NIST AI 100-1, p. 33; guidance):** "Incidents and errors are communicated to relevant AI actors, including affected communities. Processes for tracking, responding to, and recovering from incidents and errors are followed and documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MANAGE 4.3 requires processes for tracking, responding to, and recovering from incidents to be followed and documented; a separate AI or patient-safety incident process could satisfy it without an annex to the IR plan.
- **Current rationale:** An AI annex to the IR plan is one documented process for responding to and recovering from AI incidents.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-05>RMF:GOVERN-4.2`
- **Control:** GM-GOV-05 External sharing of monitoring findings. *Core:* A defined policy governs sharing monitoring findings outside the organization.
- **Source (NIST AI 100-1, p. 24; guidance):** "Organizational teams document the risks and potential impacts of the AI technology they design, develop, deploy, evaluate, and use, and they communicate about the impacts more broadly."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 4.2 asks teams to document risks and 'communicate about the impacts more broadly'; broader communication does not require an external findings-sharing policy.
- **Current rationale:** A findings-sharing policy is one way to communicate risks and impacts more broadly.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-05>RMF:GOVERN-4.3`
- **Control:** GM-GOV-05 External sharing of monitoring findings. *Core:* A defined policy governs sharing monitoring findings outside the organization.
- **Source (NIST AI 100-1, p. 24; guidance):** "Organizational practices are in place to enable AI testing, identification of incidents, and information sharing."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 4.3 asks for practices that enable 'information sharing' without saying with whom; internal sharing practices satisfy it without an external policy.
- **Current rationale:** An external sharing policy is one practice that enables information sharing about AI incidents and testing.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-06>RMF:GOVERN-2.2`
- **Control:** GM-GOV-06 Monitoring resources and competence. *Core:* Monitoring has a budget, and monitoring staff and users are trained for the system.
- **Source (NIST AI 100-1, p. 23; guidance):** "The organization’s personnel and partners receive AI risk management training to enable them to perform their duties and responsibilities consistent with related policies, procedures, and agreements."
- **Property:** `integral_to` → `example_of`
- **Basis:** Second pass: GOVERN 2.2 asks for AI risk management training that enables personnel to perform their duties. General AI risk management training could meet it, so system-specific training is not necessary.
- **First pass:** supported (`integral_to`); changed in the second pass.
- **Current rationale:** System-specific training for monitoring staff and users is one form of AI risk management training that enables them to perform their duties.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-06>RMF:MAP-3.4`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-06 Monitoring resources and competence. *Core:* Monitoring has a budget, and monitoring staff and users are trained for the system.
- **Source (NIST AI 100-1, p. 27; guidance):** "Processes for operator and practitioner proficiency with AI system performance and trustworthiness – and relevant technical standards and certifications – are defined, assessed, and documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MAP 3.4 asks that 'processes for operator and practitioner proficiency' be defined, assessed, and documented; proficiency can be established by competency assessment or credentialing instead of training.
- **Current rationale:** System-specific training is one process for establishing operator and practitioner proficiency.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-06>RMF:MANAGE-2.1`
- **Control:** GM-GOV-06 Monitoring resources and competence. *Core:* Monitoring has a budget, and monitoring staff and users are trained for the system.
- **Source (NIST AI 100-1, p. 32; guidance):** "Resources required to manage AI risks are taken into account – along with viable non-AI alternative systems, approaches, or methods – to reduce the magnitude or likelihood of potential impacts."
- **Property:** `integral_to` → `example_of`
- **Basis:** MANAGE 2.1 asks that resources be 'taken into account'; a monitoring budget line is one way, not the only one.
- **Current rationale:** A monitoring budget is one way resources required to manage AI risk are taken into account.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-07>RMF:MEASURE-1.3`
- **Control:** GM-GOV-07 Independent assessment of monitoring. *Core:* Someone independent of the build/operate team periodically assesses the monitoring.
- **Source (NIST AI 100-1, p. 29; guidance):** "Internal experts who did not serve as front-line developers for the system and/or independent assessors are involved in regular assessments and updates. Domain experts, users, AI actors external to the team that developed or deployed the AI system, and affected communities are consulted in support of assessments as necessary per organizational risk tolerance."
- **Property:** `integral_to` → `example_of`
- **Basis:** Second pass: MEASURE 1.3 is met by 'internal experts who did not serve as front-line developers', which includes members of the operating team. GM-GOV-07 excludes the operating team, so its core is sufficient but not necessary.
- **First pass:** supported (`integral_to`); changed in the second pass.
- **Current rationale:** An assessor independent of both the build and operate teams is one way to involve experts who did not serve as front-line developers in regular assessments.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-01>RMF:MEASURE-1.1`
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (NIST AI 100-1, p. 29; guidance):** "Approaches and metrics for measurement of AI risks enumerated during the MAP function are selected for implementation starting with the most significant AI risks. The risks or trustworthiness characteristics that will not – or cannot – be measured are properly documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MEASURE 1.1 asks that measurement approaches be selected and unmeasurable risks documented; this can happen without a local baseline or silent trial.
- **Current rationale:** Choosing baseline metrics, and recording risks left unmeasured, is part of selecting measurement approaches.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-01>RMF:MEASURE-2.3`
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (NIST AI 100-1, p. 29; guidance):** "AI system performance or assurance criteria are measured qualitatively or quantitatively and demonstrated for conditions similar to deployment setting(s). Measures are documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MEASURE 2.3 asks for performance demonstrated 'for conditions similar to deployment setting(s)'; external validation in a similar setting can meet this without a local silent trial.
- **Current rationale:** A local silent trial measures performance under conditions like the deployment setting.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-01>RMF:MANAGE-1.1`
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (NIST AI 100-1, p. 32; guidance):** "A determination is made as to whether the AI system achieves its intended purposes and stated objectives and whether its development or deployment should proceed."
- **Property:** `precedes` → `example_of`
- **Basis:** MANAGE 1.1's go/no-go determination can rest on developer or external evidence; a local baseline is not a prerequisite.
- **Current rationale:** A local baseline informs the determination of whether deployment should proceed.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-02>RMF:MEASURE-3.1`
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (NIST AI 100-1, p. 30; guidance):** "Approaches, personnel, and documentation are in place to regularly identify and track existing, unanticipated, and emergent AI risks based on factors such as intended and actual performance in deployed contexts."
- **Property:** `integral_to` → `example_of`
- **Basis:** MEASURE 3.1 tracks risks 'based on factors such as intended and actual performance'; 'such as' makes performance illustrative, not required.
- **Current rationale:** Local validity results are one factor for tracking emergent risk in the deployed context.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FAIR-01>RMF:MEASURE-2.11`
- **Control:** GM-FAIR-01 Subgroup performance baseline. *Core:* Subgroup performance is evaluated before deployment.
- **Source (NIST AI 100-1, p. 30; guidance):** "Fairness and bias – as identified in the MAP function – are evaluated and results are documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MEASURE 2.11 requires fairness to be 'evaluated and results ... documented' without saying when or in whose data; developer evaluation can satisfy it, so a deployer pre-deployment baseline is not required.
- **Current rationale:** A local subgroup baseline is one documented fairness evaluation.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-OPS-01>RMF:MEASURE-2.4`
- **Author's ruling (guided review):** Accept
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (NIST AI 100-1, p. 29; guidance):** "The functionality and behavior of the AI system and its components – as identified in the MAP function – are monitored when in production."
- **Property:** `precedes` → `example_of`
- **Basis:** Production monitoring can query source data directly; a central protected log store is not a prerequisite.
- **Current rationale:** Central logs are one data source for production monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-01>RMF:GOVERN-5.2`
- **Control:** GM-HF-01 User feedback capture and adjudication. *Core:* End users can report problems with outputs, and the reports are integrated into monitoring metrics.
- **Source (NIST AI 100-1, p. 24; guidance):** "Mechanisms are established to enable the team that developed or deployed AI systems to regularly incorporate adjudicated feedback from relevant AI actors into system design and implementation."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 5.2 asks for mechanisms to incorporate adjudicated feedback 'from relevant AI actors' into design and implementation; adjudicated feedback from other actors (external reviewers, auditors) can satisfy it, and HF-01 feeds metrics, not design.
- **Current rationale:** Adjudicated end-user feedback is one stream a team can incorporate into design and implementation.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-01>RMF:MANAGE-4.1`
- **Control:** GM-HF-01 User feedback capture and adjudication. *Core:* End users can report problems with outputs, and the reports are integrated into monitoring metrics.
- **Source (NIST AI 100-1, p. 33; guidance):** "Post-deployment AI system monitoring plans are implemented, including mechanisms for capturing and evaluating input from users and other relevant AI actors, appeal and override, decommissioning, incident response, recovery, and change management."
- **Property:** `integral_to` → `example_of`
- **Basis:** Second pass: MANAGE 4.1 names 'mechanisms for capturing and evaluating input from users'. Periodic user surveys or interviews capture and evaluate user input without a problem-reporting route, so HF-01's core is not necessary.
- **First pass:** supported (`integral_to`); changed in the second pass.
- **Current rationale:** An in-workflow problem-reporting route is one mechanism for capturing and evaluating input from users.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>RMF:MAP-2.2`
- **Author's ruling (guided review):** Accept
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (NIST AI 100-1, p. 26; guidance):** "Information about the AI system’s knowledge limits and how system output may be utilized and overseen by humans is documented. Documentation provides sufficient information to assist relevant AI actors when making decisions and taking subsequent actions."
- **Property:** `integral_to` → `example_of`
- **Basis:** MAP 2.2 asks that knowledge limits and appropriate use be documented sufficiently for decision-makers; developer documentation or other user guidance can satisfy it without a deployer-maintained attribute register.
- **Current rationale:** A current source-attribute record is one form of documentation of knowledge limits and appropriate use.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-LSI-03>RMF:MAP-5.2`
- **Control:** GM-LSI-03 Affected-community engagement and appeals. *Core:* Patients and affected communities have a route to report problems and appeal outcomes, fed into metrics.
- **Source (NIST AI 100-1, p. 28; guidance):** "Practices and personnel for supporting regular engagement with relevant AI actors and integrating feedback about positive, negative, and unanticipated impacts are in place and documented."
- **Property:** `integral_to` → `example_of`
- **Basis:** MAP 5.2 asks for engagement with 'relevant AI actors'; engagement with affected communities specifically is not required by the text.
- **Current rationale:** Engagement with affected communities is one practice for regular engagement with relevant AI actors.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-LSI-03>RMF:GOVERN-5.1`
- **Control:** GM-LSI-03 Affected-community engagement and appeals. *Core:* Patients and affected communities have a route to report problems and appeal outcomes, fed into metrics.
- **Source (NIST AI 100-1, p. 24; guidance):** "Organizational policies and practices are in place to collect, consider, prioritize, and integrate feedback from those external to the team that developed or deployed the AI system regarding the potential individual and societal impacts related to AI risks."
- **Property:** `integral_to` → `example_of`
- **Basis:** GOVERN 5.1 asks for feedback from 'those external to the team'; clinician users and external reviewers are also external to the team, so a patient-facing route is not required.
- **Current rationale:** A patient and community reporting route is one way to collect feedback from people external to the team.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

### Monitoring challenge (NIST AI 800-4) (31)

#### `GM-GOV-05>A84:XC-VT-G2`
- **Control:** GM-GOV-05 External sharing of monitoring findings. *Core:* A defined policy governs sharing monitoring findings outside the organization.
- **Source (NIST AI 800-4, Table 2, p. 9; monitoring challenge):** "Immature information sharing ecosystem"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule: a challenge has no completion condition, so no control is necessary to it.
- **Current rationale:** Deployers sharing findings is one contribution to a more mature information-sharing ecosystem.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-06>A84:XC-RR-B1`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-06 Monitoring resources and competence. *Core:* Monitoring has a budget, and monitoring staff and users are trained for the system.
- **Source (NIST AI 800-4, Table 2, p. 9; monitoring challenge):** "Financial costs and compute/human resources"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** A monitoring budget makes financial, compute, and human resource costs explicit.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-01>A84:FUN-G2`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Establishing performance baselines and thresholds"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Recording a local baseline with deviation thresholds is one response to the baseline-and-threshold gap.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-01>A84:FUN`
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system continue to work as intended? Measuring system functions, capabilities, and features, for example to ensure the system continues to work as intended"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule; the category is defined 'for example'.
- **Current rationale:** A baseline is one reference point for functionality monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-02>A84:FUN-B1`
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Detecting performance degradation and drift"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Measuring local validity over time is one way to detect performance degradation.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-02>A84:FUN`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system continue to work as intended? Measuring system functions, capabilities, and features, for example to ensure the system continues to work as intended"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Local validity monitoring is one form of functionality monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-03>A84:FUN-B1`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-03 Input data and population drift detection. *Core:* Input data and population mix are compared against a reference distribution.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Detecting performance degradation and drift"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Input drift detection is one way to detect drift before outcome labels arrive.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-04>A84:FUN-B2`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-04 Outcome label acquisition. *Core:* Reference-standard outcome labels are obtained for monitored cases.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Missing high-quality ground truth datasets"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** A label specification with adjudication is one response to missing ground truth.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-05>A84:FUN-G1`
- **Control:** GM-FUN-05 Longitudinal record and version comparison. *Core:* Performance results from earlier points in time remain available for comparison.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Lack of systematic model comparison"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Same-data comparison of model versions is one form of systematic model comparison.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-05>A84:FUN-B3`
- **Control:** GM-FUN-05 Longitudinal record and version comparison. *Core:* Performance results from earlier points in time remain available for comparison.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Overhead of longitudinal tracking"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** A retained time series is one way to lower the overhead of longitudinal tracking.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-OPS-01>A84:OPS-B1`
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Fragmented logging across distributed infrastructure"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule; a federated query layer is another answer.
- **Current rationale:** A central log store is one answer to fragmented logging across distributed infrastructure.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-OPS-01>A84:OPS`
- **Author's ruling (guided review):** Accept
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system maintain consistent service across its infrastructure? Measuring system infrastructure components, for example to ensure the system maintains consistent levels of service"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Complete logs are one basis for infrastructure-level monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-OPS-01>A84:HF-G5`
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Underutilization of telemetry data"
- **Property:** `precedes` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Captured logs are one source of telemetry to put to use.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-OPS-01>A84:FUN-B3`
- **Author's ruling (guided review):** Remove
- **Control:** GM-OPS-01 Central, tamper-protected monitoring logs. *Core:* Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Overhead of longitudinal tracking"
- **Property:** `precedes` → `removed`
- **Basis:** AI 800-4 rule.
- **Current rationale:** (removed in the relevance review; see section 5)
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: removed)

#### `GM-OPS-02>A84:OPS-G1`
- **Control:** GM-OPS-02 Service level and cost telemetry. *Core:* Service levels and indirect costs of the AI system are tracked.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Tracking indirect costs beyond compute"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Tracking reviewer time, labeling, and energy is one way to track indirect costs beyond compute.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-OPS-02>A84:OPS`
- **Control:** GM-OPS-02 Service level and cost telemetry. *Core:* Service levels and indirect costs of the AI system are tracked.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system maintain consistent service across its infrastructure? Measuring system infrastructure components, for example to ensure the system maintains consistent levels of service"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Service-level monitoring is one form of operational monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-01>A84:HF-B1`
- **Control:** GM-HF-01 User feedback capture and adjudication. *Core:* End users can report problems with outputs, and the reports are integrated into monitoring metrics.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Overhead of collecting and gauging user feedback"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Low-effort in-workflow capture is one way to reduce the overhead of collecting user feedback.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-01>A84:HF`
- **Control:** GM-HF-01 User feedback capture and adjudication. *Core:* End users can report problems with outputs, and the reports are integrated into monitoring metrics.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Is the system transparent to humans and high quality? Measuring human-system interactions, for example to ensure the system produces high-quality outputs and is transparent"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** User feedback is one measure of human-system interaction.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-02>A84:HF-G3`
- **Control:** GM-HF-02 Interaction and override telemetry. *Core:* User interactions with outputs are measured.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Limited understanding of user interaction and behavior"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Interaction telemetry is one way to understand user interaction and behavior.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-02>A84:HF-G5`
- **Control:** GM-HF-02 Interaction and override telemetry. *Core:* User interactions with outputs are measured.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Underutilization of telemetry data"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Interaction reporting is one way to use telemetry that would otherwise sit unused.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-02>A84:HF-G4`
- **Control:** GM-HF-02 Interaction and override telemetry. *Core:* User interactions with outputs are measured.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Lack of insight into characteristics of system users"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Results by role, specialty, and site give some insight into the characteristics of system users.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-SEC-01>A84:SEC-B1`
- **Control:** GM-SEC-01 Adversarial input, misuse, and anomalous behavior detection. *Core:* AI-specific anomalous or adversarial behavior is detected.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Detecting deceptive behavior"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Comparing production with evaluation behavior is one check for deceptive behavior.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-SEC-01>A84:SEC`
- **Control:** GM-SEC-01 Adversarial input, misuse, and anomalous behavior detection. *Core:* AI-specific anomalous or adversarial behavior is detected.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Is the system secure against attacks and misuse? Measuring where the system is potentially vulnerable to adversarial attacks and misuse"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Detecting attack and misuse attempts is one form of security monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-SEC-04>A84:XC-TMT-B3`
- **Author's ruling (guided review):** Accept
- **Control:** GM-SEC-04 Privacy-preserving handling of monitoring data. *Core:* Monitoring data are handled with privacy protections.
- **Source (NIST AI 800-4, Table 2, p. 9; monitoring challenge):** "Monitoring may infringe security and privacy"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Privacy-preserving handling of monitoring data is one response to the concern that monitoring may infringe privacy.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-CMP-01>A84:CMP-B1`
- **Control:** GM-CMP-01 Requirements register for the deployed system. *Core:* Applicable AI legal and regulatory requirements are documented.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Navigating the complexity of the policy landscape"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** A maintained requirements register is one tool for navigating a complex policy landscape.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-CMP-01>A84:CMP`
- **Control:** GM-CMP-01 Requirements register for the deployed system. *Core:* Applicable AI legal and regulatory requirements are documented.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system adhere to relevant regulations and directives? Measuring system components for adherence to relevant laws, regulations, standards, controls, and guidelines"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** A requirements register lists the obligations compliance monitoring measures against.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-CMP-03>A84:CMP-G1`
- **Control:** GM-CMP-03 Out-of-scope and policy-violating use monitoring. *Core:* Use of the system is checked against its documented intended scope.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Minimal tracking of terms of service violations"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Flagging use against terms and cautioned uses is one way to track terms-of-service violations.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-LSI-01>A84:LSI-G2`
- **Author's ruling (guided review):** Accept
- **Control:** GM-LSI-01 AI incident and near-miss log with impact fields. *Core:* AI incidents and errors are recorded.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Capturing large-scale impacts within incident logging"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Impact fields are one way to capture large-scale impacts in incident logging.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-LSI-01>A84:LSI`
- **Control:** GM-LSI-01 AI incident and near-miss log with impact fields. *Core:* AI incidents and errors are recorded.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system promote human flourishing? Measuring system properties that have wide downstream impacts, for example to ensure the system promotes human flourishing"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Aggregated impact data are one measure of wide downstream effects.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-LSI-02>A84:LSI-G1`
- **Control:** GM-LSI-02 Outcome and benefit measurement. *Core:* Benefit measures are defined and tracked.
- **Source (NIST AI 800-4, Table 3, p. 17; monitoring challenge):** "Defining metrics for beneficial impacts to humans"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Defining benefit measures is one response to the gap in metrics for beneficial impacts.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-LSI-02>A84:LSI`
- **Control:** GM-LSI-02 Outcome and benefit measurement. *Core:* Benefit measures are defined and tracked.
- **Source (NIST AI 800-4, Table 1, p. 6; monitoring challenge):** "Does the system promote human flourishing? Measuring system properties that have wide downstream impacts, for example to ensure the system promotes human flourishing"
- **Property:** `integral_to` → `example_of`
- **Basis:** AI 800-4 rule.
- **Current rationale:** Population-level benefit measures are one form of large-scale impact monitoring.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

### Regulatory disclosure requirement (HTI-1) (26)

#### `GM-GOV-01>HTI:B8.i`
- **Control:** GM-GOV-01 Monitoring plan and accountable owner. *Core:* A post-deployment monitoring plan covering the system exists.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(i); disclosure requirement):** "Description of process and frequency by which the intervention's validity is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(8)(i) requires a description of the process and frequency of validity monitoring; the regulation does not say who monitors, and the description can describe the developer's process. A deployer plan is not required to produce it.
- **Current rationale:** Where the deploying organization runs validity monitoring, its plan is the process the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-GOV-01>HTI:B8.iii`
- **Control:** GM-GOV-01 Monitoring plan and accountable owner. *Core:* A post-deployment monitoring plan covering the system exists.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iii); disclosure requirement):** "Description of the process and frequency by which the intervention's fairness is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** Same as (B)(8)(i): the fairness-monitoring description can describe any party's process.
- **Current rationale:** Where the deploying organization runs fairness monitoring, its plan is the process the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-01>HTI:B8.ii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-01 Performance baseline and deviation thresholds. *Core:* A pre-deployment local baseline with deviation thresholds is recorded.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(ii); disclosure requirement):** "Validity of intervention in local data;"
- **Property:** `precedes` → `example_of`
- **Basis:** (B)(8)(ii) is the value of validity in local data; measuring it needs no baseline (judging it against thresholds does).
- **Current rationale:** A baseline gives the local validity value a reference for interpretation.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-02>HTI:B8.i`
- **Control:** GM-FUN-02 Local validity monitoring. *Core:* Validity is measured in the deploying organization's own data.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(i); disclosure requirement):** "Description of process and frequency by which the intervention's validity is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** The process description can describe any party's monitoring process.
- **Current rationale:** Where the deploying organization runs it, local validity monitoring is the process the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FUN-03>HTI:B4.iv`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-03 Input data and population drift detection. *Core:* Input data and population mix are compared against a reference distribution.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(4)(iv); disclosure requirement):** "Description of relevance of training data to intended deployed setting; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(4)(iv) is a description of relevance of training data to the 'intended deployed setting', a developer statement; drift monitoring tests it locally but is not needed to produce or maintain it. GAP-M's 'evidence_accruing' class for this attribute is an analytic choice, not source text.
- **Current rationale:** Drift monitoring gives local evidence on whether the training-data relevance statement holds.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-04>HTI:B8.iv`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FUN-04 Outcome label acquisition. *Core:* Reference-standard outcome labels are obtained for monitored cases.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iv); disclosure requirement):** "Fairness of intervention in local data; and"
- **Property:** `precedes` → `example_of`
- **Basis:** Second pass: fairness measures such as demographic or output-rate parity compare outputs across groups and need no outcome labels, so obtaining labels is not a prerequisite for every local fairness value. The precedes claim holds only for label-dependent measures and is downgraded.
- **First pass:** supported (`precedes`); changed in the second pass.
- **Current rationale:** For label-dependent fairness measures such as subgroup calibration or error-rate parity, local outcome labels come first; label-free measures such as output-rate parity can be computed without them.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-FUN-06>HTI:B9.ii`
- **Control:** GM-FUN-06 Correction and deactivation triggers. *Core:* A mechanism with assigned authority exists to supersede, disengage, or deactivate the system.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(9)(ii); disclosure requirement):** "Description of frequency by which the intervention's performance is corrected when risks related to validity and fairness are identified."
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(9)(ii) describes how often performance is corrected; it can describe the developer's correction practice, so deployer triggers are not required to produce it.
- **Current rationale:** Deployer triggers show how often performance is corrected locally, which the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-FAIR-02>HTI:B8.iii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-FAIR-02 Local fairness monitoring. *Core:* Fairness of the intervention is measured in the deploying organization's own data (subgroup performance and output disparities).
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iii); disclosure requirement):** "Description of the process and frequency by which the intervention's fairness is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** The process description can describe any party's monitoring process.
- **Current rationale:** Where the deploying organization runs it, local fairness monitoring is the process the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-OPS-03>HTI:B9.i`
- **Author's ruling (guided review):** Accept
- **Control:** GM-OPS-03 Change and configuration control for AI components. *Core:* Changes the organization makes to AI models and configuration pass through change control.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(9)(i); disclosure requirement):** "Description of process and frequency by which the intervention is updated; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(9)(i) describes the update process and frequency; it can describe the developer's process.
- **Current rationale:** The deployer's change process is one update process the attribute can describe.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-03>HTI:B3.ii`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(3)(ii); disclosure requirement):** "Known risks, inappropriate settings, inappropriate uses, or known limitations."
- **Property:** `integral_to` → `example_of`
- **Basis:** The developer can update known risks under (v)(A)(1); deployer recording under (v)(B)(1) is one route, not the only one.
- **Current rationale:** Recording newly found risks and limitations is one way the deploying organization keeps this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B4.iv`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(4)(iv); disclosure requirement):** "Description of relevance of training data to intended deployed setting; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** Developer statement about the intended deployed setting; the developer can keep it current. The 'evidence_accruing' class is GAP-M's analytic choice.
- **Current rationale:** Recording local drift findings is one way to keep the relevance statement accurate.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B6.i`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(6)(i); disclosure requirement):** "Description of the data source, clinical setting, or environment where an intervention's validity and fairness has been assessed, other than the source of training and testing data"
- **Property:** `integral_to` → `example_of`
- **Basis:** External validation descriptions are developer-held; the developer can keep them current under (v)(A)(1).
- **Current rationale:** Updating the record when a new external validation appears is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B6.ii`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(6)(ii); disclosure requirement):** "Party that conducted the external testing;"
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(6)(i).
- **Current rationale:** Updating the record when a new external validation appears is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B6.iii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(6)(iii); disclosure requirement):** "Description of demographic representativeness of external data according to variables in paragraph (b)(11)(iv)(A)(5)-(13) including, at a minimum, those used as input features in the intervention; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(6)(i).
- **Current rationale:** Updating the record when a new external validation appears is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-03>HTI:B6.iv`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(6)(iv); disclosure requirement):** "Description of external validation process."
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(6)(i).
- **Current rationale:** Updating the record when a new external validation appears is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B7.iii`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(7)(iii); disclosure requirement):** "Validity of intervention in data external to or from a different source than the initial training data;"
- **Property:** `integral_to` → `example_of`
- **Basis:** Developer-held external result; the developer can keep it current.
- **Current rationale:** Updating the record when new external validity results appear is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B7.iv`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(7)(iv); disclosure requirement):** "Fairness of intervention in data external to or from a different source than the initial training data;"
- **Property:** `integral_to` → `example_of`
- **Basis:** Developer-held external result; the developer can keep it current.
- **Current rationale:** Updating the record when new external fairness results appear is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B7.v`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(7)(v); disclosure requirement):** "References to evaluation of use of the intervention on outcomes, including, bibliographic citations or hyperlinks to evaluations of how well the intervention reduced morbidity, mortality, length of stay, or other outcomes;"
- **Property:** `integral_to` → `example_of`
- **Basis:** References can cite evaluations the developer tracks.
- **Current rationale:** Adding new outcome evaluations to the record is one way to keep this attribute current.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B8.i`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(i); disclosure requirement):** "Description of process and frequency by which the intervention's validity is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** The process description may describe the developer's process.
- **Current rationale:** Keeping the displayed process description in line with the process actually run is one way to keep this attribute accurate.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B8.iii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(8)(iii); disclosure requirement):** "Description of the process and frequency by which the intervention's fairness is monitored over time;"
- **Property:** `integral_to` → `example_of`
- **Basis:** The process description may describe the developer's process.
- **Current rationale:** Keeping the displayed process description in line with the process actually run is one way to keep this attribute accurate.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-HF-03>HTI:B9.i`
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(9)(i); disclosure requirement):** "Description of process and frequency by which the intervention is updated; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** The update-process description may describe the developer's process.
- **Current rationale:** Keeping the displayed update process in line with practice is one way to keep this attribute accurate.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-HF-03>HTI:B9.ii`
- **Author's ruling (guided review):** Accept
- **Control:** GM-HF-03 Source-attribute currency and user transparency. *Core:* The deploying organization updates the source-attribute record when an underlying fact changes.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(9)(ii); disclosure requirement):** "Description of frequency by which the intervention's performance is corrected when risks related to validity and fairness are identified."
- **Property:** `integral_to` → `example_of`
- **Basis:** The correction-frequency description may describe the developer's practice.
- **Current rationale:** Keeping the displayed correction frequency in line with practice is one way to keep this attribute accurate.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-CMP-03>HTI:B2.i`
- **Control:** GM-CMP-03 Out-of-scope and policy-violating use monitoring. *Core:* Use of the system is checked against its documented intended scope.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(2)(i); disclosure requirement):** "Intended use of the intervention;"
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(2)(i) is a description of intended use; use monitoring checks conformance to it but the description stays accurate whether or not use conforms.
- **Current rationale:** Use monitoring checks actual use against the stated intended use.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-CMP-03>HTI:B2.ii`
- **Control:** GM-CMP-03 Out-of-scope and policy-violating use monitoring. *Core:* Use of the system is checked against its documented intended scope.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(2)(ii); disclosure requirement):** "Intended patient population(s) for the intervention's use;"
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(2)(i): the intended-population description does not depend on monitoring actual patients.
- **Current rationale:** Use monitoring checks the patients the intervention runs on against the stated intended population.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-CMP-03>HTI:B3.i`
- **Control:** GM-CMP-03 Out-of-scope and policy-violating use monitoring. *Core:* Use of the system is checked against its documented intended scope.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(3)(i); disclosure requirement):** "Description of tasks, situations, or populations where a user is cautioned against applying the intervention; and"
- **Property:** `integral_to` → `example_of`
- **Basis:** As (B)(2)(i): the cautioned-use description does not depend on enforcing it.
- **Current rationale:** Use monitoring flags use against the stated cautioned uses.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: proposed)

#### `GM-LSI-02>HTI:B7.v`
- **Author's ruling (guided review):** Accept
- **Control:** GM-LSI-02 Outcome and benefit measurement. *Core:* Benefit measures are defined and tracked.
- **Source (45 CFR 170.315(b)(11)(iv)(B)(7)(v); disclosure requirement):** "References to evaluation of use of the intervention on outcomes, including, bibliographic citations or hyperlinks to evaluations of how well the intervention reduced morbidity, mortality, length of stay, or other outcomes;"
- **Property:** `integral_to` → `example_of`
- **Basis:** (B)(7)(v) asks for 'references to evaluation of use ... on outcomes'; external evaluations can be cited without local benefit measurement.
- **Current rationale:** A local outcome evaluation adds a reference the attribute can cite.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

### Voluntary practice (CISA CPG 2.0) (6)

#### `GM-GOV-02>CPG:2.A`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-02 AI system and model inventory. *Core:* Deployed AI systems are recorded in an inventory.
- **Source (CISA CPG 2.0, goal 2.A; voluntary practice):** "Outcome: A maintained asset inventory to improve cybersecurity resilience by reducing downtime, aiding recovery, bolstering defenses, and improving preparedness. | Scope: Data, hardware, software, systems, facilities, personnel. | Recommended Action: Maintain a regularly updated inventory of all organizational assets (i.e., data, hardware, software, systems, facilities, and personnel). IT and OT assets determined to be critical for business or operational functions should be updated on a more frequent basis."
- **Property:** `integral_to` → `example_of`
- **Basis:** Second pass: CPG 2.A requires an inventory of all assets but does not set its granularity. An AI intervention embedded in the EHR can be covered by the EHR's inventory entry without being recorded individually, so recording each AI system is not necessary to the goal.
- **First pass:** supported (`integral_to`); changed in the second pass.
- **Current rationale:** Recording each deployed AI intervention in the asset inventory is one way to bring AI components into the asset-inventory goal.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-04>CPG:5.A`
- **Author's ruling (guided review):** Accept
- **Control:** GM-GOV-04 AI incident response integration. *Core:* The incident response plan addresses AI-specific incidents.
- **Source (CISA CPG 2.0, goal 5.A; voluntary practice):** "Outcome: Coordinate crisis communication methods between internal and external organization partners and critical suppliers. | Scope: Organization-wide. | Recommended Action: Design a communications plan that identifies stakeholders and mechanisms for coordination and communications during an incident.Collaborate with stakeholders and securely share information consistent with response plans and information-sharing agreements. Priorities for sharing information include preventing the spread of infections to other systems and networks.Regularly update senior leadership on the status of major incidents.Notify human resources when malicious insider activity occurs.Establish and follow media communications procedures for incident response that comply with the organization’s policies on media interaction and information disclosure."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 5.A asks for an organization-wide incident communications plan; a general plan covers incidents affecting the AI system without an AI-specific annex.
- **Current rationale:** The AI annex adds AI-specific stakeholders to the incident communications plan.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

#### `GM-GOV-04>CPG:5.B`
- **Author's ruling (guided review):** Accept; reword to cyber scope
- **Control:** GM-GOV-04 AI incident response integration. *Core:* The incident response plan addresses AI-specific incidents.
- **Source (CISA CPG 2.0, goal 5.B; voluntary practice):** "Outcome: CISA and other organizations are better able to provide assistance or understand the broader scope of a cyber incident. | Scope: Organization-wide. | Recommended Action: Organizations maintain policy and procedures on to whom and how to report all confirmed cybersecurity incidents to appropriate external entities (e.g., state/federal regulators or sector risk management agencies [SRMAs] as required, information sharing and analysis centers [ISACs], information sharing and analysis organizations [ISAOs], and CISA).Known incidents are reported to CISA as well as other necessary parties within time frames directed by applicable regulatory guidance or in the absence of guidance, as soon as safely feasible."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 5.B asks for policy on reporting 'all confirmed cybersecurity incidents'; a general reporting policy already covers confirmed incidents involving the AI system.
- **Current rationale:** The AI annex makes explicit that confirmed cybersecurity incidents involving the AI system (for example, compromise of the model or its data) are reported under the general policy.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: revised)

#### `GM-GOV-04>CPG:6.A`
- **Author's ruling (guided review):** Accept; replace rationale
- **Control:** GM-GOV-04 AI incident response integration. *Core:* The incident response plan addresses AI-specific incidents.
- **Source (CISA CPG 2.0, goal 6.A; voluntary practice):** "Outcome: Organizations are capable of safely and effectively recovering from a cybersecurity incident. | Scope: Organizational assets. | Recommended Action: Execute plans to recover and restore service to business- or mission-critical assets or systems that might be impacted by a cybersecurity incident. This may include the ability to execute mission essential functions in a degraded manner without access to critical assets or even internet access (e.g., shift to paper-based operations, radio communications, etc.)Complete post-incident analysis to identify areas for improvement and refine the incident response plan. Focus on incorporating lessons learned, enhancing detection and response capabilities, updating policies and procedures including training, and ensuring that all stakeholders are informed of the changes."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 6.A asks for recovery plans for assets impacted by a cybersecurity incident; general recovery planning can cover the AI system without AI-specific steps.
- **Current rationale:** Updating the AI annex after each AI incident is one way to refine the incident response plan from lessons learned.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: revised)

#### `GM-GOV-07>CPG:2.C`
- **Control:** GM-GOV-07 Independent assessment of monitoring. *Core:* Someone independent of the build/operate team periodically assesses the monitoring.
- **Source (CISA CPG 2.0, goal 2.C; voluntary practice):** "Outcome: Validate that implemented security controls are properly configured and working as intended | Scope: Organizational assets and networks. | Recommended Action: Organizations regularly engage third-party cybersecurity experts to validate their defenses through various exercises, such as penetration tests, bug bounties, incident simulations, and table-top exercises. These tests, both announced and unannounced, assess the ability of adversaries to infiltrate and move laterally within the network, targeting critical systems. Ensure findings from these tests are addressed."
- **Property:** `integral_to` → `removed`
- **Basis:** CPG 2.C's Recommended Action is third-party validation of cybersecurity defenses (penetration tests, bug bounties, incident simulations); an assessment of AI monitoring design is neither that activity nor required by it.
- **Current rationale:** (removed in the relevance review; see section 5)
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: removed)

#### `GM-SEC-01>CPG:4.B`
- **Author's ruling (guided review):** Accept
- **Control:** GM-SEC-01 Adversarial input, misuse, and anomalous behavior detection. *Core:* AI-specific anomalous or adversarial behavior is detected.
- **Source (CISA CPG 2.0, goal 4.B; voluntary practice):** "Outcome: Organizations can identify adverse security events. | Scope: Organization-wide. | Recommended Action: Ensure the organization has defined clear criteria and processes for adverse events. If an adverse event is suspected, follow the protocol outlined in the incident response plan to escalate the situation.Automate event information analysis as much as possible to accelerate the investigative timeline for managing suspected adverse events. This will give analysts the time and capacity to mitigate these events effectively.Conduct analyst role-specific training on the proper protocols and procedures to follow in the event of a suspected cyber incident.OT: Organizations should account for OT-specific events and anomalies in their processes and environments. It’s important to recognize that certain tools and alerts for behaviors or events that could indicate an intrusion might actually be normal within the OT environment."
- **Property:** `integral_to` → `example_of`
- **Basis:** CPG 4.B's Recommended Action is organization-wide adverse-event criteria and processes (Scope: organization-wide); general criteria can cover the AI host without AI-specific detection rules such as crafted-input or out-of-distribution detection.
- **Current rationale:** AI-specific anomaly rules extend the organization's adverse-event criteria to the AI system.
- **Author ruling:** ☐ agree ☐ change to ______  (review_status: accepted)

## 9. Wording corrected

- Release wording: the README, report, CITATION.cff, workbook, and OSCAL metadata now say the package is an unpublished draft with author review pending. The report no longer says it is "released" or "archived". The DOI reads "not yet assigned". Licensing is described as planned on release.
- AI assistance: the draft statement now says what the AI assistant did and that the author's review has not happened. The earlier sentence saying the author "made and verified every judgment call, link, and number before release" is removed. A final build is refused unless `author_review: complete` is set and the author has written her own `ai_statement_final` in `RELEASE.yaml`.
- Tooling versus review: the QA report, README, and report now separate automated checks (pipeline), the pre-review audit (AI-assisted), and the author's review (pending).
- Source kinds: every element now carries `source_type` and `obligation_holder`. Every link carries `target_source_type`, and every control is labeled `practice_type: suggested_practice`.
- Coverage: a coverage statement (mapping coverage does not show compliance, achievement of outcomes, or monitoring effectiveness) is in the bundle, README, report, workbook, OSCAL metadata, and QA report.
- HTI-1: the change classes are labeled analytic everywhere; `post_deployment_class` is renamed `gapm_change_class`; the counts are reconciled as above.
- Second pass (relevance review): a new disposition, `uncovered`, separates real gaps in GAP-M from scope decisions. Every link now carries `conditional`, `example_review`, and `example_review_note`. The compiler adds rule R12 (every link has an audit entry or a review decision) and rule R13 (removed links stay removed). Coverage figures fell, and the documents say so.

## 10. What the author decides

- [ ] Accept keeping the 9 unresolved links as conditional `example_of` for v0.1.0 (section 7), or rule on any of them individually. Their relevance has been assessed separately and is supported; only their necessity is open.
- [ ] Decide whether "validity" in (B)(8)(ii) means validity measured against local outcomes. If it does, `GM-FUN-04>HTI:B8.ii` can return to `precedes`; if label-free estimates under a no-shift assumption also count, it becomes `example_of` (revised). Until then it is a conditional link (section 7). Fairness in (B)(8)(iv) stays example_of either way, because output-rate parity uses no labels.
- [ ] Confirm or overturn each of the 14 supported necessity links (section 6).
- [ ] Spot-check the revised links (section 8); at minimum, every revised link to guidance and to voluntary practices.
- [ ] Spot-check the relevance review (section 5): every removal, and a sample of the 170 kept links (record the sampling seed).
- [ ] Accept or change the dispositions of the 12 elements left without links (section 5.4).
- [ ] Accept or change the source-kind rules in section 1, especially the rule that no practice is necessary to an AI 800-4 challenge.
- [ ] Accept or change the GAP-M change classes (J6), now documented as analytic.
- [ ] Only then set `review_status: accepted` on what you accept, and `author_review: complete` in `RELEASE.yaml`.

## 11. Second correction pass (2026-10-05)

Prepared by the AI assistant with tooling support at the author's request. It is not independent expert validation and not the author's review. All 21 links still asserting necessity after the first pass were rechecked against a narrowed control core and the exact source text. Conditions that appeared only in rationales, such as a register format, an approval step, or pre-set triggers, were removed. Any claim that could not withstand a plausible alternative way of achieving the source element was downgraded.

### 11.1 Property changes

| Link | First pass | Now | Reason |
|---|---|---|---|
| `GM-GOV-02>CPG:2.A` | `integral_to` (supported) | `example_of` (revised) | CPG 2.A requires an inventory of all assets but does not set its granularity. An AI intervention embedded in the EHR can be covered by the EHR's inventory entry without being recorded individually, so recording each AI system is not necessary to the goal. |
| `GM-GOV-06>RMF:GOVERN-2.2` | `integral_to` (supported) | `example_of` (revised) | GOVERN 2.2 asks for AI risk management training that enables personnel to perform their duties. General AI risk management training could meet it, so system-specific training is not necessary. |
| `GM-GOV-07>RMF:MEASURE-1.3` | `integral_to` (supported) | `example_of` (revised) | MEASURE 1.3 is met by 'internal experts who did not serve as front-line developers', which includes members of the operating team. GM-GOV-07 excludes the operating team, so its core is sufficient but not necessary. |
| `GM-FUN-04>HTI:B8.ii` | `precedes` (supported) | `example_of` (unresolved) | Second pass, as substantiated on 2026-10-05: outcome-based validity measures (discrimination, calibration, positive predictive value) use local outcome labels. Label-free performance estimation exists in the literature: Garg et al. (ICLR 2022, arXiv:2201.04234) propose Average Thresholded Confidence (ATC), which predicts accuracy "as the fraction of unlabeled examples for which model confidence exceeds that threshold" learned on labeled source data. The same paper shows that "absent further assumptions, accuracy on the target is identifiable iff p_t(y/x) is uniquely identified", and names covariate shift (p_s(y/x) = p_t(y/x)) and label shift as conditions under which estimation can work; it estimates accuracy only and was evaluated on image benchmarks. A label-free estimate of local validity therefore rests on an assumption that the outcome relationship has not shifted, which is part of what local validation would test. Whether such an estimate counts as "validity of intervention in local data" is an interpretive question, so the precedes claim is neither supported nor refuted; it is held as unresolved. |
| `GM-FUN-04>HTI:B8.iv` | `precedes` (supported) | `example_of` (revised) | Fairness measures such as demographic or output-rate parity compare outputs across groups and need no outcome labels, so obtaining labels is not a prerequisite for every local fairness value. The precedes claim holds only for label-dependent measures and is downgraded. |
| `GM-FAIR-02>HTI:B8.iv` | `integral_to` (supported) | `example_of` (unresolved) | 'Fairness of intervention in local data' does not define fairness. Necessity holds only if fairness is read as a comparison across groups (the regulation lists demographic characteristics in (A)(5)–(13) for evidence-based interventions, which points toward, but does not establish, a group reading); individual-fairness measures are an alternative. This is the same condition as GM-FAIR-02>RMF:MEASURE-2.11. |
| `GM-HF-01>RMF:MANAGE-4.1` | `integral_to` (supported) | `example_of` (revised) | MANAGE 4.1 names 'mechanisms for capturing and evaluating input from users'. Periodic user surveys or interviews capture and evaluate user input without a problem-reporting route, so HF-01's core is not necessary. |

### 11.2 Necessity kept, rationale corrected

- `GM-GOV-01>RMF:MANAGE-4.1` (`integral_to`): MANAGE 4.1 is the outcome that post-deployment monitoring plans are implemented; a plan covering the system is a component of that outcome.
- `GM-GOV-02>RMF:GOVERN-1.6` (`integral_to`): GOVERN 1.6 asks for mechanisms to inventory AI systems; recording deployed AI systems in an inventory is what such a mechanism does.
- `GM-GOV-03>CPG:1.D` (`integral_to`): Contract terms requiring the developer to notify the organization of security incidents and vulnerabilities are this goal's recommended action.
- `GM-FUN-02>HTI:B8.ii` (`integral_to`): A populated local-validity value is a measurement of validity in local data, which is this control's core.
- `GM-FUN-05>RMF:MEASURE-4.3` (`integral_to`): Identifying a measurable improvement or decline requires performance from more than one point in time to be available for comparison.
- `GM-FUN-06>RMF:MANAGE-2.4` (`integral_to`): MANAGE 2.4 names mechanisms, with assigned responsibility, to supersede, disengage, or deactivate a system; that mechanism is this control's core.
- `GM-OPS-01>CPG:3.Q` (`integral_to`): CPG 3.Q's action covers application and service logs on all assets where feasible; collecting the AI components' administrative and security logs centrally, with an alert if logging stops, is that action applied to the AI system.
- `GM-OPS-03>CPG:3.N` (`integral_to`): AI configuration changes go through the change management process this CPG goal requires.
- `GM-HF-01>RMF:MEASURE-3.3` (`integral_to`): User problem reports integrated into evaluation metrics are what this control produces.
- `GM-SEC-02>CPG:2.B` (`integral_to`): AI software components the organization operates are organizational assets, so they fall within the vulnerability management program this goal requires.
- `GM-SEC-03>CPG:3.H` (`integral_to`): Least privilege over AI configuration and monitoring data is this CPG goal applied to AI.
- `GM-CMP-01>RMF:GOVERN-1.1` (`integral_to`): GOVERN 1.1 requires AI legal and regulatory requirements to be documented; documenting them is this control's core.
- `GM-LSI-01>RMF:MANAGE-4.3` (`integral_to`): Tracking incidents and errors requires that they be recorded; that record is this control's core.
- `GM-LSI-03>RMF:MEASURE-3.3` (`integral_to`): An appeal route for impacted communities, integrated into metrics, is what this subcategory asks for.

### 11.3 Control cores narrowed to the part a source can require

- **GM-GOV-01.** Was: "A written post-deployment monitoring plan with a named owner exists for the system." Now: "A post-deployment monitoring plan covering the system exists."
- **GM-GOV-03.** Was: "Contracts with the developer require notice of security incidents and vulnerabilities (and model changes)." Now: "Contracts with the developer require notice of security incidents and vulnerabilities."
- **GM-FUN-05.** Was: "Performance results are retained over time so they can be compared." Now: "Performance results from earlier points in time remain available for comparison."
- **GM-FUN-06.** Was: "A deactivation/correction mechanism exists with an assigned authority." Now: "A mechanism with assigned authority exists to supersede, disengage, or deactivate the system."
- **GM-FAIR-02.** Was: "Subgroup performance is measured in the deploying organization's own data." Now: "Fairness of the intervention is measured in the deploying organization's own data (subgroup performance and output disparities)."
- **GM-OPS-01.** Was: "AI system logs go to the organization's central, access-protected log store, with alerts if logging stops." Now: "Administrative and security logs of the AI system's components that the organization operates go to the organization's central, access-protected log store, with an alert if logging stops."
- **GM-HF-01.** Was: "End users can report problems with outputs, and reports are evaluated and fed into monitoring metrics." Now: "End users can report problems with outputs, and the reports are integrated into monitoring metrics."
- **GM-SEC-02.** Was: "AI software components are in the vulnerability management program." Now: "AI software components the organization operates are in its vulnerability management program."
- **GM-LSI-01.** Was: "AI incidents and near misses are recorded." Now: "AI incidents and errors are recorded."

### 11.4 Other corrections

- **GM-HF-03:** now separates the 11 attributes that 170.315(b)(11)(v)(A)(2) allows to be shown as not available from the other 20. For those 20, (v)(A)(1) expects complete and up-to-date descriptions, and a missing value is recorded as a gap to resolve with the developer, not marked not available.
- **Report claim:** "none of these documents refers to the others at element level" is narrowed to the texts actually reviewed. None of the four cites another there. The AI RMF refers to the NIST Cybersecurity Framework (not one of the four), and AI 800-4 cites NIST AI 100-2. The HTI-1 preamble was not reviewed.
- **AI 800-4 scope:** the report states it "is focused on generative AI systems, however the concepts are relevant to other types of AI and machine learning" (p. 4, note 4). This is now stated in the README, the report, and LIMITATIONS.
- **Label-free validity, substantiated (2026-10-05, at the author's request):** the earlier statement that label-free performance estimation is "a plausible, if weaker" alternative was checked against a primary source. Garg et al., *Leveraging Unlabeled Data to Predict Out-of-Distribution Performance* (ICLR 2022, arXiv:2201.04234), propose Average Thresholded Confidence, which estimates accuracy from unlabeled target data. The same paper shows target accuracy is identifiable only under assumptions on the shift, such as covariate shift with p(y|x) unchanged. Because an unchanged outcome relationship is part of what local validation tests, the source does not establish that a label-free estimate satisfies (B)(8)(ii). The explanation was narrowed, and `GM-FUN-04>HTI:B8.ii` moved from revised to unresolved (conditional `example_of`); its property did not change.
- **Report Table 4** now shows the `precedes` total, and its column headers no longer wrap mid-word.
