"""Air & Climate AI - one app that serves the website AND runs the policy agent.
Run:  pip install -r requirements.txt
      set GROQ_API_KEY (PowerShell: $env:GROQ_API_KEY="gsk_...")
      python app.py   ->  http://localhost:5000
Routes:  /            website (website/index.html)
         /agent       policy agent page (website/agent.html)
         /api/policies  POST {"question": "..."} -> JSON policies
         /api/facts   GET  facts the agent is allowed to use
         /api/health  GET  status check
"""
import importlib.util, os
from flask import Flask, jsonify, request, send_from_directory

ROOT = os.path.dirname(os.path.abspath(__file__))
WEB = os.path.join(ROOT, "website")

# load agent/agent.py by path (keeps the agent folder independent of the web layer)
spec = importlib.util.spec_from_file_location("policy_agent", os.path.join(ROOT, "agent", "agent.py"))
policy_agent = importlib.util.module_from_spec(spec)
spec.loader.exec_module(policy_agent)

app = Flask(__name__, static_folder=WEB, static_url_path="")

@app.get("/")
def home():
    return send_from_directory(WEB, "index.html")

@app.get("/agent")
def agent_page():
    return send_from_directory(WEB, "agent.html")

@app.get("/api/health")
def health():
    return jsonify(status="ok", model=policy_agent.MODEL, key_set=bool(os.environ.get("GROQ_API_KEY")))

@app.get("/api/facts")
def facts():
    return jsonify(policy_agent.load_facts())

@app.post("/api/policies")
def policies():
    question = (request.get_json(silent=True) or {}).get("question", "").strip()
    if not question:
        return jsonify(error="Please type a question."), 400
    if len(question) > 500:
        return jsonify(error="Question too long (max 500 characters)."), 400
    key = os.environ.get("GROQ_API_KEY")
    if not key:
        return jsonify(error="Server has no GROQ_API_KEY set. Set it and restart."), 500
    try:
        from groq import Groq
        return jsonify(policy_agent.run(question, Groq(api_key=key)))
    except Exception as e:          # schema failure, API error, bad JSON
        return jsonify(error=f"Agent failed: {type(e).__name__}: {e}"), 502

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", 5000)), debug=False)
