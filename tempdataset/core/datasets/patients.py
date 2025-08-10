"""
Patients dataset generator.

Generates realistic patient records for healthcare systems.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class PatientsDataset(BaseDataset):
    """Patients dataset generator for healthcare records."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._patient_counter = 1
    
    def _init_data_lists(self) -> None:
        self.genders = ['Male', 'Female', 'Other']
        self.blood_types = ['A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-']
        self.statuses = ['Active', 'Inactive', 'Deceased']
        
        self.insurance_providers = [
            'Blue Cross Blue Shield', 'Aetna', 'Cigna', 'UnitedHealthcare',
            'Humana', 'Kaiser Permanente', 'Anthem', 'Medicaid', 'Medicare',
            'Tricare', 'Health Net', 'Molina Healthcare'
        ]
        
        self.common_allergies = [
            'Penicillin', 'Peanuts', 'Shellfish', 'Latex', 'Sulfa drugs',
            'Tree nuts', 'Eggs', 'Milk', 'Soy', 'Wheat', 'Aspirin',
            'Iodine', 'Codeine', 'Morphine', None
        ]
        
        self.chronic_conditions = [
            'Diabetes Type 2', 'Hypertension', 'Asthma', 'Arthritis',
            'Depression', 'Anxiety Disorder', 'COPD', 'Heart Disease',
            'High Cholesterol', 'Osteoporosis', 'Chronic Pain',
            'Fibromyalgia', 'Migraine', 'Sleep Apnea', None
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic patient info
        patient_id = f"PAT-2025-{self._patient_counter:06d}"
        self._patient_counter += 1
        
        first_name = self.faker_utils.first_name()
        last_name = self.faker_utils.last_name()
        
        # Demographics
        gender = random.choice(self.genders)
        
        # Age distribution - more realistic with higher concentration in middle age
        age_weights = [0.05, 0.15, 0.25, 0.30, 0.20, 0.05]  # 0-17, 18-35, 36-50, 51-65, 66-80, 81+
        age_ranges = [(0, 17), (18, 35), (36, 50), (51, 65), (66, 80), (81, 95)]
        age_range = random.choices(age_ranges, weights=age_weights)[0]
        age = random.randint(age_range[0], age_range[1])
        
        date_of_birth = datetime.now() - timedelta(days=age * 365 + random.randint(0, 364))
        
        blood_type = random.choice(self.blood_types)
        
        # Contact information
        phone_number = self.faker_utils.phone_number()
        email = self.faker_utils.email(f"{first_name} {last_name}")
        address = self.faker_utils.address()
        city = self.faker_utils.city()
        state = self.faker_utils.state()
        country = self.faker_utils.country()
        postal_code = self.faker_utils.postal_code()
        
        # Emergency contact
        emergency_contact_name = self.faker_utils.name()
        emergency_contact_phone = self.faker_utils.phone_number()
        
        # Healthcare provider info
        primary_physician_id = f"PHY-{random.randint(1000, 9999)}"
        
        # Insurance
        insurance_provider = random.choice(self.insurance_providers)
        insurance_policy_number = f"{random.choice(['POL', 'INS', 'MED'])}-{random.randint(10000000, 99999999)}"
        
        # Medical conditions
        allergies = random.choice(self.common_allergies)
        if allergies is None and random.random() < 0.3:  # 30% chance of multiple allergies
            num_allergies = random.randint(2, 4)
            allergy_list = random.sample([a for a in self.common_allergies if a is not None], num_allergies)
            allergies = '; '.join(allergy_list)
        
        chronic_conditions = random.choice(self.chronic_conditions)
        if chronic_conditions is None and random.random() < 0.2:  # 20% chance of multiple conditions
            num_conditions = random.randint(2, 3)
            condition_list = random.sample([c for c in self.chronic_conditions if c is not None], num_conditions)
            chronic_conditions = '; '.join(condition_list)
        
        # Registration and status
        date_registered = self.faker_utils.date_between(
            datetime.now() - timedelta(days=3650),  # Up to 10 years ago
            datetime.now()
        )
        
        # Status - older patients more likely to be inactive/deceased
        if age > 80:
            status = random.choices(self.statuses, weights=[0.7, 0.25, 0.05])[0]
        elif age > 65:
            status = random.choices(self.statuses, weights=[0.85, 0.14, 0.01])[0]
        else:
            status = random.choices(self.statuses, weights=[0.95, 0.05, 0.0])[0]
        
        return {
            'patient_id': patient_id,
            'first_name': first_name,
            'last_name': last_name,
            'date_of_birth': date_of_birth.strftime('%Y-%m-%d'),
            'gender': gender,
            'blood_type': blood_type,
            'phone_number': phone_number,
            'email': email,
            'address': address,
            'city': city,
            'state': state,
            'country': country,
            'postal_code': postal_code,
            'emergency_contact_name': emergency_contact_name,
            'emergency_contact_phone': emergency_contact_phone,
            'primary_physician_id': primary_physician_id,
            'insurance_provider': insurance_provider,
            'insurance_policy_number': insurance_policy_number,
            'allergies': allergies,
            'chronic_conditions': chronic_conditions,
            'date_registered': date_registered.strftime('%Y-%m-%d %H:%M:%S'),
            'status': status
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'patient_id': 'string', 'first_name': 'string', 'last_name': 'string',
            'date_of_birth': 'date', 'gender': 'string', 'blood_type': 'string',
            'phone_number': 'string', 'email': 'string', 'address': 'string',
            'city': 'string', 'state': 'string', 'country': 'string',
            'postal_code': 'string', 'emergency_contact_name': 'string',
            'emergency_contact_phone': 'string', 'primary_physician_id': 'string',
            'insurance_provider': 'string', 'insurance_policy_number': 'string',
            'allergies': 'string', 'chronic_conditions': 'string',
            'date_registered': 'datetime', 'status': 'string'
        }
