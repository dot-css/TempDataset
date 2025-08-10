"""
Dataset definitions module.

Contains all dataset generators including the base abstract class.
"""

from .base import BaseDataset
from .crm import CrmDataset
from .customers import CustomersDataset
from .ecommerce import EcommerceDataset
from .inventory import InventoryDataset
from .marketing import MarketingDataset
from .retail import RetailDataset
from .reviews import ReviewsDataset
from .sales import SalesDataset
from .suppliers import SuppliersDataset
# Financial datasets
from .stocks import StocksDataset
from .banking import BankingDataset
from .cryptocurrency import CryptocurrencyDataset
from .insurance import InsuranceDataset
from .loans import LoansDataset
from .investments import InvestmentsDataset
from .accounting import AccountingDataset
from .payments import PaymentsDataset
# IoT Sensor datasets
from .weather import WeatherDataset
from .energy import EnergyDataset
from .traffic import TrafficDataset
from .environmental import EnvironmentalDataset
from .industrial import IndustrialDataset
from .smarthome import SmartHomeDataset
# Healthcare datasets
from .patients import PatientsDataset
from .appointments import AppointmentsDataset
from .lab_results import LabResultsDataset
from .prescriptions import PrescriptionsDataset
from .medical_history import MedicalHistoryDataset
from .clinical_trials import ClinicalTrialsDataset
# Social datasets
from .social_media import SocialMediaDataset
from .user_profiles import UserProfilesDataset

__all__ = [
    "BaseDataset", "CrmDataset", "CustomersDataset", "EcommerceDataset", 
    "InventoryDataset", "MarketingDataset", "RetailDataset", "ReviewsDataset", 
    "SalesDataset", "SuppliersDataset", "StocksDataset", "BankingDataset",
    "CryptocurrencyDataset", "InsuranceDataset", "LoansDataset", 
    "InvestmentsDataset", "AccountingDataset", "PaymentsDataset",
    "WeatherDataset", "EnergyDataset", "TrafficDataset", "EnvironmentalDataset",
    "IndustrialDataset", "SmartHomeDataset",
    "PatientsDataset", "AppointmentsDataset", "LabResultsDataset", 
    "PrescriptionsDataset", "MedicalHistoryDataset", "ClinicalTrialsDataset",
    "SocialMediaDataset", "UserProfilesDataset"
]