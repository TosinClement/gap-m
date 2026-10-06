#!/usr/bin/env python3
"""01_fetch.py — download the four GAP-M source documents and log provenance.

Writes to data/raw/ and appends one line per file to data/raw/PROVENANCE.txt
(date | file | bytes | sha256 | url | note).

Sources (all U.S. government works):
  S1 NIST AI 100-1 (AI RMF 1.0)            nvlpubs.nist.gov
  S2 NIST AI 800-4                          nvlpubs.nist.gov
  S3 45 CFR 170.315 (eCFR, point-in-time)   ecfr.gov versioner API
  S4 CISA CPG 2.0 web page                  cisa.gov (via Internet Archive copy; see note)

CISA's site refuses non-browser clients, so S4 is fetched from a fixed Internet Archive
snapshot. 02_registries.py records the SHA-256 of the parsed goal records; the same
hash was obtained by parsing the live cisa.gov page in a browser on 2026-10-05, which
shows the snapshot and the live page carry identical goal text.

Usage: python code/01_fetch.py [--skip-existing]
"""
import argparse
import gzip
import os
import subprocess
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
LOG = os.path.join(RAW, "PROVENANCE.txt")
ECFR_DATE = "2026-10-01"
WAYBACK_TS = "20260928190145"

SOURCES = [
    ("NIST.AI.100-1.pdf", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
     "S1 AI RMF 1.0, doi:10.6028/NIST.AI.100-1"),
    ("NIST.AI.800-4.pdf", "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.800-4.pdf",
     "S2 AI 800-4, doi:10.6028/NIST.AI.800-4"),
    (f"ecfr_45cfr170.315_{ECFR_DATE}.xml",
     f"https://www.ecfr.gov/api/versioner/v1/full/{ECFR_DATE}/title-45.xml?part=170&section=170.315",
     f"S3 eCFR point-in-time text as of {ECFR_DATE}; section last amended 2025-10-01"),
    ("ecfr_45cfr170.315_versions.json",
     "https://www.ecfr.gov/api/versioner/v1/versions/title-45.json?part=170&section=170.315",
     "S3 amendment history for 45 CFR 170.315"),
    (f"cisa_cpg2_wayback_{WAYBACK_TS}.html",
     f"https://web.archive.org/web/{WAYBACK_TS}/https://www.cisa.gov/cybersecurity-performance-goals-2-0-cpg-2-0",
     "S4 CISA CPG 2.0 page, Internet Archive snapshot; live page parsed in browser 2026-10-05 gives identical goal records"),
]


def fetch(url, dest):
    req = urllib.request.Request(url, headers={
        "User-Agent": "GAP-M research fetch (mailto:clementtosin92@gmail.com)",
        "Accept-Encoding": "gzip",
    })
    with urllib.request.urlopen(req, timeout=120) as r:
        data = r.read()
        if r.headers.get("Content-Encoding") == "gzip":
            data = gzip.decompress(data)
    with open(dest, "wb") as f:
        f.write(data)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-existing", action="store_true")
    a = ap.parse_args()
    os.makedirs(RAW, exist_ok=True)
    failed = []
    for name, url, note in SOURCES:
        dest = os.path.join(RAW, name)
        if a.skip_existing and os.path.exists(dest):
            print("skip", name)
            continue
        try:
            fetch(url, dest)
        except Exception as e:  # network policy differs by machine; report, do not hide
            print(f"FAILED {name}: {e}", file=sys.stderr)
            failed.append(name)
            continue
        subprocess.run([sys.executable, os.path.join(ROOT, "code", "provenance.py"),
                        dest, url, "--log", LOG, "--note", note], check=True)
    if failed:
        print("Some downloads failed; place the files in data/raw/ by hand and re-run with --skip-existing:",
              ", ".join(failed), file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
