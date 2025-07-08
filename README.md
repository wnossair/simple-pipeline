# Market Data ETL Pipeline

## Description

This project is a simple ETL (Extract, Transform, Load) pipeline designed to process financial market data from JSONL files. It extracts trade and quote events, transforms them into a structured format, validates the data, and loads it into a SQLite database. Finally, it generates a transaction cost analysis report from the processed data.

## Features

* **Extract**: Reads market data events (trades and quotes) from JSONL files.
* **Validate**: Performs validation on timestamps and prices to ensure data quality.
* **Transform**: Converts raw data into a clean, flat, and structured format.
* **Load**: Loads the transformed data into `trades` and `quotes` tables in a SQLite database.
* **Report**: Calculates transaction costs based on the loaded data and generates a summary report in both text and CSV formats.
* **Logging**: Logs the pipeline's operations and any errors encountered to both the console and a log file.

## Requirements

* Python 3.x
* The libraries listed in `requirements.txt`. The primary dependency is `pandas`.
* Docker (for containerized execution)

## Setup and Installation

1. **Clone the repository:**
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Create and activate a virtual environment (recommended for local development):**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows, use `.venv\Scripts\activate`
   ```

3. **Install the required dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Place your raw data files (in `jsonl` format) into the `data/` directory at the root of the project. If this directory does not exist, you will need to create it.
2. Run the main pipeline script from the project's root directory:
   ```bash
   python src/pipeline.py
   ```
   The script will process all `.jsonl` files found in the `data/` directory.

## Running with Docker

This project includes a `Dockerfile` to allow you to build and run the pipeline in a containerized environment. This is the recommended way to run the application to ensure consistency.

### Build the Docker Image

From the root directory of the project, run the following command to build the Docker image:
```bash
docker build -t market-data-etl .
```

### Run the Docker Container

Once the image is built, you can run the pipeline by starting a container. You need to mount the `data` and `output` directories from your local machine to the container so that the application can read the input files and write the output files.

1. Make sure you have your `.jsonl` data files in a `data` directory in the root of the project.
2. Create an empty `output` directory in the root of the project.
3. Run the following command to start the container:
```bash
docker run --rm \
  -v "$(pwd)/data:/app/data" \
  -v "$(pwd)/output:/app/output" \
  market-data-etl
```
The application will run, and the output files will be created in the `output` directory on your local machine.

## Project Structure

```
├── .dockerignore
├── .gitignore
├── Dockerfile
├── data/
│   └── (Your JSONL data files go here)
├── output/
│   ├── etl_pipeline.log
│   ├── market_data.db
│   ├── tx_report.csv
│   └── tx_report.txt
├── requirements.txt
└── src/
    ├── config.py           # Configuration settings, including file paths.
    ├── extract.py          # Extracts data from JSONL files.
    ├── transform.py        # Transforms and validates data.
    ├── load.py             # Loads data into the SQLite database.
    ├── report.py           # Generates the transaction cost report.
    ├── pipeline.py         # Main script to orchestrate the ETL process.
    ├── models.py           # Data validation models.
    └── logging_config.py   # Logging configuration.
```

## Configuration

All configuration is handled in the `src/config.py` file. You can modify the following paths:

* `DATA_DIR`: The directory where the input JSONL files are located.
* `OUTPUT_DIR`: The directory where all output files will be saved.
* `DB_PATH`: The path to the SQLite database file.
* `LOG_FILE`: The path to the log file.

## Output

The pipeline generates the following files in the `output/` directory:

* `market_data.db`: An SQLite database file containing the `trades` and `quotes` tables with the processed data.
* `etl_pipeline.log`: A log file containing detailed information about the pipeline's execution.
* `tx_report.txt`: A human-readable text report summarizing the average transaction cost and number of trades for each symbol.
* `tx_report.csv`: A CSV file containing the same transaction cost report data for easier analysis.
