# ASC27 Curriculum verification map

This directory is the maintained source for verifying the user-facing behavior and beginner pedagogical quality of the `asc27-curriculum` interactive website (`site/`), docs (`docs/`), and slide decks (`slides/`). Read this index before driving the site, then follow the matching feature file.

## Baseline preconditions

- Serve `site/` locally via `.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh start` on a disposable loopback port (`127.0.0.1:<port>`).
- Isolate concurrent runs with `ASC27_VERIFY_STATE_DIR=/tmp/asc27-verify-$RUN_ID` and `ASC27_VERIFY_PORT=0`.
- Run `.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh doctor` and confirm `OK:` with `pages=8/8` and the current git revision.
- Never drive a server that was not started by this verification run.
- Save proof artifacts outside the server state directory, under `/tmp/asc27-verify-evidence/$RUN_ID/`, so `serve-site.sh stop` never deletes them.

## Driving conventions

- Drive real browser sessions against `http://127.0.0.1:<port>/...` using the Codex in-app browser (`cua_repl` with `"iab"`) or another browser automation harness.
- Prefer ARIA roles, accessible names, and stable element IDs (`#am-f`, `#rf-i`, `#rg-next`, `#pw-f`, `#pp-filters`) over pixel coordinates.
- On every lab you touch, verify both **functional state changes** (controls update the SVG/grid and numeric readouts) and **beginner pedagogy** against `references/pedagogy-rubric.md` (visual-first, bare-minimum text, core-formula intuition, does not just repeat the PPT).
- Also run `.agents/skills/verify-asc27-curriculum/scripts/audit-pedagogy.py --strict` to verify zero broken internal links/anchors and check text density.

## Proof and skip reporting

- Capture the user action and resulting state, not only the initial load.
- UI proof includes a browser screenshot (`*.png`) showing the updated visual/graph and the updated readout/takeaway, plus DOM/text state confirmation.
- Audit proof includes the saved JSON/stdout from `audit-pedagogy.py`.
- Record the feature ID and entry point used with every artifact.
- Report any unreachable path with the attempted command and unmet precondition. Never report a skipped entry point as verified.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior, followed by exactly four H2 sections in this order:

1. `Sub-features`
2. `How to get to it (user POV)`
3. `Driving it with cua_repl (iab)`
4. `Gotchas`

## Features

- [Knowledge Graph & Navigation](./knowledge-graph-nav.md) covers `site/index.html`, the interactive 5-layer graph, detail panel, stage cards, and top navigation bar.
- [Stage 1: Hardware Physics & Roofline](./stage1-physics-labs.md) covers `site/stage1-foundations.html` (Cache Locality, Amdahl vs. Gustafson, Live Roofline).
- [Stage 2: Parallelism & GPU Tiling](./stage2-parallel-labs.md) covers `site/stage2-parallelism.html` (False Sharing, MPI 2D Halo Exchange, CUDA Shared-Memory Tiling).
- [Stage 3: AI Systems & GPU Porting](./stage3-ai-labs.md) covers `site/stage3-ai-systems.html` (VRAM Calculator, Ring All-Reduce Animator, KV Cache Decode, AMSS-NCKU Waterfall).
- [Stage 4: ASC Sprint & Past Problems](./stage4-asc-and-past-problems.md) covers `site/stage4-asc-sprint.html` (HPL Simulator, Power Wall & DVFS, Qubit Memory Wall) and `site/past-problems.html` (filterable archive C01–C10).
