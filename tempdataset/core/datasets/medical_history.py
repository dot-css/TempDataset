"""
Medical history dataset generator.

Generates realistic patient medical history records.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class MedicalHistoryDataset(BaseDataset):
    """Medical history dataset generator for patient conditions."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._history_counter = 1
    
    def _init_data_lists(self) -> None:
        # Medical conditions with ICD-10 codes and typical treatments
        self.medical_conditions = {
            'Hypertension': {
                'codes': ['I10', 'I11.9', 'I12.9'],
                'treatments': ['Lisinopril therapy', 'Lifestyle modification', 'DASH diet', 'Amlodipine therapy'],
                'chronic_likelihood': 0.9
            },
            'Type 2 Diabetes Mellitus': {
                'codes': ['E11.9', 'E11.65', 'E11.40'],
                'treatments': ['Metformin therapy', 'Insulin therapy', 'Diet modification', 'Glucose monitoring'],
                'chronic_likelihood': 0.95
            },
            'Hyperlipidemia': {
                'codes': ['E78.5', 'E78.0', 'E78.2'],
                'treatments': ['Statin therapy', 'Diet modification', 'Exercise program', 'Atorvastatin therapy'],
                'chronic_likelihood': 0.8
            },
            'Coronary Artery Disease': {
                'codes': ['I25.10', 'I25.9', 'I25.119'],
                'treatments': ['Cardiac catheterization', 'Stent placement', 'Beta-blocker therapy', 'Aspirin therapy'],
                'chronic_likelihood': 0.9
            },
            'Asthma': {
                'codes': ['J45.9', 'J45.909', 'J45.40'],
                'treatments': ['Albuterol inhaler', 'Inhaled corticosteroids', 'Allergy management', 'Bronchodilator therapy'],
                'chronic_likelihood': 0.85
            },
            'Depression': {
                'codes': ['F32.9', 'F33.9', 'F32.2'],
                'treatments': ['SSRI therapy', 'Cognitive behavioral therapy', 'Psychotherapy', 'Sertraline therapy'],
                'chronic_likelihood': 0.7
            },
            'Anxiety Disorder': {
                'codes': ['F41.9', 'F41.1', 'F40.9'],
                'treatments': ['Anxiolytic therapy', 'Cognitive behavioral therapy', 'Relaxation techniques', 'SSRI therapy'],
                'chronic_likelihood': 0.6
            },
            'Osteoarthritis': {
                'codes': ['M19.90', 'M15.9', 'M19.011'],
                'treatments': ['NSAIDs', 'Physical therapy', 'Joint injection', 'Weight management'],
                'chronic_likelihood': 0.95
            },
            'COPD': {
                'codes': ['J44.1', 'J44.0', 'J44.10'],
                'treatments': ['Bronchodilator therapy', 'Inhaled corticosteroids', 'Pulmonary rehabilitation', 'Oxygen therapy'],
                'chronic_likelihood': 0.95
            },
            'Chronic Kidney Disease': {
                'codes': ['N18.9', 'N18.6', 'N18.3'],
                'treatments': ['ACE inhibitor therapy', 'Dietary restriction', 'Phosphate binders', 'Nephrology consultation'],
                'chronic_likelihood': 0.9
            },
            'Atrial Fibrillation': {
                'codes': ['I48.91', 'I48.0', 'I48.1'],
                'treatments': ['Anticoagulation therapy', 'Rate control', 'Cardioversion', 'Ablation therapy'],
                'chronic_likelihood': 0.8
            },
            'Migraine': {
                'codes': ['G43.909', 'G43.919', 'G43.009'],
                'treatments': ['Triptan therapy', 'Preventive medication', 'Lifestyle modification', 'Botox injections'],
                'chronic_likelihood': 0.7
            },
            'Pneumonia': {
                'codes': ['J18.9', 'J15.9', 'J44.0'],
                'treatments': ['Antibiotic therapy', 'Supportive care', 'Hospitalization', 'Respiratory therapy'],
                'chronic_likelihood': 0.1
            },
            'Gastroesophageal Reflux Disease': {
                'codes': ['K21.9', 'K21.0', 'K20.9'],
                'treatments': ['PPI therapy', 'H2 blocker therapy', 'Lifestyle modification', 'Dietary changes'],
                'chronic_likelihood': 0.8
            },
            'Sleep Apnea': {
                'codes': ['G47.33', 'G47.30', 'G47.39'],
                'treatments': ['CPAP therapy', 'Weight loss', 'Sleep study', 'Oral appliance'],
                'chronic_likelihood': 0.9
            }
        }
        
        self.condition_statuses = ['Active', 'Resolved', 'Chronic']
        
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic history record info
        history_id = f"HIS-2025-{self._history_counter:06d}"
        self._history_counter += 1
        
        patient_id = f"PAT-2025-{random.randint(1, 999999):06d}"
        physician_id = f"PHY-{random.randint(1000, 9999)}" if random.random() < 0.8 else None
        
        # Select medical condition
        condition_name = random.choice(list(self.medical_conditions.keys()))
        condition_info = self.medical_conditions[condition_name]
        
        condition_code = random.choice(condition_info['codes']) if random.random() < 0.9 else None
        
        # Diagnosis date - can be anywhere from 10 years ago to now
        diagnosis_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=3650),  # Up to 10 years ago
            datetime.now()
        )
        
        # Determine status based on condition type
        chronic_likelihood = condition_info['chronic_likelihood']
        if random.random() < chronic_likelihood:
            status = 'Chronic'
        else:
            status = random.choices(['Active', 'Resolved'], weights=[0.3, 0.7])[0]
        
        # Treatment information
        treatment_name = random.choice(condition_info['treatments']) if random.random() < 0.8 else None
        
        if treatment_name:
            # Treatment typically starts close to diagnosis date
            treatment_start_delay = random.randint(0, 30)  # 0-30 days after diagnosis
            treatment_start_date = diagnosis_date + timedelta(days=treatment_start_delay)
            
            # Treatment end date
            if status == 'Resolved':
                # Resolved conditions have treatment end dates
                treatment_duration = random.randint(30, 365)  # 1 month to 1 year
                treatment_end_date = treatment_start_date + timedelta(days=treatment_duration)
            elif status == 'Chronic':
                # Chronic conditions may have ongoing treatment
                if random.random() < 0.3:  # 30% have treatment end dates (switched treatments)
                    treatment_duration = random.randint(90, 1095)  # 3 months to 3 years
                    treatment_end_date = treatment_start_date + timedelta(days=treatment_duration)
                else:
                    treatment_end_date = None  # Ongoing treatment
            else:  # Active
                # Active conditions may or may not have treatment end dates
                if random.random() < 0.5:
                    treatment_duration = random.randint(7, 180)  # 1 week to 6 months
                    treatment_end_date = treatment_start_date + timedelta(days=treatment_duration)
                else:
                    treatment_end_date = None
        else:
            treatment_start_date = None
            treatment_end_date = None
        
        # Notes (optional)
        notes_options = [
            'Patient responding well to treatment',
            'Medication dosage adjusted',
            'Requires regular monitoring',
            'Patient non-compliant with medication',
            'Condition well-controlled',
            'Referred to specialist',
            'Family history positive',
            'Patient education provided',
            'Lifestyle modifications recommended',
            None
        ]
        notes = random.choice(notes_options) if random.random() < 0.4 else None
        
        return {
            'history_id': history_id,
            'patient_id': patient_id,
            'condition_name': condition_name,
            'condition_code': condition_code,
            'diagnosis_date': diagnosis_date.strftime('%Y-%m-%d'),
            'status': status,
            'treatment_name': treatment_name,
            'treatment_start_date': treatment_start_date.strftime('%Y-%m-%d') if treatment_start_date else None,
            'treatment_end_date': treatment_end_date.strftime('%Y-%m-%d') if treatment_end_date else None,
            'physician_id': physician_id,
            'notes': notes
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'history_id': 'string', 'patient_id': 'string', 'condition_name': 'string',
            'condition_code': 'string', 'diagnosis_date': 'date', 'status': 'string',
            'treatment_name': 'string', 'treatment_start_date': 'date', 'treatment_end_date': 'date',
            'physician_id': 'string', 'notes': 'string'
        }
