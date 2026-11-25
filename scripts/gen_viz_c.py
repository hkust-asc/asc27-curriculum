#!/usr/bin/env python3
"""Generate 10 minimalist SVG/PNG diagrams (c01-c10) for verified past ASC problems."""

from __future__ import annotations

import math
from pathlib import Path
from typing import List, Tuple

import numpy as np

from svg_kit import C, PlotBox, SVGCanvas


def pill(
    svg: SVGCanvas,
    x: float,
    y: float,
    w: float,
    h: float,
    label: str,
    fill: str,
    stroke: str,
    text_color: str,
    size: float = 15,
    weight: str = "bold",
    mono: bool = False,
) -> None:
    svg.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.4, rx=h / 2)
    svg.text(x + w / 2, y + h * 0.66, label, size=size, color=text_color, weight=weight, anchor="middle", mono=mono)


def draw_hbar(
    svg: SVGCanvas,
    x: float,
    y: float,
    w: float,
    h: float,
    fill: str,
    stroke: str = "none",
    rx: float = 4,
) -> None:
    svg.rect(x, y, max(w, 2.0), h, fill=fill, stroke=stroke, sw=1.2 if stroke != "none" else 0, rx=rx)


# ---------------------------------------------------------------------------
# C01: ASC22 Yuan 4.7B LLM
# ---------------------------------------------------------------------------
def make_c01() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC22 Yuan 4.7B LLM: Training Layout & Convergence Gate",
        "40 layers · d=3072 · 24 heads · Seq 2048 · 1B tokens · PyTorch · Historical 3 kW cap",
        accent=C["blue"],
    )

    # Left Panel: Transformer FLOPs + 3D Parallel under 3 kW
    svg.panel_box(28, 92, 436, 536, "Transformer FLOPs & 3D Parallel Placement", accent=C["blue"])

    # FLOPs formula box
    svg.rect(46, 140, 400, 68, fill=C["surface_blue"], stroke=C["blue"], sw=1.3, rx=6)
    svg.text(62, 165, "Training compute  C ≈ 6 · Φ · D", size=16.0, color=C["blue"], weight="bold", mono=True)
    svg.text(62, 193, "6 × 4.7×10⁹ × 10⁹ ≈ 2.82 × 10¹⁹ FLOPs", size=15.5, color=C["ink"], weight="bold", mono=True)

    # Transformer layer block schematic
    svg.text(48, 232, "Single Layer (×40 layers, ~4.7B total params)", size=15.0, color=C["ink"], weight="bold")
    svg.rect(48, 244, 396, 134, fill=C["bg"], stroke=C["axis"], sw=1.3, rx=6, dash="5,4")
    svg.node_box(64, 258, 168, 54, "MHA (24 heads)", "d=3072, QKV+O", fill=C["white"], stroke=C["blue"], bar_color=C["blue"])
    svg.line(232, 285, 258, 285, stroke=C["blue"], sw=2.0, marker_end="arr_blue")
    svg.node_box(262, 258, 168, 54, "FFN (4d = 12288)", "W₁: d×4d, W₂: 4d×d", fill=C["white"], stroke=C["teal"], bar_color=C["teal"])
    svg.text(246, 336, "Params / layer ≈ 12d² ≈ 113M · Seq L = 2048", size=14.2, color=C["ink2"], anchor="middle")
    svg.text(246, 362, "Training state (weights+grads+Adam) > 1 GPU", size=14.2, color=C["coral"], weight="bold", anchor="middle")

    # 3D Parallel Placement Box under 3 kW
    svg.text(48, 404, "3D Parallel Partitioning under 3 kW Cap", size=15.0, color=C["ink"], weight="bold")
    svg.rect(48, 416, 396, 196, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)

    # Two nodes / GPU group diagram
    # Stage 0 & Stage 1 (PP) with TP inside node and DP across replicas
    stages = [
        (64, 434, "PP Stage 0 (L1–L20)", C["blue"], C["surface_blue"]),
        (256, 434, "PP Stage 1 (L21–L40)", C["violet"], C["surface_violet"]),
    ]
    for sx, sy, title, col, bg in stages:
        svg.rect(sx, sy, 172, 92, fill=bg, stroke=col, sw=1.4, rx=6)
        svg.text(sx + 86, sy + 22, title, size=14.5, color=col, weight="bold", anchor="middle")
        svg.rect(sx + 12, sy + 32, 68, 44, fill=C["white"], stroke=col, sw=1.2, rx=4)
        svg.text(sx + 46, sy + 52, "GPU 0", size=14, color=C["ink"], weight="bold", anchor="middle")
        svg.text(sx + 46, sy + 69, "TP 0", size=13, color=C["muted"], anchor="middle", mono=True)
        svg.rect(sx + 92, sy + 32, 68, 44, fill=C["white"], stroke=col, sw=1.2, rx=4)
        svg.text(sx + 126, sy + 52, "GPU 1", size=14, color=C["ink"], weight="bold", anchor="middle")
        svg.text(sx + 126, sy + 69, "TP 1", size=13, color=C["muted"], anchor="middle", mono=True)
        svg.line(sx + 80, sy + 54, sx + 92, sy + 54, stroke=col, sw=1.8)

    # PP arrow between stages
    svg.line(236, 480, 254, 480, stroke=C["violet"], sw=2.0, marker_end="arr_violet")

    # Communication legend pills
    svg.text(64, 550, "TP: Intra-node NVLink All-Reduce (high BW)", size=14.2, color=C["blue"], weight="bold")
    svg.text(64, 574, "PP: P2P activations (minimize bubbles)", size=14.2, color=C["violet"], weight="bold")
    svg.text(64, 598, "DP/ZeRO: Ring grad sync · Cluster ≤ 3 kW", size=14.2, color=C["gold"], weight="bold")

    # Right Panel: Synthetic Schematic Training Loss Curve
    svg.panel_box(484, 92, 448, 536, "Schematic Convergence & Acceptance Gate", accent=C["teal"])

    pb = PlotBox(svg, 560, 152, 344, 300, xmin=0.0, xmax=1.05, ymin=5.0, ymax=11.0)
    pb.draw_axes(
        xticks=[(0.0, "0"), (0.25, "0.25B"), (0.5, "0.5B"), (0.75, "0.75B"), (1.0, "1.0B")],
        yticks=[(5.0, "5.0"), (6.0, "6.0"), (7.0, "7.0"), (8.0, "8.0"), (9.0, "9.0"), (10.0, "10.0"), (11.0, "11.0")],
        xlabel="Trained Tokens (Schematic)",
        ylabel="NLL Training Loss",
    )

    # Shaded pass region below loss 7.0
    y7 = pb.py(7.0)
    svg.rect(pb.x, y7, pb.w, pb.y + pb.h - y7, fill=C["surface_teal"], opacity=0.7)
    svg.line(pb.x, y7, pb.x + pb.w, y7, stroke=C["coral"], sw=2.2, dash="7,5")
    svg.text(pb.x + pb.w - 6, y7 - 10, "Hard gate: Loss < 7.0", size=14.5, color=C["coral"], weight="bold", anchor="end")
    svg.text(pb.x + pb.w - 6, y7 + 22, "Pass region", size=14.5, color=C["teal"], weight="bold", anchor="end")

    # Vertical line at 1.0B tokens
    x1b = pb.px(1.0)
    svg.line(x1b, pb.y, x1b, pb.y + pb.h, stroke=C["gold"], sw=1.8, dash="4,4")
    svg.text(x1b - 6, pb.y + 18, "1B tokens", size=14.5, color=C["gold"], weight="bold", anchor="end")

    # Smooth synthetic schematic loss curve crossing 7.0 around 0.72B
    xs = np.linspace(0.015, 1.0, 140)
    ys = 5.85 + 4.95 * np.exp(-3.4 * xs) + 0.75 * np.exp(-18.0 * xs) + 0.06 * np.sin(36 * xs) * np.exp(-1.5 * xs)
    pb.plot_curve(xs, ys, stroke=C["blue"], sw=3.0)

    # Find exact crossing point near 7.0
    idx_cross = int(np.argmin(np.abs(ys - 7.0)))
    cx_val, cy_val = float(xs[idx_cross]), float(ys[idx_cross])
    svg.circle(pb.px(cx_val), pb.py(cy_val), 6.0, fill=C["teal"], stroke=C["white"], sw=2.0)
    svg.line(pb.px(cx_val), pb.py(cy_val) - 8, pb.px(cx_val) + 34, pb.py(cy_val) - 52, stroke=C["teal"], sw=1.5)
    svg.text(pb.px(cx_val) + 38, pb.py(cy_val) - 56, f"Crosses 7.0 (~{cx_val:.2f}B)", size=14.0, color=C["teal"], weight="bold")

    # End marker at 1.0B
    end_y = float(ys[-1])
    svg.circle(pb.px(1.0), pb.py(end_y), 5.5, fill=C["blue"], stroke=C["white"], sw=2.0)
    svg.text(pb.px(1.0) - 12, pb.py(end_y) + 22, f"End ~{end_y:.2f} (schematic)", size=14.0, color=C["blue"], weight="bold", anchor="end")

    # Bottom acceptance checklist inside right panel
    svg.rect(504, 514, 408, 96, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(520, 538, "ASC22 Acceptance & Scoring Rules", size=15.5, color=C["ink"], weight="bold")
    svg.multiline(
        520,
        562,
        [
            "• PyTorch only (Megatron-LM / DeepSpeed allowed)",
            "• Loss ≥ 7.0 or missing logs / TensorBoard → 0 pts",
        ],
        size=14.0,
        color=C["ink2"],
        lh=24,
    )

    return svg.save_and_render("c01_asc22_yuan_llm", png_width=1800)


# ---------------------------------------------------------------------------
# C02: ASC22 DeePMD-kit
# ---------------------------------------------------------------------------
def make_c02() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC22 DeePMD-kit: Compute Pipeline & Bottlenecks",
        "Systems: water / Cu / Al-Cu-Mg · Gate: dp test consistency · Historical 3 kW finals cap",
        accent=C["teal"],
    )

    # Top pipeline box
    svg.panel_box(28, 92, 904, 274, "End-to-End Potential Energy Surface Pipeline (Bottleneck Profile)", accent=C["blue"])

    # 4 stages left-to-right
    # Stage 1: Atomic Coordinates
    svg.rect(48, 148, 162, 148, fill=C["surface"], stroke=C["slate"], sw=1.6, rx=8)
    svg.text(129, 176, "1. Coordinates", size=16.0, color=C["ink"], weight="bold", anchor="middle")
    svg.text(129, 200, "R = {r1, ..., rN}", size=13.5, color=C["blue"], anchor="middle", mono=True)
    svg.text(129, 224, "Atom types + PBC", size=14.2, color=C["ink2"], anchor="middle")
    pill(svg, 64, 246, 130, 32, "water/Cu/Alloy", C["white"], C["axis"], C["ink2"], size=13.5, mono=True)

    # Arrow 1->2
    svg.line(210, 222, 238, 222, stroke=C["slate"], sw=2.2, marker_end="arr")

    # Stage 2: Neighbor List & Descriptor (Memory-Bound)
    svg.rect(242, 148, 228, 148, fill=C["surface_coral"], stroke=C["coral"], sw=2.0, rx=8)
    svg.rect(242, 148, 228, 30, fill=C["coral"], rx=6)
    svg.rect(242, 170, 228, 8, fill=C["coral"])
    svg.text(356, 169, "Memory-Bound Hotspot", size=14.5, color=C["white"], weight="bold", anchor="middle")
    svg.text(356, 204, "2. Neighbor & Descriptor", size=15.5, color=C["ink"], weight="bold", anchor="middle")
    svg.multiline(
        356,
        230,
        ["Env matrix R_i & cutoff s(r)", "Irregular gather & random reads", "Small-kernel & Python overhead"],
        size=13.8,
        color=C["ink2"],
        anchor="middle",
        lh=21,
    )

    # Arrow 2->3
    svg.line(470, 222, 498, 222, stroke=C["coral"], sw=2.2, marker_end="arr_coral")

    # Stage 3: Embedding & Fitting MLP (Compute-Bound)
    svg.rect(502, 148, 218, 148, fill=C["surface_teal"], stroke=C["teal"], sw=2.0, rx=8)
    svg.rect(502, 148, 218, 30, fill=C["teal"], rx=6)
    svg.rect(502, 170, 218, 8, fill=C["teal"])
    svg.text(611, 169, "Compute-Bound Core", size=14.5, color=C["white"], weight="bold", anchor="middle")
    svg.text(611, 204, "3. Embed & Fitting MLP", size=15.5, color=C["ink"], weight="bold", anchor="middle")
    svg.multiline(
        611,
        230,
        ["Embedding Net (local sym.)", "Fitting Net (residual MLP)", "Batched dense GEMM kernels"],
        size=13.8,
        color=C["ink2"],
        anchor="middle",
        lh=21,
    )

    # Arrow 3->4
    svg.line(720, 222, 748, 222, stroke=C["teal"], sw=2.2, marker_end="arr_teal")

    # Stage 4: Energy & Forces
    svg.rect(752, 148, 162, 148, fill=C["surface_blue"], stroke=C["blue"], sw=1.6, rx=8)
    svg.text(833, 176, "4. Energy & Forces", size=15.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(833, 206, "E = Σ E_i", size=15.5, color=C["ink"], weight="bold", anchor="middle", mono=True)
    svg.text(833, 236, "F_i = -∇_ri E", size=15.0, color=C["blue"], weight="bold", anchor="middle", mono=True)
    svg.text(833, 266, "Autodiff backward pass", size=13.5, color=C["muted"], anchor="middle")
    svg.text(833, 286, "+ Virial stress tensor", size=13.5, color=C["muted"], anchor="middle")

    # Precision note strip inside top panel
    svg.rect(48, 314, 866, 36, fill=C["surface_gold"], stroke=C["gold"], sw=1.2, rx=6)
    svg.text(
        481,
        338,
        "Allowed knobs only: descriptor/precision, fitting_net/precision, type_one_side (other hyperparams locked)",
        size=14.2,
        color=C["ink"],
        weight="bold",
        anchor="middle",
    )

    # Bottom Left: Optimization Callout (Tabulation + Kernel Fusion)
    svg.panel_box(28, 386, 520, 244, "Core Optimizations: Tabulation & Kernel Fusion", accent=C["teal"])

    svg.rect(48, 438, 232, 172, fill=C["surface_teal"], stroke=C["teal"], sw=1.4, rx=6)
    svg.text(64, 466, "Model Tabulation", size=15.8, color=C["teal"], weight="bold")
    svg.multiline(
        64,
        494,
        [
            "• Discretize Embedding Net",
            "• 5th-order spline lookup tables",
            "• Cuts descriptor FLOPs & I/O",
            "• Fits frequent local env calls",
        ],
        size=13.8,
        color=C["ink2"],
        lh=26,
    )

    svg.rect(296, 438, 232, 172, fill=C["surface_blue"], stroke=C["blue"], sw=1.4, rx=6)
    svg.text(312, 466, "Kernel Fusion & Precision", size=15.5, color=C["blue"], weight="bold")
    svg.multiline(
        312,
        494,
        [
            "• Fuse neighbor, s(r), & gather",
            "• Reduce intermediate HBM I/O",
            "• Mixed precision on key layers",
            "• Pair with type_one_side flag",
        ],
        size=13.8,
        color=C["ink2"],
        lh=26,
    )

    # Bottom Right: Verification Gate (`dp test`)
    svg.panel_box(568, 386, 364, 244, "Accuracy Gate: dp test", accent=C["coral"])
    svg.rect(588, 438, 324, 52, fill=C["ink"], rx=6)
    svg.text(750, 461, "dp test -m frozen_model.pb", size=14.5, color=C["white"], weight="bold", anchor="middle", mono=True)
    svg.text(750, 481, "-s data_system", size=14.5, color="#93C5FD", anchor="middle", mono=True)

    svg.multiline(
        588,
        518,
        [
            "• Must match official branch outputs",
            "• Covers water, Cu, and Al-Cu-Mg",
            "• Check energy & forces, not loss alone",
            "• Guard against low-precision drift",
        ],
        size=14.0,
        color=C["ink2"],
        lh=26,
    )

    return svg.save_and_render("c02_asc22_deepmd", png_width=1800)


# ---------------------------------------------------------------------------
# C03: ASC24 GoMars Mars Global Atmospheric Model
# ---------------------------------------------------------------------------
def make_c03() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC24 GoMars Atmospheric Model: Polar Bottleneck & MPI",
        "Non-hydrostatic lat-lon dycore · Historical 3 kW baseline · SJTU Application Innovation",
        accent=C["coral"],
    )

    # Left Panel: Sphere / Lat-Lon Grid showing polar meridian crowding
    svg.panel_box(28, 92, 436, 536, "Polar Meridian Convergence & CFL Limit", accent=C["coral"])

    cx, cy, R = 246.0, 294.0, 132.0
    # Sphere base
    svg.circle(cx, cy, R, fill=C["surface_coral"], stroke=C["coral"], sw=2.0)
    # Latitude circles (projected)
    for lat_deg in [-65, -40, -15, 0, 15, 40, 65]:
        lat = math.radians(lat_deg)
        y_lat = cy - R * math.sin(lat)
        rx_lat = R * math.cos(lat)
        ry_lat = rx_lat * 0.22
        col = C["coral"] if abs(lat_deg) >= 60 else C["axis"]
        sw = 1.8 if abs(lat_deg) >= 60 else 1.1
        svg.ellipse(cx, y_lat, rx_lat, ry_lat, fill="none", stroke=col, sw=sw)

    # Longitude meridians converging at North & South poles
    for lon_deg in range(-75, 90, 15):
        lon = math.radians(lon_deg)
        pts = []
        for lat_deg in range(-90, 95, 5):
            lat = math.radians(lat_deg)
            px = cx + R * math.cos(lat) * math.sin(lon)
            py = cy - R * math.sin(lat)
            pts.append((px, py))
        svg.polyline(pts, stroke=C["blue"], sw=1.15)

    # Highlight North & South pole singularity zones
    svg.circle(cx, cy - R + 12, 22, fill=C["coral"], opacity=0.22)
    svg.circle(cx, cy - R + 12, 22, fill="none", stroke=C["coral"], sw=2.0)
    svg.circle(cx, cy + R - 12, 22, fill=C["coral"], opacity=0.22)
    svg.circle(cx, cy + R - 12, 22, fill="none", stroke=C["coral"], sw=2.0)

    # Callouts on sphere
    svg.line(cx + 22, cy - R + 12, cx + 110, cy - R - 2, stroke=C["coral"], sw=1.6)
    svg.text(cx + 114, cy - R - 4, "North pole", size=14.5, color=C["coral"], weight="bold")
    svg.text(cx + 114, cy - R + 16, "Δx → 0", size=14.5, color=C["coral"], weight="bold")

    svg.line(cx + 22, cy + R - 12, cx + 110, cy + R + 4, stroke=C["coral"], sw=1.6)
    svg.text(cx + 114, cy + R + 2, "South pole", size=14.5, color=C["coral"], weight="bold")
    svg.text(cx + 114, cy + R + 20, "dense cells", size=13.5, color=C["coral"])

    svg.line(cx - R - 2, cy, cx - R - 34, cy, stroke=C["blue"], sw=1.5)
    svg.text(42, cy - 6, "Wide cells", size=14.0, color=C["blue"], weight="bold")
    svg.text(42, cy + 14, "max Δx", size=13.5, color=C["muted"])

    # CFL & Load imbalance formula box at bottom of left panel
    svg.rect(48, 456, 396, 152, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(64, 482, "Dual Physical & Parallel Bottleneck", size=15.5, color=C["coral"], weight="bold")
    svg.text(64, 510, "CFL: Δt ≤ C_max · Δx_min / c_max", size=14.5, color=C["ink"], weight="bold", mono=True)
    svg.multiline(
        64,
        538,
        [
            "• Converging poles shrink Δx, forcing tiny Δt / filters",
            "• Uniform splits overload polar ranks, idling equator",
            "• Idle tail caps strong scaling via Amdahl's law",
        ],
        size=13.8,
        color=C["ink2"],
        lh=24,
    )

    # Right Panel: MPI 2D Domain Decomposition & Halo Exchange
    svg.panel_box(484, 92, 448, 536, "MPI 2D Decomposition & Halo Exchange", accent=C["teal"])

    # 2D non-uniform latitude-weighted decomposition grid
    svg.text(504, 152, "Latitude-Weighted 2D Split (Coarse Polar Ranks)", size=14.8, color=C["ink"], weight="bold")
    gx, gy, gw, gh = 514.0, 168.0, 388.0, 206.0
    # Non-uniform latitude bands: polar bands narrower in lon split or tuned rows
    row_y = [gy, gy + 36, gy + 82, gy + 128, gy + 170, gy + gh]
    col_x = [gx, gx + 97, gx + 194, gx + 291, gx + gw]

    for r in range(5):
        is_polar = r in (0, 4)
        n_cols = 2 if is_polar else 4
        step_w = gw / n_cols
        for c in range(n_cols):
            rx0 = gx + c * step_w
            ry0 = row_y[r]
            rw = step_w
            rh = row_y[r + 1] - row_y[r]
            fill = C["surface_gold"] if is_polar else (C["surface_teal"] if (r == 2 and c == 1) else C["surface_blue"])
            stroke = C["gold"] if is_polar else (C["teal"] if (r == 2 and c == 1) else C["blue"])
            svg.rect(rx0 + 2, ry0 + 2, rw - 4, rh - 4, fill=fill, stroke=stroke, sw=1.4, rx=4)
            lbl = f"Polar R{r*2+c}" if is_polar else f"R({r},{c})"
            svg.text(rx0 + rw / 2, ry0 + rh / 2 + 5, lbl, size=13.5, color=C["ink"], weight="bold" if (r == 2 and c == 1) else "normal", anchor="middle", mono=True)

    # Halo exchange arrows around highlighted center rank (r=2, c=1)
    hx = gx + 97 + 97 / 2
    hy = (row_y[2] + row_y[3]) / 2
    svg.line(hx, row_y[2] + 6, hx, row_y[2] - 12, stroke=C["coral"], sw=2.0, marker_end="arr_coral")
    svg.line(hx, row_y[3] - 6, hx, row_y[3] + 12, stroke=C["coral"], sw=2.0, marker_end="arr_coral")
    svg.line(gx + 101, hy, gx + 85, hy, stroke=C["coral"], sw=2.0, marker_end="arr_coral")
    svg.line(gx + 190, hy, gx + 206, hy, stroke=C["coral"], sw=2.0, marker_end="arr_coral")

    # Legend under grid
    svg.rect(514, 384, 16, 14, fill=C["surface_gold"], stroke=C["gold"], sw=1.2, rx=2)
    svg.text(536, 396, "Merged polar tiles (fewer α)", size=13.5, color=C["ink2"])
    svg.rect(732, 384, 16, 14, fill=C["surface_teal"], stroke=C["teal"], sw=1.2, rx=2)
    svg.text(754, 396, "Non-blocking halo", size=13.5, color=C["ink2"])

    # Load Balance Before vs After Gantt bars
    svg.rect(504, 414, 408, 194, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(520, 440, "Step Timeline: Uniform vs Load-Balanced", size=15.0, color=C["ink"], weight="bold")

    # Before: Polar slow, Equator waiting
    svg.text(520, 468, "Uniform Partition", size=14.0, color=C["coral"], weight="bold")
    svg.text(520, 492, "Polar rank", size=13.5, color=C["muted"])
    draw_hbar(svg, 608, 478, 272, 18, C["coral"])
    svg.text(520, 518, "Eq. rank", size=13.5, color=C["muted"])
    draw_hbar(svg, 608, 504, 144, 18, C["blue"])
    draw_hbar(svg, 754, 504, 126, 18, C["surface_coral"], stroke=C["coral"])
    svg.text(817, 517, "Barrier wait", size=13.0, color=C["coral"], weight="bold", anchor="middle")

    # After: Balanced + overlap
    svg.text(520, 548, "Weighted 2D + Irecv/Isend Overlap", size=14.0, color=C["teal"], weight="bold")
    svg.text(520, 572, "Balanced", size=13.5, color=C["muted"])
    draw_hbar(svg, 608, 558, 162, 18, C["teal"])
    draw_hbar(svg, 772, 558, 22, 18, C["gold"])
    svg.text(802, 572, "Aligned sync", size=13.5, color=C["teal"], weight="bold")

    svg.text(520, 598, "Note: WannierTools 3× is a separate case, not GoMars.", size=13.0, color=C["muted"])

    return svg.save_and_render("c03_asc24_gomars", png_width=1800)


# ---------------------------------------------------------------------------
# C04: ASC25 AlphaFold3
# ---------------------------------------------------------------------------
def make_c04() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC25 AlphaFold3: Inference Pipeline & CPU-Only Tuning",
        "Prelim CPU/GPU (≥16-bit BF16) → Finals CPU-only 4 kW (≥3 nodes, ≤2 kW/node, dual Xeon 6760P)",
        accent=C["violet"],
    )

    # Top Panel: Pipeline
    svg.panel_box(28, 92, 904, 218, "AlphaFold3 Core Inference Pipeline (Pairformer O(N³) Hotspot)", accent=C["violet"])

    svg.node_box(48, 146, 152, 82, "Input Features", "Seq / MSA / Templates", fill=C["surface"], stroke=C["slate"], bar_color=C["slate"])
    svg.line(200, 187, 224, 187, stroke=C["slate"], sw=2.0, marker_end="arr")

    svg.node_box(228, 146, 154, 82, "MSA Module", "Row / col attention", fill=C["surface_blue"], stroke=C["blue"], bar_color=C["blue"])
    svg.line(382, 187, 406, 187, stroke=C["blue"], sw=2.0, marker_end="arr_blue")

    # Highlighted Pairformer O(N^3)
    svg.rect(410, 138, 280, 98, fill=C["surface_coral"], stroke=C["coral"], sw=2.2, rx=8)
    svg.text(550, 162, "Pairformer (48 Blocks)", size=16.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(550, 184, "Triangle Mult + Triangle Attention", size=14.5, color=C["ink"], weight="bold", anchor="middle")
    pill(svg, 450, 200, 200, 28, "O(N³) Compute Bottleneck", C["coral"], C["coral"], C["white"], size=13.5)

    svg.line(690, 187, 714, 187, stroke=C["coral"], sw=2.0, marker_end="arr_coral")

    svg.node_box(718, 146, 194, 82, "Diffusion Module", "All-atom 3D denoising", fill=C["surface_teal"], stroke=C["teal"], bar_color=C["teal"])

    # Bottom strip of pipeline
    svg.rect(48, 250, 864, 44, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(
        480,
        277,
        "N×N×C pair tensors dominate long sequences; BF16 has 7-bit mantissa, requiring FP32 accumulation",
        size=14.2,
        color=C["ink2"],
        anchor="middle",
    )

    # Bottom Left: Prelim vs Finals Rule Contrast Card
    svg.panel_box(28, 330, 412, 300, "Prelim vs Finals Platform Shift", accent=C["blue"])

    svg.rect(48, 382, 372, 102, fill=C["surface_blue"], stroke=C["blue"], sw=1.4, rx=6)
    svg.text(64, 408, "Preliminary Round", size=16.0, color=C["blue"], weight="bold")
    svg.multiline(
        64,
        434,
        [
            "• CPU or GPU platforms allowed",
            "• Weight & compute precision ≥ 16-bit (BF16)",
        ],
        size=14.2,
        color=C["ink2"],
        lh=26,
    )

    # Transition arrow
    svg.line(234, 486, 234, 512, stroke=C["coral"], sw=2.4, marker_end="arr_coral")
    svg.text(248, 504, "GPUs disallowed in finals", size=14.0, color=C["coral"], weight="bold")

    svg.rect(48, 516, 372, 98, fill=C["surface_coral"], stroke=C["coral"], sw=1.6, rx=6)
    svg.text(64, 542, "Finals (Historical Baseline)", size=16.0, color=C["coral"], weight="bold")
    svg.multiline(
        64,
        568,
        [
            "• Mandatory CPU-only (dual Xeon 6760P)",
            "• Total ≤ 4 kW · ≥ 3 nodes · ≤ 2 kW/node",
        ],
        size=14.2,
        color=C["ink2"],
        lh=26,
    )

    # Bottom Right: SJTU 30x+ CPU Speedup Breakdown
    svg.panel_box(460, 330, 472, 300, "SJTU 30×+ CPU Inference Breakdown", accent=C["teal"])

    # Big metric highlight
    svg.rect(480, 380, 432, 54, fill=C["surface_teal"], stroke=C["teal"], sw=1.6, rx=6)
    svg.text(500, 414, "30×+", size=26, color=C["teal"], weight="bold", mono=True)
    svg.text(586, 404, "End-to-End CPU Inference Speedup", size=15.5, color=C["ink"], weight="bold")
    svg.text(586, 424, "Source: ASC26 overview talk retrospective", size=13.5, color=C["muted"])

    pillars = [
        (
            "1. AMX BF16 + Native oneDNN",
            "Enable Xeon 6760P AMX tiles over scalar/AVX paths",
            C["blue"],
            C["surface_blue"],
        ),
        (
            "2. Kernel & Tensor Layout Fusion",
            "Cut transposes and writebacks across Pairformer ops",
            C["violet"],
            C["surface_violet"],
        ),
        (
            "3. NUMA Pinning & Multi-Node Scheduling",
            "Balance samples across ≥3 nodes; curb cross-socket traffic",
            C["gold"],
            C["surface_gold"],
        ),
    ]
    for idx, (pt, pd, col, bg) in enumerate(pillars):
        py0 = 448 + idx * 56
        svg.rect(480, py0, 432, 48, fill=bg, stroke=col, sw=1.2, rx=6)
        svg.rect(480, py0, 5, 48, fill=col, rx=2)
        svg.text(496, py0 + 20, pt, size=15, color=col, weight="bold")
        svg.text(496, py0 + 40, pd, size=13.8, color=C["ink2"])

    return svg.save_and_render("c04_asc25_alphafold3", png_width=1800)


# ---------------------------------------------------------------------------
# C05: ASC25 DeepSeek R1-Distill 32B CPU-only
# ---------------------------------------------------------------------------
def make_c05() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC25 DeepSeek R1-Distill 32B: CPU Bandwidth Ceiling",
        "CPU-only · Historical 4 kW cap · ≥4-bit quant allowed · No pruning or cross-run KV reuse",
        accent=C["blue"],
    )

    # Left Panel: Weight Footprint Bar Chart
    svg.panel_box(28, 92, 434, 416, "32B Weight Footprint (GB)", accent=C["blue"])

    pb1 = PlotBox(svg, 98, 156, 336, 294, xmin=0, xmax=3, ymin=0, ymax=75)
    pb1.draw_axes(
        xticks=[],
        yticks=[(0, "0"), (16, "16"), (32, "32"), (48, "48"), (64, "64")],
        ylabel="Weight Footprint (GB)",
    )

    precisions = [
        ("BF16", "16-bit", 64.0, C["coral"]),
        ("INT8", "8-bit", 32.0, C["gold"]),
        ("INT4", "4-bit", 16.0, C["teal"]),
    ]
    bar_w = 64.0
    for i, (name, sub, val, col) in enumerate(precisions):
        cx = pb1.px(i + 0.5)
        y_top = pb1.py(val)
        y_bot = pb1.py(0)
        svg.rect(cx - bar_w / 2, y_top, bar_w, y_bot - y_top, fill=col, rx=5)
        svg.text(cx, y_top - 10, f"{int(val)} GB", size=16.5, color=col, weight="bold", anchor="middle", mono=True)
        svg.text(cx, y_bot + 22, name, size=15.5, color=C["ink"], weight="bold", anchor="middle")
        svg.text(cx, y_bot + 41, sub, size=13.5, color=C["muted"], anchor="middle")

    # Ratio arrow BF16 -> INT4
    svg.path(
        f"M {pb1.px(0.5) + 34:.1f} {pb1.py(64) + 12:.1f} Q {pb1.px(1.6):.1f} {pb1.py(68):.1f} {pb1.px(2.5) - 6:.1f} {pb1.py(28):.1f}",
        stroke=C["teal"],
        sw=2.0,
        dash="5,4",
        marker_end="arr_teal",
    )
    svg.text(pb1.px(1.85), pb1.py(54), "4× less I/O", size=15, color=C["teal"], weight="bold", anchor="middle")

    # Right Panel: Theoretical DDR5 Decode Ceiling + ZJU 14.9 tok/s
    svg.panel_box(482, 92, 450, 416, "Decode Ceiling (Dual DDR5 = 400 GB/s)", accent=C["teal"])

    pb2 = PlotBox(svg, 554, 156, 352, 294, xmin=0, xmax=3, ymin=0, ymax=30)
    pb2.draw_axes(
        xticks=[],
        yticks=[(0, "0"), (5, "5"), (10, "10"), (15, "15"), (20, "20"), (25, "25"), (30, "30")],
        ylabel="Throughput Ceiling (tok/s)",
    )

    ceilings = [
        ("BF16", 6.25, "6.2", C["coral"]),
        ("INT8", 12.5, "12.5", C["gold"]),
        ("INT4", 25.0, "25.0", C["teal"]),
    ]
    for i, (name, val, lbl, col) in enumerate(ceilings):
        cx = pb2.px(i + 0.5)
        y_top = pb2.py(val)
        y_bot = pb2.py(0)
        svg.rect(cx - bar_w / 2, y_top, bar_w, y_bot - y_top, fill=col, rx=5)
        if name == "INT8":
            svg.text(cx, y_top + 20, "12.5", size=15.5, color=C["white"], weight="bold", anchor="middle", mono=True)
            svg.text(cx, y_top + 38, "tok/s", size=13.5, color=C["white"], weight="bold", anchor="middle", mono=True)
        else:
            svg.text(cx, y_top - 10, f"{lbl} tok/s", size=15.5, color=col, weight="bold", anchor="middle", mono=True)
        svg.text(cx, y_bot + 22, name, size=15.5, color=C["ink"], weight="bold", anchor="middle")
        svg.text(cx, y_bot + 41, "400 / GB", size=13.5, color=C["muted"], anchor="middle", mono=True)

    # ZJU 14.9 tok/s horizontal reference line & callout
    y_zju = pb2.py(14.9)
    svg.line(pb2.x, y_zju, pb2.x + pb2.w, y_zju, stroke=C["violet"], sw=2.4, dash="7,4")
    svg.circle(pb2.px(2.62), y_zju, 6.0, fill=C["violet"], stroke=C["white"], sw=2.0)
    svg.rect(pb2.x + 6, pb2.y + 6, 214, 38, fill=C["surface_violet"], stroke=C["violet"], sw=1.4, rx=6)
    svg.text(pb2.x + 16, pb2.y + 22, "ZJU measured: 14.9 tok/s", size=14.2, color=C["violet"], weight="bold")
    svg.text(pb2.x + 16, pb2.y + 38, "Single-stream (~60% INT4 BW)", size=12.6, color=C["ink2"])

    # Bottom summary banner (Rules + Formula)
    svg.rect(28, 526, 904, 106, fill=C["white"], stroke=C["grid"], sw=1.4, rx=8)
    svg.rect(28, 526, 6, 106, fill=C["blue"], rx=2)

    svg.text(50, 554, "Decode BW bound: tok/s ≤ B_DDR5 / (Bytes_weights + Bytes_KV)", size=15.5, color=C["blue"], weight="bold", mono=True)
    svg.text(50, 581, "Each generated token streams all weights + KV cache; low arithmetic intensity pins CPU decode to DRAM BW.", size=14.2, color=C["ink2"])

    pill(svg, 50, 594, 192, 28, "✓ ≥4-bit quant allowed", C["surface_teal"], C["teal"], C["teal"], size=13.5)
    pill(svg, 254, 594, 184, 28, "✕ No model pruning", C["surface_coral"], C["coral"], C["coral"], size=13.5)
    pill(svg, 450, 594, 228, 28, "✕ No cross-run KV reuse", C["surface_coral"], C["coral"], C["coral"], size=13.5)
    pill(svg, 690, 594, 222, 28, "Baseline: CPU-only 4 kW", C["surface_gold"], C["gold"], C["gold"], size=13.5)

    return svg.save_and_render("c05_asc25_deepseek_r1", png_width=1800)


# ---------------------------------------------------------------------------
# C06: ASC26 UnifoLM-WMA-0 Embodied World Model
# ---------------------------------------------------------------------------
def make_c06() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC26 UnifoLM-WMA-0 World Model: Pipeline & Speedups",
        "Prelim 20 cases (≥16-bit, PSNR≥25) → Finals 6 cases (5 kW, open precision & sampler, PSNR≥25)",
        accent=C["violet"],
    )

    # Top Panel: Pipeline
    svg.panel_box(28, 92, 904, 178, "Diffusion Video World-Model Inference Pipeline", accent=C["violet"])

    svg.node_box(48, 146, 176, 74, "Action + History", "Robot pose & frames", fill=C["surface"], stroke=C["slate"], bar_color=C["slate"])
    svg.line(224, 183, 252, 183, stroke=C["slate"], sw=2.0, marker_end="arr")

    svg.rect(256, 138, 306, 90, fill=C["surface_violet"], stroke=C["violet"], sw=2.0, rx=8)
    svg.text(409, 166, "Spatial / Temporal UNet Diffusion", size=16, color=C["violet"], weight="bold", anchor="middle")
    svg.text(409, 191, "Multi-step denoising (GroupNorm / GEGLU / GEMM)", size=13.2, color=C["ink2"], anchor="middle")
    svg.text(409, 214, "Stack: TensorRT + TeaCache + ParaStep", size=13.5, color=C["blue"], weight="bold", anchor="middle")

    svg.line(562, 183, 590, 183, stroke=C["violet"], sw=2.0, marker_end="arr_violet")

    svg.node_box(594, 146, 152, 74, "Predicted Video", "Future rollout", fill=C["surface_blue"], stroke=C["blue"], bar_color=C["blue"])
    svg.line(746, 183, 774, 183, stroke=C["blue"], sw=2.0, marker_end="arr_blue")

    svg.rect(778, 146, 136, 74, fill=C["surface_coral"], stroke=C["coral"], sw=2.0, rx=8)
    svg.text(846, 173, "Quality Gate", size=15.0, color=C["coral"], weight="bold", anchor="middle")
    svg.text(846, 196, "PSNR ≥ 25 dB", size=15.0, color=C["ink"], weight="bold", anchor="middle", mono=True)
    svg.text(846, 213, "Fail any case → 0", size=12.2, color=C["coral"], anchor="middle")

    svg.text(48, 254, "Opening precision, sampler, and step count in finals lets teams cut both step count and per-step latency while keeping PSNR ≥ 25.", size=13.6, color=C["muted"])

    # Bottom Panel: Verified ASC26 Speedup Horizontal Bar Chart
    svg.panel_box(28, 290, 904, 342, "Verified ASC26 Speedups vs Official Baseline (~780 s/case)", accent=C["teal"])

    # Horizontal bars: Speedup ratio (1x to 30x)
    rows = [
        ("Official Baseline", "~780 s/case reference", 1.0, "1.0×", C["axis"]),
        ("Prelim · QLU (1 GPU)", "Fused kernels + NHWC (8MN→4MN)", 5.41, "5.41×", C["blue_l"]),
        ("Prelim · QLU (Multi-GPU)", "Persistent service + multi-GPU", 8.13, "8.13×", C["blue"]),
        ("Prelim · SHU (2 GPUs)", "TRT+TeaCache+ParaStep · 36.9 dB", 8.22, "8.22×", C["violet"]),
        ("Finals · BUPT", "~30 s/case (open prec/steps)", 26.0, ">20× (~30s)", C["gold"]),
        ("Finals · PKU", "~26 s/case (open prec/steps)", 30.0, ">20× (~26s)", C["teal"]),
    ]

    x_bar0 = 312.0
    max_bar_w = 468.0
    max_val = 32.0
    y_start = 344.0
    row_h = 44.0

    # Gridlines for 0x, 5x, 10x, 20x, 30x
    for tick in [0, 5, 10, 15, 20, 25, 30]:
        tx = x_bar0 + (tick / max_val) * max_bar_w
        svg.line(tx, y_start - 8, tx, y_start + len(rows) * row_h - 8, stroke=C["grid"], sw=1.0)
        svg.text(tx, y_start + len(rows) * row_h + 12, f"{tick}×", size=13.5, color=C["muted"], anchor="middle", mono=True)

    for i, (label, detail, val, badge, col) in enumerate(rows):
        ry = y_start + i * row_h
        svg.text(x_bar0 - 12, ry + 14, label, size=14.8, color=C["ink"], weight="bold", anchor="end")
        svg.text(x_bar0 - 12, ry + 32, detail, size=12.6, color=C["muted"], anchor="end")
        bw = max((val / max_val) * max_bar_w, 10.0)
        draw_hbar(svg, x_bar0, ry + 5, bw, 24, col, rx=4)
        svg.text(x_bar0 + bw + 10, ry + 22, badge, size=15, color=col if col != C["axis"] else C["slate"], weight="bold", mono=True)

    # Separator dashed line between Prelim and Finals
    y_sep = y_start + 4 * row_h - 6
    svg.line(48, y_sep, 912, y_sep, stroke=C["gold"], sw=1.4, dash="6,4")
    svg.text(906, y_sep - 5, "▲ Prelim (≥16-bit locked)   ▼ Finals (5 kW · open precision/sampler)", size=13.0, color=C["gold"], weight="bold", anchor="end")

    return svg.save_and_render("c06_asc26_unifolm_wma", png_width=1800)


# ---------------------------------------------------------------------------
# C07: ASC26 AMSS-NCKU Numerical Relativity
# ---------------------------------------------------------------------------
def make_c07() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC26 AMSS-NCKU Numerical Relativity: AMR & Speedups",
        "Binary black hole merger (GW150914) · Gates: trajectory RMS < 1%, ADM < 2 · Finals 5 kW",
        accent=C["blue"],
    )

    # Left Panel: Concentric 9-level nested AMR grid + wave extraction sphere
    svg.panel_box(28, 92, 434, 536, "9-Level Nested AMR Grid & Wave Sphere", accent=C["blue"])

    cx, cy = 245.0, 312.0

    # Outer gravitational wave extraction sphere (r=168)
    svg.circle(cx, cy, 168, fill=C["surface_violet"], stroke=C["violet"], sw=2.0, opacity=0.45)
    svg.circle(cx, cy, 168, fill="none", stroke=C["violet"], sw=2.0)
    # Dashed ripple arcs for GW150914 radiation
    svg.circle(cx, cy, 146, fill="none", stroke=C["violet"], sw=1.2, opacity=0.55)

    # Concentric AMR levels (showing L0 -> L4 -> L6 -> L8 moving boxes)
    amr_boxes = [
        (244, C["surface"], C["axis"], "L0 coarse (Δt)"),
        (182, C["surface_blue"], C["blue_l"], "L3 (8×)"),
        (124, "#DBEAFE", C["blue"], "L6 (16×)"),
    ]
    for side, fill, stroke, lbl in amr_boxes:
        svg.rect(cx - side / 2, cy - side / 2, side, side, fill=fill, stroke=stroke, sw=1.5, rx=3)
        svg.text(cx - side / 2 + 6, cy - side / 2 + 16, lbl, size=13, color=stroke, weight="bold", mono=True)

    # Level-8 finest moving boxes around the two black holes (32x subcycling)
    bh1 = (cx - 28, cy + 8)
    bh2 = (cx + 28, cy - 8)
    # Orbit dashed ellipse
    svg.ellipse(cx, cy, 34, 18, fill="none", stroke=C["coral"], sw=1.5, dash="4,3")

    for bx, by in [bh1, bh2]:
        svg.rect(bx - 24, by - 24, 48, 48, fill=C["surface_coral"], stroke=C["coral"], sw=1.8, rx=2)
        # Sub-grid lines inside L8
        svg.line(bx - 8, by - 24, bx - 8, by + 24, stroke=C["coral"], sw=0.7)
        svg.line(bx + 8, by - 24, bx + 8, by + 24, stroke=C["coral"], sw=0.7)
        svg.line(bx - 24, by - 8, bx + 24, by - 8, stroke=C["coral"], sw=0.7)
        svg.line(bx - 24, by + 8, bx + 24, by + 8, stroke=C["coral"], sw=0.7)
        svg.circle(bx, by, 7.5, fill=C["ink"])

    # Callouts on AMR diagram
    svg.text(cx, cy - 176, "Outer GW extraction sphere Ψ₄ (GW150914)", size=14.2, color=C["violet"], weight="bold", anchor="middle")
    svg.line(bh2[0] + 24, bh2[1] - 20, cx + 106, cy - 92, stroke=C["coral"], sw=1.5)
    svg.text(cx + 110, cy - 96, "L8 finest", size=14.2, color=C["coral"], weight="bold")
    svg.text(cx + 110, cy - 78, "32× subcycle", size=12.8, color=C["coral"], mono=True)

    # Bottom summary inside Left Panel
    svg.rect(48, 498, 394, 112, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.multiline(
        64,
        522,
        [
            "• 24 vars/cell; RK4 runs four 3D stencil RHS/step",
            "• Fine subcycling + inter-level interp & halo comms",
            "• Finals cases: GW150914, triple BH, full merger",
            "• Physics gates: RMS < 1%, ADM < 2 (math equiv.)",
        ],
        size=13.6,
        color=C["ink2"],
        lh=24,
    )

    # Right Panel: Verified ASC26 Team Achievements
    svg.panel_box(482, 92, 450, 536, "Verified ASC26 Team Speedups (By Source)", accent=C["teal"])

    # Card 1: ZJU (Prelim 18.6x -> Finals 30x)
    svg.rect(502, 144, 410, 142, fill=C["surface_teal"], stroke=C["teal"], sw=1.6, rx=8)
    svg.text(518, 170, "Zhejiang Univ. (ZJU · ASC26 Talk)", size=15.5, color=C["teal"], weight="bold")
    svg.text(518, 194, "Full-kernel GPU offload + register/SMEM tuning", size=13.8, color=C["ink2"])

    # Visual bar pair for ZJU
    svg.text(518, 222, "Prelim 44,425→2,376s", size=13.2, color=C["ink"], mono=True)
    draw_hbar(svg, 718, 208, 114, 18, C["blue_l"])
    svg.text(840, 222, "18.6×", size=15.5, color=C["blue"], weight="bold", mono=True)

    svg.text(518, 254, "Finals peak end-to-end", size=13.8, color=C["ink"], weight="bold")
    draw_hbar(svg, 718, 240, 178, 18, C["teal"])
    svg.text(896, 276, "Up to ~30×", size=15.0, color=C["teal"], weight="bold", anchor="end", mono=True)

    # Card 2: THU (4.5s -> 0.85s/step progression)
    svg.rect(502, 302, 410, 184, fill=C["surface_blue"], stroke=C["blue"], sw=1.6, rx=8)
    svg.text(518, 328, "Tsinghua (THU · Prep step-time progression)", size=14.8, color=C["blue"], weight="bold")

    thu_steps = [
        ("CPU baseline", 4.5, C["axis"]),
        ("Init GPU (122 H2D/D2H)", 4.7, C["coral"]),
        ("GPU-resident state", 1.4, C["gold"]),
        ("2c GPU + 62c analysis", 1.0, C["blue_l"]),
        ("3-stage pipeline", 0.85, C["teal"]),
    ]
    for idx, (st_lbl, sec, col) in enumerate(thu_steps):
        sy = 344 + idx * 27
        svg.text(672, sy + 15, st_lbl, size=13.2, color=C["ink2"], anchor="end")
        bw = (sec / 5.0) * 160.0
        draw_hbar(svg, 682, sy + 3, bw, 16, col, rx=3)
        svg.text(682 + bw + 8, sy + 16, f"{sec:.2f}s" if sec == 0.85 else f"{sec:.1f}s", size=13.6, color=col if col != C["axis"] else C["slate"], weight="bold", mono=True)

    # Card 3: PKU (5.50x + RMS 1.9e-9)
    svg.rect(502, 502, 410, 108, fill=C["surface_violet"], stroke=C["violet"], sw=1.6, rx=8)
    svg.text(518, 528, "Peking Univ. (PKU · ASC26 Talk Prelim)", size=15.5, color=C["violet"], weight="bold")
    svg.text(518, 556, "End-to-end 5.50× (TwoPunctures 64c OMP 5.46×)", size=13.8, color=C["ink"], weight="bold")
    pill(svg, 518, 568, 314, 30, "Verified trajectory RMS = 1.9 × 10⁻⁹", C["white"], C["violet"], C["violet"], size=13.6, mono=True)

    return svg.save_and_render("c07_asc26_amss_ncku", png_width=1800)


# ---------------------------------------------------------------------------
# C08: ASC26 QiboTN CPU-only Quantum Simulation
# ---------------------------------------------------------------------------
def make_c08() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC26 QiboTN Quantum Sim: State-Vector Wall vs Tensor Net",
        "CPU-only (GPU use → 0 pts) · Historical 5 kW baseline · Circuits: QFT / QAOA / Supremacy",
        accent=C["violet"],
    )

    # Main Semi-Log PlotBox: M(n) = 16 * 2^n Bytes for n in [10, 50]
    svg.panel_box(28, 92, 578, 536, "complex128 Exponential Wall: M(n) = 16 · 2ⁿ Bytes", accent=C["violet"])

    # y range: 10^4 (10 KiB) to 10^17 (100 PiB)
    pb = PlotBox(svg, 118, 154, 464, 344, xmin=10, xmax=52, ymin=1e4, ymax=1e17, xlog=False, ylog=True)
    pb.draw_axes(
        xticks=[(10, "10q"), (20, "20q"), (30, "30q"), (40, "40q"), (50, "50q")],
        yticks=[
            (16 * (2**10), "16 KiB"),
            (16 * (2**20), "16 MiB"),
            (16 * (2**30), "16 GiB"),
            (16 * (2**40), "16 TiB"),
            (16 * (2**50), "16 PiB"),
        ],
        xlabel="Number of Qubits (n)",
        ylabel="Memory Footprint (log scale)",
    )

    # Exact State-Vector curve: M(n) = 16 * 2^n
    ns = np.linspace(10, 50, 200)
    mem_sv = 16.0 * (2.0**ns)
    pb.plot_curve(ns, mem_sv, stroke=C["coral"], sw=3.2)

    # Tensor Network MPS scaling (bond dimension chi=64, 256): M_MPS(n) ≈ 16 * 2 * n * chi^2
    mem_mps64 = 16.0 * 2.0 * ns * (64.0**2)
    mem_mps256 = 16.0 * 2.0 * ns * (256.0**2)
    pb.plot_curve(ns, mem_mps256, stroke=C["teal"], sw=2.6, dash="8,5")
    pb.plot_curve(ns, mem_mps64, stroke=C["blue"], sw=2.6)

    # Reference line: Typical single-node server RAM ~ 1 TiB
    y_ram = pb.py(2**40)
    svg.line(pb.x, y_ram, pb.x + pb.w, y_ram, stroke=C["gold"], sw=1.6, dash="4,4")
    svg.text(pb.x + 8, y_ram - 7, "Single-node server DRAM (~1 TiB)", size=13.5, color=C["gold"], weight="bold")

    # Explicit verified milestone markers: 20q, 30q, 40q, 50q
    milestones = [
        (20, 16 * (2**20), "20q = 16 MiB", 16, 44, "start"),
        (30, 16 * (2**30), "30q = 16 GiB", -12, -14, "end"),
        (40, 16 * (2**40), "40q = 16 TiB", -12, -14, "end"),
        (50, 16 * (2**50), "50q = 16 PiB", -12, 6, "end"),
    ]
    for q, mval, lbl, dx, dy, anc in milestones:
        px, py = pb.px(q), pb.py(mval)
        svg.circle(px, py, 6.2, fill=C["coral"], stroke=C["white"], sw=2.0)
        if q == 20:
            svg.line(px + 4, py + 6, px + 14, py + 31, stroke=C["coral"], sw=1.4)
        svg.text(px + dx, py + dy, lbl, size=14.2, color=C["coral"], weight="bold", anchor=anc, mono=True)

    # Curve labels for MPS
    svg.text(pb.px(44), pb.py(16 * 2 * 44 * (256**2)) - 12, "MPS (χ=256)", size=14, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb.px(44), pb.py(16 * 2 * 44 * (64**2)) + 20, "MPS (χ=64): O(n·χ²)", size=14, color=C["blue"], weight="bold", anchor="middle")

    # Formula legend bar inside left panel bottom
    svg.rect(48, 560, 538, 50, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(62, 581, "State vector: 16 B/amp × 2ⁿ (every +10 qubits scales 1024×)", size=13.8, color=C["coral"], weight="bold")
    svg.text(62, 602, "Tensor network MPS: exploits low entanglement & treewidth", size=13.8, color=C["teal"], weight="bold")

    # Right Column: Two Callout Panels
    # Top Right: Unit Typo Correction Callout
    svg.panel_box(626, 92, 306, 268, "Erratum: Slide p.20 Unit Typo", accent=C["coral"])

    svg.rect(644, 144, 270, 92, fill=C["surface_coral"], stroke=C["coral"], sw=1.4, rx=6)
    svg.text(656, 168, "ASC26 slide p.20 typo (1024× off):", size=13.8, color=C["coral"], weight="bold")
    svg.text(656, 194, "✕ 20q printed as 16 GB", size=14.2, color=C["coral"], mono=True)
    svg.text(656, 220, "✕ 40q printed as 16 PB", size=14.2, color=C["coral"], mono=True)

    svg.rect(644, 248, 270, 96, fill=C["surface_teal"], stroke=C["teal"], sw=1.6, rx=6)
    svg.text(656, 272, "Exact complex128 math:", size=14.0, color=C["teal"], weight="bold")
    svg.text(656, 298, "✓ 20q = 16·2²⁰ = 16 MiB", size=14.2, color=C["ink"], weight="bold", mono=True)
    svg.text(656, 324, "✓ 40q = 16·2⁴⁰ = 16 TiB", size=14.2, color=C["ink"], weight="bold", mono=True)

    # Bottom Right: Fudan C-Rewrite Speedup & CPU-only Constraints
    svg.panel_box(626, 380, 306, 248, "Fudan CPU-Only Optimization", accent=C["blue"])

    svg.rect(644, 430, 270, 62, fill=C["surface_blue"], stroke=C["blue"], sw=1.4, rx=6)
    svg.text(779, 456, "Python → Native C Rewrite", size=15.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(779, 480, "Tens-of-× faster tensor contraction", size=13.5, color=C["ink2"], anchor="middle")

    svg.multiline(
        644,
        518,
        [
            "• Remove Python & dynamic allocs",
            "• Contiguous layout & cache reuse",
            "• Enable compiler SIMD vectorization",
            "• Verify via mean expectation value",
        ],
        size=13.8,
        color=C["ink2"],
        lh=26,
    )

    return svg.save_and_render("c08_asc26_qibotn", png_width=1800)


# ---------------------------------------------------------------------------
# C09: ASC26 Mystery LeWorldModel (JEPA)
# ---------------------------------------------------------------------------
def make_c09() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC26 Mystery App LeWorldModel (JEPA): >100× Speedup",
        "Mandatory AMD W7900D (ROCm) · Finals 5 kW · 200 PushT cases · Hard gate: success ≥ 90%",
        accent=C["blue"],
    )

    # Top Panel: JEPA Encoder-Predictor + CEM Latent Planning Loop
    svg.panel_box(28, 92, 904, 212, "JEPA Latent Predictor & CEM Planning Loop (No Pixel Decoding)", accent=C["blue"])

    svg.node_box(48, 146, 150, 74, "Observation o(t)", "Current PushT state", fill=C["surface"], stroke=C["slate"], bar_color=C["slate"])
    svg.line(198, 183, 224, 183, stroke=C["slate"], sw=2.0, marker_end="arr")

    svg.node_box(228, 146, 148, 74, "Encoder", "Map to latent s(t)", fill=C["surface_blue"], stroke=C["blue"], bar_color=C["blue"])
    svg.line(376, 183, 404, 183, stroke=C["blue"], sw=2.0, marker_end="arr_blue")

    svg.node_box(408, 146, 198, 74, "JEPA Predictor", "Rollout s(t+k) = f(s(t), a)", fill=C["surface_violet"], stroke=C["violet"], bar_color=C["violet"])
    svg.line(606, 183, 634, 183, stroke=C["violet"], sw=2.0, marker_end="arr_violet")

    svg.node_box(638, 146, 150, 74, "CEM Scorer", "Rank action samples", fill=C["surface_teal"], stroke=C["teal"], bar_color=C["teal"])
    svg.line(788, 183, 814, 183, stroke=C["teal"], sw=2.0, marker_end="arr_teal")

    svg.rect(818, 146, 94, 74, fill=C["surface_gold"], stroke=C["gold"], sw=1.8, rx=8)
    svg.text(865, 178, "Best Action", size=14.2, color=C["gold"], weight="bold", anchor="middle")
    svg.text(865, 200, "a* → step", size=14.0, color=C["ink"], weight="bold", anchor="middle", mono=True)

    # CEM feedback arc below Predictor & CEM
    svg.path(
        "M 713 220 L 713 254 L 507 254 L 507 224",
        stroke=C["teal"],
        sw=2.0,
        dash="6,4",
        marker_end="arr_teal",
    )
    svg.text(610, 274, "Iterative CEM sampling (hotspot: tiny forwards + launch overhead)", size=13.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(138, 266, "Cached goal s_goal", size=13.8, color=C["blue"], weight="bold", anchor="middle")
    svg.path("M 218 262 L 302 262 L 302 224", stroke=C["blue"], sw=1.6, dash="4,3", marker_end="arr_blue")

    # Bottom Left: Verified ASC26 Finals Benchmark Bar Chart (>100x speedup)
    svg.panel_box(28, 322, 434, 310, "ASC26 Finals Wall Time (200 Cases · All >100×)", accent=C["teal"])

    pb = PlotBox(svg, 98, 384, 338, 184, xmin=0, xmax=3, ymin=0, ymax=22)
    pb.draw_axes(
        xticks=[],
        yticks=[(0, "0s"), (5, "5s"), (10, "10s"), (15, "15s"), (20, "20s")],
        ylabel="Total Wall Time, 200 Cases (s)",
    )

    teams = [
        ("BUPT", 14.0, C["teal"]),
        ("THU", 16.0, C["blue"]),
        ("PKU", 17.0, C["violet"]),
    ]
    bw = 64.0
    for idx, (tname, sec, col) in enumerate(teams):
        cx = pb.px(idx + 0.5)
        y_top = pb.py(sec)
        y_bot = pb.py(0)
        svg.rect(cx - bw / 2, y_top, bw, y_bot - y_top, fill=col, rx=5)
        # 16 s sits under the 100× pill; tuck that one value inside the bar
        if sec >= 15.5:
            svg.text(cx, y_top + 22, f"{int(sec)} s", size=16, color=C["white"], weight="bold", anchor="middle", mono=True)
        else:
            svg.text(cx, y_top - 12, f"{int(sec)} s", size=17, color=col, weight="bold", anchor="middle", mono=True)
        svg.text(cx, y_bot + 24, tname, size=15, color=C["ink"], weight="bold", anchor="middle")

    # Speedup badge inside chart top-left
    pill(svg, 244, 394, 178, 26, "Top 3 all exceed 100×", C["surface_gold"], C["gold"], C["gold"], size=13.2)
    svg.text(245, 616, "All runs meet PushT success ≥ 90% (ASC26 overview talk)", size=13.2, color=C["muted"], anchor="middle")

    # Bottom Right: Key Optimization Techniques (by team & stack)
    svg.panel_box(482, 322, 450, 310, "Key Optimization Stack (ROCm Ecosystem)", accent=C["violet"])

    techs = [
        ("BF16 Mixed Precision & Feature Caching", "Cut latent forward latency; reuse static goal embeddings", C["blue"], C["surface_blue"]),
        ("HIP Graph Capture", "Eliminate dense ROCm kernel launch overhead in CEM loop", C["violet"], C["surface_violet"]),
        ("Early-Exit on Solved Episodes", "Mask completed PushT rollouts to skip wasted CEM steps", C["teal"], C["surface_teal"]),
        ("Async Video I/O & Multi-Node Pools", "Remove CPU-GPU sync stalls; NUMA pin + async encoding", C["gold"], C["surface_gold"]),
    ]
    for idx, (tt, td, col, bg) in enumerate(techs):
        ty = 374 + idx * 60
        svg.rect(500, ty, 414, 50, fill=bg, stroke=col, sw=1.3, rx=6)
        svg.rect(500, ty, 5, 50, fill=col, rx=2)
        svg.text(516, ty + 21, tt, size=14.8, color=col, weight="bold")
        svg.text(516, ty + 41, td, size=13.2, color=C["ink2"])

    return svg.save_and_render("c09_asc26_leworldmodel", png_width=1800)


# ---------------------------------------------------------------------------
# C10: ASC26 Group Competition ICON Climate Model
# ---------------------------------------------------------------------------
def make_c10() -> Path:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC26 Group Task ICON Climate Model: Mesh & Alliance",
        "CPU-only (GPU use → 0 pts) · Finals 5 kW · 8 pts group task · Shared patches, solo runs",
        accent=C["teal"],
    )

    # Left Panel: Lat-Lon vs ICON Icosahedral Mesh + 3 Test Cases
    svg.panel_box(28, 92, 446, 536, "Lat-Lon Grid vs ICON Icosahedral Mesh", accent=C["blue"])

    # Left mini-sphere: Lat-Lon (polar singularity)
    c1x, c1y, r_s = 136.0, 224.0, 74.0
    svg.circle(c1x, c1y, r_s, fill=C["surface_coral"], stroke=C["coral"], sw=1.8)
    for lat_d in [-55, -25, 0, 25, 55]:
        lat = math.radians(lat_d)
        yl = c1y - r_s * math.sin(lat)
        rxl = r_s * math.cos(lat)
        svg.ellipse(c1x, yl, rxl, rxl * 0.22, fill="none", stroke=C["axis"], sw=1.0)
    for lon_d in range(-60, 90, 30):
        lon = math.radians(lon_d)
        pts = [(c1x + r_s * math.cos(math.radians(a)) * math.sin(lon), c1y - r_s * math.sin(math.radians(a))) for a in range(-90, 95, 10)]
        svg.polyline(pts, stroke=C["coral"], sw=1.1)
    svg.circle(c1x, c1y - r_s + 8, 12, fill=C["coral"], opacity=0.3)
    svg.text(c1x, c1y + r_s + 24, "Classic Lat-Lon", size=14.8, color=C["coral"], weight="bold", anchor="middle")
    svg.text(c1x, c1y + r_s + 44, "Polar singularity & skew", size=13.2, color=C["muted"], anchor="middle")

    # VS arrow
    svg.line(218, c1y, 266, c1y, stroke=C["teal"], sw=2.4, marker_end="arr_teal")
    svg.text(242, c1y - 10, "vs", size=14.5, color=C["teal"], weight="bold", anchor="middle")

    # Right mini-sphere: ICON Icosahedral Geodesic Triangular Mesh
    c2x, c2y = 360.0, 224.0
    svg.circle(c2x, c2y, r_s, fill=C["surface_teal"], stroke=C["teal"], sw=1.8)
    # Draw neat projected triangular geodesic grid clipped naturally inside circle
    hex_pts = []
    for ring_r, count, phase in [(0.0, 1, 0.0), (0.44 * r_s, 6, 0.0), (0.86 * r_s, 12, math.pi / 12)]:
        ring = []
        for k in range(count):
            ang = phase + 2 * math.pi * k / count
            ring.append((c2x + ring_r * math.cos(ang), c2y + ring_r * math.sin(ang)))
        hex_pts.append(ring)
    center_pt = hex_pts[0][0]
    r1 = hex_pts[1]
    r2 = hex_pts[2]
    # Connect center to ring 1 and ring 1 around
    for i in range(6):
        svg.line(center_pt[0], center_pt[1], r1[i][0], r1[i][1], stroke=C["teal"], sw=1.3)
        svg.line(r1[i][0], r1[i][1], r1[(i + 1) % 6][0], r1[(i + 1) % 6][1], stroke=C["teal"], sw=1.3)
    # Connect ring 1 to ring 2 forming uniform triangles
    for i in range(6):
        p1 = r1[i]
        p1_next = r1[(i + 1) % 6]
        a = r2[(2 * i - 1) % 12]
        b = r2[(2 * i) % 12]
        c = r2[(2 * i + 1) % 12]
        for tgt in (a, b, c):
            svg.line(p1[0], p1[1], tgt[0], tgt[1], stroke=C["teal"], sw=1.15)
        svg.line(p1_next[0], p1_next[1], c[0], c[1], stroke=C["teal"], sw=1.15)
    for j in range(12):
        svg.line(r2[j][0], r2[j][1], r2[(j + 1) % 12][0], r2[(j + 1) % 12][1], stroke=C["teal"], sw=1.15)
    # Highlight one triangle + its halo neighbors
    svg.polygon([center_pt, r1[0], r1[1]], fill=C["blue"], stroke=C["blue"], sw=1.4, opacity=0.35)
    svg.polygon([r1[0], r1[1], r2[1]], fill=C["gold"], stroke=C["gold"], sw=1.2, opacity=0.35)

    svg.text(c2x, c2y + r_s + 24, "ICON Icosahedral Mesh", size=14.8, color=C["teal"], weight="bold", anchor="middle")
    svg.text(c2x, c2y + r_s + 44, "Uniform triangles (no poles)", size=13.2, color=C["muted"], anchor="middle")

    # 3 Test Cases Box at bottom of Left Panel
    svg.rect(48, 370, 406, 236, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(64, 398, "Three ASC26 Finals Earth-System Cases", size=15.2, color=C["ink"], weight="bold")

    cases = [
        ("RCE_torus", "24-day sim", "Idealized radiative-convective atmosphere dycore", C["blue"], C["surface_blue"]),
        ("OMIP", "20-year sim", "Global ocean + sea-ice circulation long-run throughput", C["teal"], C["surface_teal"]),
        ("aquaplanet", "2-month sim", "Coupled ocean-atmosphere flux exchange on water world", C["violet"], C["surface_violet"]),
    ]
    for idx, (cname, dur, desc, col, bg) in enumerate(cases):
        cy0 = 414 + idx * 60
        svg.rect(62, cy0, 378, 50, fill=bg, stroke=col, sw=1.3, rx=6)
        svg.text(76, cy0 + 21, cname, size=15, color=col, weight="bold", mono=True)
        pill(svg, 204, cy0 + 6, 108, 22, dur, C["white"], col, col, size=12.8)
        svg.text(76, cy0 + 42, desc, size=13.0, color=C["ink2"])

    # Right Panel: Winning 5-University Alliance Diagram
    svg.panel_box(494, 92, 438, 536, "Winning 5-University Alliance (ASC26 Talk)", accent=C["gold"])

    # Central Shared Optimization Hub
    hub_x, hub_y = 713.0, 272.0
    svg.rect(hub_x - 102, hub_y - 44, 204, 88, fill=C["surface_gold"], stroke=C["gold"], sw=2.0, rx=10)
    svg.text(hub_x, hub_y - 16, "Shared Patch Repo", size=15.5, color=C["gold"], weight="bold", anchor="middle")
    svg.text(hub_x, hub_y + 8, "OpenMP · Lean Halo", size=13.8, color=C["ink"], weight="bold", anchor="middle")
    svg.text(hub_x, hub_y + 30, "SIMD · MPI Sync (+5%)", size=13.8, color=C["teal"], weight="bold", anchor="middle")

    # 5 universities arranged around hub (pentagon)
    unis = [
        ("SJTU", "Shanghai Jiao Tong", 0, C["blue"]),
        ("QHU", "Qinghai Univ.", 72, C["teal"]),
        ("BUAA", "Beihang Univ.", 144, C["violet"]),
        ("BNU", "Beijing Normal", 216, C["blue"]),
        ("EAFIT", "EAFIT (Colombia)", 288, C["coral"]),
    ]
    rad_x, rad_y = 148.0, 114.0
    for code, cname, deg, col in unis:
        ang = math.radians(deg - 90)
        ux = hub_x + rad_x * math.cos(ang)
        uy = hub_y + rad_y * math.sin(ang)
        # Bidirectional connector to hub
        dx, dy = ux - hub_x, uy - hub_y
        dist = math.hypot(dx, dy)
        sx = hub_x + dx * (62 / dist)
        sy = hub_y + dy * (46 / dist)
        ex = ux - dx * (46 / dist)
        ey = uy - dy * (28 / dist)
        svg.line(sx, sy, ex, ey, stroke=col, sw=1.8, marker_start="arr_gold", marker_end="arr")

        bw_u, bh_u = 114.0, 46.0
        svg.rect(ux - bw_u / 2, uy - bh_u / 2, bw_u, bh_u, fill=C["white"], stroke=col, sw=1.8, rx=8)
        svg.text(ux, uy - 2, code, size=15.5, color=col, weight="bold", anchor="middle", mono=True)
        svg.text(ux, uy + 16, cname, size=11.8, color=C["ink2"], anchor="middle")

    # Bottom Rules & Patch Checklist inside Right Panel
    svg.rect(514, 434, 398, 174, fill=C["surface"], stroke=C["grid"], sw=1.2, rx=6)
    svg.text(530, 460, "Rules & Verified Optimizations", size=15.2, color=C["ink"], weight="bold")
    svg.multiline(
        530,
        488,
        [
            "• Cross-university teams share source patches",
            "• Each team runs solo on its 5 kW CPU-only cluster",
            "• Tuning: OpenMP scheduling, lean halo, dead-kernel cut",
            "• Explicit inner-loop SIMD; MPI sync gain ~+5%",
            "• Note: 8-pt group rule is ASC26 finals, not ASC27",
        ],
        size=13.5,
        color=C["ink2"],
        lh=24,
    )

    return svg.save_and_render("c10_asc26_icon_group", png_width=1800)


def main() -> None:
    makers = [
        make_c01,
        make_c02,
        make_c03,
        make_c04,
        make_c05,
        make_c06,
        make_c07,
        make_c08,
        make_c09,
        make_c10,
    ]
    for fn in makers:
        out = fn()
        print(f"Rendered: {out}")


if __name__ == "__main__":
    main()
