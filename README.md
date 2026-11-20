# FINCAPES: Jamali marginal emission factor (MEF) readiness

## Research question

**What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin (CM) approach?**

This repository contains only the active MEF readiness research. No numerical Jamali MEF has been estimated or validated here. Published CM factors remain an accounting benchmark, not an observed MEF. Carbon crediting is treated as policy motivation for assessing CM, not as credit eligibility or issuance.

## Start here

All research materials live under [`mef_research/`](mef_research/):

1. [Mission and boundaries](mef_research/MISSION.md)
2. [Working report](mef_research/REPORT.md)
3. [Credibility protocol (MEF vs CM)](mef_research/CREDIBILITY_PROTOCOL.md)
4. [Work reference / session handoff](mef_research/WORK_REFERENCE.md)
5. [Methods review](mef_research/METHODS_REVIEW.md) and [final readiness](mef_research/FINAL_READINESS.md)
6. [Pilot M1 scaffold and public demos](mef_research/pilot_m1/README.md) (method illustrations — not Jamali MEFs)
7. [Draft report assets](mef_research/report_draft/)
8. [Presentation outline](mef_research/PRESENTATION_OUTLINE.md)

**Current status:** readiness stage is closable with the credibility protocol; short-run M1 pilot remains **blocked on PLN UIP2B interval data**. Supporting planning snapshots and plant samples are under [`mef_research/supporting_inputs/`](mef_research/supporting_inputs/) and [`mef_research/raw/`](mef_research/raw/).

Offline evidence check (hashes, not model accuracy):

```bash
python3 -B mef_research/audit_review_sources.py
```

## What this repo is not

Unrelated earlier FINCAPES experiments (credit-factor sensitivity models, Wayang Windu ML forecasting, Ember/demand EDA packages, regulatory dossier beyond MEF readiness) were removed so the repository matches this research question only.
