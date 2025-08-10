"""
User sessions dataset generator.

Generates realistic user session tracking data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class UserSessionsDataset(BaseDataset):
    """User sessions dataset generator for user behavior analytics and session tracking."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._session_counter = 1
    
    def _init_data_lists(self) -> None:
        self.devices = ['Desktop', 'Mobile', 'Tablet']
        
        self.operating_systems = [
            'Windows 10', 'Windows 11', 'macOS Monterey', 'macOS Ventura', 'macOS Sonoma',
            'iOS 16', 'iOS 17', 'Android 12', 'Android 13', 'Android 14',
            'Ubuntu 20.04', 'Ubuntu 22.04'
        ]
        
        self.browsers = [
            'Chrome 120', 'Chrome 121', 'Firefox 121', 'Safari 17',
            'Edge 120', 'Opera 106', 'Mobile Safari', 'Chrome Mobile'
        ]
        
        self.countries = [
            'United States', 'United Kingdom', 'Canada', 'Germany', 'France',
            'Japan', 'Australia', 'India', 'Brazil', 'Spain', 'Italy', 'Netherlands'
        ]
        
        self.cities = {
            'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Liverpool', 'Bristol'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'Germany': ['Berlin', 'Munich', 'Hamburg', 'Frankfurt', 'Cologne'],
            'France': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice'],
            'Japan': ['Tokyo', 'Osaka', 'Yokohama', 'Nagoya', 'Sapporo'],
            'Australia': ['Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide'],
            'India': ['Mumbai', 'Delhi', 'Bangalore', 'Chennai', 'Kolkata'],
            'Brazil': ['São Paulo', 'Rio de Janeiro', 'Brasília', 'Salvador', 'Fortaleza'],
            'Spain': ['Madrid', 'Barcelona', 'Valencia', 'Seville', 'Zaragoza'],
            'Italy': ['Rome', 'Milan', 'Naples', 'Turin', 'Florence'],
            'Netherlands': ['Amsterdam', 'Rotterdam', 'The Hague', 'Utrecht', 'Eindhoven']
        }
        
        self.traffic_sources = [
            'Direct', 'Google Search', 'Bing Search', 'Social Media', 'Email Campaign',
            'Referral', 'Paid Ads', 'Newsletter', 'YouTube', 'LinkedIn'
        ]
        
        self.utm_campaigns = [
            'summer_sale_2024', 'new_user_welcome', 'holiday_promotion',
            'product_launch', 'retargeting_campaign', 'brand_awareness',
            'seasonal_offer', 'loyalty_program', None
        ]
        
        self.session_outcomes = [
            'conversion', 'bounce', 'engaged_browsing', 'abandoned_cart',
            'newsletter_signup', 'account_creation', 'support_contact'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic session info
        session_id = f"SESS-2025-{self._session_counter:08d}"
        self._session_counter += 1
        
        # User ID - some sessions are anonymous
        user_id = f"USER-{random.randint(10000, 99999)}" if random.random() < 0.7 else None
        is_authenticated = user_id is not None
        
        # Session timing
        session_start = self.faker_utils.date_between(
            datetime.now() - timedelta(days=30),
            datetime.now()
        )
        session_start = datetime.combine(
            session_start,
            datetime.min.time().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Session duration (in minutes) - varies by outcome
        if random.random() < 0.15:  # Bounce sessions
            duration_minutes = random.randint(1, 3)
            outcome = 'bounce'
        elif random.random() < 0.1:  # Conversion sessions
            duration_minutes = random.randint(15, 120)
            outcome = 'conversion'
        else:  # Regular sessions
            duration_minutes = random.randint(3, 60)
            outcome = random.choice(self.session_outcomes[2:])  # Excluding conversion and bounce
        
        session_end = session_start + timedelta(minutes=duration_minutes)
        
        # Device and browser info
        device_type = random.choices(
            self.devices,
            weights=[0.55, 0.35, 0.10]  # Desktop, Mobile, Tablet
        )[0]
        
        if device_type == 'Desktop':
            operating_system = random.choice([os for os in self.operating_systems if 'Windows' in os or 'macOS' in os or 'Ubuntu' in os])
            browser = random.choice([b for b in self.browsers if 'Mobile' not in b])
        elif device_type == 'Mobile':
            operating_system = random.choice([os for os in self.operating_systems if 'iOS' in os or 'Android' in os])
            browser = random.choice(['Mobile Safari', 'Chrome Mobile'])
        else:  # Tablet
            operating_system = random.choice([os for os in self.operating_systems if 'iOS' in os or 'Android' in os])
            browser = random.choice(['Safari 17', 'Chrome Mobile'])
        
        # Location
        country = random.choice(self.countries)
        city = random.choice(self.cities[country])
        
        # Traffic source and campaign
        traffic_source = random.choice(self.traffic_sources)
        utm_campaign = random.choice(self.utm_campaigns) if traffic_source != 'Direct' else None
        
        # Page metrics
        page_views = random.randint(1, 25)
        if outcome == 'bounce':
            page_views = 1
        elif outcome == 'conversion':
            page_views = random.randint(5, 25)
        
        # Engagement metrics
        bounce_rate = 1.0 if outcome == 'bounce' else 0.0
        
        # Entry and exit pages
        entry_pages = ['/home', '/products', '/about', '/login', '/search', '/blog']
        exit_pages = ['/home', '/products', '/checkout', '/contact', '/logout', '/404']
        
        entry_page = random.choice(entry_pages)
        if outcome == 'conversion':
            exit_page = '/checkout'
        elif outcome == 'bounce':
            exit_page = entry_page
        else:
            exit_page = random.choice(exit_pages)
        
        # Conversion data
        conversion_flag = outcome == 'conversion'
        conversion_value = round(random.uniform(25.0, 500.0), 2) if conversion_flag else 0.0
        
        # Returning vs new user
        is_returning_user = random.random() < 0.4 if is_authenticated else False
        
        return {
            'session_id': session_id,
            'user_id': user_id,
            'session_start': session_start.strftime('%Y-%m-%d %H:%M:%S'),
            'session_end': session_end.strftime('%Y-%m-%d %H:%M:%S'),
            'duration_minutes': duration_minutes,
            'device_type': device_type,
            'operating_system': operating_system,
            'browser': browser,
            'country': country,
            'city': city,
            'traffic_source': traffic_source,
            'utm_campaign': utm_campaign,
            'entry_page': entry_page,
            'exit_page': exit_page,
            'page_views': page_views,
            'bounce_rate': bounce_rate,
            'conversion_flag': conversion_flag,
            'conversion_value': conversion_value,
            'is_authenticated': is_authenticated,
            'is_returning_user': is_returning_user
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'session_id': 'string', 'user_id': 'string', 'session_start': 'datetime',
            'session_end': 'datetime', 'duration_minutes': 'integer', 'device_type': 'string',
            'operating_system': 'string', 'browser': 'string', 'country': 'string',
            'city': 'string', 'traffic_source': 'string', 'utm_campaign': 'string',
            'entry_page': 'string', 'exit_page': 'string', 'page_views': 'integer',
            'bounce_rate': 'float', 'conversion_flag': 'boolean', 'conversion_value': 'float',
            'is_authenticated': 'boolean', 'is_returning_user': 'boolean'
        }
