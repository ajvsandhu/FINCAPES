# FINCAPES MEF work reference

**Purpose:** one place to look when writing or revising the final report.  
**Date:** 17 November 2026.  
**Rule:** nothing in the modelling demos is a numerical Jamali MEF unless UIP2B interval data are obtained and reviewed.

---

## 1. Research question

What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin (CM) approach?

**Current answer in one line:** geothermal is the intervention (short-run displacement + long-run capacity effects); methods are clear; public Jamali interval data are not; recommended first pilot is historical regression conditional on PLN UIP2B data; a credibility protocol defines when a future MEF may inform CM assessment (carbon credits = motivation only).

Supporting close-out docs: [`CREDIBILITY_PROTOCOL.md`](CREDIBILITY_PROTOCOL.md), [`FINAL_READINESS.md`](FINAL_READINESS.md), [`REPORT.md`](REPORT.md) (§1A geothermal spine), draft §1 in [`report_draft/jamali_mef_report_draft.html`](report_draft/jamali_mef_report_draft.html).

---

## 2. Main draft report

| File | Role |
|---|---|
| [`report_draft/jamali_mef_report_draft.html`](report_draft/jamali_mef_report_draft.html) | Working draft (figures embedded) |
| [`report_draft/jamali_mef_report_draft.pdf`](report_draft/jamali_mef_report_draft.pdf) | PDF build |
| [`report_draft/assets/`](report_draft/assets/) | Figures copied into the draft |
| Rebuild PDF | `python3 -B mef_research/report_draft/build_pdf.py` |

Supporting readiness write-ups: [`FINAL_READINESS.md`](FINAL_READINESS.md), [`REPORT.md`](REPORT.md), [`NEXT_STEP.md`](NEXT_STEP.md).

---

## 3. What has been completed

### A. Methods and readiness
- Reviewed M1 historical regression, M2 reduced-order dispatch, M3 network-aware, M4 ML, M5 AVERT, plus long-run capacity expansion.
- Conclusion: no numerical Jamali MEF yet; M1 is the lowest-input first pilot.
- Draft UIP2B data request prepared, **not sent** ([`FINAL_READINESS.md`](FINAL_READINESS.md)).

### B. Jamali evidence audit
- Partial register: 43 existing entries, 294 planning rows, 25 isolated East Java systems.
- IP roster + IPP alias audits (Grati conflict held; Jawa 4 / Jawa 8 / Batang identities resolved).
- NP annual heat rates/availability sample; Wayang Windu monthly/daily samples; annual sales.
- Zenodo “Jamali Power System Dataset” checked: empty of data.

Outputs under [`output/`](output/).

### C. Audit figures (real Jamali evidence only)
Folder: [`figures/audit/`](figures/)  
Script: `python3 -B mef_research/figures/build_audit_figures.py`

### D. M1 pilot scaffold
Folder: [`pilot_m1/`](pilot_m1/)

| Piece | What it is |
|---|---|
| `schema.md` | Expected UIP2B-mapped columns |
| `generate_toy_data.py` / `toy_data/` | Synthetic half-hourly grid |
| `run_pilot.py` | Chronological demand MEF + hour-of-day profile |
| `prepare_eia930_demo.py` | Maps EIA-930 → schema for CISO/ERCO/MISO/PJM |
| `run_public_comparisons.py` | AEF vs MEF; demand vs fossil MEF; multi-BA hours |
| `build_literature_panel.py` | Siler-Evans published regional MEF panel |
| `run_data_gap_simulation.py` | Hourly → daily → monthly → annual collapse |
| `run_toy_geothermal_counterfactual.py` | Toy with/without +500 MW geothermal |
| `run_jamali_merit_order_illustration.py` | Night/peak cartoon from NP heat rates |

**Raw EIA file:** download to `pilot_m1/public_demo/raw/` (gitignored; ~40 MB).  
URL pattern: `https://www.eia.gov/electricity/gridmonitor/sixMonthFiles/EIA930_BALANCE_2024_Jan_Jun.csv`

---

## 4. Key modelling results to cite carefully

### Published literature (not re-estimated)
- US regional CO₂ MEFs ~486–834 kg/MWh (Siler-Evans, 2012, Table 2.1).
- Midwest ≈ 70% higher CO₂ MEF than West.
- AEF can differ from MEF by ~35% for CO₂ in some regions (Table 2.2).

### Public EIA demos (constructed CO₂; NOT Jamali)
| BA | AEF | Demand MEF | Fossil MEF | Note |
|---|---|---|---|---|
| CISO | 0.14 | 0.18 | 0.41 | Cleaner / no coal in construction |
| ERCO | 0.28 | 0.47 | 0.54 | Mid |
| MISO | 0.40 | 0.62 | 0.67 | Highest coal share / highest MEF |
| PJM | 0.34 | 0.34 | 0.54 | AEF ≈ demand MEF |

Fossil-generation regressions fit much better (R² ≈ 0.95+) than demand regressions.

### Data-gap simulation (NOT Jamali)
On MISO/CISO, coarsening hourly → daily → monthly changes β; **annual totals cannot run a change-on-change regression at all**.

### Toy geothermal +500 MW (NOT Jamali)
Implied avoided ≈ **0.64 tCO₂ per extra geothermal MWh** in the toy world; night displaces more coal, peaks more gas.

### Stylised Jamali merit-order cartoon (NOT a MEF)
Using NP heat rates + assumed fuel prices: **night → coal on margin (~1.0 t/MWh proxy)**; **peak → gas on margin (~0.42)**. Illustrative only.

---

## 5. Figures map (draft)

| Figure theme | Asset / source |
|---|---|
| Register counts, planning tech, sales, heat rates, Wayang Windu, readiness | `figures/audit/` / `report_draft/assets/01–08…` |
| Literature regional MEFs | `literature_region_mefs.png` |
| AEF vs MEF; demand vs fossil; multi-BA hours | `outputs_public_compare/` |
| Data-gap by frequency | `outputs_data_gap/data_gap_mef_by_frequency.png` |
| Toy geothermal displacement | `outputs_toy_geothermal/toy_geothermal_displacement.png` |
| Jamali night/peak cartoon | `outputs_jamali_illustration/jamali_merit_order_night_peak.png` |
| Toy M1 scatter / hour profile | `outputs_toy/` |

---

## 6. What the final report can claim vs must not claim

**Can claim**
- Pathway, data requirements, readiness by method.
- Partial Jamali register and audit findings.
- Method demos on toy / public US data, clearly labelled.
- That foreign evidence shows MEFs are system-specific and AEF≠MEF.
- That annual Jamali data are insufficient for a short-run MEF pilot.
- A protocol for validating a future MEF before it informs CM assessment.
- That carbon crediting is the policy context for assessing CM (not a completed credit study).

**Must not claim**
- Any number as “the Jamali MEF.”
- That toy / EIA / cartoon results are Indonesian geothermal impacts.
- That MEF must replace CM.
- That ML is ready for Jamali.
- Credit eligibility, volumes or issuance for any project.

---

## 7. Next institutional decision

Send or hold the drafted PLN UIP2B / ESDM data request.  
If data arrive → run `run_pilot.py` on mapped inputs **and apply** [`CREDIBILITY_PROTOCOL.md`](CREDIBILITY_PROTOCOL.md).  
If not → deliver readiness assessment + credibility protocol + labelled CM benchmark.

---

## 8. Quick rebuild commands

```bash
# from repo root FINCAPES/
python3 -B mef_research/figures/build_audit_figures.py
python3 -B mef_research/pilot_m1/generate_toy_data.py
python3 -B mef_research/pilot_m1/run_pilot.py
python3 -B mef_research/pilot_m1/prepare_eia930_demo.py   # needs raw EIA CSV
python3 -B mef_research/pilot_m1/run_public_comparisons.py
python3 -B mef_research/pilot_m1/build_literature_panel.py
python3 -B mef_research/pilot_m1/run_data_gap_simulation.py
python3 -B mef_research/pilot_m1/run_toy_geothermal_counterfactual.py
python3 -B mef_research/pilot_m1/run_jamali_merit_order_illustration.py
python3 -B mef_research/report_draft/build_pdf.py
```
