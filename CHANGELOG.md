# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Future enhancements and features

## [0.2.0] - 2025-01-12

### Fixed
- **CRITICAL FIX**: Resolved datetime type mismatch error that was preventing generation of `user_profiles`, `suppliers`, `prescriptions`, and `insurance` datasets
  - Fixed inconsistent return types between Faker and fallback date generation methods
  - Updated `faker_utils.py` to ensure consistent `date` object returns
  - All 40 datasets now generate successfully in both Colab and Kaggle environments
- **API COMPATIBILITY**: Fixed `TempDataFrame.shape` to work both as property and method
  - Users can now use both `df.shape` and `df.shape()` syntax
  - Maintains backward compatibility with existing code
  - Implemented custom descriptor for seamless property/method access

### Changed
- Enhanced error handling and type consistency across datetime operations
- Improved cross-platform compatibility for environments with or without Faker library

### Technical
- Updated type annotations for better type safety
- Enhanced fallback implementations for environments without optional dependencies
- Improved test coverage for datetime edge cases

## [0.1.2] - 2025-01-10

### Added
- **NEW SOCIAL DATASETS**: Added 2 new social media datasets
  - `social_media`: Social media posts with engagement metrics (17 columns)
  - `user_profiles`: Social media user profiles with demographics (17 columns)
- Enhanced CLI with comprehensive dataset listing (now 40 total datasets)
- Complete test coverage for all 40 datasets
- Improved CLI help text with categorized dataset listings

### Fixed
- Fixed CLI syntax errors and improved error handling
- Enhanced dataset registration and validation

### Changed
- Updated CLI to display all 40 available datasets in organized categories
- Improved dataset documentation and examples

## [0.1.1] - 2025-01-XX

### Added
- Enhanced dataset collection with 38 datasets across multiple categories
- Financial datasets (8): stocks, banking, cryptocurrency, insurance, loans, investments, accounting, payments
- IoT sensor datasets (6): weather, energy, traffic, environmental, industrial, smarthome
- Healthcare datasets (6): patients, appointments, lab_results, prescriptions, medical_history, clinical_trials
- Technology datasets (8): web_analytics, app_usage, system_logs, api_calls, server_metrics, user_sessions, error_logs, performance
- Core business datasets (10): crm, customers, ecommerce, employees, inventory, marketing, retail, reviews, sales, suppliers

## [0.1.0] - 2025-01-XX

### Added
- Initial release of TempDataset library
- Core `tempdataset()` function for dataset generation
- `TempDataFrame` class for data manipulation
- Sales dataset generator with realistic data patterns
- CSV and JSON file I/O support
- Memory-efficient data generation
- Performance monitoring and statistics
- Comprehensive error handling with custom exceptions
- Type hints and mypy support
- Zero-dependency core functionality
- Optional Faker integration for enhanced data generation

### Features
- Generate realistic sales transaction data
- Export data to CSV and JSON formats
- Read CSV and JSON files into TempDataFrame
- Filter and select data operations
- Statistical summaries and data information
- Memory usage tracking
- Performance profiling
- Command-line interface (CLI)

### Technical
- Python 3.7+ compatibility
- Comprehensive test coverage (>95%)
- Performance benchmarks
- Memory optimization
- Type safety with mypy
- Code formatting with Black
- Linting with flake8
- Continuous integration setup

### Documentation
- Complete API documentation
- Usage examples and tutorials
- Development setup guide
- Contributing guidelines
- Performance optimization tips

## [0.0.1] - Development

### Added
- Project structure and initial codebase
- Basic dataset generation functionality
- Core utilities and data structures
- Initial test framework