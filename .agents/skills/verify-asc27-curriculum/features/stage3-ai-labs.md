# Stage 3: AI Systems & GPU Porting

Stage 3 (`site/stage3-ai-systems.html`) visualizes Transformer training VRAM (`#vram`), 4-GPU Ring All-Reduce (`#ring`), LLM KV-cache decode bottleneck (`#kv`), and the ASC26 AMSS-NCKU GPU porting waterfall (`#amss`).

## Sub-features

- `s3-vram` adjusts parameters (`#vr-p`), batch/seq multiplier (`#vr-b`), FSDP GPUs (`#vr-g`), and activation checkpointing (`#vr-ck-off`/`#vr-ck-on`), updating `#vr-bars`, `#vr-tot`, `#vr-40`, and `#vr-80`.
- `s3-ring` steps through 6 Ring All-Reduce steps (`#rg-next`, `#rg-play`, `#rg-reset`), updating `#rg-phase`, `#rg-vol`, and chunk states in `#rg-svg`.
- `s3-kv` sweeps sequence length (`#kv-t`), batch (`#kv-b`), and weight precision (`#kv-bf16` vs. `#kv-int4`), updating `#kv-mem`, `#kv-tpot`, `#kv-tps`, and `#kv-svg`.
- `s3-amss` clicks through the optimization stage buttons in `#amss-btns`, updating `#amss-svg` and `#amss-msg`.

## How to get to it (user POV)

- Click `Stage 3: AI & Porting` in the top nav bar.
- Click the `AI Systems & GPU Porting` stage card on `index.html`.
- Follow deep links `stage3-ai-systems.html#vram`, `#ring`, `#kv`, or `#amss`.

## Driving it with cua_repl (iab)

Preconditions:

- `serve-site.sh doctor` reports `OK:` for `http://127.0.0.1:<port>`.
- Evidence directory `/tmp/asc27-verify-evidence/$RUN_ID/stage3/` exists.

- **Open Stage 3.** Navigate to `http://127.0.0.1:<port>/stage3-ai-systems.html`. All 4 lab sections render cleanly.
- **Drive VRAM Calculator.** At default (`4.7B`, `1 GPU`, checkpointing off), `#vr-40` and `#vr-80` show `OOM`. Set `#vr-g` to `4` (dispatch `input`) and click `#vr-ck-on`; `#vr-tot` drops below 40 GB and `#vr-40` flips to `Fits`.
- **Drive Ring All-Reduce.** Click `#rg-next` 6 times from `Step 0 / 6` to `Step 6 / 6`. `#rg-phase` transitions `Initial` -> `Reduce-Scatter` (steps 1–3) -> `All-Gather` (steps 4–5) -> `Complete` (step 6), and `#rg-vol` reaches `1.50 G`. Inspect `#rg-svg`: verify whether all 16 chunk cells show `ALL` at step 6 (see Gotchas).
- **Drive KV Cache & AMSS.** Toggle `#kv-int4` and confirm `#kv-tpot` drops and `#kv-tps` rises. Click two buttons in `#amss-btns` and confirm `#amss-msg` and `#amss-svg` update.
- **Check pedagogy.** Verify each widget connects directly to its core formula (`16P` static bytes, `2((p-1)/p)G`, decode bandwidth bound) with short takeaways instead of repeating `slides/pdf/03-stage3-ai-systems.pdf`.
- **Proof.** Save screenshots to `/tmp/asc27-verify-evidence/$RUN_ID/stage3/` and record `#vr-tot`, `#rg-step-val`, and chunk labels at step 6.

## Gotchas

- At step 3 (end of Reduce-Scatter), each GPU must show exactly one `ALL` chunk (4 distinct chunks across the 4 GPUs); at step 6 (`Complete`), all 16 chunk cells across the 4 GPUs must show `ALL`.
