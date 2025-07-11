# transform.py
"""This module contains the Transformer class which is responsible for 
translating validated Pydantic models into a flat, structured format for loading."""

from typing import List, Dict
from models import MarketEvent

class Transformer:
    """Class to transform validated MarketEvent Pydantic models into flat dictionaries."""

    def __init__(self, logger):
        self.logger = logger
        # No bad_records needed here anymore, as validation is done during extraction.

    def transform_trade(self, trade_event: MarketEvent) -> Dict:
        """Transforms a trade MarketEvent model into a flat dictionary."""
        # The trade object is guaranteed by the extraction logic to exist and be valid.
        flat_trade = {
            'symbol': trade_event.symbol,
            'timestamp': trade_event.timestamp.isoformat(),
            'price': trade_event.trade.price,
            'size': trade_event.trade.size,
            'exchange': trade_event.trade.exchange or '',
            'condition': trade_event.trade.condition or ''
        }
        return flat_trade

    def transform_quote(self, quote_event: MarketEvent) -> Dict:
        """Transforms a quote MarketEvent model into a flat dictionary."""
        # The quote object is guaranteed by the extraction logic to exist and be valid.
        flat_quote = {
            'symbol': quote_event.symbol,
            'timestamp': quote_event.timestamp.isoformat(),
            'bid': quote_event.quote.bid,
            'ask': quote_event.quote.ask,
            'exchange': quote_event.quote.exchange or ''
        }
        return flat_quote

    def transform(
            self,
            trades: List[MarketEvent],
            quotes: List[MarketEvent]
            ) -> tuple[List[Dict], List[Dict]]:

        """Transforms lists of validated trade and quote events."""
        transformed_trades = [self.transform_trade(t) for t in trades]
        transformed_quotes = [self.transform_quote(q) for q in quotes]

        self.logger.info(
            f"Transformed {len(transformed_trades)} trades and {len(transformed_quotes)} quotes.")

        return transformed_trades, transformed_quotes
