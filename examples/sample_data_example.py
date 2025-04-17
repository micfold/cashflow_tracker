#!/usr/bin/env python3
"""
Example script showing how to generate and analyze sample data
"""

import sys
import os
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.utils.defaults import generate_sample_transactions
from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_all_transactions, extract_all_producers
)
from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category, aggregate_by_producer
)
from cashflow_tracker.core.calculation import (
    calculate_net_cashflow, calculate_cash_allocation
)
from cashflow_tracker.utils.defaults import (
    create_category_rules, create_producer_patterns
)
from cashflow_tracker.output.visualisations import create_matplotlib_charts


def main():
    """Generate and analyze sample data"""
    print("Generating sample data...")
    transactions = generate_sample_transactions(num_transactions=100)

    print(f"Generated {len(transactions)} sample transactions")

    # Process the transactions
    print("Processing transactions...")
    category_rules = create_category_rules()
    producer_patterns = create_producer_patterns()

    transactions = clean_transaction_data(transactions)
    transactions = categorize_all_transactions(transactions, category_rules)
    transactions = extract_all_producers(transactions, producer_patterns)

    # Analyze the data
    print("Analyzing data...")
    type_summary = aggregate_by_type(transactions)
    category_summary = aggregate_by_category(transactions)
    producer_summary = aggregate_by_producer(transactions)

    # Display summary information
    print("\nCashflow Summary:")
    print(f"Total Income: ${type_summary.get('Income', 0):.2f}")
    print(f"Total Expenses: ${type_summary.get('Expense', 0):.2f}")

    net_cashflow = calculate_net_cashflow(
        type_summary.get('Income', 0),
        type_summary.get('Expense', 0)
    )
    print(f"Net Cashflow: ${net_cashflow:.2f}")

    # Calculate and display cash allocation
    cash_allocation = calculate_cash_allocation(transactions)
    print("\nCash Allocation:")
    print(f"Spending: {cash_allocation.get('Spending', 0):.1f}%")
    print(f"Saving: {cash_allocation.get('Saving', 0):.1f}%")
    print(f"Investing: {cash_allocation.get('Investing', 0):.1f}%")

    # Display top spending categories
    expense_categories = category_summary[
        category_summary['Type'] == 'Expense'
        ].sort_values('Amount', ascending=False)

    print("\nTop Spending Categories:")
    for i, row in enumerate(expense_categories.head(5).itertuples(), 1):
        print(f"{i}. {row.Category}: ${row.Amount:.2f}")

    # Create visualizations
    output_dir = 'sample_charts'
    print(f"\nGenerating charts in '{output_dir}' directory...")
    create_matplotlib_charts(transactions, output_dir)
    print("Charts generated successfully!")

    # Save the transactions to CSV
    output_file = 'sample_transactions.csv'
    transactions.to_csv(output_file, index=False)
    print(f"Saved sample transactions to '{output_file}'")


if __name__ == "__main__":
    main()
