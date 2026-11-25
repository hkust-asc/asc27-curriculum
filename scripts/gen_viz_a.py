#!/usr/bin/env python3
"""Generate Batch A (9 English minimalist technical SVG/PNG diagrams) for HKUST ASC27 curriculum."""

from __future__ import annotations

import math
from datetime import date
from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_kit import C, PlotBox, SVGCanvas


def build_00_knowledge_graph() -> Path:
    svg = SVGCanvas(1280, 640)
    svg.header(
        "ASC27 Five-Layer First-Principles Knowledge Graph",
        "Deriving parallel models, performance diagnosis, AI systems, and competition execution from hardware physics",
        accent=C["blue"],
    )

    layers = [
        (
            "L1",
            "Architecture & Physics",
            C["blue"],
            C["surface_blue"],
            [
                ("A1", "Work & Precision", "FLOPs · FP64 / FP32 / BF16"),
                ("A2", "Memory Wall", "Cache · DDR5 DRAM · HBM3"),
                ("A3", "Power & Thermal Wall", "TDP · Efficiency (GFLOP/W)"),
            ],
        ),
        (
            "L2",
            "Parallel Models",
            C["teal"],
            C["surface_teal"],
            [
                ("B1", "CPU Parallelism", "SIMD · OpenMP · NUMA"),
                ("B2", "Distributed Topology", "MPI · Halo · RDMA"),
                ("B3", "GPU SIMT Model", "CUDA · HIP · Tiling"),
            ],
        ),
        (
            "L3",
            "Perf Analysis & Tuning",
            C["gold"],
            C["surface_gold"],
            [
                ("C1", "Scaling Laws", "Amdahl · Gustafson"),
                ("C2", "Roofline & Profiling", "Roofline · Nsight / perf"),
                ("C3", "Verification & CI", "Reference · Soak Regression"),
            ],
        ),
        (
            "L4",
            "AI Systems & Training",
            C["violet"],
            C["surface_violet"],
            [
                ("D1", "Mixed Precision & VRAM", "BF16 · Memory Budget"),
                ("D2", "Multi-D Parallel & NCCL", "DP / FSDP / TP / PP"),
                ("D3", "Inference & World Models", "KV Cache · LLM / World"),
            ],
        ),
        (
            "L5",
            "ASC Competition Ops",
            C["coral"],
            C["surface_coral"],
            [
                ("E1", "Power-Capped Tuning", "HPL · HPCG · Power Limit"),
                ("E2", "Domain & Mystery Apps", "SciComp · CPU-only"),
                ("E3", "Proposal & Defense", "Proposal · Poster · Team"),
            ],
        ),
    ]

    row_y0 = 96
    row_h = 84
    row_gap = 20
    label_x = 32
    col_x = [262, 532, 802]
    card_w = 246
    card_h = 74

    node_pos = {}

    for r_idx, (lcode, lname, accent, tint, nodes) in enumerate(layers):
        ry = row_y0 + r_idx * (row_h + row_gap)
        svg.rect(label_x, ry, 1030, row_h, fill=tint, stroke=C["grid"], sw=1.1, rx=8)
        svg.rect(label_x, ry, 7, row_h, fill=accent, rx=2)
        svg.text(label_x + 22, ry + 34, lcode, size=18, color=accent, weight="bold", mono=True)
        svg.text(label_x + 22, ry + 59, lname, size=15, color=C["ink"], weight="bold")

        for c_idx, (ncode, title, sub) in enumerate(nodes):
            nx = col_x[c_idx]
            ny = ry + (row_h - card_h) / 2
            svg.rect(nx, ny, card_w, card_h, fill=C["white"], stroke=accent, sw=1.5, rx=6)
            svg.rect(nx + 10, ny + 10, 32, 22, fill=tint, stroke=accent, sw=1.0, rx=4)
            svg.text(nx + 26, ny + 26, ncode, size=13, color=accent, weight="bold", anchor="middle", mono=True)
            svg.text(nx + 49, ny + 26, title, size=14.5, color=C["ink"], weight="bold")
            svg.text(nx + 14, ny + 54, sub, size=13.5, color=C["muted"])
            node_pos[ncode] = (nx, ny, card_w, card_h)

        if r_idx < len(layers) - 1:
            y_start = ry + row_h + 1
            y_end = ry + row_h + row_gap - 2
            for cx_arr in [col_x[0] + card_w / 2, col_x[1] + card_w / 2, col_x[2] + card_w / 2]:
                svg.line(cx_arr, y_start, cx_arr, y_end, stroke=C["axis"], sw=1.8, marker_end="arr_muted")

    # Right-hand cross-layer dependency panel
    svg.rect(1078, 96, 174, 500, fill=C["white"], stroke=C["grid"], sw=1.2, rx=8)
    svg.text(1165, 118, "Cross-Layer Links", size=14.5, color=C["ink"], weight="bold", anchor="middle")
    svg.line(1092, 127, 1238, 127, stroke=C["grid"], sw=1.0)

    a3 = node_pos["A3"]
    b2 = node_pos["B2"]
    c2 = node_pos["C2"]
    c3 = node_pos["C3"]
    d2 = node_pos["D2"]
    e1 = node_pos["E1"]
    e2 = node_pos["E2"]
    e3 = node_pos["E3"]

    # 1. C3 -> E3 (innermost right channel x=1092)
    x_ch1 = 1092
    y_c3 = c3[1] + c3[3] * 0.55
    y_e3 = e3[1] + e3[3] * 0.45
    svg.path(
        f"M {c3[0]+c3[2]:.1f} {y_c3:.1f} L {x_ch1:.1f} {y_c3:.1f} L {x_ch1:.1f} {y_e3:.1f} L {e3[0]+e3[2]+3:.1f} {y_e3:.1f}",
        stroke=C["gold"],
        sw=2.0,
        dash="6,4",
        marker_end="arr_gold",
    )

    # 2. A3 -> E1 (outermost right channel x=1240, then along bottom rail y=616 to E1 bottom)
    x_ch4 = 1240
    y_a3 = a3[1] + a3[3] * 0.5
    y_bot = 616
    x_e1_mid = e1[0] + e1[2] * 0.5
    svg.path(
        f"M {a3[0]+a3[2]:.1f} {y_a3:.1f} L {x_ch4:.1f} {y_a3:.1f} L {x_ch4:.1f} {y_bot:.1f} "
        f"L {x_e1_mid:.1f} {y_bot:.1f} L {x_e1_mid:.1f} {e1[1]+e1[3]+3:.1f}",
        stroke=C["coral"],
        sw=2.1,
        dash="6,4",
        marker_end="arr_coral",
    )

    # 3. B2 -> D2 (vertical gutter between col2 and col3 at x=790)
    x_g2 = 790
    y_b2 = b2[1] + b2[3] * 0.5
    y_d2 = d2[1] + d2[3] * 0.5
    svg.path(
        f"M {b2[0]+b2[2]:.1f} {y_b2:.1f} L {x_g2:.1f} {y_b2:.1f} L {x_g2:.1f} {y_d2:.1f} L {d2[0]+d2[2]+3:.1f} {y_d2:.1f}",
        stroke=C["teal"],
        sw=2.1,
        dash="5,4",
        marker_end="arr_teal",
    )

    # 4. C2 -> E2 (vertical gutter between col1 and col2 at x=520)
    x_g1 = 520
    y_c2 = c2[1] + c2[3] * 0.5
    y_e2 = e2[1] + e2[3] * 0.5
    svg.path(
        f"M {c2[0]:.1f} {y_c2:.1f} L {x_g1:.1f} {y_c2:.1f} L {x_g1:.1f} {y_e2:.1f} L {e2[0]-3:.1f} {y_e2:.1f}",
        stroke=C["blue"],
        sw=2.1,
        dash="5,4",
        marker_end="arr_blue",
    )

    # Clean legend cards inside right panel for the 4 cross-layer links
    cross_items = [
        ("A3 → E1", "Power wall bounds", "HPL / HPCG tuning", C["coral"], C["surface_coral"]),
        ("B2 → D2", "RDMA topology", "drives NCCL perf", C["teal"], C["surface_teal"]),
        ("C2 → E2", "Roofline isolates", "mystery bottlenecks", C["blue"], C["surface_blue"]),
        ("C3 → E3", "Regression evidence", "backs final defense", C["gold"], C["surface_gold"]),
    ]
    ly = 160
    for code, l1, l2, col, bg in cross_items:
        svg.rect(1106, ly, 120, 68, fill=bg, stroke=col, sw=1.3, rx=6)
        svg.line(1114, ly + 18, 1132, ly + 18, stroke=col, sw=2.2, dash="4,3")
        svg.text(1138, ly + 23, code, size=13.5, color=col, weight="bold", mono=True)
        svg.text(1166, ly + 42, l1, size=12.5, color=C["ink2"], anchor="middle")
        svg.text(1166, ly + 58, l2, size=12.5, color=C["ink2"], anchor="middle")
        ly += 86

    # Inline gutter pills with comfortable padding
    svg.rect(766, 325, 48, 22, fill=C["surface_teal"], stroke=C["teal"], sw=1.1, rx=4)
    svg.text(790, 340, "B2→D2", size=11, color=C["teal"], weight="bold", anchor="middle", mono=True)

    svg.rect(496, 429, 48, 22, fill=C["surface_blue"], stroke=C["blue"], sw=1.1, rx=4)
    svg.text(520, 444, "C2→E2", size=11, color=C["blue"], weight="bold", anchor="middle", mono=True)

    return svg.save_and_render("00_knowledge_graph", png_width=2200)


def build_00_roadmap_timeline() -> Path:
    svg = SVGCanvas(1280, 540)
    svg.header(
        "ASC27 24-Week Training Roadmap (2026-11-25 to 2027-05-11)",
        "Four progressive curriculum stages aligned with official ASC27 milestones and HKUST weekly cadence",
        accent=C["blue"],
    )

    d_start = date(2026, 11, 25)
    d_end = date(2027, 5, 19)
    total_days = (d_end - d_start).days

    chart_x = 256
    chart_w = 984
    chart_y = 148
    chart_h = 282

    def dx(dt: date) -> float:
        return chart_x + ((dt - d_start).days / total_days) * chart_w

    def wx(week_idx: float) -> float:
        days = (week_idx - 1.0) * 7.0
        return chart_x + (days / total_days) * chart_w

    svg.rect(chart_x, chart_y, chart_w, chart_h, fill=C["white"], stroke=C["grid"], sw=1.3, rx=6)

    x_reg = dx(date(2027, 1, 10))
    x_pre_s = dx(date(2027, 1, 11))
    x_pre_e = dx(date(2027, 2, 28))
    x_fin_s = dx(date(2027, 5, 1))
    x_fin_e = dx(date(2027, 5, 15))

    svg.rect(x_pre_s, chart_y, x_pre_e - x_pre_s, chart_h, fill=C["surface_gold"], opacity=0.75)
    svg.rect(x_fin_s, chart_y, x_fin_e - x_fin_s, chart_h, fill=C["surface_coral"], opacity=0.75)

    months = [
        (date(2026, 12, 1), "2026/12"),
        (date(2027, 1, 1), "2027/01"),
        (date(2027, 2, 1), "2027/02"),
        (date(2027, 3, 1), "2027/03"),
        (date(2027, 4, 1), "2027/04"),
        (date(2027, 5, 1), "2027/05"),
    ]
    for md, mlbl in months:
        mx = dx(md)
        svg.line(mx, chart_y, mx, chart_y + chart_h, stroke=C["grid"], sw=1.1)
        svg.text(mx, chart_y + chart_h + 22, mlbl, size=14, color=C["muted"], anchor="middle", mono=True)

    for w in [1, 4, 8, 12, 16, 20, 24]:
        xw = wx(w)
        svg.line(xw, chart_y - 6, xw, chart_y, stroke=C["axis"], sw=1.4)
        svg.text(xw, chart_y - 11, f"W{w}", size=13, color=C["slate"], weight="bold", anchor="middle", mono=True)

    # Non-overlapping milestone pills & vertical dashed lines
    svg.line(x_reg, 114, x_reg, chart_y + chart_h + 4, stroke=C["coral"], sw=2.0, dash="6,4")
    reg_w = 216
    svg.rect(x_reg - reg_w + 8, 84, reg_w, 30, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=5)
    svg.text(x_reg - reg_w / 2 + 8, 104, "Reg. Deadline: 2027-01-10", size=13.5, color=C["coral"], weight="bold", anchor="middle")

    svg.line(x_pre_e, 114, x_pre_e, chart_y + chart_h + 4, stroke=C["gold"], sw=2.0, dash="6,4")
    x_pre_mid = (x_pre_s + x_pre_e) / 2
    pre_w = 218
    svg.rect(x_pre_mid - pre_w / 2, 84, pre_w, 30, fill=C["surface_gold"], stroke=C["gold"], sw=1.2, rx=5)
    svg.text(x_pre_mid, 104, "Prelim Window: 01/11–02/28", size=13.5, color=C["gold"], weight="bold", anchor="middle")

    svg.line(x_fin_s, 114, x_fin_s, chart_y + chart_h + 4, stroke=C["coral"], sw=2.0, dash="6,4")
    x_fin_mid = (x_fin_s + x_fin_e) / 2
    fin_w = 148
    svg.rect(x_fin_mid - fin_w / 2, 84, fin_w, 30, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=5)
    svg.text(x_fin_mid, 104, "Finals: May 2027", size=13.5, color=C["coral"], weight="bold", anchor="middle")

    stages = [
        ("Stage 1", "Hardware & Modeling", "W1–W3", "M01–M04", 1.0, 4.0, C["blue"], C["surface_blue"], "Precision · Memory Wall · Amdahl · Roofline"),
        ("Stage 2", "Node-to-Cluster Parallel", "W4–W8", "M05–M08", 4.0, 9.0, C["teal"], C["surface_teal"], "SIMD/OpenMP · MPI/RDMA · CUDA/HIP · Baselines"),
        ("Stage 3", "AI Systems & Prelims", "W9–W13", "M09–M12", 9.0, 14.0, C["violet"], C["surface_violet"], "BF16/VRAM · FSDP/TP/NCCL · Inference · Proposal"),
        ("Stage 4", "Finals Stress & Mystery", "W14–W24", "M13–M16", 14.0, 25.0, C["coral"], C["surface_coral"], "Power-Capped HPL/HPCG · SciComp · Mystery · Defense"),
    ]

    row_step = 68
    bar_h = 42
    for i, (snum, stitle, wspan, mspan, w0, w1, col, tint, detail) in enumerate(stages):
        ry = chart_y + 18 + i * row_step
        if i > 0:
            svg.line(chart_x, ry - 12, chart_x + chart_w, ry - 12, stroke=C["grid"], sw=0.9)
        svg.rect(34, ry - 2, 206, bar_h + 4, fill=tint, stroke=C["grid"], sw=1.1, rx=6)
        svg.rect(34, ry - 2, 6, bar_h + 4, fill=col, rx=2)
        svg.text(50, ry + 16, f"{snum}  {wspan}", size=14.5, color=col, weight="bold")
        svg.text(50, ry + 36, stitle, size=14, color=C["ink"])

        bx0 = wx(w0)
        bx1 = wx(w1)
        bw = bx1 - bx0
        svg.rect(bx0, ry, bw, bar_h, fill=col, rx=6)
        svg.text(bx0 + 12, ry + 26, mspan, size=14.5, color=C["white"], weight="bold", mono=True)

        if bw >= 340:
            svg.text(bx0 + 96, ry + 26, detail, size=13.5, color=C["white"])
        else:
            pill_w = len(detail) * 7.2 + 20
            svg.rect(bx1 + 8, ry + 8, pill_w, 26, fill=C["white"], opacity=0.92, rx=4)
            svg.text(bx1 + 16, ry + 26, detail, size=13.5, color=C["ink2"])

    svg.rect(34, 468, 1206, 48, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=8)
    svg.rect(34, 468, 6, 48, fill=C["gold"], rx=2)
    svg.text(54, 497, "HKUST Cadence", size=15, color=C["ink"], weight="bold")
    svg.text(
        188,
        497,
        "Wednesdays 18:30–20:00 in-person seminar & lab review  ·  Official ASC27 deadlines are midnight UTC+8",
        size=14.5,
        color=C["ink2"],
    )

    return svg.save_and_render("00_roadmap_timeline", png_width=2200)


def build_m01_gemm_work_traffic() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "GEMM Work vs. Memory Traffic: Why Arithmetic Intensity Scales as O(N)",
        "C = A × B (N×N FP64): 2N³ FLOPs vs. unblocked 16N³ B and theoretical minimum 24N² B",
        accent=C["blue"],
    )

    svg.panel_box(32, 86, 896, 174, "Matrix Multiplication C = A × B: Work and Data Reuse Structure", accent=C["blue"])

    cx, cy, s = 82, 146, 82
    svg.rect(cx, cy, s, s, fill=C["surface_teal"], stroke=C["teal"], sw=1.8, rx=4)
    svg.rect(cx + 30, cy + 28, 14, 14, fill=C["teal"], rx=2)
    svg.text(cx + s / 2, cy - 8, "C (N×N)", size=15, color=C["teal"], weight="bold", anchor="middle")
    svg.text(cx + s / 2, cy + s + 18, "N² writes", size=13.5, color=C["muted"], anchor="middle")

    svg.text(cx + s + 22, cy + 48, "=", size=24, color=C["ink"], weight="bold", anchor="middle")

    ax = cx + s + 44
    svg.rect(ax, cy, s, s, fill=C["surface_blue"], stroke=C["blue"], sw=1.8, rx=4)
    svg.rect(ax, cy + 28, s, 14, fill=C["blue"], opacity=0.35)
    svg.text(ax + s / 2, cy - 8, "A (N×N)", size=15, color=C["blue"], weight="bold", anchor="middle")
    svg.text(ax + s / 2, cy + s + 18, "N× row reuse", size=13.5, color=C["muted"], anchor="middle")

    svg.text(ax + s + 22, cy + 48, "×", size=24, color=C["ink"], weight="bold", anchor="middle")

    bx = ax + s + 44
    svg.rect(bx, cy, s, s, fill=C["surface_gold"], stroke=C["gold"], sw=1.8, rx=4)
    svg.rect(bx + 30, cy, 14, s, fill=C["gold"], opacity=0.4)
    svg.text(bx + s / 2, cy - 8, "B (N×N)", size=15, color=C["gold"], weight="bold", anchor="middle")
    svg.text(bx + s / 2, cy + s + 18, "N× col reuse", size=13.5, color=C["muted"], anchor="middle")

    fx = 468
    svg.rect(fx, 134, 438, 112, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(fx + 18, 160, "Compute Work (FMA = 2 FLOPs)", size=14.5, color=C["ink"], weight="bold")
    svg.text(fx + 422, 160, "W = 2N³ FLOPs", size=14.5, color=C["blue"], weight="bold", anchor="end", mono=True)
    svg.line(fx + 16, 172, fx + 422, 172, stroke=C["grid"], sw=1.0)
    svg.text(fx + 18, 196, "Naive Traffic (FP64 = 8 B)", size=14.5, color=C["ink2"])
    svg.text(fx + 422, 196, "Q_naive = 16N³ B", size=14.5, color=C["coral"], weight="bold", anchor="end", mono=True)
    svg.text(fx + 18, 226, "Optimal Lower Bound (3N²)", size=14.5, color=C["ink2"])
    svg.text(fx + 422, 226, "Q_min = 24N² B", size=14.5, color=C["teal"], weight="bold", anchor="end", mono=True)

    svg.panel_box(32, 276, 896, 360, "Log-Log Scaling of Compute Work vs. Memory Traffic (N ∈ [64, 8192])", accent=C["teal"])

    pb = PlotBox(svg, 120, 326, 768, 246, xmin=64, xmax=8192, ymin=1e4, ymax=1e14, xlog=True, ylog=True)
    pb.draw_axes(
        xticks=[(64, "64"), (128, "128"), (256, "256"), (512, "512"), (1024, "1024"), (2048, "2048"), (4096, "4096"), (8192, "8192")],
        yticks=[(1e4, "10⁴"), (1e6, "10⁶"), (1e8, "10⁸"), (1e10, "10¹⁰"), (1e12, "10¹²"), (1e14, "10¹⁴")],
        xlabel="Matrix Dimension N (log₂ scale)",
        ylabel="FLOPs or Bytes (log₁₀)",
    )

    ns = np.geomspace(64, 8192, 200)
    flops = 2.0 * (ns ** 3)
    q_naive = 16.0 * (ns ** 3)
    q_min = 24.0 * (ns ** 2)

    poly_pts = [(pb.px(v), pb.py(2.0 * v ** 3)) for v in ns] + [(pb.px(v), pb.py(24.0 * v ** 2)) for v in reversed(ns)]
    svg.polygon(poly_pts, fill=C["surface_teal"], opacity=0.75)

    pb.plot_curve(ns, q_naive, stroke=C["coral"], sw=2.8, dash="8,4")
    pb.plot_curve(ns, flops, stroke=C["blue"], sw=3.2)
    pb.plot_curve(ns, q_min, stroke=C["teal"], sw=3.2)

    n_ref = 2048.0
    x_ref = pb.px(n_ref)
    y_w = pb.py(2.0 * n_ref ** 3)
    y_q = pb.py(24.0 * n_ref ** 2)
    svg.line(x_ref, y_w + 5, x_ref, y_q - 5, stroke=C["teal"], sw=2.2, marker_start="arr_teal", marker_end="arr_teal")
    svg.rect(x_ref - 166, (y_w + y_q) / 2 - 23, 156, 46, fill=C["white"], stroke=C["teal"], sw=1.3, rx=5)
    svg.text(x_ref - 88, (y_w + y_q) / 2 - 3, "I_max = N / 12", size=13.5, color=C["teal"], weight="bold", anchor="middle", mono=True)
    svg.text(x_ref - 88, (y_w + y_q) / 2 + 16, "N=2048 → 171 F/B", size=13, color=C["ink2"], anchor="middle")

    svg.text(pb.px(1450), pb.py(16.0 * (1450 ** 3)) - 14, "Naive traffic 16N³ B (slope 3)", size=14, color=C["coral"], weight="bold", anchor="end")
    svg.text(pb.px(4300), pb.py(2.0 * (4300 ** 3)) + 26, "Work 2N³ FLOPs", size=14, color=C["blue"], weight="bold", anchor="middle")
    svg.text(pb.px(3600), pb.py(24.0 * (3600 ** 2)) + 26, "Optimal bound 24N² B (slope 2)", size=14, color=C["teal"], weight="bold", anchor="middle")

    svg.rect(136, 338, 294, 54, fill=C["white"], stroke=C["grid"], sw=1.1, rx=5)
    svg.text(148, 359, "Naive intensity: I = 0.125 FLOP/B (flat)", size=13.5, color=C["coral"], weight="bold")
    svg.text(148, 380, "Blocking lifts intensity linearly to O(N)", size=13.5, color=C["teal"], weight="bold")

    return svg.save_and_render("m01_gemm_work_traffic")


def build_m02_memory_hierarchy_numa() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Memory Hierarchy Latency Wall & Dual-Socket NUMA Topology",
        "Access latency spans 3 orders of magnitude; cross-socket traffic and poor First-Touch degrade bandwidth",
        accent=C["blue"],
    )

    svg.panel_box(32, 88, 456, 540, "Memory Latency (log₁₀ scale) & Peak Bandwidth", accent=C["blue"])

    items = [
        ("Register", 0.3, "~0.3 ns", ">10 TB/s", C["teal"]),
        ("L1 Cache", 1.0, "~1 ns", "Multi-TB/s", C["teal"]),
        ("L2 Cache", 4.0, "~4 ns", "~1–2 TB/s", C["blue"]),
        ("L3 Cache", 15.0, "~15 ns", "~0.5–1 TB/s", C["blue"]),
        ("DDR5 DRAM", 80.0, "~80 ns", "~0.3 TB/s", C["coral"]),
        ("HBM3 (GPU)", 100.0, "~100 ns", "~3.35 TB/s", C["violet"]),
    ]

    bx0 = 148
    bw_max = 238
    vmin, vmax = 0.1, 250.0

    def lx(val: float) -> float:
        t = (math.log10(val) - math.log10(vmin)) / (math.log10(vmax) - math.log10(vmin))
        return bx0 + t * bw_max

    y_top = 152
    y_bot = 526
    for tick_v, tick_l in [(0.1, "0.1"), (1.0, "1"), (10.0, "10"), (100.0, "100 ns")]:
        tx = lx(tick_v)
        svg.line(tx, y_top - 10, tx, y_bot, stroke=C["grid"], sw=1.1)
        svg.text(tx, y_bot + 20, tick_l, size=13, color=C["muted"], anchor="middle", mono=True)
    svg.line(bx0, y_bot, bx0 + bw_max, y_bot, stroke=C["slate"], sw=1.6)
    svg.line(bx0, y_top - 10, bx0, y_bot, stroke=C["slate"], sw=1.6)

    bar_h = 34
    gap = 60
    for idx, (name, ns_val, lat_lbl, bw_lbl, col) in enumerate(items):
        by = y_top + 10 + idx * gap
        svg.text(bx0 - 12, by + 22, name, size=14.5, color=C["ink"], weight="bold", anchor="end")
        w_bar = lx(ns_val) - bx0
        svg.rect(bx0, by, w_bar, bar_h, fill=col, rx=4)
        if w_bar >= 68:
            svg.text(bx0 + w_bar - 8, by + 22, lat_lbl, size=13.5, color=C["white"], weight="bold", anchor="end", mono=True)
            svg.text(bx0 + w_bar + 8, by + 22, bw_lbl, size=12.5, color=C["ink2"])
        else:
            svg.text(bx0 + w_bar + 8, by + 22, f"{lat_lbl} · {bw_lbl}", size=13, color=C["ink2"])

    svg.rect(48, 562, 424, 52, fill=C["surface_violet"], stroke=C["violet"], sw=1.1, rx=6)
    svg.text(60, 583, "Key contrast: HBM3 latency exceeds DDR5, yet wide buses", size=13.5, color=C["violet"], weight="bold")
    svg.text(60, 603, "deliver >10× bandwidth via massive thread concurrency.", size=13.5, color=C["ink2"])

    svg.panel_box(504, 88, 424, 540, "Dual-Socket NUMA Topology & First-Touch Rule", accent=C["coral"])

    s0_x, s1_x = 528, 742
    s_y, s_w, s_h = 148, 162, 118

    for sx, sname, accent, tint in [
        (s0_x, "Socket 0 (NUMA 0)", C["blue"], C["surface_blue"]),
        (s1_x, "Socket 1 (NUMA 1)", C["teal"], C["surface_teal"]),
    ]:
        svg.rect(sx, s_y, s_w, s_h, fill=tint, stroke=accent, sw=1.8, rx=8)
        svg.text(sx + s_w / 2, s_y + 24, sname, size=14, color=accent, weight="bold", anchor="middle")
        for ci in range(4):
            cx = sx + 14 + ci * 35
            svg.rect(cx, s_y + 36, 28, 26, fill=C["white"], stroke=accent, sw=1.2, rx=4)
            svg.text(cx + 14, s_y + 53, f"C{ci}", size=11.5, color=C["ink2"], anchor="middle", mono=True)
        svg.rect(sx + 14, s_y + 72, s_w - 28, 30, fill=C["white"], stroke=accent, sw=1.2, rx=4)
        svg.text(sx + s_w / 2, s_y + 92, "Shared L3 Cache", size=13, color=C["ink2"], weight="bold", anchor="middle")

    svg.line(s0_x + s_w + 2, s_y + 58, s1_x - 2, s_y + 58, stroke=C["coral"], sw=2.6, marker_start="arr_coral", marker_end="arr_coral")
    svg.rect(682, s_y + 18, 68, 26, fill=C["surface_coral"], stroke=C["coral"], sw=1.1, rx=4)
    svg.text(716, s_y + 36, "UPI/xGMI", size=11.5, color=C["coral"], weight="bold", anchor="middle", mono=True)

    m_y, m_h = 338, 66
    svg.rect(s0_x, m_y, s_w, m_h, fill=C["white"], stroke=C["blue"], sw=1.8, rx=6)
    svg.text(s0_x + s_w / 2, m_y + 28, "Local DDR5 #0", size=14.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(s0_x + s_w / 2, m_y + 50, "~80 ns · full BW", size=13, color=C["muted"], anchor="middle")

    svg.rect(s1_x, m_y, s_w, m_h, fill=C["white"], stroke=C["teal"], sw=1.8, rx=6)
    svg.text(s1_x + s_w / 2, m_y + 28, "Local DDR5 #1", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(s1_x + s_w / 2, m_y + 50, "~80 ns · full BW", size=13, color=C["muted"], anchor="middle")

    svg.line(s0_x + 26, s_y + s_h + 2, s0_x + 26, m_y - 3, stroke=C["blue"], sw=2.4, marker_start="arr_blue", marker_end="arr_blue")
    svg.text(s0_x + 38, 300, "Local", size=13, color=C["blue"], weight="bold")
    svg.text(s0_x + 38, 317, "1× lat.", size=12.5, color=C["blue"])

    svg.line(s1_x + s_w - 26, s_y + s_h + 2, s1_x + s_w - 26, m_y - 3, stroke=C["teal"], sw=2.4, marker_start="arr_teal", marker_end="arr_teal")
    svg.text(s1_x + s_w - 38, 300, "Local", size=13, color=C["teal"], weight="bold", anchor="end")
    svg.text(s1_x + s_w - 38, 317, "full BW", size=12.5, color=C["teal"], anchor="end")

    svg.line(s0_x + s_w - 24, s_y + s_h + 4, s1_x + 28, m_y - 4, stroke=C["coral"], sw=2.3, dash="6,4", marker_end="arr_coral")
    svg.rect(646, 286, 144, 40, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=5)
    svg.text(718, 303, "Remote NUMA Hop", size=12.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(718, 320, "1.5–2× lat. · link contention", size=11.5, color=C["coral"], anchor="middle")

    svg.rect(524, 428, 384, 186, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=8)
    svg.rect(524, 428, 6, 186, fill=C["gold"], rx=2)
    svg.text(544, 454, "Linux First-Touch Page Placement Rule", size=15, color=C["ink"], weight="bold")
    svg.multiline(
        544,
        480,
        [
            "• Physical pages map on first write (not malloc)",
            "• Bug: serial init pins entire array to Node 0",
            "• Fix: parallel OpenMP init matching compute schedule",
            "• Pair with OMP_PROC_BIND=close + numactl",
        ],
        size=13.8,
        color=C["ink2"],
        lh=24,
    )
    svg.rect(544, 574, 348, 28, fill=C["white"], stroke=C["gold"], sw=1.1, rx=4)
    svg.text(718, 593, "#pragma omp parallel for schedule(static)", size=13, color=C["gold"], weight="bold", anchor="middle", mono=True)

    return svg.save_and_render("m02_memory_hierarchy_numa")


def build_m03_amdahl_gustafson() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Amdahl Strong Scaling Ceiling vs. Gustafson Weak Scaling",
        "Fixed problem size hits the serial limit 1/(1−f); scaling work with cores maintains linear speedup",
        accent=C["blue"],
    )

    svg.panel_box(32, 88, 444, 540, "Strong Scaling: Amdahl S(k) = 1 / [(1−f) + f/k]", accent=C["coral"])

    pb_l = PlotBox(svg, 98, 152, 352, 340, xmin=1, xmax=256, ymin=0, ymax=108, xlog=True, ylog=False)
    pb_l.draw_axes(
        xticks=[(1, "1"), (4, "4"), (16, "16"), (64, "64"), (256, "256")],
        yticks=[(0, "0"), (20, "20×"), (40, "40×"), (60, "60×"), (80, "80×"), (100, "100×")],
        xlabel="Processor Count k (log scale)",
        ylabel="Speedup S(k)",
    )

    ks = np.geomspace(1, 256, 200)
    amdahl_specs = [
        (0.99, C["teal"], 100.0),
        (0.95, C["blue"], 20.0),
        (0.90, C["gold"], 10.0),
        (0.50, C["coral"], 2.0),
    ]
    for f_val, col, asym in amdahl_specs:
        ys = 1.0 / ((1.0 - f_val) + f_val / ks)
        pb_l.plot_curve(ks, ys, stroke=col, sw=2.8)
        y_as = pb_l.py(asym)
        svg.line(pb_l.x, y_as, pb_l.x + pb_l.w, y_as, stroke=col, sw=1.2, dash="4,4")

    svg.text(pb_l.px(28), pb_l.py(94), "Limit 100× (f = 0.99)", size=13.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb_l.px(95), pb_l.py(23.5), "Limit 20× (f = 0.95)", size=13.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(pb_l.px(95), pb_l.py(12.2), "10× (f = 0.90)", size=13, color=C["gold"], weight="bold", anchor="middle")
    svg.text(pb_l.px(95), pb_l.py(3.6), "2× (f = 0.50)", size=13, color=C["coral"], weight="bold", anchor="middle")

    svg.rect(52, 554, 404, 58, fill=C["surface_coral"], stroke=C["coral"], sw=1.1, rx=6)
    svg.text(66, 576, "Fixed total workload (Strong Scaling):", size=13.5, color=C["coral"], weight="bold")
    svg.text(66, 598, "Even 5% serial work caps 256-core speedup below 20×.", size=13.5, color=C["ink2"])

    svg.panel_box(492, 88, 436, 540, "Weak Scaling: Gustafson S_w(k) = (1−s) + s·k", accent=C["teal"])

    pb_r = PlotBox(svg, 560, 152, 344, 340, xmin=0, xmax=128, ymin=0, ymax=136, xlog=False, ylog=False)
    pb_r.draw_axes(
        xticks=[(0, "0"), (32, "32"), (64, "64"), (96, "96"), (128, "128")],
        yticks=[(0, "0"), (32, "32×"), (64, "64×"), (96, "96×"), (128, "128×")],
        xlabel="Processor Count k (linear scale)",
        ylabel="Scaled Speedup S(k)",
    )

    klin = np.linspace(1, 128, 200)
    pb_r.plot_curve(klin, klin, stroke=C["axis"], sw=1.6, dash="5,5")
    g95 = 0.05 + 0.95 * klin
    pb_r.plot_curve(klin, g95, stroke=C["teal"], sw=3.0)
    g80 = 0.20 + 0.80 * klin
    pb_r.plot_curve(klin, g80, stroke=C["blue"], sw=2.8)
    a95 = 1.0 / (0.05 + 0.95 / klin)
    pb_r.plot_curve(klin, a95, stroke=C["coral"], sw=2.8, dash="7,4")

    x80 = pb_r.px(80)
    y_g95 = pb_r.py(0.05 + 0.95 * 80)
    y_a95 = pb_r.py(1.0 / (0.05 + 0.95 / 80))
    svg.line(x80, y_g95 + 5, x80, y_a95 - 5, stroke=C["gold"], sw=2.0, marker_start="arr_gold", marker_end="arr_gold")
    svg.rect(x80 - 128, (y_g95 + y_a95) / 2 - 15, 120, 30, fill=C["surface_gold"], stroke=C["gold"], sw=1.1, rx=4)
    svg.text(x80 - 68, (y_g95 + y_a95) / 2 + 5, "Same 5% serial", size=12.5, color=C["gold"], weight="bold", anchor="middle")

    svg.text(pb_r.px(68), pb_r.py(82), "Ideal S = k", size=13, color=C["muted"], anchor="end")
    svg.text(pb_r.px(125), pb_r.py(108), "Weak s = 0.95", size=13, color=C["teal"], weight="bold", anchor="end")
    svg.text(pb_r.px(125), pb_r.py(84), "Weak s = 0.80", size=13, color=C["blue"], weight="bold", anchor="end")
    svg.text(pb_r.px(125), pb_r.py(23), "Strong f = 0.95", size=13, color=C["coral"], weight="bold", anchor="end")

    svg.rect(512, 554, 396, 58, fill=C["surface_teal"], stroke=C["teal"], sw=1.1, rx=6)
    svg.text(526, 576, "Fixed work per core (Weak Scaling):", size=13.5, color=C["teal"], weight="bold")
    svg.text(526, 598, "Grid or matrix grows with nodes in large HPC runs.", size=13.5, color=C["ink2"])

    return svg.save_and_render("m03_amdahl_gustafson")


def build_m04_roofline_model() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Roofline Performance Model: CPU DDR5 vs. GPU HBM3 & Tensor Core",
        "R(I) = min(P_peak, B_mem × I) · Classifying kernels into memory-bound and compute-bound regimes",
        accent=C["blue"],
    )

    pb = PlotBox(svg, 108, 108, 804, 434, xmin=0.0625, xmax=1024.0, ymin=0.01, ymax=2000.0, xlog=True, ylog=True)

    x_ridge_split = pb.px(13.3)
    svg.rect(pb.x, pb.y, x_ridge_split - pb.x, pb.h, fill=C["surface_coral"], opacity=0.55)
    svg.rect(x_ridge_split, pb.y, pb.x + pb.w - x_ridge_split, pb.h, fill=C["surface_teal"], opacity=0.55)

    xticks = [
        (0.0625, "1/16"),
        (0.25, "1/4"),
        (1.0, "1"),
        (4.0, "4"),
        (16.0, "16"),
        (64.0, "64"),
        (256.0, "256"),
        (1024.0, "1024"),
    ]
    yticks = [
        (0.01, "0.01"),
        (0.1, "0.1"),
        (1.0, "1"),
        (10.0, "10"),
        (100.0, "100"),
        (1000.0, "1000"),
    ]
    for vx, lbl in xticks:
        gx = pb.px(vx)
        svg.line(gx, pb.y, gx, pb.y + pb.h, stroke=C["grid"], sw=1.0)
        svg.line(gx, pb.y + pb.h, gx, pb.y + pb.h + 5, stroke=C["axis"], sw=1.4)
        svg.text(gx, pb.y + pb.h + 22, lbl, size=14, color=C["muted"], anchor="middle", mono=True)
    for vy, lbl in yticks:
        gy = pb.py(vy)
        svg.line(pb.x, gy, pb.x + pb.w, gy, stroke=C["grid"], sw=1.0)
        svg.line(pb.x - 5, gy, pb.x, gy, stroke=C["axis"], sw=1.4)
        svg.text(pb.x - 10, gy + 5, lbl, size=14, color=C["muted"], anchor="end", mono=True)
    svg.line(pb.x, pb.y + pb.h, pb.x + pb.w, pb.y + pb.h, stroke=C["slate"], sw=1.8)
    svg.line(pb.x, pb.y, pb.x, pb.y + pb.h, stroke=C["slate"], sw=1.8)
    svg.text(pb.x + pb.w / 2, pb.y + pb.h + 48, "Arithmetic Intensity I (FLOP / Byte, log scale)", size=15.5, color=C["ink2"], weight="bold", anchor="middle")
    svg.text(pb.x - 62, pb.y + pb.h / 2, "Attainable Performance R (TFLOP/s)", size=15.5, color=C["ink2"], weight="bold", anchor="middle", rotate=-90)

    svg.text(pb.px(0.8), pb.y + 24, "Memory-Bound Regime", size=15, color=C["coral"], weight="bold", anchor="middle")
    svg.text(pb.px(64), pb.y + 24, "Compute-Bound Regime", size=15, color=C["teal"], weight="bold", anchor="middle")

    xs = np.geomspace(0.0625, 1024.0, 400)
    r_cpu = np.minimum(4.0, 0.300 * xs)
    r_gpu_fp64 = np.minimum(34.0, 3.350 * xs)
    r_gpu_bf16 = np.minimum(989.0, 3.350 * xs)

    pb.plot_curve(xs, r_gpu_bf16, stroke=C["violet"], sw=3.2)
    pb.plot_curve(xs, r_gpu_fp64, stroke=C["teal"], sw=3.2)
    pb.plot_curve(xs, r_cpu, stroke=C["blue"], sw=3.2)

    ridges = [
        (13.33, 4.0, "I*=13.3", C["blue"], 12, 22, "start"),
        (10.15, 34.0, "I*=10.1", C["teal"], -12, -12, "end"),
        (295.2, 989.0, "I*=295", C["violet"], -12, -10, "end"),
    ]
    for rx, ry, rlbl, col, dx_t, dy_t, anch in ridges:
        svg.circle(pb.px(rx), pb.py(ry), 5.5, fill=C["white"], stroke=col, sw=2.4)
        svg.line(pb.px(rx), pb.py(ry) + 6, pb.px(rx), pb.y + pb.h, stroke=col, sw=1.1, dash="3,4")
        svg.text(pb.px(rx) + dx_t, pb.py(ry) + dy_t, rlbl, size=13.5, color=col, weight="bold", anchor=anch, mono=True)

    svg.text(pb.px(960), pb.py(989) + 22, "GPU BF16 Tensor: 989 TF", size=14, color=C["violet"], weight="bold", anchor="end")
    svg.text(pb.px(960), pb.py(34) - 10, "GPU HBM3 FP64: 34 TF (3.35 TB/s)", size=14, color=C["teal"], weight="bold", anchor="end")
    svg.text(pb.px(960), pb.py(4.0) - 10, "CPU DDR5 FP64: 4 TF (300 GB/s)", size=14, color=C["blue"], weight="bold", anchor="end")

    kernels = [
        (0.17, 0.44, "STREAM Triad", "I=0.17", C["coral"], 12, 5, "start"),
        (0.25, 0.060, "HPCG SpMV", "I=0.25", C["coral"], 12, 6, "start"),
        (1.5, 2.0, "3D Stencil", "I=1.5", C["gold"], -12, 5, "end"),
        (120.0, 72.0, "Dense GEMM", "I=120", C["violet"], -12, 5, "end"),
    ]
    for kx, ky, kname, ki, col, ox, oy, anch in kernels:
        px_k, py_k = pb.px(kx), pb.py(ky)
        svg.circle(px_k, py_k, 6.5, fill=col, stroke=C["white"], sw=1.8)
        svg.text(px_k + ox, py_k + oy, f"{kname} ({ki})", size=13.5, color=col, weight="bold", anchor=anch)

    sx0, sy0 = pb.px(1.5), pb.py(2.0)
    svg.line(sx0 + 12, sy0 - 10, pb.px(6.8), sy0 - 10, stroke=C["gold"], sw=2.2, marker_end="arr_gold")
    svg.text(pb.px(3.2), sy0 - 20, "Reduce traffic (right)", size=13, color=C["gold"], weight="bold", anchor="middle")

    gx0, gy0 = pb.px(120.0), pb.py(72.0)
    svg.line(gx0, gy0 - 10, gx0, pb.py(310.0), stroke=C["violet"], sw=2.2, marker_end="arr_violet")
    svg.text(gx0 + 12, pb.py(155.0), "SIMD / Tensor (up)", size=13.5, color=C["violet"], weight="bold")

    svg.rect(32, 608, 896, 36, fill=C["surface"], stroke=C["grid"], sw=1.1, rx=6)
    svg.text(
        480,
        631,
        "Tuning order: measure I and R first → if I < I*, cut bytes moved (right); if I ≥ I*, unlock SIMD/Tensor pipelines (up)",
        size=13.8,
        color=C["ink2"],
        anchor="middle",
    )

    return svg.save_and_render("m04_roofline_model")


def build_m05_simd_openmp_numa() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Single-Node CPU Efficiency: SIMD, Cache Lines, and NUMA",
        "Data layout, 64B cache-line isolation, and First-Touch thread pinning govern single-node scaling",
        accent=C["blue"],
    )

    svg.panel_box(32, 86, 896, 174, "1. AVX-512 SIMD (8×FP64 = 512-bit): Contiguous SoA vs. Strided AoS", accent=C["blue"])

    svg.text(56, 146, "SoA (Structure of Arrays) — Contiguous Load", size=14.5, color=C["teal"], weight="bold")
    lane_x0 = 56
    lane_y = 158
    lw = 44
    for i in range(8):
        svg.rect(lane_x0 + i * (lw + 3), lane_y, lw, 30, fill=C["surface_teal"], stroke=C["teal"], sw=1.4, rx=4)
        svg.text(lane_x0 + i * (lw + 3) + lw / 2, lane_y + 20, f"x[{i}]", size=13, color=C["teal"], weight="bold", anchor="middle", mono=True)
    svg.line(lane_x0 + 186, lane_y + 34, lane_x0 + 186, lane_y + 52, stroke=C["teal"], sw=2.0, marker_end="arr_teal")
    svg.rect(lane_x0, lane_y + 56, 373, 30, fill=C["teal"], rx=5)
    svg.text(lane_x0 + 186, lane_y + 76, "Single vmovupd + vfmadd231pd (8 lanes full)", size=13.5, color=C["white"], weight="bold", anchor="middle")

    ax0 = 492
    svg.text(ax0, 146, "AoS (Array of Structures) — Strided Gather", size=14.5, color=C["coral"], weight="bold")
    fields = ["x0", "y0", "z0", "x1", "y1", "z1", "x2", "y2", "z2"]
    fw = 42
    for i, f in enumerate(fields):
        is_x = f.startswith("x")
        fill = C["surface_coral"] if is_x else C["surface"]
        st = C["coral"] if is_x else C["axis"]
        tc = C["coral"] if is_x else C["muted"]
        svg.rect(ax0 + i * (fw + 3), lane_y, fw, 30, fill=fill, stroke=st, sw=1.3, rx=4)
        svg.text(ax0 + i * (fw + 3) + fw / 2, lane_y + 20, f, size=13, color=tc, weight="bold" if is_x else "normal", anchor="middle", mono=True)
    svg.line(ax0 + 202, lane_y + 34, ax0 + 202, lane_y + 52, stroke=C["coral"], sw=2.0, marker_end="arr_coral")
    svg.rect(ax0, lane_y + 56, 402, 30, fill=C["surface_coral"], stroke=C["coral"], sw=1.4, rx=5)
    svg.text(ax0 + 201, lane_y + 76, "Slow vgatherdpd; 67% of cache line unused", size=13.5, color=C["coral"], weight="bold", anchor="middle")

    svg.panel_box(32, 276, 896, 174, "2. OpenMP 64B Cache-Line False Sharing vs. Padded Accumulators", accent=C["coral"])

    svg.text(56, 336, "Bug: Adjacent sums share one 64B cache line", size=14.5, color=C["coral"], weight="bold")
    svg.rect(56, 348, 376, 56, fill=C["surface_coral"], stroke=C["coral"], sw=1.6, dash="5,3", rx=6)
    svg.text(244, 365, "Single 64-Byte Cache Line (MESI invalidation storm)", size=12.5, color=C["coral"], weight="bold", anchor="middle")
    for i in range(4):
        bx = 68 + i * 89
        svg.rect(bx, 372, 82, 24, fill=C["white"], stroke=C["coral"], sw=1.2, rx=4)
        svg.text(bx + 41, 389, f"sum[{i}]", size=12.5, color=C["ink"], anchor="middle", mono=True)
    svg.text(244, 428, "T0–T3 concurrent writes trigger cache-line ping-pong", size=13.5, color=C["coral"], anchor="middle")

    rx0 = 492
    svg.text(rx0, 336, "Fix: 64B padding or reduction(+:s)", size=14.5, color=C["teal"], weight="bold")
    for i in range(4):
        bx = rx0 + i * 102
        svg.rect(bx, 348, 94, 48, fill=C["surface_teal"], stroke=C["teal"], sw=1.4, rx=5)
        svg.text(bx + 47, 368, f"T{i} own line", size=12.5, color=C["teal"], weight="bold", anchor="middle")
        svg.text(bx + 47, 387, "alignas(64)", size=11.5, color=C["ink2"], anchor="middle", mono=True)
    svg.rect(rx0, 408, 400, 28, fill=C["surface"], stroke=C["teal"], sw=1.2, rx=4)
    svg.text(rx0 + 200, 427, "OMP_PROC_BIND=close  OMP_PLACES=cores", size=13, color=C["teal"], weight="bold", anchor="middle", mono=True)

    svg.panel_box(32, 466, 896, 170, "3. Dual-Socket NUMA First-Touch Parallel Initialization Alignment", accent=C["teal"])

    svg.rect(56, 514, 174, 46, fill=C["surface_blue"], stroke=C["blue"], sw=1.5, rx=6)
    svg.text(143, 534, "Threads 0 .. N/2−1", size=13.5, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(143, 552, "Socket 0 Cores", size=13, color=C["ink2"], anchor="middle")

    svg.line(234, 537, 294, 537, stroke=C["blue"], sw=2.2, marker_end="arr_blue")
    svg.text(264, 528, "Init + Comp", size=11.5, color=C["blue"], weight="bold", anchor="middle")

    svg.rect(298, 514, 156, 46, fill=C["white"], stroke=C["blue"], sw=1.6, rx=6)
    svg.text(376, 534, "A[0 .. M/2−1]", size=13.5, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(376, 552, "NUMA Node 0 DRAM", size=12.5, color=C["muted"], anchor="middle")

    svg.rect(492, 514, 174, 46, fill=C["surface_teal"], stroke=C["teal"], sw=1.5, rx=6)
    svg.text(579, 534, "Threads N/2 .. N−1", size=13.5, color=C["teal"], weight="bold", anchor="middle", mono=True)
    svg.text(579, 552, "Socket 1 Cores", size=13, color=C["ink2"], anchor="middle")

    svg.line(670, 537, 730, 537, stroke=C["teal"], sw=2.2, marker_end="arr_teal")
    svg.text(700, 528, "Init + Comp", size=11.5, color=C["teal"], weight="bold", anchor="middle")

    svg.rect(734, 514, 166, 46, fill=C["white"], stroke=C["teal"], sw=1.6, rx=6)
    svg.text(817, 534, "A[M/2 .. M−1]", size=13.5, color=C["teal"], weight="bold", anchor="middle", mono=True)
    svg.text(817, 552, "NUMA Node 1 DRAM", size=12.5, color=C["muted"], anchor="middle")

    svg.rect(56, 578, 844, 42, fill=C["surface_gold"], stroke=C["gold"], sw=1.1, rx=6)
    svg.text(
        478,
        604,
        "Checklist: verify AVX-512 via compiler opt-report, rule out false sharing with perf c2c, confirm 100% local pages in numastat",
        size=13.5,
        color=C["ink"],
        weight="bold",
        anchor="middle",
    )

    return svg.save_and_render("m05_simd_openmp_numa")


def build_m06_mpi_halo_hockney() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "MPI Communication Cost Model & 3D Halo Overlap",
        "Hockney T(m) = α + m/B separates latency vs. bandwidth regimes; non-blocking MPI hides halo transfers",
        accent=C["blue"],
    )

    svg.panel_box(32, 88, 468, 542, "Hockney Model (NDR400 IB: α=1.8 μs, B=50 GB/s)", accent=C["blue"])

    pb = PlotBox(svg, 108, 152, 366, 344, xmin=16, xmax=64 * 1024 * 1024, ymin=1.0, ymax=2000.0, xlog=True, ylog=True)

    m_half = 90000.0
    x_mh = pb.px(m_half)
    svg.rect(pb.x, pb.y, x_mh - pb.x, pb.h, fill=C["surface_coral"], opacity=0.55)
    svg.rect(x_mh, pb.y, pb.x + pb.w - x_mh, pb.h, fill=C["surface_teal"], opacity=0.55)

    xticks = [
        (64, "64B"),
        (1024, "1KB"),
        (16384, "16KB"),
        (262144, "256KB"),
        (4194304, "4MB"),
        (67108864, "64MB"),
    ]
    yticks = [
        (1.0, "1"),
        (10.0, "10"),
        (100.0, "100"),
        (1000.0, "1000"),
    ]
    for vx, lbl in xticks:
        gx = pb.px(vx)
        svg.line(gx, pb.y, gx, pb.y + pb.h, stroke=C["grid"], sw=1.0)
        svg.line(gx, pb.y + pb.h, gx, pb.y + pb.h + 5, stroke=C["axis"], sw=1.4)
        svg.text(gx, pb.y + pb.h + 22, lbl, size=12.5, color=C["muted"], anchor="middle", mono=True)
    for vy, lbl in yticks:
        gy = pb.py(vy)
        svg.line(pb.x, gy, pb.x + pb.w, gy, stroke=C["grid"], sw=1.0)
        svg.line(pb.x - 5, gy, pb.x, gy, stroke=C["axis"], sw=1.4)
        svg.text(pb.x - 10, gy + 5, lbl, size=13, color=C["muted"], anchor="end", mono=True)
    svg.line(pb.x, pb.y + pb.h, pb.x + pb.w, pb.y + pb.h, stroke=C["slate"], sw=1.8)
    svg.line(pb.x, pb.y, pb.x, pb.y + pb.h, stroke=C["slate"], sw=1.8)
    svg.text(pb.x + pb.w / 2, pb.y + pb.h + 46, "Message Size m (Bytes, log scale)", size=14.5, color=C["ink2"], weight="bold", anchor="middle")
    svg.text(pb.x - 52, pb.y + pb.h / 2, "Transfer Time T(m) (μs)", size=14.5, color=C["ink2"], weight="bold", anchor="middle", rotate=-90)

    svg.text(pb.px(950), pb.y + 24, "Latency-Dominated", size=13.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(pb.px(950), pb.y + 42, "T ≈ α (coalesce msgs)", size=12.5, color=C["coral"], anchor="middle")
    svg.text(pb.px(3.5e6), pb.y + 24, "Bandwidth-Dominated", size=13.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb.px(3.5e6), pb.y + 42, "T ≈ m / B", size=12.5, color=C["teal"], anchor="middle")

    ms = np.geomspace(16, 64 * 1024 * 1024, 300)
    t_us = 1.8 + ms / 50000.0
    pb.plot_curve(ms, t_us, stroke=C["blue"], sw=3.2)

    svg.line(pb.x, pb.py(1.8), x_mh, pb.py(1.8), stroke=C["coral"], sw=1.4, dash="4,4")
    svg.text(pb.px(45), pb.py(1.8) - 8, "α = 1.8 μs", size=13, color=C["coral"], weight="bold", mono=True)

    svg.line(x_mh, pb.y + 52, x_mh, pb.y + pb.h, stroke=C["gold"], sw=1.8, dash="5,4")
    svg.circle(x_mh, pb.py(3.6), 6.0, fill=C["gold"], stroke=C["white"], sw=1.8)
    svg.rect(x_mh - 76, pb.py(3.6) - 44, 156, 30, fill=C["white"], stroke=C["gold"], sw=1.2, rx=4)
    svg.text(x_mh + 2, pb.py(3.6) - 24, "m₁/₂ = α·B = 90 KB", size=13, color=C["gold"], weight="bold", anchor="middle", mono=True)

    svg.rect(52, 558, 428, 54, fill=C["surface_blue"], stroke=C["blue"], sw=1.1, rx=6)
    svg.text(64, 580, "Takeaway: below 90 KB, link utilization stays under 50%;", size=13.5, color=C["blue"], weight="bold")
    svg.text(64, 600, "pack small buffers to amortize per-message latency α.", size=13.5, color=C["ink2"])

    svg.panel_box(516, 88, 412, 268, "3D Domain Decomposition: O(L³) vs. O(6L²)", accent=C["teal"])

    cx, cy = 626, 224
    dx_c, dy_c = 58, 30
    h_c = 78
    p_top = [(cx, cy - h_c), (cx + dx_c, cy - h_c + dy_c), (cx, cy - h_c + 2 * dy_c), (cx - dx_c, cy - h_c + dy_c)]
    p_left = [(cx - dx_c, cy - h_c + dy_c), (cx, cy - h_c + 2 * dy_c), (cx, cy + 2 * dy_c), (cx - dx_c, cy + dy_c)]
    p_right = [(cx, cy - h_c + 2 * dy_c), (cx + dx_c, cy - h_c + dy_c), (cx + dx_c, cy + dy_c), (cx, cy + 2 * dy_c)]

    svg.polygon(p_top, fill=C["surface_teal"], stroke=C["teal"], sw=1.8)
    svg.polygon(p_left, fill=C["surface_blue"], stroke=C["blue"], sw=1.8)
    svg.polygon(p_right, fill=C["surface_coral"], stroke=C["coral"], sw=1.8)

    svg.line(cx - dx_c / 2, cy - h_c + dy_c / 2, cx + dx_c / 2, cy - h_c + 1.5 * dy_c, stroke=C["teal"], sw=1.0, dash="3,3")
    svg.line(cx + dx_c / 2, cy - h_c + dy_c / 2, cx - dx_c / 2, cy - h_c + 1.5 * dy_c, stroke=C["teal"], sw=1.0, dash="3,3")
    svg.line(cx - dx_c, cy - h_c / 2 + dy_c, cx, cy - h_c / 2 + 2 * dy_c, stroke=C["blue"], sw=1.0, dash="3,3")
    svg.line(cx, cy - h_c / 2 + 2 * dy_c, cx + dx_c, cy - h_c / 2 + dy_c, stroke=C["coral"], sw=1.0, dash="3,3")

    svg.text(cx - dx_c - 12, cy - 10, "L", size=14.5, color=C["ink"], weight="bold", anchor="end", mono=True)
    svg.text(cx, cy + 2 * dy_c + 24, "L³ subdomain (6 halo faces)", size=13.5, color=C["ink2"], weight="bold", anchor="middle")

    svg.rect(710, 144, 202, 188, fill=C["surface"], stroke=C["grid"], sw=1.1, rx=6)
    svg.text(722, 170, "Surface / Volume Ratio", size=14, color=C["ink"], weight="bold")
    svg.text(722, 198, "Comm / Comp", size=13.5, color=C["coral"], weight="bold", mono=True)
    svg.text(722, 220, "∝ 6L² / L³ = 6/L", size=14, color=C["coral"], weight="bold", mono=True)
    svg.line(722, 234, 900, 234, stroke=C["grid"], sw=1.0)
    svg.multiline(
        722,
        258,
        [
            "• 3D cuts beat 1D slabs",
            "• Larger L lowers comm %",
            "• Small L hits strong wall",
        ],
        size=13,
        color=C["ink2"],
        lh=22,
    )

    svg.panel_box(516, 372, 412, 258, "Non-Blocking MPI_Isend/Irecv Overlap", accent=C["violet"])

    svg.text(534, 430, "Blocking: Halo exchange serialized with compute", size=13.5, color=C["coral"], weight="bold")
    y_b1 = 440
    svg.rect(534, y_b1, 126, 32, fill=C["coral"], rx=4)
    svg.text(597, y_b1 + 21, "Halo Comm", size=13, color=C["white"], weight="bold", anchor="middle")
    svg.rect(664, y_b1, 184, 32, fill=C["blue"], rx=4)
    svg.text(756, y_b1 + 21, "Interior Compute", size=13, color=C["white"], weight="bold", anchor="middle")
    svg.rect(852, y_b1, 58, 32, fill=C["teal"], rx=4)
    svg.text(881, y_b1 + 21, "Bdry", size=13, color=C["white"], weight="bold", anchor="middle")

    svg.text(534, 502, "Non-blocking: Isend/Irecv overlapped with interior", size=13.5, color=C["teal"], weight="bold")
    y_b2 = 512
    svg.rect(534, y_b2, 184, 28, fill=C["blue"], rx=4)
    svg.text(626, y_b2 + 19, "Interior Compute (no halo)", size=12.5, color=C["white"], weight="bold", anchor="middle")
    svg.rect(534, y_b2 + 34, 126, 26, fill=C["violet"], rx=4)
    svg.text(597, y_b2 + 51, "Async RDMA Transfer", size=11.5, color=C["white"], weight="bold", anchor="middle")
    svg.rect(722, y_b2, 62, 60, fill=C["teal"], rx=4)
    svg.text(753, y_b2 + 27, "Waitall", size=11.5, color=C["white"], weight="bold", anchor="middle", mono=True)
    svg.text(753, y_b2 + 46, "+ Bdry", size=12, color=C["white"], weight="bold", anchor="middle")

    svg.line(788, y_b2 + 30, 908, y_b2 + 30, stroke=C["teal"], sw=2.0, marker_start="arr_teal", marker_end="arr_teal")
    svg.text(848, y_b2 + 20, "Hidden halo time", size=12.5, color=C["teal"], weight="bold", anchor="middle")

    svg.text(534, 608, "Requirement: interior compute time ≥ halo transfer time.", size=13, color=C["muted"])

    return svg.save_and_render("m06_mpi_halo_hockney")


def build_m07_cuda_gemm_tiling() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "GPU GEMM Hierarchical Tiling & Optimization Ladder",
        "Staging tiles from HBM through Shared Memory to thread registers reduces global traffic by B_K×",
        accent=C["blue"],
    )

    svg.panel_box(32, 86, 896, 250, "Three-Level Tiling Flow: HBM → Shared Memory (Block) → Registers (Thread Micro-Tile)", accent=C["blue"])

    x1, y1, w1, h1 = 56, 138, 224, 178
    svg.rect(x1, y1, w1, h1, fill=C["surface_coral"], stroke=C["coral"], sw=1.7, rx=8)
    svg.text(x1 + w1 / 2, y1 + 24, "1. HBM Global Memory", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(x1 + w1 / 2, y1 + 44, "~3.35 TB/s · ~100 ns", size=12.5, color=C["muted"], anchor="middle", mono=True)
    svg.rect(x1 + 22, y1 + 62, 78, 78, fill=C["white"], stroke=C["coral"], sw=1.3, rx=3)
    svg.rect(x1 + 22, y1 + 82, 78, 18, fill=C["blue"], opacity=0.35)
    svg.rect(x1 + 48, y1 + 82, 22, 18, fill=C["blue"])
    svg.text(x1 + 61, y1 + 156, "A (M×K)", size=12.5, color=C["ink2"], anchor="middle", mono=True)

    svg.rect(x1 + 124, y1 + 62, 78, 78, fill=C["white"], stroke=C["coral"], sw=1.3, rx=3)
    svg.rect(x1 + 152, y1 + 62, 18, 78, fill=C["gold"], opacity=0.35)
    svg.rect(x1 + 152, y1 + 88, 18, 22, fill=C["gold"])
    svg.text(x1 + 163, y1 + 156, "B (K×N)", size=12.5, color=C["ink2"], anchor="middle", mono=True)

    svg.line(x1 + w1 + 4, y1 + 88, x1 + w1 + 54, y1 + 88, stroke=C["blue"], sw=2.4, marker_end="arr_blue")
    svg.text(x1 + w1 + 29, y1 + 74, "float4", size=12, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(x1 + w1 + 29, y1 + 108, "Coalesced", size=11.5, color=C["blue"], anchor="middle")

    x2, w2 = 342, 250
    svg.rect(x2, y1, w2, h1, fill=C["surface_blue"], stroke=C["blue"], sw=1.7, rx=8)
    svg.text(x2 + w2 / 2, y1 + 24, "2. Shared Memory (On-SM)", size=14.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(x2 + w2 / 2, y1 + 44, "On-chip SRAM · Double buffer", size=12.5, color=C["muted"], anchor="middle")

    svg.rect(x2 + 24, y1 + 64, 52, 78, fill=C["blue"], opacity=0.22, stroke=C["blue"], sw=1.5, rx=3)
    svg.text(x2 + 50, y1 + 102, "As", size=14, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(x2 + 50, y1 + 120, "B_M×B_K", size=11.5, color=C["ink2"], anchor="middle", mono=True)

    svg.rect(x2 + 100, y1 + 64, 122, 46, fill=C["gold"], opacity=0.25, stroke=C["gold"], sw=1.5, rx=3)
    svg.text(x2 + 161, y1 + 86, "Bs (B_K×B_N)", size=13, color=C["gold"], weight="bold", anchor="middle", mono=True)

    svg.rect(x2 + 100, y1 + 122, 122, 40, fill=C["white"], stroke=C["blue"], sw=1.2, rx=4)
    svg.text(x2 + 161, y1 + 140, "HBM traffic ÷ B_K", size=12.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(x2 + 161, y1 + 156, "Avoid bank conflicts", size=11.5, color=C["muted"], anchor="middle")

    svg.line(x2 + w2 + 4, y1 + 88, x2 + w2 + 54, y1 + 88, stroke=C["teal"], sw=2.4, marker_end="arr_teal")
    svg.text(x2 + w2 + 29, y1 + 74, "Outer prod", size=11.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(x2 + w2 + 29, y1 + 108, "T_M×T_N", size=11.5, color=C["teal"], anchor="middle", mono=True)

    x3, w3 = 654, 250
    svg.rect(x3, y1, w3, h1, fill=C["surface_teal"], stroke=C["teal"], sw=1.7, rx=8)
    svg.text(x3 + w3 / 2, y1 + 24, "3. Thread Register Micro-Tile", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(x3 + w3 / 2, y1 + 44, "Zero-wait accum · full FMA", size=12.5, color=C["muted"], anchor="middle")

    svg.rect(x3 + 26, y1 + 86, 22, 58, fill=C["blue"], rx=3)
    svg.text(x3 + 37, y1 + 160, "T_M", size=12, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(x3 + 64, y1 + 118, "⊗", size=18, color=C["ink"], weight="bold", anchor="middle")
    svg.rect(x3 + 84, y1 + 58, 66, 20, fill=C["gold"], rx=3)
    svg.text(x3 + 117, y1 + 72, "T_N", size=12, color=C["white"], weight="bold", anchor="middle", mono=True)
    svg.rect(x3 + 84, y1 + 86, 66, 58, fill=C["white"], stroke=C["teal"], sw=1.8, rx=4)
    for r in range(1, 3):
        svg.line(x3 + 84, y1 + 86 + r * 19.3, x3 + 150, y1 + 86 + r * 19.3, stroke=C["teal"], sw=0.9)
    for c in range(1, 3):
        svg.line(x3 + 84 + c * 22, y1 + 86, x3 + 84 + c * 22, y1 + 144, stroke=C["teal"], sw=0.9)
    svg.text(x3 + 117, y1 + 160, "C reg tile", size=12, color=C["teal"], weight="bold", anchor="middle")

    svg.multiline(
        x3 + 160,
        y1 + 98,
        ["1 SMEM load", "feeds T_M·T_N", "FMA ops"],
        size=12.5,
        color=C["ink2"],
        lh=19,
    )

    svg.panel_box(32, 352, 896, 282, "Illustrative CUDA FP32 GEMM Optimization Ladder (% of cuBLAS)", accent=C["teal"])

    steps = [
        ("1. Naive Global Access", 3, C["coral"], "Uncoalesced; HBM read per FMA"),
        ("2. Coalesced Global Loads", 14, C["coral"], "Contiguous 128B warp transactions"),
        ("3. Shared Memory Tiling", 38, C["gold"], "Block-level reuse cuts HBM traffic"),
        ("4. 2D Register Blocking", 68, C["blue"], "Amortizes SMEM loads via micro-tile"),
        ("5. float4 + Double Buffer", 86, C["teal"], "128-bit loads & prefetch overlap"),
        ("6. cuBLAS Reference", 100, C["violet"], "SASS scheduling + Tensor/optimal tile"),
    ]

    bx0 = 256
    bw_full = 360
    y_start = 404
    row_g = 35
    bar_h = 23

    for pct in [0, 25, 50, 75, 100]:
        gx = bx0 + (pct / 100.0) * bw_full
        svg.line(gx, y_start - 6, gx, y_start + 6 * row_g - 8, stroke=C["grid"], sw=1.0)
        svg.text(gx, y_start + 6 * row_g + 10, f"{pct}%", size=12.5, color=C["muted"], anchor="middle", mono=True)
    svg.line(bx0, y_start - 6, bx0, y_start + 6 * row_g - 8, stroke=C["slate"], sw=1.5)

    for idx, (label, pct, col, note) in enumerate(steps):
        ry = y_start + idx * row_g
        svg.text(bx0 - 12, ry + 16, label, size=14, color=C["ink"], weight="bold", anchor="end")
        w_b = max(10.0, (pct / 100.0) * bw_full)
        svg.rect(bx0, ry, w_b, bar_h, fill=col, rx=4)
        if pct >= 18:
            svg.text(bx0 + w_b - 8, ry + 16, f"{pct}%", size=13, color=C["white"], weight="bold", anchor="end", mono=True)
        else:
            svg.text(bx0 + w_b + 8, ry + 16, f"{pct}%", size=13, color=col, weight="bold", mono=True)
        svg.text(bx0 + bw_full + 20, ry + 16, note, size=13.5, color=C["ink2"])

    return svg.save_and_render("m07_cuda_gemm_tiling")


def main() -> None:
    builders = [
        build_00_knowledge_graph,
        build_00_roadmap_timeline,
        build_m01_gemm_work_traffic,
        build_m02_memory_hierarchy_numa,
        build_m03_amdahl_gustafson,
        build_m04_roofline_model,
        build_m05_simd_openmp_numa,
        build_m06_mpi_halo_hockney,
        build_m07_cuda_gemm_tiling,
    ]
    for fn in builders:
        out = fn()
        print(f"Rendered: {out}")


if __name__ == "__main__":
    main()
