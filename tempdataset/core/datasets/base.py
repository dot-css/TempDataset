"""
Base dataset class for all dataset generators.

Provides the abstract interface that all dataset generators must implement.
"""

from abc import ABC, abstractmethod
from typing import List, Dict, Any
import random


class BaseDataset(ABC):
    """
    Abstract base class for all dataset generators.
    
    This class defines the interface that all dataset generators must implement
    to be compatible with the TempDataset library.
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the dataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        self.rows = rows
        self.seed = None
    
    @abstractmethod
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate dataset rows.
        
        Returns:
            List of dictionaries representing dataset rows
        """
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        pass
    
    def set_seed(self, seed: int) -> None:
        """
        Set random seed for reproducible generation.
        
        Args:
            seed: Random seed value
        """
        self.seed = seed
        random.seed(seed)