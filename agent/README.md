# Policy agent (Task 3)
Analyses the article's issues and proposes **three evidence-graded policy options with justification and trade-offs**: ENSO-aware seasonal forecasting, airshed-level action plans, crop-calendar advisories.

## Workflow
question -> load `facts.json` (18 sourced facts, ids F1..F18) -> LLM drafts JSON -> `validate()` checks it -> retry with the exact error if it fails -> web page / table.

Schema per policy: `policy, justification, evidence (fact ids), expected_impact, trade_offs (>=2), implementation_difficulty, evidence_strength`.
Checks: exactly 3 policies, all fields present, at least 2 trade-offs, difficulty and strength from fixed sets, every cited id exists (invented ids rejected).

## Run
- Laptop: `pip install -r ../requirements.txt`, set `GROQ_API_KEY`, `python agent.py "your question"` or `python ../app.py` then open `/agent`.
- Colab: `agent_colab.ipynb` (no GPU; key in Colab secret `GROQ_API_KEY`); it shows the agent page inside the notebook. Screenshot 3 different questions.
- Tests (no key, no internet): `pytest` from the repo root.

## Stack
Python, Groq API (`openai/gpt-oss-120b`, JSON mode), Flask, pytest with a fake LLM, GitHub Actions. No MCP servers or skills.

## Design principles
Evidence-grounded (only `facts.json`, ids cited); findings kept apart from proposals; structured, validated output; trade-offs mandatory; evidence strength stated because the studies cover two winters and are correlational; human-in-the-loop (options, not decisions); logic separate from the web layer.

## Limits
Citation checks prove an id exists, not that the reasoning is right; a human must read the output. Background facts F16-F18 are marked VERIFY. The agent is only as good as its 18 facts: add more sourced facts to improve it.
