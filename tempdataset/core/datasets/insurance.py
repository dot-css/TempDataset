"""
Insurance dataset generator.

Generates realistic insurance policy, claims, and risk assessment data.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class InsuranceDataset(BaseDataset):
    """
    Insurance dataset generator that creates realistic insurance data.
    
    Generates 20 columns of insurance data including:
    - Policy information (ID, type, coverage, premiums)
    - Claims data (claim ID, amounts, status)
    - Risk assessment and agent information
    - Geographic and temporal data
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the InsuranceDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._policy_counter = 10001
        self._customer_counter = 1
        self._claim_counter = 1001
        self._agent_counter = 101
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Policy types
        self.policy_types = ['Auto', 'Health', 'Property', 'Life', 'Business', 'Travel', 'Disability']
        
        # Payment frequencies
        self.payment_frequencies = ['Monthly', 'Quarterly', 'Semi-Annual', 'Annual']
        
        # Claim reasons by policy type
        self.claim_reasons = {
            'Auto': ['Collision', 'Theft', 'Vandalism', 'Weather Damage', 'Hit and Run', 'Glass Damage'],
            'Health': ['Emergency Room', 'Surgery', 'Prescription Drugs', 'Specialist Visit', 'Diagnostic Tests', 'Physical Therapy'],
            'Property': ['Fire Damage', 'Water Damage', 'Theft', 'Storm Damage', 'Vandalism', 'Equipment Failure'],
            'Life': ['Death Benefit', 'Terminal Illness', 'Accidental Death'],
            'Business': ['Property Damage', 'Liability Claim', 'Business Interruption', 'Cyber Attack', 'Equipment Loss'],
            'Travel': ['Trip Cancellation', 'Medical Emergency', 'Lost Luggage', 'Flight Delay', 'Emergency Evacuation'],
            'Disability': ['Injury', 'Illness', 'Accident', 'Work-Related Disability']
        }
        
        # Claim statuses
        self.claim_statuses = ['Pending', 'Under Review', 'Approved', 'Rejected', 'Paid', 'Partially Paid', 'Closed']
        
        # Risk ratings
        self.risk_ratings = ['Low', 'Medium', 'High', 'Very High']
        
        # Agent names
        self.agent_names = [
            'John Smith', 'Sarah Johnson', 'Michael Brown', 'Lisa Davis', 'Robert Wilson',
            'Jennifer Garcia', 'David Miller', 'Amanda Taylor', 'Christopher Anderson', 'Michelle Martinez',
            'Daniel Thompson', 'Jessica White', 'Matthew Jackson', 'Ashley Harris', 'James Martin',
            'Emily Clark', 'Andrew Rodriguez', 'Stephanie Lewis', 'Joshua Walker', 'Nicole Hall'
        ]
        
        # Regions
        self.regions = ['Northeast', 'Southeast', 'Midwest', 'Southwest', 'West', 'Northwest', 'Central']
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate insurance dataset rows.
        
        Returns:
            List of dictionaries representing insurance data rows
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
        """Generate a single insurance data row."""
        
        # Generate policy information
        policy_type = random.choice(self.policy_types)
        payment_frequency = random.choice(self.payment_frequencies)
        
        # Generate policy dates
        start_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1095),  # 3 years ago
            datetime.now() - timedelta(days=30)     # 30 days ago
        )
        
        # Policy duration varies by type
        duration_months = self._get_policy_duration(policy_type)
        end_date = start_date + timedelta(days=duration_months * 30)
        
        # Generate coverage and premium amounts
        coverage_amount = self._generate_coverage_amount(policy_type)
        premium_amount = self._generate_premium_amount(policy_type, coverage_amount)
        
        # Generate claim information (not all policies have claims)
        has_claim = random.random() < 0.3  # 30% of policies have claims
        
        claim_id = None
        claim_date = None
        claim_amount = None
        claim_reason = None
        claim_status = None
        
        if has_claim:
            claim_id = self._generate_claim_id()
            claim_date = self.faker_utils.date_between(start_date, min(end_date, datetime.now().date()))
            claim_amount = self._generate_claim_amount(policy_type, coverage_amount)
            claim_reason = random.choice(self.claim_reasons.get(policy_type, ['General Claim']))
            claim_status = random.choice(self.claim_statuses)
        
        # Generate risk score
        risk_score = self._generate_risk_score(policy_type, has_claim)
        
        # Generate agent information
        agent_name = random.choice(self.agent_names)
        
        # Generate location information
        region = random.choice(self.regions)
        country = self.faker_utils.country()
        city = self.faker_utils.city()
        
        # Generate notes (occasionally)
        notes = None
        if random.random() < 0.2:
            note_options = [
                'Customer requested policy review', 'Premium discount applied', 'Multi-policy discount',
                'Good driver discount', 'No claims bonus', 'Policy auto-renewed', 'Payment plan adjusted',
                'Coverage increased', 'Deductible modified', 'Agent referral bonus'
            ]
            notes = random.choice(note_options)
        
        return {
            'policy_id': self._generate_policy_id(),
            'customer_id': self._generate_customer_id(),
            'policy_type': policy_type,
            'coverage_amount': coverage_amount,
            'premium_amount': round(premium_amount, 2),
            'payment_frequency': payment_frequency,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d'),
            'claim_id': claim_id,
            'claim_date': claim_date.strftime('%Y-%m-%d') if claim_date else None,
            'claim_amount': round(claim_amount, 2) if claim_amount else None,
            'claim_reason': claim_reason,
            'claim_status': claim_status,
            'risk_score': round(risk_score, 3),
            'agent_id': self._generate_agent_id(),
            'agent_name': agent_name,
            'region': region,
            'country': country,
            'city': city,
            'notes': notes
        }
    
    def _generate_policy_id(self) -> str:
        """Generate policy ID in format POL-NNNNNN."""
        policy_num = str(self._policy_counter).zfill(6)
        self._policy_counter += 1
        return f"POL-{policy_num}"
    
    def _generate_customer_id(self) -> str:
        """Generate customer ID in format CUST-NNNNNN."""
        customer_num = str(self._customer_counter).zfill(6)
        self._customer_counter += 1
        return f"CUST-{customer_num}"
    
    def _generate_claim_id(self) -> str:
        """Generate claim ID in format CLM-NNNNNN."""
        claim_num = str(self._claim_counter).zfill(6)
        self._claim_counter += 1
        return f"CLM-{claim_num}"
    
    def _generate_agent_id(self) -> str:
        """Generate agent ID in format AGT-NNN."""
        agent_num = str(self._agent_counter).zfill(3)
        self._agent_counter += 1
        return f"AGT-{agent_num}"
    
    def _get_policy_duration(self, policy_type: str) -> int:
        """
        Get typical policy duration in months.
        
        Args:
            policy_type: Type of insurance policy
            
        Returns:
            Duration in months
        """
        durations = {
            'Auto': 12,
            'Health': 12,
            'Property': 12,
            'Life': 240,  # 20 years
            'Business': 12,
            'Travel': 1,
            'Disability': 24
        }
        
        return durations.get(policy_type, 12)
    
    def _generate_coverage_amount(self, policy_type: str) -> float:
        """
        Generate realistic coverage amount based on policy type.
        
        Args:
            policy_type: Type of insurance policy
            
        Returns:
            Coverage amount
        """
        coverage_ranges = {
            'Auto': (25000, 500000),
            'Health': (50000, 2000000),
            'Property': (100000, 1000000),
            'Life': (50000, 5000000),
            'Business': (100000, 10000000),
            'Travel': (1000, 100000),
            'Disability': (25000, 500000)
        }
        
        min_coverage, max_coverage = coverage_ranges.get(policy_type, (10000, 100000))
        return round(random.uniform(min_coverage, max_coverage), 2)
    
    def _generate_premium_amount(self, policy_type: str, coverage_amount: float) -> float:
        """
        Generate realistic premium amount based on policy type and coverage.
        
        Args:
            policy_type: Type of insurance policy
            coverage_amount: Coverage amount
            
        Returns:
            Premium amount
        """
        # Premium as percentage of coverage
        premium_rates = {
            'Auto': (0.02, 0.08),      # 2-8% of coverage
            'Health': (0.05, 0.15),    # 5-15% of coverage
            'Property': (0.005, 0.02), # 0.5-2% of coverage
            'Life': (0.01, 0.05),      # 1-5% of coverage
            'Business': (0.01, 0.08),  # 1-8% of coverage
            'Travel': (0.05, 0.2),     # 5-20% of coverage
            'Disability': (0.02, 0.1)  # 2-10% of coverage
        }
        
        min_rate, max_rate = premium_rates.get(policy_type, (0.01, 0.05))
        rate = random.uniform(min_rate, max_rate)
        
        return coverage_amount * rate
    
    def _generate_claim_amount(self, policy_type: str, coverage_amount: float) -> float:
        """
        Generate realistic claim amount.
        
        Args:
            policy_type: Type of insurance policy
            coverage_amount: Coverage amount
            
        Returns:
            Claim amount
        """
        # Claims are typically a fraction of coverage
        max_claim = coverage_amount * 0.8  # Max 80% of coverage
        min_claim = coverage_amount * 0.001  # Min 0.1% of coverage
        
        # Skew towards smaller claims
        claim_amount = random.uniform(min_claim, max_claim)
        
        # Apply power law distribution (most claims are small)
        claim_amount = claim_amount * (random.random() ** 2)
        
        return max(100, claim_amount)  # Minimum claim of $100
    
    def _generate_risk_score(self, policy_type: str, has_claim: bool) -> float:
        """
        Generate risk score based on policy type and claim history.
        
        Args:
            policy_type: Type of insurance policy
            has_claim: Whether policy has claims
            
        Returns:
            Risk score between 0 and 1
        """
        base_risk = {
            'Auto': 0.3,
            'Health': 0.4,
            'Property': 0.2,
            'Life': 0.1,
            'Business': 0.5,
            'Travel': 0.6,
            'Disability': 0.3
        }.get(policy_type, 0.3)
        
        # Adjust risk based on claims
        if has_claim:
            base_risk += 0.2
        
        # Add random variation
        risk_score = base_risk + random.uniform(-0.2, 0.2)
        
        # Ensure score is between 0 and 1
        return max(0, min(1, risk_score))
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'policy_id': 'string',
            'customer_id': 'string',
            'policy_type': 'string',
            'coverage_amount': 'float',
            'premium_amount': 'float',
            'payment_frequency': 'string',
            'start_date': 'date',
            'end_date': 'date',
            'claim_id': 'string',
            'claim_date': 'date',
            'claim_amount': 'float',
            'claim_reason': 'string',
            'claim_status': 'string',
            'risk_score': 'float',
            'agent_id': 'string',
            'agent_name': 'string',
            'region': 'string',
            'country': 'string',
            'city': 'string',
            'notes': 'string'
        }
