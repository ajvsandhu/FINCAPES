# Dated IPP/other-PLN identity and capacity audit

Completed **11 November 2026**. This is the bounded follow-up to the [PLN IP roster audit](IP_ROSTER_AUDIT.md), using one dated official register and targeted primary corroboration. It resolves identities within a selected subset; it is not a full Jamali census, a new dispatch dataset or an MEF estimate.

## Copy-ready findings

The follow-up reconciled several overlapping generator names using ESDM's national vital-object register dated 28 November 2024, operator information and official historical releases. Jawa 4 is Tanjung Jati B units 5–6, distinct from the original units 1–4. At Cilacap, the original units 1–2, Expansion I and Expansion II are separate groups. Jawa 8 is Expansion II, corresponding to the operator's Unit 3A. Batang/Jawa Tengah PPP belongs to Bhimasena Power Indonesia and is distinct from Bhumi Jati Power's Jawa 4. Six earlier register entries are mapped to 12 descriptive unit labels across three sites, with the November 2024 register as the common membership anchor (ESDM, 2024, rows 127, 132 and 136; Sumber Segara Primadaya, n.d.; ESDM, 2017, 2020; Bhimasena Power Indonesia, 2023).

The investigation also establishes why different MW figures must not be treated as equivalent. PLN Statistics 2024 reports 2,811.40 MW installed and 2,643.80 MW of Daya Mampu for the original Tanjung Jati B reporting group. Other sources give different nominal or project capacities for the same groups without establishing a complete conversion between them. These observations are retained separately rather than averaged or silently corrected (PLN, 2025b, Tables 1, 20–22; ESDM, 2024, row 136).

For Jawa 8, the capacity distinction is explicitly documented. ESDM's February 2020 release states 1,000 MW total capacity, including 55 MW for plant use and 945 MW supplied to PLN. This is a source-backed capacity bridge; it is not a measurement of hourly output or annual dependable capacity. Likewise, an investor's equity-equivalent MW is a financial attribution and must not be counted as an additional physical generating unit (ESDM, 2020; Kansai Electric, n.d.).

This audit resolves selected identity overlaps but leaves a full, consistently dated installed/dependable fleet unresolved. Official registry identifiers, compatible interval demand, generation, fuel/emissions and exchange records remain missing. Neither the short-run nor long-run numerical MEF route is cleared. The next step should now be a bounded operating-data sample and schema check, rather than extending the fleet-source search indefinitely.

## Sources, dates and evidence depth

Exact URLs, SHA-256, access outcomes and evidence limits are in [ipp_alias_manifest.json](ipp_alias_manifest.json). New snapshots are under `raw/`; output tables and source-page images are under [output/ipp_alias_audit/](output/ipp_alias_audit/).

| ID | Evidence inspected | What it supports and does not support |
|---|---|---|
| I4 | Kepmen ESDM No.310.K/BN.05/MEM.S/2024, 28 November 2024; PDF pp.1,4,51–53 | Target equipment/entity groupings in rows127/132/136 and five control rows. Full 72-page scanned PDF acquired; selected rows manually transcribed from rendered pages. This is a vital-object designation list, not a complete operational unit census or a legal-eligibility opinion |
| I5 | Sumber Segara Primadaya operator profile, retrieved11 November2026 | Four Cilacap unit labels, nominal capacities and retrospective COD months. Undated live page is not relabelled as an archived2024 operating roster |
| I6 | ESDM press release073.Pers/04/SJI/2020,17February2020 | Jawa8/ExpansionII alias, operation by late2019, explicit total/own-use/PLN-supply bridge; Adipala separate from S2P site groups. No hourly observations |
| I7 | Kansai Electric project page, full web-tool text inspected; selected factual transcription archived | Units5–6, capacity2140MW, equity-equivalent535MW and project commercial-operation month September2022. Direct curl403 retained; snapshot is not rawHTML. Gross/net/DMN conversion not established |
| I8 | ESDM fact sheet31August2017, especially items3–6 | Original versus expansion unit names and historical nominal capacities. Its planned2021 COD dates are not accepted as realised commissioning dates |
| I9 | BPI operator release22July2023 about15July visit | Batang unit1 COD15August2022, unit2 COD31August2022 and500kV connection context. Unrelated Jawa1 wording is not used to identify another resource |
| J2 | Existing official PLN Statistics2024, PDF19/58/60/62 | UIK Tanjung Jati B four-unit reporting count, installed and Daya Mampu annual values. No invented allocation of group MW among units |

## Dated union and capacity treatment

The [dated identity union](output/ipp_alias_audit/dated_identity_union.csv) uses **28 November2024** as a common membership anchor because that is the date of I4. It combines twelve descriptive labels: TJB1–4, TJB5–6/Jawa4, S2P1/2/3/3A, and Batang1–2. Listing, pre-anchor operating evidence and retrospective COD reports support identities; they do not establish interval availability or rule out every subsequent retirement. The annual PLN capacity observations are explicitly dated to the2024 year-end reporting basis and are **not assigned to28November** as if they were measured then.

`resource_key` is a repository crosswalk key. `official_registry_unit_id` remains blank. The source labels “Unit3A” and “Unit5” are descriptive unit numbers, not proof of a national regulatory identifier. Unit-level installed and dependable fields remain blank where only nominal/project figures or a group total are supported. No flat per-unit division of the TJB group installed/DMN totals is performed.

| Earlier alias | Disposition in the partial union |
|---|---|
| EX-020 Tanjung Jati B | Original units1–4 reporting group; whole-site usage can be broader, so retain exact source scope |
| EX-025 Jawa4 | TJB units5–6; no additional Jawa4 pseudo-plant |
| EX-027 Cilacap | Original units1–2 in this RUPTL grouping; distinguish from the operator's whole-site name |
| EX-022 Cilacap Exp | ExpansionI/Unit3 supported by the separate Jawa8 entry and official660MW expansionI wording; generic “expansion” alone remains ambiguous |
| EX-023 Jawa8 | ExpansionII / operator Unit3A; one resource, not three plants |
| EX-024 Jawa Tengah PPP | Batang units1–2, PT Bhimasena Power Indonesia; separate site/company from PT Bhumi Jati Power |

Adipala's660MW is a separate plant in Cilacap regency and already appears in the IP roster; it is not a fifth S2P unit to add to that company's2260MW site total. Rembang is also already represented in NP evidence; its register appearance is a control, not additional630MW. GI/GISTET/GIS, reservoirs, transmission and control centres are not generator rows. Mrica/PB Sudirman naming is corroborated by row134, but register180MW and annual source180.90MW remain distinct observations. PLTG Lomanis and Tambak Lorok register capacities are controls with unresolved status/definition matching, not extra generators appended to the union.

## Capacity reconciliation and remaining coverage

| Quantity | Verified result | Interpretation |
|---|---|---|
| S2P four-unit nominal capacity | 300+300+660+1000=2260MW | Operator nominal total; no annual DMN claim |
| Jawa8 source capacity bridge | 1000−55=945MW | Explicit2020 release, not a2024 dispatch measurement |
| Geographical Cilacap group in2020 release | S2P2260+separate Adipala660=2920MW | Geography is not one operator's fleet |
| TJB original group, PLN2024 | 2811.40MW installed;2643.80MW Daya Mampu;4 units | Two labelled annual quantities, not interchangeable |
| TJB original group, I4 | 1420+1420=2840MW versus annual installed2811.40MW | 28.60MW unresolved definition/source difference, not allocated to losses/own-use |
| TJB original group, I8 | 4x660=2640MW historical nominal | Not automatically annual installed or Daya Mampu |
| TJB5–6, I4 versus sponsor I7 | 2000MW versus2140MW | Different observations;140MW difference retained, no unsupported gross/net bridge |
| Kansai equity-equivalent capacity | 535MW=25% of2140MW | Financial attribution; excluded from physical capacity sums |

For the targeted subset, explicit matched annual installed/Daya Mampu information is available only for the four-unit original TJB **reporting group**. The other eight target labels have nominal/project observations, not a verified same-date installed/DMN pair. None of the twelve labels has acquired a fully matched **unit-level** installed/DMN pair in this step. These statements do not describe all data held by the operators.

The RUPTL2025 existing-supply benchmark remains49,616MW installed and46,867MW DMN. A full benchmark residual or covered percentage is **not computed** from a partial identity union with mixed source capacity definitions and dates. The earlier IP and NP layers remain separate, with aliases linked rather than blindly appended. Isolated and outside-Jamali exclusions from the earlier audits are preserved. The three target sites are mapped to main-Jamali membership; missing capacity definitions remain an unresolved bucket rather than assumed zero.

## Reproduce and stopping decision

```sh
python3 -B mef_research/audit_ipp_aliases.py
python3 -B mef_research/audit_ip_roster.py
python3 -B mef_research/build_jamali_inventory.py
python3 -B mef_research/audit_jamali_planning_inputs.py
python3 -B mef_research/audit_review_sources.py
```

New audit requires PyMuPDF and Matplotlib plus Python's standard library. It verifies input hashes, key HTML markers, twelve unique/non-overlapping unit keys, six alias links, selected annual PLN row values and explicit capacity arithmetic. The scanned decree's manual transcription is retained in `selected_official_register_rows.csv`; render snapshots allow a reader to check it against the original. Manual transcription is not an independent engineering verification. Checks do not establish model accuracy or causal identification.

**Stop fleet-source hunting at this checkpoint.** The next bounded task is to locate and inspect one actual Jamali operating-data sample/schema: matching timestamps for demand and generation plus emissions or compatible fuel-construction inputs, with exchange/boundary metadata. Record timezone, frequency, gross/net definitions, coverage, missingness and access terms. Stop after one sample compatibility decision or a documented bounded access failure. If no compatible sample is obtainable, consolidate the completed evidence into a final method-dependent readiness assessment and implementation recommendations rather than fitting unsupported models or continuing unrestricted searches. No institutional contact, commits, pushes, branches or delegation are authorised.
