# models.py
"""This module contains classes and functions for validating market data."""

import datetime

class MarketDataValidator:
    """Class containing methods to validate different aspects of market data."""

    @staticmethod
    def validate_timestamp(timestamp: str) -> bool:
        """Validate timestamp format."""
        try:
            datetime.datetime.fromisoformat(timestamp)
            return True
        except (ValueError, TypeError):
            return False

    @staticmethod
    def validate_price(price: float) -> bool:
        """Validate price is non-negative."""
        return price >= 0 if isinstance(price, (int, float)) else False
