"""
Weekday spending chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter, PROFESSIONAL_COLORS


def generate_weekday_spending_chart(expense_data: pd.DataFrame, output_dir: str = '.') -> pd.Series:
    """
    Generate a bar chart showing spending by day of week

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        Series containing weekday spending data
    """
    # Ensure expense_data has the 'Weekday' column
    if 'Weekday' not in expense_data.columns:
        expense_data = expense_data.copy()
        expense_data['Weekday'] = pd.to_datetime(expense_data[TransactionSchema.DATE]).dt.day_name()

    # Aggregate by day of week
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_spending = expense_data.groupby('Weekday')[TransactionSchema.AMOUNT].sum()
    weekday_spending = weekday_spending.reindex(weekday_order)

    # Create figure
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

    # Create bar chart with improved styling
    bars = ax.bar(
        weekday_order,
        weekday_spending,
        color=PROFESSIONAL_COLORS[:7],
        width=0.7,
        edgecolor='white',
        linewidth=1
    )

    # Add a curved line connecting the tops of bars
    ax.plot(
        weekday_order,
        weekday_spending,
        color='#4c72b0',
        linewidth=2,
        marker='o',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='#4c72b0',
        markeredgewidth=1.5,
        alpha=0.7
    )

    # Add title and labels with proper styling
    ax.set_title('Weekly Expenditure Pattern Analysis', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Day of Week', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Total Expenditure', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add data labels on top of bars
    for bar in bars:
        height = bar.get_height()
        ax.text(
            bar.get_x() + bar.get_width() / 2.,
            height * 1.01,
            f'${height:,.0f}',
            ha='center',
            va='bottom',
            fontsize=9
        )

    # Add subtle grid
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Highlight weekends with background shading
    weekend_indices = [weekday_order.index('Saturday'), weekday_order.index('Sunday')]
    for idx in weekend_indices:
        ax.axvspan(
            idx - 0.4,
            idx + 0.4,
            color='#f2f2f2'
        )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spending_by_weekday.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return weekday_spending