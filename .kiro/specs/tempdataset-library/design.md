# Design Document

## Overview

The TempDataset Library is designed as a lightweight, dependency-minimal Python library that generates realistic temporary datasets for testing and development. The architecture follows a modular design with clear separation of concerns between data generation, file I/O, and data manipulation components.

The library provides a pandas-like interface through a custom `TempDataFrame` class while maintaining zero dependency on pandas itself. This approach ensures minimal installation footprint while providing familiar data exploration methods.

## Architecture

### High-Level Architecture

```mermaid
graph TB
    A[Main API - tempdataset()] --> B[Generator Engine]
    B --> C[Dataset Registry]
    C --> D[Sales Dataset]
    C --> E[Future Datasets]
    
    B --> F[Data Generation]
    F --> G[Faker Integration]
    F --> H[Fallback Generators]
    
    B --> I[TempDataFrame]
    I --> J[Data Exploration]
    I --> K[File I/O]
    
    K --> L[CSV Handler]
    K --> M[JSON Handler]
    
    style A fill:#e1f5fe
    style I fill:#f3e5f5
    style B fill:#e8f5e8
```

### Module Structure

```
tempdataset/
├── __init__.py                 # Main API exports
├── core/
│   ├── __init__.py
│   ├── generator.py            # Core generation engine
│   ├── datasets/               # Dataset definitions
│   │   ├── __init__.py
│   │   ├── base.py            # BaseDataset abstract class
│   │   └── sales.py           # SalesDataset implementation
│   ├── io/                    # File I/O operations
│   │   ├── __init__.py
│   │   ├── csv_handler.py     # CSV read/write operations
│   │   └── json_handler.py    # JSON read/write operations
│   └── utils/
│       ├── __init__.py
│       ├── data_frame.py      # TempDataFrame implementation
│       └── faker_utils.py     # Faker integration utilities
```

## Components and Interfaces

### 1. Main API Interface

```python
def tempdataset(dataset_type: str, rows: int = 500) -> Union[TempDataFrame, None]:
    """
    Main entry point for dataset generation.
    
    Args:
        dataset_type: Dataset type ('sales') or filename ('sales.csv', 'sales.json')
        rows: Number of rows to generate
        
    Returns:
        TempDataFrame for dataset types, None for file outputs
    """

def read_csv(filename: str) -> TempDataFrame:
    """Read CSV file into TempDataFrame"""

def read_json(filename: str) -> TempDataFrame:
    """Read JSON file into TempDataFrame"""
```

### 2. TempDataFrame Class

The `TempDataFrame` serves as a lightweight alternative to pandas DataFrame with essential data exploration methods:

```python
class TempDataFrame:
    def __init__(self, data: List[Dict], columns: List[str]):
        self._data = data
        self._columns = columns
    
    def head(self, n: int = 5) -> str:
        """Display first n rows"""
    
    def tail(self, n: int = 5) -> str:
        """Display last n rows"""
    
    @property
    def shape(self) -> Tuple[int, int]:
        """Return (rows, columns) tuple"""
    
    @property
    def columns(self) -> List[str]:
        """Return column names"""
    
    def info(self) -> str:
        """Display dataset information"""
    
    def to_csv(self, filename: str) -> None:
        """Export to CSV file"""
    
    def to_json(self, filename: str) -> None:
        """Export to JSON file"""
```

### 3. Dataset Generation System

#### BaseDataset Abstract Class

```python
from abc import ABC, abstractmethod

class BaseDataset(ABC):
    def __init__(self, rows: int = 500):
        self.rows = rows
        self.seed = None
    
    @abstractmethod
    def generate(self) -> List[Dict]:
        """Generate dataset rows"""
        pass
    
    @abstractmethod
    def get_schema(self) -> Dict[str, str]:
        """Return column schema with types"""
        pass
    
    def set_seed(self, seed: int) -> None:
        """Set random seed for reproducible generation"""
        self.seed = seed
```

#### SalesDataset Implementation

The `SalesDataset` class implements comprehensive sales data generation with 27 columns as specified in requirements. Key design decisions:

- **Realistic Data Generation**: Uses Faker library when available for names, addresses, emails
- **Data Consistency**: Ensures logical relationships between fields (dates, calculations)
- **Performance Optimization**: Generates data in batches for large datasets
- **Configurable Categories**: Maintains realistic product categories and subcategories

### 4. Data Generation Engine

The generator engine coordinates between different components:

```python
class DataGenerator:
    def __init__(self):
        self.datasets = {}
        self.faker_available = self._check_faker()
    
    def register_dataset(self, name: str, dataset_class: Type[BaseDataset]):
        """Register new dataset type"""
    
    def generate(self, dataset_type: str, rows: int) -> TempDataFrame:
        """Generate dataset using registered generators"""
    
    def _check_faker(self) -> bool:
        """Check if Faker library is available"""
```

### 5. File I/O System

#### CSV Handler
- Uses Python's built-in `csv` module
- Handles large files through streaming
- Supports various CSV dialects
- Provides proper error handling for malformed files

#### JSON Handler
- Uses Python's built-in `json` module
- Handles large JSON files efficiently
- Supports both array-of-objects and object-per-line formats
- Provides clear error messages for parsing issues

## Data Models

### Sales Dataset Schema

The sales dataset includes 27 columns with specific data types and generation rules:

| Column | Type | Generation Rule |
|--------|------|----------------|
| order_id | string | "ORD-YYYY-{sequential}" |
| customer_id | string | "CUST-{4-digit}" |
| customer_name | string | Faker.name() or random selection |
| customer_email | string | Generated from name + domain |
| product_id | string | "PROD-{3-letter}{3-digit}" |
| product_name | string | Category-appropriate product names |
| category | string | Predefined categories (Electronics, etc.) |
| subcategory | string | Category-specific subcategories |
| brand | string | Category-appropriate brand names |
| quantity | integer | Random 1-10 |
| unit_price | float | Category-based price ranges |
| total_price | float | quantity × unit_price |
| discount | float | 0-20% of total_price |
| final_price | float | total_price - discount |
| order_date | datetime | Random within date range |
| ship_date | datetime | order_date + 1-7 days |
| delivery_date | datetime | ship_date + 2-14 days |
| sales_rep | string | Faker.name() or predefined list |
| region | string | North, South, East, West, Central |
| country | string | Faker.country() or predefined |
| state/province | string | Country-appropriate states |
| city | string | Faker.city() or predefined |
| postal_code | string | Region-appropriate format |
| customer_segment | string | Consumer, Corporate, Home Office |
| order_priority | string | Low, Medium, High, Critical |
| shipping_mode | string | Standard, Express, Overnight |
| payment_method | string | Credit Card, Debit Card, PayPal, Bank Transfer |
| customer_age | integer | Random 18-80 |
| customer_gender | string | Male, Female, Other |
| profit | float | 10-30% of final_price |

### Data Relationships and Consistency

The design ensures logical consistency through:

1. **Temporal Consistency**: order_date < ship_date < delivery_date
2. **Mathematical Consistency**: Calculated fields use proper formulas
3. **Geographic Consistency**: Matching regions, countries, states, and postal codes
4. **Category Consistency**: Products match their categories and subcategories
5. **Customer Consistency**: Names and emails are logically related

## Error Handling

### Error Categories and Responses

1. **Invalid Dataset Type**
   - Error: `DatasetNotFoundError`
   - Message: "Dataset type '{type}' not found. Available types: {available_types}"

2. **File Operation Errors**
   - Error: `FileNotFoundError`, `PermissionError`, `IOError`
   - Provide clear messages with suggested solutions

3. **Data Generation Errors**
   - Error: `DataGenerationError`
   - Include context about what failed and potential fixes

4. **Memory/Performance Errors**
   - Error: `MemoryError`
   - Suggest reducing dataset size or using file output

### Graceful Degradation

- **Faker Unavailable**: Fall back to basic random generation with warning
- **Large Dataset Requests**: Provide progress indication and memory warnings
- **File Format Issues**: Attempt to parse with multiple strategies before failing

## Testing Strategy

### Unit Testing Approach

1. **Dataset Generation Tests**
   - Verify all required columns are present
   - Validate data types and formats
   - Test data consistency rules
   - Performance tests for large datasets

2. **TempDataFrame Tests**
   - Test all exploration methods (head, tail, info, etc.)
   - Verify property calculations (shape, columns)
   - Test edge cases (empty datasets, single row)

3. **File I/O Tests**
   - Test CSV/JSON read/write operations
   - Test error handling for malformed files
   - Test large file handling
   - Test file path edge cases

4. **Integration Tests**
   - End-to-end workflow testing
   - Cross-platform compatibility
   - Memory usage validation
   - Performance benchmarking

### Test Data Strategy

- Use small, predictable datasets for unit tests
- Generate larger datasets for performance testing
- Create malformed files for error handling tests
- Test with and without optional dependencies

### Performance Testing

- Benchmark generation of 1K, 10K, 100K, 1M rows
- Memory usage profiling for large datasets
- File I/O performance testing
- Comparison with pandas (when available) for reference

## Implementation Considerations

### Dependency Management

- **Core Dependencies**: Only Python standard library
- **Optional Dependencies**: Faker for realistic data generation
- **Development Dependencies**: pytest, coverage, performance profiling tools

### Memory Optimization

- Use generators for large dataset creation
- Implement streaming for file operations
- Provide memory usage warnings for large requests
- Consider chunked processing for very large datasets

### Extensibility Design

- Plugin architecture for custom datasets
- Clear base classes for extension
- Registry system for dataset discovery
- Helper utilities for common generation patterns

### Cross-Platform Compatibility

- Use `pathlib` for file path handling
- Test on Windows, macOS, and Linux
- Handle different CSV dialects and line endings
- Ensure proper encoding handling for international data

This design provides a solid foundation for implementing the TempDataset library while maintaining simplicity, performance, and extensibility.