"""
Energy dataset generator.

Generates realistic energy consumption and production data with smart meter readings
including electricity, gas, solar, and wind energy sources.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class EnergyDataset(BaseDataset):
    """
    Energy dataset generator that creates realistic energy meter data.
    
    Generates energy consumption and production data including:
    - Reading identification (reading_id, timestamp, meter_id)
    - Location and energy source information
    - Consumption and production metrics
    - Cost calculations and tariff plans
    - Peak demand and outage tracking
    - CO2 emissions calculations
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the EnergyDataset generator.
        
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
        
        # Energy sources
        self.energy_sources = ['Electricity', 'Gas', 'Solar', 'Wind']
        
        # Tariff plans
        self.tariff_plans = ['Standard', 'Time-of-Use', 'Peak/Off-Peak']
        
        # US states and cities
        self.locations = [
            'New York, NY', 'Los Angeles, CA', 'Chicago, IL', 'Houston, TX',
            'Phoenix, AZ', 'Philadelphia, PA', 'San Antonio, TX', 'San Diego, CA',
            'Dallas, TX', 'San Jose, CA', 'Austin, TX', 'Jacksonville, FL',
            'Fort Worth, TX', 'Columbus, OH', 'Charlotte, NC', 'San Francisco, CA',
            'Indianapolis, IN', 'Seattle, WA', 'Denver, CO', 'Washington, DC'
        ]
        
        # CO2 emission factors (kg CO2 per kWh) by energy source
        self.co2_factors = {
            'Electricity': 0.4,  # Grid average
            'Gas': 0.2,
            'Solar': 0.0,
            'Wind': 0.0
        }
        
        # Typical tariff rates (USD per kWh) by plan
        self.tariff_rates = {
            'Standard': 0.12,
            'Time-of-Use': {'peak': 0.18, 'off_peak': 0.08},
            'Peak/Off-Peak': {'peak': 0.20, 'off_peak': 0.06}
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate energy dataset rows.
        
        Returns:
            List of dictionaries representing energy meter readings
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
        """Generate a single energy meter reading row."""
        
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
        
        # Select energy source and location
        energy_source = random.choice(self.energy_sources)
        location = random.choice(self.locations)
        
        # Generate consumption based on energy source and time
        consumption_kwh = self._get_consumption(energy_source, timestamp)
        
        # Generate production (mainly for renewable sources)
        production_kwh = self._get_production(energy_source, timestamp)
        
        # Calculate net usage
        net_usage_kwh = consumption_kwh - production_kwh
        
        # Select tariff plan and calculate cost
        tariff_plan = random.choice(self.tariff_plans)
        cost_usd = self._calculate_cost(consumption_kwh, tariff_plan, timestamp)
        
        # Generate peak demand
        peak_demand_kw = consumption_kwh * random.uniform(0.8, 1.5)
        
        # Generate outage data (5% chance of outage)
        outage_flag = random.random() < 0.05
        outage_duration_min = random.randint(5, 240) if outage_flag else 0
        
        # Calculate CO2 emissions
        co2_emissions_kg = consumption_kwh * self.co2_factors[energy_source]
        
        return {
            'reading_id': self._generate_reading_id(),
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'meter_id': self._generate_meter_id(),
            'location': location,
            'energy_source': energy_source,
            'consumption_kwh': round(consumption_kwh, 2),
            'production_kwh': round(production_kwh, 2),
            'net_usage_kwh': round(net_usage_kwh, 2),
            'cost_usd': round(cost_usd, 2),
            'tariff_plan': tariff_plan,
            'peak_demand_kw': round(peak_demand_kw, 2),
            'outage_flag': outage_flag,
            'outage_duration_min': outage_duration_min,
            'co2_emissions_kg': round(co2_emissions_kg, 3)
        }
    
    def _generate_reading_id(self) -> str:
        """
        Generate reading ID in format "ENG-YYYY-NNNNNN".
        
        Returns:
            Formatted reading ID
        """
        year = datetime.now().year
        reading_num = str(self._reading_counter).zfill(6)
        self._reading_counter += 1
        return f"ENG-{year}-{reading_num}"
    
    def _generate_meter_id(self) -> str:
        """
        Generate meter ID in format "MTR-AAANNN".
        
        Returns:
            Formatted meter ID
        """
        letters = ''.join(random.choices(string.ascii_uppercase, k=3))
        numbers = ''.join(random.choices(string.digits, k=3))
        return f"MTR-{letters}{numbers}"
    
    def _get_consumption(self, energy_source: str, timestamp: datetime) -> float:
        """
        Get energy consumption based on source and time.
        
        Args:
            energy_source: Type of energy source
            timestamp: Current timestamp
            
        Returns:
            Energy consumption in kWh
        """
        hour = timestamp.hour
        month = timestamp.month
        
        # Base consumption patterns
        if energy_source == 'Electricity':
            # Higher consumption during peak hours and summer/winter
            base_consumption = 25
            if hour in [7, 8, 9, 17, 18, 19, 20]:  # Peak hours
                base_consumption *= 1.5
            if month in [6, 7, 8, 12, 1, 2]:  # Summer/Winter
                base_consumption *= 1.3
            return base_consumption + random.uniform(-5, 10)
        
        elif energy_source == 'Gas':
            # Higher in winter months
            base_consumption = 15
            if month in [11, 12, 1, 2, 3]:  # Winter
                base_consumption *= 2
            return base_consumption + random.uniform(-3, 8)
        
        elif energy_source in ['Solar', 'Wind']:
            # Lower consumption as these are mainly production sources
            return random.uniform(2, 8)
        
        return random.uniform(10, 30)
    
    def _get_production(self, energy_source: str, timestamp: datetime) -> float:
        """
        Get energy production based on source and time.
        
        Args:
            energy_source: Type of energy source
            timestamp: Current timestamp
            
        Returns:
            Energy production in kWh
        """
        hour = timestamp.hour
        month = timestamp.month
        
        if energy_source == 'Solar':
            # Production only during daylight hours
            if 6 <= hour <= 18:
                # Peak production around noon
                if 10 <= hour <= 14:
                    base_production = 20
                else:
                    base_production = 10
                
                # Higher production in summer
                if month in [5, 6, 7, 8, 9]:
                    base_production *= 1.4
                
                return base_production + random.uniform(-3, 5)
            else:
                return 0.0
        
        elif energy_source == 'Wind':
            # Variable production throughout the day
            base_production = 12
            # Higher production in winter and spring
            if month in [11, 12, 1, 2, 3, 4]:
                base_production *= 1.3
            return base_production + random.uniform(-5, 8)
        
        else:
            # Electricity and Gas don't typically produce energy
            return 0.0
    
    def _calculate_cost(self, consumption_kwh: float, tariff_plan: str, timestamp: datetime) -> float:
        """
        Calculate energy cost based on consumption and tariff plan.
        
        Args:
            consumption_kwh: Energy consumption
            tariff_plan: Tariff plan type
            timestamp: Current timestamp
            
        Returns:
            Cost in USD
        """
        hour = timestamp.hour
        
        if tariff_plan == 'Standard':
            return consumption_kwh * self.tariff_rates['Standard']
        
        elif tariff_plan == 'Time-of-Use':
            # Peak hours: 7-9 AM, 5-8 PM
            if hour in [7, 8, 9, 17, 18, 19, 20]:
                rate = self.tariff_rates['Time-of-Use']['peak']
            else:
                rate = self.tariff_rates['Time-of-Use']['off_peak']
            return consumption_kwh * rate
        
        elif tariff_plan == 'Peak/Off-Peak':
            # Peak hours: 6-10 AM, 4-9 PM
            if hour in [6, 7, 8, 9, 10, 16, 17, 18, 19, 20, 21]:
                rate = self.tariff_rates['Peak/Off-Peak']['peak']
            else:
                rate = self.tariff_rates['Peak/Off-Peak']['off_peak']
            return consumption_kwh * rate
        
        return consumption_kwh * 0.12  # Default rate
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'reading_id': 'string',
            'timestamp': 'datetime',
            'meter_id': 'string',
            'location': 'string',
            'energy_source': 'string',
            'consumption_kwh': 'float',
            'production_kwh': 'float',
            'net_usage_kwh': 'float',
            'cost_usd': 'float',
            'tariff_plan': 'string',
            'peak_demand_kw': 'float',
            'outage_flag': 'boolean',
            'outage_duration_min': 'integer',
            'co2_emissions_kg': 'float'
        }