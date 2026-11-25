#!/usr/bin/env python3
"""
Minimalist Native LibreOffice Impress (.odp) Presentation Builder
Generates strict ODF 1.2 .odp files optimized for LibreOffice 26.x rendering,
PDF export, and clean PPTX round-trip conversion.
"""

from __future__ import annotations

import os
import subprocess
import tempfile
import zipfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import List, Optional, Tuple
from xml.sax.saxutils import escape as xml_escape

from PIL import Image

from formula_render import render_formula_png


# Minimalist Academic HPC Palette (HKUST-inspired)
PALETTE = {
    "bg": "#FFFFFF",
    "bg_cover": "#0B2545",
    "bg_divider": "#0F172A",
    "surface": "#F8FAFC",
    "surface_alt": "#F1F5F9",
    "border": "#E2E8F0",
    "ink": "#0F172A",
    "ink_secondary": "#334155",
    "ink_muted": "#64748B",
    "accent": "#0B4F8A",       # Deep HPC Blue
    "gold": "#C48A1A",         # HKUST Gold
    "teal": "#0D9488",         # Compute / Optimal
    "coral": "#C2410C",        # Bottleneck / Alert
    "violet": "#6D28D9",       # AI / Quantum
    "white": "#FFFFFF",
    "light_text": "#CBD5E1",
}


def esc(text: str) -> str:
    return xml_escape(text, {"'": "&apos;", '"': "&quot;"})


@dataclass
class SlideSpec:
    kind: str  # "cover", "divider", "content_visual", "full_visual", "table", "two_col", "problem"
    title: str
    subtitle: str = ""
    section_tag: str = ""
    bullets: List[str] = field(default_factory=list)
    formula: str = ""
    formula_tex: str = ""
    formula_caption: str = ""
    image_path: Optional[str] = None
    image_caption: str = ""
    table_headers: List[str] = field(default_factory=list)
    table_rows: List[List[str]] = field(default_factory=list)
    table_col_widths_cm: List[float] = field(default_factory=list)
    left_title: str = ""
    left_bullets: List[str] = field(default_factory=list)
    right_title: str = ""
    right_bullets: List[str] = field(default_factory=list)
    callout: str = ""
    footnote: str = ""
    speaker_notes: str = ""
    accent_color: str = PALETTE["accent"]
    problem_dims: List[Tuple[str, str]] = field(default_factory=list)
    problem_meta: str = ""


class ODPDeck:
    """Native ODF 1.2 Presentation (.odp) generator for LibreOffice Impress."""

    PAGE_W = 33.867  # 16:9 widescreen in cm (13.333 in)
    PAGE_H = 19.050  # 16:9 widescreen in cm (7.500 in)

    def __init__(self, title: str, author: str = "HKUST ASC Team", deck_code: str = ""):
        self.title = title
        self.author = author
        self.deck_code = deck_code
        self.slides: List[SlideSpec] = []
        self._images: dict[str, Tuple[str, bytes]] = {}
        self._img_counter = 0
        self._style_counter = 0
        self._auto_styles: List[str] = []

    def add_slide(self, slide: SlideSpec) -> None:
        self.slides.append(slide)

    def _next_style(self, prefix: str) -> str:
        self._style_counter += 1
        return f"{prefix}_{self._style_counter}"

    def _register_image(self, path: str) -> Tuple[str, int, int]:
        abs_path = str(Path(path).resolve())
        if not os.path.exists(abs_path):
            raise FileNotFoundError(f"Slide image not found: {abs_path}")
        with Image.open(abs_path) as im:
            w_px, h_px = im.size
        if abs_path not in self._images:
            self._img_counter += 1
            ext = Path(abs_path).suffix.lower().lstrip(".") or "png"
            zip_name = f"Pictures/img_{self._img_counter:03d}.{ext}"
            with open(abs_path, "rb") as f:
                self._images[abs_path] = (zip_name, f.read())
        return self._images[abs_path][0], w_px, h_px

    def _fit_image_box(
        self, box_x: float, box_y: float, box_w: float, box_h: float, w_px: int, h_px: int
    ) -> Tuple[float, float, float, float]:
        """Letterbox-fit image cleanly inside target box without distortion."""
        img_ratio = w_px / max(h_px, 1)
        box_ratio = box_w / max(box_h, 0.01)
        if img_ratio > box_ratio:
            w = box_w
            h = box_w / img_ratio
        else:
            h = box_h
            w = box_h * img_ratio
        x = box_x + (box_w - w) / 2.0
        y = box_y + (box_h - h) / 2.0
        return x, y, w, h

    def _make_rect_style(
        self,
        fill_color: Optional[str] = None,
        stroke_color: Optional[str] = None,
        stroke_width: str = "0.03cm",
        pad_lr: str = "0.25cm",
        pad_tb: str = "0.18cm",
        v_align: str = "top",
    ) -> str:
        name = self._next_style("gr")
        fill_attr = f'draw:fill="solid" draw:fill-color="{fill_color}"' if fill_color else 'draw:fill="none"'
        stroke_attr = (
            f'draw:stroke="solid" svg:stroke-color="{stroke_color}" svg:stroke-width="{stroke_width}"'
            if stroke_color
            else 'draw:stroke="none"'
        )
        self._auto_styles.append(
            f'<style:style style:name="{name}" style:family="graphic">'
            f'<style:graphic-properties {stroke_attr} {fill_attr} '
            f'fo:padding-left="{pad_lr}" fo:padding-right="{pad_lr}" '
            f'fo:padding-top="{pad_tb}" fo:padding-bottom="{pad_tb}" '
            f'draw:textarea-vertical-align="{v_align}"/>'
            f"</style:style>"
        )
        return name

    def _make_text_style(
        self,
        size_pt: float,
        color: str,
        bold: bool = False,
        italic: bool = False,
        mono: bool = False,
    ) -> str:
        name = self._next_style("T")
        latin = "Menlo" if mono else "Helvetica Neue"
        asian = "Helvetica Neue"
        wt = "bold" if bold else "normal"
        st = "italic" if italic else "normal"
        self._auto_styles.append(
            f'<style:style style:name="{name}" style:family="text">'
            f'<style:text-properties fo:font-family="{latin}" style:font-family-asian="{asian}" '
            f'fo:font-size="{size_pt}pt" style:font-size-asian="{size_pt}pt" '
            f'fo:font-weight="{wt}" style:font-weight-asian="{wt}" '
            f'fo:font-style="{st}" style:font-style-asian="{st}" '
            f'fo:color="{color}"/>'
            f"</style:style>"
        )
        return name

    def _make_para_style(
        self,
        align: str = "start",
        space_after: str = "0.22cm",
        space_before: str = "0cm",
        line_height: str = "128%",
        margin_left: str = "0cm",
        text_indent: str = "0cm",
    ) -> str:
        name = self._next_style("P")
        self._auto_styles.append(
            f'<style:style style:name="{name}" style:family="paragraph">'
            f'<style:paragraph-properties fo:text-align="{align}" '
            f'fo:margin-top="{space_before}" fo:margin-bottom="{space_after}" '
            f'fo:line-height="{line_height}" fo:margin-left="{margin_left}" '
            f'fo:text-indent="{text_indent}"/>'
            f"</style:style>"
        )
        return name

    def _make_page_style(self, bg_color: str) -> str:
        name = self._next_style("dp")
        self._auto_styles.append(
            f'<style:style style:name="{name}" style:family="drawing-page">'
            f'<style:drawing-page-properties draw:fill="solid" draw:fill-color="{bg_color}"/>'
            f"</style:style>"
        )
        return name

    def _frame_textbox(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        paragraphs_xml: str,
        gr_style: Optional[str] = None,
    ) -> str:
        st = gr_style or self._make_rect_style(None, None, pad_lr="0.05cm", pad_tb="0.04cm")
        return (
            f'<draw:frame draw:style-name="{st}" svg:x="{x:.3f}cm" svg:y="{y:.3f}cm" '
            f'svg:width="{w:.3f}cm" svg:height="{h:.3f}cm">'
            f"<draw:text-box>{paragraphs_xml}</draw:text-box>"
            f"</draw:frame>"
        )

    def _rect(
        self,
        x: float,
        y: float,
        w: float,
        h: float,
        fill: Optional[str],
        stroke: Optional[str] = None,
        stroke_w: str = "0.03cm",
    ) -> str:
        st = self._make_rect_style(fill, stroke, stroke_width=stroke_w, pad_lr="0cm", pad_tb="0cm")
        return (
            f'<draw:rect draw:style-name="{st}" svg:x="{x:.3f}cm" svg:y="{y:.3f}cm" '
            f'svg:width="{w:.3f}cm" svg:height="{h:.3f}cm"/>'
        )

    def _image_frame(self, path: str, box_x: float, box_y: float, box_w: float, box_h: float) -> str:
        zip_name, w_px, h_px = self._register_image(path)
        x, y, w, h = self._fit_image_box(box_x, box_y, box_w, box_h, w_px, h_px)
        st = self._make_rect_style(None, None, pad_lr="0cm", pad_tb="0cm")
        return (
            f'<draw:frame draw:style-name="{st}" svg:x="{x:.3f}cm" svg:y="{y:.3f}cm" '
            f'svg:width="{w:.3f}cm" svg:height="{h:.3f}cm">'
            f'<draw:image xlink:href="{zip_name}" xlink:type="simple" xlink:show="embed" xlink:actuate="onLoad"/>'
            f"</draw:frame>"
        )

    def _p(self, text: str, t_style: str, p_style: str) -> str:
        lines = str(text).split("\n")
        body = "<text:line-break/>".join(
            f'<text:span text:style-name="{t_style}">{esc(line)}</text:span>' for line in lines
        )
        return f'<text:p text:style-name="{p_style}">{body}</text:p>'

    def _p_mixed(self, spans: List[Tuple[str, str]], p_style: str) -> str:
        inner = "".join(f'<text:span text:style-name="{ts}">{esc(tx)}</text:span>' for tx, ts in spans)
        return f'<text:p text:style-name="{p_style}">{inner}</text:p>'

    def _build_notes(self, notes_text: str) -> str:
        if not notes_text.strip():
            return ""
        p_st = self._make_para_style(space_after="0.16cm", line_height="120%")
        t_st = self._make_text_style(11.0, "#1E293B")
        gr_st = self._make_rect_style(None, None, pad_lr="0.1cm", pad_tb="0.1cm")
        paras = "".join(
            self._p(line.strip(), t_st, p_st)
            for line in notes_text.strip().splitlines()
            if line.strip()
        )
        return (
            f'<presentation:notes draw:style-name="dp_notes">'
            f'<draw:frame draw:style-name="{gr_st}" presentation:class="notes" '
            f'svg:x="1.5cm" svg:y="13.5cm" svg:width="18cm" svg:height="14.5cm">'
            f"<draw:text-box>{paras}</draw:text-box>"
            f"</draw:frame>"
            f"</presentation:notes>"
        )

    def _build_header(self, s: SlideSpec, slide_num: int, total: int) -> List[str]:
        els: List[str] = []
        els.append(self._rect(1.5, 0.85, 1.1, 0.11, s.accent_color))
        if s.section_tag:
            t_tag = self._make_text_style(10.5, s.accent_color, bold=True)
            p_tag = self._make_para_style(align="start", space_after="0cm")
            els.append(self._frame_textbox(2.8, 0.66, 22.0, 0.65, self._p(s.section_tag, t_tag, p_tag)))
        t_num = self._make_text_style(10.5, PALETTE["ink_muted"])
        p_num = self._make_para_style(align="end", space_after="0cm")
        num_label = f"{self.deck_code}  {slide_num:02d} / {total:02d}" if self.deck_code else f"{slide_num:02d} / {total:02d}"
        els.append(self._frame_textbox(26.5, 0.66, 5.85, 0.65, self._p(num_label, t_num, p_num)))

        title_size = 24.0 if len(s.title) > 28 else 26.5
        t_title = self._make_text_style(title_size, PALETTE["ink"], bold=True)
        p_title = self._make_para_style(align="start", space_after="0cm", line_height="112%")
        els.append(self._frame_textbox(1.5, 1.32, 30.8, 1.45, self._p(s.title, t_title, p_title)))

        els.append(self._rect(1.5, 2.86, 30.85, 0.035, PALETTE["border"]))
        return els

    def _build_footer(self, s: SlideSpec) -> List[str]:
        if not s.footnote:
            return []
        t_fn = self._make_text_style(9.5, PALETTE["ink_muted"])
        p_fn = self._make_para_style(align="start", space_after="0cm", line_height="115%")
        return [self._frame_textbox(1.5, 18.08, 30.85, 0.72, self._p(s.footnote, t_fn, p_fn))]

    def _build_formula_strip(
        self, x: float, y: float, w: float, h: float, formula: str, caption: str, accent: str,
        formula_tex: str = "",
    ) -> List[str]:
        els: List[str] = []
        els.append(self._rect(x, y, w, h, PALETTE["surface"], PALETTE["border"], "0.025cm"))
        els.append(self._rect(x, y, 0.14, h, accent))
        if formula_tex:
            image = render_formula_png(formula_tex)
            cap_h = 1.12 if caption else 0.0
            els.append(self._image_frame(image, x + 0.32, y + 0.10, w - 0.50, h - cap_h - 0.16))
            if caption:
                t_cap = self._make_text_style(10.4, PALETTE["ink_muted"])
                p_cap = self._make_para_style(space_after="0cm", line_height="112%")
                els.append(self._frame_textbox(x + 0.28, y + h - cap_h, w - 0.40, cap_h - 0.06, self._p(caption, t_cap, p_cap)))
            return els
        f_size = 12.2 if len(formula) > 58 else (13.2 if len(formula) > 44 else 14.5)
        t_form = self._make_text_style(f_size, PALETTE["ink"], bold=True, mono=True)
        p_form = self._make_para_style(space_after="0.08cm", line_height="118%")
        paras = self._p(formula, t_form, p_form)
        if caption:
            t_cap = self._make_text_style(10.8, PALETTE["ink_muted"])
            p_cap = self._make_para_style(space_after="0cm", line_height="115%")
            paras += self._p(caption, t_cap, p_cap)
        gr_pad = self._make_rect_style(None, None, pad_lr="0.28cm", pad_tb="0.16cm", v_align="middle")
        els.append(self._frame_textbox(x + 0.18, y, w - 0.24, h, paras, gr_style=gr_pad))
        return els

    def _build_callout_strip(
        self, x: float, y: float, w: float, h: float, text: str, accent: str
    ) -> List[str]:
        els: List[str] = []
        els.append(self._rect(x, y, w, h, PALETTE["surface"], PALETTE["border"], "0.025cm"))
        els.append(self._rect(x, y, 0.14, h, accent))
        t_co = self._make_text_style(12.4, PALETTE["ink_secondary"], bold=False)
        p_co = self._make_para_style(space_after="0cm", line_height="122%")
        gr_pad = self._make_rect_style(None, None, pad_lr="0.30cm", pad_tb="0.14cm", v_align="middle")
        els.append(self._frame_textbox(x + 0.18, y, w - 0.24, h, self._p(text, t_co, p_co), gr_style=gr_pad))
        return els

    def _render_slide(self, s: SlideSpec, idx: int, total: int) -> str:
        els: List[str] = []

        if s.kind == "cover":
            dp = self._make_page_style(PALETTE["bg_cover"])
            els.append(self._rect(0.0, 0.0, 0.55, self.PAGE_H, PALETTE["gold"]))
            els.append(self._rect(2.4, 3.3, 2.2, 0.14, PALETTE["gold"]))
            if s.section_tag:
                t_tag = self._make_text_style(14.0, "#93C5FD", bold=True)
                p_tag = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(2.4, 3.85, 28.0, 0.9, self._p(s.section_tag, t_tag, p_tag)))

            title_lines = s.title.count("\n") + 1
            title_size = 34.0 if title_lines >= 3 else 39.0
            title_h = 5.15 if title_lines >= 3 else 4.2
            t_main = self._make_text_style(title_size, PALETTE["white"], bold=True)
            p_main = self._make_para_style(space_after="0.25cm", line_height="112%")
            els.append(self._frame_textbox(2.4, 4.85, 28.5, title_h, self._p(s.title, t_main, p_main)))

            if s.subtitle:
                t_sub = self._make_text_style(17.0, PALETTE["light_text"])
                p_sub = self._make_para_style(space_after="0cm", line_height="130%")
                els.append(self._frame_textbox(2.4, 10.15, 27.2, 2.55, self._p(s.subtitle, t_sub, p_sub)))

            if s.footnote:
                els.append(self._rect(2.4, 15.6, 28.5, 0.03, "#334155"))
                t_ft = self._make_text_style(12.2, "#94A3B8")
                p_ft = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(2.4, 16.05, 28.5, 1.4, self._p(s.footnote, t_ft, p_ft)))

        elif s.kind == "divider":
            dp = self._make_page_style(PALETTE["bg_divider"])
            els.append(self._rect(0.0, 0.0, 0.45, self.PAGE_H, s.accent_color))
            els.append(self._rect(2.6, 6.0, 2.4, 0.14, PALETTE["gold"]))
            if s.section_tag:
                t_tag = self._make_text_style(15.0, "#93C5FD", bold=True)
                p_tag = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(2.6, 6.55, 28.0, 0.9, self._p(s.section_tag, t_tag, p_tag)))
            t_main = self._make_text_style(35.0, PALETTE["white"], bold=True)
            p_main = self._make_para_style(space_after="0.3cm", line_height="118%")
            els.append(self._frame_textbox(2.6, 7.75, 28.0, 3.2, self._p(s.title, t_main, p_main)))
            if s.subtitle:
                t_sub = self._make_text_style(17.0, PALETTE["light_text"])
                p_sub = self._make_para_style(space_after="0cm", line_height="135%")
                els.append(self._frame_textbox(2.6, 11.2, 26.5, 3.4, self._p(s.subtitle, t_sub, p_sub)))

        elif s.kind == "content_visual":
            dp = self._make_page_style(PALETTE["bg"])
            els.extend(self._build_header(s, idx, total))

            left_x, left_w = 1.5, 12.1
            cur_y = 3.22
            if s.subtitle:
                sub_h = 1.55 if len(s.subtitle) > 78 else 0.85
                t_sub = self._make_text_style(12.6, s.accent_color, bold=True)
                p_sub = self._make_para_style(space_after="0.08cm", line_height="122%")
                els.append(self._frame_textbox(left_x, cur_y, left_w, sub_h, self._p(s.subtitle, t_sub, p_sub)))
                cur_y += sub_h + 0.08

            has_formula = bool(s.formula)
            bullet_h = (13.95 - cur_y) if has_formula else (17.55 - cur_y)
            b_size = 15.2 if len(s.bullets) <= 4 else 14.2
            t_dot = self._make_text_style(b_size, s.accent_color, bold=True)
            t_b = self._make_text_style(b_size, PALETTE["ink_secondary"])
            p_b = self._make_para_style(
                space_after="0.40cm", line_height="134%", margin_left="0.55cm", text_indent="-0.55cm"
            )
            b_xml = "".join(self._p_mixed([("▪  ", t_dot), (b, t_b)], p_b) for b in s.bullets)
            els.append(self._frame_textbox(left_x, cur_y, left_w, bullet_h, b_xml))

            if has_formula:
                els.extend(
                    self._build_formula_strip(
                        left_x, 14.25, left_w, 3.30, s.formula, s.formula_caption, s.accent_color,
                        formula_tex=s.formula_tex,
                    )
                )

            right_x, right_y, right_w, right_h = 14.25, 3.28, 18.10, 13.70
            if s.image_path:
                els.append(self._image_frame(s.image_path, right_x, right_y, right_w, right_h))
            if s.image_caption:
                t_ic = self._make_text_style(10.5, PALETTE["ink_muted"])
                p_ic = self._make_para_style(align="center", space_after="0cm")
                els.append(self._frame_textbox(right_x, 17.12, right_w, 0.65, self._p(s.image_caption, t_ic, p_ic)))

            els.extend(self._build_footer(s))

        elif s.kind == "problem":
            dp = self._make_page_style(PALETTE["bg"])
            els.extend(self._build_header(s, idx, total))

            left_x, left_w = 1.5, 12.25
            cur_y = 3.25
            if s.problem_meta:
                meta_h = 1.02 if len(s.problem_meta) > 64 else 0.62
                t_meta = self._make_text_style(10.8, PALETTE["ink_muted"], bold=True)
                p_meta = self._make_para_style(space_after="0.06cm", line_height="118%")
                els.append(self._frame_textbox(left_x, cur_y, left_w, meta_h, self._p(s.problem_meta, t_meta, p_meta)))
                cur_y += meta_h + 0.08

            dim_colors = [PALETTE["accent"], PALETTE["coral"], PALETTE["teal"]]
            gap = 0.24
            n_dims = max(len(s.problem_dims), 1)
            dim_h = (17.60 - cur_y - gap * (n_dims - 1)) / n_dims
            for di, (d_label, d_text) in enumerate(s.problem_dims):
                dc = dim_colors[di % len(dim_colors)]
                by = cur_y + di * (dim_h + gap)
                els.append(self._rect(left_x, by, left_w, dim_h, PALETTE["surface"], PALETTE["border"], "0.02cm"))
                els.append(self._rect(left_x, by, 0.13, dim_h, dc))
                t_lbl = self._make_text_style(12.2, dc, bold=True)
                t_txt = self._make_text_style(13.2, PALETTE["ink_secondary"])
                p_lbl = self._make_para_style(space_after="0.08cm", line_height="114%")
                p_txt = self._make_para_style(space_after="0cm", line_height="128%")
                gr_pad = self._make_rect_style(None, None, pad_lr="0.26cm", pad_tb="0.16cm", v_align="top")
                els.append(
                    self._frame_textbox(
                        left_x + 0.18,
                        by,
                        left_w - 0.22,
                        dim_h,
                        self._p(d_label, t_lbl, p_lbl) + self._p(d_text, t_txt, p_txt),
                        gr_style=gr_pad,
                    )
                )

            right_x, right_y, right_w, right_h = 14.30, 3.28, 18.05, 13.70
            if s.image_path:
                els.append(self._image_frame(s.image_path, right_x, right_y, right_w, right_h))
            if s.image_caption:
                t_ic = self._make_text_style(10.5, PALETTE["ink_muted"])
                p_ic = self._make_para_style(align="center", space_after="0cm")
                els.append(self._frame_textbox(right_x, 17.12, right_w, 0.65, self._p(s.image_caption, t_ic, p_ic)))

            els.extend(self._build_footer(s))

        elif s.kind == "full_visual":
            dp = self._make_page_style(PALETTE["bg"])
            els.extend(self._build_header(s, idx, total))
            top_y = 3.22
            if s.subtitle:
                t_sub = self._make_text_style(13.5, PALETTE["ink_secondary"])
                p_sub = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(1.5, top_y, 30.8, 0.78, self._p(s.subtitle, t_sub, p_sub)))
                top_y += 0.85

            img_h = 13.65 if not s.callout else 12.15
            if s.image_path:
                els.append(self._image_frame(s.image_path, 1.5, top_y, 30.85, img_h))

            if s.callout:
                cy = top_y + img_h + 0.28
                els.append(self._rect(1.5, cy, 30.85, 1.32, PALETTE["surface"], PALETTE["border"], "0.02cm"))
                els.append(self._rect(1.5, cy, 0.14, 1.32, s.accent_color))
                t_co = self._make_text_style(12.8, PALETTE["ink_secondary"])
                p_co = self._make_para_style(space_after="0cm", line_height="122%")
                gr_pad = self._make_rect_style(None, None, pad_lr="0.32cm", pad_tb="0.14cm", v_align="middle")
                els.append(self._frame_textbox(1.72, cy, 30.5, 1.32, self._p(s.callout, t_co, p_co), gr_style=gr_pad))

            els.extend(self._build_footer(s))

        elif s.kind == "two_col":
            dp = self._make_page_style(PALETTE["bg"])
            els.extend(self._build_header(s, idx, total))
            top_y = 3.30
            if s.subtitle:
                t_sub = self._make_text_style(14.0, PALETTE["ink_secondary"])
                p_sub = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(1.5, top_y, 30.8, 0.85, self._p(s.subtitle, t_sub, p_sub)))
                top_y += 0.98

            col_w = 14.95
            col_h = 15.60 - top_y
            for cx, ctitle, cbullets, ccolor in [
                (1.5, s.left_title, s.left_bullets, s.accent_color),
                (17.4, s.right_title, s.right_bullets, PALETTE["teal"]),
            ]:
                els.append(self._rect(cx, top_y, col_w, 0.10, ccolor))
                t_ct = self._make_text_style(16.8, PALETTE["ink"], bold=True)
                p_ct = self._make_para_style(space_after="0.15cm")
                els.append(self._frame_textbox(cx, top_y + 0.25, col_w, 0.95, self._p(ctitle, t_ct, p_ct)))

                t_dot = self._make_text_style(13.8, ccolor, bold=True)
                t_b = self._make_text_style(14.0, PALETTE["ink_secondary"])
                p_b = self._make_para_style(
                    space_after="0.30cm", line_height="132%", margin_left="0.52cm", text_indent="-0.52cm"
                )
                b_xml = "".join(self._p_mixed([("▪  ", t_dot), (b, t_b)], p_b) for b in cbullets)
                els.append(self._frame_textbox(cx, top_y + 1.32, col_w, col_h - 1.35, b_xml))

            if s.callout:
                els.extend(self._build_callout_strip(1.5, 16.05, 30.85, 1.72, s.callout, s.accent_color))

            els.extend(self._build_footer(s))

        elif s.kind == "table":
            dp = self._make_page_style(PALETTE["bg"])
            els.extend(self._build_header(s, idx, total))
            top_y = 3.25
            if s.subtitle:
                t_sub = self._make_text_style(13.5, PALETTE["ink_secondary"])
                p_sub = self._make_para_style(space_after="0cm")
                els.append(self._frame_textbox(1.5, top_y, 30.8, 0.78, self._p(s.subtitle, t_sub, p_sub)))
                top_y += 0.86

            ncols = len(s.table_headers)
            total_w = 30.85
            if s.table_col_widths_cm and len(s.table_col_widths_cm) == ncols:
                col_ws = s.table_col_widths_cm
            else:
                col_ws = [total_w / ncols] * ncols

            col_xml_parts = []
            for cw in col_ws:
                cs = self._next_style("co")
                self._auto_styles.append(
                    f'<style:style style:name="{cs}" style:family="table-column">'
                    f'<style:table-column-properties style:column-width="{cw:.3f}cm"/>'
                    f"</style:style>"
                )
                col_xml_parts.append(f'<table:table-column table:style-name="{cs}"/>')

            ce_hdr = self._next_style("ce")
            ce_even = self._next_style("ce")
            ce_odd = self._next_style("ce")
            self._auto_styles.append(
                f'<style:style style:name="{ce_hdr}" style:family="table-cell">'
                f'<style:graphic-properties draw:fill="solid" draw:fill-color="{s.accent_color}" '
                f'fo:padding-left="0.22cm" fo:padding-right="0.22cm" fo:padding-top="0.18cm" fo:padding-bottom="0.18cm" '
                f'fo:border="0.02cm solid #CBD5E1" draw:textarea-vertical-align="middle"/>'
                f"</style:style>"
            )
            self._auto_styles.append(
                f'<style:style style:name="{ce_even}" style:family="table-cell">'
                f'<style:graphic-properties draw:fill="solid" draw:fill-color="#FFFFFF" '
                f'fo:padding-left="0.22cm" fo:padding-right="0.22cm" fo:padding-top="0.16cm" fo:padding-bottom="0.16cm" '
                f'fo:border="0.02cm solid #E2E8F0" draw:textarea-vertical-align="middle"/>'
                f"</style:style>"
            )
            self._auto_styles.append(
                f'<style:style style:name="{ce_odd}" style:family="table-cell">'
                f'<style:graphic-properties draw:fill="solid" draw:fill-color="#F8FAFC" '
                f'fo:padding-left="0.22cm" fo:padding-right="0.22cm" fo:padding-top="0.16cm" fo:padding-bottom="0.16cm" '
                f'fo:border="0.02cm solid #E2E8F0" draw:textarea-vertical-align="middle"/>'
                f"</style:style>"
            )

            nrows = len(s.table_rows)
            avail_h = (15.65 if s.callout else 17.55) - top_y
            hdr_h = 1.10
            row_h = min(3.0, max(1.02, (avail_h - hdr_h) / max(nrows, 1)))
            ro_hdr = self._next_style("ro")
            ro_body = self._next_style("ro")
            self._auto_styles.append(
                f'<style:style style:name="{ro_hdr}" style:family="table-row">'
                f'<style:table-row-properties style:row-height="{hdr_h:.3f}cm"/>'
                f"</style:style>"
            )
            self._auto_styles.append(
                f'<style:style style:name="{ro_body}" style:family="table-row">'
                f'<style:table-row-properties style:row-height="{row_h:.3f}cm"/>'
                f"</style:style>"
            )

            t_hdr = self._make_text_style(11.8, PALETTE["white"], bold=True)
            p_hdr = self._make_para_style(space_after="0cm", line_height="114%")
            body_pt = 10.6 if nrows >= 7 else (11.2 if nrows >= 5 else 12.0)
            t_cell_bold = self._make_text_style(body_pt, PALETTE["ink"], bold=True)
            t_cell = self._make_text_style(body_pt, PALETTE["ink_secondary"])
            p_cell = self._make_para_style(space_after="0cm", line_height="120%")

            rows_xml = []
            hdr_cells = "".join(
                f'<table:table-cell table:style-name="{ce_hdr}">{self._p(h, t_hdr, p_hdr)}</table:table-cell>'
                for h in s.table_headers
            )
            rows_xml.append(f'<table:table-row table:style-name="{ro_hdr}">{hdr_cells}</table:table-row>')

            for ri, row in enumerate(s.table_rows):
                cst = ce_even if ri % 2 == 0 else ce_odd
                cells = []
                for ci, val in enumerate(row):
                    ts = t_cell_bold if ci == 0 else t_cell
                    cells.append(f'<table:table-cell table:style-name="{cst}">{self._p(val, ts, p_cell)}</table:table-cell>')
                rows_xml.append(f'<table:table-row table:style-name="{ro_body}">{"".join(cells)}</table:table-row>')

            tbl_h = hdr_h + row_h * nrows
            tbl_xml = (
                f'<draw:frame svg:x="1.500cm" svg:y="{top_y:.3f}cm" '
                f'svg:width="{total_w:.3f}cm" svg:height="{tbl_h:.3f}cm">'
                f"<table:table>{''.join(col_xml_parts)}{''.join(rows_xml)}</table:table>"
                f"</draw:frame>"
            )
            els.append(tbl_xml)

            if s.callout:
                cy = min(16.10, top_y + tbl_h + 0.35)
                els.append(self._rect(1.5, cy, 30.85, 1.50, PALETTE["surface"], PALETTE["border"], "0.02cm"))
                els.append(self._rect(1.5, cy, 0.14, 1.50, s.accent_color))
                t_co = self._make_text_style(12.0, PALETTE["ink_secondary"])
                p_co = self._make_para_style(space_after="0cm", line_height="120%")
                gr_pad = self._make_rect_style(None, None, pad_lr="0.30cm", pad_tb="0.14cm", v_align="middle")
                els.append(self._frame_textbox(1.72, cy, 30.45, 1.50, self._p(s.callout, t_co, p_co), gr_style=gr_pad))

            els.extend(self._build_footer(s))

        else:
            raise ValueError(f"Unknown slide kind: {s.kind}")

        notes_xml = self._build_notes(s.speaker_notes)
        return (
            f'<draw:page draw:name="slide_{idx:02d}" draw:style-name="{dp}" draw:master-page-name="Default">'
            f"{''.join(els)}{notes_xml}"
            f"</draw:page>"
        )

    def save(self, out_odp: str | Path) -> Path:
        out_path = Path(out_odp).resolve()
        out_path.parent.mkdir(parents=True, exist_ok=True)
        self._auto_styles = [
            '<style:style style:name="dp_notes" style:family="drawing-page">'
            '<style:drawing-page-properties draw:fill="solid" draw:fill-color="#FFFFFF"/>'
            "</style:style>"
        ]
        self._style_counter = 0

        total = len(self.slides)
        pages_xml = [self._render_slide(s, i + 1, total) for i, s in enumerate(self.slides)]

        manifest_entries = [
            '<manifest:file-entry manifest:full-path="/" manifest:version="1.2" manifest:media-type="application/vnd.oasis.opendocument.presentation"/>',
            '<manifest:file-entry manifest:full-path="content.xml" manifest:media-type="text/xml"/>',
            '<manifest:file-entry manifest:full-path="styles.xml" manifest:media-type="text/xml"/>',
            '<manifest:file-entry manifest:full-path="meta.xml" manifest:media-type="text/xml"/>',
        ]
        for zip_name, _ in self._images.values():
            mime = "image/png" if zip_name.endswith(".png") else "image/jpeg"
            manifest_entries.append(
                f'<manifest:file-entry manifest:full-path="{zip_name}" manifest:media-type="{mime}"/>'
            )

        manifest_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<manifest:manifest xmlns:manifest="urn:oasis:names:tc:opendocument:xmlns:manifest:1.0" manifest:version="1.2">\n'
            + "\n".join(f"  {e}" for e in manifest_entries)
            + "\n</manifest:manifest>\n"
        )

        meta_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<office:document-meta xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/" office:version="1.2">\n'
            f"  <office:meta><dc:title>{esc(self.title)}</dc:title><dc:creator>{esc(self.author)}</dc:creator></office:meta>\n"
            "</office:document-meta>\n"
        )

        styles_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<office:document-styles xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
            'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
            'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" '
            'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
            'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
            'office:version="1.2">\n'
            "  <office:font-face-decls>\n"
            '    <style:font-face style:name="Helvetica Neue" svg:font-family="&apos;Helvetica Neue&apos;"/>\n'
            '    <style:font-face style:name="Helvetica Neue" svg:font-family="&apos;Helvetica Neue&apos;"/>\n'
            '    <style:font-face style:name="Menlo" svg:font-family="&apos;Menlo&apos;"/>\n'
            "  </office:font-face-decls>\n"
            "  <office:styles>\n"
            '    <style:style style:name="dp-default" style:family="drawing-page">\n'
            '      <style:drawing-page-properties draw:fill="solid" draw:fill-color="#FFFFFF"/>\n'
            "    </style:style>\n"
            "  </office:styles>\n"
            "  <office:automatic-styles>\n"
            '    <style:page-layout style:name="PM1">\n'
            f'      <style:page-layout-properties fo:margin-top="0cm" fo:margin-bottom="0cm" fo:margin-left="0cm" fo:margin-right="0cm" fo:page-width="{self.PAGE_W:.3f}cm" fo:page-height="{self.PAGE_H:.3f}cm" style:print-orientation="landscape"/>\n'
            "    </style:page-layout>\n"
            '    <style:page-layout style:name="PM2">\n'
            '      <style:page-layout-properties fo:page-width="21cm" fo:page-height="29.7cm" style:print-orientation="portrait"/>\n'
            "    </style:page-layout>\n"
            "  </office:automatic-styles>\n"
            "  <office:master-styles>\n"
            '    <style:master-page style:name="Default" style:page-layout-name="PM1" draw:style-name="dp-default"/>\n'
            '    <style:handout-master style:page-layout-name="PM2"/>\n'
            "  </office:master-styles>\n"
            "</office:document-styles>\n"
        )

        content_xml = (
            '<?xml version="1.0" encoding="UTF-8"?>\n'
            '<office:document-content xmlns:office="urn:oasis:names:tc:opendocument:xmlns:office:1.0" '
            'xmlns:style="urn:oasis:names:tc:opendocument:xmlns:style:1.0" '
            'xmlns:text="urn:oasis:names:tc:opendocument:xmlns:text:1.0" '
            'xmlns:draw="urn:oasis:names:tc:opendocument:xmlns:drawing:1.0" '
            'xmlns:table="urn:oasis:names:tc:opendocument:xmlns:table:1.0" '
            'xmlns:fo="urn:oasis:names:tc:opendocument:xmlns:xsl-fo-compatible:1.0" '
            'xmlns:svg="urn:oasis:names:tc:opendocument:xmlns:svg-compatible:1.0" '
            'xmlns:xlink="http://www.w3.org/1999/xlink" '
            'xmlns:presentation="urn:oasis:names:tc:opendocument:xmlns:presentation:1.0" '
            'office:version="1.2">\n'
            "  <office:font-face-decls>\n"
            '    <style:font-face style:name="Helvetica Neue" svg:font-family="&apos;Helvetica Neue&apos;"/>\n'
            '    <style:font-face style:name="Helvetica Neue" svg:font-family="&apos;Helvetica Neue&apos;"/>\n'
            '    <style:font-face style:name="Menlo" svg:font-family="&apos;Menlo&apos;"/>\n'
            "  </office:font-face-decls>\n"
            "  <office:automatic-styles>\n"
            + "\n".join(f"    {st}" for st in self._auto_styles)
            + "\n  </office:automatic-styles>\n"
            "  <office:body>\n"
            "    <office:presentation>\n"
            + "\n".join(f"      {pg}" for pg in pages_xml)
            + "\n    </office:presentation>\n"
            "  </office:body>\n"
            "</office:document-content>\n"
        )

        with zipfile.ZipFile(out_path, "w") as zf:
            zf.writestr(
                "mimetype",
                "application/vnd.oasis.opendocument.presentation",
                compress_type=zipfile.ZIP_STORED,
            )
            zf.writestr("META-INF/manifest.xml", manifest_xml, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("meta.xml", meta_xml, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("styles.xml", styles_xml, compress_type=zipfile.ZIP_DEFLATED)
            zf.writestr("content.xml", content_xml, compress_type=zipfile.ZIP_DEFLATED)
            for zip_name, raw in self._images.values():
                zf.writestr(zip_name, raw, compress_type=zipfile.ZIP_DEFLATED)

        return out_path


def convert_odp_with_libreoffice(odp_path: Path, pdf_dir: Path, pptx_dir: Path) -> Tuple[Path, Path]:
    """Use LibreOffice headless with an isolated UserInstallation profile to export PDF & PPTX."""
    pdf_dir.mkdir(parents=True, exist_ok=True)
    pptx_dir.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix="lo_prof_") as prof_dir:
        env_arg = f"-env:UserInstallation=file://{prof_dir}"
        for fmt, out_dir in [("pdf", pdf_dir), ("pptx", pptx_dir)]:
            cmd = [
                "soffice",
                env_arg,
                "--headless",
                "--convert-to",
                fmt,
                "--outdir",
                str(out_dir),
                str(odp_path),
            ]
            res = subprocess.run(cmd, capture_output=True, text=True, check=False)
            if res.returncode != 0:
                raise RuntimeError(f"LibreOffice {fmt} conversion failed for {odp_path.name}: {res.stderr}")
    stem = odp_path.stem
    return pdf_dir / f"{stem}.pdf", pptx_dir / f"{stem}.pptx"
