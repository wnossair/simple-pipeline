# pipeline.py
"""This is the main module for the Market Data ETL pipeline.
It orchestrates the extraction, transformation, and loading of market data."""

from config import Config
from logging_config import setup_logging
from extract import Extractor
from transform import Transformer
from load import Loader
from report import Reporter

class MarketDataETL:
    """Class responsible for executing the entire Market Data ETL pipeline.
    
    This class initializes all necessary components and orchestrates their interaction 
    to process market data from JSONL files, transform it, and load it into a database.
    """

    def __init__(self):
        # Create the output directory if it doesn't exist
        Config.OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

        self.logger = setup_logging(Config.LOG_FILE)
        self.extractor = Extractor(self.logger)
        self.transformer = Transformer(self.logger)
        self.loader = Loader(Config.DB_PATH, self.logger)
        self.bad_records = []

    def process_files(self) -> None:
        """Process all JSONL files in the data directory."""
        self.loader.initialize_database()

        for file_path in sorted(Config.DATA_DIR.glob('*.jsonl')):
            self.logger.info("Processing file: %s", file_path)
            trades, quotes = self.extractor.extract(file_path)
            transformed_trades, transformed_quotes = self.transformer.transform(trades, quotes)
            self.loader.load(transformed_trades, transformed_quotes)

            self.bad_records.extend(self.extractor.bad_records)

        reporter = Reporter(self.loader.conn, self.logger, Config.OUTPUT_DIR)
        reporter.generate_transaction_cost_report(self.bad_records)
        self.loader.close()

if __name__ == "__main__":
    etl = MarketDataETL()
    etl.process_files()
