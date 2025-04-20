"""
Charts module for the Cashflow Tracker
"""

from .manager import (
    create_visualisations,
    PROFESSIONAL_COLORS,
    money_formatter,
    set_professional_style,
)
from .category_spending_chart import generate_spending_by_category_chart
from .monthly_comparison_chart import generate_monthly_comparison_chart
from .cash_allocation_chart import generate_cash_allocation_chart
from .net_cashflow_chart import generate_net_cashflow_chart
from .category_heatmap import generate_category_stacked
from .top_vendors_chart import generate_top_vendors_chart

# Advanced chart generators
from .daily_spending_chart import generate_daily_spending_chart
from .weekday_spending_chart import generate_weekday_spending_chart
from .transaction_distribution_chart import generate_transaction_distribution_chart
from .budget_comparison_chart import generate_budget_comparison_chart
from .cumulative_cashflow_chart import generate_cumulative_cashflow_chart

from .monthly_category_proportion_chart import generate_monthly_category_proportion
from .category_treemap_chart import generate_category_treemap
from .sankey_flow_chart import generate_sankey_flow_diagram

# For backward compatibility
def create_matplotlib_charts(transaction_data, output_dir='.'):
    """Backward compatibility wrapper for create_visualisations"""
    return create_visualisations(transaction_data, output_dir)

def create_advanced_visualisations(transaction_data, output_dir='.', budget_data=None):
    """Backward compatibility wrapper for create_visualisations"""
    return create_visualisations(transaction_data, output_dir, budget_data)

__all__ = ['create_visualisations',
           'create_matplotlib_charts', # will be removed once regression tests are done
           'create_advanced_visualisations', # will be removed once regression tests are done
           'PROFESSIONAL_COLORS',
           'money_formatter',
           'set_professional_style',
           'generate_spending_by_category_chart',
           'generate_cash_allocation_chart',
           'generate_monthly_comparison_chart',
           'generate_net_cashflow_chart',
           'generate_category_stacked',
           'generate_top_vendors_chart',
           'generate_daily_spending_chart',
           'generate_weekday_spending_chart',
           'generate_transaction_distribution_chart',
           'generate_budget_comparison_chart',
           'generate_cumulative_cashflow_chart',
           'generate_monthly_category_proportion',
           'generate_category_treemap',
           'generate_sankey_flow_diagram',



           # Add other chart functions as they're implemented
]