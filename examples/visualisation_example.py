"""
Example script showing advanced visualizations
"""

import sys
import os
import pandas as pd
from pathlib import Path

# Add parent directory to path to import package
sys.path.append(str(Path(__file__).parent.parent))

from cashflow_tracker.utils.defaults import generate_sample_transactions
from cashflow_tracker.core.processing import clean_transaction_data
from cashflow_tracker.output.visualisations import (
    create_matplotlib_charts, create_advanced_visualizations
)
from cashflow_tracker.utils.defaults import create_default_categories


def main():
    """Create advanced visualizations from sample data"""
    print("Generating sample data for visualizations...")

    # Generate a larger sample for better visualizations
    transactions = generate_sample_transactions(num_transactions=200)
    transactions = clean_transaction_data(transactions)

    # Create output directory
    output_dir = 'advanced_charts'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Generate standard charts
    print("Generating standard charts...")
    create_matplotlib_charts(transactions, output_dir)

    # Generate advanced charts
    print("Generating advanced charts...")
    categories = create_default_categories()
    create_advanced_visualizations(transactions, output_dir, categories)

    print(f"All charts generated in '{output_dir}' directory")

    # List the generated charts
    chart_files = os.listdir(output_dir)
    print("\nGenerated chart files:")
    for i, file in enumerate(chart_files, 1):
        print(f"{i}. {file}")


if __name__ == "__main__":
    main()