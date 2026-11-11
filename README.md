# FINCAPES: towards marginal emission factors for Indonesia

## Active research direction

**What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin approach?**

Direction adopted: 6 November 2026. Jamali is the initial case study; any switch of grid must be justified by data coverage and documented before modelling.

Scope broadened on 10 November 2026 to include investment and retirement responses. The earlier short-run review remains a completed component, not a lifetime geothermal assessment.

The aim is a practical, evidence-based pathway towards future MEF estimation—not a predetermined claim that MEF must replace combined margin (CM) accounting. No Indonesian MEF has yet been estimated or validated in this repository.

## Start here

For the next work session, use [the bounded inventory task and handoff](mef_research/NEXT_STEP.md), updated 11 November 2026.

1. [Research mission and handoff](mef_research/MISSION.md): question, boundaries, deliverables and safeguards.
2. [Initial data-readiness audit](mef_research/DATA_READINESS.md): what existing evidence can support and what still needs checking.
3. [New working report](mef_research/REPORT.md): completed scoping findings and clearly marked remaining work.
4. [Completed first-stage methods comparison](mef_research/METHODS_REVIEW.md) and [source register](mef_research/SOURCE_REGISTER.md): evidence depth, data requirements and initial access checks.
5. [Copy-ready first-stage section](mef_research/FIRST_STAGE_RESULTS.md) and [working references](mef_research/REFERENCES.md): report prose and a separate list for later citations.
6. [Expanded critical literature review](mef_research/CRITICAL_LITERATURE_REVIEW.md) and [claim–evidence ledger](mef_research/CLAIM_EVIDENCE.md): study-specific findings, precise locations and Jamali implications, revised 10 November 2026.
7. [Long-run review and Jamali readiness table](mef_research/LONG_RUN_REVIEW.md) and [supporting evidence](mef_research/LONG_RUN_EVIDENCE.md): completed scope extension, CM comparison, bounded input assessment and modelling decision.

8. [Completed targeted Jamali input audit](mef_research/JAMALI_INPUT_AUDIT.md): reproduced regional/system table differences, new official annual statistics snapshot, input gaps and a report-ready chart.

**Current status:** methods reviews and a targeted boundary/demand audit are complete. Regional/system differences are quantified, but their full coverage bridge remains unresolved. PLN Statistics 2024 was acquired through a working official route and adds annual fuel/price context, not interval operating records. Neither numerical Jamali pilot is cleared. **Next milestone:** build and reconcile a resource-level fleet inventory and electrical-boundary crosswalk, while identifying compatible time profiles and operating observations. Select software only after those checks, not by trying more ML algorithms or tuning CM weights.

Source snapshots can be checked offline with `python3 -B mef_research/audit_review_sources.py` from the repository root. This checks evidence integrity, not model accuracy.

## Existing work remains available

| Existing work | Role in the new direction |
|---|---|
| [Previous research report](FINCAPES_revised_research_report.md) | Background: published-factor, generation and commissioning sensitivity; not the new report |
| [Geothermal accounting model](geothermal_credit_model/README.md) | Reproducible previous calculations; not a dispatch model or MEF estimator |
| [Regulatory evidence review](policy_regulatory_review/README.md) | Starting legal context, with unresolved applicability checks; not an exhaustive current-law opinion |
| [Data inventory](grid_data_sources/data_inventory.csv) | Earlier source leads; “obtained” does not mean suitable for MEF estimation |
| [Wayang Windu forecasting](wayang_windu_ml/README.md) | Evaluated plant-output case study; not evidence of marginal grid emissions |
| [Geothermal data research](geothermal_ml_data_research/README.md) | Previous coverage/access audits; foreign geothermal output alone is not a full-grid MEF dataset |
| `ruptl_eda/`, `ember_indonesia_eda/`, `electricity_demand_ml/` | Planning context and previous exploratory work; not the active research objective |

Previous scripts, datasets and outputs are preserved. Their documented commands retain their original meaning. The previously proposed CM-weight experiment is deferred: it is not a prerequisite for the new MEF research. No existing script should be described as estimating MEFs merely by relabelling its outputs.
