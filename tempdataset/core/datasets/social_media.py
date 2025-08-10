"""
Social Media dataset generator.

Generates realistic social media post data with engagement metrics,
content analysis, and geographic information.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class SocialMediaDataset(BaseDataset):
    """
    Social Media dataset generator that creates realistic social media post data.
    
    Generates social media posts with:
    - Post information (post_id, dates, type, content)
    - User details (user_id, platform)
    - Engagement metrics (likes, comments, shares, views)
    - Content analysis (hashtags, mentions, sentiment)
    - Geographic data (location)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the SocialMediaDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._post_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Social media platforms
        self.platforms = [
            'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 
            'YouTube', 'Snapchat', 'Pinterest', 'Reddit', 'Discord'
        ]
        
        # Post types
        self.post_types = ['Text', 'Image', 'Video', 'Link', 'Story', 'Poll', 'Live', 'Reel']
        
        # Sentiment categories
        self.sentiments = ['Positive', 'Neutral', 'Negative']
        
        # Popular hashtags by category
        self.hashtag_categories = {
            'lifestyle': ['#lifestyle', '#daily', '#mood', '#vibes', '#blessed', '#grateful'],
            'food': ['#food', '#foodie', '#delicious', '#yummy', '#cooking', '#recipe'],
            'travel': ['#travel', '#vacation', '#wanderlust', '#explore', '#adventure', '#trip'],
            'fitness': ['#fitness', '#workout', '#gym', '#health', '#motivation', '#fit'],
            'business': ['#business', '#entrepreneur', '#success', '#marketing', '#growth', '#startup'],
            'tech': ['#tech', '#technology', '#innovation', '#digital', '#ai', '#coding'],
            'fashion': ['#fashion', '#style', '#ootd', '#trendy', '#shopping', '#outfit'],
            'nature': ['#nature', '#outdoors', '#sunset', '#beautiful', '#photography', '#landscape']
        }
        
        # Sample content templates by post type
        self.content_templates = {
            'Text': [
                "Just had an amazing day! Feeling grateful for all the good things in life.",
                "Excited to share some big news with everyone! Stay tuned for updates.",
                "Monday motivation: Every day is a new opportunity to grow and learn.",
                "Reflecting on the weekend and all the memories made with friends and family.",
                "Sometimes the smallest moments bring the greatest joy."
            ],
            'Image': [
                "Check out this beautiful sunset from my evening walk!",
                "Homemade dinner turned out better than expected. Recipe in comments!",
                "New haircut, new me! Thanks to my amazing stylist.",
                "Weekend vibes with the best company. Love these people!",
                "Finally finished this project I've been working on for months."
            ],
            'Video': [
                "Quick tutorial on how to make the perfect morning smoothie!",
                "Behind the scenes of today's photoshoot. So much fun!",
                "Dancing to my favorite song because it's Friday!",
                "Time-lapse of my latest art project coming together.",
                "Workout routine that's been keeping me motivated lately."
            ],
            'Link': [
                "Found this incredible article about sustainable living. Must read!",
                "New blog post is live! Sharing my thoughts on work-life balance.",
                "This podcast episode completely changed my perspective on creativity.",
                "Amazing documentary about ocean conservation. Link in bio!",
                "Just discovered this app that's been a game-changer for productivity."
            ],
            'Story': [
                "Coffee shop adventures this morning ☕",
                "Quick gym session before work 💪",
                "Trying out a new recipe tonight 🍝",
                "Beautiful weather for a walk in the park 🌞",
                "Late night coding session in progress 💻"
            ]
        }
        
        # Common mention patterns
        self.mention_patterns = [
            '@friend', '@family_member', '@colleague', '@brand', '@influencer',
            '@company', '@restaurant', '@gym', '@store', '@artist'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate social media dataset rows.
        
        Returns:
            List of dictionaries representing social media post rows
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
        """Generate a single social media post row."""
        
        # Generate post date (within last year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        post_date = self.faker_utils.date_between(start_date, end_date)
        
        # Generate platform and post type
        platform = random.choice(self.platforms)
        post_type = random.choice(self.post_types)
        
        # Generate content based on post type
        content_text = self._generate_content(post_type)
        media_url = self._generate_media_url(post_type)
        
        # Generate engagement metrics based on platform and content quality
        engagement_metrics = self._generate_engagement_metrics(platform, post_type)
        
        # Generate hashtags and mentions
        hashtags = self._generate_hashtags()
        mentions = self._generate_mentions()
        
        # Generate sentiment
        sentiment = self._generate_sentiment(content_text)
        
        # Generate location (some posts have location, some don't)
        location_data = self._generate_location() if random.random() < 0.6 else (None, None)
        
        return {
            'post_id': self._generate_post_id(post_date),
            'user_id': self._generate_user_id(),
            'platform': platform,
            'post_date': post_date.strftime('%Y-%m-%d %H:%M:%S'),
            'post_type': post_type,
            'content_text': content_text,
            'media_url': media_url,
            'likes_count': engagement_metrics['likes'],
            'comments_count': engagement_metrics['comments'],
            'shares_count': engagement_metrics['shares'],
            'views_count': engagement_metrics['views'],
            'hashtags': hashtags,
            'mentions': mentions,
            'engagement_rate_percent': engagement_metrics['engagement_rate'],
            'location_country': location_data[0],
            'location_city': location_data[1],
            'sentiment': sentiment
        }
    
    def _generate_post_id(self, post_date: datetime) -> str:
        """
        Generate post ID in format "POST-YYYY-NNNNNN".
        
        Args:
            post_date: Date of the post
            
        Returns:
            Formatted post ID
        """
        year = post_date.year
        post_num = str(self._post_counter).zfill(6)
        self._post_counter += 1
        return f"POST-{year}-{post_num}"
    
    def _generate_user_id(self) -> str:
        """
        Generate user ID in format "USER-YYYY-NNNNNN".
        
        Returns:
            Formatted user ID
        """
        year = random.randint(2020, 2025)
        user_num = str(random.randint(1, 999999)).zfill(6)
        return f"USER-{year}-{user_num}"
    
    def _generate_content(self, post_type: str) -> str:
        """
        Generate content text based on post type.
        
        Args:
            post_type: Type of the post
            
        Returns:
            Content text or None for media-only posts
        """
        if post_type in self.content_templates:
            base_content = random.choice(self.content_templates[post_type])
            
            # Sometimes return None for pure media posts
            if post_type in ['Image', 'Video'] and random.random() < 0.2:
                return None
            
            return base_content
        
        return "Check out this amazing content!"
    
    def _generate_media_url(self, post_type: str) -> str:
        """
        Generate media URL based on post type.
        
        Args:
            post_type: Type of the post
            
        Returns:
            Media URL or None for text posts
        """
        if post_type == 'Text':
            return None if random.random() < 0.8 else f"https://example.com/media/{random.randint(1000, 9999)}.jpg"
        elif post_type == 'Image':
            return f"https://example.com/images/{random.randint(1000, 9999)}.jpg"
        elif post_type == 'Video':
            return f"https://example.com/videos/{random.randint(1000, 9999)}.mp4"
        elif post_type == 'Link':
            domains = ['example.com', 'blog.example.com', 'news.example.com', 'shop.example.com']
            return f"https://{random.choice(domains)}/article/{random.randint(100, 999)}"
        else:
            return f"https://example.com/media/{random.randint(1000, 9999)}.jpg" if random.random() < 0.7 else None
    
    def _generate_engagement_metrics(self, platform: str, post_type: str) -> Dict[str, Any]:
        """
        Generate realistic engagement metrics based on platform and post type.
        
        Args:
            platform: Social media platform
            post_type: Type of the post
            
        Returns:
            Dictionary with engagement metrics
        """
        # Base engagement ranges by platform
        platform_ranges = {
            'Instagram': {'likes': (10, 500), 'comments': (1, 50), 'shares': (0, 20)},
            'Facebook': {'likes': (5, 300), 'comments': (0, 30), 'shares': (0, 50)},
            'Twitter': {'likes': (2, 200), 'comments': (0, 25), 'shares': (0, 100)},
            'TikTok': {'likes': (50, 1000), 'comments': (5, 100), 'shares': (2, 200)},
            'LinkedIn': {'likes': (3, 150), 'comments': (0, 20), 'shares': (0, 30)},
            'YouTube': {'likes': (20, 800), 'comments': (2, 80), 'shares': (1, 40)},
        }
        
        # Default ranges for other platforms
        default_range = {'likes': (5, 250), 'comments': (0, 25), 'shares': (0, 30)}
        ranges = platform_ranges.get(platform, default_range)
        
        # Generate base metrics
        likes = random.randint(*ranges['likes'])
        comments = random.randint(*ranges['comments'])
        shares = random.randint(*ranges['shares'])
        
        # Adjust based on post type
        if post_type == 'Video':
            likes = int(likes * random.uniform(1.2, 2.0))
            comments = int(comments * random.uniform(1.1, 1.5))
            shares = int(shares * random.uniform(1.3, 1.8))
        elif post_type == 'Image':
            likes = int(likes * random.uniform(1.1, 1.6))
        elif post_type == 'Text':
            likes = int(likes * random.uniform(0.7, 1.2))
            comments = int(comments * random.uniform(1.2, 1.8))
        
        # Generate views (higher than engagement)
        total_engagement = likes + comments + shares
        views = int(total_engagement * random.uniform(5, 20)) if total_engagement > 0 else random.randint(10, 100)
        
        # Calculate engagement rate
        engagement_rate = round((total_engagement / views * 100), 2) if views > 0 else 0.0
        
        return {
            'likes': likes,
            'comments': comments,
            'shares': shares,
            'views': views,
            'engagement_rate': engagement_rate
        }
    
    def _generate_hashtags(self) -> str:
        """
        Generate hashtags for the post.
        
        Returns:
            Comma-separated string of hashtags
        """
        # Randomly select a category and number of hashtags
        num_hashtags = random.randint(0, 8)
        if num_hashtags == 0:
            return ""
        
        # Select hashtags from different categories
        all_hashtags = []
        for category in random.sample(list(self.hashtag_categories.keys()), min(3, len(self.hashtag_categories))):
            all_hashtags.extend(self.hashtag_categories[category])
        
        selected_hashtags = random.sample(all_hashtags, min(num_hashtags, len(all_hashtags)))
        return ", ".join(selected_hashtags)
    
    def _generate_mentions(self) -> str:
        """
        Generate mentions for the post.
        
        Returns:
            Comma-separated string of mentions
        """
        num_mentions = random.randint(0, 4)
        if num_mentions == 0:
            return ""
        
        mentions = []
        for _ in range(num_mentions):
            base_mention = random.choice(self.mention_patterns)
            mention = f"{base_mention}{random.randint(1, 999)}"
            mentions.append(mention)
        
        return ", ".join(mentions)
    
    def _generate_sentiment(self, content_text: str) -> str:
        """
        Generate sentiment based on content.
        
        Args:
            content_text: The post content
            
        Returns:
            Sentiment category
        """
        if content_text is None:
            return random.choice(self.sentiments)
        
        # Simple sentiment analysis based on keywords
        positive_words = ['amazing', 'great', 'love', 'excited', 'happy', 'grateful', 'wonderful', 'perfect', 'best']
        negative_words = ['bad', 'terrible', 'hate', 'angry', 'sad', 'disappointed', 'worst', 'awful']
        
        content_lower = content_text.lower()
        positive_count = sum(1 for word in positive_words if word in content_lower)
        negative_count = sum(1 for word in negative_words if word in content_lower)
        
        if positive_count > negative_count:
            return 'Positive'
        elif negative_count > positive_count:
            return 'Negative'
        else:
            return 'Neutral'
    
    def _generate_location(self) -> tuple:
        """
        Generate location data.
        
        Returns:
            Tuple of (country, city)
        """
        country = self.faker_utils.country()
        city = self.faker_utils.city()
        return (country, city)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'post_id': 'string',
            'user_id': 'string',
            'platform': 'string',
            'post_date': 'datetime',
            'post_type': 'string',
            'content_text': 'string',
            'media_url': 'string',
            'likes_count': 'integer',
            'comments_count': 'integer',
            'shares_count': 'integer',
            'views_count': 'integer',
            'hashtags': 'string',
            'mentions': 'string',
            'engagement_rate_percent': 'float',
            'location_country': 'string',
            'location_city': 'string',
            'sentiment': 'string'
        }