#!/usr/bin/env bash
# Rebuild GAP-M end to end. Run from the repository root:  bash run_all.sh [--fetch]
# Without --fetch, the committed files in data/raw/ are used (recommended: identical inputs).
set -euo pipefail
cd "$(dirname "$0")"
if [[ "${1:-}" == "--fetch" ]]; then python3 code/01_fetch.py; fi
python3 code/02_registries.py > /dev/null && echo "02 registries ok"
python3 code/03_crosswalk.py
python3 code/04_qa.py
python3 code/05_figures.py
python3 code/06_documents.py
python3 code/07_review_report.py
python3 code/08_approval_package.py
python3 code/09_author_review.py
echo "Done. Read data/processed/qa_report.txt first."
