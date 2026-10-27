# Preparation (homework) checklist
Shows what was set up before the exam. Tick what you actually did.
- [ ] Colab opened, T4 GPU confirmed, `HF_TOKEN` (write) and `GROQ_API_KEY` stored as Colab secrets
- [ ] GitHub repo created, cloned, one test push done; GitHub Pages tried
- [ ] Base models shortlisted: Qwen2.5-1.5B-Instruct (fast), Qwen2.5-3B-Instruct (better), Llama-3.2-1B/3B-Instruct (alternative; needs licence acceptance)
- [ ] Datasets shortlisted: own Q&A built from the article and agency pages (this repo); search the Hugging Face Hub for climate / environmental-science Q&A and check licence + 10 sample rows before use
- [ ] `train.ipynb` run once end to end on practice data; known T4 fixes applied (fp16 + fp32 LoRA weights)
- [ ] Sample agent run; `facts.json` format and validation rules rehearsed
- [ ] Website template and design plan (`website/SPEC.md`) ready

## Exam-day plan (3 hours)
| Time | Do |
|---|---|
| 0:00-0:20 | Repo + facts file from the article; start dataset build |
| 0:20-0:40 | Start Colab training (runs in the background) |
| 0:40-1:40 | Website in small prompts, commit after each |
| 1:40-2:20 | Agent + its page, run 3 questions |
| 2:20-2:40 | Chat UI, held-out score, screenshots |
| 2:40-3:00 | README (honest status), push, submit link |

## Swapping to another assignment
Change only: `agent/facts.json`, `POLICIES` in `agent.py`, the facts list in `llm/build_dataset.py`, and `website/data.js` plus section text. Training notebook, Flask app, tests and agent page stay the same.
