# ASC27 24-Week Training Roadmap

Start date: **2026-11-25**. The course runs 24 weeks until **2027-05-11** at **8 to 12 hours per person per week**. The team meets every **Wednesday from 18:30 to 20:00 HKT**.

## Official ASC27 Timeline

Dates and eligibility below come from the *2027 ASC Student Supercomputer Challenge Call for Participation*.

| Item | Official ASC27 Status |
| --- | --- |
| Online Registration | 2026-11-19 to 2027-01-10 (faculty advisor receives team account and password) |
| Preliminary Round | 2027-01-11 to 2027-02-28 (English proposal graded on academic merit and technical quality) |
| Final Competition | May 2027 (exact dates and host venue TBD; cluster build, HPL, HPCG, AI/science apps, poster, defense) |
| Deadlines | Midnight at the end of the stated date, **UTC+8** (Hong Kong time) |
| Team Roster | 5 undergraduate students (under 4 academic years) + 1 faculty advisor; locked at prelim submission |
| Advancement Limit | Multiple prelim teams per university allowed; max 1 finalist team per university |
| Power Cap, Hardware & Weights | **TBD by ASC27 Committee** |

Stage 4 uses three historical power caps as practice targets:
- **3 kW**: ASC22 finals limit.
- **4 kW**: ASC25 finals CPU-only limit.
- **5 kW**: ASC26 finals limit ($\le 2\ \mathrm{kW}$ per node, $\ge 3$ nodes).

**2027-05-11** is our internal full-rehearsal cutoff. When the committee posts exact May dates, Stage 4 adjusts its final sprint weeks.

## Four-Stage Roadmap

| Stage and Duration | Core Goal | Tech Stack | Verifiable Milestones | ASC Scoring Links |
| --- | --- | --- | --- | --- |
| **Stage 1: Foundations**<br>3 weeks (2026-11-25 to 12-15)<br>M01 to M04 | Measure arithmetic work, memory traffic, scaling limits, and Roofline bounds before editing code. | C11, Python, NumPy, `clock_gettime`, `perf stat`, STREAM, `numactl` | $2n^3$ GEMM timing and FP32/FP64 error table; LLC-miss and NUMA latency diff; Amdahl/Gustafson plots and one-page Roofline chart | Backs up cluster choices in the preliminary proposal and sets up HPL/HPCG analysis |
| **Stage 2: Parallelism and GPUs**<br>5 weeks (2026-12-16 to 01-19)<br>M05 to M08 | Write fast CPU SIMD/OpenMP, MPI halo exchange, and CUDA/HIP GEMM code, and read profiler traces. | OpenMP, AVX2/AVX-512, `numactl`, MPI, CUDA/HIP, cuBLAS, `nsys`, `ncu`, Score-P, Slurm | 4-variant CPU speedup table with false-sharing fix; 2D MPI halo solver on $\ge 4$ ranks; tiled CUDA GEMM vs. cuBLAS; annotated `nsys` and Score-P timeline | Builds skills for prelim app prototypes, HPL grids, HPCG halos, and GPU kernels |
| **Stage 3: AI Systems and Porting**<br>5 weeks (2027-01-20 to 02-23)<br>M09 to M12 | Model GPU VRAM and Ring All-Reduce cost, split prefill/decode latency, and run 200-step porting checks. | PyTorch, `torch.amp`, DDP, FSDP, NCCL/RCCL, KV cache profiling, CUDA streams | Byte-exact VRAM table verified with an intentional OOM; Ring All-Reduce timing vs. $2(p-1)G/p$; prefill/decode and KV cache log; 200-step stencil regression | Runs in parallel with the 01-11 to 02-28 preliminary window for AI and scientific chapters |
| **Stage 4: ASC Sprint**<br>11 weeks (2027-02-24 to 05-11)<br>M13 to M16 | Tune HPL and HPCG under 3/4/5 kW practice caps, run mystery-app drills, and rehearse the English defense. | Netlib HPL, HPCG 3.0+, RAPL/IPMI/DVFS power logs, Slurm `sbatch`, git evidence bundles | Passing HPL runs across $N$, $NB$, $P \times Q$; 1800 s HPCG run without Quick Path; live power-vs-speed sweep; mystery-app bundle and timed 10-min defense | Covers all ASC27 finals categories: cluster build, HPL, HPCG, apps, poster, and Q&A |

Stage 2 ends on 2027-01-19, eight days after the preliminary round opens (2027-01-11). In Weeks 7 and 8, the team confirms registration and drafts the cluster design while applying Stage 2–3 tools directly to the preliminary tasks.

## Weekly Sprint Plan

Each week includes one Wednesday lab demo (18:30 to 20:00 HKT) and one checked-in repository artifact.

### Stage 1: Foundations (Weeks 1 to 3)

| Week | Dates | Module and Focus | Weekly Deliverable |
| --- | --- | --- | --- |
| W01 | 2026-11-25 to 12-01 | M01: GEMM work, timers, floating-point precision | `results/w01-gemm.md`: $2n^3$ count, wall time, GFLOP/s, and FP32 vs. FP64 error for $n \in \{512, 1024, 2048\}$ |
| W02 | 2026-12-02 to 12-08 | M02: Cache locality, memory wall, NUMA | `perf stat` LLC-miss log and local vs. remote `numactl` timing on a 2D stencil larger than LLC |
| W03 | 2026-12-09 to 12-15 | M03 + M04: Amdahl/Gustafson and Roofline | Scaling plot (measured vs. model) and Roofline chart placing GEMM and stencil against STREAM $B$ |

### Stage 2: Parallelism and GPUs (Weeks 4 to 8)

| Week | Dates | Module and Focus | Weekly Deliverable |
| --- | --- | --- | --- |
| W04 | 2026-12-16 to 12-22 | M05 (Part 1): Vectorization and SIMD intrinsics | 4-column timing table (scalar, `-O3`, `omp simd`, AVX2/AVX-512) checked against FP64 reference |
| W05 | 2026-12-23 to 12-29 | M05 (Part 2): OpenMP binding and false sharing | Thread sweep comparing `OMP_PROC_BIND=close` vs. `spread`, plus before/after false-sharing padding |
| W06 | 2026-12-30 to 01-05 | M06 (Part 1): MPI domain split and halo exchange | Non-blocking 2D halo solver on $\ge 4$ ranks verified against serial output |
| W07 | 2027-01-06 to 01-12 | M06 (Part 2): Collectives, Hockney sweep, **01-10 reg check** | `MPI_Allreduce` latency/bandwidth plot; confirm advisor received ASC27 account email |
| W08 | 2027-01-13 to 01-19 | M07 + M08: Tiled CUDA/HIP GEMM, Slurm, `nsys`/Score-P | Tiled GPU GEMM % of cuBLAS/rocBLAS; annotated `nsys` timeline marking two idle gaps |

### Stage 3: AI Systems and Porting (Weeks 9 to 13)

| Week | Dates | Module and Focus | Weekly Deliverable |
| --- | --- | --- | --- |
| W09 | 2027-01-20 to 01-26 | M09: Transformer VRAM budget and mixed precision | FP32 vs. BF16 byte table verified by triggering one deliberate OOM |
| W10 | 2027-01-27 to 02-02 | M10 (Part 1): DDP and Ring All-Reduce traffic | Multi-GPU DDP run comparing measured collective time to $2(p-1)G/p$ |
| W11 | 2027-02-03 to 02-09 | M10 (Part 2): FSDP, TP, and PP trade-offs | Memory and step-time table across DDP, FSDP, and a 2-GPU TP equivalence test |
| W12 | 2027-02-10 to 02-16 | M11: Prefill/decode split, KV cache, denoising | Prefill and per-token decode latencies matched to $M_{\mathrm{KV}}$; denoising step timing vs. error |
| W13 | 2027-02-17 to 02-23 | M12: Scientific porting and 200-step regression | Phase breakdown, resident-buffer fix, and 200-step RMS diff; freeze prelim charts before **02-28** |

### Stage 4: ASC Sprint (Weeks 14 to 24)

| Week | Dates | Module and Focus | Weekly Deliverable |
| --- | --- | --- | --- |
| W14 | 2027-02-24 to 03-02 | M13 (Part 1): Single-node HPL (`N`, `NB`, BLAS) | Passing `xhpl` log with manual $\frac{2}{3}N^3 / T_{\mathrm{wall}}$ check |
| W15 | 2027-03-03 to 03-09 | M13 (Part 2): Multi-node HPL $P \times Q$ grids | Two $P \times Q$ grid runs diagnosing panel broadcast vs. trailing GEMM |
| W16 | 2027-03-10 to 03-16 | M14 (Part 1): HPCG build and 1800 s run | Valid HPCG output with Quick Path disabled in overnight `sbatch` |
| W17 | 2027-03-17 to 03-23 | M14 (Part 2): SpMV/SymGS Roofline audit | Arithmetic intensity math and `perf stat` memory-stall breakdown |
| W18 | 2027-03-24 to 03-30 | M15 (Part 1): Power telemetry and 3 kW practice cap | Live power-vs-$R_{\max}$ curve tagged as ASC22 3 kW practice target |
| W19 | 2027-03-31 to 04-06 | M15 (Part 2): 4 kW / 5 kW caps and DVFS sweeps | Frequency/power-cap sweep recording wall time and FLOP/J |
| W20 | 2027-04-07 to 04-13 | M16 (Part 1): Mystery-app drill I (first 90 min) | Build notes, hotspot profile, accuracy gate, and locked baseline run |
| W21 | 2027-04-14 to 04-20 | M16 (Part 2): Mystery-app drill II (optimize + rollback) | Verified before/after timing, accuracy diff, and rollback script |
| W22 | 2027-04-21 to 04-27 | M16 (Part 3): Evidence bundle and peer replay | Clean `evidence/` folder re-run by a second teammate |
| W23 | 2027-04-28 to 05-04 | M16 (Part 4): English poster and Q&A rehearsal | Draft A0 poster, 10-min two-speaker script, and 8 Q&A cards |
| W24 | 2027-05-05 to 05-11 | 48-hour mock finals dress rehearsal | End-to-end run: cluster check, HPL, HPCG, one app, and poster defense |

## Wednesday Session Format (18:30 to 20:00 HKT)

1. **18:30 to 18:45 (Debug Review)**: One teammate shows a slow or broken run from last week with exact flags and counters.
2. **18:45 to 19:35 (Live Lab)**: Instructor runs one live compile, profile, or debug experiment via `srun`, `perf`, `nsys`, or `ncu`.
3. **19:35 to 20:00 (Next Milestone)**: Team records next week's test command and numerical tolerance.

## Lab Pass Criteria

Each weekly submission passes when all five checks hold:

| Check | Pass | Fail |
| --- | --- | --- |
| Exact Command | Full compile and run flags sit at the top of the log | Screenshot only or vague notes |
| Clear Units | Every time, GFLOP/s, error, and watt value includes its formula and unit | Unanchored claims ("much faster") |
| Accuracy Check | Output passes the pre-registered reference or residual test | Program exits 0 with no math check |
| Control Variable | At least one parameter swept (size, threads, pinning, precision, or watts) | One cherry-picked number |
| Source Tag | Tags lab hardware or historical baseline year clearly | Mixes past power caps with ASC27 rules |
