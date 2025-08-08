from tempdataset.core.datasets.sales import SalesDataset
from datetime import datetime

# Test date relationships
sales = SalesDataset(rows=5)
data = sales.generate()

print('Testing date relationships:')
for i, row in enumerate(data):
    print(f'Row {i+1}:')
    
    order_date = datetime.strptime(row['order_date'], '%Y-%m-%d')
    ship_date = datetime.strptime(row['ship_date'], '%Y-%m-%d')
    delivery_date = datetime.strptime(row['delivery_date'], '%Y-%m-%d')
    
    ship_days = (ship_date - order_date).days
    delivery_days = (delivery_date - ship_date).days
    
    print(f'  order_date: {row["order_date"]}')
    print(f'  ship_date: {row["ship_date"]} ({ship_days} days after order)')
    print(f'  delivery_date: {row["delivery_date"]} ({delivery_days} days after ship)')
    
    # Verify constraints
    ship_valid = 1 <= ship_days <= 7
    delivery_valid = 2 <= delivery_days <= 14
    
    print(f'  Ship date valid (1-7 days): {ship_valid}')
    print(f'  Delivery date valid (2-14 days): {delivery_valid}')
    print()