import sys
import time
import logging
from pathlib import Path

import pandas as pd

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from config import DOWNLOADS_DIR, STORAGE_LOG_DIR       
from storage.database import get_connection, create_all

DTYPE_MAP = {
    "ride_id": "string",
    "rideable_type": "string",
    "start_station_name": "string",
    "start_station_id": "string",
    "end_station_name": "string",
    "end_station_id": "string",
    "member_casual": "string",
    "start_lat": "float64",
    "start_lng": "float64",
    "end_lat": "float64",
    "end_lng": "float64",
}
PARSE_DATES = ["started_at", "ended_at"]
CHUNK_SIZE = 100_000

def setup_loader_logging():
    logger = logging.getLogger()
    fh = logging.FileHandler(STORAGE_LOG_DIR / "loader.log")
    fh.setLevel(logging.INFO)
    fmt = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    fh.setFormatter(fmt)
    logger.addHandler(fh)

def load_csv_to_duckdb(csv_path, conn):
    total_rows = 0
    try:
        reader = pd.read_csv(
            csv_path,
            dtype=DTYPE_MAP,
            parse_dates=PARSE_DATES,
            chunksize=CHUNK_SIZE,
            encoding="utf-8",
        )
        for chunk in reader:
            conn.register("chunk_df", chunk)
            conn.execute("INSERT OR IGNORE INTO raw_rides SELECT * FROM chunk_df")
            conn.unregister("chunk_df")
            total_rows += len(chunk)
    except Exception as e:
        logging.error(f"Error loading {csv_path.name}: {e}")
        return 0
    return total_rows

def main():
    setup_loader_logging()
    conn = get_connection()
    create_all(conn)

    csv_files = sorted(DOWNLOADS_DIR.glob("*.csv"))

    for csv_file in csv_files:
        start = time.time()
        logging.info(f"Loading {csv_file.name} …")
        rows = load_csv_to_duckdb(csv_file, conn)
        elapsed = time.time() - start
        conn.execute(
            "INSERT INTO ingestion_log (file_name, rows_loaded, started_at, finished_at, status) "
            "VALUES (?, ?, CURRENT_TIMESTAMP, CURRENT_TIMESTAMP, 'success')",
            [csv_file.name, rows],
        )
        print(f"{rows} rows in {elapsed:.2f}s")

    total = conn.execute("SELECT COUNT(*) FROM raw_rides").fetchone()[0]
    print(f"\nTotal rows in raw_rides: {total}")
    conn.close()

if __name__ == "__main__":
    main()