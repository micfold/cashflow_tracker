"""
Monthly category proportion chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from core.schema import TransactionSchema
from .constants import PROFESSIONAL_COLORS


def generate_monthly_category_proportion(expense_data: pd.DataFrame, output_dir: str = '.') -> pd.DataFrame:
    """
    Generate a stacked bar chart showing monthly spending by category proportion.
    Each month's total spending is represented as a full bar, with categories as proportions.

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        DataFrame with monthly category proportion data
    """
    # Check if expense_data has a Month column
    if 'Month' not in expense_data.columns:
        expense_data = expense_data.copy()
        expense_data['Month'] = pd.to_datetime(expense_data[TransactionSchema.DATE]).dt.strftime('%Y-%m')

    # Aggregate by month and category
    monthly_category = expense_data.groupby(['Month', TransactionSchema.CATEGORY])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Calculate the total amount per month
    monthly_total = expense_data.groupby('Month')[TransactionSchema.AMOUNT].sum().reset_index()
    monthly_total = monthly_total.rename(columns={TransactionSchema.AMOUNT: 'Total'})

    # Merge with totals
    monthly_category = pd.merge(monthly_category, monthly_total, on='Month')

    # Calculate percentage of total for each category
    monthly_category['Percentage'] = monthly_category[TransactionSchema.AMOUNT] / monthly_category['Total'] * 100

    # Pivot data for plotting
    pivot_data = pd.pivot_table(
        monthly_category,
        index='Month',
        columns=TransactionSchema.CATEGORY,
        values='Percentage',
        aggfunc='sum'
    ).fillna(0)

    # Sort by month
    pivot_data = pivot_data.sort_index()

    # If not enough months, return early
    if len(pivot_data) <= 1:
        print("Warning: Not enough monthly data for a proportion chart")
        return monthly_category

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')

    # Get categories
    categories = pivot_data.columns

    # Create stacked bar chart
    bottom = np.zeros(len(pivot_data))

    for i, category in enumerate(categories):
        values = pivot_data[category].values
        ax.bar(
            pivot_data.index,
            values,
            bottom=bottom,
            label=category,
            color=PROFESSIONAL_COLORS[i % len(PROFESSIONAL_COLORS)],
            width=0.7,
            edgecolor='white',
            linewidth=0.7
        )
        # Update bottom for next stack
        bottom += values

    # Add title and labels
    ax.set_title('Monthly Expenditure Breakdown', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Month', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Percentage of Monthly Total (%)', fontweight='bold', fontsize=12, labelpad=10)

    # Add legend
    ax.legend(
        title='Categories',
        loc='upper left',
        bbox_to_anchor=(1, 1),
        frameon=False
    )

    # Format y-axis as percentage
    ax.set_ylim(0, 100)
    ax.set_yticks(range(0, 101, 10))
    ax.set_yticklabels([f'{x}%' for x in range(0, 101, 10)])

    # Rotate x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add subtle grid on y-axis only
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add data labels for significant segments (>10%)
    for i, category in enumerate(categories):
        values = pivot_data[category].values
        prev_bottom = bottom - values
        for j, (value, start) in enumerate(zip(values, prev_bottom)):
            if value > 10:  # Only label segments larger than 10%
                # Position text in the middle of each segment
                y_pos = start + value / 2
                ax.text(
                    j, y_pos, f'{value:.1f}%',
                    ha='center', va='center',
                    fontsize=9, fontweight='bold',
                    color='white'
                )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'monthly_category_proportion.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return monthly_category