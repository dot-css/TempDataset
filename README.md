# TempDataset

[![PyPI version](https://badge.fury.io/py/tempdataset.svg)](https://badge.fury.io/py/tempdataset)
[![Python Support](https://img.shields.io/pypi/pyversions/tempdataset.svg)](https://pypi.org/project/tempdataset/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

A lightweight Python library for generating realistic temporary datasets for testing and development. Generate **40+ different dataset types** including business, financial, IoT, healthcare, and technology data!

## ✨ Features

- **40+ Dataset Types**: Business, financial, IoT sensors, healthcare, social media, and technology datasets
- **Zero Dependencies**: Works with just Python standard library
- **Multiple Formats**: Generate CSV, JSON, or in-memory datasets
- **Realistic Data**: Built-in faker integration with realistic patterns
- **Technology Focus**: New datasets for DevOps, monitoring, web analytics, and system performance
- **Memory Efficient**: Optimized for large dataset generation
- **Python 3.7+**: Compatible with modern Python versions

## 🚀 Quick Start

### Installation

```bash
pip install tempdataset
```

### Basic Usage

```python
import tempdataset

# Generate datasets
data = tempdataset.create_dataset('sales', 1000)
tech_data = tempdataset.create_dataset('web_analytics', 500)
server_metrics = tempdataset.create_dataset('server_metrics', 200)

# Save directly to files
tempdataset.create_dataset('sales_data.csv', 1000)
tempdataset.create_dataset('api_logs.json', 500)

# Get help and see all available datasets  
tempdataset.list_datasets() # Show all 40+ datasets
tempdataset.help()          # Quick help guide
```
```

## 📊 Available Datasets (40 Total)

TempDataset provides **40 comprehensive datasets** across 6 major categories:

### 🏢 Core Business Datasets (10)
- **`sales`** - Sales transactions and orders (27 columns)
- **`customers`** - Customer profiles and demographics (31 columns)  
- **`ecommerce`** - E-commerce transactions and reviews (35+ columns)
- **`employees`** - Employee records and HR data (30+ columns)
- **`marketing`** - Marketing campaigns and performance (32+ columns)
- **`retail`** - Retail store operations (28+ columns)
- **`suppliers`** - Supplier management data (22+ columns)
- **`crm`** - Customer relationship management (30+ columns)
- **`inventory`** - Inventory and warehouse data (25+ columns)
- **`reviews`** - Product and service reviews (15+ columns)

### 💰 Financial Datasets (8)
- **`stocks`** - Stock market trading data (20+ columns)
- **`banking`** - Banking transactions (20+ columns)
- **`cryptocurrency`** - Cryptocurrency trading (20+ columns)
- **`insurance`** - Insurance policies and claims (20+ columns)
- **`loans`** - Loan applications and management (20+ columns)
- **`investments`** - Investment portfolios (20+ columns)
- **`accounting`** - General ledger and accounting (20+ columns)
- **`payments`** - Digital payment processing (25+ columns)

### 🌐 Technology Datasets (8) ⭐ *NEW!*
- **`web_analytics`** - Website analytics and traffic (17 columns)
- **`app_usage`** - Mobile app usage analytics (15 columns)
- **`system_logs`** - System and application logs (11 columns)
- **`api_calls`** - API calls and performance (12 columns)
- **`server_metrics`** - Server performance monitoring (22 columns)
- **`user_sessions`** - User session tracking (20 columns)
- **`error_logs`** - Application error logs (16 columns)
- **`performance`** - Application performance monitoring (21 columns)

### 🏥 Healthcare Datasets (6)
- **`patients`** - Patient medical records (22 columns)
- **`appointments`** - Medical appointments (14 columns)
- **`lab_results`** - Laboratory test results (13 columns)
- **`prescriptions`** - Medication prescriptions (16 columns)
- **`medical_history`** - Patient medical history (11 columns)
- **`clinical_trials`** - Clinical trial data (14 columns)

### �️ IoT Sensor Datasets (6)  
- **`weather`** - Weather sensor monitoring (18 columns)
- **`energy`** - Smart meter energy data (14 columns)
- **`traffic`** - Traffic sensor monitoring (15 columns)
- **`environmental`** - Environmental monitoring (17 columns)
- **`industrial`** - Industrial sensor data (16 columns)
- **`smarthome`** - Smart home IoT devices (16 columns)

### 📱 Social Media Datasets (2)
- **`social_media`** - Social media posts and engagement (16 columns)
- **`user_profiles`** - Social media user profiles (17 columns)

### 🚀 Quick Examples

```python
# Generate different types of datasets
sales = tempdataset.create_dataset('sales', 1000)
tech_logs = tempdataset.create_dataset('system_logs', 500)  
health_data = tempdataset.create_dataset('patients', 200)
crypto = tempdataset.create_dataset('cryptocurrency', 300)

# Get help and list all datasets
tempdataset.list_datasets()  # Show all 40 datasets
tempdataset.help()          # Quick reference guide
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