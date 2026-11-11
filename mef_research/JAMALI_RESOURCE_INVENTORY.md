# Jamali resource inventory and electrical-boundary crosswalk

Bounded assessment completed **11 November 2026**. This is a reproducible first resource register, **not a complete unit census or a reconciled dispatch fleet**. No numerical Jamali MEF has been estimated. Existing observations, planning candidates, isolated systems and transfers are kept separate.

## Copy-ready finding

A source-backed resource register makes the remaining modelling gaps more specific. The RUPTL provincial annex identifies named generators and their connections to the Jawa–Bali network, while its development tables contain 294 planning rows across the seven provinces. Of these, 270 rows are labelled Jawa Bali and 24 have other system labels. These are planning records, including capacity quotas, storage, replacements and relocations; they are not 294 confirmed new generating units. The existing-resource register contains 43 named entries, including complex-level names, a reporting portfolio and excluded or unresolved connections. It does not yet cover every operating unit (PLN, 2025a, Annex B).

The planning lists can be checked more closely than a simple sum of published MW suggests. After separating explicitly footnoted replacements, relocations and efficiency additions, the extracted rows reproduce each provincial scenario recap with residuals below 1 MW. Those residuals are retained. This arithmetic bridge does not establish that every listed MW is new nameplate capacity or connected to the main grid: the lists also include isolated projects and storage. Quota allocations must not be added again to the named potential projects that may fulfil them (PLN, 2025a, provincial development tables and footnotes).

Newly archived statistics from PLN Nusantara Power provide named-resource installed and net dependable capacities, annual availability indicators and annual net plant heat rates. These improve the engineering-data pathway, but reporting resources can contain several generators, and the publication has unresolved internal capacity differences. Annual heat rates are average conversion measures, not incremental heat-rate curves. Together with existing annual demand and plant-only generation/emissions samples, these sources support further data preparation; they do not yet support a numerical estimate of the system's marginal emissions response (PLN Nusantara Power, n.d., reporting period 2020–2024, Tables 1–3, 6 and 8).

## Files and row semantics

All generated tables are in [output/jamali_inventory/](output/jamali_inventory/). CSV files open directly in a spreadsheet; this document supplies the interpretation.

| File | Coverage and treatment |
|---|---|
| `existing_resources.csv` | 43 named evidence entries across Java and Bali, mostly plants/complexes; includes reporting portfolio and exclusions. A partial register, not 43 disjoint physical plants |
| `planned_resources.csv` | All numbered rows in the seven selected provincial development lists: DKI 2, Banten 39, West Java 75, Central Java 60, DIY 4, East Java 86, Bali 28. Both scenario COD fields retained |
| `isolated_systems.csv` | 25 named East Java systems, **not** fabricated generating-unit rows; RUPTL PDF p.918 / B-94 |
| `boundary_crosswalk.csv` | Imports, internal transfers, reporting organisations, DIY supply, Tiga Nusa and isolated-capacity exceptions |
| `capacity_observations.csv` | 11 selected NP reporting-resource capacity observations; alternative observations, not extra plants to add to the existing register |
| `annual_operating_characteristics.csv` | Six named-resource 2024 heat-rate/availability examples, exact pages and limitations |
| `reconciliation.csv` | Raw candidate-list comparisons, scenario-specific bridges, existing-fleet benchmark and source conflicts |
| `planning_table_cells.json`, `page_text_snapshots.json` | Re-extractable raw cells and selected full-page text; PDF binaries remain the authoritative layout evidence |
| `sample_*.csv`, `validation.json` | Real local time-profile samples and reproducibility checks; sample metadata below |

`EX-*` and `R25-*` are stable **repository evidence keys**, not official plant or unit IDs. Official plant/unit identifiers remain blank where not established. A named unit group (Suralaya 1–8 or Jawa-7 units 1–2) is not split into invented per-unit capacities. Blank capacity, fuel, commissioning and retirement fields mean unknown, not zero. Technology labels are preserved; PLTU alone is not sufficient evidence to assign a particular fuel specification.

The curated input is [jamali_existing_resource_evidence.json](jamali_existing_resource_evidence.json). Exact source URLs, input hashes and page coverage are in [jamali_inventory_manifest.json](jamali_inventory_manifest.json). Full bibliography is in [REFERENCES.md](REFERENCES.md#resource-inventory-follow-up--11-november-2026).

## Boundary and double-counting rules

1. **Use electrical membership.** Named 150/500 kV connections in Annex B support inclusion; province and operator name alone do not. The Gresik and Grati complexes span voltage levels and each remains one evidence entry. Network topology and terminal-level unit allocation remain unresolved.
2. **Keep overlaps visible.** Tanjung Jati B/Jawa 4 and Cilacap/expansion/Jawa 8 need an alias/unit bridge. They are not summed. NP capacity observations supplement RUPTL names; they are not additional resources. UP Brantas is held as a portfolio pending constituent mapping. No parent PLN total is added to its subsidiaries or regional reporting rows.
3. **Exclude isolated systems until connection is evidenced.** Bawean is explicitly isolated on PDF p.918. Central Java Table B4.3 labels 5.7 MW PLN and 1.6 MW IPP diesel isolated. East Java Table B6.3 labels 69.6 MW PLTM and 3.2 MW PLTMG isolated. The surprising PLTM label is retained for investigation; no unsupported allocation to the 25 systems is made. Tiga Nusa solar is held separately because Table B7.3 does not label its system Jawa Bali.
4. **Separate transfers from generators.** The Java–Bali cable is internal to whole-Jamali accounting; it must not appear as a 380 MW generator or external import. Sumatera energy embedded in projected hydro/geothermal entries is external imported electricity, not proof of a locally connected plant. Its source plants and interval attribution remain unknown.
5. **Separate projected resource roles.** Banten Jawa-5's 1,000 MW is footnoted replacement of oil/gas steam capacity. West Java Muara Tawar's 250 MW is an efficiency addition without added gas consumption. East Java Madura's footnoted 465 MW comprises relocation entries. Each stays in the register, but is excluded in the documented addition-recap bridge. This is not a general assumption that every replacement is zero net capacity.
6. **Do not add quotas, potential lists and storage as if they were independent plants.** Repeated Bedugul, Ijen and Grindulu rows retain their source row IDs; repeated names may denote stages/units, so they are unresolved matches rather than automatically deleted duplicates. Storage MW is power capacity; energy duration is missing. PLTS+BESS values are not split into invented component sizes.

## Reconciliation results and limits

The explicitly selected existing-fleet benchmark is RUPTL Table 5.86, **2025 existing supply**, not a claim of observed 2025 output: 49,616 MW installed and 46,867 MW DMN. Its DMN reporting components reproduce the total: 29,673 own + 17,191 IPP + 3 excess power. The named-resource register is incomplete and overlapping, so it is deliberately not assigned a grid-wide MW sum or coverage percentage against that benchmark.

For all 14 province–scenario comparisons, excluding the page-specific footnoted replacement/efficiency/relocation entries gives absolute differences no greater than **0.65 MW** from the selected recap totals. Exact residuals and source pages remain in the CSV. This is arithmetic consistency, not independent verification of every project or an explanation of the earlier regional/system energy gaps.

Additional conflicts are preserved: Banten's narrative supply groups sum to 9,231 MW, versus 9,253 MW installed in Table B2.3 (PDF pp.824–825). NP's Table 1 category subtotals sum to 18,333 MW, while its displayed total is 18,332 MW (PDF pp.26–27); its headline is 18,333 MW (p.8). Gresik is 2,222 MW on NP p.16 and 2,219 MW in Table 1 p.27. These are source/definition issues pending resolution, not numbers silently corrected by extraction. The visibly unusual non-Java values on NP p.27 are not accepted as a verified national fleet.

## Real time-profile samples and compatibility

| Sample | Frequency, coverage and boundary | Access/documentation and limitation |
|---|---|---|
| RUPTL historical sales copy | Annual 2015–2024, filtered to Jamali, retaining customer groups. Billed GWh, not interval system demand; 2024 source forecast/partial status must be retained | Existing derivative, source RUPTL; hashes recorded. Calendar-year labels, timezone not specified/meaningful as interval timestamps. No aligned interval demand sample obtained |
| Wayang Windu monthly main meter | 42 months, Jan 2018–Jun 2021; two geothermal units, reported MWh with meter adjustments | Revised v04 monitoring report Annex 5, printed pp.90–94; public UNFCCC route. Existing factual transcription, no local report binary. Timezone, day cut-off and gross/net interpretation not independently verified in this step; not grid-wide generation |
| Wayang Windu daily examples | Five non-contiguous dates across 2013–2017; unit DCS generation MWh, steam tonnes, reported steam emissions tCO₂ | Exact report IDs/pages retained in rows and original source register. Dates are not a continuous daily series. Reported project emissions are not whole-Jamali emissions and are not independently measured interval system CO₂ |
| NP annual production/heat-rate evidence | Published annual 2020–2024 tables; annual 2024 NPHR and EAF examples extracted | Tables 3, 6, 8 and definitions p.66. No hourly fuel quantities, incremental heat-rate curves, consistent full-fleet fuel factors or exchange series. Production table headings have unit inconsistencies; no new production values converted into emissions here |

Existing sample URLs and version history remain in `geothermal_ml_data_research/sources.csv` and `output/wayang_windu_audit.json`. Public readability is not an established redistribution licence. No login, restricted access or institutional contact was attempted. A targeted official-source/operator search found no compatible downloadable interval package in this pass. An indexed third-party copy of a UIP2B statistics book is only an unverified lead, not primary numerical evidence.

These samples are genuine but **incompatible in time and coverage**. No hourly rows, timezone, missingness result or grid-wide emissions label has been invented. Neither resampling annual sales nor repeating annual heat rates would create the missing operating-response observations.

## Method-dependent input coverage and feasibility

| Input | Verified improvement | Remaining gap |
|---|---|---|
| Fleet and boundary | Named resources/connections, complete selected planning lists, isolated-system register, imports/internal-transfer rules | Complete official unit IDs and alias bridge, constituent portfolios, captive/embedded generation, full-grid reconciliation |
| Operating conversion and availability | Selected annual NP NPHR and EAF, installed and DMN observations | Unit-level incremental heat rates where required; outages/time-dependent availability; startup, ramps and minimum output for commitment models |
| Economics | Earlier PLN annual fuel-price context; some annual heat rates now identified | Resource/fuel matching, quality/heat-content basis, variable O&M and contract constraints; annual average prices are not marginal costs or future paths |
| Investment/retirement | Candidate status, alternative scenario COD, explicit replacement/relocation flags | Costs, build limits, financing, lifetimes, contracts and resource-specific retirement evidence; source planning dates are not observed commissioning |
| Demand/generation/emissions profiles | Actual annual demand proxy and monthly/daily plant samples documented | Compatible system demand–generation/emissions–exchange intervals, timezone, gross/net definitions, historical overlap and research-use terms |
| Calibration | Reproducible source arithmetic and integrity | Operating/emissions validation, causal identification, and a defined intervention/horizon; no future counterfactual observation exists |

**Decision: roadmap only; neither numerical pilot is cleared.** The existing-resource census remains partial. These findings neither establish CM inferiority nor determine legal eligibility or demonstrated MEF accuracy. Short-run work holds the fleet fixed; long-run work requires justified capacity responses. A finite project/no-project scenario remains different from a local marginal derivative.

**Next bounded task:** obtain and inspect one official unit/plant roster for the missing PLN Indonesia Power and IPP resources, using the selected 49,616 MW/46,867 MW source definitions as benchmarks. Resolve the named alias/portfolio matches and report covered, excluded and unresolved MW separately; stop after that roster audit. Keep interval-data acquisition as an independent gate rather than starting a dispatch fit from annual averages.

## Reproduce and inspect

```sh
python3 -B mef_research/build_jamali_inventory.py
python3 -B mef_research/audit_jamali_planning_inputs.py
python3 -B mef_research/audit_review_sources.py
```

Requires PyMuPDF (`fitz`); table extraction was checked with version 1.26.5. The build checks input SHA-256, unique evidence IDs, contiguous source row numbering, 294 populated planning rows, scenario-recap residuals below 1 MW and sample uniqueness. Selected full pages RUPTL 818/916 and NP 27/42 were rendered and inspected visually. The DKI table detector's row split is explicitly corrected from the visible page; raw cells remain available. All 294 planning rows are populated but have not received independent second-person verification. Passing checks establishes reproducibility and bounded consistency, not modelling accuracy. Earlier model outputs remain unchanged.
