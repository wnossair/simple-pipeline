# extract.py
"""This module contains the Extractor class which is responsible for 
extracting trade and quote events from JSONL files."""

import json
from typing import Dict, List, Tuple
from pathlib import Path
from models import MarketDataValidator

class Extractor:
    """Class to extract trade and quote events from JSONL files.
    
    This class reads a specified JSONL file, parses each line as a JSON object,
    and categorizes the records into trades and quotes based on their event type. 
    It also validates timestamps and logs any bad records encountered during extraction.
    """

    def __init__(self, logger):
        self.logger = logger
        self.bad_records = []

    def extract(self, file_path: Path) -> Tuple[List[Dict], List[Dict]]:
        """Extract trade and quote events from JSONL file."""
        trades = []
        quotes = []

        with open(file_path, 'r', encoding="utf-8") as f:
            for line_number, line in enumerate(f, 1):
                try:
                    record = json.loads(line.strip())
                    if not isinstance(record, dict):
                        raise ValueError("Record is not a valid JSON object")

                    if record.get('event_type') == 'trade':
                        if MarketDataValidator.validate_timestamp(record.get('timestamp')):
                            record['_file'] = str(file_path)
                            record['_line'] = line_number
                            trades.append(record)
                        else:
                            self.bad_records.append({
                                'file': str(file_path),
                                'line': line_number,
                                'error': 'Invalid timestamp',
                                'record': line.strip()
                            })
                    elif record.get('event_type') == 'quote':
                        if MarketDataValidator.validate_timestamp(record.get('timestamp')):
                            record['_file'] = str(file_path)
                            record['_line'] = line_number
                            quotes.append(record)
                        else:
                            self.bad_records.append({
                                'file': str(file_path),
                                'line': line_number,
                                'error': 'Invalid timestamp',
                                'record': line.strip()
                            })
                    else:
                        self.bad_records.append({
                            'file': str(file_path),
                            'line': line_number,
                            'error': 'Unknown event_type',
                            'record': line.strip()
                        })
                except json.JSONDecodeError:
                    self.bad_records.append({
                        'file': str(file_path),
                        'line': line_number,
                        'error': 'Invalid JSON',
                        'record': line.strip()
                    })

        self.logger.info(
            f"Extracted {len(trades)} trades and {len(quotes)} quotes "
            f"from {file_path}"
        )
        return trades, quotes
