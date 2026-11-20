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
**What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal in Jamali, and how could that inform assessment of the combined-margin (CM) approach?**

- Short-run: which existing plants respond today  
- Long-run: what gets built/retired later (separate, larger programme)  
- Aim: credible pathway — not “MEF must replace CM”

---

## Slide 3 — MEF vs CM (30 seconds)
| | MEF | CM |
|---|---|---|
| Idea | What actually responds when demand/supply changes | UN accounting rule (OM + BM) |
| Needs | Time-aligned operating data | Annual published factors |
| Status for us | Not estimable yet for Jamali | Available as benchmark only |

**Say:** “MEF is conceptually better for ‘what does geothermal displace?’ But we won’t claim it’s better than CM until we can measure it.”

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

## Slide 11 — Recommendations / next decision
1. **Request** ≥1 year half-hourly UIP2B data (draft ready, not sent)  
2. **On receipt:** run historical-regression pilot (code ready)  
3. Use plant register for emissions construction  
4. Defer dispatch / network / ML / long-run until pilot proves value  
5. If no data: publish readiness + CM benchmark — don’t fake MEFs from annual data  

**Ask the room:** authorise sending the data request?

---

## Slide 12 — Bottom line
- Research question for this stage: **answered**  
- Deliverable: **pathway + readiness + ready pilot**  
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
