#!/usr/bin/env python3
"""Audit beginner clarity, visual-first balance, and link integrity across asc27-curriculum."""

from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
SITE_DIR = ROOT / "site"
DOCS_DIR = ROOT / "docs"

SITE_PAGES = [
    "index.html",
    "stage1-foundations.html",
    "stage2-parallelism.html",
    "stage3-ai-systems.html",
    "stage4-asc-sprint.html",
    "past-problems.html",
]

STYLE_BANS = [
    ("em_dash", re.compile(r"—")),
    ("not_x_but_y", re.compile(r"\bnot\s+[^.!?\n]{1,40},\s*but\b", re.IGNORECASE)),
]


def strip_html(html: str) -> str:
    cleaned = re.sub(r"<script[\s\S]*?</script>", " ", html)
    cleaned = re.sub(r"<style[\s\S]*?</style>", " ", cleaned)
    cleaned = re.sub(r"<svg[\s\S]*?</svg>", " ", cleaned)
    cleaned = re.sub(r"<[^>]+>", " ", cleaned)
    return re.sub(r"\s+", " ", cleaned).strip()


def sentence_lengths(text: str) -> list[int]:
    parts = re.split(r"(?<=[.!?])\s+", text)
    lengths: list[int] = []
    for part in parts:
        words = re.findall(r"[A-Za-z0-9_'-]+", part)
        if len(words) >= 4:
            lengths.append(len(words))
    return lengths


def audit_site_page(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    text = strip_html(raw)
    words = re.findall(r"[A-Za-z0-9_'-]+", text)
    sent_lens = sentence_lengths(text)
    long_sents = [n for n in sent_lens if n > 25]

    svgs = len(re.findall(r"<svg\b", raw))
    canvas_or_bars = len(re.findall(r'id="(?:cache-grid|vr-bars|pp-grid)"', raw))
    visual_widgets = svgs + canvas_or_bars
    controls = len(re.findall(r"<(?:input|button|select)\b", raw))
    lab_cards = len(re.findall(r'<section[^>]*class="lab-card"', raw))

    # Check internal relative hrefs and hash targets
    broken_links: list[str] = []
    for href in re.findall(r'href="([^"]+)"', raw):
        if href.startswith(("http://", "https://", "mailto:", "#")) or "${" in href:
            continue
        target_file, _, frag = href.partition("#")
        target_path = SITE_DIR / target_file
        if not target_path.exists():
            broken_links.append(href)
        elif frag:
            target_raw = target_path.read_text(encoding="utf-8")
            if f'id="{frag}"' not in target_raw:
                broken_links.append(href)

    # Also check JS-embedded lab links like link: "stage1-foundations.html#roofline"
    for href in re.findall(r'(?:link|lab):\s*"([^"]+)"', raw):
        target_file, _, frag = href.partition("#")
        target_path = SITE_DIR / target_file
        if not target_path.exists():
            broken_links.append(href)
        elif frag:
            target_raw = target_path.read_text(encoding="utf-8")
            if f'id="{frag}"' not in target_raw:
                broken_links.append(href)

    style_hits = {name: len(pat.findall(text)) for name, pat in STYLE_BANS}
    words_per_lab = round(len(words) / max(1, lab_cards), 1)

    warnings: list[str] = []
    if path.name.startswith("stage") and visual_widgets < lab_cards:
        warnings.append(f"fewer visual widgets ({visual_widgets}) than lab cards ({lab_cards})")
    if path.name.startswith("stage") and controls < lab_cards * 2:
        warnings.append(f"low interactivity: {controls} controls across {lab_cards} lab cards")
    if words_per_lab > 180:
        warnings.append(f"text-heavy page: {words_per_lab} static words/lab (>180)")
    if long_sents:
        warnings.append(f"{len(long_sents)} sentences exceed 25 words (max={max(long_sents)})")
    for name, count in style_hits.items():
        if count > 0:
            warnings.append(f"style rule hit: {name}={count}")

    return {
        "file": str(path.relative_to(ROOT)),
        "static_words": len(words),
        "lab_cards": lab_cards,
        "words_per_lab": words_per_lab,
        "visual_widgets": visual_widgets,
        "controls": controls,
        "long_sentences_over_25w": len(long_sents),
        "broken_links": broken_links,
        "style_hits": style_hits,
        "warnings": warnings,
    }


def audit_doc(path: Path) -> dict:
    raw = path.read_text(encoding="utf-8")
    # Strip fenced code blocks and markdown table separator lines
    no_code = re.sub(r"```[\s\S]*?```", " ", raw)
    prose_lines = [
        line
        for line in no_code.splitlines()
        if line.strip()
        and not line.strip().startswith(("#", "|", "![", "---"))
    ]
    prose = " ".join(prose_lines)
    sent_lens = sentence_lengths(prose)
    long_sents = [n for n in sent_lens if n > 25]
    style_hits = {name: len(pat.findall(no_code)) for name, pat in STYLE_BANS}
    words = re.findall(r"[A-Za-z0-9_'-]+", no_code)

    warnings: list[str] = []
    if long_sents:
        warnings.append(f"{len(long_sents)} prose sentences exceed 25 words (max={max(long_sents)})")
    for name, count in style_hits.items():
        if count > 0:
            warnings.append(f"style rule hit: {name}={count}")

    return {
        "file": str(path.relative_to(ROOT)),
        "words": len(words),
        "long_sentences_over_25w": len(long_sents),
        "style_hits": style_hits,
        "warnings": warnings,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description="Audit asc27-curriculum clarity and visual-first metrics.")
    parser.add_argument("--out", help="Write JSON report to this path")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on broken links")
    args = parser.parse_args()

    site_reports = [audit_site_page(SITE_DIR / name) for name in SITE_PAGES]
    doc_reports = [audit_doc(p) for p in sorted(DOCS_DIR.glob("*.md"))]

    broken_total = sum(len(r["broken_links"]) for r in site_reports)
    report = {
        "site": site_reports,
        "docs": doc_reports,
        "broken_link_count": broken_total,
    }

    if args.out:
        out_path = Path(args.out)
        out_path.parent.mkdir(parents=True, exist_ok=True)
        out_path.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")

    print("== Site Visual-First & Clarity Audit ==")
    for r in site_reports:
        status = "FAIL" if r["broken_links"] else ("WARN" if r["warnings"] else "PASS")
        print(
            f"[{status}] {r['file']}: {r['static_words']} words, "
            f"{r['visual_widgets']} visuals, {r['controls']} controls, "
            f"{r['words_per_lab']} w/lab, broken_links={len(r['broken_links'])}"
        )
        for b in r["broken_links"]:
            print(f"   broken link: {b}")
        for w in r["warnings"]:
            print(f"   warn: {w}")

    print("\n== Docs Readability Audit ==")
    for r in doc_reports:
        status = "WARN" if r["warnings"] else "PASS"
        print(f"[{status}] {r['file']}: {r['words']} words, >25w_sents={r['long_sentences_over_25w']}")
        for w in r["warnings"]:
            print(f"   warn: {w}")

    if args.strict and broken_total > 0:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
