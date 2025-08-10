"""
Performance monitoring dataset generator.

Generates realistic application performance metrics.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class PerformanceDataset(BaseDataset):
    """Performance monitoring dataset generator for application performance tracking."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._metric_counter = 1
    
    def _init_data_lists(self) -> None:
        self.applications = [
            'web-frontend', 'user-service', 'order-service', 'payment-service',
            'inventory-service', 'notification-service', 'auth-service',
            'report-service', 'mobile-api', 'admin-panel', 'analytics-service'
        ]
        
        self.endpoints = {
            'web-frontend': ['/home', '/products', '/checkout', '/profile', '/search'],
            'user-service': ['/api/users', '/api/users/{id}', '/api/users/search', '/api/users/profile'],
            'order-service': ['/api/orders', '/api/orders/{id}', '/api/orders/status', '/api/orders/history'],
            'payment-service': ['/api/payments/process', '/api/payments/{id}', '/api/payments/refund'],
            'inventory-service': ['/api/inventory', '/api/inventory/check', '/api/inventory/update'],
            'notification-service': ['/api/notifications/send', '/api/notifications/{id}'],
            'auth-service': ['/api/auth/login', '/api/auth/logout', '/api/auth/refresh', '/api/auth/validate'],
            'report-service': ['/api/reports/sales', '/api/reports/users', '/api/reports/performance'],
            'mobile-api': ['/mobile/auth', '/mobile/products', '/mobile/orders', '/mobile/profile'],
            'admin-panel': ['/admin/dashboard', '/admin/users', '/admin/orders', '/admin/settings'],
            'analytics-service': ['/api/analytics/events', '/api/analytics/reports', '/api/analytics/metrics']
        }
        
        self.environments = ['production', 'staging', 'development']
        
        self.regions = ['us-east-1', 'us-west-2', 'eu-west-1', 'ap-southeast-1']
        
        self.performance_metrics = [
            'response_time', 'throughput', 'error_rate', 'cpu_usage',
            'memory_usage', 'database_query_time', 'cache_hit_rate'
        ]
        
        self.alert_types = ['SLA_BREACH', 'HIGH_ERROR_RATE', 'SLOW_RESPONSE', 'RESOURCE_USAGE']
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic metric info
        metric_id = f"PERF-2025-{self._metric_counter:08d}"
        self._metric_counter += 1
        
        # Timestamp - performance metrics collected frequently
        timestamp = self.faker_utils.date_between(
            datetime.now() - timedelta(days=7),
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
        
        # Application and endpoint
        application = random.choice(self.applications)
        endpoint = random.choice(self.endpoints[application])
        environment = random.choices(
            self.environments,
            weights=[0.70, 0.20, 0.10]  # production, staging, development
        )[0]
        region = random.choice(self.regions)
        
        # Performance metrics - realistic values based on application type
        if 'service' in application:
            # Microservices typically faster
            response_time_ms = random.randint(50, 2000)
            throughput_rps = random.randint(10, 500)
        elif application == 'web-frontend':
            # Frontend can be slower due to rendering
            response_time_ms = random.randint(200, 5000)
            throughput_rps = random.randint(20, 200)
        else:
            # Admin/reporting applications
            response_time_ms = random.randint(500, 10000)
            throughput_rps = random.randint(1, 50)
        
        # Error rate - lower for production
        if environment == 'production':
            error_rate_percent = round(random.uniform(0.0, 5.0), 2)
        else:
            error_rate_percent = round(random.uniform(0.0, 15.0), 2)
        
        # System resources
        cpu_usage_percent = round(random.uniform(5.0, 90.0), 2)
        memory_usage_percent = round(random.uniform(20.0, 85.0), 2)
        
        # Database performance
        database_query_time_ms = random.randint(10, 1000)
        database_connections = random.randint(5, 100)
        
        # Cache performance
        cache_hit_rate_percent = round(random.uniform(75.0, 99.0), 2)
        
        # Network metrics
        network_latency_ms = random.randint(1, 200)
        
        # Concurrent users
        concurrent_users = random.randint(1, 1000)
        
        # SLA metrics
        sla_target_ms = random.choice([500, 1000, 2000, 5000])
        sla_compliance = response_time_ms <= sla_target_ms
        
        # Availability
        uptime_percent = round(random.uniform(95.0, 100.0), 3)
        
        # Alert conditions
        alert_triggered = (
            response_time_ms > sla_target_ms or
            error_rate_percent > 5.0 or
            cpu_usage_percent > 80.0 or
            memory_usage_percent > 80.0
        )
        
        if alert_triggered:
            if response_time_ms > sla_target_ms:
                alert_type = 'SLOW_RESPONSE'
            elif error_rate_percent > 5.0:
                alert_type = 'HIGH_ERROR_RATE'
            elif cpu_usage_percent > 80.0 or memory_usage_percent > 80.0:
                alert_type = 'RESOURCE_USAGE'
            else:
                alert_type = random.choice(self.alert_types)
        else:
            alert_type = None
        
        # Performance score (0-100)
        performance_score = 100
        if response_time_ms > sla_target_ms:
            performance_score -= 20
        if error_rate_percent > 2.0:
            performance_score -= 15
        if cpu_usage_percent > 70.0:
            performance_score -= 10
        if memory_usage_percent > 70.0:
            performance_score -= 10
        if cache_hit_rate_percent < 85.0:
            performance_score -= 5
        
        performance_score = max(0, performance_score)
        
        return {
            'metric_id': metric_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'application': application,
            'endpoint': endpoint,
            'environment': environment,
            'region': region,
            'response_time_ms': response_time_ms,
            'throughput_rps': throughput_rps,
            'error_rate_percent': error_rate_percent,
            'cpu_usage_percent': cpu_usage_percent,
            'memory_usage_percent': memory_usage_percent,
            'database_query_time_ms': database_query_time_ms,
            'database_connections': database_connections,
            'cache_hit_rate_percent': cache_hit_rate_percent,
            'network_latency_ms': network_latency_ms,
            'concurrent_users': concurrent_users,
            'sla_target_ms': sla_target_ms,
            'sla_compliance': sla_compliance,
            'uptime_percent': uptime_percent,
            'alert_triggered': alert_triggered,
            'alert_type': alert_type,
            'performance_score': performance_score
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'metric_id': 'string', 'timestamp': 'datetime', 'application': 'string',
            'endpoint': 'string', 'environment': 'string', 'region': 'string',
            'response_time_ms': 'integer', 'throughput_rps': 'integer',
            'error_rate_percent': 'float', 'cpu_usage_percent': 'float',
            'memory_usage_percent': 'float', 'database_query_time_ms': 'integer',
            'database_connections': 'integer', 'cache_hit_rate_percent': 'float',
            'network_latency_ms': 'integer', 'concurrent_users': 'integer',
            'sla_target_ms': 'integer', 'sla_compliance': 'boolean',
            'uptime_percent': 'float', 'alert_triggered': 'boolean',
            'alert_type': 'string', 'performance_score': 'integer'
        }
