"""
Budget comparison chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from matplotlib.ticker import FuncFormatter
from pandas import DataFrame

from core.schema import TransactionSchema
from .constants import money_formatter


def generate_budget_comparison_chart(expense_data: pd.DataFrame, budget_data: pd.DataFrame,
                                     output_dir: str = '.') -> DataFrame | None:
    """
    Generate a bar chart comparing actual spending to budget by category

    Args:
        expense_data: DataFrame with expense data
        budget_data: DataFrame with budget information
        output_dir: Directory to save images

    Returns:
        DataFrame with budget comparison data
    """
    if budget_data is None or budget_data.empty:
        return None

    # Aggregate expenses by category
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Merge with budget data
    budget_compare = pd.merge(
        category_totals,
        budget_data,
        left_on=TransactionSchema.CATEGORY,
        right_on='Main Category',
        how='left'
    )

    # Remove categories with no budget
    budget_compare = budget_compare.dropna(subset=['Budget Amount'])

    if budget_compare.empty:
        return None

    # Create figure
    fig, ax = plt.subplots(figsize=(14, 8), facecolor='white')

    # Sort by budget used percentage for better visualization
    if len(budget_compare) > 0:
        budget_compare['Budget Used (%)'] = (budget_compare[TransactionSchema.AMOUNT] /
                                             budget_compare['Budget Amount'] * 100)
        budget_compare = budget_compare.sort_values('Budget Used (%)', ascending=False)

    # Create bar positions
    categories = budget_compare[TransactionSchema.CATEGORY]
    x_pos = np.arange(len(categories))
    width = 0.35

    # Create bars with improved styling
    actual_bars = ax.bar(
        x_pos - width / 2,
        budget_compare[TransactionSchema.AMOUNT],
        width,
        label='Actual',
        color='#4c72b0',
        edgecolor='white',
        linewidth=1
    )

    budget_bars = ax.bar(
        x_pos + width / 2,
        budget_compare['Budget Amount'],
        width,
        label='Budget',
        color='#ccb974',
        edgecolor='white',
        linewidth=1
    )

    # Add proper styling
    ax.set_xlabel('Category', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_ylabel('Amount', fontweight='bold', fontsize=12, labelpad=10)
    ax.set_title('Budget vs. Actual Expenditure Analysis', fontweight='bold', fontsize=14, pad=15)
    ax.set_xticks(x_pos)
    ax.set_xticklabels(categories, rotation=45, ha='right')

    # Format y-axis as currency
    ax.yaxis.set_major_formatter(FuncFormatter(money_formatter))

    # Add legend with better styling
    ax.legend(
        frameon=True,
        framealpha=0.9,
        edgecolor='lightgray',
        loc='best'
    )

    # Add subtle grid
    ax.grid(axis='y', linestyle='--', alpha=0.3)

    # Add percentage labels above bars
    for i, (actual, budget) in enumerate(zip(budget_compare[TransactionSchema.AMOUNT],
                                             budget_compare['Budget Amount'])):
        percentage = (actual / budget * 100) if budget > 0 else 0
        color = '#c44e52' if percentage > 100 else '#55a868'

        ax.text(
            x_pos[i],
            max(actual, budget) * 1.05,
            f'{percentage:.1f}%',
            ha='center',
            va='bottom',
            fontsize=9,
            fontweight='bold',
            color=color
        )

    # Save the figure
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'budget_vs_actual.png'), dpi=300, bbox_inches='tight')
    plt.close()

    return budget_compare