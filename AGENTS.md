# HKUST ASC27 Curriculum — Repository Rules

Follow these rules on every change to `site/`, `scripts/`, `diagrams/`, `slides/`, or `docs/`.

## Design & Visual Pedagogy
- Follow `.agents/skills/asc27-design-system/SKILL.md` and `DESIGN_SPEC.md`.
- Use the **Anatomy** neutral palette (`#FAFAFA` ground, `#FFFFFF` cards, `#EBEBEB` hairlines, `#171717` / `#525252` / `#737373` inks) with one semantic accent per figure (`#0B4F8A`, `#0D9488`, `#6D28D9`, `#C2410C`, `#C48A1A`).
- Use the **Designed-to-Scale** workbench layout: persistent left course-tree rail, centered interactive stage with HUD stat chips, and concise controls/guide.
- Present structure from first principles: use a **directed graph** for dependencies, a **visual roadmap track** for multi-week curricula, and a **proportional timeline** for schedules instead of flat HTML tables.

## Formulas & Symbol Clarity
- **Webapp (`site/`)**: Render all formulas using vendored KaTeX (`site/assets/vendor/katex/`) via `window.ASC27.renderFormulaBox(...)` with interactive hover/click symbol chips. Never ship raw ASCII math in visible formula containers.
- **Slides (`scripts/build_decks.py`)**: Every slide with `formula_tex` must also define `formula_symbols` (`List[Tuple[str, str]]`) so every symbol is explicitly explained on the slide.

## Beginner Writing Style (ASD-STE100)
- Keep slide bullets under 20 words and web prose sentences under 25 words.
- No em dashes (`—`), no "not X, but Y" phrasing, and no raw ASCII arrows/inequalities (`->`, `=>`, `<=`, `>=`) in visible text.
- Interactive HTML labs must add visual intuition beyond the slide decks, never repeat slide bullets verbatim.

## Verification & Pre-Commit Gate
- Before committing, run:
  ```bash
  python3 .agents/skills/verify-asc27-curriculum/scripts/audit-pedagogy.py --strict
  python3 .agents/skills/verify-formal-ring-allreduce/scripts/verify-ring.py
  ```
- To enable the automatic local pre-commit hook:
  ```bash
  git config core.hooksPath .githooks
  ```
- Rebuild diagrams and decks after editing `scripts/`:
  ```bash
  uv run --with numpy --with pillow python3 scripts/generate_all_diagrams.py
  uv run --with pillow python3 scripts/build_decks.py
  ```
