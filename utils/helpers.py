"""
Helper functions for the Cashflow Tracker
"""

import pandas as pd
import os
import re
from typing import Dict, List, Optional, Union, Any
from datetime import datetime, timedelta
import calendar


def ensure_directory_exists(directory_path: str) -> None:
    """
    Ensure that a directory exists, creating it if necessary

    Args:
        directory_path: Path to the directory
    """
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)


def format_currency(value: Union[float, int]) -> str:
    """
    Format a numeric value as a currency string

    Args:
        value: Numeric value to format

    Returns:
        Formatted currency string
    """
    return f"${value:,.2f}"


def format_percentage(value: Union[float, int]) -> str:
    """
    Format a numeric value as a percentage string

    Args:
        value: Numeric value to format (0-100)

    Returns:
        Formatted percentage string
    """
    return f"{value:.1f}%"


def extract_date_from_filename(filename: str) -> Optional[datetime]:
    """
    Extract a date from a filename (e.g., statement_2025_04_15.csv)

    Args:
        filename: Name of the file

    Returns:
        Datetime object if a date is found, None otherwise
    """
    # Try to find a date pattern in the format YYYY_MM_DD or YYYY-MM-DD
    pattern = r'(\d{4})[_-](\d{1,2})[_-](\d{1,2})'
    match = re.search(pattern, filename)

    if match:
        try:
            year = int(match.group(1))
            month = int(match.group(2))
            day = int(match.group(3))
            return datetime(year, month, day)
        except (ValueError, IndexError):
            return None

    return None


def get_month_range(year: int, month: int) -> tuple:
    """
    Get the start and end dates for a specific month

    Args:
        year: Year
        month: Month (1-12)

    Returns:
        Tuple of (start_date, end_date)
    """
    start_date = datetime(year, month, 1)

    # Calculate the last day of the month
    _, last_day = calendar.monthrange(year, month)
    end_date = datetime(year, month, last_day)

    return start_date, end_date


def detect_csv_dialect(file_path: str) -> Dict[str, Any]:
    """
    Detect the dialect (delimiter, etc.) of a CSV file

    Args:
        file_path: Path to the CSV file

    Returns:
        Dictionary with detected parameters
    """
    # Read a small sample of the file
    with open(file_path, 'r', newline='', encoding='utf-8-sig') as f:
        sample = f.read(4096)

    # Count potential delimiters
    delimiters = [',', ';', '\t', '|']
    counts = {d: sample.count(d) for d in delimiters}

    # Select the delimiter with the highest count
    likely_delimiter = max(counts.items(), key=lambda x: x[1])[0]

    # Detect if the first row is a header
    lines = sample.split('\n')
    if len(lines) >= 2:
        first_row = lines[0].split(likely_delimiter)
        second_row = lines[1].split(likely_delimiter)

        # If the first row contains mostly strings and the second row contains
        # mostly numbers, the first row is likely a header
        first_row_numeric = sum(1 for cell in first_row if cell.strip().replace('.', '', 1).isdigit())
        second_row_numeric = sum(1 for cell in second_row if cell.strip().replace('.', '', 1).isdigit())

        has_header = first_row_numeric < second_row_numeric
    else:
        has_header = True  # Default assumption

    return {
        'delimiter': likely_delimiter,
        'has_header': has_header,
        'quotechar': '"',
        'doublequote': True
    }


def merge_dataframes(df1: pd.DataFrame, df2: pd.DataFrame, key_columns: List[str]) -> pd.DataFrame:
    """
    Merge two DataFrames, handling duplicate columns

    Args:
        df1: First DataFrame
        df2: Second DataFrame
        key_columns: List of column names to use as keys for the merge

    Returns:
        Merged DataFrame
    """
    # Find columns in both DataFrames
    common_cols = set(df1.columns) & set(df2.columns)
    common_cols = common_cols - set(key_columns)

    # Create suffixes for duplicate columns
    suffixes = ('_1', '_2')

    # Merge DataFrames
    merged_df = pd.merge(df1, df2, on=key_columns, suffixes=suffixes, how='outer')

    # Combine duplicate columns (prefer df1 values, use df2 if df1 is NaN)
    for col in common_cols:
        col1 = f"{col}{suffixes[0]}"
        col2 = f"{col}{suffixes[1]}"

        # Create combined column
        merged_df[col] = merged_df[col1].combine_first(merged_df[col2])

        # Drop the duplicate columns
        merged_df = merged_df.drop([col1, col2], axis=1)

    return merged_df


def generate_filename(base_name: str, extension: str, timestamp: bool = True) -> str:
    """
    Generate a filename with an optional timestamp

    Args:
        base_name: Base name for the file
        extension: File extension (without the dot)
        timestamp: Whether to include a timestamp

    Returns:
        Generated filename
    """
    if timestamp:
        now = datetime.now()
        timestamp_str = now.strftime('%Y%m%d_%H%M%S')
        return f"{base_name}_{timestamp_str}.{extension}"
    else:
        return f"{base_name}.{extension}"


def deep_get(dictionary: Dict[str, Any], keys: List[str], default: Any = None) -> Any:
    """
    Safely get a value from a nested dictionary

    Args:
        dictionary: Dictionary to get the value from
        keys: List of keys to traverse
        default: Default value to return if the key is not found

    Returns:
        Value at the specified keys or the default value
    """
    d = dictionary
    for key in keys:
        if isinstance(d, dict) and key in d:
            d = d[key]
        else:
            return default
    return d