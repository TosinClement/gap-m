# Verification checklist: GAP-M v0.1.0 (author completes before release)

Status: released 2026-10-05.

## Reproduce
- [x] `bash run_all.sh` on a fresh clone: every step finishes and `QA PASS` prints (build checks, 2026-10-05: QA PASS in the cloud and on the author's Mac)
- [x] Two clean rebuilds in the same environment produce byte-identical files (compare SHA-256) (build checks, 2026-10-05)
- [x] A rebuild in a second environment matches the data, schema, CSV, JSON, and Markdown files byte for byte; the workbook and PDF are expected to match in content (cells, extracted text), not in bytes (build checks, 2026-10-05: author's Mac)
- [x] Hashes in `data/raw/PROVENANCE.txt` match a fresh fetch, or any drift is explained (a changed eCFR text date or a new CPG page is a source change, not a bug) (re-fetched 2026-10-05; all match; see mapping/author_review.yaml provenance_refetch)
- [x] Every number in README.md and the technical report comes from `report/stats.json` (regenerated, not typed) (build design; release statement figures checked by QA)

## Source checks (by hand, against the original documents)
- [x] AI RMF: open NIST AI 100-1 at pp. 22–33; check GOVERN 1.4, MAP 1.1, MEASURE 2.4, and MANAGE 4.1 against `elements.csv` (QA report, section 6) (author spot-check: all four match) (docs/AUTHOR_REVIEW.md)
- [x] AI 800-4: open Table 1 (p. 6), Table 2 (p. 9), and Table 3 (p. 17); confirm the 6 categories, 13 cross-cutting items, and 19 category challenges (author spot-check: counts match) (docs/AUTHOR_REVIEW.md)
- [x] HTI-1: open eCFR 45 CFR 170.315(b)(11)(iv)(B); confirm 31 attributes and spot-check (4)(iv), (7)(v), and (8)(ii) (author spot-check: all match) (docs/AUTHOR_REVIEW.md)
- [x] HTI-1: confirm (b)(11) has not been amended since 2025-10-01 (eCFR "Timeline" for 170.315); if it has, re-run and re-review (author check: no newer amendment) (docs/AUTHOR_REVIEW.md)
- [x] CPG 2.0: open the CISA page; confirm 34 goals and spot-check 1.D, 3.Q, and 4.B (author spot-check: all match) (docs/AUTHOR_REVIEW.md)
- [x] Re-read licensing: all four sources are U.S. government works; nothing restricts redistribution of the quoted text (checked against primary sources; edits approved) (docs/AUTHOR_REVIEW.md)

## Necessity audit (docs/MAPPING_REVIEW.md)
- [x] Accept keeping the 9 **unresolved** links as conditional `example_of` for v0.1.0 (section 7), or rule on any individually in `data/processed/mapping_review.csv` (Decision 1; each reviewed individually) (docs/AUTHOR_REVIEW.md)
- [x] Confirm or overturn every **supported** necessity link (section 6) (all 14 integral_to links reviewed) (docs/AUTHOR_REVIEW.md)
- [x] Spot-check **revised** links (section 8) (24 in sample + 3 targeted CPG links) (docs/AUTHOR_REVIEW.md)

## Relevance review of example_of links (docs/MAPPING_REVIEW.md, section 5)
- [x] Check every removal (section 5.1) and every reworded rationale (5.2) (32 removals confirmed; 9 rewordings ruled on) (docs/AUTHOR_REVIEW.md)
- [x] Spot-check a sample of kept links (record the seed) (66 links, seed 20261005) (docs/AUTHOR_REVIEW.md)
- [x] Accept or change the dispositions of elements left without links (5.4), including the three `uncovered` gaps (Decision 3, J5, MANAGE 3.2) docs/AUTHOR_DECISIONS.md
- [x] Accept or change the per-source-kind rules (especially: no practice is necessary to an AI 800-4 challenge) (Decision 2) docs/AUTHOR_DECISIONS.md

## Judgment calls to own (edit `mapping/*.yaml`, then re-run)
- [x] **J1** "Six monitoring-challenge categories" = AI 800-4 Table 1 categories, with Table 3 challenges beneath and Table 2 as a secondary layer. Agree, or change the wording of the release title. (accepted) docs/AUTHOR_DECISIONS.md
- [x] **J2** Read all 32 control definitions (objective, activity, evidence, cadence, owner role). Change anything you would not defend. (all 32 reviewed) (docs/AUTHOR_REVIEW.md)
- [x] **J3** Review the links in `mapping/gapm_controls.yaml` (the workbook's Links sheet is easier). Minimum: every `integral_to` and `precedes` link, every conditional link, and a random 25% of other `example_of` links (record the seed). Then set `review_status` to `accepted`. (minimum set reviewed; per-item status recorded) (docs/AUTHOR_REVIEW.md)
- [x] **J4** Fairness placed under Functionality with Large-Scale Impacts secondary. (accepted) docs/AUTHOR_DECISIONS.md
- [x] **J5** Out-of-scope and prerequisite dispositions in `mapping/dispositions.yaml`. (accepted) docs/AUTHOR_DECISIONS.md
- [x] **J6** GAP-M analytic change class for each of the 31 HTI attributes in `mapping/hti_attribute_classes.yaml` (not established by the regulation). (accepted) docs/AUTHOR_DECISIONS.md
- [x] Mapping vocabulary: NIST IR 8477 supportive relationships (`supports` + integral_to / example_of / precedes) is right for this use case. (checked against NIST IR 8477 sec. 4.2) (docs/AUTHOR_REVIEW.md)

## Before it goes public
- [x] README, LIMITATIONS, and the technical report revised in your own voice; nothing remains you cannot defend (author approved current text; third person) (docs/AUTHOR_REVIEW.md)
- [x] Write your own release statement in `RELEASE.yaml` as `ai_statement_final` (what the AI assistant did, and what you reviewed and how); set `author_review: complete`. The build refuses `final: true` until both are set. (approved and saved; author_review: complete, 2026-10-05) (docs/AUTHOR_REVIEW.md)
- [x] Zenodo DOI reserved; `RELEASE.yaml`: set `release_date`, `doi`, and `final: true`; re-run `bash run_all.sh` (DOI 10.5281/zenodo.23178136 reserved by the author in a Zenodo draft; release date 2026-10-05; final build QA PASS)
- [x] Draft status lines removed from docs/; `python3 code/publish_gate.py . --allow-draft-in code/` passes (no draft stamps, no verify tags, no placeholders) (gate clear, 2026-10-05)
- [ ] Evidence log row written on release day
