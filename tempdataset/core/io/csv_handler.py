"""
CSV file I/O handler.

Handles reading and writing CSV files for the TempDataset library.
"""

import csv
import os
from typing import List, Dict, Any, Optional, Iterator
from pathlib import Path
from ..utils.data_frame import TempDataFrame
from ..exceptions import CSVReadError, CSVWriteError, ValidationError


def read_csv(filename: str, chunk_size: Optional[int] = None) -> TempDataFrame:
    """
    Read CSV file into TempDataFrame.
    
    Args:
        filename: Path to CSV file
        chunk_size: Optional chunk size for streaming large files
        
    Returns:
        TempDataFrame containing the CSV data
        
    Raises:
        ValidationError: If parameters are invalid
        CSVReadError: If the CSV file is malformed or cannot be read
    """
    # Validate input parameters
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if chunk_size is not None:
        if not isinstance(chunk_size, int) or chunk_size <= 0:
            raise ValidationError("chunk_size", chunk_size, "positive integer or None")
    
    file_path = Path(filename)
    
    # Check if file exists
    if not file_path.exists():
        raise CSVReadError(filename, FileNotFoundError(f"No such file or directory: '{filename}'"))
    
    try:
        data = []
        columns = []
        
        with open(file_path, 'r', encoding='utf-8', newline='') as csvfile:
            # Try to detect the CSV dialect
            try:
                sample = csvfile.read(1024)
                csvfile.seek(0)
                dialect = csv.Sniffer().sniff(sample)
            except csv.Error:
                # Fall back to default dialect if detection fails
                dialect = csv.excel
            
            reader = csv.DictReader(csvfile, dialect=dialect)
            
            # Get column names from the first row
            if reader.fieldnames:
                columns = list(reader.fieldnames)
            else:
                raise CSVReadError(filename, Exception("No columns found - file may be empty or malformed"))
            
            # Read data with optional chunking for large files
            if chunk_size:
                data = list(_read_csv_chunks(reader, chunk_size))
            else:
                try:
                    data = list(reader)
                except csv.Error as e:
                    raise CSVReadError(filename, e)
        
        return TempDataFrame(data, columns)
        
    except UnicodeDecodeError as e:
        raise CSVReadError(filename, e)
    except PermissionError as e:
        raise CSVReadError(filename, e)
    except OSError as e:
        raise CSVReadError(filename, e)
    except Exception as e:
        # Catch any other unexpected errors
        if isinstance(e, (ValidationError, CSVReadError)):
            raise  # Re-raise our custom exceptions
        raise CSVReadError(filename, e)


def _read_csv_chunks(reader: csv.DictReader, chunk_size: int) -> Iterator[Dict[str, Any]]:
    """
    Read CSV data in chunks to manage memory usage.
    
    Args:
        reader: CSV DictReader instance
        chunk_size: Number of rows to read at a time
        
    Yields:
        Dictionary representing a row of data
    """
    count = 0
    for row in reader:
        yield row
        count += 1
        if count % chunk_size == 0:
            # This allows for memory management in very large files
            pass


def write_csv(data: List[Dict[str, Any]], filename: str, columns: Optional[List[str]] = None) -> None:
    """
    Write data to CSV file.
    
    Args:
        data: List of dictionaries containing the data
        filename: Path to output CSV file
        columns: Optional list of column names to specify order
        
    Raises:
        ValidationError: If parameters are invalid
        CSVWriteError: If writing fails
    """
    # Validate input parameters
    if not isinstance(data, list):
        raise ValidationError("data", data, "list of dictionaries")
    
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if columns is not None:
        if not isinstance(columns, list):
            raise ValidationError("columns", columns, "list of strings or None")
        if not all(isinstance(col, str) for col in columns):
            raise ValidationError("columns", columns, "list of strings or None")
    
    if not data:
        raise CSVWriteError(filename, Exception("Cannot write empty data to CSV file"))
    
    # Validate that data contains dictionaries
    if not all(isinstance(row, dict) for row in data):
        raise ValidationError("data", data, "list of dictionaries")
    
    file_path = Path(filename)
    
    # Create directory if it doesn't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise CSVWriteError(filename, e)
    
    # Determine columns if not provided
    if columns is None:
        columns = list(data[0].keys()) if data else []
    
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile, 
                fieldnames=columns,
                quoting=csv.QUOTE_MINIMAL,
                escapechar='\\',
                lineterminator='\n'
            )
            
            # Write header
            writer.writeheader()
            
            # Write data rows
            for row in data:
                try:
                    # Filter row to only include specified columns
                    filtered_row = {col: row.get(col, '') for col in columns}
                    writer.writerow(filtered_row)
                except csv.Error as e:
                    raise CSVWriteError(filename, e)
                    
    except PermissionError as e:
        raise CSVWriteError(filename, e)
    except OSError as e:
        raise CSVWriteError(filename, e)
    except Exception as e:
        # Catch any other unexpected errors
        if isinstance(e, (ValidationError, CSVWriteError)):
            raise  # Re-raise our custom exceptions
        raise CSVWriteError(filename, e)


def write_csv_streaming(data_generator: Iterator[Dict[str, Any]], filename: str, columns: List[str]) -> None:
    """
    Write data to CSV file using streaming for large datasets.
    
    Args:
        data_generator: Iterator yielding dictionaries of data
        filename: Path to output CSV file
        columns: List of column names
        
    Raises:
        ValidationError: If parameters are invalid
        CSVWriteError: If writing fails
    """
    # Validate input parameters
    if not hasattr(data_generator, '__iter__'):
        raise ValidationError("data_generator", data_generator, "iterator")
    
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not isinstance(columns, list):
        raise ValidationError("columns", columns, "list of strings")
    
    if not all(isinstance(col, str) for col in columns):
        raise ValidationError("columns", columns, "list of strings")
    
    file_path = Path(filename)
    
    # Create directory if it doesn't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise CSVWriteError(filename, e)
    
    try:
        with open(file_path, 'w', encoding='utf-8', newline='') as csvfile:
            writer = csv.DictWriter(
                csvfile,
                fieldnames=columns,
                quoting=csv.QUOTE_MINIMAL,
                escapechar='\\',
                lineterminator='\n'
            )
            
            # Write header
            writer.writeheader()
            
            # Write data rows from generator
            for row in data_generator:
                try:
                    # Filter row to only include specified columns
                    filtered_row = {col: row.get(col, '') for col in columns}
                    writer.writerow(filtered_row)
                except csv.Error as e:
                    raise CSVWriteError(filename, e)
                    
    except PermissionError as e:
        raise CSVWriteError(filename, e)
    except OSError as e:
        raise CSVWriteError(filename, e)
    except Exception as e:
        # Catch any other unexpected errors
        if isinstance(e, (ValidationError, CSVWriteError)):
            raise  # Re-raise our custom exceptions
        raise CSVWriteError(filename, e)