"""
Sales dataset generator.

Generates realistic sales data with 27 columns including order information,
customer details, product information, and financial calculations.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class SalesDataset(BaseDataset):
    """
    Sales dataset generator that creates realistic sales transaction data.
    
    Generates 27 columns of sales data including:
    - Order information (order_id, dates, priority)
    - Customer details (customer_id, name, email, demographics)
    - Product information (product_id, name, category, brand)
    - Financial data (prices, discounts, profit)
    - Geographic data (region, country, state, city)
    - Shipping and payment information
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the SalesDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._order_counter = 1
        self._customer_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Product categories and subcategories
        self.categories = {
            'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Cameras', 'Gaming'],
            'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes', 'Accessories', 'Outerwear'],
            'Home & Garden': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Tools', 'Appliances'],
            'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports', 'Winter Sports', 'Cycling'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children', 'Comics', 'Reference'],
            'Health & Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Supplements', 'Personal Care', 'Fragrances']
        }
        
        # Brands by category
        self.brands = {
            'Electronics': ['Apple', 'Samsung', 'Sony', 'LG', 'HP', 'Dell', 'Canon', 'Nintendo'],
            'Clothing': ['Nike', 'Adidas', 'Levi\'s', 'Gap', 'H&M', 'Zara', 'Under Armour', 'Puma'],
            'Home & Garden': ['IKEA', 'Home Depot', 'Lowe\'s', 'Target', 'Walmart', 'Wayfair', 'Ashley', 'KitchenAid'],
            'Sports': ['Nike', 'Adidas', 'Under Armour', 'Reebok', 'Puma', 'New Balance', 'Wilson', 'Spalding'],
            'Books': ['Penguin', 'Random House', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Scholastic'],
            'Health & Beauty': ['L\'Oreal', 'Maybelline', 'Revlon', 'Neutrogena', 'Olay', 'Clinique', 'MAC', 'Estee Lauder']
        }
        
        # Product names by category
        self.product_names = {
            'Electronics': {
                'Smartphones': ['iPhone Pro', 'Galaxy S Series', 'Pixel Phone', 'OnePlus Device'],
                'Laptops': ['MacBook Pro', 'ThinkPad', 'Surface Laptop', 'Gaming Laptop'],
                'Tablets': ['iPad', 'Galaxy Tab', 'Surface Pro', 'Fire Tablet'],
                'Headphones': ['AirPods', 'Wireless Headphones', 'Gaming Headset', 'Noise Cancelling'],
                'Cameras': ['DSLR Camera', 'Mirrorless Camera', 'Action Camera', 'Instant Camera'],
                'Gaming': ['Gaming Console', 'Controller', 'Gaming Mouse', 'Mechanical Keyboard']
            },
            'Clothing': {
                'Shirts': ['Cotton T-Shirt', 'Dress Shirt', 'Polo Shirt', 'Hoodie'],
                'Pants': ['Jeans', 'Chinos', 'Dress Pants', 'Joggers'],
                'Dresses': ['Summer Dress', 'Evening Dress', 'Casual Dress', 'Maxi Dress'],
                'Shoes': ['Running Shoes', 'Dress Shoes', 'Sneakers', 'Boots'],
                'Accessories': ['Watch', 'Belt', 'Wallet', 'Sunglasses'],
                'Outerwear': ['Jacket', 'Coat', 'Sweater', 'Vest']
            },
            'Home & Garden': {
                'Furniture': ['Sofa', 'Dining Table', 'Bed Frame', 'Office Chair'],
                'Kitchen': ['Coffee Maker', 'Blender', 'Cookware Set', 'Dinnerware'],
                'Bedding': ['Sheet Set', 'Comforter', 'Pillow', 'Mattress'],
                'Decor': ['Wall Art', 'Lamp', 'Vase', 'Mirror'],
                'Tools': ['Drill', 'Hammer', 'Screwdriver Set', 'Tool Box'],
                'Appliances': ['Microwave', 'Vacuum', 'Air Fryer', 'Dishwasher']
            },
            'Sports': {
                'Fitness': ['Treadmill', 'Dumbbells', 'Yoga Mat', 'Resistance Bands'],
                'Outdoor': ['Tent', 'Sleeping Bag', 'Hiking Boots', 'Backpack'],
                'Team Sports': ['Basketball', 'Soccer Ball', 'Baseball Glove', 'Football'],
                'Water Sports': ['Swimsuit', 'Goggles', 'Life Jacket', 'Surfboard'],
                'Winter Sports': ['Ski Boots', 'Snowboard', 'Winter Jacket', 'Gloves'],
                'Cycling': ['Mountain Bike', 'Helmet', 'Bike Lock', 'Water Bottle']
            },
            'Books': {
                'Fiction': ['Mystery Novel', 'Romance Novel', 'Sci-Fi Book', 'Fantasy Series'],
                'Non-Fiction': ['Biography', 'Self-Help Book', 'History Book', 'Travel Guide'],
                'Educational': ['Textbook', 'Study Guide', 'Workbook', 'Reference Manual'],
                'Children': ['Picture Book', 'Chapter Book', 'Activity Book', 'Board Book'],
                'Comics': ['Graphic Novel', 'Comic Series', 'Manga', 'Superhero Comic'],
                'Reference': ['Dictionary', 'Encyclopedia', 'Atlas', 'Cookbook']
            },
            'Health & Beauty': {
                'Skincare': ['Moisturizer', 'Cleanser', 'Serum', 'Sunscreen'],
                'Makeup': ['Foundation', 'Lipstick', 'Mascara', 'Eyeshadow'],
                'Hair Care': ['Shampoo', 'Conditioner', 'Hair Styling', 'Hair Treatment'],
                'Supplements': ['Vitamins', 'Protein Powder', 'Omega-3', 'Probiotics'],
                'Personal Care': ['Toothpaste', 'Deodorant', 'Body Wash', 'Lotion'],
                'Fragrances': ['Perfume', 'Cologne', 'Body Spray', 'Essential Oil']
            }
        }
        
        # Geographic data
        self.regions = ['North', 'South', 'East', 'West', 'Central']
        
        # Customer segments
        self.customer_segments = ['Consumer', 'Corporate', 'Home Office']
        
        # Order priorities
        self.order_priorities = ['Low', 'Medium', 'High', 'Critical']
        
        # Shipping modes
        self.shipping_modes = ['Standard', 'Express', 'Overnight', 'Same Day']
        
        # Payment methods
        self.payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'Cash', 'Check']
        
        # Sales representatives
        self.sales_reps = [
            'John Smith', 'Sarah Johnson', 'Mike Davis', 'Lisa Wilson', 'David Brown',
            'Jennifer Garcia', 'Robert Miller', 'Amanda Taylor', 'Chris Anderson', 'Michelle White'
        ]
        
        # Gender options
        self.genders = ['Male', 'Female', 'Other']
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate sales dataset rows.
        
        Returns:
            List of dictionaries representing sales transaction rows
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
        """Generate a single sales transaction row."""
        
        # Generate order date (within last 2 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        order_date = self.faker_utils.date_between(start_date, end_date)
        
        # Generate customer information
        customer_name = self.faker_utils.name()
        customer_email = self.faker_utils.email(customer_name)
        
        # Generate product information
        category = random.choice(list(self.categories.keys()))
        subcategory = random.choice(self.categories[category])
        brand = random.choice(self.brands[category])
        product_name = random.choice(self.product_names[category][subcategory])
        
        # Generate quantities and pricing
        quantity = random.randint(1, 10)
        unit_price = self._generate_unit_price(category)
        total_price = quantity * unit_price
        discount = round(total_price * random.uniform(0, 0.20), 2)  # 0-20% discount
        final_price = total_price - discount
        profit = round(final_price * random.uniform(0.10, 0.30), 2)  # 10-30% profit
        
        # Generate dates with proper relationships
        ship_date = order_date + timedelta(days=random.randint(1, 7))
        delivery_date = ship_date + timedelta(days=random.randint(2, 14))
        
        # Generate geographic information
        region = random.choice(self.regions)
        country = self.faker_utils.country()
        state = self.faker_utils.state()
        city = self.faker_utils.city()
        postal_code = self.faker_utils.postal_code()
        
        # Generate customer demographics
        customer_age = random.randint(18, 80)
        customer_gender = random.choice(self.genders)
        
        return {
            'order_id': self._generate_order_id(order_date),
            'customer_id': self._generate_customer_id(),
            'customer_name': customer_name,
            'customer_email': customer_email,
            'product_id': self._generate_product_id(),
            'product_name': product_name,
            'category': category,
            'subcategory': subcategory,
            'brand': brand,
            'quantity': quantity,
            'unit_price': round(unit_price, 2),
            'total_price': round(total_price, 2),
            'discount': discount,
            'final_price': round(final_price, 2),
            'order_date': order_date.strftime('%Y-%m-%d'),
            'ship_date': ship_date.strftime('%Y-%m-%d'),
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'sales_rep': random.choice(self.sales_reps),
            'region': region,
            'country': country,
            'state/province': state,
            'city': city,
            'postal_code': postal_code,
            'customer_segment': random.choice(self.customer_segments),
            'order_priority': random.choice(self.order_priorities),
            'shipping_mode': random.choice(self.shipping_modes),
            'payment_method': random.choice(self.payment_methods),
            'customer_age': customer_age,
            'customer_gender': customer_gender,
            'profit': profit
        }
    
    def _generate_order_id(self, order_date: datetime) -> str:
        """
        Generate order ID in format "ORD-YYYY-NNNNNN".
        
        Args:
            order_date: Date of the order
            
        Returns:
            Formatted order ID
        """
        year = order_date.year
        order_num = str(self._order_counter).zfill(6)
        self._order_counter += 1
        return f"ORD-{year}-{order_num}"
    
    def _generate_customer_id(self) -> str:
        """
        Generate customer ID in format "CUST-NNNN".
        
        Returns:
            Formatted customer ID
        """
        customer_num = str(self._customer_counter).zfill(4)
        self._customer_counter += 1
        return f"CUST-{customer_num}"
    
    def _generate_product_id(self) -> str:
        """
        Generate product ID in format "PROD-AAANNN".
        
        Returns:
            Formatted product ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"PROD-{letters}{numbers}"
    
    def _generate_unit_price(self, category: str) -> float:
        """
        Generate realistic unit price based on category.
        
        Args:
            category: Product category
            
        Returns:
            Unit price as float
        """
        price_ranges = {
            'Electronics': (50, 2000),
            'Clothing': (15, 300),
            'Home & Garden': (20, 1500),
            'Sports': (25, 800),
            'Books': (10, 50),
            'Health & Beauty': (5, 200)
        }
        
        min_price, max_price = price_ranges.get(category, (10, 100))
        return random.uniform(min_price, max_price)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'order_id': 'string',
            'customer_id': 'string',
            'customer_name': 'string',
            'customer_email': 'string',
            'product_id': 'string',
            'product_name': 'string',
            'category': 'string',
            'subcategory': 'string',
            'brand': 'string',
            'quantity': 'integer',
            'unit_price': 'float',
            'total_price': 'float',
            'discount': 'float',
            'final_price': 'float',
            'order_date': 'date',
            'ship_date': 'date',
            'delivery_date': 'date',
            'sales_rep': 'string',
            'region': 'string',
            'country': 'string',
            'state/province': 'string',
            'city': 'string',
            'postal_code': 'string',
            'customer_segment': 'string',
            'order_priority': 'string',
            'shipping_mode': 'string',
            'payment_method': 'string',
            'customer_age': 'integer',
            'customer_gender': 'string',
            'profit': 'float'
        }