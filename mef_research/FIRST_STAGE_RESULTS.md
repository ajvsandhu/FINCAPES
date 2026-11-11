# Initial Review of MEF Estimation Methods and Jamali Data Readiness

## Purpose of the review

The first stage of this research examined how marginal emission factors (MEFs) are estimated and what information would be needed to apply suitable methods to the Jawa–Madura–Bali (Jamali) electricity system. The objective was to identify a defensible starting approach and assess data requirements before selecting or training a model.

The review focused on short-run MEFs: how much electricity-system emissions change when electricity use increases or decreases slightly, using the power plants already available. This differs from average grid intensity, which describes emissions per unit of electricity across the whole generation mix. It also differs from long-run effects, which include changes caused by building new power plants or retiring existing ones.

## Methods and data requirements

The review compared four research examples and one government manual. It was a targeted review, not an exhaustive survey. The evidence includes an author's dissertation chapter, official supporting information, a full dynamic-dispatch paper, a government manual and shared author code. Not all journal main texts were available. These distinctions are important because a publisher summary alone cannot establish a study's complete methods or validation procedure.

### Historical regression

Siler-Evans, Azevedo and Morgan (2012) provide a historical regression example. Detailed methodological evidence was obtained from Chapter 2 of Siler-Evans's dissertation, which identifies itself as based on that paper. The chapter uses hourly generator emissions and gross fossil output. It estimates a marginal factor from the relationship between hour-to-hour emissions changes and fossil-generation changes, then examines subsets by month, hour and generation level (Siler-Evans, 2012, §§2.3–2.4.2, pp.8–11).

This is not the same as directly observing how total grid demand causes emissions to change. Fossil generation is used as a demand proxy, regional electricity exchanges are ignored, and the interpretation assumes excluded generators are not responding at the margin. The author also discusses hydro timing and renewable curtailment. A comparison with operator fuel information provides a useful check, but the compared metrics are explicitly not identical (Siler-Evans, 2012, §§2.8.2–2.8.3, pp.26–30).

For Jamali, the lesson is to distinguish a fossil-generation response from a total-demand response. A similar regression would require matching emissions and generation records and a justified treatment of non-fossil generation and exchanges, rather than simply adding more economic predictors.

### Reduced-order dispatch modelling

Deetjen and Azevedo (2019) offer a model of generator dispatch. Their author code uses generator operating characteristics and defines its response series from recorded fossil generation. Their official supporting information documents variable operating-cost assumptions and an approximation to coal-plant minimum downtime. This illustrates why fuel type alone cannot describe which generators can adjust output (Deetjen & Azevedo, 2019, supporting information, pp.S1–S3; archived author code).

The supporting information also shows that a model can perform differently depending on what is evaluated. Its benchmarking discussion distinguishes total-emissions and MEF comparisons, while a separate section identifies limitations in simulated prices. Its trade discussion does not, by itself, validate how exchanges would respond to an intervention (Deetjen & Azevedo, 2019, supporting information, pp.S4–S8).

For Jamali, this approach would require evidence on availability, costs, efficiency, emissions and operating constraints. The review does not establish that dispatch modelling is universally more accurate than regression, or that a good total-emissions estimate validates marginal response.

### Dynamic and network-aware modelling

Fuentes Valenzuela et al. (2024) calculate marginal emissions by examining how an optimisation-based dispatch model responds to a small demand change. The framework can represent network and time-dependent constraints. Importantly, its historical Western U.S. exercise omits transmission constraints because those data were unavailable; it compares model-implied emissions changes with observed hourly changes. A separate network simulation investigates location-dependent responses (Fuentes Valenzuela et al., 2024, §§II–IV, especially §IV-A–B, pp.1142–1143).

For Jamali, this distinction prevents overstating the evidence. A historical operating check and a network simulation are not the same as direct validation of a geothermal project's avoided emissions. Local transmission and operating information would be needed before claiming comparable location-specific results.

### Machine-learning-assisted modelling

Mayes, Klein and Sanders (2024) investigate a neural-network/linear-composite approach for CAISO. The full article methods were not retrieved, so the detailed assessment concerns the pinned author notebook. Its features include load, variable renewable generation and time information. It learns coefficients that are multiplied by changes in load and renewable output to reconstruct observed emissions changes. It does not train against directly observed “ideal MEF” labels (S3researchUSC, n.d., archived notebook, cells 11 and 17).

The inspected notebook uses shuffled training, validation and test assignments, with preprocessing fitted on training rows. Its evaluation helpers assess emissions-change predictions. These checks do not independently establish that the coefficients are causal MEFs or demonstrate forecasting on a strictly later period (S3researchUSC, n.d., cells 11 and 21). These are code-level observations, not a conclusion about every published experiment. For a future Jamali forecasting pilot, chronological evaluation and predictor-availability checks would therefore be required.

### Historical-hourly tools

The EPA's AVERT manual describes grouping historical hours by regional fossil-generation level and using information on unit operation, generation, heat input and emissions. Its limitations include no explicit ramping/cycling response, constant interregional exchanges as demand changes, and outputs representing expected rather than precise observed trajectories (U.S. EPA, 2024, Appendix D, pp.70–71; Appendix L, pp.135–136).

AVERT therefore provides a useful reference for documenting assumptions, but its U.S. datasets are not Jamali operating evidence. Adapting such an approach would require compatible local records and a justified electrical boundary.

### Overall implications

Together, the sources show why MEF research requires more than choosing an algorithm. The study must first define what changes, which emissions are counted and what evidence supports the estimated response. Fitting emissions levels, predicting emissions changes and estimating a causal intervention effect are different tasks. A transparent statistical baseline is a conditional starting candidate, not a demonstrated winner. No reviewed source establishes an accurate Jamali MEF or shows that MEF should replace CM in Indonesian crediting.

## Initial findings for Jamali

The first data-access screen identified official annual electricity statistics and relevant generator-emissions reporting sources. However, it did not verify a compatible historical dataset linking Jamali electricity demand with emissions, or with generation and fuel information suitable for constructing emissions, at matching operational intervals.

Some candidate publications and portals could not be retrieved in the research environment. These access problems do not demonstrate that the required data do not exist. The present finding is narrower: suitable coverage, access and compatibility have not yet been established.

Existing annual planning tables, national electricity aggregates and monthly observations from one geothermal field remain useful background. They do not, by themselves, provide the grid-wide operational response needed for the proposed analysis.

## Implications and next step

No numerical Jamali MEF has been estimated at this stage. The immediate next step is to obtain and inspect a small, compatible sample containing time-stamped system demand, operational emissions or defensible emissions-construction inputs, and documentation of units, grid boundaries and electricity exchanges. A sample can establish whether the records are compatible, but is not automatically sufficient for estimation across seasons and operating conditions.

If suitable evidence becomes available, a transparent statistical baseline is the first approach to assess before introducing more complex models. This is a proposed starting route, not a demonstrated accuracy ranking. Any future application to geothermal must also justify the link between a demand-based response and an additional geothermal injection.

The research currently supports a structured pathway towards MEF estimation, not a conclusion that MEF must replace combined margin accounting. If suitable operational data remain inaccessible or incompatible, a documented data-readiness assessment and practical roadmap will remain valid research outputs.
