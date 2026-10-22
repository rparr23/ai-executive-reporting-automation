import copy
import csv
import sqlite3
import unittest
from pathlib import Path
from src.app import metrics, narrative, queue_report, render

ROOT = Path(__file__).resolve().parents[1]


class ReportingTests(unittest.TestCase):
    def setUp(self):
        with (ROOT/'sample-data/transactions.csv').open(newline='') as file:
            self.rows = list(csv.DictReader(file))
        self.db = sqlite3.connect(':memory:')

    def tearDown(self):
        self.db.close()

    def test_known_totals_reconcile(self):
        actual = metrics(self.rows, '2026-10')
        self.assertEqual(actual, {'period':'2026-10','transactions':4,'revenue':'4000.00','cost':'400.00','average_order_value':'1000.00','resolved':3,'average_resolution_hours':'3.00','cost_per_transaction':'100.00','automation_success_rate':'75.00'})

    def test_missing_period_blocks(self):
        with self.assertRaises(ValueError):
            metrics(self.rows, '2027-01')

    def test_duplicate_transactions_block(self):
        with self.assertRaises(ValueError):
            metrics(self.rows+[self.rows[0]], '2026-10')

    def test_invalid_source_values_block(self):
        for key,value in [('revenue','NaN'),('cost','-1'),('resolved','yes'),('date','bad'),('resolution_hours','-2')]:
            rows = copy.deepcopy(self.rows)
            rows[0][key] = value
            with self.assertRaises(ValueError):
                metrics(rows, '2026-10')

    def test_no_resolved_records_returns_null(self):
        rows = copy.deepcopy(self.rows)
        for row in rows:
            row['resolved'] = '0'
        self.assertIsNone(metrics(rows, '2026-10')['average_resolution_hours'])

    def test_narrative_uses_calculated_data(self):
        kpis = metrics(self.rows, '2026-10')
        self.assertIn('4000.00 USD', narrative(kpis))
        self.assertIn('75.00%', narrative(kpis))

    def test_approval_and_allowlist_and_duplicate_queue(self):
        kpis = metrics(self.rows, '2026-10')
        with self.assertRaises(ValueError):
            queue_report(self.db, kpis, ['a'], ['a'])
        with self.assertRaises(ValueError):
            queue_report(self.db, kpis, ['b'], ['a'], True)
        self.assertFalse(queue_report(self.db, kpis, ['a'], ['a'], True)['duplicate'])
        self.assertTrue(queue_report(self.db, kpis, ['a'], ['a'], True)['duplicate'])

    def test_html_escapes_source_text(self):
        kpis = metrics(self.rows, '2026-10')
        kpis['extra'] = '<script>alert(1)</script>'
        self.assertNotIn('<script>', render(kpis))


if __name__ == '__main__':
    unittest.main()
