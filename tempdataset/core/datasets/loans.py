"""
Loans dataset generator.

Generates realistic loan application, approval, and repayment data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class LoansDataset(BaseDataset):
    """
    Loans dataset generator that creates realistic loan data.
    
    Generates 20 columns of loan data including:
    - Loan application and approval information
    - Loan terms and payment details
    - Risk assessment and collateral information
    - Payment status and branch data
    """
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._loan_counter = 100001
        self._customer_counter = 1
        self._branch_counter = 1
    
    def _init_data_lists(self) -> None:
        self.loan_types = ['Mortgage', 'Auto', 'Personal', 'Student', 'Business', 'Home Equity']
        self.payment_statuses = ['Current', 'Late', 'Defaulted', 'Paid Off', '30 Days Late', '60 Days Late', '90+ Days Late']
        self.risk_ratings = ['Low', 'Medium', 'High', 'Very High']
        self.collateral_types = ['Real Estate', 'Vehicle', 'Equipment', 'Securities', 'Cash Deposit', None]
        self.branch_locations = ['Downtown Branch', 'Mall Branch', 'Suburban Branch', 'Business District Branch']
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        loan_type = random.choice(self.loan_types)
        
        # Application date
        application_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1095), datetime.now() - timedelta(days=30)
        )
        
        # Approval date (80% get approved)
        approval_date = None
        if random.random() < 0.8:
            approval_date = application_date + timedelta(days=random.randint(1, 30))
        
        # Loan terms based on type
        loan_amount, interest_rate, term_months = self._generate_loan_terms(loan_type)
        
        # Monthly payment calculation
        monthly_rate = interest_rate / 100 / 12
        if monthly_rate > 0:
            monthly_payment = (loan_amount * monthly_rate * (1 + monthly_rate) ** term_months) / \
                             ((1 + monthly_rate) ** term_months - 1)
        else:
            monthly_payment = loan_amount / term_months
        
        total_repayment = monthly_payment * term_months
        
        # Payment status and last payment
        payment_status = random.choice(self.payment_statuses)
        
        last_payment_date = None
        if approval_date and payment_status != 'Defaulted':
            last_payment_date = approval_date + timedelta(days=random.randint(30, 365))
        
        # Outstanding balance
        if payment_status == 'Paid Off':
            outstanding_balance = 0
        elif approval_date:
            payments_made = random.randint(0, term_months)
            outstanding_balance = max(0, loan_amount - (payments_made * (loan_amount / term_months)))
        else:
            outstanding_balance = loan_amount
        
        # Collateral
        collateral = self._get_collateral(loan_type)
        
        # Credit score and risk rating
        credit_score = random.randint(300, 850)
        risk_rating = self._get_risk_rating(credit_score, loan_type)
        
        # Location
        country = self.faker_utils.country()
        branch_location = random.choice(self.branch_locations)
        
        # Notes
        notes = random.choice([
            'First-time borrower', 'Repeat customer', 'Co-signer required', 'Income verified',
            'Self-employed borrower', 'High debt-to-income ratio', 'Excellent credit history', None
        ]) if random.random() < 0.3 else None
        
        return {
            'loan_id': f"LOAN-{self._loan_counter:06d}",
            'customer_id': f"CUST-{self._customer_counter:06d}",
            'loan_type': loan_type,
            'application_date': application_date.strftime('%Y-%m-%d'),
            'approval_date': approval_date.strftime('%Y-%m-%d') if approval_date else None,
            'loan_amount': round(loan_amount, 2),
            'interest_rate': round(interest_rate, 2),
            'term_months': term_months,
            'monthly_payment': round(monthly_payment, 2),
            'total_repayment': round(total_repayment, 2),
            'payment_status': payment_status,
            'last_payment_date': last_payment_date.strftime('%Y-%m-%d') if last_payment_date else None,
            'outstanding_balance': round(outstanding_balance, 2),
            'collateral': collateral,
            'credit_score': credit_score,
            'risk_rating': risk_rating,
            'branch_id': f"BR-{self._branch_counter:03d}",
            'branch_location': branch_location,
            'country': country,
            'notes': notes
        }
    
    def _generate_loan_terms(self, loan_type: str):
        terms = {
            'Mortgage': (random.uniform(100000, 800000), random.uniform(2.5, 6.5), random.choice([180, 240, 300, 360])),
            'Auto': (random.uniform(15000, 80000), random.uniform(3.0, 8.0), random.choice([36, 48, 60, 72])),
            'Personal': (random.uniform(5000, 50000), random.uniform(6.0, 18.0), random.choice([24, 36, 48, 60])),
            'Student': (random.uniform(10000, 100000), random.uniform(3.0, 7.0), random.choice([120, 180, 240])),
            'Business': (random.uniform(25000, 500000), random.uniform(4.0, 12.0), random.choice([60, 84, 120])),
            'Home Equity': (random.uniform(20000, 200000), random.uniform(3.5, 8.5), random.choice([120, 180, 240]))
        }
        return terms.get(loan_type, (random.uniform(10000, 100000), random.uniform(5.0, 15.0), 60))
    
    def _get_collateral(self, loan_type: str):
        collateral_map = {
            'Mortgage': 'Real Estate',
            'Auto': 'Vehicle',
            'Home Equity': 'Real Estate',
            'Business': random.choice(['Equipment', 'Real Estate', 'Securities']),
            'Personal': random.choice([None, 'Cash Deposit']),
            'Student': None
        }
        return collateral_map.get(loan_type, None)
    
    def _get_risk_rating(self, credit_score: int, loan_type: str):
        if credit_score >= 750:
            return 'Low'
        elif credit_score >= 650:
            return 'Medium'
        elif credit_score >= 550:
            return 'High'
        else:
            return 'Very High'
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'loan_id': 'string', 'customer_id': 'string', 'loan_type': 'string',
            'application_date': 'date', 'approval_date': 'date', 'loan_amount': 'float',
            'interest_rate': 'float', 'term_months': 'integer', 'monthly_payment': 'float',
            'total_repayment': 'float', 'payment_status': 'string', 'last_payment_date': 'date',
            'outstanding_balance': 'float', 'collateral': 'string', 'credit_score': 'integer',
            'risk_rating': 'string', 'branch_id': 'string', 'branch_location': 'string',
            'country': 'string', 'notes': 'string'
        }
