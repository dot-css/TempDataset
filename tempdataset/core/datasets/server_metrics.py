"""
Server metrics dataset generator.

Generates realistic server performance metrics.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class ServerMetricsDataset(BaseDataset):
    """Server metrics dataset generator for system monitoring and performance analysis."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._metric_counter = 1
    
    def _init_data_lists(self) -> None:
        self.server_names = [
            'web-01', 'web-02', 'web-03', 'api-01', 'api-02', 'db-primary',
            'db-replica', 'cache-01', 'cache-02', 'lb-01', 'worker-01',
            'worker-02', 'monitor-01', 'backup-01'
        ]
        
        self.metric_types = [
            'cpu_usage', 'memory_usage', 'disk_usage', 'network_io',
            'disk_io', 'load_average', 'connection_count', 'response_time'
        ]
        
        self.server_environments = ['production', 'staging', 'development']
        
        self.datacenter_locations = [
            'us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1',
            'us-central-1', 'eu-central-1'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic metric info
        metric_id = f"METRIC-2025-{self._metric_counter:08d}"
        self._metric_counter += 1
        
        # Timestamp - metrics are recent and frequent
        timestamp = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1),
            datetime.now()
        )
        timestamp = datetime.combine(
            timestamp,
            datetime.min.time().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59)
            )
        )
        
        # Server info
        server_name = random.choice(self.server_names)
        environment = random.choice(self.server_environments)
        datacenter = random.choice(self.datacenter_locations)
        
        # CPU metrics
        cpu_usage = round(random.uniform(10.0, 95.0), 2)
        cpu_cores = random.choice([2, 4, 8, 16, 32])
        
        # Memory metrics (in GB)
        memory_total_gb = random.choice([8, 16, 32, 64, 128])
        memory_used_gb = round(memory_total_gb * random.uniform(0.2, 0.9), 2)
        memory_usage_percent = round((memory_used_gb / memory_total_gb) * 100, 2)
        
        # Disk metrics (in GB)
        disk_total_gb = random.choice([100, 250, 500, 1000, 2000])
        disk_used_gb = round(disk_total_gb * random.uniform(0.1, 0.8), 2)
        disk_usage_percent = round((disk_used_gb / disk_total_gb) * 100, 2)
        
        # Network metrics (in MB/s)
        network_in_mbps = round(random.uniform(0.1, 100.0), 2)
        network_out_mbps = round(random.uniform(0.1, 100.0), 2)
        
        # Load average (typical Unix load averages)
        load_average_1min = round(random.uniform(0.1, cpu_cores * 1.5), 2)
        load_average_5min = round(random.uniform(0.1, cpu_cores * 1.2), 2)
        load_average_15min = round(random.uniform(0.1, cpu_cores * 1.0), 2)
        
        # Connection metrics
        active_connections = random.randint(10, 1000)
        
        # Temperature (in Celsius) - higher for high CPU usage
        if cpu_usage > 80:
            temperature_celsius = round(random.uniform(65.0, 85.0), 1)
        elif cpu_usage > 60:
            temperature_celsius = round(random.uniform(50.0, 70.0), 1)
        else:
            temperature_celsius = round(random.uniform(35.0, 55.0), 1)
        
        # Uptime in hours
        uptime_hours = random.randint(1, 8760)  # Up to 1 year
        
        # Status based on various metrics
        if (cpu_usage > 90 or memory_usage_percent > 95 or 
            disk_usage_percent > 95 or temperature_celsius > 80):
            status = 'critical'
        elif (cpu_usage > 80 or memory_usage_percent > 85 or 
              disk_usage_percent > 85 or temperature_celsius > 70):
            status = 'warning'
        else:
            status = 'healthy'
        
        return {
            'metric_id': metric_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'server_name': server_name,
            'environment': environment,
            'datacenter': datacenter,
            'cpu_usage_percent': cpu_usage,
            'cpu_cores': cpu_cores,
            'memory_total_gb': memory_total_gb,
            'memory_used_gb': memory_used_gb,
            'memory_usage_percent': memory_usage_percent,
            'disk_total_gb': disk_total_gb,
            'disk_used_gb': disk_used_gb,
            'disk_usage_percent': disk_usage_percent,
            'network_in_mbps': network_in_mbps,
            'network_out_mbps': network_out_mbps,
            'load_average_1min': load_average_1min,
            'load_average_5min': load_average_5min,
            'load_average_15min': load_average_15min,
            'active_connections': active_connections,
            'temperature_celsius': temperature_celsius,
            'uptime_hours': uptime_hours,
            'status': status
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'metric_id': 'string', 'timestamp': 'datetime', 'server_name': 'string',
            'environment': 'string', 'datacenter': 'string', 'cpu_usage_percent': 'float',
            'cpu_cores': 'integer', 'memory_total_gb': 'integer', 'memory_used_gb': 'float',
            'memory_usage_percent': 'float', 'disk_total_gb': 'integer', 'disk_used_gb': 'float',
            'disk_usage_percent': 'float', 'network_in_mbps': 'float', 'network_out_mbps': 'float',
            'load_average_1min': 'float', 'load_average_5min': 'float', 'load_average_15min': 'float',
            'active_connections': 'integer', 'temperature_celsius': 'float', 'uptime_hours': 'integer',
            'status': 'string'
        }
