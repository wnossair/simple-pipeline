# transform.py
"""This module contains the Transformer class which is responsible for 
translating trade and quote records from raw data structures into a flat, 
structured format with validation."""

from typing import Dict, List, Optional
from models import MarketDataValidator

class Transformer:
    """Class to transform trade and quote records.
    
    This class provides methods to validate and convert trade and quote records 
    from their raw input formats into a more structured format. It also logs any 
    bad records encountered during the transformation process.
    """

    def __init__(self, logger):
        self.logger = logger
        self.bad_records = []

    def transform_trade(self, trade: Dict) -> Optional[Dict]:
        """Transform trade record into flat structure with validation."""
        try:
            if not MarketDataValidator.validate_price(trade['trade']['price']):
                self.bad_records.append({
                    'file': trade.get('_file', 'unknown'),
                    'line': trade.get('_line', 'unknown'),
                    'error': f"Invalid price: {trade['trade']['price']}",
                    'record': str(trade)
                })
                return None

            return {
                'symbol': trade.get('symbol'),
                'timestamp': trade.get('timestamp'),
                'price': trade['trade']['price'],
                'size': trade['trade'].get('size'),
                'exchange': trade['trade'].get('exchange', ''),
                'condition': trade['trade'].get('condition', '')
            }
        except (KeyError, TypeError) as e:
            self.bad_records.append({
                'file': trade.get('_file', 'unknown'),
                'line': trade.get('_line', 'unknown'),
                'error': f"Transformation error: {str(e)}",
                'record': str(trade)
            })
            return None

    def transform_quote(self, quote: Dict) -> Optional[Dict]:
        """Transform quote record into flat structure with validation."""
        try:
            if not (MarketDataValidator.validate_price(quote['quote']['bid']) and
                   MarketDataValidator.validate_price(quote['quote']['ask'])):
                self.bad_records.append({
                    'file': quote.get('_file', 'unknown'),
                    'line': quote.get('_line', 'unknown'),
                    'error': f"Invalid prices: bid={quote['quote']['bid']}, ask={quote['quote']['ask']}",
                    'record': str(quote)
                })
                return None

            return {
                'symbol': quote.get('symbol'),
                'timestamp': quote.get('timestamp'),
                'bid': quote['quote']['bid'],
                'ask': quote['quote']['ask'],
                'exchange': quote['quote'].get('exchange', '')
            }
        except (KeyError, TypeError) as e:
            self.bad_records.append({
                'file': quote.get('_file', 'unknown'),
                'line': quote.get('_line', 'unknown'),
                'error': f"Transformation error: {str(e)}",
                'record': str(quote)
            })
            return None

    def transform(self, trades: List[Dict], quotes: List[Dict]) -> tuple[List[Dict], List[Dict]]:
        """Transform lists of trades and quotes."""
        transformed_trades = [t for t in (self.transform_trade(t) for t in trades) if t]
        transformed_quotes = [q for q in (self.transform_quote(q) for q in quotes) if q]
        return transformed_trades, transformed_quotes
