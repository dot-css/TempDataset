"""
TempDataset Library - Generate temporary datasets for testing and development.

A lightweight Python library for generating realistic sample data without heavy dependencies.
"""

from .core.generator import DataGenerator
from .core.utils.data_frame import TempDataFrame
from .core.io.csv_handler import read_csv as _read_csv
from .core.io.json_handler import read_json as _read_json
from .core.datasets.sales import SalesDataset

# Initialize the main generator
_generator = DataGenerator()

# Register available datasets
_generator.register_dataset('sales', SalesDataset)

def tempdataset(dataset_type: str, rows: int = 500):
    """
    Generate temporary datasets or save to files.
    
    Args:
        dataset_type: Dataset type ('sales') or filename ('sales.csv', 'sales.json')
        rows: Number of rows to generate (default: 500)
        
    Returns:
        TempDataFrame for dataset types, None for file outputs
        
    Raises:
        ValueError: If dataset_type is invalid or rows is negative
        TypeError: If parameters are not of expected types
    """
    # Parameter validation
    if not isinstance(dataset_type, str):
        raise TypeError("dataset_type must be a string")
    
    if not isinstance(rows, int):
        raise TypeError("rows must be an integer")
    
    if rows < 0:
        raise ValueError("rows must be non-negative")
    
    if not dataset_type.strip():
        raise ValueError("dataset_type cannot be empty")
    
    # Detect file extensions and validate supported formats
    if dataset_type.endswith('.csv') or dataset_type.endswith('.json'):
        # Validate file extension
        supported_extensions = ['.csv', '.json']
        extension = '.' + dataset_type.split('.')[-1]
        if extension not in supported_extensions:
            raise ValueError(f"Unsupported file format: {extension}. Supported formats: {supported_extensions}")
    
    try:
        return _generator.generate(dataset_type, rows)
    except Exception as e:
        # Re-raise with more context if needed
        if "not found" in str(e):
            available_datasets = list(_generator.datasets.keys())
            raise ValueError(f"Dataset type '{dataset_type}' not found. Available types: {available_datasets}") from e
        raise


def read_csv(filename: str) -> TempDataFrame:
    """
    Read CSV file into TempDataFrame.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        TempDataFrame containing the CSV data
        
    Raises:
        TypeError: If filename is not a string
        ValueError: If filename is empty
        FileNotFoundError: If the file doesn't exist
        CSVReadError: If the CSV file is malformed or cannot be read
    """
    # Parameter validation
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    
    if not filename.strip():
        raise ValueError("filename cannot be empty")
    
    # Validate file extension
    if not filename.lower().endswith('.csv'):
        raise ValueError("filename must have .csv extension")
    
    try:
        return _read_csv(filename)
    except Exception as e:
        # Provide more helpful error messages
        if isinstance(e, FileNotFoundError):
            raise FileNotFoundError(f"CSV file not found: {filename}. Please check the file path.") from e
        raise


def read_json(filename: str) -> TempDataFrame:
    """
    Read JSON file into TempDataFrame.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        TempDataFrame containing the JSON data
        
    Raises:
        TypeError: If filename is not a string
        ValueError: If filename is empty
        FileNotFoundError: If the file doesn't exist
        JSONReadError: If the JSON file is malformed or cannot be read
    """
    # Parameter validation
    if not isinstance(filename, str):
        raise TypeError("filename must be a string")
    
    if not filename.strip():
        raise ValueError("filename cannot be empty")
    
    # Validate file extension
    if not filename.lower().endswith('.json'):
        raise ValueError("filename must have .json extension")
    
    try:
        return _read_json(filename)
    except Exception as e:
        # Provide more helpful error messages
        if isinstance(e, FileNotFoundError):
            raise FileNotFoundError(f"JSON file not found: {filename}. Please check the file path.") from e
        raise


__version__ = "0.1.0"
__all__ = ["tempdataset", "TempDataFrame", "read_csv", "read_json"]