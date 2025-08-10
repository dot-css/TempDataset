"""
Environmental dataset generator.

Generates realistic environmental monitoring data with air quality measurements,
pollution levels, noise monitoring, and atmospheric conditions.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class EnvironmentalDataset(BaseDataset):
    """
    Environmental dataset generator that creates realistic environmental sensor data.
    
    Generates environmental monitoring data including:
    - Record identification (record_id, timestamp, location_id)
    - Geographic information (city, country)
    - Air quality measurements (PM2.5, PM10, gases)
    - Noise level monitoring
    - Air Quality Index calculations
    - Weather correlation data
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the EnvironmentalDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._record_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Air quality categories
        self.air_quality_categories = ['Good', 'Moderate', 'Unhealthy', 'Hazardous']
        
        # Major cities with typical pollution levels
        self.cities_pollution = {
            'Beijing': {'country': 'China', 'pollution_level': 'high'},
            'Delhi': {'country': 'India', 'pollution_level': 'high'},
            'Los Angeles': {'country': 'United States', 'pollution_level': 'medium'},
            'Mexico City': {'country': 'Mexico', 'pollution_level': 'high'},
            'London': {'country': 'United Kingdom', 'pollution_level': 'medium'},
            'Paris': {'country': 'France', 'pollution_level': 'medium'},
            'Tokyo': {'country': 'Japan', 'pollution_level': 'medium'},
            'New York': {'country': 'United States', 'pollution_level': 'medium'},
            'São Paulo': {'country': 'Brazil', 'pollution_level': 'high'},
            'Cairo': {'country': 'Egypt', 'pollution_level': 'high'},
            'Sydney': {'country': 'Australia', 'pollution_level': 'low'},
            'Vancouver': {'country': 'Canada', 'pollution_level': 'low'},
            'Stockholm': {'country': 'Sweden', 'pollution_level': 'low'},
            'Zurich': {'country': 'Switzerland', 'pollution_level': 'low'},
            'Singapore': {'country': 'Singapore', 'pollution_level': 'medium'}
        }
        
        # Pollution level multipliers
        self.pollution_multipliers = {
            'low': 0.5,
            'medium': 1.0,
            'high': 2.0
        }
        
        # AQI breakpoints for PM2.5 (simplified)
        self.aqi_breakpoints = [
            (0, 12, 0, 50),      # Good
            (12.1, 35.4, 51, 100),   # Moderate
            (35.5, 55.4, 101, 150),  # Unhealthy for Sensitive Groups
            (55.5, 150.4, 151, 200), # Unhealthy
            (150.5, 250.4, 201, 300), # Very Unhealthy
            (250.5, 500, 301, 500)    # Hazardous
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate environmental dataset rows.
        
        Returns:
            List of dictionaries representing environmental sensor readings
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
        """Generate a single environmental sensor reading row."""
        
        # Generate timestamp (within last 30 days)
        end_time = datetime.now()
        start_time = end_time - timedelta(days=30)
        date_part = self.faker_utils.date_between(start_time, end_time)
        # Convert date to datetime with random time
        timestamp = datetime.combine(date_part, datetime.min.time()) + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # Select city and get pollution characteristics
        city = random.choice(list(self.cities_pollution.keys()))
        city_data = self.cities_pollution[city]
        country = city_data['country']
        pollution_level = city_data['pollution_level']
        multiplier = self.pollution_multipliers[pollution_level]
        
        # Generate PM2.5 levels (fine particles)
        base_pm25 = 15  # Base level
        pm25 = base_pm25 * multiplier * random.uniform(0.5, 2.0)
        
        # Generate PM10 levels (coarse particles) - typically higher than PM2.5
        pm10 = pm25 * random.uniform(1.2, 2.5)
        
        # Generate gas concentrations
        no2_ppb = self._get_no2_level(pollution_level, timestamp)
        so2_ppb = self._get_so2_level(pollution_level, timestamp)
        co_ppm = self._get_co_level(pollution_level, timestamp)
        o3_ppb = self._get_o3_level(pollution_level, timestamp)
        
        # Generate noise level (urban areas typically 50-80 dB)
        base_noise = 55
        if pollution_level == 'high':
            base_noise = 65  # Busier cities are noisier
        elif pollution_level == 'low':
            base_noise = 45  # Cleaner cities often quieter
        
        noise_db = base_noise + random.uniform(-10, 15)
        
        # Calculate AQI based on PM2.5 (simplified)
        aqi = self._calculate_aqi(pm25)
        
        # Determine air quality category
        air_quality_category = self._get_air_quality_category(aqi)
        
        # Generate weather data that correlates with pollution
        temperature_c, humidity_percent, pressure_hpa = self._get_weather_data(city, timestamp, pollution_level)
        
        return {
            'record_id': self._generate_record_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'location_id': self._generate_location_id(city),
            'city': city,
            'country': country,
            'pm2_5': round(pm25, 1),
            'pm10': round(pm10, 1),
            'no2_ppb': round(no2_ppb, 1),
            'so2_ppb': round(so2_ppb, 1),
            'co_ppm': round(co_ppm, 2),
            'o3_ppb': round(o3_ppb, 1),
            'noise_db': round(noise_db, 1),
            'aqi': int(aqi),
            'air_quality_category': air_quality_category,
            'temperature_c': round(temperature_c, 1),
            'humidity_percent': round(humidity_percent, 1),
            'pressure_hpa': round(pressure_hpa, 1)
        }
    
    def _generate_record_id(self) -> str:
        """
        Generate record ID in format "ENV-YYYY-NNNNNN".
        
        Returns:
            Formatted record ID
        """
        year = datetime.now().year
        record_num = str(self._record_counter).zfill(6)
        self._record_counter += 1
        return f"ENV-{year}-{record_num}"
    
    def _generate_location_id(self, city: str) -> str:
        """
        Generate location ID based on city.
        
        Args:
            city: City name
            
        Returns:
            Formatted location ID
        """
        city_code = city.replace(' ', '').upper()[:3]
        location_num = random.randint(1, 999)
        return f"LOC-{city_code}-{location_num:03d}"
    
    def _get_no2_level(self, pollution_level: str, timestamp: datetime) -> float:
        """
        Get NO2 concentration based on pollution level and time.
        
        Args:
            pollution_level: City pollution level
            timestamp: Current timestamp
            
        Returns:
            NO2 concentration in ppb
        """
        hour = timestamp.hour
        base_no2 = 20
        
        # Higher during rush hours
        if hour in [7, 8, 9, 17, 18, 19]:
            base_no2 *= 1.5
        
        # Apply pollution level multiplier
        multiplier = self.pollution_multipliers[pollution_level]
        no2 = base_no2 * multiplier * random.uniform(0.5, 2.0)
        
        return max(no2, 1)  # Minimum 1 ppb
    
    def _get_so2_level(self, pollution_level: str, timestamp: datetime) -> float:
        """
        Get SO2 concentration based on pollution level.
        
        Args:
            pollution_level: City pollution level
            timestamp: Current timestamp
            
        Returns:
            SO2 concentration in ppb
        """
        base_so2 = 10
        multiplier = self.pollution_multipliers[pollution_level]
        so2 = base_so2 * multiplier * random.uniform(0.3, 3.0)
        
        return max(so2, 0.5)  # Minimum 0.5 ppb
    
    def _get_co_level(self, pollution_level: str, timestamp: datetime) -> float:
        """
        Get CO concentration based on pollution level and time.
        
        Args:
            pollution_level: City pollution level
            timestamp: Current timestamp
            
        Returns:
            CO concentration in ppm
        """
        hour = timestamp.hour
        base_co = 1.0
        
        # Higher during rush hours
        if hour in [7, 8, 9, 17, 18, 19]:
            base_co *= 1.3
        
        multiplier = self.pollution_multipliers[pollution_level]
        co = base_co * multiplier * random.uniform(0.5, 2.5)
        
        return max(co, 0.1)  # Minimum 0.1 ppm
    
    def _get_o3_level(self, pollution_level: str, timestamp: datetime) -> float:
        """
        Get O3 concentration based on pollution level and time.
        
        Args:
            pollution_level: City pollution level
            timestamp: Current timestamp
            
        Returns:
            O3 concentration in ppb
        """
        hour = timestamp.hour
        base_o3 = 30
        
        # Higher during afternoon (photochemical reactions)
        if 12 <= hour <= 16:
            base_o3 *= 1.4
        
        multiplier = self.pollution_multipliers[pollution_level]
        o3 = base_o3 * multiplier * random.uniform(0.4, 2.0)
        
        return max(o3, 5)  # Minimum 5 ppb
    
    def _calculate_aqi(self, pm25: float) -> float:
        """
        Calculate AQI based on PM2.5 concentration.
        
        Args:
            pm25: PM2.5 concentration
            
        Returns:
            Air Quality Index value
        """
        # Find the appropriate breakpoint
        for pm_low, pm_high, aqi_low, aqi_high in self.aqi_breakpoints:
            if pm_low <= pm25 <= pm_high:
                # Linear interpolation
                aqi = ((aqi_high - aqi_low) / (pm_high - pm_low)) * (pm25 - pm_low) + aqi_low
                return aqi
        
        # If PM2.5 is extremely high, return maximum AQI
        return 500
    
    def _get_air_quality_category(self, aqi: float) -> str:
        """
        Get air quality category based on AQI.
        
        Args:
            aqi: Air Quality Index value
            
        Returns:
            Air quality category
        """
        if aqi <= 50:
            return 'Good'
        elif aqi <= 100:
            return 'Moderate'
        elif aqi <= 200:
            return 'Unhealthy'
        else:
            return 'Hazardous'
    
    def _get_weather_data(self, city: str, timestamp: datetime, pollution_level: str) -> tuple:
        """
        Get weather data that correlates with pollution levels.
        
        Args:
            city: City name
            timestamp: Current timestamp
            pollution_level: City pollution level
            
        Returns:
            Tuple of (temperature, humidity, pressure)
        """
        month = timestamp.month
        
        # Base temperature by city (simplified)
        if city in ['Beijing', 'New York', 'London', 'Paris', 'Stockholm', 'Zurich']:
            # Temperate climate
            if month in [12, 1, 2]:
                base_temp = random.uniform(-5, 5)
            elif month in [6, 7, 8]:
                base_temp = random.uniform(20, 30)
            else:
                base_temp = random.uniform(10, 20)
        elif city in ['Delhi', 'Cairo', 'Mexico City']:
            # Hot climate
            base_temp = random.uniform(15, 40)
        else:
            # Moderate climate
            base_temp = random.uniform(10, 25)
        
        temperature_c = base_temp + random.uniform(-5, 5)
        
        # Humidity (higher pollution often correlates with certain weather patterns)
        if pollution_level == 'high':
            humidity_percent = random.uniform(40, 80)  # Often more humid in polluted areas
        else:
            humidity_percent = random.uniform(30, 70)
        
        # Atmospheric pressure
        pressure_hpa = random.uniform(1000, 1030)
        
        return temperature_c, humidity_percent, pressure_hpa
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'record_id': 'string',
            'timestamp': 'datetime',
            'location_id': 'string',
            'city': 'string',
            'country': 'string',
            'pm2_5': 'float',
            'pm10': 'float',
            'no2_ppb': 'float',
            'so2_ppb': 'float',
            'co_ppm': 'float',
            'o3_ppb': 'float',
            'noise_db': 'float',
            'aqi': 'integer',
            'air_quality_category': 'string',
            'temperature_c': 'float',
            'humidity_percent': 'float',
            'pressure_hpa': 'float'
        }