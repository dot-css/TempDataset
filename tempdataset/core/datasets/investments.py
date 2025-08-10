"""
Investments dataset generator.

Generates realistic investment portfolio data with performance tracking.
"""

import random
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class InvestmentsDataset(BaseDataset):
    """Investment portfolio dataset generator."""
    
    def __init__(self, rows: int = 500):
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        self._init_data_lists()
        self._portfolio_counter = 10001
        self._customer_counter = 1
        self._broker_counter = 1
    
    def _init_data_lists(self) -> None:
        self.asset_types = ['Stock', 'Bond', 'ETF', 'Mutual Fund', 'REIT', 'Crypto', 'Commodity']
        self.sectors = ['Technology', 'Healthcare', 'Finance', 'Energy', 'Consumer', 'Industrial', 'Utilities', 'Real Estate']
        self.risk_levels = ['Low', 'Medium', 'High', 'Very High']
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD']
        
        self.assets_by_type = {
            'Stock': [('AAPL', 'Apple Inc.'), ('MSFT', 'Microsoft'), ('GOOGL', 'Alphabet'), ('AMZN', 'Amazon'), ('TSLA', 'Tesla')],
            'Bond': [('TLT', 'Treasury Bond ETF'), ('CORP', 'Corporate Bond'), ('MUNI', 'Municipal Bond'), ('GOVT', 'Government Bond')],
            'ETF': [('SPY', 'S&P 500 ETF'), ('QQQ', 'NASDAQ ETF'), ('VTI', 'Total Market ETF'), ('IWM', 'Small Cap ETF')],
            'Mutual Fund': [('FXAIX', 'Fidelity 500 Fund'), ('VTSAX', 'Vanguard Total Market'), ('VTSMX', 'Vanguard Total Stock')],
            'REIT': [('VNQ', 'Vanguard REIT'), ('SCHH', 'Schwab REIT'), ('IYR', 'iShares REIT')],
            'Crypto': [('BTC', 'Bitcoin'), ('ETH', 'Ethereum'), ('ADA', 'Cardano'), ('SOL', 'Solana')],
            'Commodity': [('GLD', 'Gold ETF'), ('SLV', 'Silver ETF'), ('USO', 'Oil ETF'), ('DBA', 'Agriculture ETF')]
        }
    
    def generate(self) -> List[Dict[str, Any]]:
        if self.seed is not None:
            random.seed(self.seed)
            self.faker_utils.set_seed(self.seed)
        
        return [self._generate_row() for _ in range(self.rows)]
    
    def _generate_row(self) -> Dict[str, Any]:
        asset_type = random.choice(self.asset_types)
        asset_symbol, asset_name = random.choice(self.assets_by_type[asset_type])
        
        # Purchase details
        purchase_date = self.faker_utils.date_between(
            datetime.now() - timedelta(days=1095), datetime.now() - timedelta(days=30)
        )
        quantity = random.uniform(1, 1000) if asset_type in ['Stock', 'ETF'] else random.uniform(0.1, 100)
        purchase_price = self._generate_price(asset_type)
        
        # Current performance
        current_price = purchase_price * random.uniform(0.7, 1.5)  # -30% to +50% change
        market_value = quantity * current_price
        gain_loss_amount = market_value - (quantity * purchase_price)
        gain_loss_percent = (gain_loss_amount / (quantity * purchase_price)) * 100
        
        # Portfolio allocation
        allocation_percent = random.uniform(1, 25)  # 1-25% of portfolio
        
        # Risk and dividends
        risk_level = self._get_risk_level(asset_type)
        dividend_yield = self._get_dividend_yield(asset_type)
        sector = random.choice(self.sectors)
        currency = random.choice(self.currencies) if random.random() < 0.1 else 'USD'
        
        # Timestamps
        last_updated = self.faker_utils.date_between(purchase_date, datetime.now())
        
        # Notes
        notes = random.choice([
            'Long-term hold', 'Growth investment', 'Dividend focus', 'Speculative play',
            'Portfolio diversification', 'Value investment', 'Income generation', None
        ]) if random.random() < 0.2 else None
        
        return {
            'portfolio_id': f"PORT-{self._portfolio_counter:05d}",
            'customer_id': f"CUST-{self._customer_counter:06d}",
            'asset_type': asset_type,
            'asset_symbol': asset_symbol,
            'asset_name': asset_name,
            'quantity': round(quantity, 4),
            'purchase_date': purchase_date.strftime('%Y-%m-%d'),
            'purchase_price': round(purchase_price, 2),
            'current_price': round(current_price, 2),
            'market_value': round(market_value, 2),
            'gain_loss_amount': round(gain_loss_amount, 2),
            'gain_loss_percent': round(gain_loss_percent, 2),
            'sector': sector,
            'risk_level': risk_level,
            'allocation_percent': round(allocation_percent, 2),
            'dividend_yield': round(dividend_yield, 2),
            'last_updated': last_updated.strftime('%Y-%m-%d %H:%M:%S'),
            'currency': currency,
            'broker_id': f"BRK-{self._broker_counter:03d}",
            'notes': notes
        }
    
    def _generate_price(self, asset_type: str):
        price_ranges = {
            'Stock': (10, 500), 'Bond': (95, 105), 'ETF': (20, 400),
            'Mutual Fund': (10, 100), 'REIT': (15, 150),
            'Crypto': (0.1, 50000), 'Commodity': (10, 200)
        }
        min_price, max_price = price_ranges.get(asset_type, (10, 100))
        return random.uniform(min_price, max_price)
    
    def _get_risk_level(self, asset_type: str):
        risk_map = {
            'Stock': random.choice(['Medium', 'High']),
            'Bond': 'Low', 'ETF': random.choice(['Low', 'Medium']),
            'Mutual Fund': random.choice(['Low', 'Medium']),
            'REIT': 'Medium', 'Crypto': 'Very High', 'Commodity': 'High'
        }
        return risk_map.get(asset_type, 'Medium')
    
    def _get_dividend_yield(self, asset_type: str):
        if asset_type in ['Stock', 'ETF', 'REIT']:
            return random.uniform(0, 8)
        elif asset_type in ['Bond', 'Mutual Fund']:
            return random.uniform(1, 5)
        return 0  # Crypto and some others don't pay dividends
    
    def get_schema(self) -> Dict[str, str]:
        return {
            'portfolio_id': 'string', 'customer_id': 'string', 'asset_type': 'string',
            'asset_symbol': 'string', 'asset_name': 'string', 'quantity': 'float',
            'purchase_date': 'date', 'purchase_price': 'float', 'current_price': 'float',
            'market_value': 'float', 'gain_loss_amount': 'float', 'gain_loss_percent': 'float',
            'sector': 'string', 'risk_level': 'string', 'allocation_percent': 'float',
            'dividend_yield': 'float', 'last_updated': 'datetime', 'currency': 'string',
            'broker_id': 'string', 'notes': 'string'
        }
