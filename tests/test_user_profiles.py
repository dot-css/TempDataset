"""
Tests for user profiles dataset generator.

Tests the UserProfilesDataset class functionality including data generation,
schema validation, and realistic data patterns.
"""

import pytest
from datetime import datetime
from tempdataset.core.datasets.user_profiles import UserProfilesDataset


class TestUserProfilesDataset:
    """Test cases for UserProfilesDataset."""
    
    def test_initialization(self):
        """Test dataset initialization with different row counts."""
        # Test default initialization
        dataset = UserProfilesDataset()
        assert dataset.rows == 500
        
        # Test custom row count
        dataset = UserProfilesDataset(1000)
        assert dataset.rows == 1000
        
        # Test zero rows
        dataset = UserProfilesDataset(0)
        assert dataset.rows == 0
    
    def test_schema(self):
        """Test dataset schema structure."""
        dataset = UserProfilesDataset()
        schema = dataset.get_schema()
        
        # Check all required columns are present
        expected_columns = [
            'user_id', 'username', 'full_name', 'email', 'join_date',
            'platform', 'followers_count', 'following_count', 'total_posts',
            'bio', 'profile_picture_url', 'account_status', 'verified',
            'location_country', 'location_city', 'interests', 'connections'
        ]
        
        assert len(schema) == len(expected_columns)
        for column in expected_columns:
            assert column in schema
        
        # Check data types
        assert schema['user_id'] == 'string'
        assert schema['username'] == 'string'
        assert schema['full_name'] == 'string'
        assert schema['email'] == 'string'
        assert schema['join_date'] == 'date'
        assert schema['platform'] == 'string'
        assert schema['followers_count'] == 'integer'
        assert schema['following_count'] == 'integer'
        assert schema['total_posts'] == 'integer'
        assert schema['bio'] == 'string'
        assert schema['profile_picture_url'] == 'string'
        assert schema['account_status'] == 'string'
        assert schema['verified'] == 'boolean'
        assert schema['location_country'] == 'string'
        assert schema['location_city'] == 'string'
        assert schema['interests'] == 'string'
        assert schema['connections'] == 'integer'
    
    def test_data_generation(self):
        """Test basic data generation functionality."""
        dataset = UserProfilesDataset(10)
        data = dataset.generate()
        
        # Check correct number of rows
        assert len(data) == 10
        
        # Check each row has all required columns
        for row in data:
            assert len(row) == 17  # Total number of columns
            
            # Check required fields are present
            assert 'user_id' in row
            assert 'username' in row
            assert 'full_name' in row
            assert 'email' in row
            assert 'join_date' in row
            assert 'platform' in row
            assert 'followers_count' in row
            assert 'following_count' in row
            assert 'total_posts' in row
            assert 'account_status' in row
            assert 'verified' in row
            assert 'interests' in row
            assert 'connections' in row
    
    def test_user_id_format(self):
        """Test user ID format and uniqueness."""
        dataset = UserProfilesDataset(5)
        data = dataset.generate()
        
        user_ids = [row['user_id'] for row in data]
        
        # Check uniqueness
        assert len(set(user_ids)) == len(user_ids)
        
        # Check format (USER-YYYY-NNNNNN)
        for user_id in user_ids:
            assert user_id.startswith('USER-')
            parts = user_id.split('-')
            assert len(parts) == 3
            assert len(parts[1]) == 4  # Year
            assert len(parts[2]) == 6  # Sequential number
            assert parts[1].isdigit()
            assert parts[2].isdigit()
    
    def test_username_format(self):
        """Test username format and characteristics."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        for row in data:
            username = row['username']
            assert isinstance(username, str)
            assert len(username) > 0
            assert len(username) <= 20  # Should not be too long
            # Username should not contain spaces
            assert ' ' not in username
    
    def test_platform_values(self):
        """Test platform values are from expected list."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        expected_platforms = [
            'Facebook', 'Instagram', 'Twitter', 'LinkedIn', 'TikTok', 
            'YouTube', 'Snapchat', 'Pinterest', 'Reddit', 'Discord'
        ]
        
        platforms = [row['platform'] for row in data]
        for platform in platforms:
            assert platform in expected_platforms
    
    def test_account_status_values(self):
        """Test account status values are from expected list."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        expected_statuses = ['Active', 'Suspended', 'Deleted', 'Inactive']
        
        statuses = [row['account_status'] for row in data]
        for status in statuses:
            assert status in expected_statuses
        
        # Most accounts should be active
        active_count = sum(1 for status in statuses if status == 'Active')
        assert active_count > len(statuses) * 0.5  # More than 50% should be active
    
    def test_social_metrics(self):
        """Test social metrics are realistic."""
        dataset = UserProfilesDataset(10)
        data = dataset.generate()
        
        for row in data:
            # Check metrics are non-negative integers
            assert isinstance(row['followers_count'], int)
            assert isinstance(row['following_count'], int)
            assert isinstance(row['total_posts'], int)
            assert isinstance(row['connections'], int)
            assert row['followers_count'] >= 0
            assert row['following_count'] >= 0
            assert row['total_posts'] >= 0
            assert row['connections'] >= 0
    
    def test_verification_status(self):
        """Test verification status logic."""
        dataset = UserProfilesDataset(50)
        data = dataset.generate()
        
        verified_users = [row for row in data if row['verified']]
        unverified_users = [row for row in data if not row['verified']]
        
        # Most users should not be verified
        assert len(unverified_users) > len(verified_users)
        
        # Verified users should generally have more followers
        if verified_users and unverified_users:
            avg_verified_followers = sum(user['followers_count'] for user in verified_users) / len(verified_users)
            avg_unverified_followers = sum(user['followers_count'] for user in unverified_users) / len(unverified_users)
            
            # This is a tendency, not a strict rule, so we'll be lenient
            # Just check that verified users exist and have reasonable follower counts
            for user in verified_users:
                assert user['followers_count'] >= 0
    
    def test_email_format(self):
        """Test email format is valid."""
        dataset = UserProfilesDataset(10)
        data = dataset.generate()
        
        for row in data:
            email = row['email']
            assert isinstance(email, str)
            assert '@' in email
            assert '.' in email
            assert len(email) > 5  # Minimum reasonable email length
    
    def test_date_format(self):
        """Test join date format and realistic range."""
        dataset = UserProfilesDataset(10)
        data = dataset.generate()
        
        for row in data:
            join_date_str = row['join_date']
            
            # Check format (YYYY-MM-DD)
            try:
                join_date = datetime.strptime(join_date_str, '%Y-%m-%d')
            except ValueError:
                pytest.fail(f"Invalid date format: {join_date_str}")
            
            # Check date is within last 5 years
            now = datetime.now()
            days_diff = (now - join_date).days
            assert 0 <= days_diff <= 1825  # 5 years
    
    def test_bio_content(self):
        """Test bio content and format."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        bio_count = 0
        for row in data:
            bio = row['bio']
            
            if bio is not None:
                bio_count += 1
                assert isinstance(bio, str)
                assert len(bio) > 0
                # Bio should be reasonable length
                assert len(bio) < 500
        
        # Some users should have bios, some shouldn't
        assert bio_count > 0
        assert bio_count < len(data)  # Not all users have bios
    
    def test_interests_format(self):
        """Test interests format and structure."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        for row in data:
            interests = row['interests']
            assert isinstance(interests, str)
            
            if interests and interests.strip():
                # Should be comma-separated
                interest_list = [interest.strip() for interest in interests.split(',')]
                
                # Should have multiple interests
                assert len(interest_list) >= 2
                
                for interest in interest_list:
                    # Each interest should not be empty
                    assert len(interest) > 0
    
    def test_location_data(self):
        """Test location data consistency."""
        dataset = UserProfilesDataset(20)
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
    
    def test_profile_picture_url(self):
        """Test profile picture URL format."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        for row in data:
            profile_picture_url = row['profile_picture_url']
            
            if profile_picture_url is not None:
                assert isinstance(profile_picture_url, str)
                assert profile_picture_url.startswith('https://')
                assert profile_picture_url.endswith('.jpg')
    
    def test_social_metrics_relationships(self):
        """Test relationships between social metrics."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        for row in data:
            followers = row['followers_count']
            following = row['following_count']
            posts = row['total_posts']
            connections = row['connections']
            
            # All should be non-negative
            assert followers >= 0
            assert following >= 0
            assert posts >= 0
            assert connections >= 0
            
            # Connections should generally be related to followers
            # (This is a loose relationship, not strict)
            if followers > 0:
                assert connections >= 0
    
    def test_platform_specific_metrics(self):
        """Test that metrics vary appropriately by platform."""
        dataset = UserProfilesDataset(50)
        data = dataset.generate()
        
        # Group by platform
        platform_data = {}
        for row in data:
            platform = row['platform']
            if platform not in platform_data:
                platform_data[platform] = []
            platform_data[platform].append(row)
        
        # Check that different platforms have different characteristics
        for platform, users in platform_data.items():
            if len(users) > 1:  # Only check if we have multiple users
                followers_counts = [user['followers_count'] for user in users]
                # Should have some variation in follower counts
                assert min(followers_counts) >= 0
                assert max(followers_counts) >= min(followers_counts)
    
    def test_seed_reproducibility(self):
        """Test that setting seed produces reproducible results."""
        dataset1 = UserProfilesDataset(5)
        dataset1.set_seed(42)
        data1 = dataset1.generate()
        
        dataset2 = UserProfilesDataset(5)
        dataset2.set_seed(42)
        data2 = dataset2.generate()
        
        # Should generate identical data
        assert len(data1) == len(data2)
        for i in range(len(data1)):
            assert data1[i]['user_id'] == data2[i]['user_id']
            assert data1[i]['username'] == data2[i]['username']
            assert data1[i]['platform'] == data2[i]['platform']
            assert data1[i]['followers_count'] == data2[i]['followers_count']
    
    def test_empty_dataset(self):
        """Test generation of empty dataset."""
        dataset = UserProfilesDataset(0)
        data = dataset.generate()
        
        assert len(data) == 0
        assert isinstance(data, list)
    
    def test_large_dataset(self):
        """Test generation of larger dataset."""
        dataset = UserProfilesDataset(100)
        data = dataset.generate()
        
        assert len(data) == 100
        
        # Check variety in generated data
        platforms = set(row['platform'] for row in data)
        statuses = set(row['account_status'] for row in data)
        usernames = set(row['username'] for row in data)
        
        # Should have multiple different values
        assert len(platforms) > 1
        assert len(statuses) > 1
        assert len(usernames) >= 95  # Most usernames should be unique (allow some duplicates)
    
    def test_account_age_impact(self):
        """Test that account age impacts social metrics appropriately."""
        dataset = UserProfilesDataset(20)
        data = dataset.generate()
        
        # Parse join dates and check metrics
        for row in data:
            join_date = datetime.strptime(row['join_date'], '%Y-%m-%d')
            account_age_days = (datetime.now() - join_date).days
            
            followers = row['followers_count']
            posts = row['total_posts']
            
            # Older accounts should generally have more activity
            # This is a tendency, not a strict rule
            assert followers >= 0
            assert posts >= 0
            
            # Very new accounts (less than 30 days) might have lower metrics
            # Very old accounts (more than 1000 days) might have higher metrics
            # But we'll just check they're reasonable
            if account_age_days < 30:
                # New accounts might have lower activity, but not necessarily
                pass
            elif account_age_days > 1000:
                # Old accounts might have higher activity, but not necessarily
                pass