"""
Radar chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import os
from core.schema import TransactionSchema, CategorySchema


def generate_radar_chart(expense_data: pd.DataFrame, output_dir: str = '.',
                         budget_data: pd.DataFrame = None) -> pd.DataFrame:
    """
    Generate a radar chart comparing actual spending with budget by category.
    If budget_data is not provided, it will just show the expense distribution.

    Args:
        expense_data: DataFrame with expense data
        output_dir: Directory to save images
        budget_data: Optional DataFrame with budget information

    Returns:
        DataFrame with comparison data
    """
    # Aggregate expenses by category
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Sort categories by amount for better visualization
    category_totals = category_totals.sort_values(TransactionSchema.AMOUNT, ascending=False)

    # If we have too many categories, limit to top N for readability
    max_categories = 10
    if len(category_totals) > max_categories:
        top_categories = category_totals.head(max_categories - 1)
        other_amount = category_totals.iloc[max_categories - 1:][TransactionSchema.AMOUNT].sum()
        other_row = pd.DataFrame({
            TransactionSchema.CATEGORY: ['Other'],
            TransactionSchema.AMOUNT: [other_amount]
        })
        category_totals = pd.concat([top_categories, other_row], ignore_index=True)

    # Set up figure with polar projection (for radar chart)
    fig = plt.figure(figsize=(10, 10), facecolor='white')
    ax = fig.add_subplot(111, polar=True)

    # Get category names and values
    categories = category_totals[TransactionSchema.CATEGORY].tolist()
    values = category_totals[TransactionSchema.AMOUNT].tolist()

    # Number of categories
    N = len(categories)

    # Set angles for each category
    angles = np.linspace(0, 2 * np.pi, N, endpoint=False).tolist()

    # Make the plot circular by repeating the first value
    values.append(values[0])
    angles.append(angles[0])

    # Get budget values if budget data is provided and in the correct format
    if budget_data is not None and isinstance(budget_data, pd.DataFrame):
        if CategorySchema.MAIN_CATEGORY in budget_data.columns and CategorySchema.BUDGET in budget_data.columns:
            budget_values = []
            for category in categories:
                budget_row = budget_data[budget_data[CategorySchema.MAIN_CATEGORY] == category]
                if not budget_row.empty:
                    budget_values.append(budget_row[CategorySchema.BUDGET].iloc[0])
                else:
                    budget_values.append(0)  # No budget defined

            # Make the plot circular by repeating the first value
            budget_values.append(budget_values[0])

            # Plot budget values
            ax.plot(angles, budget_values, linewidth=2, linestyle='--', color='#55a868', label='Budget')
            ax.fill(angles, budget_values, alpha=0.1, color='#55a868')

    # Plot actual spending values
    ax.plot(angles, values, linewidth=2, linestyle='-', color='#4c72b0', label='Actual')
    ax.fill(angles, values, alpha=0.25, color='#4c72b0')

    # Add category labels
    plt.xticks(angles[:-1], categories, fontsize=10)

    # Add radial labels (amount markers)
    max_value = max(values)

    if 'budget_values' in locals():
        max_value = max(max_value, max(budget_values))

    # Round max value up to nearest 'nice' number for better tick marks
    if max_value < 100:
        tick_step = 20
    elif max_value < 500:
        tick_step = 100
    elif max_value < 1000:
        tick_step = 200
    elif max_value < 5000:
        tick_step = 1000
    else:
        # Round up to nearest 1000
        tick_step = 1000 * (int(max_value / 1000) + 1)

    # Set yticks
    plt.yticks(
        np.arange(0, max_value * 1.1, tick_step),
        [f'${int(x):,}' for x in np.arange(0, max_value * 1.1, tick_step)],
        fontsize=8
    )
    plt.ylim(0, max_value * 1.1)

    # Add title and legend
    plt.title(
        'Expense Categories Radar Chart',
        fontweight='bold',
        fontsize=14,
        y=1.1
    )

    if 'budget_values' in locals():
        plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))

    # Add subtle grid with lighter color
    ax.grid(True, color='lightgray', alpha=0.7)

    # Save the figure
    plt.tight_layout()
    plt.savefig(
        os.path.join(output_dir, 'category_radar.png'),
        dpi=300,
        bbox_inches='tight'
    )
    plt.close()

    return category_totals