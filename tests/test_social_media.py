"""
Tests for social media dataset generator.

Tests the SocialMediaDataset class functionality including data generation,
schema validation, and realistic data patterns.
"""

import pytest
from datetime import datetime
from tempdataset.core.datasets.social_media import SocialMediaDataset


class TestSocialMediaDataset:
    """Test cases for SocialMediaDataset."""
    
    def test_initialization(self):
        """Test dataset initialization with different row counts."""
        # Test default initialization
        dataset = SocialMediaDataset()
        assert dataset.rows == 500
        
        # Test custom row count
        dataset = SocialMediaDataset(1000)
        assert dataset.rows == 1000
        
        # Test zero rows
        dataset = SocialMediaDataset(0)
        assert dataset.rows == 0
    
    def test_schema(self):
        """Test dataset schema structure."""
        dataset = SocialMediaDataset()
        schema = dataset.get_schema()
        
        # Check all required columns are present
        expected_columns = [
            'post_id', 'user_id', 'platform', 'post_date', 'post_type',
            'content_text', 'media_url', 'likes_count', 'comments_count',
            'shares_count', 'views_count', 'hashtags', 'mentions',
            'engagement_rate_percent', 'location_country', 'location_city', 'sentiment'
        ]
        
        assert len(schema) == len(expected_columns)
        for column in expected_columns:
            assert column in schema
        
        # Check data types
        assert schema['post_id'] == 'string'
        assert schema['user_id'] == 'string'
        assert schema['platform'] == 'string'
        assert schema['post_date'] == 'datetime'
        assert schema['post_type'] == 'string'
        assert schema['content_text'] == 'string'
        assert schema['media_url'] == 'string'
        assert schema['likes_count'] == 'integer'
        assert schema['comments_count'] == 'integer'
        assert schema['shares_count'] == 'integer'
        assert schema['views_count'] == 'integer'
        assert schema['hashtags'] == 'string'
        assert schema['mentions'] == 'string'
        assert schema['engagement_rate_percent'] == 'float'
        assert schema['location_country'] == 'string'
        assert schema['location_city'] == 'string'
        assert schema['sentiment'] == 'string'
    
    def test_data_generation(self):
        """Test basic data generation functionality."""
        dataset = SocialMediaDataset(10)
        data = dataset.generate()
        
        # Check correct number of rows
        assert len(data) == 10
        
        # Check each row has all required columns
        for row in data:
            assert len(row) == 17  # Total number of columns
            
            # Check required fields are present
            assert 'post_id' in row
            assert 'user_id' in row
            assert 'platform' in row
            assert 'post_date' in row
            assert 'post_type' in row
            assert 'likes_count' in row
            assert 'comments_count' in row
            assert 'shares_count' in row
            assert 'views_count' in row
            assert 'engagement_rate_percent' in row
            assert 'sentiment' in row
    
    def test_post_id_format(self):
        """Test post ID format and uniqueness."""
        dataset = SocialMediaDataset(5)
        data = dataset.generate()
        
        post_ids = [row['post_id'] for row in data]
        
        # Check uniqueness
        assert len(set(post_ids)) == len(post_ids)
        
        # Check format (POST-YYYY-NNNNNN)
        for post_id in post_ids:
            assert post_id.startswith('POST-')
            parts = post_id.split('-')
            assert len(parts) == 3
            assert len(parts[1]) == 4  # Year
            assert len(parts[2]) == 6  # Sequential number
            assert parts[1].isdigit()
            assert parts[2].isdigit()
    
    def test_user_id_format(self):
        """Test user ID format."""
        dataset = SocialMediaDataset(5)
        data = dataset.generate()
        
        for row in data:
            user_id = row['user_id']
            assert user_id.startswith('USER-')
            parts = user_id.split('-')
            assert len(parts) == 3
            assert len(parts[1]) == 4  # Year
            assert len(parts[2]) == 6  # Sequential number
            assert parts[1].isdigit()
            assert parts[2].isdigit()
    
    def test_platform_values(self):
        """Test platform values are from expected list."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        expected_platforms = [
            'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 
            'YouTube', 'Snapchat', 'Pinterest', 'Reddit', 'Discord'
        ]
        
        platforms = [row['platform'] for row in data]
        for platform in platforms:
            assert platform in expected_platforms
    
    def test_post_type_values(self):
        """Test post type values are from expected list."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        expected_post_types = ['Text', 'Image', 'Video', 'Link', 'Story', 'Poll', 'Live', 'Reel']
        
        post_types = [row['post_type'] for row in data]
        for post_type in post_types:
            assert post_type in expected_post_types
    
    def test_engagement_metrics(self):
        """Test engagement metrics are realistic."""
        dataset = SocialMediaDataset(10)
        data = dataset.generate()
        
        for row in data:
            # Check metrics are non-negative integers
            assert isinstance(row['likes_count'], int)
            assert isinstance(row['comments_count'], int)
            assert isinstance(row['shares_count'], int)
            assert isinstance(row['views_count'], int)
            assert row['likes_count'] >= 0
            assert row['comments_count'] >= 0
            assert row['shares_count'] >= 0
            assert row['views_count'] >= 0
            
            # Check engagement rate is a float between 0 and 100
            assert isinstance(row['engagement_rate_percent'], float)
            assert 0 <= row['engagement_rate_percent'] <= 100
            
            # Views should generally be higher than total engagement
            total_engagement = row['likes_count'] + row['comments_count'] + row['shares_count']
            if total_engagement > 0:
                assert row['views_count'] >= total_engagement
    
    def test_sentiment_values(self):
        """Test sentiment values are from expected categories."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        expected_sentiments = ['Positive', 'Neutral', 'Negative']
        
        sentiments = [row['sentiment'] for row in data]
        for sentiment in sentiments:
            assert sentiment in expected_sentiments
    
    def test_date_format(self):
        """Test post date format and realistic range."""
        dataset = SocialMediaDataset(10)
        data = dataset.generate()
        
        for row in data:
            post_date_str = row['post_date']
            
            # Check format (YYYY-MM-DD HH:MM:SS)
            try:
                post_date = datetime.strptime(post_date_str, '%Y-%m-%d %H:%M:%S')
            except ValueError:
                pytest.fail(f"Invalid date format: {post_date_str}")
            
            # Check date is within last year
            now = datetime.now()
            days_diff = (now - post_date).days
            assert 0 <= days_diff <= 365
    
    def test_content_and_media_relationship(self):
        """Test relationship between post type, content, and media URL."""
        dataset = SocialMediaDataset(50)
        data = dataset.generate()
        
        for row in data:
            post_type = row['post_type']
            content_text = row['content_text']
            media_url = row['media_url']
            
            # Text posts should have content and may or may not have media
            if post_type == 'Text':
                # Most text posts should have content
                if content_text is None:
                    # If no content, should be rare
                    pass
            
            # Image/Video posts should have media URL
            elif post_type in ['Image', 'Video']:
                # Should have media URL (though some might not have content)
                if media_url is not None:
                    assert isinstance(media_url, str)
                    assert media_url.startswith('https://')
            
            # Link posts should have media URL
            elif post_type == 'Link':
                if media_url is not None:
                    assert isinstance(media_url, str)
                    assert media_url.startswith('https://')
    
    def test_hashtags_format(self):
        """Test hashtags format and structure."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        for row in data:
            hashtags = row['hashtags']
            
            if hashtags and hashtags.strip():
                # Should be comma-separated
                hashtag_list = [tag.strip() for tag in hashtags.split(',')]
                
                for hashtag in hashtag_list:
                    # Each hashtag should start with #
                    assert hashtag.startswith('#')
                    # Should not be empty after #
                    assert len(hashtag) > 1
    
    def test_mentions_format(self):
        """Test mentions format and structure."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        for row in data:
            mentions = row['mentions']
            
            if mentions and mentions.strip():
                # Should be comma-separated
                mention_list = [mention.strip() for mention in mentions.split(',')]
                
                for mention in mention_list:
                    # Each mention should start with @
                    assert mention.startswith('@')
                    # Should not be empty after @
                    assert len(mention) > 1
    
    def test_location_data(self):
        """Test location data consistency."""
        dataset = SocialMediaDataset(20)
        data = dataset.generate()
        
        for row in data:
            country = row['location_country']
            city = row['location_city']
            
            # Both should be None or both should have values
            if country is None:
                assert city is None
            elif country is not None:
                assert city is not None
                assert isinstance(country, str)
                assert isinstance(city, str)
                assert len(country.strip()) > 0
                assert len(city.strip()) > 0
    
    def test_seed_reproducibility(self):
        """Test that setting seed produces reproducible results."""
        dataset1 = SocialMediaDataset(5)
        dataset1.set_seed(42)
        data1 = dataset1.generate()
        
        dataset2 = SocialMediaDataset(5)
        dataset2.set_seed(42)
        data2 = dataset2.generate()
        
        # Should generate identical data
        assert len(data1) == len(data2)
        for i in range(len(data1)):
            assert data1[i]['post_id'] == data2[i]['post_id']
            assert data1[i]['platform'] == data2[i]['platform']
            assert data1[i]['post_type'] == data2[i]['post_type']
            assert data1[i]['likes_count'] == data2[i]['likes_count']
    
    def test_empty_dataset(self):
        """Test generation of empty dataset."""
        dataset = SocialMediaDataset(0)
        data = dataset.generate()
        
        assert len(data) == 0
        assert isinstance(data, list)
    
    def test_large_dataset(self):
        """Test generation of larger dataset."""
        dataset = SocialMediaDataset(100)
        data = dataset.generate()
        
        assert len(data) == 100
        
        # Check variety in generated data
        platforms = set(row['platform'] for row in data)
        post_types = set(row['post_type'] for row in data)
        sentiments = set(row['sentiment'] for row in data)
        
        # Should have multiple different values
        assert len(platforms) > 1
        assert len(post_types) > 1
        assert len(sentiments) > 1
    
    def test_engagement_rate_calculation(self):
        """Test that engagement rate is calculated correctly."""
        dataset = SocialMediaDataset(10)
        data = dataset.generate()
        
        for row in data:
            likes = row['likes_count']
            comments = row['comments_count']
            shares = row['shares_count']
            views = row['views_count']
            engagement_rate = row['engagement_rate_percent']
            
            if views > 0:
                expected_rate = ((likes + comments + shares) / views) * 100
                # Allow for small floating point differences
                assert abs(engagement_rate - expected_rate) < 0.01
            else:
                assert engagement_rate == 0.0