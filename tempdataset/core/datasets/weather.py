"""
Weather dataset generator.

Generates realistic weather sensor data with IoT sensor readings including
temperature, humidity, pressure, wind, precipitation, and air quality metrics.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class WeatherDataset(BaseDataset):
    """
    Weather dataset generator that creates realistic weather sensor data.
    
    Generates weather sensor readings including:
    - Record identification (record_id, timestamp, location_id)
    - Geographic data (city, country, coordinates)
    - Temperature and humidity metrics
    - Atmospheric pressure and wind data
    - Precipitation and weather conditions
    - Air quality and visibility metrics
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the WeatherDataset generator.
        
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
        
        # Weather conditions
        self.weather_conditions = ['Clear', 'Cloudy', 'Rain', 'Snow', 'Storm', 'Fog']
        
        # Wind direction names for reference
        self.wind_directions = {
            0: 'N', 45: 'NE', 90: 'E', 135: 'SE',
            180: 'S', 225: 'SW', 270: 'W', 315: 'NW'
        }
        
        # Major cities with approximate coordinates
        self.cities_coords = {
            'New York': {'country': 'United States', 'lat': 40.7128, 'lon': -74.0060},
            'London': {'country': 'United Kingdom', 'lat': 51.5074, 'lon': -0.1278},
            'Tokyo': {'country': 'Japan', 'lat': 35.6762, 'lon': 139.6503},
            'Sydney': {'country': 'Australia', 'lat': -33.8688, 'lon': 151.2093},
            'Paris': {'country': 'France', 'lat': 48.8566, 'lon': 2.3522},
            'Berlin': {'country': 'Germany', 'lat': 52.5200, 'lon': 13.4050},
            'Toronto': {'country': 'Canada', 'lat': 43.6532, 'lon': -79.3832},
            'Mumbai': {'country': 'India', 'lat': 19.0760, 'lon': 72.8777},
            'São Paulo': {'country': 'Brazil', 'lat': -23.5505, 'lon': -46.6333},
            'Cairo': {'country': 'Egypt', 'lat': 30.0444, 'lon': 31.2357}
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate weather dataset rows.
        
        Returns:
            List of dictionaries representing weather sensor readings
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
        """Generate a single weather sensor reading row."""
        
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
        
        # Select city and coordinates
        city = random.choice(list(self.cities_coords.keys()))
        city_data = self.cities_coords[city]
        country = city_data['country']
        
        # Add some variation to coordinates
        latitude = city_data['lat'] + random.uniform(-0.1, 0.1)
        longitude = city_data['lon'] + random.uniform(-0.1, 0.1)
        
        # Generate weather condition first to influence other metrics
        weather_condition = random.choice(self.weather_conditions)
        
        # Generate temperature based on season and location
        base_temp = self._get_base_temperature(city, timestamp)
        temperature_c = base_temp + random.uniform(-5, 5)
        
        # Generate humidity (higher for rain/storm)
        if weather_condition in ['Rain', 'Storm']:
            humidity_percent = random.uniform(70, 100)
        elif weather_condition == 'Clear':
            humidity_percent = random.uniform(30, 60)
        else:
            humidity_percent = random.uniform(40, 80)
        
        # Generate atmospheric pressure
        pressure_hpa = random.uniform(950, 1050)
        
        # Generate wind data
        wind_speed_kmh = self._get_wind_speed(weather_condition)
        wind_direction_deg = random.randint(0, 359)
        
        # Generate precipitation
        precipitation_mm = self._get_precipitation(weather_condition)
        
        # Generate UV index (0 for night, higher for clear days)
        hour = timestamp.hour
        if 6 <= hour <= 18:  # Daytime
            if weather_condition == 'Clear':
                uv_index = random.uniform(3, 11)
            elif weather_condition in ['Cloudy', 'Fog']:
                uv_index = random.uniform(1, 5)
            else:
                uv_index = random.uniform(0, 3)
        else:  # Nighttime
            uv_index = 0.0
        
        # Generate visibility
        if weather_condition == 'Fog':
            visibility_km = random.uniform(0.1, 2)
        elif weather_condition in ['Rain', 'Snow', 'Storm']:
            visibility_km = random.uniform(2, 8)
        else:
            visibility_km = random.uniform(8, 20)
        
        # Calculate dew point (simplified formula)
        dew_point_c = temperature_c - ((100 - humidity_percent) / 5)
        
        # Calculate heat index (simplified)
        if temperature_c > 26:  # Only relevant for high temperatures
            heat_index_c = temperature_c + (humidity_percent - 40) * 0.1
        else:
            heat_index_c = temperature_c
        
        return {
            'record_id': self._generate_record_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'location_id': self._generate_location_id(city),
            'city': city,
            'country': country,
            'latitude': round(latitude, 6),
            'longitude': round(longitude, 6),
            'temperature_c': round(temperature_c, 1),
            'humidity_percent': round(humidity_percent, 1),
            'pressure_hpa': round(pressure_hpa, 1),
            'wind_speed_kmh': round(wind_speed_kmh, 1),
            'wind_direction_deg': wind_direction_deg,
            'precipitation_mm': round(precipitation_mm, 1),
            'weather_condition': weather_condition,
            'uv_index': round(uv_index, 1),
            'visibility_km': round(visibility_km, 1),
            'dew_point_c': round(dew_point_c, 1),
            'heat_index_c': round(heat_index_c, 1)
        }
    
    def _generate_record_id(self) -> str:
        """
        Generate record ID in format "WEA-YYYY-NNNNNN".
        
        Returns:
            Formatted record ID
        """
        year = datetime.now().year
        record_num = str(self._record_counter).zfill(6)
        self._record_counter += 1
        return f"WEA-{year}-{record_num}"
    
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
    
    def _get_base_temperature(self, city: str, timestamp: datetime) -> float:
        """
        Get base temperature for city and season.
        
        Args:
            city: City name
            timestamp: Current timestamp
            
        Returns:
            Base temperature in Celsius
        """
        # Simplified seasonal temperature by city
        month = timestamp.month
        
        # Northern hemisphere cities
        if city in ['New York', 'London', 'Paris', 'Berlin', 'Toronto']:
            if month in [12, 1, 2]:  # Winter
                return random.uniform(-5, 5)
            elif month in [3, 4, 5]:  # Spring
                return random.uniform(10, 20)
            elif month in [6, 7, 8]:  # Summer
                return random.uniform(20, 30)
            else:  # Fall
                return random.uniform(5, 15)
        
        # Southern hemisphere cities
        elif city in ['Sydney', 'São Paulo']:
            if month in [6, 7, 8]:  # Winter
                return random.uniform(5, 15)
            elif month in [9, 10, 11]:  # Spring
                return random.uniform(15, 25)
            elif month in [12, 1, 2]:  # Summer
                return random.uniform(25, 35)
            else:  # Fall
                return random.uniform(10, 20)
        
        # Tropical cities
        else:  # Tokyo, Mumbai, Cairo
            return random.uniform(15, 35)
    
    def _get_wind_speed(self, weather_condition: str) -> float:
        """
        Get wind speed based on weather condition.
        
        Args:
            weather_condition: Current weather condition
            
        Returns:
            Wind speed in km/h
        """
        if weather_condition == 'Storm':
            return random.uniform(40, 120)
        elif weather_condition in ['Rain', 'Snow']:
            return random.uniform(15, 40)
        elif weather_condition == 'Clear':
            return random.uniform(0, 15)
        else:  # Cloudy, Fog
            return random.uniform(5, 25)
    
    def _get_precipitation(self, weather_condition: str) -> float:
        """
        Get precipitation amount based on weather condition.
        
        Args:
            weather_condition: Current weather condition
            
        Returns:
            Precipitation in mm
        """
        if weather_condition == 'Storm':
            return random.uniform(10, 50)
        elif weather_condition == 'Rain':
            return random.uniform(1, 20)
        elif weather_condition == 'Snow':
            return random.uniform(0.5, 10)  # Snow water equivalent
        else:
            return 0.0
    
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
            'latitude': 'float',
            'longitude': 'float',
            'temperature_c': 'float',
            'humidity_percent': 'float',
            'pressure_hpa': 'float',
            'wind_speed_kmh': 'float',
            'wind_direction_deg': 'integer',
            'precipitation_mm': 'float',
            'weather_condition': 'string',
            'uv_index': 'float',
            'visibility_km': 'float',
            'dew_point_c': 'float',
            'heat_index_c': 'float'
        }