"""
Command-line interface for the Cashflow Tracker
"""

import argparse
import os
import pandas as pd
from cashflow_tracker.core.schema import TransactionSchema
from cashflow_tracker.core.ingestion import ingest_csv, ingest_excel
from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_all_transactions, extract_all_producers
)
from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category,
    aggregate_by_producer, aggregate_by_month
)
from cashflow_tracker.core.calculation import (
    calculate_net_cashflow, calculate_cash_allocation, calculate_budget_comparison
)
from cashflow_tracker.output.excel import (
    create_excel_workbook, populate_transaction_sheet,
    populate_category_sheet, populate_summary_sheet, create_charts
)
from cashflow_tracker.output.visualisations import create_matplotlib_charts
from cashflow_tracker.utils.defaults import (
    create_default_categories, create_category_rules,
    create_producer_patterns, generate_sample_transactions
)


def main():
    """
    Main function to run the cashflow tracker from command line
    """
    parser = argparse.ArgumentParser(description='Cashflow Tracker')
    parser.add_argument('--input', help='Input file path (CSV or Excel)')
    parser.add_argument('--output', default='cashflow_tracker.xlsx',
                        help='Output Excel file path')
    parser.add_argument('--sample', action='store_true',
                        help='Generate sample data')
    parser.add_argument('--num-samples', type=int, default=50,
                        help='Number of sample transactions to generate')
    parser.add_argument('--charts', action='store_true',
                        help='Generate additional matplotlib charts')
    parser.add_argument('--charts-dir', default='charts',
                        help='Directory to save additional charts')

    args = parser.parse_args()

    # Step 1: Data ingestion
    if args.sample:
        print("Generating sample data...")
        transaction_data = generate_sample_transactions(args.num_samples)
    elif args.input:
        print(f"Reading data from {args.input}...")
        if args.input.endswith('.csv'):
            transaction_data = ingest_csv(args.input)
        elif args.input.endswith(('.xlsx', '.xls')):
            transaction_data = ingest_excel(args.input)
        else:
            raise ValueError("Unsupported file format. Use CSV or Excel.")
    else:
        # Create empty transaction log
        transaction_data = pd.DataFrame(columns=TransactionSchema.get_columns())

    # Step 2: Data cleaning
    print("Cleaning and normalizing data...")
    transaction_data = clean_transaction_data(transaction_data)

    # Step 3: Create categories
    print("Setting up categories...")
    category_data = create_default_categories()

    # Step 4: Process transactions (categorize & extract producer)
    print("Processing transactions...")
    category_rules = create_category_rules()
    producer_patterns = create_producer_patterns()

    if not transaction_data.empty:
        transaction_data = categorize_all_transactions(transaction_data, category_rules)
        transaction_data = extract_all_producers(transaction_data, producer_patterns)

    # Step 5: Aggregate data
    print("Aggregating data...")
    type_summary = aggregate_by_type(transaction_data)
    category_summary = aggregate_by_category(transaction_data)
    producer_summary = aggregate_by_producer(transaction_data)
    monthly_summary = aggregate_by_month(transaction_data)

    # Step 6: Calculations
    print("Performing calculations...")
    net_cashflow = calculate_net_cashflow(type_summary.get('Income', 0), type_summary.get('Expense', 0))
    cash_allocation = calculate_cash_allocation(transaction_data)
    budget_comparison = calculate_budget_comparison(category_summary, category_data)

    # Step 7: Create Excel workbook
    print("Creating Excel workbook...")
    wb = create_excel_workbook()

    # Step 8: Populate sheets
    print("Populating sheets...")
    populate_transaction_sheet(wb, transaction_data)
    populate_category_sheet(wb, category_data)
    populate_summary_sheet(wb, type_summary, category_summary, cash_allocation, budget_comparison)
    create_charts(wb, category_summary, cash_allocation, monthly_summary)

    # Step 9: Save workbook
    print(f"Saving workbook to {args.output}...")
    wb.save(args.output)

    # Step 10: Generate additional charts if requested
    if args.charts:
        print(f"Generating additional charts in '{args.charts_dir}'...")
        if not os.path.exists(args.charts_dir):
            os.makedirs(args.charts_dir)
        create_matplotlib_charts(transaction_data, args.charts_dir)

    print("Done!")
    return 0