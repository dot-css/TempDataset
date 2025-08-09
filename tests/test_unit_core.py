"""
Unit tests for core functionality - simplified approach.

Tests TempDataFrame methods, CSV/JSON I/O operations, SalesDataset generation,
and data consistency validation as specified in task 6.1.
"""

import pytest
import tempfile
import os
import json
import re
from datetime import datetime

# Import the library components
import tempdataset
from tempdataset.core.utils.data_frame import TempDataFrame
from tempdataset.core.datasets.sales import SalesDataset
from tempdataset.core.io.csv_handler import read_csv
from tempdataset.core.io.json_handler import read_json
from tempdataset.core.exceptions import ValidationError


class TestTempDataFrameBasics:
    """Test basic TempDataFrame functionality."""
    
    def test_constructor_and_properties(self):
        """Test TempDataFrame constructor and basic properties."""
        data = [
            {"name": "Alice", "age": 25, "salary": 50000.0},
            {"name": "Bob", "age": 30, "salary": 75000.0}
        ]
        columns = ["name", "age", "salary"]
        df = TempDataFrame(data, columns)
        
        # Test basic properties
        assert df.shape == (2, 3)
        assert df.columns == columns
        assert len(df._data) == 2
    
    def test_head_and_tail_methods(self):
        """Test head() and tail() methods."""
        data = [
            {"name": "Alice", "age": 25},
            {"name": "Bob", "age": 30},
            {"name": "Charlie", "age": 35}
        ]
        df = TempDataFrame(data, ["name", "age"])
        
        # Test head
        head_result = df.head(2)
        from tempdataset.core.utils.data_frame import DisplayFormatter
        assert isinstance(head_result, DisplayFormatter)
        head_str = str(head_result)
        assert "Alice" in head_str
        assert "Bob" in head_str
        assert "Charlie" not in head_str
        
        # Test tail
        tail_result = df.tail(2)
        assert isinstance(tail_result, DisplayFormatter)
        tail_str = str(tail_result)
        assert "Bob" in tail_str
        assert "Charlie" in tail_str
        assert "Alice" not in tail_str
    
    def test_info_method(self):
        """Test info() method."""
        data = [
            {"name": "Alice", "age": 25, "salary": 50000.0},
            {"name": "Bob", "age": 30, "salary": 75000.0}
        ]
        df = TempDataFrame(data, ["name", "age", "salary"])
        
        info_result = df.info()
        from tempdataset.core.utils.data_frame import DisplayFormatter
        assert isinstance(info_result, DisplayFormatter)
        info_str = str(info_result)
        assert "TempDataFrame" in info_str
        assert "2 entries" in info_str
        assert "3 columns" in info_str
        assert "memory usage" in info_str
    
    def test_empty_dataframe(self):
        """Test empty DataFrame behavior."""
        df = TempDataFrame([], ["col1", "col2"])
        
        assert df.shape == (0, 2)
        assert df.columns == ["col1", "col2"]
        assert df.head() == "Empty DataFrame"
        assert df.tail() == "Empty DataFrame"
        assert df.info() == "Empty DataFrame"


class TestTempDataFrameFileIO:
    """Test TempDataFrame file I/O operations."""
    
    def test_csv_export_and_import(self):
        """Test CSV export and import cycle."""
        data = [
            {"name": "Alice", "age": 25, "score": 95.5},
            {"name": "Bob", "age": 30, "score": 87.2}
        ]
        columns = ["name", "age", "score"]
        original_df = TempDataFrame(data, columns)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.csv', delete=False) as f:
            temp_file = f.name
        
        try:
            # Export to CSV
            original_df.to_csv(temp_file)
            assert os.path.exists(temp_file)
            
            # Import from CSV
            loaded_df = read_csv(temp_file)
            assert loaded_df.shape == original_df.shape
            assert loaded_df.columns == original_df.columns
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)
    
    def test_json_export_and_import(self):
        """Test JSON export and import cycle."""
        data = [
            {"name": "Alice", "age": 25, "score": 95.5},
            {"name": "Bob", "age": 30, "score": 87.2}
        ]
        columns = ["name", "age", "score"]
        original_df = TempDataFrame(data, columns)
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
            temp_file = f.name
        
        try:
            # Export to JSON
            original_df.to_json(temp_file)
            assert os.path.exists(temp_file)
            
            # Import from JSON
            loaded_df = read_json(temp_file)
            assert loaded_df.shape == original_df.shape
            assert loaded_df.columns == original_df.columns
            
            # Verify data integrity
            loaded_data = loaded_df._data
            assert loaded_data[0]["name"] == "Alice"
            assert loaded_data[0]["age"] == 25
            assert loaded_data[0]["score"] == 95.5
            
        finally:
            if os.path.exists(temp_file):
                os.unlink(temp_file)


class TestSalesDatasetGeneration:
    """Test SalesDataset generation functionality."""
    
    def test_sales_dataset_basic_generation(self):
        """Test basic SalesDataset generation."""
        dataset = SalesDataset(rows=5)
        data = dataset.generate()
        
        # Test row count
        assert len(data) == 5
        
        # Test that each row is a dictionary
        for row in data:
            assert isinstance(row, dict)
            assert len(row) > 0
    
    def test_sales_dataset_required_columns(self):
        """Test that SalesDataset generates required columns."""
        dataset = SalesDataset(rows=3)
        data = dataset.generate()
        
        # Core required columns that should be present
        required_columns = [
            'order_id', 'customer_id', 'customer_name', 'customer_email',
            'product_id', 'product_name', 'category', 'subcategory', 'brand',
            'quantity', 'unit_price', 'total_price', 'discount', 'final_price',
            'order_date', 'ship_date', 'delivery_date', 'sales_rep', 'region',
            'country', 'state/province', 'city', 'postal_code', 'customer_segment',
            'order_priority', 'shipping_mode', 'payment_method', 'customer_age',
            'customer_gender', 'profit'
        ]
        
        for row in data:
            for col in required_columns:
                assert col in row, f"Missing required column: {col}"
    
    def test_sales_dataset_id_formats(self):
        """Test SalesDataset ID format validation."""
        dataset = SalesDataset(rows=3)
        data = dataset.generate()
        
        for row in data:
            # Test order_id format: ORD-YYYY-NNNNNN
            order_id_pattern = r'^ORD-\d{4}-\d{6}$'
            assert re.match(order_id_pattern, row['order_id']), \
                f"Invalid order_id format: {row['order_id']}"
            
            # Test customer_id format: CUST-NNNN
            customer_id_pattern = r'^CUST-\d{4}$'
            assert re.match(customer_id_pattern, row['customer_id']), \
                f"Invalid customer_id format: {row['customer_id']}"
            
            # Test product_id format: PROD-AAANNN
            product_id_pattern = r'^PROD-[A-Z]{3}\d{3}$'
            assert re.match(product_id_pattern, row['product_id']), \
                f"Invalid product_id format: {row['product_id']}"
    
    def test_sales_dataset_data_types(self):
        """Test SalesDataset generates correct data types."""
        dataset = SalesDataset(rows=3)
        data = dataset.generate()
        
        for row in data:
            # String fields
            assert isinstance(row['order_id'], str)
            assert isinstance(row['customer_id'], str)
            assert isinstance(row['customer_name'], str)
            assert isinstance(row['product_name'], str)
            assert isinstance(row['category'], str)
            
            # Integer fields
            assert isinstance(row['quantity'], int)
            assert isinstance(row['customer_age'], int)
            
            # Float fields
            assert isinstance(row['unit_price'], (int, float))
            assert isinstance(row['total_price'], (int, float))
            assert isinstance(row['final_price'], (int, float))
            assert isinstance(row['profit'], (int, float))
            
            # Date fields (stored as strings)
            assert isinstance(row['order_date'], str)
            assert isinstance(row['ship_date'], str)
            assert isinstance(row['delivery_date'], str)
            
            # Validate date format YYYY-MM-DD
            date_pattern = r'^\d{4}-\d{2}-\d{2}$'
            assert re.match(date_pattern, row['order_date'])
            assert re.match(date_pattern, row['ship_date'])
            assert re.match(date_pattern, row['delivery_date'])


class TestDataConsistencyValidation:
    """Test data consistency and relationship validation."""
    
    def test_sales_calculations_consistency(self):
        """Test that sales calculations are mathematically consistent."""
        dataset = SalesDataset(rows=5)
        data = dataset.generate()
        
        for row in data:
            # Test total_price = quantity × unit_price (with reasonable tolerance)
            expected_total = row['quantity'] * row['unit_price']
            assert abs(row['total_price'] - expected_total) < 1.0, \
                f"total_price calculation error: {row['total_price']} vs expected {expected_total}"
            
            # Test final_price = total_price - discount
            expected_final = row['total_price'] - row['discount']
            assert abs(row['final_price'] - expected_final) < 0.01, \
                f"final_price calculation error: {row['final_price']} vs expected {expected_final}"
            
            # Test that values are positive
            assert row['unit_price'] > 0
            assert row['total_price'] > 0
            assert row['final_price'] > 0
            assert row['profit'] > 0
            assert row['discount'] >= 0
    
    def test_date_relationships_consistency(self):
        """Test that date relationships are logically consistent."""
        dataset = SalesDataset(rows=5)
        data = dataset.generate()
        
        for row in data:
            order_date = datetime.strptime(row['order_date'], '%Y-%m-%d')
            ship_date = datetime.strptime(row['ship_date'], '%Y-%m-%d')
            delivery_date = datetime.strptime(row['delivery_date'], '%Y-%m-%d')
            
            # Test chronological order: order_date <= ship_date <= delivery_date
            assert order_date <= ship_date, \
                f"ship_date should be >= order_date: {order_date} vs {ship_date}"
            assert ship_date <= delivery_date, \
                f"delivery_date should be >= ship_date: {ship_date} vs {delivery_date}"
    
    def test_categorical_data_consistency(self):
        """Test that categorical data uses valid predefined values."""
        dataset = SalesDataset(rows=10)
        data = dataset.generate()
        
        # Get expected values from dataset
        expected_regions = dataset.regions
        expected_segments = dataset.customer_segments
        expected_priorities = dataset.order_priorities
        expected_shipping_modes = dataset.shipping_modes
        expected_payment_methods = dataset.payment_methods
        expected_genders = dataset.genders
        expected_categories = list(dataset.categories.keys())
        
        for row in data:
            # Test that categorical values are from predefined lists
            assert row['region'] in expected_regions
            assert row['customer_segment'] in expected_segments
            assert row['order_priority'] in expected_priorities
            assert row['shipping_mode'] in expected_shipping_modes
            assert row['payment_method'] in expected_payment_methods
            assert row['customer_gender'] in expected_genders
            assert row['category'] in expected_categories
            
            # Test subcategory is valid for the category
            expected_subcategories = dataset.categories[row['category']]
            assert row['subcategory'] in expected_subcategories
    
    def test_numeric_ranges_consistency(self):
        """Test that numeric values are within reasonable ranges."""
        dataset = SalesDataset(rows=10)
        data = dataset.generate()
        
        for row in data:
            # Test quantity range (should be positive and reasonable)
            assert 1 <= row['quantity'] <= 20
            
            # Test customer age range
            assert 18 <= row['customer_age'] <= 80
            
            # Test that prices are positive
            assert row['unit_price'] > 0
            assert row['total_price'] > 0
            assert row['final_price'] > 0
            assert row['profit'] > 0
            
            # Test discount is reasonable (non-negative and not more than total)
            assert row['discount'] >= 0
            assert row['discount'] <= row['total_price']
    
    def test_email_format_consistency(self):
        """Test that email addresses have valid format."""
        dataset = SalesDataset(rows=5)
        data = dataset.generate()
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        
        for row in data:
            assert re.match(email_pattern, row['customer_email']), \
                f"Invalid email format: {row['customer_email']}"


class TestMainAPIIntegration:
    """Test main API integration."""
    
    def test_tempdataset_function_basic(self):
        """Test basic tempdataset() function usage."""
        # Test dataset generation
        df = tempdataset.create_dataset('sales', rows=5)
        assert isinstance(df, TempDataFrame)
        assert df.shape[0] == 5  # 5 rows
        assert df.shape[1] > 0   # Has columns
    
    def test_tempdataset_file_output(self):
        """Test tempdataset() function with file output."""
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_csv = f.name
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_json = f.name
        
        try:
            # Test CSV output
            result = tempdataset.create_dataset(temp_csv, rows=3)
            assert isinstance(result, TempDataFrame)  # Now returns TempDataFrame
            assert os.path.exists(temp_csv)
            
            # Test JSON output
            result = tempdataset.create_dataset(temp_json, rows=3)
            assert isinstance(result, TempDataFrame)  # Now returns TempDataFrame
            assert os.path.exists(temp_json)
            
        finally:
            for temp_file in [temp_csv, temp_json]:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)
    
    def test_read_functions(self):
        """Test read_csv() and read_json() functions."""
        # Create test data
        data = [{"name": "Alice", "age": 25}, {"name": "Bob", "age": 30}]
        df = TempDataFrame(data, ["name", "age"])
        
        with tempfile.NamedTemporaryFile(suffix='.csv', delete=False) as f:
            temp_csv = f.name
        
        with tempfile.NamedTemporaryFile(suffix='.json', delete=False) as f:
            temp_json = f.name
        
        try:
            # Export data
            df.to_csv(temp_csv)
            df.to_json(temp_json)
            
            # Test read functions
            csv_df = tempdataset.read_csv(temp_csv)
            json_df = tempdataset.read_json(temp_json)
            
            assert isinstance(csv_df, TempDataFrame)
            assert isinstance(json_df, TempDataFrame)
            assert csv_df.shape == (2, 2)
            assert json_df.shape == (2, 2)
            
        finally:
            for temp_file in [temp_csv, temp_json]:
                if os.path.exists(temp_file):
                    os.unlink(temp_file)


if __name__ == "__main__":
    pytest.main([__file__, "-v"])