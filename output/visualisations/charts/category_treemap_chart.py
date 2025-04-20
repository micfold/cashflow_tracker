"""
Category treemap chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import squarify
import pandas as pd
import os
from core.schema import TransactionSchema
from .constants import PROFESSIONAL_COLORS


def generate_category_treemap(expense_data: pd.DataFrame, output_dir: str = '.') -> pd.DataFrame:
    """
    Generate a treemap showing proportion of spending by category

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images

    Returns:
        DataFrame with category data
    """
    # Aggregate by category
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[TransactionSchema.AMOUNT].sum()

    # Sort by value for better visualization
    category_totals = category_totals.sort_values(ascending=False)

    # Create figure
    plt.figure(figsize=(12, 8), facecolor='white')

    # Create treemap
    squarify.plot(
        sizes=category_totals.values,
        label=[f"{cat}\n${amt:,.0f}" for cat, amt in zip(category_totals.index, category_totals.values)],
        alpha=0.8,
        color=PROFESSIONAL_COLORS[:len(category_totals)],
        pad=True,
        text_kwargs={'fontsize': 12, 'fontweight': 'bold'}
    )

    # Add title
    plt.title('Expenditure Distribution by Category', fontweight='bold', fontsize=14, pad=15)
    plt.axis('off')  # Turn off axis

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_treemap.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return category_totals