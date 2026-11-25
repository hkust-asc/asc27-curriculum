# 16-Module Teaching Script (M01 to M16)

This syllabus specifies every teaching module in [roadmap.md](roadmap.md). Weekly Wednesday sessions (18:30 to 20:00 HKT) demonstrate one live experiment per module while students study derivations beforehand. Commands assume a Linux cluster with Slurm, GCC/Clang, OpenMPI, and CUDA/ROCm toolchains; node names are left generic rather than tied to any historical ASC cluster BOM. Historical 3/4/5 kW figures appear exclusively as stress-test scenarios in M15, because the official ASC27 power cap, hardware list, and scoring formula remain TBD.

---

## M01: GEMM Workload, Timing & Floating-Point Precision

**Stage:** Stage 1, Week 1 (2026-11-25 to 12-01).

### Slide Title

GEMM $2n^3$ Operation Count, Monotonic Timing & IEEE-754 Precision

### Slide Bullets

- Dense $n \times n$ matrix multiplication $C = AB$ performs $2n^3$ floating-point operations (multiply and add counted separately).
- Monotonic wall time, CPU process time, and CUDA event intervals measure different execution scopes and must be declared alongside every GFLOP/s figure.
- IEEE-754 FP64 carries 52 mantissa bits compared with 23 in FP32, 10 in FP16, and 7 in BF16; iterative accumulation magnifies rounding error far beyond single-GEMM tolerances.
- Aggressive compiler flags such as `-ffast-math` reorder non-associative floating-point additions, shifting both speed and trailing digits.
- Unverified timings serve only as debugging scratchpad entries until matched against a reference solution.

### Visual Suggestion

Dual-axis plot showing $2n^3$ FLOPs vs. measured GFLOP/s across $n \in \{256, 512, 1024, 2048\}$ paired with a log-scale FP32 vs. FP64 relative Frobenius error curve (`diagrams/png/m01_gemm_work_traffic.png`). Use `#0B4F8A` for FP64, `#C48A1A` for FP32, and a clean white canvas.

### Speaker Notes & Lab

**1. First-Principles Derivation.** Computing $C_{ij} = \sum_{k=0}^{n-1} A_{ik} B_{kj}$ executes one multiply and one add for every $(i, j, k)$ triple, giving exact arithmetic work $W = 2n^3$ and sustained throughput $P_{\mathrm{eff}} = W / T_{\mathrm{wall}}$. If $T_{\mathrm{wall}}$ includes cold allocation or first-touch page faults, small-$n$ measurements reflect startup latency $\alpha$ rather than arithmetic throughput. IEEE-754 binary formats have unit roundoff $u = 2^{-(m+1)}$, so inner-product accumulation error scales as $O(n u) \lVert a \rVert \lVert b \rVert$.

**2. Required Lab & Profiling Tasks.** Implement a plain C11 triple-loop GEMM without calling BLAS, wrap only the compute loop with `clock_gettime(CLOCK_MONOTONIC)` after one warmup pass, and compare `-O3` against `-O3 -ffast-math`:

```bash
gcc -O3 -std=c11 -o gemm_o3 gemm.c -lm
gcc -O3 -ffast-math -std=c11 -o gemm_fast gemm.c -lm
/usr/bin/time -f "wall=%e user=%U sys=%S" ./gemm_o3 1024
perf stat -e task-clock,cycles,instructions ./gemm_o3 1024
perf stat -e task-clock,cycles,instructions ./gemm_fast 1024
```

Compute relative error $\lVert C - C_{\mathrm{ref}} \rVert_F / \lVert C_{\mathrm{ref}} \rVert_F$ against an FP64 reference kernel across $n \in \{512, 1024, 2048\}$ and commit `results/w01-gemm.md`.

**3. Classic References.** Bryant & O'Hallaron, *CS:APP* (3rd ed.), Chapter 2 (Representing and Manipulating Information: Floating Point) and Chapter 5 (Optimizing Program Performance); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (6th ed.), Appendix J (Computer Arithmetic).

**4. ASC Competition Scoring Tips.** Every GFLOP/s number in a preliminary proposal must reconcile to explicit $W$ and $T_{\mathrm{wall}}$ definitions. Past ASC tasks invalidate faster runs the moment accuracy gates fail (for instance, Yuan $\mathrm{Loss} < 7.0$ and DeePMD `dp test` consistency in ASC22), so numerical verification always precedes speedup reporting.

---

## M02: Memory Wall, Spatial/Temporal Locality & NUMA Architecture

**Stage:** Stage 1, Week 2 (2026-12-02 to 12-08).

### Slide Title

Memory Hierarchy Latency, Cache Locality & Multi-Socket NUMA

### Slide Bullets

- Off-chip data movement obeys $T(m) = \alpha + m / B$, capping performance whenever operands spill past L1/L2/L3 caches.
- Spatial locality harvests full 64-byte cache lines via unit-stride access; temporal locality reuses hot blocks before eviction.
- Switching loop order from `ijk` to `ikj` keeps $2n^3$ unchanged while cutting cache misses and wall time by an order of magnitude.
- Multi-socket servers split DRAM into NUMA domains where remote socket fetches incur higher $\alpha$ and lower $B$.
- First-touch OS allocation binds physical pages to the socket that initializes them, making parallel initialization essential.

### Visual Suggestion

Three-level memory staircase (L1, L3, local DRAM, remote NUMA DRAM) annotated with measured latency and bandwidth alongside a $4 \times 4$ row-major vs. strided access diagram (`diagrams/png/m02_memory_hierarchy_numa.png`). Highlight local NUMA in `#0D9488` and remote NUMA penalty in `#C2410C`.

### Speaker Notes & Lab

**1. First-Principles Derivation.** Every cache miss fetches a 64-byte line across the memory bus at cost $T(m) = \alpha + m/B$. In unblocked GEMM, reading $A$ and $B$ without cache reuse moves $Q = \Theta(n^3)$ bytes, holding arithmetic intensity $I = W / Q$ near $O(1)$. Cache blocking with tile size $b$ keeps a $b \times b$ submatrix resident in L1/L2, lowering DRAM traffic to $O(n^3 / b + n^2)$ bytes and raising $I$ proportionally to $b$.

**2. Required Lab & Profiling Tasks.** Build a 2D 5-point stencil whose working set exceeds the node's last-level cache (LLC), then measure cache misses and local vs. remote NUMA allocation:

```bash
gcc -O3 -std=c11 -o stencil stencil.c
perf stat -e cache-references,cache-misses,LLC-load-misses ./stencil 4096
numactl --hardware
numactl --cpunodebind=0 --membind=0 ./stencil 4096
numactl --cpunodebind=0 --membind=1 ./stencil 4096
```

If a test machine has only one NUMA node, execute the NUMA comparison on a dual-socket cluster node via `srun` and document the exact `numactl --hardware` topology.

**3. Classic References.** Bryant & O'Hallaron, *CS:APP* (3rd ed.), Chapter 6 (The Memory Hierarchy); Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (6th ed.), Chapter 2 (Memory Hierarchy Design).

**4. ASC Competition Scoring Tips.** Finals servers are commonly high-core-count dual-socket systems (such as dual AMD EPYC 9755 with 256 cores in ASC26). Omitting first-touch initialization and NUMA pinning immediately forfeits 30% to 50% of memory bandwidth on HPCG and CPU-only stencil codes.

---

## M03: Amdahl & Gustafson Laws: Physical Scaling Boundaries

**Stage:** Stage 1, Week 3 First Half (2026-12-09 to 12-15, paired with M04).

### Slide Title

Strong Scaling Ceilings & Weak Scaling Assumptions

### Slide Bullets

- Amdahl's Law bounds fixed-problem strong scaling at $S(k) = 1 / [(1 - f) + f / k]$, approaching $1 / (1 - f)$ as workers $k \to \infty$.
- Gustafson's Law yields scaled speedup $(1 - f) + f k$ only when per-worker load stays constant and serial overhead does not grow with $k$.
- Serial initialization, file I/O, barrier wait, and load imbalance inflate $(1 - f)$ long before raw core counts saturate.
- Weak scaling enlarges total memory and inter-node communication volume, requiring fresh bottleneck checks at every scale point.
- Every scaling chart must state whether problem size stayed fixed (strong) or grew proportionally (weak), along with exact $N$ per point.

### Visual Suggestion

Dual-curve chart contrasting Amdahl ($f = 0.90, 0.95, 0.99$) against Gustafson linear scaling alongside stacked wall-time bars showing serial fraction dominance at $k = 1, 2, 4, 8, 16$ (`diagrams/png/m03_amdahl_gustafson.png`). Use `#0B4F8A` for parallel work and `#C2410C` for serial fraction.

### Speaker Notes & Lab

**1. First-Principles Derivation.** Normalize single-worker runtime to $1 = (1 - f) + f$, where $(1 - f)$ is strictly serial and $f$ divides cleanly across $k$ workers. Strong scaling runtime is $T(k) = (1 - f) + f/k$, giving $S(k) = 1 / [(1 - f) + f/k]$. At $f = 0.90$, even 16 cores cap out near $6.4\times$ and infinite cores cap at $10\times$. In ASC26 AMSS-NCKU, speeding up the RHS kernel by $1.47\times$ produced only $1.22\times$ end-to-end speedup because RHS was roughly 20% of step time.

**2. Required Lab & Profiling Tasks.** Parallelize the outer loop of M01 GEMM with OpenMP and sweep thread counts under fixed problem size (strong) and scaled problem size (weak):

```bash
gcc -O3 -fopenmp -o gemm_omp gemm_omp.c -lm
for k in 1 2 4 8 16; do
  OMP_NUM_THREADS=$k OMP_PROC_BIND=close OMP_PLACES=cores ./gemm_omp 1024
done
```

Fit the empirical serial fraction $(1 - f)$ from measured runtimes, plot predicted Amdahl speedup against actual speedup, and explain deviations (thread launch overhead, memory contention, or core oversubscription).

**3. Classic References.** Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (6th ed.), Chapter 1 (Fundamentals of Quantitative Design and Analysis); Stanford CS149 Lecture 1–2 (Why Parallelism and Scaling Limits); Amdahl (1967) and Gustafson (1988) original short papers.

**4. ASC Competition Scoring Tips.** HPL behaves closely to weak scaling when $N$ grows with cluster RAM, whereas fixed-mesh scientific simulations and HPCG hit strong-scaling ceilings rapidly. Reporting both strong and weak scaling curves with explicit serial breakdown distinguishes strong preliminary proposals.

---

## M04: Roofline Model & Quantitative Bottleneck Diagnosis

**Stage:** Stage 1, Week 3 Second Half (2026-12-09 to 12-15).

### Slide Title

Roofline Upper Bounds & Hardware-Anchored Diagnosis

### Slide Bullets

- Attainable throughput is bounded by $R \le \min(P_{\mathrm{peak}}, B \cdot I)$, where arithmetic intensity $I = W / Q$ measures FLOPs per byte moved.
- The ridge point $I_b = P_{\mathrm{peak}} / B$ separates the memory-bandwidth slope ($I < I_b$) from the compute ceiling ($I > I_b$).
- Machine ceilings $P_{\mathrm{peak}}$ and sustained $B$ must be measured on the target node rather than copied from vendor marketing slides.
- Optimization follows four ordered steps: count $W$, measure or bound $Q$, plot $(I, R)$ on the Roofline, then edit either data movement or compute.
- Once a kernel sits close to the compute roof, further gains require algorithmic FLOP reduction or shifting effort to outer caller overhead.

### Visual Suggestion

Log-log Roofline plot with measured STREAM Triad bandwidth slope (`#C2410C`), scalar vs. SIMD compute roofs (`#0B4F8A`), vertical ridge line $I_b$, and plotted points for naive GEMM, tiled GEMM, and 2D stencil (`diagrams/png/m04_roofline_model.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** Execution cannot finish faster than either compute time $W / P_{\mathrm{peak}}$ or memory transfer time $Q / B$. Thus $T \ge \max(W / P_{\mathrm{peak}}, Q / B)$, and inverting yields $R = W / T \le \min(P_{\mathrm{peak}}, B \cdot I)$. Roofline is a ceiling model: pipeline stalls, poor instruction mix, or launch latency place real kernels below the roof.

**2. Required Lab & Profiling Tasks.** Measure sustained DRAM bandwidth with STREAM Triad and hardware counters on M01/M02 binaries:

```bash
gcc -O3 -fopenmp -DSTREAM_ARRAY_SIZE=80000000 -o stream stream.c
OMP_NUM_THREADS=16 OMP_PROC_BIND=close ./stream
perf stat -e cycles,instructions,LLC-load-misses,fp_arith_inst_retired.scalar_double ./gemm_o3 1024
perf stat -e cycles,instructions,LLC-load-misses ./stencil 4096
```

Submit a one-page Roofline chart showing exact machine $P_{\mathrm{peak}}$, STREAM $B$, ridge point $I_b$, both plotted kernels, and the concrete next-week optimization target.

**3. Classic References.** Williams, Waterman, & Patterson, "Roofline: An Insightful Visual Performance Model for Multicore Architectures" (*Communications of the ACM*, 2009); Stanford CS149 Lecture on Performance Modeling and Roofline Analysis.

**4. ASC Competition Scoring Tips.** Pair Roofline with time-fraction profiling before editing any finals application. Optimizing a kernel that consumes 15% of runtime yields little score even if it climbs right up to the compute roof.

---

## M05: Multi-Level CPU Parallelism: SIMD, OpenMP & NUMA Pinning

**Stage:** Stage 2, Weeks 4 to 5 (2026-12-16 to 12-29).

### Slide Title

Vector Lanes, OpenMP Threading & False-Sharing Elimination

### Slide Bullets

- AVX2 processes 4 FP64 lanes per vector FMA and AVX-512 processes 8; loop-carried dependencies or pointer aliasing disable auto-vectorization.
- Compiler optimization reports (`-fopt-info-vec-missed` or `-Rpass-missed=loop-vectorize`) pinpoint why loops fail to vectorize before resorting to intrinsics.
- Dynamic or guided OpenMP schedules recover balance on irregular loops where static chunking leaves trailing threads waiting.
- `OMP_PROC_BIND=close` keeps cooperating threads inside one L3/NUMA domain, while `spread` maximizes aggregate memory channels across sockets.
- False sharing occurs when distinct threads write adjacent variables on the same 64-byte cache line, collapsing multicore scaling via coherence traffic.

### Visual Suggestion

Three-layer CPU diagram showing AVX vector lanes inside a core, OpenMP threads across cores with cache-line padding separating per-thread accumulators, and `close` vs. `spread` NUMA socket placement (`diagrams/png/m05_simd_openmp_numa.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** Combining SIMD width $v$ and $p$ physical cores raises theoretical throughput up to $v \cdot p$ times scalar single-core rate only when memory bandwidth and cache coherence hold. When two threads write to `sum[tid]` stored contiguously in an array of 8-byte doubles, up to 8 threads thrash a single 64-byte MESI cache line; padding each slot to `alignas(64)` eliminates coherence invalidations.

**2. Required Lab & Profiling Tasks.** Compare scalar, auto-vectorized, `#pragma omp simd`, and explicit AVX2/AVX-512 intrinsic kernels, plus `close` vs. `spread` pinning and a false-sharing fix:

```bash
gcc -O3 -march=native -fopenmp -fopt-info-vec-missed -o gemm_vec gemm_vec.c -lm
OMP_NUM_THREADS=16 OMP_PROC_BIND=close OMP_PLACES=cores \
  numactl --cpunodebind=0 --membind=0 perf stat -e L1-dcache-load-misses,cache-misses ./gemm_vec 1024
OMP_NUM_THREADS=16 OMP_PROC_BIND=spread OMP_PLACES=cores \
  perf stat -e L1-dcache-load-misses,cache-misses ./gemm_vec 1024
```

Build a deliberate false-sharing reduction benchmark and record wall time before and after 64-byte alignment padding.

**3. Classic References.** MIT 6.172 (*Performance Engineering of Software Systems*), Lectures on Vectorization, Multicore Programming, and Cache-Efficient Algorithms; Bryant & O'Hallaron, *CS:APP* Chapter 5; Intel Intrinsics Guide (instruction reference).

**4. ASC Competition Scoring Tips.** CPU-only finals applications (ASC25 AlphaFold3 and DeepSeek, ASC26 QiboTN and ICON) assign zero points if GPUs run. Clean SIMD inner loops, cache blocking, and verified NUMA pinning directly decide rankings on these tasks.

---

## M06: Distributed-Memory Programming: MPI, Halo Exchange & RDMA Topology

**Stage:** Stage 2, Weeks 6 to 7 (2026-12-30 to 2027-01-12).

### Slide Title

Domain Decomposition, Non-Blocking Halos & Hockney Collectives

### Slide Bullets

- 2D and 3D grid decomposition exchanges only ghost (halo) faces across neighbor ranks, giving a surface-to-volume communication advantage as local subdomain size grows.
- Overlapping interior updates with `MPI_Isend` / `MPI_Irecv` and `MPI_Waitall` hides network latency $\alpha$ behind useful arithmetic.
- Small messages saturate startup latency $\alpha$; large collectives saturate link bandwidth $B$ according to $T(m) = \alpha + m / B$.
- Ring All-Reduce over a $G$-byte buffer across $p$ ranks transfers $2(p - 1)G / p$ bytes per rank across reduce-scatter and all-gather phases.
- Process grids $P \times Q$ should map onto physical sockets and InfiniBand HCAs rather than arbitrary square factorizations.

### Visual Suggestion

2D decomposed grid with highlighted halo strips (`#C48A1A`) paired with a log-log Hockney message-size latency/bandwidth plot separating the $\alpha$-dominated and $B$-dominated regions (`diagrams/png/m06_mpi_halo_hockney.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** A $p$-rank ring All-Reduce partitions $G$ bytes into $p$ chunks of $G/p$ bytes, running $(p - 1)$ steps of reduce-scatter and $(p - 1)$ steps of all-gather. Each rank sends and receives $V_{\mathrm{ring}} = 2 \frac{p - 1}{p} G$ bytes with total latency $2(p - 1)\alpha$ and bandwidth cost $2\frac{p - 1}{p}\frac{G}{B}$. RDMA (InfiniBand HDR/NDR) cuts $\alpha$ by bypassing kernel TCP stacks while per-socket HCAs prevent PCIe/QPI saturation.

**2. Required Lab & Profiling Tasks.** Implement a 2D 5-point stencil with non-blocking halo exchange verified against a serial baseline, then sweep message sizes with `MPI_Allreduce`:

```bash
mpicc -O3 -std=c11 -o halo2d halo2d.c -lm
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./halo2d 2048 200
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./osu_allreduce -m 8:4194304
```

Log the exact network fabric (Ethernet vs. InfiniBand HDR/NDR) and L2 error against the serial run. During Week 7, verify that the faculty advisor received the ASC27 registration confirmation email ahead of the **2027-01-10** midnight UTC+8 deadline.

**3. Classic References.** Gropp, Lusk, & Skjellum, *Using MPI* (3rd ed.), Chapters 3–5 (Point-to-Point, Non-Blocking Communication, Collectives); Stanford CS149 Lecture on Message Passing and Communication Costs; OSU Micro-Benchmarks documentation.

**4. ASC Competition Scoring Tips.** One off-by-one halo corner error fails numerical checks and yields zero points on HPCG, GoMars, AMSS-NCKU, or ICON. In ASC26 finals, Tsinghua paired H100 nodes with dedicated per-socket InfiniBand HCAs to maximize effective HPCG communication bandwidth $B$.

---

## M07: GPU SIMT Architecture & Hand-Written CUDA GEMM Approaching cuBLAS

**Stage:** Stage 2, Week 8 First Half (2027-01-13 to 01-19, paired with M08).

### Slide Title

SIMT Execution, Shared-Memory Tiling & cuBLAS Reference Gap

### Slide Bullets

- GPUs schedule warps (32 threads on NVIDIA, 64-thread wavefronts on AMD) across SMs to hide hundreds of cycles of HBM latency.
- Uncoalesced global loads, shared-memory bank conflicts, and intra-warp branch divergence immediately cut memory throughput and active lanes.
- Naive one-thread-per-output GEMM sits near $I \approx 0.25$ FLOP/byte in FP32 and stalls on HBM bandwidth.
- Tiling $A$ and $B$ into shared memory plus register-level outer products raises arithmetic intensity linearly with tile edge $b$, approaching cuBLAS.
- CUDA and HIP share the same grid/block/shared-memory execution model; portable roofline tuning transfers directly across NVIDIA and AMD GPUs.

### Visual Suggestion

Hierarchical GEMM tiling schematic (global HBM tile $\to$ shared-memory block tile $\to$ per-thread register micro-tile) beside a Roofline progression bar from naive CUDA to shared-memory tiled to vectorized register-tiled vs. cuBLAS (`diagrams/png/m07_cuda_gemm_tiling.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** Loading a $b \times b$ tile of $A$ and $B$ from HBM into shared memory reads $2 b^2$ elements to execute $2 b^3$ FLOPs, boosting HBM arithmetic intensity by a factor of $b / 2$. Adding a $t_m \times t_n$ register micro-tile per thread further cuts shared-memory reads by $t_m t_n / (t_m + t_n)$. Excessive register usage lowers active warps per SM (occupancy), re-exposing latency, so tile sizes must balance reuse against occupancy in `ncu`.

**2. Required Lab & Profiling Tasks.** Implement naive, shared-memory tiled, and register-tiled GEMM kernels and benchmark them against cuBLAS (or `hipcc` + rocBLAS on AMD nodes):

```bash
nvcc -O3 -arch=native -o gemm_naive gemm_naive.cu -lcublas
nvcc -O3 -arch=native -o gemm_tiled gemm_tiled.cu -lcublas
ncu --metrics sm__throughput.avg.pct_of_peak_sustained_elapsed,dram__throughput.avg.pct_of_peak_sustained_elapsed,sm__warps_active.avg.pct_of_peak_sustained_active \
  ./gemm_tiled 4096
```

Verify maximum relative error against cuBLAS before recording % of cuBLAS throughput at $n = 4096$.

**3. Classic References.** NVIDIA *CUDA C++ Programming Guide*, Chapters on Programming Model, Hardware Implementation, and Performance Guidelines (Shared Memory & Coalescing); Stanford CS149 GPU Architecture & Programming Lectures; Simon Boehm's CUDA SGEMM optimization notes (read for tiling progression, benchmarked independently on lab GPUs).

**4. ASC Competition Scoring Tips.** Knowing how to write and read custom kernels enables high-impact fusion (such as Qilu Univ. of Tech. cutting UnifoLM fused op traffic from $8MN$ to $4MN$ bytes and Zhejiang Univ. tiling 3D stencils with `__launch_bounds__` in ASC26 AMSS-NCKU). Always verify whether the bottleneck is kernel speed or host-device transfers first.

---

## M08: Slurm Scheduling, Core Binding & Timeline Profiling (Nsight Systems / Score-P)

**Stage:** Stage 2, Week 8 Second Half (2027-01-13 to 01-19).

### Slide Title

Deterministic Slurm Allocation & Multi-Stream Timeline Diagnosis

### Slide Bullets

- Slurm flags (`-N`, `-n`, `--cpus-per-task`, `--cpu-bind=cores`, `--gres=gpu`) enforce reproducible CPU/GPU affinity rather than relying on OS migration.
- Interactive `salloc` sessions speed up debugging, whereas competition and proposal numbers must come from versioned `sbatch` scripts.
- Nsight Systems (`nsys`) reveals cross-component timeline gaps (H2D copies, host launch stalls, stream barriers); Nsight Compute (`ncu`) inspects single kernels.
- Score-P traces MPI rank wait imbalances and OpenMP synchronization overhead across multi-node CPU and hybrid runs.
- Profiling instrumentation adds overhead; always capture final wall-clock timings with tracing turned off.

### Visual Suggestion

Horizontal multi-track timeline showing CPU host thread, CUDA H2D/Compute/D2H streams before and after pinned-memory async overlap, and an MPI rank trace highlighting wait stalls (`diagrams/png/m08_timeline_profiling.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** Without asynchronous streams and pinned host memory, total step time sums serially: $T_{\mathrm{serial}} = T_{\mathrm{H2D}} + T_{\mathrm{kernel}} + T_{\mathrm{D2H}}$. With page-locked host buffers (`cudaMallocHost`) and chunked streams, steady-state pipeline time drops toward $T_{\mathrm{pipe}} \approx \max(T_{\mathrm{H2D}}, T_{\mathrm{kernel}}, T_{\mathrm{D2H}})$ plus prologue/epilogue startup. On MPI ranks, any load skew turns directly into idle wait at collective barriers, enlarging Amdahl's serial term $(1 - f)$.

**2. Required Lab & Profiling Tasks.** Allocate nodes cleanly with Slurm, capture GPU and MPI traces, and extract summary statistics from CLI:

```bash
salloc -N 1 -n 1 --cpus-per-task=8 --gres=gpu:1 --time=01:00:00
srun --cpu-bind=cores nsys profile --trace=cuda,nvtx,osrt -o gemm_trace ./gemm_tiled 4096
nsys stats --report cuda_gpu_kern_sum,cuda_gpu_mem_time_sum gemm_trace.nsys-rep
scorep mpicc -O3 -o halo2d_sc halo2d.c -lm
srun -N 2 --ntasks-per-node=4 --cpu-bind=cores ./halo2d_sc 2048 200
```

Annotate at least two idle gaps in the `nsys` timeline and identify the slowest MPI rank pair from Score-P output.

**3. Classic References.** SchedMD Slurm Official Documentation (`srun` and `sbatch` CPU/GPU Binding sections); NVIDIA *Nsight Systems User Guide* (CLI Profiling and CUDA Trace); Score-P User Manual (MPI Instrumentation and Cube/Scalasca inspection).

**4. ASC Competition Scoring Tips.** ASC finals prohibit reboots or hardware changes during testing windows (as seen in ASC22 and ASC26). Locking pinning and environment modules inside reproducible launch scripts eliminates last-minute configuration drift and provides clean evidence if judges request a rerun.

---

## M09: Transformer VRAM Budgeting & Mixed-Precision Training (FP16/BF16/FP8)

**Stage:** Stage 3, Week 9 (2027-01-20 to 01-26).

### Slide Title

Parameter, Gradient, Optimizer & Activation Memory Accounting

### Slide Bullets

- Model weights account for only one slice of training VRAM; gradients, FP32 optimizer states, and saved activations dominate peak footprint.
- Mixed-precision Adam holds approximately $16\,\Phi$ bytes of static state per $\Phi$ parameters (2B weights, 2B grads, 4B master weights, 4B momentum, 4B variance).
- Activation memory grows with `batch_size * layers * seq_len * hidden_dim`, independent of parameter sharding unless activation checkpointing recomputes layers.
- FP16's 5-bit exponent underflows small gradients and requires `GradScaler`; BF16 keeps FP32's 8-bit exponent with 7 mantissa bits and generally trains without loss scaling.
- FP8 (E4M3/E5M2) demands hardware Tensor Core support, dynamic scaling factors, and explicit compliance with competition bit-width rules.

### Visual Suggestion

Stacked VRAM breakdown bars comparing FP32 vs. BF16 mixed precision vs. BF16 + activation checkpointing for a concrete Transformer, paired with bit-layout comparison of FP32, FP16, BF16, and FP8 (`diagrams/png/m09_transformer_memory_precision.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** For a Transformer with $\Phi$ parameters, FP32 Adam stores $4\Phi$ bytes each for weights, gradients, first moment $m$, and second moment $v$ ($16\Phi$ bytes total). Mixed-precision training keeps BF16/FP16 forward weights and gradients ($4\Phi$) alongside FP32 master weights and Adam states ($12\Phi$), still totaling $\approx 16\Phi$ static bytes while halving GEMM bandwidth and doubling Tensor Core FLOP/s. Activation memory for attention and FFN scales with $b_{\mathrm{sz}} \cdot L \cdot n_{\mathrm{seq}} \cdot d$; gradient checkpointing trades $\approx 33\%$ extra forward compute to reduce saved activations from $O(L)$ to $O(\sqrt{L})$.

**2. Required Lab & Profiling Tasks.** Build a small PyTorch Transformer script that prints exact `param.numel()` and `torch.cuda.max_memory_allocated()` across FP32, BF16, and activation checkpointing, then deliberately double batch size until OOM:

```bash
python3 train_tiny_gpt.py --dtype fp32 --batch 16 --seq 512 --layers 6 --d_model 512
python3 train_tiny_gpt.py --dtype bf16 --batch 16 --seq 512 --layers 6 --d_model 512
python3 train_tiny_gpt.py --dtype bf16 --batch 16 --seq 512 --layers 6 --d_model 512 --grad_ckpt
python3 train_tiny_gpt.py --dtype bf16 --batch 128 --seq 512 --layers 6 --d_model 512
```

Verify predicted byte totals against PyTorch allocator stats and explain which tensor term triggered the OOM.

**3. Classic References.** Micikevicius et al., *Mixed Precision Training* (ICLR 2018); Korthikanti et al., *Reducing Activation Recomputation in Large Transformer Models* (MLSys 2023, Section 4 memory equations); PyTorch `torch.amp` official documentation.

**4. ASC Competition Scoring Tips.** Always check precision floors before enabling low-bit modes: ASC26 UnifoLM prelim enforced $\ge 16$-bit weights (zeroing an entire scene on violation), and ASC22 Yuan required PyTorch convergence below $\mathrm{Loss} < 7.0$ over 1B tokens.

---

## M10: Distributed Training: DP / FSDP / TP / PP & Ring All-Reduce

**Stage:** Stage 3, Weeks 10 to 11 (2027-01-27 to 02-09).

### Slide Title

Multi-Dimensional Parallelism & Collective Communication Cost

### Slide Bullets

- Data Parallelism (DDP) replicates model state on every GPU and synchronizes gradients via All-Reduce of payload $G$ each step.
- FSDP / ZeRO-3 shards parameters, gradients, and optimizer states across $p$ GPUs, trading All-Gather and Reduce-Scatter collectives for $p\times$ static VRAM capacity.
- Tensor Parallelism (TP) splits intra-layer GEMMs and inserts two All-Reduce operations per Transformer block, requiring fast intra-node NVLink or XGMI.
- Pipeline Parallelism (PP) distributes layers across stages with bubble fraction $(p_{\mathrm{pp}} - 1) / (m + p_{\mathrm{pp}} - 1)$ across $m$ micro-batches.
- Ring All-Reduce transfers $2(p - 1)G / p$ bytes per rank; NCCL (NVIDIA) and RCCL (AMD) map collectives onto the physical topology from M06.

### Visual Suggestion

Four-panel layout comparing DDP, FSDP, TP, and PP memory/communication patterns on 4 GPUs beside the Ring All-Reduce chunk diagram showing $2(p - 1)G / p$ traffic (`diagrams/png/m10_distributed_training_ring.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** In DDP, gradient volume $G = b_g \Phi$ traverses the ring in $2(p - 1)$ steps with per-GPU traffic $V = 2 \frac{p - 1}{p} G$, overlapped via backward bucket hooks (`bucket_cap_mb`). In FSDP, forward All-Gather plus backward All-Gather and Reduce-Scatter move $3 \frac{p - 1}{p} G$ total bytes (1.5x DDP) to fit models exceeding single-GPU HBM. On PCIe servers without NVLink (common in ASC finals nodes with $\le 2$ PCIe GPUs per server), cross-GPU TP stalls on PCIe bandwidth, making DDP/FSDP or sample-level parallelism superior.

**2. Required Lab & Profiling Tasks.** Launch multi-GPU DDP and FSDP runs with `torchrun` and profile collective overlap with `nsys`:

```bash
srun -N 1 --ntasks=1 --gres=gpu:2 --cpus-per-task=8 \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode ddp --seq 512
srun -N 1 --ntasks=1 --gres=gpu:2 --cpus-per-task=8 \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode fsdp --seq 512
NCCL_DEBUG=INFO nsys profile -o ddp_nccl \
  torchrun --standalone --nproc_per_node=2 train_dist.py --mode ddp --steps 10
```

Check `NCCL_DEBUG=INFO` to confirm the active transport (SHM/NVLink/PCIe/IB) and compare measured All-Reduce duration against $2(p - 1)G / (p B_{\mathrm{link}})$. Also verify a minimal 2-GPU column/row TP linear layer matches unsharded forward outputs numerically.

**3. Classic References.** Rajbhandari et al., *ZeRO: Memory Optimizations Toward Training Trillion Parameter Models* (SC 2020); Shoeybi et al., *Megatron-LM* (2019, Section 3 Tensor Parallelism); PyTorch Distributed DDP and FSDP tutorials; NVIDIA NCCL documentation.

**4. ASC Competition Scoring Tips.** ASC22 Yuan 4.7B explicitly required PyTorch distributed training (DeepSpeed/Megatron-LM encouraged) with complete logs containing hyperparameters, random seed, start/end timestamps, and per-step loss/time. Establish structured logging early so every experiment exports proposal-ready CSV/TensorBoard traces.

---

## M11: LLM & World-Model Inference: Prefill/Decode, KV Cache & Denoising Acceleration

**Stage:** Stage 3, Week 12 (2027-02-10 to 02-16).

### Slide Title

Prefill vs. Decode Regimes, KV Cache Growth & Diffusion Speedup

### Slide Bullets

- Autoregressive LLM inference divides into compute-bound prefill (processing all prompt tokens in parallel GEMMs) and memory-bandwidth-bound decode (one token per step).
- KV cache footprint scales as $2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$, turning long-context decode into an HBM/DRAM streaming bottleneck governed by $T(m) = \alpha + m / B$.
- Resident serving, CUDA/HIP graph capture, and compiled execution (`torch.compile`, TensorRT) eliminate repeated model-load and Python dispatch latency.
- Diffusion world models pay $N_{\mathrm{steps}} \cdot T_{\mathrm{step}}$; adaptive step caching (such as TeaCache $\ell_1$ latent gating), operator fusion, and async video encoding cut end-to-end time.
- Every inference shortcut must pass exact task gates (PSNR $\ge 25$ in ASC26 UnifoLM, push success $\ge 90\%$ in LeWorldModel, no banned pruning or cross-run KV reuse).

### Visual Suggestion

Side-by-side timeline contrasting compute-bound Prefill against memory-bound Decode (with growing KV read width per token) plus a diffusion step-skipping schematic showing computed vs. cached steps (`diagrams/png/m11_llm_inference_kv_denoising.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** At decode step $t$, each layer reads all weight matrices ($\approx 2\Phi_{\mathrm{layer}} b_w$ bytes) plus $2 b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$ bytes of cached keys and values to advance $b_{\mathrm{sz}}$ tokens. For $b_{\mathrm{sz}} = 1$, arithmetic intensity sits near $I \approx 1$ FLOP/byte, so time per output token (TPOT) approaches $(M_{\mathrm{weights}} + M_{\mathrm{KV}}) / B_{\mathrm{mem}}$. Quantization shrinks $M_{\mathrm{weights}}$ directly; continuous batching raises $b_{\mathrm{sz}}$ to amortize weight loads. In diffusion models, skipping redundant denoising evaluations cuts $W$ directly while step-level $\ell_1$ thresholds guard perceptual fidelity.

**2. Required Lab & Profiling Tasks.** Measure prefill latency (TTFT), per-token decode latency (TPOT), and allocator delta on a small causal Transformer, plus step-level timing on a lightweight denoising loop:

```bash
python3 bench_infer.py --prompt_len 256 --gen_tokens 128 --dtype bf16
python3 bench_infer.py --prompt_len 1024 --gen_tokens 128 --dtype bf16
nsys profile --trace=cuda,nvtx -o infer_trace \
  python3 bench_infer.py --prompt_len 256 --gen_tokens 32 --dtype bf16
```

Match measured KV memory growth against $2 L b_{\mathrm{sz}} n_{\mathrm{kv}} d_h t b_e$, compare eager execution against `torch.compile` or CUDA Graph replay, and verify exact numerical or MSE tolerance on any cached denoising step.

**3. Classic References.** Pope et al., *Efficiently Scaling Transformer Inference* (MLSys 2023); Kwon et al., *Efficient Memory Management for Large Language Model Serving with PagedAttention* (SOSP 2023); Hugging Face KV Cache documentation; ASC26 team summaries for UnifoLM-WMA-0 (Qilu Univ. of Tech., Shanghai Univ., PKU, BUPT) and LeWorldModel.

**4. ASC Competition Scoring Tips.** Notice how rules shift between rounds: ASC26 UnifoLM locked weights to $\ge 16$-bit in prelims yet unlocked precision, samplers, and step counts in finals while keeping PSNR $\ge 25$. Separating server startup (`/preload`, `/warmup`) from per-case inference and overlapping FFmpeg video writes on RAMDisk (`tmpfs`) produced major real-world gains in ASC26.

---

## M12: Scientific GPU Porting, Bottleneck Shifts & Long-Run Regression (AMSS-NCKU Case)

**Stage:** Stage 3, Week 13 (2027-02-17 to 02-23).

### Slide Title

Compute-to-Transfer-to-Analysis Bottleneck Shifts & 200-Step Verification

### Slide Bullets

- Offloading only the hottest compute kernel onto a GPU often slows down the full program when host-device transfers enter the critical path.
- Tsinghua's ASC26 AMSS-NCKU progression illustrates sequential bottleneck migration: CPU ~4.5 s $\to$ GPU v1 4.7 s (122 roundtrips) $\to$ GPU-resident 1.4 s $\to$ 2+62 core split 1.0 s $\to$ 3-stage relay 0.85 s.
- Keeping all AMR grids resident in GPU HBM eliminates per-step PCIe roundtrips and demands explicit host/device version validity flags.
- Once GPU compute finishes quickly, downstream CPU post-processing creates pipeline backpressure requiring dedicated analysis threads and asynchronous snapshot buffers.
- Short 50-step smoke tests hide stale-copy bugs that diverge by over 60x at 200 steps; long-run regression is mandatory before merging any change.

### Visual Suggestion

Five-bar step-time waterfall showing the AMSS-NCKU optimization stages (labeled as Tsinghua preparation-machine case study) paired with a 3-stage asynchronous GPU-snapshot / D2H / CPU-analysis relay timeline (`diagrams/png/m12_amss_bottleneck_shift.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** When a legacy solver runs 122 host-device pack/copy/unpack cycles per coarse step, total step time becomes $T_{\mathrm{step}} = T_{\mathrm{GPU}} + 122(\alpha_{\mathrm{PCIe}} + m / B_{\mathrm{PCIe}}) + T_{\mathrm{pack}}$, making GPU v1 slower than 64-core CPU (4.7 s vs. 4.5 s). Making grids resident on a single H100 (avoiding PCIe inter-GPU links without NVLink) removes the 122 transfers (1.4 s). Splitting 64 host cores into 2 GPU-driver cores plus 62 OpenMP waveform-extraction cores widens the downstream stage (1.0 s), and triple-buffered asynchronous snapshot relay hides remaining handoff stalls (0.85 s).

**2. Required Lab & Profiling Tasks.** Extend M06 `halo2d` with a deliberately broken host-copy loop and stale-halo bug, then run 50-step vs. 200-step regressions:

```bash
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 50 --copy-each-step
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 200 --resident
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 50 --stale-halo-demo
srun -N 1 -n 4 --cpu-bind=cores ./halo2d --steps 200 --stale-halo-demo
```

Log relative RMS against the serial reference at steps 50 and 200, plus a phased timer breakdown (compute, pack/copy, analysis). Freeze all ASC27 preliminary proposal charts by the end of Week 13 ahead of the **2027-02-28** midnight UTC+8 deadline.

**3. Classic References.** Song Jiaxing (Tsinghua ASC26), *Bringing Black Holes onto GPUs: ASC26 AMSS-NCKU Experience*; ASC26 Optimization Introduction slides on UESTC (task-based packing + memory pool + kernel fusion), Zhejiang Univ. (44,425 s $\to$ 2,376 s, 18.6x prelim $\to$ 30x finals), and PKU (5.50x, RMS $1.9 \times 10^{-9}$); Hennessy & Patterson Chapter 1.

**4. ASC Competition Scoring Tips.** Pair incremental AI-assisted code porting with automated verification: build a rock-solid reference runner and automated RMS/constraint checker first, then commit small verifiable changes (Tsinghua logged 150+ incremental commits).

---

## M13: HPL Benchmark: LU Factorization & Multi-Node Tuning

**Stage:** Stage 4, Weeks 14 to 15 (2027-02-24 to 03-09).

### Slide Title

HPL Matrix Order $N$, Block Size $NB$ & $P \times Q$ Process Grids

### Slide Bullets

- HPL solves dense linear system $Ax = b$ via partial-pivoting LU factorization with leading workload $W = \frac{2}{3}N^3 + 2N^2$ FP64 FLOPs.
- Sustained performance $R_{\max} = W / T_{\mathrm{wall}}$ is meaningful only when HPL's built-in backward residual check prints `PASSED`.
- Larger $N$ raises compute-to-communication ratio until hitting available RAM/HBM (~80% to 90% usable memory without swapping).
- Block size $NB$ trades panel-factorization overhead (small $NB$) against trailing-matrix DGEMM efficiency (larger $NB$).
- Process grid $P \times Q = p$ generally selects $P \le Q$ (nearly square) aligned with node and HCA topology so panel broadcasts minimize hops.

### Visual Suggestion

Blocked LU matrix schematic distinguishing factored region, active panel, and trailing DGEMM update alongside a multi-grid $R_{\max}$ sensitivity chart over $NB$ and $P \times Q$ (`diagrams/png/m13_hpl_panel_scaling.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** At elimination step $k$, updating the trailing $(N - k) \times (N - k)$ submatrix via rank-$NB$ DGEMM requires $2 (N - k)^2 NB$ FLOPs. Summing over $N / NB$ panels gives $W_{\mathrm{LU}} = \frac{2}{3}N^3 + O(N^2)$ FLOPs. Because trailing DGEMM dominates compute while panel factorization and row-swap broadcasts sit on the critical path, efficiency $\eta = R_{\max} / P_{\mathrm{peak}}$ increases with $N$ and degrades if $P$ is too large relative to $Q$.

**2. Required Lab & Profiling Tasks.** Compile or load Netlib HPL linked against optimized BLAS (OpenBLAS/MKL/AOCL or NVIDIA HPC-Benchmarks HPL on GPU nodes) and sweep $NB$ and $P \times Q$:

```bash
# Generate HPL.dat with verified N, NB in {128, 192, 256, 384}, and two P x Q grids
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores ./xhpl | tee hpl_n1_2x4.log
srun -N 2 --ntasks=16 --cpus-per-task=4 --cpu-bind=cores ./xhpl | tee hpl_n2_4x4.log
grep -E "WR|PASSED|FAILED" hpl_n*.log
```

Cross-check reported $R_{\max}$ manually against $\frac{2}{3}N^3 / T_{\mathrm{wall}}$ and reject any run that fails residual verification.

**3. Classic References.** Petitet, Whaley, Dongarra, & Cleary, *HPL: A Portable Implementation of the High-Performance Linpack Benchmark for Distributed-Memory Computers* (`HPL.dat` Tuning Guide); Dongarra, Luszczek, & Petitet, "The LINPACK Benchmark: Past, Present and Future" (*Concurrency and Computation*, 2003).

**4. ASC Competition Scoring Tips.** ASC27 Call for Participation confirms HPL as a finals benchmark and Highest LINPACK as an award, while power limits and exact point formulas remain TBD. In ASC26 finals (5 kW cap), Qilu Univ. of Tech. won Highest LINPACK using a 4-node heterogeneous cluster (6x H200 + 2x AMD W7900D) combined with automated parameter search and tight power capping.

---

## M14: HPCG Benchmark: Sparse Conjugate Gradient & Memory/Comm Tuning

**Stage:** Stage 4, Weeks 16 to 17 (2027-03-10 to 03-23).

### Slide Title

HPCG Sparse Kernels, Bandwidth Ceilings & Sustained-Runtime Discipline

### Slide Bullets

- HPCG models real PDE workloads through preconditioned conjugate gradient (SpMV, symmetric Gauss-Seidel SymGS, multigrid restriction/prolongation, and dot-product `Allreduce`).
- Sparse 27-point stencil operations carry arithmetic intensity near $I \approx 0.25$ FLOP/byte, pinning HPCG onto the memory-bandwidth slope of the Roofline.
- Achieved HPCG GFLOP/s is typically 1% to 5% of HPL $R_{\max}$; both benchmarks expose complementary sides of the same cluster.
- Historical finals discipline (ASC22 official rule) required HPCG 3.0 runtime $\ge 1800$ seconds with Quick Path disabled to prevent transient cache/thermal boosts.
- Balancing local subdomain aspect ratio (`nx, ny, nz`), NUMA memory binding, and per-socket network links determines sustained HPCG score.

### Visual Suggestion

27-point 3D stencil sparsity access pattern paired with a Roofline comparison showing HPL near the compute roof vs. HPCG pinned on the DRAM/HBM bandwidth slope (`diagrams/png/m14_hpcg_spmv_symgs.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** Each row of the 27-point sparse matrix holds up to 27 nonzeros, executing 54 FLOPs while reading 27 FP64 values (216 B), 27 column indices (108 B), and irregular vector elements from $x$, yielding $I < 0.25$ FLOP/byte. SymGS adds triangular loop dependencies requiring multicoloring or hyperplane scheduling for SIMD/GPU concurrency, while global dot products inject synchronous `MPI_Allreduce` latency every iteration.

**2. Required Lab & Profiling Tasks.** Run HPCG with Quick Path disabled (`hpcg.dat` setting target time $\ge 1800$ s for overnight formal `sbatch` and shorter 60 s iterations during class):

```bash
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores ./xhpcg
grep -E "HPCG result is|Final Summary|Total Time|GFLOP/s" HPCG-Benchmark*.txt
srun -N 1 --ntasks=8 --cpus-per-task=4 --cpu-bind=cores \
  perf stat -e LLC-load-misses,cycles,instructions ./xhpcg
```

Confirm the output explicitly states `HPCG result is VALID` and reconcile achieved GFLOP/s against measured STREAM bandwidth multiplied by SpMV arithmetic intensity.

**3. Classic References.** Dongarra, Heroux, & Luszczek, *HPCG Benchmark: A New Metric for Ranking High Performance Computing Systems* (UTK Technical Report, 2015); official `hpcg-benchmark/hpcg` repository documentation.

**4. ASC Competition Scoring Tips.** Tsinghua won ASC26 HPCG under the 5 kW cap by pairing H100 memory bandwidth with dedicated per-socket InfiniBand HCAs so multi-node halo and `Allreduce` traffic stayed uncontended. Always verify the current year's official HPCG runtime requirement once ASC27 finals rules arrive.

---

## M15: Peak Compute Under the Power Wall: DVFS, Historical 3/4/5 kW Stress Tests & Cluster Design

**Stage:** Stage 4, Weeks 18 to 19 (2027-03-24 to 04-06).

### Slide Title

CMOS Power Scaling, DVFS Sweet Spots & Cluster Co-Design

### Slide Bullets

- Dynamic switching power obeys $P_{\mathrm{dyn}} \propto C_{\mathrm{eff}} V^2 f$; modest clock reductions lower voltage and cut watts faster than linear throughput loss.
- 3 kW (ASC22), 4 kW (ASC25), and 5 kW (ASC26) are historical stress-test baselines; the official ASC27 power cap and node limits are still TBD.
- Adding extra GPUs boosts HPL peak FLOP/s while consuming rack wattage and potentially hurting CPU-only or memory/interconnect-heavy workloads.
- Power must be sampled at the wall/PDU or BMC/IPMI/GPU telemetry under live steady load; subtracting idle power misrepresents rack-meter compliance.
- Exceeding the on-site power wall invalidates the running task in ASC finals, so every tuned launch script needs a verified safety margin.

### Visual Suggestion

Measured $R_{\max}$ vs. total system power curve with vertical dashed reference lines at 3 kW (ASC22), 4 kW (ASC25), and 5 kW (ASC26) labeled "Historical Stress-Test Baselines (ASC27 TBD)" (`diagrams/png/m15_power_wall_dvfs.png`). Use `#0D9488` for compliant operating points and `#C2410C` for over-cap points.

### Speaker Notes & Lab

**1. First-Principles Derivation.** Dynamic power scales as $P_{\mathrm{dyn}} \propto C_{\mathrm{eff}} V^2 f$, while static leakage, fans, switches, and storage add a fixed base floor $P_{\mathrm{static}}$. Under a fixed total cap $P_{\max}$, available compute power is $P_{\max} - P_{\mathrm{static}}$, so minimizing idle node count and switch overhead frees watts for active silicon. On GPUs, setting `nvidia-smi -pl` or ROCm power caps shifts execution onto the flat efficiency knee where FLOP/W peaks.

**2. Required Lab & Profiling Tasks.** Record live power telemetry alongside an HPL or GEMM load across at least three power/frequency caps permitted on lab hardware:

```bash
# Query GPU power caps and read telemetry in a side monitor (adjust permissions per cluster policy)
nvidia-smi --query-gpu=timestamp,index,power.draw,clocks.sm,temperature.gpu --format=csv -l 1 > gpu_pwr.csv &
MON_PID=$!
srun -N 1 --ntasks=1 --gres=gpu:2 --cpu-bind=cores ./xhpl
kill $MON_PID
# Host BMC / RAPL telemetry where permitted:
ipmitool dcmi power reading || cat /sys/class/powercap/intel-rapl:0/energy_uj
```

Plot GFLOP/s and GFLOP/W across tested caps, clearly recording sensor scope (GPU-only vs. full-node BMC) and avoiding unverified extrapolation beyond physical lab wattage.

**3. Classic References.** Hennessy & Patterson, *Computer Architecture: A Quantitative Approach* (6th ed.), Chapter 1 (Trends in Power and Energy in Integrated Circuits); Intel RAPL / NVIDIA NVML / AMD `rocm-smi` power-capping manuals; ASC22 Final Notification Appendix I and ASC26 cluster statistics (99 servers, 174 GPUs across 25 teams).

**4. ASC Competition Scoring Tips.** Cluster design in preliminary proposals must justify node count, CPU sockets, GPU count, interconnect, and power headroom across both compute-bound (HPL/AI) and bandwidth-bound (HPCG/CPU-only) workloads. Once ASC27 publishes official rack wattage and node caps, swap the vertical reference lines without altering the tuning procedure.

---

## M16: Mystery-App Rapid Profiling, Reproducible Evidence Chains & English Proposal / Poster Defense

**Stage:** Stage 4, Weeks 20 to 24 (2027-04-07 to 05-11).

### Slide Title

48-Hour Mystery-App Triage, Evidence Packaging & Committee Defense

### Slide Bullets

- The first 90 minutes of any mystery application establish three facts: clean build recipe, input/output and accuracy gate, and hotspot wall-time share.
- Lock a passing reference run before editing code; if an edit breaks verification or exceeds power, a single rollback script restores the last valid submission.
- Every claim in an English proposal or poster maps directly to an `evidence/` bundle holding git commit hashes, launch commands, raw logs, power traces, and accuracy diffs.
- Proposals undergo strict similarity screening (plagiarism yields zero points), requiring original technical prose backed by raw team experiments.
- Rehearse a timed 10-minute two-speaker English presentation plus 3 to 5 minutes of Q&A (following historical ASC22 defense timing until ASC27 finalizes exact slots) and cross-university patch exchange workflows for Group Competition.

### Visual Suggestion

48-hour competition triage workflow diagram (Build $\to$ Reference Run $\to$ Profile $\to$ Verify-Gated Optimization Loop $\to$ Freeze & Rollback $\to$ Evidence Bundle $\to$ Poster/Q&A) paired with the 5-file `evidence/` directory tree (`diagrams/png/m16_asc_workflow_scoring.png`).

### Speaker Notes & Lab

**1. First-Principles Derivation.** M16 unifies L1–L4 into an auditable engineering workflow: Roofline (`C2`) selects where to optimize, Amdahl's fraction (`C1`) predicts maximum return, RMS/constraint gates (`C3`) accept or reject edits, and reproducible packaging (`E3`) converts runtime gains into competition credit.

**2. Required Lab & Profiling Tasks.** Run a timed 90-minute mystery drill on an unseen C++/MPI or PyTorch solver released by seniors at Wednesday kickoff, building a clean `evidence/` folder:

```bash
perf record -F 99 -g -- ./mystery_app --steps 20
perf report --stdio --sort=dso,symbol | head -n 40
srun --cpu-bind=cores ./mystery_app --steps 200 > evidence/02-ref.log
diff -u evidence/02-ref.log evidence/opt.log
```

Required directory layout for Weeks 20 to 24:

```text
evidence/
  00-build.md        # exact compiler, modules, git commit, build flags
  01-profile.txt     # perf / nsys / Score-P hotspot breakdown
  02-ref.log         # reference output and accuracy tolerance
  03-run.sh          # single reproducible submission command + rollback target
  04-result.md       # wall time, speedup, accuracy pass, live power, math-equivalence note
```

During Week 23, two student speakers deliver a timed 10-minute English slide/poster rehearsal and answer 8 prepared Q&A probes covering mathematical equivalence, roofline limits, and failed optimization branches. Week 24 executes a compressed 48-hour mock finals sprint ending 2027-05-11 (or earlier if official May finals dates dictate).

**3. Classic References.** *2027 ASC Student Supercomputer Challenge Call for Participation* (official proposal, poster, and presentation expectations); *ASC22 Final Competition Notification* Appendix II (historical rules on mathematical equivalence, ban on input-specific hacks, 10-minute English presentation, and cross-university group rules); *ASC26 Optimization Introduction* slides on similarity screening and ICON Group Competition collaboration.

**4. ASC Competition Scoring Tips.** Split presentation slides cleanly between algorithmic/mathematical changes (with proof of equivalence) and systems/runtime optimizations (binding, memory pools, async I/O, power capping). Judges routinely probe whether speedups generalize beyond test inputs; presenting negative ablations alongside winning commits demonstrates engineering rigor.
