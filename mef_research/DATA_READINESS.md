# Jamali data-readiness audit: first external screen

**10 November targeted audit completed:** see [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md). Regional/system planning totals were compared across all ten years; the full coverage bridge remains unresolved. PLN Statistics 2024 is now archived via a working official route (J2), superseding the original D1 retrieval failure for acquisition status. Annual fuel quantities/prices are available as context, but no compatible interval operating pair or complete engineering input package was obtained. Next: resource-level fleet inventory and boundary crosswalk, plus time-profile acquisition.

**10 November scope extension:** this file retains the original short-run screen. A separate [long-run readiness table](LONG_RUN_REVIEW.md#what-jamali-evidence-is-ready) now assesses capacity-expansion requirements against inspected RUPTL tables. It does not convert annual plans into interval observations or clear a numerical pilot.

Status: **bounded external screen completed, 6 November 2026**. The repository seed below has been supplemented with primary-source leads and access checks. This is not an exhaustive availability search. No compatible Jamali interval operating dataset has yet been obtained and no MEF has been fitted. See the [methods-to-data matrix](METHODS_REVIEW.md) and [source register](SOURCE_REGISTER.md).

## External source screen

| Source ID | What was verified | Access / suitability status | Next evidence needed |
|---|---|---|---|
| D1 / follow-up J2: official PLN Statistics 2024 PDF | Original URL failed; alternative official route acquired and selected annual tables inspected on 10 November | Full annual PDF archived; no interval series acquired | Reconcile reporting units to the electrical boundary; use annual quantities/prices as context, not complete plant-level costs |
| D2: ESDM APPLE-GATRIK announcement and portal FAQ | Official announcement confirms generator-emissions reporting purpose; FAQ describes registered-company/admin access and public annual information | Announcement and FAQ HTML archived. Neither establishes public hourly unit records; manual lead could not be retrieved as a PDF | Confirm actual data fields, reporting resolution, historical coverage and authorised research access |
| D3: historical load/public-information portal leads | Addresses were screened, not verified as current usable services | DNS/access failures; no record sample downloaded or current request route confirmed | Locate a current official operator/data-access route; do not assume a historical website still serves data |
| D4: existing repository records | Annual RUPTL/Ember and monthly Wayang Windu files inspected | Useful context or plant-output evidence; not an interval grid response dataset | Obtain aligned system-level operating observations rather than relabelling existing scenarios |

Access failure is not proof that a dataset does not exist or is legally unavailable. None of these statuses is a finding of noncompliance. No third-party message or data request has been sent. The source register records exact URLs and acquisition limits.

## Existing evidence

| Evidence inspected in the existing repository | Potential use | Why it is not sufficient on its own |
|---|---|---|
| RUPTL coverage documented in the previous report and `grid_data_sources/data_inventory.csv`: annual historical Jamali generation and planning tables | System context and annual reconciliation | Annual aggregates/plans do not identify interval operating responses; 2024 historical generation is partial/unaudited to October |
| Ember annual Indonesian extracts, described in the previous report | National context and broad consistency checks | Not a Jamali operational series; lifecycle averages are not marginal operational factors; no Indonesian monthly records were found in the earlier inspected extracts |
| Wayang Windu monthly records and earlier daily-report leads in `geothermal_ml_data_research/README.md` | Plant-output context and measurement lessons | One geothermal field does not observe the response of the rest of Jamali; a complete older daily series has not been extracted |
| ESDM factor tables and `policy_regulatory_review/README.md` | Published accounting benchmark and regulatory context | CM/OM/BM entries are not observed interval system-emissions labels |
| GENESIS plans, grid mapping and original accounting outputs | Background on geothermal additions and geography | Future capacity/timing assumptions are not historical dispatch observations |
| WDI macro indicators and foreign geothermal datasets | Possible context or separate method demonstrations | Geography, frequency and targets do not supply the missing Jamali operating response |

The evidence above supports starting the audit, **not a finding that Jamali MEF estimation is impossible**. Inspect actual candidate files and their documentation before making that decision.

## Candidate variables and access checks

These are a provisional screening list, not a universal mandatory feature set. Method choice determines requirements.

| Candidate information | Role to investigate | Current MEF-audit status |
|---|---|---|
| Interval Jamali system load or demand | Define demand-response estimand; distinguish load from sales | Suitable series not verified after initial portal/source screen |
| Time-aligned plant/unit or fuel-specific generation | Identify system composition and operating response | Suitable interval grid-wide series not yet verified |
| Measured CO₂ or fuel quantities, quality and compatible factors | Construct operational emissions with declared uncertainty | Reporting-system purpose verified; compatible interval grid-wide target/access not verified |
| Imports/exports, transmission limits and boundary definitions | Account for emissions shifted outside the boundary | Suitable operational series not yet verified |
| Outages, availability, ramp limits and plant metadata | Explain dispatch constraints; support engineering approaches | Coverage/access not yet audited for MEF |
| Weather, calendar, hydro conditions and variable renewable output | Investigate demand/supply drivers and confounding | Candidate covariates; causal role and availability to be assessed |
| Prices, dispatch rules, fuel costs and contracts | Explain dispatch incentives if relevant to the chosen method | Optional/method-dependent; access not yet audited |

GDP and national annual fuel imports are not substitutes for interval system load, generation or emissions. Their inclusion would need a timescale-specific rationale. Do not treat every candidate variable as an independent predictor: generation, load and emissions can be jointly determined, and some variables may be consequences of the perturbation being studied.

## Required record for each new source

Record source owner and exact URL; access/retrieval date; observed versus forecast status; geography and electrical boundary; first/last timestamps; resolution/timezone; units and gross/net definitions; missing/duplicate intervals; revisions/publication lag; emissions accounting scope; licence/access constraints; local snapshot path and SHA-256; suitable methods and unresolved limitations.

## Feasibility judgement

**Pilot gate not cleared.** The methods reviews, initial external screen and targeted planning-input audit are complete. Annual publication acquisition progressed, but the full boundary bridge, resource-level engineering package and compatible interval operating sample remain unresolved. No reviewed route is yet supported by a verified compatible Jamali dataset. This does not mean all routes are impossible. Select a historical overlap period only after inspecting compatible records. A statistical association, strong forecast score or synthetic sample expansion does not by itself identify a marginal emissions response.

## Minimum sample package to seek next

This is a proposed acquisition specification, not a message sent to an institution:

1. A machine-readable sample of time-stamped Jamali system demand, specifying MW versus MWh, interval duration, timezone and gross/net boundary.
2. For the same intervals, system operational CO₂ or generation by unit/fuel with compatible emissions-construction information. Constant fuel factors produce an estimated response target with limitations, not direct measured CO₂.
3. Boundary/interchange metadata and relevant flows, including whether captive/embedded generation is included.
4. A data dictionary, missing/quality flags, revision status, available historical span and research-use terms.

Seek a sample/schema first. One sample month can test parsing and compatibility but is not automatically sufficient for estimation across seasons or regimes. Full coverage, identifying variation and validation needs determine the eventual study period and sample size. Do not impose a universal number of observations or bootstrap a small sample into apparent independent history.
