"""
Cash allocation chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from core.schema import TransactionSchema


def generate_cash_allocation_chart(expense_data: pd.DataFrame, output_dir: str = '.') -> dict:
    """
    Generate a pie chart showing cash allocation (spending/saving/investing)

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        Dictionary with allocation data
    """
    # Calculate the allocations
    spending = expense_data[~expense_data[TransactionSchema.CATEGORY].isin(
        ['Savings', 'Investments'])][TransactionSchema.AMOUNT].sum()

    saving = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Savings'][
        TransactionSchema.AMOUNT].sum()

    investing = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Investments'][
        TransactionSchema.AMOUNT].sum()

    # Create allocation data
    allocation_data = [spending, saving, investing]
    allocation_labels = ['Spending', 'Saving', 'Investing']
    allocation_colors = ['#c44e52', '#55a868', '#4c72b0']  # red, green, blue

    plt.figure(figsize=(10, 8), facecolor='white')

    # Create the pie chart with better styling
    wedges, texts, autotexts = plt.pie(
        allocation_data,
        labels=None,  # We'll use a legend instead
        autopct='%1.1f%%',
        startangle=90,
        colors=allocation_colors,
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        pctdistance=0.85
    )

    # Style the percentage text
    for autotext in autotexts:
        autotext.set_fontweight('bold')

    # Add a white circle at the center for donut chart
    centre_circle = plt.Circle((0, 0), 0.5, fc='white')
    plt.gca().add_artist(centre_circle)

    # Equal aspect ratio ensures that pie is drawn as a circle
    plt.axis('equal')

    # Add title with proper styling
    plt.title('Fund Allocation Analysis', fontweight='bold', fontsize=14, pad=15)

    # Add a legend
    plt.legend(
        allocation_labels,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cash_allocation_pie.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Return allocation data as dictionary
    return {
        'Spending': spending,
        'Saving': saving,
        'Investing': investing
    }