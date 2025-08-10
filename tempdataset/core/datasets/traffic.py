"""
Traffic dataset generator.

Generates realistic traffic sensor data with vehicle counts, speeds, congestion levels,
and incident information for urban traffic monitoring systems.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class TrafficDataset(BaseDataset):
    """
    Traffic dataset generator that creates realistic traffic sensor data.
    
    Generates traffic monitoring data including:
    - Record identification (record_id, timestamp, sensor_id)
    - Road and location information
    - Vehicle counts and speed measurements
    - Traffic density and congestion levels
    - Incident tracking and weather impact
    - Public transport delays
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the TrafficDataset generator.
        
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
        
        # Traffic density levels
        self.traffic_densities = ['Low', 'Medium', 'High', 'Severe']
        
        # Congestion levels
        self.congestion_levels = ['Free Flow', 'Slow', 'Stop-and-Go', 'Gridlock']
        
        # Incident types
        self.incident_types = ['Accident', 'Roadwork', 'Obstruction', None]
        
        # Weather conditions
        self.weather_conditions = ['Clear', 'Rain', 'Snow', 'Fog', 'Storm', 'Cloudy']
        
        # Major cities
        self.cities = [
            'New York', 'Los Angeles', 'Chicago', 'Houston', 'Phoenix',
            'Philadelphia', 'San Antonio', 'San Diego', 'Dallas', 'San Jose',
            'Austin', 'Jacksonville', 'Fort Worth', 'Columbus', 'Charlotte'
        ]
        
        # Road types and names
        self.road_types = ['Highway', 'Interstate', 'Boulevard', 'Avenue', 'Street', 'Parkway']
        self.road_names = [
            'Main', 'First', 'Second', 'Third', 'Park', 'Oak', 'Pine', 'Maple',
            'Cedar', 'Elm', 'Washington', 'Lincoln', 'Jefferson', 'Madison',
            'Jackson', 'Franklin', 'Roosevelt', 'Kennedy', 'Johnson', 'Wilson'
        ]
        
        # Speed limits by road type (km/h)
        self.speed_limits = {
            'Highway': 100,
            'Interstate': 120,
            'Boulevard': 60,
            'Avenue': 50,
            'Street': 40,
            'Parkway': 80
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate traffic dataset rows.
        
        Returns:
            List of dictionaries representing traffic sensor readings
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
        """Generate a single traffic sensor reading row."""
        
        # Generate timestamp (within last 7 days for recent traffic data)
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        date_part = self.faker_utils.date_between(start_time, end_time)
        # Convert date to datetime with random time
        timestamp = datetime.combine(date_part, datetime.min.time()) + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # Select city and generate road name
        city = random.choice(self.cities)
        road_type = random.choice(self.road_types)
        road_base = random.choice(self.road_names)
        road_name = f"{road_base} {road_type}"
        
        # Generate traffic metrics based on time of day
        hour = timestamp.hour
        is_rush_hour = hour in [7, 8, 9, 17, 18, 19]
        is_weekend = timestamp.weekday() >= 5
        
        # Generate vehicle count
        vehicle_count = self._get_vehicle_count(hour, is_rush_hour, is_weekend)
        
        # Generate average speed based on road type and traffic
        speed_limit = self.speed_limits[road_type]
        avg_speed_kmh = self._get_average_speed(speed_limit, vehicle_count, is_rush_hour)
        
        # Determine traffic density and congestion
        traffic_density, congestion_level = self._get_traffic_conditions(vehicle_count, avg_speed_kmh, speed_limit)
        
        # Generate incident data (10% chance of incident)
        incident_flag = random.random() < 0.10
        incident_type = random.choice(self.incident_types) if incident_flag else None
        
        # Calculate travel time based on speed and congestion
        base_travel_time = 10.0  # Base 10 minutes for segment
        if congestion_level == 'Free Flow':
            travel_time_min = base_travel_time
        elif congestion_level == 'Slow':
            travel_time_min = base_travel_time * 1.5
        elif congestion_level == 'Stop-and-Go':
            travel_time_min = base_travel_time * 2.5
        else:  # Gridlock
            travel_time_min = base_travel_time * 4.0
        
        # Add incident impact
        if incident_flag:
            travel_time_min *= random.uniform(1.2, 2.0)
        
        # Generate weather condition
        weather_condition = random.choice(self.weather_conditions)
        
        # Weather impact on speed and travel time
        if weather_condition in ['Rain', 'Snow', 'Fog', 'Storm']:
            avg_speed_kmh *= random.uniform(0.7, 0.9)
            travel_time_min *= random.uniform(1.1, 1.4)
        
        # Generate lane closures (more likely during incidents)
        if incident_flag:
            lane_closures = random.randint(1, 3)
        else:
            lane_closures = random.randint(0, 1) if random.random() < 0.05 else 0
        
        # Generate public transport delay
        public_transport_delay_min = self._get_public_transport_delay(congestion_level, weather_condition)
        
        return {
            'record_id': self._generate_record_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'sensor_id': self._generate_sensor_id(),
            'road_name': road_name,
            'city': city,
            'vehicle_count': vehicle_count,
            'avg_speed_kmh': round(avg_speed_kmh, 1),
            'traffic_density': traffic_density,
            'congestion_level': congestion_level,
            'incident_flag': incident_flag,
            'incident_type': incident_type,
            'travel_time_min': round(travel_time_min, 1),
            'weather_condition': weather_condition,
            'lane_closures': lane_closures,
            'public_transport_delay_min': round(public_transport_delay_min, 1)
        }
    
    def _generate_record_id(self) -> str:
        """
        Generate record ID in format "TRA-YYYY-NNNNNN".
        
        Returns:
            Formatted record ID
        """
        year = datetime.now().year
        record_num = str(self._record_counter).zfill(6)
        self._record_counter += 1
        return f"TRA-{year}-{record_num}"
    
    def _generate_sensor_id(self) -> str:
        """
        Generate sensor ID in format "SEN-AAANNN".
        
        Returns:
            Formatted sensor ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"SEN-{letters}{numbers}"
    
    def _get_vehicle_count(self, hour: int, is_rush_hour: bool, is_weekend: bool) -> int:
        """
        Get vehicle count based on time patterns.
        
        Args:
            hour: Hour of the day
            is_rush_hour: Whether it's rush hour
            is_weekend: Whether it's weekend
            
        Returns:
            Number of vehicles
        """
        base_count = 50
        
        if is_weekend:
            # Lower traffic on weekends
            base_count *= 0.7
            # Higher traffic during afternoon/evening
            if 12 <= hour <= 20:
                base_count *= 1.3
        else:
            # Weekday patterns
            if is_rush_hour:
                base_count *= 2.5
            elif 10 <= hour <= 16:  # Midday
                base_count *= 1.2
            elif 22 <= hour or hour <= 5:  # Night
                base_count *= 0.3
        
        return int(base_count + random.uniform(-15, 25))
    
    def _get_average_speed(self, speed_limit: int, vehicle_count: int, is_rush_hour: bool) -> float:
        """
        Get average speed based on traffic conditions.
        
        Args:
            speed_limit: Speed limit for the road
            vehicle_count: Number of vehicles
            is_rush_hour: Whether it's rush hour
            
        Returns:
            Average speed in km/h
        """
        # Start with speed limit
        avg_speed = speed_limit
        
        # Reduce speed based on vehicle count
        if vehicle_count > 100:
            avg_speed *= 0.4  # Heavy traffic
        elif vehicle_count > 75:
            avg_speed *= 0.6  # Moderate traffic
        elif vehicle_count > 50:
            avg_speed *= 0.8  # Light traffic
        
        # Additional reduction during rush hour
        if is_rush_hour:
            avg_speed *= 0.7
        
        # Add some randomness
        avg_speed += random.uniform(-5, 5)
        
        # Ensure minimum speed
        return max(avg_speed, 5)
    
    def _get_traffic_conditions(self, vehicle_count: int, avg_speed: float, speed_limit: int) -> tuple:
        """
        Determine traffic density and congestion level.
        
        Args:
            vehicle_count: Number of vehicles
            avg_speed: Average speed
            speed_limit: Speed limit
            
        Returns:
            Tuple of (traffic_density, congestion_level)
        """
        speed_ratio = avg_speed / speed_limit
        
        # Determine traffic density
        if vehicle_count < 30:
            traffic_density = 'Low'
        elif vehicle_count < 60:
            traffic_density = 'Medium'
        elif vehicle_count < 100:
            traffic_density = 'High'
        else:
            traffic_density = 'Severe'
        
        # Determine congestion level based on speed ratio
        if speed_ratio > 0.8:
            congestion_level = 'Free Flow'
        elif speed_ratio > 0.5:
            congestion_level = 'Slow'
        elif speed_ratio > 0.2:
            congestion_level = 'Stop-and-Go'
        else:
            congestion_level = 'Gridlock'
        
        return traffic_density, congestion_level
    
    def _get_public_transport_delay(self, congestion_level: str, weather_condition: str) -> float:
        """
        Get public transport delay based on traffic and weather.
        
        Args:
            congestion_level: Current congestion level
            weather_condition: Weather condition
            
        Returns:
            Delay in minutes
        """
        base_delay = 0
        
        # Delay based on congestion
        if congestion_level == 'Slow':
            base_delay = 2
        elif congestion_level == 'Stop-and-Go':
            base_delay = 5
        elif congestion_level == 'Gridlock':
            base_delay = 12
        
        # Additional delay for bad weather
        if weather_condition in ['Rain', 'Snow', 'Storm']:
            base_delay += random.uniform(1, 5)
        elif weather_condition == 'Fog':
            base_delay += random.uniform(2, 8)
        
        return base_delay + random.uniform(0, 3)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'record_id': 'string',
            'timestamp': 'datetime',
            'sensor_id': 'string',
            'road_name': 'string',
            'city': 'string',
            'vehicle_count': 'integer',
            'avg_speed_kmh': 'float',
            'traffic_density': 'string',
            'congestion_level': 'string',
            'incident_flag': 'boolean',
            'incident_type': 'string',
            'travel_time_min': 'float',
            'weather_condition': 'string',
            'lane_closures': 'integer',
            'public_transport_delay_min': 'float'
        }