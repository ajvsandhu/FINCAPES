# Completed commissioning-delay sensitivity

## Purpose and settings

This experiment isolates the effect of timing on the same GENESIS planned
projects used by the original fixed-factor model. It does not select a best
emission factor or estimate the probability of an actual delay.

- Cases: current planned schedule, additional one-year delay, additional two-year delay.
- First full generation year = original commissioning year + additional delay + 1.
- Fixed annual capacity factor: 80%; fixed modelling hours: 8,760 per year.
- Fixed observation window: 2025–2034; no electricity before the first full generation year.
- Same 2,503 MW Jamali and 2,007 MW main-grid Sumatera cohorts; isolated Sabang excluded.
- Same five published factor specifications and accounting boundaries as the base model.
- No RUPTL growth bound or coal/gas replacement assumptions in this experiment.
- Cohorts remain in the inventory even when shifted beyond 2034; this is not cancellation.

The script imports `planned_capacity()`, `factor_methods()` and constants from
the base model. It filters original project membership once through that
existing cohort function, then shifts dates without filtering shifted cohorts.
Original scripts and output files are not overwritten.

## Cumulative electricity, 2025–2034

| Grid | Additional delay | Electricity (TWh) | Reduction (TWh) | Reduction (%) | First full generation after 2034 (MW) |
|---|---:|---:|---:|---:|---:|
| Jamali | 0 years | 49.588608 | 0.000000 | 0.0000 | 0 |
| Jamali | 1 year | 32.047584 | 17.541024 | 35.3731 | 1,040 |
| Jamali | 2 years | 21.794880 | 27.793728 | 56.0486 | 1,418 |
| Sumatera | 0 years | 47.465184 | 0.000000 | 0.0000 | 0 |
| Sumatera | 1 year | 33.400128 | 14.065056 | 29.6324 | 505 |
| Sumatera | 2 years | 22.874112 | 24.591072 | 51.8087 | 505 |

Percentages compare each delayed case with the current schedule for the same
grid. Late additions make these finite-window results particularly sensitive:
Jamali's 1,040 MW commissioned in 2033 first generates in 2034, 2035 or 2036
under the three cases. Another 378 MW commissioned in 2032 starts in 2035 under
the two-year delay. Sumatera's 505 MW commissioned in 2033 starts after the
window under both delay cases. Earlier cohorts also lose in-window generation
years even if they begin operating before 2035.

## Gross avoided grid emissions, 2025–2034

| Grid | Factor method | Current schedule (MtCO₂) | Additional 1 year (MtCO₂) | Additional 2 years (MtCO₂) |
|---|---|---:|---:|---:|
| Jamali | OM | 39.67 | 25.64 | 17.44 |
| Jamali | BM | 46.61 | 30.12 | 20.49 |
| Jamali | CM ex-post 50/50 | 43.14 | 27.88 | 18.96 |
| Jamali | CM ex-ante 50/50 | 43.14 | 27.88 | 18.96 |
| Jamali | JCM alternative | 30.70 | 19.84 | 13.49 |
| Sumatera | OM | 36.55 | 25.72 | 17.61 |
| Sumatera | BM | 53.16 | 37.41 | 25.62 |
| Sumatera | CM ex-post 50/50 | 44.62 | 31.40 | 21.50 |
| Sumatera | CM ex-ante 50/50 | 44.14 | 31.06 | 21.27 |
| Sumatera | JCM alternative | 21.74 | 15.30 | 10.48 |

Since factors remain fixed, percentage emissions reductions are identical to
percentage electricity reductions within each grid. Absolute reductions depend
on the chosen factor. Both are provided at full calculation precision in the
summary CSV. Calculate differences before rounding, not from these displayed
two-decimal values. BM remains highest and the JCM alternative lowest; this is
not an accuracy or eligibility ranking. ESDM/JCM source-vintage differences and
the ex-ante factor's stated coverage limitation remain unchanged.

These specified timing cases have larger effects than the 12.5% change produced
by moving the original 80% capacity factor to 70% or 90%. That is a comparison
of chosen assumption ranges, not of probabilities or estimated uncertainty.
The results quantify generation and associated gross grid emissions outside
the study window, not permanent lifetime losses, net emissions or issued credits.
No prediction of actual commissioning dates or improved emissions accuracy is made.

## Reproduction and output dictionary

From the repository root:

```sh
python3 -B geothermal_credit_model/commissioning_delay_sensitivity.py
```

Requires Python with pandas, NumPy and Matplotlib. Versions used are recorded
in `output/commissioning_delay/run_manifest.json`. The script runs validation
before writing results and returns a nonzero exit if a check fails.

All new results live in `output/commissioning_delay/`:

| File | Contents |
|---|---|
| `commissioning_delay_cohorts.csv` | All 54 original grid/year/delay records, including zero-capacity cohorts, shifted commissioning and generation dates, full operating years within the window, and capacity retained after the window |
| `commissioning_delay_generation_by_year.csv` | 60 unique grid/delay/year rows: operating MW, annual MWh and cumulative MWh; use this for generation totals without repeating factor methods |
| `commissioning_delay_by_year.csv` | 300 grid/delay/year/factor rows with annual and cumulative emissions, reference quantities and reductions |
| `commissioning_delay_summary.csv` | 30 grid/delay/factor totals, absolute and percentage reductions, 2034 operating capacity and capacity starting after 2034 |
| `emission_factor_methods.csv` | Exact applied factors and source labels, including JCM factors inherited from the base model |
| `commissioning_delay_annual_generation.png` | Annual generation paths; two panels use the same vertical scale |
| `commissioning_delay_factor_comparison.png` | Cumulative gross emissions for all five methods and three timing cases |
| `validation_checks.json` | 93 passing implementation checks |
| `run_manifest.json` / `input_snapshots/` | Settings, package versions, source paths, SHA-256 hashes and exact source copies |

Annual `estimated_generation_mwh` and `gross_avoided_emissions_tco2` are annual
quantities; their summary counterparts are 2025–2034 totals. Cumulative columns
in the annual table run from 2025 through `analysis_year`. The prefix
`current_schedule_` identifies the matching zero-additional-delay reference;
`reduction_` is reference minus scenario; `reduction_pct_` is 100 times that
reduction divided by reference. Percentages are blank where the annual or
cumulative reference is zero (including 2025), rather than reporting an
undefined 0/0 as 0%. Cumulative quantities should not be summed across years.
Generation repeats across the five factor methods in emissions tables and
must not be summed across methods.

Snapshots preserve the mapped capacity table, ESDM factor table, base script
(which contains JCM values), and original annual and summary outputs used for
reconciliation. They are copies of existing repository artifacts, not newly
downloaded data. Reproduction uses the original repository paths; to reconstruct
this exact run after future input changes, restore the recorded snapshot bytes
at their manifest source paths in a separate working copy before running.

## Completed validation

- Zero delay exactly equals the original in-memory central model on all shared fields.
- Saved original annual and summary electricity/emissions match within an absolute tolerance of 0.0000001 MWh/tCO₂, allowing only floating-point/CSV round-trip effects.
- Original membership and grid totals are retained under every delay; no duplicate cohort or output keys occur.
- All 60 annual generation rows are checked directly against original cohort timing.
- Independent cohort-year sums reconcile cumulative electricity; post-window cohorts contribute zero in-window electricity.
- Annual and cumulative generation are nonnegative and never increase when the uniform additional delay grows; cumulative generation does not fall as time advances.
- Generation is identical across factor methods; factors remain fixed and emissions equal electricity times factor.
- Annual sums reconcile cumulative totals; absolute/percentage reductions use the current schedule of the same grid/factor.
- Separately from the script's 93 checks, all 300 annual emissions rows and all 30 summary rows were recalculated from CSV inputs using standard-library Decimal arithmetic, within the same absolute tolerance.
- A second complete run reproduced all 14 output/snapshot files byte-for-byte, including both PNGs; both charts were visually inspected for legibility.

These checks establish arithmetic consistency and reproducibility, not agreement
with unobserved future project generation or displaced grid emissions.
