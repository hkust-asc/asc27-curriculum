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
            kind="two_col",
            section_tag="00 · PRELIMINARY ROUND & ONBOARDING",
            title="ASC Preliminary Round Format and How to Join",
            subtitle="Two-month remote engineering sprint that selects global finalists from written technical proposals",
            left_title="What Happens in the Preliminary Round",
            left_bullets=[
                "No on-site cluster yet: teams run benchmarks and apps on our own servers.",
                "Deliverable: one English technical proposal covering design, tuning, and results.",
                "Typical tasks: cluster design under power cap, HPL/HPCG, AI, and science apps.",
                "Judges score correctness, speedup evidence, methodology, and power analysis.",
                "Top teams worldwide advance to the May 2027 on-site finals.",
            ],
            right_title="How to Join HKUST ASC27 Today",
            right_bullets=[
                "No prior HPC background required; curiosity and Linux comfort are enough.",
                "Attend Wednesday evening sessions (18:30 to 20:00) and complete Stage 1 labs.",
                "Teams of 5 undergrads form before the Jan 10 registration deadline.",
                "Start tonight: explore the interactive labs and pick one starter benchmark.",
                "Repo & labs: hkust-asc.github.io/asc27-curriculum",
            ],
            callout="Timeline check: register by Jan 10, 2027; Preliminary Round runs Jan 11 to Feb 28, 2027 (24:00 UTC+8).",
            footnote="HKUST ASC Team · Open to all HKUST undergraduates",
            speaker_notes=(
                "Onboarding notes:\n"
                "1. Reassure beginners: everyone starts from Stage 1 together; you do not need prior MPI or CUDA experience to join.\n"
                "2. Clarify that Prelim is a remote 7-week engineering & writing sprint (Jan 11 to Feb 28), not an exam.\n"
                "3. Point attendees to the interactive web curriculum and team sign-up channel right after Q&A."
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
            callout="Four bridges: A3 Power → E1 Power Benchmarks; B2 RDMA → D2 Distributed Training; C2 Roofline → E2 Apps; C3 Regression → E3 Defense.",
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
            callout="Schedule anchors: register by Jan 10; run Stage 3 during Prelim (Jan 11 to Feb 28); run power and mystery drills Mar to May.",
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
                    "Bound compute, memory, Amdahl, and Roofline limits",
                    "Linux, C/C++, Git, perf, likwid, STREAM, numactl",
                    "Plot node Roofline; speed up tiled GEMM ≥ 8x",
                    "Proposal modeling and hotspot triage",
                ],
                [
                    "Stage 2 Parallelism\n5 wks (12/16 - 01/19)\nM05 to M08",
                    "Scale across SIMD, OpenMP, MPI, and CUDA",
                    "OpenMP, AVX2/512, MPI, CUDA/HIP, Slurm, nsys/ncu, Score-P",
                    "CUDA GEMM ≥ 75% cuBLAS; MPI weak scaling ≥ 85%",
                    "CPU-only apps, multi-node codes, custom GPU kernels",
                ],
                [
                    "Stage 3 AI Systems\n5 wks (01/20 - 02/23)\nM09 to M12",
                    "Cut AI memory/comms walls and port science to GPU",
                    "PyTorch, BF16/FP8, FSDP/Megatron, NCCL/RCCL, TensorRT, CUDA Graph",
                    "7B VRAM error ≤ 5%; GPU stencil passes 200-step check",
                    "LLM/World Model tasks (Prelim) and GPU science",
                ],
                [
                    "Stage 4 ASC Sprint\n11 wks (02/24 - 05/11)\nM13 to M16",
                    "Hit HPL/HPCG targets, power caps, and English Q&A",
                    "HPL, HPCG, MKL/OpenBLAS, nvidia-smi/rocm-smi, IPMI power telemetry",
                    "Tune 3/4/5 kW presets; pass 48 h mystery drill and mock Q&A",
                    "HPL/HPCG, power budget, mystery/group apps, 10-pt defense",
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
                "Baseline first: fix seeds and save one reference output and wall time.",
                "Bound the limit: count FLOPs and bytes to find the Roofline ceiling.",
                "Profile end to end: split time into compute, copy, sync, and I/O.",
                "Change one thing: test one edit and log speedup plus hardware efficiency.",
                "Verify long runs: check full-step error and power cap before merge.",
            ],
            right_title="Recommended 5-Student ASC Role Matrix",
            right_bullets=[
                "Cluster Lead: OS, GPU/IB drivers, RDMA, Slurm, HPL, and power limits.",
                "CPU Lead: SIMD, OpenMP, NUMA pinning, HPCG, and CPU-only tasks.",
                "GPU & Science Lead: CUDA/HIP porting, residency, async streams, checks.",
                "AI Systems Lead: mixed precision, FSDP, KV cache, TensorRT, world models.",
                "Shared work: English Proposal, ablation plots, poster, and mock Q&A.",
            ],
            callout="Hard rules: wrong answers score 0. Breaking the power cap disqualifies the run. Every speedup must reproduce.",
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
                "Dense N × N GEMM does 2N³ FLOPs on only 3N² elements.",
                "Reuse grows with N, so large GEMM becomes compute-bound.",
                "Warm up caches, use a monotonic timer, and report the median.",
                "FP64, FP32, and BF16 trade decimal precision for speed and VRAM.",
            ],
            formula="W = 2N³ FLOPs,  Q_min = 3N² · b Bytes  →  I_max = 2N / (3b)",
            formula_tex=r"W=2N^{3},\; Q_{\min}=3N^{2}b \;\Rightarrow\; I_{\max}=\frac{2N}{3b}",
            formula_symbols=[
                ("W", "total FLOPs"),
                ("N", "matrix side"),
                ("Q_min", "minimum bytes moved"),
                ("b", "bytes/value (8 B FP64)"),
                ("I_max", "max FLOP/byte"),
            ],
            formula_caption="b = bytes per value (8 B for FP64). Naive loops move up to 2N³ · b bytes.",
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
                "DRAM is ~80x slower than L1 cache; bytes cost more than math.",
                "Row-order loops use cache lines well; tiling reuses data in cache.",
                "Reading across CPU sockets pays a slow NUMA interconnect hop.",
                "Linux places each page on the socket that first writes to it.",
            ],
            formula="T_eff = T_hit + MissRate * T_miss    (L1 ~1 ns vs. DRAM ~80 ns)",
            formula_tex=r"T_{\mathrm{eff}}=T_{\mathrm{hit}}+\mathrm{MissRate}\cdot T_{\mathrm{miss}}",
            formula_symbols=[
                ("T_eff", "effective access time"),
                ("T_hit", "cache hit latency (~1 ns)"),
                ("MissRate", "fraction missing cache"),
                ("T_miss", "DRAM penalty (~80 ns)"),
            ],
            formula_caption="Pick tile size B so 3 · B² · sizeof(T) fits inside L1 or L2 cache.",
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
                "A 5% serial part caps strong scaling at 20x, even with infinite cores.",
                "Weak scaling grows problem size with cores to keep every core busy.",
                "Locks, barriers, I/O, and slow ranks act just like serial code.",
                "Measure a kernel's total runtime share before optimizing it.",
            ],
            formula="Amdahl: S(k) = 1 / [(1 - f) + f/k]   |   Gustafson: S_w(k) = (1 - s) + s·k",
            formula_tex=r"S(k)=\frac{1}{(1-f)+f/k},\quad S_{w}(k)=(1-s)+sk",
            formula_symbols=[
                ("S(k)", "strong speedup"),
                ("f", "parallel work fraction"),
                ("k", "worker count"),
                ("S_w(k)", "weak scaled speedup"),
                ("s", "scaled parallel share"),
            ],
            formula_caption="f = parallel fraction. As k → ∞, strong scaling stops at 1 / (1 - f).",
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
                "Intensity I = FLOPs / Byte places a kernel on the slope or flat roof.",
                "Ridge point I* = P_peak / B is the knee; GPUs push I* past 250 FLOP/B.",
                "Memory-bound (left of I*): cut bytes with fusion, tiling, or quantization.",
                "Compute-bound (right of I*): raise FLOPs with SIMD or Tensor Cores.",
            ],
            formula="R ≤ min(P_peak, B · I),   Ridge Point I* = P_peak / B",
            formula_tex=r"R\le\min(P_{\mathrm{peak}},\,B\cdot I),\quad I^{*}=\frac{P_{\mathrm{peak}}}{B}",
            formula_symbols=[
                ("R", "achievable FLOP/s"),
                ("P_peak", "peak compute (FLOP/s)"),
                ("B", "memory bandwidth (B/s)"),
                ("I", "intensity (FLOP/B)"),
                ("I*", "ridge point"),
            ],
            formula_caption="R = speed (FLOP/s), P_peak = peak compute, B = memory bandwidth (B/s).",
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
                "Measure node bandwidth (STREAM Triad) and peak FP64 DGEMM by script.",
                "Build tiled GEMM with loop reorder for ≥ 8x speedup over naive ijk.",
                "Log local vs. cross-socket NUMA bandwidth with numactl.",
                "Plot the node Roofline with STREAM, SpMV, Stencil, and tiled GEMM.",
            ],
            right_title="Verification & Engineering Hygiene",
            right_bullets=[
                "Check every FP64 GEMM against reference with relative error < 1e-12.",
                "Report median and std dev across ≥ 5 timed runs after warm-up.",
                "Save compiler flags and lscpu / lstopo topology snapshots.",
                "Follow Git rules: clean commits, no binaries or raw datasets.",
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
                "AVX-512 runs 8 FP64 lanes at once; use SoA layout for contiguous loads.",
                "Pick OpenMP static, dynamic, or guided schedules to balance uneven loops.",
                "Two cores writing one 64 B cache line trigger slow False Sharing bounces.",
                "Pin threads (OMP_PROC_BIND) and init arrays in parallel for First-Touch.",
            ],
            formula="P_CPU = N_cores · f_clk · W_SIMD · 2 (FMA/cycle)",
            formula_tex=r"P_{\mathrm{CPU}}=N_{\mathrm{cores}}\, f_{\mathrm{clk}}\, W_{\mathrm{SIMD}}\cdot 2",
            formula_symbols=[
                ("P_CPU", "peak CPU FLOP/s"),
                ("N_cores", "physical cores"),
                ("f_clk", "clock rate (Hz)"),
                ("W_SIMD", "vector lanes"),
                ("2", "FLOPs per FMA"),
            ],
            formula_caption="Missing SIMD, core pinning, or NUMA locality multiplies your slowdown.",
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
                "Hockney's law splits message time into fixed latency α plus size m / B.",
                "Small messages pay mostly latency; pack them past m_1/2 = α · B.",
                "A 3D subdomain computes O(L³) volume but sends only O(6L²) halo faces.",
                "Post MPI_Isend/Irecv before interior updates to hide network wait.",
            ],
            formula="T(m) = α + m / B,   Half-Bandwidth Size m_1/2 = α · B",
            formula_tex=r"T(m)=\alpha+\frac{m}{B},\quad m_{1/2}=\alpha B",
            formula_symbols=[
                ("T(m)", "transfer time"),
                ("α", "network latency (s)"),
                ("m", "message size (B)"),
                ("B", "link bandwidth (B/s)"),
                ("m_1/2", "half-bandwidth size"),
            ],
            formula_caption="When m ≪ α · B, latency dominates. Volume-to-surface ratio L/6 sets halo cost.",
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
                "GPUs run 32-thread warps together; coalesce HBM loads and avoid divergence.",
                "Shared Memory tiles cut HBM reads by B_K; pad rows to stop bank conflicts.",
                "Register blocking holds a TM × TN sub-tile per thread to relieve SMEM.",
                "float4 loads and double buffering bring custom GEMM close to cuBLAS.",
            ],
            formula="HBM Cut = B_K,   Tile Intensity I_tile ≈ 2 / [(1/B_M + 1/B_N) · b]",
            formula_tex=r"I_{\mathrm{tile}}\approx\frac{2}{(1/B_{M}+1/B_{N})\,b}",
            formula_symbols=[
                ("I_tile", "tiled FLOP/byte"),
                ("B_M, B_N", "output tile dimensions"),
                ("b", "bytes per element"),
            ],
            formula_caption="Tiling turns O(N³) HBM reads into O(N³ / B_K) coalesced block loads.",
            image_path=img("m07_cuda_gemm_tiling.png"),
            image_caption="GPU HBM → SMEM → Register tiling flow (top) and 5-step optimization ladder toward cuBLAS (bottom)",
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
                "Bind Slurm ranks explicitly to CPU cores, local NUMA RAM, and nearest GPU.",
                "Nsight Systems puts CPU calls, PCIe copies, and GPU kernels on one clock.",
                "Pinned host RAM lets H2D copy, compute, and D2H copy run at once.",
                "Score-P and Scalasca expose MPI barrier wait and OpenMP imbalance.",
            ],
            formula="T_pipe = max(T_H2D, T_kernel, T_D2H) + Drain ≪ T_H2D + T_kernel + T_D2H",
            formula_tex=r"T_{\mathrm{pipe}}=\max(T_{\mathrm{H2D}},T_{\mathrm{ker}},T_{\mathrm{D2H}})",
            formula_symbols=[
                ("T_pipe", "overlapped chunk time"),
                ("T_H2D", "host-to-GPU copy"),
                ("T_ker", "GPU kernel time"),
                ("T_D2H", "GPU-to-host copy"),
            ],
            formula_caption="Async streams shrink a serial sum down to the single slowest engine.",
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
                "CPU 3D Stencil (SIMD + OpenMP + NUMA) reaches ≥ 75% of STREAM.",
                "Multi-node MPI 3D Stencil hits ≥ 85% weak scaling up to 4 nodes.",
                "Custom FP32 CUDA GEMM hits ≥ 75% of cuBLAS with ncu Roofline proof.",
                "Multi-stream GPU pipeline cuts wall time ≥ 2x in nsys.",
            ],
            right_title="ASC27 Preliminary Kickoff (Jan 11 to Feb 28)",
            right_bullets=[
                "Finish ASC27 registration before 2027-01-10 24:00 UTC+8.",
                "Run baseline builds and first profiles within 48 h of task release.",
                "Write automated accuracy checkers before any aggressive code rewrite.",
                "Save lstopo and nvidia-smi topo -m graphs for the Proposal.",
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
                "Mixed-precision AdamW needs 16 bytes per parameter in static VRAM.",
                "Activations grow with batch and sequence length; checkpointing trades FLOPs for RAM.",
                "BF16 keeps FP32's exponent range, avoiding fragile FP16 loss scaling.",
                "FP8 Tensor Cores double throughput when paired with blockwise scaling.",
            ],
            formula="M_train ≈ 16 · Φ + O(B · S · L · H) + Workspace (Bytes)",
            formula_tex=r"M_{\mathrm{train}}\approx 16\Phi+O(B\,S\,L\,H)",
            formula_symbols=[
                ("M_train", "training VRAM (B)"),
                ("Φ", "parameter count"),
                ("16", "B/param (BF16+Adam)"),
                ("B,S,L,H", "batch, seq, layers, hidden"),
            ],
            formula_caption="Φ = parameters (7B static state ≈ 112 GB). Training compute ≈ 6 · Φ · D FLOPs.",
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
                "ZeRO and FSDP split weights, grads, and Adam state across GPUs.",
                "Tensor Parallel runs two All-Reduces per layer; keep it on NVLink.",
                "Pipeline Parallel sends activations across nodes; 1F1B cuts idle bubbles.",
                "Ring All-Reduce moves 2(p-1)G/p bytes per GPU, staying flat as p grows.",
            ],
            formula="Ring All-Reduce / GPU = 2 · (p - 1)/p · G  →  2G (Bytes)",
            formula_tex=r"V_{\mathrm{ring}}=\frac{2(p-1)}{p}G \rightarrow 2G",
            formula_symbols=[
                ("V_ring", "bytes sent per GPU"),
                ("p", "number of GPUs"),
                ("G", "full gradient size (B)"),
            ],
            formula_caption="G = gradient bytes, p = GPUs. Overlap NCCL/RCCL buckets with backward.",
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
                "Prefill is compute-bound GEMM; Decode streams all weights per token (BW-bound).",
                "INT8 and INT4 weights cut bytes read per token and lift Decode speed directly.",
                "KV Cache grows with batch and length; PagedAttention and GQA save VRAM.",
                "World models speed up via resident servers, TensorRT, CUDA Graphs, and TeaCache.",
            ],
            formula="Decode ≤ B_mem / (W + KV),   KV = 2 · L · n_kv · d_h · S · B · b",
            formula_tex=r"R_{\mathrm{dec}}\le\frac{B_{\mathrm{mem}}}{W+\mathrm{KV}}",
            formula_symbols=[
                ("R_dec", "decode tokens/s"),
                ("B_mem", "HBM bandwidth (B/s)"),
                ("W", "model weight bytes"),
                ("KV", "KV-cache bytes"),
            ],
            formula_caption="Cutting bytes per step and launch latency speeds up both LLMs and world models.",
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
            subtitle="ASC26 AMSS-NCKU case: Compute-bound → Transfer-bound → CPU Analysis-bound",
            bullets=[
                "GPU v1 was slower than CPU (4.5 s → 4.7 s) from 122 PCIe copies per step.",
                "Keeping all grids resident on one GPU cut step time down to 1.4 s.",
                "Next, CPU analysis stalled the GPU; a 2+62 split and 3-stage relay hit 0.85 s.",
                "Stale-copy bugs grew 60x after 200 steps; short tests miss silent drift.",
            ],
            formula="T_step: 4.5s (CPU) → 4.7s (v1) → 1.4s (Resident) → 1.0s → 0.85s",
            formula_tex=r"4.5\,\mathrm{s}\rightarrow 4.7\,\mathrm{s}\rightarrow 1.4\,\mathrm{s}\rightarrow 0.85\,\mathrm{s}",
            formula_symbols=[
                ("4.5s", "CPU baseline"),
                ("4.7s", "PCIe-bound v1"),
                ("1.4s", "GPU-resident"),
                ("0.85s", "fused & async"),
            ],
            formula_caption="Without NVLink, 1 resident H100 beat 4 GPUs shuffling grids over PCIe.",
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
                "7B VRAM estimator within 5% of measured PyTorch memory snapshots.",
                "Multi-GPU FSDP/DDP scaling ≥ 85% with nccl-tests BusBW logs.",
                "Inference ablation table (quantization, TensorRT, Graphs) plus accuracy.",
                "GPU-resident stencil with stage timers and passing 200-step error log.",
            ],
            right_title="ASC27 English Proposal Safeguards",
            right_bullets=[
                "Write every section from your own data; committee runs similarity checks.",
                "Show each edit as Hypothesis → Profile → Change → Ablation → Accuracy.",
                "Freeze code 5 days early to rerun every table and pack required folders.",
                "Verify every required log, curve, output file, and script before upload.",
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
                "HPL solves dense Ax = b in (2/3)N³ FP64 FLOPs using 8N² bytes of RAM.",
                "Fill 80% to 90% of RAM so O(N³) math hides O(N²) panel sends.",
                "Block size NB balances DGEMM speed vs. skew; pick grid P × Q with P ≤ Q.",
                "Tune CPU/GPU split, look-ahead depth, and per-GPU power caps together.",
            ],
            formula="W_HPL = (2/3)N³ + 2N² FLOPs,   Memory = 8N² Bytes (FP64)",
            formula_tex=r"W_{\mathrm{HPL}}=\tfrac{2}{3}N^{3}+2N^{2},\quad M=8N^{2}",
            formula_symbols=[
                ("W_HPL", "LU solve FLOPs"),
                ("N", "matrix order"),
                ("M", "FP64 matrix RAM (B)"),
                ("8", "bytes per FP64"),
            ],
            formula_caption="Valid run requires scaled residual ‖Ax - b‖∞ / (ε(‖A‖‖x‖ + ‖b‖)N) < 16.",
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
                "HPCG solves a 27-point 3D sparse grid with Multigrid Conjugate Gradient.",
                "SpMV and SymGS sit near 0.25 FLOP/B, hitting only 1% to 5% of HPL peak.",
                "SymGS has loop dependencies; break them with multi-coloring or blocks.",
                "Global MPI_Allreduce dot products expose network latency and rank skew.",
            ],
            formula="I_HPCG ≈ 0.25 FLOP/B  →  R_HPCG ≈ 0.25 · B_mem (Memory-Bound)",
            formula_tex=r"I_{\mathrm{HPCG}}\approx 0.25 \Rightarrow R\approx 0.25\, B_{\mathrm{mem}}",
            formula_symbols=[
                ("I_HPCG", "sparse intensity (FLOP/B)"),
                ("R", "sustained HPCG FLOP/s"),
                ("B_mem", "DRAM/HBM bandwidth (B/s)"),
            ],
            formula_caption="Clean grid sizes, NUMA pinning, and per-socket IB HCAs give the biggest gains.",
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
                "Dynamic power scales as C · V² · f ≈ f³; top boost clocks waste watts.",
                "Capping each GPU near its efficiency knee lets you run more GPUs.",
                "Past finals caps rose from 3 kW (ASC22) to 4 kW (ASC25) and 5 kW (ASC26).",
                "ASC27's cap is unannounced; keep pre-tested 3, 4, and 5 kW presets ready.",
            ],
            formula="P_total = P_static + C_eff · V² · f,   Efficiency = R(f) / P(f)",
            formula_tex=r"P=P_{\mathrm{static}}+C_{\mathrm{eff}}V^{2}f,\quad \eta=\frac{R(f)}{P(f)}",
            formula_symbols=[
                ("P", "total power (W)"),
                ("P_static", "leakage power (W)"),
                ("C_eff", "switched capacitance"),
                ("V, f", "voltage & clock"),
                ("η", "FLOP per Joule"),
            ],
            formula_caption="PDU meters enforce live peak watts; keep 5% to 8% spike headroom.",
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
                "Spend the first 2 hours of a mystery app on baseline, checker, and profiler.",
                "Any wrong answer or rule break scores 0; keep edits mathematically equivalent.",
                "App tasks carry most points (four 18-pt apps + 8-pt group task in ASC26).",
                "English poster and Q&A carry 10 points; lead with profiles and ablations.",
            ],
            formula="P_app = (T_min / T_team) · Full + Base,   P_bench = (R_team / R_max) · Full + Base",
            formula_tex=r"P_{\mathrm{app}}=\frac{T_{\min}}{T_{\mathrm{team}}}\,\mathrm{Full}+\mathrm{Base}",
            formula_symbols=[
                ("P_app", "application score"),
                ("T_min", "fastest valid time"),
                ("T_team", "your valid time"),
                ("Full, Base", "max & baseline points"),
            ],
            formula_caption="ASC26 reference formula (ASC27 TBD). Failed verification always scores 0.",
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
                "Verify 3, 4, and 5 kW power presets and live IPMI wattage watchdogs.",
                "Test offline setup scripts (OS, CUDA/ROCm, MPI, Slurm) from scratch.",
                "Run HPL/HPCG sweep scripts with residual checks for safe scores in under 1 h.",
                "Practice building and profiling on both NVIDIA CUDA and AMD ROCm.",
            ],
            right_title="Applications, Mystery Drills & Defense",
            right_bullets=[
                "Complete ≥ 2 blind 48-hour mystery drills with Git patch review.",
                "Ship every app with a 1-minute smoke test and full accuracy check.",
                "Rehearse the A0 English poster, 10-minute talk, and 30 Q&A cards.",
                "Audit code for mathematical equivalence and zero dataset hardcoding.",
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
                ["C01", "ASC22 Yuan 4.7B LLM", "GPU cluster · 3 kW", "Dense GEMM + gradient All-Reduce", "M09, M10, M15"],
                ["C02", "ASC22 DeePMD-kit", "CPU/GPU · 3 kW", "Irregular gather + small MLP GEMM", "M02, M07, M09"],
                ["C03", "ASC24 GoMars", "Multi-node CPU · 3 kW", "Lat-lon 3D stencil + polar load skew", "M05, M06, M14"],
                ["C04", "ASC25 AlphaFold3", "Prelim GPU · Finals CPU 4 kW", "O(N³) triangle attention + diffusion", "M05, M08, M11"],
                ["C05", "ASC25 DeepSeek 32B", "CPU-only 4 kW · ≥ 4-bit", "DDR5 BW-bound decode + KV cache", "M02, M04, M11"],
                ["C06", "ASC26 UnifoLM-WMA-0", "Prelim ≥ 16-bit · Finals 5 kW", "UNet diffusion denoising + video I/O", "M07, M08, M11"],
                ["C07", "ASC26 AMSS-NCKU", "CPU+GPU · 5 kW", "9-level AMR 3D stencil + wave extract", "M03, M08, M12"],
                ["C08", "ASC26 QiboTN", "CPU-only 5 kW", "Tensor contraction (vs 16·2ⁿ wall)", "M02, M04, M05"],
                ["C09", "ASC26 LeWorldModel", "AMD W7900D only · 5 kW", "JEPA latent rollouts + CEM planning", "M07, M08, M16"],
                ["C10", "ASC26 ICON (Group)", "CPU-only 5 kW · 8 pts", "Icosahedral climate mesh + MPI halo", "M05, M06, M16"],
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
            problem_meta="40 Layers · 1B Tokens · Loss below 7.0 · PyTorch · 3 kW Finals",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Pretrains a 4.7B Chinese LLM on 100 GB of text as fast as possible while reaching loss below 7.0.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Dense Transformer GEMMs total ~6·Φ·D (~2.82×10¹⁹ FLOPs). Compute-bound on each GPU; limited across GPUs by gradient sync.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M01/M04 (GEMM, Roofline), Stage 3 M09/M10 (16·Φ VRAM, BF16, Ring All-Reduce), Stage 4 M15 (3 kW cap).",
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
            problem_meta="Water / Cu / Al-Cu-Mg · dp test RMSE Gate · 3 kW Finals",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Trains neural atomic potentials with quantum accuracy at classical MD speed for million-atom materials simulation.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Two regimes: neighbor gathers are memory-bound; small MLP networks are compute-bound with force gradients F = -∇E.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M04 (cache, Roofline), Stage 2 M07/M08 (kernel fusion, profiling), Stage 3 M09 (mixed precision).",
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
            problem_meta="Multi-Node CPU · 3 kW Finals · SJTU Application Innovation",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Simulates global Martian winds, dust transport, and heat cycles for landing-site weather and climate study.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "3D stencils on a lat-lon grid. Memory-bandwidth and MPI halo-bound; tight cells near the poles cause load skew.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M03 (blocking, load balance), Stage 2 M05/M06 (SIMD, OpenMP/MPI halo overlap), Stage 4 M14.",
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
            problem_meta="Prelim GPU (≥ 16-bit) · Finals CPU-Only 4 kW · SJTU 30x+",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Predicts 3D atomic structures of proteins, DNA, RNA, and ligands for structural biology and drug discovery.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "O(N³) Triangle Updates and Attention followed by diffusion. Long chains strain memory bandwidth and tensor transposes.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M05/M08 (Xeon AMX/AVX-512, NUMA, profiling), Stage 3 M09/M11 (BF16, graph compilation, fusion).",
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
            problem_meta="CPU-Only 4 kW · ≥ 4-bit Quant · No Pruning · ZJU 14.9 tok/s",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Serves a 32B reasoning LLM fast on a 4 kW CPU-only cluster with zero GPUs.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Decode reads all weights per token (intensity below 2 FLOP/B), pinned to DDR5 bandwidth: tok/s ≤ B_DDR5 / ModelBytes.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M02/M04 (DDR5 Roofline), Stage 2 M05 (AVX-512/AMX, NUMA), Stage 3 M11 (INT4 quantization, KV cache).",
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
            problem_meta="Prelim ≥ 16-bit, PSNR ≥ 25 · Finals 5 kW · PKU 26 s / BUPT 30 s",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Speeds up Unitree's robot world model, which predicts future video from robot actions for faster planning.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Multi-step UNet diffusion mixes compute-bound conv/attention with memory-bound norms, plus cold load and video I/O.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M07/M08 (fused kernels, profiling), Stage 3 M11 (resident serving, TensorRT, TeaCache, async video).",
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
            problem_meta="5 kW · RMS Error below 1% · |v| ≤ 2 · ZJU 30x / THU 0.85 s/step",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Solves Einstein's equations to simulate binary black-hole mergers and gravitational waves like GW150914.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "RK4 3D stencils across 9 nested AMR grids (24 fields/cell), inter-level interpolation, and CPU wave extraction.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M03 (Amdahl), Stage 2 M07/M08 (tiling, streams), Stage 3 M12 (GPU residency, relay, 200-step checks).",
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
            problem_meta="CPU-Only 5 kW (GPU = 0 pts) · QFT / QAOA · Fudan C Rewrite 10x+",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Simulates quantum circuits (QFT, QAOA, random circuits) on classical CPUs and checks expectation values.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Full state vectors need 16·2ⁿ bytes (40 qubits = 16 TiB). Tensor networks bypass that wall, leaving contraction and Python overhead.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 1 M01/M02/M04 (16·2ⁿ wall, cache), Stage 2 M05/M06 (C/C++ rewrite, SIMD, OpenMP, multi-node).",
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
            problem_meta="AMD W7900D Only · 5 kW · 200 Cases · Success ≥ 90% · Top 3 > 100x",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Runs LeWorldModel (JEPA) in latent space to plan 200 PushT robot tasks with ≥ 90% success.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Repeated Encoder-Predictor rollouts in CEM planning. Bottlenecked by tiny kernel launches, CPU-GPU syncs, and video I/O.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M07/M08 (ROCm/HIP, profiling), Stage 3 M11 (BF16, caching, HIP Graphs), Stage 4 M16 (48 h mystery).",
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
            problem_meta="CPU-Only 5 kW · 8 pts · RCE_torus / OMIP / aquaplanet",
            problem_dims=[
                (
                    "1. What the Problem Solves",
                    "Optimizes the ICON global climate model (SC25 Gordon Bell Prize) for coupled weather and ocean simulation.",
                ),
                (
                    "2. Underlying Math & Compute Profile",
                    "Icosahedral mesh removes polar bottlenecks for coupled atmosphere and ocean PDEs. Memory-bandwidth and MPI halo-bound.",
                ),
                (
                    "3. Prerequisites & Roadmap Mapping",
                    "Stage 2 M05/M06/M08 (SIMD, OpenMP, slim halo, MPI), Stage 4 M14/M16 (sparse grids, alliance Git patches).",
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
