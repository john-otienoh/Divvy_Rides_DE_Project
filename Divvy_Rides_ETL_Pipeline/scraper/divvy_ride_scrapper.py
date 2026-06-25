#!/usr/bin/env python3
"""
Scrape the Divvy Tripdata S3 index page and store file metadata in a sqlite database.
"""
import re
import sys
import xml.etree.ElementTree as ET
import logging
from pathlib import Path
from typing import List, Dict

import requests
import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import DB_PATH, SCRAPER_LOG_DIR

# Configuration
BASE_URL = "https://divvy-tripdata.s3.amazonaws.com/"          

# Size constants matching the original JavaScript logic (SI units)
KB = 1024
MB = 1_000_000
GB = 1_000_000_000

# Regex to detect file extensions (like .zip, .html)
EXT_PATTERN = re.compile(r'\.([a-zA-Z0-9]{1,10})$')

# Logging
def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")

    # Console handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # File handler – now writes to the central logs/scraper/
    fh = logging.FileHandler(SCRAPER_LOG_DIR / "scrape.log", encoding='utf-8')
    fh.setFormatter(fmt)
    logger.addHandler(fh)

# Friendly size 
def friendly_size(size_bytes: int) -> str:
    """Convert bytes to human-readable string as done in the S3 index page."""
    if size_bytes == 0:
        return ''
    elif size_bytes < KB:
        return f"{size_bytes} B"
    elif size_bytes < MB:
        return f"{size_bytes / KB:.0f} KB"
    elif size_bytes < GB:
        return f"{size_bytes / MB:.2f} MB"
    else:
        return f"{size_bytes / GB:.2f} GB"

def friendly_type(filename: str) -> str:
    """Determine type string (e.g. 'ZIP file') from extension."""
    m = EXT_PATTERN.search(filename)
    if m:
        return f"{m.group(1).upper()} file"
    return "Unknown"

# Fetch and parse the S3 XML
def fetch_file_list(url: str) -> List[Dict]:
    """Return list of dicts with keys: name, last_modified, size_bytes, size_friendly, type."""
    logging.info(f"Fetching S3 bucket listing from {url}")
    resp = requests.get(url, timeout=30)
    resp.raise_for_status()

    # Parse XML
    root = ET.fromstring(resp.text)
    ns = {'s3': 'http://s3.amazonaws.com/doc/2006-03-01/'}
    files = []
    for contents in root.findall('s3:Contents', ns):
        key = contents.find('s3:Key', ns).text
        if key.endswith('/'):
            continue
        last_modified = contents.find('s3:LastModified', ns).text
        size_str = contents.find('s3:Size', ns).text
        size_bytes = int(size_str)

        file_name = key.split('/')[-1]  
        file_url = BASE_URL + file_name 
        files.append({
            'name': file_name,
            'url': file_url,
            'last_modified': last_modified,
            'size_bytes': size_bytes,
            'size_friendly': friendly_size(size_bytes),
            'type': friendly_type(file_name),
        })
    logging.info(f"Extracted {len(files)} file entries")
    return files

# Database helpers
def init_duckdb(db_path: str):
    conn = duckdb.connect(str(DB_PATH))
    conn.execute("""
        CREATE TABLE IF NOT EXISTS files (
            name VARCHAR,
            url VARCHAR,
            last_modified VARCHAR,
            size_bytes BIGINT,
            size_friendly VARCHAR,
            type VARCHAR,
            scraped_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    return conn

def insert_duckdb(conn, files: List[Dict]):
    conn.execute("DELETE FROM files")
    for f in files:
        conn.execute("""
            INSERT INTO files (name, url, last_modified, size_bytes, size_friendly, type)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (f['name'], f['url'], f['last_modified'], f['size_bytes'],
              f['size_friendly'], f['type']))
    logging.info(f"Inserted {len(files)} rows into DuckDB")

def main():
    setup_logging()
    logging.info("Starting Divvy S3 scraper (XML API)")

    try:
        files = fetch_file_list(BASE_URL)
    except Exception as e:
        logging.error(f"Failed to fetch/parse S3 listing: {e}")
        sys.exit(1)

    conn = init_duckdb(DB_PATH)
    insert_duckdb(conn, files)
    cnt = conn.execute("SELECT COUNT(*) FROM files").fetchone()[0]
    conn.close()

    logging.info(f"Done. {cnt} files stored in {DB_PATH}")

if __name__ == "__main__":
    main()