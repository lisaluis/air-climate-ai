# Air & Climate AI: when weather, not just emissions, drives pollution

Open Book Lab Exam, **Assignment C**. Article: *"Study traces how an El Niño changed the pollution map"* (Times of India, with the related IMD/IITM climate-zone study).

## 1. Problem definition
> **How should pollution and agriculture policy adapt when weather, not just emissions, drives outcomes?**

Winter PM2.5 flipped between 2022-23 (La Niña: north India up to 30% cleaner, Mumbai up 45%) and 2023-24 (El Niño: Jaipur up about 50%, Delhi over 10%, peninsula cleaner) with no major change in emissions or policy. Separately, the hot semi-arid zone has spread east into Uttar Pradesh over 70 years. Scope for 3 hours: explain this clearly (website), answer questions about it reliably (fine-tuned small LLM), and propose evidence-graded policy options with trade-offs (agent). Key issues covered: weather-driven variability, limits of local emission control, regional air transport, shifting climate zones and agriculture.

## 2. Technology stack
| | Task 1: Website | Task 2: Fine-tuned LLM | Task 3: Policy agent |
|---|---|---|---|
| Core | HTML, CSS, JavaScript (no build, no chart library) | Qwen2.5-3B-Instruct (1.5B fallback), SFT with QLoRA via TRL | Python, Groq API (`openai/gpt-oss-120b`, JSON mode), Flask |
| Quantization | n/a | 4-bit NF4, double quantization, fp16 compute | n/a |
| LoRA | n/a | r=16, alpha=32, dropout 0.05, all attention + MLP projections | n/a |
| Compute | Browser | Colab T4 GPU (~15 GB); peak memory: *fill from `nvidia-smi`* | CPU; model runs on Groq servers |
| UI | The site itself (`index.html`) | Gradio chat in Colab (`share=True`) | `agent.html` served by Flask; runs on a laptop or in Colab |
| Testing | `node --check`, browser check | Held-out evaluation, base vs fine-tuned | pytest with a fake LLM; GitHub Actions |
| Tools / MCP / skills | AI coding assistant (Cursor/Copilot) for iteration | Hugging Face `transformers`, `peft`, `trl`, `bitsandbytes` | No MCP servers or skills used (not needed; facts are a local file) |

## 3. Design principles
- **Website:** DRY (`data.js` is the only place numbers live), orthogonality (data / structure / style / behaviour in separate files, one function per block), small iterations (one commit per block), documentation (source under every chart, `SPEC.md`). Design: one memorable interaction (the winters flip), colour used only to carry meaning (teal cleaner, amber dirtier), accessible and responsive.
- **LLM:** small and cheap (4-bit + LoRA on a free GPU); honest evaluation on held-out *phrasings never seen in training*; "I am not sure" examples to reduce made-up numbers; no secrets in notebooks.
- **Agent:** evidence-grounded (cites fact ids, invented ids rejected), validated structured output with retries, mandatory trade-offs, evidence strength stated, findings kept apart from proposals, human-in-the-loop, logic separate from the web layer and tested without a key.
- **Honesty:** where the article gives no figure the site shows a hatched "direction only" bar, never an invented number.

## 4. Repository layout
```
website/      Task 1  explainer + agent page (HTML, CSS, JS)   -> website/README.md
llm/          Task 2  data builder, train.ipynb, chat_ui.ipynb -> llm/README.md
agent/        Task 3  agent.py, facts.json, agent_colab.ipynb, tests -> agent/README.md
app.py        Flask app: serves the website and runs the agent
tests/        route tests         screenshots/  evidence         PREPARATION.md  homework
```

## 5. Run it
**Website only:** open `website/index.html` in a browser.
**Website + agent (laptop):** `pip install -r requirements.txt`, set `GROQ_API_KEY`, `python app.py`, open http://localhost:5000 and `/agent`.
**Colab (no setup on your machine):**
| What | Notebook | GPU |
|---|---|---|
| Train + evaluate + chat UI | `llm/train.ipynb` | T4 |
| Chat UI from a saved adapter | `llm/chat_ui.ipynb` | T4 |
| Policy agent website | `agent/agent_colab.ipynb` | none |

Before first use, replace `YOUR-USERNAME` in `website/data.js` and the three notebooks with your GitHub username. Tests: `pip install -r requirements.txt -r requirements-dev.txt && pytest`.

## 6. Output and honest status
Fill this in from what you actually ran.
- Screenshots in `screenshots/`: website (both winters), before/after LLM answers, `nvidia-smi`, held-out score, LLM chat UI, agent UI (3 questions).
- Held-out score: base ___ -> fine-tuned ___. Training time ___, final loss ___, peak GPU memory ___ GB.
- [ ] Website  [ ] Fine-tune + evaluation  [ ] LLM chat UI in Colab  [ ] Agent UI in Colab  [ ] GitHub Pages link
- Known limits: the ENSO findings come from two winters and are correlational; city bars without a stated figure show direction only; background standards (WHO, NAAQS, NCAP) are marked VERIFY in `facts.json`; the training set is small (see `llm/README.md`).
