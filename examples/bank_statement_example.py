"""
Example script showing how to process a bank statement
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.core.schema import TransactionSchema
from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_all_transactions, extract_all_producers
)
from cashflow_tracker.utils.defaults import (
    create_category_rules, create_producer_patterns
)
from cashflow_tracker.cli import main as tracker_main


def create_sample_bank_statement():
    """Create a sample bank statement CSV for demonstration"""
    print("Creating sample bank statement...")

    # Sample bank statement data
    bank_data = {
        'Date': [
            '2025-04-01', '2025-04-02', '2025-04-05',
            '2025-04-10', '2025-04-15', '2025-04-20',
            '2025-04-25', '2025-04-28', '2025-04-30'
        ],
        'Description': [
            'DEPOSIT - EMPLOYER INC',
            'PAYMENT - APARTMENT RENT',
            'POS PURCHASE - KROGER GROCERY',
            'ACH DEBIT - NETFLIX SUBSCRIPTION',
            'TRANSFER TO SAVINGS',
            'POS PURCHASE - AMAZON.COM',
            'POS PURCHASE - SHELL OIL',
            'ELECTRONIC PMT - CREDIT CARD',
            'DEPOSIT - FREELANCE PAYMENT'
        ],
        'Debit': [
            '', '1200.00', '89.50', '15.99', '200.00', '45.75', '35.25', '150.00', ''
        ],
        'Credit': [
            '3500.00', '', '', '', '', '', '', '', '750.00'
        ]
    }

    # Create DataFrame and save to CSV
    bank_df = pd.DataFrame(bank_data)
    output_file = 'sample_bank_statement.csv'
    bank_df.to_csv(output_file, index=False)

    print(f"Sample bank statement created at '{output_file}'")
    return output_file


def process_bank_statement(bank_file):
    """Process a bank statement CSV file"""
    print(f"Processing bank statement from '{bank_file}'...")

    # Read the bank statement
    bank_data = pd.read_csv(bank_file)

    # Transform to standard format
    transactions = pd.DataFrame(columns=TransactionSchema.get_columns())
    rows = []

    for _, row in bank_data.iterrows():
        # Determine transaction type and amount
        if row['Credit'] and float(row['Credit']) > 0:
            amount = float(row['Credit'])
            transaction_type = 'Income'
        else:
            amount = float(row['Debit']) if row['Debit'] else 0
            transaction_type = 'Expense'

        # Create transaction
        transaction = {
            TransactionSchema.DATE: pd.to_datetime(row['Date']),
            TransactionSchema.DESCRIPTION: row['Description'],
            TransactionSchema.AMOUNT: amount,
            TransactionSchema.TYPE: transaction_type,
            # Other fields will be filled by processing functions
            TransactionSchema.CATEGORY: None,
            TransactionSchema.SUBCATEGORY: None,
            TransactionSchema.PRODUCER: None,
            TransactionSchema.PAYMENT_METHOD: 'Bank Account',
            TransactionSchema.NOTES: None
        }

        rows.append(transaction)

    transactions = pd.DataFrame(rows)

    # Process transactions
    print("Categorizing transactions...")
    category_rules = create_category_rules()
    producer_patterns = create_producer_patterns()

    transactions = clean_transaction_data(transactions)
    transactions = categorize_all_transactions(transactions, category_rules)
    transactions = extract_all_producers(transactions, producer_patterns)

    # Save processed transactions
    output_file = 'processed_bank_statement.csv'
    transactions.to_csv(output_file, index=False)
    print(f"Processed transactions saved to '{output_file}'")

    return output_file


def main():
    """Main function"""
    # First create a sample bank statement
    bank_file = create_sample_bank_statement()

    # Process the bank statement
    processed_file = process_bank_statement(bank_file)

    # Generate the Excel tracker
    print("\nGenerating Excel cashflow tracker...")
    tracker_main(['--input', processed_file,
                  '--output', 'bank_statement_tracker.xlsx',
                  '--charts'])

    print("\nProcess completed!")
    print("Output files:")
    print("  - sample_bank_statement.csv (raw bank data)")
    print("  - processed_bank_statement.csv (categorized transactions)")
    print("  - bank_statement_tracker.xlsx (Excel tracker)")
    print("  - charts/ (visualizations)")


if __name__ == "__main__":
    main()