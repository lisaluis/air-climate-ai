"""Builds the SFT dataset (chat JSONL) for the Air-Quality & Climate assistant.
Facts come from the two TOI articles in the assignment (exact figures) plus a few background standards marked VERIFY.
Each fact is asked in several phrasings; out-of-scope questions get an honest "not sure" answer.
Run:  python build_dataset.py   ->  air_climate.jsonl (train) + heldout_test.jsonl (test, never trained on)
To grow the data: add more (questions, answer) entries to F, or paste article/agency text into an LLM and
ask for Q&A pairs in this same format, then spot-check every number against the source."""
import json, random
random.seed(11)

SYSTEM = ("You are an air-quality and climate assistant for India. Explain ENSO, PM2.5 and pollution meteorology "
          "in plain language using the facts you were trained on. If you are not sure, say so and point to IMD, CPCB or the original study.")

F = [
 (["What is ENSO?", "Can you explain El Nino Southern Oscillation simply?", "What do El Nino and La Nina mean?", "Why do people talk about ENSO when discussing weather in India?"],
  "ENSO (El Nino-Southern Oscillation) is a natural climate cycle in the tropical Pacific. El Nino is its warm phase and La Nina its cool phase. Each changes atmospheric circulation far away, including the winter winds over India, which affects where pollution disperses or builds up."),
 (["What is PM2.5?", "What does PM2.5 mean in air quality reports?", "Why is PM2.5 considered dangerous?"],
  "PM2.5 is particulate matter with a diameter of 2.5 micrometres or smaller. These particles are small enough to go deep into the lungs, which is why PM2.5 is the main number used in air-quality reports and health guidelines."),
 (["How did winter 2022-23 differ from earlier years for north India's air?", "What happened to PM2.5 in north India in winter 2022-23?", "Was north India's air cleaner in 2022-23?"],
  "Winter 2022-23 was a La Nina winter and north India was remarkably clean: PM2.5 was down by up to 30% from the 2019-22 average."),
 (["What happened to Mumbai's air in winter 2022-23?", "Which part of India got dirtier in the La Nina winter?", "Did peninsular India's air get better or worse in 2022-23?"],
  "In winter 2022-23 peninsular India was considerably dirtier than usual. Average PM2.5 in Mumbai rose by 45% compared with the 2019-22 average."),
 (["What happened to PM2.5 in winter 2023-24?", "How did the pollution pattern change in the El Nino winter?", "Which cities got dirtier in 2023-24?"],
  "In winter 2023-24, an El Nino winter, the pattern reversed. PM2.5 spiralled in the north, with Jaipur up about 50% and Delhi up over 10% against the 2019-22 average, while peninsular India became cleaner."),
 (["How big were the year-to-year PM2.5 swings?", "Did emissions change between the two winters?", "Did pollution policies or emissions change a lot in 2022-24?"],
  "Year-to-year PM2.5 changes ranged from about a 40% decline to a 70% increase versus the 2019-22 average, despite no major change in emissions or pollution-control policies. Weather and wind patterns decided where pollution accumulated."),
 (["Why was north India cleaner during La Nina?", "How did La Nina winds affect pollution in Delhi?", "Where did the pollution go in winter 2022-23?"],
  "Under La Nina, stronger winds over north India dispersed emissions from stubble burning and local sources. The altered circulation bypassed Delhi and its surroundings and carried the pollutants south to peninsular cities such as Mumbai and Thiruvananthapuram."),
 (["Why did pollution build up in Delhi and Jaipur during El Nino?", "How did El Nino change winter winds over north India?", "What does stagnation mean for air pollution?"],
  "Under El Nino, winds over northern India were weaker and passed through areas such as Delhi and Jaipur instead of carrying pollutants away. The resulting stagnation favoured the build-up of PM2.5."),
 (["How does rain affect PM2.5?", "Which weather factors mattered in the two winters?", "What is a shallow boundary layer and why does it matter for pollution?"],
  "Rain can remove pollutants from the air. In 2022-23 rainfall was more strongly linked to lower PM2.5, while in 2023-24 surface pressure mattered more: high pressure, weak winds and a shallow boundary layer can trap pollutants close to the ground."),
 (["What did the backward trajectories show?", "Why did Hyderabad's pollution move opposite to Jaipur's?", "How did researchers trace where polluted air came from?"],
  "The researchers used backward air-mass trajectories. Jaipur continued to receive air from polluted northern regions during the El Nino winter, while Hyderabad received cleaner marine and southern air, which helps explain why the pollution pattern moved in opposite directions."),
 (["What does the study mean for Delhi-NCR?", "Do low local emissions guarantee clean air in Delhi?", "Can strong winds make high emissions less harmful locally?"],
  "For Delhi-NCR the study implies that low local or agricultural emissions do not automatically guarantee cleaner air if large-scale circulation turns stagnant. Conversely, even substantial emissions can have a smaller local impact when strong winds disperse or divert them."),
 (["Does El Nino always make Delhi's air worse?", "Can we predict future winters from this study?", "What are the limits of the ENSO pollution study?"],
  "No. The authors caution that the correlations neither establish direct causality nor can be extrapolated to other years, and that El Nino does not invariably worsen air quality in Delhi or north India. Only two unusual winters were studied."),
 (["Is this winter's El Nino expected to be strong?", "What did Gufran Beig say about this year's El Nino?"],
  "Gufran Beig, one of the study's authors, said this year's El Nino is likely to be the strongest on record. The authors stressed they are not implying that the 2023-24 pollution pattern will repeat this winter."),
 (["Which journal published the study and what is it called?", "What is the title of the ENSO air-quality paper?"],
  "The paper, titled 'Air quality in flux: The baffling ENSO transition in India', was published in the journal Atmospheric Pollution Research."),
 (["How has the hot semi-arid zone changed in northwest India?", "Is the dry zone expanding in north India?", "What did the IMD and IITM study find about climate zones?"],
  "In northwest India the hot semi-arid zone grew from about a quarter of the region's area in 1951-60 to a third in 1991-2020, while the temperate zone shrank from about a quarter to under a fifth. The hot, dry zone has pushed east into Uttar Pradesh."),
 (["What happened to the climate zones of peninsular India?", "Is southern India getting wetter?"],
  "In peninsular India the hot semi-arid zone shrank from about 30% of the region to 16%. Most of that land became tropical savannah, which now covers about three-quarters of the peninsula, a change the authors attribute to rising rainfall over southern India."),
 (["Why does the shifting climate zone matter for farming?", "Why does the move of the dry zone into Uttar Pradesh matter?", "Who could use the climate-zone study?"],
  "Uttar Pradesh is one of India's most important farming regions, so the timing of sowing and harvesting needs to be watched closely, said lead author Ananya Karmakar of the study by IMD and IITM. The study could be handy for farm-sector policymakers."),
 (["Which regions moved into the hot semi-arid zone?", "What happened in Marathwada and Vidarbha?"],
  "Marathwada and west Vidarbha moved into the hot semi-arid zone, while the tropical monsoon zone extended along the Konkan coast, coastal Karnataka and Kerala."),
 (["What is the WHO guideline for PM2.5?", "What PM2.5 level does WHO consider safe?"],
  "The 2021 WHO air-quality guideline for PM2.5 is 5 micrograms per cubic metre as an annual mean and 15 micrograms per cubic metre as a 24-hour mean. Please verify against the current WHO text."),
 (["What are India's PM2.5 standards?", "What is the NAAQS limit for PM2.5 in India?"],
  "India's National Ambient Air Quality Standards for PM2.5 are 40 micrograms per cubic metre annual and 60 micrograms per cubic metre for 24 hours. Please verify against the current CPCB notification."),
 (["What is the National Clean Air Programme?", "Who coordinates air-quality action across Delhi-NCR?"],
  "The National Clean Air Programme, launched in 2019, sets city-level PM targets for non-attainment cities, and the Commission for Air Quality Management (CAQM) coordinates action across Delhi-NCR and adjoining states. Please verify details with MoEFCC and CAQM."),
 (["What is an airshed?", "Why plan air-quality action by airshed instead of by city?"],
  "An airshed is a region where air and pollutants circulate together, regardless of state or city borders. Planning by airshed means neighbouring jurisdictions coordinate, which matters when winds carry pollution across borders, as the ENSO study found."),
 (["What does the ENSO study imply for policy?", "Should India only rely on cutting local emissions?"],
  "The study shows weather can decide where pollution accumulates even when emissions are broadly similar, so local emission cuts alone cannot guarantee cleaner air in a given winter. Ideas such as ENSO-aware seasonal forecasts and airshed-level planning are policy proposals that build on this finding; they are not conclusions of the study."),
]
UNSURE = ["What is the PM2.5 level in Pune today?", "What was Chennai's exact PM2.5 change in winter 2023-24?",
 "Will this winter be worse than last winter in Delhi?", "How much money has NCAP spent on Mumbai?",
 "What is the fine for stubble burning in Punjab?", "What was Bengaluru's PM2.5 in 2019?",
 "How many deaths did PM2.5 cause in India last year?", "Which month will the monsoon end this year?",
 "What is the PM10 limit in Kerala?", "How many cities are in the National Clean Air Programme?"]
UA = ("I am not sure about that. My training data does not cover it reliably. Please check IMD, CPCB or the original study for the exact answer.")

rows, held = [], []
for qs, ans in F:
    if len(qs) >= 3:                      # hold out the last phrasing of each fact: never seen in training
        held.append((qs[-1], ans)); qs = qs[:-1]
    for q in qs:
        rows.append((q, ans))
        rows.append(("Quick question: " + q[0].lower() + q[1:], ans))
        rows.append(("In simple words, " + q[0].lower() + q[1:], ans))
for q in UNSURE[:-3]:
    rows += [(q, UA), ("Please tell me: " + q, UA)]
held += [(q, UA) for q in UNSURE[-3:]]    # 3 out-of-scope questions held out too
random.shuffle(rows); train = rows
def w(path, data):
    with open(path, "w", encoding="utf-8") as f:
        for q, a in data:
            f.write(json.dumps({"messages": [{"role": "system", "content": SYSTEM}, {"role": "user", "content": q},
                                             {"role": "assistant", "content": a}]}, ensure_ascii=False) + "\n")
w("air_climate.jsonl", train); w("heldout_test.jsonl", held)
print(len(train), "train;", len(held), "held out")
