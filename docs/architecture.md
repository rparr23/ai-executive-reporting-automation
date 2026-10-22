# Architecture

## Microsoft target

```mermaid
flowchart TD
Source["SharePoint facts"] --> Model["Power BI semantic model"]
Model --> Dashboard["Executive dashboard"]
Model --> KPIs["Approved DAX query"]
KPIs --> Narrative["AI narrative"]
Narrative --> Review["Reviewer approval"]
Review -->|Approve| Outlook["Allowlisted Outlook delivery"]
Review -->|Reject| Recovery["Correction queue"]
```

## Local implementation

Python CLI → validated synthetic inputs → domain logic → local SQLite state or HTML report. No Microsoft connector calls occur in the default walkthrough.

The cloud flow is an implementation plan. Local tests verify the reference logic; tenant identity, permission filtering, external delivery and connector failure semantics require separate integration tests.

## Trust boundaries

External content is untrusted. Identity and allowed recipients are resolved outside the model. The model cannot grant permissions, approve its own work or decide recipients. Source permissions must be enforced before retrieval; output validation alone cannot prevent leakage.
