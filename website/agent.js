// Agent page. Two modes, same output format:
//  1. SERVER mode  - /api/policies (Flask app.py on a laptop or in Colab; the key stays on the server).
//  2. BROWSER mode - GitHub Pages has no server, so the page calls Groq directly with a key the user pastes.
// The prompt and validation rules mirror agent/agent.py; facts come from agent/facts.json in both modes.
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const EXAMPLES = ["How should pollution and agriculture policy adapt when weather, not just emissions, drives outcomes?",
  "Why can Delhi get dirtier air even when local emissions do not rise?",
  "What should states do together when pollution crosses state borders?"];
const POLICIES = ["ENSO-aware seasonal pollution forecasting", "Regional (airshed-level) action plans across state borders", "Crop-calendar advisories for farmers"];
const REQUIRED = ["policy", "justification", "evidence", "expected_impact", "trade_offs", "implementation_difficulty", "evidence_strength"];
const GROQ_URL = "https://api.groq.com/openai/v1/chat/completions", MODEL = "openai/gpt-oss-120b";
const SYSTEM = `You are a policy analyst advising Indian central and state governments on air quality and climate.
Rules:
1. Use ONLY the numbered facts provided. Never invent statistics. Cite fact ids (e.g. F5) in 'evidence'.
2. Keep two things apart: what the studies FOUND (facts) and what you PROPOSE (your policy options). Never say a study recommends a policy.
3. Every policy MUST have at least 2 trade_offs (cost, equity, feasibility, political or data risks).
4. The studies are correlational and cover two winters: reflect that in 'evidence_strength' (strong|moderate|weak) and say so in expected_impact. Do not promise numeric reductions.
5. These are options for human decision-makers, not decisions.
Return ONLY a JSON object: {"issue_analysis": "2-3 sentences", "policies": [ {policy, justification, evidence (list of strings with fact ids), expected_impact, trade_offs (list), implementation_difficulty (low|medium|high), evidence_strength (strong|moderate|weak)} ]}`;
let FACTS = {}, SERVER = false;

function validate(d) {                       // same checks as agent.py validate()
  if (!Array.isArray(d.policies) || d.policies.length !== POLICIES.length) throw new Error(`expected ${POLICIES.length} policies`);
  d.policies.forEach((p, i) => {
    const miss = REQUIRED.filter(k => !(k in p)); if (miss.length) throw new Error(`policy ${i + 1}: missing ${miss}`);
    if (!Array.isArray(p.trade_offs) || p.trade_offs.length < 2) throw new Error(`policy ${i + 1}: at least 2 trade-offs required`);
    if (!["low", "medium", "high"].includes(String(p.implementation_difficulty).toLowerCase())) throw new Error(`policy ${i + 1}: difficulty must be low, medium or high`);
    if (!["strong", "moderate", "weak"].includes(String(p.evidence_strength).toLowerCase())) throw new Error(`policy ${i + 1}: evidence_strength must be strong, moderate or weak`);
    const cited = (p.evidence || []).join(" ").match(/F\d+/g) || [];
    if (!cited.length) throw new Error(`policy ${i + 1}: no fact ids cited`);
    const bad = cited.filter(id => !FACTS[id]); if (bad.length) throw new Error(`policy ${i + 1}: cites unknown facts ${bad}`);
  });
  return d;
}
async function browserRun(question, key, retries = 2) {
  const factText = Object.values(FACTS).map(f => `${f.id}: ${f.fact} [${f.source}]`).join("\n");
  let messages = [{ role: "system", content: SYSTEM },
    { role: "user", content: `Question: ${question}\n\nFacts:\n${factText}\n\nCover exactly these policies:\n- ${POLICIES.join("\n- ")}` }], last;
  for (let a = 0; a <= retries; a++) {
    const r = await fetch(GROQ_URL, { method: "POST", headers: { "Content-Type": "application/json", Authorization: "Bearer " + key },
      body: JSON.stringify({ model: MODEL, temperature: 0.2, response_format: { type: "json_object" }, messages }) });
    const j = await r.json();
    if (!r.ok) throw new Error((j.error && j.error.message) || "Groq request failed (" + r.status + ")");
    const content = j.choices[0].message.content;
    try { return validate(JSON.parse(content)); }
    catch (e) { last = e; messages = messages.concat([{ role: "assistant", content }, { role: "user", content: `Your answer failed validation: ${e.message}. Fix it and return the full JSON again.` }]); }
  }
  throw new Error("Output failed validation after " + (retries + 1) + " attempts: " + last.message);
}

function fid(id) { const f = FACTS[id]; return `<span class="fid" title="${f ? esc(f.fact + " [" + f.source + "]") : ""}">${id}</span>`; }
function render(d) {
  let h = `<h2 style="margin-top:2rem">Issue analysis</h2><p>${esc(d.issue_analysis || "")}</p>`;
  d.policies.forEach((p, i) => {
    const ids = (p.evidence || []).join(" ").match(/F\d+/g) || [], s = String(p.evidence_strength).toLowerCase();
    h += `<div class="pol"><h3>${i + 1}. ${esc(p.policy)}</h3>
      <div class="tags"><span class="tag ${s}">Evidence: ${esc(s)}</span><span class="tag">Difficulty: ${esc(p.implementation_difficulty)}</span></div>
      <p>${esc(p.justification)}</p><dl><dt>Evidence</dt><dd>${ids.map(fid).join(" ")}</dd>
      <dt>Expected impact</dt><dd>${esc(p.expected_impact)}</dd>
      <dt>Trade-offs</dt><dd><ul>${p.trade_offs.map(t => `<li>${esc(t)}</li>`).join("")}</ul></dd></dl></div>`;
  });
  $("#out").innerHTML = h;
}
async function run() {
  const q = $("#q").value.trim(), btn = $("#go"), key = $("#key").value.trim();
  if (!q) { $("#out").innerHTML = `<p class="err">Type a question first.</p>`; return; }
  if (!SERVER && !key) { $("#out").innerHTML = `<p class="err">Paste your Groq key above first (free at console.groq.com).</p>`; $("#key").focus(); return; }
  btn.disabled = true; btn.textContent = "Analysing…"; $("#out").innerHTML = "";
  try {
    if (SERVER) {
      const r = await fetch("/api/policies", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q }) });
      const d = await r.json(); if (!r.ok) throw new Error(d.error || "Request failed"); render(d);
    } else { sessionStorage.setItem("gk", key); render(await browserRun(q, key)); }
  } catch (e) {
    $("#out").innerHTML = `<p class="err"><b>The agent could not answer.</b> ${esc(e.message)}</p>`;
  } finally { btn.disabled = false; btn.textContent = "Get policy options"; }
}
async function init() {
  EXAMPLES.forEach(t => { const b = document.createElement("button"); b.className = "chip"; b.textContent = t.length > 60 ? t.slice(0, 57) + "…" : t; b.onclick = () => { $("#q").value = t; }; $("#chips").appendChild(b); });
  SERVER = await fetch("/api/health").then(r => r.ok).catch(() => false);
  try {
    const list = await fetch(SERVER ? "/api/facts" : "../agent/facts.json").then(r => r.json());
    list.forEach(x => FACTS[x.id] = x);
  } catch (e) { $("#out").innerHTML = `<p class="err">Could not load the facts file. Open this page from the live site or run <code>python app.py</code>.</p>`; }
  if (!SERVER) { $("#keybox").hidden = false; $("#key").value = sessionStorage.getItem("gk") || ""; }
  $("#go").onclick = run;
}
init();
