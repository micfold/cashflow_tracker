"""
Unit tests for data ingestion functions
"""

import unittest
import pandas as pd
import os
import tempfile
from pathlib import Path
import sys

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.core.ingestion import (
    ingest_csv, ingest_excel, create_manual_transaction
)
from cashflow_tracker.core.schema import TransactionSchema


class TestIngestion(unittest.TestCase):
    """Test data ingestion functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Create temporary CSV file
        self.temp_csv = tempfile.NamedTemporaryFile(suffix='.csv', delete=False)
        self.csv_filename = self.temp_csv.name

        # Create test data
        self.test_data = pd.DataFrame({
            'Date': ['2025-04-01', '2025-04-02'],
            'Description': ['Test Income', 'Test Expense'],
            'Amount': [1000.0, 500.0],
            'Type': ['Income', 'Expense']
        })

        # Write to CSV
        self.test_data.to_csv(self.csv_filename, index=False)

        # Create temporary Excel file
        self.temp_excel = tempfile.NamedTemporaryFile(suffix='.xlsx', delete=False)
        self.excel_filename = self.temp_excel.name

        # Write to Excel
        self.test_data.to_excel(self.excel_filename, index=False)

    def tearDown(self):
        """Tear down test fixtures"""
        os.unlink(self.csv_filename)
        os.unlink(self.excel_filename)

    def test_ingest_csv(self):
        """Test CSV ingestion"""
        df = ingest_csv(self.csv_filename)

        # Check shape
        self.assertEqual(df.shape, (2, 4))

        # Check column values
        self.assertEqual(df['Date'].iloc[0], '2025-04-01')
        self.assertEqual(df['Description'].iloc[1], 'Test Expense')
        self.assertEqual(df['Amount'].iloc[0], 1000.0)
        self.assertEqual(df['Type'].iloc[1], 'Expense')

    def test_ingest_excel(self):
        """Test Excel ingestion"""
        df = ingest_excel(self.excel_filename)

        # Check shape
        self.assertEqual(df.shape, (2, 4))

        # Check column values
        self.assertEqual(df['Date'].iloc[0], '2025-04-01')
        self.assertEqual(df['Description'].iloc[1], 'Test Expense')
        self.assertEqual(df['Amount'].iloc[0], 1000.0)
        self.assertEqual(df['Type'].iloc[1], 'Expense')

    def test_create_manual_transaction(self):
        """Test manual transaction creation"""
        transaction = create_manual_transaction(
            date='2025-04-15',
            description='Test Transaction',
            amount=100.0,
            transaction_type='Expense',
            category='Food',
            subcategory='Groceries',
            producer='Test Store',
            payment_method='Credit Card',
            notes='Test notes'
        )

        # Check transaction data
        self.assertEqual(transaction[TransactionSchema.DESCRIPTION], 'Test Transaction')
        self.assertEqual(transaction[TransactionSchema.AMOUNT], 100.0)
        self.assertEqual(transaction[TransactionSchema.TYPE], 'Expense')
        self.assertEqual(transaction[TransactionSchema.CATEGORY], 'Food')
        self.assertEqual(transaction[TransactionSchema.SUBCATEGORY], 'Groceries')
        self.assertEqual(transaction[TransactionSchema.PRODUCER], 'Test Store')
        self.assertEqual(transaction[TransactionSchema.PAYMENT_METHOD], 'Credit Card')
        self.assertEqual(transaction[TransactionSchema.NOTES], 'Test notes')


if __name__ == '__main__':
    unittest.main()