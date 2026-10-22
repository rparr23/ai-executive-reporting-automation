# Product requirements: AI Business Reporting and Executive Dashboard

Version 1.0 • October 22, 2026 • Product owner: Richard Parr

## Problem and users

Leaders manually consolidate operational data and produce weekly narratives with inconsistent KPI definitions.

Users: Business analysts, operations managers, executive reviewers, approved report recipients.

## Outcome and success definition

Deliver a reviewable automation with source traceability, deterministic validation, explicit approvals and replay protection. The local reference must pass its supplied positive and negative tests. Cloud completion requires the same scenarios executed in the Microsoft environment, an authorized pilot and an exported solution or report evidence.

No adoption, hours saved, accuracy percentage or financial return is claimed by this PRD. Any target below is a proposed pilot criterion rather than a measured result.

## MVP scope

1. Read synthetic transactions and calculate reconciled monthly KPIs using precise decimal arithmetic.
2. Provide an accessible local HTML report plus Power BI DAX and Power Query source artifacts.
3. Produce a data-only narrative; cloud AI narrative must be separately reviewed against calculated values.
4. Require reviewer approval and allowlisted recipients before report queuing or distribution.

## Explicit exclusions and reference limits

- HTML is a local report, not a published Power BI dashboard or PBIX file.
- Default narrative is deterministic and cannot measure AI quality. Azure-generated executive prose remains a tenant implementation step.
- No refresh schedule, email send or live source connection is active. No business ROI has been measured.
- No production rollout, financial transactions or unsolicited external messages.
- No real employee, meeting or financial records in the public repository.
- No guarantee that local approval or identity simulation enforces tenant security.

## Functional requirements and traceability

| ID | Required behavior | Local test evidence |
|---|---|---|
| RPT-01 | October KPIs reconcile to 4000 USD revenue, 400 USD cost and 4 transactions. | test_known_totals_reconcile |
| RPT-02 | Missing periods, duplicate transactions or malformed source values block reporting. | test_missing_period_blocks; test_duplicate_transactions_block; test_invalid_source_values_block |
| RPT-03 | Resolution average is null when there are no resolved transactions. | test_no_resolved_records_returns_null |
| RPT-04 | Narrative uses supplied calculated KPI values; HTML escapes data. | test_narrative_uses_calculated_data; test_html_escapes_source_text |
| RPT-05 | Unapproved or unauthorized distribution is blocked and retries do not duplicate local outbox records. | test_approval_and_allowlist_and_duplicate_queue |

Cloud acceptance must separately validate connector semantics, end-user permissions, approver identity, retries and delivery reconciliation. Local test names do not imply those cloud tests were performed.

## User journey

1. An authorized user or scheduled trigger submits a source reference and unique version key.
2. The workflow validates inputs and reserves the processing key before expensive work.
3. The automation retrieves permitted source data and produces the proposed response or structured result.
4. Validation checks required fields, provenance and business rules. Uncertainty goes to review.
5. A verified reviewer approves the exact version before any external action.
6. The workflow persists action references, audit status and a user-visible outcome.
7. Retries use the existing version ledger; changed content requires a new version.

## Data model

### Transactions

| Field | Definition |
|---|---|
| transaction_id | Text; unique; one row per combined synthetic sale/service transaction |
| date | Date; reporting date |
| revenue | Decimal USD; nonnegative |
| cost | Decimal USD; nonnegative |
| resolved | 0 or 1 |
| resolution_hours | Decimal; required for resolved rows |
| automation_success | 0 or 1 |

### ReportRuns

| Field | Definition |
|---|---|
| ReportVersionKey | Text; period + data checksum + recipient-set hash |
| RefreshId | Text |
| CalculatedKPIJSON | Multiline JSON |
| Narrative | Multiline text |
| State | PendingReview, Approved, Delivered, Failed |
| ReviewerObjectId | Text |
| DeliveryReference | Text |

## State and failure model

Use Pending/Received, Validated, PendingReview, Approved, Completed, Rejected and Failed as the conceptual lifecycle; project-specific state names are defined in the data contract. Keep processing status distinct from remote delivery status. Retry network failures only when replay is safe. Do not retry validation errors. A timeout after a remote write may have succeeded: enter reconciliation instead of blindly creating another remote record.

Corrected inputs receive a new version key, linked to the original for audit. Never mutate an approved payload silently. Local SQLite transactions guard local state; they cannot make external Microsoft API writes atomic.

## Nonfunctional requirements

- Identity: Entra authentication; resolve roles from trusted identity claims and enforce source authorization in the data layer.
- Secrets: managed connection references or approved secret store; no tokens in Git, logs or prompts.
- Data protection: synthetic data in demos; production retention, geographic location and DLP approved by tenant owner.
- Reliability: unique keys, transaction-backed reservations, bounded retry and a manual recovery queue.
- Observability: correlation ID, source/version reference, attempt, stage, result and timestamps; exclude raw sensitive text.
- Accessibility: readable text, table headings, visible status and no color-only meaning in the eventual tenant UI.
- Performance pilot target: measure median and p95 end-to-end latency on at least 20 representative sources. Set budget only after baseline collection.
- Availability: no production SLA for this portfolio reference; tenant SLA and ownership require a separate operational agreement.

## Build sequence and deliverables

| Stage | Milestone | Work and exit condition |
|---|---|---|
| 1 | Data and KPI contract | Define transaction grain, currency and reporting window; publish synthetic facts and reconciliation totals. |
| 2 | Power BI model | Load with Power Query, create date relationship and DAX measures; build revenue, service and operations pages. |
| 3 | Narrative workflow | Refresh, wait for success, query exact measures and generate constrained narrative with explicit period. |
| 4 | Review and distribution | Review calculations and narrative, restrict recipients, record delivery keys and test refresh/missing-data failures. |

Sequence across portfolio: support agent, meeting automation, document processing, executive reporting. Each project has its own commit history, tests and deployment gate.

## Dependencies and licensing gate

Target stack: Power BI, Power Automate, SharePoint, Azure OpenAI, Outlook. A tenant owner must verify environment roles, SharePoint permissions, premium connector availability, Copilot/AI Builder capacity, Azure deployment quota and Power BI sharing rights as applicable. This repository does not provision resources or incur cloud charges. Do not hard-code trial eligibility or prices.

## Pilot acceptance

- All local automated tests pass with evidence recorded.
- All requirement rows pass in a configured tenant using synthetic data.
- Two differently authorized test users demonstrate expected access boundaries.
- Duplicate, rejection, missing-data and downstream-failure scenarios produce correct audit states.
- Sanitized Microsoft solution export/report artifact, real screenshots and a 2-4 minute demonstration are attached.
- A business owner signs off the source-of-truth data, KPI meanings and reviewer routing.

## Risks and mitigations

| Risk | Mitigation | Owner |
|---|---|---|
| Model produces unsupported facts | Source evidence, schema checks and human review | AI solution owner |
| Connector runs with broader access than user | Least privilege, caller authorization and dual-user tests | Tenant admin |
| Retry duplicates a remote write | Unique ledger plus post-timeout reconciliation | Workflow owner |
| Source content changes after approval | Versioned keys and exact approved payload hash | Data owner |
| Trial or licensing gaps prevent demo | Validate capacity and permissions before provisioning | Tenant admin |
| Prototype mistaken for deployment | Evidence status in README and release checklist | Portfolio owner |

## Measurement and resume evidence

Measure baseline manual effort, automated processing effort, reviewer time, success rate, review rate, error rate and actual cost over a documented sample. Preserve numerator, denominator, sample selection and environment. Describe local reference and cloud pilot separately. Do not claim production deployment or percentage savings until verified.

## Release definition

Local reference release: code, fixtures, tests, executed walkthrough, PRD and implementation plan committed. Microsoft pilot release: tenant prerequisites configured, native artifacts exported, acceptance evidence recorded and approved test group onboarded. Production release: separate security, support, cost and retention approval.

## Authoritative implementation references

- [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries)
- [Refresh semantic model](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset)
- [Structured output](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
