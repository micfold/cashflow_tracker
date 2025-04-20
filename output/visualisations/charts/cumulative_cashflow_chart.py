"""
Cumulative cashflow chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from matplotlib.ticker import FuncFormatter
from core.schema import TransactionSchema
from .constants import money_formatter


def generate_cumulative_cashflow_chart(transaction_data: pd.DataFrame, output_dir: str = '.') -> pd.DataFrame:
    """
    Generate a line chart showing cumulative cashflow over time

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images

    Returns:
        DataFrame with cumulative cashflow data
    """
    # Ensure the data has a Date column
    if 'Date' not in transaction_data.columns:
        transaction_data = transaction_data.copy()
        transaction_data['Date'] = pd.to_datetime(transaction_data[TransactionSchema.DATE])

    # Sort by date
    sorted_data = transaction_data.sort_values('Date')

    # Group by date and type
    daily_data = sorted_data.groupby(['Date', TransactionSchema.TYPE])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Pivot to have Income and Expense columns
    daily_pivot = pd.pivot_table(
        daily_data,
        index='Date',
        columns=TransactionSchema.TYPE,
        values=TransactionSchema.AMOUNT,
        aggfunc='sum'
    ).fillna(0).reset_index()

    # Calculate cumulative sums
    if 'Income' in daily_pivot.columns:
        daily_pivot['Cumulative Income'] = daily_pivot['Income'].cumsum()
    else:
        daily_pivot['Cumulative Income'] = 0
        daily_pivot['Income'] = 0

    if 'Expense' in daily_pivot.columns:
        daily_pivot['Cumulative Expense'] = daily_pivot['Expense'].cumsum()
    else:
        daily_pivot['Cumulative Expense'] = 0
        daily_pivot['Expense'] = 0

    daily_pivot['Net Cashflow'] = daily_pivot['Cumulative Income'] - daily_pivot['Cumulative Expense']

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')

    # Create line plots with improved styling
    ax.plot(
        daily_pivot['Date'],
        daily_pivot['Cumulative Income'],
        label='Cumulative Income',
        linewidth=2,
        color='#55a868'
    )

    ax.plot(
        daily_pivot['Date'],
        daily_pivot['Cumulative Expense'],
        label='Cumulative Expense',
        linewidth=2,
        color='#c44e52'
    )

    ax.plot(
        daily_pivot['Date'],
        daily_pivot['Net Cashflow'],
        label='Net Cashflow',
        linewidth=3,
        color='#4c72b0'
    )

    # Add filled areas with better transparency
    ax.fill_between(
        daily_pivot['Date'],
        daily_pivot['Cumulative Income'],
        alpha=0.15,
        color='#55a868'
    )

    ax.fill_between(
        daily_pivot['Date'],
        daily_pivot['Cumulative Expense'],
        alpha=0.15,
        color='#c44e52'
    )

    # Add proper styling
    ax.set_title('Cumulative Financial Flow Analysis', fontweight='bold', fontsize=14, pad=15)
    ax.set_xlabel('Date', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Amount', fontweight='bold', fontsize=12, labelpad=10)

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add subtle grid
    ax.grid(True, linestyle='--', alpha=0.3)

    # Improve legend
    ax.legend(
        frameon=True,
        framealpha=0.9,
        edgecolor='lightgray',
        loc='best'
    )

    # Add annotations for key points with improved styling
    if len(daily_pivot) > 0:
        max_net = daily_pivot['Net Cashflow'].max()
        max_net_date = daily_pivot.loc[daily_pivot['Net Cashflow'].idxmax(), 'Date']

        min_net = daily_pivot['Net Cashflow'].min()
        min_net_date = daily_pivot.loc[daily_pivot['Net Cashflow'].idxmin(), 'Date']

        # Annotation for maximum
        ax.annotate(
            f'Max: ${max_net:,.2f}',
            xy=(max_net_date, max_net),
            xytext=(10, 10),
            textcoords='offset points',
            arrowprops=dict(
                arrowstyle='->',
                connectionstyle='arc3,rad=.2',
                color='#4c72b0'
            ),
            bbox=dict(
                boxstyle='round,pad=0.3',
                fc='white',
                ec='#4c72b0',
                alpha=0.7
            ),
            fontsize=9
        )

        # Annotation for minimum
        ax.annotate(
            f'Min: ${min_net:,.2f}',
            xy=(min_net_date, min_net),
            xytext=(10, -25),
            textcoords='offset points',
            arrowprops=dict(
                arrowstyle='->',
                connectionstyle='arc3,rad=.2',
                color='#c44e52'
            ),
            bbox=dict(
                boxstyle='round,pad=0.3',
                fc='white',
                ec='#c44e52',
                alpha=0.7
            ),
            fontsize=9
        )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cumulative_cashflow.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return daily_pivot