# Microsoft deployment guide

**Not deployed:** these steps require access to a configured Microsoft tenant. The repository contains a local reference and implementation specification, not a ready-to-import managed solution.

## Preflight

1. Select a development Power Platform environment and a synthetic-data-only SharePoint site. Confirm ownership, maker rights and DLP policy.
2. Confirm capacity and licensing for Power BI, Power Automate, SharePoint, Azure OpenAI, Outlook. Confirm any paid action with your organization before enabling it.
3. Create a named solution, environment variables and service connection references. Restrict makers and reviewers to the test group.
4. Create the lists/tables in [data contract](data-contract.md). Enforce unique keys at the datastore, not only in flow conditions.
5. Define the approver group, recipient allowlist, retention and failure recovery owner. Use a secure connector or Key Vault for secrets.

## Build the workflow

### 1. Recurrence trigger

Set tenant-approved timezone and cadence; no schedule is activated by this repository.

### 2. Refresh semantic model

Request refresh and poll refresh history until completion; fail or time out before querying stale results.

### 3. Execute approved DAX

Query only agreed measures and explicit reporting period. Check API errors and empty/null results; attach refresh ID and data timestamp.

### 4. Reconcile KPI values

Compare row counts and totals to source checksums and control totals. Never ask an LLM to calculate money.

### 5. Generate narrative

Provide only validated KPI JSON, period, units and null semantics. Require observations and recommendations to be separate. Block invented numbers in review.

### 6. Start and wait for an approval

Reviewer compares narrative to the KPI table and approves the exact report version.

### 7. Recipient gate and delivery

Intersect requested recipients with an administrator-owned allowlist. Reserve delivery key, send through Outlook, persist reference; reconcile uncertain sends.

### 8. Audit and failure

Capture refresh ID, correlation ID, report hash and delivery status. Missing data or failed refresh => no email; alert the owner.

## Validate and release

1. Run the local suite and walkthrough for expected behavior; do not treat it as cloud validation.
2. Repeat all PRD acceptance rows in the tenant. Capture run IDs, input versions, expected/actual results and timestamps.
3. Use at least an ordinary employee/test user and a restricted reviewer/admin to test access. Verify unauthorized input fails before any write.
4. Inject invalid inputs, a duplicate submission, connector permission denial and a timeout after a write. Reconcile the remote system before retrying uncertain writes.
5. Inspect all artifacts for secrets and real data. Export the actual unmanaged solution via Power Platform tooling; bind connection references when importing into another environment.
6. Record a 2-4 minute demo from the actual Microsoft UI, including one success and one refusal/review case. Add sanitized screenshots and tenant test results.
7. Update docs/evidence-status.md only for verified capabilities. Keep prototype, pilot and production claims separate.

## Rollback

Disable triggers and distribution first. Preserve the audit ledger and remote references. Revert to the prior solution version in the dev environment; reconcile pending deliveries rather than replaying them blindly. Do not delete source records or logs as part of rollback. Remove only explicitly disposable synthetic records after the test owner agrees.

## References

- [Execute Queries](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/execute-queries)
- [Refresh semantic model](https://learn.microsoft.com/en-us/rest/api/power-bi/datasets/refresh-dataset)
- [Structured output](https://learn.microsoft.com/en-us/azure/foundry/openai/how-to/structured-outputs)
