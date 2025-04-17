"""
Cashflow Tracker package

A comprehensive system for tracking cash flow, categorizing transactions,
and visualizing financial data.
"""

__version__ = "0.1.0"

# Import core components for easy access
from cashflow_tracker.core.schema import TransactionSchema, CategorySchema
from cashflow_tracker.core.ingestion import (
    ingest_csv, ingest_excel, create_manual_transaction
)
from cashflow_tracker.core.processing import (
    clean_transaction_data, categorize_transaction,
    categorize_all_transactions, extract_producer,
    extract_all_producers
)
from cashflow_tracker.core.aggregation import (
    aggregate_by_type, aggregate_by_category,
    aggregate_by_producer, aggregate_by_month
)
from cashflow_tracker.core.calculation import (
    calculate_net_cashflow, calculate_cash_allocation,
    calculate_budget_comparison
)
from cashflow_tracker.output.excel import (
    create_excel_workbook, populate_transaction_sheet,
    populate_category_sheet, populate_summary_sheet,
    create_charts
)
from cashflow_tracker.output.visualisations import create_matplotlib_charts
from cashflow_tracker.utils.defaults import (
    create_default_categories, create_category_rules,
    create_producer_patterns, generate_sample_transactions
)