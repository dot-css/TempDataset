"""
Prescriptions dataset generator.

Generates realistic prescription records for medications.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class PrescriptionsDataset(BaseDataset):
    """Prescriptions dataset generator for medication records."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._prescription_counter = 1
    
    def _init_data_lists(self) -> None:
        # Common medications with their typical dosages and routes
        self.medications = {
            'Lisinopril': {
                'code': 'ACE001',
                'dosages': ['5 mg', '10 mg', '20 mg', '40 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily', 'Twice daily'],
                'typical_quantity': [30, 90],
                'refills': [3, 6, 11]
            },
            'Metformin': {
                'code': 'DIAB001',
                'dosages': ['500 mg', '850 mg', '1000 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily', 'Twice daily', 'Three times daily'],
                'typical_quantity': [60, 90, 180],
                'refills': [5, 11]
            },
            'Atorvastatin': {
                'code': 'STAT001',
                'dosages': ['10 mg', '20 mg', '40 mg', '80 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily'],
                'typical_quantity': [30, 90],
                'refills': [5, 11]
            },
            'Amlodipine': {
                'code': 'CCB001',
                'dosages': ['2.5 mg', '5 mg', '10 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily'],
                'typical_quantity': [30, 90],
                'refills': [5, 11]
            },
            'Omeprazole': {
                'code': 'PPI001',
                'dosages': ['20 mg', '40 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily', 'Twice daily'],
                'typical_quantity': [30, 90],
                'refills': [3, 5, 11]
            },
            'Albuterol': {
                'code': 'BRONC001',
                'dosages': ['90 mcg/actuation', '108 mcg/actuation'],
                'route': 'Inhalation',
                'frequencies': ['As needed', 'Every 4-6 hours as needed'],
                'typical_quantity': [1, 2, 3],
                'refills': [5, 11]
            },
            'Sertraline': {
                'code': 'SSRI001',
                'dosages': ['25 mg', '50 mg', '100 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily'],
                'typical_quantity': [30, 90],
                'refills': [5, 11]
            },
            'Ibuprofen': {
                'code': 'NSAID001',
                'dosages': ['200 mg', '400 mg', '600 mg', '800 mg'],
                'route': 'Oral',
                'frequencies': ['Every 6-8 hours as needed', 'Three times daily', 'Four times daily'],
                'typical_quantity': [30, 60, 90],
                'refills': [0, 1, 2, 3]
            },
            'Warfarin': {
                'code': 'ANTIC001',
                'dosages': ['1 mg', '2 mg', '2.5 mg', '5 mg', '7.5 mg', '10 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily'],
                'typical_quantity': [30, 90],
                'refills': [2, 5]
            },
            'Hydrochlorothiazide': {
                'code': 'DIUR001',
                'dosages': ['12.5 mg', '25 mg', '50 mg'],
                'route': 'Oral',
                'frequencies': ['Once daily'],
                'typical_quantity': [30, 90],
                'refills': [5, 11]
            },
            'Insulin Glargine': {
                'code': 'INSUL001',
                'dosages': ['100 units/mL'],
                'route': 'Injection',
                'frequencies': ['Once daily', 'Twice daily'],
                'typical_quantity': [1, 3],  # Number of pens/vials
                'refills': [2, 5]
            },
            'Gabapentin': {
                'code': 'ANTIC002',
                'dosages': ['100 mg', '300 mg', '400 mg', '600 mg', '800 mg'],
                'route': 'Oral',
                'frequencies': ['Twice daily', 'Three times daily'],
                'typical_quantity': [60, 90, 180],
                'refills': [2, 5]
            }
        }
        
        self.prescription_statuses = ['Active', 'Completed', 'Discontinued']
        
        self.pharmacy_names = [
            'CVS Pharmacy', 'Walgreens', 'Rite Aid', 'Walmart Pharmacy',
            'Target Pharmacy', 'Kroger Pharmacy', 'Safeway Pharmacy',
            'Costco Pharmacy', 'Kaiser Permanente Pharmacy', 'Express Scripts',
            'Local Community Pharmacy', 'Hospital Pharmacy'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic prescription info
        prescription_id = f"RX-2025-{self._prescription_counter:06d}"
        self._prescription_counter += 1
        
        patient_id = f"PAT-2025-{random.randint(1, 999999):06d}"
        physician_id = f"PHY-{random.randint(1000, 9999)}"
        
        # Select medication
        medication_name = random.choice(list(self.medications.keys()))
        med_info = self.medications[medication_name]
        
        medication_code = med_info['code']
        dosage = random.choice(med_info['dosages'])
        frequency = random.choice(med_info['frequencies'])
        route = med_info['route']
        quantity_prescribed = random.choice(med_info['typical_quantity'])
        refills_allowed = random.choice(med_info['refills'])
        
        # Prescription dates
        start_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=180),
            datetime.now()
        )
        
        # End date based on medication type and quantity
        if frequency == 'Once daily':
            days_supply = quantity_prescribed
        elif frequency == 'Twice daily':
            days_supply = quantity_prescribed // 2
        elif frequency == 'Three times daily':
            days_supply = quantity_prescribed // 3
        elif frequency == 'Four times daily':
            days_supply = quantity_prescribed // 4
        elif 'as needed' in frequency.lower():
            # PRN medications last longer
            days_supply = quantity_prescribed * 2
        else:
            days_supply = 30  # Default 30 days
        
        # Some prescriptions are long-term (no end date)
        if random.random() < 0.3:  # 30% are ongoing
            end_date = None
        else:
            end_date = start_date + timedelta(days=days_supply)
        
        # Pharmacy information
        pharmacy_name = random.choice(self.pharmacy_names)
        if 'CVS' in pharmacy_name:
            pharmacy_contact = f"(555) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
        elif 'Walgreens' in pharmacy_name:
            pharmacy_contact = f"(800) {random.randint(100, 999)}-{random.randint(1000, 9999)}"
        else:
            pharmacy_contact = self.faker_utils.phone_number()
        
        # Prescription status
        if end_date and end_date < datetime.now().date():
            status = random.choices(
                self.prescription_statuses,
                weights=[0.1, 0.8, 0.1]  # Most completed prescriptions are actually completed
            )[0]
        elif end_date is None or end_date >= datetime.now().date():
            status = random.choices(
                self.prescription_statuses,
                weights=[0.9, 0.05, 0.05]  # Most current prescriptions are active
            )[0]
        else:
            status = 'Active'
        
        # Notes (optional)
        notes_options = [
            'Take with food', 'Take on empty stomach', 'Do not crush or chew',
            'May cause drowsiness', 'Avoid alcohol', 'Monitor blood pressure',
            'Check blood glucose regularly', 'Take at bedtime', 'Generic substitution allowed',
            None
        ]
        notes = random.choice(notes_options) if random.random() < 0.4 else None
        
        return {
            'prescription_id': prescription_id,
            'patient_id': patient_id,
            'physician_id': physician_id,
            'medication_name': medication_name,
            'medication_code': medication_code,
            'dosage': dosage,
            'frequency': frequency,
            'route': route,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'quantity_prescribed': quantity_prescribed,
            'refills_allowed': refills_allowed,
            'pharmacy_name': pharmacy_name,
            'pharmacy_contact': pharmacy_contact,
            'status': status,
            'notes': notes
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'prescription_id': 'string', 'patient_id': 'string', 'physician_id': 'string',
            'medication_name': 'string', 'medication_code': 'string', 'dosage': 'string',
            'frequency': 'string', 'route': 'string', 'start_date': 'date',
            'end_date': 'date', 'quantity_prescribed': 'integer', 'refills_allowed': 'integer',
            'pharmacy_name': 'string', 'pharmacy_contact': 'string', 'status': 'string',
            'notes': 'string'
        }
