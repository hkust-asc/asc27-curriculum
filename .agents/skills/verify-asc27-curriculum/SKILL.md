---
name: verify-asc27-curriculum
description: "Verify the HKUST ASC27 interactive HTML curriculum (site/), docs, and generated slides the way a beginner learner uses them. Launches an isolated local HTTP server, drives live widgets in the browser, audits visual-first beginner pedagogy (intuition over detail, graphs/widgets over PPT text repetition), and preserves proof artifacts."
---

# Verify ASC27 Curriculum

Use this skill after editing any page in `site/`, any curriculum doc in `docs/`, or any diagram/deck script in `scripts/`. It proves both **runtime behavior** (the interactive HTML widgets, SVGs, sliders, and navigation actually work in a real browser) and **beginner pedagogical quality** (clear, concise intuition around core formulas; visual-first interactive labs that add insight beyond the PPT slides rather than repeating them).

Read [`features/README.md`](features/README.md) for the maintained feature map and [`references/pedagogy-rubric.md`](references/pedagogy-rubric.md) for the beginner clarity and explorable-explanation rubric before driving.

## Launch

Start an isolated loopback static server for `site/` with a unique `RUN_ID` so concurrent runs never collide:

```bash
export RUN_ID="run-$(date +%s)-$$"
export ASC27_VERIFY_STATE_DIR="/tmp/asc27-verify-state-$RUN_ID"
export ASC27_VERIFY_PORT=0
export ASC27_EVIDENCE_DIR="/tmp/asc27-verify-evidence/$RUN_ID"
mkdir -p "$ASC27_EVIDENCE_DIR"

.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh start
```

Ready means `serve-site.sh start` prints `started pid=<PID> url=http://127.0.0.1:<PORT>` and `doctor` reports `pages=8/8`.

If you also edited diagram or deck generators (`scripts/gen_viz_*.py`, `scripts/build_decks.py`), rebuild first with:

```bash
python3 scripts/generate_all_diagrams.py
python3 scripts/build_decks.py
```

## Doctor

Run this read-only check before driving and whenever anything looks off:

```bash
.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh doctor
```

Expected output: `OK: pid=<PID> url=http://127.0.0.1:<PORT> pages=8/8 rev=<git-sha>`. If it fails, stop and fix the server or missing file before driving.

## Drive

1. **Run the automated pedagogy and link audit** (checks every `site/*.html` link/anchor, visual-widget-to-lab ratio, static word density per lab, and ASD-STE100 sentence length/style rules in `docs/*.md` and `site/*.html`):

```bash
python3 .agents/skills/verify-asc27-curriculum/scripts/audit-pedagogy.py \
  --strict \
  --out "$ASC27_EVIDENCE_DIR/pedagogy-audit.json"
```

2. **Drive the live site in a real browser** using Codex's in-app browser (`cua_repl` with `"iab"`) against `http://127.0.0.1:<PORT>/...` following the exact recipe in [`features/`](features/README.md):
   - Open the page via `await cua.createBrowserTab("iab", url, { visible: false })`.
   - Interact with real user controls (buttons like `#mode-col`, `#cache-step`, `#rg-next`, `[data-cap="3000"]`, `[data-f="cpu"]`, and range sliders `#am-f`, `#rf-i`, `#vr-g`, `#pw-f` with `input` events).
   - Observe both the updated numeric readouts/takeaways and the rendered SVG/grid visual.
   - Grade the page visually against [`references/pedagogy-rubric.md`](references/pedagogy-rubric.md):
     - Does the interactive widget give extra intuition beyond the slide deck, rather than repeating PPT bullets?
     - Are axes, legends, thresholds, and takeaways clear to a complete HPC/Linux/AI outsider with minimal text?
     - Is the explanation centered on 1 core formula or physical principle without drowning in low-level trivia?

## Evidence

Store all proof artifacts under `$ASC27_EVIDENCE_DIR` (`/tmp/asc27-verify-evidence/$RUN_ID/`), never inside `$ASC27_VERIFY_STATE_DIR`.

Proof standards:

- Exercise the real user path in the browser; never call internal drawing helpers directly to fake a pass.
- Capture **before and after** states (the user action + the resulting DOM/SVG state), not just an initial screenshot.
- Include at least:
  - `$ASC27_EVIDENCE_DIR/pedagogy-audit.json` from `audit-pedagogy.py`.
  - One or more browser screenshots (`*.png`) showing the live visual after interaction, plus recorded before/after stat values and the feature ID + entry point used.
- Do not weaken a check when a widget or doc has a real bug (for example, broken Ring All-Reduce completion in Stage 3); report it as a finding.

## Cleanup

Tear down only the server instance started by this run:

```bash
.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh stop
```

Never kill `python3` by process name. `serve-site.sh stop` kills only the recorded PID and deletes `$ASC27_VERIFY_STATE_DIR`, leaving `$ASC27_EVIDENCE_DIR` intact. Verify `ls -la "$ASC27_EVIDENCE_DIR"` after cleanup.

## Helpers

Both helper scripts are executable:

- `.agents/skills/verify-asc27-curriculum/scripts/serve-site.sh {start|doctor|stop}` — starts, checks, and cleanly stops an isolated loopback server for `site/`.
- `.agents/skills/verify-asc27-curriculum/scripts/audit-pedagogy.py [--strict] [--out <json>]` — audits broken internal links/anchors, visual-widget coverage, static word density per lab, and ASD-STE100 sentence/style rules across `site/*.html` and `docs/*.md`.
