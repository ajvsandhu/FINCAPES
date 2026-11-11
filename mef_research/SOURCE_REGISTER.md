# Source register and search boundaries

## O1 — operating-data sample check, 11 November 2026

See [OPERATING_SAMPLE_CHECK.md](OPERATING_SAMPLE_CHECK.md) and [operating_sample_manifest.json](operating_sample_manifest.json). O1, Zenodo record 20098065 (*Jamali Power System Dataset* v1.0.0, CC BY 4.0), was downloaded via the Zenodo API and its MD5 matched. Archive contents: README, LICENSE and `.gitignore` only; zero data files. Linked GitHub repository returned 404. Screened but not adopted: Power-Lab 2030/2035 scenario profiles, a restricted ITPLN thesis and an IEEE paper using unpublished UIP2B half-hourly load, and the commercial Electricity Maps API. No login, account or contact.

## I4–I9 — dated IPP/other-PLN identity audit, 11 November 2026

See [IPP_ALIAS_AUDIT.md](IPP_ALIAS_AUDIT.md) and [ipp_alias_manifest.json](ipp_alias_manifest.json) for URLs, SHA-256 hashes and evidence depth. I4, Kepmen ESDM 310.K/BN.05/MEM.S/2024 (28 November 2024), was acquired as a full 72-page scanned PDF; rows 127 and 131–137 were manually transcribed from rendered pages 1, 4 and 51–53 and visually checked (not OCR). I5 (Sumber Segara Primadaya profile) and I7 (Kansai Electric project page) are undated live operator pages retrieved 11 November 2026; I7 returned curl 403, so only a selected factual web-tool transcription is archived. I6 (ESDM release, 17 February 2020), I8 (ESDM fact sheet, 31 August 2017) and I9 (Bhimasena Power release, 22 July 2023) are archived HTML. The Bhumi Jati Power page returned 403 and is not used. J2 was reused for TJB annual rows. The register is vital-object designation evidence, not an operating census or legal-eligibility opinion. No login or institutional contact occurred.

## I3 — official PLN Indonesia Power roster, 11 November 2026

Official statistics index → linked public 2024 viewer → viewer's enabled PDF download: full 76-page *Laporan Statistik 2024* acquired. [ip_roster_manifest.json](ip_roster_manifest.json) records exact routes, hashes and inspected/rendered pages. Tables 9/11 separate owned and O&M installed capacities; Table 13 supplies national plant/machine cells. Publication date unestablished; 2024 is reporting year. [The audit](IP_ROSTER_AUDIT.md) preserves plant-total, count and cell conflicts, 13 alias/parent mappings, excluded systems and unresolved boundaries. Official unit IDs/DMN/commissioning/retirement are not invented. No restricted access or institutional contact; a 2025 report listing was observed but not used to redefine the historical benchmark.

## Resource-inventory follow-up — 11 November 2026

See [JAMALI_RESOURCE_INVENTORY.md](JAMALI_RESOURCE_INVENTORY.md) and [jamali_inventory_manifest.json](jamali_inventory_manifest.json). L6 was re-inspected at provincial resource/connection and planning tables; no replacement RUPTL file was downloaded. New source **I2**, official PLN Nusantara Power *Statistik Perusahaan 2020–2024*, was downloaded in full (68 pages), with selected capacity, operating, heat-rate and definitions tables inspected. Publication date is unestablished; 2024 is the reporting year. Source conflicts remain explicit. Selected pages were visually checked. Existing Wayang Windu samples and RUPTL annual sales are hash-checked derivatives retaining earlier transcription/version limits. A targeted official-source/operator search yielded no compatible interval package; third-party indexed operator-book copies were not used numerically. No contact or restricted access occurred.

## Targeted planning-input audit — 10 November 2026

See [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md) for findings and [planning_input_audit_manifest.json](planning_input_audit_manifest.json) for exact URLs, hashes, inspected pages and access outcomes. [REFERENCES.md](REFERENCES.md#targeted-jamali-input-audit) stores the bibliography and all additional provenance/access routes screened in this step.

| ID | Evidence inspected | Outcome and limits |
|---|---|---|
| J1 / L6 | Existing full RUPTL PDF; selected boundary, sales, power-balance and generation tables | Ten years reconciled arithmetically; full coverage bridge unresolved. Isolated-solar and embedded-import notes recorded. No interval observations acquired |
| J2 / D1 follow-up | Full 106-page Statistics 2024 PDF via working official index/download route | Archived and hash-checked; selected annual definitions, balances, fuel and price tables inspected. Resolves publication acquisition, not hourly-data access; old failed URL retained separately |
| J3a/J3b | Earlier extracted sales/generation files | Hash-checked derivative inputs, not independent evidence; sales exact, generation component residuals up to 2 GWh retained |

Visual checks: J1 PDF pp.324, 360, 484; J2 PDF pp.8, 67. Selected additional pages were text-inspected as recorded in the manifest. The figure was visually inspected. No upstream research code, institutional login or third-party message was used. This bounded follow-up is not an exhaustive search or proof of total public-data absence.

Review date: **6 November 2026**. Stable source IDs below are used by the methods table and data audit. The machine-readable [source manifest](source_manifest.json) records snapshots, hashes, retrieval failures and inspected notebook evidence. Full-text availability is not inferred from a search snippet. Archived upstream code is evidence only; it was **not executed**.

The [working reference list](REFERENCES.md) retains full bibliographic details for end-of-report citations. Following the request for stronger substantiation, the [critical literature section](CRITICAL_LITERATURE_REVIEW.md) and updated [copy-ready section](FIRST_STAGE_RESULTS.md) now include author–year citations. A [claim–evidence ledger](CLAIM_EVIDENCE.md) records precise locations and separates source findings from recommendations.

**10 November 2026 update:** newly inspected sources and retrieval attempts are recorded in [deeper_review_manifest.json](deeper_review_manifest.json). The original 6 November snapshots and their manifest remain unchanged.

## Methods

### M1 — historical regression example

Siler-Evans, K., Azevedo, I. L. & Morgan, M. G. (2012), *Marginal Emissions Factors for the U.S. Electricity System*, Environmental Science & Technology 46(9), 4742–4748. DOI: `10.1021/es300145v`.

- [Publisher abstract](https://pubs.acs.org/doi/10.1021/es300145v).
- [Author institution's factor repository](https://www.cmu.edu/cedm/tools-for-cedm/marginal-emissions-factors-repository-mefr.html).
- Initial evidence was abstract and institutional page only. **Upgraded:** [author's dissertation](https://www.cmu.edu/ceic/assets/docs/publications/phd-dissertations/2012/kyle-siler-evans-phd-thesis-2012.pdf), full 150-page PDF archived; relevant Chapter 2 inspected. Its footnote on PDF p.15 identifies the chapter as based on the published paper, not necessarily identical to the journal version. Detailed claims cite the thesis: §§2.3–2.4.2, pp.8–11; §§2.8.2–2.8.3, pp.26–30 (PDF offset +10). No other thesis chapter or factor spreadsheet is treated as newly analysed.

### M2 — reduced-order dispatch

Deetjen, T. A. & Azevedo, I. L. (2019), *Reduced-Order Dispatch Model for Simulating Marginal Emissions Factors for the United States Power Sector*, Environmental Science & Technology 53(17), 10506–10513. DOI: `10.1021/acs.est.9b02500`.

- [Publisher abstract](https://pubs.acs.org/doi/10.1021/acs.est.9b02500).
- [Author implementation](https://github.com/tdeetjen/simple_dispatch), archived at commit `84f14faf36fbaa5721aaaf8ac83c2257c6901658`.
- Inspected `README.md` and `simple_dispatch.py`, especially `generatorData` input definitions, `hist_downtime`, `coal_min_downtime` and demand-series construction. Full article not locally archived or fully reviewed. An extra file named by the older README returned 404; this does not invalidate the successfully retrieved files.
- **Upgraded:** full [official supporting information](https://acs.figshare.com/articles/journal_contribution/Reduced-Order_Dispatch_Model_for_Simulating_Marginal_Emissions_Factors_for_the_United_States_Power_Sector/9722123), DOI `10.1021/acs.est.9b02500.s001`, retrieved through the public Figshare API and archived with its metadata. Nine PDF pages: cover plus S1–S8, not a nine-page main article. Inspected operating assumptions, trade discussion and benchmarking limitations; main-article retrieval still returned 403.

### M3 — dynamic locational response

Fuentes Valenzuela, L., Degleris, A., El Gamal, A., Pavone, M. & Rajagopal, R., *Dynamic Locational Marginal Emissions via Implicit Differentiation*, IEEE Transactions on Power Systems 39(1), January 2024, 1138–1147; online publication 22 February 2023.

- [Full author-hosted article](https://www-isl.stanford.edu/~abbas/papers/Dynamic_Locational_Marginal_Emmissions_via_Implicit_Differentiation_journal.pdf).
- Archived full PDF, 10 pages. Inspected model formulation and experiments, especially PDF pp.5–7 / printed pp.1142–1144. Rendered p.5 checked visually. No numerical improvement from this foreign study is adopted as Indonesian accuracy.

### M4 — neural network / linear composite

Mayes, S., Klein, N. & Sanders, K. T. (2024), *Using neural networks to forecast marginal emissions factors: A CAISO case study*, Journal of Cleaner Production 434, 139895. DOI: `10.1016/j.jclepro.2023.139895`.

- [Publisher record and summary](https://www.sciencedirect.com/science/article/pii/S0959652623040532).
- [Author repository](https://github.com/S3researchUSC/MEF-Regression), archived at commit `81a20e83ca179ca62107805d780c5f20fce0def1`.
- Inspected `README.md` and `MLP_MEFs.ipynb`: zero-based cells 11 (split, features, scaling) and 17 (coefficient-based emissions-change loss). Notebook outputs were not independently reproduced. Code-level observations must not be generalised to all paper experiments. Full article methods were not retrieved; publisher access was inconsistent.
- **10 November check:** additionally inspected cell 21's reconstructed-emissions evaluation helpers. Main-paper and accepted-manuscript searches, including bibliographic location metadata, did not produce a verified full text. The expanded section therefore remains explicitly a notebook-level methodological assessment, not a full-paper replication or numerical superiority claim.

### M5 — documented historical-hourly tool

U.S. EPA (April 2024), *AVERT User Manual*, version 4.3.

- [Official manual page](https://www.epa.gov/avert/avert-user-manual).
- [Full manual](https://www.epa.gov/system/files/documents/2024-04/avert-user-manual-v4.3.pdf).
- Archived full PDF, 149 pages. Focused checks: short-run discussion p.8, analysis structure p.13, statistical procedure pp.70–71 and limitations pp.135–136 (printed pages; PDF pages have a six-page offset). Short-run discussion at PDF p.14 rendered and checked visually. This is a government method reference, not a fifth empirical study.

Acquired documents are evidence snapshots, not a grant of redistribution or operational-data reuse rights. No Indonesian data licence, interval coverage, timezone or gross/net field definition has been established for the inaccessible leads below; these must be verified from actual data documentation.

## Indonesian data leads screened

### D1 — PLN Statistics 2024

[Official PDF located](https://web.pln.co.id/statics/uploads/2025/09/Statistik-PLN-2024-Ind-Eng.pdf). The original retrieval failed (web tool 502; local DNS resolution failure). **Initial status: located, not downloaded. Follow-up: J2 acquired the full publication through a different official route on 10 November.** Preserve this failed-URL history; use the J2 snapshot/page evidence for subsequent claims, not search-index text.

### D2 — APPLE-GATRIK reporting context

- [ESDM announcement, 29 August 2018](https://www.esdm.go.id/id/berita-unit/direktorat-jenderal-ketenagalistrikan/sosialiasi-pengoperasian-aplikasi-apple-gatrik): official confirmation of the reporting system's purpose, not proof of current public interval access.
- [Reporting portal FAQ](https://perdagangankarbon-esdm.id/site/bantuan): distinguishes registered generator/administrator access from public annual information. Archived HTML; public raw interval records were not verified. Portal text alone does not establish current reporting frequency or dataset quality.
- [Official manual lead](https://gatrik.esdm.go.id/assets/uploads/download_index/files/87d63-2.-pedoman-pengisian-apple-gatrik.pdf): local DNS failure; web tool returned a loading HTML page rather than a PDF. Not archived as a PDF or treated as full-text reviewed.

### D3 — historical P3B / public-information leads

The historical `https://p3bjawabali.pln.co.id/` address was located through older research references; retrieval failed through local DNS. The candidate `https://web.pln.co.id/ppid` address was also inaccessible in this environment and was not verified as the current official request endpoint. **Neither is an audited current data portal or confirmed data-request route.** No login, account creation, request or contact was attempted. Verify a current official route before any future contact, which requires a separate user instruction.

### D4 — sources already in this repository

The following files were inspected as existing evidence, not newly downloaded for this review:

- `../ruptl_eda/output/ruptl_historical_generation.csv`: annual generation, including Jamali; `partial_year` flag.
- `../ruptl_eda/output/ruptl_projected_emissions.csv`: future scenario emissions, not observed history.
- `../ember_indonesia_eda/output/ember_indonesia_electricity_generation_yearly.csv`: national annual series, including aggregate rows.
- `../geothermal_ml_data_research/data/wayang_windu_monthly_main_meter_2018_2021.csv`: monthly plant records.
- `../grid_data_sources/data_inventory.csv` and the previous research report: provenance and previously documented boundaries.

## Long-run extension — 10 November 2026

The active scope now includes investment and retirement effects. See [LONG_RUN_EVIDENCE.md](LONG_RUN_EVIDENCE.md) for L1–L6 source depth, exact claim locations and inference boundaries; [REFERENCES.md](REFERENCES.md#long-run-extension--reviewed-10-november-2026) contains the complete source links. Six new snapshots and the existing RUPTL hash are recorded in [long_run_review_manifest.json](long_run_review_manifest.json).

- **L1:** full Gagnon–Cole article HTML obtained, with focused checks of intervention modelling, findings and stated limitations.
- **L2:** short supporting commentary obtained; not counted as independent numerical validation.
- **L3:** full Cambium 2024 documentation PDF obtained, with focused section/page review and a visual check of the long-run definition.
- **L4a–c:** official GenX introduction, input and limitation pages obtained; mutable documentation captured by content hash rather than assigned an unsupported release number.
- **L5:** CM definitions verified only through indexed official TOOL07 v07.0 catalogue text. Direct requests returned challenge/non-PDF HTML; no full-tool acquisition or current-law finding is claimed.
- **L6:** existing RUPTL snapshot re-inspected; regional/system sales, capacity and addition boundaries checked. Annual plans are not reclassified as operational observations or a no-geothermal counterfactual.

This extension supports a methods-and-data roadmap, not a numerical long-run Jamali pilot. No new local interval dataset, complete model input package or institutional access permission was acquired. Failed access routes remain separate from substantive findings. Sources from the same research group and conceptual commentaries are not treated as independent confirmations.

## Original short-run search and selection limits

Queries covered named MEF methods, author code, EPA AVERT, PLN statistics, Jamali/P2B load, APPLE-GATRIK, public-information access and Indonesian/Java–Bali MEF terminology. Search results were screened for primary authors, institutions and official publishers. This was a bounded first pass, not an exhaustive or PRISMA review; no claim of research novelty or total public-data absence is made. Inaccessible, annual, projected and plant-only evidence was kept distinct from a usable interval grid dataset.

The Suri, Arifi & Azevedo 2023 [workshop preprint](https://arxiv.org/html/2310.01524v1) was screened but not used as completed empirical validation: its text contains proposed future directions. Other discovered secondary pages were not used to establish technical claims. This prevents proposed CNN/LSTM work from being reported as demonstrated improvement.
