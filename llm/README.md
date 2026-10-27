# Air-Quality & Climate Assistant (Task 2: SFT + QLoRA)
Small LLM fine-tuned to explain ENSO, PM2.5, pollution meteorology and India's shifting climate zones, and to say "I am not sure" outside its knowledge.

## Problem
Generic models answer in generic terms (or invent numbers) about the 2022-24 ENSO pollution flip and the climate-zone study. Goal: a cheap model that answers from the article's facts and admits gaps.

## Run (Colab, free T4)
1. Upload `train.ipynb` to colab.research.google.com, Runtime > T4 GPU, Run all (it clones this repo for the data; set `REPO` first).
2. Step 10 opens a Gradio chat with a public link: screenshot it.
3. Later demos without retraining: `chat_ui.ipynb` (set `ADAPTER`).

## Stack
Qwen2.5-3B-Instruct (change `MODEL_ID` for 1.5B), SFT with TRL `SFTTrainer`, QLoRA: 4-bit NF4 + double quant + fp16 compute, LoRA r=16 alpha=32 on all projections, 4 epochs, lr 2e-4, effective batch 8, Gradio UI. Compute: Colab T4. Memory and time: *fill from the notebook (`nvidia-smi`, trainer log)*.

## Dataset
- `build_dataset.py` -> `air_climate.jsonl` (155 train pairs) and `heldout_test.jsonl` (17). Source: the two TOI articles (exact figures) plus a few background standards (WHO, NAAQS, NCAP) marked VERIFY. Each fact is asked in several phrasings, plus out-of-scope questions answered with "I am not sure".
- One phrasing of every fact is held out entirely, so the test checks new wording, not memorised strings.
- **To make it stronger (recommended, 30 min):** (1) paste article or agency text into an LLM with: *"Write 40 Q&A pairs, each fact in 3 phrasings, 5 questions whose answer is not in the text must say you are not sure, use only facts in the text; output one JSON per line {messages:[system,user,assistant]}"*; (2) spot-check 10 answers against the source; (3) optionally mix a public Hugging Face Q&A set by setting `HF_EXTRA` in the notebook (check licence and sample rows first); (4) retrain.

## Evaluation (held-out)
Score = share of the numbers in the reference answer that the model reproduces ("not sure" references score 1 only if the model also says so; text-only references are skipped). Base is scored with the adapter switched off.
| Model | Mean score |
|---|---|
| Base | ___ |
| Fine-tuned | ___ |

Limits: 17 questions is a small sample, number matching ignores whether a number is attached to the right meaning, and the held-out questions test the same facts in new wording, not new facts. Read the answers yourself too.

## Design principles
Honest held-out evaluation; small and cheap; fewer made-up answers via "not sure" examples; reproducible single notebook; no secrets in code.

## Results and failures
Before: *describe what the base model said*. After: *describe what changed and which facts it still gets wrong*. Screenshots: `../screenshots/`.
