# Official PLN Indonesia Power roster audit

Completed **11 November 2026**. One bounded official-roster audit; no numerical MEF or full-grid coverage claim. This follows the [first resource register](JAMALI_RESOURCE_INVENTORY.md). The earlier 43 named evidence entries remain preserved; the new national roster is a separate, cross-referenced layer, not additional plants to append and sum blindly.

## Report-ready findings

The follow-up acquired PLN Indonesia Power's official *Laporan Statistik 2024* through the company's statistics index and its linked public document viewer. The report distinguishes company-owned capacity from capacity operated under operation-and-maintenance contracts and provides a table of installed capacity by plant and machine. The audit extracted 142 plant/group rows and 476 nonblank machine-capacity cells from that national table. The cells are source observations, not 476 independently verified operating units: the source's row-level machine counts sum to 475, and Grati contains an unresolved count/capacity conflict (PLN Indonesia Power, n.d., reporting year 2024, Tables 9–13).

Several overlaps can now be handled explicitly. Suralaya 1–7 totals 3,400 MW in the report, and the separately reported Suralaya 8 contributes 625 MW, reproducing the RUPTL's 4,025 MW Suralaya 1–8 grouping. LBE remains a separate name and must not be merged merely because its capacity is also 625 MW. Priok's 2,947 MW reporting total includes 2,841.70 MW labelled Priok and 105.30 MW at Senayan. Lontar comprises 945 MW in the owned-capacity table and 315 MW under O&M; these reproduce its 1,260 MW plant-group total without adding the same capacity twice (Tables 9, 11 and 13; PLN, 2025a, PDF p.824).

The audit also shows why reporting portfolios cannot define the electrical boundary. The Kamojang portfolio includes geothermal resources outside Java, while the Semarang and Bali portfolios include island resources that must be separated from main-grid generation. A provisional resource-level crosswalk maps 16,704.07 MW of the audited plant totals to main-Jamali resources, holds 362.53 MW unresolved, excludes 33.28 MW of isolated resources and excludes 4,802.05 MW outside Jamali. These are partitions of this particular national roster, including owned and O&M resources, not a census of all Jamali generators. Smaller hydro connections and dated Jatigede membership remain unresolved; source-local machine numbers have not been promoted to official unit identifiers.

The result improves fleet documentation but does not close the modelling gate. The new roster supplies installed capacity; it does not supply a complete, matching set of dependable capacities, chronological operating records, commissioning/retirement evidence or official unit identifiers. Its 2024 reporting scope cannot be divided directly by the RUPTL's 2025 existing-supply benchmark to claim a verified fleet coverage percentage. Neither short-run nor long-run numerical MEF estimation is cleared.

## Source and reproducibility

- Official index: https://www.plnindonesiapower.co.id/laporan-statistik
- Official linked viewer: https://ipstore.plnindonesiapower.co.id:1996/statisticreport2024/
- PDF exposed by the viewer's enabled download configuration: https://ipstore.plnindonesiapower.co.id:1996/statisticreport2024/files/downloads/Laporan_Statistik_IP_2024.pdf
- Local snapshot: `raw/pln_ip_statistics_2024.pdf`, 76 pages, reporting year 2024. Publication date not established; do not assign a publication year from the reporting title alone.
- [Manifest](ip_roster_manifest.json): source routes, hashes, inspected pages, access and evidence limits. Public read access does not establish a redistribution licence. No login, contact or institutional request occurred.
- [Output folder](output/ip_roster_audit/): `plant_roster.csv`, `machine_cells.csv`, `alias_crosswalk.csv`, `ownership_controls.csv`, `capacity_reconciliation.csv`, `source_conflicts.csv`, source text/position snapshots, chart and `validation.json`.

```sh
python3 -B mef_research/audit_ip_roster.py
```

Requires PyMuPDF 1.26.5 and Matplotlib. Coordinates are rotated in memory to read the landscape Table 13; the archived PDF is unchanged. Input hashes, 142 plant rows, 476 observed machine cells, unique row keys/columns, capacity partitions and roster-wide controls are checked. Source text and positioned words preserve evidence for each row. All six Table 13 pages and selected ownership-control pages were rendered and visually inspected. Extraction is not an independent engineering verification of each machine.

## What the rows mean

- Plant/group totals are the aggregation controls. Parent business-unit totals and their machine/plant children must never be summed together.
- `I3-P...` keys are repository evidence IDs. `source_local_column` records a numbered column in Table 13, not an official station-wide or regulatory unit identifier. A combined-cycle block's machine columns must not be assumed to be independently dispatchable generating blocks.
- Source `*` flags denote O&M resources, following Table 9's note and Table 11 controls. Owned and managed resources remain visible, but management does not establish ownership or the absence of another reporting parent.
- Capacity is installed/nameplate as defined on PDF p.74, not DMN. Blank dependable capacity, fuel specification, commissioning and retirement dates remain unknown. Operational inclusion is limited to the source's 2024 reporting context, not verified current 2026 status.
- Boundary membership is stricter than geography. Named plants with source connections are mapped; smaller Saguling/Mrica hydro rows are held unresolved where constituent terminal evidence was not checked. Jatigede is held unresolved because an O&M roster entry and a future planning entry need a dated bridge. Excluded capacities do not explain the earlier regional/system energy differences automatically.

## Explicit reconciliation and unresolved matches

| Check | Result | Interpretation |
|---|---|---|
| National Table 9 owned row sum | 20,843.50 MW versus printed 20,843.51 MW | Retain −0.01 MW source/rounding residual |
| Table 13 child plant totals | 21,901.93 MW versus 20,843.51 owned + 1,058.39 O&M = 21,901.90 MW | Retain +0.03 MW residual; do not force balance |
| Suralaya 1–8 | 3,400 + 625 = 4,025 MW | Exact installed group bridge to RUPTL p.824; no proof of a DMN bridge |
| Lontar | 945 owned + 315 O&M = 1,260 MW | Ownership/management distinction explains overlapping totals |
| Mrica portfolio | Table 9 333.78 MW; Table 13 333.79 MW | Preserve 0.01 MW conflict; PB. Sudirman alone is 180.90 MW and is not the whole portfolio |
| Grati block 1 | Printed 2 machines / 260.33 MW; three visible machine cells sum to 276.97 MW | 16.64 MW extra cell retained, not deleted or accepted as a verified third machine; hold machine-level use |
| Mahakam Bontang diesel | Child cells 10.16 MW; printed plant total 10.18 MW | Outside Jamali; retain −0.02 MW discrepancy |

The existing RUPTL benchmarks remain **49,616 MW installed** and **46,867 MW DMN**, Table 5.86 2025 existing supply. Those are system planning definitions, whereas the new national company roster is dated 2024 and mixes owned/O&M coverage. No subtraction is called “missing Jamali capacity”: differences would conflate year, system, ownership and capacity basis. PLN NP, other PLN resources, IPPs and captive/embedded generation still require a consistent dated union. The Tanjung Jati B/Jawa 4 and Cilacap/expansion/Jawa 8 aliases remain unresolved because this IP roster does not cover them sufficiently.

The 13-row alias crosswalk links earlier evidence keys to the new source rows. It resolves source grouping and avoids parent/child duplication; it does not assert a complete legal-owner or official unit-ID match. Kamojang, Salak and Darajad here cover only the source's named machine groups, not every geothermal operator or future candidate at those fields.

## Coverage and next bounded task

| Input | Position after this audit |
|---|---|
| Named resources and machine capacities | Official installed-capacity cells acquired; plant/group controls and 13 alias links recorded |
| Electrical boundary | Main-grid, unresolved, isolated and outside-Jamali partitions documented; smaller hydro and dated Jatigede membership held unresolved |
| Ownership and reporting | Owned/O&M distinction reconciled; parent totals excluded from resource summation |
| Dependable capacity and operating limits | Still no complete matched unit-level package; installed MW must not substitute for DMN |
| Commissioning and retirement | Dates/official unit IDs remain blank unless supported elsewhere; age or planning COD is not proof |
| Demand, generation, fuel/emissions and exchanges | No new compatible interval package acquired; earlier real but incompatible samples retain their limits |
| Full fleet | Company roster is not a full Jamali fleet; IPP and other-PLN coverage still unresolved |

**Next bounded task:** audit one official IPP/other-PLN roster for the same historical reference date, prioritising the Tanjung Jati B/Jawa 4 and Cilacap/Jawa 8 overlaps. Produce a dated union of resource rows with explicit installed/DMN bases and retain an unresolved bucket. Stop after this reconciliation; do not initiate dispatch fitting. Interval-data access remains an independent gate, and no institutional contact is authorised.
