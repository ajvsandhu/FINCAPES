# Next step: Jamali generator inventory and boundary mapping

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
