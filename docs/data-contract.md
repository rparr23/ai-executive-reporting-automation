# Data contract

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

The Python reference uses SQLite or CSV equivalents, not native SharePoint schema provisioning. See src/app.py for exact reference fields. All cloud identity fields must be resolved by the authenticated service, not accepted from model output. Use ISO 8601 dates and UTC audit timestamps; the reporting period uses the agreed business calendar.
