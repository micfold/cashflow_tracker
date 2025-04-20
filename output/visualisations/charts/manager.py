"""
Main chart management functions for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import os
from typing import Optional, Any
from typing import List
from core.schema import TransactionSchema

# Import constants
from .constants import PROFESSIONAL_COLORS, money_formatter

# Import individual chart functions
from .category_spending_chart import generate_spending_by_category_chart
from .cash_allocation_chart import generate_cash_allocation_chart
from .monthly_comparison_chart import generate_monthly_comparison_chart
from .net_cashflow_chart import generate_net_cashflow_chart
from .category_heatmap import generate_category_stacked
from .top_vendors_chart import generate_top_vendors_chart
from .category_treemap_chart import generate_category_treemap
from .monthly_category_proportion_chart import generate_monthly_category_proportion

# Advanced chart generators
from .daily_spending_chart import generate_daily_spending_chart
from .weekday_spending_chart import generate_weekday_spending_chart
from .budget_comparison_chart import generate_budget_comparison_chart
from .cumulative_cashflow_chart import generate_cumulative_cashflow_chart

from .sankey_flow_chart import generate_sankey_flow_diagram

# Import other chart modules as they're created
# etc.


def set_professional_style():
    """Configure matplotlib for professional/academic visualisations"""
    plt.rcParams.update({
        'font.family': 'serif',
        'font.serif': ['Times New Roman', 'DejaVu Serif', 'Liberation Serif'],
        'font.size': 10,
        'axes.titlesize': 12,
        'axes.labelsize': 10,
        'xtick.labelsize': 9,
        'ytick.labelsize': 9,
        'legend.fontsize': 9,
        'figure.titlesize': 14,
        'figure.figsize': (8, 6),
        'figure.dpi': 300,
        'axes.grid': True,
        'grid.alpha': 0.3,
        'axes.axisbelow': True,
        'axes.spines.top': False,
        'axes.spines.right': False,
    })

    # Use a professional seaborn style
    sns.set_style("whitegrid")

    # Make sure we're using our color palette
    sns.set_palette(PROFESSIONAL_COLORS)

def create_visualisations(transaction_data: pd.DataFrame,
                          output_dir: str = '.',
                          budget_data: Optional[pd.DataFrame] = None,
                          chart_types: Optional[List[str]] = None) -> dict[Any, Any]:
    """
    Create visualisations and save as image files

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images
        budget_data: Optional DataFrame with budget information
        chart_types: Optional list of chart types to generate (generates all if None)
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set professional style
    set_professional_style()

    # Create a copy to avoid modifying the original dataframe
    transaction_data = transaction_data.copy()

    # Filter for expenses
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense'].copy()

    # Add date-related columns
    transaction_data['Month'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.strftime('%Y-%m')
    transaction_data['Day'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.day
    transaction_data['Weekday'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.day_name()
    transaction_data['Date'] = pd.to_datetime(transaction_data[TransactionSchema.DATE])


    # Define all available charts
    all_charts = {
        # Basic charts
        'category_spending': lambda: generate_spending_by_category_chart(expense_data, output_dir),
        'cash_allocation': lambda: generate_cash_allocation_chart(expense_data, output_dir),
        'monthly_comparison': lambda: generate_monthly_comparison_chart(transaction_data, output_dir),
        'net_cashflow': lambda: generate_net_cashflow_chart(transaction_data, output_dir),
        'category_heatmap': lambda: generate_category_stacked(expense_data, transaction_data, output_dir),
        'top_vendors': lambda: generate_top_vendors_chart(expense_data, output_dir),

        # Advanced charts
        'daily_spending': lambda: generate_daily_spending_chart(expense_data, output_dir),
        'weekday_spending': lambda: generate_weekday_spending_chart(expense_data, output_dir),
        'cumulative_cashflow': lambda: generate_cumulative_cashflow_chart(transaction_data, output_dir),

        'monthly_category_proportion': lambda: generate_monthly_category_proportion(expense_data, output_dir),
        'category_treemap': lambda: generate_category_treemap(expense_data, output_dir),
        'sankey_flow': lambda: generate_sankey_flow_diagram(expense_data, output_dir),

        # Add more charts as they are implemented,
        # etc.
    }

    # Add budget-dependent charts if budget data is provided
    if budget_data is not None:
        all_charts['budget_comparison'] = lambda: generate_budget_comparison_chart(expense_data, budget_data, output_dir)

    # Determine which charts to generate
    charts_to_generate = chart_types if chart_types else all_charts.keys()

    # Generate selected charts
    results = {}

    # Generate selected charts
    for chart_type in charts_to_generate:
        if chart_type in all_charts:
            print(f"Generating {chart_type} chart...")
            all_charts[chart_type]()
        else:
            print(f"Warning: Chart type '{chart_type}' not recognized")

    # Handle dependent charts
    if 'monthly_comparison' in results:
        monthly_pivot = results.get('monthly_comparison')

        if 'net_cashflow' in charts_to_generate or chart_types is None:
            print("Generating net cashflow chart...")
            results['net_cashflow'] = generate_net_cashflow_chart(transaction_data, output_dir)

        if 'category_heatmap' in charts_to_generate or chart_types is None:
            print("Generating category heatmap...")
            results['category_heatmap'] = generate_category_stacked(expense_data, monthly_pivot, output_dir)

    return results