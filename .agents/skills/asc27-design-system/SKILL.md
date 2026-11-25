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

- **Webapp (`site/`)**:
  - Render every formula with vendored KaTeX (`site/assets/vendor/katex/`) via the shared helper in `site/assets/common.js`. Never leave raw ASCII math (`^`, `<=`, `->`, `*`) in visible formula blocks.
  - Every formula block MUST include interactive **symbol annotations**: clickable/hoverable symbol chips below or linked to the formula (`.sym-chip` with tooltip + active highlight) so a complete beginner immediately knows what every letter (`N`, `I`, `B`, `f`, `k`, `alpha`, `Phi`, `G`) means and its units.
- **Slides (`scripts/build_decks.py`, `scripts/odp_builder.py`, `scripts/formula_render.py`)**:
  - Render every `formula_tex` with local `pdflatex` to a cropped PNG cached in `slides/.formula-cache/`.
  - Every slide with a `formula_tex` MUST populate `formula_symbols` (list of `(symbol, meaning)` pairs) so no symbol appears undefined on a slide.

## 4. Beginner Pedagogy & Writing Rules

- Target audience: undergraduate beginner in HPC, Linux, and AI.
- Lead with physical intuition and one core formula; cut low-level trivia.
- Short sentences (under 20 words in slides/steps, under 25 words in web prose).
- No em dashes, no "not X, but Y" filler, no raw ASCII arrows (`->`, `=>`, `<=`, `>=`) in visible text.
- Interactive HTML labs must add visual intuition beyond the slides (animations, sliders, live plots), never repeat slide bullets verbatim.
