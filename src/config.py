# config.py
"""This module contains configuration settings for the Market Data ETL pipeline."""

from pathlib import Path

class Config:
    """Class containing configuration settings.

    This class defines various paths and parameters used throughout the Market
    Data ETL pipeline, such as data directories, output directories, database paths,
    and log file paths.
    """
    # Get the directory where this config.py file is located ('.../src/')
    SRC_DIR = Path(__file__).resolve().parent

    # Get the base directory of the project ('.../simple-pipeline/')
    BASE_DIR = SRC_DIR.parent

    # Define paths relative to the project's base directory
    DATA_DIR = BASE_DIR / "data"
    OUTPUT_DIR = BASE_DIR / "output"
    DB_PATH = OUTPUT_DIR / "market_data.db"
    LOG_FILE = OUTPUT_DIR / "etl_pipeline.log"
