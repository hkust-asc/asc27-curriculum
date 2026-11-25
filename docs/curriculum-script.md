# 16-Module Teaching Script (M01 to M16)

This script details all 16 modules in [roadmap.md](roadmap.md). Each Wednesday session (18:30 to 20:00 HKT) runs one live lab while students read the short math notes ahead of class.

Commands target a Linux cluster with Slurm, GCC/Clang, OpenMPI, and CUDA/ROCm. Historical 3/4/5 kW limits appear in M15 as practice scenarios (official ASC27 power cap and hardware list are TBD).

---

## M01: GEMM Workload, Timing, and Floating-Point Precision

**Stage:** Stage 1, Week 1 (2026-11-25 to 12-01).

### Slide Title

GEMM $2n^3$ Work, Monotonic Timers, and IEEE-754 Precision

### Slide Bullets

- Dense $n \times n$ matrix multiply $C = AB$ executes $2n^3$ floating-point operations (multiply and add counted separately).
- Monotonic wall time, CPU time, and CUDA events measure different scopes. Declare the timer with every GFLOP/s value.
- Mantissa bits set precision: FP64 has 52, FP32 has 23, FP16 has 10, and BF16 has 7. Long loops accumulate rounding drift.
- Compiler flag `-ffast-math` reorders floating-point additions. Speed changes, and trailing digits change too.
- Match every run against a reference output before recording speedup.

### Visual

Dual-axis chart of $2n^3$ FLOPs vs. GFLOP/s across $n \in \{256, 512, 1024, 2048\}$ with FP32 vs. FP64 error (`diagrams/png/m01_gemm_work_traffic.png`).

### Speaker Notes and Lab

**1. Derivation.** Each $(i, j, k)$ triple in $C_{ij} = \sum_{k=0}^{n-1} A_{ik} B_{kj}$ runs one multiply and one add. Total work is $W = 2n^3$, and sustained speed is $P_{\mathrm{eff}} = W / T_{\mathrm{wall}}$. Exclude cold memory allocation from $T_{\mathrm{wall}}$ so small-$n$ timings measure math. IEEE-754 unit roundoff is $u = 2^{-(m+1)}$, so inner-product error scales as $O(n u) \lVert a \rVert \lVert b \rVert$.

**2. Lab.** Write a plain C11 triple-loop GEMM. Time only the compute loop with `clock_gettime(CLOCK_MONOTONIC)` after one warmup pass. Compare `-O3` with `-O3 -ffast-math`:

```bash
gcc -O3 -std=c11 -o gemm_o3 gemm.c -lm
gcc -O3 -ffast-math -std=c11 -o gemm_fast gemm.c -lm
/usr/bin/time -f "wall=%e user=%U sys=%S" ./gemm_o3 1024
perf stat -e task-clock,cycles,instructions ./gemm_o3 1024
perf stat -e task-clock,cycles,instructions ./gemm_fast 1024
```

Compute $\lVert C - C_{\mathrm{ref}} \rVert_F / \lVert C_{\mathrm{ref}} \rVert_F$ against FP64 for $n \in \{512, 1024, 2048\}$ and commit `results/w01-gemm.md`.

**3. Reading.** Bryant & O'Hallaron, *CS:APP* (3rd ed.), Ch. 2 and Ch. 5; Hennessy & Patterson (6th ed.), Appendix J.

**4. ASC Tip.** State $W$ and $T_{\mathrm{wall}}$ next to every GFLOP/s figure in proposals. Always verify accuracy before reporting speedup.

---

## M02: Memory Wall, Cache Locality, and NUMA

**Stage:** Stage 1, Week 2 (2026-12-02 to 12-08).

### Slide Title

Cache Latency, Data Locality, and Multi-Socket NUMA

### Slide Bullets

- Off-chip data transfer follows $T(m) = \alpha + m / B$. Spilling past L1/L2/L3 cache caps speed.
- Spatial locality uses full 64-byte cache lines via unit-stride loops. Temporal locality reuses hot blocks before eviction.
- Changing GEMM loop order from `ijk` to `ikj` keeps $2n^3$ FLOPs fixed while slashing cache misses.
- Multi-socket servers split DRAM into NUMA domains. Remote socket reads add latency $\alpha$ and cut bandwidth $B$.
- First-touch allocation binds memory pages to the socket that initializes them. Initialize arrays in parallel.

### Visual

Memory hierarchy staircase (L1, L3, local DRAM, remote NUMA) beside a row-major vs. strided access grid (`diagrams/png/m02_memory_hierarchy_numa.png`).

### Speaker Notes and Lab

**1. Derivation.** Each cache miss loads a 64-byte line at cost $T(m) = \alpha + m/B$. Naive GEMM moves $Q = \Theta(n^3)$ bytes, holding intensity $I = W / Q$ near $O(1)$. Cache blocking with tile size $b$ keeps a $b \times b$ block in cache, dropping DRAM traffic to $O(n^3/b + n^2)$ bytes and raising $I$ by $b\times$.

**2. Lab.** Build a 2D 5-point stencil larger than the last-level cache (LLC). Measure cache misses and local vs. remote NUMA speed:

```bash
gcc -O3 -std=c11 -o stencil stencil.c
perf stat -e cache-references,cache-misses,LLC-load-misses ./stencil 4096
numactl --hardware
numactl --cpunodebind=0 --membind=0 ./stencil 4096
numactl --cpunodebind=0 --membind=1 ./stencil 4096
```

On a single-socket laptop, run the NUMA test on a dual-socket cluster node via `srun` and log `numactl --hardware`.

**3. Reading.** Bryant & O'Hallaron, *CS:APP* (3rd ed.), Ch. 6; Hennessy & Patterson (6th ed.), Ch. 2.

**4. ASC Tip.** Finals nodes often use dual-socket CPUs (like 256-core dual EPYC 9755 in ASC26). Missing first-touch init or NUMA binding drops 30% to 50% of memory bandwidth on HPCG and CPU stencils.

---

## M03: Amdahl and Gustafson Scaling Limits

**Stage:** Stage 1, Week 3 First Half (2026-12-09 to 12-15).

### Slide Title

Strong Scaling Ceilings and Weak Scaling Assumptions

### Slide Bullets

- Amdahl's Law caps fixed-problem strong scaling at $S(k) = 1 / [(1 - f) + f / k]$, with ceiling $1 / (1 - f)$.
- Gustafson's Law gives scaled speedup $(1 - f) + f k$ when per-worker load stays constant and serial work stays flat.
- Serial setup, file I/O, barrier wait, and load imbalance grow $(1 - f)$ well before core counts fill up.
- Weak scaling increases total memory and network volume, so re-profile at every scale point.
- Label every scaling plot as strong or weak and print exact problem size $N$ at each point.

### Visual

Amdahl ($f = 0.90, 0.95, 0.99$) vs. Gustafson curves beside stacked bars showing serial time share across $k = 1..16$ (`diagrams/png/m03_amdahl_gustafson.png`).

### Speaker Notes and Lab

**1. Derivation.** Normalize single-core runtime to $1 = (1 - f) + f$. On $k$ workers, fixed-size runtime is $T(k) = (1 - f) + f/k$, giving $S(k) = 1 / [(1 - f) + f/k]$. At $f = 0.90$, 16 cores reach $6.4\times$ and infinite cores cap at $10\times$. In ASC26 AMSS-NCKU, speeding up the RHS kernel by $1.47\times$ gave $1.22\times$ full-step speedup because RHS took 20% of wall time.

**2. Lab.** Add OpenMP to M01 GEMM and sweep thread counts under strong and weak scaling:

```bash
gcc -O3 -fopenmp -o gemm_omp gemm_omp.c -lm
for k in 1 2 4 8 16; do
  OMP_NUM_THREADS=$k OMP_PROC_BIND=close OMP_PLACES=cores ./gemm_omp 1024
done
```

Fit the empirical serial fraction $(1 - f)$, plot model vs. measured speedup, and explain any gap.

**3. Reading.** Hennessy & Patterson (6th ed.), Ch. 1; Stanford CS149 Lectures 1–2; Amdahl (1967) and Gustafson (1988).

**4. ASC Tip.** HPL scales weakly as $N$ grows with RAM. Fixed-mesh scientific codes and HPCG hit strong-scaling ceilings quickly.

---

## M04: Roofline Model and Bottleneck Diagnosis

**Stage:** Stage 1, Week 3 Second Half (2026-12-09 to 12-15).

### Slide Title

Roofline Upper Bounds and Hardware-Anchored Diagnosis

### Slide Bullets

- Attainable speed obeys $R \le \min(P_{\mathrm{peak}}, B \cdot I)$, where arithmetic intensity $I = W / Q$ is FLOPs per byte moved.
- Ridge point $I_b = P_{\mathrm{peak}} / B$ divides the memory-bandwidth slope ($I < I_b$) from the compute roof ($I > I_b$).
- Measure $P_{\mathrm{peak}}$ and sustained STREAM bandwidth $B$ directly on your target node.
- Follow four steps: count $W$, measure $Q$, plot $(I, R)$ on the Roofline, then tune the active limit.
- Near the compute roof, further gains require fewer FLOPs or tuning outer caller code.

### Visual

Log-log Roofline plot with STREAM Triad slope, scalar and SIMD roofs, ridge $I_b$, and plotted GEMM/stencil points (`diagrams/png/m04_roofline_model.png`).

### Speaker Notes and Lab

**1. Derivation.** Runtime obeys $T \ge \max(W / P_{\mathrm{peak}}, Q / B)$. Inverting gives $R = W / T \le \min(P_{\mathrm{peak}}, B \cdot I)$. Pipeline stalls, bad instruction mix, and launch latency push real kernels below the roof.

**2. Lab.** Measure DRAM bandwidth with STREAM Triad and hardware counters on M01/M02 binaries:

```bash
gcc -O3 -fopenmp -DSTREAM_ARRAY_SIZE=80000000 -o stream stream.c
OMP_NUM_THREADS=16 OMP_PROC_BIND=close ./stream
perf stat -e cycles,instructions,LLC-load-misses,fp_arith_inst_retired.scalar_double ./gemm_o3 1024
perf stat -e cycles,instructions,LLC-load-misses ./stencil 4096
```

Submit a one-page Roofline chart showing $P_{\mathrm{peak}}$, STREAM $B$, $I_b$, and both kernels.

**3. Reading.** Williams, Waterman, & Patterson, "Roofline" (*CACM*, 2009); Stanford CS149 Roofline lecture.

**4. ASC Tip.** Combine Roofline with time-share profiling. Tuning a kernel that takes 15% of total time yields small gains even at the compute roof.

---

## M05: CPU SIMD, OpenMP, and NUMA Pinning

**Stage:** Stage 2, Weeks 4 to 5 (2026-12-16 to 12-29).

### Slide Title

Vector Lanes, OpenMP Threading, and False-Sharing Fixes

### Slide Bullets

- AVX2 runs 4 FP64 lanes per FMA and AVX-512 runs 8. Dependencies or pointer aliasing block auto-vectorization.
- Use `-fopt-info-vec-missed` or `-Rpass-missed=loop-vectorize` to inspect why loops stay scalar.
- Dynamic or guided OpenMP schedules balance irregular loops where static chunks leave trailing threads waiting.
- `OMP_PROC_BIND=close` keeps threads on one socket. `spread` uses memory channels across all sockets.
- False sharing happens when threads write adjacent slots in one 64-byte cache line. Pad each slot to 64 bytes.

### Visual

CPU diagram showing AVX lanes, padded per-thread accumulators, and `close` vs. `spread` NUMA placement (`diagrams/png/m05_simd_openmp_numa.png`).

### Speaker Notes and Lab

**1. Derivation.** Vector width $v$ and $p$ cores give up to $v \cdot p$ speedup when bandwidth and coherence hold. Contiguous `sum[tid]` doubles share one 64-byte MESI line across 8 threads, causing coherence storms. Padding with `alignas(64)` removes the invalidations.

**2. Lab.** Benchmark scalar, `-O3`, `omp simd`, and AVX2/AVX-512 intrinsics, plus `close` vs. `spread` pinning and a false-sharing fix:

```bash
gcc -O3 -march=native -fopenmp -fopt-info-vec-missed -o gemm_vec gemm_vec.c -lm
OMP_NUM_THREADS=16 OMP_PROC_BIND=close OMP_PLACES=cores \
  numactl --cpunodebind=0 --membind=0 perf stat -e L1-dcache-load-misses,cache-misses ./gemm_vec 1024
OMP_NUM_THREADS=16 OMP_PROC_BIND=spread OMP_PLACES=cores \
  perf stat -e L1-dcache-load-misses,cache-misses ./gemm_vec 1024
```

Record wall time before and after 64-byte padding on a parallel reduction.

**3. Reading.** MIT 6.172 Lectures on Vectorization and Multicore; *CS:APP* Ch. 5; Intel Intrinsics Guide.

**4. ASC Tip.** CPU-only finals apps (ASC25 AlphaFold3/DeepSeek, ASC26 QiboTN/ICON) award zero points if GPUs run. Clean SIMD loops and NUMA pinning decide these tasks.

---

## M06: MPI Domain Decomposition, Halo Exchange, and RDMA

**Stage:** Stage 2, Weeks 6 to 7 (2026-12-30 to 2027-01-12).

### Slide Title

Domain Splitting, Non-Blocking Halos, and Hockney Collectives

### Slide Bullets

- 2D and 3D grid splits exchange only ghost (halo) borders. Larger subdomains raise the compute-to-halo ratio.
- Overlap interior math with `MPI_Isend`, `MPI_Irecv`, and `MPI_Waitall` to hide network latency $\alpha$.
- Small messages hit latency $\alpha$. Large collectives saturate bandwidth $B$ via $T(m) = \alpha + m / B$.
- Ring All-Reduce on $G$ bytes across $p$ ranks moves $2(p - 1)G / p$ bytes per rank.
- Align process grid $P \times Q$ with physical sockets and InfiniBand HCAs.

### Visual

2D grid with highlighted halo strips beside a log-log Hockney latency/bandwidth plot (`diagrams/png/m06_mpi_halo_hockney.png`).

### Speaker Notes and Lab

**1. Derivation.** Ring All-Reduce splits $G$ bytes into $p$ chunks and runs $p-1$ reduce-scatter steps plus $p-1$ all-gather steps. Each rank moves $V_{\mathrm{ring}} = 2 \frac{p - 1}{p} G$ bytes in time $2(p - 1)\alpha + 2\frac{p - 1}{p}\frac{G}{B}$. RDMA bypasses the OS TCP stack to shrink $\alpha$. Per-socket HCAs keep bisection bandwidth high.

**2. Lab.** Implement a non-blocking 2D halo stencil verified against serial output, then sweep `MPI_Allreduce` sizes:

```bash
mpicc -O3 -std=c11 -o halo2d halo2d.c -lm
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./halo2d 2048 200
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./osu_allreduce -m 8:4194304
```

Log the network fabric and L2 error. In Week 7, confirm your advisor received the ASC27 account email before the **2027-01-10** deadline.

**3. Reading.** Gropp, Lusk, & Skjellum, *Using MPI* (3rd ed.), Ch. 3–5; Stanford CS149 Message Passing lecture; OSU Micro-Benchmarks docs.

**4. ASC Tip.** One halo corner bug fails verification on HPCG, GoMars, AMSS-NCKU, and ICON. In ASC26, Tsinghua used per-socket InfiniBand HCAs to win HPCG.

---

## M07: GPU SIMT and Hand-Written CUDA GEMM

**Stage:** Stage 2, Week 8 First Half (2027-01-13 to 01-19).

### Slide Title

SIMT Warps, Shared-Memory Tiling, and cuBLAS Comparison

### Slide Bullets

- GPUs schedule 32-thread warps (NVIDIA) or 64-thread wavefronts (AMD) across SMs to hide HBM latency.
- Uncoalesced global loads, shared-memory bank conflicts, and warp divergence cut throughput sharply.
- Naive one-thread-per-output FP32 GEMM sits near $I \approx 0.25$ FLOP/byte and stalls on HBM bandwidth.
- Tiling $A$ and $B$ into shared memory plus register micro-tiles raises intensity linearly with tile size $b$.
- CUDA and HIP share the same grid, block, and shared-memory model across NVIDIA and AMD GPUs.

### Visual

GEMM tiling hierarchy (HBM $\to$ shared memory $\to$ registers) beside a speedup bar from naive to register-tiled vs. cuBLAS (`diagrams/png/m07_cuda_gemm_tiling.png`).

### Speaker Notes and Lab

**1. Derivation.** Loading $b \times b$ tiles of $A$ and $B$ reads $2b^2$ elements for $2b^3$ FLOPs, boosting HBM intensity by $b/2$. Adding a $t_m \times t_n$ register tile per thread cuts shared-memory reads by $t_m t_n / (t_m + t_n)$. High register counts lower active warps (occupancy), so check the balance in `ncu`.

**2. Lab.** Implement naive, shared-memory tiled, and register-tiled GEMM and compare with cuBLAS (or `hipcc` + rocBLAS):

```bash
nvcc -O3 -arch=native -o gemm_naive gemm_naive.cu -lcublas
nvcc -O3 -arch=native -o gemm_tiled gemm_tiled.cu -lcublas
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,dram__throughput.avg.pct_of_peak_sustained_elapsed,sm__warps_active.avg.pct_of_peak_sustained_active \
  ./gemm_tiled 4096
```

Verify relative error against cuBLAS before recording % of cuBLAS speed at $n = 4096$.

**3. Reading.** NVIDIA *CUDA C++ Programming Guide* (Programming Model and Performance Guidelines); Stanford CS149 GPU lectures; Simon Boehm's CUDA SGEMM notes.

**4. ASC Tip.** Custom kernel fusion won big in ASC26: Qilu cut UnifoLM traffic from $8MN$ to $4MN$ bytes, and ZJU tiled 3D stencils with `__launch_bounds__` in AMSS-NCKU.

---

## M08: Slurm Binding and Timeline Profiling (`nsys` / Score-P)

**Stage:** Stage 2, Week 8 Second Half (2027-01-13 to 01-19).

### Slide Title

Slurm Resource Binding and Multi-Stream Timeline Analysis

### Slide Bullets

- Slurm flags (`-N`, `-n`, `--cpus-per-task`, `--cpu-bind=cores`, `--gres=gpu`) lock repeatable CPU and GPU affinity.
- Use `salloc` for live debugging. Record all final numbers from checked-in `sbatch` scripts.
- Nsight Systems (`nsys`) shows timeline gaps (H2D copies, host launch stalls, stream syncs). Nsight Compute (`ncu`) inspects one kernel.
- Score-P traces MPI barrier waits and OpenMP skew across multi-node runs.
- Turn tracing off when recording final wall-clock scores.

### Visual

Multi-track timeline comparing serial H2D/Compute/D2H against pinned async overlap plus an MPI rank wait trace (`diagrams/png/m08_timeline_profiling.png`).

### Speaker Notes and Lab

**1. Derivation.** Synchronous GPU steps sum serially: $T_{\mathrm{serial}} = T_{\mathrm{H2D}} + T_{\mathrm{kernel}} + T_{\mathrm{D2H}}$. Pinned host memory (`cudaMallocHost`) and chunked streams overlap stages toward $T_{\mathrm{pipe}} \approx \max(T_{\mathrm{H2D}}, T_{\mathrm{kernel}}, T_{\mathrm{D2H}})$. On MPI ranks, any load skew adds directly to Amdahl's serial share $(1 - f)$.

**2. Lab.** Capture `nsys` and Score-P traces under Slurm:

```bash
salloc -N 1 -n 1 --cpus-per-task=8 --gres=gpu:1 --time=01:00:00
srun --cpu-bind=cores nsys profile --trace=cuda,nvtx,osrt -o gemm_trace ./gemm_tiled 4096
nsys stats --report cuda_gpu_kern_sum,cuda_gpu_mem_time_sum gemm_trace.nsys-rep
scorep mpicc -O3 -o halo2d_sc halo2d.c -lm
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./halo2d_sc 2048 200
```

Mark two idle gaps in `nsys` and name the slowest MPI rank pair from Score-P.

**3. Reading.** SchedMD Slurm docs (`srun`/`sbatch` binding); NVIDIA *Nsight Systems User Guide*; Score-P User Manual.

**4. ASC Tip.** Finals lock hardware during testing windows. Putting exact binding flags in launch scripts prevents silent config drift.

---

## M09: Transformer VRAM Budgeting and Mixed Precision

**Stage:** Stage 3, Week 9 (2027-01-20 to 01-26).

### Slide Title

Parameter, Gradient, Optimizer, and Activation Memory Math

### Slide Bullets

- Model weights are one slice of training VRAM. Gradients, FP32 optimizer states, and activations take most of the memory.
- Mixed-precision Adam uses about $16\,\Phi$ static bytes for $\Phi$ parameters (2B weights, 2B grads, 4B master, 4B momentum, 4B variance).
- Activation RAM scales with `batch * layers * seq_len * hidden_dim`. Activation checkpointing trades compute for memory.
- FP16 has a 5-bit exponent and needs `GradScaler`. BF16 keeps FP32's 8-bit exponent and trains directly.
- FP8 (E4M3/E5M2) needs Tensor Core support, dynamic scaling, and rule compliance checks.

### Visual

Stacked VRAM bars (FP32 vs. BF16 vs. BF16 + checkpointing) beside FP32/FP16/BF16/FP8 bit layouts (`diagrams/png/m09_transformer_memory_precision.png`).

### Speaker Notes and Lab

**1. Derivation.** FP32 Adam holds $4\Phi$ bytes each for weights, grads, $m$, and $v$ ($16\Phi$ bytes). Mixed-precision Adam stores BF16 weights and grads ($4\Phi$) plus FP32 master weights and moments ($12\Phi$), still $16\Phi$ static bytes while halving GEMM bandwidth and doubling Tensor Core speed. Gradient checkpointing adds ~33% forward compute to cut saved activations from $O(L)$ to $O(\sqrt{L})$.

**2. Lab.** Print `param.numel()` and `torch.cuda.max_memory_allocated()` across FP32, BF16, and checkpointing, then double batch size until OOM:

```bash
python3 train_tiny_gpt.py --dtype fp32 --batch 16 --seq 512 --layers 6 --d_model 512
python3 train_tiny_gpt.py --dtype bf16 --batch 16 --seq 512 --layers 6 --d_model 512
python3 train_tiny_gpt.py --dtype bf16 --batch 16 --seq 512 --layers 6 --d_model 512 --grad_ckpt
python3 train_tiny_gpt.py --dtype bf16 --batch 128 --seq 512 --layers 6 --d_model 512
```

Match predicted bytes to PyTorch stats and identify which tensor triggered the OOM.

**3. Reading.** Micikevicius et al., *Mixed Precision Training* (ICLR 2018); Korthikanti et al. (MLSys 2023, Sec. 4); PyTorch `torch.amp` docs.

**4. ASC Tip.** Check precision rules first: ASC26 UnifoLM prelim required $\ge 16$-bit weights, and ASC22 Yuan required $\mathrm{Loss} < 7.0$ over 1B tokens.

---

## M10: Distributed Training (DP, FSDP, TP, PP) and Ring All-Reduce

**Stage:** Stage 3, Weeks 10 to 11 (2027-01-27 to 02-09).

### Slide Title

Multi-GPU Parallelism and Collective Communication Cost

### Slide Bullets

- DDP copies static state to every GPU and runs Ring All-Reduce on gradients $G$ each step.
- FSDP / ZeRO-3 shards parameters, gradients, and optimizer state across $p$ GPUs using All-Gather and Reduce-Scatter.
- Tensor Parallelism (TP) splits intra-layer GEMMs with two All-Reduces per block, requiring NVLink or XGMI.
- Pipeline Parallelism (PP) splits layers across $p_{\mathrm{pp}}$ stages with bubble share $(p_{\mathrm{pp}} - 1) / (m + p_{\mathrm{pp}} - 1)$.
- Ring All-Reduce moves $2(p - 1)G / p$ bytes per rank through NCCL (NVIDIA) or RCCL (AMD).

### Visual

Four-panel DDP, FSDP, TP, and PP comparison on 4 GPUs beside the Ring All-Reduce chunk flow (`diagrams/png/m10_distributed_training_ring.png`).

### Speaker Notes and Lab

**1. Derivation.** DDP moves $V = 2 \frac{p - 1}{p} G$ bytes per GPU and overlaps communication with backward hooks. FSDP moves $3 \frac{p - 1}{p} G$ bytes (1.5x DDP) to fit larger models. On PCIe servers without NVLink, cross-GPU TP stalls on PCIe bandwidth, making DDP/FSDP or sample-level splits faster.

**2. Lab.** Run 2-GPU DDP and FSDP with `torchrun` and profile collective overlap:

```bash
srun -N 1 --ntasks=1 --gres=gpu:2 --cpus-per-task=8 \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode ddp --seq 512
srun -N 1 --ntasks=1 --gres=gpu:2 --cpus-per-task=8 \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode fsdp --seq 512
NCCL_DEBUG=INFO nsys profile -o ddp_nccl \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode ddp --steps 10
```

Check `NCCL_DEBUG=INFO` for active transport (SHM/NVLink/PCIe/IB) and match All-Reduce time to $2(p - 1)G / (p B_{\mathrm{link}})$. Verify a 2-GPU TP linear layer matches unsharded output.

**3. Reading.** Rajbhandari et al., *ZeRO* (SC 2020); Shoeybi et al., *Megatron-LM* (2019, Sec. 3); PyTorch DDP/FSDP tutorials; NVIDIA NCCL docs.

**4. ASC Tip.** ASC22 Yuan required PyTorch logs with seeds, timestamps, and per-step loss. Log clean CSV and TensorBoard traces from day one.

---

## M11: LLM and World-Model Inference Optimization

**Stage:** Stage 3, Week 12 (2027-02-10 to 02-16).

### Slide Title

Prefill vs. Decode Regimes, KV Cache Growth, and Diffusion Speedup

### Slide Bullets

- LLM prefill runs parallel GEMMs over all prompt tokens (compute-bound). Decode generates one token per step (memory-bound).
- KV cache grows as $2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$, turning long decode into a streaming HBM/DRAM bottleneck.
- Resident serving, CUDA/HIP graphs, and `torch.compile` or TensorRT remove model-load and Python dispatch stalls.
- Diffusion world models pay $N_{\mathrm{steps}} \cdot T_{\mathrm{step}}$. Step caching (TeaCache), op fusion, and async video I/O cut runtime.
- Check every shortcut against quality targets (PSNR $\ge 25$ in UnifoLM, $\ge 90\%$ success in LeWorldModel).

### Visual

Prefill vs. Decode timeline with growing KV read width plus a diffusion step-caching schematic (`diagrams/png/m11_llm_inference_kv_denoising.png`).

### Speaker Notes and Lab

**1. Derivation.** Each decode step reads all layer weights plus $2 b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$ KV bytes for $b_{\mathrm{sz}}$ tokens. At $b_{\mathrm{sz}} = 1$, intensity stays near $I \approx 1$ FLOP/byte, so time per output token (TPOT) approaches $(M_{\mathrm{weights}} + M_{\mathrm{KV}}) / B_{\mathrm{mem}}$. Quantization shrinks $M_{\mathrm{weights}}$; batching amortizes weight reads. In diffusion models, $\ell_1$ latent gating skips redundant UNet passes while protecting PSNR.

**2. Lab.** Measure prefill latency (TTFT), decode latency (TPOT), and KV memory growth on a small Transformer:

```bash
python3 bench_infer.py --prompt_len 256 --gen_tokens 128 --dtype bf16
python3 bench_infer.py --prompt_len 1024 --gen_tokens 128 --dtype bf16
nsys profile --trace=cuda,nvtx -o infer_trace \
  python3 bench_infer.py --prompt_len 256 --gen_tokens 32 --dtype bf16
```

Match measured KV bytes to $2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$ and compare eager mode with `torch.compile` or CUDA Graphs.

**3. Reading.** Pope et al., *Efficiently Scaling Transformer Inference* (MLSys 2023); Kwon et al., *PagedAttention* (SOSP 2023); Hugging Face KV Cache docs.

**4. ASC Tip.** Separate `/preload` and `/warmup` from per-case runs, and overlap FFmpeg writes on `tmpfs` RAMDisk (used by top ASC26 UnifoLM teams).

---

## M12: Scientific GPU Porting and Bottleneck Shifts (AMSS-NCKU)

**Stage:** Stage 3, Week 13 (2027-02-17 to 02-23).

### Slide Title

Bottleneck Migration and 200-Step Regression Verification

### Slide Bullets

- Moving only the hottest kernel to a GPU can slow down the app when PCIe copies enter the critical path.
- Tsinghua's AMSS-NCKU prep progression: CPU 4.5 s $\to$ GPU v1 4.7 s (122 copies) $\to$ resident 1.4 s $\to$ 2+62 core split 1.0 s $\to$ 3-stage relay 0.85 s.
- Keeping AMR grids resident in GPU HBM removes per-step PCIe roundtrips and requires host/device validity flags.
- Fast GPU steps expose CPU post-processing backpressure, solved by dedicated analysis threads and async ring buffers.
- 50-step smoke tests hide stale-copy bugs that grow >60x at 200 steps. Run long regressions before merging.

### Visual

Five-bar AMSS-NCKU timing waterfall beside a 3-stage async GPU-snapshot / D2H / CPU-analysis relay (`diagrams/png/m12_amss_bottleneck_shift.png`).

### Speaker Notes and Lab

**1. Derivation.** With 122 host-device roundtrips per coarse step, $T_{\mathrm{step}} = T_{\mathrm{GPU}} + 122(\alpha_{\mathrm{PCIe}} + m / B_{\mathrm{PCIe}}) + T_{\mathrm{pack}}$, making GPU v1 slower than 64-core CPU (4.7 s vs. 4.5 s). Keeping grids on one H100 drops step time to 1.4 s. Splitting 64 host cores into 2 driver + 62 OpenMP analysis threads cuts it to 1.0 s, and triple-buffered snapshot relay reaches 0.85 s.

**2. Lab.** Add a per-step host-copy mode and a stale-halo bug to M06 `halo2d`, then compare 50-step and 200-step runs:

```bash
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 50 --copy-each-step
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 200 --resident
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 50 --stale-halo-demo
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 200 --stale-halo-demo
```

Log RMS against serial reference at steps 50 and 200. Freeze all preliminary proposal charts before **2027-02-28 24:00 UTC+8**.

**3. Reading.** Song Jiaxing (Tsinghua ASC26), *Bringing Black Holes onto GPUs*; ASC26 Optimization Intro slides (UESTC, ZJU, PKU).

**4. ASC Tip.** Build an automated reference runner and RMS checker before porting. Commit small verified changes (Tsinghua logged 150+ commits).

---

## M13: HPL Benchmark and Multi-Node Tuning

**Stage:** Stage 4, Weeks 14 to 15 (2027-02-24 to 03-09).

### Slide Title

HPL Matrix Order $N$, Block Size $NB$, and $P \times Q$ Grids

### Slide Bullets

- HPL solves $Ax = b$ via LU factorization with leading workload $W = \frac{2}{3}N^3 + 2N^2$ FP64 FLOPs.
- Report $R_{\max} = W / T_{\mathrm{wall}}$ only when HPL's backward residual check prints `PASSED`.
- Larger $N$ raises compute-to-communication ratio up to ~80%–90% of usable RAM/HBM without swapping.
- Block size $NB$ balances panel factorization overhead (small $NB$) against trailing DGEMM speed (larger $NB$).
- Choose $P \times Q = p$ with $P \le Q$ aligned to nodes and HCAs to minimize broadcast hops.

### Visual

Blocked LU matrix schematic (factored, active panel, trailing DGEMM) beside $R_{\max}$ sweeps across $NB$ and $P \times Q$ (`diagrams/png/m13_hpl_panel_scaling.png`).

### Speaker Notes and Lab

**1. Derivation.** Step $k$ updates the trailing $(N - k) \times (N - k)$ matrix via rank-$NB$ DGEMM costing $2(N - k)^2 NB$ FLOPs. Summing over $N/NB$ panels yields $\frac{2}{3}N^3 + O(N^2)$ FLOPs. Trailing DGEMM supplies peak compute while panel broadcasts sit on the critical path.

**2. Lab.** Run Netlib HPL (or NVIDIA HPC-Benchmarks HPL on GPUs) across $NB \in \{128, 192, 256, 384\}$ and two $P \times Q$ grids:

```bash
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores ./xhpl | tee hpl_n1_2x4.log
srun -N 2 --ntasks=16 --cpus-per-task=4 --cpu-bind=cores ./xhpl | tee hpl_n2_4x4.log
grep -E "WR|PASSED|FAILED" hpl_n*.log
```

Check reported $R_{\max}$ manually against $\frac{2}{3}N^3 / T_{\mathrm{wall}}$.

**3. Reading.** Petitet et al., *HPL Tuning Guide*; Dongarra, Luszczek, & Petitet, "The LINPACK Benchmark" (2003).

**4. ASC Tip.** In ASC26 (5 kW cap), Qilu Univ. of Tech. won Highest LINPACK on a 4-node cluster (6x H200 + 2x W7900D) using automated parameter search and power capping.

---

## M14: HPCG Sparse Conjugate Gradient Tuning

**Stage:** Stage 4, Weeks 16 to 17 (2027-03-10 to 03-23).

### Slide Title

HPCG Sparse Kernels, Bandwidth Ceilings, and Sustained Runs

### Slide Bullets

- HPCG models PDE solvers via preconditioned conjugate gradient (SpMV, SymGS, multigrid, and dot-product `Allreduce`).
- 27-point sparse stencils sit near $I \approx 0.25$ FLOP/byte on the memory-bandwidth slope of the Roofline.
- HPCG typically reaches 1% to 5% of HPL $R_{\max}$, exposing memory and network limits.
- Practice the 1800-second sustained runtime with Quick Path disabled (historical ASC22 rule).
- Balance subdomain dimensions (`nx, ny, nz`), NUMA binding, and per-socket network links.

### Visual

27-point 3D stencil sparsity diagram beside a Roofline placing HPL at the compute roof and HPCG on the bandwidth slope (`diagrams/png/m14_hpcg_spmv_symgs.png`).

### Speaker Notes and Lab

**1. Derivation.** Each row holds up to 27 nonzeros: 54 FLOPs against 216 B values, 108 B indices, and irregular vector reads ($I < 0.25$ FLOP/byte). SymGS adds triangular dependencies requiring multicoloring or hyperplanes, while dot products add `MPI_Allreduce` latency every iteration.

**2. Lab.** Run HPCG with Quick Path disabled (60 s in class, 1800 s overnight via `sbatch`):

```bash
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores ./xhpcg
grep -E "HPCG result is|Final Summary|Total Time|GFLOP/s" HPCG-Benchmark*.txt
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores \
  perf stat -e LLC-load-misses,cycles,instructions ./xhpcg
```

Confirm `HPCG result is VALID` and compare achieved GFLOP/s against STREAM $B \times I$.

**3. Reading.** Dongarra, Heroux, & Luszczek, *HPCG Benchmark* (UTK Tech Report, 2015); `hpcg-benchmark/hpcg` docs.

**4. ASC Tip.** Tsinghua won ASC26 HPCG under 5 kW by pairing H100 HBM bandwidth with per-socket InfiniBand HCAs.

---

## M15: Power Wall, DVFS, and Cluster Co-Design

**Stage:** Stage 4, Weeks 18 to 19 (2027-03-24 to 04-06).

### Slide Title

CMOS Power Scaling, DVFS Sweet Spots, and Cluster Co-Design

### Slide Bullets

- Dynamic power obeys $P_{\mathrm{dyn}} \propto C_{\mathrm{eff}} V^2 f$. Modest clock drops cut watts faster than throughput.
- Practice against historical baselines: 3 kW (ASC22), 4 kW (ASC25), and 5 kW (ASC26). ASC27 power cap is TBD.
- Extra GPUs boost HPL peak speed while eating rack watts needed by CPU-only and memory-bound apps.
- Sample live steady-state power at the PDU, BMC/IPMI, or GPU sensors. Never subtract idle power.
- Tripping the finals power meter invalidates the active run. Keep a safety margin in every script.

### Visual

$R_{\max}$ vs. power curve with vertical dashed baselines at 3 kW, 4 kW, and 5 kW (`diagrams/png/m15_power_wall_dvfs.png`).

### Speaker Notes and Lab

**1. Derivation.** Total power is $P_{\mathrm{static}} + C_{\mathrm{eff}} V^2 f$. Under cap $P_{\max}$, cutting idle nodes and fans leaves more watts for compute silicon. Setting `nvidia-smi -pl` or ROCm power caps moves GPUs to the efficiency knee where FLOP/W peaks.

**2. Lab.** Log live GPU and node power during HPL or GEMM across three power caps:

```bash
nvidia-smi --query-gpu=timestamp,index,power.draw,clocks.sm,temperature.gpu --format=csv -l 1 > gpu_pwr.csv &
MON_PID=$!
srun -N 1 --ntasks=1 --gres=gpu:2 --cpu-bind=cores ./xhpl
kill $MON_PID
ipmitool dcmi power reading || cat /sys/class/powercap/intel-rapl:0/energy_uj
```

Plot GFLOP/s and GFLOP/W across caps and record the exact sensor scope.

**3. Reading.** Hennessy & Patterson (6th ed.), Ch. 1 (Power and Energy); Intel RAPL, NVML, and `rocm-smi` manuals.

**4. ASC Tip.** Justify node count, CPU sockets, GPUs, and interconnects across both compute-bound (HPL/AI) and bandwidth-bound (HPCG/CPU-only) workloads.

---

## M16: Mystery-App Triage, Evidence Chains, and English Defense

**Stage:** Stage 4, Weeks 20 to 24 (2027-04-07 to 05-11).

### Slide Title

48-Hour Mystery-App Triage, Evidence Bundles, and Q&A

### Slide Bullets

- Spend the first 90 minutes finding three facts: build recipe, accuracy gate, and hotspot time share.
- Lock a passing baseline and a one-command rollback script before editing code.
- Link every proposal or poster claim to an `evidence/` folder with commits, flags, logs, power traces, and diffs.
- Proposals pass similarity screening. Write original prose backed by raw team measurements.
- Rehearse a 10-minute two-speaker English talk plus 3 to 5 minutes of Q&A and cross-university patch sharing.

### Visual

48-hour triage flow (Build $\to$ Baseline $\to$ Profile $\to$ Verify Loop $\to$ Rollback $\to$ Evidence $\to$ Defense) beside the 5-file `evidence/` tree (`diagrams/png/m16_asc_workflow_scoring.png`).

### Speaker Notes and Lab

**1. Derivation.** M16 joins all layers: Roofline (`C2`) picks the target, Amdahl (`C1`) bounds the gain, RMS checks (`C3`) accept edits, and evidence packaging (`E3`) earns competition credit.

**2. Lab.** Run a 90-minute drill on an unseen solver and populate `evidence/`:

```bash
perf record -F 99 -g -- ./mystery_app --steps 20
perf report --stdio --sort=dso,symbol | head -n 40
srun --cpu-bind=cores ./mystery_app --steps 200 > evidence/02-ref.log
diff -u evidence/02-ref.log evidence/opt.log
```

Required directory tree:

```text
evidence/
  00-build.md        # compiler, modules, git commit, build flags
  01-profile.txt     # perf / nsys / Score-P hotspot breakdown
  02-ref.log         # reference output and tolerance
  03-run.sh          # single submission command + rollback target
  04-result.md       # wall time, speedup, accuracy pass, live power
```

In Week 23, two speakers rehearse a 10-minute talk and 8 Q&A probes. Week 24 runs a 48-hour mock finals sprint ending 2027-05-11.

**3. Reading.** *2027 ASC Call for Participation*; *ASC22 Final Notification* Appendix II; *ASC26 Optimization Intro* slides.

**4. ASC Tip.** Separate algorithmic edits (with math-equivalence proof) from systems edits (binding, pools, async I/O, power caps) in your slides.
