# Cashflow Tracker Usage Guide

This document provides detailed instructions on how to use the Cashflow Tracker system for tracking, analyzing, and visualizing your financial data.

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

1. Install the package using pip:

```bash
# From PyPI (once published)
pip install cashflow-tracker

# From source code
git clone https://github.com/yourusername/cashflow-tracker.git
cd cashflow-tracker
pip install -e .
```

2. Verify installation:

```bash
python -m cashflow_tracker --version
```

## Basic Usage

### Command Line Interface

The Cashflow Tracker provides a command line interface for common operations:

#### Generate a new tracker with sample data

```bash
python -m cashflow_tracker --sample --output my_finances.xlsx
```

#### Process an existing CSV file

```bash
python -m cashflow_tracker --input my_transactions.csv --output my_finances.xlsx
```

#### Generate charts and visualizations

```bash
python -m cashflow_tracker --input my_transactions.csv --charts
```

#### Get help on available commands

```bash
python -m cashflow_tracker --help
```

### Input Data Format

#### CSV Format

The Cashflow Tracker can import CSV files with the following columns:

```
Date,Description,Amount,Type,Category,Subcategory,Producer/Vendor,Payment Method,Notes
2025-04-01,Monthly Salary,3500.00,Income,Income,Salary,Acme Corporation,Direct Deposit,Regular monthly salary
2025-04-03,Apartment Rent,1200.00,Expense,Housing,Rent/Mortgage,Landlord,Bank Transfer,Monthly rent payment
```

Not all columns are required. At minimum, the following columns are needed:
- Date
- Description
- Amount

The system will attempt to infer missing information based on the data.

#### Bank Statement Format

The Cashflow Tracker can also import bank statements in various formats:

```
Date,Description,Debit,Credit,Balance
2025-04-01,"DIRECT DEPOSIT - ACME CORPORATION",,3500.00,3500.00
2025-04-03,"PAYMENT - APARTMENT RENT",1200.00,,2300.00
```

When importing bank statements, the system will:
1. Convert the data to the standard format
2. Classify transactions as Income (Credit) or Expense (Debit)
3. Attempt to categorize transactions based on descriptions

## Working with Transactions

### Adding Transactions Manually

You can add transactions programmatically:

```python
from cashflow_tracker.core.ingestion import create_manual_transaction
import pandas as pd

# Create a new transaction
transaction = create_manual_transaction(
    date="2025-04-15",
    description="Grocery shopping",
    amount=87.35,
    transaction_type="Expense",
    category="Food",
    subcategory="Groceries",
    producer="Whole Foods",
    payment_method="Credit Card",
    notes="Weekly grocery shopping"
)

# Create a DataFrame with the transaction
transactions = pd.DataFrame([transaction])

# Save to CSV
transactions.to_csv("my_transactions.csv", index=False)
```

### Categorizing Transactions

The Cashflow Tracker automatically categorizes transactions based on keywords in the description. You can customize the categorization rules:

```python
from cashflow_tracker.utils.defaults import create_category_rules
from cashflow_tracker.core.processing import categorize_all_transactions
import pandas as pd

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Get default category rules
category_rules = create_category_rules()

# Add a custom rule
category_rules["Health"] = ["pharmacy", "doctor", "medical", "clinic", "hospital"]

# Apply categorization
categorized_transactions = categorize_all_transactions(transactions, category_rules)

# Save categorized transactions
categorized_transactions.to_csv("categorized_transactions.csv", index=False)
```

## Analyzing Financial Data

### Basic Analysis

To perform basic financial analysis:

```python
from cashflow_tracker.core.aggregation import aggregate_by_type, aggregate_by_category
from cashflow_tracker.core.calculation import calculate_net_cashflow, calculate_cash_allocation
import pandas as pd

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Aggregate by type (Income/Expense)
type_summary = aggregate_by_type(transactions)
income = type_summary.get('Income', 0)
expenses = type_summary.get('Expense', 0)

# Calculate net cashflow
net_cashflow = calculate_net_cashflow(income, expenses)
print(f"Net Cashflow: ${net_cashflow:.2f}")

# Analyze spending by category
category_summary = aggregate_by_category(transactions)
print("Top Spending Categories:")
expense_categories = category_summary[
    category_summary['Type'] == 'Expense'
].sort_values('Amount', ascending=False)

for i, row in enumerate(expense_categories.head(5).itertuples(), 1):
    print(f"{i}. {row.Category}: ${row.Amount:.2f}")

# Calculate cash allocation
cash_allocation = calculate_cash_allocation(transactions)
print(f"Spending: {cash_allocation.get('Spending', 0):.1f}%")
print(f"Saving: {cash_allocation.get('Saving', 0):.1f}%")
print(f"Investing: {cash_allocation.get('Investing', 0):.1f}%")
```

### Advanced Analysis

For more advanced analysis, use the specialized functions:

```python
from cashflow_tracker.core.aggregation import aggregate_by_month, aggregate_by_producer
from cashflow_tracker.core.calculation import calculate_savings_rate
import pandas as pd

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Analyze monthly trends
monthly_data = aggregate_by_month(transactions)
print("Monthly Trends:")
for _, row in monthly_data.iterrows():
    print(f"{row['Month']}: {row['Type']} - ${row['Amount']:.2f}")

# Analyze spending by vendor/producer
producer_data = aggregate_by_producer(transactions)
expense_producers = producer_data[
    producer_data['Type'] == 'Expense'
].sort_values('Amount', ascending=False)

print("\nTop Vendors by Spending:")
for i, row in enumerate(expense_producers.head(5).itertuples(), 1):
    print(f"{i}. {row.Producer}: ${row.Amount:.2f}")

# Calculate savings rate
income = transactions[transactions['Type'] == 'Income']['Amount'].sum()
regular_expenses = transactions[
    (transactions['Type'] == 'Expense') & 
    ~transactions['Category'].isin(['Savings', 'Investments'])
]['Amount'].sum()

savings_rate = calculate_savings_rate(income, regular_expenses)
print(f"\nSavings Rate: {savings_rate:.1f}%")
```

## Generating Reports and Visualizations

### Excel Reports

To generate a comprehensive Excel report:

```python
from cashflow_tracker.output.excel import (
    create_excel_workbook, populate_transaction_sheet,
    populate_category_sheet, populate_summary_sheet, create_charts
)
from cashflow_tracker.utils.defaults import create_default_categories
from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category, aggregate_by_month
)
from cashflow_tracker.core.calculation import calculate_cash_allocation
import pandas as pd

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Create workbook
wb = create_excel_workbook()

# Populate transaction sheet
populate_transaction_sheet(wb, transactions)

# Create and populate category sheet
categories = create_default_categories()
populate_category_sheet(wb, categories)

# Calculate summaries
type_summary = aggregate_by_type(transactions)
category_summary = aggregate_by_category(transactions)
monthly_summary = aggregate_by_month(transactions)
cash_allocation = calculate_cash_allocation(transactions)

# Populate summary sheet
populate_summary_sheet(wb, type_summary, category_summary, cash_allocation)

# Create charts
create_charts(wb, category_summary, cash_allocation, monthly_summary)

# Save workbook
wb.save("financial_report.xlsx")
```

### Visualizations

To generate visualizations:

```python
from cashflow_tracker.output.visualisations import (
    create_matplotlib_charts, create_advanced_visualizations
)
from cashflow_tracker.utils.defaults import create_default_categories
import pandas as pd
import os

# Create output directory
output_dir = "financial_charts"
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Generate basic charts
create_matplotlib_charts(transactions, output_dir)

# Generate advanced visualizations
categories = create_default_categories()
create_advanced_visualizations(transactions, output_dir, categories)

print(f"Charts generated in '{output_dir}' directory")
```

## Customization

### Adding Custom Categories

To customize the category system:

```python
from cashflow_tracker.utils.defaults import create_default_categories
import pandas as pd

# Get default categories
categories = create_default_categories()

# Add a new category
new_row = pd.DataFrame({
    'Main Category': ['Education'],
    'Subcategory': [['Tuition', 'Books', 'Courses']],
    'Description': ['Educational expenses'],
    'Budget Amount': [300.0]
})

categories = pd.concat([categories, new_row], ignore_index=True)

# Save to CSV
categories.to_csv("custom_categories.csv", index=False)
```

### Creating Custom Visualizations

To create custom visualizations:

```python
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

# Load transactions
transactions = pd.read_csv("my_transactions.csv")

# Convert date to datetime
transactions['Date'] = pd.to_datetime(transactions['Date'])

# Extract year-month
transactions['Month'] = transactions['Date'].dt.strftime('%Y-%m')

# Create a custom visualization
plt.figure(figsize=(12, 6))
expense_data = transactions[transactions['Type'] == 'Expense']
monthly_spending = expense_data.groupby(['Month', 'Category'])['Amount'].sum().reset_index()

# Create a pivot table for better visualization
pivot_data = monthly_spending.pivot_table(
    index='Month',
    columns='Category',
    values='Amount',
    fill_value=0
)

# Create stacked bar chart
pivot_data.plot(kind='bar', stacked=True, figsize=(12, 6))
plt.title('Monthly Spending by Category', fontsize=16)
plt.xlabel('Month')
plt.ylabel('Amount ($)')
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig('custom_monthly_spending.png', dpi=300)
```

## Tips and Best Practices

### Data Organization

1. **Consistent Categorization**: Use consistent categories for all transactions to get accurate insights.

2. **Regular Updates**: Update your transactions regularly (weekly or bi-weekly) to maintain an accurate financial picture.

3. **Review Categorization**: Periodically review automatic categorization for accuracy and adjust as needed.

4. **Split Multi-Category Transactions**: For shopping trips with multiple categories (e.g., groceries and household items), consider splitting the transaction for better accuracy.

### Performance Tips

1. **CSV vs. Excel**: For large datasets, CSV files load faster than Excel files.

2. **Pre-processing**: Pre-process and clean your data before analysis if you have many transactions.

3. **Batch Processing**: Process transactions in batches if you have years of historical data.

### Financial Management

1. **Budget Comparison**: Regularly compare actual spending against your budget to stay on track.

2. **Track Trends**: Watch for spending trends over time to identify areas for improvement.

3. **Regular Reports**: Generate monthly or quarterly reports to review your financial health.

4. **Annual Review**: Perform an annual financial review to set budgets and goals for the next year.

## Troubleshooting

### Common Issues

1. **Date Format Errors**: Ensure dates are in YYYY-MM-DD format or a format recognizable by pandas.

2. **Missing Categories**: If transactions aren't categorized correctly, add more keywords to the category rules.

3. **Excel Formatting Issues**: If Excel charts aren't displaying correctly, check that you have the latest version of openpyxl installed.

4. **Import Errors**: For bank statements, make sure the column names match the expected format or provide column mappings.

### Getting Help

If you encounter issues:

1. Check the documentation in the `docs/` directory.
2. Look at the example scripts in the `examples/` directory.
3. Run the unit tests to check for system integrity.
4. Post an issue on the GitHub repository for additional help.