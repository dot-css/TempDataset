"""
TempDataset Library - Generate temporary datasets for testing and development.

A lightweight Python library for generating realistic sample data without heavy dependencies.
"""

from .core.generator import DataGenerator
from .core.utils.data_frame import TempDataFrame
from .core.io.csv_handler import read_csv as _read_csv
from .core.io.json_handler import read_json as _read_json
from .core.datasets.sales import SalesDataset
from .core.datasets.customers import CustomersDataset
from .core.datasets.ecommerce import EcommerceDataset
from .core.exceptions import (
    TempDatasetError, DatasetNotFoundError, DataGenerationError,
    ValidationError, CSVReadError, CSVWriteError, JSONReadError, JSONWriteError,
    FileOperationError, MemoryError as TempDatasetMemoryError
)

# Initialize the main generator
_generator = DataGenerator()

# Register available datasets
_generator.register_dataset('sales', SalesDataset)
_generator.register_dataset('customers', CustomersDataset)
_generator.register_dataset('ecommerce', EcommerceDataset)

def create_dataset(dataset_type: str, rows: int = 500):
    """
    Generate temporary datasets or save to files.
    
    Args:
        dataset_type: Dataset type ('sales', 'customers', 'ecommerce') or filename ('sales.csv', 'customers.json', 'ecommerce.json')
        rows: Number of rows to generate (default: 500)
        
    Returns:
        TempDataFrame containing the generated data (also saves to file if filename provided)
        
    Raises:
        ValidationError: If parameters are invalid
        DatasetNotFoundError: If dataset type is not available
        DataGenerationError: If data generation fails
        TempDatasetMemoryError: If memory limits are exceeded
        CSVWriteError: If CSV file writing fails
        JSONWriteError: If JSON file writing fails
    """
    # Use the generator's validation and error handling
    return _generator.generate(dataset_type, rows)


def read_csv(filename: str) -> TempDataFrame:
    """
    Read CSV file into TempDataFrame.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        TempDataFrame containing the CSV data
        
    Raises:
        ValidationError: If parameters are invalid
        CSVReadError: If the CSV file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.csv'):
        raise ValidationError("filename", filename, "filename with .csv extension")
    
    # Use the CSV handler's validation and error handling
    return _read_csv(filename)


def read_json(filename: str) -> TempDataFrame:
    """
    Read JSON file into TempDataFrame.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        TempDataFrame containing the JSON data
        
    Raises:
        ValidationError: If parameters are invalid
        JSONReadError: If the JSON file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.json'):
        raise ValidationError("filename", filename, "filename with .json extension")
    
    # Use the JSON handler's validation and error handling
    return _read_json(filename)


def get_performance_stats():
    """
    Get performance statistics from the data generator.
    
    Returns:
        Dictionary with performance statistics including timing and memory usage
    """
    return _generator.get_performance_stats()


def reset_performance_stats():
    """Reset performance monitoring counters."""
    _generator.memory_monitor.reset()
    _generator.profiler = _generator.profiler.__class__()


__version__ = "0.1.0"

# Alias for convenience (matches the library name)
tempdataset = create_dataset

__all__ = ["create_dataset", "tempdataset", "TempDataFrame", "read_csv", "read_json", "get_performance_stats", "reset_performance_stats"]