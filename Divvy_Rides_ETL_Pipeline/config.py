# config.py
from pathlib import Path

# Base directory of the project (where this config.py lives)
BASE_DIR = Path(__file__).resolve().parent

# Centralised logs directory (top‑level "logs")
LOG_DIR = BASE_DIR / "logs"
LOG_DIR.mkdir(exist_ok=True)

# DuckDB database – you can keep it in "scraper" or move it here; I'll set it to root
DB_PATH = BASE_DIR / "divvy.duckdb"           # single, central database

# Raw CSV files (the ones downloaded by your threadpool script)
DOWNLOADS_DIR = BASE_DIR / "data" / "raw"     # matches your structure

# Other directories (optional)
SCRAPER_LOG_DIR = LOG_DIR / "scraper"
SCRAPER_LOG_DIR.mkdir(exist_ok=True)

STORAGE_LOG_DIR = LOG_DIR / "storage"
STORAGE_LOG_DIR.mkdir(exist_ok=True)

DOWNLOAD_LOG_FILE = LOG_DIR / "download.log"