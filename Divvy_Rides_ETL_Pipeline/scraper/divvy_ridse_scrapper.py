#!/usr/bin/env python3
"""
Scrape the Divvy Tripdata S3 index page and store file metadata in a sqlite database.
"""
import re
import sys
import logging
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional

import requests
from bs4 import BeautifulSoup
import duckdb  
import sqlite3 

# Configuration
INDEX_URL = "https://divvy-tripdata.s3.amazonaws.com/index.html"
DB_TYPE = "sqlite"          
DB_PATH = "divvy_files.db"  
LOG_DIR = Path("logs")
LOG_FILE = LOG_DIR / "scrape.log"


# Regex to parse size strings
SIZE_PATTERN = re.compile(r'([\d.]+)\s*(KB|MB|GB|TB|B)', re.IGNORECASE)

def setup_logging():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=[
            logging.FileHandler(LOG_FILE, encoding='utf-8'),
            logging.StreamHandler(sys.stdout)
        ]
    )