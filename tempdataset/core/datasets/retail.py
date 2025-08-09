"""
Retail dataset generator.

Generates realistic retail store operations & POS transactions data with comprehensive
columns including transaction details, store information, product data, and inventory tracking.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class RetailDataset(BaseDataset):
    """
    Retail store operations & POS transactions dataset generator.
    
    Generates comprehensive retail data including:
    - Transaction information (transaction_id, receipt_number, datetime)
    - Store details (store_id, name, type, location)
    - POS and cashier information
    - Product details (product_id, name, category, brand)
    - Pricing and discount calculations
    - Payment and loyalty information
    - Inventory tracking (before/after sale)
    - Financial metrics (gross margin)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the RetailDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._transaction_counter = 1
        self._receipt_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Store types
        self.store_types = ['Supermarket', 'Department Store', 'Convenience Store', 'Specialty Store']
        
        # Store names by type
        self.store_names = {
            'Supermarket': ['FreshMart', 'GroceryPlus', 'SuperSave', 'FoodWorld', 'MegaMart'],
            'Department Store': ['StyleHub', 'Fashion Central', 'TrendMart', 'EliteStore', 'ShopAll'],
            'Convenience Store': ['QuickStop', 'Corner Store', 'EasyMart', 'FastShop', '24/7 Store'],
            'Specialty Store': ['TechZone', 'BookNook', 'SportsPro', 'BeautyBox', 'HomeDecor']
        }
        
        # Product categories and subcategories
        self.categories = {
            'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Cameras', 'Gaming'],
            'Grocery': ['Fresh Produce', 'Dairy', 'Meat', 'Bakery', 'Beverages', 'Snacks'],
            'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes', 'Accessories', 'Outerwear'],
            'Home': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Tools', 'Appliances'],
            'Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Fragrances', 'Personal Care', 'Wellness'],
            'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports', 'Winter Sports', 'Cycling']
        }
        
        # Brands by category
        self.brands = {
            'Electronics': ['Apple', 'Samsung', 'Sony', 'LG', 'HP', 'Dell', 'Canon', 'Nintendo'],
            'Grocery': ['Organic Valley', 'Kraft', 'Nestle', 'Coca-Cola', 'Pepsi', 'General Mills', 'Kelloggs', 'Unilever'],
            'Clothing': ['Nike', 'Adidas', 'Levi\'s', 'Gap', 'H&M', 'Zara', 'Under Armour', 'Puma'],
            'Home': ['IKEA', 'Ashley', 'Wayfair', 'KitchenAid', 'Black & Decker', 'Cuisinart', 'Hamilton Beach', 'Dyson'],
            'Beauty': ['L\'Oreal', 'Maybelline', 'Revlon', 'Neutrogena', 'Olay', 'Clinique', 'MAC', 'Estee Lauder'],
            'Sports': ['Nike', 'Adidas', 'Under Armour', 'Reebok', 'Puma', 'New Balance', 'Wilson', 'Spalding']
        }
        
        # Product names by category and subcategory
        self.product_names = {
            'Electronics': {
                'Smartphones': ['iPhone Pro', 'Galaxy S Series', 'Pixel Phone', 'OnePlus Device'],
                'Laptops': ['MacBook Pro', 'ThinkPad', 'Surface Laptop', 'Gaming Laptop'],
                'Tablets': ['iPad', 'Galaxy Tab', 'Surface Pro', 'Fire Tablet'],
                'Headphones': ['AirPods', 'Wireless Headphones', 'Gaming Headset', 'Noise Cancelling'],
                'Cameras': ['DSLR Camera', 'Mirrorless Camera', 'Action Camera', 'Instant Camera'],
                'Gaming': ['Gaming Console', 'Controller', 'Gaming Mouse', 'Mechanical Keyboard']
            },
            'Grocery': {
                'Fresh Produce': ['Organic Apples', 'Fresh Bananas', 'Leafy Greens', 'Tomatoes'],
                'Dairy': ['Whole Milk', 'Greek Yogurt', 'Cheddar Cheese', 'Butter'],
                'Meat': ['Ground Beef', 'Chicken Breast', 'Salmon Fillet', 'Turkey Slices'],
                'Bakery': ['Whole Wheat Bread', 'Croissants', 'Bagels', 'Muffins'],
                'Beverages': ['Orange Juice', 'Coffee Beans', 'Sparkling Water', 'Energy Drink'],
                'Snacks': ['Potato Chips', 'Granola Bars', 'Mixed Nuts', 'Chocolate']
            },
            'Clothing': {
                'Shirts': ['Cotton T-Shirt', 'Dress Shirt', 'Polo Shirt', 'Hoodie'],
                'Pants': ['Jeans', 'Chinos', 'Dress Pants', 'Joggers'],
                'Dresses': ['Summer Dress', 'Evening Dress', 'Casual Dress', 'Maxi Dress'],
                'Shoes': ['Running Shoes', 'Dress Shoes', 'Sneakers', 'Boots'],
                'Accessories': ['Watch', 'Belt', 'Wallet', 'Sunglasses'],
                'Outerwear': ['Jacket', 'Coat', 'Sweater', 'Vest']
            },
            'Home': {
                'Furniture': ['Sofa', 'Dining Table', 'Bed Frame', 'Office Chair'],
                'Kitchen': ['Coffee Maker', 'Blender', 'Cookware Set', 'Dinnerware'],
                'Bedding': ['Sheet Set', 'Comforter', 'Pillow', 'Mattress Topper'],
                'Decor': ['Wall Art', 'Table Lamp', 'Decorative Vase', 'Mirror'],
                'Tools': ['Cordless Drill', 'Hammer Set', 'Screwdriver Kit', 'Tool Box'],
                'Appliances': ['Microwave', 'Vacuum Cleaner', 'Air Fryer', 'Coffee Machine']
            },
            'Beauty': {
                'Skincare': ['Moisturizer', 'Facial Cleanser', 'Anti-Aging Serum', 'Sunscreen'],
                'Makeup': ['Foundation', 'Lipstick', 'Mascara', 'Eyeshadow Palette'],
                'Hair Care': ['Shampoo', 'Conditioner', 'Hair Styling Gel', 'Hair Treatment'],
                'Fragrances': ['Perfume', 'Cologne', 'Body Spray', 'Essential Oil'],
                'Personal Care': ['Electric Toothbrush', 'Deodorant', 'Body Wash', 'Hand Lotion'],
                'Wellness': ['Vitamins', 'Protein Powder', 'Omega-3', 'Probiotics']
            },
            'Sports': {
                'Fitness': ['Yoga Mat', 'Dumbbells', 'Resistance Bands', 'Exercise Ball'],
                'Outdoor': ['Hiking Boots', 'Camping Tent', 'Sleeping Bag', 'Backpack'],
                'Team Sports': ['Basketball', 'Soccer Ball', 'Baseball Glove', 'Football'],
                'Water Sports': ['Swimsuit', 'Swimming Goggles', 'Life Jacket', 'Water Bottle'],
                'Winter Sports': ['Ski Boots', 'Snowboard', 'Winter Jacket', 'Thermal Gloves'],
                'Cycling': ['Mountain Bike', 'Bike Helmet', 'Bike Lock', 'Cycling Shorts']
            }
        }
        
        # Payment methods
        self.payment_methods = ['Cash', 'Credit Card', 'Debit Card', 'Mobile Payment', 'Gift Card']
        
        # Transaction statuses
        self.transaction_statuses = ['Completed', 'Cancelled', 'Refunded']
        
        # Shift IDs
        self.shift_ids = ['SHIFT-AM-001', 'SHIFT-PM-002', 'SHIFT-EVE-003', 'SHIFT-NIGHT-004']
        
        # Cashier names
        self.cashier_names = [
            'Alice Johnson', 'Bob Smith', 'Carol Davis', 'David Wilson', 'Emma Brown',
            'Frank Miller', 'Grace Taylor', 'Henry Anderson', 'Ivy Martinez', 'Jack Thompson',
            'Kate Garcia', 'Liam Rodriguez', 'Mia Lopez', 'Noah Lee', 'Olivia White'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate retail dataset rows.
        
        Returns:
            List of dictionaries representing retail transaction rows
        """
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        data = []
        
        for i in range(self.rows):
            row = self._generate_row()
            data.append(row)
        
        return data
    
    def _generate_row(self) -> Dict[str, Any]:
        """Generate a single retail transaction row."""
        
        # Generate transaction datetime (within last year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        transaction_date = self.faker_utils.date_between(start_date, end_date)
        
        # Add time component
        hour = random.randint(8, 22)  # Store hours 8 AM to 10 PM
        minute = random.randint(0, 59)
        second = random.randint(0, 59)
        transaction_datetime = datetime.combine(transaction_date, datetime.min.time()).replace(hour=hour, minute=minute, second=second)
        
        # Generate store information
        store_type = random.choice(self.store_types)
        store_name = random.choice(self.store_names[store_type])
        
        # Generate location
        location_city = self.faker_utils.city()
        location_state_province = self.faker_utils.state()
        location_country = self.faker_utils.country()
        
        # Generate cashier information
        cashier_name = random.choice(self.cashier_names)
        
        # Generate product information
        category = random.choice(list(self.categories.keys()))
        subcategory = random.choice(self.categories[category])
        brand = random.choice(self.brands[category])
        product_name = random.choice(self.product_names[category][subcategory])
        
        # Generate quantities and pricing
        quantity = random.randint(1, 20)
        unit_price = round(self._generate_unit_price(category), 2)  # Round unit price
        total_price = round(quantity * unit_price, 2)  # Round to avoid floating point errors
        discount_percentage = round(random.uniform(0, 50), 2)
        discount_amount = round(total_price * discount_percentage / 100, 2)
        final_price = round(total_price - discount_amount, 2)
        
        # Generate inventory data
        inventory_before_sale = random.randint(quantity, quantity + 100)  # Ensure enough stock
        
        # Generate transaction status
        transaction_status = random.choices(
            self.transaction_statuses,
            weights=[85, 10, 5],  # Most completed, some cancelled/refunded
            k=1
        )[0]
        
        # Adjust inventory after sale based on status
        if transaction_status == 'Completed':
            inventory_after_sale = inventory_before_sale - quantity
        else:
            inventory_after_sale = inventory_before_sale  # No inventory change for cancelled/refunded
        
        # Generate loyalty information
        loyalty_member = random.choice([True, False])
        loyalty_points_earned = 0
        if loyalty_member and transaction_status == 'Completed':
            loyalty_points_earned = random.randint(0, 500)
        
        # Generate gross margin (10-40% of final price)
        gross_margin = round(final_price * random.uniform(0.10, 0.40), 2)
        
        # Generate shift ID based on time
        if 6 <= hour < 14:
            shift_id = 'SHIFT-AM-001'
        elif 14 <= hour < 22:
            shift_id = 'SHIFT-PM-002'
        else:
            shift_id = 'SHIFT-NIGHT-004'
        
        # Generate notes (optional)
        notes = None
        if random.random() < 0.1:  # 10% chance of having notes
            note_options = [
                'Customer requested gift receipt',
                'Price match applied',
                'Manager approval required',
                'Customer loyalty discount applied',
                'Bulk purchase discount',
                'Seasonal promotion applied'
            ]
            notes = random.choice(note_options)
        
        return {
            'transaction_id': self._generate_transaction_id(transaction_datetime),
            'store_id': self._generate_store_id(),
            'store_name': store_name,
            'store_type': store_type,
            'location_city': location_city,
            'location_state_province': location_state_province,
            'location_country': location_country,
            'pos_terminal_id': self._generate_pos_terminal_id(),
            'cashier_id': self._generate_cashier_id(),
            'cashier_name': cashier_name,
            'transaction_datetime': transaction_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'product_id': self._generate_product_id(),
            'product_name': product_name,
            'category': category,
            'subcategory': subcategory,
            'brand': brand,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'total_price': round(total_price, 2),
            'discount_percentage': discount_percentage,
            'discount_amount': discount_amount,
            'final_price': round(final_price, 2),
            'payment_method': random.choice(self.payment_methods),
            'loyalty_member': loyalty_member,
            'loyalty_points_earned': loyalty_points_earned,
            'transaction_status': transaction_status,
            'inventory_before_sale': inventory_before_sale,
            'inventory_after_sale': inventory_after_sale,
            'supplier_id': self._generate_supplier_id(),
            'gross_margin': gross_margin,
            'receipt_number': self._generate_receipt_number(),
            'shift_id': shift_id,
            'notes': notes
        }
    
    def _generate_transaction_id(self, transaction_datetime: datetime) -> str:
        """
        Generate transaction ID in format "POS-YYYY-NNNNNN".
        
        Args:
            transaction_datetime: Date and time of the transaction
            
        Returns:
            Formatted transaction ID
        """
        year = transaction_datetime.year
        transaction_num = str(self._transaction_counter).zfill(6)
        self._transaction_counter += 1
        return f"POS-{year}-{transaction_num}"
    
    def _generate_store_id(self) -> str:
        """
        Generate store ID in format "STORE-NNN".
        
        Returns:
            Formatted store ID
        """
        store_num = str(random.randint(1, 999)).zfill(3)
        return f"STORE-{store_num}"
    
    def _generate_pos_terminal_id(self) -> str:
        """
        Generate POS terminal ID in format "POS-NN".
        
        Returns:
            Formatted POS terminal ID
        """
        terminal_num = str(random.randint(1, 20)).zfill(2)
        return f"POS-{terminal_num}"
    
    def _generate_cashier_id(self) -> str:
        """
        Generate cashier ID in format "CASH-NNNN".
        
        Returns:
            Formatted cashier ID
        """
        cashier_num = str(random.randint(1, 9999)).zfill(4)
        return f"CASH-{cashier_num}"
    
    def _generate_product_id(self) -> str:
        """
        Generate product ID in format "PROD-AAANNN".
        
        Returns:
            Formatted product ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"PROD-{letters}{numbers}"
    
    def _generate_supplier_id(self) -> str:
        """
        Generate supplier ID in format "SUPP-NNNN".
        
        Returns:
            Formatted supplier ID
        """
        supplier_num = str(random.randint(1, 9999)).zfill(4)
        return f"SUPP-{supplier_num}"
    
    def _generate_receipt_number(self) -> str:
        """
        Generate receipt number in format "RCPT-NNNNNN".
        
        Returns:
            Formatted receipt number
        """
        receipt_num = str(self._receipt_counter).zfill(6)
        self._receipt_counter += 1
        return f"RCPT-{receipt_num}"
    
    def _generate_unit_price(self, category: str) -> float:
        """
        Generate realistic unit price based on category.
        
        Args:
            category: Product category
            
        Returns:
            Unit price as float
        """
        price_ranges = {
            'Electronics': (25, 2000),
            'Grocery': (1, 50),
            'Clothing': (10, 300),
            'Home': (15, 1500),
            'Beauty': (5, 200),
            'Sports': (20, 800)
        }
        
        min_price, max_price = price_ranges.get(category, (5, 100))
        return random.uniform(min_price, max_price)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'transaction_id': 'string',
            'store_id': 'string',
            'store_name': 'string',
            'store_type': 'string',
            'location_city': 'string',
            'location_state_province': 'string',
            'location_country': 'string',
            'pos_terminal_id': 'string',
            'cashier_id': 'string',
            'cashier_name': 'string',
            'transaction_datetime': 'datetime',
            'product_id': 'string',
            'product_name': 'string',
            'category': 'string',
            'subcategory': 'string',
            'brand': 'string',
            'quantity': 'integer',
            'unit_price': 'float',
            'total_price': 'float',
            'discount_percentage': 'float',
            'discount_amount': 'float',
            'final_price': 'float',
            'payment_method': 'string',
            'loyalty_member': 'boolean',
            'loyalty_points_earned': 'integer',
            'transaction_status': 'string',
            'inventory_before_sale': 'integer',
            'inventory_after_sale': 'integer',
            'supplier_id': 'string',
            'gross_margin': 'float',
            'receipt_number': 'string',
            'shift_id': 'string',
            'notes': 'string'
        }