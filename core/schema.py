"""
Data schemas for the Cashflow Tracker
"""

from typing import List


class TransactionSchema:
    """Schema for transaction data"""
    DATE = 'Date'
    DESCRIPTION = 'Description'
    AMOUNT = 'Amount'
    TYPE = 'Type'
    CATEGORY = 'Category'
    SUBCATEGORY = 'Subcategory'
    PRODUCER = 'Producer/Vendor'
    PAYMENT_METHOD = 'Payment Method'
    NOTES = 'Notes'

    @classmethod
    def get_columns(cls) -> List[str]:
        """Return all column names"""
        return [cls.DATE, cls.DESCRIPTION, cls.AMOUNT, cls.TYPE,
                cls.CATEGORY, cls.SUBCATEGORY, cls.PRODUCER,
                cls.PAYMENT_METHOD, cls.NOTES]


class CategorySchema:
    """Schema for category data"""
    MAIN_CATEGORY = 'Main Category'
    SUBCATEGORY = 'Subcategory'
    DESCRIPTION = 'Description'
    BUDGET = 'Budget Amount'

    @classmethod
    def get_columns(cls) -> List[str]:
        """Return all column names"""
        return [cls.MAIN_CATEGORY, cls.SUBCATEGORY, cls.DESCRIPTION, cls.BUDGET]