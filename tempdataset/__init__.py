"""
TempDataset Library - Generate temporary datasets for testing and development.

A lightweight Python library for generating realistic sample data without heavy dependencies.
"""

from .core.generator import DataGenerator
from .core.utils.data_frame import TempDataFrame
from .core.io.csv_handler import read_csv as _read_csv
from .core.io.json_handler import read_json as _read_json
from .core.datasets.sales import SalesDataset
from .core.datasets.customers import CustomersDataset
from .core.datasets.ecommerce import EcommerceDataset
from .core.datasets.employees import EmployeesDataset
from .core.datasets.marketing import MarketingDataset
from .core.datasets.retail import RetailDataset
from .core.datasets.suppliers import SuppliersDataset
from .core.exceptions import (
    TempDatasetError, DatasetNotFoundError, DataGenerationError,
    ValidationError, CSVReadError, CSVWriteError, JSONReadError, JSONWriteError,
    FileOperationError, MemoryError as TempDatasetMemoryError
)

# Initialize the main generator
_generator = DataGenerator()

# Register available datasets
_generator.register_dataset('sales', SalesDataset)
_generator.register_dataset('customers', CustomersDataset)
_generator.register_dataset('ecommerce', EcommerceDataset)
_generator.register_dataset('employees', EmployeesDataset)
_generator.register_dataset('marketing', MarketingDataset)
_generator.register_dataset('retail', RetailDataset)
_generator.register_dataset('suppliers', SuppliersDataset)

def create_dataset(dataset_type: str, rows: int = 500):
    """
    Generate temporary datasets or save to files.
    
    Args:
        dataset_type: Dataset type ('sales', 'customers', 'ecommerce', 'employees', 'marketing', 'retail', 'suppliers') or filename ('sales.csv', 'customers.json', 'ecommerce.json', 'employees.csv', 'marketing.csv', 'retail.csv', 'suppliers.csv')
        rows: Number of rows to generate (default: 500)
        
    Returns:
        TempDataFrame containing the generated data (also saves to file if filename provided)
        
    Raises:
        ValidationError: If parameters are invalid
        DatasetNotFoundError: If dataset type is not available
        DataGenerationError: If data generation fails
        TempDatasetMemoryError: If memory limits are exceeded
        CSVWriteError: If CSV file writing fails
        JSONWriteError: If JSON file writing fails
    """
    # Use the generator's validation and error handling
    return _generator.generate(dataset_type, rows)


def read_csv(filename: str) -> TempDataFrame:
    """
    Read CSV file into TempDataFrame.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        TempDataFrame containing the CSV data
        
    Raises:
        ValidationError: If parameters are invalid
        CSVReadError: If the CSV file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.csv'):
        raise ValidationError("filename", filename, "filename with .csv extension")
    
    # Use the CSV handler's validation and error handling
    return _read_csv(filename)


def read_json(filename: str) -> TempDataFrame:
    """
    Read JSON file into TempDataFrame.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        TempDataFrame containing the JSON data
        
    Raises:
        ValidationError: If parameters are invalid
        JSONReadError: If the JSON file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.json'):
        raise ValidationError("filename", filename, "filename with .json extension")
    
    # Use the JSON handler's validation and error handling
    return _read_json(filename)


def get_performance_stats():
    """
    Get performance statistics from the data generator.
    
    Returns:
        Dictionary with performance statistics including timing and memory usage
    """
    return _generator.get_performance_stats()


def reset_performance_stats():
    """Reset performance monitoring counters."""
    _generator.memory_monitor.reset()
    _generator.profiler = _generator.profiler.__class__()


def help():
    """
    Display comprehensive help information about available datasets and usage.
    
    This function provides detailed information about:
    - All available datasets
    - Column descriptions for each dataset
    - Usage examples
    - Quick start guide
    """
    help_text = """
================================================================================
                            TempDataset Library
                     Generate Realistic Test Data with Ease
================================================================================

QUICK START
================================================================================
import tempdataset

# Generate 1000 rows of any dataset
data = tempdataset.create_dataset('sales', 1000)

# Save directly to files
tempdataset.create_dataset('customers.csv', 500)    # CSV format
tempdataset.create_dataset('ecommerce.json', 200)   # JSON format

# Read data back
csv_data = tempdataset.read_csv('customers.csv')
json_data = tempdataset.read_json('ecommerce.json')

AVAILABLE DATASETS
================================================================================

SALES DATASET
-------------
tempdataset.create_dataset('sales', rows)

27 Columns: Complete sales transaction data
• Order Info: order_id, dates, priority, sales_rep
• Customer: customer_id, name, email, age, gender, segment
• Product: product_id, name, category, subcategory, brand
• Financial: prices, discounts, profit, payment_method
• Geographic: region, country, state, city, postal_code
• Logistics: shipping_mode, delivery dates

CUSTOMERS DATASET
-----------------
tempdataset.create_dataset('customers', rows)

31 Columns: Complete customer profiles
• Personal: names, email, phone, demographics, birth_date
• Professional: occupation, company, annual_income
• Geographic: full address details with region
• Account: creation date, status, purchase history
• Loyalty: membership, points, preferences, newsletter
• Analytics: total_orders, total_spent, average_order_value

ECOMMERCE DATASET
-----------------
tempdataset.create_dataset('ecommerce', rows)

35+ Columns: Comprehensive e-commerce transactions
• Transaction: transaction_id, order details, timestamps
• Customer: demographics, purchase behavior, device info
• Product: detailed product catalog with variants
• Business: pricing, margins, seller info, commissions
• Reviews: ratings, review counts, return data
• Digital: website sessions, mobile app usage

EMPLOYEES DATASET
-----------------
tempdataset.create_dataset('employees', rows)

30+ Columns: Complete employee records
• Personal: names, contact, demographics, emergency contacts
• Professional: job title, department, manager, salary
• Employment: hire date, status, employment type
• Performance: performance ratings, reviews, goals
• Benefits: health insurance, retirement, PTO balances
• Skills: skill ratings, certifications, training

MARKETING DATASET
-----------------
tempdataset.create_dataset('marketing', rows)

32+ Columns: Marketing campaign performance
• Campaign: campaign_id, name, type, duration
• Channels: email, social media, paid ads, content marketing
• Performance: impressions, clicks, conversions, ROI
• Audience: demographics, segments, engagement metrics
• Budget: spend data, cost per acquisition, lifetime value
• Attribution: touch points, conversion paths

RETAIL DATASET
--------------
tempdataset.create_dataset('retail', rows)

28+ Columns: In-store retail operations
• Transaction: receipt_id, timestamp, store info
• Product: SKU, barcode, inventory levels
• Sales: quantities, prices, discounts, tax
• Store: store_id, location, staff info
• Customer: demographics, loyalty cards
• Operations: shift data, seasonal trends

SUPPLIERS DATASET
-----------------
tempdataset.create_dataset('suppliers', rows)

22+ Columns: Supplier and vendor management
• Supplier: supplier_id, company name, contact details
• Business: industry, size, years in business
• Performance: quality ratings, delivery metrics
• Financial: payment terms, credit ratings
• Geographic: location data, service areas
• Contracts: contract terms, certifications

USAGE EXAMPLES
================================================================================

# Basic Usage
data = tempdataset.create_dataset('sales', 1000)
print(f"Generated {len(data)} rows with {len(data.columns)} columns")

# Data Analysis
high_value_sales = data.filter(lambda row: row['final_price'] > 500)
customer_summary = data.select(['customer_name', 'final_price', 'order_date'])

# Export Options
data.to_csv('output.csv')          # Export to CSV
data.to_json('output.json')        # Export to JSON
dict_data = data.to_dict()          # Convert to dictionary

# Direct File Generation
tempdataset.create_dataset('sales_data.csv', 2000)        # Generate & save CSV
tempdataset.create_dataset('customer_data.json', 1500)    # Generate & save JSON

# Performance Monitoring
stats = tempdataset.get_performance_stats()
print(f"Generation time: {stats['generation_time']:.2f}s")
print(f"Memory usage: {stats['memory_usage']:.2f}MB")

# Data Operations
data.head(10)           # First 10 rows
data.tail(5)            # Last 5 rows
data.describe()         # Statistical summary
data.info()             # Data information
data.memory_usage()     # Memory usage details

TERMINAL USAGE
================================================================================
# Command-line interface (if installed as CLI)
tempdataset sales -r 1000 --verbose
tempdataset customers.csv -r 500
tempdataset --list
tempdataset --help-datasets

MORE INFO
================================================================================
• Documentation: https://tempdataset.readthedocs.io/
• GitHub: https://github.com/dot-css/TempDataset
• Issues: https://github.com/dot-css/TempDataset/issues
• License: MIT

Version: 0.1.0 | Made with love for the Python testing community
"""
    print(help_text)


def list_datasets():
    """
    List all available datasets with brief descriptions.
    
    Returns:
        Dictionary with dataset names as keys and descriptions as values
    """
    datasets = {
        'sales': {
            'description': 'Sales transaction data with 27 columns',
            'columns': 27,
            'features': ['Order details', 'Customer info', 'Product data', 'Financial metrics', 'Geographic data']
        },
        'customers': {
            'description': 'Customer profiles with 31 columns', 
            'columns': 31,
            'features': ['Personal info', 'Demographics', 'Purchase history', 'Loyalty data', 'Account details']
        },
        'ecommerce': {
            'description': 'E-commerce transactions with 35+ columns',
            'columns': 35,
            'features': ['Transactions', 'Reviews', 'Digital metrics', 'Seller data', 'Device info']
        },
        'employees': {
            'description': 'Employee records with 30+ columns',
            'columns': 30,
            'features': ['HR data', 'Performance metrics', 'Benefits', 'Skills', 'Department info']
        },
        'marketing': {
            'description': 'Marketing campaign data with 32+ columns',
            'columns': 32,
            'features': ['Campaign metrics', 'Channel performance', 'ROI data', 'Audience analytics']
        },
        'retail': {
            'description': 'Retail store operations with 28+ columns', 
            'columns': 28,
            'features': ['In-store transactions', 'Inventory', 'Store operations', 'Staff data']
        },
        'suppliers': {
            'description': 'Supplier management data with 22+ columns',
            'columns': 22, 
            'features': ['Supplier profiles', 'Performance metrics', 'Contract data', 'Quality ratings']
        }
    }
    
    print("\nAvailable TempDataset Datasets")
    print("=" * 50)
    
    for name, info in datasets.items():
        print(f"\n• {name.upper()}")
        print(f"   {info['description']}")
        print(f"   Features: {', '.join(info['features'])}")
        print(f"   Usage: tempdataset.create_dataset('{name}', rows)")
    
    print(f"\nUse tempdataset.help() for detailed examples and documentation")
    
    return datasets


__version__ = "0.1.0"

# Alias for convenience (matches the library name)
tempdataset = create_dataset

__all__ = ["create_dataset", "tempdataset", "TempDataFrame", "read_csv", "read_json", "get_performance_stats", "reset_performance_stats", "help", "list_datasets"]