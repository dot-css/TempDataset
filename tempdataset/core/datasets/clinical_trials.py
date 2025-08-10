"""
Clinical trials dataset generator.

Generates realistic clinical trial records.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class ClinicalTrialsDataset(BaseDataset):
    """Clinical trials dataset generator for research studies."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._trial_counter = 1
    
    def _init_data_lists(self) -> None:
        self.trial_phases = ['Phase I', 'Phase II', 'Phase III', 'Phase IV']
        self.trial_statuses = ['Recruiting', 'Active', 'Completed', 'Terminated', 'Suspended']
        
        # Medical conditions commonly studied in clinical trials
        self.conditions_studied = [
            'Cancer', 'Alzheimer\'s Disease', 'Diabetes', 'Cardiovascular Disease',
            'Depression', 'Rheumatoid Arthritis', 'Multiple Sclerosis', 'Parkinson\'s Disease',
            'Asthma', 'COPD', 'Hypertension', 'Obesity', 'Chronic Pain', 'HIV/AIDS',
            'Hepatitis C', 'Kidney Disease', 'Osteoporosis', 'Psoriasis', 'Migraine',
            'Sleep Disorders', 'Anxiety Disorders', 'Bipolar Disorder', 'Schizophrenia',
            'Inflammatory Bowel Disease', 'Lupus', 'Fibromyalgia'
        ]
        
        # Pharmaceutical companies and research institutions
        self.sponsors = [
            'Pfizer Inc.', 'Johnson & Johnson', 'Roche', 'Novartis', 'Merck & Co.',
            'GlaxoSmithKline', 'AstraZeneca', 'Eli Lilly', 'Bristol-Myers Squibb', 'AbbVie',
            'Amgen', 'Gilead Sciences', 'Biogen', 'Regeneron', 'Vertex Pharmaceuticals',
            'National Institute of Health', 'National Cancer Institute', 'Mayo Clinic',
            'Johns Hopkins University', 'Stanford University', 'Harvard Medical School',
            'MD Anderson Cancer Center', 'Cleveland Clinic', 'Massachusetts General Hospital'
        ]
        
        # Study locations
        self.study_locations = [
            'Boston, MA', 'New York, NY', 'Philadelphia, PA', 'Baltimore, MD',
            'Atlanta, GA', 'Miami, FL', 'Nashville, TN', 'Chicago, IL', 'Detroit, MI',
            'Minneapolis, MN', 'Houston, TX', 'Dallas, TX', 'Phoenix, AZ', 'Denver, CO',
            'Los Angeles, CA', 'San Francisco, CA', 'San Diego, CA', 'Seattle, WA',
            'Portland, OR', 'Rochester, NY', 'Cleveland, OH', 'Pittsburgh, PA'
        ]
        
        # Trial name templates
        self.trial_name_templates = [
            'Efficacy of {drug} in {condition}',
            'Safety and Efficacy Study of {drug} for {condition}',
            'Randomized Trial of {drug} vs Placebo in {condition}',
            'Long-term Safety Study of {drug}',
            'Dose-Finding Study of {drug} in {condition}',
            'Combination Therapy with {drug} for {condition}',
            'Biomarker Study in {condition} Patients',
            'Quality of Life Study in {condition}',
            'Prevention Trial for {condition}',
            'Extended Follow-up Study of {drug}'
        ]
        
        # Drug names (fictional)
        self.drug_names = [
            'Therapeutix-1', 'MediCure-250', 'BioHeal-X', 'PharmaSol-III',
            'TreatWell-500', 'HealFast-A', 'CurePath-B', 'MediGen-Z',
            'BioFix-Plus', 'TherapyMax-7', 'HealthBoost-Q', 'MediAdvance-12'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic trial info
        trial_id = f"CTR-2025-{self._trial_counter:06d}"
        self._trial_counter += 1
        
        # Select condition and generate trial name
        condition_studied = random.choice(self.conditions_studied)
        drug_name = random.choice(self.drug_names)
        
        trial_name_template = random.choice(self.trial_name_templates)
        if '{drug}' in trial_name_template and '{condition}' in trial_name_template:
            trial_name = trial_name_template.format(drug=drug_name, condition=condition_studied)
        elif '{drug}' in trial_name_template:
            trial_name = trial_name_template.format(drug=drug_name)
        elif '{condition}' in trial_name_template:
            trial_name = trial_name_template.format(condition=condition_studied)
        else:
            trial_name = trial_name_template
        
        # Sponsor
        sponsor = random.choice(self.sponsors)
        
        # Trial dates
        # Trials can start from 5 years ago to 2 years in the future
        start_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1825),  # 5 years ago
            datetime.now() + timedelta(days=730)    # 2 years in future
        )
        
        # Phase and status
        phase = random.choice(self.trial_phases)
        status = random.choice(self.trial_statuses)
        
        # End date based on phase and status
        if status in ['Completed', 'Terminated']:
            # Completed/terminated trials have end dates
            if phase == 'Phase I':
                duration_months = random.randint(6, 18)
            elif phase == 'Phase II':
                duration_months = random.randint(12, 36)
            elif phase == 'Phase III':
                duration_months = random.randint(24, 60)
            else:  # Phase IV
                duration_months = random.randint(12, 48)
            
            end_date = start_date + timedelta(days=duration_months * 30)
        elif status in ['Recruiting', 'Active']:
            # Some ongoing trials have planned end dates
            if random.random() < 0.7:  # 70% have planned end dates
                if phase == 'Phase I':
                    duration_months = random.randint(6, 18)
                elif phase == 'Phase II':
                    duration_months = random.randint(12, 36)
                elif phase == 'Phase III':
                    duration_months = random.randint(24, 60)
                else:  # Phase IV
                    duration_months = random.randint(12, 48)
                
                end_date = start_date + timedelta(days=duration_months * 30)
            else:
                end_date = None
        else:  # Suspended
            end_date = None
        
        # Number of participants based on phase
        if phase == 'Phase I':
            number_of_participants = random.randint(20, 100)
        elif phase == 'Phase II':
            number_of_participants = random.randint(100, 300)
        elif phase == 'Phase III':
            number_of_participants = random.randint(300, 3000)
        else:  # Phase IV
            number_of_participants = random.randint(500, 5000)
        
        # Principal investigator
        principal_investigator_id = f"PI-{random.randint(10000, 99999)}"
        
        # Study location
        study_location = random.choice(self.study_locations)
        
        # Protocol summary
        protocol_templates = [
            'This is a randomized, double-blind, placebo-controlled study evaluating the efficacy and safety of {drug} in patients with {condition}.',
            'A multicenter, open-label study to assess the long-term safety of {drug} in {condition} patients.',
            'Phase {phase} dose-escalation study to determine the maximum tolerated dose of {drug} in {condition}.',
            'Randomized controlled trial comparing {drug} to standard of care in patients with {condition}.',
            'Biomarker-driven study evaluating {drug} in patients with {condition} and specific genetic markers.',
            'Quality of life assessment in {condition} patients receiving {drug} therapy.',
            'Prevention study evaluating {drug} in high-risk individuals for {condition} development.'
        ]
        
        protocol_template = random.choice(protocol_templates)
        protocol_summary = protocol_template.format(
            drug=drug_name, 
            condition=condition_studied.lower(),
            phase=phase
        )
        
        # Results summary (only for completed trials)
        if status == 'Completed':
            results_templates = [
                'Primary endpoint was met with statistical significance (p<0.05).',
                'Study met its primary efficacy endpoint with acceptable safety profile.',
                'Treatment showed significant improvement compared to placebo.',
                'No significant difference between treatment groups was observed.',
                'Study was positive for primary endpoint but showed safety concerns.',
                'Biomarker analysis revealed subset of patients with enhanced response.'
            ]
            results_summary = random.choice(results_templates)
        else:
            results_summary = None
        
        # Publication link (only for completed trials with results)
        if status == 'Completed' and results_summary and random.random() < 0.6:
            journal_names = ['NEJM', 'Lancet', 'JAMA', 'Nature Medicine', 'Science Translational Medicine']
            journal = random.choice(journal_names)
            publication_link = f"https://doi.org/10.{random.randint(1000, 9999)}/{journal.lower().replace(' ', '-')}.{random.randint(2020, 2025)}.{random.randint(100000, 999999)}"
        else:
            publication_link = None
        
        return {
            'trial_id': trial_id,
            'trial_name': trial_name,
            'sponsor': sponsor,
            'start_date': start_date.strftime('%Y-%m-%d'),
            'end_date': end_date.strftime('%Y-%m-%d') if end_date else None,
            'phase': phase,
            'status': status,
            'condition_studied': condition_studied,
            'number_of_participants': number_of_participants,
            'principal_investigator_id': principal_investigator_id,
            'study_location': study_location,
            'protocol_summary': protocol_summary,
            'results_summary': results_summary,
            'publication_link': publication_link
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'trial_id': 'string', 'trial_name': 'string', 'sponsor': 'string',
            'start_date': 'date', 'end_date': 'date', 'phase': 'string',
            'status': 'string', 'condition_studied': 'string', 'number_of_participants': 'integer',
            'principal_investigator_id': 'string', 'study_location': 'string',
            'protocol_summary': 'string', 'results_summary': 'string', 'publication_link': 'string'
        }
