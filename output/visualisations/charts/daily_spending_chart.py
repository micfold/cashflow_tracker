"""
Daily spending chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter


def generate_daily_spending_chart(expense_data: pd.DataFrame, output_dir: str = '.') -> pd.Series:
    """
    Generate a line chart showing spending by day of month

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        Series containing daily spending data
    """
    # Ensure expense_data has the 'Day' column
    if 'Day' not in expense_data.columns:
        expense_data = expense_data.copy()
        expense_data['Day'] = pd.to_datetime(expense_data[TransactionSchema.DATE]).dt.day

    # Aggregate by day of month
    daily_spending = expense_data.groupby('Day')[TransactionSchema.AMOUNT].sum()

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 6), facecolor='white')

    # Create line plot with area fill instead of bar chart
    days = daily_spending.index
    amounts = daily_spending.values

    # Plot the line with connecting segments and markers
    ax.plot(
        days,
        amounts,
        color='#4c72b0',
        linewidth=2,
        marker='o',
        markersize=5,
        markerfacecolor='white',
        markeredgecolor='#4c72b0',
        markeredgewidth=1.5
    )

    # Add area fill below the line
    ax.fill_between(
        days,
        amounts,
        color='#4c72b0',
        alpha=0.1
    )

    # Add title and labels with proper styling
    ax.set_title('Daily Expenditure Pattern Analysis', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Day of Month', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Total Expenditure', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Improve x-axis
    ax.set_xticks(days)
    ax.set_xlim(0.5, 31.5)  # Adjust for month days

    # Add subtle grid
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add average line
    avg_spend = daily_spending.mean()
    ax.axhline(
        y=avg_spend,
        color='#c44e52',
        linestyle='--',
        linewidth=1.5,
        alpha=0.8
    )

    # Add annotation for average
    ax.text(
        28,
        avg_spend * 1.05,
        f'Daily Average: ${avg_spend:.2f}',
        fontsize=9,
        color='#c44e52',
        fontweight='bold',
        bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='lightgray', alpha=0.7)
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spending_by_day.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return daily_spending