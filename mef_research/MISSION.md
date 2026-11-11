# Research mission: a pathway towards MEFs for Jamali

## Main question

**What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin approach?**

Scope broadened on 10 November 2026 following the user's geothermal/carbon-credit objective. The original short-run review is retained; it is not relabelled as long-run evidence. See the [completed long-run extension](LONG_RUN_REVIEW.md).

## Purpose in plain language

Establish what we would need to estimate how geothermal development affects both electricity-system operation and future capacity choices. Use Jamali as the initial case study and produce a credible roadmap for future Indonesian marginal-emissions research and policy consideration.

We are not assuming that MEF is always more suitable than CM, that present rules are wrong, or that an ML model can discover a uniquely ideal factor. MEF is itself an emission factor. Accounting compliance, operational emissions response and credit issuance are distinct questions.

## Supporting questions

1. How do CM, average grid intensity and short- versus long-run MEFs differ in purpose and interpretation?
2. Which published estimation methods are credible for which questions, and what data and identification assumptions do they require?
3. Which suitable Jamali datasets are actually retrievable, at what frequency, coverage and measurement boundary?
4. What variables and modelling methods are feasible given those data, and what would their limitations be?
5. What targeted improvements in access, documentation or measurement would enable future estimation?

## Scope and target definition

- Initial boundary: Jamali interconnected electricity system, not national Indonesia or a province by convenience. Check imports/exports, embedded generation and captive generation explicitly.
- Two distinct targets: a short-run response with installed capacity fixed, and a long-run response allowing justified investment/retirement changes. Neither is an automatic geothermal crediting factor. Define any finite project-scenario result separately from a local marginal derivative.
- Define the perturbation, response horizon and units before fitting: for example, change in operational CO₂ emissions per incremental MWh of system demand. Extra demand and extra geothermal injection are not assumed interchangeable without a boundary and operating-response justification.
- Historical period: **not selected yet**. Choose a defensible overlap of verified operational datasets. Do not carry the previous 2025–2034 projection window into historical estimation by default.
- Hourly/sub-hourly records are a priority for investigating operating responses, not a universal sufficient condition. Coarser-data methods must have an explicit, defensible interpretation; annual planning scenarios do not become operational observations.
- Long-run investment/retirement effects are now in the methods-and-readiness scope; numerical estimation remains conditional on inputs. Neither the historical period nor future modelling horizon is selected. Do not assume the earlier 2025–2034 window spans geothermal's lifetime.

## Work sequence and decision gates

### 1. Methods and evidence review — first scoping pass completed

Build a source-cited methods matrix covering statistical approaches, dispatch/engineering approaches and ML-assisted approaches. For each, record the estimand, geography, temporal resolution, variables, emissions construction, identification assumptions, treatment of imports and validation. Separate methodological requirements from optional predictors.

The [first methods matrix](METHODS_REVIEW.md) is complete as a bounded review of four research examples and one official method, with explicit full-text/code/abstract evidence limits. It does not establish an Indonesian MEF or universal best algorithm.

On 10 November 2026, the [critical literature review](CRITICAL_LITERATURE_REVIEW.md) and [claim–evidence ledger](CLAIM_EVIDENCE.md) deepened this stage with precise methodological findings, supporting-document/version distinctions and author–year citations. Main-text gaps remain explicit; a generic list of model categories is not sufficient evidence for choosing a method.

### 2. Jamali source audit — targeted planning audit completed

The [long-run methods and planning-input screen](LONG_RUN_REVIEW.md) and subsequent [targeted input audit](JAMALI_INPUT_AUDIT.md), completed 10 November, assess local inputs. The latter reproduces regional/system demand differences and acquires official annual fuel/price context. The full coverage bridge remains unresolved. Next build a resource-level fleet inventory and electrical-boundary crosswalk; retain time-profile and operating-data acquisition as a separate requirement. No numerical pilot is cleared.

Start with the seed in [DATA_READINESS.md](DATA_READINESS.md). Investigate official PLN/ESDM and system-operator publications first, then suitable supplementary sources. Record exact URLs, retrieval dates, accessible files, coverage, units, timezone, gross/net boundaries, licences and limitations. A portal listing or one example date is not a verified time series. Save immutable input snapshots and checksums when files are obtained.

The first external source screen is complete but has not verified a compatible interval load–emissions pair. Sample/schema acquisition and compatibility checking remain necessary, not model training. Access failures must not be described as evidence that Indonesia lacks the data.

### 3. Feasibility decision — initial judgement recorded; inputs not cleared

The bounded long-run review supports a roadmap, not a numerical local estimate. Revisit that judgement only when the documented input gaps are addressed. Neither short-run nor long-run numerical estimation is currently cleared.

For each candidate method, assess whether its essential inputs and assumptions can be supported. Check overlapping time coverage, missingness, aggregation, boundary compatibility, emissions measurement and confounding. Record a justified decision: pilot feasible, narrower pilot feasible, or roadmap only. Do not choose a different grid just because its result looks preferable.

### 4. Conditional historical pilot — not started

If justified, implement a simple transparent baseline before more flexible methods. Use time-respecting holdouts, training-only preprocessing and appropriate sensitivity checks. Assess observable emissions/generation fit separately from the credibility of the estimated marginal response. A predictive derivative, feature importance score or correlation is not automatically a causal MEF. No pilot is required when the evidence does not support it.

A long-run pilot has a separate gate: coherent system inputs, economic and policy assumptions, and a defined project/no-project experiment allowing permitted capacity responses. Baseline reproduction and historical operating checks do not validate an unobserved future. Do not replace these requirements with an ML forecast of CM.

### 5. Report and recommendations

Deliver a documented methods comparison, data inventory, variable rationale, feasibility judgement and practical roadmap. Include reproducible pilot scripts and tables only if a pilot is feasible. Distinguish recommendations for data access or research governance from proposed changes to crediting rules.

## What success looks like

A defensible account of **what can be estimated, what cannot yet be estimated, and what would make the next step possible**. A well-supported negative feasibility finding is a valid research result. No ML improvement, ideal CM weight or legal amendment is required for success.

## Handoff safeguards

The active question supersedes the earlier fixed-factor study as the repository's main direction. Preserve that study and all original outputs as background; do not retroactively describe them as MEF estimates. Do not resume the deferred CM-weight experiment unless explicitly requested. Existing regulatory notes need programme/version checks before final legal conclusions. Do not claim GDP, fuel imports, bootstrapping or foreign plant data solve the identification problem. Do not commit, push, branch or delegate without a new explicit request. Leave unrelated `.DS_Store` changes alone.
