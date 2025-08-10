"""
Lab results dataset generator.

Generates realistic laboratory test results.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any, Tuple

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class LabResultsDataset(BaseDataset):
    """Lab results dataset generator for medical testing."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._lab_counter = 1
    
    def _init_data_lists(self) -> None:
        # Common lab tests with their codes, units, and reference ranges
        self.lab_tests = {
            'CBC': {
                'code': 'CBC001',
                'tests': [
                    ('White Blood Cell Count', 'WBC', 'cells/μL', (4500, 11000)),
                    ('Red Blood Cell Count', 'RBC', 'cells/μL', (4200000, 5400000)),
                    ('Hemoglobin', 'HGB', 'g/dL', (12.0, 16.0)),
                    ('Hematocrit', 'HCT', '%', (36, 46)),
                    ('Platelet Count', 'PLT', 'cells/μL', (150000, 450000))
                ]
            },
            'Lipid Panel': {
                'code': 'LIPID001',
                'tests': [
                    ('Total Cholesterol', 'CHOL', 'mg/dL', (125, 200)),
                    ('HDL Cholesterol', 'HDL', 'mg/dL', (40, 60)),
                    ('LDL Cholesterol', 'LDL', 'mg/dL', (70, 130)),
                    ('Triglycerides', 'TRIG', 'mg/dL', (35, 150))
                ]
            },
            'Basic Metabolic Panel': {
                'code': 'BMP001',
                'tests': [
                    ('Glucose', 'GLU', 'mg/dL', (70, 100)),
                    ('Sodium', 'NA', 'mEq/L', (136, 145)),
                    ('Potassium', 'K', 'mEq/L', (3.5, 5.1)),
                    ('Chloride', 'CL', 'mEq/L', (98, 107)),
                    ('BUN', 'BUN', 'mg/dL', (7, 20)),
                    ('Creatinine', 'CREAT', 'mg/dL', (0.6, 1.3))
                ]
            },
            'Liver Function Tests': {
                'code': 'LFT001',
                'tests': [
                    ('ALT', 'ALT', 'U/L', (7, 40)),
                    ('AST', 'AST', 'U/L', (10, 40)),
                    ('Bilirubin Total', 'TBIL', 'mg/dL', (0.3, 1.2)),
                    ('Alkaline Phosphatase', 'ALP', 'U/L', (44, 147))
                ]
            },
            'Thyroid Function': {
                'code': 'THYROID001',
                'tests': [
                    ('TSH', 'TSH', 'mIU/L', (0.4, 4.0)),
                    ('T4 Free', 'T4F', 'ng/dL', (0.8, 1.8)),
                    ('T3 Total', 'T3T', 'ng/dL', (80, 200))
                ]
            },
            'Urinalysis': {
                'code': 'UA001',
                'tests': [
                    ('Specific Gravity', 'SPGR', '', (1.003, 1.030)),
                    ('Protein', 'PROT', 'mg/dL', (0, 20)),
                    ('Glucose', 'UGLU', 'mg/dL', (0, 15)),
                    ('Ketones', 'KET', 'mg/dL', (0, 5))
                ]
            }
        }
        
        self.flags = ['Normal', 'High', 'Low', 'Critical']
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic lab result info
        lab_result_id = f"LAB-2025-{self._lab_counter:06d}"
        self._lab_counter += 1
        
        patient_id = f"PAT-2025-{random.randint(1, 999999):06d}"
        ordering_physician_id = f"PHY-{random.randint(1000, 9999)}"
        lab_technician_id = f"TECH-{random.randint(100, 999)}"
        
        # Select random test panel
        test_panel = random.choice(list(self.lab_tests.keys()))
        panel_info = self.lab_tests[test_panel]
        
        # Select specific test from the panel
        test_info = random.choice(panel_info['tests'])
        test_name, test_code, unit, ref_range = test_info
        
        # Generate collection and result dates
        collection_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=30),
            datetime.now()
        )
        
        # Add realistic times
        collection_hour = random.randint(6, 16)  # Collection typically during day
        collection_minute = random.choice([0, 15, 30, 45])
        collection_datetime = datetime.combine(collection_date, datetime.min.time()).replace(
            hour=collection_hour, 
            minute=collection_minute, 
            second=0
        )
        
        # Result date is typically 1-3 days after collection
        result_delay_hours = random.randint(4, 72)  # 4 hours to 3 days
        result_datetime = collection_datetime + timedelta(hours=result_delay_hours)
        
        # Generate test result value based on reference range
        min_ref, max_ref = ref_range
        
        # Determine if result is normal, high, or low
        result_type = random.choices(
            ['normal', 'high', 'low', 'critical'],
            weights=[0.70, 0.15, 0.13, 0.02]  # Most results are normal
        )[0]
        
        if result_type == 'normal':
            result_value = round(random.uniform(min_ref, max_ref), 2)
            flag = 'Normal'
        elif result_type == 'high':
            # High values are 10-50% above normal range
            multiplier = random.uniform(1.1, 1.5)
            result_value = round(max_ref * multiplier, 2)
            flag = 'High'
        elif result_type == 'low':
            # Low values are 10-50% below normal range
            multiplier = random.uniform(0.5, 0.9)
            result_value = round(min_ref * multiplier, 2)
            flag = 'Low'
        else:  # critical
            # Critical values are significantly outside normal range
            if random.choice([True, False]):
                # Critically high
                multiplier = random.uniform(2.0, 4.0)
                result_value = round(max_ref * multiplier, 2)
            else:
                # Critically low
                multiplier = random.uniform(0.1, 0.4)
                result_value = round(min_ref * multiplier, 2)
            flag = 'Critical'
        
        # For certain tests, use integer values
        if test_code in ['WBC', 'RBC', 'PLT']:
            result_value = int(result_value)
        
        # Reference range string
        if isinstance(min_ref, int) and isinstance(max_ref, int):
            reference_range = f"{min_ref}-{max_ref}"
        else:
            reference_range = f"{min_ref:.1f}-{max_ref:.1f}"
        
        # Notes (optional)
        notes_options = [
            'Sample hemolyzed', 'Fasting specimen', 'Non-fasting specimen',
            'Sample collected properly', 'Repeated due to interference',
            'Critical value called to physician', None
        ]
        notes = random.choice(notes_options) if random.random() < 0.3 else None
        
        return {
            'lab_result_id': lab_result_id,
            'patient_id': patient_id,
            'test_name': test_name,
            'test_code': test_code,
            'collection_date': collection_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'result_date': result_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'result_value': str(result_value),  # Store as string to handle both int and float
            'unit': unit,
            'reference_range': reference_range,
            'flag': flag,
            'ordering_physician_id': ordering_physician_id,
            'lab_technician_id': lab_technician_id,
            'notes': notes
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'lab_result_id': 'string', 'patient_id': 'string', 'test_name': 'string',
            'test_code': 'string', 'collection_date': 'datetime', 'result_date': 'datetime',
            'result_value': 'string', 'unit': 'string', 'reference_range': 'string',
            'flag': 'string', 'ordering_physician_id': 'string', 'lab_technician_id': 'string',
            'notes': 'string'
        }
