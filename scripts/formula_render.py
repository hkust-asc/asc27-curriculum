#!/usr/bin/env python3
"""Render a LaTeX math string to a tightly cropped PNG for slide formula strips."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import tempfile
from pathlib import Path

from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
CACHE_DIR = ROOT / "slides" / ".formula-cache"
STRIP_BG = (248, 250, 252)
PDFLATEX_CANDIDATES = (
    "pdflatex",
    "/Library/TeX/texbin/pdflatex",
    "/usr/local/texlive/2026basic/bin/universal-darwin/pdflatex",
)

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


def _pdflatex() -> str:
    for candidate in PDFLATEX_CANDIDATES:
        found = shutil.which(candidate) if "/" not in candidate else candidate
        if found and Path(found).exists():
            return found
    raise FileNotFoundError("pdflatex not found. Install a TeX distribution to render slide formulas.")


def _crop_onto_strip(src: Path, dest: Path) -> None:
    image = Image.open(src).convert("RGB")
    diff = ImageChops.difference(image, Image.new("RGB", image.size, (255, 255, 255)))
    bbox = diff.getbbox()
    if bbox is None:
        raise RuntimeError(f"LaTeX render produced an empty page: {src}")
    pad = 10
    left = max(0, bbox[0] - pad)
    top = max(0, bbox[1] - pad)
    right = min(image.width, bbox[2] + pad)
    bottom = min(image.height, bbox[3] + pad)
    cropped = image.crop((left, top, right, bottom))
    canvas = Image.new("RGB", cropped.size, STRIP_BG)
    ink = cropped.convert("L").point(lambda p: 0 if p > 248 else 255)
    canvas.paste(cropped, mask=ink)
    dest.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(dest, "PNG")


def render_formula_png(tex_body: str, cache_dir: Path = CACHE_DIR) -> str:
    """Return a cached PNG path for display math. `tex_body` is the math interior, without `$`."""
    key = hashlib.sha256(tex_body.encode("utf-8")).hexdigest()[:20]
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
