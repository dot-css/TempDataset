"""
TempDataFrame class for data manipulation.

Provides a lightweight alternative to pandas DataFrame with essential data exploration methods.
"""

import csv
import json
import sys
from typing import List, Dict, Any, Tuple, Union
from ..exceptions import ValidationError, CSVWriteError, JSONWriteError


class TempDataFrame:
    """
    Lightweight DataFrame-like class for data manipulation and exploration.
    
    Provides essential methods for working with tabular data without pandas dependency.
    """
    
    def __init__(self, data: List[Dict[str, Any]], columns: List[str]):
        """
        Initialize TempDataFrame.
        
        Args:
            data: List of dictionaries representing rows
            columns: List of column names
            
        Raises:
            ValidationError: If parameters are invalid
        """
        # Validate input parameters
        if not isinstance(data, list):
            raise ValidationError("data", data, "list of dictionaries")
        
        if not isinstance(columns, list):
            raise ValidationError("columns", columns, "list of strings")
        
        if not all(isinstance(col, str) for col in columns):
            raise ValidationError("columns", columns, "list of strings")
        
        # Validate that data contains dictionaries (if not empty)
        if data and not all(isinstance(row, dict) for row in data):
            raise ValidationError("data", data, "list of dictionaries")
        
        self._data = data
        self._columns = columns
    
    def head(self, n: int = 5) -> str:
        """
        Display first n rows in a readable format.
        
        Args:
            n: Number of rows to display (default: 5)
            
        Returns:
            Formatted string representation of the first n rows
            
        Raises:
            ValidationError: If n is not a positive integer
        """
        # Validate input parameter
        if not isinstance(n, int):
            raise ValidationError("n", n, "integer")
        
        if n <= 0:
            raise ValidationError("n", n, "positive integer")
        
        if not self._data:
            return "Empty DataFrame"
        
        # Get the first n rows
        rows_to_show = self._data[:n]
        
        return self._format_rows(rows_to_show)
    
    def tail(self, n: int = 5) -> str:
        """
        Display last n rows in a readable format.
        
        Args:
            n: Number of rows to display (default: 5)
            
        Returns:
            Formatted string representation of the last n rows
            
        Raises:
            ValidationError: If n is not a positive integer
        """
        # Validate input parameter
        if not isinstance(n, int):
            raise ValidationError("n", n, "integer")
        
        if n <= 0:
            raise ValidationError("n", n, "positive integer")
        
        if not self._data:
            return "Empty DataFrame"
        
        # Get the last n rows
        rows_to_show = self._data[-n:]
        
        return self._format_rows(rows_to_show)
    
    @property
    def shape(self) -> Tuple[int, int]:
        """
        Return (rows, columns) tuple.
        
        Returns:
            Tuple containing number of rows and columns
        """
        return (len(self._data), len(self._columns))
    
    @property
    def columns(self) -> List[str]:
        """
        Return column names.
        
        Returns:
            List of column names
        """
        return self._columns.copy()
    
    def info(self) -> str:
        """
        Display dataset information including column types and memory usage.
        
        Returns:
            Formatted string with dataset information
        """
        if not self._data:
            return "Empty DataFrame"
        
        rows, cols = self.shape
        
        # Calculate column types and non-null counts
        column_info = []
        for col in self._columns:
            non_null_count = sum(1 for row in self._data if row.get(col) is not None)
            
            # Determine data type from first non-null value
            dtype = "object"
            for row in self._data:
                value = row.get(col)
                if value is not None:
                    if isinstance(value, int):
                        dtype = "int64"
                    elif isinstance(value, float):
                        dtype = "float64"
                    elif isinstance(value, bool):
                        dtype = "bool"
                    elif isinstance(value, str):
                        dtype = "object"
                    break
            
            column_info.append({
                'column': col,
                'non_null': non_null_count,
                'dtype': dtype
            })
        
        # Calculate approximate memory usage
        memory_usage = self._estimate_memory_usage()
        
        # Format output
        info_lines = [
            f"<class 'tempdataset.core.utils.data_frame.TempDataFrame'>",
            f"RangeIndex: {rows} entries, 0 to {rows-1}" if rows > 0 else "RangeIndex: 0 entries",
            f"Data columns (total {cols} columns):"
        ]
        
        # Add column information
        info_lines.append(" #   Column" + " " * 15 + "Non-Null Count  Dtype")
        info_lines.append("---  ------" + " " * 15 + "--------------  -----")
        
        for i, col_info in enumerate(column_info):
            col_name = col_info['column'][:20]  # Truncate long column names
            info_lines.append(f" {i:<3} {col_name:<20} {col_info['non_null']} non-null    {col_info['dtype']}")
        
        info_lines.append(f"dtypes: {self._get_dtype_counts()}")
        info_lines.append(f"memory usage: {memory_usage}")
        
        return "\n".join(info_lines)
    
    def to_csv(self, filename: str) -> None:
        """
        Export to CSV file.
        
        Args:
            filename: Path to output CSV file
            
        Raises:
            ValidationError: If filename is invalid
            CSVWriteError: If CSV writing fails
        """
        # Validate input parameter
        if not isinstance(filename, str):
            raise ValidationError("filename", filename, "string")
        
        if not filename.strip():
            raise ValidationError("filename", filename, "non-empty string")
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                if not self._data:
                    # Write just headers for empty DataFrame
                    writer = csv.writer(csvfile)
                    writer.writerow(self._columns)
                    return
                
                writer = csv.DictWriter(csvfile, fieldnames=self._columns)
                writer.writeheader()
                writer.writerows(self._data)
                
        except PermissionError as e:
            raise CSVWriteError(filename, e)
        except OSError as e:
            raise CSVWriteError(filename, e)
        except Exception as e:
            # Catch any other unexpected errors
            if isinstance(e, (ValidationError, CSVWriteError)):
                raise  # Re-raise our custom exceptions
            raise CSVWriteError(filename, e)
    
    def to_json(self, filename: str) -> None:
        """
        Export to JSON file.
        
        Args:
            filename: Path to output JSON file
            
        Raises:
            ValidationError: If filename is invalid
            JSONWriteError: If JSON writing fails
        """
        # Validate input parameter
        if not isinstance(filename, str):
            raise ValidationError("filename", filename, "string")
        
        if not filename.strip():
            raise ValidationError("filename", filename, "non-empty string")
        
        try:
            with open(filename, 'w', encoding='utf-8') as jsonfile:
                json.dump(self._data, jsonfile, indent=2, default=str)
                
        except PermissionError as e:
            raise JSONWriteError(filename, e)
        except OSError as e:
            raise JSONWriteError(filename, e)
        except (TypeError, ValueError) as e:
            raise JSONWriteError(filename, e)
        except Exception as e:
            # Catch any other unexpected errors
            if isinstance(e, (ValidationError, JSONWriteError)):
                raise  # Re-raise our custom exceptions
            raise JSONWriteError(filename, e)
    
    def _format_rows(self, rows: List[Dict[str, Any]]) -> str:
        """
        Format rows for display.
        
        Args:
            rows: List of row dictionaries to format
            
        Returns:
            Formatted string representation
        """
        if not rows:
            return "Empty DataFrame"
        
        # Calculate column widths
        col_widths = {}
        for col in self._columns:
            # Start with column name width
            col_widths[col] = len(col)
            
            # Check data widths
            for row in rows:
                value_str = str(row.get(col, ''))
                col_widths[col] = max(col_widths[col], len(value_str))
            
            # Set minimum and maximum widths
            col_widths[col] = max(col_widths[col], 3)  # Minimum width
            col_widths[col] = min(col_widths[col], 20)  # Maximum width for readability
        
        # Create header
        header_parts = []
        separator_parts = []
        
        for col in self._columns:
            width = col_widths[col]
            header_parts.append(col.ljust(width))
            separator_parts.append('-' * width)
        
        lines = [
            '  '.join(header_parts),
            '  '.join(separator_parts)
        ]
        
        # Add data rows
        for i, row in enumerate(rows):
            row_parts = []
            for col in self._columns:
                value = row.get(col, '')
                value_str = str(value)
                
                # Truncate if too long
                if len(value_str) > col_widths[col]:
                    value_str = value_str[:col_widths[col]-3] + '...'
                
                row_parts.append(value_str.ljust(col_widths[col]))
            
            lines.append('  '.join(row_parts))
        
        return '\n'.join(lines)
    
    def _estimate_memory_usage(self) -> str:
        """
        Estimate memory usage of the DataFrame.
        
        Returns:
            Human-readable memory usage string
        """
        if not self._data:
            return "0 bytes"
        
        # Rough estimation based on Python object sizes
        total_bytes = 0
        
        # Base object overhead
        total_bytes += sys.getsizeof(self._data)
        total_bytes += sys.getsizeof(self._columns)
        
        # Data content
        for row in self._data:
            total_bytes += sys.getsizeof(row)
            for value in row.values():
                total_bytes += sys.getsizeof(value)
        
        # Convert to human readable format
        if total_bytes < 1024:
            return f"{total_bytes} bytes"
        elif total_bytes < 1024 * 1024:
            return f"{total_bytes / 1024:.1f} KB"
        else:
            return f"{total_bytes / (1024 * 1024):.1f} MB"
    
    def _get_dtype_counts(self) -> str:
        """
        Get counts of different data types.
        
        Returns:
            String describing data type distribution
        """
        if not self._data:
            return "no data"
        
        dtype_counts = {}
        
        for col in self._columns:
            # Determine data type from first non-null value
            dtype = "object"
            for row in self._data:
                value = row.get(col)
                if value is not None:
                    if isinstance(value, int):
                        dtype = "int64"
                    elif isinstance(value, float):
                        dtype = "float64"
                    elif isinstance(value, bool):
                        dtype = "bool"
                    elif isinstance(value, str):
                        dtype = "object"
                    break
            
            dtype_counts[dtype] = dtype_counts.get(dtype, 0) + 1
        
        # Format as "type(count), type(count), ..."
        parts = [f"{dtype}({count})" for dtype, count in sorted(dtype_counts.items())]
        return ", ".join(parts)