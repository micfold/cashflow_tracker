"""
Net cashflow chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter


def generate_net_cashflow_chart(monthly_pivot: pd.DataFrame, output_dir: str = '.') -> pd.DataFrame:
    """
    Generate a line chart showing net cashflow over time

    Args:
        monthly_pivot: DataFrame with monthly income/expense data
        output_dir: Directory to save images

    Returns:
        DataFrame with net cashflow data
    """
    if 'Income' not in monthly_pivot.columns or 'Expense' not in monthly_pivot.columns:
        return monthly_pivot

    # Calculate net cashflow
    net_cashflow = monthly_pivot.copy()
    net_cashflow['Net'] = net_cashflow['Income'] - net_cashflow['Expense']

    fig, ax = plt.subplots(figsize=(12, 6), facecolor='white')

    # Plot the line with markers and connecting lines
    ax.plot(
        net_cashflow.index,
        net_cashflow['Net'],
        marker='o',
        markersize=6,
        markerfacecolor='white',
        markeredgecolor='#4c72b0',
        markeredgewidth=1.5,
        color='#4c72b0',
        linewidth=2
    )

    # Add reference line at y=0
    ax.axhline(y=0, color='#c44e52', linestyle='-', alpha=0.3, linewidth=1.5)

    # Add title and labels with proper styling
    ax.set_title('Net Cashflow Analysis', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Month', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Net Cashflow', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add subtle grid
    ax.grid(True, linestyle='--', alpha=0.3)

    # Add data labels at each point
    for i, value in enumerate(net_cashflow['Net']):
        ax.annotate(
            f'${value:,.0f}',
            (net_cashflow.index[i], value),
            xytext=(0, 10 if value >= 0 else -25),
            textcoords='offset points',
            ha='center',
            fontsize=8,
            bbox=dict(boxstyle='round,pad=0.3', fc='white', ec='lightgray', alpha=0.7)
        )

    # Highlight positive and negative areas
    ax.fill_between(
        net_cashflow.index,
        net_cashflow['Net'],
        0,
        where=(net_cashflow['Net'] >= 0),
        interpolate=True,
        alpha=0.2,
        color='#55a868',
        label='Surplus'
    )
    ax.fill_between(
        net_cashflow.index,
        net_cashflow['Net'],
        0,
        where=(net_cashflow['Net'] <= 0),
        interpolate=True,
        alpha=0.2,
        color='#c44e52',
        label='Deficit'
    )

    # Improve x-axis labels
    plt.xticks(rotation=45, ha='right')

    # Add legend
    ax.legend(frameon=True, framealpha=0.9, edgecolor='lightgray')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'net_cashflow_line.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return net_cashflow