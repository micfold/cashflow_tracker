"""
Data processing functions for the Cashflow Tracker
"""

import pandas as pd
import re
from typing import Dict, List, Optional
from cashflow_tracker.core.schema import TransactionSchema


def clean_transaction_data(df: pd.DataFrame, date_col: Optional[str] = None,
                           amount_col: Optional[str] = None) -> pd.DataFrame:
    """
    Clean and normalize transaction data

    Args:
        df: DataFrame with raw transaction data
        date_col: Column name containing date (if not standard)
        amount_col: Column name containing amount (if not standard)

    Returns:
        Cleaned DataFrame with standardized structure
    """
    # Create a copy to avoid modifying the original
    clean_df = df.copy()

    # Map columns to standard schema if needed
    if date_col and date_col != TransactionSchema.DATE:
        clean_df[TransactionSchema.DATE] = clean_df[date_col]

    if amount_col and amount_col != TransactionSchema.AMOUNT:
        clean_df[TransactionSchema.AMOUNT] = clean_df[amount_col]

    # Ensure date is datetime
    if TransactionSchema.DATE in clean_df.columns:
        clean_df[TransactionSchema.DATE] = pd.to_datetime(clean_df[TransactionSchema.DATE])

    # Ensure amount is float
    if TransactionSchema.AMOUNT in clean_df.columns:
        clean_df[TransactionSchema.AMOUNT] = clean_df[TransactionSchema.AMOUNT].astype(float)

    # Add missing columns from the schema
    for col in TransactionSchema.get_columns():
        if col not in clean_df.columns:
            clean_df[col] = None

    # Determine transaction type based on amount if not specified
    if TransactionSchema.TYPE not in df.columns or df[TransactionSchema.TYPE].isna().any():
        mask = clean_df[TransactionSchema.AMOUNT] >= 0
        clean_df.loc[mask, TransactionSchema.TYPE] = 'Income'
        clean_df.loc[~mask, TransactionSchema.TYPE] = 'Expense'

        # Ensure expense amounts are positive for better readability
        expense_mask = clean_df[TransactionSchema.TYPE] == 'Expense'
        clean_df.loc[expense_mask, TransactionSchema.AMOUNT] = clean_df.loc[
            expense_mask, TransactionSchema.AMOUNT].abs()

    return clean_df[TransactionSchema.get_columns()]


def categorize_transaction(transaction: pd.Series,
                           category_rules: Dict[str, List[str]],
                           producer_category_map: Optional[Dict[str, str]] = None) -> pd.Series:
    """
    Categorize a transaction based on rules and maps

    Args:
        transaction: Series containing transaction data
        category_rules: Dict mapping keywords to categories
        producer_category_map: Dict mapping producers to categories

    Returns:
        Transaction with category assigned
    """
    new_transaction = transaction.copy()

    # First check if producer is in the map
    if (producer_category_map and
            transaction[TransactionSchema.PRODUCER] in producer_category_map):
        new_transaction[TransactionSchema.CATEGORY] = producer_category_map[
            transaction[TransactionSchema.PRODUCER]]
        return new_transaction

    # Check description against rules
    description = str(transaction[TransactionSchema.DESCRIPTION]).lower()

    for category, keywords in category_rules.items():
        for keyword in keywords:
            if keyword.lower() in description:
                new_transaction[TransactionSchema.CATEGORY] = category
                return new_transaction

    # Default category based on type
    if transaction[TransactionSchema.TYPE] == 'Income':
        new_transaction[TransactionSchema.CATEGORY] = 'Income'
    else:
        new_transaction[TransactionSchema.CATEGORY] = 'Miscellaneous'

    return new_transaction


def categorize_all_transactions(df: pd.DataFrame,
                                category_rules: Dict[str, List[str]],
                                producer_category_map: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Apply categorization to all transactions

    Args:
        df: DataFrame with transaction data
        category_rules: Dict mapping keywords to categories
        producer_category_map: Dict mapping producers to categories

    Returns:
        DataFrame with categories assigned
    """
    return df.apply(
        lambda row: categorize_transaction(row, category_rules, producer_category_map),
        axis=1
    )


def extract_producer(transaction: pd.Series,
                     producer_patterns: Optional[Dict[str, str]] = None) -> pd.Series:
    """
    Extract producer/vendor information from transaction

    Args:
        transaction: Series containing transaction data
        producer_patterns: Dict of regex patterns to extract producer names

    Returns:
        Transaction with producer assigned
    """
    new_transaction = transaction.copy()

    # Skip if producer is already assigned
    if pd.notna(transaction[TransactionSchema.PRODUCER]):
        return new_transaction

    description = str(transaction[TransactionSchema.DESCRIPTION])

    # Apply regex patterns if provided
    if producer_patterns:
        for pattern, producer in producer_patterns.items():
            if re.search(pattern, description, re.IGNORECASE):
                new_transaction[TransactionSchema.PRODUCER] = producer
                return new_transaction

    # Default: use first part of description as producer
    words = description.split()
    if words:
        new_transaction[TransactionSchema.PRODUCER] = words[0]

    return new_transaction


def extract_all_producers(df: pd.DataFrame,
                          producer_patterns: Optional[Dict[str, str]] = None) -> pd.DataFrame:
    """
    Apply producer extraction to all transactions

    Args:
        df: DataFrame with transaction data
        producer_patterns: Dict of regex patterns to extract producer names

    Returns:
        DataFrame with producers assigned
    """
    return df.apply(
        lambda row: extract_producer(row, producer_patterns),
        axis=1
    )
