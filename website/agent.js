// Talks to /api/policies (Flask app.py, locally or inside Colab). No numbers live here.
const $ = (s) => document.querySelector(s);
const esc = (t) => String(t).replace(/[&<>"]/g, (c) => ({ "&": "&amp;", "<": "&lt;", ">": "&gt;", '"': "&quot;" }[c]));
const EXAMPLES = ["How should pollution and agriculture policy adapt when weather, not just emissions, drives outcomes?",
  "Why can Delhi get dirtier air even when local emissions do not rise?",
  "What should states do together when pollution crosses state borders?"];
let FACTS = {};

fetch("/api/facts").then(r => r.json()).then(f => f.forEach(x => FACTS[x.id] = x)).catch(() => {});
EXAMPLES.forEach(t => { const b = document.createElement("button"); b.className = "chip"; b.textContent = t.length > 60 ? t.slice(0, 57) + "…" : t; b.onclick = () => { $("#q").value = t; }; $("#chips").appendChild(b); });

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
  const q = $("#q").value.trim(), btn = $("#go");
  if (!q) { $("#out").innerHTML = `<p class="err">Type a question first.</p>`; return; }
  btn.disabled = true; btn.textContent = "Analysing…"; $("#out").innerHTML = "";
  try {
    const r = await fetch("/api/policies", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ question: q }) });
    const d = await r.json();
    if (!r.ok) throw new Error(d.error || "Request failed");
    render(d);
  } catch (e) {
    $("#out").innerHTML = `<p class="err"><b>The agent could not answer.</b> ${esc(e.message)}<br>It needs its server: run <code>python app.py</code> with <code>GROQ_API_KEY</code> set, or open <code>agent/agent_colab.ipynb</code> in Colab.</p>`;
  } finally { btn.disabled = false; btn.textContent = "Get policy options"; }
}
$("#go").onclick = run;
