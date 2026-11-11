# Long-run marginal emissions: methods and Jamali readiness

**Follow-up:** the [targeted planning-input audit](JAMALI_INPUT_AUDIT.md) now quantifies the regional/system differences and archives official annual fuel/price context. It supersedes the next-step acquisition status below, not this review's original evidence record. Numerical inputs remain gated.

**Completed focused review: 10 November 2026.** This extends the earlier short-run review; it does not replace it. No Jamali MEF, dispatch model or capacity-expansion model was fitted. Full references and precise evidence locations are recorded in [REFERENCES.md](REFERENCES.md) and [LONG_RUN_EVIDENCE.md](LONG_RUN_EVIDENCE.md).

## Purpose

Geothermal development can affect both how existing power plants operate and which plants are built or retired. The research therefore now asks: **What data and modelling approaches would be needed to estimate the short- and long-run marginal emissions effects of geothermal development in Jamali, and how could these inform assessment of the combined-margin approach?**

## Why long-run effects matter

A short-run dispatch model asks which existing plants change their output when electricity supply or demand changes. A capacity-expansion model also allows decisions about building and retiring plants. Long-run analysis is therefore not simply a short-run emission factor averaged over more years: it must allow the intervention to change the future system itself (Gagnon & Cole, 2022, Introduction and Discussion).

Gagnon and Cole (2022) use the U.S. ReEDS model to compare emissions factors against simulated demand interventions. Their long-run factor performed better for the interventions examined within that modelling experiment. However, the authors explicitly limit the comparison to the assumed future and tested interventions. This is evidence that structural responses can matter, not proof of the accuracy of an Indonesian factor or a geothermal crediting method (Results; Limitations of the study).

## What the reviewed methods actually do

Cambium 2024 runs a baseline and a changed-demand case, allowing both capacity and operation to respond. Its documentation also distinguishes an anticipated intervention from an unexpected one: the timing of investment responses affects whether short-run, long-run or transitional treatment is appropriate (Gagnon et al., 2025, p.29 and §6.4, pp.44–46). A geothermal injection must not simply inherit a factor expressed per MWh of customer demand; delivery losses, location and the generation profile require explicit treatment.

GenX provides a concrete example of the inputs for capacity-expansion modelling: demand profiles, resource availability, fuel prices and emissions characteristics, generator costs and performance, and network information for multi-zone cases. Its documentation also records simplifying assumptions, including market and foresight assumptions. Choosing an open-source model would not remove the need to justify its behaviour for Jamali (GenX Project, n.d., Model Inputs and Limitations).

| Approach | What can change? | What it can contribute | Main limitation for this project |
|---|---|---|---|
| Historical regression | Observed operating relationships | Evidence about short-run responses | Does not directly identify future investment decisions |
| Fixed-fleet dispatch | Output of available plants | Which generation a geothermal injection might displace | Cannot establish investment or retirement effects |
| Capacity expansion with operating representation | Capacity, retirement and output, within specified constraints | A conditional comparison of future systems with and without additional geothermal | Requires a substantially specified local input package and defensible future assumptions |

The first two rows retain the findings of the [earlier review](CRITICAL_LITERATURE_REVIEW.md); the third is supported by the reviewed ReEDS/Cambium study and GenX documentation. This table is a methods comparison, not a ranking of demonstrated Jamali accuracy.

## How this relates to CM

CM is not a simple grid average. UNFCCC TOOL07 version 07.0 defines it as a weighted combination of an operating margin, concerning affected existing generation, and a build margin, concerning prospective generation. A long-run model could investigate the investment response more explicitly, but that does not establish that CM is unsuitable or that a modelled factor is eligible for credits (UNFCCC, 2018, §§1–2, paragraphs 1–3).

The TOOL07 definition was checked through the official catalogue's indexed text; direct full-document retrieval failed. It is used here as a methodological reference, not a determination of current Indonesian programme requirements. Legal applicability, additionality, project emissions, verification and issuance remain separate from estimating gross displaced grid emissions.

## What Jamali evidence is ready?

The following is a **bounded readiness assessment**, based on existing repository records and newly inspected RUPTL pages. “Not verified” means this review has not established a usable input package, not that the data do not exist. Sources are identified by L-numbers in the evidence ledger.

| Information needed | Verified evidence | Remaining gap before a numerical pilot |
|---|---|---|
| Demand and operating time profile | RUPTL annual sales and system power-balance projections (L6, Tables 5.69, 5.86–5.87) | Sales, gross generation and system load are not interchangeable; a compatible time profile is not verified |
| Existing fleet and technical performance | Aggregate existing installed/net dependable capacity in the power balances (L6) | Reconciled unit/resource inventory, efficiency, availability and operating limits not verified as a model-ready package |
| Construction and retirement choices | Annual additions and retirement/mothballing rows (L6, Tables 5.86–5.89) | Distinguish committed from genuinely adjustable projects; establish retirement rules and candidate build limits |
| Investment and fuel economics | RUPTL explains least-cost planning (L6, §II.2, PDF p.55) | Local technology costs, fuel-price paths, heat rates, financing and relevant contract restrictions not verified as a compatible package |
| Renewable, hydro, geothermal and storage operation | Planned technologies/capacities are listed (L6, Tables 5.88–5.89) | Time profiles, seasonal hydro limits, storage behaviour and geothermal delivery assumptions require documentation |
| Transmission and electricity exchanges | RUPTL discusses regional balance and excludes specified Sumatera–Java hydro/geothermal transfers from the local additions tables (L6, PDF pp.361–362) | Compatible flow limits, losses and external supply responses are not verified; a one-zone simplification needs justification |
| Emissions and validation observations | Annual scenario generation/emissions and earlier short-run access screen (D4 and L6) | No compatible interval response-validation dataset has been verified; forecasts are not observed outcomes |
| Policy constraints and study horizon | RUPTL provides 2025–2034 scenarios | Establish version-specific policies and post-2034 assumptions before making lifetime claims |

An important boundary check emerged: Table 5.69 reports 226,327 GWh of regional sales for 2025, whereas Table 5.86 reports 226,107 GWh for the Jawa–Bali system. Those totals should not be silently merged. Their coverage needs reconciliation before modelling (PLN, 2025, PDF pp.324 and 351).

Both RE Base and ARED already contain geothermal additions. Their difference is therefore not a controlled experiment showing geothermal's impact. The earlier annual coal/gas replacement scenarios also do not optimise construction, retirement or dispatch; they remain separate exploratory calculations.

## Feasibility decision and next step

**A numerical long-run Jamali MEF pilot is not yet supported by the audited input package. A documented methods-and-data roadmap is supported.** The existing plans are useful starting evidence, but the core operating, economic and boundary inputs are not yet reconciled. Neither more ML algorithms nor bootstrapping resolves that gap.

The next task is a targeted input-availability audit: first reconcile the Jamali boundary and demand series, then seek a documented fleet/resource inventory, economic assumptions and representative operating profiles. Record provenance, units and completeness before choosing software. No institutional contact is authorised by this review.

If that gate is later cleared, the proposed experiment is to compare two otherwise matched futures with and without a **defined additional geothermal intervention**, allowing permitted investment, retirement and dispatch responses. A baseline that already includes the project must be adjusted transparently, not counted as a no-project case. For a finite project, report the difference in cumulative emissions and any per-MWh normalisation as a **project-scenario result**, not automatically an infinitesimal or universally applicable MEF. Test alternative demand, fuel-cost, policy and retirement assumptions. These are proposed design choices, not completed simulations.

## Research conclusion so far

The review supports broadening the research beyond short-run responses. It does not yet support a numerical replacement for CM or a recommendation to change crediting rules. A defensible policy contribution at this stage is to identify the data disclosure, model documentation and validation needed before a Jamali marginal-emissions approach could be assessed for use.
