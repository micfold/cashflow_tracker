# output/visualisations/charts/constants.py
"""
Constants for chart generation in the Cashflow Tracker
"""

# Set up styling constants
PROFESSIONAL_COLORS = [
    '#4c72b0',  # blue
    '#55a868',  # green
    '#c44e52',  # red
    '#8172b3',  # purple
    '#ccb974',  # yellow
    '#64b5cd',  # light blue
    '#a9b5ae',  # gray-green
    '#dd8452',  # orange
]

def money_formatter(x, pos):
    """Format y-axis ticks as currency values"""
    return f'${x:,.0f}'