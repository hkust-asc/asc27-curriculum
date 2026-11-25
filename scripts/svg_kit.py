#!/usr/bin/env python3
"""Minimalist SVG plotting & schematic drawing toolkit for HKUST ASC27 curriculum."""

from __future__ import annotations

import math
import subprocess
from pathlib import Path
from typing import Iterable, List, Optional, Sequence, Tuple
from xml.sax.saxutils import escape

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SVG_DIR = ROOT / "diagrams" / "svg"
PNG_DIR = ROOT / "diagrams" / "png"

C = {
    "bg": "#FAFAFA",
    "white": "#FFFFFF",
    "surface": "#F4F4F5",
    "surface_blue": "#EFF6FF",
    "surface_teal": "#F0FDFA",
    "surface_coral": "#FFF7ED",
    "surface_gold": "#FEFCE8",
    "surface_violet": "#F5F3FF",
    "ink": "#171717",
    "ink2": "#525252",
    "muted": "#737373",
    "grid": "#EBEBEB",
    "axis": "#A3A3A3",
    "blue": "#0B4F8A",
    "blue_l": "#3B82F6",
    "gold": "#C48A1A",
    "teal": "#0D9488",
    "coral": "#C2410C",
    "violet": "#6D28D9",
    "slate": "#525252",
}

FONT_SANS = "Inter, Helvetica Neue, Arial, sans-serif"
FONT_MONO = "SF Mono, Menlo, DejaVu Sans Mono, monospace"


def esc(s: str) -> str:
    return escape(str(s), {"'": "&apos;", '"': "&quot;"})


class SVGCanvas:
    def __init__(self, width: int = 960, height: int = 660, bg: str = C["bg"]):
        self.w = width
        self.h = height
        self.bg = bg
        self.defs: List[str] = []
        self.els: List[str] = []
        self._add_default_markers()

    def _add_default_markers(self) -> None:
        for name, color in [
            ("arr", C["slate"]),
            ("arr_blue", C["blue"]),
            ("arr_teal", C["teal"]),
            ("arr_coral", C["coral"]),
            ("arr_gold", C["gold"]),
            ("arr_violet", C["violet"]),
            ("arr_muted", C["muted"]),
        ]:
            self.defs.append(
                f'<marker id="{name}" viewBox="0 0 10 10" refX="8.5" refY="5" '
                f'markerWidth="7" markerHeight="7" orient="auto-start-reverse">'
                f'<path d="M 1 1.5 L 9 5 L 1 8.5 z" fill="{color}"/></marker>'
            )

    def add(self, raw: str) -> None:
        self.els.append(raw)

    def rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: str = C["white"],
        stroke: str = "none",
        sw: float = 1.5,
        rx: float = 0,
        dash: str = "",
        opacity: float = 1.0,
    ) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        op = f' opacity="{opacity}"' if opacity < 1.0 else ""
        self.els.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{w:.1f}" height="{h:.1f}" '
            f'rx="{rx:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{op}/>'
        )

    def circle(
        self, cx: float, cy: float, r: float, fill: str = C["blue"], stroke: str = "none", sw: float = 1.5, opacity: float = 1.0
    ) -> None:
        op = f' opacity="{opacity}"' if opacity < 1.0 else ""
        self.els.append(
            f'<circle cx="{cx:.1f}" cy="{cy:.1f}" r="{r:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{op}/>'
        )

    def ellipse(
        self, cx: float, cy: float, rx: float, ry: float, fill: str = "none", stroke: str = C["blue"], sw: float = 1.5, dash: str = ""
    ) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.els.append(
            f'<ellipse cx="{cx:.1f}" cy="{cy:.1f}" rx="{rx:.1f}" ry="{ry:.1f}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}/>'
        )

    def line(
        self,
        x1: float,
        y1: float,
        x2: float,
        y2: float,
        stroke: str = C["slate"],
        sw: float = 1.8,
        dash: str = "",
        marker_end: str = "",
        marker_start: str = "",
    ) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{marker_end})"' if marker_end else ""
        ms = f' marker-start="url(#{marker_start})"' if marker_start else ""
        self.els.append(
            f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" '
            f'stroke="{stroke}" stroke-width="{sw}"{d}{ms}{me}/>'
        )

    def polyline(
        self,
        pts: Sequence[Tuple[float, float]],
        stroke: str = C["blue"],
        sw: float = 2.6,
        fill: str = "none",
        dash: str = "",
    ) -> None:
        pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        d = f' stroke-dasharray="{dash}"' if dash else ""
        self.els.append(
            f'<polyline points="{pstr}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}" '
            f'stroke-linejoin="round" stroke-linecap="round"{d}/>'
        )

    def polygon(
        self,
        pts: Sequence[Tuple[float, float]],
        fill: str = C["surface_blue"],
        stroke: str = "none",
        sw: float = 1.2,
        opacity: float = 1.0,
    ) -> None:
        pstr = " ".join(f"{x:.1f},{y:.1f}" for x, y in pts)
        op = f' opacity="{opacity}"' if opacity < 1.0 else ""
        self.els.append(f'<polygon points="{pstr}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{op}/>')

    def path(
        self,
        d_str: str,
        stroke: str = C["slate"],
        sw: float = 1.8,
        fill: str = "none",
        dash: str = "",
        marker_end: str = "",
    ) -> None:
        d = f' stroke-dasharray="{dash}"' if dash else ""
        me = f' marker-end="url(#{marker_end})"' if marker_end else ""
        self.els.append(f'<path d="{d_str}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"{d}{me}/>')

    def text(
        self,
        x: float,
        y: float,
        s: str,
        size: float = 16,
        color: str = C["ink"],
        weight: str = "normal",
        anchor: str = "start",
        mono: bool = False,
        rotate: Optional[float] = None,
    ) -> None:
        ff = FONT_MONO if mono else FONT_SANS
        tf = f' transform="rotate({rotate:.1f} {x:.1f} {y:.1f})"' if rotate is not None else ""
        self.els.append(
            f'<text x="{x:.1f}" y="{y:.1f}" font-family="{ff}" font-size="{size}" '
            f'font-weight="{weight}" fill="{color}" text-anchor="{anchor}"{tf}>{esc(s)}</text>'
        )

    def multiline(
        self,
        x: float,
        y: float,
        lines: Sequence[str],
        size: float = 15,
        color: str = C["ink2"],
        weight: str = "normal",
        anchor: str = "start",
        lh: float = 21,
        mono: bool = False,
    ) -> None:
        for i, ln in enumerate(lines):
            self.text(x, y + i * lh, ln, size=size, color=color, weight=weight, anchor=anchor, mono=mono)

    def header(self, title: str, subtitle: str = "", accent: str = C["blue"]) -> None:
        self.rect(28, 22, 6, 36 if subtitle else 28, fill=accent, rx=2)
        self.text(44, 44, title, size=22, color=C["ink"], weight="bold")
        if subtitle:
            self.text(44, 66, subtitle, size=14.5, color=C["muted"])

    def panel_box(self, x: float, y: float, w: float, h: float, title: str = "", accent: str = C["blue"]) -> None:
        self.rect(x, y, w, h, fill=C["white"], stroke=C["grid"], sw=1.4, rx=8)
        if title:
            self.rect(x, y, w, 34, fill=C["surface"], stroke=C["grid"], sw=1.0, rx=8)
            self.rect(x, y + 26, w, 8, fill=C["surface"])
            self.line(x, y + 34, x + w, y + 34, stroke=C["grid"], sw=1.0)
            self.rect(x + 12, y + 9, 4, 16, fill=accent, rx=2)
            self.text(x + 24, y + 23, title, size=15.5, color=C["ink"], weight="bold")

    def node_box(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        title: str,
        subtitle: str = "",
        fill: str = C["white"],
        stroke: str = C["blue"],
        title_color: str = C["ink"],
        bar_color: Optional[str] = None,
    ) -> None:
        self.rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.6, rx=6)
        if bar_color:
            self.rect(x, y, 5, h, fill=bar_color, rx=2)
        if subtitle:
            self.text(x + w / 2, y + h * 0.43, title, size=15.5, color=title_color, weight="bold", anchor="middle")
            self.text(x + w / 2, y + h * 0.76, subtitle, size=13.5, color=C["muted"], anchor="middle")
        else:
            self.text(x + w / 2, y + h * 0.60, title, size=15.5, color=title_color, weight="bold", anchor="middle")

    def save_and_render(self, name: str, png_width: int = 1800) -> Path:
        SVG_DIR.mkdir(parents=True, exist_ok=True)
        PNG_DIR.mkdir(parents=True, exist_ok=True)
        svg_path = SVG_DIR / f"{name}.svg"
        png_path = PNG_DIR / f"{name}.png"
        xml = (
            f'<svg xmlns="http://www.w3.org/2000/svg" width="{self.w}" height="{self.h}" '
            f'viewBox="0 0 {self.w} {self.h}">\n'
            f"  <defs>\n"
            + "\n".join(f"    {d}" for d in self.defs)
            + "\n  </defs>\n"
            f'  <rect width="{self.w}" height="{self.h}" fill="{self.bg}"/>\n'
            + "\n".join(f"  {e}" for e in self.els)
            + "\n</svg>\n"
        )
        svg_path.write_text(xml, encoding="utf-8")
        subprocess.run(
            ["rsvg-convert", "-d", "300", "-p", "300", "-w", str(png_width), str(svg_path), "-o", str(png_path)],
            check=True,
        )
        return png_path


class PlotBox:
    """Exact coordinate mapper for linear / log plots inside SVGCanvas."""

    def __init__(
        self,
        svg: SVGCanvas,
        x: float,
        y: float,
        w: float,
        h: float,
        xmin: float,
        xmax: float,
        ymin: float,
        ymax: float,
        xlog: bool = False,
        ylog: bool = False,
    ):
        self.svg = svg
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.xmin = xmin
        self.xmax = xmax
        self.ymin = ymin
        self.ymax = ymax
        self.xlog = xlog
        self.ylog = ylog

    def px(self, vx: float) -> float:
        if self.xlog:
            t = (math.log10(vx) - math.log10(self.xmin)) / (math.log10(self.xmax) - math.log10(self.xmin))
        else:
            t = (vx - self.xmin) / (self.xmax - self.xmin)
        return self.x + t * self.w

    def py(self, vy: float) -> float:
        if self.ylog:
            t = (math.log10(vy) - math.log10(self.ymin)) / (math.log10(self.ymax) - math.log10(self.ymin))
        else:
            t = (vy - self.ymin) / (self.ymax - self.ymin)
        return self.y + self.h - t * self.h

    def draw_axes(
        self,
        xticks: Sequence[Tuple[float, str]],
        yticks: Sequence[Tuple[float, str]],
        xlabel: str = "",
        ylabel: str = "",
    ) -> None:
        self.svg.rect(self.x, self.y, self.w, self.h, fill=C["white"], stroke="none")
        for vx, lbl in xticks:
            gx = self.px(vx)
            self.svg.line(gx, self.y, gx, self.y + self.h, stroke=C["grid"], sw=1.0)
            self.svg.line(gx, self.y + self.h, gx, self.y + self.h + 5, stroke=C["axis"], sw=1.4)
            self.svg.text(gx, self.y + self.h + 22, lbl, size=13.5, color=C["muted"], anchor="middle")
        for vy, lbl in yticks:
            gy = self.py(vy)
            self.svg.line(self.x, gy, self.x + self.w, gy, stroke=C["grid"], sw=1.0)
            self.svg.line(self.x - 5, gy, self.x, gy, stroke=C["axis"], sw=1.4)
            self.svg.text(self.x - 10, gy + 5, lbl, size=13.5, color=C["muted"], anchor="end")
        self.svg.line(self.x, self.y + self.h, self.x + self.w, self.y + self.h, stroke=C["slate"], sw=1.8)
        self.svg.line(self.x, self.y, self.x, self.y + self.h, stroke=C["slate"], sw=1.8)
        if xlabel:
            self.svg.text(self.x + self.w / 2, self.y + self.h + 46, xlabel, size=15, color=C["ink2"], weight="bold", anchor="middle")
        if ylabel:
            self.svg.text(self.x - 54, self.y + self.h / 2, ylabel, size=15, color=C["ink2"], weight="bold", anchor="middle", rotate=-90)

    def plot_curve(
        self,
        xs: Iterable[float],
        ys: Iterable[float],
        stroke: str = C["blue"],
        sw: float = 2.8,
        dash: str = "",
    ) -> None:
        pts = []
        for vx, vy in zip(xs, ys):
            if self.xmin <= vx <= self.xmax and self.ymin <= vy <= self.ymax:
                pts.append((self.px(vx), self.py(vy)))
        if len(pts) >= 2:
            self.svg.polyline(pts, stroke=stroke, sw=sw, dash=dash)
