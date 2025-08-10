#!/usr/bin/env python3
"""
Command-line interface for TempDataset.
"""

import argparse
import sys
from typing import Optional

from . import create_dataset, help as show_help, list_datasets, __version__


def main(args: Optional[list] = None) -> int:
    """
    Main CLI entry point.
    
    Args:
        args: Command line arguments (for testing)
        
    Returns:
        Exit code (0 for success, 1 for error)
    """
    parser = argparse.ArgumentParser(
        description="Generate temporary datasets for testing and development",
        prog="tempdataset",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Available datasets (40 total):

CORE BUSINESS:
  crm           - Customer relationship management (30+ columns)
  customers     - Customer profiles (31 columns)  
  ecommerce     - E-commerce transactions (35+ columns)
  employees     - Employee records (30+ columns)
  inventory     - Inventory and warehouse stock (25+ columns)
  marketing     - Marketing campaigns (32+ columns)
  retail        - Retail operations (28+ columns)
  reviews       - Product and service reviews (15+ columns)
  sales         - Sales transaction data (27 columns)
  suppliers     - Supplier management (22+ columns)

FINANCIAL:
  stocks        - Stock market trading data (20+ columns)
  banking       - Banking transaction data (20+ columns)
  cryptocurrency - Cryptocurrency trading data (20+ columns)
  insurance     - Insurance policies and claims (20+ columns)
  loans         - Loan applications and management (20+ columns)
  investments   - Portfolio and investment tracking (20+ columns)
  accounting    - General ledger and financial statements (20+ columns)
  payments      - Digital payment processing (25+ columns)

IOT SENSOR:
  weather       - Weather sensor monitoring data (18 columns)
  energy        - Smart meter energy monitoring (14 columns)
  traffic       - Traffic sensor monitoring data (15 columns)
  environmental - Environmental monitoring data (17 columns)
  industrial    - Industrial sensor monitoring data (16 columns)
  smarthome     - Smart home IoT device data (16 columns)

HEALTHCARE:
  patients      - Patient medical records (22 columns)
  appointments  - Medical appointment scheduling (14 columns)
  lab_results   - Laboratory test results (13 columns)
  prescriptions - Medication prescriptions (16 columns)
  medical_history - Patient medical history (11 columns)
  clinical_trials - Clinical trial research data (14 columns)

TECHNOLOGY:
  web_analytics - Website analytics and traffic data (17 columns)
  app_usage     - Mobile app usage analytics (15 columns)
  system_logs   - System and application logs (11 columns)
  api_calls     - API call logs and performance (12 columns)
  server_metrics - Server performance monitoring (22 columns)
  user_sessions - User session tracking (20 columns)
  error_logs    - Application error logs (16 columns)
  performance   - Application performance monitoring (21 columns)

SOCIAL:
  social_media  - Social media posts with engagement (16 columns)
  user_profiles - Social media user profiles (17 columns)

Examples:
  tempdataset sales -r 1000            # Generate 1000 sales records
  tempdataset customers.csv -r 500     # Generate 500 customers to CSV
  tempdataset ecommerce.json --rows 800    # Generate 800 e-commerce records to JSON
  tempdataset --help-datasets           # Show comprehensive help
  tempdataset --list                    # List all datasets
        """
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"tempdataset {__version__}"
    )
    
    parser.add_argument(
        "--help-datasets",
        action="store_true",
        help="Show comprehensive help about all available datasets"
    )
    
    parser.add_argument(
        "--list",
        action="store_true", 
        help="List all available datasets with descriptions"
    )
    
    parser.add_argument(
        "dataset_type",
        nargs="?",
        help="Dataset type to generate (e.g., 'sales') or output filename (e.g., 'data.csv')"
    )
    
    parser.add_argument(
        "-r", "--rows",
        type=int,
        default=500,
        help="Number of rows to generate (default: 500)"
    )
    
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Enable verbose output"
    )
    
    if args is None:
        args = sys.argv[1:]
    
    parsed_args = parser.parse_args(args)
    
    try:
        # Handle help and list commands
        if parsed_args.help_datasets:
            show_help()
            return 0
            
        if parsed_args.list:
            list_datasets()
            return 0
        
        # Check if dataset_type is provided
        if not parsed_args.dataset_type:
            parser.print_help()
            print("\nError: dataset_type is required (unless using --help-datasets or --list)")
            return 1
        
        if parsed_args.verbose:
            print(f"Generating {parsed_args.rows} rows of {parsed_args.dataset_type} data...")
        
        result = create_dataset(parsed_args.dataset_type, parsed_args.rows)
        
        # Always show the data summary 
        print(f"Generated {len(result)} rows with {len(result.columns)} columns")
        
        # If it's a filename (has extension), mention the file was saved
        if '.' in parsed_args.dataset_type and any(parsed_args.dataset_type.endswith(ext) for ext in ['.csv', '.json']):
            print(f"Data saved to: {parsed_args.dataset_type}")
        
        if parsed_args.verbose:
            print(f"Columns: {', '.join(result.columns)}")
            print(f"Memory usage: {result.memory_usage():.2f} MB")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())