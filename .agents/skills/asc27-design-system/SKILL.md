---
name: asc27-design-system
description: "Design system and visual pedagogy guide for the HKUST ASC27 interactive curriculum, SVG diagrams, and slide decks. Combines Designed-to-Scale interactive layout architecture with Anatomy's crisp editorial palette and visual restraint. Use whenever building or revising web pages in site/, diagrams in scripts/gen_viz_*.py, or slides in scripts/build_decks.py."
---

# ASC27 Design System & Visual Pedagogy

Use this skill for every visual, interactive, and slide change in `hkust-asc/asc27-curriculum`.

## 1. Visual Identity (Anatomy Styling x Designed-to-Scale Architecture)

- **Aesthetic foundation (from `skills.wheresryan.sh/anatomy`)**:
  - Neutral paper ground `#FAFAFA`, crisp white surfaces `#FFFFFF`, subtle wells `#F1F1F1` / `#F6F6F6`, hairline rules `#EBEBEB` / `#E5E5E5`.
  - Ink hierarchy: primary `#171717`, secondary `#525252`, muted `#737373` / `#8F8F8F`, faint `#BDBDBD`.
  - Soft hairline card elevation (`0 0 0 1px rgb(0 0 0 / 0.05), 0 1px 2px rgb(0 0 0 / 0.04), 0 4px 12px -4px rgb(0 0 0 / 0.05)`), generous whitespace, no heavy neon gradients.
  - Typography: clean sans (`Inter` / system UI) for prose and UI, italic editorial serif (`EB Garamond` / Georgia) for section indices (`01`, `02`) and emphasis, tabular monospace (`SF Mono` / `JetBrains Mono`) for numeric readouts and code.
  - Accent restraint: one semantic accent per figure or stage so the learner's eye lands immediately on what moves:
    - Deep HPC Blue `#0B4F8A` (Physics / Primary)
    - Teal `#0D9488` (Parallelism / Optimal / Hit)
    - Violet `#6D28D9` (AI Systems / Memory)
    - Coral `#C2410C` (Bottleneck / Alert / Miss)
    - HKUST Gold `#C48A1A` (Profiling / Milestones)
- **Interactive workbench architecture (from `designed-to-scale.vercel.app`)**:
  - **Left navigation rail / course tree**: collapsible stage modules, live progress checkmarks, and jump links to every lab and overview view.
  - **Center stage**: live visual artifact framed with top-left numeric HUD chips (tabular-nums, semantic left-edge indicator bar: good/warn/bad), top-right compact tools (play/step/reset/presets), bottom legend, and optional horizontal step-timeline bar underneath.
  - **Right/adjacent guide & controls rail**: concise intuition prose (1 to 3 short sentences), KaTeX-rendered core formula with interactive hover/click symbol annotations, and direct manipulation sliders/toggles.

## 2. First-Principles Information Presentation

Never default to a flat HTML or slide table when the underlying structure has geometry, time, or topology:

- **Knowledge Graph (`site/index.html`)**: Render as an actual interactive directed graph (layered node-edge topology with curved dependency edges, hover/click neighborhood highlighting, and cross-layer ASC bridge paths), never a rigid grid table.
- **Curriculum Roadmap (`site/index.html`, `00-overview-roadmap`)**: Render as a visual 24-week spatial roadmap track with stage spans, milestone markers, and clickable module stops, not a grid of uniform cards or a text table.
- **Official Schedule / Milestones (`site/index.html`, `00-overview-roadmap`)**: Render as a horizontal proportional timeline from Nov 2026 to May 2027 with phase bars, deadline pins, and today/cutoff markers, not a 3-column table.
- **Past ASC Problems (`site/past-problems.html`)**: Pair a visual Bottleneck x Hardware Matrix / Timeline view with filterable cards and an interactive problem inspector showing LaTeX math and direct lab links.

## 3. LaTeX Formulas & Mandatory Symbol Clarity

Use the **Color-Coded Annotated Formula** pattern across both the interactive webapp and slide decks so a complete beginner can visually map every variable to its physical meaning at a glance:

- **Shared Visual Spec (Web + Slides)**:
  - **5-color semantic cycle**:
    1. Blue (`#2563EB` stroke / `#EFF6FF` fill)
    2. Green (`#16A34A` stroke / `#F0FDF4` fill)
    3. Violet (`#7C3AED` stroke / `#F5F3FF` fill)
    4. Orange (`#EA580C` stroke / `#FFF7ED` fill)
    5. Teal (`#0D9488` stroke / `#F0FDFA` fill)
  - **Consistent multi-occurrence coloring**: If a variable appears more than once in the same equation (for example, `P_peak` and `B` in Roofline, or `p` and `G` in Ring All-Reduce), wrap **every occurrence** in the same color-coded rounded pill box.
  - **Curved upward callout arrows**: Draw a color-matched curved arrow from each legend card underneath up to its primary term pill in the formula (routing around fraction bars for numerator terms so arrows never cross denominators).
- **Webapp (`site/assets/common.js`, `site/assets/style.css`)**:
  - Render every formula with vendored KaTeX (`site/assets/vendor/katex/`) via `window.ASC27.renderFormulaBox(container, { tex, symbols })`. Never leave raw ASCII math (`^`, `<=`, `->`, `*`) in visible formula blocks.
  - `renderFormulaBox` wraps every matched variable occurrence in `.ft-pill.ft-c{0..4}` via KaTeX `\htmlClass` + `\htmlData`, renders `.sym-card` boxes below, draws curved SVG arrows in `.formula-arrows`, and shows a color-matched `.sym-popover` on hover, focus, or click while highlighting all occurrences of that variable and dimming others.
- **Slides (`scripts/build_decks.py`, `scripts/odp_builder.py`, `scripts/formula_render.py`)**:
  - Every slide with a `formula_tex` MUST populate `formula_symbols` (list of `(symbol, meaning)` pairs).
  - `odp_builder.py` calls `render_annotated_formula_png(formula_tex, formula_symbols)` which compiles a 2-pass TikZ + `pdflatex` annotated diagram cached in `slides/.formula-cache/`.

## 4. Beginner Pedagogy & Writing Rules

- Target audience: undergraduate beginner in HPC, Linux, and AI.
- Lead with physical intuition and one core formula; cut low-level trivia.
- Short sentences (under 20 words in slides/steps, under 25 words in web prose).
- No em dashes, no "not X, but Y" filler, no raw ASCII arrows (`->`, `=>`, `<=`, `>=`) in visible text.
- Interactive HTML labs must add visual intuition beyond the slides (animations, sliders, live plots), never repeat slide bullets verbatim.
