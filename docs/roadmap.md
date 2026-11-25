# ASC27 24-Week Training Roadmap

Reference date: **2026-11-25**. The curriculum runs 24 weeks from **2026-11-25 to 2027-05-11** at **8 to 12 hours per person per week**, anchored on HKUST ASC weekly training sessions every **Wednesday 18:30 to 20:00 HKT**. Remaining weekly hours go to reproducible lab runs, written logs, and peer code reviews.

## Verified ASC27 Timeline & Rule Boundaries

All entries below come directly from the official *2027 ASC Student Supercomputer Challenge Call for Participation*. Items absent from that notice remain explicitly marked TBD; historical numbers never substitute for missing ASC27 rules.

| Item | Verified Official Status |
| --- | --- |
| Online Registration | 2026-11-19 to 2027-01-10; faculty advisor receives entry confirmation, team account number, and password |
| Preliminary Competition | 2027-01-11 to 2027-02-28; comprehensive proposal reviewed solely on academic merit and technical excellence (creativity, teamwork, innovation) |
| Final Competition | May 2027 (exact dates and host venue TBD); on-site custom cluster building, HPL and HPCG benchmarks, AI and scientific application optimization, poster and oral presentation |
| Submission Deadlines | Midnight at the end of the stated date, **UTC+8** (same local time as Hong Kong) |
| Team Composition | 5 undergraduate students + 1 faculty advisor; roster finalized at preliminary proposal submission; undergraduates must have completed fewer than 4 academic years of full-time study when finalists are confirmed |
| Advancement Quota | Multiple teams per university allowed in preliminary round; maximum 1 finalist team per university |
| Power Cap, Hardware BOM & Scoring Formula | **TBD by ASC27 Committee**; do not cite 3 kW, 4 kW, or 5 kW as ASC27 rules |

Historical finals power ceilings serve solely as Stage 4 stress-test baselines and must carry their year label in all logs:
- **3 kW baseline**: ASC22 on-site finals (official *ASC22 Final Competition Notification*; exceeding 3 kW invalidated the running task).
- **4 kW baseline**: ASC25 finals CPU-only tasks (AlphaFold3, DeepSeek R1-Distill 32B; historical reference baseline).
- **5 kW baseline**: ASC26 finals cluster limit with $\le 2\ \mathrm{kW}$ per node and $\ge 3$ nodes (*ASC26 Optimization & Innovation Introduction* talk).

Because exact May 2027 finals dates are still TBD, **2027-05-11** serves as the internal course completion and full-rehearsal cutoff rather than an announced competition date. Once the ASC27 Committee releases exact dates, Stage 4 adjusts its final sprint weeks without changing M01 to M12 ordering.

## 4-Stage Roadmap Overview

| Stage & Duration | Core Objective | Key Tech Stack | Verifiable Hands-on Milestones | ASC Competition Scoring Links |
| --- | --- | --- | --- | --- |
| **Stage 1: Foundations**<br>3 weeks (2026-11-25 to 2026-12-15)<br>Modules M01 to M04 | Measure arithmetic work, memory traffic, scaling ceilings, and Roofline placement before editing code. | C11, Python, NumPy, `clock_gettime`, `perf stat`, STREAM, `numactl`, Roofline analysis | Verified $2n^3$ GEMM timing and FP32/FP64 relative error table across three sizes; cache-miss and cross-NUMA latency diff; Amdahl/Gustafson plots and one-page Roofline bottleneck diagnosis | Justifies cluster architecture choices in the English preliminary proposal and establishes quantitative HPL/HPCG interpretation (exact ASC27 point weights TBD) |
| **Stage 2: Parallelism & Acceleration**<br>5 weeks (2026-12-16 to 2027-01-19)<br>Modules M05 to M08 | Deliver verified speedups across CPU SIMD/OpenMP, MPI halo exchange, CUDA/HIP GEMM, and Slurm profiling. | OpenMP, AVX2/AVX-512 intrinsics, `numactl`, MPI (`Isend`/`Irecv`, `Allreduce`), CUDA/HIP, cuBLAS, Nsight Systems, Nsight Compute, Score-P, Slurm `srun` | 4-variant CPU speedup table with pinning and false-sharing fix; 2D MPI halo exchange verified against serial reference on $\ge 4$ ranks; tiled CUDA GEMM achieving target fraction of cuBLAS with `ncu` metrics; annotated `nsys` and Score-P timeline explaining idle gaps | Feeds directly into preliminary cluster and application prototypes, HPL process grids, HPCG/scientific halo scaling, and GPU kernel engineering |
| **Stage 3: AI Systems & Performance Tuning**<br>5 weeks (2027-01-20 to 2027-02-23)<br>Modules M09 to M12 | Model GPU VRAM and Ring All-Reduce budgets, split prefill/decode inference cost, and run long-step scientific porting regressions. | PyTorch, `torch.amp` (FP16/BF16/FP8 concepts), DDP, FSDP, NCCL/RCCL, KV cache profiling, CUDA streams, multi-hundred-step RMS regression | Exact parameter/gradient/optimizer/activation byte budget verified against intentional OOM; Ring All-Reduce time matched against $2(p-1)G/p$; split prefill vs. decode and KV cache memory measurement; ported stencil or mini-app passing $\ge 200$-step reference regression with bottleneck-shift breakdown | Aligns directly with the 2027-01-11 to 2027-02-28 preliminary window for LLM, world-model, and scientific optimization chapters plus mandatory convergence/accuracy logs |
| **Stage 4: ASC Competition Sprint**<br>11 weeks (2027-02-24 to 2027-05-11)<br>Modules M13 to M16 | Tune HPL and HPCG under historical 3/4/5 kW stress-test baselines, execute 48-hour mystery-app sprints, and polish the English defense. | Netlib HPL, HPCG 3.0+, RAPL/IPMI/DVFS power logging, Slurm `sbatch`, English proposal & poster templates, git evidence packaging | Validated HPL runs across $N$, $NB$, $P\times Q$ grids; sustained HPCG run following the historical 1800 s no-Quick-Path discipline; measured power-vs-performance sweep labeled with historical 3/4/5 kW baselines; complete mystery-app evidence bundle and timed 10-minute English presentation + Q&A rehearsal | Targets all confirmed ASC27 finals categories: on-site cluster build, HPL, HPCG, AI and scientific applications, poster, and committee presentation |

Stage 2 closes on 2027-01-19, eight days after preliminary competition launch (2027-01-11). During Week 7 and Week 8, teams lock registration status and draft the baseline cluster design while immediately applying MPI, GPU, and profiling skills to the released preliminary tasks throughout Stage 3 until the 2027-02-28 midnight UTC+8 deadline.

## Weekly Sprint Guide

Each week commits to one Wednesday classroom demo (18:30 to 20:00 HKT) and one verifiable repository artifact.

### Stage 1: Foundations (Weeks 1 to 3)

| Week | Dates | Module & Focus | Weekly Verifiable Deliverable |
| --- | --- | --- | --- |
| W01 | 2026-11-25 to 12-01 | M01: GEMM workload, timers, floating-point precision | `results/w01-gemm.md`: $2n^3$ count, monotonic wall time, GFLOP/s, and FP32 vs. FP64 relative error for $n \in \{512, 1024, 2048\}$ |
| W02 | 2026-12-02 to 12-08 | M02: Cache locality, memory wall, NUMA placement | `perf stat` LLC-miss report plus local vs. remote `numactl` timing comparison on a 2D stencil larger than LLC |
| W03 | 2026-12-09 to 12-15 | M03 + M04: Amdahl/Gustafson scaling and Roofline diagnosis | One-page scaling plot (measured vs. predicted) plus Roofline chart placing M01 GEMM and M02 stencil against measured machine $P_{\mathrm{peak}}$ and STREAM $B$ |

### Stage 2: Parallelism & Acceleration (Weeks 4 to 8)

| Week | Dates | Module & Focus | Weekly Verifiable Deliverable |
| --- | --- | --- | --- |
| W04 | 2026-12-16 to 12-22 | M05 (Part 1): Compiler vectorization and SIMD intrinsics | 4-column timing and retired-FP report (scalar, `-O3`, `omp simd`, AVX2/AVX-512 intrinsic) verified against FP64 reference |
| W05 | 2026-12-23 to 12-29 | M05 (Part 2): OpenMP scheduling, core binding, false sharing | Thread sweep (1 to physical cores) comparing `OMP_PROC_BIND=close` vs. `spread`, plus a false-sharing counterexample before/after padding |
| W06 | 2026-12-30 to 01-05 | M06 (Part 1): MPI domain decomposition and halo exchange | Non-blocking 2D halo solver on $\ge 4$ ranks verified within L2 tolerance against serial output |
| W07 | 2027-01-06 to 01-12 | M06 (Part 2): Collectives, Hockney sweep, **ASC27 reg check (01-10 deadline)** | OSU or custom `MPI_Allreduce` latency/bandwidth plot separating $\alpha$-bound and $B$-bound regimes; confirm faculty advisor received ASC27 account email |
| W08 | 2027-01-13 to 01-19 | M07 + M08: Tiled CUDA/HIP GEMM, Slurm binding, `nsys`/Score-P timelines | Tiled GPU GEMM speedup vs. naive kernel and fraction of cuBLAS/rocBLAS; annotated `nsys` timeline identifying at least two idle gaps |

### Stage 3: AI Systems & Performance Tuning (Weeks 9 to 13)

| Week | Dates | Module & Focus | Weekly Verifiable Deliverable |
| --- | --- | --- | --- |
| W09 | 2027-01-20 to 01-26 | M09: Transformer VRAM budget and mixed precision (FP16/BF16/FP8) | Static + activation byte table comparing FP32 vs. BF16, validated by triggering one deliberate OOM and explaining which component overflowed |
| W10 | 2027-01-27 to 02-02 | M10 (Part 1): DDP and Ring All-Reduce traffic verification | Multi-GPU DDP run comparing observed collective time against $2(p-1)G/p$ over measured interconnect bandwidth |
| W11 | 2027-02-03 to 02-09 | M10 (Part 2): FSDP, TP, and PP partitioning trade-offs | Single-model memory and step-time comparison across DDP, FSDP, and a minimal TP/PP forward-equivalence check on lab hardware |
| W12 | 2027-02-10 to 02-16 | M11: LLM prefill/decode split, KV cache, diffusion denoising | Separate prefill latency and per-token decode latency log matched against $M_{\mathrm{KV}}$ growth, plus multi-step denoising timing vs. accuracy check |
| W13 | 2027-02-17 to 02-23 | M12: Scientific GPU porting, bottleneck shifts, long-run regression | Profile breakdown, resident-buffer fix, and $\ge 200$-step reference diff; freeze all preliminary proposal figures ahead of **2027-02-28 24:00 UTC+8** submission |

### Stage 4: ASC Competition Sprint (Weeks 14 to 24)

| Week | Dates | Module & Focus | Weekly Verifiable Deliverable |
| --- | --- | --- | --- |
| W14 | 2027-02-24 to 03-02 | M13 (Part 1): Single-node HPL (`N`, `NB`, BLAS threading) | Passing `xhpl` output with residual verification and manual check of $\frac{2}{3}N^3 / T_{\mathrm{wall}}$ against reported $R_{\max}$ |
| W15 | 2027-03-03 to 03-09 | M13 (Part 2): Multi-node HPL process grid ($P \times Q$) and interconnect | At least two $P \times Q$ grid comparisons diagnosing panel broadcast vs. trailing GEMM bottlenecks |
| W16 | 2027-03-10 to 03-16 | M14 (Part 1): HPCG build and sustained-runtime discipline | Verified HPCG output file with Quick Path disabled, targeting the historical 1800-second sustained window in overnight `sbatch` |
| W17 | 2027-03-17 to 03-23 | M14 (Part 2): SpMV/SymGS Roofline audit and halo alignment | Arithmetic intensity calculation and `perf stat` memory-stall breakdown confirming HPCG sits on the bandwidth slope |
| W18 | 2027-03-24 to 03-30 | M15 (Part 1): Power telemetry and 3 kW historical stress test | Power-vs-$R_{\max}$ curve measured during live runs (labeled "ASC22 3 kW baseline, non-binding for ASC27") |
| W19 | 2027-03-31 to 04-06 | M15 (Part 2): 4 kW / 5 kW baselines, DVFS, node-count trade-offs | Controlled frequency/power-cap sweep recording wall time and energy efficiency (FLOP/J) without extrapolating beyond physical hardware wattage |
| W20 | 2027-04-07 to 04-13 | M16 (Part 1): Mystery-app drill I (first 90 minutes) | Build notes, I/O inventory, hotspot profile, accuracy gate, and locked baseline run command for an unseen solver |
| W21 | 2027-04-14 to 04-20 | M16 (Part 2): Mystery-app drill II (targeted optimization + rollback) | Verified before/after timing, numerical diff against reference, and single-command rollback script |
| W22 | 2027-04-21 to 04-27 | M16 (Part 3): Reproducible evidence bundle and cross-team workflow | Standardized `evidence/` directory that a second teammate can re-execute from a clean checkout to reproduce runtime and accuracy |
| W23 | 2027-04-28 to 05-04 | M16 (Part 4): English poster and timed defense rehearsal | Draft A0/landscape technical poster, 10-minute two-speaker English script, and 8+ technical Q&A cards covering mathematical equivalence |
| W24 | 2027-05-05 to 05-11 | Full dress rehearsal (compressed 48-hour mock finals) | End-to-end simulation: cluster sanity check, HPL, HPCG, one application optimization, and poster defense (cutoff 2027-05-11; adjust if official May finals schedule falls earlier) |

## Wednesday Evening Session Cadence (18:30 to 20:00 HKT)

Every 90-minute session follows a strict three-block rhythm so lecture time never crowds out measurement:
1. **18:30 to 18:45 (Failure Post-Mortem)**: One teammate walks through a broken or slow run from the previous week showing exact CLI flags, counter output, and reference diff.
2. **18:45 to 19:35 (Live Lab Walkthrough)**: Instructor compiles, profiles, or debugs one concrete experiment live via `srun`, `perf`, `nsys`, or `ncu`. Mathematical derivations are assigned as pre-reading.
3. **19:35 to 20:00 (Milestone Contract)**: Team writes down next week's acceptance command and numerical tolerance. Once logged, tolerances cannot be loosened mid-week.

Absent members submit the same weekly artifact to the team repository before the next Wednesday session.

## Lab Verification Rubric

Every weekly artifact is checked against five binary criteria. A milestone passes only when all five hold.

| Criterion | Pass | Fail |
| --- | --- | --- |
| Reproducible Command | Exact compile and run commands (including thread count, binding flags, GPU IDs, and dataset paths) sit at the top of the report | Screenshot-only report or vague prose such as "ran with `srun`" |
| Defined Metrics | Every wall time, GFLOP/s, relative error, and watt reading states its numerator, denominator, and unit | Unanchored claims ("much faster") or speedups without a recorded baseline |
| Correctness Gate | Output matches a pre-registered reference solution, residual threshold, or official validation tool | Program exits 0 without numerical verification |
| Controlled Baseline | At least one isolated control variable (problem size, thread count, pinning mode, precision, or power cap) | Single cherry-picked "best" number with no ablation |
| Source & Rule Scope | Explicitly tags whether hardware/power settings belong to the HKUST lab or a historical ASC baseline | Presents 3 kW, 4 kW, 5 kW, or a past GPU BOM as an official ASC27 regulation |

During Stage 4, an additional gate applies to every optimization PR: **mathematical equivalence**. Any change that alters the underlying mathematical algorithm must be flagged as experimental and kept out of competition submission scripts unless permitted by an explicit competition rule (such as unlocked samplers in ASC26 UnifoLM finals).
