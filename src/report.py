# report.py
"""This module contains the Reporter class which is responsible for generating 
transaction cost reports based on market data stored in a database."""

from pathlib import Path
from collections import defaultdict
from typing import List, Dict
import pandas as pd

class Reporter:
    """Class to generate transaction cost reports.
    
    This class reads trade and quote data from a database, calculates the 
    transaction costs for each trade, and generates both text and CSV reports.
    """

    def __init__(self, conn, logger, output_path):
        self.conn = conn
        self.logger = logger
        self.output_path = output_path

    def generate_transaction_cost_report(self, bad_records: List[Dict]) -> None:
        """Generate transaction cost report based on trades and quotes."""
        trades_df = pd.read_sql_query("SELECT * FROM trades", self.conn)
        transaction_costs = defaultdict(list)

        cursor = self.conn.cursor()
        for _, trade in trades_df.iterrows():
            symbol = trade['symbol']
            trade_ts = trade['timestamp']
            trade_price = trade['price']
            exchange = trade['exchange']

            cursor.execute('''
                SELECT bid, ask
                FROM quotes
                WHERE symbol = ? AND timestamp <= ?
                ORDER BY timestamp DESC
                LIMIT 1
            ''', (symbol, trade_ts))

            quote = cursor.fetchone()
            if quote:
                bid, ask = quote
                mid_price = (bid + ask) / 2
                cost = (trade_price / mid_price - 1) * 100  # in percentage
                transaction_costs[symbol].append(cost)
                if exchange:
                    transaction_costs[f"{symbol}_{exchange}"].append(cost)

        # Generate text report
        report = []
        report.append("Transaction Cost Report (in %)")
        report.append("=" * 30)

        # Prepare CSV data
        csv_data = []

        for key, costs in transaction_costs.items():
            avg_cost = sum(costs) / len(costs)
            num_trades = len(costs)
            report.append(f"{key}:")
            report.append(f"  Average Transaction Cost: {avg_cost:.4f}%")
            report.append(f"  Number of Trades: {num_trades}")
            report.append("")
            csv_data.append({
                'key': key,
                'average_transaction_cost_percent': avg_cost,
                'number_of_trades': num_trades
            })

        # Output to console
        print("\n".join(report))

        # Output to tx_report.txt
        with open(Path(self.output_path, 'tx_report.txt'), 'w', encoding='utf-8') as f:
            f.write("\n".join(report))

        # Output to tx_report.csv
        report_df = pd.DataFrame(csv_data)
        report_df.to_csv(Path(self.output_path, 'tx_report.csv'), index=False)

        # Log bad records
        if bad_records:
            self.logger.warning("Bad records encountered:")
            for record in bad_records:
                self.logger.warning(
                    f"File: {record['file']}, "
                    f"Line: {record['line']}, "
                    f"Error: {record['error']}, "
                    f"Record: {record['record']}"
                )
