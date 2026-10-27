"""Air-quality & climate policy agent: question -> facts lookup -> policy generation -> validated JSON.
Setup:  pip install groq ; export GROQ_API_KEY="..."   (Colab: use a userdata secret, never commit keys)
Run:    python agent.py "How should policy adapt when weather drives pollution?"   (--json for raw JSON)
Tests:  pip install pytest && pytest
"""
import json, os, re, sys

MODEL = os.environ.get("GROQ_MODEL", "openai/gpt-oss-120b")
POLICIES = ["ENSO-aware seasonal pollution forecasting",
            "Regional (airshed-level) action plans across state borders",
            "Crop-calendar advisories for farmers"]
REQUIRED = ["policy", "justification", "evidence", "expected_impact", "trade_offs",
            "implementation_difficulty", "evidence_strength"]
DIFFICULTY = {"low", "medium", "high"}
STRENGTH = {"strong", "moderate", "weak"}

SYSTEM = """You are a policy analyst advising Indian central and state governments on air quality and climate.
Rules:
1. Use ONLY the numbered facts provided. Never invent statistics. Cite fact ids (e.g. F5) in 'evidence'.
2. Keep two things apart: what the studies FOUND (facts) and what you PROPOSE (your policy options). Never say a study recommends a policy.
3. Every policy MUST have at least 2 trade_offs (cost, equity, feasibility, political or data risks).
4. The studies are correlational and cover two winters: reflect that in 'evidence_strength' (strong|moderate|weak) and say so in expected_impact. Do not promise numeric reductions.
5. These are options for human decision-makers, not decisions.
Return ONLY a JSON object: {"issue_analysis": "2-3 sentences", "policies": [ {policy, justification,
evidence (list of strings with fact ids), expected_impact, trade_offs (list), implementation_difficulty (low|medium|high),
evidence_strength (strong|moderate|weak)} ]}"""

def load_facts(path=os.path.join(os.path.dirname(__file__), "facts.json")):
    return json.load(open(path, encoding="utf-8"))

def validate(data, valid_ids):
    """Check the model's JSON. Raises ValueError with a clear reason (used to trigger a retry)."""
    policies = data.get("policies")
    if not isinstance(policies, list) or len(policies) != len(POLICIES):
        raise ValueError(f"expected {len(POLICIES)} policies")
    for i, p in enumerate(policies, 1):
        missing = [k for k in REQUIRED if k not in p]
        if missing:
            raise ValueError(f"policy {i}: missing {missing}")
        if not isinstance(p["trade_offs"], list) or len(p["trade_offs"]) < 2:
            raise ValueError(f"policy {i}: at least 2 trade-offs required")
        if str(p["implementation_difficulty"]).lower() not in DIFFICULTY:
            raise ValueError(f"policy {i}: difficulty must be low, medium or high")
        if str(p["evidence_strength"]).lower() not in STRENGTH:
            raise ValueError(f"policy {i}: evidence_strength must be strong, moderate or weak")
        cited = set(re.findall(r"F\d+", " ".join(map(str, p["evidence"]))))
        if not cited:
            raise ValueError(f"policy {i}: no fact ids cited")
        unknown = cited - set(valid_ids)
        if unknown:
            raise ValueError(f"policy {i}: cites unknown facts {sorted(unknown)}")
    return data

def run(question, client, retries=2):
    """Ask the LLM, validate, and retry (telling the model what was wrong) if the checks fail."""
    facts = load_facts()
    ids = [f["id"] for f in facts]
    fact_text = "\n".join(f"{f['id']}: {f['fact']} [{f['source']}]" for f in facts)
    user = f"Question: {question}\n\nFacts:\n{fact_text}\n\nCover exactly these policies:\n- " + "\n- ".join(POLICIES)
    messages = [{"role": "system", "content": SYSTEM}, {"role": "user", "content": user}]
    last_error = None
    for _ in range(retries + 1):
        r = client.chat.completions.create(model=MODEL, temperature=0.2,
                                           response_format={"type": "json_object"}, messages=messages)
        content = r.choices[0].message.content
        try:
            return validate(json.loads(content), ids)
        except (ValueError, json.JSONDecodeError) as e:
            last_error = e
            messages = messages + [{"role": "assistant", "content": content},
                                   {"role": "user", "content": f"Your answer failed validation: {e}. Fix it and return the full JSON again."}]
    raise RuntimeError(f"Agent output failed validation after {retries + 1} attempts: {last_error}")

def show(data):
    print("\nISSUE ANALYSIS:", data.get("issue_analysis", ""), "\n")
    for i, p in enumerate(data["policies"], 1):
        print(f"{i}. {p['policy']}  [difficulty: {p['implementation_difficulty']}, evidence: {p['evidence_strength']}]")
        print("   Why:       ", p["justification"])
        print("   Evidence:  ", "; ".join(p["evidence"]))
        print("   Impact:    ", p["expected_impact"])
        print("   Trade-offs:", " | ".join(p["trade_offs"]), "\n")

if __name__ == "__main__":
    from groq import Groq
    args = sys.argv[1:]
    q = " ".join(a for a in args if a != "--json") or "How should pollution and agriculture policy adapt when weather, not just emissions, drives outcomes?"
    result = run(q, Groq(api_key=os.environ["GROQ_API_KEY"]))
    print(json.dumps(result, indent=2, ensure_ascii=False)) if "--json" in args else show(result)
