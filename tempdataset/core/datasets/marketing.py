"""
Marketing dataset generator.

Generates realistic marketing campaign data with 36 columns including campaign information,
performance metrics, audience details, and financial calculations.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class MarketingDataset(BaseDataset):
    """
    Marketing dataset generator that creates realistic marketing campaign data.
    
    Generates 36 columns of marketing data including:
    - Campaign information (campaign_id, name, dates, status)
    - Channel and platform details (channel, platform, creative information)
    - Audience information (target_audience, audience_size, demographics)
    - Financial data (budget, spend, revenue, costs)
    - Performance metrics (impressions, clicks, conversions, rates)
    - Geographic data (region, country)
    - Engagement metrics (likes, comments, shares)
    - Management information (agency, manager)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the MarketingDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._campaign_counter = 1
        self._creative_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Marketing channels and their corresponding platforms
        self.channel_platforms = {
            'Email': ['Mailchimp', 'SendGrid', 'Constant Contact', 'Campaign Monitor', 'ConvertKit', 'AWeber'],
            'Social Media': ['Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 'Snapchat', 'Pinterest'],
            'Search Engine': ['Google Ads', 'Bing Ads', 'Yahoo Ads', 'DuckDuckGo Ads'],
            'TV': ['National TV', 'Cable TV', 'Streaming TV', 'Local TV'],
            'Radio': ['AM Radio', 'FM Radio', 'Satellite Radio', 'Podcast Ads'],
            'Print': ['Newspaper', 'Magazine', 'Direct Mail', 'Billboard'],
            'Outdoor': ['Billboard', 'Transit Ads', 'Street Furniture', 'Digital Signage']
        }
        
        # Campaign types and names
        self.campaign_types = [
            'Brand Awareness', 'Product Launch', 'Lead Generation', 'Sales Promotion',
            'Customer Retention', 'Event Promotion', 'Holiday Campaign', 'Back to School',
            'Black Friday', 'Summer Sale', 'New Year', 'Valentine\'s Day'
        ]
        
        self.campaign_name_templates = [
            '{type} Q{quarter} {year}',
            '{type} - {season} {year}',
            '{product} Launch Campaign',
            '{type} {month} {year}',
            'Holiday {type} Campaign',
            '{brand} {type} Initiative'
        ]
        
        # Target audiences
        self.age_groups = ['18-25', '26-35', '36-45', '46-55', '55-65', '65+']
        self.demographics = ['Urban', 'Suburban', 'Rural']
        self.interests = [
            'Tech-savvy', 'Fitness Enthusiasts', 'Fashion Lovers', 'Food & Beverage',
            'Travel Enthusiasts', 'Sports Fans', 'Music Lovers', 'Gaming Community',
            'Health Conscious', 'Eco-Friendly', 'Luxury Seekers', 'Budget Conscious'
        ]
        
        # Geographic regions and countries
        self.regions = ['North America', 'Europe', 'Asia-Pacific', 'Latin America', 'Middle East & Africa']
        self.region_countries = {
            'North America': ['United States', 'Canada', 'Mexico'],
            'Europe': ['United Kingdom', 'Germany', 'France', 'Italy', 'Spain', 'Netherlands'],
            'Asia-Pacific': ['Japan', 'Australia', 'South Korea', 'Singapore', 'India', 'China'],
            'Latin America': ['Brazil', 'Argentina', 'Mexico', 'Chile', 'Colombia'],
            'Middle East & Africa': ['UAE', 'Saudi Arabia', 'South Africa', 'Egypt', 'Israel']
        }
        
        # Campaign statuses
        self.campaign_statuses = ['Planned', 'Active', 'Completed', 'Paused', 'Cancelled']
        
        # Creative types
        self.creative_types = ['Image', 'Video', 'Carousel', 'Text', 'Mixed']
        
        # Marketing agencies
        self.agencies = [
            'Creative Solutions Inc', 'Digital Marketing Pro', 'Brand Builders LLC',
            'Marketing Mavericks', 'Strategic Advertising Co', 'Innovation Marketing Group',
            'Global Campaigns Ltd', 'Performance Marketing Hub', 'Creative Edge Agency',
            'Digital Dynamics', 'Marketing Masters', 'Brand Vision Studios'
        ]
        
        # Manager names (using common marketing names)
        self.managers = [
            'Sarah Marketing', 'John Campaign', 'Lisa Strategy', 'Mike Creative',
            'Jennifer Digital', 'Robert Analytics', 'Amanda Brand', 'Chris Performance',
            'Michelle Growth', 'David Social', 'Emily Content', 'James Acquisition'
        ]
        
        # Seasons and months
        self.seasons = ['Spring', 'Summer', 'Fall', 'Winter']
        self.months = ['January', 'February', 'March', 'April', 'May', 'June',
                      'July', 'August', 'September', 'October', 'November', 'December']
        
        # Product categories for campaign naming
        self.products = [
            'Smartphone', 'Laptop', 'Clothing Line', 'Skincare', 'Fitness App',
            'Food Delivery', 'Streaming Service', 'Electric Vehicle', 'Travel Package',
            'Home Appliance', 'Gaming Console', 'Fashion Brand'
        ]
        
        self.brands = [
            'TechNova', 'StyleMax', 'FitLife', 'FoodieExpress', 'StreamNow',
            'EcoDrive', 'WanderLust', 'HomeComfort', 'GameZone', 'UrbanStyle'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate marketing dataset rows.
        
        Returns:
            List of dictionaries representing marketing campaign rows
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
        """Generate a single marketing campaign row."""
        
        # Generate campaign dates (within last 2 years to next 6 months)
        end_date = datetime.now() + timedelta(days=180)
        start_date = datetime.now() - timedelta(days=730)
        
        campaign_start = self.faker_utils.date_between(start_date, end_date)
        
        # Ensure we have a datetime object, not a date object
        if hasattr(campaign_start, 'date'):
            # It's a datetime object
            campaign_start_date = campaign_start.date()
        else:
            # It's a date object
            campaign_start_date = campaign_start
            # Convert to datetime for consistency in other operations
            campaign_start = datetime.combine(campaign_start, datetime.min.time())
        
        # Campaign duration between 7 days to 90 days
        duration_days = random.randint(7, 90)
        campaign_end = campaign_start + timedelta(days=duration_days)
        
        # Generate channel and platform
        channel = random.choice(list(self.channel_platforms.keys()))
        platform = random.choice(self.channel_platforms[channel])
        
        # Generate campaign name
        campaign_name = self._generate_campaign_name()
        
        # Generate target audience
        age_group = random.choice(self.age_groups)
        demographic = random.choice(self.demographics)
        interest = random.choice(self.interests)
        target_audience = f"{age_group}, {demographic}, {interest}"
        
        # Generate audience size based on channel
        audience_size = self._generate_audience_size(channel)
        
        # Generate budget and spend
        budget_usd = round(random.uniform(1000, 500000), 2)
        spend_usd = round(budget_usd * random.uniform(0.7, 1.0), 2)  # 70-100% of budget
        
        # Generate performance metrics
        impressions = self._generate_impressions(channel, spend_usd)
        clicks = self._generate_clicks(impressions)
        conversions = self._generate_conversions(clicks)
        
        # Calculate rates
        click_through_rate = round((clicks / impressions * 100) if impressions > 0 else 0, 2)
        conversion_rate = round((conversions / clicks * 100) if clicks > 0 else 0, 2)
        
        # Calculate costs
        cost_per_click = round((spend_usd / clicks) if clicks > 0 else 0, 2)
        cost_per_conversion = round((spend_usd / conversions) if conversions > 0 else 0, 2)
        
        # Generate revenue and ROI
        revenue_usd = round(conversions * random.uniform(50, 500), 2)  # $50-500 per conversion
        roi_percentage = round(((revenue_usd - spend_usd) / spend_usd * 100) if spend_usd > 0 else 0, 2)
        
        # Generate geographic information
        region = random.choice(self.regions)
        country = random.choice(self.region_countries[region])
        
        # Generate status based on dates
        current_date = datetime.now().date()
        if campaign_start_date > current_date:
            status = 'Planned'
        elif campaign_start_date <= current_date <= campaign_end.date():
            status = random.choice(['Active', 'Paused'])
        else:
            status = random.choice(['Completed', 'Cancelled'])
        
        # Generate creative information
        creative_type = random.choice(self.creative_types)
        creative_name = self._generate_creative_name(creative_type)
        
        # Generate engagement metrics
        likes, comments, shares = self._generate_engagement_metrics(impressions, channel)
        engagement_rate = round(((likes + comments + shares) / impressions * 100) if impressions > 0 else 0, 2)
        
        # Generate additional metrics
        bounce_rate = round(random.uniform(20, 80), 2)  # 20-80%
        avg_session_duration = round(random.uniform(30, 600), 2)  # 30 seconds to 10 minutes
        
        # Generate lead metrics
        lead_count = random.randint(0, conversions * 3)  # 0 to 3x conversions
        cost_per_lead = round((spend_usd / lead_count) if lead_count > 0 else 0, 2)
        
        # Generate ad frequency
        ad_frequency = round(random.uniform(1.0, 8.0), 2)
        
        # Generate agency and manager
        agency_name = random.choice(self.agencies)
        manager_name = random.choice(self.managers)
        
        return {
            'campaign_id': self._generate_campaign_id(campaign_start),
            'campaign_name': campaign_name,
            'start_date': campaign_start.strftime('%Y-%m-%d'),
            'end_date': campaign_end.strftime('%Y-%m-%d'),
            'channel': channel,
            'platform': platform,
            'target_audience': target_audience,
            'budget_usd': budget_usd,
            'spend_usd': spend_usd,
            'impressions': impressions,
            'clicks': clicks,
            'click_through_rate': click_through_rate,
            'conversions': conversions,
            'conversion_rate': conversion_rate,
            'cost_per_click': cost_per_click,
            'cost_per_conversion': cost_per_conversion,
            'revenue_usd': revenue_usd,
            'roi_percentage': roi_percentage,
            'region': region,
            'country': country,
            'status': status,
            'creative_type': creative_type,
            'audience_size': audience_size,
            'bounce_rate': bounce_rate,
            'avg_session_duration': avg_session_duration,
            'lead_count': lead_count,
            'cost_per_lead': cost_per_lead,
            'engagement_rate': engagement_rate,
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'ad_frequency': ad_frequency,
            'creative_id': self._generate_creative_id(),
            'creative_name': creative_name,
            'agency_name': agency_name,
            'manager_name': manager_name
        }
    
    def _generate_campaign_id(self, campaign_date: datetime) -> str:
        """
        Generate campaign ID in format "CMP-YYYY-NNNNNN".
        
        Args:
            campaign_date: Date of the campaign
            
        Returns:
            Formatted campaign ID
        """
        year = campaign_date.year
        campaign_num = str(self._campaign_counter).zfill(6)
        self._campaign_counter += 1
        return f"CMP-{year}-{campaign_num:0>6}"
    
    def _generate_creative_id(self) -> str:
        """
        Generate creative ID in format "CRTV-NNNNNN".
        
        Returns:
            Formatted creative ID
        """
        creative_num = str(self._creative_counter).zfill(6)
        self._creative_counter += 1
        return f"CRTV-{creative_num:0>6}"
    
    def _generate_campaign_name(self) -> str:
        """
        Generate realistic campaign name.
        
        Returns:
            Campaign name string
        """
        template = random.choice(self.campaign_name_templates)
        
        replacements = {
            'type': random.choice(self.campaign_types),
            'quarter': random.randint(1, 4),
            'year': random.randint(2023, 2025),
            'season': random.choice(self.seasons),
            'month': random.choice(self.months),
            'product': random.choice(self.products),
            'brand': random.choice(self.brands)
        }
        
        # Replace placeholders in template
        name = template
        for key, value in replacements.items():
            name = name.replace(f'{{{key}}}', str(value))
        
        return name
    
    def _generate_creative_name(self, creative_type: str) -> str:
        """
        Generate creative name based on type.
        
        Args:
            creative_type: Type of creative
            
        Returns:
            Creative name string
        """
        type_templates = {
            'Image': ['Static Banner', 'Product Photo', 'Brand Logo', 'Lifestyle Image'],
            'Video': ['Product Demo', 'Brand Story', 'Testimonial Video', 'How-to Video'],
            'Carousel': ['Product Showcase', 'Step-by-step Guide', 'Feature Highlights'],
            'Text': ['Compelling Copy', 'Call-to-Action Text', 'Product Description'],
            'Mixed': ['Multi-format Campaign', 'Integrated Creative', 'Cross-platform Asset']
        }
        
        base_name = random.choice(type_templates[creative_type])
        version = random.choice(['V1', 'V2', 'V3', 'Final', 'A', 'B'])
        
        return f"{base_name} {version}"
    
    def _generate_audience_size(self, channel: str) -> int:
        """
        Generate audience size based on channel.
        
        Args:
            channel: Marketing channel
            
        Returns:
            Audience size as integer
        """
        size_ranges = {
            'Email': (1000, 100000),
            'Social Media': (5000, 2000000),
            'Search Engine': (10000, 5000000),
            'TV': (100000, 10000000),
            'Radio': (50000, 2000000),
            'Print': (20000, 500000),
            'Outdoor': (100000, 3000000)
        }
        
        min_size, max_size = size_ranges.get(channel, (1000, 100000))
        return random.randint(min_size, max_size)
    
    def _generate_impressions(self, channel: str, spend: float) -> int:
        """
        Generate impressions based on channel and spend.
        
        Args:
            channel: Marketing channel
            spend: Campaign spend
            
        Returns:
            Number of impressions
        """
        # Different channels have different cost per impression ranges
        cpm_ranges = {
            'Email': (0.1, 1.0),  # Very low CPM
            'Social Media': (1.0, 15.0),
            'Search Engine': (2.0, 20.0),
            'TV': (5.0, 50.0),
            'Radio': (3.0, 25.0),
            'Print': (2.0, 30.0),
            'Outdoor': (1.0, 10.0)
        }
        
        min_cpm, max_cpm = cpm_ranges.get(channel, (1.0, 10.0))
        cpm = random.uniform(min_cpm, max_cpm)
        
        # Calculate impressions: spend / (cpm / 1000)
        impressions = int((spend / cpm) * 1000)
        
        # Add some randomness
        return random.randint(int(impressions * 0.8), int(impressions * 1.2))
    
    def _generate_clicks(self, impressions: int) -> int:
        """
        Generate clicks based on impressions.
        
        Args:
            impressions: Number of impressions
            
        Returns:
            Number of clicks
        """
        # Typical CTR ranges from 0.1% to 8%
        ctr = random.uniform(0.001, 0.08)
        clicks = int(impressions * ctr)
        
        return max(0, clicks)  # Ensure non-negative
    
    def _generate_conversions(self, clicks: int) -> int:
        """
        Generate conversions based on clicks.
        
        Args:
            clicks: Number of clicks
            
        Returns:
            Number of conversions
        """
        # Typical conversion rates range from 0.5% to 15%
        conversion_rate = random.uniform(0.005, 0.15)
        conversions = int(clicks * conversion_rate)
        
        return max(0, conversions)  # Ensure non-negative
    
    def _generate_engagement_metrics(self, impressions: int, channel: str) -> tuple:
        """
        Generate likes, comments, and shares based on impressions and channel.
        
        Args:
            impressions: Number of impressions
            channel: Marketing channel
            
        Returns:
            Tuple of (likes, comments, shares)
        """
        # Engagement rates vary by channel
        if channel == 'Social Media':
            # Higher engagement for social media
            likes_rate = random.uniform(0.01, 0.05)  # 1-5%
            comments_rate = random.uniform(0.001, 0.01)  # 0.1-1%
            shares_rate = random.uniform(0.001, 0.005)  # 0.1-0.5%
        elif channel in ['Email', 'Search Engine']:
            # Lower engagement for non-social channels
            likes_rate = random.uniform(0.001, 0.01)  # 0.1-1%
            comments_rate = random.uniform(0.0001, 0.005)  # 0.01-0.5%
            shares_rate = random.uniform(0.0001, 0.002)  # 0.01-0.2%
        else:
            # Minimal engagement for traditional channels
            likes_rate = random.uniform(0.0001, 0.005)
            comments_rate = random.uniform(0.00001, 0.001)
            shares_rate = random.uniform(0.00001, 0.0005)
        
        likes = int(impressions * likes_rate)
        comments = int(impressions * comments_rate)
        shares = int(impressions * shares_rate)
        
        return max(0, likes), max(0, comments), max(0, shares)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'campaign_id': 'string',
            'campaign_name': 'string',
            'start_date': 'date',
            'end_date': 'date',
            'channel': 'string',
            'platform': 'string',
            'target_audience': 'string',
            'budget_usd': 'float',
            'spend_usd': 'float',
            'impressions': 'integer',
            'clicks': 'integer',
            'click_through_rate': 'float',
            'conversions': 'integer',
            'conversion_rate': 'float',
            'cost_per_click': 'float',
            'cost_per_conversion': 'float',
            'revenue_usd': 'float',
            'roi_percentage': 'float',
            'region': 'string',
            'country': 'string',
            'status': 'string',
            'creative_type': 'string',
            'audience_size': 'integer',
            'bounce_rate': 'float',
            'avg_session_duration': 'float',
            'lead_count': 'integer',
            'cost_per_lead': 'float',
            'engagement_rate': 'float',
            'likes': 'integer',
            'comments': 'integer',
            'shares': 'integer',
            'ad_frequency': 'float',
            'creative_id': 'string',
            'creative_name': 'string',
            'agency_name': 'string',
            'manager_name': 'string'
        }
