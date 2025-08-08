#!/usr/bin/env python3
"""
Test edge cases for TempDataFrame
"""

from tempdataset.core.utils.data_frame import TempDataFrame

print("=== Testing Edge Cases ===")
print()

# Test empty DataFrame
print("1. Empty DataFrame:")
empty_df = TempDataFrame([], ["col1", "col2"])
print("Shape:", empty_df.shape)
print("Columns:", empty_df.columns)
print("Head:")
print(empty_df.head())
print("Info:")
print(empty_df.info())
print()

# Test DataFrame with None values
print("2. DataFrame with None values:")
data_with_none = [
    {"name": "Alice", "age": 25, "city": None},
    {"name": None, "age": None, "city": "Boston"},
    {"name": "Charlie", "age": 35, "city": "Chicago"}
]
df_none = TempDataFrame(data_with_none, ["name", "age", "city"])
print("Head:")
print(df_none.head())
print("Info:")
print(df_none.info())
print()

# Test single row DataFrame
print("3. Single row DataFrame:")
single_row = [{"name": "Alice", "age": 25}]
df_single = TempDataFrame(single_row, ["name", "age"])
print("Shape:", df_single.shape)
print("Head:")
print(df_single.head())
print("Tail:")
print(df_single.tail())
print()

print("=== All edge case tests completed! ===")