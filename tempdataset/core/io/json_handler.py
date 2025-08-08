"""
JSON file I/O handler.

Handles reading and writing JSON files for the TempDataset library.
"""

import json
import os
from typing import List, Dict, Any, Optional, Iterator, Union
from pathlib import Path
from ..utils.data_frame import TempDataFrame


class JSONError(Exception):
    """Base exception for JSON operations."""
    pass


class JSONReadError(JSONError):
    """Exception raised when JSON reading fails."""
    pass


class JSONWriteError(JSONError):
    """Exception raised when JSON writing fails."""
    pass


def read_json(filename: str, lines: bool = False) -> TempDataFrame:
    """
    Read JSON file into TempDataFrame.
    
    Args:
        filename: Path to JSON file
        lines: If True, treat as line-delimited JSON (JSONL)
        
    Returns:
        TempDataFrame containing the JSON data
        
    Raises:
        FileNotFoundError: If the file doesn't exist
        JSONReadError: If the JSON file is malformed or cannot be read
    """
    file_path = Path(filename)
    
    # Check if file exists
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {filename}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            if lines:
                data = _read_jsonl(jsonfile, filename)
            else:
                data = _read_json_array(jsonfile, filename)
        
        # Extract columns from the first row if data exists
        columns = list(data[0].keys()) if data else []
        
        return TempDataFrame(data, columns)
        
    except UnicodeDecodeError as e:
        raise JSONReadError(f"Encoding error reading JSON file {filename}: {str(e)}")
    except PermissionError:
        raise JSONReadError(f"Permission denied reading JSON file: {filename}")
    except OSError as e:
        raise JSONReadError(f"OS error reading JSON file {filename}: {str(e)}")


def _read_json_array(jsonfile, filename: str) -> List[Dict[str, Any]]:
    """
    Read JSON file as array of objects.
    
    Args:
        jsonfile: Open file object
        filename: Filename for error messages
        
    Returns:
        List of dictionaries representing the data
        
    Raises:
        JSONReadError: If JSON parsing fails
    """
    try:
        content = json.load(jsonfile)
        
        if isinstance(content, list):
            # Validate that all items are dictionaries
            for i, item in enumerate(content):
                if not isinstance(item, dict):
                    raise JSONReadError(f"Item {i} in JSON array is not an object in file: {filename}")
            return content
        elif isinstance(content, dict):
            # Single object, wrap in list
            return [content]
        else:
            raise JSONReadError(f"JSON file must contain an array of objects or a single object: {filename}")
            
    except json.JSONDecodeError as e:
        raise JSONReadError(f"Invalid JSON in file {filename}: {str(e)}")


def _read_jsonl(jsonfile, filename: str) -> List[Dict[str, Any]]:
    """
    Read line-delimited JSON file.
    
    Args:
        jsonfile: Open file object
        filename: Filename for error messages
        
    Returns:
        List of dictionaries representing the data
        
    Raises:
        JSONReadError: If JSON parsing fails
    """
    data = []
    line_number = 0
    
    for line in jsonfile:
        line_number += 1
        line = line.strip()
        
        if not line:  # Skip empty lines
            continue
            
        try:
            obj = json.loads(line)
            if not isinstance(obj, dict):
                raise JSONReadError(f"Line {line_number} is not a JSON object in file: {filename}")
            data.append(obj)
        except json.JSONDecodeError as e:
            raise JSONReadError(f"Invalid JSON on line {line_number} in file {filename}: {str(e)}")
    
    return data


def write_json(data: List[Dict[str, Any]], filename: str, lines: bool = False, indent: Optional[int] = 2) -> None:
    """
    Write data to JSON file.
    
    Args:
        data: List of dictionaries containing the data
        filename: Path to output JSON file
        lines: If True, write as line-delimited JSON (JSONL)
        indent: Indentation for pretty printing (ignored for JSONL)
        
    Raises:
        JSONWriteError: If writing fails
    """
    if not isinstance(data, list):
        raise JSONWriteError("Data must be a list of dictionaries")
    
    file_path = Path(filename)
    
    # Create directory if it doesn't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise JSONWriteError(f"Cannot create directory for JSON file {filename}: {str(e)}")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            if lines:
                _write_jsonl(data, jsonfile, filename)
            else:
                _write_json_array(data, jsonfile, filename, indent)
                
    except PermissionError:
        raise JSONWriteError(f"Permission denied writing to JSON file: {filename}")
    except OSError as e:
        raise JSONWriteError(f"OS error writing JSON file {filename}: {str(e)}")


def _write_json_array(data: List[Dict[str, Any]], jsonfile, filename: str, indent: Optional[int]) -> None:
    """
    Write data as JSON array.
    
    Args:
        data: List of dictionaries
        jsonfile: Open file object
        filename: Filename for error messages
        indent: Indentation level
        
    Raises:
        JSONWriteError: If writing fails
    """
    try:
        json.dump(data, jsonfile, indent=indent, ensure_ascii=False, separators=(',', ': '))
    except (TypeError, ValueError) as e:
        raise JSONWriteError(f"Error serializing data to JSON file {filename}: {str(e)}")


def _write_jsonl(data: List[Dict[str, Any]], jsonfile, filename: str) -> None:
    """
    Write data as line-delimited JSON.
    
    Args:
        data: List of dictionaries
        jsonfile: Open file object
        filename: Filename for error messages
        
    Raises:
        JSONWriteError: If writing fails
    """
    for i, row in enumerate(data):
        try:
            json_line = json.dumps(row, ensure_ascii=False, separators=(',', ':'))
            jsonfile.write(json_line + '\n')
        except (TypeError, ValueError) as e:
            raise JSONWriteError(f"Error serializing row {i} to JSON in file {filename}: {str(e)}")


def write_json_streaming(data_generator: Iterator[Dict[str, Any]], filename: str, lines: bool = True) -> None:
    """
    Write data to JSON file using streaming for large datasets.
    
    Args:
        data_generator: Iterator yielding dictionaries of data
        filename: Path to output JSON file
        lines: If True, write as line-delimited JSON (recommended for streaming)
        
    Raises:
        JSONWriteError: If writing fails
    """
    if not lines:
        raise JSONWriteError("Streaming JSON writing only supports line-delimited format (lines=True)")
    
    file_path = Path(filename)
    
    # Create directory if it doesn't exist
    try:
        file_path.parent.mkdir(parents=True, exist_ok=True)
    except OSError as e:
        raise JSONWriteError(f"Cannot create directory for JSON file {filename}: {str(e)}")
    
    try:
        with open(file_path, 'w', encoding='utf-8') as jsonfile:
            for i, row in enumerate(data_generator):
                try:
                    json_line = json.dumps(row, ensure_ascii=False, separators=(',', ':'))
                    jsonfile.write(json_line + '\n')
                except (TypeError, ValueError) as e:
                    raise JSONWriteError(f"Error serializing row {i} to JSON in file {filename}: {str(e)}")
                    
    except PermissionError:
        raise JSONWriteError(f"Permission denied writing to JSON file: {filename}")
    except OSError as e:
        raise JSONWriteError(f"OS error writing JSON file {filename}: {str(e)}")


def detect_json_format(filename: str) -> str:
    """
    Detect whether a JSON file is array format or line-delimited format.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        'array' for standard JSON array, 'lines' for line-delimited JSON
        
    Raises:
        JSONReadError: If file cannot be read or format cannot be determined
    """
    file_path = Path(filename)
    
    if not file_path.exists():
        raise FileNotFoundError(f"JSON file not found: {filename}")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as jsonfile:
            # Read first few characters to detect format
            first_char = jsonfile.read(1)
            if not first_char:
                raise JSONReadError(f"Empty JSON file: {filename}")
            
            if first_char == '[':
                return 'array'
            elif first_char == '{':
                return 'lines'
            else:
                raise JSONReadError(f"Unrecognized JSON format in file: {filename}")
                
    except UnicodeDecodeError as e:
        raise JSONReadError(f"Encoding error reading JSON file {filename}: {str(e)}")
    except OSError as e:
        raise JSONReadError(f"OS error reading JSON file {filename}: {str(e)}")