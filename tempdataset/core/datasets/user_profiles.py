"""
User Profiles dataset generator.

Generates realistic user profile data for social media platforms
with demographics, engagement metrics, and account information.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class UserProfilesDataset(BaseDataset):
    """
    User Profiles dataset generator that creates realistic social media user profiles.
    
    Generates user profiles with:
    - User information (user_id, username, personal details)
    - Account details (join_date, platform, status)
    - Social metrics (followers, following, posts)
    - Profile content (bio, interests, connections)
    - Geographic data (location)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the UserProfilesDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._user_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Social media platforms
        self.platforms = [
            'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 
            'YouTube', 'Snapchat', 'Pinterest', 'Reddit', 'Discord'
        ]
        
        # Account statuses
        self.account_statuses = ['Active', 'Suspended', 'Deleted', 'Inactive']
        
        # Common interests categories
        self.interest_categories = {
            'hobbies': ['Photography', 'Reading', 'Gaming', 'Cooking', 'Gardening', 'Music', 'Art', 'Writing'],
            'sports': ['Football', 'Basketball', 'Tennis', 'Swimming', 'Running', 'Cycling', 'Yoga', 'Hiking'],
            'technology': ['Programming', 'AI', 'Blockchain', 'Mobile Apps', 'Web Development', 'Data Science'],
            'lifestyle': ['Fashion', 'Beauty', 'Travel', 'Food', 'Fitness', 'Wellness', 'Home Decor'],
            'entertainment': ['Movies', 'TV Shows', 'Podcasts', 'Stand-up Comedy', 'Theater', 'Concerts'],
            'business': ['Entrepreneurship', 'Marketing', 'Finance', 'Leadership', 'Networking', 'Innovation'],
            'education': ['Online Learning', 'Languages', 'Science', 'History', 'Philosophy', 'Psychology']
        }
        
        # Bio templates by platform type
        self.bio_templates = {
            'professional': [
                "Digital marketing specialist | Coffee enthusiast | Dog lover",
                "Software engineer by day, photographer by night 📸",
                "Helping businesses grow through innovative solutions",
                "Passionate about technology and sustainable living",
                "Building the future, one line of code at a time"
            ],
            'personal': [
                "Living life one adventure at a time ✈️",
                "Foodie | Traveler | Always looking for the next great story",
                "Spreading positivity wherever I go 🌟",
                "Mom of two | Yoga instructor | Plant-based living",
                "Just trying to make the world a little brighter"
            ],
            'creative': [
                "Artist | Dreamer | Creator of beautiful things",
                "Capturing moments that matter 📷",
                "Music is my language, art is my voice",
                "Turning ideas into reality through design",
                "Storyteller with a passion for visual narratives"
            ],
            'influencer': [
                "Lifestyle blogger | Brand partnerships: email@example.com",
                "Fashion & beauty content creator | Link in bio 👇",
                "Sharing my journey to inspire yours ✨",
                "Authentic content | Real stories | Genuine connections",
                "Building a community of like-minded souls"
            ]
        }
        
        # Username patterns
        self.username_patterns = [
            '{first_name}_{last_name}',
            '{first_name}{number}',
            '{first_name}_{word}',
            '{word}_{first_name}',
            '{first_name}{last_initial}{number}',
            'the_{first_name}',
            '{first_name}_official'
        ]
        
        # Common username words
        self.username_words = [
            'creative', 'digital', 'real', 'official', 'pro', 'studio', 'life', 'world',
            'vibes', 'daily', 'journey', 'adventures', 'stories', 'moments', 'dreams'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate user profiles dataset rows.
        
        Returns:
            List of dictionaries representing user profile rows
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
        """Generate a single user profile row."""
        
        # Generate basic user information
        full_name = self.faker_utils.name()
        first_name = full_name.split()[0].lower()
        last_name = full_name.split()[-1].lower()
        
        # Generate join date (within last 5 years)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=1825)  # 5 years
        join_date = self.faker_utils.date_between(start_date, end_date)
        
        # Generate platform
        platform = random.choice(self.platforms)
        
        # Generate username
        username = self._generate_username(first_name, last_name)
        
        # Generate email
        email = self.faker_utils.email(full_name)
        
        # Generate social metrics based on account age and platform
        account_age_days = (datetime.now().date() - join_date).days
        social_metrics = self._generate_social_metrics(platform, account_age_days)
        
        # Generate bio and interests
        bio = self._generate_bio()
        interests = self._generate_interests()
        
        # Generate account status (most are active)
        account_status = self._generate_account_status()
        
        # Generate verification status (rare)
        verified = self._generate_verification_status(social_metrics['followers_count'])
        
        # Generate location
        location_data = self._generate_location() if random.random() < 0.7 else (None, None)
        
        # Generate profile picture URL
        profile_picture_url = self._generate_profile_picture_url()
        
        # Generate connections (for platforms like LinkedIn)
        connections = self._generate_connections(platform, social_metrics['followers_count'])
        
        return {
            'user_id': self._generate_user_id(join_date),
            'username': username,
            'full_name': full_name,
            'email': email,
            'join_date': join_date.strftime('%Y-%m-%d'),
            'platform': platform,
            'followers_count': social_metrics['followers_count'],
            'following_count': social_metrics['following_count'],
            'total_posts': social_metrics['total_posts'],
            'bio': bio,
            'profile_picture_url': profile_picture_url,
            'account_status': account_status,
            'verified': verified,
            'location_country': location_data[0],
            'location_city': location_data[1],
            'interests': interests,
            'connections': connections
        }
    
    def _generate_user_id(self, join_date) -> str:
        """
        Generate user ID in format "USER-YYYY-NNNNNN".
        
        Args:
            join_date: Date when user joined
            
        Returns:
            Formatted user ID
        """
        year = join_date.year
        user_num = str(self._user_counter).zfill(6)
        self._user_counter += 1
        return f"USER-{year}-{user_num}"
    
    def _generate_username(self, first_name: str, last_name: str) -> str:
        """
        Generate username based on name and patterns.
        
        Args:
            first_name: User's first name
            last_name: User's last name
            
        Returns:
            Generated username
        """
        pattern = random.choice(self.username_patterns)
        
        # Replace placeholders
        username = pattern.format(
            first_name=first_name,
            last_name=last_name,
            last_initial=last_name[0] if last_name else 'x',
            number=random.randint(1, 999),
            word=random.choice(self.username_words)
        )
        
        # Ensure username is not too long
        if len(username) > 20:
            username = f"{first_name}{random.randint(1, 999)}"
        
        return username
    
    def _generate_social_metrics(self, platform: str, account_age_days: int) -> Dict[str, int]:
        """
        Generate realistic social metrics based on platform and account age.
        
        Args:
            platform: Social media platform
            account_age_days: Age of account in days
            
        Returns:
            Dictionary with social metrics
        """
        # Base ranges by platform
        platform_ranges = {
            'Instagram': {'followers': (50, 5000), 'following': (100, 1500), 'posts': (10, 2000)},
            'Facebook': {'followers': (20, 2000), 'following': (50, 800), 'posts': (5, 1000)},
            'Twitter': {'followers': (30, 3000), 'following': (100, 2000), 'posts': (50, 5000)},
            'TikTok': {'followers': (100, 10000), 'following': (200, 1000), 'posts': (20, 500)},
            'LinkedIn': {'followers': (100, 5000), 'following': (200, 2000), 'posts': (10, 500)},
            'YouTube': {'followers': (10, 1000), 'following': (50, 500), 'posts': (5, 200)},
        }
        
        # Default ranges for other platforms
        default_range = {'followers': (50, 2000), 'following': (100, 1000), 'posts': (10, 800)}
        ranges = platform_ranges.get(platform, default_range)
        
        # Adjust based on account age (older accounts tend to have more activity)
        age_multiplier = min(1.0 + (account_age_days / 365) * 0.3, 2.0)  # Max 2x multiplier
        
        followers_count = int(random.randint(*ranges['followers']) * age_multiplier)
        following_count = int(random.randint(*ranges['following']) * age_multiplier)
        total_posts = int(random.randint(*ranges['posts']) * age_multiplier)
        
        # Ensure following is not much higher than followers for most users
        if following_count > followers_count * 3 and random.random() < 0.7:
            following_count = int(followers_count * random.uniform(0.5, 2.0))
        
        return {
            'followers_count': followers_count,
            'following_count': following_count,
            'total_posts': total_posts
        }
    
    def _generate_bio(self) -> str:
        """
        Generate bio text.
        
        Returns:
            Bio text or None for some users
        """
        # Some users don't have bios
        if random.random() < 0.3:
            return None
        
        # Select bio type
        bio_type = random.choice(['professional', 'personal', 'creative', 'influencer'])
        bio = random.choice(self.bio_templates[bio_type])
        
        return bio
    
    def _generate_interests(self) -> str:
        """
        Generate user interests.
        
        Returns:
            Comma-separated string of interests
        """
        num_interests = random.randint(2, 8)
        
        # Select interests from different categories
        all_interests = []
        selected_categories = random.sample(
            list(self.interest_categories.keys()), 
            min(3, len(self.interest_categories))
        )
        
        for category in selected_categories:
            all_interests.extend(self.interest_categories[category])
        
        selected_interests = random.sample(all_interests, min(num_interests, len(all_interests)))
        return ", ".join(selected_interests)
    
    def _generate_account_status(self) -> str:
        """
        Generate account status with realistic distribution.
        
        Returns:
            Account status
        """
        # Most accounts are active
        weights = [0.85, 0.05, 0.02, 0.08]  # Active, Suspended, Deleted, Inactive
        return random.choices(self.account_statuses, weights=weights)[0]
    
    def _generate_verification_status(self, followers_count: int) -> bool:
        """
        Generate verification status based on follower count.
        
        Args:
            followers_count: Number of followers
            
        Returns:
            Verification status
        """
        # Higher follower count increases chance of verification
        if followers_count > 10000:
            return random.random() < 0.3
        elif followers_count > 5000:
            return random.random() < 0.1
        elif followers_count > 1000:
            return random.random() < 0.02
        else:
            return random.random() < 0.001
    
    def _generate_location(self) -> tuple:
        """
        Generate location data.
        
        Returns:
            Tuple of (country, city)
        """
        country = self.faker_utils.country()
        city = self.faker_utils.city()
        return (country, city)
    
    def _generate_profile_picture_url(self) -> str:
        """
        Generate profile picture URL.
        
        Returns:
            Profile picture URL or None
        """
        # Some users don't have profile pictures
        if random.random() < 0.15:
            return None
        
        return f"https://example.com/profiles/{random.randint(1000, 9999)}.jpg"
    
    def _generate_connections(self, platform: str, followers_count: int) -> int:
        """
        Generate connections count (mainly for LinkedIn-style platforms).
        
        Args:
            platform: Social media platform
            followers_count: Number of followers
            
        Returns:
            Number of connections
        """
        if platform == 'LinkedIn':
            # LinkedIn connections are typically lower than followers
            base_connections = int(followers_count * random.uniform(0.3, 0.8))
            return max(base_connections, random.randint(50, 500))
        else:
            # For other platforms, connections might be similar to followers
            return int(followers_count * random.uniform(0.1, 0.5))
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'user_id': 'string',
            'username': 'string',
            'full_name': 'string',
            'email': 'string',
            'join_date': 'date',
            'platform': 'string',
            'followers_count': 'integer',
            'following_count': 'integer',
            'total_posts': 'integer',
            'bio': 'string',
            'profile_picture_url': 'string',
            'account_status': 'string',
            'verified': 'boolean',
            'location_country': 'string',
            'location_city': 'string',
            'interests': 'string',
            'connections': 'integer'
        }