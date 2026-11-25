#!/usr/bin/env python3
"""Render LaTeX math strings to tightly cropped PNGs for slide formula strips.

Supports both plain math (`render_formula_png`) and color-coded annotated
formulas with pill boxes, curved upward arrows, and matching legend cards
(`render_annotated_formula_png`).
"""

from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
import tempfile
from pathlib import Path
from typing import List, Optional, Sequence, Tuple

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "slides" / ".formula-cache"
STRIP_BG = (255, 255, 255)
PDFLATEX_CANDIDATES = (
    "pdflatex",
    "/Library/TeX/texbin/pdflatex",
    "/usr/local/texlive/2026basic/bin/universal-darwin/pdflatex",
)

# 5-color cycle matching webapp .ft-c0 .. .ft-c4
TERM_COLORS = [
    ("2563EB", "EFF6FF"),  # blue
    ("16A34A", "F0FDF4"),  # green
    ("7C3AED", "F5F3FF"),  # violet
    ("EA580C", "FFF7ED"),  # orange
    ("0D9488", "F0FDFA"),  # teal
]

TEX_TEMPLATE = r"""\documentclass{article}
\usepackage{amsmath,amssymb,lmodern}
\usepackage[T1]{fontenc}
\pagestyle{empty}
\pdfpagewidth=18cm
\pdfpageheight=3.2cm
\setlength{\oddsidemargin}{-1in}
\setlength{\topmargin}{-1in}
\setlength{\textwidth}{17.6cm}
\setlength{\textheight}{3.0cm}
\setlength{\parindent}{0pt}
\begin{document}
\noindent{\fontsize{15}{18}\selectfont $\displaystyle __BODY__$}
\end{document}
"""

ANNOTATED_TEX_TEMPLATE = r"""\documentclass{article}
\usepackage{amsmath,amssymb,lmodern}
\usepackage[T1]{fontenc}
\usepackage[paperwidth=32cm,paperheight=11cm,margin=0.4cm]{geometry}
\usepackage{xcolor}
\usepackage{tikz}
\usetikzlibrary{positioning,arrows.meta,calc}
\pagestyle{empty}
\setlength{\parindent}{0pt}

\definecolor{c0b}{HTML}{2563EB} \definecolor{c0bg}{HTML}{EFF6FF}
\definecolor{c1b}{HTML}{16A34A} \definecolor{c1bg}{HTML}{F0FDF4}
\definecolor{c2b}{HTML}{7C3AED} \definecolor{c2bg}{HTML}{F5F3FF}
\definecolor{c3b}{HTML}{EA580C} \definecolor{c3bg}{HTML}{FFF7ED}
\definecolor{c4b}{HTML}{0D9488} \definecolor{c4bg}{HTML}{F0FDFA}
\definecolor{ink}{HTML}{171717}
\definecolor{muted}{HTML}{525252}

\newcommand{\term}[4]{%
  \tikz[remember picture, baseline=(#1.base)]{%
    \node[draw=#2, fill=#3, line width=1.05pt, rounded corners=4pt, inner xsep=4.5pt, inner ysep=2.6pt] (#1) {$\displaystyle #4$};%
  }%
}

\begin{document}
\vspace*{0.3cm}
\begin{center}
{\fontsize{15.5}{19}\selectfont%
$\displaystyle __FORMULA__$%
}
\end{center}
\vspace{1.05cm}
\begin{center}
\begin{tikzpicture}[remember picture]
__CARDS__
\end{tikzpicture}
\end{center}
\begin{tikzpicture}[remember picture, overlay]
__ARROWS__
\end{tikzpicture}
\end{document}
"""


def _pdflatex() -> str:
    for candidate in PDFLATEX_CANDIDATES:
        found = shutil.which(candidate) if "/" not in candidate else candidate
        if found and Path(found).exists():
            return found
    raise FileNotFoundError("pdflatex not found. Install a TeX distribution to render slide formulas.")


def _crop_onto_strip(src: Path, dest: Path, bg: Tuple[int, int, int] = STRIP_BG) -> None:
    image = Image.open(src).convert("RGB")
    diff = ImageChops.difference(image, Image.new("RGB", image.size, (255, 255, 255)))
    bbox = diff.getbbox()
    if bbox is None:
        raise RuntimeError(f"LaTeX render produced an empty page: {src}")
    pad = 12
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(image.width, bbox[2] + pad)
    bottom = min(image.height, bbox[3] + pad)
    cropped = image.crop((left, top, right, bottom))
    if bg == (255, 255, 255):
        dest.parent.mkdir(parents=True, exist_ok=True)
        cropped.save(dest, "PNG")
        return
    canvas = Image.new("RGB", cropped.size, bg)
    ink = cropped.convert("L").point(lambda p: 0 if p > 250 else 255)
    canvas.paste(cropped, mask=ink)
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "PNG")


def _escape_latex_text(text: str) -> str:
    rep = {
        "\\": r"\textbackslash{}",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
        "{": r"\{",
        "}": r"\}",
        "~": r"\textasciitilde{}",
        "^": r"\textasciicircum{}",
    }
    out = "".join(rep.get(ch, ch) for ch in text)
    out = out.replace("α", r"$\alpha$").replace("Φ", r"$\Phi$").replace("η", r"$\eta$")
    out = out.replace("→", r"$\to$").replace("≤", r"$\le$").replace("≥", r"$\ge$")
    return out


def _sym_to_tex_candidates(sym: str) -> List[str]:
    """Convert a plain symbol string like 'T_eff' or 'α' to candidate LaTeX math fragments."""
    s = sym.strip()
    cands: List[str] = [s]
    # Greek mappings
    greek = {"α": r"\alpha", "Φ": r"\Phi", "η": r"\eta", "χ": r"\chi", "φ": r"\phi", "τ": r"\tau"}
    if s in greek:
        cands.insert(0, greek[s])
    # Subscript patterns like T_eff -> T_{\mathrm{eff}}, Q_min -> Q_{\min}, m_1/2 -> m_{1/2}
    if "_" in s and not s.startswith("\\") and "{" not in s and "," not in s:
        base, sub = s.split("_", 1)
        if sub == "min":
            cands.insert(0, rf"{base}_{{\min}}")
        elif sub == "max":
            cands.insert(0, rf"{base}_{{\max}}")
        elif len(sub) == 1:
            cands.insert(0, rf"{base}_{{{sub}}}")
            cands.insert(0, rf"{base}_{sub}")
        else:
            cands.insert(0, rf"{base}_{{\mathrm{{{sub}}}}}")
            cands.insert(0, rf"{base}_{{{sub}}}")
    if s == "I*":
        cands.insert(0, r"I^{*}")
        cands.insert(1, r"I^*")
    if s in ("MissRate", "KV", "Full", "Base"):
        cands.insert(0, rf"\mathrm{{{s}}}")
    if s == "S_w(k)":
        cands.insert(0, r"S_{w}(k)")
        cands.insert(1, r"S_w(k)")
    if s.endswith("s") and s[:-1].replace(".", "", 1).isdigit():
        cands.insert(0, rf"{s[:-1]}\,\mathrm{{s}}")
    if "," in s:
        # e.g. "B_M, B_N" or "B,S,L,H" or "V, f" or "Full, Base"
        parts = [p.strip() for p in s.split(",") if p.strip()]
        if parts:
            # Also try matching the first sub-token or space-separated form
            cands.append(r"\,".join(parts))
            cands.append(" ".join(parts))
            cands.extend(_sym_to_tex_candidates(parts[0]))
    return list(dict.fromkeys(cands))


def _sym_display_tex(sym: str, matched_tex: Optional[str]) -> str:
    """Return a clean LaTeX math expression for the symbol header inside a callout card."""
    if matched_tex and "," not in sym:
        return matched_tex
    s = sym.strip()
    greek = {"α": r"\alpha", "Φ": r"\Phi", "η": r"\eta", "χ": r"\chi", "φ": r"\phi", "τ": r"\tau"}
    if s in greek:
        return greek[s]
    if s == "I*":
        return r"I^{*}"
    if s == "S_w(k)":
        return r"S_{w}(k)"
    if s.endswith("s") and s[:-1].replace(".", "", 1).isdigit():
        return rf"{s[:-1]}\,\mathrm{{s}}"
    if "," in s:
        parts = [_sym_display_tex(p.strip(), None) for p in s.split(",") if p.strip()]
        return r",\,".join(parts)
    if "_" in s and "{" not in s:
        base, sub = s.split("_", 1)
        if sub in ("min", "max"):
            return rf"{base}_{{\{sub}}}"
        if len(sub) == 1:
            return rf"{base}_{sub}"
        return rf"{base}_{{\mathrm{{{sub}}}}}"
    if s in ("MissRate", "KV", "Full", "Base"):
        return rf"\mathrm{{{s}}}"
    return s


def _in_frac_numerator(s: str, pos: int) -> bool:
    """Return True if index `pos` lies inside the first braced argument of \\frac{...}{...}."""
    i = 0
    n = len(s)
    while i < n:
        if s.startswith(r"\frac", i) or s.startswith(r"\tfrac", i):
            j = i + (5 if s.startswith(r"\frac", i) else 6)
            while j < n and s[j].isspace():
                j += 1
            if j < n and s[j] == "{":
                depth = 1
                k = j + 1
                while k < n and depth > 0:
                    if s[k] == "{":
                        depth += 1
                    elif s[k] == "}":
                        depth -= 1
                    k += 1
                if j < pos < k:
                    return True
                i = j + 1
                continue
        i += 1
    return False


def _wrap_formula_with_terms(tex_body: str, symbols: Sequence[Tuple[str, str]]) -> Tuple[str, dict[int, str], set[int]]:
    """Wrap all occurrences of each matched symbol in tex_body with color-coded \\term pills.

    The primary occurrence for symbol `idx` (preferring one outside a fraction numerator)
    gets TikZ node `t<idx>` as the arrow anchor; additional occurrences of the same
    symbol get unique TikZ nodes `t<idx>_<k>` with the same color pill so repeated
    variables share identical color coding across the formula.
    """
    work = tex_body
    placed: dict[int, str] = {}
    top_indices: set[int] = set()
    placeholders: List[Tuple[str, int, str, str]] = []  # (token, idx, node_name, orig)
    indexed = [(idx, sym, _sym_to_tex_candidates(sym)) for idx, (sym, _) in enumerate(symbols)]
    # Longest candidate first so T_{\mathrm{eff}} matches before T
    ordered = sorted(indexed, key=lambda x: max((len(c) for c in x[2]), default=0), reverse=True)

    for idx, _sym, cands in ordered:
        matched = False
        for v in cands:
            if not v:
                continue
            start = 0
            candidates_pos: List[Tuple[bool, int]] = []
            while True:
                pos = work.find(v, start)
                if pos == -1:
                    break
                prev = work[pos - 1] if pos > 0 else ""
                nxt = work[pos + len(v)] if pos + len(v) < len(work) else ""
                in_cmd = prev == "\\" and not v.startswith("\\")
                is_single = len(v) == 1 and v.isalnum()
                bad_single = is_single and (
                    (prev.isalpha() or prev == "_") or (nxt.isalnum() or nxt == "_")
                )
                # Check we are not inside an already-inserted placeholder @@TERMk@@
                prefix_window = work[max(0, pos - 14):pos]
                inside_ph = "@@TERM" in prefix_window and "@@" not in prefix_window[prefix_window.rfind("@@TERM") + 6:]
                if not in_cmd and not bad_single and not inside_ph:
                    candidates_pos.append((_in_frac_numerator(work, pos), pos))
                    start = pos + len(v)
                else:
                    start = pos + 1
            if candidates_pos:
                # Choose primary anchor: prefer non-numerator occurrence, then leftmost
                primary = min(candidates_pos, key=lambda pair: (pair[0], pair[1]))
                if primary[0]:
                    top_indices.add(idx)
                placed[idx] = v
                # Replace from right to left so earlier offsets remain valid
                for occ_i, (_is_num, pos) in enumerate(sorted(candidates_pos, key=lambda pair: pair[1], reverse=True)):
                    prev = work[pos - 1] if pos > 0 else ""
                    ph_id = len(placeholders)
                    token = f"@@TERM{ph_id}@@"
                    node_name = f"t{idx}" if pos == primary[1] else f"t{idx}_{occ_i}"
                    need_braces = prev in ("^", "_") and not v.startswith("{")
                    work = work[:pos] + (f"{{{token}}}" if need_braces else token) + work[pos + len(v):]
                    placeholders.append((token, idx, node_name, v))
                matched = True
            if matched:
                break

    for token, idx, node_name, orig in placeholders:
        ci = idx % len(TERM_COLORS)
        rep = rf"{{\term{{{node_name}}}{{c{ci}b}}{{c{ci}bg}}{{{orig}}}}}"
        work = work.replace(token, rep)
    return work, placed, top_indices


def render_formula_png(tex_body: str, cache_dir: Path = CACHE_DIR) -> str:
    """Return a cached PNG path for plain display math."""
    key = hashlib.sha256(("v1:" + tex_body).encode("utf-8")).hexdigest()[:20]
    dest = cache_dir / f"{key}.png"
    if dest.exists() and dest.stat().st_size > 0:
        return str(dest)

    work = Path(tempfile.mkdtemp(prefix="asc27-formula-"))
    tex_path = work / "formula.tex"
    tex_path.write_text(TEX_TEMPLATE.replace("__BODY__", tex_body), encoding="utf-8")
    proc = subprocess.run(
        [_pdflatex(), "-interaction=nonstopmode", "-halt-on-error", "formula.tex"],
        cwd=work,
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0 or not (work / "formula.pdf").exists():
        log_path = work / "formula.log"
        log_tail = log_path.read_text(encoding="utf-8", errors="replace")[-1500:] if log_path.exists() else proc.stdout[-1500:]
        raise RuntimeError(f"pdflatex failed for formula: {tex_body}\n{log_tail}")

    png_base = work / "formula"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "280", str(work / "formula.pdf"), str(png_base)],
        check=True,
        capture_output=True,
    )
    rendered = work / "formula-1.png"
    if not rendered.exists():
        raise RuntimeError(f"pdftoppm produced no PNG for formula: {tex_body}")
    _crop_onto_strip(rendered, dest)
    shutil.rmtree(work, ignore_errors=True)
    return str(dest)


def render_annotated_formula_png(
    tex_body: str,
    symbols: Sequence[Tuple[str, str]],
    cache_dir: Path = CACHE_DIR,
) -> str:
    """Render a color-coded annotated formula diagram with rounded term pills, curved arrows, and legend cards."""
    if not symbols:
        return render_formula_png(tex_body, cache_dir=cache_dir)

    payload = json.dumps({"v": "annot-v3", "tex": tex_body, "syms": list(symbols)}, ensure_ascii=False)
    key = hashlib.sha256(payload.encode("utf-8")).hexdigest()[:20]
    dest = cache_dir / f"annot-{key}.png"
    if dest.exists() and dest.stat().st_size > 0:
        return str(dest)

    wrapped_tex, placed, top_indices = _wrap_formula_with_terms(tex_body, symbols)

    card_lines: List[str] = []
    gap_cm = "0.26cm" if len(symbols) >= 5 else "0.38cm"
    for idx, (sym, meaning) in enumerate(symbols):
        ci = idx % len(TERM_COLORS)
        pos_opt = "" if idx == 0 else f"right={gap_cm} of c{idx - 1}, "
        sym_tex = _sym_display_tex(sym, placed.get(idx))
        meaning_esc = _escape_latex_text(meaning)
        card_lines.append(
            f"  \\node[{pos_opt}draw=c{ci}b, fill=c{ci}bg, line width=0.9pt, rounded corners=5pt, "
            f"inner xsep=6.5pt, inner ysep=4pt, align=left, font=\\sffamily] (c{idx})\n"
            f"    {{\\textcolor{{c{ci}b}}{{\\fontsize{{10.5}}{{12.5}}\\selectfont ${sym_tex}$}}\\\\[-1pt]"
            f"{{\\fontsize{{8.2}}{{9.8}}\\selectfont\\textcolor{{ink}}{{{meaning_esc}}}}}}};"
        )

    arrow_lines: List[str] = []
    for idx in sorted(placed.keys()):
        ci = idx % len(TERM_COLORS)
        if idx in top_indices:
            arrow_lines.append(
                f"  \\draw[c{ci}b, line width=1.05pt, -{{Triangle[length=4.8pt, width=4.0pt]}}]\n"
                f"    (c{idx}.north) .. controls ($(c{idx}.north)+(0,0.85)$) and ($(t{idx}.west)+(-0.65,-0.25)$) .. ($(t{idx}.west)+(-0.07,0)$);"
            )
        else:
            arrow_lines.append(
                f"  \\draw[c{ci}b, line width=1.05pt, -{{Triangle[length=4.8pt, width=4.0pt]}}]\n"
                f"    (c{idx}.north) .. controls ($(c{idx}.north)+(0,0.45)$) and ($(t{idx}.south)+(0,-0.45)$) .. ($(t{idx}.south)+(0,-0.07)$);"
            )

    tex_src = (
        ANNOTATED_TEX_TEMPLATE
        .replace("__FORMULA__", wrapped_tex)
        .replace("__CARDS__", "\n".join(card_lines))
        .replace("__ARROWS__", "\n".join(arrow_lines))
    )

    work = Path(tempfile.mkdtemp(prefix="asc27-annot-"))
    tex_path = work / "formula.tex"
    tex_path.write_text(tex_src, encoding="utf-8")

    # Two pdflatex passes required for TikZ remember picture / overlay coordinates
    for _ in range(2):
        proc = subprocess.run(
            [_pdflatex(), "-interaction=nonstopmode", "-halt-on-error", "formula.tex"],
            cwd=work,
            capture_output=True,
            text=True,
        )
        if proc.returncode != 0 or not (work / "formula.pdf").exists():
            log_path = work / "formula.log"
            log_tail = log_path.read_text(encoding="utf-8", errors="replace")[-1500:] if log_path.exists() else proc.stdout[-1500:]
            shutil.rmtree(work, ignore_errors=True)
            raise RuntimeError(f"pdflatex failed for annotated formula: {tex_body}\n{log_tail}")

    png_base = work / "formula"
    subprocess.run(
        ["pdftoppm", "-png", "-r", "260", str(work / "formula.pdf"), str(png_base)],
        check=True,
        capture_output=True,
    )
    rendered = work / "formula-1.png"
    if not rendered.exists():
        shutil.rmtree(work, ignore_errors=True)
        raise RuntimeError(f"pdftoppm produced no PNG for annotated formula: {tex_body}")
    _crop_onto_strip(rendered, dest, bg=(255, 255, 255))
    shutil.rmtree(work, ignore_errors=True)
    return str(dest)
