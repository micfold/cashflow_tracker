# Cashflow Tracker

A comprehensive Python application for tracking cashflow, categorizing transactions, and visualizing financial data.

## Overview

Cashflow Tracker is a powerful tool designed to help you manage your personal finances through:

- **Automated transaction categorization** based on description and vendor
- **Cash allocation analysis** showing spending, saving, and investing distribution
- **Budget comparison** to track spending against your financial goals
- **Beautiful visualizations** including pie charts, bar charts, and trend analysis
- **Excel report generation** for complete financial overview

## Features

- 📊 **Transaction Management**: Record and organize all financial transactions
- 🏷️ **Smart Categorization**: Automatically classify transactions into categories
- 📈 **Financial Analysis**: Calculate key metrics like net cashflow and savings rate
- 📝 **Budget Tracking**: Compare actual spending with budget targets
- 📱 **Vendor Analysis**: Track spending by vendor/producer
- 📷 **Data Visualization**: Generate informative charts and graphs
- 📑 **Reporting**: Export formatted Excel workbooks with interactive charts

## Installation

### Prerequisites

- Python 3.8 or higher
- pip package manager

### Installation Steps

```bash
# Install required packages
pip install pandas openpyxl matplotlib seaborn numpy

# Clone the repository
git clone https://github.com/micfold/cashflow-tracker.git
cd cashflow-tracker

# Install the package in development mode
pip install -e .
```

## Quick Start

### Command Line Usage

```bash
# Generate a sample cashflow tracker
cashflow-tracker --sample --output my_finances.xlsx

# Process your own transaction data
cashflow-tracker --input my_transactions.csv --output my_finances.xlsx

# Generate additional charts and visualizations
cashflow-tracker --input my_transactions.csv --charts
```

### Python Script Usage

```python
from cashflow_tracker.utils.defaults import generate_sample_transactions
from cashflow_tracker.core.processing import clean_transaction_data
from cashflow_tracker.core.aggregation import aggregate_by_type
from cashflow_tracker.output.excel import create_excel_workbook, populate_transaction_sheet

# Generate sample data
transactions = generate_sample_transactions(num_transactions=100)
transactions = clean_transaction_data(transactions)

# Create an Excel report
wb = create_excel_workbook()
populate_transaction_sheet(wb, transactions)
wb.save("my_finances.xlsx")
```

## Input Data Format

The Cashflow Tracker accepts transaction data in CSV format with the following columns:

```
Date,Description,Amount,Type,Category,Subcategory,Producer/Vendor,Payment Method,Notes
2025-04-01,Monthly Salary,3500.00,Income,Income,Salary,Acme Corporation,Direct Deposit,Regular monthly salary
2025-04-03,Apartment Rent,1200.00,Expense,Housing,Rent/Mortgage,Landlord,Bank Transfer,Monthly rent payment
```

At minimum, you need to provide the Date, Description, and Amount columns. The system will attempt to infer missing information.

## Documentation

For detailed documentation, see the `docs/` directory:

- [Usage Guide](docs/usage.md): Detailed instructions on using the system
- [Examples](docs/examples.md): Code examples for common tasks
- [Architecture](docs/architecture.md): System architecture and design

## Example Scripts

The `examples/` directory contains several example scripts:

- `sample_data_example.py`: Working with sample data
- `bank_statement_example.py`: Processing bank statements
- `manual_entry_example.py`: Manual transaction entry
- `visualization_example.py`: Creating advanced visualizations

## Project Structure

```
cashflow_tracker/
│
├── cashflow_tracker/            # Main package directory
│   ├── core/                    # Core functionality
│   │   ├── schema.py            # Data schemas
│   │   ├── ingestion.py         # Data ingestion
│   │   ├── processing.py        # Data processing
│   │   ├── aggregation.py       # Data aggregation
│   │   └── calculation.py       # Financial calculations
│   │
│   ├── output/                  # Output generation
│   │   ├── excel.py             # Excel generation
│   │   ├── charts.py            # Chart generation
│   │   └── visualizations.py    # Matplotlib visualizations
│   │
│   └── utils/                   # Utility functions
│       ├── defaults.py          # Default values
│       └── helpers.py           # Helper functions
│
├── examples/                    # Example scripts
├── tests/                       # Unit tests
└── docs/                        # Documentation
```

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

---

Created with ❤️ for better financial management. Inspired by the need for a simple yet powerful cashflow tracking system.