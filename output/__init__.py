"""
Output generation modules for the Cashflow Tracker

This package contains modules for generating outputs from the Cashflow Tracker,
including Excel workbooks, charts, and visualisations.
"""

# Import key functions for easier access
from output.excel import (
    create_excel_workbook,
    populate_transaction_sheet,
    populate_category_sheet,
    populate_summary_sheet,
    create_charts
)

from output.visualisations import create_visualisations