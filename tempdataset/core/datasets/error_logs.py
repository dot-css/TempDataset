"""
Error logs dataset generator.

Generates realistic application error logs and stack traces.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class ErrorLogsDataset(BaseDataset):
    """Error logs dataset generator for application error tracking and debugging."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._error_counter = 1
    
    def _init_data_lists(self) -> None:
        self.error_types = [
            'NullPointerException', 'SQLException', 'TimeoutException', 'ValidationException',
            'AuthenticationException', 'FileNotFoundException', 'NetworkException',
            'OutOfMemoryError', 'IllegalArgumentException', 'ConcurrentModificationException',
            'JsonParseException', 'HttpClientException', 'DatabaseConnectionException',
            'ConfigurationException', 'SecurityException'
        ]
        
        self.error_severity = ['LOW', 'MEDIUM', 'HIGH', 'CRITICAL']
        
        self.applications = [
            'user-service', 'order-service', 'payment-service', 'inventory-service',
            'notification-service', 'auth-service', 'report-service', 'web-app',
            'mobile-api', 'admin-panel', 'analytics-service', 'file-service'
        ]
        
        self.error_messages = {
            'NullPointerException': [
                'Object reference not set to an instance of an object',
                'Attempted to access null object property',
                'Null pointer dereference in user data processing'
            ],
            'SQLException': [
                'Connection timeout to database server',
                'Syntax error in SQL query execution',
                'Foreign key constraint violation',
                'Table does not exist in database'
            ],
            'TimeoutException': [
                'Request timeout after 30 seconds',
                'Database query execution timeout',
                'External API call timeout',
                'Connection timeout to upstream service'
            ],
            'ValidationException': [
                'Invalid email format provided',
                'Required field missing in request',
                'Data validation failed for user input',
                'Invalid date format in request payload'
            ],
            'AuthenticationException': [
                'Invalid credentials provided',
                'JWT token has expired',
                'User account is locked or disabled',
                'Authentication token is malformed'
            ],
            'FileNotFoundException': [
                'Configuration file not found',
                'Template file missing from resources',
                'Log file cannot be accessed',
                'Upload file path does not exist'
            ],
            'NetworkException': [
                'Network connectivity lost',
                'DNS resolution failed',
                'Connection refused by remote host',
                'SSL handshake failed'
            ]
        }
        
        self.stack_traces = {
            'NullPointerException': [
                'at com.example.service.UserService.processUser(UserService.java:45)',
                'at com.example.controller.UserController.getUser(UserController.java:78)',
                'at com.example.util.DataProcessor.process(DataProcessor.java:123)'
            ],
            'SQLException': [
                'at java.sql.DriverManager.getConnection(DriverManager.java:664)',
                'at com.example.dao.UserDao.findById(UserDao.java:89)',
                'at org.hibernate.engine.jdbc.connections.internal.DriverConnectionCreator.makeConnection'
            ],
            'TimeoutException': [
                'at java.util.concurrent.FutureTask.get(FutureTask.java:205)',
                'at com.example.service.ExternalApiService.callApi(ExternalApiService.java:156)',
                'at okhttp3.internal.connection.RealConnection.connectSocket'
            ]
        }
        
        self.environments = ['production', 'staging', 'development']
        
        self.affected_users_ranges = [(0, 0), (1, 5), (6, 20), (21, 100), (101, 1000)]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic error info
        error_id = f"ERR-2025-{self._error_counter:08d}"
        self._error_counter += 1
        
        # Timestamp - errors occur more frequently during business hours
        timestamp = self.faker_utils.date_between(
            datetime.now() - timedelta(days=7),
            datetime.now()
        )
        
        # Weight towards business hours (9 AM - 6 PM)
        hour_weights = [0.02] * 9 + [0.08] * 9 + [0.04] * 6  # 24 hours
        hour = random.choices(range(24), weights=hour_weights)[0]
        
        timestamp = datetime.combine(
            timestamp,
            datetime.min.time().replace(
                hour=hour,
                minute=random.randint(0, 59),
                second=random.randint(0, 59),
                microsecond=random.randint(0, 999999)
            )
        )
        
        # Error details
        error_type = random.choice(self.error_types)
        application = random.choice(self.applications)
        environment = random.choices(
            self.environments,
            weights=[0.70, 0.20, 0.10]  # production, staging, development
        )[0]
        
        # Error message
        if error_type in self.error_messages:
            error_message = random.choice(self.error_messages[error_type])
        else:
            error_message = f"An unexpected {error_type.lower()} occurred"
        
        # Stack trace
        if error_type in self.stack_traces:
            stack_trace = random.choice(self.stack_traces[error_type])
        else:
            stack_trace = f"at com.example.service.{application.replace('-', '').title()}Service.process"
        
        # Severity based on error type and environment
        if error_type in ['OutOfMemoryError', 'DatabaseConnectionException'] or environment == 'production':
            severity = random.choices(
                self.error_severity,
                weights=[0.10, 0.20, 0.40, 0.30]  # LOW, MEDIUM, HIGH, CRITICAL
            )[0]
        else:
            severity = random.choices(
                self.error_severity,
                weights=[0.30, 0.40, 0.20, 0.10]  # LOW, MEDIUM, HIGH, CRITICAL
            )[0]
        
        # User context - some errors affect specific users
        user_id = f"USER-{random.randint(10000, 99999)}" if random.random() < 0.6 else None
        session_id = f"SESS-2025-{random.randint(10000000, 99999999)}" if user_id else None
        
        # Request info for web-related errors
        if 'service' in application or application in ['web-app', 'mobile-api']:
            request_url = random.choice([
                '/api/users/profile', '/api/orders/create', '/api/payments/process',
                '/api/auth/login', '/api/products/search', '/dashboard/reports'
            ])
            http_method = random.choice(['GET', 'POST', 'PUT', 'DELETE'])
        else:
            request_url = None
            http_method = None
        
        # Server info
        server_name = f"{application}-{random.randint(1, 3):02d}"
        
        # Resolution status
        resolution_status = random.choices(
            ['Open', 'In Progress', 'Resolved', 'Closed'],
            weights=[0.25, 0.15, 0.40, 0.20]
        )[0]
        
        # Affected users count based on severity
        if severity == 'CRITICAL':
            affected_users_min, affected_users_max = random.choice(self.affected_users_ranges[3:])
        elif severity == 'HIGH':
            affected_users_min, affected_users_max = random.choice(self.affected_users_ranges[2:4])
        elif severity == 'MEDIUM':
            affected_users_min, affected_users_max = random.choice(self.affected_users_ranges[1:3])
        else:  # LOW
            affected_users_min, affected_users_max = random.choice(self.affected_users_ranges[:2])
        
        affected_users_count = random.randint(affected_users_min, affected_users_max)
        
        # First occurrence flag
        first_occurrence = random.random() < 0.3
        
        return {
            'error_id': error_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'application': application,
            'environment': environment,
            'error_type': error_type,
            'severity': severity,
            'error_message': error_message,
            'stack_trace': stack_trace,
            'user_id': user_id,
            'session_id': session_id,
            'request_url': request_url,
            'http_method': http_method,
            'server_name': server_name,
            'resolution_status': resolution_status,
            'affected_users_count': affected_users_count,
            'first_occurrence': first_occurrence
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'error_id': 'string', 'timestamp': 'datetime', 'application': 'string',
            'environment': 'string', 'error_type': 'string', 'severity': 'string',
            'error_message': 'string', 'stack_trace': 'string', 'user_id': 'string',
            'session_id': 'string', 'request_url': 'string', 'http_method': 'string',
            'server_name': 'string', 'resolution_status': 'string',
            'affected_users_count': 'integer', 'first_occurrence': 'boolean'
        }
