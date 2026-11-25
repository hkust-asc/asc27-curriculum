# Stage 4: ASC Sprint & Past Problems

Stage 4 (`site/stage4-asc-sprint.html`) teaches HPL grid tuning (`#hpl`), cluster Power Wall & DVFS under 3/4/5 kW caps (`#power`), and exponential qubit state-vector memory (`#qubit`). Past Problems (`site/past-problems.html`) lets learners filter C01–C10 and jump straight to the matching lab.

## Sub-features

- `s4-hpl` sweeps matrix order `#hpl-n`, block size `#hpl-nb`, and process grid `[data-pq]`, showing RAM fill, 90% swap limit, and estimated efficiency (`#hpl-eff`).
- `s4-power-dvfs` switches cap presets (`[data-cap]` 3/4/5 kW), sweeps active GPUs (`#pw-g`) and clock ratio (`#pw-f`), flipping `#pw-st` between `VALID` and `OVER CAP` on `#pw-svg`.
- `s4-qubit-wall` sweeps `#qb-n` or clicks `[data-q]` presets (`20`, `30`, `40`), verifying exact binary units (`16.0 MiB`, `16.0 GiB`, `16.0 TiB`).
- `pp-filter-and-link` filters the 10 cards in `#pp-grid` via `#pp-filters` (`All`, `GPU Allowed`, `CPU-Only`, `AI / World Model`, `Scientific PDE`), updates `#pp-detail`, and links back to the right Stage 1–4 lab.

## How to get to it (user POV)

- Click `Stage 4: ASC Sprint` or `Past Problems` in the top nav bar.
- Click the `HPL, HPCG & Power Wall` card on `index.html`.
- Follow deep links `stage4-asc-sprint.html#hpl`, `#power`, or `#qubit`.

## Driving it with cua_repl (iab)

Preconditions:

- `serve-site.sh doctor` reports `OK:` for `http://127.0.0.1:<port>`.
- Evidence directory `/tmp/asc27-verify-evidence/$RUN_ID/stage4/` exists.

- **Drive Power Wall & DVFS.** Open `stage4-asc-sprint.html#power`. Click the `3 kW` cap preset (`[data-cap="3000"]`); at default 6 GPUs / 0.85x, `#pw-st` flips to `OVER CAP` in coral. Lower `#pw-f` or `#pw-g` (dispatch `input`) until `#pw-st` returns to `VALID` and `#pw-svg` moves the dot left of the dashed cap line.
- **Drive Qubit Wall.** Click `[data-q="40"]`; `#qb-mem` displays `16.0 TiB`. Click `[data-q="20"]`; `#qb-mem` displays `16.0 MiB`.
- **Drive Past Problems.** Open `past-problems.html`. Click `[data-f="cpu"]` (`CPU-Only`); `#pp-grid` filters down to CPU-only problems. Click a card and verify `#pp-detail` updates with its math, accuracy gate, and working link to a Stage 1–4 lab.
- **Check pedagogy.** Verify Stage 4 separates historical baselines (3/4/5 kW) from ASC27 TBD rules and makes the DVFS `V^2 * f` knee visible on `#pw-svg` with minimal text.
- **Proof.** Save screenshots of the `#power` cap transition and filtered `#pp-grid` to `/tmp/asc27-verify-evidence/$RUN_ID/stage4/`.

## Gotchas

- `qb-mem` must use binary units (`MiB`, `GiB`, `TiB`), never decimal `MB`/`GB` for `16 * 2^n` bytes (per `DESIGN_SPEC.md`).
