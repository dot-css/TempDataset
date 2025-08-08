# Requirements Document

## Introduction

The TempDataset Library is a Python library designed to generate temporary datasets for testing, prototyping, and development purposes. The library provides a simple, intuitive API that requires minimal code to generate realistic sample data, with built-in support for common data formats and exploration methods without external dependencies like pandas.

## Requirements

### Requirement 1

**User Story:** As a developer, I want to generate sample datasets with a single function call, so that I can quickly create test data for my applications.

#### Acceptance Criteria

1. WHEN I call `tempdataset('sales')` THEN the system SHALL return a TempDataFrame with 500 rows of sales data by default
2. WHEN I call `tempdataset('sales', rows=5000)` THEN the system SHALL return a TempDataFrame with exactly 5000 rows of sales data
3. WHEN I call `tempdataset('sales', rows=0)` THEN the system SHALL return an empty TempDataFrame with proper column structure
4. WHEN I call `tempdataset('invalid_dataset')` THEN the system SHALL raise a clear error indicating the dataset type is not supported

### Requirement 2

**User Story:** As a developer, I want to save generated datasets directly to files, so that I can persist test data for later use or sharing.

#### Acceptance Criteria

1. WHEN I call `tempdataset('sales.csv')` THEN the system SHALL generate 500 rows of sales data and save it to a CSV file
2. WHEN I call `tempdataset('sales.csv', rows=1000)` THEN the system SHALL generate 1000 rows and save to CSV
3. WHEN I call `tempdataset('sales.json')` THEN the system SHALL generate 500 rows of sales data and save it to a JSON file
4. WHEN I call `tempdataset('sales.json', rows=2000)` THEN the system SHALL generate 2000 rows and save to JSON
5. IF the target file already exists THEN the system SHALL overwrite it without prompting
6. IF the target directory doesn't exist THEN the system SHALL create the necessary directories

### Requirement 3

**User Story:** As a developer, I want to read existing dataset files without pandas dependency, so that I can work with previously generated data using the same interface.

#### Acceptance Criteria

1. WHEN I call `tempdataset.read_csv('sales.csv')` THEN the system SHALL return a TempDataFrame with the CSV data
2. WHEN I call `tempdataset.read_json('sales.json')` THEN the system SHALL return a TempDataFrame with the JSON data
3. IF the file doesn't exist THEN the system SHALL raise a FileNotFoundError with a clear message
4. IF the file format is invalid THEN the system SHALL raise a parsing error with details
5. WHEN reading large files THEN the system SHALL handle them efficiently without excessive memory usage

### Requirement 4

**User Story:** As a developer, I want to explore generated datasets using familiar methods, so that I can quickly understand the data structure and content.

#### Acceptance Criteria

1. WHEN I call `data.head()` THEN the system SHALL display the first 5 rows in a readable format
2. WHEN I call `data.head(10)` THEN the system SHALL display the first 10 rows
3. WHEN I call `data.tail()` THEN the system SHALL display the last 5 rows
4. WHEN I call `data.tail(15)` THEN display the last 15 rows
5. WHEN I access `data.shape` THEN the system SHALL return a tuple with (rows, columns) count
6. WHEN I access `data.columns` THEN the system SHALL return a list of column names
7. WHEN I call `data.info()` THEN the system SHALL display dataset information including column types and memory usage

### Requirement 5

**User Story:** As a developer, I want to generate realistic sales data with comprehensive fields, so that my test scenarios closely match real-world data structures.

#### Acceptance Criteria

1. WHEN generating sales data THEN the system SHALL include all 27 required columns: order_id, customer_id, customer_name, customer_email, product_id, product_name, category, subcategory, brand, quantity, unit_price, total_price, discount, final_price, order_date, ship_date, delivery_date, sales_rep, region, country, state/province, city, postal_code, customer_segment, order_priority, shipping_mode, payment_method, customer_age, customer_gender, profit
2. WHEN generating order_id THEN the system SHALL use format "ORD-YYYY-NNNNNN" with sequential numbers
3. WHEN generating customer_id THEN the system SHALL use format "CUST-NNNN" 
4. WHEN generating product_id THEN the system SHALL use format "PROD-AAANNN" with letters and numbers
5. WHEN calculating total_price THEN the system SHALL ensure total_price = quantity × unit_price
6. WHEN calculating final_price THEN the system SHALL ensure final_price = total_price - discount
7. WHEN generating ship_date THEN the system SHALL ensure ship_date is order_date + 1-7 days
8. WHEN generating delivery_date THEN the system SHALL ensure delivery_date is ship_date + 2-14 days
9. WHEN generating profit THEN the system SHALL calculate as 10-30% of final_price

### Requirement 6

**User Story:** As a developer, I want the library to use minimal dependencies, so that it doesn't add bloat to my project or cause dependency conflicts.

#### Acceptance Criteria

1. WHEN installing the library THEN the system SHALL only require standard library modules for core functionality
2. WHEN faker is available THEN the system SHALL use it for realistic data generation
3. WHEN faker is not available THEN the system SHALL fall back to basic random data generation
4. WHEN importing the library THEN the system SHALL NOT require pandas or any heavy data processing libraries
5. IF optional dependencies are missing THEN the system SHALL provide clear guidance on installation

### Requirement 7

**User Story:** As a developer, I want consistent and reproducible data generation, so that I can create reliable tests and demos.

#### Acceptance Criteria

1. WHEN I set a random seed THEN the system SHALL generate identical datasets across multiple runs
2. WHEN generating related data fields THEN the system SHALL maintain logical consistency (e.g., matching addresses and postal codes)
3. WHEN generating categorical data THEN the system SHALL use realistic distributions and relationships
4. WHEN generating dates THEN the system SHALL ensure chronological consistency across order, ship, and delivery dates

### Requirement 8

**User Story:** As a developer, I want the library to handle large datasets efficiently, so that I can generate substantial amounts of test data without performance issues.

#### Acceptance Criteria

1. WHEN generating 10,000+ rows THEN the system SHALL complete within reasonable time (< 30 seconds)
2. WHEN working with large datasets THEN the system SHALL manage memory usage efficiently
3. WHEN saving large files THEN the system SHALL use streaming where appropriate to avoid memory issues
4. WHEN an operation takes significant time THEN the system SHOULD provide progress indication

### Requirement 9

**User Story:** As a developer, I want comprehensive error handling and validation, so that I can quickly identify and resolve issues with my data generation requests.

#### Acceptance Criteria

1. WHEN invalid parameters are provided THEN the system SHALL raise descriptive errors
2. WHEN file operations fail THEN the system SHALL provide clear error messages with suggested solutions
3. WHEN data generation fails THEN the system SHALL indicate the specific issue and recovery options
4. WHEN memory limits are exceeded THEN the system SHALL fail gracefully with guidance on reducing dataset size

### Requirement 10

**User Story:** As a developer, I want to extend the library with custom datasets, so that I can generate domain-specific test data for my applications.

#### Acceptance Criteria

1. WHEN I create a custom dataset class THEN the system SHALL provide a clear base class to inherit from
2. WHEN I register a custom dataset THEN the system SHALL make it available through the main tempdataset() function
3. WHEN implementing custom datasets THEN the system SHALL provide helper methods for common data generation patterns
4. WHEN custom datasets are used THEN the system SHALL maintain the same API consistency as built-in datasets