# Final method-dependent readiness assessment for a Jamali MEF

Completed **11 November 2026**. This consolidates the completed evidence stages — [methods review](METHODS_REVIEW.md), [long-run review](LONG_RUN_REVIEW.md), [input audit](JAMALI_INPUT_AUDIT.md), [resource inventory](JAMALI_RESOURCE_INVENTORY.md), [IP roster audit](IP_ROSTER_AUDIT.md), [IPP identity audit](IPP_ALIAS_AUDIT.md) and [operating-sample check](OPERATING_SAMPLE_CHECK.md). No new sources were searched and no model was fitted.

## Copy-ready conclusion

No numerical marginal emissions factor (MEF) for the Jamali grid is supported by the evidence currently accessible to this project. The binding constraint is the same for every short-run route: there is no verified, time-aligned record of Jamali system demand together with generation by unit or fuel and a way to construct emissions for the same intervals. Half-hourly system load is known to be held by PLN's Java–Bali dispatch centre (UIP2B) and has been used in academic studies, but it has not been published. Annual planning and statistical sources, partial fleet registers and plant-level samples are useful context and model inputs; they cannot substitute for interval operating observations.

The project has nonetheless produced a reusable foundation: a reviewed methods-to-data matrix, a source-backed partial generator register with alias and boundary crosswalks, annual heat-rate and availability evidence for part of the fleet, and reproducible audits that keep installed, dependable, nominal and project capacity separate. The recommended route is a **historical-regression short-run MEF (M1 type) as the first pilot, conditional on obtaining one year of half-hourly UIP2B data**, with reduced-order dispatch as a later cross-check and capacity expansion treated as a separate, longer programme. Until then, ESDM's published combined-margin factors remain an accounting benchmark, not an observed MEF, and should be reported as such.

## Readiness by route

| Route | What existing evidence supports | Missing for a numerical pilot | Status |
|---|---|---|---|
| **M1 historical regression** (Siler-Evans type) | Method and estimand defined; boundary issues (exchanges, Sumatera imports, isolated systems) documented | Interval Jamali demand and fossil generation or emissions for the same timestamps; timezone and gross/net definitions | **Blocked by one data request** — the lowest-input route |
| **M5 AVERT-style historical-hourly** | Implementation reference reviewed | Unit-level hourly generation and heat input; U.S. defaults are not transferable | Blocked; needs more than M1 |
| **M2 reduced-order dispatch** | Partial unit register; NP annual heat rates and availability; PLN annual fuel prices; IP/IPP identity crosswalks | Complete dated fleet with dependable capacity; heat-rate curves; contract (take-or-pay) constraints; interval demand for calibration | Partially supplied; not calibratable without interval data |
| **M3 network-resolved sensitivities** | None beyond plant locations | Topology, line limits, interval operation | Not ready; later option |
| **M4 ML forecasting of MEF** | Method and code risks (shuffled split) reviewed | A defensible emissions-response target, which itself needs M1/M2 data | Not ready; depends on M1/M2 |
| **Long-run capacity expansion** | RUPTL 2025–2034 power balances, additions, retirements, annual scenarios | Model-ready fleet and cost package, time profiles, transfer limits, post-2034 policy assumptions | Not ready; separate multi-stage programme |
| **Accounting benchmark** (ESDM CM/OM/BM) | Published factors and regulatory context | — | Available, but not an observed MEF and not to be relabelled as one |

## Implementation recommendations

1. **Make one precise data request** (draft below), sent only with authorisation. One year of half-hourly data is enough for an M1 pilot; longer histories enable seasonal and trend checks.
2. **On receipt, run the M1 pilot** on a chronological split: regress interval changes in constructed CO₂ on changes in demand (or fossil generation), with emissions built from generation by unit/fuel and the annual NP/PLN heat rates and fuel factors already archived, and stated uncertainty. Report the estimand explicitly (total-demand MEF versus fossil-generation response).
3. **Use the existing register for the emissions construction**, not as a complete fleet: map received unit or fuel-type series through the alias crosswalks; keep unmatched MW visible.
4. **Treat geothermal displacement as a finite project/no-project comparison** for a stated period, distinct from a local marginal derivative, and do not claim MEF superiority over CM without evidence.
5. **Defer M2, M3 and long-run modelling** until M1 results and the requested data establish whether the fleet package is worth completing.
6. **If the request is refused or unanswered**, the defensible deliverable is this readiness assessment plus the accounting benchmark, clearly labelled — not a model fitted to annual or synthetic data.

## Draft data request (not sent)

> **To:** PT PLN (Persero) UIP2B Jawa, Madura dan Bali — with copy to the Directorate General of Electricity (ESDM) as appropriate
> **Subject:** Research request — historical Jamali system operating data for emissions analysis
>
> We request, for research use under stated confidentiality terms, historical operating data for the interconnected Java–Madura–Bali system for at least one full calendar year (preferably 2023–2024):
>
> 1. System load at 30-minute (or hourly) resolution, with timestamp convention and timezone (WIB), MW or MWh definition, and whether values are gross or net of auxiliary use and losses.
> 2. Generation for the same intervals by unit, or at minimum by plant and fuel type, with unit identifiers and the installed/dependable capacity basis used.
> 3. Interchange and boundary flows for the same intervals, including the Java–Bali cable and any transfers from Sumatera, and a list of resources excluded from the system total.
> 4. Where available, fuel consumption or heat rates by unit, and any emissions data reported through APPLE-GATRIK.
> 5. Documentation of missing intervals, revisions and data-quality flags.
>
> Data would be used only to estimate marginal emissions responses for research; results would be shared with PLN before publication, and no unit-level commercial information would be published without consent.

## Scope and safeguards

This assessment draws only on evidence already archived and reviewed in this repository. Bounded searches are not evidence of total public-data absence. No institutional contact has occurred; sending the draft request requires fresh authorisation.
