# models.py
"""This module contains the Pydantic models for validating market data."""

from datetime import datetime
from typing import Optional, Any
from pydantic import BaseModel, Field, model_validator, ConfigDict

class TradeDetails(BaseModel):
    """Pydantic model for the nested 'trade' object with validation rules."""
    price: float = Field(gt=0)  # Price must be a float and greater than 0
    size: int = Field(gt=0)     # Size must be an integer and greater than 0
    exchange: Optional[str] = None
    condition: Optional[str] = None

class QuoteDetails(BaseModel):
    """Pydantic model for the nested 'quote' object with validation rules."""
    bid: float = Field(ge=0)  # Bid can be 0 or positive
    ask: float = Field(ge=0)  # Ask can be 0 or positive
    exchange: Optional[str] = None

class MarketEvent(BaseModel):
    """
    The main Pydantic model for a single market event from a JSONL file.
    It automatically validates the top-level fields and the nested trade/quote objects.
    """
    event_type: str
    symbol: str
    timestamp: datetime
    trade: Optional[TradeDetails] = None
    quote: Optional[QuoteDetails] = None

    # Use model_config for Pydantic v2 to allow extra attributes
    model_config = ConfigDict(extra='allow')

    @model_validator(mode='before')
    @classmethod
    def check_payload_matches_event_type(cls, data: Any) -> Any:
        """
        Ensures that the correct data payload (trade or quote) is present
        and the other is absent, based on the event_type.
        """
        if not isinstance(data, dict):
            return data # Let other validators handle non-dict data

        event_type = data.get('event_type')
        has_trade = 'trade' in data and data['trade'] is not None
        has_quote = 'quote' in data and data['quote'] is not None

        if event_type == 'trade':
            if not has_trade:
                raise ValueError("For event_type 'trade', 'trade' payload must be present.")
            if has_quote:
                raise ValueError("For event_type 'trade', 'quote' payload must not be present.")
        elif event_type == 'quote':
            if not has_quote:
                raise ValueError("For event_type 'quote', 'quote' payload must be present.")
            if has_trade:
                raise ValueError("For event_type 'quote', 'trade' payload must not be present.")
        elif event_type is not None:
            raise ValueError(f"Unknown event_type: '{event_type}'. Must be 'trade' or 'quote'.")

        return data
