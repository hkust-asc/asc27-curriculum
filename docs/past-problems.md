# Past ASC Competition Problems (C01 to C10)

This catalog breaks down 10 real ASC applications from ASC22 through ASC26. Each entry lists its source, math profile, roadmap link, and winning team methods.

**Sources**
- **ASC22 Notices**: Official ASC22 preliminary and final PDFs.
- **ASC26 Committee Talk**: *ASC26 Optimization and Innovation Introduction* (Liu Yu, Oct 2026).
- **Tsinghua Talk**: *Bringing Black Holes onto GPUs* (Song Jiaxing, Tsinghua ASC26 team).
- **Curriculum Record**: Verified ASC24 and ASC25 competition summaries.

---

## C01: ASC22 Yuan 4.7B Large Language Model

**Source:** ASC22 Preliminary Notification (30 pts) and Final Notification (18 pts, 3 kW cap).

### What It Does

Teams pretrain a 4.7B-parameter Chinese Transformer (Yuan) on 100 GB of Common Crawl text. Preliminary config is 40 layers, hidden size $d = 3072$, 24 heads, sequence length $n = 2048$, and 1B tokens in PyTorch. Final loss must fall below `7.0`.

### Math and Bottlenecks

Training minimizes autoregressive negative log-likelihood across 2048-token windows:

$$\mathrm{Loss} = \sum_{k=1}^{n} -\log P(x_k \mid x_1, \dots, x_{k-1}), \qquad \mathrm{FFN}(x) = \max(0, x W_1 + b_1) W_2 + b_2.$$

Compute scales as $O(6 \Phi \cdot N_{\mathrm{tokens}})$ FLOPs. Mixed-precision Adam static state for $\Phi = 4.7 \times 10^9$ takes about 75 GB before activations. That overflows one 40 GB A100 GPU and requires ZeRO/FSDP, tensor, or pipeline parallelism plus Ring All-Reduce ($2(p-1)G/p$ bytes per GPU).

### Roadmap Links

- **Stage 3 / M09**: Transformer VRAM budgeting, mixed precision, and loss $< 7.0$ checks.
- **Stage 3 / M10**: DDP, FSDP/ZeRO, TP, and PP over NVLink or PCIe/InfiniBand.
- **Stage 1 / M01 and Stage 4 / M16**: Structured training logs (seed, timestamps, per-step loss, TensorBoard).

### Visual

40-layer Transformer diagram with $d = 3072$, 24 heads, and a 3-part VRAM bar showing overflow past 40 GB (`diagrams/png/c01_asc22_yuan_llm.png`).

### Notes

- **Hardware (ASC22):** Inspur NF5280M6 nodes (up to 2x A100-PCIe-40G each) behind a 3 kW cluster cap.
- **Pass rules:** Loss $< 7.0$; missing `Yuan/Log`, `Yuan/tensorboard`, or `Yuan/model` folders score 0.
- **Winning methods:** BF16/FP16 mixed precision, activation checkpointing, DeepSpeed/Megatron-LM sharding, fused LayerNorm/attention kernels, and backward-pass communication overlap.

---

## C02: ASC22 DeePMD (Deep Potential Molecular Dynamics)

**Source:** ASC22 Preliminary Notification (30 pts) and Final Notification (18 pts, 3 kW cap).

### What It Does

Teams accelerate GPU training of `DeePMD-kit` (`asc-2022` branch) on three materials: Water, Copper, and Al-Cu-Mg alloy. Only three `input.json` keys may change: `descriptor/precision`, `fitting_net/precision`, and `type_one_side`. Outputs must pass `dp test -m frozen_model.pb -s data`.

### Math and Bottlenecks

DeePMD predicts potential energy $E$ and interatomic forces $\mathbf{F}_i = -\nabla_{\mathbf{r}_i} E$ from atomic coordinates. It builds local neighbor descriptors (`se_e2_a` net `[25, 50, 100]`) and feeds them into a residual MLP (`[240, 240, 240]`). Neighbor-list gather/scatter ops cause irregular memory access and many small kernel launches. Dropping `float64` too aggressively drifts force accuracy.

### Roadmap Links

- **Stage 1 / M01–M02**: FP64 vs. FP32 error growth and irregular memory locality.
- **Stage 2 / M07–M08**: CUDA kernel fusion and `nsys` timeline inspection.
- **Stage 3 / M12**: Automated `dp test` checks before keeping any kernel edit.

### Visual

Three-material pipeline (Water, Cu, Al-Cu-Mg $\to$ `se_e2_a` descriptor $\to$ fitting net $\to$ `dp test`) showing the three legal JSON flags (`diagrams/png/c02_asc22_deepmd.png`).

### Notes

- **Hardware (ASC22):** 3 kW on-site cap.
- **Bottlenecks:** Default `float64` cost, neighbor-list build latency, small kernel launches, and host-device syncs.
- **Winning methods:** Enable `type_one_side`, use verified mixed precision where `dp test` passes, fuse custom CUDA descriptor ops, and lower logging I/O frequency.

---

## C03: ASC24 GoMars (Martian Atmospheric Model)

**Source:** ASC26 Committee Talk and Curriculum Record (ASC24 finals, 3 kW cap; SJTU Application Innovation). *Note:* ASC24 also had WannierTools (Peking Univ. 3x GPU speedup); keep the two tasks separate.

### What It Does

GoMars simulates Martian wind, temperature, and dust transport on a latitude-longitude global grid. Finals teams scale multi-node time-stepping throughput under a 3 kW cluster cap.

### Math and Bottlenecks

Coupled 3D fluid PDEs run horizontal stencils and vertical column physics. On a latitude-longitude grid, east-west spacing shrinks as $\Delta x \propto R \cos(\phi)\,\Delta\lambda$ near the poles. Polar filtering and tighter CFL limits overload polar MPI ranks, leaving equatorial ranks idle at barriers and raising Amdahl's serial fraction $(1 - f)$.

### Roadmap Links

- **Stage 2 / M06**: 2D/3D MPI domain split and non-blocking halo exchange.
- **Stage 1 / M03**: Amdahl strong-scaling loss from barrier wait.
- **Stage 2 / M05 and M08**: Hybrid MPI+OpenMP pinning and Score-P rank traces.

### Visual

Latitude-longitude sphere with polar grid bunching beside an MPI Gantt trace showing equatorial wait gaps (`diagrams/png/c03_asc24_gomars.png`).

### Notes

- **Bottlenecks:** Polar load imbalance, small-message halo exchanges, and memory-bound 3D stencils.
- **Winning method:** Shanghai Jiao Tong University won Application Innovation through load balancing, halo overlap, and hybrid MPI+OpenMP layout tuning.
- **Compare with C10:** ICON replaces latitude-longitude grids with a uniform icosahedral mesh to remove polar bottlenecks.

---

## C04: ASC25 AlphaFold3 (Biomolecular Structure Prediction)

**Source:** ASC26 Committee Talk (p.6, p.26: SJTU 30x+ CPU speedup) and Curriculum Record (finals CPU-only 4 kW, $\ge 3$ nodes, $\le 2$ kW/node; SJTU e Prize).

### What It Does

AlphaFold3 predicts 3D structures of proteins and biomolecular complexes. Prelims allowed CPU or GPU at $\ge 16$-bit (BF16 floor). Finals ran CPU-only under a 4 kW cluster cap across at least 3 nodes.

### Math and Bottlenecks

Pairformer blocks run triangle updates and triangle attention costing up to $O(N_{\mathrm{res}}^3)$ FLOPs and $O(N_{\mathrm{res}}^2)$ pair memory, followed by a diffusion coordinate head. On CPUs, large pair tensors spill past L3 cache and contend for DRAM channels. Precision stays at BF16/FP32, making AVX-512/AMX math, cache blocking, and multi-node scheduling essential.

### Roadmap Links

- **Stage 2 / M05**: AVX-512/BF16 SIMD, OpenMP scheduling, and NUMA first-touch.
- **Stage 1 / M04**: Roofline split between compute-bound GEMMs and bandwidth-bound attention ops.
- **Stage 3 / M09**: Activation memory budgeting and 16-bit precision compliance.

### Visual

Prelim (CPU/GPU, BF16) vs. Finals (CPU-only, 4 kW, $\ge 3$ nodes) comparison with SJTU's 30x+ speedup bar (`diagrams/png/c04_asc25_alphafold3.png`).

### Notes

- **Bottlenecks:** Cubic triangle attention, LLC/NUMA thrashing on pair tensors, and Python dispatch overhead.
- **Winning method:** Shanghai Jiao Tong University reached over 30x CPU speedup (e Prize) using custom CPU kernels, BLAS/vector tuning, memory layout changes, and balanced multi-node execution.

---

## C05: ASC25 DeepSeek R1-Distill 32B (CPU-Only LLM Inference)

**Source:** Curriculum Record for ASC25 finals (CPU-only 4 kW; $\ge 4$-bit quantization allowed; no pruning; no cross-run KV reuse; Zhejiang Univ. 14.9 tok/s single-thread).

### What It Does

Teams speed up inference of DeepSeek R1-Distill 32B on a CPU-only 4 kW cluster. Rules allow $\ge 4$-bit weight quantization, ban structural pruning, and ban reusing KV cache across runs.

### Math and Bottlenecks

At 4-bit quantization, 32B weights occupy 16 to 18 GiB. Each decode token streams all weights plus KV cache $M_{\mathrm{KV}} = 2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$ from host DRAM:

$$\mathrm{TPOT} \approx \frac{M_{\mathrm{weights,quant}} + M_{\mathrm{KV}}}{B_{\mathrm{DRAM,eff}}} + \alpha_{\mathrm{dequant}}.$$

Decode sits at $I \approx 1$ FLOP/byte on the memory-bandwidth slope. Unpacking 4-bit integers, NUMA traffic, and weight layout decide token rate.

### Roadmap Links

- **Stage 3 / M11**: Prefill vs. decode split, KV cache growth, and DRAM streaming bounds.
- **Stage 3 / M09**: Quantized bit-width accounting ($\ge 4$-bit floor).
- **Stage 2 / M05**: Fused SIMD dequant-GEMV kernels and NUMA weight sharding.

### Visual

Decode dataflow showing 4-bit weights (16 to 18 GiB) and KV cache streaming into fused SIMD GEMV kernels, noting ZJU's 14.9 tok/s single-thread result (`diagrams/png/c05_asc25_deepseek_r1.png`).

### Notes

- **Bottlenecks:** DRAM bandwidth streaming 32B weights per token, integer unpacking cost, and NUMA contention.
- **Winning method:** Zhejiang University reached 14.9 tok/s single-thread by pairing compact 4-bit layouts with cache-friendly fused SIMD GEMV kernels.

---

## C06: ASC26 UnifoLM-WMA-0 (Embodied World Model)

**Source:** ASC26 Committee Talk (pp.12–15; prelim 30 pts, finals 18 pts, 5 kW cap).

### What It Does

`UnifoLM-WMA-0` generates robot action video rollouts. Prelims tested 20 samples (5 scenes $\times$ 4 cases) with $\ge 16$-bit weights and $\mathrm{PSNR} \ge 25\ \mathrm{dB}$ (one failed case zeroes the scene). Finals tested 6 cases and unlocked precision, samplers, and step counts while keeping $\mathrm{PSNR} \ge 25\ \mathrm{dB}$.

### Math and Bottlenecks

Case runtime splits into load, diffusion denoising, VAE decode, and video encoding:

$$T_{\mathrm{case}} = T_{\mathrm{init}} + N_{\mathrm{steps}} \cdot T_{\mathrm{denoise}} + T_{\mathrm{decode}} + T_{\mathrm{encode}}.$$

Resident serving cuts $T_{\mathrm{init}}$ to zero. Fusing GroupNorm, GELU, LayerNorm, and GEMM cuts memory traffic (Qilu Univ. of Tech. dropped traffic from $8MN$ to $4MN$ bytes). Adaptive step caching (TeaCache) skips redundant UNet steps using latent $\ell_1$ distance while keeping $\mathrm{PSNR} \ge 25\ \mathrm{dB}$.

### Roadmap Links

- **Stage 3 / M11**: Diffusion step skipping, TeaCache gating, and async video I/O.
- **Stage 2 / M07**: Custom CUDA/TileLang fusion and TensorRT compilation.
- **Stage 3 / M09**: Prelim $\ge 16$-bit rule vs. finals unlocked precision.

### Visual

Prelim vs. Finals speedup waterfall: Qilu Univ. of Tech. (5.41x 1-GPU, 8.13x multi-GPU), Shanghai Univ. (8.22x 2-GPU end-to-end, 14.53x single-step), PKU (26 s/case), and BUPT (30 s/case, >20x) (`diagrams/png/c06_asc26_unifolm_wma.png`).

### Notes

- **Qilu Univ. of Tech. (Prelim):** 5.41x 1-GPU / 8.13x multi-GPU via TileLang/CUDA NHWC fusion ($8MN \to 4MN$ bytes), resident server, RAMDisk (`tmpfs`) + async FFmpeg, and hybrid parallelism.
- **Shanghai Univ. (Prelim):** 8.22x dual-GPU end-to-end via TensorRT ONNX, UNet TeaCache, and ParaStep-Adaptive speculative dual-GPU overlap (PSNR 39.8 to 36.9 dB).
- **PKU (26 s) and BUPT (30 s) in Finals:** >20x speedup (from ~13 min to under 30 s) via `/preload`–`/warmup`–`/run` serving, decoupled sampling steps, TeaCache, and async streaming output.

---

## C07: ASC26 AMSS-NCKU (Binary Black Hole Merger)

**Source:** ASC26 Committee Talk (pp.16–19; 18 pts, 5 kW cap) and Tsinghua Talk (Song Jiaxing, pp.2–32).

### What It Does

AMSS-NCKU solves Einstein's field equations on 9-level Adaptive Mesh Refinement (AMR) grids to simulate black hole mergers and gravitational waves. Finals scored GW150914 inspiral (4 pts), three-black-hole collision (5 pts), and full merger waveforms (9 pts). Accuracy requires trajectory $\mathrm{RMS} < 1\%$ and ADM violation $< 2$.

### Math and Bottlenecks

TwoPunctures builds initial data. RK4 then evolves 24 coupled fields per grid point using 3D stencils across 9 refinement levels (level 8 runs 32 fine steps per coarse step). Bottlenecks shift three times:
1. **Compute:** Thousands of FLOPs per point in RHS.
2. **Transfer:** 122 host-device pack/copy/unpack roundtrips and 65 AMR interpolations per coarse step.
3. **Analysis:** CPU spherical-surface waveform extraction stalls the GPU.

### Roadmap Links

- **Stage 3 / M12**: Bottleneck migration and 200-step stale-copy regression.
- **Stage 1 / M03–M04**: Amdahl wall fraction (1.47x RHS gave 1.22x step speedup) and register reuse.
- **Stage 2 / M07–M08**: GPU-resident pools, kernel fusion/fission, shared-memory 3D halos, and async relay buffers.

### Visual

Tsinghua step-time drop (CPU 4.5 s $\to$ GPU v1 4.7 s $\to$ resident 1.4 s $\to$ 2+62 core split 1.0 s $\to$ 3-stage relay 0.85 s) beside ZJU (18.6x prelim $\to$ 30x finals) and PKU (5.50x, RMS $1.9 \times 10^{-9}$) (`diagrams/png/c07_asc26_amss_ncku.png`).

### Notes

- **Tsinghua (prep machine: 4x H100 without NVLink + 256-core EPYC 9755):** Ran all grids on 1 H100 to avoid PCIe inter-GPU hops. Kept 60+ temporary arrays in registers (1500 to 600 LOC), moved all 65 interpolations onto GPU across 150+ commits (4.7 s to 1.4 s), split 64 host cores into 2 driver + 62 OpenMP analysis threads (1.0 s), and added 3-stage ring buffers (0.85 s). Stale copies passed at 50 steps but failed >60x at 200 steps.
- **UESTC (Prelim):** OpenMP task `data_packer`, GPU RK4 fusion, device memory pool, and pinned async transfers.
- **Zhejiang Univ. (Prelim to Finals):** 44,425 s (32-MPI CPU) to 2,376 s (1 GPU) = 18.6x prelim, reaching 30x in finals via multi-stream ghost-zone sync, kernel fission + `__launch_bounds__`, and 3D shared-memory tiling.
- **PKU (2nd on task in finals):** 5.50x amortized speedup at RMS $1.9 \times 10^{-9}$, plus 5.46x OpenMP speedup on TwoPunctures (468.75 s to 85.88 s).

---

## C08: ASC26 QiboTN (CPU-Only Quantum Tensor-Network Simulation)

**Source:** ASC26 Committee Talk (pp.20–21; 18 pts, CPU-only, 5 kW cap).

### What It Does

QiboTN simulates quantum circuits (QFT, QAOA, Supremacy) using tensor-network contraction on CPUs. Grading checks mean expectation values and ranks by wall time. Any GPU use scores 0.

### Math and Bottlenecks

Direct state-vector simulation stores $2^n$ `complex128` amplitudes (16 bytes each):

$$M(n) = 16 \cdot 2^{n}\ \text{bytes} \implies M(20) = 16\ \mathrm{MiB}, \quad M(40) = 16\ \mathrm{TiB}.$$

*Unit correction:* Slide p.20 of the ASC26 talk prints `16 GB` and `16 PB` (a 1024x typo). Exact values are **16 MiB** (20 qubits) and **16 TiB** (40 qubits). Tensor-network contraction avoids the $2^n$ wall, making Python interpreter dispatch, tensor transposes, and memory allocation the main CPU bottlenecks.

### Roadmap Links

- **Stage 1 / M02**: Exponential memory wall ($16 \cdot 2^n$ bytes) and cache-friendly layouts.
- **Stage 2 / M05**: CPU-only SIMD, OpenMP, native C kernels, and NUMA memory pools.
- **Stage 4 / M16**: Expectation-value checks during language rewrites.

### Visual

Log-scale memory curve $16 \cdot 2^n$ showing 20q = 16 MiB and 40q = 16 TiB beside Fudan's Python-to-C rewrite (`diagrams/png/c08_asc26_qibotn.png`).

### Notes

- **Bottlenecks:** Python dispatch overhead in QiboTN/Quimb, temporary tensor allocations, contraction order, and unpinned BLAS threads.
- **Winning method:** Fudan University rewrote the core contraction loops from Python into native C with custom memory management, gaining tens-of-times speedup while matching expectation values.

---

## C09: ASC26 Mystery App: LeWorldModel (JEPA on AMD W7900D)

**Source:** ASC26 Committee Talk (pp.22–23; 18 pts, 5 kW cap, AMD W7900D).

### What It Does

Revealed on site, `LeWorldModel` (LeWM) is a JEPA world model that predicts dynamics in latent space. Teams ran 200 `PushT` planning and video cases on sponsored **AMD W7900D** GPUs (ROCm), minimizing wall time with task **success rate $\ge 90\%$**.

### Math and Bottlenecks

Each episode loops JEPA Encoder–Predictor rollouts inside Cross-Entropy Method (CEM) trajectory planning. Small batches make GPU kernels launch-bound while CPU video encoding stalls the host. AMD W7900D requires ROCm/HIP graphs and PyTorch compilation.

### Roadmap Links

- **Stage 3 / M11**: Latent feature caching and accuracy-gated CEM pruning.
- **Stage 2 / M05 and M08**: NUMA worker pools, multi-node slicing, and HIP graph capture.
- **Stage 4 / M16**: 48-hour mystery-app profiling on AMD ROCm hardware.

### Visual

JEPA + CEM planning loop beside top-3 wall times for 200 PushT cases (BUPT 14 s, Tsinghua 16 s, PKU 17 s; all >100x speedup at $\ge 90\%$ success) (`diagrams/png/c09_asc26_leworldmodel.png`).

### Notes

- **BUPT (14 s):** Dual-node slicing, tuned CEM iterations/population, BF16 + initial/goal feature caching, and early stop on solved episodes.
- **Tsinghua (16 s):** NUMA-bound worker pool, distributed CEM + tensor caching, compute-graph capture/replay, and async video encoding.
- **PKU (17 s):** Client/server multi-node GPU layout, BF16 + dynamic compilation of hot cost tensors, zero-copy tensor conversion, and tuned CEM settings.

---

## C10: ASC26 Group Competition: ICON (Global Climate Model)

**Source:** ASC26 Committee Talk (pp.8–9, 24–25; 8 pts, CPU-only, 5 kW cap).

### What It Does

Five-university alliances optimized the SC25 Gordon Bell Prize-winning ICON Earth-system model across three benchmarks (`RCE_torus`, `OMIP` ocean + sea ice, and `aquaplanet`). Execution was **CPU-only** within 5 kW. Alliances shared code patches, while each team ran independently on its own cluster.

### Math and Bottlenecks

ICON discretizes climate PDEs on a uniform **icosahedral** mesh, removing the polar grid bunching seen in GoMars (C03). Under CPU-only rules, speed depends on inner-loop SIMD vectorization, compact halo exchanges, OpenMP scheduling, removing redundant kernels, and cutting MPI sync waits.

### Roadmap Links

- **Stage 2 / M05–M06**: Inner-loop SIMD, OpenMP scheduling, halo reduction, and MPI sync tuning.
- **Stage 1 / M03**: Multi-component load balance and strong scaling.
- **Stage 4 / M16**: Cross-university git patch sharing with independent cluster runs.

### Visual

Uniform icosahedral mesh vs. latitude-longitude poles, paired with the winning alliance flow (shared patch $\to$ 5 independent CPU-only runs: QHU, SJTU, BUAA, BNU, EAFIT) (`diagrams/png/c10_asc26_icon_group.png`).

### Notes

- **Winning alliance (Qinghai Univ., SJTU, BUAA, BNU, EAFIT Colombia):** Tuned OpenMP scheduling, trimmed halo exchanges, removed redundant kernels, added explicit inner-loop SIMD directives, and cut MPI sync overhead by ~5%.
