"""
Financial calculation functions for the Cashflow Tracker
"""

import pandas as pd
from typing import Dict, Optional
from core.schema import TransactionSchema, CategorySchema


def calculate_net_cashflow(income: float, expense: float) -> float:
    """
    Calculate net cashflow

    Args:
        income: Total income
        expense: Total expense

    Returns:
        Net cashflow
    """
    return income - expense


def calculate_cash_allocation(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate cash allocation (spending/saving/investing)

    Args:
        df: DataFrame with transaction data

    Returns:
        Dict with allocation percentages
    """
    # Filter for expenses only
    expenses = df[df[TransactionSchema.TYPE] == 'Expense']
    total_expenses = expenses[TransactionSchema.AMOUNT].sum()

    # Calculate allocations
    spending = expenses[~expenses[TransactionSchema.CATEGORY].isin(
        ['Savings', 'Investments'])][TransactionSchema.AMOUNT].sum()

    saving = expenses[expenses[TransactionSchema.CATEGORY] == 'Savings'][
        TransactionSchema.AMOUNT].sum()

    investing = expenses[expenses[TransactionSchema.CATEGORY] == 'Investments'][
        TransactionSchema.AMOUNT].sum()

    # Calculate percentages
    if total_expenses > 0:
        return {
            'Spending': spending / total_expenses * 100,
            'Saving': saving / total_expenses * 100,
            'Investing': investing / total_expenses * 100
        }
    else:
        return {'Spending': 0, 'Saving': 0, 'Investing': 0}


def calculate_budget_comparison(actual_data: pd.DataFrame,
                                budget_data: pd.DataFrame) -> pd.DataFrame:
    """
    Compare actual spending with budget

    Args:
        actual_data: DataFrame with aggregated category data
        budget_data: DataFrame with budget data

    Returns:
        DataFrame with comparison results
    """
    # Filter for expenses only
    expenses = actual_data[actual_data[TransactionSchema.TYPE] == 'Expense']

    # Merge with budget data
    result = pd.merge(
        expenses,
        budget_data[[CategorySchema.MAIN_CATEGORY, CategorySchema.BUDGET]],
        left_on=TransactionSchema.CATEGORY,
        right_on=CategorySchema.MAIN_CATEGORY,
        how='left'
    )

    # Calculate percentage of budget used
    result['Budget Used (%)'] = (result[TransactionSchema.AMOUNT] /
                                 result[CategorySchema.BUDGET] * 100)

    # Calculate difference from budget
    result['Difference'] = result[CategorySchema.BUDGET] - result[TransactionSchema.AMOUNT]

    return result


def calculate_monthly_growth_rate(df: pd.DataFrame,
                                  months: int = 3) -> Dict[str, float]:
    """
    Calculate growth rate over recent months

    Args:
        df: DataFrame with transaction data
        months: Number of months to consider

    Returns:
        Dict with growth rates for income and expenses
    """
    # Add month column and sort
    df_with_month = df.copy()
    df_with_month['Month'] = pd.to_datetime(df_with_month[TransactionSchema.DATE]).dt.strftime('%Y-%m')
    monthly_data = df_with_month.groupby(['Month', TransactionSchema.TYPE])[
        TransactionSchema.AMOUNT].sum().reset_index()

    # Convert to pivot table
    pivot = monthly_data.pivot(index='Month', columns=TransactionSchema.TYPE,
                               values=TransactionSchema.AMOUNT).fillna(0)
    pivot = pivot.sort_index()

    # Limit to requested number of months
    pivot = pivot.tail(months)

    # Calculate growth rates
    growth_rates = {}

    for col in ['Income', 'Expense']:
        if col in pivot.columns and len(pivot) >= 2:
            first_value = pivot[col].iloc[0]
            last_value = pivot[col].iloc[-1]

            if first_value > 0:
                growth_rate = ((last_value / first_value) - 1) * 100
                growth_rates[f'{col} Growth'] = growth_rate
            else:
                growth_rates[f'{col} Growth'] = 0
        else:
            growth_rates[f'{col} Growth'] = 0

    return growth_rates


def calculate_savings_rate(income: float, expenses: float) -> float:
    """
    Calculate savings rate (percentage of income saved)

    Args:
        income: Total income
        expenses: Total expenses excluding savings/investments

    Returns:
        Savings rate as a percentage
    """
    if income > 0:
        savings = income - expenses
        return (savings / income) * 100
    else:
        return 0