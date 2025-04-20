"""
Category spending chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import os
from core.schema import TransactionSchema
from .constants import PROFESSIONAL_COLORS


def generate_spending_by_category_chart(expense_data: pd.DataFrame, output_dir: str = '.') -> pd.Series:
    """
    Generate a pie chart showing spending by category

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        Series containing category totals
    """
    # Calculate category totals
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[TransactionSchema.AMOUNT].sum()

    # Sort by value for better visualization
    category_totals = category_totals.sort_values(ascending=False)

    plt.figure(figsize=(10, 8), facecolor='white')

    # Create pie chart with better styling
    wedges, texts, autotexts = plt.pie(
        category_totals,
        labels=None,  # We'll use a legend instead
        autopct='%1.1f%%',
        startangle=90,
        colors=PROFESSIONAL_COLORS[:len(category_totals)],
        wedgeprops={'edgecolor': 'white', 'linewidth': 1.5},
        textprops={'fontsize': 9},
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
    plt.title('Expenditure Distribution by Category', fontweight='bold', fontsize=14, pad=15)

    # Add a legend with category names
    plt.legend(
        category_totals.index,
        loc="center left",
        bbox_to_anchor=(1, 0.5),
        frameon=False,
        title="Categories"
    )

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_spending_pie.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return category_totals