"""
Chart generation logic for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
from io import BytesIO
import base64
from typing import Dict, List, Optional, Tuple
from cashflow_tracker.core.schema import TransactionSchema


def generate_pie_chart_base64(data: Dict[str, float], title: str,
                              colors: Optional[List[str]] = None) -> str:
    """
    Generate a pie chart and return as base64 encoded string

    Args:
        data: Dictionary with labels and values
        title: Chart title
        colors: Optional list of colors

    Returns:
        Base64 encoded PNG image
    """
    # Create figure and plot
    plt.figure(figsize=(8, 6))
    plt.pie(data.values(), labels=data.keys(), autopct='%1.1f%%',
            startangle=90, shadow=True, colors=colors)
    plt.axis('equal')
    plt.title(title)

    # Save to in-memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    plt.close()

    # Convert to base64
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{image_data}"


def generate_bar_chart_base64(data: pd.DataFrame, x_col: str, y_col: str,
                              title: str, xlabel: str, ylabel: str) -> str:
    """
    Generate a bar chart and return as base64 encoded string

    Args:
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_col: Column name for y-axis
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label

    Returns:
        Base64 encoded PNG image
    """
    plt.figure(figsize=(10, 6))
    plt.bar(data[x_col], data[y_col], color=plt.cm.tab10.colors[:len(data)])
    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()

    # Save to in-memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    plt.close()

    # Convert to base64
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{image_data}"


def generate_line_chart_base64(data: pd.DataFrame, x_col: str, y_cols: List[str],
                               title: str, xlabel: str, ylabel: str) -> str:
    """
    Generate a line chart and return as base64 encoded string

    Args:
        data: DataFrame with chart data
        x_col: Column name for x-axis
        y_cols: List of column names for y-axis (multiple lines)
        title: Chart title
        xlabel: X-axis label
        ylabel: Y-axis label

    Returns:
        Base64 encoded PNG image
    """
    plt.figure(figsize=(10, 6))

    for i, col in enumerate(y_cols):
        plt.plot(data[x_col], data[col], marker='o', linewidth=2,
                 label=col, color=plt.cm.tab10.colors[i % 10])

    plt.title(title)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()
    plt.tight_layout()

    # Save to in-memory buffer
    buffer = BytesIO()
    plt.savefig(buffer, format='png', dpi=100)
    plt.close()

    # Convert to base64
    buffer.seek(0)
    image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

    return f"data:image/png;base64,{image_data}"


def generate_spending_by_category_chart(transaction_data: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    """
    Generate a spending by category pie chart

    Args:
        transaction_data: DataFrame with transaction data

    Returns:
        Tuple of (base64 image, category data dictionary)
    """
    # Filter for expenses only
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']

    # Group by category
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[
        TransactionSchema.AMOUNT].sum().to_dict()

    # Generate chart
    chart = generate_pie_chart_base64(
        category_totals,
        'Spending by Category',
        plt.cm.Paired.colors
    )

    return chart, category_totals


def generate_cash_allocation_chart(transaction_data: pd.DataFrame) -> Tuple[str, Dict[str, float]]:
    """
    Generate a cash allocation pie chart

    Args:
        transaction_data: DataFrame with transaction data

    Returns:
        Tuple of (base64 image, allocation data dictionary)
    """
    # Filter for expenses only
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']

    # Calculate allocations
    spending = expense_data[~expense_data[TransactionSchema.CATEGORY].isin(
        ['Savings', 'Investments'])][TransactionSchema.AMOUNT].sum()

    saving = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Savings'][
        TransactionSchema.AMOUNT].sum()

    investing = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Investments'][
        TransactionSchema.AMOUNT].sum()

    # Create data dictionary
    allocation_data = {
        'Spending': spending,
        'Saving': saving,
        'Investing': investing
    }

    # Generate chart
    chart = generate_pie_chart_base64(
        allocation_data,
        'Cash Allocation',
        ['#ff9999', '#66b3ff', '#99ff99']
    )

    return chart, allocation_data