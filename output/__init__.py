"""
Output generation modules for the Cashflow Tracker

This package contains modules for generating outputs from the Cashflow Tracker,
including Excel workbooks, charts, and visualizations.
"""

# Import key functions for easier access
from cashflow_tracker.output.excel import (
    create_excel_workbook,
    populate_transaction_sheet,
    populate_category_sheet,
    populate_summary_sheet,
    create_charts
)

from cashflow_tracker.output.visualisations import (
    create_matplotlib_charts,
    create_advanced_visualizations
)

from cashflow_tracker.output.charts import (
    generate_pie_chart_base64,
    generate_bar_chart_base64,
    generate_line_chart_base64,
    generate_spending_by_category_chart,
    generate_cash_allocation_chart
)