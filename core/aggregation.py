"""
Data aggregation functions for the Cashflow Tracker
"""

import pandas as pd
from typing import Dict
from core.schema import TransactionSchema


def aggregate_by_type(df: pd.DataFrame) -> Dict[str, float]:
    """
    Aggregate transactions by type (Income/Expense)

    Args:
        df: DataFrame with transaction data

    Returns:
        Dict with total income and expense
    """
    result = df.groupby(TransactionSchema.TYPE)[TransactionSchema.AMOUNT].sum()

    return {
        'Income': result.get('Income', 0),
        'Expense': result.get('Expense', 0)
    }


def aggregate_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions by category

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame with amount sum per category
    """
    return df.groupby([TransactionSchema.TYPE, TransactionSchema.CATEGORY])[
        TransactionSchema.AMOUNT].sum().reset_index()


def aggregate_by_producer(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions by producer/vendor

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame with amount sum per producer
    """
    return df.groupby([TransactionSchema.TYPE, TransactionSchema.PRODUCER])[
        TransactionSchema.AMOUNT].sum().reset_index()


def aggregate_by_month(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions by month

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame with amount sum per month and type
    """
    # Add month column
    df_with_month = df.copy()
    df_with_month['Month'] = df_with_month[TransactionSchema.DATE].dt.strftime('%Y-%m')

    # Group by month and type
    return df_with_month.groupby(['Month', TransactionSchema.TYPE])[
        TransactionSchema.AMOUNT].sum().reset_index()


def aggregate_by_payment_method(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions by payment method

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame with amount sum per payment method
    """
    return df.groupby([TransactionSchema.TYPE, TransactionSchema.PAYMENT_METHOD])[
        TransactionSchema.AMOUNT].sum().reset_index()


def aggregate_by_subcategory(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aggregate transactions by subcategory

    Args:
        df: DataFrame with transaction data

    Returns:
        DataFrame with amount sum per subcategory within category
    """
    return df.groupby([TransactionSchema.TYPE, TransactionSchema.CATEGORY,
                       TransactionSchema.SUBCATEGORY])[
        TransactionSchema.AMOUNT].sum().reset_index()
