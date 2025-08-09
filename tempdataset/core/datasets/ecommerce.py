"""
E-commerce dataset generator.

Generates realistic e-commerce transaction data with comprehensive columns including
customer information, product details, pricing, shipping, and business metrics.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class EcommerceDataset(BaseDataset):
    """
    E-commerce dataset generator that creates realistic transaction data.
    
    Generates comprehensive e-commerce data including:
    - Transaction and customer information
    - Product details with categories and brands
    - Pricing with discounts and profit calculations
    - Shipping and delivery information
    - Geographic and demographic data
    - Reviews and returns data
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the EcommerceDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._transaction_counter = 1
        self._customer_counter = 1
        self._seller_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Product categories and subcategories
        self.categories = {
            'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Headphones', 'Cameras', 'Gaming', 'Wearables', 'Audio'],
            'Fashion': ['Clothing', 'Shoes', 'Accessories', 'Jewelry', 'Bags', 'Watches', 'Sunglasses', 'Belts'],
            'Home & Garden': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Tools', 'Appliances', 'Lighting', 'Storage'],
            'Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Fragrances', 'Personal Care', 'Bath & Body', 'Nail Care', 'Men\'s Grooming'],
            'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports', 'Winter Sports', 'Cycling', 'Running', 'Yoga'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children', 'Comics', 'Reference', 'Self-Help', 'Biography']
        }
        
        # Brands by category
        self.brands = {
            'Electronics': ['Apple', 'Samsung', 'Sony', 'LG', 'HP', 'Dell', 'Canon', 'Nintendo', 'Microsoft', 'Google'],
            'Fashion': ['Nike', 'Adidas', 'Levi\'s', 'Gap', 'H&M', 'Zara', 'Under Armour', 'Puma', 'Calvin Klein', 'Tommy Hilfiger'],
            'Home & Garden': ['IKEA', 'Home Depot', 'Lowe\'s', 'Target', 'Walmart', 'Wayfair', 'Ashley', 'KitchenAid', 'Black & Decker', 'Cuisinart'],
            'Beauty': ['L\'Oreal', 'Maybelline', 'Revlon', 'Neutrogena', 'Olay', 'Clinique', 'MAC', 'Estee Lauder', 'CoverGirl', 'Dove'],
            'Sports': ['Nike', 'Adidas', 'Under Armour', 'Reebok', 'Puma', 'New Balance', 'Wilson', 'Spalding', 'Coleman', 'The North Face'],
            'Books': ['Penguin', 'Random House', 'HarperCollins', 'Simon & Schuster', 'Macmillan', 'Scholastic', 'Oxford', 'Cambridge']
        }
        
        # Product names by category and subcategory
        self.product_names = {
            'Electronics': {
                'Smartphones': ['iPhone Pro Max', 'Galaxy S Ultra', 'Pixel Phone', 'OnePlus Device', 'Xiaomi Phone'],
                'Laptops': ['MacBook Pro', 'ThinkPad X1', 'Surface Laptop', 'Gaming Laptop', 'Chromebook'],
                'Tablets': ['iPad Pro', 'Galaxy Tab', 'Surface Pro', 'Fire Tablet', 'iPad Air'],
                'Headphones': ['AirPods Pro', 'Wireless Headphones', 'Gaming Headset', 'Noise Cancelling', 'Bluetooth Earbuds'],
                'Cameras': ['DSLR Camera', 'Mirrorless Camera', 'Action Camera', 'Instant Camera', 'Security Camera'],
                'Gaming': ['Gaming Console', 'Wireless Controller', 'Gaming Mouse', 'Mechanical Keyboard', 'Gaming Chair'],
                'Wearables': ['Smart Watch', 'Fitness Tracker', 'Smart Ring', 'VR Headset', 'Smart Glasses'],
                'Audio': ['Bluetooth Speaker', 'Sound Bar', 'Home Theater', 'Portable Speaker', 'Smart Speaker']
            },
            'Fashion': {
                'Clothing': ['Cotton T-Shirt', 'Dress Shirt', 'Polo Shirt', 'Hoodie', 'Jeans', 'Dress Pants'],
                'Shoes': ['Running Shoes', 'Dress Shoes', 'Sneakers', 'Boots', 'Sandals', 'High Heels'],
                'Accessories': ['Leather Wallet', 'Designer Handbag', 'Baseball Cap', 'Scarf', 'Gloves', 'Hat'],
                'Jewelry': ['Gold Necklace', 'Silver Ring', 'Diamond Earrings', 'Bracelet', 'Pendant', 'Cufflinks'],
                'Bags': ['Backpack', 'Messenger Bag', 'Tote Bag', 'Laptop Bag', 'Travel Bag', 'Clutch'],
                'Watches': ['Smart Watch', 'Analog Watch', 'Digital Watch', 'Luxury Watch', 'Sports Watch', 'Fashion Watch'],
                'Sunglasses': ['Aviator Sunglasses', 'Wayfarer Sunglasses', 'Cat Eye Sunglasses', 'Sports Sunglasses', 'Designer Sunglasses', 'Polarized Sunglasses'],
                'Belts': ['Leather Belt', 'Canvas Belt', 'Designer Belt', 'Dress Belt', 'Casual Belt', 'Chain Belt']
            },
            'Home & Garden': {
                'Furniture': ['Sofa Set', 'Dining Table', 'Bed Frame', 'Office Chair', 'Coffee Table', 'Bookshelf'],
                'Kitchen': ['Coffee Maker', 'Blender', 'Cookware Set', 'Dinnerware', 'Stand Mixer', 'Food Processor'],
                'Bedding': ['Sheet Set', 'Comforter', 'Memory Foam Pillow', 'Mattress', 'Blanket', 'Duvet Cover'],
                'Decor': ['Wall Art', 'Table Lamp', 'Decorative Vase', 'Mirror', 'Candles', 'Picture Frame'],
                'Tools': ['Cordless Drill', 'Hammer Set', 'Screwdriver Set', 'Tool Box', 'Saw', 'Level'],
                'Appliances': ['Microwave Oven', 'Vacuum Cleaner', 'Air Fryer', 'Dishwasher', 'Washing Machine', 'Refrigerator'],
                'Lighting': ['LED Bulbs', 'Ceiling Fan', 'Floor Lamp', 'Pendant Light', 'String Lights', 'Desk Lamp'],
                'Storage': ['Storage Bins', 'Closet Organizer', 'Shoe Rack', 'Storage Cabinet', 'Drawer Organizer', 'Garage Storage']
            },
            'Beauty': {
                'Skincare': ['Moisturizer', 'Facial Cleanser', 'Anti-Aging Serum', 'Sunscreen', 'Face Mask', 'Toner'],
                'Makeup': ['Foundation', 'Lipstick', 'Mascara', 'Eyeshadow Palette', 'Concealer', 'Blush'],
                'Hair Care': ['Shampoo', 'Conditioner', 'Hair Styling Gel', 'Hair Treatment', 'Hair Dryer', 'Curling Iron'],
                'Fragrances': ['Eau de Parfum', 'Cologne', 'Body Spray', 'Essential Oil', 'Perfume Set', 'Travel Size Fragrance'],
                'Personal Care': ['Electric Toothbrush', 'Deodorant', 'Body Wash', 'Hand Lotion', 'Lip Balm', 'Face Wash'],
                'Bath & Body': ['Body Lotion', 'Bath Bombs', 'Shower Gel', 'Body Scrub', 'Bath Salts', 'Body Oil'],
                'Nail Care': ['Nail Polish', 'Nail File', 'Cuticle Oil', 'Nail Art Kit', 'Base Coat', 'Top Coat'],
                'Men\'s Grooming': ['Beard Oil', 'Shaving Cream', 'Aftershave', 'Hair Pomade', 'Face Moisturizer', 'Body Wash']
            },
            'Sports': {
                'Fitness': ['Treadmill', 'Dumbbells', 'Yoga Mat', 'Resistance Bands', 'Exercise Bike', 'Pull-up Bar'],
                'Outdoor': ['Camping Tent', 'Sleeping Bag', 'Hiking Boots', 'Backpack', 'Camping Chair', 'Portable Grill'],
                'Team Sports': ['Basketball', 'Soccer Ball', 'Baseball Glove', 'Football', 'Tennis Racket', 'Volleyball'],
                'Water Sports': ['Swimsuit', 'Swimming Goggles', 'Life Jacket', 'Surfboard', 'Snorkel Set', 'Water Bottle'],
                'Winter Sports': ['Ski Boots', 'Snowboard', 'Winter Jacket', 'Ski Gloves', 'Snow Goggles', 'Thermal Underwear'],
                'Cycling': ['Mountain Bike', 'Bike Helmet', 'Bike Lock', 'Water Bottle', 'Cycling Shorts', 'Bike Light'],
                'Running': ['Running Shoes', 'Running Watch', 'Athletic Shorts', 'Sports Bra', 'Running Belt', 'Compression Socks'],
                'Yoga': ['Yoga Mat', 'Yoga Blocks', 'Yoga Strap', 'Meditation Cushion', 'Yoga Towel', 'Yoga Pants']
            },
            'Books': {
                'Fiction': ['Mystery Novel', 'Romance Novel', 'Sci-Fi Book', 'Fantasy Series', 'Thriller', 'Historical Fiction'],
                'Non-Fiction': ['Biography', 'Self-Help Book', 'History Book', 'Travel Guide', 'Business Book', 'Health & Wellness'],
                'Educational': ['Textbook', 'Study Guide', 'Workbook', 'Reference Manual', 'Language Learning', 'Test Prep'],
                'Children': ['Picture Book', 'Chapter Book', 'Activity Book', 'Board Book', 'Coloring Book', 'Educational Toy'],
                'Comics': ['Graphic Novel', 'Comic Series', 'Manga', 'Superhero Comic', 'Indie Comic', 'Art Book'],
                'Reference': ['Dictionary', 'Encyclopedia', 'Atlas', 'Cookbook', 'Manual', 'Guide Book'],
                'Self-Help': ['Productivity Book', 'Motivation Book', 'Personal Development', 'Career Guide', 'Relationship Guide', 'Finance Book'],
                'Biography': ['Celebrity Biography', 'Historical Figure', 'Business Leader', 'Sports Figure', 'Political Figure', 'Artist Biography']
            }
        }
        
        # Customer segments
        self.customer_segments = ['Consumer', 'Corporate', 'Home Office']
        
        # Payment methods
        self.payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer', 'COD']
        
        # Shipping modes with delivery time ranges
        self.shipping_modes = {
            'Standard': (5, 10),
            'Express': (2, 4),
            'Overnight': (1, 1)
        }
        
        # Order statuses
        self.order_statuses = ['Pending', 'Processing', 'Shipped', 'Delivered', 'Cancelled', 'Returned']
        
        # Countries with states/provinces and cities
        self.geographic_data = {
            'United States': {
                'California': ['Los Angeles', 'San Francisco', 'San Diego', 'Sacramento'],
                'New York': ['New York City', 'Buffalo', 'Rochester', 'Albany'],
                'Texas': ['Houston', 'Dallas', 'Austin', 'San Antonio'],
                'Florida': ['Miami', 'Orlando', 'Tampa', 'Jacksonville']
            },
            'Canada': {
                'Ontario': ['Toronto', 'Ottawa', 'Hamilton', 'London'],
                'Quebec': ['Montreal', 'Quebec City', 'Laval', 'Gatineau'],
                'British Columbia': ['Vancouver', 'Victoria', 'Surrey', 'Burnaby']
            },
            'United Kingdom': {
                'England': ['London', 'Manchester', 'Birmingham', 'Liverpool'],
                'Scotland': ['Edinburgh', 'Glasgow', 'Aberdeen', 'Dundee'],
                'Wales': ['Cardiff', 'Swansea', 'Newport', 'Wrexham']
            }
        }
        
        # Coupon codes
        self.coupon_codes = [
            'SAVE10', 'WELCOME20', 'FIRST15', 'SUMMER25', 'WINTER30', 'SPRING20',
            'FALL15', 'HOLIDAY50', 'NEWUSER', 'LOYALTY10', 'FLASH20', 'WEEKEND15'
        ]
        
        # Review comments (positive and negative)
        self.review_comments = {
            5: ['Excellent product!', 'Love it!', 'Perfect quality', 'Highly recommend', 'Amazing value'],
            4: ['Good quality', 'Happy with purchase', 'Works well', 'Nice product', 'Satisfied'],
            3: ['Okay product', 'Average quality', 'It\'s fine', 'Decent', 'Could be better'],
            2: ['Not great', 'Poor quality', 'Disappointed', 'Issues with product', 'Below expectations'],
            1: ['Terrible', 'Waste of money', 'Broken on arrival', 'Very poor quality', 'Do not buy']
        }
        
        # Return reasons
        self.return_reasons = [
            'Defective product', 'Wrong size', 'Not as described', 'Changed mind',
            'Damaged in shipping', 'Poor quality', 'Wrong item received', 'No longer needed'
        ]
        
        # Seller names
        self.seller_names = [
            'TechWorld Store', 'Fashion Hub', 'Home Essentials', 'Beauty Palace', 'Sports Central',
            'Book Haven', 'Electronics Plus', 'Style Station', 'Garden Paradise', 'Fitness Pro',
            'Digital Dreams', 'Trendy Threads', 'Kitchen Masters', 'Beauty Boutique', 'Active Life'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate e-commerce dataset rows.
        
        Returns:
            List of dictionaries representing e-commerce transaction rows
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
        """Generate a single e-commerce transaction row."""
        
        # Generate transaction date (within last 2 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)
        transaction_date = self.faker_utils.date_between(start_date, end_date)
        
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
        discount_percentage = round(random.uniform(0, 50), 2)
        discount_amount = round((total_price * discount_percentage) / 100, 2)
        final_price = total_price - discount_amount
        
        # Generate shipping information
        shipping_mode = random.choice(list(self.shipping_modes.keys()))
        shipping_cost = self._generate_shipping_cost(shipping_mode, final_price)
        
        # Generate delivery date based on shipping mode
        min_days, max_days = self.shipping_modes[shipping_mode]
        delivery_date = transaction_date + timedelta(days=random.randint(min_days, max_days))
        
        # Generate geographic information
        country = random.choice(list(self.geographic_data.keys()))
        state_province = random.choice(list(self.geographic_data[country].keys()))
        city = random.choice(self.geographic_data[country][state_province])
        postal_code = self._generate_postal_code(country)
        
        # Generate order status
        order_status = random.choice(self.order_statuses)
        
        # Generate coupon code (30% chance)
        coupon_code = random.choice(self.coupon_codes) if random.random() < 0.3 else None
        
        # Generate review data (70% chance of having a review)
        review_rating = None
        review_comment = None
        if random.random() < 0.7:
            review_rating = random.randint(1, 5)
            review_comment = random.choice(self.review_comments[review_rating])
        
        # Generate return data (10% chance)
        return_requested = random.random() < 0.1
        return_reason = random.choice(self.return_reasons) if return_requested else None
        
        # Generate seller information
        seller_name = random.choice(self.seller_names)
        
        # Calculate profit (10-30% of final_price)
        profit = round(final_price * random.uniform(0.10, 0.30), 2)
        
        return {
            'transaction_id': self._generate_transaction_id(transaction_date),
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
            'discount_percentage': discount_percentage,
            'discount_amount': discount_amount,
            'final_price': round(final_price, 2),
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'payment_method': random.choice(self.payment_methods),
            'shipping_mode': shipping_mode,
            'shipping_cost': shipping_cost,
            'order_status': order_status,
            'delivery_date': delivery_date.strftime('%Y-%m-%d'),
            'country': country,
            'state_province': state_province,
            'city': city,
            'postal_code': postal_code,
            'customer_segment': random.choice(self.customer_segments),
            'coupon_code': coupon_code,
            'review_rating': review_rating,
            'review_comment': review_comment,
            'return_requested': return_requested,
            'return_reason': return_reason,
            'seller_id': self._generate_seller_id(),
            'seller_name': seller_name,
            'profit': profit
        }
    
    def _generate_transaction_id(self, transaction_date: datetime) -> str:
        """
        Generate transaction ID in format "TXN-YYYY-NNNNNN".
        
        Args:
            transaction_date: Date of the transaction
            
        Returns:
            Formatted transaction ID
        """
        year = transaction_date.year
        txn_num = str(self._transaction_counter).zfill(6)
        self._transaction_counter += 1
        return f"TXN-{year}-{txn_num}"
    
    def _generate_customer_id(self) -> str:
        """
        Generate customer ID in format "CUST-NNNNNN".
        
        Returns:
            Formatted customer ID
        """
        customer_num = str(self._customer_counter).zfill(6)
        self._customer_counter += 1
        return f"CUST-{customer_num:0>6}"
    
    def _generate_product_id(self) -> str:
        """
        Generate product ID in format "PROD-AAANNN".
        
        Returns:
            Formatted product ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"PROD-{letters}{numbers}"
    
    def _generate_seller_id(self) -> str:
        """
        Generate seller ID in format "SELL-NNNNN".
        
        Returns:
            Formatted seller ID
        """
        seller_num = str(random.randint(1, 99999)).zfill(5)
        return f"SELL-{seller_num}"
    
    def _generate_unit_price(self, category: str) -> float:
        """
        Generate realistic unit price based on category.
        
        Args:
            category: Product category
            
        Returns:
            Unit price as float
        """
        price_ranges = {
            'Electronics': (25, 3000),
            'Fashion': (10, 500),
            'Home & Garden': (15, 2000),
            'Beauty': (5, 300),
            'Sports': (20, 1000),
            'Books': (8, 75)
        }
        
        min_price, max_price = price_ranges.get(category, (10, 100))
        return random.uniform(min_price, max_price)
    
    def _generate_shipping_cost(self, shipping_mode: str, final_price: float) -> float:
        """
        Generate realistic shipping cost based on shipping mode and order value.
        
        Args:
            shipping_mode: Type of shipping
            final_price: Final price of the order
            
        Returns:
            Shipping cost as float
        """
        base_costs = {
            'Standard': 5.99,
            'Express': 12.99,
            'Overnight': 24.99
        }
        
        base_cost = base_costs.get(shipping_mode, 5.99)
        
        # Free shipping for orders over $50
        if final_price > 50:
            return 0.0
        
        # Add variation
        return round(base_cost + random.uniform(-2, 2), 2)
    
    def _generate_postal_code(self, country: str) -> str:
        """
        Generate realistic postal code based on country.
        
        Args:
            country: Country name
            
        Returns:
            Postal code as string
        """
        if country == 'United States':
            return f"{random.randint(10000, 99999)}"
        elif country == 'Canada':
            letter1 = random.choice(string.ascii_uppercase)
            digit1 = random.randint(0, 9)
            letter2 = random.choice(string.ascii_uppercase)
            digit2 = random.randint(0, 9)
            letter3 = random.choice(string.ascii_uppercase)
            digit3 = random.randint(0, 9)
            return f"{letter1}{digit1}{letter2} {digit2}{letter3}{digit3}"
        elif country == 'United Kingdom':
            return f"{random.choice(['SW', 'NW', 'SE', 'NE', 'W', 'E', 'N', 'S'])}{random.randint(1, 20)} {random.randint(1, 9)}{random.choice(string.ascii_uppercase)}{random.choice(string.ascii_uppercase)}"
        else:
            return f"{random.randint(10000, 99999)}"
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'transaction_id': 'string',
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
            'discount_percentage': 'float',
            'discount_amount': 'float',
            'final_price': 'float',
            'transaction_date': 'datetime',
            'payment_method': 'string',
            'shipping_mode': 'string',
            'shipping_cost': 'float',
            'order_status': 'string',
            'delivery_date': 'date',
            'country': 'string',
            'state_province': 'string',
            'city': 'string',
            'postal_code': 'string',
            'customer_segment': 'string',
            'coupon_code': 'string',
            'review_rating': 'integer',
            'review_comment': 'string',
            'return_requested': 'boolean',
            'return_reason': 'string',
            'seller_id': 'string',
            'seller_name': 'string',
            'profit': 'float'
        }