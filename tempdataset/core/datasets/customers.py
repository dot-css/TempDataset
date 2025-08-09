"""
Customers dataset generator.

Generates realistic customer data with comprehensive customer information,
demographics, purchasing history, and loyalty data.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class CustomersDataset(BaseDataset):
    """
    Customers dataset generator that creates realistic customer profile data.
    
    Generates comprehensive customer data including:
    - Personal information (names, contact details, demographics)
    - Geographic data (addresses, regions)
    - Financial data (income, spending patterns)
    - Account information (registration, status, preferences)
    - Loyalty and engagement metrics
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the CustomersDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential customer IDs
        self._customer_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Gender options
        self.genders = ['Male', 'Female', 'Other']
        
        # Marital status options
        self.marital_statuses = ['Single', 'Married', 'Divorced', 'Widowed']
        
        # Occupation categories with realistic job titles
        self.occupations = [
            'Software Engineer', 'Data Analyst', 'Marketing Manager', 'Sales Representative',
            'Teacher', 'Nurse', 'Doctor', 'Lawyer', 'Accountant', 'Consultant',
            'Project Manager', 'Business Analyst', 'HR Manager', 'Operations Manager',
            'Customer Service Representative', 'Graphic Designer', 'Writer', 'Editor',
            'Financial Advisor', 'Real Estate Agent', 'Chef', 'Mechanic', 'Electrician',
            'Plumber', 'Carpenter', 'Police Officer', 'Firefighter', 'Paramedic',
            'Pharmacist', 'Dentist', 'Veterinarian', 'Architect', 'Civil Engineer',
            'Mechanical Engineer', 'Electrical Engineer', 'Research Scientist',
            'Product Manager', 'UX Designer', 'Web Developer', 'Database Administrator',
            'System Administrator', 'Network Engineer', 'Cybersecurity Specialist',
            'Social Worker', 'Therapist', 'Physical Therapist', 'Pilot', 'Flight Attendant',
            'Retail Manager', 'Store Clerk', 'Warehouse Worker', 'Truck Driver',
            'Construction Worker', 'Landscaper', 'Photographer', 'Musician', 'Artist'
        ]
        
        # Company names by industry
        self.companies = [
            # Technology
            'TechCorp Solutions', 'Digital Dynamics', 'InnovateTech', 'DataSync Systems',
            'CloudFirst Technologies', 'SmartCode Inc', 'NextGen Software', 'ByteForce',
            'CyberShield Security', 'AI Innovations',
            
            # Healthcare
            'HealthFirst Medical', 'WellCare Systems', 'MediTech Solutions', 'CarePoint Health',
            'Wellness Partners', 'Advanced Medical', 'LifeCare Group', 'Premier Health',
            'MedAssist Technologies', 'HealthTech Innovations',
            
            # Financial Services
            'Capital Partners', 'Financial Solutions Group', 'Investment Advisors',
            'Wealth Management Corp', 'Banking Solutions', 'Credit Union Services',
            'Insurance Partners', 'Asset Management', 'Financial Planning Inc',
            'Investment Services',
            
            # Manufacturing
            'Manufacturing Solutions', 'Industrial Systems', 'Production Partners',
            'Quality Manufacturing', 'Precision Industries', 'Advanced Manufacturing',
            'Supply Chain Solutions', 'Production Technologies', 'Manufacturing Corp',
            'Industrial Partners',
            
            # Retail
            'Retail Solutions', 'Customer First', 'Shopping Centers', 'Retail Partners',
            'Consumer Goods', 'Merchandise Corp', 'Retail Technologies', 'Store Solutions',
            'Commerce Partners', 'Retail Innovations',
            
            # Education
            'Education Partners', 'Learning Solutions', 'Academic Services', 'School Systems',
            'Educational Technologies', 'Training Solutions', 'Learning Corp',
            'Education Innovations', 'Academic Partners', 'Knowledge Systems',
            
            # Government/Non-profit
            'Public Services', 'Government Solutions', 'Community Partners', 'Social Services',
            'Non-profit Organizations', 'Public Sector', 'Community Services',
            'Government Technologies', 'Public Partners', 'Civic Solutions'
        ]
        
        # Geographic regions
        self.regions = ['North', 'South', 'East', 'West', 'Central']
        
        # Customer segments
        self.customer_segments = ['Consumer', 'Corporate', 'Home Office']
        
        # Payment methods
        self.payment_methods = ['Credit Card', 'Debit Card', 'PayPal', 'Bank Transfer']
        
        # Shipping modes
        self.shipping_modes = ['Standard', 'Express', 'Overnight']
        
        # Account statuses
        self.account_statuses = ['Active', 'Inactive', 'Suspended']
        
        # Notes/remarks (some customers will have null notes)
        self.customer_notes = [
            'VIP customer', 'Late payments', 'Excellent payment history', 'Bulk order customer',
            'Frequent buyer', 'Corporate account', 'Seasonal customer', 'High-value customer',
            'Referral source', 'Long-term customer', 'Price-sensitive customer',
            'Quality-focused customer', 'Early adopter', 'Brand advocate', 'Volume buyer'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate customers dataset rows.
        
        Returns:
            List of dictionaries representing customer profile rows
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
        """Generate a single customer profile row."""
        
        # Generate personal information
        first_name = self.faker_utils.first_name()
        last_name = self.faker_utils.last_name()
        full_name = f"{first_name} {last_name}"
        email = self._generate_email(first_name, last_name)
        phone_number = self._generate_international_phone()
        gender = random.choice(self.genders)
        
        # Generate age and birth date with consistent relationship
        age = random.randint(18, 80)
        today = datetime.now()
        birth_year = today.year - age
        # Random month and day for birth date
        date_of_birth = datetime(
            birth_year,
            random.randint(1, 12),
            random.randint(1, 28)  # Use 28 to avoid month-end issues
        )
        
        # Generate demographic information
        marital_status = random.choice(self.marital_statuses)
        occupation = random.choice(self.occupations)
        company = random.choice(self.companies)
        
        # Generate income with realistic distribution (skewed towards middle class)
        annual_income = self._generate_realistic_income()
        
        # Generate address information
        street_address = self.faker_utils.address().split('\n')[0]  # First line only
        city = self.faker_utils.city()
        state_province = self.faker_utils.state()
        postal_code = self.faker_utils.postal_code()
        country = self.faker_utils.country()
        region = random.choice(self.regions)
        
        # Generate account dates with proper relationships
        # Account created sometime in the last 5 years
        account_created_date = self.faker_utils.date_between(
            today - timedelta(days=5*365),
            today
        )
        
        # Generate order history
        total_orders = random.randint(0, 50)  # Some customers may have 0 orders
        
        if total_orders > 0:
            # Last purchase should be after account creation
            last_purchase_date = self.faker_utils.date_between(
                account_created_date,
                today
            )
            
            # Generate spending with correlation to income and orders
            base_spending = annual_income * random.uniform(0.05, 0.20)  # 5-20% of income
            # Add some randomness and correlation with number of orders
            total_spent = base_spending * (1 + (total_orders - 25) * 0.02)
            total_spent = max(100, total_spent)  # Minimum spending
            total_spent = round(total_spent, 2)
            
            average_order_value = round(total_spent / total_orders, 2)
        else:
            # New customer with no purchases yet
            last_purchase_date = None
            total_spent = 0.0
            average_order_value = 0.0
        
        # Generate loyalty information
        # Higher chance of loyalty membership for customers with more orders
        loyalty_probability = min(0.8, 0.2 + (total_orders * 0.02))
        loyalty_member = random.random() < loyalty_probability
        
        if loyalty_member:
            # Loyalty points correlate with spending
            max_points = min(10000, int(total_spent * 0.1))
            loyalty_points = random.randint(0, max_points)
        else:
            loyalty_points = 0
        
        # Generate preferences
        preferred_payment_method = random.choice(self.payment_methods)
        preferred_shipping_mode = random.choice(self.shipping_modes)
        
        # Newsletter subscription (higher probability for loyalty members)
        newsletter_probability = 0.7 if loyalty_member else 0.4
        newsletter_subscribed = random.random() < newsletter_probability
        
        # Customer segment (correlate with income and spending)
        if annual_income > 150000 or total_spent > 10000:
            customer_segment = random.choice(['Corporate', 'Home Office'])
        else:
            customer_segment = 'Consumer'
        
        # Account status (mostly active)
        account_status_weights = [0.85, 0.10, 0.05]  # Active, Inactive, Suspended
        account_status = random.choices(self.account_statuses, weights=account_status_weights)[0]
        
        # Notes (30% chance of having notes)
        notes = random.choice(self.customer_notes) if random.random() < 0.3 else None
        
        return {
            'customer_id': self._generate_customer_id(),
            'first_name': first_name,
            'last_name': last_name,
            'full_name': full_name,
            'email': email,
            'phone_number': phone_number,
            'gender': gender,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
            'age': age,
            'marital_status': marital_status,
            'occupation': occupation,
            'company': company,
            'annual_income': annual_income,
            'street_address': street_address,
            'city': city,
            'state_province': state_province,
            'postal_code': postal_code,
            'country': country,
            'region': region,
            'account_created_date': account_created_date.strftime('%Y-%m-%d %H:%M:%S'),
            'last_purchase_date': last_purchase_date.strftime('%Y-%m-%d %H:%M:%S') if last_purchase_date else None,
            'total_orders': total_orders,
            'total_spent': total_spent,
            'average_order_value': average_order_value,
            'loyalty_member': loyalty_member,
            'loyalty_points': loyalty_points,
            'preferred_payment_method': preferred_payment_method,
            'preferred_shipping_mode': preferred_shipping_mode,
            'newsletter_subscribed': newsletter_subscribed,
            'customer_segment': customer_segment,
            'account_status': account_status,
            'notes': notes
        }
    
    def _generate_customer_id(self) -> str:
        """
        Generate customer ID in format "CUST-NNNNNN".
        
        Returns:
            Formatted customer ID
        """
        customer_num = str(self._customer_counter).zfill(6)
        self._customer_counter += 1
        return f"CUST-{customer_num}"
    
    def _generate_email(self, first_name: str, last_name: str) -> str:
        """
        Generate realistic email address based on name.
        
        Args:
            first_name: Customer's first name
            last_name: Customer's last name
            
        Returns:
            Email address
        """
        # Create variations of name-based emails
        patterns = [
            f"{first_name.lower()}.{last_name.lower()}",
            f"{first_name.lower()}{last_name.lower()}",
            f"{first_name[0].lower()}{last_name.lower()}",
            f"{first_name.lower()}{last_name[0].lower()}",
            f"{first_name.lower()}.{last_name.lower()}{random.randint(1, 99)}"
        ]
        
        base_email = random.choice(patterns)
        # Clean up the email (remove special characters)
        base_email = ''.join(c for c in base_email if c.isalnum() or c == '.')
        
        domains = [
            'gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'aol.com',
            'icloud.com', 'protonmail.com', 'mail.com', 'zoho.com', 'fastmail.com'
        ]
        
        domain = random.choice(domains)
        return f"{base_email}@{domain}"
    
    def _generate_international_phone(self) -> str:
        """
        Generate phone number in international format.
        
        Returns:
            International phone number
        """
        # Common country codes and formats
        formats = [
            f"+1-{random.randint(200, 999)}-{random.randint(200, 999)}-{random.randint(1000, 9999)}",  # US/Canada
            f"+44-{random.randint(20, 79)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",  # UK
            f"+49-{random.randint(30, 89)}-{random.randint(10000, 99999)}",  # Germany
            f"+33-{random.randint(1, 9)}-{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}-{random.randint(10, 99)}",  # France
            f"+61-{random.randint(2, 8)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",  # Australia
            f"+81-{random.randint(3, 9)}-{random.randint(1000, 9999)}-{random.randint(1000, 9999)}",  # Japan
        ]
        
        return random.choice(formats)
    
    def _generate_realistic_income(self) -> float:
        """
        Generate realistic annual income with proper distribution.
        
        Returns:
            Annual income in USD
        """
        # Create a more realistic income distribution (not uniform)
        # Most people earn in middle ranges, fewer at extremes
        
        # Use different probability ranges
        income_ranges = [
            (10000, 30000, 0.15),   # Low income: 15%
            (30000, 50000, 0.25),   # Lower-middle: 25%
            (50000, 75000, 0.30),   # Middle: 30%
            (75000, 100000, 0.15),  # Upper-middle: 15%
            (100000, 150000, 0.10), # High: 10%
            (150000, 250000, 0.05)  # Very high: 5%
        ]
        
        # Select range based on weights
        ranges_list = [(min_inc, max_inc) for min_inc, max_inc, _ in income_ranges]
        weights = [weight for _, _, weight in income_ranges]
        
        selected_range = random.choices(ranges_list, weights=weights)[0]
        min_income, max_income = selected_range
        
        # Generate income within the selected range
        income = random.uniform(min_income, max_income)
        
        # Round to nearest 1000 for realism
        income = round(income / 1000) * 1000
        
        return float(income)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'customer_id': 'string',
            'first_name': 'string',
            'last_name': 'string',
            'full_name': 'string',
            'email': 'string',
            'phone_number': 'string',
            'gender': 'string',
            'date_of_birth': 'date',
            'age': 'integer',
            'marital_status': 'string',
            'occupation': 'string',
            'company': 'string',
            'annual_income': 'float',
            'street_address': 'string',
            'city': 'string',
            'state_province': 'string',
            'postal_code': 'string',
            'country': 'string',
            'region': 'string',
            'account_created_date': 'datetime',
            'last_purchase_date': 'datetime',
            'total_orders': 'integer',
            'total_spent': 'float',
            'average_order_value': 'float',
            'loyalty_member': 'boolean',
            'loyalty_points': 'integer',
            'preferred_payment_method': 'string',
            'preferred_shipping_mode': 'string',
            'newsletter_subscribed': 'boolean',
            'customer_segment': 'string',
            'account_status': 'string',
            'notes': 'string'
        }
