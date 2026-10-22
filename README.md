# AI Business Reporting and Executive Dashboard

Independent portfolio project by Richard Parr • Future of Work Training Institute

Leaders manually consolidate operational data and produce weekly narratives with inconsistent KPI definitions.

**Current status:** tested Python reference application with synthetic data. Microsoft cloud deployment is pending. This repository does not establish business adoption or tenant deployment.

## Run the working reference

Python 3.11+; no paid service, API key or third-party Python package required for runtime or tests.

```bash
python3 -m unittest discover -s tests -v
python3 src/app.py --period 2026-10 --html report.html
python3 src/app.py --period 2026-10 --approve --recipient reviewer@example.invalid
```

Run from this repository root. SQLite state is local and excluded from Git. Use a fresh `--db` path for repeat demonstrations. The CLI will return a nonzero exit code for invalid operations.

## Microsoft target

Power BI, Power Automate, SharePoint, Azure OpenAI, Outlook

See [the PRD](docs/PRD.md), [architecture](docs/architecture.md), [deployment guide](docs/deployment-guide.md), [data contract](docs/data-contract.md), [test results](tests/results.txt), [recorded CLI run](demo/output.txt), and [evidence status](docs/evidence-status.md).

## Included behavior and limits

1. Read synthetic transactions and calculate reconciled monthly KPIs using precise decimal arithmetic.
2. Provide an accessible local HTML report plus Power BI DAX and Power Query source artifacts.
3. Produce a data-only narrative; cloud AI narrative must be separately reviewed against calculated values.
4. Require reviewer approval and allowlisted recipients before report queuing or distribution.

- HTML is a local report, not a published Power BI dashboard or PBIX file.
- Default narrative is deterministic and cannot measure AI quality. Azure-generated executive prose remains a tenant implementation step.
- No refresh schedule, email send or live source connection is active. No business ROI has been measured.

Power Automate artifacts in `flows/` are explicit build specifications, not tenant-generated solution exports. Production permission and connector tests remain outstanding. The reference's CLI approval flags simulate a reviewer; cloud deployment must verify reviewer identity server-side.

## Validation and business value

Eight automated reference tests cover positive and failure paths. Tests are regression evidence for the included synthetic cases, not an enterprise performance benchmark. See [measurement plan](docs/measurement-plan.md) before making any ROI claim.

## Sources

Implementation references checked October 22, 2026; confirm tenant-specific licensing, connector availability and capacity before deployment.

- [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries)
- [Refresh semantic model](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset)
- [Structured output](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)

MIT licensed. All sample records are synthetic.
