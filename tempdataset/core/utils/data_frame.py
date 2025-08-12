"""
TempDataFrame class for data manipulation.

Provides a lightweight alternative to pandas DataFrame with essential data exploration methods.
"""

import csv
import json
import sys
from typing import List, Dict, Any, Tuple, Union
from ..exceptions import ValidationError, CSVWriteError, JSONWriteError


class DisplayFormatter:
    """Helper class to format output for Jupyter/Colab display."""
    
    def __init__(self, content: str):
        self.content = content
    
    def __str__(self) -> str:
        return self.content
    
    def __repr__(self) -> str:
        return self.content
    
    def __eq__(self, other) -> bool:
        """Enable comparison with strings for testing."""
        if isinstance(other, str):
            return self.content == other
        elif isinstance(other, DisplayFormatter):
            return self.content == other.content
        return False
    
    def __contains__(self, item) -> bool:
        """Enable 'in' operator for string searching."""
        return item in self.content
    
    def _repr_html_(self) -> str:
        """HTML representation for Jupyter notebooks."""
        # Convert the text table to a simple HTML table for better display
        lines = self.content.split('\n')
        if not lines:
            return f"<pre>{self.content}</pre>"
        
        # For simple text formatting, just use <pre> tag to preserve spacing
        return f"<pre style='font-family: monospace; white-space: pre;'>{self.content}</pre>"


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
    
    def __len__(self) -> int:
        """
        Return the number of rows in the DataFrame.
        
        Returns:
            Number of rows
        """
        return len(self._data)
    
    def head(self, n: int = 5) -> DisplayFormatter:
        """
        Display first n rows in a readable format.
        
        Args:
            n: Number of rows to display (default: 5)
            
        Returns:
            DisplayFormatter object with formatted representation of the first n rows
            
        Raises:
            ValidationError: If n is not a positive integer
        """
        # Validate input parameter
        if not isinstance(n, int):
            raise ValidationError("n", n, "integer")
        
        if n <= 0:
            raise ValidationError("n", n, "positive integer")
        
        if not self._data:
            result = DisplayFormatter("Empty DataFrame")
        else:
            # Get the first n rows
            rows_to_show = self._data[:n]
            result = DisplayFormatter(self._format_rows(rows_to_show))
        
        # Auto-print in script context
        print(result.content)
        return result
    
    def tail(self, n: int = 5) -> DisplayFormatter:
        """
        Display last n rows in a readable format.
        
        Args:
            n: Number of rows to display (default: 5)
            
        Returns:
            DisplayFormatter object with formatted representation of the last n rows
            
        Raises:
            ValidationError: If n is not a positive integer
        """
        # Validate input parameter
        if not isinstance(n, int):
            raise ValidationError("n", n, "integer")
        
        if n <= 0:
            raise ValidationError("n", n, "positive integer")
        
        if not self._data:
            result = DisplayFormatter("Empty DataFrame")
        else:
            # Get the last n rows
            rows_to_show = self._data[-n:]
            result = DisplayFormatter(self._format_rows(rows_to_show))
        
        # Auto-print in script context
        print(result.content)
        return result
    
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
    
    def describe(self) -> DisplayFormatter:
        """
        Generate descriptive statistics for numeric columns.
        
        Returns:
            DisplayFormatter object with statistical summary
        """
        if not self._data:
            result = DisplayFormatter("Empty DataFrame")
        else:
            # Find numeric columns
            numeric_cols = []
            for col in self._columns:
                # Check if column contains numeric data
                has_numeric = False
                for row in self._data:
                    value = row.get(col)
                    if value is not None and isinstance(value, (int, float)) and not isinstance(value, bool):
                        has_numeric = True
                        break
                if has_numeric:
                    numeric_cols.append(col)
            
            if not numeric_cols:
                result = DisplayFormatter("No numeric columns found")
            else:
                # Calculate statistics for each numeric column
                stats = {}
                for col in numeric_cols:
                    values = []
                    for row in self._data:
                        value = row.get(col)
                        if value is not None and isinstance(value, (int, float)) and not isinstance(value, bool):
                            values.append(float(value))
                    
                    if values:
                        values.sort()
                        n = len(values)
                        
                        # Calculate statistics
                        count = n
                        mean = sum(values) / n
                        std = (sum((x - mean) ** 2 for x in values) / (n - 1)) ** 0.5 if n > 1 else 0.0
                        min_val = min(values)
                        max_val = max(values)
                        
                        # Percentiles
                        q25_idx = int(n * 0.25)
                        q50_idx = int(n * 0.50)
                        q75_idx = int(n * 0.75)
                        
                        q25 = values[q25_idx] if q25_idx < n else values[-1]
                        q50 = values[q50_idx] if q50_idx < n else values[-1]
                        q75 = values[q75_idx] if q75_idx < n else values[-1]
                        
                        stats[col] = {
                            'count': count,
                            'mean': mean,
                            'std': std,
                            'min': min_val,
                            '25%': q25,
                            '50%': q50,
                            '75%': q75,
                            'max': max_val
                        }
                
                if not stats:
                    result = DisplayFormatter("No numeric data found")
                else:
                    # Format output similar to pandas describe()
                    stat_names = ['count', 'mean', 'std', 'min', '25%', '50%', '75%', 'max']
                    
                    # Calculate column widths
                    col_widths = {}
                    for col in numeric_cols:
                        col_widths[col] = max(len(col), 10)  # Minimum width of 10
                    
                    # Create header
                    header_parts = [''.ljust(8)]  # Space for stat names
                    for col in numeric_cols:
                        header_parts.append(col.rjust(col_widths[col]))
                    
                    lines = ['  '.join(header_parts)]
                    
                    # Add statistics rows
                    for stat_name in stat_names:
                        row_parts = [stat_name.ljust(8)]
                        for col in numeric_cols:
                            if col in stats:
                                value = stats[col][stat_name]
                                if stat_name == 'count':
                                    formatted_value = f"{int(value)}"
                                else:
                                    formatted_value = f"{value:.6f}"
                                row_parts.append(formatted_value.rjust(col_widths[col]))
                            else:
                                row_parts.append(''.rjust(col_widths[col]))
                        lines.append('  '.join(row_parts))
                    
                    result = DisplayFormatter('\n'.join(lines))
        
        # Auto-print in script context
        print(result.content)
        return result

    def info(self) -> DisplayFormatter:
        """
        Display dataset information including column types and memory usage.
        
        Returns:
            DisplayFormatter object with dataset information
        """
        if not self._data:
            result = DisplayFormatter("Empty DataFrame")
        else:
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
            
            result = DisplayFormatter("\n".join(info_lines))
        
        # Auto-print in script context
        print(result.content)
        return result
    
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
    
    def memory_usage(self) -> float:
        """
        Get memory usage in megabytes.
        
        Returns:
            Memory usage in MB as a float
        """
        if not self._data:
            return 0.0
        
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
        
        # Return as MB
        return total_bytes / (1024 * 1024)
    
    def filter(self, condition_func) -> 'TempDataFrame':
        """
        Filter rows based on a condition function.
        
        Args:
            condition_func: Function that takes a row dict and returns True/False
            
        Returns:
            New TempDataFrame with filtered rows
            
        Raises:
            ValidationError: If condition_func is not callable
        """
        if not callable(condition_func):
            raise ValidationError("condition_func", condition_func, "callable function")
        
        filtered_data = []
        for row in self._data:
            try:
                if condition_func(row):
                    filtered_data.append(row.copy())
            except Exception as e:
                # Skip rows that cause errors in the condition function
                continue
        
        return TempDataFrame(filtered_data, self._columns.copy())
    
    def select(self, columns: List[str]) -> 'TempDataFrame':
        """
        Select specific columns from the DataFrame.
        
        Args:
            columns: List of column names to select
            
        Returns:
            New TempDataFrame with selected columns only
            
        Raises:
            ValidationError: If columns parameter is invalid or contains non-existent columns
        """
        if not isinstance(columns, list):
            raise ValidationError("columns", columns, "list of strings")
        
        if not all(isinstance(col, str) for col in columns):
            raise ValidationError("columns", columns, "list of strings")
        
        # Check if all requested columns exist
        missing_cols = [col for col in columns if col not in self._columns]
        if missing_cols:
            raise ValidationError("columns", missing_cols, f"columns that exist in DataFrame. Available columns: {self._columns}")
        
        # Create new data with only selected columns
        selected_data = []
        for row in self._data:
            selected_row = {col: row.get(col) for col in columns}
            selected_data.append(selected_row)
        
        return TempDataFrame(selected_data, columns.copy())
    
    def to_dict(self) -> List[Dict[str, Any]]:
        """
        Convert DataFrame to list of dictionaries.
        
        Returns:
            List of dictionaries representing the data
        """
        return [row.copy() for row in self._data]
    
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