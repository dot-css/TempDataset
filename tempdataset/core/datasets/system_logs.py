"""
System logs dataset generator.

Generates realistic system log entries.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class SystemLogsDataset(BaseDataset):
    """System logs dataset generator for server and application logs."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._log_counter = 1
    
    def _init_data_lists(self) -> None:
        self.log_levels = ['INFO', 'WARN', 'ERROR', 'DEBUG']
        
        self.system_names = [
            'web-server-01', 'web-server-02', 'api-gateway', 'database-primary',
            'database-replica', 'cache-server', 'load-balancer', 'auth-service',
            'payment-service', 'notification-service', 'file-server', 'backup-server'
        ]
        
        self.service_names = [
            'nginx', 'apache', 'tomcat', 'mysql', 'postgresql', 'redis',
            'elasticsearch', 'rabbitmq', 'docker', 'kubernetes', 'jenkins',
            'grafana', 'prometheus', 'auth-api', 'user-service', 'order-service'
        ]
        
        self.log_messages = {
            'INFO': [
                'Service started successfully',
                'User logged in successfully',
                'Database connection established',
                'Cache cleared successfully',
                'Backup completed successfully',
                'Health check passed',
                'Configuration reloaded',
                'Request processed successfully',
                'File uploaded successfully',
                'Email sent successfully'
            ],
            'WARN': [
                'High memory usage detected',
                'Slow query detected',
                'Connection pool near capacity',
                'Disk space running low',
                'Certificate expiring soon',
                'Rate limit approaching',
                'Retry attempt failed',
                'Deprecated API usage detected',
                'Unusual traffic pattern detected',
                'Cache miss rate high'
            ],
            'ERROR': [
                'Database connection failed',
                'Authentication failed',
                'File not found',
                'Permission denied',
                'Network timeout occurred',
                'Service unavailable',
                'Invalid request format',
                'Payment processing failed',
                'Email delivery failed',
                'Backup failed'
            ],
            'DEBUG': [
                'Processing request payload',
                'Database query executed',
                'Cache lookup performed',
                'Validation check completed',
                'Configuration parameter loaded',
                'Memory allocation performed',
                'Thread pool status checked',
                'Security token validated',
                'API response formatted',
                'Cleanup operation completed'
            ]
        }
        
        self.event_codes = [
            'E001', 'E002', 'E003', 'W001', 'W002', 'I001', 'I002', 'D001', None
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic log info
        log_id = f"SYSLOG-2025-{self._log_counter:06d}"
        self._log_counter += 1
        
        # Timestamp - logs are recent
        timestamp = self.faker_utils.date_between(
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
        timestamp = datetime.combine(
            timestamp,
            datetime.min.time().replace(
                hour=random.randint(0, 23),
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
                microsecond=random.randint(0, 999999)
            )
        )
        
        # System and host info
        system_name = random.choice(self.system_names)
        host_ip = f"{random.randint(10, 192)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Log level distribution - INFO most common, ERROR least common
        log_level = random.choices(
            self.log_levels,
            weights=[0.60, 0.20, 0.10, 0.10]  # INFO, WARN, ERROR, DEBUG
        )[0]
        
        # Message based on log level
        message = random.choice(self.log_messages[log_level])
        
        # Process and thread IDs
        process_id = random.randint(1000, 99999)
        thread_id = random.randint(1, 999)
        
        # Service name
        service_name = random.choice(self.service_names)
        
        # Event code - more likely for WARN and ERROR
        if log_level in ['WARN', 'ERROR']:
            event_code = random.choice([code for code in self.event_codes if code is not None])
        else:
            event_code = random.choice(self.event_codes)  # Can be None
        
        # User ID - only some logs have user context
        user_id = f"USER-{random.randint(10000, 99999)}" if random.random() < 0.3 else None
        
        return {
            'log_id': log_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'system_name': system_name,
            'host_ip': host_ip,
            'log_level': log_level,
            'message': message,
            'process_id': process_id,
            'thread_id': thread_id,
            'service_name': service_name,
            'event_code': event_code,
            'user_id': user_id
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'log_id': 'string', 'timestamp': 'datetime', 'system_name': 'string',
            'host_ip': 'string', 'log_level': 'string', 'message': 'string',
            'process_id': 'integer', 'thread_id': 'integer', 'service_name': 'string',
            'event_code': 'string', 'user_id': 'string'
        }
