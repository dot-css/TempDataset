"""
Dataset definitions module.

Contains all dataset generators including the base abstract class.
"""

from .base import BaseDataset
from .customers import CustomersDataset
from .ecommerce import EcommerceDataset
from .marketing import MarketingDataset
from .retail import RetailDataset
from .sales import SalesDataset
from .suppliers import SuppliersDataset

__all__ = ["BaseDataset", "CustomersDataset", "EcommerceDataset", "MarketingDataset", "RetailDataset", "SalesDataset", "SuppliersDataset"]