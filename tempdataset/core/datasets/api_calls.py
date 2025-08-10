"""
API calls dataset generator.

Generates realistic API call logs and metrics.
"""

import random
import json
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class ApiCallsDataset(BaseDataset):
    """API calls dataset generator for API usage analytics and monitoring."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._call_counter = 1
    
    def _init_data_lists(self) -> None:
        self.http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']
        
        self.api_endpoints = [
            '/api/v1/users', '/api/v1/users/{id}', '/api/v1/auth/login', '/api/v1/auth/logout',
            '/api/v1/orders', '/api/v1/orders/{id}', '/api/v1/products', '/api/v1/products/{id}',
            '/api/v1/customers', '/api/v1/customers/{id}', '/api/v1/payments', '/api/v1/payments/{id}',
            '/api/v1/inventory', '/api/v1/reports', '/api/v1/analytics', '/api/v1/settings',
            '/api/v2/users', '/api/v2/orders', '/api/v2/products', '/api/v2/customers',
            '/api/internal/health', '/api/internal/metrics', '/api/webhook/payment',
            '/api/webhook/shipping', '/api/admin/users', '/api/admin/system'
        ]
        
        self.status_codes = {
            200: 0.65,  # OK
            201: 0.10,  # Created
            400: 0.08,  # Bad Request
            401: 0.05,  # Unauthorized
            404: 0.04,  # Not Found
            500: 0.03,  # Internal Server Error
            403: 0.02,  # Forbidden
            429: 0.02,  # Too Many Requests
            502: 0.01   # Bad Gateway
        }
        
        self.error_messages = {
            400: ['Invalid request format', 'Missing required fields', 'Invalid parameter values'],
            401: ['Authentication failed', 'Invalid token', 'Token expired'],
            403: ['Access denied', 'Insufficient permissions', 'Resource forbidden'],
            404: ['Resource not found', 'Endpoint not found', 'User not found'],
            429: ['Rate limit exceeded', 'Too many requests', 'API quota exceeded'],
            500: ['Internal server error', 'Database connection failed', 'Service unavailable'],
            502: ['Bad gateway', 'Upstream server error', 'Proxy error']
        }
        
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36',
            'curl/7.68.0', 'PostmanRuntime/7.28.4', 'python-requests/2.28.1',
            'axios/0.27.2', 'okhttp/4.9.3', 'Go-http-client/1.1'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        # Basic call info
        call_id = f"API-2025-{self._call_counter:08d}"
        self._call_counter += 1
        
        # Timestamp - API calls are recent
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
        
        # API endpoint and method
        api_endpoint = random.choice(self.api_endpoints)
        
        # HTTP method distribution based on endpoint
        if '/auth/' in api_endpoint or api_endpoint.endswith('/{id}'):
            http_method = random.choices(
                ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                weights=[0.40, 0.25, 0.20, 0.10, 0.05]
            )[0]
        else:
            http_method = random.choices(
                ['GET', 'POST', 'PUT', 'DELETE', 'PATCH'],
                weights=[0.60, 0.20, 0.10, 0.05, 0.05]
            )[0]
        
        # Request payload size (larger for POST/PUT)
        if http_method in ['POST', 'PUT', 'PATCH']:
            request_payload_size = random.randint(100, 5000)
        else:
            request_payload_size = random.randint(0, 500)
        
        # Status code
        status_code = random.choices(
            list(self.status_codes.keys()),
            weights=list(self.status_codes.values())
        )[0]
        
        # Response payload size based on status code
        if status_code in [200, 201]:
            response_payload_size = random.randint(50, 10000)
        elif status_code in [400, 401, 403, 404]:
            response_payload_size = random.randint(50, 500)
        else:
            response_payload_size = random.randint(20, 200)
        
        # Response time - slower for errors and complex endpoints
        if status_code >= 500:
            response_time_ms = random.randint(5000, 30000)
        elif status_code >= 400:
            response_time_ms = random.randint(100, 2000)
        elif 'reports' in api_endpoint or 'analytics' in api_endpoint:
            response_time_ms = random.randint(1000, 8000)
        else:
            response_time_ms = random.randint(50, 1500)
        
        # Client IP
        client_ip = f"{random.randint(1, 223)}.{random.randint(1, 255)}.{random.randint(1, 255)}.{random.randint(1, 255)}"
        
        # Auth token used - most endpoints require auth
        auth_token_used = random.random() < 0.85
        
        # User ID - present when auth token is used
        if auth_token_used:
            user_id = f"USER-{random.randint(10000, 99999)}"
        else:
            user_id = None
        
        # Error message for error status codes
        if status_code >= 400:
            error_message = random.choice(self.error_messages.get(status_code, ['Unknown error']))
        else:
            error_message = None
        
        return {
            'call_id': call_id,
            'timestamp': timestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
            'api_endpoint': api_endpoint,
            'http_method': http_method,
            'request_payload_size': request_payload_size,
            'response_payload_size': response_payload_size,
            'status_code': status_code,
            'response_time_ms': response_time_ms,
            'client_ip': client_ip,
            'auth_token_used': auth_token_used,
            'user_id': user_id,
            'error_message': error_message
        }
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'call_id': 'string', 'timestamp': 'datetime', 'api_endpoint': 'string',
            'http_method': 'string', 'request_payload_size': 'integer',
            'response_payload_size': 'integer', 'status_code': 'integer',
            'response_time_ms': 'integer', 'client_ip': 'string',
            'auth_token_used': 'boolean', 'user_id': 'string', 'error_message': 'string'
        }
