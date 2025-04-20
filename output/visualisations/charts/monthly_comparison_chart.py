"""
Monthly comparison chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter


def generate_monthly_comparison_chart(transaction_data: pd.DataFrame, output_dir: str = '.') -> pd.DataFrame:
    """
    Generate a bar chart showing monthly income vs expenses

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images

    Returns:
        DataFrame with monthly pivot data
    """
    # Aggregate by month and type
    monthly_data = transaction_data.groupby(['Month', TransactionSchema.TYPE])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Pivot the data for easier plotting
    monthly_pivot = pd.pivot_table(
        monthly_data,
        index='Month',
        columns=TransactionSchema.TYPE,
        values=TransactionSchema.AMOUNT,
        aggfunc='sum'
    ).fillna(0)

    # Sort by month
    monthly_pivot = monthly_pivot.sort_index()

    # Create figure with professional styling
    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

    # Create the bar chart
    monthly_pivot.plot(
        kind='bar',
        ax=ax,
        color=['#c44e52', '#55a868'],  # green for income, red for expense
        width=0.8,
        edgecolor='white',
        linewidth=0.7
    )

    # Add title and labels with proper styling
    ax.set_title('Monthly Income vs Expenses', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Month', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Amount', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Improve legend
    ax.legend(
        title='',
        frameon=True,
        framealpha=0.9,
        edgecolor='lightgray'
    )

    # Improve x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add subtle grid on y-axis only
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add data labels on top of bars
    for container in ax.containers:
        ax.bar_label(container, fmt='${:.0f}', fontsize=8, padding=3)

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'monthly_comparison_bar.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return monthly_pivot