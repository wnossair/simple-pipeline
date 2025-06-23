# load.py
"""This module contains the Loader class which is responsible for loading 
transformed records into a SQLite database."""

import sqlite3
from typing import Dict, List

class Loader:
    """Class to load transformed records into a SQLite database.
    
    This class provides methods to initialize the database, load data into the 
    trades and quotes tables, and close the database connection.
    """

    def __init__(self, db_path: str, logger):
        self.db_path = db_path
        self.logger = logger
        self.conn = None
        self.cursor = None

    def initialize_database(self) -> None:
        """Initialize SQLite database with trades and quotes tables."""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS trades (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                timestamp TEXT,
                price REAL,
                size INTEGER,
                exchange TEXT,
                condition TEXT
            )
        ''')

        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS quotes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                symbol TEXT,
                timestamp TEXT,
                bid REAL,
                ask REAL,
                exchange TEXT
            )
        ''')
        self.conn.commit()

    def load(self, trades: List[Dict], quotes: List[Dict]) -> None:
        """Load transformed records into SQLite database."""
        for trade in trades:
            self.cursor.execute('''
                INSERT INTO trades (symbol, timestamp, price, size, exchange, condition)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (
                trade['symbol'],
                trade['timestamp'],
                trade['price'],
                trade['size'],
                trade['exchange'],
                trade['condition']
            ))

        for quote in quotes:
            self.cursor.execute('''
                INSERT INTO quotes (symbol, timestamp, bid, ask, exchange)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                quote['symbol'],
                quote['timestamp'],
                quote['bid'],
                quote['ask'],
                quote['exchange']
            ))

        self.conn.commit()
        self.logger.info(f"Loaded {len(trades)} trades and {len(quotes)} quotes")

    def close(self):
        """Close database connection."""
        if self.conn:
            self.conn.close()
