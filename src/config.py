# config.py
"""This module contains configuration settings for the Market Data ETL pipeline."""

from pathlib import Path

class Config:
    """Class containing configuration settings.
    
    This class defines various paths and parameters used throughout the Market 
    Data ETL pipeline, such as data directories, output directories, database paths,
    and log file paths.
    """

    DATA_DIR = Path("../data")
    OUTPUT_DIR = Path("../output")
    DB_PATH = Path(OUTPUT_DIR, "market_data.db")
    LOG_FILE = Path(OUTPUT_DIR, "etl_pipeline.log")
