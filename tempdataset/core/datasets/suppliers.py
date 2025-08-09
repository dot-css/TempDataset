"""
Suppliers dataset generator.

Generates realistic suppliers data with 30 columns including supplier information,
contact details, performance metrics, and contract information.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class SuppliersDataset(BaseDataset):
    """
    Suppliers dataset generator that creates realistic supplier data.
    
    Generates 30 columns of supplier data including:
    - Supplier identification (supplier_id, name)
    - Contact information (name, title, email, phone, fax, website)
    - Address details (address, city, state, country, postal code)
    - Business classification (type, industry, product categories)
    - Performance metrics (rating, on-time delivery, lead time)
    - Contract information (dates, value, payment terms)
    - Order history and statistics
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the SuppliersDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._supplier_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Supplier types
        self.supplier_types = ['Manufacturer', 'Distributor', 'Wholesaler', 'Service Provider']
        
        # Industries and their corresponding product categories
        self.industries = {
            'Electronics': [
                'Laptops, Cables, Batteries',
                'Smartphones, Tablets, Accessories',
                'Audio Equipment, Headphones, Speakers',
                'Computer Components, Hardware, Software',
                'Gaming Consoles, Controllers, Games'
            ],
            'Apparel': [
                'Clothing, Shoes, Accessories',
                'Sportswear, Athletic Shoes, Equipment',
                'Formal Wear, Business Attire, Suits',
                'Casual Wear, Denim, T-shirts',
                'Outerwear, Jackets, Coats'
            ],
            'Food & Beverage': [
                'Fresh Produce, Fruits, Vegetables',
                'Packaged Foods, Snacks, Beverages',
                'Dairy Products, Meat, Seafood',
                'Baked Goods, Desserts, Confectionery',
                'Organic Foods, Health Products, Supplements'
            ],
            'Automotive': [
                'Car Parts, Engine Components, Brakes',
                'Tires, Wheels, Automotive Fluids',
                'Electronics, GPS, Audio Systems',
                'Tools, Equipment, Maintenance Supplies',
                'Motorcycles, ATVs, Marine Vehicles'
            ],
            'Healthcare': [
                'Medical Equipment, Devices, Supplies',
                'Pharmaceuticals, Medications, Vaccines',
                'Laboratory Equipment, Testing Supplies',
                'Personal Protective Equipment, Safety Gear',
                'Wellness Products, Vitamins, Supplements'
            ],
            'Home & Garden': [
                'Furniture, Home Decor, Lighting',
                'Kitchen Appliances, Cookware, Utensils',
                'Garden Tools, Plants, Landscaping',
                'Cleaning Supplies, Household Items',
                'Bedding, Linens, Bathroom Accessories'
            ],
            'Construction': [
                'Building Materials, Lumber, Steel',
                'Tools, Hardware, Fasteners',
                'Electrical Supplies, Wiring, Fixtures',
                'Plumbing Supplies, Pipes, Fittings',
                'Safety Equipment, Protective Gear'
            ],
            'Industrial': [
                'Manufacturing Equipment, Machinery',
                'Raw Materials, Chemicals, Metals',
                'Safety Equipment, Industrial Supplies',
                'Packaging Materials, Containers, Labels',
                'Quality Control, Testing Equipment'
            ],
            'Office Supplies': [
                'Stationery, Paper, Writing Instruments',
                'Office Furniture, Desks, Chairs',
                'Technology, Computers, Printers',
                'Cleaning Supplies, Maintenance Items',
                'Break Room Supplies, Coffee, Snacks'
            ],
            'Beauty & Personal Care': [
                'Cosmetics, Skincare, Fragrances',
                'Hair Care Products, Styling Tools',
                'Personal Hygiene, Oral Care, Bath Products',
                'Wellness Products, Spa Supplies',
                'Professional Beauty Equipment, Salon Supplies'
            ]
        }
        
        # Contact titles
        self.contact_titles = [
            'Sales Manager', 'Account Manager', 'Business Development Manager',
            'Regional Sales Director', 'Key Account Executive', 'Sales Representative',
            'Customer Success Manager', 'Partner Manager', 'Territory Manager',
            'VP of Sales', 'Sales Coordinator', 'Client Relations Manager'
        ]
        
        # Payment terms
        self.payment_terms = ['Net 30', 'Net 45', 'Net 60', 'Prepaid']
        
        # Primary contact methods
        self.primary_contact_methods = ['Email', 'Phone', 'Fax', 'In-person']
        
        # Sample notes
        self.notes_templates = [
            'Excellent service quality and reliability',
            'Long-standing partner with competitive pricing',
            'Specializes in custom solutions and quick turnaround',
            'Strong technical support and customer service',
            'Preferred for urgent orders and emergency supplies',
            'Offers volume discounts and flexible payment terms',
            'Certified supplier with quality assurance program',
            'Regional supplier with local market expertise',
            'New supplier under evaluation period',
            'Backup supplier for critical components'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate suppliers dataset rows.
        
        Returns:
            List of dictionaries representing supplier rows
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
        """Generate a single supplier row."""
        
        # Generate supplier basic info
        supplier_name = self.faker_utils.company()
        contact_name = self.faker_utils.name()
        contact_title = random.choice(self.contact_titles)
        
        # Generate contact information
        email = self.faker_utils.email(contact_name)
        phone_number = self.faker_utils.phone_number()
        fax_number = self.faker_utils.phone_number() if random.random() > 0.3 else None
        website = f"www.{supplier_name.lower().replace(' ', '').replace(',', '').replace('.', '')}.com" if random.random() > 0.2 else None
        
        # Generate address
        address = self.faker_utils.address()
        city = self.faker_utils.city()
        state = self.faker_utils.state()
        country = self.faker_utils.country()
        postal_code = self.faker_utils.postal_code()
        
        # Generate business classification
        supplier_type = random.choice(self.supplier_types)
        industry = random.choice(list(self.industries.keys()))
        product_categories = random.choice(self.industries[industry])
        
        # Generate performance metrics
        rating = random.randint(1, 5)
        on_time_delivery_rate = round(random.uniform(70.0, 100.0), 1)
        average_lead_time_days = random.randint(1, 30)
        
        # Generate contract information
        contract_start_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1825),  # Up to 5 years ago
            datetime.now() - timedelta(days=30)     # At least 30 days ago
        )
        
        # Contract end date (70% have ongoing contracts)
        contract_end_date = None
        if random.random() > 0.7:
            contract_end_date = contract_start_date + timedelta(
                days=random.randint(365, 1095)  # 1-3 years from start
            )
            # Ensure end date is not in the past for active contracts
            if contract_end_date < datetime.now().date():
                contract_end_date = datetime.now().date() + timedelta(days=random.randint(30, 730))
        
        # Generate financial information
        annual_contract_value_usd = round(random.uniform(10000, 5000000), 2)
        payment_terms = random.choice(self.payment_terms)
        
        # Preferred supplier logic (high rating and delivery rate)
        preferred_supplier = (rating >= 4 and on_time_delivery_rate >= 90.0) or random.random() > 0.8
        
        # Generate order history
        total_orders = random.randint(5, 500)
        average_order_value = annual_contract_value_usd / max(total_orders * random.uniform(0.8, 1.2), 1)
        total_order_value_usd = round(total_orders * average_order_value, 2)
        
        # Last order date
        last_order_date = self.faker_utils.date_between(
            contract_start_date,
            min(datetime.now().date(), contract_end_date) if contract_end_date else datetime.now().date()
        )
        
        # Return rate (preferred suppliers have lower return rates)
        if preferred_supplier:
            return_rate_percentage = round(random.uniform(0.0, 5.0), 1)
        else:
            return_rate_percentage = round(random.uniform(0.0, 15.0), 1)
        
        # Primary contact method
        primary_contact_method = random.choice(self.primary_contact_methods)
        
        # Notes (40% have notes)
        notes = random.choice(self.notes_templates) if random.random() > 0.6 else None
        
        return {
            'supplier_id': self._generate_supplier_id(),
            'supplier_name': supplier_name,
            'contact_name': contact_name,
            'contact_title': contact_title,
            'email': email,
            'phone_number': phone_number,
            'fax_number': fax_number,
            'website': website,
            'address': address,
            'city': city,
            'state_province': state,
            'country': country,
            'postal_code': postal_code,
            'supplier_type': supplier_type,
            'industry': industry,
            'product_categories': product_categories,
            'rating': rating,
            'on_time_delivery_rate': on_time_delivery_rate,
            'average_lead_time_days': average_lead_time_days,
            'contract_start_date': contract_start_date.strftime('%Y-%m-%d'),
            'contract_end_date': contract_end_date.strftime('%Y-%m-%d') if contract_end_date else None,
            'annual_contract_value_usd': annual_contract_value_usd,
            'payment_terms': payment_terms,
            'preferred_supplier': preferred_supplier,
            'return_rate_percentage': return_rate_percentage,
            'last_order_date': last_order_date.strftime('%Y-%m-%d'),
            'total_orders': total_orders,
            'total_order_value_usd': total_order_value_usd,
            'primary_contact_method': primary_contact_method,
            'notes': notes
        }
    
    def _generate_supplier_id(self) -> str:
        """
        Generate supplier ID in format "SUP-NNNNNN".
        
        Returns:
            Formatted supplier ID
        """
        supplier_num = str(self._supplier_counter).zfill(6)
        self._supplier_counter += 1
        return f"SUP-{supplier_num}"
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'supplier_id': 'string',
            'supplier_name': 'string',
            'contact_name': 'string',
            'contact_title': 'string',
            'email': 'string',
            'phone_number': 'string',
            'fax_number': 'string',
            'website': 'string',
            'address': 'string',
            'city': 'string',
            'state_province': 'string',
            'country': 'string',
            'postal_code': 'string',
            'supplier_type': 'string',
            'industry': 'string',
            'product_categories': 'string',
            'rating': 'integer',
            'on_time_delivery_rate': 'float',
            'average_lead_time_days': 'integer',
            'contract_start_date': 'date',
            'contract_end_date': 'date',
            'annual_contract_value_usd': 'float',
            'payment_terms': 'string',
            'preferred_supplier': 'boolean',
            'return_rate_percentage': 'float',
            'last_order_date': 'date',
            'total_orders': 'integer',
            'total_order_value_usd': 'float',
            'primary_contact_method': 'string',
            'notes': 'string'
        }
