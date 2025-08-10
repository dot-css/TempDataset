"""
Inventory dataset generator.

Generates realistic inventory and warehouse stock level data with 25+ columns including
stock quantities, SKU details, storage locations, reorder thresholds, and supplier links.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class InventoryDataset(BaseDataset):
    """
    Inventory dataset generator that creates realistic warehouse and stock data.
    
    Generates 25+ columns of inventory data including:
    - Product information (SKU, name, category, supplier)
    - Stock levels (on hand, reserved, reorder thresholds)
    - Pricing and valuation (unit price, total value)
    - Warehouse location (warehouse, aisle, shelf, bin)
    - Restock scheduling and lead times
    - Special handling requirements
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the InventoryDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential SKUs
        self._sku_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Product categories and subcategories
        self.categories = {
            'Electronics': ['Smartphones', 'Laptops', 'Tablets', 'Accessories', 'Components'],
            'Clothing': ['Shirts', 'Pants', 'Dresses', 'Shoes', 'Accessories'],
            'Home & Garden': ['Furniture', 'Kitchen', 'Bedding', 'Decor', 'Tools'],
            'Sports': ['Fitness', 'Outdoor', 'Team Sports', 'Water Sports', 'Equipment'],
            'Books': ['Fiction', 'Non-Fiction', 'Educational', 'Children', 'Reference'],
            'Health & Beauty': ['Skincare', 'Makeup', 'Hair Care', 'Supplements', 'Personal Care'],
            'Automotive': ['Parts', 'Accessories', 'Tools', 'Fluids', 'Electronics'],
            'Office Supplies': ['Paper', 'Writing', 'Storage', 'Technology', 'Furniture']
        }
        
        # Product names by category
        self.product_names = {
            'Electronics': {
                'Smartphones': ['iPhone Pro Max', 'Galaxy S Ultra', 'Pixel Pro', 'OnePlus Pro'],
                'Laptops': ['MacBook Pro', 'ThinkPad X1', 'Surface Laptop', 'Gaming Laptop Pro'],
                'Tablets': ['iPad Pro', 'Galaxy Tab S', 'Surface Pro', 'Fire HD Tablet'],
                'Accessories': ['Wireless Charger', 'Phone Case', 'Screen Protector', 'Cable'],
                'Components': ['RAM Module', 'SSD Drive', 'Graphics Card', 'Motherboard']
            },
            'Clothing': {
                'Shirts': ['Cotton T-Shirt', 'Dress Shirt', 'Polo Shirt', 'Hoodie'],
                'Pants': ['Jeans', 'Chinos', 'Dress Pants', 'Joggers'],
                'Dresses': ['Summer Dress', 'Evening Dress', 'Casual Dress', 'Maxi Dress'],
                'Shoes': ['Running Shoes', 'Dress Shoes', 'Sneakers', 'Boots'],
                'Accessories': ['Watch', 'Belt', 'Wallet', 'Sunglasses']
            },
            'Home & Garden': {
                'Furniture': ['Sofa', 'Dining Table', 'Bed Frame', 'Office Chair'],
                'Kitchen': ['Coffee Maker', 'Blender', 'Cookware Set', 'Dinnerware'],
                'Bedding': ['Sheet Set', 'Comforter', 'Pillow', 'Mattress Topper'],
                'Decor': ['Wall Art', 'Table Lamp', 'Vase', 'Mirror'],
                'Tools': ['Power Drill', 'Hammer', 'Screwdriver Set', 'Tool Box']
            },
            'Sports': {
                'Fitness': ['Treadmill', 'Dumbbells', 'Yoga Mat', 'Resistance Bands'],
                'Outdoor': ['Camping Tent', 'Sleeping Bag', 'Hiking Boots', 'Backpack'],
                'Team Sports': ['Basketball', 'Soccer Ball', 'Baseball Glove', 'Football'],
                'Water Sports': ['Swimsuit', 'Goggles', 'Life Jacket', 'Surfboard'],
                'Equipment': ['Exercise Bike', 'Weight Bench', 'Pull-up Bar', 'Kettlebell']
            },
            'Books': {
                'Fiction': ['Mystery Novel', 'Romance Novel', 'Sci-Fi Book', 'Fantasy Series'],
                'Non-Fiction': ['Biography', 'Self-Help Book', 'History Book', 'Travel Guide'],
                'Educational': ['Textbook', 'Study Guide', 'Workbook', 'Reference Manual'],
                'Children': ['Picture Book', 'Chapter Book', 'Activity Book', 'Board Book'],
                'Reference': ['Dictionary', 'Encyclopedia', 'Atlas', 'Cookbook']
            },
            'Health & Beauty': {
                'Skincare': ['Moisturizer', 'Cleanser', 'Serum', 'Sunscreen'],
                'Makeup': ['Foundation', 'Lipstick', 'Mascara', 'Eyeshadow'],
                'Hair Care': ['Shampoo', 'Conditioner', 'Hair Styling Gel', 'Hair Treatment'],
                'Supplements': ['Multivitamin', 'Protein Powder', 'Omega-3', 'Probiotics'],
                'Personal Care': ['Toothpaste', 'Deodorant', 'Body Wash', 'Lotion']
            },
            'Automotive': {
                'Parts': ['Brake Pads', 'Air Filter', 'Spark Plugs', 'Oil Filter'],
                'Accessories': ['Floor Mats', 'Seat Covers', 'Phone Mount', 'Dash Cam'],
                'Tools': ['Socket Set', 'Wrench Set', 'Jack', 'Tire Gauge'],
                'Fluids': ['Motor Oil', 'Brake Fluid', 'Coolant', 'Transmission Fluid'],
                'Electronics': ['Car Stereo', 'GPS Navigator', 'Backup Camera', 'Alarm System']
            },
            'Office Supplies': {
                'Paper': ['Copy Paper', 'Notebook', 'Sticky Notes', 'Envelopes'],
                'Writing': ['Pen Set', 'Pencils', 'Markers', 'Highlighters'],
                'Storage': ['File Cabinet', 'Storage Box', 'Binders', 'Folders'],
                'Technology': ['Printer', 'Scanner', 'Shredder', 'Calculator'],
                'Furniture': ['Desk', 'Office Chair', 'Bookshelf', 'Filing Cabinet']
            }
        }
        
        # Supplier names
        self.supplier_names = [
            'Global Supply Co', 'Premier Distributors', 'Elite Wholesale', 'United Suppliers',
            'Advanced Logistics', 'Prime Vendors', 'International Trading', 'Smart Supply Chain',
            'Reliable Partners', 'Quality Distributors', 'Express Wholesale', 'Direct Supply',
            'Professional Vendors', 'Efficient Logistics', 'Trusted Suppliers'
        ]
        
        # Warehouse locations
        self.warehouse_locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX', 'Phoenix, AZ',
            'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA', 'Dallas, TX', 'San Jose, CA',
            'Austin, TX', 'Jacksonville, FL', 'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC'
        ]
        
        # Stock statuses
        self.stock_statuses = ['In Stock', 'Low Stock', 'Out of Stock']
        
        # Units of measure
        self.units_of_measure = ['Each', 'Box', 'Case', 'Pallet', 'Dozen', 'Pair', 'Set', 'Pack']
        
        # Sample notes
        self.notes_templates = [
            'High-demand item, monitor closely',
            'Seasonal product, adjust for trends',
            'Fragile - handle with care',
            'Fast-moving inventory',
            'Bulk discount available',
            'Special storage requirements',
            'Popular during holidays',
            'Requires temperature control',
            'Limited shelf life',
            'Customer favorite'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate inventory dataset rows.
        
        Returns:
            List of dictionaries representing inventory item rows
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
        """Generate a single inventory item row."""
        
        # Generate product information
        category = random.choice(list(self.categories.keys()))
        subcategory = random.choice(self.categories[category])
        product_name = random.choice(self.product_names[category][subcategory])
        
        # Generate supplier information
        supplier_name = random.choice(self.supplier_names)
        supplier_id = self._generate_supplier_id(supplier_name)
        
        # Generate stock quantities
        quantity_on_hand = random.randint(0, 1000)
        quantity_reserved = random.randint(0, min(quantity_on_hand, 100))
        reorder_level = random.randint(10, 100)
        reorder_quantity = random.randint(50, 500)
        
        # Generate pricing
        unit_price = self._generate_unit_price(category)
        total_value = quantity_on_hand * unit_price
        
        # Generate warehouse location
        warehouse_id = self._generate_warehouse_id()
        warehouse_location = random.choice(self.warehouse_locations)
        aisle = f"A{random.randint(1, 20)}"
        shelf = f"S{random.randint(1, 10)}"
        bin_location = f"B{random.randint(1, 50)}"
        
        # Generate dates
        last_restock_date = self._generate_last_restock_date()
        next_restock_date = self._generate_next_restock_date(last_restock_date)
        
        # Generate stock status
        stock_status = self._determine_stock_status(quantity_on_hand, reorder_level)
        
        # Generate lead time and other attributes
        lead_time_days = random.randint(1, 30)
        unit_of_measure = random.choice(self.units_of_measure)
        hazardous_material = random.choice([True, False]) if category in ['Automotive', 'Health & Beauty'] else False
        
        # Generate expiration date (only for certain categories)
        expiration_date = self._generate_expiration_date(category) if category in ['Health & Beauty', 'Books'] else None
        
        # Generate notes
        notes = random.choice(self.notes_templates)
        
        return {
            'sku': self._generate_sku(),
            'product_name': product_name,
            'category': category,
            'subcategory': subcategory,
            'supplier_id': supplier_id,
            'supplier_name': supplier_name,
            'quantity_on_hand': quantity_on_hand,
            'quantity_reserved': quantity_reserved,
            'reorder_level': reorder_level,
            'reorder_quantity': reorder_quantity,
            'unit_price': round(unit_price, 2),
            'total_value': round(total_value, 2),
            'warehouse_id': warehouse_id,
            'warehouse_location': warehouse_location,
            'aisle': aisle,
            'shelf': shelf,
            'bin': bin_location,
            'last_restock_date': last_restock_date.strftime('%Y-%m-%d'),
            'next_restock_date': next_restock_date.strftime('%Y-%m-%d'),
            'stock_status': stock_status,
            'lead_time_days': lead_time_days,
            'unit_of_measure': unit_of_measure,
            'hazardous_material': hazardous_material,
            'expiration_date': expiration_date.strftime('%Y-%m-%d') if expiration_date else None,
            'notes': notes
        }
    
    def _generate_sku(self) -> str:
        """
        Generate SKU in format "SKU-NNNNN".
        
        Returns:
            Formatted SKU
        """
        sku_num = str(self._sku_counter).zfill(5)
        self._sku_counter += 1
        return f"SKU-{sku_num}"
    
    def _generate_supplier_id(self, supplier_name: str) -> str:
        """
        Generate supplier ID based on supplier name.
        
        Args:
            supplier_name: Name of the supplier
            
        Returns:
            Formatted supplier ID
        """
        # Create ID from first letters of supplier name
        words = supplier_name.split()
        prefix = ''.join(word[0].upper() for word in words[:3])
        number = random.randint(100, 999)
        return f"SUP-{prefix}{number}"
    
    def _generate_warehouse_id(self) -> str:
        """
        Generate warehouse ID in format "WH-NNN".
        
        Returns:
            Formatted warehouse ID
        """
        warehouse_num = random.randint(100, 999)
        return f"WH-{warehouse_num}"
    
    def _generate_unit_price(self, category: str) -> float:
        """
        Generate realistic unit price based on category.
        
        Args:
            category: Product category
            
        Returns:
            Unit price as float
        """
        price_ranges = {
            'Electronics': (25, 1500),
            'Clothing': (10, 200),
            'Home & Garden': (15, 800),
            'Sports': (20, 500),
            'Books': (5, 40),
            'Health & Beauty': (3, 100),
            'Automotive': (10, 300),
            'Office Supplies': (2, 150)
        }
        
        min_price, max_price = price_ranges.get(category, (5, 100))
        return random.uniform(min_price, max_price)
    
    def _generate_last_restock_date(self) -> datetime:
        """
        Generate last restock date (within last 6 months).
        
        Returns:
            Last restock datetime
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=180)  # 6 months
        return self.faker_utils.date_between(start_date, end_date)
    
    def _generate_next_restock_date(self, last_restock_date: datetime) -> datetime:
        """
        Generate next restock date (1-60 days from last restock).
        
        Args:
            last_restock_date: Date of last restock
            
        Returns:
            Next restock datetime
        """
        days_ahead = random.randint(1, 60)
        return last_restock_date + timedelta(days=days_ahead)
    
    def _determine_stock_status(self, quantity_on_hand: int, reorder_level: int) -> str:
        """
        Determine stock status based on quantity and reorder level.
        
        Args:
            quantity_on_hand: Current stock quantity
            reorder_level: Reorder threshold
            
        Returns:
            Stock status string
        """
        if quantity_on_hand == 0:
            return 'Out of Stock'
        elif quantity_on_hand <= reorder_level:
            return 'Low Stock'
        else:
            return 'In Stock'
    
    def _generate_expiration_date(self, category: str) -> Optional[datetime]:
        """
        Generate expiration date for applicable categories.
        
        Args:
            category: Product category
            
        Returns:
            Expiration datetime or None
        """
        if category == 'Health & Beauty':
            # 6 months to 3 years from now
            days_ahead = random.randint(180, 1095)
        elif category == 'Books':
            # Books don't really expire, but for demo purposes
            days_ahead = random.randint(1825, 3650)  # 5-10 years
        else:
            return None
        
        return datetime.now() + timedelta(days=days_ahead)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'sku': 'string',
            'product_name': 'string',
            'category': 'string',
            'subcategory': 'string',
            'supplier_id': 'string',
            'supplier_name': 'string',
            'quantity_on_hand': 'integer',
            'quantity_reserved': 'integer',
            'reorder_level': 'integer',
            'reorder_quantity': 'integer',
            'unit_price': 'float',
            'total_value': 'float',
            'warehouse_id': 'string',
            'warehouse_location': 'string',
            'aisle': 'string',
            'shelf': 'string',
            'bin': 'string',
            'last_restock_date': 'date',
            'next_restock_date': 'date',
            'stock_status': 'string',
            'lead_time_days': 'integer',
            'unit_of_measure': 'string',
            'hazardous_material': 'boolean',
            'expiration_date': 'date',
            'notes': 'string'
        }