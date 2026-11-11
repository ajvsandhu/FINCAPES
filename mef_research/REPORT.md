# Towards estimating marginal emission factors for Jamali

**Working report: initial scoping findings from 6 November 2026, methodological review deepened 10 November 2026.** No numerical MEF has been estimated. This is the new active report. The [previous report](../FINCAPES_revised_research_report.md) is preserved as background.

## 1. Research purpose

What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin approach?

The scope was broadened on 10 November 2026 to include capacity investment and retirement responses. The original short-run review remains a completed component. The [long-run review](LONG_RUN_REVIEW.md) contains copy-ready findings, a method-to-data table and the bounded feasibility decision; its [evidence ledger](LONG_RUN_EVIDENCE.md) records source depth and precise locations.

The intended contribution is a documented pathway towards credible estimation. Replacing CM, discovering an ideal factor or demonstrating an ML win is not a predetermined outcome.

## 2. Concepts and policy context — to develop

Define CM, average intensity and short-/long-run MEFs. Specify demand versus electricity-injection perturbations. Review applicable accounting context with version-specific primary sources. The existing regulatory review is a starting point, not a completed current-law determination.

The long-run extension now distinguishes fixed-fleet dispatch from models that allow capacity changes and explains why CM is not a simple grid average. That conceptual comparison does not resolve Indonesian programme-specific eligibility or justify replacing CM.

## 3. MEF estimation methods — critical review deepened 10 November 2026

The earlier generic summary has been replaced by a [cited critical literature review](CRITICAL_LITERATURE_REVIEW.md) and a [copy-ready report section](FIRST_STAGE_RESULTS.md). The [claim–evidence ledger](CLAIM_EVIDENCE.md) records the page, section or code cell behind each substantive finding. Full references remain in [REFERENCES.md](REFERENCES.md).

The evidence is now more specific. Siler-Evans's corresponding thesis chapter estimates a relationship between changes in fossil generation and emissions, uses fossil output as a demand proxy and ignores regional exchanges. Its operator comparison uses non-identical metrics (Siler-Evans, 2012, Chapter 2, §§2.3–2.4.2 and 2.8.2–2.8.3). These findings qualify the earlier description of a generic demand–emissions regression.

Deetjen and Azevedo's official supporting information documents operating-cost and minimum-downtime assumptions, an approximate trade discussion and different benchmarking endpoints. Their archived code constructs its response series from fossil generation (Deetjen & Azevedo, 2019, supporting information, pp.S1–S8; author implementation). The main article was not obtained in full, so the supporting document is identified explicitly.

Fuentes Valenzuela et al. distinguish a historical check without transmission constraints from a separate network simulation (2024, §IV-A–B). The shared Mayes-related notebook learns coefficients through an emissions-change objective and uses a shuffled split; these are implementation observations, not verification of every published experiment (S3researchUSC, n.d., notebook cells 11, 17 and 21). The EPA manual additionally documents constant interregional trade and omitted explicit ramp/cycling response (U.S. EPA, 2024, pp.135–136).

The synthesis is not that one method is proven best. The target, boundary and validation claim must be defined first. Predictions of emissions levels or changes do not independently establish a causal geothermal impact. No new model or Indonesian accuracy result was produced by this revision.

## 4. Jamali data and variable readiness — initial external screen completed

The first screen identified official annual PLN statistics and ESDM's generator-emissions reporting context, but did not verify a usable overlapping Jamali interval load–emissions dataset. The official ESDM announcement and reporting-portal FAQ were archived. An initial PLN statistics retrieval failure was resolved on 10 November through a working official route: the full Statistics 2024 PDF is now archived and selected annual tables inspected. Historical portal/manual access limitations remain; they do not prove that the required operating data do not exist. Exact statuses are recorded in [DATA_READINESS.md](DATA_READINESS.md).

The completed [targeted planning-input audit](JAMALI_INPUT_AUDIT.md) compared all ten planning years. Regional sales exceed interconnected-system sales by 220 GWh in 2025 and 308 GWh in 2034, around 0.1% of regional sales. The differences are quantified, not fully explained. RUPTL explicitly includes isolated-system solar in some additions and Sumatera imports within some hydro/geothermal entries. These coverage checks matter before tables are combined (PLN, 2025a, Tables 5.69, 5.86–5.89, 5.143–5.144 and footnotes).

PLN Statistics 2024 adds annual energy-balance, fuel-use and fuel-price context, but reporting-unit totals still need mapping to the electrical boundary. Annual fuel prices do not supply generator heat rates, future investment costs or hour-by-hour operating response (PLN, 2025b, definitions and Tables 1–2, 24–26). The audit includes report-ready prose, a boundary-comparison PNG, source snapshots and reproducible checks. No MEF was fitted.

Existing RUPTL annual generation and future scenarios remain useful system context. National Ember aggregates and one-field Wayang Windu monthly observations do not supply grid-wide interval emissions response. They should not be pooled or relabelled to create an MEF target. GDP, annual fuel imports and resampling existing observations cannot substitute for the missing operational evidence.

## 5. Feasibility decision — numerical pilots not yet supported

**Final readiness assessment, 11 November:** the [consolidated assessment](FINAL_READINESS.md) concludes that no numerical Jamali MEF is supported by currently accessible evidence. The binding gap for every short-run route is time-aligned interval demand with generation by unit or fuel. The recommended first pilot is a historical-regression short-run MEF, conditional on one year of half-hourly PLN UIP2B data; a precise data request is drafted but not sent. ESDM combined-margin factors remain an accounting benchmark, not an observed MEF.

**Operating-data sample check, 11 November:** a [bounded check](OPERATING_SAMPLE_CHECK.md) inspected one openly licensed candidate described as Jamali operational and generation data (Ikhsan, 2026). Its archived release contains no data records, and its linked repository is unavailable, so it is incompatible. Other leads were future scenario profiles or PLN half-hourly load used in studies but not published. No accessible time-aligned Jamali demand, generation and emissions or fuel package has been verified; neither numerical route is cleared. The next step is a final method-dependent readiness assessment with a precise data request, not further source searching.

**Dated IPP identity follow-up, 11 November:** the [IPP/other-PLN alias audit](IPP_ALIAS_AUDIT.md) reconciled overlapping generator names using ESDM's national vital-object register dated 28 November 2024, operator information and official historical releases. Jawa 4 is Tanjung Jati B units 5–6, distinct from original units 1–4; Jawa 8 is Cilacap Expansion II (operator Unit 3A), separate from the original units and Expansion I; Batang/Jawa Tengah PPP belongs to Bhimasena Power Indonesia, not Bhumi Jati Power. Six earlier register entries now map to 12 descriptive unit labels across three sites. Matched annual installed and Daya Mampu values (2,811.40 and 2,643.80 MW) exist only for the original Tanjung Jati B reporting group; other sources give nominal, project, own-use-adjusted or equity-equivalent MW, which are kept separate rather than summed (ESDM, 2020, 2024; PLN, 2025b). No official unit identifiers or full-grid coverage percentage are established. Fleet-source searching stops here; the next bounded step is one Jamali operating-data sample and schema check. This supersedes the IPP roster task proposed in the next paragraph.

**Official-roster follow-up, 11 November:** the [PLN Indonesia Power roster audit](IP_ROSTER_AUDIT.md) acquired the official 76-page 2024 report, extracted its national machine-capacity table, and added 13 explicit alias/parent crosswalks. Suralaya, Priok/Senayan and Lontar groupings now have source-backed installed-capacity bridges. Owned capacity, O&M resources, isolated systems and resources outside Jamali are distinguished. Machine-level source conflicts remain visible, official unit identifiers and a matching DMN package remain incomplete, and no full-grid coverage percentage is claimed against the differently dated RUPTL benchmark. The next bounded step is an official IPP/other-PLN roster reconciliation for a consistent reference date; interval data remain a separate gate. This supersedes the earlier proposed PLN IP roster task below.

**11 November resource follow-up:** the [resource register and boundary assessment](JAMALI_RESOURCE_INVENTORY.md) now contains 43 named existing-resource entries, 294 provincial planning rows, 25 isolated East Java systems, selected annual capacity/heat-rate/availability observations, and reproducible checks. Existing entries include complexes, a portfolio and exclusions; this is a partial register, not a complete unit census. Page-specific replacement, relocation and efficiency flags bridge planning rows to scenario recaps with residuals below 1 MW. Real annual demand and monthly/daily plant samples do not form an aligned grid-wide operating dataset. Neither pilot is cleared. The next bounded task supersedes the earlier inventory instruction below: audit one missing-fleet official roster and resolve aliases/portfolios against the selected existing-supply benchmark.

The focused long-run screen and targeted input audit found useful planning/annual sources, but no reconciled local fleet, economic, operating-profile and boundary package sufficient for a defensible capacity-expansion pilot. The regional/system mismatch is now measured, with its full cause still unresolved. **Next:** construct and reconcile a resource-level fleet inventory and boundary crosswalk, documenting missing operating/economic fields; identify compatible time profiles. The supported output remains a methods-and-data roadmap, not a numerical long-run MEF or rule-change recommendation. These are bounded findings, not evidence of total public-data absence; see [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md).

For the short-run route, the next task remains obtaining and inspecting a small compatible operating-data sample and its schema: system demand, operational emissions or defensible emissions-construction inputs, and boundary/interchange metadata for the same intervals. This will test access and compatibility before a full historical period or model is selected. A sample useful for parsing is not automatically large or varied enough for estimation.

A transparent statistical baseline is the first route to assess if the response data become available. This is a proposal based on audit burden, not a demonstrated method ranking. If the records remain inaccessible or incompatible, the evidence-backed output will be a data-readiness roadmap rather than a fabricated MEF. Any grid change requires a documented rationale independent of desired results.

## 6. Conditional pilot — not performed

Include only if the feasibility gate is met. Report protocol, validation, estimates, sensitivities and identification limits. Otherwise replace this section with a concrete data-acquisition and modelling roadmap.

## 7. Policy and research recommendations — not yet established

Tie each recommendation to an observed evidence gap. Separate data-disclosure improvements, modelling standards and any proposed crediting-rule change. Neither existing CM sensitivity nor a new short-run estimate proves the full long-run effect of planned geothermal.

## 8. Conclusion — to be determined by evidence

Summarise what available evidence supports, remaining barriers and practical next steps. A rigorous readiness assessment without a numerical MEF remains a valid result.

## Background appendix

Reference, without repeating in full, the earlier factor/timing sensitivities and bounded Wayang Windu forecasting case study where relevant. Keep national annual-demand forecasting in research history, not the main MEF analysis.
