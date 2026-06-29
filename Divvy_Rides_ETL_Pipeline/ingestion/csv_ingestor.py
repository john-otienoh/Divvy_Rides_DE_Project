#!/usr/bin/env python3
"""Download Divvy tripdata ZIPs using a thread pool – centralised config."""

import logging
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from urllib.parse import urlparse
import zipfile
import duckdb

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from config import DOWNLOADS_DIR, LOG_DIR, DOWNLOAD_LOG_FILE, DB_PATH

# Configuration
REQUEST_TIMEOUT = 60
CHUNK_SIZE = 8192
MAX_RETRIES = 3
BACKOFF_FACTOR = 0.5
MAX_WORKERS = 5

# Logging
def setup_logging():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)
    fmt = logging.Formatter(
        "%(asctime)s - %(levelname)s - %(message)s", datefmt="%Y-%m-%d %H:%M:%S"
    )

    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(logging.INFO)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    fh = logging.FileHandler(DOWNLOAD_LOG_FILE, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

# URL validation
def create_retry_session() -> requests.Session:
    session = requests.Session()
    retry_strategy = Retry(
        total=MAX_RETRIES,
        backoff_factor=BACKOFF_FACTOR,
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["HEAD", "GET"],
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("https://", adapter)
    session.mount("http://", adapter)
    return session

def top_recent_file_urls(db_path: str, limit: int = 5) -> list[str]:
    """
    Return a list of download URLs for the most recently modified files.
    """
    conn = duckdb.connect(db_path, read_only=True)
    try:
        result = conn.execute("""
            SELECT url
            FROM files
            ORDER BY last_modified DESC
            LIMIT ?
        """, [limit]).fetchall()
        return [row[0] for row in result]
    finally:
        conn.close()

def check_url_validity(url: str) -> bool:
    """Return True if a HEAD request succeeds (status < 400)."""
    with create_retry_session() as session:
        try:
            resp = session.head(url, timeout=10, allow_redirects=True)
            if resp.status_code < 400:
                logging.info(f"Valid: {url} (status {resp.status_code})")
                return True
            else:
                logging.warning(f"Invalid: {url} (status {resp.status_code})")
                return False
        except requests.RequestException as e:
            logging.warning(f"Unreachable: {url} ({e})")
            return False

# Download
def download_file(url: str, dest: Path) -> bool:
    """Download a file with streaming, retries, and cleanup on failure."""
    session = create_retry_session()
    try:
        logging.info(f"Downloading {url}")
        with session.get(url, stream=True, timeout=REQUEST_TIMEOUT) as resp:
            resp.raise_for_status()
            with open(dest, "wb") as f:
                for chunk in resp.iter_content(chunk_size=CHUNK_SIZE):
                    if chunk:
                        f.write(chunk)
        logging.info(f"Downloaded {dest.name}")
        return True
    except Exception as e:
        logging.error(f"Download failed: {url} - {e}")
        if dest.exists():
            dest.unlink()
        return False

# Extraction
def extract_csv_and_delete_zip(zip_path: Path, extract_to: Path) -> bool:
    """Extract all .csv files, then delete the ZIP."""
    csv_found = False
    try:
        with zipfile.ZipFile(zip_path, "r") as zf:
            for member in zf.namelist():
                if member.lower().endswith(".csv") and not Path(member).name.startswith("._"):
                    target = extract_to / Path(member).name
                    with zf.open(member) as src, open(target, "wb") as dst:
                        dst.write(src.read())
                    csv_found = True
                    logging.info(f"Extracted {target.name}")
    except zipfile.BadZipFile as e:
        logging.error(f"Bad ZIP {zip_path}: {e}")
    except Exception as e:
        logging.error(f"Extraction error {zip_path}: {e}")
    finally:
        try:
            zip_path.unlink()
            logging.info(f"Deleted ZIP {zip_path.name}")
        except Exception as e:
            logging.error(f"Could not delete {zip_path}: {e}")
    return csv_found

# Single task for a thread
def process_one(url: str) -> bool:
    """Download + extract for a single URL."""
    filename = Path(urlparse(url).path).name
    zip_path = DOWNLOADS_DIR / filename
    if not download_file(url, zip_path):
        return False
    return extract_csv_and_delete_zip(zip_path, DOWNLOADS_DIR)

# Main
def main():
    setup_logging()
    DOWNLOADS_DIR.mkdir(parents=True, exist_ok=True)  

    # Validate URLs first
    logging.info("Validating URLs...")
    URLS = top_recent_file_urls(db_path=str(DB_PATH))
    valid_urls = [url for url in URLS if check_url_validity(url)]
    logging.info(f"{len(valid_urls)}/{len(URLS)} URLs are valid.")

    if not valid_urls:
        logging.error("No valid URLs to process.")
        return

    # Process with thread pool
    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_url = {executor.submit(process_one, url): url for url in valid_urls}
        for future in as_completed(future_to_url):
            url = future_to_url[future]
            try:
                ok = future.result()
                if not ok:
                    logging.warning(f"Failed to process {url}")
            except Exception as e:
                logging.error(f"Unhandled error for {url}: {e}")

    logging.info("All downloads complete.")

if __name__ == "__main__":
    main()