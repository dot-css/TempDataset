"""
TempDataset Library - Generate temporary datasets for testing and development.

A lightweight Python library for generating realistic sample data without heavy dependencies.
"""

from .core.generator import DataGenerator
from .core.utils.data_frame import TempDataFrame
from .core.io.csv_handler import read_csv as _read_csv
from .core.io.json_handler import read_json as _read_json
from .core.datasets.crm import CrmDataset
from .core.datasets.customers import CustomersDataset
from .core.datasets.ecommerce import EcommerceDataset
from .core.datasets.employees import EmployeesDataset
from .core.datasets.inventory import InventoryDataset
from .core.datasets.marketing import MarketingDataset
from .core.datasets.retail import RetailDataset
from .core.datasets.reviews import ReviewsDataset
from .core.datasets.sales import SalesDataset
from .core.datasets.suppliers import SuppliersDataset
# Financial datasets
from .core.datasets.stocks import StocksDataset
from .core.datasets.banking import BankingDataset
from .core.datasets.cryptocurrency import CryptocurrencyDataset
from .core.datasets.insurance import InsuranceDataset
from .core.datasets.loans import LoansDataset
from .core.datasets.investments import InvestmentsDataset
from .core.datasets.accounting import AccountingDataset
from .core.datasets.payments import PaymentsDataset
# IoT Sensor datasets
from .core.datasets.weather import WeatherDataset
from .core.datasets.energy import EnergyDataset
from .core.datasets.traffic import TrafficDataset
from .core.datasets.environmental import EnvironmentalDataset
from .core.datasets.industrial import IndustrialDataset
from .core.datasets.smarthome import SmartHomeDataset
# Healthcare datasets
from .core.datasets.patients import PatientsDataset
from .core.datasets.appointments import AppointmentsDataset
from .core.datasets.lab_results import LabResultsDataset
from .core.datasets.prescriptions import PrescriptionsDataset
from .core.datasets.medical_history import MedicalHistoryDataset
from .core.datasets.clinical_trials import ClinicalTrialsDataset
# Social datasets
from .core.datasets.social_media import SocialMediaDataset
from .core.datasets.user_profiles import UserProfilesDataset
# Technology datasets
from .core.datasets.web_analytics import WebAnalyticsDataset
from .core.datasets.app_usage import AppUsageDataset
from .core.datasets.system_logs import SystemLogsDataset
from .core.datasets.api_calls import ApiCallsDataset
from .core.datasets.server_metrics import ServerMetricsDataset
from .core.datasets.user_sessions import UserSessionsDataset
from .core.datasets.error_logs import ErrorLogsDataset
from .core.datasets.performance import PerformanceDataset
from .core.exceptions import (
    TempDatasetError, DatasetNotFoundError, DataGenerationError,
    ValidationError, CSVReadError, CSVWriteError, JSONReadError, JSONWriteError,
    FileOperationError, MemoryError as TempDatasetMemoryError
)

# Initialize the main generator
_generator = DataGenerator()

# Register available datasets
_generator.register_dataset('crm', CrmDataset)
_generator.register_dataset('customers', CustomersDataset)
_generator.register_dataset('ecommerce', EcommerceDataset)
_generator.register_dataset('employees', EmployeesDataset)
_generator.register_dataset('inventory', InventoryDataset)
_generator.register_dataset('marketing', MarketingDataset)
_generator.register_dataset('retail', RetailDataset)
_generator.register_dataset('reviews', ReviewsDataset)
_generator.register_dataset('sales', SalesDataset)
_generator.register_dataset('suppliers', SuppliersDataset)
# Register financial datasets
_generator.register_dataset('stocks', StocksDataset)
_generator.register_dataset('banking', BankingDataset)
_generator.register_dataset('cryptocurrency', CryptocurrencyDataset)
_generator.register_dataset('insurance', InsuranceDataset)
_generator.register_dataset('loans', LoansDataset)
_generator.register_dataset('investments', InvestmentsDataset)
_generator.register_dataset('accounting', AccountingDataset)
_generator.register_dataset('payments', PaymentsDataset)
# Register IoT sensor datasets
_generator.register_dataset('weather', WeatherDataset)
_generator.register_dataset('energy', EnergyDataset)
_generator.register_dataset('traffic', TrafficDataset)
_generator.register_dataset('environmental', EnvironmentalDataset)
_generator.register_dataset('industrial', IndustrialDataset)
_generator.register_dataset('smarthome', SmartHomeDataset)
# Register healthcare datasets
_generator.register_dataset('patients', PatientsDataset)
_generator.register_dataset('appointments', AppointmentsDataset)
_generator.register_dataset('lab_results', LabResultsDataset)
_generator.register_dataset('prescriptions', PrescriptionsDataset)
_generator.register_dataset('medical_history', MedicalHistoryDataset)
_generator.register_dataset('clinical_trials', ClinicalTrialsDataset)
# Register social datasets
_generator.register_dataset('social_media', SocialMediaDataset)
_generator.register_dataset('user_profiles', UserProfilesDataset)
# Register technology datasets
_generator.register_dataset('web_analytics', WebAnalyticsDataset)
_generator.register_dataset('app_usage', AppUsageDataset)
_generator.register_dataset('system_logs', SystemLogsDataset)
_generator.register_dataset('api_calls', ApiCallsDataset)
_generator.register_dataset('server_metrics', ServerMetricsDataset)
_generator.register_dataset('user_sessions', UserSessionsDataset)
_generator.register_dataset('error_logs', ErrorLogsDataset)
_generator.register_dataset('performance', PerformanceDataset)

def create_dataset(dataset_type: str, rows: int = 500):
    """
    Generate temporary datasets or save to files.
    
    Args:
        dataset_type: Dataset type or filename
            Available types: 'crm', 'customers', 'ecommerce', 'employees', 'inventory', 
            'marketing', 'retail', 'reviews', 'sales', 'suppliers', 'stocks', 'banking', 
            'cryptocurrency', 'insurance', 'loans', 'investments', 'accounting', 'payments',
            'weather', 'energy', 'traffic', 'environmental', 'industrial', 'smarthome',
            'patients', 'appointments', 'lab_results', 'prescriptions', 'medical_history', 'clinical_trials',
            'social_media', 'user_profiles', 'web_analytics', 'app_usage', 'system_logs', 'api_calls', 
            'server_metrics', 'user_sessions', 'error_logs', 'performance'
            Or filename with extension: 'data.csv', 'data.json'
        rows: Number of rows to generate (default: 500)
        
    Returns:
        TempDataFrame containing the generated data (also saves to file if filename provided)
        
    Raises:
        ValidationError: If parameters are invalid
        DatasetNotFoundError: If dataset type is not available
        DataGenerationError: If data generation fails
        TempDatasetMemoryError: If memory limits are exceeded
        CSVWriteError: If CSV file writing fails
        JSONWriteError: If JSON file writing fails
    """
    # Use the generator's validation and error handling
    return _generator.generate(dataset_type, rows)


def read_csv(filename: str) -> TempDataFrame:
    """
    Read CSV file into TempDataFrame.
    
    Args:
        filename: Path to CSV file
        
    Returns:
        TempDataFrame containing the CSV data
        
    Raises:
        ValidationError: If parameters are invalid
        CSVReadError: If the CSV file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.csv'):
        raise ValidationError("filename", filename, "filename with .csv extension")
    
    # Use the CSV handler's validation and error handling
    return _read_csv(filename)


def read_json(filename: str) -> TempDataFrame:
    """
    Read JSON file into TempDataFrame.
    
    Args:
        filename: Path to JSON file
        
    Returns:
        TempDataFrame containing the JSON data
        
    Raises:
        ValidationError: If parameters are invalid
        JSONReadError: If the JSON file is malformed or cannot be read
    """
    # Validate file extension
    if not isinstance(filename, str):
        raise ValidationError("filename", filename, "string")
    
    if not filename.strip():
        raise ValidationError("filename", filename, "non-empty string")
    
    if not filename.lower().endswith('.json'):
        raise ValidationError("filename", filename, "filename with .json extension")
    
    # Use the JSON handler's validation and error handling
    return _read_json(filename)


def help():
    """Display help information about TempDataset usage."""
    print("""
TempDataset - Generate Realistic Test Data
==========================================

Quick Examples:
  import tempdataset
  
  # Generate datasets
  data = tempdataset.create_dataset('sales', 1000)
  customers = tempdataset.create_dataset('customers', 500)
  
  # Save to files
  tempdataset.create_dataset('data.csv', 1000)
  tempdataset.create_dataset('data.json', 500)

Available Functions:
  tempdataset.list_datasets()     - Show all available datasets
  tempdataset.help()             - Show this help
  tempdataset.create_dataset()   - Generate datasets

For complete documentation: https://github.com/dot-css/TempDataset
""")


def list_datasets():
    """List all available datasets with their names only."""
    datasets = {
        # Core Business (10)
        'crm': 'Customer relationship management',
        'customers': 'Customer profiles and demographics',
        'ecommerce': 'E-commerce transactions', 
        'employees': 'Employee records and HR data',
        'inventory': 'Inventory and warehouse data',
        'marketing': 'Marketing campaigns and metrics',
        'retail': 'Retail store operations',
        'reviews': 'Product and service reviews',
        'sales': 'Sales transactions and orders',
        'suppliers': 'Supplier management data',
        
        # Financial (8)
        'stocks': 'Stock market trading data',
        'banking': 'Banking transactions',
        'cryptocurrency': 'Cryptocurrency trading',
        'insurance': 'Insurance policies and claims',
        'loans': 'Loan applications and management',
        'investments': 'Investment portfolios',
        'accounting': 'General ledger and accounting',
        'payments': 'Digital payment processing',
        
        # IoT Sensors (6)
        'weather': 'Weather sensor monitoring',
        'energy': 'Smart meter energy data',
        'traffic': 'Traffic sensor monitoring',
        'environmental': 'Environmental monitoring',
        'industrial': 'Industrial sensor data',
        'smarthome': 'Smart home IoT devices',
        
        # Healthcare (6)
        'patients': 'Patient medical records',
        'appointments': 'Medical appointments',
        'lab_results': 'Laboratory test results',
        'prescriptions': 'Medication prescriptions',
        'medical_history': 'Patient medical history',
        'clinical_trials': 'Clinical trial data',
        
        # Social Media (2)
        'social_media': 'Social media posts and engagement',
        'user_profiles': 'Social media user profiles',
        
        # Technology (8)
        'web_analytics': 'Website analytics and traffic',
        'app_usage': 'Mobile app usage analytics',
        'system_logs': 'System and application logs',
        'api_calls': 'API calls and performance',
        'server_metrics': 'Server performance monitoring',
        'user_sessions': 'User session tracking',
        'error_logs': 'Application error logs',
        'performance': 'Application performance monitoring'
    }
    
    print("\nTempDataset - Available Datasets")
    print("=" * 40)
    
    categories = {
        'Core Business (10)': ['crm', 'customers', 'ecommerce', 'employees', 'inventory', 'marketing', 'retail', 'reviews', 'sales', 'suppliers'],
        'Financial (8)': ['stocks', 'banking', 'cryptocurrency', 'insurance', 'loans', 'investments', 'accounting', 'payments'],
        'IoT Sensors (6)': ['weather', 'energy', 'traffic', 'environmental', 'industrial', 'smarthome'],
        'Healthcare (6)': ['patients', 'appointments', 'lab_results', 'prescriptions', 'medical_history', 'clinical_trials'],
        'Social Media (2)': ['social_media', 'user_profiles'],
        'Technology (8)': ['web_analytics', 'app_usage', 'system_logs', 'api_calls', 'server_metrics', 'user_sessions', 'error_logs', 'performance']
    }
    
    for category, dataset_names in categories.items():
        print(f"\n{category}:")
        for name in dataset_names:
            print(f"  • {name:18} - {datasets[name]}")
    
    print(f"\nTotal: {len(datasets)} datasets available")
    print("\nUsage: tempdataset.create_dataset('dataset_name', rows)")
    print("Example: tempdataset.create_dataset('sales', 1000)")
    
    return list(datasets.keys())


def get_performance_stats():
    """Get performance statistics from the data generator."""
    return _generator.get_performance_stats()


def reset_performance_stats():
    """Reset performance monitoring counters."""
    _generator.memory_monitor.reset()
    _generator.profiler = _generator.profiler.__class__()


__version__ = "0.2.0"

# Alias for convenience (matches the library name)
tempdataset = create_dataset

__all__ = ["create_dataset", "tempdataset", "TempDataFrame", "read_csv", "read_json", "get_performance_stats", "reset_performance_stats", "help", "list_datasets"]