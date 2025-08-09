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
Available datasets:
  sales      - Sales transaction data (27 columns)
  customers  - Customer profiles (31 columns)  
  ecommerce  - E-commerce transactions (35+ columns)
  employees  - Employee records (30+ columns)
  marketing  - Marketing campaigns (32+ columns)
  retail     - Retail operations (28+ columns)
  suppliers  - Supplier management (22+ columns)

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