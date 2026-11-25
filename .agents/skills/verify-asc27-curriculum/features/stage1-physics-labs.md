# Stage 1: Hardware Physics & Roofline

Stage 1 (`site/stage1-foundations.html`) teaches three foundational bottlenecks through live widgets: 64-byte cache-line locality (`#cache`), Amdahl vs. Gustafson scaling (`#amdahl`), and the log-log Roofline model (`#roofline`).

## Sub-features

- `s1-cache-walk` steps or plays through the 8x8 matrix (`#cache-grid`) in row-major (`#mode-row`) vs. column-major (`#mode-col`), updating hits (`#c-hits`), misses (`#c-misses`), and hit rate (`#c-rate`).
- `s1-amdahl-sweep` moves `#am-f` (parallel fraction) and `#am-k` (cores), updating `#am-svg`, Amdahl speedup (`#am-s`), hard ceiling (`#am-max`), and Gustafson (`#am-g`).
- `s1-roofline-regime` moves `#rf-p`, `#rf-b`, `#rf-i` (or clicks preset kernel buttons `[data-i]`), shifting the dot on `#rf-svg` across the ridge point `I_b = P_peak / B` and flipping `#rf-reg` between `Memory` and `Compute`.

## How to get to it (user POV)

- Click `Stage 1: Physics` in the top nav bar.
- Click the `Hardware Physics & Roofline` stage card on `index.html`.
- Follow deep links `stage1-foundations.html#cache`, `#amdahl`, or `#roofline` from the Knowledge Graph.

## Driving it with cua_repl (iab)

Preconditions:

- `serve-site.sh doctor` reports `OK:` for `http://127.0.0.1:<port>`.
- Evidence directory `/tmp/asc27-verify-evidence/$RUN_ID/stage1/` exists.

- **Open Stage 1.** Navigate to `http://127.0.0.1:<port>/stage1-foundations.html`. All three lab cards (`#cache`, `#amdahl`, `#roofline`) render with non-empty `#cache-grid`, `#am-svg`, and `#rf-svg`.
- **Drive Cache Locality.** Click `#cache-step` 4 times in default `Row-major (ikj)` mode; `#c-misses` becomes `1`, `#c-hits` becomes `3`, `#c-rate` becomes `75%`. Switch to `#mode-col` (`Column-major (ijk)`) and click `#cache-step` 4 times; `#c-misses` becomes `4`, `#c-hits` stays `0`, `#c-rate` is `0%`.
- **Drive Amdahl vs. Gustafson.** Set `#am-f` to `90` and `#am-k` to `64` and dispatch `input`. `#am-max` updates to `10.0x`, `#am-s` updates to `8.77x`, and `#am-msg` names the serial wall-time share.
- **Drive Roofline.** Set `#rf-i` to `2.0` (100 FLOP/B, well above `I_b = 15.0`) and dispatch `input`. `#rf-reg` flips from `Memory` to `Compute`, `#rf-r` clamps at `30.00 TF/s`, and `#rf-msg` switches to compute-bound guidance.
- **Check pedagogy.** Verify each lab teaches via the live grid/plot with minimal text (no wall of PPT bullets) and that an outsider can see why `75% vs 0%`, the `1/(1-f)` ceiling, and the `I_b` ridge point happen directly from the visual.
- **Proof.** Save screenshots of the updated Roofline or Cache state to `/tmp/asc27-verify-evidence/$RUN_ID/stage1/` and record before/after stat readouts.

## Gotchas

- `#rf-i` is stored in `log10(I)` units (`-1` to `2.2`), not linear FLOP/B. Setting `value = "2.0"` means `10^2 = 100 FLOP/B`.
- Setting `<input type="range">` programmatically via JS requires dispatching an `input` event so `oninput` handlers redraw the SVG.
- Clicking `#cache-play` starts a `110ms` interval; use `#cache-step` for deterministic step-by-step assertions or stop playback before snapshotting.
