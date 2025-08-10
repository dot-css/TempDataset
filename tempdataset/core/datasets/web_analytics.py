"""
Web analytics dataset generator.

Generates realistic web analytics and traffic data.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class WebAnalyticsDataset(BaseDataset):
    """Web analytics dataset generator for website traffic data."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._session_counter = 1
    
    def _init_data_lists(self) -> None:
        self.device_types = ['Desktop', 'Mobile', 'Tablet']
        
        self.browsers = [
            'Chrome', 'Firefox', 'Safari', 'Edge', 'Opera', 
            'Internet Explorer', 'Samsung Internet', 'UC Browser'
        ]
        
        self.operating_systems = [
            'Windows 10', 'Windows 11', 'macOS', 'Linux', 'iOS', 
            'Android', 'ChromeOS', 'Ubuntu'
        ]
        
        self.traffic_sources = ['Organic', 'Paid', 'Referral', 'Direct', 'Social', 'Email']
        
        self.page_urls = [
            '/', '/home', '/products', '/about', '/contact', '/blog',
            '/services', '/pricing', '/login', '/signup', '/checkout',
            '/cart', '/search', '/category/electronics', '/category/clothing',
            '/product/laptop', '/product/phone', '/support', '/faq', '/terms'
        ]
        
        self.referrer_domains = [
            'google.com', 'facebook.com', 'twitter.com', 'linkedin.com',
            'youtube.com', 'instagram.com', 'reddit.com', 'pinterest.com',
            'tiktok.com', 'bing.com', 'yahoo.com', None
        ]
        
        self.campaign_names = [
            'summer_sale_2025', 'black_friday', 'product_launch',
            'brand_awareness', 'retargeting_campaign', 'email_newsletter',
            'social_media_ads', 'search_ads', None
        ]
        
        self.countries = [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
            'Australia', 'Japan', 'China', 'India', 'Brazil', 'Mexico',
            'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Spain', 'Italy'
        ]
        
        self.cities = {
            'United States': ['New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix'],
            'Canada': ['Toronto', 'Vancouver', 'Montreal', 'Calgary', 'Ottawa'],
            'United Kingdom': ['London', 'Manchester', 'Birmingham', 'Glasgow', 'Liverpool'],
            'Germany': ['Berlin', 'Munich', 'Hamburg', 'Cologne', 'Frankfurt'],
            'France': ['Paris', 'Lyon', 'Marseille', 'Toulouse', 'Nice']
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic session info
        session_id = f"WEB-2025-{self._session_counter:06d}"
        self._session_counter += 1
        
        # User ID - 70% of sessions have user IDs (logged in users)
        user_id = f"USER-{random.randint(10000, 999999)}" if random.random() < 0.7 else None
        
        # Page and referrer
        page_url = random.choice(self.page_urls)
        
        # Referrer logic
        traffic_source = random.choice(self.traffic_sources)
        if traffic_source == 'Direct':
            referrer_url = None
        elif traffic_source == 'Organic':
            referrer_url = f"https://www.{random.choice(['google.com', 'bing.com'])}/search?q=keywords"
        else:
            referrer_domain = random.choice([r for r in self.referrer_domains if r is not None])
            referrer_url = f"https://www.{referrer_domain}/page" if referrer_domain else None
        
        # Timestamp
        timestamp = self.faker_utils.date_between(
            datetime.now() - timedelta(days=30),
            datetime.now()
        )
        # Add time component
        timestamp = datetime.combine(
            timestamp,
            datetime.min.time().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Device and browser info
        device_type = random.choice(self.device_types)
        
        # Browser distribution based on device type
        if device_type == 'Mobile':
            browser = random.choices(
                ['Chrome', 'Safari', 'Samsung Internet', 'Firefox'],
                weights=[0.5, 0.3, 0.15, 0.05]
            )[0]
            os_options = ['iOS', 'Android']
        elif device_type == 'Tablet':
            browser = random.choices(['Safari', 'Chrome', 'Firefox'], weights=[0.6, 0.3, 0.1])[0]
            os_options = ['iOS', 'Android']
        else:  # Desktop
            browser = random.choices(
                ['Chrome', 'Firefox', 'Safari', 'Edge'],
                weights=[0.65, 0.15, 0.12, 0.08]
            )[0]
            os_options = ['Windows 10', 'Windows 11', 'macOS', 'Linux']
        
        operating_system = random.choice(os_options)
        
        # Geographic info
        geo_country = random.choice(self.countries)
        if geo_country in self.cities:
            geo_city = random.choice(self.cities[geo_country])
        else:
            geo_city = self.faker_utils.city()
        
        # Session metrics
        page_views = random.randint(1, 20)
        
        # Session duration - varies by page views
        if page_views == 1:
            session_duration_seconds = random.randint(5, 300)  # Bounce
            bounce_rate = 100.0
        else:
            session_duration_seconds = random.randint(60, 3600)  # 1 minute to 1 hour
            bounce_rate = 0.0
        
        # Conversion
        conversion_occurred = random.random() < 0.03  # 3% conversion rate
        conversion_value = None
        if conversion_occurred:
            conversion_value = round(random.uniform(10.0, 500.0), 2)
        
        # Campaign
        campaign_name = None
        if traffic_source in ['Paid', 'Email', 'Social']:
            campaign_name = random.choice([c for c in self.campaign_names if c is not None])
        
        return {
            'session_id': session_id,
            'user_id': user_id,
            'page_url': page_url,
            'referrer_url': referrer_url,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'page_views': page_views,
            'session_duration_seconds': session_duration_seconds,
            'bounce_rate': bounce_rate,
            'device_type': device_type,
            'browser': browser,
            'operating_system': operating_system,
            'geo_country': geo_country,
            'geo_city': geo_city,
            'conversion_occurred': conversion_occurred,
            'conversion_value': conversion_value,
            'traffic_source': traffic_source,
            'campaign_name': campaign_name
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'session_id': 'string', 'user_id': 'string', 'page_url': 'string',
            'referrer_url': 'string', 'timestamp': 'datetime', 'page_views': 'integer',
            'session_duration_seconds': 'integer', 'bounce_rate': 'float', 'device_type': 'string',
            'browser': 'string', 'operating_system': 'string', 'geo_country': 'string',
            'geo_city': 'string', 'conversion_occurred': 'boolean', 'conversion_value': 'float',
            'traffic_source': 'string', 'campaign_name': 'string'
        }
