"""
Stocks dataset generator.

Generates realistic stock market OHLCV data with volatility and trading behavior.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class StocksDataset(BaseDataset):
    """
    Stocks dataset generator that creates realistic stock market data.
    
    Generates 20 columns of stock data including:
    - Basic stock info (ticker, company, sector, industry)
    - OHLCV data (open, high, low, close, volume)
    - Financial metrics (market cap, PE ratio, dividend yield)
    - Market performance indicators
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the StocksDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
        
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Stock sectors and industries
        self.sectors = {
            'Technology': ['Software', 'Semiconductors', 'Hardware', 'Internet', 'Cloud Computing'],
            'Finance': ['Banking', 'Insurance', 'Investment Services', 'Real Estate', 'Fintech'],
            'Healthcare': ['Pharmaceuticals', 'Biotechnology', 'Medical Devices', 'Healthcare Services'],
            'Energy': ['Oil & Gas', 'Renewable Energy', 'Utilities', 'Coal', 'Nuclear'],
            'Consumer Discretionary': ['Retail', 'Automotive', 'Entertainment', 'Travel', 'Luxury Goods'],
            'Consumer Staples': ['Food & Beverages', 'Household Products', 'Personal Care', 'Tobacco'],
            'Industrials': ['Aerospace', 'Construction', 'Manufacturing', 'Transportation', 'Defense'],
            'Materials': ['Chemicals', 'Mining', 'Steel', 'Paper', 'Packaging'],
            'Communications': ['Telecom', 'Media', 'Broadcasting', 'Publishing', 'Advertising'],
            'Real Estate': ['REITs', 'Real Estate Development', 'Property Management', 'Commercial Real Estate']
        }
        
        # Stock tickers and company names by sector
        self.stock_data = {
            'Technology': [
                ('AAPL', 'Apple Inc.'), ('MSFT', 'Microsoft Corporation'), ('GOOGL', 'Alphabet Inc.'),
                ('AMZN', 'Amazon.com Inc.'), ('META', 'Meta Platforms Inc.'), ('TSLA', 'Tesla Inc.'),
                ('NVDA', 'NVIDIA Corporation'), ('NFLX', 'Netflix Inc.'), ('CRM', 'Salesforce Inc.'),
                ('ADBE', 'Adobe Inc.'), ('INTC', 'Intel Corporation'), ('AMD', 'Advanced Micro Devices'),
                ('ORCL', 'Oracle Corporation'), ('IBM', 'International Business Machines'), ('CSCO', 'Cisco Systems')
            ],
            'Finance': [
                ('JPM', 'JPMorgan Chase & Co.'), ('BAC', 'Bank of America Corp'), ('WFC', 'Wells Fargo & Co'),
                ('GS', 'Goldman Sachs Group'), ('MS', 'Morgan Stanley'), ('C', 'Citigroup Inc.'),
                ('USB', 'U.S. Bancorp'), ('PNC', 'PNC Financial Services'), ('BLK', 'BlackRock Inc.'),
                ('AXP', 'American Express Co'), ('TFC', 'Truist Financial'), ('COF', 'Capital One Financial')
            ],
            'Healthcare': [
                ('JNJ', 'Johnson & Johnson'), ('PFE', 'Pfizer Inc.'), ('UNH', 'UnitedHealth Group'),
                ('ABBV', 'AbbVie Inc.'), ('MRK', 'Merck & Co.'), ('LLY', 'Eli Lilly and Co'),
                ('TMO', 'Thermo Fisher Scientific'), ('DHR', 'Danaher Corporation'), ('BMY', 'Bristol Myers Squibb'),
                ('MDT', 'Medtronic plc'), ('GILD', 'Gilead Sciences'), ('CVS', 'CVS Health Corporation')
            ],
            'Energy': [
                ('XOM', 'Exxon Mobil Corporation'), ('CVX', 'Chevron Corporation'), ('COP', 'ConocoPhillips'),
                ('SLB', 'Schlumberger Limited'), ('EOG', 'EOG Resources'), ('PXD', 'Pioneer Natural Resources'),
                ('KMI', 'Kinder Morgan'), ('OKE', 'ONEOK Inc.'), ('WMB', 'Williams Companies'), ('MPC', 'Marathon Petroleum'),
                ('VLO', 'Valero Energy'), ('PSX', 'Phillips 66'), ('HAL', 'Halliburton Company'), ('BKR', 'Baker Hughes')
            ],
            'Consumer Discretionary': [
                ('HD', 'Home Depot Inc.'), ('MCD', 'McDonald\'s Corporation'), ('NKE', 'Nike Inc.'),
                ('SBUX', 'Starbucks Corporation'), ('LOW', 'Lowe\'s Companies'), ('TGT', 'Target Corporation'),
                ('F', 'Ford Motor Company'), ('GM', 'General Motors Company'), ('DIS', 'Walt Disney Company'),
                ('AMZN', 'Amazon.com Inc.'), ('EBAY', 'eBay Inc.'), ('BKNG', 'Booking Holdings Inc.')
            ],
            'Consumer Staples': [
                ('WMT', 'Walmart Inc.'), ('PG', 'Procter & Gamble Co'), ('KO', 'Coca-Cola Company'),
                ('PEP', 'PepsiCo Inc.'), ('COST', 'Costco Wholesale'), ('WBA', 'Walgreens Boots Alliance'),
                ('KR', 'Kroger Co.'), ('CL', 'Colgate-Palmolive Co'), ('GIS', 'General Mills Inc.'),
                ('K', 'Kellogg Company'), ('CPB', 'Campbell Soup Company'), ('SYY', 'Sysco Corporation')
            ],
            'Industrials': [
                ('BA', 'Boeing Company'), ('CAT', 'Caterpillar Inc.'), ('GE', 'General Electric'),
                ('HON', 'Honeywell International'), ('UPS', 'United Parcel Service'), ('FDX', 'FedEx Corporation'),
                ('LMT', 'Lockheed Martin Corp'), ('RTX', 'Raytheon Technologies'), ('MMM', '3M Company'),
                ('DE', 'Deere & Company'), ('EMR', 'Emerson Electric Co'), ('ITW', 'Illinois Tool Works')
            ],
            'Materials': [
                ('LIN', 'Linde plc'), ('APD', 'Air Products and Chemicals'), ('SHW', 'Sherwin-Williams Company'),
                ('FCX', 'Freeport-McMoRan Inc.'), ('NEM', 'Newmont Corporation'), ('DOW', 'Dow Inc.'),
                ('DD', 'DuPont de Nemours'), ('PPG', 'PPG Industries'), ('ECL', 'Ecolab Inc.'),
                ('CF', 'CF Industries Holdings'), ('MOS', 'Mosaic Company'), ('NUE', 'Nucor Corporation')
            ],
            'Communications': [
                ('VZ', 'Verizon Communications'), ('T', 'AT&T Inc.'), ('TMUS', 'T-Mobile US'),
                ('CMCSA', 'Comcast Corporation'), ('DIS', 'Walt Disney Company'), ('NFLX', 'Netflix Inc.'),
                ('VIA', 'ViacomCBS Inc.'), ('FOX', 'Fox Corporation'), ('DISH', 'DISH Network Corporation'),
                ('CHTR', 'Charter Communications'), ('LUMN', 'Lumen Technologies'), ('S', 'Sprint Corporation')
            ],
            'Real Estate': [
                ('AMT', 'American Tower Corporation'), ('PLD', 'Prologis Inc.'), ('CCI', 'Crown Castle International'),
                ('EQIX', 'Equinix Inc.'), ('WY', 'Weyerhaeuser Company'), ('PSA', 'Public Storage'),
                ('AVB', 'AvalonBay Communities'), ('EQR', 'Equity Residential'), ('DLR', 'Digital Realty Trust'),
                ('SBAC', 'SBA Communications'), ('O', 'Realty Income Corporation'), ('SPG', 'Simon Property Group')
            ]
        }
        
        # Stock exchanges
        self.exchanges = ['NASDAQ', 'NYSE', 'AMEX']
        
        # Currencies
        self.currencies = ['USD', 'EUR', 'GBP', 'JPY', 'CAD', 'AUD', 'CHF', 'CNY']
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate stocks dataset rows.
        
        Returns:
            List of dictionaries representing stock data rows
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
        """Generate a single stock data row."""
        
        # Select random sector and get stock data
        sector = random.choice(list(self.sectors.keys()))
        industry = random.choice(self.sectors[sector])
        ticker, company_name = random.choice(self.stock_data[sector])
        
        # Generate date (within last year)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=365)
        date = self.faker_utils.date_between(start_date, end_date)
        
        # Generate base price (sector-dependent)
        base_price = self._generate_base_price(sector)
        
        # Generate OHLCV data with realistic relationships
        open_price = base_price * random.uniform(0.95, 1.05)
        
        # High and low relative to open
        high_price = open_price * random.uniform(1.00, 1.08)
        low_price = open_price * random.uniform(0.92, 1.00)
        
        # Close price between low and high
        close_price = random.uniform(low_price, high_price)
        
        # Adjusted close (usually very close to close)
        adjusted_close_price = close_price * random.uniform(0.98, 1.02)
        
        # Volume (sector and price dependent)
        volume = self._generate_volume(sector, base_price)
        
        # Market cap based on price and shares outstanding
        shares_outstanding = random.randint(100_000_000, 10_000_000_000)
        market_cap = close_price * shares_outstanding
        
        # Financial ratios
        pe_ratio = random.uniform(5, 50) if random.random() > 0.1 else None
        dividend_yield = random.uniform(0, 8) if random.random() > 0.4 else 0
        beta = random.uniform(0.3, 2.5)
        
        # 52-week range
        week_52_high = close_price * random.uniform(1.05, 1.5)
        week_52_low = close_price * random.uniform(0.5, 0.95)
        
        # Day change percentage
        day_change_percent = ((close_price - open_price) / open_price) * 100
        
        # Exchange and currency
        exchange = random.choice(self.exchanges)
        currency = random.choice(self.currencies) if exchange != 'NYSE' and exchange != 'NASDAQ' else 'USD'
        
        return {
            'ticker': ticker,
            'company_name': company_name,
            'sector': sector,
            'industry': industry,
            'exchange': exchange,
            'date': date.strftime('%Y-%m-%d %H:%M:%S'),
            'open_price': round(open_price, 2),
            'high_price': round(high_price, 2),
            'low_price': round(low_price, 2),
            'close_price': round(close_price, 2),
            'adjusted_close_price': round(adjusted_close_price, 2),
            'volume': volume,
            'market_cap': round(market_cap, 2),
            'pe_ratio': round(pe_ratio, 2) if pe_ratio else None,
            'dividend_yield': round(dividend_yield, 2),
            'beta': round(beta, 2),
            'currency': currency,
            '52_week_high': round(week_52_high, 2),
            '52_week_low': round(week_52_low, 2),
            'day_change_percent': round(day_change_percent, 2)
        }
    
    def _generate_base_price(self, sector: str) -> float:
        """
        Generate realistic base price based on sector.
        
        Args:
            sector: Stock sector
            
        Returns:
            Base stock price
        """
        price_ranges = {
            'Technology': (20, 300),
            'Finance': (15, 150),
            'Healthcare': (30, 200),
            'Energy': (10, 100),
            'Consumer Discretionary': (25, 180),
            'Consumer Staples': (40, 120),
            'Industrials': (50, 250),
            'Materials': (20, 80),
            'Communications': (15, 100),
            'Real Estate': (30, 150)
        }
        
        min_price, max_price = price_ranges.get(sector, (20, 100))
        return random.uniform(min_price, max_price)
    
    def _generate_volume(self, sector: str, price: float) -> int:
        """
        Generate realistic trading volume.
        
        Args:
            sector: Stock sector
            price: Stock price
            
        Returns:
            Trading volume
        """
        # Base volume ranges by sector
        base_volumes = {
            'Technology': (1_000_000, 50_000_000),
            'Finance': (500_000, 20_000_000),
            'Healthcare': (800_000, 15_000_000),
            'Energy': (2_000_000, 30_000_000),
            'Consumer Discretionary': (1_500_000, 25_000_000),
            'Consumer Staples': (1_000_000, 10_000_000),
            'Industrials': (500_000, 8_000_000),
            'Materials': (800_000, 12_000_000),
            'Communications': (2_000_000, 40_000_000),
            'Real Estate': (300_000, 5_000_000)
        }
        
        min_vol, max_vol = base_volumes.get(sector, (500_000, 10_000_000))
        
        # Higher volume for lower-priced stocks
        price_factor = max(0.5, min(2.0, 100 / price))
        
        volume = random.randint(int(min_vol * price_factor), int(max_vol * price_factor))
        return volume
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'ticker': 'string',
            'company_name': 'string',
            'sector': 'string',
            'industry': 'string',
            'exchange': 'string',
            'date': 'datetime',
            'open_price': 'float',
            'high_price': 'float',
            'low_price': 'float',
            'close_price': 'float',
            'adjusted_close_price': 'float',
            'volume': 'integer',
            'market_cap': 'float',
            'pe_ratio': 'float',
            'dividend_yield': 'float',
            'beta': 'float',
            'currency': 'string',
            '52_week_high': 'float',
            '52_week_low': 'float',
            'day_change_percent': 'float'
        }
