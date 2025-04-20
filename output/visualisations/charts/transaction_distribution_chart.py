"""
Transaction distribution chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from core.schema import TransactionSchema


def generate_transaction_distribution_chart(transaction_data: pd.DataFrame, output_dir: str = '.') -> dict:
    """
    Generate histograms showing the distribution of transaction amounts

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images

    Returns:
        Dictionary with distribution statistics
    """
    # Create figure
    plt.figure(figsize=(12, 6), facecolor='white')

    # Create two subplots with improved styling
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 6), facecolor='white')

    # Split data by type
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']
    income_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Income']

    # Plot for expenses with KDE
    sns.histplot(
        expense_data[TransactionSchema.AMOUNT],
        kde=True,
        bins=20,
        color='#c44e52',
        alpha=0.7,
        ax=ax1
    )
    ax1.set_title('Expense Transaction Distribution', fontweight='bold', fontsize=12)
    ax1.set_xlabel('Amount', fontweight='bold', fontsize=10)
    ax1.set_ylabel('Frequency', fontweight='bold', fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.3)

    # Add mean and median markers
    mean_expense = expense_data[TransactionSchema.AMOUNT].mean()
    median_expense = expense_data[TransactionSchema.AMOUNT].median()

    ax1.axvline(mean_expense, color='black', linestyle='-', linewidth=1.5, alpha=0.7,
                label=f'Mean: ${mean_expense:.2f}')
    ax1.axvline(median_expense, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
                label=f'Median: ${median_expense:.2f}')
    ax1.legend(frameon=True, framealpha=0.9, edgecolor='lightgray')

    # Plot for income with KDE (if there's income data)
    if not income_data.empty:
        sns.histplot(
            income_data[TransactionSchema.AMOUNT],
            kde=True,
            bins=20,
            color='#55a868',
            alpha=0.7,
            ax=ax2
        )
        ax2.set_title('Income Transaction Distribution', fontweight='bold', fontsize=12)
        ax2.set_xlabel('Amount', fontweight='bold', fontsize=10)
        ax2.set_ylabel('Frequency', fontweight='bold', fontsize=10)
        ax2.grid(axis='y', linestyle='--', alpha=0.3)

        # Add mean and median markers
        mean_income = income_data[TransactionSchema.AMOUNT].mean()
        median_income = income_data[TransactionSchema.AMOUNT].median()

        ax2.axvline(mean_income, color='black', linestyle='-', linewidth=1.5, alpha=0.7,
                    label=f'Mean: ${mean_income:.2f}')
        ax2.axvline(median_income, color='gray', linestyle='--', linewidth=1.5, alpha=0.7,
                    label=f'Median: ${median_income:.2f}')
        ax2.legend(frameon=True, framealpha=0.9, edgecolor='lightgray')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'amount_distribution.png'), dpi=300, bbox_inches='tight')
    plt.close()

    # Return distribution statistics
    stats = {
        'expense': {
            'mean': mean_expense if 'mean_expense' in locals() else 0,
            'median': median_expense if 'median_expense' in locals() else 0,
            'count': len(expense_data)
        }
    }

    if not income_data.empty:
        stats['income'] = {
            'mean': mean_income,
            'median': median_income,
            'count': len(income_data)
        }

    return stats