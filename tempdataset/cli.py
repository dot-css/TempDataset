#!/usr/bin/env python3
"""
Command-line interface for TempDataset.
"""

import argparse
import sys
from typing import Optional

from . import tempdataset, __version__


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
        prog="tempdataset"
    )
    
    parser.add_argument(
        "--version",
        action="version",
        version=f"tempdataset {__version__}"
    )
    
    parser.add_argument(
        "dataset_type",
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
        if parsed_args.verbose:
            print(f"Generating {parsed_args.rows} rows of {parsed_args.dataset_type} data...")
        
        result = tempdataset(parsed_args.dataset_type, parsed_args.rows)
        
        if result is not None:
            # Dataset type was specified, show summary
            print(f"Generated {len(result)} rows with {len(result.columns)} columns")
            if parsed_args.verbose:
                print(f"Columns: {', '.join(result.columns)}")
                print(f"Memory usage: {result.memory_usage():.2f} MB")
        else:
            # File was generated
            print(f"Successfully generated {parsed_args.dataset_type}")
        
        return 0
        
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    sys.exit(main())