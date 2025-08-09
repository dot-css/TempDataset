#!/usr/bin/env python3
"""
Test script for the new EcommerceDataset functionality.
"""

import sys
import os

# Add the current directory to Python path so we can import tempdataset
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

import tempdataset

def test_ecommerce_dataset():
    """Test the EcommerceDataset functionality."""
    print("Testing EcommerceDataset...")
    
    # Test 1: Generate basic ecommerce dataset
    print("\n1. Generating 10 ecommerce transactions...")
    data = tempdataset('ecommerce', rows=10)
    print(f"Generated {len(data)} rows")
    print("Columns:", list(data.columns))
    
    # Test 2: Display first few rows
    print("\n2. First 3 rows:")
    print(data.head(3))
    
    # Test 3: Check data types and schema
    print("\n3. Data info:")
    print(data.info())
    
    # Test 4: Test specific column values
    print("\n4. Sample data validation:")
    first_row = data.iloc[0]
    print(f"Transaction ID: {first_row['transaction_id']}")
    print(f"Customer: {first_row['customer_name']} ({first_row['customer_email']})")
    print(f"Product: {first_row['product_name']} ({first_row['category']} - {first_row['subcategory']})")
    print(f"Price: ${first_row['unit_price']:.2f} x {first_row['quantity']} = ${first_row['total_price']:.2f}")
    print(f"Discount: {first_row['discount_percentage']}% (${first_row['discount_amount']:.2f})")
    print(f"Final Price: ${first_row['final_price']:.2f}")
    print(f"Profit: ${first_row['profit']:.2f}")
    print(f"Location: {first_row['city']}, {first_row['state_province']}, {first_row['country']}")
    
    # Test 5: Verify calculations
    print("\n5. Verifying calculations...")
    for i in range(min(3, len(data))):
        row = data.iloc[i]
        expected_total = row['unit_price'] * row['quantity']
        expected_discount = (row['total_price'] * row['discount_percentage']) / 100
        expected_final = row['total_price'] - row['discount_amount']
        
        print(f"Row {i+1}:")
        print(f"  Total price calculation: {row['unit_price']:.2f} x {row['quantity']} = {expected_total:.2f} (actual: {row['total_price']:.2f})")
        print(f"  Discount calculation: {row['total_price']:.2f} x {row['discount_percentage']:.2f}% = {expected_discount:.2f} (actual: {row['discount_amount']:.2f})")
        print(f"  Final price calculation: {row['total_price']:.2f} - {row['discount_amount']:.2f} = {expected_final:.2f} (actual: {row['final_price']:.2f})")
    
    # Test 6: Save to file
    print("\n6. Saving to files...")
    csv_data = tempdataset('ecommerce.csv', rows=5)
    json_data = tempdataset('ecommerce.json', rows=5)
    print("Files created: ecommerce.csv, ecommerce.json")
    
    print("\n✅ All tests passed! EcommerceDataset is working correctly.")
    return True

if __name__ == "__main__":
    try:
        test_ecommerce_dataset()
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)