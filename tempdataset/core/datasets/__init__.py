"""
Dataset definitions module.

Contains all dataset generators including the base abstract class.
"""

from .base import BaseDataset
from .customers import CustomersDataset
from .ecommerce import EcommerceDataset

__all__ = ["BaseDataset", "CustomersDataset", "EcommerceDataset"]