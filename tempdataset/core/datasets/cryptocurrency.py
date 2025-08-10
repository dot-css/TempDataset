"""
Cryptocurrency dataset generator.

Generates realistic cryptocurrency trading data with extreme volatility modeling.
"""

import random
import string
from datetime import datetime, timedelta
from typing import List, Dict, Any, Optional

from .base import BaseDataset
from ..utils.faker_utils import get_faker_utils


class CryptocurrencyDataset(BaseDataset):
    """
    Cryptocurrency dataset generator that creates realistic crypto trading data.
    
    Generates 20 columns of cryptocurrency data including:
    - Basic crypto info (symbol, name, blockchain)
    - OHLCV data with extreme volatility
    - Market metrics (market cap, supply, volume)
    - Blockchain statistics (hash rate, difficulty, fees)
    """
    
    def __init__(self, rows: int = 500):
        """
        Initialize the CryptocurrencyDataset generator.
        
        Args:
            rows: Number of rows to generate (default: 500)
        """
        super().__init__(rows)
        self.faker_utils = get_faker_utils()
        
        # Initialize data for consistent generation
        self._init_data_lists()
    
    def _init_data_lists(self) -> None:
        """Initialize predefined data lists for realistic generation."""
        
        # Major cryptocurrencies with their data
        self.cryptocurrencies = {
            'BTC': {
                'name': 'Bitcoin',
                'blockchain': 'Bitcoin',
                'price_range': (20000, 70000),
                'market_cap_range': (400_000_000_000, 1_400_000_000_000),
                'max_supply': 21_000_000,
                'has_hash_rate': True
            },
            'ETH': {
                'name': 'Ethereum',
                'blockchain': 'Ethereum',
                'price_range': (1200, 4800),
                'market_cap_range': (150_000_000_000, 580_000_000_000),
                'max_supply': None,
                'has_hash_rate': False
            },
            'BNB': {
                'name': 'BNB',
                'blockchain': 'Binance Smart Chain',
                'price_range': (200, 600),
                'market_cap_range': (30_000_000_000, 90_000_000_000),
                'max_supply': 200_000_000,
                'has_hash_rate': False
            },
            'ADA': {
                'name': 'Cardano',
                'blockchain': 'Cardano',
                'price_range': (0.3, 3.0),
                'market_cap_range': (10_000_000_000, 100_000_000_000),
                'max_supply': 45_000_000_000,
                'has_hash_rate': False
            },
            'XRP': {
                'name': 'XRP',
                'blockchain': 'XRP Ledger',
                'price_range': (0.3, 2.0),
                'market_cap_range': (15_000_000_000, 100_000_000_000),
                'max_supply': 100_000_000_000,
                'has_hash_rate': False
            },
            'SOL': {
                'name': 'Solana',
                'blockchain': 'Solana',
                'price_range': (8, 260),
                'market_cap_range': (3_000_000_000, 120_000_000_000),
                'max_supply': None,
                'has_hash_rate': False
            },
            'DOT': {
                'name': 'Polkadot',
                'blockchain': 'Polkadot',
                'price_range': (4, 55),
                'market_cap_range': (5_000_000_000, 55_000_000_000),
                'max_supply': None,
                'has_hash_rate': False
            },
            'DOGE': {
                'name': 'Dogecoin',
                'blockchain': 'Dogecoin',
                'price_range': (0.05, 0.7),
                'market_cap_range': (7_000_000_000, 100_000_000_000),
                'max_supply': None,
                'has_hash_rate': True
            },
            'AVAX': {
                'name': 'Avalanche',
                'blockchain': 'Avalanche',
                'price_range': (9, 146),
                'market_cap_range': (3_000_000_000, 50_000_000_000),
                'max_supply': 720_000_000,
                'has_hash_rate': False
            },
            'MATIC': {
                'name': 'Polygon',
                'blockchain': 'Polygon',
                'price_range': (0.3, 2.9),
                'market_cap_range': (3_000_000_000, 25_000_000_000),
                'max_supply': 10_000_000_000,
                'has_hash_rate': False
            },
            'LINK': {
                'name': 'Chainlink',
                'blockchain': 'Ethereum',
                'price_range': (5, 52),
                'market_cap_range': (2_500_000_000, 25_000_000_000),
                'max_supply': 1_000_000_000,
                'has_hash_rate': False
            },
            'UNI': {
                'name': 'Uniswap',
                'blockchain': 'Ethereum',
                'price_range': (3, 45),
                'market_cap_range': (2_000_000_000, 35_000_000_000),
                'max_supply': 1_000_000_000,
                'has_hash_rate': False
            }
        }
        
        # Trading pairs
        self.trading_pairs = [
            'BTC/USDT', 'ETH/USDT', 'BNB/USDT', 'ADA/USDT', 'XRP/USDT', 'SOL/USDT',
            'ETH/BTC', 'ADA/BTC', 'XRP/BTC', 'DOT/BTC', 'LINK/BTC', 'UNI/BTC',
            'BTC/USD', 'ETH/USD', 'ADA/USD', 'SOL/USD'
        ]
        
        # Cryptocurrency exchanges
        self.exchanges = [
            'Binance', 'Coinbase Pro', 'Kraken', 'Huobi', 'KuCoin', 'Bitfinex',
            'Gate.io', 'OKX', 'Bybit', 'FTX', 'Gemini', 'Bitstamp'
        ]
    
    def generate(self) -> List[Dict[str, Any]]:
        """
        Generate cryptocurrency dataset rows.
        
        Returns:
            List of dictionaries representing cryptocurrency data rows
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
        """Generate a single cryptocurrency data row."""
        
        # Select random cryptocurrency
        symbol = random.choice(list(self.cryptocurrencies.keys()))
        crypto_data = self.cryptocurrencies[symbol]
        
        # Generate timestamp (within last 30 days for more recent data)
        end_date = datetime.now()
        start_date = end_date - timedelta(days=30)
        date_time = self.faker_utils.date_between(start_date, end_date)
        
        # Generate OHLCV data with extreme volatility typical of crypto
        min_price, max_price = crypto_data['price_range']
        base_price = random.uniform(min_price, max_price)
        
        # Crypto has much higher volatility than stocks
        open_price = base_price * random.uniform(0.85, 1.15)
        
        # High and low with extreme movements
        high_price = open_price * random.uniform(1.00, 1.25)
        low_price = open_price * random.uniform(0.75, 1.00)
        
        # Close price anywhere between low and high
        close_price = random.uniform(low_price, high_price)
        
        # Volume - crypto has highly variable volume
        volume = self._generate_crypto_volume(symbol)
        
        # Market cap and supply
        min_market_cap, max_market_cap = crypto_data['market_cap_range']
        market_cap = random.uniform(min_market_cap, max_market_cap)
        
        # Circulating supply based on market cap and price
        circulating_supply = market_cap / close_price
        
        # Max supply
        max_supply = crypto_data['max_supply']
        
        # Change percentages (crypto has extreme volatility)
        change_24h = ((close_price - open_price) / open_price) * 100
        change_7d = change_24h + random.uniform(-50, 50)  # 7-day change can be extreme
        
        # Exchange and trading pair
        exchange = random.choice(self.exchanges)
        trading_pair = random.choice(self.trading_pairs)
        
        # Ensure trading pair matches symbol
        if symbol not in trading_pair:
            trading_pair = f"{symbol}/USDT"
        
        # Blockchain metrics
        transaction_count = random.randint(100_000, 2_000_000)
        
        # Hash rate and difficulty (only for PoW coins)
        hash_rate = None
        difficulty = None
        if crypto_data['has_hash_rate']:
            if symbol == 'BTC':
                hash_rate = random.uniform(200, 400)  # EH/s
                difficulty = random.uniform(25_000_000_000_000, 50_000_000_000_000)
            else:  # Other PoW coins
                hash_rate = random.uniform(50, 200)
                difficulty = random.uniform(1_000_000, 10_000_000)
        
        # Network fees
        network_fees = self._generate_network_fees(symbol)
        
        return {
            'symbol': symbol,
            'name': crypto_data['name'],
            'date_time': date_time.strftime('%Y-%m-%d %H:%M:%S'),
            'open_price': round(open_price, 6),
            'high_price': round(high_price, 6),
            'low_price': round(low_price, 6),
            'close_price': round(close_price, 6),
            'volume': round(volume, 2),
            'market_cap': round(market_cap, 2),
            'circulating_supply': round(circulating_supply, 2),
            'max_supply': max_supply,
            '24h_change_percent': round(change_24h, 2),
            '7d_change_percent': round(change_7d, 2),
            'exchange': exchange,
            'trading_pair': trading_pair,
            'blockchain': crypto_data['blockchain'],
            'transaction_count': transaction_count,
            'hash_rate': round(hash_rate, 2) if hash_rate else None,
            'difficulty': round(difficulty, 0) if difficulty else None,
            'network_fees': round(network_fees, 6)
        }
    
    def _generate_crypto_volume(self, symbol: str) -> float:
        """
        Generate realistic trading volume for cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Trading volume
        """
        volume_ranges = {
            'BTC': (500_000_000, 50_000_000_000),
            'ETH': (200_000_000, 20_000_000_000),
            'BNB': (100_000_000, 5_000_000_000),
            'ADA': (50_000_000, 2_000_000_000),
            'XRP': (100_000_000, 5_000_000_000),
            'SOL': (200_000_000, 8_000_000_000),
            'DOT': (50_000_000, 1_000_000_000),
            'DOGE': (500_000_000, 10_000_000_000),
            'AVAX': (100_000_000, 2_000_000_000),
            'MATIC': (50_000_000, 1_500_000_000),
            'LINK': (100_000_000, 2_000_000_000),
            'UNI': (50_000_000, 1_000_000_000)
        }
        
        min_vol, max_vol = volume_ranges.get(symbol, (10_000_000, 500_000_000))
        
        # Add extreme volatility to volume
        volume = random.uniform(min_vol, max_vol) * random.uniform(0.1, 10)
        
        return volume
    
    def _generate_network_fees(self, symbol: str) -> float:
        """
        Generate realistic network fees for cryptocurrency.
        
        Args:
            symbol: Cryptocurrency symbol
            
        Returns:
            Network fee amount
        """
        fee_ranges = {
            'BTC': (0.00001, 0.001),
            'ETH': (0.001, 0.1),
            'BNB': (0.0001, 0.01),
            'ADA': (0.1, 2.0),
            'XRP': (0.00001, 0.01),
            'SOL': (0.000005, 0.01),
            'DOT': (0.01, 1.0),
            'DOGE': (0.01, 10.0),
            'AVAX': (0.001, 0.1),
            'MATIC': (0.0001, 0.1),
            'LINK': (0.001, 0.1),
            'UNI': (0.001, 0.1)
        }
        
        min_fee, max_fee = fee_ranges.get(symbol, (0.001, 0.1))
        return random.uniform(min_fee, max_fee)
    
    def get_schema(self) -> Dict[str, str]:
        """
        Return column schema with types.
        
        Returns:
            Dictionary mapping column names to their data types
        """
        return {
            'symbol': 'string',
            'name': 'string',
            'date_time': 'datetime',
            'open_price': 'float',
            'high_price': 'float',
            'low_price': 'float',
            'close_price': 'float',
            'volume': 'float',
            'market_cap': 'float',
            'circulating_supply': 'float',
            'max_supply': 'float',
            '24h_change_percent': 'float',
            '7d_change_percent': 'float',
            'exchange': 'string',
            'trading_pair': 'string',
            'blockchain': 'string',
            'transaction_count': 'integer',
            'hash_rate': 'float',
            'difficulty': 'float',
            'network_fees': 'float'
        }
