# Power BI semantic model and report recipe

1. Create a `CsvPath` text parameter in Power Query and import src/transactions.pq as `Transactions`. For service deployment replace File.Contents with an approved SharePoint connector, or configure an approved gateway. A desktop local path does not refresh by itself in the service.
2. Reject duplicate/blank transaction IDs and invalid types before refresh. Do not silently remove duplicate facts. All money is USD; multi-currency needs an approved conversion model.
3. Create Dates = CALENDAR(DATE(2026,1,1), DATE(2027,12,31)), mark as date table, and relate Dates[Date] 1:* Transactions[date] with single-direction filtering.
4. Create each measure from src/measures.dax individually. Format currency to 2 decimals, duration to hours, and success/growth as percentages. Python success rate is percentage points (75.00); the DAX measure is a fraction (0.75) formatted as percent.
5. Revenue page: period slicer, revenue/AOV cards and monthly revenue line. Service page: resolved count and mean resolution hours. Operations page: cost per transaction and automation success. Add a reconciliation table and last refresh timestamp.
6. October control totals: 4 transactions, revenue 4000.00, cost 400.00, AOV 1000.00, 3 resolved, mean resolution 3 hours, cost/transaction 100.00 and success 75%. September revenue is 800.00; October month-over-month growth is 400%, a small synthetic example rather than a real business trend.
7. The synthetic grain combines one sales/service transaction per row. For real businesses separate SalesFact, TicketsFact and AutomationRunsFact; their denominators differ. Do not label transaction counts as orders or support tickets without the data owner's agreement.
8. Publish to a test workspace after verifying sharing entitlements. Enable refresh using approved credentials. Query measures only after confirmed refresh success and explicit period filtering. Test row-level security with a viewer identity; workspace admins are not an adequate RLS test.

No PBIX/PBIP export or published workspace exists in this repository. Source M and DAX are provided for construction and reconciliation.
