"""
Industrial dataset generator.

Generates realistic industrial sensor data with machine monitoring metrics,
operational status, maintenance tracking, and predictive failure indicators.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class IndustrialDataset(BaseDataset):
    """
    Industrial dataset generator that creates realistic industrial sensor data.
    
    Generates industrial monitoring data including:
    - Sensor identification (sensor_reading_id, timestamp, machine_id, factory_id)
    - Location and operational status
    - Machine performance metrics (temperature, vibration, pressure, RPM)
    - Power consumption and oil levels
    - Fault detection and maintenance scheduling
    - Predictive failure analysis
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the IndustrialDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
        # Counter for sequential IDs
        self._reading_counter = 1
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Operating status options
        self.operating_statuses = ['Running', 'Idle', 'Maintenance', 'Fault']
        
        # Factory locations
        self.locations = [
            'Detroit, MI', 'Houston, TX', 'Chicago, IL', 'Los Angeles, CA',
            'Atlanta, GA', 'Phoenix, AZ', 'Cleveland, OH', 'Pittsburgh, PA',
            'Milwaukee, WI', 'Indianapolis, IN', 'Birmingham, AL', 'Buffalo, NY',
            'Memphis, TN', 'Louisville, KY', 'Nashville, TN', 'Charlotte, NC'
        ]
        
        # Common fault codes
        self.fault_codes = [
            'E001', 'E002', 'E003', 'E004', 'E005', 'E006', 'E007', 'E008',
            'W001', 'W002', 'W003', 'W004', 'W005',
            'M001', 'M002', 'M003', 'M004',
            'T001', 'T002', 'T003',
            'P001', 'P002', 'P003',
            'V001', 'V002', 'V003'
        ]
        
        # Machine types for ID generation
        self.machine_types = ['CNC', 'PUMP', 'MOTOR', 'CONV', 'PRESS', 'WELD', 'DRILL', 'MILL']
        
        # Factory types for ID generation
        self.factory_types = ['AUTO', 'STEEL', 'CHEM', 'FOOD', 'TEXT', 'ELEC', 'PHARM', 'AERO']
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate industrial dataset rows.
        
        Returns:
            List of dictionaries representing industrial sensor readings
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
        """Generate a single industrial sensor reading row."""
        
        # Generate timestamp (within last 7 days for recent monitoring)
        end_time = datetime.now()
        start_time = end_time - timedelta(days=7)
        date_part = self.faker_utils.date_between(start_time, end_time)
        # Convert date to datetime with random time
        timestamp = datetime.combine(date_part, datetime.min.time()) + timedelta(
            hours=random.randint(0, 23),
            minutes=random.randint(0, 59),
            seconds=random.randint(0, 59)
        )
        
        # Generate machine and factory IDs
        machine_id = self._generate_machine_id()
        factory_id = self._generate_factory_id()
        location = random.choice(self.locations)
        
        # Generate operating status
        operating_status = random.choice(self.operating_statuses)
        
        # Generate sensor readings based on operating status
        temperature_c, vibration_mm_s, pressure_bar, rpm, power_kw = self._get_sensor_readings(operating_status)
        
        # Generate oil level
        oil_level_percent = self._get_oil_level(operating_status)
        
        # Generate fault code (only if status is Fault)
        fault_code = random.choice(self.fault_codes) if operating_status == 'Fault' else None
        
        # Generate maintenance due date
        maintenance_due_date = self._get_maintenance_due_date(timestamp, operating_status)
        
        # Generate predictive failure flag based on sensor readings
        predicted_failure_flag = self._predict_failure(temperature_c, vibration_mm_s, pressure_bar, oil_level_percent)
        
        # Generate downtime (only for Maintenance or Fault status)
        if operating_status in ['Maintenance', 'Fault']:
            downtime_minutes = random.randint(30, 480)  # 30 minutes to 8 hours
        else:
            downtime_minutes = 0
        
        return {
            'sensor_reading_id': self._generate_reading_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'machine_id': machine_id,
            'factory_id': factory_id,
            'location': location,
            'operating_status': operating_status,
            'temperature_c': round(temperature_c, 1),
            'vibration_mm_s': round(vibration_mm_s, 2),
            'pressure_bar': round(pressure_bar, 1),
            'rpm': int(rpm),
            'power_kw': round(power_kw, 1),
            'oil_level_percent': round(oil_level_percent, 1),
            'fault_code': fault_code,
            'maintenance_due_date': maintenance_due_date.strftime('%Y-%m-%d'),
            'predicted_failure_flag': predicted_failure_flag,
            'downtime_minutes': downtime_minutes
        }
    
    def _generate_reading_id(self) -> str:
        """
        Generate sensor reading ID in format "IND-YYYY-NNNNNN".
        
        Returns:
            Formatted reading ID
        """
        year = datetime.now().year
        reading_num = str(self._reading_counter).zfill(6)
        self._reading_counter += 1
        return f"IND-{year}-{reading_num}"
    
    def _generate_machine_id(self) -> str:
        """
        Generate machine ID in format "MACH-TYPE-NNN".
        
        Returns:
            Formatted machine ID
        """
        machine_type = random.choice(self.machine_types)
        machine_num = random.randint(1, 999)
        return f"MACH-{machine_type}-{machine_num:03d}"
    
    def _generate_factory_id(self) -> str:
        """
        Generate factory ID in format "FAC-TYPE-NN".
        
        Returns:
            Formatted factory ID
        """
        factory_type = random.choice(self.factory_types)
        factory_num = random.randint(1, 99)
        return f"FAC-{factory_type}-{factory_num:02d}"
    
    def _get_sensor_readings(self, operating_status: str) -> tuple:
        """
        Get sensor readings based on operating status.
        
        Args:
            operating_status: Current operating status
            
        Returns:
            Tuple of (temperature, vibration, pressure, rpm, power)
        """
        if operating_status == 'Running':
            # Normal operating ranges
            temperature_c = random.uniform(60, 85)
            vibration_mm_s = random.uniform(2, 8)
            pressure_bar = random.uniform(5, 15)
            rpm = random.uniform(1200, 3000)
            power_kw = random.uniform(50, 200)
            
        elif operating_status == 'Idle':
            # Lower readings when idle
            temperature_c = random.uniform(25, 45)
            vibration_mm_s = random.uniform(0.5, 3)
            pressure_bar = random.uniform(1, 5)
            rpm = random.uniform(0, 500)
            power_kw = random.uniform(5, 25)
            
        elif operating_status == 'Maintenance':
            # Very low or zero readings during maintenance
            temperature_c = random.uniform(20, 35)
            vibration_mm_s = random.uniform(0, 1)
            pressure_bar = random.uniform(0, 2)
            rpm = 0
            power_kw = random.uniform(0, 5)
            
        else:  # Fault
            # Abnormal readings indicating problems
            temperature_c = random.uniform(90, 120)  # Overheating
            vibration_mm_s = random.uniform(15, 30)  # Excessive vibration
            pressure_bar = random.uniform(0.5, 3) if random.random() < 0.5 else random.uniform(20, 30)  # Too low or too high
            rpm = random.uniform(0, 4000)  # Erratic
            power_kw = random.uniform(0, 300)  # Erratic
        
        return temperature_c, vibration_mm_s, pressure_bar, rpm, power_kw
    
    def _get_oil_level(self, operating_status: str) -> float:
        """
        Get oil level based on operating status.
        
        Args:
            operating_status: Current operating status
            
        Returns:
            Oil level percentage
        """
        if operating_status == 'Running':
            return random.uniform(40, 100)
        elif operating_status == 'Idle':
            return random.uniform(30, 100)
        elif operating_status == 'Maintenance':
            return random.uniform(0, 100)  # Could be drained for maintenance
        else:  # Fault
            return random.uniform(0, 30)  # Low oil might cause faults
    
    def _get_maintenance_due_date(self, current_timestamp: datetime, operating_status: str) -> datetime:
        """
        Get maintenance due date based on current status.
        
        Args:
            current_timestamp: Current timestamp
            operating_status: Current operating status
            
        Returns:
            Maintenance due date
        """
        if operating_status == 'Maintenance':
            # If currently in maintenance, next maintenance is further out
            days_ahead = random.randint(60, 180)
        elif operating_status == 'Fault':
            # If faulty, maintenance is overdue or very soon
            days_ahead = random.randint(-30, 7)
        else:
            # Normal maintenance schedule
            days_ahead = random.randint(7, 90)
        
        return current_timestamp + timedelta(days=days_ahead)
    
    def _predict_failure(self, temperature: float, vibration: float, pressure: float, oil_level: float) -> bool:
        """
        Predict failure based on sensor readings.
        
        Args:
            temperature: Temperature reading
            vibration: Vibration reading
            pressure: Pressure reading
            oil_level: Oil level percentage
            
        Returns:
            True if failure is predicted
        """
        failure_score = 0
        
        # High temperature increases failure risk
        if temperature > 90:
            failure_score += 3
        elif temperature > 80:
            failure_score += 1
        
        # High vibration increases failure risk
        if vibration > 20:
            failure_score += 3
        elif vibration > 10:
            failure_score += 1
        
        # Abnormal pressure increases failure risk
        if pressure < 2 or pressure > 18:
            failure_score += 2
        
        # Low oil level increases failure risk
        if oil_level < 20:
            failure_score += 2
        elif oil_level < 40:
            failure_score += 1
        
        # Predict failure if score is high enough
        return failure_score >= 3
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'sensor_reading_id': 'string',
            'timestamp': 'datetime',
            'machine_id': 'string',
            'factory_id': 'string',
            'location': 'string',
            'operating_status': 'string',
            'temperature_c': 'float',
            'vibration_mm_s': 'float',
            'pressure_bar': 'float',
            'rpm': 'integer',
            'power_kw': 'float',
            'oil_level_percent': 'float',
            'fault_code': 'string',
            'maintenance_due_date': 'date',
            'predicted_failure_flag': 'boolean',
            'downtime_minutes': 'integer'
        }