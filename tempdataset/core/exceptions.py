"""
Custom exception classes for the TempDataset library.

Provides specific exception types for different error scenarios with helpful messages.
"""


class TempDatasetError(Exception):
    """Base exception class for all TempDataset library errors."""
    pass


class DatasetNotFoundError(TempDatasetError):
    """Raised when a requested dataset type is not available."""
    
    def __init__(self, dataset_type: str, available_types: list):
        self.dataset_type = dataset_type
        self.available_types = available_types
        message = (
            f"Dataset type '{dataset_type}' not found. "
            f"Available types: {available_types}. "
            f"Suggestion: Check spelling or register a custom dataset."
        )
        super().__init__(message)


class DataGenerationError(TempDatasetError):
    """Raised when data generation fails."""
    
    def __init__(self, message: str, dataset_type: str = None, rows: int = None):
        self.dataset_type = dataset_type
        self.rows = rows
        
        full_message = f"Data generation failed: {message}"
        if dataset_type:
            full_message += f" (Dataset: {dataset_type}"
            if rows is not None:
                full_message += f", Rows: {rows}"
            full_message += ")"
        
        super().__init__(full_message)


class FileOperationError(TempDatasetError):
    """Base class for file operation errors."""
    
    def __init__(self, message: str, filename: str = None):
        self.filename = filename
        
        full_message = message
        if filename:
            full_message += f" (File: {filename})"
        
        super().__init__(full_message)


class CSVReadError(FileOperationError):
    """Raised when CSV file reading fails."""
    
    def __init__(self, filename: str, original_error: Exception = None):
        self.original_error = original_error
        
        message = f"Failed to read CSV file: {filename}. "
        
        if original_error:
            if "No such file or directory" in str(original_error):
                message += "File not found. Please check the file path exists."
            elif "Permission denied" in str(original_error):
                message += "Permission denied. Please check file permissions."
            elif "Invalid" in str(original_error) or "malformed" in str(original_error).lower():
                message += "File appears to be malformed. Please check CSV format."
            else:
                message += f"Error details: {str(original_error)}"
        
        message += " Suggestion: Ensure the file exists and is a valid CSV format."
        
        super().__init__(message, filename)


class CSVWriteError(FileOperationError):
    """Raised when CSV file writing fails."""
    
    def __init__(self, filename: str, original_error: Exception = None):
        self.original_error = original_error
        
        message = f"Failed to write CSV file: {filename}. "
        
        if original_error:
            if "Permission denied" in str(original_error):
                message += "Permission denied. Please check directory permissions."
            elif "No space left" in str(original_error):
                message += "Insufficient disk space."
            elif "No such file or directory" in str(original_error):
                message += "Directory does not exist."
            else:
                message += f"Error details: {str(original_error)}"
        
        message += " Suggestion: Ensure the directory exists and you have write permissions."
        
        super().__init__(message, filename)


class JSONReadError(FileOperationError):
    """Raised when JSON file reading fails."""
    
    def __init__(self, filename: str, original_error: Exception = None):
        self.original_error = original_error
        
        message = f"Failed to read JSON file: {filename}. "
        
        if original_error:
            if "No such file or directory" in str(original_error):
                message += "File not found. Please check the file path exists."
            elif "Permission denied" in str(original_error):
                message += "Permission denied. Please check file permissions."
            elif "JSON" in str(original_error) or "decode" in str(original_error).lower():
                message += "File contains invalid JSON. Please check JSON format."
            else:
                message += f"Error details: {str(original_error)}"
        
        message += " Suggestion: Ensure the file exists and contains valid JSON."
        
        super().__init__(message, filename)


class JSONWriteError(FileOperationError):
    """Raised when JSON file writing fails."""
    
    def __init__(self, filename: str, original_error: Exception = None):
        self.original_error = original_error
        
        message = f"Failed to write JSON file: {filename}. "
        
        if original_error:
            if "Permission denied" in str(original_error):
                message += "Permission denied. Please check directory permissions."
            elif "No space left" in str(original_error):
                message += "Insufficient disk space."
            elif "No such file or directory" in str(original_error):
                message += "Directory does not exist."
            else:
                message += f"Error details: {str(original_error)}"
        
        message += " Suggestion: Ensure the directory exists and you have write permissions."
        
        super().__init__(message, filename)


class ValidationError(TempDatasetError):
    """Raised when input validation fails."""
    
    def __init__(self, parameter: str, value, expected_type: str = None, additional_info: str = None):
        self.parameter = parameter
        self.value = value
        self.expected_type = expected_type
        
        message = f"Invalid value for parameter '{parameter}': {repr(value)}"
        
        if expected_type:
            message += f". Expected {expected_type}"
        
        if additional_info:
            message += f". {additional_info}"
        
        # Add suggestions based on common validation errors
        if parameter == "rows":
            message += " Suggestion: Use a positive integer (e.g., rows=1000)."
        elif parameter == "dataset_type":
            message += " Suggestion: Use a valid dataset name (e.g., 'sales') or filename (e.g., 'data.csv')."
        elif parameter == "filename":
            message += " Suggestion: Provide a valid file path with appropriate extension."
        
        super().__init__(message)


class MemoryError(TempDatasetError):
    """Raised when memory limits are exceeded."""
    
    def __init__(self, requested_rows: int, estimated_memory_mb: float = None):
        self.requested_rows = requested_rows
        self.estimated_memory_mb = estimated_memory_mb
        
        message = f"Memory limit exceeded for {requested_rows:,} rows"
        
        if estimated_memory_mb:
            message += f" (estimated {estimated_memory_mb:.1f} MB required)"
        
        message += ". Suggestions: "
        message += "1) Reduce the number of rows, "
        message += "2) Use file output instead of in-memory generation, "
        message += "3) Process data in smaller batches."
        
        super().__init__(message)


class PerformanceWarning(UserWarning):
    """Warning for performance-related issues."""
    pass


class DependencyWarning(UserWarning):
    """Warning for missing optional dependencies."""
    pass