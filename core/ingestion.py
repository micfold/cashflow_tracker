"""
Data ingestion functions for the Cashflow Tracker
"""

import pandas as pd
from typing import Optional
from core.schema import TransactionSchema


def ingest_csv(file_path: str) -> pd.DataFrame:
    """
    Ingest data from CSV file

    Args:
        file_path: Path to the CSV file

    Returns:
        DataFrame with the raw data
    """
    return pd.read_csv(file_path)


def ingest_excel(file_path: str, sheet_name: Optional[str] = None) -> pd.DataFrame:
    """
    Ingest data from Excel file

    Args:
        file_path: Path to the Excel file
        sheet_name: Name of the sheet to read (optional)

    Returns:
        DataFrame with the raw data
    """
    if sheet_name:
        return pd.read_excel(file_path, sheet_name=sheet_name)
    else:
        return pd.read_excel(file_path)


def create_manual_transaction(date: str, description: str, amount: float,
                              transaction_type: str, category: Optional[str] = None,
                              subcategory: Optional[str] = None, producer: Optional[str] = None,
                              payment_method: Optional[str] = None, notes: Optional[str] = None) -> pd.Series:
    """
    Create a new transaction manually

    Args:
        date: Transaction date (YYYY-MM-DD)
        description: Transaction description
        amount: Transaction amount (positive for income, negative for expense)
        transaction_type: 'Income' or 'Expense'
        category, subcategory, producer, payment_method, notes: Optional fields

    Returns:
        Series containing the transaction data
    """
    return pd.Series({
        TransactionSchema.DATE: pd.to_datetime(date),
        TransactionSchema.DESCRIPTION: description,
        TransactionSchema.AMOUNT: float(amount),
        TransactionSchema.TYPE: transaction_type,
        TransactionSchema.CATEGORY: category,
        TransactionSchema.SUBCATEGORY: subcategory,
        TransactionSchema.PRODUCER: producer,
        TransactionSchema.PAYMENT_METHOD: payment_method,
        TransactionSchema.NOTES: notes
    })
