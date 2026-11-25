---
name: verify-formal-ring-allreduce
description: "Formally verify the Ring All-Reduce state machine (site/stage3-ai-systems.html:getRingState) and the core HPC physics formulas (Amdahl, Roofline, Qubit memory wall, DVFS) using exhaustive JS execution + Z3 SMT proofs. Use when editing interactive lab math, ring/collective animations, or slider formulas."
---

# Formal Verification: Ring All-Reduce & Core Physics Invariants

This skill checks the mathematical and state-machine promises that `asc27-curriculum` teaches beginners. A silent error in a teaching simulator teaches the wrong mental model (for example, claiming Ring All-Reduce completes in 6 steps while leaving chunks unreduced, or claiming a memory-bound kernel is compute-bound).

## Covered Code & Sync Record

- **Sync commit:** `1290290`
- **Covered files and functions:**
  - `site/stage3-ai-systems.html`: `getRingState(step)` (Ring All-Reduce 4-GPU, 4-chunk state machine)
  - `site/stage1-foundations.html`: `drawAmdahl()` (Amdahl/Gustafson formulas), `drawRoofline()` (Roofline ridge point & regime)
  - `site/stage4-asc-sprint.html`: `drawQubit()` (`16 * 2^n` binary memory law), `clusterStats(gpus, freq)` (DVFS power/throughput monotonicity)

Before relying on a pass, check whether any covered file changed since the sync commit:

```bash
git diff --stat 1290290..HEAD -- site/stage1-foundations.html site/stage3-ai-systems.html site/stage4-asc-sprint.html
```

Only move the sync commit forward after confirming that `scripts/verify_curriculum_invariants.py` still describes the actual code at the new commit.

## Properties Verified (Plain Language)

1. **Ring All-Reduce completion (`ring_allreduce_js`):** Starting from 4 GPUs each holding 4 local chunks, after step 3 (end of Reduce-Scatter) every GPU must hold exactly 1 fully reduced chunk (all 4 distinct), and after step 6 (end of All-Gather) every GPU must hold all 4 fully reduced chunks (`ALL`).
   - *Harm if broken:* Beginners watch an animation that prints "Complete" while chunks are still partial (`c0`..`c3`), breaking their intuition for how Ring All-Reduce works.
2. **Amdahl ceiling & Gustafson dominance (`z3_amdahl_gustafson`):** Over the full continuous slider domain `f in [0.5, 0.995]`, `k in [1, 128]`, strong-scaling speedup always stays in `[1, 1/(1-f))` and never exceeds weak-scaling Gustafson speedup.
   - *Harm if broken:* Learners see impossible speedups above the serial ceiling `1/(1-f)`.
3. **Roofline ridge-point soundness (`z3_roofline`):** Over `P in [2, 100]`, `B in [0.2, 5.0]`, `I in [0.1, 160]`, `I < P/B` implies `R = B * I < P` (Memory-bound) and `I >= P/B` implies `R = P <= B * I` (Compute-bound).
   - *Harm if broken:* The ridge point `I_b` and regime label disagree with the plotted roofline.
4. **Qubit binary memory law (`z3_qubit_memory`):** For every integer `n in [10..44]`, `16 * 2^n == 2^(n+4)` with exact binary anchors `20q = 16 MiB`, `30q = 16 GiB`, `40q = 16 TiB`.
   - *Harm if broken:* Reintroduces the 1024x unit error the curriculum explicitly corrects.
5. **DVFS efficiency knee (`z3_dvfs_monotonicity`):** Over `gpus in [2, 10]` and `0.5 <= f1 < f2 <= 1.0`, raising clock ratio strictly raises both dynamic power and FP64 throughput while strictly lowering dynamic FLOP/W.
   - *Harm if broken:* The DVFS curve contradicts why lowering clock under a power cap beats removing GPUs.

## Tool & Scope

- **Tools:** `node` (executes the exact `getRingState` function extracted from `site/stage3-ai-systems.html` across all `(step, gpu, chunk)` states) and `z3` (`QF_NRA` nonlinear real arithmetic SMT solver for continuous formula domains).
- **What is NOT covered:** Visual layout/CSS overlap, SVG coordinate clipping, browser event wiring (covered by `verify-asc27-curriculum`), or prose/slide wording.

## Run the Check

```bash
python3 .agents/skills/verify-formal-ring-allreduce/scripts/verify_curriculum_invariants.py
```

Use `--json` for machine-readable output. Exit code `0` means all 5 checks passed; exit code `1` means at least one invariant failed with a concrete counterexample.

## Interpreting Failures & Updating the Verification

- **Real bug vs. modeling error:**
  - For `ring_allreduce_js`, the script runs the *actual* JS function from `site/stage3-ai-systems.html`. A failure is a real bug in `getRingState` unless the HTML intentionally changed the ring size (`p != 4`) or chunk encoding (`4 != ALL`).
  - For the `z3_*` checks, if a formula expression changed intentionally (for example, changing the DVFS exponent or slider range), update the matching assertion and expression guard in `scripts/verify_curriculum_invariants.py`, re-run, and confirm the check still fails on a deliberately broken variant.
- **Findings stay findings:** Never weaken an invariant to make broken code pass.

## Current Known Finding (at sync commit `eb56d34`)
## Baseline Status

All 5 invariants pass at sync commit `1290290` (`getRingState(step)` accumulates `prev[recvFrom][chunk] + 1` during Reduce-Scatter so step 3 finishes 1 distinct `ALL` chunk per GPU, and forwards `prev[recvFrom][(recvFrom + 1 - k + 4) % 4]` during All-Gather so step 6 finishes all 16 chunks).
