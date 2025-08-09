"""
Unit tests for the suppliers dataset.
"""

import unittest
import random
from datetime import datetime, timedelta
from tempdataset.core.datasets.suppliers import SuppliersDataset


class TestSuppliersDataset(unittest.TestCase):
    """Test cases for the SuppliersDataset class."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.dataset = SuppliersDataset(rows=100)
        self.small_dataset = SuppliersDataset(rows=5)
    
    def test_dataset_initialization(self):
        """Test dataset initialization."""
        self.assertEqual(self.dataset.rows, 100)
        self.assertIsNotNone(self.dataset.faker_utils)
        self.assertEqual(self.dataset._supplier_counter, 1)
    
    def test_generate_basic_functionality(self):
        """Test basic data generation functionality."""
        data = self.small_dataset.generate()
        
        # Check that we get the correct number of rows
        self.assertEqual(len(data), 5)
        
        # Check that each row is a dictionary
        for row in data:
            self.assertIsInstance(row, dict)
    
    def test_all_required_columns_present(self):
        """Test that all required columns are present."""
        data = self.small_dataset.generate()
        
        expected_columns = [
            'supplier_id', 'supplier_name', 'contact_name', 'contact_title',
            'email', 'phone_number', 'fax_number', 'website', 'address', 'city',
            'state_province', 'country', 'postal_code', 'supplier_type', 'industry',
            'product_categories', 'rating', 'on_time_delivery_rate', 'average_lead_time_days',
            'contract_start_date', 'contract_end_date', 'annual_contract_value_usd',
            'payment_terms', 'preferred_supplier', 'return_rate_percentage',
            'last_order_date', 'total_orders', 'total_order_value_usd',
            'primary_contact_method', 'notes'
        ]
        
        # Check first row for all columns
        first_row = data[0]
        for column in expected_columns:
            self.assertIn(column, first_row, f"Column '{column}' missing from generated data")
    
    def test_supplier_id_generation(self):
        """Test supplier ID generation and uniqueness."""
        data = self.dataset.generate()
        
        # Check supplier ID format
        for row in data:
            supplier_id = row['supplier_id']
            self.assertRegex(supplier_id, r'^SUP-\d{6}$', f"Invalid supplier ID format: {supplier_id}")
        
        # Check uniqueness
        supplier_ids = [row['supplier_id'] for row in data]
        unique_ids = set(supplier_ids)
        self.assertEqual(len(unique_ids), len(supplier_ids), "Supplier IDs are not unique")
    
    def test_data_types_and_constraints(self):
        """Test data types and value constraints."""
        data = self.small_dataset.generate()
        
        for row in data:
            # String fields
            self.assertIsInstance(row['supplier_name'], str)
            self.assertIsInstance(row['contact_name'], str)
            self.assertIsInstance(row['contact_title'], str)
            self.assertIsInstance(row['email'], str)
            self.assertIsInstance(row['phone_number'], str)
            self.assertIsInstance(row['address'], str)
            self.assertIsInstance(row['city'], str)
            self.assertIsInstance(row['state_province'], str)
            self.assertIsInstance(row['country'], str)
            self.assertIsInstance(row['postal_code'], str)
            self.assertIsInstance(row['supplier_type'], str)
            self.assertIsInstance(row['industry'], str)
            self.assertIsInstance(row['product_categories'], str)
            self.assertIsInstance(row['payment_terms'], str)
            self.assertIsInstance(row['primary_contact_method'], str)
            self.assertIsInstance(row['contract_start_date'], str)
            self.assertIsInstance(row['last_order_date'], str)
            
            # Optional string fields (can be None)
            if row['fax_number'] is not None:
                self.assertIsInstance(row['fax_number'], str)
            if row['website'] is not None:
                self.assertIsInstance(row['website'], str)
            if row['contract_end_date'] is not None:
                self.assertIsInstance(row['contract_end_date'], str)
            if row['notes'] is not None:
                self.assertIsInstance(row['notes'], str)
            
            # Numeric fields
            self.assertIsInstance(row['rating'], int)
            self.assertIsInstance(row['on_time_delivery_rate'], float)
            self.assertIsInstance(row['average_lead_time_days'], int)
            self.assertIsInstance(row['annual_contract_value_usd'], float)
            self.assertIsInstance(row['return_rate_percentage'], float)
            self.assertIsInstance(row['total_orders'], int)
            self.assertIsInstance(row['total_order_value_usd'], float)
            
            # Boolean fields
            self.assertIsInstance(row['preferred_supplier'], bool)
    
    def test_value_constraints(self):
        """Test that values meet the specified constraints."""
        data = self.dataset.generate()
        
        for row in data:
            # Rating constraint (1-5)
            self.assertGreaterEqual(row['rating'], 1)
            self.assertLessEqual(row['rating'], 5)
            
            # On-time delivery rate (70-100%)
            self.assertGreaterEqual(row['on_time_delivery_rate'], 70.0)
            self.assertLessEqual(row['on_time_delivery_rate'], 100.0)
            
            # Return rate (0-15%)
            self.assertGreaterEqual(row['return_rate_percentage'], 0.0)
            self.assertLessEqual(row['return_rate_percentage'], 15.0)
            
            # Lead time days (positive)
            self.assertGreater(row['average_lead_time_days'], 0)
            
            # Total orders (positive)
            self.assertGreater(row['total_orders'], 0)
            
            # Contract value (positive)
            self.assertGreater(row['annual_contract_value_usd'], 0)
            self.assertGreater(row['total_order_value_usd'], 0)
    
    def test_enum_values(self):
        """Test that enum fields contain expected values."""
        data = self.dataset.generate()
        
        expected_supplier_types = ['Manufacturer', 'Distributor', 'Wholesaler', 'Service Provider']
        expected_payment_terms = ['Net 30', 'Net 45', 'Net 60', 'Prepaid']
        expected_contact_methods = ['Email', 'Phone', 'Fax', 'In-person']
        
        for row in data:
            self.assertIn(row['supplier_type'], expected_supplier_types)
            self.assertIn(row['payment_terms'], expected_payment_terms)
            self.assertIn(row['primary_contact_method'], expected_contact_methods)
    
    def test_preferred_supplier_logic(self):
        """Test that preferred supplier logic is generally followed."""
        data = self.dataset.generate()
        
        # Get preferred suppliers
        preferred_suppliers = [row for row in data if row['preferred_supplier']]
        
        # Most preferred suppliers should have high ratings or delivery rates
        high_performance_preferred = 0
        for supplier in preferred_suppliers:
            if supplier['rating'] >= 4 or supplier['on_time_delivery_rate'] >= 90.0:
                high_performance_preferred += 1
        
        # At least 50% of preferred suppliers should have high performance
        if len(preferred_suppliers) > 0:
            performance_ratio = high_performance_preferred / len(preferred_suppliers)
            self.assertGreaterEqual(performance_ratio, 0.5, 
                                  "Less than 50% of preferred suppliers have high performance")
    
    def test_industry_product_categories_consistency(self):
        """Test that product categories match their industries."""
        data = self.small_dataset.generate()
        
        for row in data:
            industry = row['industry']
            product_categories = row['product_categories']
            
            # Check that product categories string is not empty
            self.assertTrue(len(product_categories) > 0)
            
            # Check that it contains meaningful product information
            self.assertNotEqual(product_categories, industry)  # Should be different from industry
    
    def test_date_constraints(self):
        """Test date field constraints."""
        data = self.small_dataset.generate()
        
        for row in data:
            # Parse dates
            contract_start = datetime.strptime(row['contract_start_date'], '%Y-%m-%d').date()
            last_order = datetime.strptime(row['last_order_date'], '%Y-%m-%d').date()
            
            # Contract start should be in the past
            self.assertLessEqual(contract_start, datetime.now().date())
            
            # Last order should be after or equal to contract start
            self.assertGreaterEqual(last_order, contract_start)
            
            # Last order should be in the past or today
            self.assertLessEqual(last_order, datetime.now().date())
            
            # If contract end date exists, check constraints
            if row['contract_end_date']:
                contract_end = datetime.strptime(row['contract_end_date'], '%Y-%m-%d').date()
                self.assertGreaterEqual(contract_end, contract_start)
    
    def test_email_format(self):
        """Test email format validation."""
        data = self.small_dataset.generate()
        
        for row in data:
            email = row['email']
            self.assertIn('@', email, f"Email '{email}' missing @ symbol")
            self.assertIn('.', email, f"Email '{email}' missing domain extension")
    
    def test_schema_method(self):
        """Test the get_schema method."""
        schema = self.dataset.get_schema()
        
        # Check that schema is a dictionary
        self.assertIsInstance(schema, dict)
        
        # Check that all columns are in schema
        expected_columns = [
            'supplier_id', 'supplier_name', 'contact_name', 'contact_title',
            'email', 'phone_number', 'fax_number', 'website', 'address', 'city',
            'state_province', 'country', 'postal_code', 'supplier_type', 'industry',
            'product_categories', 'rating', 'on_time_delivery_rate', 'average_lead_time_days',
            'contract_start_date', 'contract_end_date', 'annual_contract_value_usd',
            'payment_terms', 'preferred_supplier', 'return_rate_percentage',
            'last_order_date', 'total_orders', 'total_order_value_usd',
            'primary_contact_method', 'notes'
        ]
        
        for column in expected_columns:
            self.assertIn(column, schema, f"Column '{column}' missing from schema")
        
        # Check specific data types
        self.assertEqual(schema['supplier_id'], 'string')
        self.assertEqual(schema['rating'], 'integer')
        self.assertEqual(schema['on_time_delivery_rate'], 'float')
        self.assertEqual(schema['preferred_supplier'], 'boolean')
        self.assertEqual(schema['contract_start_date'], 'date')
    
    def test_reproducibility_with_seed(self):
        """Test that data generation is reproducible with the same seed."""
        # Generate data with the same seed twice
        dataset1 = SuppliersDataset(rows=10)
        dataset1.seed = 42
        data1 = dataset1.generate()
        
        dataset2 = SuppliersDataset(rows=10)
        dataset2.seed = 42
        data2 = dataset2.generate()
        
        # The data should be identical
        self.assertEqual(len(data1), len(data2))
        for i in range(len(data1)):
            self.assertEqual(data1[i]['supplier_id'], data2[i]['supplier_id'])
            self.assertEqual(data1[i]['supplier_name'], data2[i]['supplier_name'])
            self.assertEqual(data1[i]['rating'], data2[i]['rating'])


if __name__ == '__main__':
    unittest.main()
