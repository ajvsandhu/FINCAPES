# Claim–evidence ledger for the revised literature section

Verified 10 November 2026. These locators support [CRITICAL_LITERATURE_REVIEW.md](CRITICAL_LITERATURE_REVIEW.md). “Documented” means found in the identified source, not independently reproduced or causally validated. PDF pages below are one-based; notebook cells are zero-based. New files and retrieval limits are in [deeper_review_manifest.json](deeper_review_manifest.json).

| ID | Documented claim | Exact evidence | Evidence boundary |
|---|---|---|---|
| E01 | Siler-Evans's chapter identifies itself as based on the 2012 joint paper | `raw/siler_evans_thesis_2012.pdf`, PDF p.15 / printed p.5, footnote 1 | Author's dissertation chapter, not a retrieved copy of the journal version |
| E02 | Hourly generator emissions and gross output; regional matching | Same PDF pp.18–19 / printed pp.8–9, §2.3 | Coverage is the source's CEMS sample, not every generator |
| E03 | Regression of adjacent-hour emissions changes on fossil-generation changes; subgroup regressions | Same PDF pp.19–21 / printed pp.9–11, §§2.4.1–2.4.2 | Fossil generation is a proxy, not measured total system demand |
| E04 | Imports/exports ignored; omitted-generator and hydro/curtailment caveats | Same PDF pp.19–21, 36–38 / printed pp.9–11, 26–28 | Source acknowledges limits; they are not assumptions established for Jamali |
| E05 | Operator fuel comparison uses non-identical metrics | Same PDF pp.39–40 / printed pp.29–30, §2.8.3, Figure 2.6 | Corroboration, not a directly observed causal MEF or future holdout |
| E06 | Variable costs and minimum-downtime approximation | `raw/deetjen_supporting_information.pdf`, PDF pp.2–4 / printed pp.S1–S3 | Specific model settings, not universal operating requirements |
| E07 | Regional trade is discussed and approximated | Same PDF pp.5–6 / printed pp.S4–S5 | Discussion is not validation of a dynamic exchange response |
| E08 | Benchmark ordering depends on endpoint; simulated-price limitations | Same PDF pp.6–9 / printed pp.S5–S8, Figures S4–S5 | Particular comparison; do not infer a universal model ranking |
| E09 | Reduced-order code defines `demand` from fossil generation | `raw/simple_dispatch_simple_dispatch.py`, `calcDemandData`, `demandTimeSeries`, pinned revision in original manifest | Implementation evidence, not total-customer-load measurement |
| E10 | Dynamic-dispatch historical experiment lacks transmission data and compares implied with observed hourly emissions changes | `raw/dynamic_lme.pdf`, PDF pp.5–6 / printed pp.1142–1143, §IV-A and Figure 2 | Historical operating check, not directly observed intervention response |
| E11 | Separate network simulation uses 240-bus system | Same PDF p.6 / printed p.1143, §IV-B | Simulation network, not empirical validation of every locational effect |
| E12 | Locational response is obtained through dispatch sensitivity | Same PDF pp.2–5 / printed pp.1139–1142, §§II–III | Optimisation-model derivative, not supervised learning of true MEF labels |
| E13 | ML features, coefficient-based emissions-change objective and target | `raw/MEF-Regression_MLP_MEFs.ipynb`, cells 11 and 17, especially `feature_cols` and both `mse_loss_regularized_preds_*` functions | Shared notebook; no execution or entire-paper replication |
| E14 | Shuffled split; training-only scaler fitting | Same notebook cell 11: `np.random.shuffle(set_assignments)`, `scaler.fit(train_x)` | Does not establish a chronological future-period test |
| E15 | Evaluation reconstructs emissions changes from coefficients | Same notebook cell 21: `get_r_squared`, `mean_absolute_error` | Observable response fit is not direct causal-MEF error |
| E16 | AVERT bins fossil generation and collects operating/emissions distributions | `raw/avert_v43.pdf`, PDF pp.76–77 / printed pp.70–71, Appendix D | Historical statistical construction, not one universally marginal unit |
| E17 | No explicit ramp/cycling response; expected rather than exact trajectories; constant interregional trade | Same PDF pp.141–142 / printed pp.135–136, Appendix L | Explicit source limitations; not necessarily appropriate for Jamali |
| E18 | AVERT distinguishes operational short-run scope from structural long-run effects | Same PDF p.14 / printed p.8 | Does not establish endogenous long-run capacity response |

## FINCAPES interpretation, not results from the foreign studies

| ID | Proposed conclusion | Supporting evidence | What remains to be demonstrated |
|---|---|---|---|
| P01 | Define total-demand versus fossil-generation response explicitly | E02–E04, E09, E13 | Appropriate perturbation, controls and boundary for actual Jamali records |
| P02 | Do not assume grid-average or published CM values are true MEF labels | E03, E12–E15 | A credible emissions target and identification strategy |
| P03 | Evaluate operational prediction and marginal-response interpretation separately | E05, E08, E10, E15 | Suitable local validation and sensitivity checks |
| P04 | Examine hydro, trade, curtailment and operating constraints before adapting methods | E04, E06–E07, E10–E11, E17 | Their actual role in the selected Jamali period |
| P05 | Assess a transparent baseline before a flexible ML extension | E03, E06, E13–E15 | Feasibility and relative performance on local evidence; no winner has been established |

## Evidence upgrades and unresolved access

- M1 moved from abstract-only methodological coverage to an inspected corresponding thesis chapter. Cite Siler-Evans's dissertation for the detailed chapter findings; do not silently attribute the retrieved version to the journal text.
- M2 now includes the full official supporting information. The main article remains unverified in full. Do not infer uninspected main-paper methods or the causal status of its benchmark from a supplementary figure alone.
- M4 remains a code-level methodological review supported by publisher summary. The main paper's full predictor availability, trade treatment and forecasting protocol have not been verified. No numerical claim of its superiority is adopted.
- M3 and M5 remain full-document sources with focused methodological checks, not independent reproductions of their models.
