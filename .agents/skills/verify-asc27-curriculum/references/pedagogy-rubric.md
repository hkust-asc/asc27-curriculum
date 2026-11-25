# Pedagogy & Explorable-Explanation Rubric (ASC27 Beginner Audience)

The target learner is an undergraduate beginner in HPC, Linux, and AI systems. Every review of `site/`, `docs/`, `diagrams/`, or `slides/` checks both **functional behavior** (the widget works) and **pedagogical value** (a complete outsider builds intuition without drowning in detail).

## Grounded External & Local Standards

- **Explorable Explanations** (Bret Victor, *Up and Down the Ladder of Abstraction*; Distill.pub): an interactive page exists to let the learner *play with a parameter and watch the system react*, not to mirror slide bullet points. Concrete first, then parameter sweep, then general rule.
- **Cognitive Load & Visual-First** (Mayer's Multimedia Principles; 3Blue1Brown): pair a diagram or live plot with bare-minimum text that anchors what each axis, color, and lever means. Cut decorative prose and redundant text that repeats the slide deck.
- **Core-Formula Spine** (this repo's `DESIGN_SPEC.md` and `docs/knowledge-graph.md`): extend intuition around a few durable formulas (`R = min(P_peak, B * I)`, `S(k) = 1 / ((1-f) + f/k)`, `T(m) = alpha + m/B`, `P_dyn ~ C * V^2 * f`, `M_qubit(n) = 16 * 2^n`, `T_ring = 2((p-1)/p) * G / B`) instead of cataloguing hardware trivia.
- **Plain English** (ASD-STE100 in `DESIGN_SPEC.md` + pstack `teach` / `technical-writing`): short sentences (under 20 words for steps, under 25 words for explanations), active voice, one idea per sentence, no em dashes, no "not X, but Y" framing, no unexplained acronyms on first sight.

## Checklist for Every Interactive HTML Lab (`site/*.html`)

1. **Adds intuition beyond the slides (No PPT repetition):**
   - Pass: changing a slider or stepping an animation visibly changes a graph, grid, or state diagram and reveals a non-obvious threshold (ridge point, swap cliff, OOM boundary, power cap, cache-line bounce).
   - Fail: the section is mostly prose cards or bullet lists that restate `slides/pdf/*.pdf` without a reactive visual.
2. **Visual-first, bare-minimum text:**
   - Pass: a complete outsider can tell what the plot shows from its title, axis labels, legend, and a 1–2 sentence takeaway that updates with the state.
   - Fail: multi-paragraph lectures on the HTML page, or unlabeled axes/numbers where an outsider cannot tell what moved or why it matters.
3. **Anchored to one core formula or physical limit:**
   - Pass: each lab highlights 1 core relationship and lets the learner push it past a cliff or knee.
   - Fail: dumps 6+ unrelated knobs or low-level flags before the learner grasps the main bottleneck.
4. **Beginner-safe defaults & clear cause-and-effect:**
   - Pass: the initial load already shows a readable, meaningful state; every button/slider causes an immediate, obvious visual change plus a plain-English takeaway.
   - Fail: broken initial SVG, dead controls, NaN/clipped labels, or jargon-only output without plain interpretation.

## Checklist for Docs & Slides (`docs/*.md`, `slides/`)

1. **Concise intuition over exhaustive detail:** explain the *why* and the *core formula* first; push long command references or vendor specifics to lab appendices.
2. **Sentence and paragraph budget:** explanations under 25 words per sentence, paragraphs 2–4 sentences, active voice, consistent naming across docs, slides, and web labs.
3. **Cross-surface consistency:** official ASC27 dates stay separate from historical baselines (ASC22 3 kW, ASC25 4 kW, ASC26 5 kW), and binary units match exact math (`16 * 2^20 = 16 MiB`, `16 * 2^40 = 16 TiB`).
