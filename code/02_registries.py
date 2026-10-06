#!/usr/bin/env python3
"""02_registries.py — parse the four sources into one element registry.

Reads data/raw/*, mapping/ai800_4_elements.yaml, mapping/hti_attribute_classes.yaml.
Writes:
  data/registry/elements.csv / elements.json   every element, verbatim text, locator
  data/registry/registry_qa.json               parse checks consumed by 04_build.py

Element id scheme
  RMF:GOVERN            function          RMF:GOVERN-1 category        RMF:GOVERN-1.1 subcategory
  A84:FUN               monitoring cat.   A84:FUN-G1 category challenge  A84:XC-TMT cross-cutting cat.
  A84:XC-TMT-G1         cross-cutting item
  HTI:B1                attribute group   HTI:B1.i attribute  (= 45 CFR 170.315(b)(11)(iv)(B)(1)(i))
  CPG:GOVERN            CPG function      CPG:1.A goal
"""
import hashlib
import json
import os
import re
import sys

import pdfplumber
import yaml
from bs4 import BeautifulSoup
import pandas as pd

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW = os.path.join(ROOT, "data", "raw")
OUT = os.path.join(ROOT, "data", "registry")
MAP = os.path.join(ROOT, "mapping")

# SHA-256 of the 34 CPG goal records (compact JSON) parsed from the live cisa.gov page
# in a browser on 2026-10-05. The archived copy must reproduce it.
CPG_LIVE_SHA256 = "7d3afda4ba166c6dcfb33211a1b87878ea1916e420d4cf7adde26d69c5604073"

ROMAN = ["i", "ii", "iii", "iv", "v", "vi", "vii", "viii", "ix", "x"]
ws = lambda t: re.sub(r"\s+", " ", t).strip()
elements, qa = [], {}


# What kind of statement each source makes. GAP-M controls themselves are suggested practices.
SOURCE_TYPE = {
    "AI RMF 1.0": "guidance",                       # voluntary risk-management outcomes
    "NIST AI 800-4": "monitoring_challenge",         # research report on monitoring challenges; not requirements
    "ONC HTI-1 (b)(11)": "regulatory_disclosure_requirement",  # certification requirement on Health IT Modules
    "CISA CPG 2.0": "voluntary_practice",            # voluntary baseline practices with recommended actions
}
OBLIGATION = {
    "AI RMF 1.0": "none (voluntary)",
    "NIST AI 800-4": "none (describes challenges)",
    "ONC HTI-1 (b)(11)": "certified Health IT Module / its developer",
    "CISA CPG 2.0": "none (voluntary)",
}


def add(**k):
    base = dict(element_id=None, framework=None, level=None, parent_id=None, code=None,
                label=None, text=None, locator=None, mappable=False)
    base.update(k)
    base["source_type"] = SOURCE_TYPE[base["framework"]]
    base["obligation_holder"] = OBLIGATION[base["framework"]]
    elements.append(base)


# ---------------------------------------------------------------- S1 AI RMF 1.0
def rmf():
    path = os.path.join(RAW, "NIST.AI.100-1.pdf")
    vocab = set()
    L, R = [], []

    def cluster(words):
        words = sorted(words, key=lambda w: w["top"])
        lines = []
        for w in words:
            if lines and abs(w["top"] - lines[-1][0]) <= 3.5:
                lines[-1][1].append(w)
            else:
                lines.append([w["top"], [w]])
        return [(round(t), " ".join(x["text"] for x in sorted(l, key=lambda w: w["x0"]))) for t, l in lines]

    with pdfplumber.open(path) as pdf:
        for p in pdf.pages:
            for w in p.extract_words(x_tolerance=1):
                if not w["text"].endswith("-"):
                    vocab.add(re.sub(r"[^\w’'-]", "", w["text"]).lower())
        for pg in range(26, 38):  # Core tables, printed pp. 21-33
            words = pdf.pages[pg].extract_words(x_tolerance=1)
            hdr = [w["top"] for w in words if w["text"] == "Subcategories"]
            if not hdr:
                continue
            body = [w for w in words if w["top"] > hdr[0] + 5]
            ends = [w["top"] for w in body if w["x0"] <= 92 or w["text"] == "Page"]
            stop = min(ends) if ends else 1e9
            body = [w for w in body if w["top"] < stop - 1]
            foot = [w["text"] for w in words if w["top"] > 690]
            nums = [foot[k + 1] for k in range(len(foot) - 1) if foot[k] == "Page" and foot[k + 1].isdigit()]
            printed = int(nums[0]) if nums else None  # printed page number from the running footer
            L += [(printed, t) for _, t in cluster([w for w in body if w["x0"] < 200])]
            R += [(printed, t) for _, t in cluster([w for w in body if w["x0"] >= 200])]

    dehyph = []

    def join(lines):
        s, pages = "", []
        for pg, ln in lines:
            if s.endswith("-"):
                head = re.findall(r"(\w+)-$", s)
                tail = re.findall(r"^(\w+)", ln)
                cand = (head[0] + tail[0]).lower() if head and tail else None
                compound = (head[0] + "-" + tail[0]).lower() if head and tail else None
                # Rule: a line-end hyphen is kept only when the joined word is not used in
                # AI 100-1 and the document uses that hyphenated compound, or other compounds on
                # the same 4+ letter head (e.g. "context-"); otherwise it is a typesetting break.
                prefix_compound = head and len(head[0]) >= 4 and any(v.startswith(head[0].lower() + "-") for v in vocab)
                if compound and cand not in vocab and (compound in vocab or prefix_compound):
                    dehyph.append(f"{head[0]}-|{tail[0]} kept hyphen (hyphenated compound pattern in document)")
                    s = s + ln
                else:
                    how = "word elsewhere in document" if cand in vocab else "default rule"
                    dehyph.append(f"{head[0]}-|{tail[0]} -> {head[0] + tail[0]} ({how})")
                    s = s[:-1] + ln
            else:
                s = (s + " " + ln) if s else ln
            pages.append((len(s), pg))
        return s, pages

    # drop the table running footer "Continued on next page" before joining
    R = [(pg, t.replace("Continued on next page", "").strip()) for pg, t in R]
    R = [(pg, t) for pg, t in R if t]
    rtext, rpages = join(R)
    ltext, lpages = join(L)
    fn = r"(GOVERN|MAP|MEASURE|MANAGE)"

    def page_at(pages, pos):
        for end, pg in pages:
            if pos < end:
                return pg
        return pages[-1][1]

    subs = [(m.group(1), m.group(2), ws(m.group(3)), page_at(rpages, m.start()))
            for m in re.finditer(fn + r" (\d+\.\d+): (.*?)(?= " + fn + r" \d+\.\d+:|$)", rtext)]
    cats = [(m.group(1), m.group(2), ws(m.group(3)), page_at(lpages, m.start()))
            for m in re.finditer(fn + r" (\d+): (.*?)(?= " + fn + r" \d+:|$)", ltext)]
    fdesc = {"GOVERN": "A culture of risk management is cultivated and present",
             "MAP": "Context is recognized and risks related to context are identified",
             "MEASURE": "Identified risks are assessed, analyzed, or tracked",
             "MANAGE": "Risks are prioritized and acted upon based on a projected impact"}
    for f in ["GOVERN", "MAP", "MEASURE", "MANAGE"]:
        add(element_id=f"RMF:{f}", framework="AI RMF 1.0", level="function", code=f,
            label=f.title(), text=fdesc[f], locator="NIST AI 100-1, Figure 5")
    for f, n, t, pg in cats:
        add(element_id=f"RMF:{f}-{n}", framework="AI RMF 1.0", level="category", parent_id=f"RMF:{f}",
            code=f"{f} {n}", label=f"{f} {n}", text=t, locator=f"NIST AI 100-1, p. {pg}")
    for f, n, t, pg in subs:
        add(element_id=f"RMF:{f}-{n}", framework="AI RMF 1.0", level="subcategory",
            parent_id=f"RMF:{f}-{n.split('.')[0]}", code=f"{f} {n}", label=f"{f} {n}", text=t,
            locator=f"NIST AI 100-1, p. {pg}", mappable=True)
    qa["rmf"] = {"categories": len(cats), "subcategories": len(subs),
                 "by_function": {f: sum(1 for s in subs if s[0] == f) for f in fdesc},
                 "dehyphenation": dehyph}


# ---------------------------------------------------------------- S2 AI 800-4
def ai800_4():
    y = yaml.safe_load(open(os.path.join(MAP, "ai800_4_elements.yaml"), encoding="utf-8"))

    def norm(t):
        t = t.replace("•", " ")
        t = re.sub(r"-\s*\n\s*", "-", t)
        return re.sub(r"\s+", " ", t)

    texts = []
    with pdfplumber.open(os.path.join(RAW, "NIST.AI.800-4.pdf")) as pdf:
        for p in pdf.pages:
            texts.append(norm(p.extract_text(x_tolerance=1.5) or ""))
            for xs in (230, 250, 270, 290, 310):
                for box in ((0, 0, xs, p.height), (xs, 0, p.width, p.height)):
                    texts.append(norm(p.crop(box).extract_text(x_tolerance=1.5) or ""))
    checked, missing = 0, []

    def check(s):
        nonlocal checked
        checked += 1
        if not any(s in t for t in texts):
            missing.append(s)

    for c in y["categories"]:
        for k in ("name", "question", "definition"):
            check(c[k])
        add(element_id=f"A84:{c['id']}", framework="NIST AI 800-4", level="monitoring_category",
            code=c["id"], label=c["name"], text=f"{c['question']} {c['definition']}",
            locator=f"NIST AI 800-4, Table 1, p. {c['page']}", mappable=True)
    for c in y["challenges"]:
        check(c["text"])
        add(element_id=f"A84:{c['id']}", framework="NIST AI 800-4", level=f"category_{c['kind']}",
            parent_id=f"A84:{c['category']}", code=c["id"], label=c["text"], text=c["text"],
            locator=f"NIST AI 800-4, Table 3, p. {c['page']}", mappable=True)
    for x in y["cross_cutting"]:
        check(x["name"])
        add(element_id=f"A84:{x['id']}", framework="NIST AI 800-4", level="crosscutting_category",
            code=x["id"], label=x["name"], text=x["name"], locator="NIST AI 800-4, Table 2, p. 9")
        for i in x["items"]:
            check(i["text"])
            add(element_id=f"A84:{i['id']}", framework="NIST AI 800-4", level=f"crosscutting_{i['kind']}",
                parent_id=f"A84:{x['id']}", code=i["id"], label=i["text"], text=i["text"],
                locator="NIST AI 800-4, Table 2, p. 9", mappable=True)
    qa["ai800_4"] = {"strings_checked": checked, "strings_missing": missing,
                     "categories": len(y["categories"]), "category_challenges": len(y["challenges"]),
                     "crosscutting_items": sum(len(x["items"]) for x in y["cross_cutting"])}


# ---------------------------------------------------------------- S3 HTI-1 (b)(11)(iv)(B)
def hti():
    import html as H
    x = open(os.path.join(RAW, "ecfr_45cfr170.315_2026-10-01.xml"), encoding="utf-8").read()
    t = H.unescape(re.sub(r"<P>", "\n", x))
    t = re.sub(r"<[^>]+>", "", t)
    i = t.find("(B) For Predictive Decision Support Interventions:")
    j = t.find("(v) Source attribute access and modification", i)
    block = t[i:j]
    classes = yaml.safe_load(open(os.path.join(MAP, "hti_attribute_classes.yaml"), encoding="utf-8"))
    groups, attrs = [], []
    g = None
    for line in [ws(l) for l in block.split("\n") if ws(l)][1:]:
        m = re.match(r"^\((\d)\) (.*)$", line)
        if m:
            g = m.group(1)
            groups.append((g, m.group(2)))
            continue
        m = re.match(r"^\(([ivx]+)\) (.*)$", line)
        if m and g:
            attrs.append((g, m.group(1), m.group(2)))
    for gn, gt in groups:
        add(element_id=f"HTI:B{gn}", framework="ONC HTI-1 (b)(11)", level="attribute_group",
            code=f"(B)({gn})", label=re.sub(r",? including(?: at a minimum)?:$", "", gt), text=gt,
            locator=f"45 CFR 170.315(b)(11)(iv)(B)({gn})")
    for gn, r, at in attrs:
        cid = f"B{gn}.{r}"
        cl = classes.get(cid, {})
        add(element_id=f"HTI:{cid}", framework="ONC HTI-1 (b)(11)", level="source_attribute",
            parent_id=f"HTI:B{gn}", code=f"(B)({gn})({r})", label=at.rstrip(";. ").replace("; and", ""),
            text=at, locator=f"45 CFR 170.315(b)(11)(iv)(B)({gn})({r})", mappable=True,
            hti_gapm_change_class=cl.get("class"), hti_gapm_change_note=cl.get("note"),
            hti_na_flag=cl.get("may_indicate_not_available", False))
    vers = json.load(open(os.path.join(RAW, "ecfr_45cfr170.315_versions.json")))["content_versions"]
    qa["hti"] = {"groups": len(groups), "attributes": len(attrs),
                 "by_group": {gn: sum(1 for a in attrs if a[0] == gn) for gn, _ in groups},
                 "classified": sum(1 for gn, r, _ in attrs if f"B{gn}.{r}" in classes),
                 "section_last_amended": max(v["amendment_date"] for v in vers),
                 "ecfr_text_date": "2026-10-01"}


# ---------------------------------------------------------------- S4 CISA CPG 2.0
def cpg():
    """Parse CPG 2.0 goals from the archived CISA page when it is present; otherwise load the committed records.

    The archived HTML is not redistributed in the release (it contains Internet Archive markup that is not a
    U.S. Government work). The 34 parsed goal records are written to data/raw/cisa_cpg2_records.json, and a build
    without the HTML must reproduce the recorded SHA-256 of those records exactly.
    """
    fnc = {"1": "Govern", "2": "Identify", "3": "Protect", "4": "Detect", "5": "Respond", "6": "Recover"}
    rec_path = os.path.join(RAW, "cisa_cpg2_records.json")
    html = [n for n in os.listdir(RAW) if n.startswith("cisa_cpg2_wayback_") and n.endswith(".html")]
    if not html:
        rows = json.load(open(rec_path, encoding="utf-8"))
        if hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest() != CPG_LIVE_SHA256:
            raise SystemExit("cisa_cpg2_records.json does not match the recorded CPG hash")
        return cpg_add(rows, fnc, source="records")
    f = html[0]
    s = BeautifulSoup(open(os.path.join(RAW, f), encoding="utf-8").read(), "lxml")
    keys = ["Outcome:", "Risk Addressed:", "Scope:", "Recommended Action:", "Cost:", "Impact:",
            "Ease of Implementation"]
    fields = ["outcome", "risk_addressed", "scope", "recommended_action", "cost", "impact", "ease"]
    rows = []
    for dt in s.find_all("dt"):
        h = ws(dt.get_text())
        m = re.match(r"^(.*) \((\d)\.([A-Z])\)$", h)
        if not m:
            continue
        dd = dt.find_next_sibling()
        b = ws(dd.get_text()) if dd else ""
        r = {"cpg_id": f"{m[2]}.{m[3]}", "function": fnc[m[2]], "title": m[1]}
        pos = [b.find(k) for k in keys]
        for n, k in enumerate(keys):
            st = pos[n]
            if st < 0:
                r[fields[n]] = None
                continue
            e = min([p for p in pos if p > st] + [len(b)])
            r[fields[n]] = b[st + len(k):e].strip()
        rows.append(r)
    with open(rec_path, "w", encoding="utf-8") as fh:
        fh.write(json.dumps(rows, ensure_ascii=False, separators=(",", ":")))
    return cpg_add(rows, fnc, source=f)


def cpg_add(rows, fnc, source):
    digest = hashlib.sha256(json.dumps(rows, ensure_ascii=False, separators=(",", ":")).encode()).hexdigest()
    for k, v in fnc.items():
        add(element_id=f"CPG:{v.upper()}", framework="CISA CPG 2.0", level="function", code=k,
            label=v, text=v, locator=f"CISA CPG 2.0, {v} ({k})")
    for r in rows:
        add(element_id=f"CPG:{r['cpg_id']}", framework="CISA CPG 2.0", level="goal",
            parent_id=f"CPG:{r['function'].upper()}", code=r["cpg_id"], label=r["title"],
            text=r["outcome"], locator=f"CISA CPG 2.0, goal {r['cpg_id']}", mappable=True,
            cpg_risk_addressed=r["risk_addressed"], cpg_scope=r["scope"],
            cpg_recommended_action=r["recommended_action"], cpg_cost=r["cost"],
            cpg_impact=r["impact"], cpg_ease=r["ease"])
    qa["cpg"] = {"goals": len(rows), "by_function": {v: sum(1 for r in rows if r["function"] == v) for v in fnc.values()},
                 "null_fields": [r["cpg_id"] for r in rows if any(v is None for v in r.values())],
                 "record_sha256": digest, "live_sha256": CPG_LIVE_SHA256,
                 "matches_live_capture": digest == CPG_LIVE_SHA256}


def main():
    os.makedirs(OUT, exist_ok=True)
    rmf(); ai800_4(); hti(); cpg()
    ids = [e["element_id"] for e in elements]
    qa["duplicate_ids"] = sorted({i for i in ids if ids.count(i) > 1})
    qa["elements_total"] = len(elements)
    qa["mappable_total"] = sum(e["mappable"] for e in elements)
    json.dump(elements, open(os.path.join(OUT, "elements.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    pd.DataFrame(elements).to_csv(os.path.join(OUT, "elements.csv"), index=False)
    json.dump(qa, open(os.path.join(OUT, "registry_qa.json"), "w"), indent=1, ensure_ascii=False)
    print(json.dumps({k: v for k, v in qa.items() if k != "rmf"} | {"rmf": {k: v for k, v in qa["rmf"].items() if k != "dehyphenation"}}, indent=1))
    hard = [qa["rmf"]["categories"] == 19, qa["rmf"]["subcategories"] == 72, not qa["ai800_4"]["strings_missing"],
            qa["hti"]["attributes"] == 31, qa["cpg"]["goals"] == 34, qa["cpg"]["matches_live_capture"],
            not qa["duplicate_ids"]]
    if not all(hard):
        sys.exit("registry checks FAILED")


if __name__ == "__main__":
    main()
