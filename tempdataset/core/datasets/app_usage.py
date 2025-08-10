"""
App usage dataset generator.

Generates realistic mobile/web application usage data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class AppUsageDataset(BaseDataset):
    """App usage dataset generator for application analytics."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._usage_counter = 1
    
    def _init_data_lists(self) -> None:
        self.app_versions = ['1.0.0', '1.1.0', '1.2.0', '1.2.1', '2.0.0', '2.0.1', '2.1.0']
        
        self.device_models = {
            'iOS': [
                'iPhone 14 Pro', 'iPhone 14', 'iPhone 13 Pro', 'iPhone 13',
                'iPhone 12', 'iPhone SE', 'iPad Pro', 'iPad Air', 'iPad'
            ],
            'Android': [
                'Samsung Galaxy S23', 'Samsung Galaxy S22', 'Google Pixel 7',
                'OnePlus 11', 'Xiaomi 13', 'Samsung Galaxy A54', 'Huawei P50'
            ]
        }
        
        self.device_os_versions = {
            'iOS': ['16.0', '16.1', '16.2', '15.7', '15.6', '14.8'],
            'Android': ['13', '12', '11', '10', '9']
        }
        
        self.network_types = ['WiFi', '4G', '5G', '3G', 'Edge']
        
        self.app_features = [
            'Login', 'Profile', 'Settings', 'Search', 'Notifications',
            'Chat', 'Camera', 'Gallery', 'Maps', 'Payment', 'Share',
            'Favorites', 'History', 'Help', 'Feedback', 'Dark Mode'
        ]
        
        self.countries = [
            'United States', 'India', 'China', 'Brazil', 'Japan',
            'Germany', 'United Kingdom', 'France', 'Canada', 'Australia'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic usage info
        usage_id = f"APPUSE-2025-{self._usage_counter:06d}"
        self._usage_counter += 1
        
        user_id = f"USER-{random.randint(100000, 999999)}"
        app_version = random.choice(self.app_versions)
        
        # Device info
        device_os = random.choice(['iOS', 'Android'])
        device_model = random.choice(self.device_models[device_os])
        device_os_version = f"{device_os} {random.choice(self.device_os_versions[device_os])}"
        
        # Session info
        session_id = f"SESS-{random.randint(100000, 999999)}"
        
        # Session timing
        session_start_time = self.faker_utils.date_between(
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
        session_start_time = datetime.combine(
            session_start_time,
            datetime.min.time().replace(
                hour=random.randint(6, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Session duration based on usage patterns
        session_duration_minutes = random.choices(
            [1, 5, 15, 30, 60, 120],  # Common session lengths
            weights=[0.3, 0.25, 0.2, 0.15, 0.07, 0.03]
        )[0]
        
        session_end_time = session_start_time + timedelta(minutes=session_duration_minutes)
        screen_time_seconds = session_duration_minutes * 60
        
        # Features used
        num_features = random.randint(1, 8)
        features_used = random.sample(self.app_features, num_features)
        features_used_str = ', '.join(features_used)
        
        # Events and interactions
        events_triggered = random.randint(5, 100)
        
        # Network type
        network_type = random.choices(
            self.network_types,
            weights=[0.6, 0.25, 0.10, 0.04, 0.01]  # WiFi most common
        )[0]
        
        # App stability
        crashes_occurred = random.choices([0, 1, 2], weights=[0.95, 0.04, 0.01])[0]
        
        # In-app purchases
        purchase_probability = 0.05  # 5% of sessions have purchases
        if random.random() < purchase_probability:
            in_app_purchases = round(random.uniform(0.99, 49.99), 2)
        else:
            in_app_purchases = 0.0
        
        # Location
        location_country = random.choice(self.countries)
        
        return {
            'usage_id': usage_id,
            'user_id': user_id,
            'app_version': app_version,
            'device_model': device_model,
            'device_os': device_os_version,
            'session_id': session_id,
            'session_start_time': session_start_time.strftime('%Y-%m-%d %H:%M:%S'),
            'session_end_time': session_end_time.strftime('%Y-%m-%d %H:%M:%S'),
            'features_used': features_used_str,
            'events_triggered': events_triggered,
            'screen_time_seconds': screen_time_seconds,
            'network_type': network_type,
            'crashes_occurred': crashes_occurred,
            'in_app_purchases': in_app_purchases,
            'location_country': location_country
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'usage_id': 'string', 'user_id': 'string', 'app_version': 'string',
            'device_model': 'string', 'device_os': 'string', 'session_id': 'string',
            'session_start_time': 'datetime', 'session_end_time': 'datetime',
            'features_used': 'string', 'events_triggered': 'integer',
            'screen_time_seconds': 'integer', 'network_type': 'string',
            'crashes_occurred': 'integer', 'in_app_purchases': 'float',
            'location_country': 'string'
        }
