"""
Smart Home dataset generator.

Generates realistic smart home IoT device data with home automation events,
device status monitoring, environmental sensors, and security alerts.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class SmartHomeDataset(BaseDataset):
    """
    Smart Home dataset generator that creates realistic smart home IoT data.
    
    Generates smart home device data including:
    - Event identification (event_id, timestamp, home_id)
    - Device information (room, device_type, device_id)
    - Device status and environmental readings
    - Motion detection and security monitoring
    - Home automation triggers and alerts
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the SmartHomeDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._event_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Room types in a typical home
        self.rooms = [
            'Living Room', 'Kitchen', 'Master Bedroom', 'Bedroom 2', 'Bedroom 3',
            'Bathroom', 'Master Bathroom', 'Dining Room', 'Office', 'Garage',
            'Basement', 'Attic', 'Hallway', 'Entryway', 'Laundry Room'
        ]
        
        # Device types
        self.device_types = ['Thermostat', 'Camera', 'Light', 'Door Lock', 'Appliance']
        
        # Device status options
        self.device_statuses = ['On', 'Off', 'Standby', 'Open', 'Closed']
        
        # Security alert types
        self.alert_types = [
            'Motion Detected', 'Door/Window Opened', 'Unusual Activity',
            'System Armed', 'System Disarmed', 'Low Battery', 'Device Offline'
        ]
        
        # Automation triggers
        self.automation_triggers = [
            'Schedule', 'Motion', 'Temperature', 'Time', 'Geofence',
            'Voice Command', 'App Control', 'Sensor', 'Security Event'
        ]
        
        # Specific devices by type
        self.specific_devices = {
            'Thermostat': ['Nest Thermostat', 'Ecobee Smart', 'Honeywell T9', 'Emerson Sensi'],
            'Camera': ['Ring Indoor Cam', 'Arlo Pro', 'Wyze Cam', 'Nest Cam'],
            'Light': ['Philips Hue', 'LIFX Bulb', 'Smart Switch', 'LED Strip'],
            'Door Lock': ['August Smart Lock', 'Yale Assure', 'Schlage Encode', 'Kwikset Halo'],
            'Appliance': ['Smart Fridge', 'Smart Oven', 'Robot Vacuum', 'Smart Washer', 'Smart Dryer', 'Smart Dishwasher']
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate smart home dataset rows.
        
        Returns:
            List of dictionaries representing smart home device events
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
        """Generate a single smart home device event row."""
        
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
        
        # Generate home and room
        home_id = self._generate_home_id()
        room = random.choice(self.rooms)
        
        # Generate device information
        device_type = random.choice(self.device_types)
        device_id = self._generate_device_id(device_type)
        
        # Generate device status based on type and time
        status = self._get_device_status(device_type, timestamp)
        
        # Generate environmental readings
        temperature_c, humidity_percent = self._get_environmental_readings(room, timestamp)
        
        # Generate energy usage based on device type and status
        energy_usage_kwh = self._get_energy_usage(device_type, status)
        
        # Generate motion detection (higher probability in certain rooms and times)
        motion_detected = self._get_motion_detection(room, timestamp)
        
        # Generate door/window status
        door_window_open = self._get_door_window_status(room, device_type)
        
        # Generate light level
        light_level_lux = self._get_light_level(room, timestamp)
        
        # Generate security alert (5% chance)
        security_alert_flag = random.random() < 0.05
        alert_type = random.choice(self.alert_types) if security_alert_flag else None
        
        # Generate automation trigger (30% chance of automated event)
        automation_trigger = random.choice(self.automation_triggers) if random.random() < 0.30 else None
        
        return {
            'event_id': self._generate_event_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'home_id': home_id,
            'room': room,
            'device_type': device_type,
            'device_id': device_id,
            'status': status,
            'temperature_c': round(temperature_c, 1),
            'humidity_percent': round(humidity_percent, 1),
            'energy_usage_kwh': round(energy_usage_kwh, 3),
            'motion_detected': motion_detected,
            'door_window_open': door_window_open,
            'light_level_lux': round(light_level_lux, 1),
            'security_alert_flag': security_alert_flag,
            'alert_type': alert_type,
            'automation_trigger': automation_trigger
        }
    
    def _generate_event_id(self) -> str:
        """
        Generate event ID in format "SMH-YYYY-NNNNNN".
        
        Returns:
            Formatted event ID
        """
        year = datetime.now().year
        event_num = str(self._event_counter).zfill(6)
        self._event_counter += 1
        return f"SMH-{year}-{event_num}"
    
    def _generate_home_id(self) -> str:
        """
        Generate home ID in format "HOME-NNNN".
        
        Returns:
            Formatted home ID
        """
        home_num = random.randint(1, 9999)
        return f"HOME-{home_num:04d}"
    
    def _generate_device_id(self, device_type: str) -> str:
        """
        Generate device ID based on device type.
        
        Args:
            device_type: Type of device
            
        Returns:
            Formatted device ID
        """
        type_code = device_type[:3].upper()
        device_num = random.randint(1, 999)
        return f"DEV-{type_code}-{device_num:03d}"
    
    def _get_device_status(self, device_type: str, timestamp: datetime) -> str:
        """
        Get device status based on type and time.
        
        Args:
            device_type: Type of device
            timestamp: Current timestamp
            
        Returns:
            Device status
        """
        hour = timestamp.hour
        
        if device_type == 'Light':
            # Lights more likely to be on during evening/night
            if 18 <= hour <= 23 or 6 <= hour <= 8:
                return random.choice(['On', 'On', 'On', 'Off'])  # 75% on
            else:
                return random.choice(['On', 'Off', 'Off', 'Off'])  # 25% on
        
        elif device_type == 'Thermostat':
            # Thermostats are usually always on, but may be in different modes
            return random.choice(['On', 'On', 'On', 'Standby'])
        
        elif device_type == 'Camera':
            # Cameras usually always on for security
            return random.choice(['On', 'On', 'On', 'Standby'])
        
        elif device_type == 'Door Lock':
            # Doors can be open or closed
            return random.choice(['Open', 'Closed', 'Closed', 'Closed'])  # Usually closed
        
        elif device_type == 'Appliance':
            # Appliances vary by time of day
            if 6 <= hour <= 9 or 17 <= hour <= 21:  # Morning and evening
                return random.choice(['On', 'On', 'Off', 'Standby'])
            else:
                return random.choice(['On', 'Off', 'Off', 'Standby'])
        
        return random.choice(self.device_statuses)
    
    def _get_environmental_readings(self, room: str, timestamp: datetime) -> tuple:
        """
        Get temperature and humidity readings based on room and time.
        
        Args:
            room: Room name
            timestamp: Current timestamp
            
        Returns:
            Tuple of (temperature, humidity)
        """
        hour = timestamp.hour
        month = timestamp.month
        
        # Base temperature varies by room
        if room in ['Kitchen', 'Laundry Room']:
            base_temp = 24  # Warmer due to appliances
        elif room in ['Basement', 'Garage']:
            base_temp = 18  # Cooler
        elif room in ['Bathroom', 'Master Bathroom']:
            base_temp = 23  # Slightly warmer
        else:
            base_temp = 21  # Standard room temperature
        
        # Seasonal adjustment
        if month in [12, 1, 2]:  # Winter
            base_temp -= 2
        elif month in [6, 7, 8]:  # Summer
            base_temp += 2
        
        # Daily variation
        if 14 <= hour <= 16:  # Afternoon peak
            base_temp += 1
        elif 3 <= hour <= 6:  # Early morning low
            base_temp -= 1
        
        temperature_c = base_temp + random.uniform(-2, 2)
        
        # Humidity varies by room
        if room in ['Bathroom', 'Master Bathroom']:
            humidity_percent = random.uniform(50, 80)  # Higher humidity
        elif room in ['Kitchen', 'Laundry Room']:
            humidity_percent = random.uniform(45, 70)
        else:
            humidity_percent = random.uniform(35, 60)
        
        return temperature_c, humidity_percent
    
    def _get_energy_usage(self, device_type: str, status: str) -> float:
        """
        Get energy usage based on device type and status.
        
        Args:
            device_type: Type of device
            status: Current device status
            
        Returns:
            Energy usage in kWh
        """
        if status in ['Off', 'Closed']:
            return random.uniform(0, 0.001)  # Minimal standby power
        
        # Energy usage by device type (per hour)
        energy_ranges = {
            'Thermostat': (0.002, 0.005),  # Very low, just controls
            'Camera': (0.005, 0.015),      # Low power devices
            'Light': (0.008, 0.060),       # LED to incandescent range
            'Door Lock': (0.001, 0.003),   # Very low power
            'Appliance': (0.100, 2.000)    # Wide range depending on appliance
        }
        
        min_usage, max_usage = energy_ranges.get(device_type, (0.005, 0.050))
        
        if status == 'Standby':
            # Standby uses less power
            return random.uniform(min_usage * 0.1, min_usage * 0.3)
        else:
            return random.uniform(min_usage, max_usage)
    
    def _get_motion_detection(self, room: str, timestamp: datetime) -> bool:
        """
        Get motion detection based on room and time.
        
        Args:
            room: Room name
            timestamp: Current timestamp
            
        Returns:
            True if motion detected
        """
        hour = timestamp.hour
        
        # Higher probability of motion during active hours
        if 6 <= hour <= 23:
            base_probability = 0.3
        else:
            base_probability = 0.05  # Low probability at night
        
        # Adjust by room type
        if room in ['Living Room', 'Kitchen']:
            base_probability *= 1.5  # More active rooms
        elif room in ['Bedroom 2', 'Bedroom 3', 'Office']:
            base_probability *= 0.7  # Less active rooms
        elif room in ['Garage', 'Basement', 'Attic']:
            base_probability *= 0.3  # Rarely used rooms
        
        return random.random() < base_probability
    
    def _get_door_window_status(self, room: str, device_type: str) -> bool:
        """
        Get door/window open status.
        
        Args:
            room: Room name
            device_type: Type of device
            
        Returns:
            True if door/window is open
        """
        if device_type == 'Door Lock':
            # Doors are usually closed
            return random.random() < 0.1
        
        # For other devices, simulate window sensors
        if room in ['Living Room', 'Bedroom 2', 'Bedroom 3', 'Master Bedroom']:
            # Rooms with windows
            return random.random() < 0.15
        else:
            # Rooms without windows or rarely opened
            return random.random() < 0.05
    
    def _get_light_level(self, room: str, timestamp: datetime) -> float:
        """
        Get light level based on room and time.
        
        Args:
            room: Room name
            timestamp: Current timestamp
            
        Returns:
            Light level in lux
        """
        hour = timestamp.hour
        
        # Base light level by time of day
        if 6 <= hour <= 8:  # Dawn
            base_lux = 100
        elif 9 <= hour <= 17:  # Daytime
            base_lux = 500
        elif 18 <= hour <= 20:  # Dusk
            base_lux = 200
        else:  # Night
            base_lux = 10
        
        # Adjust by room (some rooms have less natural light)
        if room in ['Basement', 'Garage', 'Bathroom']:
            base_lux *= 0.3  # Less natural light
        elif room in ['Living Room', 'Kitchen']:
            base_lux *= 1.2  # More windows/artificial light
        
        return base_lux + random.uniform(-base_lux * 0.3, base_lux * 0.5)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'event_id': 'string',
            'timestamp': 'datetime',
            'home_id': 'string',
            'room': 'string',
            'device_type': 'string',
            'device_id': 'string',
            'status': 'string',
            'temperature_c': 'float',
            'humidity_percent': 'float',
            'energy_usage_kwh': 'float',
            'motion_detected': 'boolean',
            'door_window_open': 'boolean',
            'light_level_lux': 'float',
            'security_alert_flag': 'boolean',
            'alert_type': 'string',
            'automation_trigger': 'string'
        }