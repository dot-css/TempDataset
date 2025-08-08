#!/usr/bin/env python3
"""
Quick test of TempDataFrame implementation
"""

from tempdataset.core.utils.data_frame import TempDataFrame

# Test data
test_data = [
    {"name": "Alice", "age": 25, "city": "New York", "salary": 50000.0},
    {"name": "Bob", "age": 30, "city": "San Francisco", "salary": 75000.0},
    {"name": "Charlie", "age": 35, "city": "Chicago", "salary": 60000.0},
    {"name": "Diana", "age": 28, "city": "Boston", "salary": 65000.0},
    {"name": "Eve", "age": 32, "city": "Seattle", "salary": 70000.0}
]

columns = ["name", "age", "city", "salary"]

# Create TempDataFrame
df = TempDataFrame(test_data, columns)

print("=== Testing TempDataFrame ===")
print()

print("Shape:", df.shape)
print("Columns:", df.columns)
print()

print("Head (default 5):")
print(df.head())
print()

print("Head (3):")
print(df.head(3))
print()

print("Tail (default 5):")
print(df.tail())
print()

print("Tail (2):")
print(df.tail(2))
print()

print("Info:")
print(df.info())
print()

# Test CSV export
print("Testing CSV export...")
df.to_csv("test_output.csv")
print("CSV exported to test_output.csv")

# Test JSON export
print("Testing JSON export...")
df.to_json("test_output.json")
print("JSON exported to test_output.json")

print()
print("=== All tests completed successfully! ===")