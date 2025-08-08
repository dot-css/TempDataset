from tempdataset.core.datasets.sales import SalesDataset
import re

# Test ID formats and calculations
sales = SalesDataset(rows=3)
data = sales.generate()

print('Testing ID formats and calculations:')
for i, row in enumerate(data):
    print(f'Row {i+1}:')
    
    # Test order_id format: ORD-YYYY-NNNNNN
    order_id_pattern = r'^ORD-\d{4}-\d{6}$'
    print(f'  order_id: {row["order_id"]} - Valid: {bool(re.match(order_id_pattern, row["order_id"]))}')
    
    # Test customer_id format: CUST-NNNN
    customer_id_pattern = r'^CUST-\d{4}$'
    print(f'  customer_id: {row["customer_id"]} - Valid: {bool(re.match(customer_id_pattern, row["customer_id"]))}')
    
    # Test product_id format: PROD-AAANNN
    product_id_pattern = r'^PROD-[A-Z]{3}\d{3}$'
    print(f'  product_id: {row["product_id"]} - Valid: {bool(re.match(product_id_pattern, row["product_id"]))}')
    
    # Test calculations
    expected_total = row['quantity'] * row['unit_price']
    expected_final = row['total_price'] - row['discount']
    
    print(f'  quantity: {row["quantity"]}, unit_price: {row["unit_price"]:.2f}')
    print(f'  total_price: {row["total_price"]:.2f} (expected: {expected_total:.2f}) - Match: {abs(row["total_price"] - expected_total) < 0.01}')
    print(f'  discount: {row["discount"]:.2f}')
    print(f'  final_price: {row["final_price"]:.2f} (expected: {expected_final:.2f}) - Match: {abs(row["final_price"] - expected_final) < 0.01}')
    print(f'  profit: {row["profit"]:.2f} ({(row["profit"]/row["final_price"]*100):.1f}% of final_price)')
    print()