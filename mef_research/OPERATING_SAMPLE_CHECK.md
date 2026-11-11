# Jamali operating-data sample check

Completed **11 November 2026**. This is the bounded step named in [IPP_ALIAS_AUDIT.md](IPP_ALIAS_AUDIT.md): inspect one actual Jamali operating-data sample and make a compatibility decision. Hashes, URLs and screened leads are in [operating_sample_manifest.json](operating_sample_manifest.json).

## Copy-ready finding

A targeted search for openly downloadable Jamali operating data identified one candidate that claimed to provide operational and generation data for the interconnected Java–Madura–Bali system: the *Jamali Power System Dataset* v1.0.0, published on Zenodo on 9 May 2026 under CC BY 4.0 (Ikhsan, 2026). The archived release was downloaded and checksum-verified. It contains only a README, a licence notice and a software `.gitignore`; no data records are included, and the linked GitHub repository was no longer available on 11 November 2026. Its description also refers to benchmark economic-dispatch cases rather than observed time-stamped operations. The candidate is therefore **incompatible** with an MEF estimation sample.

Other leads were screened but not adopted. A public Indonesian modelling repository provides hourly Jawa–Bali demand profiles for 2030 and 2035 scenarios, which are projections rather than historical observations. Recent studies report half-hourly Jamali load obtained from PLN's Java–Bali dispatch centre, confirming that such records exist, but the files were not published with those studies. No openly accessible, time-aligned Jamali demand, generation and emissions or fuel package has been verified. Neither the short-run nor the long-run numerical MEF route is cleared.

## Schema check

| Required field | Result for O1 |
|---|---|
| Time-stamped demand (MW/MWh, interval, timezone) | Absent |
| Generation by unit or fuel, same intervals | Absent |
| Emissions or fuel quantities/factors | Absent (README mentions “emission parameters” only) |
| Exchange / boundary metadata | Absent |
| Gross/net definitions, coverage, missingness | Not assessable; zero data files |
| Access terms | CC BY 4.0 on the record; nothing usable to license |

## Screened leads not adopted

| Lead | Why not used |
|---|---|
| [Power-Lab/data-indonesia-2025](https://github.com/Power-Lab/data-indonesia-2025) | Hourly demand files are 2030/2035 scenario inputs, not observations |
| [ITPLN thesis on half-hourly Jamali load, 2023–2024](https://repository.itpln.ac.id/id/eprint/6778/) and an IEEE ICHVEPS 2025 paper on seven months of 30-minute load | Show that PLN UIP2B interval load exists; data not published; thesis restricted to registered users |
| [Electricity Maps API](https://app.electricitymaps.com/docs/reference/carbon-intensity/latest) | Country-level Indonesia zone only, model-estimated, account/commercial access; not opened |

## Stopping decision

The gate stops here with a documented incompatibility, as planned. Fleet-source hunting and open-ended data searches should not resume. The next bounded task is to **consolidate the completed evidence into a final method-dependent readiness assessment and implementation recommendations**: for each MEF route, what the existing evidence supports, which inputs are missing, and the specific data request (for example, half-hourly UIP2B Jamali load with unit or fuel-type generation for a stated overlap period) that would unlock it. Any request to PLN or ESDM is institutional contact and requires fresh authorisation.

No data were fabricated, resampled or modelled. No login, paid access, institutional contact, commit, push, branch or delegation occurred.
