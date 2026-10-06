#!/usr/bin/env python3
"""05_figures.py — report figures from the crosswalk outputs.

Fig 1  coverage of each framework's elements by disposition and link strength
Fig 2  link counts, GAP-M control family x source-framework group (heatmap)
Fig 3  the 31 HTI-1 attributes x the controls that maintain them, by IR 8477 property

Figures carry a DRAFT stamp unless RELEASE.yaml has final: true or --final is passed.
Palette: dataviz reference palette (blue sequential ramp; neutral grays for unmapped).
"""
import json
import os
import sys

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.colors import LinearSegmentedColormap, ListedColormap, BoundaryNorm
import yaml

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIG = os.path.join(ROOT, "report", "figures")
J = lambda *p: json.load(open(os.path.join(ROOT, *p), encoding="utf-8"))
rel = yaml.safe_load(open(os.path.join(ROOT, "RELEASE.yaml")))
FINAL = rel.get("final") or "--final" in sys.argv

INK, INK2, MUTED, GRID, SURF = "#0b0b0b", "#52514e", "#8a8984", "#e4e3df", "#fcfcfb"
BLUE_DARK, BLUE, BLUE_LIGHT = "#1c5cab", "#2a78d6", "#86b6ef"
GRAY_DARK, GRAY_MID, GRAY_LIGHT = "#5f5e5a", "#8a8984", "#b0afaa"  # validated ordinal neutral ramp (light end 2.14:1)
SEQ = ["#fcfcfb", "#cde2fb", "#9ec5f4", "#6da7ec", "#3987e5", "#256abf", "#184f95", "#0d366b"]

plt.rcParams.update({"font.family": "DejaVu Sans", "font.size": 9, "axes.edgecolor": GRID,
                     "axes.labelcolor": INK2, "xtick.color": INK2, "ytick.color": INK2,
                     "figure.facecolor": SURF, "axes.facecolor": SURF, "savefig.facecolor": SURF})


def stamp(fig):
    if not FINAL:
        fig.text(0.99, 0.01, "Release candidate — not for citation" if rel.get("author_review") == "complete" else "DRAFT — not for citation", ha="right", va="bottom", fontsize=8,
                 color="#b33a3a", weight="bold")


def credit(fig):
    fig.text(0.01, 0.01, f"GAP-M v{rel['version']} · Clement, T." + (" · CC BY 4.0" if FINAL else (" · release candidate" if rel.get("author_review") == "complete" else " · unpublished draft")), ha="left", va="bottom",
             fontsize=7, color=MUTED)


def fig1(S, disp):
    fws = [("AI RMF 1.0", "AI RMF 1.0\nsubcategories"), ("NIST AI 800-4", "NIST AI 800-4\ncategories + challenges"),
           ("ONC HTI-1 (b)(11)", "HTI-1 predictive DSI\nsource attributes"), ("CISA CPG 2.0", "CISA CPG 2.0\ngoals")]
    cats = [("integral", "Mapped, ≥1 integral link", BLUE_DARK),
            ("other", "Mapped, example/precedes only", BLUE_LIGHT),
            ("uncovered", "Uncovered (gap in GAP-M)", GRAY_DARK),
            ("prerequisite", "Prerequisite baseline", GRAY_MID),
            ("out_of_scope", "Out of monitoring scope", GRAY_LIGHT)]
    fig, ax = plt.subplots(figsize=(7.2, 3.0))
    for i, (fw, lab) in enumerate(fws):
        D = [d for d in disp if d["framework"] == fw]
        vals = {"integral": sum(d["disposition"] == "mapped" and d["n_integral"] > 0 for d in D),
                "other": sum(d["disposition"] == "mapped" and d["n_integral"] == 0 for d in D),
                "prerequisite": sum(d["disposition"] == "prerequisite" for d in D),
                "out_of_scope": sum(d["disposition"] == "out_of_scope" for d in D),
                "uncovered": sum(d["disposition"] == "uncovered" for d in D)}
        n, left = len(D), 0
        for k, _, col in cats:
            w = 100 * vals[k] / n
            if w:
                ax.barh(i, w - 0.4, left=left + 0.2, color=col, height=0.56, edgecolor="none")
                if w >= 7:
                    ax.text(left + w / 2, i, str(vals[k]), ha="center", va="center", fontsize=8,
                            color="white" if k in ("integral", "uncovered", "prerequisite") else INK)
            left += w
        ax.text(101.5, i, f"n = {n}", va="center", fontsize=8, color=INK2)
    ax.set_yticks(range(len(fws)), [f[1] for f in fws])
    ax.invert_yaxis()
    ax.set_xlim(0, 112)
    ax.set_xticks([0, 25, 50, 75, 100], ["0%", "25%", "50%", "75%", "100%"])
    ax.xaxis.grid(True, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    for s in ("top", "right", "left"):
        ax.spines[s].set_visible(False)
    ax.tick_params(axis="y", length=0)
    hs = [plt.Rectangle((0, 0), 1, 1, color=c) for _, _, c in cats]
    ax.legend(hs, [l for _, l, _ in cats], ncol=3, frameon=False, fontsize=7.2, loc="upper center",
              bbox_to_anchor=(0.42, 1.30))
    fig.subplots_adjust(left=0.22, right=0.97, top=0.80, bottom=0.14)
    stamp(fig); credit(fig)
    fig.savefig(os.path.join(FIG, "fig1_coverage.png"), dpi=220)
    plt.close(fig)


def fig2(links, controls, el):
    E = {e["element_id"]: e for e in el}
    fam_order = ["GOV", "FUN", "FAIR", "OPS", "HF", "SEC", "CMP", "LSI"]
    fam_name = {c["family"]: c["family_name"] for c in controls}
    nctrl = {f: sum(c["family"] == f for c in controls) for f in fam_order}

    def col(l):
        t = l["target_id"]
        e = E[t]
        if t.startswith("RMF:"):
            return ("AI RMF", e["code"].split()[0].title())
        if t.startswith("A84:"):
            if e["level"].startswith("crosscutting"):
                return ("AI 800-4", "Cross-cut")
            return ("AI 800-4", (e["parent_id"] or t).split(":")[1].split("-")[0])
        if t.startswith("HTI:"):
            return ("HTI-1", e["parent_id"].split(":")[1])
        return ("CPG 2.0", e["parent_id"].split(":")[1].title())

    cols = [("AI RMF", x) for x in ["Govern", "Map", "Measure", "Manage"]] + \
           [("AI 800-4", x) for x in ["FUN", "OPS", "HF", "SEC", "CMP", "LSI", "Cross-cut"]] + \
           [("HTI-1", f"B{i}") for i in range(1, 10)] + \
           [("CPG 2.0", x) for x in ["Govern", "Identify", "Protect", "Detect", "Respond", "Recover"]]
    M = [[0] * len(cols) for _ in fam_order]
    cmap_c = {c["control_id"]: c["family"] for c in controls}
    for l in links:
        M[fam_order.index(cmap_c[l["control_id"]])][cols.index(col(l))] += 1
    vmax = max(max(r) for r in M)
    cmap = LinearSegmentedColormap.from_list("seq", SEQ)
    fig, ax = plt.subplots(figsize=(9.6, 3.9))
    ax.imshow(M, cmap=cmap, vmin=0, vmax=vmax, aspect="auto")
    for i, r in enumerate(M):
        for j, v in enumerate(r):
            if v:
                ax.text(j, i, str(v), ha="center", va="center", fontsize=7.5,
                        color="white" if v > vmax * 0.55 else INK)
    ax.set_xticks(range(len(cols)), [c[1] for c in cols], rotation=90, fontsize=7.5)
    ax.set_yticks(range(len(fam_order)), [f"{fam_name[f]} ({nctrl[f]})" for f in fam_order], fontsize=8)
    ax.set_xticks([x - 0.5 for x in range(1, len(cols))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(fam_order))], minor=True)
    ax.grid(which="minor", color=SURF, lw=1.5)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_visible(False)
    start = 0
    for g in ["AI RMF", "AI 800-4", "HTI-1", "CPG 2.0"]:
        n = sum(c[0] == g for c in cols)
        ax.text(start + n / 2 - 0.5, -0.9, g, ha="center", va="bottom", fontsize=8.5, weight="bold", color=INK)
        if start:
            ax.axvline(start - 0.5, color=INK2, lw=1)
        start += n
    fig.subplots_adjust(left=0.22, right=0.99, top=0.88, bottom=0.2)
    stamp(fig); credit(fig)
    fig.savefig(os.path.join(FIG, "fig2_family_by_source.png"), dpi=220)
    plt.close(fig)


def fig3(links, hti):
    hl = [l for l in links if l["target_id"].startswith("HTI:")]
    ctrls = sorted({l["control_id"] for l in hl}, key=lambda c: (["GOV", "FUN", "FAIR", "OPS", "HF", "SEC", "CMP", "LSI"].index(c.split("-")[1]), c))
    rows = [h["element_id"] for h in hti]
    val = {"example_of": 1, "precedes": 2, "integral_to": 3}
    M = [[0] * len(ctrls) for _ in rows]
    for l in hl:
        M[rows.index(l["target_id"])][ctrls.index(l["control_id"])] = val[l["property"]]
    cmap = ListedColormap([SURF, BLUE_LIGHT, "#5598e7", BLUE_DARK])
    norm = BoundaryNorm([-0.5, 0.5, 1.5, 2.5, 3.5], 4)
    fig, ax = plt.subplots(figsize=(8.6, 8.4))
    ax.imshow(M, cmap=cmap, norm=norm, aspect="auto")
    cls_short = {"static_at_release": "static", "process_description": "process", "evidence_accruing": "accruing",
                 "locally_measured": "local"}
    labs = []
    for h in hti:
        a = h["attribute"]
        a = (a[:43] + "…") if len(a) > 44 else a
        labs.append(f"{h['element_id'][4:]:<7}{a:<45}{cls_short[h['gapm_change_class']]:>9}")
    ax.set_yticks(range(len(rows)), labs, fontsize=6.4, family="DejaVu Sans Mono")
    ax.set_xticks(range(len(ctrls)), ctrls, rotation=90, fontsize=7)
    ax.xaxis.tick_top()
    ax.set_xticks([x - 0.5 for x in range(1, len(ctrls))], minor=True)
    ax.set_yticks([y - 0.5 for y in range(1, len(rows))], minor=True)
    ax.grid(which="minor", color=GRID, lw=0.5)
    ax.tick_params(which="both", length=0)
    for s in ax.spines.values():
        s.set_color(GRID)
    hs = [plt.Rectangle((0, 0), 1, 1, color=c) for c in (BLUE_DARK, "#5598e7", BLUE_LIGHT)]
    ax.legend(hs, ["integral to", "precedes", "example of"], ncol=3, frameon=False, fontsize=7.5,
              loc="upper center", bbox_to_anchor=(0.4, -0.01))
    fig.subplots_adjust(left=0.555, right=0.99, top=0.9, bottom=0.06)
    stamp(fig); credit(fig)
    fig.savefig(os.path.join(FIG, "fig3_hti_attribute_maintenance.png"), dpi=220)
    plt.close(fig)


def main():
    os.makedirs(FIG, exist_ok=True)
    S = J("report", "stats.json")
    disp = J("data", "crosswalk", "gapm_dispositions.json")
    links = J("data", "crosswalk", "gapm_links.json")
    controls = J("data", "crosswalk", "gapm_controls.json")
    el = J("data", "registry", "elements.json")
    hti = J("data", "crosswalk", "gapm_crosswalk.json")["hti_attributes"]
    fig1(S, disp); fig2(links, controls, el); fig3(links, hti)
    print("figures written", "(FINAL)" if FINAL else ("(RELEASE CANDIDATE)" if rel.get("author_review") == "complete" else "(DRAFT)"))


if __name__ == "__main__":
    main()
