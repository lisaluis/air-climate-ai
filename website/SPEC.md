# Website spec (Task 1)
Goal: explain why winter PM2.5 flipped between north and peninsular India in 2022-23 and 2023-24 while emissions barely changed, and show the shifting climate zones.
Audience: curious citizens and students. Neutral, evidence-first tone; every claim traced to the TOI article.
Sections: hero + interactive flip chart (city-wise PM2.5 change, both winters) | why (ENSO, wind, rain, pressure, caveats) | climate-zone shifts | three policy levers | links to the agent and the assistant.
Pages: `index.html` (explainer), `agent.html` (policy agent UI, needs `app.py` or Colab).
Stack: plain HTML/CSS/JS, no build step, no chart library (bars are CSS), Google Fonts (Familjen Grotesk, Literata).
Design: haze-grey paper, ink-teal text, diverging teal (cleaner) / amber (dirtier) used only for data meaning. One orchestrated motion: the bars grow in, then flip once from 2022-23 to 2023-24; user toggles respond instantly. Respects reduced motion; keyboard focus visible; responsive down to phones.
Principles: DRY (`data.js` holds all numbers and sources), orthogonality (data / structure / style / behaviour in separate files, one function per block), small iterations (one commit per block), documentation (source note under every chart).
Honesty rule: where the article states no figure for a city, the bar is hatched and labelled "direction only"; nothing is invented.
