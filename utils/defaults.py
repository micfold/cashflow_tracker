"""
Default values and generators for the Cashflow Tracker
"""

import pandas as pd
import random
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from core.schema import TransactionSchema, CategorySchema


def create_default_categories() -> pd.DataFrame:
    """
    Create default categories with budgets

    Returns:
        DataFrame with category data
    """
    categories = {
        CategorySchema.MAIN_CATEGORY: [
            'Income', 'Housing', 'Transportation', 'Food',
            'Entertainment', 'Shopping', 'Personal',
            'Savings', 'Investments', 'Debt', 'Miscellaneous'
        ],
        CategorySchema.SUBCATEGORY: [
            ['Salary', 'Freelance', 'Investments', 'Gifts', 'Other Income'],
            ['Rent/Mortgage', 'Utilities', 'Maintenance', 'Insurance'],
            ['Gas', 'Public Transit', 'Car Payment', 'Car Insurance', 'Maintenance'],
            ['Groceries', 'Restaurants', 'Takeout'],
            ['Movies', 'Games', 'Events', 'Subscriptions'],
            ['Clothing', 'Electronics', 'Home Goods'],
            ['Healthcare', 'Education', 'Gym', 'Personal Care'],
            ['Emergency Fund', 'Goals'],
            ['Stocks', 'Bonds', 'Real Estate', 'Cryptocurrency'],
            ['Credit Card', 'Student Loans', 'Personal Loans'],
            ['Other']
        ],
        CategorySchema.DESCRIPTION: [
            'All income sources',
            'Housing-related expenses',
            'Transportation-related expenses',
            'Food and dining expenses',
            'Entertainment and leisure',
            'Shopping for goods',
            'Personal care and development',
            'Money set aside for savings',
            'Investment activities',
            'Debt payments',
            'Miscellaneous expenses'
        ],
        CategorySchema.BUDGET: [
            0,  # Income (no budget constraint)
            1000,  # Housing
            500,  # Transportation
            400,  # Food
            200,  # Entertainment
            300,  # Shopping
            200,  # Personal
            300,  # Savings
            200,  # Investments
            500,  # Debt
            100  # Miscellaneous
        ]
    }

    return pd.DataFrame(categories)


def create_category_rules() -> Dict[str, List[str]]:
    """
    Create default rules for auto-categorization

    Returns:
        Dict with keywords for each category
    """
    return {
        'Housing': ['rent', 'mortgage', 'home', 'apartment', 'electricity',
                    'water', 'gas bill', 'internet', 'maintenance'],
        'Transportation': ['gas', 'fuel', 'bus', 'train', 'subway', 'uber', 'lyft', 'taxi',
                           'car payment', 'insurance', 'repair', 'maintenance'],
        'Food': ['grocery', 'restaurant', 'cafe', 'coffee', 'takeout', 'doordash',
                 'ubereats', 'grubhub', 'dining'],
        'Entertainment': ['movie', 'theater', 'concert', 'subscription', 'netflix',
                          'spotify', 'amazon prime', 'hulu', 'disney', 'ticket'],
        'Shopping': ['amazon', 'walmart', 'target', 'clothing', 'shoes', 'electronics',
                     'furniture', 'home goods', 'appliance'],
        'Personal': ['doctor', 'medical', 'pharmacy', 'gym', 'fitness', 'education',
                     'tuition', 'books', 'haircut', 'salon', 'spa'],
        'Savings': ['transfer to savings', 'emergency fund', 'savings goal'],
        'Investments': ['investment', 'stock', 'etf', 'mutual fund', 'bond', 'real estate',
                        'crypto', 'bitcoin', 'ethereum'],
        'Debt': ['credit card payment', 'loan payment', 'student loan', 'debt'],
        'Income': ['salary', 'paycheck', 'deposit', 'dividend', 'interest', 'refund',
                   'payment received', 'client payment']
    }


def create_producer_patterns() -> Dict[str, str]:
    """
    Create default patterns for producer/vendor extraction

    Returns:
        Dict with regex patterns and producer names
    """
    return {
        r'amazon': 'Amazon',
        r'netflix': 'Netflix',
        r'spotify': 'Spotify',
        r'uber(eats)?': 'Uber',
        r'lyft': 'Lyft',
        r'doordash': 'DoorDash',
        r'grubhub': 'GrubHub',
        r'walmart': 'Walmart',
        r'target': 'Target',
        r'starbucks': 'Starbucks',
        r'mcdonald\'?s': 'McDonalds',
        r'deposit': 'Bank Deposit',
        r'transfer': 'Bank Transfer',
        r'withdrawal': 'ATM Withdrawal',
        r'payroll|direct deposit|salary': 'Employer',
        r'insurance': 'Insurance Company',
        r'mortgage|rent': 'Housing Provider',
        r'electric|gas|water|utility': 'Utility Company',
        r'phone|mobile|wireless': 'Phone Provider',
        r'internet|cable|wifi': 'Internet Provider'
    }


def generate_sample_transactions(num_transactions: int = 50) -> pd.DataFrame:
    """
    Generate sample transactions for testing

    Args:
        num_transactions: Number of transactions to generate

    Returns:
        DataFrame with sample transactions
    """
    # Categories and subcategories
    categories = {
        'Income': ['Salary', 'Freelance', 'Investments'],
        'Housing': ['Rent/Mortgage', 'Utilities'],
        'Transportation': ['Gas', 'Public Transit'],
        'Food': ['Groceries', 'Restaurants'],
        'Entertainment': ['Movies', 'Subscriptions'],
        'Shopping': ['Clothing', 'Electronics'],
        'Savings': ['Emergency Fund'],
        'Investments': ['Stocks']
    }

    # Producers for each category
    producers = {
        'Income': ['Employer', 'Client', 'Dividend'],
        'Housing': ['Landlord', 'Electric Company', 'Water Company'],
        'Transportation': ['Gas Station', 'Transit Authority', 'Uber'],
        'Food': ['Grocery Store', 'Restaurant', 'Cafe'],
        'Entertainment': ['Cinema', 'Netflix', 'Spotify'],
        'Shopping': ['Amazon', 'Walmart', 'Target'],
        'Savings': ['Bank'],
        'Investments': ['Brokerage']
    }

    # Descriptions
    descriptions = {
        'Income': ['Monthly Salary', 'Client Payment', 'Dividend Payment'],
        'Housing': ['Monthly Rent', 'Electricity Bill', 'Water Bill'],
        'Transportation': ['Gas Refill', 'Monthly Transit Pass', 'Uber Ride'],
        'Food': ['Grocery Shopping', 'Dinner Out', 'Lunch'],
        'Entertainment': ['Movie Tickets', 'Netflix Subscription', 'Spotify Premium'],
        'Shopping': ['Online Purchase', 'Clothing', 'Electronics'],
        'Savings': ['Transfer to Savings'],
        'Investments': ['Stock Purchase']
    }

    # Generate transactions
    transactions = []
    today = datetime.now()

    for _ in range(num_transactions):
        # Random date within the last 3 months
        days_ago = random.randint(0, 90)
        date = today - timedelta(days=days_ago)

        # 80% chance of expense, 20% chance of income
        transaction_type = 'Income' if random.random() < 0.2 else 'Expense'

        if transaction_type == 'Income':
            category = 'Income'
            amount = random.uniform(1000, 5000)
        else:
            # Random category for expenses
            category = random.choice([c for c in categories.keys() if c != 'Income'])

            # Amount depends on category
            if category == 'Housing':
                amount = random.uniform(800, 2000)
            elif category == 'Transportation':
                amount = random.uniform(20, 200)
            elif category == 'Food':
                amount = random.uniform(10, 150)
            elif category == 'Entertainment':
                amount = random.uniform(10, 50)
            elif category == 'Shopping':
                amount = random.uniform(20, 500)
            elif category == 'Savings':
                amount = random.uniform(100, 1000)
            elif category == 'Investments':
                amount = random.uniform(100, 2000)
            else:
                amount = random.uniform(10, 100)

        # Random subcategory, producer, and description
        subcategory = random.choice(categories.get(category, ['Other']))
        producer = random.choice(producers.get(category, ['Other']))
        description = random.choice(descriptions.get(category, ['Payment']))

        # Payment method
        payment_methods = ['Credit Card', 'Debit Card', 'Cash', 'Bank Transfer']
        payment_method = random.choice(payment_methods)

        # Create transaction
        transaction = {
            TransactionSchema.DATE: date,
            TransactionSchema.DESCRIPTION: description,
            TransactionSchema.AMOUNT: amount,
            TransactionSchema.TYPE: transaction_type,
            TransactionSchema.CATEGORY: category,
            TransactionSchema.SUBCATEGORY: subcategory,
            TransactionSchema.PRODUCER: producer,
            TransactionSchema.PAYMENT_METHOD: payment_method,
            TransactionSchema.NOTES: None
        }

        transactions.append(transaction)

    return pd.DataFrame(transactions)