"""
Unit tests for data processing functions
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_transaction,
    categorize_all_transactions, extract_producer,
    extract_all_producers
)
from cashflow_tracker.core.schema import TransactionSchema


class TestProcessing(unittest.TestCase):
    """Test data processing functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Create test data
        self.test_data = pd.DataFrame({
            'Date': ['2025-04-01', '2025-04-02', '2025-04-03'],
            'Description': ['Salary Payment', 'Groceries at Walmart', 'Netflix Subscription'],
            'Amount': [1000.0, -50.0, -15.99],
        })

        # Define test category rules
        self.category_rules = {
            'Income': ['salary', 'deposit', 'paycheck'],
            'Food': ['groceries', 'supermarket', 'restaurant'],
            'Entertainment': ['netflix', 'movie', 'subscription']
        }

        # Define test producer patterns
        self.producer_patterns = {
            r'walmart': 'Walmart',
            r'netflix': 'Netflix'
        }

    def test_clean_transaction_data(self):
        """Test transaction data cleaning"""
        df = clean_transaction_data(self.test_data)

        # Check that all schema columns are present
        for col in TransactionSchema.get_columns():
            self.assertIn(col, df.columns)

        # Check that date is converted to datetime
        self.assertTrue(pd.api.types.is_datetime64_dtype(df[TransactionSchema.DATE]))

        # Check that transaction types are correctly assigned based on amount
        self.assertEqual(df[TransactionSchema.TYPE].iloc[0], 'Income')
        self.assertEqual(df[TransactionSchema.TYPE].iloc[1], 'Expense')
        self.assertEqual(df[TransactionSchema.TYPE].iloc[2], 'Expense')

        # Check that expense amounts are converted to positive
        self.assertEqual(df[TransactionSchema.AMOUNT].iloc[1], 50.0)
        self.assertEqual(df[TransactionSchema.AMOUNT].iloc[2], 15.99)

    def test_categorize_transaction(self):
        """Test transaction categorization"""
        # Clean the data first
        df = clean_transaction_data(self.test_data)

        # Test each transaction
        categorized_transaction1 = categorize_transaction(
            df.iloc[0], self.category_rules
        )
        self.assertEqual(categorized_transaction1[TransactionSchema.CATEGORY], 'Income')

        categorized_transaction2 = categorize_transaction(
            df.iloc[1], self.category_rules
        )
        self.assertEqual(categorized_transaction2[TransactionSchema.CATEGORY], 'Food')

        categorized_transaction3 = categorize_transaction(
            df.iloc[2], self.category_rules
        )
        self.assertEqual(categorized_transaction3[TransactionSchema.CATEGORY], 'Entertainment')

    def test_categorize_all_transactions(self):
        """Test transaction categorization for all rows"""
        # Clean the data first
        df = clean_transaction_data(self.test_data)

        # Categorize all transactions
        categorized_df = categorize_all_transactions(df, self.category_rules)

        # Check categories
        self.assertEqual(categorized_df[TransactionSchema.CATEGORY].iloc[0], 'Income')
        self.assertEqual(categorized_df[TransactionSchema.CATEGORY].iloc[1], 'Food')
        self.assertEqual(categorized_df[TransactionSchema.CATEGORY].iloc[2], 'Entertainment')

    def test_extract_producer(self):
        """Test producer extraction"""
        # Clean the data first
        df = clean_transaction_data(self.test_data)

        # Test each transaction
        transaction1 = extract_producer(df.iloc[0], self.producer_patterns)
        self.assertEqual(transaction1[TransactionSchema.PRODUCER], 'Salary')  # First word in description

        transaction2 = extract_producer(df.iloc[1], self.producer_patterns)
        self.assertEqual(transaction2[TransactionSchema.PRODUCER], 'Walmart')  # Matched pattern

        transaction3 = extract_producer(df.iloc[2], self.producer_patterns)
        self.assertEqual(transaction3[TransactionSchema.PRODUCER], 'Netflix')  # Matched pattern

    def test_extract_all_producers(self):
        """Test producer extraction for all rows"""
        # Clean the data first
        df = clean_transaction_data(self.test_data)

        # Extract producers for all transactions
        df_with_producers = extract_all_producers(df, self.producer_patterns)

        # Check producers
        self.assertEqual(df_with_producers[TransactionSchema.PRODUCER].iloc[0], 'Salary')
        self.assertEqual(df_with_producers[TransactionSchema.PRODUCER].iloc[1], 'Walmart')
        self.assertEqual(df_with_producers[TransactionSchema.PRODUCER].iloc[2], 'Netflix')


if __name__ == '__main__':
    unittest.main()