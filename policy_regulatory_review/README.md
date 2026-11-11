# FINCAPES: targeted regulatory evidence review

> **Research-direction update:** this review is retained as policy background for the [active Jamali MEF-readiness mission](../mef_research/MISSION.md). The CM-weight experiment specified below belongs to the previous direction and is deferred, not the current next task. No legal findings below are changed by this project-scope update.

Review date: **6 November 2026**. Stage A completed: bounded documentary review, not an exhaustive legal opinion or an approval of a crediting project. No model inputs, weights or existing results were changed.

## Purpose

Assess whether existing Indonesian requirements already address CM selection, reporting and review before proposing a policy change. The main emissions research question remains unchanged. The policy extension asks whether selection, justification, disclosure and review of geothermal grid factors are sufficiently clear and supported in practice.

**Main finding:** the reviewed framework is not a regulatory vacuum. The 2021 factor decree already distinguishes technology-specific CM columns. Numerical sensitivity alone cannot establish that a prescribed weighting is wrong, or that legislation must change.

## Evidence matrix

“Verified” below means the identified provision was checked, not that it governs every project today. PDF page references are one-based. Source URLs, acquisition boundaries and checksums are in [source_manifest.json](source_manifest.json).

| Source | Verified provision | Research implication and boundary |
|---|---|---|
| Kepmen ESDM 163.K/HK.02/MEM.S/2021 | Annex p.13 assigns columns 7/9 (OM 0.5, BM 0.5) to mitigation activities except wind/solar; columns 8/10 (0.75/0.25) are for wind/solar. Diktum KETIGA, p.4 permits changes following Directorate General of Electricity data updates. | Geothermal falls within the non-wind/solar category **in this decree**. Do not present alternative weights as freely selectable compliance options. An update provision already exists. This is a 2019-data snapshot, not proof of applicability through 2034 or across programmes. |
| Permen ESDM 22/2019 | Pasal 8(1)–(3), p.8: annual activity-information collection; institutional responsibilities for factor calculation; ministerial establishment of electricity-system factors on the DG's proposal. | There is an existing institutional route. Annual activity collection does not itself establish an annual CM publication requirement. Current institutional arrangements and later amendments must be checked for implementation. |
| Permen ESDM 16/2022 | Pasal 14–16, pp.9–10 distinguish trading/offsets and include renewable-generation offset activities subject to certification requirements. Pasal 21–22, pp.12–13 address activity reporting; Pasal 25, p.14 verification. Pasal 32(3), p.16 provides six-monthly evaluation of NEK implementation. | Renewable generation is not automatically issued credits. Existing reporting and verification should not be described as absent. Six-monthly implementation evaluation is **not** a requirement to reset CM weights every six months. Continued application must be read with newer rules. |
| Perpres 110/2025 | Pasal 81(4)–(5), pp.54–55 includes baseline calculations, reference periods, assumptions and methodology in technical reporting. Pasal 84–86, pp.57–58 covers validation/verification. Pasal 100–103, p.67 provides transition, repeal of Perpres 98/2021 and commencement. Promulgation: 10 October 2025, p.68. | Reporting and independent assurance already have a framework. Earlier implementing rules are preserved subject to the transition clause; neither wholesale invalidation nor unconditional continued applicability should be assumed. This regulation does not itself establish an empirically optimal CM weight. |
| Permen LH/BPLH 10/2026 | Official metadata records enactment 2 July, promulgation/effect 6 July 2026 and status “Berlaku.” Full text, Pasal 46, p.23 addresses transition for existing offset activities. | Include SRUK-era procedures when assessing a present-day project. Registry transition is not a numerical CM-selection rule. Reviewed online; no local PDF successfully archived. |
| UNFCCC A6.4-AMT-007 v02.0 | Official version page: valid from 9 October 2026. Section 5.7.1.4, paras 101–103, pp.32–33 specifies CM calculation, conditional default weights and conservative selection, subject to the referring methodology. | This is an Article 6.4 methodological tool, **not automatically Indonesian domestic law**. Applicability depends on programme, methodology, category and version. An Indonesian historical factor table and an international tool must not be blended into one rule. Reviewed online; no local PDF archived. |

The current official SRUK information page also identifies Perpres 110/2025 and Permen LH/BPLH 10/2026. Its “soon” label for energy-sector implementing regulation is a portal statement, not proof that no later energy rule exists.

## What the evidence supports

1. **Verified requirement:** selection categories and update authority already exist in the examined decree. Any recommendation must acknowledge them.
2. **Research inference:** material sensitivity makes traceable selection important; it does not identify a true weight or demonstrate noncompliance.
3. **Candidate policy proposal:** assess whether an accessible, versioned factor register and a standard project-level factor disclosure sheet would improve implementation of existing requirements. This is a proposal for assessment, not a demonstrated missing legal duty.
4. **Not established:** that 50/50 is physically inaccurate; that a different weight would improve accuracy; that all programmes require the same weighting; or that a statutory amendment is necessary.

## Candidate implementation package, not a final amendment recommendation

The research can develop a compact disclosure template recording:

- grid boundary and interconnection treatment;
- official source, underlying data years, document/version and applicability dates;
- OM/BM values, prescribed weights, CM ex-ante/ex-post status and selection rationale;
- generation boundary, timing and capacity-factor assumptions;
- project-emissions deductions and separate eligibility/verification requirements;
- sensitivity results labelled as analytical scenarios, not selectable credit claims;
- responsible authority and a link to the applicable update or transition notice.

**Decision rule:** if the complete current methodology already requires these items, recommend implementation, accessibility or enforcement only where an implementation audit demonstrates a problem. If a material requirement is genuinely absent, identify the lowest appropriate instrument—guidance, template, decree or regulation—before recommending amendment. If no relevant gap is demonstrated, report that result rather than forcing a law-change conclusion.

## Unresolved applicability checks

This bounded review did not obtain an authoritative approved text/version and approval record for the geothermal methodology identified in secondary discovery as **MSEP-011**. No claimed “lower of ex-ante/ex-post” selection rule from that secondary account is adopted here. Failure to retrieve the text is **not evidence that no methodology or selection rule exists**.

The full chain of subsequent energy-sector instruments, programme-specific decisions and all 2026 NDC implementing provisions has not been exhaustively audited. In particular, a discovery lead for Permen LH/BPLH 7/2026 was not verified against primary text. Check these before issuing a project-compliance or final legal-amendment recommendation. Historical TOOL07 is background in the existing report, not treated as the universally current rule.

## Next numerical stage — specified, not performed here

Run a controlled **CM-weight sensitivity**, separate from the earlier multi-method comparison:

- Hold the same mapped projects, 2025–2034 window, original schedule, one-year start lag, 80% capacity factor and 8,760-hour year fixed.
- Use the same published 2019 OM/BM pair within each grid. Compute analytical CM as `w_OM * OM + (1 - w_OM) * BM`.
- Compare illustrative OM weights 0, 0.25, 0.50, 0.75 and 1, clearly distinguishing mathematical endpoints from a CM policy recommendation. No weight is labelled optimal or automatically eligible.
- Show electricity held fixed, derived factor, gross emissions and differences from the **reconstructed** 50/50 case, not from a different vintage/programme factor.
- Preserve the published CM columns. Their rounding/internal precision means reconstructed 50/50 need not reproduce every published value exactly; explicitly report that distinction rather than silently changing the baseline.
- Validate endpoints, weights summing to one, arithmetic, constant generation and annual-to-cumulative reconciliation. Keep timing and coal/gas replacement comparisons separate.

This test measures how consequential weighting is, not which weight is empirically correct. Establishing physical superiority would require a defined counterfactual model and appropriate independent operational evidence. GDP or resampling existing observations cannot supply that missing target by themselves.

## Audit trail and reproduction

Four primary PDFs are archived unchanged under `raw/`. The existing seven-page factor-table file in `grid_data_sources/raw/` remains untouched; the newly archived decree has **13 pages including its operative provisions**. Scanned sources were checked using rendered pages, not assumed readable from empty text extraction. The manifest records pages reviewed and SHA-256 hashes. Online-only sources are explicitly marked as such.

Use [report_policy_section.md](report_policy_section.md) for copy-ready prose. This review changes the research framing, not the original emissions calculations. No new accuracy result or CM-weight experiment is claimed.
