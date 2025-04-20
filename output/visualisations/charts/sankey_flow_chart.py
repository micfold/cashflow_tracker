"""
Sankey diagram chart generation for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import os
from core.schema import TransactionSchema
from .constants import PROFESSIONAL_COLORS
import plotly.graph_objects as go
import plotly.io as pio

def generate_sankey_flow_diagram(transaction_data: pd.DataFrame, output_dir: str = '.') -> dict:
    """
    Generate a Sankey diagram showing the flow of money from income categories to expense categories.

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images

    Returns:
        Dictionary with flow data
    """

    # Split transactions into income and expense
    income_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Income']
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']

    # Aggregate by category
    income_by_category = income_data.groupby(TransactionSchema.CATEGORY)[TransactionSchema.AMOUNT].sum()
    expense_by_category = expense_data.groupby(TransactionSchema.CATEGORY)[TransactionSchema.AMOUNT].sum()

    # Create nodes
    nodes = []
    node_colors = []

    # Income nodes (sources)
    for category in income_by_category.index:
        nodes.append(f"Income: {category}")
        node_colors.append('#55a868')  # Green for income

    # Add "Total Income" node
    nodes.append("Total Income")
    node_colors.append('#55a868')  # Green

    # Expense nodes (targets)
    for category in expense_by_category.index:
        nodes.append(f"Expense: {category}")
        node_colors.append('#c44e52')  # Red for expense

    # Create links from income categories to total income
    source = []
    target = []
    value = []

    # Index of "Total Income" node
    total_income_idx = len(income_by_category)

    # Links from income categories to total income
    for i, (category, amount) in enumerate(income_by_category.items()):
        source.append(i)  # Income category node
        target.append(total_income_idx)  # Total income node
        value.append(amount)

    # Links from total income to expense categories
    for i, (category, amount) in enumerate(expense_by_category.items()):
        source.append(total_income_idx)  # Total income node
        target.append(total_income_idx + 1 + i)  # Expense category node
        value.append(amount)


    # Create links with color
    link_colors = ['rgba(85, 168, 104, 0.5)' for _ in range(len(income_by_category))] + \
                  ['rgba(196, 78, 82, 0.5)' for _ in range(len(expense_by_category))]

    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=nodes,
            color=node_colors
        ),
        link=dict(
            source=source,
            target=target,
            value=value,
            color=link_colors
        )
    )])

    # Update layout
    fig.update_layout(
        title_text="Cashflow Sankey Diagram",
        font_size=12,
        font_family="Arial",
        width=1000,
        height=800
    )

    # Save as HTML (interactive) and as PNG (static)
    pio.write_html(fig, os.path.join(output_dir, 'cashflow_sankey.html'))
    pio.write_image(fig, os.path.join(output_dir, 'cashflow_sankey.png'))

    # Return flow data
    return {
        'nodes': nodes,
        'source': source,
        'target': target,
        'value': value
    }