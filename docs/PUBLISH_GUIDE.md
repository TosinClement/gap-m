# Publish guide: GAP-M v0.1.0

Status: released 2026-10-05.

## 0. Reserve the DOI and finalize (10 min)
1. zenodo.org → New upload → under "Digital Object Identifier", choose to get a DOI now (reserve). Save the draft; do not publish yet. Copy the reserved DOI (10.5281/zenodo.NNNNNNNN).
2. Edit `RELEASE.yaml`: set `release_date: "YYYY-MM-DD"`, `doi: "10.5281/zenodo.NNNNNNNN"` (the reserved DOI), and `final: true`.
3. Review status is already recorded per item from `mapping/author_review.yaml`: reviewed practices and links are `accepted`, `revised`, or `rejected`; the 185 links you did not individually review stay `proposed` by design, as your release statement says. `author_review: complete` and `ai_statement_final` are already set. Do not change these at release.
4. Replace the `Status: release candidate…` line at the top of each file in `docs/` with `Status: released YYYY-MM-DD` (the generated docs update themselves on the final build).
5. Rebuild: `bash run_all.sh`. Check that `QA PASS` prints (including the release-statement check) and the figures and report carry no draft or release-candidate stamps.
6. Run `python3 code/publish_gate.py . --allow-draft-in code/`. It must report zero blockers before you continue.

## 1. GitHub (10 min)
1. Create an empty public repository at github.com/new named **gap-m** under TosinClement, with no README, license, or .gitignore.
2. In Terminal, inside the `GAP-M` folder:
   ```bash
   git init -b main
   git config user.name "Tosin Clement"
   git config user.email "clementtosin92@gmail.com"
   git add -A
   git commit -m "GAP-M v0.1.0"
   git remote add origin https://github.com/TosinClement/gap-m.git
   git push -u origin main
   git tag -a v0.1.0 -m "GAP-M v0.1.0"
   git push origin v0.1.0
   ```
3. Use the prebuilt release archive `../GAP-M_v0.1.0_release/gap-m-v0.1.0.zip` (its SHA-256 is in `../GAP-M_v0.1.0_release/RELEASE_NOTES.md`). Optional cross-check: `git ls-files | sort` should list the same files as the archive manifest.
4. Create the release: `gh release create v0.1.0 ../GAP-M_v0.1.0_release/gap-m-v0.1.0.zip report/GAP-M_technical_report.pdf data/crosswalk/gapm_crosswalk.json --title "GAP-M v0.1.0" --notes-file ../GAP-M_v0.1.0_release/RELEASE_NOTES.md`

## 2. Zenodo (10 min)
Return to the saved draft with the reserved DOI (manual upload, as for FedDrift and CapacityDrift; the GitHub integration is off).
1. Drag in the three files from `GAP-M_v0.1.0_release/`: `gap-m-v0.1.0.zip`, `GAP-M_technical_report.pdf`, and `gapm_crosswalk.json` (the same files attached to the GitHub release).
2. Metadata:
   - **Resource type:** Dataset
   - **Title:** GAP-M: Governance-Aligned Post-deployment Monitoring
   - **Creator:** Clement, Tosin · ORCID 0009-0001-2055-5113 · Independent Researcher
   - **Description:** paste the release description from `GAP-M_v0.1.0_release/RELEASE_NOTES.md`
   - **License:** Creative Commons Attribution 4.0 International
   - **Version:** 0.1.0 · **Publication date:** your release date
   - **Keywords:** AI governance; post-deployment monitoring; NIST AI RMF; NIST AI 800-4; HTI-1; decision support interventions; CISA CPG; crosswalk; OSCAL
   - **Related identifiers:**
     - https://github.com/TosinClement/gap-m (is supplement to)
     - 10.6028/NIST.AI.100-1 (is derived from)
     - 10.6028/NIST.AI.800-4 (is derived from)
     - 10.6028/NIST.IR.8477 (references)
3. Check the file checksums against the GitHub release, then Publish. The DOI goes live and resolves to the record.

## 3. Record it the same day
Add a row to `EVIDENCE_LOG.csv` in the EB2 PETTION BUILD folder with the date, the DOI link, the GitHub release URL, file checksums, and a 0-download snapshot. Save PDFs of the Zenodo record and the GitHub release page next to the CapacityDrift captures.

## Later (optional)
- **arXiv (cs.CY):** submit the technical report. You must submit it yourself; first-time submitters in a category may need endorsement.
- **NIST OLIR:** package the links as an Informative Reference submission (see docs/NEXT_STEPS.md).
