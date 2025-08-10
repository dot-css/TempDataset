"""
CRM dataset generator.

Generates realistic customer relationship management data with 30+ columns including
customer interactions, sales pipeline, account history, support cases, and loyalty data.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class CrmDataset(BaseDataset):
    """
    CRM dataset generator that creates realistic customer relationship management data.
    
    Generates 30+ columns of CRM data including:
    - Customer information (customer_id, name, email, company, demographics)
    - Account management (account_manager, creation_date, status)
    - Interactions (channel, notes, contact dates)
    - Sales pipeline (stage, deal value, probability)
    - Support data (tickets, satisfaction ratings)
    - Geographic and preference data
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the CrmDataset generator.
        
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
        
        # Industries
        self.industries = [
            'Technology', 'Healthcare', 'Finance', 'Manufacturing', 'Retail',
            'Education', 'Real Estate', 'Automotive', 'Energy', 'Telecommunications',
            'Media', 'Transportation', 'Hospitality', 'Construction', 'Agriculture',
            'Pharmaceuticals', 'Aerospace', 'Food & Beverage', 'Legal', 'Consulting'
        ]
        
        # Account managers
        self.account_managers = [
            'Sarah Johnson', 'Mike Davis', 'Lisa Wilson', 'David Brown', 'Jennifer Garcia',
            'Robert Miller', 'Amanda Taylor', 'Chris Anderson', 'Michelle White', 'Kevin Lee',
            'Rachel Green', 'Tom Wilson', 'Emily Chen', 'Mark Thompson', 'Jessica Rodriguez'
        ]
        
        # Interaction channels
        self.interaction_channels = ['Email', 'Phone', 'Meeting', 'Chat', 'Video Call', 'Social Media']
        
        # Sales stages
        self.sales_stages = ['Lead', 'Prospect', 'Negotiation', 'Closed Won', 'Closed Lost']
        
        # Loyalty status levels
        self.loyalty_statuses = ['Bronze', 'Silver', 'Gold', 'Platinum']
        
        # Referral sources
        self.referral_sources = [
            'Online Ad', 'Friend', 'Trade Show', 'Website', 'Social Media',
            'Email Campaign', 'Cold Call', 'Partner Referral', 'Search Engine', 'Direct Mail'
        ]
        
        # Preferred contact times
        self.contact_times = ['Morning', 'Afternoon', 'Evening']
        
        # Account statuses
        self.account_statuses = ['Active', 'Inactive', 'Suspended']
        
        # Regions
        self.regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East & Africa']
        
        # Sample interaction notes
        self.interaction_notes_templates = [
            'Discussed product features and pricing options',
            'Follow-up call scheduled for next week',
            'Customer expressed interest in enterprise solution',
            'Provided demo of new features',
            'Addressed technical questions about integration',
            'Negotiating contract terms and conditions',
            'Customer requested additional references',
            'Discussed implementation timeline',
            'Reviewed proposal and next steps',
            'Customer needs approval from management'
        ]
        
        # Sample notes
        self.notes_templates = [
            'High-value customer with strong growth potential',
            'Requires regular check-ins and support',
            'Decision maker for technology purchases',
            'Price-sensitive but loyal customer',
            'Interested in long-term partnership',
            'Prefers email communication over phone',
            'Has specific compliance requirements',
            'Looking to expand to new markets',
            'Seasonal business with peak in Q4',
            'Strong advocate for our products'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate CRM dataset rows.
        
        Returns:
            List of dictionaries representing CRM customer rows
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
        """Generate a single CRM customer row."""
        
        # Generate customer information
        first_name = self.faker_utils.first_name()
        last_name = self.faker_utils.last_name()
        customer_name = f"{first_name} {last_name}"
        email = self.faker_utils.email(customer_name)
        phone_number = self.faker_utils.phone_number()
        company = self.faker_utils.company()
        industry = random.choice(self.industries)
        
        # Generate account information
        account_manager = random.choice(self.account_managers)
        account_creation_date = self._generate_account_creation_date()
        last_contact_date = self._generate_last_contact_date(account_creation_date)
        
        # Generate interaction data
        interaction_channel = random.choice(self.interaction_channels)
        interaction_notes = random.choice(self.interaction_notes_templates)
        
        # Generate sales pipeline data
        sales_stage = random.choice(self.sales_stages)
        deal_value = self._generate_deal_value(sales_stage)
        deal_probability = self._generate_deal_probability(sales_stage)
        
        # Generate loyalty and purchase data
        loyalty_status = random.choice(self.loyalty_statuses)
        total_orders = self._generate_total_orders(loyalty_status)
        total_spent = self._generate_total_spent(total_orders, loyalty_status)
        
        # Generate support data
        support_tickets = random.randint(0, 20)
        support_satisfaction = random.randint(1, 5) if support_tickets > 0 else None
        
        # Generate preferences and settings
        preferred_contact_time = random.choice(self.contact_times)
        newsletter_subscribed = random.choice([True, False])
        referral_source = random.choice(self.referral_sources)
        
        # Generate geographic data
        region = random.choice(self.regions)
        country = self.faker_utils.country()
        state = self.faker_utils.state()
        city = self.faker_utils.city()
        postal_code = self.faker_utils.postal_code()
        
        # Generate additional data
        notes = random.choice(self.notes_templates)
        account_status = random.choice(self.account_statuses)
        
        return {
            'customer_id': self._generate_customer_id(),
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone_number': phone_number,
            'company': company,
            'industry': industry,
            'account_manager': account_manager,
            'account_creation_date': account_creation_date.strftime('%Y-%m-%d'),
            'last_contact_date': last_contact_date.strftime('%Y-%m-%d'),
            'interaction_channel': interaction_channel,
            'interaction_notes': interaction_notes,
            'sales_stage': sales_stage,
            'deal_value': round(deal_value, 2),
            'deal_probability': deal_probability,
            'loyalty_status': loyalty_status,
            'total_orders': total_orders,
            'total_spent': round(total_spent, 2),
            'support_tickets': support_tickets,
            'support_satisfaction': support_satisfaction,
            'preferred_contact_time': preferred_contact_time,
            'newsletter_subscribed': newsletter_subscribed,
            'referral_source': referral_source,
            'region': region,
            'country': country,
            'state': state,
            'city': city,
            'postal_code': postal_code,
            'notes': notes,
            'account_status': account_status
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
    
    def _generate_account_creation_date(self) -> datetime:
        """
        Generate account creation date (within last 3 years).
        
        Returns:
            Account creation datetime
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1095)  # 3 years
        return self.faker_utils.date_between(start_date, end_date)
    
    def _generate_last_contact_date(self, creation_date: datetime) -> datetime:
        """
        Generate last contact date (between creation date and now).
        
        Args:
            creation_date: Account creation date
            
        Returns:
            Last contact datetime
        """
        end_date = datetime.now()
        return self.faker_utils.date_between(creation_date, end_date)
    
    def _generate_deal_value(self, sales_stage: str) -> float:
        """
        Generate deal value based on sales stage.
        
        Args:
            sales_stage: Current sales stage
            
        Returns:
            Deal value as float
        """
        base_ranges = {
            'Lead': (1000, 25000),
            'Prospect': (5000, 50000),
            'Negotiation': (10000, 100000),
            'Closed Won': (15000, 150000),
            'Closed Lost': (2000, 30000)
        }
        
        min_val, max_val = base_ranges.get(sales_stage, (5000, 50000))
        return random.uniform(min_val, max_val)
    
    def _generate_deal_probability(self, sales_stage: str) -> float:
        """
        Generate deal probability based on sales stage.
        
        Args:
            sales_stage: Current sales stage
            
        Returns:
            Deal probability as percentage (0-100)
        """
        probability_ranges = {
            'Lead': (5, 25),
            'Prospect': (25, 50),
            'Negotiation': (50, 85),
            'Closed Won': (100, 100),
            'Closed Lost': (0, 0)
        }
        
        min_prob, max_prob = probability_ranges.get(sales_stage, (25, 75))
        return random.uniform(min_prob, max_prob)
    
    def _generate_total_orders(self, loyalty_status: str) -> int:
        """
        Generate total orders based on loyalty status.
        
        Args:
            loyalty_status: Customer loyalty level
            
        Returns:
            Total number of orders
        """
        order_ranges = {
            'Bronze': (1, 5),
            'Silver': (6, 15),
            'Gold': (16, 35),
            'Platinum': (36, 100)
        }
        
        min_orders, max_orders = order_ranges.get(loyalty_status, (1, 10))
        return random.randint(min_orders, max_orders)
    
    def _generate_total_spent(self, total_orders: int, loyalty_status: str) -> float:
        """
        Generate total spent based on orders and loyalty status.
        
        Args:
            total_orders: Number of orders
            loyalty_status: Customer loyalty level
            
        Returns:
            Total amount spent
        """
        avg_order_ranges = {
            'Bronze': (50, 200),
            'Silver': (200, 500),
            'Gold': (500, 1500),
            'Platinum': (1500, 5000)
        }
        
        min_avg, max_avg = avg_order_ranges.get(loyalty_status, (100, 500))
        avg_order_value = random.uniform(min_avg, max_avg)
        
        return total_orders * avg_order_value * random.uniform(0.8, 1.2)  # Add some variance
    
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
            'email': 'string',
            'phone_number': 'string',
            'company': 'string',
            'industry': 'string',
            'account_manager': 'string',
            'account_creation_date': 'date',
            'last_contact_date': 'date',
            'interaction_channel': 'string',
            'interaction_notes': 'string',
            'sales_stage': 'string',
            'deal_value': 'float',
            'deal_probability': 'float',
            'loyalty_status': 'string',
            'total_orders': 'integer',
            'total_spent': 'float',
            'support_tickets': 'integer',
            'support_satisfaction': 'integer',
            'preferred_contact_time': 'string',
            'newsletter_subscribed': 'boolean',
            'referral_source': 'string',
            'region': 'string',
            'country': 'string',
            'state': 'string',
            'city': 'string',
            'postal_code': 'string',
            'notes': 'string',
            'account_status': 'string'
        }