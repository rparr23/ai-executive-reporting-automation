"""Reconciled KPI reference with a local review/distribution outbox."""
import argparse
import csv
import hashlib
import html
import json
import sqlite3
from datetime import date
from decimal import Decimal, InvalidOperation
from pathlib import Path


def metrics(rows, period):
    date.fromisoformat(period + '-01')
    seen, selected = set(), []
    for row in rows:
        if not row['transaction_id'] or row['transaction_id'] in seen:
            raise ValueError('Missing or duplicate transaction ID')
        seen.add(row['transaction_id'])
        day = date.fromisoformat(row['date'])
        try:
            revenue, cost = Decimal(row['revenue']), Decimal(row['cost'])
            if not all(v.is_finite() and v >= 0 and v.as_tuple().exponent >= -2 for v in [revenue, cost]):
                raise ValueError('Invalid money')
        except InvalidOperation as exc:
            raise ValueError('Invalid money') from exc
        if row['resolved'] not in {'0', '1'} or row['automation_success'] not in {'0', '1'}:
            raise ValueError('Flags must be 0 or 1')
        try:
            hours = Decimal(row['resolution_hours']) if row['resolution_hours'] else None
        except InvalidOperation as exc:
            raise ValueError('Invalid resolution hours') from exc
        if hours is not None and (not hours.is_finite() or hours < 0):
            raise ValueError('Invalid resolution hours')
        if row['resolved'] == '1' and hours is None:
            raise ValueError('Resolved transaction missing resolution hours')
        if day.strftime('%Y-%m') == period:
            selected.append((row, revenue, cost, hours))
    if not selected:
        raise ValueError('No data for requested period; distribution blocked')
    revenue = sum((r[1] for r in selected), Decimal(0))
    cost = sum((r[2] for r in selected), Decimal(0))
    resolved = [r for r in selected if r[0]['resolved'] == '1']
    return {'period': period, 'transactions': len(selected), 'revenue': str(revenue.quantize(Decimal('.01'))), 'cost': str(cost.quantize(Decimal('.01'))), 'average_order_value': str((revenue / len(selected)).quantize(Decimal('.01'))), 'resolved': len(resolved), 'average_resolution_hours': str((sum((r[3] for r in resolved), Decimal(0)) / len(resolved)).quantize(Decimal('.01'))) if resolved else None, 'cost_per_transaction': str((cost / len(selected)).quantize(Decimal('.01'))), 'automation_success_rate': str((Decimal(sum(int(r[0]['automation_success']) for r in selected)) * 100 / len(selected)).quantize(Decimal('.01')))}


def narrative(kpis):
    return f"{kpis['period']}: revenue {kpis['revenue']} USD across {kpis['transactions']} transactions. Average order value {kpis['average_order_value']} USD. Resolved {kpis['resolved']} service transactions. Automation success {kpis['automation_success_rate']}%."


def render(kpis):
    table = ''.join(f'<tr><th scope="row">{html.escape(key)}</th><td>{html.escape(str(value))}</td></tr>' for key, value in kpis.items())
    return '<!doctype html><html lang="en"><meta charset="utf-8"><meta name="viewport" content="width=device-width"><title>FOWTI Executive Report</title><style>body{font:18px system-ui;max-width:900px;margin:3rem auto;padding:1rem;color:#162238;background:#f4f7fa}table{width:100%;border-collapse:collapse;background:white}th,td{text-align:left;padding:1rem;border-bottom:1px solid #ccc}p{line-height:1.6}</style><main><h1>Executive Performance Report</h1><p>Synthetic portfolio data • Local reference • Pending human review</p><p>' + html.escape(narrative(kpis)) + '</p><table><caption>Monthly reconciled KPIs in USD</caption><thead><tr><th>Metric</th><th>Value</th></tr></thead><tbody>' + table + '</tbody></table></main></html>'


def queue_report(db, kpis, recipients, allowed, approved=False):
    if not approved:
        raise ValueError('Reviewer approval required')
    if not recipients or not set(recipients).issubset(set(allowed)):
        raise ValueError('Recipient is not allowlisted')
    db.execute('CREATE TABLE IF NOT EXISTS outbox (id TEXT PRIMARY KEY, payload TEXT NOT NULL)')
    payload = json.dumps({'kpis': kpis, 'narrative': narrative(kpis), 'recipients': sorted(set(recipients))}, sort_keys=True)
    key = hashlib.sha256(payload.encode()).hexdigest()
    with db:
        cur = db.execute('INSERT OR IGNORE INTO outbox VALUES (?,?)', (key, payload))
    return {'report_id': key, 'duplicate': cur.rowcount == 0, 'delivery': 'local_outbox_only'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data', default='sample-data/transactions.csv')
    parser.add_argument('--period', default='2026-10')
    parser.add_argument('--html', default='report.html')
    parser.add_argument('--db', default='state.db')
    parser.add_argument('--approve', action='store_true')
    parser.add_argument('--recipient', action='append', default=[])
    parser.add_argument('--allowlist', default='sample-data/recipients.json')
    args = parser.parse_args()
    try:
        with open(args.data, newline='') as file:
            kpis = metrics(list(csv.DictReader(file)), args.period)
        Path(args.html).write_text(render(kpis))
        result = {'kpis': kpis, 'narrative': narrative(kpis), 'html': args.html}
        if args.approve or args.recipient:
            with sqlite3.connect(args.db) as db:
                result['queue'] = queue_report(db, kpis, args.recipient, json.loads(Path(args.allowlist).read_text()), args.approve)
        print(json.dumps(result, indent=2))
    except (ValueError, KeyError, OSError, sqlite3.Error) as exc:
        parser.exit(2, f'Operation failed: {exc}\n')


if __name__ == '__main__':
    main()
