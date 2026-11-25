#!/usr/bin/env python3
"""Generate minimalist English SVG/PNG diagrams for Modules 08-16 of HKUST ASC27."""

from __future__ import annotations

import math
import sys
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from svg_kit import C, PlotBox, SVGCanvas


def draw_bracket_h(
    svg: SVGCanvas,
    x1: float,
    x2: float,
    y: float,
    tick: float = 6.0,
    stroke: str = C["slate"],
    sw: float = 1.6,
) -> None:
    svg.line(x1, y, x2, y, stroke=stroke, sw=sw)
    svg.line(x1, y, x1, y + tick, stroke=stroke, sw=sw)
    svg.line(x2, y, x2, y + tick, stroke=stroke, sw=sw)


def gen_m08_timeline_profiling() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Nsight Systems / Score-P Timeline Profiling",
        "Blocking sync (pageable) vs. pinned memory, multi-stream overlap, and Slurm core pinning",
        accent=C["blue"],
    )

    for label, col, lx in [
        ("CPU Prep", C["blue_l"], 36),
        ("PCIe H2D", C["gold"], 166),
        ("GPU Kernel", C["teal"], 298),
        ("PCIe D2H", C["violet"], 444),
        ("Idle Bubble / Sync Wait", C["coral"], 578),
    ]:
        if label.startswith("Idle"):
            svg.rect(lx, 78, 16, 13, fill="#FFF1ED", stroke=col, sw=1.4, rx=2, dash="3,2")
        else:
            svg.rect(lx, 78, 16, 13, fill=col, rx=2)
        svg.text(lx + 22, 90, label, size=14.5, color=C["ink2"])

    tx0, scale = 158.0, 7.4
    tx = lambda ms: tx0 + ms * scale

    svg.panel_box(28, 104, 904, 224, "Before: Blocking Sync (Pageable Memory + Default Stream 0)", accent=C["coral"])
    for ms in range(0, 100, 10):
        svg.line(tx(ms), 144, tx(ms), 290, stroke=C["grid"], sw=1.0)

    for name, ty in [("CPU Thread", 150), ("PCIe H2D", 184), ("GPU Kernel", 218), ("PCIe D2H", 252)]:
        svg.text(146, ty + 18, name, size=14.5, color=C["ink2"], weight="bold", anchor="end")
        svg.rect(tx0, ty, 95 * scale, 26, fill=C["surface"], stroke=C["grid"], sw=0.8, rx=3)

    for idx in range(3):
        b = idx * 30.0
        svg.rect(tx(b), 150, 8 * scale, 26, fill=C["blue_l"], rx=3)
        svg.text(tx(b + 4), 168, f"P{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(b + 8), 150, 22 * scale, 26, fill="#FFF1ED", stroke=C["coral"], sw=1.1, rx=3, dash="4,3")
        svg.text(tx(b + 19), 168, "Sync Wait", size=14.5, color=C["coral"], anchor="middle")
        svg.rect(tx(b + 8), 184, 7 * scale, 26, fill=C["gold"], rx=3)
        svg.text(tx(b + 11.5), 202, f"H{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(b + 15), 218, 10 * scale, 26, fill=C["teal"], rx=3)
        svg.text(tx(b + 20), 236, f"K{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(b + 25), 252, 5 * scale, 26, fill=C["violet"], rx=3)
        svg.text(tx(b + 27.5), 270, f"D{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")

    for bs, be, lbl in [(0, 15, "GPU Idle"), (25, 45, "GPU Bubble"), (55, 75, "GPU Bubble")]:
        svg.rect(tx(bs), 218, (be - bs) * scale, 26, fill="#FFF1ED", stroke=C["coral"], sw=1.2, rx=3, dash="4,3")
        svg.text(tx((bs + be) / 2), 236, lbl, size=14.5, color=C["coral"], weight="bold", anchor="middle")

    svg.line(tx(90), 142, tx(90), 296, stroke=C["coral"], sw=2.0, dash="5,3")
    svg.rect(tx(90) - 56, 295, 112, 24, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=4)
    svg.text(tx(90), 312, "Total: 90 ms", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    for ms in [0, 20, 40, 60, 80]:
        svg.text(tx(ms), 305, f"{ms} ms", size=14.5, color=C["muted"], anchor="middle")
    svg.text(tx(40), 322, "Effective GPU utilization ~33% (serialized waits + pageable copies)", size=14.5, color=C["coral"], anchor="middle")

    svg.panel_box(28, 342, 904, 290, "After: Pinned Memory + Multi-Stream Async + Slurm Core Pinning (--cpu-bind=cores)", accent=C["teal"])
    for ms in range(0, 100, 10):
        svg.line(tx(ms), 384, tx(ms), 574, stroke=C["grid"], sw=1.0)

    for name, ty in [("CPU (Pinned)", 392), ("Stream 0", 426), ("Stream 1", 460), ("Stream 2", 494), ("GPU Active", 532)]:
        svg.text(146, ty + 18, name, size=14.5, color=C["ink2"], weight="bold", anchor="end")
        svg.rect(tx0, ty, (42 if ty != 532 else 95) * scale, 25, fill=C["surface"], stroke=C["grid"], sw=0.8, rx=3)

    streams = [
        (0, 0.0, 3.5, 3.5, 8.0, 8.0, 17.0, 17.0, 20.0, 426),
        (1, 3.5, 7.0, 8.0, 12.5, 17.0, 26.0, 26.0, 29.0, 460),
        (2, 7.0, 10.5, 12.5, 17.0, 26.0, 35.0, 35.0, 38.0, 494),
    ]
    for idx, c0, c1, h0, h1, k0, k1, d0, d1, sy in streams:
        svg.rect(tx(c0), 392, (c1 - c0) * scale, 25, fill=C["blue_l"], rx=3)
        svg.text(tx((c0 + c1) / 2), 409, f"P{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(h0), sy, (h1 - h0) * scale, 25, fill=C["gold"], rx=3)
        svg.text(tx((h0 + h1) / 2), sy + 17, f"H{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(k0), sy, (k1 - k0) * scale, 25, fill=C["teal"], rx=3)
        svg.text(tx((k0 + k1) / 2), sy + 17, f"K{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.rect(tx(d0), sy, (d1 - d0) * scale, 25, fill=C["violet"], rx=3)
        svg.text(tx((d0 + d1) / 2), sy + 17, f"D{idx}", size=14.5, color=C["white"], weight="bold", anchor="middle")

    svg.rect(tx(8), 532, 27 * scale, 25, fill=C["teal"], rx=3)
    svg.text(tx(21.5), 549, "Bubble-Free Compute (K0+K1+K2)", size=14.5, color=C["white"], weight="bold", anchor="middle")

    svg.line(tx(38), 382, tx(38), 580, stroke=C["teal"], sw=2.2, dash="5,3")
    svg.line(tx(90), 382, tx(90), 580, stroke=C["coral"], sw=1.6, dash="4,4")
    svg.line(tx(38) + 6, 404, tx(90) - 6, 404, stroke=C["teal"], sw=2.4, marker_start="arr_teal", marker_end="arr_teal")
    svg.rect(tx(49.5), 388, 224, 30, fill=C["surface_teal"], stroke=C["teal"], sw=1.5, rx=6)
    svg.text(tx(49.5) + 112, 408, "~2.4x Faster (90 -> 38 ms)", size=14.5, color=C["teal"], weight="bold", anchor="middle")

    svg.rect(tx(43.5), 428, 434, 96, fill=C["white"], stroke=C["grid"], sw=1.4, rx=6)
    svg.rect(tx(43.5), 428, 5, 96, fill=C["teal"], rx=2)
    svg.multiline(
        tx(43.5) + 18,
        451,
        [
            "Key Profiling Optimizations:",
            "1. cudaMallocHost pinned memory enables async DMA overlap",
            "2. Three CUDA streams pipeline H2D, Kernel, and D2H stages",
            "3. Slurm --cpu-bind=cores removes OS migration jitter",
        ],
        size=14.5,
        color=C["ink2"],
        lh=21,
    )

    svg.line(tx0, 576, tx(95), 576, stroke=C["slate"], sw=1.6)
    for ms in [0, 10, 20, 30, 38, 50, 60, 70, 80, 90]:
        col = C["teal"] if ms == 38 else (C["coral"] if ms == 90 else C["muted"])
        svg.line(tx(ms), 576, tx(ms), 582, stroke=col, sw=1.4)
        svg.text(tx(ms), 598, f"{ms}", size=14.5, color=col, weight="bold" if ms in (38, 90) else "normal", anchor="middle")
    svg.text(tx(47.5), 620, "Wall-Clock Time (ms)", size=15, color=C["ink2"], weight="bold", anchor="middle")
    svg.save_and_render("m08_timeline_profiling")


def gen_m09_transformer_memory_precision() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Transformer Training Memory & Floating-Point Formats",
        "7B mixed-precision AdamW memory (16 Phi = 112 GB) + activations vs. IEEE / AI bit layouts",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 452, 546, "7B Mixed-Precision AdamW Memory (GB)", accent=C["blue"])
    pb = PlotBox(svg, x=98, y=144, w=358, h=346, xmin=0.0, xmax=2.0, ymin=0.0, ymax=200.0)
    pb.draw_axes(
        xticks=[],
        yticks=[(0, "0"), (40, "40"), (80, "80"), (120, "120"), (160, "160"), (200, "200")],
        ylabel="GPU Memory (GB)",
    )

    y80 = pb.py(80)
    svg.line(pb.x, y80, pb.x + pb.w, y80, stroke=C["coral"], sw=1.8, dash="6,4")
    svg.rect(pb.x + 4, y80 - 24, 168, 20, fill=C["surface_coral"], stroke=C["coral"], sw=1.0, rx=3)
    svg.text(pb.x + 88, y80 - 9, "80 GB GPU Limit", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    y112 = pb.py(112)
    svg.line(pb.x, y112, pb.px(0.5) - 58, y112, stroke=C["slate"], sw=1.5, dash="4,4")
    svg.line(pb.px(1.48) + 58, y112, pb.x + pb.w, y112, stroke=C["slate"], sw=1.5, dash="4,4")
    svg.text(pb.x + 6, y112 - 8, "Static 16 Phi = 112 GB", size=14.5, color=C["slate"], weight="bold", anchor="start")

    static_segs = [
        (0, 14, C["blue"], "W 14"),
        (14, 28, C["blue_l"], "G 14"),
        (28, 56, C["violet"], "FP32 28"),
        (56, 112, C["gold"], "Adam m,v 56 GB"),
    ]
    bars = [
        (0.50, 70, C["coral"], "Act ~70 GB", "~182 GB", "No Checkpointing"),
        (1.48, 14, C["teal"], "Act 14", "~126 GB", "With Checkpointing"),
    ]
    bw = 104.0
    for cx_v, act_gb, act_col, act_lbl, tot_lbl, xlbl in bars:
        bx = pb.px(cx_v) - bw / 2
        for v0, v1, col, seg_lbl in static_segs:
            yt, h = pb.py(v1), pb.py(v0) - pb.py(v1)
            svg.rect(bx, yt, bw, h, fill=col, stroke=C["white"], sw=1.0)
            if h >= 21:
                svg.text(bx + bw / 2, yt + h / 2 + 5, seg_lbl, size=14.5, color=C["white"], weight="bold", anchor="middle")
        ya, ha = pb.py(112 + act_gb), pb.py(112) - pb.py(112 + act_gb)
        svg.rect(bx, ya, bw, ha, fill=act_col, stroke=C["white"], sw=1.0)
        if ha >= 21:
            svg.text(bx + bw / 2, ya + ha / 2 + 5, act_lbl, size=14.5, color=C["white"], weight="bold", anchor="middle")
        svg.text(bx + bw / 2, ya - 9, tot_lbl, size=15, color=act_col, weight="bold", anchor="middle")
        svg.text(bx + bw / 2, pb.y + pb.h + 24, xlbl, size=14.5, color=C["ink"], weight="bold", anchor="middle")

    svg.text(pb.px(1.48), pb.py(154), "Act -80%", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb.px(1.48), pb.py(142), "(+33% recompute)", size=14.5, color=C["muted"], anchor="middle")

    for lbl, col, lx, ly in [
        ("BF16 Weights (2Φ = 14 GB)", C["blue"], 46, 546),
        ("BF16 Grads (2Φ = 14 GB)", C["blue_l"], 264, 546),
        ("FP32 Master (4Φ = 28 GB)", C["violet"], 46, 574),
        ("Adam m,v FP32 (8Φ = 56 GB)", C["gold"], 264, 574),
        ("Activations (No Ckpt / With Ckpt)", C["coral"], 46, 602),
    ]:
        svg.rect(lx, ly - 11, 13, 13, fill=col, rx=2)
        svg.text(lx + 19, ly, lbl, size=14.5, color=C["ink2"])

    svg.panel_box(496, 86, 436, 546, "Floating-Point Bit Layouts (Sign / Exp / Mant)", accent=C["violet"])
    for lbl, col, lx in [("Sign", C["coral"], 518), ("Exponent (Range)", C["blue"], 592), ("Mantissa (Precision)", C["teal"], 752)]:
        svg.rect(lx, 134, 14, 14, fill=col, rx=2)
        svg.text(lx + 19, 146, lbl, size=14.5, color=C["ink2"], weight="bold")

    formats = [
        ("FP64 (64b)", "1 + 11 + 52", 26, 98, 266, "Range +-10^308 · HPC double precision (HPL / HPCG)"),
        ("FP32 (32b)", "1 + 8 + 23", 26, 82, 198, "Range +-10^38 · Master weights & Adam optimizer states"),
        ("BF16 (16b)", "1 + 8 + 7", 26, 82, 108, "Same 8-bit exponent as FP32 · no loss scaling needed"),
        ("FP16 (16b)", "1 + 5 + 10", 26, 58, 132, "Range +-6.5e4 overflows easily · requires GradScaler"),
        ("FP8 E4M3", "1 + 4 + 3", 26, 52, 68, "H100 / B200 Tensor Core inference & FP8 training"),
    ]
    bx0 = 518.0
    for idx, (fname, bspec, sw, ew, mw, note) in enumerate(formats):
        fy = 176.0 + idx * 78.0
        svg.text(bx0, fy, fname, size=15.5, color=C["ink"], weight="bold")
        svg.text(bx0 + 116, fy, bspec, size=14.5, color=C["muted"], mono=True)
        by, bh = fy + 8, 28.0
        eb, mb = [p.strip() for p in bspec.split("+")[1:]]
        svg.rect(bx0, by, sw, bh, fill=C["coral"], stroke=C["white"], sw=1.2, rx=2)
        svg.text(bx0 + sw / 2, by + 19, "1", size=14.5, color=C["white"], weight="bold", anchor="middle", mono=True)
        svg.rect(bx0 + sw, by, ew, bh, fill=C["blue"], stroke=C["white"], sw=1.2, rx=2)
        svg.text(bx0 + sw + ew / 2, by + 19, f"{eb}b", size=14.5, color=C["white"], weight="bold", anchor="middle", mono=True)
        svg.rect(bx0 + sw + ew, by, mw, bh, fill=C["teal"], stroke=C["white"], sw=1.2, rx=2)
        svg.text(bx0 + sw + ew + mw / 2, by + 19, f"{mb}b", size=14.5, color=C["white"], weight="bold", anchor="middle", mono=True)
        if idx == 1:
            svg.line(bx0 + sw, by + bh, bx0 + sw, by + 78, stroke=C["gold"], sw=1.8, dash="3,2")
            svg.line(bx0 + sw + ew, by + bh, bx0 + sw + ew, by + 78, stroke=C["gold"], sw=1.8, dash="3,2")
        if idx == 2:
            svg.rect(bx0 + sw + ew + mw + 12, by + 2, 152, 24, fill=C["surface_gold"], stroke=C["gold"], sw=1.2, rx=4)
            svg.text(bx0 + sw + ew + mw + 88, by + 18, "Matches FP32 Exp", size=14.5, color=C["gold"], weight="bold", anchor="middle")
        svg.text(bx0, by + bh + 18, note, size=14.5, color=C["ink2"])

    svg.rect(516, 560, 396, 58, fill=C["surface_violet"], stroke=C["violet"], sw=1.4, rx=6)
    svg.multiline(
        530,
        583,
        [
            "Static Memory = (2 + 2 + 4 + 8)Φ = 16Φ  (7B -> 112 GB)",
            "Practice: BF16 fwd/bwd + FP32 accumulation + FSDP sharding",
        ],
        size=14.5,
        color=C["ink"],
        lh=22,
    )
    svg.save_and_render("m09_transformer_memory_precision")


def gen_m10_distributed_training_ring() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "3D Parallelism Hardware Mapping & Ring All-Reduce",
        "Hierarchy-aware TP / PP / FSDP placement and bandwidth-optimal 4-GPU circular All-Reduce",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 456, 546, "3D Parallelism Topology (2 Nodes x 4 GPUs)", accent=C["blue"])

    def draw_node(ny: float, node_lbl: str, g0: int, tp_lbl: str) -> None:
        svg.rect(48, ny, 416, 148, fill=C["surface_blue"], stroke=C["blue"], sw=1.5, rx=8, dash="6,3")
        svg.text(62, ny + 22, node_lbl, size=15, color=C["blue"], weight="bold")
        svg.rect(220, ny + 6, 232, 22, fill=C["surface_teal"], stroke=C["teal"], sw=1.0, rx=4)
        svg.text(336, ny + 21, "Intra-Node NVLink ~900 GB/s", size=14.5, color=C["teal"], weight="bold", anchor="middle")
        svg.rect(68, ny + 84, 376, 12, fill=C["teal"], rx=4, opacity=0.25)
        svg.line(74, ny + 90, 438, ny + 90, stroke=C["teal"], sw=3.2)
        for i in range(4):
            gx = 64 + i * 98
            svg.rect(gx, ny + 38, 82, 46, fill=C["white"], stroke=C["blue"], sw=1.6, rx=6)
            svg.text(gx + 41, ny + 58, f"GPU {g0 + i}", size=14.5, color=C["ink"], weight="bold", anchor="middle")
            svg.text(gx + 41, ny + 76, f"TP r{i}", size=14.5, color=C["teal"], weight="bold", anchor="middle")
            svg.line(gx + 41, ny + 84, gx + 41, ny + 94, stroke=C["teal"], sw=2.4)
        svg.text(256, ny + 116, tp_lbl, size=14.5, color=C["ink2"], weight="bold", anchor="middle")
        svg.text(256, ny + 136, "2 All-Reduces per layer stay inside high-BW NVLink domain", size=14.5, color=C["muted"], anchor="middle")

    draw_node(134, "Node 0", 0, "Tensor Parallel Group 0 (Intra-Node)")

    svg.rect(58, 326, 396, 44, fill=C["surface_coral"], stroke=C["coral"], sw=1.6, rx=6)
    svg.text(256, 346, "Inter-Node InfiniBand NDR / RoCE (~50 GB/s)", size=15, color=C["coral"], weight="bold", anchor="middle")
    svg.text(256, 364, "~18x slower than NVLink: assign P2P & overlapped collectives", size=14.5, color=C["ink2"], anchor="middle")

    svg.line(134, 282, 134, 324, stroke=C["violet"], sw=2.6, marker_end="arr_violet")
    svg.line(134, 370, 134, 412, stroke=C["violet"], sw=2.6, marker_end="arr_violet")
    svg.rect(52, 290, 166, 26, fill=C["surface_violet"], stroke=C["violet"], sw=1.1, rx=4)
    svg.text(135, 308, "Pipeline (PP P2P)", size=14.5, color=C["violet"], weight="bold", anchor="middle")

    svg.line(378, 282, 378, 324, stroke=C["gold"], sw=2.6, marker_start="arr_gold", marker_end="arr_gold")
    svg.line(378, 370, 378, 412, stroke=C["gold"], sw=2.6, marker_start="arr_gold", marker_end="arr_gold")
    svg.rect(236, 290, 228, 26, fill=C["surface_gold"], stroke=C["gold"], sw=1.1, rx=4)
    svg.text(350, 308, "FSDP / DP (RS + All-Gather)", size=14.5, color=C["gold"], weight="bold", anchor="middle")

    draw_node(414, "Node 1", 4, "Tensor Parallel Group 1 (Intra-Node)")

    for lbl, col, bgc, px, pw in [
        ("TP -> NVLink", C["teal"], C["surface_teal"], 48, 128),
        ("PP -> IB P2P", C["violet"], C["surface_violet"], 186, 126),
        ("FSDP -> IB Overlap", C["gold"], C["surface_gold"], 322, 142),
    ]:
        svg.rect(px, 578, pw, 36, fill=bgc, stroke=col, sw=1.3, rx=6)
        svg.text(px + pw / 2, 601, lbl, size=14.5, color=col, weight="bold", anchor="middle")

    svg.panel_box(500, 86, 432, 546, "4-GPU Ring All-Reduce Two-Phase Topology", accent=C["teal"])
    cx, cy, ring_r = 716.0, 278.0, 110.0

    for a1_d, a2_d in [(-62, -28), (28, 62), (118, 152), (208, 242)]:
        a1, a2 = math.radians(a1_d), math.radians(a2_d)
        for rad, col, sw, dash, mk in [
            (114.0, C["blue"], 2.8, "", "arr_blue"),
            (92.0, C["teal"], 2.2, "5,3", "arr_teal"),
        ]:
            x1, y1 = cx + rad * math.cos(a1), cy + rad * math.sin(a1)
            x2, y2 = cx + rad * math.cos(a2), cy + rad * math.sin(a2)
            svg.path(f"M {x1:.1f} {y1:.1f} A {rad:.1f} {rad:.1f} 0 0 1 {x2:.1f} {y2:.1f}", stroke=col, sw=sw, dash=dash, marker_end=mk)

    svg.circle(cx, cy, 56, fill=C["white"], stroke=C["grid"], sw=1.6)
    svg.multiline(cx, cy - 14, ["p = 4 Ranks", "Send G/p / step", "No bottleneck"], size=14.5, color=C["ink"], weight="bold", anchor="middle", lh=20)

    chunk_cols = [C["blue"], C["teal"], C["violet"], C["gold"]]
    for gid, gx, gy, acc in [
        (0, cx, cy - ring_r, C["blue"]),
        (1, cx + ring_r, cy, C["teal"]),
        (2, cx, cy + ring_r, C["violet"]),
        (3, cx - ring_r, cy, C["gold"]),
    ]:
        svg.rect(gx - 47, gy - 28, 94, 56, fill=C["white"], stroke=acc, sw=1.8, rx=7)
        svg.text(gx, gy - 6, f"GPU {gid}", size=15, color=C["ink"], weight="bold", anchor="middle")
        for cid in range(4):
            bx = gx - 38 + cid * 19.5
            svg.rect(bx, gy + 4, 17, 16, fill=chunk_cols[cid] if cid == gid else C["surface"], stroke=chunk_cols[cid], sw=0.9, rx=2)
            svg.text(bx + 8.5, gy + 16, f"c{cid}", size=14.5, color=C["white"] if cid == gid else C["muted"], weight="bold", anchor="middle", mono=True)

    svg.line(518, 146, 548, 146, stroke=C["blue"], sw=2.6, marker_end="arr_blue")
    svg.text(554, 151, "Scatter-Reduce", size=14.5, color=C["blue"], weight="bold")
    svg.line(774, 146, 804, 146, stroke=C["teal"], sw=2.2, dash="5,3", marker_end="arr_teal")
    svg.text(810, 151, "All-Gather", size=14.5, color=C["teal"], weight="bold")

    svg.rect(518, 434, 192, 82, fill=C["surface_blue"], stroke=C["blue"], sw=1.3, rx=6)
    svg.text(614, 456, "Phase 1: Scatter-Reduce", size=14.5, color=C["blue"], weight="bold", anchor="middle")
    svg.multiline(614, 478, ["p - 1 = 3 ring hops", "1 reduced shard / rank"], size=14.5, color=C["ink2"], anchor="middle", lh=20)

    svg.rect(722, 434, 192, 82, fill=C["surface_teal"], stroke=C["teal"], sw=1.3, rx=6)
    svg.text(818, 456, "Phase 2: All-Gather", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.multiline(818, 478, ["p - 1 = 3 ring hops", "Full gradient on all ranks"], size=14.5, color=C["ink2"], anchor="middle", lh=20)

    svg.rect(518, 528, 396, 88, fill=C["white"], stroke=C["teal"], sw=1.8, rx=7)
    svg.rect(518, 528, 6, 88, fill=C["teal"], rx=2)
    svg.text(538, 552, "Per-Rank Traffic (Bandwidth-Optimal)", size=14.5, color=C["ink"], weight="bold")
    svg.text(538, 580, "Bytes / rank = 2(p - 1)G / p  ->  2G", size=15.5, color=C["teal"], weight="bold", mono=True)
    svg.text(538, 604, "Independent of rank count p as p grows; limited only by min link BW", size=14.5, color=C["muted"])
    svg.save_and_render("m10_distributed_training_ring")


def gen_m11_llm_inference_kv_denoising() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "LLM Inference Regimes & Diffusion Denoising Acceleration",
        "Prefill (Compute-bound GEMM) vs. Decode (BW-bound GEMV + KV Cache), TeaCache & ParaStep",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 452, 546, "LLM Inference: Prefill vs. Decode Regimes", accent=C["blue"])
    pb = PlotBox(svg, x=98, y=138, w=358, h=188, xmin=0.5, xmax=1000.0, ymin=1.0, ymax=2000.0, xlog=True, ylog=True)
    pb.draw_axes(
        xticks=[(1, "1"), (10, "10"), (100, "100"), (1000, "1000")],
        yticks=[(1, "1"), (10, "10"), (100, "100"), (1000, "1k")],
        xlabel="Arithmetic Intensity I (FLOP / Byte)",
        ylabel="Perf (TFLOP/s)",
    )
    xs = np.logspace(math.log10(0.5), math.log10(1000.0), 160)
    pb.plot_curve(xs, np.minimum(3.35 * xs, 989.0), stroke=C["slate"], sw=2.8)

    rx = pb.px(295.2)
    svg.line(rx, pb.y, rx, pb.y + pb.h, stroke=C["muted"], sw=1.2, dash="4,3")
    svg.text(rx - 6, pb.y + 18, "I* ~ 295", size=14.5, color=C["muted"], anchor="end", mono=True)

    dx, dy = pb.px(1.5), pb.py(4.8)
    svg.circle(dx, dy, 6.5, fill=C["coral"], stroke=C["white"], sw=1.5)
    svg.rect(dx + 12, dy - 26, 160, 38, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=4)
    svg.text(dx + 92, dy - 10, "Decode (I ~ 1-2)", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(dx + 92, dy + 6, "Memory-BW GEMV", size=14.5, color=C["ink2"], anchor="middle")

    px_pt, py_pt = pb.px(420.0), pb.py(880.0)
    svg.circle(px_pt, py_pt, 6.5, fill=C["teal"], stroke=C["white"], sw=1.5)
    svg.rect(px_pt - 160, py_pt + 16, 158, 38, fill=C["surface_teal"], stroke=C["teal"], sw=1.2, rx=4)
    svg.text(px_pt - 81, py_pt + 32, "Prefill (High I)", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(px_pt - 81, py_pt + 48, "Compute-Bound GEMM", size=14.5, color=C["ink2"], anchor="middle")

    svg.rect(46, 386, 202, 134, fill=C["surface_teal"], stroke=C["teal"], sw=1.4, rx=6)
    svg.text(147, 408, "Prefill Phase", size=15, color=C["teal"], weight="bold", anchor="middle")
    svg.multiline(58, 432, ["Kernel: Matrix GEMM", "Bound: Tensor Core FLOPs", "Metric: TTFT latency", "Opt: FlashAttention"], size=14.5, color=C["ink2"], lh=22)

    svg.rect(260, 386, 202, 134, fill=C["surface_coral"], stroke=C["coral"], sw=1.4, rx=6)
    svg.text(361, 408, "Decode Phase", size=15, color=C["coral"], weight="bold", anchor="middle")
    svg.multiline(272, 432, ["Kernel: Matrix-Vec GEMV", "Bound: HBM BW & capacity", "Metric: TPOT latency", "Opt: GQA + PagedAttn"], size=14.5, color=C["ink2"], lh=22)

    svg.rect(46, 534, 416, 84, fill=C["surface_gold"], stroke=C["gold"], sw=1.5, rx=6)
    svg.text(60, 556, "KV Cache Footprint (Scales Linearly with S and B)", size=14.5, color=C["ink"], weight="bold")
    svg.text(60, 583, "M_KV = 2 · L · n_kv · d_h · S · B · b   (Bytes)", size=14.5, color=C["gold"], weight="bold", mono=True)
    svg.text(60, 606, "L layers, n_kv KV heads, head dim d_h, seq len S, batch B, bytes b", size=14.5, color=C["ink2"])

    svg.panel_box(496, 86, 436, 546, "Diffusion / World Model Pipeline (TeaCache + ParaStep)", accent=C["violet"])
    svg.text(516, 146, "1. Iterative Denoising (t_T -> t_0) & TeaCache Skip", size=15, color=C["ink"], weight="bold")

    sx0 = 520.0
    steps = [("t_T", "Noise", C["slate"], False), ("t_3", "DiT", C["violet"], False), ("t_2", "Skip", C["muted"], True), ("t_1", "DiT", C["violet"], False), ("t_0", "Output", C["teal"], False)]
    for idx, (st, sub, col, skip) in enumerate(steps):
        sx, sy = sx0 + idx * 80, 204.0
        svg.rect(sx, sy, 62, 48, fill=C["surface"] if skip else C["white"], stroke=col, sw=1.6, rx=6, dash="4,3" if skip else "")
        svg.text(sx + 31, sy + 22, st, size=14.5, color=col, weight="bold", anchor="middle", mono=True)
        svg.text(sx + 31, sy + 40, sub, size=14.5, color=C["muted"] if skip else C["ink2"], anchor="middle")
        if idx < 4:
            svg.line(sx + 63, sy + 24, sx + 78, sy + 24, stroke=C["slate"], sw=1.6, marker_end="arr")

    x1, x2 = sx0 + 111, sx0 + 271
    svg.path(f"M {x1:.1f} 202 Q {(x1 + x2) / 2:.1f} 152 {x2:.1f} 202", stroke=C["teal"], sw=2.4, marker_end="arr_teal")
    svg.rect(608, 156, 208, 24, fill=C["surface_teal"], stroke=C["teal"], sw=1.1, rx=4)
    svg.text(712, 173, "TeaCache Reuse (delta < eps)", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(714, 272, "Reuse prior DiT residual when input delta < eps (-30 to 50% steps)", size=14.5, color=C["ink2"], anchor="middle")

    svg.line(514, 290, 914, 290, stroke=C["grid"], sw=1.4)
    svg.text(516, 316, "2. ParaStep 2-GPU Speculative Step Overlap", size=15, color=C["ink"], weight="bold")

    svg.text(516, 354, "1-GPU", size=14.5, color=C["muted"], weight="bold")
    for k in range(4):
        bx = 582 + k * 79
        svg.rect(bx, 336, 73, 28, fill=C["surface"], stroke=C["slate"], sw=1.3, rx=4)
        svg.text(bx + 36.5, 355, f"Step {k}", size=14.5, color=C["ink2"], weight="bold", anchor="middle")
    svg.line(892, 332, 892, 480, stroke=C["coral"], sw=1.5, dash="4,3")
    svg.text(892, 326, "4T", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    svg.text(516, 412, "GPU 0", size=14.5, color=C["blue"], weight="bold")
    svg.text(516, 456, "GPU 1", size=14.5, color=C["violet"], weight="bold")
    for bx, lbl in [(582, "Step 0"), (668, "Step 2")]:
        svg.rect(bx, 392, 76, 30, fill=C["blue"], rx=4)
        svg.text(bx + 38, 412, lbl, size=14.5, color=C["white"], weight="bold", anchor="middle")
    for bx, lbl in [(614, "Step 1*"), (700, "Step 3*")]:
        svg.rect(bx, 436, 78, 30, fill=C["violet"], rx=4)
        svg.text(bx + 39, 456, lbl, size=14.5, color=C["white"], weight="bold", anchor="middle")

    svg.line(632, 422, 646, 434, stroke=C["gold"], sw=2.0, marker_end="arr_gold")
    svg.line(680, 436, 692, 424, stroke=C["gold"], sw=2.0, marker_end="arr_gold")
    svg.line(718, 422, 732, 434, stroke=C["gold"], sw=2.0, marker_end="arr_gold")

    svg.line(780, 386, 780, 480, stroke=C["teal"], sw=2.0, dash="4,3")
    svg.line(784, 426, 888, 426, stroke=C["teal"], sw=2.2, marker_start="arr_teal", marker_end="arr_teal")
    svg.rect(790, 392, 118, 28, fill=C["surface_teal"], stroke=C["teal"], sw=1.2, rx=4)
    svg.text(849, 411, "~1.7-1.9x", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(714, 500, "*GPU 1 predicts latent state early and syncs correction via NVLink", size=14.5, color=C["ink2"], anchor="middle")

    svg.rect(514, 534, 400, 84, fill=C["surface_violet"], stroke=C["violet"], sw=1.5, rx=6)
    svg.text(528, 558, "ASC26 UnifoLM / LeWM Optimization Playbook", size=14.5, color=C["violet"], weight="bold")
    svg.multiline(
        528,
        582,
        [
            "1. Trim redundant steps with TeaCache, then overlap with ParaStep",
            "2. Validate every shortcut against full-trajectory quality gates",
        ],
        size=14.5,
        color=C["ink2"],
        lh=21,
    )
    svg.save_and_render("m11_llm_inference_kv_denoising")


def gen_m12_amss_bottleneck_shift() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "AMSS-NCKU Step Latency & Bottleneck Shift Case Study",
        "Verified Tsinghua ASC26 talk data · Numerical relativity step cut from 4.50s to 0.85s (5.3x)",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 904, 286, "Step Latency Progression (Seconds / Step, Lower Is Better)", accent=C["blue"])
    bx0, px_s = 232.0, 76.0
    for sec in range(6):
        gx = bx0 + sec * px_s
        svg.line(gx, 134, gx, 336, stroke=C["grid"], sw=1.0)
        svg.text(gx, 355, f"{sec}.0 s", size=14.5, color=C["muted"], anchor="middle")
    svg.line(bx0, 134, bx0, 338, stroke=C["slate"], sw=1.6)

    stages = [
        ("Original CPU", 4.50, C["slate"], "4.50 s (1.0x)", "Compute-bound BSSN RHS"),
        ("GPU v1 (RHS only)", 4.70, C["coral"], "4.70 s (4% slower)", "122 H2D/D2H roundtrips"),
        ("GPU-Resident", 1.40, C["gold"], "1.40 s (3.2x)", "Zero PCIe transfers"),
        ("2+62 Core Split", 1.00, C["blue"], "1.00 s (4.5x)", "2 GPU drivers + 62 CPU interp"),
        ("3-Stage Async Relay", 0.85, C["teal"], "0.85 s (5.3x)", "Compute / comm / BC overlap"),
    ]
    for idx, (label, val, col, vtxt, note) in enumerate(stages):
        by = 142.0 + idx * 39.0
        bw = val * px_s
        svg.text(bx0 - 12, by + 19, label, size=14.5, color=C["ink"], weight="bold", anchor="end")
        svg.rect(bx0, by, bw, 26, fill=col, rx=4)
        svg.text(bx0 + bw + 10, by + 19, vtxt, size=14.5, color=col, weight="bold")
        svg.text(914, by + 19, note, size=14.5, color=C["ink2"], anchor="end")

    svg.panel_box(28, 386, 904, 246, "GPU v1 Time Breakdown (4.70 s) & Bottleneck Migration", accent=C["coral"])
    sx0, tot_w, sy, sh = 52.0, 856.0, 456.0, 42.0
    segs = [
        (33, C["coral"], "33% Pack / Unpack"),
        (32, C["gold"], "32% CPU Interp / Regrid"),
        (21, C["violet"], "21% Copy & Wait"),
        (14, C["slate"], "14% Other"),
    ]
    cur_x, bounds = sx0, []
    for pct, col, lbl in segs:
        sw = tot_w * pct / 100.0
        svg.rect(cur_x, sy, sw, sh, fill=col, stroke=C["white"], sw=1.4, rx=3)
        svg.text(cur_x + sw / 2, sy + 26, lbl, size=14.5, color=C["white"], weight="bold", anchor="middle")
        bounds.append((cur_x, cur_x + sw))
        cur_x += sw

    draw_bracket_h(svg, bounds[0][0] + 2, bounds[1][1] - 2, sy - 10, tick=7, stroke=C["coral"], sw=1.8)
    svg.text((bounds[0][0] + bounds[1][1]) / 2, sy - 18, "65% (~2/3) Non-RHS Host & Grid Overhead", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    draw_bracket_h(svg, bounds[2][0] + 2, bounds[2][1] - 2, sy - 10, tick=7, stroke=C["violet"], sw=1.6)
    svg.text((bounds[2][0] + bounds[2][1]) / 2, sy - 18, "122 H2D/D2H Trips", size=14.5, color=C["violet"], weight="bold", anchor="middle")

    flow = [
        ("1. Compute-Bound", "Original CPU (4.5s)", "Slow BSSN RHS kernel", C["slate"], C["surface"]),
        ("2. Transfer-Bound", "GPU v1 (4.7s)", "122 copies + pack/unpack", C["coral"], C["surface_coral"]),
        ("3. Analysis-Bound", "GPU-Resident (1.4s)", "CPU interp stalls GPU", C["gold"], C["surface_gold"]),
        ("4. Balanced Relay", "Split + Async (0.85s)", "5.3x pipelined speedup", C["teal"], C["surface_teal"]),
    ]
    fw, fgap, fy = 188.0, 34.6, 530.0
    for idx, (title, s1, s2, col, bgc) in enumerate(flow):
        fx = 52.0 + idx * (fw + fgap)
        svg.rect(fx, fy, fw, 82, fill=bgc, stroke=col, sw=1.6, rx=7)
        svg.rect(fx, fy, fw, 6, fill=col, rx=3)
        svg.text(fx + fw / 2, fy + 30, title, size=15.5, color=col, weight="bold", anchor="middle")
        svg.text(fx + fw / 2, fy + 52, s1, size=14.5, color=C["ink"], weight="bold", anchor="middle")
        svg.text(fx + fw / 2, fy + 71, s2, size=14.5, color=C["ink2"], anchor="middle")
        if idx < 3:
            svg.line(fx + fw + 4, fy + 41, fx + fw + fgap - 4, fy + 41, stroke=C["slate"], sw=2.4, marker_end="arr")
    svg.save_and_render("m12_amss_bottleneck_shift")


def gen_m13_hpl_panel_scaling() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "HPL 2D Block-Cyclic Layout & Efficiency Scaling",
        "P x Q = 2 x 3 panel broadcast + trailing DGEMM and RAM occupancy scaling (20% to 90%)",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 452, 546, "2D Block-Cyclic Matrix (P x Q = 2 x 3, Block NB)", accent=C["blue"])
    gx0, gy0, bs = 112.0, 168.0, 46.0

    draw_bracket_h(svg, gx0, gx0 + 6 * bs, gy0 - 14, tick=6, stroke=C["slate"], sw=1.4)
    svg.text(gx0 + 3 * bs, gy0 - 22, "Matrix Order N (Blocks of NB x NB)", size=14.5, color=C["ink2"], weight="bold", anchor="middle")
    svg.line(gx0 - 12, gy0, gx0 - 12, gy0 + bs, stroke=C["blue"], sw=1.6)
    svg.line(gx0 - 12, gy0, gx0 - 6, gy0, stroke=C["blue"], sw=1.6)
    svg.line(gx0 - 12, gy0 + bs, gx0 - 6, gy0 + bs, stroke=C["blue"], sw=1.6)
    svg.text(gx0 - 18, gy0 + bs / 2 + 5, "NB", size=14.5, color=C["blue"], weight="bold", anchor="end", mono=True)

    for r in range(6):
        for c in range(6):
            bx, by = gx0 + c * bs, gy0 + r * bs
            if r < 1 or c < 1:
                fc, sc, tc = C["surface"], C["axis"], C["muted"]
            elif c == 1 and r >= 1:
                fc, sc, tc = C["surface_gold"], C["gold"], C["gold"]
            elif r == 1 and c >= 2:
                fc, sc, tc = C["surface_violet"], C["violet"], C["violet"]
            else:
                fc, sc, tc = C["surface_teal"], C["teal"], C["teal"]
            svg.rect(bx, by, bs, bs, fill=fc, stroke=sc, sw=1.3)
            svg.text(bx + bs / 2, by + bs / 2 + 5, f"({r % 2},{c % 3})", size=14.5, color=tc, weight="bold", anchor="middle", mono=True)

    svg.rect(gx0 + bs, gy0 + bs, bs, 5 * bs, fill="none", stroke=C["gold"], sw=2.6)
    svg.rect(gx0 + 2 * bs, gy0 + 2 * bs, 4 * bs, 4 * bs, fill="none", stroke=C["teal"], sw=2.6)
    svg.line(gx0 + 1.85 * bs, gy0 + 3.5 * bs, gx0 + 2.45 * bs, gy0 + 3.5 * bs, stroke=C["gold"], sw=2.6, marker_end="arr_gold")
    svg.rect(gx0 + 2.35 * bs, gy0 + 3.08 * bs, 148, 38, fill=C["white"], stroke=C["teal"], sw=1.4, rx=5, opacity=0.96)
    svg.text(gx0 + 2.35 * bs + 74, gy0 + 3.08 * bs + 16, "Trailing Matrix", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(gx0 + 2.35 * bs + 74, gy0 + 3.08 * bs + 32, "DGEMM Update", size=14.5, color=C["ink2"], anchor="middle")

    for lbl, fc, sc, lx in [
        ("Factored L/U", C["surface"], C["axis"], 46),
        ("Panel Broadcast", C["surface_gold"], C["gold"], 172),
        ("TRSM Row Swap", C["surface_violet"], C["violet"], 326),
    ]:
        svg.rect(lx, 464, 14, 14, fill=fc, stroke=sc, sw=1.4, rx=2)
        svg.text(lx + 20, 476, lbl, size=14.5, color=C["ink2"])

    svg.rect(46, 496, 416, 120, fill=C["surface_blue"], stroke=C["blue"], sw=1.5, rx=6)
    svg.text(62, 520, "HPL Compute, Memory & Communication Complexity", size=14.8, color=C["blue"], weight="bold")
    svg.text(62, 548, "FLOPs = 2N^3 / 3    Memory = 8N^2 Bytes (FP64)", size=14.5, color=C["ink"], weight="bold", mono=True)
    svg.multiline(
        62,
        574,
        [
            "Compute grows as O(N^3) while panel comms grow only as O(N^2)",
            "2D cyclic layout keeps every (P,Q) rank balanced as matrix shrinks",
        ],
        size=14.5,
        color=C["ink2"],
        lh=21,
    )

    svg.panel_box(496, 86, 436, 546, "HPL Efficiency vs. RAM Occupancy (20%-90%)", accent=C["teal"])
    pb = PlotBox(svg, x=572, y=150, w=338, h=306, xmin=15.0, xmax=95.0, ymin=40.0, ymax=92.0)
    pb.draw_axes(
        xticks=[(20, "20%"), (40, "40%"), (60, "60%"), (80, "80%"), (90, "90%")],
        yticks=[(40, "40%"), (50, "50%"), (60, "60%"), (70, "70%"), (80, "80%"), (90, "90%")],
        xlabel="Node Memory Occupancy (8N^2 / RAM)",
        ylabel="Peak Efficiency (%)",
    )

    x80, x88 = pb.px(80.0), pb.px(88.0)
    svg.rect(x80, pb.y, x88 - x80, pb.h, fill=C["surface_teal"], stroke="none", opacity=0.85)
    svg.line(x80, pb.y, x80, pb.y + pb.h, stroke=C["teal"], sw=1.2, dash="4,3")
    svg.line(x88, pb.y, x88, pb.y + pb.h, stroke=C["teal"], sw=1.2, dash="4,3")
    svg.text((x80 + x88) / 2, pb.py(86.5), "Target", size=13.5, color=C["teal"], weight="bold", anchor="middle")

    x92 = pb.px(92.0)
    svg.line(x92, pb.y, x92, pb.y + pb.h, stroke=C["coral"], sw=1.6, dash="4,3")
    svg.text(x92 + 2, pb.y + 18, "OOM", size=14.5, color=C["coral"], weight="bold", anchor="end")

    u = np.linspace(20.0, 90.0, 140)
    uf = u / 100.0
    r = np.sqrt(uf)
    e_opt = 93.0 / (1.0 + 0.082 / r + 0.042 / uf)
    e_bad = 93.0 / (1.0 + 0.240 / r + 0.065 / uf)
    pb.plot_curve(u, e_opt, stroke=C["teal"], sw=3.0)
    pb.plot_curve(u, e_bad, stroke=C["coral"], sw=2.4, dash="6,4")

    for u_pt, dx_l, dy_l, anc in [(20.0, 10, 18, "start"), (84.0, -6, 20, "end")]:
        v = 93.0 / (1.0 + 0.082 / math.sqrt(u_pt / 100.0) + 0.042 / (u_pt / 100.0))
        svg.circle(pb.px(u_pt), pb.py(v), 5.5, fill=C["teal"], stroke=C["white"], sw=1.4)
        svg.text(pb.px(u_pt) + dx_l, pb.py(v) + dy_l, f"{v:.1f}%", size=14.5, color=C["teal"], weight="bold", anchor=anc)

    svg.text(pb.px(52), pb.py(82.0), "Square Grid P ~ Q + Tuned NB", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb.px(55), pb.py(57.0), "Skewed Grid (e.g. P = 1)", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    svg.rect(514, 520, 400, 96, fill=C["surface_teal"], stroke=C["teal"], sw=1.5, rx=6)
    svg.text(528, 544, "Practical HPL Tuning Checklist", size=15, color=C["teal"], weight="bold")
    svg.multiline(
        528,
        568,
        [
            "1. Size N to 80-88% RAM to amortize O(N^2) communication",
            "2. Reserve ~12% RAM for OS + MPI buffers to prevent swap",
            "3. Choose near-square P <= Q and sweep NB (192-384)",
        ],
        size=14.5,
        color=C["ink2"],
        lh=20,
    )
    svg.save_and_render("m13_hpl_panel_scaling")


def gen_m14_hpcg_spmv_symgs() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "HPCG Sparse Computation & HPL Efficiency Gap",
        "27-point 3D stencil & Multigrid V-Cycle (SymGS) inside PCG vs. ~1.5-4% peak efficiency",
        accent=C["violet"],
    )

    svg.panel_box(28, 86, 452, 546, "27-Point 3D Stencil & PCG Multigrid V-Cycle", accent=C["violet"])
    ox, oy = 148.0, 224.0
    proj = lambda i, j, k: (ox + i * 34.0 - j * 28.0, oy + i * 12.0 + j * 15.0 - k * 34.0)

    for a, b in [
        ((-1, -1, -1), (1, -1, -1)), ((-1, 1, -1), (1, 1, -1)), ((-1, -1, 1), (1, -1, 1)), ((-1, 1, 1), (1, 1, 1)),
        ((-1, -1, -1), (-1, 1, -1)), ((1, -1, -1), (1, 1, -1)), ((-1, -1, 1), (-1, 1, 1)), ((1, -1, 1), (1, 1, 1)),
        ((-1, -1, -1), (-1, -1, 1)), ((1, -1, -1), (1, -1, 1)), ((-1, 1, -1), (-1, 1, 1)), ((1, 1, -1), (1, 1, 1)),
    ]:
        svg.line(*proj(*a), *proj(*b), stroke=C["grid"], sw=1.4)

    cx0, cy0 = proj(0, 0, 0)
    for nb in [(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]:
        svg.line(cx0, cy0, *proj(*nb), stroke=C["blue_l"], sw=2.0)

    pts = sorted([(i + j - k, i, j, k) for i in (-1, 0, 1) for j in (-1, 0, 1) for k in (-1, 0, 1)])
    for _, i, j, k in pts:
        px_v, py_v = proj(i, j, k)
        d = abs(i) + abs(j) + abs(k)
        if d == 0:
            svg.circle(px_v, py_v, 7.0, fill=C["coral"], stroke=C["white"], sw=1.6)
        elif d == 1:
            svg.circle(px_v, py_v, 5.2, fill=C["blue"], stroke=C["white"], sw=1.2)
        else:
            svg.circle(px_v, py_v, 3.8, fill=C["teal"], stroke=C["white"], sw=0.9, opacity=0.85)

    svg.text(244, 156, "27-Point 3D Stencil", size=15.5, color=C["ink"], weight="bold")
    svg.multiline(
        244,
        182,
        [
            "Center (red) + 26 neighbors",
            "27 nonzeros per sparse row",
            "CSR indirect memory gather:",
            "y[i] += val[j] * x[col[j]]",
            "Strided access breaks reuse",
        ],
        size=14.5,
        color=C["ink2"],
        lh=22,
    )

    svg.line(46, 326, 462, 326, stroke=C["grid"], sw=1.4)
    svg.text(48, 352, "Outer PCG Loop + Multigrid (MG) V-Cycle Preconditioner", size=14.8, color=C["violet"], weight="bold")
    svg.rect(56, 366, 396, 28, fill=C["surface_blue"], stroke=C["blue"], sw=1.3, rx=5)
    svg.text(254, 385, "PCG Outer: SpMV + WAXPBY + MPI_Allreduce (DDOT)", size=14.5, color=C["blue"], weight="bold", anchor="middle")

    svg.line(108, 394, 108, 412, stroke=C["blue"], sw=1.8, marker_end="arr_blue")
    svg.line(400, 412, 400, 394, stroke=C["teal"], sw=1.8, marker_end="arr_teal")
    svg.line(128, 456, 154, 479, stroke=C["coral"], sw=2.2, marker_end="arr_coral")
    svg.line(192, 521, 226, 543, stroke=C["coral"], sw=2.2, marker_end="arr_coral")
    svg.line(282, 543, 316, 521, stroke=C["teal"], sw=2.2, marker_end="arr_teal")
    svg.line(354, 479, 380, 456, stroke=C["teal"], sw=2.2, marker_end="arr_teal")

    svg.text(84, 514, "Restrict", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(84, 531, "(downsample)", size=14.5, color=C["muted"], anchor="middle")
    svg.text(422, 514, "Prolong", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(422, 531, "(interpolate)", size=14.5, color=C["muted"], anchor="middle")

    for vx, vy, t1, t2, sc, fc in [
        (108, 434, "Fine (h)", "Pre-SymGS", C["blue"], C["surface_blue"]),
        (170, 500, "Mid (2h)", "SymGS", C["blue_l"], C["white"]),
        (254, 564, "Coarse (4h)", "Coarse Solve", C["violet"], C["surface_violet"]),
        (338, 500, "Mid (2h)", "SymGS", C["blue_l"], C["white"]),
        (400, 434, "Fine (h)", "Post-SymGS", C["teal"], C["surface_teal"]),
    ]:
        nw = 104 if "Coarse" in t1 else 88
        svg.rect(vx - nw / 2, vy - 21, nw, 42, fill=fc, stroke=sc, sw=1.6, rx=6)
        svg.text(vx, vy - 2, t1, size=14.5, color=sc, weight="bold", anchor="middle")
        svg.text(vx, vy + 15, t2, size=14.5, color=C["ink2"], anchor="middle")

    svg.text(254, 616, "SymGS has loop-carried dependencies; needs multi-coloring for GPU", size=14.5, color=C["ink2"], anchor="middle")

    svg.panel_box(496, 86, 436, 546, "Achieved Peak Efficiency: HPL vs. HPCG", accent=C["coral"])
    pb = PlotBox(svg, x=572, y=142, w=338, h=192, xmin=0.08, xmax=120.0, ymin=0.6, ymax=140.0, xlog=True, ylog=True)
    pb.draw_axes(
        xticks=[(0.1, "0.1"), (1, "1"), (10, "10"), (100, "100")],
        yticks=[(1, "1%"), (10, "10%"), (100, "100%")],
        xlabel="Arithmetic Intensity I (FLOP / Byte)",
        ylabel="% FP64 Peak",
    )
    xs = np.logspace(math.log10(0.08), math.log10(120.0), 160)
    pb.plot_curve(xs, np.minimum(100.0, 100.0 * xs / 8.0), stroke=C["slate"], sw=2.6)

    rx = pb.px(8.0)
    svg.line(rx, pb.y, rx, pb.y + pb.h, stroke=C["muted"], sw=1.2, dash="4,3")
    svg.text(rx + 6, pb.y + 20, "I* ~ 8", size=14.5, color=C["muted"], mono=True)

    hx, hy = pb.px(45.0), pb.py(80.0)
    svg.circle(hx, hy, 6.5, fill=C["teal"], stroke=C["white"], sw=1.5)
    svg.rect(hx - 134, hy + 14, 140, 36, fill=C["surface_teal"], stroke=C["teal"], sw=1.2, rx=4)
    svg.text(hx - 64, hy + 29, "HPL ~75-85%", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(hx - 64, hy + 44, "Dense DGEMM", size=14.5, color=C["ink2"], anchor="middle")

    cx_p, cy_p = pb.px(0.25), pb.py(2.4)
    svg.circle(cx_p, cy_p, 6.5, fill=C["coral"], stroke=C["white"], sw=1.5)
    svg.rect(cx_p + 12, cy_p - 28, 156, 36, fill=C["surface_coral"], stroke=C["coral"], sw=1.2, rx=4)
    svg.text(cx_p + 90, cy_p - 12, "HPCG ~1.5-4%", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    svg.text(cx_p + 90, cy_p + 3, "I ~ 0.25 FLOP/B", size=14.5, color=C["ink2"], anchor="middle")

    svg.text(516, 404, "Linear-Scale Gap (25-40x Lower Peak Fraction)", size=14.8, color=C["ink"], weight="bold")
    bx0_b, bfull = 584.0, 212.0
    svg.text(bx0_b - 10, 434, "HPL", size=14.5, color=C["teal"], weight="bold", anchor="end")
    svg.rect(bx0_b, 416, bfull, 24, fill=C["surface"], stroke=C["grid"], sw=1.0, rx=3)
    svg.rect(bx0_b, 416, bfull * 0.80, 24, fill=C["teal"], rx=3)
    svg.text(bx0_b + bfull + 10, 433, "75-85% peak", size=14.5, color=C["teal"], weight="bold")
    svg.text(bx0_b - 10, 468, "HPCG", size=14.5, color=C["coral"], weight="bold", anchor="end")
    svg.rect(bx0_b, 450, bfull, 24, fill=C["surface"], stroke=C["grid"], sw=1.0, rx=3)
    svg.rect(bx0_b, 450, max(8.0, bfull * 0.03), 24, fill=C["coral"], rx=2)
    svg.text(bx0_b + bfull + 10, 467, "1.5-4% peak", size=14.5, color=C["coral"], weight="bold")

    svg.rect(514, 492, 400, 126, fill=C["surface_coral"], stroke=C["coral"], sw=1.5, rx=6)
    svg.text(528, 516, "Three Root Causes of HPCG Efficiency Ceiling", size=15, color=C["coral"], weight="bold")
    svg.multiline(
        528,
        542,
        [
            "1. Tiny arithmetic intensity: I ~ 0.25 FLOP/B (BW-bound)",
            "2. Indirect CSR indexing (x[col[j]]) hurts cache locality",
            "3. Global MPI_Allreduce barrier on every DDOT inner product",
        ],
        size=14.5,
        color=C["ink2"],
        lh=24,
    )
    svg.save_and_render("m14_hpcg_spmv_symgs")


def gen_m15_power_wall_dvfs() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "Power Wall, CMOS DVFS Sweet Spot & ASC Power Caps",
        "Cubic dynamic power vs. frequency scaling, plus historical ASC limits and ASC27 presets",
        accent=C["gold"],
    )

    svg.panel_box(28, 86, 452, 546, "CMOS DVFS Normalized Curves (f in [0.5, 1.0])", accent=C["blue"])
    pb = PlotBox(svg, x=98, y=148, w=358, h=304, xmin=0.50, xmax=1.02, ymin=0.0, ymax=2.08)
    pb.draw_axes(
        xticks=[(0.5, "0.5"), (0.6, "0.6"), (0.7, "0.7"), (0.8, "0.8"), (0.9, "0.9"), (1.0, "1.0")],
        yticks=[(0.0, "0.0"), (0.5, "0.5"), (1.0, "1.0"), (1.5, "1.5"), (2.0, "2.0")],
        xlabel="Normalized Frequency f / f_max",
        ylabel="Normalized Value (Ratio)",
    )

    xs1, xs2 = pb.px(0.75), pb.px(0.82)
    svg.rect(xs1, pb.y, xs2 - xs1, pb.h, fill=C["surface_gold"], stroke="none")
    svg.line(xs1, pb.y, xs1, pb.y + pb.h, stroke=C["gold"], sw=1.4, dash="4,3")
    svg.line(xs2, pb.y, xs2, pb.y + pb.h, stroke=C["gold"], sw=1.4, dash="4,3")
    svg.rect(xs1 - 46, pb.y + 6, 142, 38, fill=C["white"], stroke=C["gold"], sw=1.2, rx=4)
    svg.text((xs1 + xs2) / 2, pb.y + 22, "DVFS Sweet Spot", size=14.5, color=C["gold"], weight="bold", anchor="middle")
    svg.text((xs1 + xs2) / 2, pb.y + 38, "0.75-0.82 f_max", size=14.5, color=C["ink2"], anchor="middle", mono=True)

    f = np.linspace(0.50, 1.00, 150)
    p_f = 0.15 + 0.85 * (f ** 3)
    r_f = f
    eff = r_f / p_f
    pb.plot_curve(f, eff, stroke=C["teal"], sw=3.0)
    pb.plot_curve(f, r_f, stroke=C["blue"], sw=2.8)
    pb.plot_curve(f, p_f, stroke=C["coral"], sw=3.0)

    f_m = 0.78
    p_m = 0.15 + 0.85 * (f_m ** 3)
    for val, col in [(f_m / p_m, C["teal"]), (f_m, C["blue"]), (p_m, C["coral"])]:
        svg.circle(pb.px(f_m), pb.py(val), 5.5, fill=col, stroke=C["white"], sw=1.4)
    svg.circle(pb.px(1.0), pb.py(1.0), 5.0, fill=C["slate"], stroke=C["white"], sw=1.4)

    svg.text(pb.px(0.92), pb.py(1.40), "Efficiency R/P", size=14.5, color=C["teal"], weight="bold", anchor="middle")
    svg.text(pb.px(0.61), pb.py(0.84), "Perf R(f) = f", size=14.5, color=C["blue"], weight="bold", anchor="middle")
    svg.text(pb.px(0.67), pb.py(0.14), "Power P(f) = 0.15 + 0.85f^3", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    svg.rect(46, 514, 416, 102, fill=C["surface_blue"], stroke=C["blue"], sw=1.4, rx=6)
    svg.text(60, 538, "Sweet-Spot Quantitative Gain (f = 0.78 f_max)", size=14.5, color=C["blue"], weight="bold")
    svg.multiline(
        60,
        562,
        [
            "Power drops sharply: P(0.78) = 0.55 (-45% power)",
            "Performance holds: R(0.78) = 0.78 (-22% clock)",
            "Perf/Watt rises 1.41x: run more nodes under fixed cap",
        ],
        size=14.5,
        color=C["ink2"],
        lh=21,
    )

    svg.panel_box(496, 86, 436, 546, "Historical ASC Power Caps & ASC27 Presets", accent=C["gold"])
    pb2 = PlotBox(svg, x=562, y=156, w=348, h=290, xmin=0.0, xmax=4.2, ymin=0.0, ymax=6.4)
    pb2.draw_axes(
        xticks=[],
        yticks=[(0, "0"), (1, "1"), (2, "2"), (3, "3"), (4, "4"), (5, "5"), (6, "6")],
        ylabel="Cluster Power Cap (kW)",
    )

    stack_cols = [C["blue"], C["teal"], C["slate"], C["gold"]]
    bw2 = 60.0
    for cx_v, lbl, top_lbl, vals in [
        (0.52, "ASC22", "3.0 kW", [1.65, 0.55, 0.50, 0.30]),
        (1.52, "ASC25", "4.0 kW", [2.30, 0.70, 0.60, 0.40]),
        (2.52, "ASC26", "5.0 kW", [2.95, 0.85, 0.70, 0.50]),
    ]:
        bx = pb2.px(cx_v) - bw2 / 2
        acc = 0.0
        for sv, col in zip(vals, stack_cols):
            yt = pb2.py(acc + sv)
            svg.rect(bx, yt, bw2, pb2.py(acc) - yt, fill=col, stroke=C["white"], sw=1.0)
            acc += sv
        svg.text(pb2.px(cx_v), pb2.py(acc) - 8, top_lbl, size=14.5, color=C["ink"], weight="bold", anchor="middle")
        svg.text(pb2.px(cx_v), pb2.y + pb2.h + 22, lbl, size=14.5, color=C["ink"], weight="bold", anchor="middle")

    svg.rect(pb2.px(1.50), pb2.py(6.30), 166, 26, fill=C["surface_coral"], stroke=C["coral"], sw=1.1, rx=4)
    svg.text(pb2.px(1.50) + 83, pb2.py(6.30) + 17, "<=2 kW/node, >=3 nodes", size=14.5, color=C["coral"], weight="bold", anchor="middle")
    svg.line(pb2.px(2.52), pb2.py(5.72), pb2.px(2.52), pb2.py(5.48), stroke=C["coral"], sw=1.4)

    bx27 = pb2.px(3.62) - bw2 / 2
    svg.rect(bx27, pb2.py(5.0), bw2, pb2.py(0.0) - pb2.py(5.0), fill=C["surface_violet"], stroke=C["violet"], sw=1.8, rx=4, dash="5,3")
    for tier in (3.0, 4.0, 5.0):
        yt = pb2.py(tier)
        svg.line(bx27, yt, bx27 + bw2, yt, stroke=C["violet"], sw=1.3, dash="3,2")
        svg.text(bx27 + bw2 / 2, yt + 16, f"{int(tier)} kW?", size=14.5, color=C["violet"], weight="bold", anchor="middle")
    svg.text(pb2.px(3.62), pb2.py(5.55), "Official TBD", size=14.5, color=C["violet"], weight="bold", anchor="middle")
    svg.text(pb2.px(3.62), pb2.py(5.16), "3/4/5 kW Tests", size=14.5, color=C["violet"], anchor="middle")
    svg.text(pb2.px(3.62), pb2.y + pb2.h + 22, "ASC27 TBD", size=14.5, color=C["violet"], weight="bold", anchor="middle")

    for lbl, col, lx in [("GPU", C["blue"], 514), ("CPU", C["teal"], 582), ("Sys + IB", C["slate"], 650), ("Margin ~10%", C["gold"], 750)]:
        svg.rect(lx, 490, 14, 14, fill=col, rx=2)
        svg.text(lx + 20, 502, lbl, size=14.5, color=C["ink2"])

    svg.rect(514, 522, 400, 94, fill=C["surface_gold"], stroke=C["gold"], sw=1.5, rx=6)
    svg.text(528, 545, "Power-Meter Compliance Playbook", size=14.8, color=C["gold"], weight="bold")
    svg.multiline(
        528,
        569,
        [
            "1. Cap GPUs via nvidia-smi -pl; keep ~10% safety headroom",
            "2. Separate official ASC27 rules from historical baselines",
            "3. Pre-validate 3 / 4 / 5 kW automated profile presets",
        ],
        size=14.5,
        color=C["ink2"],
        lh=20,
    )
    svg.save_and_render("m15_power_wall_dvfs")


def gen_m16_asc_workflow_scoring() -> None:
    svg = SVGCanvas(960, 660)
    svg.header(
        "ASC Finals 48h Workflow & Historical Scoring Weights",
        "Five-stage regression loop & ASC26 100-point split (historical reference; ASC27 rules TBD)",
        accent=C["blue"],
    )

    svg.panel_box(28, 86, 904, 246, "ASC Finals 48-Hour Execution & Regression Loop", accent=C["blue"])
    pipe = [
        ("01", "CPU Reference", "0-4h", C["slate"], C["surface"], ["Lock reference output", "Measure baseline time", "Build auto-diff script"]),
        ("02", "Profile", "4-10h", C["blue"], C["surface_blue"], ["Nsight / Score-P trace", "Split compute vs. copy", "Pinpoint real hotspot"]),
        ("03", "Optimize", "10-32h", C["teal"], C["surface_teal"], ["GPU-resident + async", "Kernel & MPI tuning", "Small verified commits"]),
        ("04", "Accuracy Gate", "32-42h", C["violet"], C["surface_violet"], ["Full long-step runs", "Check conservation", "Zero tolerance pass"]),
        ("05", "Power & Q&A", "42-48h", C["gold"], C["surface_gold"], ["Live meter peak soak", "Lock safety headroom", "Poster & jury Q&A"]),
    ]
    cw, cgap, cx0, cy0, ch = 154.0, 25.0, 44.0, 136.0, 142.0
    for idx, (num, title, hrs, col, bgc, bullets) in enumerate(pipe):
        cx = cx0 + idx * (cw + cgap)
        svg.rect(cx, cy0, cw, ch, fill=bgc, stroke=col, sw=1.6, rx=7)
        svg.rect(cx, cy0, cw, 28, fill=col, rx=6)
        svg.rect(cx, cy0 + 20, cw, 8, fill=col)
        svg.text(cx + 10, cy0 + 20, num, size=14.5, color=C["white"], weight="bold", mono=True)
        svg.text(cx + cw - 10, cy0 + 19, hrs, size=14.5, color=C["white"], anchor="end", mono=True)
        svg.text(cx + cw / 2, cy0 + 50, title, size=15, color=C["ink"], weight="bold", anchor="middle")
        svg.multiline(cx + 11, cy0 + 74, bullets, size=14.5, color=C["ink2"], lh=21)
        if idx < 4:
            svg.line(cx + cw + 3, cy0 + ch / 2, cx + cw + cgap - 3, cy0 + ch / 2, stroke=C["slate"], sw=2.2, marker_end="arr")

    x_s3 = cx0 + 2 * (cw + cgap) + cw / 2
    x_s4 = cx0 + 3 * (cw + cgap) + cw / 2
    x_s5 = cx0 + 4 * (cw + cgap) + cw / 2
    y_bot, y_loop = cy0 + ch, 308.0
    svg.line(x_s5, y_bot, x_s5, y_loop, stroke=C["coral"], sw=1.8, dash="5,3")
    svg.line(x_s4, y_bot, x_s4, y_loop, stroke=C["coral"], sw=1.8, dash="5,3")
    svg.line(x_s5, y_loop, x_s3, y_loop, stroke=C["coral"], sw=1.8, dash="5,3")
    svg.line(x_s3, y_loop, x_s3, y_bot + 3, stroke=C["coral"], sw=1.8, dash="5,3", marker_end="arr_coral")
    svg.rect(x_s3 + 60, y_loop - 12, 316, 22, fill=C["white"], stroke=C["coral"], sw=1.1, rx=4)
    svg.text(x_s3 + 218, y_loop + 4, "Failed Accuracy or Power Cap -> Roll Back & Retune", size=14.5, color=C["coral"], weight="bold", anchor="middle")

    svg.panel_box(28, 346, 904, 286, "ASC26 Finals 100-Point Distribution (Historical Baseline)", accent=C["teal"])
    bx0, tot_w, by0, bh = 52.0, 856.0, 424.0, 56.0
    items = [
        ("ICON", 8, C["blue_l"]),
        ("HPL", 5, C["slate"]),
        ("HPCG", 5, "#64748B"),
        ("UnifoLM", 18, C["violet"]),
        ("AMSS-NCKU", 18, C["blue"]),
        ("QiboTN", 18, C["teal"]),
        ("Mystery LeWM", 18, C["coral"]),
        ("Pres.", 10, C["gold"]),
    ]
    cur_x, bounds = bx0, []
    for name, pts, col in items:
        sw = tot_w * pts / 100.0
        svg.rect(cur_x, by0, sw, bh, fill=col, stroke=C["white"], sw=1.4, rx=3)
        fs = 12.2 if pts == 5 else (14.0 if pts <= 10 else 15.0)
        svg.text(cur_x + sw / 2, by0 + 25, name, size=fs, color=C["white"], weight="bold", anchor="middle")
        svg.text(cur_x + sw / 2, by0 + 45, f"{pts} pts" if pts >= 8 else f"{pts}", size=14.5, color=C["white"], weight="bold", anchor="middle")
        bounds.append((cur_x, cur_x + sw))
        cur_x += sw

    draw_bracket_h(svg, bounds[0][0] + 2, bounds[2][1] - 2, by0 - 10, tick=7, stroke=C["slate"], sw=1.6)
    svg.text((bounds[0][0] + bounds[2][1]) / 2, by0 - 18, "Group + Bench (18)", size=14.5, color=C["slate"], weight="bold", anchor="middle")
    draw_bracket_h(svg, bounds[3][0] + 2, bounds[6][1] - 2, by0 - 10, tick=7, stroke=C["blue"], sw=2.0)
    svg.text((bounds[3][0] + bounds[6][1]) / 2, by0 - 18, "Four Core Applications (72 pts total · 18 pts each)", size=14.8, color=C["blue"], weight="bold", anchor="middle")
    draw_bracket_h(svg, bounds[7][0] + 2, bounds[7][1] - 2, by0 - 10, tick=7, stroke=C["gold"], sw=1.6)
    svg.text((bounds[7][0] + bounds[7][1]) / 2, by0 - 18, "Q&A (10)", size=14.5, color=C["gold"], weight="bold", anchor="middle")

    for tp in [0, 8, 18, 36, 54, 72, 90, 100]:
        tx = bx0 + tot_w * tp / 100.0
        svg.line(tx, by0 + bh, tx, by0 + bh + 6, stroke=C["axis"], sw=1.2)
        svg.text(tx, by0 + bh + 21, f"{tp}", size=14.5, color=C["muted"], anchor="middle")

    svg.rect(52, 514, 476, 100, fill=C["surface_blue"], stroke=C["blue"], sw=1.5, rx=6)
    svg.text(68, 538, "Normalized Relative Scoring Formula (ASC Convention)", size=14.8, color=C["blue"], weight="bold")
    svg.text(68, 566, "Total = Sum w_i * (Perf_team,i / Perf_best,i) + S_pres", size=14.5, color=C["ink"], weight="bold", mono=True)
    svg.text(68, 594, "Missing an accuracy gate or exceeding power voids that task score", size=14.5, color=C["ink2"])

    svg.rect(544, 514, 364, 100, fill=C["surface_gold"], stroke=C["gold"], sw=1.5, rx=6)
    svg.text(560, 538, "ASC27 Preparation Takeaways", size=14.8, color=C["gold"], weight="bold")
    svg.multiline(
        560,
        562,
        [
            "1. Core apps carry 72%: balanced passes beat one hero run",
            "2. HPL/HPCG (10 pts) rapidly validate cluster stability",
            "3. Note: Official ASC27 tasks & weights are TBD",
        ],
        size=14.5,
        color=C["ink2"],
        lh=20,
    )
    svg.save_and_render("m16_asc_workflow_scoring")


def main() -> None:
    for fn in [
        gen_m08_timeline_profiling,
        gen_m09_transformer_memory_precision,
        gen_m10_distributed_training_ring,
        gen_m11_llm_inference_kv_denoising,
        gen_m12_amss_bottleneck_shift,
        gen_m13_hpl_panel_scaling,
        gen_m14_hpcg_spmv_symgs,
        gen_m15_power_wall_dvfs,
        gen_m16_asc_workflow_scoring,
    ]:
        fn()
        print(f"Generated {fn.__name__}")


if __name__ == "__main__":
    main()
