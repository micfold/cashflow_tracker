"""
Data visualization functions for the Cashflow Tracker
"""

import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import os
from typing import Optional
from cashflow_tracker.core.schema import TransactionSchema

def create_matplotlib_charts(transaction_data: pd.DataFrame, output_dir: str = '.') -> None:
    """
    Create matplotlib visualizations and save as image files

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set style
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)

    # 1. Spending by Category Pie Chart
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']
    category_totals = expense_data.groupby(TransactionSchema.CATEGORY)[TransactionSchema.AMOUNT].sum()

    plt.figure(figsize=(10, 8))
    plt.pie(category_totals, labels=category_totals.index, autopct='%1.1f%%',
           startangle=90, shadow=True)
    plt.axis('equal')
    plt.title('Spending by Category', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'category_spending_pie.png'), dpi=300)
    plt.close()

    # 2. Cash Allocation Pie Chart (Spending/Saving/Investing)
    # Calculate the allocations
    spending = expense_data[~expense_data[TransactionSchema.CATEGORY].isin(
        ['Savings', 'Investments'])][TransactionSchema.AMOUNT].sum()

    saving = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Savings'][
        TransactionSchema.AMOUNT].sum()

    investing = expense_data[expense_data[TransactionSchema.CATEGORY] == 'Investments'][
        TransactionSchema.AMOUNT].sum()

    # Create pie chart
    allocation_data = [spending, saving, investing]
    allocation_labels = ['Spending', 'Saving', 'Investing']

    plt.figure(figsize=(10, 8))
    plt.pie(allocation_data, labels=allocation_labels, autopct='%1.1f%%',
           startangle=90, shadow=True, colors=['#ff9999','#66b3ff','#99ff99'])
    plt.axis('equal')
    plt.title('Cash Allocation', fontsize=16)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cash_allocation_pie.png'), dpi=300)
    plt.close()

    # 3. Monthly Income vs Expenses Bar Chart
    transaction_data['Month'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.strftime('%Y-%m')
    monthly_data = transaction_data.groupby(['Month', TransactionSchema.TYPE])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Pivot the data for easier plotting
    monthly_pivot = pd.pivot_table(
        monthly_data,
        index='Month',
        columns=TransactionSchema.TYPE,
        values=TransactionSchema.AMOUNT,
        aggfunc='sum'
    ).fillna(0)

    # Sort by month
    monthly_pivot = monthly_pivot.sort_index()

    # Create bar chart
    plt.figure(figsize=(12, 6))
    monthly_pivot.plot(kind='bar', color=['green', 'red'])
    plt.title('Monthly Income vs Expenses', fontsize=16)
    plt.xlabel('Month')
    plt.ylabel('Amount')
    plt.legend(title='Type')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'monthly_comparison_bar.png'), dpi=300)
    plt.close()

    # 4. Net Cashflow Line Chart
    net_cashflow = monthly_pivot.copy()
    if 'Income' in net_cashflow.columns and 'Expense' in net_cashflow.columns:
        net_cashflow['Net'] = net_cashflow['Income'] - net_cashflow['Expense']

        plt.figure(figsize=(12, 6))
        net_cashflow['Net'].plot(kind='line', marker='o', color='blue', linewidth=2)
        plt.axhline(y=0, color='r', linestyle='-', alpha=0.3)
        plt.title('Net Cashflow Trend', fontsize=16)
        plt.xlabel('Month')
        plt.ylabel('Net Cashflow')
        plt.grid(True)
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'net_cashflow_line.png'), dpi=300)
        plt.close()

    # 5. Category Spending Heatmap by Month
    if len(monthly_pivot) > 1:
        # Aggregate expenses by category and month
        category_monthly = expense_data.groupby(['Month', TransactionSchema.CATEGORY])[
            TransactionSchema.AMOUNT].sum().reset_index()

        # Pivot to get categories as columns and months as rows
        category_pivot = pd.pivot_table(
            category_monthly,
            index='Month',
            columns=TransactionSchema.CATEGORY,
            values=TransactionSchema.AMOUNT,
            aggfunc='sum'
        ).fillna(0)

        # Sort by month
        category_pivot = category_pivot.sort_index()

        # Create heatmap
        plt.figure(figsize=(14, 8))
        sns.heatmap(category_pivot, annot=True, fmt='.0f', cmap='YlGnBu')
        plt.title('Monthly Spending by Category', fontsize=16)
        plt.ylabel('Month')
        plt.xlabel('Category')
        plt.tight_layout()
        plt.savefig(os.path.join(output_dir, 'category_month_heatmap.png'), dpi=300)
        plt.close()

    # 6. Top Spending by Producer/Vendor
    producer_totals = expense_data.groupby(TransactionSchema.PRODUCER)[
        TransactionSchema.AMOUNT].sum().sort_values(ascending=False)

    # Get top 10 producers
    top_producers = producer_totals.head(10)

    plt.figure(figsize=(12, 6))
    top_producers.plot(kind='bar', color=plt.cm.tab10.colors)
    plt.title('Top 10 Vendors by Spending', fontsize=16)
    plt.xlabel('Vendor')
    plt.ylabel('Total Amount')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'top_producers_bar.png'), dpi=300)
    plt.close()

def create_advanced_visualizations(transaction_data: pd.DataFrame,
                                 output_dir: str = '.',
                                 budget_data: Optional[pd.DataFrame] = None) -> None:
    """
    Create advanced visualizations for deeper financial analysis

    Args:
        transaction_data: DataFrame with transaction data
        output_dir: Directory to save images
        budget_data: Optional DataFrame with budget information
    """
    # Ensure output directory exists
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set style
    sns.set_style('whitegrid')
    plt.rcParams['figure.figsize'] = (10, 6)

    # Process data
    expense_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Expense']
    transaction_data['Month'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.strftime('%Y-%m')
    transaction_data['Day'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.day
    transaction_data['Weekday'] = pd.to_datetime(transaction_data[TransactionSchema.DATE]).dt.day_name()

    # 1. Spending Patterns by Day of Month
    daily_spending = expense_data.groupby('Day')[TransactionSchema.AMOUNT].sum()

    plt.figure(figsize=(14, 6))
    daily_spending.plot(kind='bar', color=plt.cm.viridis(np.linspace(0, 1, len(daily_spending))))
    plt.title('Spending by Day of Month', fontsize=16)
    plt.xlabel('Day')
    plt.ylabel('Total Amount')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spending_by_day.png'), dpi=300)
    plt.close()

    # 2. Spending by Day of Week
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    weekday_spending = expense_data.groupby('Weekday')[TransactionSchema.AMOUNT].sum()
    weekday_spending = weekday_spending.reindex(weekday_order)

    plt.figure(figsize=(12, 6))
    weekday_spending.plot(kind='bar', color=plt.cm.tab10.colors)
    plt.title('Spending by Day of Week', fontsize=16)
    plt.xlabel('Day of Week')
    plt.ylabel('Total Amount')
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'spending_by_weekday.png'), dpi=300)
    plt.close()

    # 3. Distribution of Transaction Amounts
    plt.figure(figsize=(12, 6))

    # Plot for expenses
    plt.subplot(1, 2, 1)
    sns.histplot(expense_data[TransactionSchema.AMOUNT], kde=True, bins=20, color='red')
    plt.title('Distribution of Expense Amounts', fontsize=14)
    plt.xlabel('Amount')
    plt.ylabel('Frequency')

    # Plot for income
    income_data = transaction_data[transaction_data[TransactionSchema.TYPE] == 'Income']
    if not income_data.empty:
        plt.subplot(1, 2, 2)
        sns.histplot(income_data[TransactionSchema.AMOUNT], kde=True, bins=20, color='green')
        plt.title('Distribution of Income Amounts', fontsize=14)
        plt.xlabel('Amount')
        plt.ylabel('Frequency')

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'amount_distribution.png'), dpi=300)
    plt.close()

    # 4. Budget vs Actual Comparison (if budget data is provided)
    if budget_data is not None:
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

        if not budget_compare.empty:
            plt.figure(figsize=(14, 8))

            # Create bar positions
            categories = budget_compare[TransactionSchema.CATEGORY]
            x_pos = np.arange(len(categories))
            width = 0.35

            # Create bars
            plt.bar(x_pos - width/2, budget_compare['Amount'], width, label='Actual', color='coral')
            plt.bar(x_pos + width/2, budget_compare['Budget Amount'], width, label='Budget', color='skyblue')

            # Add labels and formatting
            plt.xlabel('Category', fontsize=12)
            plt.ylabel('Amount', fontsize=12)
            plt.title('Budget vs Actual by Category', fontsize=16)
            plt.xticks(x_pos, categories, rotation=45, ha='right')
            plt.legend()
            plt.grid(axis='y', linestyle='--', alpha=0.7)

            plt.tight_layout()
            plt.savefig(os.path.join(output_dir, 'budget_vs_actual.png'), dpi=300)
            plt.close()

    # 5. Cumulative Cashflow Over Time
    transaction_data['Date'] = pd.to_datetime(transaction_data[TransactionSchema.DATE])
    transaction_data = transaction_data.sort_values('Date')

    # Group by date and type
    daily_data = transaction_data.groupby(['Date', TransactionSchema.TYPE])[
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

    plt.figure(figsize=(14, 8))
    plt.plot(daily_pivot['Date'], daily_pivot['Cumulative Income'], 'g-', label='Cumulative Income')
    plt.plot(daily_pivot['Date'], daily_pivot['Cumulative Expense'], 'r-', label='Cumulative Expense')
    plt.plot(daily_pivot['Date'], daily_pivot['Net Cashflow'], 'b-', label='Net Cashflow')

    plt.fill_between(daily_pivot['Date'], daily_pivot['Cumulative Income'], alpha=0.2, color='green')
    plt.fill_between(daily_pivot['Date'], daily_pivot['Cumulative Expense'], alpha=0.2, color='red')

    # Add formatting
    plt.title('Cumulative Cashflow Over Time', fontsize=16)
    plt.xlabel('Date')
    plt.ylabel('Amount')
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.legend()

    # Add annotations for key points
    max_net = daily_pivot['Net Cashflow'].max()
    max_net_date = daily_pivot.loc[daily_pivot['Net Cashflow'].idxmax(), 'Date']

    min_net = daily_pivot['Net Cashflow'].min()
    min_net_date = daily_pivot.loc[daily_pivot['Net Cashflow'].idxmin(), 'Date']

    plt.annotate(f'Max: {max_net:.2f}', xy=(max_net_date, max_net),
                xytext=(10, 10), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

    plt.annotate(f'Min: {min_net:.2f}', xy=(min_net_date, min_net),
                xytext=(10, -20), textcoords='offset points',
                arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=.2'))

    plt.tight_layout()
    plt.savefig(os.path.join(output_dir, 'cumulative_cashflow.png'), dpi=300)
    plt.close()