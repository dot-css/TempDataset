"""
Core data generation engine.

Coordinates dataset generation and manages the dataset registry.
"""

import os
from typing import Dict, Type, Union, Optional
from .datasets.base import BaseDataset
from .utils.data_frame import TempDataFrame


class DataGenerator:
    """
    Main data generation engine that coordinates dataset creation.
    
    Manages dataset registration and provides the main generation interface.
    """
    
    def __init__(self):
        """Initialize the data generator with empty registry."""
        self.datasets: Dict[str, Type[BaseDataset]] = {}
        self.faker_available = self._check_faker()
    
    def register_dataset(self, name: str, dataset_class: Type[BaseDataset]) -> None:
        """
        Register a new dataset type.
        
        Args:
            name: Name of the dataset type
            dataset_class: Class that implements BaseDataset
        """
        self.datasets[name] = dataset_class
    
    def generate(self, dataset_type: str, rows: int = 500) -> Union[TempDataFrame, None]:
        """
        Generate dataset using registered generators.
        
        Args:
            dataset_type: Dataset type ('sales') or filename ('sales.csv', 'sales.json')
            rows: Number of rows to generate
            
        Returns:
            TempDataFrame for dataset types, None for file outputs
        """
        # Check if it's a file output request
        if dataset_type.endswith('.csv') or dataset_type.endswith('.json'):
            return self._generate_to_file(dataset_type, rows)
        
        # Generate dataset in memory
        if dataset_type not in self.datasets:
            available = list(self.datasets.keys())
            raise ValueError(f"Dataset type '{dataset_type}' not found. Available types: {available}")
        
        dataset_class = self.datasets[dataset_type]
        dataset = dataset_class(rows)
        data = dataset.generate()
        schema = dataset.get_schema()
        columns = list(schema.keys())
        
        return TempDataFrame(data, columns)
    
    def _generate_to_file(self, filename: str, rows: int) -> None:
        """
        Generate dataset and save to file.
        
        Args:
            filename: Output filename with extension
            rows: Number of rows to generate
        """
        # Extract dataset type from filename
        base_name = os.path.splitext(filename)[0]
        extension = os.path.splitext(filename)[1]
        
        # For now, assume 'sales' dataset - will be expanded later
        dataset_type = 'sales'
        
        # Generate the data
        temp_df = self.generate(dataset_type, rows)
        
        # Save to appropriate format
        if extension == '.csv':
            temp_df.to_csv(filename)
        elif extension == '.json':
            temp_df.to_json(filename)
        else:
            raise ValueError(f"Unsupported file format: {extension}")
    
    def _check_faker(self) -> bool:
        """
        Check if Faker library is available.
        
        Returns:
            True if Faker is available, False otherwise
        """
        try:
            import faker
            return True
        except ImportError:
            return False