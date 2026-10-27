"""Route tests for the Flask app. The LLM call is replaced, so no key or internet is needed. Run: pytest"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import app as web

client = web.app.test_client()

def test_home_and_agent_pages_load():
    assert client.get("/").status_code == 200
    assert client.get("/agent").status_code == 200

def test_health_and_facts():
    assert client.get("/api/health").get_json()["status"] == "ok"
    assert len(client.get("/api/facts").get_json()) >= 10

def test_empty_and_long_questions_rejected():
    assert client.post("/api/policies", json={"question": ""}).status_code == 400
    assert client.post("/api/policies", json={"question": "x" * 501}).status_code == 400

def test_missing_key_gives_clear_error(monkeypatch):
    monkeypatch.delenv("GROQ_API_KEY", raising=False)
    r = client.post("/api/policies", json={"question": "hi"})
    assert r.status_code == 500 and "GROQ_API_KEY" in r.get_json()["error"]

def test_success_and_agent_failure_paths(monkeypatch):
    monkeypatch.setenv("GROQ_API_KEY", "dummy")
    monkeypatch.setattr(web.policy_agent, "run", lambda q, c: {"issue_analysis": "ok", "policies": []})
    assert client.post("/api/policies", json={"question": "hi"}).get_json()["issue_analysis"] == "ok"
    def boom(q, c): raise RuntimeError("failed validation")
    monkeypatch.setattr(web.policy_agent, "run", boom)
    assert client.post("/api/policies", json={"question": "hi"}).status_code == 502
