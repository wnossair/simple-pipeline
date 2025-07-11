# extract.py
"""This module contains the Extractor class which is responsible for 
extracting and validating market data from JSONL files using Pydantic."""

from typing import List, Tuple
from pathlib import Path
from pydantic import ValidationError
from models import MarketEvent # Import the Pydantic model

class Extractor:
    """Class to extract and validate market events from JSONL files using Pydantic."""

    def __init__(self, logger):
        self.logger = logger
        self.bad_records = []

    def extract(self, file_path: Path) -> Tuple[List[MarketEvent], List[MarketEvent]]:
        """
        Extract and validate trade and quote events from a JSONL file.
        Returns lists of validated Pydantic MarketEvent objects.
        """
        trades = []
        quotes = []

        with open(file_path, 'r', encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                try:
                    # Pydantic parses the JSON and runs all validators,
                    # including the custom @model_validator.
                    event = MarketEvent.model_validate_json(line)

                    # FIX: Attach file and line info using direct attribute assignment
                    event.source_file = str(file_path)
                    event.source_line = line_number

                    # The logic is now simpler: if validation passed, we just sort the event.
                    # The @model_validator already guarantees the payload matches the type.
                    if event.event_type == 'trade':
                        trades.append(event)
                    elif event.event_type == 'quote':
                        quotes.append(event)

                except (ValidationError, ValueError) as e:
                    # Any validation error (from Pydantic or our custom validator) is caught here.
                    self.bad_records.append({
                        'file': str(file_path),
                        'line': line_number,
                        'error': str(e),
                        'record': line.strip()
                    })

        self.logger.info(
            f"Extracted {len(trades)} trades and {len(quotes)} quotes "
            f"from {file_path}"
        )
        return trades, quotes
