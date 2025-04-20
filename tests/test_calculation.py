"""
Unit tests for financial calculation functions
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from core.calculation import (
    calculate_net_cashflow, calculate_cash_allocation,
    calculate_budget_comparison, calculate_savings_rate
)
from core.schema import TransactionSchema, CategorySchema


class TestCalculation(unittest.TestCase):
    """Test financial calculation functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Create test transaction data
        self.transaction_data = pd.DataFrame({
            TransactionSchema.DATE: pd.to_datetime(['2025-04-01', '2025-04-02', '2025-04-03', '2025-04-04']),
            TransactionSchema.DESCRIPTION: ['Salary', 'Rent', 'Savings Transfer', 'Investment Purchase'],
            TransactionSchema.AMOUNT: [2000.0, 800.0, 300.0, 400.0],
            TransactionSchema.TYPE: ['Income', 'Expense', 'Expense', 'Expense'],
            TransactionSchema.CATEGORY: ['Income', 'Housing', 'Savings', 'Investments'],
            TransactionSchema.SUBCATEGORY: ['Salary', 'Rent/Mortgage', 'Emergency Fund', 'Stocks'],
            TransactionSchema.PRODUCER: ['Employer', 'Landlord', 'Bank', 'Brokerage'],
            TransactionSchema.PAYMENT_METHOD: ['Direct Deposit', 'Bank Transfer', 'Bank Transfer', 'Bank Transfer'],
            TransactionSchema.NOTES: [None, None, None, None]
        })

        # Create test category data
        self.category_data = pd.DataFrame({
            CategorySchema.MAIN_CATEGORY: ['Housing', 'Savings', 'Investments'],
            CategorySchema.SUBCATEGORY: [['Rent/Mortgage'], ['Emergency Fund'], ['Stocks']],
            CategorySchema.DESCRIPTION: ['Housing expenses', 'Savings', 'Investments'],
            CategorySchema.BUDGET: [1000.0, 200.0, 300.0]
        })

    def test_calculate_net_cashflow(self):
        """Test net cashflow calculation"""
        income = 2000.0
        expense = 1500.0

        result = calculate_net_cashflow(income, expense)
        self.assertEqual(result, 500.0)

    def test_calculate_cash_allocation(self):
        """Test cash allocation calculation"""
        result = calculate_cash_allocation(self.transaction_data)

        # Calculate expected percentages
        total_expense = 1500.0  # 800 + 300 + 400
        spending_percent = (800.0 / total_expense) * 100  # Only Housing is regular spending
        saving_percent = (300.0 / total_expense) * 100
        investing_percent = (400.0 / total_expense) * 100

        # Check results
        self.assertAlmostEqual(result['Spending'], spending_percent)
        self.assertAlmostEqual(result['Saving'], saving_percent)
        self.assertAlmostEqual(result['Investing'], investing_percent)

        # Check that percentages add up to 100%
        self.assertAlmostEqual(
            result['Spending'] + result['Saving'] + result['Investing'],
            100.0
        )

    def test_calculate_budget_comparison(self):
        """Test budget comparison calculation"""
        # Create category summary
        category_summary = pd.DataFrame({
            TransactionSchema.TYPE: ['Expense', 'Expense', 'Expense'],
            TransactionSchema.CATEGORY: ['Housing', 'Savings', 'Investments'],
            TransactionSchema.AMOUNT: [800.0, 300.0, 400.0]
        })

        # Calculate budget comparison
        result = calculate_budget_comparison(category_summary, self.category_data)

        # Check results
        housing_row = result[result[TransactionSchema.CATEGORY] == 'Housing']
        self.assertEqual(housing_row[TransactionSchema.AMOUNT].iloc[0], 800.0)
        self.assertEqual(housing_row[CategorySchema.BUDGET].iloc[0], 1000.0)
        self.assertEqual(housing_row['Difference'].iloc[0], 200.0)  # Under budget
        self.assertEqual(housing_row['Budget Used (%)'].iloc[0], 80.0)  # 80% of budget used

        savings_row = result[result[TransactionSchema.CATEGORY] == 'Savings']
        self.assertEqual(savings_row[TransactionSchema.AMOUNT].iloc[0], 300.0)
        self.assertEqual(savings_row[CategorySchema.BUDGET].iloc[0], 200.0)
        self.assertEqual(savings_row['Difference'].iloc[0], -100.0)  # Over budget
        self.assertEqual(savings_row['Budget Used (%)'].iloc[0], 150.0)  # 150% of budget used

    def test_calculate_savings_rate(self):
        """Test savings rate calculation"""
        income = 2000.0
        expenses = 800.0  # Only include regular spending, not savings/investments

        result = calculate_savings_rate(income, expenses)
        expected_rate = ((2000.0 - 800.0) / 2000.0) * 100  # (income - expenses) / income

        self.assertEqual(result, expected_rate)

        # Edge case: zero income
        result_zero = calculate_savings_rate(0, 100)
        self.assertEqual(result_zero, 0)


if __name__ == '__main__':
    unittest.main()