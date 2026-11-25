#!/usr/bin/env python3
"""
Build all 6 modular LibreOffice Impress (.odp) training slide decks for HKUST ASC27 (English Edition),
then convert each deck via LibreOffice headless to PDF and PPTX.

Decks:
  00-overview-roadmap    (Overview, Knowledge Graph, 24-Week Roadmap & Source Mapping)
  01-stage1-foundations  (Stage 1 Foundations: M01-M04)
  02-stage2-parallelism  (Stage 2 Parallelism & Acceleration: M05-M08)
  03-stage3-ai-systems   (Stage 3 AI Systems & Performance Tuning: M09-M12)
  04-stage4-asc-sprint   (Stage 4 ASC Competition Sprint: M13-M16)
  05-past-asc-problems   (Verified Past ASC Competition Problems: C01-C10)
"""

from __future__ import annotations

import sys
from pathlib import Path

from odp_builder import ODPDeck, PALETTE, SlideSpec, convert_odp_with_libreoffice

ROOT = Path(__file__).resolve().parent.parent
PNG_DIR = ROOT / "diagrams" / "png"
ODP_DIR = ROOT / "slides" / "odp"
PPTX_DIR = ROOT / "slides" / "pptx"
PDF_DIR = ROOT / "slides" / "pdf"


def img(name: str) -> str:
    return str(PNG_DIR / name)


def build_deck_00() -> ODPDeck:
    d = ODPDeck(
        title="ASC27 First-Principles Curriculum Overview & Roadmap",
        deck_code="00",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="HKUST ASC TEAM · ASC27 FIRST-PRINCIPLES CURRICULUM",
            title="High-Performance Computing &\nAI Systems Training Curriculum",
            subtitle="First-principles path from physical limits, memory walls, and Roofline bounds to ASC27 competition readiness",
            footnote="HKUST ASC Team  ·  24-Week Schedule (2026-11-25 to 2027-05-11)  ·  LibreOffice Impress Native Edition",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="table",
            section_tag="00 · OVERVIEW · RULES & SOURCES",
            title="ASC27 Official Milestones and Reference Boundaries",
            subtitle="Separating confirmed ASC27 rules from historical power-cap baselines and team case studies",
            table_headers=["Source Document", "Classification", "Key Constraints & Knowledge Graph Mapping"],
            table_col_widths_cm=[7.4, 5.6, 17.85],
            table_rows=[
                [
                    "ASC27 Call for Participation",
                    "Official ASC27 Rules",
                    "Registration Nov 19, 2026 to Jan 10, 2027; Prelim Jan 11 to Feb 28, 2027; Finals May 2027; 5 undergrads + 1 advisor; max 1 finalist/university; deadlines midnight UTC+8 (Maps to E1, E3)",
                ],
                [
                    "ASC22 Prelim & Final Notifications",
                    "Historical Baseline (3 kW)",
                    "HPL, HPCG, Yuan 4.7B LLM (1B tokens, loss < 7.0), and DeePMD-kit under 3 kW on-site power cap and relative scoring formulas (Maps to D1, D2, E1, E2)",
                ],
                [
                    "ASC26 Optimization Intro (Committee)",
                    "Historical Summary (5 kW)",
                    "5 kW cluster cap, <= 2 kW/node, >= 3 nodes; 6 tasks: HPL/HPCG, UnifoLM-WMA-0, AMSS-NCKU, QiboTN, LeWM mystery app, ICON group task (Maps to A3, D3, E1, E2, E3)",
                ],
                [
                    "ASC26 AMSS-NCKU Talk (Tsinghua)",
                    "Team Engineering Case Study",
                    "CPU 4.5s -> GPU v1 4.7s (122 transfers) -> GPU-resident 1.4s -> 2+62 core split 1.0s -> 3-stage relay 0.85s; bottleneck shift & 200-step regression (Maps to A2, B3, C2, C3, E2)",
                ],
                [
                    "Kwan Wing-keung Roadshow & Map of HPC",
                    "Macro Landscape",
                    "Five physical and software walls (Memory, Power, Communication, Programmability, Fault Tolerance) across full HPC+AI stack (Maps to L1 to L5)",
                ],
            ],
            callout="Rule boundary: ASC27 final power cap, approved hardware list, and scoring weights are not yet announced. 3 kW, 4 kW, and 5 kW serve strictly as historical stress-test presets.",
            footnote="Compiled from official ASC27 Call for Participation, ASC22 notices, ASC26 committee slides, and Tsinghua team talk",
            speaker_notes=(
                "Speaker guidance:\n"
                "1. Establish epistemic discipline on slide 2: never confuse past-year rules or team talks with binding ASC27 regulations.\n"
                "2. All ASC27 submission deadlines fall at midnight (24:00) UTC+8, matching Hong Kong local time (HKT).\n"
                "3. Connect the five walls in the Map of HPC directly to the five layers of our curriculum."
            ),
        )
    )
    d.add_slide(
        SlideSpec(
            kind="full_visual",
            section_tag="00 · KNOWLEDGE GRAPH",
            title="Five-Layer First-Principles Knowledge Graph (L1 to L5)",
            subtitle="Every layer resolves a concrete physical or algorithmic bottleneck, joined by four cross-layer contest bridges",
            image_path=img("00_knowledge_graph.png"),
            callout="Four cross-layer bridges: A3 Power/Thermal -> E1 Power-Capped Benchmarks; B2 RDMA Topology -> D2 Distributed Training; C2 Roofline Profiling -> E2 Scientific/Mystery Apps; C3 Regression -> E3 Proposal & Q&A.",
            footnote="Repository sources: docs/knowledge-graph.md and diagrams/knowledge-graph.mmd",
            speaker_notes=(
                "Dependency narrative:\n"
                "- L1 sets hard physical ceilings on compute, memory movement, and heat dissipation.\n"
                "- L2 introduces parallel execution models to overcome single-core frequency stagnation and single-node memory caps.\n"
                "- L3 provides mathematical bounds (Amdahl, Gustafson, Roofline) and empirical profiling to expose real bottlenecks.\n"
                "- L4 maps those hardware fundamentals onto modern AI training, distributed collectives, and inference serving.\n"
                "- L5 integrates full-stack engineering under strict power caps, numerical correctness gates, and English oral defense."
            ),
        )
    )
    d.add_slide(
        SlideSpec(
            kind="full_visual",
            section_tag="00 · ROADMAP TIMELINE",
            title="24-Week Training Gantt Chart (2026-11-25 to 2027-05-11)",
            subtitle="Aligned with HKUST ASC Wednesday evening sessions (8 to 12 hours/week/member) and official ASC27 windows",
            image_path=img("00_roadmap_timeline.png"),
            callout="Key schedule anchors: register and lock roster by 2027-01-10; run Stage 3 in parallel with the Preliminary Round (01-11 to 02-28); dedicate March to May to power-capped sprints and mystery drills.",
            footnote="Schedule baseline: 2026-11-25 (HKT); exact May 2027 finals dates follow official committee release",
            speaker_notes=(
                "Pacing rationale:\n"
                "- Stage 1 (3 weeks) builds measurement hygiene and roofline intuition before touching complex parallel frameworks.\n"
                "- Stage 2 (5 weeks) completes the OpenMP, MPI, CUDA, and Slurm toolkit right as Preliminary Round opens.\n"
                "- Stage 3 (5 weeks) overlaps directly with the Preliminary Round so AI and GPU porting labs feed straight into the proposal.\n"
                "- Stage 4 (11 weeks) sharpens HPL/HPCG, 3/4/5 kW power capping, 48-hour mystery simulations, and English defense."
            ),
        )
    )
    d.add_slide(
        SlideSpec(
            kind="table",
            section_tag="00 · FOUR-STAGE ROADMAP",
            title="Four-Stage Curriculum Roadmap Overview",
            subtitle="Each stage closes with quantifiable hands-on milestones tied directly to ASC scoring items",
            table_headers=[
                "Stage & Duration",
                "Core Objective",
                "Key Tech Stack",
                "Verifiable Hands-on Milestones",
                "ASC Scoring Links",
            ],
            table_col_widths_cm=[4.3, 5.2, 5.8, 9.15, 6.4],
            table_rows=[
                [
                    "Stage 1 Foundations\n3 wks (11/25 - 12/15)\nM01 to M04",
                    "Quantify work, memory traffic, Amdahl bounds, and Roofline ceilings",
                    "Linux, C/C++, Git, perf, likwid, STREAM, numactl",
                    "Measure DDR5 bandwidth & FP64 peak; plot empirical Roofline; speed up single-core GEMM >= 8x via tiling",
                    "Proposal performance modeling, hotspot triage, avoiding blind tuning",
                ],
                [
                    "Stage 2 Parallelism\n5 wks (12/16 - 01/19)\nM05 to M08",
                    "Master CPU SIMD/OpenMP, multi-node MPI overlap, and CUDA SIMT",
                    "OpenMP, AVX2/512, MPI, CUDA/HIP, Slurm, nsys/ncu, Score-P",
                    "Hand-written CUDA GEMM >= 75% cuBLAS; 3D Stencil MPI weak scaling >= 85%; pinned timeline report",
                    "CPU-only tasks, multi-node scientific scaling, custom GPU kernels",
                ],
                [
                    "Stage 3 AI Systems\n5 wks (01/20 - 02/23)\nM09 to M12",
                    "Solve LLM memory/comms walls, inference latency, and GPU porting",
                    "PyTorch, BF16/FP8, FSDP/Megatron, NCCL/RCCL, TensorRT, CUDA Graph",
                    "Predict 7B memory within 5%; multi-GPU scaling >= 85%; port Stencil to GPU passing 200-step regression",
                    "LLM & World Model tasks (Prelim 30 pts / e-Prize), GPU science porting",
                ],
                [
                    "Stage 4 ASC Sprint\n11 wks (02/24 - 05/11)\nM13 to M16",
                    "Deliver peak HPL/HPCG, power-capped clusters, mystery apps, and Q&A",
                    "HPL, HPCG, MKL/OpenBLAS, nvidia-smi/rocm-smi, IPMI power telemetry",
                    "Tune HPL/HPCG under 3/4/5 kW presets; pass 48h blind mystery drill; complete English poster mock Q&A",
                    "HPL/HPCG benchmarks, cluster power design, mystery & group apps, 10-pt defense",
                ],
            ],
            footnote="Detailed weekly sprints and lab acceptance criteria appear in docs/roadmap.md",
            speaker_notes=(
                "Execution management:\n"
                "1. Hold a 30-minute stage gate review at the end of each stage where every member merges reproducible scripts and plots via Git PR.\n"
                "2. Reject bare wall-time claims: every report must include hardware efficiency (% of peak or % of STREAM), error metrics, and environment metadata."
            ),
        )
    )
    d.add_slide(
        SlideSpec(
            kind="two_col",
            section_tag="00 · FIRST-PRINCIPLES METHOD",
            title="Five-Step Performance Loop and Five-Member Team Roles",
            subtitle="Every optimization must follow empirical measurement and automated long-run verification",
            left_title="Five-Step Performance Engineering Loop",
            left_bullets=[
                "Baseline first: fix random seeds and inputs, archive an unmodified reference output and wall clock.",
                "Bound the problem: compute theoretical FLOPs and minimum bytes to locate the Roofline ceiling.",
                "Profile end to end: split runtime into compute, transfer, synchronization, and I/O via perf/nsys/Score-P.",
                "Change one bottleneck: isolate each code change and record both speedup and hardware utilization.",
                "Run long regression: verify full-step numerical error, invariants, and power cap before merging.",
            ],
            right_title="Recommended 5-Student ASC Role Matrix",
            right_bullets=[
                "Cluster & Systems Lead: OS tuning, GPU/IB drivers, RDMA topology, Slurm, HPL, and power control.",
                "CPU & Comms Lead: SIMD vectorization, OpenMP, NUMA pinning, HPCG, and CPU-only applications.",
                "GPU & Science Lead: CUDA/HIP porting, device residency, async pipelines, and numerical regression.",
                "AI Systems Lead: mixed precision, distributed training, KV cache, TensorRT, and world models.",
                "Shared ownership: English Proposal writing, ablation evidence, poster design, and mock Q&A.",
            ],
            callout="Non-negotiable contest rules: failing correctness scores 0; exceeding the power cap disqualifies the run; all speedups must stay reproducible and rule-compliant.",
            footnote="Continue sequentially through Decks 01 to 04 and the 10 verified past problems in Deck 05",
            speaker_notes=(
                "Coaching note:\n"
                "1. Roles prevent duplication during crunch time, but everyone completes Stage 1 and Stage 2 together to avoid single-point-of-failure knowledge silos.\n"
                "2. Before using coding agents on tedious porting tasks, lock down a fast reference comparator and stage-by-stage timer."
            ),
        )
    )
    return d


def build_deck_01() -> ODPDeck:
    d = ODPDeck(
        title="Stage 1 Foundations: Physical Limits & Performance Models (M01-M04)",
        deck_code="S1",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="STAGE 1 · WEEKS 1 TO 3 (2026-11-25 TO 2026-12-15) · M01 TO M04",
            title="Stage 1 Foundations\nArchitecture Limits & Performance Models",
            subtitle="Build quantitative intuition from operation counts, memory hierarchies, Amdahl scaling, and the Roofline model",
            footnote="HKUST ASC27 Curriculum  ·  Covers Knowledge Graph L1 (A1-A3) and L3 (C1-C2)",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M01 · WORKLOAD, TIMING & PRECISION",
            title="GEMM Work, Traffic, Timing, and Floating-Point Precision",
            subtitle="Count minimum floating-point operations and bytes before writing optimization code",
            bullets=[
                "Dense N x N GEMM executes 2N^3 FLOPs while reading and writing only 3N^2 elements.",
                "Arithmetic intensity grows as O(N), giving large GEMM strong compute-bound potential.",
                "Benchmarking requires cache warm-up, monotonic timers, and median reporting across trials.",
                "FP64, FP32, and BF16 trade mantissa precision against range, throughput, and memory footprint.",
            ],
            formula="W = 2N^3 FLOPs,   Q_min = 3N^2 * b Bytes   =>   I_max = 2N / (3b)",
            formula_caption="b = element width (8 B for FP64); unblocked naive loops trigger up to 2N^3 * b memory traffic",
            image_path=img("m01_gemm_work_traffic.png"),
            image_caption="Growth of GEMM FLOPs (2N^3), naive unblocked traffic, and minimum byte traffic vs. matrix size N",
            footnote="Lab: implement C++ triple-loop GEMM; compare ijk vs. ikj loop order and -O3 with perf stat",
            speaker_notes=(
                "1. First-Principles Derivation: C[i,j] = sum_k A[i,k]*B[k,j] performs N^3 fused multiply-adds (2N^3 FLOPs). "
                "Naive ijk accesses B with stride N, causing repeated cache evictions and turning O(N^2) theoretical traffic into O(N^3) real DRAM reads.\n"
                "2. Required Lab: time N=1024 FP64 GEMM with clock_gettime(CLOCK_MONOTONIC) and inspect IPC/cache-misses via perf stat -e cycles,instructions,cache-misses.\n"
                "3. Classic Resources: CS:APP Chapters 2 & 5; MIT 6.172 Lecture 1 (Bentley Rules & Matrix Multiplication).\n"
                "4. ASC Tip: spend the first 10 minutes on any new problem calculating theoretical FLOPs and minimum bytes to expose headroom immediately."
            ),
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M02 · MEMORY WALL & NUMA",
            title="Memory Wall, Cache Locality, and Dual-Socket NUMA",
            subtitle="Moving one byte from DRAM costs orders of magnitude more latency and energy than one FMA",
            bullets=[
                "Latency spans two orders of magnitude from registers to DRAM while compute outpaces bandwidth.",
                "Loop permutation exploits spatial locality; cache tiling reuses blocks to capture temporal locality.",
                "Dual-socket servers suffer remote UPI/xGMI hops whenever threads read across NUMA domains.",
                "Linux uses First-Touch page placement, so the initializing thread determines physical memory locality.",
            ],
            formula="T_eff = T_hit + MissRate * T_miss    (L1 ~1 ns vs. DRAM ~80 ns)",
            formula_caption="Choose tile size B such that 3 * B^2 * sizeof(T) fits comfortably inside L1 or L2 cache",
            image_path=img("m02_memory_hierarchy_numa.png"),
            image_caption="Memory hierarchy latency/bandwidth tiers (left) and dual-socket NUMA local vs. remote hops (right)",
            footnote="Lab: run STREAM Triad with numactl --cpunodebind/--membind to quantify local vs. cross-socket penalty",
            speaker_notes=(
                "1. First-Principles Derivation: off-chip pin count and wire capacitance energy (pJ/bit) constrain DRAM bandwidth far more tightly than transistor logic density.\n"
                "2. Required Lab: compile STREAM Triad, compare local binding (--cpunodebind=0 --membind=0) against cross-socket (--membind=1), and verify LLC miss drop via perf stat -e LLC-load-misses.\n"
                "3. Classic Resources: CS:APP Chapter 6; Ulrich Drepper, What Every Programmer Should Know About Memory.\n"
                "4. ASC Tip: finals nodes often pack 256 cores across 2 sockets (e.g., ASC26 dual EPYC 9755). Ignoring NUMA and First-Touch easily surrenders 30% to 50% of memory bandwidth."
            ),
            accent_color=PALETTE["coral"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M03 · AMDAHL & GUSTAFSON LAWS",
            title="Amdahl and Gustafson Laws: Physical Scaling Bounds",
            subtitle="Serial fractions, barriers, and load imbalance cap parallel speedup long before core count runs out",
            bullets=[
                "Under strong scaling, a 5% serial fraction caps maximum speedup at 20x regardless of core count.",
                "Weak scaling grows problem size with processor count, exposing why exascale clusters target larger grids.",
                "Locks, global reductions, file I/O, and straggler ranks behave mathematically like serial sections.",
                "Optimizing a sub-kernel before measuring its whole-program share yields minimal wall-time gain.",
            ],
            formula="Amdahl: S(k) = 1 / [(1 - f) + f / k]     Gustafson: S_w(k) = (1 - s) + s * k",
            formula_caption="f = parallel fraction; as k -> infinity, strong scaling converges strictly to 1 / (1 - f)",
            image_path=img("m03_amdahl_gustafson.png"),
            image_caption="Amdahl strong-scaling asymptotes (left) contrasted with Gustafson weak scaling (right)",
            footnote="Lab: measure 1 to 64-core strong and weak scaling curves on a 2D heat solver and fit empirical (1 - f)",
            speaker_notes=(
                "1. First-Principles Derivation: any non-overlapped serial setup, synchronization barrier, or tail-latency rank sits inside (1 - f).\n"
                "2. Real ASC Evidence: in ASC26 AMSS-NCKU, speeding up the RHS kernel by 1.47x yielded only 1.22x full-program speedup because RHS was just ~20% of CPU runtime.\n"
                "3. Classic Resources: Hennessy & Patterson Chapter 1; Stanford CS149 Lecture 2.\n"
                "4. ASC Tip: in English Proposals, explicitly separate strong scaling (fixed test case wall time) from weak scaling and diagnose sub-linear curves with profiler breakdowns."
            ),
            accent_color=PALETTE["accent"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M04 · ROOFLINE MODEL",
            title="Roofline Model: Bounding Compute and Memory Regimes",
            subtitle="One log-log diagram diagnoses whether to cut data movement or raise arithmetic throughput",
            bullets=[
                "Arithmetic intensity I = FLOPs / Bytes places each kernel on the bandwidth slope or compute ceiling.",
                "Ridge point I* = P_peak / B marks hardware balance; GPU Tensor Cores push I* above 250 FLOP/B.",
                "Memory-bound kernels improve by moving right: operator fusion, cache reuse, and quantization.",
                "Compute-bound kernels improve by moving up: SIMD width, ILP, and Tensor Core utilization.",
            ],
            formula="R <= min( P_peak,  B * I ),     Ridge Point  I* = P_peak / B",
            formula_caption="R = attained throughput (FLOP/s), P_peak = peak compute, B = sustained memory bandwidth (B/s)",
            image_path=img("m04_roofline_model.png"),
            image_caption="Empirical log-log Roofline comparing CPU DDR5 and GPU HBM3 with canonical HPC/AI kernels",
            footnote="Lab: construct your node's Roofline from STREAM + DGEMM and plot 4 experimental kernels",
            speaker_notes=(
                "1. First-Principles Derivation: Roofline (Williams et al., 2009) bounds runtime by max(W / P_peak, Q / B), giving an immediate visual diagnostic.\n"
                "2. Required Lab: collect CPU Roofline via Intel Advisor or likwid-perfctr and GPU Roofline via ncu --set roofline on STREAM, SpMV, 3D Stencil, and GEMM.\n"
                "3. Classic Resources: Williams, Waterman, Patterson (2009), Roofline: An Insightful Visual Performance Model; NERSC Roofline guides.\n"
                "4. ASC Tip: a measured before-and-after Roofline plot in your Proposal proves root-cause understanding far better than raw speedup tables alone."
            ),
            accent_color=PALETTE["teal"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="two_col",
            section_tag="STAGE 1 · VERIFICATION RUBRIC",
            title="Stage 1 Verification Gate and Deliverables",
            subtitle="Every team member submits reproducible benchmarks and plots via Git PR by 2026-12-15",
            left_title="Quantitative Lab Milestones",
            left_bullets=[
                "Measure sustained node bandwidth (STREAM Triad) and FP64 peak DGEMM via automated scripts.",
                "Implement cache-blocked GEMM with loop permutation achieving >= 8x speedup over naive ijk.",
                "Benchmark dual-socket local vs. cross-NUMA bandwidth with explicit numactl logs.",
                "Plot an empirical machine Roofline marking STREAM, SpMV, Stencil, and tiled GEMM.",
            ],
            right_title="Verification & Engineering Hygiene",
            right_bullets=[
                "Verify every optimized FP64 GEMM against reference output with max relative error < 1e-12.",
                "Report median and standard deviation across >= 5 timed runs after warm-up.",
                "Record compiler version, build flags, and lscpu / lstopo hardware topology snapshots.",
                "Follow HKUST ASC Git rules: clean commits, no binaries or raw datasets committed.",
            ],
            callout="Next transition (Stage 2): once single-core locality reaches hardware limits, scale outward via SIMD/OpenMP, distributed MPI, and GPU SIMT.",
            footnote="Stage 1 Gate Checkpoint: 2026-12-15",
            speaker_notes=(
                "Gate review format: dedicate 20 minutes during the Week 3 Wednesday meeting for 2 to 3 members to walk through their Roofline plots and perf counters live."
            ),
        )
    )
    return d


def build_deck_02() -> ODPDeck:
    d = ODPDeck(
        title="Stage 2 Parallelism & Acceleration: CPU, MPI & GPU (M05-M08)",
        deck_code="S2",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="STAGE 2 · WEEKS 4 TO 8 (2026-12-16 TO 2027-01-19) · M05 TO M08",
            title="Stage 2 Parallelism & Acceleration\nMulti-Core CPU, Distributed MPI, and GPU SIMT",
            subtitle="Unlock vector lanes, non-blocking halo overlap, tiled CUDA kernels, and hardware-pinned timeline profiling",
            footnote="HKUST ASC27 Curriculum  ·  Covers Knowledge Graph L2 (B1-B3) and L3 (C2 Timeline Profiling)",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M05 · CPU PARALLELISM",
            title="Three-Level CPU Parallelism: SIMD, OpenMP, and NUMA",
            subtitle="Full CPU performance requires simultaneous utilization of vector width, physical cores, and local RAM",
            bullets=[
                "AVX-512 processes 8 FP64 lanes per instruction; Structure-of-Arrays (SoA) ensures contiguous loads.",
                "OpenMP schedules (static, dynamic, guided) balance loop overhead against irregular iteration work.",
                "Threads writing adjacent variables in one 64 B cache line trigger costly False Sharing traffic.",
                "Pin threads with OMP_PROC_BIND and OMP_PLACES while parallelizing initialization for First-Touch.",
            ],
            formula="P_CPU = N_cores * f_clk * W_SIMD * 2 (FMA/cycle)",
            formula_caption="Missing vectorization, core pinning, or NUMA locality each costs a multiplicative factor",
            image_path=img("m05_simd_openmp_numa.png"),
            image_caption="SIMD vector lanes, 64 B False Sharing mitigation, and dual-socket NUMA binding",
            footnote="Lab: optimize 3D Stencil and SpMV with SoA layout, -march=native, OpenMP binding, and First-Touch",
            speaker_notes=(
                "1. First-Principles Derivation: after Dennard scaling ended, CPU throughput scaled via wider SIMD registers, dual FMA units, and high core counts rather than clock speed.\n"
                "2. Required Lab: compile with -O3 -march=native -fopt-info-vec-missed; compare unpinned runs against OMP_PROC_BIND=close OMP_PLACES=cores.\n"
                "3. Classic Resources: MIT 6.172 Lectures 4 & 10; OpenMP 5.2 Specification; Intel Optimization Reference Manual.\n"
                "4. ASC Tip: CPU-only finals apps appear almost every year (ASC25 AlphaFold3/DeepSeek, ASC26 QiboTN/ICON), making pure-CPU mastery essential."
            ),
            accent_color=PALETTE["accent"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M06 · DISTRIBUTED MEMORY & MPI",
            title="Multi-Node Scaling: MPI, Halo Exchange, and RDMA",
            subtitle="Crossing node boundaries shifts the bottleneck to network latency alpha and interconnect bandwidth B",
            bullets=[
                "Hockney's model separates transfer time into fixed latency alpha and bandwidth term m / B.",
                "Small messages sit in the latency regime; aggregate buffers to push past half-bandwidth size m_1/2.",
                "3D domain decomposition performs O(L^3) volume work while exchanging O(6L^2) halo surfaces.",
                "Posting MPI_Isend/Irecv before interior updates hides network latency behind local computation.",
            ],
            formula="T(m) = alpha + m / B,     Half-Bandwidth Point  m_1/2 = alpha * B",
            formula_caption="For m << alpha * B, latency dominates; volume-to-surface ratio L / 6 sets halo fraction",
            image_path=img("m06_mpi_halo_hockney.png"),
            image_caption="Hockney latency-bandwidth model (left) and non-blocking 3D Halo overlap pipeline (right)",
            footnote="Lab: fit alpha and B using OSU Micro-Benchmarks; implement non-blocking 3D 7-point Stencil",
            speaker_notes=(
                "1. First-Principles Derivation: inter-node fabrics (e.g., InfiniBand NDR400 RDMA) deliver 1 to 2 orders of magnitude lower bandwidth and microsecond latency compared to HBM/DDR.\n"
                "2. Required Lab: run osu_latency and osu_bw; refactor blocking MPI_Sendrecv into MPI_Isend/Irecv plus interior/boundary splitting and measure 4-node weak scaling.\n"
                "3. Classic Resources: Gropp et al., Using MPI; OSU Micro-Benchmarks; Grama et al., Introduction to Parallel Computing.\n"
                "4. ASC Tip: GoMars, ICON, and HPCG rely heavily on slimming halo payloads and mapping one MPI rank per NUMA socket paired with its local InfiniBand HCA."
            ),
            accent_color=PALETTE["teal"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M07 · GPU SIMT & CUDA GEMM",
            title="GPU SIMT Architecture: Hand-Tuned CUDA GEMM vs. cuBLAS",
            subtitle="Hide HBM latency with warp-level occupancy and amplify data reuse in Shared Memory and registers",
            bullets=[
                "GPUs execute 32-thread warps in lockstep; coalesce global loads and avoid warp branch divergence.",
                "Shared Memory tiling cuts global HBM traffic by factor B_K; pad arrays to avoid bank conflicts.",
                "2D Register Blocking accumulates TM x TN sub-tiles per thread, relieving Shared Memory bandwidth.",
                "Vectorized float4 loads and double buffering lift hand-written GEMM close to vendor cuBLAS.",
            ],
            formula="HBM Traffic Reduction = B_K,     Tile Intensity  I_tile ~ 2 / [(1/B_M + 1/B_N) * b]",
            formula_caption="Hierarchical tiling turns O(N^3) HBM reads into O(N^3 / B_K) coalesced block loads",
            image_path=img("m07_cuda_gemm_tiling.png"),
            image_caption="GPU HBM -> SMEM -> Register tiling flow (top) and 5-step optimization ladder toward cuBLAS (bottom)",
            footnote="Lab: progress through 5 CUDA GEMM versions and track SM/DRAM SOL% with Nsight Compute",
            speaker_notes=(
                "1. First-Principles Derivation: GPUs dedicate die area to dense ALUs and massive register files instead of deep speculative logic, hiding hundreds of cycles of HBM latency through zero-overhead warp switching.\n"
                "2. Required Lab: inspect each iteration via ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,dram__throughput.avg.pct_of_peak_sustained_elapsed to watch bottlenecks migrate from DRAM to SMEM to FMA.\n"
                "3. Classic Resources: NVIDIA CUDA C++ Programming Guide; Simon Boehm, How to Optimize a CUDA Matmul Kernel; Stanford CS149 GPU lectures.\n"
                "4. ASC Tip: custom fused operators (e.g., QLU's NHWC GroupNorm/GEGLU in UnifoLM or ZJU's register-blocked 3D Stencil in AMSS-NCKU) reuse these exact tiling mechanics."
            ),
            accent_color=PALETTE["gold"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M08 · SLURM & TIMELINE PROFILING",
            title="Slurm Topology Pinning and Timeline Profiling (nsys / Score-P)",
            subtitle="Without a unified timeline, hidden synchronization bubbles and cross-PCIe mismatches stay invisible",
            bullets=[
                "Slurm scripts must explicitly bind ranks to CPU cores, local NUMA memory, and closest GPU/NIC.",
                "Nsight Systems exposes CPU launches, PCIe transfers, and GPU streams on one shared clock.",
                "Page-locked (Pinned) host memory enables true async overlap across H2D, compute, and D2H engines.",
                "Score-P and Scalasca diagnose MPI barrier wait times and OpenMP load skew across nodes.",
            ],
            formula="T_pipe = max(T_H2D, T_kernel, T_D2H) + Startup/Drain  <<  T_H2D + T_kernel + T_D2H",
            formula_caption="Multi-stream async pipelining compresses serial sums into the single slowest engine stage",
            image_path=img("m08_timeline_profiling.png"),
            image_caption="Blocking sync bubbles before tuning (top) vs. pinned multi-stream async overlap after tuning (bottom)",
            footnote="Lab: combine srun --cpu-bind with nsys profile to eliminate injected sync stalls across GPU streams",
            speaker_notes=(
                "1. First-Principles Derivation: a node contains independent hardware engines (CPU cores, DMA copy engines, GPU SMs, RDMA NICs); blocking APIs serialize engines that can run concurrently.\n"
                "2. Required Lab: run nsys profile --trace=cuda,nvtx,osrt,mpi to pinpoint unexpected cudaStreamSynchronize gaps and tiny kernel launch overhead (fixable with CUDA Graphs).\n"
                "3. Classic Resources: NVIDIA Nsight Systems User Guide; Score-P Documentation; HKUST ITSO Slurm KB.\n"
                "4. ASC Tip: on-site finals prohibit hardware reboots once testing starts; verify lstopo and nvidia-smi topo -m bindings within the first 30 minutes of cluster bring-up."
            ),
            accent_color=PALETTE["violet"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="two_col",
            section_tag="STAGE 2 · VERIFICATION RUBRIC",
            title="Stage 2 Verification Gate and Preliminary Round Launch",
            subtitle="Week 8 (2027-01-19) coincides with ASC27 Preliminary Round opening; everyone needs a full parallel toolkit",
            left_title="Hands-on Acceptance Thresholds",
            left_bullets=[
                "CPU 3D Stencil with SIMD, OpenMP, and NUMA pinning reaches >= 75% of empirical STREAM ceiling.",
                "Multi-node MPI non-blocking 3D Stencil achieves >= 85% weak scaling efficiency up to 4 nodes.",
                "Hand-written FP32 CUDA GEMM reaches >= 75% of cuBLAS throughput with ncu Roofline proof.",
                "Slurm-pinned multi-stream GPU pipeline cuts end-to-end wall time >= 2x confirmed in nsys.",
            ],
            right_title="ASC27 Preliminary Kickoff (Jan 11 to Feb 28)",
            right_bullets=[
                "Complete official ASC27 registration and finalize team intent before 2027-01-10 midnight UTC+8.",
                "Run baseline builds and first-pass profiles for all preliminary tasks within 48 hours of release.",
                "Build automated numerical accuracy checkers before attempting aggressive code rewrites.",
                "Archive cluster topology graphs (lstopo, nvidia-smi topo -m) for the Proposal system chapter.",
            ],
            callout="Next transition (Stage 3): channel CPU, MPI, and GPU primitives into AI training, inference optimization, and scientific GPU porting.",
            footnote="Stage 2 Gate Checkpoint: 2027-01-19",
            speaker_notes=(
                "Schedule sync: because ASC27 Preliminary Round starts Jan 11, swap generic practice stencils in Weeks 7-8 directly for hot kernels extracted from the newly released ASC27 tasks."
            ),
        )
    )
    return d


def build_deck_03() -> ODPDeck:
    d = ODPDeck(
        title="Stage 3 AI Systems & Performance Tuning (M09-M12)",
        deck_code="S3",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="STAGE 3 · WEEKS 9 TO 13 (2027-01-20 TO 2027-02-23) · M09 TO M12",
            title="Stage 3 AI Systems & Tuning\nDistributed Training, Inference,\nand GPU Porting",
            subtitle="Memory budgets, 3D collectives, inference latency, and long-horizon numerical regression",
            footnote="HKUST ASC27 Curriculum  ·  Covers Knowledge Graph L4 (D1-D3) and L3 (C3 Regression & Reproducibility)",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M09 · MEMORY BUDGET & MIXED PRECISION",
            title="Transformer Memory Budgets and Mixed-Precision Training",
            subtitle="Exact accounting of static optimizer state and dynamic activations governs model fit and MFU",
            bullets=[
                "Mixed-precision AdamW holds 16 bytes per parameter in static state (weights, grads, FP32 moments).",
                "Activations grow with batch size and sequence length; activation checkpointing trades FLOPs for VRAM.",
                "BF16 preserves FP32's 8-bit exponent range, removing fragile FP16 loss scaling in LLM training.",
                "FP8 Tensor Cores double math throughput when paired with blockwise scaling factors for stability.",
            ],
            formula="M_train ~ 16 * Phi  +  O(B * S * L * H)  +  Workspace   (Bytes)",
            formula_caption="Phi = parameter count (7B static state alone ~112 GB); total training work ~ 6 * Phi * D FLOPs",
            image_path=img("m09_transformer_memory_precision.png"),
            image_caption="7B AdamW memory breakdown with checkpointing (left) and IEEE/BF16/FP8 bit layouts (right)",
            footnote="Lab: build a PyTorch VRAM predictor (<5% error) and benchmark BF16 + FlashAttention vs. FP32",
            speaker_notes=(
                "1. First-Principles Derivation: static memory = 2B (BF16 weight) + 2B (BF16 grad) + 4B (FP32 master weight) + 4B (Adam m) + 4B (Adam v) = 16*Phi bytes. "
                "FlashAttention fuses tiled softmax inside on-chip SRAM, cutting attention memory from O(S^2) to O(S).\n"
                "2. Required Lab: validate your analytical predictor against torch.cuda.memory_snapshot() and compare MFU and loss convergence across FP32 vs. BF16.\n"
                "3. Classic Resources: Micikevicius et al. (2018), Mixed Precision Training; Dao et al., FlashAttention-2; Korthikanti et al. (2022) selective recomputation.\n"
                "4. ASC Tip: ASC22 Yuan 4.7B and ASC26 UnifoLM prelim (>=16-bit rule) both hinge on maximizing throughput while respecting strict precision and convergence gates."
            ),
            accent_color=PALETTE["violet"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M10 · DISTRIBUTED TRAINING & COLLECTIVES",
            title="3D Distributed Training: DP, FSDP, TP, PP, and Ring All-Reduce",
            subtitle="Place high-frequency collectives inside high-bandwidth NVLink domains and sparse traffic across nodes",
            bullets=[
                "ZeRO and FSDP shard optimizer states, gradients, and parameters to remove cross-GPU state redundancy.",
                "Tensor Parallel executes two All-Reduces per layer and belongs almost exclusively inside NVLink nodes.",
                "Pipeline Parallel sends point-to-point activations across nodes; 1F1B scheduling trims pipeline bubbles.",
                "Ring All-Reduce transfers 2(p-1)G/p bytes per rank, keeping bandwidth cost flat as GPU count p grows.",
            ],
            formula="Ring All-Reduce Volume / Rank = 2 * (p - 1) / p * G   ->   2G  (Bytes)",
            formula_caption="G = total gradient bytes, p = GPU count; overlap NCCL/RCCL buckets with backward pass",
            image_path=img("m10_distributed_training_ring.png"),
            image_caption="Mapping 3D parallelism to NVLink vs. IB fabrics (left) and 4-GPU Ring All-Reduce flow (right)",
            footnote="Lab: measure BusBW with nccl-tests (all_reduce_perf) and compare PyTorch DDP vs. FSDP scaling",
            speaker_notes=(
                "1. First-Principles Derivation: match each parallelism axis's communication-to-compute ratio against link speeds (NVLink ~900 GB/s vs. PCIe ~64 GB/s vs. IB NDR400 ~50 GB/s).\n"
                "2. Required Lab: run nccl-tests intra-node and inter-node; test how TP=2 behaves with and without NVLink to see the PCIe penalty firsthand.\n"
                "3. Classic Resources: Shoeybi et al., Megatron-LM; Rajbhandari et al., ZeRO; NVIDIA NCCL documentation.\n"
                "4. ASC Tip: finals servers often lack NVLink (e.g., <= 2 PCIe GPUs per server in ASC26). Avoid cross-PCIe Tensor Parallel; favor Data/FSDP or sample-level parallelism."
            ),
            accent_color=PALETTE["accent"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M11 · AI INFERENCE OPTIMIZATION",
            title="AI Inference Regimes: Prefill, Decode, KV Cache, and Denoising",
            subtitle="Inference spans opposite sides of the Roofline, demanding distinct compute and bandwidth tactics",
            bullets=[
                "LLM Prefill runs compute-bound GEMMs (TTFT); Decode streams full weights per token (bandwidth-bound).",
                "Weight quantization (INT8/INT4) cuts bytes loaded per token and lifts Decode speed proportionally.",
                "KV Cache grows with batch and sequence length; PagedAttention and GQA prevent VRAM fragmentation.",
                "Diffusion and world models accelerate via resident serving, TensorRT, CUDA Graphs, and TeaCache.",
            ],
            formula="Decode Ceiling <= B_mem / (W_bytes + KV_bytes),   KV = 2 * L * n_kv * d_h * S * B * b",
            formula_caption="Reducing bytes read per step and kernel launch latency unifies LLM and world-model tuning",
            image_path=img("m11_llm_inference_kv_denoising.png"),
            image_caption="LLM Prefill vs. Decode Roofline split (left) and World-Model denoising cache pipeline (right)",
            footnote="Lab: measure BF16 vs. INT4 Decode tok/s against memory bandwidth ceiling; capture CUDA Graphs",
            speaker_notes=(
                "1. First-Principles Derivation: single-stream autoregressive decode has arithmetic intensity ~1-2 FLOP/B, well below every modern ridge point; shrinking model bytes beats adding FLOPs.\n"
                "2. World Models & Diffusion: sequential UNet/DiT denoising steps exhibit slow latent drift, enabling TeaCache reuse and speculative cross-GPU step pipelining (ParaStep) alongside resident servers that eliminate cold model loads.\n"
                "3. Classic Resources: Kwon et al., vLLM / PagedAttention; llama.cpp quantization kernels; TensorRT Developer Guide.\n"
                "4. ASC Tip: read precision and state rules carefully (e.g., >=16-bit prelim vs. >=4-bit CPU finals, no cross-run KV reuse, hard PSNR >= 25 dB quality gates)."
            ),
            accent_color=PALETTE["teal"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M12 · SCIENTIFIC GPU PORTING & REGRESSION",
            title="Scientific GPU Porting, Bottleneck Migration, and Regression",
            subtitle="ASC26 AMSS-NCKU real case study: Compute-bound -> Transfer-bound -> Downstream Analysis-bound",
            bullets=[
                "First GPU port ran slower than CPU (4.5s -> 4.7s/step) due to 122 host-device roundtrips per step.",
                "Stage timing exposed 2/3 non-RHS overhead; full GPU memory residency slashed latency to 1.4s.",
                "Faster GPU caused CPU wave-extraction backpressure; 2+62 core split and 3-stage relay reached 0.85s.",
                "Stale-copy bugs grew 60x only after 200 steps; short smoke tests miss silent numerical divergence.",
            ],
            formula="T_step: 4.5s (CPU) -> 4.7s (GPU v1) -> 1.4s (Resident) -> 1.0s (2+62) -> 0.85s (Relay)",
            formula_caption="Without NVLink, keeping all grids resident on 1 of 4 H100s beat multi-GPU PCIe shuffling",
            image_path=img("m12_amss_bottleneck_shift.png"),
            image_caption="Tsinghua ASC26 AMSS-NCKU step-time evolution and GPU v1 overhead breakdown (Song Jiaxing talk)",
            footnote="Lab: port a 3D Stencil + grid interpolation loop to GPU with copy-validity guards and 200-step CI",
            speaker_notes=(
                "1. First-Principles Lesson: once on GPU, where data lives and how often it crosses PCIe dominates wall time far more than kernel FLOPs.\n"
                "2. Correctness Engineering: maintain explicit host/device validity flags on every array so reading a stale copy aborts immediately, holding 200-step error at ~1e-8.\n"
                "3. AI Coding Agent Workflow: tedious, localized migrations paired with an exact CPU reference oracle are ideal for agent-assisted iteration while humans set architecture and gates.\n"
                "4. Source: Song Jiaxing (Tsinghua ASC26 Team), Moving Black Holes onto GPUs (2026)."
            ),
            accent_color=PALETTE["coral"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="two_col",
            section_tag="STAGE 3 · PRELIM SPRINT CHECKPOINT",
            title="Stage 3 Verification Gate and Preliminary Proposal Freeze",
            subtitle="Week 13 (2027-02-23) locks technical results 5 days ahead of the ASC27 Preliminary deadline (2027-02-28)",
            left_title="Technical Deliverables",
            left_bullets=[
                "7B VRAM budget estimator validated within 5% of measured PyTorch memory snapshots.",
                "Multi-GPU FSDP/DDP training scaling >= 85% with documented nccl-tests BusBW.",
                "Inference ablation table covering quantization / TensorRT / Graph Capture plus quality checks.",
                "GPU-resident scientific kernel with stage-timer breakdown and passing 200-step error log.",
            ],
            right_title="ASC27 English Proposal Safeguards",
            right_bullets=[
                "Write every section originally from team measurements; committee enforces strict similarity checks.",
                "Structure each optimization as Hypothesis -> Profile Proof -> Change -> Ablation -> Accuracy Check.",
                "Freeze code 5 days early to re-run every final table end to end and package required directories.",
                "Verify every mandatory log, TensorBoard curve, output artifact, and source script before upload.",
            ],
            callout="Next transition (Stage 4): shift immediately after preliminary submission into HPL, HPCG, power-capped cluster drills, and English defense.",
            footnote="ASC27 Preliminary Submission Deadline: 2027-02-28 24:00 (UTC+8)",
            speaker_notes=(
                "Proposal strategy: preliminary evaluation selects finalists solely on academic merit and technical excellence. Clean first-principles figures and honest ablations stand out immediately."
            ),
        )
    )
    return d


def build_deck_04() -> ODPDeck:
    d = ODPDeck(
        title="Stage 4 ASC Competition Sprint (M13-M16)",
        deck_code="S4",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="STAGE 4 · WEEKS 14 TO 24 (2027-02-24 TO 2027-05-11) · M13 TO M16",
            title="Stage 4 ASC Competition Sprint\nBenchmarks, Power Walls, and Finals Execution",
            subtitle="Master HPL, HPCG, DVFS efficiency sweet spots, 48-hour blind mystery workflows, and English defense",
            footnote="HKUST ASC27 Curriculum  ·  Covers Knowledge Graph L5 (E1-E3) and Full-Stack Integration",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M13 · HPL BENCHMARK TUNING",
            title="HPL Tuning: Dense LU Factorization and Peak FP64 Throughput",
            subtitle="Maximize trailing DGEMM share while overlapping O(N^2) panel broadcasts behind computation",
            bullets=[
                "HPL solves dense Ax = b in (2/3)N^3 FP64 FLOPs, occupying 8N^2 bytes of system or GPU memory.",
                "Scale N to 80%-90% of available memory so O(N^3) compute amortizes O(N^2) panel communication.",
                "Block size NB balances DGEMM efficiency against load skew; choose process grid P x Q with P <= Q.",
                "Heterogeneous clusters tune CPU/GPU split, look-ahead depth, and per-card power limits jointly.",
            ],
            formula="W_HPL = (2/3) N^3 + 2 N^2 FLOPs,     Memory = 8 N^2 Bytes (FP64)",
            formula_caption="Passing run requires scaled residual ||Ax - b||_inf / (eps*(||A||||x||+||b||)*N) < 16",
            image_path=img("m13_hpl_panel_scaling.png"),
            image_caption="2D Block-Cyclic panel broadcast vs. trailing DGEMM (left) and efficiency vs. RAM fill N (right)",
            footnote="Lab: sweep N, NB, P x Q, RFACT, and BCAST on GPU/CPU HPL under controlled power ceilings",
            speaker_notes=(
                "1. First-Principles Derivation: >99% of HPL FLOPs occur in trailing DGEMM updates, yet the critical path sits on panel pivoting and broadcast—making look-ahead depth and IB bandwidth crucial.\n"
                "2. Required Lab: script automated parameter sweeps over (N, NB, P, Q, BCAST, DEPTH) while logging TFLOP/s, residual pass/fail, and wall power.\n"
                "3. Classic Resources: Netlib HPL Tuning Guide; NVIDIA HPC-Benchmarks container docs; ASC26 QLU Highest LINPACK case (4 nodes, 6x H200 + 2x W7900D + AI-assisted parameter search).\n"
                "4. ASC Tip: prepare pre-validated HPL.dat presets for multiple power tiers so you lock a safe baseline within the first hour on site."
            ),
            accent_color=PALETTE["accent"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M14 · HPCG BENCHMARK TUNING",
            title="HPCG Tuning: Sparse Grids, Multigrid, and Interconnect Latency",
            subtitle="A mirror of real scientific PDE codes bounded by memory bandwidth, indirection, and collectives",
            bullets=[
                "HPCG solves a 27-point 3D sparse linear system via Multigrid-Preconditioned Conjugate Gradient.",
                "Core SpMV and SymGS kernels sit near 0.25 FLOP/Byte, typically reaching only 1% to 5% of HPL peak.",
                "Symmetric Gauss-Seidel carries loop dependencies resolved via multi-coloring or block-independent order.",
                "Global dot-product MPI_Allreduce calls expose microsecond fabric latency and rank imbalance.",
            ],
            formula="I_HPCG ~ 0.25 FLOP/Byte   =>   R_HPCG ~ 0.25 * B_mem   (Strictly Memory & Latency Bound)",
            formula_caption="Contiguous subdomain dimensions, NUMA isolation, and per-socket IB HCAs deliver major gains",
            image_path=img("m14_hpcg_spmv_symgs.png"),
            image_caption="27-point 3D stencil & Multigrid V-Cycle (left) and why HPCG trails HPL efficiency (right)",
            footnote="Lab: run official HPCG, inspect YAML DDOT/SpMV/MG splits, and tune local (nx, ny, nz) + bindings",
            speaker_notes=(
                "1. First-Principles Derivation: unlike HPL's O(N) intensity, sparse non-zeros execute 2 FLOPs while fetching 8 B value + 4 B index + indirect vector entries, pinning performance to DRAM/HBM bandwidth and network latency.\n"
                "2. Required Lab: align local grid dimensions (nx, ny, nz) to multiples of 8 or 16 within official run-time specs; dissect YAML timings across DDOT, WAXPBY, SpMV, and MG.\n"
                "3. Classic Resources: Dongarra et al., Toward a New Metric for Ranking HPC Systems; official HPCG GitHub repository.\n"
                "4. ASC Tip: Tsinghua won ASC26 HPCG by matching H100 memory bandwidth with dedicated InfiniBand NICs per CPU socket to attack both memory and latency walls."
            ),
            accent_color=PALETTE["teal"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M15 · POWER WALL & CLUSTER DESIGN",
            title="Power Wall Engineering: DVFS Sweet Spots and 3/4/5 kW Drills",
            subtitle="Dynamic power scales roughly as frequency cubed, so disciplined capping raises cluster throughput",
            bullets=[
                "CMOS dynamic power obeys P_dyn proportional to C * V^2 * f; top boost clocks waste disproportionate watts.",
                "Capping GPU power near the efficiency knee frees budget for extra accelerators or CPU headroom.",
                "Historical finals limits rose from 3 kW (ASC22) to 4 kW (ASC25) and 5 kW (ASC26).",
                "Because ASC27 power limits remain unannounced, prepare pre-tested 3, 4, and 5 kW presets.",
            ],
            formula="P_total = P_static + C_eff * V^2 * f,     Energy Efficiency = R(f) / P(f)",
            formula_caption="Total energy E = integral P(t) dt; contest PDU meters enforce real-time peak cap compliance",
            image_path=img("m15_power_wall_dvfs.png"),
            image_caption="Normalized CMOS cubic power curve & efficiency knee (left) and ASC 3/4/5 kW budget history (right)",
            footnote="Lab: sweep nvidia-smi -pl / rocm-smi power caps while logging IPMI wall watts and HPL/AI throughput",
            speaker_notes=(
                "1. First-Principles Derivation: with V scaling roughly linearly with f, P_dyn scales near f^3 while throughput scales linearly with f. "
                "Trimming clock frequency by 15% cuts dynamic power by ~35%-40%, letting the same power cap drive more hardware.\n"
                "2. Historical Context: ASC22 finals enforced 3 kW; ASC25 enforced 4 kW (>=3 nodes, <=2 kW/node); ASC26 enforced 5 kW (>=3 nodes, <=2 kW/node, no hardware reboot during testing; 25 teams fielded 99 servers and 174 GPUs, 64% using 4 nodes).\n"
                "3. Strict Rule Reminder: never assume ASC27 is 5 kW until officially published; keep 5%-8% spike headroom below any PDU threshold.\n"
                "4. Classic Resources: Hennessy & Patterson Section 1.5; Green500 measurement methodology."
            ),
            accent_color=PALETTE["coral"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="content_visual",
            section_tag="M16 · MYSTERY APP, REPRODUCIBILITY & PRESENTATION",
            title="48-Hour Mystery Workflow, Scoring Strategy, and English Defense",
            subtitle="Finals reward zero-fault correctness, disciplined time allocation, and crisp technical communication",
            bullets=[
                "When the mystery app unlocks on site, spend the first 2 hours on baseline, checker, and profiler.",
                "Failed accuracy or rule violation scores 0; keep every algorithmic change mathematically equivalent.",
                "Application tasks dominate total points (e.g., four 18-pt apps + 8-pt group task in ASC26).",
                "English poster and Q&A carry 10 points; defend bottlenecks, ablations, and cluster choices cleanly.",
            ],
            formula="P_app = (T_min / T_team) * Full + Base,     P_bench = (R_team / R_max) * Full + Base",
            formula_caption="Illustrative ASC26 finals formula (ASC27 scoring TBD); zero points if accuracy verification fails",
            image_path=img("m16_asc_workflow_scoring.png"),
            image_caption="48-hour on-site regression pipeline (top) and ASC26 100-point scoring breakdown (bottom)",
            footnote="Lab: run two full 48-hour closed mock finals with an unseen mystery task and 15-min English Q&A",
            speaker_notes=(
                "1. On-Site Pacing: finish racking, OS/driver/IB verification, and safe HPL/HPCG presets during setup days. Once testing opens, clusters cannot reboot or change hardware.\n"
                "2. Group Competition: cross-university alliances receive the task ~5 days before finals; establish clean Git patch review and daily syncs early while tuning bindings locally.\n"
                "3. English Defense Coaching: avoid reading slides aloud; lead with bottleneck evidence, before/after profiles, correctness proofs, and prepared answers to common judge questions.\n"
                "4. Sources: ASC27 Call for Participation and ASC26 Final Competition Notification."
            ),
            accent_color=PALETTE["gold"],
        )
    )
    d.add_slide(
        SlideSpec(
            kind="two_col",
            section_tag="STAGE 4 · FINAL READINESS CHECKLIST",
            title="Pre-Finals Departure Readiness Checklist",
            subtitle="Eliminate operational surprises during training so competition hours stay focused on performance",
            left_title="Cluster & Operations Preparedness",
            left_bullets=[
                "3 kW, 4 kW, and 5 kW power presets and live IPMI wattage watchdog scripts verified.",
                "Offline provisioning scripts (OS tuning, CUDA/ROCm, MPI, Slurm, containers) tested from scratch.",
                "HPL and HPCG parameter sweep scripts with automatic residual checks deliver safe scores in < 1 h.",
                "Team comfortable compiling and profiling on both NVIDIA CUDA and AMD ROCm/HIP stacks.",
            ],
            right_title="Applications, Mystery Drills & Defense",
            right_bullets=[
                "Completed >= 2 full 48-hour blind mystery simulations including Git patch collaboration.",
                "Every application ships with a 1-minute smoke check and full-length accuracy regression gate.",
                "A0 English poster layout and 10-minute presentation rehearsed with 30 judge Q&A flashcards.",
                "Codebase audited for mathematical equivalence and zero dataset-specific hardcoding.",
            ],
            callout="Put every stage to the test right away by dissecting 10 verified real past ASC problems in Deck 05.",
            footnote="HKUST ASC27 Final Sprint Gate: 2027-05-11",
            speaker_notes=(
                "Final coaching reminder: under competition sleep deprivation, the top two causes of lost medals are unverified submissions and PDU trips. Automate both guardrails."
            ),
        )
    )
    return d


def build_deck_05() -> ODPDeck:
    d = ODPDeck(
        title="Verified Past ASC Competition Problems (C01-C10)",
        deck_code="C",
    )
    d.add_slide(
        SlideSpec(
            kind="cover",
            section_tag="PAST ASC ARCHIVE · VERIFIED REAL PROBLEMS (2022 TO 2026) · C01 TO C10",
            title="Verified Past ASC Problem Analysis\nFrom Domain Science to Bottlenecks & Tuning",
            subtitle="Ten real preliminary, final, mystery, and group-competition tasks mapped directly to our 4-stage curriculum",
            footnote="HKUST ASC27 Curriculum  ·  Fixed 3-part breakdown per problem: What · Math & Profile · Roadmap Link",
        )
    )
    d.add_slide(
        SlideSpec(
            kind="table",
            section_tag="C00 · PROBLEM MATRIX",
            title="Master Index of Ten Verified Past ASC Problems (C01 to C10)",
            subtitle="Spanning LLM pretraining/inference, AI for Science, planetary climate, numerical relativity, quantum TN, and world models",
            table_headers=["ID", "Year & Problem", "Hardware & Power Rules", "Core Compute Profile", "Roadmap Link"],
            table_col_widths_cm=[1.7, 7.2, 6.4, 9.15, 6.4],
            table_rows=[
                ["C01", "ASC22 Yuan 4.7B LLM", "GPU cluster · 3 kW finals", "Dense GEMM / Attention · compute + comms", "S3 M09, M10 · S4 M15"],
                ["C02", "ASC22 DeePMD-kit", "CPU/GPU · 3 kW finals", "Irregular neighbor gather + small MLP GEMM", "S1 M02 · S2 M07 · S3 M09"],
                ["C03", "ASC24 GoMars Atmosphere", "Multi-node CPU · 3 kW", "Lat-lon non-hydrostatic stencil + polar skew", "S2 M05, M06 · S4 M14"],
                ["C04", "ASC25 AlphaFold3", "Prelim GPU / Finals CPU-only 4 kW", "Pairformer O(N^3) triangle attn + diffusion", "S2 M05, M08 · S3 M09, M11"],
                ["C05", "ASC25 DeepSeek R1-Distill 32B", "Finals CPU-only 4 kW · >=4-bit", "Memory-BW-bound decode + KV cache", "S1 M02, M04 · S2 M05 · S3 M11"],
                ["C06", "ASC26 UnifoLM-WMA-0", "Prelim >=16-bit / Finals 5 kW open", "UNet diffusion denoising + video I/O", "S2 M07, M08 · S3 M11"],
                ["C07", "ASC26 AMSS-NCKU", "Hetero CPU+GPU · 5 kW", "9-level AMR 3D stencil + interp + wave extract", "S1 M03 · S2 M06-08 · S3 M12"],
                ["C08", "ASC26 QiboTN Quantum", "Finals CPU-only 5 kW", "Tensor network contraction (vs 16*2^n wall)", "S1 M02, M04 · S2 M05, M06"],
                ["C09", "ASC26 Mystery LeWM (JEPA)", "AMD W7900D only · 5 kW", "Latent Encoder-Predictor + CEM planning", "S2 M07, M08 · S3 M11 · S4 M16"],
                ["C10", "ASC26 Group Task ICON", "Finals CPU-only 5 kW · 8 pts", "Icosahedral multi-sphere coupling + Halo", "S2 M05, M06, M08 · S4 M14, M16"],
            ],
            footnote="All problem names, constraints, and team results verified from official ASC22/25/26 notices and committee slides",
            speaker_notes=(
                "Five-year trend analysis:\n"
                "1. AI tasks evolved from pretraining (Yuan) to CPU LLM inference (DeepSeek) to embodied and JEPA world models (UnifoLM, LeWM).\n"
                "2. CPU-only tasks recur every year (AlphaFold3, DeepSeek, QiboTN, ICON); pure-CPU skills win medals.\n"
                "3. Cross-vendor readiness (NVIDIA CUDA + AMD ROCm) and cross-school Git collaboration are permanent fixtures."
            ),
        )
    )

    problems = [
        SlideSpec(
            kind="problem",
            section_tag="C01 · ASC22 PRELIM & FINALS · LLM PRETRAINING",
            title="ASC22 Yuan 4.7B: Distributed LLM Pretraining",
            problem_meta="40 Layers · d=3072 · 24 Heads · seq=2048 · 1B Tokens · Loss < 7.0 · PyTorch · 3 kW Finals",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Pretrains a 4.7B-parameter Chinese language model (Inspur Yuan 1.0 architecture) on a 100 GB corpus, minimizing wall-clock time while driving convergence loss strictly below 7.0.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Transformer QKV projections, Self-Attention, and FFN dense GEMMs totaling ~6*Phi*D (~2.82e19 FLOPs for 1B tokens). Compute-bound per GPU, constrained cross-GPU by gradient synchronization.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M01/M04 (GEMM & Roofline), Stage 3 M09/M10 (16*Phi VRAM budgeting, FP16/BF16 mixed precision, DP/TP/PP & Ring All-Reduce), Stage 4 M15 (3 kW power management).",
                ),
            ],
            image_path=img("c01_asc22_yuan_llm.png"),
            image_caption="Yuan 4.7B training FLOPs, 3D parallel layout under 3 kW, and Loss < 7.0 acceptance curve",
            footnote="Source: ASC22 Preliminary & Final Competition Notifications (30 pts in Prelim)",
            speaker_notes=(
                "Rules & Winning Optimization Levers:\n"
                "- Mandatory deliverables include pretraining logs, TensorBoard files, loss curve, and reproducible code; missing files or final loss >= 7.0 yields 0.\n"
                "- Under the 3 kW finals cap, teams battled VRAM pressure and PCIe/IB All-Reduce stalls.\n"
                "- Top teams combined mixed precision, fused LayerNorm/Softmax/Adam kernels, backward-comm overlap, and tuned global batch size + warmup schedules to hit loss < 7.0 in minimal wall time."
            ),
            accent_color=PALETTE["violet"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C02 · ASC22 PRELIM & FINALS · AI FOR SCIENCE",
            title="ASC22 DeePMD-kit: Deep Potential Molecular Dynamics",
            problem_meta="Gordon Bell Lineage · water / Cu / Al-Cu-Mg Datasets · dp test RMSE Gate · 3 kW Finals",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Trains neural interatomic potentials with ab-initio quantum accuracy at classical MD speed, enabling million-atom materials and chemical simulations.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Two-regime workload: neighbor-list assembly and smooth descriptors are irregular memory-bound gathers; Embedding/Fitting MLPs run batched small GEMMs (compute-bound) with autodiff forces F = -grad(E).",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M04 (cache locality & dual-regime Roofline), Stage 2 M07/M08 (GPU kernel fusion & launch latency profiling), Stage 3 M09 (mixed precision & force-gradient stability).",
                ),
            ],
            image_path=img("c02_asc22_deepmd.png"),
            image_caption="DeePMD-kit descriptor gather, batched MLP potential network, and force backpropagation hotspots",
            footnote="Source: ASC22 Preliminary & Final Competition Notifications (official ASC22 branch)",
            speaker_notes=(
                "Rules & Winning Optimization Levers:\n"
                "- Teams must build from the designated ASC22 branch of DeePMD-kit and pass dp test energy and force RMSE verification.\n"
                "- Hotspots shift across water, copper, and Al-Cu-Mg alloy systems due to varying neighbor counts and frequent small-kernel launches.\n"
                "- Key optimizations: model compression / descriptor tabulation, custom fused CUDA operators for environment matrices, reduced precision-casting overhead, and async data pipelines."
            ),
            accent_color=PALETTE["teal"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C03 · ASC24 FINALS · PLANETARY CLIMATE",
            title="ASC24 GoMars: Martian Global Atmospheric Circulation",
            problem_meta="IAP CAS Non-Hydrostatic Mars Model · Multi-Node CPU · 3 kW Finals · SJTU Application Innovation",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Simulates global Martian atmospheric dynamics, dust transport, and thermal cycles to support landing-site meteorology and planetary climate research.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "3D finite-difference stencils on a non-hydrostatic latitude-longitude grid plus physical parameterizations. Strictly memory-bandwidth and MPI halo-bound, complicated by polar meridian convergence (CFL limits & load skew).",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M03 (cache blocking & Amdahl load balance), Stage 2 M05/M06 (SIMD vectorization, hybrid OpenMP/MPI, non-blocking halo overlap), Stage 4 M14 (low-intensity tuning).",
                ),
            ],
            image_path=img("c03_asc24_gomars.png"),
            image_caption="GoMars latitude-longitude polar convergence effect and MPI 2D domain decomposition halo strategy",
            footnote="Source: ASC24 public finals records and ASC26 committee historical problem overview",
            speaker_notes=(
                "Rules & Winning Optimization Levers:\n"
                "- Executed on multi-node CPU clusters under a 3 kW cap with strict physical-field error verification.\n"
                "- Lat-lon grids squeeze zonal cell spacing near both poles, creating polar filtering overhead and uneven MPI rank load.\n"
                "- Winning levers (SJTU Application Innovation): rebalanced 2D MPI decompositions, inner-loop refactoring for AVX-512 vectorization, non-blocking halo exchange overlapped with interior stencil sweeps, and reduced redundant I/O."
            ),
            accent_color=PALETTE["coral"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C04 · ASC25 PRELIM & FINALS · NOBEL-LEVEL AI4S",
            title="ASC25 AlphaFold3: Cross-Architecture Biomolecular Structure",
            problem_meta="Prelim CPU/GPU (BF16 >=16-bit) · Finals CPU-Only 4 kW (>=3 nodes, <=2 kW/node) · SJTU e-Prize 30x+",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Predicts 3D atomic complexes of proteins, DNA, RNA, and small-molecule ligands, accelerating structural biology and drug discovery in a 2024 Nobel Chemistry domain.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "MSA and Pairformer execute O(N^3) Triangle Multiplicative Updates and Triangle Attention (compute-heavy) followed by a diffusion structure module; long sequences strain tensor memory bandwidth and layout transposes.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M05/M08 (Xeon AMX/AVX-512 vectorization, NUMA pinning, timeline profiling), Stage 3 M09/M11 (BF16 mixed precision, inference graph compilation & layout fusion).",
                ),
            ],
            image_path=img("c04_asc25_alphafold3.png"),
            image_caption="AlphaFold3 pipeline and CPU-only dual Xeon 6760P AMX BF16 optimization path",
            footnote="Source: ASC25 Prelim/Final notifications and ASC26 committee retrospective (SJTU 30x+ speedup)",
            speaker_notes=(
                "Rules & Winning Optimization Levers:\n"
                "- Preliminary round permitted CPU/GPU with >=16-bit precision (BF16); Finals shifted to strict CPU-only 4 kW clusters (dual Xeon 6760P, >=3 nodes, <=2 kW/node).\n"
                "- Default JAX/XLA CPU execution under-utilized Intel AMX BF16 tile engines and suffered excessive intermediate tensor copies.\n"
                "- SJTU captured the e-Prize with >30x CPU speedup by replacing triangle hotspots with AMX-accelerated oneDNN BF16 kernels, eliminating layout transposes, and scheduling NUMA-local multi-instance workers."
            ),
            accent_color=PALETTE["accent"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C05 · ASC25 FINALS · CPU-ONLY LLM INFERENCE",
            title="ASC25 DeepSeek R1-Distill 32B: CPU-Only LLM Inference",
            problem_meta="Finals CPU-Only 4 kW · >=4-bit Quant Allowed · No Pruning · No Cross-Run KV Reuse · ZJU 14.9 tok/s",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Serves a 32B reasoning LLM at high token throughput without any GPUs inside a 4 kW CPU cluster, testing low-latency AI deployment on general-purpose servers.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Autoregressive decode scans the full weight matrix per generated token at arithmetic intensity < 2 FLOP/B, strictly pinned to DDR5 memory bandwidth (tok/s <= B_DDR5 / ModelBytes).",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M04 (DDR5 bandwidth ceiling & Roofline), Stage 2 M05 (AVX-512/AMX quantized GEMV & NUMA weight sharding), Stage 3 M11 (INT4 quantization & KV cache management).",
                ),
            ],
            image_path=img("c05_asc25_deepseek_r1.png"),
            image_caption="32B model footprint across BF16/INT8/INT4 vs. theoretical DDR5 decode throughput ceiling",
            footnote="Source: ASC25 Finals records (strictly forbidding pruning and cross-execution KV cache reuse)",
            speaker_notes=(
                "Rules & Winning Optimization Levers:\n"
                "- Allowed >=4-bit quantization while banning pruning and cross-run KV caching, verified against accuracy benchmarks.\n"
                "- First-principles math: shrinking 32B weights from BF16 (~64 GB) to INT4 (~16-18 GB) immediately lifts the DDR5 memory-bandwidth ceiling by ~3.5x to 4x.\n"
                "- ZJU reached 14.9 tok/s single-thread by fusing 4-bit dequantization directly into AVX-512/AMX microkernels, sharding weights strictly along NUMA domains, and saturating multi-channel DDR5."
            ),
            accent_color=PALETTE["gold"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C06 · ASC26 PRELIM & FINALS · EMBODIED WORLD MODEL",
            title="ASC26 UnifoLM-WMA-0: Embodied World Model Inference",
            problem_meta="Prelim 5x4=20 Cases (>=16-bit, PSNR>=25) · Finals 5 kW 6 Cases Open Precision/Sampler · PKU 26s / BUPT 30s",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Accelerates Unitree's embodied world model—a neural physics simulator generating predicted future video from robot actions—removing the planning bottleneck in VLA robotics.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Spatial-temporal UNet backbone with multi-step diffusion denoising (hybrid compute-bound attention/conv and memory-bound normalization), compounded by cold startup and video encoding I/O.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M07/M08 (fused GPU kernels & timeline profiling), Stage 3 M11 (resident serving, TensorRT, TeaCache latent caching, step-parallel execution & async video encoding).",
                ),
            ],
            image_path=img("c06_asc26_unifolm_wma.png"),
            image_caption="UnifoLM-WMA-0 pipeline and verified ASC26 speedup ladder from ~13 min baseline down to 26 s/case",
            footnote="Source: ASC26 Prelim/Final notifications and committee optimization report (pp. 12-15)",
            speaker_notes=(
                "Rules & Top Team Breakthroughs:\n"
                "- Hard visual quality gate: PSNR >= 25 dB (any single failing case zeroed the entire scene in Prelim). Prelim locked weights >=16-bit; Finals unlocked precision, samplers, and step counts.\n"
                "- Prelim standouts: QLU rewrote GroupNorm/GEGLU in TileLang/CUDA with NHWC fusion (traffic 8MN->4MN, 5.41x 1-GPU / 8.13x multi-GPU); SHU stacked TensorRT (8.40x) + UNet TeaCache (1.36x) + 2-GPU ParaStep speculative overlap for 8.22x end-to-end at 36.9 dB PSNR.\n"
                "- Finals leaders: PKU refactored into a minimal functional stack with graph compilation and decoupled action/video sampling (26 s/case); BUPT combined mmap fast loading, on-demand heads, TeaCache, and async streaming I/O (30 s/case, >20x)."
            ),
            accent_color=PALETTE["violet"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C07 · ASC26 PRELIM & FINALS · NUMERICAL RELATIVITY",
            title="ASC26 AMSS-NCKU: Binary Black Hole Gravitational Waves",
            problem_meta="Prelim + Finals · 5 kW · Trajectory RMS < 1% · ADM Constraint |v| <= 2 · ZJU 30x / THU 0.85 s/step",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Numerically solves Einstein's field equations to replay GW150914 inspiral, 3-black-hole head-on collision, and full merger-ringdown waveforms for gravitational-wave astronomy.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "TwoPunctures elliptic initial data followed by RK4 3D finite-difference stencils across 9 nested AMR levels (24 fields/cell, 32 substeps on finest level), inter-level interpolation, and spherical wave extraction.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M03 (Amdahl stage profiling), Stage 2 M07/M08 (register/SMEM tiling, Kernel Fission, async streams), Stage 3 M12 (GPU residency, 3-stage relay & 200-step regression).",
                ),
            ],
            image_path=img("c07_asc26_amss_ncku.png"),
            image_caption="9-level nested AMR black-hole subcycling (left) and ASC26 ZJU, THU, and PKU results (right)",
            footnote="Source: ASC26 committee optimization report (pp. 16-19) and Tsinghua Song Jiaxing talk",
            speaker_notes=(
                "Rules & Multi-Team Optimization Comparison:\n"
                "- Strict physics invariants: trajectory RMS error < 1%, ADM constraint violation < 2, and mathematically equivalent algorithms.\n"
                "- ZJU (44,425 s -> 2,376 s = 18.6x Prelim; up to 30x Finals): full GPU evolution, register-heavy layout, Kernel Fission, ghost-zone-only PCIe sync, and AI-assisted Fortran->CUDA migration.\n"
                "- THU (4.5 s -> 4.7 s -> 1.4 s -> 1.0 s -> 0.85 s/step): eliminated 122 host-device roundtrips via single-H100 residency, then broke CPU analysis backpressure with 2+62 core split and 3-stage relay.\n"
                "- UESTC: task-based OpenMP packing + device memory pool + prefetching; PKU: 5.50x speedup with 1.9e-9 RMS error."
            ),
            accent_color=PALETTE["coral"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C08 · ASC26 FINALS · CPU-ONLY QUANTUM SIMULATION",
            title="ASC26 QiboTN: CPU-Only Quantum Tensor Network Simulation",
            problem_meta="Finals CPU-Only 5 kW (GPU Use = 0 pts) · QFT / QAOA / Supremacy · Fudan C Rewrite 10x+",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Simulates quantum circuits (QFT, QAOA, random supremacy circuits) on classical supercomputers and verifies expectation values to support NISQ algorithm and error-correction research.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "State-vector complex128 storage requires 16 * 2^n bytes (40 qubits = 16 TiB, hitting the memory wall). QiboTN uses Matrix Product States and contraction-path optimization, shifting load to tensor contractions and Python overhead.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M01/M02/M04 (complexity accounting, exponential memory wall, cache layout), Stage 2 M05/M06 (C/C++ low-level rewrite, SIMD, OpenMP & multi-node contraction).",
                ),
            ],
            image_path=img("c08_asc26_qibotn.png"),
            image_caption="Exact 16*2^n complex128 state-vector memory wall (20q = 16 MiB, 40q = 16 TiB) vs. MPS scaling",
            footnote="Math erratum: ASC26 slide p.20 mislabeled 20q/40q as 16 GB/16 PB (1024x too high); exact values are 16 MiB and 16 TiB",
            speaker_notes=(
                "Verified Math Correction & Engineering Takeaway:\n"
                "- Exact calculation: one complex128 amplitude = 16 bytes -> M(n) = 16 * 2^n bytes. Thus n=20 is 16 MiB, n=30 is 16 GiB, n=40 is 16 TiB, and n=50 is 16 PiB (correcting the 1024x unit typo on slide p.20 of the committee overview).\n"
                "- Hard constraint: strictly CPU-only under 5 kW; invoking any GPU scores 0. Ranked by total wall clock after expectation-value verification.\n"
                "- Fudan University's winning insight: when interpreter dispatch and Python memory management overshadow raw FLOPs, rewriting the core contraction engine cleanly in C with custom memory pools yields tens-of-times speedup."
            ),
            accent_color=PALETTE["accent"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C09 · ASC26 MYSTERY APPLICATION · JEPA ON AMD ROCM",
            title="ASC26 Mystery App LeWorldModel: JEPA Planning on AMD ROCm",
            problem_meta="Revealed On Site · AMD W7900D Only · 5 kW · 200 PushT Cases · Success >= 90% · Top 3 > 100x",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Runs Yann LeCun's JEPA-based LeWorldModel to predict physical dynamics in compact latent space and plan 200 PushT control episodes with >= 90% task success.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Encoder-Predictor forward rollouts inside iterative Cross-Entropy Method (CEM) trajectory planning. Heavily bottlenecked by tiny-kernel launch latency, CPU-GPU syncs, and video encoding I/O on AMD ROCm.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M07/M08 (AMD ROCm/HIP portability, NUMA & timeline profiling), Stage 3 M11 (BF16, feature caching, HIP Graph capture), Stage 4 M16 (48-hour blind mystery workflow).",
                ),
            ],
            image_path=img("c09_asc26_leworldmodel.png"),
            image_caption="JEPA latent CEM planning loop (top) and ASC26 finals >100x benchmark: BUPT 14s, THU 16s, PKU 17s (bottom)",
            footnote="Source: ASC26 Mystery Application Notification and committee optimization report (pp. 22-23)",
            speaker_notes=(
                "Rules & Top-3 Playbooks (>100x over baseline):\n"
                "- Mandatory platform: sponsored AMD W7900D GPUs only (ROCm stack), 5 kW cluster cap, >= 90% PushT success across 200 cases.\n"
                "- BUPT (14 s): 2-node multi-process slicing + trimmed CEM iterations/candidates + BF16 & target/init feature cache + early-exit masking for solved episodes.\n"
                "- THU (16 s): NUMA pinning + environment worker pool + distributed sample-level CEM + Graph Capture/Replay eliminating launch overhead + async streaming video encoding.\n"
                "- PKU (17 s): Client/Server architecture + multi-node slicing + BF16 + zero-copy pure-tensor conversion removing CPU-GPU syncs."
            ),
            accent_color=PALETTE["teal"],
        ),
        SlideSpec(
            kind="problem",
            section_tag="C10 · ASC26 GROUP COMPETITION · GORDON BELL CLIMATE",
            title="ASC26 Group Competition ICON: Global Climate Earth System",
            problem_meta="Finals CPU-Only 5 kW · 8 Finals Points · RCE_torus / OMIP / aquaplanet · Shared Patch, Independent Runs",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Optimizes MPI-M's ICON framework (SC25 Gordon Bell Prize 1.25 km global coupled climate simulation) for next-generation digital-twin weather and carbon-cycle modeling.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Unstructured icosahedral geodesic mesh eliminates lat-lon polar singularities while solving coupled atmosphere, ocean, and sea-ice PDEs. Dominated by memory bandwidth, halo exchanges, and MPI synchronization.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M05/M06/M08 (explicit inner-loop SIMD, OpenMP scheduling, slim halo & MPI profiling), Stage 4 M14/M16 (sparse grid tuning & cross-university Git patch collaboration).",
                ),
            ],
            image_path=img("c10_asc26_icon_group.png"),
            image_caption="ICON uniform icosahedral mesh & 3 test cases (left) and winning 5-university alliance model (right)",
            footnote="Source: ASC26 Group Competition Task Description and committee report (pp. 24-25)",
            speaker_notes=(
                "Rules & Winning Alliance Results:\n"
                "- Released ~5 days before finals; 5 randomly mixed domestic/international teams form each alliance, sharing source patches freely while running CPU-only on their own 5 kW clusters (GPU use = 0).\n"
                "- Three cases: RCE_torus (24-day idealized atmosphere), OMIP (20-year ocean + sea-ice), aquaplanet (2-month coupled ocean).\n"
                "- Winning alliance (Qinghai Univ + SJTU + BUAA + BNU + EAFIT Colombia): tuned OpenMP scheduling, trimmed halo domain exchanges, pruned redundant kernels, enforced inner-loop SIMD vectorization, and gained ~5% extra via MPI sync optimization while passing full verification."
            ),
            accent_color=PALETTE["gold"],
        ),
    ]
    for p in problems:
        d.add_slide(p)

    return d


def main() -> None:
    decks = [
        ("00-overview-roadmap", build_deck_00),
        ("01-stage1-foundations", build_deck_01),
        ("02-stage2-parallelism", build_deck_02),
        ("03-stage3-ai-systems", build_deck_03),
        ("04-stage4-asc-sprint", build_deck_04),
        ("05-past-asc-problems", build_deck_05),
    ]

    missing = []
    for name, fn in decks:
        deck = fn()
        for s in deck.slides:
            if s.image_path and not Path(s.image_path).exists():
                missing.append(s.image_path)
    if missing:
        print("ERROR: Missing PNG diagrams:", file=sys.stderr)
        for m in sorted(set(missing)):
            print("  -", m, file=sys.stderr)
        sys.exit(1)

    for name, fn in decks:
        deck = fn()
        odp_path = ODP_DIR / f"{name}.odp"
        deck.save(odp_path)
        pdf_path, pptx_path = convert_odp_with_libreoffice(odp_path, PDF_DIR, PPTX_DIR)
        print(
            f"[OK] {name}: {len(deck.slides)} slides -> "
            f"{odp_path.name} ({odp_path.stat().st_size // 1024} KB), "
            f"{pptx_path.name} ({pptx_path.stat().st_size // 1024} KB), "
            f"{pdf_path.name} ({pdf_path.stat().st_size // 1024} KB)"
        )


if __name__ == "__main__":
    main()
