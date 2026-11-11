# Methods and Data Requirements: A Critical Literature Review

Updated 10 November 2026. This section replaces the earlier generic methods summary. Author–year citations and precise methodological locations are included; full reference details remain in [REFERENCES.md](REFERENCES.md). The [claim–evidence ledger](CLAIM_EVIDENCE.md) separates documented findings from our implications for Jamali.

## Scope and evidence reviewed

This targeted review examines four research examples and the U.S. Environmental Protection Agency's AVERT manual. It is not an exhaustive literature review. The methodological evidence includes the relevant chapter of Siler-Evans's dissertation, Deetjen and Azevedo's supporting information and author code, the full dynamic-dispatch paper, the AVERT manual, and the shared CAISO neural-network notebook. The main Deetjen and Mayes journal articles were not obtained in full. Supporting information, a dissertation chapter and source code are identified as such rather than represented as the published main papers.

The studies investigate related but different quantities. Some estimate a relationship between fossil generation and emissions; others model a demand perturbation or learn coefficients through an emissions-change objective. This matters because a variable called “demand” does not necessarily represent total electricity use across a grid. The review therefore compares the response being estimated, the information required and the evidence used to assess it—not merely the algorithm name.

## 1. Historical regression: a transparent method with a restricted response boundary

Siler-Evans, Azevedo and Morgan (2012) provide an influential example of historical regression. The detailed evidence reviewed here comes from Chapter 2 of Siler-Evans's dissertation, which explicitly identifies itself as based on that paper. It uses hourly generator-level emissions and gross output from the U.S. EPA's Continuous Emissions Monitoring System, matched to regional boundaries. It estimates a marginal factor from the slope of a regression of hour-to-hour emissions changes on fossil-generation changes. Separate subsets examine differences by month, hour and generation level (Siler-Evans, 2012, Chapter 2, §§2.3–2.4.2, printed pp.8–11).

This is more specific than regressing total emissions on an arbitrary set of economic variables. Its central empirical information is **how fossil output and emissions change together over matching intervals**. However, the chapter uses fossil generation as a proxy for system demand, ignores interregional imports and exports, and conditions its interpretation on excluded generators not responding at the margin. It discusses hydro timing and renewable curtailment as limitations. Its comparison with operator-reported marginal fuel information is a useful check, but the author explicitly notes that the quantities compared are not identical (Siler-Evans, 2012, §§2.4.1–2.4.2 and 2.8.2–2.8.3, pp.9–11 and 26–30).

**Implication for Jamali:** this provides a transparent starting structure, not a ready-made Indonesian factor. A study using only fossil generation must either defend its link to system demand or describe the result more narrowly as a fossil-generation response. The treatment of hydro, other non-fossil output and electrical exchanges must be examined rather than inherited from the U.S. case.

## 2. Reduced-order dispatch: operating assumptions matter as much as fuel type

Deetjen and Azevedo (2019) offer a reduced-order dispatch alternative. Their archived implementation constructs a generator merit order from operating characteristics; its `calcDemandData` and `demandTimeSeries` functions define the response series using recorded fossil generation. The official supporting information shows why a fuel label alone is insufficient: variable operating costs depend on generator characteristics, and a minimum-downtime approximation represents coal units remaining at minimum output rather than repeatedly shutting down and restarting. The specific numerical settings are assumptions of that implementation, not established Indonesian operating rules (Deetjen & Azevedo, 2019, supporting information, pp.S1–S3; archived author code).

The supporting information also prevents a simple claim that more complex models are always more accurate. In its 2014 Texas benchmarking example, it reports lower MEF error for Plexos than for Simple Dispatch, but higher MEF error than for regression; Plexos has higher total-emissions error than Simple Dispatch in that comparison. These are source-reported benchmark comparisons, not independent replications or proof of a causal counterfactual. It separately reports limitations in simulated prices. The trade discussion estimates the scale of interregional exchanges but does not by itself establish a validated exchange response to an intervention (Deetjen & Azevedo, 2019, supporting information, pp.S4–S8).

**Implication for Jamali:** a dispatch approach would need evidence on generator availability, operating costs, heat/emission rates and relevant operating constraints. Annual coal and gas totals cannot identify these features. Benchmarking must specify the outcome being assessed; reasonable total emissions do not automatically validate marginal response, prices or a no-project scenario.

## 3. Dynamic network modelling: distinguish historical checks from network simulations

Fuentes Valenzuela et al. (2024) calculate locational marginal emissions by differentiating an optimisation-based dispatch model. This is a sensitivity calculation based on a specified operating model, not a neural network learning an ideal emission factor. The framework can represent network limits and dependencies across time, including storage and ramping (Fuentes Valenzuela et al., 2024, §§II–III).

An important distinction appears in the experiments. The historical Western U.S. exercise omits transmission constraints because the required data were unavailable. It assesses model-implied emissions changes against observed hourly emissions changes. The separate 240-bus network experiment investigates location-dependent responses using a specified simulation network (Fuentes Valenzuela et al., 2024, §IV-A–B, printed pp.1142–1143).

**Implication for Jamali:** the paper supports investigating operating constraints, but it does not establish that a network-resolved Jamali model can be built from existing annual statistics or plant coordinates. Its historical error comparison is also not direct observation of an otherwise identical system with and without geothermal. Physical-model sensitivity, historical fit and project-impact validation must remain separate claims.

## 4. Machine learning: what is actually learned, and how it is evaluated

Mayes, Klein and Sanders (2024) investigate a neural-network/linear-composite approach for CAISO. Because the full article methods were not retrieved, the detailed findings here concern the **pinned author notebook**, not every experiment reported in the paper. Its feature list contains load, variable renewable generation, hour, day of year and a time-trend variable. The loss function forms predicted emissions changes from a learned demand coefficient multiplied by load change, a learned renewable coefficient multiplied by renewable-output change, and an optional intercept. It compares that sum with observed emissions changes; there is no directly observed “ideal MEF” training label (S3researchUSC, n.d., archived notebook, cells 11 and 17).

This provides a concrete role for ML: estimating state-dependent response coefficients while fitting observable emissions changes. It also exposes the validation question. The inspected notebook shuffles training, validation and test assignments, although scaling is fitted on training rows. Its evaluation helpers assess reconstructed emissions-change predictions. Those checks do not independently verify the coefficients as causal responses, and shuffled assignments do not demonstrate performance on a strictly later period (S3researchUSC, n.d., notebook cells 11 and 21).

**Implication for Jamali:** an ML extension would still require an emissions-response dataset and a defensible interpretation of the coefficients. A future forecasting study should use chronological evaluation and account for when its predictors become available. These are FINCAPES recommendations, not a claim that the entire Mayes paper used the inspected notebook's split or that its published results were reproduced here.

## 5. Historical-hourly tools: a documented method is not a transferable dataset

The EPA's AVERT manual offers a documented historical-hourly approach. Its statistical module groups hours by regional fossil-generation level and constructs information about unit operation, generation, heat input and emissions. This is different from assuming that one named plant always supplies the next unit of electricity (U.S. EPA, 2024, Appendix D, pp.70–71).

The manual identifies important limits: it does not explicitly represent changes in generator ramping and cycling, it holds interregional imports and exports constant as demand changes, and its outputs are expected outcomes rather than precise observed trajectories. Its short-run scope is not equivalent to estimating endogenous investment and retirement effects (U.S. EPA, 2024, p.8 and Appendix L, pp.135–136).

**Implication for Jamali:** AVERT is useful as a reference for transparent assumptions and documentation. Its U.S. regional datasets and default treatment of trade cannot be treated as Indonesian operating evidence. An adaptation would require local records and justification of the operating boundary.

## 6. Cross-study synthesis and research decision

The review supports four conclusions for the proposed Jamali study.

First, **the response must be defined before selecting variables**. Demand, fossil generation and renewable injections are not interchangeable. A factor estimated for one perturbation needs justification before being applied to another.

Second, **emissions information is essential, but its construction must be disclosed**. Observed emissions, fuel-based estimates and simulated emissions have different measurement and modelling limitations. Published CM values should not be used as observed causal-MEF labels.

Third, **validation depends on the claim**. Fitting emissions levels, predicting emissions changes, checking operator fuel information and differentiating a dispatch model are different assessments. They cannot be combined into a single cross-study accuracy ranking. None of the reviewed evidence demonstrates an accurate Jamali MEF or a legally eligible geothermal crediting factor.

Fourth, **more detailed models require better-supported assumptions, not just more predictors**. The first task is to establish whether accessible Jamali records can support a clearly bounded statistical response estimate or a specified engineering model. A transparent statistical baseline remains a conditional candidate, not a proven best method. An ML extension should follow only if there are adequate observations, a clear interpretation and a suitable evaluation design.

The earlier annual scenarios and plant-output forecasts remain background. No model has been fitted in this literature-review revision, and no conclusion has been reached that MEF should replace CM. The immediate deliverable before numerical work remains a compatible operational-data sample and an explicit assessment of what it can identify.
