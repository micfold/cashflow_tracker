"""
Unit tests for data aggregation functions
"""

import unittest
import pandas as pd
import sys
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category,
    aggregate_by_producer, aggregate_by_month,
    aggregate_by_payment_method, aggregate_by_subcategory
)
from cashflow_tracker.core.schema import TransactionSchema


class TestAggregation(unittest.TestCase):
    """Test data aggregation functions"""

    def setUp(self):
        """Set up test fixtures"""
        # Create test data
        self.test_data = pd.DataFrame({
            TransactionSchema.DATE: pd.to_datetime([
                '2025-04-01', '2025-04-15', '2025-04-20',
                '2025-05-01', '2025-05-15'
            ]),
            TransactionSchema.DESCRIPTION: [
                'Salary', 'Groceries', 'Restaurant',
                'Salary', 'Rent'
            ],
            TransactionSchema.AMOUNT: [
                3000.0, 150.0, 75.0,
                3000.0, 1200.0
            ],
            TransactionSchema.TYPE: [
                'Income', 'Expense', 'Expense',
                'Income', 'Expense'
            ],
            TransactionSchema.CATEGORY: [
                'Income', 'Food', 'Food',
                'Income', 'Housing'
            ],
            TransactionSchema.SUBCATEGORY: [
                'Salary', 'Groceries', 'Restaurants',
                'Salary', 'Rent/Mortgage'
            ],
            TransactionSchema.PRODUCER: [
                'Employer', 'Grocery Store', 'Restaurant',
                'Employer', 'Landlord'
            ],
            TransactionSchema.PAYMENT_METHOD: [
                'Direct Deposit', 'Credit Card', 'Cash',
                'Direct Deposit', 'Bank Transfer'
            ],
            TransactionSchema.NOTES: [
                None, None, None, None, None
            ]
        })

    def test_aggregate_by_type(self):
        """Test aggregation by transaction type"""
        result = aggregate_by_type(self.test_data)

        # Check results
        self.assertEqual(result['Income'], 6000.0)
        self.assertEqual(result['Expense'], 1425.0)

    def test_aggregate_by_category(self):
        """Test aggregation by category"""
        result = aggregate_by_category(self.test_data)

        # Check that we have the right number of rows
        self.assertEqual(len(result), 3)  # Income, Food, Housing

        # Check specific values
        income_row = result[(result[TransactionSchema.TYPE] == 'Income') &
                            (result[TransactionSchema.CATEGORY] == 'Income')]
        self.assertEqual(income_row[TransactionSchema.AMOUNT].iloc[0], 6000.0)

        food_row = result[(result[TransactionSchema.TYPE] == 'Expense') &
                          (result[TransactionSchema.CATEGORY] == 'Food')]
        self.assertEqual(food_row[TransactionSchema.AMOUNT].iloc[0], 225.0)

        housing_row = result[(result[TransactionSchema.TYPE] == 'Expense') &
                             (result[TransactionSchema.CATEGORY] == 'Housing')]
        self.assertEqual(housing_row[TransactionSchema.AMOUNT].iloc[0], 1200.0)

    def test_aggregate_by_producer(self):
        """Test aggregation by producer/vendor"""
        result = aggregate_by_producer(self.test_data)

        # Check that we have the right number of rows
        self.assertEqual(len(result), 4)  # Employer, Grocery Store, Restaurant, Landlord

        # Check specific values
        employer_row = result[(result[TransactionSchema.TYPE] == 'Income') &
                              (result[TransactionSchema.PRODUCER] == 'Employer')]
        self.assertEqual(employer_row[TransactionSchema.AMOUNT].iloc[0], 6000.0)

        grocery_row = result[(result[TransactionSchema.TYPE] == 'Expense') &
                             (result[TransactionSchema.PRODUCER] == 'Grocery Store')]
        self.assertEqual(grocery_row[TransactionSchema.AMOUNT].iloc[0], 150.0)

    def test_aggregate_by_month(self):
        """Test aggregation by month"""
        result = aggregate_by_month(self.test_data)

        # Check that we have the right number of rows
        self.assertEqual(len(result), 4)  # April Income, April Expense, May Income, May Expense

        # Check specific values
        april_income = result[(result['Month'] == '2025-04') &
                              (result[TransactionSchema.TYPE] == 'Income')]
        self.assertEqual(april_income[TransactionSchema.AMOUNT].iloc[0], 3000.0)

        april_expense = result[(result['Month'] == '2025-04') &
                               (result[TransactionSchema.TYPE] == 'Expense')]
        self.assertEqual(april_expense[TransactionSchema.AMOUNT].iloc[0], 225.0)

        may_income = result[(result['Month'] == '2025-05') &
                            (result[TransactionSchema.TYPE] == 'Income')]
        self.assertEqual(may_income[TransactionSchema.AMOUNT].iloc[0], 3000.0)

        may_expense = result[(result['Month'] == '2025-05') &
                             (result[TransactionSchema.TYPE] == 'Expense')]
        self.assertEqual(may_expense[TransactionSchema.AMOUNT].iloc[0], 1200.0)

    def test_aggregate_by_payment_method(self):
        """Test aggregation by payment method"""
        result = aggregate_by_payment_method(self.test_data)

        # Check that we have the right number of rows
        self.assertEqual(len(result), 4)  # Direct Deposit, Credit Card, Cash, Bank Transfer

        # Check specific values
        direct_deposit = result[(result[TransactionSchema.TYPE] == 'Income') &
                                (result[TransactionSchema.PAYMENT_METHOD] == 'Direct Deposit')]
        self.assertEqual(direct_deposit[TransactionSchema.AMOUNT].iloc[0], 6000.0)

        credit_card = result[(result[TransactionSchema.TYPE] == 'Expense') &
                             (result[TransactionSchema.PAYMENT_METHOD] == 'Credit Card')]
        self.assertEqual(credit_card[TransactionSchema.AMOUNT].iloc[0], 150.0)

    def test_aggregate_by_subcategory(self):
        """Test aggregation by subcategory"""
        result = aggregate_by_subcategory(self.test_data)

        # Check that we have the right number of rows
        self.assertEqual(len(result), 4)  # Salary, Groceries, Restaurants, Rent/Mortgage

        # Check specific values
        salary = result[(result[TransactionSchema.TYPE] == 'Income') &
                        (result[TransactionSchema.SUBCATEGORY] == 'Salary')]
        self.assertEqual(salary[TransactionSchema.AMOUNT].iloc[0], 6000.0)

        groceries = result[(result[TransactionSchema.TYPE] == 'Expense') &
                           (result[TransactionSchema.SUBCATEGORY] == 'Groceries')]
        self.assertEqual(groceries[TransactionSchema.AMOUNT].iloc[0], 150.0)

        restaurants = result[(result[TransactionSchema.TYPE] == 'Expense') &
                             (result[TransactionSchema.SUBCATEGORY] == 'Restaurants')]
        self.assertEqual(restaurants[TransactionSchema.AMOUNT].iloc[0], 75.0)


if __name__ == '__main__':
    unittest.main()