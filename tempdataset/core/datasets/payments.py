"""
Payments dataset generator.

Generates realistic digital payment transactions through multiple gateways.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class PaymentsDataset(BaseDataset):
    """Payments dataset generator for digital payment transactions."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._transaction_counter = 100001
    
    def _init_data_lists(self) -> None:
        self.payment_methods = [
            'Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay',
            'Bank Transfer', 'Cryptocurrency', 'Stripe', 'Square', 'Venmo', 'Zelle'
        ]
        
        self.payment_gateways = [
            'Stripe', 'PayPal', 'Square', 'Braintree', 'Authorize.Net',
            'Worldpay', 'Adyen', 'Klarna', 'Razorpay', 'Mollie'
        ]
        
        self.currencies = ['USD', 'EUR', 'GBP', 'CAD', 'AUD', 'JPY', 'CHF', 'SEK', 'NOK', 'DKK']
        
        self.transaction_types = [
            'Purchase', 'Refund', 'Recurring', 'Subscription', 'Transfer',
            'Withdrawal', 'Deposit', 'Fee', 'Chargeback', 'Authorization'
        ]
        
        self.transaction_statuses = ['Pending', 'Completed', 'Failed', 'Cancelled', 'Refunded']
        
        self.countries = [
            'United States', 'United Kingdom', 'Germany', 'France', 'Canada',
            'Australia', 'Netherlands', 'Sweden', 'Norway', 'Denmark'
        ]
        
        self.merchants = [
            'Amazon', 'eBay', 'Shopify Store', 'WooCommerce', 'Etsy',
            'Best Buy', 'Target', 'Walmart', 'Nike', 'Apple Store'
        ]
        
        self.failure_reasons = [
            'Insufficient funds', 'Card expired', 'Invalid CVV', 'Card declined',
            'Network error', 'Fraud detected', 'Limit exceeded', 'Invalid account'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic transaction info
        transaction_id = f"TXN-{self._transaction_counter:08d}"
        self._transaction_counter += 1
        
        # Dates
        date_part = self.faker_utils.date_between(
            datetime.now() - timedelta(days=90), datetime.now()
        )
        # Add random time component
        created_at = datetime.combine(
            date_part, 
            datetime.min.time().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Payment details
        payment_method = random.choice(self.payment_methods)
        payment_gateway = random.choice(self.payment_gateways)
        transaction_type = random.choice(self.transaction_types)
        
        # Amount generation based on transaction type
        if transaction_type == 'Fee':
            amount = random.uniform(0.30, 25.00)
        elif transaction_type in ['Transfer', 'Withdrawal', 'Deposit']:
            amount = random.uniform(50, 5000)
        elif transaction_type == 'Subscription':
            amount = random.choice([9.99, 19.99, 29.99, 49.99, 99.99])
        else:  # Purchase, Refund, etc.
            amount = random.uniform(5, 2000)
        
        # Currency (affects amount slightly for non-USD)
        currency = random.choice(self.currencies)
        if currency == 'JPY':
            amount *= 110  # Approximate USD to JPY conversion
        elif currency == 'EUR':
            amount *= 0.85
        elif currency == 'GBP':
            amount *= 0.75
        
        # Status and processing
        status = random.choice(self.transaction_statuses)
        
        # Processing times
        if status == 'Completed':
            processing_time_seconds = random.uniform(1.2, 45.0)
            settled_at = created_at + timedelta(seconds=processing_time_seconds)
        elif status == 'Pending':
            processing_time_seconds = None
            settled_at = None
        else:
            processing_time_seconds = random.uniform(0.5, 15.0)
            settled_at = None
        
        # Fee calculation (gateway takes a cut)
        if status == 'Completed' and transaction_type not in ['Refund', 'Chargeback']:
            fee_percentage = random.uniform(0.025, 0.035)  # 2.5% - 3.5%
            fixed_fee = random.uniform(0.15, 0.30)
            transaction_fee = amount * fee_percentage + fixed_fee
        else:
            transaction_fee = 0.00
        
        # Customer info
        customer_id = f"CUST-{random.randint(10000, 99999)}"
        customer_email = self.faker_utils.email()
        
        # Merchant info
        merchant_name = random.choice(self.merchants)
        merchant_category = random.choice([
            'E-commerce', 'Retail', 'Software', 'Digital Services', 'Food & Beverage',
            'Travel', 'Entertainment', 'Finance', 'Healthcare', 'Education'
        ])
        
        # Geographic data
        billing_country = random.choice(self.countries)
        ip_address = f"{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Risk assessment
        risk_score = random.uniform(0, 100)
        fraud_detected = risk_score > 85 or status == 'Failed' and random.random() < 0.3
        
        # Failure handling
        failure_reason = None
        if status == 'Failed':
            failure_reason = random.choice(self.failure_reasons)
        
        # Card/account info (masked for security)
        if payment_method in ['Credit Card', 'Debit Card']:
            card_last_four = f"****-{random.randint(1000, 9999)}"
            card_brand = random.choice(['Visa', 'Mastercard', 'Amex', 'Discover'])
            account_id = None
        elif payment_method in ['PayPal', 'Stripe', 'Square']:
            card_last_four = None
            card_brand = None
            account_id = f"{payment_method.upper()}-{random.randint(100000, 999999)}"
        else:
            card_last_four = None
            card_brand = None
            account_id = f"ACC-{random.randint(1000000, 9999999)}"
        
        # Reference numbers
        gateway_reference = f"{payment_gateway.upper()}-{random.randint(1000000, 9999999)}"
        merchant_reference = f"ORD-{random.randint(100000, 999999)}"
        
        # Recurring payment info
        is_recurring = transaction_type in ['Recurring', 'Subscription']
        recurring_frequency = None
        if is_recurring:
            recurring_frequency = random.choice(['Monthly', 'Quarterly', 'Yearly', 'Weekly'])
        
        # Metadata
        user_agent = random.choice([
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'Mozilla/5.0 (iPhone; CPU iPhone OS 14_7_1 like Mac OS X)',
            'Mozilla/5.0 (Android 11; Mobile; rv:89.0) Gecko/89.0'
        ]) if random.random() < 0.8 else None
        
        return {
            'transaction_id': transaction_id,
            'payment_method': payment_method,
            'payment_gateway': payment_gateway,
            'transaction_type': transaction_type,
            'amount': round(amount, 2),
            'currency': currency,
            'transaction_fee': round(transaction_fee, 2),
            'status': status,
            'created_at': created_at.strftime('%Y-%m-%d %H:%M:%S'),
            'settled_at': settled_at.strftime('%Y-%m-%d %H:%M:%S') if settled_at else None,
            'processing_time_seconds': round(processing_time_seconds, 2) if processing_time_seconds else None,
            'customer_id': customer_id,
            'customer_email': customer_email,
            'merchant_name': merchant_name,
            'merchant_category': merchant_category,
            'card_last_four': card_last_four,
            'card_brand': card_brand,
            'account_id': account_id,
            'billing_country': billing_country,
            'ip_address': ip_address,
            'gateway_reference': gateway_reference,
            'merchant_reference': merchant_reference,
            'risk_score': round(risk_score, 2),
            'fraud_detected': fraud_detected,
            'failure_reason': failure_reason,
            'is_recurring': is_recurring,
            'recurring_frequency': recurring_frequency,
            'user_agent': user_agent[:50] + '...' if user_agent and len(user_agent) > 50 else user_agent
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'transaction_id': 'string', 'payment_method': 'string', 'payment_gateway': 'string',
            'transaction_type': 'string', 'amount': 'float', 'currency': 'string',
            'transaction_fee': 'float', 'status': 'string', 'created_at': 'datetime',
            'settled_at': 'datetime', 'processing_time_seconds': 'float', 'customer_id': 'string',
            'customer_email': 'string', 'merchant_name': 'string', 'merchant_category': 'string',
            'card_last_four': 'string', 'card_brand': 'string', 'account_id': 'string',
            'billing_country': 'string', 'ip_address': 'string', 'gateway_reference': 'string',
            'merchant_reference': 'string', 'risk_score': 'float', 'fraud_detected': 'boolean',
            'failure_reason': 'string', 'is_recurring': 'boolean', 'recurring_frequency': 'string',
            'user_agent': 'string'
        }
