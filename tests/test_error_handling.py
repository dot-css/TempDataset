"""
Test error handling and validation functionality.

Tests custom exceptions and input validation across the library.
"""

import pytest
import tempfile
import os
from pathlib import Path

# Import the library and exceptions
import tempdataset
from tempdataset.core.exceptions import (
    TempDatasetError, DatasetNotFoundError, DataGenerationError,
    ValidationError, CSVReadError, CSVWriteError, JSONReadError, JSONWriteError,
    FileOperationError, MemoryError as TempDatasetMemoryError
)
from tempdataset.core.utils.data_frame import TempDataFrame


class TestValidationErrors:
    """Test input validation and ValidationError exceptions."""
    
    def test_tempdataset_invalid_dataset_type(self):
        """Test ValidationError for invalid dataset_type parameter."""
        # Test non-string dataset_type
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset(123)
        assert "dataset_type" in str(exc_info.value)
        assert "string" in str(exc_info.value)
        
        # Test empty dataset_type
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset("")
        assert "dataset_type" in str(exc_info.value)
        assert "non-empty string" in str(exc_info.value)
    
    def test_tempdataset_invalid_rows(self):
        """Test ValidationError for invalid rows parameter."""
        # Test non-integer rows
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset("sales", rows="100")
        assert "rows" in str(exc_info.value)
        assert "integer" in str(exc_info.value)
        
        # Test negative rows
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset("sales", rows=-5)
        assert "rows" in str(exc_info.value)
        assert "non-negative integer" in str(exc_info.value)
    
    def test_read_csv_invalid_filename(self):
        """Test ValidationError for invalid filename in read_csv."""
        # Test non-string filename
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_csv(123)
        assert "filename" in str(exc_info.value)
        assert "string" in str(exc_info.value)
        
        # Test empty filename
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_csv("")
        assert "filename" in str(exc_info.value)
        assert "non-empty string" in str(exc_info.value)
        
        # Test invalid extension
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_csv("data.txt")
        assert "filename" in str(exc_info.value)
        assert ".csv extension" in str(exc_info.value)
    
    def test_read_json_invalid_filename(self):
        """Test ValidationError for invalid filename in read_json."""
        # Test non-string filename
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_json(123)
        assert "filename" in str(exc_info.value)
        assert "string" in str(exc_info.value)
        
        # Test empty filename
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_json("")
        assert "filename" in str(exc_info.value)
        assert "non-empty string" in str(exc_info.value)
        
        # Test invalid extension
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_json("data.txt")
        assert "filename" in str(exc_info.value)
        assert ".json extension" in str(exc_info.value)
    
    def test_tempdf_invalid_constructor_params(self):
        """Test ValidationError for invalid TempDataFrame constructor parameters."""
        # Test non-list data
        with pytest.raises(ValidationError) as exc_info:
            TempDataFrame("not a list", ["col1"])
        assert "data" in str(exc_info.value)
        assert "list of dictionaries" in str(exc_info.value)
        
        # Test non-list columns
        with pytest.raises(ValidationError) as exc_info:
            TempDataFrame([], "not a list")
        assert "columns" in str(exc_info.value)
        assert "list of strings" in str(exc_info.value)
        
        # Test non-string columns
        with pytest.raises(ValidationError) as exc_info:
            TempDataFrame([], [1, 2, 3])
        assert "columns" in str(exc_info.value)
        assert "list of strings" in str(exc_info.value)
        
        # Test non-dict data items
        with pytest.raises(ValidationError) as exc_info:
            TempDataFrame([1, 2, 3], ["col1"])
        assert "data" in str(exc_info.value)
        assert "list of dictionaries" in str(exc_info.value)
    
    def test_tempdf_head_tail_invalid_n(self):
        """Test ValidationError for invalid n parameter in head/tail methods."""
        df = TempDataFrame([{"col1": "value1"}], ["col1"])
        
        # Test non-integer n
        with pytest.raises(ValidationError) as exc_info:
            df.head("5")
        assert "n" in str(exc_info.value)
        assert "integer" in str(exc_info.value)
        
        # Test non-positive n
        with pytest.raises(ValidationError) as exc_info:
            df.head(0)
        assert "n" in str(exc_info.value)
        assert "positive integer" in str(exc_info.value)
        
        # Same for tail
        with pytest.raises(ValidationError) as exc_info:
            df.tail(-1)
        assert "n" in str(exc_info.value)
        assert "positive integer" in str(exc_info.value)


class TestDatasetNotFoundError:
    """Test DatasetNotFoundError exceptions."""
    
    def test_invalid_dataset_type(self):
        """Test DatasetNotFoundError for unknown dataset types."""
        with pytest.raises(DatasetNotFoundError) as exc_info:
            tempdataset.tempdataset("unknown_dataset")
        
        error = exc_info.value
        assert error.dataset_type == "unknown_dataset"
        assert "sales" in str(error.available_types)
        assert "not found" in str(error)
        assert "Available types" in str(error)


class TestFileOperationErrors:
    """Test file operation error handling."""
    
    def test_csv_read_file_not_found(self):
        """Test CSVReadError for non-existent files."""
        with pytest.raises(CSVReadError) as exc_info:
            tempdataset.read_csv("nonexistent.csv")
        
        error = exc_info.value
        assert error.filename == "nonexistent.csv"
        assert "not found" in str(error).lower()
    
    def test_json_read_file_not_found(self):
        """Test JSONReadError for non-existent files."""
        with pytest.raises(JSONReadError) as exc_info:
            tempdataset.read_json("nonexistent.json")
        
        error = exc_info.value
        assert error.filename == "nonexistent.json"
        assert "not found" in str(error).lower()
    
    def test_csv_read_malformed_file(self):
        """Test CSVReadError for malformed CSV files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            # Write malformed CSV (unclosed quotes)
            f.write('col1,col2\n"unclosed quote,value2\n')
            temp_file = f.name
        
        try:
            with pytest.raises(CSVReadError) as exc_info:
                tempdataset.read_csv(temp_file)
            
            error = exc_info.value
            assert error.filename == temp_file
            assert "malformed" in str(error).lower() or "error" in str(error).lower()
        finally:
            os.unlink(temp_file)
    
    def test_json_read_malformed_file(self):
        """Test JSONReadError for malformed JSON files."""
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            # Write malformed JSON
            f.write('{"key": "value",}')  # Trailing comma
            temp_file = f.name
        
        try:
            with pytest.raises(JSONReadError) as exc_info:
                tempdataset.read_json(temp_file)
            
            error = exc_info.value
            assert error.filename == temp_file
            assert "json" in str(error).lower() or "decode" in str(error).lower()
        finally:
            os.unlink(temp_file)


class TestMemoryError:
    """Test memory limit error handling."""
    
    def test_memory_limit_exceeded(self):
        """Test TempDatasetMemoryError for very large datasets."""
        # Try to generate a dataset that would exceed memory limits
        # This should trigger the memory check in the generator
        with pytest.raises(TempDatasetMemoryError) as exc_info:
            tempdataset.tempdataset("sales", rows=1000000)  # 1 million rows
        
        error = exc_info.value
        assert error.requested_rows == 1000000
        assert "memory limit exceeded" in str(error).lower()
        assert "suggestions" in str(error).lower()


class TestErrorMessages:
    """Test that error messages are helpful and descriptive."""
    
    def test_validation_error_suggestions(self):
        """Test that ValidationError provides helpful suggestions."""
        # Test rows parameter suggestion
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset("sales", rows=-1)
        assert "positive integer" in str(exc_info.value)
        assert "rows=1000" in str(exc_info.value)
        
        # Test dataset_type parameter suggestion
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset("")
        assert "dataset name" in str(exc_info.value) or "filename" in str(exc_info.value)
    
    def test_dataset_not_found_suggestions(self):
        """Test that DatasetNotFoundError provides helpful suggestions."""
        with pytest.raises(DatasetNotFoundError) as exc_info:
            tempdataset.tempdataset("invalid")
        
        error_msg = str(exc_info.value)
        assert "not found" in error_msg
        assert "Available types" in error_msg
        assert "sales" in error_msg
        assert "spelling" in error_msg or "register" in error_msg
    
    def test_file_operation_error_suggestions(self):
        """Test that file operation errors provide helpful suggestions."""
        with pytest.raises(CSVReadError) as exc_info:
            tempdataset.read_csv("missing.csv")
        
        error_msg = str(exc_info.value)
        assert "not found" in error_msg.lower()
        assert "check" in error_msg.lower()
        assert "path" in error_msg.lower()
    
    def test_memory_error_suggestions(self):
        """Test that MemoryError provides helpful suggestions."""
        with pytest.raises(TempDatasetMemoryError) as exc_info:
            tempdataset.tempdataset("sales", rows=1000000)
        
        error_msg = str(exc_info.value)
        assert "suggestions" in error_msg.lower()
        assert "reduce" in error_msg.lower()
        assert "file output" in error_msg.lower()
        assert "batches" in error_msg.lower()


class TestErrorHierarchy:
    """Test that custom exceptions follow proper inheritance hierarchy."""
    
    def test_exception_inheritance(self):
        """Test that all custom exceptions inherit from TempDatasetError."""
        # Test that specific exceptions are instances of base exception
        try:
            tempdataset.tempdataset("invalid")
        except DatasetNotFoundError as e:
            assert isinstance(e, TempDatasetError)
        
        try:
            tempdataset.tempdataset("sales", rows=-1)
        except ValidationError as e:
            assert isinstance(e, TempDatasetError)
        
        try:
            tempdataset.read_csv("missing.csv")
        except CSVReadError as e:
            assert isinstance(e, FileOperationError)
            assert isinstance(e, TempDatasetError)


if __name__ == "__main__":
    pytest.main([__file__])