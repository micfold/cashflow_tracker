"""
Top vendors chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter, PROFESSIONAL_COLORS


def generate_top_vendors_chart(expense_data: pd.DataFrame, output_dir: str = '.', top_n: int = 10) -> pd.Series:
    """
    Generate a horizontal bar chart showing top vendors by spending

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images
        top_n: Number of top vendors to show

    Returns:
        Series containing top vendor data
    """
    # Calculate totals by producer
    producer_totals = expense_data.groupby(TransactionSchema.PRODUCER)[
        TransactionSchema.AMOUNT].sum().sort_values(ascending=False)

    # Get top N producers
    top_producers = producer_totals.head(top_n)

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

    # Create horizontal bar chart for better readability of vendor names
    bars = ax.barh(
        top_producers.index[::-1],  # Reverse for descending order
        top_producers.values[::-1],
        color=PROFESSIONAL_COLORS[:len(top_producers)],
        height=0.7,
        edgecolor='white',
        linewidth=0.7
    )

    # Add title and labels with proper styling
    ax.set_title('Top Vendors by Expenditure', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Total Amount', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Vendor', fontweight='bold', fontsize=12, labelpad=10)

    # Format x-axis as currency
    ax.xaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add subtle grid on x-axis only
    ax.grid(axis='x', linestyle='--', alpha=0.3)

    # Add data labels inside bars
    for bar in bars:
        width = bar.get_width()
        label_position = width * 0.95
        ax.text(
            label_position,
            bar.get_y() + bar.get_height() / 2,
            f'${width:,.0f}',
            va='center',
            ha='right',
            fontsize=9,
            color='white',
            fontweight='bold'
        )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_producers_bar.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return top_producers