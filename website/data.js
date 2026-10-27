// Single source of truth for every number on the site (DRY). Source: TOI, "Study traces how an El Niño changed the
// pollution map" (study in Atmospheric Pollution Research; IMD/IITM climate-zone study). Change figures here only.
const DATA = {
  repo: "lisaluis/air-climate-ai",
  northDrop: 30,                                  // north India PM2.5 fell by up to this % in 2022–23
  scaleMax: 60,                                   // % change that fills half of the chart track
  winters: {
    w2223: { label: "2022–23", enso: "La Niña", caption: "Stronger winds swept emissions out of the north and carried them south. North India’s PM2.5 fell by up to 30% against the 2019–22 average; Mumbai’s rose 45%." },
    w2324: { label: "2023–24", enso: "El Niño", caption: "Weaker winds let pollution stagnate over Delhi and Jaipur. Jaipur rose about 50% and Delhi over 10%, while the peninsula got sharply cleaner." }
  },
  // v = % change in winter PM2.5 vs the 2019–22 average when the article states it; otherwise only the direction
  // shown in the article's chart is known (hatched bar). min = "at least", approx = "about".
  cities: [
    { name: "Noida",          group: "north", w2223: { dir: "down" }, w2324: { dir: "up" } },
    { name: "Rohtak",         group: "north", w2223: { dir: "down" }, w2324: { dir: "up" } },
    { name: "Greater Noida",  group: "north", w2223: { dir: "down" }, w2324: { dir: "up" } },
    { name: "Bahadurgarh",    group: "north", w2223: { dir: "down" }, w2324: { dir: "up" } },
    { name: "Delhi",          group: "north", w2223: { dir: "down" }, w2324: { v: 10, min: true } },
    { name: "Jaipur",         group: "north", w2223: { dir: "down" }, w2324: { v: 50, approx: true } },
    { name: "Ballabgarh",     group: "north", w2223: { dir: "down" }, w2324: { dir: "up" } },
    { name: "Hyderabad",      group: "peninsula", w2223: { dir: "up" }, w2324: { dir: "down" } },
    { name: "Vapi",           group: "peninsula", w2223: { dir: "up" }, w2324: { dir: "down" } },
    { name: "Mumbai",         group: "peninsula", w2223: { v: 45 },     w2324: { dir: "down" } },
    { name: "Pune",           group: "peninsula", w2223: { dir: "up" }, w2324: { dir: "down" } },
    { name: "Chennai",        group: "peninsula", w2223: { dir: "up" }, w2324: { dir: "down" } },
    { name: "Thiruvananthapuram", group: "peninsula", w2223: { dir: "up" }, w2324: { dir: "down" } }
  ],
  swing: { low: -40, high: 70 },                  // year-to-year range vs 2019–22 average, no major emission change
  zones: [                                        // % of region's area; "then" = 1951–60, "now" = 1991–2020 (NW India)
    { name: "Northwest India: hot semi-arid", then: 25, now: 33, nowText: "a third" },
    { name: "Northwest India: temperate",     then: 25, now: 19, nowText: "under a fifth" },
    { name: "Peninsular India: hot semi-arid", then: 30, now: 16, nowText: "16%" }
  ],
  zoneMax: 40,
  levers: [
    { name: "ENSO-aware seasonal forecasts", idea: "Publish an early-winter outlook of where pollution is likely to accumulate, using the ENSO phase alongside emissions.",
      why: "The same emissions gave a 40% fall in one winter and a 70% rise in another, so a forecast that ignores weather misses the main swing.",
      trade: "Only two winters were studied and the link is correlation, so forecasts could be wrong and erode trust." },
    { name: "Airshed-level action plans", idea: "Plan and enforce controls across state borders for the region whose air actually mixes.",
      why: "In La Niña winds carried Delhi-area pollution to Mumbai and Thiruvananthapuram; city boundaries did not hold it.",
      trade: "Needs states to share costs and data, and is slower to agree than a city plan." },
    { name: "Crop-calendar advisories", idea: "Tell farmers when to sow, harvest and clear residue as the dry zone moves east.",
      why: "The hot semi-arid zone has pushed into Uttar Pradesh, where sowing and harvest timing needs watching.",
      trade: "Advisories only work with extension staff who reach small farmers, and shifting dates can clash with market or irrigation schedules." }
  ]
};
