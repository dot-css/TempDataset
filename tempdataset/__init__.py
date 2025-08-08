"""
TempDataset Library - Generate temporary datasets for testing and development.

A lightweight Python library for generating realistic sample data without heavy dependencies.
"""

from .core.generator import DataGenerator
from .core.utils.data_frame import TempDataFrame
from .core.io.csv_handler import read_csv
from .core.io.json_handler import read_json

# Initialize the main generator
_generator = DataGenerator()

def tempdataset(dataset_type: str, rows: int = 500):
    """
    Generate temporary datasets or save to files.
    
    Args:
        dataset_type: Dataset type ('sales') or filename ('sales.csv', 'sales.json')
        rows: Number of rows to generate (default: 500)
        
    Returns:
        TempDataFrame for dataset types, None for file outputs
    """
    return _generator.generate(dataset_type, rows)

__version__ = "0.1.0"
__all__ = ["tempdataset", "TempDataFrame", "read_csv", "read_json"]