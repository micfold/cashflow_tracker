"""
Category spending stacked bar chart generation for the Cashflow Tracker
"""
from typing import Any

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from core.schema import TransactionSchema
from .constants import PROFESSIONAL_COLORS, money_formatter
from matplotlib.ticker import FuncFormatter


def generate_category_stacked(expense_data: pd.DataFrame, transaction_data: pd.DataFrame,
                              output_dir: str = '.') -> pd.DataFrame | None:
    """
    Generate a stacked bar chart showing category spending by month
    (Formerly a heatmap, changed to stacked bar for better readability)

    Args:
        expense_data: DataFrame with expense data
        transaction_data: DataFrame with transaction data (for month reference)
        output_dir: Directory to save images

    Returns:
        DataFrame with category pivot data
    """
    # Check if transaction_data has a Month column
    if 'Month' not in transaction_data.columns:
        print("Warning: Cannot create category chart - 'Month' column not found")
        return None

    # Check if expense_data has a Month column and add it if not
    if 'Month' not in expense_data.columns:
        expense_data = expense_data.copy()
        expense_data['Month'] = pd.to_datetime(expense_data[TransactionSchema.DATE]).dt.strftime('%Y-%m')

    # Create monthly pivot from transaction_data for reference
    monthly_pivot = None
    if 'Month' in transaction_data.columns:
        monthly_data = transaction_data.groupby(['Month', TransactionSchema.TYPE])[
            TransactionSchema.AMOUNT].sum().reset_index()
        monthly_pivot = pd.pivot_table(
            monthly_data,
            index='Month',
            columns=TransactionSchema.TYPE,
            values=TransactionSchema.AMOUNT,
            aggfunc='sum'
        ).fillna(0)

    # Check if we have enough data for a chart
    if monthly_pivot is None or len(monthly_pivot) <= 1:
        print("Warning: Not enough monthly data for a category chart")
        return None

    # Aggregate expenses by category and month
    category_monthly = expense_data.groupby(['Month', TransactionSchema.CATEGORY])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Pivot to get categories as columns and months as rows
    category_pivot = pd.pivot_table(
        category_monthly,
        index='Month',
        columns=TransactionSchema.CATEGORY,
        values=TransactionSchema.AMOUNT,
        aggfunc='sum'
    ).fillna(0)

    # Sort by month
    category_pivot = category_pivot.sort_index()

    # Create figure with good size for time series
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')

    # Get a list of categories (columns)
    categories = category_pivot.columns

    # Create a numpy array for the bottom positions of each stack
    bottoms = np.zeros(len(category_pivot))

    # Plot each category as a stacked bar
    for i, category in enumerate(categories):
        values = category_pivot[category].values
        color_idx = i % len(PROFESSIONAL_COLORS)  # cycle through colors if more categories than colors

        bars = ax.bar(
            category_pivot.index,
            values,
            bottom=bottoms,
            label=category,
            color=PROFESSIONAL_COLORS[color_idx],
            width=0.7,
            edgecolor='white',
            linewidth=0.5
        )

        # Add data labels to bars that are large enough
        for j, (value, bottom) in enumerate(zip(values, bottoms)):
            if value > category_pivot.values.sum() * 0.03:  # Only label if > 3% of total spending
                # Position text in middle of segment
                ax.text(
                    j,
                    bottom + value/2,
                    f'${value:,.0f}',
                    ha='center',
                    va='center',
                    fontsize=8,
                    fontweight='bold',
                    color='white'
                )

        # Update the bottom position for the next category
        bottoms += values

    # Add proper styling
    ax.set_title('Monthly Expenditure by Category', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Month', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Amount ($)', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add legend with better positioning
    ax.legend(
        title='Categories',
        loc='upper left',
        bbox_to_anchor=(1, 1),
        frameon=True,
        framealpha=0.9,
        edgecolor='lightgray'
    )

    # Add subtle grid on y-axis only
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Rotate x-axis labels for better readability
    plt.xticks(rotation=45, ha='right')

    # Add total amount on top of each bar
    for i, month in enumerate(category_pivot.index):
        total = category_pivot.iloc[i].sum()
        ax.text(
            i,
            total * 1.02,  # Slightly above the bar
            f'${total:,.0f}',
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
            color='black',
            bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='lightgray', alpha=0.7)
        )

    plt.tight_layout()
    # Use a new filename to avoid overwriting the old heatmap
    plt.savefig(os.path.join(output_dir, 'category_month_stacked.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return category_pivot