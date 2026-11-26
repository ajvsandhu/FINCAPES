# Quick presentation: Jamali MEF readiness work

**Audience:** supervisors / research meeting  
**Length:** ~8–12 minutes  
**Message:** We figured out what it would take to estimate MEFs for Jamali. The methods are clear. Public interval data are not. A pilot is ready once PLN UIP2B data arrive. No Jamali MEF number is claimed yet.

**Source of truth:** [WORK_REFERENCE.md](WORK_REFERENCE.md) · draft PDF: [report_draft/jamali_mef_report_draft.pdf](report_draft/jamali_mef_report_draft.pdf)

---

## Slide 1 — Title
**Estimating Marginal Emission Factors for Jamali: What We’ve Done**

- FINCAPES / geothermal emissions research  
- Pathway and readiness assessment (not a final Jamali MEF number)

**Say:** “This is a readiness study: what data and methods would we need, and how far are we?”

---

## Slide 2 — Research question
**What data and methods would we need to estimate geothermal’s short- and long-run marginal emissions effects on Jamali — and how could that inform assessing the combined-margin (CM) approach?**

- Short-run: which existing plants respond today  
- Long-run: what gets built/retired later (separate, larger programme)  
- Aim: credible pathway — not “MEF must replace CM”  
- Full/report wording stays in MISSION.md; this is the slide-readable form only

---

## Slide 2b — Geothermal is the intervention (main point)
**Not a side example — the whole study hangs on this.**

1. **Why geothermal:** near must-run / steady injection into Jamali → something else backs down  
2. **Short-run:** which fossil (or other) plants reduce hour by hour → short-run MEF  
3. **Long-run:** what gets built/retired over project life → separate programme  
4. **CM + carbon credits:** CM is the usual accounting factor for that avoided emissions story  
5. **Why no number yet:** no interval UIP2B-class data → cannot claim MEF beats CM for Jamali geothermal  

**Say:** “We’re not studying MEFs in the abstract. We’re asking what it would take to measure geothermal’s grid emissions impact, and whether CM is good enough for that.”

**Figure (optional):** stylised merit-order night/peak or toy geothermal displacement — label clearly as illustration.

---

## Slide 3 — MEF vs CM (30 seconds)
| | MEF | CM |
|---|---|---|
| Idea | What actually responds when demand/supply changes | UN accounting rule (OM + BM) |
| Needs | Time-aligned operating data | Annual published factors |
| Status for us | Not estimable yet for Jamali | Available as benchmark only |

**Carbon credits:** motivation for assessing CM — projects may seek credits that use CM-type factors. This work does **not** issue credits or declare CM invalid.

**Say:** “MEF is conceptually better for ‘what does geothermal displace?’ But we won’t claim it’s better than CM until we can measure it — and pass a credibility check.”

---

## Slide 4 — What I did (work packages)
1. **Methods review** — 5 short-run approaches + long-run  
2. **Data requirements** — 8 data categories  
3. **Jamali data audit** — register, aliases, operating samples  
4. **Readiness decision** — blocked on UIP2B interval data  
5. **Pilot scaffold + demos** — toy, US public data, illustrations  
6. **Draft report + reproducibility**

---

## Slide 5 — Methods reviewed
- **M1 Historical regression** ← recommended first pilot  
- **M2 Reduced-order dispatch**  
- **M3 Network-aware modelling**  
- **M4 Machine learning** (deferred; needs same data + careful validation)  
- **M5 AVERT-style historical tools**  
- **Long-run capacity expansion** — separate programme  

**Say:** “All short-run methods need the same missing ingredient: time-aligned demand, generation, emissions.”

---

## Slide 6 — Jamali evidence we built
**Figure:** `report_draft/assets/01_register_counts.png`

- 43 existing named entries  
- 294 planning rows  
- 25 isolated East Java systems (kept out)  
- Alias fixes: Jawa 4, Jawa 8, Batang; Grati conflict held  
- NP heat rates / availability; annual sales; Wayang Windu sample  

**Say:** “We have a solid inventory foundation. It is not yet a complete unit census, and it is not interval operating data.”

---

## Slide 7 — The binding gap
**Figure:** `report_draft/assets/08_method_readiness.png`

- No verified public Jamali demand–generation–emissions interval dataset  
- Half-hourly load exists at PLN UIP2B (used in studies) but unpublished  
- Zenodo “Jamali operational” dataset: empty  

**Punchline:** No numerical Jamali MEF is supported yet.

---

## Slide 8 — Why annual data aren’t enough
**Figure:** `report_draft/assets/data_gap_mef_by_frequency.png`

- Same public series, coarsened hourly → daily → monthly  
- Estimates change; **annual totals can’t run the regression at all**  

**Say:** “This is why we can’t just use PLN annual statistics to invent an MEF.”

---

## Slide 9 — Why local MEFs matter (literature)
**Figure:** `report_draft/assets/literature_region_mefs.png`

- Published US MEFs: ~486–834 kgCO₂/MWh by region  
- Midwest ≈ 70% higher than West  
- Average factors can miss marginal response by ~35% in some regions  

**Say:** “Foreign numbers don’t transfer to Indonesia — but they show why local estimation capacity matters.”

---

## Slide 10 — Pilot is ready (demos, not Jamali)
**Figures (pick 1–2):**
- `aef_vs_demand_mef.png`  
- `demand_vs_fossil_mef.png`  
- `multi_ba_hour_demand_mef.png`  

Public EIA demos (CISO / ERCO / MISO / PJM):
- AEF ≠ MEF in several systems  
- Demand MEF ≠ fossil-generation MEF  
- Coal-heavier systems → higher MEFs  

**Also built:**
- Toy chronological M1 pipeline  
- Toy with/without geothermal illustration  
- Stylised Jamali night/peak merit-order cartoon (`jamali_merit_order_night_peak.png`)

**Say clearly:** “These are method demonstrations. Not Jamali MEFs.”

---

## Slide 11 — Credibility before “prefer MEF over CM”
Protocol: [`CREDIBILITY_PROTOCOL.md`](CREDIBILITY_PROTOCOL.md)

1. Define estimand first (perturbation, boundary, horizon)  
2. Check **fit** and **marginal response** separately — don’t score MEF vs CM as truth  
3. Triangulate (M1 + second method where possible) + uncertainty  
4. Only then compare to CM: is the gap large and robust?  
5. Outcomes: inform assessment / report both / discuss rules — not automatic replacement  

**Say:** “Getting data and fitting a model is not enough. Credibility is the gate before any carbon-credit conversation about preferring MEF.”

---

## Slide 12 — Recommendations / next decision
1. **Request** ≥1 year half-hourly UIP2B data (draft ready, not sent)  
2. **On receipt:** run historical-regression pilot (code ready) **under the credibility protocol**  
3. Use plant register for emissions construction  
4. Defer dispatch / network / ML / long-run until pilot proves value  
5. If no data: publish readiness + CM benchmark — don’t fake MEFs from annual data  

**Ask the room:** authorise sending the data request?

---

## Slide 13 — Bottom line
- Research question for this stage: **answered**  
- Deliverable: **pathway + readiness + ready pilot + credibility protocol**  
- Carbon credits: **motivation only** — not eligibility or issuance  
- Not delivered (and not claimed): **a Jamali MEF number**  
- Next research phase starts when interval data arrive  

---

## Optional backup slides
- MEF methods one-liners (regression vs simulation vs ML)  
- Full data-requirements table (8 categories)  
- Toy geothermal displacement figure  
- Exact UIP2B request contents  
- Repo map: `mef_research/WORK_REFERENCE.md`

---

## Suggested figure pack for slides (copy these)
From `mef_research/report_draft/assets/`:
1. `01_register_counts.png`  
2. `08_method_readiness.png`  
3. `data_gap_mef_by_frequency.png`  
4. `literature_region_mefs.png`  
5. `aef_vs_demand_mef.png`  
6. `jamali_merit_order_night_peak.png` (optional Indonesia-facing close)
