# Visual and Content Specification

## Design Philosophy (Anatomy x Designed-to-Scale)
- **Styling (`skills.wheresryan.sh/anatomy`)**: Crisp neutral paper canvas (`#FAFAFA`), pure white elevated cards (`#FFFFFF`), hairline borders (`#EBEBEB`), high-contrast editorial ink (`#171717` / `#525252` / `#737373`), generous breathing room, and one focused accent color per figure.
- **Interactive Architecture (`designed-to-scale.vercel.app`)**: Persistent left course-tree rail, centered live stage with HUD metric chips and step timeline, and concise side controls/guide with LaTeX formulas and interactive symbol annotations.
- **First-Principles Presentation**:
  - Represent dependencies as an interactive **Knowledge Graph** (layered DAG with curved edges and neighborhood highlighting).
  - Represent time and deadlines as a proportional **Timeline** (Nov 2026 to May 2027).
  - Represent the 24-week curriculum as a visual **Roadmap Track** with clickable stage spans and milestones.
  - Represent formulas in **LaTeX** (KaTeX in `site/`, `pdflatex` PNGs in `slides/`) with explicit **symbol definitions** (hover/click chips on web, inline symbol legend in slides).

## Language and Style (ASD-STE100)
- Write all documentation, diagrams, slides, and web pages in plain English.
- Use short sentences (under 20 words for steps, under 25 words for explanations).
- Keep paragraphs to 2 to 4 sentences. Put one idea in each sentence.
- Use active voice and simple verbs (`is`, `are`, `has`, `runs`, `measures`).
- State facts directly. Avoid "not X, but Y" phrasing, em dashes, hype, and repeated rule warnings.
- Keep ASC27 official dates separate from historical baselines (ASC22 3 kW, ASC25 4 kW, ASC26 5 kW).
- Use exact binary memory units for QiboTN state vectors ($16 \cdot 2^n$ bytes): 20 qubits = 16 MiB, 40 qubits = 16 TiB.

## Color Palette
- Canvas background: `#FAFAFA` (web, diagrams, and slide ground) / `#FFFFFF` (elevated cards and plot surfaces)
- Surface well: `#F1F1F1` / `#F5F5F5`
- Hairline border and gridline: `#EBEBEB` / `#E5E5E5`
- Primary ink: `#171717`
- Secondary ink: `#525252`
- Muted ink and axes: `#737373` / `#A3A3A3`
- Deep HPC Blue (Primary): `#0B4F8A`
- HKUST Gold (Secondary): `#C48A1A`
- Teal (Compute / Speedup / Pass): `#0D9488`
- Coral (Bottleneck / Memory-bound / Alert): `#C2410C`
- Violet (AI / Distributed / Quantum): `#6D28D9`

## SVG Diagram Standards
- Render PNGs with `rsvg-convert -d 300 -p 300 -w 1800 input.svg -o output.png` (use `-w 2200` for wide `00_` overview figures).
- Fonts: `Inter, Helvetica Neue, Arial, sans-serif` for labels, `Georgia, serif` italic for editorial section numerals, and `SF Mono, Menlo, DejaVu Sans Mono, monospace` for code and tabular numbers.
- Aspect ratios: `viewBox="0 0 960 660"` for slide visuals; `viewBox="0 0 1280 640"` or `1280 540` for overview figures.
- Keep minimum label size at 14.5px on a 960x660 canvas with margins of at least 32px.

## Design Skill Reference
- Detailed component patterns, KaTeX formula conventions, and slide symbol-legend rules live in `.agents/skills/asc27-design-system/SKILL.md`.
