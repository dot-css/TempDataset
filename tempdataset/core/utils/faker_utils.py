"""
Faker integration utilities.

Provides utilities for integrating with the Faker library for realistic data generation,
with fallback implementations when Faker is not available.
"""

import random
import string
from typing import Optional, List, Dict, Any, Callable
from datetime import datetime, timedelta, date


class FakerUtils:
    """Utility class for Faker integration with fallback data generation."""
    
    def __init__(self, seed: Optional[int] = None):
        """
        Initialize FakerUtils with optional seed.
        
        Args:
            seed: Random seed for reproducible data generation
        """
        self.faker = None
        self.faker_available = False
        self.seed = seed
        
        # Initialize Faker if available
        self._init_faker()
        
        # Set random seed
        if seed is not None:
            random.seed(seed)
            if self.faker:
                self.faker.seed_instance(seed)
    
    def _init_faker(self) -> None:
        """Initialize Faker library if available."""
        try:
            from faker import Faker
            self.faker = Faker()
            self.faker_available = True
        except ImportError:
            self.faker_available = False
    
    def is_faker_available(self) -> bool:
        """
        Check if Faker library is available.
        
        Returns:
            True if Faker is available, False otherwise
        """
        return self.faker_available
    
    def set_seed(self, seed: int) -> None:
        """
        Set random seed for reproducible data generation.
        
        Args:
            seed: Random seed value
        """
        self.seed = seed
        random.seed(seed)
        if self.faker:
            self.faker.seed_instance(seed)
    
    def name(self) -> str:
        """
        Generate a realistic name.
        
        Returns:
            A person's name
        """
        if self.faker_available:
            return self.faker.name()
        else:
            return self._fallback_name()
    
    def first_name(self) -> str:
        """
        Generate a realistic first name.
        
        Returns:
            A first name
        """
        if self.faker_available:
            return self.faker.first_name()
        else:
            return random.choice(self._get_first_names())
    
    def last_name(self) -> str:
        """
        Generate a realistic last name.
        
        Returns:
            A last name
        """
        if self.faker_available:
            return self.faker.last_name()
        else:
            return random.choice(self._get_last_names())
    
    def email(self, name: Optional[str] = None) -> str:
        """
        Generate a realistic email address.
        
        Args:
            name: Optional name to base email on
            
        Returns:
            An email address
        """
        if self.faker_available:
            return self.faker.email()
        else:
            return self._fallback_email(name)
    
    def address(self) -> str:
        """
        Generate a realistic address.
        
        Returns:
            A street address
        """
        if self.faker_available:
            return self.faker.address()
        else:
            return self._fallback_address()
    
    def city(self) -> str:
        """
        Generate a realistic city name.
        
        Returns:
            A city name
        """
        if self.faker_available:
            return self.faker.city()
        else:
            return random.choice(self._get_cities())
    
    def state(self) -> str:
        """
        Generate a realistic state/province name.
        
        Returns:
            A state or province name
        """
        if self.faker_available:
            return self.faker.state()
        else:
            return random.choice(self._get_states())
    
    def country(self) -> str:
        """
        Generate a realistic country name.
        
        Returns:
            A country name
        """
        if self.faker_available:
            return self.faker.country()
        else:
            return random.choice(self._get_countries())
    
    def postal_code(self) -> str:
        """
        Generate a realistic postal code.
        
        Returns:
            A postal code
        """
        if self.faker_available:
            return self.faker.postcode()
        else:
            return self._fallback_postal_code()
    
    def phone_number(self) -> str:
        """
        Generate a realistic phone number.
        
        Returns:
            A phone number
        """
        if self.faker_available:
            return self.faker.phone_number()
        else:
            return self._fallback_phone_number()
    
    def company(self) -> str:
        """
        Generate a realistic company name.
        
        Returns:
            A company name
        """
        if self.faker_available:
            return self.faker.company()
        else:
            return self._fallback_company()
    
    def date_between(self, start_date: datetime, end_date: datetime) -> date:
        """
        Generate a random date between two dates.
        
        Args:
            start_date: Start date
            end_date: End date
            
        Returns:
            A random date between the specified dates
        """
        if self.faker_available:
            return self.faker.date_between(start_date=start_date, end_date=end_date)
        else:
            return self._fallback_date_between(start_date, end_date)
    
    # Fallback implementations when Faker is not available
    
    def _fallback_name(self) -> str:
        """Generate a name using fallback method."""
        first = random.choice(self._get_first_names())
        last = random.choice(self._get_last_names())
        return f"{first} {last}"
    
    def _fallback_email(self, name: Optional[str] = None) -> str:
        """Generate an email using fallback method."""
        if name:
            # Create email from name
            clean_name = name.lower().replace(' ', '.')
            clean_name = ''.join(c for c in clean_name if c.isalnum() or c == '.')
        else:
            clean_name = f"user{random.randint(1, 9999)}"
        
        domain = random.choice(['gmail.com', 'yahoo.com', 'hotmail.com', 'outlook.com', 'example.com'])
        return f"{clean_name}@{domain}"
    
    def _fallback_address(self) -> str:
        """Generate an address using fallback method."""
        number = random.randint(1, 9999)
        street_name = random.choice(['Main St', 'Oak Ave', 'First St', 'Second Ave', 'Park Rd', 'Elm St'])
        return f"{number} {street_name}"
    
    def _fallback_postal_code(self) -> str:
        """Generate a postal code using fallback method."""
        return f"{random.randint(10000, 99999)}"
    
    def _fallback_phone_number(self) -> str:
        """Generate a phone number using fallback method."""
        area = random.randint(200, 999)
        exchange = random.randint(200, 999)
        number = random.randint(1000, 9999)
        return f"({area}) {exchange}-{number}"
    
    def _fallback_company(self) -> str:
        """Generate a company name using fallback method."""
        prefixes = ['Global', 'United', 'International', 'Advanced', 'Premier', 'Elite']
        suffixes = ['Corp', 'Inc', 'LLC', 'Ltd', 'Group', 'Solutions', 'Systems', 'Technologies']
        middle = ['Tech', 'Data', 'Digital', 'Smart', 'Pro', 'Max', 'Plus', 'Prime']
        
        if random.choice([True, False]):
            return f"{random.choice(prefixes)} {random.choice(middle)} {random.choice(suffixes)}"
        else:
            return f"{random.choice(middle)} {random.choice(suffixes)}"
    
    def _fallback_date_between(self, start_date: datetime, end_date: datetime) -> date:
        """Generate a random date between two dates using fallback method."""
        # Convert datetime inputs to date objects if needed
        if isinstance(start_date, datetime):
            start_date = start_date.date()
        if isinstance(end_date, datetime):
            end_date = end_date.date()
        
        time_between = end_date - start_date
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        result_date = start_date + timedelta(days=random_days)
        
        # Return a date object to match Faker's behavior
        return result_date
    
    def _get_first_names(self) -> List[str]:
        """Get list of common first names for fallback."""
        return [
            'James', 'Mary', 'John', 'Patricia', 'Robert', 'Jennifer', 'Michael', 'Linda',
            'William', 'Elizabeth', 'David', 'Barbara', 'Richard', 'Susan', 'Joseph', 'Jessica',
            'Thomas', 'Sarah', 'Christopher', 'Karen', 'Charles', 'Nancy', 'Daniel', 'Lisa',
            'Matthew', 'Betty', 'Anthony', 'Helen', 'Mark', 'Sandra', 'Donald', 'Donna',
            'Steven', 'Carol', 'Paul', 'Ruth', 'Andrew', 'Sharon', 'Joshua', 'Michelle',
            'Kenneth', 'Laura', 'Kevin', 'Sarah', 'Brian', 'Kimberly', 'George', 'Deborah',
            'Edward', 'Dorothy', 'Ronald', 'Lisa', 'Timothy', 'Nancy', 'Jason', 'Karen'
        ]
    
    def _get_last_names(self) -> List[str]:
        """Get list of common last names for fallback."""
        return [
            'Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis',
            'Rodriguez', 'Martinez', 'Hernandez', 'Lopez', 'Gonzalez', 'Wilson', 'Anderson',
            'Thomas', 'Taylor', 'Moore', 'Jackson', 'Martin', 'Lee', 'Perez', 'Thompson',
            'White', 'Harris', 'Sanchez', 'Clark', 'Ramirez', 'Lewis', 'Robinson', 'Walker',
            'Young', 'Allen', 'King', 'Wright', 'Scott', 'Torres', 'Nguyen', 'Hill',
            'Flores', 'Green', 'Adams', 'Nelson', 'Baker', 'Hall', 'Rivera', 'Campbell'
        ]
    
    def _get_cities(self) -> List[str]:
        """Get list of common cities for fallback."""
        return [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix', 'Philadelphia',
            'San Antonio', 'San Diego', 'Dallas', 'San Jose', 'Austin', 'Jacksonville',
            'Fort Worth', 'Columbus', 'Charlotte', 'San Francisco', 'Indianapolis', 'Seattle',
            'Denver', 'Washington', 'Boston', 'El Paso', 'Nashville', 'Detroit', 'Oklahoma City',
            'Portland', 'Las Vegas', 'Memphis', 'Louisville', 'Baltimore', 'Milwaukee',
            'Albuquerque', 'Tucson', 'Fresno', 'Sacramento', 'Kansas City', 'Mesa',
            'Atlanta', 'Omaha', 'Colorado Springs', 'Raleigh', 'Miami', 'Virginia Beach'
        ]
    
    def _get_states(self) -> List[str]:
        """Get list of US states for fallback."""
        return [
            'Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado', 'Connecticut',
            'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho', 'Illinois', 'Indiana', 'Iowa',
            'Kansas', 'Kentucky', 'Louisiana', 'Maine', 'Maryland', 'Massachusetts', 'Michigan',
            'Minnesota', 'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada', 'New Hampshire',
            'New Jersey', 'New Mexico', 'New York', 'North Carolina', 'North Dakota', 'Ohio',
            'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island', 'South Carolina', 'South Dakota',
            'Tennessee', 'Texas', 'Utah', 'Vermont', 'Virginia', 'Washington', 'West Virginia',
            'Wisconsin', 'Wyoming'
        ]
    
    def _get_countries(self) -> List[str]:
        """Get list of countries for fallback."""
        return [
            'United States', 'Canada', 'United Kingdom', 'Germany', 'France', 'Italy', 'Spain',
            'Australia', 'Japan', 'China', 'India', 'Brazil', 'Mexico', 'Russia', 'South Korea',
            'Netherlands', 'Sweden', 'Norway', 'Denmark', 'Finland', 'Switzerland', 'Austria',
            'Belgium', 'Portugal', 'Greece', 'Poland', 'Czech Republic', 'Hungary', 'Ireland',
            'New Zealand', 'Singapore', 'Thailand', 'Malaysia', 'Philippines', 'Indonesia',
            'Vietnam', 'South Africa', 'Egypt', 'Turkey', 'Israel', 'Argentina', 'Chile'
        ]


# Global instance for easy access
_faker_utils_instance: Optional[FakerUtils] = None


def get_faker_utils(seed: Optional[int] = None) -> FakerUtils:
    """
    Get a global FakerUtils instance.
    
    Args:
        seed: Optional seed for reproducible data generation
        
    Returns:
        FakerUtils instance
    """
    global _faker_utils_instance
    
    if _faker_utils_instance is None or seed is not None:
        _faker_utils_instance = FakerUtils(seed=seed)
    
    return _faker_utils_instance


def is_faker_available() -> bool:
    """
    Check if Faker library is available.
    
    Returns:
        True if Faker is available, False otherwise
    """
    return get_faker_utils().is_faker_available()


def set_global_seed(seed: int) -> None:
    """
    Set global seed for reproducible data generation.
    
    Args:
        seed: Random seed value
    """
    get_faker_utils().set_seed(seed)


# Convenience functions for common operations
def generate_name() -> str:
    """Generate a realistic name."""
    return get_faker_utils().name()


def generate_email(name: Optional[str] = None) -> str:
    """Generate a realistic email address."""
    return get_faker_utils().email(name)


def generate_address() -> str:
    """Generate a realistic address."""
    return get_faker_utils().address()


def generate_city() -> str:
    """Generate a realistic city name."""
    return get_faker_utils().city()


def generate_state() -> str:
    """Generate a realistic state name."""
    return get_faker_utils().state()


def generate_country() -> str:
    """Generate a realistic country name."""
    return get_faker_utils().country()


def generate_postal_code() -> str:
    """Generate a realistic postal code."""
    return get_faker_utils().postal_code()


def generate_phone_number() -> str:
    """Generate a realistic phone number."""
    return get_faker_utils().phone_number()


def generate_company() -> str:
    """Generate a realistic company name."""
    return get_faker_utils().company()