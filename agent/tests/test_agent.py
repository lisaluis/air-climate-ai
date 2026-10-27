"""Unit tests: no network, no API key. The LLM is replaced by a fake client.  Run: pytest"""
import copy, json, os, sys
import pytest

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import agent

IDS = [f["id"] for f in agent.load_facts()]

def good_policy(n=0):
    return {"policy": agent.POLICIES[n], "justification": "because", "evidence": ["F5", "F7"], "evidence_strength": "moderate",
            "expected_impact": "qualitative", "trade_offs": ["cost", "equity"], "implementation_difficulty": "medium"}

def good_data():
    return {"issue_analysis": "ok", "policies": [good_policy(i) for i in range(len(agent.POLICIES))]}

class FakeClient:
    """Returns the queued answers in order and counts how often it was called."""
    def __init__(self, answers):
        self.answers, self.calls = list(answers), 0
        self.chat = self; self.completions = self
    def create(self, **kwargs):
        content = self.answers[min(self.calls, len(self.answers) - 1)]
        self.calls += 1
        msg = type("M", (), {"content": content})
        return type("R", (), {"choices": [type("C", (), {"message": msg})]})

# ---- data quality ----
def test_facts_have_unique_ids_and_sources():
    facts = agent.load_facts()
    assert len(IDS) == len(set(IDS))
    assert all(f["fact"] and f["source"] for f in facts)

# ---- validate() ----
def test_valid_data_passes():
    assert agent.validate(good_data(), IDS)

def test_wrong_policy_count_fails():
    d = good_data(); d["policies"].pop()
    with pytest.raises(ValueError, match="expected"):
        agent.validate(d, IDS)

def test_missing_field_fails():
    d = good_data(); del d["policies"][1]["expected_impact"]
    with pytest.raises(ValueError, match="missing"):
        agent.validate(d, IDS)

def test_single_trade_off_fails():
    d = good_data(); d["policies"][0]["trade_offs"] = ["only one"]
    with pytest.raises(ValueError, match="trade-offs"):
        agent.validate(d, IDS)

def test_bad_difficulty_fails():
    d = good_data(); d["policies"][2]["implementation_difficulty"] = "impossible"
    with pytest.raises(ValueError, match="difficulty"):
        agent.validate(d, IDS)

def test_bad_strength_fails():
    d = good_data(); d["policies"][1]["evidence_strength"] = "certain"
    with pytest.raises(ValueError, match="evidence_strength"):
        agent.validate(d, IDS)

def test_invented_citation_fails():
    d = good_data(); d["policies"][2]["evidence"] = ["F99"]
    with pytest.raises(ValueError, match="unknown facts"):
        agent.validate(d, IDS)

def test_no_citation_fails():
    d = good_data(); d["policies"][0]["evidence"] = ["common sense"]
    with pytest.raises(ValueError, match="no fact ids"):
        agent.validate(d, IDS)

# ---- run() with a fake LLM ----
def test_run_returns_valid_answer_first_try():
    c = FakeClient([json.dumps(good_data())])
    assert agent.run("q", c)["issue_analysis"] == "ok"
    assert c.calls == 1

def test_run_retries_after_bad_answer():
    bad = good_data(); bad["policies"][0]["evidence"] = ["F99"]
    c = FakeClient([json.dumps(bad), json.dumps(good_data())])
    assert agent.run("q", c)
    assert c.calls == 2

def test_run_retries_after_invalid_json():
    c = FakeClient(["not json at all", json.dumps(good_data())])
    assert agent.run("q", c)
    assert c.calls == 2

def test_run_gives_up_after_retries():
    bad = good_data(); bad["policies"][0]["trade_offs"] = []
    c = FakeClient([json.dumps(bad)])
    with pytest.raises(RuntimeError, match="failed validation"):
        agent.run("q", c, retries=2)
    assert c.calls == 3
