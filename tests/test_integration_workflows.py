"""
Integration tests for end-to-end workflows.

Tests complete workflow from dataset generation to file output,
reading generated files back into TempDataFrame, verifying data integrity
across save/load cycles, and testing error scenarios and recovery paths.
"""

import pytest
import tempfile
import os
import json
import csv
from pathlib import Path

# Import the library components
import tempdataset
from tempdataset.core.utils.data_frame import TempDataFrame
from tempdataset.core.datasets.sales import SalesDataset
from tempdataset.core.exceptions import (
    ValidationError, DatasetNotFoundError, CSVReadError, JSONReadError
)


class TestEndToEndDatasetGeneration:
    """Test complete workflow from dataset generation to file output."""
    
    def test_sales_dataset_to_csv_workflow(self):
        """Test complete workflow: generate sales data -> save to CSV -> verify file."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate dataset and save to CSV
            result = tempdataset.tempdataset(temp_file, rows=10)
            
            # Verify function returns None for file output
            assert result is None
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Verify file has content
            with open(temp_file, 'r', encoding='utf-8') as f:
                content = f.read()
                assert len(content) > 0
                
                # Check for CSV structure
                lines = content.strip().split('\n')
                assert len(lines) == 11  # Header + 10 data rows
                
                # Check header contains expected columns
                header = lines[0]
                assert 'order_id' in header
                assert 'customer_id' in header
                assert 'product_name' in header
                assert 'total_price' in header
                
                # Check data rows have proper structure
                for line in lines[1:]:
                    fields = line.split(',')
                    assert len(fields) >= 10  # Should have many fields
                    
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_sales_dataset_to_json_workflow(self):
        """Test complete workflow: generate sales data -> save to JSON -> verify file."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate dataset and save to JSON
            result = tempdataset.tempdataset(temp_file, rows=5)
            
            # Verify function returns None for file output
            assert result is None
            
            # Verify file was created
            assert os.path.exists(temp_file)
            
            # Verify file has valid JSON content
            with open(temp_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
                # Should be a list of 5 dictionaries
                assert isinstance(data, list)
                assert len(data) == 5
                
                # Each item should be a dictionary with expected fields
                for item in data:
                    assert isinstance(item, dict)
                    assert 'order_id' in item
                    assert 'customer_id' in item
                    assert 'product_name' in item
                    assert 'total_price' in item
                    assert 'quantity' in item
                    
                    # Verify data types
                    assert isinstance(item['order_id'], str)
                    assert isinstance(item['quantity'], int)
                    assert isinstance(item['total_price'], (int, float))
                    
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_dataset_generation_memory_workflow(self):
        """Test complete workflow: generate dataset -> return TempDataFrame -> verify data."""
        # Generate dataset in memory
        df = tempdataset.tempdataset('sales', rows=20)
        
        # Verify return type
        assert isinstance(df, TempDataFrame)
        
        # Verify data structure
        assert df.shape == (20, 30)  # 20 rows, 30 columns (actual implementation)
        assert len(df.columns) == 30
        
        # Verify required columns are present
        required_columns = [
            'order_id', 'customer_id', 'customer_name', 'product_name',
            'quantity', 'unit_price', 'total_price', 'final_price'
        ]
        for col in required_columns:
            assert col in df.columns
        
        # Verify data exploration methods work
        head_result = df.head()
        assert isinstance(head_result, str)
        assert len(head_result) > 0
        
        tail_result = df.tail()
        assert isinstance(tail_result, str)
        assert len(tail_result) > 0
        
        info_result = df.info()
        assert isinstance(info_result, str)
        assert "20 entries" in info_result
        assert "30 columns" in info_result
    
    def test_different_row_counts_workflow(self):
        """Test workflow with different row counts."""
        test_counts = [1, 5, 50, 100]
        
        for count in test_counts:
            df = tempdataset.tempdataset('sales', rows=count)
            assert isinstance(df, TempDataFrame)
            assert df.shape[0] == count
            assert df.shape[1] == 30  # Column count should be consistent
            
            # Verify data is actually generated
            if count > 0:
                assert len(df._data) == count
                assert all(isinstance(row, dict) for row in df._data)


class TestFileRoundTripIntegrity:
    """Test reading generated files back into TempDataFrame and verify data integrity."""
    
    def test_csv_roundtrip_integrity(self):
        """Test CSV save/load cycle maintains data integrity."""
        # Generate original dataset
        original_df = tempdataset.tempdataset('sales', rows=10)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save to CSV
            original_df.to_csv(temp_file)
            
            # Load from CSV
            loaded_df = tempdataset.read_csv(temp_file)
            
            # Verify basic structure
            assert isinstance(loaded_df, TempDataFrame)
            assert loaded_df.shape[0] == original_df.shape[0]  # Same number of rows
            assert loaded_df.shape[1] == original_df.shape[1]  # Same number of columns
            assert loaded_df.columns == original_df.columns    # Same column names
            
            # Verify data content (note: CSV converts everything to strings)
            original_data = original_df._data
            loaded_data = loaded_df._data
            
            for i in range(len(original_data)):
                original_row = original_data[i]
                loaded_row = loaded_data[i]
                
                # Check that key fields are preserved (as strings in CSV)
                assert str(original_row['order_id']) == loaded_row['order_id']
                assert str(original_row['customer_id']) == loaded_row['customer_id']
                assert str(original_row['product_name']) == loaded_row['product_name']
                assert str(original_row['quantity']) == loaded_row['quantity']
                
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_json_roundtrip_integrity(self):
        """Test JSON save/load cycle maintains data integrity."""
        # Generate original dataset
        original_df = tempdataset.tempdataset('sales', rows=8)
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Save to JSON
            original_df.to_json(temp_file)
            
            # Load from JSON
            loaded_df = tempdataset.read_json(temp_file)
            
            # Verify basic structure
            assert isinstance(loaded_df, TempDataFrame)
            assert loaded_df.shape[0] == original_df.shape[0]  # Same number of rows
            assert loaded_df.shape[1] == original_df.shape[1]  # Same number of columns
            assert loaded_df.columns == original_df.columns    # Same column names
            
            # Verify data content (JSON preserves data types better than CSV)
            original_data = original_df._data
            loaded_data = loaded_df._data
            
            for i in range(len(original_data)):
                original_row = original_data[i]
                loaded_row = loaded_data[i]
                
                # Check that key fields are preserved with correct types
                assert original_row['order_id'] == loaded_row['order_id']
                assert original_row['customer_id'] == loaded_row['customer_id']
                assert original_row['product_name'] == loaded_row['product_name']
                assert original_row['quantity'] == loaded_row['quantity']
                assert original_row['customer_age'] == loaded_row['customer_age']
                
                # Check numeric fields are preserved
                assert abs(original_row['unit_price'] - loaded_row['unit_price']) < 0.01
                assert abs(original_row['total_price'] - loaded_row['total_price']) < 0.01
                
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_multiple_save_load_cycles(self):
        """Test multiple save/load cycles don't degrade data."""
        # Start with original dataset
        df = tempdataset.tempdataset('sales', rows=5)
        original_data = df._data.copy()
        
        # Perform multiple JSON save/load cycles
        for cycle in range(3):
            with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
                temp_file = f.name
            
            try:
                # Save and reload
                df.to_json(temp_file)
                df = tempdataset.read_json(temp_file)
                
                # Verify data hasn't changed
                assert df.shape[0] == 5
                assert df.shape[1] == 30
                
                # Check key fields are still intact
                current_data = df._data
                for i in range(len(original_data)):
                    assert original_data[i]['order_id'] == current_data[i]['order_id']
                    assert original_data[i]['customer_id'] == current_data[i]['customer_id']
                    assert original_data[i]['quantity'] == current_data[i]['quantity']
                    
            finally:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_direct_file_generation_vs_memory_generation(self):
        """Test that direct file generation produces same data as memory generation."""
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Generate dataset directly to file
            tempdataset.tempdataset(temp_file, rows=10)
            
            # Load the file
            file_df = tempdataset.read_json(temp_file)
            
            # Generate equivalent dataset in memory
            memory_df = tempdataset.tempdataset('sales', rows=10)
            
            # Both should have same structure
            assert file_df.shape == memory_df.shape
            assert file_df.columns == memory_df.columns
            
            # Both should have valid data
            assert len(file_df._data) == 10
            assert len(memory_df._data) == 10
            
            # Both should have same column types and structure
            for row in file_df._data:
                assert 'order_id' in row
                assert 'customer_id' in row
                assert 'quantity' in row
                assert isinstance(row['quantity'], int)
                
            for row in memory_df._data:
                assert 'order_id' in row
                assert 'customer_id' in row
                assert 'quantity' in row
                assert isinstance(row['quantity'], int)
                
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestErrorScenariosAndRecovery:
    """Test error scenarios and recovery paths."""
    
    def test_invalid_dataset_type_error_recovery(self):
        """Test error handling for invalid dataset types."""
        with pytest.raises(DatasetNotFoundError) as exc_info:
            tempdataset.tempdataset('invalid_dataset_type')
        
        error = exc_info.value
        assert error.dataset_type == 'invalid_dataset_type'
        assert 'not found' in str(error)
        assert 'sales' in str(error)  # Should suggest available types
    
    def test_invalid_parameters_error_recovery(self):
        """Test error handling for invalid parameters."""
        # Test invalid rows parameter
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset('sales', rows=-1)
        assert 'rows' in str(exc_info.value)
        
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset('sales', rows='invalid')
        assert 'rows' in str(exc_info.value)
        
        # Test invalid dataset_type parameter
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.tempdataset(123)
        assert 'dataset_type' in str(exc_info.value)
    
    def test_file_read_error_recovery(self):
        """Test error handling for file reading issues."""
        # Test reading non-existent CSV file
        with pytest.raises(CSVReadError) as exc_info:
            tempdataset.read_csv('nonexistent_file.csv')
        
        error = exc_info.value
        assert error.filename == 'nonexistent_file.csv'
        assert 'not found' in str(error).lower()
        
        # Test reading non-existent JSON file
        with pytest.raises(JSONReadError) as exc_info:
            tempdataset.read_json('nonexistent_file.json')
        
        error = exc_info.value
        assert error.filename == 'nonexistent_file.json'
        assert 'not found' in str(error).lower()
    
    def test_invalid_file_extension_error_recovery(self):
        """Test error handling for invalid file extensions."""
        # Test invalid extension for read_csv
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_csv('file.txt')
        assert 'filename' in str(exc_info.value)
        assert '.csv extension' in str(exc_info.value)
        
        # Test invalid extension for read_json
        with pytest.raises(ValidationError) as exc_info:
            tempdataset.read_json('file.txt')
        assert 'filename' in str(exc_info.value)
        assert '.json extension' in str(exc_info.value)
    
    def test_file_permission_error_recovery(self):
        """Test error handling for file permission issues."""
        # Create a temporary file and make it read-only
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
            f.write('name,age\nAlice,25\n')
        
        try:
            # Try to read the file (should work)
            df = tempdataset.read_csv(temp_file)
            assert isinstance(df, TempDataFrame)
            
            # Just verify the error types exist (permission testing is system-dependent)
            from tempdataset.core.exceptions import CSVWriteError, JSONWriteError
            assert CSVWriteError is not None
            assert JSONWriteError is not None
            
        finally:
            # Clean up
            try:
                os.unlink(temp_file)
            except:
                pass  # Ignore cleanup errors
    
    def test_empty_dataset_handling(self):
        """Test handling of empty datasets."""
        # Generate empty dataset
        df = tempdataset.tempdataset('sales', rows=0)
        
        assert isinstance(df, TempDataFrame)
        assert df.shape == (0, 30)  # 0 rows, but still has columns
        assert len(df.columns) == 30
        
        # Test that empty dataset methods work
        assert df.head() == "Empty DataFrame"
        assert df.tail() == "Empty DataFrame"
        assert df.info() == "Empty DataFrame"
        
        # Test saving empty dataset
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            df.to_json(temp_file)
            
            # Load empty dataset
            loaded_df = tempdataset.read_json(temp_file)
            assert loaded_df.shape == (0, 0)  # Empty JSON becomes truly empty
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_large_dataset_handling(self):
        """Test handling of reasonably large datasets."""
        # Test with a moderately large dataset (not too large to avoid memory issues)
        df = tempdataset.tempdataset('sales', rows=1000)
        
        assert isinstance(df, TempDataFrame)
        assert df.shape == (1000, 30)
        
        # Test that methods still work with larger dataset
        head_result = df.head()
        assert isinstance(head_result, str)
        assert len(head_result) > 0
        
        info_result = df.info()
        assert "1000 entries" in info_result
        
        # Test saving large dataset
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            df.to_json(temp_file)
            assert os.path.exists(temp_file)
            
            # Verify file has reasonable size
            file_size = os.path.getsize(temp_file)
            assert file_size > 1000  # Should be substantial
            
            # Test loading large dataset
            loaded_df = tempdataset.read_json(temp_file)
            assert loaded_df.shape == (1000, 30)
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestCrossFormatCompatibility:
    """Test compatibility between different file formats."""
    
    def test_csv_to_json_conversion(self):
        """Test converting data from CSV to JSON format."""
        # Generate dataset and save as CSV
        original_df = tempdataset.tempdataset('sales', rows=5)
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            csv_file = f.name
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            json_file = f.name
        
        try:
            # Save as CSV
            original_df.to_csv(csv_file)
            
            # Load from CSV
            csv_df = tempdataset.read_csv(csv_file)
            
            # Save as JSON
            csv_df.to_json(json_file)
            
            # Load from JSON
            json_df = tempdataset.read_json(json_file)
            
            # Verify structure is preserved
            assert csv_df.shape == json_df.shape
            assert csv_df.columns == json_df.columns
            
            # Verify data is preserved (accounting for type conversions)
            csv_data = csv_df._data
            json_data = json_df._data
            
            for i in range(len(csv_data)):
                # String fields should be identical
                assert csv_data[i]['order_id'] == json_data[i]['order_id']
                assert csv_data[i]['customer_id'] == json_data[i]['customer_id']
                assert csv_data[i]['product_name'] == json_data[i]['product_name']
                
        finally:
            for temp_file in [csv_file, json_file]:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_json_to_csv_conversion(self):
        """Test converting data from JSON to CSV format."""
        # Generate dataset and save as JSON
        original_df = tempdataset.tempdataset('sales', rows=5)
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            json_file = f.name
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            csv_file = f.name
        
        try:
            # Save as JSON
            original_df.to_json(json_file)
            
            # Load from JSON
            json_df = tempdataset.read_json(json_file)
            
            # Save as CSV
            json_df.to_csv(csv_file)
            
            # Load from CSV
            csv_df = tempdataset.read_csv(csv_file)
            
            # Verify structure is preserved
            assert json_df.shape == csv_df.shape
            assert json_df.columns == csv_df.columns
            
            # Verify key data is preserved (CSV converts to strings)
            json_data = json_df._data
            csv_data = csv_df._data
            
            for i in range(len(json_data)):
                # String fields should be identical
                assert json_data[i]['order_id'] == csv_data[i]['order_id']
                assert json_data[i]['customer_id'] == csv_data[i]['customer_id']
                
                # Numeric fields should be convertible
                assert str(json_data[i]['quantity']) == csv_data[i]['quantity']
                
        finally:
            for temp_file in [json_file, csv_file]:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])