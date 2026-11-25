# Visual and Content Specification

## Language and Style (ASD-STE100)
- Write all documentation, diagrams, slides, and web pages in plain English.
- Use short sentences (under 20 words for steps, under 25 words for explanations).
- Keep paragraphs to 2 to 4 sentences. Put one idea in each sentence.
- Use active voice and simple verbs (`is`, `are`, `has`, `runs`, `measures`).
- State facts directly. Avoid "not X, but Y" phrasing, em dashes, hype, and repeated rule warnings.
- Keep ASC27 official dates separate from historical baselines (ASC22 3 kW, ASC25 4 kW, ASC26 5 kW).
- Use exact binary memory units for QiboTN state vectors ($16 \cdot 2^n$ bytes): 20 qubits = 16 MiB, 40 qubits = 16 TiB.

## Color Palette
- Canvas background: `#FFFFFF` (slides) / `#FAFBFD` (diagrams and web cards)
- Surface tint: `#F1F5F9` / `#F8FAFC`
- Primary ink: `#0F172A`
- Secondary ink: `#334155`
- Muted axis and gridline: `#CBD5E1` / `#E2E8F0`
- Deep HPC Blue (Primary): `#0B4F8A`
- HKUST Gold (Secondary): `#C48A1A`
- Teal (Compute / Speedup / Pass): `#0D9488`
- Coral (Bottleneck / Memory-bound / Alert): `#C2410C`
- Violet (AI / Distributed / Quantum): `#6D28D9`

## SVG Diagram Standards
- Render PNGs with `rsvg-convert -d 300 -p 300 -w 1800 input.svg -o output.png` (use `-w 2200` for wide `00_` overview figures).
- Fonts: `Helvetica Neue, Arial, sans-serif` for labels and `Menlo, DejaVu Sans Mono, monospace` for code.
- Aspect ratios: `viewBox="0 0 960 660"` for slide visuals; `viewBox="0 0 1280 640"` or `1280 540` for overview figures.
- Keep minimum label size at 14.5px on a 960x660 canvas with margins of at least 32px.
