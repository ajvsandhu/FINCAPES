# MEF methods linked to Jamali data requirements

**Scope update — 10 November 2026:** this document retains the original short-run methods comparison. The [long-run extension](LONG_RUN_REVIEW.md) adds investment/retirement modelling, a CM comparison and a separate Jamali readiness decision. Historical regression and fixed-fleet dispatch must not be relabelled as lifetime geothermal-impact estimates.

Review date: **6 November 2026**. Completed first-stage **scoping review**, not a systematic literature review or a fitted Indonesian model. Four research examples and one government method were selected to cover statistical, reduced-order, network and ML-assisted approaches. Evidence depth differs and is stated below. Selection is for methodological contrast, not a ranking by reported accuracy.

**Evidence deepened on 10 November 2026:** use the [cited critical literature review](CRITICAL_LITERATURE_REVIEW.md) and [claim–evidence ledger](CLAIM_EVIDENCE.md) for the report. The matrix below has been updated for the newly inspected thesis chapter and official supporting information; this does not mean all journal main texts were obtained.

## 1. Define the quantity before choosing an algorithm

Working target for a possible first pilot: **the short-run change in operational system CO₂ emissions associated with an incremental MWh of Jamali electricity demand**, for a specified interval and electrical boundary, with installed capacity held fixed. Units: tCO₂/MWh. This is a proposed estimand, not a measured series already held in the repository.

Average intensity is total emissions divided by electricity. A marginal response concerns a change in emissions relative to a defined perturbation. A statistical slope estimates an empirical relationship under its identification assumptions; a dispatch sensitivity estimates a response conditional on that model. Neither is automatically an observed causal effect.

Keep these distinctions explicit:

- Demand changes versus geothermal injections: location, curtailment, losses and operating constraints may differ. Do not apply a demand-based factor to geothermal without a justified link.
- Operational CO₂ versus lifecycle CO₂-equivalent: define one compatible boundary before constructing the target.
- Retrospective estimation versus day-ahead forecasting: realised weather and dispatch may explain history but may not be available at a forecast origin.
- Short-run response versus long-run capacity changes: the first pilot would not establish the full 2025–2034 or lifetime impact of geothermal.

## 2. Primary-source methods matrix

Source IDs resolve in [SOURCE_REGISTER.md](SOURCE_REGISTER.md). The last column is **our feasibility inference**, not a claim made by the cited foreign study.

| Example and evidence depth | Quantity and method | Essential input pattern | Validation / scope boundary | Jamali implication |
|---|---|---|---|---|
| **M1 — Siler-Evans, Azevedo & Morgan (2012)**; corresponding Chapter 2 of author's dissertation now inspected, not the journal version | Regression of adjacent-hour emissions changes on fossil-generation changes; subgroup analysis by time and output | Hourly CEMS emissions and gross fossil output matched to regional boundaries | Thesis ignores regional trade and conditions interpretation on omitted generators; operator fuel comparison explicitly uses non-identical metrics | Separate a fossil-generation response from a total-demand MEF and test boundary assumptions; see ledger E01–E05 |
| **M2 — Deetjen & Azevedo (2019)**; full official supporting information plus pinned author code, not full main article | Reduced-order regional dispatch using operating characteristics and an approximation to minimum downtime | Generator capacity, heat/emission rates, fuel costs and availability; archived code's response series is fossil generation | Supporting benchmark ordering depends on endpoint; price output has limits; regional trade is discussed rather than its intervention response established | Verify local operating rules, not just annual fuel totals; see ledger E06–E09 |
| **M3 — Fuentes Valenzuela et al. (2024 issue; online 2023)**; full author-hosted paper | Locational demand sensitivities via implicit differentiation of dynamic dispatch | Generator costs/constraints/emissions, time-indexed demand; network topology/limits for locational results; ramp/storage parameters where represented | Western U.S. experiment compares model-implied changes with observed changes; a separate 240-bus simulation explores network effects. Not a directly observed no-project counterfactual | Network-resolved MEFs are a later option: topology, constraints and operation must be supported, not inferred from a plant-location map |
| **M4 — Mayes, Klein & Sanders (2024)**; publisher summary plus pinned shared notebook/README | CAISO MLP-linear model for emissions response / MEF forecasting | Inspected code uses load, variable renewable output and time features; loss uses changes in emissions, load and VRE | Shared notebook shuffles 60/20/20 assignments and fits scaler on training rows. This is a code observation, not proof every published experiment has that split. No results reproduced | ML still needs a defensible emissions target. For a forecasting pilot, use chronological evaluation and audit predictor availability rather than copying the split |
| **M5 — U.S. EPA AVERT v4.3 (2024)**; full official manual, not a research article | Historical-hourly probabilistic generation/emissions response to an energy-change profile | Unit-level hourly generation, heat input/emissions, regional aggregation and intervention timing | Manual describes short-run application and limitations, including lack of within-region transmission constraints. U.S. regional files are not Indonesian data | Useful implementation reference; adapting the method requires Indonesian operating records. Running U.S. defaults would not estimate Jamali MEFs |

Trade-accounting evidence differs: the inspected M1 thesis explicitly ignores imports/exports; M2's supporting information discusses their regional scale but does not establish a validated intervention response. M4's full treatment remains unverified. M3's historical check lacks transmission data, while its network case is a separate simulation. M5 holds interregional imports/exports constant as load changes (manual p.136); adopting that assumption for Jamali would need justification. Its CO₂ “tons” are U.S. short tons, not metric tonnes, so numerical reuse would require conversion.

The inspected M2 implementation defines its `demand` series as CEMS fossil generation (`calcDemandData` / `demandTimeSeries`), not unrestricted total customer demand. This reinforces the need to specify the perturbation and target rather than copying variable names across systems.

## 3. Variables: required information is not the same as a feature list

| Information | Role in a statistical first pilot | Extra role in engineering / ML options | Priority |
|---|---|---|---|
| System demand or a clearly defined generation-response variable, with timestamps | Defines perturbation and explanatory variation | Dispatch input or ML predictor | Essential for the selected estimand; demand and fossil generation are not interchangeable |
| Operational system CO₂, or compatible generation/fuel observations to construct it | Response variable, including measurement uncertainty | Model calibration / validation; ML response target | Essential; never use published CM as the observed MEF label |
| Non-fossil supply, time/season and relevant operating conditions | Candidate controls or alternative variation; assess confounding and endogeneity | State variables and forecast features | Method-dependent; select by causal/physical role, not correlation alone |
| Interchange, boundary and loss treatment | Distinguish domestic production from displaced emissions elsewhere | Network boundary conditions / calibration | Essential boundary decision; an actual intertie series is needed where exchanges materially affect the response |
| Unit capacities, heat/emission rates, costs and availability | Optional disaggregation / diagnostics | Central to reduced-order dispatch | Required for that approach, not for every regression |
| Network topology/limits, ramping and storage | Not prerequisites for every aggregate regression | Needed where the model claims these spatial/dynamic effects | Required to support corresponding engineering claims |
| Weather and calendar | Potential drivers/controls; avoid assuming weather is an exogenous instrument without justification | Forecast covariates with issue times | Supplementary after target/boundary feasibility |

**GDP and annual national fuel imports are not a substitute for the response dataset.** Resampling the same observations does not create missing operational evidence. Feature importance does not establish causal marginal response. A flexible model's derivative is not automatically a causal MEF.

## 4. Recommended starting route — conditional, not fitted

Start by assessing a **transparent statistical response baseline**, not by assuming a neural network is best. This is a feasibility preference based on the audit burden, not a demonstrated ranking of methods.

Before fitting, document:

1. The perturbation, time resolution, production/consumption boundary and usable historical overlap.
2. Emissions construction, gross/net conversions, treatment of imports, missing intervals and revisions. Do not silently interpolate outages or treat missing records as zero.
3. Which variables are drivers, confounders, outcomes or mediators; the source of identifying variation; what remains unidentifiable. A time-controlled regression alone is not proof of causality.
4. A simple empirical specification and sensitivity alternatives, with serial dependence and structural changes considered. Avoid blindly taking adjacent-hour ratios when demand changes approach zero.
5. Chronological holdouts and training-only preprocessing if predicting future observations. Observable prediction error and marginal-response credibility require separate checks; do not score a MEF against CM or annual average intensity as physical truth.

**Present decision:** no numerical Jamali method is cleared for fitting. The initial screen has not verified an overlapping operational load–emissions pair or a sufficiently specified Indonesian dispatch dataset. This is an evidence/access limitation of this review, not a finding of national data absence.

## 5. Immediate next task

Verify whether a **single compatible historical sample** of Jamali load and emissions-construction data can be obtained, with timestamp, unit and boundary documentation. Prioritise hourly or finer records to evaluate these methods. Start with sample/schema access before requesting or extracting years of records. If obtained, audit overlap and measurement quality before choosing the final period or model. If not, record the precise obstacle and continue the data-readiness roadmap. No third-party request has been sent.
