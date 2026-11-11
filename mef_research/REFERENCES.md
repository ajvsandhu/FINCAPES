# Working references for the MEF research

## Targeted Jamali input audit

Reviewed **10 November 2026**. Source IDs J1–J3 refer to [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md); hashes, access attempts and page coverage are in [planning_input_audit_manifest.json](planning_input_audit_manifest.json).

- **J1 / L6 — PLN (2025a):** PT PLN (Persero). *RUPTL 2025–2034*. Primary PDF: https://gatrik.esdm.go.id/gatrik/gatrik-api/storage/migrasi/download_index/files/b967d-ruptl-pln-2025-2034-pub-.pdf . Existing repository snapshot: `../grid_data_sources/raw/ruptl_2025_2034.pdf`. Targeted evidence: Table 5.69 (PDF p.324 / V-88); Tables 5.86–5.87 (PDF pp.351, 355 / V-115, V-119); §V.5.7.3.2 item 5 (PDF p.360 / V-124); local-addition footnotes (PDF pp.361–362); regional generation totals/import footnotes (PDF pp.484–485 / V-248–249); isolated East Java systems (PDF p.918 / B-94); reporting responsibilities (PDF p.48 / I-11); planning constraints (PDF p.350 / V-114). Annual projections are not operating observations.
- **J2 — PLN (2025b):** PT PLN (Persero). *Statistik PLN 2024 / PLN Statistics 2024*. Preface dated June 2025; calendar-year 2024 coverage defined at PDF p.11 / ix. Official index: https://www.pln.co.id/laporan-statistik-id . Official download: https://www.pln.co.id/webapi/media/file/webkorp/asset/Statistik2024.pdf . Archived: `raw/pln_statistics_2024_official.pdf`, 106 pages. Selected evidence: definitions (PDF pp.8–11 / vi–ix); reporting notes and annual balances (PDF pp.16, 19–21); annual fuel use (Table 24, PDF p.66 / 50); annual fuel unit prices (Table 25, PDF p.67 / 51); annual energy by fuel (Table 26, PDF pp.68–69 / 52–53). Full PDF acquired, selected sections inspected; not a claim of full numerical extraction, interval coverage or open-data licensing.
- **J3a/J3b:** repository derivatives `../ruptl_eda/output/ruptl_projected_sales.csv` and `../ruptl_eda/output/ruptl_projected_generation.csv`, checked against J1. Not independent publications.

Additional provenance/access routes checked (not new modelling datasets):

- Official ESDM RUPTL release, 3 June 2025: https://esdm.go.id/id/media-center/arsip-berita/kementerian-esdm-resmi-merilis-dokumen-ruptl-pln-2025-2034 . Viewed for provenance only.
- Official PLN RUPTL listing: https://www.pln.co.id/hubungan-investor-id/informasi-perusahaan-id/ruptl-id-1 . Search-screened; no replacement source snapshot used.
- Old statistics route, retry failed: https://web.pln.co.id/statics/uploads/2025/09/Statistik-PLN-2024-Ind-Eng.pdf . Do not claim byte identity with J2.
- APPLE-GATRIK manual lead, retry failed: https://gatrik.esdm.go.id/assets/uploads/download_index/files/87d63-2.-pedoman-pengisian-apple-gatrik.pdf . No manual acquired or substantive findings drawn from it.

Last updated: **10 November 2026**. Full reference details remain here for the eventual bibliography; revised report prose now uses author–year citations. This is not a claim that every main article was read in full. Preserve the evidence-depth notes when deciding which claims each source can support. Original snapshots remain in [source_manifest.json](source_manifest.json); additions are in [deeper_review_manifest.json](deeper_review_manifest.json). See the [source register](SOURCE_REGISTER.md) and [claim ledger](CLAIM_EVIDENCE.md) for exact support.

## Core methods references

### M1

Siler-Evans, K., Azevedo, I. L., & Morgan, M. G. (2012). Marginal emissions factors for the U.S. electricity system. *Environmental Science & Technology, 46*(9), 4742–4748. DOI: `10.1021/es300145v`.

- Publisher: https://pubs.acs.org/doi/10.1021/es300145v
- Supporting author-institution resource: Carnegie Mellon University, Center for Climate and Energy Decision Making. (n.d.). *Marginal Emissions Factors Repository*. https://www.cmu.edu/cedm/tools-for-cedm/marginal-emissions-factors-repository-mefr.html
- Initial access/review: 6 November 2026. Detailed methodological coverage upgraded on 10 November through the corresponding dissertation chapter below, not through a retrieved journal version.

### M1a — detailed chapter used for methodological claims

Siler-Evans, K. (2012). *Evaluating interventions in the U.S. electricity system: Assessments of energy efficiency, renewable energy, and small-scale cogeneration* [Doctoral dissertation, Carnegie Mellon University]. Chapter 2, especially §§2.3–2.4.2 and 2.8.2–2.8.3.

- https://www.cmu.edu/ceic/assets/docs/publications/phd-dissertations/2012/kyle-siler-evans-phd-thesis-2012.pdf
- Retrieved and inspected 10 November 2026. Full PDF archived; only identified methodological chapter sections are relied upon. Cite this dissertation for detailed chapter claims. The chapter identifies itself as based on M1.

### M2

Deetjen, T. A., & Azevedo, I. L. (2019). Reduced-order dispatch model for simulating marginal emissions factors for the United States power sector. *Environmental Science & Technology, 53*(17), 10506–10513. DOI: `10.1021/acs.est.9b02500`.

- Publisher: https://pubs.acs.org/doi/10.1021/acs.est.9b02500
- Author code: Deetjen, T. (n.d.). *simple_dispatch* [Source code]. https://github.com/tdeetjen/simple_dispatch
- Inspected revision: `84f14faf36fbaa5721aaaf8ac83c2257c6901658`; pinned file URLs recorded in the manifest.
- Access/review date: 6 November 2026. Publisher abstract and author README/code reviewed; full article methods not fully audited. Cite the code for implementation-specific observations.

### M2a — official supporting information used for expanded review

Deetjen, T. A., & Azevedo, I. L. (2019). *Supporting information: A reduced-order dispatch model for simulating marginal emissions factors for the U.S. power sector*. American Chemical Society. DOI: `10.1021/acs.est.9b02500.s001`.

- Official record: https://acs.figshare.com/articles/journal_contribution/Reduced-Order_Dispatch_Model_for_Simulating_Marginal_Emissions_Factors_for_the_United_States_Power_Sector/9722123
- Public metadata: https://api.figshare.com/v2/articles/9722123
- File: https://ndownloader.figshare.com/files/17412503
- Retrieved and inspected 10 November 2026. Nine PDF pages including cover; printed S1–S8. Cite supporting information explicitly for operating assumptions and supplementary benchmarks, not as if the full main article was obtained.

### M3

Fuentes Valenzuela, L., Degleris, A., El Gamal, A., Pavone, M., & Rajagopal, R. (2024). Dynamic locational marginal emissions via implicit differentiation. *IEEE Transactions on Power Systems, 39*(1), 1138–1147. Online publication: 22 February 2023.

- Author-hosted full text: https://www-isl.stanford.edu/~abbas/papers/Dynamic_Locational_Marginal_Emmissions_via_Implicit_Differentiation_journal.pdf
- Access/review date: 6 November 2026. Full text archived; formulation and experiments inspected. No DOI added without verification.

### M4

Mayes, S., Klein, N., & Sanders, K. T. (2024). Using neural networks to forecast marginal emissions factors: A CAISO case study. *Journal of Cleaner Production, 434*, 139895. DOI: `10.1016/j.jclepro.2023.139895`.

- Publisher: https://www.sciencedirect.com/science/article/pii/S0959652623040532
- Author repository: S3researchUSC. (n.d.). *MEF-Regression* [Source code and notebooks]. https://github.com/S3researchUSC/MEF-Regression
- Inspected revision: `81a20e83ca179ca62107805d780c5f20fce0def1`; pinned file URLs recorded in the manifest.
- Access/review date: 6 November 2026. Publisher summary and author notebook/README reviewed; full article methods not retrieved. Notebook observations do not establish the protocol for every published experiment.

### M5

U.S. Environmental Protection Agency. (2024, April). *AVERT user manual* (Version 4.3).

- Manual landing page: https://www.epa.gov/avert/avert-user-manual
- Full manual: https://www.epa.gov/system/files/documents/2024-04/avert-user-manual-v4.3.pdf
- Access/review date: 6 November 2026. Full PDF archived; relevant scope, method and limitation sections inspected. A government method reference, not an additional empirical study.

## Indonesian reporting context

### D2a — official historical announcement

Kementerian Energi dan Sumber Daya Mineral. (2018, August 29). *Sosialiasi pengoperasian aplikasi Apple Gatrik*.

- URL: https://www.esdm.go.id/id/berita-unit/direktorat-jenderal-ketenagalistrikan/sosialiasi-pengoperasian-aplikasi-apple-gatrik
- Access/review date: 6 November 2026. Official historical statement of reporting-system purpose; not evidence of current public interval-data access.

### D2b — reporting-portal description

APPLE-GATRIK. (n.d.). *Bantuan: Pertanyaan yang sering diutarakan*.

- URL: https://perdagangankarbon-esdm.id/site/bantuan
- Access/review date: 6 November 2026. Portal description of access categories and public information; actual unit-level interval availability not verified. Institutional context cross-checked against the ESDM announcement rather than inferred from the domain alone.

## Located but not fully inspected — not evidence of data content

- **D1:** PT PLN (Persero), *Statistik PLN 2024*. https://web.pln.co.id/statics/uploads/2025/09/Statistik-PLN-2024-Ind-Eng.pdf — located 6 November 2026; this URL's retrieval failed. Follow-up J2 below acquired the publication through a different official route on 10 November; its preface establishes June 2025 publication. Do not infer byte identity across URLs or cite uninspected tables.
- **D2 manual lead:** https://gatrik.esdm.go.id/assets/uploads/download_index/files/87d63-2.-pedoman-pengisian-apple-gatrik.pdf — retrieval failed / loading HTML returned, not a reviewed PDF.
- **D3 historical portal:** https://p3bjawabali.pln.co.id/ — inaccessible in this screen; not verified as a current service.
- **D3 candidate information route:** https://web.pln.co.id/ppid — inaccessible and not verified as the current request endpoint. No request was sent.

## Screened but not used as completed validation

Suri, D., Arifi, A., & Azevedo, I. (2023). *Nowcasting day-ahead marginal emissions using multi-headed CNNs and deep generative models* [Workshop preprint]. arXiv:2310.01524.

- https://arxiv.org/abs/2310.01524
- https://arxiv.org/html/2310.01524v1
- Screened 6 November 2026. Contains proposed future directions; not counted as a completed validation study in the core comparison.

## Long-run extension — reviewed 10 November 2026

The following sources support [LONG_RUN_REVIEW.md](LONG_RUN_REVIEW.md). The [long-run evidence ledger](LONG_RUN_EVIDENCE.md) records claim locations and limits; [the manifest](long_run_review_manifest.json) records snapshots and unsuccessful retrievals. This is a focused comparison, not an exhaustive review or a claim of the latest software/report edition.

### L1 — long-run modelling study

Gagnon, P., & Cole, W. (2022). Planning for the evolution of the electric grid with a long-run marginal emission rate. *iScience, 25*(3), 103915. DOI: `10.1016/j.isci.2022.103915`.

- Full article: https://pmc.ncbi.nlm.nih.gov/articles/PMC8873608/
- Local snapshot: `raw/gagnon_cole_2022.html`.
- Full HTML acquired; focused reading of Introduction, Results, Discussion, Limitations of the study, and Model and scenario description. U.S. simulation evidence, not a reproduction or Jamali accuracy result.

### L2 — complementary commentary, not independent validation

Gagnon, P. J., Bistline, J. E. T., Alexander, M. H., & Cole, W. J. (2022). Short-run marginal emission rates omit important impacts of electric-sector interventions. *Proceedings of the National Academy of Sciences*. DOI: `10.1073/pnas.2211624119`.

- Full text: https://pmc.ncbi.nlm.nih.gov/articles/PMC9894150/
- Local snapshot: `raw/gagnon_structural_response_2022.html`.
- Short conceptual commentary inspected; not counted as another empirical validation experiment.

### L3 — documented long-run implementation

Gagnon, P., Sanchez Perez, P. A., Florez, J., Morris, J., Llerena Velasquez, M., & Eisenman, J. (2025, April). *Cambium 2024 scenario descriptions and documentation*. National Renewable Energy Laboratory. NREL/TP-6A40-93005.

- Acquired PDF: https://docs.nlr.gov/docs/fy25osti/93005.pdf
- Original citation URL printed in the report: https://www.nrel.gov/docs/fy25osti/93005.pdf
- Local snapshot: `raw/cambium_2024_documentation.pdf`.
- Full PDF acquired; focused review of overview, selected caveats, printed p.29 and §6.4. Preserve the report's 2025 date and named institution despite the changed host domain. It is U.S. methodological evidence, not local factor data.

### L4a–c — capacity-expansion inputs and assumptions

GenX Project. (n.d.). *GenX.jl documentation: Introduction; Model inputs; Limitations of the GenX model*. Live `stable` documentation, retrieved 10 November 2026.

- Introduction: https://genxproject.github.io/GenX.jl/stable/
- Model inputs: https://genxproject.github.io/GenX.jl/stable/User_Guide/model_input/
- Limitations: https://genxproject.github.io/GenX.jl/stable/limitations_genx/
- Local snapshots: `raw/genx_introduction.html`, `raw/genx_model_inputs.html`, `raw/genx_limitations.html`.
- These snapshots establish documented input fields and stated approximations, not that FINCAPES has configured or run GenX. No version number is assigned from the mutable `stable` URL.

### L5 — CM definition only; full document not acquired

United Nations Framework Convention on Climate Change. (2018, August 31). *TOOL07: Tool to calculate the emission factor for an electricity system* (Version 07.0).

- Official catalogue: https://cdm.unfccc.int/Reference/catalogue/document?doc_id=000004278
- Definitions reviewed in indexed official text: §§1–2, paragraphs 1–3. Direct full-document retrieval failed; returned HTML was not saved as a PDF. No domestic legal-applicability conclusion follows from this reference. Failed routes are preserved in the manifest.

### L6 — existing Jamali planning evidence

PT PLN (Persero). (2025a). *Rencana Usaha Penyediaan Tenaga Listrik (RUPTL) 2025–2034*. Approved through Kepmen ESDM No. 188.K/TL.03/MEM.L/2025, 26 May 2025. The suffix distinguishes this publication from Statistics 2024 (2025b) in the targeted audit.

- Existing source URL: https://gatrik.esdm.go.id/gatrik/gatrik-api/storage/migrasi/download_index/files/b967d-ruptl-pln-2025-2034-pub-.pdf
- Existing repository snapshot: `../grid_data_sources/raw/ruptl_2025_2034.pdf`; not newly downloaded for this extension.
- Focused rechecks: least-cost planning, PDF p.55; Table 5.69, PDF p.324; Tables 5.86–5.89 and regional-balance discussion, PDF pp.351–362; Tables 5.143–5.144, PDF pp.483–485; Tables 5.179–5.180, PDF p.513.
- Planning assumptions and outputs, not historical operational targets or a complete optimisation input package. The electrical boundary must be reconciled with the regional label.

## Coverage and maintenance notes

This file records sources used for the new MEF first-stage review, not every unrelated search result. Existing Indonesian regulatory sources remain documented in [the policy source manifest](../policy_regulatory_review/source_manifest.json); earlier datasets retain their original provenance. The present copy-ready section does not make a new legal-applicability conclusion.

For each later source actually used, add authors/institution, title, date/version, exact URL/DOI, access date, evidence depth and supported claims. Save a snapshot/hash where possible. Keep discovery leads, failed access attempts and sources used as evidence distinct. Do not fill missing bibliographic metadata by guessing.
