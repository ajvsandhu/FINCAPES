# Long-run review: evidence and access ledger

**Subsequent audit:** additional source/page evidence and acquisition updates are recorded in [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md) and [planning_input_audit_manifest.json](planning_input_audit_manifest.json). Earlier source statuses below describe this review stage.

Review date: **10 November 2026**. This supplements, rather than rewrites, the original [claim–evidence ledger](CLAIM_EVIDENCE.md). Source locations below support [LONG_RUN_REVIEW.md](LONG_RUN_REVIEW.md). Full URLs are kept in [REFERENCES.md](REFERENCES.md); hashes are in [long_run_review_manifest.json](long_run_review_manifest.json).

## Sources and evidence depth

| ID | Source | Material inspected | Evidence/access boundary |
|---|---|---|---|
| L1 | Gagnon & Cole (2022), *Planning for the evolution of the electric grid with a long-run marginal emission rate* | Full article HTML archived; focused reading of Introduction, Results, Discussion, Limitations of the study and Model and scenario description | U.S. ReEDS modelling experiment; no independent reproduction; no Indonesian validation |
| L2 | Gagnon et al. (2022), *Short-run marginal emission rates omit important impacts of electric-sector interventions* | Full short commentary HTML archived and inspected | Conceptual supporting commentary, not an independent validation study |
| L3 | Gagnon et al. (2025), *Cambium 2024 Scenario Descriptions and Documentation*, NREL/TP-6A40-93005 | Full 77-page PDF archived; focused checks PDF pp.1–2, 8–10, 23, 36–37 and 51–59; printed page = PDF page minus 7 in the main body | Reviewed edition, not a claim it is the latest edition; U.S. scenarios and factors are not Jamali inputs. Printed p.29 additionally rendered for visual review |
| L4a–c | GenX Project, Introduction, Model Inputs and Limitations | Three official documentation HTML snapshots; focused checks of model purpose, mandatory inputs, resource cost/performance fields, retirement fields and stated simplifications | Live `stable` documentation captured by hash/date; no release number inferred and no software run |
| L5 | UNFCCC (2018), TOOL07 v07.0 | Official catalogue indexed text, §§1–2, paragraphs 1–3 | Definition-only check via search index. Direct catalogue returned challenge HTML; candidate PDF endpoints returned HTML, not a PDF. No full TOOL07 snapshot or domestic applicability determination |
| L6 | PLN (2025), RUPTL 2025–2034 | Existing 1,253-page PDF, hash recorded without duplication. Focused checks PDF pp.55, 324, 351–362, 483–485 and 513; selected table fragments and previous extraction code cross-checked | A plan, not observed future outcomes or a downloadable optimisation input package. Table 5.86 on PDF p.351 visually inspected |

## Claim-level evidence

| Claim | Evidence location | What is supported | What is not established |
|---|---|---|---|
| LR01 | L1 Introduction, Discussion; L2 body; L3 §6.4, printed pp.44–46 / PDF pp.51–53 | Long-run marginal responses include structural changes; averaging future short-run rates does not add that response | That long-run factors are always preferable for every accounting purpose |
| LR02 | L1 Results and Limitations of the study | The tested long-run metric performed better within the study's modelling experiment; performance depends on the future and interventions examined | A directly observed true future, local causal validation, or universal superiority over CM |
| LR03 | L3 printed p.29 / PDF p.36 and §6.4, PDF pp.52–53 | Base/Perturb solves can rerun expansion and production-cost models; anticipated versus unexpected interventions and load-versus-injection boundaries matter | That copying a U.S. end-use factor is valid for Jamali geothermal |
| LR04 | L4b Model Inputs §1: `Fuels_data.csv`, `Demand_data.csv`, `Generators_variability.csv`, `Resources`, `Network.csv`; Tables 5a–b and retirement fields | Cost/performance, demand and availability data are concrete model inputs; network input is conditional on spatial configuration | That every GenX field is universally required, or these inputs have been acquired locally |
| LR05 | L4c Limitations, items Time period, Cost and Market | Documentation explicitly acknowledges approximations and market assumptions | That software selection removes institutional/contract constraints |
| LR06 | L5 §§1–2, paragraphs 1–3, indexed official text | CM combines OM and BM, relating to affected existing and prospective generation | Full methodological eligibility checks or the current Indonesian legal requirement |
| LR07 | L6 Table 5.69, PDF p.324 (V-88); Table 5.86, PDF p.351 (V-115) | 2025 regional sales 226,327 GWh differ from Jawa–Bali system sales 226,107 GWh; the source tables use different labels | Cause of the coverage difference; permission to treat the series as interchangeable |
| LR08 | L6 Tables 5.86–5.87, PDF pp.351 and 355 | Existing capacity, retirement and mothballing rows are present; `Retired` is dashes and `Mothballed` is −927 MW in 2031 in both displayed tables | No possible future retirements or a unit-resolved lifetime/retirement dataset. Mothballing is not relabelled as retirement |
| LR09 | L6 Tables 5.88–5.89, PDF pp.360–362; footnote PDF pp.361–362 | Both scenarios include geothermal; footnote excludes 2,600 MW of specified interconnection hydro/geothermal from local additions | RE Base minus ARED isolates geothermal, or regional power-balance and local-additions boundaries are identical |
| LR10 | L6 §II.2, PDF p.55 (II-5); generation Tables 5.143–5.144, PDF pp.483–485; emissions Tables 5.179–5.180, PDF p.513 | Least-cost planning description and annual scenario outputs are present | Complete auditable cost/performance inputs or historical dispatch-validation observations |

## FINCAPES interpretations and proposed work

- **LP01 — revised scope:** retain the short-run review and add long-run structural responses for the geothermal question. This is a research-design choice, not a claim that the literature mandates one crediting method.
- **LP02 — readiness decision:** a roadmap is supported; numerical modelling is gated on a reconciled Jamali input package. This is bounded by the inspection above and [DATA_READINESS.md](DATA_READINESS.md), not a finding of total public-data absence.
- **LP03 — future experiment:** paired project/no-project futures with documented boundary, horizon and permitted capacity responses. Finite-project normalisations should not be labelled a universal marginal derivative without sensitivity checks. No such experiment was run.
- **LP04 — policy inference:** data access, documentation and validation recommendations are warranted; a recommendation to replace CM is not established. Legal review remains separate.

## Integrity and acquisition notes

The new manifest preserves successful snapshot hashes and unsuccessful TOOL07 routes separately. The original and deeper-review manifests are unchanged. The RUPTL record points to the already archived repository file and identifies it as an existing input, not a newly acquired document. HTML paper metadata verifies authors, titles and DOIs. Downloaded upstream HTML/code is not executed. Offline checks establish file/evidence integrity, not the correctness of a future counterfactual or the accuracy of an MEF.
