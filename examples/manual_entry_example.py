#!/usr/bin/env python3
"""
Example script showing manual transaction entry
"""

import sys
import os
import pandas as pd
from pathlib import Path
from datetime import datetime

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.core.schema import TransactionSchema
from cashflow_tracker.core.ingestion import create_manual_transaction
from cashflow_tracker.cli import main as tracker_main


def enter_manual_transaction():
    """Simulate manual transaction entry with user input"""
    # In a real application, this would use input() to get data from the user
    # Here we'll simulate a console-based transaction entry

    print("Enter transaction details:")
    print("-------------------------")

    # In a real app, these would be gathered using input()
    # date = input("Date (YYYY-MM-DD): ")
    # description = input("Description: ")
    # amount = float(input("Amount: "))
    # ...

    # For this example, we'll use predefined values
    date = "2025-04-15"
    description = "Grocery shopping at Whole Foods"
    amount = 87.35
    transaction_type = "Expense"
    category = "Food"
    subcategory = "Groceries"
    producer = "Whole Foods"
    payment_method = "Credit Card"
    notes = "Weekly grocery shopping"

    # Echo the input values
    print(f"Date: {date}")
    print(f"Description: {description}")
    print(f"Amount: ${amount}")
    print(f"Type: {transaction_type}")
    print(f"Category: {category}")
    print(f"Subcategory: {subcategory}")
    print(f"Producer/Vendor: {producer}")
    print(f"Payment Method: {payment_method}")
    print(f"Notes: {notes}")

    # Create the transaction
    transaction = create_manual_transaction(
        date=date,
        description=description,
        amount=amount,
        transaction_type=transaction_type,
        category=category,
        subcategory=subcategory,
        producer=producer,
        payment_method=payment_method,
        notes=notes
    )

    return transaction


def main():
    """Main function for manual transaction entry example"""
    print("Cashflow Tracker - Manual Transaction Entry Example")
    print("==================================================")

    # Create a transactions DataFrame
    transactions = pd.DataFrame(columns=TransactionSchema.get_columns())

    # Add some predefined transactions
    transactions = pd.concat([transactions, pd.DataFrame([{
        TransactionSchema.DATE: pd.to_datetime("2025-04-01"),
        TransactionSchema.DESCRIPTION: "Monthly Salary",
        TransactionSchema.AMOUNT: 3500.00,
        TransactionSchema.TYPE: "Income",
        TransactionSchema.CATEGORY: "Income",
        TransactionSchema.SUBCATEGORY: "Salary",
        TransactionSchema.PRODUCER: "Employer Inc.",
        TransactionSchema.PAYMENT_METHOD: "Direct Deposit",
        TransactionSchema.NOTES: "Regular monthly salary"
    }])], ignore_index=True)

    transactions = pd.concat([transactions, pd.DataFrame([{
        TransactionSchema.DATE: pd.to_datetime("2025-04-03"),
        TransactionSchema.DESCRIPTION: "Rent Payment",
        TransactionSchema.AMOUNT: 1200.00,
        TransactionSchema.TYPE: "Expense",
        TransactionSchema.CATEGORY: "Housing",
        TransactionSchema.SUBCATEGORY: "Rent/Mortgage",
        TransactionSchema.PRODUCER: "Landlord",
        TransactionSchema.PAYMENT_METHOD: "Bank Transfer",
        TransactionSchema.NOTES: "Monthly apartment rent"
    }])], ignore_index=True)

    transactions = pd.concat([transactions, pd.DataFrame([{
        TransactionSchema.DATE: pd.to_datetime("2025-04-10"),
        TransactionSchema.DESCRIPTION: "Netflix Subscription",
        TransactionSchema.AMOUNT: 15.99,
        TransactionSchema.TYPE: "Expense",
        TransactionSchema.CATEGORY: "Entertainment",
        TransactionSchema.SUBCATEGORY: "Subscriptions",
        TransactionSchema.PRODUCER: "Netflix",
        TransactionSchema.PAYMENT_METHOD: "Credit Card",
        TransactionSchema.NOTES: "Monthly streaming service"
    }])], ignore_index=True)

    # Interactive mode - Add multiple transactions through user input
    add_more = True
    while add_more:
        print("\nAdding a new transaction...\n")
        new_transaction = enter_manual_transaction()
        transactions = pd.concat([transactions, pd.DataFrame([new_transaction])], ignore_index=True)

        # In a real app, we would ask for confirmation
        # add_more = input("\nAdd another transaction? (y/n): ").lower().startswith('y')

        # For this example, we'll just add one transaction
        add_more = False

    print("\nAll transactions:")
    print("------------------")
    # Format the display of transactions
    display_df = transactions.copy()
    display_df[TransactionSchema.DATE] = display_df[TransactionSchema.DATE].dt.strftime('%Y-%m-%d')

    # Print a simplified view
    for i, row in display_df.iterrows():
        print(f"{row[TransactionSchema.DATE]} | {row[TransactionSchema.DESCRIPTION]:<30} | "
              f"${row[TransactionSchema.AMOUNT]:>8.2f} | {row[TransactionSchema.TYPE]:<7} | "
              f"{row[TransactionSchema.CATEGORY]}")

    # Save transactions to CSV
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    csv_file = os.path.join(output_dir, "manual_transactions.csv")
    transactions.to_csv(csv_file, index=False)
    print(f"\nTransactions saved to '{csv_file}'")

    # Generate the Excel tracker
    excel_file = os.path.join(output_dir, "manual_tracker.xlsx")
    print(f"\nGenerating Excel cashflow tracker to '{excel_file}'...")

    # Prepare arguments for the CLI function
    sys.argv = ['dummy', '--input', csv_file, '--output', excel_file, '--charts']
    tracker_main()

    print("\nProcess completed!")
    print("\nOutput files:")
    print(f"  - {csv_file} (transaction data)")
    print(f"  - {excel_file} (Excel tracker)")
    print(f"  - {output_dir}/charts/ (visualizations)")

    print("\nSummary statistics:")
    total_income = transactions[transactions[TransactionSchema.TYPE] == 'Income'][TransactionSchema.AMOUNT].sum()
    total_expenses = transactions[transactions[TransactionSchema.TYPE] == 'Expense'][TransactionSchema.AMOUNT].sum()
    net_cashflow = total_income - total_expenses

    print(f"Total Income: ${total_income:.2f}")
    print(f"Total Expenses: ${total_expenses:.2f}")
    print(f"Net Cashflow: ${net_cashflow:.2f}")

    print("\nThank you for using Cashflow Tracker!")


if __name__ == "__main__":
    main()