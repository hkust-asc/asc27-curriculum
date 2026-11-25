# Stage 2: Parallelism & GPU Tiling

Stage 2 (`site/stage2-parallelism.html`) demonstrates CPU false sharing vs. 64-byte padding (`#false-sharing`), MPI 2D halo exchange and Hockney communication cost (`#mpi-halo`), and CUDA shared-memory GEMM tiling (`#cuda-tile`).

## Sub-features

- `s2-false-sharing` toggles `#fs-packed` vs. `#fs-padded`, runs 16 writes (`#fs-run`), and contrasts coherence invalidations (`#fs-inv`: `48` vs `0`) and speedup (`#fs-spd`: `0.6x` vs `3.8x`).
- `s2-mpi-halo` sweeps subdomain edge `#mpi-l` and latency `#mpi-a` and toggles `#mpi-blk` vs. `#mpi-nb` (`Isend/Irecv Overlap`), updating `#mpi-ratio`, `#mpi-share`, and `#mpi-svg`.
- `s2-cuda-tile` switches tile size presets inside `#cuda-tile`, updating HBM traffic cut (`#cu-cut`), FP32 arithmetic intensity (`#cu-int`), shared memory per block (`#cu-smem`), and `#cu-svg`.

## How to get to it (user POV)

- Click `Stage 2: Parallel` in the top nav bar.
- Click the `SIMD, MPI & GPU Tiling` stage card on `index.html`.
- Follow deep links `stage2-parallelism.html#false-sharing`, `#mpi-halo`, or `#cuda-tile`.

## Driving it with cua_repl (iab)

Preconditions:

- `serve-site.sh doctor` reports `OK:` for `http://127.0.0.1:<port>`.
- Evidence directory `/tmp/asc27-verify-evidence/$RUN_ID/stage2/` exists.

- **Open Stage 2.** Navigate to `http://127.0.0.1:<port>/stage2-parallelism.html`. `#fs-svg`, `#mpi-svg`, and `#cu-svg` all render.
- **Drive False Sharing.** Click `#fs-packed`, then `#fs-run` and wait ~3.2s for 16 ticks (or verify `#fs-inv` climbs by 3 per write toward `48`). Switch to `#fs-padded`, click `#fs-run`; `#fs-inv` stays `0` and `#fs-spd` shows `3.8x`.
- **Drive MPI Halo.** Set `#mpi-l` to `16`, `#mpi-a` to `10`, dispatch `input`; `#mpi-share` spikes and `#mpi-msg` warns that communication dominates. Click `#mpi-nb` (`Isend/Irecv Overlap`); `#mpi-share` drops.
- **Drive CUDA Tiling.** Click tile buttons in `#cuda-tile` (e.g., `8x8` vs `32x32`); `#cu-cut`, `#cu-int`, and `#cu-smem` update alongside `#cu-svg`.
- **Check pedagogy.** Confirm the visual makes the 64-byte MESI bounce, 4L vs L^2 surface-to-volume ratio, and tile reuse immediately obvious to a beginner without dense code listings.
- **Proof.** Save screenshots of before/after states to `/tmp/asc27-verify-evidence/$RUN_ID/stage2/` and log readouts.

## Gotchas

- `#fs-run` animates 16 writes at `180ms` per tick (~2.9s total). Wait for the animation to finish or click `#fs-reset` before switching modes.
