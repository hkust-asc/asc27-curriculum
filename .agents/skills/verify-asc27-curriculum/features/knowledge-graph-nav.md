# Knowledge Graph & Navigation

The landing page (`site/index.html`) lets a beginner explore the 5-layer HPC/AI dependency graph, click any node to see its bottleneck and core formula, and jump directly into the matching interactive lab or stage page.

## Sub-features

- `kg-initial` renders the 5-layer SVG (`#kg-svg`) with a default selected node and populated detail panel (`#kg-detail`).
- `kg-node-select` updates `#kg-detail` (title, bottleneck, formula, lab link) when any `.kg-node` is clicked.
- `kg-deep-link` jumps from the detail panel's CTA link to the exact lab anchor (`#cache`, `#roofline`, `#power`, etc.).
- `nav-bar` switches cleanly across all 6 pages (`Home`, `Stage 1: Physics`, `Stage 2: Parallel`, `Stage 3: AI & Porting`, `Stage 4: ASC Sprint`, `Past Problems`) with the active link highlighted.

## How to get to it (user POV)

- Open `http://127.0.0.1:<port>/index.html` directly.
- Click the brand link `HKUST ASC27 Interactive Lab` or `Home` in the top navigation bar from any subpage.

## Driving it with cua_repl (iab)

Preconditions:

- `serve-site.sh doctor` reports `OK:` for `http://127.0.0.1:<port>`.
- Evidence directory `/tmp/asc27-verify-evidence/$RUN_ID/kg/` exists.

- **Open home page.** Run `let tab = await cua.createBrowserTab("iab", "http://127.0.0.1:<port>/index.html", { visible: false });`. Page heading `Learn HPC and AI Systems by Playing With the Physics` and `#kg-svg` appear; `#kg-detail` is non-empty.
- **Select a graph node.** Click node `A3` (`[data-id="A3"]`) inside `#kg-svg`. `#kg-detail` updates to `A3: Power Wall & DVFS`, shows `P_dyn ~ C_eff * V^2 * f`, and links to `stage4-asc-sprint.html#power`.
- **Follow deep link.** Click the `#kg-detail` action link (`Play Power Wall & DVFS Lab`). Browser navigates to `stage4-asc-sprint.html#power` and the `#power` section is present and interactive.
- **Check pedagogy.** Confirm `#kg-detail` stays concise (bottleneck + formula + link, no multi-paragraph lecture) and visually anchors the 5-layer structure rather than duplicating `slides/pdf/00-overview-roadmap.pdf`.
- **Proof.** Save a screenshot of the selected node state to `/tmp/asc27-verify-evidence/$RUN_ID/kg/node-a3.png` and log the extracted `#kg-detail` text and destination URL after clicking the link.

## Gotchas

- `#site-header` and `#site-footer` are injected client-side by `site/assets/common.js`. If `common.js` fails to load, the nav bar is empty even though `index.html` returned HTTP 200.
- SVG `<g class="kg-node" data-id="...">` elements do not expose button roles; target them via `[data-id="A3"]` or their visible node text.
