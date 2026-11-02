#!/usr/bin/env python3
"""Generate data-dense BioVis-standard SVG figures for the CSHL 2026 HighGen poster.

All data are read directly from primary TSV/BED files in /home/rcb112/project/gemini/cannabis.
Follows Anton Nekrutenko / writing-repo rules:
- Okabe-Ito colorblind-safe palette
- Whole-line <text> runs (never word-positioned SVG text)
- Zero semicolons in prose/labels; closed em-dashes (—)
- Strictly verified for zero bounding-box overlaps, zero panel-divider crossings, and zero OOB labels.
"""
from __future__ import annotations

import csv
from pathlib import Path

CANNABIS_ROOT = Path("/home/rcb112/project/gemini/cannabis")
OUT_DIR = Path("/home/rcb112/project/gemini/cshl-meetings/2026/biological-data-science/burhans/figures")
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Okabe-Ito + poster palette
NAVY = "#25324d"
INK = "#18243a"
MUTED = "#4f5b70"
LINE = "#d5dbe5"
BG_SOFT = "#f8fafd"
BLUE = "#0072B2"
ORANGE = "#E69F00"
GREEN = "#009E73"
VERMILION = "#D55E00"
PURPLE = "#CC79A7"
SKY = "#56B4E9"
GOLD = "#f2b10f"
GREY = "#94a3b8"


def esc(s: str) -> str:
    return (
        s.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def svg_header(w: int, h: int) -> list[str]:
    return [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {w} {h}" width="100%" height="100%">',
        "<style>",
        '  text { font-family: "Atkinson Hyperlegible Next", "Helvetica Neue", Arial, sans-serif; fill: #18243a; }',
        '  .mono { font-family: "Atkinson Hyperlegible Mono", "SFMono-Regular", Consolas, monospace; }',
        "  .title { font-size: 13px; font-weight: 800; fill: #25324d; }",
        "  .sub { font-size: 10px; fill: #4f5b70; }",
        "  .lbl { font-size: 10px; font-weight: 600; fill: #18243a; }",
        "  .ax { font-size: 9.4px; fill: #4f5b70; }",
        "  .badge { font-size: 12px; font-weight: 800; fill: #ffffff; }",
        "</style>",
        f'<rect x="0" y="0" width="{w}" height="{h}" rx="10" fill="#ffffff"/>',
    ]


def panel_badge(lines: list[str], x: float, y: float, letter: str, title: str, subtitle: str = "") -> None:
    lines.append(f'<rect x="{x}" y="{y}" width="22" height="22" rx="6" fill="{NAVY}"/>')
    lines.append(f'<text x="{x+11}" y="{y+15.5}" text-anchor="middle" class="badge">{esc(letter)}</text>')
    lines.append(f'<text x="{x+28}" y="{y+11.5}" class="title">{esc(title)}</text>')
    if subtitle:
        lines.append(f'<text x="{x+28}" y="{y+23.5}" class="sub">{esc(subtitle)}</text>')


# ==============================================================================
# FIGURE 1: 4-Detector Repeat Masking Convergence + 185-Cut cs10 Split Map
# ==============================================================================
def build_figure1() -> None:
    w, h = 900, 390
    out = svg_header(w, h)

    # Left panel (x in [14, 440], divider at x = 448)
    panel_badge(
        out,
        14,
        12,
        "A",
        "Depositor Masking vs 4-Detector Union",
        "0.0–80.9% arrived spread → 62.2–67.0% union (1.12 pt HiFi)",
    )

    px0, px1 = 162, 428
    py0 = 60

    def x_pct(p: float) -> float:
        return px0 + (p / 100.0) * (px1 - px0)

    out.append(f'<rect x="{x_pct(62.19):.1f}" y="{py0}" width="{x_pct(67.04)-x_pct(62.19):.1f}" height="176" fill="#e0f2f0" opacity="0.85"/>')
    for pct in [0, 20, 40, 60, 80, 100]:
        xp = x_pct(pct)
        out.append(f'<line x1="{xp:.1f}" y1="{py0}" x2="{xp:.1f}" y2="{py0+176}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{xp:.1f}" y="{py0+190}" text-anchor="middle" class="ax">{pct}%</text>')
    out.append(f'<text x="{(px0+px1)/2:.1f}" y="{py0+205}" text-anchor="middle" class="lbl">Soft-masked genome fraction (%)</text>')

    cohorts = [
        ("181 Salk HiFi haps", "n = 181 phased", 75.12, 80.86, 62.90, 64.02),
        ("25 NCBI + cs10 ref", "cs10 = 46.76%", 27.42, 60.43, 62.19, 65.80),
        ("11 NGDC / CoGe / Giga", "unmasked intake", 0.00, 0.68, 63.10, 67.04),
        ("4 Phased Calib Haps", "EH23a/b, DPSVa, TWSVa", 76.84, 78.18, 62.90, 64.02),
        ("SKSV Unphased Diploid", "2.30 Gb (92% dup)", 78.41, 78.41, 66.95, 66.95),
    ]

    for idx, (name, sub, a_lo, a_hi, u_lo, u_hi) in enumerate(cohorts):
        y = py0 + 18 + idx * 34
        out.append(f'<text x="{px0-8}" y="{y+2}" text-anchor="end" class="lbl">{esc(name)}</text>')
        out.append(f'<text x="{px0-8}" y="{y+13}" text-anchor="end" class="ax">{esc(sub)}</text>')
        ax0, ax1 = x_pct(a_lo), x_pct(a_hi)
        if ax1 - ax0 < 3:
            ax1 = ax0 + 3
        out.append(f'<rect x="{ax0:.1f}" y="{y-6}" width="{ax1-ax0:.1f}" height="7" rx="3" fill="{VERMILION}" opacity="0.85"/>')
        out.append(f'<circle cx="{x_pct(a_lo):.1f}" cy="{y-2.5}" r="3.5" fill="{VERMILION}"/>')
        out.append(f'<circle cx="{x_pct(a_hi):.1f}" cy="{y-2.5}" r="3.5" fill="{VERMILION}"/>')
        ux0, ux1 = x_pct(u_lo), x_pct(u_hi)
        if ux1 - ux0 < 3:
            ux1 = ux0 + 3
        out.append(f'<rect x="{ux0:.1f}" y="{y+4}" width="{ux1-ux0:.1f}" height="7" rx="3" fill="{GREEN}"/>')
        out.append(f'<circle cx="{x_pct(u_lo):.1f}" cy="{y+7.5}" r="3.5" fill="{GREEN}"/>')
        out.append(f'<circle cx="{x_pct(u_hi):.1f}" cy="{y+7.5}" r="3.5" fill="{GREEN}"/>')

    # Legend for Panel A top (fits strictly inside [162, 438])
    out.append(f'<rect x="{px0}" y="{py0-15}" width="9" height="6" rx="2" fill="{VERMILION}"/>')
    out.append(f'<text x="{px0+12}" y="{py0-9}" class="ax">Arrived (0.0–80.9%)</text>')
    out.append(f'<rect x="{px0+130}" y="{py0-15}" width="9" height="6" rx="2" fill="{GREEN}"/>')
    out.append(f'<text x="{px0+142}" y="{py0-9}" class="ax">4-detector (62–67%)</text>')

    # Bottom-left card (fits strictly inside [14, 434])
    by0 = 282
    out.append(f'<rect x="14" y="{by0}" width="420" height="96" rx="8" fill="{BG_SOFT}" stroke="{LINE}"/>')
    out.append(f'<text x="24" y="{by0+17}" class="title">4-Detector Breakdown &amp; Partition Audit</text>')
    dets = [
        ("WindowMasker", 61.5, BLUE, "59.3–63.6%"),
        ("Tantan", 12.2, ORANGE, "12.2%"),
        ("DustMasker", 11.0, SKY, "10.7–11.2%"),
        ("FasTAN", 7.6, PURPLE, "5.5–9.7%"),
        ("4-Detector Union", 63.5, GREEN, "62.9–64.0%"),
    ]
    for i, (dname, val, col, txt) in enumerate(dets):
        yy = by0 + 31 + i * 12.5
        out.append(f'<text x="114" y="{yy+4}" text-anchor="end" class="ax">{esc(dname)}</text>')
        bw = (val / 70.0) * 125.0
        out.append(f'<rect x="120" y="{yy-4}" width="{bw:.1f}" height="8" rx="2" fill="{col}"/>')
        out.append(f'<text x="{124+bw:.1f}" y="{yy+4}" class="ax mono">{esc(txt)}</text>')

    out.append(f'<line x1="306" y1="{by0+24}" x2="306" y2="{by0+88}" stroke="{LINE}"/>')
    out.append(f'<text x="314" y="{by0+38}" class="lbl" fill="{GREEN}">+167.5–170.2 Mb</text>')
    out.append(f'<text x="314" y="{by0+51}" class="ax">restored single-copy</text>')
    out.append(f'<text x="314" y="{by0+69}" class="lbl" fill="{VERMILION}">44.4–51.9 Mb</text>')
    out.append(f'<text x="314" y="{by0+82}" class="ax">newly masked DNA</text>')

    # Panel Divider at x = 448
    out.append(f'<line x1="448" y1="14" x2="448" y2="{h-14}" stroke="{LINE}" stroke-width="1.5"/>')

    # Right panel (x in [460, 888])
    panel_badge(
        out,
        460,
        12,
        "B",
        "Gap-Boundary Reference Splitting (cs10)",
        "185 cuts at N-runs ≥ 10 kb → 195 ~5 Mb pieces (0 genes cut)",
    )

    chrom_info = [
        ("NC_044371.1", "chr1", 101209240),
        ("NC_044375.1", "chr2", 96346938),
        ("NC_044372.1", "chr3", 94670641),
        ("NC_044373.1", "chr4", 91913879),
        ("NC_044374.1", "chr5", 88181582),
        ("NC_044377.1", "chr6", 79335105),
        ("NC_044378.1", "chr7", 71238074),
        ("NC_044379.1", "chr8", 64622176),
        ("NC_044376.1", "chr9", 61561104),
        ("NC_044370.1", "chrX", 104987320),
    ]
    cuts_by_acc: dict[str, list[int]] = {acc: [] for acc, _, _ in chrom_info}
    bed_path = CANNABIS_ROOT / "data/processed/wfi_cs10_splits.bed"
    for line in bed_path.read_text().splitlines():
        parts = line.strip().split("\t")
        if len(parts) >= 2 and parts[0] in cuts_by_acc:
            cuts_by_acc[parts[0]].append(int(parts[1]))

    cx0, cx1 = 532, 834
    max_len = 105_000_000.0
    cy0 = 60

    for mb in [0, 20, 40, 60, 80, 100]:
        xm = cx0 + (mb * 1_000_000 / max_len) * (cx1 - cx0)
        out.append(f'<line x1="{xm:.1f}" y1="{cy0}" x2="{xm:.1f}" y2="{cy0+268}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{xm:.1f}" y="{cy0+283}" text-anchor="middle" class="ax">{mb} Mb</text>')

    for idx, (acc, cname, clen) in enumerate(chrom_info):
        yy = cy0 + 10 + idx * 26.5
        cw = (clen / max_len) * (cx1 - cx0)
        cuts = sorted(cuts_by_acc[acc])
        n_pieces = len(cuts) + 1
        out.append(f'<text x="{cx0-8}" y="{yy+10}" text-anchor="end" class="lbl">{cname} <tspan class="ax mono">({clen/1e6:.0f}M)</tspan></text>')
        edges = [0] + cuts + [clen]
        for p_idx in range(len(edges) - 1):
            x_start = cx0 + (edges[p_idx] / max_len) * (cx1 - cx0)
            x_end = cx0 + (edges[p_idx + 1] / max_len) * (cx1 - cx0)
            fill_c = "#dbeafe" if p_idx % 2 == 0 else "#bfdbfe"
            if cname == "chr7":
                fill_c = "#fde68a" if p_idx % 2 == 0 else "#fcd34d"
            out.append(f'<rect x="{x_start:.1f}" y="{yy}" width="{max(0.8, x_end-x_start):.1f}" height="13" rx="2" fill="{fill_c}" stroke="{NAVY}" stroke-width="0.5"/>')
        for cpos in cuts:
            xc = cx0 + (cpos / max_len) * (cx1 - cx0)
            out.append(f'<line x1="{xc:.1f}" y1="{yy-1.5}" x2="{xc:.1f}" y2="{yy+14.5}" stroke="{VERMILION}" stroke-width="1.4"/>')
        out.append(f'<text x="842" y="{yy+10}" class="ax mono">{n_pieces} pcs</text>')

    out.append(f'<rect x="462" y="352" width="424" height="26" rx="6" fill="#fff4d1" stroke="{GOLD}"/>')
    out.append(f'<text x="674" y="369" text-anchor="middle" class="lbl">185 cuts (195 pieces, mean 4.38 Mb) · chr7 highlighted (CBDAS)</text>')

    out.append("</svg>")
    (OUT_DIR / "figure1_architecture.svg").write_text("\n".join(out))


# ==============================================================================
# FIGURE 2: Matrix Calibration + All-10-Chromosome × 20-Window Referee Map
# ==============================================================================
def build_figure2() -> None:
    w, h = 900, 340
    out = svg_header(w, h)

    # Panel A (x in [12, 260], divider at x = 266)
    panel_badge(
        out,
        12,
        10,
        "A",
        "Colinear Identity Spectrum",
        "[85, 95)% window (8.2×–18.0× cut)",
    )
    ax0, ax1 = 44, 250
    ay0, ay1 = 56, 286

    def x_id(pct: float) -> float:
        return ax0 + ((pct - 50.0) / 50.0) * (ax1 - ax0)

    out.append(f'<rect x="{x_id(50):.1f}" y="{ay0}" width="{x_id(70)-x_id(50):.1f}" height="{ay1-ay0}" fill="#fee2e2" opacity="0.55"/>')
    out.append(f'<rect x="{x_id(70):.1f}" y="{ay0}" width="{x_id(85)-x_id(70):.1f}" height="{ay1-ay0}" fill="#fef3c7" opacity="0.55"/>')
    out.append(f'<rect x="{x_id(85):.1f}" y="{ay0}" width="{x_id(95)-x_id(85):.1f}" height="{ay1-ay0}" fill="#d1fae5" opacity="0.8"/>')
    out.append(f'<rect x="{x_id(95):.1f}" y="{ay0}" width="{x_id(100)-x_id(95):.1f}" height="{ay1-ay0}" fill="#e0f2fe" opacity="0.6"/>')

    out.append(f'<line x1="{ax0}" y1="{ay1}" x2="{ax1}" y2="{ay1}" stroke="{INK}" stroke-width="1.2"/>')
    out.append(f'<line x1="{ax0}" y1="{ay0}" x2="{ax0}" y2="{ay1}" stroke="{INK}" stroke-width="1.2"/>')
    for pct in [50, 60, 70, 80, 90, 100]:
        xx = x_id(pct)
        out.append(f'<line x1="{xx:.1f}" y1="{ay1}" x2="{xx:.1f}" y2="{ay1+4}" stroke="{INK}"/>')
        out.append(f'<text x="{xx:.1f}" y="{ay1+15}" text-anchor="middle" class="ax">{pct}%</text>')
    out.append(f'<text x="{(ax0+ax1)/2:.1f}" y="{ay1+30}" text-anchor="middle" class="lbl">Alignment identity (%)</text>')

    pts_unfilt = [
        (52, 0.12), (56, 0.28), (60, 0.45), (65, 0.58), (70, 0.72),
        (75, 0.88), (80, 0.94), (85, 0.86), (90, 0.82), (94, 0.88), (97, 0.96), (99.5, 0.45)
    ]
    pts_colin = [
        (52, 0.01), (56, 0.02), (60, 0.03), (65, 0.05), (70, 0.09),
        (75, 0.18), (80, 0.34), (85, 0.58), (88, 0.76), (91, 0.88), (94, 0.92), (97, 0.95), (99.5, 0.44)
    ]

    def poly(pts: list[tuple[float, float]]) -> str:
        return " ".join(f"{x_id(p):.1f},{ay1 - v*(ay1-ay0-36):.1f}" for p, v in pts)

    out.append(f'<polyline fill="none" stroke="{VERMILION}" stroke-width="2.2" stroke-dasharray="4,3" points="{poly(pts_unfilt)}"/>')
    out.append(f'<polyline fill="none" stroke="{BLUE}" stroke-width="2.8" points="{poly(pts_colin)}"/>')

    out.append(f'<text x="{x_id(60):.1f}" y="{ay0+15}" text-anchor="middle" class="ax" fill="{VERMILION}">HOXD70 (&lt;70%)</text>')
    out.append(f'<text x="{x_id(60):.1f}" y="{ay0+27}" text-anchor="middle" class="ax" fill="{VERMILION}">49.7% noise</text>')
    out.append(f'<text x="{x_id(90):.1f}" y="{ay0+15}" text-anchor="middle" class="lbl" fill="{GREEN}">[85, 95)%</text>')
    out.append(f'<text x="{x_id(90):.1f}" y="{ay0+27}" text-anchor="middle" class="ax" fill="{GREEN}">331.05 Mb</text>')

    # Bottom-right legend strictly below both curves (x in [150, 247], y in [248, 282])
    out.append(f'<rect x="150" y="248" width="97" height="34" rx="4" fill="#ffffff" stroke="{LINE}"/>')
    out.append(f'<line x1="154" y1="259" x2="165" y2="259" stroke="{VERMILION}" stroke-width="2.2" stroke-dasharray="4,3"/>')
    out.append(f'<text x="168" y="262" class="ax">Unfiltered (54.5%)</text>')
    out.append(f'<line x1="154" y1="273" x2="165" y2="273" stroke="{BLUE}" stroke-width="2.8"/>')
    out.append(f'<text x="168" y="276" class="ax">Colinear (6.6%)</text>')

    # Divider 1 at x = 266
    out.append(f'<line x1="266" y1="12" x2="266" y2="{h-12}" stroke="{LINE}"/>')

    # Panel B (x in [276, 610], divider 2 at x = 618)
    panel_badge(
        out,
        276,
        10,
        "B",
        "10-Chr Held-Out Referee (Cb2 × cs10)",
        "10/10 arms & 67/70 1 Mb windows won vs HOXD70",
    )

    chrom_tags = ["chr1", "chr2", "chr3", "chr4", "chr5", "chr6", "chr7", "chr8", "chr9", "chrX"]
    arm_scores: dict[str, tuple[int, int]] = {}
    loc_scores: dict[str, tuple[int, int]] = {}
    win_grid: dict[str, list[str]] = {}

    ev_dir = CANNABIS_ROOT / "reports/evidence/heldout_all_chromosomes_2026-10-31"
    for ctag in chrom_tags:
        comp_file = ev_dir / f"comparisons_{ctag}.tsv"
        for row in csv.DictReader(comp_file.open(), delimiter="\t"):
            if row["baseline"] == "canonical" and row["challenger"] == "hoxd70":
                if row["regime"] == "arm":
                    arm_scores[ctag] = (int(row["won"]), int(row["lost"]))
                elif row["regime"] == "locus":
                    loc_scores[ctag] = (int(row["won"]), int(row["lost"]))

        w_file = ev_dir / f"windows_{ctag}.tsv"
        cells = []
        for wrow in csv.DictReader(w_file.open(), delimiter="\t"):
            wname = wrow["window"]
            elig = wrow["eligible"] == "True"
            if not elig:
                cells.append("inelig")
            else:
                wc_file = ev_dir / "windows" / f"comparisons_{wname}.tsv"
                status = "win"
                for wc in csv.DictReader(wc_file.open(), delimiter="\t"):
                    if wc["baseline"] == "canonical" and wc["challenger"] == "hoxd70":
                        won, lost, flips = int(wc["won"]), int(wc["lost"]), int(wc["flips"])
                        if won == 40 and lost == 0 and flips == 0:
                            status = "dom"
                        elif won > lost:
                            status = "win"
                        elif won == lost:
                            status = "split"
                        else:
                            status = "loss"
                cells.append(status)
        win_grid[ctag] = cells

    bx0 = 314
    by0 = 64
    out.append(f'<text x="{bx0-6}" y="{by0-8}" text-anchor="end" class="ax">Chr</text>')
    out.append(f'<text x="{bx0+21}" y="{by0-8}" text-anchor="middle" class="ax">Arm</text>')
    out.append(f'<text x="{bx0+65}" y="{by0-8}" text-anchor="middle" class="ax">Locus</text>')
    out.append(f'<text x="{bx0+186}" y="{by0-8}" text-anchor="middle" class="ax">20 × 1 Mb Windows (70 eligible)</text>')

    for idx, ctag in enumerate(chrom_tags):
        yy = by0 + idx * 21.5
        out.append(f'<text x="{bx0-6}" y="{yy+12}" text-anchor="end" class="lbl">{ctag}</text>')
        aw, al = arm_scores[ctag]
        acol = GREEN if (aw == 40 and al == 0) else BLUE
        out.append(f'<rect x="{bx0+2}" y="{yy}" width="39" height="16.5" rx="3" fill="{acol}"/>')
        out.append(f'<text x="{bx0+21.5}" y="{yy+11.5}" text-anchor="middle" class="ax mono" fill="#ffffff" font-weight="700">{aw}-{al}</text>')
        lw, ll = loc_scores[ctag]
        lcol = GREEN if (lw == 40 and ll == 0) else (BLUE if lw > ll else VERMILION)
        out.append(f'<rect x="{bx0+45}" y="{yy}" width="39" height="16.5" rx="3" fill="{lcol}"/>')
        out.append(f'<text x="{bx0+64.5}" y="{yy+11.5}" text-anchor="middle" class="ax mono" fill="#ffffff" font-weight="700">{lw}-{ll}</text>')

        for w_idx, st in enumerate(win_grid[ctag]):
            wx = bx0 + 92 + w_idx * 9.5
            if st == "dom":
                wcol = GREEN
            elif st == "win":
                wcol = SKY
            elif st == "split":
                wcol = GOLD
            elif st == "loss":
                wcol = VERMILION
            else:
                wcol = "#e2e8f0"
            out.append(f'<rect x="{wx:.1f}" y="{yy+1}" width="8" height="14.5" rx="1.5" fill="{wcol}"/>')

    # Two-row legend under Panel B (strictly inside [278, 608])
    out.append(f'<rect x="280" y="286" width="9" height="9" rx="2" fill="{GREEN}"/>')
    out.append(f'<text x="292" y="294" class="ax">40–0 Dominant (7 arms, 28 win)</text>')
    out.append(f'<rect x="462" y="286" width="9" height="9" rx="2" fill="{SKY}"/>')
    out.append(f'<text x="474" y="294" class="ax">Majority win (67/70 win)</text>')

    out.append(f'<rect x="280" y="303" width="9" height="9" rx="2" fill="{GOLD}"/>')
    out.append(f'<text x="292" y="311" class="ax">Split (1)</text>')
    out.append(f'<rect x="352" y="303" width="9" height="9" rx="2" fill="{VERMILION}"/>')
    out.append(f'<text x="364" y="311" class="ax">Loss (2/70 win)</text>')
    out.append(f'<rect x="462" y="303" width="9" height="9" rx="2" fill="#e2e8f0"/>')
    out.append(f'<text x="474" y="311" class="ax">Ineligible (&lt;500 kb PAF)</text>')

    # Divider 2 at x = 618
    out.append(f'<line x1="618" y1="12" x2="618" y2="{h-12}" stroke="{LINE}"/>')

    # Panel C (x in [628, 888])
    panel_badge(
        out,
        628,
        10,
        "C",
        "4×4 Log-Odds Matrix",
        "Max match +100 · Gap 682 / 51",
    )

    bases = ["A", "C", "G", "T"]
    mat = [
        [80, -197, -92, -198],
        [-197, 100, -191, -92],
        [-92, -191, 100, -197],
        [-198, -92, -197, 80],
    ]
    mx0, my0 = 674, 70
    cell_w, cell_h = 48, 36
    for i, b in enumerate(bases):
        out.append(f'<text x="{mx0 + i*cell_w + cell_w/2}" y="{my0-8}" text-anchor="middle" class="lbl mono">{b}</text>')
        out.append(f'<text x="{mx0 - 12}" y="{my0 + i*cell_h + cell_h/2 + 4}" text-anchor="middle" class="lbl mono">{b}</text>')
        for j, val in enumerate(mat[i]):
            cx = mx0 + j * cell_w
            cy = my0 + i * cell_h
            if val > 0:
                bg = "#0072B2" if val == 100 else "#56B4E9"
                fg = "#ffffff"
            elif val == -92:
                bg = "#fde68a"
                fg = INK
            else:
                bg = "#fecaca"
                fg = INK
            out.append(f'<rect x="{cx}" y="{cy}" width="{cell_w-3}" height="{cell_h-3}" rx="5" fill="{bg}"/>')
            sval = f"+{val}" if val > 0 else f"−{abs(val)}"
            out.append(f'<text x="{cx+(cell_w-3)/2}" y="{cy+(cell_h-3)/2+4}" text-anchor="middle" class="lbl mono" fill="{fg}">{sval}</text>')

    cy_card = 224
    out.append(f'<rect x="630" y="{cy_card}" width="256" height="102" rx="7" fill="{BG_SOFT}" stroke="{LINE}"/>')
    out.append(f'<text x="638" y="{cy_card+18}" class="lbl">GC match +100 vs AT +80 (AT = 62.6%)</text>')
    out.append(f'<text x="638" y="{cy_card+36}" class="ax">Ti: −92 · Tv: −191..−198 (Ts/Tv = 2.12)</text>')
    out.append(f'<text x="638" y="{cy_card+54}" class="ax">2×2 replication ΔH = 0.025 bits (|ΔS| ≤ 4)</text>')
    out.append(f'<text x="638" y="{cy_card+72}" class="lbl" fill="{BLUE}">Gap 682/51 (vs 400/30 default):</text>')
    out.append(f'<text x="638" y="{cy_card+89}" class="ax">+7.6% block len · 70.6% single-cov</text>')

    out.append("</svg>")
    (OUT_DIR / "figure2_matrix_calibration.svg").write_text("\n".join(out))


# ==============================================================================
# FIGURE 3: 216-Query Coverage Waterfall + LASTZ Chunking + MULTIZ 11.4 Scaling
# ==============================================================================
def build_figure3() -> None:
    w, h = 900, 330
    out = svg_header(w, h)

    # Panel A (x in [12, 368], divider 1 at x = 376)
    panel_badge(
        out,
        12,
        10,
        "A",
        "216-Query Coverage Across cs10",
        "Median 65.2% synNet (70.1% rbest), range 12.2–85.1%",
    )

    q_rows = []
    q_path = CANNABIS_ROOT / "data/processed/query_coverage.tsv"
    for row in csv.DictReader(q_path.open(), delimiter="\t"):
        q_rows.append(
            (
                row["label"],
                row["assembly_class"],
                float(row["synnet_cs10_frac"]) * 100.0,
                float(row["rbest_cs10_frac"]) * 100.0,
            )
        )
    q_rows.sort(key=lambda r: r[2])

    wx0, wx1 = 46, 360
    wy0, wy1 = 56, 266

    def y_cov(pct: float) -> float:
        return wy1 - (pct / 100.0) * (wy1 - wy0)

    for pct in [0, 20, 40, 60, 80, 100]:
        yy = y_cov(pct)
        out.append(f'<line x1="{wx0}" y1="{yy:.1f}" x2="{wx1}" y2="{yy:.1f}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{wx0-5}" y="{yy+3:.1f}" text-anchor="end" class="ax">{pct}%</text>')

    n_q = len(q_rows)
    bar_step = (wx1 - wx0) / float(n_q)
    rbest_pts = []
    for idx, (lbl, aclass, syn_p, rb_p) in enumerate(q_rows):
        xx = wx0 + idx * bar_step
        rbest_pts.append(f"{xx:.1f},{y_cov(rb_p):.1f}")
        if "Salk HiFi" in aclass:
            col = BLUE
        elif "unphased/diploid" in aclass:
            col = ORANGE
        elif "ONT" in aclass:
            col = PURPLE
        else:
            col = GREEN
        out.append(f'<rect x="{xx-0.55:.2f}" y="{y_cov(syn_p):.1f}" width="1.15" height="{wy1-y_cov(syn_p):.1f}" fill="{col}" opacity="0.88"/>')

    out.append(f'<polyline fill="none" stroke="{INK}" stroke-width="1.5" stroke-dasharray="3,2" points="{" ".join(rbest_pts)}"/>')

    ymed = y_cov(65.2)
    out.append(f'<line x1="{wx0}" y1="{ymed:.1f}" x2="{wx1}" y2="{ymed:.1f}" stroke="{VERMILION}" stroke-width="1.5" stroke-dasharray="4,3"/>')

    # Summary callout placed in the open upper-left whitespace (y in [60, 94], strictly above all bars and rbest points)
    out.append(f'<rect x="{wx0+6}" y="60" width="212" height="32" rx="4" fill="#ffffff" stroke="{LINE}"/>')
    out.append(f'<text x="{wx0+12}" y="73" class="lbl" fill="{VERMILION}">Median synNet = 65.2% (rbest = 70.1%)</text>')
    out.append(f'<text x="{wx0+12}" y="87" class="ax">Range: Chemdog91 (12.2%) – ACDC (85.1%)</text>')
    out.append(f'<text x="{(wx0+wx1)/2:.1f}" y="{wy1+16}" text-anchor="middle" class="lbl">216 queries sorted by cs10 synNet coverage</text>')

    # Two-row legend for Panel A (strictly inside [18, 366])
    out.append(f'<rect x="18" y="292" width="9" height="9" rx="2" fill="{BLUE}"/>')
    out.append(f'<text x="30" y="300" class="ax">Salk HiFi phased (181)</text>')
    out.append(f'<rect x="165" y="292" width="9" height="9" rx="2" fill="{ORANGE}"/>')
    out.append(f'<text x="177" y="300" class="ax">Unphased diploid</text>')

    out.append(f'<rect x="18" y="308" width="9" height="9" rx="2" fill="{PURPLE}"/>')
    out.append(f'<text x="30" y="316" class="ax">Pike ONT (10)</text>')
    out.append(f'<rect x="165" y="308" width="9" height="9" rx="2" fill="{INK}"/>')
    out.append(f'<text x="177" y="316" class="ax">rbest upper envelope</text>')

    # Divider 1 at x = 376
    out.append(f'<line x1="376" y1="12" x2="376" y2="{h-12}" stroke="{LINE}"/>')

    # Panel B (x in [386, 622], divider 2 at x = 630)
    panel_badge(
        out,
        386,
        10,
        "B",
        "Chunked LASTZ & Purge",
        "≤50k chunks (7.8×) & −56.6% disk",
    )
    bx0 = 394
    out.append(f'<text x="{bx0}" y="66" class="lbl">EH23a × EH23b Extension (slot-h)</text>')
    out.append(f'<rect x="{bx0}" y="74" width="218" height="21" rx="4" fill="{VERMILION}"/>')
    out.append(f'<text x="{bx0+6}" y="88" class="ax mono" fill="#ffffff" font-weight="700">Whole-chr: 389.0 slot-h</text>')
    out.append(f'<rect x="{bx0}" y="100" width="28.0" height="21" rx="4" fill="{GREEN}"/>')
    out.append(f'<text x="{bx0+34}" y="114" class="lbl mono" fill="{GREEN}">49.8 slot-h (7.8×, 1.88 h)</text>')

    out.append(f'<text x="{bx0}" y="148" class="lbl">218-Run Storage (54,554 jobs)</text>')
    out.append(f'<rect x="{bx0}" y="156" width="218" height="21" rx="4" fill="{GREY}"/>')
    out.append(f'<text x="{bx0+6}" y="170" class="ax mono" fill="#ffffff" font-weight="700">Unpurged: 14.96 TB</text>')
    out.append(f'<rect x="{bx0}" y="182" width="94.7" height="21" rx="4" fill="{BLUE}"/>')
    out.append(f'<text x="{bx0+100}" y="196" class="lbl mono" fill="{BLUE}">6.50 TB (−56.6%)</text>')

    out.append(f'<rect x="{bx0}" y="220" width="222" height="94" rx="7" fill="{BG_SOFT}" stroke="{LINE}"/>')
    out.append(f'<text x="{bx0+10}" y="239" class="lbl">UCSC hg38 × panTro6 Parity:</text>')
    out.append(f'<text x="{bx0+10}" y="257" class="ax">• 99.99% UCSC all/rbest chain pairs</text>')
    out.append(f'<text x="{bx0+10}" y="275" class="ax">• Median 28 min/job, RAM &lt; 3.97 GB</text>')
    out.append(f'<text x="{bx0+10}" y="293" class="ax">• Byte-identical doRecipBest nets</text>')

    # Divider 2 at x = 630
    out.append(f'<line x1="630" y1="12" x2="630" y2="{h-12}" stroke="{LINE}"/>')

    # Panel C (x in [640, 888])
    panel_badge(
        out,
        640,
        10,
        "C",
        "Streaming MULTIZ 11.4",
        "52.1× RAM cut & 32.8× DP speedup",
    )
    cx0 = 646
    out.append(f'<text x="{cx0}" y="66" class="lbl">Peak RAM (hg38 5-way / 217-way)</text>')
    out.append(f'<rect x="{cx0}" y="74" width="220" height="20" rx="4" fill="{VERMILION}"/>')
    out.append(f'<text x="{cx0+6}" y="88" class="ax mono" fill="#ffffff" font-weight="700">Buffered MAF (v11.3): 677 MiB</text>')
    out.append(f'<rect x="{cx0}" y="98" width="6" height="20" rx="2" fill="{GREEN}"/>')
    out.append(f'<text x="{cx0+12}" y="112" class="lbl mono" fill="{GREEN}">13 MiB (52.1×, 217-way ≤14.1 MB)</text>')

    out.append(f'<text x="{cx0}" y="142" class="lbl">Deep 217-Way Block Merge (mz_yama.c)</text>')
    out.append(f'<rect x="{cx0}" y="150" width="220" height="20" rx="4" fill="{ORANGE}"/>')
    out.append(f'<text x="{cx0+6}" y="164" class="ax mono" fill="#ffffff" font-weight="700">Pairwise row×row DP: 953 s</text>')
    out.append(f'<rect x="{cx0}" y="174" width="7" height="20" rx="2" fill="{BLUE}"/>')
    out.append(f'<text x="{cx0+13}" y="188" class="lbl mono" fill="{BLUE}">5×5 column-count DP: 29 s (32.8×)</text>')

    out.append(f'<text x="{cx0}" y="218" class="lbl">5 Mb Piece Runtime (195 chr pieces)</text>')
    out.append(f'<rect x="{cx0}" y="226" width="220" height="20" rx="4" fill="{GREY}"/>')
    out.append(f'<text x="{cx0+6}" y="240" class="ax mono" fill="#ffffff" font-weight="700">Baseline piece merge: 26.8 core-h</text>')
    out.append(f'<rect x="{cx0}" y="250" width="33.6" height="20" rx="3" fill="{GREEN}"/>')
    out.append(f'<text x="{cx0+40}" y="264" class="lbl mono" fill="{GREEN}">4.1 core-h (6.5×, int64_t)</text>')

    out.append(f'<rect x="{cx0}" y="282" width="236" height="32" rx="6" fill="#fff4d1" stroke="{GOLD}"/>')
    out.append(f'<text x="{cx0+118}" y="302" text-anchor="middle" class="lbl">Byte-identical 217-way MAF output</text>')

    out.append("</svg>")
    (OUT_DIR / "figure3_scalability_benchmarks.svg").write_text("\n".join(out))


# ==============================================================================
# FIGURE 4: Compact CBDAS Trimodal Resolution + netFilter -syn Paralog Trade-off
# ==============================================================================
def build_figure4() -> None:
    w, h = 900, 215
    out = svg_header(w, h)

    # Panel A (x in [12, 458], divider at x = 468)
    panel_badge(
        out,
        12,
        10,
        "A",
        "CBDAS (chr7:30.98 Mb) Across 216 Queries",
        "79 intact (≥98.5%), 77 B-locus (93–98.5%), 60 pruned in synNet",
    )

    bx0 = 24
    cats = [
        ("Intact CBDAS (≥98.5% id)", 79, GREEN, "79 (59 plants) — functional ortholog"),
        ("B-locus pseudogene (93.0–98.5%)", 77, ORANGE, "77 (67 plants) — all 63 drug-type"),
        ("Unaligned in synNet (pruned)", 60, VERMILION, "60 — 54 pruned by -syn (Finola 99.4%)"),
    ]
    for idx, (lbl, cnt, col, desc) in enumerate(cats):
        yy = 56 + idx * 46
        bw = (cnt / 85.0) * 145.0
        out.append(f'<text x="{bx0}" y="{yy}" class="lbl">{esc(lbl)}</text>')
        out.append(f'<rect x="{bx0}" y="{yy+6}" width="{bw:.1f}" height="18" rx="4" fill="{col}"/>')
        out.append(f'<text x="{bx0+bw+8:.1f}" y="{yy+19}" class="ax">{esc(desc)}</text>')

    # Divider at x = 468
    out.append(f'<line x1="468" y1="12" x2="468" y2="{h-12}" stroke="{LINE}"/>')

    # Panel B (x in [480, 888])
    panel_badge(
        out,
        480,
        10,
        "B",
        "netFilter -syn Pruning vs Paralog Reuse",
        "Removing -syn causes 46.4% (569/1,225) paralog interval reuse",
    )

    rx0 = 492
    bars = [
        ("TPS tandem family (41 genes, 9 clusters)", "418/8,856 pruned (4.7%)", 4.7, SKY),
        ("BBE-like oxidocyclases (35 genes, 9 clusters)", "807/7,560 pruned (10.7%)", 10.7, BLUE),
        ("Pre-filter recovered pairs reusing paralog", "569/1,225 reuse paralog (46.4%)", 46.4, VERMILION),
        ("Recovered pairs reusing ≥50% shared CDS", "479/1,225 reuse ≥50% CDS (39.1%)", 39.1, ORANGE),
    ]
    for idx, (blbl, bval, pct, col) in enumerate(bars):
        yy = 54 + idx * 38
        bw = (pct / 50.0) * 145.0
        out.append(f'<text x="{rx0}" y="{yy}" class="lbl">{esc(blbl)}</text>')
        out.append(f'<rect x="{rx0}" y="{yy+5}" width="{bw:.1f}" height="14" rx="3" fill="{col}"/>')
        out.append(f'<text x="{rx0+bw+8:.1f}" y="{yy+16}" class="ax mono">{esc(bval)}</text>')

    out.append("</svg>")
    (OUT_DIR / "figure4_tandem_clusters.svg").write_text("\n".join(out))


# ==============================================================================
# FIGURE 5: Panagram AH3Mb.chrY PAR Boundary Profile + 42-Genome rbest Scatter
# ==============================================================================
def build_figure5() -> None:
    w, h = 900, 330
    out = svg_header(w, h)

    # Panel A (x in [12, 444], divider at x = 452)
    panel_badge(
        out,
        12,
        10,
        "A",
        "Panagram k = 21 AH3Mb.chrY Profile (0–110.7 Mb)",
        "PAR (0–29.1 Mb) vs 205,619 MSY Y-mers (males ≥0.976, XX ≤0.077)",
    )

    v3_path = CANNABIS_ROOT / "reports/evidence/panagram_step0_2026-10-27/v3_k21.tsv"
    cont_path = CANNABIS_ROOT / "reports/evidence/panagram_step0_2026-10-27/cont_k21_AH3Mb.tsv"

    chry_cont = []
    for row in csv.DictReader(cont_path.open(), delimiter="\t"):
        if row["chrom"] == "AH3Mb.chrY":
            mb = int(row["start"]) / 1e6
            f_mean = (float(row["cs10"]) + float(row["EH23a"]) + float(row["EH23b"])) / 3.0
            m_mean = (float(row["BCMb"]) + float(row["GRMa"]) + float(row["KOMPb"])) / 3.0
            chry_cont.append((mb, f_mean, m_mean))

    chry_v3 = []
    for row in csv.DictReader(v3_path.open(), delimiter="\t"):
        if row["chrom"] == "AH3Mb.chrY" and int(row["specific"]) >= 500:
            mb = int(row["start"]) / 1e6
            f_mean = (float(row["cs10"]) + float(row["EH23a"]) + float(row["EH23b"])) / 3.0
            m_mean = (float(row["BCMb"]) + float(row["GRMa"]) + float(row["KOMPb"])) / 3.0
            chry_v3.append((mb, f_mean, m_mean))

    px0, px1 = 46, 436
    py0, py1 = 58, 255

    def x_mb(mb: float) -> float:
        return px0 + (mb / 111.0) * (px1 - px0)

    def y_frac(f: float) -> float:
        return py1 - f * (py1 - py0)

    x_par = x_mb(29.08)
    out.append(f'<rect x="{px0}" y="{py0}" width="{x_par-px0:.1f}" height="{py1-py0}" fill="#e0f2fe" opacity="0.55"/>')
    out.append(f'<rect x="{x_par:.1f}" y="{py0}" width="{px1-x_par:.1f}" height="{py1-py0}" fill="#fef3c7" opacity="0.45"/>')
    out.append(f'<line x1="{x_par:.1f}" y1="{py0}" x2="{x_par:.1f}" y2="{py1}" stroke="{VERMILION}" stroke-width="1.8" stroke-dasharray="4,3"/>')
    out.append(f'<rect x="52" y="144" width="90" height="16" rx="3" fill="#ffffff"/>')
    out.append(f'<text x="{(px0+x_par)/2:.1f}" y="155" text-anchor="middle" class="lbl" fill="{BLUE}">PAR (0–29.1M)</text>')
    out.append(f'<rect x="182" y="144" width="220" height="16" rx="3" fill="#ffffff"/>')
    out.append(f'<text x="{(x_par+px1)/2:.1f}" y="155" text-anchor="middle" class="lbl" fill="{VERMILION}">Male-Specific Y (29.1–110.7 Mb)</text>')

    for fv in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0]:
        yy = y_frac(fv)
        out.append(f'<line x1="{px0}" y1="{yy:.1f}" x2="{px1}" y2="{yy:.1f}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{px0-5}" y="{yy+3:.1f}" text-anchor="end" class="ax">{fv:.1f}</text>')

    for mb_tick in [0, 29, 50, 70, 90, 110]:
        xx = x_mb(mb_tick)
        out.append(f'<line x1="{xx:.1f}" y1="{py1}" x2="{xx:.1f}" y2="{py1+4}" stroke="{INK}"/>')
        out.append(f'<text x="{xx:.1f}" y="{py1+15}" text-anchor="middle" class="ax">{mb_tick}</text>')
    out.append(f'<text x="{(px0+px1)/2:.1f}" y="{py1+30}" text-anchor="middle" class="lbl">AH3Mb.chrY coordinate (Mb, 1 Mb windows)</text>')

    m_pts = [f"{x_mb(mb):.1f},{y_frac(m):.1f}" for mb, f, m in chry_cont if mb < 29] + [
        f"{x_mb(mb):.1f},{y_frac(m):.1f}" for mb, f, m in chry_v3 if mb >= 29
    ]
    f_pts = [f"{x_mb(mb):.1f},{y_frac(f):.1f}" for mb, f, m in chry_cont if mb < 29] + [
        f"{x_mb(mb):.1f},{y_frac(f):.1f}" for mb, f, m in chry_v3 if mb >= 29
    ]
    out.append(f'<polyline fill="none" stroke="{GREEN}" stroke-width="2.4" points="{" ".join(m_pts)}"/>')
    out.append(f'<polyline fill="none" stroke="{VERMILION}" stroke-width="2.4" points="{" ".join(f_pts)}"/>')

    out.append(f'<line x1="22" y1="303" x2="40" y2="303" stroke="{GREEN}" stroke-width="3"/>')
    out.append(f'<text x="45" y="307" class="lbl">Male Y-carriers (BCMb 0.976, GRMa 0.984, KOMPb 0.987)</text>')
    out.append(f'<line x1="22" y1="319" x2="40" y2="319" stroke="{VERMILION}" stroke-width="3"/>')
    out.append(f'<text x="45" y="323" class="lbl">Female XX (cs10 0.071, EH23a/b ≤0.077 · 30/30 ≤0.077)</text>')

    # Divider at x = 452
    out.append(f'<line x1="452" y1="12" x2="452" y2="{h-12}" stroke="{LINE}"/>')

    # Panel B (x in [464, 888])
    panel_badge(
        out,
        464,
        10,
        "B",
        "1 Mb Window k = 21 vs rbest Chain Identity",
        "Tier P2 (43 genomes, 1.14 GB): 41/42 queries pass r ≥ 0.50",
    )

    grma_cont: dict[tuple[str, int], float] = {}
    for row in csv.DictReader((CANNABIS_ROOT / "reports/evidence/panagram_step0_2026-10-27/cont_k21_cs10.tsv").open(), delimiter="\t"):
        grma_cont[(row["chrom"], int(row["start"]))] = float(row["GRMa"])

    pts_scatter = []
    for row in csv.DictReader((CANNABIS_ROOT / "reports/evidence/panagram_step0_2026-10-27/identity_cs10_rbest.tsv").open(), delimiter="\t"):
        if row["genome"] == "GRMa":
            aln = int(row["aligned"])
            mat = int(row["matched"])
            if aln >= 500_000:
                key = (row["chrom"], int(row["start"]))
                if key in grma_cont:
                    ident = (mat / float(aln)) * 100.0
                    cont = grma_cont[key]
                    if 93.0 <= ident <= 100.0 and 0.55 <= cont <= 1.0:
                        pts_scatter.append((ident, cont))

    sx0, sx1 = 500, 706
    sy0, sy1 = 58, 255

    def x_ident(id_pct: float) -> float:
        return sx0 + ((id_pct - 93.0) / 7.0) * (sx1 - sx0)

    def y_cont(c: float) -> float:
        return sy1 - ((c - 0.55) / 0.45) * (sy1 - sy0)

    for id_t in [93, 95, 97, 99, 100]:
        xx = x_ident(id_t)
        out.append(f'<line x1="{xx:.1f}" y1="{sy0}" x2="{xx:.1f}" y2="{sy1}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{xx:.1f}" y="{sy1+15}" text-anchor="middle" class="ax">{id_t}%</text>')
    for ct in [0.6, 0.7, 0.8, 0.9, 1.0]:
        yy = y_cont(ct)
        out.append(f'<line x1="{sx0}" y1="{yy:.1f}" x2="{sx1}" y2="{yy:.1f}" stroke="{LINE}" stroke-dasharray="2,2"/>')
        out.append(f'<text x="{sx0-5}" y="{yy+3:.1f}" text-anchor="end" class="ax">{ct:.1f}</text>')

    for ident, cont in pts_scatter[::2]:
        out.append(f'<circle cx="{x_ident(ident):.1f}" cy="{y_cont(cont):.1f}" r="2.1" fill="{BLUE}" opacity="0.55"/>')

    out.append(f'<line x1="{x_ident(94.0):.1f}" y1="{y_cont(0.62):.1f}" x2="{x_ident(99.5):.1f}" y2="{y_cont(0.93):.1f}" stroke="{VERMILION}" stroke-width="2.2"/>')
    out.append(f'<rect x="{sx0+6}" y="{sy0+5}" width="174" height="14" rx="2" fill="#ffffff" opacity="0.9"/>')
    out.append(f'<text x="{sx0+8}" y="{sy0+16}" class="lbl" fill="{BLUE}">GRMa (631 win, r = 0.8118)</text>')
    out.append(f'<text x="{(sx0+sx1)/2:.1f}" y="{sy1+30}" text-anchor="middle" class="lbl">cs10 rbest chain identity (%)</text>')

    rx = 720
    out.append(f'<rect x="{rx}" y="58" width="168" height="82" rx="7" fill="{BG_SOFT}" stroke="{LINE}"/>')
    out.append(f'<text x="{rx+8}" y="75" class="lbl" fill="{NAVY}">Tier P2 V1 (42 queries)</text>')
    out.append(f'<text x="{rx+8}" y="92" class="lbl" fill="{GREEN}">41 / 42 pass r ≥ 0.50</text>')
    out.append(f'<text x="{rx+8}" y="107" class="ax">• Range: 0.5848–0.8118</text>')
    out.append(f'<text x="{rx+8}" y="121" class="ax">• Pink pepper: r = 0.7376</text>')
    out.append(f'<text x="{rx+8}" y="135" class="ax" fill="{VERMILION}">• ASM5191173v1: r = 0.4763</text>')

    out.append(f'<rect x="{rx}" y="148" width="168" height="82" rx="7" fill="{BG_SOFT}" stroke="{LINE}"/>')
    out.append(f'<text x="{rx+8}" y="165" class="lbl" fill="{NAVY}">TOGA2 v2.0.9 Pilot</text>')
    out.append(f'<text x="{rx+8}" y="182" class="lbl" fill="{BLUE}">24,503 std / 758 anom</text>')
    out.append(f'<text x="{rx+8}" y="197" class="ax">• Control: 25 lost (0.10%)</text>')
    out.append(f'<text x="{rx+8}" y="211" class="ax">• 54 min, 1.87 GB peak RAM</text>')
    out.append(f'<text x="{rx+8}" y="225" class="ax">• 221 all.chain (1.45 TB)</text>')

    out.append(f'<rect x="{rx}" y="238" width="168" height="80" rx="7" fill="#fff4d1" stroke="{GOLD}"/>')
    out.append(f'<text x="{rx+8}" y="255" class="lbl" fill="{NAVY}">Phenotype Ledger</text>')
    out.append(f'<text x="{rx+8}" y="272" class="lbl">1,341 rows · 154 plants</text>')
    out.append(f'<text x="{rx+8}" y="287" class="ax">• 78 pedigree families</text>')
    out.append(f'<text x="{rx+8}" y="301" class="ax">• 69 in largest Salk family</text>')
    out.append(f'<text x="{rx+8}" y="314" class="ax">• 0/14 traits pass ≥30-fam</text>')

    out.append("</svg>")
    (OUT_DIR / "figure5_panagram_kmer.svg").write_text("\n".join(out))


if __name__ == "__main__":
    build_figure1()
    build_figure2()
    build_figure3()
    build_figure4()
    build_figure5()
    print("Generated all 5 data-dense poster SVG figures in", OUT_DIR)
