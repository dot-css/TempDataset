"""
Test cases for the retail dataset functionality.

Tests the RetailDataset class and its integration with the main TempDataset library.
"""

import pytest
import tempfile
import os
from datetime import datetime

import tempdataset
from tempdataset.core.datasets.retail import RetailDataset
from tempdataset.core.exceptions import ValidationError


class TestRetailDataset:
    """Test cases for RetailDataset class."""
    
    def test_retail_dataset_initialization(self):
        """Test RetailDataset initialization."""
        dataset = RetailDataset(100)
        assert dataset.rows == 100
        assert dataset.seed is None
    
    def test_retail_dataset_generate_basic(self):
        """Test basic data generation."""
        dataset = RetailDataset(10)
        data = dataset.generate()
        
        assert isinstance(data, list)
        assert len(data) == 10
        assert all(isinstance(row, dict) for row in data)
    
    def test_retail_dataset_required_columns(self):
        """Test that all required columns are present."""
        dataset = RetailDataset(5)
        data = dataset.generate()
        
        expected_columns = [
            'transaction_id', 'store_id', 'store_name', 'store_type',
            'location_city', 'location_state_province', 'location_country',
            'pos_terminal_id', 'cashier_id', 'cashier_name', 'transaction_datetime',
            'product_id', 'product_name', 'category', 'subcategory', 'brand',
            'quantity', 'unit_price', 'total_price', 'discount_percentage',
            'discount_amount', 'final_price', 'payment_method', 'loyalty_member',
            'loyalty_points_earned', 'transaction_status', 'inventory_before_sale',
            'inventory_after_sale', 'supplier_id', 'gross_margin', 'receipt_number',
            'shift_id', 'notes'
        ]
        
        for row in data:
            for column in expected_columns:
                assert column in row, f"Missing column: {column}"
    
    def test_retail_dataset_unique_ids(self):
        """Test that transaction IDs and receipt numbers are unique."""
        dataset = RetailDataset(20)
        data = dataset.generate()
        
        transaction_ids = [row['transaction_id'] for row in data]
        receipt_numbers = [row['receipt_number'] for row in data]
        
        assert len(set(transaction_ids)) == len(transaction_ids), "Transaction IDs should be unique"
        assert len(set(receipt_numbers)) == len(receipt_numbers), "Receipt numbers should be unique"
    
    def test_retail_dataset_id_format(self):
        """Test ID format validation."""
        dataset = RetailDataset(5)
        data = dataset.generate()
        
        for row in data:
            # Test transaction ID format: POS-YYYY-NNNNNN
            assert row['transaction_id'].startswith('POS-')
            assert len(row['transaction_id']) == 15  # POS-YYYY-NNNNNN
            
            # Test store ID format: STORE-NNN
            assert row['store_id'].startswith('STORE-')
            assert len(row['store_id']) == 9  # STORE-NNN
            
            # Test POS terminal ID format: POS-NN
            assert row['pos_terminal_id'].startswith('POS-')
            assert len(row['pos_terminal_id']) == 6  # POS-NN
            
            # Test cashier ID format: CASH-NNNN
            assert row['cashier_id'].startswith('CASH-')
            assert len(row['cashier_id']) == 9  # CASH-NNNN
            
            # Test product ID format: PROD-AAANNN
            assert row['product_id'].startswith('PROD-')
            assert len(row['product_id']) == 11  # PROD-AAANNN
            
            # Test supplier ID format: SUPP-NNNN
            assert row['supplier_id'].startswith('SUPP-')
            assert len(row['supplier_id']) == 9  # SUPP-NNNN
            
            # Test receipt number format: RCPT-NNNNNN
            assert row['receipt_number'].startswith('RCPT-')
            assert len(row['receipt_number']) == 11  # RCPT-NNNNNN
    
    def test_retail_dataset_data_types(self):
        """Test data types of generated columns."""
        dataset = RetailDataset(5)
        data = dataset.generate()
        
        for row in data:
            # String columns
            string_columns = [
                'transaction_id', 'store_id', 'store_name', 'store_type',
                'location_city', 'location_state_province', 'location_country',
                'pos_terminal_id', 'cashier_id', 'cashier_name', 'transaction_datetime',
                'product_id', 'product_name', 'category', 'subcategory', 'brand',
                'payment_method', 'transaction_status', 'supplier_id', 'receipt_number',
                'shift_id'
            ]
            for col in string_columns:
                assert isinstance(row[col], str), f"Column {col} should be string"
            
            # Integer columns
            integer_columns = [
                'quantity', 'loyalty_points_earned', 'inventory_before_sale', 'inventory_after_sale'
            ]
            for col in integer_columns:
                assert isinstance(row[col], int), f"Column {col} should be integer"
            
            # Float columns
            float_columns = [
                'unit_price', 'total_price', 'discount_percentage', 'discount_amount',
                'final_price', 'gross_margin'
            ]
            for col in float_columns:
                assert isinstance(row[col], (int, float)), f"Column {col} should be numeric"
            
            # Boolean columns
            assert isinstance(row['loyalty_member'], bool), "loyalty_member should be boolean"
            
            # Notes can be string or None
            assert row['notes'] is None or isinstance(row['notes'], str), "notes should be string or None"
    
    def test_retail_dataset_price_calculations(self):
        """Test price calculation logic."""
        dataset = RetailDataset(10)
        data = dataset.generate()
        
        for row in data:
            # Test total price calculation
            expected_total = row['quantity'] * row['unit_price']
            assert abs(row['total_price'] - expected_total) < 0.01, "Total price calculation error"
            
            # Test discount amount calculation
            expected_discount = row['total_price'] * row['discount_percentage'] / 100
            assert abs(row['discount_amount'] - expected_discount) < 0.01, "Discount amount calculation error"
            
            # Test final price calculation
            expected_final = row['total_price'] - row['discount_amount']
            assert abs(row['final_price'] - expected_final) < 0.01, "Final price calculation error"
    
    def test_retail_dataset_inventory_logic(self):
        """Test inventory before/after sale logic."""
        dataset = RetailDataset(20)
        data = dataset.generate()
        
        for row in data:
            # Inventory before sale should be >= quantity
            assert row['inventory_before_sale'] >= row['quantity'], "Not enough inventory for sale"
            
            # Check inventory after sale based on transaction status
            if row['transaction_status'] == 'Completed':
                expected_after = row['inventory_before_sale'] - row['quantity']
                assert row['inventory_after_sale'] == expected_after, "Inventory after sale calculation error"
            else:
                # For cancelled/refunded transactions, inventory should remain the same
                assert row['inventory_after_sale'] == row['inventory_before_sale'], "Inventory should not change for cancelled/refunded transactions"
    
    def test_retail_dataset_loyalty_points_logic(self):
        """Test loyalty points logic."""
        dataset = RetailDataset(20)
        data = dataset.generate()
        
        for row in data:
            if row['loyalty_member'] and row['transaction_status'] == 'Completed':
                # Loyalty members with completed transactions should earn points
                assert row['loyalty_points_earned'] >= 0, "Loyalty points should be non-negative"
            else:
                # Non-members or non-completed transactions should not earn points
                assert row['loyalty_points_earned'] == 0, "Non-members or cancelled transactions should not earn points"
    
    def test_retail_dataset_shift_logic(self):
        """Test shift ID logic based on transaction time."""
        dataset = RetailDataset(10)
        data = dataset.generate()
        
        for row in data:
            # Parse transaction datetime to check shift logic
            dt = datetime.strptime(row['transaction_datetime'], '%Y-%m-%d %H:%M:%S')
            hour = dt.hour
            
            if 6 <= hour < 14:
                assert row['shift_id'] == 'SHIFT-AM-001', "Morning shift should be SHIFT-AM-001"
            elif 14 <= hour < 22:
                assert row['shift_id'] == 'SHIFT-PM-002', "Afternoon shift should be SHIFT-PM-002"
            else:
                assert row['shift_id'] == 'SHIFT-NIGHT-004', "Night shift should be SHIFT-NIGHT-004"
    
    def test_retail_dataset_enum_values(self):
        """Test that categorical columns contain valid values."""
        dataset = RetailDataset(50)
        data = dataset.generate()
        
        valid_store_types = ['Supermarket', 'Department Store', 'Convenience Store', 'Specialty Store']
        valid_categories = ['Electronics', 'Grocery', 'Clothing', 'Home', 'Beauty', 'Sports']
        valid_payment_methods = ['Cash', 'Credit Card', 'Debit Card', 'Mobile Payment', 'Gift Card']
        valid_transaction_statuses = ['Completed', 'Cancelled', 'Refunded']
        
        for row in data:
            assert row['store_type'] in valid_store_types, f"Invalid store type: {row['store_type']}"
            assert row['category'] in valid_categories, f"Invalid category: {row['category']}"
            assert row['payment_method'] in valid_payment_methods, f"Invalid payment method: {row['payment_method']}"
            assert row['transaction_status'] in valid_transaction_statuses, f"Invalid transaction status: {row['transaction_status']}"
    
    def test_retail_dataset_schema(self):
        """Test dataset schema method."""
        dataset = RetailDataset(1)
        schema = dataset.get_schema()
        
        assert isinstance(schema, dict)
        assert len(schema) == 33  # Should have 33 columns
        
        # Check some key schema entries
        assert schema['transaction_id'] == 'string'
        assert schema['quantity'] == 'integer'
        assert schema['unit_price'] == 'float'
        assert schema['loyalty_member'] == 'boolean'
        assert schema['transaction_datetime'] == 'datetime'
    
    def test_retail_dataset_reproducibility(self):
        """Test that setting seed produces reproducible results."""
        dataset1 = RetailDataset(10)
        dataset1.set_seed(42)
        data1 = dataset1.generate()
        
        dataset2 = RetailDataset(10)
        dataset2.set_seed(42)
        data2 = dataset2.generate()
        
        # Should generate identical data with same seed
        assert data1 == data2, "Same seed should produce identical results"


class TestRetailDatasetIntegration:
    """Test retail dataset integration with main TempDataset library."""
    
    def test_retail_dataset_creation(self):
        """Test retail dataset creation through main API."""
        data = tempdataset.create_dataset('retail', rows=10)
        
        assert data is not None
        assert len(data) == 10
        assert len(data.columns) == 33
    
    def test_retail_file_export(self):
        """Test retail dataset file export."""
        with tempfile.TemporaryDirectory() as temp_dir:
            # Test CSV export
            csv_file = os.path.join(temp_dir, 'retail_test.csv')
            data_csv = tempdataset.create_dataset(csv_file, rows=5)
            assert os.path.exists(csv_file)
            assert len(data_csv) == 5
            
            # Test JSON export
            json_file = os.path.join(temp_dir, 'retail_test.json')
            data_json = tempdataset.create_dataset(json_file, rows=5)
            assert os.path.exists(json_file)
            assert len(data_json) == 5
    
    def test_retail_tempdataset_integration(self):
        """Test retail dataset with tempdataset alias."""
        data = tempdataset.tempdataset('retail', rows=15)
        
        assert data is not None
        assert len(data) == 15
        assert 'transaction_id' in data.columns
        assert 'store_name' in data.columns
        assert 'product_name' in data.columns
    
    def test_retail_data_variety(self):
        """Test that retail dataset generates variety in data."""
        data = tempdataset.create_dataset('retail', rows=100)
        
        # Check variety in categories
        categories = set(row['category'] for row in data._data)
        store_types = set(row['store_type'] for row in data._data)
        payment_methods = set(row['payment_method'] for row in data._data)
        
        # Should have multiple categories, store types, and payment methods
        assert len(categories) >= 3, "Should have variety in categories"
        assert len(store_types) >= 2, "Should have variety in store types"
        assert len(payment_methods) >= 3, "Should have variety in payment methods"
    
    def test_retail_data_consistency(self):
        """Test data consistency across retail dataset."""
        data = tempdataset.create_dataset('retail', rows=50)
        
        for row in data._data:
            # All required fields should be present and non-empty
            assert row['transaction_id'], "Transaction ID should not be empty"
            assert row['store_name'], "Store name should not be empty"
            assert row['product_name'], "Product name should not be empty"
            assert row['cashier_name'], "Cashier name should not be empty"
            
            # Numeric fields should be positive
            assert row['quantity'] > 0, "Quantity should be positive"
            assert row['unit_price'] > 0, "Unit price should be positive"
            assert row['total_price'] > 0, "Total price should be positive"
            assert row['final_price'] >= 0, "Final price should be non-negative"
            
            # Discount percentage should be within valid range
            assert 0 <= row['discount_percentage'] <= 50, "Discount percentage should be 0-50%"
    
    def test_retail_data_ranges(self):
        """Test that retail data falls within expected ranges."""
        data = tempdataset.create_dataset('retail', rows=30)
        
        for row in data._data:
            # Quantity should be reasonable
            assert 1 <= row['quantity'] <= 20, "Quantity should be 1-20"
            
            # Loyalty points should be reasonable
            assert 0 <= row['loyalty_points_earned'] <= 500, "Loyalty points should be 0-500"
            
            # Gross margin should be reasonable percentage of final price
            if row['final_price'] > 0:
                margin_percentage = (row['gross_margin'] / row['final_price']) * 100
                assert 0 <= margin_percentage <= 50, "Gross margin should be reasonable percentage"
            
            # Inventory should be reasonable
            assert row['inventory_before_sale'] >= row['quantity'], "Should have enough inventory"
            assert row['inventory_after_sale'] >= 0, "Inventory after sale should be non-negative"