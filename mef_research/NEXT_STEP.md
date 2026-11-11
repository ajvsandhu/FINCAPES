# Next step: Jamali generator inventory and boundary mapping

## Latest handoff: final readiness assessment completed

Read [FINAL_READINESS.md](FINAL_READINESS.md). No numerical Jamali MEF is supported by currently accessible evidence; the binding gap for every short-run route is time-aligned interval demand plus generation by unit/fuel. Recommended first pilot: M1 historical regression, conditional on one year of half-hourly UIP2B data. A data request is drafted but **not sent**.

**Next decision (user):** authorise or decline sending the drafted request to PLN UIP2B/ESDM. If authorised and data arrive, run the M1 pilot as specified in the assessment. If declined, the deliverable is the readiness assessment plus the clearly labelled CM accounting benchmark. Do not resume open-ended source searching.

## Earlier handoff: operating-data sample check completed (incompatible)

Read [OPERATING_SAMPLE_CHECK.md](OPERATING_SAMPLE_CHECK.md). The one inspected candidate, the Zenodo *Jamali Power System Dataset* v1.0.0 (CC BY 4.0, 9 May 2026), contains no data records — only README, licence and `.gitignore` — and its linked GitHub repository returns 404. Screened leads were scenario profiles (2030/2035), unpublished PLN UIP2B half-hourly load used in theses, or country-level commercial estimates. No compatible interval package is verified; neither numerical pilot is cleared.

**Next bounded task:** do not resume source hunting. Consolidate the completed evidence into a final method-dependent readiness assessment and implementation recommendations: per MEF route, what existing evidence supports, what is missing, and the precise data request that would unlock it. Drafting a request is allowed; sending it to PLN/ESDM is institutional contact and needs fresh authorisation. No commits, pushes, branches or delegation.

## Earlier handoff: dated IPP/other-PLN identity audit completed

Read [IPP_ALIAS_AUDIT.md](IPP_ALIAS_AUDIT.md) and reproduce with `python3 -B mef_research/audit_ipp_aliases.py`. Using the ESDM national vital-object register of 28 November 2024 (Kepmen 310.K/BN.05/MEM.S/2024, rows 127/132/136) as the membership anchor, six earlier aliases map to 12 descriptive unit labels at three sites: Tanjung Jati B 1–4, TJB 5–6 (= Jawa 4), Cilacap S2P 1/2/3/3A (3A = Expansion II = Jawa 8) and Batang 1–2 (Jawa Tengah PPP). Adipala, Rembang, substations and other register controls are not added as new generators. Matched annual installed/Daya Mampu exists only for the original TJB four-unit reporting group (2,811.40 / 2,643.80 MW, PLN 2024); the other eight labels have nominal/project MW only. No mixed-basis total, official unit IDs or coverage percentage is produced. Neither numerical pilot is cleared.

**Next bounded task:** stop fleet-source hunting. Locate and inspect one actual Jamali operating-data sample/schema: matching timestamps for demand and generation plus emissions or compatible fuel-construction inputs, with exchange/boundary metadata. Record timezone, frequency, gross/net definitions, coverage, missingness and access terms. Stop after one sample compatibility decision or a documented bounded access failure; if none is obtainable, consolidate the evidence into a final method-dependent readiness assessment. No commits, pushes, branches, delegation or institutional contact without fresh authorisation.

## Earlier handoff: official PLN IP roster audit completed

Read [IP_ROSTER_AUDIT.md](IP_ROSTER_AUDIT.md) and reproduce with `python3 -B mef_research/audit_ip_roster.py`. The official 2024 report is archived with provenance through the official statistics index and viewer. Table 13 yields 142 national plant/group rows and 476 visible machine-capacity cells; source count is 475, with the Grati conflict held unresolved. Thirteen alias/parent crosswalks include Suralaya 1–8, Priok/Senayan and Lontar owned/O&M bridges. The roster is an additional evidence layer, not plants to append blindly to the old register. Neither numerical pilot is cleared.

**Next bounded task:** audit one official IPP/other-PLN roster for a consistent historical reference date, prioritising Tanjung Jati B/Jawa 4 and Cilacap/expansion/Jawa 8. Produce a dated union with installed/DMN definitions, resolved aliases, exclusions and an unresolved bucket. The 2024 IP company roster is not directly comparable to the RUPTL 2025 existing-supply benchmark; no coverage percentage is established. Stop at reconciliation. Interval demand/generation/emissions/exchange acquisition remains an independent gate. No commits, pushes, branches, delegation or institutional contact without fresh authorisation. Post actual findings and copy-ready prose in chat as well as saving them in the repo.

## Updated handoff after the 11 November resource pass

The work below has now produced a [bounded resource register and assessment](JAMALI_RESOURCE_INVENTORY.md), not a complete unit census. Start with that finding and `output/jamali_inventory/validation.json`. The register contains 43 existing named evidence entries, all 294 numbered rows from the selected provincial planning lists, and 25 isolated East Java systems. NP annual heat rates and availability improve engineering coverage. Neither numerical pilot is cleared; no complete interval demand/generation/emissions/exchange package was obtained.

**Next bounded implementation:** obtain and audit one official missing-fleet roster covering PLN Indonesia Power and/or IPP resources. Resolve official IDs, plant/unit aliases and constituent portfolios against the explicitly selected RUPTL Table 5.86 2025 existing-supply definitions (49,616 MW installed; 46,867 MW DMN). Report covered, excluded and unresolved MW separately. Do not sum the present overlapping named entries or treat the current 2026 date as evidence that a planned unit commissioned. Stop at the roster reconciliation; interval data remain a separate gate.

Reproduce with `python3 -B mef_research/build_jamali_inventory.py`. Source snapshots, raw cells, hashes and limitations are documented in the new assessment and manifest. Keep no-commit/no-push/no-branch/no-delegation/no-contact safeguards. Earlier instructions below are retained as the scope of the completed bounded pass, with full fleet coverage still unfinished.

## Original inventory scope

Handoff updated **11 November 2026**. The research is continuing; the current methods-and-readiness stage is complete, not the overall project. Read [MISSION.md](MISSION.md), [REPORT.md](REPORT.md) and [JAMALI_INPUT_AUDIT.md](JAMALI_INPUT_AUDIT.md) first.

## Immediate task

Build a source-backed inventory of generators connected to the interconnected Jamali grid. Separate existing units, planned candidates, isolated systems and electricity imported from other grids. Do not start model training or manufacture missing operating data.

For each plant/unit, record identifier, technology/fuel, location, electrical connection, operating/planned status, reporting organisation, installed and dependable capacity where available, commissioning/retirement evidence, source URL/page/date, and unresolved fields. Distinguish plant totals from unit rows to prevent double counting. Preserve published values and revisions.

Reconcile totals against explicitly chosen source definitions. Record excluded isolated plants and unresolved matches; a regional total is not automatically the interconnected-system total. Do not infer the cause of the previously measured regional/system gaps without evidence.

In parallel, seek a real sample of time-stamped demand, generation and emissions or compatible emissions-construction inputs. Record resolution, timezone, gross/net definitions, coverage, exchanges, missingness and access terms. Annual prices require heat rates and other costs before they become generator marginal costs; they are not future cost paths.

## Deliverables and stopping point

1. Reproducible inventory, input snapshots and source register.
2. Boundary crosswalk and reconciliation checks, with unresolved differences visible.
3. Coverage table for operating characteristics, economics, time profiles and exchanges.
4. Short report-ready finding: whether a numerical route is now supported, what remains missing, and one bounded next task.

Missing fields remain missing. Neither a populated inventory nor a good emissions forecast alone establishes a credible MEF. A finite geothermal project/no-project comparison must be distinguished from a local marginal derivative. Do not claim MEF superiority, legal applicability or improved accuracy without supporting evidence.

## Notes for the working document

- Call the data-requirements table a **method-dependent checklist**, not a universal minimum: not every method requires dispatch instructions, unit commitment records or a full network model.
- Remove pasted citation artifacts such as `citeturn235520search0`; retain author–year citations and use [REFERENCES.md](REFERENCES.md) for the bibliography.
- Describe the targeted planning audit as completed. Its full boundary bridge and the generator inventory remain unfinished; no numerical Jamali MEF has been estimated.

## Working safeguards

Keep earlier fixed-factor, timing and plant-output ML work as background. Keep full reference URLs in the repository. Do the work directly unless delegation is specifically useful and authorised; no new agent is necessary for this inventory task. Do not send institutional messages without approval. The 11 November request authorises publishing the current research checkpoint, not future automatic commits or pushes. Leave unrelated `.DS_Store` files untouched.
