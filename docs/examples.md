# Cashflow Tracker Examples

This document provides practical examples of using the Cashflow Tracker for various tasks.

## Example 1: Basic Usage with Sample Data

This example demonstrates how to generate and analyze sample data.

```python
from cashflow_tracker.utils.defaults import generate_sample_transactions
from cashflow_tracker.core.processing import clean_transaction_data
from cashflow_tracker.core.aggregation import aggregate_by_type
from cashflow_tracker.output.excel import create_excel_workbook, populate_transaction_sheet

# Generate sample data (100 transactions)
transactions = generate_sample_transactions(num_transactions=100)

# Clean the data
transactions = clean_transaction_data(transactions)

# Get summary information
type_summary = aggregate_by_type(transactions)
print(f"Total Income: ${type_summary.get('Income', 0):.2f}")
print(f"Total Expenses: ${type_summary.get('Expense', 0):.2f}")
print(f"Net Cashflow: ${type_summary.get('Income', 0) - type_summary.get('Expense', 0):.2f}")

# Create an Excel workbook
wb = create_excel_workbook()
populate_transaction_sheet(wb, transactions)
wb.save("sample_data.xlsx")
```

## Example 2: Processing a Bank Statement

This example shows how to process a bank statement CSV file.

```python
import pandas as pd
from cashflow_tracker.core.schema import TransactionSchema
from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_all_transactions, extract_all_producers
)
from cashflow_tracker.utils.defaults import (
    create_category_rules, create_producer_patterns
)
from cashflow_tracker.cli import main as tracker_main

# Read the bank statement
bank_data = pd.read_csv("bank_statement.csv")

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
        TransactionSchema.CATEGORY: None,
        TransactionSchema.SUBCATEGORY: None,
        TransactionSchema.PRODUCER: None,
        TransactionSchema.PAYMENT_METHOD: 'Bank Account',
        TransactionSchema.NOTES: None
    }
    
    rows.append(transaction)

transactions = pd.DataFrame(rows)

# Process transactions
category_rules = create_category_rules()
producer_patterns = create_producer_patterns()

transactions = clean_transaction_data(transactions)
transactions = categorize_all_transactions(transactions, category_rules)
transactions = extract_all_producers(transactions, producer_patterns)

# Save processed transactions
transactions.to_csv("processed_transactions.csv", index=False)

# Generate Excel tracker
tracker_main(['--input', 'processed_transactions.csv', 
              '--output', 'bank_tracker.xlsx',
              '--charts'])
```

## Example 3: Manual Transaction Entry

This example demonstrates manual transaction entry.

```python
import pandas as pd
from cashflow_tracker.core.schema import TransactionSchema
from cashflow_tracker.core.ingestion import create_manual_transaction
from cashflow_tracker.output.excel import (
    create_excel_workbook, populate_transaction_sheet,
    populate_category_sheet, populate_summary_sheet, create_charts
)
from cashflow_tracker.utils.defaults import create_default_categories
from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category, aggregate_by_month
)
from cashflow_tracker.core.calculation import calculate_cash_allocation

# Create transactions DataFrame
transactions = pd.DataFrame(columns=TransactionSchema.get_columns())

# Add transactions
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

# Add another transaction using create_manual_transaction
new_transaction = create_manual_transaction(
    date="2025-04-03",
    description="Rent Payment",
    amount=1200.00,
    transaction_type="Expense",
    category="Housing",
    subcategory="Rent/Mortgage",
    producer="Landlord",
    payment_method="Bank Transfer",
    notes="Monthly rent payment"
)

transactions = pd.concat([transactions, pd.DataFrame([new_transaction])], ignore_index=True)

# Save to CSV
transactions.to_csv("manual_transactions.csv", index=False)

# Generate Excel workbook
wb = create_excel_workbook()
populate_transaction_sheet(wb, transactions)

# Add categories
categories = create_default_categories()
populate_category_sheet(wb, categories)

# Calculate summaries
type_summary = aggregate_by_type(transactions)
category_summary = aggregate_by_category(transactions)
monthly_summary = aggregate_by_month(transactions)
cash_allocation = calculate_cash_allocation(transactions)

# Populate summary and charts
populate_summary_sheet(wb, type_summary, category_summary, cash_allocation)
create_charts(wb, category_summary, cash_allocation, monthly_summary)

# Save workbook
wb.save("manual_tracker.xlsx")
```

## Example 4: Advanced Visualizations

This example shows how to create advanced visualizations.

```python
import pandas as pd
import os
from cashflow_tracker.utils.defaults import generate_sample_transactions
from cashflow_tracker.output.visualisations import (
    create_matplotlib_charts, create_advanced_visualizations
)
from cashflow_tracker.utils.defaults import create_default_categories

# Generate sample data
transactions = generate_sample_transactions(num_transactions=200)

# Create output directory
output_dir = 'advanced_charts'
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Generate standard charts
create_matplotlib_charts(transactions, output_dir)

# Generate advanced charts
categories = create_default_categories()
create_advanced_visualizations(transactions, output_dir, categories)

print(f"Charts generated in '{output_dir}' directory")
```

## Example 5: Budget Analysis

This example demonstrates budget analysis.

```python
import pandas as pd
from cashflow_tracker.utils.defaults import (
    generate_sample_transactions, create_default_categories
)
from cashflow_tracker.core.calculation import calculate_budget_comparison
from cashflow_tracker.core.aggregation import aggregate_by_category
import matplotlib.pyplot as plt

# Generate sample data
transactions = generate_sample_transactions(num_transactions=150)

# Get categories with budgets
category_data = create_default_categories()

# Aggregate by category