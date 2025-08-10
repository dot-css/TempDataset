"""
Banking dataset generator.

Generates realistic banking transaction data with account details and fraud detection.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class BankingDataset(BaseDataset):
    """
    Banking dataset generator that creates realistic banking transaction data.
    
    Generates 20 columns of banking data including:
    - Transaction details (ID, type, amount, currency)
    - Account information (account ID, type, balances)
    - Merchant and location data
    - Fraud detection indicators
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the BankingDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._transaction_counter = 1
        self._account_counter = 1000
        self._customer_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Account types
        self.account_types = ['Checking', 'Savings', 'Business', 'Money Market', 'Certificate of Deposit']
        
        # Transaction types
        self.transaction_types = ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee', 'Interest', 'Refund']
        
        # Merchant categories
        self.merchant_categories = [
            'Grocery Stores', 'Gas Stations', 'Restaurants', 'Retail Stores', 'Online Shopping',
            'ATM Withdrawals', 'Bank Transfers', 'Utility Payments', 'Insurance Payments',
            'Healthcare', 'Entertainment', 'Travel', 'Education', 'Professional Services',
            'Home Improvement', 'Automotive', 'Clothing', 'Electronics', 'Pharmacy',
            'Subscription Services'
        ]
        
        # Merchants by category
        self.merchants = {
            'Grocery Stores': ['Walmart Supercenter', 'Target', 'Kroger', 'Safeway', 'Whole Foods Market', 'Costco Wholesale'],
            'Gas Stations': ['Shell', 'Exxon', 'BP', 'Chevron', 'Mobil', '76', 'Arco', 'Texaco'],
            'Restaurants': ['McDonald\'s', 'Starbucks', 'Subway', 'Pizza Hut', 'KFC', 'Taco Bell', 'Chipotle', 'Panera Bread'],
            'Retail Stores': ['Amazon', 'Best Buy', 'Home Depot', 'Lowe\'s', 'Macy\'s', 'Target', 'CVS Pharmacy'],
            'Online Shopping': ['Amazon.com', 'eBay', 'PayPal', 'Apple Store', 'Google Play', 'Netflix', 'Spotify'],
            'ATM Withdrawals': ['Bank of America ATM', 'Chase ATM', 'Wells Fargo ATM', 'Citibank ATM', 'Local Credit Union ATM'],
            'Bank Transfers': ['Zelle Transfer', 'Wire Transfer', 'ACH Transfer', 'Online Banking Transfer'],
            'Utility Payments': ['Electric Company', 'Gas Company', 'Water Department', 'Internet Provider', 'Cable Company'],
            'Insurance Payments': ['Auto Insurance', 'Health Insurance', 'Home Insurance', 'Life Insurance'],
            'Healthcare': ['Medical Center', 'Dental Office', 'Pharmacy', 'Urgent Care', 'Specialist Clinic'],
            'Entertainment': ['Movie Theater', 'Concert Venue', 'Sports Arena', 'Theme Park', 'Streaming Service'],
            'Travel': ['Airport', 'Hotel', 'Rental Car', 'Uber', 'Lyft', 'Airline'],
            'Education': ['University Tuition', 'Student Loans', 'Online Course', 'Textbook Store'],
            'Professional Services': ['Legal Services', 'Accounting Firm', 'Consulting', 'Real Estate'],
            'Home Improvement': ['Home Depot', 'Lowe\'s', 'Hardware Store', 'Contractor Payment'],
            'Automotive': ['Auto Dealership', 'Car Repair Shop', 'Auto Parts Store', 'Car Wash'],
            'Clothing': ['Department Store', 'Fashion Retailer', 'Shoe Store', 'Online Clothing'],
            'Electronics': ['Best Buy', 'Apple Store', 'Electronics Store', 'Computer Store'],
            'Pharmacy': ['CVS Pharmacy', 'Walgreens', 'Rite Aid', 'Local Pharmacy'],
            'Subscription Services': ['Netflix', 'Spotify', 'Amazon Prime', 'Gym Membership', 'Magazine Subscription']
        }
        
        # Currencies
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'CNY']
        
        # Fraud reasons
        self.fraud_reasons = [
            'Suspicious location', 'Unusual spending pattern', 'Card not present', 
            'Multiple failed PIN attempts', 'High-risk merchant', 'Velocity check failed',
            'Blacklisted merchant', 'Suspicious time of transaction', 'Amount threshold exceeded'
        ]
        
        # Branch locations
        self.branch_locations = [
            'Downtown Branch', 'Mall Branch', 'Airport Branch', 'University Branch',
            'Business District Branch', 'Suburban Branch', 'Highway Branch', 'Shopping Center Branch'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate banking dataset rows.
        
        Returns:
            List of dictionaries representing banking transaction rows
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
        """Generate a single banking transaction row."""
        
        # Generate transaction date (within last year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        transaction_date = self.faker_utils.date_between(start_date, end_date)
        
        # Generate account information
        account_type = random.choice(self.account_types)
        transaction_type = random.choice(self.transaction_types)
        
        # Generate transaction amount based on type and account
        transaction_amount = self._generate_transaction_amount(transaction_type, account_type)
        
        # Generate merchant information (not all transactions have merchants)
        merchant_name = None
        merchant_category = None
        
        if transaction_type in ['Payment', 'Withdrawal'] and random.random() > 0.3:
            merchant_category = random.choice(self.merchant_categories)
            if merchant_category in self.merchants:
                merchant_name = random.choice(self.merchants[merchant_category])
        
        # Generate balances
        balance_before = random.uniform(100, 50000)
        
        if transaction_type in ['Deposit', 'Interest', 'Refund']:
            balance_after = balance_before + transaction_amount
        else:
            balance_after = balance_before - transaction_amount
        
        # Ensure balance doesn't go negative (with some overdraft allowance)
        if balance_after < -500:
            balance_after = random.uniform(-500, 0)
            balance_before = balance_after + transaction_amount
        
        # Generate location information
        country = self.faker_utils.country()
        city = self.faker_utils.city()
        postal_code = self.faker_utils.postal_code()
        
        # Generate fraud detection
        fraud_flag = self._determine_fraud_flag(transaction_amount, merchant_category, transaction_type)
        fraud_reason = None
        
        if fraud_flag:
            fraud_reason = random.choice(self.fraud_reasons)
        
        # Generate branch information
        branch_location = random.choice(self.branch_locations)
        
        # Currency (mostly local currency with some international)
        currency = random.choice(self.currencies) if random.random() < 0.1 else 'USD'
        
        # Notes (occasionally present)
        notes = None
        if random.random() < 0.15:
            note_options = [
                'Customer initiated transfer', 'Automatic bill payment', 'Mobile deposit',
                'ATM transaction', 'Online banking transaction', 'Branch transaction',
                'Phone banking transaction', 'Recurring payment', 'One-time payment'
            ]
            notes = random.choice(note_options)
        
        return {
            'transaction_id': self._generate_transaction_id(),
            'account_id': self._generate_account_id(),
            'customer_id': self._generate_customer_id(),
            'account_type': account_type,
            'transaction_date': transaction_date.strftime('%Y-%m-%d %H:%M:%S'),
            'transaction_type': transaction_type,
            'transaction_amount': round(transaction_amount, 2),
            'currency': currency,
            'merchant_name': merchant_name,
            'merchant_category': merchant_category,
            'balance_before': round(balance_before, 2),
            'balance_after': round(balance_after, 2),
            'branch_id': self._generate_branch_id(),
            'branch_location': branch_location,
            'fraud_flag': fraud_flag,
            'fraud_reason': fraud_reason,
            'country': country,
            'city': city,
            'postal_code': postal_code,
            'notes': notes
        }
    
    def _generate_transaction_id(self) -> str:
        """Generate transaction ID in format TXN-YYYYMMDD-NNNNNN."""
        date_part = datetime.now().strftime('%Y%m%d')
        number_part = str(self._transaction_counter).zfill(6)
        self._transaction_counter += 1
        return f"TXN-{date_part}-{number_part}"
    
    def _generate_account_id(self) -> str:
        """Generate account ID in format ACC-NNNNNNN."""
        account_num = str(self._account_counter).zfill(7)
        self._account_counter += 1
        return f"ACC-{account_num}"
    
    def _generate_customer_id(self) -> str:
        """Generate customer ID in format CUST-NNNNNN."""
        customer_num = str(self._customer_counter).zfill(6)
        self._customer_counter += 1
        return f"CUST-{customer_num}"
    
    def _generate_branch_id(self) -> str:
        """Generate branch ID in format BR-NNN."""
        branch_num = str(random.randint(1, 999)).zfill(3)
        return f"BR-{branch_num}"
    
    def _generate_transaction_amount(self, transaction_type: str, account_type: str) -> float:
        """
        Generate realistic transaction amount based on type and account.
        
        Args:
            transaction_type: Type of transaction
            account_type: Type of account
            
        Returns:
            Transaction amount
        """
        base_ranges = {
            'Deposit': (50, 5000),
            'Withdrawal': (20, 1000),
            'Transfer': (100, 10000),
            'Payment': (15, 2000),
            'Fee': (5, 50),
            'Interest': (1, 100),
            'Refund': (10, 500)
        }
        
        # Adjust ranges based on account type
        if account_type == 'Business':
            multiplier = random.uniform(2, 10)
        elif account_type == 'Savings':
            multiplier = random.uniform(1.5, 3)
        else:
            multiplier = 1
        
        min_amount, max_amount = base_ranges.get(transaction_type, (10, 1000))
        amount = random.uniform(min_amount, max_amount) * multiplier
        
        return amount
    
    def _determine_fraud_flag(self, amount: float, merchant_category: str, transaction_type: str) -> bool:
        """
        Determine if transaction should be flagged as fraudulent.
        
        Args:
            amount: Transaction amount
            merchant_category: Merchant category
            transaction_type: Transaction type
            
        Returns:
            True if flagged as fraud, False otherwise
        """
        fraud_probability = 0.02  # Base 2% fraud rate
        
        # Increase fraud probability for high amounts
        if amount > 5000:
            fraud_probability += 0.05
        elif amount > 2000:
            fraud_probability += 0.02
        
        # Increase fraud probability for certain categories
        high_risk_categories = ['Online Shopping', 'Electronics', 'Travel', 'Entertainment']
        if merchant_category in high_risk_categories:
            fraud_probability += 0.03
        
        # Increase fraud probability for withdrawals
        if transaction_type == 'Withdrawal':
            fraud_probability += 0.01
        
        return random.random() < fraud_probability
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'transaction_id': 'string',
            'account_id': 'string',
            'customer_id': 'string',
            'account_type': 'string',
            'transaction_date': 'datetime',
            'transaction_type': 'string',
            'transaction_amount': 'float',
            'currency': 'string',
            'merchant_name': 'string',
            'merchant_category': 'string',
            'balance_before': 'float',
            'balance_after': 'float',
            'branch_id': 'string',
            'branch_location': 'string',
            'fraud_flag': 'boolean',
            'fraud_reason': 'string',
            'country': 'string',
            'city': 'string',
            'postal_code': 'string',
            'notes': 'string'
        }
