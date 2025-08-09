# TempDataset

[![PyPI version](https://badge.fury.io/py/tempdataset.svg)](https://badge.fury.io/py/tempdataset)
[![Python Support](https://img.shields.io/pypi/pyversions/tempdataset.svg)](https://pypi.org/project/tempdataset/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python library for generating realistic temporary datasets for testing and development. No heavy dependencies required - works with just the Python standard library!

## Features

- Lightweight: Zero dependencies for core functionality
- Multiple Formats: Generate CSV, JSON, or in-memory datasets
- Realistic Data: Built-in datasets with realistic patterns
- Extensible: Easy to add custom dataset types
- Memory Efficient: Optimized for large dataset generation
- Python 3.7+: Compatible with modern Python versions

## Quick Start

### Installation

```bash
pip install tempdataset
```

```bash
pip install git+https://github.com/dot-css/TempDataset
```

### Basic Usage

```python
import tempdataset

# Generate 1000 rows of any dataset type
data = tempdataset.create_dataset('sales', 1000)
data.head()

# Save directly to CSV
tempdataset.create_dataset('sales.csv', 500)

# Save directly to JSON
tempdataset.create_dataset('customers.json', 500)

# Read data back
csv_data = tempdataset.read_csv('sales.csv')
json_data = tempdataset.read_json('customers.json')

# Get help and see all available datasets
tempdataset.help()          # Comprehensive help
tempdataset.list_datasets() # Quick dataset overview
```

## Available Datasets

TempDataset provides **7 comprehensive datasets** for various use cases:

### 🛒 Sales Dataset
Complete sales transaction data with **27 columns**:
```python
sales_data = tempdataset.create_dataset('sales', 1000)
```
**Features:** Order information, customer details, product data, financial calculations, geographic data, shipping details

**Key Columns:** `order_id`, `customer_name`, `product_name`, `category`, `final_price`, `order_date`, `sales_rep`, `region`, `profit`

### 👥 Customers Dataset  
Comprehensive customer profiles with **31 columns**:
```python
customers_data = tempdataset.create_dataset('customers', 1000)
```
**Features:** Personal information, demographics, purchase history, loyalty data, account status, preferences

**Key Columns:** `customer_id`, `full_name`, `email`, `age`, `annual_income`, `total_spent`, `loyalty_points`, `account_status`

### 🛍️ E-commerce Dataset
Advanced e-commerce transaction data with **35+ columns**:
```python
ecommerce_data = tempdataset.create_dataset('ecommerce', 1000)
```
**Features:** Transaction details, customer behavior, product catalog, reviews, returns, digital metrics, seller information

**Key Columns:** `transaction_id`, `customer_rating`, `seller_rating`, `return_status`, `device_type`, `conversion_rate`

### 👨‍💼 Employees Dataset
Complete HR and employee management data with **30+ columns**:
```python
employees_data = tempdataset.create_dataset('employees', 1000)
```
**Features:** Personal info, job details, performance metrics, benefits, skills, department structure

**Key Columns:** `employee_id`, `job_title`, `department`, `salary`, `performance_rating`, `benefits`, `skills`

### 📢 Marketing Dataset
Marketing campaign performance data with **32+ columns**:
```python
marketing_data = tempdataset.create_dataset('marketing', 1000)
```
**Features:** Campaign metrics, channel performance, ROI analysis, audience data, conversion tracking

**Key Columns:** `campaign_id`, `channel`, `impressions`, `clicks`, `conversions`, `roi`, `cost_per_click`

### 🏪 Retail Dataset
In-store retail operations data with **28+ columns**:
```python
retail_data = tempdataset.create_dataset('retail', 1000)
```
**Features:** Point-of-sale transactions, inventory management, store operations, staff data, seasonal trends

**Key Columns:** `receipt_id`, `store_id`, `product_sku`, `quantity_sold`, `staff_id`, `inventory_level`

### 🏭 Suppliers Dataset
Supplier and vendor management data with **22+ columns**:
```python
suppliers_data = tempdataset.create_dataset('suppliers', 1000)
```
**Features:** Supplier profiles, performance metrics, contract management, quality ratings, delivery data

**Key Columns:** `supplier_id`, `company_name`, `quality_rating`, `delivery_performance`, `contract_value`

### Quick Help
```python
# Get comprehensive help and examples
tempdataset.help()

# List all datasets with descriptions  
tempdataset.list_datasets()

# See specific dataset schema
data = tempdataset.create_dataset('sales', 10)
print(data.columns)  # View all column names
```

## Advanced Usage

### Working with TempDataFrame

```python
data = tempdataset.create_dataset('sales', 1000)

# Basic operations
data.head(10)          # First 10 rows
data.tail(5)           # Last 5 rows
data.describe()        # Statistical summary
data.info()            # Data info

# Filtering and selection
filtered = data.filter(lambda row: row['amount'] > 100)
selected = data.select(['customer_name', 'amount', 'date'])

# Export options
data.to_csv('output.csv')
data.to_json('output.json')
data.to_dict()                # Convert to dictionary
```

### Performance Monitoring

```python
import tempdataset

# Generate data
data = tempdataset.create_dataset('sales', 10000)

# Check performance stats
stats = tempdataset.get_performance_stats()
print(f"Generation time: {stats['generation_time']:.2f}s")
print(f"Memory usage: {stats['memory_usage']:.2f}MB")

# Reset stats for next operation
tempdataset.reset_performance_stats()
```

## Development

### Setting up Development Environment

```bash
# Clone the repository
git clone https://github.com/dot-css/TempDataset.git
cd TempDataset

# Install development dependencies
pip install -e .[dev]

# Run tests
pytest

# Run tests with coverage
pytest --cov=tempdataset

# Run performance benchmarks
pytest .benchmarks/
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test categories
pytest -m "not slow"          # Skip slow tests
pytest -m integration         # Only integration tests
pytest -m performance         # Only performance tests

# Run with coverage report
pytest --cov=tempdataset --cov-report=html
```

### Code Quality

```bash
# Format code
black tempdataset tests

# Lint code
flake8 tempdataset tests

# Type checking
mypy tempdataset
```

## API Reference

### Core Functions

#### `create_dataset(dataset_type, rows=500)`
Generate temporary datasets or save to files.

**Parameters:**
- `dataset_type` (str): Dataset type or filename
  - **Available types:** `'sales'`, `'customers'`, `'ecommerce'`, `'employees'`, `'marketing'`, `'retail'`, `'suppliers'`
  - **File formats:** `'sales.csv'`, `'customers.json'`, etc.
- `rows` (int): Number of rows to generate (default: 500)

**Returns:**
- `TempDataFrame` containing the generated data (also saves to file if filename provided)

#### `help()`
Display comprehensive help information about all available datasets, including column descriptions, usage examples, and feature details.

#### `list_datasets()`
Get a quick overview of all available datasets with their key features and column counts.

#### `read_csv(filename)`
Read CSV file into TempDataFrame.

#### `read_json(filename)`
Read JSON file into TempDataFrame.

### TempDataFrame Methods

- `head(n=5)`: Get first n rows
- `tail(n=5)`: Get last n rows
- `describe()`: Statistical summary
- `info()`: Dataset information
- `filter(func)`: Filter rows by function
- `select(columns)`: Select specific columns
- `to_csv(filename)`: Export to CSV
- `to_json(filename)`: Export to JSON
- `to_dict()`: Convert to dictionary

## Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Workflow

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Run the test suite
6. Submit a pull request

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Changelog

See [CHANGELOG.md](CHANGELOG.md) for a detailed history of changes.

## Support

- Documentation: https://tempdataset.readthedocs.io/
- Issue Tracker: https://github.com/dot-css/TempDataset/issues
- Discussions: https://github.com/dot-css/TempDataset/discussions

## Acknowledgments

- Built with love for the Python testing community
- Inspired by the need for lightweight, dependency-free test data generation
- Thanks to all contributors who help make this project better!