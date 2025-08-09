"""
Tests for EcommerceDataset functionality.
"""

import unittest
import tempfile
import os
from tempdataset import tempdataset
from tempdataset.core.datasets.ecommerce import EcommerceDataset


class TestEcommerceDataset(unittest.TestCase):
    """Test cases for EcommerceDataset."""
    
    def test_ecommerce_dataset_creation(self):
        """Test basic EcommerceDataset creation."""
        dataset = EcommerceDataset(rows=10)
        self.assertEqual(dataset.rows, 10)
    
    def test_ecommerce_data_generation(self):
        """Test data generation."""
        dataset = EcommerceDataset(rows=5)
        data = dataset.generate()
        
        self.assertEqual(len(data), 5)
        self.assertIsInstance(data, list)
        self.assertIsInstance(data[0], dict)
    
    def test_ecommerce_schema(self):
        """Test schema definition."""
        dataset = EcommerceDataset()
        schema = dataset.get_schema()
        
        # Check that all required columns are present
        required_columns = [
            'transaction_id', 'customer_id', 'customer_name', 'customer_email',
            'product_id', 'product_name', 'category', 'subcategory', 'brand',
            'quantity', 'unit_price', 'total_price', 'discount_percentage',
            'discount_amount', 'final_price', 'transaction_date', 'payment_method',
            'shipping_mode', 'shipping_cost', 'order_status', 'delivery_date',
            'country', 'state_province', 'city', 'postal_code', 'customer_segment',
            'coupon_code', 'review_rating', 'review_comment', 'return_requested',
            'return_reason', 'seller_id', 'seller_name', 'profit'
        ]
        
        for column in required_columns:
            self.assertIn(column, schema)
    
    def test_ecommerce_data_consistency(self):
        """Test data consistency and calculations."""
        dataset = EcommerceDataset(rows=10)
        dataset.set_seed(42)
        data = dataset.generate()
        
        for row in data:
            # Test price calculations
            expected_total = row['unit_price'] * row['quantity']
            self.assertAlmostEqual(row['total_price'], expected_total, places=1)
            
            expected_discount = (row['total_price'] * row['discount_percentage']) / 100
            self.assertAlmostEqual(row['discount_amount'], expected_discount, places=1)
            
            expected_final = row['total_price'] - row['discount_amount']
            self.assertAlmostEqual(row['final_price'], expected_final, places=1)
            
            # Test data types
            self.assertIsInstance(row['transaction_id'], str)
            self.assertIsInstance(row['customer_id'], str)
            self.assertIsInstance(row['quantity'], int)
            self.assertIsInstance(row['unit_price'], float)
            self.assertIsInstance(row['return_requested'], bool)
    
    def test_ecommerce_tempdataset_integration(self):
        """Test integration with tempdataset function."""
        data = tempdataset('ecommerce', rows=5)
        
        self.assertEqual(len(data), 5)
        self.assertEqual(len(data.columns), 34)  # All required columns
    
    def test_ecommerce_file_export(self):
        """Test file export functionality."""
        with tempfile.TemporaryDirectory() as temp_dir:
            csv_file = os.path.join(temp_dir, 'test_ecommerce.csv')
            json_file = os.path.join(temp_dir, 'test_ecommerce.json')
            
            # Test CSV export
            tempdataset(csv_file, rows=5)
            self.assertTrue(os.path.exists(csv_file))
            
            # Test JSON export
            tempdataset(json_file, rows=5)
            self.assertTrue(os.path.exists(json_file))
    
    def test_ecommerce_data_ranges(self):
        """Test that generated data falls within expected ranges."""
        dataset = EcommerceDataset(rows=20)
        dataset.set_seed(42)
        data = dataset.generate()
        
        for row in data:
            # Test quantity range
            self.assertGreaterEqual(row['quantity'], 1)
            self.assertLessEqual(row['quantity'], 10)
            
            # Test discount percentage range
            self.assertGreaterEqual(row['discount_percentage'], 0)
            self.assertLessEqual(row['discount_percentage'], 50)
            
            # Test unit price is positive
            self.assertGreater(row['unit_price'], 0)
            
            # Test profit is positive
            self.assertGreater(row['profit'], 0)
            
            # Test review rating range (if present)
            if row['review_rating'] is not None:
                self.assertGreaterEqual(row['review_rating'], 1)
                self.assertLessEqual(row['review_rating'], 5)


if __name__ == '__main__':
    unittest.main()