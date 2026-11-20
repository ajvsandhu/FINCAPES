# Credibility protocol: when a model-based MEF may inform assessment of CM

**Status:** Stage-closing protocol for this readiness research (20 November 2026).  
**Not yet applied:** no Jamali MEF has been estimated; this document defines how a future estimate would be judged before anyone argues it should inform—or displace—combined-margin (CM) use.

Related: [MISSION.md](MISSION.md), [FINAL_READINESS.md](FINAL_READINESS.md), [METHODS_REVIEW.md](METHODS_REVIEW.md), [REPORT.md](REPORT.md).

---

## 1. Policy motivation: carbon credits (context, not a deliverable)

Geothermal projects may seek **carbon credits** or related emissions accounting. In that setting, **CM** (typically an operating-margin / build-margin blend under a stated methodology version) is often the published factor used to quantify displaced grid emissions.

This research treats carbon crediting as the **why** for assessing CM, not as a completed finding:

| Include as context | Do not claim from this stage |
|---|---|
| Credits motivate why CM vs operational response matters | That Indonesian rules are wrong |
| CM is the accounting benchmark used in many crediting workflows | That MEF must replace CM for credit issuance |
| A validated local MEF could *inform* whether CM is a good proxy for displaced emissions | Credit volumes, eligibility, or issuance for any project |
| Accounting compliance, operational MEF, and credit issuance are distinct questions | That this study has validated a factor for use in crediting |

**Copy-ready sentence for the report:**

> Carbon crediting is the policy context for assessing the combined-margin approach. This study designs a pathway to estimate marginal emissions effects for Jamali; it does not determine credit eligibility or issue factors for use in crediting.

---

## 2. What “credible enough” means

CM and MEF answer different questions:

- **CM** — an accounting rule (published OM + BM weights/factors under a methodology).
- **MEF** — an estimate of a physical (or modelled) emissions response to a defined perturbation.

Therefore credibility is **not** “the model beats CM on R²,” and MEF must **not** be scored against CM as physical truth. Credibility means the estimate:

1. Targets a **stated estimand** (perturbation, boundary, horizon, units).
2. Passes **observable fit** checks and **marginal-response** checks separately.
3. Is **stable** under pre-specified sensitivities and a second method on the same estimand (where feasible).
4. Only then is compared to CM for **policy implication** — whether the gap is large, robust, and relevant to crediting assessment.

Preferring MEF “instead of CM” remains a **governance** outcome, not an automatic scientific result. Evidence may support: report both; use MEF for impact assessment; reconsider CM weights; or leave CM unchanged for accounting compliance.

---

## 3. Required claim definition (before fitting)

Document in writing before any pilot run:

1. **Perturbation** — e.g. incremental system demand vs incremental geothermal injection (not assumed interchangeable without justification).
2. **Response** — change in operational CO₂ (or constructed emissions) for the interconnected Jamali boundary.
3. **Horizon** — short-run (fixed fleet) vs finite project/no-project period vs long-run capacity response (separate gates).
4. **Units** — e.g. tCO₂ per MWh of the stated perturbation.
5. **Comparison claim** — what would count as informing CM assessment (e.g. robust MEF–CM gap of stated magnitude under stated assumptions), without presupposing replacement.

---

## 4. Three separate check layers

### A. Observable fit (necessary, not sufficient)

- Chronological holdout; training-only preprocessing.
- Reproduction of generation/emissions levels or changes at the estimation frequency.
- Transparent emissions construction (heat rates, fuel factors, gross/net, missing intervals).
- Failures here block any MEF–CM comparison.

### B. Marginal-response credibility

- Stability of the estimated response across seasons, hours-of-day, and structural regimes where data allow.
- Sensitivities: emissions factors, fleet mapping/aliases, import/export treatment, demand vs fossil-generation specification.
- Identification limits stated explicitly; a regression slope or model derivative is not automatically a causal geothermal impact.
- Do not treat feature importance, shuffled-split accuracy, or prediction of CM/AEF as validation of a MEF.

### C. Policy comparison to CM (only after A and B)

- Place the MEF beside the published ESDM (or programme-specific) CM for the same conceptual use case, with versions and vintages labelled.
- Report the gap with uncertainty; ask whether it is large and robust under the pre-specified sensitivities.
- Map implications to options: *inform assessment*, *report both*, *research governance / data access*, or *proposed rule discussion* — never silent relabelling of CM as an observed MEF.

---

## 5. Triangulation rule (short-run)

Minimum standard for a short-run Jamali claim that may inform CM assessment:

| Step | Requirement |
|---|---|
| Primary | Transparent historical-regression pilot (M1-type) on time-aligned interval data |
| Cross-check | Second method on the **same estimand** where inputs allow (e.g. reduced-order dispatch), or a documented reason why triangulation is not yet possible |
| Uncertainty | Interval or sensitivity band, not a single point presented as exact |
| Labelling | “Estimated short-run MEF under stated assumptions” — not “the official factor” |

Long-run capacity-expansion results use a **separate** protocol gate (project/no-project, permitted capacity responses, unobserved future). Historical operating fit does not validate an unobserved counterfactual.

---

## 6. Decision rule (copy-ready)

**Pass (may inform CM assessment):** estimand defined; interval data and emissions construction documented; chronological validation; marginal response stable under pre-specified sensitivities; MEF–CM gap reported with uncertainty; carbon-credit implications stated as assessment input only.

**Hold (do not prefer MEF over CM):** any of the above fails; only annual or synthetic data; only predictive fit without response checks; only one fragile specification; gap disappears under reasonable sensitivities.

**Out of scope for this readiness stage:** issuing credits; declaring CM legally invalid; fitting ML as a substitute for identification; using foreign MEFs as Indonesian factors.

---

## 7. What completes this research stage vs Phase 2

**This stage is complete when** the report includes: methods and data readiness; the binding interval-data gap; this credibility protocol; carbon credits as motivation with the boundary sentence above; and CM retained as the labelled accounting benchmark until a future estimate passes the protocol.

**Phase 2 (new study) starts only if** compatible UIP2B (or equivalent) interval data are obtained: run M1 → apply §§3–6 → then discuss implications for CM and crediting assessment.
