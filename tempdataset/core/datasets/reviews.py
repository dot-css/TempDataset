"""
Reviews dataset generator.

Generates realistic product and service review data with 15+ columns including
ratings, comments, reviewer details, product links, and sentiment analysis.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class ReviewsDataset(BaseDataset):
    """
    Reviews dataset generator that creates realistic product and service review data.
    
    Generates 15+ columns of review data including:
    - Review identification (review_id, product_id, customer info)
    - Rating and feedback (rating, title, text, sentiment)
    - Verification and engagement (verified purchase, helpful votes)
    - Seller interaction (response from seller, response date)
    - Geographic and temporal data
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the ReviewsDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counters for sequential IDs
        self._review_counter = 1
        self._product_counter = 1
        self._customer_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Product categories and names
        self.product_categories = {
            'Electronics': ['Smartphone', 'Laptop', 'Tablet', 'Headphones', 'Smart Watch', 'Camera'],
            'Clothing': ['T-Shirt', 'Jeans', 'Dress', 'Sneakers', 'Jacket', 'Sweater'],
            'Home & Kitchen': ['Coffee Maker', 'Blender', 'Vacuum Cleaner', 'Air Fryer', 'Cookware Set'],
            'Books': ['Fiction Novel', 'Self-Help Book', 'Cookbook', 'Biography', 'Textbook'],
            'Sports': ['Running Shoes', 'Yoga Mat', 'Dumbbells', 'Bicycle', 'Tennis Racket'],
            'Beauty': ['Moisturizer', 'Lipstick', 'Shampoo', 'Perfume', 'Foundation'],
            'Toys': ['Board Game', 'Action Figure', 'Puzzle', 'Building Blocks', 'Doll'],
            'Automotive': ['Car Phone Mount', 'Dash Cam', 'Floor Mats', 'Air Freshener']
        }
        
        # Review titles by rating (positive to negative)
        self.review_titles = {
            5: [
                'Absolutely love it!', 'Perfect product!', 'Exceeded expectations',
                'Amazing quality', 'Highly recommend', 'Best purchase ever',
                'Outstanding performance', 'Fantastic value', 'Love everything about it'
            ],
            4: [
                'Very good product', 'Happy with purchase', 'Good quality',
                'Solid choice', 'Pretty good', 'Worth buying',
                'Good value for money', 'Satisfied customer', 'Nice product'
            ],
            3: [
                'It\'s okay', 'Average product', 'Mixed feelings',
                'Could be better', 'Decent but not great', 'Fair quality',
                'Acceptable', 'Nothing special', 'Middle of the road'
            ],
            2: [
                'Disappointed', 'Not as expected', 'Poor quality',
                'Had issues', 'Wouldn\'t recommend', 'Below average',
                'Not worth it', 'Had problems', 'Unsatisfied'
            ],
            1: [
                'Terrible product', 'Complete waste of money', 'Awful quality',
                'Don\'t buy this', 'Worst purchase ever', 'Completely broken',
                'Total disappointment', 'Save your money', 'Horrible experience'
            ]
        }
        
        # Review text templates by rating
        self.review_texts = {
            5: [
                'This product exceeded all my expectations. The quality is outstanding and it works perfectly. I would definitely buy again and recommend to others.',
                'Amazing product! Great build quality, fast shipping, and excellent customer service. Couldn\'t be happier with this purchase.',
                'Perfect in every way. Easy to use, durable, and exactly what I was looking for. Five stars all the way!',
                'Outstanding quality and performance. This has become one of my favorite purchases. Highly recommend to anyone considering it.',
                'Absolutely love this product! It\'s well-made, functional, and looks great. Worth every penny.'
            ],
            4: [
                'Very good product overall. Minor issues but nothing major. Good value for the price and I\'m satisfied with the purchase.',
                'Happy with this purchase. Good quality and works as expected. Would recommend to others looking for this type of product.',
                'Solid product with good build quality. A few minor complaints but overall very pleased with the performance.',
                'Good product that does what it\'s supposed to do. No major issues and decent value for money.',
                'Pretty good purchase. Quality is good and it arrived quickly. Would consider buying from this brand again.'
            ],
            3: [
                'It\'s an okay product. Does the job but nothing spectacular. Average quality for the price point.',
                'Mixed feelings about this purchase. Some good points and some not so good. It\'s acceptable but could be better.',
                'Decent product but has some limitations. Works fine for basic use but don\'t expect anything amazing.',
                'Average quality product. It works but there are probably better options available for similar price.',
                'It\'s fine, nothing more nothing less. Gets the job done but doesn\'t stand out in any particular way.'
            ],
            2: [
                'Disappointed with this purchase. Quality is below what I expected and had several issues right out of the box.',
                'Not impressed with this product. Poor build quality and doesn\'t work as advertised. Would not recommend.',
                'Had high hopes but this product fell short. Multiple problems and customer service wasn\'t helpful.',
                'Below average product. Cheap materials and poor construction. There are better alternatives available.',
                'Not worth the money. Quality issues and doesn\'t perform as expected. Look elsewhere.'
            ],
            1: [
                'Terrible product! Broke within days of use. Complete waste of money and time. Avoid at all costs.',
                'Worst purchase I\'ve made in a long time. Poor quality, doesn\'t work properly, and customer service is non-existent.',
                'Don\'t buy this product! It\'s cheaply made, doesn\'t work as advertised, and is a complete disappointment.',
                'Awful quality and completely useless. Arrived damaged and replacement was just as bad. Save your money.',
                'Complete garbage. Nothing works properly and it feels like it will break any moment. Terrible experience.'
            ]
        }
        
        # Seller response templates
        self.seller_responses = [
            'Thank you for your review! We\'re glad you\'re happy with your purchase.',
            'We appreciate your feedback and are working to improve our products.',
            'Thank you for choosing our product. Your satisfaction is our priority.',
            'We\'re sorry to hear about the issues. Please contact our support team.',
            'Thanks for the honest review. We value all customer feedback.',
            'We\'re thrilled you love the product! Thank you for the recommendation.',
            'Your feedback helps us improve. Thank you for taking the time to review.',
            'We apologize for any inconvenience. We\'ll make this right.',
            'Thank you for the detailed review. We\'re glad it met your expectations.',
            'We appreciate your business and your honest feedback.'
        ]
        
        # Countries for geographic diversity
        self.countries = [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'France',
            'Australia', 'Japan', 'Italy', 'Spain', 'Netherlands',
            'Sweden', 'Brazil', 'India', 'South Korea', 'Mexico'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate reviews dataset rows.
        
        Returns:
            List of dictionaries representing review rows
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
        """Generate a single review row."""
        
        # Generate rating first as it influences other fields
        rating = self._generate_weighted_rating()
        
        # Generate product information
        category = random.choice(list(self.product_categories.keys()))
        product_name = random.choice(self.product_categories[category])
        product_id = self._generate_product_id()
        
        # Generate customer information
        customer_name = self.faker_utils.name()
        customer_id = self._generate_customer_id()
        
        # Generate review date (within last 2 years)
        review_date = self._generate_review_date()
        
        # Generate review content based on rating
        review_title = random.choice(self.review_titles[rating])
        review_text = random.choice(self.review_texts[rating])
        
        # Generate verification and engagement data
        verified_purchase = random.choice([True, False])
        helpful_votes = self._generate_helpful_votes(rating)
        
        # Generate sentiment score based on rating
        sentiment_score = self._generate_sentiment_score(rating)
        
        # Generate seller response (not all reviews get responses)
        has_response = random.random() < 0.3  # 30% chance of seller response
        response_from_seller = random.choice(self.seller_responses) if has_response else None
        response_date = self._generate_response_date(review_date) if has_response else None
        
        # Generate geographic data
        country = random.choice(self.countries)
        
        return {
            'review_id': self._generate_review_id(),
            'product_id': product_id,
            'product_name': product_name,
            'customer_id': customer_id,
            'customer_name': customer_name,
            'review_date': review_date.strftime('%Y-%m-%d'),
            'rating': rating,
            'review_title': review_title,
            'review_text': review_text,
            'verified_purchase': verified_purchase,
            'helpful_votes': helpful_votes,
            'sentiment_score': round(sentiment_score, 2),
            'response_from_seller': response_from_seller,
            'response_date': response_date.strftime('%Y-%m-%d') if response_date else None,
            'country': country
        }
    
    def _generate_review_id(self) -> str:
        """
        Generate review ID in format "REV-NNNNNN".
        
        Returns:
            Formatted review ID
        """
        review_num = str(self._review_counter).zfill(6)
        self._review_counter += 1
        return f"REV-{review_num}"
    
    def _generate_product_id(self) -> str:
        """
        Generate product ID in format "PROD-AAANNN".
        
        Returns:
            Formatted product ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"PROD-{letters}{numbers}"
    
    def _generate_customer_id(self) -> str:
        """
        Generate customer ID in format "CUST-NNNN".
        
        Returns:
            Formatted customer ID
        """
        customer_num = str(self._customer_counter).zfill(4)
        self._customer_counter += 1
        return f"CUST-{customer_num}"
    
    def _generate_weighted_rating(self) -> int:
        """
        Generate rating with realistic distribution (more 4-5 star reviews).
        
        Returns:
            Rating from 1 to 5
        """
        # Weighted distribution: more positive reviews
        weights = [0.05, 0.10, 0.15, 0.35, 0.35]  # 1-star to 5-star
        return random.choices([1, 2, 3, 4, 5], weights=weights)[0]
    
    def _generate_review_date(self) -> datetime:
        """
        Generate review date (within last 2 years).
        
        Returns:
            Review datetime
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=730)  # 2 years
        return self.faker_utils.date_between(start_date, end_date)
    
    def _generate_helpful_votes(self, rating: int) -> int:
        """
        Generate helpful votes based on rating (higher ratings tend to get more votes).
        
        Args:
            rating: Review rating (1-5)
            
        Returns:
            Number of helpful votes
        """
        # Higher ratings tend to get more helpful votes
        base_range = {
            1: (0, 5),
            2: (0, 8),
            3: (0, 12),
            4: (2, 20),
            5: (5, 35)
        }
        
        min_votes, max_votes = base_range[rating]
        return random.randint(min_votes, max_votes)
    
    def _generate_sentiment_score(self, rating: int) -> float:
        """
        Generate sentiment score based on rating (-1.0 to 1.0).
        
        Args:
            rating: Review rating (1-5)
            
        Returns:
            Sentiment score as float
        """
        # Map rating to sentiment score ranges
        sentiment_ranges = {
            1: (-1.0, -0.6),
            2: (-0.8, -0.2),
            3: (-0.3, 0.3),
            4: (0.2, 0.8),
            5: (0.6, 1.0)
        }
        
        min_sentiment, max_sentiment = sentiment_ranges[rating]
        return random.uniform(min_sentiment, max_sentiment)
    
    def _generate_response_date(self, review_date: datetime) -> datetime:
        """
        Generate seller response date (1-30 days after review).
        
        Args:
            review_date: Date of the original review
            
        Returns:
            Response datetime
        """
        days_after = random.randint(1, 30)
        return review_date + timedelta(days=days_after)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'review_id': 'string',
            'product_id': 'string',
            'product_name': 'string',
            'customer_id': 'string',
            'customer_name': 'string',
            'review_date': 'date',
            'rating': 'integer',
            'review_title': 'string',
            'review_text': 'string',
            'verified_purchase': 'boolean',
            'helpful_votes': 'integer',
            'sentiment_score': 'float',
            'response_from_seller': 'string',
            'response_date': 'date',
            'country': 'string'
        }