"""
Appointments dataset generator.

Generates realistic medical appointment records.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class AppointmentsDataset(BaseDataset):
    """Appointments dataset generator for medical scheduling."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._appointment_counter = 1
    
    def _init_data_lists(self) -> None:
        self.departments = [
            'Cardiology', 'Neurology', 'Orthopedics', 'Dermatology',
            'Pediatrics', 'Internal Medicine', 'Gynecology', 'Oncology',
            'Psychiatry', 'Radiology', 'Emergency Medicine', 'Family Medicine',
            'Gastroenterology', 'Endocrinology', 'Pulmonology', 'Urology',
            'Ophthalmology', 'ENT', 'Rheumatology', 'Nephrology'
        ]
        
        self.appointment_types = ['In-person', 'Telehealth']
        
        self.appointment_statuses = ['Scheduled', 'Completed', 'Canceled', 'No-Show']
        
        self.visit_reasons = {
            'Cardiology': [
                'Chest pain evaluation', 'Hypertension management', 'Heart murmur assessment',
                'Coronary artery disease follow-up', 'Arrhythmia monitoring', 'Preventive cardiology'
            ],
            'Neurology': [
                'Headache evaluation', 'Seizure management', 'Memory concerns',
                'Tremor assessment', 'Stroke follow-up', 'Neuropathy evaluation'
            ],
            'Orthopedics': [
                'Joint pain assessment', 'Sports injury', 'Back pain evaluation',
                'Fracture follow-up', 'Arthritis management', 'Post-surgical care'
            ],
            'Dermatology': [
                'Skin lesion examination', 'Acne treatment', 'Rash evaluation',
                'Mole check', 'Psoriasis management', 'Skin cancer screening'
            ],
            'Pediatrics': [
                'Well-child visit', 'Vaccination', 'Growth assessment',
                'Developmental concerns', 'Acute illness', 'School physical'
            ],
            'Internal Medicine': [
                'Annual physical', 'Diabetes management', 'Preventive care',
                'Chronic disease management', 'Health maintenance', 'Medication review'
            ]
        }
        
        # Default reasons for departments not specifically listed
        self.default_visit_reasons = [
            'Follow-up appointment', 'Initial consultation', 'Routine check-up',
            'Symptom evaluation', 'Treatment planning', 'Progress assessment',
            'Medication adjustment', 'Specialist referral', 'Second opinion',
            'Preventive care'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic appointment info
        appointment_id = f"APP-2025-{self._appointment_counter:06d}"
        self._appointment_counter += 1
        
        patient_id = f"PAT-2025-{random.randint(1, 999999):06d}"
        physician_id = f"PHY-{random.randint(1000, 9999)}"
        department = random.choice(self.departments)
        
        # Appointment timing
        # Generate appointments from 3 months ago to 3 months in the future
        appointment_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=90),
            datetime.now() + timedelta(days=90)
        )
        
        # Add realistic appointment times (business hours)
        hour = random.choice(range(8, 18))  # 8 AM to 5 PM
        minute = random.choice([0, 15, 30, 45])  # 15-minute intervals
        appointment_datetime = datetime.combine(appointment_date, datetime.min.time()).replace(hour=hour, minute=minute, second=0)
        
        # Booking date - typically 1-30 days before appointment
        days_before_booking = random.randint(1, 30)
        booking_date = appointment_datetime - timedelta(days=days_before_booking)
        
        # Appointment details
        appointment_type = random.choice(self.appointment_types)
        
        # Choose reason based on department
        if department in self.visit_reasons:
            reason_for_visit = random.choice(self.visit_reasons[department])
        else:
            reason_for_visit = random.choice(self.default_visit_reasons)
        
        # Status based on appointment date
        if appointment_datetime > datetime.now():
            status = 'Scheduled'
            check_in_time = None
            check_out_time = None
        else:
            # Past appointments have various statuses
            status = random.choices(
                self.appointment_statuses,
                weights=[0.05, 0.80, 0.10, 0.05]  # Scheduled, Completed, Canceled, No-Show
            )[0]
            
            if status == 'Completed':
                # Generate realistic check-in/check-out times
                check_in_delay = random.randint(-5, 20)  # Can be early or late
                check_in_time = appointment_datetime + timedelta(minutes=check_in_delay)
                
                # Appointment duration typically 15-60 minutes
                duration = random.randint(15, 60)
                check_out_time = check_in_time + timedelta(minutes=duration)
            elif status == 'No-Show':
                check_in_time = None
                check_out_time = None
            else:  # Canceled or Scheduled (rare for past dates)
                check_in_time = None
                check_out_time = None
        
        # Follow-up requirements
        follow_up_required = random.choice([True, False])
        if follow_up_required and status == 'Completed':
            # Follow-up typically scheduled 1-12 weeks later
            follow_up_weeks = random.randint(1, 12)
            follow_up_date = appointment_datetime + timedelta(weeks=follow_up_weeks)
        else:
            follow_up_date = None
        
        # Notes (optional)
        notes_options = [
            'Patient arrived on time',
            'Patient reported improvement in symptoms',
            'Medication adjustment needed',
            'Referred to specialist',
            'Lab work ordered',
            'Follow-up imaging scheduled',
            'Patient education provided',
            'Insurance verification completed',
            None  # No notes
        ]
        notes = random.choice(notes_options)
        
        return {
            'appointment_id': appointment_id,
            'patient_id': patient_id,
            'physician_id': physician_id,
            'department': department,
            'appointment_date': appointment_datetime.strftime('%Y-%m-%d %H:%M:%S'),
            'booking_date': booking_date.strftime('%Y-%m-%d %H:%M:%S'),
            'appointment_type': appointment_type,
            'reason_for_visit': reason_for_visit,
            'status': status,
            'check_in_time': check_in_time.strftime('%Y-%m-%d %H:%M:%S') if check_in_time else None,
            'check_out_time': check_out_time.strftime('%Y-%m-%d %H:%M:%S') if check_out_time else None,
            'notes': notes,
            'follow_up_required': follow_up_required,
            'follow_up_date': follow_up_date.strftime('%Y-%m-%d %H:%M:%S') if follow_up_date else None
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'appointment_id': 'string', 'patient_id': 'string', 'physician_id': 'string',
            'department': 'string', 'appointment_date': 'datetime', 'booking_date': 'datetime',
            'appointment_type': 'string', 'reason_for_visit': 'string', 'status': 'string',
            'check_in_time': 'datetime', 'check_out_time': 'datetime', 'notes': 'string',
            'follow_up_required': 'boolean', 'follow_up_date': 'datetime'
        }
