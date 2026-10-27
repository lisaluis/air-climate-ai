// Rendering only: all numbers come from data.js. One small function per block (orthogonality).
const $ = (s) => document.querySelector(s);
const el = (tag, cls, html) => { const e = document.createElement(tag); if (cls) e.className = cls; if (html != null) e.innerHTML = html; return e; };

function bindNumbers() {
  const w = DATA.cities, mumbai = w.find(c => c.name === "Mumbai").w2223.v;
  const text = { mumbai: mumbai + "%", northDrop: DATA.northDrop + "%", swingLow: DATA.swing.low + "%", swingHigh: "+" + DATA.swing.high + "%" };
  document.querySelectorAll("[data-bind]").forEach(n => n.textContent = text[n.dataset.bind]);
}

function barGeometry(cell) {                       // signed length on a -50..50 track
  const known = typeof cell.v === "number", sign = cell.dir === "down" ? -1 : 1;
  const len = known ? Math.min(50, cell.v / DATA.scaleMax * 50) : 12;
  return { left: sign < 0 ? 50 - len : 50, width: len, dir: cell.dir || "up", known };
}
function label(cell) {
  if (typeof cell.v !== "number") return "";
  return (cell.approx ? "≈" : "") + (cell.min ? ">" : "") + "+" + cell.v + "%";
}

function buildChart() {
  const root = $("#chart");
  [["north", "North India"], ["peninsula", "Peninsular India"]].forEach(([g, title]) => {
    root.appendChild(el("h3", null, title));
    DATA.cities.filter(c => c.group === g).forEach(c => {
      const row = el("div", "row"), track = el("div", "track"), bar = el("i", "bar"), val = el("span", "val");
      bar.style.left = "50%"; bar.style.width = "0%"; bar.dataset.city = c.name;
      track.appendChild(bar); row.append(el("span", null, c.name), track, val); root.appendChild(row);
    });
  });
}
function showWinter(key) {
  const w = DATA.winters[key];
  document.querySelectorAll(".toggle button").forEach(b => b.setAttribute("aria-pressed", b.dataset.w === key));
  $("#caption").textContent = w.caption;
  DATA.cities.forEach(c => {
    const bar = document.querySelector(`.bar[data-city="${c.name}"]`), cell = c[key], g = barGeometry(cell);
    bar.style.left = g.left + "%"; bar.style.width = g.width + "%";
    bar.className = "bar " + (g.dir === "down" ? "down" : "up") + (g.known ? "" : " dir");
    const v = bar.parentElement.nextElementSibling; v.textContent = label(cell) || (g.dir === "down" ? "cleaner" : "dirtier");
    v.className = "val " + (g.dir === "down" ? "down" : "up");
    bar.setAttribute("aria-label", `${c.name}: ${g.dir === "down" ? "cleaner" : "dirtier"} in ${w.label}`);
  });
}

function buildToggle() {
  [["t1", "e1", "w2223"], ["t2", "e2", "w2324"]].forEach(([t, e, k]) => { $("#" + t).textContent = DATA.winters[k].label; $("#" + e).textContent = DATA.winters[k].enso; });
  let touched = false;
  document.querySelectorAll(".toggle button").forEach(b => b.addEventListener("click", () => { touched = true; showWinter(b.dataset.w); }));
  requestAnimationFrame(() => setTimeout(() => showWinter("w2223"), 150));
  // one orchestrated moment: after the first winter has grown in, flip once to the second
  if (!matchMedia("(prefers-reduced-motion: reduce)").matches)
    setTimeout(() => { if (!touched) showWinter("w2324"); }, 3600);
}

function buildZones() {
  const root = $("#zonechart");
  DATA.zones.forEach(z => {
    const r = el("div", "zr", `<b>${z.name}</b>`);
    [["then", z.then, "about " + z.then + "%"], ["now", z.now, z.nowText]].forEach(([cls, v, t]) => {
      const row = el("div", "zb"), bar = el("i", cls); bar.dataset.w = v / DATA.zoneMax * 100;
      row.append(bar, el("span", null, t)); r.appendChild(row);
    });
    root.appendChild(r);
  });
  const grow = () => document.querySelectorAll("#zonechart i").forEach(b => b.style.width = b.dataset.w + "%");
  new IntersectionObserver((e, o) => { if (e[0].isIntersecting) { grow(); o.disconnect(); } }, { threshold: .3 }).observe(root);
}

function buildLevers() {
  const root = $("#levers");
  DATA.levers.forEach(l => root.appendChild(el("div", "lv",
    `<div><h3>${l.name}</h3><p>${l.idea}</p></div><div><small>Why the findings point here</small><p>${l.why}</p></div><div class="t"><small>Trade-off</small><p>${l.trade}</p></div>`)));
  $("#chatlink").href = `https://colab.research.google.com/github/${DATA.repo}/blob/main/llm/chat_ui.ipynb`;
}

bindNumbers(); buildChart(); buildToggle(); buildZones(); buildLevers();
