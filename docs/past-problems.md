# Past ASC Competition Problems: Technical Analysis (C01 to C10)

This catalog analyzes 10 real ASC competition applications from ASC22 through ASC26. Every entry distinguishes official notices from committee talks, team case studies, and curated historical baselines. Because the ASC27 Committee has not yet released ASC27 application tasks, power caps, hardware specs, or scoring formulas, all historical wattages and point weights below serve strictly as training context.

**Source Labels Used Throughout**
- **ASC22 Preliminary / Final Notification**: official ASC22 committee PDFs.
- **ASC26 Committee Talk**: *ASC26 Competition Optimization & Innovation Introduction* (Liu Yu, ASC Committee, Oct 2026).
- **Tsinghua Talk**: *Bringing Black Holes onto GPUs: ASC26 AMSS-NCKU Experience* (Song Jiaxing, Tsinghua ASC26 team).
- **Historical Curriculum Record**: verified ASC24/ASC25 competition summaries maintained for curriculum continuity where standalone PDF notifications are not bundled in the repository extract.

---

## C01: ASC22 Yuan 4.7B Large Language Model

**Source:** ASC22 Preliminary Round Notification (Section 3, 30 pts) and ASC22 Final Competition Notification (YLLM, 18 pts; 3 kW on-site power limit).

### What the Problem Solves

Teams pretrain a 4.7-billion-parameter Chinese autoregressive Transformer language model (Yuan architecture) on a 100 GB Common Crawl dataset filtered by MDFS. Preliminary parameters are fixed at 40 layers, hidden size $d = 3072$, 24 attention heads, sequence length $n = 2048$, and 1 billion training tokens. PyTorch is mandatory (other deep learning frameworks prohibited; Hugging Face, DeepSpeed, and Megatron-LM encouraged). Final loss must converge below `7.0` or the submission is invalid. Finals changed layer count, hidden size, and heads on site under a strict 3 kW cluster cap.

### Underlying Math & Compute Profile

Training minimizes autoregressive negative log-likelihood across each 2048-token window:

$$\mathrm{Loss} = \sum_{k=1}^{n} -\log P(x_k \mid x_1, \dots, x_{k-1}), \qquad \mathrm{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2,$$

with $W_1 \in \mathbb{R}^{d \times 4d}$ and $W_2 \in \mathbb{R}^{4d \times d}$. Compute scales with token count and dense projection GEMMs ($O(6 \Phi \cdot N_{\mathrm{tokens}})$ FLOPs). Static mixed-precision Adam state for $\Phi = 4.7 \times 10^9$ parameters reaches $\approx 75\ \mathrm{GB}$ before activations, overflowing single-GPU 40 GB A100 memory and forcing model/pipeline/ZeRO parallelism plus collective Ring All-Reduce ($2(p - 1)G / p$ bytes per rank).

### Prerequisites & Roadmap Mapping

- **Stage 3 / M09**: Transformer VRAM budgeting, mixed precision, and convergence gating ($\mathrm{Loss} < 7.0$).
- **Stage 3 / M10**: DP, FSDP/ZeRO, TP, and PP trade-offs over NVLink vs. PCIe/InfiniBand.
- **Stage 1 / M01 & Stage 4 / M16**: mandatory structured logs (hyperparameters, random seed, start/end timestamps, per-iteration loss and elapsed time, TensorBoard traces).

### Visual Suggestion

40-layer Transformer vertical schematic annotated with $d = 3072$, 24 heads, $4d$ FFN, and the 3-part VRAM breakdown (weights, optimizer states, activations) exceeding a single 40 GB GPU (`diagrams/png/c01_asc22_yuan_llm.png`).

### Speaker Notes

- **Hardware & Power Wall**: Prelim recommended multi-GPU NVLink/NVSwitch servers under a 3 kW cluster design budget; on-site finals enforced a hard 3 kW wall-power cap on Inspur NF5280M6 nodes (up to 2x A100-PCIe-40G each).
- **Accuracy & Submission Gates**: Final loss $< 7.0$ is binary; missing `Yuan/Log`, `Yuan/tensorboard`, or `Yuan/model` folders yields 0 points.
- **Primary Bottlenecks**: Single-GPU VRAM overflow, activation footprint at sequence length 2048, and inter-node gradient/activation synchronization.
- **Optimization Strategy**: Combine BF16/FP16 mixed precision, activation checkpointing, ZeRO/FSDP or TP+PP partitioning via DeepSpeed/Megatron-LM, fused attention/LayerNorm kernels, and overlap of backward pass with gradient All-Reduce.

---

## C02: ASC22 DeePMD (Deep Potential Molecular Dynamics)

**Source:** ASC22 Preliminary Round Notification (Section 4, 30 pts) and ASC22 Final Competition Notification (18 pts; 3 kW on-site cap).

### What the Problem Solves

Teams compile and accelerate GPU training of `DeePMD-kit` (official `asc-2022` branch) across three fixed material benchmark systems: Water (`asc-water`), Copper (`asc-copper`), and an Al-Cu-Mg ternary alloy (`asc-mgalcu`). Except for `model/descriptor/precision`, `model/fitting_net/precision`, and `model/descriptor/type_one_side`, no `input.json` training hyperparameters may be altered. Correctness is verified via `dp test -m frozen_model.pb -s data`, requiring consistency with the baseline `asc-2022` branch.

### Underlying Math & Compute Profile

DeePMD maps atomic coordinates, species types, and simulation box geometry to an ab-initio-accurate potential energy surface (PES) $E$ and interatomic forces $\mathbf{F}_i = -\nabla_{\mathbf{r}_i} E$. Each step builds symmetry-preserving local environment descriptors (`se_e2_a` embedding net `[25, 50, 100]` over neighbor lists) followed by a residual fitting MLP (`[240, 240, 240]`). Unlike pure LLM GEMMs, descriptor neighbor construction and gather/scatter operations exhibit irregular memory access and high kernel launch count, while lowering precision from `float64` to mixed precision risks force-error drift.

### Prerequisites & Roadmap Mapping

- **Stage 1 / M01–M02**: FP64 vs. FP32/mixed-precision error propagation and irregular neighbor-list memory locality.
- **Stage 2 / M07–M08**: CUDA kernel fusion and `nsys` timeline inspection to distinguish custom descriptor ops from MLP GEMMs.
- **Stage 3 / M12**: automated `dp test` regression before accepting any kernel or precision modification.

### Visual Suggestion

Three-benchmark pipeline diagram (Water, Cu, Al-Cu-Mg $\to$ `se_e2_a` descriptor + neighbor list $\to$ fitting net $\to$ energy/forces $\to$ `dp test` verification gate) highlighting the three legal JSON knobs (`diagrams/png/c02_asc22_deepmd.png`).

### Speaker Notes

- **Hardware & Power Wall**: Prelim permitted any device capable of running `DeePMD-kit`; finals enforced the 3 kW on-site limit and restricted modifications to parallel/runtime settings on announced workloads.
- **Accuracy Gate**: `dp test` energy and force errors must remain consistent with the reference `asc-2022` branch; modified source code and full `ase_results/{water,cu,alloy}` logs must be archived for audit.
- **Primary Bottlenecks**: Default `float64` overhead on GPUs with lower FP64 throughput, neighbor-list construction latency, small-tensor kernel launches, and host-device synchronization during `dp train`.
- **Optimization Strategy**: Enable legal `type_one_side` and validated mixed precision (`float32`/`float64` hybrid where `dp test` holds), fuse custom TensorFlow/CUDA descriptor operators, optimize neighbor-list sorting, and eliminate unnecessary `disp_freq` or profiling I/O overhead.

---

## C03: ASC24 GoMars (Martian Atmospheric Global Circulation Model)

**Source:** ASC26 Committee Talk (ASC24 frontier application timeline) paired with Historical Curriculum Record for ASC24 finals context (3 kW historical baseline; SJTU Application Innovation). Note: on slide p.26 of the ASC26 Committee Talk, the ASC24 highlight entry cites Peking Univ.'s 3x GPU speedup on WannierTools rather than GoMars; keep those two ASC24 tasks separate in all presentations.

### What the Problem Solves

GoMars simulates global Martian atmospheric dynamics (wind, temperature, dust/mass transport) using a non-hydrostatic dynamical core discretized on a latitude-longitude spherical grid. Finals teams optimize multi-node parallel throughput of time-stepped global atmospheric forecasts under a 3 kW historical cluster cap while preserving numerical physical consistency.

### Underlying Math & Compute Profile

Non-hydrostatic fluid equations update coupled 3D atmospheric state fields via horizontal finite-difference stencils and vertical column physics. On a latitude-longitude grid, physical zonal spacing shrinks as $\Delta x \propto R \cos(\phi)\,\Delta\lambda$ toward the poles, tightening the CFL timestep constraint and creating polar filtering plus severe load imbalance between polar and equatorial MPI ranks. Every timestep exchanges ghost halos across neighbor domains; skewed rank completion times leave faster ranks stalled at MPI barriers, inflating Amdahl's serial fraction $(1 - f)$.

### Prerequisites & Roadmap Mapping

- **Stage 2 / M06**: 2D/3D MPI domain decomposition, non-blocking halo exchange, and Hockney latency/bandwidth tuning.
- **Stage 1 / M03**: Amdahl strong-scaling breakdown when polar ranks create barrier stalls.
- **Stage 2 / M05 & M08**: hybrid MPI+OpenMP core pinning and Score-P rank-imbalance profiling.

### Visual Suggestion

Latitude-longitude sphere highlighting polar grid convergence alongside an MPI rank Gantt trace showing equatorial ranks waiting on overloaded polar ranks (`diagrams/png/c03_asc24_gomars.png`).

### Speaker Notes

- **Hardware & Power Wall**: Historical ASC24 finals operated under a 3 kW cluster cap (non-binding for ASC27).
- **Primary Bottlenecks**: Polar grid clustering causing asymmetric computation/filtering load, frequent small-message halo exchanges, and memory-bandwidth-bound 3D stencils.
- **Winning Team Approach**: Shanghai Jiao Tong University earned the Application Innovation award on GoMars by targeting domain load balancing, halo communication overlap, and hybrid CPU/MPI layout optimization.
- **Curriculum Lesson**: Contrast GoMars's latitude-longitude pole singularity directly against ICON's uniform icosahedral grid in C10 to illustrate how discretization geometry dictates parallel scalability.

---

## C04: ASC25 AlphaFold3 (Biomolecular Structure Prediction)

**Source:** ASC26 Committee Talk (p.6 Nobel-level applications & p.26 achievement highlight: SJTU 30x+ CPU inference speedup in ASC25) paired with Historical Curriculum Record (prelim CPU/GPU BF16 $\ge 16$-bit; finals CPU-only 4 kW, $\ge 3$ nodes, $\le 2$ kW/node; SJTU e Prize).

### What the Problem Solves

AlphaFold3 predicts 3D structures of proteins and biomolecular complexes from sequence inputs. Preliminary rounds permitted CPU or GPU inference with precision at least 16-bit (BF16 floor). Finals removed GPUs completely, enforcing a CPU-only 4 kW cluster cap across at least 3 nodes ($\le 2$ kW per node) to test pure CPU algorithmic, memory, and vector engineering on modern AI-for-Science workloads.

### Underlying Math & Compute Profile

AlphaFold3 combines Pairformer blocks (triangle multiplicative updates and triangle self-attention scaling up to $O(N_{\mathrm{res}}^3)$ FLOPs and $O(N_{\mathrm{res}}^2)$ pair-representation memory) with a diffusion-based atomic coordinate module. On CPU-only clusters, dense tensor contractions compete for DRAM bandwidth and L2/L3 cache capacity while sparse/masked padding wastes cycles if computed naively. Dropping below 16-bit precision breaks structural accuracy tolerances, making BF16/FP32 vector math (AVX-512/AMX), cache blocking, and multi-node task scheduling decisive.

### Prerequisites & Roadmap Mapping

- **Stage 2 / M05**: CPU SIMD vectorization (AVX-512 / BF16 instructions), OpenMP scheduling, and NUMA first-touch placement.
- **Stage 1 / M04**: Roofline separation between compute-bound triangle GEMMs and bandwidth-bound elementwise/attention ops.
- **Stage 3 / M09**: intermediate activation memory budgeting and 16-bit precision floor compliance.

### Visual Suggestion

Two-regime panel contrasting Prelim (CPU/GPU, BF16 $\ge 16$-bit) with Finals (CPU-only, 4 kW, $\ge 3$ nodes, $\le 2$ kW/node) plus the 30x+ CPU inference speedup bar for SJTU (`diagrams/png/c04_asc25_alphafold3.png`).

### Speaker Notes

- **Hardware & Power Wall**: Historical ASC25 finals enforced CPU-only execution under a 4 kW cluster budget with $\ge 3$ nodes and $\le 2$ kW per node (non-binding for ASC27).
- **Accuracy Gate**: Precision locked at $\ge 16$-bit (BF16 minimum) in prelims; structural predictions must pass official accuracy verification.
- **Primary Bottlenecks**: Cubic triangle attention cost, massive intermediate pair tensors thrashing LLC/NUMA channels, and Python/framework dispatch overhead on multi-socket CPUs.
- **Winning Team Approach**: Shanghai Jiao Tong University achieved over 30x CPU inference speedup (earning the e Prize) through deep CPU kernel optimization, vector/BLAS tuning, memory layout restructuring, and balanced multi-node CPU parallelism.

---

## C05: ASC25 DeepSeek R1-Distill 32B (CPU-Only LLM Inference)

**Source:** Historical Curriculum Record for ASC25 finals (CPU-only 4 kW; $\ge 4$-bit quantization allowed; no pruning; no cross-run KV cache reuse; Zhejiang Univ. 14.9 tok/s single-thread). Note: the ASC26 Committee Talk mentions LLM tasks spanning ASC22–25 without printing R1-Distill specifics; cite this entry as a curated ASC25 historical baseline.

### What the Problem Solves

Teams optimize inference throughput of the 32-billion-parameter reasoning model DeepSeek R1-Distill 32B on a CPU-only cluster capped at 4 kW. Rules allow weight quantization down to 4-bit ($\ge 4$-bit), strictly forbid structural pruning, and forbid reusing KV cache across independent runs.

### Underlying Math & Compute Profile

Even at 4-bit quantization ($\approx 0.5$ bytes/param plus group scales), 32B weights occupy $\approx 16$ to $18\ \mathrm{GiB}$. Autoregressive decoding streams this entire quantized weight footprint plus growing KV cache $M_{\mathrm{KV}} = 2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$ from host DRAM every generated token:

$$\mathrm{TPOT} \approx \frac{M_{\mathrm{weights,quant}} + M_{\mathrm{KV}}}{B_{\mathrm{DRAM,eff}}} + \alpha_{\mathrm{dequant}}.$$

Decode sits deep inside the memory-bandwidth regime ($I \approx 1$ FLOP/byte), where dequantization overhead, NUMA traffic, and cache-unfriendly weight packing dictate tokens per second.

### Prerequisites & Roadmap Mapping

- **Stage 3 / M11**: prefill vs. decode split, KV cache scaling, and streaming bandwidth bounds.
- **Stage 3 / M09**: quantized bit-width accounting ($\ge 4$-bit legal floor vs. banned pruning).
- **Stage 2 / M05**: CPU SIMD fused dequant-dot-product kernels, NUMA weight sharding, and core pinning.

### Visual Suggestion

Decode-step dataflow diagram showing 4-bit weight streaming ($\approx 16$ to 18 GiB) + growing KV cache passing through CPU memory channels into fused SIMD dequant-GEMV kernels, with rule callouts ($\ge 4$-bit allowed, no pruning, no cross-run KV reuse; ZJU 14.9 tok/s single-thread) (`diagrams/png/c05_asc25_deepseek_r1.png`).

### Speaker Notes

- **Hardware & Power Wall**: CPU-only execution behind the historical ASC25 4 kW cluster cap (non-binding for ASC27).
- **Compliance Rules**: Quantization $\ge 4$-bit permitted; model pruning prohibited; cross-run KV cache reuse prohibited so every evaluation builds fresh context.
- **Primary Bottlenecks**: DRAM memory bandwidth streaming 32B weights per token, on-the-fly integer-to-float unpacking overhead, and multi-socket NUMA contention.
- **Winning Team Approach**: Zhejiang University reached 14.9 tok/s in single-thread inference by pairing compact legal quantization layouts with cache-friendly fused SIMD GEMV kernels and low-overhead runtime scheduling.

---

## C06: ASC26 UnifoLM-WMA-0 (Embodied World Model)

**Source:** ASC26 Committee Talk (Task 2/6, slides pp.12–15; ASC26 prelim 30 pts, finals 18 pts, 5 kW cluster cap).

### What the Problem Solves

Teams accelerate inference for Unitree's embodied world model `UnifoLM-WMA-0`, a neural simulator that generates physically plausible video rollouts for robot action planning. Prelim tested 5 scenes $\times$ 4 cases = 20 samples under a strict $\ge 16$-bit weight constraint and hard video quality floor $\mathrm{PSNR} \ge 25\ \mathrm{dB}$ (any single failing case zeroes the entire scene). Finals tested 6 cases and unlocked weight precision, diffusion samplers, and step counts while preserving $\mathrm{PSNR} \ge 25\ \mathrm{dB}$.

### Underlying Math & Compute Profile

End-to-end runtime decomposes into model load/init, iterative UNet/Transformer diffusion denoising across $N_{\mathrm{steps}}$, VAE decoding, and video I/O encoding:

$$T_{\mathrm{case}} = T_{\mathrm{init}} + N_{\mathrm{steps}} \cdot T_{\mathrm{denoise}} + T_{\mathrm{decode}} + T_{\mathrm{encode}}.$$

Eliminating per-case reload via resident serving drives $T_{\mathrm{init}} \to 0$. Fusing GroupNorm, GELU/GEGLU, LayerNorm, and GEMM+bias+activation shrinks memory traffic (Qilu Univ. of Tech. compressed traffic from $8MN$ down to $4MN$ bytes), while adaptive step caching (TeaCache) computes latent $\ell_1$ distance across iterations to skip redundant UNet passes without breaching $\mathrm{PSNR} \ge 25\ \mathrm{dB}$.

### Prerequisites & Roadmap Mapping

- **Stage 3 / M11**: diffusion denoising step reduction, TeaCache latent gating, and async I/O pipelines.
- **Stage 2 / M07**: custom CUDA/TileLang operator fusion and TensorRT graph compilation.
- **Stage 3 / M09**: strict prelim $\ge 16$-bit precision gate vs. unlocked finals precision/sampler trade-offs.

### Visual Suggestion

Prelim vs. Finals optimization waterfall displaying Qilu Univ. of Tech. (5.41x single GPU, 8.13x multi-GPU), Shanghai Univ. (8.22x dual-GPU end-to-end; 14.53x single-step denoise), and Finals leaders PKU (26 s/case) and BUPT (30 s/case, >20x vs. baseline) (`diagrams/png/c06_asc26_unifolm_wma.png`).

### Speaker Notes

- **Hardware & Power Wall**: ASC26 finals operated within the 5 kW cluster cap ($\le 2$ kW/node, $\ge 3$ nodes, $\le 2$ GPUs/server).
- **Accuracy Gate**: $\mathrm{PSNR} \ge 25\ \mathrm{dB}$ on every case; prelim additionally required $\ge 16$-bit weights.
- **Primary Bottlenecks**: Repeated per-request model loading and CUDA context init, heavy UNet/Attention denoising steps, un-fused normalization/activation memory traffic, and synchronous video disk writes.
- **Winning Team Approaches**:
  - *Qilu Univ. of Tech. (Prelim ASC1534)*: 5.41x single-GPU / 8.13x multi-GPU via TileLang/CUDA fused NHWC kernels ($8MN \to 4MN$ bytes), resident server process, RAMDisk (`tmpfs`) + async FFmpeg streaming, selective FP16/BF16, and hybrid data/model parallelism.
  - *Shanghai Univ. (Prelim ASC1623)*: 8.22x dual-GPU end-to-end (14.53x single-step denoise) via TensorRT ONNX compilation (8.40x single step), UNet-adapted TeaCache with $\ell_1$ logistic gating (1.36x extra), and ParaStep-Adaptive speculative dual-GPU step overlap (PSNR 39.8 $\to$ 36.9 dB, far above 25 dB).
  - *PKU (26 s/case) & BUPT (30 s/case) in Finals*: >20x end-to-end speedup (from ~13 min to under 30 s) via compact functional inference stacks, `/preload`–`/warmup`–`/run` serving, decoupled action/video sampling steps, TeaCache, and async streaming video output.

---

## C07: ASC26 AMSS-NCKU (Numerical Relativity Binary Black Hole Merger)

**Source:** ASC26 Committee Talk (Task 3/6, slides pp.16–19; 18 pts, 5 kW finals cap) and Tsinghua Talk (Song Jiaxing, slides pp.2–32).

### What the Problem Solves

AMSS-NCKU solves Einstein's field equations numerically on 9-level nested Adaptive Mesh Refinement (AMR) grids to simulate black hole inspiral, merger, and ringdown gravitational waves. Finals evaluated three scientific cases: GW150914 inspiral (4 pts), equal-mass Bowen-York three-black-hole collision (5 pts), and full binary merger waveform generation (9 pts). Correctness gates require black hole trajectory $\mathrm{RMS} < 1\%$, ADM constraint violation $< 2$, and mathematically equivalent algorithms.

### Underlying Math & Compute Profile

TwoPunctures solves elliptic initial data, followed by hyperbolic RK4 time evolution (4 RHS evaluations per step) over 24 coupled field variables per grid point using 3D stencils ($\pm 2$ neighbors per axis) across 9 refinement levels where level 8 sub-cycles 32 fine steps per coarse step. Profiling exposes three sequential bottlenecks: (1) thousands of FLOPs per grid point in RHS (`compute`), (2) 122 host-device pack/copy/unpack roundtrips plus 65 coarse-fine interpolations per coarse step (`transfer`), and (3) spherical-surface gravitational-wave interpolation and integration on CPU (`analysis backpressure`).

### Prerequisites & Roadmap Mapping

- **Stage 3 / M12**: flagship case study for bottleneck migration (compute $\to$ transfer $\to$ analysis) and 200-step stale-copy regression.
- **Stage 1 / M03–M04**: Amdahl wall-time fraction (1.47x RHS gave 1.22x full step when RHS was ~20%) and register-level stencil reuse.
- **Stage 2 / M07–M08**: GPU-resident memory pools, kernel fusion/fission, shared-memory 3D halo tiling, and pinned async relay pipelines.

### Visual Suggestion

Five-stage timing drop from Song Jiaxing's Tsinghua preparation benchmark (CPU ~4.5 s $\to$ GPU v1 4.7 s $\to$ GPU-resident 1.4 s $\to$ 2+62 core split 1.0 s $\to$ 3-stage relay 0.85 s) beside Zhejiang Univ. (44,425 s $\to$ 2,376 s, 18.6x prelim $\to$ 30x finals) and PKU (5.50x, RMS $1.9 \times 10^{-9}$) (`diagrams/png/c07_asc26_amss_ncku.png`).

### Speaker Notes

- **Hardware & Power Wall**: Finals operated under the 5 kW cluster cap. Tsinghua prepared on 4x H100 without NVLink + 256-core AMD EPYC 9755 and deliberately ran all grids on 1 H100 because inter-level AMR interpolation across PCIe outweighed multi-GPU gains.
- **Accuracy Gate**: Trajectory $\mathrm{RMS} < 1\%$ and ADM constraint violation $< 2$. Stale host/device copies looked normal at 50 steps yet grew >60x worse by 200 steps; explicit array validity flags restored $10^{-8}$ agreement.
- **Winning Team Approaches**:
  - *Tsinghua (Runner-Up overall; prep progression)*: point-wise C++ RHS keeping 60+ temporary grids in registers (1500 $\to$ 600 LOC); moved all 65 interpolations, boundary sync, black-hole tracking, and regridding onto GPU across 150+ verified commits (4.7 s $\to$ 1.4 s); split 64 host cores into 2 GPU-driver + 62 OpenMP waveform-extraction threads (1.0 s); added 3-stage snapshot/D2H/relay ring buffers (0.85 s).
  - *UESTC (Prelim ASC1599)*: OpenMP task-based `data_packer`, GPU `enforce_ga` + RK4 fusion, device memory pool eliminating repeated `cudaMalloc`/`cudaFree`, pinned async transfers, and `cudaMemPrefetchAsync`.
  - *Zhejiang Univ. (Prelim ASC1514 $\to$ Finals)*: 44,425 s (32-MPI CPU) $\to$ 2,376 s (1 GPU) = 18.6x in prelim, reaching 30x in finals via multi-stream pipelines, ghost-zone-only PCIe sync, kernel fission + `__launch_bounds__` register/occupancy tuning, 3D shared-memory halo tiling, and AI-assisted Fortran/C++-to-CUDA porting.
  - *PKU (Prelim ASC1484, 2nd on task in finals)*: 5.50x amortized speedup with trajectory RMS $1.9 \times 10^{-9}$ and 5.46x OpenMP speedup on TwoPunctures (468.75 s $\to$ 85.88 s on 64 cores).

---

## C08: ASC26 QiboTN (CPU-Only Quantum Circuit Tensor-Network Simulation)

**Source:** ASC26 Committee Talk (Task 4/6, slides pp.20–21; 18 pts, CPU-only, 5 kW finals cap).

### What the Problem Solves

QiboTN simulates large quantum circuits via tensor-network contraction (Matrix Product States and optimized contraction paths over backends such as Quimb) across three workloads: Quantum Fourier Transform (QFT), QAOA variational optimization, and random Supremacy circuits. Correctness checks mean expectation values; ranking uses total wall-clock time. **Using any GPU yields 0 points.**

### Underlying Math & Compute Profile

Direct state-vector simulation stores $2^n$ complex amplitudes in `complex128` (16 bytes each):

$$M(n) = 16 \cdot 2^{n}\ \text{bytes} \implies M(20) = 16\ \mathrm{MiB}, \quad M(40) = 16\ \mathrm{TiB}.$$

**Verified Unit Correction:** Slide p.20 of the ASC26 Committee Talk misprints 20 qubits as `16 GB` and 40 qubits as `16 PB`, a $1024\times$ ($2^{10}$) unit error substituting GB/PB for MiB/TiB. Exact binary values are **16 MiB** (20 qubits) and **16 TiB** (40 qubits). Tensor-network contraction shifts complexity from exponential $2^n$ state vectors to contraction-path treewidth, turning Python interpreter overhead, tensor transpose/layout, and BLAS/memory allocation into the dominant CPU bottlenecks.

### Prerequisites & Roadmap Mapping

- **Stage 1 / M02**: exponential state-vector memory wall ($16 \cdot 2^n$ bytes) and cache-aware tensor layouts.
- **Stage 2 / M05**: CPU-only SIMD, OpenMP, compiled C/C++ kernels, and NUMA memory management.
- **Stage 4 / M16**: expectation-value verification gates during aggressive language-level rewrites.

### Visual Suggestion

Log-scale memory-wall curve $M(n) = 16 \cdot 2^n$ bytes highlighting the explicit unit correction callout (20q = 16 MiB, 40q = 16 TiB vs. p.20 misprint) alongside Fudan's Python-to-C rewrite pipeline (`diagrams/png/c08_asc26_qibotn.png`).

### Speaker Notes

- **Hardware & Power Wall**: Strictly CPU-only inside the 5 kW ASC26 finals cluster limit; any GPU offload triggers automatic 0 points.
- **Accuracy Gate**: Mean expectation values must pass committee verification across QFT, QAOA, and Supremacy workloads.
- **Primary Bottlenecks**: Python interpreter dispatch overhead in original QiboTN/Quimb glue code, repeated temporary tensor allocations, suboptimal contraction ordering, and un-pinned CPU BLAS threads.
- **Winning Team Approach**: Fudan University ported the core tensor-network simulation algorithms completely from Python into native C with compiler optimization and custom memory management, delivering tens-of-times speedup while maintaining exact simulation correctness.

---

## C09: ASC26 Mystery Application: LeWorldModel (JEPA on AMD W7900D)

**Source:** ASC26 Committee Talk (Task 5/6, slides pp.22–23; 18 pts, 5 kW finals cap, AMD W7900D platform).

### What the Problem Solves

Revealed on site as the ASC26 Mystery Application, `LeWorldModel` (LeWM) is a Joint Embedding Predictive Architecture (JEPA) world model from Yann LeCun's team that predicts dynamics in compact latent space rather than pixel space. Teams run 200 `PushT` planning and video-generation cases strictly on sponsored **AMD W7900D** GPUs (ROCm ecosystem), minimizing total wall-clock time while maintaining task **success rate $\ge 90\%$**.

### Underlying Math & Compute Profile

Each `PushT` episode alternates between JEPA Encoder–Predictor latent forward passes and Cross-Entropy Method (CEM) trajectory optimization (sampling candidate action sequences, rolling out latent predictions, scoring costs, and iterating). Total work scales linearly with active episodes $\times$ CEM iterations $\times$ candidate population size. Small batch sizes and iterative loops leave GPU kernels launch-bound while video encoding stalls host CPU cores; switching to AMD W7900D requires ROCm/HIP compatibility rather than NVIDIA-only TensorRT tooling.

### Prerequisites & Roadmap Mapping

- **Stage 3 / M11**: world-model inference acceleration, latent feature caching, and accuracy-gated planning pruning.
- **Stage 2 / M05 & M08**: NUMA-bound environment worker pools, multi-node slicing, and HIP/CUDA graph capture to cut launch overhead.
- **Stage 4 / M16**: rapid 48-hour mystery-app profiling on unfamiliar accelerator hardware (ROCm).

### Visual Suggestion

JEPA Encoder–Predictor + CEM planning loop diagram paired with the top-3 finals wall-time bars over 200 PushT cases (BUPT 14 s, Tsinghua 16 s, PKU 17 s, all exceeding 100x speedup at $\ge 90\%$ success rate on AMD W7900D) (`diagrams/png/c09_asc26_leworldmodel.png`).

### Speaker Notes

- **Hardware & Power Wall**: Mandatory AMD W7900D execution under the 5 kW ASC26 finals cluster limit; NVIDIA-only software stacks cannot substitute.
- **Accuracy Gate**: Task success rate $\ge 90\%$ across all 200 PushT cases; overly aggressive CEM truncation breaks physical intuition and invalidates speedups.
- **Primary Bottlenecks**: Redundant CEM candidate rollouts on already-solved episodes, Python/ROCm kernel launch latency, host-device synchronization, and synchronous video rendering.
- **Winning Team Approaches (all >100x speedup)**:
  - *BUPT (14 s)*: dual-node multi-process slicing, tuned CEM iterations and candidate count, BF16 mixed precision + initial/goal feature caching, and early masking/termination of already-succeeded episodes.
  - *Tsinghua (16 s)*: NUMA-bound environment worker pool, sample-level distributed CEM + tensor caching, compute-graph capture/replay removing launch overhead, and asynchronous overlapped video encoding.
  - *PKU (17 s)*: client/server multi-node multi-GPU architecture, BF16 + feature caching + dynamic compilation of hot cost tensors, zero-redundancy tensor conversion eliminating CPU-GPU sync, and tuned CEM hyperparameters.

---

## C10: ASC26 Group Competition: ICON (Global Climate Model)

**Source:** ASC26 Committee Talk (Task 6/6, slides pp.8–9 & 24–25; 8 pts toward finals total, CPU-only, 5 kW cluster cap).

### What the Problem Solves

The ASC26 Group Competition brought the SC25 Gordon Bell Prize-winning ICON Earth-system model (developed by the Max Planck Institute for Meteorology) directly onto student clusters. Cross-university alliances of 5 teams (including international teams, assigned in March and given the task 5 days pre-finals) optimized three coupled climate benchmarks (`RCE_torus` 24-day idealized atmosphere, `OMIP` 20-year ocean + sea ice, and `aquaplanet` 2-month coupled ocean) under a strict **CPU-only** and **5 kW** limit. Alliances share optimization patches collaboratively, while each team executes independently on its own cluster.

### Underlying Math & Compute Profile

ICON discretizes non-hydrostatic atmospheric, oceanic, land, and sea-ice PDEs on a globally uniform **icosahedral** spherical mesh, eliminating the polar grid singularities of latitude-longitude models like GoMars (C03). Each timestep couples component fluxes across irregular triangular/hexagonal cell neighborhoods. Under the CPU-only mandate, performance hinges on inner-loop SIMD vectorization, compact halo domain exchanges, OpenMP scheduling, removing redundant computational kernels, and cutting MPI synchronization overhead.

### Prerequisites & Roadmap Mapping

- **Stage 2 / M05–M06**: explicit SIMD inner loops, OpenMP scheduling, halo-exchange reduction, and MPI synchronization tuning.
- **Stage 1 / M03**: multi-component coupling load balance and strong-scaling ceilings.
- **Stage 4 / M16**: cross-university git patch sharing combined with independent per-cluster reproducibility.

### Visual Suggestion

Uniform icosahedral global mesh contrasted against latitude-longitude polar convergence, paired with the winning alliance workflow (shared optimization patch $\to$ 5 independent CPU-only $\le 5$ kW cluster runs for QHU + SJTU + BUAA + BNU + EAFIT) (`diagrams/png/c10_asc26_icon_group.png`).

### Speaker Notes

- **Hardware & Power Wall**: Strictly CPU-only (using GPUs yields 0 points) within the 5 kW ASC26 finals cluster cap; group competition counted 8 points toward the 100-point finals total (ASC27 group scoring weight TBD).
- **Collaboration Rule**: Teams inside each randomly drawn 5-team group share source code, build recipes, and debugging findings, yet every team must execute all workloads independently on its own cluster (remote operation by partner teams is prohibited).
- **Primary Bottlenecks**: Multi-sphere coupling data movement, oversized halo exchanges, redundant kernel sweeps, unvectorized inner loops, and MPI barrier latency.
- **Winning Alliance Approach (Qinghai Univ. + SJTU + BUAA + BNU + EAFIT Colombia)**: Led jointly in code integration with SJTU, the winning group combined OpenMP thread scheduling tuning, streamlined halo domain exchanges, removal of redundant kernels, explicit inner-loop SIMD compiler directives, and ~5% MPI communication/synchronization gain verified for correctness.

---

## Citation Guardrails for ASC27 Proposals

| Permitted in ASC27 Proposals | Prohibited in ASC27 Proposals |
| --- | --- |
| Official ASC27 rules directly from *2027 ASC Call for Participation* (dates, 5 undergrads + 1 advisor, max 1 finalist/university, midnight UTC+8, HPL/HPCG/apps/poster scope) | Claiming 3 kW, 4 kW, 5 kW, node caps, or ASC22/26 point splits as official ASC27 rules before committee publication |
| Historical ASC22–26 benchmarks and team results explicitly labeled by year and source tier | Conflating ASC24 GoMars with ASC24 WannierTools, or copying slide p.20's erroneous `16 GB / 16 PB` qubit memory labels |
| Exact state-vector scaling $16 \cdot 2^n$ bytes (20q = 16 MiB, 40q = 16 TiB) with transparent note on the $2^{10}$ correction | Silently reusing unverified external numbers without raw team logs or explicit source attribution |
