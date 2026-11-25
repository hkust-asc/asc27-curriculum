# Visual & Content Specification (English Edition)

## Language & Tone
- **100% English** across all repository documentation, Mermaid diagrams, SVG/PNG figures, slide text, tables, formulas, callouts, footnotes, and speaker notes.
- Clean, direct, academic/engineering technical writing. Avoid AI-slop clichés: no em dashes (`—`) in slide bullets, no vertical bar lists (`A | B | C`), no "It's not X, it's Y" constructions, no passive filler, no slogan-like hype, no imperative slide titles.
- Strict factual separation: clearly distinguish official ASC27 rules (registration 2026-11-19 to 2027-01-10, preliminary round 2027-01-11 to 2027-02-28, finals May 2027, 5 undergraduates + 1 faculty advisor, max 1 finalist team per university, all deadlines midnight UTC+8) from historical stress-test baselines (ASC22 3 kW, ASC25 4 kW, ASC26 5 kW). Never fabricate ASC27 power cap, hardware specs, or scoring formulas.
- Verified math correction: QiboTN state-vector memory for `complex128` (16 bytes/amplitude) is $16 \cdot 2^n$ bytes: 20 qubits = **16 MiB** (not 16 GB), 40 qubits = **16 TiB** (not 16 PB), correcting the 1024× unit typo on slide p.20 of the ASC26 optimization intro talk.

## Minimalist Color Palette (Academic HPC / HKUST-inspired)
- Canvas background: `#FFFFFF` (slides) / `#FAFBFD` (diagram canvas)
- Surface tint (flat editorial bands only, no cluttered card grids): `#F1F5F9` / `#F8FAFC`
- Primary ink: `#0F172A`
- Secondary ink: `#334155`
- Muted axis/gridline: `#CBD5E1` / `#E2E8F0`
- Primary Accent (Deep HPC Blue): `#0B4F8A`
- Secondary Accent (HKUST Gold): `#C48A1A`
- Teal Accent (Compute / Optimal / Speedup): `#0D9488`
- Coral Accent (Bottleneck / Memory-bound / Alert): `#C2410C`
- Violet Accent (AI / Distributed / Quantum): `#6D28D9`

## SVG Diagram Standards
- Render via `rsvg-convert -d 300 -p 300 -w 1800 input.svg -o output.png` (and `-w 2200` for wide `00_` diagrams).
- Font family in SVG: `Helvetica Neue, Arial, sans-serif` and monospace `Menlo, DejaVu Sans Mono, monospace`.
- Aspect ratio: `viewBox="0 0 960 660"` for right-hand slide visuals; `viewBox="0 0 1280 640"` or `1280 540` for full-width overview diagrams.
- Crisp legibility: minimum 14.5px text in 960×660 canvas, generous margins (≥32px), mathematically computed axes/curves via numpy, zero overlapping or clipped labels.
